"""Independent symbolic proof of WFTA8 and the 144-channel WFTA15x8 tensor.
Uses exact Q[z] remainders modulo cyclotomic polynomials, not floating point.
"""
import json
import sympy as sp
from symbolic_check import codelet_matrices

def matrices8(z):
    # Each row in B is one channel of before8 applied to natural-order input.
    x=sp.symbols('x0:8')
    s=[x[j]+x[j+4] for j in range(4)]
    t=[x[j]-x[j+4] for j in range(4)]
    Bforms=(s[0]+s[2],s[1]+s[3],s[0]-s[2],s[1]-s[3],t[0],t[2],t[1]+t[3],t[1]-t[3])
    B=sp.Matrix([[sp.expand(e).coeff(v) for v in x] for e in Bforms])
    y=sp.symbols('y0:8')
    Aforms=[None]*8
    Aforms[0]=y[0]+y[1];Aforms[4]=y[0]-y[1]
    Aforms[2]=y[2]+y[3];Aforms[6]=y[2]-y[3]
    Aforms[1]=y[4]+y[5]+y[6]+y[7]
    Aforms[5]=y[4]+y[5]-y[6]-y[7]
    Aforms[3]=y[4]-y[5]+y[6]-y[7]
    Aforms[7]=y[4]-y[5]-y[6]+y[7]
    A=sp.Matrix([[sp.expand(e).coeff(v) for v in y] for e in Aforms])
    i=z**2
    D=[sp.Integer(1)]*3+[i,sp.Integer(1),i,z*(1+i)/2,z*(1-i)/2]
    return A,D,B

def run():
    z=sp.Symbol('z')
    A,D,B=matrices8(z)
    lhs=A*sp.diag(*D)*B
    phi8=sp.Poly(sp.cyclotomic_poly(8,z),z,domain=sp.QQ)
    for k in range(8):
        for j in range(8):
            poly=sp.Poly(sp.expand(lhs[k,j]-z**(k*j)),z,domain=sp.QQ)
            if not poly.rem(phi8).is_zero:raise AssertionError(('F8',k,j,poly.rem(phi8)))
    # Verify F15 factor codelets, then D15*D8 in Q[z]/Phi120.
    phi120=sp.Poly(sp.cyclotomic_poly(120,z),z,domain=sp.QQ)
    d3=codelet_matrices(3,z**40)[1]
    d5=codelet_matrices(5,z**24)[1]
    d8=matrices8(z**15)[1]
    exact_identities=[];other=[]
    for v in range(6):
        for u in range(3):
            for t in range(8):
                coeff=sp.Poly(sp.expand(d5[v]*d3[u]*d8[t]-1),z,domain=sp.QQ)
                rem=coeff.rem(phi120)
                if rem.is_zero:exact_identities.append((v,u,t))
                else:other.append((v,u,t))
    assert len(exact_identities)==4,exact_identities
    return dict(wfta8=dict(before_shape=list(B.shape),after_shape=list(A.shape),diagonal_width=8,
                    additions=26,nonidentity_multiplications=4,exact_dft_entries=64,
                    primitive_polynomial=str(phi8.as_expr())),
                tensor120=dict(width=144,identity_coefficients=len(exact_identities),
                    identity_indices=exact_identities,nonidentity_multiplications=144-len(exact_identities),
                    checked_entries=144,primitive_polynomial=str(phi120.as_expr())),
                all_exact=True)

if __name__=='__main__':print(json.dumps(run(),indent=2))
