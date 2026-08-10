# M5 ray-coefficient verification report

Date: 4 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Formal amplitude coefficients

The module defines the exact formal bidegree coefficient

```lean
amplitudeCoeff v p q = ((-i)^q / q!) * rayMomentCoeff v p q.
```

This already includes the amplitude normalisation. Identification with the
analytic matrix exponential remains the separately planned analytic bridge.

Lean verifies that every perturbation-degree-zero coefficient vanishes by M1
baseline darkness, and that positive-degree coefficients inherit M4's
endpoint support barrier.

## First surviving coefficients

Lean proves over complex directions:

```text
amplitudeCoeff v 1 3 = i L(v) / 6
```

and, under `L(v)=0`,

```text
amplitudeCoeff v 2 4 = Q(v) / 12.
```

The result over complex directions contains the paper's real-direction case
by scalar inclusion.

## Complete first-order vanishing

The principal bridge theorem is:

```lean
theorem amplitudeCoeff_one_eq_zero_of_linear_zero
    (v : Internal → ℂ) (hL : linearCoeff v = 0) (q : Nat) :
    amplitudeCoeff v 1 q = 0
```

Thus `L=0` removes the complete first-order sequence, not only the `(1,3)`
boundary coefficient.

The Lean proof is purely finite algebra:

1. every word coefficient is dark on plane A via `rOrig`;
2. every word coefficient is dark on plane B via `rAlt`;
3. perturbation-degree-one coefficients are additive in the direction;
4. every `L=0` direction decomposes, without division, as
   `(d₂,d₂,d₃,d₃) + (d₁-d₂,0,0,d₁-d₂)`, one vector on each plane.

This supplies the same bridge obligation as the transformed-resolvent route
while reusing the already verified signed certificates.

## Build and axiom report

After replacing an oversized normalization proof with a compact distributive
proof, `lake build` completed successfully with 8666 jobs. Lean reported for
all principal M5 theorems:

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Lean/Mathlib foundational axioms. The module uses no
`sorry`, `admit`, `unsafe`, or user-declared axiom.

## Gate status

- M0 model lock: **complete**.
- M1 signed involutions and baseline darkness: **complete**.
- M2 exact selected numerator: **complete**.
- M3 dark-plane decomposition and certificates: **complete**.
- M4 locked endpoint-word support: **complete**.
- M5 formal ray/amplitude coefficients: **complete**.
- Next dependency node: M6, the exhaustive fixed-ray trichotomy.
