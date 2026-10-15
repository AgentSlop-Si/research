import json,random,math
from pathlib import Path

def div_p(x,m,ledger):
 p=(1<<m)-1;q=0
 while x>>m:
  hi=x>>m;lo=x&p
  ledger['folds']+=1;ledger['scan_bit_upper']+=x.bit_length()+max(q.bit_length(),hi.bit_length())+2
  q+=hi;x=hi+lo
 if x>=p:q+=1;x-=p
 return q,x

def encode(x,m,d):
 ledger={'folds':0,'scan_bit_upper':0,'p_digits':0};out=[];p=(1<<m)-1
 while x:
  digit=0;weight=1
  for _ in range(d):
   x,a=div_p(x,m,ledger);digit+=a*weight
   weight=(weight<<m)-weight;ledger['p_digits']+=1
  out.append(digit)
 return out or [0],ledger

def decode(a,m,d):
 x=0;bit_work=0
 for z in reversed(a):
  for _ in range(d):bit_work+=x.bit_length()+m;x=(x<<m)-x
  bit_work+=max(x.bit_length(),z.bit_length())+1;x+=z
 return x,bit_work

def multiply(a,b,m,d):
 # Explicit schoolbook control, not a fast candidate or a free large product.
 p=(1<<m)-1;Q=p**d
 c=[0]*(len(a)+len(b));calls=[]
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   calls.append((x.bit_length(),y.bit_length()));s=0;v=x;u=y
   while u:
    if u&1:s+=v
    u>>=1;v<<=1
   c[i+j]+=s
 carry=0
 for i in range(len(c)):
  v=c[i]+carry;digit=0;weight=1
  for _ in range(d):
   v,r=div_p(v,m,{'folds':0,'scan_bit_upper':0});digit+=r*weight;weight=(weight<<m)-weight
  c[i]=digit;carry=v
 assert carry==0
 return c,calls

if __name__ == '__main__':
 R=random.Random(74191);divs=products=roundtrips=0;rows=[]
 for m in [2,3,5,7,13]:
  p=(1<<m)-1;assert all(p%t for t in range(2,math.isqrt(p)+1))
  for d in [1,2,3,4,8]:
   Q=p**d
   for n in [1,8,32,128,512]:
    for X in [0,(1<<n)-1,R.getrandbits(n)]:
     Y=R.getrandbits(n);a,L=encode(X,m,d);b,_=encode(Y,m,d)
     x,w=decode(a,m,d);assert x==X;roundtrips+=1
     c,calls=multiply(a,b,m,d);z,_=decode(c,m,d);assert z==X*Y;products+=1
     assert all(0<=t<Q for t in a+c)
    rows.append({'N':n,'m':m,'p':p,'d':d,'Q_bits':Q.bit_length(),'digits':len(a),'digit_storage_upper_bits':len(a)*Q.bit_length(),'folds':L['folds'],'fold_scan_proxy':L['scan_bit_upper'],'reconstruction_scan_proxy':w,'schoolbook_scalar_products':len(calls),'coefficient_bound_bits':(max(len(a),len(b))*(Q-1)**2).bit_length()})
  for n in range(0,300,7):
   x=R.getrandbits(n);q,r=div_p(x,m,{'folds':0,'scan_bit_upper':0});assert(q,r)==divmod(x,p);divs+=1
 # Every odd prime power of a Mersenne prime p=2^m-1,m>=2 has v2(phi)=1.
 root_rows=[]
 for m,d in [(2,1),(2,2),(2,3),(3,1),(3,2),(5,1)]:
  p=(1<<m)-1;Q=p**d
  fourth=[a for a in range(Q) if math.gcd(a,Q)==1 and pow(a,4,Q)==1 and pow(a,2,Q)!=1]
  assert not fourth;root_rows.append({'p':p,'d':d,'modulus':Q,'primitive_order4_units':len(fourth)})
 Path(__file__).with_name('RESULTS.json').write_text(json.dumps({'roundtrips':roundtrips,'full_products':products,'divmod_checks':divs,'root_controls':root_rows,'parameter_ledgers':rows,'scope':'Reference exact base-p^d grouping using Mersenne shift/add divmod and shift/subtract reconstruction; schoolbook control, not a speedup; scan proxies are not runtime'},indent=2))
 print(roundtrips,products,divs)
