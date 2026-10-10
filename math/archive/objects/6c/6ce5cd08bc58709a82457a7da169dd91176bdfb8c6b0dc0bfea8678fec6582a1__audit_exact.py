"""Fresh independent exact arithmetic. Reads predecessor JSON as data only.

All polynomial coefficients are ascending. This implementation uses only the
Python standard library; no predecessor implementation is imported or run.
"""
from fractions import Fraction as F
from math import gcd, comb, factorial, isqrt
from functools import reduce
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
SOURCE = Path('ramified_chirp_squarefreeness_0341')

def trim(a):
    a = list(a)
    while a and a[-1] == 0: a.pop()
    return a

def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])

def neg(a): return [-x for x in a]

def mul(a,b):
    c=[0]*(len(a)+len(b)-1) if a and b else []
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def divmodq(a,b):
    a=[F(x) for x in trim(a)]; b=[F(x) for x in trim(b)]
    assert b
    q=[F(0)]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        j=len(a)-len(b); v=a[-1]/b[-1]; q[j]=v
        for i,x in enumerate(b): a[i+j]-=v*x
        a=trim(a)
    return trim(q),a

PHI={1:[-1,1]}
def phi(n):
    if n not in PHI:
        x=[-1]+[0]*(n-1)+[1]
        for d in range(1,n):
            if n%d==0:
                x,r=divmodq(x,phi(d)); assert not r
        assert all(v.denominator==1 for v in x)
        PHI[n]=[int(v) for v in x]
    return PHI[n]

class Cyclotomic:
    def __init__(self,d):
        self.d=d; self.mod=phi(d); self.degree=len(self.mod)-1
        self.zero=(); self.one=(F(1),); self.w=self.e([0,1])
    def e(self,a): return tuple(divmodq(a,self.mod)[1])
    def c(self,n): return self.e([n])
    def add(self,a,b): return tuple(add(a,b))
    def neg(self,a): return tuple(neg(a))
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b): return self.e(mul(a,b))
    def pow(self,a,n):
        if n<0: return self.pow(self.inv(a),-n)
        v=self.one
        while n:
            if n&1: v=self.mul(v,a)
            a=self.mul(a,a); n//=2
        return v
    def inv(self,a):
        assert a
        r0,r1=self.mod,list(a); t0,t1=[],[1]
        while r1:
            q,r=divmodq(r0,r1); r0,r1=r1,r
            t0,t1=t1,add(t0,neg(mul(q,t1)))
        assert len(r0)==1
        return self.e([x/r0[0] for x in t0])
    def scale(self,a,k): return tuple(trim([v*k for v in a]))
    def ints(self,a):
        assert all(x.denominator==1 for x in a)
        return [int(x) for x in a]
    def det(self,M):
        M=[list(r) for r in M]; n=len(M); ans=self.one
        for j in range(n):
            p=next((i for i in range(j,n) if M[i][j]),None)
            if p is None: return self.zero
            if p!=j: M[p],M[j]=M[j],M[p]; ans=self.neg(ans)
            pivot=M[j][j]; ans=self.mul(ans,pivot); inv=self.inv(pivot)
            for i in range(j+1,n):
                f=self.mul(M[i][j],inv)
                for k in range(j+1,n): M[i][k]=self.sub(M[i][k],self.mul(f,M[j][k]))
                M[i][j]=self.zero
        return ans

def h_at_w(K,n):
    row=[K.one]
    for j in range(1,n+1):
        new=[]
        for k in range(j+1):
            v=row[k-1] if k else K.zero
            if k<len(row): v=K.add(v,K.mul(K.pow(K.w,k),row[k]))
            new.append(v)
        row=new
    return row

def zrem(K,a,g):
    a=list(a)
    while a and not a[-1]: a.pop()
    assert g[-1]==K.one
    while len(a)>=len(g):
        j=len(a)-len(g); v=a[-1]
        for i,c in enumerate(g): a[i+j]=K.sub(a[i+j],K.mul(v,c))
        while a and not a[-1]: a.pop()
    return a

