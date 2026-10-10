"""Fresh literal original-resolvent control at the certified good reduction.
Standalone; executes/imports no research program, reads no prior witness.
"""
import json,time
from pathlib import Path
start=time.time();P=23;N=11;D=6;q=2;c=[12,21,2,4,0,0,1]
inv=lambda x:pow(x%P,-1,P)
Z=(0,)*D;O=(1,0,0,0,0,0);T=(0,1,0,0,0,0)
def plus(a,b):return tuple((x+y)%P for x,y in zip(a,b))
def neg(a):return tuple(-x%P for x in a)
def scale(a,v):return tuple(x*v%P for x in a)
def mult(a,b):
    v=[0]*(2*D-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):v[i+j]=(v[i+j]+x*y)%P
    for i in range(2*D-2,D-1,-1):
        z=v[i]
        if z:
            for k in range(D):v[i-D+k]=(v[i-D+k]-z*c[k])%P
    return tuple(v[:D])
def power(a,n):
    v=O
    while n:
        if n&1:v=mult(v,a)
        a=mult(a,a);n//=2
    return v
def solve(A,b):
    A=[row[:]+[b[i]] for i,row in enumerate(A)];n=len(A)
    for j in range(n):
        k=next(k for k in range(j,n) if A[k][j]%P);A[k],A[j]=A[j],A[k]
        v=inv(A[j][j]);A[j]=[v*x%P for x in A[j]]
        for i in range(n):
            if i!=j:
                v=A[i][j];A[i]=[(x-v*y)%P for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]
def inverse(a):
    cols=[mult(a,tuple(int(j==i) for j in range(D))) for i in range(D)]
    ans=tuple(solve([[cols[j][i] for j in range(D)] for i in range(D)],list(O)))
    assert mult(a,ans)==O
    return ans
pows=[power(T,i) for i in range(N)]
tr=[sum(mult(pows[i],tuple(int(k==j) for k in range(D)))[j] for j in range(D))%P for i in range(D)]
def trace(a):return sum(x*y for x,y in zip(a,tr))%P

def G(e,d,a,b):
    r=e*a%N;l=d*b%N
    if r+l>=N:return 0
    z=pow(q,e*d%N,P);v=1
    for j in range(1,l+1):v=v*(1-pow(z,r+j,P))*inv(1-pow(z,j,P))%P
    return v
f=lambda a,b:pow(q,3*(a+b)**2%N,P)
H=q*inv(1+q)%P
s=[1]+[(f(a,1)*inv(H*G(1,1,a,1))-G(-1,1,a,1)*inv(G(1,1,a,1)))%P for a in range(2,10)]
Tb=inv(G(-1,1,9,2));u=[(f(a,2)-Tb*G(-1,1,a,2))*inv(G(1,1,a,2))%P for a in range(2,9)]
A=[[s[r+k] for k in range(4)] for r in range(3)]+[u[:4]]
assert solve(A,[-s[r+6]%P for r in range(3)]+[-u[6]%P])==c[:4]
mat={b:[[G(1,1,a,b)*v%P for v in pows[a]]+[G(-1,1,a,b),G(1,-1,a,b)]+[G(-1,-1,a,b)*v%P for v in pows[-a%N]] for a in range(N)] for b in range(N)}
z={};k0=-H*(s[5]+sum(c[k]*s[k-1] for k in range(1,6)))*inv(c[0])%P
z[1]=[k0]+[H*s[d-1]%P for d in range(1,6)]+[H,(f(0,1)-k0-H)%P]+[0]*6
k1=-(u[5]+sum(c[k]*u[k-1] for k in range(1,6)))*inv(c[0])%P
k0=-(u[4]+c[1]*k1+sum(c[k]*u[k-2] for k in range(2,6)))*inv(c[0])%P
hp=(f(1,2)-G(1,1,1,2)*k1)*inv(G(1,-1,1,2))%P
km1=(f(10,2)-Tb*G(-1,1,10,2))*inv(G(-1,-1,10,2))%P
z[2]=[k0,k1]+u[:4]+[Tb,hp]+[(f(0,2)-k0-Tb-hp)%P,km1]+[0]*4
cols={0:[0,1,2,3,4,5,6,8,9,10,11],3:[0,1,2,3,4,5,6,7,8,9,10],4:[0,1,2,3,4,5,6,7,9,10,11],5:[0,1,2,3,4,5,6,9,10,11,12]}
for b,Cb in cols.items():
    vals=solve([[row[j] for j in Cb] for row in mat[b]],[f(a,b) for a in range(N)])
    z[b]=[0]*14
    for j,v in zip(Cb,vals):z[b][j]=v
