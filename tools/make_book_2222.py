#!/usr/bin/env python3
import os, re, time, subprocess, argparse
from pathlib import Path

PART_LIMIT = 20 * 1024 * 1024  # 20MB per part for GitHub
OUTDIR = Path("docs/2222")

CODE_ROOTS = [
  "/root/logos_lrb",
  "/opt/logos",
  "/opt/logos/bin",
  "/opt/logos/configs",
]

WALLET_FRONT_ROOTS = [
  "/opt/logos/www/wallet_dev",
  "/opt/logos/www/wallet",
  "/opt/logos/www/wallet_prod",
  "/opt/logos/www/wallet_premium",
  "/var/www/logos/wallet",
  "/var/www/logos/wallet3",
]

NGINX_CONF_PATHS = [
  "/etc/nginx/nginx.conf",
  "/etc/nginx/sites-enabled",
  "/etc/nginx/sites-available",
]

NGINX_LOGS = [
  "/var/log/nginx/access.log",
  "/var/log/nginx/error.log",
]

NODE_API_UNITS_CANDIDATES = [
  "logos-node@main",
  "logos-node",
  "logos-node.service",
  "logos-node@main.service",
]

WALLET_API_UNITS_CANDIDATES = [
  "logos-wallet-proxy",
  "lrb-proxy",
  "lrb-scanner",
  "logos-wallet-proxy.service",
  "lrb-proxy.service",
  "lrb-scanner.service",
]

ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt|env)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.exe$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
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

SENSITIVE_ENV_KEYS = re.compile(r"(?i)\b(secret|token|apikey|api_key|private|privkey|password|passwd|mnemonic|seed|sign_key|bearer|key)\b")
RID_KEY_FILES = re.compile(r"(?i)\.(key|rid)$")

def sh(cmd: str) -> str:
  try:
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
  except subprocess.CalledProcessError as e:
    return e.output or ""

def q(s: str) -> str:
  return "'" + s.replace("'", "'\"'\"'") + "'"

def is_skipped_path(p: str) -> bool:
  return any(s in p for s in SKIP_PATH_CONTAINS)

def fence_lang(path: str) -> str:
  ext = Path(path).suffix.lower().lstrip(".")
  return ext if ext else ""

def redact_text(path: str, text: str) -> str:
  base = os.path.basename(path)
  if RID_KEY_FILES.search(path):
    return "REDACTED (sensitive key/rid file)\n"
  if base.endswith(".env") or ".env" in base or base in ("proxy.env","wallet-proxy.env","keys.env","keys.envy"):
    out_lines = []
    for line in text.splitlines(True):
      if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1)
        if SENSITIVE_ENV_KEYS.search(k):
          out_lines.append(f"{k}=REDACTED\n")
        else:
          out_lines.append(line)
      else:
        out_lines.append(line)
    return "".join(out_lines)
  return text

def walk_files(root: str):
  for cur, dnames, fnames in os.walk(root):
    parts = [x for x in cur.split("/") if x]
    if any(d in parts for d in SKIP_DIRS):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
    for n in fnames:
      if SKIP_NAME.search(n):
        continue
      p = os.path.join(cur, n)
      if is_skipped_path(p):
        continue
      if not ALLOW_EXT.search(n):
        continue
      yield p

class BookWriter:
  def __init__(self, outdir: Path):
    self.outdir = outdir
    self.part_idx = 1
    self.cur_bytes = 0
    self.files_embedded = 0
    self._open()

  def _path(self) -> Path:
    return self.outdir / f"2222_part{self.part_idx:03d}.md"

  def _open(self):
    self.cur_path = self._path()
    self.f = self.cur_path.open("w", encoding="utf-8", errors="replace")

  def _rotate(self):
    self.f.close()
    self.part_idx += 1
    self.cur_bytes = 0
    self._open()

  def write(self, s: str):
    b = len(s.encode("utf-8", errors="replace"))
    if self.cur_bytes + b > PART_LIMIT and self.cur_bytes > 0:
      self._rotate()
    self.f.write(s)
    self.cur_bytes += b

  def close(self):
    self.f.close()

