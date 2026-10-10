#!/usr/bin/env python3
"""Own exact Gaussian rationals and independent real-arithmetic controls."""
from fractions import Fraction as Q
from pathlib import Path
import math,cmath,random,json,sys
R=random.Random(360049)
class Z:
 def __init__(self,a=0,b=0):
  if isinstance(a,Z):self.a,self.b=a.a,a.b
  else:self.a,self.b=Q(a),Q(b)
 def __add__(self,y):y=Z(y);return Z(self.a+y.a,self.b+y.b)
 __radd__=__add__
 def __neg__(self):return Z(-self.a,-self.b)
 def __sub__(self,y):return self+-Z(y)
 def __rsub__(self,y):return Z(y)+-self
 def __mul__(self,y):y=Z(y);return Z(self.a*y.a-self.b*y.b,self.a*y.b+self.b*y.a)
 __rmul__=__mul__
 def inverse(self):n=self.a*self.a+self.b*self.b;assert n;return Z(self.a/n,-self.b/n)
 def __truediv__(self,y):return self*Z(y).inverse()
 def __pow__(self,n):
  a=self;o=Z(1)
  while n:
   if n&1:o=o*a
   a=a*a;n//=2
  return o
 def __eq__(self,y):y=Z(y);return self.a==y.a and self.b==y.b
 def encode(self):return [str(self.a),str(self.b)]
def eye(n):return [[Z(i==j) for j in range(n)] for i in range(n)]
def inverse(a):
 n=len(a);z=[row[:]+eye(n)[i] for i,row in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]!=0);z[j],z[k]=z[k],z[j];c=z[j][j].inverse();z[j]=[v*c for v in z[j]]
  for k in range(n):
   if k!=j:
    c=z[k][j];z[k]=[v-c*w for v,w in zip(z[k],z[j])]
 return [r[n:] for r in z]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def mv(a,v):return [sum(x*y for x,y in zip(r,v)) for r in a]
def transpose(a):return list(map(list,zip(*a)))
def green(cycle,beta):
 n=len(cycle);pos={a:i for i,a in enumerate(cycle)}
 return [[(1-beta)*beta**((pos[i]-pos[j])%n)/(1-beta**n) for j in range(n)] for i in range(n)]
def apply_scan(v,cycle,beta):
 # Solve z_i-beta*z_(i-1)=(1-beta)v_i, with one cyclic boundary.
 n=len(v);y=[(1-beta)*v[i] for i in cycle];b=0.
 for c in y:b=beta*b+c
 last=b/(1-beta**n);out=[0.]*n
 for index,c in zip(cycle,y):last=beta*last+c;out[index]=last
 return out

