# Fresh direct companion invocation; runs only this packet's new checker.
import exact_local_checker as e
import sympy as s
G=[]
for _,_,A in e.firstp:
 row=[]
 for _,_,B in e.firstp:
  x=e.frob(A,B)/(e.s*e.c)**2
  row.append(s.simplify(s.expand_complex(e.K.to_sympy(x))))
 G.append(row)
M=s.Matrix(G)
print('GRAM/(sc)^2',M)
print('DETERMINANT',s.factor(M.det()))
print('EIGENVALUES',M.eigenvals())
