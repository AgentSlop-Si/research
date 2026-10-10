#!/usr/bin/env python3
"""Fresh exact review of 1805 guarded certificates. No inherited code is loaded.

Coefficients are rational vectors in the power basis of Q(z)/(Phi_11).
Polynomial identities are recomputed in sparse dictionaries. Negative divisibility
is certified by exact finite-field witnesses, with the divisor's leading
coefficient a unit at the chosen residue place (see report for the proof).
"""
import ast
import gzip
import hashlib
import json
import math
import time
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT/'research_cycle_1805/guarded_fourier_reduction'
PREV = ROOT/'research_cycle_1758/symbolic_independent_review'
VARS = (0,11,22,25,34,39,41,44,49,52,55,65,83,88,91,92)
POS = {v:i for i,v in enumerate(VARS)}
E0 = (0,)*16
Z0 = ((0,)*10,1)
ONE = ((1,)+(0,)*9,1)
ZETA = ((0,1)+(0,)*8,1)
CHECKS = []
START = time.monotonic()

def check(ok,msg):
    if not ok: raise AssertionError(msg)
def mark(msg):
    CHECKS.append(msg)
    print(f'{time.monotonic()-START:.2f}s {msg}',flush=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):
    if str(p).endswith('.gz'):
        with gzip.open(p,'rt') as f:return json.load(f)
    return json.loads(Path(p).read_text())
def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def coefficient(a,d=1):
    check(len(a)==10 and all(type(x) is int for x in a),'coefficient vector')
    check(type(d) is int and d!=0,'coefficient denominator')
    if d<0:a=[-x for x in a];d=-d
    g=math.gcd(d,*a)
    return (tuple(x//g for x in a),d//g)
def cint(n):return coefficient([n]+[0]*9)
def cneg(a):return (tuple(-x for x in a[0]),a[1])
def cadd(a,b):
    if a==Z0:return b
    if b==Z0:return a
    g=math.gcd(a[1],b[1]);s=b[1]//g;t=a[1]//g
    return coefficient([x*s+y*t for x,y in zip(a[0],b[0])],a[1]*s)
@lru_cache(maxsize=131072)
def cmul(a,b):
    if a==Z0 or b==Z0:return Z0
    if a==ONE:return b
    if b==ONE:return a
    # Ordinary convolution, then quotient by the monic polynomial Phi_11.
    t=[0]*19
    for i,x in enumerate(a[0]):
        if x:
            for j,y in enumerate(b[0]):
                if y:t[i+j]+=x*y
    for k in range(18,9,-1):
        q=t[k]
        if q:
            for j in range(k-10,k):t[j]-=q
        t[k]=0
    return coefficient(t[:10],a[1]*b[1])
@lru_cache(maxsize=8192)
def cinv(a):
    check(a!=Z0,'inverse zero')
    # Invert the 10x10 multiplication map using rational Gaussian elimination.
    cols=[]
    for j in range(10):
        basis=coefficient([int(i==j) for i in range(10)])
        b=cmul(a,basis);cols.append([Fraction(x,b[1]) for x in b[0]])
    m=[[cols[j][i] for j in range(10)]+[Fraction(i==0)] for i in range(10)]
    for col in range(10):
        pivot=next(i for i in range(col,10) if m[i][col])
        m[col],m[pivot]=m[pivot],m[col]
        q=m[col][col];m[col]=[x/q for x in m[col]]
        for i in range(10):
            if i!=col:
                q=m[i][col]
                if q:m[i]=[x-q*y for x,y in zip(m[i],m[col])]
    d=math.lcm(*(row[-1].denominator for row in m))
    result=coefficient([int(row[-1]*d) for row in m],d)
    check(cmul(a,result)==ONE,'inverse verification')
    return result
def cpow(a,k):
    if k<0:return cpow(cinv(a),-k)
    r=ONE
    while k:
        if k&1:r=cmul(r,a)
        a=cmul(a,a);k//=2
    return r
@lru_cache(maxsize=65536)
def parse_coeff(s):
    def rec(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return cint(n.value)
        if isinstance(n,ast.Name) and n.id=='zeta':return ZETA
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return cneg(rec(n.operand))
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.UAdd):return rec(n.operand)
        if isinstance(n,ast.BinOp):
            if isinstance(n.op,ast.Pow):
                check(isinstance(n.right,ast.Constant) and type(n.right.value) is int,'power AST')
                return cpow(rec(n.left),n.right.value)
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op,ast.Add):return cadd(a,b)
            if isinstance(n.op,ast.Sub):return cadd(a,cneg(b))
            if isinstance(n.op,ast.Mult):return cmul(a,b)
            if isinstance(n.op,ast.Div):return cmul(a,cinv(b))
        raise AssertionError('unrecognized coefficient syntax')
    return rec(ast.parse(s,mode='eval').body)
def padd(a,b):
    r=dict(a)
    for e,c in b.items():
        q=cadd(r.get(e,Z0),c)
        if q!=Z0:r[e]=q
        else:r.pop(e,None)
    return r
def pneg(a):return {e:cneg(c) for e,c in a.items()}
def pscale(a,c):return {} if c==Z0 else {e:cmul(v,c) for e,v in a.items()}
def pmul(a,b):
    if not a or not b:return {}
    r={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f))
            q=cadd(r.get(g,Z0),cmul(c,d))
            if q!=Z0:r[g]=q
            else:r.pop(g,None)
    return r
