# A sharp growing-fiber centered family and a genuine sparse approximant

18 October 2026 UTC. New restricted construction, pending independent review.

## Result and boundary

There is no nonzero centered source with a constant-size exact Fourier support at the accepted oversampling ratio. This is a property of the centered source itself, not just of the old singleton supplier. The smallest possible exact support has at least M−N+1 entries.

The following explicit family attains that lower bound. Let M=2^m, N=M/4, and let the actual original N-vector be constant and nonzero, with a canonical Gaussian-dyadic value c 2^−F. Its correctly centered, normalized Fourier target has exactly 3N+1 nonzeros: frequency zero and three growing residue fibers modulo four. Thus three short fiber descriptions do not mean three Fourier coefficients.

A new deterministic provider evaluates a truncated Dirichlet formula at only S=1+3·2^ceil(m/4)/2 frequencies. It produces finite dyadic Z on the accepted P=16m+16 grid and proves

    ||Z − U_M J_N u||_infinity <= M^−1/4 ||u||_2.

This discharges, with room to spare, the accepted outer theorem's beta=1/4 premise for this explicitly restricted original family. The input, centering, normalizer, grid, coefficient cap, scale, and all costs are bound below. This is a valid source-level composition with the accepted outer theorem. It is not a general sparse-recovery implementation or an execution of the whole outer stream.

The new standalone front end was executed. Its final fresh batch includes three complete front-end runs, one of which freshly scans and replays all 512 entries of a dense original. It writes 39 front-end coefficient records. Independent rational direct-sum checks cover 20 more coefficient evaluations; exact cyclotomic controls establish the claimed support patterns at seven small sizes and the centered inverse identity at 56 coordinates. No historical program was imported or executed; no external write occurred.

## 1. Frozen premises and precise change of interface

SOURCE_BINDINGS.json binds the inspected accepted centering obstruction, its independent review, the dense dispatch/report review, and the actual outer theorem and median grammar. Those are read-only source premises. The accepted centering review's conclusion and the dense review's distinction between FIRST_DFT and SINGLETON_SECOND_NORMALIZED remain unchanged.

The transform is the negative unitary DFT

    (U_L w)_k = L^−1/2 sum_j w_j exp(−2 pi i j k/L).

J_N places coordinate j at residue j−a0 modulo M, where a0=floor((N−1)/2). The old singleton supplier started with a sparse M-vector x and supplied U_M x/alpha; its recovery targeted R_M x/alpha. None of those operations is reused or relabeled here.

The new original is an N-vector u0. The new provider's exact source is v=J_N u, and its exact spectral target is z=U_M v. The final target after the accepted outer stage is U_N u0. Restricting u0 to an explicitly recognized constant vector is the scope of this construction. No claim is made that an arbitrary prior sparse original belongs to it.

The provider evaluates a known source formula. It does not recover unknown support from bucket values. In particular, it imports none of the old 29-call recovery theorem, hash-isolation probability, hidden source descriptor, or original support witnesses. Its success guarantee is deterministic.

## 2. The sharp exact-support barrier and a minimal witness

If a nonzero z has s Fourier coordinates and U_M^−1 z is supported in the centered N-interval, that inverse transform has M−N consecutive zeros. Any s consecutive zeros of a transform of an s-supported vector give a nonsingular Vandermonde system: its columns have distinct nodes exp(2 pi i k/M). Therefore s>M−N. Equivalently,

    |supp(U_M J_N u)| >= M−N+1,  for every nonzero u.

The sign reversal relative to the already accepted forward-transform proof changes the nodes but not their distinctness or Vandermonde determinant. This extends the accepted obstruction from the old supplier overlap to every exactly centered nonzero source.

Now take m>=3, N=M/4, u_j=a for every j, with a nonzero complex scalar. For z=U_M J_N u,

    z_0 = a N / sqrt(M),
    z_k = a/sqrt(M) · exp(−pi i k/M)
          · sin(pi k/4) / sin(pi k/M),  k!=0 mod M.      (1)

To derive (1), sum the N-term geometric progression. Its phase after centering is

    exp(2 pi i a0 k/M) exp(−pi i (N−1)k/M)
       = exp(−pi i k/M),

because N is even and 2a0=N−2. This residual half-sample phase is essential. Dropping it gives the wrong centered target.

The denominator in (1) is nonzero away from k=0. The numerator vanishes precisely when k is a multiple of four. Thus the exact support is

    {0} union {4r+1:0<=r<N} union {4r+2:0<=r<N}
        union {4r+3:0<=r<N},

of cardinality 1+3N=M−N+1. The lower bound is attained. Each residue fiber has N entries, so the exact spectrum is dense in coordinate count even though it has a short algebraic description. For M=2^28 the exact support is 201,326,593, not sixteen.

