# LOGOS — WALLET PERIMETER BOOK (FULL)

UTC build: 20260112T131955Z

- Detected PROD wallet dir: `/var/www/logos/wallet`

- Detected openapi.json: `/root/logos_lrb/node/openapi/openapi.json`

- Wallet-proxy dirs: `/opt/logos/wallet-proxy`, `/root/logos_lrb/wallet-proxy`


## API_BASE_URL / /api hints (from frontend grep)
```text
/var/www/logos/wallet/js/api.js:1:export const API = "/api";
/var/www/logos/wallet/js/core.js:2:export const API = "/api";
/var/www/logos/wallet/js/app_wallet.js:2:import { apiGet, apiPost } from "./api.js";
/var/www/logos/wallet/app.js:2:const API = location.origin + '/api/';     // ГАРАНТИРОВАННЫЙ префикс
/var/www/logos/wallet/wallet.js:2:// Подключение к API через /api (nginx proxy)
/var/www/logos/wallet/wallet.js:3:const BASE = location.origin + '/api';
/var/www/logos/wallet/app.v3.js:1:const API = location.origin + '/api/';
/var/www/logos/wallet/app.v2.js:2:const API = location.origin + '/api/';
/var/www/logos/wallet/staking.js:10:    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
/var/www/logos/wallet/staking.js:15:    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
/var/www/logos/wallet/staking.js:22:    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
/var/www/logos/wallet/staking.js:27:    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
/var/www/logos/wallet/staking.js:34:    const b=await (await fetch(`${location.origin + '/api'}/balance/${encodeURIComponent(session.rid)}`)).json();
/var/www/logos/wallet/staking.js:38:    const r=await fetch(`${location.origin + '/api'}/stake/submit`,{method:'POST',headers:{'Content-Type':'application/json'},
```


## NGINX snippets (wallet/api/proxy)
```nginx
    # root /var/www/wallet;
        proxy_pass http://127.0.0.1:8080;
upstream logos_wallet_api {
    location ^~ /wallet_v2/ {
        try_files $uri $uri/ /wallet_v2/index.html;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    location ^~ /wallet_dev/ {
        alias /opt/logos/www/wallet_dev/;
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    location ^~ /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
        proxy_pass http://logos_node_backend/;
    location = /wallet-api { return 301 /wallet-api/; }
    location ^~ /wallet-api/ {
        proxy_pass http://logos_wallet_api/;
    location ^~ /api/ {
        proxy_pass http://logos_node_backend/;
        proxy_pass http://logos_wallet_api/;
```


## SYSTEMD units (wallet/proxy/logos)
### systemd unit: logos-agent.service
```ini
# /etc/systemd/system/logos-agent.service
[Unit]
Description=Logos Codex Agent
After=network.target

[Service]
User=logos-agent
Group=logos-agent
EnvironmentFile=/etc/logos-agent.env
ExecStart=/opt/logos-agent/venv/bin/python /opt/logos-agent/agent.py --worker
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-airdrop-api.service
```ini
# /etc/systemd/system/logos-airdrop-api.service
[Unit]
Description=LOGOS Airdrop API (FastAPI on :8092, Postgres)
After=network.target postgresql.service
Requires=network.target postgresql.service

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-api

# Все секреты и DSN лежат здесь
EnvironmentFile=/etc/logos/airdrop-api.env
Environment=PYTHONUNBUFFERED=1

# Uvicorn внутри venv, 4 воркера
ExecStart=/opt/logos/airdrop-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8092 --workers 4 --proxy-headers

