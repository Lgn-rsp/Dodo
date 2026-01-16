# BOOK_234 — wallet-proxy: address-book + storage + scanner

- Generated: 2026-01-16T08:25:54Z
- Scope: /opt/logos/wallet-proxy


# 1) Address-book (RID → addresses)


## app.py (receive + derivation + balances)

**Path:** `/opt/logos/wallet-proxy/app.py`

```
import os, json, time, asyncio


from decimal import Decimal, ROUND_DOWN

TOKEN_DECIMALS = {
    "USDT": 6,
}

def to_base_units(amount_str: str, token: str) -> int:
    d = TOKEN_DECIMALS.get(token.upper(), 18)
    a = Decimal(str(amount_str))
    q = (a * (Decimal(10) ** d)).quantize(Decimal("1"), rounding=ROUND_DOWN)
    return int(q)
# ====== DB session fallback (SessionLocal) ======
# Ensures SessionLocal exists even if earlier patches removed DB setup.
try:
    SessionLocal  # noqa
except NameError:
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
    except Exception as e:
        raise RuntimeError(f"SQLAlchemy missing or broken: {e}")

    _engine = globals().get("engine") or globals().get("ENGINE")
    if _engine is None:
        DB_URL = (
            os.environ.get("WALLET_PROXY_DB_URL")
            or os.environ.get("DATABASE_URL")
            or "sqlite:////opt/logos/wallet-proxy/wallet_proxy.db"
        )
        if DB_URL.startswith("sqlite"):
            _engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(DB_URL)
        globals()["engine"] = _engine

    SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)
    globals()["SessionLocal"] = SessionLocal
# ====== /DB session fallback ======
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from web3 import Web3
from sqlalchemy import Column, Integer, String, BigInteger, create_engine, select, Index
from sqlalchemy.orm import declarative_base, Session
import aiohttp
from bip_utils import Bip84, Bip84Coins, Bip44, Bip44Coins, Bip44Changes
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST


# ====== env fallback loader (so systemd/envfile issues won't break XPUB) ======
def _load_env_file(path="/etc/logos/wallet-proxy.env"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                # do not override existing env
                if k and k not in os.environ:
                    os.environ[k] = v
    except FileNotFoundError:
        pass
    except Exception as e:
        print("WARN: failed to load env file:", e)

_load_env_file()

# ====== ENV ======
NODE_URL     = os.environ.get("LRB_NODE_URL", "http://127.0.0.1:8080")
BRIDGE_KEY   = os.environ.get("LRB_BRIDGE_KEY", "")
CORS         = [o.strip() for o in os.environ.get("LRB_WALLET_CORS", "*").split(",") if o.strip()]
ETH_RPC      = os.environ.get("ETH_PROVIDER_URL", "")
USDT_ADDRESS = os.environ.get("USDT_ERC20_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
HOT_PK       = os.environ.get("ETH_HOT_WALLET_PK", "")
BTC_XPUB     = os.environ.get("BTC_XPUB", "")
ETH_XPUB     = os.environ.get("ETH_XPUB", "")
TRON_XPUB    = os.environ.get("TRON_XPUB", "")
DB_URL       = "sqlite:////opt/logos/wallet-proxy/wproxy.db"

# ====== DB ======
Base = declarative_base()

class DepositMap(Base):
    __tablename__ = "deposit_map"
    id         = Column(Integer, primary_key=True)
    rid        = Column(String, index=True, nullable=False)
    token      = Column(String, nullable=False)
    network    = Column(String, nullable=False)
    index      = Column(Integer, nullable=False, default=0)
    address    = Column(String, unique=True, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()))

Index("ix_dep_unique", DepositMap.rid, DepositMap.token, DepositMap.network, unique=True)

class SeenTx(Base):
    __tablename__ = "seen_tx"
    id      = Column(Integer, primary_key=True)
    txid    = Column(String, unique=True, nullable=False)
    rid     = Column(String, index=True)
    token   = Column(String)
    network = Column(String)

engine = create_engine(DB_URL, future=True)
Base.metadata.create_all(engine)

# ====== Web3 ======
w3: Optional[Web3] = None
USDT = None
ERC20_ABI = json.loads("""
[
 {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},
 {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"},
 {"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}
]
""")
if ETH_RPC:
    try:
        w3 = Web3(Web3.HTTPProvider(ETH_RPC, request_kwargs={"timeout": 10}))
        if w3.is_connected():
            USDT = w3.eth.contract(
                address=Web3.to_checksum_address(USDT_ADDRESS),
                abi=ERC20_ABI,
            )
            print("INFO Web3 connected:", USDT_ADDRESS)
        else:
            print("WARN ETH RPC not reachable")
            w3 = None
    except Exception as e:
        print("WARN web3 init error:", e)
        w3 = None
        USDT = None

# ====== HTTP helper ======
async def http_json(method: str, url: str, body: dict = None, headers: dict = None):
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method, url, json=body, headers=headers) as r:
            t = await r.text()
            try:
                data = json.loads(t) if t else {}
            except Exception:
                data = {"raw": t}
            return r.status, data

# ====== FastAPI ======
app = FastAPI(title="LRB Wallet Proxy", version="1.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS if CORS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== Pydantic v2-safe models ======
class TopupRequest(BaseModel):
    rid: str
    token: Literal["USDT"] = "USDT"
    network: Literal["ETH"] = "ETH"

class TopupResponse(BaseModel):
    rid: str
    token: str
    network: str
    address: str

class WithdrawRequest(BaseModel):
    rid: str
    token: Literal["USDT"] = "USDT"
    network: Literal["ETH"] = "ETH"
    amount: int
    to_address: str
    request_id: str

class QuoteRequest(BaseModel):
    from_token: str
    to_token: str
    amount: int

class QuoteResponse(BaseModel):
    price: float
    expected_out: float

# ====== Metrics ======
PROXY_TOPUP_REQ    = Counter("proxy_topup_requests_total", "topup requests")
PROXY_WITHDRAW_OK  = Counter("proxy_withdraw_ok_total",   "withdraw ok")
PROXY_WITHDRAW_ERR = Counter("proxy_withdraw_err_total",  "withdraw err")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)



# ====== Address derivation (watch-only) ======

# ====== Address derivation (watch-only) ======
# NOTE: address must be globally unique in deposit_map.address
# so we allocate a unique index per chain and retry on collisions.

from sqlalchemy.exc import IntegrityError
from bip_utils import Bip84, Bip84Coins, Bip44, Bip44Coins, Bip44Changes

def _require_env(name: str) -> str:
    v = (os.environ.get(name, "") or "").strip()
    if not v:
        raise HTTPException(status_code=500, detail=f"{name} not configured")
    return v

def _derive_address(chain: str, index: int) -> str:
    chain = chain.upper()
    if chain == "BTC":
        key = _require_env("BTC_XPUB")  # actually zpub ok
        acc = Bip84.FromExtendedKey(key, Bip84Coins.BITCOIN)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    if chain == "ETH":
        key = _require_env("ETH_XPUB")
        acc = Bip44.FromExtendedKey(key, Bip44Coins.ETHEREUM)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    if chain == "TRON":
        key = _require_env("TRON_XPUB")
        acc = Bip44.FromExtendedKey(key, Bip44Coins.TRON)
        return acc.Change(Bip44Changes.CHAIN_EXT).AddressIndex(index).PublicKey().ToAddress()
    raise HTTPException(status_code=400, detail=f"unsupported chain: {chain}")

def _chain_from(token: str, network: str) -> str:
    # нормализуем в "цепь", чтобы USDT на ETH использовал тот же пул адресов ETH
    n = (network or "").upper()
    if n in ("ETH", "ETHEREUM", "ERC20"):
        return "ETH"
    if n in ("TRON", "TRC20"):
        return "TRON"
    if n in ("BTC", "BITCOIN"):
        return "BTC"
    return n

def _next_index(sess, chain: str) -> int:
    # глобальный next index по цепи (не по RID!)
    q = sess.query(DepositMap).filter(DepositMap.network == chain).order_by(DepositMap.index.desc()).first()
    if not q:
        return 0
    try:
        return int(q.index) + 1
    except Exception:
        return 0

def _get_or_create_addr(rid: str, token: str, network: str) -> str:
    chain = _chain_from(token, network)

    # 1) если уже есть адрес для rid+chain — вернём
    with SessionLocal() as sess:
        row = sess.query(DepositMap).filter(
            DepositMap.rid == rid,
            DepositMap.network == chain
        ).first()
        if row:
            return row.address

        # 2) выделяем уникальный индекс по chain
        for _ in range(0, 2048):
            idx = _next_index(sess, chain) + _
            addr = _derive_address(chain, idx)

            obj = DepositMap(
                rid=rid,
                token=token,
                network=chain,
                index=idx,
                address=addr,
                created_at=int(time.time()),
            )

            sess.add(obj)

            # --- race-safe commit ---
            try:
                sess.commit()
                return addr
            except IntegrityError:
                sess.rollback()

                # 1) если параллельный запрос уже создал маппинг для этого кошелька — просто вернём его
                row2 = sess.query(DepositMap).filter(
                    DepositMap.rid == rid,
                    DepositMap.token == token,
                    DepositMap.network == chain
                ).first()
                if row2:
                    return row2.address

                # 2) иначе это коллизия по address/index (или другой UNIQUE) — пробуем следующий idx
                continue

        raise HTTPException(status_code=500, detail="unable to allocate unique address")
# ====== Endpoints ======

# --- receive addresses (watch-only) ---
@app.get("/v1/receive/{rid}")
def receive_addresses(rid: str):
    rid = (rid or "").strip()
    if not rid:
        raise HTTPException(status_code=400, detail="rid is required")

    # BTC / ETH / TRON: один адрес на цепь.
    # USDT на ETH/TRON использует тот же адрес соответствующей цепи.
    addrs = {
        "BTC": _get_or_create_addr(rid, "BTC", "BTC"),
        "ETH": _get_or_create_addr(rid, "ETH", "ETH"),
        "TRON": _get_or_create_addr(rid, "TRON", "TRON"),
        "USDT_ERC20": _get_or_create_addr(rid, "USDT", "ETH"),
        "USDT_TRC20": _get_or_create_addr(rid, "USDT", "TRON"),
    }
    return {"rid": rid, "lgn_rid": rid, "addresses": addrs}



# --- balances (live) ---
from decimal import Decimal
import time

_USDT_ETH = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT ERC20 mainnet
_USDT_TRON = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"         # USDT TRC20 (Tether)

_ERC20_ABI_MIN = [
    {"name":"balanceOf","type":"function","stateMutability":"view",
     "inputs":[{"name":"account","type":"address"}],
     "outputs":[{"name":"","type":"uint256"}]},
    {"name":"decimals","type":"function","stateMutability":"view",
     "inputs":[], "outputs":[{"name":"","type":"uint8"}]},
]

def _d(x, q=18):
    try:
        return str((Decimal(x) / (Decimal(10) ** Decimal(q))).normalize())
    except Exception:
        return None

def _http_get_json(url: str, params=None, timeout=12):
    # requests может не быть -> fallback на urllib
    try:
        import requests
        r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent":"logos-wallet-proxy/1.0"})
        r.raise_for_status()
        return r.json()
    except Exception:
        import json, urllib.request, urllib.parse
        if params:
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent":"logos-wallet-proxy/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "ignore"))

def _btc_balance_blockstream(addr: str):
    # confirmed + mempool balances in sats
    j = _http_get_json(f"https://blockstream.info/api/address/{addr}")
    cs = j.get("chain_stats") or {}
    ms = j.get("mempool_stats") or {}
    confirmed = int(cs.get("funded_txo_sum", 0)) - int(cs.get("spent_txo_sum", 0))
    mempool = int(ms.get("funded_txo_sum", 0)) - int(ms.get("spent_txo_sum", 0))
    total = confirmed + mempool
    return {
        "confirmed_sat": confirmed,
        "mempool_sat": mempool,
        "total_sat": total,
        "total_btc": _d(total, 8),
        "source": "blockstream.info"
    }

def _eth_balances_web3(addr: str):
    # web3 instance
    try:
        w3 = globals().get("w3") or globals().get("W3")
        if w3 is None:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(_require_env("ETH_PROVIDER_URL"), request_kwargs={"timeout": 12}))
            globals()["w3"] = w3
        if not w3.is_connected():
            return {"error": "ETH provider not connected"}

        wei = int(w3.eth.get_balance(addr))
        out = {"wei": wei, "eth": _d(wei, 18), "source": "web3"}

        # USDT ERC20
        c = w3.eth.contract(address=w3.to_checksum_address(_USDT_ETH), abi=_ERC20_ABI_MIN)
        try:
            dec = int(c.functions.decimals().call())
        except Exception:
            dec = 6
        raw = int(c.functions.balanceOf(w3.to_checksum_address(addr)).call())
        out["usdt_erc20"] = {"raw": raw, "usdt": _d(raw, dec), "decimals": dec, "contract": _USDT_ETH}
        return out
    except Exception as e:
        return {"error": f"eth_web3_failed: {e}"}

def _tron_balances(addr: str):
    # 1) try tronpy (if installed)
    try:
        from tronpy import Tron
        client = Tron()
        trx = client.get_account_balance(addr)  # float TRX
        # TRC20 USDT
        usdt = client.get_contract(_USDT_TRON).functions.balanceOf(addr)
        usdt_raw = int(usdt)
        return {
            "trx": str(trx),
            "sun": int(Decimal(trx) * Decimal(1_000_000)),
            "usdt_trc20": {"raw": usdt_raw, "usdt": _d(usdt_raw, 6), "decimals": 6, "contract": _USDT_TRON},
            "source": "tronpy"
        }
    except Exception:
        pass

    # 2) fallback: tronscan public api
    try:
        j = _http_get_json("https://apilist.tronscanapi.com/api/account", params={"address": addr})
        # TRX
        bal_sun = int(j.get("balance", 0))
        out = {
            "sun": bal_sun,
            "trx": _d(bal_sun, 6),
            "source": "tronscan"
        }
        # USDT TRC20 from token balances
        tb = j.get("trc20token_balances") or j.get("trc20TokenBalances") or []
        usdt_raw = None
        for it in tb:
            ca = (it.get("contract_address") or it.get("contractAddress") or "").strip()
            if ca == _USDT_TRON:
                usdt_raw = it.get("balance") or it.get("tokenBalance") or it.get("quantity")
                break
        if usdt_raw is not None:
            try:
                usdt_raw = int(str(usdt_raw))
            except Exception:
                usdt_raw = None
        out["usdt_trc20"] = {"raw": usdt_raw, "usdt": _d(usdt_raw or 0, 6), "decimals": 6, "contract": _USDT_TRON}
        return out
    except Exception as e:
        return {"error": f"tron_failed: {e}"}

@app.get("/v1/balances/{rid}")
def balances(rid: str):
    rid = (rid or "").strip()
    if not rid:
        raise HTTPException(status_code=400, detail="rid is required")

    # addresses (ensure mapping exists)
    addrs = {
        "BTC": _get_or_create_addr(rid, "BTC", "BTC"),
        "ETH": _get_or_create_addr(rid, "ETH", "ETH"),
        "TRON": _get_or_create_addr(rid, "TRON", "TRON"),
        "USDT_ERC20": _get_or_create_addr(rid, "USDT", "ETH"),
        "USDT_TRC20": _get_or_create_addr(rid, "USDT", "TRON"),
    }

    t0 = time.time()
    out = {
        "rid": rid,
        "addresses": addrs,
        "balances": {},
        "ts": int(time.time())
    }

    # BTC
    try:
        out["balances"]["BTC"] = _btc_balance_blockstream(addrs["BTC"])
    except Exception as e:
        out["balances"]["BTC"] = {"error": f"btc_failed: {e}"}

    # ETH + USDT_ERC20
    out["balances"]["ETH"] = _eth_balances_web3(addrs["ETH"])

    # TRON + USDT_TRC20
    out["balances"]["TRON"] = _tron_balances(addrs["TRON"])

    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out
@app.get("/")
def root():
    return {"ok": True, "service": "wallet-proxy", "eth_connected": bool(w3)}

@app.post("/v1/topup/request", response_model=TopupResponse)
def topup_request(req: TopupRequest):
    PROXY_TOPUP_REQ.inc()
    if not w3:
        raise HTTPException(503, "ETH RPC not connected")
    if not HOT_PK:
        raise HTTPException(500, "HOT wallet not configured")

    deposit_address = w3.eth.account.from_key(HOT_PK).address

    with Session(engine) as s:
        dm = s.execute(
            select(DepositMap).where(
                DepositMap.rid == req.rid,
                DepositMap.token == req.token,
                DepositMap.network == req.network,
            )
        ).scalar_one_or_none()
        if dm is None:
            s.add(
                DepositMap(
                    rid=req.rid,
                    token=req.token,
                    network=req.network,
                    address=deposit_address,
                )
            )
            s.commit()

    return TopupResponse(
        rid=req.rid,
        token=req.token,
        network=req.network,
        address=deposit_address,
    )

@app.post("/v1/withdraw")
async def withdraw(req: WithdrawRequest):
    try:
        if req.amount <= 0:
            raise HTTPException(400, "amount<=0")
        if not w3 or not USDT:
            raise HTTPException(503, "ETH RPC not connected")

        acct = w3.eth.account.from_key(HOT_PK)

        # redeem из LRB-ноды
        hdr = (
            {"X-Bridge-Key": BRIDGE_KEY}
            if not BRIDGE_KEY.startswith("ey")
            else {"Authorization": f"Bearer {BRIDGE_KEY}"}
        )
        st, data = await http_json(
            "POST",
            f"{NODE_URL}/bridge/redeem",
            {
                "rid": req.rid,
                "amount": req.amount,
                "request_id": req.request_id,
            },
            hdr,
        )
        if st // 100 != 2:
            raise HTTPException(st, f"bridge redeem failed: {data}")

        # ERC-20 перевод USDT
        nonce = w3.eth.get_transaction_count(acct.address)
        tx = USDT.functions.transfer(
            Web3.to_checksum_address(req.to_address),
            to_base_units(req.amount, (getattr(req,"token",None) or "USDT")),
        ).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "from": acct.address,
                "nonce": nonce,
                "gas": 90000,
                "maxFeePerGas": w3.to_wei("30", "gwei"),
                "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
            }
        )
        signed = w3.eth.account.sign_transaction(tx, private_key=HOT_PK)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction).hex()

        with Session(engine) as s:
            s.add(
                SeenTx(
                    txid=tx_hash,
                    rid=req.rid,
                    token=req.token,
                    network=req.network,
                )
            )
            s.commit()

        PROXY_WITHDRAW_OK.inc()
        return {"ok": True, "txid": tx_hash}
    except HTTPException:
        PROXY_WITHDRAW_ERR.inc()
        raise
    except Exception as e:
        PROXY_WITHDRAW_ERR.inc()
        raise HTTPException(500, f"withdraw error: {e}")

@app.post("/v1/quote", response_model=QuoteResponse)
async def quote(req: QuoteRequest):
    return QuoteResponse(price=1.0, expected_out=float(req.amount))
```

