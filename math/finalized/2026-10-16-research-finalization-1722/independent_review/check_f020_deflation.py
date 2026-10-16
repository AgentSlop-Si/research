"""Review-authored SymPy controls, independent of the author's bit-polynomial code.
Only the pre-existing m=1,2,3,4,12 coefficient controls; no support census.
"""
import json
import sympy as s
q,X=s.symbols('q X')
R=s.GF(2).poly_ring(q)
previous=s.Poly(1,X,domain=R)
current=s.Poly(X+q+q*q,X,domain=R)

def valuation(poly,f):
    v=0
    while True:
        quotient,remainder=poly.div(f)
        if not remainder.is_zero:return v
        poly=quotient; v+=1

out=[]
for m in range(1,13):
    if m>=2:
        previous,current=current,s.Poly((X+q**(2*m-1)*(1+q))*current.as_expr()
            +(1+q**(2*m-1))*(1+q**(2*m-2))*previous.as_expr(),X,domain=R)
    if m not in (1,2,3,4,12):continue
    cs=list(reversed(current.all_coeffs()))
    A=s.Poly(sum(cs[j]*X**(j//2) for j in range(0,len(cs),2)),X,domain=R)
    B=s.Poly(sum(cs[j]*X**(j//2) for j in range(1,len(cs),2)),X,domain=R)
    endpoint=s.Poly(cs[0],q,modulus=2)
    resultant=s.Poly(s.resultant(A,B),q,modulus=2)
    product=endpoint*resultant
    N=m*(m+1)*(2*m+1)//3
    v=(m+1)//2; kappa=m+3*(m*m//4)+2*(m//4)
    denominator=s.Poly(q**v*(q+1)**kappa,q,modulus=2)
    local=[];delta=0
    for d in range(3,m+1,2):
        k=m//d;rho=(d-1)//2*k+k//2;exponent=k+rho
        cyclotomic=s.Poly(s.cyclotomic_poly(d,q),q,modulus=2)
        ev=valuation(endpoint,cyclotomic);rv=valuation(resultant,cyclotomic)
        assert ev>=k and rv>=rho
        if m%d==0:assert ev==k
        denominator*=cyclotomic**exponent
        delta+=cyclotomic.degree()*exponent
        local.append({'d':d,'endpoint_valuation':ev,'resultant_valuation':rv,
            'endpoint_required':k,'resultant_required':rho})
    quotient,remainder=product.div(denominator)
    assert remainder.is_zero and product.degree()==N
    assert quotient.degree()==N-v-kappa-delta
    out.append({'m':m,'degree':N,'new_degree_bound':quotient.degree(),
        'extra_removed_degree':delta,'local':local})
print(json.dumps({'result':'PASS','symbolic_engine':s.__version__,'controls':out},indent=2))
