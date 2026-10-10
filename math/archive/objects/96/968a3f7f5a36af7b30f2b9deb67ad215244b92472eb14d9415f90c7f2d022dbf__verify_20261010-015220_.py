#!/usr/bin/env python3
"""Exact modular test of two-sided free-gauge Fourier/Green Segre-eigenvector gate.
No NumPy for exact modular algebra; all inversions and determinants checked in GF(97).
"""
import json, random, math
from pathlib import Path
Q=97
RNG=random.Random(20261010)

def mul(A,B,p=Q):
    n=len(A); m=len(B[0]); r=len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(r))%p for j in range(m)] for i in range(n)]

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def diag(d):return [[d[i] if i==j else 0 for j in range(len(d))] for i in range(len(d))]
def det(A,p=Q):
    n=len(A);B=[r[:] for r in A]; out=1
    for j in range(n):
        k=next((i for i in range(j,n) if B[i][j]%p),None)
        if k is None:return 0
        if k!=j: B[j],B[k]=B[k],B[j];out=-out
        t=B[j][j]%p;out=out*t%p
        inv=pow(t,-1,p)
        for i in range(j+1,n):
            f=B[i][j]*inv%p
            for h in range(j,n):B[i][h]=(B[i][h]-f*B[j][h])%p
    return out%p

def inv(A,p=Q):
    n=len(A);B=[[(v%p) for v in row]+I for row,I in zip(A,eye(n))]
    for j in range(n):
        k=next((i for i in range(j,n) if B[i][j]%p),None)
        if k is None:raise ValueError('singular')
        B[j],B[k]=B[k],B[j]
        t=pow(B[j][j],-1,p);B[j]=[v*t%p for v in B[j]]
        for i in range(n):
            if i!=j:
                a=B[i][j]
                B[i]=[(B[i][h]-a*B[j][h])%p for h in range(2*n)]
    return [r[n:] for r in B]

def add(A,B,p=Q):return [[(u+v)%p for u,v in zip(x,y)] for x,y in zip(A,B)]
def sub(A,B,p=Q):return [[(u-v)%p for u,v in zip(x,y)] for x,y in zip(A,B)]
def transpose(A):return [list(r) for r in zip(*A)]
def vec(A,v,p=Q):return [sum(a*b for a,b in zip(row,v))%p for row in A]
def hadamard_div(A,B,p=Q):return [[u*pow(v,-1,p)%p for u,v in zip(x,y)] for x,y in zip(A,B)]

def primitive_root_order(n,p=Q):
    assert (p-1)%n==0
    for base in range(2,p):
        w=pow(base,(p-1)//n,p)
        if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in prime_factors(n)):return w
    raise RuntimeError

def prime_factors(n):
    f=[]; d=2
    while d*d<=n:
        if n%d==0:
            f.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:f.append(n)
    return f

def Fourier(n,p=Q):
    w=primitive_root_order(n,p)
    return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]

def cycle(n,rng=RNG):
    c=list(range(n));rng.shuffle(c); pi=[0]*n
    for i,j in zip(c,c[1:]+c[:1]):pi[i]=j
    return pi

