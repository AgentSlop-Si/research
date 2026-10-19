"""Fresh symbolic certificate for an explicit C8 rank-zero witness.
No author or historical code is imported or run. Symbolic identities only.
"""
import sympy as s, json, time
started=time.time(); I=s.I; rt=s.sqrt(2); z=s.symbols('z',nonzero=True)
zeta=(1+I)/rt
A4=[-z,z/zeta,s.Integer(1),1/zeta]
B4=[s.Integer(1),zeta**3/z,-1/z,zeta**3]
A=s.diag(*(A4*2)); B=s.diag(*(B4*2))
F=s.Matrix(8,8,lambda j,k:s.expand_complex(zeta**((-j*k)%8))/s.sqrt(8))
simp=lambda x:s.simplify(s.expand_complex(x)) if not x.free_symbols else s.simplify(s.expand(x))
# Keeping z formally complex avoids unwanted conjugation assumptions in algebra.
U=(F*A*F*B).applyfunc(simp)
checks={}
checks['F_unitary']=all(s.simplify(v)==0 for v in F.conjugate().T*F-s.eye(8))
T=s.zeros(8)
columns=[]
for parity in [0,1]:
 for eta in [1,-1]:
  for j in [parity,parity+2]:
   v=s.zeros(8,1);v[j]=1/s.sqrt(2);v[j+4]=eta/s.sqrt(2);columns.append(v)
T=s.Matrix.hstack(*columns)
blocks=(T.T*U*T).applyfunc(simp)
checks['sector_transform_orthogonal']=T.T*T==s.eye(8)
checks['off_block_entries_vanish']=all(s.simplify(blocks[j,k])==0 for j in range(8) for k in range(8) if j//2!=k//2)
alpha=(1-z)/2; beta=-(1+z)/2; gamma=(z+1)/(2*zeta); delta=I*(1-z)/(2*zeta)
expected=[s.Matrix([[alpha,beta],[beta,alpha]])*s.diag(B4[0],B4[2]),s.Matrix([[gamma,delta],[delta,-gamma]])*s.diag(B4[0],B4[2]),s.Matrix([[beta,alpha],[alpha,beta]])*s.diag(B4[1],B4[3]),s.Matrix([[delta,-gamma],[-gamma,-delta]])*s.diag(B4[1],B4[3])]
checks['four_sector_formulas']=all(s.simplify(v)==0 for j,E in enumerate(expected) for v in blocks[2*j:2*j+2,2*j:2*j+2]-E)
h=s.symbols('h',real=True)
traces=[1-(z+1/z)/2,(1+(z+1/z)/2)/zeta,(1+(z+1/z)/2)/zeta,1-(z+1/z)/2]
dets=[1,-I,-I,1]
checks['four_block_traces']=all(s.simplify(E.trace()-traces[j])==0 for j,E in enumerate(expected))
checks['four_block_determinants']=all(s.simplify(E.det()-dets[j])==0 for j,E in enumerate(expected))
hstar=s.sqrt(rt-1); c=(1-hstar)/2; d=(1+hstar)/2
# This exact identity, with positive quantities and theta,beta in (0,pi/2),
# proves theta-beta=pi/4 from cos(theta)=c and cos(beta)=d.
checks['positive_angle_match']=s.simplify((rt*d-c)**2-(1-c*c))==0
checks['quadratic_root_identity']=s.simplify((4+2*rt)*c*(1-c)-1)==0
checks['h_between_zero_and_one']=bool(hstar>0) and bool(hstar<1)
checks['c_between_zero_and_half']=bool(c>0) and bool(c<s.Rational(1,2))
checks['angle_match_positive_branch']=bool(rt*d-c>0)
# Check P^2=A and Q^2=B using formal square-root w^2=z and rho^2=zeta.
rho=(s.sqrt(2+rt)+I*s.sqrt(2-rt))/2
checks['rho_square_is_zeta']=s.simplify(rho**2-zeta)==0
w=s.symbols('w',positive=True) # Polynomial/rational identities then extend to all nonzero complex w.
P4=[-I*w,w/rho,1,1/rho];Q4=[1,rho**3/w,I/w,rho**3]
checks['P_square_is_A']=all(s.simplify(s.expand_complex(p*p-a.subs(z,w*w)))==0 for p,a in zip(P4,A4))
checks['Q_square_is_B']=all(s.simplify(s.expand_complex(q*q-b.subs(z,w*w)))==0 for q,b in zip(Q4,B4))
# Algebraic objective claimed for exact witness.
D=s.sqrt(1+hstar)/2
checks['objective_half_angle']=s.simplify(D*D-(1-c)/2)==0
assert all(checks.values()), checks
out={'status':'PASS','checks':checks,'claim':'Explicit legal witness only; no global optimum claim','upper_bound_exact':'sqrt(1+sqrt(sqrt(2)-1))/2','upper_bound_decimal':str(s.N(D,40)),'previous_upper_bound':'1/sqrt(2)','wall_seconds':time.time()-started}
print(json.dumps(out,indent=2))
open('/workspace/shared/phase_rankzero_exact_20261019_1220/EXACT_UPPER_RESULTS.json','w').write(json.dumps(out,indent=2)+'\n')
