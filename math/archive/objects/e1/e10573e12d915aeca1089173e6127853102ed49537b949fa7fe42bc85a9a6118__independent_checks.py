#!/usr/bin/env python3
"""Independent Weyl monomial normal-form and paid recovery controls.
Auditor-authored standard-library code; no uploaded or constructor code imported.
Dense matrices are used only to generate and verify exact small controls.
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


def transpose(A):return list(map(list,zip(*A)))
def scale(t,A,p):return [[t*x%p for x in row] for row in A]
def plus(A,B,p):return [[(x+y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def primality(x):return x>=2 and all(x%d for d in range(2,math.isqrt(x)+1))
def roots(n):
    k=20
    while not primality(2*n*k+1):k+=1
    p=2*n*k+1;factors=[q for q in range(2,2*n+1) if 2*n%q==0 and primality(q)]
    for a in range(2,p):
        tau=pow(a,k,p)
        if all(pow(tau,2*n//q,p)!=1 for q in factors):return p,tau*tau%p,tau
    raise AssertionError

def weyl(n,w,p):
    return ([[int(i==(j+1)%n) for j in range(n)] for i in range(n)],[[pow(w,j,p)*int(i==j)%p for j in range(n)] for i in range(n)])
def fourier(n,w,p):return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]
def base(n,d,w,p):
    c=n//d;H=[[0]*n for _ in range(n)]
    for r in range(c):
        for k in range(d):
            for ell in range(d):H[r*d+k][r+c*ell]=pow(w,(-c*k*ell)%n,p)
    return H

def left_monomial(H,p,rng):
    rows=list(range(len(H)));rng.shuffle(rows)
    return [scale(rng.randrange(1,p),[H[i]],p)[0] for i in rows]
def mono(A,p):
    n=len(A);perm=[];weights=[]
    for j in range(n):
        ix=[i for i in range(n) if A[i][j]%p]
        if len(ix)!=1:return None
        perm.append(ix[0]);weights.append(A[ix[0]][j]%p)
    if len(set(perm))!=n:return None
    return perm,weights

def cycles(perm):
    seen=[False]*len(perm);out=[]
    for start in range(len(perm)):
        if seen[start]:continue
        z=start;C=[]
        while not seen[z]:seen[z]=True;C.append(z);z=perm[z]
        assert z==start;out.append(C)
    return out

def recover(U,V,w,p,seed_oracle):
    n=len(U[0]);a,uw=U;b,vw=V
    assert all(uw) and all(vw)
    for perm in [a,b]:
        seen=[False]*n
        for j in perm:assert 0<=j<n and not seen[j];seen[j]=True
    powers=[1]
    for i in range(1,n+1):
        powers.append(powers[-1]*w%p);assert powers[-1]!=1 or i==n
    assert powers[-1]==1
    C=cycles(b);d=len(C[0]);assert all(len(x)==d for x in C);c=len(C)
    products=[math.prod(vw[i] for i in x)%p for x in C]
    z=[j for j,x in enumerate(products) if x==1];assert len(z)==1
    which={x:j for j,Cj in enumerate(C) for x in Cj};order=[];j=z[0];visited=[False]*c
    for r in range(c):
        assert not visited[j];visited[j]=True;order.append(j);j=which[a[C[j][0]]]
    assert j==order[0];C=[C[j] for j in order]
    assert all(math.prod(vw[i] for i in Cr)%p==powers[(r*d)%n] for r,Cr in enumerate(C))
    loc={i:(r,k) for r,Cr in enumerate(C) for k,i in enumerate(Cr)};pref=[]
    for Cr in C:
        h=[1]
        for i in Cr[:-1]:h.append(h[-1]*vw[i]%p)
        pref.append(h)
    ainv=[0]*n
    for i,j in enumerate(a):ainv[j]=i
    seed=seed_oracle(C[0][0],0);assert seed!=0;gamma=[seed]
    for j in range(n-1):
        u=ainv[C[(j+1)%c][0]];r,k=loc[u];assert r==j%c
        gamma.append(uw[u]*gamma[-1]*pref[r][k]*powers[(-j*k)%n]%p)
    H=[[0]*n for _ in range(n)]
    for j in range(n):
        r=j%c
        for k,i in enumerate(C[r]):H[i][j]=gamma[j]*pref[r][k]*powers[(-j*k)%n]%p
    return H,{'d':d,'c':c,'seed_row':C[0][0],'seed_queries':1,'gamma_entries':n,'prefix_entries':n,
              'root_table_multiplications':n,'gamma_multiplications':3*(n-1),'cycle_product_multiplications':n,
              'prefix_multiplications':n-c,'dense_emission_entries':n*d}

def controls():
    rng=random.Random(43621);out=[]
    for n in list(range(1,17))+[18,20,24,27,32,36]:
        p,w,tau=roots(n);S,D=weyl(n,w,p);F=fourier(n,w,p)
        for d in [d for d in range(1,n+1) if n%d==0]:
            for twist in range(3):
                H=base(n,d,w,p)
                if twist:
                    chirp=[pow(w,j*(j-1)//2,p) if n%2 else pow(tau,j*j,p) for j in range(n)]
                    C=[[chirp[j]*int(i==j)%p for j in range(n)] for i in range(n)];H=product(H,C,p)
                    if twist==2:H=product(H,F,p)
                H=left_monomial(H,p,rng);HI=inv(H,p)
                U=mono(product(product(H,S,p),HI,p),p);V=mono(product(product(H,D,p),HI,p),p);assert U and V
                calls=[]
                def oracle(i,j):calls.append((i,j));return H[i][j]
                R,stats=recover(U,V,w,p,oracle);assert R==H and len(calls)==1
                assert {sum(x!=0 for x in row) for row in H}=={sum(x!=0 for x in col) for col in zip(*H)}=={stats['d']}
                for j in range(n):
                    for i in range(n):assert H[U[0][i]][(j+1)%n]==U[1][i]*H[i][j]%p
                R2,_=recover(U,V,w,p,lambda i,j:2*H[i][j]%p);assert R2==scale(2,H,p)
                out.append({'N':n,'field':p,'original_block':d,'twist':twist,'recovered':stats})
    return out

def interface_tests():
    out=[];sharp=[]
    for n in [3,4,6,8,9,12,16,25]:
        p,w,tau=roots(n);F=fourier(n,w,p);S,D=weyl(n,w,p);Si=transpose(S);ds=[d for d in range(1,n+1) if n%d==0]
        for dp in ds:
            P=transpose(base(n,dp,w,p));Pi=inv(P,p)
            A1=product(product(Pi,D,p),P,p);A2=product(product(Pi,Si,p),P,p)
            assert mono(transpose(A2),p) and mono(transpose(A1),p)
            calls=[]
            def p_seed(i,j):assert j==0;calls.append(i);return P[0][i]
            RP,st=recover(mono(transpose(A2),p),mono(transpose(A1),p),w,p,p_seed)
            assert RP==transpose(P) and st['d']==dp and len(calls)==1
            B=product(Pi,F,p);m=max(sum(x!=0 for x in row) for row in B);assert m*dp==n
            sharp.append({'N':n,'dP':dp,'dQ':1,'m':m})
            for dq in ds:
                Q=base(n,dq,w,p);Qi=inv(Q,p);T1=product(product(Q,S,p),Qi,p);T2=product(product(Q,D,p),Qi,p)
                assert mono(T1,p) and mono(T2,p)
                RQ,sq=recover(mono(T1,p),mono(T2,p),w,p,lambda i,j:Q[i][j]);assert RQ==Q
                B=product(product(Pi,F,p),Qi,p);m=max(sum(x!=0 for x in row) for row in B)
                assert product(B,T1,p)==product(A1,B,p) and product(B,T2,p)==product(A2,B,p) and m*dp*dq>=n
                out.append({'N':n,'dP':dp,'dQ':dq,'m':m,'bound_product':m*dp*dq})
    return {'cases':out,'sharp_Q_identity_cases':sharp}

def negative_tests():
    p=13;n=4;S,D=weyl(n,12,p);H=plus(ident(n),scale(2,product(S,S,p),p),p);HI=inv(H,p)
    U=product(product(H,S,p),HI,p);V=product(product(H,D,p),HI,p)
    assert mono(U,p) and mono(V,p) and all(sum(x!=0 for x in row)==2 for row in H)
    assert all(len(c)==1 for c in cycles(mono(V,p)[0]))
    p,w,_=roots(4);S,D=weyl(4,w,p);H=[[1,0,1,0],[1,0,p-1,0],[0,1,0,0],[0,0,0,1]];HI=inv(H,p)
    U=mono(product(product(H,S,p),HI,p),p);V=mono(product(product(H,D,p),HI,p),p)
    assert U is None and V and sorted(map(len,cycles(V[0])))==[1,1,2]
    p=13;w=3;n=3;S,D=weyl(n,w,p);F=fourier(n,w,p)
    H=[[F[i][j]*[1,1,2][j]%p for j in range(n)] for i in range(n)];HI=inv(H,p)
    assert mono(product(product(H,D,p),HI,p),p) and mono(product(product(H,S,p),HI,p),p) is None
    return {'nonprimitive_root_counterexample':{'N':4,'field':13,'omega':12,'H':'I+2S^2','H_row_support':2,'V_cycle_length':1},
            'single_conjugate_counterexample':{'N':4,'cycle_lengths':[1,1,2]},
            'unrestricted_converse_rejected':{'N':3,'field':13,'H':'F_3 diag(1,1,2)'}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='INDEPENDENT_RESULTS.json');args=ap.parse_args()
    r={'status':'PASS','constructor_or_uploaded_code_executed':False,'recovery_cases':controls(),'interfaces':interface_tests(),'negative_controls':negative_tests()}
    Path(args.output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print('PASS recovery',len(r['recovery_cases']),'interface',len(r['interfaces']['cases']),'sharp',len(r['interfaces']['sharp_Q_identity_cases']))
if __name__=='__main__':main()