def add_cmd(w: BookWriter, title: str, cmd: str):
  w.write(f"\n\n## {title}\n\n**CMD:** `{cmd}`\n\n```text\n")
  out = sh(cmd)
  w.write(out.rstrip() + "\n")
  w.write("```\n")

def add_file(w: BookWriter, path: str):
  try:
    txt = Path(path).read_text(encoding="utf-8", errors="replace")
  except Exception as e:
    w.write(f"\n\n### FILE: {path}\n\n```text\nREAD_ERROR: {e}\n```\n")
    return
  txt = redact_text(path, txt)
  lang = fence_lang(path)
  w.write(f"\n\n### FILE: {path}\n\n```{lang}\n")
  w.write(txt.rstrip("\n") + "\n")
  w.write("```\n")
  w.files_embedded += 1

def detect_unit(cands):
  for u in cands:
    out = sh(f"systemctl status {q(u)} --no-pager 2>/dev/null | head -n 1")
    if out.strip():
      return u
  return ""

def find_node_api_sources():
  patterns = [
    "submit_tx","/submit_tx","balance","/balance","nonce","/nonce",
    "debug_canon","axum","Router","route(","post(","get(",
    "balance/{rid}","submit_tx_batch",
  ]
  found = set()
  for root in CODE_ROOTS:
    if not os.path.isdir(root):
      continue
    for ptn in patterns:
      cmd = (
        "grep -R --line-number -I --binary-files=without-match "
        "--exclude-dir=.git --exclude-dir=target --exclude-dir=node_modules "
        "--exclude-dir=venv --exclude-dir=.venv --exclude-dir=__pycache__ "
        f"{q(ptn)} {q(root)} 2>/dev/null | head -n 600"
      )
      out = sh(cmd)
      for line in out.splitlines():
        m = re.match(r"^([^:]+):\d+:", line)
        if not m:
          continue
        fp = m.group(1)
        if is_skipped_path(fp):
          continue
        if os.path.isfile(fp) and ALLOW_EXT.search(fp) and not SKIP_NAME.search(fp):
          found.add(fp)
  return sorted(found)

def collect_env_for_node():
  envs = []
  cands = [
    "/etc/logos/node-main.env",
    "/etc/logos/node-a.env",
    "/etc/logos/node-b.env",
    "/etc/logos/node-c.env",
    "/etc/logos/keys.env",
    "/etc/logos/keys.envy",
    "/etc/logos/genesis.yaml",
  ]
  for p in cands:
    if os.path.isfile(p):
      envs.append(p)
  out = sh("ls -1 /etc/logos/node-*.env 2>/dev/null || true")
  for line in out.splitlines():
    lp = line.strip()
    if lp and os.path.isfile(lp):
      envs.append(lp)
  return sorted(set(envs))

