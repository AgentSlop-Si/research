#!/usr/bin/env python3
"""Independent audit arithmetic, authored for this audit.
No supplied or predecessor source is executed, imported, or compiled.
Only Python's standard library is used. Binary-polynomial coefficients are
integers, with bit j denoting the coefficient of q**j. Outer polynomials
are coefficient lists in ascending order. Supplied JSON is read as claims
only after each independent computation has completed.
"""
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
SOURCE=Path('characteristic_two_chirp_guard_0320')

def bm(a,b):
    """Carryless polynomial multiplication over F_2, without reduction."""
    out=0
    while b:
        if b&1: out^=a
        b>>=1; a<<=1
    return out

def bd(a,b):
    assert b
    quotient=0
    while a and a.bit_length()>=b.bit_length():
        shift=a.bit_length()-b.bit_length()
        quotient^=1<<shift; a^=b<<shift
    return quotient,a

def bexact(a,b):
    c,r=bd(a,b)
    assert r==0, ('nonexact ring division',a,b,r)
    return c

def bp(a,e):
    out=1
    while e:
        if e&1: out=bm(out,a)
        a=bm(a,a); e>>=1
    return out

def irreducible(f):
    """Exhaust all possible monic proper factors of degree at most d/2."""
    d=f.bit_length()-1
    if d<1: return False
    for k in range(1,d//2+1):
        for g in range(1<<k,1<<(k+1)):
            if bd(f,g)[1]==0: return False
    return True

def prime_divisors(n):
    out=[]; p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0: n//=p
        p+=1
    if n>1: out.append(n)
    return out

class Field:
    def __init__(self,f):
        assert irreducible(f)
        self.f=f; self.d=f.bit_length()-1
    def mul(self,a,b): return bd(bm(a,b),self.f)[1]
    def pow(self,a,e):
        if e<0: a=self.inv(a); e=-e
        ans=1
        while e:
            if e&1: ans=self.mul(ans,a)
            a=self.mul(a,a); e>>=1
        return ans
    def inv(self,a):
        assert a
        ans=self.pow(a,(1<<self.d)-2)
        assert self.mul(a,ans)==1
        return ans
    def order_is(self,a,n):
        return self.pow(a,n)==1 and all(self.pow(a,n//p)!=1 for p in prime_divisors(n))

def trim(a):
    a=list(a)
    while a and not a[-1]: a.pop()
    return a

def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a): c[i]^=v
    for i,v in enumerate(b): c[i]^=v
    return trim(c)

def scale(a,c,mul): return trim([mul(x,c) for x in a])

def mulp(a,b,mul):
    if not a or not b: return []
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]^=mul(x,y)
    return trim(c)

def deriv(a): return trim([a[j+1] if j%2==0 else 0 for j in range(len(a)-1)])

def pdiv(a,b,F):
    a=trim(a); b=trim(b); assert b
    q=[0]*max(0,len(a)-len(b)+1)
    inv=F.inv(b[-1])
    while len(a)>=len(b):
        k=len(a)-len(b); v=F.mul(a[-1],inv); q[k]^=v
        a=add(a,[0]*k+scale(b,v,F.mul))
    return trim(q),a

def gcd_bezout(a,b,F):
    A,B=trim(a),trim(b); u,v=[1],[]; s,t=[],[1]
    while B:
        q,r=pdiv(A,B,F)
        A,B=B,r
        u,s=s,add(u,mulp(q,s,F.mul))
        v,t=t,add(v,mulp(q,t,F.mul))
    factor=F.inv(A[-1])
    g=scale(A,factor,F.mul); u=scale(u,factor,F.mul); v=scale(v,factor,F.mul)
    assert add(mulp(u,a,F.mul),mulp(v,b,F.mul))==g
    assert not pdiv(a,g,F)[1] and not pdiv(b,g,F)[1]
    return g,u,v

def gaussian_row(n,qpow,mul):
    # [a,k]_q = [a-1,k]_q + q^(a-k) [a-1,k-1]_q.
    row=[1]
    for a in range(1,n+1):
        nextrow=[0]*(a+1)
        for k in range(a+1):
            if k<a: nextrow[k]^=row[k]
            if k>0: nextrow[k]^=mul(qpow(a-k),row[k-1])
        row=nextrow
    return row

def contracted(r,qpow,mul):
    if r==0: return [1]
    before=[1]; now=[1^qpow(1),1]
    for j in range(2,r+1):
        c=mul(qpow(2*j-2),1^qpow(1))
        d=mul(1^qpow(2*j-2),1^qpow(2*j-3))
        before,now=now,add(mulp([c,1],now,mul),scale(before,d,mul))
    return now

def inflate(P,mul):
    r=len(P)-1
    # Laurent y=z+z^-1 expansion, followed by multiplication by z^r.
    power={0:1}; out=[0]*(2*r+1)
    for coeff in P:
        for exp,v in power.items(): out[r+exp]^=mul(coeff,v)
        nextpower={}
        for exp,v in power.items():
            for nextexp in (exp-1,exp+1): nextpower[nextexp]=nextpower.get(nextexp,0)^v
        power={e:v for e,v in nextpower.items() if v}
    return trim(out)

def determinant_bareiss(matrix):
    """Exact fraction-free elimination in F_2[q], no field quotient shortcuts."""
    a=[row[:] for row in matrix]; n=len(a)
    if n==0: return 1
    prev=1
    for k in range(n-1):
        pivot=next((j for j in range(k,n) if a[j][k]),None)
        if pivot is None: return 0
        a[k],a[pivot]=a[pivot],a[k]
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=bm(pivot,a[i][j])^bm(a[i][k],a[k][j])
                a[i][j]=bexact(numerator,prev)
            a[i][k]=0
        prev=pivot
    return a[-1][-1]

def resultant(a,b):
    a=trim(a); b=trim(b)
    if not a: return 0 if len(b)>1 else 1
    if not b: return 0 if len(a)>1 else 1
    n=len(a)-1; m=len(b)-1
    if n==0: return bp(a[0],m)
    if m==0: return bp(b[0],n)
    rows=[]
    for shift in range(m): rows.append([0]*shift+list(reversed(a))+[0]*(m-1-shift))
    for shift in range(n): rows.append([0]*shift+list(reversed(b))+[0]*(n-1-shift))
    return determinant_bareiss(rows)

def cyclotomic_binary(n):
    # Monic exact division via x^n+1 = product_{d|n} Phi_d in F_2[x].
    values={}
    for d in range(1,n+1):
        if n%d: continue
        f=(1<<d)^1
        for k,phi in values.items():
            if d%k==0: f=bexact(f,phi)
        values[d]=f
    return values[n]

def hexes(a): return [hex(v) for v in a]

def symbolic_controls():
    rows=[]
    for r in range(1,11):
        H=gaussian_row(2*r,lambda e:1<<e,bm)
        P=contracted(r,lambda e:1<<e,bm)
        assert inflate(P,bm)==H
        constant=1
        for j in range(1,r+1): constant=bm(constant,1^(1<<(2*j-1)))
        assert P[0]==constant
        row={'r':r,'H_degree':2*r,'reciprocal_identity':True,'constant_product':True}
        if r<=6:
            A=P[::2]; B=P[1::2]
            R=resultant(A,B); DP=resultant(P,deriv(P)); DH=resultant(H,deriv(H))
            assert DP==bm(R,R)
            assert DH==bm(bm(constant,constant),bm(DP,DP))
            row.update({'ordinary_discriminant_identity':True,'parity_resultant_identity':True,
                        'R_q_polynomial_hex':hex(R),'DiscP_q_polynomial_hex':hex(DP),
                        'DiscH_q_polynomial_hex':hex(DH)})
            if r==3:
                expected=bm(bm(bp(3,6),7),0x3b)
                assert R==expected
                row['R3_factorization_verified']=True
        rows.append(row)
    return rows

def counterexample(n,N,f):
    F=Field(f); assert F.order_is(2,N)
    H=gaussian_row(n,lambda e:F.pow(2,e),F.mul)
    D=deriv(H); g,u,v=gcd_bezout(H,D,F)
    P=contracted(n//2,lambda e:F.pow(2,e),F.mul)
    assert inflate(P,F.mul)==H
    gp,_,_=gcd_bezout(P,deriv(P),F)
    assert P[0]!=0
    out={'n':n,'N':N,'modulus_hex':hex(f),'irreducible_exhaustive_trial_division':True,
         'exact_order_verified':True,'H_coefficients':hexes(H),'ordinary_derivative':hexes(D),
         'gcd':hexes(g),'gcd_degree':len(g)-1,'contracted_gcd_degree':len(gp)-1,
         'bezout_U':hexes(u),'bezout_V':hexes(v),'bezout_verified':True,
         'H_quotient_by_gcd':hexes(pdiv(H,g,F)[0]),'not_target_half_degree':n!=(N-1)//2}
    return out

def factor_85_controls():
    factors=[]
    for f in range(1<<8,1<<9):
        if irreducible(f):
            F=Field(f)
            if F.order_is(2,85): factors.append(f)
    product=1
    rows=[]
    for f in factors:
        product=bm(product,f)
        row=counterexample(52,85,f)
        rows.append(row)
    assert len(factors)==8
    assert product==cyclotomic_binary(85)
    assert [r['modulus_hex'] for r in rows if r['gcd_degree']>0]==['0x177']
    assert [r['gcd_degree'] for r in rows]==[0,4,0,0,0,0,0,0]
    return {'factors_independently_enumerated':list(map(hex,factors)),
            'product_equals_Phi85':True,'Phi85_hex':hex(product),
            'bad_factor_count':1,'good_factor_count':7,'rows':rows}

def frobenius_control(N,f):
    F=Field(f); assert F.order_is(2,N)
    m=(N-1)//2; H=gaussian_row(m,lambda e:F.pow(2,e),F.mul)
    products=[1]
    for j in range(1,N):
        term=1^F.pow(2,j); assert term
        products.append(F.mul(products[-1],term))
    assert products[-1]==1
    for k,c in enumerate(H):
        rhs=F.mul(F.pow(2,-k*k),F.mul(products[2*k],F.inv(F.pow(products[k],4))))
        assert F.mul(c,c)==rhs
    M=m*(m+1)//2; h=(N+1)//2
    assert products[m]==F.pow(2,h*M)
    delta=F.mul(F.pow(2,-M),products[m])
    assert F.pow(delta,2)==F.pow(2,-M)
    assert F.pow(delta,16)==2
    inverse_16=pow(16,-1,N)
    assert delta==F.pow(2,inverse_16)
    return {'N':N,'m':m,'modulus_hex':hex(f),'all_coefficients_checked':m+1,
            'coefficient_frobenius_identity':True,'full_product_is_one':True,
            'half_product_monomial':True,'delta_squared_identity':True,
            'delta_16_equals_q':True,'inverse_16_mod_N':inverse_16,
            'delta_hex':hex(delta),'diagonal_monomial_identity':True,
            'target_squarefreeness_test_performed':False}

def parity_degree_drop_controls():
    # Specializations over F_2[q] with generic parity coefficient terms removed.
    cases=[[],[1],[0,1],[1,1],[1,0,1],[1,1,1],[1,0,0,1],
           [1,2,0,0,1],[1,0,0,0,1],[1,2,0,0,0,1],[1,0,4,0,0,1]]
    rows=[]
    for P in cases:
        if len(P)<2: continue
        R=resultant(P[::2],P[1::2]); D=resultant(P,deriv(P))
        assert D==bm(R,R)
        rows.append({'P':hexes(P),'R':hex(R),'DiscP':hex(D),'verified':True})
    return rows

def main():
    symbolic=symbolic_controls()
    case31=counterexample(6,31,0x3b)
    F=Field(0x3b); H=list(map(lambda h:int(h,16),case31['H_coefficients']))
    G=[1,0,7,0,1]
    assert case31['gcd']==hexes(G)
    assert H==mulp(G,[1,4,1],F.mul)
    assert G==mulp([1,0x1b,1],[1,0x1b,1],F.mul)
    case31['stated_factorization_and_square_verified']=True
    case15=counterexample(10,15,0x19)
    assert case15['gcd']==['0x1','0x0','0x7','0x0','0x1']
    all85=factor_85_controls()
    case85=next(row for row in all85['rows'] if row['modulus_hex']=='0x177')
    assert case85['gcd']==['0x1','0x0','0xa','0x0','0x1']
    frobenius=[frobenius_control(9,0x49),frobenius_control(21,0x57)]
    frobenius += [frobenius_control(85,int(f,16)) for f in all85['factors_independently_enumerated']]
    # Compare exact recomputed outputs to supplied numeric data, never to code.
    claims=json.loads((SOURCE/'CONTROL_RESULTS.json').read_text())
    fresh_cases=[case31,case15,case85]
    for fresh in fresh_cases:
        claim=next(r for r in claims['stronger_claim_counterexamples'] if r['degree_n']==fresh['n'] and r['order_N']==fresh['N'])
        assert fresh['H_coefficients']==claim['H_coefficients_low_to_high_hex']
        assert fresh['ordinary_derivative']==claim['derivative_coefficients_low_to_high_hex']
        assert fresh['gcd']==claim['gcd_coefficients_low_to_high_hex']
    claimed85=[(r['modulus_hex'],r['gcd_degree']) for r in claims['order_85_degree_52_factors']]
    assert claimed85==[(r['modulus_hex'],r['gcd_degree']) for r in all85['rows']]
    result={'all_controls_passed':True,'implementation':'Fresh standard-library-only binary-polynomial arithmetic',
        'supplied_code_executed_imported_or_compiled':False,'symbolic_controls':symbolic,
        'parity_degree_drop_controls':parity_degree_drop_controls(),
        'counterexamples':fresh_cases,'order_85_factors':all85,'frobenius_controls':frobenius,
        'exact_claimed_coefficients_derivatives_gcds_match':True,
        'accepted_finite_certificate_recensus':False,'uniform_squarefreeness_inferred':False,
        'novelty_inferred':False}
    target=OUT/'FRESH_CONTROL_RESULTS.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_controls_passed':True,'symbolic_reciprocal_checks':len(symbolic),
        'ordinary_discriminant_checks':6,'order_85_gcd_degrees':[r['gcd_degree'] for r in all85['rows']],
        'frobenius_checks':len(frobenius),'result_file':str(target)},indent=2))

if __name__=='__main__': main()
