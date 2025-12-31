# LOGOS — Directory Book

## ROOT: /root/logos_lrb/tools

---
## STRUCTURE
```
/root/logos_lrb/tools
/root/logos_lrb/tools/bench
/root/logos_lrb/tools/bench/go
/root/logos_lrb/tools/gen_rid
/root/logos_lrb/tools/gen_rid/src
/root/logos_lrb/tools/go_test
/root/logos_lrb/tools/load
/root/logos_lrb/tools/sdk
/root/logos_lrb/tools/sdk/go
/root/logos_lrb/tools/sdk/ts
```

---
## FILES (FULL SOURCE)


### FILE: /root/logos_lrb/tools/admin_cli.sh
```
#!/usr/bin/env bash
set -euo pipefail

NODE_URL="${NODE_URL:-http://127.0.0.1:8080}"

# --- helpers ---
get_env() {
  systemctl show -p Environment logos-node.service \
    | sed -n 's/^Environment=//p' \
    | tr ' ' '\n' \
    | sed 's/"//g'
}

ENV_CACHE="$(get_env || true)"
get_var() { echo "$ENV_CACHE" | sed -n "s/^$1=//p" | head -n1; }

AK="${AK:-$(get_var LRB_ADMIN_KEY || true)}"
BK="${BK:-$(get_var LRB_BRIDGE_KEY || true)}"

require_admin_key() {
  if [[ -z "${AK:-}" || "$AK" == "CHANGE_ADMIN_KEY" ]]; then
    echo "[!] LRB_ADMIN_KEY не задан или дефолтный. Укажи AK=... в окружении или в keys.conf" >&2
    exit 1
  fi
}
require_bridge_key() {
  if [[ -z "${BK:-}" || "$BK" == "CHANGE_ME" ]]; then
    echo "[!] LRB_BRIDGE_KEY не задан или дефолтный. Укажи BK=... в окружении или в keys.conf" >&2
    exit 1
  fi
}

jq_or_cat() {
  if command -v jq >/dev/null 2>&1; then jq .; else cat; fi
}

usage() {
cat <<'EOF'
admin_cli.sh — удобные команды для LOGOS LRB (prod)

ENV:
  NODE_URL=http://127.0.0.1:8080     # адрес ноды (по умолчанию)
  AK=<admin-key>                     # можно переопределить, иначе берется из systemd
  BK=<bridge-key>                    # можно переопределить, иначе берется из systemd

Команды:
  health                      — /healthz
  head                        — /head
  node-info                   — /node/info
  validators                  — /admin/validators
  metrics [grep]              — /metrics (опциональный grep)

  snapshot-json               — GET /admin/snapshot (требует AK)
  snapshot-file [name]        — GET /admin/snapshot/file?name=NAME (требует AK)
  restore <abs_path.json>     — POST /admin/restore (требует AK)

  deposit <rid> <amount> <ext_txid>         — POST /bridge/deposit (требует BK)
  redeem  <rid> <amount> <request_id>       — POST /bridge/redeem (требует BK)
  verify  <ticket> <vk_b58> <signature_b64> — POST /bridge/verify

  account-txs <rid> [limit]   — GET /account/:rid/txs?limit=N

Примеры:
  ./admin_cli.sh head
  ./admin_cli.sh validators
  AK=$(systemctl show -p Environment logos-node.service | sed -n 's/.*LRB_ADMIN_KEY=\([^ ]*\).*/\1/p') \
    ./admin_cli.sh snapshot-json
  BK=$(systemctl show -p Environment logos-node.service | sed -n 's/.*LRB_BRIDGE_KEY=\([^ ]*\).*/\1/p') \
    ./admin_cli.sh deposit RID_A 12345 ext-1
EOF
}

cmd="${1:-}"
case "$cmd" in
  ""|-h|--help|help) usage; exit 0 ;;
esac
shift || true

case "$cmd" in
  health)
    curl -s "$NODE_URL/healthz" | jq_or_cat
    ;;

  head)
    curl -s "$NODE_URL/head" | jq_or_cat
    ;;

  node-info)
    curl -s "$NODE_URL/node/info" | jq_or_cat
    ;;

  validators)
    curl -s "$NODE_URL/admin/validators" | jq_or_cat
    ;;

  metrics)
    body="$(curl -s "$NODE_URL/metrics")"
    if [[ $# -gt 0 ]]; then echo "$body" | grep -E "$*" || true; else echo "$body"; fi
    ;;

  snapshot-json)
    require_admin_key
    curl -s -H "X-Admin-Key: $AK" "$NODE_URL/admin/snapshot" | jq_or_cat
    ;;

  snapshot-file)
    require_admin_key
    name="${1:-snap-$(date +%s).json}"
    curl -s -H "X-Admin-Key: $AK" "$NODE_URL/admin/snapshot/file?name=$name" | jq_or_cat
    ;;

  restore)
    require_admin_key
    file="${1:-}"
    [[ -z "$file" ]] && { echo "[!] usage: restore /var/lib/logos/snapshots/<file>.json" >&2; exit 1; }
    curl -s -X POST -H "content-type: application/json" -H "X-Admin-Key: $AK" \
      "$NODE_URL/admin/restore" \
      -d "{\"file\":\"$file\"}" | jq_or_cat
    ;;

  deposit)
    require_bridge_key
    rid="${1:-}"; amt="${2:-}"; xtx="${3:-}"
    [[ -z "$rid" || -z "$amt" || -z "$xtx" ]] && { echo "[!] usage: deposit <rid> <amount> <ext_txid>" >&2; exit 1; }
    curl -s -X POST "$NODE_URL/bridge/deposit" \
      -H "content-type: application/json" -H "X-Bridge-Key: $BK" \
      -d "{\"rid\":\"$rid\",\"amount\":$amt,\"ext_txid\":\"$xtx\"}" | jq_or_cat
    ;;

  redeem)
    require_bridge_key
    rid="${1:-}"; amt="${2:-}"; reqid="${3:-}"
    [[ -z "$rid" || -z "$amt" || -z "$reqid" ]] && { echo "[!] usage: redeem <rid> <amount> <request_id>" >&2; exit 1; }
    curl -s -X POST "$NODE_URL/bridge/redeem" \
      -H "content-type: application/json" -H "X-Bridge-Key: $BK" \
      -d "{\"rid\":\"$rid\",\"amount\":$amt,\"request_id\":\"$reqid\"}" | jq_or_cat
    ;;

  verify)
    ticket="${1:-}"; vk_b58="${2:-}"; sig_b64="${3:-}"
    [[ -z "$ticket" || -z "$vk_b58" || -z "$sig_b64" ]] && { echo "[!] usage: verify <ticket> <vk_b58> <signature_b64>" >&2; exit 1; }
    curl -s -X POST "$NODE_URL/bridge/verify" \
      -H "content-type: application/json" \
      -d "{\"ticket\":\"$ticket\",\"vk_b58\":\"$vk_b58\",\"signature_b64\":\"$sig_b64\"}" | jq_or_cat
    ;;

  account-txs)
    rid="${1:-}"; limit="${2:-100}"
    [[ -z "$rid" ]] && { echo "[!] usage: account-txs <rid> [limit]" >&2; exit 1; }
    curl -s "$NODE_URL/account/$rid/txs?limit=$limit" | jq_or_cat
    ;;

  *)
    echo "[!] unknown command: $cmd" >&2
    usage
    exit 1
    ;;
esac

```

### FILE: /root/logos_lrb/tools/admin_fund.sh
```
#!/usr/bin/env bash
set -euo pipefail

API="${API:-http://127.0.0.1:8080}"
RID="${RID:?RID required}"
AMOUNT="${AMOUNT:-1000000000000}"   # 1e12 LGN, хватит для бенчей
NONCE="${NONCE:-0}"
ADMIN_JWT="${ADMIN_JWT:?ADMIN_JWT required}"

echo "[*] set_balance $RID = $AMOUNT"
curl -sf -X POST "$API/admin/set_balance" \
  -H "X-Admin-JWT: $ADMIN_JWT" \
  -H 'Content-Type: application/json' \
  -d "{\"rid\":\"$RID\",\"amount\":$AMOUNT}" || { echo; echo "[ERR] set_balance failed"; exit 1; }
echo

echo "[*] set_nonce $RID = $NONCE"
curl -sf -X POST "$API/admin/set_nonce" \
  -H "X-Admin-JWT: $ADMIN_JWT" \
  -H 'Content-Type: application/json' \
  -d "{\"rid\":\"$RID\",\"value\":$NONCE}" || { echo; echo "[ERR] set_nonce failed"; exit 1; }
echo

```

### FILE: /root/logos_lrb/tools/batch.json
```

```

### FILE: /root/logos_lrb/tools/bench/submit_tx_auto.js
```
import http from 'k6/http';
import { check } from 'k6';
import exec from 'k6/execution';

// Конфиг через env: RATE, DURATION, VUS, MAX_VUS, BASE, TO_RID, FOUNDER_SK_HEX, AMOUNT
export const options = {
  scenarios: {
    submit: {
      executor: 'constant-arrival-rate',
      rate: Number(__ENV.RATE || '2000'),   // запросов/сек
      timeUnit: '1s',
      duration: __ENV.DURATION || '25s',
      preAllocatedVUs: Number(__ENV.VUS || '2000'),
      maxVUs: Number(__ENV.MAX_VUS || '4000'),
    },
  },
};

const BASE = __ENV.BASE || 'http://127.0.0.1:8080';
const TO   = __ENV.TO_RID || '';
const SK   = __ENV.FOUNDER_SK_HEX || '';
const AM   = Number(__ENV.AMOUNT || '1');

export default function () {
  // Уникальный nonce во всём тесте: 1..N
  const nonce = exec.scenario.iterationInTest + 1;

  const body = JSON.stringify({
    from_sk_hex: SK,
    to: TO,
    amount: AM,
    nonce: nonce,
  });

  const res = http.post(`${BASE}/admin/submit_tx_auto`, body, {
    headers: { 'Content-Type': 'application/json' },
    timeout: '30s',
  });

  check(res, {
    '200 OK': r => r.status === 200,
  });
}

```

### FILE: /root/logos_lrb/tools/book_make.sh
```
#!/usr/bin/env bash
set -euo pipefail

# Куда писать книгу
DATE_UTC=$(date -u +%Y-%m-%dT%H-%M-%SZ)
BOOK="docs/LOGOS_LRB_BOOK_${DATE_UTC}.txt"

# Корень репозитория (чтобы пути были относительные)
REPO_ROOT="/root/logos_lrb"
cd "$REPO_ROOT"

echo "[*] Building book: $BOOK"
mkdir -p docs

# --- списки включений/исключений ---
# Git-трекаемые файлы + критичные конфиги вне репы
INCLUDE_LIST="$(mktemp)"
EXTRA_LIST="$(mktemp)"

# 1) всё полезное из git (код/конфиги), без мусора
git ls-files \
  | grep -Ev '^(\.gitignore|README\.md|LICENSE|^docs/LOGOS_LRB_BOOK_|^docs/.*\.pdf$)' \
  | grep -Ev '(^target/|/target/|^node_modules/|/node_modules/|\.DS_Store|\.swp$|\.sqlite$|/data\.sled|/data\.sled/|\.pem$|\.key$)' \
  > "$INCLUDE_LIST"

# 2) системные файлы вне репы (если существуют)
add_extra() { [[ -f "$1" ]] && echo "$1" >> "$EXTRA_LIST"; }
add_extra "/etc/systemd/system/logos-node.service"
for f in /etc/systemd/system/logos-node.service.d/*.conf; do [[ -f "$f" ]] && echo "$f" >> "$EXTRA_LIST"; done
add_extra "/etc/nginx/conf.d/10_lrb_https.conf"
add_extra "/etc/prometheus/prometheus.yml"
for f in /etc/prometheus/rules/*.yml; do [[ -f "$f" ]] && echo "$f" >> "$EXTRA_LIST"; done
# Grafana provisioning/дашборды (если есть)
for f in /etc/grafana/provisioning/dashboards/*.yaml /var/lib/grafana/dashboards/*.json; do
  [[ -f "$f" ]] && echo "$f" >> "$EXTRA_LIST"
done
# OpenAPI (в репе уже есть), APK/лендинг укажем ссылкой — бинарники в книгу не кладём

# --- заголовок книги ---
{
  echo "LOGOS LRB — FULL LIVE BOOK (${DATE_UTC})"
  echo
  echo "Содержимое: весь код репозитория + ключевая инфраструктура (systemd/nginx/prometheus/grafana),"
  echo "формат: секции BEGIN/END FILE c sha256 и блочным EOF. Бинарники (APK, sled, pem) не включаются."
  echo
  echo "Репозиторий: $REPO_ROOT"
  echo
} > "$BOOK"

emit_file () {
  local src="$1" dst
  # внутри репо пишем относительные пути; вне — абсолютные
  if [[ "$src" == $REPO_ROOT/* ]]; then
    dst="/${src#$REPO_ROOT/}"
  else
    dst="$src"
  fi
  # пропуск «мусора»
  if [[ -d "$src" ]]; then return 0; fi
  if [[ ! -f "$src" ]]; then return 0; fi
  # вычисляем sha256
  local sum
  sum=$(sha256sum "$src" | awk '{print $1}')
  {
    echo "===== BEGIN FILE $dst ====="
    echo "# sha256: $sum"
    echo "<<'EOF'"
    cat "$src"
    echo "EOF"
    echo "===== END FILE $dst ====="
    echo
  } >> "$BOOK"
}

echo "[*] Emitting repo files..."
while IFS= read -r p; do emit_file "$REPO_ROOT/$p"; done < "$INCLUDE_LIST"

echo "[*] Emitting extra system files..."
if [[ -s "$EXTRA_LIST" ]]; then
  while IFS= read -r p; do emit_file "$p"; done < "$EXTRA_LIST"
fi

# --- прикладываем «паспорт» окружения ---
{
  echo "===== BEGIN FILE /docs/ENV_SNAPSHOT.txt ====="
  echo "# sha256: N/A"
  echo "<<'EOF'"
  echo "[systemd env]"
  systemctl show logos-node -p Environment | sed 's/^Environment=//'
  echo
  echo "[nginx -v]"
  nginx -v 2>&1 || true
  echo
  echo "[prometheus rules list]"
  ls -1 /etc/prometheus/rules 2>/dev/null || true
  echo
  echo "[grafana dashboards list]"
  ls -1 /var/lib/grafana/dashboards 2>/dev/null || true
  echo "EOF"
  echo "===== END FILE /docs/ENV_SNAPSHOT.txt ====="
  echo
} >> "$BOOK"

echo "[*] Book is ready: $BOOK"

```

### FILE: /root/logos_lrb/tools/book_restore.sh
```
#!/usr/bin/env bash
set -euo pipefail

BOOK="${1:-}"
if [[ -z "$BOOK" || ! -f "$BOOK" ]]; then
  echo "usage: $0 /path/to/LOGOS_LRB_BOOK_*.txt"; exit 1
fi

echo "[*] Restoring files from: $BOOK"
RESTORED=0
BADHASH=0

# прочитаем книгу и вытащим секции
# формат: BEGIN FILE <path>\n# sha256: <hex>\n<<'EOF'\n...EOF\nEND FILE
awk '
  /^===== BEGIN FILE / {
    inblock=1
    path=""
    sha=""
    gsub(/^===== BEGIN FILE /,"")
    gsub(/ =====$/,"")
    path=$0
    next
  }
  inblock && /^# sha256:/ {
    sha=$2
    next
  }
  inblock && /^<<'\''EOF'\''/ { collecting=1; content=""; next }
  collecting && /^EOF$/ { collecting=0; inblock=2; next }
  inblock==1 && !collecting { next }
  collecting { content = content $0 "\n"; next }
  inblock==2 && /^===== END FILE / {
    # записываем файл
    # создадим директорию
    cmd = "mkdir -p \"" path "\""
    sub(/\/[^\/]+$/, "", cmdpath=path) # dir part
    if (cmdpath != "") {
      system("mkdir -p \"" cmdpath "\"")
    }
    # записываем
    f = path
    gsub(/\r$/,"",content)
    # защитимся от /etc/... если нет прав — предложим sudo
    # но здесь просто пишем как есть
    outfile = path
    # если путь абсолютный, пишем в тот же абсолютный; если относительный — относительно cwd
    # создадим временный и заменим
    tmpfile = outfile ".tmp.restore"
    # в shell передам через printf
    print content > tmpfile
    close(tmpfile)
    # проверка sha256 если есть
    if (sha != "" && sha != "N/A") {
      cmdsum = "sha256sum \"" tmpfile "\" | awk '\''{print $1}'\''"
      cmdsum | getline got
      close(cmdsum)
      if (got != sha) {
        print "[WARN] sha256 mismatch for " outfile " expected=" sha " got=" got
        BADHASH++
      }
    }
    system("install -m 0644 \"" tmpfile "\" \"" outfile "\"")
    system("rm -f \"" tmpfile "\"")
    print "[OK] restored " outfile
    RESTORED++
    inblock=0
    next
  }
  END {
    # summary в AWK не выведем; сделаем в оболочке
  }
' "$BOOK"

echo "[*] Restored files: $RESTORED"
if [[ "${BADHASH:-0}" -gt 0 ]]; then
  echo "[!] WARNING: sha256 mismatches: $BADHASH"
fi

echo "[*] Done. Проверь права на системные файлы, возможно потребуется sudo chown/chmod."

```

### FILE: /root/logos_lrb/tools/build_book_from_list.sh
```
#!/usr/bin/env bash
set -e

LIST="$1"
OUT="$2"

echo "# $(basename "$OUT" .md)" > "$OUT"
echo "" >> "$OUT"

while IFS= read -r FILE; do
  [ -f "$FILE" ] || continue

  EXT="${FILE##*.}"
  LANG="$EXT"

  echo "## $FILE" >> "$OUT"
  echo '```'"$LANG" >> "$OUT"
  cat "$FILE" >> "$OUT"
  echo '```' >> "$OUT"
  echo "" >> "$OUT"
done < "$LIST"

```

### FILE: /root/logos_lrb/tools/build_books_ascii.sh
```
#!/usr/bin/env bash
set -Eeuo pipefail
export LANG=C LC_ALL=C
cd /root/logos_lrb

STAMP="${STAMP:-$(date +%F_%H-%M-%S)}"
OUTDIR="docs/LOGOS_LRB_BOOK"
SNAPDIR="docs/snapshots"
ROOTS_FILE="${ROOTS_FILE:-$(ls -1t docs/REPO_ROOTS_*.txt 2>/dev/null | head -n1)}"

mkdir -p "$OUTDIR" "$SNAPDIR"

build_one() {
  local root="$1"
  [ -z "$root" ] && return
  [ "$root" = "." ] && return
  [ ! -d "$root" ] && return

  local safe="${root//[\/ ]/__}"
  local book="${OUTDIR}/BOOK_${safe}_${STAMP}.md"
  local snap="${SNAPDIR}/SNAP_${safe}_${STAMP}.tar.xz"

  {
    echo "# BOOK for '${root}' (LIVE ${STAMP})"
    echo
    echo "## Project tree (${root})"
    echo '```text'
  } > "$book"

  find "$root" \
    -path "$root/target" -o -path "$root/.git" -o -path "$root/tests" -o -path "$root/node_modules" -prune -o \
    -type d -print \
  | awk -v r="$root" '{p=$0; if(p==r){print "."; next} sub("^" r "/","",p); print p}' \
  | LC_ALL=C sort >> "$book"

  {
    echo '```'
    echo
    echo "## Files (sources/configs/docs)  full content"
    echo
  } >> "$book"

  LC_ALL=C find "$root" \
    \( -path "$root/target" -o -path "$root/.git" -o -path "$root/tests" -o -path "$root/node_modules" \) -prune -o \
    -type f \( -name '*.rs' -o -name '*.toml' -o -name '*.yaml' -o -name '*.yml' -o \
               -name '*.json' -o -name '*.md'   -o -name '*.sh'   -o -name '*.py'  -o \
               -name '*.service' -o -name '*.conf' -o -name 'Makefile' -o -name '*.sql' -o \
               -name '*.mjs' -o -name '*.ts' -o -name '*.tsx' \) -print0 \
  | sort -z \
  | while IFS= read -r -d '' f; do
      kb=$(du -k "$f" | awk '{print $1}')
      if [ "$kb" -gt 5120 ]; then
        printf "### \`%s\` (skipped: >5MB)\n\n" "$f" >> "$book"
        continue
      fi
      case "$f" in
        *.rs) lang=rust ;;
        *.toml) lang=toml ;;
        *.yaml|*.yml) lang=yaml ;;
        *.json) lang=json ;;
        *.sh) lang=bash ;;
        *.py) lang=python ;;
        *.service|*.conf) lang=ini ;;
        *.sql) lang=sql ;;
        Makefile) lang=make ;;
        *.md) lang=markdown ;;
        *.mjs) lang=javascript ;;
        *.ts)  lang=typescript ;;
        *.tsx) lang=tsx ;;
        *)     lang=text ;;
      esac
      printf "### \`%s\`\n\n\`\`\`%s\n" "$f" "$lang" >> "$book"
      cat "$f" >> "$book"
      printf "\n\`\`\`\n\n" >> "$book"
    done

  tar -C . \
    --exclude="./$root/target" \
    --exclude="./$root/.git" \
    --exclude="./$root/tests" \
    --exclude="./$root/node_modules" \
    -c "$root" | xz -T1 -9 -c > "$snap"

  printf "[OK] %-16s book=%-6s snap=%s\n" "$root" "$(du -h "$book" | awk '{print $1}')" "$(du -h "$snap" | awk '{print $1}')"
}

