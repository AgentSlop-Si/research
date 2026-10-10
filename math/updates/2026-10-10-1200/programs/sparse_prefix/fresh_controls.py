"""Fresh independent controls for the sparse-prefix proof; no source imports."""
from itertools import product, combinations, permutations
from math import comb, gcd
from random import Random
from pathlib import Path
import json

rng=Random(771041)
stats={}

def mm(A,B,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]

def invert(A,p):
    n=len(A); W=[[(x%p) for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next((k for k in range(j,n) if W[k][j]),None)
        if k is None: return None
        W[k],W[j]=W[j],W[k]
        q=pow(W[j][j],-1,p); W[j]=[x*q%p for x in W[j]]
        for k in range(n):
            if k!=j:
                q=W[k][j]; W[k]=[(x-q*y)%p for x,y in zip(W[k],W[j])]
    return [row[n:] for row in W]

def rank(A,p):
    if not A: return 0
    W=[row[:] for row in A]; at=0
    for j in range(len(W[0])):
        k=next((k for k in range(at,len(W)) if W[k][j]%p),None)
        if k is None: continue
        W[at],W[k]=W[k],W[at]; q=pow(W[at][j],-1,p)
        W[at]=[x*q%p for x in W[at]]
        for k in range(at+1,len(W)):
            q=W[k][j]; W[k]=[(x-q*y)%p for x,y in zip(W[k],W[at])]
        at+=1
        if at==len(W): break
    return at

def green_dense(weights,p):
    m=len(weights); A=[[int(i==j) for j in range(m)] for i in range(m)]
    for i,a in enumerate(weights): A[i][(i-1)%m]=(A[i][(i-1)%m]-a)%p
    return invert(A,p)

# Exhaustive uneven degree statistics, unrelated to uploaded implementation.
num=0; windows=0
for n in range(2,7):
    for degrees in product(range(1,5),repeat=n):
        total=sum(degrees); r=2*total//n
        assert sum(d<=r for d in degrees)*2>n
        for k in range(1,n+1):
            w=[sum(degrees[(i+j)%n] for j in range(k)) for i in range(n)]
            assert sum(w)==k*total
            assert min(w)<=k*total//n
            windows+=1
        num+=1
stats['exhaustive_degree_vectors']=num
stats['cyclic_window_averaging_checks']=windows

# Dense inverse, all small subsets, arbitrary zero weights and zero forcing.
plans=0; restrictions=0; zero_forcing=0; normal_forms=0
for p in (17,97):
    for m in range(1,9):
        for rep in range(15):
            weights=[rng.randrange(p) for _ in range(m)]
            if rep%3==0: weights[rng.randrange(m)]=0
            G=green_dense(weights,p)
            if G is None: continue
            C=[[rng.randrange(p) if rng.randrange(4)==0 else 0 for _ in range(4)] for _ in range(m)]
            V=mm(G,C,p)
            for size in range(5):
                for J in combinations(range(4),size):
                    f=sum(any(row[j] for j in J) for row in C); dirs=set()
                    for row in V:
                        v=[row[j] for j in J]; a=next((x for x in v if x),None)
                        if a is not None: dirs.add(tuple(x*pow(a,-1,p)%p for x in v))
                    assert len(dirs)<=f
                    restrictions+=1; zero_forcing+=int(f==0)
            if all(weights):
                w=[1]
                for a in weights[1:]: w.append(w[-1]*a%p)
                eta=1
                for a in weights: eta=eta*a%p
                rho=eta*pow((1-eta)%p,-1,p)%p
                H=[[(int(j<=i)+rho)*w[i]*pow(w[j],-1,p)%p for j in range(m)] for i in range(m)]
                assert G==H
                normal_forms+=1
            plans+=1
stats.update(dense_random_plans=plans,projective_restrictions=restrictions,
             zero_forcing_restrictions=zero_forcing,closed_cycle_normal_forms=normal_forms)

# Consecutive Fourier columns remain full spark after cyclic wrap.
minors=0
for p,n,w in ((17,8,2),(17,16,3),(97,6,36),(97,12,6)):
    assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
    for k in range(1,min(n,4)+1):
        for start in range(n):
            for rows in combinations(range(n),k):
                A=[[pow(w,i*((start+j)%n),p) for j in range(k)] for i in rows]
                assert rank(A,p)==k
                minors+=1
stats['consecutive_cyclic_vandermonde_minors']=minors

# Build finite Fourier controls from the mathematical identities only.
controls=[]
p=17
n=4; w=4
C=[[1,0,0,0],[0,0,1,0],[0,0,-2,0],[0,1,0,0],[0,0,0,1],[0,0,0,-2]]
R=[[0,1,0,0,1,0],[0,0,1,0,0,w],[0,1,0,0,-1,0],[0,0,1,0,0,-w]]
G=green_dense([0,1,1,0,1,1],p)
assert mm(mm(R,G,p),C,p)==[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
controls.append(dict(n=n,m=6,nnz_C=6,nnz_R=8,equals_fourier=True))
n=8; w=2; B=4; q=2; zeta=4
order=[0,2,1,3]; gammas=[0,1,pow(zeta,3,p),pow(zeta,2,p)]
C=[]; weights=[]
for t in range(q):
    prev=[0]*B
    for k,gamma in zip(order,gammas):
        cur=[pow(zeta,k*u,p) for u in range(B)]
        row=[0]*n
        for u in range(B): row[t+q*u]=(cur[u]-gamma*prev[u])%p
        C.append(row); weights.append(gamma); prev=cur
R=[[0]*n for _ in range(n)]
for k in range(n):
    for t in range(q): R[k][t*B+order.index(k%B)]=pow(w,k*t,p)
G=green_dense(weights,p)
assert mm(mm(R,G,p),C,p)==[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
nin=sum(bool(x) for row in C for x in row); nout=sum(bool(x) for row in R for x in row)
assert nin==22 and nout==16
assert max(sum(bool(row[j]) for row in C) for j in range(n))==3
assert max(sum(bool(x) for x in row) for row in R)==2
controls.append(dict(n=n,m=n,nnz_C=nin,nnz_R=nout,equals_fourier=True))
stats['finite_controls']=controls

# Alter one second-fiber read; the first column and degree caps remain correct.
R[0][B]=(R[0][B]+1)%p
wrong=mm(mm(R,G,p),C,p)
assert [row[0] for row in wrong]==[1]*n
assert wrong!=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
stats['seed_and_capacity_passing_phase_failure']=True

# Independently check the closed-tour scope correction.
tour_records=[]
for B in (2,4,8):
    best_open=best_closed=0
    for tail in permutations(range(1,B)):
        order=(0,)+tail
        score=sum(gcd(abs(order[i]-order[i-1]),B) for i in range(1,B))
        best_open=max(best_open,score)
        best_closed=max(best_closed,score+gcd(order[-1],B))
    assert best_open==(B*B-1)//3
    assert best_closed==(B*B+2)//3
    z=pow(3,16//B,17)
    order=[int(format(i,'0%db'%(B.bit_length()-1))[::-1],2) for i in range(B)]
    V=[[pow(z,k*u,17) for u in range(B)] for k in order]
    weights=[z]+[1]*(B-1)
    C=[[(V[i][u]-weights[i]*V[(i-1)%B][u])%17 for u in range(B)] for i in range(B)]
    G=green_dense(weights,17)
    assert mm(G,C,17)==V
    count=sum(bool(x) for row in C for x in row)
    assert count==(2*B*B-2)//3
    tour_records.append(dict(B=B,open_minimum=(2*B*B+1)//3,closed_minimum=count))
stats['row_tour_scope_correction']=tour_records

# Check the necessary d=4 cutoff.
assert 4*comb(20,4)==19380
assert 8<=2*comb(9,2) and 8<=3*comb(8,3)
stats['degree_four_capacity']=19380
stats['status']='PASS; finite controls support but do not prove the asymptotic theorem.'
Path(__file__).with_name('FRESH_CONTROL_RESULTS.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))

