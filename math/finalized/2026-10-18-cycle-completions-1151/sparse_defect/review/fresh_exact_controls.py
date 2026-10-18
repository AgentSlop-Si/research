#!/usr/bin/env python3
"""Independent review controls. Original candidate code is not imported or run.

Fourier entries are encoded as exponent/coefficient pairs. Integer polynomial
coefficient arrays are reduced by monic cyclotomic polynomials. SymPy supplies
only the cyclotomic polynomial and separate N=3 radical algebra.
"""
from pathlib import Path
from itertools import permutations
from functools import lru_cache
import hashlib
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'candidate'
X=sp.Symbol('X')

@lru_cache(None)
def phi(n):
    return tuple(reversed([int(c) for c in sp.Poly(sp.cyclotomic_poly(n,X),X).all_coeffs()]))

def reduce_coefficients(coeff,n):
    """Independent schoolbook polynomial remainder, ascending coefficient order."""
    a=list(coeff)
    f=phi(n); degree=len(f)-1
    for j in range(len(a)-1,degree-1,-1):
        c=a[j]
        if c:
            for k in range(degree+1):
                a[j-degree+k]-=c*f[k]
    return tuple(a[:degree])

@lru_cache(None)
def reduce_counts(coeff,n):
    return reduce_coefficients(coeff,n)

def is_scalar_gram(entries,n,scalar,columns=False):
    """entries are None or (integer coefficient, exponent modulo n)."""
    d=len(phi(n))-1
    for i in range(n):
        for j in range(n):
            terms=[0]*n
            for k in range(n):
                u,v=(entries[k][i],entries[k][j]) if columns else (entries[i][k],entries[j][k])
                if u is not None and v is not None:
                    c,e=u; f,g=v
                    terms[((g-e) if columns else (e-g))%n]+=c*f
            expected=(scalar if i==j else 0,)+(0,)*(d-1)
            if reduce_counts(tuple(terms),n)!=expected:
                return False
    return True

