"""Independent mathematical audit. No uploaded programs imported or executed."""
import json, math, random, hashlib, pathlib, itertools
P=998244353
B=pathlib.Path(__file__).resolve().parent
out={}

def rank(M,p=P):
 a=[[v%p for v in r] for r in M]; n=len(a);m=len(a[0]) if n else 0;k=0
 for j in range(m):
  t=next((i for i in range(k,n) if a[i][j]),None)
  if t is None:continue
  a[k],a[t]=a[t],a[k];inv=pow(a[k][j],-1,p)
  a[k]=[v*inv%p for v in a[k]]
  for i in range(k+1,n):
   v=a[i][j]
   if v:a[i]=[(x-v*y)%p for x,y in zip(a[i],a[k])]
  k+=1
  if k==n:break
 return k

def mm(A,B,p=P):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def mv(A,x,p=P):return [sum(a*b for a,b in zip(r,x))%p for r in A]
def trans(A):return [list(r) for r in zip(*A)]
def sub(A,B,p=P):return [[(x-y)%p for x,y in zip(a,b)] for a,b in zip(A,B)]
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def perm(s):return [[int(s[j]==i) for j in range(len(s))] for i in range(len(s))]
def inv(A,p=P):
 n=len(A); a=[[(v%p) for v in r]+e for r,e in zip(A,eye(n))]
 for k in range(n):
  t=next((i for i in range(k,n) if a[i][k]),None)
  if t is None:return None
  a[k],a[t]=a[t],a[k];u=pow(a[k][k],-1,p);a[k]=[v*u%p for v in a[k]]
  for i in range(n):
   if i!=k:
    u=a[i][k];a[i]=[(x-u*y)%p for x,y in zip(a[i],a[k])]
 return [r[n:] for r in a]
def cycles(s):
 seen=set();c=0
 for j in range(len(s)):
  if j in seen:continue
  c+=1
  while j not in seen:seen.add(j);j=s[j]
 return c
def diff_rank(s,t):
 ti=[0]*len(t)
 for i,v in enumerate(t):ti[v]=i
 return len(s)-cycles([ti[v] for v in s])
def green(s,a,p=P):
 # Cycle-wise recurrence formula valid for every permutation.
 n=len(s);G=[[0]*n for _ in range(n)]
 for j in range(n):
  cyc=[j];i=s[j]
  while i!=j:cyc.append(i);i=s[i]
  den=pow((1-pow(a,len(cyc),p))%p,-1,p);v=den
  for i in cyc:G[i][j]=v;v=v*a%p
 return G
def random_cycle(n,seed):
 a=list(range(n));random.Random(seed).shuffle(a);s=[0]*n
 for i in range(n):s[a[i]]=a[(i+1)%n]
 return s
