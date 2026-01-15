# BOOK 1234 — wallet_prod + wallet-proxy + nginx routes (sanitized)

Generated: 2026-01-15T12:23:27Z

Secrets/tokens/keys were sanitized to `***`.

## What is inside
- wallet_prod (or active wallet_dev/wallet_premium/wallet) : app.html, app.js, modules/* (including lgn_send.js if exists)
- wallet-proxy : full source project (text/code files, no venv)
- nginx vhost(s) for mw-expedition.com (routes for /node-api and /wallet-api)
- systemd units (cat) related to wallet/node/proxy/scanner
- sanitized env files (wallet/proxy/node)
- logs (journalctl + nginx error/access tails)

### Front root chosen: `/opt/logos/www/wallet_prod`
### wallet-proxy root chosen: `/opt/logos/wallet-proxy`

### nginx vhost files detected:
- `/etc/nginx/sites-available/logos.conf`
- `/etc/nginx/sites-available/logos.conf.bak_2025-12-13_090034`
- `/etc/nginx/sites-available/logos_front.bak`
- `/etc/nginx/sites-available/logos_front.bak.20251125T072637`
- `/etc/nginx/sites-available/logos_front.bak.20251127T134555`
- `/etc/nginx/sites-enabled/logos.conf`

## Parts
- `BOOK_1234_part001.md`

