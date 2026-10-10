# Relative cyclotomic rank and the gcd orbit component

Version 2026-10-10, Phase 32 source version 0. Mathematical status: scoped pass with field, proof-writing, arithmetic-ledger and certificate-packaging corrections.

For d|N, K=Q(zeta_N), E=Q(zeta_d), H=Gal(K/E), and c_d(N)=sum_{m|N} phi(gcd(m,d)),

max rank_E L(F_N)=N-c_d(N),

where L:K->E ranges over E-linear functionals with L(1)=0. The sharp exterior factorization has E-valued coefficients; it can use rational interface maps A,B but the bypass F_N P_H is generally E-valued. The rational gcd-orbit Fourier component has an O(N) exact-arithmetic evaluator, which does not compute the full arbitrary-input DFT.

## Field assumptions and minimal polynomials



The actual theorem assumes d divides N. It sets K = Q(zeta_N), E = Q(zeta_d), and H = Gal(K/E) = {a in (Z/NZ)^*: a = 1 modulo d}. Under that assumption E is a subfield of K. There is no missing-containment error in the theorem as written.

The degree [K:E] is phi(N)/phi(d) = |H|. The minimal polynomial of zeta_N over E is the product of (t - zeta_N^a) over a in H. Its coefficients are H-invariant and hence lie in E. The orbit of zeta_N has |H| distinct elements, so this polynomial is irreducible over E and has the required degree. Over Q, the minimal polynomial remains Phi_N(t), of degree phi(N). These two degrees must not be confused. For N=8 and d=4, the relative polynomial is t^2 - i, whereas Phi_8(t) = t^4 + 1.

An extension to arbitrary d must change the field construction. Put E_0 = E intersect K and M = EK; use Gal(M/E), identified by restriction with Gal(K/E_0), and an E-linear functional M -> E. One must not write an E-linear map K -> E when K is not an E-vector space. For cyclotomic fields, E_0 = Q(zeta_gcd(N,d)) and M = Q(zeta_lcm(N,d)); the correct orbit group is determined by the intersection. This is a clarification for possible future extensions, not an omitted hypothesis in the supplied theorem.

## Rank theorem and attainment

For an E-linear functional L: K -> E with L(1)=0, E-linearity implies L(e)=0 for every e in E. An H-orbit-invariant vector x in E^N has F_N x in E^N. Consequently the c_d(N)-dimensional invariant subspace lies in the kernel of L(F_N), giving rank_E L(F_N) <= N - c_d(N).

The trace pairing in a finite separable extension identifies such functionals with L_b(z)=Tr_{K/E}(bz), where Tr(b)=0. Choose a normal element u and set b=|H|u-Tr(u). The group-algebra operator C_b = sum_a sigma_a(b) Pi_a kills the trivial H-mode and is invertible on each nontrivial H-character mode. Therefore its kernel in the index permutation representation is exactly the invariant subspace. The identity L_b(F_N)=C_b F_N and the invertibility of F_N prove attainment. Because L_b(F_N) has entries in E, extending scalars to K does not change its rank.

One proof-writing correction is useful. The supplied matrix (sigma_ab(u)) is a reverse group-circulant; for groups with characters of order greater than two it is not literally diagonalized with the stated character sums as eigenvalues. Replace it by (sigma_{a b^{-1}}(u)), which differs only by a column permutation. That conventional group matrix has the claimed character eigenvalues and remains invertible by normal-basis/separability theory. The conclusion survives unchanged.

The finite-abelian-group extension is valid as well. Apply the same group-algebra operator to the character table; the multiplicity of the trivial representation is the number of H-orbits on the group. A nonfaithful action causes no problem, since characters absent from the representation need not be considered.

## The exterior field and the sharp sandwich

