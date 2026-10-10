"""Fresh author control. No supplied or predecessor program is read or imported.
Finite-field tests illustrate and check the displayed theorem; the proof is symbolic.
"""
import json
from pathlib import Path
from math import prod

OUT=Path(__file__).resolve().parent

def prime(p):
    return p>=2 and all(p%d for d in range(2,int(p**0.5)+1))

def field(N):
    p=N+1
    while not prime(p): p+=N
    for q in range(2,p):
        if pow(q,N,p)==1 and all(pow(q,d,p)!=1 for d in range(1,N)):
            return p,q
    raise AssertionError((N,p))

def solve(A,b,p):
    n=len(A)
    R=[[x%p for x in row]+[b[i]%p] for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n) if R[i][j])
        R[j],R[k]=R[k],R[j]
        a=pow(R[j][j],-1,p);R[j]=[a*x%p for x in R[j]]
        for i in range(n):
            if i!=j:
                a=R[i][j];R[i]=[(x-a*y)%p for x,y in zip(R[i],R[j])]
    return [R[i][-1] for i in range(n)]

def rank(A,p):
    A=[list(row) for row in A]; r=0
    for j in range(len(A[0])):
        k=next((i for i in range(r,len(A)) if A[i][j]%p),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        inv=pow(A[r][j],-1,p);A[r]=[x*inv%p for x in A[r]]
        for i in range(r+1,len(A)):
            t=A[i][j];A[i]=[(x-t*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def inverse(A,p):
    n=len(A);R=[[x%p for x in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next(i for i in range(j,n) if R[i][j]);R[j],R[k]=R[k],R[j]
        inv=pow(R[j][j],-1,p);R[j]=[x*inv%p for x in R[j]]
        for i in range(n):
            if i!=j:
                t=R[i][j];R[i]=[(x-t*y)%p for x,y in zip(R[i],R[j])]
    return [row[n:] for row in R]

def mul(A,B,p):
    n=len(A)
    return [[sum(A[i][r]*B[r][j] for r in range(n))%p for j in range(n)] for i in range(n)]

def run(N,literal=False):
    p,q=field(N);m=N-2;h=(N-1)//2
    X=[pow(q,j,p) for j in range(2,N)]
    slots=[(1,1,x) for x in X]+[(-1,1,1),(1,-1,1)]+[(-1,-1,x) for x in X]
    assert len(slots)==2*N-2
    def G(e,d,a,b):
        r=(e*a)%N;l=(d*b)%N
        if r+l>=N:return 0
        z=pow(q,(e*d)%N,p);num=den=1
        for j in range(1,l+1):
            num=num*(1-pow(z,r+j,p))%p
            den=den*(1-pow(z,j,p))%p
        return num*pow(den,-1,p)%p
    def interp(vals,start):
        d=len(vals)
        return solve([[pow(X[i],r,p) for i in range(d)] for r in range(start,start+d)],vals,p)+[0]*(m-d)
    def pos(row,b):
        if b==1:
            y=row[N-1]*pow(G(-1,1,N-1,1),-1,p)%p
            vals=[(row[a]-y*G(-1,1,a,1))*pow(G(1,1,a,1),-1,p)%p for a in range(1,N-1)]
            P=interp(vals,1);z=(row[0]-y-sum(P))%p
            return P+[y,z]+[0]*m
        a=N-b;y=row[a]*pow(G(-1,1,a,b),-1,p)%p
        P=interp([(row[a]-y*G(-1,1,a,b))*pow(G(1,1,a,b),-1,p)%p for a in range(N-b)],0)
        vals=[0]+[(row[N-r]-y*G(-1,1,N-r,b))*pow(G(-1,-1,N-r,b),-1,p)%p for r in range(1,b)]
        Q=interp(vals,0)
        return P+[y,0]+Q
    # A fixed nontrivial dense coefficient target, no Fourier symmetry assumed.
    C=[[(a*a+3*a*b+7*b*b+5*a+11*b+13+pow(2,(a+2*b)%17,p))%p for b in range(N)] for a in range(N)]
    amps=[[0]*N for _ in slots]
    d=[sum(C[a][0]*pow(q,(-j*a)%N,p) for a in range(N))*pow(N,-1,p)%p for j in range(N)]
    row0=d[2:]+[d[0],0]+[0]*(m-1)+[d[1]]
    for i,x in enumerate(row0):amps[i][0]=x
    for b in range(1,N):
        if b<=h:
            row=pos([C[a][b] for a in range(N)],b)
        else:
            v=pos([C[(-a)%N][b] for a in range(N)],N-b)
            row=v[m+2:]+[v[m+1],v[m]]+v[:m]
        for i,(e,dd,x) in enumerate(slots):amps[i][(dd*b)%N]=row[i]
    ranks=[]
    for b in range(N):
        M=[[G(e,d,a,b)*pow(x,(e*a)%N,p)%p for e,d,x in slots] for a in range(N)]
        ranks.append(rank(M,p))
        for a in range(N):
            got=sum(M[a][i]*amps[i][(slots[i][1]*b)%N] for i in range(len(slots)))%p
            assert got==C[a][b],(N,p,a,b,got,C[a][b])
    assert ranks==[N]*N
    res={'N':N,'p':p,'q':q,'slots':len(slots),'row_ranks':ranks,'weyl_equations_checked':N*N,'literal_branches_checked':0}
    if literal:
        acc=[[0]*N for _ in range(N)];I=[[int(i==j) for j in range(N)] for i in range(N)]
        for i,(e,d,x) in enumerate(slots):
            assert (1-pow(x,N,p)-1)%p==p-1
            ws=[-sum(amps[i][l]*pow(q,(-e*d*j*l)%N,p) for l in range(N))%p for j in range(N)]
            for j,w in enumerate(ws):
                H=[[int(k==t) for t in range(N)] for k in range(N)]
                for t in range(N):
                    H[(t+e)%N][t]=(H[(t+e)%N][t]-x)%p
                    H[t][t]=(H[t][t]-pow(q,(e*d*j+d*t)%N,p))%p
                V=inverse(H,p)
                assert mul(H,V,p)==I and mul(V,H,p)==I
                for k in range(N):
                    for t in range(N):acc[k][t]=(acc[k][t]+w*V[k][t]*pow(N,-1,p))%p
        target=[[sum(C[(k-t)%N][b]*pow(q,(b*t)%N,p) for b in range(N))%p for t in range(N)] for k in range(N)]
        assert acc==target
        res['literal_branches_checked']=N*len(slots)
        res['original_matrix_entries_checked']=N*N
    return res

if __name__=='__main__':
    results=[run(N,literal=N in (3,5,9,15)) for N in range(3,42,2)]
    out={'status':'PASS','scope':'Fresh finite-field controls of the explicit all-order construction; the theorem is proved symbolically, not inferred from tests.','results':results}
    (OUT/'FRESH_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','orders':[r['N'] for r in results],'total_weyl_equations':sum(r['weyl_equations_checked'] for r in results),'literal_branches':sum(r['literal_branches_checked'] for r in results),'literal_entries':sum(r.get('original_matrix_entries_checked',0) for r in results)},indent=2))
