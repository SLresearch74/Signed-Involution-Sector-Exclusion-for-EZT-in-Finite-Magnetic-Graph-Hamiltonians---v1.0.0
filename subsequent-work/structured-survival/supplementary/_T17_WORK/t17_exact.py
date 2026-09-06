"""Exact T17 certificates. Consumes terminal T16 ledgers; builds no PP matrix."""
from __future__ import annotations
import hashlib
import json
import math
from collections import Counter
from functools import lru_cache
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '_MV1_WORK' / 'deps'))
import sympy as sp

OUT = ROOT / 'T17_PRIME_POWER_ARITHMETIC_TAXONOMY'
t, z, X = sp.symbols('t z X')
K8 = sp.QQ.algebraic_field(sp.I, sp.sqrt(2))

def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))

def digest(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()

def clean(v):
    return sp.cancel(sp.expand(v))

def zeros(m):
    return all(clean(v) == 0 for v in m)

@lru_cache(None)
def parse(s):
    return sp.sympify(s, locals={'t': t, 'z': z, 'I': sp.I})

def content(values, domain=K8):
    g = sp.Poly(0, t, domain=domain)
    for v in values:
        g = sp.gcd(g, sp.Poly(v, t, domain=domain))
        if g.degree() == 0:
            return sp.Integer(1)
    return sp.Integer(0) if g.is_zero else g.monic().as_expr()

def normalized(v, invert_t=False):
    if v == 0:
        return sp.Integer(0)
    p = sp.Poly(v, t, extension=True)
    if invert_t:
        k = min(e[0] for e, c in p.terms())
        p = sp.Poly(sp.cancel(p.as_expr()/t**k), t, extension=True)
    return p.monic().as_expr()

def closure(initial, edges):
    keep = set(initial)
    while True:
        nxt = {j for j in keep if all(v in keep for u,v in edges if u == j)}
        if nxt == keep:
            return sorted(keep)
        keep = nxt

def freeze_regression():
    d = read('T16_ARITHMETIC_BLOCK_DARKNESS/T16_MACHINE_READABLE.json')
    old = read('T15_FREEZE_REPAIRS_RESPONSE_PROFILE/T15_MACHINE_READABLE.json')
    comps = d['n8_arithmetic_recovery']['components']
    assert len(comps) == 16
    assert Counter(b['raw_generator_g'] for c in comps for b in c['blocks']) == {'1':48,'t':56,'0':8}
    assert Counter(e['raw_edge_generator_h'] for c in comps for e in c['edges']) == {'1':140,'t':64}
    assert len(old['n8_profile_classification']['families']) == 16
    result = []
    hist = Counter()
    for c, prev in zip(comps, old['n8_profile_classification']['families']):
        blocks = []
        for b in c['blocks']:
            raw = parse(b['raw_generator_g'])
            grades = b['final_polynomial_coefficients']
            all_coeff = [parse(v) for h in grades for v in h['coefficients_in_z']]
            # Terminal arithmetic only: check divisibility and a sharp early witness.
            if raw == 0:
                assert all(v == 0 for v in all_coeff)
                earliest = None
            else:
                assert all(sp.rem(sp.Poly(v,t,domain=K8),sp.Poly(raw,t,domain=K8)).is_zero for v in all_coeff)
                earliest = next((h['grade'] for h in grades if normalized(content([parse(v) for v in h['coefficients_in_z']]),True) == 1),None)
                assert earliest is not None
                assert content([parse(v) for v in grades[earliest]['coefficients_in_z']]) == raw
                hist[str(earliest)] += 1
            assert str(normalized(raw, True)) == b['normalized_stratum_generator']
            blocks.append({'block_id': b['block_id'], 'g_raw':str(raw), 'g_stratum_normalized':str(normalized(raw,True)),
                'g_class_zero_unit_nonconstant':'zero' if raw == 0 else 'unit',
                'g_factorization':[],'g_zero_locus':'Sigma' if raw == 0 else 'empty',
                'g_arithmetic_certificate': b['arithmetic_derivation_ledger'],
                'common_future_divisor_certificate':'All terminal coefficients zero' if raw == 0 else 'All coefficients divisible by raw g; earliest grade has exactly that content',
                'earliest_unit_certificate':earliest})
        edges = []
        for e in c['edges']:
            vals = [parse(v) for v in e['arithmetic_derivation_ledger']['final_z_coefficients']]
            assert str(content(vals)) == e['raw_edge_generator_h']
            assert normalized(content(vals), True) == 1
            edges.append({'edge_id': e['edge_id'], 'source_block':e['source_block'],'target_block':e['target_block'],
                'h_raw':e['raw_edge_generator_h'],'h_stratum_normalized':'1','h_class_zero_unit_nonconstant':'unit',
                'h_factorization':[],'h_zero_locus':'empty','h_arithmetic_certificate':e['arithmetic_derivation_ledger']})
        zero_ids = [b['block_id'] for b in blocks if b['g_stratum_normalized']=='0']
        graph = [(e['source_block'],e['target_block']) for e in edges]
        surv = closure(zero_ids,graph)
        assert zero_ids == c['specialization']['K0_from_generators']
        assert surv == c['specialization']['Kmax_from_graph']
        assert c['specialization']['T15_crosscheck']
        # Compare actual T15 records, not only T16's stored boolean.
        old_text = prev['identity']
        assert c['source'] == prev['source'] and c['target'] == prev['target']
        assert c['component_id'] == f"({old_text['x']},{old_text['y']},{old_text['direction']})"
        assert zero_ids == prev['specialized_decomposable_K0']['locked_nonzero']
        assert surv == prev['specialized_Kmax']['locked_nonzero']
        assert graph == [(e['source_block'],e['target_block']) for e in prev['specialized_nonzero_declared_edge_graph']['locked_nonzero']]
        # T15 stores the same profile under its structured residual fields.
        marked = c['Song_to_recurrence_assembly']['T12_marked_certificate']
        pred = ((marked['orientation_type']=='variable_ket_x' and marked['chi4']==-1)
                or (marked['orientation_type']!='variable_ket_x' and c['source']==2))
        assert zero_ids == ([4] if pred else [])
        result.append({'component_id':c['component_id'],'n':8,'connection_set':[1,3],
            'graph_realized_boolean':True,'graph_realization_certificate':'Inherited locked graph; rechecked baseline n8 certificate in new_graph_atlas',
            'Song_fibres':c['Song_fibres'],'marked_Song_values':c['marked_Song_values'],
            'orientation':old_text['direction'],'source':c['source'],'target':c['target'],
            'declared_events':c['event_labels'],'recombination_classes':'locked Construction A, T16 ledger',
            'stratum_id':'n8_locked_D_t','stratum_ideal':['0'],'stratum_localization_set':['t'],
            'stratum_coordinate_ring':'K8[t,t^-1]','reachability_stratum':c['reachability_stratum'],
            'marked_classification':marked,'blocks':blocks,'edges':edges,'K0':zero_ids,'G_nz':graph,'Kmax':surv,
            'direct_zero_forward_closed':not zero_ids or (parse(c['Song_to_recurrence_assembly']['compiled_output_numerators_a'][4])==0 and closure([4],graph)==[4]),
            'theorem_status':'VERIFIED-EXACT','prior_art_status':'PROVED-SYNTHESIS','paper_location':'main example and appendix ledger'})
    assert sum(len(c['blocks']) for c in result)==112
    return {'status':'VERIFIED-EXACT','block_raw_counts':{'1':48,'t':56,'0':8},'block_normalized_counts':{'1':104,'0':8},
        'edge_raw_counts':{'1':140,'t':64},'edge_normalized_counts':{'1':204},'earliest_unit_histogram':dict(hist),
        'all_locked_K0_Kmax_match_T15':True,'mixed_factors_absent':True,'components':result}

def rem(v,n):
    return sp.rem(sp.Poly(v,X,domain=sp.QQ),sp.Poly(sp.cyclotomic_poly(n,X),X)).as_expr()

def cycle_record(n, mask, r):
    q=n//math.gcd(r,n)
    p=next(iter(sp.factorint(n)))
    counts=[0]*q
    for m in mask:
        counts[m%q]+=1
    balanced=(not mask if q==1 else all(len({counts[j+k*(q//p)] for k in range(p)})==1 for j in range(q//p)))
    value=rem(sum(X**((m*r)%n) for m in mask),n)
    assert (value==0)==balanced
    return {'r':r,'additive_order':q,'collapsed_counts_mod_q':counts,'p_cycle_balanced':balanced,'Song_value':str(value)}

def baseline(n, connection, target, c, masks):
    H=sp.zeros(n)
    for j in range(n):
        for k in connection:
            H[j,(j+k)%n]=sp.I
            H[j,(j-k)%n]=-sp.I
    E=sp.eye(n)
    assert H==H.conjugate().T and H**3==c*H
    rt=sp.sqrt(c)
    poles=[sp.Integer(0),-rt,rt]
    P=[E-H**2/c,(H**2-rt*H)/(2*c),(H**2+rt*H)/(2*c)]
    assert zeros(sum(P,sp.zeros(n))-E)
    for j in range(3):
        assert zeros(P[j]**2-P[j]) and zeros(H*P[j]-poles[j]*P[j])
        assert int(sp.trace(P[j]))==len(masks[j])
        assert P[j][target,0]==0 and P[j][0,target]==0
        assert P[j][0,0]==P[j][target,target]==sp.Rational(len(masks[j]),n)
        for k in range(3):
            if j!=k: assert zeros(P[j]*P[k])
    N=sp.ilcm(n,4)
    eig=[]
    for m in range(n):
        eig.append(rem(X**(int(N)//4)*sum(X**((int(N)//n*k*m)%int(N))-X**((-int(N)//n*k*m)%int(N)) for k in connection),int(N)))
    assert len(set(map(str,eig)))==3
    for j,mask in enumerate(masks):
        assert all(eig[m]==eig[mask[0]] for m in mask)
        assert (eig[mask[0]]==0)==(j==0)
        if j: assert rem(eig[mask[0]]**2-c,int(N))==0
    assert rem(eig[masks[1][0]]+eig[masks[2][0]],int(N))==0
    positive_root = 2*(X+X**7) if n==8 else X**3+X**33
    assert rem(eig[masks[1][0]]+positive_root,int(N))==0
    assert rem(eig[masks[2][0]]-positive_root,int(N))==0
    records={str(j):[cycle_record(n,m,r) for r in range(n)] for j,m in enumerate(masks)}
    for j in range(3):
        assert records[str(j)][target]['Song_value']=='0'
    transports=[]
    for u in range(n):
        if math.gcd(u,n)==1:
            for j,mask in enumerate(masks):
                moved=sorted((u*m)%n for m in mask)
                # Actual mask transport, with simultaneous action on all marked values.
                for r in range(n):
                    val=parse(records[str(j)][r]['Song_value']).subs(sp.Symbol('X'),X)
                    assert rem(val.subs(X,X**u),n)==rem(sum(X**((m*r)%n) for m in moved),n)
                transports.append({'unit':u,'from_mask':j,'transported_mask':moved})
    Q=z*(z*z-c)
    q=[sp.Rational(len(m),n)/(z-p) for m,p in zip(masks,poles)]
    rho=clean(sum(q))
    # Matrix resolvent identity independently verifies the spectral rational functions.
    G=sum((Pj/(z-pj) for Pj,pj in zip(P,poles)),sp.zeros(n))
    assert zeros((z*E-H)*G-E)
    assert clean(G[0,0]-rho)==0 and clean(G[target,target]-rho)==0 and clean(G[target,0])==0
    cert={'n':n,'connection_set':connection,'source':0,'target':target,
        'coefficient_field':f'Q(zeta_{int(N)})','Song_subfield':f'Q(zeta_{n})',
        'cyclotomic_response_order':int(N),'H0_entries':[[str(v) for v in row] for row in H.tolist()],
        'H0_identity':f'H0^3={c} H0','Hermitian':True,'oriented_connection_disjoint_from_negative':not(set(connection)&{(-k)%n for k in connection}),
        'Song_fibres':[{'block_id':j,'pole':str(poles[j]),'mask':masks[j],'weight':str(sp.Rational(len(masks[j]),n)),'pole_cyclotomic_representation':str(eig[masks[j][0]])} for j in range(3)],
        'marked_Song_values':records,'additive_orders':{str(r):n//math.gcd(r,n) for r in range(n)},
        'p_cycle_classes':records,'Galois_transport':transports,
        'signed_Song_relations':'S_j(0)=|M_j|; S_j(target-source)=S_j(source-target)=0; all other values and compatible transports listed',
        'projector_Gram_on_source_target':[{'block_id':j,'matrix':[[str(Pj[0,0]),'0'],['0',str(Pj[target,target])]],'determinant':str(Pj[0,0]**2)} for j,Pj in enumerate(P)],
        'projector_checks':True,'resolvent_identity_check':True,'rho':str(rho),'fixed_denominator':str(Q),
        'graph_realized_boolean':True,'connected_baseline':math.gcd(n,*connection)==1}
    return cert,H,P,poles,q,rho,Q,G

def family(base, label, a, b):
    cert,H,P,poles,q,rho,Q,G=base
    n=cert['n']; ell=cert['target']; domain=sp.QQ.algebraic_field(sp.I,sp.sqrt(2 if n==8 else 3))
    assert content([a,b],domain)==1
    va=sp.zeros(n,1); va[ell]=a; va[0]=b
    bra=sp.zeros(1,n);bra[0]=1
    A=va*bra
    O=sp.Matrix([[clean(a*qj) for qj in q]])
    M=sp.Matrix(3,3,lambda j,k:clean(b*q[k]))
    # Exact physical contractions in the nonvanishing polynomial image frame.
    for j in range(3):
        assert clean((G*P[j]*va)[ell]-O[j])==0
        assert clean((bra*G*P[j]*va)[0]-b*q[j])==0
    rows=[O]
    for h in range(1,3):
        rows.append((rows[-1]*M).applyfunc(clean))
    blocks=[]
    for j in range(3):
        polys=[]
        for h in range(3):
            assert clean(rows[h][j]-a*b**h*rho**h*q[j])==0
            polys.append(sp.Poly(sp.cancel(rows[h][j]*Q**(h+1),extension=True),z,domain=domain.poly_ring(t)))
        g=content([v for p in polys for v in p.all_coeffs()],domain)
        assert g==normalized(a)
        blocks.append({'block_id':j,'g_raw':str(g),'g_stratum_normalized':str(g),
            'g_class_zero_unit_nonconstant':'zero' if g==0 else 'unit' if g==1 else 'nonconstant',
            'g_factorization':str(sp.factor(g)),'g_zero_locus':'Sigma' if g==0 else 'empty' if g==1 else f'V({g})',
            'g_arithmetic_certificate':{'finite_horizon':2,'numerators_by_grade':[str(p.as_expr()) for p in polys],
                'formula':'r_h,j=a*b^h*rho^h*q_j'},
            'common_future_divisor_certificate':'Each future contains a; grade 0 has content exactly a',
            'earliest_unit_certificate':0 if g==1 else None})
    edges=[]
    for j in range(3):
        for k in range(3):
            numerator=sp.Poly(sp.cancel(M[j,k]*Q,extension=True),z,domain=domain.poly_ring(t))
            h=content(numerator.all_coeffs(),domain)
            assert h==normalized(b)
            edges.append({'edge_id':f'E{k}_to_{j}','source_block':k,'target_block':j,
                'h_raw':str(h),'h_stratum_normalized':str(h),'h_class_zero_unit_nonconstant':'zero' if h==0 else 'unit' if h==1 else 'nonconstant',
                'h_factorization':str(sp.factor(h)),'h_zero_locus':'Sigma' if h==0 else 'empty' if h==1 else f'V({h})',
                'h_arithmetic_certificate':{'numerator':str(numerator.as_expr()),'formula':'b*q_source'}})
    specs=[]
    values=sorted(set([-1,0,1,2]+[int(v) for v in sp.solve(a,t)+sp.solve(b,t) if v.is_Integer]))
    for tau in values:
        At=A.subs(t,tau)
        assert At.rank()==1
        assert all((Pj*At).rank()==1 for Pj in P)
        dark=[j for j in range(3) if all(clean(row[j].subs(t,tau))==0 for row in rows)]
        graph=[(k,j) for j in range(3) for k in range(3) if clean(M[j,k].subs(t,tau))!=0]
        assert dark==([0,1,2] if a.subs(t,tau)==0 else [])
        assert closure(dark,graph)==dark
        # Independent direct physical Neumann series: first three event grades.
        phys=G[:,0]
        for order in range(1,4):
            phys=(G*At*phys).applyfunc(clean)
            assert clean(phys[ell,0]-a.subs(t,tau)*b.subs(t,tau)**(order-1)*rho**(order+1))==0
        specs.append({'t':tau,'rank_A':1,'projected_ranks':[1,1,1],'structured_reachable':[0,1,2],
            'K0':dark,'G_nz':graph,'Kmax':closure(dark,graph),'physical_Neumann_grades_1_to_3':True})
    return {'family_id':label,'baseline_certificate_id':f'n{n}','n':n,'connection_set':cert['connection_set'],
        'graph_realized_boolean':True,'graph_realization_certificate':cert,
        'Song_fibres':cert['Song_fibres'],'marked_Song_values':cert['marked_Song_values'],
        'additive_orders':cert['additive_orders'],'p_cycle_classes':cert['p_cycle_classes'],
        'Galois_transport':cert['Galois_transport'],'signed_Song_relations':cert['signed_Song_relations'],
        'coefficient_field':cert['coefficient_field'],'Song_subfield':cert['Song_subfield'],'parameter_ring':'K[t]',
        'stratum_id':'all_t','stratum_ideal':['0'],'stratum_localization_set':['1'],'stratum_coordinate_ring':'K[t]',
        'reachability_stratum':'All 3 coordinate blocks directly reached by nonzero input rho at every t; structured, not ordinary Kalman reachability',
        'source':0,'target':ell,'orientation':f'0_to_{ell}; bra=source',
        'declared_events':[{'id':'A','epsilon_degree':1,'a':str(a),'b':str(b),'matrix':'(a|target>+b|source>)<source|','rank':1}],
        'recombination_classes':'One recombined rank-one coefficient A(t); polynomial summands are not distinct declared events',
        'rank_certificate':'gcd(a,b)=1 and nonzero projector Gram determinants; projected image frames never vanish',
        'arithmetic_recurrence':{'Omega':[str(v) for v in O],'M':[[str(v) for v in row] for row in M.tolist()],
            'input':[str(rho)]*3,'future':'r_h,j=a*b^h*rho^h*q_j','finite_horizon':2,'PP_constructed':False},
        'blocks':blocks,'edges':edges,'K0':'all 3 iff a(t)=0; otherwise none',
        'G_nz':'complete directed graph including loops iff b(t)!=0; otherwise empty',
        'Kmax':'equals K0','specializations':specs,
        'exact_physical_transfer':'epsilon*a*rho^2/(1-epsilon*b*rho)',
        'theorem_status':'VERIFIED-EXACT','prior_art_status':'PROVED-SYNTHESIS; novelty OPEN','paper_location':'core constructive theorem'}

def controls():
    same=[]
    for n,m,mask in [(4,8,[0,2]),(8,16,[0,4]),(9,27,[0,3,6])]:
        vals=[str(rem(sum(X**j for j in mask),q)) for q in (n,m)]
        assert vals[0]=='0' and vals[1]!='0'
        same.append({'orders':[n,m],'mask':mask,'values':vals,'graph_realized_boolean':False})
    prime_cases=0
    for p in [3,5,7]:
        for bits in range(1,2**p-1):
            mask=[j for j in range(p) if bits>>j&1]
            for r in range(1,p):
                assert rem(sum(X**((j*r)%p) for j in mask),p)!=0
                prime_cases+=1
    zeta_cancel=rem(X-X,3); zeta_nonzero=rem(X-X**2,3)
    assert zeta_cancel==0 and zeta_nonzero!=0
    O=sp.Matrix([[0,1/z,1/z]])
    Tminus=sp.zeros(3);Tminus[1,0]=1/z;Tminus[2,0]=-1/z
    Tplus=sp.zeros(3);Tplus[1,0]=1/z;Tplus[2,0]=1/z
    assert (O*Tminus)[0]==0 and (O*Tplus)[0]==2/z**2
    assert Tminus**2==sp.zeros(3)
    return {'same_radical':same,
        'equal_cardinality':{'n':8,'masks':[[0,4],[0,2]],'values':['0',str(rem(1+X**2,8))],'graph_realized_boolean':False},
        'marginal_Galois_additive_cycle_unsigned':{'n':3,'mask':[1],'displacement_tuples':[[1,1],[1,2]],
            'signed_sum_tuples':['zeta3-zeta3','zeta3-zeta3^2'],'values':['0',str(zeta_nonzero)],
            'additive_orders':[3,3],'p_cycle_classes':['unbalanced','unbalanced'],
            'marginal_orbits_equal':True,'joint_orbits_equal':False,'graph_realized_boolean':False,'status':'FALSIFIED'},
        'nonlocal_coherent_darkness':{'states':['A','B','C'],'Omega':['0','1/z','1/z'],
            'edges_minus':['A->B:1/z','A->C:-1/z'],'edges_plus':['A->B:1/z','A->C:1/z'],
            'g_A_minus':'0','g_A_plus':'1','K0_minus':['A'],'Kmax_minus':[],'graph_realized_boolean':False},
        'earliest_unit_not_necessary':{'grade_contents':['t','t-1'],'aggregate_content':str(content([t,t-1])),
            'graph_realized_boolean':False,'status':'VERIFIED-EXACT'},
        'prime_nonvanishing':{'primes':[3,5,7],'exact_mask_displacement_cases':prime_cases,'status':'VERIFIED-EXACT'},
        'ideal_only_propagation':{'summands':['1','t-1'],'coherent_content':'t','ideal_sum':'1','status':'FALSIFIED','graph_realized_boolean':False},
        'split_recombine':{'same_aggregate_response':True,'K0':['A','B'],'recombined_Kmax':['A','B'],'split_Kmax':[],
            'recombined_edges':['A->B:1','B->U:1-1=0'],'split_edges':['A->B:1','B->U:1','B->U:-1'],
            'verification':closure([0,1],[(0,1)])==[0,1] and closure([0,1],[(0,1),(1,2)])==[],
            'graph_realized_boolean':False,'status':'VERIFIED-EXACT'}}

def enrich(data):
    data['exact_runtime']={'Python':sys.version.split()[0],'SymPy':sp.__version__,'floating_point_used':False}
    data['theorem_registry']=[
        {'id':'common_future','status':'PROVED-SYNTHESIS','paper_location':'supporting proposition'},
        {'id':'dark_pair_one_event_classifier','status':'PROVED-SYNTHESIS','paper_location':'core theorem'},
        {'id':'amplitude_blind_obstruction','status':'PROVED-SYNTHESIS','paper_location':'core theorem'},
        {'id':'locked_n8','status':'VERIFIED-EXACT','paper_location':'main corollary'},
        {'id':'universal_multi_event_compact_taxonomy','status':'OPEN','paper_location':'not claimed'},
        {'id':'novelty','status':'OPEN','paper_location':'dedicated priority audit'}]
    data['prior_art_sources']=[
        {'url':'https://lall.stanford.edu/engr210a/lectures/lecture4_2001_10_10_01.pdf','mechanism':'finite observability / Markov parameters','status':'PRIOR-ART-OWNED'},
        {'url':'https://stacks.math.columbia.edu/tag/0AS9','mechanism':'content ideals','status':'PRIOR-ART-OWNED'},
        {'url':'https://ifatwww.et.uni-magdeburg.de/ifac2020/media/pdfs/0233.pdf','mechanism':'parametric polynomial gcd structural-property certificates','status':'PRIOR-ART-OWNED'},
        {'url':'https://arxiv.org/abs/2608.10643','mechanism':'mixed-graph zero transfer','status':'PRIOR-ART-OWNED'},
        {'url':'https://arxiv.org/abs/math/9511209','mechanism':'vanishing root-of-unity sums','status':'PRIOR-ART-OWNED'}]
    for comp in data['locked_n8']['components']:
        x,y,_=comp['component_id'][1:-1].split(',')
        comp.update({'parameter_ring':'K8[t]','coefficient_field':'K8=Q(zeta8)','Song_subfield':'Q(zeta8)',
            'physical_coefficients':{'A1':'|1><1|-|5><5|','A2':f't|{x}><{y}|','epsilon_degrees':[1,2]},
            'additive_orders':{str(r):8//math.gcd(r,8) for r in range(8)},
            'p_cycle_classes':{'reference':'new_graph_atlas[0].graph_realization_certificate.p_cycle_classes'},
            'Galois_transport':{'reference':'new_graph_atlas[0].graph_realization_certificate.Galois_transport'},
            'signed_Song_relations':comp['marked_classification']})
        if comp['K0']:
            assert comp['direct_zero_forward_closed']
            assert not any(e['source_block']==4 for e in comp['edges'])
    names=[
        ('exact_order','formal_control_atlas.same_radical',False),
        ('cardinality','formal_control_atlas.equal_cardinality',False),
        ('local_zero_pattern','formal_control_atlas.nonlocal_coherent_darkness',False),
        ('marginal_Galois','formal_control_atlas.marginal_Galois_additive_cycle_unsigned',False),
        ('orientation','locked_n8.components: (6,1) forward versus reverse',True),
        ('split_recombine','formal_control_atlas.split_recombine',False),
        ('localization','locked_n8.block_raw_counts and edge_raw_counts',True),
        ('mixed_factor_absence','locked_n8.mixed_factors_absent',True),
        ('ideal_only','formal_control_atlas.ideal_only_propagation',False),
        ('formal_vs_graph','separate actual and formal atlases',None),
        ('additive_order_alone','signature.signature_counterexample_pair',True),
        ('p_cycle_alone','signature.signature_counterexample_pair',True),
        ('nonconstant_existence','new_graph_atlas[0:2]',True),
        ('prime_nonvanishing','formal_control_atlas.prime_nonvanishing',False)]
    data['mandatory_falsification_suite']=[{'control_id':name,'evidence_reference':ref,'graph_realized_boolean':graph,
        'status':'VERIFIED-EXACT'} for name,ref,graph in names]
    return data

def main():
    print('Phase 0: checking terminal freeze regression',flush=True)
    locked=freeze_regression()
    print('Phase 0 PASS; earliest unit histogram '+str(locked['earliest_unit_histogram']),flush=True)
    print('Building exact oriented-circulant certificates',flush=True)
    n8=baseline(8,[1,3],2,8,[[0,2,4,6],[1,3],[5,7]])
    n9=baseline(9,[3],1,3,[[0,3,6],[1,4,7],[2,5,8]])
    families=[]
    for base,name,a,b in [(n8,'n8_affine_competition',1-t,1+t),(n9,'n9_affine_competition',1-t,1+t),
        (n8,'n8_block_root_1',t-1,sp.Integer(1)),(n8,'n8_block_root_2',t-2,sp.Integer(1)),
        (n8,'n8_edge_root_1',sp.Integer(1),t-1),(n8,'n8_edge_root_2',sp.Integer(1),t-2),
        (n8,'n8_identically_dark',sp.Integer(0),sp.Integer(1)),(n8,'n8_identically_edgeless',sp.Integer(1),sp.Integer(0))]:
        print('Verifying '+name,flush=True)
        families.append(family(base,name,a,b))
    formal=controls()
    signature={'candidate_signature':'certified dark-pair one-event amplitude-ideal signature',
        'signature_components':['actual dark-pair Song certificate','ordered source/target and bra=source','single rank-one event declaration','fixed strong stratum','normalized ideal(a)','normalized ideal(b)'],
        'signature_sufficiency_status':'PROVED-SYNTHESIS',
        'reconstruction':'all g=normalize(a), all h=normalize(b); K0=Kmax=all iff a=0 at the point',
        'signature_counterexample_pair':[
            {'reduced':'all static Song data, signed Song relations, orientation and unweighted declared inventory, but no amplitude polynomials',
             'families':['n8_block_root_1','n8_block_root_2'],'different':'g=t-1 versus t-2','graph_realized_boolean':True},
            {'reduced':'same reduced signature','families':['n8_edge_root_1','n8_edge_root_2'],'different':'h=t-1 versus t-2','graph_realized_boolean':True}],
        'minimality':'Sufficient; amplitude ideal pair relatively necessary for separate g and h targets in this class; no absolute canonical claim'}
    data={'stage':'T17','scope':'one-dimensional rank-one symbolic parameter families over fixed prime-power Song arithmetic',
        'coefficient_field':'K contains K_Song, baseline poles, and fixed amplitudes','Song_subfield':'Q(zeta_n)','parameter_ring':'R=K[t]',
        'strata_convention':'Sigma=V(I) intersect D(S), A=S^-1(R/I); normalized polynomial generators only on PID domain strata',
        'input_hashes':{f:digest(f) for f in ['T16_ARITHMETIC_BLOCK_DARKNESS/T16_MACHINE_READABLE.json','T15_FREEZE_REPAIRS_RESPONSE_PROFILE/T15_MACHINE_READABLE.json']},
        'freeze_repairs':['response field','locally closed strata','zero generator separate'],
        'locked_n8':locked,'new_graph_atlas':families,'formal_control_atlas':formal,'signature':signature,
        'bounded_search':{'n4':'C={1} has singleton nonzero-pole fibres, so this nonempty baseline has no dark pair; not a universal perturbation no-go',
            'n8':'positive connected baseline','n9':'positive disconnected baseline','n16_n25_n27':'not searched for new graphs after small positive certificates; formal order controls retained'},
        'PP_matrix_constructed':False,'theorem_status':'PROVED-SYNTHESIS','prior_art_status':'standard mechanisms PRIOR-ART-OWNED; novelty OPEN',
        'paper_location':'core plus appendix falsification ledger',
        'final_judgement':'CORE THEORY READY FOR PAPER FREEZE for the frozen arithmetic framework, locked census and certified dark-pair one-event classifier with amplitude-blind obstruction; no universal compact taxonomy asserted'}
    OUT.mkdir(exist_ok=True)
    (OUT/'T17_MACHINE_READABLE.json').write_text(json.dumps(enrich(data),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('T17 exact computation PASS; graph families='+str(len(families))+'; locked blocks=112; locked edges=204; PP not constructed',flush=True)

if __name__=='__main__':
    main()