For F_N = R + A T B with R, A, B over E, applying the sharp E-linear functional yields L(F_N)=A L(T) B. The bound min(rank_E A, rank_E B) >= N-c_d(N) follows. Extending the functional E-linearly to a common coefficient field is legitimate as a vector-space extension; no multiplicativity is asserted or needed.

Let P=P_H be the rational orbit-average projector. The rational maps A and B described in the source satisfy AB=I-P and BA=I. Since F_N commutes with P,

F_N = F_N P + A (B F_N A) B.

The core width is N-c_d(N), and this attains the E-relative lower bound even with rational A and B. However, the bypass F_N P has entries in E, not necessarily Q. The phrase “sharp as a rational-interface width statement” is safe only if it means rational A and B with an explicitly E-valued bypass. It is false if read as sharpness with every exterior coefficient, including R, rational.

Concrete counterexample to that broader reading: take N=8, d=4. Then H={1,5}, c_4(8)=6, and the relative width is 2. The orbit of column 1 is {1,5}, and

(F_8 P_H)[2,1] = (zeta_8^2 + zeta_8^10)/2 = i.

Thus R is not rational. An all-rational exterior instead falls under d=1 and requires width 8-tau(8)=4. The d=4 decomposition cannot refute that bound.

The rank throughout is rank over E. The trace functional is E-linear; being also Q-linear does not convert this into a Q-coefficient theorem. If E^N is explicitly regarded as a Q-vector space, restriction of scalars multiplies its dimension and the rank of an E-linear operator by [E:Q]. That is a different representation and cost model. Because A and B themselves have rational entries, their ordinary matrix ranks agree over Q and E; this does not make R rational.

Suggested replacement sentence: “The bound is sharp for E-valued exterior coefficients; it is attained with rational interface maps A and B and an E-valued bypass R=F_N P_H.” Apply the same qualification to the dyadic tradeoff and negative-gate wording.

## Orbit counts and the isolated twiddle stage

The formula c_d(N)=sum_{m|N} phi(gcd(m,d)) is correct for d|N. Partition indices by exact additive order m. The image of H on the order-m elements is the kernel of unit reduction to gcd(m,d), and its index is phi(gcd(m,d)). Burnside's fixed-point formula gives the equivalent average of gcd(a-1,N).

The stated prime-power formula, multiplicativity, fixed-d bound c_d(N) <= phi(d)tau(N), and dyadic N/4 threshold follow. “Fixed d” matters in the N-o(N) statement; allowing d to grow changes the tradeoff. Allowing E=K removes this particular obstruction completely, but does not make those exterior operations free.

The relative twiddle rank is also correct: any root outside E is nonzero under some functional annihilating E, and over the infinite field E a single functional can avoid finitely many zero hyperplanes. The 15-replicate diagonal therefore has rank 15 times the number of non-E entries. This concerns an isolated interface, not multiplication count after adjacent-stage mixing.

## The O(N) component and its missing complement

For d=1, H-orbits are the gcd(k,N) classes. Average the arbitrary input on those classes, transform the tau(N) class means with classical Ramanujan coefficients, and scatter the class outputs. The result is exactly F_N P x = P F_N x. This identity holds for arbitrary input x; it does not say that P is the identity.

The O(N) arithmetic argument is valid. Accumulation and scattering cost O(N), while the divisor-indexed map costs O(tau(N)^2). The elementary bound tau(N) <= 2 sqrt(N) proves O(N) field arithmetic. Sieve and gcd-label recurrences use O(N) logarithmic-word operations; the additional divisor-pair gcd work is O(tau(N)^2 log N)=o(N), using the standard divisor-function bound tau(N)=N^{o(1)}. Space is O(N) field elements and integer words.

The complement has dimension N-tau(N). It is not computed here. The core B F_N A in the sharp decomposition still contains the noninvariant Fourier work. Computing the projection and then doing a conventional full residual FFT adds overhead unless a separately proved joint circuit removes more work than it adds. No such circuit or saving is established in this phase.

