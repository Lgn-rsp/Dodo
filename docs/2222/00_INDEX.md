# BOOK 2222 — Node-API backend + logs around send failure + LGN send frontend

Generated: 2026-01-14 12:06:56Z
Window: since=10 minutes ago until=now

Includes:
- node-api: systemd + env/configs + detected sources for /node-api/balance and /node-api/submit_tx
- logs: journalctl node-api + nginx access/error filtered for submit_tx
- frontend: modules/lgn_send.js + app.js + auth.js (+ full modules dirs if present)

Secrets in env are REDACTED.
