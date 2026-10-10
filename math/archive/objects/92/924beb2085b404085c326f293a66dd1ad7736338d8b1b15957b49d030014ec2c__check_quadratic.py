"""Fresh reconstruction from inert integer Green data, with polarization and
polynomial determinant expansion. No supplied executable program is used.
"""
from pathlib import Path
from itertools import combinations,permutations
from math import gcd
import json,hashlib
from own_modular import eye,add,sub,mul,rank,determinant
D=Path(__file__).resolve().parent

def invring(a,mod):
 n=len(a);t=[r[:]+e for r,e in zip(a,eye(n))]
 for k in range(n):
  s=next(i for i in range(k,n) if gcd(t[i][k],mod)==1);t[k],t[s]=t[s],t[k]
  z=pow(t[k][k],-1,mod);t[k]=[x*z%mod for x in t[k]]
  for i in range(n):
   if i!=k:
    z=t[i][k];t[i]=[(x-z*y)%mod for x,y in zip(t[i],t[k])]
 return [r[n:] for r in t]
def branch(b,mod):
 n=len(b['cycle']);q=eye(n)
 for i in range(n):q[i][b['cycle'][i]]=(q[i][b['cycle'][i]]-b['weights'][i])%mod
 g=invring(q,mod)
 g=[[b['left_diag'][i]*g[i][j]*b['right_diag'][j]%mod for j in range(n)] for i in range(n)]
 return [[g[b['row_permutation'][i]][b['col_permutation'][j]] for j in range(n)] for i in range(n)]
def stages(c,mod,t=1):
 aa=[branch(b,mod) for b in c['trace_A']];bb=[branch(b,mod) for b in c['trace_B']]
 aa=add(*aa,mod);base=add(*bb,mod)
 out=[r[:] for r in base]
 for i in range(c['n']):out[i][0]=(out[i][0]+(t-1)*bb[0][i][0])%mod
 return aa,out,bb

def comm_at(c,t,w,mod):
 A,B,_=stages(c,mod,t);ai=invring(A,mod);n=c['n'];ts=[]
 for j in [1,2]:
  v=[B[i][0]*pow(B[i][j],-1,mod)%mod for i in range(n)]
  diag=[[int(i==k)*v[i] for k in range(n)] for i in range(n)]
  T=mul(mul(A,diag,mod),ai,mod)
  T=[[T[i][k]*pow(w,j*k,mod)%mod for k in range(n)] for i in range(n)];ts.append(T)
 return sub(mul(ts[0],ts[1],mod),mul(ts[1],ts[0],mod),mod)
def padd(a,b,p):return [( (a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))]
def pmul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c
def pdet(a,p):
 n=len(a);out=[0]
 for perm in permutations(range(n)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=[sign%p]
  for i in range(n):term=pmul(term,a[i][perm[i]],p)
  out=padd(out,term,p)
 return out

def det_no_div(a,mod):return pdet([[[x] for x in row] for row in a],mod)[0]
results=[]
for n in [3,4]:
 c=json.loads((D/f'source_inputs/CERT_N{n}.json').read_text());p=c['prime'];w=c['root'];A,B,bb=stages(c,p)
 assert (A,B)==(c['A'],c['B']) and bb==[c['gB1'],c['gB2']]
 invring(A,p);invring(B,p);assert all(x for row in B for x in row)
 ai=invring(A,p);ps=[[[ai[u][a]*pow(w,a*j,p)*pow(B[u][j],-1,p)%p for a in range(n)] for u in range(n)] for j in range(3)]
 invring(ps[0],p)
 def minors(cvec):
  z=[[sum(ps[j][u][a]*cvec[a] for a in range(n))%p for j in range(3)] for u in range(n)]
  return [(z[u][j]*z[v][k]-z[u][k]*z[v][j])%p for j,k in combinations(range(3),2) for u,v in combinations(range(n),2)]
 es=eye(n);diagcols=[minors(e) for e in es];cols=[]
 for a in range(n):
  for b in range(a,n):
   if a==b:cols.append(diagcols[a])
   else:
    v=[int(i==a)+int(i==b) for i in range(n)];vv=minors(v)
    cols.append([(x-y-z)%p for x,y,z in zip(vv,diagcols[a],diagcols[b])])
 Q=[list(r) for r in zip(*cols)]
 assert Q==c['original_Q'];assert rank(Q,p)==n*(n+1)//2==c['quadratic_rank']
 comm=comm_at(c,1,w,p);assert comm==c['original_commutator'] and det_no_div(comm,p)==0
 # Determine commutator polynomial by three degree-two evaluations then expand determinant.
 k0,k1,k2=[comm_at(c,t,w,p) for t in [0,1,2]]
 poly=[]
 for i in range(n):
  row=[]
  for j in range(n):
   c2=(k2[i][j]-2*k1[i][j]+k0[i][j])*pow(2,-1,p)%p;c1=(k1[i][j]-k0[i][j]-c2)%p
   row.append([k0[i][j],c1,c2])
  poly.append(row)
 f=pdet(poly,p);assert f==c['polynomial_modp']
 derivative=sum(i*x for i,x in enumerate(f))%p;assert derivative==c['derivative_modp'] and derivative
 # Build a maximal minor via incremental row-independence.
 selected=[];rr=0
 for i,row in enumerate(Q):
  nr=rank([Q[t] for t in selected]+[row],p)
  if nr>rr:selected.append(i);rr=nr
  if rr==len(Q[0]):break
 md=determinant([Q[t] for t in selected],p);assert md
 lifts=[{'modulus':p,'lifted_root_t':1,'lifted_Fourier_root_omega':w}];tt=1;ww=w;old=p
 for step in range(2,5):
  new=old*p
  quotient=((pow(ww,n,new)-1)%new)//old
  ww=(ww+old*(-quotient*pow(n*pow(ww,n-1,p)%p,-1,p)%p))%new
  assert pow(ww,n,new)==1
  val=det_no_div(comm_at(c,tt,ww,new),new);assert val%old==0
  tt=(tt+old*(-(val//old)*pow(derivative,-1,p)%p))%new
  assert det_no_div(comm_at(c,tt,ww,new),new)==0
  lifts.append({'modulus':new,'lifted_root_t':tt,'lifted_Fourier_root_omega':ww});old=new
 saved=json.loads((D/'source_inputs/HENSEL_RESULTS.json').read_text())[str(n)];assert lifts==saved
 results.append({'N':n,'field':p,'root':w,'branch_reconstructions':4,'lift_matrix_shape':[len(Q),len(Q[0])],'lift_rank':rr,'selected_minor_rows':selected,'selected_minor_det':md,'commutator_det':0,'commutator_polynomial':f,'derivative_at1':derivative,'hensel_lifts':lifts})
out={'status':'PASS','certificates':results,'method':'Fresh sparse inverse reconstruction; quadratic coefficients by polarization; determinant polynomial from degree-two commutator interpolation and Leibniz determinant expansion; independent Hensel digit corrections.','supplied_programs_executed':False,'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (D/'source_inputs').glob('*.json')}}
(D/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
