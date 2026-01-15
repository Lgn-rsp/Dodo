# LOGOS WALLET — BOOK 444

**Дата сборки книги (UTC):** 2026-01-15T10:56:44Z

Эта книга собрана автоматически из пакета: `logos_wallet_pack_v555_20260115T103920Z.tar.gz`.

---

## 1) Что именно зафиксировано
- Полный слепок **wallet_prod** (и при наличии wallet_dev / wallet_premium)
- nginx vhost'ы и upstream'ы (маршрутизация /node-api и /wallet-api)
- systemd unit'ы (как реально подняты сервисы)
- OpenAPI ноды (если было доступно при сборке пакета)
- хвост логов (для диагностики LGN send)

---

## 2) Канонический инвентарь (паспорт сборки)

### 2.1 Источник правды
- **Активная версия UI:** wallet_prod
- wallet_dev: присутствует (сравнение старых ручек/модулей)
- wallet_premium: присутствует (сравнение UX/верстки)

### 2.2 Обязательные файлы
| Файл/папка | Назначение |
|---|---|
| auth.html/auth.js/auth.css | onboarding: create/confirm/restore/unlock |
| app.html/app.js/app.css | основной кошелек UI |
| modules/ | модули (LGN send и др.) |
| vendor/ | зависимости (wordlist/bip39_lite/nacl) |

### 2.3 Дерево wallet_prod
```
./api_base.js
./app.css
./app.html
./app.html.bak_defer_20260113T144828Z
./app.html.bak_lgn_script_20260113T161416Z
./app.html.bak_lgn_ui_20260113T160813Z
./app.html.bak_ridfix_20260114T082058Z
./app.html.bak_seed_20260114T073805Z
./app.js
./app.js.bak_sendfix_20260114T084901Z
./assets.js
./auth.css
./auth.css.bad_20260114T075224Z
./auth.css.bak_seed_ui_20260114T102523Z
./auth.html
./auth.html.bad_20260114T075205Z
./auth.html.bak_20260114T073719Z
./auth.html.bak_add_bip39lite_20260114T100145Z
./auth.html.bak_bip39_20260114T083211Z
./auth.html.bak_bip39lite_20260114T084844Z
./auth.html.bak_bip39loader_20260114T083924Z
./auth.html.bak_clean_20260114T095410Z
./auth.html.bak_fix_bip39lite_20260114T090446Z
./auth.html.bak_fix_loader_20260114T080919Z
./auth.html.bak_seed_ui_20260114T102523Z
./auth.js
./auth.js.bak_20260113T164701Z
./auth.js.bak_bip39fix_20260114T083232Z
./auth.js.bak_bip39lite_patch_20260114T092639Z
./auth.js.bak_fix_ed25519_20260114T065333Z
./auth.js.bak_fix_syntax_20260114T095429Z
./auth.js.bak_fullreplace_20260114T073738Z
./auth.js.bak_keypersist_20260113T163557Z
./auth.js.bak_keysfix_20260113T173340Z
./auth.js.bak_profiles_20260114T071654Z
./auth.js.bak_seed_ui_20260114T102523Z
./compat.js
./connect.js
./index.html
./index.html.bak_20260114T073703Z
./login.html
./modules/lgn_send.js
./modules/lgn_send.js.bad_20260113T164615Z
./modules/lgn_send.js.bak_20260113T161920Z
./modules/lgn_send.js.bak_fix_20260113T163514Z
./modules/lgn_send.js.bak_fix_20260113T171032Z
./modules/lgn_send.js.bak_fix_20260113T173041Z
./modules/lgn_send.js.bak_seed_20260114T073821Z
./modules/send.js
./modules/send.js.bak_20260113T150254Z
./modules/send.js.bak_broken_20260113T153553Z
./modules/send.js.bak_broken_20260113T153640Z
./modules/settings.js
./modules/settings.js.bak_clear_20260113T144947Z
./modules/tx_redirect.js
./tabs.js
./ui.css
./ui.js
./vendor/bip39_english.txt
./vendor/bip39_lite.js
./vendor/bip39_lite.js.bak_20260114T092555Z
./vendor/bip39_lite.js.bak_20260114T100204Z
./vendor/nacl-fast.min.js
./vendor/wordlist_en.js
./wallet.css
```

