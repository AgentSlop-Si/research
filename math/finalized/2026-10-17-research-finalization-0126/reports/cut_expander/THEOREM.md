# Explicit finite noncancellation and homogeneous-weight obstruction for M-CUT-EXPANDER

17 October 2026 UTC. Candidate for independent review. This advances the existing coefficient-realization gate; it does not close M-CUT-EXPANDER or construct Fourier coefficients.

## Result in one paragraph

One fixed rational coefficient recipe realizes **maximal actual off-cut rank at every coordinate cut** of the twenty-plan, two-stage MGG grammar at N=4,9,16. The certificate covers 66,058 directed cuts by exact finite-field elimination and lifts to the same explicit rational and complex matrices. At every square length the normalized recipe is legal, uniformly well conditioned, and has an O(N) exact-field evaluator with all twenty solves charged. Nevertheless, its homogeneous branch weights force a constant-vector invariant that excludes the normalized Fourier target with operator error at least sqrt(1-1/N). Thus finite actual-rank realization is strictly weaker than Fourier realization, even for this particular well-conditioned survivor. No all-size maximal-cut-rank claim is made.

## 1. Fully specified grammar and coefficients

For s>=2 let N=s^2. Index vertices (x,y) in (Z/sZ)^2 by j=s*x+y. Define four permutations, with arithmetic modulo s:

- pi_0(x,y)=(x+2y,y)
- pi_1(x,y)=(x+2y+1,y)
- pi_2(x,y)=(x,y+2x)
- pi_3(x,y)=(x,y+2x+1)

Let P_a e_j=e_{pi_a(j)}. For q=0,...,19 put gamma_q=(q+1)/101 and

G_q=(I-gamma_q P_(q mod 4))^(-1),
X=sum_(q=0)^9 G_q, Y=sum_(q=10)^19 G_q, T=YX/100.

The division by100 is an explicit scalar normalization. It does not affect any rank. This is a specified10+10 partition of five copies of each of the four maps. It belongs to the accepted broader arbitrary-permutation/multicycle grammar; it is not asserted to be the only historical partition or a four-Hamiltonian-plan realization. There are no hidden intervening permutations, entrywise masks or uncharged oracle stages.

Each gamma lies strictly between0 and1, so every cycle guard 1-gamma_q^ell is nonzero over Q and C. This includes length-one cycles. No zero edge is used.

### Theorem A: finite simultaneous actual-rank realization

For each s in {2,3,4}, and every nonempty proper R subset {0,...,N-1}, with C its complement,

rank_Q T[R,C] = rank_C T[R,C] = min(|R|,|C|).

The quantifier includes both directed complementary blocks: enumerating every R includes C as well. It is about complementary coordinate cuts, not every rectangular submatrix with arbitrary overlapping row/column sets.

### Exact certificate and proof

Use p=1,000,000,007. The fresh checker verifies p is prime by trial division. Since p does not divide101 or100, the input coefficients and normalization reduce modulo p. For every branch and every permutation cycle, it checks 101^ell-(q+1)^ell is nonzero mod p. Thus each denominator inverse is defined in Z_(p) and commutes with reduction. The checker constructs each inverse by exact modular Gauss–Jordan elimination and verifies A_q G_q=I. It forms X,Y and YX in the stipulated order.

For every mask1 through2^N-2 it performs rectangular Gaussian elimination on (YX)[R,C]. All ranks equal the smaller side size. A full-rank block over F_p has a maximal minor with nonzero reduction. That minor of the explicit rational block is therefore nonzero. Rational rank reaches the dimension upper bound, as does complex rank. Multiplication by1/100 preserves it. This is a one-way nonzero-minor lifting argument, not inference of complex feasibility from a finite-field point with unrelated coordinates.

The bounded certificate results are:

- N=4:14/14 directed cuts maximal
- N=9:510/510 directed cuts maximal
- N=16:65,534/65,534 directed cuts maximal
- Total:66,058/66,058, with zero rank failures

CHECK_RESULTS.json saves all reduced product matrices, branch coefficients and cycle lengths, per-size cut counts, and the SHA256 of the canonical mask/rank/capacity stream. check_coefficients.py reconstructs everything from the displayed formulas with the Python standard library. The matrix is retained unnormalized modulo p; normalization is explicitly invertible. These finite checks are the certificate for Theorem A, not an all-length extrapolation.

## 2. Uniform legality, conditioning and charged evaluator

The recipe in Section1 is defined for every integer s>=2. A permutation matrix P is unitary over C. For0<=gamma<1,

|| (I-gamma P)^(-1) ||_2 <= 1/(1-gamma),
Re((I-gamma P)^(-1)) >= (1/(1+gamma)) I.

For the second inequality diagonalize P unitarily and use

Re(1/(1-gamma e^(i theta))) >=1/(1+gamma).

After multiplication by the positive denominator, this reduces to gamma(1-gamma)(1+cos(theta))>=0. Averaging the ten branches and using the largest gamma in each stage gives

sigma_min(X/10)>=101/111, ||X/10||_2<=101/91,
sigma_min(Y/10)>=101/121, ||Y/10||_2<=101/81.

Indeed ||Az||>=Re(z*Az)/||z|| for every nonzero z. Consequently, uniformly in s,

sigma_min(T)>=10201/13431,
||T||_2<=10201/7371,
kappa_2(T)<=13431/7371<1.823.

This is conditioning of the complete matrix; it does not lower-bound the smallest singular value of every cut block. Theorem A certifies exact cut rank only. It does not certify numerically robust cut ranks or finite-precision stability of an implementation.

