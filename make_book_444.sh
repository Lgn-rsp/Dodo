#!/usr/bin/env bash
set -euo pipefail

ARCHIVE="${1:?Usage: ./make_book_444.sh /path/to/logos_wallet_pack_*.tar.gz}"
BOOK="BOOK_444.md"
WORK=".work_book_444"

rm -rf "$WORK"
mkdir -p "$WORK"
tar -xzf "$ARCHIVE" -C "$WORK"

PACK_DIR="$(find "$WORK" -maxdepth 1 -type d -name 'logos_wallet_pack_*' | head -n 1)"
if [[ -z "${PACK_DIR}" ]]; then
  echo "ERR: pack dir not found after extract"
  exit 1
fi

WPROD="$PACK_DIR/wallet_prod"
WDEV="$PACK_DIR/wallet_dev"
WPREM="$PACK_DIR/wallet_premium"
NG="$PACK_DIR/nginx"
SD="$PACK_DIR/systemd"
OA="$PACK_DIR/openapi"
LG="$PACK_DIR/logs"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

head_safe() { local f="$1"; local n="${2:-200}"; [[ -f "$f" ]] && sed -n "1,${n}p" "$f" || true; }

redact() {
  sed -E \
    -e 's/(Authorization:)[^\r\n]*/\1 [REDACTED]/g' \
    -e 's/(api[_-]?key["=: ]+)[^" ]+/\1[REDACTED]/gi' \
    -e 's/(secret["=: ]+)[^" ]+/\1[REDACTED]/gi' \
    -e 's/(password["=: ]+)[^" ]+/\1[REDACTED]/gi' \
    -e 's/(postgres:\/\/)[^@]+@/\1[REDACTED]@/g'
}

{
  echo "# LOGOS WALLET — BOOK 444"
  echo
  echo "**Дата сборки книги (UTC):** $ts"
  echo
  echo "Эта книга собрана автоматически из пакета: \`$(basename "$ARCHIVE")\`."
  echo
  echo "---"
  echo
  echo "## 1) Что именно зафиксировано"
  echo "- Полный слепок **wallet_prod** (и при наличии wallet_dev / wallet_premium)"
  echo "- nginx vhost'ы и upstream'ы (маршрутизация /node-api и /wallet-api)"
  echo "- systemd unit'ы (как реально подняты сервисы)"
  echo "- OpenAPI ноды (если было доступно при сборке пакета)"
  echo "- хвост логов (для диагностики LGN send)"
  echo
  echo "---"
  echo
  echo "## 2) Канонический инвентарь (паспорт сборки)"
  echo
  echo "### 2.1 Источник правды"
  echo "- **Активная версия UI:** wallet_prod"
  [[ -d "$WDEV" ]] && echo "- wallet_dev: присутствует (сравнение старых ручек/модулей)"
  [[ -d "$WPREM" ]] && echo "- wallet_premium: присутствует (сравнение UX/верстки)"
  echo
  echo "### 2.2 Обязательные файлы"
  echo "| Файл/папка | Назначение |"
  echo "|---|---|"
  echo "| auth.html/auth.js/auth.css | onboarding: create/confirm/restore/unlock |"
  echo "| app.html/app.js/app.css | основной кошелек UI |"
  echo "| modules/ | модули (LGN send и др.) |"
  echo "| vendor/ | зависимости (wordlist/bip39_lite/nacl) |"
  echo
  echo "### 2.3 Дерево wallet_prod"
  echo '```'
  (cd "$WPROD" && find . -maxdepth 3 -type f | sort) 2>/dev/null || true
  echo '```'
  echo
  echo "### 2.4 SHA256 (wallet_prod)"
  echo '```'
  (cd "$WPROD" && find . -type f -maxdepth 4 -print0 | sort -z | xargs -0 sha256sum) 2>/dev/null || true
  echo '```'
  echo
  echo "---"
  echo
  echo "## 3) Nginx (sites-enabled / sites-available)"
  echo
  echo "### sites-enabled"
  echo '```'
  (find "$NG/sites-enabled" -maxdepth 1 -type f -print -exec echo "----- {} -----" \; -exec cat {} \; 2>/dev/null | redact) || true
  echo '```'
  echo
  echo "### sites-available"
  echo '```'
  (find "$NG/sites-available" -maxdepth 1 -type f -print -exec echo "----- {} -----" \; -exec cat {} \; 2>/dev/null | redact) || true
  echo '```'
  echo
  echo "---"
  echo
  echo "## 4) systemd units"
  echo '```'
  (find "$SD/system" -maxdepth 1 -type f -name "*.service" -print -exec echo "----- {} -----" \; -exec cat {} \; 2>/dev/null | redact) || true
  echo '```'
  echo
  echo "---"
  echo
  echo "## 5) Node OpenAPI"
  if [[ -f "$OA/node-openapi.json" ]]; then
    echo
    echo '```json'
    head_safe "$OA/node-openapi.json" 2000 | redact
    echo '```'
  else
    echo
    echo "_OpenAPI не найден в пакете._"
  fi
  echo
  echo "---"
  echo
  echo "## 6) E2E плейбук: перевод LGN"
  echo "1) Unlock -> seed/keys в sessionStorage"
  echo "2) Draft TxIn: from/to/amount/nonce/memo"
  echo "3) Подпись Ed25519 -> sig_hex"
  echo "4) POST /node-api/submit_tx"
  echo "5) Проверка /node-api/balance/{rid}"
  echo "6) История: /node-api/history/{rid} (если есть)"
  echo
  echo "---"
  echo
  echo "## 7) Логи (tail)"
  echo
  echo "### logos-node@a"
  echo '```'
  head_safe "$LG/logos-node@a.log" 400 | redact
  echo '```'
  echo
  echo "### journal tail"
  echo '```'
  head_safe "$LG/journal_tail.log" 250 | redact
  echo '```'
  echo
  echo "---"
  echo
  echo "## 8) Release discipline"
  echo "- Снапшот: wallet_prod__v555_* (rsync 1:1)"
  echo "- Новая версия: wallet_prod__vNNN_*"
  echo "- Переключение: nginx root/alias или симлинк"
  echo "- Откат: вернуть root/alias на предыдущую папку + reload nginx"
  echo
} > "$BOOK"

echo "OK: wrote $BOOK"
