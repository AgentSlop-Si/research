import unittest,random
from math import gcd
from phase13 import *

CASES=[(3,307),(5,521),(7,701),(9,919),(11,1123),(15,1531),(17,1871),(21,2143)]

class Phase13Test(unittest.TestCase):
    def test_01_primitive_root(self):
        for n,p in CASES:
            w=omega_root(n,p)
            self.assertEqual(pow(w,n,p),1)
            self.assertTrue(all(pow(w,n//q,p)!=1 for q in primes_of(n)))

    def test_02_gauss_nonzero(self):
        for n,p in CASES:
            w=omega_root(n,p)
            G=sum(pow(w,j*j%n,p) for j in range(n))%p
            G2=sum(pow(w,-j*j%n,p) for j in range(n))%p
            self.assertEqual(G*G2%p,n%p)
            self.assertNotEqual(G,0)

    def test_03_independent_trace(self):
        for n,p in CASES:
            w=omega_root(n,p)
            self.assertEqual(coeff_F(n,w,p),coeff_trace(fourier(n,w,p),w,p))

    def test_04_reconstruct_every_fourier_entry(self):
        for n,p in CASES:
            w=omega_root(n,p)
            self.assertEqual(synth(coeff_F(n,w,p),w,p),fourier(n,w,p))

    def test_05_flat_and_full_rank(self):
        for n,p in CASES:
            w=omega_root(n,p);C=coeff_F(n,w,p)
            self.assertTrue(all(z for row in C for z in row))
            self.assertEqual(rank(C,p),n)

    def test_06_green_two_path_has_rank_one_coefficients(self):
        for n,p in CASES:
            w=omega_root(n,p);a=2;b=3
            while pow(a,n,p)==1:a+=1
            while pow(b,n,p)==1:b+=1
            C=coeff_trace(branch_matrix(n,a,b,w,p),w,p)
            den=pow((1-pow(a,n,p))*(1-pow(b,n,p))%p,-1,p)
            self.assertEqual(C,[[den*pow(a,i,p)*pow(b,j,p)%p for j in range(n)]for i in range(n)])
            self.assertEqual(rank(C,p),1)

    def test_07_endpoint_Weyl_gauges_keep_rank_one(self):
        for n,p in CASES[:6]:
            w=omega_root(n,p);a=2;b=3
            while pow(a,n,p)==1:a+=1
            while pow(b,n,p)==1:b+=1
            C=coeff_trace(branch_matrix(n,a,b,w,p),w,p)
            # M_L=S^l1 T^l2, M_R=S^r1 T^r2.
            for l1,l2,r1,r2 in [(1,2,3,4),(0,1,2,0),(4,2,0,3)]:
                shifted=[]
                for i in range(n):
                    row=[]
                    for j in range(n):
                        a0=(i-l1-r1)%n;b0=(j-l2-r2)%n
                        phase=(l2*a0+(l2+b0)*r1)%n
                        row.append(C[a0][b0]*pow(w,phase,p)%p)
                    shifted.append(row)
                self.assertEqual(rank(shifted,p),1)

    def test_08_rotated_formula_independently_derived(self):
        bs=[(1,0,0,1),(1,0,1,1),(0,1,1,1),(1,1,0,1),(1,2,1,3)]
        for n,p in CASES[:7]:
            w=omega_root(n,p)
            for basis in bs:
                if gcd(basis[0]*basis[3]-basis[1]*basis[2],n)!=1:continue
                self.assertEqual(rotated(n,w,p,*basis),rotated_direct(n,w,p,*basis))

    def test_09_rank_formula_all_selected_gauges(self):
        bs=[(1,0,0,1),(1,0,1,1),(0,1,1,1),(1,1,0,1),(1,2,1,3),(1,0,1,7),(1,0,1,11)]
        for n,p in CASES[:7]:
            w=omega_root(n,p)
            for basis in bs:
                if gcd(basis[0]*basis[3]-basis[1]*basis[2],n)!=1:continue
                self.assertEqual(rank(rotated(n,w,p,*basis),p),rotated_rank(n,*basis))

    def test_10_coordinate_rank_drop_is_real(self):
        for n,p in CASES:
            w=omega_root(n,p)
            self.assertEqual(rank(rotated(n,w,p,1,0,0,1),p),n)
            self.assertEqual(rank(rotated(n,w,p,1,0,1,1),p),1)

    def test_11_hankel_rescues_rank_one_coordinate(self):
        for n,p in CASES:
            w=omega_root(n,p)
            self.assertEqual(rank(hankel(n,w,p,1,0,1,1),p),(n+1)//2)

    def test_12_all_symplectic_bases_quadratic_identity(self):
        for n in [3,5,7,11]:
            for u in range(n):
                for v in range(n):
                    for r in range(n):
                        for s in range(n):
                            D,z=delta(n,u,v,r,s)
                            if D==0:continue
                            A=(u*u+v*v)%n;B=(r*r+s*s)%n;dot=(u*r+v*s)%n
                            self.assertEqual((A*B-dot*dot-D*D)%n,0)
                            if z==0:
                                self.assertNotEqual(A,0)
                                self.assertNotEqual(B,0)
                                self.assertEqual((A*B-2*D*D)%n,0)

    def test_13_two_Green_ordered_operator_matches_dense(self):
        random.seed(130)
        for n,p in CASES:
            w=omega_root(n,p);a=2;b=3
            while pow(a,n,p)==1:a+=1
            while pow(b,n,p)==1:b+=1
            A=branch_matrix(n,a,b,w,p)
            for _ in range(3):
                x=[random.randrange(p) for j in range(n)]
                self.assertEqual(branch_apply(x,a,b,w,p),matvec(A,x,p))

    def test_14_parallel_noncommuting_network_matches_dense(self):
        random.seed(131)
        for n,p in CASES:
            w=omega_root(n,p);a=2;b=3
            while pow(a,n,p)==1:a+=1
            while pow(b,n,p)==1:b+=1
            A=sum_matrix(n,a,b,w,p)
            for _ in range(3):
                x=[random.randrange(p) for j in range(n)]
                self.assertEqual(sum_apply(x,a,b,w,p),matvec(A,x,p))

    def test_15_parallel_Green_network_is_not_fourier(self):
        for n,p in CASES:
            w=omega_root(n,p);a=2;b=3
            while pow(a,n,p)==1:a+=1
            while pow(b,n,p)==1:b+=1
            self.assertNotEqual(sum_matrix(n,a,b,w,p),fourier(n,w,p))

    def test_16_inverse_of_branch_sum_is_dense(self):
        for n,p in CASES[:6]:
            w=omega_root(n,p)
            witness=find_dense_inverse_witness(n,w,p)
            self.assertIsNotNone(witness,(n,p))
            a,b=witness;I=inverse(sum_matrix(n,a,b,w,p),p)
            self.assertTrue(all(z for row in I for z in row))

    def test_17_exact_field_work_scales_linearly(self):
        p=998244353
        for n in [64,256,1024,4096,16384]:
            w=omega_root(n,p);x=[(j*j+17*j+43)%p for j in range(n)]
            c=Cost();out=sum_apply(x,2,3,w,p,c)
            self.assertEqual(len(out),n)
            self.assertLess(c.total,13*n)
            iv=pow(1-pow(2,n,p),-1,p)
            for j in [0,1,n//3,n-1]:
                convolution=sum(pow(2,(j-k)%n,p)*x[k] for k in range(n))*iv%p
                self.assertEqual(out[j],(convolution+x[j]*pow(1-3*pow(w,j,p),-1,p))%p)

if __name__=='__main__':unittest.main(verbosity=2)

class Phase13BatchTests(unittest.TestCase):
    def test_18_batch_modulation_inverse(self):
        p=998244353
        for n in [8,64,256,1024,4096]:
            w=omega_root(n,p)
            a=prepare_gt(n,3,w,p);c=Cost();b=prepare_gt_batch(n,3,w,p,c)
            self.assertEqual(a,b)
            self.assertEqual(c.inv,1)
            self.assertLess(c.total,7*n)

    def test_19_prepared_data_reuse(self):
        p=998244353
        for n in [64,1024,4096]:
            w=omega_root(n,p);c=Cost();diag=prepare_gt_batch(n,3,w,p,c)
            prep=c.total
            for shift in [0,7,19]:
                x=[(i*i+shift*37+31)%p for i in range(n)]
                online=Cost();out=sum_apply(x,2,3,w,p,online,diag)
                self.assertEqual(len(out),n)
                self.assertLess(online.total,8*n)
            self.assertLess(prep,7*n)

class Phase13OrientationTests(unittest.TestCase):
    def test_20_reverse_orientation_has_full_weyl_rank(self):
        for n,p in [(3,307),(5,521),(7,701),(9,919),(15,1531)]:
            w=omega_root(n,p);a=2;b=3
            A=reverse_matrix(n,a,b,w,p)
            C=coeff_trace(A,w,p)
            den=pow((1-pow(a,n,p))*(1-pow(b,n,p))%p,-1,p)
            ref=[[den*pow(a,i,p)*pow(b,j,p)*pow(w,i*j%n,p)%p for j in range(n)]for i in range(n)]
            self.assertEqual(C,ref)
            self.assertEqual(rank(C,p),n)
            x=[(k*k+13*k+17)%p for k in range(n)]
            self.assertEqual(reverse_apply(x,a,b,w,p),matvec(A,x,p))
            self.assertNotEqual(A,fourier(n,w,p))

    def test_21_triple_path_full_rank_yet_linear_executor(self):
        for n,p in [(3,307),(5,521),(7,701),(9,919),(15,1531)]:
            w=omega_root(n,p);a=2;b=3;g=4
            for t in [a,b,g]:self.assertNotEqual(pow(t,n,p),1)
            A=triple_matrix(n,a,b,g,w,p)
            self.assertEqual(rank(coeff_trace(A,w,p),p),n)
            x=[(11*k*k+19*k+5)%p for k in range(n)]
            self.assertEqual(triple_apply(x,a,b,g,w,p),matvec(A,x,p))
            self.assertNotEqual(A,fourier(n,w,p))
