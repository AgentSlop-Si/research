def compile_(h,matching=True,reclaim=False,dirty=True):
 t0=time.time();c,blocks,uses,value_uses,owner,signal,order,contains=build(h);v=len(c.inputs)
 print('built',h,len(blocks),'regions',flush=True,file=sys.stderr)
 edges,chosen,right,stats=match(blocks,uses,matching)
 print('matched',len(chosen),'seconds',time.time()-t0,flush=True,file=sys.stderr)
 slots=[];frames=[];ops=[];events=[];hist=Counter();assign={};sources={};retired=set();stats['regions']=len(blocks);stats['matched']=len(chosen);stats['multi_node_regions']=sum(len(b['nodes'])>1 for b in blocks)
 def new(g):
  s=len(slots);slots.append(0);frames.append(g);hist[blocks[g]['rank']]+=1;events.append((s,-1,g));return s
 def raise_(s,g):
  old=frames[s];assert contains(blocks[old]['frame'],blocks[g]['frame']);hist[blocks[g]['rank']-blocks[old]['rank']]+=1;frames[s]=g;events.append((s,old,g))
 def xor(a,b,g):
  assert a!=b;raise_(a,g);raise_(b,g);slots[a]^=slots[b];ops.append((a,b,g))
 def acquire(g,anchors):
  if reclaim:
   bb={}
   def ins(s):
    row=slots[s];expr=1<<s
    while row:
     p=row.bit_length()-1
     if p not in bb:bb[p]=(row,expr);return None
     old,e=bb[p];row^=old;expr^=e
    return expr
   for s in anchors:ins(s)
   for s in sorted(retired):
    if not contains(blocks[frames[s]]['frame'],blocks[g]['frame']):continue
    e=ins(s)
    if e is None:continue
    assert e>>s&1;e^=1<<s;aa=[]
    while e:
     bit=e&-e;aa.append(bit.bit_length()-1);e^=bit
    for a in aa:xor(s,a,g)
    assert not slots[s];retired.remove(s);stats['reclaimed']+=1;stats['clearing_xors']+=len(aa);return s
  return new(g)
 for step,g in enumerate(order):
  b=blocks[g];outuses=[u for u in b['uses']if u not in right];outvalues=sorted({uses[u][0]for u in outuses});assert outvalues==b['outvalues']
  if b['source']:
   x=b['nodes'][0];s=new(g);sources[x-1]=s;slots[s]=signal[x];value_slots={x:s};spare=[]
  else:
   ins=[assign[next(u for u in value_uses[y]if uses[u][1]==g and uses[u][2]is None)]for y in b['inputs']]
   assert len(set(ins))==len(ins)
   for s,y in zip(ins,b['inputs']):assert slots[s]==signal[y];raise_(s,g)
   # Independent desired output rows first, then preserved input signals,
   # then standard-unit completion. Every row is a literal linear form
   # on incoming physical roles, hence invertible on all dirty inputs.
   rows=[];labels=[];echelon=[]
   for x in outvalues:
    r=b['coeff'][x]
    if independent(echelon,r):rows.append(r);labels.append(('value',x));echelon=basis(rows)
   output_rank=len(rows)
   for e in sorted(b['selected']):
    _,u,i=edges[e];r=1<<i;assert independent(echelon,r);rows.append(r);labels.append(('carry',u));echelon=basis(rows)
   for i in range(len(ins)):
    if independent(echelon,1<<i):rows.append(1<<i);labels.append(('retire',i));echelon=basis(rows)
   assert len(rows)==len(ins)
   rr=rows.copy();elim=[]
   for i in range(len(ins)):
    j=next(j for j in range(i,len(ins))if rr[j]>>i&1)
    if j!=i:
     # Synthesize swap as three XORs at the single common frame.
     for a,z in ((i,j),(j,i),(i,j)):rr[a]^=rr[z];elim.append((a,z))
    for j in range(len(ins)):
     if j!=i and rr[j]>>i&1:rr[j]^=rr[i];elim.append((j,i))
   assert rr==[1<<i for i in range(len(ins))]
   for a,z in reversed(elim):xor(ins[a],ins[z],g)
   value_slots={};spare=[]
   for s,(kind,key)in zip(ins,labels):
    if kind=='value':value_slots[key]=s;assert slots[s]==signal[key]
    elif kind=='carry':assign[key]=s;assert slots[s]==signal[uses[key][0]]
    else:retired.add(s);spare.append(s)
   # Express every dependent desired output in the new independent basis.
   ob=list(value_slots);bb={}
   for i,x in enumerate(ob):
    r=b['coeff'][x];e=1<<i
    while r:
     p=r.bit_length()-1
     if p not in bb:bb[p]=(r,e);break
     old,ee=bb[p];r^=old;e^=ee
   for x in outvalues:
    if x in value_slots:continue
    r=b['coeff'][x];e=0
    while r:p=r.bit_length()-1;old,ee=bb[p];r^=old;e^=ee
    s=acquire(g,list(value_slots.values()))
    for i,y in enumerate(ob):
     if e>>i&1:xor(s,value_slots[y],g)
    assert slots[s]==signal[x];value_slots[x]=s
  used=set()
  for u in outuses:
   x=uses[u][0];s=value_slots[x]
   if x in used:
    ss=acquire(g,list(value_slots.values()));xor(ss,s,g);s=ss
   used.add(x);assert u not in assign;assign[u]=s
  if step%5000==0:print('compile',h,step,len(slots),'reclaimed',stats['reclaimed'],'seconds',time.time()-t0,flush=True,file=sys.stderr)
 output_slots=[];output_records=[];scatter=[0]*v;J=[]
 for u,(x,g,target)in enumerate(uses):
  if target is None:continue
  s=assign[u];assert slots[s]==signal[x];raise_(s,g);output_slots.append(s)
  common,triple=target;output_records.append((s,g,common,triple))
  targets=[i for i,t in enumerate(c.inputs)if common in t]if len(triple)==1 else[c.inputs.index(triple)]
  for i in targets:scatter[i]^=slots[s];J.append((v+i,2*v+s))
  rank=blocks[g]['rank']
  if len(triple)==1:hist[rank]+=1;hist[h-rank]+=1
  else:hist[h-1-rank]+=1;hist[1]+=1
 assert len(set(output_slots))==len(output_slots)
 for s in retired:hist[h-blocks[frames[s]]['rank']]+=1
 assert len(retired)+len(output_slots)==len(slots)
 assert scatter==[1<<i for i in range(v)]
 R=len(slots);mass=sum(k*v for k,v in hist.items());assert mass==h*R+h*(h-1),(mass,R)
 if dirty:
  initial=[1<<i for i in range(2*v+R)];M=[(2*v+a,2*v+b)for a,b,g in ops];V=[(2*v+s,i)for i,s in sources.items()];word=M+J+M[::-1]+V+M+J+M[::-1]+V
  for dual in (False,True):
   values=initial.copy()
   for a,b in reversed(word)if dual else word:
    if dual:a,b=b,a
    values[a]^=values[b]
   assert values[2*v:]==initial[2*v:]
   if dual:assert values[:v]==[initial[i]^initial[v+i]for i in range(v)]and values[v:2*v]==initial[v:2*v]
   else:assert values[v:2*v]==[initial[i]^initial[v+i]for i in range(v)]and values[:v]==initial[:v]
 return dict(h=h,mode=dict(matching=matching,reclaim=reclaim),roles=R,baseline_pr48_roles={23:36432,25:48329}[h],histogram=dict(hist),rank_mass=mass,elementary_xors=len(ops),stats=dict(stats),dirty_basis_vectors=2*v+R,complete_dirty_basis_both_orientations=dirty,all_physical_frame_inclusions=True,seconds=time.time()-t0),dict(h=h,v=v,R=R,ops=ops,sources=sources,scatter=J,outputs=output_records,frames=[b['frame']for b in blocks],events=events)
