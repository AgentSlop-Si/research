# All functions imported here were freshly authored in this same package.
import independent_controls as c
import sympy as s
for N in [5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65]:
 fs=s.factor_list(s.Poly(s.cyclotomic_poly(N,c.q),c.q,modulus=2))[1]
 f=sum(int(co)%2<<int(exp[0]) for exp,co in fs[0][0].terms())
 hs=[[1],[1,1]];bad=[]
 for n in range(2,N):
  hs.append(c.add(c.add(hs[-1],c.mulz(hs[-1])),c.scale(c.mulz(hs[-2]),1^c.fpow(2,n-1,f),f)))
  if n%2==0 and n!=(N-1)//2:
   g=c.zgcd(hs[-1],c.deriv(hs[-1]),f)
   if len(g)>1:bad.append((n,len(g)-1))
 print(N,hex(f),bad,flush=True)
