"""Fresh bounded transcription controls; no historical code imported or run."""
import json
from pathlib import Path
import sympy as s

q, w, z = s.symbols('q w z')
limit = 5
C = [s.Integer(1), w - 2 + q + q**2]
beta = lambda j: (1-q**(2*j))*(1-q**(2*j+1))
for k in range(1,limit):
    C.append(s.expand((w-2+q**(2*k+1)+q**(2*k+2))*C[k]-beta(k)*C[k-1]))
H = [s.Integer(1), 1+z]
for n in range(1,2*limit+1):
    H.append(s.expand((1+z)*H[n]-z*(1-q**n)*H[n-1]))
results = []
for m in range(1,limit+1):
    lifted = s.expand(z**m*(z+1)*C[m].subs(w,z+2+1/z))
    assert s.expand(H[2*m+1]-lifted) == 0
    K = s.Integer(0)
    for k in range(m):
        K += C[k]**2*s.prod(beta(j) for j in range(k+1,m))
    W = s.diff(C[m],w)*C[m-1]-C[m]*s.diff(C[m-1],w)
    assert s.expand(W-K) == 0
    record={'m':m,'odd_RS_contraction':True,'ordinary_derivative_kernel':True}
    if m <= 3:
        prefactor=s.prod(beta(j)**j for j in range(1,m))
        assert s.expand(s.resultant(C[m],s.expand(K),w)-s.discriminant(C[m],w)*prefactor) == 0
        record['exact_resultant_discriminant_identity']=True
    results.append(record)
receipt={'scope':'Five symbolic transcription controls only; no root-order or layer census, not a proof of uniform noncancellation.', 'results':results,'supplied_programs_executed':0}
integer_checks=[]
for e in range(1,7):
    def v5(n):
        exponent=0
        while n%5 == 0:
            n//=5
            exponent+=1
        return exponent
    a=(5**e-1)//2
    direct=sum((27*k//2)*5**v5(k) for k in range(1,a+1))
    numerator=(216*e+45)*25**e-16*e*5**e-45
    assert numerator%160 == 0 and direct == numerator//160
    integer_checks.append({'e':e,'known_prefactor_valuation':direct,'closed_expression_matches':True})
receipt['integer_valuation_identity_controls']=integer_checks
out=Path(__file__).with_name('BOUNDED_CHECKS.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
