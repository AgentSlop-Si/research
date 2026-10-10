#!/usr/bin/env python3
"""Fresh exact controls; dense arithmetic is only a bounded test oracle."""
import json, hashlib
from pathlib import Path


def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def mm(a,b,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)]for row in a]
def mv(a,x,p):return [sum(u*v for u,v in zip(row,x))%p for row in a]
def determinant(a,p):
    a=[r[:]for r in a];d=1
    for j in range(len(a)):
        k=next((k for k in range(j,len(a))if a[k][j]),None)
        if k is None:return 0
        if k!=j:a[j],a[k]=a[k],a[j];d=-d
        t=a[j][j];d=d*t%p;iv=pow(t,-1,p)
        for k in range(j+1,len(a)):
            c=a[k][j]*iv%p
            for l in range(j,len(a)):a[k][l]=(a[k][l]-c*a[j][l])%p
    return d%p

def solve(a,b,p):
    n=len(a);a=[row[:]+[x]for row,x in zip(a,b)]
    for j in range(n):
        k=next((k for k in range(j,n)if a[k][j]),None)
        assert k is not None
        a[j],a[k]=a[k],a[j];iv=pow(a[j][j],-1,p);a[j]=[v*iv%p for v in a[j]]
        for k in range(n):
            if k!=j:
                c=a[k][j];a[k]=[(v-c*w)%p for v,w in zip(a[k],a[j])]
    return [row[-1]for row in a]

def kernel(x,z,p):
    n=len(x);y=list(x);y[0]=0;scale=1;edges=0
    while scale<n:
        for odd in range(1,n//scale,2):
            s=scale*odd;parent=2*s%n
            if parent:y[parent]=(y[parent]+z*y[s])%p;edges+=1
        scale*=2
    y[0]=-sum(y[1:])%p
    assert sum(y)%p==0
    return y,edges

def kernel_jet(x,p):
    N=len(x);n=N.bit_length()-1;y=[[0]]+[[v%p]for v in x[1:]];scale=1
    while scale<N:
        for odd in range(1,N//scale,2):
            s=scale*odd;parent=2*s%N
            if parent:
                need=len(y[s])+1
                y[parent]+=[0]*max(0,need-len(y[parent]))
                for j,v in enumerate(y[s]):y[parent][j+1]=(y[parent][j+1]+v)%p
        scale*=2
    y[0]=[0]*n
    for row in y[1:]:
        for j,v in enumerate(row):y[0][j]=(y[0][j]-v)%p
    assert sum(len(row)for row in y)==2*N-2
    for i in range(1,N):assert len(y[i])==(i&-i).bit_length()
    return y

def case(N,p,w,z):
    assert pow(w,N,p)==1 and pow(w,N//2,p)!=1
    m=N//2;A=[[0]*N for _ in range(N)];Q=[[0]*N for _ in range(N)]
    for s in range(N):
        A[2*s%N][s]=1;Q[2*s%N][s]=1;Q[(2*s+1)%N][s]=pow(w,s,p)
    IQ=[[(int(i==j)-z*Q[i][j])%p for j in range(N)]for i in range(N)]
    IA=[[(int(i==j)-z*A[i][j])%p for j in range(N)]for i in range(N)]
    cols=[kernel([int(i==j)for i in range(N)],z,p)[0]for j in range(N)]
    K=list(map(list,zip(*cols)));E=[[int(i==0)for j in range(N)]for i in range(N)]
    assert mm(IA,K,p)==[[(int(i==j)-E[i][j])%p for j in range(N)]for i in range(N)]
    assert all(K[i][0]==0 for i in range(N)) and all(sum(K[i][j]for i in range(N))%p==0 for j in range(N))
    def C(v):return [pow(w,r,p)*(v[r]-v[r+m])%p for r in range(m)]
    KJ=[[K[i][2*j+1]for j in range(m)]for i in range(N)]
    HT=list(map(list,zip(*(C([KJ[i][j]for i in range(N)])for j in range(m)))))
    M=[[(int(i==j)-z*HT[i][j])%p for j in range(m)]for i in range(m)]
    B=[M[i]+[(-int(i==0))%p]for i in range(m)]+[[(-z)%p]*m+[(1-z)%p]]
    d=determinant(IQ,p);db=determinant(B,p);assert d==db
    solves=0;marked=0
    if d:
        for trial in range(3):
            x=[(i*i+7*i+trial*11+3)%p for i in range(N)]
            kx,edges=kernel(x,z,p);jet=kernel_jet(x,p)
            assert [sum(v*pow(z,j,p)for j,v in enumerate(row))%p for row in jet]==kx
            rhs=C(kx)+[sum(x)%p]
            sol=solve(B,rhs,p);u,t=sol[:-1],sol[-1]
            ju=[u[i//2]if i%2 else 0 for i in range(N)]
            kju,_=kernel(ju,z,p)
            y=[(kx[i]+z*kju[i]+(t if i==0 else 0))%p for i in range(N)]
            assert mv(IQ,y,p)==x and y==solve(IQ,x,p)
            h=[(5*i+2*trial+1)%p for i in range(N)]
            aa=[z*sum(h[i]*KJ[i][j]for i in range(N))%p for j in range(m)]+[h[0]]
            marked_val=(sum(h[i]*kx[i]for i in range(N))+sum(a*b for a,b in zip(aa,sol)))%p
            assert marked_val==sum(a*b for a,b in zip(h,y))%p
            solves+=1;marked+=1
    return {'N':N,'prime':p,'z':z,'det_original':d,'det_regularized_border':db,'root_pole_parameter':z==1,'M_singular':determinant(M,p)==0,'exact_solve_controls':solves,'marked_bilinear_controls':marked,'full_tree_jet_coefficient_capacity':2*N-2,'tree_nonroot_propagations':N-2,'border_dimension':m+1}

cases=[]
for p,g,sizes in [(97,5,(2,4,8,16,32)),(65537,3,(2,4,8,16,32,64)),(3,2,(2,))]:
    for N in sizes:
        w=pow(g,(p-1)//N,p)
        for z in sorted({0,1,2,pow(2,-1,p),3%p}):cases.append(case(N,p,w,z))
assert any(c['prime']==3 and c['z']==1 and c['M_singular']and c['det_original']for c in cases)
out={'cases':cases,'all_exact_assertions_passed':True,'dense_matrices_determinants_and_solves_are_test_oracles_only':True,'source_uploaded_code_executed':False,'scope':'Pole cancellation and an exact half-size bordered reduction; the coupled border solve and marked coefficient extraction remain unsolved fast operations.'}
Path(__file__).with_name('ROOT_POLE_CANCELLATION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'case_count':len(cases),'root_pole_cases':sum(c['root_pole_parameter']for c in cases),'vector_solve_controls':sum(c['exact_solve_controls']for c in cases),'marked_controls':sum(c['marked_bilinear_controls']for c in cases),'all_exact_assertions_passed':True},indent=2))
