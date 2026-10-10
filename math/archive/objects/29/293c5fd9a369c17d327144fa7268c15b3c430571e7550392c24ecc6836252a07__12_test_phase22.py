import math, pathlib, random, sys, unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from phase22_gram import *

class ExactQuadraticGate(unittest.TestCase):
    def test_fourier_square_is_reflection(self):
        for n in (4,8,16,32,64,128):
            F=fft_matrix(n)
            self.assertEqual(matmul(transpose(F),F),reverse_matrix(n))
            self.assertEqual(matmul(F,F),reverse_matrix(n))

    def test_weighted_cycle_solve(self):
        for n in (8,16,32,64,128):
            green=seeded_green_sum(n,30,2)
            for term in green.terms:
                rng=random.Random(2026)
                x=[rng.randrange(MOD) for _ in range(n)]
                y=term.apply(x)
                # Undo output gauge; verify cyclic bidiagonal equation.
                local=[y[term.order[j]]*pow(term.left[j],-1,MOD)%MOD for j in range(n)]
                source=[term.right[j]*x[term.order[j]]%MOD for j in range(n)]
                self.assertTrue(all((local[j]-term.weights[j]*local[j-1]-source[j])%MOD==0 for j in range(n)))

    def test_hidden_phase_and_permutation_recovered(self):
        for n in (8,16,32,64):
            for seed in (17,29,2026):
                rng=random.Random(seed)
                A=dense_from_apply(seeded_green_sum(n,seed,2),n)
                perm=list(range(n));rng.shuffle(perm)
                q=[rng.randrange(1,MOD) for _ in range(n)]
                F=fft_matrix(n)
                B=make_positive_control(A,perm,q,F)
                self.assertEqual(apply_sandwich(A,q,perm,B),F)
                K,C=quadratic_form_data(A,B)
                status,pr=permutation_fingerprint_gate(K,C)
                self.assertEqual(status,'candidate')
                self.assertEqual(pr,perm)
                qr=recover_mask(K,C,pr)
                self.assertIsNotNone(qr)
                self.assertTrue(qr==q or qr==[(-x)%MOD for x in q])
                Mr=apply_sandwich(A,qr,pr,B)
                if Mr!=F:
                    qr=[(-x)%MOD for x in qr]
                    Mr=apply_sandwich(A,qr,pr,B)
                self.assertEqual(Mr,F)
                self.assertEqual(weyl_defect_counts(Mr),(0,0))

    def test_independent_green_cycles_are_rejected_for_fixed_samples(self):
        for n in (8,16,32,64):
            for seed in (11,17,23,29,43,2026):
                A=dense_from_apply(seeded_green_sum(n,seed,2),n)
                B=dense_from_apply(seeded_green_sum(n,seed+701,2),n)
                K,C=quadratic_form_data(A,B)
                status,perm=permutation_fingerprint_gate(K,C)
                self.assertEqual(status,'excluded',(n,seed,status))
                self.assertIsNone(perm)

    def test_quadratic_gate_is_not_fourier_sufficient(self):
        for n in (8,16,32,64):
            rng=random.Random(2026)
            A=dense_from_apply(seeded_green_sum(n,2026),n)
            p=list(range(n));rng.shuffle(p)
            q=[rng.randrange(1,MOD) for _ in range(n)]
            F=fft_matrix(n)
            # U is bilinearly Fourier-orthogonal, and U00=F00,
            # yet the second Weyl equation must fail.
            U=[row[:] for row in F]
            for i in range(1,n,2): U[i]=[(-v)%MOD for v in U[i]]
            self.assertEqual(matmul(transpose(U),U),reverse_matrix(n))
            self.assertEqual(U[0][0],F[0][0])
            B=make_positive_control(A,p,q,U)
            K,C=quadratic_form_data(A,B)
            state,pp=permutation_fingerprint_gate(K,C)
            self.assertEqual((state,pp),('candidate',p))
            mask=recover_mask(K,C,p)
            self.assertIsNotNone(mask)
            rec=apply_sandwich(A,mask,p,B)
            if rec[0][0]!=F[0][0]:
                mask=[(-v)%MOD for v in mask]
                rec=apply_sandwich(A,mask,p,B)
            self.assertEqual(rec,U)
            d1,d2=weyl_defect_counts(rec)
            self.assertEqual(d1,0)
            self.assertGreater(d2,0)

    def test_signature_ambiguity_is_not_misreported_as_veto(self):
        n=8;F=fft_matrix(n)
        A=identity(n);B=F
        K,C=quadratic_form_data(A,B)
        # K=I has zero offdiagonal; row fingerprints identical.
        self.assertEqual(permutation_fingerprint_gate(K,C)[0],'ambiguous')
        self.assertIsNone(recover_mask(K,C,list(range(n))))

