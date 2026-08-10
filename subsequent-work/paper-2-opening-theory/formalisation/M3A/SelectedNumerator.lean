import M3A.Model
import M3A.CoefficientAlgebra

namespace M3A

/-- Retained spectral-matrix rows after deleting source row 0. -/
def retainedRow (i : Fin 5) : State := i.succ

/-- Retained spectral-matrix columns after deleting target column 5. -/
def retainedCol (j : Fin 5) : State := j.castSucc

/-- The `5 × 5` minor obtained from `z I - H(d)` by deleting row 0 and
column 5. -/
def selectedMinor {K : Type*} [Ring K]
    (z : K) (d : Internal → K) : Matrix (Fin 5) (Fin 5) K :=
  (spectralMatrix z d).submatrix retainedRow retainedCol

/-- An explicit display of the selected minor, used to certify the retained
row and column embeddings before determinant expansion. -/
def selectedMinorExplicit {K : Type*} [Ring K]
    (z : K) (d : Internal → K) : Matrix (Fin 5) (Fin 5) K :=
  !![-1, z - d 0, -1, -1, 0;
     -1, -1, z - d 1, 0, -1;
     -1, -1, 0, z - d 2, -1;
     -1, 0, -1, -1, z - d 3;
     0, -1, 1, -1, 1]

theorem selectedMinor_eq_explicit {K : Type*} [CommRing K]
    (z : K) (d : Internal → K) :
    selectedMinor z d = selectedMinorExplicit z d := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [selectedMinor, selectedMinorExplicit, spectralMatrix, hamiltonian,
      diagonalPerturbation, H0, retainedRow, retainedCol]

/-- The unreduced selected adjugate cofactor. The minus sign is
`(-1)^(0+5)`, with row 0 and column 5 deleted. -/
def selectedNumerator {K : Type*} [CommRing K]
    (z : K) (d : Internal → K) : K :=
  -Matrix.det (selectedMinor z d)

set_option maxHeartbeats 2000000 in
-- Recursive expansion of the declared `Fin 5` determinant exceeds the default budget.
/-- The exact actual-coordinate selected numerator, proved by expanding the
declared cofactor rather than by interpolation or numerical evaluation. -/
theorem selectedNumerator_formula {K : Type*} [CommRing K]
    (z : K) (d : Internal → K) :
    selectedNumerator z d =
      linearCoeff d * (z ^ 2 + 2 * z) +
      2 * quadraticCoeff d * (z + 1) +
      cubicNumeratorCoeff d := by
  rw [selectedNumerator, selectedMinor_eq_explicit]
  simp [selectedMinorExplicit, Matrix.det_succ_row_zero, Fin.sum_univ_succ,
    Fin.succAbove,
    linearCoeff, quadraticCoeff, cubicNumeratorCoeff, ell, quad, cubicCoeff]
  ring

/-- The exact numerator after substituting the fixed ray `d = εv`. -/
theorem selectedNumerator_ray_formula {K : Type*} [CommRing K]
    (z ε : K) (v : Internal → K) :
    selectedNumerator z (ε • v) =
      ε * linearCoeff v * (z ^ 2 + 2 * z) +
      2 * ε ^ 2 * quadraticCoeff v * (z + 1) +
      ε ^ 3 * cubicNumeratorCoeff v := by
  rw [selectedNumerator_formula]
  simp [linearCoeff, quadraticCoeff, cubicNumeratorCoeff, ell, quad, cubicCoeff,
    smul_eq_mul]
  ring

/-- The tuple-form coefficient syzygy. -/
theorem cubicNumeratorCoeff_syzygy {K : Type*} [CommRing K]
    (v : Internal → K) :
    cubicNumeratorCoeff v
      + (v 1 + v 3) * quadraticCoeff v
      + v 1 * v 3 * linearCoeff v = 0 := by
  simpa [linearCoeff, quadraticCoeff, cubicNumeratorCoeff] using
    coefficient_syzygy (v 0) (v 1) (v 2) (v 3)

/-- If the linear and quadratic numerator coefficients vanish, the cubic one
vanishes as well; hence this family has no separate cubic branch. -/
theorem cubicNumeratorCoeff_eq_zero_of_linear_quadratic_zero
    {K : Type*} [CommRing K] (v : Internal → K)
    (hL : linearCoeff v = 0) (hQ : quadraticCoeff v = 0) :
    cubicNumeratorCoeff v = 0 := by
  have h := cubicNumeratorCoeff_syzygy v
  rw [hL, hQ] at h
  simpa using h

#print axioms selectedMinor_eq_explicit
#print axioms selectedNumerator_formula
#print axioms selectedNumerator_ray_formula
#print axioms cubicNumeratorCoeff_eq_zero_of_linear_quadratic_zero

end M3A
