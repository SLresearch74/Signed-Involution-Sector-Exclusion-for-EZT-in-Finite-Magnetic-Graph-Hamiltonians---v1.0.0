import M3A.Types

namespace M3A

variable {𝕂 : Type*} [CommRing 𝕂]

def ell (v₁ v₂ v₃ v₄ : 𝕂) : 𝕂 :=
  v₁ - v₂ + v₃ - v₄

def quad (v₁ v₂ v₃ v₄ : 𝕂) : 𝕂 :=
  v₂ * v₄ - v₁ * v₃

def cubicCoeff (v₁ v₂ v₃ v₄ : 𝕂) : 𝕂 :=
  v₁ * v₂ * (v₃ - v₄) +
  v₃ * v₄ * (v₁ - v₂)

/-- The linear numerator coefficient in four-coordinate notation. -/
def linearCoeff (d : Internal → 𝕂) : 𝕂 :=
  ell (d 0) (d 1) (d 2) (d 3)

/-- The quadratic numerator coefficient in four-coordinate notation. -/
def quadraticCoeff (d : Internal → 𝕂) : 𝕂 :=
  quad (d 0) (d 1) (d 2) (d 3)

/-- The cubic numerator coefficient in four-coordinate notation. -/
def cubicNumeratorCoeff (d : Internal → 𝕂) : 𝕂 :=
  cubicCoeff (d 0) (d 1) (d 2) (d 3)

theorem coefficient_syzygy
    (v₁ v₂ v₃ v₄ : 𝕂) :
    cubicCoeff v₁ v₂ v₃ v₄
      + (v₂ + v₄) * quad v₁ v₂ v₃ v₄
      + v₂ * v₄ * ell v₁ v₂ v₃ v₄
      = 0 := by
  simp [cubicCoeff, quad, ell]
  ring

#print axioms coefficient_syzygy

end M3A
