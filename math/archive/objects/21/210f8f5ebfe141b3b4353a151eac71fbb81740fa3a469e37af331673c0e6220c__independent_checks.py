#!/usr/bin/env python3
"""Independent exhaustive N5 certificate, rebuilt from target and all cycles.
No constructor or uploaded code is imported. Standard library only.
"""
from pathlib import Path
import itertools,json,sys,random,hashlib
p=241
class E:
 __slots__=('a','b')
 def __init__(self,a=0,b=0):
  if isinstance(a,E):self.a,self.b=a.a,a.b
  else:self.a,self.b=a%p,b%p
 def __add__(self,y):y=E(y);return E(self.a+y.a,self.b+y.b)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.b)
 def __sub__(self,y):return self+-E(y)
 def __rsub__(self,y):return E(y)+-self
 def __mul__(self,y):y=E(y);return E(self.a*y.a+7*self.b*y.b,self.a*y.b+self.b*y.a)
 __rmul__=__mul__
 def inverse(self):d=(self.a*self.a-7*self.b*self.b)%p;assert d;d=pow(d,-1,p);return E(self.a*d,-self.b*d)
 def __truediv__(self,y):return self*E(y).inverse()
 def __eq__(self,y):y=E(y);return self.a==y.a and self.b==y.b
 def __bool__(self):return bool(self.a or self.b)
 def __pow__(self,n):
  out=E(1);a=self
  while n:
   if n&1:out=out*a
   a=a*a;n//=2
  return out
 def enc(self):return [self.a,self.b]
def norm(v):
 a,b=map(E,v);assert a or b
 return (E(1),b/a) if a else (E(),E(1))
def vkey(v):return tuple((c.a,c.b) for c in norm(v))
def rowskey(vv):return tuple(vkey(v) for v in vv)
def ei(n):return [[E(i==j) for j in range(n)] for i in range(n)]
def em(a,b):return [[sum((x*y for x,y in zip(r,c)),E()) for c in zip(*b)] for r in a]
def erank(a,return_rows=False):
 a=[list(map(E,r)) for r in a];ids=list(range(len(a)));used=[];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];ids[k],ids[q]=ids[q],ids[k];used.append(ids[k]);scale=a[k][j].inverse();a[k]=[v*scale for v in a[k]]
  for q in range(k+1,len(a)):
   scale=a[q][j]
   if scale:a[q]=[v-scale*w for v,w in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return (k,used) if return_rows else k

def edet(a):
 a=[list(map(E,r)) for r in a];z=E(1)
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return E()
  if k!=j:a[k],a[j]=a[j],a[k];z=-z
  pivot=a[j][j];z=z*pivot
  for i in range(j+1,len(a)):
   c=a[i][j]/pivot
   if c:
    for k in range(j,len(a)):a[i][k]=a[i][k]-c*a[j][k]
 return z

def einv(a):
 n=len(a);a=[list(map(E,r))+ei(n)[i] for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]);a[k],a[j]=a[j],a[k];q=a[j][j].inverse();a[j]=[v*q for v in a[j]]
  for k in range(n):
   if k!=j:
    q=a[k][j]
    if q:a[k]=[v-q*w for v,w in zip(a[k],a[j])]
 return [r[n:] for r in a]
# Base-field 2x2 operations for projective forests.
def det(a):return (a[0][0]*a[1][1]-a[0][1]*a[1][0])%p
def mul(a,b):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def tr(a):return list(map(list,zip(*a)))
def invert(a):q=pow(det(a),-1,p);return [[a[1][1]*q%p,-a[0][1]*q%p],[-a[1][0]*q%p,a[0][0]*q%p]]
def transform(a,v):return norm([sum((x*y for x,y in zip(r,v)),E()) for r in a])
def trim(a):
 a=[x%p for x in a]
 while a and not a[-1]:a.pop()
 return a

def rem(a,b):
 a=trim(a);b=trim(b)
 while len(a)>=len(b):
  c=a[-1]*pow(b[-1],-1,p)%p;k=len(a)-len(b)
  for j,x in enumerate(b):a[k+j]=(a[k+j]-c*x)%p
  a=trim(a)
 return a

def gcd(a,b):
 a=trim(a);b=trim(b)
 while b:a,b=b,rem(a,b)
 return [x*pow(a[-1],-1,p)%p for x in a] if a else []
