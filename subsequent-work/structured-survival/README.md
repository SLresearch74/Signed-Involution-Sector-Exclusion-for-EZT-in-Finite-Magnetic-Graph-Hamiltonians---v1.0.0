# From Zero Transfer to Structured Survival on Oriented-Circulant Baselines

**Zach Medford and Joshua Barker**  
Preprint package · 6 September 2026 · version 1.0.0  
**Zenodo DOI:** pending reserved DOI insertion

[Read the paper](manuscript/main.pdf) · [LaTeX source](manuscript/main.tex) · [Citation metadata](CITATION.cff) · [Validation](VALIDATION.md) · [Zenodo metadata](ZENODO_METADATA.md) · [Licensing](LICENSES.md)

## What this package contains

This package accompanies a bounded synthesis/application study of prescribed marked rank-one perturbations of known oriented-circulant zero-transfer baselines. It combines established finite-observability, invariant-kernel, polynomial-content and circulant Fourier methods and includes a bounded exact seven-block worked classification on the eight-site baseline.

The manuscript makes **no priority claim** for the precise seven-block arithmetic pattern and does **not** claim a new general observability, invariant-subspace, cyclotomic or rank-one-update theory.

### Quick navigation

| Need | Go to |
|---|---|
| Read the manuscript | [`manuscript/main.pdf`](manuscript/main.pdf) |
| Inspect the source | [`manuscript/main.tex`](manuscript/main.tex) |
| Check references | [`manuscript/references.bib`](manuscript/references.bib) |
| Reproduce paper-facing exact checks | [`manuscript/reproducibility/`](manuscript/reproducibility/) |
| Inspect exact validation | [`VALIDATION.md`](VALIDATION.md) |
| Verify archive integrity | [`verify_archive.py`](verify_archive.py) and [`SHA256SUMS`](SHA256SUMS) |
| Inspect full frozen computation evidence | [`supplementary/`](supplementary/) |
| Cite the work | [`CITATION.cff`](CITATION.cff) |
| Prepare Zenodo deposit | [`ZENODO_METADATA.md`](ZENODO_METADATA.md) |
| Check licensing | [`LICENSES.md`](LICENSES.md) |

## Reproduce the exact results

From this directory, using Python 3.12 and SymPy 1.14.0:

```sh
python -m pip install -r requirements-exact.txt
python verify_archive.py
python manuscript/reproducibility/exact_checks.py
python supplementary/_T17_WORK/verify_t17.py
```

The archive verifier uses only the Python standard library. It checks integrity hashes, both upstream input hashes, the compact census and all 16 directional classifications against the full T17 ledger. The paper-facing script checks the eight-site matrix identities, spectrum, baseline darkness, diagonal Green function and affine rank-one expansion. The independent T17 verifier additionally checks 192 exact Gaussian-rational physical coefficients and exact Fourier pole signs.

To regenerate the complete symbolic ledger, work in a disposable copy of this directory:

```sh
python supplementary/_T17_WORK/t17_exact.py
python supplementary/_T17_WORK/verify_t17.py
```

The symbolic generator recomputes the locked regression, eight graph-realised families, formal controls and 888 prime-local nonvanishing cases. It overwrites the T17 JSON, and the independent verifier overwrites its verification JSON. Validate the frozen archive before regeneration so that original evidence and regenerated outputs remain distinguishable.

## Package layout

```text
structured-survival/
  README.md
  CITATION.cff
  ZENODO_METADATA.md
  LICENSES.md
  VALIDATION.md
  SHA256SUMS
  verify_archive.py
  requirements-exact.txt
  requirements-figures.txt

  manuscript/
    main.pdf
    main.tex
    references.bib
    data/
    figures/
    reproducibility/

  supplementary/
    T15_FREEZE_REPAIRS_RESPONSE_PROFILE/
    T16_ARITHMETIC_BLOCK_DARKNESS/
    T17_PRIME_POWER_ARITHMETIC_TAXONOMY/
    _T17_WORK/
```

Historical T17 readiness and prior-art reports are retained as provenance records. Their provisional drafting instructions and novelty assessments predate the final manuscript; the September manuscript controls the present claims and scope.

## Exact ledger and reported census

The full T17 ledger SHA-256 recorded by the package is:

```text
ed4e31ea0d45b7104d7b03ecd1d5df63295bc0b7a8e54c78462edf23e055fc33
```

The frozen census contains 16 marked components, 112 block generators and 204 arrow generators. Raw block counts are 48 unit, 56 proportional to \(t\) and 8 zero; after localisation to \(D(t)\), there are 104 unit and 8 zero. Raw arrow counts are 140 unit and 64 proportional to \(t\); all 204 become units on \(D(t)\). Eight of the 16 marked directions have dark block 4. These are bounded exact results for the prescribed families, not claims of a universal classification.

## Figures and manuscript build

To redraw the figures:

```sh
python -m pip install -r requirements-figures.txt
python manuscript/figures/generate_figures.py
```

To compile the manuscript, install LaTeX with `latexmk`, `biber` and `biblatex`, then:

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Floating-point values are used only for illustrations; no plot is used as proof.

## Citation and archive status

Until the Zenodo DOI is inserted, cite:

**Zach Medford and Joshua Barker, _From Zero Transfer to Structured Survival on Oriented-Circulant Baselines_, version 1.0.0, 6 September 2026**, together with the exact GitHub revision used.

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff). Deposit-ready metadata and the final DOI insertion checklist are in [`ZENODO_METADATA.md`](ZENODO_METADATA.md).

The DOI of the earlier signed-involution paper is a different scholarly record and must not be used for this manuscript.

## Authorship and assistance

The manuscript contains a transparency statement recording assistance from ChatGPT and Gemini. These tools are not authors. Responsibility for checking the mathematics, validating computations, verifying citations, auditing generated code/data and deciding on dissemination or submission remains with the named human authors.

Affiliations, ORCIDs and contact details have not been invented and may be added by the authors when appropriate.

## Licensing

Code is MIT-licensed. Unless otherwise stated, manuscript text, scholarly figures, tables and research data in this package are available under CC BY 4.0. See [`LICENSES.md`](LICENSES.md) for the scope and third-party-material note.

## Publication workflow

The remaining archive step is to insert the reserved Zenodo DOI consistently before the record is published. After DOI insertion, update affected hashes and validation records, then use the Zenodo DOI as the canonical outreach link and this GitHub directory as the reproducibility source.
