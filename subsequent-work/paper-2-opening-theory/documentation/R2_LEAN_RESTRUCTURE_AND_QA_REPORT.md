# R2 Lean-centred restructure and QA report

Date: 9 August 2026
Result: **PASS**

## Editorial restructure

- Retitled the manuscript around its kernel-checked fixed-ray and fixed-fibre contribution.
- Rewrote the abstract and introduction so the M0--M8 formal development is the principal evidentiary spine.
- Added a theorem-to-Lean architecture section and detailed appendix traceability map.
- Added theorem-level formal-status annotations to baseline darkness, the selected numerator, pointwise dark planes, locked endpoint support, the fixed-ray trichotomy and the fixed-fibre Newton theorem.
- Separated the Lean-checked pointwise dark-plane result from the conventionally proved multivariate ideal equality.
- Marked the post-fixed-fibre pullback, arc, atlas, Groebner/Rees and Noetherian results as outside the current Lean package.
- Rewrote reproducibility, scope and conclusion sections around the explicit trust boundary.

## Citations

- The manuscript uses Biber with `biblatex` author--date style, name--year commas, alphabetical sorting and preserved surname prefixes.
- Added and verified the primary Lean 4 and Mathlib papers:
  - de Moura and Ullrich (2021), DOI `10.1007/978-3-030-79876-5_37`;
  - The mathlib Community (2020), DOI `10.1145/3372885.3373824`.
- All 24 cited keys resolve; no bibliography entry is missing from the final build.

## Build and visual QA

- Engine: pdfTeX 1.40.29, TeX Live 2026; latexmk 4.88; Biber 2.21.
- Output: 30 A4 pages.
- Final log: no undefined references, undefined citations, duplicate labels, empty bibliography or overfull boxes.
- Every page was rasterised at 110 dpi and inspected in eight contact sheets.
- The title/abstract, formal architecture table, theorem annotations, scope transition, reproducibility section, Lean traceability tables and Harvard bibliography were also inspected at page resolution.
- No clipping, overlap, cropped figures, broken glyphs or unreadable tables were found.

The historical R1.0 archive and manifest are not silently rewritten by this report; R2 is the revised manuscript source and PDF produced from the current `PAPER` tree.