squares={x*x%p:x for x in range(p)}
def sqrt_base(d):
 d%=p
 if d in squares:return E(squares[d])
 assert d*pow(7,-1,p)%p in squares;return E(0,squares[d*pow(7,-1,p)%p])
def peval(q,v):return q[0]*v[0]*v[0]+q[1]*v[0]*v[1]+q[2]*v[1]*v[1]
def domain(qs):
 nonzero=[q for q in qs if any(q)];assert nonzero,'unrestricted component'
 g=[]
 for q in nonzero:g=gcd(g,q)
 roots=[]
 if len(g)==2:roots=[(E(1),E(-g[0]*pow(g[1],-1,p)))]
 if len(g)==3:
  a,b,c=g[2],g[1],g[0];d=(b*b-4*a*c)%p;root=sqrt_base(d);roots=[(E(1),(-b+root)/E(2*a))]
  if d:roots.append((E(1),(-b-root)/E(2*a)))
 if all(q[2]==0 for q in qs):roots.append((E(),E(1)))
 assert all(all(not peval(q,v) for q in qs) for v in roots)
 assert len(set(vkey(v) for v in roots))==len(roots)
 return roots,{'gcd':g,'infinity':all(q[2]==0 for q in qs),'quadratics':qs}

def cycles(n):
 out=[]
 for rest in itertools.permutations(range(1,n)):
  seq=(0,)+rest;pi=[0]*n
  for i,j in zip(seq,seq[1:]+seq[:1]):pi[i]=j
  out.append(pi)
 assert len(set(map(tuple,out)))==len(out)
 return out

