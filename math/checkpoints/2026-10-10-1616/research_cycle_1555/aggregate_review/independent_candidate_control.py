"""Independent exact verification of the reported p5 aggregate witness.
Only the reviewer's newly written field helper is imported.
"""
from reviewer_cyclotomic import ZERO, ONE, add, sub, neg, mul, inv, scale, POWERS
from fractions import Fraction
from pathlib import Path
import json

n=5
Z=POWERS
order=[0,1,2,4,3]

def summands(xs):
    s=ZERO
    for x in xs:s=add(s,x)
    return s

def matmul(A,B):
    return [[summands(mul(a,b) for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def nnz(A):return sum(x!=ZERO for row in A for x in row)
def enc(x):return [str(v) for v in x]
def matenc(A):return [[enc(x) for x in row] for row in A]
def identity():return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def matrix_inverse(A):
    M=[list(row)+unit for row,unit in zip(A,identity())]
    for col in range(n):
        k=next(k for k in range(col,n) if M[k][col]!=ZERO)
        M[k],M[col]=M[col],M[k]
        u=inv(M[col][col]);M[col]=[mul(x,u) for x in M[col]]
        for k in range(n):
            if k==col:continue
            a=M[k][col]
            M[k]=[sub(x,mul(a,y)) for x,y in zip(M[k],M[col])]
    assert [row[:n] for row in M]==identity()
    return [row[n:] for row in M]

F=[[Z[i*j%n] for j in range(n)] for i in range(n)]
c=add(Z[1],Z[4])
d=summands((scale(Z[1],2),neg(Z[2]),Z[3],scale(Z[4],-2)))
b=[ONE,neg(ONE),c,neg(c),d]
assert all(x!=ZERO for x in b)
assert mul(c,add(Z[2],Z[3]))==neg(ONE)
C=identity()
links=[]
for j in range(1,n):
    a=neg(mul(b[j-1],inv(b[j])))
    C[order[j]][order[j-1]]=a;links.append(a)
R=matmul(matrix_inverse(C),F)
prefix_rows=[]
for j in range(n):
    row=[mul(summands(mul(b[k],Z[order[k]*t%n]) for k in range(j+1)),inv(b[j])) for t in range(n)]
    assert row==R[order[j]]
    prefix_rows.append(row)
q3_at2=summands(mul(b[k],Z[order[k]*2%n]) for k in range(4))
assert d==neg(mul(Z[4],q3_at2))
assert nnz(C)==9 and nnz(R)==20
assert matmul(C,R)==F
B=[]
fiber_entries=0
for t in range(n):
    q=(-3*t*t)%n
    Bt=[[mul(Z[q],R[v][t]) if u==t else ZERO for u in range(n)] for v in range(n)]
    H=matmul(matmul(C,Bt),F)
    expected=[[Z[(q+(i+j)*t)%n] for j in range(n)] for i in range(n)]
    assert H==expected
    B.append(Bt);fiber_entries+=n*n
Bsum=[[summands(B[t][i][j] for t in range(n)) for j in range(n)] for i in range(n)]
raw=matmul(matmul(C,Bsum),F)
G=summands(Z[-3*t*t%n] for t in range(n))
assert G!=ZERO
corrected=[[mul(mul(mul(inv(G),Z[-3*i*i%n]),raw[i][j]),Z[-3*j*j%n]) for j in range(n)] for i in range(n)]
assert corrected==F
# Check Fourier inversion and full cyclic Weyl relation independently.
Finv=matrix_inverse(corrected)
assert Finv==[[scale(Z[-i*j%n],Fraction(1,5)) for j in range(n)] for i in range(n)]
assert [corrected[i][0] for i in range(n)]==[ONE]*n
assert all(corrected[i][(j+1)%n]==mul(Z[i],corrected[i][j]) for i in range(n) for j in range(n))
# Sum Galois conjugates of the support-zero conditions is not used as a substitute for a complex proof.
zeros=[[i,t] for i,row in enumerate(R) for t,x in enumerate(row) if x==ZERO]
result={
 'status':'passed_exact',
 'coefficient_domain':'Q[zeta5] with zeta5 primitive; literal vectors are in basis 1,zeta,zeta²,zeta³',
 'source_programs_executed_or_imported':False,
 'reviewer_helper_only':True,
 'order':order,'prefix_coefficients':[enc(x) for x in b],
 'chain_links':[enc(x) for x in links],
 'C':matenc(C),'R_CinverseF':matenc(R),'A':matenc(F),
 'B_t':[matenc(x) for x in B],
 'R_zero_positions':zeros,'R_column_nnz':[sum(R[i][t]!=ZERO for i in range(n)) for t in range(n)],
 'support_count':{'A':nnz(F),'C':nnz(C),'colored_middle':sum(nnz(x) for x in B),'total':nnz(F)+nnz(C)+sum(nnz(x) for x in B),'dense_baseline':55},
 'all_slice_entries_checked':fiber_entries,'all_corrected_transfer_entries_checked':25,
 'gauss_scalar':enc(G),'Fourier_inverse_verified':True,'Weyl_verified':True,
 'claims_not_established':['any asymptotic speedup','practical speedup','lower bound 54 optimal','arbitrary wider or noninvertible aggregate model'],
}
out=Path(__file__).parent/'INDEPENDENT_CANDIDATE_RESULTS.json';out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['A','C','R_CinverseF','B_t']},indent=2))
