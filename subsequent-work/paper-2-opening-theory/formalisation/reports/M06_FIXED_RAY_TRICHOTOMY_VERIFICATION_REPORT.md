# M6 fixed-ray trichotomy verification report

Date: 9 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Actual coefficient support

The module works with the literal bidegree support of the selected amplitude:

```lean
def coefficientSupport (v : Internal → ℂ) : Set (Nat × Nat) :=
  {u | amplitudeCoeff v u.1 u.2 ≠ 0}
```

It also defines the coordinatewise natural upper orthant. Consequently, the
branch theorems state both non-vanishing at the claimed Newton vertex and a
global support inclusion, rather than only naming an informal leading term.

## Generic linear branch

If `L(v) ≠ 0`, Lean constructs `LinearRayData v` and proves:

- the vertex `(1,3)` belongs to the coefficient support;
- its exact value is `i L(v) / 6`;
- every supported bidegree `(p,q)` satisfies `p ≥ 1` and `q ≥ 3`.

The support inclusion combines M1 baseline darkness with M4's endpoint-word
barrier. Non-vanishing at `(1,3)` follows from M5's exact coefficient formula.

## Protected quadratic branch

If `L(v) = 0` and `Q(v) ≠ 0`, Lean constructs `QuadraticRayData v` and proves:

- the vertex `(2,4)` belongs to the coefficient support;
- its exact value is `Q(v) / 12`;
- every supported bidegree `(p,q)` satisfies `p ≥ 2` and `q ≥ 4`.

The stronger lower bound uses M5's theorem that the complete perturbation-
degree-one coefficient sequence vanishes on `L=0`, not merely the endpoint
coefficient.

## Dark branch and exclusion of a cubic branch

If `L(v) = Q(v) = 0`, M3's plane decomposition places the direction on one of
the two exact dark planes. M5's signed-symmetry word certificates then show
that every amplitude coefficient vanishes. Lean therefore proves:

```lean
coefficientSupport v = ∅
```

This is strictly stronger than vanishing of a proposed cubic coefficient: it
rules out any residual cubic or higher fixed-ray branch.

## Exhaustive deterministic classification

`RayBranch` has exactly three constructors: `linear`, `quadratic`, and `dark`.
The noncomputable classifier first tests `L` and then `Q`. Lean proves the
three exact characterisations:

```text
classifyRay v = linear    ↔ L(v) ≠ 0
classifyRay v = quadratic ↔ L(v) = 0 ∧ Q(v) ≠ 0
classifyRay v = dark      ↔ L(v) = 0 ∧ Q(v) = 0
```

`fixedRay_trichotomy` proves exhaustivity at the certificate level, while
`classifyRay_spec` returns the complete support certificate appropriate to
the unique classified branch. The formal statement is over complex
directions and therefore contains the paper's real-direction case.

## Build and axiom report

The module-level build completed successfully with 8664 jobs. After importing
M6 from the root library, the complete `lake build` completed successfully
with 8667 jobs.

Lean reported for the principal M6 theorems:

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
- M6 exhaustive fixed-ray trichotomy: **complete**.
- Next dependency node: M7, the fixed-fibre Newton theorem.
