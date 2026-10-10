"""Fresh sign/gcd/phase-table numerical controls. Proofs do not depend on floats."""
import cmath,math,json
from pathlib import Path
out=Path(__file__).resolve().parent

def jacobi(a,n):
    a%=n;result=1
    while a:
        while a%2==0:
            a//=2
            if n%8 in (3,5):result=-result
        a,n=n,a
        if a%4==n%4==3:result=-result
        a%=n
    return result if n==1 else 0
worst=0;worst_inv=0;tests=0
for n in range(3,46,2):
    for a in range(1,n):
        if math.gcd(a,n)!=1:continue
        b=5%n;c=7%n;w=cmath.exp(2j*math.pi/n)
        g=(1 if n%4==1 else 1j)*jacobi(a,n)*math.sqrt(n)
        inv4a=pow(4*a,-1,n)
        for k in range(n):
            direct=sum(w**((a*j*j+b*j+c-k*j)%n) for j in range(n))
            pred=g*w**((c-inv4a*(b-k)**2)%n)
            worst=max(worst,abs(pred-direct))
            # Explicit reciprocal formula, avoiding the formerly reversed phase.
            reciprocal=g.conjugate()/n*w**((inv4a*(b-k)**2-c)%n)
            worst_inv=max(worst_inv,abs(reciprocal-1/direct))
            tests+=1
assert worst<1e-11 and worst_inv<1e-11
# Nonunit chirp slopes must have zero Fourier values outside the residue class.
zeros=0
for n,a,b in [(9,3,1),(15,5,2),(21,7,3),(45,15,4)]:
    d=math.gcd(a,n);w=cmath.exp(2j*math.pi/n)
    for k in range(n):
        direct=sum(w**((a*j*j+(b-k)*j)%n) for j in range(n))
        if (b-k)%d:
            assert abs(direct)<1e-11;zeros+=1
        else:assert abs(abs(direct)-math.sqrt(n*d))<1e-11
r={'evidence_kind':'fresh binary64 sign and normalization checks, not proof of interval certification','full_chirp_frequency_checks':tests,'max_gauss_formula_residual':worst,'max_reciprocal_formula_residual':worst_inv,'singular_chirp_zero_checks':zeros}
(out/'fresh_chirp_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
