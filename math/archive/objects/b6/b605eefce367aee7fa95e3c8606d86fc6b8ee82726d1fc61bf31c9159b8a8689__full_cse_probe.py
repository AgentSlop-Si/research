"""CSE scan across the COMPLETE WFTA120 graph with exact field scalars.
If a duplicate occurs modulo prime, verify independently over another prime
or cyclotomic symbolic ring before calling it a valid characteristic-zero fusion.
"""
from collections import defaultdict
from crt15 import Cost,P,GENERATOR,ALT_P,ALT_GENERATOR
from fused120 import make_fused120_plan
from wfta8 import before8,after8
from wfta15 import before3,after3,before5,after5

class Lin:
 __slots__=('t','idx','vector')
 def __init__(self,t,idx,v):self.t,self.idx,self.vector=t,idx,v
 def __add__(self,other):return self.t.op(self,other,1)
 def __sub__(self,other):return self.t.op(self,other,-1)
 def __mod__(self,p):return self
 def __mul__(self,k):return self.t.scale(self,k)
 def __repr__(self):return f'#{self.idx}'
class C:
 def __init__(self,p,n):
  self.p=p;self.n=n;self.cache={};self.instructions=[]
  self.adds=self.muls=self.add_reuses=self.mul_reuses=self.copy_reuses=0
  for i in range(n):self._new(('input',i),tuple(1 if j==i else 0 for j in range(n)))
 def _new(self,instr,v):
  i=len(self.instructions);x=Lin(self,i,v)
  self.instructions.append(instr);self.cache[v]=x
  return x
 def op(self,a,b,s):
  v=tuple((x+s*y)%self.p for x,y in zip(a.vector,b.vector))
  if v in self.cache:
   self.add_reuses+=1
   return self.cache[v]
  self.adds+=1
  return self._new(('add' if s==1 else 'sub',a.idx,b.idx),v)
 def scale(self,a,k):
  if k==1:return a
  v=tuple((x*k)%self.p for x in a.vector)
  if v in self.cache:
   self.mul_reuses+=1
   return self.cache[v]
  self.muls+=1
  return self._new(('mul',a.idx,k),v)
 @property
 def inp(self):return [self.cache[tuple(1 if j==i else 0 for j in range(self.n))] for i in range(self.n)]

def compile120(plan):
 p=plan.wfta.base.p;c=C(p,120);a=c.inp;dummy=Cost()
 b8=[list(before8(tuple(a[8*v+j] for j in range(8)),p,dummy)) for v in range(15)]
 b3=[[[None]*8 for _ in range(3)] for _ in range(5)]
 for v5 in range(5):
  for t8 in range(8):
   vv=before3(tuple(b8[(10*u3+6*v5)%15][t8] for u3 in range(3)),p,dummy)
   for u3 in range(3):b3[v5][u3][t8]=vv[u3]
 b5=[[[None]*8 for _ in range(3)] for _ in range(6)]
 for u3 in range(3):
  for t8 in range(8):
   vv=before5(tuple(b3[v5][u3][t8] for v5 in range(5)),p,dummy)
   for v5 in range(6):b5[v5][u3][t8]=vv[v5]
 pre=c.adds
 scaled=[[[None]*8 for _ in range(3)] for _ in range(6)]
 for v5 in range(6):
  for u3 in range(3):
   for t8 in range(8):scaled[v5][u3][t8]=b5[v5][u3][t8]*plan.d120[v5][u3][t8]
 mid=c.muls
 p5=[[[None]*8 for _ in range(3)] for _ in range(5)]
 for u3 in range(3):
  for t8 in range(8):
   vv=after5(tuple(scaled[v5][u3][t8] for v5 in range(6)),p,dummy)
   for v5 in range(5):p5[v5][u3][t8]=vv[v5]
 p3=[[None]*8 for _ in range(15)]
 for v5 in range(5):
  for t8 in range(8):
   vv=after3(tuple(p5[v5][u3][t8] for u3 in range(3)),p,dummy)
   for u3 in range(3):p3[(5*u3+3*v5)%15][t8]=vv[u3]
 out=[]
 for v in range(15):out.extend(after8(tuple(p3[v]),p,dummy))
 return c,[z.idx for z in out],{'preadd':pre,'postadd':c.adds-pre,'midmul':mid,'add_reuses':c.add_reuses,'mul_reuses':c.mul_reuses,'total':c.adds+c.muls}

if __name__=='__main__':
 for p,gen in ((P,GENERATOR),(ALT_P,ALT_GENERATOR)):
  plan=make_fused120_plan(120,p=p,gen=gen)
  c,outs,stats=compile120(plan)
  print('field',p,'stats',stats,'nodes',len(c.instructions),'unique outputs',len(set(outs)))
  assert stats['total']<=1178
