# Atlas B — formal arithmetic controls

None of the controls in this document is asserted to be an oriented-circulant realization. They test algebraic implications. The actual nonconstant existence result comes exclusively from Atlas A.

## Exact order and cardinality

Reduce 1+X^2 modulo Phi4 and Phi8 to obtain 0 versus 1+X^2. Reduce 1+X^4 modulo Phi8 and Phi16 to obtain 0 versus 1+X^4. Reduce 1+X^3+X^6 modulo Phi9 and Phi27 to obtain 0 versus itself. At n=8, masks {0,4} and {0,2} have equal size but values 0 and 1+i. These are actual cyclotomic calculations, not certificates that the masks occur as whole spectral fibres of a specified graph.

## Marginal Galois data and signed coherence

At n=3 with M={1}, compare zeta3-zeta3 with zeta3-zeta3^2. Each occurring value is nonzero, primitive, has modulus one, belongs to the same marginal orbit, and has the same unbalanced singleton count type. The first sum is zero; the second reduces to 1+2X modulo X^2+X+1. Joint transport is different. This is the precise falsification of marginal-orbit compression.

## Nonlocal cancellation and the K0/Kmax distinction

The three-state fan-out has Omega=(0,1/z,1/z), arrows A->B=1/z,A->C=-1/z, and no later continuations. It has g_A=0, g_B=g_C=1, K0={A}, Kmax empty. Replacing -1 by +1 gives g_A=1. No nonzero local coefficient was replaced by zero, and the unweighted graph did not change.

## Declared split/recombine

With states A,B,U, output only at U, include A->B=1. Either declare one recombined arrow B->U=(+1)+(-1)=0, or two independent declared arrows with coefficients +1 and -1. The aggregate recurrence is the same: K0={A,B}. But the first declared model retains {A,B} in Kmax; the second has no nonempty forward-closed subset of K0. This is a structured-declaration control, not a graph existence claim.

## Content and denominator controls

The coherent sum 1+(t-1)=t has ideal (t), whereas the sum of the separate summand ideals is (1). The shortest version is 1-1=0 with both summand ideals unit. Grade contents (t) and (t-1) jointly generate (1), although neither grade has unit content. A formal diagonal response with entries 1 and (t-1)(1+zeta_n) has a nonconstant coordinate factor when the latter scalar is nonzero, but no graph realization follows merely from writing it down.

Unsafe parameter-dependent clearing manufactures a false factor: 1/z becomes t/(tz). The valid fixed-denominator numerator is 1, not t. All new T17 certificates instead use fixed Q=z(z^2-c).

## Standing

The listed polynomial and rational identities are VERIFIED-EXACT and have elementary proofs. The reduced sufficiency assertions they contradict are FALSIFIED. Whether the precise abstract fan-out or split/recombine model has a realization within a narrower graph subclass is OPEN and unnecessary for the separate actual amplitude-blind obstruction theorem.
