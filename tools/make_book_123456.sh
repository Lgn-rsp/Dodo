#!/usr/bin/env bash
set -euo pipefail

OUTDIR="docs/123456"
PREFIX="BOOK_123456"
PART_LIMIT=$((20*1024*1024)) # 20MB
mkdir -p "$OUTDIR"
rm -f "$OUTDIR/${PREFIX}_part"*.md "$OUTDIR/00_INDEX.md"

part=1
cur="$OUTDIR/${PREFIX}_part$(printf "%03d" "$part").md"

new_part() {
  part=$((part+1))
  cur="$OUTDIR/${PREFIX}_part$(printf "%03d" "$part").md"
}

cur_size() { [ -f "$cur" ] && wc -c < "$cur" || echo 0; }

append_raw() {
  local s="$1"
  local sz add
  sz="$(cur_size)"
  add="$(printf "%s" "$s" | wc -c)"
  if [ $((sz+add)) -ge "$PART_LIMIT" ]; then new_part; fi
  printf "%s" "$s" >> "$cur"
}

append_title()   { append_raw "\n# $1\n"; }
append_section() { append_raw "\n## $1\n"; }
append_block() {
  local t="$1" body="$2"
  append_section "$t"
  append_raw "\n\`\`\`\n${body}\n\`\`\`\n"
}

sanitize_stream() {
  # Санитайзит секреты в env/логах: оставляет ключи, режет значения
  sed -E \
    -e 's/^([A-Za-z0-9_]*(SECRET|TOKEN|API[_-]?KEY|PRIVATE|PRIVKEY|PASSWORD|PASSWD|MNEMONIC|SEED|BEARER|RPC|INFURA|ALCHEMY|MORALIS|QUICKNODE|ANKR|TRONGRID|HOTWALLET|HOT_WALLET|XPRV|XSEED)[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*).*/\1***/I' \
    -e 's/^(Authorization:[[:space:]]*Bearer[[:space:]]*).*/\1***/I'
}