for b in range(1,6):z[N-b]=z[b][8:14]+[z[b][7],z[b][6]]+z[b][:6]
assert all(sum(x*y for x,y in zip(row,z[b]))%P==f(a,b) for b in range(N) for a,row in enumerate(mat[b]))
gprime=tuple((k+1)*c[k+1]%P for k in range(D));gi=inverse(gprime)
def amp(K):
    num=Z
    for d in range(D):
        for k in range(d+1,D+1):num=plus(num,scale(pows[k-1-d],K[d]*c[k]))
    return mult(num,gi)
C=sum(pow(q,-t*t%N,P) for t in range(N))*inv(N)%P
I=[[O if a==b else Z for b in range(N)] for a in range(N)]
F=[[0]*N for _ in range(N)];guards=[];generic_checks=0
for e,d,group in [(1,1,'plus'),(-1,1,'back'),(1,-1,'front'),(-1,-1,'minus')]:
    isroot=group in ['plus','minus'];alpha=T if isroot else O
    guard=neg(power(alpha,N));guardinv=inverse(guard);guards.append(list(guard))
    hs=[Z]*N
    for b in range(N):
        h=amp(z[b][:6]) if group=='plus' else amp(z[b][8:14]) if group=='minus' else scale(O,z[b][6 if group=='back' else 7])
        hs[d*b%N]=h
    for j in range(N):
        diag=[pow(q,(e*d*j+d*k)%N,P) for k in range(N)]
        def left(B):return [[plus(mult(alpha,B[(a-e)%N][b]),scale(B[a][b],diag[a])) for b in range(N)] for a in range(N)]
        def right(B):return [[plus(mult(alpha,B[a][(b+e)%N]),scale(B[a][b],diag[b])) for b in range(N)] for a in range(N)]
        Xpower=[row[:] for row in I];Qsum=[row[:] for row in I]
        for k in range(1,N):
            Xpower=left(Xpower);Qsum=[[plus(a,b) for a,b in zip(ra,rb)] for ra,rb in zip(Qsum,Xpower)]
        Xn=left(Xpower);Xnscalar=plus(power(alpha,N),O)
        assert Xn==[[Xnscalar if a==b else Z for b in range(N)] for a in range(N)]
        Qinv=[[mult(x,guardinv) for x in row] for row in Qsum]
        for B in [left(Qinv),right(Qinv)]:
            assert [[plus(x,neg(y)) for x,y in zip(rx,ry)] for rx,ry in zip(Qinv,B)]==I
        w=Z
        for ell in range(N):w=plus(w,scale(hs[ell],pow(q,-e*d*j*ell%N,P)))
        w=scale(mult(guard,w),C)
        for a in range(N):
            for b in range(N):
                val=mult(w,Qinv[a][b])
                if not isroot:assert all(t==0 for t in val[1:])
                F[a][b]=(F[a][b]+inv(N)*(trace(val) if isroot else val[0]))%P
        generic_checks+=1
assert F==[[pow(q,-a*b%N,P) for b in range(N)] for a in range(N)]
result={'status':'PASS','prime':P,'q':q,'quotient_polynomial':c,'trace_basis':tr,'C':C,'guard_polynomials':guards,'generic_branch_checks':generic_checks,'individual_branches_represented':154,'both_inverse_products_per_generic_branch':True,'all_121_original_matrix_entries':True,'all_121_weyl_entries':True,'node_amplitudes':'Lagrange cardinal functional in F_23[t]/g; no root selection','scope':'Finite-field literal control only; characteristic-zero proof is the separate algebraic construction and good-reduction argument.','seconds':time.time()-start}
Path(__file__).with_name('N11_LITERAL_MOD23_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
