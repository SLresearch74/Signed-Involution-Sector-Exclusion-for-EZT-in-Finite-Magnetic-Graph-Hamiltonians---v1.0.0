import M3A.FixedRayTrichotomy

namespace M3A

/-- The coordinatewise real upper orthant based at a natural bidegree. -/
def realUpperOrthant (u : Nat × Nat) : Set (ℝ × ℝ) :=
  Set.Ici (u.1 : ℝ) ×ˢ Set.Ici (u.2 : ℝ)

/-- The union of the real nonnegative quadrant translated by every actual
support exponent. -/
def supportPlusQuadrant (S : Set (Nat × Nat)) : Set (ℝ × ℝ) :=
  {x | ∃ u ∈ S, x ∈ realUpperOrthant u}

/-- The Newton polyhedron is the real convex hull of actual support plus the
nonnegative quadrant. The empty-support convention therefore gives `∅`. -/
def newtonPolyhedron (S : Set (Nat × Nat)) : Set (ℝ × ℝ) :=
  convexHull ℝ (supportPlusQuadrant S)

theorem realUpperOrthant_convex (u : Nat × Nat) :
    Convex ℝ (realUpperOrthant u) := by
  simpa [realUpperOrthant] using
    (convex_Ici (u.1 : ℝ)).prod (convex_Ici (u.2 : ℝ))

/-- If the actual support contains `u` and is contained in its natural upper
orthant, then support plus the quadrant is already the real upper orthant. -/
theorem supportPlusQuadrant_eq_realUpperOrthant_of_vertex
    (S : Set (Nat × Nat)) (u : Nat × Nat)
    (hu : u ∈ S) (hS : S ⊆ natUpperOrthant u) :
    supportPlusQuadrant S = realUpperOrthant u := by
  apply Set.Subset.antisymm
  · rintro x ⟨w, hwS, hxw⟩
    have huw := hS hwS
    change u.1 ≤ w.1 ∧ u.2 ≤ w.2 at huw
    change (w.1 : ℝ) ≤ x.1 ∧ (w.2 : ℝ) ≤ x.2 at hxw
    change (u.1 : ℝ) ≤ x.1 ∧ (u.2 : ℝ) ≤ x.2
    have huw1 : (u.1 : ℝ) ≤ (w.1 : ℝ) := by exact_mod_cast huw.1
    have huw2 : (u.2 : ℝ) ≤ (w.2 : ℝ) := by exact_mod_cast huw.2
    exact ⟨huw1.trans hxw.1, huw2.trans hxw.2⟩
  · intro x hxu
    exact ⟨u, hu, hxu⟩

/-- The general one-vertex Newton lemma. Both inclusions are exact: support
containment gives one direction, while the present vertex supplies the whole
translated quadrant in the other. -/
theorem newton_eq_orthant_of_vertex
    (S : Set (Nat × Nat)) (u : Nat × Nat)
    (hu : u ∈ S) (hS : S ⊆ natUpperOrthant u) :
    newtonPolyhedron S = realUpperOrthant u := by
  rw [newtonPolyhedron,
    supportPlusQuadrant_eq_realUpperOrthant_of_vertex S u hu hS]
  exact (realUpperOrthant_convex u).convexHull_eq

@[simp]
theorem supportPlusQuadrant_empty :
    supportPlusQuadrant (∅ : Set (Nat × Nat)) = ∅ := by
  ext x
  simp [supportPlusQuadrant]

@[simp]
theorem newtonPolyhedron_empty :
    newtonPolyhedron (∅ : Set (Nat × Nat)) = ∅ := by
  simp [newtonPolyhedron]

/-- The M6 support certificates assembled into the exact conditional support
shape used by the Newton theorem. -/
theorem fixedFibre_support_shape (v : Internal → ℂ) :
    if linearCoeff v ≠ 0 then
      (1, 3) ∈ coefficientSupport v ∧
        coefficientSupport v ⊆ natUpperOrthant (1, 3)
    else if quadraticCoeff v ≠ 0 then
      (2, 4) ∈ coefficientSupport v ∧
        coefficientSupport v ⊆ natUpperOrthant (2, 4)
    else
      coefficientSupport v = ∅ := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · rw [if_pos hL]
    let hD := linearRayData_of_linear_ne v hL
    exact ⟨hD.leading_mem, hD.support_subset⟩
  · rw [if_neg hL]
    have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · rw [if_pos hQ]
      let hD := quadraticRayData_of_linear_zero_quadratic_ne v hL0 hQ
      exact ⟨hD.leading_mem, hD.support_subset⟩
    · rw [if_neg hQ]
      exact (darkRayData_of_linear_quadratic_zero v hL0
        (not_ne_iff.mp hQ)).support_empty

/-- The fixed-fibre Newton polyhedron is one of the two declared real upper
orthants, or empty for the exact-dark fibre. -/
theorem fixedFibre_newton (v : Internal → ℂ) :
    newtonPolyhedron (coefficientSupport v) =
      if linearCoeff v ≠ 0 then realUpperOrthant (1, 3)
      else if quadraticCoeff v ≠ 0 then realUpperOrthant (2, 4)
      else ∅ := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · rw [if_pos hL]
    let hD := linearRayData_of_linear_ne v hL
    exact newton_eq_orthant_of_vertex (coefficientSupport v) (1, 3)
      hD.leading_mem hD.support_subset
  · rw [if_neg hL]
    have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · rw [if_pos hQ]
      let hD := quadraticRayData_of_linear_zero_quadratic_ne v hL0 hQ
      exact newton_eq_orthant_of_vertex (coefficientSupport v) (2, 4)
        hD.leading_mem hD.support_subset
    · rw [if_neg hQ]
      rw [(darkRayData_of_linear_quadratic_zero v hL0
        (not_ne_iff.mp hQ)).support_empty]
      exact newtonPolyhedron_empty

