# FULL SOURCE — `/opt/logos/airdrop-api`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/opt/logos/airdrop-api/app.py`

```py
# (БОЕВОЙ app.py с OAuth endpoints + verify последнего твита)
# ВНИМАНИЕ: файл большой; вставляется целиком одним heredoc.
# Если хочешь — я могу разбить на 2 cat-блока, но лучше одним.

from __future__ import annotations

import base64
import json
import logging
import os
import secrets
import time
from collections import deque
from contextlib import contextmanager
from typing import Any, Deque, Dict, Optional

from fastapi import FastAPI, Header, HTTPException, Request, Response
from pydantic import BaseModel, Field
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from x_oauth import pkce_pair, oauth_authorize_url, token_exchange, token_refresh, enc, dec, x_get


# -------------------- CONFIG --------------------

REF_TARGET = int(os.getenv("AIRDROP_REF_TARGET", "5"))
SITE_ORIGIN = (os.getenv("AIRDROP_SITE_ORIGIN", "https://mw-expedition.com") or "https://mw-expedition.com").rstrip("/")
AIRDROP_API_KEY = (os.getenv("AIRDROP_API_KEY", "") or "").strip()

DB_DSN = (os.getenv("AIRDROP_DB_DSN") or os.getenv("AIRDROP_PG_DSN") or "").strip()
if not DB_DSN:
    raise RuntimeError("AIRDROP_DB_DSN (or AIRDROP_PG_DSN) is required")

DB_POOL_MIN = int(os.getenv("AIRDROP_DB_POOL_MIN", "1"))
DB_POOL_MAX = int(os.getenv("AIRDROP_DB_POOL_MAX", "10"))

WALLET_CHALLENGE_TTL = int(os.getenv("AIRDROP_WALLET_CHALLENGE_TTL", "600"))
RATE_WINDOW_SEC = int(os.getenv("AIRDROP_RATE_WINDOW_SEC", "60"))
RATE_REGISTER_PER_IP = int(os.getenv("AIRDROP_RATE_REGISTER_PER_IP", "12"))
RATE_STATUS_PER_TOKEN = int(os.getenv("AIRDROP_RATE_STATUS_PER_TOKEN", "30"))
RATE_WALLET_PER_TOKEN = int(os.getenv("AIRDROP_RATE_WALLET_PER_TOKEN", "10"))
RATE_UPDATE_PER_TOKEN = int(os.getenv("AIRDROP_RATE_UPDATE_PER_TOKEN", "10"))

# OAuth/X
X_PROJECT_USERNAME = (os.getenv("X_PROJECT_USERNAME", "RspLogos") or "RspLogos").lstrip("@")
X_OAUTH_STATE_TTL = int(os.getenv("X_OAUTH_STATE_TTL", "600"))
X_OAUTH_STATE_GRACE = int(os.getenv("X_OAUTH_STATE_GRACE", "600"))
X_OAUTH_COOLDOWN = int(os.getenv("X_OAUTH_COOLDOWN", "180"))


# -------------------- LOGGING --------------------

log = logging.getLogger("airdrop-api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


# -------------------- DB --------------------

POOL = ConnectionPool(
    conninfo=DB_DSN,
    min_size=DB_POOL_MIN,
    max_size=DB_POOL_MAX,
    kwargs={"row_factory": dict_row},
)

@contextmanager
def get_cursor():
    with POOL.connection() as conn:
        with conn.cursor() as cur:
            yield conn, cur


def init_db() -> None:
    now = int(time.time())
    with get_cursor() as (conn, cur):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS airdrop_users (
              id            BIGSERIAL PRIMARY KEY,
              token         TEXT UNIQUE NOT NULL,
              ref_token     TEXT,
              wallet_bound  BOOLEAN NOT NULL DEFAULT FALSE,
              telegram_ok   BOOLEAN NOT NULL DEFAULT FALSE,
              twitter_follow   BOOLEAN NOT NULL DEFAULT FALSE,
              twitter_like     BOOLEAN NOT NULL DEFAULT FALSE,
              twitter_retweet  BOOLEAN NOT NULL DEFAULT FALSE,
              referrals     INTEGER NOT NULL DEFAULT 0,
              points        INTEGER NOT NULL DEFAULT 0,
              created_at    BIGINT NOT NULL,
              updated_at    BIGINT NOT NULL
            );
            """
        )

        # Wallet fields
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS wallet_rid TEXT;")
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS wallet_bound_at BIGINT NOT NULL DEFAULT 0;")
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS wallet_challenge TEXT;")
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS wallet_challenge_exp BIGINT NOT NULL DEFAULT 0;")

        # X fields
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS twitter_username TEXT;")
        cur.execute("ALTER TABLE airdrop_users ADD COLUMN IF NOT EXISTS twitter_checked_at BIGINT NOT NULL DEFAULT 0;")

        # OAuth state
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS airdrop_oauth_state (
              state         TEXT PRIMARY KEY,
              token         TEXT NOT NULL,
              code_verifier TEXT NOT NULL,
              created_at    BIGINT NOT NULL,
              exp_at        BIGINT NOT NULL
            );
            """
        )
        cur.execute("CREATE INDEX IF NOT EXISTS idx_oauth_state_exp ON airdrop_oauth_state(exp_at);")

        # OAuth tokens (encrypted)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS airdrop_x_oauth (
              token           TEXT PRIMARY KEY,
              x_user_id       TEXT NOT NULL,
              access_token_e  TEXT NOT NULL,
              refresh_token_e TEXT,
              expires_at      BIGINT NOT NULL DEFAULT 0,
              updated_at      BIGINT NOT NULL
            );
            """
        )

        # Indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_airdrop_points ON airdrop_users(points DESC);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_airdrop_token ON airdrop_users(token);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_airdrop_ref_token ON airdrop_users(ref_token);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_airdrop_twitter_username ON airdrop_users(twitter_username);")

        # Unique wallet rid
        cur.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_airdrop_wallet_rid_unique "
            "ON airdrop_users(wallet_rid) WHERE wallet_rid IS NOT NULL;"
        )

        conn.commit()

    log.info("airdrop-api db init ok (ts=%s)", now)


# -------------------- METRICS --------------------

REQS = Counter("airdrop_http_requests_total", "HTTP requests", ["path", "method", "status"])
LAT = Histogram("airdrop_http_request_duration_seconds", "HTTP request latency", ["path", "method"])

REG_TOTAL = Counter("airdrop_register_total", "Register attempts", ["result"])
STATUS_TOTAL = Counter("airdrop_status_total", "Status calls", ["result"])
UPDATE_TOTAL = Counter("airdrop_update_total", "Update calls", ["result"])


# -------------------- RATE LIMIT --------------------

_buckets: Dict[str, Deque[float]] = {}

def _rate_ok(key: str, limit: int) -> bool:
    now = time.monotonic()
    b = _buckets.setdefault(key, deque())
    while b and (now - b[0]) > RATE_WINDOW_SEC:
        b.popleft()
    if len(b) >= limit:
        return False
    b.append(now)
    return True


# -------------------- HELPERS --------------------

def get_ip(request: Request) -> str:
    xf = request.headers.get("x-forwarded-for", "")
    if xf:
        return xf.split(",")[0].strip()
    return request.client.host if request.client else "0.0.0.0"

_B58_ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_B58_IDX = {c: i for i, c in enumerate(_B58_ALPH)}

def b58decode(s: str) -> bytes:
    s = (s or "").strip()
    if not s:
        return b""
    num = 0
    for ch in s:
        if ch not in _B58_IDX:
            raise ValueError("invalid base58 char")
        num = num * 58 + _B58_IDX[ch]
    pad = 0
    for ch in s:
        if ch == "1":
            pad += 1
        else:
            break
    full = num.to_bytes((num.bit_length() + 7) // 8, "big") if num > 0 else b""
    return (b"\x00" * pad) + full

def b64url_decode(s: str) -> bytes:
    s = (s or "").strip()
    if not s:
        return b""
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * (-len(s) % 4)
    return base64.b64decode(s.encode("ascii"))

def compute_points(wallet_bound: bool, telegram_ok: bool, twitter_follow: bool, twitter_like: bool, twitter_retweet: bool, referrals: int) -> int:
    flags = int(wallet_bound) + int(telegram_ok) + int(twitter_like) + int(twitter_retweet)
    refs = min(int(referrals or 0), REF_TARGET)
    return flags * 20 + refs * 10

def _norm_x_username(s: str) -> str:
    s = (s or "").strip()
    if s.startswith("@"):
        s = s[1:]
    s = s.replace("https://x.com/", "").replace("http://x.com/", "")
    s = s.replace("https://twitter.com/", "").replace("http://twitter.com/", "")
    s = s.split("?")[0].split("/")[0].strip().lower()
    if not s or len(s) > 32:
        raise ValueError("bad twitter_username")
    return s

def _now() -> int:
    return int(time.time())


# -------------------- MODELS --------------------

class RegisterRequest(BaseModel):
    ref_token: Optional[str] = None

class RegisterResponse(BaseModel):
    ok: bool = True
    token: str

class StatusRequest(BaseModel):
    token: str

class AirdropStatus(BaseModel):
    ok: bool = True
    token: str
    points: int
    referrals: int
    ref_target: int
    wallet_bound: bool
    wallet_rid: Optional[str] = None
    telegram_ok: bool
    twitter_follow: bool
    twitter_like: bool
    twitter_retweet: bool
    rank: int
    total: int
    site_origin: str = SITE_ORIGIN

class UpdateRequest(BaseModel):
    token: str
    wallet_bound: Optional[bool] = None
    telegram_ok: Optional[bool] = None
    twitter_follow: Optional[bool] = None
    twitter_like: Optional[bool] = None
    twitter_retweet: Optional[bool] = None
    referrals: Optional[int] = None

class SetXUsernameRequest(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)
    twitter_username: str = Field(..., min_length=1, max_length=128)

class VerifyXRequest(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)

class OAuthStartReq(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)


# -------------------- APP --------------------

app = FastAPI(title="LOGOS Airdrop API", version="1.3.0-oauth-per-user")


@app.on_event("startup")
def _startup():
    init_db()
    log.info("airdrop-api started")


@app.middleware("http")
async def _metrics_mw(request: Request, call_next):
    path = request.url.path
    method = request.method
    start = time.perf_counter()
    status = "500"
    try:
        resp = await call_next(request)
        status = str(resp.status_code)
        return resp
    finally:
        dur = time.perf_counter() - start
        LAT.labels(path=path, method=method).observe(dur)
        REQS.labels(path=path, method=method, status=status).inc()


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": "airdrop-api"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def _status_for_token(token: str) -> AirdropStatus:
    with get_cursor() as (conn, cur):
        cur.execute("SELECT * FROM airdrop_users WHERE token=%s", (token,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="token not found")

        wallet_bound = bool(row.get("wallet_bound"))
        telegram_ok = bool(row.get("telegram_ok"))
        twitter_follow = bool(row.get("twitter_follow"))
        twitter_like = bool(row.get("twitter_like"))
        twitter_retweet = bool(row.get("twitter_retweet"))
        referrals = int(row.get("referrals") or 0)

        points = int(row.get("points") or 0)
        if points == 0 and (wallet_bound or telegram_ok or twitter_follow or twitter_like or twitter_retweet or referrals):
            points = compute_points(wallet_bound, telegram_ok, twitter_follow, twitter_like, twitter_retweet, referrals)
            cur.execute("UPDATE airdrop_users SET points=%s, updated_at=%s WHERE token=%s", (points, _now(), token))
            conn.commit()

        cur.execute("SELECT COUNT(*) AS n FROM airdrop_users")
        total = int((cur.fetchone() or {}).get("n") or 0)

        cur.execute("SELECT COUNT(*) AS better FROM airdrop_users WHERE points > %s", (points,))
        better = int((cur.fetchone() or {}).get("better") or 0)
        rank = better + 1

        return AirdropStatus(
            token=token,
            points=points,
            referrals=min(referrals, REF_TARGET),
            ref_target=REF_TARGET,
            wallet_bound=wallet_bound,
            wallet_rid=row.get("wallet_rid"),
            telegram_ok=telegram_ok,
            twitter_follow=twitter_follow,
            twitter_like=twitter_like,
            twitter_retweet=twitter_retweet,
            rank=rank,
            total=total,
        )


@app.post("/api/airdrop/register_web", response_model=RegisterResponse)
def register_web(req: RegisterRequest, request: Request):
    ip = get_ip(request)
    if not _rate_ok(f"reg:{ip}", RATE_REGISTER_PER_IP):
        REG_TOTAL.labels(result="rate_limited").inc()
        raise HTTPException(status_code=429, detail="rate limit: register")

    now = _now()
    token = secrets.token_urlsafe(16)

    with get_cursor() as (conn, cur):
        cur.execute(
            "INSERT INTO airdrop_users(token, ref_token, created_at, updated_at) VALUES (%s, %s, %s, %s)",
            (token, (req.ref_token or None), now, now),
        )

        if req.ref_token:
            cur.execute("SELECT * FROM airdrop_users WHERE token=%s FOR UPDATE", (req.ref_token,))
            ref_row = cur.fetchone()
            if ref_row:
                new_refs = min(REF_TARGET, int(ref_row.get("referrals") or 0) + 1)
                new_points = compute_points(
                    bool(ref_row.get("wallet_bound")),
                    bool(ref_row.get("telegram_ok")),
                    bool(ref_row.get("twitter_follow")),
                    bool(ref_row.get("twitter_like")),
                    bool(ref_row.get("twitter_retweet")),
                    new_refs,
                )
                cur.execute(
                    "UPDATE airdrop_users SET referrals=%s, points=%s, updated_at=%s WHERE token=%s",
                    (new_refs, new_points, now, req.ref_token),
                )

        conn.commit()

    REG_TOTAL.labels(result="ok").inc()
    return RegisterResponse(ok=True, token=token)


@app.post("/api/airdrop/status", response_model=AirdropStatus)
def status(req: StatusRequest, request: Request):
    tok = (req.token or "").strip()
    if not tok:
        STATUS_TOTAL.labels(result="bad_req").inc()
        raise HTTPException(status_code=400, detail="token required")

    ip = get_ip(request)
    if not _rate_ok(f"st:{tok}:{ip}", RATE_STATUS_PER_TOKEN):
        STATUS_TOTAL.labels(result="rate_limited").inc()
        raise HTTPException(status_code=429, detail="rate limit: status")

    STATUS_TOTAL.labels(result="ok").inc()
    return _status_for_token(tok)


@app.post("/api/airdrop/update", response_model=AirdropStatus)
def update(req: UpdateRequest, request: Request, x_api_key: Optional[str] = Header(default=None, alias="x-api-key")):
    if not AIRDROP_API_KEY:
        UPDATE_TOTAL.labels(result="server_misconf").inc()
        raise HTTPException(status_code=500, detail="AIRDROP_API_KEY is not set")
    if (x_api_key or "").strip() != AIRDROP_API_KEY:
        UPDATE_TOTAL.labels(result="unauthorized").inc()
        raise HTTPException(status_code=401, detail="bad api key")

    tok = (req.token or "").strip()
    if not tok:
        UPDATE_TOTAL.labels(result="bad_req").inc()
        raise HTTPException(status_code=400, detail="token required")

    ip = get_ip(request)
    if not _rate_ok(f"upd:{tok}:{ip}", RATE_UPDATE_PER_TOKEN):
        UPDATE_TOTAL.labels(result="rate_limited").inc()
        raise HTTPException(status_code=429, detail="rate limit: update")

    now = _now()
    with get_cursor() as (conn, cur):
        cur.execute("SELECT * FROM airdrop_users WHERE token=%s FOR UPDATE", (tok,))
        row = cur.fetchone()
        if not row:
            UPDATE_TOTAL.labels(result="not_found").inc()
            raise HTTPException(status_code=404, detail="token not found")

        wallet_bound = bool(row.get("wallet_bound"))
        telegram_ok = bool(row.get("telegram_ok"))
        twitter_follow = bool(row.get("twitter_follow"))
        twitter_like = bool(row.get("twitter_like"))
        twitter_retweet = bool(row.get("twitter_retweet"))
        referrals = int(row.get("referrals") or 0)

        if req.telegram_ok is not None:
            telegram_ok = bool(req.telegram_ok)
        if req.twitter_follow is not None:
            twitter_follow = bool(req.twitter_follow)
        if req.twitter_like is not None:
            twitter_like = bool(req.twitter_like)
        if req.twitter_retweet is not None:
            twitter_retweet = bool(req.twitter_retweet)
        if req.referrals is not None:
            referrals = max(referrals, int(req.referrals))
        referrals = min(referrals, REF_TARGET)

        points = compute_points(wallet_bound, telegram_ok, twitter_follow, twitter_like, twitter_retweet, referrals)

        cur.execute(
            """
            UPDATE airdrop_users
            SET telegram_ok=%s,
                twitter_follow=%s,
                twitter_like=%s,
                twitter_retweet=%s,
                referrals=%s,
                points=%s,
                updated_at=%s
            WHERE token=%s
            """,
            (telegram_ok, twitter_follow, twitter_like, twitter_retweet, referrals, points, now, tok),
        )
        conn.commit()

    UPDATE_TOTAL.labels(result="ok").inc()
    return _status_for_token(tok)


# -------------------- OAuth endpoints --------------------

@app.post("/api/x/oauth/start")
def x_oauth_start(req: OAuthStartReq):
    tok = req.token.strip()
    now = _now()

    with get_cursor() as (conn, cur):
        cur.execute("SELECT token FROM airdrop_users WHERE token=%s", (tok,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="token_not_found")

        state = secrets.token_urlsafe(24)
        verifier, challenge = pkce_pair()
        exp = now + X_OAUTH_STATE_TTL

        cur.execute(
            "INSERT INTO airdrop_oauth_state(state, token, code_verifier, created_at, exp_at) VALUES (%s,%s,%s,%s,%s)",
            (state, tok, enc(verifier), now, exp),
        )
        conn.commit()

    return {"ok": True, "auth_url": oauth_authorize_url(state, challenge)}


@app.get("/api/x/oauth/callback")
def x_oauth_callback(state: str, code: str):
    now = _now()

    with get_cursor() as (conn, cur):
        cur.execute("SELECT * FROM airdrop_oauth_state WHERE state=%s", (state,))
        st = cur.fetchone()
        if not st:
            raise HTTPException(status_code=400, detail="bad_state")
        if int(st.get("exp_at") or 0) < (now - X_OAUTH_STATE_GRACE):
            cur.execute("DELETE FROM airdrop_oauth_state WHERE state=%s", (state,))
            conn.commit()
            raise HTTPException(status_code=400, detail="state_expired")

        tok = st["token"]
        verifier = dec(st["code_verifier"])
        cur.execute("DELETE FROM airdrop_oauth_state WHERE state=%s", (state,))
        conn.commit()

    tr = token_exchange(code, verifier)
    access = tr.get("access_token")
    refresh = tr.get("refresh_token")
    expires_in = int(tr.get("expires_in") or 0)
    if not access:
        raise HTTPException(status_code=502, detail="oauth_token_exchange_failed")

    me = x_get("/2/users/me", access)
    x_user_id = (((me or {}).get("data") or {}) or {}).get("id")
    if not x_user_id:
        raise HTTPException(status_code=502, detail="x_me_failed")

    exp_at = now + expires_in if expires_in > 0 else 0

    with get_cursor() as (conn, cur):
        cur.execute(
            """
            INSERT INTO airdrop_x_oauth(token, x_user_id, access_token_e, refresh_token_e, expires_at, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT(token) DO UPDATE SET
              x_user_id=EXCLUDED.x_user_id,
              access_token_e=EXCLUDED.access_token_e,
              refresh_token_e=EXCLUDED.refresh_token_e,
              expires_at=EXCLUDED.expires_at,
              updated_at=EXCLUDED.updated_at
            """,
            (tok, x_user_id, enc(access), enc(refresh) if refresh else None, exp_at, now),
        )
        conn.commit()

    # return to airdrop page
    return Response(status_code=302, headers={"Location": f"{SITE_ORIGIN}/airdrop?oauth=ok"})


def _get_oauth_access(tok: str) -> Optional[str]:
    now = _now()
    with get_cursor() as (conn, cur):
        cur.execute("SELECT * FROM airdrop_x_oauth WHERE token=%s", (tok,))
        row = cur.fetchone()
        if not row:
            return None
        access = dec(row["access_token_e"])
        refresh_e = row.get("refresh_token_e")
        refresh = dec(refresh_e) if refresh_e else None
        exp_at = int(row.get("expires_at") or 0)

    if refresh and exp_at and exp_at < now + 60:
        tr = token_refresh(refresh)
        new_access = tr.get("access_token")
        new_refresh = tr.get("refresh_token") or refresh
        expires_in = int(tr.get("expires_in") or 0)
        if new_access:
            new_exp = now + expires_in if expires_in > 0 else 0
            with get_cursor() as (conn, cur):
                cur.execute(
                    "UPDATE airdrop_x_oauth SET access_token_e=%s, refresh_token_e=%s, expires_at=%s, updated_at=%s WHERE token=%s",
                    (enc(new_access), enc(new_refresh) if new_refresh else None, new_exp, now, tok),
                )
                conn.commit()
            return new_access
    return access


def _x_me(access: str) -> str:
    me = x_get("/2/users/me", access)
    myid = (((me or {}).get("data") or {}) or {}).get("id")
    if not myid:
        raise RuntimeError("x_me_failed")
    return str(myid)

def _x_user_id_by_username(access: str, username: str) -> str:
    target = x_get(f"/2/users/by/username/{username}", access)
    tid = (((target or {}).get("data") or {}) or {}).get("id")
    if not tid:
        raise RuntimeError("x_user_lookup_failed")
    return str(tid)

def _x_latest_tweet_id(access: str, user_id: str) -> str:
    # last non-reply tweet
    data = x_get(f"/2/users/{user_id}/tweets?max_results=5&exclude=replies", access)
    arr = (data or {}).get("data") or []
    if not arr:
        # fallback: include replies
        data = x_get(f"/2/users/{user_id}/tweets?max_results=5", access)
        arr = (data or {}).get("data") or []
    if not arr:
        raise RuntimeError("no_recent_tweets")
    return str(arr[0].get("id"))

def _x_follow_ok(access: str, myid: str, target_id: str) -> bool:
    pagination = None
    for _ in range(3):
        path = f"/2/users/{myid}/following?max_results=100"
        if pagination:
            path += f"&pagination_token={pagination}"
        data = x_get(path, access)
        arr = (data or {}).get("data") or []
        for u in arr:
            if str(u.get("id")) == str(target_id):
                return True
        meta = (data or {}).get("meta") or {}
        pagination = meta.get("next_token")
        if not pagination:
            break
    return False

def _x_like_ok(access: str, myid: str, tweet_id: str) -> bool:
    pagination = None
    for _ in range(3):
        path = f"/2/users/{myid}/liked_tweets?max_results=100"
        if pagination:
            path += f"&pagination_token={pagination}"
        data = x_get(path, access)
        arr = (data or {}).get("data") or []
        for t in arr:
            if str(t.get("id")) == str(tweet_id):
                return True
        meta = (data or {}).get("meta") or {}
        pagination = meta.get("next_token")
        if not pagination:
            break
    return False

def _x_retweet_ok(access: str, myid: str, tweet_id: str) -> bool:
    pagination = None
    for _ in range(10):
        path = f"/2/tweets/{tweet_id}/retweeted_by?max_results=100"
        if pagination:
            path += f"&pagination_token={pagination}"
        data = x_get(path, access)
        arr = (data or {}).get("data") or []
        for u in arr:
            if str(u.get("id")) == str(myid):
                return True
        meta = (data or {}).get("meta") or {}
        pagination = meta.get("next_token")
        if not pagination:
            break
    return False



@app.post("/api/airdrop/set_x_username")
def set_x_username(req: SetXUsernameRequest):
    tok = req.token.strip()
    uname = _norm_x_username(req.twitter_username)
    now = _now()
    with get_cursor() as (conn, cur):
        cur.execute("UPDATE airdrop_users SET twitter_username=%s, updated_at=%s WHERE token=%s", (uname, now, tok))
        if cur.rowcount != 1:
            raise HTTPException(status_code=404, detail="token_not_found")
        conn.commit()
    return _status_for_token(tok)


@app.post("/api/airdrop/verify_x")
def verify_x(req: VerifyXRequest):
    tok = req.token.strip()
    now = _now()

    with get_cursor() as (conn, cur):
        cur.execute(
            "SELECT token,twitter_checked_at,twitter_follow,twitter_like,twitter_retweet,referrals,wallet_bound,telegram_ok FROM airdrop_users WHERE token=%s",
            (tok,),
        )
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="token_not_found")

    last = int(row.get("twitter_checked_at") or 0)
    if now - last < X_OAUTH_COOLDOWN:
        st = _status_for_token(tok).dict()
        st["ok"] = True
        st["x_retry_after"] = max(0, X_OAUTH_COOLDOWN - (now - last))
        return st

    access = _get_oauth_access(tok)

    with get_cursor() as (conn, cur):
        cur.execute("UPDATE airdrop_users SET twitter_checked_at=%s, updated_at=%s WHERE token=%s", (now, now, tok))
        conn.commit()

    if not access:
        return {"ok": False, "error": "x_oauth_required", "message": "Connect X first"}

    try:
        myid = _x_me(access)
        target_id = _x_user_id_by_username(access, X_PROJECT_USERNAME)
        last_tweet_id = _x_latest_tweet_id(access, target_id)

        follow_ok = True  # follow disabled (prod)
        like_ok = _x_like_ok(access, myid, last_tweet_id)
        rt_ok = _x_retweet_ok(access, myid, last_tweet_id)
    except Exception as e:
        return {"ok": False, "error": "x_oauth_check_failed", "message": str(e)}

    new_follow = bool(row.get("twitter_follow")) or bool(follow_ok)
    new_like = bool(row.get("twitter_like")) or bool(like_ok)
    new_rt = bool(row.get("twitter_retweet")) or bool(rt_ok)

    referrals = int(row.get("referrals") or 0)
    points = compute_points(bool(row.get("wallet_bound")), bool(row.get("telegram_ok")), new_follow, new_like, new_rt, referrals)

    with get_cursor() as (conn, cur):
        cur.execute(
            "UPDATE airdrop_users SET twitter_follow=%s, twitter_like=%s, twitter_retweet=%s, points=%s, updated_at=%s WHERE token=%s",
            (new_follow, new_like, new_rt, points, now, tok),
        )
        conn.commit()

    st = _status_for_token(tok).dict()
    st["ok"] = True
    st["x_latest_tweet_id"] = last_tweet_id
    return st

# -------------------- WALLET BIND (challenge + verify) --------------------

class WalletChallengeReq(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)
    wallet_rid: str = Field(..., min_length=8, max_length=128)

class WalletChallengeResp(BaseModel):
    ok: bool = True
    token: str
    wallet_rid: str
    challenge: str
    exp_at: int

class WalletBindReq(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)
    wallet_rid: str = Field(..., min_length=8, max_length=128)
    # wallet/connect.js отдаёт base64url подпись (64 байта)
    sig_b64: str = Field(..., min_length=32, max_length=256)

def _sig_b64url_to_bytes(sig_b64: str) -> bytes:
    s = (sig_b64 or "").strip().replace("-", "+").replace("_", "/")
    s += "=" * (-len(s) % 4)
    return base64.b64decode(s.encode("ascii"))

def _wallet_verify_sig(wallet_rid: str, challenge: str, sig_b64: str) -> bool:
    try:
        pk_bytes = b58decode(wallet_rid)
        if len(pk_bytes) != 32:
            return False
        sig = _sig_b64url_to_bytes(sig_b64)
        if len(sig) != 64:
            return False
        pub = Ed25519PublicKey.from_public_bytes(pk_bytes)
        pub.verify(sig, challenge.encode("utf-8"))
        return True
    except Exception:
        return False

@app.post("/api/airdrop/wallet_challenge", response_model=WalletChallengeResp)
def wallet_challenge(req: WalletChallengeReq, request: Request, x_api_key: Optional[str] = Header(default=None, alias="x-api-key")):
    if not AIRDROP_API_KEY:
        raise HTTPException(status_code=500, detail="AIRDROP_API_KEY is not set")
    if (x_api_key or "").strip() != AIRDROP_API_KEY:
        raise HTTPException(status_code=401, detail="bad api key")

    tok = req.token.strip()
    rid = req.wallet_rid.strip()
    ip = get_ip(request)
    if not _rate_ok(f"wchal:{tok}:{ip}", RATE_WALLET_PER_TOKEN):
        raise HTTPException(status_code=429, detail="rate limit: wallet_challenge")

    now = _now()
    exp = now + WALLET_CHALLENGE_TTL
    ch = secrets.token_urlsafe(24)

    with get_cursor() as (conn, cur):
        cur.execute("SELECT token,wallet_bound,wallet_rid FROM airdrop_users WHERE token=%s FOR UPDATE", (tok,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="token_not_found")

        # если уже привязан — возвращаем пустой challenge
        if bool(row.get("wallet_bound")) and (row.get("wallet_rid") == rid):
            return WalletChallengeResp(ok=True, token=tok, wallet_rid=rid, challenge="", exp_at=0)

        cur.execute(
            "UPDATE airdrop_users SET wallet_challenge=%s, wallet_challenge_exp=%s, updated_at=%s WHERE token=%s",
            (ch, exp, now, tok),
        )
        conn.commit()

    return WalletChallengeResp(ok=True, token=tok, wallet_rid=rid, challenge=ch, exp_at=exp)

@app.post("/api/airdrop/wallet_bind", response_model=AirdropStatus)
def wallet_bind(req: WalletBindReq, request: Request, x_api_key: Optional[str] = Header(default=None, alias="x-api-key")):
    if not AIRDROP_API_KEY:
        raise HTTPException(status_code=500, detail="AIRDROP_API_KEY is not set")
    if (x_api_key or "").strip() != AIRDROP_API_KEY:
        raise HTTPException(status_code=401, detail="bad api key")

    tok = req.token.strip()
    rid = req.wallet_rid.strip()
    sig_b64 = req.sig_b64.strip()
    ip = get_ip(request)
    if not _rate_ok(f"wbind:{tok}:{ip}", RATE_WALLET_PER_TOKEN):
        raise HTTPException(status_code=429, detail="rate limit: wallet_bind")

    now = _now()
    with get_cursor() as (conn, cur):
        cur.execute("SELECT * FROM airdrop_users WHERE token=%s FOR UPDATE", (tok,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="token_not_found")

        exp = int(row.get("wallet_challenge_exp") or 0)
        ch = (row.get("wallet_challenge") or "").strip()
        if not ch or exp <= now:
            raise HTTPException(status_code=400, detail="wallet_challenge_expired")

        if not _wallet_verify_sig(rid, ch, sig_b64):
            raise HTTPException(status_code=400, detail="wallet_bad_signature")

        # enforce unique rid across users
        cur.execute("SELECT token FROM airdrop_users WHERE wallet_rid=%s AND token<>%s", (rid, tok))
        if cur.fetchone():
            raise HTTPException(status_code=409, detail="wallet_rid_already_bound")

        cur.execute(
            "UPDATE airdrop_users SET wallet_bound=TRUE, wallet_rid=%s, wallet_bound_at=%s, wallet_challenge=NULL, wallet_challenge_exp=0, updated_at=%s WHERE token=%s",
            (rid, now, now, tok),
        )
        conn.commit()

    return _status_for_token(tok)

# -------------------- Airdrop Canon Helpers --------------------

def ensure_airdrop_user(cur, token: str):
    cur.execute("SELECT token FROM airdrop_users WHERE token=%s", (token,))
    if cur.fetchone():
        return False

    now = _now()
    cur.execute(
        """
        INSERT INTO airdrop_users (
            token,
            wallet_bound,
            telegram_ok,
            twitter_follow,
            twitter_like,
            twitter_retweet,
            referrals,
            points,
            created_at,
            updated_at
        )
        VALUES (%s, FALSE, FALSE, FALSE, FALSE, FALSE, 0, 0, %s, %s)
        """,
        (token, now, now),
    )
    return True
```

