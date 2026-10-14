#!/usr/bin/env python3
"""New bounded N=13 signed-bank gate. No historical imports or executable inputs."""
from pathlib import Path
import argparse, hashlib, itertools, json, time
P,N,Q=53,13,16
COUNTS={'determinants':0,'polynomial_exact_divisions':0,'literal_inversions':0,'matrix_products':0,'degree7_polynomials':0}
def trim(x):
 x=[a%P for a in x]
 while len(x)>1 and x[-1]==0:x.pop()
 return x or [0]
def add(x,y):return trim([(x[i] if i<len(x) else 0)+(y[i] if i<len(y) else 0) for i in range(max(len(x),len(y)))])
def neg(x):return trim([-a for a in x])
def sub(x,y):return add(x,neg(y))
def scale(x,a):return trim([a*b for b in x])
def mul(x,y):
 z=[0]*(len(x)+len(y)-1)
 for i,a in enumerate(x):
  for j,b in enumerate(y):z[i+j]=(z[i+j]+a*b)%P
 return trim(z)
def divmod_poly(x,y):
 x=trim(x[:]);y=trim(y[:]);assert y!=[0]
 q=[0]*max(1,len(x)-len(y)+1);iv=pow(y[-1],-1,P)
 while x!=[0] and len(x)>=len(y):
  d=len(x)-len(y);a=x[-1]*iv%P;q[d]=a
  for j,b in enumerate(y):x[d+j]=(x[d+j]-a*b)%P
  x=trim(x)
 return trim(q),x
def exactdiv(x,y):
 q,r=divmod_poly(x,y);assert r==[0],(x,y,r);COUNTS['polynomial_exact_divisions']+=1;return q
def xgcd(x,y):
 a,b=x[:],y[:];s,t,u,v=[1],[0],[0],[1]
 while b!=[0]:
  q,r=divmod_poly(a,b);a,b=b,r;s,t=t,sub(s,mul(q,t));u,v=v,sub(u,mul(q,v))
 if a==[0]:return [0],[0],[0]
 iv=pow(a[-1],-1,P);a,s,u=scale(a,iv),scale(s,iv),scale(u,iv)
 assert add(mul(s,x),mul(u,y))==a
 return a,s,u
def peval(x,a):
 r=0
 for b in reversed(x):r=(r*a+b)%P
 return r
def pdet(mat):
 COUNTS['determinants']+=1;a=[[v[:] for v in row] for row in mat];n=len(a);prev=[1];sgn=1
 if n==0:return [1]
 for k in range(n-1):
  h=next((r for r in range(k,n) if a[r][k]!=[0]),None)
  if h is None:return [0]
  if h!=k:a[k],a[h]=a[h],a[k];sgn=-sgn
  pivot=a[k][k][:]
  for i in range(k+1,n):
   for j in range(k+1,n):a[i][j]=exactdiv(sub(mul(pivot,a[i][j]),mul(a[i][k],a[k][j])),prev)
   a[i][k]=[0]
  prev=pivot
 return scale(a[-1][-1],sgn)
def solve(a,rhs):
 n=len(a[0]);r=[row[:]+[v] for row,v in zip(a,rhs)];piv=[];k=0
 for j in range(n):
  h=next((i for i in range(k,len(r)) if r[i][j]),None)
  if h is None:continue
  r[k],r[h]=r[h],r[k];iv=pow(r[k][j],-1,P);r[k]=[v*iv%P for v in r[k]]
  for i in range(len(r)):
   if i!=k and r[i][j]:
    c=r[i][j];r[i]=[(v-c*w)%P for v,w in zip(r[i],r[k])]
  piv.append(j);k+=1
 bad=any(not any(row[:n]) and row[-1] for row in r);free=[j for j in range(n) if j not in piv]
 ans=[0]*n
 if not bad:
  for i,j in enumerate(piv):ans[j]=r[i][-1]
 basis=[]
 for j in free:
  v=[0]*n;v[j]=1
  for i,h in enumerate(piv):v[h]=-r[i][j]%P
  basis.append(v)
 return {'rank':len(piv),'augmented_rank':len(piv)+int(bad),'consistent':not bad,'particular':None if bad else ans,'null_basis':basis,'pivots':piv,'rref':r}
