# Uncited and unused reference report

The final citation/build audit removes bibliography entries not cited in the manuscript. `Stanley1980` is retained only if the D-finite comparison sentence remains; all other entries have an explicit in-text role mapped in `CLAIM_TO_REFERENCE_LEDGER.csv`.

The build-stage script compares citation keys in `.bcf` with entries in `references.bib`. Any residual unused entry is an editorial issue rather than theorem evidence and must be removed before public submission.

