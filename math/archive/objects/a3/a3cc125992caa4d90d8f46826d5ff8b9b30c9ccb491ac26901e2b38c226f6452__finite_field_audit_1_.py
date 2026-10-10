"""Exact modular independent audits of the general and Fourier-specific window bound.

The endpoint-reordered Cooley--Tukey control is ESSENTIAL: the simplified
Vandermonde inequality must not be applied after arbitrary input reorderings.
"""
from __future__ import annotations
import json, random
from pathlib import Path
import numpy as np
from window_gate import check_windows, inequalities_for_window, combinatorial_ceiling
from ct_reference_control import ct_factor, fft_matrix, qs_order

ROOT=Path(__file__).parent
P=12289

def modrank(A,p):
    A=np.asarray(A,dtype=np.int64).copy()%p
    if A.size==0:return 0
    m,n=A.shape; r=0
    for j in range(n):
        if r==m:break
        inds=np.flatnonzero(A[r:,j])
        if len(inds)==0:continue
        k=r+int(inds[0]);A[[r,k]]=A[[k,r]]
        A[r,j:]=(A[r,j:]*pow(int(A[r,j]),-1,p))%p
        if r+1<m:
            f=A[r+1:,j].copy()
            A[r+1:,j:]=(A[r+1:,j:] - f[:,None]*A[r,j:][None,:])%p
        r+=1
    return r

def invmod(A,p):
    A=np.asarray(A,dtype=np.int64)%p
    n=A.shape[0]
    assert A.shape==(n,n)
    M=np.concatenate([A.copy(),np.eye(n,dtype=np.int64)],axis=1)%p
    for j in range(n):
        nz=np.flatnonzero(M[j:,j]);assert len(nz), 'singular control'
        k=j+int(nz[0]);M[[j,k]]=M[[k,j]]
        M[j]=(M[j]*pow(int(M[j,j]),-1,p))%p
        for i in range(n):
            if i==j:continue
            f=int(M[i,j]);M[i]=(M[i]-f*M[j])%p
    assert np.array_equal((A@M[:,n:])%p,np.eye(n,dtype=np.int64))
    return M[:,n:]

