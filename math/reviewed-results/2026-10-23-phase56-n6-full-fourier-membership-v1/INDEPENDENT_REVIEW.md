# Independent acceptance: original Phase56 N6(2+3) full Fourier membership

23 October 2026. ACCEPT the exact finite target-membership certificate and its stated conditional compilation lemma. No novelty, discovery-count, priority, asymptotic FFT or owner-closure promotion is justified.

## Scope and source legality

The original source PHASE56_THEOREMS.md, SHA-256 de2d028094611802a644484c122f07949d0643948aad1e11248ee0f211e25986, was read in full. Section 56.1 allows arbitrary nonzero complex vertex gains, nonzero holonomy different from one, variable stage coefficients, invertible diagonals and unrestricted independent Hamiltonian orders. It imposes no requirement that different terms have distinct cycles. The fixed five natural cycles, identity middle diagonal and identity interstage permutation are therefore legal. Numerical gauge normalizations are not extra restrictions on that original family.

The source's earlier full membership list contains N5,7,8,11,13, not N6. Its thirteen generic-rank claims are separate and do not themselves establish Fourier membership. This is an additional finite certificate relative to that identified source, not an exhaustive literature-priority determination.

## Exact proof

Set a=exp(-pi*i/6), C(z)=sum_{k=0}^5 a^(-k^2) z^k and Q(z)=sum_{k=0}^5 a^(k^2) z^k. Both chirp sequences are 6-periodic since a^(12k+36)=1. Their cyclic convolution at offset r is a^(-r^2) sum_{k=0}^5(a^(2r))^k. Thus CQ=6 modulo z^6-1 exactly, with the correct negative Fourier sign.

The squarefreeness specialization is sound: Z[a]/(a^4-a^2+1) maps to F13 by a->2. Q and Q' retain degrees 5 and 4, and the supplied U,V satisfy U Qbar+V Qbar'=1 exactly. Therefore their algebraic resultant is nonzero in characteristic zero. This is a coefficient-ring resultant argument, not an invalid field embedding or numerical rank claim.

Q has nonzero constant and leading coefficients, so its five reciprocal roots t_s are distinct and nonzero. The cyclic inverse identity excludes t_s^6=1. Their exact lexicographic ordering is a legitimate parameter definition; existence and all identities work for any labeling. The displayed quartic factorization of the reciprocal polynomial is also exact.

For natural order, g_s(v)=t_s^v and h_s=t_s^6 make the original Green formula exactly (I-t_s P)^(-1), including its closing edge and all wrap-around entries. All gains, holonomies, Green denominators and partial-fraction factors are nonzero. The ordinary partial-fraction identity for a group of distinct nonzero roots is proved by multiplying through and checking the distinct poles. Splitting the roots into groups of two and three, and multiplying second-stage coefficients by six, gives

    S_2 S_1 = 6 product_s (I-t_sP)^(-1) = 6Q(P)^(-1)=C(P).

The external diagonals L_ii=R_ii=a^(i^2) are invertible. Every one of the 36 entries is a^(i^2-(i-j)^2+j^2)=a^(2ij), including row/column zero and cyclic wrap-around. This is precisely the negative-sign, unnormalized F6. The entire middle matrix has nonzero entries, so its first-row/column dephasing guards also hold. No generic dominance or approximate optimizer residual enters the proof.

The same proof validates the conditional compilation lemma when its explicitly stated inverse-polynomial, nonzero scalar, degree, constant-term and squarefreeness hypotheses hold. Those hypotheses are checked only at N6 here. No all-length chirp squarefreeness or small term count is inferred.

## Full cost accounting

The post-root setup upper bound is independently reproducible: 25 multiplications for gain/holonomy powers, 20 for inverse powers, 5 for h/(1-h), 8 for pairwise root ratios, 3 for triple-group denominator products, 3 for stage-two scalar-six factors, 25 for folded output gain factors, and 4 for the required chirp powers. Total: 93 multiplications. There are 8 ratio subtractions plus 5 guard subtractions, and 5 inversions each for roots, Green guards and partial-fraction denominators: 13 subtractions and 15 inversions.

This excludes no hidden algebraic setup: the report separately requires construction/isolation of the quartic roots, a splitting field, and exact root-order comparisons. It explicitly does not provide a uniform bit-cost or conditioning guarantee for those operations.

One supplied Green term has 6 input scalings, 1 total-prefix scaling and 6 output scalings, hence 13 multiplications; a five-addition prefix scan and six additions give 11 additions. Five terms, stage summations and the two outer diagonals give 77 multiplications and 73 additions online. The 71 precomputed-scalar upper bound is 5*(6 inverse gains+6 folded gains+1 prefix scalar)+6 shared outer-chirp entries. No online division or asymptotic FFT improvement is claimed.

## Independent controls and pins

fresh_checks.py was independently written and imports no author or historical program. It implements exact arithmetic in Q[a]/(a^4-a^2+1), verifies the full cyclic inverse, all 36 Fourier entries, the quartic factor, the mod13 Bezout identity and degree preservation. Separate exact rational fixtures reconstruct the original Green entries, prove their matrix inverse identity, check the two-stage partial-fraction product and compare prefix evaluation with dense original entries. Wrong Fourier sign and missing scalar-six normalization are rejected. The accounting ledger is independently checked. All 62 checks pass, with byte-identical ordinary and Python -O results. Guards are proved symbolically, not inferred from rational samples.

Accepted author manifest: 21feb41d680f9a22202a1eeaec9bb1f60ef2681beb8ff11df5280800f9e4598f.
Accepted report: 6e806c67fa049d9bcc8bf90772092b32e2816df93c74bfb986666dead4434bf4.
Source binding: 9d53348dee55654783aed2eada6faa15f5f4b140eb497128a7431f965599b8de.

BINDINGS.json retains the checked candidate/source inventory. Classical chirp convolution and partial fractions are correctly credited. The accepted result is the bounded original-grammar N6(2+3) target membership, not worldwide novelty, a competitive six-point FFT implementation, an arithmetic lower bound, or a general Fourier algorithm. No external state was changed by this reviewer.
