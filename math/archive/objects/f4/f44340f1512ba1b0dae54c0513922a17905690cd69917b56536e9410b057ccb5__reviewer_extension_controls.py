"""New controls for weighted magnetic support and scalar-normalized projection."""
import json
from pathlib import Path
from reviewer_controls import eye,inv,rankdet

def main():
    p=181;primitive=2
    assert len({pow(primitive,j,p) for j in range(p-1)})==p-1
    out=[]
    for n in [3,5,9,15]:
        om=pow(primitive,(p-1)//n,p)
        F=[[pow(om,(-i*j)%n,p) for j in range(n)] for i in range(n)]
        coeff=lambda A,a,b:sum(pow(om,(-b*i)%n,p)*A[(i+a)%n][i] for i in range(n))*pow(n,-1,p)%p
        assert all(coeff(F,a,b) for a in range(n) for b in range(n))
        for k in range(1,n+1):
            if n%k:continue
            m=n//k;q=pow(om,m,p);alpha=2
            beta=next(b for b in range(2,p) if (pow((1-pow(b,k,p))%p,m,p)-pow(alpha,n,p))%p)
            gs=[]
            for j in range(k):
                Q=eye(n)
                for i in range(n):Q[i][i]=(Q[i][i]-beta*pow(q,i+j,p))%p;Q[i][(i-1)%n]=(Q[i][(i-1)%n]-alpha)%p
                G=inv(Q,p);assert G;gs.append(G)
            # A deliberately nontrivial linear combination of every original branch.
            A=[[sum((j*j+2*j+3)*G[i][v] for j,G in enumerate(gs))%p for v in range(n)] for i in range(n)]
            allowed={(a,m*ell) for ell in range(k) for a in range(n) if a%k+ell<=k-1}
            actual={(a,b) for a in range(n) for b in range(n) if coeff(A,a,b)}
            assert actual<=allowed and len(allowed)==n*(k+1)//2<n*n
            out.append({'N':n,'K':k,'allowed_support':len(allowed),'actual_support':len(actual),'all_fourier_coefficients_nonzero':True})
    A=[[2,2,2],[2,-1,-1],[2,-1,-1]]
    assert rankdet(A,998244353)[0]==2
    r={'odd_composite_orbit_support':out,'scaled_C3_rank_two':True}
    Path(__file__).with_name('reviewer_extension_results.json').write_text(json.dumps(r,indent=2)+'\n')
    print(r)

if __name__=='__main__':main()
