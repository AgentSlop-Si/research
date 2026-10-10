import sympy as s,json,time,math
from pathlib import Path
q,z,y=s.symbols('q z y'); OUT=Path(__file__).parent
# Fresh q-Pascal construction, no predecessor code imports.
def H(n):
 row=[s.Integer(1)]
 for a in range(1,n+1):
  row=[s.Integer(1)]+[s.expand(row[k]+q**(a-k)*row[k-1]) for k in range(1,a)]+[s.Integer(1)]
 return sum(c*z**k for k,c in enumerate(row))
def coefficients(f):return [int(c) for c in s.Poly(f,q).all_coeffs()[::-1]]
results=[]
for d in [3,7,11,15,19]:
 start=time.time();ph=s.cyclotomic_poly(d,q);b=(d-1)//2
 def R(f):return s.rem(f,ph,q)
 h=H(b);u=s.div(h,z+1,z)[0]
 # Compute discriminant through reciprocal quadratic contraction.
 r=(b-1)//2;p=u
 basis=[s.Integer(2),y]
 for k in range(2,r+1):basis.append(s.expand(y*basis[-1]-basis[-2]))
 poly=s.Poly(u,z);contract=poly.nth(r)+sum(poly.nth(r+j)*basis[j] for j in range(1,r+1))
 delta=R(contract.subs(y,2)*contract.subs(y,-2)*s.discriminant(contract,y)**2) if r else s.Integer(1)
 print('d',d,'delta ready',round(time.time()-start,2),flush=True)
 # Compute the resultant exactly with coefficients in the cyclotomic field.
 K=s.QQ.alg_field_from_poly(s.Poly(ph,q),'w'); w=K.ext
 uk=s.Poly.from_dict({(k,):K([s.Rational(c) for c in s.Poly(R(s.Poly(u,z).nth(k)),q).all_coeffs()]) for k in range(b)},z,domain=K)
 fk=s.Poly(z**d+1,z,domain=K)
 resk=fk.rep.resultant(uk.rep)
 # Convert the algebraic-number coefficient list back to its q representative.
 cs=resk.to_list(); res=sum(s.Rational(c)*q**(len(cs)-1-j) for j,c in enumerate(cs))
 guard=R(delta*res);pair=R(guard*R(guard.subs(q,q**(d-1))))
 item={'d':d,'b':b,'U':str(u),'delta':coefficients(delta),'R':coefficients(res),'guard':coefficients(guard),'paired_guard':coefficients(pair),'content':int(s.Poly(pair,q).content()),'seconds':time.time()-start}
 results.append(item);(OUT/'FIXED_BASE_RESULTS.json').write_text(json.dumps(results,indent=2))
 print('d',d,'content',item['content'],'factor',s.factorint(item['content']),'time',item['seconds'],flush=True)
