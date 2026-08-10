# M8 analytic-bridge verification report

Date: 9 August 2026  
Lean: 4.32.1  
Mathlib: v4.32.1  
Result: **PASS**

## Actual selected matrix exponential

M8 defines the paper's source-to-target amplitude directly from Mathlib's
matrix exponential:

```lean
selectedAmplitude d t =
  (exp ((-i*t) • hamiltonian d)) target source.
```

This is the actual complex matrix exponential of the locked six-state
Hamiltonian, not a newly declared formal series.

## Global time-Taylor bridge

Mathlib proves global summability of the exponential series in the complete
normed matrix algebra. M8 maps that convergent matrix series through the
continuous linear functional selecting the `(target,source)` entry and proves:

```text
selectedAmplitude d t
  = Σ_q [(-i)^q/q!] selectedMoment (hamiltonian d) q · t^q.
```

The theorem is stated as `HasSum`, so convergence and the value of the sum are
both part of the Lean result. The phase and factorial normalization are proved
term by term.

## Finite perturbation polynomial at each time depth

M8 proves that diagonal perturbation is linear along a complex ray and defines
the finite evaluation of the exact M4 word coefficients. The recurrence
theorem and induction on the matrix-power depth establish:

```text
Σ_{p=0}^q ε^p rayCoeffMatrix(v,q,p)
  = hamiltonian(εv)^q.
```

Taking the selected matrix entry yields the exact fixed-depth moment identity:

```text
selectedMoment (hamiltonian(εv)) q
  = Σ_{p=0}^q rayMomentCoeff(v,p,q) ε^p.
```

This independently verifies that the recursively defined word coefficients
are the genuine perturbation coefficients of each Hamiltonian moment.

## Complete amplitude-coefficient identification

Combining the globally convergent time series with the finite perturbation
polynomial gives the principal bridge theorem:

```text
selectedRayAmplitude v ε t
  = Σ'_q Σ_{p=0}^q amplitudeCoeff(v,p,q) ε^p t^q.
```

Lean proves both the convergent `HasSum` form and the direct `tsum` equality.
Thus the coefficient array used in M5–M7 is exactly the Taylor coefficient
array of the selected matrix-exponential amplitude along every fixed complex
ray. The real-ray theorem is included by scalar restriction.

The triangular cutoff `p≤q` is exact: a length-`q` matrix word cannot contain
more than `q` perturbation letters.

## Analytic dark-ray corollary

M6 proves that every formal amplitude coefficient vanishes when `L=Q=0`.
Using the convergent M8 equality, Lean now proves the paper-facing statement:

```text
L(v)=Q(v)=0  ⟹  selectedRayAmplitude v ε t = 0
```

for every complex `ε` and `t`. Hence the absence of a cubic branch is not only
formal: the actual selected matrix-exponential amplitude is identically zero
along every exact-dark fixed ray.

## Build and axiom report

The module-level build completed successfully with 8666 jobs. After importing
M8 from the root library, the complete `lake build` completed successfully
with 8669 jobs.

Lean reported for all principal M8 theorems:

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
- M7 fixed-fibre Newton theorem: **complete**.
- M8 analytic matrix-exponential coefficient bridge: **complete**.
- Formal finite-algebra results and the paper-facing analytic amplitude are
  now connected end to end.
