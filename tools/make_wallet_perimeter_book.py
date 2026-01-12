#!/usr/bin/env python3
import os, re, subprocess, time
from pathlib import Path

TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
OUTDIR = Path("docs/WALLET_PERIMETER_BOOK")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Где искать код/конфиги
ROOTS = [
  "/opt/logos",
  "/var/www/logos",
  "/root/logos_lrb",
]

# Жестко выкидываем старые мегакниги/снапшоты
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
ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)

PART_LIMIT = 20 * 1024 * 1024  # 20MB на файл (чтобы GitHub не ругался)
MAX_FILE = 2 * 1024 * 1024     # 2MB на один исходный файл (чтобы не тащить жир)
MAX_TOTAL_FILES = 50000

def safe_name(path: str) -> str:
  s = path.strip("/").replace("/", "__")
  s = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", s)
  return s

def is_binary(path: str) -> bool:
  try:
    with open(path, "rb") as f:
      b = f.read(2048)
    return b"\x00" in b
  except:
    return True

def sh(cmd: str) -> str:
  try:
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, text=True)
  except:
    return ""

def nginx_T() -> str:
  return sh("nginx -T 2>/dev/null")

def detect_prod_wallet_dir(ng: str) -> str:
  # пытаемся понять по nginx root/alias для /wallet или /wallet3
  # если не нашли — берем существующую папку по приоритету
  candidates = []
  # ищем строки root/alias рядом с wallet
  lines = ng.splitlines()
  for i, line in enumerate(lines):
    if re.search(r"location\s+/(wallet3|wallet)\b", line):
      chunk = "\n".join(lines[max(0,i-20):i+40])
      m = re.search(r"\balias\s+([^;]+);", chunk)
      if m: candidates.append(m.group(1).strip())
      m = re.search(r"\broot\s+([^;]+);", chunk)
      if m: candidates.append(m.group(1).strip())
  for p in candidates:
    # если root=/var/www/logos то wallet лежит внутри /wallet
    if os.path.isdir(os.path.join(p, "wallet")):
      return os.path.join(p, "wallet")
    if os.path.isdir(os.path.join(p, "wallet3")):
      return os.path.join(p, "wallet3")
    if os.path.isdir(p):
      return p

  fallback = [
    "/var/www/logos/wallet",
    "/var/www/logos/wallet3",
    "/opt/logos/www/wallet",
    "/opt/logos/www/wallet_dev",
  ]
  for p in fallback:
    if os.path.isdir(p):
      return p
  return ""

def find_openapi() -> str:
  # ищем openapi.json в системных путях
  for base in ROOTS:
    if not os.path.isdir(base): 
      continue
    for cur, dnames, fnames in os.walk(base):
      if any(x in cur.split("/") for x in SKIP_DIRS):
        dnames[:] = []
        continue
      if any(s in cur for s in SKIP_PATH_CONTAINS):
        dnames[:] = []
        continue
      for n in fnames:
        if n.lower() == "openapi.json":
          return os.path.join(cur, n)
  return ""

def extract_api_base_url(wallet_dir: str) -> str:
  if not wallet_dir:
    return ""
  # ищем API_BASE_URL в фронтовых файлах
  hits = sh(f"grep -RInE \"API_BASE_URL|baseURL|/api\" {shell_quote(wallet_dir)} 2>/dev/null | head -n 80")
  return hits.strip()

def shell_quote(s: str) -> str:
  return "'" + s.replace("'", "'\"'\"'") + "'"

def extract_nginx_wallet_api_snippets(ng: str) -> str:
  # только релевантные строки
  out = []
  for line in ng.splitlines():
    if re.search(r"wallet|wallet3|wallet_dev|wallet-proxy|/api|proxy_pass|API_BASE_URL|openapi", line, re.I):
      out.append(line)
  return "\n".join(out[:4000])

def extract_systemd_units() -> str:
  # вытаскиваем unit'ы, где есть wallet/proxy/logos (без секретов)
  units = sh("systemctl list-unit-files 2>/dev/null | grep -Ei 'wallet|proxy|logos' | awk '{print $1}' | head -n 80").splitlines()
  blocks = []
  for u in units:
    txt = sh(f"systemctl cat {shell_quote(u)} 2>/dev/null")
    if not txt.strip():
      continue
    # редактируем переменные
    txt = re.sub(r"(TOKEN|KEY|SECRET|PASSWORD|PASS|PRIVATE|BEARER)=.*", r"\\1=[REDACTED]", txt, flags=re.I)
    blocks.append(f"### systemd unit: {u}\n```ini\n{txt}\n```\n")
  return "\n".join(blocks)

def should_skip_path(p: str) -> bool:
  for s in SKIP_PATH_CONTAINS:
    if s in p:
      return True
  return False

