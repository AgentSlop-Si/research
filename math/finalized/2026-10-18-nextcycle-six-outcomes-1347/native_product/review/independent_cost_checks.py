import sys, json, hashlib, math, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'candidate'))
import product_interface as P
from dependencies.kernel_stream import parameters, karatsuba
rng=random.Random(202610181343)
counts={}; transcript=[]
def record(k,v):
 counts[k]=counts.get(k,0)+1; transcript.append((k,v))
def horner(a,sign,H):
 r=[]; mask=(1<<H)-1
 for x in reversed(a):
  n=[0]*(len(r)+1)
  for j,v in enumerate(r): n[j]=(n[j]+sign*v)&mask; n[j+1]=(n[j+1]+v)&mask
  n[0]=(n[0]+x)&mask; r=n
 return r
def conv(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): r[i+j]+=x*y
 return r
for n in [2,3,4,7,8,9,15,17,31]:
 t=parameters(n,0)['t']; g=(n-1).bit_length(); short=8*((max(1,g)+7)//8)
 for H in sorted(set([1,2,max(1,t-g-1),max(1,t-g),t-g+1,3*t+5])):
  q=(H+g+t-1)//t; b=8*((2*t+g+7)//8); cap=n*b
  for sign in [-1,1]:
   a=[rng.randrange(-(1<<(H+11)),1<<(H+11)) for _ in range(n)]; calls=[]
   def mul(x,y):
    assert max(x.bit_length(), y.bit_length())<=cap
    calls.append((x.bit_length(),y.bit_length())); return karatsuba(x,y)
   got=P.shift_mod(a,sign,H,product=mul)
   assert got==horner(a,sign,H)
   expected=3*(n-1)*((t+short-1)//short)+2*(t-1).bit_length()+(5*n+1)*q
   assert len(calls)==expected,(n,H,len(calls),expected)
   record('shift_full_call_ledger',[n,H,sign,t,q,expected])
for n,H,t in [(1,9,8),(2,25,8),(7,65,16),(9,97,24),(3,257,8),(257,17,8),(513,9,8),(1,1,40),(3,25,80)]:
 q=(H+t-1)//t; R=1<<t; mask=(1<<H)-1
 for kind in range(4):
  a=[mask if kind==0 else (1<<rng.randrange(H)) if kind==1 else rng.getrandbits(H) if kind==2 else 0 for _ in range(n)]
  b=[mask if kind==0 else (1<<rng.randrange(H)) if kind==1 else rng.getrandbits(H) for _ in range(n)]
  calls=[]; count=[0]; rows={}; history={}; stats={}
  def mul(x,y): calls.append((x.bit_length(),y.bit_length())); return x*y
  def trace(r,s,j,left,right,c,old,e,new,digit):
   count[0]+=1; assert 0<=e<=n*(R-1) and 0<=new<=n*(R-1)
   assert c+old+e==digit+R*new
   assert old==history.get((j,r+s),0); history[j,r+s]=digit
   rows[r,j]=rows.get((r,j),0)+c*(R**s)
   if s==q-r-1:
    # End-of-row carry is at q, never discarded at r+s.
    assert r+s+1==q
  got=P.two_wide_convolution(a,b,H,t,product=mul,trace=trace,stats=stats)
  assert got==[v&mask for v in conv(a,b)]
  assert len(calls)==q*(q+1)//2 and count[0]==len(calls)*(2*n-1)
  assert all(max(x,y)<=stats['S'] for x,y in calls)
  record('pair_complete_ledger',[n,H,t,kind,len(calls),count[0]])
for m in [2,3,5,8,17,64,257]:
 for n in [1,2,3,6,11]:
  limit=1<<(m*n)
  for mode in range(3):
   x,y=(limit-1,limit-1) if mode==0 else (rng.randrange(limit),rng.randrange(limit))
   t=[8,24,8*((2*m+7)//8)][mode]
   stats={}; got=P.multiply_interface(x,y,m,n,t,stats=stats)
   assert got==x*y
   expected=conv(P.binary_chunks(x,m,n),P.binary_chunks(y,m,n))
   assert stats['final_coefficients']==expected and stats['raw_output_length']==2*n-1
   H=2*m+(n-1).bit_length(); assert max(expected)<1<<H
   record('complete_product',[m,n,t,hashlib.sha256(hex(got).encode()).hexdigest()])
for p in [3,7,15,31,255]:
 for K in [2,4,8,16,32,64,128]:
  for d in [1,2,3,4,5,7,11,17,32,65,129]:
   s=K*d; D=K*(p**d-1)**2; r=K
   while (p**r+1)//2<=D: r+=K
   for extra in [0,1,4]:
    child=r+extra*K
    assert child>2*d and child>=K and K*child>=2*s and child*child>=2*s
    assert (p**child+1)//2>D
    record('native_rounded_certificate',[p,K,d,child])
# Fully expanded minimum-leaf-volume recursion, represented by multiplicities.
# Independent exact log-potential check via integer products, no float logs.
for p in [3,7,31]:
 hist={s:{s:1} for s in range(2,17,2)}
 for s in range(18,514,2):
  choices=[]; K=2
  while K<=s:
   if s%K==0:
    d=s//K; r=K; D=K*(p**d-1)**2
    while (p**r+1)//2<=D:r+=K
    for child in range(r,s,K):
     if child in hist:
      h={e:K*c for e,c in hist[child].items()}; choices.append((sum(e*c for e,c in h.items()),h))
   K*=2
  if not choices: continue
  _,h=min(choices,key=lambda a:a[0]); hist[s]=h
  assert math.prod(e**(e*c) for e,c in h.items())>=s**s
  # Since every leaf exponent <=16, this is exact volume >= s log_16(s).
  volume=sum(e*c for e,c in h.items()); assert 16**volume>=s**s
  record('finite_tree_exact_potential',[p,s,volume,sorted(h.items())])
result={'status':'PASS','counts':counts,'digest':hashlib.sha256(json.dumps(transcript,sort_keys=True).encode()).hexdigest(),'external_writes':False}
Path(__file__).with_name('INDEPENDENT_COST_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
