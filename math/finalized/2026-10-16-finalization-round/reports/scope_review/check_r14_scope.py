"""Second-audit fresh checker. Reads saved results as data; executes no source programs."""
import itertools, json, math, hashlib, zipfile
from pathlib import Path
from sympy import QQ, Poly, symbols, cyclotomic_poly
from sympy.polys.matrices import DomainMatrix
from fractions import Fraction
ROOT = Path(__file__).parent

def check_group(moduli):
    elements=list(itertools.product(*[range(d) for d in moduli]))
    N=len(elements); E=math.lcm(*moduli); z=symbols('z')
    K=QQ.alg_field_from_poly(Poly(cyclotomic_poly(E,z),z))
    units=[K.unit**j for j in range(E)]
    def plus(a,b): return tuple((x+y)%d for x,y,d in zip(a,b,moduli))
    def minus(a,b): return tuple((x-y)%d for x,y,d in zip(a,b,moduli))
    def phase(a,b): return sum(x*y*(E//d) for x,y,d in zip(a,b,moduli))%E
    zero=(0,)*len(moduli)
    order2=[a for a in elements if a!=zero and plus(a,a)==zero]
    # Choose the last eligible pair, independently of the audited checker's first pair.
    x,c=[(a,b) for a in order2 for b in order2 if phase(a,b)==0][-1]
    H=[a for a in elements if phase(c,a)==0]
    R=[a for a in elements if phase(a,x)==0]
    t=[a for a in elements if a not in H][-1]
    tau=[a for a in elements if a not in R][-1]
    hrep=[a for a in H if a<plus(a,x)][::-1]
    rrep=[a for a in R if a<plus(a,c)]
    cp=[v for a in hrep for v in (a,plus(a,x))]
    rp=[v for a in rrep for v in (a,plus(a,c))]
    columns=cp+[minus(t,a) for a in reversed(cp)]
    rows=rp+[minus(tau,a) for a in reversed(rp)]
    assert len(set(rows))==N==len(set(columns))
    def matrix(rr,cc): return [[units[phase(a,b)] for b in cc] for a in rr]
    def rank(rr,cc):
        if not rr or not cc: return 0
        return DomainMatrix(matrix(rr,cc),(len(rr),len(cc)),K).rank()
    upper=[rank(rows[:k],columns[k:]) for k in range(N+1)]
    lower=[rank(rows[k:],columns[:k]) for k in range(N+1)]
    bu=[rank(rrep[:k],hrep[k:]) for k in range(N//4+1)]
    bl=[rank(rrep[k:],hrep[:k]) for k in range(N//4+1)]
    for k in range(N//2+1):
        assert upper[k]==(k+1)//2+bu[k//2]
        assert lower[k]==(k+1)//2+bl[k//2]
    assert upper==lower[::-1]
    assert max(upper+lower)==(1 if N==4 else N//4+1)
    return {'moduli':moduli,'N':N,'upper':upper,'lower':lower,'q':max(upper+lower)}

saved=json.loads((ROOT.parent/'r14'/'independent_checks.json').read_text())
assert len(saved['cases'])==saved['construction_cases']==34
assert sum(c['rank_calls_including_empty'] for c in saved['cases'])==saved['rank_calls_including_empty']==1856
for c in saved['cases']:
    n=c['N']; assert math.prod(c['moduli'])==n
    assert max(c['upper']+c['lower'])==(1 if n==4 else n//4+1)
    for k in range(n//2+1):
        assert c['upper'][k]==(k+1)//2+c['quotient_upper'][k//2]
        assert c['lower'][k]==(k+1)//2+c['quotient_lower'][k//2]
    assert c['upper']==c['lower'][::-1]
# Exact algebra of the critical-cut moment lower bound and positivity.
for L in range(2,1001):
    N=4*L; r=2*L-1; h=2*L+1
    bound=Fraction(r*h,N)+Fraction(r*(N-r),N*N)
    assert bound==L+Fraction(1,4)-Fraction(1,4*L)-Fraction(1,16*L*L)>L
    assert math.gcd(h,N)==1
result={'status':'PASS','source_programs_executed':False,
        'saved_log_consistency':{'cases':34,'rank_calls_including_empty':1856},
        'fresh_exact_cases':[check_group(m) for m in [(4,),(2,2),(8,),(2,2,2),(12,),(2,2,3),(20,),(4,3,3)]]}
(ROOT/'R14_SECOND_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'fresh_cases':len(result['fresh_exact_cases'])}))
