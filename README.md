# Signed-Involution Sector Exclusion for Exact Zero Transfer

This repository is the research record for **Paper I**:

> Zach Medford (2026), *Signed-Involution Sector Exclusion for Exact Zero
> Transfer in Finite Magnetic Graph Hamiltonians*, version 1.0.0. Zenodo.
> [https://doi.org/10.5281/zenodo.20556571](https://doi.org/10.5281/zenodo.20556571)

Paper I remains the repository's primary work. It contains the manuscript,
finite graph certificate data, figures, diagnostic summaries, and audit scripts
for exact zero transfer in finite Hermitian graph Hamiltonians.

## Paper I

For a finite graph Hamiltonian $H$, source vertex $s$, and target vertex
$\ell$, exact zero transfer means

$$
\langle \ell \vert e^{-itH} \vert s \rangle = 0
\qquad\text{for every }t\in\mathbb R.
$$

Paper I relates this condition to moment, Krylov-space, and
spectral-projector channel closure. Its constructive sufficient certificate is
a signed involution $R$ satisfying

$$
R^2=I,\qquad [H,R]=0,\qquad
R\lvert s\rangle=\lvert s\rangle,\qquad
R\lvert\ell\rangle=-\lvert\ell\rangle.
$$

The Paper I materials are:

- [`paper/`](paper/) - manuscript source and PDF;
- [`data/`](data/) - certificate records and diagnostic summaries;
- [`figures/`](figures/) - the representative certificate figure;
- [`scripts/`](scripts/) - certificate-generation and audit scripts.

Paper I is supported by machine-readable finite computations, but Paper I is
**not** represented as an entirely Lean-formalised manuscript.

## Paper II: subsequent work

The clearly separated
[`subsequent-work/paper-2-opening-theory/`](subsequent-work/paper-2-opening-theory/)
subtree contains Paper II, *Kernel-Checked Opening Theory and
Coefficient-Sensitive Newton Geometry of a Six-State Dark Quantum Channel*.

Paper II uses Paper I's exact-zero equivalences and signed-certificate method,
then studies a locked six-state diagonal perturbation family. Its Lean 4
development is kernel-checked through stages M0-M8:

- signed involutions and all-depth baseline darkness;
- the exact selected numerator;
- the pointwise dark-plane decomposition and persistent certificates;
- locked endpoint-word support;
- ray coefficients and complete first-order protection;
- the fixed-ray trichotomy;
- the fixed-fibre Newton theorem; and
- the analytic bridge to the selected matrix exponential.

Paper II's later monomial-pullback, moving-arc, universal-atlas,
Groebner/Rees, and fixed-weight Noetherian sections remain conventional exact
proofs supported by scripts and finite artifacts. They are not described as
kernel-checked.

## Reproduction

Build the Paper II formalisation:

```powershell
cd subsequent-work/paper-2-opening-theory/formalisation
lake build
lake env lean M3AFormalisation.lean
```

Run the exact Paper II verifier and its discrepancy fixture:

```powershell
cd subsequent-work/paper-2-opening-theory
python CODE/verify_paper.py
python CODE/verify_paper.py --fixture
```

Compile the Paper II manuscript:

```powershell
cd subsequent-work/paper-2-opening-theory/paper/source
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The subtree README gives the theorem-stage map, artifact traceability, trust
boundary, pinned toolchain, and complete directory guide.

## Repository version status

Paper I's Zenodo record is version `v1.0.0`. At the time of this Paper II
integration, the GitHub repository has no published GitHub Release or Git tag;
the repository's `main` branch is therefore the version-control reference for
Paper I. Paper II is being introduced through an isolated draft pull request,
without merging or creating a release.

## Scope

The repository concerns finite graph Hamiltonians and finite-dimensional
linear algebra. It does not claim intrinsic topological protection, generic
robustness, experimental implementation, continuum geometry, spacetime,
gravity, or a new physical theory.

## Licence and citation

Code is released under the MIT License. See [`CITATION.cff`](CITATION.cff) for
machine-readable citation metadata and use DOI
[`10.5281/zenodo.20556571`](https://doi.org/10.5281/zenodo.20556571) when citing
Paper I.
