import M3A.FixedFibreNewton
import Mathlib.Analysis.Normed.Algebra.MatrixExponential

namespace M3A

open NormedSpace
open scoped Matrix.Norms.Operator

/-- The selected source-to-target entry of the actual complex matrix
exponential. -/
noncomputable def selectedAmplitude
    (d : Internal → ℂ) (t : ℂ) : ℂ :=
  (exp ((-Complex.I * t) • hamiltonian d)) target source

/-- For every fixed diagonal parameter, the selected matrix-exponential entry
is the convergent time-Taylor series of the selected moments. -/
theorem selectedAmplitude_hasSum_timeTaylor
    (d : Internal → ℂ) (t : ℂ) :
    HasSum
      (fun q => ((-Complex.I) ^ q / (q.factorial : ℂ)) *
        selectedMoment (hamiltonian d) q * t ^ q)
      (selectedAmplitude d t) := by
  let X : Matrix State State ℂ :=
    (-Complex.I * t) • hamiltonian d
  have hmatrix :=
    NormedSpace.exp_series_hasSum_exp' (𝕂 := ℂ) X
  let rowEntry : Matrix State State ℂ →L[ℂ] (State → ℂ) :=
    ContinuousLinearMap.proj target
  let selectedEntry : Matrix State State ℂ →L[ℂ] ℂ :=
    (ContinuousLinearMap.proj source).comp rowEntry
  have hentry := selectedEntry.hasSum hmatrix
  change HasSum
    (fun q => ((-Complex.I) ^ q / (q.factorial : ℂ)) *
      selectedMoment (hamiltonian d) q * t ^ q)
    ((exp X) target source)
  apply hentry.congr
  intro s
  apply Finset.sum_congr rfl
  intro q _
  change
    (q.factorial : ℂ)⁻¹ * (X ^ q) target source =
      ((-Complex.I) ^ q / (q.factorial : ℂ)) *
        selectedMoment (hamiltonian d) q * t ^ q
  rw [show X = (-Complex.I * t) • hamiltonian d from rfl]
  rw [smul_pow]
  simp only [Matrix.smul_apply, selectedMoment, mul_pow, div_eq_mul_inv]
  ring

/-- Diagonal perturbation is linear along a declared complex ray. -/
theorem diagonalPerturbation_ray
    (v : Internal → ℂ) (ε : ℂ) :
    diagonalPerturbation (fun r => ε * v r) =
      ε • diagonalPerturbation v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagonalPerturbation]

theorem hamiltonian_ray
    (v : Internal → ℂ) (ε : ℂ) :
    hamiltonian (fun r => ε * v r) =
      (H0 : Matrix State State ℂ) + ε • diagonalPerturbation v := by
  simp [hamiltonian, diagonalPerturbation_ray]

/-- The finite evaluation of all perturbation-degree word coefficients below
a cutoff. -/
def rayPowerPrefix
    (v : Internal → ℂ) (ε : ℂ) (k n : Nat) : Matrix State State ℂ :=
  ∑ p ∈ Finset.range n, ε ^ p • rayCoeffMatrix v k p

theorem rayPowerPrefix_succ
    (v : Internal → ℂ) (ε : ℂ) (k n : Nat) :
    rayPowerPrefix v ε k (n + 1) =
      rayPowerPrefix v ε k n + ε ^ n • rayCoeffMatrix v k n := by
  simp [rayPowerPrefix, Finset.sum_range_succ]

/-- Evaluating the coefficient recurrence at `ε` reproduces left
multiplication by `H0 + ε D(v)`. -/
theorem rayPowerPrefix_step
    (v : Internal → ℂ) (ε : ℂ) (k n : Nat) :
    rayPowerPrefix v ε (k + 1) (n + 1) =
      (H0 : Matrix State State ℂ) * rayPowerPrefix v ε k (n + 1) +
        (ε • diagonalPerturbation v) * rayPowerPrefix v ε k n := by
  induction n with
  | zero => simp [rayPowerPrefix, rayCoeffMatrix]
  | succ n ih =>
      rw [rayPowerPrefix_succ v ε (k + 1) (n + 1)]
      rw [ih]
      rw [rayPowerPrefix_succ v ε k (n + 1)]
      rw [rayPowerPrefix_succ v ε k n]
      rw [rayCoeffMatrix]
      simp only [Matrix.mul_add, smul_add, mul_smul_comm,
        smul_mul_assoc, smul_smul, pow_succ]
      rw [mul_comm (ε ^ n) ε]
      abel

