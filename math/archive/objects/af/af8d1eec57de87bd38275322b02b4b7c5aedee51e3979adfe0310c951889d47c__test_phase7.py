#!/usr/bin/env python3
"""Independent modular test suite of Phase 7 construction and certificates."""
import unittest,random,math
from phase6_exact import P,root_of_unity,independent_full_dft,hankel_rank
from phase7_rank_fusion import (Counter, root_table, sample_dechirped_rank,
    exact_green_rank_fused, count_phase_modes, chirp_phase, dechirp)
from phase7_hidden_shift_detector import (unknown_shift_rank1_transform,
    cyclic_ratio_shift, cyclic_projective_shift, infer_shift_rank1, invert_many)


def direct_dft(x):
    n=len(x);root=root_of_unity(n)
    wn=pow(root,P-2,P)
    power=[pow(wn,i,P) for i in range(n)]
    return [sum(x[j]*power[(j*k)%n] for j in range(n))%P for k in range(n)]


def field_rank(v):
    mat=[list(row) for row in v]
    k=len(mat);m=len(mat[0]);r=0
    for col in range(m):
        pivot=next((i for i in range(r,k) if mat[i][col]),None)
        if pivot is None:continue
        mat[r],mat[pivot]=mat[pivot],mat[r]
        z=pow(mat[r][col],P-2,P)
        for j in range(col,m):mat[r][j]=mat[r][j]*z%P
        for i in range(r+1,k):
            coeff=mat[i][col]
            if coeff:
                for j in range(col,m):mat[i][j]=(mat[i][j]-coeff*mat[r][j])%P
        r+=1
    return r


def reconstruct_v(x,m,a,beta):
    n=len(x)
    return list(dechirp(x,m,a,beta,root_table(n,root_of_unity(n),None),None))


