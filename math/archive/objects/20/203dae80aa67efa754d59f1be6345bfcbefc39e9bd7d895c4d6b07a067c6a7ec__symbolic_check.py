"""Independent exact symbolic sanity check in characteristic zero (SymPy)."""
from __future__ import annotations
from sympy import symbols, I, Matrix, simplify


def audit():
    n=4
    x=symbols('x0:4')
    omega=I
    F=Matrix([[omega**(i*j) for j in range(n)] for i in range(n)])
    original=Matrix(x)
    cases={
        'nonlinear-polynomial-k':(x[0]+x[1])**2+7*x[0],
        'rational-k':(x[0]*x[1]+x[0])/(1+x[3]**2),
        'branch-positive-k':x[0]**2,
        'branch-negative-k':x[1]**2,
    }
    results={}
    for name,k in cases.items():
        e=Matrix([0,1,0,0])
        ys=F*(original-k*e)+k*(F*e)
        difference=[simplify(y-t) for y,t in zip(ys,F*original)]
        jac=ys.jacobian(x)
        jac_difference=[simplify(jac[i,j]-F[i,j]) for i in range(n) for j in range(n)]
        if any(v!=0 for v in difference+jac_difference):raise AssertionError(name)
        results[name]={'zero_output_residuals':len(difference),'zero_jacobian_residuals':len(jac_difference)}
    return results

if __name__=='__main__':
    for k,v in audit().items(): print(k,v)
