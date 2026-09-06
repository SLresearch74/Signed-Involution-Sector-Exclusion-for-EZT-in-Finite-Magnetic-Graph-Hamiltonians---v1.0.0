# Exact Zero-Transfer Research Archive

Research repository for finite-dimensional exact zero-transfer problems in Hermitian and oriented-circulant graph Hamiltonians.

## Research outputs

| Work | Authors | Status | Read | Reproduce |
|---|---|---|---|---|
| **From Zero Transfer to Structured Survival on Oriented-Circulant Baselines** | Zach Medford, Joshua Barker | Preprint package, 6 Sep 2026; Zenodo DOI pending | [PDF](subsequent-work/structured-survival/manuscript/main.pdf) · [LaTeX](subsequent-work/structured-survival/manuscript/main.tex) | [Package](subsequent-work/structured-survival/) · [Validation](subsequent-work/structured-survival/VALIDATION.md) |
| **Signed-Involution Sector Exclusion for Exact Zero Transfer in Finite Magnetic Graph Hamiltonians** | Zach Medford | Earlier manuscript in this repository | [PDF](paper/signed_involution_exact_zero_transfer_pst_revised.pdf) · [LaTeX](paper/signed_involution_exact_zero_transfer_pst_revised.tex) | [Data](data/) · [Scripts](scripts/) |

> **Current publication focus:** the structured-survival manuscript above. Its Zenodo record is being prepared separately so that the preprint and reproducibility archive have a paper-specific DOI rather than inheriting the identity of this older repository.

## Start here

For the current manuscript:

- [Read the paper](subsequent-work/structured-survival/manuscript/main.pdf)
- [Open the reproducibility package](subsequent-work/structured-survival/)
- [See exact validation results](subsequent-work/structured-survival/VALIDATION.md)
- [Use citation metadata](subsequent-work/structured-survival/CITATION.cff)
- [See Zenodo deposit metadata](subsequent-work/structured-survival/ZENODO_METADATA.md)
- [See licensing](subsequent-work/structured-survival/LICENSES.md)

For a map of newer work, see [`subsequent-work/README.md`](subsequent-work/README.md).

---

## Current manuscript: structured survival

**Zach Medford and Joshua Barker, _From Zero Transfer to Structured Survival on Oriented-Circulant Baselines_.**

The paper studies prescribed marked rank-one perturbations of known oriented-circulant zero-transfer baselines. It combines established finite-observability, invariant-kernel, polynomial-content and circulant Fourier methods and includes a bounded exact seven-block worked classification on the eight-site baseline.

The manuscript deliberately makes **no priority claim** for the precise seven-block arithmetic pattern and does **not** claim a new general observability or cyclotomic theory.

The accompanying package contains:

- manuscript PDF, LaTeX and bibliography;
- figure sources and generation script;
- compact paper-facing data;
- the full frozen T17 machine-readable ledger;
- T15/T16 upstream input ledgers;
- exact symbolic generators and independent verification scripts;
- SHA-256 integrity checks and a validation report.

---

## Earlier manuscript: signed-involution sector exclusion

The original repository work studies **exact zero-transfer pairs** in finite-dimensional Hermitian graph dynamics. For a Hamiltonian \(H\), source \(s\), and target \(\ell\), the channel is dark when

$$
\langle \ell|e^{-itH}|s\rangle=0
\qquad \forall t\in\mathbb R.
$$

The finite-dimensional spectral criterion is

$$
\langle \ell|P_\lambda|s\rangle=0
\qquad\text{for every spectral projector }P_\lambda.
$$

A signed involution supplies a sufficient sector-exclusion certificate when

$$
R^2=I,
\qquad [H,R]=0,
\qquad R|s\rangle=|s\rangle,
\qquad R|\ell\rangle=-|\ell\rangle.
$$

The corresponding `paper/`, `data/`, `figures/` and `scripts/` directories are retained for reproducibility and provenance.

---

## Repository map

```text
paper/                              earlier signed-involution manuscript
figures/                            earlier-paper figures
data/                               earlier-paper certificate and diagnostic data
scripts/                            earlier-paper analysis scripts

subsequent-work/
  README.md                         index of newer research outputs
  structured-survival/
    README.md                       paper-specific landing page
    CITATION.cff                    machine-readable citation metadata
    ZENODO_METADATA.md              deposit-ready metadata and DOI checklist
    LICENSES.md                     package licensing
    VALIDATION.md                   exact validation record
    SHA256SUMS                      integrity manifest
    verify_archive.py               archive verifier
    manuscript/                     PDF, LaTeX, bibliography, figures, exact checks
    supplementary/                  frozen T15/T16/T17 evidence and generators
```

---

## Reproducibility

The structured-survival archive is designed so that a reader can distinguish the frozen evidence from regenerated outputs. Its validation record reports successful paper-facing exact checks, full T17 regeneration, independent coefficient verification, archive-integrity checks and CFF schema validation.

Use the package-specific instructions in [`subsequent-work/structured-survival/README.md`](subsequent-work/structured-survival/README.md).

---

## Citation

The two manuscripts in this repository are separate scholarly objects and should be cited separately.

For the structured-survival preprint, use its [`CITATION.cff`](subsequent-work/structured-survival/CITATION.cff). Until the Zenodo DOI is inserted, cite the manuscript title, authors, version date and the exact GitHub revision used.

For the earlier signed-involution manuscript, use its own bibliographic record rather than the structured-survival record.

---

## Licensing

- Repository software is released under the [MIT License](LICENSE).
- The structured-survival manuscript, figures and data use the package-specific terms in [`subsequent-work/structured-survival/LICENSES.md`](subsequent-work/structured-survival/LICENSES.md).
- Separate scholarly works in this repository retain their own citation identity even when they share infrastructure.

---

## Scope

These projects concern finite graph and finite-dimensional linear-algebra computations. They do not claim to derive spacetime, gravity, quantum gravity, continuum Lorentzian geometry, generic physical dynamics, intrinsic topological protection or a universal theory of robustness.

## Authors

- Zach Medford
- Joshua Barker — co-author of the structured-survival manuscript

## Repository version

The repository name retains the historical `v1.0.0` identifier of the original signed-involution project. Paper-specific versioning for the structured-survival manuscript is maintained inside its own package and archival record.
