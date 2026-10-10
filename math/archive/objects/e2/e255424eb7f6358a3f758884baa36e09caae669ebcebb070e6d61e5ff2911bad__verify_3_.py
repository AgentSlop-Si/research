#!/usr/bin/env python3
"""Independent verifier for Weyl-expansion FFT research, 2026-10-10.
Numerical tests are not a proof. Analytic proof is in THEOREMS.md.
Requires numpy. Uses explicit dense matrices ONLY in small-size control tests.
The stochastic test operates on an O(N)-apply four-Green product without
materializing its matrix or using an FFT to compute its output.
"""
import json
import math
import numpy as np
from dataclasses import dataclass


def unitary_fourier(n):
    j = np.arange(n)
    return np.exp(-2j * np.pi * j[:, None] * j[None, :] / n) / np.sqrt(n)


def shift(v, b):
    return np.roll(v, b)


def weyl(v, a, b):
    n = len(v)
    return np.exp(-2j * np.pi * (a % n) * np.arange(n) / n) * shift(v, b)


def phiweyl(v, a, b):
    n = len(v)
    return shift(np.exp(-2j * np.pi * (b % n) * np.arange(n) / n) * v, -a)


@dataclass
class Green:
    successor: np.ndarray
    weight: np.ndarray

    @classmethod
    def make(cls, rng, n, ordered_blocks=None):
        if ordered_blocks is None:
            order = rng.permutation(n)
        else:
            order = np.concatenate([rng.permutation(block) for block in ordered_blocks])
        p = np.empty(n, dtype=int)
        p[order] = np.roll(order, -1)
        # Small nonzero weights ensure invertibility, and avoid numerical instability.
        w = (0.11 + 0.3 * rng.random(n)) * np.exp(2j * np.pi * rng.random(n))
        return cls(p, w)

    def ordered_cycle(self):
        p = self.successor
        n = len(p)
        order = np.empty(n, dtype=int)
        order[0] = 0
        for i in range(1, n):
            order[i] = p[order[i-1]]
        assert len(set(order.tolist())) == n and p[order[-1]] == order[0]
        return order

    def apply(self, v):
        # Solve (I - diag(w) P) y = v in O(N) using a single-cycle recurrence.
        order = self.ordered_cycle()
        w = self.weight[order]
        b = np.asarray(v, dtype=complex)[order]
        sum_tail = b[-1]
        for i in range(len(b) - 2, -1, -1):
            sum_tail = b[i] + w[i] * sum_tail
        cycle_product = np.prod(w)
        y = np.empty(len(b), dtype=complex)
        y[0] = sum_tail / (1 - cycle_product)
        for i in range(len(b)-1, 0, -1):
            y[i] = b[i] + w[i] * y[(i+1) % len(b)]
        out = np.empty(len(b), dtype=complex)
        out[order] = y
        return out

    def denominator(self):
        n = len(self.successor)
        a = np.eye(n, dtype=complex)
        a[np.arange(n), self.successor] -= self.weight
        return a

    def crossing(self, subset):
        n = len(self.successor)
        keep = np.zeros(n, dtype=bool)
        keep[np.asarray(subset, dtype=int)] = True
        return int(np.sum(keep & (~keep[self.successor]) & (np.abs(self.weight) > 0)))


class TwoByTwoGreen:
    def __init__(self, greens):
        assert len(greens) == 4
        self.greens = greens
        self.n = len(greens[0].weight)

    def apply(self, v):
        g1,g2,g3,g4 = self.greens
        t = g3.apply(v) + g4.apply(v)
        return g1.apply(t) + g2.apply(t)

    def dense(self):
        return np.column_stack([self.apply(np.eye(self.n)[:,j]) for j in range(self.n)])


def dense_twirl(n, M):
    U = unitary_fourier(n)
    lam = np.trace(U.conj().T @ M) / n
    tau2 = float(np.linalg.norm(M-lam*U, 'fro')**2)
    lhs = 0.0
    eye = np.eye(n, dtype=complex)
    for a in range(n):
        for b in range(n):
            W = np.column_stack([weyl(eye[:,j], a, b) for j in range(n)])
            Phi = np.column_stack([phiweyl(eye[:,j], a, b) for j in range(n)])
            lhs += np.linalg.norm(M @ W - Phi @ M, 'fro')**2 / (2*n*n)
    return tau2, lhs


def estimate_twirl(M, n, rng, shots=2500):
    out = []
    for _ in range(shots):
        a=int(rng.integers(n)); b=int(rng.integers(n))
        z=(rng.standard_normal(n)+1j*rng.standard_normal(n))/math.sqrt(2)
        E = M.apply(weyl(z,a,b)) - phiweyl(M.apply(z),a,b)
        out.append(0.5*float(np.vdot(E,E).real))
    return float(np.mean(out)), float(np.std(out)/math.sqrt(shots))


