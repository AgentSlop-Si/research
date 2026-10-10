# Boundary-aware annihilators: an independent bounded extension

9 October 2026 UTC. This is an independently derived refinement of the uploaded local-annihilator argument, using the one-sided cut accounting already present in the master window-rank audit. No publication-priority claim is made.

## Result 1: a three-sparse mismatch already at N >= 18

Let F_N[i,j]=omega^(ij) over any field containing a primitive Nth root omega. Let S1,S2 have quasiseparable orders at most r1,r2 in their stage coordinates, and let P be any internal permutation. Put

s = 2r1+1,   w = s+r2.

If

N >= s(s+2r2+1),

then F_N != S2 P S1. Moreover, at least

N+1-s(s+2r2+1)

non-wrapping consecutive input windows of length s contain a nonzero mismatch input. One can detect each mismatch using s linear functionals on the first w output coordinates.

For r1=r2=1, s=3 and w=4. Thus N >= 18 suffices, and at least N-17 input windows work. This improves the uploaded constructive threshold N >= 24; the inherited master two-stage necessary-rank filter already excludes N >= 17, so this does not improve the best existential exclusion threshold. Its contribution is a smaller, explicit local witness and a general-rank formula.

### Proof

Fix the prefix I={0,...,w-1}. Its rows have only one outside tail. Therefore rank(S2[I,I^c]) <= r2, and there is a full-row-rank s-by-w matrix Y with Y S2 supported only in columns I. This loses at most r2 dimensions, rather than the 2r2 loss needed for an interior interval.

For each non-wrapping consecutive length-s input interval J_j, the stacked exterior rows of S1[:,J_j] have rank at most 2r1. Consequently some nonzero x_j supported in J_j has S1 x_j supported in J_j.

There are N-s+1 candidate positions j. At most s*w intersect the footprint P^(-1)(I): it has w elements, and each is contained in at most s non-wrapping windows. At a nonintersecting position, Y S2 P S1 x_j=0.

The Fourier projection Y F_N[:,J_j] is the s-by-s Casoratian evaluated at z=omega^j for s independent polynomials supported in exponents 0,...,w-1. Cauchy–Binet and the leading-degree Vandermonde argument give

det(Y F_N[:,J_j]) = z^(s(s-1)/2) Q(z),

where Q is nonzero and deg Q <= s(w-s)=s*r2. The N-s+1 values omega^j are distinct because they use indices 0,...,N-s; no wrapping is used. Hence at most s*r2 positions have singular Fourier projection. At all remaining positions the nonzero x_j gives Y F_N x_j != 0.

At least N-s+1-s*w-s*r2 = N+1-s(s+2r2+1) positions remain. The stated threshold makes this number at least one. All support sizes are <=N under that threshold. No division by stage generators or assumption of stage invertibility is used.

The proof needs neither parity nor characteristic zero. A primitive Nth root in a field provides all required distinct Vandermonde nodes and already rules out characteristic dividing N. Complex roots exist at every positive N. The exact N=18 control uses F_109, whose multiplicative group has order 108, so its chosen order-18 root is admissible. It is not inferred from a dyadic test.

Natural or independently affine/copime-stride Fourier endpoints and invertible endpoint diagonal scalings are covered after phase and primitive-root adjustments. Arbitrary non-affine endpoint reordering is not covered. Transposition exchanges r1,r2 and gives the analogous output-local witness.

## Result 2: boundary-aware three-stage rank gate

For M=S3 P2 S2 P1 S1, let I,J be arbitrary nonempty consecutive intervals, with possibly different lengths. Let

b(K) = 1 if a proper interval K touches an endpoint,
       2 if K is interior,
       0 if K is the entire index range.

Set R=P2^(-1)(I), C=P1(J). Let k(R,C) be the least number of rows plus columns deleted to leave all remaining row indices strictly on one side of all remaining column indices. Then

rank(M[I,J]) <= b(J)r1 + b(I)r3 + r2 + k(R,C).

For any claimed target T=M, use h=rank(T[I,J]) on the left. If the compressed dimensions are positive, choose right/left annihilator bases losing at most b(J)r1 and b(I)r3 dimensions. Sylvester's inequality loses at most their sum, while the middle compression has rank at most r2+k. If one compressed dimension is nonpositive, the displayed bound is automatic because rank(M[I,J]) <= min(|I|,|J|). This also handles all small/degenerate windows.

For equal-width natural Fourier windows h=W. Three order-one stages with both endpoint windows touching a boundary must therefore satisfy k>=W-3, instead of the uploaded generic k>=W-5. One boundary improves the threshold to W-4. This is a necessary layout gate, not a sufficient Fourier construction or an exclusion of every permutation pair.

The same statement supports different upper/lower quasiseparable ranks: replace b(J)r1 and b(I)r3 by their actual exterior-cut rank budgets. This is the natural synthesis with the inherited window theorem. Arbitrary non-affine Fourier endpoints still require actual h; no unconditional full-spark claim is made at composite N.

## Independent exact controls

The independently authored checker covers 25 sparse-witness cases, including N=18,24,32,64; orders (r1,r2)=(1,1),(2,1),(1,2),(2,2); and zero first-stage controls. It checks actual dense candidate products and projected Fourier values at every qualifying position. All pass.

A further 2,325 actual three-stage matrix-window cases verify the boundary-aware bound; 2,075 have strictly smaller budgets than the generic two-sided formula. The separate Casoratian checks cover 125 independent polynomial spaces and 2,150 exact root evaluations. The proofs establish the general statements; these finite controls supplement them.

Witness discovery is a verifier, not a Fourier algorithm. In dense representation, forming annihilator bases and searching candidate positions has its own charged work. Fixed-rank structured representations can reduce that work, but no unrestricted circuit lower bound or practical speedup follows.
