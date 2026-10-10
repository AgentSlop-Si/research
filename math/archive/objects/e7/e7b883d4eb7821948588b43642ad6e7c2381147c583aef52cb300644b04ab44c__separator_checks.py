"""Fresh zero-weight, multi-cycle and outer-gauge controls for additive exclusion."""
from pathlib import Path
import json,random
from independent_checks import inv,mul,rank,ident

def cycle_order(perm):
 unseen=set(range(len(perm)));out=[]
 while unseen:
  k=min(unseen)
  while k in unseen:unseen.remove(k);out.append(k);k=perm[k]
 return out

def separator(orders):
 n=len(orders[0]);m=n//2;R=set(orders[0][:m]);C=set(orders[0][-m:])
 for order in orders[1:]:
  selected=[j for j in order if j in R or j in C];left=set(selected[:len(R)]);right=set(selected[len(R):]);a=(R&left,C&right);b=(R&right,C&left);R,C=max((a,b),key=lambda pair:len(pair[0]))
 return sorted(R),sorted(C)

def main():
 p=998244353;out=[]
 for n in [4,8,16,30,31,32,33,34,35,36,64]:
  rng=random.Random(5900+n)
  for trial in range(5):
   G=[];orders=[];spec=[]
   for term in range(2):
    perm=list(range(n));rng.shuffle(perm)
    if trial%2==0:
     order=list(range(n));rng.shuffle(order);perm=[0]*n
     for k in range(n):perm[order[k]]=order[(k+1)%n]
    weights=[rng.randrange(1,p) for k in range(n)]
    if trial in (1,4):weights[0]=0
    A=ident(n)
    for j in range(n):A[perm[j]][j]=(A[perm[j]][j]-weights[perm[j]])%p
    g=inv(A,p);order=cycle_order(perm);orders.append(order)
    left=[rng.randrange(1,p) for _ in range(n)];right=[rng.randrange(1,p) for _ in range(n)]
    g=[[g[i][j]*left[i]*right[j]%p for j in range(n)]for i in range(n)]
    for k in range(1,n):
     for I,J in ((order[:k],order[k:]),(order[k:],order[:k])):assert rank([[g[i][j]for j in J]for i in I],p)<=1
    G.append(g);spec.append({'permutation':perm,'zero_weights':weights.count(0)})
   R,C=separator(orders);assert len(R)==len(C) and len(R)>=(n//2+1)//2
   block=[[(G[0][i][j]+G[1][i][j])%p for j in C]for i in R];rr=rank(block,p);assert rr<=2
   out.append({'n':n,'trial':trial,'size':len(R),'rank':rr,'weighted_cycle_specs':spec})
 result={'cases':len(out),'all_cut_and_separator_ranks_pass':True,'zero_weight_and_multicycle_controls':True,'all_length_necessary_condition':'ceil(floor(N/2)/2)^2 <= 2N','small_excluded_by_bound':[n for n in range(2,65) if ((n//2+1)//2)**2>2*n],'samples':out}
 Path(__file__).with_name('SEPARATOR_RESULTS.json').write_text(json.dumps(result,indent=2));print('PASS',len(out),'independent weighted-cycle pair controls')
if __name__=='__main__':main()
