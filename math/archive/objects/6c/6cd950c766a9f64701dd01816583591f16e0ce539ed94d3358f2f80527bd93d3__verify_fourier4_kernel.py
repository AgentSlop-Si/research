#!/usr/bin/env python3
"""Exact authored finite-field controls; no downloaded executable dependencies."""
import json
from pathlib import Path


def mm(a,b,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]


def rank(a,p):
    a=[r[:] for r in a]; k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]%p),None)
        if pivot is None: continue
        a[k],a[pivot]=a[pivot],a[k]
        t=pow(a[k][j],-1,p);a[k]=[v*t%p for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                t=a[i][j];a[i]=[(x-t*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k


def primitive(p,n):
    return next(a for a in range(2,p) if pow(a,n,p)==1 and all(pow(a,d,p)!=1 for d in range(1,n) if n%d==0))


def f4(p):
    chi=primitive(p,8);ii=chi*chi%p;h=(chi+pow(chi,-1,p))%p;a=pow(chi,-1,p)
    roots=[z for z in range(p) if (z*z+h*z+ii)%p==0]
    if len(roots)!=2:return {'prime':p,'split_distinct':False,'root_count':len(roots)}
    r,s=roots;A=(a-s)*pow(r-s,-1,p)%p;B=(r-a)*pow(r-s,-1,p)%p
    guards=[(1-pow(t,4,p))%p for t in roots]
    assert all([r,s,A,B,*guards]) and guards[0]*guards[1]%p==8*ii%p
    e=[pow(chi,j*j,p) for j in range(4)]
    kernels=[]
    for z,g in zip(roots,guards):
        G=[[pow(z,(u-v)%4,p)*pow(g,-1,p)%p for v in range(4)]for u in range(4)]
        U=[[(int(u==v)-(z if u==(v+1)%4 else 0))%p for v in range(4)]for u in range(4)]
        assert mm(U,G,p)==[[int(u==v)for v in range(4)]for u in range(4)]
        kernels.append(G)
    ans=[[e[u]*e[v]*(A*guards[0]*kernels[0][u][v]+B*guards[1]*kernels[1][u][v])%p for v in range(4)]for u in range(4)]
    assert ans==[[pow(ii,u*v,p)for v in range(4)]for u in range(4)]
    return {'prime':p,'chi':chi,'i':ii,'h':h,'r':r,'s':s,'A':A,'B':B,'guards':guards,'guard_product':8*ii%p,'all_eight_masks_nonzero':True,'all_endpoints_nonzero':True,'exact_F4':True}


def f8_chart(p):
    chi=primitive(p,16);c=[pow(chi,(-t*t)%16,p)for t in range(8)]
    a=[[c[(k-j)%8]for j in range(5)]for k in range(3,8)]
    rr=rank(a,p);assert rr==5
    return {'prime':p,'chi16':chi,'constraint_matrix_rank':rr,'chart_empty':True}


out={'F4_controls':[f4(p)for p in (17,41,73,89,97,113,137,193,233,241,257)],'F8_commuting_chart_controls':[f8_chart(p)for p in (17,97,113,193,241,257)],'all_exact_assertions_passed':True,'scope':'F4 finite local kernel; no F8 factorization and no automatic Hamiltonian batch lift.'}
assert sum('exact_F4'in c for c in out['F4_controls'])>=3
Path(__file__).with_name('FOURIER4_KERNEL_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
