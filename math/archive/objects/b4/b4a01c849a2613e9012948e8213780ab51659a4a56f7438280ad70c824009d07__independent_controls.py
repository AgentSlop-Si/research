"""Fresh controls only. No predecessor source is imported or executed."""
from pathlib import Path
import json
import sympy as s
q,z,y,t=s.symbols('q z y t')
OUT=Path(__file__).resolve().parent

def bdeg(a): return a.bit_length()-1
def prem(a,b):
 while a and bdeg(a)>=bdeg(b): a^=b<<(bdeg(a)-bdeg(b))
 return a
def pgcd(a,b):
 while b: a,b=b,prem(a,b)
 return a
def fmul(a,b,f):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if bdeg(a)==bdeg(f):a^=f
 return c
def fpow(a,n,f):
 out=1
 while n:
  if n&1:out=fmul(out,a,f)
  a=fmul(a,a,f);n>>=1
 return out
def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def add(a,b):
 c=[0]*max(len(a),len(b))
 for i,v in enumerate(a):c[i]^=v
 for i,v in enumerate(b):c[i]^=v
 return trim(c)
def scale(a,c,f):return trim([fmul(v,c,f) for v in a])
def mulz(a):return [0]+a
def zrem(a,b,f):
 a=a[:];bi=fpow(b[-1],(1<<bdeg(f))-2,f)
 while a!=[0] and len(a)>=len(b):
  c=fmul(a[-1],bi,f); shift=len(a)-len(b)
  for i,v in enumerate(b):a[i+shift]^=fmul(c,v,f)
  trim(a)
 return a
def zgcd(a,b,f):
 while b!=[0]:a,b=b,zrem(a,b,f)
 return scale(a,fpow(a[-1],(1<<bdeg(f))-2,f),f)
def deriv(a):return trim([a[i] if i%2 else 0 for i in range(1,len(a))])
def irreducible(f):
 d=bdeg(f);x=2;t=x
 for i in range(1,d+1):
  t=fmul(t,t,f)
  if i<=d//2 and pgcd(t^x,f)!=1:return False
 return t==x

def field_example(n,N,f):
 assert irreducible(f)
 assert fpow(2,N,f)==1
 for p in s.factorint(N):assert fpow(2,N//int(p),f)!=1
 hs=[[1],[1,1]]
 for k in range(2,n+1):
  hs.append(add(add(hs[-1],mulz(hs[-1])),scale(mulz(hs[-2]),1^fpow(2,k-1,f),f)))
 a=hs[-1];da=deriv(a);g=zgcd(a,da,f)
 assert len(g)>1
 return {'degree_n':n,'order_N':N,'modulus_hex':hex(f),'extension_degree':bdeg(f),'H_coefficients_low_to_high_hex':[hex(v) for v in a],'derivative_coefficients_low_to_high_hex':[hex(v) for v in da],'gcd_coefficients_low_to_high_hex':[hex(v) for v in g],'gcd_degree':len(g)-1,'irreducible':True,'exact_order_verified':True,'target_half_degree':2*n+1==N}

def make_h(n,f):
 h0,h1=[1],[1,1]
 if n==0:return h0
 for k in range(2,n+1):
  h0,h1=h1,add(add(h1,mulz(h1)),scale(mulz(h0),1^fpow(2,k-1,f),f))
 return h1

def check_order_85():
 fs=[0x13f,0x177,0x17b,0x18b,0x1a3,0x1bd,0x1dd,0x1f9]
 # Verify the complete factor list independently against the integer cyclotomic polynomial.
 prod=s.Integer(1); rows=[]
 for f in fs:
  assert irreducible(f) and fpow(2,85,f)==1
  assert fpow(2,17,f)!=1 and fpow(2,5,f)!=1
  prod*=sum(q**i for i in range(bdeg(f)+1) if f>>i&1)
  h=make_h(52,f);g=zgcd(h,deriv(h),f)
  rows.append({'modulus_hex':hex(f),'extension_degree':8,'degree_H':52,'gcd_degree':len(g)-1})
 assert s.Poly(prod-s.cyclotomic_poly(85,q),q,modulus=2).is_zero
 assert [v['gcd_degree'] for v in rows]==[0,4,0,0,0,0,0,0]
 return rows

def check_target_frobenius(N,f):
 assert irreducible(f) and fpow(2,N,f)==1
 for p in s.factorint(N):assert fpow(2,N//int(p),f)!=1
 m=(N-1)//2;hs=make_h(m,f);F=[1]
 for j in range(1,N):F.append(fmul(F[-1],1^fpow(2,j,f),f))
 assert F[-1]==1
 for k,a in enumerate(hs):
  lhs=fmul(fmul(a,a,f),fpow(2,k*k,f),f)
  lhs=fmul(lhs,fpow(F[k],4,f),f)
  assert lhs==F[2*k]
 M=m*(m+1)//2
 delta=fmul(fpow(2,(-M)%N,f),F[m],f)
 assert delta==fpow(2,pow(16,-1,N),f)
 return {'N':N,'m':m,'modulus_hex':hex(f),'coefficient_frobenius_identity_verified':True,'delta_monomial_identity_verified':True,'squarefreeness_test_performed':False}

def main():
 # Polynomial controls are in the independent indeterminate q over F_2.
 def mod(e,*xs):return s.Poly(e,*xs,modulus=2).as_expr()
 hs=[s.Integer(1),z+1]
 ps=[s.Integer(1),y+1+q]
 controls=[]
 for n in range(2,21):
  hs.append(mod((z+1)*hs[-1]+(1+q**(n-1))*z*hs[-2],q,z))
  if n%2:continue
  r=n//2
  if r>=2:ps.append(mod((y+q**(2*r-2)*(1+q))*ps[-1]+(1+q**(2*r-2))*(1+q**(2*r-3))*ps[-2],q,y))
  P=ps[r]
  assert mod(s.expand(z**r*P.subs(y,z+1/z))-hs[n],q,z)==0
  const=s.prod(1+q**(2*j-1) for j in range(1,r+1))
  assert mod(P.subs(y,0)-const,q)==0
  rec={'degree_H':n,'degree_P':r,'reciprocal_deflation_verified':True,'constant_product_verified':True}
  if n<=12:
   dh=mod(s.resultant(hs[n],s.diff(hs[n],z),z),q)
   dp=mod(s.resultant(P,s.diff(P,y),y),q)
   assert mod(dh-const**2*dp**2,q)==0
   coeff=s.Poly(P,y)
   A=sum(coeff.nth(2*j)*t**j for j in range(r//2+1))
   B=sum(coeff.nth(2*j+1)*t**j for j in range((r-1)//2+1))
   R=mod(s.resultant(A,B,t),q)
   assert mod(dp-R**2,q)==0
   if r==3:
    assert mod(R-(q+1)**6*(q*q+q+1)*(q**5+q**4+q**3+q+1),q)==0
    rec['residual_R3_factorization_verified']=True
   rec['discriminant_identity_verified']=True
   rec['parity_resultant_identity_verified']=True
  controls.append(rec)
 result={'indeterminate_controls':controls,'stronger_claim_counterexamples':[field_example(6,31,0x3b),field_example(10,15,0x19),field_example(52,85,0x177)],'order_85_degree_52_factors':check_order_85(), 'target_frobenius_identity_controls':[check_target_frobenius(9,0x49),check_target_frobenius(21,0x57),check_target_frobenius(85,0x177)],'no_target_range_recensus':True,'predecessor_code_executed_or_imported':False}
 (OUT/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
