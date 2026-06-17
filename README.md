# Signed-Involution Sector Exclusion for Exact Zero Transfer

Research repository for the manuscript:

**Signed-Involution Sector Exclusion for Exact Zero Transfer in Finite Magnetic Graph Hamiltonians**
Zach Medford, 2026

This repository contains the manuscript source, certificate data, diagnostic summaries, figures, and audit scripts supporting the finite graph computations reported in the paper.

---

## Overview

This project studies **exact zero-transfer pairs** in finite-dimensional Hermitian graph dynamics.

Given a finite graph Hamiltonian (H), a source vertex (s), and a target vertex (\ell), the central condition is

[
\langle \ell|e^{-itH}|s\rangle = 0
\qquad
\forall t \in \mathbb{R}.
]

The manuscript develops a finite algebraic framework for this condition using:

* moment, Krylov, and spectral-projector characterisations;
* invariant-sector and symmetry-sector exclusion;
* signed-involution certificates;
* magnetic ({0,\pi})-phase graph Hamiltonians;
* M3A certificate-generation data;
* Layer-2 spectral-projector diagnostics;
* perturbative sector-breaking diagnostics;
* Lindblad block-preservation criteria.

The repository is intended to make the finite graph computations, certificate records, and diagnostic summaries reproducible.

---

## Main claim

The paper’s central finite-dimensional statement is that exact zero transfer is equivalent to **spectral-projector channel closure**:

[
\langle \ell|P_\lambda|s\rangle = 0
\qquad
\text{for every spectral projector } P_\lambda.
]

Signed-involution certificates provide a constructive sufficient mechanism. If

[
R^2=I,
\qquad
[H,R]=0,
\qquad
R|s\rangle=|s\rangle,
\qquad
R|\ell\rangle=-|\ell\rangle,
]

then the source and target lie in orthogonal invariant sectors, and exact zero transfer follows for all time.

---

## Repository contents

```text
paper/
  signed_involution_exact_zero_transfer_pst_revised.pdf
  signed_involution_exact_zero_transfer_pst_revised.tex

figures/
  m3a_representative_certificates.png

data/
  m3a_candidates.csv
  m3a_graph_records.csv
  m3a_phase_records.csv
  m3a_flux_records.csv
  l2_spectral_projector_audit_summary.md
  test1_zero_baseline_summary.csv
  test2_sector_breaking_scaling_summary.csv
  test3_bound_summary.csv
  test4_summary.csv
  test5_projector_summary.csv
  test6_target_resolved_summary.csv

scripts/
  magnetic_phase_search_M3A_symmetry_first_fast.py
  test5_projector_dependence.py
  test6_target_resolved_sector_breaking.py
```

---

## File guide

### `paper/`

Contains the final manuscript PDF and LaTeX source.

### `figures/`

Contains the representative M3A certificate figure used in the manuscript.

### `data/`

Contains the machine-readable certificate records and diagnostic summaries.

The M3A certificate data include:

* `m3a_graph_records.csv` — graph support records;
* `m3a_candidates.csv` — candidate identifiers, source-target pairs, involutions, sign functions, and audit norms;
* `m3a_phase_records.csv` — edge-level phase/sign data defining the signed magnetic Hamiltonians;
* `m3a_flux_records.csv` — cycle-basis flux records.

The diagnostic summaries include:

* `l2_spectral_projector_audit_summary.md` — compact Layer-2 spectral-projector audit summary;
* `test1_zero_baseline_summary.csv` — sector-preserving perturbation baseline;
* `test2_sector_breaking_scaling_summary.csv` — sector-breaking scaling audit;
* `test3_bound_summary.csv` — finite-time bound audit;
* `test4_summary.csv` — non-sufficiency of broken-sector diagnostics;
* `test5_projector_summary.csv` — projector-dependence diagnostics;
* `test6_target_resolved_summary.csv` — target-resolved sector-breaking diagnostics.

### `scripts/`

Contains the main certificate-generation and diagnostic audit scripts.

---

## Reproducibility

The certificate records in `data/` are sufficient to reconstruct the reported signed-involution certificates.

For each certificate, the relevant data are:

1. the graph support;
2. the source-target pair ((s,\ell));
3. the involution (r);
4. the sign function (\sigma);
5. the edge-level phase/sign assignment;
6. the corresponding audit norms.

The certificate condition is

[
R^2=I,
\qquad
[H,R]=0,
\qquad
R|s\rangle=|s\rangle,
\qquad
R|\ell\rangle=-|\ell\rangle.
]

The Layer-2 diagnostic checks spectral-projector channel closure:

[
\langle \ell|P_\lambda|s\rangle=0
\qquad
\forall \lambda.
]

The perturbation diagnostics test sector-preserving perturbations, sector-breaking scaling, finite-time bounds, projector dependence, and target-resolved first-order leakage.

---

## Scope and limitations

This repository contains finite graph and finite-dimensional linear-algebra computations.

It does **not** claim to derive:

* spacetime;
* gravity;
* quantum gravity;
* continuum Lorentzian geometry;
* physical dynamics;
* intrinsic topological protection;
* generic robustness;
* or a new physical theory.

The results concern exact zero-transfer structure in finite Hermitian graph Hamiltonians and the finite computations reported in the manuscript.

Related finite-duality and FCC local-to-global obstruction results are being developed separately.

---

## How to cite

If you use this repository, please cite the associated Zenodo DOI:

```text
[Zenodo DOI to be added after release]
```

A `CITATION.cff` file may also be included for citation metadata.

---

## Licence

Code in this repository is released under the MIT License.

The manuscript, figures, and data files are provided for scholarly citation and reproducibility. Unless otherwise stated, non-code materials may be reused with attribution and citation of the associated Zenodo DOI.

---

## Author

Zach Medford

---

## Version

`v1.0.0`