An exact representation consists of the original parameters and the above formula, or the equivalent finite expression using a formal primitive Mth root of unity. This is an algebraic descriptor, not a list of exact Gaussian dyadic coefficients and not a free point-value oracle. Exact coefficient expansion or numeric queries must be charged separately.

## 3. Actual original, normalization, and recognition

The original grammar has exactly m, F, kind, data. The supplied constant representation has data=(Re c,Im c), meaning all N coordinates are c 2^−F. The dense representation contains all N integer pairs and every one must equal the first. The current reference admits 11<=m<=28, component width at most 1024, and F encoding at most 128 bits; a dense scan additionally requires N<=4096. The mathematical family is not restricted by these engineering ceilings.

c is nonzero and at least one Cartesian component is odd, making F the canonical common-grid exponent. Exact built-in integer and fixed-shape checks exclude booleans, coercions, extra dictionary keys and overloaded equality. Oversized numeric fields are screened by bit_length before a magnitude copy. Every admitted dense coordinate is inspected; a different last coordinate is rejected after the paid full scan. A compressed descriptor is an original input representation, never a claim to have inspected an unavailable dense array.

Put

    E=N |c|^2,
    h=ceil(log2 sqrt(E)) = ceil(bit_length(E−1)/2),
    a=c 2^−h,  u_j=a,
    R=||u||_2=sqrt(N)|a|,
    lambda=2^sigma,  sigma=h−F.

Then 1/2<R<=1 and u0=lambda u exactly. The source is retained as immutable m,N,F,c,h,sigma and original representation kind. The reference checks |sigma|<=4m before coefficient preparation, so the accepted outer scale contract holds with d=4. An enormous symbolic exponent is not silently materialized. A zero input is deliberately outside this nonzero family; its separate zero branch remains necessary in a general dispatcher.

Recognition of an arbitrary dense array as exactly constant needs every coordinate in the worst case: otherwise change an unread coordinate. This is a recognition lower bound, not a lower bound for every approximation task. If W is raw component width and f is the encoding width of F, reading the dense representation costs at least its actual input bits and N visits. A safe schoolbook upper bound is O(N L^2+L^3), where L=2+m+W+f. Compressed recognition and normalization cost O(L^3). The descriptor retains O(L) bits. A caller retaining its original dense array for independent future replay additionally retains O(N(W+m)) bits; these do not disappear from total live storage.

## 4. A genuinely sparse, deterministic approximation

Fix beta=1/4 and put

    K=2^ceil(m/4),
    A={k mod M: −K<=k<=K, and k=0 or 4 does not divide k},
    S=|A|=1+2(K−K/4)=1+3K/2,
    P=16m+16,  rho=2^−P.

For m>=11, K<M/2, K is divisible by four, and these indices are distinct. The provider evaluates only A, rounds each coordinate to the P-grid with certified complex error at most rho, and returns zero outside A.

For nonzero circular distance d=dist_M(k,0), concavity of sine on [0,pi/2] gives |sin(pi k/M)|>=2d/M. Since |sin(pi k/4)|<=1 and M=4N, (1) yields

    |z_k| <= |a| sqrt(M)/(2d) = R/d.                    (2)

All omitted nonzero coefficients have d>K, hence |z_k|<R/K<=R M^−1/4. Omitted multiples of four are exactly zero. Every retained error is at most rho, and rho<=R M^−1/4 because R>1/2 and P>1+m/4. Therefore

    ||Z−z||_infinity <= R M^−1/4 < 4 R M^−1/4.        (3)

The exact target is still the 3N+1-supported z. Only Z is sparse. No unproved exact-sparsity condition is being passed into the old recovery theorem. In addition, |z_0|=R/2>1/4; the returned approximation at zero is genuinely nonzero.

Unitarity gives |z_k|<=R<=1, so |Z_k|<=1+rho. Every Cartesian P-grid numerator is consequently strictly below 3 M^2 2^P, the outer every-tape cap. These are unconditional numerical guarantees for every admitted input. There is no random failure event or hidden success-conditioned resource bound.

## 5. Entire finite evaluation and certificates

centered_source.py contains the new provider. It imports only Python's dataclasses, fractions and integer isqrt. It calls no floating transcendental routine, predecessor implementation or root-table oracle.

Set Q=P+2m+16. One paid Machin pi enclosure is prepared by the exact alternating series for atan(1/5) and atan(1/239), Q+10 terms each, and pi=16 atan(1/5)−4 atan(1/239). The enclosure is reduced outwards onto grid Q+16. For any requested angle pi·j/M, reduce j modulo 2M to a signed representative of magnitude at most M. Taylor's complex exponential polynomial of degree Q+40 at the midpoint angle is evaluated with exact rational arithmetic. The error interval includes both angle uncertainty and 4^(Q+41)/(Q+41)!; the real-argument integral remainder justifies the latter without an exponential multiplier. Both Cartesian intervals are then reduced outwards onto the Q-grid.

