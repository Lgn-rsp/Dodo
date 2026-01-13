#!/usr/bin/env python3
import os, re, time, json, hashlib, subprocess
from pathlib import Path

TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUTDIR = Path("docs/WALLET_PERIMETER_FULL")
OUTDIR.mkdir(parents=True, exist_ok=True)

# =========================
# НАСТРОЙКИ
# =========================

# Что включаем в "полный периметр"
INCLUDE_ROOTS = [
    "/opt/logos/www/wallet_dev",
    "/opt/logos/www/wallet",
    "/opt/logos/www/wallet_premium",
    "/opt/logos/www/wallet_v2",
    "/opt/logos/wallet-proxy",
    "/var/www/logos/wallet",
    "/var/www/logos/wallet3",
    "/var/www/logos/explorer",
]

# Точечно добавим конфиги nginx/systemd/env и openapi
INCLUDE_FILES = [
    "/etc/nginx/sites-enabled/logos.conf",
    "/etc/nginx/nginx.conf",
    "/etc/systemd/system/lrb-scanner.service",
    "/etc/systemd/system/logos-wallet-proxy.service",
    "/etc/systemd/system/lrb-proxy.service",
    "/etc/logos/proxy.env",
    "/etc/logos/wallet-proxy.env",
    "/etc/logos/node-main.env",
    "/etc/logos/node-a.env",
    "/etc/logos/node-b.env",
    "/etc/logos/node-c.env",
]

# Не включаем старые мегакниги/снапшоты чтобы не тащить мусор
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

SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots","data.sled.bak"}

# Только текстовые форматы
ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt|env)$", re.I)

# Не включаем бинарь/мусор по имени
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$|\.exe$|\.so$|\.dll$)", re.I)

# Разбиваем книгу на части, чтобы GitHub нормально принимал
PART_LIMIT = 18 * 1024 * 1024  # 18MB на part (без LFS, без warning)

# Секреты: env/key/rid — значения редактируем
SENSITIVE_ENV_NAMES = re.compile(r"(SECRET|TOKEN|KEY|PASS|PASSWORD|PRIVATE|SEED|MNEMONIC|BEARER|API_KEY|BOT|TG|TELEGRAM|TWITTER|XAUTH|COOKIE|SESSION)", re.I)

def path_skip(p: str) -> bool:
    for s in SKIP_PATH_CONTAINS:
        if s in p:
            return True
    return False

def is_sensitive_file(path: str) -> bool:
    lp = path.lower()
    base = os.path.basename(path).lower()
    if "/etc/logos/" in lp:
        if base.endswith(".key") or base.endswith(".rid"):
            return True
        if base.endswith(".env") or base.endswith(".envy"):
            return True
    if base.endswith(".env"):
        return True
    return False

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
            # оставляем несекретное как есть
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def read_text_file(path: str) -> str:
    # UTF-8 with fallback
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Path(path).read_text(encoding="latin-1", errors="replace")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def add_chunk(writer, s: str):
    writer.write(s)
    writer.flush()

class PartWriter:
    def __init__(self, outdir: Path, prefix: str):
        self.outdir = outdir
        self.prefix = prefix
        self.part_no = 1
        self.cur_path = self._make_part_path()
        self.f = self.cur_path.open("w", encoding="utf-8")
        self.bytes = 0

    def _make_part_path(self):
        return self.outdir / f"{self.prefix}_part{self.part_no:03d}.md"

    def _rotate(self):
        self.f.close()
        self.part_no += 1
        self.cur_path = self._make_part_path()
        self.f = self.cur_path.open("w", encoding="utf-8")
        self.bytes = 0

    def write(self, s: str):
        b = s.encode("utf-8")
        if self.bytes + len(b) > PART_LIMIT and self.bytes > 0:
            self._rotate()
        self.f.write(s)
        self.bytes += len(b)

    def close(self):
        self.f.close()

def collect_files_from_root(root: str):
    files=[]
    if not os.path.exists(root):
        return files
    for cur, dnames, fnames in os.walk(root):
        # пропуск мусорных директорий
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
            if not ALLOW_EXT.search(n):
                continue
            files.append(p)
    return files

def collect_all():
    files=set()

    # 1) рекурсивно по корням
    for r in INCLUDE_ROOTS:
        files.update(collect_files_from_root(r))

    # 2) точечные include
    for f in INCLUDE_FILES:
        if os.path.exists(f) and not path_skip(f):
            if not SKIP_NAME.search(os.path.basename(f)):
                if ALLOW_EXT.search(f):
                    files.add(f)

    # 3) openapi (из wallet-proxy если есть)
    #    плюс попробуем скачать с локального /wallet-api/openapi.json или /node-api/openapi.json если доступно
    candidates = [
        "/opt/logos/wallet-proxy/openapi.json",
        "/opt/logos/wallet-proxy/openapi.yaml",
        "/opt/logos/wallet-proxy/openapi.yml",
    ]
    for c in candidates:
        if os.path.exists(c):
            files.add(c)

    return sorted(files)

