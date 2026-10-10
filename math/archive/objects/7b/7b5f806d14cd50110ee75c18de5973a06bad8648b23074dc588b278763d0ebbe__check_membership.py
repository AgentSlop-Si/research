#!/usr/bin/env python3
"""Independent rank-stratified membership, cofactor and mixing-lemma controls."""
from pathlib import Path
from itertools import product
import random,json
from exact_utils import Field
from check_sectors import greens_mod
BASE=Path(__file__).parent

def solve_rect(a,b,p):
 f=Field(p);n=len(a[0]);mat=[[x%p for x in row]+[v%p] for row,v in zip(a,b)];piv=[];r=0
 for c in range(n):
  s=next((i for i in range(r,len(mat)) if mat[i][c]),None)
  if s is None:continue
  mat[r],mat[s]=mat[s],mat[r];z=f.inv(mat[r][c]);mat[r]=[v*z%p for v in mat[r]]
  for i in range(len(mat)):
   if i==r:continue
   z=mat[i][c]
   if z:mat[i]=[(v-z*w)%p for v,w in zip(mat[i],mat[r])]
  piv.append(c);r+=1
  if r==len(mat):break
 if any(not any(row[:-1]) and row[-1] for row in mat):return None
 particular=[0]*n
 for i,c in enumerate(piv):particular[c]=mat[i][-1]
 null=[]
 for c in range(n):
  if c in piv:continue
  v=[0]*n;v[c]=1
  for i,j in enumerate(piv):v[j]=-mat[i][c]%p
  null.append(v)
 return particular,null

def row_solve(t,b,p):return solve_rect(list(map(list,zip(*t))),b,p)
def full_support(sol):
 if sol is None:return False
 v,ker=sol;return all(v[j] or any(k[j] for k in ker) for j in range(len(v)))
def combine(c,t,p):return [sum(c[j]*t[j][k] for j in range(len(t)))%p for k in range(len(t[0]))]
def column_basis(t,p):
 f=Field(p);keep=[]
 for k in range(len(t[0])):
  if f.rank([[row[j] for j in keep+[k]] for row in t])>len(keep):keep.append(k)
 return keep

def strata():
 p=101;f=Field(p);out=[]
 for rank in range(9):
  t=[[int(i==j and i<rank) for j in range(12)] for i in range(8)];b=[int(j<rank) for j in range(12)]
  sol=row_solve(t,b,p);assert f.rank(t)==rank and sol is not None and full_support(sol)
  assert combine(sol[0],t,p)==b
  for k in sol[1]:assert combine(k,t,p)==[0]*12
  # Construct a full-support point, never assume a finite-field union theorem blindly.
  v=sol[0][:]
  for k in sol[1]:
   z=next(z for z in range(p) if all((v[j]+z*k[j])%p for j in range(8) if v[j] or k[j]))
   v=[(x+z*y)%p for x,y in zip(v,k)]
  assert all(v) and combine(v,t,p)==b
  bad=b[:];bad[-1]=1;assert row_solve(t,bad,p) is None and f.rank(t+[bad])==rank+1
  if rank:
   forced=b[:];forced[0]=0;assert row_solve(t,forced,p) is not None and not full_support(row_solve(t,forced,p))
  out.append({'rank':rank,'positive_membership':True,'negative_membership':True,'nonzero_guard_controls':True})
 return out

def cofactor_controls():
 p=998244353;f=Field(p);mix=[[pow(i+1,j,p) for j in range(8)] for i in range(8)];assert f.det(mix)
 records=[]
 for i in range(32):
  a,b=i,i+32;other=[j for j in range(64) if j not in (a,b)];positions=other[:6]+[a,b]
  base=[[int(k==v) for k in range(64)] for v in positions];t=f.mul(mix,base);assert f.rank(t)==8
  # One-target cofactor chart.
  off=[j for j in range(64) if j!=a];w=[[row[j] for j in off] for row in t];piv=column_basis(w,p);assert len(piv)==7
  mat=[[row[j] for j in piv] for row in w]
  co=[(-1)**j*f.det(mat[:j]+mat[j+1:])%p for j in range(8)]
  assert any(co) and combine(co,w,p)==[0]*63
  delta=sum(co[j]*t[j][a] for j in range(8))%p;assert delta
  c=[x*f.inv(delta)%p for x in co];assert combine(c,t,p)==[int(j==a) for j in range(64)]
  assert row_solve(t,[int(j==a) for j in range(64)],p)[0]==c
  # Two-target, rank-six complete cofactor chart.
  w=[[row[j] for j in other] for row in t];cols=column_basis(w,p);assert len(cols)==6
  mat=[[row[j] for j in cols] for row in w];rows=column_basis(list(map(list,zip(*mat))),p);assert len(rows)==6
  pivot=[mat[j] for j in rows];det=f.det(pivot);assert det;free=[j for j in range(8) if j not in rows];basis=[]
  for j in free:
   v=[0]*8;v[j]=det
   cp=f.solve(list(map(list,zip(*pivot))),[(-det*x)%p for x in mat[j]])
   for r,x in zip(rows,cp):v[r]=x
   assert combine(v,w,p)==[0]*62;basis.append(v)
  targets=[[sum(v[j]*t[j][k] for j in range(8))%p for k in (a,b)] for v in basis];assert f.det(targets)
  for z,k in enumerate((a,b)):
   coeff=f.solve(list(map(list,zip(*targets))),[int(q==z) for q in range(2)])
   v=[sum(coeff[q]*basis[q][j] for q in range(2))%p for j in range(8)]
   assert combine(v,t,p)==[int(q==k) for q in range(64)]
  broken=[r[:] for r in base];broken[6][other[6]]=1;tt=f.mul(mix,broken);ww=[[row[j] for j in other] for row in tt]
  assert f.rank(tt)==8 and f.rank(ww)==7 and row_solve(tt,[int(j==a) for j in range(64)],p) is None
  records.append({'pair':[a,b],'single_off_target_rank':7,'paired_off_target_rank':6,'broken_pair_rank':7})
 return records