def direct_fourier(n,p=P):
 w=pow(3,(p-1)//n,p);return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]

# Resolvent identity including characteristic divisibility and non-Hamiltonian permutations.
c=0
for p in [5,7,17,101]:
 for n in range(2,6):
  rng=random.Random(p*100+n)
  for trial in range(35):
   s=list(range(n));t=list(range(n));rng.shuffle(s);rng.shuffle(t)
   for a in range(1,min(p,5)):
    try:Gs=green(s,a,p);Gt=green(t,a,p)
    except ValueError:continue
    assert rank(sub(Gs,Gt,p),p)==diff_rank(s,t)
    assert mm(sub(eye(n),[[a*v for v in r] for r in perm(s)],p),Gs,p)==eye(n)
    c+=1
out['arbitrary_permutation_resolvent_checks']=c
# Source helper counterexample: its overwrite formula on identity permutation.
n=8;a=2
bad_scalar=pow(a,n-1,P)*pow((1-pow(a,n,P))%P,-1,P)%P
bad=[[bad_scalar*int(i==j)%P for j in range(n)] for i in range(n)]
z=[(j+1)%n for j in range(n)]
out['source_direct_green_counterexample']={'n':n,'p':P,'alpha':a,'reference':'identity','source_scalar':bad_scalar,'correct_scalar':pow(1-a,-1,P),'bad_difference_rank':rank(sub(green(z,a),bad)),'true_difference_rank':n-1,'residual_diagonal':((1-a)*bad_scalar-1)%P}
assert out['source_direct_green_counterexample']['bad_difference_rank']==8

out['all_affine']=[]
for n in [32,64,128,256]:
 s=random_cycle(n,2700+n);best=n;witness=None
 for u in range(1,n,2):
  for b in range(n):
   r=diff_rank(s,[(u*j+b)%n for j in range(n)])
   if r<best:best=r;witness=[u,b]
 assert best=={32:24,64:52,128:114,256:240}[n]
 out['all_affine'].append({'n':n,'references':n*n//2,'min_rank':best,'witness':witness})

# Exact integer Sylvester certificate, symmetric Bareiss derived afresh.
def positive_minors(A):
 a=[r[:] for r in A];n=len(a);den=1;ds=[]
 for k in range(n):
  d=a[k][k];assert d>0;ds.append(d)
  for i in range(k+1,n):
   for j in range(i,n):
    q,r=divmod(d*a[i][j]-a[i][k]*a[k][j],den);assert not r
    a[i][j]=q;a[j][i]=q
  for i in range(k+1,n):a[i][k]=a[k][i]=0
  den=d
 return ds
out['sylvester']=[]
for n in [32,64,128,256]:
 L=[[0]*n for _ in range(n)]
 for s in [[(j+1)%n for j in range(n)],random_cycle(n,2700+n)]:
  for j,k in enumerate(s):L[j][j]+=1;L[k][k]+=1;L[j][k]-=1;L[k][j]-=1
 K=[[2*n*L[i][j]+2-n*int(i==j) for j in range(n)] for i in range(n)]
 ds=positive_minors(K)
 out['sylvester'].append({'n':n,'positive_leading_minors':len(ds),'sha256':hashlib.sha256(';'.join(map(str,ds)).encode()).hexdigest(),'last_bits':ds[-1].bit_length()})

out['density']=[]
for n in [16,32,64,128]:
 t=list(range(n));t[0],t[n//4+1]=t[n//4+1],t[0];s=[t[(t[j]+1)%n] for j in range(n)];nonzero=0
 for a in range(n):
  for b in range(n):
   hist=[0]*(n//2)
   for j in range(n):
    k=(a*s[j]-b*j)%n;hist[k%(n//2)]+=1 if k<n//2 else -1
   nonzero+=any(hist)
 assert nonzero==n*n-3*n+4 and diff_rank(s,[(j+1)%n for j in range(n)])==2
 out['density'].append({'n':n,'nonzero':nonzero,'rank_gap':2})

# Cross-cut exact identity and full N=16 mixer audit.
c=0;out['mixer_cuts']=[]
for n in [4,6,8,16]:
 z=[(j+1)%n for j in range(n)];w=random_cycle(n,2700+n)
 G=green(z,pow(4,-1,P));H=green(w,pow(5,-1,P));M=[[(a+3*pow(2,-1,P)*b)%P for a,b in zip(r,s)] for r,s in zip(G,H)]
 mi=n
 for I in itertools.combinations(range(n),n//2):
  I=set(I);J=set(range(n))-I
  for s,Q in [(z,G),(w,H)]:
   cut=sum(s[j] in I for j in J)
   assert rank([[Q[i][j] for j in J] for i in I])==cut;c+=1
  mi=min(mi,rank([[M[i][j] for j in J] for i in I]))
 out['mixer_cuts'].append({'n':n,'cuts':math.comb(n,n//2),'minimum_rank':mi})
assert out['mixer_cuts'][-1]['minimum_rank']==4
out['cyclic_cut_rank_checks']=c

# Algebraic reconstruction directly from dense entries, no source oracle imports.
rng=random.Random(20251027);recovery=[]
for n in [4,8,16,32,64,128,256]:
 w=pow(3,(P-1)//n,P);roots={pow(w,i,P):i for i in range(n)}
 for trial in range(5):
  rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
  l=[rng.randrange(1,P) for _ in range(n)];r=[rng.randrange(1,P) for _ in range(n)]
  M=[[l[i]*r[j]*pow(w,rp[i]*cp[j],P)%P for j in range(n)] for i in range(n)]
  j=next(j for j in range(1,n) if math.gcd(cp[j]-cp[0],n)==1)
  aa=[roots[M[i][j]*M[0][0]*pow(M[i][0]*M[0][j],-1,P)%P] for i in range(n)]
  i=aa.index(1)
  bb=[roots[M[i][j]*M[0][0]*pow(M[i][0]*M[0][j],-1,P)%P] for j in range(n)]
  assert sorted(aa)==sorted(bb)==list(range(n))
  assert all(M[i][j]==M[i][0]*M[0][j]*pow(M[0][0],-1,P)*pow(w,aa[i]*bb[j],P)%P for i in range(n) for j in range(n))
 recovery.append({'n':n,'full_matrix_controls':5})
out['four_probe_reconstruction']=recovery
# Four structural probes do not certify equality; exact rank-one hidden corruption.
n=8;F=direct_fourier(n);M=[r[:] for r in F];M[7][7]=(M[7][7]+1)%P
assert all(M[i][j]==F[i][j] for i in range(n) for j in range(n) if i in [0,1] or j in [0,1])
out['probe_only_counterexample']={'n':n,'changed_entry':[7,7],'delta':1,'matching_rows':[0,1],'matching_columns':[0,1],'difference_rank':rank(sub(M,F))}

# Homogeneous intertwiner identities and two/three-stage witnesses.
def hom(n,a,b,d,p):return [[(a if i>j else b if i<j else d)%p for j in range(n)] for i in range(n)]
def inter(n,a,b,d,p):
 forward=b%p!=0;s=b if forward else a;o=a if forward else b
 K=[[0]*n for _ in range(n)]
 for i in range(n):K[i][(i+1)%n if forward else (i-1)%n]=s if (i<n-1 if forward else i>0) else o
 BB=[[(K[i][j]-s*int(i==j))%p for j in range(n)] for i in range(n)]
 AA=[[((d-s)*K[i][j]+s*(o-d)*int(i==j))%p for j in range(n)] for i in range(n)]
 return AA,BB,forward
c=0;homo=[]
for p,g in [(12289,11),(65537,3)]:
 for n in [8,16,32,64]:
  w=pow(g,(p-1)//n,p);assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
  FF=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
  for trial in range(32):
   pars=[]
   for k in range(3):
    a,b,d=[rng.randrange(p) for _ in range(3)]
    if trial%4==0:b=0;a=a or 1
    if trial%4==1:a=0;b=b or 1
    if trial%4==2:b=a or 1;a=b
    pars.append((a,b,d))
   HH=[hom(n,*v,p) for v in pars];AB=[inter(n,*v,p) for v in pars]
   for H,(A,BB,fwd) in zip(HH,AB):
    assert mm(BB,H,p)==mm(H,BB,p)==A;c+=1
   A1,B1,f1=AB[0];A3,B3,f3=AB[2];j=1 if f1 else 0
   v=[r[j] for r in A1];perm1=list(range(n));perm2=list(range(n));rng.shuffle(perm1);rng.shuffle(perm2)
   v=mv(HH[1],[v[k] for k in perm1],p);v=[v[k] for k in perm2];rhs=mv(A3,v,p)
   lhs=mv(B3,mv(FF,[r[j] for r in B1],p),p)
   idx=range(n-1) if f3 else range(1,n)
   assert len({lhs[i] for i in idx})==n-1
   assert len({rhs[i] for i in idx})<=13
   if n>=16:assert lhs!=rhs
  homo.append({'p':p,'n':n,'cases':32})
out['homogeneous_intertwiner_checks']=c;out['homogeneous_three_stage']=homo

# Broad asymmetric envelopes: support and Fourier polynomial constraints.
c=0
for p,g in [(12289,11),(65537,3)]:
 for n in [8,16,32,64]:
  w=pow(g,(p-1)//n,p)
  for trial in range(45):
   r=[rng.randrange(1,p) for _ in range(n)];ell=[rng.randrange(1,p) for _ in range(n)]
   u,v,b,e,d,dd=[[rng.randrange(p) for _ in range(n)] for k in range(6)]
   S1=[[u[i]*r[j]%p if i>j else v[i]*r[j]%p if i<j else d[i] for j in range(n)] for i in range(n)]
   S2=[[ell[i]*b[j]%p if i>j else ell[i]*e[j]%p if i<j else dd[i] for j in range(n)] for i in range(n)]
   gg=[rng.randrange(1,p) for _ in range(n)];hh=[rng.randrange(1,p) for _ in range(n)]
   perm1=list(range(n));rng.shuffle(perm1);left=[];right=[]
   for j in [0,1]:
    x=[0]*n;x[j]=pow(r[j],-1,p);x[j+1]=-pow(r[j+1],-1,p)%p
    y=mv(S1,x,p);assert all(y[i]==0 for i in range(n) if i not in [j,j+1])
    z=mv(S2,[y[k] for k in perm1],p);right.append([(z[i+1]*pow(ell[i+1],-1,p)-z[i]*pow(ell[i],-1,p))%p for i in range(n-1)])
    z=[gg[i]*sum(hh[k]*x[k]*pow(w,i*k,p) for k in range(n))%p for i in range(n)]
    left.append([(z[i+1]*pow(ell[i+1],-1,p)-z[i]*pow(ell[i],-1,p))%p for i in range(n-1)])
   assert sum(bool(a or b) for a,b in zip(*right))<=6
   assert sum(not(a or b) for a,b in zip(*left))<=2
   if n>=10:assert left!=right
   c+=1
out['asymmetric_envelope_cases']=c
# Twisted-circulant eigenvectors including diagonal singular choices.
c=0
for p,g in [(12289,11),(65537,3)]:
 for n in [4,8,16,32,64]:
  w=pow(g,(p-1)//n,p)
  for trial in range(12):
   q=rng.randrange(1,p)
   while pow(q,n,p)==1:q=rng.randrange(1,p)
   b=rng.randrange(1,p);a=b*pow(q,n,p)%p;d=rng.randrange(p);H=hom(n,a,b,d,p);ls=[]
   for k in range(n):
    z=q*pow(w,k,p)%p;lam=((d-b)*z+a-d)*pow(z-1,-1,p)%p;v=[pow(z,i,p) for i in range(n)]
    assert mv(H,v,p)==[lam*x%p for x in v];ls.append(lam);c+=1
   assert len(set(ls))==n
out['twisted_circulant_eigenvectors']=c
(B/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
