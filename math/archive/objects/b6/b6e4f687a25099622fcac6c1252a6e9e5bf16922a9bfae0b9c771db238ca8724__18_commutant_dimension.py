"""Exact modular rank of simultaneous commutant of T and V.
V has distinct values except symmetric coordinates, so X commuting with V
is supported on (i,i) and (i,-i). Solve [X,T]=0 on that space.
"""
import json
from harper_certificate import P,root_n


def rank_mod(A):
    if not A:return 0
    x=[row[:] for row in A]
    h=len(x);w=len(x[0]);r=0
    for j in range(w):
        pivot=next((i for i in range(r,h) if x[i][j]),None)
        if pivot is None:continue
        x[r],x[pivot]=x[pivot],x[r]
        p=pow(x[r][j],-1,P)
        x[r][j:]=[v*p%P for v in x[r][j:]]
        for i in range(r+1,h):
            if x[i][j]:
                f=x[i][j]
                for k in range(j,w):x[i][k]=(x[i][k]-f*x[r][k])%P
        r+=1
        if r==h:break
    return r


def audit(n):
    assert n>=4 and n%2==0
    basis=[(i,j) for i in range(n) for j in set((i,(-i)%n))]
    # use canonical sorted for reproducing column order
    basis.sort()
    coeffs=[[0]*len(basis) for _ in range(n*n)]
    for k,(a,b) in enumerate(basis):
        # (E*T)_{ij}=1_{i=a}(delta_{b,j+1}+delta_{b,j-1})
        # (T*E)_{ij}=1_{j=b}(delta_{i,a+1}+delta_{i,a-1})
        for j in ((b-1)%n,(b+1)%n):coeffs[a*n+j][k]+=1
        for i in ((a-1)%n,(a+1)%n):coeffs[i*n+b][k]-=1
    coeffs=[[v%P for v in row] for row in coeffs]
    r=rank_mod(coeffs)
    assert len(basis)-r==2
    return {'n':n,'commuting_with_V_parameter_count':len(basis),
            'extra_independent_T_constraints':r,'joint_commutant_dimension':len(basis)-r,
            'predicted_commutant':'span{I,J}'}

if __name__=='__main__':
    print(json.dumps([audit(n) for n in (4,8,16,32,64)],indent=2))
