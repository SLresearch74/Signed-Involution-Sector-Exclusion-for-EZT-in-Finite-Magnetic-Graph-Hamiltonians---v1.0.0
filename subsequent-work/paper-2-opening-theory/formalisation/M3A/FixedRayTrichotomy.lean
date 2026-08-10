import M3A.RayCoefficients

namespace M3A

/-- The actual bidegree support of the selected fixed-ray amplitude. -/
def coefficientSupport (v : Internal → ℂ) : Set (Nat × Nat) :=
  {u | amplitudeCoeff v u.1 u.2 ≠ 0}

/-- The coordinatewise upper orthant based at a bidegree. -/
def natUpperOrthant (u : Nat × Nat) : Set (Nat × Nat) :=
  {w | u.1 ≤ w.1 ∧ u.2 ≤ w.2}

/-- The three exhaustive fixed-ray behaviours. -/
inductive RayBranch
  | linear
  | quadratic
  | dark
  deriving DecidableEq, Repr

/-- The fixed-ray classifier is determined by the first two scalar
obstructions. -/
noncomputable def classifyRay (v : Internal → ℂ) : RayBranch :=
  if linearCoeff v ≠ 0 then .linear
  else if quadraticCoeff v ≠ 0 then .quadratic
  else .dark

/-- Certificate for the generic fixed-ray branch. -/
structure LinearRayData (v : Internal → ℂ) : Prop where
  linear_ne : linearCoeff v ≠ 0
  leading_value : amplitudeCoeff v 1 3 = Complex.I * linearCoeff v / 6
  leading_mem : (1, 3) ∈ coefficientSupport v
  support_subset : coefficientSupport v ⊆ natUpperOrthant (1, 3)

/-- Certificate for the first-order-protected quadratic branch. -/
structure QuadraticRayData (v : Internal → ℂ) : Prop where
  linear_zero : linearCoeff v = 0
  quadratic_ne : quadraticCoeff v ≠ 0
  leading_value : amplitudeCoeff v 2 4 = quadraticCoeff v / 12
  leading_mem : (2, 4) ∈ coefficientSupport v
  support_subset : coefficientSupport v ⊆ natUpperOrthant (2, 4)

/-- Certificate for an identically dark fixed ray. -/
structure DarkRayData (v : Internal → ℂ) : Prop where
  linear_zero : linearCoeff v = 0
  quadratic_zero : quadraticCoeff v = 0
  support_empty : coefficientSupport v = ∅

/-- If both scalar obstructions vanish, every amplitude coefficient vanishes. -/
theorem amplitudeCoeff_eq_zero_of_linear_quadratic_zero
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0)
    (p q : Nat) :
    amplitudeCoeff v p q = 0 := by
  rcases (ell_quad_zero_iff_planes v).mp ⟨hL, hQ⟩ with hA | hB
  · simp [amplitudeCoeff, rayMomentCoeff_eq_zero_of_planeA v hA p q]
  · simp [amplitudeCoeff, rayMomentCoeff_eq_zero_of_planeB v hB p q]

/-- A nonzero linear obstruction gives the exact `(1,3)` vertex and confines
the remaining support to its upper orthant. -/
theorem linearRayData_of_linear_ne
    (v : Internal → ℂ) (hL : linearCoeff v ≠ 0) :
    LinearRayData v := by
  refine {
    linear_ne := hL
    leading_value := amplitudeCoeff_one_three v
    leading_mem := ?_
    support_subset := ?_
  }
  · change amplitudeCoeff v 1 3 ≠ 0
    rw [amplitudeCoeff_one_three]
    exact div_ne_zero (mul_ne_zero (by norm_num) hL) (by norm_num)
  · intro w hw
    change amplitudeCoeff v w.1 w.2 ≠ 0 at hw
    change 1 ≤ w.1 ∧ 3 ≤ w.2
    have hp0 : w.1 ≠ 0 := by
      intro hp
      apply hw
      simpa [hp] using amplitudeCoeff_zero_degree v w.2
    have hp : 0 < w.1 := Nat.pos_of_ne_zero hp0
    have hq : w.1 + 2 ≤ w.2 := by
      by_contra hn
      have hlt : w.2 < w.1 + 2 := by omega
      exact hw (amplitudeCoeff_eq_zero_of_lt_endpoint v hp hlt)
    omega

