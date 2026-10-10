#!/usr/bin/env python3
"""Own finite-field fiber, expander, and Fourier controls; no source imports."""
from pathlib import Path
import json,random,sys,math,cmath
P=65537;R=random.Random(140042)
def inv(x):return pow(x%P,-1,P)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c))%P for c in zip(*b)] for r in a]
def inverse(a):
 n=len(a);a=[r[:]+eye(n)[i] for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]);a[k],a[j]=a[j],a[k];q=inv(a[j][j]);a[j]=[v*q%P for v in a[j]]
  for k in range(n):
   if k!=j:
    q=a[k][j];a[k]=[(v-q*w)%P for v,w in zip(a[k],a[j])]
 return [r[n:] for r in a]
def rank(a):
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];scale=inv(a[k][j]);a[k]=[v*scale%P for v in a[k]]
  for q in range(k+1,len(a)):
   scale=a[q][j];a[q]=[(v-scale*w)%P for v,w in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return k

def margulis(t):
 return [[((u+2*v)%t)*t+v for u in range(t) for v in range(t)], [((u+2*v+1)%t)*t+v for u in range(t) for v in range(t)], [u*t+(v+2*u)%t for u in range(t) for v in range(t)], [u*t+(v+2*u+1)%t for u in range(t) for v in range(t)]]
def lifted(t):
 s=t*t;maps=margulis(t);X=[[pi[x]*s+y for x in range(s) for y in range(s)] for pi in maps];Y=[[x*s+pi[y] for x in range(s) for y in range(s)] for pi in maps];return X,Y
def green(pi):
 n=len(pi);a=eye(n)
 for i,j in enumerate(pi):a[i][j]=(a[i][j]-inv(4))%P
 return inverse(a)
def total(gs,multiplicity=5):return [[sum(G[i][j] for G in gs)*multiplicity%P for j in range(len(gs[0]))] for i in range(len(gs[0]))]
def main():
 out={'status':'PASS','uploaded_or_constructor_code_executed':False};blocks=0;entries=0;sharp=0;gram=0
 for s in [2,4,8]:
  N=s*s;w=pow(3,(P-1)//N,P);ws=pow(w,s,P);F=[[pow(w,(-i*j)%N,P)*inv(s)%P for j in range(N)] for i in range(N)]
  XB=[[[R.randrange(P) for j in range(s)] for i in range(s)] for y in range(s)];YB=[[[R.randrange(P) for j in range(s)] for i in range(s)] for x in range(s)]
  X=[[XB[j%s][i//s][j//s] if i%s==j%s else 0 for j in range(N)] for i in range(N)];Y=[[YB[i//s][i%s][j%s] if i//s==j//s else 0 for j in range(N)] for i in range(N)];T=mm(Y,X)
  for x in range(s):
   for yp in range(s):
    B=[[T[x*s+y][xp*s+yp] for xp in range(s)] for y in range(s)];FB=[[F[x*s+y][xp*s+yp] for xp in range(s)] for y in range(s)]
    assert rank(B)<=1 and rank(FB)==s;blocks+=1
    for y in range(s):
     for xp in range(s):assert B[y][xp]==YB[x][y][yp]*XB[yp][x][xp]%P;entries+=1
  # Independently multiply all s explicitly constructed singular fiber paths.
  S=[[0]*N for _ in range(N)]
  for a in range(s):
   XA=[[pow(ws,(-(i//s)*(j%s))%s,P) if i%s==j%s and j//s==a else 0 for j in range(N)] for i in range(N)]
   YA=[[inv(s)*pow(ws,(-(i%s)*a)%s,P)*pow(w,(-(i%s)*(j%s))%N,P)%P if i//s==j//s else 0 for j in range(N)] for i in range(N)];Z=mm(YA,XA)
   S=[[(u+v)%P for u,v in zip(r,t)] for r,t in zip(S,Z)]
  assert S==F;sharp+=N*N
  # Complex Gram of Fourier transverse blocks: all singular values 1/sqrt(s).
  wc=cmath.exp(-2j*math.pi/N)
  for x in range(s):
   for yp in range(s):
    B=[[wc**((s*x+y)*(s*xp+yp))/s for xp in range(s)] for y in range(s)]
    for y in range(s):
     for z in range(s):assert abs(sum(B[y][k]*B[z][k].conjugate() for k in range(s))-int(y==z)/s)<1e-11;gram+=1
 out.update(transverse_blocks=blocks,product_entries=entries,sharp_decomposition_entries=sharp,complex_gram_entries=gram)
 # All subsets at t=2: forty plans, preserving one axis in each stage.
 t=2;s=t*t;N=s*s;xp,yp=lifted(t);plans=xp+yp;cutcases=0;minimum_slack=10**6
 for mask in range(1,(1<<N)-1):
  m=mask.bit_count();budget=5*sum(((mask>>i)&1) and not ((mask>>pi[i])&1) for pi in plans for i in range(N));cap=min(m,N-m);assert budget>cap;minimum_slack=min(minimum_slack,budget-cap);cutcases+=1
 out['all_nontrivial_cut_controls']=cutcases;out['minimum_budget_minus_maximum_possible_rank']=minimum_slack
 GX=[green(pi) for pi in xp];GY=[green(pi) for pi in yp];X=total(GX);Y=total(GY);T=mm(Y,X);mix=total(GX+GY);mixed=mm(mix,mix);polar_ranks=[];mixed_ranks=[]
 for x in range(s):
  for yp0 in range(s):
   polar_ranks.append(rank([[T[x*s+y][xp0*s+yp0] for xp0 in range(s)] for y in range(s)]));mixed_ranks.append(rank([[mixed[x*s+y][xp0*s+yp0] for xp0 in range(s)] for y in range(s)]))
 assert max(polar_ranks)<=1 and max(mixed_ranks)>1
 out['polarized_transverse_ranks']=polar_ranks;out['mixed_axis_transverse_ranks']=mixed_ranks
 # Fixed-coordinate route accounted: free diagonal gauge preserves rook support.
 gaugecontrols=0;dimensions=[]
 for s in [2,3,4,5,8]:
  N=s*s;d=N*(2*s-1);assert N*N-(2*d-N)==s*s*(s-1)*(s-3);dimensions.append([s,d,2*d-N,N*N-(2*d-N)])
  if s<=4:
   X=[[R.randrange(P) if i//s==j//s or i%s==j%s else 0 for j in range(N)] for i in range(N)];Y=[[R.randrange(P) if i//s==j//s or i%s==j%s else 0 for j in range(N)] for i in range(N)];D=[R.randrange(1,P) for _ in range(N)];DX=[[D[i]*v%P for v in r] for i,r in enumerate(X)];YDi=[[v*inv(D[j])%P for j,v in enumerate(r)] for r in Y];assert mm(Y,X)==mm(YDi,DX);gaugecontrols+=1
 out['rook_dimensions']=dimensions;out['rook_diagonal_gauges']=gaugecontrols
 # Exact normalization of graph gap and resulting operator obstruction.
 gap=5*(4-5*math.sqrt(2)/2);assert gap>2
 out['analytic_gap_gt_two']=True;out['polarized_error_floors']=[[t,round(math.sqrt(1-1/(t*t)),12)] for t in [2,3,4,8,16]]
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
