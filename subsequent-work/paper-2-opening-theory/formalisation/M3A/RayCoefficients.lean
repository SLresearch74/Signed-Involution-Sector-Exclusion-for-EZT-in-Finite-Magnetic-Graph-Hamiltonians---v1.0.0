import M3A.EndpointWords
import M3A.BaselineDarkness

namespace M3A

/-- The exact formal coefficient of `ε^p t^q` in the selected amplitude. The
analytic identification with the matrix exponential is a later bridge; the
factor `(-i)^q/q!` is already included here. -/
noncomputable def amplitudeCoeff (v : Internal → ℂ) (p q : Nat) : ℂ :=
  ((-Complex.I) ^ q / (q.factorial : ℂ)) * rayMomentCoeff v p q

/-- Baseline darkness annihilates every degree-zero moment coefficient. -/
theorem rayMomentCoeff_zero_degree
    (v : Internal → ℂ) (k : Nat) :
    rayMomentCoeff v 0 k = 0 := by
  rw [rayMomentCoeff, rayCoeffMatrix_zero_degree]
  simpa [selectedMoment] using (baseline_moments_dark (K := ℂ) k)

theorem amplitudeCoeff_zero_degree
    (v : Internal → ℂ) (q : Nat) :
    amplitudeCoeff v 0 q = 0 := by
  simp [amplitudeCoeff, rayMomentCoeff_zero_degree]

/-- The endpoint support barrier passes from moment words to amplitude
coefficients. -/
theorem amplitudeCoeff_eq_zero_of_lt_endpoint
    (v : Internal → ℂ) {p q : Nat} (hpos : 0 < p) (hq : q < p + 2) :
    amplitudeCoeff v p q = 0 := by
  simp [amplitudeCoeff, sixState_support_bound v hpos hq]

/-- The generic first boundary coefficient is `iL/6`. -/
theorem amplitudeCoeff_one_three (v : Internal → ℂ) :
    amplitudeCoeff v 1 3 = Complex.I * linearCoeff v / 6 := by
  rw [amplitudeCoeff, rayMomentCoeff_one_three]
  norm_num [pow_succ, Complex.I_mul_I]
  ring

/-- On the first-order-protected hyperplane, the quadratic boundary
coefficient is `Q/12`. -/
theorem amplitudeCoeff_two_four_of_linear_zero
    (v : Internal → ℂ) (hL : linearCoeff v = 0) :
    amplitudeCoeff v 2 4 = quadraticCoeff v / 12 := by
  rw [amplitudeCoeff, rayMomentCoeff_two_four_of_linear_zero v hL]
  norm_num [pow_succ, Complex.I_mul_I]
  ring

theorem rOrig_commutes_diagonalPerturbation_of_planeA
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneA v) :
    Commute (rOrig : Matrix State State K) (diagonalPerturbation v) := by
  simpa [hamiltonian] using
    (rOrig_commutes_hamiltonian_of_planeA v h).sub_right
      (rOrig_commutes_H0 (K := K))

theorem rAlt_commutes_diagonalPerturbation_of_planeB
    {K : Type*} [CommRing K] (v : Internal → K) (h : OnPlaneB v) :
    Commute (rAlt : Matrix State State K) (diagonalPerturbation v) := by
  simpa [hamiltonian] using
    (rAlt_commutes_hamiltonian_of_planeB v h).sub_right
      (rAlt_commutes_H0 (K := K))

/-- If a signed symmetry commutes separately with `H0` and `D(v)`, it
commutes with every fixed-degree word coefficient. -/
theorem rayCoeffMatrix_commutes_of
    {K : Type*} [CommRing K] (v : Internal → K)
    (S : Matrix State State K)
    (hH : Commute S (H0 : Matrix State State K))
    (hD : Commute S (diagonalPerturbation v))
    (k j : Nat) : Commute S (rayCoeffMatrix v k j) := by
  induction k generalizing j with
  | zero =>
      cases j with
      | zero => simp [rayCoeffMatrix]
      | succ j => simp [rayCoeffMatrix]
  | succ k ih =>
      cases j with
      | zero =>
          rw [rayCoeffMatrix]
          exact hH.mul_right (ih 0)
      | succ j =>
          rw [rayCoeffMatrix]
          exact (hH.mul_right (ih (j + 1))).add_right
            (hD.mul_right (ih j))

/-- Every perturbation-degree coefficient is dark on plane A. -/
theorem rayMomentCoeff_eq_zero_of_planeA
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (h : OnPlaneA v) (j k : Nat) :
    rayMomentCoeff v j k = 0 := by
  have hcomm :
      Commute (rOrig : Matrix State State K) (rayCoeffMatrix v k j) :=
    rayCoeffMatrix_commutes_of v rOrig rOrig_commutes_H0
      (rOrig_commutes_diagonalPerturbation_of_planeA v h) k j
  let cert :
      SignedCertificate (rayCoeffMatrix v k j)
        (rOrig : Matrix State State K) := {
    involutive := rOrig_involutive
    commutes := hcomm
    source_even := rOrig_source_even
    target_odd := rOrig_target_odd
  }
  have hz := selectedMoment_eq_zero_of_signedCertificate (by norm_num) cert 1
  simpa [selectedMoment, rayMomentCoeff] using hz

