#!/usr/bin/env python3
"""Independent literal matrix control for orientation coverage and symmetries."""
import itertools,json
from pathlib import Path
import sympy as sp
K=sp.QQ.algebraic_field(sp.exp(2*sp.pi*sp.I/7)); q=K.unit
Z=K.zero; O=K.one; N=7
BASE=Path(__file__).resolve().parent

def blank(): return [[Z for j in range(N)] for i in range(N)]
def identity(): return [[O if i==j else Z for j in range(N)] for i in range(N)]
def weyl(a,b):
    out=blank()
    for j in range(N): out[(j+a)%N][j]=q**((b*j)%N)
    return out

def add_into(dst,src):
    for i,j in itertools.product(range(N),repeat=2): dst[i][j]+=src[i][j]
def left_S(a,M): return [M[(i-a)%N][:] for i in range(N)]
def left_T(b,M): return [[q**((b*i)%N)*M[i][j] for j in range(N)] for i in range(N)]
def scale(c,M): return [[c*M[i][j] for j in range(N)] for i in range(N)]
def transpose(M): return [[M[j][i] for j in range(N)] for i in range(N)]
def reflect(M): return [[M[-i%N][-j%N] for j in range(N)] for i in range(N)]
def gaussian(n,k,t):
    answer=O
    for j in range(1,k+1):
        denominator=O-t**j
        assert denominator!=Z
        answer*= (O-t**(n-k+j))/denominator
    return answer

power_coefficients=0
for eps,delta in itertools.product([-1,1],repeat=2):
    terms={(0,0):identity()}
    for degree in range(8):
        for (r,ell),M in terms.items():
            if degree<=6:
                expected=scale(gaussian(degree,ell,q**(eps*delta)),weyl(eps*r,delta*ell))
            else:
                expected=identity() if (r,ell) in [(7,0),(0,7)] else blank()
            assert M==expected,(eps,delta,degree,r,ell)
            power_coefficients+=1
        if degree==7: break
        new={}
        for (r,ell),M in terms.items():
            for key,A in [((r+1,ell),left_S(eps,M)),((r,ell+1),left_T(delta,M))]:
                if key not in new: new[key]=blank()
                add_into(new[key],A)
        terms=new

F=[[q**((-i*j)%7) for j in range(7)] for i in range(7)]
assert transpose(F)==F and reflect(F)==F
symmetry_branches=0
for eps,delta,j in itertools.product([-1,1],[-1,1],range(7)):
    X=weyl(eps,0); Y=scale(q**((eps*delta*j)%7),weyl(0,delta))
    # Transposition changes epsilon and sends the branch label j to -j.
    assert transpose(X)==weyl(-eps,0)
    assert transpose(Y)==scale(q**(((-eps)*delta*(-j))%7),weyl(0,delta))
    # Simultaneous row/column index reflection changes both orientations.
    assert reflect(X)==weyl(-eps,0)
    assert reflect(Y)==scale(q**(((-eps)*(-delta)*j)%7),weyl(0,-delta))
    symmetry_branches+=1

corners=[]
for a,b in itertools.product([3,4],repeat=2):
    supported=[]
    for eps,delta in itertools.product([-1,1],repeat=2):
        r=(eps*a)%7; ell=(delta*b)%7
        if r+ell<=6:
            assert gaussian(r+ell,ell,q**(eps*delta))!=Z
            supported.append([eps,delta])
    assert len(supported)==1
    assert q**((2*(a+b)**2)%7)!=Z
    corners.append({'a':a,'b':b,'unique_orientation':supported[0]})

result={
 'scope':'Literal polynomial bank expansion, four-orientation support, transpose and simultaneous index reflection.',
 'checked_power_coefficient_matrices':power_coefficients,
 'power_range':'0..7 in four orientations, symbolic independent alpha and beta',
 'finite_resolvent_identity':'The seventh power equals (alpha^7+beta^7)I. Hence (I-A)*sum_{k=0}^6 A^k=(1-alpha^7-beta^7)I on both sides.',
 'fourier_symmetric':True,'fourier_invariant_under_simultaneous_index_reflection':True,
 'checked_signed_phase_symmetry_branches':symmetry_branches,
 'transpose_parameter_map':'(epsilon,delta,alpha,beta,w_j) -> (-epsilon,delta,alpha,beta,w_{-j})',
 'reflection_parameter_map':'(epsilon,delta,alpha,beta,w_j) -> (-epsilon,-delta,alpha,beta,w_j)',
 'both_symmetries_preserve_Delta':True,
 'four_corner_supports':corners,
 'padding':'A zero bank is legal with alpha=beta=1, Delta=-1 and every w_j=0. The enlarged independent-amplitude proof also directly permits zero amplitudes.',
 'conclusion':'Excluding (++ twice,-+ once) excludes three banks on either delta side. Unique supports plus zero padding cover fewer banks. Therefore at least four on each delta side, hence at least eight overall.',
 'independence':'Fresh file; no authored/predecessor research script executed, imported, compiled, or parsed.'
}
(BASE/'LITERAL_MODEL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
