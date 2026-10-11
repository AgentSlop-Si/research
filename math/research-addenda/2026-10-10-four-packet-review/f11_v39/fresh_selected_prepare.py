import pathlib,json,numpy as np,hashlib,math,collections
ROOT=pathlib.Path(__file__).resolve().parent;PACK=ROOT/'inert_packet/fft_transfer_quartic_circuit_v39'
P=json.loads((ROOT/'paths.json').read_text());selected=sorted(range(121),key=lambda i:(len(P[i]),i))[:78]
q=json.loads((PACK/'quartic_results.json').read_text());basis=json.loads((PACK/'transcendence_basis.json').read_text());jac=json.loads((PACK/'v38_jacobian_certificate.json').read_text());tangent=json.loads((PACK/'circuit_results.json').read_text())
assert selected==q['selected_ids']==tangent['selected_ids'];assert selected[:77]==basis['row_coordinate_ids']
z=np.load(PACK/'quartic_pivots.npz',allow_pickle=False);assert sorted(z.files)==['pivot_hi','pivot_lo','rounds'];n=math.comb(81,4)
for name,dt in [('rounds','i1'),('pivot_hi','<u4'),('pivot_lo','<u8')]:
 arr=z[name];assert arr.shape==(n,) and arr.dtype==np.dtype(dt)
 arr.tofile(ROOT/(name+'.bin'))
digest=hashlib.sha256(z['rounds'].tobytes()+z['pivot_hi'].tobytes()+z['pivot_lo'].tobytes()).hexdigest();assert digest==q['pivots_sha256']
assert dict(collections.Counter(z['rounds'].tolist()))=={0:1634924,1:28756,2:60}
(ROOT/'selected_paths.txt').write_text('\n'.join(str(len(P[i]))+' '+' '.join(str(e) for path in P[i] for e in path) for i in selected)+'\n')
prime=jac['prime'];w=jac['edge_weights'];assert prime==1000003 and len(w)==99 and all(0<x<prime for x in w)
J=[]
for ps in P:
 row=[0]*99
 for path in ps:
  for k,e in enumerate(path):row[e]=(row[e]+math.prod(w[f] for t,f in enumerate(path) if t!=k))%prime
 J.append(row)
def rankdet(rows):
 A=[row[:] for row in rows];nr=len(A);nc=len(A[0]);rank=0;det=1
 for col in range(nc):
  choices=[r for r in range(rank,nr) if A[r][col]]
  if not choices:continue
  r=choices[0]
  if r!=rank:A[r],A[rank]=A[rank],A[r];det=-det
  pivot=A[rank][col];det=det*pivot%prime;v=pow(pivot,-1,prime)
  for k in range(col,nc):A[rank][k]=A[rank][k]*v%prime
  for r in range(rank+1,nr):
   f=A[r][col]
   if f:
    for k in range(col,nc):A[r][k]=(A[r][k]-f*A[rank][k])%prime
  rank+=1
  if rank==nr:break
 return rank,det if nr==nc and rank==nr else None
cols=basis['selected_77_edge_columns'];assert len(cols)==len(set(cols))==77 and all(0<=x<99 for x in cols)
r,d=rankdet([[J[i][j] for j in cols] for i in selected[:77]]);assert (r,d)==(77,556448)
full_rank,_=rankdet(J);assert full_rank==77
v=tangent['normalized_nullvector'];assert len(v)==78 and sum(x!=0 for x in v)==76
assert all(sum(v[t]*J[i][j] for t,i in enumerate(selected))%prime==0 for j in range(99))
# Independent gauge-column construction over the same field.
L=json.loads((PACK/'topology_11.json').read_text())['layers'];G=[]
for lev in range(2):
 for vertex in range(11):
  g=[0]*99
  for layer in range(3):
   for k,(dst,src) in enumerate(L[layer]):
    if layer==lev and dst==vertex:g[33*layer+k]+=w[33*layer+k]
    if layer==lev+1 and src==vertex:g[33*layer+k]-=w[33*layer+k]
  g=[x%prime for x in g];assert all(sum(a*b for a,b in zip(row,g))%prime==0 for row in J);G.append(g)
assert rankdet(G)[0]==22
res={'selected_ids':selected,'coordinates':78,'columns':n,'unit_pivot_array_digest':digest,'npz_object_loading':False,'rounds':{str(k):int(v) for k,v in collections.Counter(z['rounds'].tolist()).items()},'jacobian':{'prime':prime,'selected_basis_rows':77,'minor_determinant':d,'full_rank':full_rank,'gauge_independent_vectors':22,'all_gauge_vectors_annihilated':True,'sampled_tangent_support':76,'sampled_tangent_nullvector_checked':True}}
(ROOT/'selected_preparation.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
