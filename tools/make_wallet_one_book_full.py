#!/usr/bin/env python3
import os, re, time, tarfile, hashlib
from pathlib import Path

TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

OUTDIR = Path("docs/WALLET_ONE_BOOK")
OUTDIR.mkdir(parents=True, exist_ok=True)

INDEX = OUTDIR / "00_INDEX.md"
PART_PREFIX = "WALLET_ONE_BOOK_part"
PART_LIMIT = 15 * 1024 * 1024  # 15MB на part, чтобы GitHub не ругался
CHUNK_BYTES = 350 * 1024       # кусок внутри одного FILE-блока (если файл огромный)

# Ищем “кошелёк” (prod + dev) + прокси + конфиги
WALLET_DIRS = [
  "/var/www/logos/wallet",
  "/opt/logos/www/wallet",
  "/opt/logos/www/wallet_dev",
  "/var/www/logos/wallet_dev",
  "/var/www/logos/wallet3",
]
PROXY_DIRS = [
  "/opt/logos/wallet-proxy",
  "/root/logos_lrb/wallet-proxy",
]
NGINX_DIR = "/etc/nginx"
SYSTEMD_DIRS = ["/etc/systemd/system", "/lib/systemd/system"]

# Мусор/тяжёлые бэкапы исключаем
SKIP_DIRS = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots"}
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$)", re.I)

# Разрешаем только текст/код (без картинок/бинарей в книгу)
ALLOW_EXT = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)

# Секреты: в книгу не пихаем приватки/реальные env
SENSITIVE = re.compile(r"(\.key$|\.rid$|keys\.envy?$|node-.*\.env$|node-main\.env$|proxy\.env$|wallet-proxy\.env$|airdrop-api\.env$|logos_tg_bot\.env$)", re.I)

# Жёстко не включаем старые мегакниги/снапшоты из /root/logos_lrb/docs
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

def skip_path(p: str) -> bool:
  for s in SKIP_PATH_CONTAINS:
    if s in p:
      return True
  return False

def iter_files(root: str):
  if not os.path.exists(root):
    return
  for cur, dnames, fnames in os.walk(root):
    if any(x in cur.split("/") for x in SKIP_DIRS):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
    for n in fnames:
      p = str(Path(cur) / n)
      if skip_path(p):
        continue
      if SKIP_NAME.search(n):
        continue
      if not ALLOW_EXT.search(n):
        continue
      yield Path(p)

def is_sensitive(path: Path) -> bool:
  # если это env и не *.example/sample — редактируем
  n = path.name
  if n.lower().endswith(".env") and not (n.endswith(".example") or n.endswith(".sample")):
    return True
  if SENSITIVE.search(n):
    return True
  return False

def make_part_writer():
  part_no = 1
  p = OUTDIR / f"{PART_PREFIX}{part_no:03d}.md"
  f = p.open("w", encoding="utf-8")
  size = 0
  parts = [p.name]

  def rotate():
    nonlocal part_no, p, f, size, parts
    f.close()
    part_no += 1
    p = OUTDIR / f"{PART_PREFIX}{part_no:03d}.md"
    f = p.open("w", encoding="utf-8")
    size = 0
    parts.append(p.name)

  def write(s: str):
    nonlocal size
    b = s.encode("utf-8")
    if size + len(b) > PART_LIMIT and size > 0:
      rotate()
    f.write(s)
    size += len(b)

  def close():
    f.close()

  return write, close, parts

def add_file(write, path: Path, lang_hint: str = ""):
  rp = str(path)

  # заголовок файла
  write(f"\n### FILE: {rp}\n")
  if is_sensitive(path):
    write("```text\n[REDACTED: sensitive or env file]\n```\n")
    return

  ext = path.suffix.lower().lstrip(".")
  fence = "```" + (ext if ext else "text")

  write(f"{fence}\n")

  # читаем в бинарном режиме и режем на чанки, но ВЕСЬ файл попадает в книгу
  try:
    with open(path, "rb") as bf:
      chunk_no = 0
      while True:
        data = bf.read(CHUNK_BYTES)
        if not data:
          break
        chunk_no += 1
        txt = data.decode("utf-8", errors="replace")
        write(txt)
        # если файл очень большой — разбиваем на несколько fenced blocks (чтобы part rotation не ломала fence)
        if len(data) == CHUNK_BYTES:
          write("\n```\n")
          write(f"\n> CONTINUE: {rp} (chunk {chunk_no})\n\n")
          write(f"{fence}\n")
  except Exception as e:
    write(f"\n[ERROR reading file: {e}]\n")

  write("\n```\n")

