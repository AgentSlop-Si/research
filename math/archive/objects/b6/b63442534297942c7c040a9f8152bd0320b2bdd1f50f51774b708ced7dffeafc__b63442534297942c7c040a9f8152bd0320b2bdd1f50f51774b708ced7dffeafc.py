#!/usr/bin/env python3
"""Independent exact finite-field tests for learned rational Fourier cycles."""
import random
import unittest
from phase10_rational import (P,Count,ntt,root_of_unity,root_table,
    berlekamp_massey,make_spectral_recurrent_example,learn_spectral_recurrences,
    synthesize_from_recurrences,verify_raw_recurrence,phase10_transform,
    reference_full_ntt,direct_full_dft,extract_columns,transpose_circulant_action)


def rank_mod(rows,p=P):
    if not rows:return 0
    m=[list(row) for row in rows]
    h=len(m);w=len(m[0]);i=0
    for j in range(w):
        piv=next((t for t in range(i,h) if m[t][j]%p),None)
        if piv is None:continue
        m[i],m[piv]=m[piv],m[i]
        z=pow(m[i][j],p-2,p)
        for jj in range(j,w):m[i][jj]=m[i][jj]*z%p
        for t in range(i+1,h):
            a=m[t][j]
            if a:
                for jj in range(j,w):m[t][jj]=(m[t][jj]-a*m[i][jj])%p
        i+=1
        if i==h:break
    return i


