"""Independently authored reconstruction. Never imports/evaluates source programs."""
from pathlib import Path
import random, json, hashlib, itertools
ROOT=Path(__file__).resolve().parent
SOURCE=Path('novelty_catalogue_0825/library_delta_extracted/fft_green_research_phase39_2026-10-10/fft_green_phase39_bivariate')
FIELDS=[(998244353,3,(2,7,17)),(2013265921,31,(2,3,5))]

def mm(A,B,p):
 return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def inverse(A,p):
 n=len(A);R=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)];det=1
 for j in range(n):
  k=next((k for k in range(j,n) if R[k][j]),None)
  assert k is not None,'singular'
  if k!=j:R[k],R[j]=R[j],R[k];det=-det
  u=R[j][j];det=det*u%p;v=pow(u,-1,p);R[j]=[v*x%p for x in R[j]]
  for k in range(n):
   if k!=j:
    u=R[k][j];R[k]=[(x-u*y)%p for x,y in zip(R[k],R[j])]
 return [row[n:] for row in R],det

def rankdet(A,p):
 R=[row[:] for row in A];m=len(R);n=len(R[0]);idx=list(range(m));chosen=[];det=1;r=0
 for j in range(n):
  k=next((k for k in range(r,m) if R[k][j]),None)
  if k is None:continue
  R[r],R[k]=R[k],R[r];idx[r],idx[k]=idx[k],idx[r];chosen.append(idx[r])
  u=R[r][j];det=det*u%p;u=pow(u,-1,p)
  for k in range(r+1,m):
   t=R[k][j]*u%p
   for l in range(j+1,n):R[k][l]=(R[k][l]-t*R[r][l])%p
   R[k][j]=0
  r+=1
  if r==n:break
 # product is determinant of rows in chosen elimination order, not sorted order.
 return r,chosen,det

def orders(n):
 r=random.Random(37037+n);out=[]
 while len(out)<6:
  rest=list(range(1,n));r.shuffle(rest);c=[0]+rest
  if c not in out:out.append(c)
 if n==4:extra=out[0][:]
 else:
  r=random.Random(39039+n)
  while True:
   rest=list(range(1,n));r.shuffle(rest);extra=[0]+rest
   if extra not in out:break
 return out+[extra]

