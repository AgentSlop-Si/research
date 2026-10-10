"""Fresh symbolic controls for ordinary discriminants and cyclotomic orders.

Uses installed SymPy only. No supplied or predecessor Python is imported,
executed, or compiled. Reciprocal contraction cuts large determinant degrees;
the contraction is cross-checked against direct ordinary discriminants.
"""
from pathlib import Path
from math import prod
import json
import sympy as S

OUT=Path(__file__).resolve().parent
q,z,y=S.symbols('q z y')

def H(n):
    # Direct Gaussian product formula with exact polynomial division, rather
    # than q-Pascal or the three-term recurrence used by other controls.
    coefficients=[]
    for k in range(n+1):
        num=S.Poly(1,q); den=S.Poly(1,q)
        for j in range(1,k+1):
            num*=S.Poly(1-q**(n-k+j),q); den*=S.Poly(1-q**j,q)
        coefficients.append(num.exquo(den).as_expr())
    return S.Poly(sum(v*z**k for k,v in enumerate(coefficients)),z)

def reciprocal_disc(poly):
    n=poly.degree()
    odd_factor=S.Integer(1)
    if n%2:
        poly=poly.exquo(S.Poly(z+1,z))
        odd_factor=poly.eval(-1)**2
    r=poly.degree()//2
    if not r: return S.Poly(odd_factor,q)
    cheb=[S.Integer(2),y]
    for j in range(2,r+1): cheb.append(S.expand(y*cheb[-1]-cheb[-2]))
    P=S.Poly(poly.nth(r)+sum(poly.nth(r+j)*cheb[j] for j in range(1,r+1)),y)
    contracted=S.discriminant(P.as_expr(),y)
    return S.Poly(S.expand(odd_factor*P.eval(2)*P.eval(-2)*contracted**2),q,domain=S.ZZ)

def reduce_q(expr,cyclo): return S.Poly(expr,q).rem(cyclo)

def main():
    polys={}; discs={}; checks=[]
    for n in (1,2,3,4,5,6,7,9,10,12):
        print('Computing exact ordinary discriminant, degree',n,flush=True)
        hn=H(n); dn=reciprocal_disc(hn)
        polys[n]=hn; discs[n]=dn
        if n<=7:
            direct=S.Poly(S.discriminant(hn.as_expr(),z),q)
            assert direct==dn
        checks.append({'n':n,'degree_in_q':dn.degree(),
                       'direct_discriminant_crosscheck':n<=7,
                       'disc_method':'reciprocal quadratic-product identity'})
    results={'software':{'sympy':S.__version__},'discriminant_construction':checks}
    results['separated_exact_leading_checks']=[]
    for d,A,b in ((1,5,0),(3,2,0),(3,3,0),(5,1,2),(5,2,2)):
        n=d*A+b; print('Checking exact valuation/coefficient',(d,A,b),flush=True)
        cyclo=S.Poly(S.cyclotomic_poly(d,q),q)
        quotient=discs[n]; order=0
        while quotient.rem(cyclo).is_zero:
            quotient=quotient.exquo(cyclo); order+=1
        K=d*A*(A-1)//2; assert order==K
        Q=S.Poly(q**d-1,q).exquo(cyclo)
        g=H(b); delta=S.Integer(1) if b<2 else S.discriminant(g.as_expr(),z)
        resultant=S.resultant(z**d+1,g.as_expr(),z)
        PA=prod(j**j for j in range(1,A+1))
        coefficient=((-1)**(A*(d-1)//2)*d**(d*A*(A+1)//2)*PA**d
                     *delta*resultant**(2*A))
        normalized=reduce_q(coefficient,cyclo)
        leading=reduce_q(Q.as_expr()**K*normalized.as_expr(),cyclo)
        actual=quotient.rem(cyclo)
        assert leading==actual and not actual.is_zero
        # The exact quotient has integer coefficients, not merely rational.
        quotient=S.Poly(quotient,q,domain=S.ZZ)
        results['separated_exact_leading_checks'].append({
            'd':d,'A':A,'b':b,'n':n,'exact_Phi_order':order,
            'integer_quotient_degree':quotient.degree(),
            'C_remainder':str(normalized.as_expr()),
            'E_remainder':str(actual.as_expr()),
            'Q_power_normalization_verified':True})
    results['intrinsic_overlap_controls']=[]
    for A,n,expected in ((2,7,5),(3,10,12)):
        cyclo=S.Poly(q*q+q+1,q); quotient=discs[n]; order=0
        while quotient.rem(cyclo).is_zero:
            quotient=quotient.exquo(cyclo); order+=1
        assert order==expected
        results['intrinsic_overlap_controls'].append({'d':3,'b':1,'A':A,'n':n,
          'actual_order':order,'separated_formula_would_give':3*A*(A-1)//2,
          'first_nonzero_quotient_remainder':str(quotient.rem(cyclo).as_expr())})
    # Independently duplicate all fixed-base numbers with direct symbolic
    # resultants over Z[q], rather than the norm-field determinant code.
    standard=json.loads((OUT/'EXACT_ARITHMETIC_RESULTS.json').read_text())
    results['fixed_base_second_method']=[]
    for d in (5,9,13):
        print('Crosschecking fixed-base resultants over Z[q]',d,flush=True)
        b=(d-1)//2; g=H(b); cyclo=S.Poly(S.cyclotomic_poly(d,q),q)
        delta=reduce_q(S.discriminant(g.as_expr(),z),cyclo)
        result=reduce_q(S.resultant(z**d+1,g.as_expr(),z),cyclo)
        B=(delta*result).rem(cyclo)
        expected=next(x for x in standard['fixed_bases'] if x['d']==d)
        asc=lambda p:[int(p.nth(i)) for i in range(p.degree()+1)]
        assert asc(delta)==expected['discriminant_remainder_ascending']
        assert asc(result)==expected['resultant_remainder_ascending']
        assert asc(B)==expected['product_remainder_ascending']
        assert int(B.content())==expected['content']
        results['fixed_base_second_method'].append({'d':d,
            'discriminant_remainder':str(delta.as_expr()),
            'resultant_remainder':str(result.as_expr()),
            'product_remainder':str(B.as_expr()),
            'content':int(B.content()),'agreement_with_standard_library_norm_method':True})
    results['complete_discriminants_small']={str(n):str(S.factor(discs[n].as_expr())) for n in (2,3,4,5,6,7)}
    (OUT/'DISCRIMINANT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print('All symbolic exact discriminant controls passed.',flush=True)

if __name__=='__main__': main()
