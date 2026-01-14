#!/usr/bin/env python3
import os, re, time, subprocess
from pathlib import Path

OUT = Path("docs/1111/1111_part001.md")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Периметр (что реально нужно)
WALLET_API_ROOT = "/opt/logos/wallet-proxy"          # FastAPI wallet-api (по твоим юнитам)
NODE_BIN = "/opt/logos/bin/logos_node"               # node-api (по nginx upstream)
NGINX_FILES = [
  "/etc/nginx/nginx.conf",
  "/etc/nginx/sites-enabled",
  "/etc/nginx/sites-available",
]
SYSTEMD_UNITS = [
  "logos-wallet-proxy.service",
  "lrb-proxy.service",
  "lrb-scanner.service",
  "logos-node@main.service",
  "logos-node.service",
]

ENV_FILES_HINTS = [
  "/etc/logos/wallet-proxy.env",
  "/etc/logos/proxy.env",
  "/etc/logos/node-main.env",
  "/etc/logos/node-a.env",
  "/etc/logos/node-b.env",
  "/etc/logos/node-c.env",
  "/etc/logos/genesis.yaml",
  "/etc/logos/keys.env",
  "/etc/logos/keys.envy",
]

NGINX_LOGS = [
  "/var/log/nginx/access.log",
  "/var/log/nginx/error.log",
]

# Текстовые типы
ALLOW = re.compile(r"\.(py|rs|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt|env)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.exe$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}

# Жёстко не тащим старые мегакниги/снапшоты из /root/logos_lrb/docs
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

# Редакция секретов
SENSITIVE_KEYS = re.compile(r"(?i)\b(secret|token|apikey|api_key|private|privkey|password|passwd|mnemonic|seed|bearer|sign|key)\b")
SENSITIVE_FILES = re.compile(r"(?i)\.(key|rid)$")

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

def redact_env(path: str, txt: str) -> str:
  # ключи/рид файлы не публикуем
  if SENSITIVE_FILES.search(path):
    return "REDACTED (sensitive key/rid file)\n"
  base = os.path.basename(path)
  if base.endswith(".env") or ".env" in base or base in ("proxy.env","wallet-proxy.env","keys.env","keys.envy"):
    out = []
    for line in txt.splitlines(True):
      if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1)
        if SENSITIVE_KEYS.search(k):
          out.append(f"{k}=REDACTED\n")
        else:
          out.append(line)
      else:
        out.append(line)
    return "".join(out)
  return txt

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
      if not ALLOW.search(n):
        continue
      yield p

def add_h(w, title):
  w.write("\n\n" + "# " + title + "\n")

def add_cmd(w, title, cmd):
  w.write(f"\n\n## {title}\n\n**CMD:** `{cmd}`\n\n```text\n")
  out = sh(cmd)
  w.write(out.rstrip() + "\n")
  w.write("```\n")

def add_file(w, path):
  try:
    txt = Path(path).read_text(encoding="utf-8", errors="replace")
  except Exception as e:
    w.write(f"\n\n### FILE: {path}\n\n```text\nREAD_ERROR: {e}\n```\n")
    return
  txt = redact_env(path, txt)
  w.write(f"\n\n### FILE: {path}\n\n```{fence_lang(path)}\n")
  w.write(txt.rstrip("\n") + "\n")
  w.write("```\n")

def existing_units(candidates):
  ok = []
  for u in candidates:
    out = sh(f"systemctl status {q(u)} --no-pager 2>/dev/null | head -n 1")
    if out.strip():
      ok.append(u)
  return ok

def include_env_files(w):
  w.write("\n\n## ENV/CONFIG FILES (REDACTED secrets)\n")
  for p in ENV_FILES_HINTS:
    if os.path.isfile(p):
      add_file(w, p)
  # если есть другие /etc/logos/*.env
  lst = sh("ls -1 /etc/logos/*.env 2>/dev/null || true").splitlines()
  for p in sorted(set(x.strip() for x in lst if x.strip())):
    if os.path.isfile(p):
      add_file(w, p)

def include_nginx(w):
  add_h(w, "NGINX VHOST + ROUTING (wallet / node-api / wallet-api)")
  for p in NGINX_FILES:
    if os.path.isfile(p):
      add_file(w, p)
    elif os.path.isdir(p):
      for f in sorted(walk_files(p)):
        add_file(w, f)
  add_cmd(
    w,
    "nginx -T (mw-expedition routing extract)",
    r"nginx -T 2>/dev/null | grep -nE 'server_name mw-expedition\.com|upstream logos_node_backend|upstream logos_wallet_api|location|proxy_pass|/wallet_dev/|/wallet/|/wallet-api/|/node-api/|/api/' | head -n 900"
  )

