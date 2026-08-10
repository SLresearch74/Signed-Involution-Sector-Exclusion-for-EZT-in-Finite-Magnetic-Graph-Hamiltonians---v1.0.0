from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST.sha256"
EXCLUDED_PARTS = {"tmp", "__pycache__", ".lake"}
EXCLUDED_SUFFIXES = {
    ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
    ".run.xml", ".synctex.gz", ".toc",
}


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        any(part in EXCLUDED_PARTS for part in rel.parts)
        or rel.as_posix() == "paper/source/main.pdf"
        or any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)
    )


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


expected: dict[str, str] = {}
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    value, rel = line.split("  ", 1)
    expected[rel] = value

actual_paths = {
    path.relative_to(ROOT).as_posix(): path
    for path in ROOT.rglob("*")
    if path.is_file()
    and path != MANIFEST
    and not excluded(path)
}
missing = sorted(set(expected) - set(actual_paths))
extra = sorted(set(actual_paths) - set(expected))
changed = sorted(rel for rel in set(expected) & set(actual_paths) if digest(actual_paths[rel]) != expected[rel])
if missing or extra or changed:
    print(f"FALSIFIED missing={missing} extra={extra} changed={changed}")
    raise SystemExit(1)
print(f"VERIFIED-BYTE manifest_entries={len(expected)}")