/-- The paper's positive weight `b*p + a*q`, isolated from coercion details. -/
def exponentWeight (a b : ℝ) (u : Nat × Nat) : ℝ :=
  b * (u.1 : ℝ) + a * (u.2 : ℝ)

/-- A support exponent lies in the exposed support face when it minimizes the
declared weight over the actual support. -/
def exposedSupportFace
    (S : Set (Nat × Nat)) (a b : ℝ) : Set (Nat × Nat) :=
  {u | u ∈ S ∧ ∀ w ∈ S, exponentWeight a b u ≤ exponentWeight a b w}

/-- Every strictly positive weight increases strictly away from the vertex of
a natural upper orthant. -/
theorem positiveWeight_unique_vertex
    (S : Set (Nat × Nat)) (u : Nat × Nat)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hS : S ⊆ natUpperOrthant u) :
    ∀ w ∈ S, w ≠ u →
      exponentWeight a b u < exponentWeight a b w := by
  intro w hw hwu
  have huw := hS hw
  change u.1 ≤ w.1 ∧ u.2 ≤ w.2 at huw
  by_cases hfirst : u.1 = w.1
  · have hsecond_ne : u.2 ≠ w.2 := by
      intro hsecond
      apply hwu
      exact Prod.ext hfirst.symm hsecond.symm
    have hsecond : u.2 < w.2 := lt_of_le_of_ne huw.2 hsecond_ne
    have hfirstR : (u.1 : ℝ) = (w.1 : ℝ) := by exact_mod_cast hfirst
    have hsecondR : (u.2 : ℝ) < (w.2 : ℝ) := by exact_mod_cast hsecond
    unfold exponentWeight
    rw [hfirstR]
    have hweighted := mul_lt_mul_of_pos_left hsecondR ha
    linarith
  · have hfirst_lt : u.1 < w.1 := lt_of_le_of_ne huw.1 hfirst
    have hfirstR : (u.1 : ℝ) < (w.1 : ℝ) := by exact_mod_cast hfirst_lt
    have hsecondR : (u.2 : ℝ) ≤ (w.2 : ℝ) := by exact_mod_cast huw.2
    unfold exponentWeight
    exact add_lt_add_of_lt_of_le
      (mul_lt_mul_of_pos_left hfirstR hb)
      (mul_le_mul_of_nonneg_left hsecondR ha.le)

/-- Under the one-vertex support hypotheses, every positive weight exposes
exactly that vertex. -/
theorem positiveWeight_exposedFace_eq_singleton
    (S : Set (Nat × Nat)) (u : Nat × Nat)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b)
    (hu : u ∈ S) (hS : S ⊆ natUpperOrthant u) :
    exposedSupportFace S a b = {u} := by
  ext w
  constructor
  · intro hw
    rcases hw with ⟨hwS, hwmin⟩
    have hwu : w = u := by
      by_contra hne
      have hlt := positiveWeight_unique_vertex S u ha hb hS w hwS hne
      exact (not_lt_of_ge (hwmin u hu)) hlt
    simp [hwu]
  · intro hw
    have hwu : w = u := by simpa using hw
    subst w
    refine ⟨hu, ?_⟩
    intro z hz
    by_cases hzu : z = u
    · simp [hzu]
    · exact (positiveWeight_unique_vertex S u ha hb hS z hz hzu).le

theorem linearBranch_positiveWeight_face
    (v : Internal → ℂ) (hL : linearCoeff v ≠ 0)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    exposedSupportFace (coefficientSupport v) a b = {(1, 3)} := by
  let hD := linearRayData_of_linear_ne v hL
  exact positiveWeight_exposedFace_eq_singleton
    (coefficientSupport v) (1, 3) ha hb hD.leading_mem hD.support_subset

theorem quadraticBranch_positiveWeight_face
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v ≠ 0)
    {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    exposedSupportFace (coefficientSupport v) a b = {(2, 4)} := by
  let hD := quadraticRayData_of_linear_zero_quadratic_ne v hL hQ
  exact positiveWeight_exposedFace_eq_singleton
    (coefficientSupport v) (2, 4) ha hb hD.leading_mem hD.support_subset

/-- The positive-weight exposed face follows the same exhaustive fixed-fibre
trichotomy; in the dark branch it is empty by convention. -/
theorem fixedFibre_positiveWeight_faces
    (v : Internal → ℂ) {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    exposedSupportFace (coefficientSupport v) a b =
      if linearCoeff v ≠ 0 then {(1, 3)}
      else if quadraticCoeff v ≠ 0 then {(2, 4)}
      else ∅ := by
  classical
  by_cases hL : linearCoeff v ≠ 0
  · rw [if_pos hL]
    exact linearBranch_positiveWeight_face v hL ha hb
  · rw [if_neg hL]
    have hL0 : linearCoeff v = 0 := not_ne_iff.mp hL
    by_cases hQ : quadraticCoeff v ≠ 0
    · rw [if_pos hQ]
      exact quadraticBranch_positiveWeight_face v hL0 hQ ha hb
    · rw [if_neg hQ]
      rw [(darkRayData_of_linear_quadratic_zero v hL0
        (not_ne_iff.mp hQ)).support_empty]
      simp [exposedSupportFace]

#print axioms newton_eq_orthant_of_vertex
#print axioms fixedFibre_newton
#print axioms positiveWeight_unique_vertex
#print axioms fixedFibre_positiveWeight_faces

end M3A