/-- Every perturbation-degree coefficient is dark on plane B. -/
theorem rayMomentCoeff_eq_zero_of_planeB
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (h : OnPlaneB v) (j k : Nat) :
    rayMomentCoeff v j k = 0 := by
  have hcomm :
      Commute (rAlt : Matrix State State K) (rayCoeffMatrix v k j) :=
    rayCoeffMatrix_commutes_of v rAlt rAlt_commutes_H0
      (rAlt_commutes_diagonalPerturbation_of_planeB v h) k j
  let cert :
      SignedCertificate (rayCoeffMatrix v k j)
        (rAlt : Matrix State State K) := {
    involutive := rAlt_involutive
    commutes := hcomm
    source_even := rAlt_source_even
    target_odd := rAlt_target_odd
  }
  have hz := selectedMoment_eq_zero_of_signedCertificate (by norm_num) cert 1
  simpa [selectedMoment, rayMomentCoeff] using hz

theorem diagonalPerturbation_add
    {K : Type*} [CommRing K] (u v : Internal → K) :
    diagonalPerturbation (fun r => u r + v r) =
      diagonalPerturbation u + diagonalPerturbation v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagonalPerturbation]

/-- Degree-one word coefficients are additive in the declared direction. -/
theorem rayCoeffMatrix_one_add
    {K : Type*} [CommRing K] (u v : Internal → K) (k : Nat) :
    rayCoeffMatrix (fun r => u r + v r) k 1 =
      rayCoeffMatrix u k 1 + rayCoeffMatrix v k 1 := by
  induction k with
  | zero => simp [rayCoeffMatrix]
  | succ k ih =>
      change
        (H0 : Matrix State State K) *
              rayCoeffMatrix (fun r => u r + v r) k 1 +
            diagonalPerturbation (fun r => u r + v r) *
              rayCoeffMatrix (fun r => u r + v r) k 0 =
          ((H0 : Matrix State State K) * rayCoeffMatrix u k 1 +
              diagonalPerturbation u * rayCoeffMatrix u k 0) +
            ((H0 : Matrix State State K) * rayCoeffMatrix v k 1 +
              diagonalPerturbation v * rayCoeffMatrix v k 0)
      rw [ih, diagonalPerturbation_add,
        rayCoeffMatrix_zero_degree, rayCoeffMatrix_zero_degree,
        rayCoeffMatrix_zero_degree]
      simp only [mul_add, add_mul]
      abel

theorem rayMomentCoeff_one_add
    {K : Type*} [CommRing K] (u v : Internal → K) (k : Nat) :
    rayMomentCoeff (fun r => u r + v r) 1 k =
      rayMomentCoeff u 1 k + rayMomentCoeff v 1 k := by
  simp [rayMomentCoeff, rayCoeffMatrix_one_add]

/-- The plane-A component used to decompose the hyperplane `L=0`. -/
def planeAComponent {K : Type*} [Ring K] (v : Internal → K) : Internal → K :=
  ![v 1, v 1, v 2, v 2]

/-- The plane-B component used to decompose the hyperplane `L=0`. -/
def planeBComponent {K : Type*} [Ring K] (v : Internal → K) : Internal → K :=
  ![v 0 - v 1, 0, 0, v 0 - v 1]

theorem planeAComponent_onPlaneA
    {K : Type*} [Ring K] (v : Internal → K) :
    OnPlaneA (planeAComponent v) := by
  simp [OnPlaneA, planeAComponent]

theorem planeBComponent_onPlaneB
    {K : Type*} [Ring K] (v : Internal → K) :
    OnPlaneB (planeBComponent v) := by
  simp [OnPlaneB, planeBComponent]

/-- Every direction satisfying `L=0` is the sum of one plane-A direction and
one plane-B direction; no division is required. -/
theorem direction_eq_planeComponents_of_linear_zero
    {K : Type*} [CommRing K] (v : Internal → K)
    (hL : linearCoeff v = 0) :
    v = fun r => planeAComponent v r + planeBComponent v r := by
  have hL' : v 0 - v 1 + v 2 - v 3 = 0 := by
    simpa [linearCoeff, ell] using hL
  funext r
  fin_cases r
  · simp [planeAComponent, planeBComponent]
  · simp [planeAComponent, planeBComponent]
  · simp [planeAComponent, planeBComponent]
  · change v 3 = v 2 + (v 0 - v 1)
    linear_combination -hL'

/-- The complete first-order moment sequence vanishes on `L=0`, not merely
its endpoint-boundary coefficient. -/
theorem rayMomentCoeff_one_eq_zero_of_linear_zero
    {K : Type*} [Field K] [CharZero K]
    (v : Internal → K) (hL : linearCoeff v = 0) (k : Nat) :
    rayMomentCoeff v 1 k = 0 := by
  let u := planeAComponent v
  let w := planeBComponent v
  have hv : v = fun r => u r + w r := by
    simpa [u, w] using direction_eq_planeComponents_of_linear_zero v hL
  calc
    rayMomentCoeff v 1 k =
        rayMomentCoeff (fun r => u r + w r) 1 k := by rw [hv]
    _ = rayMomentCoeff u 1 k + rayMomentCoeff w 1 k :=
      rayMomentCoeff_one_add u w k
    _ = 0 := by
      rw [rayMomentCoeff_eq_zero_of_planeA u
          (by simpa [u] using planeAComponent_onPlaneA v) 1 k]
      rw [rayMomentCoeff_eq_zero_of_planeB w
          (by simpa [w] using planeBComponent_onPlaneB v) 1 k]
      simp

theorem amplitudeCoeff_one_eq_zero_of_linear_zero
    (v : Internal → ℂ) (hL : linearCoeff v = 0) (q : Nat) :
    amplitudeCoeff v 1 q = 0 := by
  simp [amplitudeCoeff, rayMomentCoeff_one_eq_zero_of_linear_zero v hL]

#print axioms amplitudeCoeff_one_three
#print axioms amplitudeCoeff_two_four_of_linear_zero
#print axioms rayMomentCoeff_one_eq_zero_of_linear_zero
#print axioms amplitudeCoeff_one_eq_zero_of_linear_zero

end M3A
