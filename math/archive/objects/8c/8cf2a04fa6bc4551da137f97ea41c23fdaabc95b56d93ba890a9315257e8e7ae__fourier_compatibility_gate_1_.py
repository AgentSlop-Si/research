"""A NONLINEAR Fourier coefficient gate for the unchanged four-stage layout.

For every valid F = S4 P3 S3 P2 S2 P1 S1, the invertible outer inverse
stages C4=S4^-1, C1=S1^-1 necessarily satisfy
    rank( (P3^-1 C4 F C1 P1^-1)[R,C] ) <= 16.
Thus EVERY 17x17 minor of that submatrix must vanish, a family of exact
polynomial equations involving the outer inverse stage coefficients.

This is an explicitly computable NECESSARY condition, not a solution of the
equations. The controls verify nontriviality and zero-generator cases.
"""
from pathlib import Path
import json
import numpy as np
from verify_exact import affine
ROOT=Path(__file__).resolve().parent
N=256
PS=[affine(c) for c in json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())['affine_shuffle_columns']]
P1,P2,P3=PS
G=np.array([not bool(i&64) for i in range(N)])
C=np.flatnonzero(G)
R=np.flatnonzero(~G[P2])
assert len(C)==len(R)==128
BC=int(np.count_nonzero(G[1:]!=G[:-1]))
BR=int(np.count_nonzero(G[P2][1:]!=G[P2][:-1]))
assert (BC,BR)==(3,13)

def root(n,p):
    assert (p-1)%n==0
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n//2,p)!=1:return z
    raise ValueError('No root')

def rank_and_det_mod(M,p):
    """Return modular rank and determinant for square M (integer exact)."""
    A=np.asarray(M,dtype=np.int64).copy()%p
    n,m=A.shape
    rank=0;det=1;swap=0
    for j in range(m):
        if rank>=n:break
        where=np.flatnonzero(A[rank:,j])
        if not len(where):
            if n==m:return (rank,0)
            continue
        q=rank+int(where[0])
        if q!=rank:A[[rank,q]]=A[[q,rank]];swap+=1
        pivot=int(A[rank,j]);det=det*pivot%p
        inv=pow(pivot,-1,p)
        if rank+1<n:
            alpha=A[rank+1:,j]*inv%p
            A[rank+1:,j+1:]=(A[rank+1:,j+1:]-alpha[:,None]*A[rank,j+1:])%p
            A[rank+1:,j]=0
        rank+=1
    if n==m:return rank, (0 if rank<n else ((-det if swap%2 else det)%p))
    return rank,None

def rank_mod(M,p):
    a=np.asarray(M,dtype=np.int64).copy()%p;m,n=a.shape
    row=0
    for j in range(n):
        if row>=m:break
        w=np.flatnonzero(a[row:,j])
        if not len(w):continue
        piv=row+int(w[0]);a[[row,piv]]=a[[piv,row]]
        inv=pow(int(a[row,j]),-1,p)
        if row+1<m:
            alpha=a[row+1:,j]*inv%p
            a[row+1:,j+1:]=(a[row+1:,j+1:]-alpha[:,None]*a[row,j+1:])%p
            a[row+1:,j]=0
        row+=1
    return row

def Fourier_mod(p):
    w=root(N,p);powers=np.array([pow(w,i,p) for i in range(N)],dtype=np.int64)
    coords=np.arange(N,dtype=np.int64)
    return powers[(coords[:,None]*coords[None,:])%N]

def separated_stage(p,rng):
    a,b,c,e,d=[rng.integers(0,p,N,dtype=np.int64) for _ in range(5)]
    i=np.arange(N)[:,None];j=np.arange(N)[None,:]
    return np.where(i>j,a[:,None]*b[None,:],np.where(i<j,c[:,None]*e[None,:],d[:,None]))%p

def inv_lower_unit_separated(a,b,p):
    # Exact O(N^2) inverse of I+strict_lower(a_i b_j); no pivots.
    X=np.zeros((N,N),dtype=np.int64)
    pref=np.zeros(N,dtype=np.int64)
    for i in range(N):
        row=(-int(a[i])*pref)%p
        row[i]=(row[i]+1)%p
        X[i,:]=row
        pref=(pref+int(b[i])*row)%p
    return X