echo "=== Building per-root books from: ${ROOTS_FILE} ==="
while read -r root; do
  build_one "$root"
done < "$ROOTS_FILE"

echo "=== Summary ==="
du -ch "$OUTDIR"/BOOK_*_"$STAMP".md 2>/dev/null | tail -n1 || true
du -ch "$SNAPDIR"/SNAP_*_"$STAMP".tar.xz 2>/dev/null | tail -n1 || true

```

### FILE: /root/logos_lrb/tools/build_books.sh
```
#!/usr/bin/env bash
set -euo pipefail
export LANG=C LC_ALL=C

ROOT="$(cd "$(dirname "$0")/.."; pwd)"
cd "$ROOT"

STAMP="$(date +%F_%H-%M-%S)"
OUTDIR="docs/LOGOS_LRB_BOOK"
SNAPDIR="docs/snapshots"
mkdir -p "$OUTDIR" "$SNAPDIR"

# 1) строим файл корней
ROOTS_FILE="docs/REPO_ROOTS_${STAMP}.txt"
{
  find . -type f -name Cargo.toml     -printf '%h\n'
  find . -type f -name pyproject.toml -printf '%h\n'
  find . -type f -name package.json   -printf '%h\n'
  find . -type f -name go.mod         -printf '%h\n'
  # статические корни
  printf '%s\n' \
    configs configs/env \
    infra/nginx infra/systemd \
    lrb_core node wallet-proxy \
    www www/wallet www/explorer
} | sed 's#^\./##' | sort -u | grep -vE '^$' > "$ROOTS_FILE"

echo "=== Building per-root books from: $ROOTS_FILE ==="

build_one() {
  local root="$1"
  [[ -z "$root" || "$root" = "." ]] && return

  local safe="${root//[\/ ]/__}"
  local book="${OUTDIR}/BOOK_${safe}_${STAMP}.md"
  local snap="${SNAPDIR}/SNAP_${safe}_${STAMP}.tar.xz"

  {
    echo "# BOOK for '${root}' (LIVE ${STAMP})"
    echo
    echo "## Project tree (${root})"
    echo '```text'
    find "$root" \
      -path "$root/target" -prune -o \
      -path "$root/.git"   -prune -o \
      -path "$root/tests"  -prune -o \
      -type d -print \
      | sed "s#^${root}/##; s#^${root}$#.#" \
      | sort
    echo '```'
    echo
    echo "## Files (sources/configs/docs) — full content"
    echo
  } > "$book"

  # перечисляем файлы (текстовые) и кладём содержимое
  while IFS= read -r -d '' f; do
    [[ -s "$f" ]] || continue
    # скипаем > 5MB, чтобы книга не вылезла за лимит
    local_kb="$(du -k "$f" | awk '{print $1}')"
    if [ "$local_kb" -gt 5120 ]; then
      echo "### \`$f\` (skipped: >5MB)" >> "$book"
      echo >> "$book"
      continue
    fi
    lang="text"
    case "$f" in
      *.rs)        lang="rust" ;;
      *.toml)      lang="toml" ;;
      *.yaml|*.yml)lang="yaml" ;;
      *.json)      lang="json" ;;
      *.sh)        lang="bash" ;;
      *.py)        lang="python" ;;
      *.service|*.conf) lang="ini" ;;
      *.sql)       lang="sql" ;;
      Makefile)    lang="make" ;;
      *.md)        lang="markdown" ;;
      *.mjs)       lang="javascript" ;;
      *.ts)        lang="typescript" ;;
      *.tsx)       lang="tsx" ;;
    esac
    echo "### \`$f\`" >> "$book"
    echo '```'"$lang" >> "$book"
    cat "$f" >> "$book"
    echo '```' >> "$book"
    echo >> "$book"
  done < <(find "$root" \
              -path "$root/target" -prune -o \
              -path "$root/.git"   -prune -o \
              -path "$root/tests"  -prune -o \
              -type f \( \
                -name '*.rs' -o -name '*.toml' -o -name '*.yaml' -o -name '*.yml' -o \
                -name '*.json' -o -name '*.md'  -o -name '*.sh'   -o -name '*.py'  -o \
                -name '*.service' -o -name '*.conf' -o -name 'Makefile' -o -name '*.sql' -o \
                -name '*.mjs' -o -name '*.ts' -o -name '*.tsx' \
              \) -print0 | sort -z)

  # компактный снапшот дерева
  tar -C . \
    --exclude="./$root/target" \
    --exclude="./$root/.git" \
    --exclude="./$root/tests" \
    --exclude="./$root/node_modules" \
    -c "$root" | xz -T1 -9 -c > "$snap"

  printf "[OK] %-16s | book=%-6s snap=%s\n" \
    "$root" "$(du -h "$book" | awk '{print $1}')" \
    "$(du -h "$snap" | awk '{print $1}')"
}

# прогон по корням
while IFS= read -r root; do
  build_one "$root"
done < "$ROOTS_FILE"

# краткая сводка
echo
echo "=== Books summary ===";     du -ch docs/LOGOS_LRB_BOOK/BOOK_*_${STAMP}.md       | tail -n1 || true
echo "=== Snapshots summary ==="; du -ch docs/snapshots/SNAP_*_${STAMP}.tar.xz        | tail -n1 || true

```

### FILE: /root/logos_lrb/tools/canon_choice.txt
```
sha256_pipe_be_be

```

### FILE: /root/logos_lrb/tools/find_sk_var_for_rid.py
```
#!/usr/bin/env python3
import sys, re, pathlib
from nacl.signing import SigningKey

ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58enc(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = ALPH[r] + out
    pad = 0
    for x in b:
        if x == 0: pad += 1
        else: break
    return ("1"*pad) + (out or "1")

def parse_env(path: str):
    p = pathlib.Path(path)
    if not p.exists():
        return {}
    d = {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"): 
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', line)
        if not m:
            continue
        k = m.group(1)
        v = m.group(2).strip().strip('"').strip("'")
        d[k] = v
    return d

def main():
    if len(sys.argv) != 2:
        print("usage: find_sk_var_for_rid.py <RID>", file=sys.stderr)
        sys.exit(2)
    rid_target = sys.argv[1].strip()

    env = parse_env("/etc/logos/proxy.env")
    candidates = [(k, v) for k, v in env.items() if k.endswith("_SK_HEX") and len(v) >= 64]

    for k, v in candidates:
        # берём первые 64 hex (32 байта). Если у тебя ключи ровно 64 — будет ок.
        hx = v.lower().replace("0x","")[:64]
        if not re.fullmatch(r"[0-9a-f]{64}", hx):
            continue
        sk = SigningKey(bytes.fromhex(hx))
        rid2 = b58enc(bytes(sk.verify_key))
        if rid2 == rid_target:
            print(k)
            return

    # не нашли
    sys.exit(3)

if __name__ == "__main__":
    main()

```

### FILE: /root/logos_lrb/tools/gen_full_codemap.py
```
#!/usr/bin/env python3
# gen_full_codemap.py — cоздаёт единый текстовый слепок исходников из заданных директорий.
# Использование:
#   python3 gen_full_codemap.py OUTPUT.txt DIR1 [DIR2 ...]
#
# Пример:
#   python3 gen_full_codemap.py /root/logos_snapshot/SNAPSHOT_$(date +%F_%H%M).txt /root/logos_lrb /root/logos_rsp

import os, sys, hashlib, time

OK_EXT = {
    '.rs','.py','.tsx','.ts','.js','.jsx','.go',
    '.html','.htm','.css','.scss','.md','.txt',
    '.yaml','.yml','.toml','.ini','.cfg','.conf',
    '.sh','.bash','.zsh','.sql','.proto','.graphql',
    '.env.example','.service','.timer'
}

EXCLUDE_DIR_PREFIXES = (
    '.git','target','node_modules','build','dist','out','venv','.venv','__pycache__',
    '.idea','.vscode','.fleet','.DS_Store','coverage','.pytest_cache',
    '.cargo','.gradle','android/app/build','ios/Pods','.dart_tool',
    'tools/.venv','tools/venv','.husky'
)

EXCLUDE_FILE_PATTERNS = (
    '.env',        # любые .env (чтобы не потянуть реальные секреты)
    '.pem','.key','.crt','.p12','.keystore','.jks',
    '.sqlite','.db','.db3','.sqlite3',
    '.lock','.bin','.wasm','.o','.a'
)

MAX_FILE_BYTES = 400_000       # не включать слишком большие файлы
MAX_TOTAL_BYTES = 300_000_000  # общий предел (300 МБ, чтобы не улететь в космос)

def is_excluded_dir(path):
    norm = path.replace('\\','/')
    parts = norm.split('/')
    for p in parts:
        for ex in EXCLUDE_DIR_PREFIXES:
            if p == ex or norm.startswith(ex + '/'):
                return True
    return False

def is_ok_file(path):
    # исключить секреты/бинарники по шаблонам имени
    low = path.lower()
    for pat in EXCLUDE_FILE_PATTERNS:
        if low.endswith(pat) or f"/{pat}" in low:
            return False
    # по расширениям
    _, ext = os.path.splitext(path)
    if ext.lower() in OK_EXT:
        try:
            if os.path.getsize(path) <= MAX_FILE_BYTES:
                return True
        except FileNotFoundError:
            return False
    return False

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path,'rb') as r:
        while True:
            b = r.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

def collect_files(roots):
    out = []
    for root in roots:
        root = os.path.abspath(root)
        if not os.path.isdir(root):
            continue
        for dp, dn, fn in os.walk(root):
            # пропуск скрытых/исключённых директорий
            norm_dp = dp.replace('\\','/')
            if is_excluded_dir(norm_dp):
                dn[:] = []  # не спускаться ниже
                continue
            for f in fn:
                p = os.path.join(dp,f)
                norm = p.replace('\\','/')
                # пропускаем скрытые файлы
                if any(seg.startswith('.') and seg not in ('.env.example',) for seg in norm.split('/')):
                    # .env.example оставляем
                    pass
                if is_ok_file(norm):
                    out.append(norm)
    out = sorted(set(out))
    return out

def main():
    if len(sys.argv) < 3:
        print("Usage: gen_full_codemap.py OUTPUT.txt DIR1 [DIR2 ...]", file=sys.stderr)
        sys.exit(1)
    output = os.path.abspath(sys.argv[1])
    roots  = sys.argv[2:]
    files  = collect_files(roots)
    ts = time.strftime('%Y-%m-%d %H:%M:%S')

    total_written = 0
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8', errors='replace') as w:
        w.write("# FULL CODE SNAPSHOT\n")
        w.write(f"Generated: {ts}\n")
        w.write(f"Roots: {', '.join(os.path.abspath(r) for r in roots)}\n")
        w.write(f"Files count: {len(files)}\n")
        w.write("\n## Table of Contents\n")
        for i, p in enumerate(files, 1):
            anchor = f"{i}-{p.replace('/','-')}"
            w.write(f"{i}. {p}  ->  #{anchor}\n")
        w.write("\n---\n")

        for i, p in enumerate(files, 1):
            try:
                size = os.path.getsize(p)
                sha  = sha256_of_file(p)
                with open(p,'r',encoding='utf-8',errors='replace') as r:
                    data = r.read()
            except Exception as e:
                data = f"<<error reading {p}: {e}>>"
                size = -1
                sha  = "n/a"

            header = f"\n## {i}. {p}\n#size={size} bytes  sha256={sha}\n<a name=\"{i}-{p.replace('/','-')}\"></a>\n\n"
            body   = "```text\n" + data + "\n```\n"
            chunk  = header + body
            enc    = chunk.encode('utf-8', errors='replace')
            if total_written + len(enc) > MAX_TOTAL_BYTES:
                w.write("\n\n<< STOPPED: reached MAX_TOTAL_BYTES limit >>\n")
                break
            w.write(chunk)
            total_written += len(enc)

    print(f"[ok] Wrote snapshot to: {output}")
    print(f"[info] Files included: {len(files)}")
    print(f"[info] Approx bytes written: {total_written}")

if __name__ == '__main__':
    main()

```

### FILE: /root/logos_lrb/tools/gen_main_rs.sh
```
#!/usr/bin/env bash
set -euo pipefail

SRC="node/src"
STAKING="$SRC/api/staking.rs"
BRIDGE="$SRC/bridge.rs"
ARCHMOD="$SRC/api/archive.rs"
TXMOD="$SRC/api/tx.rs"
BASEMOD="$SRC/api/base.rs"
HEALTH="$SRC/health.rs"

has() { grep -qE "$2" "$1" 2>/dev/null; }

HAS_STAKE_DELEGATE=false
HAS_STAKE_UNDELEGATE=false
HAS_STAKE_CLAIM=false
HAS_STAKE_MY=false
if [[ -f "$STAKING" ]]; then
  has "$STAKING" 'pub\s+async\s+fn\s+stake_delegate'  && HAS_STAKE_DELEGATE=true
  has "$STAKING" 'pub\s+async\s+fn\s+stake_undelegate'&& HAS_STAKE_UNDELEGATE=true
  has "$STAKING" 'pub\s+async\s+fn\s+stake_claim'     && HAS_STAKE_CLAIM=true
  has "$STAKING" 'pub\s+async\s+fn\s+stake_my'        && HAS_STAKE_MY=true
fi

HAS_BRIDGE_DEPOSIT_JSON=false
HAS_BRIDGE_REDEEM_JSON=false
if [[ -f "$BRIDGE" ]]; then
  has "$BRIDGE" 'pub\s+async\s+fn\s+deposit_json' && HAS_BRIDGE_DEPOSIT_JSON=true
  has "$BRIDGE" 'pub\s+async\s+fn\s+redeem_json'  && HAS_BRIDGE_REDEEM_JSON=true
fi

HAS_ARCH_TX=false
HAS_ARCH_HIST=false
HAS_ARCH_BLOCKS=false
if [[ -f "$ARCHMOD" ]]; then
  has "$ARCHMOD" 'pub\s+async\s+fn\s+tx_by_id'        && HAS_ARCH_TX=true
  has "$ARCHMOD" 'pub\s+async\s+fn\s+history_by_rid'  && HAS_ARCH_HIST=true
  has "$ARCHMOD" 'pub\s+async\s+fn\s+recent_blocks'   && HAS_ARCH_BLOCKS=true
fi

HAS_TX_SUBMIT=false
HAS_TX_BATCH=false
if [[ -f "$TXMOD" ]]; then
  has "$TXMOD" 'pub\s+async\s+fn\s+submit_tx\b'       && HAS_TX_SUBMIT=true
  has "$TXMOD" 'pub\s+async\s+fn\s+submit_tx_batch\b' && HAS_TX_BATCH=false
fi

HAS_HEALTHZ=false
if [[ -f "$HEALTH" ]]; then
  has "$HEALTH" 'pub\s+async\s+fn\s+healthz' && HAS_HEALTHZ=true
fi

cat > "$SRC/main.rs" <<'RS'
use std::{net::SocketAddr, sync::Arc};
use anyhow::Result;
use axum::{Router, routing::{get, post}};
use tower::ServiceBuilder;
use tower_http::trace::TraceLayer;

// Импорты из библиотечной части пакета:
use logos_node::state::AppState;
use logos_node::api::{self, base};
RS

# staking
if $HAS_STAKE_DELEGATE || $HAS_STAKE_UNDELEGATE || $HAS_STAKE_CLAIM || $HAS_STAKE_MY; then
  cat >> "$SRC/main.rs" <<'RS'
use logos_node::api::staking;
RS
fi

# archive
if $HAS_ARCH_TX || $HAS_ARCH_HIST || $HAS_ARCH_BLOCKS; then
  cat >> "$SRC/main.rs" <<'RS'
use logos_node::api::archive as api_archive;
RS
fi

# tx
if $HAS_TX_SUBMIT || $HAS_TX_BATCH; then
  cat >> "$SRC/main.rs" <<'RS'
use logos_node::api::tx;
RS
fi

# health
if $HAS_HEALTHZ; then
  cat >> "$SRC/main.rs" <<'RS'
use logos_node::health;
RS
fi

# bridge
if $HAS_BRIDGE_DEPOSIT_JSON || $HAS_BRIDGE_REDEEM_JSON; then
  cat >> "$SRC/main.rs" <<'RS'
use logos_node::bridge;
RS
fi

cat >> "$SRC/main.rs" <<'RS'

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    // state
    let mut st = AppState::new()?;
    st.init_archive().await?;
    let shared = Arc::new(st);

    async fn livez() -> &'static str { "ok" }
    async fn readyz() -> &'static str { "ok" }

    // В Axum 0.7: сначала фиксируем тип состояния
    let mut app = Router::new()
        .with_state(shared.clone())
        .layer(ServiceBuilder::new().layer(TraceLayer::new_for_http()))
        .route("/livez", get(livez))
        .route("/readyz", get(readyz));
RS

if $HAS_HEALTHZ; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/healthz", get(health::healthz));
RS
fi

cat >> "$SRC/main.rs" <<'RS'
    // /head, /version
    app = app.merge(base::routes(shared.clone()));
RS

if $HAS_TX_SUBMIT; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/submit_tx", post(tx::submit_tx));
RS
fi
if $HAS_TX_BATCH; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/submit_tx_batch", post(tx::submit_tx_batch));
RS
fi

if $HAS_ARCH_TX; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/archive/tx/:txid", get(api_archive::tx_by_id));
RS
fi
if $HAS_ARCH_HIST; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/archive/history/:rid", get(api_archive::history_by_rid));
RS
fi
if $HAS_ARCH_BLOCKS; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/archive/blocks", get(api_archive::recent_blocks));
RS
fi

if $HAS_STAKE_DELEGATE; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/stake/delegate", post(staking::stake_delegate));
RS
fi
if $HAS_STAKE_UNDELEGATE; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/stake/undelegate", post(staking::stake_undelegate));
RS
fi
if $HAS_STAKE_CLAIM; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/stake/claim", post(staking::stake_claim));
RS
fi
if $HAS_STAKE_MY; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/stake/my/:rid", get(staking::stake_my));
RS
fi

if $HAS_BRIDGE_DEPOSIT_JSON; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/bridge/deposit_json", post(bridge::deposit_json));
RS
fi
if $HAS_BRIDGE_REDEEM_JSON; then
  cat >> "$SRC/main.rs" <<'RS'
    app = app.route("/bridge/redeem_json", post(bridge::redeem_json));
RS
fi

cat >> "$SRC/main.rs" <<'RS'
    let addr: SocketAddr = shared.bind_addr();
    tracing::info!("🚀 LOGOS LRB node listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    Ok(())
}
RS

echo "[gen_main_rs] main.rs generated successfully."

```

### FILE: /root/logos_lrb/tools/gen_rid/Cargo.toml
```
[package]
name = "gen_rid"
version = "0.1.0"
edition = "2021"

[dependencies]
ed25519-dalek = "2"
rand_core = "0.6"
bs58 = "0.5"
hex = "0.4"

```

### FILE: /root/logos_lrb/tools/gen_rid/src/main.rs
```
use ed25519_dalek::{SigningKey, VerifyingKey};
use rand_core::OsRng;
fn main() {
    // Если задан SK_HEX — используем его, иначе генерируем новый
    let args: Vec<String> = std::env::args().collect();
    let sk_hex = std::env::var("SK_HEX").ok();
    let (sk, sk_src) = if let Some(h) = sk_hex {
        let b = hex::decode(&h).expect("bad SK_HEX");
        let arr: [u8;32] = b.try_into().expect("need 32 bytes");
        (SigningKey::from_bytes(&arr), "import")
    } else {
        (SigningKey::generate(&mut OsRng), "generated")
    };

    let vk: VerifyingKey = sk.verifying_key();
    let rid_b58 = bs58::encode(vk.as_bytes()).into_string();

    println!("src={}", sk_src);
    println!("sk_hex={}", hex::encode(sk.to_bytes()));
    println!("vk_hex={}", hex::encode(vk.to_bytes()));
    println!("rid_b58={}", rid_b58);
}

```

### FILE: /root/logos_lrb/tools/gen_stress_key.py
```
#!/usr/bin/env python
from nacl.signing import SigningKey
import base58

sk = SigningKey.generate()
vk = sk.verify_key

sk_hex = sk._signing_key.hex()          # 32 байта seed как hex
vk_bytes = bytes(vk)                    # 32 байта pk
rid = base58.b58encode(vk_bytes).decode()

print("STRESS_SK_HEX=", sk_hex)
print("STRESS_RID   =", rid)

```

### FILE: /root/logos_lrb/tools/k6_smoke.js
```
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '60s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1500'],
  },
};

