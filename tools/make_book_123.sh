#!/usr/bin/env bash
set -euo pipefail

OUTDIR="docs/123"
OUT="${OUTDIR}/BOOK_123.md"
mkdir -p "$OUTDIR"

# --------- где искать 3 нужных блока ----------
WALLET_PROD_DIRS=(
  "/opt/logos/www/wallet_prod"
  "/opt/logos/www/wallet-prod"
  "/opt/logos/www/wallet"
  "/var/www/html/wallet_prod"
)

WALLET_PROXY_DIRS=(
  "/opt/logos/wallet-proxy"
  "/opt/logos/wallet_proxy"
  "/opt/logos/wallet-proxy-api"
  "/opt/logos/wallet_api"
)

NGINX_VHOST_GLOBS=(
  "/etc/nginx/sites-enabled/*mw-expedition*"
  "/etc/nginx/sites-available/*mw-expedition*"
  "/etc/nginx/conf.d/*mw-expedition*"
)

# ---------- утилиты ----------
have() { command -v "$1" >/dev/null 2>&1; }

pick_first_dir() {
  local d
  for d in "$@"; do
    if [[ -d "$d" ]]; then
      echo "$d"
      return 0
    fi
  done
  return 1
}

# Санитайзер: режем токены/ключи/пароли/seed/mnemonic/RPC keys/Authorization и т.п.
sanitize_to_tmp() {
  local src="$1"
  local tmp="$2"

  python3 - <<'PY' "$src" "$tmp"
import re, sys, pathlib

src = pathlib.Path(sys.argv[1])
tmp = pathlib.Path(sys.argv[2])

text = src.read_text(errors="ignore")

# 1) KEY=VALUE / "key": "value" / key: value  -> value => ***
key_pat = re.compile(r'(?im)^(\s*(?:[A-Z0-9_]*?(?:SECRET|TOKEN|API[_-]?KEY|PRIVATE|PRIVKEY|PASSWORD|PASSWD|MNEMONIC|SEED|BEARER|AUTHORIZATION|RPC|INFURA|ALCHEMY|MORALIS|QUICKNODE|ANKR|TRONGRID|HOTWALLET|HOT_WALLET)[A-Z0-9_]*?)\s*[:=]\s*)(.+?)\s*$')
text = key_pat.sub(lambda m: m.group(1) + "***", text)

# 2) Authorization: Bearer xxxx
text = re.sub(r'(?im)^(authorization\s*:\s*bearer\s+)(.+)$', r'\1***', text)

# 3) URL credentials / query tokens
text = re.sub(r'(?i)([?&](?:token|apikey|api_key|key|secret|sig|signature)=)([^&\s]+)', r'\1***', text)

# 4) long hex strings that look like private keys / secrets
text = re.sub(r'\b[a-f0-9]{64,}\b', '***', text, flags=re.I)

# 5) JWT-like tokens
text = re.sub(r'\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9._-]{10,}\.[a-zA-Z0-9._-]{10,}\b', '***', text)

tmp.write_text(text)
PY
}

append_file() {
  local src="$1"
  if [[ ! -f "$src" ]]; then
    return 0
  fi

  local tmp
  tmp="$(mktemp)"
  sanitize_to_tmp "$src" "$tmp"

  {
    echo
    echo "## FILE: \`$src\`"
    echo
    echo '```'
    cat "$tmp"
    echo
    echo '```'
    echo
  } >> "$OUT"

  rm -f "$tmp"
}

append_glob_files() {
  local g
  for g in "$@"; do
    # shellcheck disable=SC2086
    for f in $g; do
      [[ -f "$f" ]] && append_file "$f"
    done
  done
}

# ---------- сборка ----------
echo "# BOOK 123 — wallet_prod + wallet-proxy + nginx vhost (sanitized)" > "$OUT"
echo >> "$OUT"
echo "Собрано: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT"
echo >> "$OUT"
echo "Секреты/ключи/токены автоматически заменены на: \`***\`" >> "$OUT"
echo >> "$OUT"
echo "---" >> "$OUT"

# 1) wallet_prod: app.html, app.js, lgn_send.js (или где он вшит)
WPD="$(pick_first_dir "${WALLET_PROD_DIRS[@]}" || true)"
if [[ -n "${WPD:-}" ]]; then
  echo >> "$OUT"; echo "# wallet_prod" >> "$OUT"; echo >> "$OUT"
  append_file "${WPD}/app.html"
  append_file "${WPD}/app.js"

  # lgn_send.js может лежать по-разному — найдём
  LGN_SEND="$(find "$WPD" -maxdepth 4 -type f \( -name "lgn_send.js" -o -name "*lgn*send*.js" \) 2>/dev/null | head -n 1 || true)"
  if [[ -n "${LGN_SEND:-}" ]]; then
    append_file "$LGN_SEND"
  else
    echo >> "$OUT"
    echo "## NOTE: lgn_send.js не найден в $WPD (искал до глубины 4)" >> "$OUT"
    echo >> "$OUT"
  fi
else
  echo >> "$OUT"
  echo "# wallet_prod" >> "$OUT"
  echo >> "$OUT"
  echo "NOTE: wallet_prod папка не найдена в стандартных путях." >> "$OUT"
  echo >> "$OUT"
fi

# 2) wallet-proxy: app.py (главный файл)
WPR="$(pick_first_dir "${WALLET_PROXY_DIRS[@]}" || true)"
if [[ -n "${WPR:-}" ]]; then
  echo >> "$OUT"; echo "# wallet-proxy" >> "$OUT"; echo >> "$OUT"
  # пробуем явно app.py / main.py
  if [[ -f "${WPR}/app.py" ]]; then
    append_file "${WPR}/app.py"
  elif [[ -f "${WPR}/main.py" ]]; then
    append_file "${WPR}/main.py"
  else
    # если неизвестно имя — берём первые 2 python файла верхнего уровня
    while IFS= read -r f; do append_file "$f"; done < <(find "$WPR" -maxdepth 2 -type f -name "*.py" 2>/dev/null | head -n 2)
  fi

  # если есть конфиги/env рядом — добавим (санитайзится)
  while IFS= read -r f; do append_file "$f"; done < <(find "$WPR" -maxdepth 2 -type f \( -name ".env" -o -name "*.env" -o -name "*.ini" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) 2>/dev/null | head -n 20)
else
  echo >> "$OUT"
  echo "# wallet-proxy" >> "$OUT"
  echo >> "$OUT"
  echo "NOTE: wallet-proxy папка не найдена в стандартных путях." >> "$OUT"
  echo >> "$OUT"
fi

# 3) nginx vhost mw-expedition (где /api и /wallet-api проксируются)
echo >> "$OUT"; echo "# nginx vhost (mw-expedition)" >> "$OUT"; echo >> "$OUT"
append_glob_files "${NGINX_VHOST_GLOBS[@]}"

# Готово
echo >> "$OUT"
echo "---" >> "$OUT"
echo "END OF BOOK 123" >> "$OUT"

echo "OK: wrote $OUT"