def rankdet(a):
 a=[row[:] for row in a];d=1;n=len(a)
 for k in range(n):
  h=next((i for i in range(k,n) if a[i][k]),None)
  if h is None:return 0
  if h!=k:a[k],a[h]=a[h],a[k];d=-d%P
  d=d*a[k][k]%P;iv=pow(a[k][k],-1,P)
  for i in range(k+1,n):
   c=a[i][k]*iv%P
   for j in range(k,n):a[i][j]=(a[i][j]-c*a[k][j])%P
 return d

def derive():
 assert all(P%d for d in range(2,8)) and pow(Q,N,P)==1 and Q!=1
 F=[[pow(Q,-i*j,P) for j in range(N)] for i in range(N)];ivN=pow(N,-1,P)
 coeff=[[sum(F[(t+a)%N][t]*pow(Q,-b*t,P) for t in range(N))*ivN%P for b in range(N)] for a in range(N)]
 gamma=coeff[0][0];assert gamma;h=pow(4,-1,N)
 f=[[c*pow(gamma,-1,P)%P for c in row] for row in coeff]
 assert all(f[a][b]==pow(Q,h*(a+b)**2,P) for a in range(N) for b in range(N))
 D={}
 for e,d in itertools.product((1,-1),repeat=2):
  om=pow(Q,e*d,P);v={(0,0):1}
  for length in range(N+1):
   for (r,l),c in v.items():D[e,d,r,l]=c
   if length==N:assert all(c==int(r in (0,N)) for (r,l),c in v.items());break
   nv={}
   for (r,l),c in v.items():
    nv[r+1,l]=(nv.get((r+1,l),0)+c*pow(om,l,P))%P
    nv[r,l+1]=(nv.get((r,l+1),0)+c)%P
   v=nv
 def G(e,d,a,b):
  r=e*a%N;l=d*b%N
  return D[e,d,r,l] if r+l<N else 0
 moments={};triples={}
 for b in range(1,(N+1)//2):
  sole=G(-1,1,N-b,b);assert sole
  assert all(G(e,d,N-b,b)==0 for e,d in ((1,1),(1,-1),(-1,-1)))
  moments[b]=[];triples[b]=[]
  for a in range(b,N-b):
   den=G(1,1,a,b);assert den and not G(1,-1,a,b) and not G(-1,-1,a,b)
   u=f[a][b]*pow(den,-1,P)%P;v=G(-1,1,a,b)*pow(sole*den%P,-1,P)%P;ex=N-a-b
   pol=[u]+[0]*ex;pol[ex]-=v;moments[b].append(trim(pol));triples[b].append([u,v,ex])
 return F,coeff,gamma,f,D,G,moments,triples

def matrix_for(moments,m):
 rows=[];labels=[]
 for b,seq in moments.items():
  for j in range(len(seq)-m):rows.append(seq[j:j+m+1]);labels.append([b,j])
 return rows,labels

def matmul(a,b):
 COUNTS['matrix_products']+=1
 return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%P for j in range(len(b[0]))] for i in range(len(a))]
def inverse(a):
 COUNTS['literal_inversions']+=1;n=len(a);r=[row[:]+[int(i==j) for j in range(n)] for i,row in enumerate(a)]
 for j in range(n):
  h=next((i for i in range(j,n) if r[i][j]),None)
  if h is None:raise ValueError('singular')
  r[j],r[h]=r[h],r[j];iv=pow(r[j][j],-1,P);r[j]=[x*iv%P for x in r[j]]
  for i in range(n):
   if i!=j and r[i][j]:
    c=r[i][j];r[i]=[(x-c*y)%P for x,y in zip(r[i],r[j])]
 return [row[n:] for row in r]

