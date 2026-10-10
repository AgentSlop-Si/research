#!/usr/bin/env python3
"""Fresh exact Weyl tensor, factor and strengthened rational-degree controls."""
from pathlib import Path
from itertools import product,combinations
import json
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def field(n):
 assert prime_by_trial_division(n) and n%2
 for k in range(1,1000):
  p=k*n+1
  if prime_by_trial_division(p):
   for g in range(2,p):
    w=pow(g,k,p)
    if w!=1 and pow(w,n,p)==1:return p,w
 raise AssertionError

def D(n,p,w,a,b):
 mat=[[0]*n for _ in range(n)];two=pow(2,-1,n)
 for j in range(n):mat[(j+a)%n][j]=pow(w,(a*b*two+b*j)%n,p)
 return mat

def qnorm(u,n):return (u[0]**2+u[1]**2)%n
def det(u,v,n):return (u[0]*v[1]-u[1]*v[0])%n
def kap(u,v,n):return ((u[0]+u[1])*v[0]+(u[1]-u[0])*v[1])%n
def directions(n):return [(a,b) for a in range(n) for b in range(n) if a or b]
def line(n,p,w,u,t=None,s=0):
 # t is the quadratic coefficient; canonical is -||u||^2/4.
 if t is None:t=-qnorm(u,n)*pow(4,-1,n)%n
 out=[[0]*n for _ in range(n)];a,b=u;two=pow(2,-1,n)
 for m in range(n):
  for j in range(n):out[(j+m*a)%n][j]=(out[(j+m*a)%n][j]+pow(w,(t*m*m+s*m+m*m*a*b*two+m*b*j)%n,p))%p
 return out

def base_controls(n):
 p,w=field(n);f=Field(p);two=pow(2,-1,n);four=pow(4,-1,n);gamma=f.inv(n)*sum(pow(w,j*j%n,p) for j in range(n))%p;assert gamma
 F=[[pow(w,i*j%n,p) for j in range(n)] for i in range(n)];symbol={};recon=[[0]*n for _ in range(n)]
 for a,b in product(range(n),repeat=2):
  dm=D(n,p,w,-a,-b);actual=f.inv(n)*sum(dm[i][j]*F[j][i] for i in range(n) for j in range(n))%p
  expected=gamma*pow(w,(-(a*a+b*b)*four)%n,p)%p;assert actual==expected;symbol[a,b]=actual
  matrix=D(n,p,w,a,b)
  for i in range(n):
   for j in range(n):recon[i][j]=(recon[i][j]+actual*matrix[i][j])%p
 assert recon==F
 classes={'full_rank_anisotropic_lines':0,'rank_one_isotropic_lines':0,'nonvertical_fourier_equivalent_directions':0,'vertical_full_rank_directions':0};factor_checks=0
 for u in directions(n):
  a,b=u;q=qnorm(u,n);L=line(n,p,w,u)
  if not q:assert f.rank(L)==1;classes['rank_one_isotropic_lines']+=1;continue
  assert f.rank(L)==n;classes['full_rank_anisotropic_lines']+=1
  if not a:
   gm=sum(pow(w,(-j*j)%n,p) for j in range(n))%p;assert gm
   expected=[[gm*pow(w,j*j%n,p)%p if i==j else 0 for j in range(n)] for i in range(n)];classes['vertical_full_rank_directions']+=1
  else:
   inva2=pow(a,-2,n);left=-(a-b)**2*four*inva2%n;right=-(a+b)**2*four*inva2%n;slope=q*two*inva2%n;assert slope
   expected=[[pow(w,(left*i*i+slope*i*j+right*j*j)%n,p) for j in range(n)] for i in range(n)];classes['nonvertical_fourier_equivalent_directions']+=1
  assert expected==L
  for scale in (1,2,n-1):
   v=(scale*(a-b)%n,scale*(a+b)%n);assert det(u,v,n) and kap(u,v,n)==0 and kap(v,u,n)!=0
   Lv=line(n,p,w,v);assert Lv==line(n,p,w,((a-b)%n,(a+b)%n))
   actual=f.mul(L,Lv);assert all(gamma*actual[i][j]%p==F[i][j] for i in range(n) for j in range(n));factor_checks+=1
 return {'N':n,'field':p,'omega':w,'gamma':gamma,'weyl_coefficients_checked':n*n,'line_classification':classes,'all_compatible_factor_controls':factor_checks},symbol

