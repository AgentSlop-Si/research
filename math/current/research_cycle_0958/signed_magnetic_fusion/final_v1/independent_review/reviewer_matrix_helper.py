"""Independent incoming-family controls. Only JSON inputs; no supplied program imported."""
import json, math, itertools
from pathlib import Path

BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent

def rankdet(A,p):
    a=[[v%p for v in r] for r in A]; h=len(a); w=len(a[0]) if h else 0
    r=0; d=1; cols=[]
    for c in range(w):
        t=next((i for i in range(r,h) if a[i][c]),None)
        if t is None:continue
        if t!=r:a[r],a[t]=a[t],a[r];d=-d
        v=a[r][c];d=d*v%p;iv=pow(v,-1,p)
        for i in range(r+1,h):
            f=a[i][c]*iv%p
            if f:
                for j in range(c,w):a[i][j]=(a[i][j]-f*a[r][j])%p
        cols.append(c);r+=1
        if r==h:break
    return r,d%p,cols

def inv(A,p):
    n=len(A);a=[[v%p for v in row]+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for c in range(n):
        t=next((i for i in range(c,n) if a[i][c]),None)
        if t is None:return None
        a[c],a[t]=a[t],a[c];v=pow(a[c][c],-1,p);a[c]=[x*v%p for x in a[c]]
        for i in range(n):
            if i!=c:
                v=a[i][c]
                a[i]=[(x-v*y)%p for x,y in zip(a[i],a[c])]
    return [r[n:] for r in a]

def mm(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mv(A,v,p):return [sum(x*y for x,y in zip(r,v))%p for r in A]
def mp(A,k,p):
    z=eye(len(A))
    while k:
        if k&1:z=mm(z,A,p)
        A=mm(A,A,p);k//=2
    return z

def cycle_green(c,w,p):
    # Construct directly from directed paths, rather than invert the sparse matrix.
    n=len(c);H=math.prod(w)%p;den=(1-H)%p;assert den
    G=[[0]*n for _ in c];idn=pow(den,-1,p)
    for j in range(n):
        t=1
        for k in range(n):
            if k:t=t*w[(j+k)%n]%p
            G[c[(j+k)%n]][c[j]]=t*idn%p
    return G

def geometric_jacobian(rec,sign=1):
    n=rec['N'];p=rec['prime'];cycles=rec['cycles'];s=len(cycles)
    phase='gaussian_ab' in rec;ii=pow(3 if p==998244353 else 31,(p-1)//4,p)*sign%p
    if phase:
        w=[1]*(n-1)
        for a,b in rec['gaussian_ab']:
            assert (a-b*ii)%p
            w.append((a+b*ii)*pow((a-b*ii)%p,-1,p)%p)
    else:
        raw=rec['integer_weights'];v=[1]*n
        for j in range(1,n-1):v[j]=v[j-1]*raw[0][j]%p
        v[-1]=pow(raw[0][0],-1,p)
        w=[raw[t][j]*v[c[j-1]]*pow(v[c[j]],-1,p)%p for t,c in enumerate(cycles) for j in range(n)]
    gs=[cycle_green(c,w[t*n:(t+1)*n],p) for t,c in enumerate(cycles)]
    M=[[sum(g[i][j] for g in gs)%p for j in range(n)] for i in range(n)]
    assert all(x for row in M for x in row)
    assert rankdet(M,p)[0]==n
    k=4 if rec['family']=='two_phase' else n-1
    J=[]
    for j in range(1,k+1):
        row=[]
        for e in range(n-1,s*n):
            t,b=divmod(e,n);g=gs[t];u=cycles[t][b-1];v=cycles[t][b]
            z=0
            for r,c,sgn in [(0,j,1),(1,0,1),(1,j,-1),(0,0,-1)]:
                z+=sgn*g[r][v]*g[u][c]*pow(M[r][c],-1,p)
            row.append(z*(ii*w[e] if phase else 1)%p)
        J.append(row)
    return J

def phase_controls():
    src=json.loads((BASE/'phase41_supplement/FRESH_JACOBIAN_RESULTS.json').read_text())
    rows=[]
    for r in src['records']:
        p=r['prime'];J=geometric_jacobian(r)
        if 'gaussian_ab' in r:
            Jc=geometric_jacobian(r,-1);ii=pow(3 if p==998244353 else 31,(p-1)//4,p)
            re=[[(a+b)*pow(2,-1,p)%p for a,b in zip(x,y)] for x,y in zip(J,Jc)]
            im=[[(a-b)*pow(2*ii,-1,p)%p for a,b in zip(x,y)] for x,y in zip(J,Jc)]
            J=re+im;assert J==r['real_log_jacobian']
        else:assert J==r['log_jacobian']
        rank=rankdet(J,p)[0];assert rank==r['rank']
        rr=r.get('minor_rows',range(len(J)));cc=r['minor_columns']
        d=rankdet([[J[i][j] for j in cc] for i in rr],p)[1]
        assert d==r['minor_determinant'] and d
        rows.append(dict(family=r['family'],N=r['N'],prime=p,rank=rank,determinant=d,full_jacobian_equal=True))
        print('Phase41',r['family'],r['N'],p,rank,flush=True)
    return rows

def twirl_controls():
    p=97;gen=5;records=[];singular=0;weighted=0
    for n in [1,2,3,4,6,8,12]:
      om=pow(gen,96//n,p)
      for k in range(1,n+1):
       if n%k:continue
       q=pow(om,n//k,p)
       for a,b in [(0,0),(0,1),(1,0),(1,1),(2,1),(2,3),(5,7),(96,2)]:
        delta=(pow((1-pow(b,k,p))%p,n//k,p)-pow(a,n,p))%p
        gs=[]
        for j in range(k):
            Q=eye(n)
            for i in range(n):
                Q[i][i]=(Q[i][i]-b*pow(q,i+j,p))%p
                Q[i][(i-1)%n]=(Q[i][(i-1)%n]-a)%p
            g=inv(Q,p);assert (g is not None)==bool(delta)
            if g:gs.append(g)
        if not delta:singular+=1;continue
        S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
        Sk=mp(S,k,p);d=(1-pow(b,k,p))%p;c=pow(a,k,p)
        D=[[(d*int(i==j)-c*Sk[i][j])%p for j in range(n)] for i in range(n)]
        Di=inv(D,p);assert Di
        P=[[0]*n for _ in range(n)]
        for r in range(k):
            for i in range(n):P[i][(i-r)%n]=(P[i][(i-r)%n]+pow(a,r,p))%p
        avg=[[sum(g[i][j] for g in gs)*pow(k,-1,p)%p for j in range(n)] for i in range(n)]
        assert avg==mm(Di,P,p)
        rank=rankdet(avg,p)[0];assert rank==(n-k+1 if pow(a,n,p)==1 else n)
        x=[(j*j+3*j+7)%p for j in range(n)]
        z=[sum(pow(a,r,p)*x[(-r)%n] for r in range(k))%p]
        for i in range(1,n):z.append((a*z[-1]+x[i]-c*x[(i-k)%n])%p)
        assert z==mv(P,x,p)
        y=[0]*n
        if d==0:
            for i in range(n):y[i]=-z[(i+k)%n]*pow(c,-1,p)%p
        else:
            ratio=c*pow(d,-1,p)%p;m=n//k
            for residue in range(k):
                seq=[residue+t*k for t in range(m)];w=0
                for ix in seq:w=(ratio*w+z[ix]*pow(d,-1,p))%p
                prev=w*pow((1-pow(ratio,m,p))%p,-1,p)%p
                for ix in seq:prev=(ratio*prev+z[ix]*pow(d,-1,p))%p;y[ix]=prev
        assert y==mv(avg,x,p)
        for ell in range(k):
            sec=[[sum(pow(q,(-j*ell)%k,p)*g[i][v] for j,g in enumerate(gs))*pow(k,-1,p)%p for v in range(n)] for i in range(n)]
            Pq=[[0]*n for _ in range(n)]
            for r in range(k-ell):
                gb=1
                for v in range(1,ell+1):gb=gb*(1-pow(q,r+v,p))*pow((1-pow(q,v,p))%p,-1,p)%p
                for i in range(n):
                    v=(i-r)%n;Pq[i][v]=(Pq[i][v]+pow(b,ell,p)*pow(a,r,p)*gb*pow(q,v*ell,p))%p
            assert sec==mm(Di,Pq,p);weighted+=1
        F=[[pow(om,(-i*j)%n,p) for j in range(n)] for i in range(n)]
        FS=mm(F,Sk,p);SF=mm(Sk,F,p)
        assert rankdet([[(u-v)%p for u,v in zip(x,y)] for x,y in zip(FS,SF)],p)[0]==(n-k if (n-k)%2==0 else n)
        records.append(dict(N=n,K=k,alpha=a,beta=b,rank=rank,d_zero=d==0,all_sectors_checked=True))
    return dict(prime=p,records=records,singular_parameter_cases=singular,weighted_sectors=weighted)

if __name__=='__main__':
    result={'policy':'Only independently authored control functions executed; supplied JSON data read; no supplied program executed/imported/AST-parsed.',
            'phase41':phase_controls(),'magnetic_twirl':twirl_controls()}
    (OUT/'reviewer_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('DONE',len(result['phase41']),len(result['magnetic_twirl']['records']),flush=True)
