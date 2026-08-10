# M3 dark-plane verification report

Date: 4 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Pointwise decomposition

The module defines

```text
Plane A: d₁=d₂ and d₃=d₄
Plane B: d₁=d₄ and d₃=d₂
```

and verifies:

```lean
theorem ell_quad_zero_iff_planes
    {K : Type*} [CommRing K] [IsDomain K] (v : Internal → K) :
    linearCoeff v = 0 ∧ quadraticCoeff v = 0 ↔
      OnPlaneA v ∨ OnPlaneB v
```

The proof eliminates the linear equation and certifies the factorisation

```text
(d₂-d₃)(d₄-d₃) = Q + d₃L.
```

No-zero-divisors then gives the two branches. The theorem holds over every
integral domain, strengthening the field-level point-set statement required by
the manuscript.

Lean also verifies that the two plane predicates intersect exactly on the
scalar line `d₁=d₂=d₃=d₄`.

## Persistent certificates

- `rOrig_commutes_hamiltonian_of_planeA` proves that the original signed
  involution commutes with the full perturbed Hamiltonian on plane A.
- `rAlt_commutes_hamiltonian_of_planeB` proves the corresponding statement for
  the alternative involution on plane B.
- Each result is packaged as a `SignedCertificate` with the already verified
  endpoint characters and involution identity.

Consequently, `planeA_moments_dark` and `planeB_moments_dark` prove exact
selected-moment vanishing for every depth. The combined theorem
`moments_dark_of_linear_quadratic_zero` verifies that `L=Q=0` implies all-depth
darkness, using the certified plane decomposition to select the appropriate
involution.

The independent cofactor route is retained as
`selectedNumerator_eq_zero_of_linear_quadratic_zero`.

## Build and axiom report

`lake build` completed successfully with 8664 jobs. Lean reported for the
principal M3 theorems:

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Lean/Mathlib foundational axioms. The module uses no
`sorry`, `admit`, `unsafe`, or user-declared axiom.

## Scope boundary

M3 proves the pointwise union of planes and the persistent certificates. The
stronger equality of ideals in `MvPolynomial` remains a separately declared
extension; it is not required by the fixed-ray or fixed-fibre dependency
chain.

## Gate status

- M0 model lock: **complete**.
- M1 signed involutions and baseline darkness: **complete**.
- M2 exact selected numerator: **complete**.
- M3 dark-plane decomposition and certificates: **complete**.
- Next dependency node: M4, endpoint-access word support.
