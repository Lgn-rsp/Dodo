#!/usr/bin/env python3
import os, re, sys, time

ROOTS = ["/root/logos_lrb", "/opt/logos", "/var/www/logos", "/etc/logos"]

OUT_BASE = "docs/DIR_BOOKS_FULL"
PART_MAX = 24 * 1024 * 1024      # 24MB на part, чтобы GitHub не бесился
FILE_MAX = 8 * 1024 * 1024       # 8MB на файл (код целиком). Тяжёлые сборки будут пропущены.
ENCODING = "utf-8"

ALLOW = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt|env|example|sample)$", re.I)

SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)

SKIP_DIR_NAMES = {
  ".git", "target", "node_modules", "venv", ".venv", "__pycache__", "backups", "snapshots", "data.sled.bak"
}

# Доп. жёстко исключаем старые мегакниги/снапшоты, чтобы не тащить мусор
SKIP_PATH_CONTAINS = [
  "/root/logos_lrb/docs/LOGOS_",
  "/root/logos_lrb/docs/snapshots/",
  "/root/logos_lrb/docs/BOOK/",
  "/root/logos_lrb/docs/LOGOS_MONO_BOOK",
  "/root/logos_lrb/docs/LOGOS_SNAPSHOTS/",
]

def safe_name(path: str) -> str:
  s = path.strip("/").replace("/", "__")
  s = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", s)
  return s

def is_binary(path: str) -> bool:
  try:
    with open(path, "rb") as f:
      chunk = f.read(4096)
    return b"\x00" in chunk
  except Exception:
    return True

def should_skip_dir(cur: str) -> bool:
  parts = cur.split(os.sep)
  if any(p in SKIP_DIR_NAMES for p in parts):
    return True
  for bad in SKIP_PATH_CONTAINS:
    if cur.startswith(bad) or (bad in cur):
      return True
  return False

def should_skip_file(path: str) -> bool:
  base = os.path.basename(path)
  if SKIP_NAME.search(base):
    return True
  for bad in SKIP_PATH_CONTAINS:
    if path.startswith(bad) or (bad in path):
      return True
  if not ALLOW.search(base):
    return True
  return False

def etc_sensitive(path: str) -> bool:
  # /etc/logos — не льём приватные ключи/боевые env (их редактируем)
  if not path.startswith("/etc/logos/"):
    return False
  b = os.path.basename(path)
  if b.endswith(".key") or b.endswith(".rid"):
    return True
  if b in {"keys.env", "keys.envy", "proxy.env", "wallet-proxy.env", "airdrop-api.env", "logos_tg_bot.env"}:
    return True
  if re.match(r"^node-.*\.env$", b or ""):
    return True
  if b == "node-main.env":
    return True
  # Разрешим example/sample, genesis.yaml и прочие явно не секретные конфиги
  if b.endswith(".example") or b.endswith(".sample"):
    return False
  if b == "genesis.yaml":
    return False
  # остальные .env считаем чувствительными
  if ".env" in b and not (b.endswith(".example") or b.endswith(".sample")):
    return True
  return False

class PartWriter:
  def __init__(self, out_dir: str, title: str):
    self.out_dir = out_dir
    self.title = title
    os.makedirs(out_dir, exist_ok=True)
    self.part_no = 1
    self.size = 0
    self.f = None
    self.index_lines = []
    self._open_new()

  def _open_new(self):
    if self.f:
      self.f.close()
    name = f"part{self.part_no:03d}.md"
    self.path = os.path.join(self.out_dir, name)
    self.f = open(self.path, "w", encoding=ENCODING, errors="replace")
    self.size = 0
    self._w(f"# {self.title}\n\n")
    self._w(f"_Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}_\n\n")
    self._w(f"**Part:** {self.part_no}\n\n---\n\n")
    self.index_lines.append(f"- {name}")
    self.part_no += 1

  def _w(self, s: str):
    self.f.write(s)
    self.size += len(s.encode(ENCODING, errors="replace"))

  def write(self, s: str):
    bs = len(s.encode(ENCODING, errors="replace"))
    if self.size + bs > PART_MAX:
      self._open_new()
    self._w(s)

  def close(self):
    if self.f:
      self.f.close()