export default function () {
  http.get('http://127.0.0.1:8080/healthz');
  http.get('http://127.0.0.1:8080/economy');
  http.get('http://127.0.0.1:8080/balance/A');
  sleep(0.05);
}

```

### FILE: /root/logos_lrb/tools/k6_submit_tx_auto.js
```
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  scenarios: {
    ramp: { executor: 'ramping-arrival-rate',
      startRate: 200, preAllocatedVUs: 200, timeUnit: '1s',
      stages: [
        { target: 1000, duration: '20s' },
        { target: 2000, duration: '20s' },
        { target: 3000, duration: '20s' }
      ]
    }
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<200ms']
  }
};
const BASE = __ENV.BASE || 'http://127.0.0.1:8080';

export function setup() {
  const sink = http.get(`${BASE}/admin/make_rid`).json();
  const sinkRid = sink.rid_b58;
  const a = http.get(`${BASE}/admin/make_rid`).json();
  http.post(`${BASE}/faucet/${a.rid_b58}/5000000`);
  return { acc: a, sinkRid };
}

export default function (data) {
  const nonce = __ITER + 1;
  const body = JSON.stringify({ from_sk_hex: data.acc.sk_hex, to: data.sinkRid, amount: 1, nonce });
  const res = http.post(`${BASE}/admin/submit_tx_auto`, body, { headers: {'Content-Type':'application/json'} });
  check(res, { '200/201': r => r.status === 200 || r.status === 201 });
  if (__ITER % 1000 === 0) sleep(0.01);
}

```

### FILE: /root/logos_lrb/tools/load_healthz.sh
```
#!/usr/bin/env bash
# load_healthz.sh — прогон healthz с прогрессом
# Usage: ./load_healthz.sh <TOTAL=50000> <CONC=200> <MODE=rr|lb>
set -euo pipefail
TOTAL="${1:-50000}"
CONC="${2:-200}"
MODE="${3:-rr}"

start_ts=$(date +%s%3N)
cnt=0
print_prog() { cnt=$((cnt+1)); if (( cnt % 1000 == 0 )); then echo -n "."; fi; }

if [ "$MODE" = "rr" ]; then
  seq 1 "$TOTAL" | xargs -n1 -P"$CONC" -I{} bash -c '
    i="{}"; r=$(( i % 3 ))
    if   [ $r -eq 0 ]; then p=8080
    elif [ $r -eq 1 ]; then p=8082
    else                   p=8084
    fi
    curl -sS --max-time 2 -o /dev/null "http://127.0.0.1:${p}/healthz"
  ' && echo
else
  seq 1 "$TOTAL" | xargs -n1 -P"$CONC" -I{} bash -c '
    curl -sS --max-time 2 -o /dev/null "http://127.0.0.1/api/healthz"
  ' && echo
fi

end_ts=$(date +%s%3N)
dt_ms=$(( end_ts - start_ts ))
rps=$(( TOTAL * 1000 / (dt_ms>0?dt_ms:1) ))
echo "[OK] sent ${TOTAL} requests in ${dt_ms} ms  → ~${rps} req/s"

```

### FILE: /root/logos_lrb/tools/lrb_audit.sh
```
#!/usr/bin/env bash
set -euo pipefail
cd /root/logos_lrb

REPORT="AUDIT_REPORT.md"
echo "# LOGOS LRB — Аудит модулей" > "$REPORT"
echo "_$(date -u)_ UTC" >> "$REPORT"
echo >> "$REPORT"

sha() { sha256sum "$1" | awk '{print $1}'; }

audit_rust() {
  local f="$1"
  local lines; lines=$(wc -l <"$f")
  local s_unsafe s_unwrap s_expect s_panic s_todo s_dbg
  s_unsafe=$(grep -c '\<unsafe\>' "$f" || true)
  s_unwrap=$(grep -c 'unwrap(' "$f" || true)
  s_expect=$(grep -c 'expect(' "$f" || true)
  s_panic=$(grep -c 'panic!(' "$f" || true)
  s_dbg=$(grep -Ec 'dbg!|println!' "$f" || true)
  s_todo=$(grep -ni 'TODO\|FIXME\|todo!\|unimplemented!' "$f" | sed 's/^/    /' || true)
  {
    echo "### \`$f\` (Rust)"
    echo "- lines: $lines | sha256: \`$(sha "$f")\`"
    echo "- red-flags: unsafe=$s_unsafe, unwrap=$s_unwrap, expect=$s_expect, panic=$s_panic, dbg/println=$s_dbg"
    [ -n "$s_todo" ] && echo "- TODO/FIXME:"$'\n'"$s_todo"
    echo
  } >> "$REPORT"
}

audit_py() {
  local f="$1"
  local lines; lines=$(wc -l <"$f")
  local s_eval s_exec s_pickle s_subp s_todo
  s_eval=$(grep -c '\<eval\>' "$f" || true)
  s_exec=$(grep -c '\<exec\>' "$f" || true)
  s_pickle=$(grep -c 'pickle' "$f" || true)
  s_subp=$(grep -c 'subprocess' "$f" || true)
  s_todo=$(grep -ni 'TODO\|FIXME' "$f" | sed 's/^/    /' || true)
  {
    echo "### \`$f\` (Python)"
    echo "- lines: $lines | sha256: \`$(sha "$f")\`"
    echo "- red-flags: eval=$s_eval, exec=$s_exec, pickle=$s_pickle, subprocess=$s_subp"
    [ -n "$s_todo" ] && echo "- TODO/FIXME:"$'\n'"$s_todo"
    echo
  } >> "$REPORT"
}

audit_other() {
  local f="$1"
  local lines; lines=$(wc -l <"$f")
  {
    echo "### \`$f\`"
    echo "- lines: $lines | sha256: \`$(sha "$f")\`"
    grep -ni 'TODO\|FIXME' "$f" | sed 's/^/    - /' || true
    echo
  } >> "$REPORT"
}

echo "## Files in modules/" >> "$REPORT"
find modules -maxdepth 1 -type f | sort | while read -r f; do
  case "$f" in
    *.rs) audit_rust "$f" ;;
    *.py) audit_py "$f" ;;
    *.tsx|*.ts|*.yaml|*.yml|*.md) audit_other "$f" ;;
    *) audit_other "$f" ;;
  esac
done
echo >> "$REPORT"

echo "## Files in core/" >> "$REPORT"
find core -maxdepth 1 -type f | sort | while read -r f; do
  case "$f" in
    *.rs) audit_rust "$f" ;;
    *.py) audit_py "$f" ;;
    *.yaml|*.yml|*.md|*.toml) audit_other "$f" ;;
    *) audit_other "$f" ;;
  esac
done
echo >> "$REPORT"

echo "## Quick checks" >> "$REPORT"
{
  echo '```'
  cargo --version 2>/dev/null || true
  python3 --version 2>/dev/null || true
  echo '```'
  echo
} >> "$REPORT"

if [ -f Cargo.toml ]; then
  echo "### cargo check" >> "$REPORT"
  ( cargo check 2>&1 || true ) | sed 's/^/    /' >> "$REPORT"
  echo >> "$REPORT"
fi

# Python syntax check
: > py_err.log || true
find core modules -name '*.py' -print0 | xargs -0 -I{} sh -c 'python3 -m py_compile "{}" 2>>py_err.log' || true
if [ -s py_err.log ]; then
  echo "### python syntax errors" >> "$REPORT"
  sed 's/^/    /' py_err.log >> "$REPORT"
  echo >> "$REPORT"
fi

echo "Done -> $REPORT"

```

### FILE: /root/logos_lrb/tools/make_admin_jwt.py
```
#!/usr/bin/env python3
import os, time, hmac, hashlib, base64, json

def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

secret = os.environ.get("LRB_JWT_SECRET", "")
if not secret:
    raise SystemExit("need LRB_JWT_SECRET in env")

# минимальный payload: роль admin + срок
now = int(time.time())
payload = {
    "role": "admin",
    "iat": now,
    "exp": now + 3600,  # 1 час
}

header = {"alg": "HS256", "typ": "JWT"}

h = b64url(json.dumps(header, separators=(",",":")).encode())
p = b64url(json.dumps(payload, separators=(",",":")).encode())
msg = f"{h}.{p}".encode()

sig = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
token = f"{h}.{p}.{b64url(sig)}"
print(token)

```

### FILE: /root/logos_lrb/tools/make_airdrop_bots_book.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP_NAME="LOGOS_AIRDROP_BOTS_BOOK_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_AIRDROP_BOTS_BOOK/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_AIRDROP_BOTS_BOOK"

echo "# LOGOS Airdrop Bots Book (TG + X + API + Front + Infra)" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
    ! -name "*.bak" \
    ! -name "*.bak.*" \
  | sort | while read -r FILE; do
        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$FILE\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py) LANG="python" ;;
          rs) LANG="rust" ;;
          toml) LANG="toml" ;;
          yml|yaml) LANG="yaml" ;;
          sh) LANG="bash" ;;
          md) LANG="markdown" ;;
          json) LANG="json" ;;
          service|socket|conf) LANG="ini" ;;
          *) LANG="" ;;
        esac

        [ -n "$LANG" ] && echo "\`\`\`$LANG" >> "$OUT" || echo "\`\`\`" >> "$OUT"
        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`ini" >> "$OUT"
  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1) TG bot (боевой сервисный путь)
dump_dir "/opt/logos/airdrop-tg-bot" "Telegram Airdrop Bot (deployed)"

# 2) Airdrop API backend (боевой)
dump_dir "/opt/logos/airdrop-api" "Airdrop API (deployed)"

# 3) X Guard исходники (в репозитории)
dump_dir "/root/logos_lrb/modules/x_guard" "X Guard Module Source (modules/x_guard)"

# 4) systemd units
dump_file "/etc/systemd/system/logos-airdrop-tg-bot.service" "systemd: logos-airdrop-tg-bot.service"
dump_file "/etc/systemd/system/logos-airdrop-api.service"    "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"        "systemd: logos-x-guard.service"

# 5) nginx (маршрутизация API/ботов/фронта)
dump_file "/etc/nginx/sites-available/logos.conf" "nginx: logos.conf"

# ==== AIRDROP FRONT (HTML) ====
dump_file "/var/www/logos/landing/airdrop.html" "front: /var/www/logos/landing/airdrop.html"
dump_file "/var/www/logos/landing/landing/airdrop.html" "front: /var/www/logos/landing/landing/airdrop.html"

# ==== AIRDROP SHARED (MASTER) ====
dump_file "/opt/logos/www/shared/airdrop.css" "shared: airdrop.css"
dump_file "/opt/logos/www/shared/airdrop.js" "shared: airdrop.js"
dump_file "/opt/logos/www/shared/airdrop-fix.js" "shared: airdrop-fix.js"
dump_file "/opt/logos/www/shared/airdrop-x.js" "shared: airdrop-x.js"
dump_file "/opt/logos/www/shared/i18n.js" "shared: i18n.js"
dump_file "/opt/logos/www/shared/tweetnacl.min.js" "shared: tweetnacl.min.js"

# ==== AIRDROP SHARED COPIES IN LANDING ====
dump_file "/var/www/logos/landing/shared/airdrop-fix.js" "landing shared copy: airdrop-fix.js"
dump_file "/var/www/logos/landing/landing/shared/airdrop-fix.js" "landing/landing shared copy: airdrop-fix.js"


echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_airdrop_verifiers_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP_NAME="LOGOS_AIRDROP_VERIFIERS_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_AIRDROP_VERIFIERS/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_AIRDROP_VERIFIERS"

echo "# LOGOS Airdrop Verifiers Snapshot (TG + X/Twitter + Airdrop API)" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
    ! -name "*.bak" \
    ! -name "*.bak.*" \
  | sort | while read -r FILE; do
        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$FILE\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py) LANG="python" ;;
          rs) LANG="rust" ;;
          toml) LANG="toml" ;;
          yml|yaml) LANG="yaml" ;;
          sh) LANG="bash" ;;
          md) LANG="markdown" ;;
          json) LANG="json" ;;
          service|socket|conf) LANG="ini" ;;
          *) LANG="" ;;
        esac

        [ -n "$LANG" ] && echo "\`\`\`$LANG" >> "$OUT" || echo "\`\`\`" >> "$OUT"
        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`ini" >> "$OUT"
  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1) TG bot (боевой сервисный путь)
dump_dir "/opt/logos/airdrop-tg-bot" "Telegram Airdrop Bot (deployed)"

# 2) Airdrop API backend (боевой)
dump_dir "/opt/logos/airdrop-api" "Airdrop API (deployed)"

# 3) X Guard исходники (в репозитории)
dump_dir "/root/logos_lrb/modules/x_guard" "X Guard Module Source (modules/x_guard)"

# 4) systemd units
dump_file "/etc/systemd/system/logos-airdrop-tg-bot.service" "systemd: logos-airdrop-tg-bot.service"
dump_file "/etc/systemd/system/logos-airdrop-api.service"    "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"        "systemd: logos-x-guard.service"

# 5) nginx (маршрутизация API/ботов/фронта)
dump_file "/etc/nginx/sites-available/logos.conf" "nginx: logos.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_block_producer_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_BLOCK_PRODUCER_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_BLOCK_PRODUCER/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_BLOCK_PRODUCER"

echo "# LOGOS Block Producer Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/data.sled/*" \
    ! -path "*/data.sled.*/*" \
    ! -path "*/bridge_journal.sled/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          rs)          LANG="rust" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    toml)                LANG="toml" ;;
    yml|yaml)            LANG="yaml" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Ядро блокчейна: всё, где живут ledger, mempool, engine, producer
dump_dir "/root/logos_lrb/lrb_core" "LRB Core (ledger, mempool, engine, block producer)"

# 2. Нода: main.rs, API, архив, метрики — всё, что завязано на продюсере
dump_dir "/root/logos_lrb/node" "Node (REST, producer loop, archive, metrics)"

# 3. Конфиги сети и генезиса
dump_dir "/root/logos_lrb/configs" "Configs (genesis, logos_config)"

# 4. Инфраструктура для ноды (если есть шаблоны)
dump_dir "/root/logos_lrb/infra" "Infra (node-related infra configs)"

# 5. Инструменты для тестирования продюсера (бенчи)
dump_dir "/root/logos_lrb/tools" "Tools (benchmarks, tx generators, helpers)"

# 6. systemd-юниты и overrides для ноды
dump_file "/etc/systemd/system/logos-node@.service" "systemd: logos-node@.service"
dump_dir  "/etc/systemd/system/logos-node@.service.d" "systemd overrides: logos-node@.service.d"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_book_and_push.sh
```
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="/root/logos_lrb"
cd "$REPO_ROOT"

STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
BOOK="docs/LOGOS_LRB_FULL_BOOK_${STAMP}.md"

# ---- helper: pretty header
h() { echo -e "\n---\n\n## $1\n"; }

# ---- repo meta
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'detached')"
GIT_SHA="$(git rev-parse --short=12 HEAD 2>/dev/null || echo 'unknown')"
GIT_REMOTE="$(git remote get-url origin 2>/dev/null || echo 'no-remote')"

# ---- clean lists (без мусора)
# исключаем build-артефакты: target, node_modules, venv, dist, .git и пр.
EXCLUDES='
  -path */target -prune -o
  -path */node_modules -prune -o
  -path */.git -prune -o
  -path */.venv -prune -o
  -path */venv -prune -o
  -path */dist -prune -o
  -path */build -prune -o
  -path */.idea -prune -o
  -path */.vscode -prune -o
'

# ---- список корней проектов
ROOTS_FILE="docs/snapshots/REPO_ROOTS_${STAMP}.txt"
mkdir -p docs/snapshots
{
  find . $EXCLUDES -type f -name Cargo.toml -printf '%h\n'
  find . $EXCLUDES -type f -name pyproject.toml -printf '%h\n'
  find . $EXCLUDES -type f -name package.json -printf '%h\n'
  printf '%s\n' \
    configs configs/env \
    infra/nginx infra/systemd \
    lrb_core node modules www tools scripts docs
} | sed 's#^\./##' | sort -u > "$ROOTS_FILE"

