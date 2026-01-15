#!/usr/bin/env python3
import os, re, subprocess, time
from pathlib import Path

OUTDIR = Path("docs/12345")
OUTDIR.mkdir(parents=True, exist_ok=True)
INDEX = OUTDIR / "00_INDEX.md"
PART_LIMIT = 20 * 1024 * 1024

# включаем целиком: фронт + proxy + nginx vhost
FRONT_ROOTS = [
  "/opt/logos/www/wallet_prod",
  "/opt/logos/www/wallet_dev",
  "/opt/logos/www/wallet_premium",
  "/opt/logos/www/wallet",
  "/var/www/logos/wallet",
  "/var/www/logos/wallet3",
]
PROXY_ROOTS = [
  "/opt/logos/wallet-proxy",
  "/opt/logos/wallet-api",
  "/opt/logos/wallet_api",
]
NGINX_ROOTS = ["/etc/nginx/sites-enabled", "/etc/nginx/sites-available", "/etc/nginx/conf.d"]

ENV_FILES = [
  "/etc/logos/wallet-proxy.env",
  "/etc/logos/proxy.env",
  "/etc/logos/node-main.env",
  "/etc/logos/keys.env",
]
SYSTEMD_UNITS = [
  "logos-wallet-proxy","lrb-proxy","lrb-scanner","logos-node@main","logos-node","logos_wallet_api","logos_node_backend"
]
NGINX_LOGS = ["/var/log/nginx/error.log","/var/log/nginx/access.log"]

ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}

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

def is_skipped_path(p: str) -> bool:
  return any(s in p for s in SKIP_PATH_CONTAINS)

def sanitize_env_or_logs(s: str) -> str:
  # только env/logs: режем секреты, но НЕ трогаем код
  s = re.sub(r'(?im)^(\s*(?:[A-Z0-9_]*?(?:SECRET|TOKEN|API[_-]?KEY|PRIVATE|PRIVKEY|PASSWORD|PASSWD|MNEMONIC|SEED|BEARER|AUTHORIZATION|RPC|INFURA|ALCHEMY|MORALIS|QUICKNODE|ANKR|TRONGRID|HOTWALLET|HOT_WALLET)[A-Z0-9_]*?)\s*[:=]\s*)(.+?)\s*$',
             r'\1***', s)
  s = re.sub(r'(?im)^(authorization\s*:\s*bearer\s+)(.+)$', r'\1***', s)
  return s

def pick_first_dir(cands):
  for p in cands:
    if os.path.isdir(p):
      return p
  return None

def collect_tree(root: str, max_depth=7) -> str:
  root=root.rstrip("/")
  out=[]
  for cur, dnames, fnames in os.walk(root):
    parts=[p for p in cur.split(os.sep) if p]
    if any(d in SKIP_DIRS for d in parts):
      dnames[:] = []
      continue
    if is_skipped_path(cur):
      dnames[:] = []
      continue
    rel = cur[len(root):].lstrip(os.sep)
    depth = 0 if not rel else rel.count(os.sep)+1
    if depth>max_depth:
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
    out.append(cur + "/")
    for f in sorted(fnames):
      if SKIP_NAME.search(f): 
        continue
      out.append("  "*(depth+1) + f)
  return "\n".join(out) + "\n"

def walk_files(root: str):
  res=[]
  for cur, dnames, fnames in os.walk(root):
    parts=[p for p in cur.split(os.sep) if p]
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
      if not ALLOW_EXT.search(f): 
        continue
      res.append(str(Path(cur)/f))
  return res

def read_text(path: str) -> str:
  try:
    return Path(path).read_text(errors="ignore")
  except Exception as e:
    return f"[READ ERROR] {e}\n"

