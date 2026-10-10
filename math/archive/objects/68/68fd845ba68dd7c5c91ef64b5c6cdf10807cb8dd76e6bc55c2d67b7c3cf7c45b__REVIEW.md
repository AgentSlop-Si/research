# Baseline queue1, rows 40–59: independent scoped review

## Result and coverage

All 20 assigned texts, 175,714 bytes and 20 distinct SHA-256 values, were fully inspected. This completes the main reviewer's rows 40–199: 160 texts and 582,130 bytes. The independently assigned rows 0–39 have a separate sealed report and are integrated separately. `COVERAGE.json` pins each source, its provenance, exact inert snapshot, substantive claims, acceptance and remaining dependencies. This is full **text inspection**, not approval of every referenced theorem, implementation, appendix or numerical result. No supplied program was executed.

The principal accepted mathematical results here are the scoped unitary mixer construction (with one depth-zero correction), the nonuniform Fourier rigidity inequality, the fixed-kernel preparation recurrence, the path-Green Fourier conjugation/inverse identities, and the explicit condition-reset bookkeeping repairs. None supplies a general faster exact FFT. Historical originality and publication priority were not established.

## 1. Unitary tree/path mixer, row 40

For real symmetric path adjacency A, the Cayley transform C_a(A)=(I+iaA)(I−iaA)^{-1} is unitary. With ||A||₂≤2, one has ||C_a−I||₂≤4a and ||C_a−I−2iaA||₂≤8a² for a>0. Multiplying the two path factors gives error at most 32a² from I+2ia(A₁+A₂).

For a balanced cut with E path-edge occurrences, the crossing multigraph has maximum degree four. Greedy induced matching deletes at most 32 edge occurrences per selection. A diagonal compression of the crossing adjacency therefore has at least ceil(E/32) singular values at least one. At a=1/32, the Cayley product has that many crossing singular values at least 1/32. The preceding batch's independently checked balanced-word counting/union-bound argument supplies E>N/16 for every balanced cut with the stated high probability, for N divisible by 16 and N≥32. Simultaneous relabeling fixes the first path without changing the distribution.

The tree Cayley B=C₂(A_T) is symmetric unitary. Leaf elimination has positive real pivots d₀=1 and d_h=1+8/d_(h−1). Writing D₀=D₁=1 and D_(j+2)=D_(j+1)+8D_j gives d_h=D_(h+1)/D_h. At positive tree depth L, each root-column leaf entry in B has magnitude 2·2^L/D_(L+1), yielding a leaf contribution 2·4^L/D_(L+1). With λ=(1+sqrt(33))/2<4 and D_j≤λ^j, this gives induced-one norm growth Ω(m^θ), θ=log₂(4/λ)>0. Symmetry and unitarity give the corresponding inverse/infinity norms.

**Literal endpoint correction:** at depth L=0, B=2I−I=I; the leaf contribution is one, not two. The displayed leaf formula applies only for L≥1, where root and leaves are distinct. The asymptotic N≥32 construction uses positive depth and is unaffected. Fresh rational controls explicitly retain this exception.

For R=[[0,B],[B*,0]], R is a Hermitian involution. V=(I+ieR)/sqrt(1+e²), e=1/512, is unitary and ||V−I||₂<1/64. Thus S=VU retains at least the stated number of crossing singular values ≥1/64. The path factors have bounded induced-one norms, at most (17/15)² together, while V's norm grows; symmetry/unitarity transport this to growing induced-one condition number. All path/tree solves and vector operations have linear field cost, including preparing the eliminations from supplied paths. The fixed algebraic normalization constant belongs to the stated exact-complex model.

The random permutation setup is linear with a unit-cost uniform-range random oracle, or expected linear under ordinary rejection-based random-word generation. A literal deterministic worst-case bounded-bit guarantee requires further qualification. Modular unnormalized-Q controls cannot certify complex unitarity; the source correctly separates these. Its actual implementation, operation tables and numerical experiments were not replayed.

## 2. Green conjugation and fixed profile gates, row 41

