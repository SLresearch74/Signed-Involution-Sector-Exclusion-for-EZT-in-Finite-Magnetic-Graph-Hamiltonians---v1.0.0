# Graph-realizability audit

## Positive answer in the declared directed rank-one event model

Nonconstant normalized block and edge generators occur on a constant-rank, constant-structured-reachability stratum. The smallest positive baseline used here is the connected n=8 oriented circulant C={1,3}. No claim of global minimality is made.

The baseline is an actual oriented graph with Hermitian adjacency H0[j,j+c]=i and H0[j,j-c]=-i for c in C. The perturbation is a declared directed rank-one coefficient, as in the frozen M3A model; it need not be Hermitian or circulant. We do not claim that H0+epsilon A(t) is an unweighted oriented-circulant adjacency for every t. Requiring Hermitian perturbations or only single site-to-site coefficients would be a different, narrower class.

## Certified dark-pair one-event class

Fix n=p^a, an oriented Hermitian circulant H0 and distinct ordered sites (s,l) with

\[
\langle l|P_\theta|s\rangle=S_\theta(l-s)/n=0
\quad\text{for every actual spectral fibre.}
\]

Let w_theta=|M_theta|/n. Circulancy gives equal diagonal projector entries w_theta at both sites. The vectors P_theta|s> and P_theta|l> are orthogonal and nonzero, with Gram matrix w_theta I_2. In particular each relevant fibre has dimension at least two, although each declared image block below has dimension one.

Declare exactly one degree-one event

\[
A(t)=(a(t)|l\rangle+b(t)|s\rangle)\langle s|,
\qquad (a,b)A_\Sigma=A_\Sigma.
\]

The amplitude pair is unimodular on the specified PID stratum. Both A and every P_theta A have rank one there. The polynomial image frames x_theta=P_theta(a|l>+b|s>) never vanish; this is not a singular rescaling of a disappearing block. Polynomial summands of A are coherently recombined into this one declared event, not split into independent events or delay degrees.

More explicitly, choose u,v in the stratum ring with ua+vb=1. The functional (u<l|P_theta+v<s|P_theta)/w_theta takes x_theta to one. Thus each image frame has a regular left inverse on the stratum, certifying that its content factors are not artefacts of a non-primitive coordinate generator.

Put q_theta=w_theta/(z-theta), rho=sum_theta q_theta. In these frames, the frozen endpoint realization has

\[
\Omega_\theta=a q_\theta,\qquad
M_{\delta\gamma}=b q_\gamma,\qquad B_\delta=\rho.
\]

Every coordinate block is directly structurally reachable because rho is a nonzero rational function independent of t. This is structured reachability; ordinary Kalman reachability over K(z) is not asserted to have full dimension. All blocks have the same degree, with no delay-only blocks.

Induction gives r_(h,gamma)=a b^h rho^h q_gamma. Every future coefficient contains a, and grade zero has content exactly (a), because q_gamma has fixed nonzero scalar numerator after fixed denominator clearing. Each arrow has content (b). Therefore

\[
\boxed{g_{\gamma,\Sigma}=\operatorname{norm}_\Sigma(a),\qquad
h_{\delta\gamma,\Sigma}=\operatorname{norm}_\Sigma(b).}
\]

This is a graph-realized sufficient classifier for the stated class, not all rank-one prime-power families. At any parameter point K0=Kmax=W if a=0, and both are zero otherwise. The nonzero declared graph is complete, including loops, when b is nonzero and empty when b=0. Since (a,b)=1 on the stratum, both cannot vanish together.

## Connected n=8 affine example

Take (s,l)=(0,2), a=1-t, b=1+t. The masks at poles (0,-2sqrt(2),+2sqrt(2)) are ({0,2,4,6},{1,3},{5,7}). All three sums at displacement 2 vanish. Their weights are (1/2,1/4,1/4), and

\[
\rho(z)=\frac{z^2-4}{z(z^2-8)}.
\]

The stratum is all Spec K8[t]: I=0, S={1}. The rank certificate (a+b)/2=1 holds at every complex parameter value. The three block generators are t-1 and the nine recombined arrow generators are t+1. Neither factor is an architecture unit.

| Parameter | Rank A / projected ranks | K0 | Nonzero arrows | Kmax |
|---|---|---|---|---|
| t=1 | 1 / (1,1,1) | all three blocks | all nine | all three blocks |
| t=-1 | 1 / (1,1,1) | zero | none | zero |
| t different from +/-1 | 1 / (1,1,1) | zero | all nine | zero |

The physical resolvent independently has target-source entry

\[
\langle l|(zI-H_0-\epsilon A)^{-1}|s\rangle
=\frac{\epsilon a\rho^2}{1-\epsilon b\rho}.
\]

To prove it, use G0=(zI-H0)^(-1), baseline cross entry zero, <l|G0(a|l>+b|s>)=a rho and <s|G0(a|l>+b|s>)=b rho in the rank-one inverse identity. Equivalently its event-grade k coefficient is a b^(k-1)rho^(k+1). Thus t=1 is actual complete transfer darkness; t=-1 kills future arrows but does not kill the first response.

## n=9 cross-field example and certificate checks

Take C={3}, s=0,l=1. This graph is three disjoint directed triangles; disconnectedness is stated, not hidden. Masks at poles (0,-sqrt(3),+sqrt(3)) are ({0,3,6},{1,4,7},{2,5,8}), all weights 1/3, all cross sums zero, and rho=(z^2-1)/(z(z^2-3)). Use K_Song=Q(zeta9), K=Q(zeta36). The same affine family has g=t-1 and h=t+1 on all t.

For both baselines, the exact certificate checks adjacency, H0^3=c H0 (c=8 or 3), projector idempotency/orthogonality and ranks, Fourier eigenvalue fibre grouping in a cyclotomic quotient, all marked Song sums, p-cycle balance, simultaneous Galois transport, and (zI-H0)G0=I. It checks the arithmetic through H=2 and the first three physical Neumann grades independently at the marked parameter values. The all-parameter statement follows from the displayed identities and unimodularity, not from sample points.

## Bounded search and standing

At n=4, the nonempty baseline C={1} has singleton nonzero-pole fibres, excluding a dark pair for this construction. n=8 and n=9 give positives, so larger new graph searches at 16,25,27 were unnecessary and were not performed. Formal exact-order controls at those orders remain separate. The general construction is PROVED-SYNTHESIS; certified instances are VERIFIED-EXACT; novelty OPEN.
