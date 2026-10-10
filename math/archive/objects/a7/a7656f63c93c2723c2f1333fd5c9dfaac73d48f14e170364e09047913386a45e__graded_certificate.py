"""Exactly certify degree<=d Boolean spectral completion failures.

Fourier-character grading via cyclic-shift averaging ensures it suffices to
search monomials whose known frequency indices sum to the target modulo N.
A full (M+1)x(M+1) minor of these M columns + target, nonzero mod a split
prime, implies the same over characteristic-zero complex cyclotomic fields.
"""
from __future__ import annotations
from itertools import combinations, combinations_with_replacement
from spectral_boolean import primitive_root


def graded_monomials(n,known,target,d):
    out=[]
    for j in range(1,d+1):
        for idx in combinations_with_replacement(known,j):
            if sum(idx)%n==target:out.append(idx)
    return out


def degree_d_inputs(n,d):
    for size in range(d+1):
        yield from combinations(range(n),size)


def evaluations_for_support(n,p,powers,known,mons,target,support):
    sources={s:sum(powers[s][j] for j in support)%p for s in known}
    vals=[]
    for mon in mons:
        value=1
        for s in mon:value=value*sources[s]%p
        vals.append(value)
    vals.append(sum(powers[target][j] for j in support)%p)
    return vals


def rank_certificate(n:int,p:int,target:int,degree:int=3,known=None,max_rows=None):
    """Find M+1 binary samples giving a nonzero augmented determinant.

    If found, polynomial recovery in degree <=d is impossible over C as well.
    If not found, absence of a certificate is NOT existence of completion.
    """
    if known is None:known=tuple(s for s in range(n) if s!=target)
    known=tuple(known)
    w=primitive_root(n,p)
    powers=[[pow(w,(s*j)%n,p) for j in range(n)] for s in range(n)]
    mons=graded_monomials(n,known,target,degree)
    m=len(mons)
    pivots={}
    selected=[]
    rows_seen=0
    for subset in degree_d_inputs(n,degree):
        values=evaluations_for_support(n,p,powers,known,mons,target,subset)
        v=values[:]
        for pivot,basis in pivots.items():
            c=v[pivot]
            if c:
                v=[(a-c*b)%p for a,b in zip(v,basis)]
        lead=next((j for j,t in enumerate(v) if t),None)
        rows_seen+=1
        if lead is not None:
            inv=pow(v[lead],-1,p)
            pivots[lead]=[(t*inv)%p for t in v]
            selected.append(subset)
            if len(selected)==m+1:
                return {"status":"no_completion_degree_at_most_d_over_C",
                        "n":n,"prime":p,"root":w,"degree":degree,
                        "target":target,"known":known,"monomials":mons,
                        "certificate_supports":selected,"rows_examined":rows_seen,
                        "rank_aug":m+1,"num_columns":m,
                        "certificate_check":"determinant of augmented square evaluation matrix is nonzero mod p"}
        if max_rows is not None and rows_seen>=max_rows:break
    return {"status":"inconclusive","n":n,"prime":p,"degree":degree,
            "target":target,"known":known,"monomials":mons,
            "rows_examined":rows_seen,"rank_aug":len(selected),
            "num_columns":m,"certificate_supports":selected}


def determinant_mod(matrix,p):
    n=len(matrix)
    assert all(len(r)==n for r in matrix)
    a=[r[:] for r in matrix]
    det=1
    for c in range(n):
        row=next((i for i in range(c,n) if a[i][c]),None)
        if row is None:return 0
        if row!=c:
            a[c],a[row]=a[row],a[c]
            det=-det
        pivot=a[c][c]%p
        det=det*pivot%p
        inv=pow(pivot,-1,p)
        for i in range(c+1,n):
            mult=a[i][c]*inv%p
            if mult:
                for j in range(c,n):
                    a[i][j]=(a[i][j]-mult*a[c][j])%p
    return det%p


def verify_certificate(result:dict):
    if result['status'] != 'no_completion_degree_at_most_d_over_C':return False
    n,p,target=result['n'],result['prime'],result['target']
    known=tuple(result['known']); mons=[tuple(m) for m in result['monomials']]
    supports=[tuple(v) for v in result['certificate_supports']]
    if len(supports)!=len(mons)+1:return False
    if any(len(s)>result['degree'] or sorted(set(s))!=list(s) for s in supports):return False
    if mons!=graded_monomials(n,known,target,result['degree']):return False
    w=primitive_root(n,p)
    if result.get('root')!=w:return False
    powers=[[pow(w,(s*j)%n,p) for j in range(n)] for s in range(n)]
    a=[evaluations_for_support(n,p,powers,known,mons,target,s) for s in supports]
    return determinant_mod(a,p)!=0

if __name__=='__main__':
    import time,sys
    for n in [8,16,32]:
        t=time.perf_counter()
        r=rank_certificate(n,998244353,n-1,degree=3,max_rows=8000)
        print('n',n,'status',r['status'],'monomials',r['num_columns'],'rank',r['rank_aug'],'scanned',r['rows_examined'],'s',round(time.perf_counter()-t,3),flush=True)
        if r['status'].startswith('no_'):
            print('verify',verify_certificate(r),flush=True)