# ---- begin book
{
  echo "# LOGOS LRB — FULL BOOK (${STAMP})"
  echo
  echo "**Branch:** ${GIT_BRANCH}  "
  echo "**Commit:** ${GIT_SHA}  "
  echo "**Remote:** ${GIT_REMOTE}"
  h "Структура репозитория (чистая, без артефактов)"
  echo '```text'
  # печатаем дерево только до 4 уровней и без мусора
  find . $EXCLUDES -type d \( -name .git -o -name target -o -name node_modules -o -name dist -o -name build -o -name .venv -o -name venv \) -prune -false -o -type d -print \
    | sed 's#^\./##' \
    | awk -F/ 'NF<=4' \
    | sort
  echo '```'

  h "Рабочие модули и пакеты (Cargo/Python/JS)"
  echo '```text'
  cat "$ROOTS_FILE"
  echo '```'

  h "Rust workspace (manifestы)"
  find . $EXCLUDES -type f -name Cargo.toml -print \
    | sed 's#^\./##' | sort \
    | while read -r f; do
        echo -e "\n### \`$f\`\n"
        echo '```toml'
        sed -n '1,200p' "$f"
        echo '```'
      done

  h "Конфиги (genesis, logos_config, env-примеры)"
  for f in $(find configs -maxdepth 2 -type f \( -name '*.yaml' -o -name '*.yml' -o -name '*.env' -o -name '*.toml' \) | sort); do
    echo -e "\n### \`$f\`\n"
    echo '```'
    sed -n '1,300p' "$f"
    echo '```'
  done

  h "Инфраструктура: systemd и Nginx"
  for f in $(find infra/systemd -type f -name '*.service' -o -name '*.conf' 2>/dev/null | sort); do
    echo -e "\n### \`$f\`\n"
    echo '```ini'; sed -n '1,300p' "$f"; echo '```'
  done
  for f in $(find infra/nginx -type f \( -name '*.conf' -o -name '*.snippets' \) 2>/dev/null | sort); do
    echo -e "\n### \`$f\`\n"
    echo '```nginx'; sed -n '1,300p' "$f"; echo '```'
  done

  h "OpenAPI (узел /node)"
  if [ -f node/src/openapi/openapi.json ]; then
    echo "**Файл:** node/src/openapi/openapi.json  "
    echo -n "**SHA256:** "
    sha256sum node/src/openapi/openapi.json | awk '{print $1}'
    echo
    echo '```json'
    sed -n '1,400p' node/src/openapi/openapi.json
    echo '```'
  else
    echo "_openapi.json не найден_"
  fi

  h "Метрики и health-ручки (докстринги/описания)"
  grep -Rsn --include='*.rs' -E 'logos_(http|head|finalized|blocks|tx_|bridge|archive)' node 2>/dev/null | sed 's#^\./##' | head -n 400 | sed 's/^/    /'

  h "Скрипты деплоя (канон)"
  for f in $(ls -1 scripts/*.sh 2>/dev/null || true); do
    echo -e "\n### \`$f\`\n"
    echo '```bash'; sed -n '1,200p' "$f"; echo '```'
  done

  h "Суммы и размеры ключевых артефактов"
  echo '```text'
  for f in node/src/openapi/openapi.json configs/genesis.yaml configs/logos_config.yaml; do
    [ -f "$f" ] || continue
    printf "%-40s  %10s  %s\n" "$f" "$(stat -c%s "$f" 2>/dev/null)" "$(sha256sum "$f" | awk '{print $1}')"
  done
  echo '```'

} > "$BOOK"

# аккуратная подсветка завершения
wc -l "$BOOK" | awk '{printf "\nFULL_BOOK lines: %s\n", $1}'
ls -lh "$BOOK"

# ---- git add & push (openapi.json тоже как в каноне)
git add "$BOOK"
[ -f node/src/openapi/openapi.json ] && git add node/src/openapi/openapi.json || true

COMMIT_MSG="docs: FULL BOOK (prod snapshot; canon-aligned structure; clean tree; openapi)"
git commit -m "$COMMIT_MSG" || echo "Nothing to commit (already up to date)."
git push

```

### FILE: /root/logos_lrb/tools/make_bots_stack_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SNAP_NAME="LOGOS_BOTS_STACK_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_BOTS_STACK/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_BOTS_STACK"

echo "# LOGOS Bots Stack Snapshot (TG + X Guard + Airdrop API)" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
    ! -name "*.bak" \
    ! -name "*.bak.*" \
  | sort | while read -r FILE; do
        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$FILE\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py) LANG="python" ;;
          rs) LANG="rust" ;;
          toml) LANG="toml" ;;
          yml|yaml) LANG="yaml" ;;
          sh) LANG="bash" ;;
          md) LANG="markdown" ;;
          json) LANG="json" ;;
          service|socket|conf) LANG="ini" ;;
          *) LANG="" ;;
        esac

        [ -n "$LANG" ] && echo "\`\`\`$LANG" >> "$OUT" || echo "\`\`\`" >> "$OUT"
        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`ini" >> "$OUT"
  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1) TG bot (боевой сервисный путь)
dump_dir "/opt/logos/airdrop-tg-bot" "Telegram Airdrop Bot (deployed)"

# 2) Airdrop API backend (боевой)
dump_dir "/opt/logos/airdrop-api" "Airdrop API (deployed)"

# 3) X Guard исходники (в репозитории)
dump_dir "/root/logos_lrb/modules/x_guard" "X Guard Module Source (modules/x_guard)"

# 4) systemd units
dump_file "/etc/systemd/system/logos-airdrop-tg-bot.service" "systemd: logos-airdrop-tg-bot.service"
dump_file "/etc/systemd/system/logos-airdrop-api.service"    "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"        "systemd: logos-x-guard.service"

# 5) nginx (маршрутизация API/ботов/фронта)
dump_file "/etc/nginx/sites-available/logos.conf" "nginx: logos.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_codebook.sh
```
#!/usr/bin/env sh
# LOGOS LRB — FULL LIVE book: repo + infra в один TXT (с маскировкой секретов)
set -eu

ROOT="$(cd "$(dirname "$0")/.."; pwd)"
OUT_DIR="docs"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
OUT_FILE_TMP="${OUT_DIR}/LRB_FULL_LIVE_${STAMP}.txt.tmp"
OUT_FILE="${OUT_DIR}/LRB_FULL_LIVE_${STAMP}.txt"
SIZE_LIMIT="${SIZE_LIMIT:-2000000}"   # 2 MB per file
REPO_ROOT="/root/logos_lrb"

# --- ВКЛЮЧАЕМ ИЗ РЕПО ---
REPO_GLOBS='
Cargo.toml
README.md
src
lrb_core/src
node/src
modules
core
wallet-proxy
docs
www/wallet
www/explorer
infra/nginx
infra/systemd
scripts
tools
configs
'

# --- ВКЛЮЧАЕМ ИНФРУ С СЕРВЕРА ---
INFRA_FILES='
/etc/nginx/nginx.conf
/etc/nginx/conf.d/*.conf
/etc/nginx/sites-enabled/*
/etc/systemd/system/logos-node.service
/etc/systemd/system/*.service
/etc/systemd/system/*.timer
/etc/systemd/system/logos-node.service.d/*.conf
/etc/prometheus/prometheus.yml
/etc/prometheus/rules/*.yml
/etc/alertmanager/alertmanager.yml
/etc/alertmanager/secrets.env
/etc/grafana/grafana.ini
/etc/grafana/provisioning/datasources/*.yaml
/etc/grafana/provisioning/dashboards/*.yaml
/var/lib/grafana/dashboards/*.json
/opt/logos/www/wallet/*
/opt/logos/www/explorer/*
'

# --- ИСКЛЮЧЕНИЯ ДЛЯ РЕПО ---
EXCLUDES_REPO='
.git
target
node_modules
venv
__pycache__
*.pyc
data.sled
var
*.log
*.pem
*.der
*.crt
*.key
*.zip
*.tar
*.tar.gz
*.7z
LOGOS_LRB_FULL_BOOK.md
'

# язык для подсветки
lang_for() {
  case "${1##*.}" in
    rs) echo "rust" ;; toml) echo "toml" ;; json) echo "json" ;;
    yml|yaml) echo "yaml" ;; sh|bash) echo "bash" ;; py) echo "python" ;;
    js) echo "javascript" ;; ts) echo "typescript" ;; tsx|jsx) echo "tsx" ;;
    html|htm) echo "html" ;; css) echo "css" ;; md) echo "markdown" ;;
    conf|ini|service|timer|env) echo "" ;; *) echo "" ;;
  esac
}

# доверяем расширению, иначе grep -Iq
looks_text() {
  case "$1" in
    *.rs|*.toml|*.json|*.yml|*.yaml|*.sh|*.bash|*.py|*.js|*.ts|*.tsx|*.jsx|*.html|*.htm|*.css|*.md|*.conf|*.ini|*.service|*.timer|*.env) return 0;;
    *) LC_ALL=C grep -Iq . "$1";;
  esac
}

# фильтр исключений репо
should_exclude_repo() {
  f="$1"
  # с двоеточиями — мусор от редакторов
  echo "$f" | grep -q ":" && return 0
  echo "$EXCLUDES_REPO" | while IFS= read -r pat; do
    [ -z "$pat" ] && continue
    [ "${pat#\#}" != "$pat" ] && continue
    case "$f" in */$pat/*|*/$pat|$pat) exit 0;; esac
  done; return 1
}

# маска секретов
mask_secrets() {
  sed -E \
    -e 's/(TELEGRAM_BOT_TOKEN=)[A-Za-z0-9:_-]+/\1***MASKED***/g' \
    -e 's/(TELEGRAM_CHAT_ID=)[0-9-]+/\1***MASKED***/g' \
    -e 's/(LRB_ADMIN_KEY=)[A-Fa-f0-9]+/\1***MASKED***/g' \
    -e 's/(LRB_BRIDGE_KEY=)[A-Fa-f0-9]+/\1***MASKED***/g' \
    -e 's/(LRB_ADMIN_JWT_SECRET=)[A-Za-z0-9._-]+/\1***MASKED***/g'
}

write_header() {
  {
    echo "# FULL LIVE SNAPSHOT — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "# sources: $REPO_ROOT + infra (/etc, /opt)"
    echo "# size limit per file: ${SIZE_LIMIT} bytes"
    echo
  } >>"$OUT_FILE_TMP"
}

dump_file() {
  f="$1"
  [ -f "$f" ] || return 0
  echo "$f" | grep -q ":" && return 0     # отсекаем мусорные имена

  sz="$(wc -c <"$f" | tr -d ' ' || echo 0)"
  [ "$sz" -eq 0 ] && { printf "\n## FILE: %s  (SKIPPED, empty)\n" "$f" >>"$OUT_FILE_TMP"; return 0; }
  [ "$sz" -gt "$SIZE_LIMIT" ] && { printf "\n## FILE: %s  (SKIPPED, size=%sb > limit)\n" "$f" "$sz" >>"$OUT_FILE_TMP"; return 0; }

  printf "\n## FILE: %s  (size=%sb)\n" "$f" "$sz" >>"$OUT_FILE_TMP"
  if looks_text "$f"; then
    printf '```\n' >>"$OUT_FILE_TMP"
    case "$f" in
      */alertmanager/secrets.env|*/logos-node.service.d/*|*/nginx/*.conf|*/conf.d/*.conf|*/sites-enabled/*|*/prometheus*.yml|*/grafana/*.ini|*/provisioning/*|*/dashboards/*.json)
        mask_secrets < "$f" >>"$OUT_FILE_TMP" ;;
      *) cat "$f" >>"$OUT_FILE_TMP" ;;
    esac
    printf '\n```\n' >>"$OUT_FILE_TMP"
  else
    printf "\n(SKIPPED, binary/non-text)\n" >>"$OUT_FILE_TMP"
  fi
}

collect_repo() {
  echo "$REPO_GLOBS" | while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    [ "${rel#\#}" != "$rel" ] && continue
    p="$REPO_ROOT/$rel"
    if [ -d "$p" ]; then find "$p" -type f; elif [ -f "$p" ]; then echo "$p"; fi
  done
}

collect_infra() {
  echo "$INFRA_FILES" | while IFS= read -r pat; do
    [ -z "$pat" ] && continue
    [ "${pat#\#}" != "$pat" ] && continue
    for f in $pat; do [ -f "$f" ] && echo "$f"; done
  done
}

main() {
  mkdir -p "$OUT_DIR"
  : >"$OUT_FILE_TMP"
  write_header

  collect_repo  | sort -u | while IFS= read -r p; do
    if should_exclude_repo "$p"; then continue; fi
    dump_file "$p"
  done

  collect_infra | sort -u | while IFS= read -r p; do
    dump_file "$p"
  done

  mv -f "$OUT_FILE_TMP" "$OUT_FILE"
  echo "✅ created: $OUT_FILE"
  cp -f "$OUT_FILE" "${ROOT}/LOGOS_LRB_FULL_BOOK.md" 2>/dev/null || true
}

main "$@"

```

### FILE: /root/logos_lrb/tools/make_deploy_infra_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_DEPLOY_INFRA_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_DEPLOY_INFRA/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_DEPLOY_INFRA"

echo "# LOGOS Deploy + Infra Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.toml" -o \
      -name "*.json" -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          sh)          LANG="bash" ;;
          md)          LANG="markdown" ;;
          yml|yaml)    LANG="yaml" ;;
          toml)        LANG="toml" ;;
          json)        LANG="json" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    yml|yaml)            LANG="yaml" ;;
    toml)                LANG="toml" ;;
    sh)                  LANG="bash" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Скрипты деплоя/запуска
dump_dir "/root/logos_lrb/scripts" "Deploy/Bootstrap Scripts (scripts/)"

# 2. Инфраструктура (шаблоны, инфра-файлы)
dump_dir "/root/logos_lrb/infra" "Infra (infra/)"

# 3. systemd-юниты LOGOS
dump_file "/etc/systemd/system/logos-node@.service"        "systemd: logos-node@.service"
dump_dir  "/etc/systemd/system/logos-node@.service.d"      "systemd overrides: logos-node@.service.d"
dump_file "/etc/systemd/system/logos-airdrop-api.service"  "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"      "systemd: logos-x-guard.service"

# 4. nginx-конфиги LOGOS
dump_file "/etc/nginx/sites-available/logos.conf"          "nginx: logos.conf"
dump_file "/etc/nginx/sites-available/logos_front"         "nginx: logos_front"
dump_file "/etc/nginx/sites-available/logos-node-8000.conf" "nginx: logos-node-8000.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_explorer_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_EXPLORER_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_EXPLORER/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_EXPLORER"

echo "# LOGOS Explorer Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          html|htm)    LANG="html" ;;
          js)          LANG="javascript" ;;
          ts)          LANG="typescript" ;;
          css)         LANG="css" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Explorer frontend (предполагаем /www/explorer/*)
dump_dir "/root/logos_lrb/www/explorer" "Explorer Frontend (sources)"

# 2. nginx-конфиги, связанные с explorer/API ноды
dump_file "/etc/nginx/sites-available/logos.conf"           "nginx: logos.conf"
dump_file "/etc/nginx/sites-available/logos_front"          "nginx: logos_front"
dump_file "/etc/nginx/sites-available/logos-node-8000.conf" "nginx: logos-node-8000.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_front_stack_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_FRONT_STACK_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_FRONT_STACK/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_FRONT_STACK"

echo "# LOGOS Front Stack Snapshot (Wallet + Explorer + Landing + Airdrop)" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          html|htm)    LANG="html" ;;
          js)          LANG="javascript" ;;
          ts)          LANG="typescript" ;;
          css)         LANG="css" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    yml|yaml)            LANG="yaml" ;;
    toml)                LANG="toml" ;;
    sh)                  LANG="bash" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Wallet + Explorer frontend (sources)
dump_dir "/root/logos_lrb/www/wallet"   "Wallet Frontend (www/wallet)"
dump_dir "/root/logos_lrb/www/explorer" "Explorer Frontend (www/explorer)"

# 2. Wallet-proxy backend (sources + deployed)
dump_dir "/root/logos_lrb/wallet-proxy" "Wallet Proxy Backend (sources)"
dump_dir "/opt/logos/wallet-proxy"      "Wallet Proxy Backend (deployed code)"

# 3. Landing + Airdrop frontend + TG-bot
dump_dir "/var/www/logos/landing"                               "Landing + Airdrop Frontend"
dump_dir "/var/www/logos/landing/logos_tg_bot/logos_guard_bot"  "Telegram Guard Bot"

# 4. Airdrop API backend
dump_dir "/opt/logos/airdrop-api" "Airdrop API Backend"

# 5. X Guard (Twitter guard for airdrop)
dump_dir "/root/logos_lrb/modules/x_guard" "X Guard Module (modules/x_guard)"

# 6. systemd + nginx, связанные с этим фронт-стеком
dump_file "/etc/systemd/system/logos-airdrop-api.service" "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"     "systemd: logos-x-guard.service"

dump_file "/etc/nginx/sites-available/logos.conf"          "nginx: logos.conf"
dump_file "/etc/nginx/sites-available/logos_front"         "nginx: logos_front"
dump_file "/etc/nginx/sites-available/logos-node-8000.conf" "nginx: logos-node-8000.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_full_book.sh
```
#!/usr/bin/env bash
set -euo pipefail

# Hardening locale and PATH
export LC_ALL=C LANG=C
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

REPO="/root/logos_lrb"
cd "$REPO"

STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
BOOK="docs/LOGOS_LRB_FULL_BOOK_${STAMP}.md"
ROOTS_FILE="docs/snapshots/REPO_ROOTS_${STAMP}.txt"

# Clean file list (NO parentheses, NO eval)
FILES=$(
  find . -type f \
    -not -path "./.git/*" \
    -not -path "./.git" \
    -not -path "*/target/*" \
    -not -path "*/node_modules/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -not -path "*/.venv/*" \
    -not -path "*/venv/*" \
  | sed 's#^\./##' | sort
)

# Project roots (Cargo/Python/JS) + fixed directories
{
  find . -type f -name Cargo.toml \
    -not -path "./.git/*" -not -path "*/target/*" -not -path "*/node_modules/*" \
    -not -path "*/dist/*"  -not -path "*/build/*"  -not -path "*/.venv/*" -not -path "*/venv/*" \
    -printf '%h\n'
  find . -type f -name pyproject.toml \
    -not -path "./.git/*" -not -path "*/target/*" -not -path "*/node_modules/*" \
    -not -path "*/dist/*"  -not -path "*/build/*"  -not -path "*/.venv/*" -not -path "*/venv/*" \
    -printf '%h\n'
  find . -type f -name package.json \
    -not -path "./.git/*" -not -path "*/target/*" -not -path "*/node_modules/*" \
    -not -path "*/dist/*"  -not -path "*/build/*"  -not -path "*/.venv/*" -not -path "*/venv/*" \
    -printf '%h\n'
  printf '%s\n' configs configs/env infra/nginx infra/systemd lrb_core node modules www tools scripts docs
} | sed 's#^\./##' | sort -u > "$ROOTS_FILE"

# Header
{
  echo "# LOGOS LRB — FULL BOOK (${STAMP})"
  echo
  echo "**Branch:** $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo detached)  "
  echo "**Commit:** $(git rev-parse --short=12 HEAD 2>/dev/null || echo unknown)  "
  echo "**Remote:** $(git remote get-url origin 2>/dev/null || echo none)"
  echo
  echo "---"
  echo
  echo "## Repository Structure (clean, no artifacts)"
  echo '```text'
  find . -type d \
    -not -path "./.git/*" -not -path "./.git" \
    -not -path "*/target/*" -not -path "*/node_modules/*" \
    -not -path "*/dist/*"  -not -path "*/build/*" \
    -not -path "*/.venv/*" -not -path "*/venv/*" \
  | sed 's#^\./##' | awk -F/ 'NF<=6' | sort
  echo '```'
  echo
  echo "## Project Roots (Cargo/Python/JS)"
  echo '```text'
  cat "$ROOTS_FILE"
  echo '```'
  echo
  echo "## Full File Contents"
} > "$BOOK"

# Embed every file (text: full, binary: only hash+size)
for f in $FILES; do
  # Skip previous books
  case "$f" in
    docs/LOGOS_LRB_FULL_BOOK_*) continue ;;
  esac

  SIZE=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
  SHA=$( (sha256sum "$f" 2>/dev/null || shasum -a 256 "$f" 2>/dev/null) | awk '{print $1}' )

  if grep -Iq . "$f" 2>/dev/null; then
    {
      echo
      echo "### \`$f\`"
      echo
      [ -n "$SHA" ] && echo "**SHA256:** $SHA  |  **size:** ${SIZE} bytes**"
      echo
      echo '```'
      cat "$f"
      echo
      echo '```'
    } >> "$BOOK"
  else
    {
      echo
      echo "### \`$f\` (binary)"
      echo
      [ -n "$SHA" ] && echo "**SHA256:** $SHA  |  **size:** ${SIZE} bytes**"
    } >> "$BOOK"
  fi
done

# Footer
{
  echo
  echo "---"
  echo
  echo "## Summary"
  echo "- Total files: $(printf '%s\n' $FILES | wc -l)"
  echo "- Book SHA256: $( (sha256sum "$BOOK" 2>/dev/null || shasum -a 256 "$BOOK" 2>/dev/null) | awk '{print $1}')"
} >> "$BOOK"

# Git push
git add "$BOOK" || true
[ -f node/src/openapi/openapi.json ] && git add node/src/openapi/openapi.json || true
git commit -m "docs: FULL BOOK (complete snapshot; all text files included; binaries hashed)" || true
git push

# Output
wc -l "$BOOK" || true
ls -lh "$BOOK" || true

```

### FILE: /root/logos_lrb/tools/make_full_snapshot_live.sh
```
#!/usr/bin/env bash
set -euo pipefail

OUTDIR="${OUTDIR:-/root/logos_snapshot}"
STAMP=$(date +%Y%m%d_%H%M)
OUT="$OUTDIR/LRB_FULL_LIVE_${STAMP}.txt"
MAX=${MAX:-800000}  # макс размер включаемого файла (байт)

mkdir -p "$OUTDIR"

say(){ echo "$@" >&2; }
add_head(){
  echo -e "\n\n## FILE: $1  (size=${2}b)\n\`\`\`" >> "$OUT"
}
add_tail(){
  echo -e "\n\`\`\`" >> "$OUT"
}

# Источники (живые пути)
SRC_LIST=(
  "/root/logos_lrb"                   # весь код репо
  "/opt/logos/www/wallet"             # кошелёк
  "/etc/systemd/system/logos-node@.service"
  "/etc/systemd/system/logos-healthcheck.service"
  "/etc/systemd/system/logos-healthcheck.timer"
  "/etc/nginx/sites-available/logos-api-lb.conf"
  "/usr/local/bin/logos_healthcheck.sh"
)

# Заголовок
{
  echo "# FULL LIVE SNAPSHOT — $(date -u +%FT%TZ)"
  echo "# sources:"
  for s in "${SRC_LIST[@]}"; do echo "#  - $s"; done
  echo "# size limit per file: ${MAX} bytes"
  echo
} > "$OUT"

# Вспомогательные функции
is_text(){
  # бинарники/картинки отсекаем простым тестом: попытка вывести «без нулевых байтов»
  # или используем file(1) если есть
  if command -v file >/dev/null 2>&1; then
    file -b --mime "$1" | grep -qiE 'text|json|xml|yaml|toml|javascript|html|css' && return 0 || return 1
  else
    grep -Iq . "$1" && return 0 || return 1
  fi
}

