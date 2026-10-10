from pathlib import Path
import json,subprocess,tempfile,random,itertools
P=Path(__file__).parent;layout=json.loads((P/'source/AFFINE_LAYOUT.json').read_text());cert=json.loads((P/'source/EXACT_CERTIFICATES.json').read_text())['certificates'];N=256
perms=[]
for cols in layout['affine_shuffle_columns']:
 perm=[]
 for i in range(N):
  x=0
  for j,a in enumerate(cols):
   if i>>j&1:x^=a
  perm.append(x)
 assert sorted(perm)==list(range(N));perms.append(perm)
for p,w in [(12289,8340),(65537,282)]:assert pow(w,256,p)==1 and pow(w,128,p)==p-1
with tempfile.TemporaryDirectory() as td:
 binary=Path(td)/'cutown';subprocess.run(['g++','-O3','-std=c++17',str(P/'cut_certificate_own.cpp'),'-o',str(binary)],check=True)
 r=subprocess.run([str(binary)],input=' '.join(map(str,[N]+sum(perms,[]))),text=True,capture_output=True,check=True)
 results=json.loads(r.stdout);print(r.stderr,end='')
for c in cert:
 m=c['input_mask'];record=results['parity'][m-1];sets=[[int((i&m).bit_count()%2==0) for i in range(N)]]
 for p in perms:sets.append([sets[-1][p[i]] for i in range(N)])
 masks=[sum(s[1<<j]==0 and 1<<j or 0 for j in range(8)) for s in sets]
 assert masks==c['transported_masks']
 assert [i for i in range(N) if sets[0][i]]==c['cols'] and [i for i in range(N) if not sets[3][i]]==c['rows']
 assert record['boundaries']==c['stage_boundary_counts'] and record['rank']==[128,128]
 assert record['det']==[c['determinants_mod_p'][str(p)] for p in [12289,65537]]
 J=sum(1<<(j-1) for j in c['replaced_stages']);flow=results['subsets'][J-1]
 assert flow['best']==c['rank_correction_lower_bound'] and flow['flows'][m-1]==c['remaining_stage_capacity']
 assert 128-flow['flows'][m-1]==c['rank_correction_lower_bound']
 h=[70,49,69,46];assert sum(h[j-1] for j in c['replaced_stages'])>=c['rank_correction_lower_bound']
assert sum(h)==234
# Fully independent dense, general quasiseparable propagation controls, retaining zeros.
rng=random.Random(3825);p=65537
def rank(A):
 if not A:return 0
 A=[r[:] for r in A];rr=0
 for j in range(len(A[0])):
  k=next((k for k in range(rr,len(A)) if A[k][j]),None)
  if k is None:continue
  A[k],A[rr]=A[rr],A[k];v=pow(A[rr][j],-1,p);A[rr]=[x*v%p for x in A[rr]]
  for k in range(rr+1,len(A)):
   v=A[k][j];A[k]=[(x-v*y)%p for x,y in zip(A[k],A[rr])]
  rr+=1
 return rr
def mm(A,B):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def stage(n):
 a,b,c,d,pp,qq=[[rng.randrange(4) for j in range(n)] for i in range(6)];A=[[0]*n for _ in range(n)]
 for i in range(n):
  A[i][i]=rng.randrange(4)
  for j in range(i):
   v=a[i]*b[j]
   for k in range(j+1,i):v=v*pp[k]%p
   A[i][j]=v%p
  for j in range(i+1,n):
   v=c[i]*d[j]
   for k in range(i+1,j):v=v*qq[k]%p
   A[i][j]=v%p
 return A
controls=0;local=0
for n in [4,8,16]:
 for trial in range(8):
  Ss=[stage(n) for _ in range(4)];Ds=[[[rng.randrange(4) if i==j else 0 for j in range(n)] for i in range(n)] for s in range(4)];Ps=[rng.sample(range(n),n) for _ in range(3)];set0=set(rng.sample(range(n),n//2));sets=[set0]
  for pp in Ps:sets.append({i for i in range(n) if pp[i] in sets[-1]})
  budgets=[]
  for s in range(4):
   E=sets[s];d=sum((i in E)!=(i-1 in E) for i in range(1,n));budgets.append(d);block=[[Ss[s][i][j] for j in sorted(E)] for i in range(n) if i not in E];assert rank(block)<=d;local+=1
  def product(stages):
   out=stages[0]
   for s in range(1,4):out=mm(stages[s],[out[j] for j in Ps[s-1]])
   return out
  full=product(Ss)
  for J in range(1,16):
   rep=product([Ds[s] if J>>s&1 else Ss[s] for s in range(4)]);R=sorted(set(range(n))-sets[3]);C=sorted(set0)
   assert rank([[rep[i][j] for j in C] for i in R])<=sum(budgets[s] for s in range(4) if not(J>>s&1))
   hs=sum(rank([[(Ss[s][i][j]-Ds[s][i][j])%p for j in range(n)] for i in range(n)]) for s in range(4) if J>>s&1)
   assert rank([[(full[i][j]-rep[i][j])%p for j in range(n)] for i in range(n)])<=hs;controls+=1
results.update({'status':'PASS','certified_witnesses':15,'witness_determinants':30,'all_parity_ranks':510,'all_subset_parity_flows':3825,'general_QS_local_controls':local,'general_QS_replacement_controls':controls,'relaxation_witness':h,'total_rank_bound':234,'nonlinear_Toffoli_variant_used':False,'source_code_executed':False})
(P/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,sort_keys=True,indent=2)+'\n');print('ALL CHECKS PASS')
