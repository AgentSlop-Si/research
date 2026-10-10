import sympy as s
z=s.symbols('z');t=s.symbols('t0:4');aa=s.sqrt(2)*(1+s.I)/2;K=s.QQ.algebraic_field(aa)
def red(x):return s.rem(s.expand(x),z**4+1,z).expand()
M=s.Matrix(8,8,lambda r,j:red(z**((2*(j//2)*r)%8)+(-1)**j*t[j//2]*z**(((2*(j//2)+1)*r)%8)))
sig=[2,7,5,0,6,1,3,4]
E=[]
for j in [2,4,6]:
 f=red(M[0,sig[j]]*M[1,j]-M[0,j]*M[1,sig[j]]);E.append(f)
 print(j,str(s.factor(f.subs(z,aa),extension=aa)).replace(str(aa),'z'),flush=True)
print('groebner',flush=True)
g=s.groebner([f.subs(z,aa) for f in E],*t,domain=K);print(str(g).replace(str(aa),'z'),flush=True)
import json,time
rs=json.load(open('boundary_factorization_escape_0328/exact_formula_text.json'))['R']
for d in rs:
 if d['index'][0]==1:continue
 f=red(s.sympify(d['expr']).subs(s.Symbol('w'),0))
 E.append(f)
 tt=time.time();g=s.groebner([f.subs(z,aa) for f in E],*t,domain=K)
 print('added',d['index'],'basis',len(g.polys), 'seconds',time.time()-tt,flush=True)
 print(str(g).replace(str(aa),'z'),flush=True)
 if g.is_zero_dimensional is False and list(g)==[1]:break