/-- On `L=0`, a nonzero quadratic obstruction gives the exact `(2,4)`
vertex and complete first-order vanishing. -/
theorem quadraticRayData_of_linear_zero_quadratic_ne
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v ≠ 0) :
    QuadraticRayData v := by
  refine {
    linear_zero := hL
    quadratic_ne := hQ
    leading_value := amplitudeCoeff_two_four_of_linear_zero v hL
    leading_mem := ?_
    support_subset := ?_
  }
  · change amplitudeCoeff v 2 4 ≠ 0
    rw [amplitudeCoeff_two_four_of_linear_zero v hL]
    exact div_ne_zero hQ (by norm_num)
  · intro w hw
    change amplitudeCoeff v w.1 w.2 ≠ 0 at hw
    change 2 ≤ w.1 ∧ 4 ≤ w.2
    have hp0 : w.1 ≠ 0 := by
      intro hp
      apply hw
      simpa [hp] using amplitudeCoeff_zero_degree v w.2
    have hp1 : w.1 ≠ 1 := by
      intro hp
      apply hw
      simpa [hp] using amplitudeCoeff_one_eq_zero_of_linear_zero v hL w.2
    have hp : 0 < w.1 := Nat.pos_of_ne_zero hp0
    have hq : w.1 + 2 ≤ w.2 := by
      by_contra hn
      have hlt : w.2 < w.1 + 2 := by omega
      exact hw (amplitudeCoeff_eq_zero_of_lt_endpoint v hp hlt)
    omega

/-- Vanishing of both obstructions makes the entire fixed-ray support empty. -/
theorem darkRayData_of_linear_quadratic_zero
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0) :
    DarkRayData v := by
  refine {
    linear_zero := hL
    quadratic_zero := hQ
    support_empty := ?_
  }
  ext w
  constructor
  · intro hw
    change amplitudeCoeff v w.1 w.2 ≠ 0 at hw
    exact (hw
      (amplitudeCoeff_eq_zero_of_linear_quadratic_zero v hL hQ w.1 w.2)).elim
  · simp

theorem classifyRay_eq_linear_iff (v : Internal → ℂ) :
    classifyRay v = .linear ↔ linearCoeff v ≠ 0 := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · simp [classifyRay, hL]
  · by_cases hQ : quadraticCoeff v ≠ 0
    · simp [classifyRay, hL, hQ]
    · simp [classifyRay, hL, hQ]

theorem classifyRay_eq_quadratic_iff (v : Internal → ℂ) :
    classifyRay v = .quadratic ↔
      linearCoeff v = 0 ∧ quadraticCoeff v ≠ 0 := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · simp [classifyRay, hL]
  · have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · simp [classifyRay, hL0, hQ]
    · have hQ0 : quadraticCoeff v = 0 := not_ne_iff.mp hQ
      simp [classifyRay, hL0, hQ0]

theorem classifyRay_eq_dark_iff (v : Internal → ℂ) :
    classifyRay v = .dark ↔
      linearCoeff v = 0 ∧ quadraticCoeff v = 0 := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · simp [classifyRay, hL]
  · have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · simp [classifyRay, hL0, hQ]
    · have hQ0 : quadraticCoeff v = 0 := not_ne_iff.mp hQ
      simp [classifyRay, hL0, hQ0]

/-- Every fixed ray lies in exactly one of the linear, quadratic, or dark
branches, with the exact support certificate carried by that branch. -/
theorem fixedRay_trichotomy (v : Internal → ℂ) :
    LinearRayData v ∨ QuadraticRayData v ∨ DarkRayData v := by
  by_cases hL : linearCoeff v ≠ 0
  · exact Or.inl (linearRayData_of_linear_ne v hL)
  · have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · exact Or.inr (Or.inl
        (quadraticRayData_of_linear_zero_quadratic_ne v hL0 hQ))
    · exact Or.inr (Or.inr
        (darkRayData_of_linear_quadratic_zero v hL0 (not_ne_iff.mp hQ)))

/-- The deterministic classifier returns the certificate appropriate to its
branch. -/
theorem classifyRay_spec (v : Internal → ℂ) :
    match classifyRay v with
    | .linear => LinearRayData v
    | .quadratic => QuadraticRayData v
    | .dark => DarkRayData v := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · simpa [classifyRay, hL] using linearRayData_of_linear_ne v hL
  · have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · simpa [classifyRay, hL, hQ] using
        quadraticRayData_of_linear_zero_quadratic_ne v hL0 hQ
    · simpa [classifyRay, hL, hQ] using
        darkRayData_of_linear_quadratic_zero v hL0 (not_ne_iff.mp hQ)

/-- There is no residual cubic branch after `L=Q=0`: the entire coefficient
support is empty. -/
theorem no_cubic_fixedRay_branch
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0) :
    coefficientSupport v = ∅ :=
  (darkRayData_of_linear_quadratic_zero v hL hQ).support_empty

#print axioms fixedRay_trichotomy
#print axioms classifyRay_spec
#print axioms no_cubic_fixedRay_branch

end M3A
