import M3A.SignedInvolution

namespace M3A

/-- Every source-to-target moment of the locked baseline Hamiltonian vanishes,
over any characteristic-zero field. -/
theorem baseline_moments_dark
    {K : Type*} [Field K] [CharZero K] (k : Nat) :
    selectedMoment (H0 : Matrix State State K) k = 0 :=
  selectedMoment_eq_zero_of_signedCertificate (by norm_num) rOrig_certificate k

#print axioms baseline_moments_dark

end M3A