emit_file(){
  local f="$1"
  [ -f "$f" ] || return 0
  # исключения
  case "$f" in
    *.pem|*.key|*.crt|*.p12|*.so|*.bin|*.png|*.jpg|*.jpeg|*.gif|*.svg|*.woff|*.woff2|*.ttf) return 0;;
  esac
  local sz
  sz=$(stat -c%s "$f" 2>/dev/null || echo 0)
  if [ "$sz" -gt "$MAX" ]; then
    echo -e "\n\n## FILE: $f  (SKIPPED, size=${sz}b > ${MAX})" >> "$OUT"
    return 0
  fi
  if ! is_text "$f"; then
    echo -e "\n\n## FILE: $f  (SKIPPED, binary/non-text size=${sz}b)" >> "$OUT"
    return 0
  fi
  add_head "$f" "$sz"
  sed -e 's/\r$//' "$f" >> "$OUT"
  add_tail
}

# 1) Репозиторий: только текстовые файлы, игнорим target/node_modules/dist
if [ -d /root/logos_lrb ]; then
  say "[*] collecting /root/logos_lrb"
  cd /root/logos_lrb
  # берём отслеживаемые git'ом; если git недоступен — найдём все текстовые расширения
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git ls-files | while read -r f; do
      case "$f" in target/*|**/target/*|node_modules/*|dist/*) continue;; esac
      emit_file "/root/logos_lrb/$f"
    done
  else
    find . -type f ! -path "./target/*" ! -path "./node_modules/*" ! -path "./dist/*" \
      -regextype posix-extended -regex '.*\.(rs|toml|md|sh|bash|zsh|service|timer|conf|nginx|yaml|yml|json|ts|tsx|js|mjs|jsx|html|htm|css|go|py|proto|ini|cfg|txt)$' \
      -print0 | xargs -0 -I{} bash -c 'emit_file "{}"'
  fi
  cd - >/dev/null
fi

# 2) Статика кошелька
if [ -d /opt/logos/www/wallet ]; then
  say "[*] collecting /opt/logos/www/wallet"
  find /opt/logos/www/wallet -type f -print0 | while IFS= read -r -d '' f; do emit_file "$f"; done
fi

# 3) systemd units
for u in /etc/systemd/system/logos-node@.service /etc/systemd/system/logos-healthcheck.service /etc/systemd/system/logos-healthcheck.timer; do
  [ -f "$u" ] && emit_file "$u"
done

# 4) nginx site
[ -f /etc/nginx/sites-available/logos-api-lb.conf ] && emit_file /etc/nginx/sites-available/logos-api-lb.conf

# 5) healthcheck script
[ -f /usr/local/bin/logos_healthcheck.sh ] && emit_file /usr/local/bin/logos_healthcheck.sh

# 6) Живые .env → в слепок как обезличенные *.example
sanitize_env(){
  sed -E \
    -e 's/^(LRB_NODE_SK_HEX)=.*/\1=CHANGE_ME_64_HEX/' \
    -e 's/^(LRB_ADMIN_KEY)=.*/\1=CHANGE_ADMIN_KEY/' \
    -e 's/^(LRB_BRIDGE_KEY)=.*/\1=CHANGE_ME/' \
    -e 's/^(HOT_WALLET_PRIVATE_KEY)=.*/\1=CHANGE_ME/' \
    -e 's/^(TG_TOKEN)=.*/\1=CHANGE_ME/' \
    -e 's/^(TG_CHAT_ID)=.*/\1=CHANGE_ME/' \
    "$1"
}
if ls /etc/logos/node-*.env >/dev/null 2>&1; then
  for f in /etc/logos/node-*.env; do
    tmp="$(mktemp)"; sanitize_env "$f" > "$tmp"
    sz=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
    add_head "${f}.example" "$sz"
    cat "$tmp" >> "$OUT"
    add_tail
    rm -f "$tmp"
  done
fi

echo "[ok] wrote $OUT"

```

### FILE: /root/logos_lrb/tools/make_global_code_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

# Определяем корень проекта относительно самого скрипта
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"

SNAP_NAME="LOGOS_GLOBAL_CODE_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
mkdir -p "$ROOT_DIR/docs"
OUT="$ROOT_DIR/docs/$SNAP_NAME"

echo "# LOGOS Global Code Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "nginx.conf" -o -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/data.sled/*" \
    ! -path "*/data.sled.*/*" \
    ! -path "*/bridge_journal.sled/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.bak" \
    ! -name "*.backup" \
    ! -name "LOGOS_GLOBAL_CODE_SNAPSHOT_*.md" \
    ! -path "$OUT" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          rs)     LANG="rust" ;;
          toml)   LANG="toml" ;;
          yml|yaml) LANG="yaml" ;;
          sh)     LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          py)     LANG="python" ;;
          html|htm) LANG="html" ;;
          js)     LANG="javascript" ;;
          ts)     LANG="typescript" ;;
          css)    LANG="css" ;;
          md)     LANG="markdown" ;;
          json)   LANG="json" ;;
          *)      LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

# 1. Основной репозиторий LOGOS LRB (ядро, нода, модули, www, скрипты)
dump_dir "/root/logos_lrb" "LOGOS LRB Repository (core, node, modules, www, scripts)"

# 2. Веб / лэндинг / боты
dump_dir "/var/www/logos" "Web / Landing / Wallet / Explorer / Bots"

# 3. Опционально: опт-директории с конфигами/скриптами
dump_dir "/opt/logos"       "Opt LOGOS (binaries/configs/scripts)"
dump_dir "/opt/logos-agent" "Opt LOGOS Agent"
dump_dir "/opt/logos_node"  "Opt LOGOS Node (legacy)"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_LOGOS_FULL_BOOK.sh
```
#!/usr/bin/env bash
set -euo pipefail

OUT="docs/LOGOS_FULL_SYSTEM_BOOK.md"
rm -f "$OUT"

echo "# LOGOS — FULL SYSTEM BOOK" >> "$OUT"
echo "_Autogenerated: $(date -u '+%Y-%m-%d %H:%M:%SZ')_" >> "$OUT"
echo "" >> "$OUT"

section () {
  echo "" >> "$OUT"
  echo "## $1" >> "$OUT"
  echo "" >> "$OUT"
}

dump () {
  FILE="$1"
  TITLE="$2"
  if [ -f "$FILE" ]; then
    echo "### $TITLE" >> "$OUT"
    echo '```' >> "$OUT"
    sed 's/\x1b\[[0-9;]*m//g' "$FILE" >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"
  fi
}

dump_tree () {
  DIR="$1"
  TITLE="$2"
  if [ -d "$DIR" ]; then
    echo "### $TITLE" >> "$OUT"
    echo '```' >> "$OUT"
    tree -a "$DIR" -I '.git|target|node_modules|__pycache__|.venv|venv|logs|.cache' >> "$OUT"
    echo '```' >> "$OUT"
    echo "" >> "$OUT"
  fi
}

####################################
section "🧠 Blockchain Node (Rust)"

dump_tree "/root/logos_lrb" "Dev-core (logos_lrb)"
dump_tree "/opt/logos/bin" "Node binaries"
dump "/etc/systemd/system/logos-node.service" "systemd: logos-node"
dump "/etc/systemd/system/logos-node@.service" "systemd: logos-node@"

####################################
section "🛡 X Guard (Rust)"

dump_tree "/root/logos_lrb/modules/x_guard" "x_guard source"
dump "/etc/systemd/system/logos-x-guard.service" "systemd: logos-x-guard"

####################################
section "🤖 Airdrop (API + Telegram)"

dump_tree "/opt/logos/airdrop-api" "Airdrop API"
dump_tree "/opt/logos/airdrop-tg-bot" "Telegram bot"
dump "/etc/systemd/system/logos-airdrop-api.service" "systemd: airdrop-api"
dump "/etc/systemd/system/logos-airdrop-tg-bot.service" "systemd: airdrop-tg-bot"

####################################
section "🔁 Wallet Proxy + Scanner"

dump_tree "/opt/logos/wallet-proxy" "wallet-proxy"
dump "/etc/systemd/system/logos-wallet-proxy.service" "systemd: wallet-proxy"
dump "/etc/systemd/system/logos-wallet-scanner.service" "systemd: wallet-scanner"

####################################
section "🌐 Frontend (Landing / Wallet / Explorer)"

dump_tree "/var/www/logos" "Frontend tree"
dump_tree "/opt/logos/www/shared" "Shared JS/CSS"

####################################
section "🧱 Infra (systemd / env / data)"

dump_tree "/etc/logos" "ENV files (structure only)"
dump_tree "/var/lib/logos-main" "Node data"
dump_tree "/var/log/logos" "Logs"
dump_tree "/var/backups/logos" "Backups"

####################################
echo "✅ BOOK COMPLETE" >> "$OUT"

echo "Book written to $OUT"

```

### FILE: /root/logos_lrb/tools/make_LOGOS_FULL_SYSTEM_BOOK_V3_1.sh
```
#!/usr/bin/env bash
set -e

BASE="docs/LOGOS_FULL_SYSTEM_BOOK"
mkdir -p "$BASE"

write() {
  local out="$1"
  shift
  echo "# $out" > "$BASE/$out.md"
  for f in "$@"; do
    echo -e "\n---\n## $f\n" >> "$BASE/$out.md"
    sed 's/\x00//g' "$f" >> "$BASE/$out.md"
  done
}

# INDEX
cat > "$BASE/00_INDEX.md" <<EOF
# LOGOS — FULL SYSTEM BOOK

This is the complete canonical system snapshot.

Volumes:
1. Blockchain Node
2. Resonance Core (Λ0)
3. X-Guard
4. Airdrop
5. Wallet / Proxy
6. Frontend
7. Infra
8. Project Map
EOF

# NODE
write 01_BLOCKCHAIN_NODE \
  Cargo.toml Cargo.lock \
  $(find src -name '*.rs' | sort)

# RESONANCE
write 02_RESONANCE_CORE_L0 \
  $(find src -iname '*resonance*' -o -iname '*phase*' -o -iname '*Λ*')

# X-GUARD
write 03_X_GUARD \
  $(find src -iname '*guard*.rs')

# AIRDROP
write 04_AIRDROP_API_TG \
  $(find /opt/logos/airdrop-api -type f ! -path '*/.venv/*') \
  $(find /opt/logos/airdrop-tg-bot -type f ! -path '*/.venv/*')

# WALLET
write 05_WALLET_PROXY_SCANNER \
  $(find /opt/logos/wallet-proxy -type f ! -path '*/venv/*')

# FRONT
write 06_FRONTEND \
  $(find /var/www/logos -type f)

# INFRA
write 07_INFRA_SYSTEMD_ENV \
  $(find /etc/logos /etc/systemd/system -type f)

# MAP
find /root/logos_lrb /opt/logos /var/www/logos /etc/logos \
  -type d | sort > "$BASE/08_PROJECT_MAP.md"

echo "LOGOS FULL SYSTEM BOOK split complete."

```

### FILE: /root/logos_lrb/tools/make_LOGOS_FULL_SYSTEM_BOOK_V3.sh
```
#!/usr/bin/env bash
set -e

OUT="docs/LOGOS_FULL_SYSTEM_BOOK.md"
mkdir -p docs

echo "# LOGOS — FULL SYSTEM BOOK (V3)" > "$OUT"
echo "_Autogenerated: $(date -u)_\n" >> "$OUT"

dump() {
  local f="$1"
  echo -e "\n---\n## 📄 \`$f\`\n" >> "$OUT"
  sed 's/\x00//g' "$f" >> "$OUT"
}

dump_tree() {
  local dir="$1"
  echo -e "\n---\n## 📁 TREE: \`$dir\`\n" >> "$OUT"
  tree -a "$dir" >> "$OUT" || true
}

echo "## 🧠 BLOCKCHAIN NODE (RUST ядро, Λ0, RCP)" >> "$OUT"
dump Cargo.toml
dump Cargo.lock 2>/dev/null || true
dump_tree src
find src -type f -name '*.rs' | sort | while read f; do dump "$f"; done

echo "## 🛡 X-GUARD (Rust)" >> "$OUT"
find src -type f -iname '*guard*.rs' | while read f; do dump "$f"; done

echo "## 🔮 RESONANCE CORE / Λ0" >> "$OUT"
find src -type f \( -iname '*resonance*' -o -iname '*Λ*' -o -iname '*phase*' \) | while read f; do dump "$f"; done

echo "## 🤖 AIRDROP (API + TG BOT)" >> "$OUT"
dump_tree /opt/logos/airdrop-api
dump_tree /opt/logos/airdrop-tg-bot
find /opt/logos/airdrop-api /opt/logos/airdrop-tg-bot \
  -type f \( -name '*.py' -o -name '*.env' -o -name 'requirements.txt' -o -name 'pyproject.toml' \) \
  ! -path '*/.venv/*' | while read f; do dump "$f"; done

echo "## 🔁 WALLET / PROXY / SCANNER" >> "$OUT"
dump_tree /opt/logos/wallet-proxy
find /opt/logos/wallet-proxy \
  -type f \( -name '*.py' -o -name '*.env' \) \
  ! -path '*/venv/*' | while read f; do dump "$f"; done

echo "## 🌐 FRONTEND (Landing / Wallet / Explorer)" >> "$OUT"
dump_tree /var/www/logos
find /var/www/logos \
  -type f \( -name '*.html' -o -name '*.js' -o -name '*.css' \) \
  | while read f; do dump "$f"; done

echo "## 🧱 INFRA (systemd / env / ports)" >> "$OUT"
dump_tree /etc/logos
dump_tree /etc/systemd/system
find /etc/logos /etc/systemd/system \
  -type f \( -name '*.env' -o -name '*.service' -o -name '*.timer' \) \
  | while read f; do dump "$f"; done

echo "## ⚙️ TOOLS / SCRIPTS" >> "$OUT"
dump_tree tools
find tools -type f -name '*.sh' | while read f; do dump "$f"; done

echo "## 🗺 PROJECT MAP" >> "$OUT"
find /root/logos_lrb /opt/logos /var/www/logos /etc/logos \
  -type d -maxdepth 3 | sort >> "$OUT"

echo -e "\n---\n# ✅ END OF LOGOS FULL SYSTEM BOOK\n" >> "$OUT"

echo "Book written to $OUT"

```

### FILE: /root/logos_lrb/tools/make_mono_book.sh
```
#!/usr/bin/env bash
set -euo pipefail

OUT="docs/LOGOS_MONO_BOOK/LOGOS_MONO_BOOK.md"

ROOTS=(
  "/root/logos_lrb"
  "/opt/logos"
  "/var/www/logos"
  "/etc/logos"
)

MAX_BYTES=$((700*1024))  # 700KB на файл, чтобы не тащить тяжёлое

ALLOW_EXT_REGEX='\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$'
SKIP_NAME_REGEX='(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)'
SKIP_DIR_REGEX='/(\.git|target|node_modules|venv|\.venv|__pycache__|backups|snapshots|data\.sled\.bak)(/|$)'

