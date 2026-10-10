"""Independent finite-field sanity checks for the October 10 FFT theoretical audit.

This is a finite-size verifier. The accompanying markdown contains the all-N proofs.
"""
import random
P = 97
N = 16
M = 4

def root_of_exact_order(n):
    for w in range(2, P):
        if pow(w, n, P) == 1 and all(pow(w, n // q, P) != 1 for q in range(2, n + 1) if n % q == 0 and all(q % k for k in range(2, int(q ** 0.5) + 1))):
            return w
    raise ValueError('root missing')

def matmul(A, B):
    n = len(A); m = len(B[0]); k = len(B)
    return [[sum(A[i][l] * B[l][j] for l in range(k)) % P for j in range(m)] for i in range(n)]

def add(A, B):
    return [[(x+y)%P for x,y in zip(a,b)] for a,b in zip(A,B)]

def scale(A,c):
    return [[x*c%P for x in a] for a in A]

def rank(A):
    A = [list(map(lambda x:x%P, row)) for row in A]
    nr=len(A); nc=len(A[0]); row=0
    for col in range(nc):
        piv = next((i for i in range(row,nr) if A[i][col]), None)
        if piv is None: continue
        A[row],A[piv] = A[piv],A[row]
        inv=pow(A[row][col], -1, P)
        A[row] = [(v*inv)%P for v in A[row]]
        for i in range(nr):
            if i!=row and A[i][col]:
                a=A[i][col]
                A[i]=[(x-a*y)%P for x,y in zip(A[i], A[row])]
        row+=1
        if row==nr: break
    return row

def identity(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def inverse(A):
    n=len(A)
    W=[a[:]+i[:] for a,i in zip(A,identity(n))]
    for c in range(n):
        pivot=next(i for i in range(c,n) if W[i][c]%P)
        W[c],W[pivot]=W[pivot],W[c]
        x=pow(W[c][c],-1,P)
        W[c]=[(v*x)%P for v in W[c]]
        for i in range(n):
            if i==c: continue
            a=W[i][c]
            W[i]=[(v-a*u)%P for v,u in zip(W[i],W[c])]
    return [a[n:] for a in W]

def multichain_permutation(rng):
    order = list(range(N))
    rng.shuffle(order)
    pi={order[i]:order[(i+1)%N] for i in range(N)}
    return pi

def denominator(pi, weight=2):
    A=identity(N)
    for i in range(N):
        A[i][pi[i]]=(A[i][pi[i]]-weight)%P
    return A

w=root_of_exact_order(N)
F=[[pow(w,i*j,P) for j in range(N)] for i in range(N)]
S=[[int(i==(j+1)%N) for j in range(N)] for i in range(N)]
D=[[pow(w,i,P)*int(i==j) for j in range(N)] for i in range(N)]
assert matmul(F,S)==matmul(D,F)
assert [F[i][0] for i in range(N)]==[1]*N
rng=random.Random(777)
As=[denominator(multichain_permutation(rng)) for _ in range(3)]
prod=identity(N)
for t,A in enumerate(As,1):
    prod=matmul(prod,A)
    supports=[sum(v!=0 for v in row) for row in prod]
    assert max(supports)<=2**t
    print('green_product_inv_row_support after stage', t, 'max',max(supports),'bound',2**t)
assert all(v!=0 for row in inverse(F) for v in row)
Gs=[inverse(A) for A in As]
Msum=add(Gs[0],Gs[1])
weyl_error=matmul(Msum,S)
weyl_right=matmul(D,Msum)
num_defects=sum(weyl_error[i][j]!=weyl_right[i][j] for i in range(N) for j in range(N))
assert num_defects>0
print('random_two_Green_sum_Weyl_discrepant_entries',num_defects,'of',N*N)
assert len({Msum[i][i] for i in range(N)}) == 1
assert len({F[i][i] for i in range(N)}) > 1
print('ungauged_two_Green_sum_diagonal_distinct_values', len({Msum[i][i] for i in range(N)}))
print('Fourier_diagonal_distinct_values', len({F[i][i] for i in range(N)}))

v=root_of_exact_order(M)
projs=[]
for t in range(M):
    A=[[0]*N for _ in range(N)]
    for b in range(N//M):
        for u in range(M):
            for z in range(M):
                A[b*M+u][b*M+z]=pow(v, t*(u-z)%M,P)
    assert rank(A)==N//M
    projs.append(A)
psum=[[0]*N for _ in range(N)]
for Q in projs: psum=add(psum,Q)
assert psum==scale(identity(N),M)
partial=[[0]*N for _ in range(N)]
for count in range(1,M+1):
    partial=add(partial, matmul(F,projs[count-1]))
    print('phase_banks', count,'combined_rank',rank(partial),'upper_bound',count*N//M)
assert scale(partial,pow(M,-1,P))==F

# A globally dense, linearly applicable separated-generator scan is not itself the DFT.
T=[[3 if i==j else (1 if i>j else 2) for j in range(N)] for i in range(N)]
I=list(range(N//2)); J=list(range(N//2,N))
print('single_dense_scan_balanced_cut_rank',rank([[T[i][j] for j in J] for i in I]))
print('Fourier_same_cut_rank',rank([[F[i][j] for j in J] for i in I]))
print('Finite-size checks passed; these tests do NOT establish global nonexistence of all fused FFT architectures.')
