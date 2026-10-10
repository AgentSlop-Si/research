"""Reproducible tests of Phase 12 symbolic and finite-field certificates."""
import itertools
import json
import os
import random
import unittest
from cycle_minor_gate import (auxiliary_prime_root,check_green_inverse,
    determinant_polynomial, find_rectangle, generate_certificate,
    green_submatrix, is_prime, longest_monotone_subsequence_positions,
    rank_mod,permutation_cycles,linearize_perm,green_perm_submatrix,
    check_multi_green_inverse,permutation_from_ordered_cycles,
    find_sparse_avoiding_rectangle,fourier_prime_factor_grid,
    prime_power_three_minor,composite_two_green_certificate,
    composite_field_witness)

class Phase12Tests(unittest.TestCase):
    def test_erdos_szekeres_sharp_25(self):
        seq=[]
        for block in range(5):
            seq.extend(list(range(5*block+4,5*block-1,-1)))
        lis, _=longest_monotone_subsequence_positions(seq)
        self.assertEqual(len(lis),5)
        second = [0]*25
        for index,position in enumerate(seq):second[position]=index
        with self.assertRaises(ValueError):
            find_rectangle([list(range(25)),second],3)

    def test_separation_guaranteed_after_25(self):
        rng=random.Random(101)
        for n in [26,27,29,31,53,127]:
            for _ in range(15):
                a=list(range(n));b=list(range(n));rng.shuffle(a);rng.shuffle(b)
                witness=find_rectangle([a,b],3)
                self.assertEqual(len(witness['rows']),3)
                self.assertEqual(len(witness['cols']),3)
                self.assertEqual(len(set(witness['rows']+witness['cols'])),6)

    def test_every_three_minor_p7_p11_p13(self):
        for p in [7,11,13]:
            for R in itertools.combinations(range(p),3):
                for C in itertools.combinations(range(p),3):
                    self.assertTrue(determinant_polynomial(p,R,C)['cyclotomic_remainder_nonzero'],(p,R,C))

    def test_shifted_basis_green_full_inverse(self):
        rng=random.Random(3)
        q=1009
        for n in [5,7,11,19,29]:
            for _ in range(8):
                cyc=list(range(n));rng.shuffle(cyc)
                w=[rng.randrange(q) for _ in range(n)]
                self.assertTrue(check_green_inverse(cyc,w,q))

    def test_zero_weights_and_noncommuting_orders(self):
        q=1009; n=29
        a=list(range(n)); b=list(range(n-1,-1,-1))
        witness=find_rectangle([a,b],3)
        rows,cols=witness['rows'],witness['cols']
        mat=green_submatrix(a,[0]*n,rows,cols,q)
        self.assertEqual(rank_mod(mat,q),0)
        rng=random.Random(12)
        for cyc in [a,b]:
            for _ in range(20):
                w=[rng.randrange(q) for _ in range(n)]
                M=green_submatrix(cyc,w,rows,cols,q)
                self.assertLessEqual(rank_mod(M,q),1)

    def test_multi_cycle_monomial_inverses(self):
        rng=random.Random(24)
        q=1009
        for n in [7,13,29,37]:
            for _ in range(30):
                pi=list(range(n));rng.shuffle(pi)
                weights=[rng.randrange(q) for _ in range(n)]
                for cyc in permutation_cycles(pi):
                    val=1
                    for i in cyc: val=val*weights[i]%q
                    if val==1: weights[cyc[0]]=0
                self.assertTrue(check_multi_green_inverse(pi,weights,q))
                self.assertEqual(set(linearize_perm(pi)),set(range(n)))
        # Explicit fixed points, two-cycles, and mixed cycles, including zero weights
        pi=permutation_from_ordered_cycles([[0,4,7],[1,3],[2],[5,6,8,9]])
        w=[0,2,3,5,7,0,11,13,17,19]
        self.assertTrue(check_multi_green_inverse(pi,w,q))

    def test_parametric_two_green_multi_cycle_p29(self):
        rng=random.Random(91)
        p=29;q=1009
        for _ in range(40):
            p1=list(range(p));p2=list(range(p))
            rng.shuffle(p1);rng.shuffle(p2)
            order1,order2=linearize_perm(p1),linearize_perm(p2)
            certificate=find_rectangle([order1,order2],3)
            R,C=certificate['rows'],certificate['cols']
            self.assertTrue(determinant_polynomial(p,R,C)['cyclotomic_remainder_nonzero'])
            w1=[rng.randrange(q) for _ in range(p)]
            w2=[rng.randrange(q) for _ in range(p)]
            for perm,w in [(p1,w1),(p2,w2)]:
                for cyc in permutation_cycles(perm):
                    val=1
                    for i in cyc: val=val*w[i]%q
                    if val==1: w[cyc[0]]=0
            G1=green_perm_submatrix(p1,w1,R,C,q)
            G2=green_perm_submatrix(p2,w2,R,C,q)
            self.assertLessEqual(rank_mod(G1,q),1)
            self.assertLessEqual(rank_mod(G2,q),1)
            summat=[[(a+b)%q for a,b in zip(row1,row2)] for row1,row2 in zip(G1,G2)]
            self.assertLessEqual(rank_mod(summat,q),2)

    def test_parametric_no_two_green_p29_p31(self):
        for p in [29,31]:
            for seed in [0,7,118]:
                cert=generate_certificate(p,2,0,seed)
                self.assertTrue(cert['fourier_minor_cyclotomic']['cyclotomic_remainder_nonzero'])
                self.assertEqual(cert['finite_field_sample']['sum_block_rank'],2)
                self.assertNotEqual(cert['finite_field_sample']['dft_minor_det_nonzero'],0)
                self.assertTrue(all(s['full_inverse_identity_checked'] for s in cert['finite_field_sample']['green_samples']))

    def test_arbitrary_monomial_sparse_correction_p67(self):
        rng=random.Random(99)
        p=67
        for seed in range(20):
            perms=[]
            for _ in range(2):
                pi=list(range(p));rng.shuffle(pi)
                perms.append(pi)
            orders=[linearize_perm(pi) for pi in perms]
            correction=list(range(p));rng.shuffle(correction)
            supports=[[correction[i]] for i in range(p)]
            cert=find_sparse_avoiding_rectangle(orders,3,supports,1)
            R,C=cert['rows'],cert['cols']
            self.assertEqual(len(R),len(C))
            self.assertTrue(all(j not in supports[i] for i in R for j in C))
            self.assertTrue(determinant_polynomial(p,R,C)['cyclotomic_remainder_nonzero'])
            if seed==0:
                with open('witness_p67_sparse.json','w') as f:
                    json.dump({'orders':orders,'sparse_permutation':correction,
                               'rectangle':cert,
                               'dft_minor':determinant_polynomial(p,R,C)},f,indent=2)

    def test_sparse_plus_rank_one_p127(self):
        rng=random.Random(1012)
        p=127
        for _ in range(4):
            perms=[]
            for _ in range(2):
                pi=list(range(p));rng.shuffle(pi)
                perms.append(pi)
            correction=list(range(p));rng.shuffle(correction)
            supp=[[correction[i]] for i in range(p)]
            cert=find_sparse_avoiding_rectangle([linearize_perm(pi) for pi in perms],4,supp,1)
            self.assertTrue(determinant_polynomial(p,cert['rows'],cert['cols'])['cyclotomic_remainder_nonzero'])

    def test_prime_factor_submatrix_all_prime_adic_parities(self):
        cases=[(29,29,1,29),(2*29,29,2,29),
               (29**2,29,1,29**2),(2*29**2,29,2,29**2),
               (29**3,29,29,29),(2*29**3,29,58,29)]
        rng=random.Random(71)
        for n,p,spacing,order in cases:
            grid=fourier_prime_factor_grid(n,p)
            self.assertEqual(grid['spacing'],spacing)
            self.assertEqual(grid['root_order'],order)
            self.assertEqual(grid['frequency_multiplier']%p,n//p**grid['valuation']%p)
            for _ in range(60):
                R=rng.sample(range(p),3);C=rng.sample(range(p),3)
                cert=prime_power_three_minor(n,p,R,C)
                self.assertTrue(cert['determinant_nonzero_over_complex'],(n,R,C))

    def test_composite_two_solver_gate(self):
        for n,p,seed in [(58,29,1),(841,29,2),(1682,29,3),(24389,29,4)]:
            cert=composite_two_green_certificate(n,p,seed)
            self.assertTrue(cert['exact_fourier_minor']['determinant_nonzero_over_complex'])
            self.assertEqual(len(cert['original_rows']),3)
            self.assertEqual(len(cert['original_cols']),3)

    def test_composite_field_witness_p_squared(self):
        for n,p in [(58,29),(841,29),(1682,29)]:
            cert=composite_field_witness(n,p,20)
            sample=cert['modular_sample']
            self.assertTrue(sample['prime_field_primitive_root_verified'])
            self.assertNotEqual(sample['dft_minor_det'],0)
            self.assertTrue(all(r<=1 for r in sample['green_block_ranks']))
            self.assertLessEqual(sample['sum_green_block_rank'],2)
            if n==841:
                with open('witness_n841_prime_square.json','w') as f:json.dump(cert,f,indent=2)

    def test_composite_sparse_correction(self):
        rng=random.Random(347)
        n=134;p=67
        grid=fourier_prime_factor_grid(n,p)
        inv={v:i for i,v in enumerate(grid['indices'])}
        for _ in range(12):
            perms=[]
            for stage in range(2):
                pi=list(range(n));rng.shuffle(pi)
                perms.append(pi)
            orders=[[inv[v] for v in linearize_perm(pi) if v in inv] for pi in perms]
            correction=list(range(n));rng.shuffle(correction)
            support=[[inv[correction[x]]] if correction[x] in inv else []
                     for x in grid['indices']]
            rect=find_sparse_avoiding_rectangle(orders,3,support,1)
            self.assertTrue(prime_power_three_minor(n,p,rect['rows'],rect['cols'])['determinant_nonzero_over_complex'])

    def test_two_layer_escape(self):
        from product_escape_control import sample_product_escape
        for seed in [1202,1203,1204,1205,1206]:
            result=sample_product_escape(29,seed)
            self.assertLessEqual(result['stage1_crosscut_rank'],2)
            self.assertEqual(result['product_crosscut_rank'],3)
            self.assertNotEqual(result['product_crosscut_det'],0)

    def test_rank_one_correction_p53(self):
        cert=generate_certificate(53,2,1,9)
        self.assertEqual(cert['rectangle']['minor_size'],4)
        self.assertTrue(cert['fourier_minor_cyclotomic']['cyclotomic_remainder_nonzero'])
        self.assertLessEqual(cert['finite_field_sample']['sum_block_rank']+1,3)

    def test_three_green_p2411(self):
        self.assertTrue(is_prime(2411))
        cert=generate_certificate(2411,3,0,11)
        self.assertEqual(cert['rectangle']['minor_size'],4)
        self.assertGreaterEqual(cert['rectangle']['subsequence_length'],8)
        self.assertLessEqual(cert['finite_field_sample']['sum_block_rank'],3)
        self.assertNotEqual(cert['finite_field_sample']['dft_minor_det_nonzero'],0)

if __name__=='__main__':
    unittest.main(verbosity=2)
