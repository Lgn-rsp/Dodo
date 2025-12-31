# FULL SOURCE — `/root/logos_lrb/infra`

**No truncation.** Full file contents inside code fences.


---

## FILE: `/root/logos_lrb/infra/systemd/exec.conf`

```conf
[Service]
WorkingDirectory=/opt/logos
ExecStart=
ExecStart=/opt/logos/bin/logos_node
```

---

## FILE: `/root/logos_lrb/infra/systemd/keys.conf`

```conf
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key

# Реальные ключи
Environment=LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
Environment=LRB_BRIDGE_KEY=CHANGE_ME
```

---

## FILE: `/root/logos_lrb/infra/systemd/logos-healthcheck.service`

```service
[Unit]
Description=LOGOS healthcheck (HTTP)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=/etc/default/logos-healthcheck
ExecStart=/usr/local/bin/logos_healthcheck.sh
```

---

## FILE: `/root/logos_lrb/infra/systemd/logos-node.service`

```service
[Unit]
Description=LOGOS LRB Node (Axum REST on :8080)
After=network-online.target
Wants=network-online.target

[Service]
User=root
WorkingDirectory=/root/logos_lrb
ExecStart=/root/logos_lrb/target/release/logos_node
Restart=always
RestartSec=2
LimitNOFILE=65536
Environment=LRB_DEV=1

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## FILE: `/root/logos_lrb/infra/systemd/logos-node@.service`

```service
[Unit]
Description=LOGOS LRB Node (%i)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
Group=logos
EnvironmentFile=/etc/logos/node-%i.env
WorkingDirectory=/opt/logos
ExecStart=/opt/logos/bin/logos_node
Restart=always
RestartSec=1s
StartLimitIntervalSec=0
LimitNOFILE=1048576

# sandbox
AmbientCapabilities=
CapabilityBoundingSet=
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectKernelLogs=true
ProtectKernelModules=true
ProtectKernelTunables=true
ProtectControlGroups=true
ProtectClock=true
ProtectHostname=true
RestrictSUIDSGID=true
RestrictRealtime=true
LockPersonality=true
MemoryDenyWriteExecute=true
ReadWritePaths=/var/lib/logos /etc/logos
ProtectSystem=strict

# лог (journalctl -u logos-node@<inst>)
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## FILE: `/root/logos_lrb/infra/systemd/logos-snapshot.service`

```service
[Unit]
Description=LOGOS LRB periodic snapshot

[Service]
Type=oneshot
EnvironmentFile=-/etc/logos/keys.env
ExecStart=/usr/bin/curl -s -H "X-Admin-Key: ${LRB_ADMIN_KEY}" \
  http://127.0.0.1:8080/admin/snapshot-file?name=snap-$(date +%%Y%%m%%dT%%H%%M%%S).json >/dev/null
```

---

## FILE: `/root/logos_lrb/infra/systemd/lrb-proxy.service`

```service
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

---

## FILE: `/root/logos_lrb/infra/systemd/lrb-scanner.service`

```service
[Unit]
Description=LOGOS Wallet Scanner (USDT->rLGN)
After=network-online.target
Wants=network-online.target

[Service]
User=logos
WorkingDirectory=/opt/logos/wallet-proxy
EnvironmentFile=/etc/logos/proxy.env
ExecStart=/opt/logos/wallet-proxy/venv/bin/python /opt/logos/wallet-proxy/scanner.py
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

---

## FILE: `/root/logos_lrb/infra/systemd/override.conf`

```conf
[Service]
# Базовые ENV (правь под себя при необходимости)
Environment=LRB_DEV=1
Environment=LRB_PEERS=
Environment=LRB_QUORUM_N=1
Environment=LRB_VALIDATORS=

# Прод-тюнинг продюсера (можно менять без ребилда)
Environment=LRB_SLOT_MS=500
Environment=LRB_MAX_BLOCK_TX=10000
Environment=LRB_MEMPOOL_CAP=100000
Environment=LRB_MAX_AMOUNT=18446744073709551615

# rToken-мост (лимит и ключ для бриджа)
Environment=LRB_BRIDGE_MAX_PER_TX=10000000
# Админ для /admin/snapshot
```

