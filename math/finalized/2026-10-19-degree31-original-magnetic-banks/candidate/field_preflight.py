"""Fresh prime-polynomial proof, using only ordinary unbounded integer arithmetic."""
import json,time
from pathlib import Path
R=Path(__file__).resolve().parent;P=53;D=31
assert all(P%d for d in range(2,int(P**.5)+1)) and all(D%d for d in range(2,int(D**.5)+1))
def trim(a):
 a=[x%P for x in a]
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def rem(a,b):
 a=trim(a)
 while len(a)>=len(b) and a!=[0]:
  s=len(a)-len(b);q=a[-1]*pow(b[-1],-1,P)%P
  for j,v in enumerate(b):a[s+j]-=q*v
  a=trim(a)
 return a
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def power(a,e,h):
 r=[1]
 while e:
  if e&1:r=rem(mul(r,a),h)
  e//=2
  if e:a=rem(mul(a,a),h)
 return r
def gcd(a,b):
 while b!=[0]:a,b=b,rem(a,b)
 return trim([x*pow(a[-1],-1,P) for x in a])
start=time.time();tests=[]
for ac in range(52*52):
 a=ac//52+1;c=ac%52+1
 h=[c,a]+[0]*(D-2)+[1];f=[0,1];rs=[]
 for _ in range(D):f=power(f,P,h);rs.append(f)
 g=rs[0][:]+[0]*max(0,2-len(rs[0]));g[1]-=1;g=gcd(h,trim(g));ok=f==[0,1] and g==[1]
 tests.append({'linear':a,'constant':c,'final_frobenius':f,'gcd':g,'irreducible':ok})
 if ok:break
assert ok,'bounded trinomial representation search exhausted'
out={'verdict':'PASS','prime':P,'degree':D,'modulus_ascending':h,'chosen_linear':a,'chosen_constant':c,'order':str(P**D),'order_bits':(P**D).bit_length(),'all_frobenius_remainders':rs,'gcd_with_X53_minus_X':g,'proof':'53 and 31 are prime. h divides X^(53^31)-X, a squarefree polynomial whose irreducible factors have degrees dividing 31. gcd(h,X^53-X)=1 excludes degree 1, so degree(h)=31 forces h irreducible. No extension inverse used.','runtime_seconds':time.time()-start}
(R/'FIELD_SEARCH.json').write_text(json.dumps({'family':'X^31+a*X+c, lexicographic a,c=1..52','tests':tests,'chosen_linear':a,'chosen_constant':c},indent=2)+'\n')
(R/'FIELD_IRREDUCIBILITY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='all_frobenius_remainders'}))
