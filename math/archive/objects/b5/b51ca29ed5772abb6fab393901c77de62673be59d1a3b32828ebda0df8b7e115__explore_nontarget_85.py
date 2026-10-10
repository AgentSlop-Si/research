# Independent, same-package arithmetic only; half-degree targets excluded.
import independent_controls as c
import sympy as s
N=85
fs=s.factor_list(s.Poly(s.cyclotomic_poly(N,c.q),c.q,modulus=2))[1]
for fpoly,_ in fs:
 f=sum(int(co)%2<<int(exp[0]) for exp,co in fpoly.terms())
 hs=[[1],[1,1]];bad=[]
 for n in range(2,N):
  hs.append(c.add(c.add(hs[-1],c.mulz(hs[-1])),c.scale(c.mulz(hs[-2]),1^c.fpow(2,n-1,f),f)))
  if n%2==0 and n!=(N-1)//2:
   g=c.zgcd(hs[-1],c.deriv(hs[-1]),f)
   if len(g)>1:bad.append((n,len(g)-1))
 print(N,hex(f),bad,flush=True)