def check_random_networks():
    rng=np.random.default_rng(20261010)
    res=[]
    for n in (3,4,5,8,11):
        gs=[Green.make(rng,n) for _ in range(4)]
        network=TwoByTwoGreen(gs)
        M=network.dense()
        U=unitary_fourier(n)
        twirl_exact,twirl_average = dense_twirl(n,M)
        assert np.allclose(twirl_exact,twirl_average,rtol=1e-10,atol=1e-10)
        # Directly test each recurrence against the dense inverse.
        for g in gs:
            v=rng.standard_normal(n)+1j*rng.standard_normal(n)
            assert np.linalg.norm(g.denominator()@g.apply(v)-v)<1e-9
        est,se=estimate_twirl(network,n,rng,shots=2800)
        rel=abs(est-twirl_exact)/max(twirl_exact,1e-20)
        assert rel<0.12, (n,est,twirl_exact,rel)
        seed=np.linalg.norm(M[:,0]-U[:,0]); tau=math.sqrt(twirl_exact)
        spectral=np.linalg.norm(M-U,2)
        assert spectral<=seed+2*tau+1e-9
        res.append({'n':n, 'twirl_distance_squared':twirl_exact,
                    'exhaustive_covariance_energy_half':twirl_average,
                    'blackbox_probe_estimate':est,'stderr':se,
                    'relative_probe_error':rel,
                    'seed_error':float(seed),'spectral_error':float(spectral),
                    'seed_rigidity_upper_bound':float(seed+2*tau)})
    return res


def check_cut_and_parity():
    rng=np.random.default_rng(70909)
    n=18; half=n//2; part=np.arange(0,n,2); complement=np.arange(1,n,2)
    gs=[Green.make(rng,n,ordered_blocks=(part,complement)) for _ in range(4)]
    net=TwoByTwoGreen(gs)
    M=net.dense()
    ranks=[]; b=[]
    for g in gs:
        K=np.linalg.inv(g.denominator())
        observed=int(np.linalg.matrix_rank(K[np.ix_(part,complement)],tol=1e-8))
        crossing=g.crossing(part)
        assert crossing==1 and observed==crossing
        ranks.append(observed);b.append(crossing)
    budget=sum(b)
    mrank=int(np.linalg.matrix_rank(M[np.ix_(part,complement)],tol=1e-8))
    assert mrank<=budget and budget<half
    U=unitary_fourier(n)
    sv=np.linalg.svd(U[np.ix_(part,complement)],compute_uv=False)
    assert np.max(np.abs(sv-1/math.sqrt(2)))<1e-12
    error=float(np.linalg.norm(M-U,2))
    assert error >= 1/math.sqrt(2)-1e-10
    seed=float(np.linalg.norm(M[:,0]-U[:,0]))
    lam=np.trace(U.conj().T@M)/n
    tau=float(np.linalg.norm(M-lam*U,'fro'))
    assert seed+2*tau>=1/math.sqrt(2)-1e-10
    corrected=SeedCorrected(net)
    assert np.linalg.norm(corrected.apply(np.eye(n,dtype=complex)[:,0])-U[:,0])<1e-12
    corrected_dense=np.column_stack([corrected.apply(np.eye(n,dtype=complex)[:,j]) for j in range(n)])
    corrected_rank=int(np.linalg.matrix_rank(corrected_dense[np.ix_(part,complement)],tol=1e-8))
    assert corrected_rank<=budget+1<half
    corrected_lambda=np.trace(U.conj().T@corrected_dense)/n
    corrected_tau2=float(np.linalg.norm(corrected_dense-corrected_lambda*U,'fro')**2)
    assert corrected_tau2 >= 1/8-1e-9
    return {'n':n,'cut':'even versus odd','cycle_crossings':b,
            'cut_rank_budget':budget,'actual_network_cut_rank':mrank,
            'fourier_cross_singular_values_range':[float(sv.min()),float(sv.max())],
            'guaranteed_spectral_error_floor':1/math.sqrt(2),
            'observed_network_spectral_error':error,'seed_error':seed,
            'scalar_fourier_distance':tau,
            'derived_weyl_energy_floor':max(0,1/math.sqrt(2)-seed)**2/4,
            'seed_corrected_rank':corrected_rank,
            'seed_corrected_covariance_energy_half':corrected_tau2,
            'seed_corrected_theoretical_energy_floor':0.125}



