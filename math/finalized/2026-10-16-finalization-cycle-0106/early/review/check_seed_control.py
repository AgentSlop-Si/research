"""Independent exact small control; no submitted program is imported or run."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib, json

def z(a=0,b=0): return (Q(a),Q(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def mm(A,B):
    return [[sumz(mul(a,b) for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sumz(xs):
    out=z()
    for x in xs: out=add(out,x)
    return out
def adj(A): return [[conj(x) for x in col] for col in zip(*A)]
def diag(a,b): return [[a,z()],[z(),b]]

A=[[z(Q(3,5)),z(Q(4,5))],[z(Q(-4,5)),z(Q(3,5))]]
I=diag(z(1),z(1))
assert mm(A,adj(A))==I
L=diag(z(Q(3,5),Q(-4,5)),z(Q(-4,5),Q(-3,5)))
R=diag(z(1),z(0,1))
B=mm(mm(L,A),R)
assert B==[[z(Q(9,25),Q(-12,25)),z(Q(16,25),Q(12,25))],
           [z(Q(16,25),Q(12,25)),z(Q(9,25),Q(-12,25))]]
assert mm(B,adj(B))==I
assert all(sumz(row)==z(1) for row in B)
assert all(sumz(col)==z(1) for col in zip(*B))
leverage=[mul(A[0][i],adj(A)[i][0]) for i in range(2)]
assert leverage==[z(Q(9,25)),z(Q(16,25))]
assert all(x!=z(Q(1,2)) for x in leverage)
delta=Q(7,24)
assert 1-delta**2/(1-delta)==Q(359,408)
A2=[[z(Q(24,25)),z(Q(-7,25))],[z(Q(7,25)),z(Q(24,25))]]
assert mm(A2,adj(A2))==I
E=[[add(A2[i][j],z(-int(i==j))) for j in range(2)] for i in range(2)]
assert mm(adj(E),E)==diag(z(Q(2,25)),z(Q(2,25)))
assert Q(2,25)<Q(1,4)
assert [mul(A2[0][i],adj(A2)[i][0]) for i in range(2)]==[z(Q(576,625)),z(Q(49,625))]
# U=A2* F2/sqrt(2) equals M/(25 sqrt(2)); combine the two radical factors exactly.
M=[[z(31),z(17)],[z(17),z(-31)]]
assert mm(M,adj(M))==diag(z(1250),z(1250))
LT=diag(z(31,-17),z(17,31))
numer=mm(mm(LT,M),R)
V=[[mul(x,z(Q(1,1250))) for x in row] for row in numer]
assert V==[[z(Q(961,1250),Q(-527,1250)),z(Q(289,1250),Q(527,1250))],
           [z(Q(289,1250),Q(527,1250)),z(Q(961,1250),Q(-527,1250))]]
assert mm(V,adj(V))==I
assert all(sumz(row)==z(1) for row in V)
assert all(sumz(col)==z(1) for col in zip(*V))
assert Q(48**2,1250)==Q(1152,625)!=1
assert Q(14**2,1250)==Q(98,625)!=1
assert mm(V,[[z(1)],[z(0,-1)]])!=[[z(1)],[z(1)]]
out={"verdict":"PASS", "scope":"Exact two-by-two endpoint-freedom counterexample and one rational weak-coupling constant only.",
     "A_unitary":True,"first_row_nonzero":True,"seed_leverages":["9/25","16/25"],
     "required_seed_leverages":["1/2","1/2"],"L_A_R_unitary_and_biregular_sum_one":True,
     "weak_coupling_constant":"359/408", "supplied_program_executed":False,
     "author_weak_coupling_separator_independently_verified":True,
     "author_separator_distance_squared":"2/25",
     "author_separator_leverages":["576/625","49/625"],
     "normalized_U_ones_squared_moduli":["1152/625","98/625"],
     "limits":"Not a replay of the accepted N8/N16 polynomial certificates, not a numerical executor, no asymptotic or novelty certification."}
Path(__file__).with_name("INDEPENDENT_SMALL_CONTROL.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
