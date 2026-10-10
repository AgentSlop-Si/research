"""Independent exact assertions for hero17 delta graph.
Tests use direct O(N^2) DFT/convolution references, except a separate
radix-2 NTT reference for large N. Reference FFT is NOT part of algorithm.
"""
import unittest
import random
from delta_graph import (
    recognize,transform_certified,transform_if_recognized,balanced_q,
    make_delta_signal,batch_inverse_nonzero_phase_differences
)
from graph_convolution_delta import convolve_if_supported
from tensor_union import direct_dft,direct_dft_bins,direct_circular_convolution,root_for
from fiber_union import recognize as fiber_recognize,make_fiber_signal
import phase_union_general as phase


def matrix_rank(rows,p):
    A=[list(row) for row in rows]
    if not A:return 0
    n=len(A);m=len(A[0]);rank=0
    for c in range(m):
        pivot=next((j for j in range(rank,n) if A[j][c]),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank]
        v=pow(A[rank][c],-1,p)
        A[rank]=[z*v%p for z in A[rank]]
        for j in range(n):
            if j!=rank and A[j][c]:
                w=A[j][c]
                A[j]=[(a-w*b)%p for a,b in zip(A[j],A[rank])]
        rank+=1
        if rank==n:break
    return rank


def direct_spectrum(row,p,eta):
    m=len(row);rt=phase.phase_table(m,p,eta)
    return [sum(z*rt[(-h*u)%m] for u,z in enumerate(row))%p
            for h in range(m)]


def make_full_rank_dense(n,p,w,rng):
    q=balanced_q(n);m=n//q
    assert q<=m
    eta=pow(w,q,p)
    roots=phase.phase_table(m,p,eta)
    # Baseline deliberately uses every character with a nonzero coefficient.
    base_coeff=[rng.randrange(1,p) for _ in range(m)]
    changes=[[] for _ in range(q)]
    used={0}
    for t in range(1,q):
        h=t
        assert h<m
        c=rng.randrange(1,p)
        if (base_coeff[h]+c)%p==0:c=(c+1)%p or 1
        changes[t]=[(h,c)]
    base=[sum(base_coeff[h]*roots[(h*u)%m] for h in range(m))%p for u in range(m)]
    x=make_delta_signal(n,p,w,q,base,changes)
    return x,changes,base,base_coeff


