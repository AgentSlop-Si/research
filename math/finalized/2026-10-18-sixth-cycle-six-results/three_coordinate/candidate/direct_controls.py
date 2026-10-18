"""Fresh exact direct Gaussian inversions and all-entry model bridge controls.
These are transcription checks, not a substitute for the universal proof.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
ROOT=Path(__file__).resolve().parent
CHART=json.loads((ROOT/'sources/CHART.json').read_text())
class G:
 __slots__=('a','b')
 def __init__(self,a=0,b=0):
  if isinstance(a,G):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,o):
  o=G(o);return G(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return G(-self.a,-self.b)
 def __sub__(self,o):return self+-G(o)
 def __rsub__(self,o):return G(o)+-self
 def __mul__(self,o):
  o=G(o);return G(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def conj(self):return G(self.a,-self.b)
 def inv(self):
  d=self.a*self.a+self.b*self.b;assert d;return G(self.a/d,-self.b/d)
 def __truediv__(self,o):return self*G(o).inv()
 def __eq__(self,o):
  o=G(o);return self.a==o.a and self.b==o.b
 def __bool__(self):return bool(self.a or self.b)
 def abs2(self):return self.a*self.a+self.b*self.b
 def out(self):return [str(self.a),str(self.b)]
def eye():return [[G(i==j)for j in range(8)]for i in range(8)]
def zero():return [[G()for j in range(8)]for i in range(8)]
def add(A,B):return [[A[i][j]+B[i][j]for j in range(8)]for i in range(8)]
def scale(A,v):return [[a*v for a in row]for row in A]
def mm(A,B):return [[sum((A[i][k]*B[k][j]for k in range(8)),G())for j in range(8)]for i in range(8)]
def transpose(A):return [list(x)for x in zip(*A)]
def conj(A):return [[a.conj()for a in row]for row in A]
def invert(A):
 a=[A[i][:]+eye()[i]for i in range(8)]
 for k in range(8):
  r=next((r for r in range(k,8)if a[r][k]),None)
  if r is None:return None
  a[k],a[r]=a[r],a[k];v=a[k][k].inv();a[k]=[x*v for x in a[k]]
  for r in range(8):
   if r==k:continue
   v=a[r][k]
   if v:a[r]=[x-v*y for x,y in zip(a[r],a[k])]
 return [row[8:]for row in a]
def branch(s,b,label,point):
 cycle=CHART['stages'][s]['cycles'][b];W=zero();h=G(1)
 for j in range(8):
  e=8*b+j;v=G(1)
  if e>=7:
   a,bb=CHART['stages'][s]['gaussian_pairs'][e-7];v=G(a,bb)/G(a,-bb)
  if (s,e)in label:v=v*point[label.index((s,e))]
  W[cycle[j]][cycle[j-1]]=v;h=h*v
 d=G(1)-h;assert d
 B=eye();power=eye()
 for k in range(1,8):power=mm(power,W);B=add(B,power)
 T=add(eye(),scale(W,G(-1)));Ginv=invert(T);assert Ginv is not None
 assert mm(T,Ginv)==eye()and mm(Ginv,T)==eye()
 assert mm(T,B)==scale(eye(),d)and mm(B,T)==scale(eye(),d)
 assert B==scale(Ginv,d)
 return B,d,Ginv

def control(label,point):
 Bs=[];Ds=[];S=[];A=[];st=time.time()
 for s in range(2):
  bs=[branch(s,b,label,point)for b in range(3)];D=G(1);stage=zero();numer=zero()
  for B,d,g in bs:D=D*d;stage=add(stage,g)
  for b,(B,d,g)in enumerate(bs):
   other=G(1)
   for j,(_,dj,_)in enumerate(bs):
    if j!=b:other=other*dj
   numer=add(numer,scale(B,other))
  assert numer==scale(stage,D)
  assert add(stage,transpose(conj(stage)))==scale(eye(),G(3))
  Bs.append(bs);Ds.append(D);S.append(stage);A.append(numer)
 Delta=Ds[1]*Ds[0];M=mm(S[1],S[0]);N=mm(A[1],A[0]);assert N==scale(M,Delta)
 R=point[0]*point[1]*point[2];Nt=scale(conj(N),R)
 mult=R*R*G(Delta.abs2()**2)
 count=0
 for a in range(8):
  for r in range(a+1,8):
   for b in range(8):
    for c in range(b+1,8):
     P=N[r][c]*N[a][b]*Nt[r][c]*Nt[a][b]-N[r][b]*N[a][c]*Nt[r][b]*Nt[a][c]
     defect=(M[r][c]*M[a][b]).abs2()-(M[r][b]*M[a][c]).abs2()
     assert P==mult*G(defect);count+=1
 return {'label':label,'point':[z.out()for z in point],'inverse_checks':6,'numerator_entries':64,'modulus_windows':count,'seconds':time.time()-st}
def main():
 reps=[[(0,16),(0,17),(0,18)],[(1,16),(1,17),(1,18)],[(0,7),(0,8),(0,9)],[(1,8),(1,9),(1,16)],[(0,8),(0,9),(1,7)],[(0,16),(1,8),(1,9)],[(0,7),(0,8),(1,7)],[(0,8),(1,8),(1,16)]]
 points=[[G(1),G(1),G(1)],[G(F(3,5),F(4,5)),G(F(5,13),F(12,13)),G(F(8,17),F(15,17))]]
 out=[]
 for L in reps:
  for point in points:
   r=control(L,point);out.append(r);print(json.dumps(r),flush=True)
 (ROOT/'DIRECT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