Restart=always
RestartSec=3
TimeoutStopSec=20
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-airdrop-tg-bot.service
```ini
# /etc/systemd/system/logos-airdrop-tg-bot.service
[Unit]
Description=LOGOS Airdrop Telegram Bot (subscription verifier)
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-tg-bot

# Никакие ключи не меняем — только подключаем где они лежат
EnvironmentFile=/etc/logos/logos_tg_bot.env
EnvironmentFile=/etc/logos/airdrop-api.env
EnvironmentFile=/etc/logos/node-main.env

Environment=TG_CHANNEL=@logosblockchain
Environment=AIRDROP_UPDATE_URL=http://127.0.0.1:8092/api/airdrop/update
Environment=AIRDROP_API_KEY_HEADER=X-API-Key
Environment=LOG_LEVEL=INFO

ExecStart=/opt/logos/airdrop-tg-bot/.venv/bin/python /opt/logos/airdrop-tg-bot/bot.py

Restart=always
RestartSec=3
TimeoutStopSec=20
LimitNOFILE=65535

StandardOutput=journal
StandardError=journal

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-airdrop-tg-verify.service
```ini
# /etc/systemd/system/logos-airdrop-tg-verify.service
[Unit]
Description=LOGOS Airdrop Telegram Verifier
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/airdrop-tg-bot

# Уже настроенные env (не меняем ключи, только подключаем)
EnvironmentFile=/etc/logos/node-main.env
EnvironmentFile=/etc/logos/airdrop-api.env

ExecStart=/opt/logos/airdrop-tg-bot/.venv/bin/python /opt/logos/airdrop-tg-bot/bot.py
Restart=always
RestartSec=2
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-guard-bot.service
```ini
# /etc/systemd/system/logos-guard-bot.service
[Unit]
Description=LOGOS Guard Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/var/www/logos/landing/logos_tg_bot/logos_guard_bot
ExecStart=/var/www/logos/landing/logos_tg_bot/logos_guard_bot/run_bot.sh
Restart=on-failure
RestartSec=5

# позже можно завести отдельного пользователя:
# User=logos
# Group=logos

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-healthcheck.service
```ini
# /etc/systemd/system/logos-healthcheck.service
[Unit]
Description=LOGOS LRB /readyz healthcheck

[Service]
Type=oneshot
ExecStart=/usr/local/bin/logos_readyz_check.sh

```

### systemd unit: logos-ledger-backup.service
```ini
# /etc/systemd/system/logos-ledger-backup.service
[Unit]
Description=LOGOS ledger backup (sled snapshot)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=root
ExecStart=/bin/bash -c 'set -euo pipefail; TS=$(date -u +%%Y-%%m-%%dT%%H-%%M-%%SZ); \
  systemctl stop logos-node@main; \
  tar -C /var/lib/logos -czf /var/backups/logos/ledger-$TS.tgz data.sled; \
  systemctl start logos-node@main; \
  find /var/backups/logos -type f -name "ledger-*.tgz" -mtime +14 -delete'

```

### systemd unit: logos-node.service
```ini
# /etc/systemd/system/logos-node.service
[Unit]
Description=LOGOS LRB Node
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
User=logos
Group=logos
ExecStart=/opt/logos/bin/logos_node
Restart=on-failure
RestartSec=2

# security hardening
AmbientCapabilities=
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
ReadWritePaths=/var/lib/logos

