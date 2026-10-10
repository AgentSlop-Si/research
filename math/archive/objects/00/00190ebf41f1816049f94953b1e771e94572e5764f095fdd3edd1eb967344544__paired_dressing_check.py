import sympy as s,json
from pathlib import Path
z=s.symbols('z');I=s.I;rt=s.sqrt(2);q=(1+I)/rt
Z=s.zeros(4)
for k in range(4):Z[(k+1)%4,k]=1
D=s.diag(*[s.simplify(q**(k*k)) for k in range(4)])
Om=s.diag(1,I,-1,-I);F=s.Matrix([[I**(j*k) for k in range(4)]for j in range(4)])
U=(D*Z*D.inv()).applyfunc(s.simplify);V=(D.inv()*Z*D).applyfunc(s.simplify)
assert all(s.simplify(x)==0 for x in U-q*Z*Om) and all(s.simplify(x)==0 for x in V-q*Om.inv()*Z)
assert all(s.simplify(x)==0 for x in F.inv()*U*F-V)
p0=2-5*z;q0=(1-2*z)*(1-3*z)
p1=(455-1045*z)/s.Integer(874);q1=1+s.Rational(5,874)*z+s.Rational(3,437)*z*z
spoly=(317-730*z+2*z*z+5*z**3)/s.Integer(609)
assert s.rem(s.expand(spoly*p0-q0),z**4-1,z)==0
assert s.rem(s.expand(spoly*q1-p1),z**4-1,z)==0
A=((s.eye(4)-2*U).inv()+(s.eye(4)-3*U).inv()).applyfunc(s.simplify)
C=((317*s.eye(4)-730*V+2*V**2+5*V**3)/609).applyfunc(s.simplify)
B=s.eye(4)+(1-I)/rt*Z-Z**2+(1-I)/rt*Z**3
assert all(s.simplify(x)==0 for x in A*D*B*D*C-F)
comm=(A*C-C*A).applyfunc(s.simplify)
nonzero=[(i,j,str(comm[i,j])) for i in range(4) for j in range(4) if comm[i,j]!=0]
assert nonzero
out={'candidate_identity_exact':True,'U_F_equals_F_V':True,'A_C_noncommuting_entries':len(nonzero),'commutator_first_witness':nonzero[0],'q1_resultant_z4':str(s.factor(s.resultant(q1,z**4-1,z))),'q1_resultant_p1':str(s.factor(s.resultant(q1,p1,z))),'q0_resultant_z4':str(s.factor(s.resultant(q0,z**4-1,z))),'inverse_scope':'N=4 tailored rational inversion; F intertwining cancels the dressing','generic_degree_obstruction':'For nondegenerate proper [1/2] r and s, numerator rs−1 has nonzero degree 4; cannot be divisible by z^N−1 at N≥5.'}
Path(__file__).with_name('PAIRED_DRESSING_RESULTS.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
