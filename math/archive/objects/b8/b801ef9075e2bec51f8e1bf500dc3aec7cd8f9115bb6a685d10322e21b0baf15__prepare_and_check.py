"""Independently reconstruct Phase30 matrices and check saved numerical data."""
from pathlib import Path
import json,itertools,random,math,struct,hashlib
from independent_utils import family,components,rank,det
ROOT=Path(__file__).resolve().parent;SRC=ROOT/'extracted/fft_green_phase30_four_parameter';CERT=SRC/'certificates'
def mon(deg,q):
 if q==1:return [(deg,)]
 return [(i,)+tail for i in range(deg+1)for tail in mon(deg-i,q-1)]
def macaulay(T,G,rs,cs,p,degree=3,anchored=False):
 q=len(G);m=len(rs);e2=mon(2,q);base=mon(degree,q);pos={e:i for i,e in enumerate(base)};epos={e:i for i,e in enumerate(e2)};shifts=mon(degree-2,q);rows=[]
 def vec(i,j):return [G[k][i][j]for k in list(range(1,q))+[0]]
 for i,ip in itertools.combinations(range(m),2):
  for j,jp in itertools.combinations(range(m),2):
   if anchored and (i!=0 or j!=0):continue
   A=T[i][jp]*T[ip][j]%p;B=T[i][j]*T[ip][jp]%p
   v,w,x,y=vec(rs[i],cs[j]),vec(rs[ip],cs[jp]),vec(rs[i],cs[jp]),vec(rs[ip],cs[j]);coeff=[0]*len(e2)
   for u in range(q):
    for z in range(q):
     e=[0]*q;e[u]+=1;e[z]+=1;k=epos[tuple(e)];coeff[k]=(coeff[k]+A*v[u]*w[z]-B*x[u]*y[z])%p
   for shift in shifts:
    row=[0]*len(base)
    for e,co in zip(e2,coeff):row[pos[tuple(a+b for a,b in zip(e,shift))]]=co
    rows.append(row)
 return rows

def main():
 results={};specs=[]
 for n,p,generator in [(4,998244353,3),(8,998244353,3),(8,2013265921,31),(16,998244353,3)]:
  T,G,spec=family(n,p,generator);g3,sg3=components(n,(2800+n)*3+7,p,spec['root'],[11]);G+=g3;spec['G3']=sg3;specs.append(spec)
  (ROOT/f'four_N{n}_p{p}.txt').write_text(str(n)+' '+str(p)+'\n'+'\n'.join(' '.join(map(str,r))for M in [T]+G for r in M)+'\n')
  key=f'N{n}_p{p}';results[key]={'reconstructed':True}
  if p==998244353 and n in (8,16):
   c=json.loads((CERT/f'python_witnesses_N{n}.json').read_text());count=0
   for w in c['selected_witnesses']:
    mat=macaulay(T,G,w['source_rows'],w['source_columns'],p);assert det([mat[j]for j in w['pivot_rows']],p)==w['nonzero_determinant_mod_p']!=0;count+=1
   results[key]['saved_minor_witnesses_verified']=count
  if p==998244353:
   rng=random.Random(731+n);rs=list(range(n));cs=list(range(n));rng.shuffle(rs);rng.shuffle(cs);left=[rng.randrange(1,p)for _ in range(n)];right=[rng.randrange(1,p)for _ in range(n)];coeff=[1,2,3,5];B=[[sum(coeff[z]*G[z][i][j]for z in range(4))%p for j in range(n)]for i in range(n)];PT=[[left[i]*B[rs[i]][cs[j]]*right[j]%p for j in range(n)]for i in range(n)];rnk=rank(macaulay(PT,G,rs[:3],cs[:3],p),p);assert rnk<20;results[key]['independent_positive_control_rank']=rnk
   anchored=rank(macaulay(T,G,[0,1,2],[0,1,2],p,degree=5,anchored=True),p);assert anchored<56;results[key]['anchored_degree5_rank']=anchored
   g4,sg4=components(n,(2800+n)*3+11,p,spec['root'],[13]);spec['G4_custom_control']=sg4
   dims=[]
   for deg in [3,4,5]:
    MM=macaulay(T,G+g4,[0,1,2],[0,1,2],p,degree=deg);dims.append(len(MM[0])-rank(MM,p))
   results[key]['custom_five_term_3x3_quotient_dimensions']=dims
 results['rank_stream_archive']={'bytes':(CERT/'ranks_N16_all_p998244353.bin').stat().st_size,'sha256':hashlib.sha256((CERT/'ranks_N16_all_p998244353.bin').read_bytes()).hexdigest(),'all_bytes_20':set((CERT/'ranks_N16_all_p998244353.bin').read_bytes())=={20},'status':'Stored data only; independent exhaustive replay separate.'}
 (ROOT/'PREPARATION_RESULTS.json').write_text(json.dumps(results,indent=2));(ROOT/'FAMILY_SPECIFICATIONS.json').write_text(json.dumps(specs,indent=2));print(json.dumps(results,indent=2))
if __name__=='__main__':main()
