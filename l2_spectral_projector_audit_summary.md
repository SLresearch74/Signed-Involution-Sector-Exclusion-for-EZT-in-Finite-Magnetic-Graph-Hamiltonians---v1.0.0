# Layer-2 spectral-projector audit summary

This compact report records the Layer-2 conclusions retained in the manuscript. The full computation series is intended as repository material.

## Core diagnostic

For a finite Hermitian Hamiltonian

```math
H=\sum_{\lambda\in\sigma(H)}\lambda E_\lambda,
```

define the source-target spectral-projector channel component

```math
C_\lambda(\ell,s;H)=\langle \ell|E_\lambda|s\rangle.
```

Exact zero transfer is equivalent to

```math
C_\lambda(\ell,s;H)=0\quad\text{for every }\lambda\in\sigma(H).
```

The diagnostic used in the audit was

```math
\Gamma_{\ell s}(H)=\max_\lambda |\langle \ell|E_\lambda|s\rangle|.
```

## Retained conclusions

1. Sector-compatible signed systems keep the spectral-projector source-target channel closed.
2. Compatibility-breaking controls generally open the channel.
3. Replacing signed Hamiltonians by unsigned support adjacencies opens certified dark-pair channels in the tested atlas.
4. Raw eigenvalue motion is not decisive: eigenvalues may shift while the channel remains closed.
5. Degeneracy, level-spacing rigidity, recurrence and localisation are useful geometry-sensitive summaries, but they do not by themselves cause exact zero transfer.
6. Channel-aware diagnostics predict certificate structure more directly than raw spectral-shape summaries.
7. Exception cases in which an original signed-involution certificate breaks while the target remains dark motivate a future completeness theory: signed-involution darkness, larger signed-symmetry darkness, and more general Krylov or invariant-subspace darkness should be separated.

## Manuscript use

The manuscript uses this audit only to strengthen the finite spectral interpretation of the framework. It does not use these tests to claim topological protection, physical implementation, continuum geometry, or a complete classification of all graph supports.