class SeedCorrected:
    """Rank-one input-column correction: O(N) application, exact Fourier first column."""
    def __init__(self, base):
        self.base=base
        self.n=base.n
        v=np.ones(self.n,dtype=complex)/np.sqrt(self.n)
        e0=np.eye(self.n,dtype=complex)[:,0]
        self.fix=v-base.apply(e0)

    def apply(self,z):
        return self.base.apply(z)+self.fix*z[0]


def graph_pass_phase_fail():
    """Exhaustively verify a graph passes all cut tests yet fails Fourier phase."""
    rng=np.random.default_rng(20261011)
    n=16
    gs=[Green.make(rng,n) for _ in range(4)]
    # Enumerating all nontrivial subsets is feasible at n=16.
    worst=100000; witness=0
    for mask in range(1,(1<<n)-1):
        vertices=[i for i in range(n) if (mask>>i)&1]
        budget=sum(g.crossing(vertices) for g in gs)
        slack=budget-min(len(vertices),n-len(vertices))
        if slack<worst:
            worst=slack;witness=mask
    assert worst>=0
    net=TwoByTwoGreen(gs)
    M=net.dense()
    U=unitary_fourier(n)
    tau2,_=dense_twirl(n,M)
    assert tau2>0.1
    return {'n':n,'subsets_checked':(1<<n)-2,'min_cut_rank_slack':worst,
            'worst_subset': [i for i in range(n) if witness>>i&1],
            'phase_error_to_scalar_fourier_fro_squared':tau2}

def ff_rank(A,q):
    a=[[int(x)%q for x in row] for row in A]
    m=len(a); n=len(a[0]) if m else 0; r=0
    for j in range(n):
        piv=next((i for i in range(r,m) if a[i][j]),None)
        if piv is None: continue
        a[r],a[piv]=a[piv],a[r]
        inv=pow(a[r][j],-1,q)
        for k in range(j,n): a[r][k]=a[r][k]*inv%q
        for i in range(m):
            if i==r:continue
            fac=a[i][j]
            if fac:
                for k in range(j,n): a[i][k]=(a[i][k]-fac*a[r][k])%q
        r+=1
        if r==m:break
    return r