class Phase10Tests(unittest.TestCase):
    def test_ntt_standalone_against_direct_dft(self):
        r=random.Random(11)
        for n in (1,2,4,8,16,32,64):
            for _ in range(3):
                x=[r.randrange(P) for _ in range(n)]
                self.assertEqual(ntt(x,True),direct_full_dft(x))
                self.assertEqual(ntt(ntt(x,True),False),x)

    def test_transpose_circulant_fourier_identity(self):
        r=random.Random(73)
        for k in (4,8,16,32):
            for _ in range(3):
                lam=[r.randrange(P) for _ in range(k)]
                w=[r.randrange(P) for _ in range(k)]
                phi=transpose_circulant_action(w,lam)
                fw=ntt(w,True)
                self.assertEqual(ntt(phi,True),[fw[i]*lam[-i%k]%P for i in range(k)])
                # bilinear transpose identity checked independently
                v=[r.randrange(P) for _ in range(k)]
                Cv=ntt([a*b%P for a,b in zip(ntt(v,True),lam)],False)
                self.assertEqual(sum(a*b for a,b in zip(w,Cv))%P,
                                 sum(a*b for a,b in zip(phi,v))%P)

    def test_berlekamp_massey_order_and_zero(self):
        self.assertEqual(berlekamp_massey([0]*14),[1])
        r=random.Random(39)
        for d in (1,2,3,4):
            for _ in range(12):
                q=[1]+[r.randrange(1,P) for _ in range(d)]
                f=[r.randrange(P) for _ in range(d)]
                for j in range(d,3*d+5):
                    f.append(-sum(q[i]*f[j-i] for i in range(1,d+1))%P)
                got=berlekamp_massey(f[:2*d])
                self.assertEqual(len(got),d+1)
                self.assertEqual(got,q)

    def test_generated_dense_spectral_exact(self):
        for k,m in ((8,4),(16,8),(32,8),(64,16),(128,16),(256,16)):
            for d in (1,2,3):
                if 2*d>m:continue
                for seed in (12,25,81):
                    x,_,_=make_spectral_recurrent_example(k,m,d,seed)
                    y,cert,_=phase10_transform(x,m,d,rounds=3,
                        rng=random.Random(seed+101),return_certificate=True)
                    self.assertTrue(cert['accepted'],(k,m,d,cert))
                    self.assertEqual(y,reference_full_ntt(x),(k,m,d,seed))

    def test_singular_denominators_are_removable(self):
        for k,m,d in ((16,8,1),(16,8,2),(32,8,3),(128,16,4)):
            x,_,_=make_spectral_recurrent_example(k,m,d,19,force_roots=True)
            y,cert,_=phase10_transform(x,m,d,rng=random.Random(102),
                                        return_certificate=True)
            self.assertTrue(cert['accepted'])
            self.assertGreater(cert['singular_outputs'],0)
            self.assertEqual(y,reference_full_ntt(x))

    def test_random_generic_inputs_rejected(self):
        r=random.Random(615)
        for k,m,d in ((16,8,1),(32,8,2),(64,16,3)):
            for trial in range(14):
                x=[r.randrange(P) for _ in range(k*m)]
                y,cert,_=phase10_transform(x,m,d,rounds=3,
                          rng=random.Random(trial+51),return_certificate=True)
                self.assertFalse(cert['accepted'],(k,m,d,trial,cert))
                self.assertIsNone(y)

    def test_deliberate_late_corruption_detected(self):
        x,_,_=make_spectral_recurrent_example(32,8,2,18)
        base=x[:]
        base[(19*8)+7]=(base[(19*8)+7]+1)%P
        y,cert,_=phase10_transform(base,8,2,rng=random.Random(8),
                                    return_certificate=True)
        self.assertFalse(cert['accepted'])
        self.assertIsNone(y)

    def test_half_width_generic_fit_does_not_save_work(self):
        # With d=M/2 the training step itself transforms ALL M columns.
        # Generic sequences usually have recurrence order d on these 2d
        # samples. The identity remains exact but savings disappear.
        r=random.Random(998)
        for k,m,d in ((16,8,4),(32,8,4),(64,16,8)):
            x=[r.randrange(P) for _ in range(k*m)]
            y,cert,_=phase10_transform(x,m,d,
                        rng=random.Random(77),return_certificate=True)
            self.assertTrue(cert['accepted'],(k,m,d,cert))
            self.assertEqual(y,reference_full_ntt(x))
            self.assertEqual(2*d,m)

    def test_random_certificate_can_be_fooled_if_vector_known(self):
        # A one-vector fingerprint is not deterministic. Construct u!=0 with
        # w dot u=0 for the known seeded first vector and corrupt late t=7.
        k,m,d=32,8,2
        x,_,_=make_spectral_recurrent_example(k,m,d,21)
        seed=123
        w_rng=random.Random(seed)
        w=[w_rng.randrange(P) for _ in range(k)]
        i=0
        while not w[i]:i+=1
        j=i+1
        u=[0]*k
        u[i]=w[j]
        u[j]=(-w[i])%P
        for b in range(k):x[b*m+(m-1)]=(x[b*m+(m-1)]+u[b])%P
        y,cert,_=phase10_transform(x,m,d,rounds=1,
                    rng=random.Random(seed),return_certificate=True)
        self.assertTrue(cert['accepted'])
        self.assertNotEqual(y,reference_full_ntt(x))
        y2,cert2,_=phase10_transform(x,m,d,rounds=2,
                    rng=random.Random(seed),return_certificate=True)
        self.assertFalse(cert2['accepted'])
        self.assertIsNone(y2)

    def test_rational_numerator_denominator_direct_equality(self):
        # Independently evaluate finite S at all roots (not using fast output).
        for k,m,d in ((8,4,2),(16,8,2),(32,8,3)):
            x,_,f=make_spectral_recurrent_example(k,m,d,67,force_roots=True)
            cols=extract_columns(x,m)
            train,q=learn_spectral_recurrences(cols,d)
            self.assertTrue(verify_raw_recurrence(cols,q,d,2,random.Random(55)))
            y,_=synthesize_from_recurrences(train,q,m,k*m)
            ztab=root_table(k*m)
            for ell in range(k):
                for j in range(m):
                    ix=ell+j*k
                    z=ztab[(-ix)%(k*m)]
                    expect=sum(f[t][ell]*pow(z,t,P) for t in range(m))%P
                    self.assertEqual(y[ix],expect)

    def test_polynomial_identity_over_entire_coefficient_range(self):
        # Check Q*S has no interior coefficients and boundary coefficients
        # equal the head/tail decomposition before evaluating any root.
        for k,m,d in ((8,4,2),(16,8,2),(32,8,3),(32,16,4)):
            x,_,F=make_spectral_recurrent_example(k,m,d,17,force_roots=True)
            train,q=learn_spectral_recurrences(extract_columns(x,m),d)
            for ell in range(k):
                f=[F[t][ell] for t in range(m)]
                coeff=q[ell];r=len(coeff)-1
                prod=[0]*(m+r)
                for t in range(m):
                    for i in range(r+1):
                        prod[t+i]=(prod[t+i]+f[t]*coeff[i])%P
                self.assertEqual(prod[r:m],[0]*(m-r))
                head=[sum(coeff[i]*f[j-i] for i in range(j+1))%P for j in range(r)]
                tail=[sum(coeff[i]*f[m+j-i] for i in range(j+1,r+1))%P
                      for j in range(r)]
                self.assertEqual(prod[:r],head)
                self.assertEqual(prod[m:],tail)

    def test_phase9_first_order_derived_innovations_are_dense(self):
        # Our order-2 inputs have generic, all-frequency, all-position
        # innovations relative to Phase9's one-step fitted controller.
        k,m,d=32,8,2
        x,_,F=make_spectral_recurrent_example(k,m,d,204)
        lam=[F[1][ell]*pow(F[0][ell],P-2,P)%P for ell in range(k)]
        for t in range(1,m-1):
            E=[(F[t+1][ell]-lam[ell]*F[t][ell])%P for ell in range(k)]
            e=ntt(E,False)
            self.assertTrue(all(z for z in E))
            self.assertTrue(all(z for z in e))
        self.assertEqual(rank_mod([[F[t][ell] for t in range(m)] for ell in range(k)]),m)


if __name__=='__main__':unittest.main(verbosity=2)
