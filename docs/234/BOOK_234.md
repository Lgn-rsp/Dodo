# BOOK_234 — wallet-proxy: address-book + storage + scanner

- Generated: 2026-01-16T08:00:03Z
- Scope: /opt/logos/wallet-proxy (prod files), sanitized


# 1) Address-book (RID → addresses)


## wallet-proxy app.py (derivation + /v1/receive)

**Path:** `/opt/logos/wallet-proxy/app.py`

```
```

# 2) Storage layer (DepositMap / SeenTx / sqlite)


## init_db.py (db init helper)

**Path:** `/opt/logos/wallet-proxy/init_db.py`

```
```

## SQLite tables + counts (wproxy.db / wallet_proxy.db)

```bash
cd /opt/logos/wallet-proxy || exit 1; for db in wproxy.db wallet_proxy.db; do echo "=== $db ==="; sqlite3 "$db" ".tables"; sqlite3 "$db" "select count(*) as depositmap_cnt from deposit_map;" || true; sqlite3 "$db" "select count(*) as seentx_cnt from seen_tx;" || true; done
```

```
```

## Schema (head 200, wproxy.db)

```bash
cd /opt/logos/wallet-proxy || exit 1; sqlite3 wproxy.db ".schema" | head -n 200
```

```
```

# 3) Watcher / Scanner (deposit scan → SeenTx → bridge notify)


## scanner.py (scan + idempotency + bridge call)

**Path:** `/opt/logos/wallet-proxy/scanner.py`

```
```

---
END