---

## FILE: `/opt/logos/airdrop-api/db_migrate_airdrop_sqlite_to_postgres.py`

```py
#!/usr/bin/env python3
"""
One-shot миграция: SQLite airdrop.sqlite3 -> Postgres logos_airdrop.

    AIRDROP_DB_DSN="postgresql://logos_airdrop:pass@127.0.0.1:5432/logos_airdrop" \
    AIRDROP_SQLITE_PATH="/opt/logos/airdrop-api/airdrop.sqlite3" \
    python3 db_migrate_airdrop_sqlite_to_postgres.py
"""

import os
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Any, List

import psycopg2

REF_TARGET = int(os.getenv("AIRDROP_REF_TARGET", "5"))
SQLITE_PATH = os.getenv("AIRDROP_SQLITE_PATH", "/opt/logos/airdrop-api/airdrop.sqlite3")
PG_DSN = os.getenv(
    "AIRDROP_DB_DSN",
    "postgresql://logos_airdrop:change_me@127.0.0.1:5432/logos_airdrop",
)


def compute_points(
    wallet_bound: bool,
    telegram_ok: bool,
    twitter_follow: bool,
    twitter_like: bool,
    twitter_retweet: bool,
    referrals: int,
) -> int:
    base = 0
    if wallet_bound:
        base += 10
    if telegram_ok:
        base += 10
    if twitter_follow:
        base += 10
    if twitter_like:
        base += 10
    if twitter_retweet:
        base += 10

    refs_eff = max(0, min(referrals, REF_TARGET))
    return base + refs_eff * 10


def load_sqlite() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM airdrop_users")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def main() -> None:
    rows = load_sqlite()
    if not rows:
        print("No rows in SQLite airdrop_users, nothing to migrate.")
        return

    by_token: Dict[str, Dict[str, Any]] = {r["token"]: r for r in rows}
    children_by_parent: Dict[str, List[Dict[str, Any]]] = {}
    for r in rows:
        ref_token = r.get("ref_token")
        if ref_token:
            children_by_parent.setdefault(ref_token, []).append(r)

    for r in rows:
        token = r["token"]
        children = children_by_parent.get(token, [])
        completed_children = [
            c
            for c in children
            if c.get("wallet_bound")
            and c.get("telegram_ok")
            and c.get("twitter_follow")
            and c.get("twitter_like")
            and c.get("twitter_retweet")
        ]
        refs_eff = min(len(completed_children), REF_TARGET)
        r["referrals_eff"] = refs_eff
        r["points_eff"] = compute_points(
            bool(r.get("wallet_bound")),
            bool(r.get("telegram_ok")),
            bool(r.get("twitter_follow")),
            bool(r.get("twitter_like")),
            bool(r.get("twitter_retweet")),
            refs_eff,
        )

    pg = psycopg2.connect(PG_DSN)
    pg.autocommit = False
    cur = pg.cursor()

    for r in rows:
        created_at = r.get("created_at")
        updated_at = r.get("updated_at")
        if isinstance(created_at, (int, float)):
            created_at_dt = datetime.fromtimestamp(created_at, tz=timezone.utc)
        else:
            created_at_dt = datetime.now(tz=timezone.utc)
        if isinstance(updated_at, (int, float)):
            updated_at_dt = datetime.fromtimestamp(updated_at, tz=timezone.utc)
        else:
            updated_at_dt = created_at_dt

        cur.execute(
            """
            INSERT INTO airdrop_users (
                token,
                ref_token,
                wallet_bound,
                telegram_ok,
                twitter_follow,
                twitter_like,
                twitter_retweet,
                referrals,
                points,
                created_at,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (token) DO UPDATE
            SET ref_token = EXCLUDED.ref_token,
                wallet_bound = EXCLUDED.wallet_bound,
                telegram_ok = EXCLUDED.telegram_ok,
                twitter_follow = EXCLUDED.twitter_follow,
                twitter_like = EXCLUDED.twitter_like,
                twitter_retweet = EXCLUDED.twitter_retweet,
                referrals = EXCLUDED.referrals,
                points = EXCLUDED.points,
                created_at = LEAST(airdrop_users.created_at, EXCLUDED.created_at),
                updated_at = GREATEST(airdrop_users.updated_at, EXCLUDED.updated_at)
            """,
            (
                r["token"],
                r.get("ref_token"),
                bool(r.get("wallet_bound")),
                bool(r.get("telegram_ok")),
                bool(r.get("twitter_follow")),
                bool(r.get("twitter_like")),
                bool(r.get("twitter_retweet")),
                int(r.get("referrals_eff", 0)),
                int(r.get("points_eff", 0)),
                created_at_dt,
                updated_at_dt,
            ),
        )

    pg.commit()
    cur.close()
    pg.close()
    print(f"Migrated {len(rows)} users from SQLite to Postgres.")


if __name__ == "__main__":
    main()
```

