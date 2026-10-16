#!/usr/bin/env python3
"""Fresh authored controls. Never imports or executes supplied research code.

The production-like recurrence branch uses only the capped synthesis routine,
boundary polynomials, root-orbit scan, batch inverse and exceptional Horner.
The dense DFT and brute-force fitter below are verification oracles only.
"""
from itertools import product
from pathlib import Path
import json
import random


def capped_synthesis(x, cap, p):
    """Return (register length, padded connection coefficients), or None.

    Known prime field p is a caller premise. cap is less than len(x).
    Counts are algebraic operation counts; inv is separately charged.
    The register length is NOT the degree of the connection polynomial.
    """
    n = len(x)
    if not 0 <= cap < n:
        raise ValueError('need 0 <= cap < N')
    C = [1] + [0] * cap
    B = C[:]
    L, shift, invb = 0, 1, 1
    counts = dict(multiply=0, add=0, inverse=0, samples=0)
    for t in range(n):
        counts['samples'] += 1
        delta = x[t] % p
        for j in range(1, L + 1):
            delta = (delta + C[j] * x[t-j]) % p
            counts['multiply'] += 1
            counts['add'] += 1
        if delta == 0:
            shift += 1
            continue
        change = 2 * L <= t
        new_L = t + 1 - L if change else L
        if new_L > cap:
            return None, counts
        old = C[:]
        scale = delta * invb % p
        counts['multiply'] += 1
        for j in range(cap + 1):
            if j + shift <= cap:
                C[j+shift] = (C[j+shift] - scale * B[j]) % p
                counts['multiply'] += 1
                counts['add'] += 1
            else:
                assert B[j] == 0
        if change:
            L, B, shift = new_L, old, 1
            invb = pow(delta, -1, p)
            counts['inverse'] += 1
        else:
            shift += 1
    assert all((x[t] + sum(C[i]*x[t-i] for i in range(1,L+1))) % p == 0
               for t in range(L,n))
    assert counts['inverse'] <= cap
    return (L, C[:L+1]), counts


def evaluate(poly, t, p):
    answer = 0
    for a in reversed(poly):
        answer = (answer*t + a) % p
    return answer


def root_orbit(n, omega, p):
    ts, t = [], 1
    for j in range(n):
        if j and t == 1:
            raise ValueError('root has smaller order')
        ts.append(t)
        t = t*omega % p
    if t != 1:
        raise ValueError('root does not have order N')
    return ts


def batch_inverse(a, p):
    if not a:
        return []
    prefixes, total = [], 1
    for v in a:
        assert v % p != 0
        prefixes.append(total)
        total = total*v % p
    z = pow(total, -1, p)
    out = [0]*len(a)
    for i in reversed(range(len(a))):
        out[i] = z*prefixes[i] % p
        z = z*a[i] % p
    return out


def recurrence_dft(x, cap, p, omega):
    """None means exact rejection of the cap, not a Fourier result."""
    n = len(x)
    ts = root_orbit(n, omega, p)
    fitted, counts = capped_synthesis(x, cap, p)
    if fitted is None:
        return None, dict(synthesis=counts)
    L, C = fitted
    P = [sum(C[i]*x[j-i] for i in range(j+1)) % p for j in range(L)]
    B = [sum(C[i]*x[n+j-i] for i in range(j+1,L+1)) % p for j in range(L)]
    A = [(u+v) % p for u,v in zip(P,B)]
    denominators = [evaluate(C,t,p) for t in ts]
    regular = [k for k,q in enumerate(denominators) if q]
    inverse = batch_inverse([denominators[k] for k in regular],p)
    out = [None]*n
    for k,qinv in zip(regular,inverse):
        out[k] = evaluate(A,ts[k],p)*qinv % p
    exceptional = []
    for k in range(n):
        if denominators[k] == 0:
            exceptional.append(k)
            out[k] = evaluate(x,ts[k],p)
    assert len(exceptional) <= L
    return out, dict(length=L, coefficients=C, exceptional=exceptional,
                     synthesis=counts, output_inverse=int(bool(regular)))


def dense_dft(x, p, omega):
    return [sum(a*pow(omega,j*k,p) for j,a in enumerate(x)) % p
            for k in range(len(x))]


