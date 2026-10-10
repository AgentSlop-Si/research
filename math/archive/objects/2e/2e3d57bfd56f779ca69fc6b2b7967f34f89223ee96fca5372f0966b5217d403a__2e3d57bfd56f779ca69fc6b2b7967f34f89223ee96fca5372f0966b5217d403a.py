#!/usr/bin/env python3
"""Phase9B dual sparse innovations: independent exact NTT & adversarial tests."""
from __future__ import annotations
import random,unittest
from phase9_dense_cycle import P,Costs,exact_reference_dft,root_of_unity
from phase9_spectral_innovations import (
    make_spectral_cycle, exact_spectral_innovation_cycle,
    recover_spectral_innovations, verify_spectral_innovations)
from phase9_dense_cycle import learn_eigenvalues
from test_phase9 import quadratic_reference,matrix_rank_mod

class SpectralTests(unittest.TestCase):
    def check(self,k,m,events,seed=17,lam_override=None):
        x,meta=make_spectral_cycle(k,m,events,seed,lam_override)
        answer,cert,c=exact_spectral_innovation_cycle(
            x,m,max((len(u) for u in events.values()),default=0),3,
            Costs(),random.Random(seed+990),True)
        self.assertIsNotNone(answer,cert)
        self.assertEqual(answer,exact_reference_dft(x))
        if k*m<=128:self.assertEqual(answer,quadratic_reference(x))
        self.assertEqual(cert['total_innovation_modes'],sum(map(len,events.values())))
        return x,meta,cert,c

    def test_a_dense_error_every_transition(self):
        for k,m in [(16,8),(32,8),(64,8),(64,16),(128,16),(256,16),(512,16)]:
            for s in (0,1,2,3):
                rng=random.Random(k*317+m*23+s)
                events={t:[(e,rng.randrange(1,P)) for e in rng.sample(range(k),s)]
                        for t in range(1,m-1)} if s else {}
                self.check(k,m,events,seed=11+s)

    def test_b_exact_singular_denominator(self):
        for k,m in [(16,8),(32,8),(64,16)]:
            n=k*m;w=root_of_unity(n);rng=random.Random(k)
            lam=[rng.randrange(1,P) for _ in range(k)]
            lam[0]=1
            lam[1]=pow(w,1+k,P)
            ev={t:[((2*t+3)%k,100+t)] for t in range(1,m-1)}
            self.check(k,m,ev,seed=40,lam_override=lam)

    def test_c_one_fourier_mode_is_dense_position_innovation(self):
        k,m=32,8
        events={t:[(t+1,t+33)] for t in range(1,m-1)}
        x,meta,cert,c=self.check(k,m,events)
        w=root_of_unity(k)
        for t in range(1,m-1):
            ell,val=events[t][0]
            coeff=val*pow(k,P-2,P)%P
            err=[coeff*pow(w,ell*b,P)%P for b in range(k)]
            self.assertEqual(sum(z!=0 for z in err),k)
        self.assertTrue(all(meta['kernel']))
        self.assertEqual(len(set(meta['lambda'])),k)

    def test_d_generic_inputs_rejected(self):
        for k,m in [(16,8),(64,8),(128,16)]:
            rng=random.Random(k+m)
            for i in range(14):
                x=[rng.randrange(P) for _ in range(k*m)]
                y,cert,_=exact_spectral_innovation_cycle(x,m,2,3,Costs(),rng,True)
                self.assertIsNone(y)

    def test_e_more_modes_than_budget_rejected(self):
        k,m=64,16
        rng=random.Random(378)
        events={5:[(a,rng.randrange(1,P)) for a in (2,7,19,36)]}
        x,_=make_spectral_cycle(k,m,events,7)
        y,cert,_=exact_spectral_innovation_cycle(
            x,m,1,3,Costs(),random.Random(992),True)
        self.assertIsNone(y)

    def test_f_invisible_probes_detected_by_freivalds(self):
        k,m=32,8;n=k*m
        x,meta=make_spectral_cycle(k,m,{},10)
        w=root_of_unity(k)
        nodes=[pow(w,z,P) for z in range(3)]
        amps=[(nodes[1]-nodes[2])%P,(nodes[2]-nodes[0])%P,
              (nodes[0]-nodes[1])%P]
        self.assertEqual(sum(amps)%P,0)
        self.assertEqual(sum(a*r for a,r in zip(amps,nodes))%P,0)
        # Inject 3-mode error at final column only, so no later residual.
        mutated=x[:]
        for b in range(k):
            e=sum(a*pow(node,b,P) for a,node in zip(amps,nodes))%P
            mutated[b*m+m-1]=(mutated[b*m+m-1]+e)%P
        cols=[[mutated[b*m+t] for b in range(k)] for t in range(m)]
        f0,lam,tab=learn_eigenvalues(cols,n,Costs())
        ev=recover_spectral_innovations(cols,lam,tab,1,Costs())
        self.assertEqual(sum(map(len,ev)),0) # invisible to two spatial probes
        self.assertFalse(verify_spectral_innovations(
            cols,lam,ev,tab,m,Costs(),3,random.Random(448)))
        y,cert,_=exact_spectral_innovation_cycle(
            mutated,m,1,3,Costs(),random.Random(448),True)
        self.assertIsNone(y)
        self.assertEqual(cert['reason'],'independent recurrence fingerprint failed')

    def test_g_finite_size_full_rank_witness(self):
        k,m=16,8
        rng=random.Random(17)
        events={t:[((t+1)%k,rng.randrange(1,P))] for t in range(1,m-1)}
        x,meta,cert,c=self.check(k,m,events,123)
        columns=[[x[b*m+t] for t in range(m)] for b in range(k)]
        self.assertEqual(matrix_rank_mod(columns),m)
        self.assertEqual(matrix_rank_mod([[x[i+j] for j in range(k*m//2)]
                                         for i in range(k*m//2)]),k*m//2)
        self.assertTrue(all(x))

if __name__=='__main__':unittest.main(verbosity=2)
