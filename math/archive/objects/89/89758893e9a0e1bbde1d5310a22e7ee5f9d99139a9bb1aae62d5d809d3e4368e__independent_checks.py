#!/usr/bin/env python3
"""Independent bridge audit. Standard library only; no source programs imported.
Basic matrix primitives reused from the auditor-authored sparse-prefix checker.
All bridge, mutation, adjugate, gauge and solve controls authored separately here.
"""
import argparse,itertools as it,json,math,random
from pathlib import Path

def rank(A, p):
    B=[list(map(lambda x:x%p,row)) for row in A]
    if not B:return 0
    h=0
    for j in range(len(B[0])):
        z=next((z for z in range(h,len(B)) if B[z][j]),None)
        if z is None:continue
        B[z],B[h]=B[h],B[z]
        u=pow(B[h][j],-1,p)
        B[h]=[x*u%p for x in B[h]]
        for z in range(h+1,len(B)):
            u=B[z][j]
            if u:B[z]=[(x-u*y)%p for x,y in zip(B[z],B[h])]
        h+=1
        if h==len(B):break
    return h


def inv(A,p):
    n=len(A);B=[[(x%p) for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        z=next((z for z in range(j,n) if B[z][j]),None)
        assert z is not None
        B[z],B[j]=B[j],B[z]
        u=pow(B[j][j],-1,p);B[j]=[x*u%p for x in B[j]]
        for i in range(n):
            if i!=j and B[i][j]:
                u=B[i][j];B[i]=[(x-u*y)%p for x,y in zip(B[i],B[j])]
    return [row[n:] for row in B]


def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def sub(A,X,Y):return [[A[i][j] for j in Y] for i in X]
def product(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]


def plus(A,B,p):return [[(a+b)%p for a,b in zip(x,y)] for x,y in zip(A,B)]
def scale(c,A,p):return [[c*x%p for x in row] for row in A]
def vec(A,b,p):return [sum(x*y for x,y in zip(row,b))%p for row in A]
def addvec(a,b,p):return [(x+y)%p for x,y in zip(a,b)]


def det(A,p):
    B=[row[:] for row in A];ans=1
    for j in range(len(A)):
        z=next((z for z in range(j,len(A)) if B[z][j]%p),None)
        if z is None:return 0
        if z!=j:B[z],B[j]=B[j],B[z];ans=-ans
        u=B[j][j]%p;ans=ans*u%p;iu=pow(u,-1,p)
        for i in range(j+1,len(A)):
            f=B[i][j]*iu%p
            if f:
                for k in range(j+1,len(A)):B[i][k]=(B[i][k]-f*B[j][k])%p
    return ans%p


def adj_cofactors(A,p):
    n=len(A)
    return [[((-1)**(i+j)*det([[A[u][v] for v in range(n) if v!=i] for u in range(n) if u!=j],p))%p for j in range(n)] for i in range(n)]


def matpow(A,k,p):
    R=ident(len(A))
    for _ in range(k):R=product(R,A,p)
    return R


def cycden(n,p,rng,zero=False):
    order=list(range(n));rng.shuffle(order);succ=[0]*n
    for i,j in enumerate(order):succ[j]=order[(i+1)%n]
    w=[rng.randrange(1,p) for _ in range(n)]
    if zero:w[order[0]]=0
    if math.prod(w)%p==1:w[order[0]]=0
    A=ident(n)
    for i in range(n):A[i][succ[i]]=(A[i][succ[i]]-w[i])%p
    return A,order,succ,w


def solve_cycle(order,succ,w,b,p):
    # No inversion of individual edge weights, so zero edges are supported.
    z=1;beta=0
    for i in order:beta=(beta+z*b[i])%p;z=z*w[i]%p
    assert z!=1
    x=[0]*len(w);x[order[0]]=beta*pow((1-z)%p,-1,p)%p
    for i in reversed(order[1:]):x[i]=(b[i]+w[i]*x[succ[i]])%p
    return x,{'multiplications':3*len(w),'add_subtractions':2*len(w),'inversions':1}


def primality(x):return x>=2 and all(x%d for d in range(2,math.isqrt(x)+1))
def fourier(n):
    k=20
    while not primality(n*k+1):k+=1
    p=n*k+1;factors=[q for q in range(2,n+1) if n%q==0 and primality(q)]
    for a in range(2,p):
        w=pow(a,k,p)
        if all(pow(w,n//q,p)!=1 for q in factors):break
    assert pow(w,n,p)==1
    return p,w,[[pow(w,i*j,p) for j in range(n)] for i in range(n)]


def model_trials():
    rng=random.Random(727126);out=[];cofactor_cases=0;solve_cases=0
    for n in [2,3,5,7,8,11,13]:
        p,w,F=fourier(n)
        for trial in range(4):
            pars=[cycden(n,p,rng,(j+trial)%3==0) for j in range(4)]
            A,B,C,D=[z[0] for z in pars];AI,BI,CI,DI=[inv(z,p) for z in [A,B,C,D]]
            X=plus(A,B,p);Y=plus(C,D,p);K=product(C,B,p)
            M=product(plus(AI,BI,p),plus(CI,DI,p),p)
            sand=product(product(A,M,p),D,p)
            bridge=product(product(X,inv(K,p),p),Y,p)
            assert sand==bridge
            assert product(product(AI,bridge,p),DI,p)==M
            Kdet=det(K,p);Kadj=scale(Kdet,inv(K,p),p)
            assert scale(Kdet,sand,p)==product(product(X,Kadj,p),Y,p)
            assert det(M,p)*math.prod(det(z,p) for z in [A,B,C,D])%p==det(X,p)*det(Y,p)%p
            assert Kadj==product(scale(det(B,p),BI,p),scale(det(C,p),CI,p),p)
            if n<=5:assert Kadj==adj_cofactors(K,p);cofactor_cases+=1
            for Z,order,succ,ww in pars:
                assert det(Z,p)==(1-math.prod(ww))%p
                T=[[(int(i==j)-Z[i][j])%p for j in range(n)] for i in range(n)]
                assert matpow(T,n,p)==scale(math.prod(ww),ident(n),p)
                G=ident(n);power=ident(n)
                for _ in range(1,n):power=product(power,T,p);G=plus(G,power,p)
                assert G==scale(det(Z,p),inv(Z,p),p)
                b=[rng.randrange(p) for _ in range(n)];sol,cost=solve_cycle(order,succ,ww,b,p)
                assert vec(Z,sol,p)==b;solve_cases+=1
            b=[rng.randrange(p) for _ in range(n)]
            z,c1=solve_cycle(*pars[2][1:],b,p)
            z,c2=solve_cycle(*pars[1][1:],z,p)
            assert vec(K,z,p)==b
            # Gauge-independent covariance and initial-column certificate for F.
            assert all(F[i][(j+1)%n]==pow(w,i,p)*F[i][j]%p for i in range(n) for j in range(n))
            assert all(F[i][0]==1 for i in range(n))
            S=ident(n)
            for i in range(n):
                for j in range(n):S[i][j]=int(i==(j+1)%n)
            diag=[[pow(w,i,p)*int(i==j)%p for j in range(n)] for i in range(n)]
            assert product(F,S,p)==product(diag,F,p)
            scaled=scale(2,F,p);assert product(scaled,S,p)==product(diag,scaled,p) and scaled[0][0]!=1
            ones=[[1]*n for _ in range(n)];assert product(ones,S,p)!=product(diag,ones,p)
            wrong=product(product(X,inv(product(B,C,p),p),p),Y,p)
            explicit_max=lambda Z:max(max(sum(x!=0 for x in row) for row in Z),max(sum(x!=0 for x in col) for col in zip(*Z)))
            assert explicit_max(K)<=4 and explicit_max(X)<=3 and explicit_max(Y)<=3
            F_gate=scale(Kdet,product(product(A,F,p),D,p),p)==product(product(X,Kadj,p),Y,p)
            assert F_gate==(M==F)
            out.append({'N':n,'field':p,'trial':trial,'bridge_pass':True,'Fourier_gate_pass':F_gate,
                        'wrong_order_rejected':wrong!=bridge,'B_C_commute':product(B,C,p)==product(C,B,p),
                        'K_sparsity':explicit_max(K),'X_sparsity':explicit_max(X),'Y_sparsity':explicit_max(Y)})
    assert any(z['wrong_order_rejected'] for z in out)
    return {'trials':out,'cofactor_adjugate_controls':cofactor_cases,'cycle_solve_controls':solve_cases}


def singular_guard_control():
    n=3;p=13;S=[[int(j==(i+1)%n) for j in range(n)] for i in range(n)];I=ident(n)
    B=plus(I,scale(-1,S,p),p);C=plus(I,scale(-3,S,p),p);A=D=I
    K=product(C,B,p);Adj=adj_cofactors(K,p);F=[[pow(3,i*j,p) for j in range(n)] for i in range(n)]
    left=scale(det(K,p),F,p);right=product(product(plus(A,B,p),Adj,p),plus(C,D,p),p)
    assert det(A,p)==det(D,p)==1 and det(B,p)==det(C,p)==0 and rank(K,p)==1
    assert left==right==[[0]*n for _ in range(n)]
    return {'N':n,'field':p,'A_D_invertible':True,'B_C_determinants':[0,0],'K_rank':1,'adjK_zero':True,'polynomial_equation_vacuous_for_any_target':True}


def scalar_det_control():
    n=3;p=13;omega=3;F=[[pow(omega,i*j,p) for j in range(n)] for i in range(n)]
    S=[[int(j==(i+1)%n) for j in range(n)] for i in range(n)];I=ident(n)
    choices=[a for a in range(p) if pow(a,n,p)!=1]
    mats={a:plus(I,scale(-a,S,p),p) for a in choices};ivs={a:inv(mats[a],p) for a in choices}
    for aa,bb,cc,dd in it.product(choices,repeat=4):
        # Eigenvalue product cheaply chooses a determinant match, then full matrix checks it.
        ev=[((pow((1-aa*pow(omega,k,p))%p,-1,p)+pow((1-bb*pow(omega,k,p))%p,-1,p))*(pow((1-cc*pow(omega,k,p))%p,-1,p)+pow((1-dd*pow(omega,k,p))%p,-1,p)))%p for k in range(n)]
        if math.prod(ev)%p!=det(F,p):continue
        A,B,C,D=[mats[a] for a in [aa,bb,cc,dd]]
        M=product(plus(ivs[aa],ivs[bb],p),plus(ivs[cc],ivs[dd],p),p)
        assert M!=F and det(M,p)==det(F,p)
        assert det(F,p)*math.prod(det(z,p) for z in [A,B,C,D])%p==det(plus(A,B,p),p)*det(plus(C,D,p),p)%p
        return {'N':n,'field':p,'constant_weights':[aa,bb,cc,dd],'Fourier_determinant':det(F,p),'product_determinant':det(M,p),'product_is_Fourier':False,'M':M,'F':F}
    raise AssertionError('No determinant-only control found')


def gauge_scope_control():
    n=5;p=101;I=ident(n);S=[[int(j==(i+1)%n) for j in range(n)] for i in range(n)]
    A=plus(I,scale(-2,S,p),p);B=product(plus(I,scale(-3,S,p),p),matpow(S,2,p),p)
    C=plus(I,scale(-4,S,p),p);D=plus(I,scale(-5,S,p),p)
    assert all(det(Z,p) for Z in [A,B,C,D])
    X=plus(A,B,p);Y=plus(C,D,p);K=product(C,B,p)
    M=product(plus(inv(A,p),inv(B,p),p),plus(inv(C,p),inv(D,p),p),p)
    assert product(product(A,M,p),D,p)==product(product(X,inv(K,p),p),Y,p)
    assert all(sum(v!=0 for v in row)==4 for row in X)
    return {'N':n,'field':p,'general_bridge_still_valid':True,'gauged_sum_row_support':4,'gauged_sum_column_support':4,'A':'I-2S','B':'(I-3S)S^2'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='INDEPENDENT_RESULTS.json');args=ap.parse_args()
    trials=model_trials()
    report={'status':'PASS','uploaded_code_executed':False,'classification':'equivalent synthesis obligation, no Fourier construction',
            'model_trials':trials,'missing_denominator_guard':singular_guard_control(),
            'determinant_only_false_accept':scalar_det_control(),'monomial_gauge_scope':gauge_scope_control()}
    Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS independent bridge controls; trials',len(trials['trials']))
    print('Wrong order rejected:',sum(x['wrong_order_rejected'] for x in trials['trials']))
    print('Fourier passes:',sum(x['Fourier_gate_pass'] for x in trials['trials']))
    print('Scalar-only false accept:',report['determinant_only_false_accept'])
if __name__=='__main__':main()
