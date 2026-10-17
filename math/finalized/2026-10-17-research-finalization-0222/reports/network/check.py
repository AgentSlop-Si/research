#!/usr/bin/env python3
"""Fresh exact checker; standard library only; no historical code is imported.

The rank-one separated-generator chart is S_ii=d_i,
S_ij=l_i*m_j for i>j and S_ij=u_i*v_j for i<j.
P e_j=e_{p[j]}; Phi(A,B)=B P A. All computations are exact.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
from math import isqrt

N=8
PRIME=1000000007
P=[7,0,6,3,4,1,2,5]

def detexact(a):
    a=[row[:] for row in a];sign=1;previous=1
    if len(a)==1:return a[0][0]
    for k in range(len(a)-1):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        v=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                value=a[i][j]*v-a[i][k]*a[k][j]
                assert value%previous==0
                a[i][j]=value//previous
            a[i][k]=0
        previous=v
    return sign*a[-1][-1]

def stage(a):
    d,l,m,u,v=[a[k*N:(k+1)*N] for k in range(5)]
    return [[d[i] if i==j else (l[i]*m[j] if i>j else u[i]*v[j])
             for j in range(N)] for i in range(N)]

def word(a,p=P):
    A,B=stage(a[:40]),stage(a[40:])
    return [[sum(B[i][p[k]]*A[k][j] for k in range(N))
             for j in range(N)] for i in range(N)]

def detmod(a,p=PRIME):
    a=[[v%p for v in row] for row in a]
    ans=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];ans=-ans
        x=a[j][j];ans=ans*x%p;inv=pow(x,-1,p)
        for i in range(j+1,len(a)):
            q=a[i][j]*inv%p
            for k in range(j+1,len(a)):a[i][k]=(a[i][k]-q*a[j][k])%p
    return ans%p

def rankmod(a,p=PRIME):
    a=[[v%p for v in row] for row in a];r=0;pivots=[]
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][c],-1,p)
        a[r]=[v*inv%p for v in a[r]]
        for i in range(r+1,len(a)):
            q=a[i][c]
            if q:a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
        pivots.append(c);r+=1
        if r==len(a):break
    return r,pivots

def main():
    assert all(PRIME%d for d in range(2,isqrt(PRIME)+1))
    # Deterministic explicit integer parameters. No random search is used.
    params=[1+int.from_bytes(hashlib.sha256(('N8-separated-'+str(i)).encode()).digest()[:4],'big')%1009 for i in range(80)]
    W=word(params)
    minors=[]
    for k in range(1,N+1):
        zero=[];digest=hashlib.sha256();exact_digest=hashlib.sha256();count=0
        for rows in combinations(range(N),k):
            for cols in combinations(range(N),k):
                block=[[W[i][j] for j in cols] for i in rows]
                d=detmod(block);e=detexact(block);count+=1
                assert e%PRIME==d
                exact_digest.update(f'{rows}|{cols}|{e}\n'.encode())
                digest.update(f'{rows}|{cols}|{d}\n'.encode())
                if d==0:zero.append([rows,cols])
        minors.append({'size':k,'count':count,'zero_count':len(zero),'zero_examples':zero[:3],'ordered_residue_sha256':digest.hexdigest(),'ordered_exact_determinant_sha256':exact_digest.hexdigest()})
    # Each parameter occurs affinely in Phi: exact unit differences ARE derivatives.
    derivatives=[]
    for i in range(80):
        nxt=params[:];nxt[i]+=1;V=word(nxt)
        derivatives.append([V[r][c]-W[r][c] for r in range(N) for c in range(N)])
    J=[list(row) for row in zip(*derivatives)]
    rank,cols=rankmod(J)
    _,rows=rankmod([[J[r][c] for r in range(64)] for c in cols])
    certdet=detmod([[J[r][c] for c in cols] for r in rows])
    # Independent mixed derivative via a two-unit check catches non-affine accidents.
    derivative_checks=[]
    for i in range(80):
        nxt=params[:];nxt[i]+=2;V=word(nxt)
        derivative_checks.append(all(V[r][c]-W[r][c]==2*derivatives[i][r*N+c] for r in range(N) for c in range(N)))
    out={'n':N,'prime':PRIME,'permutation':P,'permutation_convention':'P e_j = e_{p[j]}','parameters':params,'integer_matrix':W,'stage_determinants_mod_prime':[detmod(stage(params[:40])),detmod(stage(params[40:]))], 'minor_checks':minors,'total_square_minors':sum(x['count'] for x in minors),'zero_square_minors':sum(x['zero_count'] for x in minors),'jacobian_rank_mod_prime':rank,'jacobian_minor_rows':rows,'jacobian_minor_columns':cols,'jacobian_minor_determinant_mod_prime':certdet,'exact_affine_derivative_checks':sum(derivative_checks),'claims_not_tested':['graph max-flow census','historical seed','N16 tangent certificate','Fourier membership','minimal defining ideal','worldwide priority']}
    assert out['total_square_minors']==12869
    assert out['zero_square_minors']==0
    assert rank==60 and certdet!=0 and len(rows)==len(cols)==60
    assert all(derivative_checks)
    assert all(out['stage_determinants_mod_prime'])
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['total_square_minors','zero_square_minors','jacobian_rank_mod_prime','jacobian_minor_determinant_mod_prime','exact_affine_derivative_checks','stage_determinants_mod_prime']},indent=2))

if __name__=='__main__':main()