The four permutation lists and their cycle decompositions take O(N) word/index work and O(N) storage. On a cycle, solving (I-gamma P)u=b consists of a forward affine recurrence, one guarded closure division, and a forward reconstruction. Computing gamma^ell costs O(ell) multiplications if needed, included in the scan; summed cycle lengths are N. Each of the twenty branch solves therefore costs O(N) exact-field arithmetic, and the two sums and scalar normalization cost O(N). All twenty occurrences, coefficient preparation, index generation, movement and storage are charged. Constants do not grow with N. This is an exact-field arithmetic/word-operation statement, not a bit-complexity, parallel-depth or floating-point implementation result. The exhaustive certificate itself costs exponentially many cuts and is separate from this evaluator.

## 3. A stronger obstruction for all homogeneous branch coefficients

### Theorem B: constant-vector Fourier gap

Let e=(1,...,1)^T/sqrt(N). Any legal scalar-weight permutation resolvent (I-gamma P)^(-1) sends e to (1-gamma)^(-1)e. Its conjugate-transpose likewise preserves span(e), so it has zero cross blocks between span(e) and e-perp. This property is preserved by arbitrary sums, products, scalar multiples and actual permutation insertions. Thus every matrix S in this homogeneous-weight grammar satisfies Se=lambda e and e* S=lambda e* for some scalar lambda.

For the normalized complex Fourier matrix Fhat_N, Fhat_N e=e_0, with |e*e_0|=1/sqrt(N). Projecting the error onto e-perp yields

||S-Fhat_N||_2 >= ||(I-ee*) Fhat_N e||_2 = sqrt(1-1/N).

Both off-diagonal blocks in the decomposition span(e) plus e-perp have norm sqrt(1-1/N), hence also

||S-Fhat_N||_F^2 >=2(1-1/N).

The same bounds hold if arbitrary permutation matrices are placed at the target's two endpoints, because they fix e and merely move e_0. Overall complex scalar normalization of S is already allowed. These are absolute errors for the normalized target.

This gives an all-size obstruction for **any homogeneous scalar coefficient per branch**, not just the20 rational values above, and even for more homogeneous branches or stages. It says nothing against nonconstant vertex/edge weights, nonconstant diagonal masks, or other operations that break the common invariant. Those are admitted in the larger weighted grammar and remain open. It is an elementary invariant argument, not a new global FFT or arithmetic-circuit lower bound. No historical-priority claim is made.

Combining Theorems A and B gives an explicit, well-conditioned counterexample to the implication "all actual coordinate cut ranks are maximal, therefore a Fourier identity is feasible for these coefficients." Unlike a graph-only countercontrol, all actual cuts are simultaneously maximal at the three certified sizes.

## 4. Owner history, source comparison, and exact remaining gate

The full live owner records were read. The accepted Phase13 review was read in full from the repository, together with the complete later REVIEW-10 M-CUT-EXPANDER outcome. The current accepted record explicitly asks for coefficient realization or a stronger obstruction; this is not settled by the overview's more generic primary-comparison wording. The present finite actual-rank realization and homogeneous-weight obstruction address that existing successor without replacing it with a generic comparison.

The accepted review identifies fixed-cut Green rank algebra, the all-square20-plan graph-capacity guarantee, the two-stage lift rank(H(F))=(r+s)N+rank(F-YX), and all relevant limitations. Our finite certificate uses its broader grammar and advances the actual-rank issue. It does not re-prove all historical checks or reconstruct an unavailable original upload.

The four index formulas match Construction8.1 in Hoory–Linial–Wigderson, *Expander Graphs and their Applications*, PDF page69 (printed page69), with Theorem8.2 supplying the5sqrt(2) spectral bound. The source gives graph expansion, not these gamma_q, the10+10 product ranks, or a Fourier realization. All-cut capacity is also directly counted in our finite checker; no rank conclusion is inferred from the spectral bound.

Accepted repository source: https://github.com/AgentSlop-Si/research/blob/2eaef05b9bbd6a9c884596179babe9cf474a8ff2/math/archive/objects/e5/e52478975ec0e501026145bf62e9bd58dde6ea0bb4c0718d7382d5d78d20a06e__REVIEW.md

Primary topology reference: https://www.math.ias.edu/~avi/BOOKS/expanderbookr1.pdf

The source filename encodes the historical identity e5247897..., while the retrieved sanitized derivative's content hash is recorded separately in SOURCE_REGISTER.json. Neither is called the other. Original-byte and historical-replay boundaries remain intact.

### Disposition

After independent acceptance, record this bounded increment on the same M-CUT-EXPANDER row, keeping TO RESEARCH and priority42. Do not create another discovery count or raise novelty. Retain all prior cell history.

The concrete remaining coefficient gate is now: either construct an exact Fourier identity in the intended legal vertex-weighted two-stage grammar (with complete denominators and charged preparation), or prove an obstruction covering that nonhomogeneous grammar. The constant-vector exclusion cannot close that gate. Uniform actual-cut-rank attainment by the displayed coefficient recipe beyond N=4,9,16 is also not proved; it should be investigated only if relevant to the selected Fourier gate, rather than silently replacing it. The supplied lifted compatibility condition remains necessary and exact, without becoming a fast rank test.

No external write or historical-program execution occurred in this work. Only the fresh self-contained checker was executed. This report makes no new worldwide-priority, Fourier-construction, unrestricted-runtime or production-readiness claim.