---

## FILE: `/root/logos_lrb/infra/systemd/runas.conf`

```conf
[Service]
User=logos
Group=logos
# разрешаем запись в каталог данных под sandbox
ReadWritePaths=/var/lib/logos
```

---

## FILE: `/root/logos_lrb/infra/systemd/security.conf`

```conf
[Service]
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
LockPersonality=true
MemoryDenyWriteExecute=false

# Разрешаем запись ровно туда, где нужно
ReadWritePaths=/var/lib/logos /opt/logos /etc/logos

WorkingDirectory=/opt/logos
ExecStart=
ExecStart=/opt/logos/bin/logos_node
```

---

## FILE: `/root/logos_lrb/infra/systemd/tuning.conf`

```conf
[Service]
Environment=LRB_SLOT_MS=500
Environment=LRB_MAX_BLOCK_TX=10000
Environment=LRB_MEMPOOL_CAP=100000
Environment=LRB_MAX_AMOUNT=18446744073709551615
```

---

## FILE: `/root/logos_lrb/infra/systemd/zz-consensus.conf`

```conf
[Service]
Environment=LRB_VALIDATORS=5Ropc1AQhzuB5uov9GJSumGWZGomE8CTvCyk8D1q1pHb
Environment=LRB_QUORUM_N=1
Environment=LRB_SLOT_MS=200
```

---

## FILE: `/root/logos_lrb/infra/systemd/zz-keys.conf`

```conf
[Service]
# читаем файл с секретами (на будущее)
EnvironmentFile=-/etc/logos/keys.env

# и ПРЯМО зашиваем реальные значения, чтобы перебить любой override
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key
Environment=LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
Environment=LRB_BRIDGE_KEY=CHANGE_ME
```

---

## FILE: `/root/logos_lrb/infra/systemd/zz-logging.conf`

```conf
[Service]
Environment=RUST_LOG=info
```

---

## FILE: `/root/logos_lrb/infra/nginx/lrb_wallet.conf`

```conf
# Глобальные зоны rate-limit (по IP)
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=proxy_zone:10m rate=10r/s;

map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    server_name _;

    # --- Безопасные заголовки ---
    add_header X-Frame-Options        SAMEORIGIN       always;
    add_header X-Content-Type-Options nosniff          always;
    add_header Referrer-Policy        strict-origin-when-cross-origin always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # CSP: только self, без inline/CDN. Разрешаем data: для иконок/картинок в UI.
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; connect-src 'self' http: https:; img-src 'self' data:; style-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none';" always;

    # --- Gzip для JSON/JS/CSS/HTML ---
    gzip on;
    gzip_types text/plain text/css application/json application/javascript application/xml;
    gzip_min_length 1024;

    # --- Редирект корня на кошелёк ---
    location = / {
        return 302 /wallet/;
    }

    # --- Кошелёк (статические файлы) ---
    location /wallet/ {
        root /opt/logos/www;
        index index.html;
        try_files $uri $uri/ /wallet/index.html;
        # кэш статики
        location ~* \.(?:js|css|png|jpg|jpeg|gif|svg|ico)$ {
            expires 30d;
            access_log off;
        }
    }

    # --- LRB node API (Axum на 8080) ---
    location /api/ {
        limit_req zone=api_zone burst=60 nodelay;

        proxy_read_timeout      30s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      15s;

        proxy_set_header Host                $host;
        proxy_set_header X-Real-IP           $remote_addr;
        proxy_set_header X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto   $scheme;

        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_pass http://127.0.0.1:8080/;
    }

    # --- Wallet Proxy (FastAPI на 9090) ---
    location /proxy/ {
        limit_req zone=proxy_zone burst=20 nodelay;

        proxy_read_timeout      30s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      15s;

        proxy_set_header Host                $host;
        proxy_set_header X-Real-IP           $remote_addr;
        proxy_set_header X-Forwarded-For     $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto   $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade             $http_upgrade;
        proxy_set_header Connection          $connection_upgrade;

        proxy_pass http://127.0.0.1:9090/;
    }

    # --- Закрыть доступ к скрытому/служебному ---
    location ~ /\.(?!well-known) {
        deny all;
    }
}
```
