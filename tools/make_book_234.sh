#!/usr/bin/env bash
set -euo pipefail

OUTDIR="docs/234"
OUT="${OUTDIR}/BOOK_234.md"
mkdir -p "$OUTDIR"
: > "$OUT"

title(){ echo -e "\n# $1\n" >> "$OUT"; }
sub(){ echo -e "\n## $1\n" >> "$OUT"; }

add_file(){
  local path="$1"
  local label="$2"
  sub "$label"
  echo "**Path:** \`$path\`" >> "$OUT"
  echo "" >> "$OUT"
  if [ ! -f "$path" ]; then
    echo "_NOT FOUND_" >> "$OUT"
    return
  fi
  echo '```' >> "$OUT"
  sed -n '1,9000p' "$path" >> "$OUT"
  echo '```' >> "$OUT"
}

add_cmd(){
  local label="$1"; shift
  sub "$label"
  echo '```bash' >> "$OUT"
  echo "$*" >> "$OUT"
  echo '```' >> "$OUT"
  echo "" >> "$OUT"
  echo '```' >> "$OUT"
  bash -lc "$*" >> "$OUT" 2>&1
  echo '```' >> "$OUT"
}

echo "# BOOK_234 — wallet-proxy: address-book + storage + scanner" >> "$OUT"
echo "" >> "$OUT"
echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT"
echo "- Scope: /opt/logos/wallet-proxy" >> "$OUT"
echo "" >> "$OUT"

title "1) Address-book (RID → addresses)"
add_file "/opt/logos/wallet-proxy/app.py" "app.py (receive + derivation + balances)"

title "2) Storage (SQLite)"
add_file "/opt/logos/wallet-proxy/init_db.py" "init_db.py"
add_cmd "DB tables + counts" 'cd /opt/logos/wallet-proxy || exit 1; for db in wproxy.db wallet_proxy.db; do echo "=== $db ==="; sqlite3 "$db" ".tables"; sqlite3 "$db" "select count(*) from deposit_map;" || true; sqlite3 "$db" "select count(*) from seen_tx;" || true; done'
add_cmd "DB schema (wproxy.db)" 'cd /opt/logos/wallet-proxy || exit 1; sqlite3 wproxy.db ".schema"'

title "3) Scanner"
add_file "/opt/logos/wallet-proxy/scanner.py" "scanner.py (scan deposits + SeenTx + bridge notify)"

echo -e "\n---\nEND\n" >> "$OUT"
echo "OK: wrote $OUT"
wc -l "$OUT"
