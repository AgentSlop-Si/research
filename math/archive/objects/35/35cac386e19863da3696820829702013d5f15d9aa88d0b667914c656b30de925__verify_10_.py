"""Independent numerical / finite-field verification of projective Fourier gauge rigidity.

Python 3, numpy only. The projective bound is proved in THEOREM.md;
this program checks random genuine 4-Green networks and known exact controls.
"""
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
RNG = np.random.default_rng(20261010)


def inverse_cycle_apply(perm, w, v):
    """Solve (I-diag(w)P_perm) y=v using one cyclic recurrence: O(N)."""
    n = len(perm)
    cyc = [0]
    for _ in range(n - 1):
        cyc.append(int(perm[cyc[-1]]))
    assert len(set(cyc)) == n and perm[cyc[-1]] == cyc[0]
    pref = 1 + 0j
    a = 0 + 0j
    for i in cyc:
        a += pref * v[i]
        pref *= w[i]
    assert abs(1 - pref) > 1e-12
    y = np.empty(n, dtype=complex)
    y[cyc[0]] = a / (1 - pref)
    for t in range(n - 1, 0, -1):
        i = cyc[t]
        y[i] = v[i] + w[i] * y[perm[i]]
    residual = y - w * y[perm] - v
    assert np.linalg.norm(residual) < 2e-9 * max(1, np.linalg.norm(v))
    return y


class Green:
    def __init__(self, n, rng):
        cycle = rng.permutation(n)
        self.perm = np.empty(n, dtype=int)
        for i, j in zip(cycle, np.roll(cycle, -1)):
            self.perm[i] = j
        self.n = n
        self.weight = (0.86 + 0.07 * rng.random(n)) * np.exp(2j * np.pi * rng.random(n))
        self.row_perm = rng.permutation(n)
        self.col_perm = rng.permutation(n)
        self.row_scale = (0.8 + .4*rng.random(n))*np.exp(2j * np.pi * rng.random(n))
        self.col_scale = (0.8 + .4*rng.random(n))*np.exp(2j * np.pi * rng.random(n))
        self.reverse = np.empty(n, dtype=int)
        self.reverse[self.perm] = np.arange(n)

    def apply(self, x):
        z = np.empty(self.n, dtype=complex)
        z[self.col_perm] = self.col_scale * x
        v = inverse_cycle_apply(self.perm, self.weight, z)
        return self.row_scale * v[self.row_perm]

    def adjoint(self, x):
        z = np.empty(self.n, dtype=complex)
        z[self.row_perm] = np.conj(self.row_scale) * x
        v = inverse_cycle_apply(self.reverse, np.conj(self.weight[self.reverse]), z)
        return np.conj(self.col_scale) * v[self.col_perm]

    def explicit(self):
        n=self.n
        K=np.eye(n,dtype=complex)
        K[np.arange(n),self.perm]-=self.weight
        G=np.linalg.inv(K)
        return self.row_scale[:,None]*G[np.ix_(self.row_perm,self.col_perm)]*self.col_scale[None,:]


class Stage:
    def __init__(self, n, rng):
        self.parts=[Green(n,rng), Green(n,rng)]
        self.n=n
    def apply(self,x): return sum((p.apply(x) for p in self.parts),np.zeros(self.n,complex))
    def adjoint(self,x): return sum((p.adjoint(x) for p in self.parts),np.zeros(self.n,complex))
    def explicit(self): return sum((p.explicit() for p in self.parts),np.zeros((self.n,self.n),complex))


def pair_matrices(A,B,omega):
    n=len(A);b0=B[:,0];b1=B[:,1];C0=A*b0[None,:];C1=A*b1[None,:]
    Delta=omega**np.arange(n)
    K=C1-Delta[:,None]*C0
    return C0,C1,K,Delta


def row_optimal(d,C0,C1,omega):
    u=C0@d; v=C1@d
    n=len(u); phase=omega**np.arange(n)
    s=np.abs(u)**2+np.abs(v)**2
    ell=np.ones(n,dtype=complex)
    good=s>1e-24
    ell[good]=(np.conj(u[good])+np.conj(v[good])*phase[good])/s[good]
    pair_err=np.linalg.norm(np.column_stack((ell*u-1,ell*v-phase)), 'fro')
    exact_sq=np.sum(np.divide(np.abs(v-phase*u)**2,s,out=np.zeros(n),where=good)+2*(~good))
    assert abs(pair_err**2-exact_sq)<2e-9*max(1,exact_sq)
    return ell,pair_err,exact_sq


def gap(C0,C1,K):
    Q=C0.conj().T@C0+C1.conj().T@C1
    ev, V=np.linalg.eigh(Q)
    assert np.min(ev)>1e-12, "Q must be strictly positive for an invertible pencil"
    Qi=(V / np.sqrt(ev)[None,:])@V.conj().T
    lam=np.linalg.eigvalsh(Qi@(K.conj().T@K)@Qi)
    assert np.min(lam)>-1e-9
    return np.sqrt(max(0.,float(lam[0])/2.)), float(np.linalg.svd(K,compute_uv=False)[-1]), float(np.linalg.cond(K))


