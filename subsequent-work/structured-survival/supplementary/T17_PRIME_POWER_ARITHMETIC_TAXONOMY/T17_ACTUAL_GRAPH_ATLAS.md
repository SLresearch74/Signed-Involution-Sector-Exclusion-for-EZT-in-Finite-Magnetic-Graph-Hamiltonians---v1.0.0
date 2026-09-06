# Atlas A — actual graph-realized evidence

All entries have actual oriented-circulant baselines. The graph certificate is for H0; allowed directed rank-one perturbations are not claimed Hermitian or circulant at every parameter value. The new families use one recombined degree-one event, not two separately declared physical events.

## Baselines

| ID | n / connection set | Ordered sites | Pole / fibre masks | Response field |
|---|---|---|---|---|
| G8 | 8 / {1,3}, connected | 0->2 | 0:{0,2,4,6}; -2sqrt(2):{1,3}; +2sqrt(2):{5,7} | Q(zeta8) |
| G9 | 9 / {3}, three components | 0->1 | 0:{0,3,6}; -sqrt(3):{1,4,7}; +sqrt(3):{2,5,8} | Q(zeta36), Song subfield Q(zeta9) |

Each baseline satisfies H0^3=c H0, with c=8 or 3. Projectors are P0=I-H0^2/c, Pminus=(H0^2-sqrt(c)H0)/(2c), Pplus=(H0^2+sqrt(c)H0)/(2c). Their ranks, spectral equations, orthogonality, diagonal weights and zero source-target entries are checked exactly. Fourier eigenvalue grouping is independently computed in Q[X]/Phi_lcm(n,4).

## New event families

For each row use A=(a|l>+b|s>)<s|, stratum Spec K[t], and all three blocks structurally reachable. There are nine declared possible arrows, including loops, with h=0 allowed for an identically zero arrow.

| Family ID | Baseline | a | b | Every g | Every h |
|---|---|---|---|---|---|
| n8_affine_competition | G8 | 1-t | 1+t | t-1 | t+1 |
| n9_affine_competition | G9 | 1-t | 1+t | t-1 | t+1 |
| n8_block_root_1 | G8 | t-1 | 1 | t-1 | 1 |
| n8_block_root_2 | G8 | t-2 | 1 | t-2 | 1 |
| n8_edge_root_1 | G8 | 1 | t-1 | 1 | t-1 |
| n8_edge_root_2 | G8 | 1 | t-2 | 1 | t-2 |
| n8_identically_dark | G8 | 0 | 1 | 0 | 1 |
| n8_identically_edgeless | G8 | 1 | 0 | 1 | 0 |

Rank never drops because each amplitude pair is unimodular and each two-site projected Gram determinant is nonzero. The JSON stores the amplitude polynomials, image-rank certificate, actual masks, every Song displacement value, collapsed counts, additive orders, compatible Galois transports, exact residual numerator coefficients through H=2, edge numerators, and direct specialized K0/G_nz/Kmax checks.

## Entire retained locked census

The sixteen locked G8 components are all eight (x,y) choices (1,4),(3,4),(5,4),(7,4),(6,1),(6,3),(6,5),(6,7), in both directions 0->2 and 2->0. The physical family is H0+epsilon A1+epsilon^2 A2 with A1=|1><1|-|5><5| and A2=t|x><y|. It uses its inherited seven-block Construction A inventory on D(t), not the three-block inventory of the new degree-one family. The fixed A1 is a signed combination of site events; the symbolic A2 is rank one.

All 112 block and 204 edge records are retained in the T17 JSON with derivation references and early certificates. At D(t), eight block-4 generators are zero, 104 are unit, and all 204 arrow generators are unit. At t=0 that inventory must be rebuilt; no absent A2 coordinate is called physically dark. The detailed family rule is in T17_N8_FINAL_CLASSIFICATION.md.

Evidence standing: the general dark-pair one-event theorem is PROVED-SYNTHESIS; the two baselines, eight new marked families and sixteen inherited components are VERIFIED-EXACT. This atlas contains no abstract mask-only diagonal controls and makes no unperformed census claim for n=16,25,27.
