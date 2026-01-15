#!/usr/bin/env python3
import os, re, subprocess, time
from pathlib import Path

OUTDIR = Path("docs/1234")
OUTDIR.mkdir(parents=True, exist_ok=True)

PART_LIMIT = 20 * 1024 * 1024   # 20MB на part (GitHub-friendly)
INDEX = OUTDIR / "00_INDEX.md"

# --- что включаем (как ты просил) ---
# A) Front: wallet_prod/app.html, wallet_prod/app.js, wallet_prod/modules/lgn_send.js (или где он сейчас)
FRONT_CANDIDATES = [
    "/opt/logos/www/wallet_prod",
    "/opt/logos/www/wallet-prod",
    "/opt/logos/www/wallet_dev",       # по nginx это реально живое
    "/opt/logos/www/wallet_premium",
    "/opt/logos/www/wallet",
    "/var/www/logos/wallet",
    "/var/www/logos/wallet3",
]

# B) wallet-proxy исходники
PROXY_CANDIDATES = [
    "/opt/logos/wallet-proxy",
    "/opt/logos/wallet_proxy",
    "/opt/logos/wallet-api",
    "/opt/logos/wallet_api",
]

# C) nginx vhost mw-expedition (где /node-api и /wallet-api)
NGINX_ROOTS = ["/etc/nginx/sites-enabled", "/etc/nginx/sites-available", "/etc/nginx/conf.d"]

# + env/systemd/logs (санитайзим)
ENV_CANDIDATES = [
    "/etc/logos/wallet-proxy.env",
    "/etc/logos/proxy.env",
    "/etc/logos/node-main.env",
    "/etc/logos/keys.env",
]

SYSTEMD_UNIT_CANDIDATES = [
    "logos-wallet-proxy",
    "lrb-proxy",
    "lrb-scanner",
    "logos-node@main",
    "logos-node",
    "logos_wallet_api",
    "logos_node_backend",
]

NGINX_LOGS = [
    "/var/log/nginx/error.log",
    "/var/log/nginx/access.log",
]

# --- фильтры ---
ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}

# жестко выкидываем старые мегакниги/снапшоты, чтобы не тащить мусор
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

def exists_dir(p: str) -> bool:
    return os.path.isdir(p)

def pick_first_existing_dir(cands):
    for p in cands:
        if exists_dir(p):
            return p
    return None

def is_skipped_path(p: str) -> bool:
    for s in SKIP_PATH_CONTAINS:
        if s in p:
            return True
    return False

def sanitize_text(s: str) -> str:
    # KEY=VALUE / key: value  -> value => ***
    s = re.sub(r'(?im)^(\s*(?:[A-Z0-9_]*?(?:SECRET|TOKEN|API[_-]?KEY|PRIVATE|PRIVKEY|PASSWORD|PASSWD|MNEMONIC|SEED|BEARER|AUTHORIZATION|RPC|INFURA|ALCHEMY|MORALIS|QUICKNODE|ANKR|TRONGRID|HOTWALLET|HOT_WALLET)[A-Z0-9_]*?)\s*[:=]\s*)(.+?)\s*$',
               r'\1***', s)
    # Authorization: Bearer xxx
    s = re.sub(r'(?im)^(authorization\s*:\s*bearer\s+)(.+)$', r'\1***', s)
    # url query tokens
    s = re.sub(r'(?i)([?&](?:token|apikey|api_key|key|secret|sig|signature)=)([^&\s]+)', r'\1***', s)
    # jwt-ish
    s = re.sub(r'\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9._-]{10,}\.[a-zA-Z0-9._-]{10,}\b', '***', s)
    # long hex (private keys)
    s = re.sub(r'\b[a-f0-9]{64,}\b', '***', s, flags=re.I)
    return s

def read_text_file(path: str) -> str:
    try:
        data = Path(path).read_text(errors="ignore")
    except Exception as e:
        return f"[READ ERROR] {e}\n"
    return sanitize_text(data)

def run_cmd(cmd):
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
        return sanitize_text(p.stdout)
    except Exception as e:
        return f"[CMD ERROR] {e}\n"

