"""Exact F241^2 completion screen; diagnostic statuses are not automatically complex exclusions."""
import importlib.util,itertools,json,collections
from pathlib import Path
P=241;NONRES=7
class E:
 __slots__=('a','b')
 def __init__(self,a=0,b=0):
  if isinstance(a,E):self.a,self.b=a.a,a.b
  else:self.a,self.b=int(a)%P,int(b)%P
 def __add__(self,o):o=E(o);return E(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.b)
 def __sub__(self,o):return self+-E(o)
 def __rsub__(self,o):return E(o)+-self
 def __mul__(self,o):o=E(o);return E(self.a*o.a+NONRES*self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def __pow__(self,n,mod=None):
  if n<0:
   den=pow((self.a*self.a-NONRES*self.b*self.b)%P,-1,P)
   return E(self.a*den,-self.b*den)**(-n)
  z=E(1);a=self
  while n:
   if n&1:z=z*a
   a=a*a;n//=2
  return z
 def __mod__(self,m):assert m==P;return self
 def __bool__(self):return bool(self.a or self.b)
 def __eq__(self,o):
  if not isinstance(o,(E,int)):return False
  o=E(o);return self.a==o.a and self.b==o.b
 def __hash__(self):return hash(self.a)if self.b==0 else hash((self.a,self.b))
 def __lt__(self,o):o=E(o);return(self.a,self.b)<(o.a,o.b)
 def __repr__(self):return f'E({self.a},{self.b})'
def encode(x):
 if isinstance(x,E):return[x.a,x.b]
 if isinstance(x,dict):return{k:encode(v)for k,v in x.items()}
 if isinstance(x,(list,tuple)):return[encode(v)for v in x]
 return x
spec=importlib.util.spec_from_file_location('own_completion',str(Path(__file__).with_name('_scale_completion_helpers.py')));s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);h=s.h;h.p=P
source=json.loads(Path(__file__).with_name('ORDER_SCREEN_RESULTS.json').read_text());domains=json.loads(Path(__file__).with_name('SURVIVOR_DOMAINS.json').read_text());B=[[E(x)for x in row]for row in source['B']]
assert pow(NONRES,(P-1)//2,P)==P-1
squares={x*x%P:x for x in range(P)}
def sqrt_base(d):
 if d in squares:return E(squares[d])
 return E(0,squares[d*pow(NONRES,-1,P)%P])
def roots(D):
 g=D['g'];out=[]
 if len(g)==3:
  disc=(g[1]**2-4*g[0]*g[2])%P;assert disc
  dd=sqrt_base(disc);out=[(E(1),(-E(g[1])+dd)*pow(2*g[2],-1,P)),(E(1),(-E(g[1])-dd)*pow(2*g[2],-1,P))]
 elif len(g)==2:out=[(E(1),E(-g[0]*pow(g[1],-1,P)))]
 else:assert not D['unrestricted']
 if D['infinity']:out.append((E(0),E(1)))
 assert len(out)==2
 assert all(all(h.qeval(q,z)==0 for e,q in D['qs'])for z in out)
 return out

def rank(A):
 M=[row[:]for row in A];r=0
 if not M:return 0
 for j in range(len(M[0])):
  k=next((k for k in range(r,len(M))if M[k][j]),None)
  if k is None:continue
  M[r],M[k]=M[k],M[r];t=pow(M[r][j],-1,P);M[r]=[v*t for v in M[r]]
  for k in range(r+1,len(M)):
   t=M[k][j];M[k]=[a-t*b for a,b in zip(M[k],M[r])]
  r+=1
  if r==len(M):break
 return r
def independent_rows(A):
 M=[row[:]for row in A];tags=list(range(len(M)));chosen=[];r=0
 for j in range(len(M[0])):
  k=next((k for k in range(r,len(M))if M[k][j]),None)
  if k is None:continue
  M[r],M[k]=M[k],M[r];tags[r],tags[k]=tags[k],tags[r];chosen.append(tags[r])
  t=pow(M[r][j],-1,P);M[r]=[x*t for x in M[r]]
  for k in range(r+1,len(M)):
   t=M[k][j];M[k]=[a-t*b for a,b in zip(M[k],M[r])]
  r+=1
  if r==len(M):break
 return chosen

def determinant(A):
 M=[row[:]for row in A];d=E(1)
 for j in range(len(M)):
  k=next((k for k in range(j,len(M))if M[k][j]),None)
  if k is None:return E(0)
  if k!=j:M[j],M[k]=M[k],M[j];d=-d
  pivot=M[j][j];d=d*pivot;iv=pow(pivot,-1,P);M[j]=[x*iv for x in M[j]]
  for k in range(j+1,len(M)):
   t=M[k][j];M[k]=[a-t*b for a,b in zip(M[k],M[j])]
 return d

results=[]
for pair in domains:
 a,b=pair['first'],pair['second'];pi=source['cycles'][a]['permutation'];tau=source['cycles'][b]['permutation'];ti=h.pinv(tau)
 for branch,zz in enumerate(itertools.product(*(roots(D)for D in pair['domains']))):
  u=[None]*5
  for cc,members in enumerate(pair['members']):
   for i in members:u[i]=h.canon(h.mv(pair['T'][i],zz[cc]))
  U=[[E(0)for j in range(5)]for i in range(5)]
  for i in range(5):U[i][i],U[i][pi[i]]=u[i]
  UB=h.mul(U,B);V=[[E(0)for j in range(5)]for i in range(5)];colranks=[];continuous=[]
  for j in range(5):
   rows=[[UB[i][j],UB[i][ti[j]]]for i in range(5)if j not in(i,pi[i],tau[i])];nz=[row for row in rows if any(row)]
   rr=rank(rows);assert rr<=1;colranks.append(rr)
   if rr==0:continuous.append(j);continue
   v=h.kernel(nz[0]);V[j][j],V[ti[j]][j]=v
  record=dict(first=a,second=b,branch=branch,component_roots=zz,row_directions=u,column_nullspace_ranks=colranks,zero_row_bases=[i for i in range(5)if not U[i][i]])
  if continuous:record.update(status='continuous_column_survivor',continuous_columns=continuous);results.append(record);continue
  K,_=s.sparse_sandwich(U,B,V);assert all(not K[i][j]for i in range(5)for j in range(5)if j not in(i,pi[i],tau[i]))
  coeff=[];rhs=[]
  for i in range(5):
   for j in range(5):
    row=[E(0)]*10;row[i]=V[i][j];row[5+j]=U[i][j]
    if any(row):coeff.append(row);rhs.append(K[i][j])
  rankA=rank(coeff);rankAug=rank([row+[v]for row,v in zip(coeff,rhs)])
  answer=s.scale_solve(U,V,K)
  augmented=[]
  for i in range(5):
   for j in range(5):
    row=[E(0)]*10;row[i]=V[i][j];row[5+j]=U[i][j];augmented.append(row+[K[i][j]])
  chosen=independent_rows(augmented);assert len(chosen)==11
  minor=[augmented[i]for i in chosen];dd=determinant(minor);assert dd
  positions=[[r//5,r%5]for r in chosen]
  row_degrees=[sum(i==ii for i,j in positions)-1 for ii in range(5)]
  col_degrees=[sum(j==jj for i,j in positions)-1 for jj in range(5)]
  assert all(x>=0 for x in row_degrees+col_degrees)and sum(row_degrees)==sum(col_degrees)==6
  lam=[E(i+2)for i in range(5)];mu=[E(2*j+3)for j in range(5)];gauge_rows=[]
  for i,j in positions:
   row=[E(0)]*10;row[i]=V[i][j]*mu[j];row[5+j]=U[i][j]*lam[i];gauge_rows.append(row+[K[i][j]*lam[i]*mu[j]])
  expected=dd
  for z,k in zip(lam,row_degrees):expected=expected*z**k
  for z,k in zip(mu,col_degrees):expected=expected*z**k
  assert determinant(gauge_rows)==expected
  record['column_directions']=[[V[j][j],V[ti[j]][j]]for j in range(5)]
  record['augmented_minor_certificate']=dict(positions=positions,determinant=dd,row_multidegrees=row_degrees,column_multidegrees=col_degrees,nonzero_gauge_check=True)
  record.update(status=answer['status']+':'+answer.get('reason','linear_completion'),zero_column_bases=[j for j in range(5)if not V[j][j]],rank_U=rank(U),rank_V=rank(V),rank_scale=rankA,rank_augmented=rankAug,scale_answer=answer)
  if answer['status']=='PASS':
   st=s.structural(U,V,list(range(5)),pi,list(range(5)),tau);record['structural_status']=st
   if st['status']=='PASS':assert s.recover(B,U,V,(list(range(5)),pi,list(range(5)),tau))['status']=='PASS'
  results.append(record)
counts=collections.Counter(x['status']for x in results);rankcounts=collections.Counter((x.get('rank_scale'),x.get('rank_augmented'),len(x['zero_row_bases']),len(x.get('zero_column_bases',[])))for x in results)
out=dict(field='F241[t]/(t^2-7)',pairs=len(domains),row_branches=len(results),counts=dict(counts),rank_counts=[dict(rank_scale=k[0],rank_augmented=k[1],zero_row_bases=k[2],zero_column_bases=k[3],count=v)for k,v in rankcounts.items()],branches=results)
Path(__file__).with_name('COMPLETION_SCREEN_RESULTS.json').write_text(json.dumps(encode(out),indent=2)+'\n')
print(json.dumps(encode({k:v for k,v in out.items()if k!='branches'}),indent=2))
