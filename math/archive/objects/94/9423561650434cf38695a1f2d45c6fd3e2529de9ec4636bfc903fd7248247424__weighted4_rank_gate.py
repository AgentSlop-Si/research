"""Exact rank-six necessary width for a fixed-rational pre/diagonal/post representation
of the formal weighted F4(a) = F4 diag(1,a,a^2,a^3).

The theorem applies to A and B with rational entries independent of a,
with arbitrary complex-polynomial/Laurent diagonal coefficient functions.
It does not bound more general circuits or pre/post maps depending on a.
"""
import json
import sympy as s

def run():
    i=s.I
    F4=s.Matrix([[1,1,1,1],[1,i,-1,-i],[1,-1,1,-1],[1,-i,-1,i]])
    coeffs=[]
    for j in range(4):
        for component in ('real','imag'):
            M=s.zeros(4,4)
            for k in range(4):
                z=s.re(F4[k,j]) if component=='real' else s.im(F4[k,j])
                M[k,j]=z
            if M!=s.zeros(4,4):
                coeffs.append((j,component,[M[k,l] for k in range(4) for l in range(4)]))
    rank=s.Matrix([x[2] for x in coeffs]).rank()
    assert len(coeffs)==6 and rank==6
    # Width-six rational A,B witnesses each output coordinate block.
    # Six channel input map x0,x2,x1,x1,x3,x3; scalars 1,a^2,a,ia,a^3,-ia^3.
    a=s.symbols('a')
    B=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,1,0,0],[0,0,0,1],[0,0,0,1]])
    D=s.diag(1,a*a,a,i*a,a**3,-i*a**3)
    # after_weighted4 constructs even/odd sums/differences; columns correspond to six channels.
    A=s.Matrix([[1,1,1,0,1,0],
                [1,-1,0,1,0,1],
                [1,1,-1,0,-1,0],
                [1,-1,0,-1,0,-1]])
    expect=F4*s.diag(1,a,a*a,a**3)
    assert s.simplify(A*D*B-expect)==s.zeros(4,4)
    return dict(rank_of_real_imaginary_coefficient_matrices=rank,
                necessary_diagonal_width_in_fixed_Q_pre_post_model=6,
                explicit_width_six_witness=True,
                proof='Six independent rational coefficient matrices for powers a^0..a^3')

if __name__=='__main__':print(json.dumps(run(),indent=2))