def collect_assets_tar():
  # ассеты — бинарные (иконки/шрифты) лучше архивом (одним файлом)
  candidates = []
  for base in WALLET_DIRS + ["/var/www/logos", "/opt/logos/www"]:
    if not base or not os.path.exists(base):
      continue
    for name in ["assets","img","images","icons","fonts"]:
      p = Path(base) / name
      if p.exists() and p.is_dir():
        candidates.append(p)

  tar_path = OUTDIR / "assets.tar.gz"
  if tar_path.exists():
    tar_path.unlink()

  added = 0
  with tarfile.open(tar_path, "w:gz") as tar:
    for src in candidates:
      # упаковываем папку целиком
      arcname = src.as_posix().strip("/").replace("/","__")
      tar.add(src, arcname=arcname, recursive=True)
      added += 1

  return candidates, added, tar_path

def find_openapi():
  for base in ["/root/logos_lrb","/opt/logos","/var/www/logos"]:
    if not os.path.exists(base): 
      continue
    for cur, dnames, fnames in os.walk(base):
      if any(x in cur.split("/") for x in SKIP_DIRS):
        dnames[:] = []
        continue
      for n in fnames:
        if n.lower() == "openapi.json":
          return str(Path(cur)/n)
  return None

def sha256_file(p: Path) -> str:
  h = hashlib.sha256()
  with open(p, "rb") as f:
    for b in iter(lambda: f.read(1024*1024), b""):
      h.update(b)
  return h.hexdigest()

def main():
  write, close, parts = make_part_writer()

  # Заголовок книги
  write("# LOGOS WALLET — ONE FULL BOOK (NO TRUNCATION)\n\n")
  write(f"- Generated: `{TS}`\n")
  write("- Policy: **NO CODE TRUNCATION** (large files are chunked, not cut)\n\n")
  write("---\n\n## CONTENT\n\n")

  all_files = []

  # 1) Wallet prod+dev
  for d in WALLET_DIRS:
    if os.path.exists(d):
      all_files += list(iter_files(d))

  # 2) Proxy
  for d in PROXY_DIRS:
    if os.path.exists(d):
      all_files += list(iter_files(d))

  # 3) NGINX + systemd (фильтруем: берём только файлы где есть wallet/api/proxy)
  def cfg_match(p: Path) -> bool:
    try:
      t = p.read_text(encoding="utf-8", errors="ignore")
    except:
      return False
    return bool(re.search(r"wallet|wallet_dev|wallet-api|/api|proxy_pass|logos_wallet", t, re.I))

  if os.path.exists(NGINX_DIR):
    for f in iter_files(NGINX_DIR):
      if cfg_match(f):
        all_files.append(f)

  for sd in SYSTEMD_DIRS:
    if os.path.exists(sd):
      for f in iter_files(sd):
        if cfg_match(f):
          all_files.append(f)

  # сорт и уникализация
  uniq = {}
  for f in all_files:
    uniq[str(f)] = f
  files = [uniq[k] for k in sorted(uniq.keys())]

  # записываем оглавление
  for f in files:
    write(f"- `{f}`\n")

  write("\n---\n\n## FULL SOURCE\n")
  for f in files:
    add_file(write, f)

  close()

  # INDEX + openapi + assets archive
  idx_lines = []
  idx_lines.append("# INDEX — WALLET ONE BOOK\n\n")
  idx_lines.append(f"- Generated: `{TS}`\n")
  idx_lines.append(f"- Parts: {len(parts)}\n\n")
  idx_lines.append("## Part files\n\n")
  idx_lines += [f"- {p}\n" for p in parts]

  src_openapi = find_openapi()
  if src_openapi:
    op = Path(src_openapi)
    dst = OUTDIR / "openapi.json"
    try:
      dst.write_text(op.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
      idx_lines.append(f"\n## openapi.json\n\n- Source: `{src_openapi}`\n- SHA256: `{sha256_file(dst)}`\n")
    except:
      idx_lines.append(f"\n## openapi.json\n\n- Found but failed to copy: `{src_openapi}`\n")
  else:
    idx_lines.append("\n## openapi.json\n\n- NOT FOUND\n")

  cand, added, tar_path = collect_assets_tar()
  idx_lines.append("\n## Assets archive\n\n")
  idx_lines.append(f"- Archive: `{tar_path}`\n")
  idx_lines.append(f"- SHA256: `{sha256_file(tar_path)}`\n")
  idx_lines.append(f"- Source roots packed: {added}\n")
  for c in cand:
    idx_lines.append(f"  - `{c}`\n")

  INDEX.write_text("".join(idx_lines), encoding="utf-8")

  print("✅ DONE")
  print(f"- Out: {OUTDIR}")
  print(f"- Parts: {len(parts)}")
  print(f"- Files inlined: {len(files)}")

if __name__ == "__main__":
  main()