The same elementary factorial bound used in the accepted dense construction gives this remainder at most 2^(−2Q−18). The reduced pi radius is below 2^(−Q−15). Thus each returned Cartesian endpoint differs from its exact sine or cosine by less than delta=4·2^−Q. The code also checks the returned interval width.

The reciprocal square root is enclosed using

    A=floor(sqrt(floor(2^(2Q)/M))),

and the interval [A,A+1] 2^−Q, collapsing the interval if A^2 M=2^(2Q). These are exact integer comparisons, not guessed normalization bits.

For k!=0 in A, sin(pi k/M) has magnitude at least 2/M. Because delta<1/M, its enclosure is separated from zero. Exact rational interval division encloses the ratio in (1). The residual phase is taken from the same certified sine/cosine pair, with the negative imaginary sign. The raw normalized a, ratio, reciprocal square root and phase are multiplied as outward interval operations. k=0 uses the separate exact-limit expression aN/sqrt(M), never a zero-over-zero division.

For completeness, the fixed precision suffices without an adaptive precision assumption. For possible denominator and numerator endpoints d',n', the ratio q'=n'/d' differs from q=n/d by at most M^2 delta; |q'|<=M. Multiplying its root interval changes the real gain by at most 3M^2 delta and leaves magnitude at most 2M. Each phase coordinate then has error at most 4M^2 delta. Rotation by a, with |Re a|+|Im a|<=2, gives final Cartesian interval endpoint errors at most 8M^2 delta. The complex half-diagonal radius is at most 12M^2 delta. Therefore rounding its midpoint to the P-grid gives a maximum complex endpoint distance below

    rho/sqrt(2) + 12M^2 delta
      = rho/sqrt(2) + 48 rho/65536 < rho.

At k=0 the corresponding bound is smaller, at most rho/sqrt(2)+2N delta. The reference nevertheless checks the exact rational sum of squared Cartesian endpoint distances against rho^2 before returning every coefficient. A failed certificate raises a typed rejection with its paid prefix; it never becomes a successful approximate answer.

The arithmetic ledger records rational operands/results and bounds each fixed primitive by a conservative cubic width envelope, including gcd and integer-root work. Its separate global control envelope covers indexing, comparisons, sorting the S locations, scalar copies, loop and ledger counters, and immutable result construction. Failed grammar/scale prefixes retain a receipt. Serialization of the result, the independent oracle, and any downstream execution remain separate work.

## 6. Concrete composition with the accepted outer stage

For every admitted m>=11, choose D=5. Then t=160m+4<M, P is exactly the outer grid, and M is the least power of two at least 4N. The actual local median input is the single immutable row of returned coefficient pairs, with the actual sorted candidate tuple A. Its Cartesian median is exactly Z, not an asserted random-recovery result.

The source-level integration recipe uses the accepted APIs as follows:

1. Run the new provider against the actual original and retain its immutable Source and returned Estimates together.
2. Extract candidates=tuple(k for k,pair in Estimates.pairs) and rows=(tuple(pair for k,pair in Estimates.pairs),). Pay these copies.
3. Call the accepted produce_medians(M,P,candidates,rows,L_outer).
4. Construct Outer(Header(N,M,5,P),produced,L_outer). Its actual median replay is paid.
5. Run FullTransfer(outer,TransferConfig(1,4,sigma,4)). Preserve the original/source association at the caller level. A request for semantic source replay reruns the new provider and compares its entire result; replay of the median alone proves only the row association.

The exact input row for the m=11 example is delivered in EXAMPLE_MEDIAN_INPUT.json. All values were produced by the new evaluator. The accepted median/outer programs were not executed in this packet. This is a mathematical composition theorem and an executable new front-end witness, not new integrated outer execution evidence.

All conditional outer hypotheses now hold against the same original, so its accepted theorem gives, deterministically,

    ||Y−U_N u0||_infinity <=
      [3t E_M + t eta(1+E_M) + 12·4^(−5m) + 2^(1−b)] ||u0||_2,

where E_M=4M^−1/4, eta=2^−8m, b=ceil(9m/4). The stronger (3) could improve the constant, but no improvement is needed for compatibility. The final scale-back is exactly the accepted representation of 2^sigma, including its paid physical numerator shift when required. All N output writes remain mandatory.

At the small executed m values this inherited bound is very loose. These runs verify target compatibility and certified coefficient production; they do not demonstrate a practically accurate or fast outer transform. In this particularly simple original family U_N u0 already has a closed form, so the composition is an interface witness rather than a competitive algorithm for constant vectors.

## 7. Complete representation, recognition, and composition costs

