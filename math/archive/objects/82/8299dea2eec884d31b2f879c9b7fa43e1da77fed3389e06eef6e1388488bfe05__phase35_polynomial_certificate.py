"""Characteristic-zero certificate for Phase 35 single-coupling Green pencils.

For A(alpha)=(I-alpha W0)^-1+(I-alpha W1)^-1, build the polynomial
C(alpha)=sum_{k=0}^{N-1} alpha^k (W0^k+W1^k). A=C/(1-alpha^N).
If F = A D P B for ANY invertible regular B and invertible monomial DP,
then N*C[0,j]*cofactor(C,0,j) - det(C) = 0 for every j.

We evaluate over p=2^127-1, interpolate all coefficients modulo p, then
reconstruct over Z with a *proved absolute coefficient bound* strictly below
p/2. GCDs are subsequently computed over characteristic ZERO, not modulo p.
"""
import argparse
import json
from math import factorial
from pathlib import Path
import sympy as sp
from phase33_two_sided import make_cycles
from phase34_products import permutation_successor, permutation_rank_difference

P=(1<<127)-1  # proved Mersenne prime
X=sp.Symbol('a')


def determinant_mod(a,p=P):
    n=len(a); b=[row[:] for row in a]; out=1
    for k in range(n):
        pivot=next((r for r in range(k,n) if b[r][k]),None)
        if pivot is None:return 0
        if pivot!=k:b[pivot],b[k]=b[k],b[pivot];out=-out
        d=b[k][k];out=out*d%p; invd=pow(d,p-2,p)
        for i in range(k+1,n):
            z=b[i][k]*invd%p
            if z:
                b[i][k]=0
                for j in range(k+1,n): b[i][j]=(b[i][j]-z*b[k][j])%p
    return out%p


def interpolate_integer(values, coeff_bound,p=P):
    """Lagrange via forward differences, with *exact* integer lifting."""
    n=len(values)-1
    assert p>2*coeff_bound
    diff=values[:]; deltas=[]
    for k in range(n+1):
        deltas.append(diff[0]);diff=[(diff[i+1]-diff[i])%p for i in range(len(diff)-1)]
    coef=[0]*(n+1);fall=[1];invfac=1
    for k in range(n+1):
        a=deltas[k]*invfac%p
        for j,v in enumerate(fall):coef[j]=(coef[j]+a*v)%p
        nxt=[0]*(len(fall)+1)
        for j,v in enumerate(fall):
            nxt[j]=(nxt[j]-k*v)%p
            nxt[j+1]=(nxt[j+1]+v)%p
        fall=nxt
        if k<n:invfac=invfac*pow(k+1,p-2,p)%p
    lifted=[v if v<=p//2 else v-p for v in coef]
    assert all(abs(v)<=coeff_bound for v in lifted)
    return sp.Poly.from_list(lifted[::-1],gens=X,domain=sp.ZZ)


def integer_determinant(a):
    """Independent integer matrix determinant, for validation (Bareiss)."""
    n=len(a);b=[[int(v) for v in row] for row in a];den=1;sign=1
    for k in range(n-1):
        if b[k][k]==0:
            s=next((i for i in range(k+1,n) if b[i][k]),None)
            if s is None:return 0
            b[k],b[s]=b[s],b[k];sign=-sign
        pivot=b[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numer=b[i][j]*pivot-b[i][k]*b[k][j]
                assert numer%den==0
                b[i][j]=numer//den
            b[i][k]=0
        den=pivot
    return sign*b[-1][-1]


def eval_poly_matrix(ex1,ex2,z):
    n=len(ex1);powers=[1]
    for _ in range(1,n):powers.append(powers[-1]*z)
    return [[powers[ex1[i][j]]+powers[ex2[i][j]] for j in range(n)] for i in range(n)]


def make_distance_arrays(cycles):
    n=len(cycles[0]);pos=[]
    for cyc in cycles:pos.append({j:i for i,j in enumerate(cyc)})
    return [[[ (pos[s][i]-pos[s][j])%n for j in range(n)]
             for i in range(n)] for s in range(2)]


def certificate(n, seed=35123, include_coefficients=False):
    cycles=make_cycles(n,2,seed)
    ex1,ex2=make_distance_arrays(cycles)
    rank_delta,cycles_count=permutation_rank_difference(
        permutation_successor(cycles[0]),permutation_successor(cycles[1]))
    # Each determinant monomial has degree <= n*(n-1), and polynomial L1 norm
    # <= n! * 2**n. The numerator is difference of two such terms.
    B=2*factorial(n)*2**n
    assert 2*B<P
    D=n*(n-1)
    ys=[[],[],[]]
    for z in range(D+1):
        powers=[1]
        for _ in range(1,n):powers.append(powers[-1]*z%P)
        c=[[(powers[ex1[i][j]]+powers[ex2[i][j]])%P for j in range(n)]
           for i in range(n)]
        det=determinant_mod(c)
        h=[]
        for j in (0,1):
            minor=[[c[i][k] for k in range(n) if k!=j] for i in range(1,n)]
            cof=determinant_mod(minor)*(-1 if j%2 else 1)%P
            h.append((n*c[0][j]*cof-det)%P)
        for dst,val in zip(ys,h+[det]):dst.append(val)
    h0,h1,det= [interpolate_integer(v,B) for v in ys]
    for z in [2,3]:
        c=eval_poly_matrix(ex1,ex2,z)
        det_exact=integer_determinant(c)
        assert det.eval(z)==det_exact
        for j,h in ((0,h0),(1,h1)):
            minor=[[c[i][k] for k in range(n) if k!=j] for i in range(1,n)]
            cof=integer_determinant(minor)*(-1 if j%2 else 1)
            assert h.eval(z)==n*c[0][j]*cof-det_exact
    gcd=h0.gcd(h1)
    quotient=det.exquo(gcd) if det.rem(gcd).is_zero else None
    excludes=quotient is not None
    data={
        'N':n,'seed':seed,'primes_for_exact_coefficient_lifting':[str(P)],
        'rigorous_abs_coeff_bound':str(B),'interpolation_degree_upper':D,
        'char_zero_degrees':{'H0':h0.degree(),'H1':h1.degree(),'det_C':det.degree(),
                             'gcd':gcd.degree()},
        'gcd_divides_det_in_Z':excludes,
        'rank_difference_between_cycles':rank_delta,
        'cycle_count_of_relative_permutation':cycles_count,
        'nonaffine_cycles':cycles,
        'checked_integer_evaluations':[2,3],
        'all_complex_admissible_couplings_excluded':excludes,
    }
    if include_coefficients:
        data['integer_coefficient_arrays_ascending']={
            'H0':list(map(int,reversed(h0.all_coeffs()))),
            'H1':list(map(int,reversed(h1.all_coeffs()))),
            'det_C':list(map(int,reversed(det.all_coeffs()))),
            'gcd':list(map(int,reversed(gcd.all_coeffs())))}
    return data


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',default='polynomial_audit.json')
    ap.add_argument('--full-coefficients',action='store_true')
    args=ap.parse_args()
    out={'phase':35,'certificates':[certificate(n,include_coefficients=args.full_coefficients)
                                   for n in (8,16)]}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    for a in out['certificates']:
        print('N={N}: rank distance={rank_difference_between_cycles}, degree(H0,H1,det,gcd)={char_zero_degrees}, gcd divides det? {gcd_divides_det_in_Z}'.format(**a))
    print('saved',args.output)