class Phase7ProofTests(unittest.TestCase):
    def test_rank_adaptive_exact_all_modes(self):
        count=0
        for q,m in [(32,4),(64,4),(128,8),(256,8),(512,8),(1024,16),(2048,16)]:
            k=q//m
            for rank in (0,1,2,min(4,m)):
                for shear in (0,1,3):
                    for seed in (5,19):
                        if rank==0:x=[0]*q
                        else:
                            g=[(shear*t)%k for t in range(m)]
                            x,_,_=sample_dechirped_rank(k,m,rank,seed=seed+q,a=3,beta=7,shifts=g)
                        shifts=[(shear*t)%k for t in range(m)]
                        got,factors,c=exact_green_rank_fused(x,m,rank,a=3,beta=7,
                            shifts=shifts,return_factors=True)
                        self.assertEqual(got,independent_full_dft(x))
                        self.assertEqual(len(factors[1]),rank)
                        if rank>0:
                            self.assertEqual(count_phase_modes(x,m,a=3,beta=7),m)
                            # Audit factorized matrix over original raw input.
                            U,H=factors;v=reconstruct_v(x,m,3,7)
                            for b in range(k):
                                for t in range(m):
                                    qpos=(b+shifts[t])%k
                                    self.assertEqual(v[b][t],sum(U[qpos][i]*H[i][t]
                                                                    for i in range(rank))%P)
                        count+=1
        print('PASS modular rank/exact cases',count)

    def test_hidden_shift_discovery_unknown_schedules(self):
        cases=0
        for q,m in [(32,4),(64,4),(128,8),(256,8),(512,8),(1024,16),(2048,16),(4096,16)]:
            k=q//m
            for choice in range(6):
                a=[1,3,5][choice%3];beta=choice*11
                rng=random.Random(31*q+choice)
                g=rng.sample(range(k),m) # distinct shifts give generic full column rank
                x,_,_=sample_dechirped_rank(k,m,1,seed=131*q+choice,
                                              a=a,beta=beta,shifts=g)
                got,params,c=unknown_shift_rank1_transform(x,m,a,beta,return_params=True)
                self.assertEqual(got,independent_full_dft(x))
                self.assertEqual(c.inversions,1)
                self.assertEqual(count_phase_modes(x,m,a,beta),m)
                # The original dechirped matrix generically has MAX rank M.
                raw=reconstruct_v(x,m,a,beta)
                self.assertEqual(field_rank(raw),m)
                f,h,found_g=params
                for b in range(k):
                    for t in range(m):
                        self.assertEqual(raw[b][t],f[(b+found_g[t])%k]*h[t]%P)
                cases+=1
        print('PASS unknown shift/full-rank cases',cases)

    def test_zero_columns_and_all_zero(self):
        for k,m in [(16,4),(32,8),(64,8)]:
            a=1;beta=0;g=[(t*t)%k for t in range(m)]
            x,U,H=sample_dechirped_rank(k,m,1,seed=k,shifts=g)
            q=k*m;tab=root_table(q,root_of_unity(q),None)
            for t in (1,m-1):
                for b in range(k):x[b*m+t]=0
            got,params,c=unknown_shift_rank1_transform(x,m,return_params=True)
            self.assertEqual(got,independent_full_dft(x))
            self.assertEqual(params[1][1],0)
            self.assertEqual(params[1][m-1],0)
            self.assertEqual(c.inversions,1)
            got,params,c=unknown_shift_rank1_transform([0]*q,m,return_params=True)
            self.assertEqual(got,[0]*q);self.assertEqual(c.inversions,0)

    def test_exact_certification_and_failure(self):
        k,m=32,8;g=[t*t%k for t in range(m)]
        x,_,_=sample_dechirped_rank(k,m,1,seed=19,shifts=g)
        for j in (0,k*m-1,31*m+7,3*m+5):
            bad=x.copy();bad[j]=(bad[j]+1)%P
            got,c=unknown_shift_rank1_transform(bad,m)
            self.assertIsNone(got)
        # Generic rank-2 input must fail rank-1 detector, even if shifts known.
        x,_,_=sample_dechirped_rank(k,m,2,seed=22,shifts=g)
        got,c=exact_green_rank_fused(x,m,1,shifts=g)
        self.assertIsNone(got)
        got,c=exact_green_rank_fused(x,m,2,shifts=g)
        self.assertEqual(got,independent_full_dft(x))
        got,c=unknown_shift_rank1_transform(x,m)
        self.assertIsNone(got)
        # Arbitrary all-nonzero raw inputs do not magically become rank 1.
        rng=random.Random(4)
        for q,m in [(64,4),(256,8)]:
            x=[rng.randrange(1,P) for _ in range(q)]
            got,c=unknown_shift_rank1_transform(x,m)
            self.assertIsNone(got)

    def test_ratio_cross_product_and_batch_inv(self):
        rng=random.Random(98)
        for k in [8,16,32,64,128]:
            f=[rng.randrange(1,P) for _ in range(k)]
            for _ in range(8):
                shift=rng.randrange(k);factor=rng.randrange(1,P)
                g=[factor*f[(j+shift)%k]%P for j in range(k)]
                found=cyclic_ratio_shift(f,g,None)
                self.assertIsNotNone(found)
                self.assertTrue(all(g[j]*f[found]%P==g[0]*f[(j+found)%k]%P
                                    for j in range(k)))
            g=f.copy();g[-1]=(g[-1]+1)%P
            self.assertIsNone(cyclic_ratio_shift(f,g,None))
        for n in [1,2,8,32,256]:
            v=[rng.randrange(1,P) for _ in range(n)];counter=Counter()
            got=invert_many(v,counter)
            self.assertEqual(counter.inversions,1)
            self.assertTrue(all(a*b%P==1 for a,b in zip(v,got)))

    def test_sparse_support_gap_recognition(self):
        rng=random.Random(101)
        for k in (8,16,32,64):
            for support in (1,2,3,5,k//2,k):
                for repeat in range(7):
                    f=[0]*k
                    for i in rng.sample(range(k),min(support,k)):
                        f[i]=rng.randrange(1,P)
                    g=rng.randrange(k);h=rng.randrange(1,P)
                    query=[h*f[(b+g)%k]%P for b in range(k)]
                    found=cyclic_projective_shift(f,query,None)
                    self.assertIsNotNone(found)
                    anchor=next(i for i,v in enumerate(query) if v)
                    self.assertTrue(all(query[b]*f[(anchor+found)%k]%P==
                            query[anchor]*f[(b+found)%k]%P for b in range(k)))
                    # Corrupt a value or support site; certify no false accept.
                    if min(support,k)>=3 and repeat%2==0:
                        bad=query.copy()
                        nz=[i for i,x in enumerate(bad) if x]
                        bad[nz[1]]=(bad[nz[1]]+1)%P
                        self.assertIsNone(cyclic_projective_shift(f,bad,None))
        # Sparse prototype with a single populated dechirped block.
        k,m=32,8
        for nz in (1,2,5,10):
            f=[0]*k
            for i in range(nz):f[(i*i+7*i)%k]=i+1
            h=[(t*t+1)%P for t in range(m)]
            g=[(t*t*3+5*t)%k for t in range(m)]
            q=k*m;tab=root_table(q,root_of_unity(q),None)
            x=[]
            for b in range(k):
                for t in range(m):
                    val=h[t]*f[(b+g[t])%k]%P
                    x.append(val*pow(chirp_phase(q,m,1,0,b,t,tab),P-2,P)%P)
            got,c=unknown_shift_rank1_transform(x,m)
            self.assertEqual(got,independent_full_dft(x))

    def test_direct_dft_independent(self):
        rng=random.Random(100)
        for q,m in [(16,2),(32,4),(64,4),(128,8)]:
            k=q//m
            for r in [1,2]:
                g=[(7*t*t+5*t)%k for t in range(m)]
                x,_,_=sample_dechirped_rank(k,m,r,seed=24+q,shifts=g)
                got,c=exact_green_rank_fused(x,m,r,shifts=g)
                self.assertEqual(got,direct_dft(x))

    def test_max_hankel_rank_explicit_and_generic(self):
        # Explicit single endpoint sample gives antitriangular nonsingular Hankel.
        for q,m in [(64,4),(128,8)]:
            k=q//m;h=q//2;b_star=k//2-1
            # Only t=M-1 in the central block; choose U support so shear maps it.
            g=[t*t%k for t in range(m)];t=m-1
            u=[0]*k;u[(b_star+g[t])%k]=1
            hv=[0]*m;hv[t]=1
            table=root_table(q,root_of_unity(q),None)
            x=[]
            for b in range(k):
                for j in range(m):
                    val=u[(b+g[j])%k]*hv[j]%P
                    x.append(val*pow(chirp_phase(q,m,1,0,b,j,table),P-2,P)%P)
            self.assertNotEqual(x[h-1],0)
            self.assertTrue(all(z==0 for z in x[h:]))
            self.assertEqual(hankel_rank(x),h)
            y,c=unknown_shift_rank1_transform(x,m)
            self.assertEqual(y,independent_full_dft(x)) # Sparse support-gap matcher works.
            x,_,_=sample_dechirped_rank(k,m,1,seed=7+q,shifts=g)
            self.assertEqual(hankel_rank(x),h)


if __name__=='__main__':unittest.main(verbosity=2)