For the signed full cycle M with M^N=−I, the geometric identities for K=I+(I−M)^{-1} and K^{-1} are valid under their displayed guards. In particular, the inverse has denominator 2^N+1, which is an additional finite-field guard. The induced-one norms are (N+2)/2 and 2^N/(2^N+1). The claimed growing condition is asymptotic; N=2 is an exceptional unit-condition case.

For the natural tridiagonal T and positive-convention Fourier F, the displayed H=FTF^{-1} is diagonal plus rank two, with entries

H[k,l]=(3−q^k−q^(−k))·[k=l]+(q^l+q^(−k))/N.

The Woodbury core and the identity, for S=T^{-1}+(T+I)^{-1},

S^{-1}=T/2+I/4−(T+I/2)^{-1}/8

are correct. For α≥0, let A₀=3+α, g_k=(A₀−q^k−q^(−k))^{-1}, t=avg g and c=avg(qg). These are real with A₀t−2c=1. The two-dimensional core [[1+c,t],[t,1+c]] has inverse infinity norm 2/[1+(A₀−2)t]≤2. Since max g≤1/(1+α), the conjugated resolvent bound is max g+4(max g)². Combining ||H||∞≤7 with α=1/2 gives the stated 73/18 inverse error-transport constant.

The no-raw-gain statement is a coefficient-norm statement in its independent-power/sign model: when the normalized source coefficients have one-norm one and the target has infinity norm one, a rescaled descriptor still pays the stated one-norm budget. It does not prohibit useful residual structure. The two-forward-K-stage obstruction is likewise confined to the same fixed signed-cycle singular-value profile, arbitrary unitary interstage mixing, and dyadic N≥8. Scalar unitarity requires a reversed pairing of singular values; the squared product 4+9/[4(1−c²)] varies over the relevant profile. N=2,4 and changes of gains, inverses or stage count need separate treatment.

Fresh modular matrix controls cover 4,095 entries at six sizes through N=32. The analytic norm proof, not modular arithmetic, justifies the complex bounds. Source-specific executor counts, weighted-affine code and historical numerical certificates remain unrerun.

## 3. Nonuniform rigidity and scan representation, row 53

For any S, put u=min row support, s=max row support and r=rank(F−S). Then

N≤u+r(s+1).

If r<N, choose r+1 cyclic-consecutive Fourier rows containing a minimum-support row of S. Their combined S support has at most u+rs columns. If N>u+r(s+1), at least r+1 columns remain untouched. The resulting Fourier submatrix is Vandermonde with distinct nodes and is invertible, contradicting rank r. The case r≥N is immediate. This proof holds over a splitting field with primitive Nth root and characteristic not dividing N.

Erasing interleaved rank-budget-B updates from the inverse scan word leaves rank error at most B. A pure word of t invertible one-way scalar scans has maximum inverse row support ≤2^t and one boundary row of support ≤2^(t−1), after all intervening monomial factors are correctly transported. Therefore

N≤2^(t−1)+B(2^t+1), t≥1.

At t=0 the monomial version gives B≥floor(N/2). This is a representation-specific necessary condition, inherited from the source lineage; it is not a lower bound on arbitrary circuits or enlarged-state representations.

The F8 quasiseparable-order-three result is sound. A nonzero combination of at most three characters on a dyadic cyclic group has at most half its entries zero: if the exponents have mixed parity, the singleton-parity term prevents simultaneous zeros at z and −z; if all have the same parity, divide out a character and descend one dyadic level. Thus every 3×5 Fourier rectangle has rank three. The exhibited parity ordering attains the profile 1,2,3,2,3,2,1.

However, an abstract quasiseparable generator representation need not be a literal raw scalar scan. In the displayed 3×3 example, first-subdiagonal requirements a₁b₀=1 and a₂b₁=1 force a₂a₁b₀≠0, contrary to the prescribed zero (2,0) entry. This does not refute a separately supplied multichannel factorization. The external Givens theorem and any explicit F8 three-channel realization were not reverified here.

Fresh exhaustive checks cover 6,859 sparse 3×3 matrices over F7, 6,272 F8 rectangles over F17 and F97, and 2,401 raw-scan parameter tuples over F7.

