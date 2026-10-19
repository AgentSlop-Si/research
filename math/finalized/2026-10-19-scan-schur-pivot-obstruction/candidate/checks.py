#!/usr/bin/env python3
"""Original exact controls. No historical imports or external dependencies."""
from fractions import Fraction as F
from pathlib import Path
import json


def zeros(r,c=None):
    return [[0]*(r if c is None else c) for _ in range(r)]

def eye(n):
    a=zeros(n)
    for i in range(n): a[i][i]=1
    return a

def tr(a): return [list(x) for x in zip(*a)]

def add(*aa):
    return [[sum(a[i][j] for a in aa) for j in range(len(aa[0][0]))] for i in range(len(aa[0]))]

def scale(a,c): return [[c*x for x in r] for r in a]

def mul(a,b):
    c=zeros(len(a),len(b[0]))
    for i,row in enumerate(a):
        for k,x in enumerate(row):
            if x:
                for j,y in enumerate(b[k]):
                    if y: c[i][j]+=x*y
    return c

def mv(a,v): return [sum(x*y for x,y in zip(r,v)) for r in a]

def block(a,b,c,d):
    return [x+y for x,y in zip(a,b)]+[x+y for x,y in zip(c,d)]

def take(a,ii,jj): return [[a[i][j] for j in jj] for i in ii]

def shift(n):
    a=zeros(n)
    for i in range(1,n):a[i][i-1]=1
    return a

def rev(i,q):
    r=0
    for _ in range(q):r=(r<<1)|(i&1);i>>=1
    return r

def perm(n):
    q=n.bit_length()-1;a=zeros(n)
    for j in range(n):a[rev(j,q)][j]=1
    return a

def anchor(n,diag=3):
    a=add(scale(eye(n),diag),shift(n),tr(shift(n)))
    a[0][0]+=1
    return a

def rank(a,p=None):
    a=[[x%p for x in r] for r in a] if p else [[F(x) for x in r] for r in a]
    r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        inv=pow(int(a[r][j]),-1,p) if p else 1/a[r][j]
        a[r]=[(x*inv)%p for x in a[r]] if p else [x*inv for x in a[r]]
        for k in range(r+1,len(a)):
            z=a[k][j]
            if z:
                a[k]=[(x-z*y)%p for x,y in zip(a[k],a[r])] if p else [x-z*y for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r

def det(a):
    a=[[F(x) for x in r] for r in a];v=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];v=-v
        z=a[j][j];v*=z
        for k in range(j+1,len(a)):
            b=a[k][j]/z
            for l in range(j,len(a)):a[k][l]-=b*a[j][l]
    return v

def band(n,w=2):
    return [(i,j) for i in range(n) for j in range(max(0,i-w),min(n,i+w+1))]

def schur_derivative(x,n):
    ee=take(x,list(range(0,2*n,2)),list(range(0,2*n,2)))
    eo=take(x,list(range(0,2*n,2)),list(range(1,2*n,2)))
    oe=take(x,list(range(1,2*n,2)),list(range(0,2*n,2)))
    oo=take(x,list(range(1,2*n,2)),list(range(1,2*n,2)))
    b=add(eye(n),shift(n))
    return add(ee,scale(mul(eo,tr(b)),F(-1,3)),scale(mul(b,oe),F(-1,3)),scale(mul(mul(b,oo),tr(b)),F(1,9)))

out={"scope":"Exact Schur-route obstruction; full endpoint H_N remains unresolved.","local":[],"pivot":[]}
for n in [4,8,16]:
    b=add(eye(n),shift(n));t=anchor(2*n);order=list(range(0,2*n,2))+list(range(1,2*n,2))
    tp=take(t,order,order);a=scale(eye(n),3);a[0][0]+=1
    assert tp==block(a,b,tr(b),scale(eye(n),3))
    s=add(a,scale(mul(b,tr(b)),F(-1,3)))
    want=add(scale(eye(n),F(7,3)),scale(shift(n),F(-1,3)),scale(tr(shift(n)),F(-1,3)))
    want[0][0]+=F(4,3)
    assert s==want
    mod=lambda z: int(z.numerator)*pow(int(z.denominator),-1,5)%5 if isinstance(z,F) else z%5
    assert [[mod(x) for x in r] for r in s]==[[3*x%5 for x in r] for r in anchor(n)]
    c=block(eye(n),scale(b,F(1,3)),zeros(n),eye(n))
    assert mul(mul(c,block(s,zeros(n),zeros(n),scale(eye(n),3))),tr(c))==tp
    j=anchor(n,-2);diff=add(eye(n),scale(shift(n),-1))
    assert j==scale(mul(diff,tr(diff)),-1)
    jpar=take(anchor(2*n,-2),order,order)
    assert add(take(jpar,list(range(n)),list(range(n))),scale(mul(b,tr(b)),F(1,2)))==scale(j,F(1,2))
    row={"smaller_n":n,"parity_schur_factorization":True,"mod5_scale":3,"negative_laplacian_identity":True}
    if n<=8:
        for i,jj in band(2*n):
            x=zeros(2*n);x[i][jj]=1;y=schur_derivative(x,n)
            assert all(y[i][j]==0 for i in range(n) for j in range(n) if abs(i-j)>2)
        for i,jj in band(n):
            goal=zeros(n);goal[i][jj]=1;x=zeros(2*n)
            if jj-i==2:x[2*i+1][2*(i+1)+1]=9
            elif i-jj==2:x[2*(jj+1)+1][2*jj+1]=9
            got=schur_derivative(x,n)
            for a0 in range(n):
                for b0 in range(n):
                    rem=goal[a0][b0]-got[a0][b0]
                    assert abs(a0-b0)<=1 or rem==0
                    x[2*a0][2*b0]+=rem
            assert schur_derivative(x,n)==goal
        row.update({"all_input_basis_support_checked":10*n-6,"all_output_basis_preimages_checked":5*n-6,"kernel_dimension":5*n})
    out["local"].append(row)