add_file() {
  local f="$1"
  if [ ! -f "$f" ]; then
    append_block "MISSING FILE: $f" "NOT FOUND"
    return 0
  fi
  case "$f" in
    *.png|*.jpg|*.jpeg|*.webp|*.gif|*.pdf|*.zip|*.gz|*.7z|*.tar|*.tar.gz|*.tar.xz|*.db|*.sqlite|*.sqlite3|*.bin)
      append_block "SKIPPED BINARY: $f" "binary skipped"
      return 0
      ;;
  esac

  append_raw "\n### FILE: $f\n\n\`\`\`\n"
  if [[ "$f" == /etc/logos/* ]] || [[ "$f" == *error.log ]] || [[ "$f" == *access.log ]]; then
    sanitize_stream < "$f" >> "$cur"
  else
    cat "$f" >> "$cur"
  fi
  append_raw "\n\`\`\`\n"
}

# ------------------ START ------------------
append_title "BOOK 123456 — wallet(front) + wallet-proxy + nginx + systemd + env(sanitized) + logs"
append_block "Generated (UTC)" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# A) FRONT: wallet_prod OR wallet_dev OR wallet OR var/www wallet
append_section "A) Front (wallet_prod/wallet_dev) — LGN send"

FRONT_CANDIDATES=(
  "/opt/logos/www/wallet_prod"
  "/opt/logos/www/wallet_dev"
  "/opt/logos/www/wallet"
  "/var/www/logos/wallet"
  "/var/www/logos/wallet3"
)

FOUND_FRONT=""
for d in "${FRONT_CANDIDATES[@]}"; do
  if [ -d "$d" ]; then FOUND_FRONT="$d"; break; fi
done
append_block "Detected front root" "${FOUND_FRONT:-NOT FOUND}"

if [ -n "$FOUND_FRONT" ]; then
  append_block "TREE (maxdepth 3)" "$(find "$FOUND_FRONT" -maxdepth 3 -type f | sed "s|^$FOUND_FRONT/||" | sort | head -n 5000)"

  for f in \
    "$FOUND_FRONT/app.html" \
    "$FOUND_FRONT/app.js" \
    "$FOUND_FRONT/index.html" \
    "$FOUND_FRONT/auth.html" \
    "$FOUND_FRONT/auth.js" \
    "$FOUND_FRONT/auth.css" \
    "$FOUND_FRONT/tx_redirect.js" \
    "$FOUND_FRONT/modules/lgn_send.js"
  do
    add_file "$f"
  done

  if [ -d "$FOUND_FRONT/modules" ]; then
    append_section "modules/ (ALL FILES)"
    while IFS= read -r f; do
      add_file "$f"
    done < <(find "$FOUND_FRONT/modules" -type f \
        ! -name "*.map" \
        ! -name "*.min.js" \
        ! -name "*.png" ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.webp" ! -name "*.gif" \
        | sort)
  fi
fi

# B) WALLET-PROXY
append_section "B) wallet-proxy (FastAPI) — topup/withdraw/watchers/addressbook"

PROXY_ROOT="/opt/logos/wallet-proxy"
append_block "Proxy root" "$PROXY_ROOT"
if [ -d "$PROXY_ROOT" ]; then
  append_block "TREE (maxdepth 4)" "$(find "$PROXY_ROOT" -maxdepth 4 -type f | sed "s|^$PROXY_ROOT/||" | sort | head -n 8000)"
  while IFS= read -r f; do
    add_file "$f"
  done < <(find "$PROXY_ROOT" -type f \
      \( -name "*.py" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" -o -name "*.ini" -o -name "*.conf" -o -name "*.md" -o -name "*.txt" -o -name "*.json" -o -name "*.sh" -o -name "requirements*.txt" \) \
      ! -path "*/venv/*" ! -path "*/.venv/*" ! -path "*/__pycache__/*" \
      | sort)
else
  append_block "wallet-proxy" "NOT FOUND"
fi

# C) NGINX: vhost mw-expedition
append_section "C) Nginx vhost (mw-expedition.com) — routing /api and /wallet-api"

VHOSTS=()
for p in /etc/nginx/sites-enabled/* /etc/nginx/sites-available/*; do
  [ -f "$p" ] || continue
  if grep -q "mw-expedition.com" "$p"; then VHOSTS+=("$p"); fi
done

if [ ${#VHOSTS[@]} -eq 0 ]; then
  append_block "VHOST files" "NOT FOUND (no files containing mw-expedition.com)"
else
  append_block "VHOST files" "$(printf "%s\n" "${VHOSTS[@]}")"
  for f in "${VHOSTS[@]}"; do add_file "$f"; done
fi

append_block "nginx -T snippet (mw-expedition.com)" "$(nginx -T 2>/dev/null | sed -n '/mw-expedition\.com/,+260p' | head -n 1200)"

# D) SYSTEMD + ENV
append_section "D) systemd units + ENV (sanitized)"

UNITS=(
  "logos-wallet-proxy.service"
  "lrb-proxy.service"
  "lrb-scanner.service"
  "logos-node@main.service"
  "logos-node.service"
  "logos_wallet_api.service"
  "logos_node_backend.service"
)

for u in "${UNITS[@]}"; do
  append_block "systemctl cat $u" "$(systemctl cat "$u" --no-pager 2>/dev/null || echo "NOT FOUND")"
  append_block "systemctl show $u (ExecStart/WD/EnvFiles)" "$(systemctl show "$u" -p WorkingDirectory -p ExecStart -p EnvironmentFiles --no-pager 2>/dev/null || echo "NOT FOUND")"
done

ENV_FILES=(
  "/etc/logos/wallet-proxy.env"
  "/etc/logos/proxy.env"
  "/etc/logos/node-main.env"
  "/etc/logos/keys.env"
)

for f in "${ENV_FILES[@]}"; do add_file "$f"; done

# E) LOGS
append_section "E) Logs (sanitized) — last 300 lines"

for u in "${UNITS[@]}"; do
  append_block "journalctl -u $u -n 300" "$(journalctl -u "$u" -n 300 --no-pager 2>/dev/null | sanitize_stream || true)"
done

for lf in /var/log/nginx/error.log /var/log/nginx/access.log; do
  if [ -f "$lf" ]; then
    append_block "tail -n 400 $lf" "$(tail -n 400 "$lf" | sanitize_stream)"
  fi
done

# INDEX
{
  echo "# 00_INDEX — BOOK 123456"
  echo ""
  echo "Parts:"
  ls -1 "$OUTDIR"/${PREFIX}_part*.md 2>/dev/null | sed 's|^| - |'
  echo ""
  echo "Front root: ${FOUND_FRONT:-NOT FOUND}"
  echo "Proxy root: $PROXY_ROOT"
  echo ""
} > "$OUTDIR/00_INDEX.md"

echo "✅ DONE: $OUTDIR"
ls -lah "$OUTDIR" | sed -n '1,120p'