class RealGramObstruction(unittest.TestCase):
    @staticmethod
    def positive_greens(n,seed):
        rng=np.random.default_rng(seed)
        A=np.zeros((n,n))
        for rho in (.75,.8):
            order=rng.permutation(n)
            S=np.zeros((n,n))
            for j in range(n): S[order[j],order[j-1]]=1
            A+=np.linalg.inv(np.eye(n)-rho*S)
        return A

    def test_positive_independently_ordered_green_sums_have_connected_gram(self):
        for n in (4,8,16,32,64):
            A=self.positive_greens(n,100+n)
            self.assertGreater(np.min(A),0)
            K=A.T@A
            self.assertGreater(np.min(K),0)
            self.assertGreater(np.linalg.svd(A,compute_uv=False).min(),0)

    def test_rank_real_and_imag_and_sharp_orthogonal_factorization(self):
        for n in (4,8,16,32,64):
            w=np.exp(-2j*np.pi/n)
            F=np.array([[w**(i*j)/np.sqrt(n) for j in range(n)] for i in range(n)])
            self.assertEqual(np.linalg.matrix_rank(F.real,tol=1e-8),n//2+1)
            self.assertEqual(np.linalg.matrix_rank(F.imag,tol=1e-8),n//2-1)
            H=F.real+2*F.imag
            _,O=np.linalg.eigh(H)
            Q=np.diag(O.T@F@O)
            recon=O@np.diag(Q)@O.T
            self.assertLess(np.max(np.abs(F-recon)),2e-12)
            self.assertLess(np.max(np.abs(O.T@O-np.eye(n))),1e-13)
            self.assertEqual(sum(abs(v.imag)<1e-8 for v in Q),n//2+1)
            self.assertEqual(sum(abs(v.real)<1e-8 for v in Q),n//2-1)

if __name__=='__main__':unittest.main()

class ParityReduction(unittest.TestCase):
    def test_exact_f_equals_linear_haar_phase_real_residual(self):
        from phase22_parity import parity_factors,apply_H,apply_Ht
        for n in (4,8,16,32,64,128):
            H,q,C=parity_factors(n)
            Qc=[[q[i]*v%MOD for v in C[i]] for i in range(n)]
            self.assertEqual(matmul(H,Qc),fft_matrix(n))
            self.assertEqual(matmul(transpose(H),H),identity(n))
            self.assertEqual(matmul(transpose(C),C),identity(n))
            x=[(j*j*83+19)%MOD for j in range(n)]
            hvec=[sum(H[i][j]*x[j] for j in range(n))%MOD for i in range(n)]
            htvec=[sum(H[j][i]*x[j] for j in range(n))%MOD for i in range(n)]
            self.assertEqual(apply_H(x),hvec)
            self.assertEqual(apply_Ht(x),htvec)
            self.assertEqual(apply_Ht(apply_H(x)),x)

    def test_residual_entropy_lower_bound(self):
        from phase22_parity import residual_entropy
        for n in (8,16,32,64,128,256):
            H,lower=residual_entropy(n)
            self.assertGreaterEqual(H+1e-9,lower)
            self.assertLess(H,n*math.log2(n)+1e-9)

class RealCovariance(unittest.TestCase):
    def test_exact_real_covariance_and_seed(self):
        from phase22_parity import parity_factors,apply_R,real_C_first_column,real_covariance_gate,cyclic_shift
        for n in (4,8,16,32,64,128):
            _,_,C=parity_factors(n)
            e0=[1]+[0]*(n-1)
            self.assertEqual([row[0] for row in C],real_C_first_column(n))
            oracle=lambda x:[sum(C[i][j]*x[j] for j in range(n))%MOD for i in range(n)]
            for k in (0,1,3,n-1):
                e=[0]*n;e[k]=1
                self.assertEqual(oracle(cyclic_shift(e)),apply_R(oracle(e)))
            report=real_covariance_gate(oracle,n,trials=2)
            self.assertTrue(report['passes_sample'],report)
            self.assertEqual(report['circuit_calls'],5)

    def test_one_equation_does_not_fix_normalization(self):
        from phase22_parity import parity_factors,real_covariance_gate
        for n in (8,16,32):
            _,_,C=parity_factors(n)
            c=7
            oracle=lambda x:[c*sum(C[i][j]*x[j] for j in range(n))%MOD for i in range(n)]
            report=real_covariance_gate(oracle,n)
            self.assertEqual(report['defect_entries'],0)
            self.assertFalse(report['calibration'])
            self.assertFalse(report['passes_sample'])
