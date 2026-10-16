#!/usr/bin/env python3
"""Fresh exact controls for ALG-039. Standard library only; no source code imported.

The algorithm under test is a leaf-to-root coefficient schedule. The separate
oracle expands the defining sum by direct source/target routing at every power.
Finite checks corroborate the report's proof; they do not prove all-size claims.
"""
from pathlib import Path
import json
import random


def valuation(s):
    assert s > 0
    return (s & -s).bit_length() - 1


def normalize(a, p):
    return a if p is None else a % p


def layout(N, d):
    assert N >= 2 and N & (N-1) == 0 and d >= 0
    n = N.bit_length()-1
    return [d+n] + [d+valuation(s)+1 for s in range(1,N)]


def tree(x, p=None):
    N, d = len(x), len(x[0])-1
    n = N.bit_length()-1
    lengths = layout(N,d)
    y = [[0]*L for L in lengths]
    for s in range(1,N):
        y[s][:d+1] = [normalize(v,p) for v in x[s]]
    edge_additions = 0
    root_additions = 0
    visits = []
    for h in range(n):
        for odd in range(1,N >> h,2):
            s = (1 << h)*odd
            visits.append(s)
            parent = (2*s) % N
            if parent:
                for j,a in enumerate(y[s]):
                    y[parent][j+1] = normalize(y[parent][j+1]+a,p)
                    edge_additions += 1
    for s in range(1,N):
        for j,a in enumerate(y[s]):
            y[0][j] = normalize(y[0][j]-a,p)
            root_additions += 1
    assert sorted(visits) == list(range(1,N))
    return y, edge_additions, root_additions


def defining_sum(x, p=None):
    N, d = len(x), len(x[0])-1
    n = N.bit_length()-1
    # Fixed rectangular storage is used only in this bounded test oracle.
    out = [[0]*(d+n) for _ in range(N)]
    for t in range(n):
        for s in range(N):
            target = ((1 << t)*s) % N
            for j,a in enumerate(x[s]):
                out[target][j+t] = normalize(out[target][j+t]+a,p)
                out[0][j+t] = normalize(out[0][j+t]-a,p)
    return out


def pad(v,L):
    return v + [0]*(L-len(v))


def actual_degree(v):
    return next((j for j in range(len(v)-1,-1,-1) if v[j]),-1)


def poly_eval(a,z,p):
    total = 0
    for c in reversed(a):
        total = (total*z+c) % p
    return total


def scalar_defining_sum(x,z,p):
    N = len(x)
    n = N.bit_length()-1
    ans = [0]*N
    for t in range(n):
        a = pow(z,t,p)
        for s,v in enumerate(x):
            ans[((1<<t)*s)%N] = (ans[((1<<t)*s)%N]+a*v)%p
            ans[0] = (ans[0]-a*v)%p
    return ans


def apply_C(y,omega,p):
    N = len(y)
    m = N//2
    out = []
    root = 1
    for r in range(m):
        L = max(len(y[r]),len(y[r+m]))
        a,b = pad(y[r],L),pad(y[r+m],L)
        out.append([root*(u-v)%p for u,v in zip(a,b)])
        root = root*omega%p
    return out


def contract(y,h,p):
    N = len(y)
    ans = [0]*len(y[0])
    for s in range(1,N):
        for j,a in enumerate(y[s]):
            ans[j] = (ans[j]+(h[s]-h[0])*a)%p
    return ans


