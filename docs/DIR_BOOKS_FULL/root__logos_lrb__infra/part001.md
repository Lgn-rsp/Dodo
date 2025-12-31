# LOGOS — Directory Book: /root/logos_lrb/infra

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/root/logos_lrb/infra
/root/logos_lrb/infra/systemd
/root/logos_lrb/infra/nginx
```

---

## FILES (FULL SOURCE)


### FILE: /root/logos_lrb/infra/systemd/exec.conf

```
[Service]
WorkingDirectory=/opt/logos
ExecStart=
ExecStart=/opt/logos/bin/logos_node

```

### FILE: /root/logos_lrb/infra/systemd/keys.conf

```
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key

# Реальные ключи
Environment=LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
Environment=LRB_BRIDGE_KEY=CHANGE_ME

```

### FILE: /root/logos_lrb/infra/systemd/keys.env.example

```
# Пример (НЕ БОЕВОЙ! замените на свои)
LRB_DATA_PATH=/var/lib/logos/data.sled
LRB_NODE_KEY_PATH=/var/lib/logos/node_key
LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
LRB_BRIDGE_KEY=CHANGE_ME
# LRB_ADMIN_JWT_SECRET=   # задаётся опционально

```

### FILE: /root/logos_lrb/infra/systemd/logos-healthcheck.service

```
[Unit]
Description=LOGOS healthcheck (HTTP)
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
EnvironmentFile=/etc/default/logos-healthcheck
ExecStart=/usr/local/bin/logos_healthcheck.sh

```

### FILE: /root/logos_lrb/infra/systemd/logos-node.service

```
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

### FILE: /root/logos_lrb/infra/systemd/logos-node.service.sample

```
# /etc/systemd/system/logos-node.service
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

# /etc/systemd/system/logos-node.service.d/exec.conf
[Service]
WorkingDirectory=/opt/logos
ExecStart=
ExecStart=/opt/logos/bin/logos_node

# /etc/systemd/system/logos-node.service.d/keys.conf
[Service]
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key

# Реальные ключи
Environment=LRB_ADMIN_KEY=0448012cf1738fd048b154a1c367cb7cb42e3fee4ab26fb04268ab91e09fb475
Environment=LRB_BRIDGE_KEY=b294771b022226e3a9d6e21f395c7b490a7f42e1fa203cd2fbb62eb3f4718bcf

# /etc/systemd/system/logos-node.service.d/override.conf
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

# /etc/systemd/system/logos-node.service.d/runas.conf
[Service]
User=logos
Group=logos
# разрешаем запись в каталог данных под sandbox
ReadWritePaths=/var/lib/logos

# /etc/systemd/system/logos-node.service.d/security.conf
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

# /etc/systemd/system/logos-node.service.d/tuning.conf
[Service]
Environment=LRB_SLOT_MS=500
Environment=LRB_MAX_BLOCK_TX=10000
Environment=LRB_MEMPOOL_CAP=100000
Environment=LRB_MAX_AMOUNT=18446744073709551615

# /etc/systemd/system/logos-node.service.d/zz-consensus.conf
[Service]
Environment=LRB_VALIDATORS=5Ropc1AQhzuB5uov9GJSumGWZGomE8CTvCyk8D1q1pHb
Environment=LRB_QUORUM_N=1
Environment=LRB_SLOT_MS=200

# /etc/systemd/system/logos-node.service.d/zz-keys.conf
[Service]
# читаем файл с секретами (на будущее)
EnvironmentFile=-/etc/logos/keys.env

# и ПРЯМО зашиваем реальные значения, чтобы перебить любой override
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key
Environment=LRB_ADMIN_KEY=0448012cf1738fd048b154a1c367cb7cb42e3fee4ab26fb04268ab91e09fb475
Environment=LRB_BRIDGE_KEY=b294771b022226e3a9d6e21f395c7b490a7f42e1fa203cd2fbb62eb3f4718bcf

# /etc/systemd/system/logos-node.service.d/zz-logging.conf
[Service]
Environment=RUST_LOG=info

```

### FILE: /root/logos_lrb/infra/systemd/logos-node@.service

