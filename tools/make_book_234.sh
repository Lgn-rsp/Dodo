#!/usr/bin/env bash
set -euo pipefail

OUTDIR="docs/234"
OUT="${OUTDIR}/BOOK_234.md"
mkdir -p "$OUTDIR"
: > "$OUT"

add_title () { echo -e "\n# $1\n" >> "$OUT"; }
add_sub ()   { echo -e "\n## $1\n" >> "$OUT"; }

sanitize_stream () {
  python3 - <<'PY'
import sys, re
s = sys.stdin.read()

# mask common secrets in assignments and env-like lines
def mask_assign(name):
  return re.sub(
    rf'(?i)\b({name})\b\s*=\s*([\'"]).*?\2',
    lambda m: f"{m.group(1)} = '***'",
    s
  )

# direct keys/tokens
for key in [
  "ETH_HOT_WALLET_PK","HOT_PK","BRIDGE_KEY","LRB_BRIDGE_KEY",
  "API_KEY","APIKEY","TOKEN","SECRET","PASSWORD","PASSWD",
  "MNEMONIC","SEED","PRIVATE_KEY","PRIVKEY"
]:
  s = re.sub(rf'(?i)\b({re.escape(key)})\b\s*=\s*([\'"]).*?\2', lambda m: f"{m.group(1)} = '***'", s)

# provider/rpc urls
for key in ["ETH_PROVIDER_URL","ETH_RPC","RPC_URL","PROVIDER_URL","ALCHEMY","INFURA","QUICKNODE","ANKR","MORALIS","TRONGRID"]:
  s = re.sub(rf'(?i)\b({re.escape(key)})\b\s*=\s*([\'"]).*?\2', lambda m: f"{m.group(1)} = '***'", s)

# xpubs
for key in ["BTC_XPUB","ETH_XPUB","TRON_XPUB"]:
  s = re.sub(rf'(?i)\b({re.escape(key)})\b\s*=\s*([\'"]).*?\2', lambda m: f"{m.group(1)} = '***'", s)

# Bearer tokens
s = re.sub(r'(?i)(Authorization:\s*Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*', r'\1***', s)
s = re.sub(r'(?i)("Authorization"\s*:\s*"Bearer\s+)[^"]+(")', r'\1***\2', s)

# 0x 64 hex
s = re.sub(r'0x[a-fA-F0-9]{64}', '0x***', s)

# env KEY=VALUE masking
def env_mask(m):
  k = m.group(1); v = m.group(2)
  if re.search(r'(?i)(token|secret|password|passwd|mnemonic|seed|priv|key|rpc|provider|xpub)', k):
    return f"{k}=***"
  return f"{k}={v}"
s = re.sub(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', env_mask, s, flags=re.M)

sys.stdout.write(s)
PY
}

add_file () {
  local path="$1"
  local label="$2"
  add_sub "$label"
  echo "**Path:** \`$path\`" >> "$OUT"
  echo "" >> "$OUT"
  if [ ! -f "$path" ]; then
    echo "_NOT FOUND: ${path}_" >> "$OUT"
    return
  fi
  echo '```' >> "$OUT"
  cat "$path" | sanitize_stream >> "$OUT"
  echo '```' >> "$OUT"
}

add_cmd () {
  local label="$1"; shift
  add_sub "$label"
  echo '```bash' >> "$OUT"
  echo "$*" >> "$OUT"
  echo '```' >> "$OUT"
  echo "" >> "$OUT"
  echo '```' >> "$OUT"
  bash -lc "$*" 2>/dev/null | head -n 200 | sanitize_stream >> "$OUT"
  echo '```' >> "$OUT"
}

echo "# BOOK_234 — wallet-proxy: address-book + storage + scanner" >> "$OUT"
echo "" >> "$OUT"
echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT"
echo "- Scope: /opt/logos/wallet-proxy (prod files), sanitized" >> "$OUT"
echo "" >> "$OUT"

add_title "1) Address-book (RID → addresses)"
add_file "/opt/logos/wallet-proxy/app.py" "wallet-proxy app.py (derivation + /v1/receive)"

add_title "2) Storage layer (DepositMap / SeenTx / sqlite)"
add_file "/opt/logos/wallet-proxy/init_db.py" "init_db.py (db init helper)"
add_cmd "SQLite tables + counts (wproxy.db / wallet_proxy.db)" \
'cd /opt/logos/wallet-proxy || exit 1; for db in wproxy.db wallet_proxy.db; do echo "=== $db ==="; sqlite3 "$db" ".tables"; sqlite3 "$db" "select count(*) as depositmap_cnt from deposit_map;" || true; sqlite3 "$db" "select count(*) as seentx_cnt from seen_tx;" || true; done'
add_cmd "Schema (head 200, wproxy.db)" \
'cd /opt/logos/wallet-proxy || exit 1; sqlite3 wproxy.db ".schema" | head -n 200'

add_title "3) Watcher / Scanner (deposit scan → SeenTx → bridge notify)"
add_file "/opt/logos/wallet-proxy/scanner.py" "scanner.py (scan + idempotency + bridge call)"

echo -e "\n---\nEND\n" >> "$OUT"
echo "OK: wrote $OUT"
ls -lah "$OUTDIR" | sed -n '1,50p'
