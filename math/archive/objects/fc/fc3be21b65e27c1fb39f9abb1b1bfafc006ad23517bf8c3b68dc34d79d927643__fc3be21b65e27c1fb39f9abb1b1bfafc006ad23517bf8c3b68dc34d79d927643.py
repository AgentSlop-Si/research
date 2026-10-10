#!/usr/bin/env python3
"""Independent finite-field verification for Phase 9. Non-fallback exact equality."""
from __future__ import annotations
import unittest, random
from phase9_dense_cycle import (
    P, Costs, make_dense_cycle, exact_dense_cycle_with_innovations,
    exact_reference_dft, berlekamp_massey, decode_sparse_syndromes,
    probabilistic_verify, learn_eigenvalues, find_innovations,
    root_of_unity,
)
from phase8_weyl_cycle import exact_ntt


def matrix_rank_mod(matrix):
    if not matrix:return 0
    a=[row[:] for row in matrix];rows=len(a);cols=len(a[0]);r=0
    for j in range(cols):
        p=next((i for i in range(r,rows) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        factor=pow(a[r][j],P-2,P)
        for k in range(j,cols):a[r][k]=a[r][k]*factor%P
        for i in range(r+1,rows):
            z=a[i][j]
            if z:
                for k in range(j,cols):a[i][k]=(a[i][k]-z*a[r][k])%P
        r+=1
        if r==rows:break
    return r


def quadratic_reference(x):
    n=len(x);wn=root_of_unity(n)
    table=[pow(wn,-a% n,P) for a in range(n)]
    return [sum(x[b]*table[a*b %n] for b in range(n))%P for a in range(n)]


class Phase9Tests(unittest.TestCase):
    def run_case(self,k,m,innov,s,seed,expect_mode=None,lam_override=None):
        x,metadata=make_dense_cycle(k,m,innov,seed,lam_override)
        answer,cert,counts=exact_dense_cycle_with_innovations(
            x,m,s,3,3,Costs(),random.Random(991+seed),True)
        self.assertIsNotNone(answer,f'{k},{m},{s},{cert}')
        self.assertEqual(answer,exact_reference_dft(x))
        if k*m<=128:self.assertEqual(answer,quadratic_reference(x))
        if expect_mode:self.assertEqual(cert['mode'],expect_mode)
        self.assertEqual(cert['innovation_total'],sum(map(len,innov.values())))
        self.assertEqual(cert['verification_rounds'],3)
        return x,metadata,cert,counts

    def test_a_dense_controller_no_errors(self):
        for k,m in [(8,4),(16,8),(32,8),(64,8),(64,16),
                    (128,8),(128,16),(256,16),(512,16)]:
            for seed in range(3):
                _,meta,cert,c=self.run_case(k,m,{},0,seed,'direct-geometric')
                self.assertTrue(all(v!=0 for v in meta['kernel_c']))
                self.assertEqual(cert['innovation_total'],0)

    def test_b_constant_total_error_exact_linear_mode(self):
        for k,m in [(16,8),(32,8),(64,16),(128,16),(256,16)]:
            for seed in range(4):
                rng=random.Random(seed*93+k)
                event_t=rng.randrange(1,m-1)
                innovations={event_t:[(b,rng.randrange(1,P)) for b in rng.sample(range(k),2)]}
                self.run_case(k,m,innovations,2,seed,'direct-geometric')

    def test_c_errors_every_step_short_ntt_mode(self):
        for k,m in [(16,8),(32,8),(64,8),(64,16),(128,16),(256,16)]:
            for s in (1,2,3):
                rng=random.Random(k*11+m*17+s)
                errors={t:[(b,rng.randrange(1,P)) for b in rng.sample(range(k),s)]
                        for t in range(1,m-1)}
                self.run_case(k,m,errors,s,42+s,'batched-small-NTT')

    def test_d_singular_denominators_are_exact(self):
        for k,m in [(16,8),(32,8),(64,16)]:
            n=k*m;wn=root_of_unity(n)
            rng=random.Random(k+m)
            lam=[rng.randrange(1,P) for _ in range(k)]
            lam[0]=1
            lam[1]=pow(wn,1+k,P)   # singular at output ell=1,j=1
            errors={t:[((t*5+2)%k,1000+t)] for t in range(1,m-1)}
            self.run_case(k,m,errors,1,83,'batched-small-NTT',lam)
            self.run_case(k,m,{1:[(5,123)]},1,83,'direct-geometric',lam)

    def test_e_random_arbitrary_rejected(self):
        for k,m in [(16,8),(32,8),(64,16)]:
            rng=random.Random(500+k+m)
            for _ in range(12):
                raw=[rng.randrange(P) for _ in range(k*m)]
                z,cert,_=exact_dense_cycle_with_innovations(
                    raw,m,2,None,3,Costs(),rng,True)
                self.assertIsNone(z)
                self.assertFalse(cert['accepted'])

    def test_f_excess_sparse_errors_rejected(self):
        k,m=64,16
        x,_=make_dense_cycle(k,m,{7:[(2,123),(9,456),(17,777)]},seed=37)
        z,cert,_=exact_dense_cycle_with_innovations(x,m,1,None,3,Costs(),random.Random(33),True)
        self.assertIsNone(z)

    def test_g_nonzero_dense_kernel_and_full_column_rank(self):
        k,m=32,8
        x,meta=make_dense_cycle(k,m,{},seed=55)
        c=meta['kernel_c'];lam=meta['lambda']
        self.assertEqual(len(set(lam)),k)
        self.assertEqual(sum(int(v!=0) for v in c),k)
        cols=[[x[b*m+t] for b in range(k)] for t in range(m)]
        self.assertEqual(matrix_rank_mod(list(map(list,zip(*cols)))),m)
        for t in range(m-1):
            for b in range(k):
                expected=sum(c[d]*cols[t][(b+d)%k] for d in range(k))%P
                self.assertEqual(cols[t+1][b],expected)
        self.assertEqual(self.run_case(k,m,{},0,55)[2]['lambda_nonzero'],k)

    def test_h_syndrome_alias_requires_fingerprint(self):
        k,m=32,8
        x,meta=make_dense_cycle(k,m,{},seed=9)
        wn=root_of_unity(k);theta=[pow(wn,-j%k,P) for j in range(3)]
        amps=[(theta[1]-theta[2])%P,(theta[2]-theta[0])%P,
              (theta[0]-theta[1])%P]
        self.assertEqual(sum(amps)%P,0)
        self.assertEqual(sum(a*t for a,t in zip(amps,theta))%P,0)
        corrupted=x[:]
        for b,a in enumerate(amps):corrupted[b*m+3]=(corrupted[b*m+3]+a)%P
        cols=[[corrupted[b*m+t] for b in range(k)] for t in range(m)]
        f0,lam,tab=learn_eigenvalues(cols,k*m,Costs())
        ev=find_innovations(cols,lam,tab,1,Costs())
        self.assertEqual(sum(map(len,ev)),0)  # deliberately invisible to 2 probes!
        self.assertFalse(probabilistic_verify(cols,lam,ev,tab,m,Costs(),3,random.Random(281)))
        z,cert,_=exact_dense_cycle_with_innovations(
            corrupted,m,1,None,3,Costs(),random.Random(281),True)
        self.assertIsNone(z)
        self.assertEqual(cert['reason'],'independent recurrence fingerprint failed')

    def test_i_prony_recovers_two_spikes(self):
        k=32;root=pow(root_of_unity(k),P-2,P)
        for s in (0,1,2,3):
            for seed in range(25):
                rng=random.Random(330+seed+31*s)
                locs=rng.sample(range(k),s)
                amps=[rng.randrange(1,P) for _ in range(s)]
                syndrome=[sum(a*pow(root,b*ell,P) for b,a in zip(locs,amps))%P
                          for ell in range(6)]
                decoded=decode_sparse_syndromes(syndrome,k,root,3,Costs())
                self.assertEqual(sorted(decoded),sorted(zip(locs,amps)))

    def test_j_one_singular_and_one_event_with_direct_limit(self):
        k,m=32,8;n=k*m;w=root_of_unity(n)
        rng=random.Random(983)
        lam=[rng.randrange(1,P) for _ in range(k)]
        lam[3]=pow(w,3+4*k,P)
        self.run_case(k,m,{m-2:[(7,997)]},1,2,'direct-geometric',lam)


if __name__=='__main__':unittest.main(verbosity=2)