is_sensitive_etc() {
  local f="$1"
  [[ "$f" == /etc/logos/* ]] || return 1
  local base; base="$(basename "$f")"
  [[ "$base" =~ \.key$ ]] && return 0
  [[ "$base" =~ \.rid$ ]] && return 0
  [[ "$base" == "keys.env" ]] && return 0
  [[ "$base" == "keys.envy" ]] && return 0
  [[ "$base" =~ ^node-.*\.env$ ]] && return 0
  [[ "$base" == "node-main.env" ]] && return 0
  [[ "$base" == "proxy.env" ]] && return 0
  [[ "$base" == "wallet-proxy.env" ]] && return 0
  [[ "$base" == "airdrop-api.env" ]] && return 0
  [[ "$base" == "logos_tg_bot.env" ]] && return 0
  return 1
}

is_env_nonexample() {
  local f="$1"
  [[ "$f" =~ \.env ]] || return 1
  [[ "$f" =~ \.example$ ]] && return 1
  [[ "$f" =~ \.sample$ ]] && return 1
  [[ "$f" =~ \.template$ ]] && return 1
  return 0
}

lang_hint() {
  local f="$1"
  case "${f##*.}" in
    rs) echo "rs" ;;
    py) echo "python" ;;
    sh) echo "bash" ;;
    toml) echo "toml" ;;
    yml|yaml) echo "yaml" ;;
    js|mjs|cjs) echo "javascript" ;;
    ts) echo "typescript" ;;
    tsx) echo "tsx" ;;
    html) echo "html" ;;
    css) echo "css" ;;
    json) echo "json" ;;
    md) echo "markdown" ;;
    *) echo "" ;;
  esac
}

mkdir -p "$(dirname "$OUT")"

{
  echo "# LOGOS — MONO BOOK (Full Snapshot)"
  echo
  echo "_Auto-generated clean structure + full source code. No backups, no binaries, no heavy._"
  echo
  echo "Generated (UTC): $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo
  echo "---"
  echo "## 1) STRUCTURE (Directories + Files)"
} > "$OUT"

for R in "${ROOTS[@]}"; do
  {
    echo
    if [[ ! -e "$R" ]]; then
      echo "### ROOT: $R (missing)"
      continue
    fi

    echo "### ROOT: $R"
    echo
    echo '```text'

    find "$R" -type d 2>/dev/null \
      | grep -Ev "$SKIP_DIR_REGEX" \
      | sort \
      | sed 's|^|DIR  |'

    find "$R" -type f 2>/dev/null \
      | grep -Ev "$SKIP_DIR_REGEX" \
      | grep -E  "$ALLOW_EXT_REGEX" \
      | grep -Ev "$SKIP_NAME_REGEX" \
      | sort \
      | sed 's|^|FILE |'

    echo '```'
  } >> "$OUT"
done

{
  echo
  echo "---"
  echo "## 2) MODULES (FULL SOURCE CODE)"
} >> "$OUT"

for R in "${ROOTS[@]}"; do
  [[ -e "$R" ]] || continue

  {
    echo
    echo "### ROOT: $R"
  } >> "$OUT"

  find "$R" -type f 2>/dev/null \
    | grep -Ev "$SKIP_DIR_REGEX" \
    | grep -E  "$ALLOW_EXT_REGEX" \
    | grep -Ev "$SKIP_NAME_REGEX" \
    | sort | while read -r f; do

      size=$(stat -c%s "$f" 2>/dev/null || echo 0)
      if (( size > MAX_BYTES )); then
        {
          echo
          echo "#### FILE: $f"
          echo "_SKIPPED: too large (${size} bytes > ${MAX_BYTES})._"
        } >> "$OUT"
        continue
      fi

      if is_sensitive_etc "$f"; then
        {
          echo
          echo "#### FILE: $f"
          echo "_REDACTED: sensitive file from /etc/logos._"
        } >> "$OUT"
        continue
      fi

      if is_env_nonexample "$f"; then
        {
          echo
          echo "#### FILE: $f"
          echo "_REDACTED: .env file (not example/sample)._"
        } >> "$OUT"
        continue
      fi

      mime=$(file -b --mime "$f" 2>/dev/null || true)
      if echo "$mime" | grep -qi 'charset=binary'; then
        {
          echo
          echo "#### FILE: $f"
          echo "_SKIPPED: binary mime ($mime)_"
        } >> "$OUT"
        continue
      fi

      lh=$(lang_hint "$f")
      {
        echo
        echo "#### FILE: $f"
        if [[ -n "$lh" ]]; then
          echo "```$lh"
        else
          echo '```'
        fi
        sed 's/\t/  /g' "$f"
        echo '```'
      } >> "$OUT"
    done
done

{
  echo
  echo "---"
  echo "## DONE"
  echo "Output: $OUT"
} >> "$OUT"

echo "✅ MONO BOOK READY: $OUT"
ls -lh "$OUT"

```

### FILE: /root/logos_lrb/tools/make_resonance_core_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_RESONANCE_CORE_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_RESONANCE_CORE/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_RESONANCE_CORE"

echo "# LOGOS Resonance Core + Modules Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.rs"   -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.md"   -o \
      -name "*.json" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/target/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          rs)          LANG="rust" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

# 1. Python core (резонанс, onboarding, rid, offline и т.п.)
dump_dir "/root/logos_lrb/core" "Python Resonance Core (core/)"

# 2. Все сервисные модули (включая x_guard, chaos_guard, env_impact и др.)
dump_dir "/root/logos_lrb/modules" "Service Modules (modules/)"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_stress_env.py
```
#!/usr/bin/env python3
import os
import secrets
from nacl.signing import SigningKey

ALPH = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

def b58enc(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n > 0:
        n, r = divmod(n, 58)
        out = ALPH[r] + out
    pad = 0
    for x in b:
        if x == 0: pad += 1
        else: break
    return ("1"*pad) + (out or "1")

def main():
    sk32 = secrets.token_bytes(32)
    sk_hex = sk32.hex()

    sk = SigningKey(sk32)
    pk = bytes(sk.verify_key)
    rid = b58enc(pk)

    to_rid = os.environ.get("LRB_TO_RID", "AxfsXECgnTiUN3qMeNmPUHJwCwwYKGTvVxcLvXsq734p")

    env_text = f"""# ==== AUTO-GENERATED TEST ENV ====
export LRB_NODE_URL="http://127.0.0.1:8080"
export LRB_FROM_RID="{rid}"
export LRB_SK_HEX="{sk_hex}"
export LRB_TO_RID="{to_rid}"

export LRB_STRESS_TOTAL=2000
export LRB_STRESS_PAR=8
export LRB_STRESS_AMOUNT=1
"""
    with open("stress-gen.env", "w", encoding="utf-8") as f:
        f.write(env_text)

    print("OK: stress-gen.env written")
    print("TEST FROM RID:", rid)

if __name__ == "__main__":
    main()

```

### FILE: /root/logos_lrb/tools/make_wallet_explorer_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_WALLET_EXPLORER_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_WALLET_EXPLORER/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_WALLET_EXPLORER"

echo "# LOGOS Wallet + Explorer Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          html|htm)    LANG="html" ;;
          js)          LANG="javascript" ;;
          ts)          LANG="typescript" ;;
          css)         LANG="css" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Frontend: wallet + explorer (исходники)
dump_dir "/root/logos_lrb/www" "Wallet + Explorer Frontend (sources)"

# 2. Wallet-proxy backend (исходники)
dump_dir "/root/logos_lrb/wallet-proxy" "Wallet Proxy Backend (sources)"

# 3. Wallet-proxy backend (боевой деплой, без venv/logs/db/env)
dump_dir "/opt/logos/wallet-proxy" "Wallet Proxy Backend (deployed code)"

# 4. Nginx configs, связанные с кошельком/эксплорером
dump_file "/etc/nginx/sites-available/logos.conf"         "nginx: logos.conf"
dump_file "/etc/nginx/sites-available/logos_front"        "nginx: logos_front"
dump_file "/etc/nginx/sites-available/logos-node-8000.conf" "nginx: logos-node-8000.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_wallet_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_WALLET_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_WALLET/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_WALLET"

echo "# LOGOS Wallet Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
    ! -name "*.env" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          html|htm)    LANG="html" ;;
          js)          LANG="javascript" ;;
          ts)          LANG="typescript" ;;
          css)         LANG="css" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Wallet frontend (предполагаем /www/wallet/*)
dump_dir "/root/logos_lrb/www/wallet" "Wallet Frontend (sources)"

# 2. Wallet-proxy backend (исходники)
dump_dir "/root/logos_lrb/wallet-proxy" "Wallet Proxy Backend (sources)"

# 3. Wallet-proxy backend (боевой код без venv/logs/db/env)
dump_dir "/opt/logos/wallet-proxy" "Wallet Proxy Backend (deployed code)"

# 4. nginx-конфиги, связанные с кошельком/эксплорером
dump_file "/etc/nginx/sites-available/logos.conf"           "nginx: logos.conf"
dump_file "/etc/nginx/sites-available/logos_front"          "nginx: logos_front"
dump_file "/etc/nginx/sites-available/logos-node-8000.conf" "nginx: logos-node-8000.conf"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/make_web_stack_snapshot.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SNAP_NAME="LOGOS_WEB_STACK_SNAPSHOT_$(date -u +%Y-%m-%dT%H-%M-%SZ).md"
OUT="$ROOT_DIR/docs/LOGOS_WEB_STACK/$SNAP_NAME"

mkdir -p "$ROOT_DIR/docs/LOGOS_WEB_STACK"

echo "# LOGOS Web Stack Snapshot" > "$OUT"
echo "" >> "$OUT"
echo "_Автогенерация: \`$(date -u "+%Y-%m-%d %H:%M:%SZ")\`_" >> "$OUT"
echo "" >> "$OUT"

dump_dir () {
  local DIR="$1"
  local TITLE="$2"

  if [ ! -d "$DIR" ]; then
    echo "- [WARN] directory not found: $DIR" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`$DIR\`" >> "$OUT"
  echo "" >> "$OUT"

  find "$DIR" \
    -type f \
    \( \
      -name "*.py"   -o \
      -name "*.html" -o -name "*.htm" -o \
      -name "*.js"   -o \
      -name "*.ts"   -o \
      -name "*.css"  -o \
      -name "*.md"   -o \
      -name "*.json" -o \
      -name "*.toml" -o \
      -name "*.yaml" -o -name "*.yml" -o \
      -name "*.sh"   -o \
      -name "*.service" -o -name "*.socket" -o \
      -name "*.conf" \
    \) \
    ! -path "*/.git/*" \
    ! -path "*/.venv/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/node_modules/*" \
    ! -path "*/logs/*" \
    ! -path "*/log/*" \
    ! -name "*.log" \
    ! -name "*.sqlite3" \
    ! -name "*.sqlite" \
    ! -name "*.db" \
  | sort | while read -r FILE; do
        local REL="$FILE"

        echo "" >> "$OUT"
        echo "---" >> "$OUT"
        echo "" >> "$OUT"
        echo "### \`$REL\`" >> "$OUT"
        echo "" >> "$OUT"

        local EXT="${FILE##*.}"
        local LANG=""
        case "$EXT" in
          py)          LANG="python" ;;
          html|htm)    LANG="html" ;;
          js)          LANG="javascript" ;;
          ts)          LANG="typescript" ;;
          css)         LANG="css" ;;
          md)          LANG="markdown" ;;
          json)        LANG="json" ;;
          toml)        LANG="toml" ;;
          yml|yaml)    LANG="yaml" ;;
          sh)          LANG="bash" ;;
          service|socket|conf) LANG="ini" ;;
          *)           LANG="" ;;
        esac

        if [ -n "$LANG" ]; then
          echo "\`\`\`$LANG" >> "$OUT"
        else
          echo "\`\`\`" >> "$OUT"
        fi

        cat "$FILE" >> "$OUT"
        echo "" >> "$OUT"
        echo "\`\`\`" >> "$OUT"
    done
}

dump_file () {
  local FILE="$1"
  local TITLE="$2"

  if [ ! -f "$FILE" ]; then
    echo "- [WARN] file not found: $FILE" >&2
    return 0
  fi

  echo "" >> "$OUT"
  echo "## $TITLE" >> "$OUT"
  echo "" >> "$OUT"
  echo "### \`$FILE\`" >> "$OUT"
  echo "" >> "$OUT"

  local EXT="${FILE##*.}"
  local LANG=""
  case "$EXT" in
    service|socket|conf) LANG="ini" ;;
    env)                 LANG="bash" ;;
    *)                   LANG="" ;;
  esac

  if [ -n "$LANG" ]; then
    echo "\`\`\`$LANG" >> "$OUT"
  else
    echo "\`\`\`" >> "$OUT"
  fi

  cat "$FILE" >> "$OUT"
  echo "" >> "$OUT"
  echo "\`\`\`" >> "$OUT"
}

# 1. Лендинг и фронтенд
dump_dir "/var/www/logos/landing" "Landing / Frontend"

# 2. Telegram guard bot
dump_dir "/var/www/logos/landing/logos_tg_bot/logos_guard_bot" "Telegram Guard Bot"

# 3. X Guard (Twitter integration) — модуль из репозитория
dump_dir "/root/logos_lrb/modules/x_guard" "X Guard (Twitter Guard Service)"

# 4. Airdrop API backend
dump_dir "/opt/logos/airdrop-api" "Airdrop API Backend"

# 5. systemd и env
dump_file "/etc/systemd/system/logos-airdrop-api.service" "systemd: logos-airdrop-api.service"
dump_file "/etc/systemd/system/logos-x-guard.service"     "systemd: logos-x-guard.service"
dump_file "/etc/logos/airdrop-api.env"                    "Env: /etc/logos/airdrop-api.env"

echo ""
echo "Snapshot written to: $OUT"

```

### FILE: /root/logos_lrb/tools/prepare_payer.sh
```
#!/usr/bin/env bash
set -euo pipefail

API=${API:-http://127.0.0.1:8080}
FROM=${FROM:-PAYER}
AMOUNT=${AMOUNT:-1000000}
NONCE=${NONCE:-0}

JWT_SECRET="$(sed -n 's/^LRB_ADMIN_JWT_SECRET=//p' /etc/logos/keys.env | tr -d '[:space:]')"
if [[ -z "${JWT_SECRET}" ]]; then
  echo "[ERR] LRB_ADMIN_JWT_SECRET is empty"; exit 1
fi

b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }

H=$(printf '{"alg":"HS256","typ":"JWT"}' | b64url)
P=$(printf '{"sub":"admin","iat":1690000000,"exp":2690000000}' | b64url)
S=$(printf '%s' "$H.$P" | openssl dgst -sha256 -hmac "$JWT_SECRET" -binary | b64url)
JWT="$H.$P.$S"

echo "[*] set_balance $FROM = $AMOUNT"
curl -sf -X POST "$API/admin/set_balance" \
  -H "X-Admin-JWT: $JWT" -H 'Content-Type: application/json' \
  -d "{\"rid\":\"$FROM\",\"amount\":$AMOUNT}" || { echo; echo "[ERR] set_balance failed"; exit 1; }
echo

echo "[*] set_nonce $FROM = $NONCE"
curl -sf -X POST "$API/admin/set_nonce" \
  -H "X-Admin-JWT: $JWT" -H 'Content-Type: application/json' \
  -d "{\"rid\":\"$FROM\",\"value\":$NONCE}" || { echo; echo "[ERR] set_nonce failed"; exit 1; }
echo

echo "[*] balance:"
curl -sf "$API/balance/$FROM" || true
echo

```

### FILE: /root/logos_lrb/tools/probe_canon.py
```
#!/usr/bin/env python3
import os, time, json, hashlib, asyncio
import aiohttp
from nacl.signing import SigningKey
import base58

NODE = os.getenv("LRB_NODE_URL", "http://127.0.0.1:8080").rstrip("/")
FROM = os.getenv("LRB_FROM_RID", "").strip()
TO   = os.getenv("LRB_TO_RID", "").strip()
SKHX = os.getenv("LRB_SK_HEX", "").strip()

if not (FROM and TO and SKHX):
    raise SystemExit("need LRB_NODE_URL, LRB_FROM_RID, LRB_TO_RID, LRB_SK_HEX")
if len(SKHX) != 64:
    raise SystemExit("LRB_SK_HEX must be 64 hex chars (32 bytes)")

sk = SigningKey(bytes.fromhex(SKHX))
if base58.b58encode(bytes(sk.verify_key)).decode() != FROM:
    raise SystemExit("SK_HEX does not match FROM_RID")

def u64be(x:int) -> bytes: return int(x).to_bytes(8,"big")
def u64le(x:int) -> bytes: return int(x).to_bytes(8,"little")

# Кандидаты: (name, make_msg_bytes)
def mk_variants():
    from_b = FROM.encode()
    to_b   = TO.encode()
    bar = b"|"
    col = b":"
    zero = b"\x00"
    v = []

    # A) sha256(from|to|amount_be|nonce_be)
    def a(amount,nonce):
        raw = b"".join([from_b,bar,to_b,bar,u64be(amount),bar,u64be(nonce)])
        return hashlib.sha256(raw).digest()
    v.append(("sha256_pipe_be_be", a))

    # B) sha256(from:to:amount_be:nonce_be)
    def b(amount,nonce):
        raw = b"".join([from_b,col,to_b,col,u64be(amount),col,u64be(nonce)])
        return hashlib.sha256(raw).digest()
    v.append(("sha256_colon_be_be", b))

    # C) sha256(from|to|amount_le|nonce_le)
    def c(amount,nonce):
        raw = b"".join([from_b,bar,to_b,bar,u64le(amount),bar,u64le(nonce)])
        return hashlib.sha256(raw).digest()
    v.append(("sha256_pipe_le_le", c))

    # D) sha256(LOGOS_LRB_TX_V1)+from+0+to+0+amount_le+nonce_le  (вариант "префикс")
    pref = hashlib.sha256(b"LOGOS_LRB_TX_V1").digest()
    def d(amount,nonce):
        raw = b"".join([pref, from_b, zero, to_b, zero, u64le(amount), u64le(nonce)])
        return raw  # тут уже "готовые байты", без sha256
    v.append(("pref_v1_raw_le_le", d))

    # E) sha256(pref_v1_raw_le_le) (префикс + sha)
    def e(amount,nonce):
        return hashlib.sha256(d(amount,nonce)).digest()
    v.append(("pref_v1_sha_le_le", e))

    return v

async def get_nonce(sess):
    async with sess.get(f"{NODE}/balance/{FROM}") as r:
        t = await r.text()
        if r.status != 200:
            raise RuntimeError(f"balance http {r.status} {t[:200]}")
        j = json.loads(t)
        return int(j.get("nonce",0))

async def submit(sess, amount, nonce, sig_hex):
    payload = {"from": FROM, "to": TO, "amount": amount, "nonce": nonce, "sig_hex": sig_hex}
    async with sess.post(f"{NODE}/submit_tx", json=payload) as r:
        t = await r.text()
        try: j = json.loads(t) if t else {}
        except: j = {"raw": t[:200]}
        return r.status, j

def accepted(resp: dict) -> bool:
    return isinstance(resp,dict) and (resp.get("accepted") is True or resp.get("ok") is True)

async def main():
    nonce0 = None
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as sess:
        nonce0 = await get_nonce(sess)
        nonce = nonce0 + 1
        amount = 1

        print("probe nonce =", nonce, "from current nonce", nonce0)

        for name, fn in mk_variants():
            msg = fn(amount, nonce)
            sig_hex = sk.sign(msg).signature.hex()
            code, j = await submit(sess, amount, nonce, sig_hex)
            print(f"[{name}] HTTP={code} resp={j}")

            if code == 200 and accepted(j):
                print("\nFOUND OK CANON:", name)
                # сохраняем выбранный вариант
                with open("tools/canon_choice.txt","w") as f:
                    f.write(name + "\n")
                return

        print("\nNO variant accepted. Look at resp fields above (likely bad_sig/malformed).")

asyncio.run(main())

```

### FILE: /root/logos_lrb/tools/repo_audit.sh
```
#!/usr/bin/env bash
set -euo pipefail

fail=0
pass(){ printf "  [OK]  %s\n" "$1"; }
err(){  printf "  [FAIL] %s\n" "$1"; fail=1; }

echo "== GIT STATUS =="
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "not a git repo"; exit 1; }
git status --porcelain

echo "== CORE CODE =="
[ -d lrb_core/src ] && pass "lrb_core/src" || err "lrb_core/src missing"
[ -f lrb_core/src/ledger.rs ] && pass "lrb_core ledger.rs" || err "ledger.rs missing"
[ -f lrb_core/src/rcp_engine.rs ] && pass "lrb_core rcp_engine.rs" || err "rcp_engine.rs missing"
[ -f lrb_core/src/phase_filters.rs ] && pass "lrb_core phase_filters.rs" || err "phase_filters.rs missing"
[ -f lrb_core/src/crypto.rs ] && pass "lrb_core crypto.rs (AEAD)" || err "crypto.rs missing"

echo "== NODE =="
for f in node/src/main.rs node/src/api.rs node/src/metrics.rs node/src/guard.rs node/src/storage.rs node/src/version.rs; do
  [ -f "$f" ] && pass "$f" || err "$f missing"
done
[ -f node/src/openapi.json ] && pass "node/src/openapi.json" || err "openapi.json missing"
[ -f node/build.rs ] && pass "node/build.rs" || err "node/build.rs missing"
[ -f node/Cargo.toml ] && pass "node/Cargo.toml" || err "node/Cargo.toml missing"

echo "== MODULES DIR =="
[ -d modules ] && pass "modules/ present" || err "modules/ missing"

echo "== WALLET =="
for f in www/wallet/index.html www/wallet/wallet.css www/wallet/wallet.js; do
  [ -f "$f" ] && pass "$f" || err "$f missing"
done

echo "== INFRA =="
for f in infra/systemd/logos-node@.service infra/systemd/logos-healthcheck.service infra/systemd/logos-healthcheck.timer \
         infra/nginx/logos-api-lb.conf.example; do
  [ -f "$f" ] && pass "$f" || err "$f missing"
done

echo "== SCRIPTS =="
[ -f scripts/bootstrap_node.sh ] && pass "scripts/bootstrap_node.sh" || err "bootstrap_node.sh missing"
[ -f scripts/logos_healthcheck.sh ] && pass "scripts/logos_healthcheck.sh" || err "logos_healthcheck.sh missing"

echo "== TOOLS =="
[ -f tools/bench/go/bench.go ] && pass "bench v4: tools/bench/go/bench.go" || err "bench.go missing"
[ -f tools/sdk/ts/index.mjs ] && pass "TS SDK: tools/sdk/ts/index.mjs" || err "TS SDK missing"
[ -f tools/sdk/ts/sdk_test.mjs ] && pass "TS SDK test" || err "TS SDK test missing"
[ -f tools/sdk/go/logosapi.go ] && pass "Go SDK: tools/sdk/go/logosapi.go" || err "Go SDK missing"

echo "== CONFIGS / EXAMPLES =="
ls -1 configs/env/*.example >/dev/null 2>&1 && pass "env examples present" || err "env examples missing"
# убедимся что реальные .env не попали
if git ls-files | grep -E '^configs/env/.*\.env$' >/dev/null; then
  err "real .env found in repo"
else
  pass "no real .env tracked"
fi

echo "== SNAPSHOTS (optional) =="
[ -d snapshots ] && echo "  [info] snapshots/ exists (ok)"; true

echo "== SIZE / SUMMARY =="
echo "  tracked files: $(git ls-files | wc -l)"
echo "  repo disk size: $(du -sh . | cut -f1)"

echo "== SECRET LEAK SCAN (quick) =="
git grep -nE '(PRIVATE|SECRET|BEGIN (RSA|EC) PRIVATE KEY)' || true
git grep -nE 'LRB_NODE_SK_HEX=[0-9a-fA-F]{64}$' || true

echo
if [ $fail -eq 0 ]; then
  echo "[RESULT] REPO OK"
else
  echo "[RESULT] FAILS PRESENT"; exit 1
fi

```

### FILE: /root/logos_lrb/tools/sdk/ts/index.mjs
```
// Lightweight production SDK for LOGOS LRB (ESM, no deps). Node 18+ (global fetch).
const DEFAULT_TIMEOUT_MS = 10_000;

export class LogosApi {
  /**
   * @param {string} baseURL e.g. "http://127.0.0.1:8080/api" or "http://host:8080"
   * @param {{timeoutMs?: number, adminKey?: string}} [opt]
   */
  constructor(baseURL, opt = {}) {
    this.baseURL = baseURL.replace(/\/$/, "");
    this.timeoutMs = opt.timeoutMs ?? DEFAULT_TIMEOUT_MS;
    this.adminKey = opt.adminKey;
  }

  _url(path) {
    return this.baseURL + (path.startsWith("/") ? path : `/${path}`);
  }

  async _fetchJSON(method, path, body, headers = {}) {
    const ctrl = new AbortController();
    const t = setTimeout(() => ctrl.abort(), this.timeoutMs);
    try {
      const r = await fetch(this._url(path), {
        method,
        headers: {
          "Content-Type": "application/json",
          ...(this.adminKey ? { "X-Admin-Key": this.adminKey } : {}),
          ...headers,
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: ctrl.signal,
      });
      const ct = r.headers.get("content-type") || "";
      let payload = null;
      if (ct.includes("application/json")) {
        payload = await r.json().catch(() => null);
      } else {
        payload = await r.text().catch(() => null);
      }
      if (!r.ok) {
        const err = new Error(`HTTP ${r.status}`);
        err.status = r.status;
        err.payload = payload;
        throw err;
      }
      return payload;
    } finally {
      clearTimeout(t);
    }
  }

  // -------- Public API
  async healthz()        { return this._fetchJSON("GET",  "/healthz"); }
  async livez()          { return this._fetchJSON("GET",  "/livez"); }
  async readyz()         { return this._fetchJSON("GET",  "/readyz"); }
  async head()           { return this._fetchJSON("GET",  "/head"); }
  async balance(rid)     { return this._fetchJSON("GET",  `/balance/${encodeURIComponent(rid)}`); }
  async debugCanon(tx)   { return this._fetchJSON("POST", "/debug_canon", { tx }); }
  async submitBatch(txs) { return this._fetchJSON("POST", "/submit_tx_batch", { txs }); }
  async faucet(rid, amount) { return this._fetchJSON("POST", "/faucet", { rid, amount }); }

  // -------- Admin
  async nodeInfo()       { return this._fetchJSON("GET",  "/node/info"); }
  async snapshot()       { return this._fetchJSON("POST", "/admin/snapshot"); }
  async restore(path)    { return this._fetchJSON("POST", "/admin/restore", { path }); }
}

```

### FILE: /root/logos_lrb/tools/sdk/ts/sdk_test.mjs
```
import { LogosApi } from "./index.mjs";

// Конфигурация
const HOST = process.env.HOST || "http://127.0.0.1:8080"; // без /api если сервер слушает напрямую
const BASE = process.env.BASE || (HOST.endsWith("/api") ? HOST : HOST + "/api");

async function main() {
  const api = new LogosApi(BASE, { timeoutMs: 10_000 });

  console.log("[*] healthz", await api.healthz());
  console.log("[*] head", await api.head());

  // RID для теста
  // (Можно сгенерить в кошельке; здесь просто smoke по faucet/balance с рандомным RID формально не пройдёт —
  // поэтому делаем только faucet на RID из кошелька, если задан)
  const RID = process.env.RID;
  if (RID) {
    console.log("[*] faucet", await api.faucet(RID, 1000000));
    console.log("[*] balance", await api.balance(RID));
  } else {
    console.log("[i] пропускаю faucet/balance: задайте RID=... в env");
  }

  // submit one (если есть RID и получатель)
  const TO = process.env.TO;
  if (RID && TO) {
    // запрос канона (реальную подпись оставим кошельку; здесь smoke-тест только на 400/401)
    const canon = await api.debugCanon({ from: RID, to: TO, amount: 1, nonce: 1 });
    console.log("[*] canon_hex len", canon.canon_hex.length);
    try {
      const resp = await api.submitBatch([{ from: RID, to: TO, amount: 1, nonce: 1, sig_hex: "00" }]);
      console.log("[*] submit", resp);
    } catch (e) {
      console.log("[*] submit expected error", e.status, e.payload?.results?.[0] ?? e.payload);
    }
  } else {
    console.log("[i] пропускаю submit: задайте RID и TO");
  }
}

main().catch(e => { console.error("ERR", e); process.exit(1); });

```

### FILE: /root/logos_lrb/tools/stress_read_wallets.py
```
#!/usr/bin/env python3
import asyncio
import time
import random

import aiohttp

# Прямо к ноде, без nginx/HTTPS
NODE_HTTP = "http://127.0.0.1:8080"

# ДВА ТВОИХ РЕАЛЬНЫХ RID
RIDS = [
    "AtxobdbGFT3kqJnjcKJJfKoYxz9dYPQDGf6FKsgk2dRt",
    "5uJn8W1eKjRvqeFZyA1VQJEZfrkpSiMX8sRUZq4V3Ry6",
]

CONCURRENCY = 16  # сколько параллельных воркеров
DELAY_BETWEEN_BATCHES = 0.05  # пауза между запросами в воркере, чтобы совсем не ДДОСить

async def one_call(session: aiohttp.ClientSession, rid: str, kind: str, wid: int) -> None:
    """
    Один запрос: либо /balance/:rid, либо /history/:rid?limit=20
    """
    if kind == "balance":
        url = f"{NODE_HTTP}/balance/{rid}"
    else:
        url = f"{NODE_HTTP}/history/{rid}?limit=20"

    t0 = time.perf_counter()
    try:
        async with session.get(url) as resp:
            text = await resp.text()
            dt_ms = (time.perf_counter() - t0) * 1000.0
            if resp.status != 200:
                print(f"[w{wid:02d}] {kind} {rid[:6]}… HTTP {resp.status} ({dt_ms:.2f} ms) :: {text[:120]!r}")
            else:
                # чтобы не засорять вывод, парсим JSON лениво
                # но хотя бы проверим, что это JSON
                try:
                    _ = await resp.json()
                    ok = "OK"
                except Exception as e:
                    ok = f"BAD_JSON: {e}"
                print(f"[w{wid:02d}] {kind} {rid[:6]}… {ok} ({dt_ms:.2f} ms)")
    except Exception as e:
        print(f"[w{wid:02d}] {kind} {rid[:6]}… ERROR: {e!r}")

async def worker(idx: int, session: aiohttp.ClientSession) -> None:
    """
    Воркёр: бесконечно дергает /balance и /history для случайного RID.
    Останавливается по Ctrl+C (KeyboardInterrupt в main()).
    """
    while True:
        rid = random.choice(RIDS)
        kind = random.choice(["balance", "history"])
        await one_call(session, rid, kind, idx)
        await asyncio.sleep(DELAY_BETWEEN_BATCHES)

async def main() -> None:
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [asyncio.create_task(worker(i, session)) for i in range(CONCURRENCY)]
        print(f"Запущено {CONCURRENCY} воркеров, жми Ctrl+C чтобы остановить.")
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nОстановлено по Ctrl+C")

```

### FILE: /root/logos_lrb/tools/stress_submit_tx.py
```
#!/usr/bin/env python3
import os, time, json, asyncio, statistics, hashlib
import aiohttp
from nacl.signing import SigningKey
import base58

NODE = os.getenv("LRB_NODE_URL", "http://127.0.0.1:8080").rstrip("/")
FROM_RID = os.getenv("LRB_FROM_RID", "").strip()
TO_RID   = os.getenv("LRB_TO_RID", "").strip()
SK_HEX   = os.getenv("LRB_SK_HEX", "").strip()

TOTAL  = int(os.getenv("LRB_STRESS_TOTAL", "2000"))
PAR    = int(os.getenv("LRB_STRESS_PAR", "8"))
AMOUNT = int(os.getenv("LRB_STRESS_AMOUNT", "1"))

def pct(vals, p):
    if not vals: return 0.0
    vals = sorted(vals)
    k = int(round((p/100.0) * (len(vals)-1)))
    k = max(0, min(k, len(vals)-1))
    return float(vals[k])

# === Каноническое сообщение (как в ноде) ===
# canonical_bytes = sha256("LOGOS_LRB_TX_V1") + from + 0 + to + 0 + amount_le + nonce_le
def u64le(x: int) -> bytes:
    return int(x).to_bytes(8, "little", signed=False)

PREFIX = hashlib.sha256(b"LOGOS_LRB_TX_V1").digest()

def canonical_bytes(from_rid: str, to_rid: str, amount: int, nonce: int) -> bytes:
    return b"".join([
        PREFIX,
        from_rid.encode("utf-8"), b"\x00",
        to_rid.encode("utf-8"),   b"\x00",
        u64le(amount),
        u64le(nonce),
    ])

async def get_json(sess, url):
    async with sess.get(url) as r:
        t = await r.text()
        if r.status != 200:
            raise RuntimeError(f"GET {url} -> {r.status} {t[:200]}")
        return json.loads(t)

async def post_json(sess, url, payload):
    t0 = time.perf_counter()
    async with sess.post(url, json=payload) as r:
        txt = await r.text()
        dt_ms = (time.perf_counter() - t0) * 1000.0
        ok = (r.status == 200)
        try:
            j = json.loads(txt) if txt else {}
        except:
            j = {"raw": txt[:200]}
        return ok, r.status, j, dt_ms

async def worker(wid, sess, sk: SigningKey, start_nonce, count, out):
    ok_n = 0
    bad_n = 0
    lat = []
    nonce = start_nonce

    for _ in range(count):
        nonce += 1
        msg = canonical_bytes(FROM_RID, TO_RID, AMOUNT, nonce)
        sig_hex = sk.sign(msg).signature.hex()

        payload = {
            "from": FROM_RID,
            "to": TO_RID,
            "amount": AMOUNT,
            "nonce": nonce,
            "signature_hex": sig_hex,
            "ts_ms": int(time.time() * 1000),
        }

        ok, code, j, dt = await post_json(sess, f"{NODE}/submit_tx", payload)
        lat.append(dt)

        # ожидаем {accepted: bool, ...}
        if ok and isinstance(j, dict) and j.get("accepted") is True:
            ok_n += 1
        else:
            bad_n += 1

    out[wid] = (ok_n, bad_n, lat)

async def main():
    if not FROM_RID or not TO_RID:
        raise SystemExit("need LRB_FROM_RID and LRB_TO_RID")
    if len(SK_HEX) != 64:
        raise SystemExit("LRB_SK_HEX must be 64 hex chars (32 bytes), without 0x")

    sk = SigningKey(bytes.fromhex(SK_HEX))

    # sanity: key must match FROM_RID
    if base58.b58encode(bytes(sk.verify_key)).decode() != FROM_RID:
        raise SystemExit("SK_HEX does not match FROM_RID")

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as sess:
        head0 = await get_json(sess, f"{NODE}/head")
        b0 = await get_json(sess, f"{NODE}/balance/{FROM_RID}")
        n0 = int(b0.get("nonce", 0))

        print("HEAD(before) =", head0)
        print("FROM(before) =", b0)

        per = TOTAL // PAR
        rem = TOTAL % PAR

        cursor = n0
        out = {}
        tasks = []
        for i in range(PAR):
            cnt = per + (1 if i < rem else 0)
            if cnt <= 0:
                continue
            tasks.append(asyncio.create_task(worker(i, sess, sk, cursor, cnt, out)))
            cursor += cnt

        t0 = time.perf_counter()
        await asyncio.gather(*tasks)
        dt = time.perf_counter() - t0

        ok_sum = sum(v[0] for v in out.values())
        bad_sum = sum(v[1] for v in out.values())
        all_lat = []
        for v in out.values():
            all_lat.extend(v[2])

        req_s = (ok_sum + bad_sum) / dt if dt > 0 else 0.0
        ok_tps = ok_sum / dt if dt > 0 else 0.0

        head1 = await get_json(sess, f"{NODE}/head")
        bf = await get_json(sess, f"{NODE}/balance/{FROM_RID}")
        bt = await get_json(sess, f"{NODE}/balance/{TO_RID}")

        print("\n=== RESULT ===")
        print(f"sent={ok_sum+bad_sum} accepted={ok_sum} rejected={bad_sum}")
        print(f"wall_s={dt:.3f} req/s={req_s:.1f} accepted_tps={ok_tps:.1f}")
        print(f"p50={pct(all_lat,50):.2f}ms p95={pct(all_lat,95):.2f}ms p99={pct(all_lat,99):.2f}ms max={max(all_lat):.2f}ms" if all_lat else "no latency")
        print("HEAD(after) =", head1)
        print("FROM(after) =", bf)
        print("TO(after)   =", bt)

if __name__ == "__main__":
    asyncio.run(main())

```

### FILE: /root/logos_lrb/tools/stress_write_batch.py
```
#!/usr/bin/env python3
import os, time, json, hashlib, asyncio, statistics
import aiohttp
from nacl.signing import SigningKey
import base58

NODE = os.getenv("LRB_NODE_URL", "http://127.0.0.1:8080").rstrip("/")
FROM = os.getenv("LRB_FROM_RID", "").strip()
TO   = os.getenv("LRB_TO_RID", "").strip()
SKHX = os.getenv("LRB_SK_HEX", "").strip()

TOTAL  = int(os.getenv("LRB_STRESS_TOTAL", "20000"))
BATCH  = int(os.getenv("LRB_BATCH_SIZE", "200"))      # размер одной пачки
AMOUNT = int(os.getenv("LRB_STRESS_AMOUNT", "1"))

# канон, который ты нашёл probe'ом
def u64be(x:int) -> bytes: return int(x).to_bytes(8, "big", signed=False)

def canon_digest(from_rid: str, to_rid: str, amount: int, nonce: int) -> bytes:
    raw = b"".join([
        from_rid.encode(), b"|",
        to_rid.encode(),   b"|",
        u64be(amount),     b"|",
        u64be(nonce),
    ])
    return hashlib.sha256(raw).digest()

def pct(vals, p):
    if not vals: return 0.0
    vals = sorted(vals)
    k = int(round((p/100.0) * (len(vals)-1)))
    k = max(0, min(k, len(vals)-1))
    return float(vals[k])

async def get_json(sess, url):
    async with sess.get(url) as r:
        t = await r.text()
        if r.status != 200:
            raise RuntimeError(f"GET {url} -> {r.status} {t[:200]}")
        return json.loads(t)

async def post_json(sess, url, payload):
    t0 = time.perf_counter()
    async with sess.post(url, json=payload) as r:
        txt = await r.text()
        dt_ms = (time.perf_counter() - t0) * 1000.0
        ok = (r.status == 200)
        try:
            j = json.loads(txt) if txt else {}
        except:
            j = {"raw": txt[:200]}
        return ok, r.status, j, dt_ms

def count_results(resp):
    """
    Поддержим несколько форматов ответа:
      - {"ok":true,"results":[...]}
      - [{"ok":true,...}, ...]
      - {"results":[...]}
    Внутри item считаем accepted, если:
      item.ok == true
      или item.info == "accepted"
      или item.accepted == true
    """
    items = None
    if isinstance(resp, dict):
        if isinstance(resp.get("results"), list):
            items = resp["results"]
        elif isinstance(resp.get("items"), list):
            items = resp["items"]
    elif isinstance(resp, list):
        items = resp

    if not items:
        return 0, 0

    ok = 0
    bad = 0
    for it in items:
        if not isinstance(it, dict):
            bad += 1
            continue
        if it.get("ok") is True or it.get("accepted") is True or it.get("info") == "accepted":
            ok += 1
        else:
            bad += 1
    return ok, bad

async def main():
    if not (FROM and TO and SKHX):
        raise SystemExit("need LRB_NODE_URL/LRB_FROM_RID/LRB_TO_RID/LRB_SK_HEX")
    if len(SKHX) != 64:
        raise SystemExit("LRB_SK_HEX must be 64 hex chars (32 bytes), without 0x")

    sk = SigningKey(bytes.fromhex(SKHX))
    if base58.b58encode(bytes(sk.verify_key)).decode() != FROM:
        raise SystemExit("SK_HEX does not match FROM_RID")

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as sess:
        head0 = await get_json(sess, f"{NODE}/head")
        b0 = await get_json(sess, f"{NODE}/balance/{FROM}")
        nonce = int(b0.get("nonce", 0))

        print("HEAD(before) =", head0)
        print("FROM(before) =", b0)
        print(f"TOTAL={TOTAL} BATCH={BATCH} AMOUNT={AMOUNT}")

        sent = 0
        ok_sum = 0
        bad_sum = 0
        lat = []

        t_start = time.perf_counter()

        while sent < TOTAL:
            n = min(BATCH, TOTAL - sent)
            txs = []
            # делаем пачку со строгим nonce++
            for i in range(1, n + 1):
                nn = nonce + i
                dig = canon_digest(FROM, TO, AMOUNT, nn)
                sig_hex = sk.sign(dig).signature.hex()
                txs.append({
                    "from": FROM,
                    "to": TO,
                    "amount": AMOUNT,
                    "nonce": nn,
                    "sig_hex": sig_hex,
                })

            ok, code, resp, dt_ms = await post_json(sess, f"{NODE}/submit_tx_batch", {"txs": txs})
            lat.append(dt_ms)

            a, r = count_results(resp)
            ok_sum += a
            bad_sum += r

            # если пачка прошла целиком — продвигаем nonce локально
            # иначе — синхронизируем nonce с ноды (чтобы не было разрыва)
            if a == n and r == 0:
                nonce += n
                sent += n
            else:
                # синхронизация nonce (дороже, но безопасно)
                b = await get_json(sess, f"{NODE}/balance/{FROM}")
                nonce = int(b.get("nonce", nonce))
                sent += n

            print(f"[BATCH] size={n} accepted={a} rejected={r} http_ms={dt_ms:.1f} nonce_now={nonce}")

        t_total = time.perf_counter() - t_start

        head1 = await get_json(sess, f"{NODE}/head")
        bf = await get_json(sess, f"{NODE}/balance/{FROM}")
        bt = await get_json(sess, f"{NODE}/balance/{TO}")

        print("\n=== RESULT ===")
        print(f"sent={TOTAL} accepted={ok_sum} rejected={bad_sum} wall_s={t_total:.3f}")
        print(f"accepted_tps={ok_sum/t_total:.1f} req_batches={len(lat)} batch_rps={len(lat)/t_total:.2f}")
        if lat:
            print(f"batch_p50={pct(lat,50):.2f}ms batch_p95={pct(lat,95):.2f}ms batch_p99={pct(lat,99):.2f}ms max={max(lat):.2f}ms")
        print("HEAD(after) =", head1)
        print("FROM(after) =", bf)
        print("TO(after)   =", bt)

if __name__ == "__main__":
    asyncio.run(main())

```

### FILE: /root/logos_lrb/tools/stress_write_tx.py
```
#!/usr/bin/env python3
import os, time, json, asyncio, hashlib, statistics
import aiohttp
from nacl.signing import SigningKey
import base58

NODE = os.getenv("LRB_NODE_URL", "http://127.0.0.1:8080").rstrip("/")
FROM = os.getenv("LRB_FROM_RID", "").strip()
TO   = os.getenv("LRB_TO_RID", "").strip()
SKHX = os.getenv("LRB_SK_HEX", "").strip()

TOTAL  = int(os.getenv("LRB_STRESS_TOTAL", "2000"))
PAR    = int(os.getenv("LRB_STRESS_PAR", "8"))
AMOUNT = int(os.getenv("LRB_STRESS_AMOUNT", "1"))

if not (FROM and TO and SKHX):
    raise SystemExit("need LRB_NODE_URL, LRB_FROM_RID, LRB_TO_RID, LRB_SK_HEX")
if len(SKHX) != 64:
    raise SystemExit("LRB_SK_HEX must be 64 hex chars (32 bytes)")

CHOICE_PATH = "tools/canon_choice.txt"
if not os.path.exists(CHOICE_PATH):
    raise SystemExit("tools/canon_choice.txt not found (run probe first)")
canon_name = open(CHOICE_PATH).read().strip()

sk = SigningKey(bytes.fromhex(SKHX))
if base58.b58encode(bytes(sk.verify_key)).decode() != FROM:
    raise SystemExit("SK_HEX does not match FROM_RID")

def u64be(x:int) -> bytes: return int(x).to_bytes(8, "big", signed=False)
from_b = FROM.encode()
to_b   = TO.encode()
bar = b"|"

def msg_bytes(amount:int, nonce:int) -> bytes:
    # Мы нашли, что принимается sha256(from|to|amount_be|nonce_be)
    raw = b"".join([from_b, bar, to_b, bar, u64be(amount), bar, u64be(nonce)])
    return hashlib.sha256(raw).digest()

def pct(vals, p):
    if not vals: return 0.0
    vals = sorted(vals)
    k = int(round((p/100.0) * (len(vals)-1)))
    k = max(0, min(k, len(vals)-1))
    return float(vals[k])

async def get_json(sess, url):
    async with sess.get(url) as r:
        t = await r.text()
        if r.status != 200:
            raise RuntimeError(f"GET {url} -> {r.status} {t[:200]}")
        return json.loads(t)

async def post_json(sess, url, payload):
    t0 = time.perf_counter()
    async with sess.post(url, json=payload) as r:
        txt = await r.text()
        dt_ms = (time.perf_counter() - t0) * 1000.0
        ok = (r.status == 200)
        try:
            j = json.loads(txt) if txt else {}
        except:
            j = {"raw": txt[:200]}
        return ok, r.status, j, dt_ms

def accepted(resp: dict) -> bool:
    return isinstance(resp, dict) and (resp.get("ok") is True or resp.get("accepted") is True or resp.get("info") == "accepted")

async def worker(wid, sess, start_nonce, count, out):
    ok_n = 0
    bad_n = 0
    lat = []
    nonce = start_nonce

    for _ in range(count):
        nonce += 1
        msg = msg_bytes(AMOUNT, nonce)
        sig_hex = sk.sign(msg).signature.hex()
        payload = {"from": FROM, "to": TO, "amount": AMOUNT, "nonce": nonce, "sig_hex": sig_hex}
        ok, code, j, dt = await post_json(sess, f"{NODE}/submit_tx", payload)
        lat.append(dt)
        if ok and accepted(j):
            ok_n += 1
        else:
            bad_n += 1
    out[wid] = (ok_n, bad_n, lat)

async def main():
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as sess:
        head0 = await get_json(sess, f"{NODE}/head")
        b0 = await get_json(sess, f"{NODE}/balance/{FROM}")
        n0 = int(b0.get("nonce", 0))
        print("CANON =", canon_name)
        print("HEAD(before) =", head0)
        print("FROM(before) =", b0)

        per = TOTAL // PAR
        rem = TOTAL % PAR
        cursor = n0
        out = {}
        tasks = []
        for i in range(PAR):
            cnt = per + (1 if i < rem else 0)
            if cnt <= 0: 
                continue
            tasks.append(asyncio.create_task(worker(i, sess, cursor, cnt, out)))
            cursor += cnt

        t0 = time.perf_counter()
        await asyncio.gather(*tasks)
        dt = time.perf_counter() - t0

        ok_sum = sum(v[0] for v in out.values())
        bad_sum = sum(v[1] for v in out.values())
        all_lat = []
        for v in out.values(): all_lat.extend(v[2])

        req_s = (ok_sum + bad_sum) / dt if dt > 0 else 0.0
        ok_tps = ok_sum / dt if dt > 0 else 0.0

        head1 = await get_json(sess, f"{NODE}/head")
        bf = await get_json(sess, f"{NODE}/balance/{FROM}")
        bt = await get_json(sess, f"{NODE}/balance/{TO}")

        print("\n=== RESULT ===")
        print(f"sent={ok_sum+bad_sum} accepted={ok_sum} rejected={bad_sum}")
        print(f"wall_s={dt:.3f} req/s={req_s:.1f} accepted_tps={ok_tps:.1f}")
        if all_lat:
            print(f"p50={pct(all_lat,50):.2f}ms p95={pct(all_lat,95):.2f}ms p99={pct(all_lat,99):.2f}ms max={max(all_lat):.2f}ms")
        print("HEAD(after) =", head1)
        print("FROM(after) =", bf)
        print("TO(after)   =", bt)

asyncio.run(main())

```

### FILE: /root/logos_lrb/tools/test_tx.sh
```
#!/usr/bin/env bash
set -euo pipefail

NODE="${NODE:-http://127.0.0.1:8080}"

echo "[*] Installing deps (jq, pip, pynacl, base58)..."
apt-get update -y >/dev/null 2>&1 || true
apt-get install -y jq python3-pip >/dev/null 2>&1 || true
python3 -m pip install --quiet --no-input pynacl base58

echo "[*] Generating key, RID and signed tx..."
PYOUT="$(python3 - <<'PY'
import json, base64, base58
from nacl.signing import SigningKey

sk = SigningKey.generate()
vk = sk.verify_key
pk = bytes(vk)
rid = base58.b58encode(pk).decode()

amount = 12345
nonce  = 1

msg_obj = {
    "from": rid,
    "to": rid,
    "amount": amount,
    "nonce": nonce,
    "public_key": base64.b64encode(pk).decode()
}
msg = json.dumps(msg_obj, separators=(',',':')).encode()
sig = sk.sign(msg).signature

tx = {
    "from": rid,
    "to": rid,
    "amount": amount,
    "nonce": nonce,
    "public_key_b58": base58.b58encode(pk).decode(),
    "signature_b64": base64.b64encode(sig).decode()
}

print(json.dumps({"rid": rid, "tx": tx}))
PY
)"

RID="$(echo "$PYOUT" | jq -r .rid)"
TX="$(echo "$PYOUT" | jq -c .tx)"

echo "[*] Healthz:"
curl -s "$NODE/healthz" | jq .

echo "[*] Head before:"
curl -s "$NODE/head" | jq .

echo "[*] Submitting tx..."
RESP="$(curl -s -X POST "$NODE/submit_tx" -H 'content-type: application/json' -d "$TX")" || true
echo "$RESP" | jq . || true

# Если узел отклонил (например, nonce/balance), покажем причину и выйдем
if ! echo "$RESP" | jq -e '.accepted == true' >/dev/null 2>&1 ; then
  echo "[!] TX not accepted. Response above."
  exit 1
fi

TXID="$(echo "$RESP" | jq -r .tx_id)"
echo "[*] tx_id=$TXID"

echo "[*] Waiting 2s for block producer..."
sleep 2

echo "[*] Head after:"
curl -s "$NODE/head" | jq .

echo "[*] Balance for RID:"
curl -s "$NODE/balance/$RID" | jq .

echo "[*] Done."

```

### FILE: /root/logos_lrb/tools/tx_load.sh
```
#!/usr/bin/env bash
# tx_load.sh — надёжная нагрузка через LB/BE без конфликтов nonce.
# Отправка батчей строго по порядку внутри каждого RID (шарда).
# Параллельность — между шардами.
#
# Usage:
#   BACKEND=http://127.0.0.1:8080 ./tx_load.sh M K C [AMOUNT] [SHARDS]
#   (если хочешь через LB: BACKEND=http://127.0.0.1/api)
set -euo pipefail
BACKEND="${BACKEND:-http://127.0.0.1:8080}"   # куда шлём ВСЁ: faucet, canon, submit
M="${1:-1000}"     # всего tx
K="${2:-100}"      # размер батча
C="${3:-10}"       # параллельность шардов (RID)
AMOUNT="${4:-1}"
SHARDS="${5:-$C}"  # число независимых отправителей (RID)

need() { command -v "$1" >/dev/null || { echo "need $1"; exit 1; }; }
need curl; need jq; need openssl; need xxd; need seq; need awk; need sort; need xargs

work="$(mktemp -d -t lrb_load_XXXX)"
trap 'rm -rf "$work"' EXIT
echo "[*] work dir: $work"
per_shard=$(( (M + SHARDS - 1) / SHARDS ))
echo "[*] total=$M  shards=$SHARDS  per_shard≈$per_shard  batch=$K  parallel=$C  amount=$AMOUNT"
echo "[*] BACKEND=$BACKEND"

make_rid() {
  local out="$1"
  openssl genpkey -algorithm Ed25519 -out "$out/ed25519.sk.pem" >/dev/null 2>&1
  openssl pkey -in "$out/ed25519.sk.pem" -pubout -outform DER | tail -c 32 | xxd -p -c 32 > "$out/pk.hex"
  python3 - "$out/pk.hex" > "$out/RID.txt" <<'PY'
import sys
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
pk=bytes.fromhex(open(sys.argv[1]).read().strip())
n=int.from_bytes(pk,'big'); s=""
while n>0: n,r=divmod(n,58); s=ALPH[r]+s
z=0
for b in pk:
    if b==0: z+=1
    else: break
print("1"*z + (s or "1"))
PY
}

# 1) Готовим шардовые каталоги: RID, faucet, nonce0
for s in $(seq 1 "$SHARDS"); do
  sd="$work/shard_$s"; mkdir -p "$sd/batches"
  make_rid "$sd"
  RID=$(cat "$sd/RID.txt")
  echo "[*] shard $s RID=$RID"
  curl -s -X POST "$BACKEND/faucet" -H 'Content-Type: application/json' \
    -d "{\"rid\":\"${RID}\",\"amount\":500000000}" >/dev/null
  NONCE0=$(curl -s "$BACKEND/balance/${RID}" | jq -r .nonce)
  echo "$NONCE0" > "$sd/nonce0"
done

# 2) Генерация подписанных tx для каждого шарда (последовательно → без гонок)
for s in $(seq 1 "$SHARDS"); do
  sd="$work/shard_$s"
  RID=$(cat "$sd/RID.txt")
  SK="$sd/ed25519.sk.pem"
  NONCE0=$(cat "$sd/nonce0")
  start=$(( (s-1)*per_shard + 1 ))
  end=$(( s*per_shard )); [ "$end" -gt "$M" ] && end="$M"
  count=$(( end - start + 1 )); [ "$count" -le 0 ] && continue
  echo "[*] shard $s: tx $start..$end (count=$count)"

  : > "$sd/cur_lines.jsonl"; idx=0; file_lines=0
  for i in $(seq 1 "$count"); do
    nonce=$(( NONCE0 + i ))
    echo "{\"tx\":{\"from\":\"$RID\",\"to\":\"$RID\",\"amount\":$AMOUNT,\"nonce\":$nonce}}" > "$sd/canon_payload.json"
    CANON_HEX=$(curl -s -X POST "$BACKEND/debug_canon" -H "Content-Type: application/json" \
      --data-binary @"$sd/canon_payload.json" | jq -r .canon_hex)
    echo -n "$CANON_HEX" | xxd -r -p > "$sd/canon.bin"
    openssl pkeyutl -sign -rawin -inkey "$SK" -in "$sd/canon.bin" -out "$sd/sig.bin" >/dev/null 2>&1
    SIG_HEX=$(xxd -p -c 256 "$sd/sig.bin")
    printf '{"from":"%s","to":"%s","amount":%s,"nonce":%s,"sig_hex":"%s"}\n' \
      "$RID" "$RID" "$AMOUNT" "$nonce" "$SIG_HEX" >> "$sd/cur_lines.jsonl"
    file_lines=$((file_lines+1))
    if [ "$file_lines" -ge "$K" ]; then
      idx=$((idx+1)); jq -s '{txs:.}' "$sd/cur_lines.jsonl" > "$sd/batches/batch_${s}_$(printf "%05d" $idx).json"
      : > "$sd/cur_lines.jsonl"; file_lines=0
    fi
  done
  if [ "$file_lines" -gt 0 ]; then
    idx=$((idx+1)); jq -s '{txs:.}' "$sd/cur_lines.jsonl" > "$sd/batches/batch_${s}_$(printf "%05d" $idx).json"
  fi
done

# 3) Отправляем батчи ПО ШАРДАМ: внутри каждого — строго по порядку; шарды — параллельно
start_ts=$(date +%s%3N)
ls -1d "$work"/shard_* | xargs -I{} -P"$C" bash -lc '
  sd="{}"
  for f in $(ls -1 "$sd"/batches/batch_*.json | sort -V); do
    curl -s -X POST "'"$BACKEND"'/submit_tx_batch" -H "Content-Type: application/json" \
      --data-binary @"$f" | jq -c "{accepted,rejected,new_height}"
  done
'
end_ts=$(date +%s%3N)
dt=$((end_ts - start_ts))
echo "=== DONE in ${dt} ms → ~ $(( M*1000/(dt>0?dt:1) )) tx/s (client-side est) ==="

# 4) HEAD / METRICS
echo "--- HEAD ---";    curl -s "$BACKEND/head" | jq .
echo "--- METRICS ---"
curl -s "$BACKEND/metrics" \
 | grep -E "lrb_tx_|submit_tx_batch|http_request_duration_seconds_bucket|http_inflight_requests" \
 | head -n 120 || true

```

### FILE: /root/logos_lrb/tools/tx_one.sh
```
#!/usr/bin/env bash
# tx_one.sh — e2e: генерирует ключ, делает RID, faucet, строит канон, подписывает Ed25519 (raw),
# отправляет /submit_tx_batch и печатает head/balance/метрики.
# Usage: PORT=8080 ./tx_one.sh [AMOUNT]
set -euo pipefail
PORT="${PORT:-8080}"
AMOUNT="${1:-1234}"

work="$(mktemp -d -t lrb_one_XXXX)"
trap 'rm -rf "$work"' EXIT

need() { command -v "$1" >/dev/null || { echo "need $1"; exit 1; }; }
need curl; need jq; need openssl; need xxd; need python3

# Key + RID
openssl genpkey -algorithm Ed25519 -out "$work/ed25519.sk.pem" >/dev/null 2>&1
openssl pkey -in "$work/ed25519.sk.pem" -pubout -outform DER | tail -c 32 | xxd -p -c 32 > "$work/pk.hex"
python3 - "$work/pk.hex" > "$work/RID.txt" <<'PY'
import sys
ALPH="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
pk=bytes.fromhex(open(sys.argv[1]).read().strip())
n=int.from_bytes(pk,'big'); s=""
while n>0: n,r=divmod(n,58); s=ALPH[r]+s
z=0
for b in pk:
    if b==0: z+=1
    else: break
print("1"*z + (s or "1"))
PY
RID=$(cat "$work/RID.txt"); echo "RID=$RID"

# Faucet + state
curl -s -X POST "http://127.0.0.1:${PORT}/faucet" -H 'Content-Type: application/json' \
  -d "{\"rid\":\"${RID}\",\"amount\":1000000}" | jq .
STATE=$(curl -s "http://127.0.0.1:${PORT}/balance/${RID}")
NONCE_CUR=$(jq -r .nonce <<<"$STATE"); NONCE=$((NONCE_CUR+1))
echo "nonce: $NONCE_CUR -> $NONCE"

# Canon
jq -n --arg f "$RID" --arg t "$RID" --argjson a "$AMOUNT" --argjson n "$NONCE" \
  '{tx:{from:$f,to:$t,amount:$a,nonce:$n}}' > "$work/canon_payload.json"
CANON_HEX=$(curl -s -X POST "http://127.0.0.1:${PORT}/debug_canon" -H 'Content-Type: application/json' \
  --data-binary @"$work/canon_payload.json" | jq -r .canon_hex)
echo -n "$CANON_HEX" | xxd -r -p > "$work/canon.bin"

# Sign
openssl pkeyutl -sign -rawin -inkey "$work/ed25519.sk.pem" -in "$work/canon.bin" -out "$work/sig.bin" >/dev/null 2>&1
SIG_HEX=$(xxd -p -c 256 "$work/sig.bin")

# Batch
jq -n --arg f "$RID" --arg t "$RID" --argjson a "$AMOUNT" --argjson n "$NONCE" --arg s "$SIG_HEX" \
  '{txs:[{from:$f,to:$t,amount:$a,nonce:$n,sig_hex:$s}]}' > "$work/batch.json"
curl -s -X POST "http://127.0.0.1:${PORT}/submit_tx_batch" -H 'Content-Type: application/json' \
  --data-binary @"$work/batch.json" | jq .

# Head / post state / metrics
echo "--- HEAD ---";         curl -s "http://127.0.0.1:${PORT}/head" | jq .
echo "--- POST ---";         curl -s "http://127.0.0.1:${PORT}/balance/${RID}" | jq .
echo "--- METRICS ---";      curl -s "http://127.0.0.1:${PORT}/metrics" \
 | grep -E "lrb_tx_|submit_tx_batch|http_inflight_requests" | head -n 40 || true

```

### FILE: /root/logos_lrb/tools/vegeta_submit_live.sh
```
#!/usr/bin/env bash
set -euo pipefail

# === defaults ===
API="http://127.0.0.1:8080"
FROM="PAYER"
TO="RCV"
AMOUNT=1
RATE=500
DURATION="60s"
START_NONCE=1
COUNT=10000
REPORT_EVERY=30   # секунд

# === parse KEY=VALUE ===
for kv in "$@"; do
  case "$kv" in
    API=*) API=${kv#API=} ;;
    FROM=*) FROM=${kv#FROM=} ;;
    TO=*) TO=${kv#TO=} ;;
    AMOUNT=*) AMOUNT=${kv#AMOUNT=} ;;
    RATE=*) RATE=${kv#RATE=} ;;
    DURATION=*) DURATION=${kv#DURATION=} ;;
    START_NONCE=*) START_NONCE=${kv#START_NONCE=} ;;
    COUNT=*) COUNT=${kv#COUNT=} ;;
    REPORT_EVERY=*) REPORT_EVERY=${kv#REPORT_EVERY=} ;;
    *) echo "[WARN] unknown arg: $kv" ;;
  esac
done

command -v vegeta >/dev/null 2>&1 || { echo "[ERR] vegeta not found"; exit 1; }

echo "[*] attack: rate=${RATE} for ${DURATION} | from=${FROM} to=${TO} amount=${AMOUNT} nonces=${START_NONCE}..$((START_NONCE+COUNT-1))"

# === generate JSONL targets ===
TARGETS="targets.jsonl"
RESULTS="results.bin"
rm -f "$TARGETS" "$RESULTS"

gen_targets_json() {
  local n=${START_NONCE}
  local end=$((START_NONCE + COUNT - 1))
  while [[ $n -le $end ]]; do
    local body b64
    body=$(printf '{"from":"%s","to":"%s","amount":%d,"nonce":%d,"memo":"load","sig_hex":"00"}' \
      "$FROM" "$TO" "$AMOUNT" "$n")
    b64=$(printf '%s' "$body" | openssl base64 -A)
    printf '{"method":"POST","url":"%s/submit_tx","body":"%s","header":{"Content-Type":["application/json"]}}\n' \
      "$API" "$b64"
    n=$((n+1))
  done
}

gen_targets_json > "$TARGETS"

# === start attack in background ===
( vegeta attack -format=json -rate="${RATE}" -duration="${DURATION}" -targets="$TARGETS" > "$RESULTS" ) &
VEG_PID=$!

# cleanup & final report on Ctrl+C / TERM
finish() {
  echo
  echo "[*] stopping attack (pid=$VEG_PID) and printing final report..."
  kill "$VEG_PID" 2>/dev/null || true
  wait "$VEG_PID" 2>/dev/null || true

  echo "[*] FINAL SUMMARY:"
  vegeta report "$RESULTS"

  echo "[*] FINAL HISTOGRAM:"
  vegeta report -type='hist[0,500us,1ms,2ms,5ms,10ms,20ms,50ms,100ms]' "$RESULTS"

  echo "[*] JSON metrics -> results.json"
  vegeta report -type=json "$RESULTS" > results.json

  # archive sample (если включён /archive)
  if curl -sf "${API}/archive/history/${FROM}" >/dev/null 2>&1; then
    echo "[*] archive sample:"
    curl -sf "${API}/archive/history/${FROM}" | jq '.[0:5]' || true
  fi
  exit 0
}
trap finish INT TERM

# === live progress loop ===
START_TS=$(date +%s)
while kill -0 "$VEG_PID" 2>/dev/null; do
  sleep "$REPORT_EVERY"
  NOW=$(date +%s); ELAPSED=$((NOW-START_TS))
  echo
  echo "[*] PROGRESS t=${ELAPSED}s:"
  vegeta report "$RESULTS" || true
done

# wait and final when finished naturally
finish

```

### FILE: /root/logos_lrb/tools/vegeta_submit.sh
```
#!/usr/bin/env bash
set -euo pipefail

# --- дефолты ---
API="http://127.0.0.1:8080"
FROM="PAYER"
TO="RCV"
AMOUNT=1
RATE=500
DURATION="60s"
START_NONCE=1
COUNT=10000

# --- парсинг KEY=VALUE из аргументов ---
for kv in "$@"; do
  case "$kv" in
    API=*) API=${kv#API=} ;;
    FROM=*) FROM=${kv#FROM=} ;;
    TO=*) TO=${kv#TO=} ;;
    AMOUNT=*) AMOUNT=${kv#AMOUNT=} ;;
    RATE=*) RATE=${kv#RATE=} ;;
    DURATION=*) DURATION=${kv#DURATION=} ;;
    START_NONCE=*) START_NONCE=${kv#START_NONCE=} ;;
    COUNT=*) COUNT=${kv#COUNT=} ;;
    *) echo "[WARN] unknown arg: $kv" ;;
  esac
