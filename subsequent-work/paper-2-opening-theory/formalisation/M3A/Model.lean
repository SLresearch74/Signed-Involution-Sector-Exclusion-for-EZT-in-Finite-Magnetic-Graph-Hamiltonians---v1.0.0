import M3A.Types

namespace M3A

/-- The locked six-state unperturbed Hamiltonian. Rows are receiving states
and columns are sending states. -/
def H0 {K : Type*} [Ring K] : Matrix State State K :=
  !![0, 1, 1, 1, 1, 0;
     1, 0, 1, 1, 0, 1;
     1, 1, 0, 0, 1, -1;
     1, 1, 0, 0, 1, 1;
     1, 0, 1, 1, 0, -1;
     0, 1, -1, 1, -1, 0]

/-- The four-coordinate diagonal perturbation, supported on states 1–4. -/
def diagonalPerturbation {K : Type*} [Ring K]
    (d : Internal → K) : Matrix State State K :=
  !![0, 0, 0, 0, 0, 0;
     0, d 0, 0, 0, 0, 0;
     0, 0, d 1, 0, 0, 0;
     0, 0, 0, d 2, 0, 0;
     0, 0, 0, 0, d 3, 0;
     0, 0, 0, 0, 0, 0]

/-- The locked diagonal family `H(d) = H0 + D(d)`. -/
def hamiltonian {K : Type*} [Ring K]
    (d : Internal → K) : Matrix State State K :=
  H0 + diagonalPerturbation d

/-- The spectral matrix `z I - H(d)`. -/
def spectralMatrix {K : Type*} [Ring K]
    (z : K) (d : Internal → K) : Matrix State State K :=
  z • (1 : Matrix State State K) - hamiltonian d

/-- The selected source-to-target matrix moment. -/
def selectedMoment {K : Type*} [Semiring K]
    (H : Matrix State State K) (k : Nat) : K :=
  (H ^ k) target source

end M3A
