"""Reviewer-authored exact backend reconstruction; no submitted program imported or run."""
import sympy as S, itertools, json, pathlib
from fractions import Fraction
x=S.Symbol('x');phi=S.cyclotomic_poly(60,x)
def red(a):return S.rem(S.expand(a),phi,x)
u=x**20;v=x**12;j=x**15
D3=[1,-S.Rational(3,2),(u-u**2)/2];D4=[1,1,1,j]
c1=(v+v**4)/2;c2=(v**2+v**3)/2;h1=(v-v**4)/2;h2=(v**2-v**3)/2
D5=[1,(c1+c2)/2-1,(c1-c2)/2,h1,h2-h1,h1+h2]
B3=[[1,1,1],[0,1,1],[0,1,-1]];A3=[[1,0,0],[1,1,1],[1,1,-1]]
B4=[[1,0,1,0],[0,1,0,1],[1,0,-1,0],[0,1,0,-1]];A4=[[1,1,0,0],[0,0,1,1],[1,-1,0,0],[0,0,1,-1]]
B5=[[1,1,1,1,1],[0,1,1,1,1],[0,1,-1,-1,1],[0,1,1,-1,-1],[0,0,1,-1,0],[0,1,0,0,-1]]
A5=[[1,0,0,0,0,0],[1,1,1,1,1,0],[1,1,-1,-1,0,1],[1,1,-1,1,0,-1],[1,1,1,-1,-1,0]]
entries=0
for n,A,D,B in [(3,A3,D3,B3),(4,A4,D4,B4),(5,A5,D5,B5)]:
 for r in range(n):
  for c in range(n):
   assert red(sum(A[r][t]*D[t]*B[t][c] for t in range(len(D)))-x**((60//n)*r*c))==0;entries+=1
coeffs={(a,b,c):red(D5[a]*D3[b]*D4[c]) for a in range(6) for b in range(3) for c in range(4)}
ident=[k for k,vv in coeffs.items() if vv==1]; assert ident==[(0,0,0),(0,0,1),(0,0,2)]
# CRT labels are independently enumerated, with a direct exponent check for all 3600 pairs.
js={(a,b,c):(40*a+36*b+45*c)%60 for a in range(3) for b in range(5) for c in range(4)}
ks={(a,b,c):(20*a+12*b+15*c)%60 for a in range(3) for b in range(5) for c in range(4)}
assert len(set(js.values()))==len(set(ks.values()))==60
for (a,b,c),jj in js.items():
 for (aa,bb,cc),kk in ks.items():assert (jj*kk-20*a*aa-12*b*bb-15*c*cc)%60==0

def ev(f,p,r):
 return sum(int(co.p)*pow(int(co.q),p-2,p)*pow(r,ex[0],p) for ex,co in S.Poly(f,x).terms())%p
p=61;root=2; assert pow(root,60,p)==1 and all(pow(root,60//d,p)!=1 for d in [2,3,5])
ids61=[key for key,vv in coeffs.items() if ev(vv,p,root)==1]
ids15=[(a,b) for a in range(6) for b in range(3) if ev(red(D5[a]*D3[b]),p,root)==1]
assert len(ids61)==6 and ids15==[(0,0),(3,2)]
# Six pre orders and six post orders, with dimension-changing tensor lanes charged explicitly.
params={3:(3,3,3,3),4:(4,4,4,4),5:(5,6,8,9)}
pre=[];post=[]
for order in itertools.permutations(params):
 size=60;cost=0
 for k in order:n,r,a,b=params[k];cost+=size//n*a;size=size//n*r
 assert size==72;pre.append((order,cost))
 size=72;cost=0
 for k in order:n,r,a,b=params[k];cost+=size//r*b;size=size//r*n
 assert size==60;post.append((order,cost))
sums=[a+b for _,a in pre for _,b in post];assert min(sums)==444 and max(sums)==492
assert S.Matrix(A4).T*S.Matrix(A4)==2*S.eye(4) and S.Matrix(B4).T*S.Matrix(B4)==2*S.eye(4)
# Rebuild annihilator coefficients by multiplying geometric factors, then test the proposed recurrences and zeros.
bound=[]
for N,a,b,p,w in [(45,11,11,181,16),(45,11,11,181,3),(49,12,12,197,16),(53,13,13,107,4),(53,13,13,107,3)]:
 q=pow(w,p-2,p);m=2*b;A0=a+1;cs=[1]
 for r in range(m):
  root=pow(q,A0+r,p);ncs=[0]*(len(cs)+1)
  for i,c in enumerate(cs):ncs[i]=(ncs[i]-root*c)%p;ncs[i+1]=(ncs[i+1]+c)%p
  cs=ncs
 assert len(cs)==m+1
 for r in range(m):
  ratio=(-pow(q,-(A0+m-r-1),p)*(1-pow(q,m-r,p))*pow((1-pow(q,r+1,p))%p,p-2,p))%p
  assert cs[r+1]==cs[r]*ratio%p
 hs={s:cs[s+b]*pow(q,s*(s-1)//2,p)%p for s in range(-b,b+1)}
 ls=[sum(c*pow(q,k*s,p) for s,c in hs.items())%p for k in range(N)]
 for k in range(N):assert (ls[k]-(pow(q,b,p)+pow(q,k-a,p))*ls[(k+1)%N]+pow(q,k-a-b,p)*ls[(k+2)%N])%p==0
 bound.append({'N':N,'p':p,'omega':w,'zeros':[i for i,vv in enumerate(ls) if vv==0],'coefficient_and_spectral_recurrences':True})
res={'short_entries_exact':entries,'CRT_entries_exact':3600,'complex_identity_positions':ident,'p61_identity_positions':ids61,'p61_F15_identity_positions':ids15,'addition_min':min(sums),'addition_max':max(sums),'boundary_controls':bound}
pathlib.Path('research_cycle_0958/review/supplement_v1/reviewer_backend_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res))
