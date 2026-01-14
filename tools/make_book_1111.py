#!/usr/bin/env python3
import os, re, time, subprocess
from pathlib import Path

OUTDIR = Path("docs/1111")
OUTDIR.mkdir(parents=True, exist_ok=True)

PART_LIMIT = 20 * 1024 * 1024  # 20MB на part чтобы GitHub не ругался (не обрезка, а разбиение)

# Где искать
FRONT_CANDIDATES = [
  "/opt/logos/www/wallet",        # предполагаемый prod
  "/opt/logos/www/wallet_prod",   # если есть
  "/opt/logos/www/wallet_dev",    # эталон dev
  "/opt/logos/www/wallet_premium",
  "/var/www/logos/wallet",
  "/var/www/logos/wallet3",
]

NGINX_PATHS = [
  "/etc/nginx/sites-enabled",
  "/etc/nginx/sites-available",
  "/etc/nginx/nginx.conf",
]

SYSTEMD_UNITS = [
  "logos-node@main",
  "logos-wallet-proxy",
  "lrb-proxy",
  "lrb-scanner",
]

# Какие файлы включаем “как код/текст”
ALLOW_EXT = re.compile(r"\.(html|css|js|mjs|cjs|ts|tsx|json|md|txt|env|ini|conf|service|yml|yaml|py|sh|toml)$", re.I)

# Мусор/бэкапы/бинарь/архивы/картинки/пдф
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.exe$|\.tar\.xz$|\.tar\.gz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}

# Жёстко не тащим старые мегакниги/снапшоты из logos_lrb/docs
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

SENSITIVE_ENV_KEYS = re.compile(r"(?i)\b(secret|token|apikey|api_key|private|privkey|password|passwd|mnemonic|seed|sign_key|bearer)\b")
RID_KEY_FILES = re.compile(r"(?i)\.(key|rid)$")

def sh(cmd: str) -> str:
  try:
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
  except subprocess.CalledProcessError as e:
    return e.output or ""

def is_skipped_path(p: str) -> bool:
  for s in SKIP_PATH_CONTAINS:
    if s in p:
      return True
  return False

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

def fence_lang(path: str) -> str:
  ext = Path(path).suffix.lower().lstrip(".")
  if ext in ("py","rs","sh","toml","yaml","yml","json","js","ts","tsx","html","css","md","ini","conf","service"):
    return ext
  return ""

def redact_text(path: str, text: str) -> str:
  # .env / env-подобные — редактируем значения
  base = os.path.basename(path)
  if base.endswith(".env") or ".env" in base or base in ("proxy.env","wallet-proxy.env","keys.env","keys.envy"):
    out_lines = []
    for line in text.splitlines(True):
      if "=" in line and not line.lstrip().startswith("#"):
        k, v = line.split("=", 1)
        if SENSITIVE_ENV_KEYS.search(k):
          out_lines.append(f"{k}=REDACTED\n")
        else:
          # безоп. вариант: значения тоже редактируем, если похоже на секрет
          if SENSITIVE_ENV_KEYS.search(v):
            out_lines.append(f"{k}=REDACTED\n")
          else:
            out_lines.append(line)
      else:
        out_lines.append(line)
    return "".join(out_lines)

  # ключи/rid файлы — вообще не кладём содержимое
  if RID_KEY_FILES.search(path):
    return "REDACTED (sensitive key/rid file)\n"

  return text

class BookWriter:
  def __init__(self, outdir: Path, prefix: str):
    self.outdir = outdir
    self.prefix = prefix
    self.part_idx = 1
    self.cur_bytes = 0
    self.cur_path = self._part_path()
    self.f = self.cur_path.open("w", encoding="utf-8", errors="replace")
    self.files_count = 0

  def _part_path(self) -> Path:
    return self.outdir / f"{self.prefix}_part{self.part_idx:03d}.md"

  def _rotate(self):
    self.f.close()
    self.part_idx += 1
    self.cur_bytes = 0
    self.cur_path = self._part_path()
    self.f = self.cur_path.open("w", encoding="utf-8", errors="replace")

  def write(self, s: str):
    b = len(s.encode("utf-8", errors="replace"))
    if self.cur_bytes + b > PART_LIMIT and self.cur_bytes > 0:
      self._rotate()
    self.f.write(s)
    self.cur_bytes += b

  def close(self):
    self.f.close()

