# Common-future divisor theorem

## Statement — PROVED-SYNTHESIS

Let K contain the Song field, fixed poles and fixed amplitudes. Work on a nonempty one-parameter PID domain stratum A=S^(-1)K[t], with a fixed marked architecture, regular nonvanishing block frames and fixed structured reachability. For a reachable one-dimensional block gamma, let r_(h,gamma)(z,t) be the exact coherently recombined residuals through a proven safe horizon H. Assume the frozen proper-response and fixed-pole hypotheses. Choose a monic parameter-independent common denominator D(z) and write

\[
D(z)r_{h,\gamma}(z,t)=P_{h,\gamma}(z,t)=\sum_j c_{h,j}(t)z^j,
\qquad \mathcal N_\gamma(u,z,t)=\sum_{h=0}^H u^hP_{h,\gamma}(z,t).
\]

Then the stratum block-darkness ideal is

\[
J_{\gamma,\Sigma}=(c_{h,j}:0\le h\le H)A.
\]

Its generator is zero when every coefficient is zero. Otherwise it is the normalized gcd of this finite nonzero coefficient list, removing only factors inverted on the stratum. In particular, for a nonzero residual list,

\[
g_\gamma\notin\{0,1\}
\iff \exists f\in A\text{ nonzero nonunit dividing every }c_{h,j}.
\]

The restriction to a nonzero list is essential: the all-zero list is divisible by every polynomial but has generator zero, not a nonconstant normalized generator.

## Proof

The independent monomials u^h z^j make the aggregate numerator zero at a geometric parameter point exactly when all c_(h,j) vanish. D is fixed and is not the zero rational function after specialization, so clearing D neither adds nor removes residual zeros. The safe-horizon theorem extends zero through H to the entire future. These are precisely the frozen block-content hypotheses. A finitely generated ideal in A is principal; its generator is the gcd up to a unit. This proves the ideal identity and the common-divisor criterion. The prime factor valuation of g is the minimum valuation among the nonzero coefficients. Localization deletes precisely the inverted prime factors. No PP matrix is required.

Multiplying a grade numerator by a fixed monic polynomial in K[z] preserves its parameter content: coefficient recovery by descending degree is triangular with diagonal one. Thus different powers of the same fixed baseline denominator may be unified safely. Multiplication by t is not such an operation unless t is a stratum unit.

## Unit certificates and their limits

A single unit coefficient suffices. More generally, a grade with unit content suffices. Define d_unit as the earliest such grade in this fixed marked recurrence, when one exists. It is a computational certificate, not an asserted canonical invariant under all presentations.

Neither condition is necessary. With grade numerators t and t-1, neither grade has unit content, but their combined ideal is (1). A complete unit certificate is a finite Bezout identity among all numerator coefficients. The order of a nonunit factor is likewise an all-future minimum, not the order in a selected grade.

## Zero loci and strata

At a geometric point tau of Sigma, the coordinate block belongs to K0 iff g_gamma(tau)=0. Nonconstant normalized g gives a proper nonempty geometric locus; it need not have a K-rational point. Closed or nonreduced strata use A=S^(-1)(R/I) and ideals directly; a polynomial factorization in a quotient with zero divisors is not silently substituted for the PID theorem. Rebuilt rank-collapse strata have new inventories.

## Interpretation and ownership

A proper block-darkness locus is simultaneous cancellation of the entire finite marked future. A factor of a mixed linear dependence, determinant, or selected residual need not divide every coefficient of a coordinate block. This explains why the locked factors 2t-i and 2t+i are absent from g and h.

Finite observability, coefficient/content ideals, gcds and localization are PRIOR-ART-OWNED mechanisms. Their application with the marked Song compiler and declared structured blocks is PROVED-SYNTHESIS. Novelty remains OPEN. This theorem does not assert a further compact arithmetic classification.
