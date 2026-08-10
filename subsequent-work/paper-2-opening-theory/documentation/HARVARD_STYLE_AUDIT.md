# Harvard style audit

The manuscript uses `biblatex` with the `authoryear` style and Biber. In-text references are author--date citations; the bibliography is alphabetised by author. DOI fields are preferred over mutable URLs when a DOI was verified.

Version R2.1 also sets `useprefix=true`, so the name prefix in `(de Moura and Ullrich, 2021)` is preserved. The formal-methods citations are the primary Lean 4 system paper and the Mathlib community paper; both DOI records are included in `CITATION_VERIFICATION_LEDGER.csv`.

Checks performed:

- every citation key in the TeX source resolves in `references.bib`;
- the Biber build reports no missing citations;
- Paper I carries its verified Zenodo DOI `10.5281/zenodo.20556571`, while the earlier Paper II R1.2 manuscript remains typed `unpublished` without an invented identifier;
- article titles, journal titles, volumes, pages/eIDs and verified DOIs are present;
- web-only arXiv metadata is used only for Sett et al. (2019), with the primary arXiv record;
- citations support contextual claims and are not used to transfer a standard framework into a priority claim.
- the Lean and Mathlib citations document the proof environment; the evidence for the M3A theorems is the checked formal source, not those citations.

The citation verification basis is in `CITATION_VERIFICATION_LEDGER.csv`.
