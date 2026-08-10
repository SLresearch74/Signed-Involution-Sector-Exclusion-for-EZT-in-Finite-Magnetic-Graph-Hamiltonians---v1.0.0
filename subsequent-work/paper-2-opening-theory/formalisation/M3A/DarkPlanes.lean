import M3A.SelectedNumerator
import M3A.SignedInvolution

namespace M3A

/-- The original exact-dark plane `d₁=d₂`, `d₃=d₄`. -/
def OnPlaneA {K : Type*} (v : Internal → K) : Prop :=
  v 0 = v 1 ∧ v 2 = v 3

/-- The alternative exact-dark plane `d₁=d₄`, `d₃=d₂`. -/
def OnPlaneB {K : Type*} (v : Internal → K) : Prop :=
  v 0 = v 3 ∧ v 2 = v 1

/-- The scalar line on which the two dark planes meet. -/
def OnScalarLine {K : Type*} (v : Internal → K) : Prop :=
  v 0 = v 1 ∧ v 1 = v 2 ∧ v 2 = v 3

/-- The pointwise dark-locus decomposition. This is proved over integral
domains, a stronger setting than the characteristic-not-two field statement
needed by the manuscript. -/
theorem ell_quad_zero_iff_planes
    {K : Type*} [CommRing K] [IsDomain K] (v : Internal → K) :
    linearCoeff v = 0 ∧ quadraticCoeff v = 0 ↔
      OnPlaneA v ∨ OnPlaneB v := by
  constructor
  · rintro ⟨hL, hQ⟩
    have hL' : v 0 - v 1 + v 2 - v 3 = 0 := by
      simpa [linearCoeff, ell] using hL
    have hfactor : (v 1 - v 2) * (v 3 - v 2) = 0 := by
      calc
        (v 1 - v 2) * (v 3 - v 2) =
            quadraticCoeff v + v 2 * linearCoeff v := by
              simp [linearCoeff, quadraticCoeff, ell, quad]
              ring
        _ = 0 := by rw [hL, hQ]; ring
    rcases mul_eq_zero.mp hfactor with hb | hd
    · right
      constructor
      · have had : v 0 - v 3 = 0 := by
          linear_combination hL' + hb
        exact sub_eq_zero.mp had
      · exact (sub_eq_zero.mp hb).symm
    · left
      constructor
      · have hab : v 0 - v 1 = 0 := by
          linear_combination hL' + hd
        exact sub_eq_zero.mp hab
      · exact (sub_eq_zero.mp hd).symm
  · rintro (hA | hB)
    · rcases hA with ⟨h01, h23⟩
      constructor
      · simp [linearCoeff, ell, h01, h23]
      · simp [quadraticCoeff, quad, h01, h23]
    · rcases hB with ⟨h03, h21⟩
      constructor
      · simp [linearCoeff, ell, h03, h21]
      · simp [quadraticCoeff, quad, h03, h21, mul_comm]

/-- The two plane predicates meet exactly on the scalar line. -/
theorem onPlaneA_and_onPlaneB_iff_scalarLine
    {K : Type*} (v : Internal → K) :
    OnPlaneA v ∧ OnPlaneB v ↔ OnScalarLine v := by
  constructor
  · rintro ⟨⟨h01, h23⟩, ⟨_, h21⟩⟩
    exact ⟨h01, h21.symm, h23⟩
  · rintro ⟨h01, h12, h23⟩
    constructor
    · exact ⟨h01, h23⟩
    · exact ⟨h01.trans (h12.trans h23), h12.symm⟩

/-- The original signed involution persists on plane A. -/
theorem rOrig_commutes_hamiltonian_of_planeA
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneA v) :
    Commute (rOrig : Matrix State State K) (hamiltonian v) := by
  rcases h with ⟨h01, h23⟩
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rOrig, hamiltonian, H0, diagonalPerturbation, Matrix.mul_apply,
      Fin.sum_univ_succ, h01, h23]

/-- The alternative signed involution persists on plane B. -/
theorem rAlt_commutes_hamiltonian_of_planeB
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneB v) :
    Commute (rAlt : Matrix State State K) (hamiltonian v) := by
  rcases h with ⟨h03, h21⟩
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rAlt, hamiltonian, H0, diagonalPerturbation, Matrix.mul_apply,
      Fin.sum_univ_succ, h03, h21]

theorem rOrig_certificate_of_planeA
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneA v) :
    SignedCertificate (hamiltonian v) (rOrig : Matrix State State K) where
  involutive := rOrig_involutive
  commutes := rOrig_commutes_hamiltonian_of_planeA v h
  source_even := rOrig_source_even
  target_odd := rOrig_target_odd

theorem rAlt_certificate_of_planeB
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneB v) :
    SignedCertificate (hamiltonian v) (rAlt : Matrix State State K) where
  involutive := rAlt_involutive
  commutes := rAlt_commutes_hamiltonian_of_planeB v h
  source_even := rAlt_source_even
  target_odd := rAlt_target_odd

/-- Every selected moment vanishes on the original plane. -/
theorem planeA_moments_dark
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (h : OnPlaneA v) (k : Nat) :
    selectedMoment (hamiltonian v) k = 0 :=
  selectedMoment_eq_zero_of_signedCertificate (by norm_num)
    (rOrig_certificate_of_planeA v h) k

/-- Every selected moment vanishes on the alternative plane. -/
theorem planeB_moments_dark
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (h : OnPlaneB v) (k : Nat) :
    selectedMoment (hamiltonian v) k = 0 :=
  selectedMoment_eq_zero_of_signedCertificate (by norm_num)
    (rAlt_certificate_of_planeB v h) k

/-- The algebraic dark-locus equations imply exact all-depth moment darkness. -/
theorem moments_dark_of_linear_quadratic_zero
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (hL : linearCoeff v = 0)
    (hQ : quadraticCoeff v = 0) (k : Nat) :
    selectedMoment (hamiltonian v) k = 0 := by
  rcases (ell_quad_zero_iff_planes v).mp ⟨hL, hQ⟩ with hA | hB
  · exact planeA_moments_dark v hA k
  · exact planeB_moments_dark v hB k

/-- The same coefficient equations annihilate the unreduced selected
numerator at every spectral parameter. -/
theorem selectedNumerator_eq_zero_of_linear_quadratic_zero
    {K : Type*} [CommRing K] (z : K) (v : Internal → K)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0) :
    selectedNumerator z v = 0 := by
  rw [selectedNumerator_formula, hL, hQ,
    cubicNumeratorCoeff_eq_zero_of_linear_quadratic_zero v hL hQ]
  ring

#print axioms ell_quad_zero_iff_planes
#print axioms rOrig_commutes_hamiltonian_of_planeA
#print axioms rAlt_commutes_hamiltonian_of_planeB
#print axioms planeA_moments_dark
#print axioms planeB_moments_dark
#print axioms moments_dark_of_linear_quadratic_zero

end M3A