def walk_files(root_dir: str):
  for cur, dnames, fnames in os.walk(root_dir):
    if should_skip_dir(cur):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIR_NAMES]
    for fn in sorted(fnames):
      path = os.path.join(cur, fn)
      if should_skip_file(path):
        continue
      yield path

def write_book(dir_path: str):
  sn = safe_name(dir_path)
  out_dir = os.path.join(OUT_BASE, sn)
  title = f"LOGOS — Directory Book: {dir_path}"

  w = PartWriter(out_dir, title)

  # STRUCTURE
  w.write("## STRUCTURE\n\n```text\n")
  for cur, dnames, fnames in os.walk(dir_path):
    if should_skip_dir(cur):
      dnames[:] = []
      continue
    dnames[:] = [d for d in dnames if d not in SKIP_DIR_NAMES]
    w.write(cur + "\n")
  w.write("```\n\n---\n\n")

  skipped_large = 0
  redacted = 0
  included = 0

  w.write("## FILES (FULL SOURCE)\n\n")

  for f in walk_files(dir_path):
    # binary?
    if is_binary(f):
      continue

    try:
      sz = os.path.getsize(f)
    except Exception:
      continue

    w.write(f"\n### FILE: {f}\n\n")

    if etc_sensitive(f):
      redacted += 1
      w.write("```text\n[REDACTED: sensitive /etc/logos file]\n```\n")
      continue

    if sz > FILE_MAX:
      skipped_large += 1
      w.write(f"```text\n[SKIPPED: too large ({sz} bytes)]\n```\n")
      continue

    w.write("```\n")
    try:
      with open(f, "r", encoding=ENCODING, errors="replace") as rf:
        w.write(rf.read())
    except Exception as e:
      w.write(f"[READ ERROR: {e}]\n")
    w.write("\n```\n")
    included += 1

  # INDEX
  idx_path = os.path.join(out_dir, "00_INDEX.md")
  with open(idx_path, "w", encoding=ENCODING, errors="replace") as idx:
    idx.write(f"# INDEX — {dir_path}\n\n")
    idx.write(f"- Included files: {included}\n")
    idx.write(f"- Redacted: {redacted}\n")
    idx.write(f"- Skipped large: {skipped_large}\n\n")
    idx.write("## Parts\n")
    idx.write("\n".join(w.index_lines) + "\n")

  w.close()
  return out_dir, included, redacted, skipped_large

def main():
  os.makedirs(OUT_BASE, exist_ok=True)

  # берём верхний уровень директорий из каждого ROOT
  targets = []
  for root in ROOTS:
    if not os.path.isdir(root):
      continue
    for name in sorted(os.listdir(root)):
      p = os.path.join(root, name)
      if os.path.isdir(p):
        # отсечём мусорные подпапки по имени
        if name in SKIP_DIR_NAMES:
          continue
        # отсечём резервные папки вида *_bak*, backup_*
        if re.search(r"(?:^\.bak|_bak|backup)", name, re.I):
          continue
        targets.append(p)

  # общий индекс
  global_index = os.path.join(OUT_BASE, "00_GLOBAL_INDEX.md")
  with open(global_index, "w", encoding=ENCODING, errors="replace") as gi:
    gi.write("# LOGOS — FULL DIRECTORY BOOKS (clean)\n\n")
    gi.write(f"_Generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}_\n\n")
    gi.write("## Books\n\n")
    for t in targets:
      gi.write(f"- {t} -> {safe_name(t)}/00_INDEX.md\n")

  # генерим
  total = 0
  for t in targets:
    out_dir, inc, red, skl = write_book(t)
    total += 1
    print(f"✅ {t} -> {out_dir} | files:{inc} redacted:{red} skipped_large:{skl}")

  print(f"\nDONE. Books: {total}\nOutput: {OUT_BASE}")

if __name__ == "__main__":
  main()
