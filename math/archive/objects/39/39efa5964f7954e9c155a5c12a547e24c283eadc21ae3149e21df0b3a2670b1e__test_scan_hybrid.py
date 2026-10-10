import sys, unittest, random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scan_hybrid import *

class TestScans(unittest.TestCase):
    def test_twoscan_full_fft_basis(self):
        columns=0
        for n in [1,2,4,8,16,32,64]:
            for j in range(n):
                x=[int(k==j) for k in range(n)]
                output,cost=fft_via_two_scans(x)
                self.assertEqual(output,dft_direct(x))
                self.assertEqual(cost['one_way_scans'],2*(n.bit_length()-1))
                columns+=1
        self.assertEqual(columns,127)

    def test_twoscan_random_field(self):
        gen=random.Random(20261009)
        for n in [2,4,8,16,32,64,128,256]:
            for _ in range(6):
                x=[gen.randrange(P) for _ in range(n)]
                fast,cost=fft_via_two_scans(x)
                self.assertEqual(fast,dft_direct(x))
                self.assertEqual(cost['additions'],n*(n.bit_length()-1))
                self.assertEqual(cost['twiddle_table_entries'],n-1)

    def test_twoscan_ignores_input_structure(self):
        n=128
        inputs=[[0]*n, [1]*n, [i%2 for i in range(n)]]
        self.assertEqual(len({tuple(sorted(fft_via_two_scans(x)[1].items())) for x in inputs}),1)

    def test_scan_inverse_individual(self):
        gen=random.Random(117)
        for n in (2,3,8,17):
            for direction in ('forward','backward'):
                for _ in range(20):
                    x=[gen.randrange(P) for _ in range(n)]
                    a=[gen.randrange(P) for _ in range(n)]
                    b=[gen.randrange(1,P) for _ in range(n)]
                    y=scan_vector(x,direction,a,b)
                    self.assertEqual(inverse_scan_vector(y,direction,a,b),x)

    def test_invertibility_required(self):
        with self.assertRaises(ValueError):
            inverse_scan_vector([1,2],'forward',[1,1],[0,1])

    def test_random_interleaved_words(self):
        for n in (4,8,16):
            for t in range(5):
                for b in range(4):
                    result=word_certificate(random_word(n,t,b,seed=n*100+7*t+b))
                    self.assertLessEqual(result['max_sparse_row_support'],min(n,1<<t))
                    self.assertLessEqual(result['difference_rank'],b)

    def test_broadcast_dense_inverse(self):
        n=8
        u=[1]*n; v=[1]*n
        H=broadcast_matrix(u,v)
        iH=invert_mod(H)
        self.assertTrue(all(all(y!=0 for y in row) for row in iH))
        self.assertEqual(rank_mod(matrix_sub(iH,identity(n))),1)

    def test_hybrid_lower_bound(self):
        n=64
        self.assertEqual([minimum_broadcast_rank_budget(n,t) for t in range(7)],
                         [32,21,12,7,3,1,0])
        for n in (8,16,32,64,128,256,1024):
            for t in range(n.bit_length()+2):
                s=min(n,2**t)
                b=n//(s+1)
                self.assertGreater((b+1)*(s+1),n)
                if b:
                    self.assertLessEqual(b*(s+1),n)

    def test_vandermonde_witnesses(self):
        rnd=random.Random(883)
        count=0
        for n in (8,16,32,64):
            for t in range(5):
                s=2**t
                for b in range(n//(s+1)):
                    rr=[set(rnd.sample(range(n),rnd.randint(0,s))) for _ in range(b+1)]
                    cert=vander_certificate(n,s,b,rr)
                    self.assertEqual(cert['minor_rank'],b+1)
                    count+=1
        self.assertGreater(count,30)

    def test_permutation_and_broadcast_invalid(self):
        with self.assertRaises(ValueError): permutation_matrix([0,0,2])
        with self.assertRaises(ValueError): broadcast_matrix([1],[P-1])

    def test_bidirectional_sum_escape(self):
        for n in [4,8,16,32]:
            info=bidirectional_sum_escape(n)
            self.assertTrue(info['inverse_all_entries_nonzero'])
            self.assertEqual(info['inverse_nnz'],n*n)
            self.assertEqual(info['inverse_minus_diagonal_rank'],n)

    def test_two_prime_fft(self):
        p=2013265921
        for n in [2,4,8,16,32]:
            data=list(range(n))
            self.assertEqual(fft_via_two_scans(data,p,31)[0],dft_direct(data,p,31))

if __name__=='__main__':unittest.main()
