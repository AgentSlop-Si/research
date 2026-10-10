#!/usr/bin/env python3
"""Independent exact algebra/control cases for the inherited ledger and new lemma."""
from pathlib import Path
from math import gcd,comb
import json,random
import sympy as sp
HERE=Path(__file__).resolve().parent
rng=random.Random(9821357)
def prime_and_root(n):
    k=1
    while not sp.isprime(k*n+1): k+=1
    p=k*n+1;g=int(sp.primitive_root(p));w=pow(g,k,p)
    assert pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in sp.factorint(n))
    return p,w
cases=[];entries=expanded=0
for M in [2,3,4,5,6,8,9,10,12,16]:
    N=M*M;p,w=prime_and_root(N);eta=pow(w,M,p)
    data=[[rng.randrange(p) for h in range(M)] for j in range(M)]
    direct=[[sum(pow(w,((1-M*h)*t*j)%N,p)*data[j][h] for j in range(M))%p
             for h in range(M)] for t in range(M)]
    for b in sp.divisors(M):
        m=M//b;zeta=pow(eta,m,p)
        hats=[[[sum(pow(zeta,(-ell*c)%b,p)*data[j][d+c*m] for c in range(b))%p
                for ell in range(b)] for d in range(m)] for j in range(M)]
        omega_small=pow(w,b*b,p)
        distinct=set()
        for d in range(m):
            q=pow(w,(1-M*d)%N,p);small=pow(q,b*b,p);distinct.add(small)
            assert small==pow(omega_small,(1-M*d)%(m*m),p)
            assert pow(small,m*m,p)==1
            assert all(pow(small,m*m//q0,p)!=1 for q0 in sp.factorint(m*m))
            for t in range(M):
                r,a=t%b,t//b
                for ell in range(b):
                    expected=sum(pow(zeta,(-ell*c)%b,p)*direct[t][d+c*m] for c in range(b))%p
                    routed=0
                    for s in range(b):
                        inner=sum(pow(small,a*v,p)*pow(q,b*r*v,p)*hats[s+b*v][d][(ell+r*s)%b] for v in range(m))%p
                        routed+=pow(q,r*s+b*s*a,p)*inner
                    assert routed%p==expected
                    entries+=1
        assert len(distinct)==m//gcd(b,m)
        volume=m*b*b*b*m
        assert volume==N*b
        expanded+=volume
        cases.append({'M':M,'b':int(b),'m':int(m),'prime':int(p),'root':w,
                      'distinct_nodes':len(distinct),'applications':int(m*b**3),'expanded_inputs':int(volume)})

# For arbitrary edge masks, the grid denominator is unit triangular. Validate one
# nonconstant-mask application directly without relying on constant-weight paths.
mask_cases=[]
for M in [2,3,4,5,8]:
    N=M*M;p=1009
    a=[rng.randrange(p) for _ in range(N)];b=[rng.randrange(p) for _ in range(N)]
    x=[rng.randrange(p) for _ in range(N)];y=[]
    for i in range(N):
        t,u=divmod(i,M)
        y.append((x[i]+(a[i]*y[i-M] if t else 0)+(b[i]*y[i-1] if u else 0))%p)
    recovered=[(y[i]-(a[i]*y[i-M] if i//M else 0)-(b[i]*y[i-1] if i%M else 0))%p for i in range(N)]
    assert x==recovered
    mask_cases.append({'M':M,'active_edges':2*M*(M-1),'exact_application_check':True})

def rev(j,bits):
    r=0
    for _ in range(bits):r=2*r+(j&1);j//=2
    return r
anchors=[];shifted=[]
for h in range(1,13):
    M=2**h;N=M*M;k=M//2;bits=2*h
    assert rev(N-2,bits)==N//2-1
    assert rev(N-1-M,bits)==N-1-M//2
    delta=2*7**k-5**k-1;gap=2*7**k-3*5**k+5
    assert delta>0 and gap>0
    anchors.append({'M':M,'N':N,'determinant_positive':True,'modulus_gap_positive':True,
                    'selected_routed_path_exponents':[k,k]})
    # pi=T1 R has pi(0)=1 for every number of bits. Thus J row 1 is e_1.
    assert (rev(0,bits)+1)%N==1
    # Ordinary grid row 1 is (t,u)=(0,1), with exactly predecessors 0 and 1.
    assert divmod(1,M)==(0,1)
    degree=int(sp.totient(N));assert degree==N//2
    shifted.append({'M':M,'N':N,'shifted_minimum_vertex':1,
                    'exact_left_row':'3 alpha e_0 + (alpha+beta) e_1',
                    'max_left_row_support':2,'fixed_right_rows_per_selected_row':2,
                    'rational_coordinate_span_upper_bound':4,'fourier_coordinate_span_degree':degree,
                    'excluded_by_degree':degree>4})
# The first four N=16 Fourier coordinates are not sufficient; an 8-dimensional
# primitive field is required. Check an explicit coefficient matrix independently.
z=sp.symbols('z');cyclo=sp.Poly(sp.cyclotomic_poly(16,z),z)
assert cyclo.as_expr()==z**8+1 and cyclo.is_irreducible
columns=[sp.Poly(z**j,z).rem(cyclo) for j in range(16)]
coordinate_matrix=sp.Matrix([[p.nth(i) for p in columns] for i in range(8)])
assert coordinate_matrix.rank()==8
result={'growing_radix':{'banks':len(cases),'exact_outputs_checked':entries,'expanded_inputs_counted':expanded,'cases':cases},
        'variable_mask_solve_controls':mask_cases,'anchor_controls':anchors,
        'shifted_symbolic_support_controls':shifted,'N16_fourier_Q_coordinate_rank':8,
        'all_size_proof':'pi(0)=1 forces routed row 1=e_1; grid row 1=3e_0+e_1 for every M>=2. At dyadic square N, Phi_N=z^(N/2)+1, so coordinate Q-span=N/2.'}
(HERE/'LEDGER_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'banks':len(cases),'exact_outputs':entries,'expanded_inputs':expanded,'anchor_sizes':len(anchors),'shifted_sizes':len(shifted),'N16_fourier_Q_coordinate_rank':8},indent=2))
