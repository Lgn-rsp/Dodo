#!/usr/bin/env python3
import os, re, sys, hashlib, time
from pathlib import Path

ROOTS = [
    "/root/logos_lrb/configs",
    "/root/logos_lrb/core",
    "/root/logos_lrb/infra",
    "/root/logos_lrb/lrb_core",
    "/root/logos_lrb/modules",
    "/root/logos_lrb/node",
    "/root/logos_lrb/scripts",
    "/root/logos_lrb/src",
    "/root/logos_lrb/tools",
    "/root/logos_lrb/wallet-proxy",
    "/root/logos_lrb/www",
    "/root/logos_lrb/www_external",
    "/opt/logos/airdrop-api",
    "/opt/logos/airdrop-tg-bot",
    "/opt/logos/bin",
    "/opt/logos/configs",
    "/opt/logos/load",
    "/opt/logos/wallet-proxy",
    "/opt/logos/www",
    "/var/www/logos/css",
    "/var/www/logos/explorer",
    "/var/www/logos/js",
    "/var/www/logos/landing",
    "/var/www/logos/wallet",
    "/var/www/logos/wallet3",
    "/var/www/logos/www",
]

OUT_ROOT = Path("docs/DIR_BOOKS_FULL_V2")
OUT_ROOT.mkdir(parents=True, exist_ok=True)

# чтобы GitHub не ругался на 50MB рекомендованный размер — режем по 40MB
PART_MAX = 40 * 1024 * 1024

# файл, который больше PART_MAX, невозможно адекватно положить внутрь md-части
# (иначе часть > 100MB). Поэтому такой файл помечаем как SKIPPED_TOO_BIG.
FILE_MAX = PART_MAX

ALLOW = re.compile(r"\.(rs|py|sh|toml|yml|yaml|md|js|mjs|cjs|ts|tsx|html|css|json|ini|conf|service|txt)$", re.I)
SKIP_NAME = re.compile(r"(\.bak|\.backup|\.broken|\.old|~$|\.tmp$|\.swp$|\.sqlite3$|\.db$|\.bin$|\.tar\.xz$|\.gz$|\.zip$|\.7z$|\.png$|\.jpg$|\.jpeg$|\.webp$|\.gif$|\.pdf$)", re.I)

SKIP_DIR_NAMES = {".git","target","node_modules","venv",".venv","__pycache__","backups","snapshots","data.sled.bak"}

# Жёстко исключаем мегакниги/снапшоты/старые книги, чтобы не тянуть мусор
SKIP_PATH_CONTAINS = [
  "/root/logos_lrb/docs/LOGOS_",
  "/root/logos_lrb/docs/snapshots/",
  "/root/logos_lrb/docs/BOOK/",
  "/root/logos_lrb/docs/LOGOS_MONO_BOOK",
  "/root/logos_lrb/docs/LOGOS_SNAPSHOTS/",
  "/root/logos_lrb/docs/LOGOS_MONO_BOOK_FULL",
  "/root/logos_lrb/docs/DIR_BOOKS",
  "/root/logos_lrb/docs/DIR_BOOKS_FULL",
]

def safe_name(path: str) -> str:
    s = path.strip("/").replace("/", "__")
    s = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", s)
    return s

def is_binary_bytes(b: bytes) -> bool:
    if b"\x00" in b:
        return True
    # много “непечатных” — вероятно бинарь
    text = sum(1 for x in b if (9 <= x <= 13) or (32 <= x <= 126) or (x >= 128))
    return text / max(1, len(b)) < 0.85

def should_skip_path(p: str) -> bool:
    for s in SKIP_PATH_CONTAINS:
        if s in p:
            return True
    return False

def is_sensitive_etc(p: str) -> bool:
    # на всякий случай: если вдруг попадёт /etc/logos — ключи не льём
    if not p.startswith("/etc/logos/"):
        return False
    base = os.path.basename(p)
    if base.endswith(".key") or base.endswith(".rid"):
        return True
    if base in ("keys.env","keys.envy","node-main.env","proxy.env","wallet-proxy.env","airdrop-api.env","logos_tg_bot.env"):
        return True
    if re.match(r"^node-.*\.env$", base):
        return True
    # .env только example/sample
    if base.endswith(".env") and not (base.endswith(".example") or base.endswith(".sample")):
        return True
    return False

def write_header(fp, title: str):
    fp.write(f"# {title}\n\n")
    fp.write(f"_Generated: {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}_\n\n")