---

## FILE: `/opt/logos/airdrop-api/x_bind.py`

```py
from __future__ import annotations

import os
import time
import json
import urllib.request
import urllib.parse
from typing import Any, Dict

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/airdrop", tags=["x-guard"])

DB_DSN = (os.getenv("AIRDROP_DB_DSN") or os.getenv("AIRDROP_PG_DSN") or "").strip()
if not DB_DSN:
    raise RuntimeError("AIRDROP_DB_DSN (or AIRDROP_PG_DSN) is required")

POOL = ConnectionPool(
    conninfo=DB_DSN,
    min_size=1,
    max_size=int(os.getenv("AIRDROP_X_POOL_MAX", "10")),
    timeout=5,
    kwargs={"row_factory": dict_row},
)

X_GUARD_URL = (os.getenv("X_GUARD_URL", "http://127.0.0.1:8091").strip().rstrip("/"))
X_PROJECT_USERNAME = os.getenv("X_PROJECT_USERNAME", "RspLogos").strip().lstrip("@")
THROTTLE_SEC = int(os.getenv("X_VERIFY_THROTTLE_SEC", "30"))


def _now() -> int:
    return int(time.time())


def compute_points(wallet_bound: bool, telegram_ok: bool, twitter_follow: bool, twitter_like: bool, twitter_retweet: bool, referrals: int) -> int:
    flags = int(wallet_bound) + int(telegram_ok) + int(twitter_follow) + int(twitter_like) + int(twitter_retweet)
    return int(flags + int(referrals or 0))


def _norm_x_username(s: str) -> str:
    s = (s or "").strip()
    if s.startswith("@"):
        s = s[1:]

    s = s.replace("https://x.com/", "").replace("http://x.com/", "")
    s = s.replace("https://twitter.com/", "").replace("http://twitter.com/", "")
    s = s.split("?")[0].split("/")[0].strip().lower()

    if not s or len(s) > 32:
        raise ValueError("bad twitter_username")

    for ch in s:
        if not (ch.isalnum() or ch == "_"):
            raise ValueError("bad twitter_username")

    return s


def _rank_for(points: int, updated_at: int) -> int:
    with POOL.connection() as c:
        r = c.execute(
            """
            SELECT 1 + COUNT(*) AS rank
            FROM airdrop_users
            WHERE (points > %s) OR (points=%s AND updated_at > %s)
            """,
            (points, points, updated_at),
        ).fetchone()
    return int(r["rank"]) if r else 1


def status_for_token(tok: str) -> Dict[str, Any]:
    with POOL.connection() as c:
        row = c.execute(
            """
            SELECT token,wallet_bound,wallet_rid,telegram_ok,
                   twitter_follow,twitter_like,twitter_retweet,
                   referrals,points,updated_at,
                   twitter_username,twitter_checked_at
            FROM airdrop_users WHERE token=%s
            """,
            (tok,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="token not found")

    rank = _rank_for(int(row["points"]), int(row["updated_at"]))
    return {
        "ok": True,
        "token": tok,
        "wallet_bound": bool(row["wallet_bound"]),
        "wallet_rid": row.get("wallet_rid"),
        "telegram_ok": bool(row["telegram_ok"]),
        "twitter_follow": bool(row["twitter_follow"]),
        "twitter_like": bool(row["twitter_like"]),
        "twitter_retweet": bool(row["twitter_retweet"]),
        "twitter_username": row.get("twitter_username"),
        "twitter_checked_at": int(row.get("twitter_checked_at") or 0),
        "referrals": int(row["referrals"]),
        "points": int(row["points"]),
        "rank": int(rank),
    }


def x_guard_check(user_username: str) -> Dict[str, Any]:
    payload = {
        "user_username": user_username,
        "project_username": X_PROJECT_USERNAME,
        "tweet_id": "any",
        "mode": "any",
        "require_follow": True,
        "require_like": True,
        "require_retweet": True,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{X_GUARD_URL}/check_airdrop",
        data=data,
        headers={"content-type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", "replace")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"x_guard_unreachable: {e}")

    try:
        return json.loads(body)
    except Exception:
        raise HTTPException(status_code=502, detail=f"x_guard_bad_json: {body[:200]}")


class SetXUsernameRequest(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)
    twitter_username: str = Field(..., min_length=1, max_length=128)


@router.post("/set_x_username")
def set_x_username(req: SetXUsernameRequest):
    tok = req.token.strip()
    try:
        uname = _norm_x_username(req.twitter_username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    now = _now()
    try:
        with POOL.connection() as c:
            cur = c.execute(
                """
                UPDATE airdrop_users
                   SET twitter_username=%s,
                       updated_at=%s
                 WHERE token=%s
                """,
                (uname, now, tok),
            )
            if cur.rowcount != 1:
                raise HTTPException(status_code=404, detail="token not found")
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="twitter_username already bound")

    return status_for_token(tok)


class VerifyXRequest(BaseModel):
    token: str = Field(..., min_length=8, max_length=128)


@router.post("/verify_x")
def verify_x(req: VerifyXRequest):
    tok = req.token.strip()
    now = _now()

    with POOL.connection() as c:
        row = c.execute(
            """
            SELECT token,twitter_username,twitter_checked_at,
                   wallet_bound,telegram_ok,
                   twitter_follow,twitter_like,twitter_retweet,
                   referrals,updated_at
            FROM airdrop_users WHERE token=%s
            """,
            (tok,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="token not found")

    uname = (row.get("twitter_username") or "").strip()
    if not uname:
        raise HTTPException(status_code=400, detail="x_username_required")

    last = int(row.get("twitter_checked_at") or 0)
    if now - last < THROTTLE_SEC:
        return status_for_token(tok)

    res = x_guard_check(uname)

    follow_ok = bool(res.get("follow_ok"))
    like_ok = bool(res.get("like_ok"))
    retweet_ok = bool(res.get("retweet_ok"))

    # sticky: навсегда true если было true хотя бы раз
    new_follow = bool(row.get("twitter_follow")) or follow_ok
    new_like = bool(row.get("twitter_like")) or like_ok
    new_rt = bool(row.get("twitter_retweet")) or retweet_ok

    new_points = compute_points(
        bool(row.get("wallet_bound")),
        bool(row.get("telegram_ok")),
        new_follow, new_like, new_rt,
        int(row.get("referrals") or 0),
    )

    with POOL.connection() as c:
        c.execute(
            """
            UPDATE airdrop_users
               SET twitter_follow=%s,
                   twitter_like=%s,
                   twitter_retweet=%s,
                   twitter_checked_at=%s,
                   points=%s,
                   updated_at=%s
             WHERE token=%s
            """,
            (new_follow, new_like, new_rt, now, new_points, now, tok),
        )

    st = status_for_token(tok)
    st["details"] = {"x_guard": res}
    return st
```