done

command -v vegeta >/dev/null 2>&1 || { echo "[ERR] vegeta not found in PATH"; exit 1; }

echo "[*] attack: rate=${RATE} for ${DURATION} | from=${FROM} to=${TO} amount=${AMOUNT} nonces=${START_NONCE}..$((START_NONCE+COUNT-1))"

gen_targets_json() {
  local n=${START_NONCE}
  local end=$((START_NONCE + COUNT - 1))
  while [[ $n -le $end ]]; do
    local body b64
    body=$(printf '{"from":"%s","to":"%s","amount":%d,"nonce":%d,"memo":"load","sig_hex":"00"}' \
      "$FROM" "$TO" "$AMOUNT" "$n")
    b64=$(printf '%s' "$body" | openssl base64 -A)
    printf '{"method":"POST","url":"%s/submit_tx","body":"%s","header":{"Content-Type":["application/json"]}}\n' \
      "$API" "$b64"
    n=$((n+1))
  done
}

# атака: live-репорт каждые 30s + финальные отчёты
gen_targets_json \
  | vegeta attack -format=json -rate="${RATE}" -duration="${DURATION}" \
  | tee results.bin \
  | vegeta report -every 30s

echo "[*] latency histogram:"
vegeta report -type='hist[0,500us,1ms,2ms,5ms,10ms,20ms,50ms,100ms]' results.bin

echo "[*] JSON metrics -> results.json"
vegeta report -type=json results.bin > results.json

# срез архива (если включён /archive)
if curl -sf "${API}/archive/history/${FROM}" >/dev/null 2>&1; then
  echo "[*] archive sample:"
  curl -sf "${API}/archive/history/${FROM}" | jq '.[0:5]' || true
fi

```