/-- The finite ray word polynomial evaluates exactly to the corresponding
matrix power. -/
theorem rayPowerPrefix_eq_hamiltonian_pow
    (v : Internal → ℂ) (ε : ℂ) (k : Nat) :
    rayPowerPrefix v ε k (k + 1) =
      hamiltonian (fun r => ε * v r) ^ k := by
  induction k with
  | zero => simp [rayPowerPrefix, rayCoeffMatrix]
  | succ k ih =>
      have hzero : rayCoeffMatrix v k (k + 1) = 0 :=
        rayCoeffMatrix_eq_zero_of_lt_degree v (by omega)
      have hprefix :
          rayPowerPrefix v ε k (k + 2) = rayPowerPrefix v ε k (k + 1) := by
        rw [rayPowerPrefix_succ]
        simp [hzero]
      rw [rayPowerPrefix_step v ε k (k + 1), hprefix, ih]
      rw [← add_mul]
      rw [← hamiltonian_ray]
      rw [pow_succ']

/-- At each fixed time depth, the moment along a ray is the finite polynomial
whose coefficients are exactly `rayMomentCoeff`. -/
theorem selectedMoment_rayExpansion
    (v : Internal → ℂ) (ε : ℂ) (q : Nat) :
    selectedMoment (hamiltonian (fun r => ε * v r)) q =
      ∑ p ∈ Finset.range (q + 1), rayMomentCoeff v p q * ε ^ p := by
  change (hamiltonian (fun r => ε * v r) ^ q) target source = _
  rw [← rayPowerPrefix_eq_hamiltonian_pow v ε q]
  simp [rayPowerPrefix, Matrix.sum_apply, rayMomentCoeff,
    Matrix.smul_apply, mul_comm]

/-- The actual selected amplitude restricted to the fixed ray `ε ↦ εv`. -/
noncomputable def selectedRayAmplitude
    (v : Internal → ℂ) (ε t : ℂ) : ℂ :=
  selectedAmplitude (fun r => ε * v r) t

/-- The complete analytic bridge: the actual matrix-exponential amplitude is
the convergent time series whose finite perturbation polynomial at depth `q`
has coefficients exactly `amplitudeCoeff v p q`. -/
theorem selectedRayAmplitude_hasSum_coefficients
    (v : Internal → ℂ) (ε t : ℂ) :
    HasSum
      (fun q => ∑ p ∈ Finset.range (q + 1),
        amplitudeCoeff v p q * ε ^ p * t ^ q)
      (selectedRayAmplitude v ε t) := by
  have htime := selectedAmplitude_hasSum_timeTaylor
    (fun r => ε * v r) t
  change HasSum
    (fun q => ∑ p ∈ Finset.range (q + 1),
      amplitudeCoeff v p q * ε ^ p * t ^ q)
    (selectedAmplitude (fun r => ε * v r) t)
  apply htime.congr
  intro s
  apply Finset.sum_congr rfl
  intro q _
  change
    ((-Complex.I) ^ q / (q.factorial : ℂ)) *
        selectedMoment (hamiltonian (fun r => ε * v r)) q * t ^ q =
      ∑ p ∈ Finset.range (q + 1),
        amplitudeCoeff v p q * ε ^ p * t ^ q
  rw [selectedMoment_rayExpansion]
  rw [Finset.mul_sum, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro p _
  unfold amplitudeCoeff
  ring

/-- Equality form of the complete bridge. The outer series converges globally
in time, and every inner perturbation sum is finite. -/
theorem selectedRayAmplitude_eq_tsum_coefficients
    (v : Internal → ℂ) (ε t : ℂ) :
    selectedRayAmplitude v ε t =
      ∑' q, ∑ p ∈ Finset.range (q + 1),
        amplitudeCoeff v p q * ε ^ p * t ^ q :=
  (selectedRayAmplitude_hasSum_coefficients v ε t).tsum_eq.symm

/-- The formal dark branch is therefore an identically zero actual
matrix-exponential amplitude along the whole complex ray. -/
theorem selectedRayAmplitude_eq_zero_of_linear_quadratic_zero
    (v : Internal → ℂ)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0)
    (ε t : ℂ) :
    selectedRayAmplitude v ε t = 0 := by
  rw [selectedRayAmplitude_eq_tsum_coefficients]
  simp [amplitudeCoeff_eq_zero_of_linear_quadratic_zero v hL hQ]

#print axioms selectedAmplitude_hasSum_timeTaylor
#print axioms rayPowerPrefix_eq_hamiltonian_pow
#print axioms selectedMoment_rayExpansion
#print axioms selectedRayAmplitude_hasSum_coefficients
#print axioms selectedRayAmplitude_eq_tsum_coefficients
#print axioms selectedRayAmplitude_eq_zero_of_linear_quadratic_zero

end M3A
