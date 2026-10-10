#!/usr/bin/env python3
"""Independent exact checks derived from the Phase7 mathematical statements."""
import pathlib,json,math,random
ROOT=pathlib.Path(__file__).resolve().parent;rng=random.Random(202610092312)
def prime(p):return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def field_root(n):
 k=1
 while not prime(k*n+1):k+=1
 p=k*n+1
 factors=[q for q in range(2,n+1) if n%q==0 and prime(q)]
 for a in range(2,p):
  w=pow(a,k,p)
  if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in factors):return p,w
 raise AssertionError('root not found')
def rank(a,p):
 a=[r[:] for r in a];rr=0
 for j in range(len(a[0])):
  k=next((k for k in range(rr,len(a)) if a[k][j]%p),None)
  if k is None:continue
  a[k],a[rr]=a[rr],a[k];iv=pow(a[rr][j],-1,p);a[rr]=[v*iv%p for v in a[rr]]
  for k in range(rr+1,len(a)):
   c=a[k][j]
   if c:a[k]=[(x-c*y)%p for x,y in zip(a[k],a[rr])]
  rr+=1
  if rr==len(a):break
 return rr

rect=[]
for n in range(2,9):
 p,w=field_root(n);f=[[pow(w,(-i*j)%n,p) for j in range(n)] for i in range(n)]
 sets=[[i for i in range(n) if mask>>i&1] for mask in range(1,1<<n)]
 best=min(d+n//d for d in range(1,n+1) if n%d==0);total=one=0
 for I in sets:
  for J in sets:
   total+=1
   criterion=all(((i-I[0])*(j-J[0]))%n==0 for i in I for j in J)
   actual=rank([[f[i][j] for j in J] for i in I],p)==1
   assert criterion==actual
   if actual:
    one+=1;g=n
    for i in I:g=math.gcd(g,i-I[0])
    d=n//g
    assert len(I)<=d and len(J)<=n//d
    assert all((j-J[0])%d==0 for j in J)
    assert len(I)*len(J)<=n
    assert n*(len(I)+len(J))>=len(I)*len(J)*best
 rect.append({'N':n,'field':p,'root':w,'rectangles_checked':total,'rank_one_rectangles':one,'exact_tiling_incidence_optimum':n*best})

tilings=[];gauge_checks=0
for n in range(2,65):
 p,w=field_root(n);table=[pow(w,-j,p) for j in range(n)];x=[rng.randrange(p) for _ in range(n)]
 target=[sum(x[j]*table[k*j%n] for j in range(n))%p for k in range(n)]
 for d in range(1,n+1):
  if n%d:continue
  q=n//d;covered=set();y=[0]*n;mult=add=0
  for r in range(q):
   for c in range(d):
    I=[r+q*v for v in range(d)];J=[c+d*z for z in range(q)]
    values=[x[j]*table[(r*d*z)%n]%p for z,j in enumerate(J)]
    mult+=q;acc=values[0]
    for value in values[1:]:acc=(acc+value)%p;add+=1
    for v,k in enumerate(I):
     y[k]=(y[k]+table[(k*c)%n]*acc)%p;mult+=1;add+=1
     for j in J:
      assert (k,j) not in covered;covered.add((k,j))
      z=(j-c)//d
      assert table[(k*j)%n]==table[(r*c+r*d*z+q*v*c)%n]
  assert len(covered)==n*n and y==target
  assert mult==n*(d+q) and add==n*(d+q-1)
  tilings.append({'N':n,'d':d,'q':q,'tile_count':n,'incidence':n*(d+q),'projection_fanout_multiplications':mult,'additions':add,'root_table_multiplications':n-1,'output_writes':n})
 # Exact diagonal-gauge invariance, sampling nonzero entries in the field.
 ar=[rng.randrange(1,p) for _ in range(n)];bc=[rng.randrange(1,p) for _ in range(n)]
 for _ in range(20):
  i,k,j,l=[rng.randrange(n) for _ in range(4)]
  a=lambda r,c:table[(r*c)%n]
  b=lambda r,c:ar[r]*a(r,c)*bc[c]%p
  lhs=a(i,j)*a(k,l)*pow(a(i,l)*a(k,j)%p,-1,p)%p
  rhs=b(i,j)*b(k,l)*pow(b(i,l)*b(k,j)%p,-1,p)%p
  assert lhs==rhs==table[((i-k)*(j-l))%n];gauge_checks+=1

# A source-model counter-control: unrestricted row mixing removes all curvature.
n=4;p,w=field_root(n);f=[[pow(w,-i*j,p) for j in range(n)] for i in range(n)]
finv=[[pow(n,-1,p)*pow(w,i*j,p)%p for j in range(n)] for i in range(n)]
assert [[sum(finv[i][k]*f[k][j] for k in range(n))%p for j in range(n)] for i in range(n)]==[[int(i==j) for j in range(n)] for i in range(n)]

def fft(seq,table,p):
 n=len(seq);N=len(table);bits=n.bit_length()-1
 data=[seq[int(format(i,f'0{bits}b')[::-1],2)] for i in range(n)] if n>1 else list(seq)
 butterflies=0;length=2
 while length<=n:
  for start in range(0,n,length):
   for j in range(length//2):
    a=data[start+j];b=data[start+j+length//2]*table[j*(N//length)]%p
    data[start+j]=(a+b)%p;data[start+j+length//2]=(a-b)%p;butterflies+=1
  length*=2
 return data,butterflies
shared=[]
for exponent in range(2,11):
 n=1<<exponent;d=1<<(exponent//2);q=n//d;p,w=field_root(n)
 table=[pow(w,-j,p) for j in range(n)];x=[rng.randrange(p) for _ in range(n)]
 target=[sum(x[j]*table[k*j%n] for j in range(n))%p for k in range(n)]
 first=[];B=0
 for c in range(d):
  v,b=fft([x[c+d*j] for j in range(q)],table,p);first.append(v);B+=b
 y=[0]*n
 for r in range(q):
  row,b=fft([first[c][r]*table[r*c%n]%p for c in range(d)],table,p);B+=b
  for v in range(d):y[r+q*v]=row[v]
 assert y==target and B==n*exponent//2
 shared.append({'N':n,'field':p,'d':d,'q':q,'butterflies':B,'scalar_multiplications_excluding_root_table':B+n,'scalar_additions':2*B,'root_table_multiplications':n-1,'output_writes':n})

out={'exhaustive_rectangle_cases':rect,'constructive_tiling_cases':tilings,'diagonal_plaquette_invariance_checks':gauge_checks,
 'shared_Cooley_Tukey_controls':shared,
 'general_GL_mixing_changes_rank_one_tiling_geometry':True,
 'reported_source_test_suite_executed':False,'independent_checker_imports_source_modules':False,'uploaded_code_executed':False}
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
