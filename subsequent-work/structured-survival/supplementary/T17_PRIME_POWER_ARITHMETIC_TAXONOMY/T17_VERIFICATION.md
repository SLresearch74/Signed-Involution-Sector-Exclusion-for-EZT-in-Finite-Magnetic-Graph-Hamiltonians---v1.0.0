# Verification and reproducibility

## Result — VERIFIED-EXACT

The inherited T16 verification passes with unchanged generator counts and locked outcomes. The T17 exact arithmetic computation passes, and the separate standard-library verifier passes without using SymPy or the same radical-projector implementation.

| Check | Result |
|---|---|
| Required deliverables | All 18 present: 17 Markdown reports and the exact JSON ledger |
| Locked census | 16 components, 112 block generators, 204 edge generators |
| Raw block counts | 1:48, t:56, 0:8 |
| Normalized block counts on D(t) | 1:104, 0:8 |
| Raw edge counts / localized edges | 1:140, t:64 / all 204 unit |
| Early unit-content grades | grade 0:60, grade 1:32, grade 2:8, grade 3:4 |
| New actual baselines / event families | 2 / 8 |
| New block / possible declared edge records | 24 / 72 |
| Independent Gaussian-rational physical coefficient checks | 192 |
| Prime local nonvanishing checks | 888 mask/displacement cases at 3,5,7 |
| Mandatory control categories | All 14 retained with evidence references |
| PP observability matrix constructed | No |

## What was independently checked

The main exact calculation recomputes content from terminal T16 coefficient ledgers; compares K0, the declared nonzero graph and Kmax directly with T15; checks adjacency/projector/Fourier/Song identities for new baselines; computes finite future and arrow contents; verifies coefficient/projected ranks and structured outcomes at all recorded sample points; and checks physical Neumann responses.

The independent verifier uses pairs of rational numbers for Gaussian arithmetic. For each new family it constructs H0 from the oriented connection set, checks H0^3=c H0, and constructs the rational resolvent polynomial

G0=I/z+H0/(z^2-c)+H0^2/[z(z^2-c)].

At z=5 and z=6 it verifies the inverse identity exactly and recomputes physical event grades 1,2,3 at the recorded parameter values. Its 192 coefficient comparisons use no floating-point tolerances. It independently checks the Fourier pole sign using reduction modulo Phi8 or Phi36. File integrity and input hashes are checked, and an exact machine-ledger hash is recorded in T17_VERIFICATION.json.

## Proof versus testing

The all-parameter rank and generator claims follow from the unimodular amplitude-pair proof, orthogonal two-site spectral projections, and the exact identity r_(h,gamma)=a b^h rho^h q_gamma. Finite parameter tests are additional regression checks, not a proof that the formula holds elsewhere. The general prime theorem and p-cycle iff have explicit algebraic proofs in their report; 888 finite cases do not substitute for those proofs.

The new baseline search was deliberately bounded. No new graph census was performed at n=16,25,27 after small positive examples were found. Formal controls at those orders remain labeled formal.

## Regeneration

The exact build is `_T17_WORK/t17_exact.py`; it uses the existing local mathematics library in `_MV1_WORK/deps`. The independent final check is `_T17_WORK/verify_t17.py` and needs only standard Python. Run the exact build first, then the independent check. The inherited check remains `_T16_WORK/verify_t16.py`. Runtime versions are recorded in the machine ledger. These are local workspace scripts; no dependencies were installed and no prior-stage files were modified.

The reproducible machine ledger is T17_MACHINE_READABLE.json; the supplementary machine verification result is T17_VERIFICATION.json. The final judgment and complete 25-question decision table are in T17_MAIN_FINDINGS.md.
