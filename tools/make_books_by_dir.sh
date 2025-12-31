#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="docs/BOOKS_BY_DIR"
mkdir -p "$OUT_DIR"

# какие папки считаем "книгами"
BOOK_DIRS=(
  "/root/logos_lrb/src"
  "/root/logos_lrb/lrb_core/src"
  "/root/logos_lrb/node/src"
  "/root/logos_lrb/modules"
  "/root/logos_lrb/tools"
  "/root/logos_lrb/scripts"
  "/root/logos_lrb/infra"
  "/root/logos_lrb/configs"

  "/opt/logos/airdrop-api"
  "/opt/logos/airdrop-tg-bot"
  "/opt/logos/wallet-proxy"
  "/opt/logos/www"

  "/var/www/logos"

  "/etc/logos"
)

MAX_BYTES=$((25*1024*1024)) # 25MB на файл (чтобы не тащить старые мегакниги)

ALLOW_EXT_REGEX='\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$'
SKIP_NAME_REGEX='(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)'
SKIP_DIR_REGEX='/(\.git|target|node_modules|venv|\.venv|__pycache__|backups|snapshots|data\.sled\.bak)(/|$)'

safe_name() { echo "$1" | sed 's|/|_|g' | sed 's|^_||'; }

etc_allow() {
  # разрешаем только "публичное" из /etc/logos
  local f="$1"
  local b; b="$(basename "$f")"
  [[ "$b" == "genesis.yaml" ]] && return 0
  [[ "$b" =~ \.example$ ]] && return 0
  [[ "$b" =~ \.sample$ ]] && return 0
  [[ "$b" =~ \.yaml$ ]] && return 0
  [[ "$b" =~ \.yml$ ]] && return 0
  [[ "$b" =~ \.conf$ ]] && return 0
  [[ "$b" =~ \.service$ ]] && return 0
  return 1
}

emit_file() {
  local f="$1" out="$2"
  local sz; sz=$(stat -c%s "$f" 2>/dev/null || echo 0)

  # /etc/logos — только публичное
  if [[ "$f" == /etc/logos/* ]]; then
    etc_allow "$f" || { echo -e "\n### FILE: $f\n\`\`\`\n[REDACTED / SKIPPED]\n\`\`\`" >> "$out"; return 0; }
  fi

  if (( sz > MAX_BYTES )); then
    echo -e "\n### FILE: $f\n\`\`\`\n[SKIPPED: too large ($sz bytes)]\n\`\`\`" >> "$out"
    return 0
  fi

  echo -e "\n### FILE: $f\n\`\`\`" >> "$out"
  sed 's/\t/  /g' "$f" >> "$out" || true
  echo -e "\n\`\`\`" >> "$out"
}

make_book() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0

  local out="$OUT_DIR/BOOK_$(safe_name "$dir").md"
  echo "# LOGOS — Directory Book" > "$out"
  echo "" >> "$out"
  echo "## ROOT: $dir" >> "$out"

  echo -e "\n---\n## STRUCTURE\n\`\`\`" >> "$out"
  find "$dir" -type d \
    ! -path '*/.git*' \
    ! -path '*/target*' \
    ! -path '*/node_modules*' \
    ! -path '*/venv*' \
    ! -path '*/.venv*' \
    ! -path '*/__pycache__*' \
    ! -path '*/backups*' \
    ! -path '*/snapshots*' \
    ! -path '*data.sled.bak*' \
    | sort >> "$out"
  echo -e "\`\`\`" >> "$out"

  echo -e "\n---\n## FILES (FULL SOURCE)\n" >> "$out"

  while IFS= read -r f; do
    emit_file "$f" "$out"
  done < <(
    find "$dir" -type f \
      ! -path '*/target/*' \
      ! -path '*/node_modules/*' \
      ! -path '*/venv/*' \
      ! -path '*/.venv/*' \
      ! -path '*/.git/*' \
      | grep -E "$ALLOW_EXT_REGEX" \
      | grep -Ev "$SKIP_NAME_REGEX" \
      | grep -Ev "$SKIP_DIR_REGEX" \
      | sort
  )

  echo "✅ BOOK: $out"
}

# индекс
INDEX="$OUT_DIR/00_INDEX.md"
echo "# LOGOS — Books by Directory" > "$INDEX"
echo "" >> "$INDEX"
echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$INDEX"
echo "" >> "$INDEX"

for d in "${BOOK_DIRS[@]}"; do
  make_book "$d"
  bn="BOOK_$(safe_name "$d").md"
  [[ -f "$OUT_DIR/$bn" ]] && echo "- [$d]($bn)" >> "$INDEX"
done

echo "DONE: $OUT_DIR"