class PartWriter:
    def __init__(self, outdir: Path, prefix: str):
        self.outdir = outdir
        self.prefix = prefix
        self.parts = []
        self.cur = ""
        self.partno = 1

    def _flush(self):
        if not self.cur.strip():
            return
        fn = self.outdir / f"{self.prefix}_part{self.partno:03d}.md"
        fn.write_text(self.cur)
        self.parts.append(fn.name)
        self.cur = ""
        self.partno += 1

    def add_block(self, title: str, content: str):
        block = f"\n## {title}\n\n```\n{content}\n```\n"
        if len((self.cur + block).encode("utf-8")) > PART_LIMIT:
            self._flush()
        self.cur += block

    def close(self):
        self._flush()

def collect_tree(root: str, max_depth=6) -> str:
    # tree не везде стоит — делаем find
    lines = []
    root = root.rstrip("/")
    for cur, dnames, fnames in os.walk(root):
        # skip dirs
        parts = [p for p in cur.split(os.sep) if p]
        if any(d in SKIP_DIRS for d in parts):
            dnames[:] = []
            continue
        if is_skipped_path(cur):
            dnames[:] = []
            continue
        # depth limit
        rel = cur[len(root):].lstrip(os.sep)
        depth = 0 if not rel else rel.count(os.sep) + 1
        if depth > max_depth:
            dnames[:] = []
            continue

        dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
        lines.append(cur + "/")
        for f in sorted(fnames):
            if SKIP_NAME.search(f):
                continue
            lines.append("  " * (depth+1) + f)
    return "\n".join(lines) + "\n"

def find_lgn_send(front_root: str) -> str:
    # 1) точный файл
    p = Path(front_root) / "modules" / "lgn_send.js"
    if p.exists():
        return str(p)
    # 2) любой похожий
    for cur, dnames, fnames in os.walk(front_root):
        parts = [p for p in cur.split(os.sep) if p]
        if any(d in SKIP_DIRS for d in parts):
            dnames[:] = []
            continue
        for f in fnames:
            if f.lower() == "lgn_send.js":
                return str(Path(cur) / f)
            if "lgn" in f.lower() and "send" in f.lower() and f.lower().endswith(".js"):
                return str(Path(cur) / f)
    return ""

def find_nginx_vhost_files() -> list[str]:
    files = []
    for root in NGINX_ROOTS:
        if not os.path.isdir(root):
            continue
        for p in Path(root).glob("*"):
            if not p.is_file():
                continue
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            if "mw-expedition.com" in txt:
                files.append(str(p))
    return sorted(set(files))

def walk_code_dir(root: str) -> list[str]:
    res = []
    for cur, dnames, fnames in os.walk(root):
        parts = [p for p in cur.split(os.sep) if p]
        if any(d in SKIP_DIRS for d in parts):
            dnames[:] = []
            continue
        if is_skipped_path(cur):
            dnames[:] = []
            continue
        dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
        for f in sorted(fnames):
            if SKIP_NAME.search(f):
                continue
            fp = str(Path(cur) / f)
            if not ALLOW_EXT.search(f):
                continue
            res.append(fp)
    return res