def prim_root(n,p):
    assert (p-1)%n==0
    for g in range(2,p):
        z=pow(g,(p-1)//n,p)
        if pow(z,n,p)==1 and (n==1 or pow(z,n//2,p)!=1):return z
    raise ValueError('no primitive root')

def generalized_necessary(M, pi, u,v, cup, cdown, bup, bdown,p):
    """All 3 rank-nullity gates with actual rectangular submatrix ranks."""
    n=len(pi);I=range(u,v+1);J=pi[u:v+1]
    a,b=min(J),max(J);t=v-u+1
    R=list(range(u))+list(range(v+1,n))
    bc=(bup if u>0 else 0)+(bdown if v<n-1 else 0)
    out=[]
    for kind,H,cost in (
      ('head',list(range(a,n)),bc+(cup if a>0 else 0)),
      ('tail',list(range(b+1)),bc+(cdown if b<n-1 else 0)),
      ('both',list(range(a,b+1)),bc+(cup if a>0 else 0)+(cdown if b<n-1 else 0)),
    ):
        k=modrank(M[np.ix_(R,H)],p) if R and H else 0
        required=t-len(H)+k
        assert required<=cost, (kind,u,v,a,b,required,cost)
        out.append((kind,required,cost,k,len(H)))
    return out

def ct_endpoint_control():
    rows=[]
    for a,b,oa,ob in [(2,4,[0,1],[0,2,1,3]),
                        (4,4,[0,2,1,3],[0,2,1,3])]:
        A,B,mid,inp,out=ct_factor(a,b,oa,ob)
        n=a*b
        C=invmod(A,P)
        assert qs_order(C)==qs_order(A)==qs_order(B)==1
        M=fft_matrix(n)[np.ix_(out,inp)]
        assert np.array_equal((M@C[:,mid])%P,B)
        allchecks=0
        for u in range(n):
            for v in range(u,n):
                generalized_necessary(M,mid,u,v,1,1,1,1,P)
                allchecks+=3
        # Specific early interval violates simplified Vandermonde screen;
        # corrected Fourier submatrix rank fully explains valid construction.
        u,v=0,2;a0,b0=min(mid[:3]),max(mid[:3]);h=b0-a0+1
        R=list(range(v+1,n));H=list(range(a0,b0+1))
        actual_rank=modrank(M[np.ix_(R,H)],P)
        generic_full_rank=min(n-3,h)
        corrected = 3-h+actual_rank
        naive = 3-h+generic_full_rank
        budget=(v<n-1)+(a0>0)+(b0<n-1)
        assert actual_rank==generic_full_rank-1
        assert corrected==budget==2 and naive==3
        assert check_windows(mid), 'both endpoint reorderings MUST defeat naive theorem'
        rows.append({'n':n,'stage_qs_ranks':[1,1],
            'exact_Fourier_factorization':True,
            'input_order':inp,'output_order':out,'middle_permutation':mid,
            'window_checks':allchecks,
            'witness_interval':[u,v],'witness_C_span':[a0,b0],
            'naive_vandermonde_rank':generic_full_rank,
            'actual_endpoint_reordered_rank':actual_rank,
            'corrected_gate_lower':corrected,'budget':budget,
            'naive_gate_lower':naive})
    return rows

def row_permuted_fourier_tests():
    rng=random.Random(20261009)
    rows=[]
    for n in (8,16,32,64):
        for p in (12289,65537):
            z=prim_root(n,p)
            O=list(range(n));rng.shuffle(O)
            M=np.array([[pow(z,O[i]*j,p) for j in range(n)] for i in range(n)],dtype=np.int64)
            count=0
            intervals=[]
            for _ in range(10 if n<=16 else 6):
                u=rng.randrange(n);v=rng.randrange(u,n)
                a=rng.randrange(n);b=rng.randrange(a,n)
                intervals.append((u,v,a,b))
            for u,v,a,b in intervals:
                R=list(range(u))+list(range(v+1,n))
                H=list(range(a,b+1))
                k=modrank(M[np.ix_(R,H)],p) if R else 0
                assert k==min(len(R),len(H)), (n,p,u,v,a,b,k)
                count+=1
            rows.append({'n':n,'p':p,'primitive_root':z,'rank_checks':count})
    return rows

def affine_input_tests():
    """A shift and odd modular stride preserve full Vandermonde rectangular ranks."""
    rng=random.Random(8437)
    rows=[]
    for n in (8,16,32,64):
        for p in (12289,65537):
            z=prim_root(n,p);count=0
            for case in range(4):
                a=rng.randrange(n);d=rng.choice(list(range(1,n,2)))
                perm_in=[(a+d*k)%n for k in range(n)]
                perm_out=list(range(n));rng.shuffle(perm_out)
                M=np.array([[pow(z,perm_out[i]*perm_in[k],p) for k in range(n)]
                            for i in range(n)],dtype=np.int64)
                for trial in range(4):
                    u=rng.randrange(n);v=rng.randrange(u,n)
                    lo=rng.randrange(n);hi=rng.randrange(lo,n)
                    R=list(range(u))+list(range(v+1,n))
                    H=list(range(lo,hi+1))
                    rk=modrank(M[np.ix_(R,H)],p) if R else 0
                    assert rk==min(len(R),len(H)),(n,p,a,d,u,v,lo,hi,rk)
                    count+=1
            rows.append({'n':n,'p':p,'tests':count,'affine_input_strides_are_invertible':True})
    return rows


def random_positive_controls():
    rng=random.Random(12938)
    counts=0
    for n in (8,16):
        for _ in range(6):
            # Both stages are invertible rank-one updates of diagonal, hence QS rank <=1.
            def stage():
                for __ in range(100):
                    u=np.array([rng.randrange(1,P) for x in range(n)],dtype=np.int64)
                    v=np.array([rng.randrange(1,P) for x in range(n)],dtype=np.int64)
                    Z=(np.eye(n,dtype=np.int64)+np.outer(u,v))%P
                    if (1+int(sum(int(u[i])*int(v[i]) for i in range(n))))%P: return Z
                raise RuntimeError('bad random seed')
            C=stage();B=stage();pi=list(range(n));rng.shuffle(pi)
            F=(B@invmod(C[:,pi],P))%P
            for u in range(n):
                for v in range(u,n):
                    generalized_necessary(F,pi,u,v,1,1,1,1,P)
                    counts+=3
    return counts


def run():
    report={
        'exact_CT_endpoint_positive_controls':ct_endpoint_control(),
        'row_reordered_Fourier_Vandermonde':row_permuted_fourier_tests(),
        'affine_input_and_arbitrary_output_tests':affine_input_tests(),
        'random_QS1_positive_general_rank_checks':random_positive_controls(),
        'scope':'General rank inequality survives both endpoint reorderings; simplified min(t,N-h) inequality requires natural Fourier input order. Positive checks are not complexity bounds.'
    }
    (ROOT/'FIELD_AUDIT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':run()
