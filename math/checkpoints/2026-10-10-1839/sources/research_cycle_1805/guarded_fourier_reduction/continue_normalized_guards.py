#!/usr/bin/env python3
"""Fresh continuation of this pass only; imports no inherited research programs."""
import json,time,importlib.util,heapq
from pathlib import Path
OUT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('our_fresh_kernel',OUT/'reduce_guarded.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def divide(a,b):
 assert b
 if not a:return {}
 lm=max(b);iv=m.inv(b[lm])
 if len(b)==1:
  if any(any(x<y for x,y in zip(e,lm)) for e in a):return None
  return {tuple(x-y for x,y in zip(e,lm)):m.mul(c,iv) for e,c in a.items()}
 r=dict(a);q={};heap=[tuple(-v for v in e) for e in r];heapq.heapify(heap);steps=0
 while r:
  while True:
   e=tuple(-v for v in heapq.heappop(heap))
   if e in r:break
  if any(x<y for x,y in zip(e,lm)):return None
  shift=tuple(x-y for x,y in zip(e,lm));c=m.mul(r[e],iv);q[shift]=m.add(q.get(shift,m.ZERO),c)
  for n,v in b.items():
   k=tuple(x+y for x,y in zip(shift,n));val=m.sub(r.get(k,m.ZERO),m.mul(c,v))
   if val==m.ZERO:r.pop(k,None)
   else:
    if k not in r:heapq.heappush(heap,tuple(-x for x in k))
    r[k]=val
  steps+=1
  if steps>m.CAP_TERMS or len(r)>m.CAP_TERMS:raise m.SizeLimit('division work/terms cap')
 return q
m.exact_div=divide

def normalize_guards(gs):
 divisors=[(k,p) for k,p in gs.items() if len(p)==1 and m.ZM not in p]
 for gid,g in list(gs.items()):
  for did,d in divisors:
   if did==gid:continue
   while True:
    q=divide(g,d)
    if q is None:break
    m.EVENTS.append(dict(kind='normalize_guard',guard=gid,nonzero_divisor_guard=did,dividend=m.keep(g),divisor=m.keep(d),quotient=m.keep(q)))
    print('NORMALIZE_GUARD',gid,did,len(g),len(q),flush=True);g=q
  gs[gid]=g

def main():
 started=time.monotonic();D=json.loads((OUT/'scan_50000/CERTIFICATE.json').read_text());m.POLYS.update(D['polynomials']);m.EVENTS.extend(D['events']);m.ATTEMPTS.extend(D['attempts'])
 es={k:m.unpack(D['polynomials'][h]) for k,h in D['final']['equations'].items()};gs={k:m.unpack(D['polynomials'][h]) for k,h in D['final']['guards'].items()};eliminated=list(D['final']['eliminated_variables'])
 round=0
 while True:
  round+=1;normalize_guards(gs);m.cancel(es,gs)
  candidates=[]
  for eid,p in es.items():
   for j,v in enumerate(m.VS):
    if v in eliminated:continue
    by=m.coeffs(p,j)
    if max(by,default=0)!=1:continue
    a=by[1];proof=m.certified_factorization(a,gs)
    if proof is not None:
     b=by.get(0,{});candidates.append((len(b)*len(a),len(p),v,eid,j,a,m.pneg(b),proof))
  candidates.sort(key=lambda x:x[:4]);print('STATS',m.stat(es),'SAFE_PIVOTS',[(c[2],c[3],len(c[5]),len(c[6])) for c in candidates],flush=True)
  if not candidates:stop='no factor divisible by retained primitive guards and no certified safe linear pivot';break
  committed=False
  for _,__,v,eid,j,den,num,proof in candidates:
   try:
    ne={};changes=[]
    for oid,p in es.items():
     q,d=m.substituted(p,j,num,den)
     if q:ne[oid]=q
     changes.append(dict(equation=oid,old=m.keep(p),new=m.keep(q),denominator_power=d))
     if sum(map(len,ne.values()))>m.CAP_TOTAL:raise m.SizeLimit('total equation term cap')
    ng={};gchanges=[]
    for gid,g in gs.items():
     q,d=m.substituted(g,j,num,den);assert q
     ng[gid]=q;gchanges.append(dict(guard=gid,old=m.keep(g),new=m.keep(q),denominator_power=d))
    m.EVENTS.append(dict(kind='linear_elimination',variable=v,source_equation=eid,source=m.keep(es[eid]),numerator=m.keep(num),denominator=m.keep(den),denominator_nonzero=dict(guard_factors=proof['guard_factors'],constant=[list(proof['constant'][0]),proof['constant'][1]]),equation_transforms=changes,guard_transforms=gchanges))
    es,gs=ne,ng;eliminated.append(v);committed=True;print('PIVOT',v,eid,m.stat(es),flush=True);break
   except m.SizeLimit as e:
    m.ATTEMPTS.append(dict(action='normalized_guard_pivot',variable=v,equation=eid,status='size_limit',reason=str(e)));print('LIMIT',v,eid,str(e),flush=True)
  if not committed:stop='all safe linear pivots exceed explicit polynomial-size/work limits';break
 final=dict(equations={k:m.keep(p) for k,p in es.items()},guards={k:m.keep(p) for k,p in gs.items()},statistics=m.stat(es),eliminated_variables=eliminated,stop_reason=stop)
 D.update(polynomials=m.POLYS,events=m.EVENTS,final=final,attempts=m.ATTEMPTS,continued_runtime_seconds=time.monotonic()-started)
 m.save_json('CERTIFICATE.json',D);m.save_json('FINAL.json',final)
 summary={k:v for k,v in D.items() if k not in ['polynomials','initial','events','final']};summary.update(initial_statistics=D['initial']['statistics'],final=final,event_count=len(m.EVENTS),cancellations=sum(e['kind']=='cancel' for e in m.EVENTS),guard_normalizations=sum(e['kind']=='normalize_guard' for e in m.EVENTS),linear_eliminations=sum(e['kind']=='linear_elimination' for e in m.EVENTS),polynomials=len(m.POLYS));m.save_json('SUMMARY.json',summary)
 print('DONE',final['statistics'],'EVENTS',len(m.EVENTS),flush=True)
if __name__=='__main__':main()
