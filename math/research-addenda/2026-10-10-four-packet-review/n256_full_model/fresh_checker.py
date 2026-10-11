# Publication adaptation of reviewer-authored checker.
# Original SHA-256: bcae2e5d2643f2c6a70630072a1cd02f5d672ae4e92f4f40a92b0ffed6bcda4e
# Changes: Replaced private source/archive provenance prelude with bundled inert-input hashes; all remaining mathematical checker logic unchanged. Result provenance key labels the reduced scope.
# Mathematical formulas, samples, assertions and proof guards are unchanged.
#!/usr/bin/env python3
"""Independent audit. Reads inert JSON/archive bytes only. Never imports source programs."""
import collections, hashlib, json, pathlib, random, zipfile, time
import numpy as np
R=pathlib.Path(__file__).resolve().parent
SRC=R/'extracted/fft_banded_full_feasibility_2026-10-11'
START=time.monotonic()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(R/name).write_text(json.dumps(obj,indent=2)+'\n')
_publication_inputs=json.loads((R/'PUBLICATION_INPUT_HASHES.json').read_text())
for _name,_hash in _publication_inputs.items():
 assert hashlib.sha256((R/_name).read_bytes()).hexdigest()==_hash, _name
G=json.loads((SRC/'reference/GENERATOR_POINT_1.json').read_text());LAY=json.loads((SRC/'reference/AFFINE_LAYOUT.json').read_text())
N=256; T=4
PERMS=[]
for cols in LAY['affine_shuffle_columns']:
 perm=[]
 for j in range(N):
  a=0
  for b,c in enumerate(cols):
   if (j>>b)&1:a^=c
  perm.append(a)
 assert sorted(perm)==list(range(N));PERMS.append(np.array(perm))

def dense(g,p):
 n=len(g['d']);d=np.zeros((n,n),dtype=np.int64)
 for i in range(n):
  for j in range(n):d[i,j]=g['d'][i] if i==j else (g['a'][i]*g['b'][j] if i>j else g['c'][i]*g['e'][j])%p
 return d%p

def eliminate(A,p,need_inverse=False):
 a=np.array(A,dtype=np.int64).copy()%p;m,n=a.shape;Q=np.eye(m,dtype=np.int64);piv=[];det=1;r=0
 for c in range(n):
  candidates=np.flatnonzero(a[r:,c]);
  if not len(candidates):continue
  rr=r+int(candidates[0])
  if rr!=r:a[[r,rr]]=a[[rr,r]];Q[[r,rr]]=Q[[rr,r]];det=-det
  x=int(a[r,c]);det=det*x%p; inv=pow(x,-1,p)
  a[r]=a[r]*inv%p;Q[r]=Q[r]*inv%p
  ix=np.flatnonzero(a[:,c]);ix=ix[ix!=r];v=a[ix,c].copy()
  a[ix]=(a[ix]-v[:,None]*a[r])%p;Q[ix]=(Q[ix]-v[:,None]*Q[r])%p
  piv.append(c);r+=1
  if r==m:break
 return {'rank':r,'rref':a,'transform':Q,'pivots':piv,'det':det%p if m==n==r else 0}

def augmented(g,y,p):
 n=len(y);a=[{} for _ in range(3*n)];v=[0]*(3*n)
 for i in range(n):
  k=3*i;a[k]={k:g['d'][i]%p,k+1:g['a'][i]%p,k+2:g['c'][i]%p};v[k]=int(y[i])%p
  a[k+1]={k+1:1};a[k+2]={k+2:1}
  if i:a[k+1].update({k-2:p-1,k-3:-g['b'][i-1]%p})
  if i<n-1:a[k+2].update({k+5:p-1,k+3:-g['e'][i+1]%p})
 for r in range(3*n):a[r]={c:z for c,z in a[r].items() if z}
 return a,v

