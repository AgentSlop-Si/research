"""Fresh final-review oracle. No candidate test/oracle imports.
The oracle uses integer-grid interval arithmetic, a different pi identity,
full direct finite summation from the original centered coordinates, and
integer bisection for the unitary root.
"""
import hashlib,json,sys,time
from dataclasses import replace
from fractions import Fraction as F
from math import factorial
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'candidate_snapshot'))
import centered_source as c
Q=320; B=1<<Q

def ceildiv(a,b):return -((-a)//b)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[1],-x[0]
def mul(x,y):
 v=[a*b for a in x for b in y];return min(v)//B,ceildiv(max(v),B)
def smul(x,p,q=1):
 v=[x[0]*p,x[1]*p];return min(v)//q,ceildiv(max(v),q)
def rat(p,q=1):return p*B//q,ceildiv(p*B,q)
def pi_iv():
 def atan(d):
  n=240
  a=sum((F((-1)**j,(2*j+1)*d**(2*j+1)) for j in range(n)),F(0))
  b=a+F((-1)**n,(2*n+1)*d**(2*n+1))
  return min(a,b),max(a,b)
 a=atan(3);b=atan(7)
 lo=8*a[0]+4*b[0];hi=8*a[1]+4*b[1]
 return lo.numerator*B//lo.denominator,ceildiv(hi.numerator*B,hi.denominator)
PI=pi_iv()

def root(k,M):
 # exp(-2*pi*i*k/M); full interval recurrence, no midpoint.
 k%=M
 if 2*k>M:k-=M
 x=smul(PI,-2*k,M)
 real,imag=(B,B),(0,0);tr,ti=(B,B),(0,0)
 for n in range(1,129):
  tr,ti=smul(neg(mul(ti,x)),1,n),smul(mul(tr,x),1,n)
  real,imag=add(real,tr),add(imag,ti)
 err=ceildiv(4**129*B,factorial(129))
 return (real[0]-err,real[1]+err),(imag[0]-err,imag[1]+err)
def cmul(z,w):
 return add(mul(z[0],w[0]),neg(mul(z[1],w[1]))),add(mul(z[0],w[1]),mul(z[1],w[0]))
def power(z,n):
 if n<0:z=(z[0],neg(z[1]));n=-n
 out=((B,B),(0,0))
 while n:
  if n&1:out=cmul(out,z)
  z=cmul(z,z);n//=2
 return out

def rroot(M):
 lo,hi=0,B
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid*mid*M<=B*B:lo=mid
  else:hi=mid
 assert lo*lo*M<=B*B<hi*hi*M
 return lo,lo if lo*lo*M==B*B else hi

def direct_original(m,a,b,h,k):
 M=1<<m;N=M//4;origin=(N-1)//2
 w=root(k,M);term=power(w,-origin)
 total=((0,0),(0,0))
 for j in range(N):
  total=add(total[0],term[0]),add(total[1],term[1])
  term=cmul(term,w)
 val=cmul(total,(rat(a,1<<h),rat(b,1<<h)))
 r=rroot(M)
 return mul(val[0],r),mul(val[1],r)

def cyclo_controls():
 rows=[]
 for m in range(3,10):
  M=1<<m;N=M//4;supp=[]
  for k in range(M):
   coeff=[0]*(M//2)
   for j in range(N):
    e=(-k*(j-(N-1)//2))%M
    coeff[e%(M//2)]+=1 if e<M//2 else -1
   if any(coeff):supp.append(k)
  assert supp==[k for k in range(M) if k==0 or k%4]
  assert len(supp)==3*N+1
  rows.append({'m':m,'N':N,'exact_support':len(supp)})
 return rows

def main():
 started=time.monotonic(); out={'source_sha256':hashlib.sha256((HERE/'candidate_snapshot/centered_source.py').read_bytes()).hexdigest(),'cyclotomic_controls':cyclo_controls(),'full_production_runs':[],'rejections':[]}
 m=11;N=1<<(m-2);a,b=-3,5;E=N*(a*a+b*b);h=((E-1).bit_length()+1)//2
 original={'m':m,'F':h+44,'kind':'dense','data':[(a,b)]*N}
 answer,receipt=c.produce(original)
 assert answer.source.scale==-44 and receipt['events']['dense_coordinate_visits']==N
 assert answer.exact_support_size==3*N+1 and len(answer.pairs)==13
 all_intervals=[]
 for k,(x,y) in answer.pairs:
  iv=direct_original(m,a,b,h,k)
  radii=[max(abs(F(v,1<<answer.bits)-F(lo,B)),abs(F(v,1<<answer.bits)-F(hi,B))) for v,(lo,hi) in zip((x,y),iv)]
  err=sum(r*r for r in radii)
  assert err<=F(1,1<<(2*answer.bits)),(k,err)
  all_intervals.append({'k':k,'real':list(map(str,iv[0])),'imag':list(map(str,iv[1])),'squared_error_upper':str(err)})
 out['full_production_runs'].append({'m':m,'kind':'dense','N':N,'support':len(answer.pairs),'scale':answer.source.scale,'receipt':receipt,'independent_direct_sum_coordinates':len(all_intervals)})
 (HERE/'ORACLE_INTERVALS.json').write_text(json.dumps({'bits':Q,'coordinates':all_intervals},indent=2)+'\n')
 # Fresh full positive-scale run and full original replay with mutated output.
 obj={'m':11,'F':h-44,'kind':'constant','data':(a,b)}
 positive,r2=c.produce(obj)
 assert positive.source.scale==44 and positive.pairs==answer.pairs
 out['full_production_runs'].append({'m':11,'kind':'constant','N':N,'support':len(positive.pairs),'scale':positive.source.scale,'receipt':r2})
 bad_pairs=((positive.pairs[0][0],(positive.pairs[0][1][0]+1,positive.pairs[0][1][1])),)+positive.pairs[1:]
 ok,replay=c.replay(obj,replace(positive,pairs=bad_pairs));assert not ok
 out['mutated_output_full_replay']={'accepted':ok,'receipt':replay}
 L=c.Ledger();big=(1<<1023)+1
 bs=c.recognize({'m':11,'F':1030,'kind':'constant','data':(big,-7)},L)
 assert bs.real==big and L.report()['max_numeric_width']>=2047
 out['wide_recognition_receipt']=L.report()
 controls=[dict(obj,m=True),dict(obj,m=10),dict(obj,m=29),dict(obj,F=True),dict(obj,F=h-45),dict(obj,F=h+45),dict(obj,data=(0,0)),dict(obj,data=(2,4)),dict(obj,data=(1<<1024,1)),dict(obj,data=(True,1)),dict(obj,data=(1,)),dict(original,data=[(a,b)]*(N-1)),dict(original,data=[(a,b)]*(N-1)+[(a,b+1)]),dict(original,data=[(a,b)]*(N-1)+[(a+2,b)]),dict(obj,unknown=1)]
 for test in controls:
  try:c.produce(test)
  except c.Rejected as e:
   assert hasattr(e,'receipt')
   out['rejections'].append({'reason':str(e),'receipt':e.receipt})
  else:raise AssertionError(('missing rejection',test))
 # Original representation is copied to immutable source, never alias-retained.
 original['data'][-1]=(99,99)
 assert (answer.source.real,answer.source.imag)==(a,b)
 out['normalization_and_cutoff_controls']=[]
 for m in range(11,129):
  M=1<<m;N=M//4;K=1<<((m+3)//4);P=16*m+16
  assert K**4>=M and K<M//2 and 160*m+4<M
  assert (1<<(4*(P-1)))>=M
  for a,b in [(1,0),(0,-1),(-3,5),((1<<1023)+1,-7)]:
   E=N*(a*a+b*b);h=((E-1).bit_length()+1)//2
   assert 4*E>1<<(2*h) and E<=1<<(2*h)
  out['normalization_and_cutoff_controls'].append(m)
 out.update(status='PASS',wall_seconds=time.monotonic()-started,historical_programs_executed=False,candidate_oracle_imported=False,full_outer_executed=False,external_writes=False)
 (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'full_frontend_executions':3,'direct_original_coordinates':len(all_intervals),'rejections':len(out['rejections']),'wall_seconds':out['wall_seconds']},indent=2))
if __name__=='__main__':main()