def ppow(p,n):
    check(type(n) is int and n>=0,'polynomial power')
    r={E0:ONE}
    while n:
        if n&1:r=pmul(r,p)
        p=pmul(p,p);n//=2
    return r
def variable(v):
    e=list(E0);e[POS[v]]=1
    return {tuple(e):ONE}
def deps(p):return {VARS[i] for e in p for i,n in enumerate(e) if n}
def degree(p,v):return max((e[POS[v]] for e in p),default=-1)
def pieces(p,v):
    i=POS[v];r={}
    for e,c in p.items():
        f=list(e);k=f[i];f[i]=0
        r.setdefault(k,{})[tuple(f)]=c
    return r
def substitute_clear(p,v,n,d):
    # d^m * p(v=n/d), computed only at the expanded stage or small identities.
    terms=pieces(p,v);m=max(terms,default=0);r={}
    np=[{E0:ONE}];dp=[{E0:ONE}]
    for k in range(m):np.append(pmul(np[-1],n));dp.append(pmul(dp[-1],d))
    for k,q in terms.items():r=padd(r,pmul(q,pmul(np[k],dp[m-k])))
    return r,m
def parse_sparse(rows):
    r={};previous=None
    for e,a,d in rows:
        check(len(e)==16 and all(type(k) is int and k>=0 for k in e),'polynomial exponents')
        e=tuple(e);c=coefficient(a,d)
        check(c!=Z0 and e not in r,'sparse nonzero/unique')
        check((list(c[0]),c[1])==(a,d),'canonical field encoding')
        check(previous is None or previous<e,'canonical term ordering')
        r[e]=c;previous=e
    return r
def verify_pool(obj,pool):
    for h,rows in obj['polynomials'].items():
        check(hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()==h,'polynomial address '+h)
        p=parse_sparse(rows)
        if h in pool:check(pool[h]==p,'polynomial collision')
        pool[h]=p

def stats(eq,pool):
    polys=[pool[h] for h in eq.values()]
    return dict(variables=sorted(set().union(*(deps(p) for p in polys))),equations=len(polys),terms=sum(map(len,polys)),max_terms=max(map(len,polys)),nonzero_constant=any(set(p)=={E0} for p in polys))
def denominator(record,guards,pool,available=None):
    proof=record['denominator_nonzero']
    c=coefficient(*proof['constant']);check(c!=Z0,'denominator constant is nonzero')
    q={E0:c}
    for g in proof['guard_factors']:
        check(g in guards,'denominator uses retained guard')
        p=pool[guards[g]]
        if available is not None:check(deps(p)<=available,'acyclic denominator guard '+g)
        q=pmul(q,p)
    check(q==pool[record['denominator']],'exact denominator product')

