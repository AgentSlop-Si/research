"""Fresh exact controls for the bounded ALG047 primary-source comparison.
No repository or uploaded research program is imported or executed.
"""
import json
from pathlib import Path

def rank(a,p):
    a=[row[:] for row in a]; r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]%p),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        z=pow(a[r][c]%p,-1,p);a[r]=[(x*z)%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                z=a[i][c];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[r])]
        r+=1
    return r

def root(N,p):
    return next(w for w in range(2,p) if pow(w,N,p)==1 and all(pow(w,j,p)!=1 for j in range(1,N)))

def run(N,p):
    w=root(N,p);inv2=pow(2,-1,N);inv4=pow(4,-1,N)
    W=lambda a:pow(w,a%N,p)
    gamma=sum(W(j*j) for j in range(N))*pow(N,-1,p)%p
    assert gamma
    dirs=[(a,b) for a in range(N) for b in range(N) if (a,b)!=(0,0)]
    coefficient_checks=cocycle_checks=pair_checks=compatible=reversal_checks=0
    # Every source Heisenberg operator pi(-a,b) matches the repository D_(a,b).
    for a,b in [(0,0)]+dirs:
        for j in range(N):
            i=(j+a)%N
            source_exponent=(-a)*b*inv2+b*i # pi(t,b)f(i)=psi(tb/2+bi)f(i+t)
            repo_exponent=a*b*inv2+b*j
            assert W(source_exponent)==W(repo_exponent)
        direct=sum(W(j*j+(a-b)*j-a*b*inv2) for j in range(N))*pow(N,-1,p)%p
        assert direct==gamma*W(-(a*a+b*b)*inv4)%p
        coefficient_checks+=1
    # The product action on each basis vector is independently compared.
    for a,b in dirs:
        for c,d in dirs:
            sigma=(b*c-a*d)%N
            for j in range(N):
                left=c*d*inv2+d*j+a*b*inv2+b*(j+c)
                right=(a+c)*(b+d)*inv2+(b+d)*j+sigma*inv2
                assert W(left)==W(right)
            cocycle_checks+=1
            if (a*d-b*c)%N==0:continue
            kappa=(a*c+b*d+sigma)%N
            tensor=[[gamma*W(-((m*a+n*c)**2+(m*b+n*d)**2)*inv4-sigma*m*n*inv2)%p for n in range(N)]for m in range(N)]
            separated=[[gamma*W(-(a*a+b*b)*m*m*inv4-(c*c+d*d)*n*n*inv4-kappa*m*n*inv2)%p for n in range(N)]for m in range(N)]
            assert tensor==separated
            assert rank(tensor,p)==(1 if kappa==0 else N)
            pair_checks+=1
            if kappa==0:
                compatible+=1
                assert (a*a+b*b)%N and (c*c+d*d)%N
                krev=(a*c+b*d-sigma)%N
                assert krev==(-2*sigma)%N and krev
                reversal_checks+=1
    return dict(N=N,coefficient_field=p,omega=w,weyl_coefficient_checks=coefficient_checks,cocycle_pairs=cocycle_checks,independent_ordered_pairs=pair_checks,compatible_pairs=compatible,reversal_checks=reversal_checks)

def main():
    results=[run(N,p) for N,p in [(3,7),(5,11),(7,29)]]
    # Composite-size guard: independent directions but nonzero nonunit kappa.
    N,p=9,19;w=root(N,p);kappa=3;half=pow(2,-1,N)
    c=[[pow(w,(-kappa*m*n*half)%N,p) for n in range(N)]for m in range(N)]
    assert rank(c,p)==3
    # Complex scalar check for standard-character source normalization.
    import cmath,math
    scalar=[]
    for N in [3,5,7,11,13,17,19]:
        G=sum(cmath.exp(2j*math.pi*j*j/N)for j in range(N))
        chi=pow((-2)%N,(N-1)//2,N);chi=-1 if chi==N-1 else chi
        C=1j**((N-1)//2)*math.sqrt(N)
        assert abs(G-C*chi)<1e-10
        scalar.append(N)
    output={'status':'PASS','scope':'Fresh finite controls corroborate convention and bounded derivation; they do not replace symbolic proofs.','prime_cases':results,'total_independent_ordered_pairs':sum(x['independent_ordered_pairs']for x in results),'total_compatible_pairs':sum(x['compatible_pairs']for x in results),'composite_negative_control':{'N':9,'coefficient_field':19,'u':[1,0],'v':[4,1],'determinant':1,'kappa':3,'rank':3},'complex_standard_character_scalar_check_primes':scalar,'complex_scalar_tolerance':1e-10,'repository_programs_executed':False}
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
