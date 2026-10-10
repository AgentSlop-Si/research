from __future__ import annotations
import hashlib
import random
import unittest
from pathlib import Path

from metaplectic_bruhat import (
    all_entries_nonzero, bruhat_certificate, chirp_operator, collapse_word,
    complexity_class, count_bruhat_cells, direct_big_cell_kernel,
    direct_borel_kernel, field_for_length, fourier_matrix, identity,
    is_easy_borel, is_monomial, lower_shear, mat_mul, operator_product,
    projectively_equal, random_sl2_word, scale_operator, sl2_elements,
    sl2_mul, unique_lul_solution, unique_ulu_solution, upper_shear,
    verify_projective_word, weil_operator, weyl_element,
)

class MetaplecticBruhatTests(unittest.TestCase):
    def test_bruhat_cell_counts(self):
        for n in (5,7,11):
            borel,big=count_bruhat_cells(n)
            self.assertEqual(borel,n*(n-1))
            self.assertEqual(big,n*n*(n-1))
            self.assertEqual(borel+big,n*(n*n-1))

    def test_direct_kernel_formulas(self):
        for n in (5,7,11):
            p,w=field_for_length(n)
            for s in sl2_elements(n):
                got=weil_operator(s,n,p,w)
                want=direct_borel_kernel(s,n,p,w) if is_easy_borel(s,n) else direct_big_cell_kernel(s,n,p,w)
                self.assertEqual(got,want,(n,s))

    def test_projective_group_law_exhaustive_n5(self):
        n=5;p,w=field_for_length(n);elems=sl2_elements(n)
        for a in elems:
            ra=weil_operator(a,n,p,w)
            for b in elems:
                lhs=mat_mul(ra,weil_operator(b,n,p,w),p)
                rhs=weil_operator(sl2_mul(a,b,n),n,p,w)
                self.assertTrue(projectively_equal(lhs,rhs,p),(a,b))

    def test_projective_group_law_random_larger(self):
        rng=random.Random(23001)
        for n in (7,11,13):
            p,w=field_for_length(n);elems=sl2_elements(n)
            for _ in range(500):
                a=elems[rng.randrange(len(elems))];b=elems[rng.randrange(len(elems))]
                self.assertTrue(projectively_equal(mat_mul(weil_operator(a,n,p,w),weil_operator(b,n,p,w),p),weil_operator(sl2_mul(a,b,n),n,p,w),p))

    def test_borel_exactly_monomial_big_cell_fourier_dense(self):
        for n in (5,7,11):
            p,w=field_for_length(n)
            for s in sl2_elements(n):
                op=weil_operator(s,n,p,w)
                if is_easy_borel(s,n):
                    self.assertTrue(is_monomial(op,p),(n,s))
                else:
                    self.assertTrue(all_entries_nonzero(op,p),(n,s))
                    self.assertEqual(complexity_class(s,n),'fourier_equivalent')

    def test_unique_three_shear_decompositions(self):
        for n in (5,7,11,13):
            self.assertEqual(unique_lul_solution(n),(1,n-1,1))
            self.assertEqual(unique_ulu_solution(n),(n-1,1,n-1))

    def test_three_shear_operator_contains_hard_middle(self):
        for n in (5,7,11,13):
            p,w=field_for_length(n)
            x,y,z=unique_lul_solution(n)
            word=[lower_shear(x,n),upper_shear(y,n),lower_shear(z,n)]
            self.assertTrue(projectively_equal(operator_product(word,n,p,w),fourier_matrix(n,p,w),p))
            self.assertEqual(complexity_class(word[0],n),'linear_monomial')
            self.assertEqual(complexity_class(word[1],n),'fourier_equivalent')
            self.assertEqual(complexity_class(word[2],n),'linear_monomial')

    def test_all_easy_words_stay_easy(self):
        rng=random.Random(23002)
        for n in (5,7,11):
            for length in (1,2,3,8,20):
                for _ in range(100):
                    word=[]
                    for _ in range(length):
                        a=rng.randrange(1,n);t=rng.randrange(n)
                        word.append(sl2_mul(lower_shear(t,n),(a,0,0,pow(a,-1,n)),n))
                    self.assertTrue(is_easy_borel(collapse_word(word,n),n))
                    self.assertNotEqual(collapse_word(word,n),weyl_element(n))

    def test_arbitrary_words_collapse_to_one_normal_form(self):
        rng=random.Random(23003)
        for n in (5,7,11):
            p,w=field_for_length(n)
            for length in (2,3,5,12):
                for _ in range(80):
                    word=random_sl2_word(n,length,rng)
                    scalar=verify_projective_word(word,n,p,w)
                    self.assertNotEqual(scalar,0)
                    final=collapse_word(word,n)
                    op=weil_operator(final,n,p,w)
                    self.assertEqual(is_monomial(op,p),is_easy_borel(final,n))

    def test_predecessor_hash(self):
        path=Path(__file__).with_name('PRIOR_v22_COMPLETE.zip')
        self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),'e1d30f08aa720c4e492a0e268b343d08d52bd80ecb126ab3fbe6c27097f36906')

if __name__=='__main__':unittest.main(verbosity=2)
