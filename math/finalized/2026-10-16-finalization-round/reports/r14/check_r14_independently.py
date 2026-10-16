"""Independent small-instance check written for the audit, 2026-10-16.

No code from the submitted archive is imported or executed. This deliberately
uses brute-force group enumeration, not the submitted lightweight constructor.
All matrix ranks are characteristic-zero exact cyclotomic-field ranks.
"""
import itertools, math, random, json, time
from pathlib import Path
from sympy import QQ, Poly, symbols, cyclotomic_poly
from sympy.polys.matrices import DomainMatrix

def check(moduli, seed):
    N = math.prod(moduli)
    E = math.lcm(*moduli)
    group = list(itertools.product(*(range(n) for n in moduli)))
    zero = (0,) * len(moduli)
    def add(a,b): return tuple((u+v)%n for u,v,n in zip(a,b,moduli))
    def sub(a,b): return tuple((u-v)%n for u,v,n in zip(a,b,moduli))
    def exponent(a,b): return sum(u*v*(E//n) for u,v,n in zip(a,b,moduli))%E
    involutions = [g for g in group if g != zero and add(g,g)==zero]
    x,c = next((x,c) for x in involutions for c in involutions if exponent(c,x)==0)
    H = [g for g in group if exponent(c,g)==0]
    R = [g for g in group if exponent(g,x)==0]
    t = next(g for g in group if g not in H)
    tau = next(g for g in group if g not in R)
    rng = random.Random(seed)
    def reps(subgroup, shift):
        pending = set(subgroup)
        representatives = []
        while pending:
            g = min(pending)
            h = add(g,shift)
            representatives.append(rng.choice([g,h]))
            pending.remove(g); pending.remove(h)
        rng.shuffle(representatives)
        return representatives
    cols0,rows0 = reps(H,x),reps(R,c)
    firstcols = [v for g in cols0 for v in [g,add(g,x)]]
    firstrows = [v for g in rows0 for v in [g,add(g,c)]]
    cols = firstcols+[sub(t,g) for g in reversed(firstcols)]
    rows = firstrows+[sub(tau,g) for g in reversed(firstrows)]
    assert set(rows)==set(group) and set(cols)==set(group)
    z = symbols('z')
    K = QQ.alg_field_from_poly(Poly(cyclotomic_poly(E,z),z),alias='zeta')
    powers = [K.unit**j for j in range(E)]
    def matrix(rs,cs): return [[powers[exponent(a,b)] for b in cs] for a in rs]
    def rank(a):
        nr=len(a); nc=len(a[0]) if nr else 0
        return DomainMatrix(a,(nr,nc),K).rank() if nr and nc else 0
    def profiles(a):
        n=len(a)
        return [[rank([r[k:] for r in a[:k]]) for k in range(n+1)],
                [rank([r[:k] for r in a[k:]]) for k in range(n+1)]]
    A,B = matrix(rows,cols),matrix(rows0,cols0)
    up,lo=profiles(A); bu,bl=profiles(B)
    for k in range(N//2+1):
        assert up[k]==(k+1)//2+bu[k//2],(moduli,seed,k,'upper')
        assert lo[k]==(k+1)//2+bl[k//2],(moduli,seed,k,'lower')
    assert up==list(reversed(lo))
    expected=1 if N==4 else N//4+1
    assert max(up+lo)==expected
    return dict(moduli=moduli,seed=seed,N=N,exponent=E,q=expected,upper=up,lower=lo,
                quotient_upper=bu,quotient_lower=bl,
                rank_calls_including_empty=2*(N+1)+2*(N//4+1))

if __name__=='__main__':
    start=time.perf_counter()
    cases=[]
    for moduli in [(4,),(2,2),(8,),(4,2),(2,2,2),(12,),(2,2,3),
                   (20,),(2,2,5),(24,),(4,2,3),(2,2,2,3),(28,),
                   (36,),(4,3,3),(2,2,3,3),(40,)]:
        for seed in [41,20261016]:
            case=check(moduli,seed)
            cases.append(case)
            print(moduli,seed,case['q'],flush=True)
    result=dict(status='PASS',implementation='audit-authored brute-force constructor; exact SymPy cyclotomic ranks',
                input_archive_code_executed=False,cases=cases,construction_cases=len(cases),
                rank_calls_including_empty=sum(c['rank_calls_including_empty'] for c in cases),
                elapsed_seconds=time.perf_counter()-start)
    Path(__file__).with_name('independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
