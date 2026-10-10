import sympy as s,json,time
z=s.symbols('z');t=s.symbols('t0:4');w=s.symbols('w');aa=s.sqrt(2)*(1+s.I)/2;K=s.QQ.algebraic_field(aa)
def red(x):return s.rem(s.expand(x),z**4+1,z).expand()
def clean(x):return red(s.together(x).as_numer_denom()[0])
def fac(x,vs):
 cc,ff=s.factor_list(x.subs(z,aa),*vs,domain=K);return str(cc).replace(str(aa),'z'),[(str(f).replace(str(aa),'z'),p) for f,p in ff]
data=json.load(open('boundary_factorization_escape_0328/exact_formula_text.json'));R=[(tuple(x['index']),s.sympify(x['expr'])) for x in data['R']]
sub={t[0]:(1+w)/(1-w*z**3),t[1]:-(1-w*z**2)/(1-w*z),t[2]:(1-w)/(1+w*z**3)}
for idx,f in R:
 if idx[-2:]==(4,6):
  nf=clean(f.subs(sub));print(idx,fac(nf,(t[3],w)),flush=True)
