#!/usr/bin/env python3
import os, re, time, subprocess
from pathlib import Path

OUTDIR = Path("docs/123456")
OUTDIR.mkdir(parents=True, exist_ok=True)
INDEX = OUTDIR / "00_INDEX.md"
PART_LIMIT = 20 * 1024 * 1024  # 20MB/part

SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
ALLOW_CODE = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)

# в книге НЕ тащим старые мегакниги/снапшоты
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

def run(cmd: str) -> str:
  p = subprocess.run(["bash","-lc",cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  return p.stdout

def sanitize_env_or_logs(s: str) -> str:
  # режем только env/logs: значения секретных переменных -> ***
  s = re.sub(
    r'(?im)^(\s*(?:[A-Z0-9_]*?(?:SECRET|TOKEN|API[_-]?KEY|PRIVATE|PRIVKEY|PASSWORD|PASSWD|MNEMONIC|SEED|BEARER|AUTHORIZATION|RPC|INFURA|ALCHEMY|MORALIS|QUICKNODE|ANKR|TRONGRID|HOTWALLET|HOT_WALLET|XPRV|XSEED)[A-Z0-9_]*?)\s*[:=]\s*)(.+?)\s*$',
    r'\1***', s
  )
  s = re.sub(r'(?im)^(authorization\s*:\s*bearer\s+)(.+)$', r'\1***', s)
  return s

def collect_tree(root: str, max_depth=8) -> str:
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

def read_text(path: str) -> str:
  try:
    return Path(path).read_text(errors="ignore")
  except Exception as e:
    return f"[READ ERROR] {e}\n"

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
      if not ALLOW_CODE.search(f):
        continue
      res.append(str(Path(cur)/f))
  return res

def find_service_unit(regex: str):
  # берём активный или любой подходящий
  out = run("systemctl list-units --type=service --all --no-pager")
  cand=[]
  for line in out.splitlines():
    if re.search(regex, line, re.I):
      unit=line.split()[0]
      cand.append(unit)
  return cand

def systemd_cat(unit: str) -> str:
  return run(f"systemctl cat {unit} --no-pager 2>/dev/null || true")

def systemd_show(unit: str) -> str:
  return run(f"systemctl show {unit} -p WorkingDirectory -p ExecStart -p EnvironmentFiles --no-pager 2>/dev/null || true")

def parse_workdir_execstart(show_text: str):
  wd=None
  ex=None
  for ln in show_text.splitlines():
    if ln.startswith("WorkingDirectory="):
      wd=ln.split("=",1)[1].strip() or None
    if ln.startswith("ExecStart="):
      ex=ln.split("=",1)[1].strip() or None
  return wd, ex

def extract_paths_from_execstart(execstart: str):
  # вытащим /opt/... и /root/... пути
  if not execstart: return []
  return sorted(set(re.findall(r'(/(?:opt|root|var|etc)[^ ;,\]]+)', execstart)))

def grep_pick_files(root: str, patterns, exts=(".py",".rs",".toml",".yml",".yaml",".conf",".ini",".service",".js",".ts",".tsx")):
  found=set()
  for cur, dnames, fnames in os.walk(root):
    parts=[p for p in cur.split(os.sep) if p]
    if any(d in SKIP_DIRS for d in parts):
      dnames[:] = []
      continue
    if is_skipped_path(cur):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
    for fn in fnames:
      p=Path(cur)/fn
      if not p.suffix.lower() in exts:
        continue
      if SKIP_NAME.search(fn):
        continue
      try:
        s=p.read_text(errors="ignore")
      except:
        continue
      for pat in patterns:
        if re.search(pat, s, re.I):
          found.add(str(p))
          break
  return sorted(found)

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
  pw = PartWriter("BOOK_123456")

  idx=[]
  idx.append("# BOOK 123456 — Wallet+ Bridges Minimal Perimeter (run-ready code)")
  idx.append(f"Generated: {ts}")
  idx.append("")
  idx.append("Includes only modules needed for:")
  idx.append("- RID→addresses address-book mapping")
  idx.append("- deposit watchers (ETH/ERC20, TRON/TRC20, BTC if exists)")
  idx.append("- redeem/payout (withdraw signing/sending + confirmations)")
  idx.append("- statuses + idempotency + durable journal")
  idx.append("- node bridge endpoints & ledger linkage")
  idx.append("- nginx routing + systemd + sanitized env/logs")
  idx.append("")
  idx.append("CODE IS INCLUDED AS-IS (no redactions in code). Only ENV and logs are sanitized to ***.")
  idx.append("")

  # ---- systemd units ----
  proxy_units = find_service_unit(r'(wallet|proxy).*service|logos-wallet-proxy|lrb-proxy')
  node_units  = find_service_unit(r'logos-node(@main)?\.service|logos-node@main|logos-node-backend|logos_node_backend')
  scanner_units = find_service_unit(r'scanner|lrb-scanner')

  idx.append("## Detected systemd units")
  idx.append("### wallet/proxy")
  idx += [f"- `{u}`" for u in proxy_units] if proxy_units else ["- NOT FOUND"]
  idx.append("### node backend")
  idx += [f"- `{u}`" for u in node_units] if node_units else ["- NOT FOUND"]
  idx.append("### scanner/watchers")
  idx += [f"- `{u}`" for u in scanner_units] if scanner_units else ["- NOT FOUND"]

  # cat + show
  for u in (proxy_units + node_units + scanner_units):
    pw.add(f"SYSTEMD SHOW: {u}", systemd_show(u))
    pw.add(f"SYSTEMD CAT: {u}", systemd_cat(u))

  # ---- derive actual code roots from units (WorkingDirectory/ExecStart) ----
  code_roots=set()

  for u in (proxy_units + node_units + scanner_units):
    st = systemd_show(u)
    wd, ex = parse_workdir_execstart(st)
    if wd and os.path.isdir(wd):
      code_roots.add(wd)
    for p in extract_paths_from_execstart(ex or ""):
      if os.path.isdir(p):
        code_roots.add(p)
      elif os.path.isfile(p):
        code_roots.add(str(Path(p).parent))

  # fallback known locations
  for p in ["/opt/logos/wallet-proxy", "/root/logos_lrb", "/root/logos_lrb/node", "/root/logos_lrb/src", "/opt/logos/configs", "/opt/logos/bin"]:
    if os.path.exists(p):
      code_roots.add(p)

  code_roots = sorted(code_roots)

  idx.append("")
  idx.append("## Code roots used")
  for r in code_roots:
    idx.append(f"- `{r}`")

  # ---- include nginx vhost mw-expedition ----
  vhosts=[]
  for root in ["/etc/nginx/sites-enabled", "/etc/nginx/sites-available", "/etc/nginx/conf.d"]:
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
  idx.append("## Nginx vhosts (mw-expedition.com)")
  idx += [f"- `{p}`" for p in vhosts] if vhosts else ["- NOT FOUND"]

  for p in vhosts:
    pw.add(f"NGINX VHOST FILE: {p}", read_text(p))
  pw.add("NGINX -T (mw-expedition snippet)", run("nginx -T 2>/dev/null | sed -n '/mw-expedition\\.com/,+320p' | head -n 800"))

  # ---- pick minimal wallet-proxy modules: addressbook/watchers/payout/status/idempotency/db ----
  proxy_like=[r for r in code_roots if "wallet-proxy" in r or "wallet_proxy" in r or "wallet-api" in r or "wallet_api" in r]
  if proxy_like:
    proxy_root = proxy_like[0]
    pw.add(f"PROXY TREE (focus): {proxy_root}", collect_tree(proxy_root, max_depth=10))

    patterns = [
      r'\brid\b', r'address', r'addrbook', r'deposit', r'receive',
      r'xpub', r'derive', r'hd', r'BIP32', r'BIP44',
      r'watch', r'scanner', r'confirm', r'confirmations',
      r'withdraw', r'payout', r'send_raw', r'sign', r'private',
      r'idempot', r'journal', r'status', r'request_id', r'ext_txid',
      r'sqlite|postgres|db_path|DATABASE|DSN'
    ]
    picked = grep_pick_files(proxy_root, patterns, exts=(".py",".sh",".toml",".yml",".yaml",".ini",".conf",".md",".txt",".json"))
    idx.append("")
    idx.append("## wallet-proxy picked files (by patterns)")
    idx += [f"- `{p}`" for p in picked] if picked else ["- NONE FOUND"]

    for fp in picked:
      pw.add(f"PROXY FILE: {fp}", read_text(fp))

  # ---- node bridge / ledger linkage minimal ----
  node_like=[]
  for r in code_roots:
    if "/root/logos_lrb" in r:
      node_like.append(r)
  # ensure main rust roots
  for r in ["/root/logos_lrb/node","/root/logos_lrb/src","/root/logos_lrb/lrb_core","/root/logos_lrb/core","/root/logos_lrb/modules"]:
    if os.path.isdir(r) and r not in node_like:
      node_like.append(r)
  node_like = sorted(set(node_like))

  patterns_node = [
    r'\bbridge\b', r'deposit', r'redeem', r'withdraw',
    r'idempot', r'journal', r'durable', r'event', r'archive', r'history',
    r'submit_tx', r'nonce', r'\bbalance\b', r'wallet-api', r'wallet_api'
  ]

  node_picked=set()
  for nr in node_like:
    if not os.path.isdir(nr): 
      continue
    for fp in grep_pick_files(nr, patterns_node, exts=(".rs",".toml",".yml",".yaml",".md",".txt",".json",".conf",".ini")):
      node_picked.add(fp)
  node_picked=sorted(node_picked)

  idx.append("")
  idx.append("## node backend picked files (bridge/ledger/status/idempotency)")
  idx += [f"- `{p}`" for p in node_picked] if node_picked else ["- NONE FOUND"]

  for fp in node_picked:
    pw.add(f"NODE FILE: {fp}", read_text(fp))

  # ---- env files (sanitized, but variable names preserved) ----
  env_candidates = [
    "/etc/logos/wallet-proxy.env", "/etc/logos/proxy.env",
    "/etc/logos/node-main.env", "/etc/logos/keys.env",
    "/etc/logos/node-a.env", "/etc/logos/node-b.env", "/etc/logos/node-c.env",
  ]
  for p in env_candidates:
    if os.path.isfile(p):
      pw.add(f"ENV SANITIZED: {p}", sanitize_env_or_logs(read_text(p)))

  # ---- logs around failure (sanitized) ----
  # user asked 2 services: logos_wallet_api, logos_node_backend — might not exist, so we include detected units too
  log_units = sorted(set(proxy_units + node_units + scanner_units + ["logos_wallet_api","logos_node_backend"]))
  for u in log_units:
    pw.add(f"JOURNALCTL -u {u} -n 300", sanitize_env_or_logs(run(f"journalctl -u {u} -n 300 --no-pager 2>/dev/null || true")))

  for lp in ["/var/log/nginx/error.log","/var/log/nginx/access.log"]:
    if os.path.isfile(lp):
      pw.add(f"NGINX LOG TAIL: {lp}", sanitize_env_or_logs(run(f"tail -n 400 {lp} 2>/dev/null || true")))

  pw.close()

  idx.append("")
  idx.append("## Parts")
  for name in pw.parts:
    idx.append(f"- `{name}`")

  INDEX.write_text("\n".join(idx) + "\n")

  print("✅ DONE: docs/123456")
  print("Parts:", len(pw.parts))
  for name in pw.parts:
    p = OUTDIR / name
    print(f" - {name}: {p.stat().st_size/1024/1024:.1f} MB")
  print("Index:", str(INDEX))

if __name__=="__main__":
  main()