def add_cmd_section(w: BookWriter, title: str, cmd: str):
  w.write(f"\n\n## {title}\n\n")
  w.write(f"**CMD:** `{cmd}`\n\n")
  out = sh(cmd)
  w.write("```text\n")
  w.write(out.strip() + "\n")
  w.write("```\n")

def add_file(w: BookWriter, path: str):
  try:
    data = Path(path).read_text(encoding="utf-8", errors="replace")
  except Exception as e:
    w.write(f"\n\n### FILE: {path}\n\n```text\nREAD_ERROR: {e}\n```\n")
    return

  data = redact_text(path, data)
  lang = fence_lang(path)

  w.write(f"\n\n### FILE: {path}\n\n")
  w.write(f"```{lang}\n")
  w.write(data.rstrip("\n") + "\n")
  w.write("```\n")
  w.files_count += 1

def find_front_roots():
  existing = []
  for p in FRONT_CANDIDATES:
    if os.path.isdir(p):
      existing.append(p)
  return existing

def find_openapi_json():
  # ищем openapi.json по типовым путям
  candidates = [
    "/opt/logos/wallet-proxy/openapi.json",
    "/opt/logos/wallet-proxy/openapi.yaml",
    "/var/www/logos/openapi.json",
    "/opt/logos/www/openapi.json",
    "/root/logos_lrb/openapi.json",
  ]
  for c in candidates:
    if os.path.isfile(c):
      return c
  # fallback: find
  out = sh("find /opt/logos /var/www/logos /root/logos_lrb -maxdepth 5 -type f -iname 'openapi.json' 2>/dev/null | head -n 1")
  p = out.strip()
  return p if p and os.path.isfile(p) else ""

def gather_related_code_by_grep():
  # найдём файлы, где реализуются node-api/wallet-api endpoints
  # берём исходники из /root/logos_lrb и /opt/logos/wallet-proxy
  roots = ["/root/logos_lrb", "/opt/logos/wallet-proxy"]
  patterns = [
    "submit_tx",
    "debug_canon",
    "canon",
    "balance",
    "nonce",
    "node-api",
    "wallet-api",
    "withdraw",
    "/submit_tx",
    "/balance",
    "/nonce",
    "FastAPI",
    "axum",
    "Router",
    "route(",
  ]
  found = set()
  for r in roots:
    if not os.path.isdir(r):
      continue
    for ptn in patterns:
      cmd = f"grep -R --line-number -I --binary-files=without-match --exclude-dir=.git --exclude-dir=target --exclude-dir=node_modules --exclude-dir=venv --exclude-dir=.venv --exclude-dir=__pycache__ --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.gif' --exclude='*.webp' --exclude='*.pdf' {sh_quote(ptn)} {sh_quote(r)} 2>/dev/null | head -n 200"
      out = sh(cmd)
      for line in out.splitlines():
        # формат: path:line:content
        m = re.match(r"^([^:]+):\d+:", line)
        if not m:
          continue
        fp = m.group(1)
        if is_skipped_path(fp): 
          continue
        if os.path.isfile(fp) and ALLOW_EXT.search(fp) and not SKIP_NAME.search(fp):
          found.add(fp)
  return sorted(found)

def sh_quote(s: str) -> str:
  return "'" + s.replace("'", "'\"'\"'") + "'"

