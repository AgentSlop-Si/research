"""Fresh construction of the Phase40 common integer graph and derivative witnesses."""
from pathlib import Path
import json,random
from fresh_reconstruct import inverse,mm,rankdet,FIELDS
ROOT=Path(__file__).resolve().parent
saved=json.loads((ROOT/'phase40_source/phase40_jacobian_certificates.json').read_text())
records=[]
for case in saved['cases']:
 n=case['N'];r=random.Random(40040+n);c=list(range(n));r.shuffle(c);cycles=[list(range(n)),c]
 r=random.Random(40040+7919+n);integer_weights=[[r.randrange(2,100000) for j in range(n)] for s in range(2)]
 for p,g,_ in FIELDS:
  # The source's conditional mod-p branch must not change the underlying integer example.
  for weights in integer_weights:
   h=1
   for w in weights:h=h*w%p
   assert h!=1
  # The first n-1 listed edges of the natural first cycle form a spanning tree.
  D=[1]*n
  for j in range(1,n-1):D[j]=D[j-1]*integer_weights[0][j]%p
  D[n-1]=pow(integer_weights[0][0],-1,p)
  norm=[]
  for cy,weights in zip(cycles,integer_weights):norm.append([w*D[cy[j-1]]*pow(D[cy[j]],-1,p)%p for j,w in enumerate(weights)])
  assert norm[0][:-1]==[1]*(n-1)
  greens=[];resolvent_dets=[]
  for cy,weights in zip(cycles,norm):
   H=[[int(i==j) for j in range(n)] for i in range(n)]
   for j,w in enumerate(weights):H[cy[j]][cy[j-1]]=(H[cy[j]][cy[j-1]]-w)%p
   G,det=inverse(H,p);greens.append(G);resolvent_dets.append(det)
  M=[[(a+b)%p for a,b in zip(r,s)] for r,s in zip(*greens)]
  Mi,mdet=inverse(M,p);assert all(x for row in M for x in row)
  ratios=[M[0][j]*M[1][0]*pow(M[1][j]*M[0][0]%p,-1,p)%p for j in range(1,5)]
  J=[]
  for j in range(1,5):
   row=[]
   for edge in range(n-1,2*n):
    s,k=divmod(edge,n);v=cycles[s][k];u=cycles[s][k-1];G=greens[s]
    # dM=G E_vu G, independently from inverse-matrix differentiation.
    terms=[(0,j,1),(1,0,1),(1,j,-1),(0,0,-1)]
    row.append(sum(sign*G[a][v]*G[u][b]*pow(M[a][b],-1,p) for a,b,sign in terms)%p)
   J.append(row)
  selected=[[row[k] for k in case['chord_indices']] for row in J]
  rank,order,det=rankdet(selected,p)
  # rankdet returns determinant in pivot-row order; correct to natural order.
  sign=(-1)**sum(order[i]>order[j] for i in range(4) for j in range(i+1,4));det=det*sign%p
  assert rank==4 and det==case['modular_determinants'][str(p)]
  records.append(dict(N=n,prime=p,cycles=cycles,integer_weights=integer_weights,tree_edges=list(range(n-1)),chord_edges=list(range(n-1,2*n)),canonical_weights=norm,all_edge_weights_nonzero=True,resolvent_determinants=resolvent_dets,middle_sum_determinant=mdet,all_middle_sum_entries_nonzero=True,cross_ratios=ratios,jacobian=J,selected_chord_indices=case['chord_indices'],minor_determinant=det,source_minor_match=True))
(ROOT/'fresh_holonomy_results.json').write_text(json.dumps({'records':records,'strengthening':'Local dominance holds on the admissible open subchart with both resolvents defined and the entire middle sum invertible and entrywise nonzero. No specific Fourier fiber or unit-modulus solution follows.'},indent=2)+'\n')
print(json.dumps({'cases':len(records),'all_source_minors_match':True,'all_middle_sums_invertible_and_entrywise_nonzero':True}))
