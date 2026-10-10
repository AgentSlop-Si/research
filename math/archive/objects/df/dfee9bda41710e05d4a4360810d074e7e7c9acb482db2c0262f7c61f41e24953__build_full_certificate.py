"""Fresh exact proof-DAG builder. Does not load or execute predecessor code.
Input is our newly generated six row-elimination polynomials, not a solver oracle.
Buchberger-style search is used only to discover a linear-combination proof of 1.
"""
import sympy as S,json,time,sys,os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.set_int_max_str_digits(0)
from sympy.polys.rings import ring
from sympy.polys.domains import QQ
z=S.Symbol('z');root=S.CRootOf(z**4+1,3);K=QQ.algebraic_field(root);Z=K.unit
R,*v=ring('t0,t1,t2,t3,w',K,order='grevlex')
def export(f):
 return [[list(ex),[[int(c.numerator),int(c.denominator)]for c in reversed(co.to_list())]]for ex,co in sorted(f.items())]
allraw=json.load(open(os.path.join(HERE,'all_row_resultants.json')))
inputs=[]
for j in range(20):
 inputs.append(R.from_dict({tuple(ex):sum(K(num)/K(den)*Z**i for i,(num,den) in enumerate(cs))for ex,cs in allraw[j]}))
F=[];nodes=[];lookup={}
def add(f,comb):
 if f in lookup:return lookup[f]
 i=len(F);F.append(f);nodes.append({'polynomial':export(f),'combination':[[j,export(c)]for j,c in comb if c]});lookup[f]=i
 return i
for i,f in enumerate(inputs):add(f,[])
active=set(range(len(F)));pairs={(j,i)for j in active for i in active if i<j}
lcm=R.monomial_lcm;div=R.monomial_div;mul=R.monomial_mul
start=time.time();n=0
while pairs:
 pair=min(pairs,key=lambda ab:(R.order(lcm(F[ab[0]].LM,F[ab[1]].LM)),ab));pairs.remove(pair);i,j=pair
 mi,mj=F[i].LM,F[j].LM;ll=lcm(mi,mj)
 if ll==mul(mi,mj):continue
 ci=R.from_dict({div(ll,mi):K.one/F[i].LC});cj=R.from_dict({div(ll,mj):K.one/F[j].LC})
 sp=ci*F[i]-cj*F[j]
 order=sorted(active,key=lambda x:R.order(F[x].LM));qs,r=sp.div([F[a]for a in order]);n+=1
 if not r:continue
 invlc=K.one/r.LC;r=r.mul_ground(invlc)
 combo={i:ci,j:-cj}
 for k,q in zip(order,qs):combo[k]=combo.get(k,R.zero)-q
 combo=[(k,c.mul_ground(invlc))for k,c in combo.items() if c]
 k=add(r,combo)
 print('NODE',k,'terms',len(r),'active',len(active),'pairs',len(pairs),'seconds',round(time.time()-start,2),flush=True)
 if r.is_ground:
  assert r==R.one
  ancestors=set();todo=[k]
  while todo:
   a=todo.pop()
   if a in ancestors:continue
   ancestors.add(a);todo.extend(b for b,c in nodes[a]['combination'])
  data={'field':'Q[z]/(z^4+1)','variables':['t0','t1','t2','t3','w'],'source_resultant_indices':list(range(20)),'inputs':[export(f)for f in inputs],'nodes':{str(a):nodes[a] for a in sorted(ancestors)},'final_node':k,'stats':{'generated_nodes':len(F),'retained_nodes':len(ancestors),'critical_pairs_reduced':n,'seconds':time.time()-start}}
  json.dump(data,open(os.path.join(HERE,'EXACT_UNIT_CERTIFICATE.json'),'w'),indent=1)
  print('CERTIFICATE',data['stats'],flush=True);break
 # Maintain a small active reducer set. This only influences discovery, never proof validity.
 old=list(active)
 for a in old:pairs.add((max(k,a),min(k,a)))
 active={a for a in active if not div(F[a].LM,r.LM)}|{k}
else:print('NO UNIT FOUND',flush=True)
