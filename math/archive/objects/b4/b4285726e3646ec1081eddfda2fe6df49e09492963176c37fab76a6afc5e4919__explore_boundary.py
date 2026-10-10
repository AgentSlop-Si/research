import sympy as s,json,time
z=s.symbols('z');t=s.symbols('t0:4');w=s.symbols('w');sig=[2,7,5,0,6,1,3,4];J=[1,2,4,5,6]
def red(x):return s.rem(s.expand(x),z**4+1,z).expand()
M=s.Matrix(8,8,lambda r,j:red(z**((2*(j//2)*r)%8)+(-1)**j*t[j//2]*z**(((2*(j//2)+1)*r)%8)))
B=[red(M[0,j]+w*M[7,j]) for j in range(8)]
R=[]
for r in range(1,8):
 E=[j for j in J if r not in {j,(j+1)%8,sig[j]}]
 for ix,j in enumerate(E):
  for k in E[ix+1:]:
   b=lambda j:red(B[sig[j]]*M[r,j]-B[j]*M[r,sig[j]])
   c=lambda j:red(B[sig[j]]*M[r-1,j]-B[j]*M[r-1,sig[j]])
   f=red(b(j)*c(k)-b(k)*c(j))
   R.append(((r,j,k),f))
print('GENERATED',flush=True)
for label,f in R:
 f0=red(f.subs(w,0));print(label, s.factor(f0),flush=True)
with open('boundary_factorization_escape_0328/exact_formula_text.json','w') as out:json.dump({'B':[str(b) for b in B],'R':[{'index':idx,'expr':str(f)} for idx,f in R]},out,indent=2)
