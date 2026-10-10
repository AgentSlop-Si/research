"""Fresh exact safe Laurent-binomial reduction of the full Fourier equations.
Only proven nonzero variables are divided. Coefficients are exact Q(zeta11).
No supplied or reviewer program is executed/imported.
"""
import json,pathlib,time,collections
import sympy as sp
from sympy.polys.domains import QQ
R=pathlib.Path(__file__).resolve().parent
L=json.loads((R/'topology_11.json').read_text())['layers'];n=11
z=sp.Symbol('zeta');t=sp.Symbol('t');K=QQ.algebraic_field((sp.Poly(sum(t**i for i in range(11)),t),z));Z=K.unit
ZERO=(0,)*99
P=collections.defaultdict(list)
for a,(u,j) in enumerate(L[0]):
 for b,(v,uu) in enumerate(L[1]):
  if u==uu:
   for c,(i,vv) in enumerate(L[2]):
    if v==vv:P[i,j].append((a,33+b,66+c))
def mono(es):
 v=[0]*99
 for e in es:v[e]+=1
 return tuple(v)
def clean(p):return {e:c for e,c in p.items() if c}
def coeff(c):return str(K.to_sympy(c))
eqs=[];labels=[]
for i in range(n):
 for j in range(n):
  p={ZERO:-(Z**((i*j)%11))}
  for es in P[i,j]:p[mono(es)]=K.one
  eqs.append(p);labels.append(['entry',i,j])
forced=set(e for ps in P.values() if len(ps)==1 for e in ps[0]);new_initial=[]
for m in json.loads((R/'minor_tropical_full_certificate.json').read_text()):
 if m['family_count']!=1:continue
 i,k=m['rows'];j,l=m['cols'];f=m['families'][0]
 target=Z**((i*j+k*l)%11)-Z**((i*l+k*j)%11)
 eqs.append({mono(f['edges']):K.convert(f['sign']),ZERO:-target});labels.append(['minor',i,k,j,l])
 forced.update(f['edges'])
initialforced=sorted(forced)
gauges=[]
for v in range(11):
 opts=[e for e,(r,c) in enumerate(L[0]) if r==v and e in forced]
 if opts:gauges.append(min(opts))
 opts=[66+e for e,(r,c) in enumerate(L[2]) if c==v and e+66 in forced]
 if opts:gauges.append(min(opts))
assert len(gauges)==21 and len(set(gauges))==21
subs=[];eliminated=set();start=time.monotonic()
def substitute(x,q,ex,why):
 global eqs
 assert x in forced and x not in eliminated and ex[x]==0
 assert all(not a or e in forced for e,a in enumerate(ex)),(x,ex)
 out=[]
 for p in eqs:
  new={}
  for old,c in p.items():
   power=old[x]
   if power:
    e=tuple(old[j]+power*ex[j] if j!=x else 0 for j in range(99));c=c*q**power
   else:e=old
   new[e]=new.get(e,K.zero)+c
  out.append(clean(new))
 eqs=out;eliminated.add(x)
 subs.append({'variable':x,'coefficient':coeff(q),'exponent':list(ex),'reason':why})
for e in gauges:substitute(e,K.one,ZERO,['gauge_fix',e])
while time.monotonic()-start<120:
 constantbad=next((i for i,p in enumerate(eqs) if len(p)==1 and next(iter(p))==ZERO),None)
 if constantbad is not None:break
 candidates=[]
 for i,p in enumerate(eqs):
  if len(p)!=2:continue
  (a,ca),(b,cb)=list(p.items())
  sa={e for e,v in enumerate(a) if v};sb={e for e,v in enumerate(b) if v}
  # At least one monomial is known nonzero, so equality forces both nonzero.
  if not (sa<=forced or sb<=forced):continue
  possible_forced=forced|sa|sb
  d=tuple(a[e]-b[e] for e in range(99))
  for x,v in enumerate(d):
   if abs(v)!=1 or x in eliminated:continue
   ex=tuple(-d[e]//v if e!=x else 0 for e in range(99))
   q=(-cb/ca) if v==1 else (-ca/cb)
   score=(sum(abs(y) for y in ex),len(sa|sb),x,i)
   candidates.append((score,i,x,q,ex,possible_forced))
 if not candidates:break
 _,i,x,q,ex,ff=min(candidates,key=lambda c:c[0]);forced=ff
 substitute(x,q,ex,labels[i])
else:constantbad=None
active=sorted(set(e for p in eqs for ex in p for e,v in enumerate(ex) if v))
nonzero=[{'label':labels[i],'terms':[{'exponent':list(ex),'coefficient':coeff(c)} for ex,c in p.items()]} for i,p in enumerate(eqs) if p]
out={'status':'contradiction' if constantbad is not None else 'reduced_without_contradiction','runtime_seconds':time.monotonic()-start,'initial_mandatory_edges':initialforced,'current_mandatory_edges':sorted(forced),'safe_gauge_edges':gauges,'substitution_count':len(subs),'substitutions':subs,'eliminated_variables':sorted(eliminated),'remaining_variable_count':len(active),'remaining_variables':active,'remaining_equation_count':len(nonzero),'remaining_term_histogram':dict(collections.Counter(len(e['terms']) for e in nonzero)),'remaining_equations':nonzero,'scope':'Exact algebraic reduction in safe Laurent variables; no assignment or global no-go unless a checked nonzero constant is derived.'}
(R/'full_fourier_monomial_reduction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['substitutions','remaining_equations','initial_mandatory_edges','current_mandatory_edges','eliminated_variables','remaining_variables','safe_gauge_edges']},indent=2))
