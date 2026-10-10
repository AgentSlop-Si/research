"""Auditor-written checks. Does not read/import/execute supplied research code."""
from fractions import Fraction as Q
import json, math, cmath
from pathlib import Path

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def add(A,B): return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(a,A): return [[a*x for x in row] for row in A]
def mm(A,B): return [[sum(a[k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for a in A]
def inv(A):
    n=len(A); W=[list(a)+b for a,b in zip(A,eye(n))]
    for j in range(n):
        p=next(i for i in range(j,n) if W[i][j]!=0)
        W[j],W[p]=W[p],W[j]; z=W[j][j]; W[j]=[a/z for a in W[j]]
        for i in range(n):
            if i!=j:
                z=W[i][j]; W[i]=[a-z*b for a,b in zip(W[i],W[j])]
    return [row[n:] for row in W]
def norm1(A):return max(sum(abs(row[j]) for row in A) for j in range(len(A)))
def norminf(A):return max(sum(abs(x) for x in row) for row in A)
def err(A,B):return max(abs(a-b) for ar,br in zip(A,B) for a,b in zip(ar,br))
def path(n):return [[Q(3 if i==j else -1 if abs(i-j)==1 else 0) for j in range(n)] for i in range(n)]
out={'scope':'Independent algebra, exact rational matrices, and floating reference checks; supplied code never run','cycle':[],'path_exact':[],'path_complex':[]}
for n in (1,2,3,4,8,12,16):
    I=eye(n); C=[[Q(0) for _ in range(n)] for _ in range(n)]
    for j in range(n):C[j][(j+1)%n]=Q(1 if j<n-1 else -1)
    K=add(I,inv(add(I,scale(-1,C)))); Ki=inv(K)
    assert norm1(K)==Q(n+2,2)
    assert norm1(Ki)==Q(2**n,2**n+1)
    assert all(x!=0 for A in (K,Ki) for row in A for x in row)
    assert mm(K,Ki)==I
    out['cycle'].append({'N':n,'norm1':str(norm1(K)),'inverse_norm1':str(norm1(Ki)),'kappa1':str(norm1(K)*norm1(Ki))})
for n in (1,2,3,4,8,16):
    T=path(n);I=eye(n);S=add(inv(T),inv(add(T,I)));Si=inv(S)
    rhs=add(add(scale(Q(1,2),T),scale(Q(1,4),I)),scale(Q(-1,8),inv(add(T,scale(Q(1,2),I)))))
    assert rhs==Si
    assert norm1(Si)<=Q(58,21) and norm1(S)*norm1(Si)<=Q(29,7)
    out['path_exact'].append({'N':n,'S_norm1':str(norm1(S)),'inverse_norm1':str(norm1(Si)),'kappa1':str(norm1(S)*norm1(Si))})
for n in (4,8,16,32):
    q=cmath.exp(2j*math.pi/n); roots=[q**i for i in range(n)]; F=[[roots[(k*j)%n] for j in range(n)] for k in range(n)]; Fi=[[roots[-k*j%n]/n for j in range(n)] for k in range(n)]
    T=[[complex(x) for x in row] for row in path(n)];H=mm(mm(F,T),Fi)
    H_formula=[[(3-roots[k]-roots[-k%n])*int(k==l)+(roots[l]+roots[-k%n])/n for l in range(n)] for k in range(n)]
    formula_error=err(H,H_formula); assert formula_error<1e-11
    I=eye(n); S=add(inv(T),inv(add(T,I)));K=mm(mm(F,S),Fi);Ki=inv(K)
    inverse_formula=add(add(scale(.5,H),scale(.25,I)),scale(-.125,inv(add(H,scale(.5,I)))))
    inverse_error=err(Ki,inverse_formula);assert inverse_error<1e-10
    assert norminf(Ki)<73/18
    woodbury_errors=[]
    for alpha in (0,.5,1):
        g=[1/(3+alpha-roots[k]-roots[-k%n]) for k in range(n)]
        A=[[1,roots[-k%n]] for k in range(n)];B=[[roots[l]/n for l in range(n)],[1/n]*n]
        Di=[[g[k]*int(k==l) for l in range(n)] for k in range(n)]
        W=add(Di,scale(-1,mm(mm(mm(mm(Di,A),inv(add(eye(2),mm(mm(B,Di),A)))),B),Di)))
        actual=inv(add(H,scale(alpha,I)));we=err(W,actual);assert we<1e-10
        assert norminf(actual)<=1/(1+alpha)+4/(1+alpha)**2+1e-12
        woodbury_errors.append(we)
    out['path_complex'].append({'N':n,'conjugacy_max_error':formula_error,'inverse_identity_max_error':inverse_error,'inverse_inf_norm':norminf(Ki),'woodbury_max_errors':woodbury_errors})
# Exact finite-field conjugacy, independent scalar and dense matrix routines.
p=998244353

def mp(A,B):return [[sum(a[k]*B[k][j] for k in range(len(B)))%p for j in range(len(B[0]))] for a in A]
def ip(A):
    n=len(A);W=[list(a)+b for a,b in zip(A,eye(n))]
    for j in range(n):
        pos=next(i for i in range(j,n) if W[i][j]%p)
        W[j],W[pos]=W[pos],W[j]; r=pow(W[j][j],-1,p);W[j]=[x*r%p for x in W[j]]
        for i in range(n):
            if i!=j:
                r=W[i][j];W[i]=[(a-r*b)%p for a,b in zip(W[i],W[j])]
    return [r[n:] for r in W]
def ap(A,B):return [[(a+b)%p for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def sp(c,A):return [[c*x%p for x in row] for row in A]
out['modular_conjugacy']=[]
for n in (2,4,8,16):
    q=pow(3,(p-1)//n,p);F=[[pow(q,k*j,p) for j in range(n)] for k in range(n)];I=eye(n)
    for a,b,c in ((1,1,1),(5,1,1),(9,3,5)):
        M=[[0]*n for _ in range(n)];Mh=[[0]*n for _ in range(n)];ai=pow(a,-1,n)
        for j in range(n):M[j][(a*j+c)%n]=pow(q,b*j,p)
        for k in range(n):
            dest=ai*(k+b)%n;Mh[k][dest]=pow(q,(-c*dest)%n,p)
        assert mp(F,M)==mp(Mh,F)
        K=ap(I,ip(ap(I,sp(-1,M))));Kh=ap(I,ip(ap(I,sp(-1,Mh))))
        assert mp(F,K)==mp(Kh,F)
        assert mp(F,ip(K))==mp(ip(Kh),F)
    out['modular_conjugacy'].append({'N':n,'descriptor_cases':3,'source_target_and_inverse':'exact PASS'})
out['derived_field_counts']={'cycle_prepare':'2N+log2(N)+4','cycle_apply':'5N+1','cycle_inverse_apply':'6N+1','signed_cycle_cold':'3N+1','bridge_prepare':'43N+31','bridge_source_S':'9N-6','bridge_target_S':'19N+12','bridge_source_inverse':'12N-5','bridge_target_inverse':'21N+8'}
out['status']='PASS'
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
