"""Independent standard-library verification; no SymPy or predecessor code.
Reads JSON data only. Validates row-elimination identities and the proof DAG.
Coefficients are exact rationals in the abstract ring Q[z]/(z^4+1).
"""
import json,hashlib,os,sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__))
ZERO=(F(0),)*4;ONE=(F(1),F(0),F(0),F(0));Z=(F(0),F(1),F(0),F(0))
def ca(a,b):return tuple(x+y for x,y in zip(a,b))
def cn(a):return tuple(-x for x in a)
def cm(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[(i+j)%4]+=x*y*(-1 if i+j>=4 else 1)
 return tuple(out)
def ci(a):
 # Invert by a fresh exact 4-by-4 Gaussian elimination.
 columns=[cm(a,tuple(F(j==i)for j in range(4)))for i in range(4)]
 A=[[columns[j][i]for j in range(4)]+[F(i==0)]for i in range(4)]
 for j in range(4):
  p=next(i for i in range(j,4)if A[i][j]);A[j],A[p]=A[p],A[j]
  d=A[j][j];A[j]=[x/d for x in A[j]]
  for i in range(4):
   if i!=j:
    d=A[i][j];A[i]=[x-d*y for x,y in zip(A[i],A[j])]
 return tuple(A[i][4]for i in range(4))
N=5;EXPZERO=(0,)*N
PONE={EXPZERO:ONE}
def pc(c):return {EXPZERO:c}if c!=ZERO else {}
def pv(j):
 e=[0]*N;e[j]=1;return {tuple(e):ONE}
def pa(a,b):
 c=dict(a)
 for e,v in b.items():
  q=ca(c.get(e,ZERO),v)
  if q==ZERO:c.pop(e,None)
  else:c[e]=q
 return c
def pn(a):return {e:cn(c)for e,c in a.items()}
def ps(a,b):return pa(a,pn(b))
def pm(a,b):
 out={}
 for e,c in a.items():
  for f,d in b.items():
   ef=tuple(x+y for x,y in zip(e,f));v=ca(out.get(ef,ZERO),cm(c,d))
   if v==ZERO:out.pop(ef,None)
   else:out[ef]=v
 return out
def scale(a,c):return {e:cm(v,c)for e,v in a.items()if cm(v,c)!=ZERO}
def loadpoly(raw):
 out={}
 for e,cs in raw:
  c=tuple([F(*q)for q in cs]+[F(0)]*(4-len(cs)))
  if c!=ZERO:out[tuple(e)]=c
 return out
def pp(a,n):
 b=PONE
 for _ in range(n):b=pm(b,a)
 return b

def proportional(a,b):
 assert a and b and set(a)==set(b)
 e=next(iter(a));c=cm(a[e],ci(b[e]));assert c!=ZERO and a==scale(b,c)
 return c

D=json.load(open(os.path.join(HERE,'EXACT_UNIT_CERTIFICATE.json')))
assert D['variables']==['t0','t1','t2','t3','w']
t=[pv(j)for j in range(4)];w=pv(4)
zp=[ONE]
for j in range(1,8):zp.append(cm(zp[-1],Z))
assert cm(zp[-1],Z)==ONE and zp[4]==cn(ONE)
M=[]
for r in range(8):
 row=[]
 for j in range(8):
  a=j-j%2
  row.append(pa(pc(zp[r*a%8]),scale(t[j//2],zp[r*(a+1)%8] if j%2==0 else cn(zp[r*(a+1)%8]))))
 M.append(row)
B=[pa(M[0][j],pm(w,M[7][j]))for j in range(8)]
sigma=[2,7,5,0,6,1,3,4]
# Each selected pair consists of columns whose pivot is 0 and whose row is off-support.
specs=[]
for r in range(1,8):
 cols=[j for j in [1,2,4,5,6]if r not in [j,(j+1)%8,sigma[j]]]
 for ia,j in enumerate(cols):
  for k in cols[ia+1:]:
   guards=[]
   if r==1:guards.append(w)
   if (j,k)==(4,6):guards.append(B[6])
   if (j,k)==(1,5):guards.append(B[1])
   if (j,k)==(2,5):guards.append(B[5])
   specs.append((r,j,k,guards))
inputs=[loadpoly(f)for f in D['inputs']];assert len(inputs)==20
scalars=[]
for idx,(r,j,k,guards)in enumerate(specs):
 for c in [j,k]:assert r not in [c,(c+1)%8,sigma[c]] and c in [1,2,4,5,6]
 def bc(c):
  return (ps(pm(B[sigma[c]],M[r][c]),pm(B[c],M[r][sigma[c]])),ps(pm(B[sigma[c]],M[r-1][c]),pm(B[c],M[r-1][sigma[c]])))
 bj,cj=bc(j);bk,ck=bc(k);resultant=ps(pm(bj,ck),pm(bk,cj))
 right=inputs[idx]
 for g in guards:right=pm(right,g)
 scalar=proportional(resultant,right);scalars.append([[q.numerator,q.denominator]for q in scalar])
print('PASS: twenty fresh Fourier row-elimination identities, with only w, B1, B5, B6 divided.')
verified={};termops=0
for key,node in sorted(D['nodes'].items(),key=lambda kv:int(kv[0])):
 idx=int(key);p=loadpoly(node['polynomial'])
 if idx<20:
  assert node['combination']==[] and p==inputs[idx]
 else:
  result={}
  for parent,mult in node['combination']:
   assert parent<idx and parent in verified
   result=pa(result,pm(loadpoly(mult),verified[parent]));termops+=1
  assert result==p,('invalid node',idx)
 verified[idx]=p
assert verified[D['final_node']]==PONE
print('PASS: exact linear-combination proof DAG ends in 1; %d nodes, %d combination terms.'%(len(verified),termops))
# Controls exercise arithmetic, exact field embedding, and rejection of certificate corruption.
for a in [ONE,Z,ca(ONE,Z),ca(ONE,zp[2]),(F(2),F(3),F(5),F(7))]:assert cm(a,ci(a))==ONE
last=verified[D['final_node']];bad=pa(last,pc(Z));assert bad!=PONE
assert ps(pm(pa(pv(0),pc(Z)),ps(pv(0),pc(Z))),ps(pp(pv(0),2),pc(zp[2])))=={}
print('PASS: coefficient inversion and polynomial positive controls, and perturbed-final negative control.')
report={'status':'verified exact characteristic-zero open-chart obstruction','field':'Q[z]/(z^4+1); no numerical embedding is assumed','necessary_nonzero_guards':['u0','B1','B5','B6'],'selected_minors':[[r,j,k]for r,j,k,g in specs],'normalization_scalars':scalars,'proof_nodes':len(verified),'combination_terms':termops,'final_constant':1,'source_sha256':hashlib.sha256(open(os.path.join(HERE,'EXACT_UNIT_CERTIFICATE.json'),'rb').read()).hexdigest()}
json.dump(report,open(os.path.join(HERE,'VERIFICATION_REPORT.json'),'w'),indent=2)

# Exact symbolic reconciliation to the exported adjacent-anchor interface.
source=os.path.join(HERE,'ADJACENT_ANCHOR_ORBIT_SYSTEM.json')
original=json.load(open(source));N=12;EXPZERO=(0,)*N;PONE={EXPZERO:ONE}
t=[pv(j)for j in range(4)];u=[pv(j+4)for j in range(8)]
M=[]
for r in range(8):
 M.append([pa(pc(zp[r*(j-j%2)%8]),scale(t[j//2],zp[r*(j-j%2+1)%8]if j%2==0 else cn(zp[r*(j-j%2+1)%8])))for j in range(8)])
A=[[pa(M[r][j],pm(u[r],M[(r-1)%8][j]))for j in range(8)]for r in range(8)]
pivot=[3,0,0,1,0,0,0,1];a=[A[pivot[j]][j]for j in range(8)];c=[A[pivot[j]][sigma[j]]for j in range(8)]
h=[[ps(pm(c[j],A[r][j]),pm(a[j],A[r][sigma[j]]))for j in range(8)]for r in range(8)]
fresh={**{'a_'+str(j):a[j]for j in range(8)},**{'c_'+str(j):c[j]for j in range(8)},**{'h_%d_%d'%(r,j):h[r][j]for r in range(8)for j in range(8)}}
for i in range(8):
 l=sigma.index(i);n=(i+1)%8
 fresh['diag_'+str(i)]=ps(pa(pm(pm(u[n],a[l]),h[i][i]),pm(pm(c[i],u[n]),h[i][l])),pm(a[l],h[n][i]))
for label,terms in original['polynomials'].items():
 exact={tuple(e):tuple(F(x)for x in co)for e,co in terms}
 assert exact==fresh[label],('export mismatch',label)
assert len(fresh)==88 and len(original['zero_equations'])==40
for r,j,k,guards in specs:
 for cc in [j,k]:assert 'h_%d_%d'%(r,cc)in original['zero_equations']
print('PASS: all 88 exported polynomials exactly match fresh symbolic formulas; all used minors occur among the 40 equations.')
report['interface_polynomials_verified']=88
json.dump(report,open(os.path.join(HERE,'VERIFICATION_REPORT.json'),'w'),indent=2)
