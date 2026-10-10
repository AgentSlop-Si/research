"""Fresh authored N=11 fourteen-bank modular and exact algebraic controls.
No supplied research code is imported or executed.
"""
import json
from pathlib import Path

P=23;N=11;M=6;Q=2

def inv(x): return pow(x%P,-1,P)
def solve(A,b):
    A=[[v%P for v in row]+[b[i]%P] for i,row in enumerate(A)];n=len(A)
    for j in range(n):
        k=next(k for k in range(j,n) if A[k][j]);A[j],A[k]=A[k],A[j]
        u=inv(A[j][j]);A[j]=[v*u%P for v in A[j]]
        for i in range(n):
            if i!=j:
                u=A[i][j];A[i]=[(x-u*y)%P for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]
def det(A):
    A=[list(row) for row in A];v=1;n=len(A)
    for j in range(n):
        k=next((k for k in range(j,n) if A[k][j]%P),None)
        if k is None:return 0
        if k!=j:A[k],A[j]=A[j],A[k];v=-v
        u=A[j][j]%P;v=v*u%P
        for i in range(j+1,n):
            z=A[i][j]*inv(u)%P;A[i]=[(x-z*y)%P for x,y in zip(A[i],A[j])]
    return v%P

def pivots(A):
    A=[list(row) for row in A];m=len(A);n=len(A[0]);r=0;cols=[]
    for j in range(n):
        k=next((k for k in range(r,m) if A[k][j]%P),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];v=inv(A[r][j]);A[r]=[v*x%P for x in A[r]]
        for i in range(r+1,m):
            v=A[i][j];A[i]=[(x-v*y)%P for x,y in zip(A[i],A[r])]
        cols.append(j);r+=1
        if r==m:break
    return cols

def rem(a,b):
    a=a[:]
    while a and not a[-1]:a.pop()
    while len(a)>=len(b):
        z=a[-1]*inv(b[-1])%P;d=len(a)-len(b)
        for k,v in enumerate(b):a[k+d]=(a[k+d]-z*v)%P
        while a and not a[-1]:a.pop()
    return a

def gcd(a,b):
    while b:a,b=b,rem(a,b)
    return [v*inv(a[-1])%P for v in a]

def G(e,d,a,b):
    r=e*a%N;l=d*b%N
    if r+l>=N:return 0
    z=pow(Q,e*d%N,P);v=1
    for j in range(1,l+1):v=v*(1-pow(z,r+j,P))*inv(1-pow(z,j,P))%P
    return v

f=lambda a,b:pow(Q,3*((a+b)**2)%N,P)
H=Q*inv(1+Q)%P
s=[1]+[(f(a,1)*inv(H*G(1,1,a,1))-G(-1,1,a,1)*inv(G(1,1,a,1)))%P for a in range(2,10)]
T=inv(G(-1,1,9,2))
u=[(f(a,2)-T*G(-1,1,a,2))*inv(G(1,1,a,2))%P for a in range(2,9)]
A=[[s[r+k] for k in range(4)] for r in range(3)]+[u[:4]]
rhs=[-s[r+6]%P for r in range(3)]+[-u[6]%P]
c=solve(A,rhs)+[0,0,1]
red=[[int(j==r) for j in range(M)] for r in range(M)]
for r in range(M,N):red.append([-sum(c[k]*red[r-M+k][j] for k in range(M))%P for j in range(M)])
matrices={};ranks=[];minors={};aug=[]
for b in range(N):
    B=[]
    for a in range(N):B.append([G(1,1,a,b)*v%P for v in red[a]]+[G(-1,1,a,b),G(1,-1,a,b)]+[G(-1,-1,a,b)*v%P for v in red[-a%N]])
    matrices[b]=B;cols=pivots(B);ranks.append(len(cols));aug.append(len(pivots([row+[f(a,b)] for a,row in enumerate(B)])))
    if len(cols)==N:minors[b]={'columns':cols,'determinant':det([[row[k] for k in cols] for row in B])}

def edge_one():
    k0=-H*(s[5]+sum(c[k]*s[k-1] for k in range(1,6)))*inv(c[0])%P
    return [k0]+[H*s[d-1]%P for d in range(1,6)]+[H,(f(0,1)-k0-H)%P]+[0]*6

def edge_two():
    # Choose K2..K7=u0..u5 and solve recurrence backwards for K1,K0.
    k1=-(u[5]+sum(c[k]*u[k-1] for k in range(1,6)))*inv(c[0])%P
    k0=-(u[4]+c[1]*k1+sum(c[k]*u[k-2] for k in range(2,6)))*inv(c[0])%P
    K=[k0,k1]+u[:4]
    hp=(f(1,2)-G(1,1,1,2)*k1)*inv(G(1,-1,1,2))%P
    # -- sector supports only r=0,1. Set higher moments zero.
    km1=(f(10,2)-T*G(-1,1,10,2))*inv(G(-1,-1,10,2))%P
    km0=(f(0,2)-k0-T-hp)%P
    return K+[T,hp]+[km0,km1,0,0,0,0]

z1=edge_one();z2=edge_two()
checks={str(b):[sum(x*y for x,y in zip(row,z))%P==f(a,b) for a,row in enumerate(matrices[b])] for b,z in [(1,z1),(2,z2)]}
result={'N':N,'banks':14,'prime':P,'q':Q,'H':H,'T':T,'edge_one_moments':s,'edge_two_moments':u,'coefficient_system':A,'coefficient_rhs':rhs,'coefficient_system_determinant':det(A),'g_ascending':c,'gcd_with_derivative':gcd(c,[k*c[k]%P for k in range(1,7)]),'row_ranks':ranks,'augmented_ranks':aug,'full_row_minors':minors,'z1':z1,'z2':z2,'edge_checks':checks,'reduced_powers':red,'matrices':matrices}
# Sylvester determinant is an independent squarefreeness certificate.
dc=[k*c[k]%P for k in range(1,7)]
S=[]
for i in range(5):S.append([0]*i+list(reversed(c))+[0]*(4-i))
for i in range(6):S.append([0]*i+list(reversed(dc))+[0]*(5-i))
result['sylvester_matrix']=S
result['resultant_g_derivative']=det(S)
assert result['resultant_g_derivative']
assert det(A) and c[0] and result['gcd_with_derivative']==[1]
assert all(all(v) for v in checks.values())
assert all(ranks[b]==N for b in [0,3,4,5,6,7,8])
Path(__file__).with_name('N11_MODULAR_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['matrices','reduced_powers']},indent=2))