def pair_controls(n,symbol):
 p,w=field(n);f=Field(p);two=pow(2,-1,n);hist={};ind=0;cocycle_checks=0
 for u in directions(n):
  for v in directions(n):
   if not det(u,v,n):continue
   ind+=1;sigma=(u[1]*v[0]-u[0]*v[1])%n
   # Explicit matrix multiplication validates sign and ordering conventions.
   left=f.mul(D(n,p,w,*u),D(n,p,w,*v));right=D(n,p,w,(u[0]+v[0])%n,(u[1]+v[1])%n);phase=pow(w,sigma*two%n,p)
   assert all(left[i][j]==phase*right[i][j]%p for i in range(n) for j in range(n));cocycle_checks+=1
   T=[[symbol[(m*u[0]+ell*v[0])%n,(m*u[1]+ell*v[1])%n]*pow(w,(-sigma*m*ell*two)%n,p)%p for ell in range(n)] for m in range(n)]
   actual=f.rank(T);assert actual==(1 if kap(u,v,n)==0 else n);hist[actual]=hist.get(actual,0)+1
   if actual==1:
    assert qnorm(u,n) and any(v==(scale*(u[0]-u[1])%n,scale*(u[0]+u[1])%n) for scale in range(1,n))
 assert ind==(n*n-1)*(n*n-n)
 return {'N':n,'independent_vector_pairs':ind,'rank_histogram':hist,'cocycle_matrix_checks':cocycle_checks,'independent_projective_line_pairs':ind//((n-1)**2),'compatible_projective_line_pairs':hist[1]//((n-1)**2)}

def stronger_degree_controls():
 out=[]
 for n in (3,5,7,11,13,17,19):
  p,w=field(n);f=Field(p);cases=0
  for q in (1,2,n-1):
   chirp=[pow(w,(-q*m*m*pow(4,-1,n))%n,p) for m in range(n)]
   for d in range(n-1):
    for e in range(n-1-d):
     # Tail zero equations for q_den(C)L=p(C); test absence of a nonzero denominator.
     rows=[[chirp[(r-k)%n] for k in range(d+1)] for r in range(e+1,n)]
     assert f.rank(rows)==d+1;cases+=1
   # Tight e=0 control: inverse cyclic polynomial has all N coefficients nonzero.
   circ=[[chirp[(i-j)%n] for j in range(n)] for i in range(n)];inv=f.inverse(circ);coeff=[inv[i][0] for i in range(n)];assert all(coeff)
   conv=[sum(coeff[k]*chirp[(r-k)%n] for k in range(n))%p for r in range(n)];assert conv==[1]+[0]*(n-1)
  out.append({'N':n,'tail_constraint_full_column_rank_checks':cases,'tight_constant_numerator_degree':n-1})
 return out

def arbitrary_quadratic_controls():
 # More factors of the same full quadratic-chirp kind still expose Fourier-equivalent factors.
 out=[]
 for n in (3,5,7):
  p,w=field(n);f=Field(p);count=0
  for u in directions(n):
   a,b=u
   for t in range(n):
    for s in (0,1):
     L=line(n,p,w,u,t,s);assert f.rank(L)==(1 if t==0 else n)
     if a:
      ai=pow(a,-1,n);two=pow(2,-1,n);left=(t*ai*ai+b*ai*two)%n;right=(t*ai*ai-b*ai*two)%n;slope=(-2*t*ai*ai)%n
      expected=[[pow(w,(left*i*i+right*j*j+slope*i*j+s*ai*(i-j))%n,p) for j in range(n)] for i in range(n)];assert L==expected
     count+=1
  out.append({'N':n,'quadratic_and_linear_phase_line_controls':count})
 return out

if __name__=='__main__':
 src=json.loads((BASE/'sources/results.json').read_text());base=[];pairs=[]
 for n in (3,5,7,11,13,17,19):
  r,symbol=base_controls(n);base.append(r)
  if n in (3,5,7):pairs.append(pair_controls(n,symbol))
  saved=next((r for r in src['line_classification'] if r['N']==n),None)
  if saved:
   assert saved['field']==r['field']
   for key,v in r['line_classification'].items():assert saved[key]==v
  print('N',n,'all factor controls PASS',flush=True)
 for saved in src['rank_dichotomy']:
  r=next(r for r in pairs if r['N']==saved['N']);assert r['independent_vector_pairs']==saved['independent_pairs'] and {str(k):v for k,v in r['rank_histogram'].items()}==saved['rank_histogram']
 degrees=stronger_degree_controls();quad=arbitrary_quadratic_controls()
 result={'status':'PASS','base':base,'exhaustive_pairs':pairs,'stronger_degree_controls':degrees,'additional_quadratic_line_controls':quad,'source_programs_executed':False,'scope':'Odd-prime fixed ordered Weyl-line pairs; full quadratic chirp factors and local rational degree; no general FFT lower bound'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS all tensor, factor, degree and quadratic extension controls',flush=True)
