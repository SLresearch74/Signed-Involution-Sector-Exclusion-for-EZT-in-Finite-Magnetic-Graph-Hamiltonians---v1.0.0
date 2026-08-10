import M3A.DarkPlanes

namespace M3A

/-- The exact sum of all length-`k` matrix words with exactly `j` copies of
`D(v)`. At each step the recurrence prepends either `H0` without changing the
degree, or `D(v)` while increasing the perturbation degree by one. -/
def rayCoeffMatrix {K : Type*} [CommRing K]
    (v : Internal → K) : Nat → Nat → Matrix State State K
  | 0, 0 => 1
  | 0, _ + 1 => 0
  | k + 1, 0 => H0 * rayCoeffMatrix v k 0
  | k + 1, j + 1 =>
      H0 * rayCoeffMatrix v k (j + 1) +
        diagonalPerturbation v * rayCoeffMatrix v k j

/-- The selected source-to-target coefficient of perturbation degree `j` in
the length-`k` word expansion. -/
def rayMomentCoeff {K : Type*} [CommRing K]
    (v : Internal → K) (j k : Nat) : K :=
  rayCoeffMatrix v k j target source

@[simp] theorem diagonalPerturbation_source
    {K : Type*} [CommRing K] (v : Internal → K) (i : State) :
    diagonalPerturbation v i source = 0 := by
  fin_cases i <;> simp [diagonalPerturbation, source]

@[simp] theorem diagonalPerturbation_target
    {K : Type*} [CommRing K] (v : Internal → K) (i : State) :
    diagonalPerturbation v target i = 0 := by
  fin_cases i <;> simp [diagonalPerturbation, target]

theorem diagonalPerturbation_pow_succ_source
    {K : Type*} [CommRing K] (v : Internal → K) (n : Nat) (i : State) :
    (diagonalPerturbation v ^ (n + 1)) i source = 0 := by
  rw [pow_succ]
  simp [Matrix.mul_apply]

