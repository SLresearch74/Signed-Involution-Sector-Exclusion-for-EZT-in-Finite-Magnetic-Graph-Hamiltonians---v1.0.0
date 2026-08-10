# M3A Paper II integrated flagship release

> **Historical source-bundle guide.** This file records the supplied R1.0
> bundle. For the repository-integrated R2.1 manuscript, build instructions
> and current trust boundary, start at `../README.md` and
> `R2_1_REPOSITORY_INTEGRATION_AUDIT.md`.

This is the author-review release of **Exact Opening and Coefficient-Sensitive Newton Geometry of a Six-State Dark Quantum Channel**, Version R1.0, 3 August 2026.

Start with `PAPER/main.pdf`. The manuscript has the required 14-section architecture, six appendices, eight vector figures, Harvard author--date references and UK English. Its principal scope boundary is:

> For every fixed positive rational weight, after finite ramification where needed, the pulled amplitude has a finitely generated coefficient ideal, so a finite coefficient-stratified exact-zero/first-survivor decision exists. No effective uniform depth bound or finite global recursive atlas over all positive weights has been proved.

Reproduce the exact checks with:

```text
python CODE/verify_paper.py
python CODE/verify_paper.py --fixture
```

The first command regenerates `EXPECTED/paper_verification.json`. The second perturbs a locked Hamiltonian edge and recomputes both exact routes; successful discrepancy detection is written to `DATA/discrepancy_detection.json`.

The audit trail is organised as follows:

- source recovery: `SOURCE_SCAN_REPORT.md`, `SOURCE_AVAILABILITY_LEDGER.md`;
- claim provenance: `THEOREM_SOURCE_MAP.csv`, `FORMULA_SOURCE_MAP.csv`, `COUNTEREXAMPLE_SOURCE_MAP.csv`;
- amendments and supersession: `AMENDMENT_DECISION_LEDGER.md`, `CONTRADICTION_AND_SUPERSESSION_LEDGER.md`;
- prior art and references: `PRIOR_ART_AUDIT.md`, `CITATION_VERIFICATION_LEDGER.csv`;
- scope and risk: `NOVELTY_AND_SCOPE_LOCK.md`, `REFEREE_RISK_AND_RESPONSE_LEDGER.md`;
- reproducibility: `REPRODUCIBILITY_PROTOCOL.md`, `ENVIRONMENT_SPECIFICATION.txt`, `MANIFEST.sha256`.
- release gates: `RELEASE_GATE_AUDIT.md`, `BUILD_AND_VISUAL_QA_REPORT.md`, `FRESH_EXTRACTION_REPORT.md`.

Evidence labels are restricted to `PROVED`, `VERIFIED-EXACT`, `VERIFIED-BYTE`, `MEASURED` with a sample size, `FALSIFIED`, `CONJECTURE`, and `UNAVAILABLE`.