def radix2_dft(x,p,omega):
    """Fresh ordinary fallback, with paid O(N) root table and O(N log N) work."""
    n=len(x)
    if n & (n-1):
        raise ValueError('fallback needs dyadic length')
    roots=root_orbit(n,omega,p)
    a=[z%p for z in x]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i<j:
            a[i],a[j]=a[j],a[i]
    width=2
    while width<=n:
        half=width//2
        for begin in range(0,n,width):
            for j in range(half):
                u=a[begin+j]
                v=a[begin+j+half]*roots[j*(n//width)]%p
                a[begin+j]=(u+v)%p
                a[begin+j+half]=(u-v)%p
        width*=2
    return a


def adaptive_dft(x,cap,p,omega):
    out,ledger=recurrence_dft(x,cap,p,omega)
    if out is None:
        return radix2_dft(x,p,omega),dict(branch='ordinary_fft',detail=ledger)
    return out,dict(branch='recurrence',detail=ledger)


def brute_min_length(x,p):
    """Exhaustive independent minimality oracle for tiny fields only."""
    for L in range(len(x)+1):
        for c in product(range(p),repeat=L):
            if all((x[t]+sum(c[i-1]*x[t-i] for i in range(1,L+1))) % p == 0
                   for t in range(L,len(x))):
                return L
    raise AssertionError


def generate(initial, coefficients, n, p):
    x = list(initial)
    L = len(initial)
    while len(x)<n:
        x.append(-sum(coefficients[i]*x[-i] for i in range(1,L+1)) % p)
    return x


def null_vector(rows, width, p):
    a=[list(r) for r in rows]
    pivots=[]
    for col in range(width):
        pivot=next((r for r in range(len(pivots),len(a)) if a[r][col]%p),None)
        if pivot is None:
            continue
        k=len(pivots)
        a[k],a[pivot]=a[pivot],a[k]
        inv=pow(a[k][col]%p,-1,p)
        a[k]=[v*inv%p for v in a[k]]
        for r in range(len(a)):
            if r!=k:
                scalar=a[r][col]
                a[r]=[(u-scalar*v)%p for u,v in zip(a[r],a[k])]
        pivots.append(col)
    free=next((c for c in range(width) if c not in pivots),None)
    if free is None:
        return None
    v=[0]*width
    v[free]=1
    for r,col in enumerate(pivots):
        v[col]=-a[r][free]%p
    assert any(v)
    assert all(sum(x*y for x,y in zip(row,v))%p==0 for row in rows)
    return v


def run():
    counts = dict(exhaustive_sequences=0, capped_decisions=0,
                  exact_dft_vectors=0, exceptional_bins=0,
                  adaptive_vectors=0, ordinary_fft_fallbacks=0,
                  projection_witnesses=0, residual_surjectivity=0,
                  channel_coset_vectors=0, channel_coset_singular_bins=0,
                  root_rejections=0)
    for p,max_n in [(2,7),(3,5)]:
        for n in range(1,max_n+1):
            for x in product(range(p),repeat=n):
                truth=brute_min_length(x,p)
                counts['exhaustive_sequences']+=1
                for cap in range(n):
                    got,ledger=capped_synthesis(x,cap,p)
                    assert (got is not None)==(truth<=cap)
                    if got is not None:
                        assert got[0]==truth
                    counts['capped_decisions']+=1
    rng=random.Random(20261016)
    for p,n,omega in [(17,4,4),(17,8,2),(17,16,3),
                      (97,8,64),(97,16,8),(97,32,28),
                      (193,64,125)]:
        root_orbit(n,omega,p)
        cases=[([0]*n,0),([1]+[0]*(n-1),1),([0]*(n-1)+[1],min(3,n-1))]
        for cap in range(1,min(n,9)):
            for trial in range(12):
                c=[1]+[rng.randrange(p) for _ in range(cap)]
                x=generate([rng.randrange(p) for _ in range(cap)],c,n,p)
                cases.append((x,cap))
        # Fourier-character mixtures force true exceptional bins.
        for r in range(1,min(7,n)):
            x=[sum(pow(omega,-j*t,p) for j in range(r))%p for t in range(n)]
            cases.append((x,r))
        # Repeated root and irreducible-polynomial recurrences.
        cases.extend([(generate([2,3],[1,-2,1],n,p),2),
                      (generate([1,2],[1,0,3],n,p),2)])
        for x,cap in cases:
            out,ledger=recurrence_dft(x,cap,p,omega)
            if out is None:
                assert x==[0]*(n-1)+[1]
                continue
            assert out==dense_dft(x,p,omega)
            counts['exact_dft_vectors']+=1
            counts['exceptional_bins']+=len(ledger['exceptional'])
        for x in [[0]*(n-1)+[1]]+[[rng.randrange(p) for j in range(n)] for _ in range(10)]:
            out,ledger=adaptive_dft(x,min(2,n-1),p,omega)
            assert out==dense_dft(x,p,omega)
            counts['adaptive_vectors']+=1
            counts['ordinary_fft_fallbacks']+=int(ledger['branch']=='ordinary_fft')
    for n,omega,p in [(8,1,17),(8,4,17),(8,3,17),(4,0,17)]:
        try:
            root_orbit(n,omega,p)
        except ValueError:
            counts['root_rejections']+=1
        else:
            raise AssertionError('bad root accepted')
    # All two-probe matrices over F_3 for K=3: nonzero residual invisible.
    for flat in product(range(3),repeat=6):
        rows=[flat[:3],flat[3:]]
        v=null_vector(rows,3,3)
        assert v is not None
        M,d=5,1
        residual=[[0]*3 for _ in range(M-2*d-1)]+[v]
        assert all(all(sum(a*b for a,b in zip(e,w))%3==0 for e in residual)
                   for w in rows)
        counts['projection_witnesses']+=1
    # ALG053's true output nodes are cosets, so z^M is usually not one.
    # Construct spectra first, invert columns, and compare full raw-input DFT.
    for p,K,M,Omega in [(17,2,4,2),(17,4,4,3),(97,4,8,28),(193,8,8,125)]:
        N=K*M
        root_orbit(N,Omega,p)
        omegaK=pow(Omega,M,p)
        for mode in range(4):
            streams=[]
            expected=[]
            for ell in range(K):
                if mode==0:
                    L,C=1,[1,-pow(Omega,-ell,p)%p]
                    f=generate([ell+1],C,M,p)
                elif mode==1:
                    L,C=2,[1,0,0]
                    f=generate([ell+1,ell+2],C,M,p)
                elif mode==2:
                    L,C=2,[1,-2,1]
                    f=generate([ell+1,ell+3],C,M,p)
                else:
                    L,C=2,[1,rng.randrange(p),rng.randrange(p)]
                    f=generate([rng.randrange(p),rng.randrange(p)],C,M,p)
                streams.append(f)
                P=[sum(C[i]*f[j-i] for i in range(j+1))%p for j in range(L)]
                B=[sum(C[i]*f[M+j-i] for i in range(j+1,L+1))%p for j in range(L)]
                gamma=pow(omegaK,ell,p)
                A=[(a+gamma*b)%p for a,b in zip(P,B)]
                for j in range(M):
                    k=ell+j*K
                    z=pow(Omega,k,p)
                    assert pow(z,M,p)==gamma
                    denominator=evaluate(C,z,p)
                    if denominator:
                        y=evaluate(A,z,p)*pow(denominator,-1,p)%p
                    else:
                        y=evaluate(f,z,p)
                        counts['channel_coset_singular_bins']+=1
                    expected.append((k,y))
            raw=[0]*N
            invK=pow(K,-1,p)
            for u in range(K):
                for t in range(M):
                    raw[u*M+t]=sum(streams[ell][t]*pow(omegaK,-u*ell,p)
                                     for ell in range(K))*invK%p
            observed=dense_dft(raw,p,Omega)
            assert observed==[v for k,v in sorted(expected)]
            counts['channel_coset_vectors']+=1
    # Construct every prescribed tail residual by triangular recurrence inversion.
    p,K,M,d=5,3,7,2
    for _ in range(50):
        q=[[1]+[rng.randrange(p) for _ in range(d)] for l in range(K)]
        desired=[[rng.randrange(p) for _ in range(K)] for t in range(M-2*d)]
        f=[[0]*K for _ in range(M)]
        for t in range(2*d,M):
            for l in range(K):
                f[t][l]=(desired[t-2*d][l]-sum(q[l][i]*f[t-i][l] for i in range(1,d+1)))%p
        actual=[[(f[t][l]+sum(q[l][i]*f[t-i][l] for i in range(1,d+1)))%p
                 for l in range(K)] for t in range(2*d,M)]
        assert actual==desired
        counts['residual_surjectivity']+=1
    result=dict(verdict='PASS', counts=counts,
                supplied_code_executed=False,
                claims='Finite controls only; proofs and model boundaries are in REPORT.md.')
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    run()