### 2.4 SHA256 (wallet_prod)
```
e447e8998505330a10f36d079df1b368f1c561e6479596c2adf6ea3e2feb25a6  ./api_base.js
3c7185635d3801bccc82f9a56334f0fb8a8c6806b18132ffaf882b127c6bb1ac  ./app.css
a4311f437115be870252365b41806e2ef82d15285c38a7eff78ca2349e266be9  ./app.html
beb333f8331af2127b15c0100180189dfbf3d6e7e4b3eca22ce50262a1dbb9c1  ./app.html.bak_defer_20260113T144828Z
5b35a0c08d1908afed902ce6fba13fc1d989a11be68a557745c4ac3e0c478972  ./app.html.bak_lgn_script_20260113T161416Z
07946da99c1e59411acd1cf533196ca6cfb07a1b835b717ff81dd71a4482e827  ./app.html.bak_lgn_ui_20260113T160813Z
a4311f437115be870252365b41806e2ef82d15285c38a7eff78ca2349e266be9  ./app.html.bak_ridfix_20260114T082058Z
a4311f437115be870252365b41806e2ef82d15285c38a7eff78ca2349e266be9  ./app.html.bak_seed_20260114T073805Z
c706c5689a798adcdd77c046a2c77de3fd31d2537e5783a1b47ac9646b7ef62b  ./app.js
c6a5689dc4f0b5c8f2b3988ca6d701698047b5562b3d445c50bd6006aba4be75  ./app.js.bak_sendfix_20260114T084901Z
c7138e4217262dfa8aa59f60c6497cb7075c0158cee66b8f5ff3476c56d2cc61  ./assets.js
f33818be958fae6005abc553e12412c948bd7957f0d0a606782f86a62960d730  ./auth.css
5bb92959c854d22f3ee130a885db5b63cc7b8ddef762aad30a83b7d9f0ea52c7  ./auth.css.bad_20260114T075224Z
cbab4d783ea3fc5660653ad81002f06939f647209d3911cc0a91899b16714bd3  ./auth.css.bak_seed_ui_20260114T102523Z
a60ef9e6cac94116727fc87b5a190b8a8bd41ef9788329217e9b2db634a5b126  ./auth.html
bac0a4adae4464eef883f814e37ec768801f5bf9f85852271846f86263567b9d  ./auth.html.bad_20260114T075205Z
a3645e89d40dc5efb024de2e2e71e2eeb4e700ecf4c918ce47e3f8baf86fecde  ./auth.html.bak_20260114T073719Z
6aff57e627f688677a0e9831322db8785f486a2169aab11cd8628aaa2c05ee8b  ./auth.html.bak_add_bip39lite_20260114T100145Z
29baeb9532ae39b1fad5a732599f3d142b79029d97e804db211000413b915e04  ./auth.html.bak_bip39_20260114T083211Z
fe93fc8db31ca4d5237ea63c42a4157610799a062d2bd3c0bd9ee2db448ec59b  ./auth.html.bak_bip39lite_20260114T084844Z
400e23a5ff8ab3f27c21cefd5d892a5a4a47fc798a1662fda48164ad1ec8610c  ./auth.html.bak_bip39loader_20260114T083924Z
95d5e1f62924de69dc57f9c23858d51c4f3877982b995f480cd3544c42aed9b5  ./auth.html.bak_clean_20260114T095410Z
335d629f0135fae68b1ddb24b70541967a47740c8fdb7cd94fad905f83b15d1f  ./auth.html.bak_fix_bip39lite_20260114T090446Z
4f89ed386bb112c895daf063d03112cdd8cb0a3fdaa5623a29bb70af85f40e6d  ./auth.html.bak_fix_loader_20260114T080919Z
88969ce498a2bfe3a9de6c9ec58b4aa26f09bec7451a82061dd9b53b00a19922  ./auth.html.bak_seed_ui_20260114T102523Z
be4383e0811130ff1180baec11136961a8b980c9aa4317eb1a063205e2c97501  ./auth.js
612a1bf16812b3e679d7a61822bda0ad81cb13f9bb31d2714e4e2ff47c6c78d2  ./auth.js.bak_20260113T164701Z
a73c79ebb3c913a122640540bc3d8847994d9012aabd902aa992f398dd303a94  ./auth.js.bak_bip39fix_20260114T083232Z
eefc7eb8412857a47b660958164bbfc5f04e822f2a330d2f49b67798189a69f9  ./auth.js.bak_bip39lite_patch_20260114T092639Z
97a4d8a381b1471db9c5c3bef4b7159facf1f5e888f7722fc2b20817af5592ce  ./auth.js.bak_fix_ed25519_20260114T065333Z
f57eb77741dc0b59d58e05d32c53fc55bc7e3384ed124f85aa3b8ae82f4236d0  ./auth.js.bak_fix_syntax_20260114T095429Z
3351e32216c8f64eb23d51b22def793d2325ba87c38a28a711c869c89c8e9e77  ./auth.js.bak_fullreplace_20260114T073738Z
340fcebf27f293763e6d2729e4ccb751969e7f68315ba524eaad4a5c4411e182  ./auth.js.bak_keypersist_20260113T163557Z
612a1bf16812b3e679d7a61822bda0ad81cb13f9bb31d2714e4e2ff47c6c78d2  ./auth.js.bak_keysfix_20260113T173340Z
b3fc449e5063d6e306dd8b088811f5bf704604842cf90f2d902c6af3df27f223  ./auth.js.bak_profiles_20260114T071654Z
6eb7fea6b56f26e72d4b8bbfbdb7e73df6516ee644c93a631027409169391f36  ./auth.js.bak_seed_ui_20260114T102523Z
a178c9fb576fbacbd49c8dd57e116b4d6e0b43c73677d826dde3d2adf393bb69  ./compat.js
780dbed59f7f8e01732f51ff0185c31a4bd8c51359ca8eba40716e2d2aabd3cd  ./connect.js
f06ebe167ccc82292e0d278c86b07bf254fc0627c51e16616ac27138c8a60f4b  ./index.html
70da1159649c00925542db4990ad894a30ffae46167fa2de4b539f94dce1bd9a  ./index.html.bak_20260114T073703Z
409ff9c314f528c39591bcd2cb7bc400fc1eb9c9e25669f231ff1b73c1cd35d0  ./login.html
27b86a434816cd5e2555a1652b13cd3dfcffc8416c6a97e59f471abb533d457a  ./modules/lgn_send.js
e46530af850763e8e9a984f631b0210e98c619bede42ea62101612c2def76e38  ./modules/lgn_send.js.bad_20260113T164615Z
b0cb5cf96943d6a1690fa1c9987239ad82c36e181577a812be8084e33e93a260  ./modules/lgn_send.js.bak_20260113T161920Z
599e868288dc4e1108e675df59a56beabb377b45accc9b16edf05de6418e17ea  ./modules/lgn_send.js.bak_fix_20260113T163514Z
c7bb6b0f700e8fa74323c14eafcdaaf3e33aad2a0843ac9271ed78a61835a37d  ./modules/lgn_send.js.bak_fix_20260113T171032Z
ea97936a35f26631d48a9429e50a553fbcb1e303d3bd21b355ca43b35d643e71  ./modules/lgn_send.js.bak_fix_20260113T173041Z
6fd51aa76e4a20f1375ae9d65515e0798c67a2cfa75c687b0369d8751f8222b8  ./modules/lgn_send.js.bak_seed_20260114T073821Z
a8b286596057fe7c955c0c7be36620e52cb36d33d2cadc0353bacc2458d38ab3  ./modules/send.js
015fbc6b85158f2da785dcf9284d0bc8f299e91c210399143a5f51b71bad9002  ./modules/send.js.bak_20260113T150254Z
a8b286596057fe7c955c0c7be36620e52cb36d33d2cadc0353bacc2458d38ab3  ./modules/send.js.bak_broken_20260113T153553Z
a8b286596057fe7c955c0c7be36620e52cb36d33d2cadc0353bacc2458d38ab3  ./modules/send.js.bak_broken_20260113T153640Z
e2a8a285289472b5ae5677ebb6869e6a33e707e670e41488a227f8c2beefc3e6  ./modules/settings.js
3dd796db98ca40f0a7ed939085b39f688f8b55bae8d9381b0ec78fe8d25eac8d  ./modules/settings.js.bak_clear_20260113T144947Z
14d7c5b092238a1d20fddb2d5c5f333337c1cc1eaba5fe76d328a75267294b0f  ./modules/tx_redirect.js
469e4796efc07d114b121e511b4a44f37fc42b85b7551868f74fa7c769f4786a  ./tabs.js
50b76a402741dad8aadafaa10bbcd00463f864129907bec514db771f80abfaa8  ./ui.css
e2814b431d1cf6c38a9f2efb1513d597b402d488d40e968cb87289c66f92f550  ./ui.js
2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda  ./vendor/bip39_english.txt
67aea87206e1edf2673d7e1716adf7156a882f61a91ce41beb57b393abf63a68  ./vendor/bip39_lite.js
fdfed8c4e96abc0b21d3b0c72631be013e8aac1cea2507f17f01cdfe98e3b106  ./vendor/bip39_lite.js.bak_20260114T092555Z
73cc3a9b649212889ee619369c7237118eef33ea0a8573816ff5ffe1bdc6f4ce  ./vendor/bip39_lite.js.bak_20260114T100204Z
3ec535c004aeeb225785d8e93fb33bf99f52e399bd7dfc01969b5629baea5131  ./vendor/nacl-fast.min.js
fb625e9a8ab2248c93a6e63998de30420d9a126c6a715f37cdcd4b97f95ef51e  ./vendor/wordlist_en.js
d808788cbb5a493d8185bb14b7021d8bcaeed7a56ce194e49e02c8aaf9607a9f  ./wallet.css
```

