"""Independent reviewer-authored controls. Reads inert JSON data, never imports or executes submitted programs."""
import json, pathlib, itertools, math
ROOT=pathlib.Path('research_cycle_0958'); OUT=ROOT/'review/supplement_v1'
def inv(a,p): return pow(a%p,p-2,p)
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b,p): return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def elim(a,p,inverse=False):
 n=len(a); b=[r[:] + (eye(n)[i] if inverse else []) for i,r in enumerate(a)]; d=1
 for k in range(n):
  z=next((i for i in range(k,n) if b[i][k]%p),None)
  if z is None: return (0,None) if inverse else 0
  if z!=k: b[z],b[k]=b[k],b[z]; d=-d
  v=b[k][k]%p; d=d*v%p; w=inv(v,p); b[k]=[x*w%p for x in b[k]]
  for i in range(n):
   if i!=k:
    w=b[i][k]; b[i]=[(x-w*y)%p for x,y in zip(b[i],b[k])]
 return (d,[r[n:] for r in b]) if inverse else d

def cycle_green(c,weights,p):
 n=len(c); W=eye(n)
 for t in range(n): W[c[t]][c[t-1]]=(W[c[t]][c[t-1]]-weights[t])%p
 d,G=elim(W,p,True); assert d; return d,G

results={'authorship':'Independent reviewer, fresh programs only','mask_reconstructions':[],'holonomy_reconstructions':[]}
for n in [4,8,16,32]:
 for p,g in [(998244353,3),(2013265921,31)]:
  data=json.loads((ROOT/f'masks/fresh_N{n}_p{p}.json').read_text()); ii=pow(g,(p-1)//4,p); z=pow(g,(p-1)//n,p)
  assert pow(z,n,p)==1 and pow(z,n//2,p)!=1
  al=[(a+b*ii)*inv(d,p)%p for a,b,d in [(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6),(1,3,11)]]
  gs=[]
  for c,a in zip(data['cycles'],al):
   pos={v:j for j,v in enumerate(c)}; den=inv(1-pow(a,n,p),p)
   gs.append([[pow(a,(pos[r]-pos[s])%n,p)*den%p for s in range(n)] for r in range(n)])
  A=[[(x+(1+ii)*inv(3,p)*y)%p for x,y in zip(r,s)] for r,s in zip(gs[0],gs[1])]
  C=[[(x+(1-ii)*inv(4,p)*y)%p for x,y in zip(r,s)] for r,s in zip(gs[4],gs[5])]
  da,ai=elim(A,p,True); dc,ci=elim(C,p,True); assert da and dc
  F=[[pow(z,r*s,p) for s in range(n)] for r in range(n)]
  T=mm(mm(ai,F,p),ci,p); Bs=[gs[t] for t in [2,3,6]]
  assert T==data['T'] and Bs==data['Bs']
  results['mask_reconstructions'].append({'N':n,'p':p,'det_A':da,'det_C':dc,'all_T_entries_nonzero':all(x for r in T for x in r),'matrices_match':True})
  if n<=8:
   with (OUT/f'input_N{n}_p{p}.txt').open('w') as f:
    f.write(f'{n} {p}\n'); f.write(' '.join(str(x) for M in [T]+Bs for r in M for x in r)+'\n')

for record in json.loads((ROOT/'masks/fresh_holonomy_results.json').read_text())['records']:
 n=record['N']; p=record['prime']; cycles=record['cycles']; edges=[]
 for s,c in enumerate(cycles):
  edges += [(s,c[t-1],c[t],record['integer_weights'][s][t]) for t in range(n)]
 pot=[None]*n; pot[0]=1; tree=record['tree_edges']
 while any(x is None for x in pot):
  changed=False
  for e in tree:
   s,u,v,w=edges[e]
   if pot[u] is not None and pot[v] is None: pot[v]=w*pot[u]%p; changed=True
   if pot[v] is not None and pot[u] is None: pot[u]=pot[v]*inv(w,p)%p; changed=True
  assert changed or all(x is not None for x in pot)
 cw=[w*pot[u]*inv(pot[v],p)%p for s,u,v,w in edges]
 assert [cw[:n],cw[n:]]==record['canonical_weights']
 d1,g1=cycle_green(cycles[0],cw[:n],p);d2,g2=cycle_green(cycles[1],cw[n:],p)
 M=[[(x+y)%p for x,y in zip(r,s)] for r,s in zip(g1,g2)]; dm=elim(M,p); assert dm and all(x for r in M for x in r)
 ratios=[M[0][j]*M[1][0]*inv(M[1][j]*M[0][0],p)%p for j in range(1,5)]
 jac=[]
 for j in range(1,5):
  row=[]
  for e in record['chord_edges']:
   s,u,v,w=edges[e];G=[g1,g2][s]
   row.append(sum(sign*G[a][v]*G[u][b]*inv(M[a][b],p) for sign,a,b in [(1,0,j),(1,1,0),(-1,1,j),(-1,0,0)])%p)
  jac.append(row)
 dj=elim([[row[t] for t in record['selected_chord_indices']] for row in jac],p)
 assert [d1,d2]==record['resolvent_determinants'] and dm==record['middle_sum_determinant']
 assert jac==record['jacobian'] and ratios==record['cross_ratios'] and dj==record['minor_determinant'] and dj
 results['holonomy_reconstructions'].append({'N':n,'p':p,'jacobian_determinant':dj,'det_middle':dm,'all_guards':True,'exact_match':True})
(OUT/'reviewer_controls_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'mask_reconstructions':len(results['mask_reconstructions']),'holonomy_reconstructions':len(results['holonomy_reconstructions']),'all_pass':True}))
