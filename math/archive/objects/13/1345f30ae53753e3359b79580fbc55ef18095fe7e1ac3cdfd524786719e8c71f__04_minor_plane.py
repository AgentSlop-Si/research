"""Symbolic candidate minor gate on h0=1,h1=0 plane, exact Z[zeta8]."""
from pathlib import Path
import sys,time
from prior_loader import activate;activate()
from exact_polynomial_gate import build,det_sparse,p1,pzero,add,pmul,pscale,cpowroot,sub
from inverse_quartic import cadd,padd,poly_eval
from itertools import combinations

def specialize(P):
    # h0=1, h1=0, variables h2->0,h6->1
    out={}
    for mon,coeff in P.items():
        if 1 in mon:continue
        m=tuple(0 if k==2 else 1 for k in mon if k>1)
        out[m]=cadd(out.get(m,(0,0,0,0)),coeff)
        if out[m]==(0,0,0,0):del out[m]
    return out

def make_gate(obj):
    U=obj['Uhat'];L=obj['Lhat']
    Y={}
    for j in [1,2,4,5]:
        rows=[]
        for i in range(4 if j==4 else 5):
            A=pscale(p1,cpowroot(i*j))
            B=add(*[pscale(U[k],cpowroot(i*k)) for k in range(j)])
            C=add(*[pscale(L[k],cpowroot(i*k)) for k in range(j+1,8)])
            rows.append([A,B,C])
        Y[j]=rows
    TT=Y[4]
    cof=[pscale(det_sparse([TT[r] for r in range(4) if r!=i]),((-1)**i,0,0,0)) for i in range(4)]
    ell=[add(*[pmul(cof[i],Y[1][i][j]) for i in range(4)]) for j in range(3)]
    A,B,C=Y[1],Y[2],Y[5]
    K=[]
    for i in range(5):K.append([*A[i],*[pscale(x,(-1,0,0,0)) for x in B[i]],pzero,pzero,pzero])
    for i in range(5):K.append([*A[i],pzero,pzero,pzero,*[pscale(x,(-1,0,0,0)) for x in C[i]]])
    K.append(ell+[pzero]*6)
    return K

def main():
    st=time.monotonic();obj=build();print('build',round(time.monotonic()-st,1),flush=True)
    print('sliced polynomial sizes',[(k,len(specialize(obj[k]))) for k in ['W','DB','DH','Dhat']],flush=True)
    gate=make_gate(obj)
    small=[[specialize(entry) for entry in row] for row in gate]
    print('K ready',round(time.monotonic()-st,1),flush=True)
    samples=[]
    # prefer one from 10-row triple intersection (no ell) and one with ell and extra first row
    minors=[(0,1,2,3,5,6,7,8,9),(0,1,2,3,5,6,7,8,10),(0,1,2,4,5,6,7,8,10),(0,1,2,3,6,7,8,9,10)]
    for I in minors:
        t0=time.monotonic()
        Q=det_sparse([small[i] for i in I])
        print('minor',I,'terms',len(Q),'degree',max((len(m) for m in Q),default=0),'secs',round(time.monotonic()-t0,2),flush=True)
        samples.append((I,Q))
    return obj,samples

if __name__=='__main__':main()
