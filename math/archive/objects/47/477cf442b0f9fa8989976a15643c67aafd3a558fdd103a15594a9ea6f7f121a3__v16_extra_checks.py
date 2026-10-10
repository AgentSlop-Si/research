from pathlib import Path
import random,json
from independent_checks import mul,rank

def kernel_vector(a,p):
 w=[r[:] for r in a];piv=[];h=0;N=len(a[0])
 for c in range(N):
  k=next((k for k in range(h,len(w)) if w[k][c]),None)
  if k is None:continue
  w[k],w[h]=w[h],w[k];iv=pow(w[h][c],-1,p);w[h]=[x*iv%p for x in w[h]]
  for k in range(len(w)):
   if k!=h:
    v=w[k][c];w[k]=[(x-v*y)%p for x,y in zip(w[k],w[h])]
  piv.append(c);h+=1
  if h==len(w):break
 free=next(c for c in range(N) if c not in piv);v=[0]*N;v[free]=1
 for row,c in enumerate(piv):v[c]=(-w[row][free])%p
 return v

def main():
 out={};n=32;p=97;omega=pow(5,3,p);rng=random.Random(9031);A=[]
 for row in range(7):
  order=list(range(n));rng.shuffle(order)
  for g in range(4):
   a=[0]*n
   for j in order[g*8:(g+1)*8]:a[j]=rng.randrange(1,p)
   A.append(a)
 v=kernel_vector(A,p);F=[[pow(omega,k*j,p)for j in range(n)]for k in range(n)];image=mul(F,[[x]for x in v],p)
 assert any(v) and not any(x[0] for x in mul(A,[[x]for x in v],p)) and any(x[0]for x in image)
 out['overlapping_transcript']={'rank':rank(A,p),'rows':28,'columns':32,'nonzero_kernel':v,'nonzero_Fourier_image':[x[0]for x in image]}
 moments=[]
 for n,p,g in [(5,101,2),(8,97,5),(16,97,5),(25,101,2),(32,193,5),(49,197,2)]:
  w=pow(g,(p-1)//n,p);x=[j+1 for j in range(n)];y=[sum(x[j]*pow(w,k*j,p)for j in range(n))%p for k in range(2*n-1)];H=[[y[i+j]for j in range(n)]for i in range(n)];assert rank(H,p)==n;moments.append({'n':n,'rank':n})
  F=[[pow(w,k*j,p)for j in range(n)]for k in range(n)];coeff=[2,3,5,7];filter_matrix=[[sum(coeff[s]for s in range(4)if i==(j+s)%n)%p for j in range(n)]for i in range(n)];left=mul(F,filter_matrix,p);right=[[(sum(coeff[s]*pow(w,i*s,p)for s in range(4))*F[i][j])%p for j in range(n)]for i in range(n)];assert left==right
 out['full_Hankel_and_filter_checks']=moments
 for n in range(2,200):
  for R in range(1,n+1):
   # Equivalent exact positive inequality R-1 >= log2 R.
   assert 2**(R-1)>=R
 out['work_proxy_integer_minimum_verified']='R−1 ≥ log2 R; equality R=1,2'
 Path(__file__).with_name('V16_EXTRA_RESULTS.json').write_text(json.dumps(out,indent=2));print('PASS independent transcript, moment, filter and work-proxy controls')
if __name__=='__main__':main()
