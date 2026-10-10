"""Fresh exact fixed-base experiment; no predecessor code imported.
Testing the specific prime-support conjecture for c_d at d=17,21,25.
"""
from sympy import QQ, Poly, cyclotomic_poly, symbols, factorint
from sympy.polys.rings import ring
from functools import reduce
from math import gcd
from time import perf_counter
import json, hashlib, pathlib
OUT=pathlib.Path(__file__).resolve().parent
q=symbols('q')

def coefficients(a):
    result=[]
    for t in reversed(a.to_list()):
        assert t.denominator==1
        result.append(int(t))
    return result or [0]

def run(d):
    t=perf_counter(); b=(d-1)//2; r=b//2
    K=QQ.alg_field_from_poly(Poly(cyclotomic_poly(d,q),q),'w')
    w=K.unit; R,z=ring('z',K)
    prev,cur=R.one,z+1
    for n in range(2,b+1):
        prev,cur=cur,(z+1)*cur+(w**(n-1)-1)*z*prev
    G=cur
    # Independently build Gaussian row by Pascal, then compare.
    row=[K.one]
    for n in range(1,b+1):
        row=[(row[k-1] if k else K.zero)+(w**k*row[k] if k<n else K.zero) for k in range(n+1)]
    assert G==sum((row[k]*z**k for k in range(b+1)),R.zero)
    assert all(row[k]==row[b-k] for k in range(b+1))
    # G=z^r P(z+1/z); Chebyshev-like Laurent contraction S_j.
    U,u=ring('u',K)
    C=[U(2),u]
    for j in range(2,r+1): C.append(u*C[-1]-C[-2])
    P=U(row[r])+sum((row[r+j]*C[j] for j in range(1,r+1)),U.zero)
    dp=P.discriminant()
    plus=P.evaluate(0,K(2)); minus=P.evaluate(0,K(-2))
    delta=plus*minus*dp**2
    # ∏ at all d roots of z^d+1, no large Sylvester determinant.
    res=K.one
    for j in range(d): res*=G.evaluate(0,-w**j)
    B=delta*res; coeff=coefficients(B); content=reduce(gcd,map(abs,coeff))
    data={'d':d,'b':b,'degree_P':r,'B_coefficients_ascending':coeff,
       'content':str(content),'content_factorization':{str(k):int(v) for k,v in factorint(content).items()},
       'discriminant_coefficients_ascending':coefficients(delta),
       'cluster_resultant_coefficients_ascending':coefficients(res),
       'P_discriminant_coefficients_ascending':coefficients(dp),
       'H_plus_one_coefficients_ascending':coefficients(plus),
       'H_minus_one_signed_coefficients_ascending':coefficients(minus),
       'elapsed_seconds':perf_counter()-t}
    (OUT/f'base_{d}.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ['d','content','content_factorization','elapsed_seconds']}),flush=True)
    return data
if __name__=='__main__':
    import sys
    for d in map(int,sys.argv[1:] or ['17','21','25']):run(d)