def residue_coefficient(a,p,z):
    check(a[1]%p!=0,'residue denominator')
    return sum(x*pow(z,i,p) for i,x in enumerate(a[0]))*pow(a[1],-1,p)%p

def evaluate_mod(poly,point,p,z,cache):
    result=0
    powers=[{0:1} for _ in VARS]
    for e,c in poly.items():
        if c not in cache:cache[c]=residue_coefficient(c,p,z)
        term=cache[c]
        for i,k in enumerate(e):
            if k:
                if k not in powers[i]:powers[i][k]=pow(point[i],k,p)
                term=term*powers[i][k]%p
        result=(result+term)%p
    return result

def negative_divisibility(initial,pool,irreducibility):
    # 1013 is prime, 11 divides 1012; verify all rather than assume.
    p=1013
    check(all(p%d for d in range(2,math.isqrt(p)+1)),'residue prime')
    z=next(x for x in range(2,p) if pow(x,11,p)==1)
    check(sum(pow(z,i,p) for i in range(11))%p==0 and z!=1,'primitive residue zeta')
    cache={};points=[];results=[]
    for c in {c for h in list(initial['equations'].values())+list(initial['guards'].values()) for c in pool[h].values()}:
        cache[c]=residue_coefficient(c,p,z)
    linear={f'x{v}':v for v in [39,41,44,52,83,88,91,92]}
    linear.update({r['guard']:r['linear_variable'] for r in irreducibility['proofs']})
    for name,h in initial['guards'].items():
        div=pool[h];v=linear[name];parts=pieces(div,v)
        check(set(parts)<= {0,1} and 1 in parts,'witness divisor linear')
        # Lex-leading coefficient unit: division in the coefficient valuation ring
        # then reduction is legitimate, even for an unknown char-zero quotient.
        lc=div[max(div)];check(cache[lc]!=0,'divisor leading coefficient residue unit')
        remaining=set(initial['equations']);seed=0
        while remaining:
            check(seed<100,'witness search exhausted')
            point=[(17+7*i+seed*(i*i+3))%p for i in range(16)]
            a=evaluate_mod(parts[1],point,p,z,cache)
            if not a:seed+=1;continue
            b=evaluate_mod(parts.get(0,{}),point,p,z,cache)
            point[POS[v]]=-b*pow(a,-1,p)%p
            check(evaluate_mod(div,point,p,z,cache)==0,'divisor zero witness')
            idx=len(points);points.append(dict(guard=name,seed=seed,point=point,leading_coefficient=cache[lc]))
            for eid in sorted(remaining,key=int):
                value=evaluate_mod(pool[initial['equations'][eid]],point,p,z,cache)
                if value:
                    results.append(dict(equation=eid,guard=name,point_index=idx,residue=value))
                    remaining.remove(eid)
            seed+=1
        print(f'  {name}: 59 exact negative witnesses',flush=True)
    check(len(results)==826 and len({(r['equation'],r['guard']) for r in results})==826,'826 unique tests')
    artifact=dict(method='Exact reduction at the residue place (p,zeta)=(1013,%d), with a unit leading coefficient for every divisor'%z,prime=p,zeta=z,variables=VARS,points=points,tests=results)
    dump('NONDIVISIBILITY_WITNESSES.json',artifact)
    return dict(tests=826,prime=p,zeta=z,points=len(points),all_nonzero=True)

