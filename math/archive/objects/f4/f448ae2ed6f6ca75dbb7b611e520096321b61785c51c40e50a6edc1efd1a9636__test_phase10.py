"""Independent tests for Hero #17's Fourier spectral projector Union.

Requires only Python standard library. Exact prime-field tests.
"""
import random
import unittest
from math import ceil,log2
from math import isqrt
from phase10 import SpectralUnion, BatchSpectralUnion, classical_fft, classical_fft_project


def is_prime(n):
    if n<2:return False
    for d in range(2,isqrt(n)+1):
        if n%d==0:return False
    return True

def factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def fixture(n):
    for t in range(1,500):
        p=t*n+1
        if not is_prime(p):continue
        for b in range(2,p):
            w=pow(b,(p-1)//n,p)
            if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in factors(n)):
                return p,w
    raise RuntimeError('no fixture')

def direct_dft(x,p,w):
    n=len(x)
    return [sum(v*pow(w,(-k*j)%n,p) for j,v in enumerate(x))%p for k in range(n)]

def direct_project(x,p,w,mask):
    n=len(x);X=direct_dft(x,p,w);v=pow(n,-1,p)
    return [v*sum(X[k]*pow(w,(k*j)%n,p) for k in mask)%p for j in range(n)]

def rank(A,p):
    a=[row[:] for row in A]
    if not a:return 0
    nr=len(a);nc=len(a[0]);r=0
    for col in range(nc):
        pivot=next((j for j in range(r,nr) if a[j][col]%p!=0),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][col],-1,p)
        a[r]=[(x*inv)%p for x in a[r]]
        for i in range(r+1,nr):
            c=a[i][col]
            if c:
                a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==nr:break
    return r

def projection_matrix(n,p,w,S):
    inv_n=pow(n,-1,p)
    return [[inv_n*sum(pow(w,(k*(j-i))%n,p) for k in S)%p
             for i in range(n)] for j in range(n)]

def matmul(A,B,p):
    return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]

