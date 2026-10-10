import unittest,random,json,math
from phase8_weyl_cycle import (P,Costs,root_of_unity,cyclic_linear_synthesize,
    exact_circulant_cycle,exact_weyl_dynamic,synthesize_time_weyl,
    full_ntt_oracle,direct_dft_oracle,roots,solve_coeffs,batch_inverse_nonzero,exact_unknown_shift_cycle,exact_circulant_rational_cycle,synthesize_circulant_order)

class TestPhase8(unittest.TestCase):
    def test_coefficients_linear_system(self):
        # Out-of-order pivots + degenerate cases.
        eqs=[([0,1],5),([1,1],8),([2,1],11),([2,0],6)]
        self.assertEqual(solve_coeffs(eqs,2),[3,5])
        self.assertIsNone(solve_coeffs(eqs+[([0,0],1)],2))
        self.assertEqual(solve_coeffs([([0,0],0)],2),[0,0])
    def test_batch_inverse(self):
        rng=random.Random(714)
        for n in (1,2,3,17,500):
            vec=[rng.randrange(1,P) for _ in range(n)]
            costs=Costs(); actual=batch_inverse_nonzero(vec,costs)
            self.assertEqual(costs.inversions,1)
            self.assertEqual([(a*b)%P for a,b in zip(vec,actual)],[1]*n)
    def test_oracle_direct(self):
        rng=random.Random(3)
        for n in (8,16,32,64):
            for _ in range(2):
                v=[rng.randrange(P) for _ in range(n)]
                self.assertEqual(full_ntt_oracle(v),direct_dft_oracle(v))
    def test_exact_circulant_all_outputs(self):
        rng=random.Random(5524)
        cases=0
        for k,m in [(8,2),(8,4),(16,4),(16,8),(32,4),(32,8),(64,8),(128,8),(256,16),(512,16)]:
            for shift in [(0,1),(0,2),(1,3)]:
                for tcase in range(4):
                    seed=[rng.randrange(P) for _ in range(k)]
                    tap=[rng.randrange(P) for _ in range(2)]
                    if tcase==0:tap=[1,0]  # includes zero-eigenvalue/denerate modes
                    if tcase==1:tap=[0,1]
                    x=cyclic_linear_synthesize(seed,m,tap,shift)
                    c=Costs(); out,info,c=exact_circulant_cycle(x,m,shift,c,True)
                    self.assertTrue(info['accepted'],info)
                    self.assertEqual(out,full_ntt_oracle(x),(k,m,shift,tap))
                    self.assertLessEqual(c.inversions,4)
                    cases+=1
        print('circulant exact cases',cases)
    def test_circulant_rejection(self):
        rng=random.Random(815)
        for k,m in [(16,8),(32,8),(64,8),(128,16)]:
            seed=[rng.randrange(1,P) for _ in range(k)]
            x=cyclic_linear_synthesize(seed,m,[2,3],(0,1))
            for idx in (1, k*m-1, (k//2)*m+1):
                y=x[:];y[idx]=(y[idx]+1)%P
                out,info,_=exact_circulant_cycle(y,m,(0,1),return_certificate=True)
                self.assertFalse(info['accepted'],(k,m,idx))
            y=[rng.randrange(P) for _ in range(k*m)]
            self.assertIsNone(exact_circulant_cycle(y,m,(0,1)))
    def test_unknown_shift_recovery(self):
        rng=random.Random(842)
        count=0
        for k,m in [(16,4),(16,8),(32,8),(64,8),(128,16),(256,16),(512,16)]:
            for d in [1,2,k//2-1,k//2+1,k-1]:
                for _ in range(4):
                    seed=[rng.randrange(1,P) for _ in range(k)]
                    c0=rng.randrange(1,P); c1=rng.randrange(1,P)
                    x=cyclic_linear_synthesize(seed,m,[c0,c1],(0,d))
                    cnt=Costs();result,cert,cnt=exact_unknown_shift_cycle(x,m,cnt,True)
                    self.assertTrue(cert['accepted'],(k,m,d,cert))
                    self.assertEqual(cert['inferred_shift'],d)
                    self.assertEqual(result,full_ntt_oracle(x))
                    count+=1
        print('unknown-shift exact recovered cases',count)
    def test_unknown_shift_scalar_and_rejection(self):
        rng=random.Random(841)
        k,m=64,8
        v=[rng.randrange(1,P) for _ in range(k)]
        x=cyclic_linear_synthesize(v,m,[71],(0,))
        got,cert,_=exact_unknown_shift_cycle(x,m,return_certificate=True)
        self.assertTrue(cert['accepted'])
        self.assertEqual(got,full_ntt_oracle(x))
        x=cyclic_linear_synthesize(v,m,[71,99],(0,19))
        x[5*m+5]=(x[5*m+5]+1)%P
        got,cert,_=exact_unknown_shift_cycle(x,m,return_certificate=True)
        self.assertIsNone(got)
        self.assertFalse(cert['accepted'])
    def test_rational_order2_and_3(self):
        rng=random.Random(934)
        count=0
        for k,m in [(8,4),(16,4),(16,8),(32,8),(64,8),(64,16),(128,16)]:
            for r in (2,3):
                for _ in range(5):
                    init=[[rng.randrange(P) for _ in range(k)] for __ in range(r)]
                    taps=[[rng.randrange(P) for _ in range(2)] for j in range(r)]
                    x=synthesize_circulant_order(init,m,taps,(0,1))
                    c=Costs()
                    got,cert,c=exact_circulant_rational_cycle(x,m,r,c=c,return_certificate=True)
                    self.assertTrue(cert['accepted'])
                    self.assertEqual(got,full_ntt_oracle(x),(k,m,r,taps))
                    self.assertLessEqual(cert['singular_outputs'],r*k)
                    count+=1
        print('rational order 2/3 exact cases',count)
    def test_rational_singular_outputs_and_reject(self):
        rng=random.Random(233)
        k,m=32,8
        init=[[rng.randrange(1,P) for _ in range(k)] for _ in range(2)]
        # Every frequency has D(z)=1-z if controls chosen as lag1 I.
        x=synthesize_circulant_order(init,m,[[1,0],[0,0]],(0,1))
        got,cert,_=exact_circulant_rational_cycle(x,m,2,return_certificate=True)
        self.assertEqual(got,full_ntt_oracle(x))
        self.assertGreaterEqual(cert['singular_outputs'],1)
        x[(k-2)*m+m-1]=(x[(k-2)*m+m-1]+1)%P
        got,cert,_=exact_circulant_rational_cycle(x,m,2,return_certificate=True)
        self.assertIsNone(got)
        self.assertFalse(cert['accepted'])
    def test_genuine_noncommutation(self):
        k=32;w=root_of_unity(k)
        v=list(range(1,k+1))
        SD=[pow(w,(b+1)%k,P)*v[(b+1)%k]%P for b in range(k)]
        DS=[pow(w,b,P)*v[(b+1)%k]%P for b in range(k)]
        self.assertNotEqual(SD,DS)
        self.assertEqual(SD,[w*z%P for z in DS])
    def test_weyl_full_exact(self):
        rng=random.Random(9431)
        cases=0
        for k,m in [(8,4),(16,4),(16,8),(32,8),(64,8),(128,8),(128,16)]:
            n=k*m;wk=root_of_unity(k)
            for dic in [[(1,0),(0,1)],[(1,0),(0,2)],[(1,1),(2,0)]]:
                for sample in range(4):
                    seed=[rng.randrange(P) for _ in range(k)]
                    controls=[[rng.randrange(1,P),rng.randrange(1,P)] for _ in range(m-1)]
                    x=synthesize_time_weyl(seed,m,dic,controls,wk)
                    c=Costs();out,cert,c=exact_weyl_dynamic(x,m,dic,c,True)
                    self.assertTrue(cert['accepted'],(k,m,dic))
                    self.assertEqual(out,full_ntt_oracle(x),(k,m,dic,sample))
                    cases+=1
        print('noncommuting Weyl exact cases',cases)
    def test_weyl_rejection(self):
        rng=random.Random(471)
        for k,m in [(16,8),(32,8),(64,8)]:
            wk=root_of_unity(k)
            x=synthesize_time_weyl([rng.randrange(1,P) for _ in range(k)],m,
                 [(1,0),(0,1)],[[1,1] for _ in range(m-1)],wk)
            x[(m//2)*k+4]=(x[(m//2)*k+4]+1)%P
            result,cert,_=exact_weyl_dynamic(x,m,return_certificate=True)
            self.assertIsNone(result)
            self.assertFalse(cert['accepted'])
    def test_cost_scaling(self):
        rng=random.Random(29)
        records=[]
        for n,m in [(256,8),(512,8),(1024,8),(2048,8),(4096,16),(8192,16),(16384,16),(32768,16),(65536,16)]:
            k=n//m
            x=cyclic_linear_synthesize([rng.randrange(P) for _ in range(k)],m,[31,17],(0,1))
            c=Costs();y,cert,c=exact_circulant_cycle(x,m,c=c,return_certificate=True)
            self.assertTrue(cert['accepted'])
            if n<=4096:self.assertEqual(y,full_ntt_oracle(x))
            records.append({'n':n,'m':m,'k':k,'total_ops':c.total(),
                    'ops_per_input':round(c.total()/n,3),'inversions':c.inversions,
                    'field_adds':c.adds,'field_mults':c.mults})
        with open('COUNTS.json','w') as f:json.dump(records,f,indent=2)
        print('cost scaling',records)

if __name__=='__main__':unittest.main(verbosity=2)
