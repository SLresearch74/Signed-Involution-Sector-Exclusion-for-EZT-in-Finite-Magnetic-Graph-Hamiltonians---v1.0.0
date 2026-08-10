# Reproducibility protocol

## Prerequisites

- Python 3.10 or later; the exact verifier uses only the standard library.
- A TeX Live 2026-compatible installation with `latexmk`, pdfLaTeX, Biber, `biblatex`, TikZ, `cleveref` and the standard AMS packages.
- A PDF rasteriser for visual inspection.

## Deterministic exact checks

From the release root:

```text
python CODE/verify_manifest.py
python CODE/verify_paper.py
python CODE/verify_paper.py --fixture
python CODE/export_tables.py
```

The manifest command must report `VERIFIED-BYTE`. The first mathematical command must report `VERIFIED-EXACT`, a 52-term denominator, signed minimal layer `[1,-1,1,-1]`, ARC1 survivor `4/5`, GF1 survivor `-32/15`, a valid 16-cone atlas and a valid 15-cell atlas.

The fixture must report `FALSIFIED` for the perturbed theorem and set both route-detection fields to true. This is the expected falsifier outcome.

## Paper build

```text
cd PAPER
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`latexmk` invokes Biber and repeats pdfLaTeX until references stabilise. Inspect the log for undefined references, missing citations, overfull boxes and font errors.

## Fresh-extraction test

1. Extract the compact release archive into a new directory.
2. Verify its sidecar SHA-256.
3. Run the manifest check and the three exact commands above.
4. Remove any pre-existing `PAPER/main.pdf` and auxiliary files in the extracted copy.
5. Run the paper build.
6. Compare the exact JSON and generated atlas tables byte-for-byte with `EXPECTED` and `DATA` in the release.
7. Render every page and inspect the title page, formulas, tables, figures, bibliography and final page.

The workstation TeX distribution required a clean path because its Windows resolver failed beneath a path containing spaces. This is a tool-path issue, not a scientific dependency; a normal TeX installation on `PATH` should use the commands unchanged.

## Manifest policy

`MANIFEST.sha256` contains one SHA-256 line for every payload file except itself and archive sidecars. Regenerate it only after every content change, then build the compact archive and hash the archive separately.