def full_case(xs,y,z,ys,F,gamma,f,G):
 banks=[(1,1,x) for x in xs]+[(-1,1,y),(1,-1,z)]+[(-1,-1,x) for x in ys]
 sectors=[];amps=[[0]*N for _ in banks]
 for b in range(N):
  a=[[pow(x,e*r%N,P)*G(e,d,r,b)%P for e,d,x in banks] for r in range(N)];rhs=[f[r][b] for r in range(N)];s=solve(a,rhs)
  sectors.append({'b':b,'matrix':a,'target':rhs,**s})
  if s['consistent']:
   for i,x in enumerate(s['particular']):amps[i][b]=x
 result={'support_pp':xs,'cross_mp':y,'cross_pm':z,'support_mm':ys,'bank_count_declared':len(banks),'all_sectors_consistent':all(s['consistent'] for s in sectors),'sectors':sectors}
 if not result['all_sectors_consistent']:return result
 total=[[0]*N for _ in range(N)];literal=[];raw=[];I=[[int(i==j) for j in range(N)] for i in range(N)]
 for bi,(e,d,x) in enumerate(banks):
  delta=-pow(x,N,P)%P;assert delta
  w=[delta*gamma*sum(amps[bi][b]*pow(Q,-e*b*j,P) for b in range(N))%P for j in range(N)]
  assert all(sum(w[j]*pow(Q,e*b*j,P) for j in range(N))*pow(N*delta*gamma%P,-1,P)%P==amps[bi][b] for b in range(N))
  bank=[[0]*N for _ in range(N)];branches=[]
  for j in range(N):
   a=[[0]*N for _ in range(N)]
   for t in range(N):a[t][t]=(1-pow(Q,e*d*j+d*t,P))%P;a[(t+e)%N][t]=(a[(t+e)%N][t]-x)%P
   inv=inverse(a);assert matmul(a,inv)==I and matmul(inv,a)==I
   branches.append(inv)
   for r in range(N):
    for t in range(N):bank[r][t]=(bank[r][t]+w[j]*pow(N,-1,P)*inv[r][t])%P
  assert all(sum(bank[(t+a)%N][t]*pow(Q,-b*t,P) for t in range(N))*pow(N,-1,P)%P==gamma*amps[bi][b]*pow(x,e*a%N,P)*G(e,d,a,b)%P for a in range(N) for b in range(N))
  for r in range(N):
   for t in range(N):total[r][t]=(total[r][t]+bank[r][t])%P
  raw.append({'epsilon':e,'delta_sign':d,'alpha':x,'beta':1,'denominator':delta,'raw_weights':w,'sector_amplitudes':amps[bi]})
  literal.append({'bank':bank,'inverses':branches,'nonzero':any(any(row) for row in bank)})
 assert total==F
 nonzero=[i for i,b in enumerate(literal) if b['nonzero']]
 assert literal[len(xs)]['nonzero'] and literal[len(xs)+1]['nonzero']
 result.update({'raw_certificate':raw,'literal_banks':literal,'aggregate':total,'physical_nonzero_count':len(nonzero),'zero_bank_indices':sorted(set(range(len(banks)))-set(nonzero)),'all_target_entries_pass':N*N})
 # Falsification controls directly from validated bank matrices.
 result['deletion_mismatch_counts']=[sum(bank['bank'][r][t]!=0 for r in range(N) for t in range(N)) for bank in literal]
 result['omit_normalization_mismatches']=sum(N*total[r][t]%P!=F[r][t] for r in range(N) for t in range(N))
 result['reverse_target_mismatches']=sum(total[r][t]!=pow(Q,r*t,P) for r in range(N) for t in range(N))
 assert result['omit_normalization_mismatches'] and result['reverse_target_mismatches']
 return result

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',default=str(Path(__file__).parent/'outputs'));args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 F,coeff,gamma,f,D,G,moments,triples=derive();E,labels=matrix_for(moments,6);assert len(E)==9 and len(E[0])==7
 minors=[];g=[0];cert=[]
 for ids in itertools.combinations(range(9),7):
  determinant=pdet([E[i] for i in ids]);minors.append({'row_indices':list(ids),'coefficients_ascending':determinant})
  ng,s,t=xgcd(g,determinant);cert=[mul(s,c) for c in cert]+[t];g=ng
  # Independently evaluate the polynomial determinant against scalar elimination.
  for y in range(P):assert peval(determinant,y)==rankdet([[peval(v,y) for v in E[i]] for i in ids])
  if g==[1]:break
 combined=[0]
 for m,c in zip(minors,cert):combined=add(combined,mul(m['coefficients_ascending'],c))
 assert combined==g
 census=[];split7=[];E7,labels7=matrix_for(moments,7);assert len(E7)==6
 for y in range(1,P):
  entry={'y':y}
  for m,mat in ((6,E),(7,E7)):
   a=[[peval(v,y) for v in row[:m]] for row in mat];rhs=[-peval(row[m],y)%P for row in mat];entry['degree'+str(m)]=solve(a,rhs)
  s=entry['degree7'];entry['degree7_split_members']=[];entry['degree7_enumeration']=[]
  if s['consistent'] and len(s['null_basis'])==1:
   for parameter in range(P):
    h=[(a+parameter*b)%P for a,b in zip(s['particular'],s['null_basis'][0])]+[1];COUNTS['degree7_polynomials']+=1
    roots=[x for x in range(1,P) if peval(h,x)==0]
    entry['degree7_enumeration'].append({'parameter':parameter,'polynomial_ascending':h,'distinct_nonzero_roots':roots})
    if len(roots)==7:
     member={'y':y,'parameter':parameter,'polynomial_ascending':h,'roots':roots};entry['degree7_split_members'].append(member);split7.append(member)
  census.append(entry)
 data={'N':N,'p':P,'q':Q,'gamma':gamma,'inverse4_modN':pow(4,-1,N),'target':F,'target_weyl':coeff,'moment_triples':triples,'moment_polynomials':moments,'degree6_rows':E,'degree6_row_labels':labels,'degree6_augmented_maximal_minors':minors,'minor_gcd':g,'minor_bezout':cert,'degree7_rows':E7,'degree7_labels':labels7,'census':census,'split_degree7_members':split7}
 cases=[]
 for left,right in itertools.product(split7[:3],repeat=2):cases.append(full_case(left['roots'],left['y'],right['y'],right['roots'],F,gamma,f,G))
 baseline=full_case(list(range(1,12)),1,1,list(range(1,12)),F,gamma,f,G)
 # One fresh beta=0 legal control and one alpha=0 legal control, not used by witness.
 controls=[]
 for alpha,beta in ((0,2),(2,0)):
  delta=(1-pow(alpha,N,P)-pow(beta,N,P))%P;assert delta
  a=[[0]*N for _ in range(N)]
  for t in range(N):a[t][t]=(1-beta*pow(Q,t,P))%P;a[(t+1)%N][t]=(a[(t+1)%N][t]-alpha)%P
  inv=inverse(a);I=[[int(i==j) for j in range(N)] for i in range(N)];assert matmul(a,inv)==I and matmul(inv,a)==I;controls.append({'alpha':alpha,'beta':beta,'denominator':delta,'passed':True})
 data['boundary_controls']=controls
 files={'GATE.json':data,'SMALL_SUPPORT_CASES.json':cases,'BASELINE.json':baseline}
 for name,value in files.items():(out/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
 sources=['singleton_minimum_synthesis_0149/RESEARCH_NOTE.md','review_cubic_thirteen_0145/REVIEW.md','parameter_annihilator_gate_0131/CONTRACT.md','parameter_annihilator_gate_0131/REPORT.md','review_twelve_independent_2212/PRIOR_ACCEPTED_GRAMMAR.md']
 bindings=[{'path':p,'bytes':Path(p).stat().st_size,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in sources]
 (out/'SOURCE_BINDINGS.json').write_text(json.dumps(bindings,indent=2)+'\n')
 summary={'N':N,'p':P,'q':Q,'gamma':gamma,'minor_gcd':g,'minors_computed':len(minors),'minor_degrees':[len(m['coefficients_ascending'])-1 for m in minors],'degree6_compatible_y':[c['y'] for c in census if c['degree6']['consistent']],'degree7_rank_counts':{str(r):sum(c['degree7']['rank']==r for c in census) for r in sorted(set(c['degree7']['rank'] for c in census))},'degree7_split_count':len(split7),'small_cases_tested':len(cases),'small_cases_successes':sum(c['all_sectors_consistent'] for c in cases),'baseline_consistent':baseline['all_sectors_consistent'],'baseline_nonzero_banks':baseline.get('physical_nonzero_count'),'baseline_sector_ranks':[s['rank'] for s in baseline['sectors']],'counts':COUNTS}
 (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'TIMING.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start},indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
