import sympy as s,itertools,json,time
N=16
v=s.symbols('a b c');z=s.Symbol('z')
for strides in itertools.combinations_with_replacement(range(1,N//2,2),3):
    cs=[s.Integer(0)]*N;cs[0]=s.Integer(1)
    for stride,alpha in zip(strides,v):
        cs=[s.expand(cs[i]+alpha*cs[(i-stride)%N]) for i in range(N)]
    eq=[s.expand((-1)**i*cs[i]-cs[(i-N//2)%N]) for i in range(N)]
    eq=[f for f in eq if f!=0]
    g=s.groebner(eq,*v,order='grevlex') if False else s.groebner(eq,*v)
    # Saturate first by nonzero parameters; allow zero too if unit impossible
    g2=s.groebner(list(g)+[z*s.prod(1-a**N for a in v)-1],z,*v)
    print(strides,'unit',list(g2)==[1],'basis',list(g),flush=True)
