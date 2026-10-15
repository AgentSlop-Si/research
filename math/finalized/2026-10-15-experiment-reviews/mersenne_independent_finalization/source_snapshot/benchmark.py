import time,statistics,random,math,json
from check import encode,decode
from pathlib import Path
PRIMES=[(998244353,3),(1004535809,3),(469762049,3)]

def ntt(a,inverse,q,g):
 n=len(a);j=0
 for i in range(1,n):
  bit=n>>1
  while j&bit:j^=bit;bit>>=1
  j^=bit
  if i<j:a[i],a[j]=a[j],a[i]
 length=2
 while length<=n:
  wlen=pow(g,(q-1)//length,q)
  if inverse:wlen=pow(wlen,q-2,q)
  for i in range(0,n,length):
   w=1
   for j in range(i,i+length//2):
    u=a[j];v=a[j+length//2]*w%q
    a[j]=(u+v)%q;a[j+length//2]=(u-v)%q;w=w*wlen%q
  length*=2
 if inverse:
  inv=pow(n,q-2,q)
  for i in range(n):a[i]=a[i]*inv%q

def conv(a,b):
 L=len(a)+len(b)-1;n=1<<(L-1).bit_length()
 bound=min(len(a),len(b))*max(a)*max(b);P=1;chosen=[]
 for q,g in PRIMES:
  assert (q-1)%n==0
  root=pow(g,(q-1)//n,q)
  assert pow(root,n,q)==1 and (n==1 or pow(root,n//2,q)!=1)
  chosen.append((q,g));P*=q
  if P>bound:break
 if P<=bound:raise ValueError('finite CRT capacity insufficient')
 c=[0]*L;M=1
 for q,g in chosen:
  aa=[z%q for z in a]+[0]*(n-len(a));bb=[z%q for z in b]+[0]*(n-len(b))
  ntt(aa,False,q,g);ntt(bb,False,q,g)
  aa=[x*y%q for x,y in zip(aa,bb)];ntt(aa,True,q,g)
  inv=pow(M,-1,q)
  for i in range(L):c[i]+=M*((aa[i]-c[i])*inv%q)
  M*=q
 return c,{'points':n,'primes':len(chosen),'butterflies':len(chosen)*3*(n//2)*(n.bit_length()-1),'coefficient_bound_bits':bound.bit_length()}

def run(X,Y,m,d,binary=False):
 t=time.perf_counter()
 if binary:
  w=m;Q=1<<w
  def digits(z):
   out=[]
   while z:out.append(z&(Q-1));z>>=w
   return out or [0]
  a,b=digits(X),digits(Y)
 else:
  Q=((1<<m)-1)**d;a,_=encode(X,m,d);b,_=encode(Y,m,d)
 t1=time.perf_counter();c,stats=conv(a,b);t2=time.perf_counter()
 carry=0
 for i in range(len(c)):carry,c[i]=divmod(c[i]+carry,Q)
 while carry:carry,z=divmod(carry,Q);c.append(z)
 if binary:
  z=0
  for v in reversed(c):z=(z<<m)+v
 else:z,_=decode(c,m,d)
 t3=time.perf_counter();assert z==X*Y
 return {'total_ms':(t3-t)*1000,'convert_ms':(t1-t)*1000,'convolution_ms':(t2-t1)*1000,'carry_reconstruct_ms':(t3-t2)*1000,**stats,'digits':max(len(a),len(b)),'block_bits':(Q-1).bit_length()}

if __name__ == '__main__':
 rng=random.Random(1882026);rows=[];best=[]
 for N in [256,1024,2048]:
  X=rng.getrandbits(N)|(1<<(N-1));Y=rng.getrandbits(N)|(1<<(N-1))
  for binary in [False,True]:
   configs=[(w,1) for w in [4,8,12,16,20,24,32,40]] if binary else [(m,d) for m in [3,5,7,13,17,19] for d in [1,2,4] if m*d<=40]
   local=[]
   for m,d in configs:
    trials=[run(X,Y,m,d,binary) for _ in range(3)]
    row={'N':N,'kind':'binary' if binary else 'mersenne_prime_power','m':m,'d':d,**trials[0]}
    for k in ['total_ms','convert_ms','convolution_ms','carry_reconstruct_ms']:row[k]=statistics.median(t[k] for t in trials)
    rows.append(row);local.append(row)
   best.append(min(local,key=lambda x:x['total_ms']))
   print(N,best[-1],flush=True)
   Path(__file__).with_name('BENCHMARK_PARTIAL.json').write_text(json.dumps({'rows':rows,'best':best},indent=2))
 Path(__file__).with_name('BENCHMARK.json').write_text(json.dumps({'rows':rows,'best':best,'timing_scope':'3-run medians; complete conversion+NTT/CRT+carry+reconstruction; same Python backend and same allocated input pair; input ingestion excluded. Native coefficient carry divmod charged in timing, no fastest-library claim; finite CRT capacity.'},indent=2))
 print(json.dumps(best,indent=2))
