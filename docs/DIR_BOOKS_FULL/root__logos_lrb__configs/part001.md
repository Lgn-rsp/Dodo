# LOGOS — Directory Book: /root/logos_lrb/configs

_Generated: 2025-12-31T06:43:51Z_

**Part:** 1

---

## STRUCTURE

```text
/root/logos_lrb/configs
/root/logos_lrb/configs/env
```

---

## FILES (FULL SOURCE)


### FILE: /root/logos_lrb/configs/genesis.yaml

```

```

### FILE: /root/logos_lrb/configs/keys.env.example

```
# LOGOS node (пример ENV)
LRB_DATA_PATH=/var/lib/logos/data.sled
LRB_NODE_KEY_PATH=/var/lib/logos/node_key
LRB_SLOT_MS=500
LRB_MAX_BLOCK_TX=10000
LRB_MEMPOOL_CAP=100000
LRB_MAX_AMOUNT=18446744073709551615
LRB_BRIDGE_MAX_PER_TX=10000000

# Секреты — задаются ТОЛЬКО вне репозитория:
# LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
# LRB_BRIDGE_KEY=CHANGE_ME
# LRB_ADMIN_JWT_SECRET=<optional>

```

### FILE: /root/logos_lrb/configs/logos_config.yaml

```

```

### FILE: /root/logos_lrb/configs/proxy.env.example

```
# Wallet Proxy / Scanner (пример ENV)
# !!! НЕ коммить настоящие ключи/приватники !!!
ETH_PROVIDER_URL=https://mainnet.infura.io/v3/XXXX...
USDT_CONTRACT=0xdAC17F958D2ee523a2206206994597C13D831ec7

# hot-кошелёк оператора (для withdraw/fee)
HOT_WALLET_ADDRESS=0x...
HOT_WALLET_PRIVATE_KEY= # НЕ класть в git, подставлять только в прод окружении

```

### FILE: /root/logos_lrb/configs/env/node-a.env.example

```
LRB_NODE_SK_HEX=CHANGE_ME_64_HEX
LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
LRB_BRIDGE_KEY=CHANGE_ME
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8080
LRB_DATA_DIR=/var/lib/logos-a
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=127.0.0.1/32,::1/128

```

### FILE: /root/logos_lrb/configs/env/node-b.env.example

```
LRB_NODE_SK_HEX=CHANGE_ME_64_HEX
LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
LRB_BRIDGE_KEY=CHANGE_ME
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8082
LRB_DATA_DIR=/var/lib/logos-b
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=127.0.0.1/32,::1/128

```

### FILE: /root/logos_lrb/configs/env/node-c.env.example

```
LRB_NODE_SK_HEX=CHANGE_ME_64_HEX
LRB_ADMIN_KEY=CHANGE_ADMIN_KEY
LRB_BRIDGE_KEY=CHANGE_ME
LRB_WALLET_ORIGIN=https://45-159-248-232.sslip.io
LRB_NODE_LISTEN=0.0.0.0:8084
LRB_DATA_DIR=/var/lib/logos-c
RUST_LOG=info
LRB_RATE_BYPASS_CIDR=127.0.0.1/32,::1/128

```

### FILE: /root/logos_lrb/configs/env/node.env.example

```
# ========= LOGOS LRB — canonical node env (prod-ready) =========
# Этот файл — пример. Для прод-ноды скопировать в /etc/logos/keys.env (права 600, владелец logos:logos)

######################
# Узел / слушатель
######################
LRB_NODE_LISTEN=0.0.0.0:8080          # HTTP API
RUST_LOG=info,hyper=warn,tower_http=warn

######################
# Ключи/секреты (заменить!)
######################
LRB_NODE_SK_HEX=CHANGE_ME_64_HEX      # если используется на уровне модулей
LRB_JWT_SECRET=CHANGE_ME              # если admin/JWT задействован
LRB_BRIDGE_KEY=CHANGE_ME              # общий секрет для X-Bridge-Key и HMAC

######################
# Хранилище / данные
######################
LRB_DATA_DIR=/var/lib/logos           # каталог данных ноды (sled и др.)
# sled будет в: $LRB_DATA_DIR/data.sled

######################
# Архив (Postgres) — рекомендуется
######################
# Пример: postgres://logos:strongpass@127.0.0.1:5432/logos?sslmode=disable
LRB_ARCHIVE_URL=postgres://logos:strongpass@127.0.0.1:5432/logos?sslmode=disable

######################
# Мост (rToken) — внешний payout
######################
BRIDGE_PAYOUT_URL=https://bridge.example.com
BRIDGE_PAYOUT_PATH=/api/payout
# LRB_BRIDGE_KEY — уже выше, используется и как HMAC-ключ

######################
# Периметр / phase-mixing
######################
PHASE_JITTER_ENABLE=true              # включить джиттер 0–7мс на submit/stake/bridge путях

######################
# Продюсер/слоты/комиссии (при необходимости)
######################
SLOT_MS=200                            # длительность слота, если используется из env
FEE_MIN=0                              # минимальная комиссия (если включишь в бизнес-логике)

######################
# Параметры rate-limit (если оборачиваешь на периметре)
######################
LRB_QPS=30                             # базовый лимит QPS
LRB_BURST=60                           # burst
LRB_RATE_BYPASS_CIDRS=127.0.0.1/32,::1/128

######################
# CORS/Origins (кошелёк/веб)
######################
LRB_WALLET_ORIGIN=http://localhost     # добавь свои origin'ы на фронт

```