---

## 3) Nginx (sites-enabled / sites-available)

### sites-enabled
```
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-enabled/logos.conf
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-enabled/logos.conf -----
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    root /opt/logos/www;
    index index.html;

    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    location ^~ /wallet_v2/ {
        try_files $uri $uri/ /wallet_v2/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet_dev/ {
        alias /opt/logos/www/wallet_dev/;
        index index.html;
        try_files $uri $uri/ /wallet_dev/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    }
    location ^~ /wallet/ {
        alias /opt/logos/www/wallet_prod/;
        index index.html;
        try_files $uri $uri/ /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api https://mw-expedition.com/wallet-api; img-src 'self' data:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self';" always;
    }

location ^~ /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/node-api;" always;
    }

    location = /node-api { return 301 /node-api/; }
    location ^~ /node-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location = /wallet-api { return 301 /wallet-api/; }
    location ^~ /wallet-api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Совместимость (старые пути)
    location ^~ /api/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ^~ /proxy/ {
        limit_req zone=api_zone burst=60 nodelay;
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}
```

### sites-available
```
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.1763742292
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.1763742292 -----
server {
    listen 80;
    server_name apk.darken.top;

    root /var/www/logos/landing;
    index index.html;

    # Лендинг как SPA
    location / { try_files $uri $uri/ /index.html; }

    # Долгие кеши для статики
    location ~* \.(?:css|js|svg|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    # Прокси к ноде (если нужно)
    location /api/ {
        proxy_pass http://127.0.0.1:8081/;
        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;
    }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251120T170654
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251120T170654 -----
server {
    listen 80;
    server_name apk.darken.top;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name apk.darken.top;

    ssl_certificate     /etc/letsencrypt/live/apk.darken.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/apk.darken.top/privkey.pem;

    # Security headers (strict)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self' https://apk.darken.top; base-uri 'self'; form-action 'self'" always;
    server_tokens off;

    # Root (landing)
    root /var/www/logos/landing;
    index index.html;

    # Gzip (brotli — по желанию, если модуль есть)
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Long cache for immutable assets (versioned filenames)
    location ~* \.(?:css|js|jpg|jpeg|png|svg|webp|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # APK remains unchanged
    location /apk/ {
        alias /var/www/logos/apk/;
        add_header Content-Disposition "attachment";
        try_files $uri =404;
    }

    # API proxy to node
    location /api/ {
        proxy_pass http://127.0.0.1:8081/;
        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;
    }

    # (Опционально) кошелёк/эксплорер, если нужны:
    # location /wallet/ { alias /opt/logos/www/wallet/; try_files $uri $uri/ /wallet/index.html; }
    # location /explorer/ { alias /opt/logos/www/explorer/; try_files $uri $uri/ /explorer/index.html; }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251127T134555
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251127T134555 -----
# Upstream'ы для API
upstream logos_api {
    server 127.0.0.1:8090;
    keepalive 64;
}

upstream airdrop_api {
    server 127.0.0.1:8090;
    keepalive 64;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;
    charset utf-8;

    # Отдельные логи проекта
    access_log /var/log/nginx/logos_front.access.log;
    error_log  /var/log/nginx/logos_front.error.log warn;

    # Безопасность
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header Permissions-Policy "geolocation=(), camera=(), microphone=()" always;

    # Сжатие — экономим трафик и ускоряем отдачу
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_vary on;
    gzip_proxied any;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/xml
        application/rss+xml
        font/woff2
        application/font-woff2
        image/svg+xml;

    # --- SPA фронт
    location / {
        try_files $uri $uri/ /index.html;
    }

    # --- Статика с долгим кешем
    location ~* \.(?:css|js|ico|png|jpe?g|gif|svg|webp|woff2?|ttf|eot)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # --- Airdrop API (FastAPI)
    location /api/airdrop/ {
        proxy_pass http://airdrop_api;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout      60s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      60s;

        # Буферизация для массовых нагрузок
        proxy_buffering on;
        proxy_buffers 32 16k;
        proxy_busy_buffers_size 64k;
    }

    # --- Основной LOGOS API
    location /api/ {
        proxy_pass http://logos_api;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout      120s;
        proxy_connect_timeout   5s;
        proxy_send_timeout      120s;

        proxy_buffering on;
        proxy_buffers 32 32k;
        proxy_busy_buffers_size 256k;
        # сюда можно навесить лимиты RPS, если нужно:
        # limit_req zone=api_burst burst=20 nodelay;
    }

    # SSL от Let's Encrypt
    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# HTTP -> HTTPS редирект
server {
    listen 80;
    listen [::]:80;
    server_name mw-expedition.com www.mw-expedition.com;

    return 301 https://$host$request_uri;
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos.conf.bak_2025-12-13_090034
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos.conf.bak_2025-12-13_090034 -----
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

# WebSocket/upgrade helper
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

# Узел LOGOS (REST API)
upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

# Wallet-proxy (депозиты USDT -> rLGN)
upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

# Airdrop API — upstream объявлен в /etc/nginx/conf.d/logos_airdrop_upstream.conf
# upstream logos_airdrop_api { ... }

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    # По умолчанию — статика кошелька/эксплорера
    root /opt/logos/www;
    index index.html;

    # === Лендинг ===
    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    # Страница аирдропа /airdrop.html
    # === Wallet SPA ===
    location /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api https://mw-expedition.com/proxy https://vnet.web3games.org https://mainnet.infura.io;" always;
    }

    # === Explorer SPA ===
    location /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        # Разрешаем inline-стили и скрипты для explorer, API остаётся только self
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api;" always;
    }

    # === REST API ноды ===
    location /api/ {
        limit_req zone=api_zone burst=60 nodelay;

        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Wallet-proxy API ===
    location /proxy/ {
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Airdrop API ===
    # Общая статика (JS/CSS/иконки)
    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos.conf
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos.conf -----
# Лимиты запросов к API
limit_req_zone $binary_remote_addr zone=api_zone:10m rate=30r/s;

# WebSocket/upgrade helper
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

# Узел LOGOS (REST API)
upstream logos_node_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

# Wallet-proxy (депозиты USDT -> rLGN)
upstream logos_wallet_api {
    server 127.0.0.1:9090;
    keepalive 16;
}

# Airdrop API — upstream объявлен в /etc/nginx/conf.d/logos_airdrop_upstream.conf
# upstream logos_airdrop_api { ... }

server {
    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;

    # По умолчанию — статика кошелька/эксплорера
    root /opt/logos/www;
    index index.html;

    # === Лендинг ===
    location = / {
        root /var/www/logos/landing;
        try_files /index.html =404;
        add_header Cache-Control "no-store" always;
    }

    # Страница аирдропа /airdrop.html
    # === Wallet SPA ===
    location /wallet/ {
        try_files $uri /wallet/index.html;
        add_header Cache-Control "no-store" always;
        add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api https://mw-expedition.com/proxy https://vnet.web3games.org https://mainnet.infura.io;" always;
    }

    # === Explorer SPA ===
    location /explorer/ {
        try_files $uri /explorer/index.html;
        add_header Cache-Control "no-store" always;
        # Разрешаем inline-стили и скрипты для explorer, API остаётся только self
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://mw-expedition.com https://mw-expedition.com/api;" always;
    }

    # === REST API ноды ===
    location /api/ {
        limit_req zone=api_zone burst=60 nodelay;

        proxy_pass http://logos_node_backend/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Wallet-proxy API ===
    location /proxy/ {
        proxy_pass http://logos_wallet_api/;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # === Airdrop API ===
    # Общая статика (JS/CSS/иконки)
    location ~* \.(?:css|js|ico|png|jpg|jpeg|svg|woff2?)$ {
        try_files $uri =404;
        add_header Cache-Control "no-store" always;
    }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak -----
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;

    charset utf-8;

    # Базовая защита
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # --- Лендинг LOGOS (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # --- Статика с долгим кэшем
    location ~* \.(?:css|js|ico|png|jpe?g|gif|svg|webp|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # --- Airdrop API (FastAPI на 127.0.0.1:8092)
    # более специфичный префикс, чем /api/, поэтому всегда пойдёт сюда
    location /api/airdrop/ {
        proxy_pass         http://127.0.0.1:8092;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout    60s;
        proxy_connect_timeout 5s;
        proxy_send_timeout    60s;
    }

    # --- Прокси к ноде LOGOS (если используешь HTTP API ноды)
    # если порт другой — просто поправь 8090 на свой
    location /api/ {
        proxy_pass         http://127.0.0.1:8090;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout    120s;
        proxy_connect_timeout 5s;
        proxy_send_timeout    120s;
    }

    ssl_certificate     /etc/letsencrypt/live/mw-expedition.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

# HTTP → HTTPS редирект
server {
    listen 80;
    listen [::]:80;
    server_name mw-expedition.com www.mw-expedition.com;

    return 301 https://$host$request_uri;
}

.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251119T165850
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251119T165850 -----
server {
    listen 127.0.0.1:8080;

    # Faucet-заглушка: всегда 200 "ok"
    location ~ ^/faucet/[^/]+/\d+$ {
        default_type text/plain;
        return 200 "ok\n";
    }

    # Всё остальное — прокси на ноду (которая слушает 127.0.0.1:8081)
    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header Connection "";
        proxy_buffering off;
    }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251125T072637
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251125T072637 -----
server {
    server_name mw-expedition.com www.mw-expedition.com;

    root /var/www/logos/landing;
    index index.html;

    add_header X-Content-Type-Options "nosniff" always;

    # Лендинг LOGOS (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Статика с долгим кэшем
    location ~* \.(?:css|js|svg|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    # Прокси к ноде (если решим использовать /api/)
    location /api/ {
        proxy_pass http://127.0.0.1:8081/;
        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/mw-expedition.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/mw-expedition.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}

server {
    if ($host = www.mw-expedition.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = mw-expedition.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name mw-expedition.com www.mw-expedition.com;
    return 404; # managed by Certbot




}.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos-node-8000.conf
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos-node-8000.conf -----
server {
    listen 8000;
    server_name _;
    # если будете раздавать фронт-кошелёк со статикой — пропишите root
    # root /var/www/wallet;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos -----
server {
  listen 80; server_name 45-159-248-232.sslip.io;
  return 301 https://$host$request_uri;
}
server {
  listen 443 ssl http2;
  server_name 45-159-248-232.sslip.io;
  ssl_certificate     /etc/letsencrypt/live/45-159-248-232.sslip.io/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/45-159-248-232.sslip.io/privkey.pem;

  root /var/www/logos;
  index index.html;

  # точный корень -> SPA
  location = / { try_files /index.html =404; add_header Cache-Control "no-store"; }

  # API -> узел
  location ^~ /api/ {
    proxy_pass http://127.0.0.1:8080/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Connection "";
    proxy_buffering off;
  }

  # SPA fallback
  location / { try_files $uri $uri/ /index.html; }

  access_log /var/log/nginx/logos_access.log;
  error_log  /var/log/nginx/logos_error.log warn;
}
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251120T172228
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/nginx/sites-available/logos_front.bak.20251120T172228 -----
server {
    listen 80;
    server_name apk.darken.top;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name apk.darken.top;

    ssl_certificate     /etc/letsencrypt/live/apk.darken.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/apk.darken.top/privkey.pem;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;

    root /var/www/logos/landing;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(?:css|js|svg|webp|woff2?)$ {
        access_log off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8081/;
        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;
    }
}
```

