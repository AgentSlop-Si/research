"""Independent exact verifier: no imports from tensor_weil.py."""
from __future__ import annotations

from collections import Counter, deque
import json


def rank_mod(a, p):
    m=[row[:] for row in a];r=0
    for c in range(len(m[0])):
        pivot=next((i for i in range(r,len(m)) if m[i][c]%p),None)
        if pivot is None:continue
        m[r],m[pivot]=m[pivot],m[r]
        inv=pow(m[r][c],-1,p);m[r]=[x*inv%p for x in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][c]%p:
                f=m[i][c]%p;m[i]=[(x-f*y)%p for x,y in zip(m[i],m[r])]
        r+=1
    return r


def mul(a,b,p):
    bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]


def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]

def block(a,b,c,d):
    n=len(a);return [a[i]+b[i] for i in range(n)]+[c[i]+d[i] for i in range(n)]

def z(n):return [[0]*n for _ in range(n)]

def chirp(c,p):
    n=len(c);return block(eye(n),z(n),c,eye(n))

def inv2(a,p):
    n=len(a);aug=[row[:]+eye(n)[i] for i,row in enumerate(a)]
    for c in range(n):
        k=next(i for i in range(c,n) if aug[i][c]%p);aug[c],aug[k]=aug[k],aug[c]
        q=pow(aug[c][c],-1,p);aug[c]=[x*q%p for x in aug[c]]
        for i in range(n):
            if i!=c:
                f=aug[i][c]%p;aug[i]=[(x-f*y)%p for x,y in zip(aug[i],aug[c])]
    return [r[n:] for r in aug]

def lin(a,p):return block(a,z(len(a)),z(len(a)),list(map(list,zip(*inv2(a,p)))))
def pw(n,p):
    a=eye(n);d=eye(n);b=z(n);c=z(n);a[0][0]=d[0][0]=0;b[0][0]=-1%p;c[0][0]=1
    return block(a,b,c,d)
def key(m):return tuple(x for r in m for x in r)
def unkey(k):return [list(k[4*i:4*i+4]) for i in range(4)]
def brank(m,p):return rank_mod([r[2:] for r in m[:2]],p)

def sp4_distribution():
    p=3
    gens=[chirp([[1,0],[0,0]],p),chirp([[0,0],[0,1]],p),chirp([[0,1],[1,0]],p),
          lin([[0,1],[1,0]],p),lin([[1,1],[0,1]],p),lin([[2,0],[0,1]],p),pw(2,p)]
    start=key(eye(4));seen={start};q=deque([start]);cnt=Counter()
    while q:
        k=q.popleft();m=unkey(k);cnt[brank(m,p)]+=1
        for g in gens:
            nk=key(mul(g,m,p))
            if nk not in seen:seen.add(nk);q.append(nk)
    assert len(seen)==51840
    assert dict(cnt)=={0:1296,1:15552,2:34992}
    return dict(sorted(cnt.items()))


def cross_ratio_exponent():
    # Exact hand-selected fields: F_19 contains 9th roots; F_101 contains 25th roots.
    cases=[]
    for p,n,ell,zeta in [(3,2,19,4),(5,2,101,16)]:
        q=p**n
        assert pow(zeta,q,ell)==1 and pow(zeta,q//p,ell)!=1
        cyclic_ratio=zeta
        assert pow(cyclic_ratio,p,ell)!=1
        omega=pow(zeta,q//p,ell)
        # Tensor witness cross ratio is omega and therefore p-torsion.
        assert pow(omega,p,ell)==1
        cases.append({"p":p,"n":n,"cyclic_order_exceeds_p":True})
    return cases


def main():
    out={"sp4_3_rank_B_distribution":sp4_distribution(),"cross_ratio_cases":cross_ratio_exponent()}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
