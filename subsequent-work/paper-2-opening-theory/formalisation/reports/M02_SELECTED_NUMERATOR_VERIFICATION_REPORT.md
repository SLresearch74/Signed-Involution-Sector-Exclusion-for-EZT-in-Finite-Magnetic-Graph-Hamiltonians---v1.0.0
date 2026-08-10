# M2 selected-numerator verification report

Date: 4 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Verified construction

The formalisation defines the locked family

```text
H(d) = H0 + diag(0,d1,d2,d3,d4,0)
B(z,d) = z I - H(d)
```

and constructs the selected minor by explicit embeddings that delete row 0
and column 5. The selected numerator is the unreduced cofactor

```text
N(z,d) = -det(B(z,d) with row 0 and column 5 deleted).
```

The negative sign is the cofactor sign `(-1)^(0+5)`. Lean separately proves
that this submatrix equals the declared explicit `5 × 5` minor before
expanding its determinant.

## Principal theorem

```lean
theorem selectedNumerator_formula {K : Type*} [CommRing K]
    (z : K) (d : Internal → K) :
    selectedNumerator z d =
      linearCoeff d * (z ^ 2 + 2 * z) +
      2 * quadraticCoeff d * (z + 1) +
      cubicNumeratorCoeff d
```

Thus Lean verifies the actual-coordinate identity

```text
N = L(z²+2z) + 2Q(z+1) + R
```

over every commutative ring. The proof is a direct finite determinant
expansion followed by ring normalisation; it uses no interpolation, sampling,
or external symbolic result as a premise.

## Corollaries

- `selectedNumerator_ray_formula` verifies
  `N(z,εv) = εℓ(z²+2z) + 2ε²Q(z+1) + ε³R`.
- `cubicNumeratorCoeff_syzygy` exposes the existing coefficient syzygy in
  four-coordinate notation.
- `cubicNumeratorCoeff_eq_zero_of_linear_quadratic_zero` verifies that
  `L = Q = 0` forces `R = 0`, eliminating a separate cubic branch.

## Build and axiom report

`lake build` completed successfully with 8663 jobs. Lean reported:

```text
'M3A.selectedNumerator_formula' depends on axioms:
[propext, Classical.choice, Quot.sound]

'M3A.selectedNumerator_ray_formula' depends on axioms:
[propext, Classical.choice, Quot.sound]

'M3A.cubicNumeratorCoeff_eq_zero_of_linear_quadratic_zero' depends on axioms:
[propext, Quot.sound]
```

These are standard Lean/Mathlib foundational axioms. The verified modules use
no `sorry`, `admit`, `unsafe`, or user-declared axiom.

## Gate status

- M0 model lock: **complete**.
- M1 signed involutions and baseline darkness: **complete**.
- M2 exact selected numerator: **complete**.
- Next dependency node: M3, the dark-plane decomposition and persistent plane
  certificates.
