"""Exact, independent regression tests for the CRT deferred graph."""
import unittest,random
from gt3_deferred import (DeferredGT3,ct3_baseline,base_radix2_full,
                          primitive_roots,direct_dft,TripleCodelet)
from entropy_gate import entropy_trajectory

class TestGT3(unittest.TestCase):
    def test_exact_all_lengths_and_field_choices(self):
        for p,g,lengths in [(2013265921,31,(6,12,24,48,96,192,384)),
                             (97,5,(6,12,24,48,96))]:
            for n in lengths:
                e=DeferredGT3(list(range(n)),p,g)
                oracle=direct_dft(list(range(n)),e.omega,p)
                self.assertEqual(e.full(),oracle)
                ct,cost=ct3_baseline(list(range(n)),p,g)
                self.assertEqual(ct,oracle)
                self.assertEqual(e.stats()['arithmetic'],e.predicted_full_arithmetic())
                self.assertEqual(cost.arithmetic()-e.stats()['arithmetic'],2*(n//3-1))

    def test_arbitrary_query_sets_and_exact_no_recomputation(self):
        for n in (6,12,24,48,96,192):
            rng=random.Random(251+n)
            x=[rng.randrange(2013265921) for _ in range(n)]
            ref=direct_dft(x,primitive_roots(n,2013265921,31),2013265921)
            for test in range(15):
                wanted=rng.sample(range(n),rng.randrange(1,n+1))
                if test==0:wanted=[n-1]
                elif test==1:wanted=list(range(n))
                s=DeferredGT3(x)
                self.assertEqual(s.preview(wanted),{k:ref[k] for k in wanted})
                jset={s.k_to_grid(k)[0] for k in wanted}
                self.assertEqual(s.stats()['peak_backup_words'],n-3*len(jset))
                self.assertEqual(s.full(),ref)
                self.assertEqual(s.stats()['arithmetic'],s.predicted_full_arithmetic())
                self.assertEqual(s.stats()['backup_current'],0)
                self.assertEqual(s.preview_done,True)

    def test_codelet_partial_all_subsets(self):
        p=2013265921
        eta=primitive_roots(3,p,31)
        rng=random.Random(253)
        for _ in range(40):
            a,b,c=[rng.randrange(p) for j in range(3)]
            direct=[(a+b*pow(eta,k,p)+c*pow(eta,2*k,p))%p for k in range(3)]
            for mask in range(1,8):
                code=TripleCodelet(a,b,c,p,eta)
                keys=[k for k in range(3) if mask&(1<<k)]
                for k in keys:self.assertEqual(code.get(k),direct[k])
                self.assertEqual(code.full(),direct)
                self.assertEqual(code.cnt.arithmetic(),8)
                self.assertEqual(code.cnt.additions,6)
                self.assertEqual(code.cnt.multiplications,2)

    def test_batched_preview_exact_counts(self):
        for n in (48,96,384,768,1536):
            G=n//3
            e=DeferredGT3([1]*n)
            want=sorted(set(list(range(10))+[n-1]))
            out=e.preview(want)
            self.assertEqual(out[0],n)
            self.assertTrue(all(out[k]==0 for k in want if k))
            self.assertLessEqual(e.stats()['arithmetic'],e.predicted_full_arithmetic())
            self.assertEqual(e.full(),[n]+[0]*(n-1))
            self.assertEqual(e.stats()['arithmetic'],e.predicted_full_arithmetic())

    def test_errors_not_accepted(self):
        with self.assertRaises(ValueError):DeferredGT3([1]*25)
        with self.assertRaises(ValueError):DeferredGT3([1]*3)
        with self.assertRaises(ValueError):DeferredGT3([1]*30)
        s=DeferredGT3([0]*48)
        with self.assertRaises(ValueError):s.preview([-1])
        with self.assertRaises(ValueError):s.preview([])
        s.preview([0])
        with self.assertRaises(ValueError):s.preview([1])
        self.assertEqual(s.full(),[0]*48)

    def test_unitary_entropy_saturation(self):
        for n in (2,4,8,16,32):
            t=entropy_trajectory(n)
            self.assertEqual(t['gate_count'],t['known_unitary_lower_bound'])
            self.assertLess(t['max_column_l2_deviation'],1e-12)
            self.assertTrue(all(abs(v-i*n)<1e-8 for i,v in enumerate(t['entropies'])))

if __name__=='__main__':unittest.main()
