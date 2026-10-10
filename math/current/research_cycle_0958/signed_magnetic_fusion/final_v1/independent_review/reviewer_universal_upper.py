"""Independent direct-resolvent verification of the 4N-bank spanning construction."""
import itertools,json
from pathlib import Path
from reviewer_matrix_helper import inv,eye

records=[]
for n,p,q in [(3,7,2),(5,11,3),(7,29,7),(9,19,4)]:
    signs=list(itertools.product([1,-1],repeat=2));iv=pow(n,-1,p)
    for mode in ['arbitrary','fourier']:
        C=[[((a*a+3*b+a*b+1)%p) for b in range(n)] for a in range(n)]
        F=[[pow(q,(-i*j)%n,p) for j in range(n)] for i in range(n)]
        if mode=='fourier':C=[[sum(pow(q,(-b*i)%n,p)*F[(i+a)%n][i] for i in range(n))*iv%p for b in range(n)] for a in range(n)]
        assigned={s:[[0]*n for _ in range(n)] for s in signs}
        for a in range(n):
            for b in range(n):
                s=next((e,d) for e,d in signs if (e*a)%n+(d*b)%n<n)
                assigned[s][(s[0]*a)%n][(s[1]*b)%n]=C[a][b]
        target=[[0]*n for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for v in range(n):target[(v+a)%n][v]=(target[(v+a)%n][v]+C[a][b]*pow(q,b*v,p))%p
        total=[[0]*n for _ in range(n)];nonzero_banks=0;inverses=0
        for e,d in signs:
            zeta=pow(q,(e*d)%n,p);h=[[0]*n for _ in range(n)]
            for ell in range(n):
                t=[0]*n
                for r in range(n-ell):
                    gb=1
                    for s in range(1,ell+1):gb=gb*(1-pow(zeta,r+s,p))*pow((1-pow(zeta,s,p))%p,-1,p)%p
                    assert gb;t[r]=assigned[e,d][r][ell]*pow(gb,-1,p)%p
                for k in range(n):h[k][ell]=sum(t[r]*pow(q,(-k*r)%n,p) for r in range(n))*iv%p
            for k in range(n):
                alpha=pow(q,k,p);weights=[-sum(h[k][ell]*pow(zeta,(-j*ell)%n,p) for ell in range(n))%p for j in range(n)]
                nonzero_banks+=bool(any(weights))
                for j,w in enumerate(weights):
                    Q=eye(n)
                    for i in range(n):
                        Q[i][i]=(Q[i][i]-pow(zeta,j,p)*pow(q,(d*i)%n,p))%p
                        Q[i][(i-e)%n]=(Q[i][(i-e)%n]-alpha)%p
                    G=inv(Q,p);assert G;inverses+=1
                    xx=[(v*v+v+1)%p for v in range(n)];yy=[0]*n;i0=(-e*j)%n;ia=pow(alpha,-1,p)
                    yy[(i0-e)%n]=-xx[i0]*ia%p
                    for step in range(1,n):
                        i=(i0-step*e)%n;di=(1-pow(zeta,j,p)*pow(q,(d*i)%n,p))%p
                        yy[(i-e)%n]=(di*yy[i]-xx[i])*ia%p
                    assert yy==[sum(a*b for a,b in zip(row,xx))%p for row in G]
                    for i in range(n):
                        for v in range(n):total[i][v]=(total[i][v]+w*G[i][v]*iv)%p
        assert total==target
        if mode=='fourier':assert target==F
        records.append({'N':n,'p':p,'mode':mode,'banks_available':4*n,'nonzero_banks':nonzero_banks,'original_inverses_checked':inverses,'backward_solvers_checked':inverses,'all_matrix_entries_equal':True})
Path(__file__).with_name('reviewer_universal_upper_results.json').write_text(json.dumps(records,indent=2)+'\n');print('DONE',len(records))