def numeric_case(n, rng):
    first=Stage(n,rng); second=Stage(n,rng)
    A=first.explicit();B=second.explicit()
    x=rng.normal(size=n)+1j*rng.normal(size=n)
    assert np.linalg.norm(first.apply(x)-A@x)<1e-10
    assert np.linalg.norm(second.apply(x)-B@x)<1e-10
    assert np.linalg.norm(first.adjoint(x)-A.conj().T@x)<1e-10
    assert np.linalg.norm(second.adjoint(x)-B.conj().T@x)<1e-10
    omega=np.exp(-2j*np.pi/n)
    C0,C1,K,Delta=pair_matrices(A,B,omega)
    f=np.array([[omega**(i*j) for j in range(n)] for i in range(n)])
    projective_gap,sigma_min,kcond=gap(C0,C1,K)
    assert projective_gap>0
    sample_errors=[];sample_optimized=[]
    for _ in range(40):
        d=(0.6+1.1*rng.random(n))*np.exp(2j*np.pi*rng.random(n))
        ell=(0.3+1.1*rng.random(n))*np.exp(2j*np.pi*rng.random(n))
        M=ell[:,None]*A@np.diag(d)@B
        actual=np.linalg.norm(M-f,2)
        assert actual >= projective_gap - 1e-8, (actual,projective_gap)
        sample_errors.append(float(actual))
        lo, pe, _=row_optimal(d,C0,C1,omega)
        Mo=lo[:,None]*(A@np.diag(d)@B)
        ee=np.linalg.norm(Mo-f,2)
        assert ee>=projective_gap-1e-8
        assert pe >= np.sqrt(2)*projective_gap-1e-8
        sample_optimized.append(float(ee))
        z=rng.normal(size=n)+1j*rng.normal(size=n)
        mv=first.apply(d*second.apply(z))
        assert np.linalg.norm(mv-A@np.diag(d)@B@z)<1e-10
        k_mv=first.apply(B[:,1]*d)-Delta*first.apply(B[:,0]*d)
        assert np.linalg.norm(k_mv-K@d)<1e-10
        u=rng.normal(size=n)+1j*rng.normal(size=n)
        k_adj=np.conj(B[:,1])*first.adjoint(u)-np.conj(B[:,0])*first.adjoint(np.conj(Delta)*u)
        assert np.linalg.norm(k_adj-K.conj().T@u)<1e-10
    return dict(n=n,gap_lower_bound=projective_gap,pencil_sigma_min=sigma_min,pencil_condition=kcond,
                smallest_random_spectral_error=min(sample_errors),smallest_row_opt_spectral_error=min(sample_optimized),
                complex_green_branches=4,checked_random_diagonal_pairs=40)


def exact_positive_control(n):
    root=np.exp(-2j*np.pi/n)
    F=np.array([[root**(j*k) for k in range(n)] for j in range(n)])
    B=np.eye(n,dtype=complex); A=F.copy()
    C0,C1,K,_=pair_matrices(A,B,root)
    assert np.linalg.norm(K@np.ones(n))<1e-10
    return dict(n=n,kind='known exact F=AIB',pencil_rank=int(np.linalg.matrix_rank(K,tol=1e-9)),passed=True)


def exact_finite_field_certificate():
    src=HERE/'REFERENCE_CERTIFICATE.json'
    c=json.loads(src.read_text())
    p=c['prime']; M=c['pencil_matrix']; n=c['N']
    assert n==len(M) and len(M[0])==n
    E=[list(map(lambda x:x%p,row)) for row in M]
    det=1
    for j in range(n):
        row=next((i for i in range(j,n) if E[i][j]%p),None)
        assert row is not None
        if row!=j:
            E[j],E[row]=E[row],E[j]
            det=-det
        pivot=E[j][j]%p; det=det*pivot%p
        inv=pow(pivot,-1,p)
        for i in range(j+1,n):
            q=E[i][j]*inv%p
            if q:
                for k in range(j,n): E[i][k]=(E[i][k]-q*E[j][k])%p
    assert det==c['two_column_pencil_det_GF65537'] ==55687
    return dict(n=n,finite_field=f'GF({p})',determinant=det,verified=True)


def run():
    r={"theorem":"Two-column projective Fourier gauge rigidity",
       "exact_controls":[exact_positive_control(i) for i in (4,8,16)],
       "complex_four_green_tests":[numeric_case(i,RNG) for i in (8,16,32)],
       "exact_modular_witness":exact_finite_field_certificate()}
    (HERE/'RESULTS.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))

if __name__=='__main__':run()