def run(cmd: str) -> str:
  p = subprocess.run(["bash","-lc",cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  return p.stdout

class PartWriter:
  def __init__(self, prefix: str):
    self.prefix=prefix
    self.part=1
    self.cur=""
    self.parts=[]
  def add(self, title: str, body: str):
    block = f"\n## {title}\n\n```\\n{body}\\n```\\n"
    if len((self.cur+block).encode("utf-8")) > PART_LIMIT:
      self.flush()
    self.cur += block
  def flush(self):
    if not self.cur.strip(): 
      return
    fn = OUTDIR / f"{self.prefix}_part{self.part:03d}.md"
    fn.write_text(self.cur)
    self.parts.append(fn.name)
    self.part += 1
    self.cur=""
  def close(self):
    self.flush()

def main():
  ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
  pw = PartWriter("BOOK_12345")

  front = pick_first_dir(FRONT_ROOTS)
  proxy = pick_first_dir(PROXY_ROOTS)

  idx=[]
  idx.append("# BOOK 12345 — Wallet+ Full Perimeter (run-ready code, sanitized env/logs)")
  idx.append(f"Generated: {ts}")
  idx.append("")
  idx.append("Code is included **as-is** (no redactions inside code).")
  idx.append("Only ENV and logs are sanitized to `***`.")
  idx.append("")
  idx.append(f"- Front root: `{front}`" if front else "- Front root: NOT FOUND")
  idx.append(f"- Proxy root: `{proxy}`" if proxy else "- Proxy root: NOT FOUND")

  # FRONT
  if front:
    pw.add(f"FRONT TREE: {front}", collect_tree(front))
    for fp in walk_files(front):
      pw.add(f"FRONT FILE: {fp}", read_text(fp))

  # PROXY
  if proxy:
    pw.add(f"PROXY TREE: {proxy}", collect_tree(proxy, max_depth=10))
    for fp in walk_files(proxy):
      pw.add(f"PROXY FILE: {fp}", read_text(fp))

  # NGINX vhost mw-expedition
  vhosts=[]
  for root in NGINX_ROOTS:
    if not os.path.isdir(root): 
      continue
    for p in Path(root).glob("*"):
      if not p.is_file(): 
        continue
      try:
        t = p.read_text(errors="ignore")
      except Exception:
        continue
      if "mw-expedition.com" in t:
        vhosts.append(str(p))
  vhosts=sorted(set(vhosts))
  idx.append("")
  idx.append("## Nginx vhosts detected (mw-expedition.com):")
  idx.extend([f"- `{p}`" for p in vhosts]) if vhosts else idx.append("- NOT FOUND")

  for p in vhosts:
    pw.add(f"NGINX VHOST FILE: {p}", read_text(p))

  pw.add("NGINX -T (mw-expedition snippet)", run("nginx -T 2>/dev/null | sed -n '/mw-expedition\\.com/,+280p' | head -n 500"))

  # SYSTEMD
  pw.add("SYSTEMD list (logos|wallet|node|proxy|scanner)", run("systemctl list-units --type=service --all | egrep -i 'logos|wallet|scanner|node|proxy' || true"))
  for u in SYSTEMD_UNITS:
    pw.add(f"SYSTEMD CAT: {u}", run(f"systemctl cat {u} --no-pager 2>/dev/null || true"))

  # ENV (sanitized)
  for p in ENV_FILES:
    if os.path.isfile(p):
      pw.add(f"ENV SANITIZED: {p}", sanitize_env_or_logs(read_text(p)))

  # LOGS (sanitized)
  for u in ["logos-wallet-proxy","lrb-scanner","logos-node@main","logos-node","lrb-proxy","logos_wallet_api","logos_node_backend"]:
    pw.add(f"JOURNALCTL -u {u} -n 300", sanitize_env_or_logs(run(f"journalctl -u {u} -n 300 --no-pager 2>/dev/null || true")))
  for lp in NGINX_LOGS:
    if os.path.isfile(lp):
      pw.add(f"NGINX LOG TAIL: {lp}", sanitize_env_or_logs(run(f"tail -n 300 {lp} 2>/dev/null || true")))

  # PROD+ plan note (topup derived addresses etc.)
  pw.add("BRIDGE PROD+ FIX PLAN (no secrets)", """\
1) Remove any HOT single-address topup:
   - Introduce HD derivation for deposit addresses (ETH first).
   - Store mapping: rid -> index -> deposit_address in DB.
   - Secrets only in /etc/logos/wallet-proxy.env:
     * ETH_DEPOSIT_XPRV or ETH_DEPOSIT_SEED (never in code/books)

2) Scanner:
   - Watch deposits to derived addresses
   - Resolve to rid via DB mapping
   - Emit rLGN mint / credit event

3) Withdraw:
   - Enforce decimals conversion (USDT=6)
   - idempotency by request_id
   - status pipeline: pending -> processing -> done/failed
""")

  pw.close()

  idx.append("")
  idx.append("## Parts")
  for name in pw.parts:
    idx.append(f"- `{name}`")
  INDEX.write_text("\n".join(idx) + "\n")

  print("✅ DONE: docs/12345")
  print("Parts:", len(pw.parts))
  for name in pw.parts:
    p = OUTDIR / name
    print(f" - {name}: {p.stat().st_size/1024/1024:.1f} MB")
  print("Index:", str(INDEX))

if __name__=="__main__":
  main()