def weighted_green(n,rng=RNG,permuted=True,trace=None):
    weights=[rng.choice([-3,-2,-1,1,2,3])%Q for _ in range(n)]
    sigma=cycle(n,rng)
    W=eye(n)
    for i in range(n):W[i][sigma[i]]=(W[i][sigma[i]]-weights[i])%Q
    try:G=inv(W)
    except ValueError:return weighted_green(n,rng,permuted,trace)
    ld=[rng.choice([1,2,3,5,7])%Q for _ in range(n)]
    rd=[rng.choice([-2,-1,1,2,3])%Q for _ in range(n)]
    G=mul(diag(ld),mul(G,diag(rd)))
    perm1=list(range(n));perm2=list(range(n))
    if permuted:
        rng.shuffle(perm1);rng.shuffle(perm2)
        G=[[G[perm1[i]][perm2[j]] for j in range(n)] for i in range(n)]
    if trace is not None:
        trace.append({'cycle':sigma, 'weights':[v if v<Q//2 else v-Q for v in weights],
          'left_diag':[v if v<Q//2 else v-Q for v in ld],
          'right_diag':[v if v<Q//2 else v-Q for v in rd],
          'row_permutation':perm1,'col_permutation':perm2})
    return G

def green_sum(n,rng=RNG,trace=None):
    return add(weighted_green(n,rng,trace=trace),weighted_green(n,rng,trace=trace))

def P_columns(A,B,C,F):
    n=len(A); AI=inv(A);CI=inv(C);H=mul(F,CI)
    assert all(all(t%Q for t in row) for row in B)
    result=[]
    for j in range(n):
        bv=[B[u][j] for u in range(n)]
        hv=[H[i][j] for i in range(n)]
        result.append(mul(diag([pow(v,-1,Q) for v in bv]),mul(AI,diag(hv))))
    return result

def get_commutator(A,B,C,F):
    Ps=P_columns(A,B,C,F)
    P0_inv=inv(Ps[0])
    T=[mul(P0_inv,Ps[j]) for j in range(len(A))]
    assert len(T)>=3
    K=sub(mul(T[1],T[2]),mul(T[2],T[1]))
    return det(K),K,T,Ps

def test_random_wiring(n,trial_count=16,two_stage=False):
    F=Fourier(n)
    cert=[]; attempts=0; singular_comm=0
    while len(cert)<trial_count and attempts<trial_count*20:
        attempts+=1
        try:
            trace=[]
            A=green_sum(n,trace=trace);B=green_sum(n,trace=trace);C=eye(n) if two_stage else green_sum(n,trace=trace)
            if not (det(A) and det(B) and det(C)):continue
            cm,K,T,Ps=get_commutator(A,B,C,F)
            if not cm:singular_comm+=1;continue
            assert det(Ps[0])
            assert all(x for row in B for x in row)
            if not cert:
                # Save first deterministic modular certificate with all matrices and permutation-derived Green sums.
                cert.append({'N':n,'field':Q,'root':primitive_root_order(n),'two_stage':two_stage,'A':A,'B':B,'C':C,'branch_parameters':trace,'P0':Ps[0], 'T1':T[1], 'T2':T[2],'commutator':K,'det_commutator':cm})
            else:
                cert.append({'det_commutator':cm})
        except (ValueError,AssertionError):continue
    assert len(cert)==trial_count,(n,len(cert),attempts)
    return {'N':n,'two_stage':two_stage,'trials':len(cert),'attempts':attempts,'singular_commutators_discarded':singular_comm,'first_det':cert[0]['det_commutator']},cert[0]

def positive_control(n,two_stage=False):
    F=Fourier(n)
    # Fully nontrivial A,C with B chosen to ensure exact identity for nonzero free gauges.
    for _ in range(200):
        A=green_sum(n); C=eye(n) if two_stage else green_sum(n)
        if not (det(A) and det(C)):continue
        d=[RNG.randrange(1,Q) for i in range(n)]
        e=[RNG.randrange(1,Q) for i in range(n)]
        c=[RNG.randrange(1,Q) for i in range(n)]
        B=mul(diag([pow(v,-1,Q) for v in d]),mul(inv(A),mul(diag(c),mul(F,mul(inv(C),diag([pow(v,-1,Q) for v in e]))))))
        if any(x==0 for row in B for x in row):continue
        Ps=P_columns(A,B,C,F)
        if det(Ps[0])==0: continue
        W=[vec(P,c) for P in Ps]
        assert all(W[j][i]==d[i]*e[j]%Q for j in range(n) for i in range(n))
        reconstructed=mul(diag([pow(v,-1,Q) for v in c]),mul(A,mul(diag(d),mul(B,mul(diag(e),C)))))
        assert reconstructed==F
        _,_,T,_=get_commutator(A,B,C,F)
        assert all(vec(T[j],c)==[e[j]*pow(e[0],-1,Q)*v%Q for v in c] for j in range(n))
        return {'N':n,'two_stage':two_stage,'pass':True,'A_det':det(A),'B_det':det(B),'C_det':det(C),'known_seed':c}
    raise AssertionError('could not build positive control')

def sparse_common_eigen_control(n=4):
    F=Fourier(n); A=eye(n); C=eye(n)
    B=[[1+(i==j) for j in range(n)] for i in range(n)]
    assert det(B)!=0
    P=P_columns(A,B,C,F);iP0=inv(P[0]);Ts=[mul(iP0,P[j]) for j in range(n)]
    K=sub(mul(Ts[1],Ts[2]),mul(Ts[2],Ts[1]))
    assert det(K)==0
    # Nevertheless no all-nonzero vector c yields rank-one W(c), as F/B is full rank.
    Qm=hadamard_div(F,B)
    assert det(Qm)!=0
    return {'N':n,'commutator_det':det(K),'hadamard_quotient_det':det(Qm),'lesson':'Commutator singularity does not imply admissible Fourier gauges.'}

def main():
    random_result={}; witnesses=[]
    for two_stage in (True,False):
        for n in (3,4,6,8):
            if (Q-1)%n:continue
            x,w=test_random_wiring(n,trial_count=8,two_stage=two_stage)
            random_result[('four_green_' if two_stage else 'six_green_')+str(n)]=x; witnesses.append(w)
    ctrl=[positive_control(n,two_stage=typ) for typ in (True,False) for n in (3,4,8)]
    edge=sparse_common_eigen_control(4)
    data={'field':Q,'negative_green_wirings':random_result,'positive_gauge_controls':ctrl,'commutator_not_sufficient_control':edge}
    folder=Path(__file__).parent
    (folder/'RESULTS.json').write_text(json.dumps(data,indent=2))
    (folder/'CERTIFICATES.json').write_text(json.dumps(witnesses,indent=2))
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
