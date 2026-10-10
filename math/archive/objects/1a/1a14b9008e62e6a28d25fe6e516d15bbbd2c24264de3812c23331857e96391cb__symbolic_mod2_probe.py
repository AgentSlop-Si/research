import sympy as s, time,json,pathlib
q,z,u=s.symbols('q z u')
H=[s.Poly(1,z),s.Poly(1+z,z)]
results=[]
for n in range(2,15):
 H.append(s.Poly((1+z)*H[-1].as_expr()+(q**(n-1)-1)*z*H[-2].as_expr(),z))
 if n%2:continue
 r=n//2; C=[s.Poly(2,u),s.Poly(u,u)]
 for j in range(2,r+1):C.append(s.Poly(u*C[-1].as_expr()-C[-2].as_expr(),u))
 P=s.Poly(H[n].nth(r),u)
 for j in range(1,r+1):P+=H[n].nth(r+j)*C[j]
 P2=s.Poly(P.as_expr(),u,domain=s.GF(2).poly_ring(q))
 # Compute ordinary resultant over GF(2)[q] with no cyclotomic quotient.
 disc=P2.discriminant()
 fac=s.factor(s.Poly(disc,q,modulus=2).as_expr(),modulus=2)
 cen=s.factor(H[n].nth(r),modulus=2)
 obj={'n':n,'contracted_discriminant_mod2':str(fac),'center_mod2':str(cen)}
 print(obj,flush=True);results.append(obj)
pathlib.Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2))
