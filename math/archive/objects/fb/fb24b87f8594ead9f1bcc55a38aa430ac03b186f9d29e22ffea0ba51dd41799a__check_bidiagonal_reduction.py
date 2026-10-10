"""Independent exact tests; no code imported from user uploads."""
import json, random
P=998244353

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(A,B): return [[sum(a*b for a,b in zip(row,col))%P for col in zip(*B)] for row in A]
def add(*As): return [[sum(vals)%P for vals in zip(*rows)] for rows in zip(*As)]
def diag(v): return [[v[i] if i==j else 0 for j in range(len(v))] for i in range(len(v))]
def rank(A):
    A=[r[:] for r in A]; m=len(A); n=len(A[0]) if m else 0; r=0
    for j in range(n):
        pivot=next((i for i in range(r,m) if A[i][j]),None)
        if pivot is None: continue
        A[r],A[pivot]=A[pivot],A[r]; q=pow(A[r][j],-1,P); A[r]=[v*q%P for v in A[r]]
        for i in range(r+1,m):
            q=A[i][j]; A[i]=[(v-q*w)%P for v,w in zip(A[i],A[r])]
        r+=1
        if r==m: break
    return r

def inv(A):
    n=len(A); T=[row[:]+unit for row,unit in zip(A,eye(n))]
    for j in range(n):
        pivot=next((i for i in range(j,n) if T[i][j]),None)
        if pivot is None: raise ValueError('singular')
        T[j],T[pivot]=T[pivot],T[j]; q=pow(T[j][j],-1,P); T[j]=[v*q%P for v in T[j]]
        for i in range(n):
            if i!=j:
                q=T[i][j]; T[i]=[(v-q*w)%P for v,w in zip(T[i],T[j])]
    return [r[n:] for r in T]

def check(a,b,c,e,d):
    n=len(a); A=eye(n); C=eye(n)
    for i in range(1,n): A[i][i-1]=-a[i]%P
    for i in range(n-1): C[i][i+1]=-c[i]%P
    B=diag(b); E=diag(e); Ei=diag([pow(v,-1,P) for v in e]); D=diag(d)
    H=add(mul(inv(A),B),mul(inv(C),E),D)
    K=mul(mul(mul(A,H),Ei),C)
    expected=add(mul(mul(B,Ei),C),A,mul(mul(mul(A,D),Ei),C))
    assert K==expected
    assert all(K[i][j]==0 for i in range(n) for j in range(n) if abs(i-j)>1)
    try: Hi=inv(H)
    except ValueError: return False,None
    assert Hi==mul(mul(mul(Ei,C),inv(K)),A)
    q=rank([[Hi[i][j] for j in range(1,n,2)] for i in range(0,n,2)])
    return True,q

rng=random.Random(20261009); checks=0; invertible=0
for n in range(2,18):
    for trial in range(15):
        # Resets included. Backward diagonal E nonzero is the reduction's explicit hypothesis.
        a=[rng.randrange(0,5) for _ in range(n)]; c=[rng.randrange(0,5) for _ in range(n)]
        b=[rng.randrange(0,5) for _ in range(n)]; e=[rng.randrange(1,5) for _ in range(n)]; d=[rng.randrange(0,5) for _ in range(n)]
        ok,_=check(a,b,c,e,d); checks+=1; invertible+=ok
examples=[]
for n in (4,8,16,32,64):
    ok,q=check([0]+[j+2 for j in range(1,n)],[1]*n,[j+3 for j in range(n-1)]+[0],[1]*n,[0]*n)
    assert ok and q==n//2
    examples.append({'N':n,'even_row_odd_column_inverse_rank':q,'lower_bound_rank_inverse_minus_any_diagonal':q})
print(json.dumps({'field_prime':P,'random_reduction_checks':checks,'invertible_inverse_checks':invertible,'upload_weight_examples':examples,'scope':'Finite exact certificates only; no all-N Fourier factorization or speedup.'},indent=2))
