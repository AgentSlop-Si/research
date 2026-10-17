"""Fresh independent arithmetic and proof-identity controls. No historical code imported."""
import json, cmath, itertools, math
from pathlib import Path

def mul(A,B,p):
    return [[sum(x*y for x,y in zip(a,b))%p for b in zip(*B)] for a in A]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def primitive(p,n):
    return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)))
def algebra_controls():
    counts={'legal_green_inverse_cases':0,'fourier_inverse_cases':0,'n2_exception_factorizations':0,'metric_projection_diagnostics':0}
    for p in (5,7,13,17,31,97):
        for n in range(1,min(25,p)):
            if (p-1)%n: continue
            w=primitive(p,n)
            F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
            Fi=[[pow(n,-1,p)*pow(w,(-i*j)%n,p)%p for j in range(n)] for i in range(n)]
            assert mul(F,Fi,p)==eye(n) and all(z for row in Fi for z in row)
            counts['fourier_inverse_cases']+=1
            for a in range(p):
                if pow(a,n,p)==1: continue
                A=[[(int(i==j)-a*int(i==(j+1)%n))%p for j in range(n)] for i in range(n)]
                G=[[pow(a,(i-j)%n,p)*pow((1-pow(a,n,p))%p,-1,p)%p for j in range(n)] for i in range(n)]
                assert mul(A,G,p)==eye(n)
                assert all(sum(z!=0 for z in row)<=2 for row in A)
                if n>=3: assert any(z==0 for row in A for z in row)
                counts['legal_green_inverse_cases']+=1
                if n==2 and a*a%p==p-1:
                    # Diagonal factorization (1-a^2)^-1 diag(1,a) F2 diag(1,a).
                    d=pow((1-a*a)%p,-1,p)
                    assert G==[[d,d*a%p],[d*a%p,(-d*a*a)%p]]
                    counts['n2_exception_factorizations']+=1
    for n in range(3,17):
        for supp in itertools.combinations(range(n),2):
            for coeff in itertools.product((1,-1,2,1j),repeat=2):
                b=[0j]*n
                for j,z in zip(supp,coeff): b[j]=z
                norm2=sum(abs(z)**2 for z in b)
                v=[sum(b[j]*cmath.exp(2j*math.pi*j*k/n) for j in range(n))/math.sqrt(n) for k in range(n)]
                for i in range(n):
                    leak=sum(abs(v[k])**2 for k in range(n) if k!=i)
                    assert leak+1e-10 >= norm2*(1-2/n)
                    counts['metric_projection_diagnostics']+=1
    count=0
    for n in (4,8,16):
        H=[[(-1)**((i&j).bit_count()) for j in range(n)] for i in range(n)]
        for j,k in itertools.combinations(range(n),2):
            for a,b in itertools.product((-2,-1,1,2),repeat=2):
                v=[a*H[j][t]+b*H[k][t] for t in range(n)];norm=a*a+b*b
                for i in range(n):
                    assert sum(z*z for t,z in enumerate(v) if t!=i)>=(n-2)*norm
                    count+=1
    counts['exact_walsh_energy_checks']=count
    return counts
if __name__=='__main__':
    out={'algebra':algebra_controls(),'qualification':'Fresh exact modular, exact integer Walsh-energy, and separately labelled floating Fourier diagnostics corroborate the written proofs; no historical replay.'}
    Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
