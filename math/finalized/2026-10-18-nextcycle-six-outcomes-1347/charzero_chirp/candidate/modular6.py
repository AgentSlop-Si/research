import sympy as S,time
from itertools import product
q=[pow(3,(-t*t)%16,17) for t in range(8)]
def calc(counts):
 p=[S.Integer(1)]+[S.Integer(0)]*7;vs=[]
 for stride,n in enumerate(counts,1):
  vv=S.symbols('a%d_1:%d'%(stride,n+1));vs+=list(vv)
  f=[S.Integer(0)]*8;f[0]=1
  for j,v in enumerate(vv,1): f[(stride*j)%8]+=v
  p=[S.expand(sum(p[j]*f[(i-j)%8] for j in range(8))) for i in range(8)]
 eq=[S.expand(p[i]-q[i]*p[0]) for i in range(1,8)]
 print('START',counts,flush=True);t=time.time()
 g=S.groebner(eq,*vs,modulus=17,order='grevlex',method='f5b')
 print('END',counts,round(time.time()-t,2),len(g.polys),list(g)==[1],flush=True)
 if list(g)!=[1]:print(g,flush=True)
for c in [(3,1,2,0),(4,1,1,0),(3,0,3,0),(4,0,2,0),(5,0,1,0)]:calc(c)