for h in [2,4,8,16,32,64]:
    q=h.bit_length()-1;N=4*h;n=2*h;p=perm(h);l=shift(h);d=add(eye(h),l);f=zeros(h);f[0][h-1]=1
    t=anchor(N);pn=perm(N);tpt=mul(mul(t,pn),t);odd=list(range(1,N,2));o=take(tpt,odd,odd)
    top=add(mul(mul(tr(d),p),d),scale(add(f,tr(f)),3))
    formula=block(top,scale(mul(p,d),3),scale(mul(tr(d),p),3),scale(p,9))
    assert o==formula
    r=add(mul(mul(tr(d),p),d),scale(mul(mul(mul(mul(p,d),p),tr(d)),p),-1),scale(add(f,tr(f)),3))
    u=mul(mul(p,tr(l)),p)
    assert r==add(mul(p,add(mul(u,l),scale(mul(l,u),-1))),scale(add(f,tr(f)),3))
    M=[(1<<b)-1 for b in range(q+1)];outside=[x for x in range(h) if x not in M]
    assert all(r[i][j]==0 for i in range(h) for j in range(h) if i not in M or j not in M)
    small=take(r,M,M)
    expected=[[int(a+b==q-1)-int(a+b==q+1)+3*int((a==0 and b==q) or (a==q and b==0)) for b in range(q+1)] for a in range(q+1)]
    assert small==expected
    jr=list(reversed(small));tri=add(shift(q+1),scale(tr(shift(q+1)),-1));tri[0][0]+=3;tri[q][q]+=3
    assert jr==tri
    determinant=det(jr);assert determinant==(6 if q%2==0 else 10)
    assert rank(small)==q+1
    rq5=h+rank(small,5);assert rq5==h+q+int(q%2==0)
    assert rank(o,5)==rq5
    for x in outside:
        e=[int(i==x) for i in range(h)];w=[3*z for z in e]+[-z for z in mv(mul(mul(p,tr(d)),p),e)]
        assert mv(o,w)==[0]*(2*h)
        if x==2:
            expectedw=[3*int(i==2) for i in range(h)]+[-int(i==2)-int(i==h-4) for i in range(h)]
            assert w==expectedw
            wf=[0]*N
            for i,idx in enumerate(odd):wf[idx]=w[i]
            assert any(mv(tpt,wf)) # This is not a null vector of the full invertible product.
    out["pivot"].append({"N":N,"h":h,"q":q,"monotone_support":M,"rank_Q_from_exact_Schur":h+q+1,"rank_mod5":rq5,"integer_null_vectors_checked":len(outside),"small_tridiagonal_determinant":int(determinant)})

N=8;t=N//4+1;p=5;A=mul(anchor(N),perm(N));powers=[eye(N)]
for _ in range(t-1):powers.append([[x%p for x in r] for r in mul(powers[-1],A)])
columns=[]
for k in range(t):
    for i,j in band(N):
        columns.append([powers[k][r][i]*powers[t-1-k][s][j]%p for r in range(N) for s in range(N)])
hrank=rank(tr(columns),p);assert hrank==64
h=2;p2=perm(h);d=add(eye(h),shift(h));f=zeros(h);f[0][-1]=1
O=block(add(mul(mul(tr(d),p2),d),scale(add(f,tr(f)),3)),scale(mul(p2,d),3),scale(mul(tr(d),p2),3),scale(p2,9))
assert det(scale(O,F(1,9)))==F(-10,81)
out["positive_scope_control"]={"N":8,"H_rank_mod5":hrank,"odd_dressed_pivot_determinant_Q":"-10/81","odd_dressed_pivot_rank_mod5":rank(O,5),"does_not_imply_H_failure":True}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
