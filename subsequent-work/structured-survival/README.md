# From Zero Transfer to Structured Survival on Oriented-Circulant Baselines

**Zach Medford and Joshua Barker**

Prepublication manuscript supplied 6 September 2026.

[Read the manuscript](manuscript/main.pdf) | [LaTeX source](manuscript/main.tex) | [Citation metadata](CITATION.cff)

This package studies prescribed marked rank-one perturbations of known oriented-circulant zero-transfer baselines. It combines standard observability, invariant-kernel, polynomial-content and Fourier methods, and includes a bounded exact seven-block classification on the eight-site baseline. The manuscript makes no priority claim for the worked classification and does not claim a new general observability or cyclotomic theory.

## Contents

- `manuscript/`: the supplied PDF, LaTeX, bibliography, figures, figure generator, compact paper tables and paper-facing exact checks. These files are preserved byte for byte from the supplied prepublication bundle.
- `supplementary/T17_PRIME_POWER_ARITHMETIC_TAXONOMY/`: the complete frozen T17 machine-readable ledger, verification outputs and accompanying computation reports.
- `supplementary/_T17_WORK/`: the original symbolic generator and independent standard-library verifier.
- `supplementary/T15_FREEZE_REPAIRS_RESPONSE_PROFILE/` and `supplementary/T16_ARITHMETIC_BLOCK_DARKNESS/`: the exact upstream JSON inputs consumed by the T17 generator.
- `SHA256SUMS` and `verify_archive.py`: integrity checks and direct checks that the manuscript summary agrees with the full ledger.
- `VALIDATION.md`: checks performed for this repository addition.

The old T17 readiness and prior-art reports are retained as historical computation records. Their drafting instructions and provisional novelty assessments predate the final manuscript; the supplied September manuscript controls the current presentation and claims. References in those reports to `_MV1_WORK/deps` or a separate T16 verifier describe the original workspace. The standalone T17 commands below use the included inputs and do not require those historical directories.

## Reproduce the exact results

Run these commands from this directory using Python 3.12 and SymPy 1.14.0:

```sh
python -m pip install -r requirements-exact.txt
python verify_archive.py
python manuscript/reproducibility/exact_checks.py
python supplementary/_T17_WORK/verify_t17.py
```

The archive verifier needs only the Python standard library. It checks file hashes, both upstream input hashes, the compact census and all 16 directional classifications against the full T17 ledger. The paper-facing script checks the eight-site matrix identities, spectrum, darkness, diagonal Green function and affine rank-one expansion. The independent T17 verifier additionally checks 192 Gaussian-rational physical coefficients and exact Fourier pole signs.

To regenerate the full symbolic ledger, work in a disposable copy of this directory:

```sh
python supplementary/_T17_WORK/t17_exact.py
python supplementary/_T17_WORK/verify_t17.py
```

The symbolic generator recomputes the locked regression, eight graph-realized families, formal controls and 888 prime-local nonvanishing cases. It overwrites the T17 JSON, and the independent verifier overwrites its verification JSON. The standard-library verifier alone reads the stored count of 888; it does not recompute those prime-local cases.

Frozen files are included so a reader can distinguish reproduction from the original evidence. Python/SymPy version changes or platform newline conventions can change byte hashes even when parsed JSON values agree. Validate the original archive before regeneration and compare parsed results as well as bytes. Repository attributes preserve the uploaded bytes on checkout.

## Figures and manuscript

The supplied figures and PDF are ready to read. To redraw the figures:

```sh
python -m pip install -r requirements-figures.txt
python manuscript/figures/generate_figures.py
```

To compile the manuscript, install LaTeX with `latexmk`, `biber` and `biblatex`, then:

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Floating-point values are used only for illustrations; no plot is used as proof.

## Exact ledger and reported census

The manuscript's compact table names `T17_MACHINE_READABLE.json` and records its SHA-256:

```text
ed4e31ea0d45b7104d7b03ecd1d5df63295bc0b7a8e54c78462edf23e055fc33
```

The frozen census contains 16 marked components, 112 block generators and 204 arrow generators. Raw block counts are 48 unit, 56 proportional to t and 8 zero; after localization to D(t), there are 104 unit and 8 zero. Raw arrow counts are 140 unit and 64 proportional to t; all 204 become units on D(t). Eight of the 16 marked directions have dark block 4. These are bounded exact results, not claims of a complete classification beyond the prescribed families.

## Citation and archive status

Cite Zach Medford and Joshua Barker, *From Zero Transfer to Structured Survival on Oriented-Circulant Baselines*, prepublication version dated 6 September 2026, with this repository's specific commit URL. Machine-readable metadata is in `CITATION.cff`.

No DOI has yet been assigned to this new manuscript/T17 package. A GitHub commit records the exact version but does not complete the checklist's DOI-deposit requirement. The earlier signed-involution paper's DOI is a different record and must not be used as the DOI of this package. Target-journal formatting and a journal-specific data statement remain author submission tasks.

## Authorship and assistance

The supplied manuscript contains the authors' disclosure naming ChatGPT and Gemini and assigning responsibility for the mathematics, computations, citations, generated code/data and dissemination to the human authors. Affiliations, ORCIDs and contact details have not been invented.

Code follows the repository's [MIT License](../../LICENSE). The repository README states the terms for manuscript, figure and data reuse; this addition introduces no separate license.
