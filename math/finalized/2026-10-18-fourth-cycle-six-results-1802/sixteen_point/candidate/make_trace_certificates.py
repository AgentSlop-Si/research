"""Discovery only: recorded modular ideal-membership derivations, checked separately."""
from pathlib import Path
from itertools import product
import json,time
from sympy.polys.rings import ring
from sympy.polys.domains import GF
from sympy.polys.orderings import grevlex
P=97

def pack(p):return [[list(m),int(c)%P] for m,c in sorted(p.items()) if int(c)%P]

def certificate(ns):
 names=[f'b{stride}_{j}' for stride,n in zip((1,3,7,5),ns) for j in range(1,n+1)]
 R,*v=ring(names,GF(P),grevlex);cs=[R.zero for _ in range(16)];cs[0]=R.one;offset=0
 for stride,n in zip((1,3,7,5),ns):
  group=[R.one]+v[offset:offset+n];offset+=n;ds=[R.zero for _ in range(16)]
  for i in range(16):
   for j,c in enumerate(group):ds[(i+stride*j)%16]+=cs[i]*c
  cs=ds
 f=[(-1)**i*cs[i]-cs[i+8] for i in range(8)]
 nodes=[{'kind':'input','index':i,'polynomial':pack(q)} for i,q in enumerate(f)]
 I={q:i for i,q in enumerate(f)}; F=set(range(len(f)));G=set();CP=set();order=R.order
 lcm=R.monomial_lcm; mul=R.monomial_mul; div=R.monomial_div
 def update(G,B,ih):
  mh=f[ih].LM; C=G.copy();D=set()
  while C:
   ig=C.pop();mg=f[ig].LM;L=lcm(mh,mg)
   def ld(ip):return div(L,lcm(mh,f[ip].LM)) is not None
   if mul(mh,mg)==L or (not any(ld(ip) for ip in C) and not any(ld(pr[1]) for pr in D)):D.add((ih,ig))
  E={(i,j) for i,j in D if mul(mh,f[j].LM)!=lcm(mh,f[j].LM)}
  Bnew={(i,j) for i,j in B if div(lcm(f[i].LM,f[j].LM),mh) is None or lcm(f[i].LM,mh)==lcm(f[i].LM,f[j].LM) or lcm(f[j].LM,mh)==lcm(f[i].LM,f[j].LM)}
  return {i for i in G if div(f[i].LM,mh) is None}|{ih},Bnew|E
 # First normalize inputs with derivation nodes, which also permits immediate unit input.
 for i in range(len(f)):
  if f[i]==R.one:return nodes,i
  if not f[i]:F.discard(i);continue
  if f[i].LC!=R.domain.one:
   c=f[i].LC;h=f[i].monic();nodes.append({'kind':'scale','source':i,'scale':int(R.domain.one/c)%P,'polynomial':pack(h)})
   I[h]=len(f);F.discard(i);F.add(len(f));f.append(h)
 while F:
  ih=min(F,key=lambda i:order(f[i].LM));F.remove(ih);G,CP=update(G,CP,ih)
 while CP:
  i,j=min(CP,key=lambda ij:order(lcm(f[ij[0]].LM,f[ij[1]].LM)));CP.remove((i,j))
  L=lcm(f[i].LM,f[j].LM);di=div(L,f[i].LM);dj=div(L,f[j].LM)
  h=f[i].mul_monom(di)-f[j].mul_monom(dj)
  J=sorted(G,key=lambda k:order(f[k].LM));quot,rem=h.div([f[k] for k in J])
  if not rem:continue
  c=rem.LC;h=rem.monic()
  if h in I:ih=I[h]
  else:
   ih=len(f);I[h]=ih;f.append(h)
   nodes.append({'kind':'spair_reduce','left':i,'right':j,'left_shift':list(di),'right_shift':list(dj),'reductions':[[k,pack(q)] for k,q in zip(J,quot) if q],'scale':int(R.domain.one/c)%P,'polynomial':pack(h)})
   assert len(nodes)==len(f)
  if h==R.one:return nodes,ih
  G,CP=update(G,CP,ih)
 raise ValueError(('not unit',ns,[str(f[i]) for i in G]))

def main():
 base=Path(__file__).parent;outdir=base/'parity7_traces';outdir.mkdir(exist_ok=True)
 pats=[ns for ns in product(range(8),repeat=4) if sum(ns)==7 and ns==max(ns[i:]+ns[:i] for i in range(4))]
 for ns in reversed(pats):
  dest=outdir/('_'.join(map(str,ns))+'.json')
  if dest.exists():print('EXISTS',ns,flush=True);continue
  tt=time.time();print('START',ns,flush=True);nodes,final=certificate(ns)
  out={'N':16,'prime':P,'stride_order':[1,3,7,5],'counts':list(ns),'nodes':nodes,'final':final}
  dest.write_text(json.dumps(out,separators=(',',':'))+'\n')
  print('DONE',ns,'nodes',len(nodes),'bytes',dest.stat().st_size,'seconds',time.time()-tt,flush=True)
if __name__=='__main__':main()