def matrices(n):
    if not isinstance(n,int) or n<2 or n%2:
        raise ValueError('even N >= 2 required')
    m=n//2
    h=[]; r=[]
    for i in range(n):
        hr=[]; rr=[]
        for j in range(n):
            keep=(i//m)==(j%2)
            hr.append((1,(i*j)%n) if keep else None)
            rr.append(None if keep else (1,(i*j)%n))
        h.append(hr); r.append(rr)
    return h,r

def half_density():
    results=[]
    for n in list(range(2,41,2))+[42,50,64]:
        h,r=matrices(n); m=n//2
        # H/sqrt(N)=M; inverse is sqrt(N)/m H*. Both Gram orders
        # directly verify both inverse products, without numerical inversion.
        checks={
            'H_Hstar_equals_mI':is_scalar_gram(h,n,m),
            'Hstar_H_equals_mI':is_scalar_gram(h,n,m,True),
            'R_Rstar_equals_mI':is_scalar_gram(r,n,m),
            'Rstar_R_equals_mI':is_scalar_gram(r,n,m,True),
            'every_inverse_row_support_m':all(sum(h[i][j] is not None for i in range(n))==m for j in range(n)),
            'every_inverse_column_support_m':all(sum(t is not None for t in row)==m for row in h),
            'complement_equals_F':all((h[i][j] or r[i][j])==(1,i*j%n) and ((h[i][j] is None)!=(r[i][j] is None)) for i in range(n) for j in range(n)),
        }
        assert all(checks.values()),(n,checks)
        results.append({'N':n,'checks':checks})
    return results

def singleton_phase():
    results=[]
    for n in range(2,10):
        accepted=[]; count=0
        for p in permutations(range(n)):
            count+=1
            if n%2==0 and all(((i-j)*(p[i]-p[j])-n//2)%n==0 for i in range(n) for j in range(i)):
                accepted.append(p)
        assert len(accepted)==(2 if n==2 else 0)
        results.append({'N':n,'permutations_checked':count,'possible_equalizers':len(accepted)})
    # Independent constant-size obstruction used in the proof: every pair
    # of neighboring row indices forces the same N/2 image increment.
    pair_obstruction=[]
    for n in range(4,202,2):
        residues=[d for d in range(n) if (-d-n//2)%n==0]
        assert residues==[n//2]
        assert (2*residues[0])%n==0
        pair_obstruction.append(n)
    return {'exhaustive':results,'neighbor_obstruction_even_N':pair_obstruction}

def zmat(m):
    return all(sp.simplify(x)==0 for x in m)

def exact_three():
    q=sp.sqrt(3); w=(-1-sp.I*q)/2
    F=sp.Matrix(3,3,lambda i,j:sp.expand(w**(i*j))/q)
    D=sp.diag(1,w,w)
    C=sp.simplify(D*F*D)
    assert zmat(C-((1-w)*sp.eye(3)+w*sp.ones(3))/q)
    eig0=-sp.I; eig1=q/2+sp.I/2; midpoint=(eig0+eig1)/2
    assert sp.simplify(abs(eig0-eig1)**2)==3
    assert sp.simplify(abs(midpoint)**2)==sp.Rational(1,4)
    # Verify group averaging on a fully symbolic diagonal, not merely witnesses.
    t=sp.symbols('t0:3'); T=sp.diag(*t); twirl=sp.zeros(3)
    for p in permutations(range(3)):
        Q=sp.zeros(3)
        for j in range(3): Q[p[j],j]=1
        assert zmat(Q*C*Q.T-C)
        twirl+=Q*T*Q.T/6
    assert zmat(twirl-sum(t)*sp.eye(3)/3)
    supports=[]
    for a in (1,2):
        for b in range(3):
            p=tuple((a*j+b)%3 for j in range(3))
            Q=sp.zeros(3)
            for j in range(3): Q[p[j],j]=1
            L=sp.diag(*(sp.expand(w**(b*i)) for i in range(3)))
            Fa=F if a==1 else sp.conjugate(F)
            Ta=midpoint*D if a==1 else sp.conjugate(midpoint*D)
            assert zmat(F*Q-L*Fa)
            M=sp.simplify(L*Ta*Q.T)
            E=sp.simplify(F-M)
            assert zmat(E*sp.conjugate(E).T-sp.Rational(3,4)*sp.eye(3))
            assert zmat(M*sp.conjugate(M).T-sp.Rational(1,4)*sp.eye(3))
            inverse=sp.simplify(4*sp.conjugate(M).T)
            assert zmat(M*inverse-sp.eye(3)) and zmat(inverse*M-sp.eye(3))
            assert all(sum(sp.simplify(inverse[i,j])!=0 for j in range(3))==1 for i in range(3))
            supports.append(p)
    assert len(set(supports))==6
    return {'symbolic_twirl':True,'two_eigenvalue_radius_squared':'3/4','witness_absolute_scale_squared':'1/4','all_six_supports_exact_witnesses':supports,'inverse_products_and_every_inverse_row':True}

def negatives():
    invalid=[]
    for n in (0,1,3,5,7):
        try: matrices(n)
        except ValueError: invalid.append(n)
    assert invalid==[0,1,3,5,7]
    h,_=matrices(6)
    damaged=[row[:] for row in h]; damaged[0][0]=(2,0)
    assert not is_scalar_gram(damaged,6,3)
    repeated=[[(1,i*j%6) if j%2==0 else None for j in range(6)] for i in range(6)]
    assert not is_scalar_gram(repeated,6,3)
    # Gain control: scaling retained M by 2 still has sparse inverse and
    # condition number 1, but cannot use the claimed I/2 Gram certificate.
    scaled=[[(2,v[1]) if v is not None else None for v in row] for row in h]
    assert not is_scalar_gram(scaled,6,3)
    assert is_scalar_gram(scaled,6,12)
    # N=4 support identity has the correct per-row norm, but it is not
    # operator-norm equality: the missing diagonal residual Gram is not 3I.
    offdiag=[[(1,i*j%4) if i!=j else None for j in range(4)] for i in range(4)]
    assert not is_scalar_gram(offdiag,4,3)
    return {'odd_or_invalid_lengths_rejected':invalid,'one_entry_corruption_rejected':True,'singular_repeated_columns_rejected':True,'gain_change_rejected':True,'row_norm_only_false_positive_rejected':True}

def bindings():
    mbytes=(SOURCE/'MANIFEST.json').read_bytes(); manifest=json.loads(mbytes)
    checks=[]
    for e in manifest['files']:
        data=(SOURCE/e['path']).read_bytes()
        assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'],e['path']
        checks.append(e)
    src=(SOURCE/'sources/PHASE20_AUDIT.md').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()
    receipt=json.loads((SOURCE/'sources/PHASE20_RECEIPT.json').read_text())
    assert blob==receipt['sha']
    initial=json.loads((ROOT/'INPUT_MANIFEST_CHECK.json').read_text())
    digest=hashlib.sha256(mbytes).hexdigest()
    assert initial['manifest_sha256']==digest,'candidate manifest changed during review'
    return {'manifest_sha256':digest,'manifest_file_count':len(checks),'source_git_blob_verified':blob,'all_manifest_members_match':True,'manifest_unchanged_since_inspection':True}

if __name__=='__main__':
    result={'candidate_bindings':bindings(),'half_density':half_density(),'singleton':singleton_phase(),'exact_N3':exact_three(),'negative_controls':negatives()}
    result['candidate_bindings_final']=bindings()
    result['all_passed']=True
    result['control_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT/'FRESH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_passed':True,'even_dimensions':[v['N'] for v in result['half_density']],'singleton_permutations':sum(v['permutations_checked'] for v in result['singleton']['exhaustive']),'N3_supports':6,'candidate_manifest_sha256':result['candidate_bindings']['manifest_sha256']}))
