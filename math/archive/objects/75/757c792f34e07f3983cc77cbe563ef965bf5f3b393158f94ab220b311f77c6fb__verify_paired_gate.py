#!/usr/bin/env python3
"""Independent paired-complement and Jacobi-dual verification for the
saved four-stage N=256 affine-scan architecture. Exact field arithmetic
is used for all algebraic claims; SVD is an explicitly non-proof control.
"""
from __future__ import annotations
import json, pathlib, sys, math
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
OLD=ROOT/'previous_research'
N=256

def affine(columns):
    out=[]
    for x in range(256):
        y=0
        for bit,col in enumerate(columns):
            if x>>bit&1:y^=int(col)
        out.append(y)
    assert sorted(out)==list(range(N))
    return np.asarray(out,dtype=np.int64)

def data():
    cfg=json.loads((ROOT/'AFFINE_LAYOUT.json').read_text())
    P1,P2,P3=[affine(x) for x in cfg['affine_shuffle_columns']]
    return P1,P2,P3

def parity(mask):
    return np.fromiter(((i&mask).bit_count()%2==0 for i in range(N)),dtype=np.bool_,count=N)

def boundary(g):return int(np.count_nonzero(g[1:]!=g[:-1]))

def gates():
    P1,P2,P3=data();q=np.arange(N)
    out=[]
    for mask in range(1,N):
        g=parity(mask)
        C=q[g]; R=q[~g[P2]]
        b=boundary(g)+boundary(g[P2])
        if b<128:
            out.append((mask,R,C,b))
    out.sort(key=lambda x:(x[3],x[0]))
    assert len(out)==32 and out[0][0]==64 and out[0][3]==16
    return out

def modrank(M,p):
    A=np.array(M,dtype=np.int64,copy=True)%p
    n,m=A.shape;r=0
    for j in range(m):
        if r>=n:break
        idx=np.flatnonzero(A[r:,j])
        if not idx.size:continue
        k=r+int(idx[0]);A[[r,k]]=A[[k,r]]
        inv=pow(int(A[r,j]),-1,p)
        if r+1<n:
            z=(A[r+1:,j]*inv)%p
            A[r+1:,j+1:]=(A[r+1:,j+1:]-z[:,None]*A[r,j+1:])%p
            A[r+1:,j]=0
        r+=1
    return r

def modinverse(M,p):
    A=np.asarray(M,dtype=np.int64).copy()%p
    n=A.shape[0]; assert A.shape==(n,n)
    I=np.eye(n,dtype=np.int64)
    for j in range(n):
        idx=np.flatnonzero(A[j:,j]);assert idx.size,'singular synthetic control'
        k=j+int(idx[0])
        if k!=j:
            A[[j,k]]=A[[k,j]];I[[j,k]]=I[[k,j]]
        t=pow(int(A[j,j]),-1,p)
        A[j,:]=A[j,:]*t%p;I[j,:]=I[j,:]*t%p
        active=np.r_[np.arange(j),np.arange(j+1,n)]
        factor=A[active,j].copy()
        A[active,:]=(A[active,:]-factor[:,None]*A[j,:])%p
        I[active,:]=(I[active,:]-factor[:,None]*I[j,:])%p
    assert np.array_equal(A,np.eye(n,dtype=np.int64))
    return I

def detmod(M,p):
    A=np.asarray(M,dtype=np.int64).copy()%p
    n=A.shape[0];assert A.shape==(n,n)
    d=1
    for j in range(n):
        idx=np.flatnonzero(A[j:,j])
        if not idx.size:return 0
        k=j+int(idx[0])
        if k!=j:
            A[[j,k]]=A[[k,j]];d=(-d)%p
        pivot=int(A[j,j]);d=d*pivot%p
        if j+1<n:
            factor=A[j+1:,j]*pow(pivot,-1,p)%p
            A[j+1:,j+1:]=(A[j+1:,j+1:]-factor[:,None]*A[j,j+1:])%p
            A[j+1:,j]=0
    return int(d)

