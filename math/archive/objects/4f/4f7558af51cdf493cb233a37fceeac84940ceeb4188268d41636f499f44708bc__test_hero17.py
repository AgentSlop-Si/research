import random
import unittest
from itertools import product
from math import gcd
from tensor_union import (
    coprime_split, crt_idempotents, direct_circular_convolution,
    direct_dft, direct_dft_bins, make_low_rank,
    root_for, recognize as tensor_recognize,
    transform_certified as tensor_transform,
    circular_convolution_certified,
)
from coset_union import recognize_and_transform as coset_transform, support_gcd
from fast_vandermonde import solve_moments
from fiber_union import (
    choose_q, make_fiber_signal, recognize as fiber_recognize,
    transform_certified as fiber_transform,
)
from fused_fft import transform_if_supported
from fiber_convolution import convolve_if_supported, union_and_convolve
import phase_union_general as phase


class Hero17Suite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primes={15:31,16:17,35:71,63:127,64:193,81:163,99:199,125:251,143:859,
                    243:487,255:1021,256:65537,323:647,512:65537,
                    729:1459,1024:65537,2303:46061}
        cls.w={n:root_for(n,p) for n,p in cls.primes.items()}
        cls.rng=random.Random(17)

    def test_coprime_factor_search(self):
        self.assertEqual(coprime_split(143),(11,13))
        self.assertEqual(coprime_split(255),(15,17))
        self.assertIsNone(coprime_split(256))
        self.assertIsNone(coprime_split(243))
        self.assertIsNone(coprime_split(127))

    def test_crt_index_is_bijection(self):
        for a,b in [(3,5),(7,9),(11,13),(15,17)]:
            n=a*b
            e1,e2=crt_idempotents(a,b)
            sequence=[(u*e1+v*e2)%n for u in range(a) for v in range(b)]
            self.assertEqual(set(sequence),set(range(n)))
            output=[(s*b+t*a)%n for s in range(a) for t in range(b)]
            self.assertEqual(set(output),set(range(n)))

    def test_random_arbitrary_factors_tensor_exact(self):
        rng=self.rng
        for a,b in [(3,5),(5,7),(7,9),(9,11),(11,13),(15,17),(17,19)]:
            n=a*b;p=self.primes[n];w=self.w[n]
            for r in [1,2,3]:
                factors_a=[[rng.randrange(p) for _ in range(a)] for _ in range(r)]
                factors_b=[[rng.randrange(p) for _ in range(b)] for _ in range(r)]
                x=make_low_rank(a,b,p,w,factors_a,factors_b)
                cert=tensor_recognize(x,p,w,r)
                self.assertIsNotNone(cert)
                self.assertEqual(tensor_transform(cert),direct_dft(x,p,w))

    def test_tensor_random_dense_rejected(self):
        p=self.primes[143];w=self.w[143]
        for _ in range(20):
            x=[self.rng.randrange(p) for _ in range(143)]
            self.assertIsNone(tensor_recognize(x,p,w,2))

    def test_tensor_certificate_reconstructs_raw(self):
        a,b=11,13;n=a*b;p=self.primes[n];w=self.w[n]
        x=make_low_rank(a,b,p,w,[[self.rng.randrange(p) for _ in range(a)] for _ in range(3)],
                        [[self.rng.randrange(p) for _ in range(b)] for _ in range(3)])
        cert=tensor_recognize(x,p,w,3)
        self.assertIsNotNone(cert)
        for u,v in product(range(a),range(b)):
            direct=sum(cert.coefficient_rows[u][l]*cert.basis_rows[l][v]
                       for l in range(cert.rank))%p
            self.assertEqual(direct,x[(u*cert.e_a+v*cert.e_b)%n])

    def test_independent_polynomial_phases_tensor_rank_one(self):
        for n in [99,143,255]:
            p=self.primes[n];w=self.w[n]
            for degree in [2,3,4,5,7]:
                x=[pow(w,(3*j**degree+7*j+4)%n,p) for j in range(n)]
                cert=tensor_recognize(x,p,w,1)
                self.assertIsNotNone(cert,(n,degree))
                self.assertEqual(cert.rank,1)
                self.assertEqual(tensor_transform(cert),direct_dft(x,p,w))

    def test_strict_expansion_previous_phase_rejects_cubic(self):
        n,p=143,self.primes[143];w=self.w[143]
        x=[pow(w,(3*j*j*j+7*j)%n,p) for j in range(n)]
        self.assertIsNone(phase.recognize(x,p,w,3))
        self.assertIsNotNone(tensor_recognize(x,p,w,1))

    def test_sum_of_distinct_polynomial_phases(self):
        for n in [99,143]:
            p=self.primes[n];w=self.w[n]
            x=[(2*pow(w,(j*j*j+4*j)%n,p)+5*pow(w,(7*j**4+3*j*j)%n,p))%p for j in range(n)]
            cert=tensor_recognize(x,p,w,2)
            self.assertIsNotNone(cert)
            self.assertLessEqual(cert.rank,2)
            self.assertEqual(tensor_transform(cert),direct_dft(x,p,w))

    def test_rank_one_convolution_exact(self):
        rng=self.rng
        for a,b in [(3,5),(7,9),(11,13),(15,17)]:
            n=a*b;p=self.primes[n];w=self.w[n]
            for r1,r2 in [(1,1),(1,2),(2,2),(2,3)]:
                x=make_low_rank(a,b,p,w,[[rng.randrange(p) for _ in range(a)] for _ in range(r1)],
                        [[rng.randrange(p) for _ in range(b)] for _ in range(r1)])
                y=make_low_rank(a,b,p,w,[[rng.randrange(p) for _ in range(a)] for _ in range(r2)],
                        [[rng.randrange(p) for _ in range(b)] for _ in range(r2)])
                cx=tensor_recognize(x,p,w,r1)
                cy=tensor_recognize(y,p,w,r2)
                self.assertIsNotNone(cx);self.assertIsNotNone(cy)
                z=circular_convolution_certified(cx,cy)
                self.assertEqual(z,direct_circular_convolution(x,y,p))
                cz=tensor_recognize(z,p,w,r1*r2)
                self.assertIsNotNone(cz)
                self.assertLessEqual(cz.rank,r1*r2)

    def test_coset_power_two_exhaustive(self):
        for n,d in [(256,16),(512,32),(1024,8)]:
            p=self.primes[n];w=self.w[n]
            m=n//d;eta=pow(w,d,p)
            x=[0]*n
            for t in range(m):x[5+d*t]=pow(eta,(3*t*t+7*t)%m,p)
            out,cert=coset_transform(x,p,w,2)
            self.assertEqual(out,direct_dft(x,p,w))
            self.assertEqual(cert.step,d)
            self.assertEqual(cert.branch,'phase-coset')

    def test_coset_short_and_singleton(self):
        n,p=256,65537;w=self.w[n]
        x=[0]*n;x[4]=27;x[132]=19
        out,cert=coset_transform(x,p,w,2)
        self.assertEqual(out,direct_dft(x,p,w))
        self.assertEqual(cert.branch,'short-coset')
        x=[0]*n;x[37]=25
        out,cert=coset_transform(x,p,w,2)
        self.assertEqual(out,direct_dft(x,p,w))
        self.assertEqual(cert.step,n)

    def test_coset_rejects_dense_random(self):
        n,p=256,65537;w=self.w[n]
        x=[self.rng.randrange(1,p) for _ in range(n)]
        out,cert=coset_transform(x,p,w,2)
        self.assertIsNone(out);self.assertIsNone(cert)

    def test_vandermonde_structured_solver(self):
        rng=self.rng
        for p in [17,193,65537]:
            for r in range(1,10):
                nodes=rng.sample(range(1,p),r)
                weights=[rng.randrange(p) for _ in range(r)]
                moments=[sum(weights[l]*pow(nodes[l],j,p) for l in range(r))%p for j in range(r)]
                self.assertEqual(solve_moments(nodes,moments,p),weights)

    def test_fiber_raw_arbitrary_modes_per_row(self):
        rng=self.rng
        for n in [16,81,125,243,256,512,1024]:
            p=self.primes[n];w=self.w[n]
            q=choose_q(n);m=n//q
            for r in [1,2,3]:
                modes=[]
                for _ in range(q):
                    modes.append([(h,rng.randrange(1,p)) for h in rng.sample(range(m),r)])
                x=make_fiber_signal(n,p,w,q,modes)
                cert=fiber_recognize(x,p,w,r)
                self.assertIsNotNone(cert,(n,r))
                self.assertLessEqual(max(map(len,cert.modes)),r)
                self.assertEqual(fiber_transform(cert),direct_dft(x,p,w))

    def test_fiber_polynomial_phases_square_even_power(self):
        for n in [16,81,256,1024]:
            p=self.primes[n];w=self.w[n]
            for d in [2,3,4,5,7]:
                x=[pow(w,(3*j**d+5*j*j+7*j+9)%n,p) for j in range(n)]
                cert=fiber_recognize(x,p,w,1)
                self.assertIsNotNone(cert,(n,d))
                self.assertEqual(fiber_transform(cert),direct_dft(x,p,w))

    def test_fiber_polynomial_phases_odd_exponent_prime_powers(self):
        for n,bound in [(125,5),(243,3),(512,1)]:
            p=self.primes[n];w=self.w[n]
            for degree in [2,3,4,5,7]:
                x=[pow(w,(3*j**degree+5*j*j+7*j+11)%n,p) for j in range(n)]
                cert=fiber_recognize(x,p,w,bound)
                self.assertIsNotNone(cert,(n,degree))
                self.assertEqual(fiber_transform(cert),direct_dft(x,p,w))

    def test_fiber_prime_sparse_spectrum(self):
        # Q=1 for prime lengths: ordinary sparse-frequency input is recognized.
        n=127;p=65537;w=root_for(n,p) if (p-1)%n==0 else None
        if w is None:
            p=509
            # 127*4+1=509 is prime
            w=root_for(n,p)
        x=make_fiber_signal(n,p,w,1,[[(3,5),(41,7)]])
        cert=fiber_recognize(x,p,w,2)
        self.assertIsNotNone(cert)
        self.assertEqual(cert.q,1)
        self.assertEqual(fiber_transform(cert),direct_dft(x,p,w))

    def test_fiber_full_matrix_rank_not_tensor_low_rank(self):
        n,p=256,65537;w=self.w[n]
        q=choose_q(n);m=n//q
        # Rows are different DFT_M characters; QxM matrix has rank Q.
        modes=[[(t,2+t)] for t in range(q)]
        x=make_fiber_signal(n,p,w,q,modes)
        self.assertTrue(all(z for z in x))
        cert=fiber_recognize(x,p,w,1)
        self.assertIsNotNone(cert)
        self.assertEqual(fiber_transform(cert),direct_dft(x,p,w))
        mat=[[x[t+q*u] for u in range(m)] for t in range(q)]
        self.assertEqual(matrix_rank(mat,p),q)

    def test_fiber_random_dense_reject(self):
        n,p=256,65537;w=self.w[n]
        for _ in range(10):
            x=[self.rng.randrange(p) for j in range(n)]
            self.assertIsNone(fiber_recognize(x,p,w,3))

    def test_fiber_corruption_reject(self):
        n,p=256,65537;w=self.w[n]
        q=choose_q(n);m=n//q
        x=make_fiber_signal(n,p,w,q,[[(t%16,t+1)] for t in range(q)])
        x[73]=(x[73]+1)%p
        self.assertIsNone(fiber_recognize(x,p,w,1))

    def test_fusion_accepts_three_disjoint_families(self):
        n,p=143,859;w=self.w[n]
        x=make_low_rank(11,13,p,w,[[j*j+3 for j in range(11)]],[[j*j*j+5 for j in range(13)]])
        result=transform_if_supported(x,p,w,1)
        self.assertEqual(result.branch,'tensor-crt')
        self.assertEqual(result.spectrum,direct_dft(x,p,w))
        n,p=256,65537;w=self.w[n];q=16
        x=make_fiber_signal(n,p,w,q,[[(t,t+1)] for t in range(q)])
        result=transform_if_supported(x,p,w,1)
        self.assertEqual(result.branch,'fiber-union')
        self.assertEqual(result.spectrum,direct_dft(x,p,w))
        # Coset case not low fiber rank due to arbitrary short sparse amplitudes.
        x=[0]*n;x[7]=3;x[135]=3
        result=transform_if_supported(x,p,w,1)
        self.assertIsNotNone(result)
        self.assertEqual(result.spectrum,direct_dft(x,p,w))

    def test_graph_union_convolution_full_rank(self):
        rng=self.rng
        for n in [16,64,256,1024]:
            p=self.primes[n];w=self.w[n];q=choose_q(n)
            h1=list(range(q));h2=list(range(q))
            rng.shuffle(h1);rng.shuffle(h2)
            x=make_fiber_signal(n,p,w,q,[[(h,rng.randrange(1,p))] for h in h1])
            y=make_fiber_signal(n,p,w,q,[[(h,rng.randrange(1,p))] for h in h2])
            self.assertEqual(matrix_rank([[x[t+q*u] for u in range(n//q)] for t in range(q)],p),q)
            self.assertEqual(matrix_rank([[y[t+q*u] for u in range(n//q)] for t in range(q)],p),q)
            z,proof=convolve_if_supported(x,y,p,w,1,1,max_states_ratio=2)
            self.assertIsNotNone(z)
            self.assertEqual(proof.matching_edges,q)
            self.assertLessEqual(proof.union_states,q)
            self.assertEqual(z,direct_circular_convolution(x,y,p))

    def test_graph_union_high_edge_count_but_low_state_count(self):
        rng=self.rng
        for n in [16,64,256,1024]:
            p=self.primes[n];w=self.w[n];q=choose_q(n)
            x=make_fiber_signal(n,p,w,q,[[(2,rng.randrange(1,p))] for t in range(q)])
            y=make_fiber_signal(n,p,w,q,[[(2,rng.randrange(1,p))] for t in range(q)])
            z,proof=convolve_if_supported(x,y,p,w,1,1,max_states_ratio=2)
            self.assertIsNotNone(z)
            self.assertEqual(proof.matching_edges,q*q)
            self.assertLessEqual(proof.union_states,q)
            self.assertEqual(z,direct_circular_convolution(x,y,p))

    def test_graph_union_random_frequencies(self):
        rng=self.rng
        for n in [16,64,256,1024]:
            p=self.primes[n];w=self.w[n];q=choose_q(n);m=n//q
            x=make_fiber_signal(n,p,w,q,[[(rng.randrange(m),rng.randrange(1,p))] for t in range(q)])
            y=make_fiber_signal(n,p,w,q,[[(rng.randrange(m),rng.randrange(1,p))] for t in range(q)])
            z,proof=convolve_if_supported(x,y,p,w,1,1,max_states_ratio=4)
            self.assertIsNotNone(z)
            self.assertEqual(z,direct_circular_convolution(x,y,p))

    def test_graph_union_rejects_too_many_output_states(self):
        n,p=256,65537;w=self.w[n];q=16;s=4
        rng=random.Random(87)
        # Q=s*s; each frequency appears s times, matching pairs cover Q targets.
        x=make_fiber_signal(n,p,w,q,[[(t%s,rng.randrange(1,p))] for t in range(q)])
        y=make_fiber_signal(n,p,w,q,[[(t//s,rng.randrange(1,p))] for t in range(q)])
        z,proof=convolve_if_supported(x,y,p,w,1,1,max_states_ratio=2)
        self.assertIsNone(z)
        self.assertEqual(proof.union_states,64)
        z,proof=convolve_if_supported(x,y,p,w,1,1,max_states_ratio=4)
        self.assertIsNotNone(z)
        self.assertEqual(z,direct_circular_convolution(x,y,p))

    def test_graph_union_rejects_arbitrary_dense_inputs(self):
        n,p=256,65537;w=self.w[n]
        x=[self.rng.randrange(p) for _ in range(n)]
        y=[self.rng.randrange(p) for _ in range(n)]
        z,proof=convolve_if_supported(x,y,p,w,1,1)
        self.assertIsNone(z)

    def test_large_tensor_spot_checks(self):
        n,p=2303,46061;a,b=47,49;w=self.w[n]
        rng=self.rng
        x=make_low_rank(a,b,p,w,[[rng.randrange(p) for _ in range(a)] for _ in range(3)],
                        [[rng.randrange(p) for _ in range(b)] for _ in range(3)])
        cert=tensor_recognize(x,p,w,3)
        self.assertIsNotNone(cert)
        out=tensor_transform(cert)
        bins=sorted(set([0,1,n-1,7,11,73]+[rng.randrange(n) for _ in range(37)]))
        self.assertEqual([out[k] for k in bins],direct_dft_bins(x,p,w,bins))


def matrix_rank(M,p):
    x=[[z%p for z in row] for row in M]
    nr=len(x);nc=len(x[0]) if nr else 0
    rank=0
    for col in range(nc):
        pivot=next((j for j in range(rank,nr) if x[j][col]),None)
        if pivot is None:continue
        x[pivot],x[rank]=x[rank],x[pivot]
        inv=pow(x[rank][col],-1,p)
        x[rank]=[v*inv%p for v in x[rank]]
        for j in range(rank+1,nr):
            fac=x[j][col]
            if fac:x[j]=[(a-fac*b)%p for a,b in zip(x[j],x[rank])]
        rank+=1
        if rank==nr:break
    return rank

if __name__=='__main__':unittest.main(verbosity=2)