def hilbert(x,y):z=[math.log(a/b) for a,b in zip(x,y)];return max(z)-min(z)
def main():
 out={'status':'PASS','uploaded_or_constructor_code_executed':False}
 eta=Q(1,100);beta=Q(3,4);n=4
 def outer(cyc):
  K=green(cyc,beta);return [[Z((1-eta)*int(i==j)+eta*K[i][j]) for j in range(n)] for i in range(n)]
 A=outer([0,2,1,3]);C=outer([3,1,0,2]);F=[[Z(0,-1)**(i*j) for j in range(n)] for i in range(n)];T=mm(mm(inverse(A),F),inverse(C));ratio=T[1][1]*T[0][0]/(T[1][0]*T[0][1]);assert ratio.b!=0
 den=2899912539166173803846278624737183270854842628572414500711388681
 assert ratio==Z(Q(3598426342590615405569035189606615739332947216624193886508681,den),Q(-2896118313759061238277363483611594285821834743452719850733760000,den))
 out['exact_N4_crossratio']=ratio.encode();assert mm(A,inverse(A))==eye(4);assert mm(C,inverse(C))==eye(4)
 # Numerical calibration tests use no source recurrence or optimizer.
 records=[];contraction=0;scancontrols=0
 tau=(math.e-1)/(math.e+1)
 for n in [4,6,8,16,32,64]:
  for trial in range(3):
   cycles=[R.sample(range(n),n) for _ in range(3)];beta=1-1/n;K=green(cycles[1],beta);Kt=transpose(K);KA=green(cycles[0],beta);KC=green(cycles[2],beta);eta=.01
   A=[[(1-eta)*(i==j)+eta*KA[i][j] for j in range(n)] for i in range(n)];C=[[(1-eta)*(i==j)+eta*KC[i][j] for j in range(n)] for i in range(n)];p=A[0];q=[r[0] for r in C]
   assert max(max(r) for r in K)/min(min(r) for r in K)<math.e
   for _ in range(2):
    x=[R.uniform(-1,1) for i in range(n)];got=apply_scan(x,cycles[1],beta);want=mv(K,x);assert max(abs(a-b) for a,b in zip(got,want))<1e-12;scancontrols+=1
   def update(v):return [a/b for a,b in zip(q,mv(Kt,[a/b for a,b in zip(p,mv(K,v))]))]
   v=[1.]*n;vother=[10**R.uniform(-3,3) for i in range(n)]
   for it in range(25):
    vn=update(v);vo=update(vother)
    if hilbert(v,vother)>1e-11:assert hilbert(vn,vo)<=tau*tau*hilbert(v,vother)+1e-12;contraction+=1
    v=vn;vother=vo
   u=[a/b for a,b in zip(p,mv(K,v))];col=[a*b for a,b in zip(v,mv(Kt,u))];res=max(abs(a/b-1) for a,b in zip(col,q));assert res<2e-12
   x=[a/b for a,b in zip(u,p)];y=[a/b for a,b in zip(v,q)];assert max(x)/min(x)<=math.e and max(y)/min(y)<=math.e
   calibrated=mm(mm([[A[i][j]*x[j] for j in range(n)] for i in range(n)],K),[[y[i]*C[i][j] for j in range(n)] for i in range(n)])
   assert max([abs(t-1) for t in calibrated[0]]+[abs(row[0]-1) for row in calibrated])<2e-12
   records.append({'N':n,'relative_marginal_tolerance':'2e-12','first_cross_tolerance':'2e-12'})
 out['calibration_records']=records;out['scan_controls']=scancontrols;out['contraction_controls']=contraction
 # Strong positive-phase Frobenius barrier; choose best positive amplitudes
 # for random rank-one phases, rather than inflating the residual.
 phasecontrols=0;gramcontrols=0
 for n in [4,6,8,12,16,32]:
  w=cmath.exp(-2j*math.pi/n);g=math.gcd(2,n);c=max(.5*math.sqrt(1-1/n),math.sqrt((1-math.sqrt(g/n))/2))
  for i in range(n):
   for j in range(n):
    value=sum(w**(2*(i-j)*k) for k in range(n));assert abs(value-(n if (2*(i-j))%n==0 else 0))<1e-10;gramcontrols+=1
  for _ in range(10):
   u=[cmath.exp(2j*math.pi*R.random()) for i in range(n)];v=[cmath.exp(2j*math.pi*R.random()) for i in range(n)];err=0
   for i in range(n):
    for j in range(n):
     h=w**(i*j);phase=u[i]*v[j];amp=max(1e-12,(h/phase).real);err+=abs(h-amp*phase)**2/n
   assert err>=n*c*c-1e-10;phasecontrols+=1
 out['positive_phase_controls']=phasecontrols;out['doubled_character_gram_entries']=gramcontrols
 # All distinct row/column cross ratios, using exact integer exponent arithmetic.
 cross=0
 for n in [4,8,12,16]:
  values=set();fourier=set()
  for i in range(n):
   for j in range(i+1,n):
    for k in range(n):
     for l in range(k+1,n):
      exponent=((i-k)%n+(j-l)%n-(i-l)%n-(j-k)%n);assert exponent in (-n,0,n);values.add(exponent//n);fourier.add(((i-j)*(k-l))%n);cross+=1
  assert len(fourier)==n
  assert values<={-1,0,1}
 out['exact_crossratio_exponent_checks']=cross
 # H(zeta) row-difference determinant for several exact rational zeta.
 determinants=[]
 for n in [2,3,4,5,8]:
  for z in [-2,-1,0,2,3]:
   a=[[Q(z if i<j else 1) for j in range(n)] for i in range(n)];det=Q(1)
   for j in range(n):
    pivot=a[j][j];assert pivot;det*=pivot
    for i in range(j+1,n):
     c=a[i][j]/pivot
     for k in range(j,n):a[i][k]-=c*a[j][k]
   assert det==(1-z)**(n-1);determinants.append([n,z,str(det)])
 out['phase_determinant_controls']=len(determinants);out['outer_limit']=round(.98**2*(1+1/math.sqrt(2))-1,12);out['necessary_phase_rank_fraction']=str(1-4*(Q(2500,2401)-1)**2)
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
