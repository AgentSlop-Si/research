"""Independent exact characteristic-zero cyclotomic proof for 3,4,5 codelets.

Verifies A_i diag(d_i) B_i = F_i modulo Φ_i(ζ), using rational polynomial
coefficients. Tensor/CRT identities then give F_60 algebraically.
"""
import sympy as sp

def codelet_matrices(n,z):
    if n==3:
        B=sp.Matrix([[1,1,1],[0,1,1],[0,1,-1]])
        A=sp.Matrix([[1,0,0],[1,1,1],[1,1,-1]])
        D=[sp.Integer(1),-sp.Rational(3,2),(z-z**2)/2]
    elif n==4:
        B=sp.Matrix([[1,0,1,0],[0,1,0,1],[1,0,-1,0],[0,1,0,-1]])
        A=sp.Matrix([[1,1,0,0],[0,0,1,1],[1,-1,0,0],[0,0,1,-1]])
        D=[sp.Integer(1),sp.Integer(1),sp.Integer(1),z]
    elif n==5:
        B=sp.Matrix([
            [1,1,1,1,1],
            [0,1,1,1,1],
            [0,1,-1,-1,1],
            [0,1,1,-1,-1],
            [0,0,1,-1,0],
            [0,1,0,0,-1],
        ])
        A=sp.Matrix([
            [1,0,0,0,0,0],
            [1,1,1,1,1,0],
            [1,1,-1,-1,0,1],
            [1,1,-1,1,0,-1],
            [1,1,1,-1,-1,0],
        ])
        c1=(z+z**4)/2;c2=(z**2+z**3)/2
        h1=(z-z**4)/2;h2=(z**2-z**3)/2
        ca=(c1+c2)/2;cd=(c1-c2)/2
        D=[sp.Integer(1),ca-1,cd,h1,h2-h1,h1+h2]
    else:raise ValueError('n must be 3,4,5')
    return A,D,B

def run():
    z=sp.Symbol('z');counts={}
    for n in (3,4,5):
        A,D,B=codelet_matrices(n,z)
        lhs=A*sp.diag(*D)*B
        cyclo=sp.Poly(sp.cyclotomic_poly(n,z),z,domain=sp.QQ)
        for j in range(n):
            for k in range(n):
                poly=sp.Poly(sp.expand(lhs[j,k]-z**(j*k)),z,domain=sp.QQ)
                rem=poly.rem(cyclo)
                assert rem.is_zero, (n,j,k,rem)
        counts[n]={'basis_entries':n*n,'pre_shape':list(B.shape),'post_shape':list(A.shape),
                   'diagonal_width':len(D),'cyclotomic_polynomial':str(cyclo.as_expr())}
    # The complete 60-point diagonal lives in Q[z]/Φ60(z). Certify exactly
    # which of its 72 entries are identically 1 (not a floating-point test).
    D3=codelet_matrices(3,z**20)[1]
    D4=codelet_matrices(4,z**15)[1]
    D5=codelet_matrices(5,z**12)[1]
    phi=sp.Poly(sp.cyclotomic_poly(60,z),z,domain=sp.QQ)
    identities=0
    for a in D3:
        for b in D4:
            for c in D5:
                v=sp.Poly(sp.expand(a*b*c-1),z,domain=sp.QQ).rem(phi)
                if v.is_zero:identities+=1
    assert identities==3,identities
    counts['60_diagonal']={'width':72,'identity_coefficients':identities,
                           'nonidentity_multiplications':72-identities,
                           'proof':'exact polynomial remainder modulo Φ60'}
    return counts

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
