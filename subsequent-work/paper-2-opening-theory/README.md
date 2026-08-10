# Paper II: kernel-checked opening theory

This subtree is subsequent work to the repository's primary Paper I. It
contains version R2.1 of:

> Zach Medford (2026), *Kernel-Checked Opening Theory and
> Coefficient-Sensitive Newton Geometry of a Six-State Dark Quantum Channel*.

Paper I supplies the model-independent exact-zero equivalences and the
signed-involution certificate method. Paper II studies the coefficient-sensitive
opening theory of one locked six-state diagonal family. Paper I is citable at
[`10.5281/zenodo.20556571`](https://doi.org/10.5281/zenodo.20556571); Paper II
does not yet have a separate DOI or release.

## Theorem-stage map

| Stage | Kernel-checked content | Principal Lean entry points |
|---|---|---|
| M0-M1 | Locked model, signed involutions, all-depth baseline darkness | `M3A.BaselineDarkness`; `baseline_moments_dark` |
| M2 | Exact unreduced selected cofactor numerator | `M3A.SelectedNumerator`; `selectedNumerator_formula` |
| M3 | Pointwise dark-plane union and persistent certificates | `M3A.DarkPlanes`; `ell_quad_zero_iff_planes` |
| M4 | Locked endpoint support and signed boundary power sum | `M3A.EndpointWords`; `sixState_support_bound`, `sixState_boundary_ray` |
| M5 | Exact ray/amplitude coefficients and complete first-order protection | `M3A.RayCoefficients`; `amplitudeCoeff_one_eq_zero_of_linear_zero` |
| M6 | Exhaustive fixed-ray classifier and trichotomy | `M3A.FixedRayTrichotomy`; `classifyRay_eq_*_iff`, `classifyRay_spec`, `fixedRay_trichotomy` |
| M7 | Actual-support Newton orthants and positive-weight faces | `M3A.FixedFibreNewton`; `fixedFibre_newton`, `fixedFibre_positiveWeight_faces` |
| M8 | Convergent analytic bridge to the selected matrix exponential | `M3A.AnalyticBridge`; `selectedRayAmplitude_eq_tsum_coefficients` |

The detailed paper-to-Lean map is in
[`formalisation/reports/M3A_THEOREM_TO_LEAN_DEPENDENCY_MAP.md`](formalisation/reports/M3A_THEOREM_TO_LEAN_DEPENDENCY_MAP.md).

## Trust boundary

The M0-M8 statements named above are checked by Lean 4.32.1 against Mathlib
v4.32.1. The included milestone reports record successful builds and axiom
inspection. The Lean source contains no `sorry`, `admit`, user-declared axiom,
or `unsafe` declaration.

The following Paper II extensions are **not** part of the present Lean package:

- the fully general rectangular endpoint theorem;
- the scheme-theoretic multivariate ideal equality;
- monomial-fibre aggregation;
- moving analytic arcs and their tie rule;
- the universal multivariate Newton atlas;
- the Groebner/Rees and marked-section results; and
- the fixed-weight Noetherian theorem.

These sections have conventional exact proofs and supplied regression
artifacts. Script verification does not promote them to kernel-checked claims.

## Directory guide

```text
paper-2-opening-theory/
  README.md
  MANIFEST.sha256
  REPRODUCE.ps1
  REPRODUCE.sh
  paper/
    source/                    LaTeX and Harvard-style bibliography
    M3A_KERNEL_CHECKED_OPENING_THEORY_R2.pdf
  formalisation/
    M3AFormalisation.lean
    lakefile.toml
    lake-manifest.json
    lean-toolchain
    M3A/                       M0-M8 Lean modules
    reports/                   dependency map and milestone reports
  CODE/                        exact verifier and manifest utilities
  DATA/                        exact denominator, atlas, and audit data
  EXPECTED/                    expected verifier output
  FIGURES/SOURCE/              TikZ figure source
  FIGURES/EXPORT/              supplied vector exports
  documentation/               provenance, audit, and inventory records
```

## Exact reproduction

From this directory on Windows:

```powershell
python CODE/verify_manifest.py
python CODE/verify_paper.py
python CODE/verify_paper.py --fixture
python CODE/export_tables.py
cd formalisation
lake build
lake env lean M3AFormalisation.lean
cd ..\paper\source
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Or run `REPRODUCE.ps1`. On Unix-like systems, run `./REPRODUCE.sh`.

The manuscript uses Biber through `latexmk`. Its final reviewed PDF is stored
one level above the source tree. Generated TeX auxiliaries and compiled Lean
artifacts are excluded from version control and from the release manifest.

## Artifact traceability

- `EXPECTED/paper_verification.json` records the exact numerator, denominator,
  endpoint, arc, and atlas checks.
- `DATA/discrepancy_detection.json` records the deliberately perturbed fixture.
- `DATA/MV1_15_CELL_ATLAS.json` and `DATA/GF1_16_CONE_ATLAS.json` are the finite
  atlas artifacts cited by the conventional extension sections.
- `documentation/SUPPLIED_ARTIFACT_INVENTORY.csv` lists every audited supplied
  file, its SHA-256 digest, and its inclusion or exclusion disposition.
- `MANIFEST.sha256` covers every committed Paper II payload file other than the
  manifest itself and excluded build products.

`PAPER 2.zip` supplied 24 manuscript-source files, one PDF, and 11 generated
TeX auxiliaries. The manuscript sources matched the integrated Paper II source
byte-for-byte. The auxiliaries were audited but not committed. The separate
integrated source directory supplied the referenced code, data, expected
output, and figures; the completed `Documents/M3AFormalisation` project supplied
the M0-M8 Lean sources and reports. No absent artifact was fabricated.

## Repository and version status

Repository:
[`SLresearch74/Signed-Involution-Sector-Exclusion-for-EZT-in-Finite-Magnetic-Graph-Hamiltonians---v1.0.0`](https://github.com/SLresearch74/Signed-Involution-Sector-Exclusion-for-EZT-in-Finite-Magnetic-Graph-Hamiltonians---v1.0.0)

The GitHub repository had no Release or Git tag when this subtree was prepared
on 10 August 2026. Integration is therefore performed on branch
`agent/doi-lean-r2-tightening` through a draft pull request; no merge or release
is part of this work.