def build(n,p,g):
 cs=orders(n);ii=pow(g,(p-1)//4,p);w=pow(g,(p-1)//n,p)
 assert ii*ii%p==p-1 and pow(w,n,p)==1 and pow(w,n//2,p)!=1
 triples=[(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6),(1,3,11)]
 alphas=[(a+b*ii)*pow(d,-1,p)%p for a,b,d in triples]
 greens=[];den=[]
 # Define W directly, then invert I-alpha W. Avoid source's closed-form dense constructor.
 for cyc,alpha in zip(cs,alphas):
  W=[[int(i==j) for j in range(n)] for i in range(n)]
  for k in range(n):W[cyc[(k+1)%n]][cyc[k]]=(W[cyc[(k+1)%n]][cyc[k]]-alpha)%p
  G,d=inverse(W,p);assert d==(1-pow(alpha,n,p))%p
  greens.append(G);den.append(d)
 wa=(1+ii)*pow(3,-1,p)%p;wc=(1-ii)*pow(4,-1,p)%p
 A=[[(a+wa*b)%p for a,b in zip(r,s)] for r,s in zip(greens[0],greens[1])]
 C=[[(a+wc*b)%p for a,b in zip(r,s)] for r,s in zip(greens[4],greens[5])]
 Ai,ad=inverse(A,p);Ci,cd=inverse(C,p);F=[[pow(w,j*k,p) for k in range(n)] for j in range(n)]
 T=mm(mm(Ai,F,p),Ci,p);Bs=[greens[j] for j in (2,3,6)]
 return dict(n=n,p=p,g=g,T=T,Bs=Bs,cycles=cs,alphas=alphas,guards=dict(resolvent_determinants=den,outer_determinants=[ad,cd],target_nonzero=all(v for row in T for v in row),i=ii,root=w))

def mons(d,k=3):
 if k==1:return [(d,)]
 return [(j,)+rest for j in range(d,-1,-1) for rest in mons(d-j,k-1)]
def polys(inst,rs,cs,pairs,target=None):
 p=inst['p'];T=target or inst['T'];Bs=inst['Bs'];base=mons(2);out=[]
 def coeffprod(r,c,s,d):
  f={e:0 for e in base}
  for a,b in itertools.product(range(3),repeat=2):
   e=tuple(int(k==a)+int(k==b) for k in range(3));f[e]+=Bs[a][r][c]*Bs[b][s][d]
  return f
 for a,b in pairs:
  l=coeffprod(rs[1],cs[a],rs[0],cs[b]);r=coeffprod(rs[1],cs[b],rs[0],cs[a]);out.append({e:(T[0][a]*T[1][b]*l[e]-T[0][b]*T[1][a]*r[e])%p for e in base})
 return out

def macaulay(inst,rs,cs,degree,target=None):
 pairs=[(0,1),(0,2),(0,3),(1,2)] if degree==3 else [(0,1),(0,2),(1,3)]
 out=mons(degree);ix={e:j for j,e in enumerate(out)};rows=[]
 for poly in polys(inst,rs,cs,pairs,target):
  for m in mons(degree-2):
   row=[0]*len(out)
   for e,v in poly.items():row[ix[tuple(a+b for a,b in zip(e,m))]]=v
   rows.append(row)
 return rows

def main():
 report={'method':'direct inversion of sparse I-alpha W; independently authored arithmetic; source files inert only','records':[],'controls':[]}
 for p,g,factors in FIELDS:
  # Trial division primality is bounded and exact; generator is checked against complete prime factors of p-1.
  assert all(p%d for d in range(2,int(p**0.5)+1));assert all(pow(g,(p-1)//q,p)!=1 for q in factors)
  for n in (4,8,16,32):
   inst=build(n,p,g);name=f'fresh_N{n}_p{p}.json';(ROOT/name).write_text(json.dumps(inst,indent=2)+'\n')
   lines=[f'{n} {p}']+[' '.join(map(str,row)) for M in [inst['T']]+inst['Bs'] for row in M]
   txt='\n'.join(lines)+'\n';(ROOT/name.replace('.json','.txt')).write_text(txt)
   original=(SOURCE/f'instances/phase39_N{n}_p{p}.txt').read_text();matches=list(map(int,txt.split()))==list(map(int,original.split()));assert matches
   fixed=[]
   for degree in (3,4):
    K=macaulay(inst,(0,1),(0,1,2,3),degree);r,idx,det=rankdet(K,p);assert r==len(K[0]);fixed.append(dict(degree=degree,rank=r,minor_rows_ordered=idx,determinant=det))
   # Explicit planted middle factorization: all minors must vanish at x=(1,7,11), regardless of masks.
   rs=list(reversed(range(n)));cs=list(range(1,n))+[0];x=(1,7,11)
   B=[[sum(x[k]*inst['Bs'][k][i][j] for k in range(3))%p for j in range(n)] for i in range(n)]
   T=[[(i+2)*(j+3)*B[rs[i]][cs[j]]%p for j in range(n)] for i in range(n)]
   plant=[]
   for degree in (3,4):
    K=macaulay(inst,rs[:2],cs[:4],degree,T);r,_,_=rankdet(K,p);assert r<len(K[0]);plant.append(r)
   for f in polys(inst,rs[:2],cs[:4],list(itertools.combinations(range(4),2)),T):assert sum(v*pow(x[0],e[0],p)*pow(x[1],e[1],p)*pow(x[2],e[2],p) for e,v in f.items())%p==0
   # Anchor forms' cross product gives a projective basepoint for three anchor quadrics.
   a=[M[0][0] for M in inst['Bs']];b=[M[1][0] for M in inst['Bs']];z=[(a[(k+1)%3]*b[(k+2)%3]-a[(k+2)%3]*b[(k+1)%3])%p for k in range(3)];assert any(z)
   for f in polys(inst,(0,1),(0,1,2,3),[(0,1),(0,2),(0,3)]):assert sum(v*pow(z[0],e[0],p)*pow(z[1],e[1],p)*pow(z[2],e[2],p) for e,v in f.items())%p==0
   record=dict(N=n,prime=p,source_instance_matches=matches,guards=inst['guards'],cycles=inst['cycles'],fixed_witnesses=fixed,planted_ranks=plant,anchor_basepoint=z)
   report['records'].append(record)
 (ROOT/'fresh_reconstruction_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'instances':len(report['records']),'all_source_instances_match':True,'all_guards_checked':True}))
if __name__=='__main__':main()
