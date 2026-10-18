"""Independent integer arithmetic is used only for mathematical test oracles."""
from itertools import product
from math import comb
from random import Random
import hashlib,json
from restricted_guards import *

rnd = Random(202610181746)
records=[]
counts={}
def record(kind,data):
 counts[kind]=counts.get(kind,0)+1
 records.append((kind,data))
def convolution(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
def evaluate(c,x):
 out=0
 for v in reversed(c):out=out*x+v
 return out
def taylor(c):
 return [sum(comb(i,j)*c[i] for i in range(j,len(c))) for j in range(len(c))]
def valuation(x):
 if not x:return None
 x=abs(x);return (x & -x).bit_length()-1

# Exact precision formula across a large grid.
for L in range(1,257):
 for m in [2,3,4,8,17,64,257]:
  bounds=product_bounds(m,L)
  expected=[min(j+1,2*L-1-j,L)*((1<<m)-1)**2 for j in range(2*L-1)]
  assert bounds==expected
  W=envelope_precision(bounds)
  gamma=guard_for_degree(2*L-2)
  delta=int(L>=4 and L%2==0 and m>=3)
  assert W==2*m+gamma+delta,(L,m,W)
  record('precision_formula',[L,m,W])

# Decoder works for the whole triangular coefficient box, even nonproducts.
for L in [1,2,3,4,5,6,8,12,17,24,33,48,65]:
 for m in [1,2,3,8,17,65,257]:
  bounds=product_bounds(m,L); W=envelope_precision(bounds); q=1<<W
  for kind in ['zero','maximum','random']:
   c=[0 if kind=='zero' else x if kind=='maximum' else rnd.randrange(x+1) for x in bounds]
   values=[evaluate(c,j)%q for j in range(len(c))]
   stats={}; got=height_decode(values,bounds,stats=stats)
   assert got==c
   assert stats['tail_max_coefficient']<L
   record('height_decoder',[L,m,kind,W,stats['tail_width']])

# Exhaustive small actual product families, paid backend as default.
for m,L in [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3)]:
 arrays=list(product(range(1<<m),repeat=L))
 for a in arrays:
  for b in arrays:
   got=restricted_convolution(list(a),list(b),m)
   assert got==convolution(a,b)
   record('exhaustive_products',[m,L,list(a),list(b)])

# Instrument explicit sample product count on direct interface.
for L in [1,2,3,4,7,12,17]:
 for m in [1,2,3,17,65,257]:
  a=[rnd.randrange(1<<m) for _ in range(L)]
  b=[rnd.randrange(1<<m) for _ in range(L)]
  calls=[]
  def backend(x,y):
   calls.append([x.bit_length(),y.bit_length()]); return karatsuba(x,y)
  stats={}; got=restricted_convolution(a,b,m,backend,stats)
  assert got==convolution(a,b)
  assert len(calls)==2*L-1
  h=m if L==1 else min(stats['W'],m+(L-1).bit_length()+(L-1)*(2*L-3).bit_length())
  assert stats['maximum_sample_bits']<=h
  record('counted_product_schedule',[L,m,stats,len(calls),h])

# Full Mersenne Taylor route, including both shifts and final carries.
for L in [1,2,3,4,5,8,12,17]:
 for m in [2,3,8,17,65,257]:
  for mode in ['random','maximum']:
   x=rnd.randrange(1<<(L*m)) if mode=='random' else (1<<(L*m))-1
   y=rnd.randrange(1<<(L*m)) if mode=='random' else x
   stats={};got=multiply_restricted(x,y,m,L,stats=stats)
   assert got==x*y
   a=binary_chunks(x,m,L);b=binary_chunks(y,m,L)
   assert stats['final_coefficients']==convolution(a,b)
   record('full_taylor_route',[L,m,mode,stats['W'],stats['guard']])

