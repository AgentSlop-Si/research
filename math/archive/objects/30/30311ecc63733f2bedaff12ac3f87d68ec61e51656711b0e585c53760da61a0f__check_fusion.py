#!/usr/bin/env python3
"""Exact finite-field checks of decoded-state BM fusion. No speed claims."""
import json, random
from pathlib import Path

P = 97
rng = random.Random(20261009)
counts = {"one_step": 0, "macro_step": 0, "full_tree": 0,
          "bm_intertwining": 0, "remainder_transpose": 0,
          "root_collision_nodes": 0, "generic_convolution_embedding": 0}

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]=(c[i+j]+x*y)%P
    return c

def inv(q,n):
    h=[pow(q[0],-1,P)]
    for i in range(1,n):
        h.append(-sum(q[j]*h[i-j] for j in range(1,min(i,len(q)-1)+1))*h[0]%P)
    return h

def pad(a,n): return a[:n]+[0]*max(0,n-len(a))
def q_from_roots(ws):
    q=[1]
    for w in ws: q=mul(q,[1,-w%P])
    return q

def samples(ws,bs,n):
    return [sum(b*pow(w,j,P) for b,w in zip(bs,ws))%P for j in range(n)]

def numerator(ws,bs):
    out=[0]*len(ws)
    for s,b in enumerate(bs):
        pol=q_from_roots(ws[:s]+ws[s+1:])
        for j,c in enumerate(pol): out[j]=(out[j]+b*c)%P
    return out

def extension(q,v,n):
    L=len(v)
    r=mul(q,v)[L:]
    if n<=L: return v[:n]
    tail=pad(mul(r,inv(q,n-L)),n-L)
    return v+[-x%P for x in tail]

def branch(p,q):
    qm=[c if j%2==0 else -c%P for j,c in enumerate(q)]
    u=mul(p,qm)
    qq=mul(q,qm)
    assert not any(qq[1::2])
    return u[::2], u[1::2], qq[::2]

def rem(a,mod):
    a=a[:]
    d=len(mod)-1
    for i in range(len(a)-1,d-1,-1):
        c=a[i]*pow(mod[d],-1,P)%P
        for j in range(d+1): a[i-d+j]=(a[i-d+j]-c*mod[j])%P
    return pad(a,d)

# 5 generates F_97^*. Every divisor N includes valid distinct Nth roots.
assert len({pow(5,j,P) for j in range(96)}) == 96
for N in [1,2,3,4,6,8,12,16,24,32,48,96]:
    root=pow(5,96//N,P)
    for trial in range(18):
        k=rng.randrange(1,min(N,12)+1)
        zs=[pow(root,e,P) for e in rng.sample(range(N),k)]
        aa=[rng.randrange(P) for _ in range(k)]
        for L in sorted({k, 1<<(k-1).bit_length(),2*k}):
            D=max(0,(max(1,(N+L-1)//L)-1).bit_length())
            nodes={0:samples(zs,aa,L)}
            ws=zs[:]
            for ell in range(D+1):
                q=q_from_roots(ws)
                if len(set(ws))<k: counts["root_collision_nodes"]+=len(nodes)
                for r,v in nodes.items():
                    bs=[a*pow(z,r,P)%P for a,z in zip(aa,zs)]
                    direct=samples(ws,bs,2*L)
                    assert extension(q,v,2*L)==direct
                    counts["one_step"]+=1
                    macro=samples(ws,bs,4*L)
                    assert extension(q,v,4*L)==macro
                    counts["macro_step"]+=1
                    pp=numerator(ws,bs)
                    pe,po,qn=branch(pp,q)
                    ce=pad(mul(pe,inv(qn,L)),L)
                    co=pad(mul(po,inv(qn,L)),L)
                    assert ce==direct[::2] and co==direct[1::2]
                    counts["bm_intertwining"]+=1
                if ell<D:
                    nextnodes={}
                    for r,v in nodes.items():
                        ext=extension(q,v,2*L)
                        nextnodes[r]=ext[::2]
                        nextnodes[r+(1<<ell)]=ext[1::2]
                    nodes=nextnodes
                    ws=[w*w%P for w in ws]
            out=[None]*((1<<D)*L)
            for r,v in nodes.items():
                for j,x in enumerate(v): out[r+(1<<D)*j]=x
            assert out[:N]==samples(zs,aa,N)
            counts["full_tree"]+=1
        # Exact full sparse Vandermonde = transpose of polynomial remainder
        # composed with initial k-sample Vandermonde.
        q=q_from_roots(zs)
        A=q[::-1]
        v=samples(zs,aa,k)
        n=max(N,k+1)
        output=[]
        for m in range(n):
            r=rem([0]*m+[1],A)
            output.append(sum(x*y for x,y in zip(r,v))%P)
        assert output==samples(zs,aa,n)
        counts["remainder_transpose"]+=1

# Generic (not root-of-unity-restricted) J contains arbitrary convolution.
for m in range(1,14):
    for _ in range(10):
        ac=[rng.randrange(P) for _ in range(m+1)]
        ac[-1]=rng.randrange(1,P)
        q=[1]+[0]*(m-1)+ac
        u=[rng.randrange(P) for _ in range(m)]
        v=[0]*m+u
        got=extension(q,v,4*m)[2*m:3*m]
        want=[-x%P for x in pad(mul(ac,u),m)]
        assert got==want
        counts["generic_convolution_embedding"]+=1

result={"field":P,"seed":20261009,"status":"all passed","counts":counts,
        "scope":"Algebraic correctness only; no timing or circuit lower-bound claim."}
Path(__file__).with_name('fusion_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
