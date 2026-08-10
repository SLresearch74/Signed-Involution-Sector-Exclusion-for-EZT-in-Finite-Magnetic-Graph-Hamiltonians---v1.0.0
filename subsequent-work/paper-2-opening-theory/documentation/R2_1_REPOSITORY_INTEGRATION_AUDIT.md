# R2.1 repository integration audit

Audit date: 10 August 2026

## Supplied material

The author-supplied `PAPER 2.zip` has SHA-256
`F50753598C75EFE3E4770F35BC91AB5417747B17AA77D1A0DE8B2DDE02E17064`.
It contains 36 files: 24 LaTeX/BibLaTeX source files, one PDF and 11 generated
TeX build products. Its 36 files are byte-identical to the corresponding files
in the supplied integrated manuscript tree.

The ZIP is not treated as the complete evidence package. The supplied
integrated tree provides the scripts, data, expected output and figures; the
completed M0--M8 project provides the Lean source, lockfile and reports. The
202-row `SUPPLIED_ARTIFACT_INVENTORY.csv` records every inclusion,
replacement, exclusion and supersession decision. Of those rows, 155 are
included directly or through a byte-identical source, while 47 are excluded or
superseded with a reason. Exclusions comprise generated TeX products,
standalone workflow boilerplate, caches/logs, duplicate inputs and earlier
PDFs. No missing file has been fabricated.

Every repository-relative artifact path named by the R2.1 paper resolves in
this subtree. No paper-referenced artifact is absent from the combined
author-supplied material. The archive by itself did not contain the scripts,
data, figures or formalisation; that distinction is retained in the inventory.

## Current manuscript

The repository PDF is
`paper/M3A_KERNEL_CHECKED_OPENING_THEORY_R2.pdf`, SHA-256
`04A9D1A9B3699574F7ED05B9F7B0E8E427FD93A5A9A2029ED497702508533F15`.
It is a 30-page A4 PDF produced from `paper/source/main.tex`. The final LaTeX
log contains no overfull box, unresolved citation, unresolved reference, empty
bibliography or multiply-defined-label warning. All 30 rendered pages were
visually reviewed for clipping, overlap, figure/table placement, references
and page boundaries.

The source identifies this repository branch as the reproducibility location,
records that no repository tag or GitHub release existed at integration time,
and cites Paper I by its verified Zenodo DOI
`10.5281/zenodo.20556571` in Harvard author--date style.

## Verification status

- `python CODE/verify_paper.py`: passed and reproduced
  `EXPECTED/paper_verification.json` byte-for-byte.
- `python CODE/verify_paper.py --fixture`: passed and reproduced
  `DATA/discrepancy_detection.json` byte-for-byte.
- JSON syntax and internal artifact paths: passed.
- Root `CITATION.cff`: valid against the CFF 1.2.0 schema.
- Lean source escape scan for `sorry`, `admit`, user `axiom` and `unsafe`:
  passed.
- Lean toolchain: Lean 4.32.1 and Lake 5.0.0, pinned by `lean-toolchain` and
  `lake-manifest.json`.
- Kernel build: `lake build` completed successfully across 8,669 jobs, and
  `lake env lean M3AFormalisation.lean` also returned successfully. The 17
  Lean/configuration files committed here are SHA-256-identical to that built
  source tree. Axiom inspection reported only `propext`, `Classical.choice`
  and `Quot.sound`.

The kernel-checked scope ends with M8 and the fixed-fibre analytic bridge.
The moving-arc, universal-atlas, Gröbner/Rees and fixed-weight Noetherian
extensions remain conventional proofs, exact-computation audits or stated
scope boundaries as labelled in the manuscript.

## Repository boundary

Paper I remains the root work. Its manuscript, data, figures and scripts are
unchanged by this integration. Root-level changes are limited to citation and
documentation metadata plus ignore rules for generated Lean/TeX products.
Paper II is confined to `subsequent-work/paper-2-opening-theory/`.
