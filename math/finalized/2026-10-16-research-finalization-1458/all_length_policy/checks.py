"""Fresh exact controls for the all-length ALG-034 policy.

No imported or executed historical research program. Standard library only.
These finite controls corroborate the proof; they do not execute a producer.
"""
import hashlib
import json
import math
import random
from pathlib import Path


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return trim(c)


def divide_monic(a, b):
    a, b = trim(a), trim(b)
    assert b[-1] == 1
    q = [0] * max(1, len(a)-len(b)+1)
    while len(a) >= len(b):
        d = len(a)-len(b)
        c = a[-1]
        q[d] += c
        for j, v in enumerate(b):
            a[d+j] -= c*v
        a = trim(a)
        if a == [0]:
            break
    return trim(q), a


def reduce_poly(a, f):
    return divide_monic(a, f)[1]


def cyclotomics(limit):
    phi = {}
    for n in range(1, limit+1):
        p = [-1] + [0]*(n-1) + [1]
        for d in range(1, n):
            if n % d == 0:
                p, r = divide_monic(p, phi[d])
                assert r == [0]
        phi[n] = p
    return phi


def monomials(f, count):
    """Second reduction route: companion recurrence, no long division."""
    d = len(f)-1
    z = [1] + [0]*(d-1)
    out = []
    for _ in range(count):
        out.append(z[:])
        lead = z[-1]
        z = [0] + z[:-1]
        for j in range(d):
            z[j] -= lead*f[j]
    return out