---

## FILE: `/opt/logos/airdrop-api/x_oauth.py`

```py
from __future__ import annotations
import base64, hashlib, json, os, secrets
from typing import Any, Dict, Tuple
from urllib.parse import urlencode
import urllib.request, urllib.error
from cryptography.fernet import Fernet

# IMPORTANT:
# - authorize endpoint is WEB: https://x.com/i/oauth2/authorize
# - token endpoint is API: https://api.x.com/2/oauth2/token

AUTH_BASE = "https://x.com"
TOKEN_BASE = "https://api.x.com"

def _b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

def pkce_pair() -> Tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge

def fernet() -> Fernet:
    key = (os.getenv("AIRDROP_X_TOKEN_KEY") or "").strip()
    if not key:
        raise RuntimeError("AIRDROP_X_TOKEN_KEY is required")
    return Fernet(key.encode())

def enc(s: str) -> str:
    return fernet().encrypt(s.encode()).decode()

def dec(s: str) -> str:
    return fernet().decrypt(s.encode()).decode()

def oauth_authorize_url(state: str, code_challenge: str) -> str:
    cid = (os.getenv("X_OAUTH_CLIENT_ID") or "").strip()
    redir = (os.getenv("X_OAUTH_REDIRECT_URI") or "").strip()
    scopes = (os.getenv("X_OAUTH_SCOPES") or "tweet.read users.read").strip()
    if not cid or not redir:
        raise RuntimeError("X_OAUTH_CLIENT_ID and X_OAUTH_REDIRECT_URI required")
    q = {
        "response_type": "code",
        "client_id": cid,
        "redirect_uri": redir,
        "scope": scopes,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTH_BASE}/i/oauth2/authorize?{urlencode(q)}"

def _basic_auth() -> str | None:
    cid = (os.getenv("X_OAUTH_CLIENT_ID") or "").strip()
    sec = (os.getenv("X_OAUTH_CLIENT_SECRET") or "").strip()
    if cid and sec:
        return base64.b64encode(f"{cid}:{sec}".encode()).decode()
    return None

def token_exchange(code: str, code_verifier: str) -> Dict[str, Any]:
    cid = (os.getenv("X_OAUTH_CLIENT_ID") or "").strip()
    redir = (os.getenv("X_OAUTH_REDIRECT_URI") or "").strip()
    if not cid or not redir:
        raise RuntimeError("X_OAUTH_CLIENT_ID and X_OAUTH_REDIRECT_URI required")
    data = urlencode({
        "grant_type": "authorization_code",
        "client_id": cid,
        "code": code,
        "redirect_uri": redir,
        "code_verifier": code_verifier,
    }).encode()
    req = urllib.request.Request(f"{TOKEN_BASE}/2/oauth2/token", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    b = _basic_auth()
    if b:
        req.add_header("Authorization", f"Basic {b}")
    with urllib.request.urlopen(req, timeout=25) as resp:
        body = resp.read().decode("utf-8", "replace")
    return json.loads(body)

def token_refresh(refresh_token: str) -> Dict[str, Any]:
    cid = (os.getenv("X_OAUTH_CLIENT_ID") or "").strip()
    if not cid:
        raise RuntimeError("X_OAUTH_CLIENT_ID required")
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": cid,
    }).encode()
    req = urllib.request.Request(f"{TOKEN_BASE}/2/oauth2/token", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    b = _basic_auth()
    if b:
        req.add_header("Authorization", f"Basic {b}")
    with urllib.request.urlopen(req, timeout=25) as resp:
        body = resp.read().decode("utf-8", "replace")
    return json.loads(body)

def x_get(path: str, access_token: str, timeout: float = 15) -> Dict[str, Any]:
    req = urllib.request.Request(f"{TOKEN_BASE}{path}", method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
        return json.loads(body)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = ""
        return {"_http_error": int(e.code), "_body": body[:500]}

```
