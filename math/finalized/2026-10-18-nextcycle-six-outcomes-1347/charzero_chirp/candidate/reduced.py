import sympy as S,time,json
D,E,F=S.symbols('D E F');a=6;b=4;p=17

def num(e):return S.Poly(S.cancel(e).as_numer_denom()[0],D,E,modulus=p).as_expr()
def run(name,eq):
 eq=[num(e) for e in eq];print(name,'eqs',eq,flush=True)
 t=time.time();g=S.groebner(eq,D,E,modulus=p,order='grevlex');print(name,'basis',g,'time',time.time()-t,flush=True)

# (5,0,1,0)
eq1=a*D**2-D+a
eq2=b*D**4+a*D**3+D**2+a*D+b
print('510',S.gcd(S.Poly(eq1,D,modulus=p),S.Poly(eq2,D,modulus=p)),flush=True)
# (4,0,2,0)
EE=b+a*D+a/D;h=D/(D+a*EE)
eqs=[EE-D**2-h*(a*D+b),a/EE-a*EE-D*EE/h-a]
print('420',[S.Poly(S.cancel(e).as_numer_denom()[0],D,modulus=p).as_expr() for e in eqs],flush=True)
print('420_gcd',S.gcd(*[S.Poly(S.cancel(e).as_numer_denom()[0],D,modulus=p) for e in eqs]),flush=True)
# (3,0,3,0)
h=D/(D+a*E);A=a*h/E;B=-a*h/D;C=(b*h-E)/D;F=E*(b/a+1/D)
# use Rational!
F=E*(S.Rational(b,a)+1/D)
run('330',[A+C*E+F-a*h,C+D+B*F+a*h,A*D+C*F-h])
# (4,1,1,0)
BB=-2*D**2/(1+D**4);AA=2*D**3/(1+D**4);HH=D*(D**4-1)/(1+D**4)
ee=(b-BB)/(1-b*BB)
eqs=[AA+HH+(AA-HH)*ee, AA-HH*ee-a*(1+BB*ee)]
print('411 polys',[S.Poly(S.cancel(e).as_numer_denom()[0],D,modulus=p).as_expr() for e in eqs],flush=True)
print('411 gcd',S.gcd(*[S.Poly(S.cancel(e).as_numer_denom()[0],D,modulus=p) for e in eqs]),flush=True)
# (3,1,2,0)
R=1-E**2-D**2*E;AA=D**3/R;CC=-D-AA*E;BB=E-D**2-AA*D*E
u=AA*D;v=BB;r=-BB*D;ss=-AA*E
f0=1+BB*E-AA*D
lin=[(v-b*u,u-b*v),(r+ss,r-ss),(r-a*u,-ss-a*v)]
fs=[f0]+[lin[i][0]*lin[j][1]-lin[i][1]*lin[j][0] for i,j in [(0,1),(0,2),(1,2)]]
run('312',fs)
