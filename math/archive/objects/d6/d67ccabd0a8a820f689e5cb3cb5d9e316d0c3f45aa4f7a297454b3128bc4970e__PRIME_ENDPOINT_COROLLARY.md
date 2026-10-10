# Prime-length endpoint-permutation corollary

Separate supplement, 9 October 2026 UTC. This does not modify the frozen three-stage milestone.

Let p be prime, and let T=Q_out F_p Q_in be the complex Fourier matrix with arbitrary independent endpoint permutations and optional invertible endpoint diagonal scalings. If

T=S3 P2 S2 P1 S1

with quasiseparable orders r1,r2,r3 in the stages' natural coordinates, then the same bounds as in the cyclic-discrepancy theorem hold:

D_grid(P2^{-1}) <= 2r1+r2+r3,
D_grid(P1) <= r1+r2+2r3,

and hence r1+r2+r3=Omega(log p).

Proof: all equal-size square submatrices of the complex prime-order Fourier matrix are nonsingular by Chebotarev's theorem. Row/column permutations and invertible diagonal scalings preserve that property. Thus every target prefix-row/cyclic-column block in the existing localization-and-averaging proof has rankW. Nothing else in that proof uses Fourier endpoint order. Apply it unchanged, then use Schmidt's planar discrepancy theorem.

The full-spark result is classical. A primary proof and exact statement were verified in Terence Tao, “An uncertainty principle for cyclic groups of prime order,” Lemma1.3, pages3–4 of https://arxiv.org/pdf/math/0308286 (v6,22July2004; published Mathematical Research Letters12(2005),121–127). This note imports that theorem and makes no novelty or publication-priority claim.

Consequently arbitrary endpoint shuffles cannot produce a three-constant-order quasiseparable factorization valid for all complex Fourier lengths, since arbitrarily large primes already force growing order. Both non-affine endpoints remain outside the present proof for general composite lengths, including dyadic families. No full-spark claim is made over arbitrary finite fields, and no unrestricted arithmetic-operation lower bound follows.
