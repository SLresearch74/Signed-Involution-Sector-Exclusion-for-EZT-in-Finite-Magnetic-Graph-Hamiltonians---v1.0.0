from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT.parent / "M3A_PAPER_II_OPENING_THEORY_R2_1.zip"
SIDECAR = ARCHIVE.with_suffix(ARCHIVE.suffix + ".sha256")
EXCLUDED_PARTS = {"tmp", "__pycache__", ".lake"}
EXCLUDED_SUFFIXES = {
    ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out",
    ".run.xml", ".synctex.gz", ".toc",
}
STAMP = (2026, 8, 10, 12, 0, 0)


def excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return (
        any(part in EXCLUDED_PARTS for part in rel.parts)
        or rel.as_posix() == "paper/source/main.pdf"
        or any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)
    )


paths = [
    path
    for path in ROOT.rglob("*")
    if path.is_file() and not excluded(path)
]
with ZipFile(ARCHIVE, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(paths):
        rel = Path(ROOT.name) / path.relative_to(ROOT)
        info = ZipInfo(rel.as_posix(), STAMP)
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

h = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
SIDECAR.write_text(f"{h}  {ARCHIVE.name}\n", encoding="ascii", newline="\n")
print(f"VERIFIED-BYTE archive_sha256={h} files={len(paths)}")