# 2) Storage (SQLite)


## init_db.py

**Path:** `/opt/logos/wallet-proxy/init_db.py`

```
import os, sqlite3, sys

def db_path_from_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return "/opt/logos/wallet-proxy/wallet_proxy.db"
    if url.startswith("sqlite:////"):
        return url[len("sqlite:////")-1:]  # keep leading /
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///"):]
    if url.startswith("sqlite://"):
        # rare, but handle
        return url.replace("sqlite://", "", 1)
    # not sqlite -> do nothing here
    return ""

DB_URL = os.environ.get("WALLET_PROXY_DB_URL") or os.environ.get("DATABASE_URL") or "sqlite:////opt/logos/wallet-proxy/wallet_proxy.db"
path = db_path_from_url(DB_URL)

if not path:
    print("INFO: non-sqlite DB configured, skip init_db")
    sys.exit(0)

os.makedirs(os.path.dirname(path), exist_ok=True)

con = sqlite3.connect(path)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS deposit_map (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rid TEXT NOT NULL,
  token TEXT NOT NULL,
  network TEXT NOT NULL,
  "index" INTEGER NOT NULL DEFAULT 0,
  address TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
""")

# глобальная уникальность адреса (у тебя это уже требуется по логике)
cur.execute("""CREATE UNIQUE INDEX IF NOT EXISTS ux_deposit_map_address ON deposit_map(address);""")

# чтобы быстро находить по (rid, network) — под ваш SELECT
cur.execute("""CREATE INDEX IF NOT EXISTS ix_deposit_map_rid_network ON deposit_map(rid, network);""")

con.commit()
con.close()

print("OK: init_db done ->", path)
```

