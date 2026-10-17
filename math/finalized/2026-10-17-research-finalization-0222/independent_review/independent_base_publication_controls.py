"""Fresh direct convolution/interpolation, Fourier and heavy-budget controls."""
from fractions import Fraction as F
import itertools,math,json
from pathlib import Path

def inv(A):
 n=len(A);B=[[F(z) for z in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
 for k in range(n):
  q=next(i for i in range(k,n) if B[i][k]);B[k],B[q]=B[q],B[k]
  v=B[k][k];B[k]=[z/v for z in B[k]]
  for i in range(n):
   if i!=k:
    v=B[i][k];B[i]=[a-v*b for a,b in zip(B[i],B[k])]
 return [row[n:] for row in B]
base_cases=0;basis_cases=0;coeff_bounds=0
for M in range(2,9):
 r=2*M-1;ell=(r-1).bit_length();D=math.factorial(r-1);K=(r-1)*(ell+1)+1
 J=inv([[t**i for i in range(r)] for t in range(r)])
 coeff=[[v*D for v in row] for row in J]
 assert all(v.denominator==1 and abs(v)<2**K for row in coeff for v in row); coeff_bounds+=r*r
 for i,j in itertools.product(range(M),repeat=2):
  z=[t**(i+j) for t in range(r)];s=[sum(a*b for a,b in zip(row,z)) for row in J]
  assert s==[int(k==i+j) for k in range(r)];basis_cases+=1
 for m,d in itertools.product(range(2,8),range(1,4)):
  Q=((1<<m)-1)**d;R=Q**M;h=(R-1).bit_length();H=h+(M-1).bit_length()+(M-1)*ell+1;B=2*H+K+(r-1).bit_length()+2
  patterns=[[0]*M,[R-1]*M,[((i+2)**3)%(R) for i in range(M)]]
  for x,y in itertools.product(patterns,repeat=2):
   u=[sum(v*t**i for i,v in enumerate(x)) for t in range(r)];v=[sum(a*t**i for i,a in enumerate(y)) for t in range(r)]
   assert all(z<2**H for z in u+v)
   z=[a*b for a,b in zip(u,v)];b=[sum(a*q for a,q in zip(row,z)) for row in coeff]
   assert all(a.denominator==1 and abs(a)<2**B and a%D==0 for a in b)
   s=[int(a/D) for a in b];direct=[sum(x[i]*y[k-i] for i in range(M) if 0<=k-i<M) for k in range(r)]
   assert s==direct
   assert sum(a*R**i for i,a in enumerate(s))==sum(a*R**i for i,a in enumerate(x))*sum(a*R**i for i,a in enumerate(y));base_cases+=1
heavy_cases=0;needs_one=0
for M,Q in [(2,2),(4,2),(4,4),(8,4)]:
 for profile in itertools.product(range(M+1),repeat=Q):
  for budget in range(Q*M+1):
   a=max(1,(budget+Q-1)//Q);B=min(M//2,a*(M.bit_length()-1));total=heavy=0;rejected=False
   for support in profile:
    total+=support;heavy+=support>B
    if total>budget:rejected=True;break
   cap=budget//(B+1)
   assert heavy<=cap+int(rejected)
   needs_one+=heavy>cap;heavy_cases+=1
fourier_cases=0;outputs=0;offgrid=0
p=97
for N in (4,8,16,32):
 Q=1<<((N.bit_length()-1)//2);M=N//Q
 w=next(z for z in range(2,p) if pow(z,N,p)==1 and pow(z,N//2,p)!=1)
 eta=pow(w,Q,p);theta=pow(w,M,p)
 for seed in range(1,11):
  a=[[(seed+3*t+7*h)**2%p if (h+t+seed)%3 else 0 for h in range(M)] for t in range(Q)]
  x=[0]*N
  for t in range(Q):
   for u in range(M):x[t+Q*u]=sum(a[t][h]*pow(eta,(-h*u)%M,p) for h in range(M))%p
  direct=[sum(x[j]*pow(w,j*k,p) for j in range(N))%p for k in range(N)]
  formula=[0]*N
  for h in range(M):
   for v in range(Q):formula[h+M*v]=M*sum(a[t][h]*pow(w,h*t,p)*pow(theta,v*t,p) for t in range(Q))%p
  assert direct==formula;fourier_cases+=1;outputs+=N
  z=next(z for z in range(p) if pow(z,M,p)!=1)
  for u in range(M):
   g=sum(pow(z,h,p)*pow(eta,u*h,p) for h in range(M))%p
   assert g and g==(1-pow(z,M,p))*pow((1-z*pow(eta,u,p))%p,-1,p)%p;offgrid+=1
out={'base_exact_full_products':base_cases,'base_basis_pair_outputs':basis_cases,'decoder_coefficients_bounded':coeff_bounds,'heavy_budget_profiles':heavy_cases,'profiles_requiring_final_heavy_allowance':needs_one,'fourier_factorization_cases':fourier_cases,'fourier_outputs':outputs,'nonzero_offgrid_coefficients':offgrid,'scope':'Fresh independent arithmetic and invoice controls only, not historical replay or performance evidence.'}
Path(__file__).with_name('INDEPENDENT_BASE_PUBLICATION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
