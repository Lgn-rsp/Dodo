#!/usr/bin/env python3
import os, re, time, subprocess, hashlib
from pathlib import Path

TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUTDIR = Path("docs/WALLET_PERIMETER_FULL_V2")
OUTDIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# INCLUDE ROOTS (полный периметр)
# -----------------------------
ROOTS = [
  "/opt/logos/www/wallet_dev",
  "/opt/logos/www/wallet",
  "/opt/logos/www/wallet_v2",
  "/opt/logos/www/wallet_premium",
  "/opt/logos/www/shared",
  "/opt/logos/wallet-proxy",
  "/var/www/logos/wallet",
  "/var/www/logos/wallet3",
  "/var/www/logos/explorer",
]

# nginx / systemd / env
EXTRA_GLOBS = [
  "/etc/nginx/nginx.conf",
  "/etc/nginx/sites-enabled/*",
  "/etc/nginx/conf.d/*",
  "/etc/nginx/snippets/*",
  "/etc/systemd/system/*.service",
  "/etc/systemd/system/*.service.d/*",
  "/etc/logos/*.env*",
  "/etc/logos/*.yaml",
  "/etc/logos/*.yml",
]

# -----------------------------
# FILTERS
# -----------------------------
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots","data.sled.bak"}
ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt|env|map|svg)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$|\.exe$|\.so$|\.dll$)", re.I)

# жёстко не тащим старые мегакниги/снапшоты
SKIP_PATH_CONTAINS = [
  "/root/logos_lrb/docs/LOGOS_",
  "/root/logos_lrb/docs/snapshots/",
  "/root/logos_lrb/docs/BOOK/",
  "/root/logos_lrb/docs/LOGOS_MONO_BOOK",
  "/root/logos_lrb/docs/LOGOS_SNAPSHOTS/",
  "/root/logos_lrb/docs/LOGOS_GLOBAL_CODE_SNAPSHOT",
  "/root/logos_lrb/docs/LOGOS_LRB_FULL_BOOK",
  "/root/logos_lrb/docs/LOGOS_FRONT_STACK",
  "/root/logos_lrb/docs/LOGOS_FULL_SYSTEM_BOOK",
  "/root/logos_lrb/docs/LOGOS_WALLET_EXPLORER",
]

# GitHub-friendly part size
PART_LIMIT = 18 * 1024 * 1024  # 18MB

# секреты редактируем
SENSITIVE_ENV_NAMES = re.compile(r"(SECRET|TOKEN|KEY|PASS|PASSWORD|PRIVATE|SEED|MNEMONIC|BEARER|API_KEY|BOT|TG|TELEGRAM|TWITTER|XAUTH|COOKIE|SESSION)", re.I)

def path_skip(p: str) -> bool:
    return any(s in p for s in SKIP_PATH_CONTAINS)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Path(path).read_text(encoding="latin-1", errors="replace")

def redact_env(text: str) -> str:
    out=[]
    for line in text.splitlines():
        if line.strip().startswith("#") or "=" not in line:
            out.append(line)
            continue
        k,v = line.split("=",1)
        k_strip=k.strip()
        if SENSITIVE_ENV_NAMES.search(k_strip):
            out.append(f"{k_strip}=REDACTED")
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def is_sensitive_file(path: str) -> bool:
    base = os.path.basename(path).lower()
    lp = path.lower()
    if base.endswith(".key") or base.endswith(".rid"):
        return True
    if base.endswith(".env") or base.endswith(".envy"):
        return True
    if "/etc/logos/" in lp and base.endswith(".env"):
        return True
    return False

class PartWriter:
    def __init__(self, outdir: Path, prefix: str):
        self.outdir = outdir
        self.prefix = prefix
        self.part_no = 1
        self.bytes = 0
        self.path = self._path()
        self.f = self.path.open("w", encoding="utf-8")

    def _path(self):
        return self.outdir / f"{self.prefix}_part{self.part_no:03d}.md"

    def _rotate(self):
        self.f.close()
        self.part_no += 1
        self.bytes = 0
        self.path = self._path()
        self.f = self.path.open("w", encoding="utf-8")

    def write(self, s: str):
        b = s.encode("utf-8")
        if self.bytes + len(b) > PART_LIMIT and self.bytes > 0:
            self._rotate()
        self.f.write(s)
        self.bytes += len(b)

    def close(self):
        self.f.close()

