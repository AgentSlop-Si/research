"""Fresh exact control for the N=11 fourteen-bank recipe.
Reads no supplied code and no witness data. Uses only installed SymPy arithmetic.
"""
import json,time
from pathlib import Path
import sympy as sp
start=time.time();x=sp.symbols('x');K=sp.QQ.alg_field_from_poly(sp.Poly(sum(x**i for i in range(11)),x),alias='q')
q=K.unit;zero=K.zero;one=K.one
N=11;M=6

def conv(a):return K(a)
def add(xs):return sum(xs,zero)
def encoded(a):
    v=list(reversed(a.to_list()));v += [sp.QQ.zero]*(10-len(v))
    return [str(z) for z in v]
def solve(A,b):
    A=[row[:]+[b[i]] for i,row in enumerate(A)];n=len(A)
    for j in range(n):
        k=next(k for k in range(j,n) if A[k][j]);A[j],A[k]=A[k],A[j]
        v=A[j][j];A[j]=[z/v for z in A[j]]
        for i in range(n):
            if i!=j:
                v=A[i][j]
                if v:A[i]=[a-v*b for a,b in zip(A[i],A[j])]
    return [row[-1] for row in A]

def determinant(A):
    A=[row[:] for row in A];n=len(A);v=one
    for j in range(n):
        k=next((k for k in range(j,n) if A[k][j]),None)
        if k is None:return zero
        if k!=j:A[k],A[j]=A[j],A[k];v=-v
        a=A[j][j];v*=a
        for i in range(j+1,n):
            z=A[i][j]/a
            if z:A[i]=[u-z*w for u,w in zip(A[i],A[j])]
    return v

cache={}
def G(e,d,a,b):
    r=e*a%N;l=d*b%N
    if r+l>=N:return zero
    key=(e*d,r,l)
    if key not in cache:
        z=q**(e*d%N);v=one
        for j in range(1,l+1):v*=((one-z**(r+j))/(one-z**j))
        cache[key]=v
    return cache[key]
f=lambda a,b:q**(3*((a+b)**2)%N)
H=q/(one+q)
s=[one]+[f(a,1)/(H*G(1,1,a,1))-G(-1,1,a,1)/G(1,1,a,1) for a in range(2,10)]
T=one/G(-1,1,9,2)
u=[(f(a,2)-T*G(-1,1,a,2))/G(1,1,a,2) for a in range(2,9)]
A=[[s[r+k] for k in range(4)] for r in range(3)]+[u[:4]]
rhs=[-s[r+6] for r in range(3)]+[-u[6]]
c=solve(A,rhs)+[zero,zero,one]
assert all(add([A[i][j]*c[j] for j in range(4)])==rhs[i] for i in range(4))
print('Coefficient system solved exactly',round(time.time()-start,2),flush=True)
red=[[conv(j==r) for j in range(M)] for r in range(M)]
for r in range(M,N):red.append([-add([c[k]*red[r-M+k][j] for k in range(M)]) for j in range(M)])
matrices={}
for b in range(N):
    matrices[b]=[[G(1,1,a,b)*v for v in red[a]]+[G(-1,1,a,b),G(1,-1,a,b)]+[G(-1,-1,a,b)*v for v in red[-a%N]] for a in range(N)]
z={}
k0=-H*(s[5]+add([c[k]*s[k-1] for k in range(1,6)]))/c[0]
z[1]=[k0]+[H*s[d-1] for d in range(1,6)]+[H,f(0,1)-k0-H]+[zero]*6
k1=-(u[5]+add([c[k]*u[k-1] for k in range(1,6)]))/c[0]
k0=-(u[4]+c[1]*k1+add([c[k]*u[k-2] for k in range(2,6)]))/c[0]
hp=(f(1,2)-G(1,1,1,2)*k1)/G(1,-1,1,2)
km1=(f(10,2)-T*G(-1,1,10,2))/G(-1,-1,10,2)
km0=f(0,2)-k0-T-hp
z[2]=[k0,k1]+u[:4]+[T,hp]+[km0,km1]+[zero]*4
for b in [1,2]:assert all(add([x*y for x,y in zip(row,z[b])])==f(a,b) for a,row in enumerate(matrices[b]))
print('Both singular edge rows matched exactly',round(time.time()-start,2),flush=True)
cols={0:[0,1,2,3,4,5,6,8,9,10,11],3:[0,1,2,3,4,5,6,7,8,9,10],4:[0,1,2,3,4,5,6,7,9,10,11],5:[0,1,2,3,4,5,6,9,10,11,12]}
dets={}
for b,C in cols.items():
    B=[[row[j] for j in C] for row in matrices[b]]
    v=solve(B,[f(a,b) for a in range(N)])
    z[b]=[zero]*14
    for j,val in zip(C,v):z[b][j]=val
    assert all(add([x*y for x,y in zip(row,z[b])])==f(a,b) for a,row in enumerate(matrices[b]))
    print('Full row solved and checked',b,round(time.time()-start,2),flush=True)
for b in range(1,6):z[N-b]=z[b][8:14]+[z[b][7],z[b][6]]+z[b][:6]
checks=[all(add([x*y for x,y in zip(row,z[b])])==f(a,b) for a,row in enumerate(matrices[b])) for b in range(N)]
assert all(checks)
C=add([q**(-t*t%N) for t in range(N)])/conv(N)
assert C
# Independently derive all Fourier coefficients from literal Weyl trace formula.
trace_checks=[add([q**((-b*t-(t+a)*t)%N) for t in range(N)])/conv(N)==C*f(a,b) for a in range(N) for b in range(N)]
assert all(trace_checks)
D5=[[s[r+k] for k in range(4)] for r in range(4)]
d5=solve(D5,[-s[r+5] for r in range(4)])+[zero,one]
res5=[u[r+5]+add([d5[k]*u[r+k] for k in range(5)]) for r in range(2)]
assert all(res5)
result={'restricted_quintic_ascending':[encoded(v) for v in d5], 'restricted_quintic_row_two_residuals':[encoded(v) for v in res5], 'N':N,'banks':14,'orientation_counts':[6,1,1,6],'coefficient_field':'Splitting field of g over Q(q), q primitive eleventh root','g_ascending':[encoded(v) for v in c],'moment_one':[encoded(v) for v in s],'moment_two':[encoded(v) for v in u],'coefficient_matrix':[[encoded(v) for v in row] for row in A],'coefficient_rhs':[encoded(v) for v in rhs],'H':encoded(H),'T':encoded(T),'C':encoded(C),'row_vectors':{str(b):[encoded(v) for v in z[b]] for b in range(N)},'all_121_weyl_equations':all(checks),'all_121_trace_coefficients':all(trace_checks),'seconds':time.time()-start,'exact_arithmetic':'SymPy QQ algebraic field ANP modulo 1+q+...+q^10; no floating point'}
Path(__file__).with_name('N11_EXACT_WITNESS.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',round(time.time()-start,2),flush=True)