def main():
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    pw = PartWriter(OUTDIR, "BOOK_1234")

    # index header
    idx = []
    idx.append("# BOOK 1234 — wallet_prod + wallet-proxy + nginx routes (sanitized)")
    idx.append("")
    idx.append(f"Generated: {ts}")
    idx.append("")
    idx.append("Secrets/tokens/keys were sanitized to `***`.")
    idx.append("")
    idx.append("## What is inside")
    idx.append("- wallet_prod (or active wallet_dev/wallet_premium/wallet) : app.html, app.js, modules/* (including lgn_send.js if exists)")
    idx.append("- wallet-proxy : full source project (text/code files, no venv)")
    idx.append("- nginx vhost(s) for mw-expedition.com (routes for /node-api and /wallet-api)")
    idx.append("- systemd units (cat) related to wallet/node/proxy/scanner")
    idx.append("- sanitized env files (wallet/proxy/node)")
    idx.append("- logs (journalctl + nginx error/access tails)")

    # --- FRONT ---
    front = pick_first_existing_dir(FRONT_CANDIDATES)
    idx.append("")
    idx.append(f"### Front root chosen: `{front}`" if front else "### Front root chosen: NOT FOUND")
    if front:
        pw.add_block(f"FRONT TREE: {front}", collect_tree(front, max_depth=6))
        # required files
        for fn in ["app.html","app.js","index.html","auth.html","auth.js","auth.css"]:
            p = str(Path(front) / fn)
            if os.path.isfile(p):
                pw.add_block(f"FRONT FILE: {p}", read_text_file(p))
        # modules full
        modules_dir = str(Path(front) / "modules")
        if os.path.isdir(modules_dir):
            pw.add_block(f"FRONT TREE modules/: {modules_dir}", collect_tree(modules_dir, max_depth=8))
            for fp in walk_code_dir(modules_dir):
                pw.add_block(f"FRONT MODULE FILE: {fp}", read_text_file(fp))
        # lgn_send explicitly
        lgn = find_lgn_send(front)
        if lgn and os.path.isfile(lgn):
            pw.add_block(f"FRONT LGN_SEND: {lgn}", read_text_file(lgn))
        else:
            pw.add_block("FRONT NOTE", f"lgn_send.js not found under {front}\n")

    # --- WALLET-PROXY ---
    proxy = pick_first_existing_dir(PROXY_CANDIDATES)
    idx.append(f"### wallet-proxy root chosen: `{proxy}`" if proxy else "### wallet-proxy root chosen: NOT FOUND")
    if proxy:
        pw.add_block(f"PROXY TREE: {proxy}", collect_tree(proxy, max_depth=8))
        # full source
        for fp in walk_code_dir(proxy):
            pw.add_block(f"PROXY FILE: {fp}", read_text_file(fp))

    # --- NGINX VHOST ---
    vhosts = find_nginx_vhost_files()
    idx.append("")
    idx.append("### nginx vhost files detected:")
    if vhosts:
        idx.extend([f"- `{p}`" for p in vhosts])
        for p in vhosts:
            pw.add_block(f"NGINX VHOST FILE: {p}", read_text_file(p))
    else:
        idx.append("- NOT FOUND (no file containing mw-expedition.com). Try: `grep -R \"mw-expedition.com\" -n /etc/nginx`")

    # also add nginx -T snippet around mw-expedition (sanitized)
    pw.add_block("NGINX -T (filtered mw-expedition.com)", run_cmd(["bash","-lc", "nginx -T 2>/dev/null | sed -n '/mw-expedition\\.com/,+260p' | head -n 400"]))

    # --- SYSTEMD UNITS (cat) ---
    pw.add_block("SYSTEMD: units list (grep logos|wallet|scanner|node)", run_cmd(["bash","-lc", "systemctl list-units --type=service --all | egrep -i 'logos|wallet|scanner|node|proxy' || true"]))
    for u in SYSTEMD_UNIT_CANDIDATES:
        pw.add_block(f"SYSTEMD CAT: {u}", run_cmd(["bash","-lc", f"systemctl cat {u} --no-pager 2>/dev/null || true"]))

    # --- ENV (sanitized) ---
    for p in ENV_CANDIDATES:
        if os.path.isfile(p):
            pw.add_block(f"ENV (sanitized): {p}", read_text_file(p))

    # --- LOGS ---
    # journalctl tails for likely services
    for u in ["logos-wallet-proxy","lrb-scanner","logos-node@main","logos-node","lrb-proxy","logos_wallet_api","logos_node_backend"]:
        pw.add_block(f"JOURNALCTL -u {u} -n 300", run_cmd(["bash","-lc", f"journalctl -u {u} -n 300 --no-pager 2>/dev/null || true"]))

    for lp in NGINX_LOGS:
        if os.path.isfile(lp):
            pw.add_block(f"NGINX LOG TAIL: {lp}", run_cmd(["bash","-lc", f"tail -n 300 {lp} 2>/dev/null || true"]))

    pw.close()

    # write index referencing parts
    parts = pw.parts[:]  # filenames
    idx.append("")
    idx.append("## Parts")
    for name in parts:
        idx.append(f"- `{name}`")
    idx.append("")
    INDEX.write_text("\n".join(idx) + "\n")

    print("✅ DONE: docs/1234")
    print("Parts:", len(parts))
    for name in parts:
        p = OUTDIR / name
        print(f"  - {name}  ({p.stat().st_size/1024/1024:.1f} MB)")
    print("Index:", str(INDEX))

if __name__ == "__main__":
    main()
