"""Self-authored exact checks; no downloaded research code is imported."""
import hashlib,json,pathlib
from check_valuation import mul,quo,divmodp,val,add,scale,trace,resultant
ROOT=pathlib.Path(__file__).resolve().parent

def ppow(a,n):
 out=1
 while n:
  if n&1:out=mul(out,a)
  a=mul(a,a);n>>=1
 return out

def translated(p,a):
 out=[0]*len(p)
 powers=[ppow(a,j) for j in range(len(p))]
 for i,c in enumerate(p):
  for j in range(i+1):
   if i&j==j:out[j]^=mul(c,powers[i-j])
 return out

def res(a,b):
 if not any(a) and len(b)==1 and b[0]==1:return 1
 return resultant(a[:],b[:])

def gaussian_trace(m):
 c=[1]
 for n in range(1,2*m+2):
  out=[0]*(n+1)
  for k in range(n+1):
   out[k]=(c[k] if k<n else 0)^((c[k-1]<<(n-k)) if k else 0)
  c=out
 u=[c[0]]
 for i in range(1,2*m+1):u.append(c[i]^u[-1])
 assert u[-1]==c[-1] and u==u[::-1]
 out=[u[m]]+[0]*m
 ck0=0;ck1=2
 for k in range(1,m+1):
  if k==1:ck=ck1
  else:ck=(ck1<<1)^ck0;ck0,ck1=ck1,ck
  for i in range(k+1):
   if ck>>i&1:out[i]^=u[m+k]
 return out

def reduction(p):return sum((c.bit_count()&1)<<i for i,c in enumerate(p))

rows=[];negative=0
for m in [1,2,3,4,12]:
 p=trace(m);assert p==gaussian_trace(m)
 e=p[0];R=res(p[::2],p[1::2]);Q=mul(e,R)
 r=m//2;par=m%2;v=(m+1)//2;N=m*(m+1)*(2*m+1)//3
 base=3*(m*m//4);extra=2*(m//4);kappa=m+base+extra
 assert val(e)==m and val(R)>=base+extra
 assert (Q.bit_length()-1)==N and val(Q,2)==v
 T=translated(p,6)
 for i,c in enumerate(T):
  required=3*((m-i+1)//2)
  assert divmodp(c,ppow(3,required))[1]==0
 assert res(T[::2],T[1::2])==R
 if m==1:
  assert T==[0,1] and R==1
  Atilde=[0];Btilde=[1];rt=1
 else:
  Atilde=[quo(T[2*i],ppow(3,3*(r+par-i))) for i in range(r+par)]
  Btilde=[quo(T[2*i+1],ppow(3,3*(r-i))) for i in range(r)]
  if not par:Atilde.append(1)
  else:Btilde.append(1)
  rt=res(Atilde,Btilde)
  assert R==mul(ppow(3,base),rt)
  main=ppow(3,r);secondary=ppow(3,r-1) if r%2 else 0
  expectedA=(secondary<<1) if par else main
  expectedB=main if par else secondary
  assert reduction(Atilde)==expectedA
  assert reduction(Btilde)==expectedB
  assert reduction(Atilde)!=(expectedA^1);negative+=1
  assert reduction(Btilde)!=(expectedB^1);negative+=1
  assert val(rt)>=extra
 qhat=quo(Q,mul(1<<v,ppow(3,kappa)))
 assert qhat.bit_length()-1==N-v-kappa
 if m<=3:
  assert val(R)==base+extra
  assert divmodp(R,ppow(3,base+extra+1))[1]!=0;negative+=1
 rows.append({'m':m,'q_degree_Q':N,'q_content_Q':v,'exact_w_valuation_E':val(e),'exact_w_valuation_R':val(R),'proved_R_lower_bound':base+extra,'proved_Q_w_lower_bound':kappa,'deflated_Q_degree':qhat.bit_length()-1,'residual_A_mod_w':hex(reduction(Atilde)),'residual_B_mod_w':hex(reduction(Btilde)),'all_checks_passed':True})
report={'controls':rows,'negative_controls_rejected':negative,'uniform_proof':'REPORT.md','scope':'Valuation/identity checks only; no endpoint-order census and no support closure.'}
(ROOT/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
# Upstream source identities are retained separately in SOURCE_BINDINGS.json.
# This portable manifest covers the package's own files only.
manifest={}
for name in ['REPORT.md','check_packet.py','check_valuation.py','RESULTS.json']:
 p=ROOT/name
 manifest[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