def collect_files(root: str):
  files = []
  for cur, dnames, fnames in os.walk(root):
    if any(x in cur.split("/") for x in SKIP_DIRS):
      dnames[:] = []
      continue
    if should_skip_path(cur):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
    for n in fnames:
      p = os.path.join(cur, n)
      if should_skip_path(p):
        continue
      if SKIP_NAME.search(n):
        continue
      if not ALLOW_EXT.search(n):
        continue
      try:
        sz = os.path.getsize(p)
      except:
        continue
      if sz > MAX_FILE:
        continue
      if is_binary(p):
        continue
      files.append(p)
      if len(files) > MAX_TOTAL_FILES:
        return files
  return files

def write_parts(title: str, header_md: str, structure: str, file_list):
  # Пишем частями
  idx = 0
  part_no = 1
  cur_bytes = 0
  part_path = OUTDIR / f"{title}_part{part_no:03d}.md"
  part = open(part_path, "w", encoding="utf-8", errors="ignore")

  def new_part():
    nonlocal part_no, part, part_path, cur_bytes
    part.close()
    part_no += 1
    cur_bytes = 0
    part_path = OUTDIR / f"{title}_part{part_no:03d}.md"
    part = open(part_path, "w", encoding="utf-8", errors="ignore")
    part.write(header_md)

  part.write(header_md)
  part.write("\n## STRUCTURE\n```text\n" + structure + "\n```\n")
  part.write("\n---\n## FILES (FULL SOURCE)\n")

  for f in file_list:
    try:
      data = Path(f).read_text(encoding="utf-8", errors="ignore")
    except:
      continue

    block = f"\n### FILE: {f}\n```text\n{data}\n```\n"
    b = block.encode("utf-8", errors="ignore")
    if cur_bytes + len(b) > PART_LIMIT:
      new_part()
    part.write(block)
    cur_bytes += len(b)

  part.close()
  return part_no

def main():
  ng = nginx_T()
  wallet_dir = detect_prod_wallet_dir(ng)
  openapi = find_openapi()

  wallet_proxy_dirs = [
    "/opt/logos/wallet-proxy",
    "/root/logos_lrb/wallet-proxy",
    "/opt/logos/www/wallet-proxy",
  ]
  wallet_proxy_dirs = [p for p in wallet_proxy_dirs if os.path.isdir(p)]

  # SUMMARY
  summary = []
  summary.append("# LOGOS — WALLET PERIMETER BOOK (FULL)\n")
  summary.append(f"UTC build: {TS}\n")
  summary.append(f"- Detected PROD wallet dir: `{wallet_dir or 'NOT FOUND'}`\n")
  summary.append(f"- Detected openapi.json: `{openapi or 'NOT FOUND'}`\n")
  summary.append(f"- Wallet-proxy dirs: {', '.join('`'+p+'`' for p in wallet_proxy_dirs) if wallet_proxy_dirs else '`NOT FOUND`'}\n")

  api_hits = extract_api_base_url(wallet_dir)
  if api_hits:
    summary.append("\n## API_BASE_URL / /api hints (from frontend grep)\n```text\n" + api_hits + "\n```\n")
  summary.append("\n## NGINX snippets (wallet/api/proxy)\n```nginx\n" + (extract_nginx_wallet_api_snippets(ng) or "NOT FOUND") + "\n```\n")
  summary.append("\n## SYSTEMD units (wallet/proxy/logos)\n" + (extract_systemd_units() or "NOT FOUND\n"))
  header_md = "\n".join(summary) + "\n---\n"

  # STRUCTURE
  targets = []
  if wallet_dir:
    targets.append(wallet_dir)
  targets += wallet_proxy_dirs
  if openapi:
    targets.append(os.path.dirname(openapi))

  # Собираем файлы
  all_files = []
  structures = []
  for t in targets:
    if not os.path.isdir(t):
      continue
    structures.append(f"\n[TARGET] {t}\n")
    for cur, dnames, _ in os.walk(t):
      if any(x in cur.split("/") for x in SKIP_DIRS):
        dnames[:] = []
        continue
      if should_skip_path(cur):
        dnames[:] = []
        continue
      dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
      structures.append(cur)
    all_files += collect_files(t)

  # Уникальные файлы
  all_files = sorted(set(all_files))

  # Индекс
  (OUTDIR / "00_INDEX.md").write_text(
    header_md +
    "## INCLUDED TARGETS\n" + "\n".join(f"- `{t}`" for t in targets) + "\n\n" +
    f"## TOTAL FILES INCLUDED\n- {len(all_files)}\n\n"
    "## PARTS\n- generated by script\n",
    encoding="utf-8", errors="ignore"
  )

  # Книга по частям
  parts = write_parts("WALLET_PERIMETER", header_md, "\n".join(structures), all_files)

  # Дополнительно — копия openapi.json как отдельный файл (если есть)
  if openapi and os.path.isfile(openapi):
    dst = OUTDIR / "openapi.json"
    try:
      dst.write_text(Path(openapi).read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
    except:
      pass

  print("✅ DONE:", OUTDIR)
  print("Parts:", parts)
  print("Files included:", len(all_files))

if __name__ == "__main__":
  main()
