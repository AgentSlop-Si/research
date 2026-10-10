#!/usr/bin/env python3
"""Own unbounded-integer congruence and modular outer-elimination audit."""
from pathlib import Path
import gzip,json,hashlib,random
from fractions import Fraction
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent;N=256

def affine(cols):
 p=[]
 for i in range(1<<len(cols)):
  v=0
  for j,c in enumerate(cols):
   if i&(1<<j):v^=c
  p.append(v)
 assert sorted(p)==list(range(len(p)));return p

def inverse(p):
 q=[0]*len(p)
 for i,v in enumerate(p):q[v]=i
 return q

def build_edges(ps):
 order=list(range(N));edges=[]
 for stage in range(4):
  edges += list(zip(order[:-1],order[1:]))
  if stage<3:order=[order[v] for v in ps[stage]]
 return edges

def spectral(ps,layout):
 edges=build_edges(ps);assert len(edges)==1020 and all(i!=j for i,j in edges)
 L=[[0]*N for _ in range(N)]
 for i,j in edges:L[i][i]+=1;L[j][j]+=1;L[i][j]-=1;L[j][i]-=1
 assert all(sum(r)==0 for r in L) and sum(L[i][i] for i in range(N))==2040
 data=json.loads(gzip.decompress((BASE/'sources/INTEGER_CONGRUENCE_CERTIFICATE.json.gz').read_bytes()))
 assert (data['N'],data['shift_num'],data['shift_den'])==(256,101,50)
 T=data['T'];assert len(T)==N and all(len(r)==N and all(type(v) is int for v in r) for r in T)
 assert all(T[i][j]==0 for i in range(N) for j in range(i)) and all(T[i][i]!=0 for i in range(N))
 M=[[50*L[i][j]-101*int(i==j)+50 for j in range(N)] for i in range(N)]
 assert all(sum(r)==12699 for r in M)
 # Sparse-L action plus exact rank-one J action; Python integers throughout.
 cols=list(map(list,zip(*T)));sums=[sum(c) for c in cols]
 neighbours=[[(j,v) for j,v in enumerate(row) if v] for row in L]
 MT=[[50*sum(v*T[j][k] for j,v in neighbours[i])-101*T[i][k]+50*sums[k] for k in range(N)] for i in range(N)]
 mtcols=list(zip(*MT));H=[[sum(a*b for a,b in zip(tcol,mtcol)) for mtcol in mtcols] for tcol in cols]
 assert all(H[i][j]==H[j][i] for i in range(N) for j in range(N))
 margins=[H[i][i]-sum(abs(H[i][j]) for j in range(N) if i!=j) for i in range(N)]
 assert min(margins)==4681152 and min(H[i][i] for i in range(N))==16706411 and all(m>0 for m in margins)
 nnz=sum(v!=0 for r in T for v in r);ma=max(abs(v) for r in T for v in r);assert (nnz,ma)==(32264,1416)
 bound=max(sum(abs(v) for v in r) for r in M)*ma*max(sum(abs(v) for v in c) for c in cols);assert bound==1379922104160 and bound<2**62
 # All diagonal entries and 29 prescribed mixed entries independently via edge quadratic forms.
 checks={(i,i) for i in range(N)}|{(0,0),(1,10),(17,103),(201,221),(255,255)}|{((i*37+11)%N,(i*83+57)%N) for i in range(24)}
 for a,b in checks:
  u,v=cols[a],cols[b];manual=50*sum((u[i]-u[j])*(v[i]-v[j]) for i,j in edges)-101*sum(x*y for x,y in zip(u,v))+50*sum(u)*sum(v)
  assert manual==H[a][b]
 lower=[]
 for a in range(1,N):
  ray=Fraction(101*a*(N-a),50*N);assert ray>min(a,N-a);lower.append(ray.numerator//ray.denominator+1)
 assert lower[127]==130
 # Explicit consistency check against the previously excluded five-Toffoli layout.
 edited=[p[:] for p in ps]
 for g in layout['toffoli_gate_sequence_in_shuffle_2']:
  gate=[i^(1<<g['target']) if all(i&(1<<c) for c in g['controls']) else i for i in range(N)]
  edited[2]=[edited[2][v] for v in gate]
 A={i for i in range(N) if (i&112).bit_count()%2==0};editedcut=sum((i in A)!=(j in A) for i,j in build_edges(edited));assert editedcut==124
 digest=hashlib.sha256(json.dumps(H,separators=(',',':')).encode()).hexdigest()
 print('Full unbounded-integer positive-definiteness certificate PASS',flush=True)
 return {'status':'PASS','all_H_entries_computed_with_unbounded_integers':N*N,'independent_edge_form_entries':len(checks),'H_sha256':digest,'path_edges':len(edges),'T_nonzero_entries':nnz,'T_max_abs':ma,'min_diagonal':min(H[i][i] for i in range(N)),'all_dominance_margins':margins,'min_margin':min(margins),'source_int64_bound':bound,'certified_lambda2_strict_lower_bound':'101/50','minimum_balanced_boundary':130,'cardinality_boundary_lower_bounds':lower,'edited_five_Toffoli_cut':editedcut,'edited_lambda2_upper_bound':'31/16'}

def primitive(p):
 assert prime_by_trial_division(p) and (p-1)%N==0
 for g in range(2,p):
  w=pow(g,(p-1)//N,p)
  if pow(w,N//2,p)!=1:return w
 raise AssertionError

def apply_separated(params,M,p):
 a,b,c,e,d=params;cols=len(M[0]);out=[[0]*cols for _ in range(N)];prefix=[0]*cols
 for i in range(N):
  out[i]=[(a[i]*prefix[k]+d[i]*M[i][k])%p for k in range(cols)]
  prefix=[(prefix[k]+b[i]*M[i][k])%p for k in range(cols)]
 suffix=[0]*cols
 for i in range(N-1,-1,-1):
  out[i]=[(out[i][k]+c[i]*suffix[k])%p for k in range(cols)]
  suffix=[(suffix[k]+e[i]*M[i][k])%p for k in range(cols)]
 return out

def upper_sum(M,p):
 out=[];acc=[0]*len(M[0])
 for row in reversed(M):acc=[(a+b)%p for a,b in zip(acc,row)];out.append(acc[:])
 return out[::-1]
def cumulative_columns(M,p):
 out=[]
 for row in M:
  acc=0;r=[]
  for v in reversed(row):acc=(acc+v)%p;r.append(acc)
  out.append(r[::-1])
 return out

def coefficients(ps):
 saved=json.loads((BASE/'sources/FOURIER_COMPATIBILITY_CERTIFICATES.json').read_text());p1,p2,p3=ps;i3=inverse(p3);i1=inverse(p1)
 C=[i for i in range(N) if not i&64];R=[i for i in range(N) if p2[i]&64]
 assert R[:17]==saved['first17_rows'] and C[:17]==saved['first17_cols'] and len(R)==len(C)==128
 g=[not i&64 for i in range(N)];pulled=[g[p2[i]] for i in range(N)]
 bc=sum(g[i]!=g[i+1] for i in range(N-1));br=sum(pulled[i]!=pulled[i+1] for i in range(N-1));assert (bc,br)==(3,13)
 records=[]
 for p in (12289,65537):
  f=Field(p);w=primitive(p);powers=[pow(w,i,p) for i in range(N)];F=[[powers[i*j%N] for j in range(N)] for i in range(N)]
  H0=[[F[i3[i]][p1[j]] for j in range(N)] for i in range(N)]
  full=f.rank([[H0[i][j] for j in C] for i in R]);det17=f.det([[H0[i][j] for j in C[:17]] for i in R[:17]])
  source=next(r for r in saved['prime_controls'] if r['p']==p);assert full==128 and det17==source['first17_minor_determinant_mod_p'] and det17
  rng=random.Random(26670101);params2=[[rng.randrange(p) for i in range(N)] for _ in range(5)];params3=[[rng.randrange(p) for i in range(N)] for _ in range(5)]
  S2=apply_separated(params2,f.eye(N),p);H=apply_separated(params3,[S2[v] for v in p2],p)
  mr=f.rank([[H[i][j] for j in C] for i in R]);assert mr==16
  zero=[[int(p2[i]==j) for j in C] for i in R];assert f.rank(zero)==0
  # Fresh exact full product. S4 is upper unit all-ones, S1 lower unit all-ones.
  routed=[[H[p3[i]][i1[j]] for j in range(N)] for i in range(N)]
  complete=cumulative_columns(upper_sum(routed,p),p)
  # C4=I-upper_shift and C1=I-lower_shift cancel those factors exactly.
  left=[[(complete[i][j]-(complete[i+1][j] if i+1<N else 0))%p for j in range(N)] for i in range(N)]
  both=[[(left[i][j]-(left[i][j+1] if j+1<N else 0))%p for j in range(N)] for i in range(N)]
  recovered=[[both[i3[i]][p1[j]] for j in range(N)] for i in range(N)];assert recovered==H
  # The same nontrivial, invertible outer inverse stages need not satisfy the Fourier constraints.
  leftF=[[(F[i][j]-(F[i+1][j] if i+1<N else 0))%p for j in range(N)] for i in range(N)]
  transformed=[[(leftF[i][j]-(leftF[i][j+1] if j+1<N else 0))%p for j in range(N)] for i in range(N)]
  candidate=[[transformed[i3[i]][p1[j]] for j in range(N)] for i in range(N)];candidate_rank=f.rank([[candidate[i][j] for j in C] for i in R]);assert candidate_rank>16
  records.append({'prime':p,'primitive_root':w,'identity_outer_selected_rank':full,'first17_determinant':det17,'fresh_valid_middle_rank':mr,'zero_generator_middle_rank':0,'fresh_full_product_elimination_entries':N*N,'fresh_nontrivial_outer_candidate_rank':candidate_rank})
  print('Exact coefficient gate and full synthetic product PASS over',p,flush=True)
 return {'boundaries':[bc,br],'middle_rank_bound':16,'first17_rows':R[:17],'first17_columns':C[:17],'field_controls':records,'minor_degrees_in_matrix_entries':{'C1':17,'C4':17,'total':34},'scope':'Necessary constraints on inverse outer stages, no feasibility decision'}

if __name__=='__main__':
 layout=json.loads((BASE/'sources/AFFINE_LAYOUT.json').read_text());assert layout['k']==8;ps=[affine(c) for c in layout['affine_shuffle_columns']];assert len(ps)==3
 result={'status':'PASS','spectral':spectral(ps,layout),'coefficient_gate':coefficients(ps),'source_programs_executed':False,'arithmetic':'Python arbitrary-precision integers and exact modular arithmetic'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
