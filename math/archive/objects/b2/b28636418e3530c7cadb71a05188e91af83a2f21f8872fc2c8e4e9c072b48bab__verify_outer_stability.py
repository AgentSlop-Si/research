#!/usr/bin/env python3
"""Exact catalog and quantitative 256-point Fourier/scan obstruction.

Only Python/NumPy. Does not claim impossibility of the unrestricted
four-stage factorization. Includes zero-generator/singular middle controls.
"""
from __future__ import annotations
import json, math, pathlib, hashlib
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent
N=256


def affine(cols):
    out=[]
    for x in range(1<<len(cols)):
        y=0
        for bit,c in enumerate(cols):
            if x & (1<<bit): y^=int(c)
        out.append(y)
    assert sorted(out)==list(range(len(out)))
    return np.asarray(out,dtype=np.int64)


def get_layout():
    d=json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())
    assert d['k']==8
    return [affine(c) for c in d['affine_shuffle_columns']]


def parity_mask(mask):
    return np.array([(int(i)&int(mask)).bit_count()&1 for i in range(N)],dtype=bool)


def boundary(arr):
    return int(np.count_nonzero(arr[1:] != arr[:-1]))


def identifying_mask(indices, parity_table):
    indicator=np.zeros(N,dtype=bool)
    indicator[np.asarray(indices,dtype=int)]=1
    for m in range(1,N):
        if np.array_equal(indicator,parity_table[m]) or np.array_equal(indicator,~parity_table[m]):
            return m
    raise ValueError('affine-transformed parity set was not parity')


def enumerate_gates():
    P1,P2,P3=get_layout()
    parity={m:parity_mask(m) for m in range(1,N)}
    out=[]
    for mask in range(1,N):
        g=~parity[mask]
        C=np.flatnonzero(g)
        R=np.flatnonzero(~g[P2])
        b0,b1=boundary(g),boundary(g[P2])
        assert len(C)==len(R)==N//2
        # H0 = P3^{-1} U P1^{-1}; exact endpoint selections.
        realrows=np.argsort(P3)[R]
        realcols=P1[C]
        a=identifying_mask(realcols,parity)
        b=identifying_mask(realrows,parity)
        # Earlier established power-of-two parity-block Fourier rank oracle.
        rank=64 if a.bit_length()+b.bit_length()<=8 else 128
        record={'mask':mask,'input_boundary':b0,'middle_boundary':b1,
                'middle_rank_ceiling':b0+b1,
                'fourier_row_parity_mask':b,'fourier_column_parity_mask':a,
                'fourier_rank_exact':rank}
        if b0+b1<N//2:
            out.append(record)
    out.sort(key=lambda d:(d['middle_rank_ceiling'],d['mask']))
    return out


