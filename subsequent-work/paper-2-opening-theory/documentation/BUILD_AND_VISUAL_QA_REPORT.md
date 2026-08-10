# Build and visual QA report

## Build result

Evidence: `VERIFIED-BYTE`.

- Clean short-path build command: `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`.
- Engine: pdfTeX 1.40.29, TeX Live 2026; latexmk 4.88; biber 2.21.
- Output: `PAPER/main.pdf`, 25 A4 pages.
- Final build log: no undefined references, undefined citations, duplicate labels, missing figures, empty bibliography, or overfull boxes.
- All eight TikZ source diagrams also compile as standalone vector PDFs in `FIGURES/EXPORT`.

## Visual result

Evidence: `VERIFIED-BYTE` for 25 rendered pages.

Every page was rasterised at 120 dpi and reviewed in three contact sheets. Pages containing the evidence-chain diagram, universal MV1 figure, 15/16 atlas tables and claim--code table were additionally inspected at page resolution. One label collision in Figure 1 was found, corrected in the TikZ source, rebuilt and re-rendered. The final review found no clipped text, overlapping labels, cropped figures, broken glyphs or unreadable tables.

Rendered review images were treated as temporary QA material and are not part of the compact release.
