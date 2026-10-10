"""Independent exact complex-symbolic check of user's x-k rewriting idea."""
from pathlib import Path
import json
import sympy as sp


def run():
    I=sp.I
    x=sp.symbols('x0:4')
    n=4
    omega=sp.exp(-2*sp.pi*I/n)
    f=sp.Matrix([[sp.expand(omega**(j*k)) for j in range(n)] for k in range(n)])
    original=f*sp.Matrix(x)
    # This k depends NONLINEARLY on x; the identity must still hold.
    k=x[0]*x[1]+x[2]**2
    residual=sp.Matrix([x[0]-k,*x[1:]])
    rewritten=f*residual+k*sp.ones(n,1)  # F*e0 = all-ones vector
    symbolic_diff=[sp.expand(z) for z in rewritten-original]
    if any(z!=0 for z in symbolic_diff):
        raise AssertionError(symbolic_diff)
    jac=rewritten.jacobian(x)
    checked=all(sp.simplify(jac[i,j]-f[i,j])==0 for i in range(n) for j in range(n))
    if not checked:
        raise AssertionError('Jacobian differs from Fourier matrix')
    # A rational nonlinear generic branch has the same rational function.
    denominator=1+x[0]*x[1]
    rational=[sp.cancel(v*denominator/denominator) for v in original]
    if any(sp.simplify(a-b) for a,b in zip(rational,original)):
        raise AssertionError('Generic rational branch differs')
    # All facts are identities of functions on C^4 (except the rational
    # representation at points where its denominator vanishes).
    report={'n':4,'field':'C','matrix_entries_exactly_verified':16,
        'nonlinear_k':'x0*x1 + x2^2','polynomial_identity':True,
        'global_jacobian_identity':True,
        'rational_generic_branch_identity':True,
        'note':'Symbolic identities are classical algebra; no speedup is proved.'}
    Path(__file__).with_name('symbolic_complex_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print('EXACT SYMBOLIC COMPLEX AUDIT PASSED')
    print('4x4 Fourier matrix: nonlinear k decomposition and all 16 Jacobian entries verified identically')
    return report

if __name__=='__main__':run()
