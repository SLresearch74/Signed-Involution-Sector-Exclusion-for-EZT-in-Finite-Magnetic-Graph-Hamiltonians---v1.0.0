#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python}"
LAKE_BIN="${LAKE_BIN:-lake}"
LATEXMK_BIN="${LATEXMK_BIN:-latexmk}"

"$PYTHON_BIN" CODE/verify_manifest.py
"$PYTHON_BIN" CODE/verify_paper.py
"$PYTHON_BIN" CODE/verify_paper.py --fixture
"$PYTHON_BIN" CODE/export_tables.py
cd formalisation
"$LAKE_BIN" build
"$LAKE_BIN" env lean M3AFormalisation.lean
cd ../paper/source
"$LATEXMK_BIN" -pdf -interaction=nonstopmode -halt-on-error main.tex

