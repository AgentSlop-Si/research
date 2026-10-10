#!/usr/bin/env python3
"""Review-owned exact controls. Reads/imports no research source program.

Dense matrix and exhaustive-word operations are verification oracles only.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent
RNG = random.Random(14533110010)


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b, p):
    bt = transpose(b)
    return [[sum(x*y for x, y in zip(row, col)) % p for col in bt] for row in a]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def inverse(a, p):
    n = len(a)
    b = [row[:] + e for row, e in zip(a, identity(n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        if pivot is None:
            return None
        b[j], b[pivot] = b[pivot], b[j]
        c = pow(b[j][j], -1, p)
        b[j] = [v*c % p for v in b[j]]
        for i in range(n):
            if i != j:
                c = b[i][j]
                b[i] = [(x-c*y) % p for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def root(p, n):
    w = next(w for w in range(2, p) if pow(w, n, p) == 1 and pow(w, n//2, p) != 1)
    assert len({pow(w, i, p) for i in range(n)}) == n
    return w


def evaluate(q, z, p):
    return sum(c*pow(z, i, p) for i, c in enumerate(q)) % p


def shift_polynomial(q, n, p):
    a = [[0]*n for _ in range(n)]
    for j in range(n):
        for k, c in enumerate(q):
            a[(j+k) % n][j] = (a[(j+k) % n][j] + c) % p
    return a


def fourier(n, w, p):
    return [[pow(w, i*j, p) for j in range(n)] for i in range(n)]


def lower_bound_control(q, n, w, p):
    while len(q) > 1 and q[-1] == 0:
        q = q[:-1]
    r = len(q)-1
    assert r < n
    Q = shift_polynomial(q, n, p)
    vals = [evaluate(q, pow(w, j, p), p) for j in range(n)]
    qi = inverse(Q, p)
    assert (qi is not None) == all(vals)
    if qi is None:
        return None
    a = multiply(multiply(transpose(Q), fourier(n, w, p), p), Q, p)
    predicted = [[pow(w, i*j, p)*sum(q[b]*vals[(j+b) % n]*pow(w, i*b, p)
                                   for b in range(r+1)) % p
                  for j in range(n)] for i in range(n)]
    assert a == predicted
    columns = transpose(a)
    assert all(sum(v != 0 for v in col) >= n-r for col in columns)
    assert all(sum(v != 0 for v in row) >= n-r for row in a)
    return {'q0_zero': q[0] == 0, 'degree': r,
            'min_column_support': min(sum(v != 0 for v in c) for c in columns)}


def polynomial_product(factors, p):
    q = [1]
    for a in factors:
        z = [0]*(len(q)+len(a)-1)
        for i, c in enumerate(q):
            for j, d in enumerate(a):
                z[i+j] = (z[i+j]+c*d) % p
        q = z
    return q


def green_controls():
    p = 65537
    gains_list = [(0,0,0,0), (3,3,3,3), (3,27,3,27), (0,3,0,27), (3,27,243,2187)]
    lambdas_list = [(1,1,1,1), (1,-1,1,-1), (0,0,0,0), (0,2,0,0), (2,3,5,7)]
    count = 0
    data = []
    for n in (2,4,8,16,32):
        for gains, ls in itertools.product(gains_list, lambdas_list):
            assert all(pow(a,n,p) != 1 for a in gains)
            gs = [inverse(shift_polynomial([1,-a % p], n, p), p) for a in gains]
            P = []
            for pair in ((0,1),(2,3)):
                P.extend([[sum(ls[t]*gs[t][i][j] for t in pair) % p for j in range(n)] for i in range(n)])
            factors = [[1,-a % p] for a in gains]
            q = polynomial_product(factors, p)
            rs = []
            for pair in ((0,1),(2,3)):
                pol = [0]*4
                for t in pair:
                    term = polynomial_product(factors[:t]+factors[t+1:], p)
                    for j,c in enumerate(term):
                        pol[j] = (pol[j] + ls[t]*c) % p
                rs.extend(shift_polynomial(pol,n,p))
            Q = shift_polynomial(q,n,p)
            assert multiply(P,Q,p) == rs
            assert max(sum(v != 0 for v in row) for row in rs) <= 4
            assert max(sum(v != 0 for v in col) for col in transpose(rs)) <= 8
            if n > 4:
                assert lower_bound_control(q,n,root(p,n),p) is not None
            count += 1
        data.append({'N':n, 'parameter_cases':len(gains_list)*len(lambdas_list)})
    return {'cases':count,'by_size':data,'includes':'zero/repeated gains, zero/canceling/scaled branch coefficients'}


def sparse_controls():
    p = 97
    count = 0
    for n in (2,4,8,16):
        m = 2*n
        for _ in range(25):
            R = [[0]*n for _ in range(m)]
            for row in R:
                for j in RNG.sample(range(n), RNG.randrange(0,min(n,4)+1)):
                    row[j] = RNG.randrange(1,p)
            H = [[0]*m for _ in range(m)]
            for i in range(m):
                for t in (0,1,2):
                    j = (i+t) % m
                    H[i][j] = H[j][i] = RNG.randrange(p)
            s = max(sum(v != 0 for v in col) for col in transpose(R))
            d = max(sum(v != 0 for v in row) for row in R)
            delta = max(sum(v != 0 for v in row) for row in H)
            A = multiply(multiply(transpose(R),H,p),R,p)
            assert all(sum(v != 0 for v in row) <= s*d*delta for row in A)
            assert sum(v != 0 for row in A for v in row) <= n*s*d*delta
            count += 1
    # A row-degree bound is not a column-degree bound without symmetry.
    H = [[1,0,0,0] for _ in range(4)]
    assert max(map(sum,H)) == 1 and max(map(sum,transpose(H))) == 4
    # Column degree alone cannot control R^T H R: d really matters.
    R = [[1]*8]
    A = multiply(transpose(R),R,97)
    assert all(sum(row) == 8 for row in A)
    return {'symmetric_rectangular_cases':count,'orientation_negative_controls':2}


def closed_words(n,k):
    N = 1 << n
    for code in range(1 << k):
        bits = [(code >> (k-1-i)) & 1 for i in range(k)]
        state = 0
        for i in range(-n,0):
            state = 2*state + bits[i % k]
        initial = state
        edges = []
        for bit in bits:
            edges.append(2*state+bit)
            state = (2*state+bit) % N
        assert state == initial
        yield edges


def locality_controls():
    cases=[]
    for n in range(1,10):
        N=1<<n
        for k in range(1,n+4):
            support=[set() for _ in range(2*N)]
            for edges in closed_words(n,k):
                for i,e in enumerate(edges):
                    support[e].update(f for j,f in enumerate(edges) if j!=i)
            actual=max(map(len,support))
            bound=k*(1 << max(0,k-n-1))
            assert actual<=bound
            cases.append({'N':N,'k':k,'maximum_structural_row_support':actual,'bound':bound})
    return cases


def centering_controls():
    p=97
    total=0
    for n in range(1,5):
        N=1<<n
        k=n+2
        edgesets=list(closed_words(n,k))
        for zero_baseline in (False,True):
            gamma=[RNG.randrange(0 if zero_baseline else 1,p) for _ in range(2*N)]
            if zero_baseline:
                gamma[0]=0
            direction=[RNG.randrange(p) for _ in gamma]
            value=0
            gradient=[0]*len(gamma)
            hessian_direction=0
            for es in edgesets:
                value+=__import__('math').prod(gamma[e] for e in es)
                for i,e in enumerate(es):
                    gradient[e]+=__import__('math').prod(gamma[f] for j,f in enumerate(es) if j!=i)
                    for j,f in enumerate(es):
                        if i!=j:
                            hessian_direction+=direction[e]*direction[f]*__import__('math').prod(gamma[g] for t,g in enumerate(es) if t not in (i,j))
            # Completely separate degree-two polynomial multiplication.
            jet=[0,0,0]
            for es in edgesets:
                t=[1,0,0]
                for e in es:
                    t=[t[0]*gamma[e]%p,(t[1]*gamma[e]+t[0]*direction[e])%p,
                       (t[2]*gamma[e]+t[1]*direction[e])%p]
                jet=[(a+b)%p for a,b in zip(jet,t)]
            assert jet[0]==value%p
            assert jet[1]==sum(a*b for a,b in zip(gradient,direction))%p
            assert 2*jet[2]%p==hessian_direction%p
            centered=[(jet[0]-value)%p,(jet[1]-sum(a*b for a,b in zip(gradient,direction)))%p,jet[2]]
            assert centered[:2]==[0,0] and centered[2]==jet[2]
            total+=1
    return {'formal_directional_cases':total,'includes_zero_baselines':True}


def main():
    exhaustive=[]
    for q in itertools.product(range(5),repeat=4):
        ans=lower_bound_control(list(q),4,2,5)
        if ans is not None:
            exhaustive.append(ans)
    random_cases=0
    for p,n,count in ((17,8,150),(97,16,80),(257,32,40)):
        w=root(p,n)
        for _ in range(count):
            while True:
                r=RNG.randrange(n)
                q=[RNG.randrange(1,p)]+[RNG.randrange(p) for _ in range(r)]
                if r:
                    q[-1]=RNG.randrange(1,p)
                ans=lower_bound_control(q,n,w,p)
                if ans is not None:
                    break
            random_cases+=1
    # Singular-Q guard failure: two columns vanish, although N-r=2.
    q=[1,0,16]
    Q=shift_polynomial(q,4,17)
    A=multiply(multiply(transpose(Q),fourier(4,4,17),17),Q,17)
    assert inverse(Q,17) is None
    assert [sum(v!=0 for v in col) for col in transpose(A)]==[0,2,0,2]
    thresholds=[]
    for n in range(3,65):
        lower=(1<<n)-4
        upper=64*(n+2)
        assert (lower>upper)==(n>=10)
        thresholds.append({'n':n,'N':1<<n,'lower':lower,'upper':upper,'excluded':lower>upper})
    results={'status':'PASS','source_execution':False,
             'exhaustive_F5_N4':{'polynomials':625,'invertible':len(exhaustive),
                                'invertible_q0_nonzero':sum(not x['q0_zero'] for x in exhaustive),
                                'invertible_q0_zero':sum(x['q0_zero'] for x in exhaustive)},
             'random_invertible_polynomial_cases':random_cases,
             'singular_denominator_negative_control':{'N':4,'field':17,'q':[1,0,16],'column_supports':[0,2,0,2]},
             'four_green':green_controls(),'sparse_product':sparse_controls(),
             'necklace_structural_locality':locality_controls(),
             'centering':centering_controls(),'thresholds':thresholds,
             'scope':'Exact finite controls corroborate formulas and guards; uniform conclusions are proved in the review, not inferred from tests.'}
    (OUT/'FRESH_REVIEW_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exhaustive_invertible':len(exhaustive),'random_polynomials':random_cases,
                      'four_green_cases':results['four_green']['cases'],'locality_cases':len(results['necklace_structural_locality'])}))


if __name__=='__main__':
    main()