---

## 4) systemd units
```
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-node.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-node.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/alertmanager.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/alertmanager.service -----
[Unit]
Description=Alertmanager
After=network-online.target

[Service]
EnvironmentFile=/etc/alertmanager/secrets.env
ExecStart=/usr/local/bin/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --storage.path=/var/lib/alertmanager \
  --web.listen-address=127.0.0.1:9093 \
  --cluster.listen-address=127.0.0.1:19094
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-wallet-scanner.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-wallet-scanner.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-proxy.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-proxy.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-tg-verify.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-tg-verify.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/node-exporter.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/node-exporter.service -----
[Unit]
Description=Node Exporter (Prometheus)
After=network-online.target

[Service]
User=nodeexp
Group=nodeexp
ExecStart=/usr/local/bin/node_exporter \
  --collector.textfile.directory=/var/lib/node_exporter/textfile
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-x-guard.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-x-guard.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-api.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-api.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-tg-bot.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-airdrop-tg-bot.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/grafana.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/grafana.service -----
[Unit]
Description=Grafana
After=network-online.target

[Service]
User=grafana
Group=grafana
ExecStart=/usr/share/grafana/bin/grafana-server \
  --homepath=/usr/share/grafana \
  --config=/etc/grafana/grafana.ini
WorkingDirectory=/usr/share/grafana
Restart=always
RestartSec=2
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-exporter.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-exporter.service -----
[Unit]
Description=LRB textfile exporter (economy/head)

[Service]
Type=oneshot
ExecStart=/usr/local/bin/lrb_exporter.sh
User=nodeexp
Group=nodeexp
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-healthcheck.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-healthcheck.service -----
[Unit]
Description=LOGOS LRB /readyz healthcheck

[Service]
Type=oneshot
ExecStart=/usr/local/bin/logos_readyz_check.sh
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-snapshot.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-snapshot.service -----
[Unit]
Description=LOGOS LRB periodic snapshot

[Service]
Type=oneshot
EnvironmentFile=-/etc/logos/keys.env
ExecStart=/usr/bin/curl -s -H "X-Admin-Key: ${LRB_ADMIN_KEY}" \
  http://127.0.0.1:8080/admin/snapshot-file?name=snap-$(date +%%Y%%m%%dT%%H%%M%%S).json >/dev/null
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-guard-bot.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-guard-bot.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-scanner.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/lrb-scanner.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-agent.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-agent.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-wallet-proxy.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-wallet-proxy.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-ledger-backup.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-ledger-backup.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos_guard_bot.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos_guard_bot.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-node@.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-node@.service -----
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
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-sled-backup.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/logos-sled-backup.service -----
[Unit]
Description=Backup sled to /root/sled_backups

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/bin/logos-sled-backup.sh
.work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/prometheus.service
----- .work_book_444/logos_wallet_pack_v555_20260115T103920Z/systemd/system/prometheus.service -----
[Unit]
Description=Prometheus
After=network-online.target

[Service]
User=prom
Group=prom
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.enable-lifecycle \
  --web.listen-address=127.0.0.1:9094
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

---

## 5) Node OpenAPI

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "LOGOS LRB — Core API",
    "version": "0.1.0",
    "description": "Public & Admin API for LOGOS LRB (strict CSP, JWT admin, rToken bridge, archive)"
  },
  "servers": [{ "url": "https://45-159-248-232.sslip.io" }],
  "paths": {
    "/healthz": {
      "get": { "summary": "Healthcheck", "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/OkMsg" } } } } } }
    },
    "/head": {
      "get": { "summary": "Chain head", "responses": { "200": { "description": "Head", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Head" } } } } } }
    },
    "/balance/{rid}": {
      "get": {
        "summary": "Account balance & nonce",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": { "200": { "description": "Balance", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Balance" } } } } }
      }
    },
    "/submit_tx": {
      "post": {
        "summary": "Submit transaction",
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/TxIn" } } } },
        "responses": { "200": { "description": "Result", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SubmitResult" } } } } }
      }
    },
    "/economy": {
      "get": { "summary": "Economy snapshot", "responses": { "200": { "description": "Economy", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/Economy" } } } } } }
    },
    "/history/{rid}": {
      "get": {
        "summary": "History by RID (from sled index)",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "History", "content": { "application/json": { "schema": { "type": "array", "items": { "$ref": "#/components/schemas/HistoryItem" } } } } }
        }
      }
    },
    "/archive/history/{rid}": {
      "get": {
        "summary": "History by RID (archive backend: SQLite/PG)",
        "parameters": [{ "name": "rid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "History", "content": { "application/json": { "schema": { "type": "array", "items": { "type": "object" } } } } }
        }
      }
    },
    "/archive/tx/{txid}": {
      "get": {
        "summary": "Get TX by txid (archive backend)",
        "parameters": [{ "name": "txid", "in": "path", "required": true, "schema": { "type": "string" } }],
        "responses": {
          "200": { "description": "TX (if any)", "content": { "application/json": { "schema": { "type": "object" } } } }
        }
      }
    },
    "/bridge/deposit": {
      "post": {
        "summary": "Register external deposit to rToken",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/DepositReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/bridge/redeem": {
      "post": {
        "summary": "Request redeem from rToken to external chain",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/RedeemReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/bridge/verify": {
      "post": {
        "summary": "Verify bridge operation",
        "security": [{ "BridgeKey": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/VerifyReq" } } } },
        "responses": { "200": { "description": "BridgeResp", "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BridgeResp" } } } } }
      }
    },
    "/admin/set_balance": {
      "post": {
        "summary": "Set balance (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SetBalanceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/set_nonce": {
      "post": {
        "summary": "Set nonce (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/SetNonceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/bump_nonce": {
      "post": {
        "summary": "Bump nonce (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BumpNonceReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/mint": {
      "post": {
        "summary": "Add minted amount (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/MintReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    },
    "/admin/burn": {
      "post": {
        "summary": "Add burned amount (admin)",
        "security": [{ "AdminJWT": [] }],
        "requestBody": { "required": true, "content": { "application/json": { "schema": { "$ref": "#/components/schemas/BurnReq" } } } },
        "responses": { "200": { "description": "OK", "content": { "application/json": { "schema": { "type": "object" } } } } }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "AdminJWT": { "type": "apiKey"[REDACTED] "in": "header", "name": "X-Admin-JWT" },
      "BridgeKey": { "type": "apiKey"[REDACTED] "in": "header", "name": "X-Bridge-Key" }
    },
    "schemas": {
      "OkMsg": { "type": "object", "properties": { "status": { "type": "string" } }, "required": ["status"] },
      "Head":  { "type": "object", "properties": { "height": { "type": "integer", "format": "uint64" } }, "required": ["height"] },
      "Balance": {
        "type": "object",
        "properties": { "rid": { "type": "string" }, "balance": { "type": "string" }, "nonce": { "type": "integer", "format": "uint64" } },
        "required": ["rid","balance","nonce"]
      },
      "TxIn": {
        "type": "object",
        "properties": {
          "from": { "type": "string" }, "to": { "type": "string" },
          "amount": { "type": "integer", "format": "uint64" },
          "nonce": { "type": "integer", "format": "uint64" },
          "memo": { "type": "string", "nullable": true },
          "sig_hex": { "type": "string" }
        },
        "required": ["from","to","amount","nonce","sig_hex"]
      },
      "SubmitResult": {
        "type": "object",
        "properties": {
          "ok": { "type": "boolean" },
          "txid": { "type": "string", "nullable": true },
          "info": { "type": "string" }
        }, "required": ["ok","info"]
      },
      "Economy": {
        "type": "object",
        "properties": { "supply": { "type": "integer" }, "burned": { "type": "integer" }, "cap": { "type": "integer" } },
        "required": ["supply","burned","cap"]
      },
      "HistoryItem": {
        "type": "object",
        "properties": {
          "txid": { "type": "string" }, "height": { "type": "integer" }, "from": { "type": "string" },
          "to": { "type": "string" }, "amount": { "type": "integer" }, "nonce": { "type": "integer" }, "ts": { "type": "integer", "nullable": true }
        },
        "required": ["txid","height","from","to","amount","nonce"]
      },
      "DepositReq": {
        "type": "object",
        "properties": { "txid":{ "type": "string" }, "amount":{ "type": "integer" }, "from_chain":{ "type": "string" }, "to_rid":{ "type": "string" } },
        "required": ["txid","amount","from_chain","to_rid"]
      },
      "RedeemReq": {
        "type": "object",
        "properties": { "rtoken_tx":{ "type": "string" }, "to_chain":{ "type": "string" }, "to_addr":{ "type": "string" }, "amount":{ "type": "integer" } },
        "required": ["rtoken_tx","to_chain","to_addr","amount"]
      },
      "VerifyReq": {
        "type": "object",
        "properties": { "op_id":{ "type": "string" } }, "required": ["op_id"]
      },
      "BridgeResp": {
        "type": "object",
        "properties": { "ok":{ "type": "boolean" }, "op_id":{ "type": "string" }, "info":{ "type": "string" } },
        "required": ["ok","op_id","info"]
      },
      "SetBalanceReq": { "type": "object", "properties": { "rid":{"type":"string"}, "amount":{"type":"string"} }, "required": ["rid","amount"] },
      "SetNonceReq":   { "type": "object", "properties": { "rid":{"type":"string"}, "value":{"type":"integer"} }, "required": ["rid","value"] },
      "BumpNonceReq":  { "type": "object", "properties": { "rid":{"type":"string"} }, "required": ["rid"] },
      "MintReq":       { "type": "object", "properties": { "amount":{"type":"integer"} }, "required": ["amount"] },
      "BurnReq":       { "type": "object", "properties": { "amount":{"type":"integer"} }, "required": ["amount"] }
    }
  }
}
```