## DB tables + counts

```bash
cd /opt/logos/wallet-proxy || exit 1; for db in wproxy.db wallet_proxy.db; do echo "=== $db ==="; sqlite3 "$db" ".tables"; sqlite3 "$db" "select count(*) from deposit_map;" || true; sqlite3 "$db" "select count(*) from seen_tx;" || true; done
```

```
=== wproxy.db ===
deposit_map  seen_tx    
3
0
=== wallet_proxy.db ===
deposit_map
60
Error: in prepare, no such table: seen_tx
```

## DB schema (wproxy.db)

```bash
cd /opt/logos/wallet-proxy || exit 1; sqlite3 wproxy.db ".schema"
```

```
CREATE TABLE deposit_map (
	id INTEGER NOT NULL, 
	rid VARCHAR NOT NULL, 
	token VARCHAR NOT NULL, 
	network VARCHAR NOT NULL, 
	"index" INTEGER NOT NULL, 
	address VARCHAR NOT NULL, 
	created_at BIGINT, 
	PRIMARY KEY (id), 
	UNIQUE (address)
);
CREATE UNIQUE INDEX ix_dep_unique ON deposit_map (rid, token, network);
CREATE INDEX ix_deposit_map_rid ON deposit_map (rid);
CREATE TABLE seen_tx (
	id INTEGER NOT NULL, 
	txid VARCHAR NOT NULL, 
	rid VARCHAR, 
	token VARCHAR, 
	network VARCHAR, 
	PRIMARY KEY (id), 
	UNIQUE (txid)
);
CREATE INDEX ix_seen_tx_rid ON seen_tx (rid);
```