# Explicit bounded-input all-integer null witnesses.
def witness(L,a,b,m):
 assert 0<=b<=a and a>=1 and 5*a+3*b<=2*L-2
 base=[sum(((-1)**(a-i))*comb(a,i)*comb(b,k-i)
           for i in range(max(0,k-b),min(a,k)+1)) for k in range(a+b+1)]
 C=max(map(abs,base));t=C.bit_length();assert m>=t
 A=3*a+b;D=5*a+3*b
 split=min(A,L-1); shift=A-split
 left=[0]*L;plus=[0]*L;minus=[0]*L
 left[split]=1<<(m-1)
 for j,c in enumerate(base):
  index=shift+2*j;assert index<L
  plus[index]=max(c,0)<<(m-t)
  minus[index]=max(-c,0)<<(m-t)
 assert all(0<=x<(1<<m) for x in left+plus+minus)
 p=convolution(left,plus);q=convolution(left,minus)
 diff=[x-y for x,y in zip(p,q)]
 e=2*m-1-t;W=e+A;H=2*m+(L-1).bit_length()
 assert p!=q and max(p+q)<(1<<H)
 for z in list(range(-50,51))+[1001,-1001]:
  x=evaluate(diff,z)
  assert x%(1<<W)==0
 assert min(valuation(evaluate(diff,2)),valuation(evaluate(diff,3)))==W
 tp,tq=taylor(p),taylor(q)
 assert any((x-y)%(1<<H) for x,y in zip(tp,tq))
 for z in range(-30,31):
  assert (evaluate(tp,z)-evaluate(tq,z))%(1<<W)==0
 lower=max(0,W-H+1)
 assert lower==max(0,3*a+b-t-(L-1).bit_length())
 return dict(L=L,m=m,a=a,b=b,t=t,H=H,W_collision=W,guard_lower=lower,
             left=left,plus=plus,minus=minus,fixed_divisor_witness_nodes=[2,3])

witnesses=[]
for L in list(range(4,41))+[65,129,257]:
 a=(2*L-2)//5;b=0
 if 2*(a+b)>L-1:continue
 baseC=comb(a,a//2);t=baseC.bit_length()
 for m in sorted(set([t,max(2,t),t+7,t+40])):
  w=witness(L,a,b,m);witnesses.append(w);record('restricted_null_witness',w)
for s in [1,2,3,4,5,8,12,20]:
 a,b=5*s,s; L=14*s+1
 cs=[sum(((-1)**(a-i))*comb(a,i)*comb(b,k-i)
     for i in range(max(0,k-b),min(a,k)+1)) for k in range(a+b+1)]
 C=max(map(abs,cs))
 # Exact squared version of C <= (200 sqrt(5)/27)**s.
 assert C*C*729**s <= 200000**s
 t=C.bit_length()
 for m in [t,t+17]:
  w=witness(L,a,b,m);witnesses.append(w);record('improved_restricted_null_witness',w)

# Exhaustive finite family information minima; n consecutive nodes capture
# every integer evaluation congruence by the integral Newton-binomial identity.
finite=[]
for m,L in [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,2),(2,3),(2,4),(3,2),(3,3)]:
 arrays=list(product(range(1<<m),repeat=L));products={}
 for i,a in enumerate(arrays):
  for b in arrays[i:]:products.setdefault(tuple(convolution(a,b)),[list(a),list(b)])
 H=2*m+(L-1).bit_length(); upper=envelope_precision(product_bounds(m,L)); last=None
 for W in range(1,upper+1):
  mask=(1<<W)-1; seen={};collision=None
  for c,ab in products.items():
   signature=tuple(evaluate(c,j)&mask for j in range(2*L-1))
   if signature in seen and seen[signature][0]!=c:
    collision=[seen[signature],[c,ab]];break
   seen[signature]=[c,ab]
  if collision:last=dict(W=W,products=collision)
  else:break
 assert collision is None
 row=dict(m=m,L=L,H=H,minimum_sample_width=W,minimum_nonnegative_guard=max(0,W-H),
          constructive_width=upper,distinct_products=len(products),last_collision=last)
 finite.append(row);record('finite_information_minimum',row)

out=dict(status='PASS',counts=counts,digest=hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
         finite_information_minima=finite,
         witness_summary=[{k:w[k] for k in ['L','m','a','b','t','H','W_collision','guard_lower']} for w in witnesses])
with open('RESULTS.json','w') as f:json.dump(out,f,indent=2)
with open('WITNESSES.json','w') as f:json.dump(witnesses,f,indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ['finite_information_minima','witness_summary']},indent=2))