def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return e.output

def glob_files(pattern: str):
    return [str(p) for p in Path("/").glob(pattern.lstrip("/"))]

def collect_files():
    files=set()

    # roots recursive
    for root in ROOTS:
        if not os.path.exists(root):
            continue
        for cur, dnames, fnames in os.walk(root):
            parts = cur.split("/")
            if any(d in parts for d in SKIP_DIRS):
                dnames[:] = []
                continue
            dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
            for n in fnames:
                if SKIP_NAME.search(n):
                    continue
                p = os.path.join(cur, n)
                if path_skip(p):
                    continue
                # разрешаем и без ext (например, "Dockerfile")? — нет, только текстовые ext
                if not ALLOW_EXT.search(n):
                    continue
                files.add(p)

    # extra globs (nginx/systemd/env)
    for g in EXTRA_GLOBS:
        for f in glob_files(g):
            if os.path.isfile(f) and not path_skip(f):
                n=os.path.basename(f)
                if SKIP_NAME.search(n):
                    continue
                # для конфигов allow даже если без ext — но тут почти всё с ext
                files.add(f)

    return sorted(files)

def try_fetch_openapi(outdir: Path):
    # node-api openapi
    urls = [
        "http://127.0.0.1:8080/openapi.json",
        "http://127.0.0.1:8080/openapi",
        "http://127.0.0.1:8080/api/openapi.json",
        "http://127.0.0.1:8080/swagger.json",
        "http://127.0.0.1:8080/docs/openapi.json",
    ]
    got=[]
    for u in urls:
        txt = run(["bash","-lc", f"curl -fsS --max-time 4 {u} 2>/dev/null || true"])
        if txt and txt.strip().startswith("{") and "openapi" in txt.lower():
            p = outdir / ("node_api_openapi.json")
            p.write_text(txt, encoding="utf-8")
            got.append(str(p))
            break
    # wallet-api openapi
    urls2 = [
        "http://127.0.0.1:9090/openapi.json",
        "http://127.0.0.1:9090/openapi",
        "http://127.0.0.1:9090/docs/openapi.json",
    ]
    for u in urls2:
        txt = run(["bash","-lc", f"curl -fsS --max-time 4 {u} 2>/dev/null || true"])
        if txt and txt.strip().startswith("{") and "openapi" in txt.lower():
            p = outdir / ("wallet_api_openapi.json")
            p.write_text(txt, encoding="utf-8")
            got.append(str(p))
            break
    return got

def node_api_inventory():
    # если openapi нет — пробуем инвентарь по типовым путям
    paths = [
        "/head",
        "/health",
        "/balance/test",
        "/balance/",
        "/balance",
        "/balance/{rid}",
        "/nonce/{rid}",
        "/submit_tx",
        "/submit_tx_batch",
        "/debug_canon",
        "/tx/",
        "/history/",
        "/stake/",
    ]
    lines=[]
    for p in paths:
        u = f"http://127.0.0.1:8080{p}"
        out = run(["bash","-lc", f"curl -sS -o /dev/null -w '%{{http_code}}' --max-time 3 {u} 2>/dev/null || true"])
        code = out.strip() if out else "NA"
        lines.append(f"{code}  {u}")
    return "\n".join(lines) + "\n"

def extract_api_base_urls(search_roots):
    # ищем API_BASE_URL / node-api / wallet-api / /api / /proxy упоминания
    cmd = (
        "grep -RIn --exclude-dir=node_modules --exclude-dir=target --exclude-dir=.git "
        "--exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.gif' --exclude='*.webp' "
        "--exclude='*.pdf' "
        "'API_BASE_URL\\|node-api\\|wallet-api\\|/api\\|/proxy\\|logos_node_backend\\|logos_wallet_api' "
        + " ".join([sh_escape(r) for r in search_roots if os.path.exists(r)])
        + " 2>/dev/null | head -n 400 || true"
    )
    return run(["bash","-lc", cmd])

def sh_escape(s: str) -> str:
    return "'" + s.replace("'", "'\"'\"'") + "'"

