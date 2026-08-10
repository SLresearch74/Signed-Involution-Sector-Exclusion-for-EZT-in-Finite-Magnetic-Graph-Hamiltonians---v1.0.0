# M4 endpoint-word verification report

Date: 4 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Exact word coefficients

`rayCoeffMatrix v k j` is defined by a finite recurrence. It is definitionally
the sum of all length-`k` noncommutative matrix words containing exactly `j`
copies of `D(v)`: each step prepends either `H0`, preserving degree, or `D(v)`,
increasing degree by one. `rayMomentCoeff` selects the target/source entry of
this complete coefficient sum.

This construction is exact finite algebra. It does not use a truncated
exponential, numerical sampling, or a candidate-word support surrogate.

## Support theorem

Lean verifies:

```lean
theorem sixState_support_bound
    {K : Type*} [CommRing K] (v : Internal → K)
    {j k : Nat} (hpos : 0 < j) (hk : k < j + 2) :
    rayMomentCoeff v j k = 0
```

The proof certifies the endpoint mechanism:

- degree greater than length gives the empty word sum;
- the all-perturbation word is killed at the source;
- with only one `H0`, the remaining word is killed at the target;
- therefore positive degree requires two unperturbed endpoint-access letters.

The baseline `j=0` layer remains separate and is governed by the already
verified `baseline_moments_dark` theorem.

## Boundary theorem

At `k=j+2`, Lean proves that the complete surviving coefficient is the single
boundary word

```text
H0 D(v)^j H0
```

and evaluates it exactly:

```lean
theorem sixState_boundary_ray ... :
    rayMomentCoeff v j (j + 2) =
      v 0 ^ j - v 1 ^ j + v 2 ^ j - v 3 ^ j
```

This is a coefficient-sum theorem, so cancellation is already accounted for.
It is stronger than merely proving that a boundary word exists.

Corollaries verify the `(1,3)` moment coefficient `L` and, on `L=0`, the
`(2,4)` moment coefficient `2Q`.

## Build and axiom report

`lake build` completed successfully with 8665 jobs. Each principal M4 theorem
depends only on:

```text
[propext, Classical.choice, Quot.sound]
```

These are standard Lean/Mathlib foundational axioms. The module uses no
`sorry`, `admit`, `unsafe`, or user-declared axiom.

## Scope boundary

M4 formalises the locked scalar-ray specialisation required by the downstream
trichotomy. The fully reusable labelled multi-index EA1 theorem—with arbitrary
ports, compatible endpoint pairs, and `ρ(γ)`—remains a later generalisation.
It is not required for M5–M7.

## Gate status

- M0 model lock: **complete**.
- M1 signed involutions and baseline darkness: **complete**.
- M2 exact selected numerator: **complete**.
- M3 dark-plane decomposition and certificates: **complete**.
- M4 locked endpoint-word support: **complete**.
- Next dependency node: M5, formal moment/amplitude coefficients and the first
  surviving bidegrees.