The stated full-transform reference remains 180 h log_2(h) + 1163 h + 15 for N=120h. This audit does not re-certify that earlier implementation; it records that Phase 32 does not improve it. Component timings/counts must not be turned into FFT speedup percentages.

## Charged cost corrections

All 12 published addition/multiplication counts and finite-field inverse-preparation counts reproduce analytically. They are nevertheless a model-dependent operation proxy, not a complete literal instruction ledger.

(a) Unary signs. The implementation executes term=-term when a Ramanujan coefficient is -1 without incrementing a counter. Later negative terms can be fused into a subtraction, so counting every literal negation is conservative rather than a necessary optimized-circuit cost. But an initially negative accumulator also occurs and is not covered by a later subtraction. The ledger must declare free sign changes or count/compile those operations explicitly.

At N=61,440 the source reports 64,448 additions/multiplications and 50 inverse preparations. There are 105 unlogged literal unary negations. Counting each of those and one event per inverse gives 64,603 events. With signed accumulation fusing subsequent signs into subtraction, one initial negation remains, giving 64,499 events in that specific model. These are component-only counts. They do not include a field-inversion implementation, bit costs, RAM operations, or a full FFT.

At N=120 the analogous source count is 446 plus 14 inverses, with 33 literal negations and one initially negative term: 493 literal events or 461 events under the same signed-accumulation model.

(b) Characteristic-zero constants. The Fraction(1,size) branch prepares exact reciprocals but does not increment the inversion/preparation field at all. That counter is accurate only for the modular branch. Count or explicitly designate the rational constant preparations offline.

(c) Inverse preparation is one recorded event, not the operation count of Euclid, exponentiation, or rational normalization. The linear arithmetic claim is sound with unit-cost field operations including inversion, or declared precomputed constants. It is not a bit-complexity or unrestricted machine-instruction theorem.

(d) General relative P_H and T=BFA do not have a supplied cheap online implementation. The O(N) claim belongs to the rational gcd-orbit component, not every growing coefficient field E. Charge relative orbit enumeration, constants, routing, A/B application, the bypass, and the residual core in any later full circuit.

(e) The field-element occupancy field is explicitly a proxy. It is not peak resident memory. Python object overhead and intermediate allocation are outside that value.

These corrections do not overturn O(N): sign handling, tau(N) inverse preparations, and a conservative O(tau(N)^2) extra charge remain linear in the stated algebraic model. In the cost table, “fourth column is a completely different output” should refer to the fifth column, the complete FFT comparator.


## Certificate boundary

A nonzero reduced minor of an algebraic-integer trace witness at a verified primitive root modulo a prime proves that the characteristic-zero minor is nonzero. An upper bound still needs the orbit argument; modular deficiency alone is insufficient. The original rank JSON contains seeds and coefficient hashes rather than all coefficients and roots. It is a reconstructible package-level witness, not a standalone numerical certificate. The supplied source modules and seed/hash records are included unchanged and are explicitly not marked as independently executed.

Fresh checks covered 1,767 (N,d) pairs through N=300; 72 stored minors; 72 additional full-rank cases in two new primes; 12 exact characteristic-zero cases; 49 twiddle profiles; 2,048 projected-output entries; 68 full-DFT negative controls; and all 12 cost rows. Their mathematical result data are included.

## Classical antecedents and remaining task

The gcd-even/Ramanujan component is classical: [Haukkanen](https://arxiv.org/abs/1210.0295), published in 2007, and [van der Kamp](https://arxiv.org/html/1201.3139). Normal-basis and group-algebra machinery is also classical; see [Giesbrecht, Jamshidpey and Schost](https://arxiv.org/html/2005.03497v2). Priority of the precise combined formulation remains unverified.

A full-transform claim would require an explicit cheap complement circuit, paid bypass and reconstruction, coefficient preparation and routing, and a same-output comparison in a common operation model. None follows from relative width alone.
