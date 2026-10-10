"""Fresh bounded exact linear elimination, never dividing by optional variables.
Produces necessary equations. Nonvanishing constraints on eliminated mandatory
variables may be dropped, so a remaining solution is not a Fourier witness.
"""
import json,pathlib,time,collections
import sympy as sp
from sympy.polys.domains import QQ
R=pathlib.Path(__file__).resolve().parent
r=json.loads((R/'full_fourier_monomial_reduction.json').read_text())
z=sp.Symbol('zeta');t=sp.Symbol('t');K=QQ.algebraic_field((sp.Poly(sum(t**i for i in range(11)),t),z));ZERO=(0,)*99
forced=set(r['current_mandatory_edges']);eliminated=set(r['eliminated_variables'])
def fromc(s):return K([QQ.convert(c) for c in sp.Poly(sp.sympify(s,locals={'zeta':z}),z,domain=QQ).all_coeffs()])
def coeff(c):return str(K.to_sympy(c))
def encode(p):return [{'exponent':list(e),'coefficient':coeff(c)} for e,c in p.items()]
eqs=[{tuple(x['exponent']):fromc(x['coefficient']) for x in p['terms']} for p in r['remaining_equations']]
labels=[p['label'] for p in r['remaining_equations']]
def norm(p):
 if not p:return p
 mins=[min(e[j] for e in p) for j in range(99)]
 assert all(a>=0 or j in forced for j,a in enumerate(mins))
 shift=tuple(a if j in forced else min(a,0) for j,a in enumerate(mins))
 return {tuple(e[j]-shift[j] for j in range(99)):c for e,c in p.items()}
def plus(a,b):
 out=dict(a)
 for e,c in b.items():
  out[e]=out.get(e,K.zero)+c
  if not out[e]:del out[e]
 return out
def times(a,b):
 out={}
 if len(a)*len(b)>200000:raise OverflowError('term multiplication cap')
 for e,c in a.items():
  for f,d in b.items():
   g=tuple(x+y for x,y in zip(e,f));out[g]=out.get(g,K.zero)+c*d
 return {e:c for e,c in out.items() if c}
start=time.monotonic();steps=[];stop='no safe linear pivot';constantbad=None
for iteration in range(60):
 eqs=[norm(p) for p in eqs]
 constantbad=next((i for i,p in enumerate(eqs) if len(p)==1 and next(iter(p))==ZERO),None)
 if constantbad is not None:stop='nonzero constant';break
 if time.monotonic()-start>90:stop='90-second cap';break
 candidates=[]
 for i,p in enumerate(eqs):
  if len(p)<2:continue
  for x in range(99):
   terms=[(e,c) for e,c in p.items() if e[x]]
   if len(terms)!=1:continue
   (e,c),=terms
   if e[x]!=1 or any(e[j] and j!=x and j not in forced for j in range(99)):continue
   degree=max((a[x] for q in eqs for a in q),default=0)
   assert degree>=1
   support=len(p)-1
   cost=sum(support**a[x] for q in eqs for a in q if a[x])
   candidates.append(((cost,support,degree,x,i),x,i,e,c))
 if not candidates:break
 _,x,i,e,c=min(candidates)
 replacement={tuple(a[j]-e[j] if j!=x else 0 for j in range(99)):-d/c for a,d in eqs[i].items() if a!=e}
 assert all(ex[x]==0 for ex in replacement)
 assert all(a>=0 or j in forced for ex in replacement for j,a in enumerate(ex))
 source=encode(eqs[i]);new=[]
 try:
  powers={0:{ZERO:K.one},1:replacement}
  for p in eqs:
   q={}
   for a,d in p.items():
    k=a[x]
    if k not in powers:
     for kk in range(2,k+1):
      if kk not in powers:powers[kk]=times(powers[kk-1],replacement)
    rem=tuple(0 if j==x else a[j] for j in range(99))
    q=plus(q,times({rem:d},powers[k]))
   if len(q)>10000:raise OverflowError('single equation term cap')
   new.append(q)
  if sum(map(len,new))>100000:raise OverflowError('total term cap')
 except OverflowError as ex:stop=str(ex);break
 eqs=new;eliminated.add(x)
 steps.append({'variable':x,'source_label':labels[i],'source_equation':source,'replacement':encode(replacement),'replacement_required_nonzero_in_original_problem':x in forced,'remaining_total_terms':sum(map(len,eqs))})
 print('step',len(steps),'variable',x,'replacementterms',len(replacement),'totalterms',sum(map(len,eqs)),flush=True)
else:stop='60-step cap'
active=sorted({j for p in eqs for e in p for j,v in enumerate(e) if v})
out={'status':'necessary-system contradiction' if constantbad is not None else 'reduced necessary system without contradiction','stop_reason':stop,'runtime_seconds':time.monotonic()-start,'elimination_steps':steps,'step_count':len(steps),'remaining_variable_count':len(active),'remaining_variables':active,'remaining_nonzero_equations':sum(bool(p) for p in eqs),'term_histogram':dict(collections.Counter(len(p) for p in eqs if p)),'remaining_equations':[{'label':lab,'terms':encode(p)} for lab,p in zip(labels,eqs) if p],'scope':'Only divisions by proved nonzero mandatory variables; dropped nonvanishing conditions mean this is a necessary relaxation, not an equivalence or candidate factorization.'}
(R/'full_fourier_linear_reduction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['elimination_steps','remaining_equations','remaining_variables']},indent=2))