---

## 6) E2E плейбук: перевод LGN
1) Unlock -> seed/keys в sessionStorage
2) Draft TxIn: from/to/amount/nonce/memo
3) Подпись Ed25519 -> sig_hex
4) POST /node-api/submit_tx
5) Проверка /node-api/balance/{rid}
6) История: /node-api/history/{rid} (если есть)

---

## 7) Логи (tail)

### logos-node@a
```
-- No entries --
```

### journal tail
```
Jan 15 10:30:15 vm15330919.example.com sshd[1720334]: Failed password [REDACTED] invalid user admin from 46.73.73.211 port 48886 ssh2
Jan 15 10:30:15 vm15330919.example.com sshd[1720334]: Connection closed by invalid user admin 46.73.73.211 port 48886 [preauth]
Jan 15 10:30:18 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:30:18 vm15330919.example.com logos_readyz_check.sh[1720343]: readyz: 200
Jan 15 10:30:18 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:30:18 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:30:25 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=79.124.58.70 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=244 ID=7297 PROTO=TCP SPT=46165 DPT=14894 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:30:25 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:30:25 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:30:25 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:30:30 vm15330919.example.com systemd[1]: logos-sled-backup.service: Deactivated successfully.
Jan 15 10:30:30 vm15330919.example.com systemd[1]: Finished logos-sled-backup.service - Backup sled to /root/sled_backups.
Jan 15 10:30:30 vm15330919.example.com systemd[1]: logos-sled-backup.service: Consumed 19.902s CPU time.
Jan 15 10:30:44 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=11194 DPT=40534 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:30:58 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:30:58 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:30:58 vm15330919.example.com logos_readyz_check.sh[1720383]: readyz: 200
Jan 15 10:30:58 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:30:58 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:30:58 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:30:58 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:31:05 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=170.64.228.71 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=240 ID=18055 PROTO=TCP SPT=44631 DPT=37122 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:31:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:31:06.298Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 11 attempts: telegram: Unauthorized (401)"
Jan 15 10:31:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:31:06.311Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:31:21 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:31:21 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:31:21 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:31:24 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=26403 DPT=54560 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:31:49 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=52160 DPT=35417 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:32:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:32:06.300Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 11 attempts: telegram: Unauthorized (401)"
Jan 15 10:32:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:32:06.312Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:32:06 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:32:06 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:32:06 vm15330919.example.com logos_readyz_check.sh[1720429]: readyz: 200
Jan 15 10:32:06 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:32:06 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:32:06 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:32:06 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:32:10 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=79.124.40.110 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=244 ID=30474 PROTO=TCP SPT=55984 DPT=20088 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:32:21 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:32:21 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:32:21 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:32:27 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=2176 DPT=16794 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:32:48 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=216.180.246.75 DST=45.159.248.232 LEN=44 TOS=0x00 PREC=0x60 TTL=60 ID=38259 PROTO=TCP SPT=21615 DPT=8585 WINDOW=1025 RES=0x00 SYN URGP=0 
Jan 15 10:33:06 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=195.184.76.171 DST=45.159.248.232 LEN=60 TOS=0x00 PREC=0x00 TTL=52 ID=47323 DF PROTO=TCP SPT=33279 DPT=2137 WINDOW=5840 RES=0x00 SYN URGP=0 
Jan 15 10:33:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:33:06.300Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 12 attempts: telegram: Unauthorized (401)"
Jan 15 10:33:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:33:06.312Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:33:18 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:33:18 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:33:18 vm15330919.example.com logos_readyz_check.sh[1720473]: readyz: 200
Jan 15 10:33:18 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:33:18 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:33:18 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:33:18 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:33:19 vm15330919.example.com systemd[1]: fwupd.service: Deactivated successfully.
Jan 15 10:33:30 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=31204 DPT=2849 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:33:46 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=195.3.222.78 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x20 TTL=247 ID=54321 PROTO=TCP SPT=46282 DPT=8008 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:34:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:34:06.301Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 12 attempts: telegram: Unauthorized (401)"
Jan 15 10:34:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:34:06.314Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:34:09 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=194.180.49.73 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x20 TTL=247 ID=14106 PROTO=TCP SPT=40483 DPT=6452 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:34:22 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:34:22 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:34:22 vm15330919.example.com logos_readyz_check.sh[1720503]: readyz: 200
Jan 15 10:34:22 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:34:22 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:34:22 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:34:22 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:34:26 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=44170 DPT=15512 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:34:44 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=79.124.58.254 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=244 ID=33931 PROTO=TCP SPT=49519 DPT=54574 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:34:58 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:34:58 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:34:58 vm15330919.example.com logos_readyz_check.sh[1720527]: readyz: 200
Jan 15 10:34:58 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:34:58 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:34:58 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:34:58 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:35:01 vm15330919.example.com CRON[1720550]: pam_unix(cron:session): session opened for user root(uid=0) by root(uid=0)
Jan 15 10:35:01 vm15330919.example.com CRON[1720551]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)
Jan 15 10:35:01 vm15330919.example.com CRON[1720550]: pam_unix(cron:session): session closed for user root
Jan 15 10:35:05 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=91.230.168.188 DST=45.159.248.232 LEN=60 TOS=0x00 PREC=0x00 TTL=48 ID=64417 DF PROTO=TCP SPT=12913 DPT=3105 WINDOW=5840 RES=0x00 SYN URGP=0 
Jan 15 10:35:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:35:06.302Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 11 attempts: telegram: Unauthorized (401)"
Jan 15 10:35:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:35:06.314Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:35:23 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:35:23 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:35:23 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:35:29 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=194.180.49.73 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x20 TTL=247 ID=5152 PROTO=TCP SPT=40483 DPT=13824 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:35:38 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:35:38 vm15330919.example.com logos_readyz_check.sh[1720575]: readyz: 200
Jan 15 10:35:38 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:35:38 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:35:47 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=35.203.210.195 DST=45.159.248.232 LEN=44 TOS=0x00 PREC=0x60 TTL=251 ID=54321 PROTO=TCP SPT=54044 DPT=91 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:36:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:36:06.303Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 12 attempts: telegram: Unauthorized (401)"
Jan 15 10:36:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:36:06.315Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:36:07 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=23795 DPT=20754 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:36:23 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:36:23 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:36:23 vm15330919.example.com logos_readyz_check.sh[1720582]: readyz: 200
Jan 15 10:36:23 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:36:23 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:36:23 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:36:23 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:36:31 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=45.142.193.136 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x20 TTL=250 ID=58848 PROTO=TCP SPT=59918 DPT=29148 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:36:48 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:36:48 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:36:48 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:36:49 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=167.94.146.42 DST=45.159.248.232 LEN=60 TOS=0x00 PREC=0x00 TTL=58 ID=42570 PROTO=TCP SPT=16916 DPT=37894 WINDOW=42340 RES=0x00 SYN URGP=0 
Jan 15 10:37:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:37:06.304Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 12 attempts: telegram: Unauthorized (401)"
Jan 15 10:37:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:37:06.317Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:37:11 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=85.142.100.104 DST=45.159.248.232 LEN=52 TOS=0x00 PREC=0x00 TTL=57 ID=0 PROTO=TCP SPT=52367 DPT=39371 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:37:23 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:37:24 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:37:24 vm15330919.example.com logos_readyz_check.sh[1720626]: readyz: 200
Jan 15 10:37:24 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:37:24 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:37:24 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:37:24 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:37:25 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=87.120.191.13 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x20 TTL=249 ID=54321 PROTO=TCP SPT=38697 DPT=8728 WINDOW=65535 RES=0x00 SYN URGP=0 
Jan 15 10:37:47 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=79.124.58.70 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=244 ID=46698 PROTO=TCP SPT=46165 DPT=5002 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:37:58 vm15330919.example.com systemd[1]: Starting logos-healthcheck.service - LOGOS LRB /readyz healthcheck...
Jan 15 10:37:58 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:37:58 vm15330919.example.com logos_readyz_check.sh[1720651]: readyz: 200
Jan 15 10:37:58 vm15330919.example.com systemd[1]: logos-healthcheck.service: Deactivated successfully.
Jan 15 10:37:58 vm15330919.example.com systemd[1]: Finished logos-healthcheck.service - LOGOS LRB /readyz healthcheck.
Jan 15 10:37:58 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:37:58 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:38:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:38:06.305Z caller=dispatch.go:353 level=error component=dispatcher msg="Notify for alerts failed" num_alerts=3 err="telegram/telegram[0]: notify retry canceled after 11 attempts: telegram: Unauthorized (401)"
Jan 15 10:38:06 vm15330919.example.com alertmanager[820]: ts=2026-01-15T10:38:06.316Z caller=notify.go:848 level=warn component=dispatcher receiver=telegram integration=telegram[0] aggrGroup={}:{} msg="Notify attempt failed, will retry later" attempts=1 err="telegram: Unauthorized (401)"
Jan 15 10:38:06 vm15330919.example.com kernel: [UFW BLOCK] IN=ens3 OUT= MAC=52:54:00:c4:7b:44:f0:1c:2d:ac:0f:60:08:00 SRC=79.124.58.70 DST=45.159.248.232 LEN=40 TOS=0x00 PREC=0x00 TTL=244 ID=49344 PROTO=TCP SPT=46165 DPT=6381 WINDOW=1024 RES=0x00 SYN URGP=0 
Jan 15 10:38:24 vm15330919.example.com systemd[1]: Starting lrb-exporter.service - LRB textfile exporter (economy/head)...
Jan 15 10:38:24 vm15330919.example.com systemd[1]: lrb-exporter.service: Deactivated successfully.
Jan 15 10:38:24 vm15330919.example.com systemd[1]: Finished lrb-exporter.service - LRB textfile exporter (economy/head).
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: (Background on this error at: https://sqlalche.me/e/20/e3q8)
Jan 15 10:38:24 vm15330919.example.com python[1620726]: scanner error: (sqlite3.OperationalError) no such table: kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [SQL: SELECT kv.k AS kv_k, kv.v AS kv_v
Jan 15 10:38:24 vm15330919.example.com python[1620726]: FROM kv
Jan 15 10:38:24 vm15330919.example.com python[1620726]: WHERE kv.k = ?]
Jan 15 10:38:24 vm15330919.example.com python[1620726]: [parameters: ('last_scanned_block',)]
```

---

## 8) Release discipline
- Снапшот: wallet_prod__v555_* (rsync 1:1)
- Новая версия: wallet_prod__vNNN_*
- Переключение: nginx root/alias или симлинк
- Откат: вернуть root/alias на предыдущую папку + reload nginx