def bareiss(a):
    a = [r[:] for r in a]
    n, old, sign = len(a), 1, 1
    if n == 0:
        return 1
    for k in range(n-1):
        pivot = next((r for r in range(k,n) if a[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k+1,n):
            for j in range(k+1,n):
                num = a[i][j]*a[k][k]-a[i][k]*a[k][j]
                assert num % old == 0
                a[i][j] = num//old
        old = a[k][k]
        for i in range(k+1,n):
            a[i][k] = 0
    return sign*a[-1][-1]


def norm_matrix(g, f):
    d = len(f)-1
    cols = []
    for j in range(d):
        c = reduce_poly([0]*j+g, f)
        cols.append(c+[0]*(d-len(c)))
    return bareiss([[cols[j][i] for j in range(d)] for i in range(d)])


def conjugate_product(g, f, L):
    result = [1]
    for r in range(L):
        if math.gcd(r,L) != 1:
            continue
        v = [0]*L
        for j,c in enumerate(g):
            v[(j*r)%L] += c
        result = reduce_poly(mul(result, reduce_poly(v,f)),f)
    return result


def blocks(N, B):
    q,r = divmod(N,B)
    s = 0
    for b in range(B):
        ell=q+(b<r)
        yield s,ell
        s += ell
    assert s == N


def policy(N,B,a,beta,x,phi, wrong_parity=False):
    L=math.lcm(2*N,4)
    f=phi[L]
    ms=monomials(f,L)
    polys, remainders, masses = [],[],[]
    for s,ell in blocks(N,B):
        g=[0]*L
        alt=[0]*(len(f)-1)
        for t in range(ell):
            h = 0 if wrong_parity else N%2
            r=(a*t*(t-1)+2*(a*s+beta)*t+h*t)%(2*N)
            e=(L//(2*N)*r)%L
            u,v=x[s+t]
            g[e]+=u
            g[(e+L//4)%L]+=v
            q=a*t*(t-1)//2+(a*s+beta)*t
            independently_formed_e=(L//N*q+(L//(2*N))*h*t)%L
            assert independently_formed_e == e
            for j in range(len(alt)):
                alt[j]+=u*ms[e][j]+v*ms[(e+L//4)%L][j]
        rem=reduce_poly(g,f)
        assert rem==trim(alt)
        A=sum(map(abs,g))
        assert A <= sum(abs(u)+abs(v) for u,v in x[s:s+ell])
        if rem != [0]:
            assert A>=1
        polys.append(trim(g)); remainders.append(rem); masses.append(A)
    return L,polys,remainders,masses


def ceil_log2(n):
    assert n>=1
    return (n-1).bit_length()


def precision_plan(N,B,W,K,q,t,D):
    H=min(math.comb(N+B-1,B),1<<(N-B))
    C=64*H*B*(1<<B)*N*N
    c=ceil_log2(C)
    G=W+(D-1)*K
    p=max(W,c+t+1,c+q+G+2)
    assert p>=W
    assert 2*C <= 1<<(p-t)
    assert C <= 1<<(p-q-G-2)
    assert N <= 1<<(2*q)
    return p,G,c


def main():
    rng=random.Random(202610161500)
    phi=cyclotomics(420)
    census={"cyclotomic_product_identities":0,"input_cases":0,"block_reductions":0,
            "exact_norm_comparisons":0,"precision_plans":0,"semantic_controls":0}
    for n in range(1,421):
        prod=[1]
        for d in range(1,n+1):
            if n%d==0: prod=mul(prod,phi[d])
        assert prod==[-1]+[0]*(n-1)+[1]
        assert len(phi[n])-1==sum(math.gcd(k,n)==1 for k in range(1,n+1))
        assert sum(map(abs,phi[n])) <= 1<<(len(phi[n])-1)
        census['cyclotomic_product_identities']+=1
    assert max(map(abs,phi[420]))==2
    census['semantic_controls']+=1

    for N in range(3,81):
        states=[(3,1,0),(N,N-1,N-1),(max(3,N//2),1,N//2)]
        for B,a,beta in states:
            for _ in range(3):
                x=[(rng.randrange(-5,6),rng.randrange(-5,6)) for j in range(N)]
                L,gs,hs,As=policy(N,B,a,beta,x,phi)
                census['input_cases']+=1
                census['block_reductions']+=B
                W=max(max(abs(u),abs(v)) for u,v in x).bit_length()
                for ell,g,h,A in zip((ell for _,ell in blocks(N,B)),gs,hs,As):
                    assert A < 2*ell*(1<<W)
                    if h!=[0]:
                        K=ceil_log2(A)
                        assert K<=W+ceil_log2(2*ell)

    for L in [8,12,16,20,24,28,32,36,40]:
        f=phi[L]
        for _ in range(12):
            g=[rng.randrange(-2,3) for j in range(min(L,6))]
            rem=reduce_poly(g,f)
            norm=norm_matrix(g,f)
            cp=conjugate_product(g,f,L)
            assert cp==[norm]
            assert (norm==0)==(rem==[0])
            if norm:
                assert abs(norm)>=1
                assert abs(norm)<=sum(map(abs,g))**(len(f)-1)
            census['exact_norm_comparisons']+=1

    # Exact nonzero input in projection kernel for a non-dyadic length.
    N,B=6,3
    x=[(1,0),(-1,0)]+[(0,0)]*(N-2)
    assert all(h==[0] for h in policy(N,B,1,0,x,phi)[2])
    assert any(u or v for u,v in x)
    census['semantic_controls']+=1

    # Dropping the odd-length phase falsely declares a nonzero target zero.
    N,B=9,3
    x=[(1,0),(-1,0)]+[(0,0)]*(N-2)
    assert any(h!=[0] for h in policy(N,B,1,0,x,phi)[2])
    assert all(h==[0] for h in policy(N,B,1,0,x,phi,True)[2])
    census['semantic_controls']+=1

    # Negacyclic reduction from the dyadic proof is invalid at L=12.
    f=phi[12]
    assert reduce_poly(f,f)==[0]
    assert divide_monic(f,[1]+[0]*5+[1])[1] == f
    census['semantic_controls']+=1

    # Original near-kernel data at a non-dyadic length retain width dependence.
    near=[]
    for k in [1,2,7,53,1024,65000]:
        N,B=6,3
        x=[(1<<k,0),(-((1<<k)-1),0)]+[(0,0)]*4
        L,gs,hs,As=policy(N,B,1,0,x,phi)
        assert hs[0]==[1] and As[0]==1
        p,G,c=precision_plan(N,B,k+1,0,ceil_log2(N),0,len(phi[L])-1)
        assert G==k+1
        near.append({"k":k,"p":p,"G":G})
        census['semantic_controls']+=1

    for N in list(range(3,81))+[105,127,255,257,1023,4096]:
        L=math.lcm(2*N,4)
        D=sum(math.gcd(k,L)==1 for k in range(1,L+1))
        for B in sorted({3,N,max(3,N//2)}):
            for W in [1,7,53,65536]:
                for K in [0,W,W+ceil_log2(2*N)]:
                    for t in [0,23]:
                        precision_plan(N,B,W,K,ceil_log2(N),t,D)
                        census['precision_plans']+=1

    # Constant-polynomial nonzero and exact-zero special cases, all length parities.
    for N in [3,4,5,6,7,8,9,10,15,21,35,105]:
        x=[(0,0)]*N
        assert all(h==[0] for h in policy(N,3,1,0,x,phi)[2])
        x[0]=(0,1)
        L,gs,hs,As=policy(N,3,1,0,x,phi)
        assert hs[0]!=[0] and As[0]==1
        assert reduce_poly([1]+[0]*(L//2-1)+[1],phi[L])==[0]
        census['semantic_controls']+=1

    result={"status":"PASS","scope":"Fresh exact algebra and planning controls only; no producer, wrapper, or downstream execution.",
            "counts":census,"near_kernel_plans":near,"cyclotomic_max_n":420,
            "controls_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out=Path(__file__).with_name('CHECK_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