class TestSpectralProjectorUnion(unittest.TestCase):
    def test_coset_formula_exact_even_and_odd(self):
        rng=random.Random(1710001)
        for n in (6,8,12,15,16,24,32,48,60,64):
            p,w=fixture(n)
            for d in (v for v in range(1,n+1) if n%v==0 and v<=8):
                for _ in range(3):
                    residues={a for a in range(d) if rng.randrange(2)}
                    plan=SpectralUnion(n,p,w,d,residues)
                    x=[rng.randrange(p) for _ in range(n)]
                    got=plan.apply(x)
                    K={k for k in range(n) if k%d in residues}
                    self.assertEqual(got,direct_project(x,p,w,K))

    def test_random_swap_and_multiple_frequency_exceptions(self):
        rng=random.Random(1710002)
        for n in (8,12,16,24,32,48,64,96,128):
            p,w=fixture(n)
            for _ in range(8):
                divs=[d for d in range(2,min(n,12)+1) if n%d==0]
                d=rng.choice(divs)
                residues={a for a in range(d) if rng.randrange(2)}
                B=[k for k in range(n) if k%d in residues]
                rest=[k for k in range(n) if k%d not in residues]
                adds=rng.sample(rest,rng.randrange(min(len(rest),3)+1))
                removes=rng.sample(B,rng.randrange(min(len(B),3)+1))
                plan=SpectralUnion(n,p,w,d,residues,adds,removes)
                x=[rng.randrange(p) for _ in range(n)]
                K=(set(B)-set(removes))|set(adds)
                self.assertEqual(plan.apply(x),direct_project(x,p,w,K))

    def test_nontrivial_dense_matrix_linear_evaluation(self):
        # A parity projector plus a single exchanged frequency generically
        # has no zero matrix entries; yet the execution remains O(N).
        for n in (8,16,32):
            p,w=fixture(n)
            plan=SpectralUnion(n,p,w,2,{0},add=(1,),remove=(0,))
            P=projection_matrix(n,p,w,{k for k in range(n) if plan.contains(k)})
            self.assertEqual(sum(x!=0 for row in P for x in row),n*n)
            rng=random.Random(n)
            x=[rng.randrange(p) for _ in range(n)]
            self.assertEqual(plan.apply(x),[sum(a*b for a,b in zip(row,x))%p for row in P])

    def test_projector_commutes_and_exact_difference_rank(self):
        rng=random.Random(1710004)
        for n in (4,6,8,10,12,16):
            p,w=fixture(n)
            for _ in range(12):
                A={k for k in range(n) if rng.randrange(2)}
                B={k for k in range(n) if rng.randrange(2)}
                PA=projection_matrix(n,p,w,A)
                PB=projection_matrix(n,p,w,B)
                PI=projection_matrix(n,p,w,A&B)
                PM=projection_matrix(n,p,w,A|B)
                self.assertEqual(matmul(PA,PB,p),PI)
                self.assertEqual(matmul(PB,PA,p),PI)
                self.assertEqual([[ (a+b-c)%p for a,b,c in zip(u,v,wrow)] for u,v,wrow in zip(PA,PB,PI)],PM)
                self.assertEqual(rank([[(a-b)%p for a,b in zip(rowa,rowb)] for rowa,rowb in zip(PA,PB)],p),len(A^B))

    def test_binary_mask_signature_barrier(self):
        # Pigeonhole gate for a restricted materialized-projector strategy:
        # B binary mask-membership signatures cannot distinguish >2^B bins.
        for n in (4,8,16,32,64):
            bits=n.bit_length()-1
            masks=[{k for k in range(n) if (k>>j)&1} for j in range(bits)]
            signatures={tuple(int(k in mask) for mask in masks) for k in range(n)}
            self.assertEqual(len(signatures),n)
            self.assertGreater(n,2**(bits-1))

    def test_reflection_commutator_vs_true_projector_commutator(self):
        # Reconstruct the previous phase's quotient-transfer reflections
        # independently from polynomial division. These m-by-m objects
        # need not commute, although the actual n-by-n Fourier projectors do.
        for n in (8,16):
            p,w=fixture(n);m=n//2
            A=(set(range(0,n,2))-{0})|{1}
            B=set(range(n))-A
            def transfer(root_labels):
                poly=[1]
                for k in sorted(root_labels):
                    z=pow(w,(-k)%n,p)
                    nxt=[0]*(len(poly)+1)
                    for j,val in enumerate(poly):
                        nxt[j]=(nxt[j]-z*val)%p
                        nxt[j+1]=(nxt[j+1]+val)%p
                    poly=nxt
                cols=[]
                for k in range(m):
                    h=[0]*(2*m);h[m+k]=1
                    for zdeg in range(2*m-1,m-1,-1):
                        top=h[zdeg]
                        if top:
                            for j in range(m):
                                h[zdeg-m+j]=(h[zdeg-m+j]-top*poly[j])%p
                            h[zdeg]=0
                    cols.append(h[:m])
                return [list(row) for row in zip(*cols)]
            RA=transfer(A);RB=transfer(B)
            AB=matmul(RA,RB,p);BA=matmul(RB,RA,p)
            self.assertEqual(rank([[(a-b)%p for a,b in zip(u,v)]
                                   for u,v in zip(AB,BA)],p),2)
            PA=projection_matrix(n,p,w,A);PB=projection_matrix(n,p,w,B)
            self.assertEqual(matmul(PA,PB,p),[[0]*n for _ in range(n)])
            self.assertEqual(matmul(PB,PA,p),[[0]*n for _ in range(n)])

    def test_automatic_union_idempotence(self):
        rng=random.Random(1710005)
        for n in (16,32,64,128):
            p,w=fixture(n);d=4
            plan=SpectralUnion(n,p,w,d,{1,2},add=(0,3),remove=(1,2))
            x=[rng.randrange(p) for _ in range(n)]
            z=plan.apply(x)
            self.assertEqual(plan.apply(z),z)

    def test_phase10_vs_full_fft_same_output(self):
        rng=random.Random(1710006)
        for n in (8,16,32,64,128,256):
            p,w=fixture(n)
            for d in (2,4):
                plan=SpectralUnion(n,p,w,d,{0},add=(1,),remove=(0,))
                x=[rng.randrange(p) for _ in range(n)]
                got=plan.apply(x)
                ref,log=classical_fft_project(x,plan)
                self.assertEqual(got,ref)
                self.assertTrue(plan.cost()['total_field_operations']>0)
                self.assertTrue(log['total_field_operations']>0)

    def test_partial_and_empty_masks(self):
        n=32;p,w=fixture(n)
        x=list(range(n))
        for res in (set(),{0,1}):
            plan=SpectralUnion(n,p,w,2,res)
            ref=direct_project(x,p,w,{k for k in range(n) if k%2 in res})
            self.assertEqual(plan.apply(x),ref)


    def test_batch_shared_union_exact(self):
        rng=random.Random(1710010)
        for n in (8,16,32,64,128):
            p,w=fixture(n)
            d=4 if n%4==0 else 2
            masks=[]
            for i in range(12):
                if i%3==0:S={0}
                elif i%3==1:S={0,2} if d>=4 else {0}
                else:S={1}
                outside=[k for k in range(n) if k%d not in S]
                inside=[k for k in range(n) if k%d in S]
                # Frequencies repeat heavily across different masks.
                added=tuple(k for k in (1,3,5) if k in outside)[:2]
                removed=tuple(k for k in (0,2,4) if k in inside)[:2]
                masks.append((S,added,removed))
            batch=BatchSpectralUnion(n,p,w,d,masks)
            x=[rng.randrange(p) for _ in range(n)]
            got=batch.apply(x)
            for i,(S,a,r) in enumerate(masks):
                single=SpectralUnion(n,p,w,d,S,a,r)
                self.assertEqual(got[i],single.apply(x))
                K={k for k in range(n) if single.contains(k)}
                self.assertEqual(got[i],direct_project(x,p,w,K))
            self.assertEqual(batch.cost()['masks'],12)
            self.assertLess(batch.cost()['distinct_exception_frequencies'],12)

    def test_batch_duplicate_masks_cost_sharing(self):
        n=1024;p,w=fixture(n)
        masks=[({0},(1,), (0,)) for _ in range(8)]
        rng=random.Random(1710011)
        x=[rng.randrange(p) for _ in range(n)]
        batch=BatchSpectralUnion(n,p,w,2,masks)
        y=batch.apply(x)
        solo_cost=0
        for S,a,r in masks:
            f=SpectralUnion(n,p,w,2,S,a,r)
            self.assertEqual(f.apply(x),y[0])
            solo_cost+=f.cost()['total_field_operations']
        self.assertLess(batch.cost()['total_field_operations'],solo_cost//2)
        self.assertEqual(batch.cost()['distinct_bases'],1)
        self.assertEqual(batch.cost()['distinct_exception_patterns'],1)

    def test_invalid_root_and_events(self):
        n=16;p,w=fixture(n)
        with self.assertRaises(ValueError):SpectralUnion(n,p,1,2,{0})
        with self.assertRaises(ValueError):SpectralUnion(n,p,w,3,{0})
        with self.assertRaises(ValueError):SpectralUnion(n,p,w,2,{0},add=(2,))
        with self.assertRaises(ValueError):SpectralUnion(n,p,w,2,{0},remove=(1,))
        with self.assertRaises(ValueError):SpectralUnion(n,p,w,2,{0},add=(1,1))
        with self.assertRaises(ValueError):SpectralUnion(n,p,w,2,{0},add=(1,),remove=(1,))

    def test_classical_fft_independent_direct(self):
        rng=random.Random(1710009)
        for n in (4,8,16,32,64,128):
            p,w=fixture(n)
            x=[rng.randrange(p) for _ in range(n)]
            y,L=classical_fft(x,p,w)
            self.assertEqual(y,direct_dft(x,p,w))

    def test_operation_growth_fully_charged(self):
        for n in (256,1024,4096):
            p,w=fixture(n)
            plan=SpectralUnion(n,p,w,4,{0,2},add=(1,),remove=(0,))
            x=[(7*j*j+11*j+3)%p for j in range(n)]
            plan.apply(x)
            self.assertLess(plan.cost()['total_field_operations'],40*n)
            self.assertEqual(plan.L.output_writes,n)
            self.assertGreaterEqual(plan.plan_ledger['plan_muls'],n-1)

if __name__=='__main__':unittest.main()