def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return e.output

def main():
    files = collect_all()

    # Инвентарь версий кошелька (что есть)
    inventory_paths = [
        "/opt/logos/www",
        "/var/www/logos",
    ]
    inventory = []
    for base in inventory_paths:
        if not os.path.isdir(base): 
            continue
        try:
            for name in sorted(os.listdir(base)):
                if "wallet" in name.lower():
                    inventory.append(os.path.join(base, name))
        except Exception:
            pass

    # nginx vhost mw-expedition.com (кусок)
    nginx_T = run(["bash","-lc","nginx -T 2>/dev/null || true"])
    vhost_block = ""
    if nginx_T:
        # вырежем server block по mw-expedition.com
        m = re.search(r"server\s*\{.*?server_name\s+mw-expedition\.com.*?\n\}", nginx_T, flags=re.S)
        if m:
            vhost_block = m.group(0)

    # systemd cat (важные сервисы)
    node_unit = run(["bash","-lc","systemctl cat logos-node@main --no-pager 2>/dev/null || true"])
    scanner_unit = run(["bash","-lc","systemctl cat lrb-scanner --no-pager 2>/dev/null || true"])
    proxy_unit = run(["bash","-lc","systemctl cat logos-wallet-proxy --no-pager 2>/dev/null || true"])
    node_show = run(["bash","-lc","systemctl show -p ExecStart -p WorkingDirectory logos-node@main --no-pager 2>/dev/null || true"])

    # начнем писать книгу
    prefix="WALLET_PERIMETER_FULL"
    pw = PartWriter(OUTDIR, prefix)

    # HEADER
    pw.write(f"# LOGOS — WALLET PERIMETER FULL BOOK\n\n")
    pw.write(f"_Generated: {TS} UTC_\n\n")
    pw.write("**Includes:** wallet_dev + wallet prod variants + wallet-proxy + nginx + systemd + openapi + inventory.\n\n")
    pw.write("---\n\n")

    # INVENTORY
    pw.write("## INVENTORY (wallet folders found)\n\n")
    for p in inventory:
        pw.write(f"- {p}\n")
    pw.write("\n---\n\n")

    # NGINX
    pw.write("## NGINX (mw-expedition.com vhost)\n\n")
    if vhost_block.strip():
        pw.write("```nginx\n")
        pw.write(vhost_block.strip() + "\n")
        pw.write("```\n\n")
    else:
        pw.write("_Could not extract mw-expedition.com server block from `nginx -T`._\n\n")
    pw.write("---\n\n")

    # SYSTEMD
    pw.write("## SYSTEMD (units)\n\n")
    pw.write("### logos-node@main\n\n```ini\n" + (node_unit.strip() or "N/A") + "\n```\n\n")
    pw.write("### logos-node@main (show)\n\n```txt\n" + (node_show.strip() or "N/A") + "\n```\n\n")
    pw.write("### lrb-scanner\n\n```ini\n" + (scanner_unit.strip() or "N/A") + "\n```\n\n")
    pw.write("### logos-wallet-proxy\n\n```ini\n" + (proxy_unit.strip() or "N/A") + "\n```\n\n")
    pw.write("---\n\n")

    # FILE INDEX
    pw.write("## FILE INDEX\n\n")
    for i, f in enumerate(files, 1):
        pw.write(f"{i:04d}. `{f}`\n")
    pw.write("\n---\n\n")

    # FULL FILES
    included = 0
    redacted = 0

    for f in files:
        try:
            p = Path(f)
            raw = p.read_bytes()
            h = sha256_bytes(raw)
            size = len(raw)

            pw.write(f"## FILE: {f}\n\n")
            pw.write(f"- bytes: {size}\n- sha256: `{h}`\n\n")

            text = read_text_file(f)
            if is_sensitive_file(f):
                text = redact_env(text)
                redacted += 1

            # code fence by ext
            ext = p.suffix.lower().lstrip(".")
            fence = ext if ext else ""
            pw.write(f"```{fence}\n")
            pw.write(text.rstrip("\n") + "\n")
            pw.write("```\n\n---\n\n")
            included += 1

        except Exception as e:
            pw.write(f"## FILE: {f}\n\n_Unable to read: {e}_\n\n---\n\n")

    pw.close()

    # INDEX FILE
    idx = OUTDIR / "00_INDEX.md"
    parts = sorted([x.name for x in OUTDIR.glob(f"{prefix}_part*.md")])
    idx.write_text(
        "# WALLET_PERIMETER_FULL — Index\n\n"
        f"Generated: {TS} UTC\n\n"
        f"Parts: {len(parts)}\n\n"
        "## Parts\n\n" +
        "\n".join([f"- {p}" for p in parts]) +
        "\n",
        encoding="utf-8"
    )

    print("✅ DONE:", OUTDIR)
    print("Parts:", len(parts))
    print("Files included:", included)
    print("Redacted env-like files:", redacted)

if __name__ == "__main__":
    main()
