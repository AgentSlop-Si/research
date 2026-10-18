"""Fresh, bounded exact checks of the comparison identities only.
No archived or predecessor code is executed or imported.
No certificate replay, range extension, or new squarefreeness claim.
"""
import json
from pathlib import Path
import sympy as s

q=s.Symbol('q')
records=[]
for N in [3,5,7,9,11,13]:
    m=(N-1)//2
    h=m+1
    phi=s.Poly(s.cyclotomic_poly(N,q),q,domain=s.QQ)
    def red(x):
        return s.rem(s.Poly(s.expand(x),q,domain=s.QQ),phi).as_expr()
    def zero(x):
        return red(x)==0
    # Fresh Pascal construction of Gaussian coefficients; no saved data read.
    G=[s.Integer(1)]
    for n in range(1,m+1):
        G=[red((G[j] if j<len(G) else 0)+(q**(n-j)*G[j-1] if j else 0)) for j in range(n+1)]
    D=[red((-1)**j*G[j]) for j in range(m+1)]
    T=list(reversed(D))
    f=[red(q**((h*k*k)%N)) for k in range(2*m+2)]
    assert all(zero(f[k]-q**((h*k+k*(k-1)//2)%N)) for k in range(2*m+2))
    def conv(a,b,n):
        return [red(sum(a[j]*b[k-j] for j in range(max(0,k-len(b)+1),min(k,len(a)-1)+1))) for k in range(n)]
    DU=conv(D,f[1:],2*m)
    DF=conv(D,f,2*m+1)
    A=DU[:m]
    B=DF[:m+1]
    assert all(x==0 for x in DU[m:])
    assert all(x==0 for x in DF[m+1:])
    assert all(zero(B[j]-D[j]-(A[j-1] if j else 0)) for j in range(m+1))
    R=[red(sum(T[j+1+l]*f[l+1] for l in range(m-j))) for j in range(m)]
    assert A==list(reversed(R))
    delta=red((-1)**m*B[m])
    product=red((-1)**m*q**((-m*(m+1)//2)%N)*s.prod(1-q**j for j in range(1,m+1)))
    assert zero(delta-product)
    assert zero(delta-(1+(-1)**m*R[0]))
    # Direct LS substitutions at the two Padé table positions.
    ls_full=[red(G[j]*(-q**(m+h))**j) for j in range(m+1)]
    ls_shift=[red(G[j]*(-q**(m-1+h+1))**j) for j in range(m+1)]
    assert D==ls_full==ls_shift
    records.append({'N':N,'m':m,'cyclotomic_degree':phi.degree(),
        'identity_checks':['chirp_scaling','two_LS_denominators','shifted_Pade_equations',
          'full_Pade_equations','numerator_relation','reciprocal_residue_numerator',
          'forced_diagonal_product','forced_diagonal_residue_sign'],
        'status':'PASS'})
out={'purpose':'bounded exact normalization controls, not finite certificate replay',
     'arithmetic':'QQ[q]/Phi_N(q), exact SymPy polynomial remainders',
     'historical_code_executed':False,'accepted_certificates_replayed':False,
     'records':records,'status':'PASS'}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
