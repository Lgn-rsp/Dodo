# FULL SOURCE — `/opt/logos/airdrop-tg-bot`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/opt/logos/airdrop-tg-bot/bot.py`

```py
#!/usr/bin/env python3
import os
import time
import json
import logging
import urllib.request
import urllib.parse

log = logging.getLogger("logos-airdrop-tg-bot")
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def env_any(*names: str, default: str = "") -> str:
    for n in names:
        v = os.getenv(n)
        if v and v.strip():
            return v.strip()
    return default

BOT_TOKEN = env_any("LOGOS_TG_BOT_TOKEN", "TG_BOT_TOKEN", "TELEGRAM_BOT_TOKEN", "BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("Missing bot token env. Expected one of: LOGOS_TG_BOT_TOKEN / TG_BOT_TOKEN / TELEGRAM_BOT_TOKEN / BOT_TOKEN")

TG_CHANNEL = env_any("TG_CHANNEL", "TELEGRAM_CHANNEL", default="@logosblockchain")
AIRDROP_API_KEY = env_any("AIRDROP_API_KEY", default="")
AIRDROP_UPDATE_URL = env_any("AIRDROP_UPDATE_URL", default="http://127.0.0.1:8092/api/airdrop/update")
AIRDROP_KEY_HEADER = env_any("AIRDROP_API_KEY_HEADER", default="X-API-Key")

TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def http_json(url: str, payload: dict | None = None, headers: dict | None = None, timeout: int = 60) -> dict:
    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw) if raw else {}

def tg_call(method: str, payload: dict, timeout: int = 60) -> dict:
    return http_json(f"{TG_API}/{method}", payload=payload, timeout=timeout)

def send_message(chat_id: int, text: str) -> None:
    try:
        tg_call("sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}, timeout=30)
    except Exception as e:
        log.warning("sendMessage failed: %s", e)

def extract_token(text: str) -> str:
    text = (text or "").strip()
    if not text.startswith("/start"):
        return ""
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return ""
    param = parts[1].strip()
    if param.startswith("airdrop_"):
        param = param[len("airdrop_"):].strip()
    return param

def is_member(user_id: int) -> bool:
    try:
        r = tg_call("getChatMember", {"chat_id": TG_CHANNEL, "user_id": user_id}, timeout=30)
        if not r.get("ok"):
            return False
        st = (r.get("result") or {}).get("status") or ""
        # creator/administrator/member/restricted считаем "в канале"
        return st in ("creator", "administrator", "member", "restricted")
    except Exception as e:
        log.warning("getChatMember error: %s", e)
        return False

def airdrop_update(token: str) -> bool:
    if not AIRDROP_API_KEY:
        log.error("AIRDROP_API_KEY missing in env; cannot update airdrop")
        return False
    try:
        headers = {AIRDROP_KEY_HEADER: AIRDROP_API_KEY}
        payload = {"token": token, "telegram_ok": True}
        r = http_json(AIRDROP_UPDATE_URL, payload=payload, headers=headers, timeout=20)
        return bool(r)  # не жёстко проверяем формат, главное чтобы 200 и JSON пришёл
    except Exception as e:
        log.error("airdrop_update error: %s", e)
        return False

def main() -> None:
    log.info("Starting TG bot. channel=%s update_url=%s", TG_CHANNEL, AIRDROP_UPDATE_URL)

    offset = 0
    while True:
        try:
            # long-polling
            url = f"{TG_API}/getUpdates?timeout=50&offset={offset}"
            r = http_json(url, payload=None, timeout=70)
            if not r.get("ok"):
                time.sleep(2)
                continue

            for upd in r.get("result", []):
                offset = max(offset, int(upd.get("update_id", 0)) + 1)

                msg = upd.get("message") or upd.get("edited_message")
                if not msg:
                    continue

                chat_id = (msg.get("chat") or {}).get("id")
                frm = msg.get("from") or {}
                user_id = frm.get("id")
                text = msg.get("text") or ""

                if not chat_id or not user_id:
                    continue

                token = extract_token(text)
                if not token:
                    continue

                if not is_member(int(user_id)):
                    send_message(int(chat_id), "Подпишись на канал @logosblockchain, потом снова нажми /start с токеном.")
                    continue

                ok = airdrop_update(token)
                if ok:
                    send_message(int(chat_id), "✅ Подписка подтверждена. Возвращайся на airdrop-страницу и жми Refresh.")
                    log.info("telegram_ok=true token=%s user_id=%s", token[:8] + "...", user_id)
                else:
                    send_message(int(chat_id), "⚠️ Не смог обновить статус в airdrop. Попробуй позже или напиши админу.")
        except Exception as e:
            log.error("loop error: %s", e)
            time.sleep(2)

if __name__ == "__main__":
    main()
```
