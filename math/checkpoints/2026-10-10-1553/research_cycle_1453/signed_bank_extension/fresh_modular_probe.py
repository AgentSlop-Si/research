"""Fresh author implementation of generic finite-field moment construction.
Reads no source programs or witness files. Search is not the proof.
"""
import json
from pathlib import Path


def inv(a,p):return pow(a%p,-1,p)
def rank_pivots(A,p):
    A=[list(row) for row in A]; m=len(A); n=len(A[0]); piv=[]; vals=[]; row=0
    for col in range(n):
        k=next((k for k in range(row,m) if A[k][col]%p),None)
        if k is None:continue
        if k!=row:A[k],A[row]=A[row],A[k]
        a=A[row][col]%p;vals.append(a);z=inv(a,p);A[row]=[x*z%p for x in A[row]]
        for k in range(row+1,m):
            z=A[k][col]%p;A[k]=[(x-z*y)%p for x,y in zip(A[k],A[row])]
        piv.append(col);row+=1
        if row==m:break
    return row,piv,vals

def solve(A,b,p):
    n=len(A);A=[[v%p for v in row]+[b[i]%p] for i,row in enumerate(A)]
    for j in range(n):
        k=next(k for k in range(j,n) if A[k][j]);A[j],A[k]=A[k],A[j]
        v=inv(A[j][j],p);A[j]=[x*v%p for x in A[j]]
        for i in range(n):
            if i!=j:
                v=A[i][j];A[i]=[(x-v*y)%p for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]

def det(A,p):
    A=[list(row) for row in A];n=len(A);v=1
    for j in range(n):
        k=next((k for k in range(j,n) if A[k][j]%p),None)
        if k is None:return 0
        if k!=j:A[k],A[j]=A[j],A[k];v=-v
        u=A[j][j]%p;v=v*u%p
        for i in range(j+1,n):
            z=A[i][j]*inv(u,p)%p;A[i]=[(x-z*y)%p for x,y in zip(A[i],A[j])]
    return v%p

def polyrem(a,b,p):
    a=a[:]
    while a and a[-1]==0:a.pop()
    while len(a)>=len(b):
        z=a[-1]*inv(b[-1],p)%p;d=len(a)-len(b)
        for k,v in enumerate(b):a[k+d]=(a[k+d]-z*v)%p
        while a and a[-1]==0:a.pop()
    return a

def gcd(a,b,p):
    while b:a,b=b,polyrem(a,b,p)
    return [(v*inv(a[-1],p))%p for v in a]

def experiment(N,p,q,c_top=0):
    m=(N-1)//2;ii=inv(4,N);H=q*inv(1+q,p)%p
    f=lambda a,b:pow(q,ii*((a+b)**2)%N,p)
    mom=[1]
    for a in range(2,N-1):
        G=(1-pow(q,a+1,p))*inv(1-q,p)%p
        B=(1-pow(q,a-1,p))*inv(1-inv(q,p),p)%p
        mom.append((f(a,1)*inv(H*G,p)-B*inv(G,p))%p)
    A=[[mom[r+k] for k in range(m-1)] for r in range(m-1)]
    c=solve(A,[(-mom[r+m]-c_top*mom[r+m-1])%p for r in range(m-1)],p)+[c_top,1]
    red=[[int(j==r) for j in range(m)] for r in range(m)]
    for r in range(m,N):red.append([(-sum(c[k]*red[r-m+k][j] for k in range(m)))%p for j in range(m)])
    def G(e,d,a,b):
        r=e*a%N;l=d*b%N
        if r+l>=N:return 0
        z=pow(q,e*d%N,p);v=1
        for j in range(1,l+1):v=v*(1-pow(z,r+j,p))*inv(1-pow(z,j,p),p)%p
        return v
    matrices={};rs=[];minors={}
    for b in range(N):
        B=[]
        for a in range(N):
            B.append([(G(1,1,a,b)*v)%p for v in red[a]]+[G(-1,1,a,b),G(1,-1,a,b)]+[(G(-1,-1,a,b)*v)%p for v in red[-a%N]])
        matrices[b]=B; rank,cols,pivs=rank_pivots(B,p);rs.append(rank)
        if rank==N:minors[b]={'columns':cols,'determinant':det([[row[k] for k in cols] for row in B],p)}
    K0=-H*(mom[m-1]+sum(c[k]*mom[k-1] for k in range(1,m)))*inv(c[0],p)%p
    edge=[K0]+[(H*mom[d-1])%p for d in range(1,m)]+[H,(f(0,1)-K0-H)%p]+[0]*m
    checks=[sum(x*y for x,y in zip(row,edge))%p==f(a,1) for a,row in enumerate(matrices[1])]
    return {'N':N,'prime':p,'q':q,'moments':mom,'moment_matrix':A,'moment_determinant':det(A,p),'polynomial_ascending':c,'gcd_with_derivative':gcd(c,[k*c[k]%p for k in range(1,len(c))],p),'row_ranks':rs,'minors':minors,'edge_vector':edge,'edge_equations':checks,'reduced_powers':red,'matrices':matrices}

if __name__=='__main__':
    p=23;N=11;q=2
    assert pow(q,N,p)==1 and q!=1
    z=experiment(N,p,q)
    Path(__file__).with_name('MODULAR_DISCOVERY.json').write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps({k:v for k,v in z.items() if k not in ['matrices','reduced_powers']},indent=2))
    print('augmented ranks', [rank_pivots([row+[pow(q,(pow(4,-1,N)*(a+b)**2)%N,p)] for a,row in enumerate(z['matrices'][b])],p)[0] for b in range(N)])
