import sympy as S
z=S.Symbol('z'); t=S.symbols('t0:4'); u=S.symbols('u0:8')
pi=list(range(1,8))+[0];sig=[2,7,5,0,6,1,3,4];k=[3,0,0,1,0,0,0,1]
def red(a): return S.rem(S.expand(a),z**4+1,z)
M=S.Matrix(8,8,lambda r,j: z**((r*(j//2*2))%8)+(-1)**j*t[j//2]*z**((r*(j//2*2+1))%8))
A=S.Matrix(8,8,lambda r,j:red(M[r,j]+u[r]*M[(r-1)%8,j]))
h={}
for j in range(8):
 for r in range(8):
  if r not in [j,pi[j],sig[j],k[j]]:
   h[r,j]=red(A[k[j],sig[j]]*A[r,j]-A[k[j],j]*A[r,sig[j]])
for ij,q in h.items():
 fac=S.factor(q,extension=S.sqrt(2))
 print(ij, len(S.Poly(q,*t,*u).terms()),':',fac)
