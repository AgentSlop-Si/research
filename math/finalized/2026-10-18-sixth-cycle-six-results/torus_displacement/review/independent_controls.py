#!/usr/bin/env python3
"""Reviewer-owned exact controls. No author or historical implementation imports."""
from pathlib import Path
from math import gcd,isqrt
from itertools import permutations
import json

P = 14401

def identity(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def plus(a,b,p=P): return [[(x+y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def minus(a,b,p=P):return [[(x-y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def times(a,b,p=P):
    out=[[0]*len(b[0]) for _ in a]
    for i,ar in enumerate(a):
        for k,x in enumerate(ar):
            if x:
                for j,y in enumerate(b[k]):out[i][j]=(out[i][j]+x*y)%p
    return out
def scaled(a,t,p=P): return [[t*x%p for x in ar] for ar in a]
def inv(a,p=P):
    n=len(a);work=[ar[:]+er for ar,er in zip(a,identity(n))]
    for j in range(n):
        hit=next(k for k in range(j,n) if work[k][j]%p)
        work[j],work[hit]=work[hit],work[j]
        work[j]=[x*pow(work[j][j],-1,p)%p for x in work[j]]
        for k in range(n):
            if k!=j:
                c=work[k][j];work[k]=[(x-c*y)%p for x,y in zip(work[k],work[j])]
    return [row[n:] for row in work]
def determinant(a,p=P):
    work=[r[:] for r in a];d=1;n=len(a)
    for j in range(n):
        hit=next((k for k in range(j,n) if work[k][j]),None)
        if hit is None:return 0
        if hit!=j:work[j],work[hit]=work[hit],work[j];d=-d
        c=work[j][j];d=d*c%p
        for k in range(j+1,n):
            scale=work[k][j]*pow(c,-1,p)%p
            for l in range(j+1,n):work[k][l]=(work[k][l]-scale*work[j][l])%p
            work[k][j]=0
    return d%p
def rank(a,p=P):
    work=[r[:] for r in a];r=0
    for j in range(len(a[0])):
        hit=next((k for k in range(r,len(a)) if work[k][j]),None)
        if hit is None:continue
        work[r],work[hit]=work[hit],work[r]
        c=pow(work[r][j],-1,p)
        for k in range(r+1,len(a)):
            f=work[k][j]*c%p
            for l in range(j,len(a[0])):work[k][l]=(work[k][l]-f*work[r][l])%p
        r+=1
    return r
def power(a,k,p=P):
    b=identity(len(a))
    for _ in range(k):b=times(b,a,p)
    return b
def factor(n):return [d for d in range(2,n+1) if n%d==0 and all(d%e for e in range(2,isqrt(d)+1))]
def exact_order(x,n,p=P):return pow(x,n,p)==1 and all(pow(x,n//l,p)!=1 for l in factor(n))
def primitive_generator(p=P):
    return next(g for g in range(2,p) if exact_order(g,p-1,p))
def orig(m,q,lam,p=P):
    n=m*m;L=identity(n);v=pow(4,-1,p)
    for a in range(m):
        for c in range(m):
            i=a*m+c;L[i][((a-1)%m)*m+c]-=v
            L[i][a*m+(c-1)%m]-=v*pow(q,a,p)
    L=[[x%p for x in row] for row in L]
    phi=[((-c)%m)*m+(a+c)%m for a in range(m) for c in range(m)]
    M=[[L[phi[i]][phi[j]] for j in range(n)] for i in range(n)]
    return L,M,plus(M,scaled(L,lam,p),p)
def row_family(m,q,lam,p=P):
    I=identity(m);U=[[int(j==(i-1)%m) for j in range(m)] for i in range(m)]
    Q=[[pow(q,-i,p)*int(i==j)%p for j in range(m)] for i in range(m)]
    W=plus(inv(U,p),Q,p);quarter=pow(4,-1,p)
    D=[minus(scaled(I,1+lam,p),scaled(U,lam*quarter*pow(q,a,p),p),p) for a in range(m)]
    R=scaled(plus(W,scaled(I,lam,p),p),quarter,p)
    return I,U,Q,W,D,R

def one(m,q,original_control):
    p=P;ell=4+m*(2*m-1).bit_length();lam=pow(2,-ell,p)
    I,U,Q,W,D,R=row_family(m,q,lam)
    E=I
    for Da in D:E=times(times(inv(Da),R),E)
    F=minus(I,E);FI=inv(F)
    displacements={}
    for aname,a in [('F',F),('Finv',FI)]:
        for xname,x in [('U',U),('Q',Q)]:
            det=determinant(minus(a,times(times(x,a),inv(x))));assert det
            displacements[aname+'_'+xname]=det
    # Truncated formal series up to z^2; each factor's coefficients derive from H^k.
    coeffs=[I,scaled(I,0),scaled(I,0)]
    for a in range(m):
        H=minus(I,scaled(U,pow(q,a,p)*pow(4,-1,p)))
        T0=scaled(W,pow(4,-1,p))
        T1=scaled(minus(I,times(H,W)),pow(4,-1,p))
        T2=scaled(minus(times(times(H,H),W),H),pow(4,-1,p))
        coeffs=[times(T0,coeffs[0]),plus(times(T0,coeffs[1]),times(T1,coeffs[0])),plus(plus(times(T0,coeffs[2]),times(T1,coeffs[1])),times(T2,coeffs[0]))]
    assert coeffs[0]==scaled(I,2*pow(4,-m,p))
    assert coeffs[1]==scaled(minus(inv(W),I),2*m*pow(4,-m,p))
    # Match actual full operator and its Schur boundary for one root per m.
    if original_control:
        L,M,K=orig(m,q,lam)
        Kr=[[((D[i//m][i%m][j%m] if i//m==j//m else 0)-(R[i%m][j%m] if j//m==(i//m-1)%m else 0))%p for j in range(m*m)] for i in range(m*m)]
        assert K==Kr
        cut=m*(m-1);A=[r[:cut] for r in K[:cut]];B=[r[cut:] for r in K[:cut]];C=[r[:cut] for r in K[cut:]];DD=[r[cut:] for r in K[cut:]]
        Schur=minus(DD,times(times(C,inv(A)),B));assert Schur==times(D[-1],F)
        assert determinant(K)==determinant(F)*__import__('functools').reduce(lambda x,Da:x*determinant(Da)%p,D,1)%p
    return {'m':m,'q':q,'first_variation':True,'displacement_determinants':displacements,'original_K_and_Schur':original_control}

def guard():
    p=79;m=2;q=p-1;lam=pow(256,-1,p)
    assert all(a*a%p!=p-1 for a in range(p))
    def fp2mul(x,y):return ((x[0]*y[0]-x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
    i=(0,1);i2=fp2mul(i,i);assert i2==(78,0) and fp2mul(i2,i2)==(1,0) and i2!=(1,0)
    L,M,K=orig(m,q,lam,p);I,U,Q,W,D,R=row_family(m,q,lam,p)
    # Leibniz determinants provide an independent elimination-free 4x4 control.
    def leibniz(a):
        answer=0
        for pi in permutations(range(len(a))):
            term=(-1)**sum(pi[x]>pi[y] for x in range(len(a)) for y in range(x+1,len(a)))
            for j,k in enumerate(pi):term=term*a[j][k]%p
            answer=(answer+term)%p
        return answer
    assert [leibniz(a) for a in [K,L,M]]==[39,2,2]
    S=plus(inv(L,p),scaled(inv(M,p),lam,p),p)
    assert leibniz(S)==69 and times(S,times(times(M,inv(K,p),p),L,p),p)==identity(4)
    assert [rank(d,p) for d in D]==[1,1]
    beta=lam*pow(4*(1+lam),-1,p)%p;assert beta==1
    return {'p':p,'extension_irreducible':True,'omega_order':4,'q_order':2,'lambda':lam,'beta':beta,'row_ranks':[1,1],'det_K':39,'det_L':2,'det_M':2,'det_S':69,'inverse_identity':True}

def main():
    assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in [79,P])
    g=primitive_generator();res=[]
    for m in [3,4,5,6,8,10,12]:
        assert (P-1)%(m*m)==0
        omega=pow(g,(P-1)//(m*m),P);assert exact_order(omega,m*m)
        q0=pow(omega,m,P)
        for k in range(1,m):
            if gcd(k,m)==1:res.append(one(m,pow(q0,k,P),k==1))
    result={'purpose':'Independent finite transcription controls, not proof of all sizes','moduli_prime':[79,P],'primitive_generator':g,'cases':res,'guard':guard(),'historical_programs_executed':False,'author_code_imported':False}
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'cases':len(res),'m_values':sorted({x['m'] for x in res}),'all_primitive_q_per_m':True,'all_assertions':True,'guard':result['guard']},indent=2))
if __name__=='__main__':main()