def inv_upper_unit_separated(c,e,p):
    # Exact O(N^2) inverse of I+strict_upper(c_i e_j); no pivots.
    X=np.zeros((N,N),dtype=np.int64)
    suff=np.zeros(N,dtype=np.int64)
    for i in range(N-1,-1,-1):
        row=(-int(c[i])*suff)%p
        row[i]=(row[i]+1)%p
        X[i,:]=row
        suff=(suff+int(e[i])*row)%p
    return X

def main():
    result={'N':N,'middle_rank_bound':BC+BR,'input_window_boundary':BC,'output_window_boundary':BR,
            'input_mask':64,'row_subset_size':len(R),'col_subset_size':len(C),
            'first17_rows':[int(x) for x in R[:17]],'first17_cols':[int(x) for x in C[:17]],
            'prime_controls':[]}
    for p in (12289,65537):
        rng=np.random.default_rng(2667)
        S2=separated_stage(p,rng);S3=separated_stage(p,rng)
        # P2 acting on vector means permuting ROWS of S2.
        H=(S3@S2[P2,:])%p
        middle_rank=rank_mod(H[np.ix_(R,C)],p)
        assert middle_rank<=16,(p,middle_rank)
        # Zero-generator control: S2=S3=I also obeys the bound.
        Id=np.eye(N,dtype=np.int64)
        zero_control=(Id@Id[P2,:])%p
        assert rank_mod(zero_control[np.ix_(R,C)],p)<=16
        F=Fourier_mod(p)
        # H0 = P3^-1 F P1^-1 for outer inverse stages equal to identity.
        H0=F[np.argsort(P3)][:,P1]
        full_rank=rank_mod(H0[np.ix_(R,C)],p)
        rank17,det17=rank_and_det_mod(H0[np.ix_(R[:17],C[:17])],p)
        assert full_rank==128 and rank17==17 and det17%p!=0,(p,full_rank,rank17,det17)
        # Nontrivial, always invertible one-sided outer inverse stages.
        # Unitriangular with strict off-diagonal rank-one tails.
        a,b,c,e=[rng.integers(0,p,N,dtype=np.int64) for _ in range(4)]
        ii=np.arange(N)[:,None];jj=np.arange(N)[None,:]
        C4=(Id+np.where(ii>jj,a[:,None]*b[None,:],0))%p
        C1=(Id+np.where(ii<jj,c[:,None]*e[None,:],0))%p
        H_random=(C4@F)%p
        H_random=(H_random@C1)%p
        H_random=H_random[np.argsort(P3)][:,P1]
        random_outer_rank=rank_mod(H_random[np.ix_(R,C)],p)
        assert random_outer_rank==128
        # Full four-factor nontrivial synthetic positive control:
        # choose S4=C4^-1, S1=C1^-1 (both quasiseparable order 1),
        # then recover the two-stage middle factor by cancelling them.
        S4=inv_lower_unit_separated(a,b,p)
        S1=inv_upper_unit_separated(c,e,p)
        assert np.array_equal((S4@C4)%p,Id)
        assert np.array_equal((S1@C1)%p,Id)
        full=(S4@H[P3,:])%p
        full=(full@S1[P1,:])%p
        recovered=(C4@full)%p
        recovered=(recovered@C1)%p
        recovered=recovered[np.argsort(P3)][:,P1]
        assert np.array_equal(recovered,H)
        assert rank_mod(recovered[np.ix_(R,C)],p)==middle_rank
        result['prime_controls'].append({'p':p,'valid_two_stage_middle_rank':middle_rank,
                        'original_Fourier_with_identity_outer_rank':full_rank,
                        'first17_minor_determinant_mod_p':int(det17),
                        'arbitrary_unitriangular_outer_inverse_rank':random_outer_rank,
                        'four_stage_synthetic_reconstruction':'passed'})
    (ROOT/'FOURIER_COMPATIBILITY_CERTIFICATES.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':main()