def include_systemd(w):
  add_h(w, "SYSTEMD UNITS (node-api + wallet-api/proxy + scanner)")
  units = existing_units(SYSTEMD_UNITS)
  w.write("\n\n## DETECTED UNITS\n\n```text\n" + ("\n".join(units) if units else "NONE") + "\n```\n")

  for u in units:
    add_cmd(w, f"systemctl cat {u}", f"systemctl cat {q(u)} --no-pager 2>/dev/null || true")
    add_cmd(w, f"systemctl show {u} (ExecStart/Env/WD)", f"systemctl show -p FragmentPath -p WorkingDirectory -p ExecStart -p EnvironmentFile {q(u)} --no-pager 2>/dev/null || true")

def include_wallet_api_sources(w):
  add_h(w, "WALLET-API (FastAPI) — FULL SOURCES + OPENAPI")
  add_cmd(w, "ls -lah wallet-api root", f"ls -lah {q(WALLET_API_ROOT)} 2>/dev/null || true")
  if os.path.isdir(WALLET_API_ROOT):
    for f in sorted(walk_files(WALLET_API_ROOT)):
      add_file(w, f)
  # openapi from running service (local)
  add_cmd(w, "curl wallet-api openapi (local 9090)", "curl -sS http://127.0.0.1:9090/openapi.json | head -n 400 || true")
  add_cmd(w, "curl wallet-api health (guess)", "curl -sS -D- http://127.0.0.1:9090/ 2>/dev/null | head -n 40 || true")

def include_node_api_proofs(w):
  add_h(w, "NODE-API (submit_tx / balance / nonce) — PROOFS + BINARY INFO")
  add_cmd(w, "ls -lah node binary", f"ls -lah {q(NODE_BIN)} 2>/dev/null || true")
  add_cmd(w, "file + sha256", f"file {q(NODE_BIN)} 2>/dev/null || true; sha256sum {q(NODE_BIN)} 2>/dev/null || true")
  add_cmd(w, "netstat/ss who listens 8080/9090", "ss -lntp | egrep '(:8080|:9090)\\b' || true")

  # openapi / endpoints (local via nginx upstream port)
  add_cmd(w, "curl node-api root (local 8080)", "curl -sS -D- http://127.0.0.1:8080/ 2>/dev/null | head -n 80 || true")
  add_cmd(w, "curl node-api openapi guess", "curl -sS http://127.0.0.1:8080/openapi.json | head -n 500 || true")
  add_cmd(w, "curl node-api routes guess (balance sample)", "curl -sS http://127.0.0.1:8080/balance/TEST 2>/dev/null | head -n 80 || true")
  add_cmd(w, "curl node-api routes guess (/head)", "curl -sS http://127.0.0.1:8080/head 2>/dev/null | head -n 120 || true")

def include_logs(w):
  add_h(w, "LOGS (moment “не отправляет”)")
  # по умолчанию последние ~15 минут
  since = "15 minutes ago"
  # node-api logs
  for u in ["logos-node@main.service","logos-node.service","logos-node@main","logos-node"]:
    out = sh(f"systemctl status {q(u)} --no-pager 2>/dev/null | head -n 1")
    if out.strip():
      add_cmd(w, f"journalctl {u} --since {since}", f"journalctl -u {q(u)} --since {q(since)} --no-pager | tail -n 600 || true")
      break

  # wallet-api logs
  for u in ["logos-wallet-proxy.service","lrb-proxy.service","lrb-scanner.service","logos-wallet-proxy","lrb-proxy","lrb-scanner"]:
    out = sh(f"systemctl status {q(u)} --no-pager 2>/dev/null | head -n 1")
    if out.strip():
      add_cmd(w, f"journalctl {u} --since {since}", f"journalctl -u {q(u)} --since {q(since)} --no-pager | tail -n 600 || true")

  # nginx access/error: submit_tx
  for lp in NGINX_LOGS:
    if os.path.isfile(lp):
      add_cmd(w, f"nginx grep submit_tx ({lp})", f"grep -nEi 'submit_tx|/node-api/|/api/|/wallet-api/|withdraw|balances' {q(lp)} | tail -n 800 || true")

def main():
  with OUT.open("w", encoding="utf-8", errors="replace") as w:
    w.write("# BOOK 1111 — Wallet+ Server Perimeter (NO CUTS)\n\n")
    w.write("Generated (UTC): " + time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()) + "\n\n")
    w.write("Includes: wallet-api sources+env+systemd, node-api proofs+systemd+env, nginx vhost routing, logs.\n")
    w.write("Secrets in env/key files are REDACTED.\n")

    include_nginx(w)
    include_systemd(w)
    include_env_files(w)
    include_wallet_api_sources(w)
    include_node_api_proofs(w)
    include_logs(w)

  print(f"✅ DONE: {OUT} ({OUT.stat().st_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
  main()