def collect_front_send_files():
  rels = ["modules/lgn_send.js","app.js","auth.js"]
  found = []
  modules_dirs = []
  for root in WALLET_FRONT_ROOTS:
    if not os.path.isdir(root):
      continue
    for r in rels:
      p = os.path.join(root, r)
      if os.path.isfile(p):
        found.append(p)
    md = os.path.join(root, "modules")
    if os.path.isdir(md):
      modules_dirs.append(md)
  return sorted(set(found)), sorted(set(modules_dirs))

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--since", default="10 minutes ago")
  ap.add_argument("--until", default="now")
  args = ap.parse_args()

  OUTDIR.mkdir(parents=True, exist_ok=True)

  (OUTDIR / "00_INDEX.md").write_text(
    "# BOOK 2222 — Node-API backend + logs around send failure + LGN send frontend\n\n"
    f"Generated: {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}\n"
    f"Window: since={args.since} until={args.until}\n\n"
    "Includes:\n"
    "- node-api: systemd + env/configs + detected sources for /node-api/balance and /node-api/submit_tx\n"
    "- logs: journalctl node-api + nginx access/error filtered for submit_tx\n"
    "- frontend: modules/lgn_send.js + app.js + auth.js (+ full modules dirs if present)\n\n"
    "Secrets in env are REDACTED.\n",
    encoding="utf-8"
  )

  w = BookWriter(OUTDIR)
  w.write(f"# BOOK 2222\n\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}\n\n---\n")

  node_unit = detect_unit(NODE_API_UNITS_CANDIDATES)
  wallet_unit = detect_unit(WALLET_API_UNITS_CANDIDATES)

  w.write("\n## DETECTED SERVICES\n\n```text\n")
  w.write(f"node-api unit: {node_unit or 'NOT FOUND'}\n")
  w.write(f"wallet-api/proxy unit: {wallet_unit or 'NOT FOUND'}\n")
  w.write("```\n")

  w.write("\n---\n# A) NODE-API BACKEND\n")
  if node_unit:
    add_cmd(w, f"systemctl cat {node_unit}", f"systemctl cat {q(node_unit)} --no-pager 2>/dev/null || true")
    add_cmd(w, f"systemctl show {node_unit}", f"systemctl show -p FragmentPath -p WorkingDirectory -p ExecStart -p EnvironmentFile {q(node_unit)} --no-pager 2>/dev/null || true")
    add_cmd(w, f"journalctl {node_unit} (window)", f"journalctl -u {q(node_unit)} --since {q(args.since)} --until {q(args.until)} --no-pager 2>/dev/null || true")
  else:
    w.write("\n```text\nNOT FOUND via candidates. Run: systemctl list-units | grep -i logos\n```\n")

  w.write("\n## Node env/configs (/etc/logos)\n")
  for p in collect_env_for_node():
    add_file(w, p)

  w.write("\n---\n# B) NGINX ROUTES + LOGS (submit_tx)\n")
  for p in NGINX_CONF_PATHS:
    if os.path.isdir(p):
      for f in sorted(walk_files(p)):
        add_file(w, f)
    elif os.path.isfile(p):
      add_file(w, p)

  add_cmd(
    w,
    "nginx -T filtered (mw-expedition.com + routing)",
    r"nginx -T 2>/dev/null | grep -nE 'server_name mw-expedition\.com|upstream logos_node_backend|upstream logos_wallet_api|location|proxy_pass|/node-api/|/wallet-api/|/api/' | head -n 600"
  )

  for lp in NGINX_LOGS:
    if os.path.isfile(lp):
      add_cmd(w, f"nginx grep submit_tx: {lp}", f"grep -nEi 'submit_tx|/node-api/|/api/submit_tx' {q(lp)} | tail -n 800 || true")

  w.write("\n---\n# C) FRONTEND FILES (LGN SEND)\n")
  found_send, modules_dirs = collect_front_send_files()

  w.write("\n## Found key frontend files\n\n```text\n" + ("\n".join(found_send) if found_send else "NONE") + "\n```\n")
  for p in found_send:
    add_file(w, p)

  for md in modules_dirs:
    w.write(f"\n## FULL MODULES DIR: {md}\n")
    for f in sorted(walk_files(md)):
      add_file(w, f)

  w.write("\n---\n# D) NODE-API SOURCES (FOUND BY GREP)\n")
  rel = find_node_api_sources()
  w.write(f"\nFound files: {len(rel)}\n\n```text\n" + ("\n".join(rel) if rel else "NONE") + "\n```\n")
  for f in rel:
    add_file(w, f)

  # bonus: binary fingerprints if node is binary-only
  add_cmd(w, "logos_node binary fingerprints", "ls -lah /opt/logos/bin/logos_node 2>/dev/null || true; sha256sum /opt/logos/bin/logos_node 2>/dev/null || true; file /opt/logos/bin/logos_node 2>/dev/null || true")

  w.close()
  parts = sorted(OUTDIR.glob("2222_part*.md"))
  (OUTDIR / "99_SUMMARY.txt").write_text(
    "BOOK 2222 generated.\n"
    f"Parts: {len(parts)}\n"
    + "\n".join([f"{p.name}  {p.stat().st_size/1024/1024:.2f} MB" for p in parts])
    + f"\n\nFiles embedded: {w.files_embedded}\n",
    encoding="utf-8"
  )

  print(f"✅ DONE: {OUTDIR}")
  print(f"Parts: {len(parts)}")
  print(f"Files embedded: {w.files_embedded}")

if __name__ == "__main__":
  main()