def band_solve(g,y,p):
 a,b=augmented(g,y,p);m=len(a);det=1;swaps=0;maxu=0;steps=0;maxp=0
 for k in range(m):
  candidates=[r for r in range(k,min(m,k+5)) if a[r].get(k,0)]
  if not candidates:
   assert all(not a[r].get(k,0) for r in range(k+5,m));return None,0,{'swaps':swaps,'update_terms':steps,'upper_band':maxu,'pivot_distance':maxp}
  j=candidates[-1] # Deliberately choose last nonzero pivot rather than source first.
  maxp=max(maxp,j-k)
  if j!=k:a[k],a[j]=a[j],a[k];b[k],b[j]=b[j],b[k];det=-det;swaps+=1
  q=a[k][k];det=det*q%p;iv=pow(q,-1,p);maxu=max(maxu,max(a[k])-k)
  assert max(a[k])-k<=7
  for r in range(k+1,min(m,k+5)):
   h=a[r].pop(k,0)*iv%p
   if not h:continue
   for c,v in a[k].items():
    if c>k:
     a[r][c]=(a[r].get(c,0)-h*v)%p;steps+=1
     if a[r][c]==0:del a[r][c]
   b[r]=(b[r]-h*b[k])%p
 ans=[0]*m
 for k in range(m-1,-1,-1):ans[k]=(b[k]-sum(v*ans[c] for c,v in a[k].items() if c>k))*pow(a[k][k],-1,p)%p
 return np.array(ans[::3],dtype=np.int64),det,{'swaps':swaps,'update_terms':steps,'upper_band':maxu,'pivot_distance':maxp}

def scan(g,x,p):
 n=len(x);l=0;r=sum(int(g['e'][i])*int(x[i]) for i in range(n))%p;out=[]
 for i in range(n):
  r=(r-g['e'][i]*int(x[i]))%p;out.append((g['d'][i]*int(x[i])+g['a'][i]*l+g['c'][i]*r)%p);l=(l+g['b'][i]*int(x[i]))%p
 return np.array(out,dtype=np.int64)

# Enumerate every compressed equation's monomials to check its actual total degree/support.
# Symbols are integer coordinate ids; None is zero; () is literal one; tuples are monomials.
GBASE=0;XBASE=5*T*N;LBASE=XBASE+(T-1)*N*N;RBASE=LBASE+T*N*(N-1);TOTAL=RBASE+T*N*(N-1)
def gsym(s,k,i):return (s*5*N+'abcde'.index(k)*N+i,)
def xsym(s,i,j):return (() if i==j else None) if s==0 else (XBASE+(s-1)*N*N+i*N+j,)
def lsym(s,i,j):return None if i==0 else (LBASE+s*N*(N-1)+(i-1)*N+j,)
def rsym(s,i,j):return None if i==N-1 else (RBASE+s*N*(N-1)+i*N+j,)
def prod(x,y):return None if x is None or y is None else tuple(sorted(x+y))
COUNTS=collections.Counter();EQCOUNT=0;MAXDEG=0;MAXTERMS=0;USED=set()
def register(terms):
 global EQCOUNT,MAXDEG,MAXTERMS
 d=collections.Counter()
 for coeff,mon in terms:
  if mon is not None:d[mon]+=coeff
 mons=[m for m,c in d.items() if c]
 assert mons
 deg=max(map(len,mons));num=len(mons);COUNTS[(deg,num)]+=1;EQCOUNT+=1;MAXDEG=max(MAXDEG,deg);MAXTERMS=max(MAXTERMS,num)
 for m in mons:USED.update(m)
for s in range(T):
 for j in range(N):
  for i in range(N-1):
   register([(1,lsym(s,i+1,j)),(-1,lsym(s,i,j)),(-1,prod(gsym(s,'b',i),xsym(s,i,j)))])
   register([(1,rsym(s,i,j)),(-1,rsym(s,i+1,j)),(-1,prod(gsym(s,'e',i+1),xsym(s,i+1,j)))])
  for i in range(N):
   ii=int(PERMS[s][i]) if s<T-1 else i
   target=xsym(s+1,i,j) if s<T-1 else () # nonzero Fourier coefficient, support only
   register([(1,target),(-1,prod(gsym(s,'d',ii),xsym(s,ii,j))),(-1,prod(gsym(s,'a',ii),lsym(s,ii,j))),(-1,prod(gsym(s,'c',ii),rsym(s,ii,j)))])
