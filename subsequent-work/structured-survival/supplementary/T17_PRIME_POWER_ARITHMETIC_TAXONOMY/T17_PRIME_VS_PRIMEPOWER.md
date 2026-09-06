# Prime versus prime-power arithmetic

## Prime local nonvanishing — PROVED

Let p be prime, empty != M proper subset of Z_p, and r!=0 modulo p. Multiplication by r permutes the exponents. If S_M(r)=0, the nonzero 0/1 mask polynomial of degree at most p-1 is divisible over Q by Phi_p=1+X+...+X^(p-1). Degree forces it to be a scalar multiple of Phi_p, whose 0/1 coefficients require the full mask. This contradicts properness.

Exceptions must be explicit: an empty mask gives zero; the full mask gives zero at nonzero displacement; r=0 gives |M| and is nonzero for every nonempty mask. The exact finite check covers every nonempty proper mask and every nonzero displacement at p=3,5,7. It checks examples, not the general proof.

For a nonempty oriented circulant of prime order the Hermitian adjacency is not scalar. All its actual nonempty spectral fibres are therefore proper. Every distinct-site projector cross entry is nonzero, ruling out an intrinsic exact-dark site pair. This agrees with the prime-order nonexistence reported by [Song and Lin](https://arxiv.org/abs/2608.10643). The empty graph is a separate degenerate exception. The prime-power dark-pair construction in this package is consequently not a hidden prime-order counterexample.

For blocks whose relevant local contractions are single nonempty-proper-mask Song sums, and whose fixed prefactors and physical amplitudes are nonzero, local arithmetic zeros cannot explain darkness at prime order. Remaining mechanisms include absent structural routes and readouts, linear-combination readout annihilation, and exact signed cancellation. With direct readout a single nonzero contraction times a stratum-unit amplitude, g=1 already at grade zero. Without these hypotheses the proposed dichotomy is too broad: an amplitude can be identically zero, or a readout can be a coherent vector combination. No universal statement suppressing those exceptions is made.

## Prime-power collapsed-count theorem — PROVED

Let n=p^a and q=n/gcd(r,n)>1. Write r=d r' with d=gcd(r,n); zeta_n^r is a primitive q-th root, differing from the chosen zeta_q by a Galois automorphism. Let c_j count m in M with m=j modulo q, for 0<=j<q. Then

\[
S_M(r)=0\iff \sum_{j=0}^{q-1}c_jX^j\text{ is divisible by }\Phi_q(X)
\iff c_j=c_{j+q/p}=\cdots=c_{j+(p-1)q/p}\quad(0\le j<q/p).
\]

For the last equivalence use Phi_q=sum_(k=0)^(p-1) X^(kq/p). A quotient of degree below q/p repeats its coefficient array in p disjoint bands, and conversely. Galois transport by r' preserves divisibility. When q=1, use S_M(0)=|M| separately; a vacuous cycle condition is not correct.

This is a local zero theorem, not a full-response classifier. Vanishing root-of-unity sums are PRIOR-ART-OWNED territory; [Lam and Leung](https://arxiv.org/abs/math/9511209) give the classical general weight classification. The displayed precise collapsed-count result is proved here by the standard cyclotomic polynomial argument, not inferred from their abstract.

## Actual application and limitation

For n=8, each locked actual fibre at displacement 2 is balanced after collapse to q=4. For n=9 with C={3}, each residue-class mask at displacement 1 is a balanced 3-cycle. These certify the actual dark source-target pairs used in the new graph examples.

For the locked eight block-4 cases, local zero-fibre contractions and signed marked relations produce a forward-closed zero block; the variable-ket cases also need the chi4 sign, and the variable-bra cases need orientation. Saying only that some mask is balanced loses those marked relations. Even complete static balance data cannot predict the roots of g=t-1 versus g=t-2 in the actual amplitude-varying pairs. Exact cyclotomic order, relative phases, orientation and coherent amplitudes remain distinct layers of information.
