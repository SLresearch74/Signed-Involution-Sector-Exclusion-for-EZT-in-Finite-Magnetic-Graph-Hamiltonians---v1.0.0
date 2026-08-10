import M3A.Model

namespace M3A

/-- The signed involution swapping states 1/2 and 3/4 and negating the target. -/
def rOrig {K : Type*} [Ring K] : Matrix State State K :=
  !![1, 0, 0, 0, 0, 0;
     0, 0, 1, 0, 0, 0;
     0, 1, 0, 0, 0, 0;
     0, 0, 0, 0, 1, 0;
     0, 0, 0, 1, 0, 0;
     0, 0, 0, 0, 0, -1]

/-- The signed involution swapping states 1/4 and 2/3 and negating the target. -/
def rAlt {K : Type*} [Ring K] : Matrix State State K :=
  !![1, 0, 0, 0, 0, 0;
     0, 0, 0, 0, 1, 0;
     0, 0, 0, 1, 0, 0;
     0, 0, 1, 0, 0, 0;
     0, 1, 0, 0, 0, 0;
     0, 0, 0, 0, 0, -1]

theorem rOrig_involutive {K : Type*} [Ring K] :
    (rOrig : Matrix State State K) * rOrig = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rOrig, Matrix.mul_apply, Fin.sum_univ_succ]

theorem rAlt_involutive {K : Type*} [Ring K] :
    (rAlt : Matrix State State K) * rAlt = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rAlt, Matrix.mul_apply, Fin.sum_univ_succ]

theorem rOrig_commutes_H0 {K : Type*} [Ring K] :
    Commute (rOrig : Matrix State State K) H0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rOrig, H0, Matrix.mul_apply, Fin.sum_univ_succ]

theorem rAlt_commutes_H0 {K : Type*} [Ring K] :
    Commute (rAlt : Matrix State State K) H0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rAlt, H0, Matrix.mul_apply, Fin.sum_univ_succ]

/-- A signed-symmetry certificate for vanishing selected moments. The
involution field records the certificate semantics; the vanishing argument
uses commutation and the opposite source/target characters. -/
structure SignedCertificate {K : Type*} [Ring K]
    (H S : Matrix State State K) : Prop where
  involutive : S * S = 1
  commutes : Commute S H
  source_even : ∀ i, S i source = if i = source then 1 else 0
  target_odd : ∀ j, S target j = if j = target then -1 else 0

theorem rOrig_source_even {K : Type*} [Ring K] (i : State) :
    (rOrig : Matrix State State K) i source =
      if i = source then 1 else 0 := by
  fin_cases i <;> simp [rOrig, source]

theorem rOrig_target_odd {K : Type*} [Ring K] (j : State) :
    (rOrig : Matrix State State K) target j =
      if j = target then -1 else 0 := by
  fin_cases j <;> simp [rOrig, target]

theorem rAlt_source_even {K : Type*} [Ring K] (i : State) :
    (rAlt : Matrix State State K) i source =
      if i = source then 1 else 0 := by
  fin_cases i <;> simp [rAlt, source]

theorem rAlt_target_odd {K : Type*} [Ring K] (j : State) :
    (rAlt : Matrix State State K) target j =
      if j = target then -1 else 0 := by
  fin_cases j <;> simp [rAlt, target]

theorem rOrig_certificate {K : Type*} [Ring K] :
    SignedCertificate (H0 : Matrix State State K) rOrig where
  involutive := rOrig_involutive
  commutes := rOrig_commutes_H0
  source_even := rOrig_source_even
  target_odd := rOrig_target_odd

theorem rAlt_certificate {K : Type*} [Ring K] :
    SignedCertificate (H0 : Matrix State State K) rAlt where
  involutive := rAlt_involutive
  commutes := rAlt_commutes_H0
  source_even := rAlt_source_even
  target_odd := rAlt_target_odd

/-- A signed certificate forces every selected matrix moment to vanish when
the scalar 2 is nonzero. -/
theorem selectedMoment_eq_zero_of_signedCertificate
    {K : Type*} [Field K]
    {H S : Matrix State State K}
    (h2 : (2 : K) ≠ 0) (cert : SignedCertificate H S) (k : Nat) :
    selectedMoment H k = 0 := by
  have hcomm : S * H ^ k = H ^ k * S := (cert.commutes.pow_right k).eq
  have hentry := congrArg (fun M => M target source) hcomm
  have hneg : -(H ^ k) target source = (H ^ k) target source := by
    simpa [Matrix.mul_apply, cert.target_odd, cert.source_even] using hentry
  have htwo : (2 : K) * (H ^ k) target source = 0 := by
    calc
      (2 : K) * (H ^ k) target source =
          (H ^ k) target source + (H ^ k) target source := by ring
      _ = -(H ^ k) target source + (H ^ k) target source := by rw [hneg]
      _ = 0 := neg_add_cancel _
  have hm : (H ^ k) target source = 0 :=
    (mul_eq_zero.mp htwo).resolve_left h2
  exact hm

end M3A