def res_monic(K,g,h):
    """Norm determinant of multiplication by h in K[z]/g."""
    n=len(g)-1
    cols=[]
    for j in range(n):
        r=zrem(K,[K.zero]*j+h,g)
        cols.append(r+[K.zero]*(n-len(r)))
    return K.det([[cols[j][i] for j in range(n)] for i in range(n)])

def disc(K,g):
    b=len(g)-1
    if b<2: return K.one
    derivative=[K.scale(g[k],k) for k in range(1,b+1)]
    return K.scale(res_monic(K,g,derivative),(-1)**(b*(b-1)//2))

def finite_trim(a,p): return trim([x%p for x in a])
def finite_div(a,b,p):
    a=finite_trim(a,p); b=finite_trim(b,p); assert b
    quotient=[0]*max(0,len(a)-len(b)+1)
    while len(a)>=len(b):
        j=len(a)-len(b); t=a[-1]*pow(b[-1],-1,p)%p; quotient[j]=t
        for i,x in enumerate(b): a[i+j]=(a[i+j]-t*x)%p
        a=trim(a)
    return trim(quotient),a
def finite_gcd(a,b,p):
    a=finite_trim(a,p); b=finite_trim(b,p)
    while b: a,b=b,finite_div(a,b,p)[1]
    return finite_trim([x*pow(a[-1],-1,p) for x in a],p) if a else []
def finite_eval(a,x,p):
    v=0
    for c in reversed(a): v=(v*x+c)%p
    return v
def finite_pow(a,n,modulus,p):
    value=[1]
    while n:
        if n&1: value=finite_div(mul(value,a),modulus,p)[1]
        a=finite_div(mul(a,a),modulus,p)[1]; n//=2
    return value
def finite_irreducible(f,p):
    n=len(f)-1; x=[0,1]
    if finite_div(add(finite_pow(x,p**n,f,p),neg(x)),f,p)[1]: return False
    return all(finite_gcd(f,add(finite_pow(x,p**(n//ell),f,p),neg(x)),p)==[1]
               for ell in prime_factors(n))
def finite_h(n,q,p):
    row=[1]
    for j in range(1,n+1):
        row=[((row[k-1] if k else 0)+(pow(q,k,p)*row[k] if k<len(row) else 0))%p
             for k in range(j+1)]
    return row
def prime(n): return n>=2 and all(n%k for k in range(2,isqrt(n)+1))
def prime_factors(n): return [k for k in range(2,n+1) if n%k==0 and prime(k)]

def fixed_base(d):
    K=Cyclotomic(d); b=(d-1)//2; g=h_at_w(K,b)
    delta=disc(K,g)
    f=[K.one]+[K.zero]*(d-1)+[K.one]
    r=K.scale(res_monic(K,g,f),(-1)**(d*b))
    product=K.mul(delta,r)
    v=K.ints(product); content=reduce(gcd,map(abs,v),0)
    assert content
    return {'d':d,'b':b,'phi_ascending':phi(d),
            'H_coefficients_in_Qw_ascending':[K.ints(a) for a in g],
            'discriminant_remainder_ascending':K.ints(delta),
            'resultant_remainder_ascending':K.ints(r),
            'product_remainder_ascending':v,'content':content,
            'primitive_part_ascending':[x//content for x in v]}

def binomial_rational(v,t):
    ans=F(1)
    for j in range(t): ans*=v-j; ans/=j+1
    return ans

def local_hermite(d,A,b):
    K=Cyclotomic(d); n=A*d+b; L=A+1
    zero=[K.zero]*L
    def sadd(a,b): return [K.add(x,y) for x,y in zip(a,b)]
    def smul(a,b):
        c=zero.copy()
        for i,x in enumerate(a):
            if not x: continue
            for j,y in enumerate(b[:L-i]):
                if y: c[i+j]=K.add(c[i+j],K.mul(x,y))
        return c
    def qpower(k):
        ans=zero.copy(); wk=K.pow(K.w,k)
        for t in range(A//2+1): ans[2*t]=K.scale(wk,binomial_rational(F(k,d),t))
        return ans
    one=zero.copy(); one[0]=K.one
    row=[one]
    for j in range(1,n+1):
        row=[sadd(row[k-1] if k else zero,
                  smul(qpower(k),row[k]) if k<len(row) else zero)
             for k in range(j+1)]
    G=h_at_w(K,b); cluster_data=[]
    for aidx in range(d):
        alpha=K.neg(K.pow(K.w,aidx))
        assert K.pow(alpha,d)==K.c(-1)
        # actual[e][j] is the coefficient of epsilon^e x^j.
        actual=[[K.zero]*L for _ in range(L)]
        for k,cq in enumerate(row):
            for j in range(min(k,A)+1):
                az=K.scale(K.pow(alpha,k-j),comb(k,j))
                for e in range(L-j):
                    actual[e+j][j]=K.add(actual[e+j][j],K.mul(cq[e],az))
        assert all(not val for erow in actual[:A] for val in erow)
        ga=K.zero
        for k,v in enumerate(G): ga=K.add(ga,K.mul(v,K.pow(alpha,k)))
        predicted=[K.zero]*L
        for j in range(A//2+1):
            degree=A-2*j
            scalar=F((-1)**(A+j)*factorial(A)*d**(A-j),2**j*factorial(j)*factorial(degree))
            predicted[degree]=K.scale(K.mul(ga,K.pow(alpha,-degree)),scalar)
        assert actual[A]==predicted
        cluster_data.append({'alpha_minus_w_power':aidx,'residual_G_nonzero':bool(ga),
                             'all_lower_epsilon_coefficients_zero':True,
                             'leading_hermite_coefficients_exact':True})
    return {'d':d,'A':A,'b':b,'n':n,'clusters':cluster_data}

def finite_exceptions():
    data=json.loads((SOURCE/'EXCEPTION_CERTIFICATES.json').read_text())
    original=json.loads(Path('diagonal_chirp_classification_0246/MODULAR_CERTIFICATES.json').read_text())
    if isinstance(original,dict):
        # Metadata wrappers are handled as data, never as executable content.
        candidates=[v for v in original.values() if isinstance(v,list)]
        original=next(v for v in candidates if v and isinstance(v[0],dict) and 'N' in v[0])
    results=[]
    for cert in data:
        N,p,q=cert['N'],cert['prime_p'],cert['primitive_q']; m=(N-1)//2
        assert N in (25,169) and prime(p) and (p-1)%N==0
        assert pow(q,N,p)==1 and all(pow(q,N//ell,p)!=1 for ell in prime_factors(N))
        H=finite_h(m,q,p); T=[((-1)**(m-j)*v)%p for j,v in enumerate(H)]
        assert T==cert['T'] and cert['minimum']==m and T[0]!=0
        Tp=[j*T[j]%p for j in range(1,len(T))]
        identity=finite_trim(add(mul(cert['squarefree_bezout_u'],T),
                                 mul(cert['squarefree_bezout_v'],Tp)),p)
        assert identity==[1] and finite_gcd(T,Tp,p)==[1]
        assert all(finite_eval(T,pow(q,k,p),p)!=0 for k in range(N))
        entry=next(x for x in original if x['N']==N)
        assert entry==cert
        results.append({'N':N,'degree':m,'prime':p,'root':q,'prime_by_trial_division':True,
                        'exact_order':N,'T_matches_fresh_qPascal':True,
                        'explicit_Bezout_identity_ascending':identity,
                        'derivative_gcd_ascending':[1],'all_N_cycle_nodes_nonzero':True,
                        'exact_match_to_original_certificate':True})
    return results

def main():
    results={'arithmetic':'Python standard library only; exact Fraction cyclotomic fields, multiplication-norm determinants, fresh q-Pascal'}
    bases=[]
    for d in (5,9,13):
        print('Computing fixed base',d,flush=True)
        bases.append(fixed_base(d))
    results['fixed_bases']=bases
    assert [b['content'] for b in bases]==[5,3**8,13**4]
    results['bad_prime_controls']=[]
    for d,p in ((5,61),(13,5)):
        b=next(x for x in bases if x['d']==d)
        dg=finite_gcd(phi(d),b['discriminant_remainder_ascending'],p)
        rg=finite_gcd(phi(d),b['resultant_remainder_ascending'],p)
        bg=finite_gcd(phi(d),b['product_remainder_ascending'],p)
        assert len(bg)<len(phi(d))
        results['bad_prime_controls'].append({'d':d,'p':p,'disc_gcd_ascending':dg,
           'resultant_gcd_ascending':rg,'product_gcd_ascending':bg,'one_good_factor_exists':True})
    assert results['bad_prime_controls'][0]['disc_gcd_ascending']==[3,1]
    assert results['bad_prime_controls'][0]['resultant_gcd_ascending']==[1]
    assert results['bad_prime_controls'][1]['disc_gcd_ascending']==[1]
    assert results['bad_prime_controls'][1]['resultant_gcd_ascending']==[1,3,0,3,1]
    bad_quartic=results['bad_prime_controls'][1]['resultant_gcd_ascending']
    assert finite_irreducible(bad_quartic,5)
    assert pow(5,4,13)==1 and pow(5,2,13)!=1 and 5%13!=1
    # Since ord_13(5)=4, every factor of Phi_13 mod 5 has degree four.
    results['d13_p5_factor_structure']={'bad_quartic_ascending':bad_quartic,
      'irreducible_by_Frobenius_gcd_test':True,'multiplicative_order_13_of_5':4,
      'number_of_distinct_irreducible_factors':3,'all_factor_degrees':4}
    roots=[q for q in range(1,61) if pow(q,5,61)==1 and q!=1]
    values=[(q*q+2*q-3)%61 for q in roots]
    assert roots==[9,20,34,58] and values==[35,10,1,0]
    assert finite_h(2,58,61)==[1,59,1]
    results['d5_p61_roots_and_discriminants']={'roots':roots,'values':values,'bad_H2_ascending':[1,59,1]}
    local=[]
    for d,A,b in ((1,5,0),(3,3,0),(5,2,2),(5,3,0),(9,2,4),(13,2,6),(3,2,1)):
        print('Checking every local cluster',(d,A,b),flush=True)
        local.append(local_hermite(d,A,b))
    results['local_hermite_controls']=local
    print('Rebuilding isolated certificates',flush=True)
    results['finite_exceptions']=finite_exceptions()
    # Verify the cyclotomic identity over Z, then coefficientwise modulo p.
    reductions=[]
    for d,p in ((1,5),(5,3),(9,5),(13,3),(25,3),(15,7),(5,13)):
        composition=[0]*((len(phi(d))-1)*p+1)
        for j,v in enumerate(phi(d)): composition[p*j]=v
        quotient,remainder=divmodq(composition,phi(d)); assert not remainder
        assert quotient==phi(d*p)
        power=[1]
        for j in range(p-1): power=mul(power,phi(d))
        assert finite_trim(quotient,p)==finite_trim(power,p)
        K=d*((p-1)//2)*(((p-1)//2)-1)//2
        reductions.append({'d':d,'p':p,'identity_over_Z':True,'mod_p_identity':True,
                           'target_cluster_K':K,'K_greater_than_p_minus_one':K>p-1})
    results['cyclotomic_identity_controls']=reductions
    (OUT/'EXACT_ARITHMETIC_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print('All fresh standard-library exact controls passed.',flush=True)

if __name__=='__main__': main()
