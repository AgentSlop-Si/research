#!/usr/bin/env python3
"""Reviewer-created cross-track and determinant controls; no upload imports."""
import json,math
from pathlib import Path
from independent_checks import field,dft,rank

def determinant(a,p):
    a=[list(row) for row in a];out=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]%p),None)
        if pivot is None:return 0
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];out=-out
        z=a[j][j]%p;out=out*z%p;iz=pow(z,-1,p)
        for i in range(j+1,len(a)):
            factor=a[i][j]*iz%p
            for k in range(j,len(a)):a[i][k]=(a[i][k]-factor*a[j][k])%p
    return out%p

def main():
    out={'peer_hankel_determinants':0,'bridge_cases':[],'uploaded_code_executed':False}
    for m in range(2,30):
        p,w=field(m*m)
        for h in range(m):
            q=pow(w,1-m*h,p);F=[1]
            for r in range(1,m):F.append(F[-1]*(1-pow(q,r,p))%p)
            d=[pow(q,r*(r-1)//2,p)*pow(F[r],-1,p)%p for r in range(m)]
            for n in range(1,(m+1)//2+1):
                assert 2*n-2<m
                H=[[d[i+j] for j in range(n)] for i in range(n)]
                predicted=pow(q,sum(j*(j-1)//2 for j in range(n)),p)
                for i in range(n):
                    predicted=predicted*d[i]%p
                    for k in range(1,n):predicted=predicted*pow((1-pow(q,i+k,p))%p,-1,p)%p
                for i in range(n):
                    for ell in range(i+1,n):predicted=predicted*(pow(q,ell,p)-pow(q,i,p))%p
                got=determinant(H,p)
                assert got==predicted and got!=0
                out['peer_hankel_determinants']+=1
    # Layout bridge plus explicit dense one-template witnesses requiring growing temporal recurrence order.
    for k,m in [(4,2),(8,4),(16,8),(32,16),(64,32)]:
        p,w=field(k*m);eta=pow(w,m,p);nu=1;a=1;beta=3
        f=[2]+[1]*(k-1);g=list(range(m));F=dft(f,eta,p)
        assert all(F)
        desired=[pow(t+1,-1,p) for t in range(m)]
        h=[]
        for t in range(m):
            factor=pow(w,-a*t*(t-1)//2-beta*t,p)*pow(eta,(nu+a*t)*g[t],p)*F[(nu+a*t)%k]%p
            h.append(desired[t]*pow(factor,-1,p)%p)
        raw=[h[t]*f[(b+g[t])%k]*pow(w,-a*t*(t-1)//2-(a*m*b+beta)*t,p)%p for b in range(k) for t in range(m)]
        C=[dft([raw[t+m*b] for b in range(k)],eta,p) for t in range(m)]
        for t in range(m):
            for channel in range(k):
                target=h[t]*pow(w,-a*t*(t-1)//2-beta*t,p)*pow(eta,(channel+a*t)*g[t],p)*F[(channel+a*t)%k]%p
                assert C[t][channel]==target
        assert [C[t][nu] for t in range(m)]==desired
        s=(m+1)//2
        temporal=rank([[C[i+j][nu] for j in range(s)] for i in range(s)],p)
        V=[[h[t]*f[(b+g[t])%k]%p for t in range(m)] for b in range(k)]
        assert temporal==s and rank(V,p)==m and all(raw)
        out['bridge_cases'].append({'phase7_K':k,'phase7_m':m,'phase4_Q':m,'phase4_M':k,'N':k*m,'p':p,'root':w,'dense_input':True,'ordinary_dechirped_rank':m,'temporal_hankel_rank':temporal,'selected_channel':nu,'selected_temporal_sequence':'C_t[nu] = 1/(t+1)'})
    return out

if __name__=='__main__':
    result=main();Path(__file__).with_name('BRIDGE_HANKEL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