def target(n,w):
 F=[[E(pow(w,i*j,p)) for j in range(n)] for i in range(n)];A=ei(n)
 for i in range(n):A[i][i]=E(pow(w,((n+1)//2)*i*i,p))
 Fi=einv(F);return einv([[Fi[i][j]+A[i][j] for j in range(n)] for i in range(n)])

def edges(B,pi,tau):
 n=len(pi);ti=[tau.index(j) for j in range(n)];out=[]
 for i,k in itertools.combinations(range(n),2):
  for j in range(n):
   if j in {i,k,pi[i],pi[k],tau[i],tau[k]}:continue
   a,b=B[i][j],B[i][ti[j]];c,d=B[pi[i]][j],B[pi[i]][ti[j]];e,f=B[k][j],B[k][ti[j]];g,h=B[pi[k]][j],B[pi[k]][ti[j]]
   C=[[(a*f-b*e)%p,(a*h-b*g)%p],[(c*f-d*e)%p,(c*h-d*g)%p]]
   assert det(C)==det([[a,b],[c,d]])*det([[e,f],[g,h]])%p
   out.append((i,k,j,C))
 return out

def row_domains(B,pi,tau):
 ee=edges(B,pi,tau);n=len(pi);adj=[[] for _ in range(n)]
 for i,k,j,C in ee:
  assert det(C),'singular transition needs separate stratum'
  H=[[C[0][1],C[1][1]],[-C[0][0]%p,-C[1][0]%p]];adj[i].append((k,H));adj[k].append((i,invert(H)))
 comp=[None]*n;maps=[None]*n;members=[]
 for root in range(n):
  if comp[root] is not None:continue
  ci=len(members);members.append([]);comp[root]=ci;maps[root]=[[1,0],[0,1]];stack=[root]
  while stack:
   i=stack.pop();members[ci].append(i)
   for k,H in adj[i]:
    if comp[k] is None:comp[k]=ci;maps[k]=mul(H,maps[i]);stack.append(k)
 qs=[[] for m in members]
 for i,k,j,C in ee:
  assert comp[i]==comp[k]
  D=mul(mul(tr(maps[i]),C),maps[k]);qs[comp[i]].append([D[0][0],(D[0][1]+D[1][0])%p,D[1][1]])
 domains=[];proof=[]
 for qq in qs:
  dom,pr=domain(qq);domains.append(dom);proof.append(pr)
 return domains,comp,maps,proof,len(ee)

def sparse_matrices(B,pi,tau,ur):
 n=len(pi);ti=[tau.index(j) for j in range(n)];U=[[E() for _ in range(n)] for _ in range(n)]
 for i,(a,b) in enumerate(ur):U[i][i]=a;U[i][pi[i]]=b
 UB=em(U,B);vc=[];ranks=[]
 for j in range(n):
  rows=[[UB[i][j],UB[i][ti[j]]] for i in range(n) if j not in {i,pi[i],tau[i]}]
  r=erank(rows);assert r==1;ranks.append(r);first=next(row for row in rows if any(row));v=norm([-first[1],first[0]]);assert all(not sum((a*b for a,b in zip(row,v)),E()) for row in rows);vc.append(v)
 V=[[E() for _ in range(n)] for _ in range(n)]
 for j,(a,b) in enumerate(vc):V[j][j]=a;V[ti[j]][j]=b
 return U,V,vc,ranks

def augmented(B,U,V):
 n=len(B);K=em(em(U,B),V);M=[]
 for i in range(n):
  for j in range(n):
   row=[E()]*(2*n+1);row[i]=V[i][j];row[n+j]=U[i][j];row[-1]=K[i][j];M.append(row)
 return M,K

def main():
 assert pow(7,120,p)==p-1 and pow(91,5,p)==1 and 91!=1
 n=5;B=target(n,91);wanted=[[161,20,102,102,20],[20,182,62,26,92],[102,62,236,28,26],[102,26,28,236,62],[20,92,26,62,182]];assert B==[[E(x) for x in row] for row in wanted]
 G=sum(pow(91,3*j*j,p) for j in range(n))%p;c=5*G%p;assert (G,c,(1+c)%p)==(103,33,34) and G*G%p==5
 BF=[[E((pow(91,i*j,p)-G*pow(91,(-3*(i+j)**2)%5,p)+c*pow(91,(-3*i*i)%5,p)*(i==j))*pow(34,-1,p)) for j in range(n)] for i in range(n)];assert BF==B
 orders=cycles(n);records=[];certificates=[];reject=0;survive=0;branches=0;components={};edgecount=0;zero_bases={};colchecks=0
 for a,pi in enumerate(orders):
  for b,tau in enumerate(orders):
   ds,comp,maps,proof,ec=row_domains(wanted,pi,tau);edgecount+=ec
   if any(not d for d in ds):
    reject+=1;records.append({'pair':[a,b],'status':'ROW_EMPTY','component_proofs':proof});continue
   assert all(len(d)==2 for d in ds);survive+=1;components[len(ds)]=components.get(len(ds),0)+1;count=0
   for roots in itertools.product(*ds):
    ur=[transform(maps[i],roots[comp[i]]) for i in range(n)];U,V,vc,rs=sparse_matrices(B,pi,tau,ur);colchecks+=len(rs);M,K=augmented(B,U,V)
    for i in range(n):
     for j in range(n):
      if j not in {i,pi[i],tau[i]}:assert not K[i][j]
    r,ids=erank(M,True);assert r==11 and erank([row[:-1] for row in M])==10
    sub=[M[i] for i in ids];dd=edet(sub);assert dd
    rd=[sum(idx//n==i for idx in ids)-1 for i in range(n)];cd=[sum(idx%n==j for idx in ids)-1 for j in range(n)];assert min(rd+cd)>=0 and sum(rd)==sum(cd)==6
    lam=[E(i+2,i+1) for i in range(n)];mu=[E(i+9,2*i+1) for i in range(n)];UU=[[lam[i]*x for x in row] for i,row in enumerate(U)];VV=[[x*mu[j] for j,x in enumerate(row)] for row in V];MM,_=augmented(B,UU,VV);d2=edet([MM[i] for i in ids]);factor=E(1)
    for x,k in zip(lam,rd):factor=factor*x**k
    for x,k in zip(mu,cd):factor=factor*x**k
    assert d2==dd*factor
    zb=(sum(not v[0] for v in ur),sum(not v[0] for v in vc));zero_bases[zb]=zero_bases.get(zb,0)+1
    certificates.append({'pair':[a,b],'rows':[[x.enc() for x in v] for v in ur],'columns':[[x.enc() for x in v] for v in vc],'positions':[[i//n,i%n] for i in ids],'determinant':dd.enc(),'row_degrees':rd,'column_degrees':cd,'zero_bases':list(zb)})
    branches+=1;count+=1
   records.append({'pair':[a,b],'status':'AUGMENTED_MINOR_REJECT','components':len(ds),'branches':count,'component_proofs':proof})
 assert (reject,survive,branches,colchecks)==(384,192,624,3120);assert components=={2:120,1:72};assert zero_bases=={(0,1):240,(1,0):240,(0,0):144}
 # Independently generated valid sums, including endpoint boundaries.
 rng=random.Random(5724);positives=[]
 for z in range(12):
  pi=orders[z];tau=orders[(7*z+3)%24];plans=[];dirs=[]
  for branch,perm in enumerate([pi,tau]):
   weights=[E(0 if (z+branch+i)%4==0 else i+branch+2) for i in range(n)];den=ei(n)
   for i in range(n):den[i][perm[i]]=den[i][perm[i]]-weights[i]
   green=einv(den);L=[E(rng.randrange(1,p)) for i in range(n)];R=[E(rng.randrange(1,p)) for i in range(n)]
   if z%3==1:L[(z+branch)%n]=E()
   if z%3==2:R[(z+2*branch)%n]=E()
   plans.append([[L[i]*green[i][j]*R[j] for j in range(n)] for i in range(n)])
   # Exact leading valuation normalization of inverse sparse row/column pairs.
   if branch==0:
    rr=[]
    for i in range(n):
     # R_i^-1 cancels in each row. Remaining coefficients L_i^-1,
     # -w_i L_pi(i)^-1. Zero endpoint uses epsilon, valuation -1.
     co=[(E(1)/L[i],0) if L[i] else (E(1),-1),(-weights[i]/L[perm[i]],0) if L[perm[i]] else (-weights[i],-1)]
     val=min(v for a,v in co if a);rr.append(norm([a if v==val else E() for a,v in co]))
    dirs.append(rr)
   else:
    cc=[];ti=[perm.index(j) for j in range(n)]
    for j in range(n):
     # L_j^-1 cancels in each column; coefficients R_j^-1,
     # -w_tau^-1(j) R_tau^-1(j)^-1.
     i=ti[j];co=[(E(1)/R[j],0) if R[j] else (E(1),-1),(-weights[i]/R[i],0) if R[i] else (-weights[i],-1)];val=min(v for a,v in co if a);cc.append(norm([a if v==val else E() for a,v in co]))
    dirs.append(cc)
  BB=[[plans[0][i][j]+plans[1][i][j] for j in range(n)] for i in range(n)];U=[[E() for _ in range(n)] for i in range(n)];V=[[E() for _ in range(n)] for i in range(n)]
  for i,v in enumerate(dirs[0]):U[i][i]=v[0];U[i][pi[i]]=v[1]
  for j,v in enumerate(dirs[1]):V[j][j]=v[0];V[tau.index(j)][j]=v[1]
  M,K=augmented(BB,U,V);r=erank(M);assert r<=10
  for i in range(n):
   for j in range(n):
    if j not in {i,pi[i],tau[i]}:assert not K[i][j]
  positives.append({'trial':z,'augmented_rank':r,'singular_endpoint':z%3!=0})
 # Actual N3 positive target with known two-Green formula and all minors.
 w=15;t=207;kappa=2;nn=3;D=[E(w),E(1),E(1)];pi=[1,2,0];tau=[2,0,1];BB=target(nn,w);branches3=[]
 for perm in [pi,tau]:
  den=ei(nn)
  for i in range(nn):den[i][perm[i]]=den[i][perm[i]]-t
  green=einv(den);branches3.append([[kappa*D[i]*green[i][j]*D[j] for j in range(nn)] for i in range(nn)])
 assert BB==[[branches3[0][i][j]+branches3[1][i][j] for j in range(nn)] for i in range(nn)]
 U=einv(branches3[0]);V=einv(branches3[1]);M,K=augmented(BB,U,V);assert erank(M)==6
 for ids in itertools.combinations(range(9),7):assert not edet([M[i] for i in ids])
 summary={'status':'PASS','uploaded_or_constructor_code_executed':False,'prime':p,'quadratic_extension':'theta^2=7','Hamiltonian_cycles':24,'ordered_pairs':576,'row_rejections':reject,'survivor_pairs':survive,'survivor_component_counts':components,'branches':branches,'column_rank_one_checks':colchecks,'all_pair_row_relations':edgecount,'nonzero_augmented_minors':branches,'gauge_checks':branches,'zero_base_counts':[{'row':a,'column':b,'count':c} for (a,b),c in sorted(zero_bases.items())],'positive_boundary_controls':positives,'N3_positive_augmented_rank':6,'N3_all_maximal_minors':36}
 out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');data={'summary':summary,'order_records':records,'branch_certificates':certificates};out.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
