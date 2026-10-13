"""Independent finite-A certificate by a split prime and polynomial gcds."""
import json, math, pathlib
P=229;D=57;B=27
assert all(P%v for v in range(2,math.isqrt(P)+1))
def clean(a):
 while a and a[-1]%P==0:a.pop()
 return [v%P for v in a]
def add(a,b):return clean([(a[j] if j<len(a) else 0)+(b[j] if j<len(b) else 0) for j in range(max(len(a),len(b)))])
def scale(a,s):return clean([v*s for v in a])
def rem(a,b):
 a=clean(a[:]);b=clean(b[:]);assert b
 while len(a)>=len(b):
  v=a[-1]*pow(b[-1],-1,P)%P;k=len(a)-len(b)
  for j in range(len(b)):a[k+j]=(a[k+j]-v*b[j])%P
  a=clean(a)
 return a
def gcd(a,b):
 while b:a,b=b,rem(a,b)
 return scale(a,pow(a[-1],-1,P)) if a else []
def derivative(a):return clean([j*a[j] for j in range(1,len(a))])
def he(n):
 a,b=[1],[0,1]
 if n==0:return a
 for j in range(1,n):a,b=b,add([0]+b,scale(a,-j))
 return b
def coeffs(q):
 vals=[1]
 for n in range(1,B+1):
  vals=[((vals[j] if j<n else 0)+(pow(q,n-j,P)*vals[j-1] if j else 0))%P for j in range(n+1)]
 return vals
witnesses=[]
for q in range(1,P):
 if pow(q,D,P)!=1 or pow(q,D//3,P)==1 or pow(q,D//19,P)==1:continue
 c=coeffs(q);g=sum(j*(-1)**(j-1)*c[j] for j in range(1,B+1))%P
 factors=[(1-pow(q,j,P))%P for j in range(1,B+1)]
 denominator_factors=[(1-pow(q,2*j,P))%P for j in range(1,(D+B)//2+1)]
 assert all(factors+denominator_factors)
 if not g:continue
 wn=math.prod(factors)%P;wd=math.prod(denominator_factors)%P
 tau=D*wn*pow(wd,-1,P)*pow(g,-1,P)%P
 out=[]
 for A in range(3,8):
  J=add([0]+he(A),scale(he(A-1),-A*tau));dd=derivative(J);G=gcd(J,dd)
  out.append({'A':A,'J_ascending':J,'derivative_ascending':dd,'monic_gcd':G})
 if all(r['monic_gcd']==[1] for r in out):
  witnesses.append({'prime':P,'q':q,'order':D,'B':B,'g':g,'W_numerator':wn,'W_denominator':wd,'tau':tau,'results':out})
  break
assert witnesses
# Check Hermite derivative convention independently for every required degree.
for n in range(1,8):assert derivative(he(n))==scale(he(n-1),n)
assert gcd([0,0,1],[0,2])!=[1] # A=1, tau=0, J=x^2
assert gcd([0,0,0,1],[0,0,3])!=[1] # A=2, tau=-1/2, J=x^3
out={'status':'PASS independent finite-A exact split-prime specialization',
 'scope':'original b27,d57 parameter; characteristic-zero DiscJ nonzero for A3..7',
 'witness':witnesses[0],'negative_controls':2}
pathlib.Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
