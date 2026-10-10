import random
import unittest
from scan_resolvent import *

class TestTwistedGate(unittest.TestCase):
    def test_bidiagonal_intertwiner_both_directions(self):
        rng=random.Random(31)
        for p in (12289,65537):
            for n in (5,8,16,32,64):
                for _ in range(24):
                    s=Scan(*(rng.randrange(p) for _ in range(3)))
                    # Explicit degenerate branches as well.
                    if _ % 7 == 0: s=Scan(rng.randrange(p),0,rng.randrange(p))
                    if _ % 7 == 1: s=Scan(0,rng.randrange(p),rng.randrange(p))
                    if _ % 7 == 2: s=Scan(0,0,rng.randrange(p))
                    for direction in ('+','-'):
                        x=[rng.randrange(p) for j in range(n)]
                        target=apply_A(s,x,p,direction)
                        self.assertEqual(apply_scan(s,apply_B(s,x,p,direction),p),target)
                        self.assertEqual(apply_B(s,apply_scan(s,x,p),p,direction),target)

    def test_exact_gauged_circulant_eigenvectors(self):
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                q=primitive_root(p)
                self.assertNotEqual(pow(q,n,p),1)
                b=3; a=b*pow(q,n,p)%p; d=5
                s=Scan(a,b,d)
                evals=circulant_gauge_test(s,q,p,n,w)
                self.assertEqual(len(evals),n)
                for i in range(n):
                    for j in range(n):
                        direct=(s.a if i>j else s.b if i<j else s.d)%p
                        conjugated=direct*pow(q,j-i,p)%p
                        circulant=(s.d if i==j else b*pow(q,(j-i)%n,p))%p
                        self.assertEqual(conjugated,circulant)

    def test_two_stage_sparse_column_obstruction(self):
        rng=random.Random(2718)
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                for trial in range(30):
                    s1=Scan(rng.randrange(1,p),rng.randrange(1,p),rng.randrange(p))
                    s2=Scan(rng.randrange(1,p),rng.randrange(1,p),rng.randrange(p))
                    if trial%4==0:s1=Scan(rng.randrange(1,p),0,rng.randrange(p))
                    if trial%4==1:s2=Scan(0,rng.randrange(1,p),rng.randrange(p))
                    if trial%4==2:s1=Scan(0,rng.randrange(1,p),rng.randrange(p))
                    perm=list(range(n));rng.shuffle(perm)
                    result=two_stage_witness(s1,s2,n,p,w,perm)
                    self.assertEqual(result['lhs_interior_nonzero'],n-1)
                    self.assertLessEqual(result['rhs_support'],4)

    def test_three_stage_alphabet_obstruction(self):
        rng=random.Random(314159)
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                for trial in range(35):
                    stages=[Scan(*(rng.randrange(1,p) for _ in range(3))) for j in range(3)]
                    if trial%5==0: stages[0]=Scan(rng.randrange(1,p),0,7)
                    if trial%5==1: stages[2]=Scan(0,rng.randrange(1,p),7)
                    if trial%5==2: stages[1]=Scan(0,0,7)
                    if trial%5==3: stages[1]=Scan(0,rng.randrange(1,p),7)
                    p1=list(range(n));rng.shuffle(p1)
                    p2=list(range(n));rng.shuffle(p2)
                    res=three_stage_witness(*stages,n,p,w,p1,p2)
                    self.assertEqual(res['lhs_interior_distinct'],n-1)
                    self.assertLessEqual(res['middle_support'],2)
                    self.assertLessEqual(res['middle_baseline_distinct'],3)
                    self.assertLessEqual(res['rhs_interior_distinct'],13)

    def test_exact_classical_fft_positive_control(self):
        # A generic FFT DOES have log2(N) sparse-butterfly stages; our theorem
        # therefore must not be extended to all O(N)-work structured stages.
        for p in (12289,65537):
            n=16;w=nth_root_of_unity(p,n)
            for j in range(n):
                x=e(n,j)
                oracle=apply_dft(x,w,p)
                y=x[:]
                # Decimation in frequency, output bit reversal.
                for m in (n,n//2,n//4,n//8):
                    h=m//2; step=n//m
                    for k in range(0,n,m):
                        for v in range(h):
                            a,b=y[k+v],y[k+v+h]
                            y[k+v]=(a+b)%p
                            y[k+v+h]=((a-b)*pow(w,v*step,p))%p
                def bitrev(i):return int(f'{i:04b}'[::-1],2)
                got=[y[bitrev(i)] for i in range(n)]
                self.assertEqual(got,oracle)

if __name__=='__main__': unittest.main(verbosity=2)

class TestWeightedExtension(unittest.TestCase):
    def test_weighted_intertwining(self):
        from weighted_gate import WeightedScan
        rng=random.Random(919)
        for p in (12289,65537):
            for n in (8,16,32):
                for _ in range(25):
                    base=Scan(*(rng.randrange(p) for _ in range(3)))
                    if _ % 5==0:base=Scan(rng.randrange(1,p),0,rng.randrange(p))
                    if _ % 5==1:base=Scan(0,rng.randrange(1,p),rng.randrange(p))
                    left=[rng.randrange(1,p) for i in range(n)]
                    right=[rng.randrange(1,p) for i in range(n)]
                    s=WeightedScan(base,left,right)
                    if orientation(base,p)=='scalar':continue
                    x=[rng.randrange(p) for i in range(n)]
                    self.assertEqual(s.B_left(s.apply(x,p),p),s.A(x,p))
                    self.assertEqual(s.apply(s.B_right(x,p),p),s.A(x,p))

    def test_weighted_two_column_certificate(self):
        from weighted_gate import WeightedScan,weighted_two_column_certificate
        rng=random.Random(240521)
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                for case in range(30):
                    def random_weighted(choice):
                        a,b,d=(rng.randrange(1,p) for _ in range(3))
                        if choice==0:b=0
                        if choice==1:a=0
                        return WeightedScan(Scan(a,b,d),[rng.randrange(1,p) for _ in range(n)],[rng.randrange(1,p) for _ in range(n)])
                    s1=random_weighted(case%3)
                    s2=random_weighted((case//3)%3)
                    order=list(range(n));rng.shuffle(order)
                    cert=weighted_two_column_certificate(s1,s2,n,p,w,order)
                    self.assertLessEqual(cert['support_union'],6)
                    self.assertLessEqual(cert['left_common_zeros'],2)
                    self.assertGreaterEqual(cert['right_common_zeros'],n-1-6)
                    if n>=16:
                        self.assertLess(cert['left_common_zeros'],cert['right_common_zeros'])

class TestAsymmetricExtension(unittest.TestCase):
    def test_asymmetric_two_stage_general_variable_generators(self):
        from asymmetric_gate import ColumnEnvelope,RowEnvelope,asymmetric_two_col_certificate
        rng=random.Random(35072026)
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                for case in range(28):
                    rand=lambda:[rng.randrange(1,p) for i in range(n)]
                    s1=ColumnEnvelope(rand(),rand(),rand(),rand())
                    s2=RowEnvelope(rand(),rand(),rand(),rand())
                    perm=list(range(n));rng.shuffle(perm)
                    gout=rand();gin=rand()
                    cert=asymmetric_two_col_certificate(s1,s2,perm,n,p,w,gout,gin)
                    self.assertLessEqual(cert['source_union'],3)
                    self.assertLessEqual(cert['rhs_union'],6)
                    self.assertLessEqual(cert['lhs_joint_zeros'],2)
                    self.assertGreaterEqual(cert['rhs_joint_zeros'],n-7)
                    if n>=16:
                        self.assertLess(cert['lhs_joint_zeros'],cert['rhs_joint_zeros'])

class TestExceptionalEndpoints(unittest.TestCase):
    def test_three_stage_scalar_first_or_last(self):
        rng=random.Random(7102026)
        for p in (12289,65537):
            n=16;w=nth_root_of_unity(p,n)
            for trial in range(24):
                s1=Scan(0,0,7)
                s2=Scan(*(rng.randrange(p) for _ in range(3)))
                s3=Scan(rng.randrange(1,p),rng.randrange(1,p),5)
                p1=list(range(n));rng.shuffle(p1)
                p2=list(range(n));rng.shuffle(p2)
                # Scalar first: B3 * F * P1^-1 has n-1 distinct interior entries
                # in the column carrying original input frequency 1.
                inv=inverse_perm(p1)
                column_of_frequency_1=p1[1]  # P1^-1 e_k = e_1 for k=p1[1]
                self.assertEqual(inv[column_of_frequency_1],1)
                dftcol=apply_dft(e(n,1),w,p)
                left=apply_B(s3,dftcol,p)
                right=apply_A(s3,permute(apply_scan(s2,e(n,column_of_frequency_1),p),p2),p)
                self.assertEqual(len(set(interior(left,orientation(s3,p)))),n-1)
                self.assertLessEqual(len(set(interior(right,orientation(s3,p)))),9)
                # Scalar last: pre-permute F*B1, preserving n distinct values.
                s1b=Scan(rng.randrange(1,p),rng.randrange(1,p),4)
                src=e(n,witness_column(s1b,n,p))
                lhs=permute(apply_dft(apply_B(s1b,src,p),w,p),inverse_perm(p2))
                rhs=apply_scan(s2,permute(apply_A(s1b,src,p),p1),p)
                self.assertEqual(len(set(lhs)),n)
                self.assertLessEqual(len(set(rhs)),5)

class TestAffineEndpoints(unittest.TestCase):
    def test_asymmetric_gate_affine_endpoint_reorders(self):
        from asymmetric_gate import ColumnEnvelope,RowEnvelope,asymmetric_two_col_certificate
        from math import gcd
        rng=random.Random(424242)
        for prime in (12289,65537):
            for n in (8,16,32,64):
                w=nth_root_of_unity(prime,n)
                units=[i for i in range(n) if gcd(i,n)==1]
                for case in range(20):
                    rs=rng.choice(units);cs=rng.choice(units)
                    r0=rng.randrange(n);c0=rng.randrange(n)
                    wp=pow(w,rs*cs,prime)
                    rand=lambda:[rng.randrange(1,prime) for _ in range(n)]
                    output_base=rand();input_base=rand()
                    gout=[output_base[i]*pow(w,rs*i*c0+r0*c0,prime)%prime for i in range(n)]
                    gin=[input_base[j]*pow(w,r0*cs*j,prime)%prime for j in range(n)]
                    # Verify exact identity of row/column-affine Fourier with diagonal-scaled wp DFT.
                    for _ in range(4):
                        i=rng.randrange(n);j=rng.randrange(n)
                        direct=output_base[i]*input_base[j]*pow(w,((rs*i+r0)*(cs*j+c0))%n,prime)%prime
                        separated=gout[i]*gin[j]*pow(wp,i*j,prime)%prime
                        self.assertEqual(direct,separated)
                    s1=ColumnEnvelope(rand(),rand(),rand(),rand())
                    s2=RowEnvelope(rand(),rand(),rand(),rand())
                    perm=list(range(n));rng.shuffle(perm)
                    cert=asymmetric_two_col_certificate(s1,s2,perm,n,prime,wp,gout,gin)
                    self.assertLessEqual(cert['lhs_joint_zeros'],2)
                    self.assertLessEqual(cert['rhs_union'],6)
                    if n>=16:self.assertLess(cert['lhs_joint_zeros'],cert['rhs_joint_zeros'])

class TestCompactPolynomial(unittest.TestCase):
    def test_exact_three_coefficient_quadratic_certificate(self):
        rng=random.Random(10102026)
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=nth_root_of_unity(p,n)
                for case in range(24):
                    r=[rng.randrange(1,p) for _ in range(3)]
                    output=[rng.randrange(1,p) for _ in range(n)]
                    x0=[pow(r[0],-1,p), -pow(r[1],-1,p)%p] + [0]*(n-2)
                    x1=[0, pow(r[1],-1,p), -pow(r[2],-1,p)%p] + [0]*(n-3)
                    f0=[a*b%p for a,b in zip(output,apply_dft(x0,w,p))]
                    f1=[a*b%p for a,b in zip(output,apply_dft(x1,w,p))]
                    roots=0
                    for i in range(n-1):
                        determinant=(f0[i]*f1[i+1]-f1[i]*f0[i+1])%p
                        z=pow(w,i,p)
                        quad=(r[2]-(1+w)*r[1]*z+w*r[0]*z*z)%p
                        scale=(output[i]*output[i+1]*z*(w-1)*pow(r[0]*r[1]*r[2],-1,p))%p
                        self.assertEqual(determinant,(scale*quad)%p)
                        roots+=quad==0
                    self.assertLessEqual(roots,2)
