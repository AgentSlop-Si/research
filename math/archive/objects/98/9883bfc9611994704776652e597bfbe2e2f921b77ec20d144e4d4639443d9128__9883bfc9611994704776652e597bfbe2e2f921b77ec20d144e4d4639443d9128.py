"""Exploratory: one-pass rank-r tile cost r*(rows+cols) for all rectangles.
This is a deliberately *defined* dense-factor accounting model. The result is
not a gate lower bound because factors may be sparse and sharing is excluded.
"""
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from phase7 import test_field,optimal_tile_cost


def rank_mod(mat,p):
    arr=[[v%p for v in row] for row in mat]
    m=len(arr);n=len(arr[0])
    rank=0
    for j in range(n):
        pivot=next((k for k in range(rank,m) if arr[k][j]),None)
        if pivot is None:continue
        arr[rank],arr[pivot]=arr[pivot],arr[rank]
        inv=pow(arr[rank][j],-1,p)
        for jj in range(j,n):arr[rank][jj]=arr[rank][jj]*inv%p
        for rr in range(rank+1,m):
            c=arr[rr][j]
            if c:
                for jj in range(j,n):arr[rr][jj]=(arr[rr][jj]-c*arr[rank][jj])%p
        rank+=1
        if rank==m:break
    return rank


def solve(n):
    p,w=test_field(n)
    powers=[pow(w,(-u)%n,p) for u in range(n)]
    subsets=[tuple(k for k in range(n) if mask>>k&1) for mask in range(1,1<<n)]
    options=[]
    for I in subsets:
        for J in subsets:
            r=rank_mod([[powers[(i*j)%n] for j in J] for i in I],p)
            options.append((I,J,r))
    o=[r*(len(I)+len(J)) for I,J,r in options]
    M=lil_matrix((n*n,len(options)))
    for col,(I,J,r) in enumerate(options):
        for i in I:
            for j in J:
                M[i*n+j,col]=1
    res=milp(c=o,integrality=[1]*len(o),bounds=Bounds(0,1),constraints=LinearConstraint(M.tocsr(),1,1),options={'time_limit':60,'mip_rel_gap':0})
    chosen=[options[i] for i,v in enumerate(res.x) if v>.5]
    return {'n':n,'opts':len(options),'ranked_cost':round(res.fun),'rankone_cost':optimal_tile_cost(n),'status':res.status, 'mix':{r:sum(1 for I,J,rr in chosen if r==rr) for I,J,r in chosen}}
if __name__=='__main__':
    for n in range(2,7):
        print(solve(n),flush=True)
