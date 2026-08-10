#!/usr/bin/env python3
"""Dependency-free exact checks for the integrated M3A Paper II release.

All arithmetic is integral or rational.  The discrepancy fixture perturbs the
locked Hamiltonian and reruns the same cofactor and moment routes; its detection
result is therefore computed, not hard-coded.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NVAR = 5  # z,d1,d2,d3,d4
ZERO = (0,) * NVAR

H0 = [
    [0, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1, -1],
    [1, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, -1],
    [0, 1, -1, 1, -1, 0],
]


def padd(a, b):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + c
        if out[m] == 0:
            del out[m]
    return out


def pneg(a):
    return {m: -c for m, c in a.items()}


def pmul(a, b):
    out = {}
    for x, cx in a.items():
        for y, cy in b.items():
            m = tuple(x[i] + y[i] for i in range(NVAR))
            out[m] = out.get(m, 0) + cx * cy
    return {m: c for m, c in out.items() if c}


def pc(c):
    return {} if not c else {ZERO: int(c)}


def pv(i, c=1):
    e = [0] * NVAR
    e[i] = 1
    return {tuple(e): c}


def parity(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2 else 1


def det_poly(a):
    n = len(a)
    total = {}
    for p in itertools.permutations(range(n)):
        term = pc(parity(p))
        for i, j in enumerate(p):
            term = pmul(term, a[i][j])
            if not term:
                break
        total = padd(total, term)
    return total


def resolvent_matrix(h0):
    out = []
    for i in range(6):
        row = []
        for j in range(6):
            q = pc(-h0[i][j])
            if i == j:
                q = padd(q, pv(0))
                if 1 <= i <= 4:
                    q = padd(q, pneg(pv(i)))
            row.append(q)
        out.append(row)
    return out


def selected_cofactor(h0):
    a = resolvent_matrix(h0)
    minor = [[a[i][j] for j in range(6) if j != 5] for i in range(6) if i != 0]
    return pneg(det_poly(minor))  # (-1)^(0+5)


def expected_numerator():
    # L(z^2+2z)+2Q(z+1)+R, with
    # L=d1-d2+d3-d4, Q=d2*d4-d1*d3,
    # R=d1*d2*(d3-d4)+d3*d4*(d1-d2).
    z = pv(0)
    ds = [None] + [pv(i) for i in range(1, 5)]
    L = padd(padd(ds[1], pneg(ds[2])), padd(ds[3], pneg(ds[4])))
    Q = padd(pmul(ds[2], ds[4]), pneg(pmul(ds[1], ds[3])))
    R = padd(pmul(pmul(ds[1], ds[2]), padd(ds[3], pneg(ds[4]))),
             pmul(pmul(ds[3], ds[4]), padd(ds[1], pneg(ds[2]))))
    return padd(padd(pmul(L, padd(pmul(z, z), {tuple([1,0,0,0,0]): 2})),
                     {m: 2*c for m, c in pmul(Q, padd(z, pc(1))).items()}), R)


def matmul_poly(a, b):
    n, m, q = len(a), len(b[0]), len(b)
    out = [[{} for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(q):
            if not a[i][k]:
                continue
            for j in range(m):
                if b[k][j]:
                    out[i][j] = padd(out[i][j], pmul(a[i][k], b[k][j]))
    return out


def h_poly(h0):
    a = [[pc(h0[i][j]) for j in range(6)] for i in range(6)]
    for i in range(1, 5):
        a[i][i] = padd(a[i][i], pv(i))
    return a


def moment_polys(h0, depth=8):
    h = h_poly(h0)
    p = [[pc(int(i == j)) for j in range(6)] for i in range(6)]
    ans = []
    for _ in range(depth + 1):
        ans.append(p[5][0])
        p = matmul_poly(p, h)
    return ans


# Gaussian rationals are (real,imaginary).
def gadd(a, b): return (a[0] + b[0], a[1] + b[1])
def gmul(a, b): return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def gscale(a, q): return (a[0]*q, a[1]*q)
G0 = (Fraction(0), Fraction(0))
G1 = (Fraction(1), Fraction(0))
GI = (Fraction(0), Fraction(1))


def smul(a, b, cap=8):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i+j <= cap:
                out[i+j] = gadd(out.get(i+j, G0), gmul(x, y))
    return {k: v for k, v in out.items() if v != G0}


def sadd(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = gadd(out.get(k, G0), v)
        if out[k] == G0:
            del out[k]
    return out


def smatmul(a, b, cap=8):
    out = [[{} for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for k in range(len(b)):
            for j in range(len(b[0])):
                out[i][j] = sadd(out[i][j], smul(a[i][k], b[k][j], cap))
    return out


def path_amplitude(dseries, ct, cap=8, h0=None):
    h0 = H0 if h0 is None else h0
    h = [[({0: (Fraction(h0[i][j]), Fraction(0))} if h0[i][j] else {})
          for j in range(6)] for i in range(6)]
    for r in range(4):
        h[r+1][r+1] = sadd(h[r+1][r+1], dseries[r])
    p = [[({0: G1} if i == j else {}) for j in range(6)] for i in range(6)]
    amp = {}
    minus_i = (Fraction(0), Fraction(-1))
    phase = G1
    ctpow = G1
    for k in range(cap + 1):
        factor = gscale(gmul(phase, ctpow), Fraction(1, math.factorial(k)))
        for deg, val in p[5][0].items():
            n = deg + k
            if n <= cap:
                amp[n] = gadd(amp.get(n, G0), gmul(factor, val))
        p = smatmul(p, h, cap)
        phase = gmul(phase, minus_i)
        ctpow = gmul(ctpow, ct)
    return {k: v for k, v in amp.items() if v != G0}


def gs(q): return {q: G1}


def qstr(g):
    def f(x): return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return {"real": f(g[0]), "imag": f(g[1])}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(fixture=False):
    h = [row[:] for row in H0]
    if fixture:
        h[2][5] = h[5][2] = 1  # controlled sign perturbation
    cofactor = selected_cofactor(h)
    target = expected_numerator()
    moments = moment_polys(h, 8)
    cofactor_match = cofactor == target

    # Coefficients at the support boundary k=j+2.
    boundary = {}
    signs = [1, -1, 1, -1]
    for r in range(4):
        e = [0]*NVAR; e[r+1] = 1
        boundary[f"d{r+1}|k3"] = moments[3].get(tuple(e), 0)
    endpoint_zeros = all(not any(sum(m[1:]) == j and c for m, c in moments[k].items())
                         for k in range(9) for j in range(1, 9) if k < j+2)

    # ARC1 control: d=(s+s^3,0,-s,0), t=c_t s.
    arc_d = [sadd(gs(1), gs(3)), {}, {1: (Fraction(-1), Fraction(0))}, {}]
    arc_symbolic_c1 = path_amplitude(arc_d, G1, 8, h)
    arc_cancel = path_amplitude(arc_d, (Fraction(0), Fraction(-2)), 8, h)

    # GF1 control: d=(s,s^3,-s,s^4), t=c_t s.
    gf_d = [gs(1), gs(3), {1: (Fraction(-1), Fraction(0))}, gs(4)]
    gf_cancel = path_amplitude(gf_d, (Fraction(0), Fraction(2)), 8, h)

    # External exact atlases, copied into this release, are structurally checked.
    fan_path = ROOT / "DATA" / "GF1_16_CONE_ATLAS.json"
    cells_path = ROOT / "DATA" / "MV1_15_CELL_ATLAS.json"
    fan = json.loads(fan_path.read_text(encoding="utf-8"))
    cells = json.loads(cells_path.read_text(encoding="utf-8"))
    fan_ok = (fan["cone_count"] == 16 and len(fan["cones"]) == 16 and
              sum(not c["radical"] for c in fan["cones"]) == 4 and
              all(c["hilbert_polynomial"] == "2n+1" for c in fan["cones"]))
    cells_list = cells["positive_normal_fan_subsets"]
    cells_ok = len(cells_list) == 15 and {tuple(x["I"]) for x in cells_list} == {
        s for r in range(1,5) for s in itertools.combinations(range(1,5), r)}

    baseline_ok = all(x == 0 for x in [moments[k].get(ZERO, 0) for k in range(9)])
    normal_expected = (cofactor_match and endpoint_zeros and baseline_ok and
                       list(boundary.values()) == signs and fan_ok and cells_ok and
                       arc_cancel.get(6, G0) == G0 and arc_cancel.get(7, G0) == (Fraction(4,5), Fraction(0)) and
                       gf_cancel.get(6, G0) == G0 and gf_cancel.get(7, G0) == (Fraction(-32,15), Fraction(0)))

    if fixture:
        detected = not cofactor_match and boundary != {f"d{r+1}|k3": signs[r] for r in range(4)}
        payload = {
            "evidence": "FALSIFIED",
            "fixture": "H0[2,5] and H0[5,2] sign changed from -1 to +1",
            "cofactor_route_detected": not cofactor_match,
            "moment_route_detected": list(boundary.values()) != signs,
            "discrepancy_detected": detected,
        }
        out = ROOT / "DATA" / "discrepancy_detection.json"
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        if not detected:
            raise SystemExit("discrepancy fixture was not independently detected")
        return payload

    payload = {
        "evidence": "VERIFIED-EXACT" if normal_expected else "FALSIFIED",
        "locked_cofactor_matches": cofactor_match,
        "denominator_term_count": len(det_poly(resolvent_matrix(h))),
        "endpoint_support_zeros": endpoint_zeros,
        "baseline_moments_zero_through_k8": baseline_ok,
        "minimal_layer_d1_to_d4": list(boundary.values()),
        "arc_control_ct_1_s6": qstr(arc_symbolic_c1.get(6, G0)),
        "arc_control_ct_minus_2i_s6": qstr(arc_cancel.get(6, G0)),
        "arc_control_ct_minus_2i_s7": qstr(arc_cancel.get(7, G0)),
        "gf1_control_ct_2i_s6": qstr(gf_cancel.get(6, G0)),
        "gf1_control_ct_2i_s7": qstr(gf_cancel.get(7, G0)),
        "gf1_atlas": {"verified": fan_ok, "sha256": sha(fan_path)},
        "mv1_atlas": {"verified": cells_ok, "sha256": sha(cells_path)},
    }
    out = ROOT / "EXPECTED" / "paper_verification.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not normal_expected:
        raise SystemExit("one or more exact checks failed")
    return payload


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", action="store_true", help="run the controlled discrepancy fixture")
    args = ap.parse_args()
    print(json.dumps(run(args.fixture), indent=2))
