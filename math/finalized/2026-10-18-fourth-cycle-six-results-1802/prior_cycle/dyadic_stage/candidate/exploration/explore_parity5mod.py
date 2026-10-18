import sympy as s,itertools,json,time
N=16
v=s.symbols('a b c d e');z=s.Symbol('z')
for strides in itertools.combinations_with_replacement(range(1,N//2,2),5):
    cs=[s.Integer(0)]*N;cs[0]=s.Integer(1)
    for stride,alpha in zip(strides,v):
        cs=[s.expand(cs[i]+alpha*cs[(i-stride)%N]) for i in range(N)]
    eq=[s.expand((-1)**i*cs[i]-cs[(i-N//2)%N]) for i in range(N)]
    eq=[f for f in eq if f!=0]
    tt=time.time();g=s.groebner(eq,*v,modulus=17)
    print(strides,'basis',list(g),'secs',round(time.time()-tt,3),flush=True)
