"""Independent full Z[q] ordinary-discriminant controls of the fresh local engine."""
import sympy as s,sys,time,json,math
from pathlib import Path
import check_exact as c
q,z=s.symbols('q z');H=[s.Poly(1,z),s.Poly(1+z,z)];results=[]
for n in range(2,9):H.append(s.Poly((1+z)*H[-1].as_expr()-z*(1-q**(n-1))*H[-2].as_expr(),z))
for d,A,b in [(3,1,0),(3,1,1),(3,1,2),(3,2,0),(3,2,1),(3,2,2),(5,1,1)]:
 start=time.time();n=d*A+b;M=d*A*(A-1)//2+A*(b%2)
 D=s.Poly(H[n].discriminant(),q);Phi=s.Poly(s.cyclotomic_poly(d,q),q);quot=D;v=0
 while True:
  nxt,rem=divmod(quot,Phi)
  if not rem.is_zero:break
  v+=1;quot=nxt
 assert v==M
 eng=c.Calc(d,M+1);Cc,extra=eng.expected(A,b)
 quotient_at_root=sum(eng.K.convert(a)*eng.w**i for (i,),a in (quot%Phi).terms())
 assert quotient_at_root==Cc*(eng.w-eng.one)**M
 c.START=time.time();r=eng.reciprocal(eng.H(n));dr,_=eng.det(eng.bezout(r))
 localD=eng.mul(eng.mul(eng.eval(r,2),eng.eval(r,-2)),eng.mul(dr,dr))
 if n%2:localD=eng.mul(localD,eng.mul(eng.eval(r,-2),eng.eval(r,-2)))
 directD=eng.trim([sum((eng.K.convert(a)*eng.w**i*math.comb(i,j) for (i,),a in D.terms() if i>=j),eng.zero) for j in range(M+1)])
 assert localD==directD,'Reciprocal Bezout engine differs from full ordinary discriminant'
 results.append({'d':d,'A':A,'b':b,'n':n,'order':v,'degree_D_in_q':D.degree(),'coefficient_after_Phi_division':eng.expr(quotient_at_root),'seconds':time.time()-start})
 print('full discriminant PASS',d,A,b,n,v,'seconds',round(time.time()-start,3),flush=True)
Path(__file__).with_name('full_small_results.json').write_text(json.dumps(results,indent=2)+'\n')