def check_case(N,d,p,g,rng):
    omega = pow(g,(p-1)//N,p)
    assert pow(omega,N,p)==1 and pow(omega,N//2,p)!=1
    n = N.bit_length()-1
    x = [[rng.randrange(p) for _ in range(d+1)] for _ in range(N)]
    y,e,r = tree(x,p)
    oracle = defining_sum(x,p)
    assert [pad(v,d+n) for v in y] == oracle
    assert sum(map(len,y)) == d*N+2*N-2
    C_nonroot = d*(N-1)+2*N-n-2
    assert sum(map(len,y[1:])) == C_nonroot
    assert e == d*(N-2)+2*N-2*n-2
    assert r == C_nonroot
    assert all(sum(row[j] for row in oracle)%p==0 for j in range(d+n))
    changed = [row[:] for row in x]
    changed[0] = [(v+1)%p for v in changed[0]]
    assert tree(changed,p)[0] == y
    for z in (0,1,p-1):
        values = [poly_eval(v,z,p) for v in x]
        assert [poly_eval(v,z,p) for v in y] == scalar_defining_sum(values,z,p)
    c = apply_C(y,omega,p)
    assert sum(map(len,c)) == d*N//2+N-1
    for r in range(N//2):
        expected = [(pow(omega,r,p)*(oracle[r][j]-oracle[r+N//2][j]))%p for j in range(d+n)]
        assert pad(c[r],d+n)==expected
    h = [rng.randrange(p) for _ in range(N)]
    marked = contract(y,h,p)
    assert marked == [sum(h[s]*oracle[s][j] for s in range(N))%p for j in range(d+n)]
    # A J-injected polynomial input must use the same guarded-free K schedule.
    jx = [[0]*(d+1) if s%2==0 else x[s] for s in range(N)]
    assert [pad(v,d+n) for v in tree(jx,p)[0]] == defining_sum(jx,p)
    # Mod z^(L+1): truncate only after/in monotone degree shifts; same prefix.
    for L in sorted({0,d,n-1,d+n-1}):
        assert [row[:L+1] for row in oracle] == [pad(v,d+n)[:L+1] for v in y]
    return {"N":N,"n":n,"d":d,"p":p,"slots":sum(map(len,y)),"edge_additions":e,"root_additions":C_nonroot}


def main():
    rng = random.Random(390016)
    cases = []
    for p,g,maxn in [(3,2,1),(17,3,4),(97,5,5),(257,3,7),(65537,3,7)]:
        for n in range(1,maxn+1):
            N = 1<<n
            for d in sorted({0,1,2,3,7,n,n+3,2*n}):
                cases.append(check_case(N,d,p,g,rng))
    # Characteristic-zero all-nonzero output witnesses for every structural slot.
    dense = []
    for n in range(1,8):
        N = 1<<n
        for d in (0,1,n,2*n):
            y,e,r = tree([[1]*(d+1) for _ in range(N)])
            assert all(all(c != 0 for c in row) for row in y)
            assert all(actual_degree(y[s])==d+valuation(s) for s in range(1,N))
            assert actual_degree(y[0]) == d+n-1
            dense.append({"N":N,"d":d,"all_nonzero_slots":sum(map(len,y))})
    # Actual degree can be strictly smaller despite degree-d nonzero input at every coordinate.
    cancellations = []
    for d in (0,1,5):
        x = [[0]*d+[a] for a in (1,1,1,-1)]
        y,_,_ = tree(x)
        assert [actual_degree(v) for v in y] == [d]*4
        cancellations.append({"N":4,"d":d,"actual_degrees":[d]*4,"structural_degrees":[d+1,d,d+1,d]})
    # A root-only polynomial is annihilated identically, including nonzero input mass.
    for n in range(1,8):
        N = 1<<n
        x = [[1,2,3]]+[[0,0,0] for _ in range(N-1)]
        assert all(all(a==0 for a in row) for row in tree(x)[0])
    # Independent exact census for large n without allocating exponentially large vectors.
    counts = []
    for n in (1,2,3,8,16,32,64,128):
        N = 1<<n
        for d in (0,1,n,3*n):
            nonroot = sum((d+h+1)*(N>>(h+1)) for h in range(n))
            assert nonroot == d*(N-1)+2*N-n-2
            assert nonroot+d+n == d*N+2*N-2
            counts.append({"n":n,"d":d,"full_slots":d*N+2*N-2})
    result = {"status":"PASS","scope":"Fresh exact finite controls, not independent acceptance or all-size experimental proof.","finite_field_cases":len(cases),"scalar_evaluations":3*len(cases),"dense_integer_witnesses":len(dense),"degree_cancellation_witnesses":len(cancellations),"root_only_annihilation_cases":7,"large_integer_census_cases":len(counts),"cases":cases,"dense_witnesses":dense,"cancellations":cancellations,"count_cases":counts,"source_programs_executed":False}
    out = Path(__file__).with_name('CHECK_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))


if __name__=='__main__':
    main()