def write_index(dir_path: str, out_dir: Path, files_all: list, skipped_big: list, skipped_bin: list):
    idx = out_dir / "00_INDEX.md"
    with idx.open("w", encoding="utf-8") as fp:
        write_header(fp, "LOGOS — Directory Code Book (FULL, no truncation)")
        fp.write(f"## ROOT: `{dir_path}`\n\n")
        fp.write("## Files included\n\n")
        for f in files_all:
            fp.write(f"- `{f}`\n")
        fp.write("\n## Skipped (too big)\n\n")
        for f, sz in skipped_big:
            fp.write(f"- `{f}` ({sz/1024/1024:.1f} MB) — SKIPPED_TOO_BIG\n")
        fp.write("\n## Skipped (binary)\n\n")
        for f in skipped_bin:
            fp.write(f"- `{f}` — SKIPPED_BINARY\n")
        fp.write("\n")

def open_part(out_dir: Path, part_no: int):
    p = out_dir / f"part{part_no:03d}.md"
    fp = p.open("w", encoding="utf-8")
    return p, fp

def main():
    global_index = OUT_ROOT / "00_GLOBAL_INDEX.md"
    books = []

    with global_index.open("w", encoding="utf-8") as gidx:
        write_header(gidx, "LOGOS — GLOBAL DIRECTORY BOOK INDEX")
        gidx.write("Список книг по директориям.\n\n")

        for root in ROOTS:
            if not os.path.isdir(root):
                continue

            book_name = safe_name(root)
            out_dir = OUT_ROOT / book_name
            out_dir.mkdir(parents=True, exist_ok=True)

            files = []
            skipped_big = []
            skipped_bin = []

            # собираем файлы
            for cur, dnames, fnames in os.walk(root):
                # выкидываем мусорные dirs
                dnames[:] = [d for d in dnames if d not in SKIP_DIR_NAMES]
                cur_norm = cur.replace("\\", "/")
                if any(f"/{d}/" in f"/{cur_norm}/" for d in SKIP_DIR_NAMES):
                    dnames[:] = []
                    continue

                for n in sorted(fnames):
                    if SKIP_NAME.search(n):
                        continue
                    if not ALLOW.search(n):
                        continue
                    p = os.path.join(cur, n).replace("\\", "/")
                    if should_skip_path(p):
                        continue
                    try:
                        sz = os.path.getsize(p)
                    except:
                        continue
                    if sz > FILE_MAX:
                        skipped_big.append((p, sz))
                        continue
                    # бинарь проверим небольшим чтением
                    try:
                        with open(p, "rb") as fb:
                            head = fb.read(8192)
                        if is_binary_bytes(head):
                            skipped_bin.append(p)
                            continue
                    except:
                        continue
                    files.append(p)

            # индекс и структура
            write_index(root, out_dir, files, skipped_big, skipped_bin)

            # начинаем части
            part_no = 1
            part_path, fp = open_part(out_dir, part_no)

            fp.write(f"# FULL SOURCE — `{root}`\n\n")
            fp.write("**No truncation.** Full file contents inside code fences.\n\n")

            cur_size = fp.tell()

            def rotate():
                nonlocal part_no, fp, part_path, cur_size
                fp.close()
                part_no += 1
                part_path, fp = open_part(out_dir, part_no)
                fp.write(f"# FULL SOURCE — `{root}` (part {part_no:03d})\n\n")
                cur_size = fp.tell()

            # пишем файлы целиком
            for f in files:
                rel = f
                fp.write(f"\n---\n\n## FILE: `{rel}`\n\n")
                # язык подсветки
                ext = Path(f).suffix.lower().lstrip(".")
                lang = ext if ext else ""
                fp.write(f"```{lang}\n")
                try:
                    with open(f, "r", encoding="utf-8", errors="replace") as fin:
                        data = fin.read()
                except Exception as e:
                    data = f"[READ_ERROR] {e}\n"
                fp.write(data)
                if not data.endswith("\n"):
                    fp.write("\n")
                fp.write("```\n")

                # если распухло — режем по частям (но без обрезки файлов)
                if fp.tell() > PART_MAX:
                    rotate()

            fp.close()

            # записать в глобальный индекс
            gidx.write(f"- `{root}` -> `docs/DIR_BOOKS_FULL_V2/{book_name}/00_INDEX.md`\n")
            books.append(book_name)

    print(f"✅ DONE. Books: {len(books)}")
    print(f"Output: {OUT_ROOT}")

if __name__ == "__main__":
    main()
