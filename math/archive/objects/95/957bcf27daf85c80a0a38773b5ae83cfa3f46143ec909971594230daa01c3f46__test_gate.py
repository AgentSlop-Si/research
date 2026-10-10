import unittest,random,math
from itertools import combinations
from research_gate import *

def bareiss_det(A):
    n=len(A)
    if not n:return 1
    B=[list(map(int,row)) for row in A]
    s=1;prev=1
    for k in range(n-1):
        if not B[k][k]:
            r=next((i for i in range(k+1,n) if B[i][k]),None)
            if r is None:return 0
            B[k],B[r]=B[r],B[k];s=-s
        z=B[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                num=B[i][j]*z-B[i][k]*B[k][j]
                assert num%prev==0
                B[i][j]=num//prev
        for i in range(k+1,n):B[i][k]=0
        prev=z
    return s*B[-1][-1]

class StructuralResearch(unittest.TestCase):
    def test_parity_permutation_theorem(self):
        p=65537
        for n in (4,8,16,32,64):
            s=scalar_stage(n)
            for perm in (bitrev(n),parity_perm(n,n+471)):
                q=perm_conjugate(s,perm)
                for k in range(1,n):
                    want=min(k,n-k)
                    up=rank_mod([row[k:] for row in q[:k]],p)
                    down=rank_mod([row[:k] for row in q[k:]],p)
                    self.assertEqual((up,down),(want,want),(n,k,perm))
                    if k<=n//2:
                        evens=sorted(perm[:k]);odds=[r+1 for r in evens]
                    else:
                        odds=sorted(perm[k:]);evens=[r-1 for r in odds]
                    U=[[s[i][j] for j in odds] for i in evens]
                    V=[[s[i][j] for j in evens] for i in odds]
                    self.assertEqual(det_mod(U,p),2%p)
                    self.assertEqual(det_mod(V,p),(-1)**(want-1)%p)

    def test_scalar_scan_det_and_executor(self):
        p=65537; rng=random.Random(303)
        for n in (2,4,8,16,32,64):
            s=scalar_stage(n)
            self.assertEqual(det_mod(s,p),(2**(n+1)-1)%p)
            a=[1]*n;b=[1]*n;c=[2]*n;e=[1]*n;d=[3]*n
            for _ in range(3):
                x=[rng.randrange(p) for _ in range(n)]
                self.assertEqual(matvec(s,x,p),apply_scan(a,b,c,e,d,x,p))

    def test_sparse_augmentation_exact(self):
        p=12289; rng=random.Random(42)
        for n in (2,3,4,7,8,12):
            for _ in range(3):
                a,b,c,e,d=([rng.randrange(-3,4) for _ in range(n)] for _ in range(5))
                S=matrix_stage(a,b,c,e,d,p)
                K=augmented_stage_matrix(a,b,c,e,d,p)
                self.assertEqual(det_mod(S,p),det_mod(K,p))
                if n<=8:
                    Si=[[a[i]*b[j] if i>j else c[i]*e[j] if i<j else d[i] for j in range(n)] for i in range(n)]
                    D=bareiss_det(Si)
                    B=3
                    self.assertLessEqual(D*D,3**(3*n)*B**(4*n))

    def test_fourier_two_by_two_formula(self):
        p=65537
        for n in (4,8,16,32):
            w=root(n,p)
            F=fft(n,w,p)
            rng=random.Random(n)
            for _ in range(150):
                r1,r2=sorted(rng.sample(range(n),2))
                c1,c2=sorted(rng.sample(range(n),2))
                self.assertEqual(minor2(F,r1,r2,c1,c2,p),fourier_minor_formula(n,w,p,r1,r2,c1,c2))
            self.assertEqual(zero_minor_count_bruteforce(n),zero_minor_count_formula(n))

    def test_quasiseparable_minor_characterization_and_zero_case(self):
        p=12289
        for n in (8,16):
            for S in (block2_stage(n,p,39+n),scalar_stage(n)):
                self.assertFalse(all_qs_minor_violations(S,p,limit=1))
                inv=inverse_mod(S,p)
                self.assertFalse(all_qs_minor_violations(inv,p,limit=1))
            bad=fft(n,root(n,p),p)
            self.assertTrue(all_qs_minor_violations(bad,p,limit=1))

    def test_inverse_stage_quotient_identity(self):
        p=12289
        for n in (8,16):
            perm=bitrev(n)
            candidates=(
                [block2_stage(n,p,n+i*101) for i in range(3)],
                [scalar_stage(n,1,2,3),block2_stage(n,p,n+51),scalar_stage(n,1,3,4)]
            )
            for S1,S2,S3 in candidates:
                target=triple_stage_product_simple(S1,S2,S3,perm,p)
                A=inverse_mod(S1,p);C=inverse_mod(S3,p)
                self.assertFalse(all_qs_minor_violations(A,p,limit=1))
                self.assertFalse(all_qs_minor_violations(C,p,limit=1))
                M=inverse_stage_middle(A,C,target,perm,p)
                self.assertEqual(M,[[z%p for z in row] for row in S2])
                self.assertFalse(all_qs_minor_violations(M,p,limit=1))
                self.assertEqual(det_mod(target,p),det_mod(S1,p)*det_mod(S2,p)*det_mod(S3,p)%p)
            # Actual Fourier fails the identity choice A=C=I, but this DOES NOT
            # exclude other inverses A,C.
            ident=[[int(i==j) for j in range(n)] for i in range(n)]
            F=fft(n,root(n,p),p)
            self.assertTrue(all_qs_minor_violations(inverse_stage_middle(ident,ident,F,perm,p),p,limit=1))

    def test_exterior_square_cauchy_binet(self):
        p=12289; rng=random.Random(39)
        for n in (4,8,16):
            F=fft(n,root(n,p),p)
            for it in range(4):
                A=[[rng.randrange(p) for _ in range(n)] for _ in range(n)]
                C=[[rng.randrange(p) for _ in range(n)] for _ in range(n)]
                triple=matmul(matmul(A,F,p),C,p)
                rows=tuple(sorted(rng.sample(range(n),2)))
                cols=tuple(sorted(rng.sample(range(n),2)))
                direct=compound_entry(triple,p,rows,cols)
                by_compound=exterior_cauchy_binet(A,F,C,rows,cols,p)
                self.assertEqual(direct,by_compound)


class ThreeStageAllLengthObstruction(unittest.TestCase):
    def test_uniform_boolean_cut_across_eight_scales(self):
        from uniform_cut import test_cut
        for n in (32,64,128,256,512,1024,2048,4096,8192):
            obj=test_cut(n)
            self.assertEqual(obj['removed_scalar_channels'],12*(n//32)+1)
            self.assertEqual(obj['rank_deficit'],n//32-1)

    def test_independent_dependency_dag(self):
        from verify_uniform_cut_independent import verify
        for n in (32,64,128,256,512):
            self.assertTrue(verify(n)['disconnected'])

    def test_uniform_wire_count_and_binary_sets(self):
        from uniform_cut import cut_sets,wire_list,BASE_INPUT_RESIDUES,FINAL_HIGH_BLOCKS
        for n in (32,64,128,256,512):
            P=bitrev(n);m=n//32;a=cut_sets(n)
            self.assertEqual({P[x]%32 for x in a['sources']},set(BASE_INPUT_RESIDUES))
            self.assertEqual(len(wire_list(n)),12*m+1)
            self.assertEqual(len(a['x2']),7*m)
            self.assertEqual({int(f'{s:05b}'[::-1],2) for s in range(21) if int(f'{s:05b}'[::-1],2)>=19},set(FINAL_HIGH_BLOCKS))

    def test_uniform_fourier_vandermonde_mod_two_primes(self):
        for n in (32,64,128):
            m=n//32;R=range(19*m,n);C=range(13*m)
            for p in (12289,65537):
                w=root(n,p)
                M=[[pow(w,i*j,p) for j in C] for i in R]
                self.assertNotEqual(det_mod(M,p),0,(n,p))
                self.assertEqual(rank_mod(M,p),13*m)

    def test_network_certificates_both_fields(self):
        import json
        from pathlib import Path
        here=Path(__file__).resolve().parent
        for n in (64,128):
            obj=json.loads((here/f'NETWORK_CERTIFICATE_N{n}.json').read_text())
            self.assertLess(obj['rank_upper_bound'],len(obj['rows']))
            for proof in obj['primes']:
                p=proof['prime'];w=root(n,p)
                self.assertEqual(w,proof['primitive_root'])
                M=[[pow(w,i*j,p) for j in obj['columns']] for i in obj['rows']]
                self.assertEqual(det_mod(M,p),proof['determinant'])

if __name__=='__main__':unittest.main(verbosity=2)
