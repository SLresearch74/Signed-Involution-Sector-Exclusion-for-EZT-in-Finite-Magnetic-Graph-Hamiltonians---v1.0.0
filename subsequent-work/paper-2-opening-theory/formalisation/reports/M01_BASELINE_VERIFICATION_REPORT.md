# M0–M1 baseline verification report

Date: 4 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Verified modules

- `M3A.Types`: locked state, internal, source, and target types.
- `M3A.Model`: the exact six-state matrix `H0` and selected moment convention.
- `M3A.SignedInvolution`: the `rOrig` and `rAlt` signed matrices, their
  involution identities, their commutation identities with `H0`, the abstract
  signed certificate, and its all-depth selected-moment theorem.
- `M3A.BaselineDarkness`: the characteristic-zero baseline theorem.

## Principal theorem

```lean
theorem baseline_moments_dark
    {K : Type*} [Field K] [CharZero K] (k : Nat) :
    selectedMoment (H0 : Matrix State State K) k = 0
```

This is an all-depth theorem: `k` is arbitrary and no finite cutoff or
numerical interpolation is used.

## Build result

`lake build` completed successfully with 8662 jobs. The new import chain built
as separate modules:

```text
Built M3A.Types
Built M3A.Model
Built M3A.SignedInvolution
Built M3A.BaselineDarkness
Built M3AFormalisation
Build completed successfully
```

## Axiom report

Lean reported:

```text
'M3A.baseline_moments_dark' depends on axioms:
[propext, Classical.choice, Quot.sound]
```

These are standard Lean/Mathlib foundational axioms. The proof uses no
`sorry`, `admit`, `unsafe`, or user-declared axiom.

## Gate status

- M0 model lock: **complete**.
- M1 signed involutions and baseline darkness: **complete**.
- Analytic matrix-exponential darkness: deferred to the planned analytic
  bridge; it is not needed for the exact moment theorem.
- Next dependency node: M2, the exact selected numerator.
