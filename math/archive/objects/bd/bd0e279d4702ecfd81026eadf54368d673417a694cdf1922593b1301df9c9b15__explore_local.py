import sympy as s
q,z,x=s.symbols('q z x')
def H(n):
 a,c=s.Integer(1),1+z
 if n==0:return a
 for k in range(2,n+1):a,c=c,s.Poly((1+z)*c+(q**(k-1)-1)*z*a,z,q).as_expr()
 return c
for d,p in [(13,5),(5,61)]:
 G=H((d-1)//2); C=s.cyclotomic_poly(d,q)
 print('CASE',d,p,'G=',G)
 for f,e in s.factor_list(C,modulus=p)[1]:
  K=s.GF(p).alg_field_from_poly(s.Poly(f,q,modulus=p),'a') if False else None
  # resultant data in Fp[q]; the detailed field controls are separate.
  print('factor',f)
 print('gcd coeff resultant:',s.gcd(s.Poly(s.resultant(z**d+1,G,z),q,modulus=p),s.Poly(C,q,modulus=p)))
 print('gcd disc:',s.gcd(s.Poly(s.discriminant(G,z),q,modulus=p),s.Poly(C,q,modulus=p)))
# symbolic discriminant local orders in q for small manageable m
for d,A,b in [(1,4,0),(3,2,0),(3,2,1),(5,2,2),(5,1,2),(3,3,1)]:
 n=d*A+b; G=H(b); D=s.Poly(s.discriminant(H(n),z),q); phi=s.Poly(s.cyclotomic_poly(d,q),q); k=0
 while not D.is_zero and s.rem(D,phi).is_zero:D=s.exquo(D,phi);k+=1
 print('valuation check',d,A,b,'m',n,'ordPhi',k,'baseR',s.rem(s.resultant(z**d+1,G,z),phi.as_expr(),q),flush=True)
