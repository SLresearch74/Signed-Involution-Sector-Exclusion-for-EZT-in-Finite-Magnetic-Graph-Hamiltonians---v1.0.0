# Structured survival — at a glance

## Paper

**From Zero Transfer to Structured Survival on Oriented-Circulant Baselines**  
Zach Medford and Joshua Barker · version 1.0.0 · 6 September 2026

[Read the PDF](manuscript/main.pdf) · [Reproduce the calculations](README.md#reproduce-the-exact-results) · [Citation metadata](CITATION.cff)

## Question

Start with an oriented-circulant Hamiltonian containing an exact zero-transfer source/target pair. After a prescribed parameterised perturbation is introduced, ask two separate questions:

1. which declared one-dimensional blocks remain dark under the complete marked future;
2. which of those dark blocks remain dark under every declared continuation.

The paper calls the second property **structured survival**.

## Main organisational distinction

The paper separates:

- aggregate zero response;
- residual darkness of one declared block;
- survival of that darkness under all declared nonzero arrows.

These are different conditions even when they arise in the same finite realisation.

## Mathematical ingredients

The work deliberately uses established machinery:

- zero-transfer spectral/fibre criteria on circulants;
- finite observability and Markov-parameter tests;
- common invariant unobservable kernels;
- polynomial coefficient/content ideals;
- root-of-unity arithmetic;
- the Sherman–Morrison rank-one inverse update.

The contribution is the bounded synthesis and exact application of those tools to a prescribed marked perturbation model.

## One-event reduction

For a marked exact-dark pair, take

$$
A(t)=\bigl(a(t)|\ell\rangle+b(t)|s\rangle\bigr)\langle s|.
$$

With diagonal baseline Green function \(d(z)\), the marked scalar response reduces to

$$
\langle \ell|(zI-H_0-\varepsilon A)^{-1}|s\rangle
=
\frac{\varepsilon a(t)d(z)^2}{1-\varepsilon b(t)d(z)}.
$$

In the associated one-dimensional marked realisation, the block-content generator is controlled by the feed-forward amplitude \(a(t)\), while the declared-arrow content is controlled by the return amplitude \(b(t)\).

## Eight-site worked calculation

On the published \(n=8\), \(\mathcal C=\{1,3\}\) zero-transfer baseline, the paper gives a bounded seven-block classification. The exact archive contains:

- 16 marked components;
- 112 block generators;
- 204 arrow generators;
- 8 dark block-4 cases on the nonzero-amplitude stratum;
- exact symbolic verification and independent coefficient checks.

The precise arithmetic pattern is reported without a priority claim.

## What is not claimed

The paper does **not** claim:

- a new general observability theorem;
- a new invariant-subspace theorem;
- a new cyclotomic theory;
- a universal perturbation classification;
- priority over unpublished results unavailable to the authors for inspection.

## Reproducibility

The package includes the manuscript, full T17 ledger, upstream T15/T16 inputs, exact symbolic generator, independent verifier, SHA-256 manifest and validation record.

Start with [`VALIDATION.md`](VALIDATION.md) for the audit summary or [`README.md`](README.md) for exact commands.

## Archive status

A Zenodo DOI is being reserved. Once inserted, the DOI should be used as the canonical publication/outreach link, while this GitHub package remains the reproducibility source.