assert TOTAL==723968 and EQCOUNT==784384 and MAXDEG==2 and MAXTERMS==4
assert len(USED)==TOTAL-16
counts={'unknowns':TOTAL,'equations':EQCOUNT,'max_total_degree':MAXDEG,'max_monomials':MAXTERMS,'structurally_unused_raw_generator_coordinates':16,'used_coordinates':len(USED),'degree_and_support_census':{f'degree_{k[0]}_terms_{k[1]}':v for k,v in sorted(COUNTS.items())}}
results={'publication_inert_files_verified':len(_publication_inputs),'compressed_model':counts,'banded':{'dense_stage_determinants':0,'dense_augmented_determinants':0,'small_invertible_roundtrips':0,'small_singular_fixtures':0,'zero_diagonal_large':[]},'fields':[]}
print('packaged input hashes and full symbolic equation census verified',flush=True)
for p in [12289,65537]:
 rng=random.Random(234400+p)
 for n in [1,2,3,4,7,13,21]:
  for trial in range(16):
   gg={k:[rng.randrange(-3,4) for _ in range(n)] for k in 'abcde'}
   if trial%4==0:gg['d']=[0]*n
   if trial==15:gg={k:[0]*n for k in 'abcde'}
   S=dense(gg,p);d=eliminate(S,p)['det'];v=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64);y=S@v%p
   got,db,metrics=band_solve(gg,y,p);assert db==d;results['banded']['dense_stage_determinants']+=1
   if n<=7:
    a,b=augmented(gg,y,p);A=np.zeros((3*n,3*n),dtype=np.int64)
    for i,row in enumerate(a):
     for j,z in row.items():A[i,j]=z
    assert eliminate(A,p)['det']==d;results['banded']['dense_augmented_determinants']+=1
    assert all(-3<=i-j<=4 for i,row in enumerate(a) for j,z in row.items())
   if d:assert np.array_equal(got,v);results['banded']['small_invertible_roundtrips']+=1
   else:assert got is None;results['banded']['small_singular_fixtures']+=1
 for n in [2,8,64,256,1024]:
  gg={'a':[1]*n,'b':[1]*n,'c':[2]*n,'d':[0]*n,'e':[1]*n};v=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64)
  y=scan(gg,v,p);got,d,met=band_solve(gg,y,p);expected=(-1)**(n-1)*(pow(2,n,p)-2)%p
  assert d==expected and d and np.array_equal(got,v)
  results['banded']['zero_diagonal_large'].append({'field':p,'N':n,'determinant':d,**met})
 print('banded controls passed',p,flush=True)
 mats=[dense(g,p) for g in G];invdata=[eliminate(S,p) for S in mats];assert all(z['rank']==N for z in invdata)
 inverses=[z['transform'] for z in invdata]
 omega=next(pow(g,(p-1)//N,p) for g in range(2,p) if pow(pow(g,(p-1)//N,p),N//2,p)==p-1)
 assert pow(omega,N,p)==1
 idx=np.arange(N,dtype=np.int64);powers=np.array([pow(omega,i,p) for i in range(N)],dtype=np.int64)
 U=powers[idx[:,None]*idx[None,:]%N]*pow(16,-1,p)%p;Ui=powers[-idx[:,None]*idx[None,:]%N]*pow(16,-1,p)%p
 assert np.array_equal(U@Ui%p,np.eye(N,dtype=np.int64))
 # All basis traces in parallel, with dense products as an independent output oracle.
 X=np.eye(N,dtype=np.int64);traces=[];positive=0
 for s,gg in enumerate(G):
  L=np.zeros_like(X);V=np.zeros_like(X)
  for i in range(1,N):L[i]=(L[i-1]+gg['b'][i-1]*X[i-1])%p
  for i in range(N-2,-1,-1):V[i]=(V[i+1]+gg['e'][i+1]*X[i+1])%p
  Y=(np.array(gg['d'])[:,None]*X+np.array(gg['a'])[:,None]*L+np.array(gg['c'])[:,None]*V)%p
  assert np.array_equal(Y,mats[s]@X%p)
  assert not np.any((L[1:]-L[:-1]-np.array(gg['b'][:-1])[:,None]*X[:-1])%p)
  assert not np.any((V[:-1]-V[1:]-np.array(gg['e'][1:])[:,None]*X[1:])%p)
  positive+=2*N*(N-1)+N*N;traces.append((X,L,V,Y));X=Y[PERMS[s]] if s<T-1 else Y
 M=X;assert positive==EQCOUNT
 mismatch=int(np.count_nonzero(M!=U));assert mismatch==({12289:65532,65537:65535}[p])
 # Negative boundary and interior mutations must be rejected by their recurrences.
 mutation_rejections=0
 for s,(X,L,V,Y) in enumerate(traces):
  for i,j,kind in [(1,0,'L'),(255,255,'L'),(0,0,'R'),(254,255,'R')]:
   Q=(L if kind=='L' else V).copy();Q[i,j]=(Q[i,j]+1)%p
   residual=(Q[1:]-Q[:-1]-np.array(G[s]['b'][:-1])[:,None]*X[:-1])%p if kind=='L' else (Q[:-1]-Q[1:]-np.array(G[s]['e'][1:])[:,None]*X[1:])%p
   assert np.any(residual);mutation_rejections+=1
 p1,p2,p3=PERMS;ip1=np.argsort(p1);ip2=np.argsort(p2);ip3=np.argsort(p3)
 GG=(mats[0]@Ui%p)@mats[3]%p;GG=GG[np.ix_(p1,ip3)]
 HH=(inverses[3]@U%p)@inverses[0]%p;HH=HH[np.ix_(ip3,p1)] # P3^-1 A P1^-1: row ip3, column p1.
 assert np.array_equal(GG@HH%p,np.eye(N,dtype=np.int64));assert np.array_equal(HH@GG%p,np.eye(N,dtype=np.int64))
 middle_roundtrips=0
 for trial in range(6):
  v=np.array([rng.randrange(p) for _ in range(N)],dtype=np.int64)
  x,_,_=band_solve(G[0],v[ip1],p);x=U@x%p;x,_,_=band_solve(G[3],x,p);x=x[ip3]
  assert np.array_equal(x,HH@v%p);assert np.array_equal(GG@x%p,v);middle_roundtrips+=1
 # Derive gate indices directly from parity and the exact p2 orientation.
 side=np.array([(j&64).bit_count()%2==0 for j in range(N)])
 bound=int(np.count_nonzero(side[1:]!=side[:-1])+np.count_nonzero(side[p2][1:]!=side[p2][:-1]));assert bound==16
 I=np.flatnonzero(~side);J=np.flatnonzero(side[p2]);assert len(I)==len(J)==128
 # Dense inverse of synthetic S3 P2 S2 independently of banded solver.
 HM=mats[2]@mats[1][p2]%p;HMdata=eliminate(HM,p);assert HMdata['rank']==N
 B=HMdata['transform'][np.ix_(I,J)];red=eliminate(B,p);assert red['rank']==16
 K=[c for c in range(128) if c not in red['pivots']];Z=np.zeros((128,112),dtype=np.int64);Z[K,:]=np.eye(112,dtype=np.int64)
 for row,col in enumerate(red['pivots']):Z[col]=(-red['rref'][row,K])%p
 assert not np.any(B@Z%p)
 BT=GG[np.ix_(I,J)];rankT=eliminate(BT,p)['rank'];assert rankT==128
 # General lift identity, negative real-Fourier fixture, and positive synthetic-target fixture.
 E=np.zeros((N,112),dtype=np.int64);E[J]=Z
 Xlift=mats[3]@E[p3]%p
 residual=(mats[0]@Ui%p)[p1]@Xlift%p
 assert np.array_equal(residual[I],BT@Z%p) and np.any(residual[I])
 # M synthetic is invertible; its inverse replaces Ui. This produces a true positive chart.
 Mi=eliminate(M,p)['transform'];GS=(mats[0]@Mi%p)@mats[3]%p;GS=GS[np.ix_(p1,ip3)]
 assert np.array_equal(GS[np.ix_(I,J)],B)
 lifted_final=((mats[0]@Mi%p)[p1]@Xlift%p)[I]
 assert not np.any(lifted_final)
 # Rank-degenerate fixtures: chart-normalized witness with first 112 pivot rows.
 extra=[]
 for rank in [0,1,15,16]:
  BC=np.zeros((128,128),dtype=np.int64)
  for a in range(rank):BC[a,112+a]=1
  ZC=np.zeros((128,112),dtype=np.int64);ZC[:112]=np.eye(112,dtype=np.int64)
  assert eliminate(BC,p)['rank']==rank and not np.any(BC@ZC%p);extra.append(rank)
 # Rank17 cannot carry any full-column-rank 112-dimensional kernel.
 B17=np.zeros((128,128),dtype=np.int64);B17[:17,:17]=np.eye(17,dtype=np.int64);assert eliminate(B17,p)['rank']==17
 # Demonstrate fixed chart insufficiency: rank16 diagonal first16 kills first112 identity chart,
 # but last112 identity chart provides a witness.
 Bother=np.zeros((128,128),dtype=np.int64);Bother[:16,:16]=np.eye(16,dtype=np.int64)
 Zother=np.zeros((128,112),dtype=np.int64);Zother[16:]=np.eye(112,dtype=np.int64)
 assert not np.any(Bother@Zother%p);assert Bother[0,0]==1
 # Evaluate both cubic blocks independently using raw prefix/suffix scans.
 Xraw=np.column_stack([scan(G[3],E[p3,j],p) for j in range(112)])
 assert np.array_equal(Xraw,Xlift)
 W=Mi@Xlift%p
 final_raw=np.column_stack([scan(G[0],W[:,j],p)[p1][I] for j in range(112)])
 assert not np.any(final_raw)
 Wbad=Ui@Xlift%p
 bad_raw=np.column_stack([scan(G[0],Wbad[:,j],p)[p1][I] for j in range(112)])
 assert np.array_equal(bad_raw,residual[I])
 # Kernel chart mutation leaves the identity block intact but breaks BZ.
 free_rows=[i for i in range(128) if i not in K]
 rr=next(i for i in free_rows if np.any(B[:,i]));Zbad=Z.copy();Zbad[rr,0]=(Zbad[rr,0]+1)%p
 assert np.array_equal(Zbad[K],np.eye(112,dtype=np.int64)) and np.any(B@Zbad%p)
 # The incompatible fixed chart contradiction is explicit: its equation (0,0)=1.
 results['fields'].append({'field':p,'primitive_root':omega,'all_basis_columns':256,'synthetic_compressed_equations_verified':positive,'fourier_coefficient_mismatches':mismatch,'state_mutation_rejections':mutation_rejections,'middle_dense_identity_sides':2,'middle_banded_apply_controls':middle_roundtrips,'mask64':{'bound':bound,'rows':I.tolist(),'columns':J.tolist(),'synthetic_rank':red['rank'],'saved_fourier_outer_rank':rankT,'kernel_pivot_rows':K,'kernel_sha256_le_i64':hashlib.sha256(Z.astype('<i8').tobytes()).hexdigest(),'kernel_equations_verified':128*112,'lift_definition_equations_verified':256*112,'positive_lift_residual_nonzeros':int(np.count_nonzero(lifted_final)),'negative_fourier_lift_residual_nonzeros':int(np.count_nonzero(residual[I])),'degenerate_rank_controls':extra,'rank17_rejection':True,'fixed_chart_incompleteness_control':True}})
 print('all-basis, middle inverse, and kernel/lift controls passed',p,flush=True)
# Additional small-characteristic controls, where the stage theorem still applies.
small={'fields':[2,3,5,17],'dense_determinants':0,'invertible_roundtrips':0,'singular_rejections':0}
for p in small['fields']:
 rng=random.Random(619+p)
 for n in [1,2,3,5]:
  for k in range(12):
   gg={s:[rng.randrange(p) for _ in range(n)] for s in 'abcde'}
   if k%3==0:gg['d']=[0]*n
   v=np.array([rng.randrange(p) for _ in range(n)],dtype=np.int64);SS=dense(gg,p);dd=eliminate(SS,p)['det']
   xx,dd2,_=band_solve(gg,SS@v%p,p);assert dd2==dd;small['dense_determinants']+=1
   if dd:assert np.array_equal(xx,v);small['invertible_roundtrips']+=1
   else:assert xx is None;small['singular_rejections']+=1
results['small_characteristic_controls']=small
# Generic characteristic-zero determinant identities, distinct from modular evidence.
import sympy as sp
symbolic=[]
for n in [1,2,3]:
 gg={k:sp.symbols(k+':'+str(n)) for k in 'abcde'};SS=sp.zeros(n);AA=sp.zeros(3*n)
 for i in range(n):
  for j in range(n):SS[i,j]=gg['d'][i] if i==j else gg['a'][i]*gg['b'][j] if i>j else gg['c'][i]*gg['e'][j]
  r=3*i;AA[r,r]=gg['d'][i];AA[r,r+1]=gg['a'][i];AA[r,r+2]=gg['c'][i];AA[r+1,r+1]=1;AA[r+2,r+2]=1
  if i:AA[r+1,r-2]=-1;AA[r+1,r-3]=-gg['b'][i-1]
  if i<n-1:AA[r+2,r+5]=-1;AA[r+2,r+3]=-gg['e'][i+1]
 assert sp.expand(AA.det(method='domain-ge')-SS.det())==0;symbolic.append(n)
results['symbolic_determinant_identity_sizes']=symbolic
results['kernel_census']={'block_size':128,'rank_bound':16,'kernel_columns':112,'free_Z_variables':16*112,'equations':128*112,'raw_degree_bound':5,'matrix_entry_degree_bound':3,'lift_extra_X_variables':256*112,'lift_equations':256*112+128*112,'lift_raw_degree_bound':3}
results['elapsed_seconds']=round(time.monotonic()-START,3)
save('fresh_check_results.json',results)
print(json.dumps(results,indent=2))