theorem diagonalPerturbation_pow_succ_target
    {K : Type*} [CommRing K] (v : Internal → K) (n : Nat) (i : State) :
    (diagonalPerturbation v ^ (n + 1)) target i = 0 := by
  rw [pow_succ']
  simp [Matrix.mul_apply]

/-- A word cannot contain more perturbation letters than its length. -/
theorem rayCoeffMatrix_eq_zero_of_lt_degree
    {K : Type*} [CommRing K] (v : Internal → K)
    {k j : Nat} (h : k < j) :
    rayCoeffMatrix v k j = 0 := by
  induction k generalizing j with
  | zero =>
      cases j with
      | zero => omega
      | succ j => simp [rayCoeffMatrix]
  | succ k ih =>
      cases j with
      | zero => omega
      | succ j =>
          simp [rayCoeffMatrix,
            ih (j := j + 1) (by omega), ih (j := j) (by omega)]

/-- At maximal degree the only word is `D(v)^j`. -/
theorem rayCoeffMatrix_top_degree
    {K : Type*} [CommRing K] (v : Internal → K) (j : Nat) :
    rayCoeffMatrix v j j = diagonalPerturbation v ^ j := by
  induction j with
  | zero => simp [rayCoeffMatrix]
  | succ j ih =>
      rw [rayCoeffMatrix]
      rw [rayCoeffMatrix_eq_zero_of_lt_degree v (by omega)]
      simp [ih, pow_succ']

/-- Degree zero is the unperturbed word `H0^k`; its darkness remains the
separate M1 theorem. -/
theorem rayCoeffMatrix_zero_degree
    {K : Type*} [CommRing K] (v : Internal → K) (k : Nat) :
    rayCoeffMatrix v k 0 = (H0 : Matrix State State K) ^ k := by
  induction k with
  | zero => simp [rayCoeffMatrix]
  | succ k ih => simp [rayCoeffMatrix, ih, pow_succ']

/-- With `j` perturbation letters and one `H0`, the source column retains only
the word whose rightmost letter is `H0`. -/
theorem rayCoeffMatrix_nearTop_source
    {K : Type*} [CommRing K] (v : Internal → K) (j : Nat) (i : State) :
    rayCoeffMatrix v (j + 1) j i source =
      (diagonalPerturbation v ^ j * (H0 : Matrix State State K)) i source := by
  induction j generalizing i with
  | zero => simp [rayCoeffMatrix]
  | succ j ih =>
      rw [rayCoeffMatrix]
      rw [Matrix.add_apply]
      rw [rayCoeffMatrix_top_degree]
      have hz :
          ((H0 : Matrix State State K) * diagonalPerturbation v ^ (j + 1))
              i source = 0 := by
        simp [Matrix.mul_apply, diagonalPerturbation_pow_succ_source]
      rw [hz, zero_add]
      calc
        (diagonalPerturbation v * rayCoeffMatrix v (j + 1) j) i source =
            ∑ x, diagonalPerturbation v i x *
              rayCoeffMatrix v (j + 1) j x source := by
                rw [Matrix.mul_apply]
        _ = ∑ x, diagonalPerturbation v i x *
              (diagonalPerturbation v ^ j * (H0 : Matrix State State K))
                x source := by
                apply Finset.sum_congr rfl
                intro x _
                rw [ih x]
        _ = (diagonalPerturbation v *
              (diagonalPerturbation v ^ j * (H0 : Matrix State State K)))
                i source := by
                rw [Matrix.mul_apply]
        _ = (diagonalPerturbation v ^ (j + 1) *
              (H0 : Matrix State State K)) i source := by
                rw [← Matrix.mul_assoc, ← pow_succ']

/-- Positive perturbation degree requires one unperturbed access edge at each
endpoint, hence no selected word coefficient occurs below `k=j+2`. -/
theorem sixState_support_bound
    {K : Type*} [CommRing K] (v : Internal → K)
    {j k : Nat} (hpos : 0 < j) (hk : k < j + 2) :
    rayMomentCoeff v j k = 0 := by
  by_cases hkj : k < j
  · simp [rayMomentCoeff, rayCoeffMatrix_eq_zero_of_lt_degree v hkj]
  have hcases : k = j ∨ k = j + 1 := by omega
  rcases hcases with rfl | rfl
  · rw [rayMomentCoeff, rayCoeffMatrix_top_degree]
    obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hpos)
    exact diagonalPerturbation_pow_succ_source v n target
  · rw [rayMomentCoeff, rayCoeffMatrix_nearTop_source]
    obtain ⟨n, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hpos)
    simp [Matrix.mul_apply, diagonalPerturbation_pow_succ_target]

/-- At the endpoint boundary the only surviving selected word is
`H0 D(v)^j H0`. -/
theorem rayMomentCoeff_boundary_matrix
    {K : Type*} [CommRing K] (v : Internal → K) (j : Nat) :
    rayMomentCoeff v j (j + 2) =
      ((H0 : Matrix State State K) * diagonalPerturbation v ^ j *
        (H0 : Matrix State State K)) target source := by
  cases j with
  | zero => simp [rayMomentCoeff, rayCoeffMatrix]
  | succ j =>
      simp only [rayMomentCoeff]
      rw [rayCoeffMatrix]
      rw [Matrix.add_apply]
      have hz :
          (diagonalPerturbation v * rayCoeffMatrix v (j + 2) j)
              target source = 0 := by
        simp [Matrix.mul_apply]
      rw [hz, add_zero]
      rw [Matrix.mul_assoc]
      simp only [Matrix.mul_apply]
      apply Finset.sum_congr rfl
      intro i _
      rw [rayCoeffMatrix_nearTop_source]
      rw [Matrix.mul_apply]

theorem diagonalPerturbation_pow_succ
    {K : Type*} [CommRing K] (v : Internal → K) (j : Nat) :
    diagonalPerturbation v ^ (j + 1) =
      diagonalPerturbation (fun r => v r ^ (j + 1)) := by
  induction j with
  | zero =>
      ext i l
      fin_cases i <;> fin_cases l <;> simp [diagonalPerturbation]
  | succ j ih =>
      rw [pow_succ]
      rw [ih]
      ext i l
      fin_cases i <;> fin_cases l <;>
        simp [diagonalPerturbation, Matrix.mul_apply, Fin.sum_univ_succ,
          pow_succ]

/-- The exact boundary coefficient is the signed power-sum of the four ray
coordinates. This is a coefficient sum, not merely existence of a word. -/
theorem sixState_boundary_ray
    {K : Type*} [CommRing K] (v : Internal → K) (j : Nat) :
    rayMomentCoeff v j (j + 2) =
      v 0 ^ j - v 1 ^ j + v 2 ^ j - v 3 ^ j := by
  rw [rayMomentCoeff_boundary_matrix]
  cases j with
  | zero => simp [H0, target, source, Matrix.mul_apply, Fin.sum_univ_succ]
  | succ j =>
      rw [diagonalPerturbation_pow_succ]
      simp [H0, diagonalPerturbation, target, source, Matrix.mul_apply,
        Fin.sum_univ_succ]
      ring

theorem rayMomentCoeff_one_three
    {K : Type*} [CommRing K] (v : Internal → K) :
    rayMomentCoeff v 1 3 = linearCoeff v := by
  rw [sixState_boundary_ray]
  simp [linearCoeff, ell]

theorem rayMomentCoeff_two_four_of_linear_zero
    {K : Type*} [CommRing K] (v : Internal → K)
    (hL : linearCoeff v = 0) :
    rayMomentCoeff v 2 4 = 2 * quadraticCoeff v := by
  rw [sixState_boundary_ray]
  have hL' : v 0 - v 1 + v 2 - v 3 = 0 := by
    simpa [linearCoeff, ell] using hL
  simp [quadraticCoeff, quad]
  linear_combination (v 0 + v 1 + v 2 + v 3) * hL'

#print axioms sixState_support_bound
#print axioms rayMomentCoeff_boundary_matrix
#print axioms sixState_boundary_ray
#print axioms rayMomentCoeff_one_three
#print axioms rayMomentCoeff_two_four_of_linear_zero

end M3A
