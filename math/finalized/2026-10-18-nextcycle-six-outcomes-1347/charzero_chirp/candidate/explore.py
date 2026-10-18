import sympy as S, time, json
from itertools import product
x,z=S.symbols('x z'); theta=S.CRootOf(z**8+1,7); K=S.QQ.algebraic_field(theta)
q=[theta**((-t*t)%16) for t in range(8)]
# coefficients use canonical algebraic field expression for smaller forms
q=[K.to_sympy(K.from_sympy(a)) for a in q]

def equations(counts):
 p=[S.Integer(1)]+[S.Integer(0)]*7; vars=[]
 for s,n in enumerate(counts,1):
  v=S.symbols('a%d_1:%d'%(s,n+1));vars+=list(v)
  f=[S.Integer(0)]*8;f[0]=1
  for j,a in enumerate(v,1):f[(s*j)%8]+=a
  p=[S.expand(sum(p[j]*f[(i-j)%8] for j in range(8))) for i in range(8)]
 y=S.Symbol('y');vars+=[y]
 return [S.expand(p[i]-q[i]*p[0]) for i in range(1,8)]+[y*p[0]-1],vars,p

if __name__=='__main__':
 import sys
 L=int(sys.argv[1]) if len(sys.argv)>1 else 5
 for n1 in range(L+1):
  for n2 in range(L-n1+1):
   for n3 in range(L-n1-n2+1):
    n4=L-n1-n2-n3
    if n1<n3 or n1+n3<4:continue
    counts=(n1,n2,n3,n4); eq,v,p=equations(counts)
    print('START',counts,flush=True);t=time.time()
    g=S.groebner(eq,*v,order='grevlex',domain=K)
    print('DONE',counts,'seconds',round(time.time()-t,2),'basis',len(g.polys),'empty',list(g)==[1],flush=True)
    if list(g)!=[1]:print(g,flush=True)
