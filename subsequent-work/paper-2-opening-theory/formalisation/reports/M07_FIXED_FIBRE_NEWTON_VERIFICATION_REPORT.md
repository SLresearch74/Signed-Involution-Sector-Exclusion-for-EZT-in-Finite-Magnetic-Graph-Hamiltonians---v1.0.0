# M7 fixed-fibre Newton verification report

Date: 9 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Genuine Newton-polyhedron definition

M7 defines the coordinatewise real upper orthant based at a natural
bidegree and the literal union of quadrant translates over the actual M6
coefficient support. The Newton polyhedron is then defined as the Mathlib
real convex hull:

```lean
def newtonPolyhedron (S : Set (Nat × Nat)) : Set (ℝ × ℝ) :=
  convexHull ℝ (supportPlusQuadrant S)
```

Thus the theorem concerns the paper's unbounded real Newton polyhedron, not
only a discrete exponent set or a set of candidate words. Since M6 support is
defined by nonzero amplitude coefficients, all coefficient cancellation has
already been accounted for.

The declared zero-germ convention is formalised explicitly:

```lean
newtonPolyhedron (∅ : Set (Nat × Nat)) = ∅
```

## General one-vertex orthant lemma

Lean proves `newton_eq_orthant_of_vertex`: if a support `S` contains `u` and
is contained in the natural upper orthant based at `u`, then

```text
newtonPolyhedron S = realUpperOrthant u.
```

The proof establishes that support plus the nonnegative quadrant is already
the entire real upper orthant. Mathlib verifies that this product of two
closed upper rays is convex, so taking its real convex hull changes nothing.
Both set inclusions are therefore explicit.

## Fixed-fibre Newton trichotomy

The principal theorem `fixedFibre_newton` applies the general lemma to M6's
actual support certificates and proves, for every fixed complex direction
`v`:

```text
L(v) ≠ 0                 : (1,3) + ℝ≥0²
L(v) = 0 and Q(v) ≠ 0    : (2,4) + ℝ≥0²
L(v) = Q(v) = 0          : ∅
```

The complex-direction statement contains the paper's real fixed fibres by
scalar inclusion. No direction depends on the perturbation parameter.

## Positive-weight exposed vertices

M7 isolates the paper's weight

```lean
exponentWeight a b (p,q) = b*p + a*q
```

and defines the exposed support face as the set of actual support exponents
minimising that weight.

The general theorem `positiveWeight_unique_vertex` proves that if `a>0` and
`b>0`, the weight increases strictly from the lower vertex to every other
support point in its upper orthant. Consequently,
`positiveWeight_exposedFace_eq_singleton` proves that the minimiser face is
exactly the singleton vertex.

The exhaustive theorem `fixedFibre_positiveWeight_faces` therefore gives:

```text
generic fibre              : {(1,3)}
protected non-dark fibre   : {(2,4)}
exact-dark fibre           : ∅
```

for every strictly positive weight.

## Scope

This milestone is the fixed-fibre theorem only. It does not assert moving-ray
uniformity, monomial-pullback behaviour, face collisions, or a universal
Newton atlas. The analytic identification of the formal amplitude
coefficients with Taylor coefficients of the matrix exponential remains the
separately planned M8 analytic bridge. Accordingly, M7 uses amplitude support
directly and introduces no unshifted-resolvent surrogate.

## Build and axiom report

The module-level build completed successfully with 8665 jobs. After importing
M7 from the root library, the complete `lake build` completed successfully
with 8668 jobs.

Lean reported for all principal M7 theorems:

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
- M7 fixed-fibre Newton polyhedra and positive-weight uniqueness: **complete**.
- Requested exact finite-algebra spine through the fixed-fibre theorem:
  **complete**.
- Optional next dependency node: M8, the analytic matrix-exponential bridge.