```
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

### FILE: /root/logos_lrb/infra/systemd/logos-snapshot.service

```
[Unit]
Description=LOGOS LRB periodic snapshot

[Service]
Type=oneshot
EnvironmentFile=-/etc/logos/keys.env
ExecStart=/usr/bin/curl -s -H "X-Admin-Key: ${LRB_ADMIN_KEY}" \
  http://127.0.0.1:8080/admin/snapshot-file?name=snap-$(date +%%Y%%m%%dT%%H%%M%%S).json >/dev/null

```

### FILE: /root/logos_lrb/infra/systemd/lrb-proxy.service

```
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

### FILE: /root/logos_lrb/infra/systemd/lrb-proxy.service.sample

```
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

### FILE: /root/logos_lrb/infra/systemd/lrb-scanner.service

```
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

### FILE: /root/logos_lrb/infra/systemd/lrb-scanner.service.sample

```
# /etc/systemd/system/lrb-scanner.service
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

### FILE: /root/logos_lrb/infra/systemd/override.conf

```
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

### FILE: /root/logos_lrb/infra/systemd/runas.conf

```
[Service]
User=logos
Group=logos
# разрешаем запись в каталог данных под sandbox
ReadWritePaths=/var/lib/logos

```

### FILE: /root/logos_lrb/infra/systemd/security.conf

```
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

### FILE: /root/logos_lrb/infra/systemd/tuning.conf

```
[Service]
Environment=LRB_SLOT_MS=500
Environment=LRB_MAX_BLOCK_TX=10000
Environment=LRB_MEMPOOL_CAP=100000
Environment=LRB_MAX_AMOUNT=18446744073709551615

```

### FILE: /root/logos_lrb/infra/systemd/zz-consensus.conf

```
[Service]
Environment=LRB_VALIDATORS=5Ropc1AQhzuB5uov9GJSumGWZGomE8CTvCyk8D1q1pHb
Environment=LRB_QUORUM_N=1
Environment=LRB_SLOT_MS=200

```

### FILE: /root/logos_lrb/infra/systemd/zz-keys.conf

```
[Service]
# читаем файл с секретами (на будущее)
EnvironmentFile=-/etc/logos/keys.env

# и ПРЯМО зашиваем реальные значения, чтобы перебить любой override
Environment=LRB_DATA_PATH=/var/lib/logos/data.sled
Environment=LRB_NODE_KEY_PATH=/var/lib/logos/node_key
Environment=LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
Environment=LRB_BRIDGE_KEY=CHANGE_ME

```

### FILE: /root/logos_lrb/infra/systemd/zz-logging.conf

```
[Service]
Environment=RUST_LOG=info

```

### FILE: /root/logos_lrb/infra/nginx/logos-api-lb.conf.example

```
server {
    listen 80;
    server_name 45-159-248-232.sslip.io;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name 45-159-248-232.sslip.io;

    ssl_certificate     /etc/letsencrypt/live/45-159-248-232.sslip.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/45-159-248-232.sslip.io/privkey.pem;

    root /opt/logos/www;
    index index.html;

    # Статика: долгий кэш
    location /wallet/ {
        alias /opt/logos/www/wallet/;
        index index.html;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    # API → узел
    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Безопасность
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; connect-src 'self' http: https:; img-src 'self' data:; style-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'none';" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Permissions-Policy "accelerometer=(),camera=(),geolocation=(),microphone=()" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip/браузерные оптимизации
    gzip on; gzip_types text/plain text/css application/json application/javascript application/octet-stream image/svg+xml;
    gzip_min_length 1024;

    access_log /var/log/nginx/logos_access.log;
    error_log  /var/log/nginx/logos_error.log;
}

```

### FILE: /root/logos_lrb/infra/nginx/lrb_wallet.conf

```
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

### FILE: /root/logos_lrb/infra/nginx/lrb_wallet.conf.sample

```
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

    # --- Безопасные заголовки (минимальный набор без ломки фронта) ---
    add_header X-Frame-Options        SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header Referrer-Policy        strict-origin-when-cross-origin;

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