def main():
    entry=load(SRC/'REVIEW_ENTRY.json')
    check(sha(SRC/'REVIEW_ENTRY.json')=='06ff76f081c8fdba74e9bc77a2036247e4515b0e57930117ea85504e616b97e7','entry hash')
    files={str(SRC.relative_to(ROOT)/'REVIEW_ENTRY.json'):sha(SRC/'REVIEW_ENTRY.json')}
    for f in entry['files']:
        p=ROOT/f['path'];check(p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],'entry manifest '+f['path']);files[f['path']]=f['sha256']
    prev=load(PREV/'RECEIPT.json')
    check(sha(PREV/'RECEIPT.json')==entry['accepted_input_receipt_sha256'],'accepted predecessor hash')
    files[str((PREV/'RECEIPT.json').relative_to(ROOT))]=sha(PREV/'RECEIPT.json')
    # Pin the accepted predecessor and all of its listed sources, without rerunning it.
    for p,h in prev['source_hashes'].items():check(sha(ROOT/p)==h,'accepted source unchanged '+p);files[p]=h
    for p,h in prev['review_artifact_hashes'].items():check(sha(PREV/p)==h,'accepted review artifact unchanged '+p);files[str((PREV/p).relative_to(ROOT))]=h
    raw=gzip.decompress((SRC/'CERTIFICATE.json.gz').read_bytes())
    check(hashlib.sha256(raw).hexdigest()==sha(SRC/'CERTIFICATE.json'),'compressed certificate identity')
    cert=json.loads(raw);branch=load(SRC/'COMPACT_BRANCH.json');irr=load(SRC/'GUARD_IRREDUCIBILITY.json');core=load(SRC/'SIMPLIFIED_CORE.json')
    check(tuple(cert['variables'])==VARS and tuple(branch['variables'])==VARS,'variable layout')
    check(cert['input_receipt_sha256']==entry['accepted_input_receipt_sha256'],'input receipt link')
    for kind in ('equations','guards'):
        check(sha(ROOT/cert[f'input_{kind}_file'])==cert[f'input_{kind}_sha256'],'input '+kind+' hash')
    check(cert['input_equations_sha256']==prev['source_hashes'][cert['input_equations_file']],'equations accepted link')
    check(cert['input_guards_sha256']==prev['review_artifact_hashes']['FINAL_COORDINATE_GUARDS.json'],'guards accepted link')
    check(branch['parent_certificate_sha256']==sha(SRC/'CERTIFICATE.json') and branch['parent_stage']=='final','compact parent link')
    check(load(SRC/'INITIAL.json')==cert['initial'] and load(SRC/'FINAL.json')==cert['final'],'standalone stage files')
    mark('Frozen entry, compressed certificate, accepted predecessor, and all listed manifest/source hashes verified')
    pool={}
    for obj in (cert,branch,irr,core):verify_pool(obj,pool)
    mark(f'{len(pool)} content-addressed polynomials independently parsed and hashes checked')
    check(cpow(ZETA,11)==ONE and cadd(sum_coeff([cpow(ZETA,i) for i in range(11)]),Z0)==Z0,'cyclotomic field relation')
    source=load(ROOT/'research_cycle_1734/pole_escape/full_fourier_linear_reduction.json.gz')
    check(hashlib.sha256(gzip.decompress((ROOT/'research_cycle_1734/pole_escape/full_fourier_linear_reduction.json.gz').read_bytes())).hexdigest()==cert['input_equations_sha256'],'accepted source gzip identity')
    initial=cert['initial'];check(len(initial['equations'])==59,'59 initial equations')
    for i,r in enumerate(source['remaining_equations']):
        check(initial['labels'][str(i)]==r['label'],'initial label')
        p={}
        for t in r['terms']:
            e=t['exponent'];check(len(e)==99,'accepted exponent length');check(all(n==0 for j,n in enumerate(e) if j not in POS),'discarded initial variable')
            key=tuple(e[j] for j in VARS);check(key not in p,'duplicate accepted monomial')
            p[key]=parse_coeff(t['coefficient'])
        check(p==pool[initial['equations'][str(i)]],'initial polynomial '+str(i))
    guards=load(ROOT/cert['input_guards_file'])
    expected={f'x{v}':variable(v) for v in guards['nonzero_surviving_coordinates']}
    for r in guards['nonzero_guard_polynomials']:
        p={}
        for t in r['terms']:
            e=list(E0)
            for v,k in t['exponent']:e[POS[v]]=k
            p[tuple(e)]=coefficient(t['coefficient_numerators'],t['coefficient_denominator'])
        expected['g'+str(r['eliminated_mandatory_edge'])]=p
    check(set(expected)==set(initial['guards']) and len(expected)==14,'all fourteen input guards')
    for g,p in expected.items():check(pool[initial['guards'][g]]==p,'input guard '+g)
    check(stats(initial['equations'],pool)==initial['statistics'],'initial statistics')
    mark('All 59 initial equations and fourteen guards match the accepted predecessor exactly')
    eq=dict(initial['equations']);gs=dict(initial['guards']);events=[]
    for k,r in enumerate(cert['events']):
        kind=r['kind']
        if kind=='linear_elimination':
            v=r['variable'];eid=r['source_equation'];check(eq[eid]==r['source'],'pivot source reference')
            n,d=pool[r['numerator']],pool[r['denominator']]
            check(v not in deps(n)|deps(d),'pivot variable independence')
            check(pool[r['source']]==padd(pmul(variable(v),d),pneg(n)),'pivot source = d*x - n')
            denominator(r,gs,pool)
            check({q['equation'] for q in r['equation_transforms']}==set(eq) and len(r['equation_transforms'])==len(eq),'all equation transforms')
            check({q['guard'] for q in r['guard_transforms']}==set(gs) and len(r['guard_transforms'])==len(gs),'all guard transforms')
            for group,key,state in [('equation_transforms','equation',eq),('guard_transforms','guard',gs)]:
                for t in r[group]:
                    check(state[t[key]]==t['old'],'old polynomial reference')
                    q,m=substitute_clear(pool[t['old']],v,n,d)
                    check(m==t['denominator_power'] and q==pool[t['new']],'exact expanded substitution '+t[key])
                    check(v not in deps(q),'eliminated variable removed')
                    state[t[key]]=t['new']
            check(not pool[eq[eid]],'solved source vanishes identically')
            del eq[eid]
            events.append(dict(kind=kind,variable=v,source=initial['labels'][eid],equation_transforms=len(r['equation_transforms']),guard_transforms=len(r['guard_transforms']),denominator_nonzero=True))
            mark('x91 field-unit pivot and all 58 equation/fourteen guard substitutions replay exactly')
        elif kind=='cancel':
            check(eq[r['equation']]==r['dividend'] and gs[r['guard']]==r['divisor'],'cancellation references')
            check(pool[r['dividend']]==pmul(pool[r['divisor']],pool[r['quotient']]),'exact cancellation product')
            eq[r['equation']]=r['quotient'];events.append(dict(kind=kind,equation=r['equation'],guard=r['guard']))
        elif kind=='normalize_guard':
            check(gs[r['guard']]==r['dividend'] and gs[r['nonzero_divisor_guard']]==r['divisor'],'guard normalization references')
            check(r['guard']!=r['nonzero_divisor_guard'],'noncircular guard cancellation')
            check(pool[r['dividend']]==pmul(pool[r['divisor']],pool[r['quotient']]),'guard quotient product')
            gs[r['guard']]=r['quotient'];events.append(dict(kind=kind,guard=r['guard'],divisor=r['nonzero_divisor_guard']))
        else:raise AssertionError('unexpected event')
    counts=Counter(r['kind'] for r in events)
    check(counts==dict(linear_elimination=1,cancel=34,normalize_guard=3),'event counts')
    check(eq==cert['final']['equations'] and gs==cert['final']['guards'],'final state references')
    finalstats=stats(eq,pool);check(finalstats==cert['final']['statistics'],'expanded final stats')
    check(finalstats['equations']==58 and finalstats['terms']==124465 and finalstats['max_terms']==25534 and len(finalstats['variables'])==15,'expanded claims')
    check(len(gs)==14 and set(gs)==set(initial['guards']),'no guard lost')
    mark('34 exact monomial cancellations and three guard normalizations verified; 15 variables, 58 equations, 124465 terms')
    # Verify circuit definitions symbolically without expanding nested compositions.
    available=set(branch['free_variables']);check(len(available)==12 and len(branch['free_variables'])==12,'12 distinct free variables')
    check([r['variable'] for r in branch['definitions']]==branch['reconstruction_order']==[39,44,55],'compact reconstruction order')
    circuit=[];remaining=dict(eq)
    for r in branch['definitions']:
        v=r['variable'];eid=r['source_equation'];n=pool[r['numerator']];d=pool[r['denominator']]
        check(v not in available and remaining[eid]==r['source'],'compact distinct source')
        check(r['source_label']==initial['labels'][eid],'compact source label')
        dependencies=deps(n)|deps(d)
        check(sorted(dependencies)==r['dependencies'] and dependencies<=available,'compact DAG dependencies')
        check(pool[r['source']]==padd(pmul(variable(v),d),pneg(n)),'compact pivot polynomial identity')
        denominator(r,gs,pool,available)
        # Cross-multiplied cancellation after substituting n/d: d*n - n*d=0.
        check(pmul(d,n)==pmul(n,d),'compact solve numerator identity')
        circuit.append(dict(variable=v,source_equation=eid,source_label=r['source_label'],dependencies=sorted(dependencies),numerator_terms=len(n),denominator_terms=len(d),denominator_nonzero=r['denominator_nonzero'],identity='source = denominator*x_variable - numerator; substitution solves identically'))
        del remaining[eid];available.add(v)
    check(remaining==branch['equations'] and branch['guards']==gs,'all compact residual references and all guards')
    check(len(remaining)==branch['equations_count']==55 and len(gs)==branch['guards_count']==14,'compact counts')
    check(available==set(finalstats['variables']),'compact free/defined coordinate partition')
    for h in list(remaining.values())+list(gs.values()):check(deps(pool[h])<=available,'closed compact evaluation')
    mark('All three compact pivots, acyclic denominator proofs, 55 residual circuits, and fourteen retained guards verified')
    # Each proof is primitive linear over the UFD K[the other coordinates].
    irr_results=[]
    check({r['guard'] for r in irr['proofs']}=={'g98','g96','g89','g95','g46','g48'} and len(irr['proofs'])==6,'six irreducibility guards')
    for r in irr['proofs']:
        check(initial['guards'][r['guard']]==r['polynomial'],'irreducibility original guard reference')
        p=pool[r['polynomial']];v=r['linear_variable'];s=pieces(p,v)
        check(set(s)<={0,1} and 1 in s,'linear irreducibility polynomial')
        a,b=pool[r['leading_coefficient']],pool[r['constant_coefficient']]
        check(s[1]==a and s.get(0,{})==b,'irreducibility coefficient decomposition')
        method=None
        if r['guard'] in ('g98','g96','g95'):
            check(set(a)=={E0} and a[E0]!=Z0,'unit leading coefficient');method='unit-leading linear'
        elif r['guard'] in ('g89','g46'):
            q,c=pool[r['quotient']],pool[r['nonzero_constant_remainder']]
            check(v not in deps(q) and set(c)=={E0} and c[E0]!=Z0,'Bezout constant')
            check(b==padd(pmul(a,q),c),'b = a*q + nonzero constant');method='primitive linear, constant Bezout remainder'
        else:
            leading=coefficient(*r['leading_constant']);check(leading!=Z0,'nonzero leading field constant')
            prod={E0:leading};factor_polys=[]
            for f in r['leading_factors']:
                fac,root=pool[f['factor']],pool[f['root']]
                check(not deps(root),'constant root for irreducible factor')
                check(fac==padd(variable(f['variable']),pneg(root)),'explicit irreducible linear factor')
                check(fac not in factor_polys,'distinct monic factors');factor_polys.append(fac)
                rem,m=substitute_clear(b,f['variable'],root,{E0:ONE})
                check(rem==pool[f['nonzero_remainder']] and rem,'nonzero factor remainder')
                prod=pmul(prod,fac)
            check(prod==a and len(factor_polys)==3,'complete leading factorization');method='primitive linear, three complete leading factors with nonzero remainders'
        irr_results.append(dict(guard=r['guard'],variable=v,method=method))
    mark('All six original-guard irreducibility certificates independently verified')
    negative=negative_divisibility(initial,pool,irr)
    mark('826 initial nondivisibility statements verified by exact residue-field witnesses')
    t=pool[core['T']];u=pool[core['U']];a=coefficient(*core['A']);c=coefficient(*core['nonzero_field_constant_c'])
    claimed_t=padd({E0:ZETA},padd(pscale(variable(41),cneg(cpow(ZETA,9))),pmul(pmul(variable(11),variable(41)),padd(variable(34),variable(49)))))
    check(t==claimed_t,'T explicit formula')
    check(cmul(a,cadd(ZETA,cneg(ONE)))==cadd(cpow(ZETA,9),cneg(cpow(ZETA,4))),'A exact formula')
    check(cadd(ZETA,cneg(ONE))!=Z0,'A denominator')
    check(c==cadd(cpow(ZETA,7),cneg(cpow(ZETA,6))) and c!=Z0,'nonzero c formula')
    check(u==padd(pscale(t,a),{E0:cneg(ONE)}),'U = A*T - 1')
    check(pool[gs['x91']]==pneg(t),'normalized guard = -T')
    d39=branch['definitions'][0];check(core['source_variable39']==d39,'simplified source39 link')
    r91=cert['events'][0];check(core['source_variable91']=={k:r91[k] for k in ('numerator','denominator')},'simplified source91 link')
    n39,D39=pool[d39['numerator']],pool[d39['denominator']]
    check(pmul(n39,t)==pmul(u,D39),'x39 = U/T cross-multiplied identity')
    n91,D91=pool[r91['numerator']],pool[r91['denominator']]
    check(n91==pneg(pmul(variable(39),t)) and D91=={E0:c},'x91 = -x39*T/c before simplification')
    # This independently checked identity cancels T only on the retained T!=0 domain.
    cleared,m=substitute_clear(n91,39,u,t)
    check(m==1 and cleared==pneg(pmul(u,t)),'x91 composed numerator, before T cancellation')
    check(pool[gs['x39']]==variable(39),'x39 exclusion retained')
    mark('Simplified T, A, U formulas and x39/x91 identities checked with all cancellation guards retained')
    # Rehash to detect concurrent or accidental input mutation during this review.
    for p,h in files.items():check(sha(ROOT/p)==h,'end-of-run frozen hash '+p)
    dump('EVENT_REPLAY.json',events)
    dump('CIRCUIT_REPLAY.json',dict(free_variables=branch['free_variables'],definitions=circuit,equations=remaining,guards=gs,identity_scope='Exact source = denominator*x - numerator identities in the 15-coordinate ring; composition through an acyclic rational evaluation DAG preserves them. No expanded or algebraically simplified twelve-variable residual system is asserted.'))
    receipt=dict(status='PASS: guarded equivalence to accepted necessary system independently verified; no factorization or impossibility conclusion',entry_sha256=sha(SRC/'REVIEW_ENTRY.json'),predecessor_receipt_sha256=sha(PREV/'RECEIPT.json'),coefficient_field='Q[zeta]/(1+zeta+...+zeta^10)',method='Fresh independent exact sparse checker and restricted AST; no inherited programs executed/imported; exact finite-field nondivisibility witnesses with unit-leading-coefficient proof',checks=CHECKS,expanded=finalstats,compact=dict(free_variables=branch['free_variables'],equations=55,guards=14,representation='exact triangular rational evaluation circuits',eliminated=[39,44,55]),event_counts=dict(counts),irreducibility=irr_results,nondivisibility=negative,simplified_core_verified=True,all_original_guards_preserved=True,source_hashes=files,checker_sha256=sha(__file__),runtime_seconds=time.monotonic()-START,scope='Equivalence only to the accepted guarded necessary checkpoint. A candidate still requires prior reverse reconstruction and all original 121 entry equations. Counts are stored residual constraints, not algebraic independence.',not_certified=['No original Fourier factorization or unrestricted complex no-go', 'No fully expanded twelve-variable residual system or residual independence', 'No exhaustive search for further compact pivots', 'Author timing/size-cap failure traces are observational logs, not mathematical certificates; they were not rerun'])
    dump('RECEIPT.json',receipt)
    print('PASS',flush=True)

def sum_coeff(cs):
    r=Z0
    for c in cs:r=cadd(r,c)
    return r

if __name__=='__main__':
    try:main()
    except Exception as e:
        dump('FAILURE.json',dict(error=repr(e),checks_completed=CHECKS,checker_sha256=sha(__file__),elapsed_seconds=time.monotonic()-START))
        raise