## 4. Fixed-kernel spectrum and condition-reset bookkeeping

Row 55's fixed-kernel 2N-bin spectrum can be prepared by the supplied two-step recurrence v_(k+2)=(1−eta^k)v_k+(−1)^k/N. The two parity cycles have products zero and two respectively, so their closure equations determine them with the stated guards. A freshly authored checker compares all 510 values for N=1,2,...,128 with direct polynomial evaluation. This accepts the algebra/preparation mechanism, not a replay of the source's production counters or full q-Pascal executor. Its orbit compiler and sparse-forcing parts have separate proofs and controls in batches 2 and 4.

Rows 56 and 59 correctly express a three-addition exchange as W_U=[[0,−U^{-1}],[U,0]]. Successive logical banks must alternate: the next exchange is conjugated by the bank swap. Applying the same orientation twice yields −V^{-1}U on the wrong logical path. Fresh noncommuting rational controls demonstrate both orientations.

Padding a matrix P by an identity changes the relevant condition measure to max(1,||P||)max(1,||P^{-1}||). This equals κ(P) only if its singular values straddle one, for example under a determinant-modulus-one anchor. A scalar 100I has condition one before padding and 100 after padding. Thus arbitrary monomial rescalings are not automatically harmless in a full-state condition argument.

For the q-Pascal middle matrix, the diagonal endpoint magnitudes alone imply κ≥N at every primitive complex root. At the canonical root and m=floor(N/8), the product estimate |1−q^r|≤2πr/N≤π/4 gives κ≥N(4/π)^m, hence ≥N(14/11)^m. The factorial/AM–GM bound yields N[7N/(22(m+1))]^m. Since P_after=M P_before, at least one adjacent prefix condition is ≥sqrt(κ(M)). These are square-state conclusions. Transparent local replay, externally supplied fast blocks, full scratch-state accounting, coefficient bounds and an effective paid scheduler remain hypotheses. An arbitrary unbounded budget function is not automatically a computable construction.

## 5. Remaining texts and scope limits

- Row 43's Hasse/Taylor-jet expansion over a commutative convolution ring avoids division by factorials. Degree, input preparation and memory costs stay explicit.
- Row 44's affine-cycle evaluator is a genuine restricted-family construction with majority discovery, full residual verification and a nonsingular target-cycle guard. The separate rows0–39 helper package supplies further independently authored controls for this same mechanism; integration records the exact link.
- Rows 45 and 54 retain supplied-state and output-size assumptions in their pruning/cache/low-rank identities. The sentence about k=N^alpha giving Theta(N log N) describes that schedule, not every structured input family.
- Row 50's sign-atom concentration calculation is valid in its stated probabilistic/error model. Finite descriptors alone do not make irrational Fourier entries exact. Full packing/word-width/scale/implementation obligations remain separate.
- Row 51 is a synthesis, not a replacement for the referenced full packing proofs, F32 minor certificate or exact F8 realization. Those dependencies were not silently accepted.
- Rows 47 and 52 distinguish adaptive organizer heuristics from worst-case variable-consumer complexity. Replanning is not generally O(1); publishing q outputs costs at least q; cached float results need not be bitwise identical. The cubic candidate-count formula is arithmetically consistent.
- Row 58's query count needs an output-writing +q term when its rank/edit count vanishes, and the threshold optimizer assumes an approximately constant flush cost.
- Rows 42,46,48,49,52 and 57 preserve engineering audits, captured logs and timing/operation tables. Their test counts, claimed defects, measured errors, RSS and runtimes are historical source evidence. Reading these is not rerunning them.

The source bibliographies were not comprehensively re-audited in this batch. All code dependencies, historical logs and missing full proofs remain explicitly scoped in `COVERAGE.json`.

## Replay and integrity

Run `python check_final_lemmas.py` for newly authored exact controls, `python isolated_replay.py` for a byte-identical result in a clean temporary directory, and `python verify_seal.py` to verify pinned package bytes. The checker imports no supplied source. `INDEPENDENT_RESULTS.json` records exact control counts. Manifest integrity does not itself imply theorem correctness.