def field_root(p):
    for g in range(2,p):
        z=pow(g,(p-1)//N,p)
        if pow(z,N//2,p)!=1:
            assert pow(z,N,p)==1
            return z
    raise RuntimeError('missing root')


def modrank(M,p):
    # Modular Gauss with vectorized elimination, no floating-point.
    A=np.asarray(M,dtype=np.int64).copy()%p
    m,n=A.shape
    row=0
    for col in range(n):
        if row==m:break
        nz=np.flatnonzero(A[row:,col]);
        if not len(nz):continue
        pivot=row+int(nz[0]);A[[row,pivot]]=A[[pivot,row]]
        inv=pow(int(A[row,col]),-1,p)
        if row+1<m:
            mul=A[row+1:,col]*inv%p
            A[row+1:,col+1:]=(A[row+1:,col+1:]-mul[:,None]*A[row,col+1:])%p
            A[row+1:,col]=0
        row+=1
    return row


def stage(p,rng):
    a,b,c,e,d=(rng.integers(0,p,N,dtype=np.int64) for _ in range(5))
    i=np.arange(N,dtype=np.int64)[:,None]
    j=np.arange(N,dtype=np.int64)[None,:]
    return np.where(i>j,a[:,None]*b[None,:],np.where(i<j,c[:,None]*e[None,:],d[:,None]))%p


def rank_checks(gates):
    P1,P2,P3=get_layout(); x=np.arange(N,dtype=np.int64)
    output=[]
    for p in (12289,65537):
        omega=field_root(p)
        z=np.array([pow(omega,k,p) for k in range(N)],dtype=np.int64)
        rng=np.random.default_rng(20261010)
        S2,S3=stage(p,rng),stage(p,rng)
        middle=(S3@S2[P2,:])%p
        # Independent exact zero-generator control, including a singular stage.
        sparse=np.eye(N,dtype=np.int64)
        sparse[::3,:]=0
        singular_middle=sparse[P2,:]
        tested_middle=[]
        masks_checked=[]
        for rec in gates:
            mask=rec['mask']; g=~parity_mask(mask)
            C=np.flatnonzero(g);R=np.flatnonzero(~g[P2])
            if rec['middle_rank_ceiling']<65:  # all spectral certificates
                actual=modrank(middle[np.ix_(R,C)],p)
                degenerate=modrank(singular_middle[np.ix_(R,C)],p)
                assert actual<=rec['middle_rank_ceiling'],(p,mask,actual)
                assert degenerate<=rec['middle_rank_ceiling'],(p,mask,degenerate)
                tested_middle.append({'mask':mask,'rank':actual,'zero_branch_rank':degenerate})
            rr=np.argsort(P3)[R];cc=P1[C]
            block=z[(rr[:,None]*cc[None,:])%N]
            actual_rank=modrank(block,p)
            assert actual_rank==rec['fourier_rank_exact'],(p,mask,actual_rank,rec)
            masks_checked.append(mask)
        output.append({'prime':p,'primitive_root':omega,
                       'all_exact_fourier_rank_checks':len(masks_checked),
                       'middle_control_tests':tested_middle})
    return output


def numerical_check(gates):
    P1,P2,P3=get_layout()
    rows=np.argsort(P3)
    c=np.arange(N)
    w=np.exp(2j*np.pi/N)
    out=[]
    for rec in gates[:7]:
        mask=rec['mask'];g=~parity_mask(mask)
        R=np.flatnonzero(~g[P2]); C=np.flatnonzero(g)
        rr=rows[R];cc=P1[C]
        # 1/sqrt(256) normalized unitary DFT, exact magnitude for each entry.
        H=(1/16)*w**((rr[:,None]*cc[None,:])%N)
        s=np.linalg.svd(H,compute_uv=False)
        k=rec['middle_rank_ceiling'];
        fro2=float(np.sum(s*s))
        assert abs(fro2-64)<1.e-9
        assert s[0]<1+1.e-12
        assert s[-1]>1e-5  # full complex rank for these 7 masks
        guaranteed=math.sqrt(max(0,(64-k)/(128-k)))
        assert s[k]+1e-10>=guaranteed
        out.append({'mask':mask,'rank_cap':k,
                    'numerical_fourth_moment':float(np.sum(s**4)),
                    'certified_lower_bound':guaranteed,
                    'observed_sigma_k_plus_1':float(s[k]),
                    'observed_smallest_sigma':float(s[-1])})
    return out


def main():
    gates=enumerate_gates()
    assert len(gates)==32, len(gates)
    assert len([g for g in gates if g['middle_rank_ceiling']<64])==7
    assert gates[0]['mask']==64 and gates[0]['middle_rank_ceiling']==16
    assert all(g['fourier_rank_exact']==128 for g in gates)
    modular=rank_checks(gates)
    numerical=numerical_check(gates)
    from verify_moment_rational import exact_interval
    _, moment_low, moment_high, _, _ = exact_interval()
    assert moment_low > __import__('fractions').Fraction(1264,25)
    assert abs(numerical[0]['numerical_fourth_moment'] - float((moment_low+moment_high)/2)) < 1e-9
    energy_rho=math.sqrt(3/7)
    rho=3*math.sqrt(2)/5
    eps_min=math.sqrt(1+rho)-1
    result={'N':N,'description':'Necessary simultaneous outer-inverse constraints; no complete nonexistence proof',
            'rank_deficient_gates':len(gates),
            'verified_complex_ranks':32,
            'strongest_gate':gates[0],
            'certified_spectral_rank_bound':rho,
            'elementary_energy_only_bound':energy_rho,
            'symmetric_unitary_diagonal_neighborhood_radius':eps_min,
            'masked_constraints':gates,
            'modular_checks':modular,
            'numerical_svd_explorations':numerical}
    (ROOT/'EXACT_AND_NUMERIC_CERTIFICATES.json').write_text(json.dumps(result,indent=2))
    print('PASS 32/32 parity-mask gates; 64/64 Fourier modular ranks; 14/14 synthetic middle checks')
    print('PASS 7/7 singular-value checks, exact rational spectral lower bound 3sqrt(2)/5')
    print('epsilon exclusion threshold',f'{eps_min:.12f}')
    print('smallest cap',gates[0], 'strongest numerical',numerical[0])
    return result

if __name__=='__main__':main()
