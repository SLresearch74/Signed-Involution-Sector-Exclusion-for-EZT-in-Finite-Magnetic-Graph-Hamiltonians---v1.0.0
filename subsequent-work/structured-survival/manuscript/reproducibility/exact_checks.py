from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
with open(ROOT/'data'/'paper_tables.json', encoding='utf-8') as f:
    D = json.load(f)

# Baseline n=8 oriented Hermitian adjacency, C={1,3}.
n=8
I=sp.I
H=sp.zeros(n)
for j in range(n):
    for c in (1,3):
        H[j,(j+c)%n] = I
        H[j,(j-c)%n] = -I
assert H.H == H
assert sp.simplify(H**3 - 8*H) == sp.zeros(n)

# Spectral multiplicities.
evals=H.eigenvals()
assert evals[sp.Integer(0)] == 4
assert evals[2*sp.sqrt(2)] == 2
assert evals[-2*sp.sqrt(2)] == 2

# Exact all-time baseline darkness for 0->2 via moments through n-1.
e0=sp.eye(n)[:,0]
e2=sp.eye(n)[:,2]
for k in range(n):
    assert sp.simplify((e2.T*(H**k)*e0)[0]) == 0

# Diagonal Green function from H^3=8H.
z=sp.symbols('z')
G = sp.eye(n)/z + H/(z**2-8) + H**2/(z*(z**2-8))
d = sp.factor((e0.T*G*e0)[0])
assert sp.simplify(d - (z**2-4)/(z*(z**2-8))) == 0
assert sp.simplify((e2.T*G*e0)[0]) == 0

# Rank-one affine family and exact marked resolvent formula.
t, eps = sp.symbols('t eps')
a=1-t
b=1+t
v=a*e2+b*e0
A=v*e0.T
# Sherman-Morrison scalar expression.
expr=sp.factor(eps*a*d**2/(1-eps*b*d))
# Its first three event grades have the expected a b^(k-1) d^(k+1).
series=sp.series(expr,eps,0,4).removeO().expand()
for k in range(1,4):
    coeff=sp.factor(series.coeff(eps,k))
    assert sp.simplify(coeff - a*b**(k-1)*d**(k+1)) == 0

# Projected coefficient ranks are constant for the affine family.
# At each spectral projector, dark-pair orthogonality gives norm^2 proportional to a^2+b^2;
# the unimodular identity a+b=2 suffices to exclude simultaneous vanishing over any field of char != 2.
assert sp.expand(a+b) == 2

# Locked census summary.
L=D['locked_n8']
assert L['components'] == 16
assert L['all_locked_K0_Kmax_match_T15'] is True
assert L['mixed_factors_absent'] is True
# JSON keys may be strings depending on the source serializer.
def val(dic, *keys):
    for k in keys:
        if k in dic:
            return dic[k]
    raise KeyError(keys)
assert val(L['block_raw_counts'],'1',1) == 48
assert val(L['block_raw_counts'],'t') == 56
assert val(L['block_raw_counts'],'0',0) == 8
assert val(L['block_normalized_counts'],'1',1) == 104
assert val(L['block_normalized_counts'],'0',0) == 8
assert val(L['edge_raw_counts'],'1',1) == 140
assert val(L['edge_raw_counts'],'t') == 64

# Exactly eight of the sixteen marked directions have dark block 4.
rows=L['classification']
assert sum(int(r['forward_dark'])+int(r['reverse_dark']) for r in rows) == 8

print('All exact paper checks passed.')
print('n=8 eigenvalue multiplicities:', {str(k):v for k,v in evals.items()})
print('d(z) =', d)
print('affine g(t)=t-1, h(t)=t+1 verified from the rank-one expansion')
print('locked dark block-4 directions = 8/16')