Let L=2+m+W+f, and retain the actual prior-history width H required by the accepted outer cost erratum. Q=O(m). Each pi/Taylor series has O(L) exact rational operations and O(L^2)-bit intermediates: a denominator bound follows from the angle-denominator powers, factorials and the product of the series denominators. With schoolbook cubic primitive envelopes, one certified coefficient costs O(L^7), including its constant number of root evaluations. The source-level bound pays the entire pi preparation, inverse square root, all S coefficients, exact interval certificates, rounding, location construction, counters, and output records:

    T_front = O(N L^6 + S L^7) for a supplied dense original,
    T_front = O(L^3 + S L^7) for a supplied constant descriptor.

The deliberately conservative global receipt uses the largest reached numeric width, O(L^2), even for input/control events. This explains the N L^6 term; it is not a claim that equality recognition intrinsically requires that much arithmetic. The N term is not inferred away when all entries happen to agree. The descriptor's exact three fibers are not expanded; expanding their exact support would require 3N+1 locations and value computation separately. No cost for 3N+1 exact numbers has been replaced by O(1) under the word “fiber.”

The accepted one-row producer and its mandatory median replay add O((S+1)H^2) binary work and O((S+1)H) retained/produced bits. They do not replace source replay. If source replay is requested, add another full T_front, its real input scan, and the separately charged strict comparison. The reference's replay returns separate production and comparison receipts, and never calls user-defined equality.

The accepted outer stream has E_outer<=S t incidences and adds

    O(N m^2 + S m^6)

binary work for fixed D=5, beta=1/4, d=4 and bounded O(m) original row/history widths. With arbitrary history retain the actual H cost and prior receipts instead. At least N output writes are paid regardless of support.

For the fixed family W,f=O(m) and bounded O(m) history-counter widths, the combined source-level bound is

    O(N m^6 + M^1/4 m^7) binary work.

The conservative global ledger deliberately overcharges simple input visits at the largest reached rational width. No linear-word bound is claimed for this packaged reference. A sharper separated implementation could account for its read/output passes and coefficient arithmetic independently, but that optimization is not needed for this interface result and is not silently credited here. This is not a general fast DFT and does not extend the finite reference beyond its stated caps. For unbounded W, f, prior histories or scale limits, use the full parameter-dependent costs instead.

New peak data, excluding an independently retained dense caller copy, are O(Nm+Sm+L^2) bits after downstream output is included; the original constant descriptor costs O(L). Retaining the input dense array adds its actual O(N(W+m)) bits. Cumulative produced/control bits, exports and retained audit traces are distinct from peak storage and remain charged separately. The reference receipts cover its own production only, not the old outer implementation, process launch, test oracle, file export or future replay.

## 8. Fresh evidence, limits, and remaining supplier lemma

The final fresh batch in RESULTS.json records:

- Exact cyclotomic-ring support checks at m=3,...,9, attaining M−N+1 each time; exact inverse centered identities at all 56 coordinates for M=8,16,32.
- Twenty coefficient checks against independent direct centered sums. The oracle uses pi/4=atan(1/2)+atan(1/3), separate even/odd Horner polynomials and integer-bisection square-root intervals, with exact rational squared-error comparisons. It does not use the production Dirichlet ratio as its target oracle.
- Two complete compressed-source runs: m=11, c=1, F=0 and m=12, c=3−i, F=3. Each writes thirteen certified sparse coefficients, including a nonzero zero-frequency value.
- A complete fresh dense-source replay at m=11, scanning every one of 512 original entries and writing thirteen more coefficients, plus a separately recorded strict comparison.
- Seven paid rejection controls, including a changed last dense coordinate, noncanonical coefficient, excessive scale, pre-outer dense boundary, boolean component, zero input and oversized component.
- Allocation-free structural plans through m=1024. These check exact guards and formulas only; they do not claim to have run a transform or written those outputs.

There was one exploratory front-end smoke run before the final source was repaired to expand comparison/prefix accounting. It is not included as a final-source run or used as independent evidence. The final batch was rerun after those repairs.

The new stopping result is a genuine nonzero centered-source family with sharp exact-support accounting, a certified sparse approximation, and a proved source-level outer composition. Independent review remains required. Integrated full-outer execution of the new provider, arbitrary original vectors, nonconstant/general balanced blocks, unknown-support recovery from measurements, the all-length general sparse branch, and ALG-034 remain open.

For a general extension, the missing supplier lemma must start with an actual retained original u0 and prove paid access to the centered source J_N(u0/lambda), followed by a deterministic or explicitly randomized sparse approximation to its generally dense exact spectrum. It cannot assume exact few-coordinate spectral support: the lower bound in section 2 forbids that for every nonzero source. It must give source-dependent approximation/recovery guarantees, every-tape caps and complete representation/recognition/query costs. This packet supplies that lemma only for the explicitly recognized constant-block family.