# env & secrets
EnvironmentFile=/etc/logos/keys.env
Environment=RUST_LOG=info
[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-node.service.d/00-prod.conf
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_LISTEN=127.0.0.1:8080
Environment=LRB_ARCHIVE_URL=postgres://logos:StrongPass123@127.0.0.1:5432/logos
Environment=LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
Environment=LRB_SLOT_MS=200
# сгенерируй рандомные секреты:
#  openssl rand -hex 32
Environment=LRB_JWT_\1=[REDACTED]
Environment=LRB_BRIDGE_\1=[REDACTED]

```

### systemd unit: logos-node@.service
```ini
# /etc/systemd/system/logos-node@.service
[Unit]
Description=LOGOS LRB Node (%i)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
EnvironmentFile=/etc/logos/node-%i.env
ExecStart=/opt/logos/bin/logos_node
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=read-only
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
CapabilityBoundingSet=
SystemCallFilter=@system-service @network-io ~keyctl
ReadWritePaths=/var/lib/logos /var/log/logos
RuntimeDirectory=logos
UMask=0077
[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-node@.service.d/10-restart-policy.conf
[Service]
Restart=on-failure
RestartSec=3
StartLimitIntervalSec=60
StartLimitBurst=5

# /etc/systemd/system/logos-node@.service.d/20-env.conf
[Service]
EnvironmentFile=-/etc/logos/node-%i.env

# /etc/systemd/system/logos-node@.service.d/30-hardening.conf
[Service]
# Sandbox
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=full
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
LockPersonality=true
MemoryDenyWriteExecute=true
RestrictRealtime=true
RestrictSUIDSGID=true
SystemCallArchitectures=native

# Разрешаем запись ТОЛЬКО где нужно
ReadWritePaths=/var/lib/logos
ReadWritePaths=/var/log/logos

# Ресурсные лимиты
LimitNOFILE=262144
LimitNPROC=8192

# Capabilities обрезаем в ноль
CapabilityBoundingSet=
AmbientCapabilities=

# /etc/systemd/system/logos-node@.service.d/31-bridge-key.conf
[Service]
Environment=LRB_BRIDGE_\1=[REDACTED]

# /etc/systemd/system/logos-node@.service.d/40-log.conf
[Service]
Environment=RUST_LOG=trace,logos=trace,consensus=trace,axum=info,h2=info,tokio=info

# /etc/systemd/system/logos-node@.service.d/41-faucet.conf
[Service]
# Типичные ключи, которые встречаются в таких сборках:
Environment=LOGOS_FAUCET_ENABLED=true
Environment=LRB_FAUCET_ENABLED=true
# (на некоторых билдах есть явный биндинг — пусть будет)
Environment=LOGOS_FAUCET_PATH=/faucet

# /etc/systemd/system/logos-node@.service.d/env.conf
[Service]
# Per-instance env (например /etc/logos/node-main.env)
EnvironmentFile=/etc/logos/node-%i.env
# Общие секреты (тот самый "keys", чтобы один раз положил — и все инстансы видят)
EnvironmentFile=/etc/logos/keys.env

# /etc/systemd/system/logos-node@.service.d/override.conf
[Service]
Environment=LOGOS_GENESIS_PATH=/etc/logos/genesis.yaml
Environment=LOGOS_NODE_KEY_PATH=/var/lib/logos/node_key

```

### systemd unit: logos-sled-backup.service
```ini
# /etc/systemd/system/logos-sled-backup.service
[Unit]
Description=Backup sled to /root/sled_backups

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/bin/logos-sled-backup.sh

```

### systemd unit: logos-snapshot.service
```ini
# /etc/systemd/system/logos-snapshot.service
[Unit]
Description=LOGOS LRB periodic snapshot

[Service]
Type=oneshot
EnvironmentFile=-/etc/logos/keys.env
ExecStart=/usr/bin/curl -s -H "X-Admin-Key: ${LRB_ADMIN_KEY}" \
  http://127.0.0.1:8080/admin/snapshot-file?name=snap-$(date +%%Y%%m%%dT%%H%%M%%S).json >/dev/null

```

### systemd unit: logos-wallet-proxy.service
```ini
# /etc/systemd/system/logos-wallet-proxy.service
[Unit]
Description=LOGOS Wallet Proxy (FastAPI + Uvicorn)
After=network-online.target
Wants=network-online.target

[Service]
EnvironmentFile=/etc/logos/wallet-proxy.env
User=logos
Group=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/wallet-proxy.env

ExecStart=/opt/logos/wallet-proxy/venv/bin/uvicorn app:app \
  --host 0.0.0.0 \
  --port 9090 \
  --workers 2

Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-wallet-proxy.service.d/override.conf
[Service]
EnvironmentFile=
EnvironmentFile=/etc/logos/wallet-proxy.env

# гарантируем, что таблица есть до старта uvicorn
ExecStartPre=/opt/logos/wallet-proxy/venv/bin/python3 /opt/logos/wallet-proxy/init_db.py

```

### systemd unit: logos-wallet-scanner.service
```ini
# /etc/systemd/system/logos-wallet-scanner.service
[Unit]
Description=LOGOS Wallet ETH->LRB USDT Scanner
After=network-online.target
Wants=network-online.target
PartOf=logos-wallet-proxy.service

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/wallet-proxy.env

ExecStart=/opt/logos/wallet-proxy/venv/bin/python /opt/logos/wallet-proxy/scanner.py

Restart=always
RestartSec=5

LimitNOFILE=65535
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-x-guard.service
```ini
# /etc/systemd/system/logos-x-guard.service
[Unit]
Description=LOGOS X Guard (Twitter airdrop verifier)
After=network-online.target logos-airdrop-api.service
Wants=network-online.target

[Service]
User=logos
Group=logos
WorkingDirectory=/opt/logos

EnvironmentFile=/etc/logos/node-main.env
EnvironmentFile=/etc/logos/airdrop-api.env

# PROD: не светим наружу, nginx/airdrop-api ходят по localhost
Environment=X_GUARD_BIND=127.0.0.1:8091

# Параметры "any лайк/ретвит/пост"
Environment=X_GUARD_RECENT_TWEETS=25
Environment=X_GUARD_USER_POSTS_SCAN=25
Environment=X_GUARD_MAX_PAGES=15
Environment=X_GUARD_TWEETS_CACHE_SEC=60
Environment=X_GUARD_CHECKS_CACHE_SEC=30

ExecStart=/opt/logos/bin/logos_x_guard
Restart=always
RestartSec=2
LimitNOFILE=65535
StandardOutput=journal
StandardError=journal

NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/logos-x-guard.service.d/override.conf
[Service]
Environment=X_GUARD_RECENT_TWEETS=8
Environment=X_GUARD_USER_POSTS_SCAN=8
Environment=X_GUARD_MAX_PAGES=3
Environment=X_GUARD_TWEETS_CACHE_SEC=600
Environment=X_GUARD_CHECKS_CACHE_SEC=180

```

### systemd unit: logos_guard_bot.service
```ini
# /etc/systemd/system/logos_guard_bot.service
[Unit]
Description=LOGOS Guard Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/www/logos/landing/logos_tg_bot/logos_guard_bot
ExecStart=/bin/bash /var/www/logos/landing/logos_tg_bot/logos_guard_bot/run_bot.sh
Restart=always
RestartSec=5
User=root
Group=root
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target

```

### systemd unit: lrb-proxy.service
```ini
# /etc/systemd/system/lrb-proxy.service
[Unit]
Description=LOGOS Wallet Proxy (FastAPI on :9090)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/proxy.env
ExecStart=/opt/logos/wallet-proxy/venv/bin/uvicorn app:app --host 0.0.0.0 --port 9090 --workers 2
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

```

### systemd unit: logos-healthcheck.timer
```ini
# /etc/systemd/system/logos-healthcheck.timer
[Unit]
Description=LOGOS LRB /readyz healthcheck timer

[Timer]
OnBootSec=30s
OnUnitActiveSec=30s
Unit=logos-healthcheck.service

[Install]
WantedBy=timers.target

```

### systemd unit: logos-ledger-backup.timer
```ini
# /etc/systemd/system/logos-ledger-backup.timer
[Unit]
Description=Nightly LOGOS ledger backup

[Timer]
OnCalendar=*-*-* 03:40:00 UTC
Persistent=true
RandomizedDelaySec=180

[Install]
WantedBy=timers.target

```

### systemd unit: logos-sled-backup.timer
```ini
# /etc/systemd/system/logos-sled-backup.timer
[Unit]
Description=Run sled backup every 15 minutes

[Timer]
OnBootSec=2m
OnUnitActiveSec=15m
Unit=logos-sled-backup.service

[Install]
WantedBy=timers.target

```

### systemd unit: logos-snapshot.timer
```ini
# /etc/systemd/system/logos-snapshot.timer
[Unit]
Description=Run LOGOS snapshot every 10 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=10min
Unit=logos-snapshot.service

[Install]
WantedBy=timers.target

```

---
## INCLUDED TARGETS
- `/var/www/logos/wallet`
- `/opt/logos/wallet-proxy`
- `/root/logos_lrb/wallet-proxy`
- `/root/logos_lrb/node/openapi`

## TOTAL FILES INCLUDED
- 27

## PARTS
- generated by script
