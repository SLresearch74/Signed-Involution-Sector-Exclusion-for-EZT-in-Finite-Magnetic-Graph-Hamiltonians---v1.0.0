"""Check archive integrity and manuscript/T17 consistency using standard Python.

Run ``python verify_archive.py`` from any directory, or supply ``--root PATH``.
This checks the recorded data; run the supplementary T17 scripts to recompute
the mathematical certificates. No archive files are modified.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


PAPER = "manuscript/data/paper_tables.json"
T17 = "supplementary/T17_PRIME_POWER_ARITHMETIC_TAXONOMY/T17_MACHINE_READABLE.json"
UPSTREAM = (
    "T15_FREEZE_REPAIRS_RESPONSE_PROFILE/T15_MACHINE_READABLE.json",
    "T16_ARITHMETIC_BLOCK_DARKNESS/T16_MACHINE_READABLE.json",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def archive_path(root: Path, relative: str) -> Path:
    parts = relative.split("/")
    require(
        bool(relative)
        and not PurePosixPath(relative).is_absolute()
        and "\\" not in relative
        and ":" not in relative
        and all(part not in ("", ".", "..") for part in parts),
        f"Unsafe or non-POSIX archive path: {relative!r}",
    )
    path = root.joinpath(*parts).resolve()
    require(path.is_relative_to(root), f"Path leaves the archive: {relative!r}")
    require(path.is_file(), f"Missing archive file: {relative}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(root: Path, relative: str) -> dict:
    try:
        data = json.loads(archive_path(root, relative).read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {relative}: {error}") from error
    require(isinstance(data, dict), f"Expected a JSON object in {relative}")
    return data


def verify(root: Path) -> None:
    manifest = root / "SHA256SUMS"
    require(manifest.is_file(), f"Missing manifest: {manifest}")
    hashes = {}
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-fA-F]{64})  (.+)", line)
        require(match is not None, f"Malformed SHA256SUMS line {number}")
        expected, relative = match.groups()
        require(relative != "SHA256SUMS", "SHA256SUMS must not list itself")
        require(relative not in hashes, f"Duplicate manifest path: {relative}")
        actual = sha256(archive_path(root, relative))
        require(actual == expected.lower(), f"SHA256 mismatch: {relative}")
        hashes[relative] = actual
    require(bool(hashes), "SHA256SUMS is empty")
    for relative in (PAPER, T17, *("supplementary/" + name for name in UPSTREAM)):
        require(relative in hashes, f"Required data file is absent from SHA256SUMS: {relative}")
    print(f"PASS: SHA256SUMS validates {len(hashes)} files.")

    paper = read_json(root, PAPER)
    ledger = read_json(root, T17)
    require(paper["source_ledger"] == "T17_MACHINE_READABLE.json", "Unexpected paper source ledger")
    require(paper["source_sha256"] == hashes[T17], "Paper source_sha256 differs from the full T17 ledger")
    require(set(ledger["input_hashes"]) == set(UPSTREAM), "Unexpected T17 upstream input inventory")
    for relative in UPSTREAM:
        require(
            ledger["input_hashes"][relative] == hashes["supplementary/" + relative],
            f"T17 upstream input hash mismatch: {relative}",
        )
    print("PASS: paper source hash and both T17 upstream input hashes agree.")

    locked = ledger["locked_n8"]
    table = paper["locked_n8"]
    components = locked["components"]
    blocks = [block for component in components for block in component["blocks"]]
    edges = [edge for component in components for edge in component["edges"]]
    require(table["components"] == len(components) == 16, "Locked component count must be 16")
    require(len(blocks) == 112 and len(edges) == 204, "Locked census must contain 112 blocks and 204 edges")
    counts = {
        "block_raw_counts": dict(Counter(block["g_raw"] for block in blocks)),
        "block_normalized_counts": dict(Counter(block["g_stratum_normalized"] for block in blocks)),
        "edge_raw_counts": dict(Counter(edge["h_raw"] for edge in edges)),
        "edge_normalized_counts": dict(Counter(edge["h_stratum_normalized"] for edge in edges)),
        "earliest_unit_histogram": dict(Counter(
            str(block["earliest_unit_certificate"])
            for block in blocks if block["earliest_unit_certificate"] is not None
        )),
    }
    for key, actual in counts.items():
        require(table[key] == locked[key] == actual, f"Census field disagrees with individual records: {key}")
    for key in ("all_locked_K0_Kmax_match_T15", "mixed_factors_absent"):
        require(table[key] is True and locked[key] is True, f"Expected true census status: {key}")
    print("PASS: census fields agree with all 16 components, 112 blocks and 204 edges.")

    by_id = {component["component_id"]: component for component in components}
    require(len(by_id) == 16, "Duplicate locked component_id")
    rows = table["classification"]
    require(len(rows) == 8, "The manuscript classification must contain eight event rows")
    checked = set()
    dark_count = 0
    for row in rows:
        event = row["event"]
        require(isinstance(event, str) and re.fullmatch(r"\(\d+,\d+\)", event) is not None,
                f"Invalid classification event: {event!r}")
        for field, direction in (("forward_dark", "forward_0_to_2"), ("reverse_dark", "reverse_2_to_0")):
            component_id = event[:-1] + "," + direction + ")"
            require(component_id in by_id, f"Classification component is missing: {component_id}")
            require(component_id not in checked, f"Duplicate classification: {component_id}")
            dark = row[field]
            require(isinstance(dark, bool), f"Expected Boolean {field} for {event}")
            expected = [4] if dark else []
            component = by_id[component_id]
            require(component["K0"] == component["Kmax"] == expected,
                    f"Manuscript darkness disagrees with K0/Kmax for {component_id}")
            checked.add(component_id)
            dark_count += int(dark)
    require(checked == set(by_id) and dark_count == 8,
            "Classification must cover all 16 directions with eight dark block-4 outcomes")
    print("PASS: all 16 directional classifications agree; eight have dark block 4.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent,
                        help="archive directory containing SHA256SUMS (default: this script's directory)")
    args = parser.parse_args()
    try:
        verify(args.root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Archive verification FAILED: {error}", file=sys.stderr)
        return 1
    print("Archive verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
