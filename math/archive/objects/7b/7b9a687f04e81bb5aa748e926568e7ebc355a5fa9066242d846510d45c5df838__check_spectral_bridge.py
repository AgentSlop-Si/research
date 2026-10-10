"""Exact tests for half-grid spectral extension over a prime field."""
import json, random
from check_displacement import rank
from pathlib import Path
P=97

def evaluate(a,x):
    y=0
    for c in reversed(a): y=(y*x+c)%P
    return y

def matvec(E,v): return [sum(a*b for a,b in zip(row,v))%P for row in E]

def main():
    rng=random.Random(20261009); reports=[]
    for L in [1,2,4,8,16]:
        alpha=next(a for a in range(1,P) if pow(a,L,P)==P-1 and pow(a,2*L,P)==1)
        omega=alpha*alpha%P
        E=[[2*pow(L*(1-alpha*pow(omega,(r-s)%L,P))%P,-1,P)%P
            for s in range(L)] for r in range(L)]
        for s in range(L):
            v=[int(j==s) for j in range(L)]
            twice=matvec(E,matvec(E,v))
            assert twice==v[1:]+v[:1]
        for k in range(1,L+1):
            for _ in range(10):
                q=[rng.randrange(P) for _ in range(k)]+[rng.randrange(1,P)]
                de=[evaluate(q,pow(omega,r,P)) for r in range(L)]
                do=[evaluate(q,alpha*pow(omega,r,P)%P) for r in range(L)]
                defect=[[(E[r][s]*(de[s]-do[r]))%P for s in range(L)] for r in range(L)]
                assert rank(defect,P)==k
                # Restrict input to degree<k polynomials: x=F[:,0:k] coeffs.
                restricted=[[sum(defect[r][s]*pow(omega,s*j,P) for s in range(L))%P
                             for j in range(k)] for r in range(L)]
                assert rank(restricted,P)==max(0,2*k-L)
        for _ in range(100):
            a=[rng.randrange(P) for _ in range(L)]
            v=[evaluate(a,pow(omega,r,P)) for r in range(L)]
            assert matvec(E,v)==[evaluate(a,alpha*pow(omega,r,P)%P) for r in range(L)]
            # A product H of degree <2L splits H(x)=He(x^2)+x Ho(x^2).
            h=[rng.randrange(P) for _ in range(2*L)]
            for r in range(L):
                x=pow(alpha,r,P); hp=evaluate(h,x); hm=evaluate(h,-x%P)
                ev=(hp+hm)*pow(2,-1,P)%P
                od=(hp-hm)*pow(2*x,-1,P)%P
                assert ev==evaluate(h[::2],pow(omega,r,P))
                assert od==evaluate(h[1::2],pow(omega,r,P))
        reports.append(dict(L=L,alpha=alpha,random_polynomials=100,squared_operator_columns=L,commutation_rank_checks=10*L,restricted_rank_checks=10*L))
    result=dict(status='passed',field_prime=P,tests=reports,
                limitation='Exact small finite-field checks; no FFT runtime or numerical-stability benchmark.')
    Path(__file__).with_name('spectral_bridge_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
