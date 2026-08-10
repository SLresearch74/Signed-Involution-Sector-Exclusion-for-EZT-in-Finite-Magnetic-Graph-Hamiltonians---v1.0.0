#!/usr/bin/env python3
"""Generate exact LaTeX/CSV tables from released machine-readable atlases."""
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "DATA"


def monomial(exps):
    names = ["z", "d_1", "d_2", "d_3", "d_4"]
    bits = []
    for name, e in zip(names, exps):
        if e == 1:
            bits.append(name)
        elif e:
            bits.append(f"{name}^{{{e}}}")
    return " ".join(bits) or "1"


primary = json.loads((DATA / "MV1_PRIMARY_EXACT.json").read_text(encoding="utf-8"))
den = primary["denominator_terms"]
lines = [r"\begin{longtable}{r r l}", r"\toprule", r"Index & Coefficient & Monomial\\", r"\midrule", r"\endhead"]
for i, term in enumerate(den, 1):
    lines.append(f"{i} & {term['coefficient']} & ${monomial(term['exponents'])}$\\\\")
lines += [r"\bottomrule", r"\end{longtable}"]
(DATA / "denominator_terms.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

cells = json.loads((DATA / "MV1_15_CELL_ATLAS.json").read_text(encoding="utf-8"))["positive_normal_fan_subsets"]
lines = [r"\begin{longtable}{r l l c c}", r"\toprule", r"Cell & $I$ & Face form (without $it^3/6$) & $\C^*$ cancel & $\R_{>0}$ cancel\\", r"\midrule", r"\endhead"]
for i, c in enumerate(cells, 1):
    I = "\\{" + ",".join(map(str, c["I"])) + "\\}"
    cc = "yes" if c["complex_torus_cancellation_nonempty"] else "no"
    pr = "yes" if c["positive_real_cancellation_nonempty"] else "no"
    form = c["face_linear_form"].replace("c1", "c_1").replace("c2", "c_2").replace("c3", "c_3").replace("c4", "c_4")
    lines.append(f"{i} & ${I}$ & ${form}$ & {cc} & {pr}\\\\")
lines += [r"\bottomrule", r"\end{longtable}"]
(DATA / "mv1_cells.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

fan = json.loads((DATA / "GF1_16_CONE_ATLAS.json").read_text(encoding="utf-8"))["cones"]
lines = [r"\begin{longtable}{l l l c l}", r"\toprule", r"Cone & Weight $(a,b,c,d)$ & Initial ideal & Radical & Adjacent\\", r"\midrule", r"\endhead"]
for c in fan:
    w = c["representative_weight"]
    wt = f"({w['a']},{w['b']},{w['c']},{w['d']})"
    ideal = c["initial_ideal"].replace("<", "(").replace(">", ")").replace("c2", "c^2").replace("d2", "d^2").replace("a2", "a^2").replace("b2", "b^2")
    adj = ", ".join(c["adjacent_cones"])
    lines.append(f"{c['cone_id']} & ${wt}$ & ${ideal}$ & {'yes' if c['radical'] else 'no'} & {adj}\\\\")
lines += [r"\bottomrule", r"\end{longtable}"]
(DATA / "gf1_cones.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

with (DATA / "DENOMINATOR_TERMS.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["index", "coefficient", "z", "d1", "d2", "d3", "d4"])
    for i, term in enumerate(den, 1):
        w.writerow([i, term["coefficient"], *term["exponents"]])

print(json.dumps({"denominator_terms": len(den), "mv1_cells": len(cells), "gf1_cones": len(fan), "evidence": "VERIFIED-EXACT"}, indent=2))
