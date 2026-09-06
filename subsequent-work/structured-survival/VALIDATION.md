# Validation for the September 2026 repository addition

Validated on 6 September 2026 using Python 3.12.14 and SymPy 1.14.0.

- The supplied paper-facing exact-check script passed: Hermitian eight-site adjacency, H0^3 = 8H0, eigenvalue multiplicities, baseline darkness, diagonal Green function, affine rank-one expansion and compact census.
- The complete original T17 symbolic generator passed in an isolated copy using the included T15/T16 input ledgers: terminal regression, eight graph families, formal controls and 888 prime-local nonvanishing cases.
- The independent standard-library T17 verifier passed, including 192 exact Gaussian-rational physical coefficient comparisons and exact Fourier pole signs.
- The regenerated full T17 ledger and verification JSON both match the frozen originals byte for byte.
- Full-ledger SHA-256 agrees with the source hash embedded in the manuscript tables: `ed4e31ea0d45b7104d7b03ecd1d5df63295bc0b7a8e54c78462edf23e055fc33`.
- The compact census and all 16 manuscript direction outcomes agree with individual records in the full ledger.
- The archive verifier was checked against the real source data and rejected corrupted hashes, duplicate or missing required manifest entries, incorrect directional classifications and unsafe paths.
- `CITATION.cff` passed CFF 1.2.0 schema validation.
- The supplied PDF has 15 pages; its title, authors and date match the LaTeX. The title page and the three figure/table pages were visually checked. The PDF, manuscript source, bibliography, figure assets and supplied computation files were copied without content changes. The manuscript was not rebuilt for this repository addition.

The scripts and stored records establish the stated finite computational checks. They do not constitute a new independent review of every mathematical proof or a Lean formalisation of this manuscript.

The DOI deposit remains pending. Historical T17 drafting and prior-art notes are preserved for provenance; they do not supersede the September manuscript's final scope and wording.
