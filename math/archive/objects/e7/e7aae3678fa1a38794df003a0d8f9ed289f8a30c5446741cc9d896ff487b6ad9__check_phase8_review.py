#!/usr/bin/env python3
"""Independent exact Phase8 audit; no source module imports."""
import json,math,random,hashlib
from pathlib import Path
def field(n):
 p=n+1
 while any(p%d==0 for d in range(2,math.isqrt(p)+1)):p+=n
 for w in range(2,p):
  if pow(w,n,p)==1 and pow(w,n//2,p)!=1:return p,w
 raise AssertionError
def dft(x,w,p):return [sum(v*pow(w,-j*t,p) for t,v in enumerate(x))%p for j in range(len(x))]
def fit(features,targets,p):
 if not features:return []
 s=len(features[0]);A=[list(f)+[y%p] for f,y in zip(features,targets)];piv=[];r=0
 for j in range(s):
  q=next((i for i in range(r,len(A)) if A[i][j]%p),None)
  if q is None:continue
  A[q],A[r]=A[r],A[q];v=pow(A[r][j],-1,p);A[r]=[x*v%p for x in A[r]]
  for i in range(len(A)):
   if i!=r:
    z=A[i][j];A[i]=[(x-z*y)%p for x,y in zip(A[i],A[r])]
  piv.append(j);r+=1
 if any(not any(row[:s]) and row[s] for row in A):return None
 ans=[0]*s
 for i,j in enumerate(piv):ans[j]=A[i][s]
 assert all(sum(a*b for a,b in zip(f,ans))%p==y%p for f,y in zip(features,targets))
 return ans
def rank(A,p):
 A=[row[:] for row in A];r=0
 for j in range(len(A[0])):
  i=next((i for i in range(r,len(A)) if A[i][j]%p),None)
  if i is None:continue
  A[r],A[i]=A[i],A[r];iv=pow(A[r][j],-1,p);A[r]=[x*iv%p for x in A[r]]
  for i in range(r+1,len(A)):
   z=A[i][j];A[i]=[(x-z*y)%p for x,y in zip(A[i],A[r])]
  r+=1
  if r==len(A):break
 return r
def columns_to_raw(cols):return [cols[t][b] for b in range(len(cols[0])) for t in range(len(cols))]
def synth_circ(initial,taps,shifts,m,p):
 cols=[row[:] for row in initial];r=len(taps);k=len(cols[0])
 for t in range(r,m):cols.append([sum(taps[h-1][i]*cols[t-h][(b+d)%k] for h in range(1,r+1) for i,d in enumerate(shifts))%p for b in range(k)])
 return cols
def rational(cols,r,shifts,w,p):
 m=len(cols);k=len(cols[0]);n=k*m;wk=pow(w,m,p)
 features=[];targets=[]
 for t in range(r,m):
  for b in range(k):features.append([cols[t-h][(b+d)%k] for h in range(1,r+1) for d in shifts]);targets.append(cols[t][b])
 co=fit(features,targets,p) if features else [0]*(r*len(shifts))
 if co is None:return None,0,None
 init=[dft(cols[t],wk,p) for t in range(r)];ans=[0]*n;sing=0
 for ell in range(k):
  coeff=[sum(co[h*len(shifts)+i]*pow(wk,ell*d,p) for i,d in enumerate(shifts))%p for h in range(r)]
  seq=[init[t][ell] for t in range(r)]
  for t in range(r,m):seq.append(sum(coeff[h-1]*seq[t-h] for h in range(1,r+1))%p)
  front=[(seq[u]-sum(coeff[h-1]*seq[u-h] for h in range(1,u+1)))%p for u in range(r)]
  back=[-sum(coeff[h-1]*seq[m+u-h] for h in range(u+1,r+1))%p for u in range(r)]
  local_sing=0
  for j in range(m):
   z=pow(w,-ell-j*k,p);den=(1-sum(coeff[h-1]*pow(z,h,p) for h in range(1,r+1)))%p
   direct=sum(v*pow(z,t,p) for t,v in enumerate(seq))%p
   top=sum((front[u]+pow(wk,-ell,p)*back[u])*pow(z,u,p) for u in range(r))%p
   assert den*direct%p==top
   if den:got=top*pow(den,-1,p)%p
   else:got=direct;local_sing+=1
   ans[ell+j*k]=got
  assert local_sing<=r;sing+=local_sing
 return ans,sing,co
def infer_shift(cols,w,p):
 k=len(cols[0]);m=len(cols);wk=pow(w,m,p)
 a=[sum(cols[0][b]*pow(wk,-ell*b,p) for b in range(k))%p for ell in range(3)]
 b=[sum(cols[1][u]*pow(wk,-ell*u,p) for u in range(k))%p for ell in range(3)]
 if not all(a):return None
 lam=[x*pow(y,-1,p)%p for x,y in zip(b,a)];dif=(lam[1]-lam[0])%p
 if not dif:return None
 q=(lam[2]-lam[1])*pow(dif,-1,p)%p
 return next((d for d in range(1,k) if pow(wk,d,p)==q),None)
def synth_weyl(seed,controls,dictionary,wk,p):
 cols=[seed[:]];k=len(seed)
 for controls_t in controls:cols.append([sum(c*pow(wk,q*b,p)*cols[-1][(b+a)%k] for c,(a,q) in zip(controls_t,dictionary))%p for b in range(k)])
 return cols
def weyl(cols,dictionary,w,p):
 m=len(cols);k=len(cols[0]);wk=pow(w,m,p);co=[]
 for t in range(m-1):
  feats=[[pow(wk,q*b,p)*cols[t][(b+a)%k]%p for a,q in dictionary] for b in range(k)]
  fitco=fit(feats,cols[t+1],p)
  if fitco is None:return None
  co.append(fitco)
 F=[dft(cols[0],wk,p)]
 for ct in co:F.append([sum(c*pow(wk,(ell-q)*a,p)*F[-1][(ell-q)%k] for c,(a,q) in zip(ct,dictionary))%p for ell in range(k)])
 assert F==[dft(col,wk,p) for col in cols]
 ans=[0]*(k*m)
 for ell in range(k):
  out=dft([F[t][ell]*pow(w,-ell*t,p)%p for t in range(m)],pow(w,k,p),p)
  for j in range(m):ans[ell+j*k]=out[j]
 return ans
def orbit_equal(f,v,p):
 if not any(f):return not any(v)
 for d in range(len(f)):
  b=next(i for i in range(len(f)) if f[(i+d)%len(f)])
  if not v[b]:continue
  if all((v[i]*f[(b+d)%len(f)]-v[b]*f[(i+d)%len(f)])%p==0 for i in range(len(f))):return True
 return False
def properties(cols,w,p):
 m=len(cols);k=len(cols[0]);raw=columns_to_raw(cols);n=k*m
 V=[[raw[b*m+t]*pow(w,t*(t-1)//2+m*b*t,p)%p for t in range(m)] for b in range(k)]
 phase=[dft(row,pow(w,k,p),p) for row in V];refs=[]
 for t in range(m):
  col=[V[b][t] for b in range(k)]
  if not any(orbit_equal(f,col,p) for f in refs):refs.append(col)
 return {'nonzero_input_count':sum(bool(v) for v in raw),'ordinary_polyphase_rank':rank([[cols[t][b] for t in range(m)] for b in range(k)],p),'phase7_dechirped_rank':rank(V,p),'active_green_modes':sum(any(phase[b][t] for b in range(k)) for t in range(m)),'phase7_projective_cyclic_shift_orbits':len(refs),'hankel_rank':rank([[raw[i+j] for j in range(n//2)] for i in range(n//2)],p),'input_sha256':hashlib.sha256(','.join(map(str,raw)).encode()).hexdigest()}
def run():
 rng=random.Random(202610092220);out={'rational_cases':0,'weyl_cases':0,'full_output_bins':0,'singular_rational_outputs':0,'unknown_shift_identifications':0,'exact_witnesses':[],'control_convolution_checks':0}
 for k,m in [(4,2),(4,4),(8,4),(8,8),(16,4),(16,8),(32,8)]:
  p,w=field(k*m);wk=pow(w,m,p)
  for r in range(1,min(3,m-1)+1):
   for rep in range(4):
    shifts=[0,1];initial=[[rng.randrange(p) for _ in range(k)] for _ in range(r)];taps=[[rng.randrange(p) for _ in shifts] for h in range(r)]
    if rep==0:
     taps=[[0,0] for _ in range(r)];taps[0][0]=1
    if r==2 and rep==1:taps=[[2,0],[-1%p,0]]
    cols=synth_circ(initial,taps,shifts,m,p);ans,sing,_=rational(cols,r,shifts,w,p)
    assert ans==dft(columns_to_raw(cols),w,p)
    out['rational_cases']+=1;out['full_output_bins']+=k*m;out['singular_rational_outputs']+=sing
  for rep in range(4):
   seed=[rng.randrange(p) for _ in range(k)];d=rng.randrange(1,k);cols=synth_circ([seed],[[3,1]],[0,d],m,p)
   inferred=infer_shift(cols,w,p)
   if inferred is not None:assert inferred==d;out['unknown_shift_identifications']+=1
   dictionary=[(1,0),(0,1)];controls=[[rng.randrange(p),rng.randrange(p)] for t in range(m-1)];cols=synth_weyl(seed,controls,dictionary,wk,p)
   assert weyl(cols,dictionary,w,p)==dft(columns_to_raw(cols),w,p);out['weyl_cases']+=1;out['full_output_bins']+=k*m
   g=[rng.randrange(p) for _ in range(k)];u=[rng.randrange(p) for _ in range(k)];G=dft(g,wk,p);U=dft(u,wk,p)
   assert dft([a*b%p for a,b in zip(g,u)],wk,p)==[sum(G[j]*U[(ell-j)%k] for j in range(k))*pow(k,-1,p)%p for ell in range(k)];out['control_convolution_checks']+=1
 # Reconstruct the three saved source witnesses from their explicit seeded parameter recipe only.
 p=2013265921;k=16;m=8;w=pow(31,(p-1)//128,p);wk=pow(w,m,p);rng=random.Random(8776)
 seed=[rng.randrange(1,p) for _ in range(k)];A=synth_circ([seed],[[3,11]],[0,5],m,p)
 initial=[[rng.randrange(1,p) for _ in range(k)] for _ in range(2)];B=synth_circ(initial,[[13,11],[7,17]],[0,1],m,p)
 controls=[[rng.randrange(1,p),rng.randrange(1,p)] for _ in range(m-1)];seed=[rng.randrange(1,p) for _ in range(k)];C=synth_weyl(seed,controls,[(1,0),(0,1)],wk,p)
 source=json.loads((Path(__file__).parent/'extracted/EXPLICIT_CERTIFICATES.json').read_text())
 for idx,cols in enumerate([A,B,C]):
  prop=properties(cols,w,p)
  for key,value in prop.items():assert value==source[idx][key],(idx,key,value,source[idx][key])
  if idx<2:ans,_,_=rational(cols,idx+1,[0,5] if idx==0 else [0,1],w,p)
  else:ans=weyl(cols,[(1,0),(0,1)],w,p)
  assert ans==dft(columns_to_raw(cols),w,p)
  if idx==0:assert infer_shift(cols,w,p)==5
  out['exact_witnesses'].append(prop)
 return out
if __name__=='__main__':
 r=run();Path(__file__).with_name('PHASE8_REVIEW_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