# 3) Scanner


## scanner.py (scan deposits + SeenTx + bridge notify)

**Path:** `/opt/logos/wallet-proxy/scanner.py`

```
import os, json, time, asyncio
from typing import Optional
from web3 import Web3
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from prometheus_client import Counter, Gauge, start_http_server
import aiohttp

DB_URL       = "sqlite:////opt/logos/wallet-proxy/wproxy.db"
NODE_URL     = os.environ.get("LRB_NODE_URL", "http://127.0.0.1:8080")
BRIDGE_KEY   = os.environ.get("LRB_BRIDGE_KEY", "")
ETH_RPC      = os.environ.get("ETH_PROVIDER_URL", "")
USDT_ADDRESS = os.environ.get("USDT_ERC20_ADDRESS", "0xdAC17F958D2ee523a2206206994597C13D831ec7")
CONFIRMATIONS= int(os.environ.get("ETH_CONFIRMATIONS", "6"))

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger

Base = declarative_base()
class DepositMap(Base):
    __tablename__ = "deposit_map"
    id = Column(Integer, primary_key=True); rid = Column(String); token = Column(String); network = Column(String); address = Column(String)
class SeenTx(Base):
    __tablename__ = "seen_tx"
    id = Column(Integer, primary_key=True); txid = Column(String, unique=True); rid = Column(String); token = Column(String); network = Column(String)
class Kv(Base):
    __tablename__ = "kv"
    k = Column(String, primary_key=True); v = Column(String, nullable=False)

engine = create_engine(DB_URL, future=True)

# metrics
SCAN_LAST_BLOCK = Gauge("scanner_last_scanned_block", "last scanned block")
SCAN_LAG        = Gauge("scanner_block_lag", "chain head minus safe block")
DEP_OK          = Counter("scanner_deposit_ok_total", "successful deposits")
DEP_ERR         = Counter("scanner_deposit_err_total","failed deposits")

async def http_json(method:str, url:str, body:dict=None, headers:dict=None):
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method, url, json=body, headers=headers) as r:
            t = await r.text()
            try: data = json.loads(t) if t else {}
            except: data = {"raw": t}
            return r.status, data

def kv_get(key:str, default:str="0")->str:
    with Session(engine) as s:
        row = s.get(Kv, key); return row.v if row else default
def kv_set(key:str, val:str):
    with Session(engine) as s:
        row = s.get(Kv, key)
        if row: row.v = val
        else:   s.add(Kv(k=key, v=val))
        s.commit()

async def scanner():
    if not ETH_RPC:
        print("No ETH RPC configured; scanner idle"); 
        while True: await asyncio.sleep(30)

    w3 = Web3(Web3.HTTPProvider(ETH_RPC, request_kwargs={"timeout":10}))
    if not w3.is_connected():
        print("ETH RPC unreachable; scanner idle")
        while True: await asyncio.sleep(30)

    USDT = w3.eth.contract(address=Web3.to_checksum_address(USDT_ADDRESS), abi=json.loads("""
    [
     {"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}
    ]
    """))
    key = "last_scanned_block"
    backoff = 1
    while True:
        try:
            head = w3.eth.block_number
            safe_to = head - CONFIRMATIONS
            last = int(kv_get(key, "0"))
            SCAN_LAG.set(max(0, head - safe_to))
            if safe_to <= last:
                await asyncio.sleep(5); continue

            step = 2000
            from_block = last + 1
            with Session(engine) as s:
                addr_map = {dm.address.lower(): dm for dm in s.query(DepositMap).all()}

            while from_block <= safe_to:
                to_block = min(from_block + step - 1, safe_to)
                logs = w3.eth.get_logs({
                    "fromBlock": from_block, "toBlock": to_block,
                    "address": Web3.to_checksum_address(USDT_ADDRESS),
                    "topics": [Web3.keccak(text="Transfer(address,address,uint256)")]
                })
                for lg in logs:
                    to_hex = "0x"+lg["topics"][2].hex()[-40:]
                    to_norm = Web3.to_checksum_address(to_hex).lower()
                    dm = addr_map.get(to_norm)
                    if not dm: continue
                    txid = lg["transactionHash"].hex()
                    value = int(lg["data"], 16)
                    # идемпотентность
                    with Session(engine) as s:
                        if s.execute(select(SeenTx).where(SeenTx.txid==txid)).scalar_one_or_none():
                            continue
                        s.add(SeenTx(txid=txid, rid=dm.rid, token=dm.token, network=dm.network)); s.commit()
                    # bridge deposit
                    hdr = {"X-Bridge-Key": os.environ.get("LRB_BRIDGE_KEY","")}
                    st, data = await http_json("POST", f"{NODE_URL}/bridge/deposit",
                                               {"rid": dm.rid, "amount": value, "ext_txid": txid}, hdr)
                    if st//100 == 2: DEP_OK.inc()
                    else:
                        DEP_ERR.inc()
                        print("WARN deposit fail", txid, st, data)
                kv_set(key, str(to_block))
                SCAN_LAST_BLOCK.set(to_block)
                from_block = to_block + 1
                backoff = 1
            await asyncio.sleep(5)
        except Exception as e:
            print("scanner error:", e)
            await asyncio.sleep(min(60, backoff)); backoff = min(60, backoff*2)

if __name__ == "__main__":
    # метрики на 9101
    start_http_server(9101)
    asyncio.run(scanner())
```

---
END