def find_db_candidates():
    # ищем пути DB в env (редактируем секреты, но путь DB нужен)
    envs = ["/etc/logos/proxy.env", "/etc/logos/wallet-proxy.env"]
    vals=[]
    for e in envs:
        if not os.path.exists(e):
            continue
        txt = read_text(e)
        for line in txt.splitlines():
            if "=" not in line:
                continue
            k,v = line.split("=",1)
            k=k.strip()
            v=v.strip().strip('"').strip("'")
            if re.search(r"(DB|DATABASE|SQLITE|DSN|POSTGRES|PG|STORAGE)", k, re.I):
                vals.append((k,v,e))
    # находим sqlite файлы по этим значениям
    sqlite_paths=[]
    for k,v,e in vals:
        if v.endswith(".db") or v.endswith(".sqlite") or v.endswith(".sqlite3"):
            if os.path.exists(v):
                sqlite_paths.append(v)
    return vals, sqlite_paths

def main():
    files = collect_files()

    # openapi grabs
    extra_generated = try_fetch_openapi(OUTDIR)
    for f in extra_generated:
        files.append(f)
    files = sorted(set(files))

    # inventory wallet dirs
    wallet_inventory=[]
    for base in ["/opt/logos/www", "/var/www/logos"]:
        if not os.path.isdir(base):
            continue
        try:
            for name in sorted(os.listdir(base)):
                if "wallet" in name.lower():
                    wallet_inventory.append(os.path.join(base, name))
        except Exception:
            pass

    nginx_T = run(["bash","-lc","nginx -T 2>/dev/null || true"])

    systemd_blocks = {
        "logos-node@main": run(["bash","-lc","systemctl cat logos-node@main --no-pager 2>/dev/null || true"]),
        "logos-wallet-proxy": run(["bash","-lc","systemctl cat logos-wallet-proxy --no-pager 2>/dev/null || true"]),
        "lrb-proxy": run(["bash","-lc","systemctl cat lrb-proxy --no-pager 2>/dev/null || true"]),
        "lrb-scanner": run(["bash","-lc","systemctl cat lrb-scanner --no-pager 2>/dev/null || true"]),
    }
    journal_blocks = {
        "logos-node@main": run(["bash","-lc","journalctl -u logos-node@main -n 200 --no-pager 2>/dev/null || true"]),
        "logos-wallet-proxy": run(["bash","-lc","journalctl -u logos-wallet-proxy -n 200 --no-pager 2>/dev/null || true"]),
        "lrb-proxy": run(["bash","-lc","journalctl -u lrb-proxy -n 200 --no-pager 2>/dev/null || true"]),
        "lrb-scanner": run(["bash","-lc","journalctl -u lrb-scanner -n 200 --no-pager 2>/dev/null || true"]),
    }

    node_inv = node_api_inventory()
    api_base_refs = extract_api_base_urls([
        "/opt/logos/www/wallet_dev",
        "/opt/logos/www/wallet",
        "/opt/logos/www/wallet_v2",
        "/opt/logos/www/wallet_premium",
        "/opt/logos/wallet-proxy",
        "/etc/nginx",
    ])

    env_kv, sqlite_paths = find_db_candidates()
    sqlite_schema = ""
    for db in sqlite_paths[:1]:
        sqlite_schema = run(["bash","-lc", f"sqlite3 {sh_escape(db)} '.schema' 2>/dev/null || true"])
        break

    prefix="WALLET_PERIMETER_FULL_V2"
    pw = PartWriter(OUTDIR, prefix)

    pw.write(f"# LOGOS — WALLET PERIMETER FULL BOOK (V2)\n\n")
    pw.write(f"_Generated: {TS} UTC_\n\n")
    pw.write("## CANONICAL ROUTING FACTS (from nginx)\n\n")
    pw.write("- PROD UI: `/wallet/` → `/opt/logos/www/wallet/`\n")
    pw.write("- DEV UI: `/wallet_dev/` → `/opt/logos/www/wallet_dev/`\n")
    pw.write("- V2 UI: `/wallet_v2/` → `/opt/logos/www/wallet_v2/`\n")
    pw.write("- NODE API: `/node-api/` → `127.0.0.1:8080`\n")
    pw.write("- WALLET API: `/wallet-api/` → `127.0.0.1:9090`\n")
    pw.write("- COMPAT: `/api/` → `127.0.0.1:8080`\n")
    pw.write("- COMPAT: `/proxy/` → `127.0.0.1:9090`\n\n")
    pw.write("---\n\n")

    pw.write("## INVENTORY (wallet folders found)\n\n")
    for p in wallet_inventory:
        pw.write(f"- {p}\n")
    pw.write("\n---\n\n")

    pw.write("## API_BASE_URL / ROUTES REFERENCES (grep)\n\n```txt\n")
    pw.write((api_base_refs or "").rstrip("\n") + "\n")
    pw.write("```\n\n---\n\n")

    pw.write("## NODE API — OPENAPI (if fetched) / INVENTORY (if not)\n\n")
    if any("node_api_openapi" in f for f in files):
        pw.write("- node_api_openapi.json: included as file below.\n\n")
    pw.write("### endpoint inventory (HTTP codes)\n\n```txt\n")
    pw.write(node_inv.rstrip("\n") + "\n")
    pw.write("```\n\n---\n\n")

    pw.write("## NGINX FULL DUMP (nginx -T)\n\n```nginx\n")
    pw.write((nginx_T or "").rstrip("\n") + "\n")
    pw.write("```\n\n---\n\n")

    pw.write("## SYSTEMD UNITS\n\n")
    for k,v in systemd_blocks.items():
        pw.write(f"### {k}\n\n```ini\n{(v or 'N/A').rstrip()}\n```\n\n")
    pw.write("---\n\n")

    pw.write("## JOURNAL LOGS (last 200 lines)\n\n")
    for k,v in journal_blocks.items():
        pw.write(f"### {k}\n\n```txt\n{(v or 'N/A').rstrip()}\n```\n\n")
    pw.write("---\n\n")

    pw.write("## DB DISCOVERY (from env)\n\n")
    if env_kv:
        pw.write("```txt\n")
        for k,v,e in env_kv:
            pw.write(f"{e}: {k}={v}\n")
        pw.write("```\n\n")
    else:
        pw.write("_No DB variables found in expected env files._\n\n")

    if sqlite_schema.strip():
        pw.write("### SQLITE SCHEMA\n\n```sql\n")
        pw.write(sqlite_schema.rstrip("\n") + "\n")
        pw.write("```\n\n")
    pw.write("---\n\n")

    pw.write("## FILE INDEX\n\n")
    for i,f in enumerate(files,1):
        pw.write(f"{i:04d}. `{f}`\n")
    pw.write("\n---\n\n")

    included = 0
    redacted = 0

    for f in files:
        try:
            p = Path(f)
            raw = p.read_bytes()
            size = len(raw)
            h = sha256_bytes(raw)
            text = read_text(f)
            if is_sensitive_file(f):
                text = redact_env(text)
                redacted += 1

            ext = p.suffix.lower().lstrip(".")
            fence = ext if ext else ""

            pw.write(f"## FILE: {f}\n\n")
            pw.write(f"- bytes: {size}\n- sha256: `{h}`\n\n")
            pw.write(f"```{fence}\n")
            pw.write(text.rstrip("\n") + "\n")
            pw.write("```\n\n---\n\n")
            included += 1
        except Exception as e:
            pw.write(f"## FILE: {f}\n\n_Unable to read: {e}_\n\n---\n\n")

    pw.close()

    idx = OUTDIR / "00_INDEX.md"
    parts = sorted([x.name for x in OUTDIR.glob(f"{prefix}_part*.md")])
    idx.write_text(
        "# WALLET_PERIMETER_FULL_V2 — Index\n\n"
        f"Generated: {TS} UTC\n\n"
        f"Parts: {len(parts)}\n"
        f"Files included: {included}\n"
        f"Redacted env-like files: {redacted}\n\n"
        "## Parts\n\n" + "\n".join([f"- {p}" for p in parts]) + "\n",
        encoding="utf-8"
    )

    print("✅ DONE:", OUTDIR)
    print("Parts:", len(parts))
    print("Files included:", included)
    print("Redacted:", redacted)

if __name__ == "__main__":
    main()