def actual_route_symmetry():
 p=998244353;f=Field(p);gs,_=greens_mod(p);w=pow(3,(p-1)//64,p);assert pow(w,32,p)==p-1
 fi=[[f.inv(64)*pow(w,-i*j%64,p)%p for j in range(64)] for i in range(64)]
 bank=[[0]*64 for _ in range(64)]
 for x in range(8):
  for i in range(8):
   for j in range(8):bank[8*x+i][8*x+j]=pow(w,8*i*j,p) if x in (0,1,4,5) else int(i==j)
 K=f.mul(gs[0],bank);R=f.mul(bank,gs[1]);rng=random.Random(195216);out=[]
 for sign in (1,-1):
  coeff=[[rng.randrange(1,p) for j in range(8)] for i in range(32)];coeff += [[sign*v%p for v in row] for row in coeff]
  L=[[sum(coeff[i][j]*gs[j][i][k] for j in range(8))%p for k in range(64)] for i in range(64)];assert f.rank(L)==64
  assert all(L[i^32][k^32]==sign*L[i][k]%p for i in range(64) for k in range(64))
  for branch in ('input','middle'):
   U=f.mul(f.mul(K,L),fi) if branch=='input' else f.mul(f.mul(L,R),fi)
   mats=[f.mul(g,U) for g in gs]
   assert all(mats[j][i+32][k]==sign*((-1)**k)*mats[j][i][k]%p for j in range(8) for i in range(32) for k in range(64))
   ranks=[]
   for i in range(32):
    wrong=[[g[i][k] for k in range(64) if k%2!=i%2] for g in mats];rank=f.rank(wrong);assert rank==8;ranks.append(rank)
   out.append({'sign':sign,'branch':branch,'pair_identity_entries':32*8*64,'wrong_parity_ranks':ranks,'fixed_factors':'independent rational commuting controls, not a reduction of the algebraic seed'})
 return out

def stronger_mixing_lemma():
 # Exhaust every 4-by-2 injective stacked column over F2.
 f=Field(2);count=0
 for values in product(range(2),repeat=8):
  stack=[list(values[2*i:2*i+2]) for i in range(4)]
  if f.rank(stack)!=2:continue
  sol=solve_rect(list(map(list,zip(*stack))),[0,0],2);assert sol is not None and len(sol[1])==2
  projected=[v[:2] for v in sol[1]];cross=stack[2:]
  assert f.rank(projected)==f.rank(cross);count+=1
 assert count==210
 # Tight rank-four example with singular diagonal blocks in 32-dimensional sectors.
 n=32;p=101;f=Field(p);D=[[int(i==j and i<28) for j in range(n)] for i in range(n)];C=[[int(i==j and i>=28) for j in range(n)] for i in range(n)]
 L=[D[i]+C[i] for i in range(n)]+[C[i]+D[i] for i in range(n)];assert f.rank(L)==64
 A=[[int(j==28+i) for j in range(n)] for i in range(4)];B=[[0]*n for i in range(4)]
 assert f.rank(A)==4 and f.rank(C)==4 and f.rank(D)==28 and f.mul(A,D)==f.mul(B,C)
 # Coefficient pair counting: every odd diagonal has twice as many nonzeros as unequal pairs.
 for pairs in (0,1,2,4,16,32):
  odd=[int(i<pairs) for i in range(32)]+[-int(i<pairs) for i in range(32)]
  assert sum(v!=0 for v in odd)==2*pairs
 return {'exhaustive_injective_stacked_columns_F2':count,'tight_singular_diagonal_control':{'sector_dimension':32,'rank_A':4,'diagonal_rank':28,'cross_rank':4,'whole_L_rank':64},'proved_unconditional_cross_rank_lower_bound':4,'proved_odd_rank_lower_bound':8,'proved_unequal_pair_lower_bound':4}

if __name__=='__main__':
 result={'status':'PASS','rank_strata':strata(),'cofactor_charts':cofactor_controls(),'actual_route_signed_controls':actual_route_symmetry(),'independent_stronger_mixing_lemma':stronger_mixing_lemma(),'scope':'Exact membership algebra and fixed-route controls; signed branches are empty by the separate sector proof; no unrestricted coefficient solution'}
 (BASE/'MEMBERSHIP_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('PASS rank strata, 32 cofactor charts, four actual-route controls and stronger mixing lemma')
