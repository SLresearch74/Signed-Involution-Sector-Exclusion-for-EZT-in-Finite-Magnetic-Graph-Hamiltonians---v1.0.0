# Edge-generator taxonomy

## Exact formula — PROVED-SYNTHESIS

Fix an arrow e and its declared recombination class. In regular rank-one block frames its scalar has a finite exact expression

\[
T_e(z,t)=\sum_{j\in C_e} a_j(t)c_j\,d_j(z),
\qquad c_j\in K,
\]

where c_j contains the marked Song contractions and normalization scalars, and d_j is a fixed-pole rational function. More general fixed polynomial numerators are allowed. Choose a parameter-independent monic denominator Q_e and write Q_e T_e=sum_k eta_(e,k)(t) z^k. Then

\[
h_{e,\Sigma}=\operatorname{norm}_\Sigma\gcd_k\eta_{e,k}(t),
\]

with the zero-list convention. Expanding the fixed functions Q_e d_j in the z basis gives a constant coefficient matrix C over K and eta=C a(t). Thus the compact edge computation is a constant marked linear map applied to the physical amplitude vector, followed by one coefficient gcd. Recombination must happen before content; all summands belong to the same declared arrow. Fixed K-linear dependencies among the d_j are part of C.

## Exact mechanisms

| Situation | Generator before stratum normalization | Interpretation |
|---|---|---|
| A single vanishing Song contraction | 0 | Local zero, provided no other declared contribution survives |
| One nonzero fixed rational contraction times amplitude a | normalize(a) | Pure amplitude factor |
| Several coherent contributions | content of C a | Can be zero, unit, or a new cancellation polynomial |
| A factor forced nonzero by the architecture stratum | Removed | Architecture-only, not a physical zero within Sigma |
| A nonunit survives without rank/reachability loss | Retained | Genuine physical edge-zero locus |

The first row is not a rule for ignoring the other summands. A declared edge that is identically zero can be recorded with h=0; it is absent from G_nz. There is no requirement to invert all nonzero-edge tests when defining an architecture stratum: edge vanishing need not be a coefficient-image rank collapse.

## Actual sharp example

For A=((1-t)|2>+(1+t)|0>)<0| on the certified n=8 baseline, each arrow gamma->delta equals (1+t)w_gamma/(z-theta_gamma). Its generator is t+1. At t=-1, all nine arrows vanish, but A=2|2><0| and all three projected image ranks are still one. Structured reachability persists through the nonzero input rho. No localization removes t+1.

More generally A=(|l>+f(t)|s>)<s| has h=f for every arrow and g=1, for any polynomial f in K[t]. Consequently fixed additive orders, masks, p-cycle balance and even complete signed static Song data cannot determine edge roots without appropriate amplitude information.

Unlike a block generator, h depends only on one declared coherent arrow, not its full future. This is the exact edge/block asymmetry. Root-of-unity arithmetic and content are PRIOR-ART-OWNED; this marked application is PROVED-SYNTHESIS; novelty OPEN.
