"""Standalone fresh exact verifier for the three forced-denominator pivots.
Only JSON data from earlier work is read. No earlier program is run or imported.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, json, time

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
ZERO=(Q(0),)*10
ONE=(Q(1),)+(Q(0),)*9
MAX_PAIRS=1000000
MAX_TERMS=50000

def fadd(a,b): return tuple(x+y for x,y in zip(a,b))
def fneg(a): return tuple(-x for x in a)
def fmul(a,b):
    # Ordinary convolution, then descending reduction by 1+z+...+z^10.
    p=[Q(0)]*19
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:p[i+j]+=x*y
    for i in range(18,9,-1):
        if p[i]:
            q=p[i]
            for j in range(11):p[i-10+j]-=q
    return tuple(p[:10])

def unpack(raw):
    out={}
    for m,c,d in raw:
        assert len(m)==16 and len(c)==10 and d>0
        assert all(isinstance(e,int) and e>=0 for e in m)
        m=tuple(m); assert m not in out
        value=tuple(Q(x,d) for x in c); assert value!=ZERO
        out[m]=value
    return out

def padd(a,b):
    out=dict(a)
    for m,c in b.items():
        v=fadd(out.get(m,ZERO),c)
        if v!=ZERO:out[m]=v
        elif m in out:del out[m]
    return out

def pneg(a):return {m:fneg(c) for m,c in a.items()}
def pmul(a,b):
    assert len(a)*len(b)<=MAX_PAIRS,'product work limit'
    out={}
    for m,c in a.items():
        for n,d in b.items():
            k=tuple(x+y for x,y in zip(m,n)); v=fadd(out.get(k,ZERO),fmul(c,d))
            if v!=ZERO:out[k]=v
            elif k in out:del out[k]
    assert len(out)<=MAX_TERMS,'polynomial term limit'
    return out

def constant(c):return {(0,)*16:c} if c!=ZERO else {}
def variable(i,V):
    m=[0]*16;m[V.index(i)]=1
    return {tuple(m):ONE}
def deps(p,V):return {V[i] for m in p for i,x in enumerate(m) if x}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(path):
    started=time.monotonic()
    D=json.loads(path.read_text())
    source=ROOT/'research_cycle_1805/guarded_fourier_reduction'
    for name,h in D['source_hashes'].items():assert sha(ROOT/name)==h,('source hash',name)
    C=json.loads((source/'CERTIFICATE.json').read_text())
    B=json.loads((source/'COMPACT_BRANCH.json').read_text())
    R=json.loads((ROOT/'research_cycle_1819/guarded_reduction_review/RECEIPT.json').read_text())
    assert R['status'].startswith('PASS:')
    assert R['source_hashes'][str((source/'CERTIFICATE.json').relative_to(ROOT))]==sha(source/'CERTIFICATE.json')
    assert R['source_hashes'][str((source/'COMPACT_BRANCH.json').relative_to(ROOT))]==sha(source/'COMPACT_BRANCH.json')
    V=C['variables'];assert V==D['variables']==B['variables']
    raw={}
    for pool in [C['polynomials'],B['polynomials'],D['polynomials']]:
        for k,v in pool.items():
            if k in raw:assert raw[k]==v,('inconsistent polynomial',k)
            raw[k]=v
    cache={}
    def get(k):
        if k not in cache:cache[k]=unpack(raw[k])
        return cache[k]
    for k,v in D['polynomials'].items():
        assert hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()==k
        get(k)
    assert D['new_eliminations']==[22,88,52]
    assert D['reconstruction_order']==[22,88,52,39,44,55]
    assert D['definitions'][3:]==B['definitions']
    assert D['free_variables']==[v for v in B['free_variables'] if v not in [22,88,52]]
    assert D['free_variables']==[0,11,25,34,41,49,65,83,92]
    assert set(D['guards'])==set(B['guards'])|{'D22','D88','D52'}
    assert all(D['guards'][g]==r for g,r in B['guards'].items())
    sources=set();available=set(D['free_variables']); checks=[]
    for j,d in enumerate(D['definitions']):
        v=d['variable'];eq=d['source_equation'];sources.add(eq)
        assert eq in C['final']['equations']
        assert d['source']==C['final']['equations'][eq]
        assert d['source_label']==C['initial']['labels'][eq]
        n,a,p=get(d['numerator']),get(d['denominator']),get(d['source'])
        assert a and n
        assert v not in deps(n,V)|deps(a,V)
        assert p==padd(pmul(variable(v,V),a),pneg(n)),('solve identity',v)
        actual=deps(n,V)|deps(a,V)
        assert actual==set(d['dependencies']) and actual<=available,('dependency',v)
        nz=d['denominator_nonzero']
        if j<3:
            assert eq in B['equations']
            assert nz['method']=='forced by source equation and nonzero numerator'
            proof=nz['numerator_nonzero']; target=n
            assert D['guards']['D'+str(v)]==d['denominator']
            assert proof['guard_factors']==([] if v in [22,88] else ['x83'])
        else:proof=nz;target=a
        cv,den=proof['constant'];assert len(cv)==10 and den>0
        fc=tuple(Q(x,den) for x in cv);assert fc!=ZERO
        product=constant(fc)
        for g in proof['guard_factors']:
            assert g in B['guards'] and D['guards'][g]==B['guards'][g]
            gp=get(D['guards'][g]);assert deps(gp,V)<=available
            product=pmul(product,gp)
        assert target==product,('nonzero identity',v)
        checks.append({'variable':v,'source_equation':eq,'source_label':d['source_label'],
                       'numerator_terms':len(n),'denominator_terms':len(a),
                       'nonzero_proof':'equation forces denominator; numerator is nonzero' if j<3 else 'retained guard product',
                       'dependencies':sorted(actual)})
        available.add(v)
    assert available==set(C['final']['statistics']['variables'])
    expected={k:r for k,r in C['final']['equations'].items() if k not in sources}
    assert D['equations']==expected
    assert D['equations']=={k:r for k,r in B['equations'].items() if k not in {'58','36','4'}}
    assert D['equation_count']==len(expected)==52
    assert D['guard_count']==len(D['guards'])==17
    assert D['original_guard_count']==len(B['guards'])==14
    assert not D['factorization_claimed'] and not D['contradiction_claimed']
    # Replay the short human-readable denominator formulas independently.
    z=(Q(0),Q(1))+(Q(0),)*8
    def zpow(k):
        value=ONE
        for _ in range(k):value=fmul(value,z)
        return constant(value)
    def xx(k):return variable(k,V)
    def plus(*ps):
        value={}
        for p in ps:value=padd(value,p)
        return value
    def times(*ps):
        value=constant(ONE)
        for p in ps:value=pmul(value,p)
        return value
    a=times(xx(11),xx(34));w=times(xx(0),xx(65))
    d22=plus(xx(34),xx(49))
    d88=plus(pneg(zpow(7)),times(xx(41),plus(zpow(1),pneg(zpow(10)),
        times(a,plus(zpow(7),pneg(zpow(9)),times(plus(zpow(2),pneg(zpow(0))),xx(83)))),
        times(w,plus(zpow(10),times(a,plus(xx(83),pneg(zpow(7)))))))))
    d52=plus(pneg(xx(83)),times(w,plus(pneg(zpow(7)),times(zpow(6),xx(83)))),
        times(xx(0),xx(49),plus(zpow(3),times(plus(zpow(5),pneg(zpow(2))),xx(83)),
            times(xx(25),plus(pneg(zpow(2)),times(zpow(1),xx(83)))),
            times(plus(pneg(zpow(8)),times(zpow(7),xx(83))),xx(88),
                  plus(zpow(0),pneg(xx(92)),pneg(w))))))
    for name,p in [('D22',d22),('D88',d88),('D52',d52)]:assert p==get(D['guards'][name]),('compact formula',name)
    # Check that every residual and every guard is a well-formed polynomial in
    # coordinates already available; no residual is expanded under substitution.
    for r in list(D['equations'].values())+list(D['guards'].values()):
        assert deps(get(r),V)<=available
    return {'status':'PASS: author-side exact replay; independent review pending',
            'certificate_sha256':sha(path),'checker_sha256':sha(Path(__file__)),
            'source_hashes':D['source_hashes'],'free_variables':D['free_variables'],
            'free_variable_count':9,'residual_equations':52,'retained_original_guards':14,
            'derived_denominator_guards':3,'total_guards':17,'pivots':checks,
            'parent_residual_polynomials_expanded':False,
            'zero_branches_omitted':False,
            'equivalence':'Exact guarded equivalence to the accepted 12-variable necessary circuit system; no original factorization or impossibility claim.',
            'runtime_seconds':round(time.monotonic()-started,6)}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=OUT/'CONSEQUENCE_CERTIFICATE.json');parser.add_argument('--no-receipt',action='store_true')
    args=parser.parse_args();result=verify(args.certificate)
    if not args.no_receipt:(OUT/'CHECK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
