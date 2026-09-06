# Reproducibility

## Requirements

- Python 3
- SymPy
- NumPy
- Matplotlib
- NetworkX
- LaTeX with `latexmk`, `biber` and `biblatex`

## Exact checks

```bash
python reproducibility/exact_checks.py
```

This checks the paper-facing eight-site adjacency, `H0^3=8H0`, spectral multiplicities, finite baseline darkness, the exact diagonal Green function, the first three coefficients of the affine rank-one response, and the compact locked-census summary.

## Figures

```bash
python figures/generate_figures.py
```

The manuscript uses the resulting vector-PDF figures.

## Manuscript

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

The bibliography is processed by `biber` through `latexmk`.

## Source data

`data/paper_tables.json` is a compact extract prepared from `T17_MACHINE_READABLE.json`. Its recorded SHA-256 identifies the exact source ledger used to prepare the manuscript tables.
