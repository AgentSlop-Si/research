import sympy as s,time
N=16;A,B,c,d,e=s.symbols('A B c d e');vs=[A,B,c,d,e]
cs=[s.Integer(0)]*N;cs[:3]=[s.Integer(1),A,B]
for stride,alpha in [(3,c),(5,d),(7,e)]:cs=[s.expand(cs[i]+alpha*cs[(i-stride)%N]) for i in range(N)]
eq=[s.expand((-1)**i*cs[i]-cs[(i-8)%N]) for i in range(8)]
print(list(enumerate(cs)),flush=True);print(eq,flush=True)
for p in [17,0]:
 t=time.time();g=s.groebner(eq,*vs,modulus=p or None);print(p,list(g),time.time()-t,flush=True)
