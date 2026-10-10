import unittest,random,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from phase23_resolvent import *

# Independent radix-two NTT / C = Q^-1 H^T F reference executor.
def reference_c(x:list[int])->list[int]:
    n=len(x);w=root(n);a=[t%P for t in x]
    j=0
    for i in range(1,n):
        k=n>>1
        while j&k:j^=k;k>>=1
        j^=k
        if i<j:a[i],a[j]=a[j],a[i]
    length=2
    while length<=n:
        wn=pow(w,n//length,P)
        for lo in range(0,n,length):
            t=1
            for k in range(length//2):
                u=a[lo+k];v=a[lo+k+length//2]*t%P
                a[lo+k]=(u+v)%P;a[lo+k+length//2]=(u-v)%P
                t=t*wn%P
        length*=2
    scale=pow(sqrt_mod(n),-1,P)
    a=[v*scale%P for v in a]
    h=n//2;is2=pow(sqrt_mod(2),-1,P)
    ip=pow(pow(w,n//4,P),-1,P)
    out=[0]*n;out[0]=a[0];out[1]=a[h]
    for j in range(1,h):
        out[j+1]=(a[j]+a[n-j])*is2%P
        out[h+j]=(a[j]-a[n-j])*is2%P*ip%P
    return out

class TestPhase23(unittest.TestCase):
    def test_roots_and_rotation(self):
        for n in (4,8,16,32,128,512,4096):
            a=RealGreenFourier.create(n)
            self.assertEqual(pow(a.omega,n,P),1)
            self.assertEqual(pow(a.omega,n//2,P),P-1)
            for c,s in a.angles:
                self.assertEqual((c*c+s*s)%P,1)

    def test_geometric_nonroot_exact(self):
        rng=random.Random(202623)
        for n in (4,8,16,32,64,128,256,512,1024,4096):
            model=RealGreenFourier.create(n)
            for z in (0,2,3,rng.randrange(2,P)):
                if pow(z,n,P)==1:continue
                self.assertEqual(model.geometric(z),reference_c(synthesize_exponential_sequence(n,[z],[1])))

    def test_all_root_frequencies(self):
        for n in (4,8,16,32,64,128):
            model=RealGreenFourier.create(n)
            z=1;step=pow(model.omega,-1,P)
            for _ in range(n):
                self.assertEqual(model.geometric(z),reference_c(synthesize_exponential_sequence(n,[z],[1])))
                z=z*step%P

    def test_exponential_mixtures(self):
        rng=random.Random(993)
        for n in (8,64,256,1024):
            model=RealGreenFourier.create(n)
            for r in (1,2,4,9):
                nodes=[rng.randrange(1,P) for _ in range(r)]
                nodes[0]=1
                weights=[rng.randrange(P) for _ in range(r)]
                x=synthesize_exponential_sequence(n,nodes,weights)
                self.assertEqual(model.exponential_sum(nodes,weights),reference_c(x))

    def test_batch_inversion(self):
        rng=random.Random(39)
        for n in (1,2,3,31,1000):
            ds=[rng.randrange(1,P) for _ in range(n)]
            inv=batch_invert_nonzero(ds)
            self.assertTrue(all(a*b%P==1 for a,b in zip(ds,inv)))
        with self.assertRaises(ZeroDivisionError):batch_invert_nonzero([1,0,3])

    def test_rank_barrier_pure_exponential(self):
        rng=random.Random(301)
        for n in (8,16,32,64,128):
            for r in (1,2,3):
                x=synthesize_exponential_sequence(n,[i+2 for i in range(r)],[i+3 for i in range(r)])
                self.assertLessEqual(hankel_rank(x),r)
            self.assertEqual(hankel_rank([rng.randrange(P) for _ in range(n)]),n//2)

    def test_binary_collision_rank_not_low(self):
        rng=random.Random(457)
        for n in (32,64,128,256):
            ranks=[hankel_rank([rng.randrange(2) for _ in range(n)]) for _ in range(8)]
            self.assertEqual(ranks,[n//2]*8)

    def test_antidiagonal_hankel_witness(self):
        for n in (8,16,32,64,128):
            m=n//2;x=[0]*n;x[m-1]=1
            self.assertEqual(hankel_rank(x),m)

    def test_exact_inverse_row_sparsity(self):
        for n in (8,16,32,64,128):
            counts=[0]*n
            for k in range(n):
                e=[0]*n;e[k]=1
                out=reference_c(e)
                count=sum(v!=0 for v in out)
                counts[k]=count
                self.assertEqual(count,c_inverse_row_nonzeros(n,k))
            self.assertTrue(all(counts[k]==n-1 for k in range(1,n,2)))

if __name__=='__main__':unittest.main()

class TestAdaptivePhase23(unittest.TestCase):
    def test_recognition_one_two_and_zero(self):
        rng=random.Random(893)
        for n in (8,16,64,256,1024):
            eng=RealGreenFourier.create(n)
            for r in (0,1,2):
                nodes=[rng.randrange(2,P) for _ in range(r)]
                if r==2:nodes[0]=1 # root-of-unity branch mixed with ordinary node
                weights=[rng.randrange(1,P) for _ in range(r)]
                x=synthesize_exponential_sequence(n,nodes,weights)
                dec=discover_geometric_rank_at_most_two(x)
                self.assertIsNotNone(dec)
                self.assertEqual(synthesize_exponential_sequence(n,*dec),x)
                y,method=adaptive_real_transform(x,eng)
                self.assertEqual(y,reference_c(x))
                self.assertEqual(method,'green_rank_'+str(r))

    def test_fallback_random_binary(self):
        rng=random.Random(812)
        for n in (8,16,64,256,1024):
            eng=RealGreenFourier.create(n)
            x=[rng.randrange(2) for _ in range(n)]
            out,method=adaptive_real_transform(x,eng)
            self.assertEqual(out,reference_c(x))
            self.assertEqual(method,'reference_fft_fallback')

    def test_fallback_random_field(self):
        rng=random.Random(921)
        for n in (8,32,128,512):
            x=[rng.randrange(P) for _ in range(n)]
            out,method=adaptive_real_transform(x)
            self.assertEqual(out,reference_c(x))
            self.assertEqual(method,'reference_fft_fallback')

    def test_detector_rejects_nongeometric(self):
        for n in (8,16,32,64):
            x=[0]*n;x[n//2-1]=1
            self.assertIsNone(discover_geometric_rank_at_most_two(x))
            self.assertEqual(adaptive_real_transform(x)[0],reference_c(x))

class TestAdditionalAlgebra(unittest.TestCase):
    def test_general_linear_recurrence_hankel_bound(self):
        # An order-three recurrence, not necessarily a three-distinct-pole sequence.
        for n in (16,32,64,128):
            x=[1,2,7]
            for k in range(n-3):x.append((3*x[-1]+5*x[-2]+11*x[-3])%P)
            self.assertLessEqual(hankel_rank(x),3)

    def test_repeated_pole_does_not_falsely_recognize_rank2(self):
        # (a+b*k)*z^k: Hankel rank <= 2 but NOT a sum of distinct exponentials.
        for n in (8,32,128):
            z=17
            x=[(5+9*k)*pow(z,k,P)%P for k in range(n)]
            self.assertEqual(hankel_rank(x),2)
            self.assertIsNone(discover_geometric_rank_at_most_two(x))
            out,how=adaptive_real_transform(x)
            self.assertEqual(how,'reference_fft_fallback')
            self.assertEqual(out,reference_c(x))

    def test_small_gf2_hankel_count(self):
        # Independent finite-field enumeration: for m=1..7, exactly half.
        from audit import invertible_hankel_gf2
        for m in range(1,8):
            cases=1<<(2*m-1)
            self.assertEqual(sum(invertible_hankel_gf2(v,m) for v in range(cases)),cases//2)

class TestSparseDifferenceGreen(unittest.TestCase):
    def test_step_signals(self):
        for n in (8,16,64,256,1024,4096):
            eng=RealGreenFourier.create(n)
            for cut in (1,n//4,n//2,n-1):
                x=[7]*cut+[12]*(n-cut)
                expected=reference_c(x)
                self.assertEqual(real_transform_sparse_differences(x,eng,1,2),expected)
                actual,method=adaptive_real_transform_structured(x,eng)
                self.assertEqual(actual,expected)
                self.assertTrue(method.startswith('green_'))

    def test_affine_signals_and_second_difference(self):
        for n in (8,16,64,256,1024,4096):
            eng=RealGreenFourier.create(n)
            x=[(31+7*k)%P for k in range(n)]
            self.assertEqual(len([v for v in cyclic_difference(x,2) if v]),2)
            self.assertEqual(real_transform_sparse_differences(x,eng,2,2),reference_c(x))
            got,method=adaptive_real_transform_structured(x,eng)
            self.assertEqual(got,reference_c(x))
            self.assertEqual(method,'green_difference_r2')

    def test_sparse_difference_greater_order(self):
        n=128;eng=RealGreenFourier.create(n)
        # Quadratic polynomial has cyclic third difference supported near wrap.
        x=[(k*k+2*k+5)%P for k in range(n)]
        d=cyclic_difference(x,3)
        self.assertLessEqual(sum(v!=0 for v in d),3)
        self.assertEqual(real_transform_sparse_differences(x,eng,3,3),reference_c(x))

    def test_random_dense_fallback(self):
        rng=random.Random(113)
        for n in (16,64,256,1024):
            x=[rng.randrange(P) for _ in range(n)]
            eng=RealGreenFourier.create(n)
            y,how=adaptive_real_transform_structured(x,eng)
            self.assertEqual(how,'reference_fft_fallback')
            self.assertEqual(y,reference_c(x))

    def test_permutation_covariance_of_difference_support(self):
        rng=random.Random(229)
        for n in (16,64,256):
            x=[rng.randrange(2) for _ in range(n)]
            perm=list(range(n));rng.shuffle(perm)
            # y_(perm[k])=x_k; P maps old coordinate k to perm[k].
            y=[0]*n
            for k,t in enumerate(perm):y[t]=x[k]
            # Z_perm y at perm[k] equals y at perm[k-1].
            diff_perm=[0]*n
            for k,t in enumerate(perm):diff_perm[t]=(y[t]-y[perm[k-1]])%P
            dd=cyclic_difference(x,1)
            self.assertEqual(sum(v!=0 for v in diff_perm),sum(v!=0 for v in dd))
            for k,t in enumerate(perm):self.assertEqual(diff_perm[t],dd[k])

class TestFullBinaryDistributions(unittest.TestCase):
    def test_exact_binary_hankel_rank_distribution(self):
        from audit import hankel_rank_gf2
        for m in range(1,8):
            from collections import Counter
            hist=Counter(hankel_rank_gf2(v,m) for v in range(1<<(2*m-1)))
            self.assertEqual(hist[0],1)
            for r in range(1,m):self.assertEqual(hist[r],3*4**(r-1))
            self.assertEqual(hist[m],4**(m-1))

    def test_binary_transition_distribution(self):
        from audit import cyclic_transitions
        import math,collections
        for n in (4,8,12):
            hist=collections.Counter(cyclic_transitions(v,n) for v in range(1<<n))
            for s in range(n+1):
                self.assertEqual(hist[s],2*math.comb(n,s) if s%2==0 else 0)

    def test_second_difference_support_dominates_binary_transitions(self):
        from audit import cyclic_transitions
        rng=random.Random(9958)
        for n in (8,16,64,256):
            for _ in range(25):
                x=[rng.randrange(2) for _ in range(n)]
                mask=sum(v<<i for i,v in enumerate(x))
                transitions=cyclic_transitions(mask,n)
                self.assertLessEqual(transitions,sum(v!=0 for v in cyclic_difference(x,2)))