def ntt2(a,omega,p,inverse=False):
    """TEST-ONLY completely independent radix-two NTT."""
    n=len(a)
    if n&(n-1):raise ValueError('only powers of two')
    z=list(a)
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:j^=bit;bit>>=1
        j^=bit
        if i<j:z[i],z[j]=z[j],z[i]
    L=2
    while L<=n:
        step=pow(omega,n//L,p)
        if not inverse:step=pow(step,-1,p)
        for i in range(0,n,L):
            w=1
            for j in range(L//2):
                u=z[i+j];v=z[i+j+L//2]*w%p
                z[i+j]=(u+v)%p;z[i+j+L//2]=(u-v)%p
                w=w*step%p
        L*=2
    if inverse:
        inv=pow(n,-1,p)
        z=[v*inv%p for v in z]
    return z


class DeltaGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p=65537
        cls.rng=random.Random(170217)
        cls.root_cache={n:root_for(n,cls.p) for n in [16,64,256,1024,4096,16384,65536]}

    def test_geometric_batch_inverse(self):
        n=256;p=self.p;w=self.root_cache[n]
        roots=phase.phase_table(n,p,w)
        inv=batch_inverse_nonzero_phase_differences(roots,p)
        for k in range(1,n):
            self.assertEqual((1-roots[-k])*inv[k]%p,1)

    def test_raw_generic_dense_full_rank_q_equals_m(self):
        for n in [16,64,256]:
            q=balanced_q(n);m=n//q;p=self.p;w=self.root_cache[n]
            x,changes,base,coeff=make_full_rank_dense(n,p,w,self.rng)
            self.assertEqual(q,m)
            rows=[[x[t+q*u] for u in range(m)] for t in range(q)]
            self.assertEqual(matrix_rank(rows,p),q)
            # Every fiber has dense M-point spectrum: old sparse-fiber
            # recognition fails even for constant bound r<=3.
            eta=pow(w,q,p)
            for row in rows:
                self.assertEqual(sum(z!=0 for z in direct_spectrum(row,p,eta)),m)
            self.assertIsNone(fiber_recognize(x,p,w,3,q))
            spectrum,cert=transform_if_recognized(x,p,w,1,1,q)
            self.assertIsNotNone(cert)
            self.assertEqual(spectrum,direct_dft(x,p,w))
            self.assertEqual(len(cert.anchors),1)
            self.assertEqual(len(cert.events),q-1)
            self.assertEqual(len(spectrum),n)

    def test_exact_arbitrary_baseline_and_modes(self):
        rng=self.rng;p=self.p
        for n in [16,64,256,1024]:
            w=self.root_cache[n];q=balanced_q(n);m=n//q
            for r in [1,2,3]:
                base=[rng.randrange(p) for _ in range(m)]
                changes=[[]]
                for t in range(1,q):
                    ss=rng.randrange(0,r+1)
                    hs=rng.sample(range(m),ss)
                    changes.append([(h,rng.randrange(1,p)) for h in hs])
                x=make_delta_signal(n,p,w,q,base,changes)
                spectrum,cert=transform_if_recognized(x,p,w,r,1,q)
                self.assertIsNotNone(cert,(n,r))
                self.assertEqual(spectrum,direct_dft(x,p,w),(n,r))
                self.assertLessEqual(len(cert.events),r*(q-1))

    def test_two_anchor_resets(self):
        rng=self.rng;p=self.p;n=256;w=self.root_cache[n];q=m=16
        base=[rng.randrange(p) for _ in range(m)]
        changes=[[]]+[[(t%16,rng.randrange(1,p))] for t in range(1,q)]
        reset_row=[rng.randrange(p) for _ in range(m)]
        x=make_delta_signal(n,p,w,q,base,changes,{8:reset_row})
        self.assertIsNone(recognize(x,p,w,1,1,q))
        cert=recognize(x,p,w,1,2,q)
        self.assertIsNotNone(cert)
        self.assertEqual([(s.first,s.last) for s in cert.anchors],[(0,7),(8,15)])
        self.assertEqual(len(cert.events),q-2)
        self.assertEqual(transform_certified(cert),direct_dft(x,p,w))
        out,stats=transform_certified(cert,True)
        self.assertEqual(stats['dense_frequency_updates'],2*n)
        self.assertEqual(stats['event_frequency_updates'],(q-2)*q)

    def test_fail_closed_random_dense(self):
        rng=self.rng;p=self.p;n=256;w=self.root_cache[n]
        for _ in range(100):
            x=[rng.randrange(p) for j in range(n)]
            self.assertIsNone(recognize(x,p,w,2,2))

    def test_scaling_spot_checks(self):
        p=self.p;rng=self.rng
        for n in [4096,16384,65536]:
            w=self.root_cache[n];q=balanced_q(n)
            x,_,_,_=make_full_rank_dense(n,p,w,rng)
            cert=recognize(x,p,w,1,1,q)
            self.assertIsNotNone(cert)
            output,stats=transform_certified(cert,True)
            self.assertEqual(stats['anchors'],1)
            self.assertEqual(stats['delta_events'],q-1)
            self.assertLessEqual(stats['total_frequency_updates'],2*n)
            bins=list(dict.fromkeys([0,1,2,3,q-1,q,q+1,n//2,n-2,n-1]+
                                    [rng.randrange(n) for _ in range(20)]))
            self.assertEqual([output[k] for k in bins],direct_dft_bins(x,p,w,bins))

    def test_convolution_rescue_expanse(self):
        p=self.p;n=256;w=self.root_cache[n];q=m=16;s=4
        mx=[[(t%s,1)] for t in range(q)]
        my=[[(t//s,1)] for t in range(q)]
        a=make_fiber_signal(n,p,w,q,mx)
        b=make_fiber_signal(n,p,w,q,my)
        value,info=convolve_if_supported(a,b,p,w,1,1,q,2,2)
        self.assertIsNotNone(value)
        self.assertEqual(info.method,'delta-graph')
        self.assertEqual(info.nonzero_states,s*q)
        self.assertLessEqual(info.delta_states,2*s+1)
        self.assertEqual(value,direct_circular_convolution(a,b,p))

    def test_convolution_large_reference_ntt(self):
        p=self.p;n=4096;w=self.root_cache[n];q=m=64;s=8
        a=make_fiber_signal(n,p,w,q,[[(t%s,1)] for t in range(q)])
        b=make_fiber_signal(n,p,w,q,[[(t//s,1)] for t in range(q)])
        value,info=convolve_if_supported(a,b,p,w,1,1,q,2,2)
        self.assertIsNotNone(value)
        self.assertEqual(info.method,'delta-graph')
        F=ntt2(a,w,p);G=ntt2(b,w,p)
        expected=ntt2([u*v%p for u,v in zip(F,G)],w,p,True)
        self.assertEqual(value,expected)

    def test_convolution_high_variation_rejects(self):
        rng=self.rng;p=self.p;n=4096;w=self.root_cache[n];q=m=64;s=8
        mx=[[(t%s,rng.randrange(1,p))] for t in range(q)]
        my=[[(t//s,rng.randrange(1,p))] for t in range(q)]
        a=make_fiber_signal(n,p,w,q,mx)
        b=make_fiber_signal(n,p,w,q,my)
        value,info=convolve_if_supported(a,b,p,w,1,1,q,2,2)
        self.assertIsNone(value)
        self.assertFalse(info.accepted)
        self.assertGreater(info.delta_states,2*q)

    def test_production_root_invalid_rejected(self):
        p=self.p;n=256
        x=[0]*n
        with self.assertRaises(ValueError):
            recognize(x,p,1,1,1,16)


if __name__=='__main__':unittest.main()

class BudgetVariationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from delta_graph_budget import recognize_budgeted,transform_if_recognized
        cls.recognize=staticmethod(recognize_budgeted)
        cls.compute=staticmethod(transform_if_recognized)
        cls.p=65537
        cls.rng=random.Random(181717)
        cls.omega={n:root_for(n,cls.p) for n in [64,256,1024]}

    def test_variable_mode_density(self):
        rng=self.rng;p=self.p
        for n in [64,256,1024]:
            q=balanced_q(n);m=n//q;w=self.omega[n]
            for trial in range(7):
                base=[rng.randrange(p) for _ in range(m)]
                budget=q
                changes=[[] for _ in range(q)]
                for t in range(1,q):
                    take=rng.randint(0,min(4,budget,m))
                    changes[t]=[(h,rng.randrange(1,p))
                                for h in rng.sample(range(m),take)]
                    budget-=take
                x=make_delta_signal(n,p,w,q,base,changes)
                out,cert=self.compute(x,p,w,q,1,q)
                self.assertIsNotNone(cert,(n,trial))
                self.assertLessEqual(len(cert.events),q)
                self.assertEqual(out,direct_dft(x,p,w))

    def test_single_maximally_dense_difference(self):
        rng=self.rng;p=self.p
        for n in [64,256,1024]:
            q=m=balanced_q(n);w=self.omega[n]
            base=[rng.randrange(p) for _ in range(m)]
            changes=[[] for _ in range(q)]
            # This one arbitrary M-dimensional update is permitted by
            # global budget R=M=Q. All following differences are zero.
            changes[q//2]=[(h,rng.randrange(1,p)) for h in range(m)]
            x=make_delta_signal(n,p,w,q,base,changes)
            self.assertIsNone(recognize(x,p,w,2,1,q))
            out,cert=self.compute(x,p,w,q,1,q)
            self.assertIsNotNone(cert)
            self.assertEqual(len(cert.events),m)
            self.assertEqual(out,direct_dft(x,p,w))

    def test_zero_total_budget_and_random_reject(self):
        n=256;p=self.p;w=self.omega[n];q=m=16
        row=[self.rng.randrange(p) for _ in range(m)]
        x=make_delta_signal(n,p,w,q,row,[[] for _ in range(q)])
        result,cert=self.compute(x,p,w,0,1,q)
        self.assertIsNotNone(cert)
        self.assertEqual(result,direct_dft(x,p,w))
        for _ in range(50):
            fresh=[self.rng.randrange(p) for _ in range(n)]
            self.assertIsNone(self.recognize(fresh,p,w,q,1,q))

    def test_random_dense_budget_with_reset(self):
        rng=self.rng;p=self.p;n=256;q=m=16;w=self.omega[n]
        base=[rng.randrange(p) for _ in range(m)]
        changes=[[] for _ in range(q)]
        changes[4]=[(j,rng.randrange(1,p)) for j in range(m)]
        reset=[rng.randrange(p) for _ in range(m)]
        x=make_delta_signal(n,p,w,q,base,changes,{10:reset})
        out,cert=self.compute(x,p,w,q,2,q)
        self.assertIsNotNone(cert)
        self.assertEqual(len(cert.anchors),2)
        self.assertEqual(len(cert.events),m)
        self.assertEqual(out,direct_dft(x,p,w))

class SecondDifferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from second_difference_graph import make_acceleration_signal,recognize,transform_certified,transform_if_recognized
        cls.build=staticmethod(make_acceleration_signal)
        cls.recognize=staticmethod(recognize)
        cls.compute=staticmethod(transform_if_recognized)
        cls.raw_transform=staticmethod(transform_certified)
        cls.p=65537
        cls.rng=random.Random(21555)
        cls.omega={n:root_for(n,cls.p) for n in [16,64,256,1024,4096,16384]}

    def test_random_acceleration_exact(self):
        rng=self.rng;p=self.p
        for n in [16,64,256,1024]:
            w=self.omega[n];q=balanced_q(n);m=n//q
            for trial in range(5):
                row0=[rng.randrange(p) for _ in range(m)]
                row1=[rng.randrange(p) for _ in range(m)]
                events=[[] for _ in range(q)]
                budget=q
                for t in range(2,q):
                    count=rng.randrange(0,min(4,budget,m)+1)
                    events[t]=[(h,rng.randrange(1,p)) for h in rng.sample(range(m),count)]
                    budget-=count
                x=self.build(n,p,w,q,row0,row1,events)
                actual,cert=self.compute(x,p,w,q,q)
                self.assertIsNotNone(cert,(n,trial))
                self.assertEqual(actual,direct_dft(x,p,w),(n,trial))

    def test_affine_base_has_dense_transitions(self):
        rng=self.rng;p=self.p;n=256;q=m=16;w=self.omega[n]
        roots=phase.phase_table(m,p,pow(w,q,p))
        coeff0=[10+h for h in range(m)]
        coeff_slope=[100+h for h in range(m)]
        row0=[sum(coeff0[h]*roots[h*u%m] for h in range(m))%p for u in range(m)]
        row1=[sum((coeff0[h]+coeff_slope[h])*roots[h*u%m]
                 for h in range(m))%p for u in range(m)]
        changes=[[] for _ in range(q)]
        for t in range(2,q):changes[t]=[(t,2)]
        x=self.build(n,p,w,q,row0,row1,changes)
        rows=[[x[t+q*u] for u in range(m)] for t in range(q)]
        self.assertEqual(matrix_rank(rows,p),q)
        self.assertTrue(all(all(direct_spectrum(row,p,roots[1])) for row in rows))
        from delta_graph_budget import recognize_budgeted
        self.assertIsNone(recognize_budgeted(x,p,w,q,1,q))
        actual,cert=self.compute(x,p,w,q,q)
        self.assertIsNotNone(cert)
        self.assertEqual(len(cert.events),q-2)
        self.assertEqual(actual,direct_dft(x,p,w))

    def test_spot_large(self):
        rng=self.rng;p=self.p
        for n in [4096,16384]:
            q=balanced_q(n);m=n//q;w=self.omega[n]
            row0=[rng.randrange(p) for _ in range(m)]
            row1=[rng.randrange(p) for _ in range(m)]
            events=[[] for _ in range(q)]
            for t in range(2,q):events[t]=[(t%m,3+t)]
            x=self.build(n,p,w,q,row0,row1,events)
            cert=self.recognize(x,p,w,q,q)
            self.assertIsNotNone(cert)
            out,info=self.raw_transform(cert,True)
            self.assertLessEqual(info['initial_updates']+info['event_updates'],2*n)
            bins=list(dict.fromkeys([0,1,2,q-1,q,q+1,n-1]+[rng.randrange(n) for _ in range(30)]))
            self.assertEqual([out[k] for k in bins],direct_dft_bins(x,p,w,bins))

    def test_dense_random_rejection(self):
        rng=self.rng;p=self.p;n=256;w=self.omega[n]
        for _ in range(50):
            x=[rng.randrange(p) for _ in range(n)]
            self.assertIsNone(self.recognize(x,p,w,16,16))

class NewtonUnionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from newton_union import recognize,transform_certified,transform_if_recognized,build_newton_signal,truncated_binomial_geometric
        cls.recognize=staticmethod(recognize)
        cls.transform=staticmethod(transform_certified)
        cls.compute=staticmethod(transform_if_recognized)
        cls.make=staticmethod(build_newton_signal)
        cls.kernel=staticmethod(truncated_binomial_geometric)
        cls.p=65537
        cls.rng=random.Random(171717)
        cls.w={n:root_for(n,cls.p) for n in [16,64,256,1024,4096]}

    def test_kernel_exhaustive_short(self):
        p=self.p
        for z in [0,1,2,3,144,1234,p-1]:
            iv=pow((1-z)%p,-1,p) if z!=1 else 0
            for d in range(1,7):
                for L in range(0,22):
                    got=self.kernel(z,L,d,p,iv,pow(z,L,p))
                    want=sum(__import__('math').comb(v+d-1,d-1)*pow(z,v,p)
                             for v in range(L))%p
                    self.assertEqual(got,want,(z,d,L))

    def test_newton_any_fixed_order(self):
        rng=self.rng;p=self.p
        for n in [16,64,256,1024]:
            w=self.w[n];q=balanced_q(n);m=n//q
            for d in range(1,min(4,q)+1):
                for rep in range(4):
                    initial=[[rng.randrange(p) for _ in range(m)] for _ in range(d)]
                    changes=[[] for _ in range(q)]
                    R=q
                    for t in range(d,q):
                        cnt=rng.randrange(min(3,R,m)+1)
                        changes[t]=[(h,rng.randrange(1,p))
                                    for h in rng.sample(range(m),cnt)]
                        R-=cnt
                    x=self.make(n,p,w,q,d,initial,changes)
                    y,cert=self.compute(x,p,w,d,q,q)
                    self.assertIsNotNone(cert,(n,d,rep))
                    self.assertEqual(y,direct_dft(x,p,w),(n,d,rep))

    def test_newton_first_and_second_agree_prior_executors(self):
        rng=self.rng;p=self.p;n=256;w=self.w[n];q=m=16
        initial=[[rng.randrange(p) for _ in range(m)] for _ in range(2)]
        events=[[] for _ in range(q)]
        for t in range(2,q):events[t]=[(t,5+t)]
        x=self.make(n,p,w,q,2,initial,events)
        from second_difference_graph import transform_if_recognized as second
        y1,c1=self.compute(x,p,w,2,q,q)
        y2,c2=second(x,p,w,q,q)
        self.assertIsNotNone(c1);self.assertIsNotNone(c2)
        self.assertEqual(y1,y2)
        self.assertEqual(y1,direct_dft(x,p,w))

    def test_newton_full_rank_dense_q_by_m(self):
        p=self.p;n=256;q=m=16;d=3;w=self.w[n]
        roots=phase.phase_table(m,p,pow(w,q,p))
        init=[]
        # Three arbitrary dense M-spectra, linearly independent on h=0,1,2.
        for t in range(d):
            coeff=[(23+3*h+h*h+(t+1)**(h%3))%p for h in range(m)]
            init.append([sum(coeff[h]*roots[(h*u)%m] for h in range(m))%p
                         for u in range(m)])
        delta=[[] for _ in range(q)]
        for t in range(d,q):delta[t]=[(t,2)]
        x=self.make(n,p,w,q,d,init,delta)
        rows=[[x[t+q*u] for u in range(m)] for t in range(q)]
        self.assertEqual(matrix_rank(rows,p),q)
        y,cert=self.compute(x,p,w,d,q,q)
        self.assertIsNotNone(cert)
        self.assertEqual(y,direct_dft(x,p,w))

    def test_newton_random_dense_reject(self):
        p=self.p;n=256;w=self.w[n]
        for d in [1,2,3,4]:
            for _ in range(25):
                x=[self.rng.randrange(p) for _ in range(n)]
                self.assertIsNone(self.recognize(x,p,w,d,16,16))

    def test_newton_large_spot(self):
        rng=self.rng;p=self.p;n=4096;w=self.w[n];q=m=64;d=4
        init=[[rng.randrange(p) for _ in range(m)] for _ in range(d)]
        events=[[] for _ in range(q)]
        for t in range(d,q):events[t]=[(t,3+t)]
        x=self.make(n,p,w,q,d,init,events)
        cert=self.recognize(x,p,w,d,q,q)
        self.assertIsNotNone(cert)
        y,info=self.transform(cert,True)
        self.assertLessEqual(info['event_terms'],n)
        bins=[0,1,63,64,65,2048,4095]+[rng.randrange(n) for _ in range(25)]
        self.assertEqual([y[k] for k in bins],direct_dft_bins(x,p,w,bins))