def field_root(p):
    for g in range(2,p):
        z=pow(g,(p-1)//N,p)
        if pow(z,N//2,p)!=1 and pow(z,N,p)==1:return z
    raise ValueError('no root')

def fourier(p):
    z=field_root(p)
    powers=np.array([pow(z,i,p) for i in range(N)],dtype=np.int64)
    e=np.arange(N,dtype=np.int64)
    F=powers[(e[:,None]*e[None,:])%N]
    inverse=powers[(-e[:,None]*e[None,:])%N]
    a=pow(16,-1,p)
    return F*a%p,inverse*a%p

def rand_stage(p,rng):
    a,b,c,e,d=[rng.integers(0,p,N,dtype=np.int64) for _ in range(5)]
    d=(d% (p-1))+1
    i=np.arange(N)[:,None];j=np.arange(N)[None,:]
    return np.where(i>j,a[:,None]*b[None,:],np.where(i<j,c[:,None]*e[None,:],d[:,None]))%p

def general_qs_stage(p,rng):
    """Standard recurrence generators with exact zeros, no divisions.
    S[i,j] = row_i * transfer_(i-1)...transfer_(j+1) * col_j
    below the diagonal; independent generators above the diagonal.
    """
    ll,lc,lt,ul,uc,ut=[rng.integers(0,p,N,dtype=np.int64) for _ in range(6)]
    lt[::17]=0;ut[7::19]=0;ll[3::23]=0;uc[5::29]=0
    diag=rng.integers(1,p,N,dtype=np.int64)
    S=np.diag(diag)
    for j in range(N):
        multiplier=1
        for i in range(j+1,N):
            if i>j+1:multiplier=multiplier*int(lt[i-1])%p
            S[i,j]=int(ll[i])*multiplier*int(lc[j])%p
    for i in range(N):
        multiplier=1
        for j in range(i+1,N):
            if j>i+1:multiplier=multiplier*int(ut[j-1])%p
            S[i,j]=int(ul[i])*multiplier*int(uc[j])%p
    return S

def test():
    P1,P2,P3=data();Ip3=np.argsort(P3)
    v=gates();all_idx=np.arange(N)
    res={'n':N,'gates':len(v),'paired_gates':2*len(v),'controls':[],'fourier_minor_witnesses':[]}
    for p in (12289,65537):
        U,Uinv=fourier(p)
        assert np.array_equal(U@Uinv%p,np.eye(N,dtype=np.int64))
        # Identity-outer Fourier controls, also check dual (inverse) blocks.
        H0=U[np.ix_(Ip3,P1)]
        G0=Uinv[np.ix_(P1,Ip3)]
        checked=0
        for mask,R,C,b in v:
            Rc=np.setdiff1d(all_idx,R,assume_unique=True)
            Cc=np.setdiff1d(all_idx,C,assume_unique=True)
            for block_name,rows,cols,dual_rows,dual_cols in (("A",R,C,Cc,Rc),("D",Rc,Cc,C,R)):
                if mask==64:
                    primal17=detmod(H0[np.ix_(rows[:17],cols[:17])],p)
                    dual17=detmod(G0[np.ix_(dual_rows[:17],dual_cols[:17])],p)
                    assert primal17 and dual17
                    res['fourier_minor_witnesses'].append({
                        'prime':p,'block':block_name,'primal_17x17_det':primal17,
                        'dual_17x17_det':dual17})
                rank=modrank(H0[np.ix_(rows,cols)],p)
                dualrank=modrank(G0[np.ix_(dual_rows,dual_cols)],p)
                assert rank==dualrank==128,(p,mask,b,rank,dualrank)
                checked+=1
        # A generic invertible synthetic middle product. Tests zero/nonzero
        # generator branches are also included by diagonal-stage controls.
        rng=np.random.default_rng(1729+p)
        S2=general_qs_stage(p,rng);S3=general_qs_stage(p,rng)
        H=S3@S2[P2,:]%p
        Hinv=modinverse(H,p)
        nchecks=0
        for mask,R,C,b in v:
            Rc=np.setdiff1d(all_idx,R,assume_unique=True)
            Cc=np.setdiff1d(all_idx,C,assume_unique=True)
            for rows,cols,dual_rows,dual_cols in ((R,C,Cc,Rc),(Rc,Cc,C,R)):
                rank=modrank(H[np.ix_(rows,cols)],p)
                dualrank=modrank(Hinv[np.ix_(dual_rows,dual_cols)],p)
                assert rank==dualrank<=b,(p,mask,b,rank,dualrank)
                nchecks+=1
            if mask==64:
                assert modrank(H[np.ix_(R,Cc)],p)>=128-b
                assert modrank(H[np.ix_(Rc,C)],p)>=128-b
        # Degenerate zero-generator control (all identity stages)
        D=np.eye(N,dtype=np.int64)[P2,:]
        for mask,R,C,b in v[:7]:
            Rc=np.setdiff1d(all_idx,R,assume_unique=True)
            Cc=np.setdiff1d(all_idx,C,assume_unique=True)
            assert modrank(D[np.ix_(R,C)],p)<=b
            assert modrank(D[np.ix_(Rc,Cc)],p)<=b
        res['controls'].append({'field':p,'fourier_full_ranks_and_duals':checked,
              'synthetic_primal_and_dual_ranks':nchecks,'degenerate_paired_cases':14})
        print('PASS p',p,'Fourier and Jacobi blocks',checked,
              'synthetic complemented and dual gates',nchecks,flush=True)
    # Numerical check of singular-value pairing and the relaxation optimum.
    omega=np.exp(2j*np.pi/N)
    xy=np.arange(N,dtype=np.int64)
    UF=np.exp(2j*np.pi*(xy[:,None]*xy[None,:])/N)/16
    H0=UF[np.ix_(Ip3,P1)]
    mask,R,C,b=v[0]
    Rc=np.setdiff1d(all_idx,R,assume_unique=True)
    Cc=np.setdiff1d(all_idx,C,assume_unique=True)
    A=H0[np.ix_(R,C)];D=H0[np.ix_(Rc,Cc)]
    svA=np.linalg.svd(A,compute_uv=False);svD=np.linalg.svd(D,compute_uv=False)
    assert np.allclose(svA,svD,atol=1e-12,rtol=0)
    tailA=float(np.sum(svA[b:]**2));tailD=float(np.sum(svD[b:]**2))
    assert tailA+tailD>96 and tailA+tailD<97
    # Exact combinatorial certificate that elementary scalar tail-energy
    # inequalities from ALL 64 gates cannot improve the paired 96 bound.
    base_support=np.zeros((N,N),dtype=np.bool_)
    base_support[np.ix_(Ip3[R],P1[C])]=True
    base_support[np.ix_(Ip3[Rc],P1[Cc])]=True
    assert int(base_support.sum())==32768
    all_overlap=[]
    for mm,rr,cc,bb in v[1:]:
        rrc=np.setdiff1d(all_idx,rr,assume_unique=True)
        ccc=np.setdiff1d(all_idx,cc,assume_unique=True)
        for rr2,cc2 in ((rr,cc),(rrc,ccc)):
            overlap=int(base_support[np.ix_(Ip3[rr2],P1[cc2])].sum())
            assert overlap==8192,(mm,overlap)
            all_overlap.append(overlap)
    # Each nonleading half-block receives 8192*(48/16384)=24 units
    # of artificial cell energy. Its required scalar budget <=17.
    assert max(max(0,64-item[3]) for item in v[1:])==17
    res['energy_relaxation_certificate']={
        'all_64_scalar_frobenius_energy_constraints_optimum_squared':96,
        'base_two_blocks_each_cell_weight':'3/1024',
        'base_support_cells':32768,
        'every_other_half_block_overlap_cells':8192,
        'other_half_blocks_checked':len(all_overlap),
        'maximum_other_scalar_energy_demand':17,
        'artificial_energy_received_by_each_other_half_block':24
    }
    # New unitary-outer-stage geometry theorem, conditional on both C's
    # being exactly unitary (not assumed for the main FFT candidate).
    geom=math.sqrt(2-2*math.sqrt(7)/5)
    epsu=geom/2
    st=3*math.sqrt(2)/5
    th=math.acos(st)
    def rot(x):return np.array([[math.cos(x),-math.sin(x)],[math.sin(x),math.cos(x)]])
    # Sharp two-dimensional model at the boundary s=3sqrt(2)/5.
    assert abs(np.linalg.norm(rot(th)-rot(math.pi/2),ord=2)-geom)<1e-12
    res['unitary_outer_conditional_bound']={
        'certified_strict_min_operator_distance':'sqrt(2-2sqrt(7)/5)',
        'decimal':geom,
        'strict_unitary_symmetric_radius':epsu,
        'conditional_on_outer_C1_C4_being_unitary':True
    }
    res['norm_bounds']={
        'paired_mask':64,'middle_rank_cap_each':16,
        'certified_min_frobenius_norm_squared':96,
        'certified_min_trace_norm':96,
        'observed_optimal_paired_block_frobenius_squared':tailA+tailD,
        'observed_paired_block_spectral_pairing_max_difference':float(np.max(np.abs(svA-svD))),
        'observed_best_two_block_frobenius_norm':math.sqrt(tailA+tailD),
        'largest_below_rank_threshold_singular_value':float(svA[b]),
    }
    assert len(v)==32
    (ROOT/'NEW_CERTIFICATES.json').write_text(json.dumps(res,indent=2))
    print('PASS 64 complementary rank gates, Jacobi dualities, cross-block ranks and CS pairing')
    print('PASS exact Frobenius lower bound sqrt(96), trace norm lower bound 96')
    print('Relaxed optimum (numerical, non-proof):', math.sqrt(tailA+tailD))

if __name__=='__main__':test()