def ff_green_matrix(p,w,q):
    n=len(p)
    # Build G using modular forward recurrence via direct inverse of K.
    K=[[int(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):K[i][p[i]]=(K[i][p[i]]-w[i])%q
    ext=[row+list(1 if i==j else 0 for j in range(n)) for i,row in enumerate(K)]
    for j in range(n):
        piv=next((i for i in range(j,n) if ext[i][j]%q),None)
        assert piv is not None, 'singular Green denominator'
        ext[j],ext[piv]=ext[piv],ext[j]
        inv=pow(ext[j][j],-1,q)
        ext[j]=[(x*inv)%q for x in ext[j]]
        for i in range(n):
            if i==j:continue
            fac=ext[i][j]
            if fac:ext[i]=[(x-fac*y)%q for x,y in zip(ext[i],ext[j])]
    return [row[n:] for row in ext]


def check_exact_field_cuts():
    rng=np.random.default_rng(117)
    results=[]
    for n,q in ((7,337),(11,331),(18,109)):
        # All are primes congruent to 1 mod n; exact-field tests of Green ranks.
        assert all(q%p for p in range(2,int(q**0.5)+1)) and (q-1)%n==0
        for case in range(6):
            order=rng.permutation(n)
            p=[0]*n
            for i in range(n):p[int(order[i])]=int(order[(i+1)%n])
            w=[int(x) for x in rng.integers(1,q,size=n)]
            # Change a weight if denominator is singular.
            prod=math.prod(w)%q
            if prod==1:w[0]=w[0]*2%q
            G=ff_green_matrix(p,w,q)
            sz=n//2
            P=list(map(int,rng.choice(n,size=sz,replace=False)))
            C=[j for j in range(n) if j not in P]
            rank=ff_rank([[G[i][j] for j in C] for i in P],q)
            boundary=sum(1 for i in P if p[i] not in P and w[i]%q)
            assert rank==boundary,(n,case,rank,boundary)
        results.append({'n':n,'modulus':q,'exact_cases_passed':6})
    return results



def mod_green_apply(p, w, v, q):
    n=len(p)
    order=[0]
    for _ in range(1,n):order.append(p[order[-1]])
    assert len(set(order))==n and p[order[-1]]==0
    tail=v[order[-1]]%q
    for k in range(n-2,-1,-1):
        j=order[k]
        tail=(v[j]+w[j]*tail)%q
    lam=math.prod(w)%q
    assert lam!=1
    y=[0]*n
    y[order[0]]=tail*pow((1-lam)%q,-1,q)%q
    for k in range(n-1,0,-1):
        j=order[k]
        y[j]=(v[j]+w[j]*y[p[j]])%q
    return y


def check_exact_field_one_sided_fft_gate():
    # Finite-field polynomial identity test. Acceptance is one-sided only
    # for a FIXED finite field, and rejection can be lifted to exact
    # characteristic-zero algebra when the reduction is valid.
    n=11; q=331
    omega=next(w for g in range(2,q) if (w:=pow(g,(q-1)//n,q))!=1)
    assert pow(omega,n,q)==1
    rng=np.random.default_rng(346)
    branches=[]
    for _ in range(4):
        order=list(map(int,rng.permutation(n)))
        p=[0]*n
        for j in range(n):p[order[j]]=order[(j+1)%n]
        w=list(map(int,rng.integers(1,q,size=n)))
        if math.prod(w)%q==1:w[0]=w[0]*2%q
        assert math.prod(w)%q!=1
        branches.append((p,w))
    def network(z):
        def g(t,x):return mod_green_apply(branches[t][0],branches[t][1],x,q)
        right=[(u+v)%q for u,v in zip(g(2,z),g(3,z))]
        return [(u+v)%q for u,v in zip(g(0,right),g(1,right))]
    e0=[1]+[0]*(n-1)
    adjustment=[(1-v)%q for v in network(e0)]
    def corrected(z):
        return [(a+adjustment[j]*z[0])%q for j,a in enumerate(network(z))]
    assert corrected(e0)==[1]*n
    def Fourier(z):
        return [sum(pow(omega,(k*j)%n,q)*z[j] for j in range(n))%q for k in range(n)]
    assert Fourier(e0)==[1]*n
    def covariance_errors(M,z):
        Sz=[z[(j-1)%n] for j in range(n)]
        left=M(Sz)
        right=[pow(omega,j,q)*x%q for j,x in enumerate(M(z))]
        return [(x-y)%q for x,y in zip(left,right)]
    random_tests=12
    for _ in range(random_tests):
        z=list(map(int,rng.integers(0,q,size=n)))
        assert covariance_errors(Fourier,z)==[0]*n
        # This particular non-Fourier operator has many nonzero defects.
        assert covariance_errors(corrected,z)!=[0]*n
    return {'n':n,'q':q,'root':omega,'positive_control_passed':True,
            'seed_corrected_wrong_green_rejections':random_tests,
            'max_false_accept_probability_if_residual_nonzero':q**(-random_tests)}


def column_localized_adversary():
    """A one-column defect defeats naive column sampling but not Weyl twirls.
    For this illustrative control M=U+(U e2)e1*, so U itself is not evaluated:
    Fourier portions cancel algebraically from every covariance residual.
    """
    rng=np.random.default_rng(20261012)
    n=1024; shots=128; j=1; jprime=2
    u=np.exp(-2j*np.pi*np.arange(n)*jprime/n)/math.sqrt(n)
    # ||U e2 e1*||_F^2=1, and Tr(U* (U e2 e1*))=0, so tau^2=1.
    chosen=rng.integers(n,size=shots)
    direct_samples=np.where(chosen==j,float(n),0.0)
    twirl_samples=[]
    for _ in range(shots):
        a=int(rng.integers(n));b=int(rng.integers(n))
        z=(rng.standard_normal(n)+1j*rng.standard_normal(n))/math.sqrt(2)
        ew=u*weyl(z,a,b)[j] - phiweyl(u,a,b)*z[j]
        twirl_samples.append(0.5*float(np.vdot(ew,ew).real))
    mean=float(np.mean(twirl_samples))
    assert 0.55<mean<1.45,mean
    return {'n':n,'shots':shots,'true_phase_distance_squared':1.0,
            'naive_column_hits':int(np.sum(chosen==j)),
            'naive_column_estimate':float(np.mean(direct_samples)),
            'weyl_twirl_estimate':mean,
            'naive_column_worstcase_samples_for_90pct_detection':
                math.ceil(math.log(0.1)/math.log(1-1/n))}

def main():
    out={'complex_weyl_tests':check_random_networks(),
         'parity_spectral_cut':check_cut_and_parity(),
         'graph_pass_but_wrong_fourier':graph_pass_phase_fail(),
         'single_column_error_detection':column_localized_adversary(),
         'exact_modular_green_cut_tests':check_exact_field_cuts(),
         'modular_covariance_identity_gate':check_exact_field_one_sided_fft_gate()}
    with open('RESULTS.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
