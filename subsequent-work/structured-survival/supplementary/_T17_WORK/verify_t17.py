"""Independent standard-library integrity and Gaussian-rational physical checks."""
from fractions import Fraction as F
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'T17_PRIME_POWER_ARITHMETIC_TAXONOMY'
REQUIRED=['T16_FREEZE_REPAIRS','MAIN_FINDINGS','GRAPH_REALIZABILITY_AUDIT','COMMON_FUTURE_DIVISOR_THEOREM',
    'ZERO_UNIT_NONCONSTANT_CLASSIFICATION','EDGE_GENERATOR_TAXONOMY','BLOCK_GENERATOR_TAXONOMY',
    'PRIME_VS_PRIMEPOWER','SIGNATURE_CANDIDATES','SIGNATURE_FALSIFICATION_LEDGER','ACTUAL_GRAPH_ATLAS',
    'FORMAL_CONTROL_ATLAS','N8_FINAL_CLASSIFICATION','FACTOR_PROVENANCE_TAXONOMY','CORE_THEOREM_MAP',
    'PRIOR_ART_MAP','PAPER_READINESS']

def gauss(a=0,b=0): return (F(a),F(b))
ZERO=gauss()
def add(v,w): return (v[0]+w[0],v[1]+w[1])
def mul(v,w): return (v[0]*w[0]-v[1]*w[1],v[0]*w[1]+v[1]*w[0])
def scale(v,a): return (v[0]*a,v[1]*a)
def matmul(A,B):
    return [[sumg(mul(A[i][k],B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sumg(items):
    result=ZERO
    for v in items: result=add(result,v)
    return result
def cyclotomic_zero(terms,N):
    modulus={0:1,4:1} if N==8 else {0:1,6:-1,12:1}
    degree=max(modulus)
    p=[0]*(max(terms)+1)
    for k,v in terms.items():p[k]+=v
    for k in range(len(p)-1,degree-1,-1):
        c=p[k]
        for j,v in modulus.items():p[k-degree+j]-=c*v
    return not any(p)
def polynomial(s,tau):
    def visit(v):
        if isinstance(v,ast.Constant) and isinstance(v.value,int):return F(v.value)
        if isinstance(v,ast.Name) and v.id=='t':return F(tau)
        if isinstance(v,ast.UnaryOp) and isinstance(v.op,ast.USub):return -visit(v.operand)
        if isinstance(v,ast.BinOp):
            a,b=visit(v.left),visit(v.right)
            if isinstance(v.op,ast.Add):return a+b
            if isinstance(v.op,ast.Sub):return a-b
            if isinstance(v.op,ast.Mult):return a*b
            if isinstance(v.op,ast.Div):return a/b
            if isinstance(v.op,ast.Pow) and b.denominator==1:return a**int(b)
        raise ValueError(ast.dump(v))
    return visit(ast.parse(s,mode='eval').body)

def main():
    for suffix in REQUIRED:
        path=OUT/f'T17_{suffix}.md'
        assert path.is_file() and path.stat().st_size>600, path
    data=json.loads((OUT/'T17_MACHINE_READABLE.json').read_text(encoding='utf-8'))
    for rel,sha in data['input_hashes'].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha
    assert not data['PP_matrix_constructed']
    assert len(data['mandatory_falsification_suite'])==14
    locked=data['locked_n8']
    assert len(locked['components'])==16
    assert sum(len(c['blocks']) for c in locked['components'])==112
    assert sum(len(c['edges']) for c in locked['components'])==204
    assert locked['earliest_unit_histogram']=={'0':60,'1':32,'2':8,'3':4}
    assert sum(c['K0']==[4] for c in locked['components'])==8
    for c in locked['components']:
        assert c['K0']==c['Kmax']
        assert all(e['h_stratum_normalized']=='1' for e in c['edges'])
        if c['K0']: assert not any(e['source_block']==4 for e in c['edges'])
    physical_checks=0
    for fam in data['new_graph_atlas']:
        assert fam['graph_realized_boolean'] and fam['stratum_localization_set']==['1']
        assert len(fam['blocks'])==3 and len(fam['edges'])==9
        n=fam['n'];ell=fam['target'];c=8 if n==8 else 3
        N=8 if n==8 else 36
        # Check the negative pole's exact Fourier expression against a positive
        # real cyclotomic expression: 2(zeta8+zeta8^-1) or zeta36^3+zeta36^-3.
        terms={1:2,7:2} if n==8 else {3:1,33:1}
        for step in fam['connection_set']:
            for exponent,sgn in [(step*N//n,1),((-step*N//n)%N,-1)]:
                power=N//4+exponent
                terms[power]=terms.get(power,0)+sgn
        assert cyclotomic_zero(terms,N)
        H=[[ZERO for _ in range(n)] for _ in range(n)]
        for j in range(n):
            for k in fam['connection_set']:
                H[j][(j+k)%n]=gauss(0,1);H[j][(j-k)%n]=gauss(0,-1)
        H2=matmul(H,H);H3=matmul(H2,H)
        assert H3==[[scale(v,c) for v in row] for row in H]
        for zs in [5,6]:
            # Rational resolvent polynomial in H, independent of radical projectors.
            G=[[add(add(gauss(F(int(i==j),zs)),scale(H[i][j],F(1,zs*zs-c))),
                scale(H2[i][j],F(1,zs*(zs*zs-c)))) for j in range(n)] for i in range(n)]
            ZH=[[add(gauss(zs if i==j else 0),scale(H[i][j],-1)) for j in range(n)] for i in range(n)]
            assert matmul(ZH,G)==[[gauss(int(i==j)) for j in range(n)] for i in range(n)]
            rho=G[0][0]
            assert G[ell][0]==ZERO and G[ell][ell]==rho
            for spec in fam['specializations']:
                tau=spec['t'];a=polynomial(fam['declared_events'][0]['a'],tau);b=polynomial(fam['declared_events'][0]['b'],tau)
                assert a!=0 or b!=0
                dark=[0,1,2] if a==0 else []
                assert spec['K0']==dark==spec['Kmax']
                assert len(spec['G_nz'])==(9 if b else 0)
                for block in fam['blocks']:
                    assert (polynomial(block['g_stratum_normalized'],tau)==0)==(a==0)
                for edge in fam['edges']:
                    assert (polynomial(edge['h_stratum_normalized'],tau)==0)==(b==0)
                vec=[[G[j][0]] for j in range(n)]
                expected=rho
                for grade in range(1,4):
                    Avec=[[ZERO] for _ in range(n)]
                    Avec[0][0]=scale(vec[0][0],b);Avec[ell][0]=scale(vec[0][0],a)
                    vec=matmul(G,Avec)
                    expected=mul(expected,rho)
                    assert vec[ell][0]==scale(expected,a*b**(grade-1))
                    physical_checks+=1
    assert len(data['new_graph_atlas'])==8
    assert data['formal_control_atlas']['prime_nonvanishing']['exact_mask_displacement_cases']==888
    report={'status':'VERIFIED-EXACT','required_files':18,'locked_components':16,'locked_blocks':112,'locked_edges':204,
        'new_graph_baselines':2,'new_marked_families':8,'new_blocks':24,'new_edges':72,
        'independent_Gaussian_rational_physical_coefficients_checked':physical_checks,
        'prime_local_nonvanishing_cases':888,'mandatory_controls':14,'exact_Fourier_pole_sign_checks':True,'PP_constructed':False,
        'machine_sha256':hashlib.sha256((OUT/'T17_MACHINE_READABLE.json').read_bytes()).hexdigest()}
    (OUT/'T17_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