def main():
  ts = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
  idx = OUTDIR / "00_INDEX.md"

  # Пишем INDEX
  idx.write_text(
f"""# BOOK 1111 — WALLET PROD + NGINX + NODE-API/WALLET-API (FULL)

Generated: {ts}

## What is inside
- Frontend wallet folders (prod/dev/premium if exist)
- Nginx vhost / routing (mw-expedition.com)
- Systemd units for node-api / wallet-api / scanner
- openapi.json (if found)
- Full source files for:
  - wallet_prod front: app.html/app.js/modules/*/tx_redirect/auth*
  - nginx config files (sites-enabled/available + includes)
  - wallet-proxy project (if present)
  - node-api related sources найденные по grep (submit_tx/balance/nonce/etc)

## Notes
- NO LFS
- NO snapshots/old mega-books
- Secrets in env are REDACTED
""", encoding="utf-8")

  w = BookWriter(OUTDIR, "1111")

  # Заголовок книги
  w.write(f"# BOOK 1111 — FULL (no truncation, may be split)\n\nGenerated: {ts}\n\n---\n")

  # 1) Inventory: что реально есть
  w.write("\n## INVENTORY: wallet folders present\n\n```text\n")
  for p in find_front_roots():
    w.write(p + "\n")
  w.write("```\n")

  # 2) Frontend folders (весь код)
  for root in find_front_roots():
    w.write(f"\n\n## FRONTEND ROOT: {root}\n")
    w.write("\n### TREE (depth 3)\n\n```text\n")
    w.write(sh(f"find {sh_quote(root)} -maxdepth 3 -type f 2>/dev/null | sed 's#^{root}/##' | head -n 2000").rstrip()+"\n")
    w.write("```\n")

    # Включаем ВСЕ текстовые файлы оттуда (полностью), без мусора
    for f in sorted(walk_files(root)):
      add_file(w, f)

  # 3) NGINX: полный vhost (файлы + nginx -T фильтр)
  w.write("\n\n---\n## NGINX CONFIG FILES\n")
  for p in NGINX_PATHS:
    if os.path.isdir(p):
      for f in sorted(walk_files(p)):
        add_file(w, f)
    elif os.path.isfile(p):
      add_file(w, p)

  # nginx -T (весь вывод огромный, поэтому даём блок по mw-expedition.com + upstream)
  add_cmd_section(w, "NGINX -T (filtered: mw-expedition.com + upstreams + wallet/api)", r"nginx -T 2>/dev/null | awk 'BEGIN{p=0} /server_name mw-expedition.com/{p=1} p{print} /}\s*$/{if(p){print; exit}}'")

  # 4) SYSTEMD units
  w.write("\n\n---\n## SYSTEMD UNITS\n")
  for u in SYSTEMD_UNITS:
    add_cmd_section(w, f"SYSTEMD: systemctl cat {u}", f"systemctl cat {u} --no-pager 2>/dev/null || true")
    add_cmd_section(w, f"SYSTEMD: systemctl show {u}", f"systemctl show -p FragmentPath -p WorkingDirectory -p ExecStart -p EnvironmentFile {u} --no-pager 2>/dev/null || true")

  # 5) openapi.json
  op = find_openapi_json()
  if op:
    w.write("\n\n---\n## OPENAPI\n")
    add_file(w, op)
  else:
    w.write("\n\n---\n## OPENAPI\n\n```text\nopenapi.json not found in expected paths\n```\n")

  # 6) wallet-proxy project целиком (если есть)
  wp = "/opt/logos/wallet-proxy"
  if os.path.isdir(wp):
    w.write("\n\n---\n## WALLET-PROXY PROJECT (/opt/logos/wallet-proxy)\n")
    w.write("\n### TREE (depth 4)\n\n```text\n")
    w.write(sh(f"find {sh_quote(wp)} -maxdepth 4 -type f 2>/dev/null | sed 's#^{wp}/##' | head -n 4000").rstrip()+"\n")
    w.write("```\n")
    for f in sorted(walk_files(wp)):
      add_file(w, f)

  # 7) Node-api sources (по grep)
  w.write("\n\n---\n## NODE-API / WALLET-API RELATED SOURCES (found by grep)\n")
  rel = gather_related_code_by_grep()
  w.write(f"\nFound files: {len(rel)}\n\n```text\n" + "\n".join(rel) + "\n```\n")
  for f in rel:
    add_file(w, f)

  w.close()

  # финальный summary
  parts = sorted(OUTDIR.glob("1111_part*.md"))
  summary = OUTDIR / "99_SUMMARY.txt"
  summary.write_text(
    "BOOK 1111 generated.\n"
    f"Parts: {len(parts)}\n"
    + "\n".join([f"{p.name}  {p.stat().st_size/1024/1024:.2f} MB" for p in parts])
    + f"\n\nFiles embedded (approx): {w.files_count}\n",
    encoding="utf-8"
  )

  print(f"✅ DONE: {OUTDIR}")
  print(f"Parts: {len(parts)}")
  print(f"Files embedded: {w.files_count}")

if __name__ == "__main__":
  main()
