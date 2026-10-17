"""Fresh exact certificates; finite-field witnesses imply characteristic-zero nonvanishing."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent
# Dense ascending polynomials. All arithmetic uses Python integers modulo a stated prime.
def trim(a):
 a=list(a)
 while a and a[-1]==0:a.pop()
 return a
def add(a,b,p):return trim([((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
def neg(a,p):return [(-v)%p for v in a]
def sub(a,b,p):return add(a,neg(b,p),p)
def mul(a,b,p):
 if not a or not b:return []
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return trim(c)
def scale(a,t,p):return trim([x*t%p for x in a])
def divrem(a,b,p):
 a=trim(a); assert b
 quotient=[0]*max(0,len(a)-len(b)+1); inv=pow(b[-1],-1,p)
 while a and len(a)>=len(b):
  k=len(a)-len(b); c=a[-1]*inv%p;quotient[k]=c
  for j,v in enumerate(b):a[k+j]=(a[k+j]-c*v)%p
  a=trim(a)
 return trim(quotient),a
def xgcd(a,b,p):
 r0,r1=a,b;s0,s1=[1],[];t0,t1=[],[1]
 while r1:
  q,r=divrem(r0,r1,p);r0,r1=r1,r;s0,s1=s1,sub(s0,mul(q,s1,p),p);t0,t1=t1,sub(t0,mul(q,t1,p),p)
 c=pow(r0[-1],-1,p)
 return scale(r0,c,p),scale(s0,c,p),scale(t0,c,p)
def derivative(a,p):return trim([i*a[i]%p for i in range(1,len(a))])
def gaussian(n,q,p):
 row=[1]
 for r in range(1,n+1):
  row=[((row[k] if k<r else 0)+(pow(q,r-k,p)*row[k-1] if k else 0))%p for k in range(r+1)]
 return row
def prime(n):return n>=2 and all(n%j for j in range(2,int(n**.5)+1))
def order(a,p):
 v=a%p;k=1
 while v!=1:v=v*a%p;k+=1
 return k
records=[]
for d,bs in [(9,range(3,9)),(25,range(5,25))]:
 for b in bs:
  ell=d+1;attempts=[]
  while True:
   if not prime(ell) or (ell-1)%d:ell+=1;continue
   a=next(a for a in range(2,ell) if order(a,ell)==d)
   h=gaussian(b,a,ell); hp=derivative(h,ell);u=h
   if b%2:u,remainder=divrem(h,[1,1],ell);assert not remainder
   f=[1]+[0]*(d-1)+[1]
   g,A,B=xgcd(h,hp,ell);v,C,D=xgcd(u,f,ell)
   attempts.append({'prime':ell,'root':a,'derivative_gcd_degree':len(g)-1,'node_gcd_degree':len(v)-1})
   if g==[1] and v==[1]:break
   ell+=1
  assert add(mul(A,h,ell),mul(B,hp,ell),ell)==[1]
  assert add(mul(C,u,ell),mul(D,f,ell),ell)==[1]
  p0=3 if d==9 else 5
  assert sum(pow(a,j*(d//p0),ell) for j in range(p0))%ell==0
  rec={'d':d,'b':b,'prime':ell,'omega_image':a,'root_order':d,'H_ascending':h,'U_ascending':u,
       'H_Hprime_bezout':[A,B],'U_F_bezout':[C,D],'attempts':attempts,
       'charzero_conclusions':{'H_squarefree':True,'U_squarefree':True,'U_F_coprime':True,'H_F_gcd':'z+1' if b%2 else '1'}}
  records.append(rec);print(f'd={d}, b={b}: certified over QQ(omega) by prime {ell}, omega -> {a}; attempts={len(attempts)}',flush=True)
(P/'modular_certificates.json').write_text(json.dumps({'coefficient_order':'ascending','scope':'Characteristic-zero conclusions certified by one good reduction; no positive-characteristic uniform theorem','records':records},indent=2)+'\n')
