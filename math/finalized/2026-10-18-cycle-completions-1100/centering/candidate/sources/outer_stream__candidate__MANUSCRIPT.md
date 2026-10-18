# Complete retained outer transfer with an exact t<M boundary

18 October 2026. **New author candidate; independent final review pending.**

## Result and exact scope

This closes a distinct executable stage left open by the accepted coefficient and iterator work: a genuine locally computed sparse-median output now passes through **every** retained coefficient, exact complex estimate multiplication, exact signed scatter, one final rounding for **all N rows**, and exact scale-back. Every prefix is paid. A fresh run evaluates all 885 coefficients for an N=257, M=2048, D=5 four-support fixture and checks every returned row against independent guaranteed target intervals. No selected-coefficient subset is substituted for the stream.

The stage has an explicit deterministic contract for all its accepted inputs, including arbitrarily unsuccessful recovery outputs subject to the declared every-tape magnitude cap. It also has a conditional original-target error theorem when the separate source and recovery premises are supplied. Those premises are not manufactured by the local median binding.

The t<M guard is proved and characterized exactly. A failed guard returns a specific dense-transfer requirement **before scalar setup and N allocation**. The sparse-output interface does not contain the original signal needed by the prescribed dense branch. This is the precise remaining interface dependency, rather than an implicit assumption that a dense result exists. Full sparse recovery, original-signal provenance, a dense/all-length executable, and independent amplification remain outside this result. ALG-034 stays open; Q16/STR-Q1 archived status, novelty, and theorem claims are unchanged.

## 1. Accepted dependencies and model

The following byte-identical local dependencies were independently accepted in the preceding cycle:

- production_scalar.py: SHA-256 73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e. Fixed-D schoolbook source bound and complex eta certificate are owned by q16_scalar_final_review_20261017_2140/REVIEW.md.
- outer_wrapper.py: d26c4cfe6d6c1430ce59b682f24bf69e2560fae81e8de60c63fc435b69b0637e.
- sparse_output.py: 92577edf07395237940aad94326a8d1e5c4a18b194a9162af84ada2d826edafa.
- The last two depend on q16_wrapper_final_review_20261017_2143/REVIEW.md **together with ERRATUM.md**, which corrects the arbitrary-row-count/cumulative-counter cost and includes retained original-row storage. That clarification remains mandatory here.

The model is trusted local execution with exact immutable built-in tuples and integers. The median output is actually computed, and Outer pays semantic replay against its immutable original rows. An arbitrary hash, label, or caller output assertion is not a producer. This is not hostile-runtime security, unknown-origin authentication, or historical execution attestation. The fresh stream never accepts externally supplied coefficient records or an arbitrary callback.

The inherited all-length mathematical theorem supplies the centered interpolation identity and tail estimate, and its section 6 supplies the every-tape median magnitude bound. This manuscript identifies those as premises rather than reproving the underlying sparse-recovery theorem. Its source is q16_scalar_completion_20261017_2129/sources/evidence/accepted/ALL_LENGTH_THEOREM.md, whose recovery qualifications continue to apply.

No prior artifact was modified. No external write or publication was attempted.

## 2. Input/output contract

Let N>=1, D>=5 be exact integers and M=2^m the smallest power of two at least 4N. Write

    s=Dm, h=16s+1, t=2h+2=32Dm+4,
    P=16m+16, eta=2^-((D+3)m), p=(D+3)m+3.

Receive an accepted bound Outer instance. Its actual locally produced median result has a sorted distinct support K subset {0,...,M-1}, |K|=S, with exact complex values

    Z_k = (a_k+i b_k) / 2^P.

Zero entries may be retained and are charged. The new stage explicitly checks

    |a_k| < 3 M^2 2^P and |b_k| < 3 M^2 2^P.             (A)

This is the accepted front-end's every-tape cap, not a success-conditioned estimate. Original input rows can be wider than their medians; their reading, sorting, retention and semantic replay remain separately charged at their actual widths.

Receive a positive fixed rational beta=bn/bd<1/2, an exact integer d>=1, and a scale power sigma with |sigma|<=d m. For the fixed-family complexity assertion, D, beta, d are fixed parameters with fixed encodings. The general callable interface still pays actual widths, including an unreduced rational beta encoding or large d. Define exactly

    b = ceil((beta+2)m).

The result is an immutable N-tuple of Cartesian integer pairs with one nonnegative denominator exponent, representing Y. The initial round is on normalized grid 2^-b. Scale-back multiplies by 2^sigma: if b-sigma>=0, the numerator stays unchanged and the denominator exponent becomes b-sigma; otherwise the numerator is shifted by sigma-b and the exponent is zero. Both are exact representations of the same scaled value.

The output retains the identical accepted source binding and a single-use local owner identity. Replacing the returned output object or fields is rejected. This does not add an original-signal association missing from the supplied median context.

## 3. Full stream, coverage and t<M

For each supported k, the accepted iterator emits the integer lifts

    r0 = ceil(N(k-h-1)/M), r1 = ceil(N(k+h+1)/M),
    r0 <= r < r1, ell = r mod N.

The row stencil is k = floor(ell M/N)+j modulo M for -h<=j<=h+1. Lifting ell by multiples of N proves that the emitted interval is exactly equivalent to this stencil. For t<M its real length Nt/M is less than N, so reduction modulo N is injective. Distinct support indices then give distinct ordered incidences. Every row contains at most t terms and

    E = sum_k (r1-r0) <= S ceil(Nt/M) <= S t.

The fresh FullTransfer owns this complete iterator. Every ordinal must equal the next expected ordinal; every coefficient is generated and source-validated through that same Outer object; its incidence and p-grid must match. At termination, the consumed and evaluated counts must equal the sum of the paid endpoint lengths. No skipped coefficient is inferred from its predicted smallness or from a zero estimate. A missing first/intermediate item, duplicate, reorder, or missing suffix cannot yield a completed result. The code uses no E-record collection.

### Exact guard classification

For allowed D,m the guard is precisely

    D <= floor((2^m-5)/(32m)).

Equality t=M cannot occur: for m>=5, 2^m is divisible by 32 whereas t is 4 modulo 32; for 2<=m<=4, D>=5 already gives t>M. Thus every failed guard has t>M. The ratio (32Dm+4)/2^m strictly decreases for m>=2 and tends to zero. For each fixed D there is a single finite first permissible m; all larger m pass. For D=5 it is m=11, corresponding exactly to 257<=N<=512 for that first block. The preceding m=10 block fails.

The same guard implies M>32s+4, so q=floor(M/(8s))>=4; the kernel is in its accepted nondegenerate regime. Also b<=3m while p+P=(D+19)m+19, so the final rounding shift is always nonnegative on this domain.

The strict guard is substantive. At N=256,M=1024,D=5,k=0, the unguarded lift interval emits 401 records but only 256 distinct rows. Treating this as a sparse incidence set double-counts coefficients. More generally, when t>M the total lifted incidence count over all M columns is Nt>NM, so at least one column must repeat a row. Every fixed row's t consecutive stencil offsets also repeat residues. This refutes an unguarded reuse of the accepted uniqueness and row-sparsity reasoning.

The mathematical half-open interval is injective even at the hypothetical equality t=M, but this equality is unavailable in the actual parameter family. No guard relaxation is being proposed.

## 4. Exact scatter and every-prefix width

Set w=P+2m+2, so (A) implies |a_k|,|b_k|<2^w. The accepted scalar certificate gives complex |Ctilde-C|<=eta with |C|<3, hence |Ctilde|<4 and, in particular, each Cartesian p-grid numerator has magnitude <4*2^p. The code checks that Cartesian bound too.

For coefficient numerator c+i d and estimate numerator a+i b, calculate exactly

    real = a c - b d, imag = a d + b c.

These four products and two sums use no intermediate rounding. A Cartesian contribution has magnitude strictly less than 2^(p+w+3). Every row has at most t distinct terms. Any prefix of any row therefore has magnitude strictly less than

    t 2^(p+w+3) <= 2^(p+w+3+ceil(log2 t)).

A signed allocation of

    W_acc = p+w+4+ceil(log2 t)

bits suffices on every tape. In the usual signed range [-2^(W_acc-1),2^(W_acc-1)-1], the strict positive-side inequality also covers the negative side. The implementation checks this at every update, together with the row term count, so a large intermediate sum followed by cancellation cannot hide an overflow. Python integers do not wrap; a violated invariant is a deterministic contract/implementation failure, never a sparse-recovery failure event.

N real, imaginary, and count slots are explicitly initialized and paid. All E contributions are accumulated on common exponent p+P. Each of the N Cartesian rows is rounded only once, by signed floor/remainder nearest-even, to exponent b. The complex rounding error is at most 2^-b (the tighter sqrt(2)/2 factor is unnecessary). Exact scale-back follows the representation rule in section 2. Even empty support returns and pays all N zeros and does no pi/sqrt setup.

## 5. Universal deterministic and conditional target theorems

### Every accepted sparse output, every tape

Let C be the exact retained phase/interpolation matrix from the accepted coefficient target, and let I_ell be row ell's active support. The produced output satisfies

    |Y_ell - 2^sigma (C Z)_ell|
      <= 2^sigma [eta sum_(k in I_ell) |Z_k| + 2^-b].       (1)

Proof: each complete emitted coefficient is within eta in complex modulus; exact multiplication and summation add no arithmetic error; triangle inequality bounds their combined perturbation by the sum displayed; the sole final round contributes at most 2^-b; scale-back is exact. This argument uses no successful-recovery event. The checked cap gives sum|Z_k|<3 sqrt(2) t M^2 if a uniform all-tape numerical envelope is desired.

For independent interval tests we use the valid upper bound sum|Z_k| <= sum(|a_k|+|b_k|)/2^P. This is a test bound for (1), not a replacement of complex eta by a Cartesian tolerance.

### Conditional original normalized input

Suppose separately that an actual normalized u in C^N is centered into v in C^M as prescribed by the accepted theorem, that R=||u||_2>1/2, and that z=U_M v. Suppose its actual sparse result satisfies the simultaneous event

    ||Z-z||_infinity <= E_M R, E_M=4 M^-beta.

The inherited centered identity is U_N u=D_phase B_full z, with retained C and tail operator norm at most 12*4^-s. Therefore the normalized output obeys

    ||2^-sigma Y-U_N u||_infinity
      <= [3t E_M + t eta(1+E_M) + 12*4^-s + 2^(1-b)] R.    (2)

The four terms are, respectively, recovery error through the retained row; coefficient perturbation applied to Z; interpolation tail applied to the exact z; and the final round. In particular the tail is not applied to an uncontrolled failed-tape Z, and the multiplier is t, not E or S. If x=2^sigma u, linearity and exact scaling give the same relative bound against U_N x.

The stage does not inspect a signal, establish centering, measure a recovery probability, or make random draws. Hence it cannot assert (2) without the separate premises. For ALG-034, any producer/normalization/second-transform target must stay exactly as supplied by its actual bridge: a projected or reflected projected target cannot silently be relabeled U_N of the original input. Formula (1), and conditional formula (2) under a specifically identified u, are the full claims here.

## 6. Complete costs and storage

Costs are cumulative; no constructor, validation, semantic replay, failed-prefix, repeated API call, scalar preparation, field movement or output pass is silently free. Receipt snapshots/JSON, test oracle work, hashes and process launch are separate finite harness work. The receipts are source-level binary-arithmetic/control bounds, not Python instruction counts or host-speed claims.

Let R_rows be the supplied odd median-row count. The accepted producer plus its separate paid replay use

    T_med = O(1+S+R_rows+S R_rows log(R_rows+1))

new control events per pass, with O(T_med H^2) binary work and O(T_med H) cumulative produced/control bits, where H includes actual reached data/header widths, row/address widths, prior ledger-counter widths, and log(previous events+new events+2). This is precisely the accepted mandatory erratum. The retained original rows, candidate/output records and sorting workspace cost O((S R_rows+S+R_rows+1)H) data/address bits. Do not replace this with just O(Sm).

For fixed D,beta,d, O(m)-bounded actual original input rows and O(m)-bit prior counter widths, all new outer metadata and accumulator/output fields have O(m) bits. The bound S<=M and E<=St make new counter widths O(m) too. The scalar source uses O_D(m) events and O_D(m^2)-bit intermediate integers per coefficient, yielding O_D(m^5) schoolbook bit work and O_D(m^3) cumulative produced bits. One lazy pi/root setup costs the same order and occurs once only when E>0. Consequently a safe complete binary upper bound, **in addition to the genuine producer/replay prefixes**, is

    O_D((N+S+E+1)m^2 + 1_(E>0)m^5 + E m^5).             (3)

For arbitrary prior histories or wider fixed-parameter encodings, replace the nonnumeric m-width shorthand by the actual H envelope above and retain the old receipts; there is no bound depending only on new amplitudes. Additional caller validation/reporting calls are additional work. No D-uniform m^5 claim is made.

The source explicitly has only E coefficient evaluations. The N initialization/output pass uses bounded O(m)-bit additions, shifts, comparisons, indexing and I/O. Under the accepted growing-word model these are O(1) word operations apiece; pessimistically simulating scalar bit work in words gives

    O_D(N+S+E+1 + 1_(E>0)m^5 + E m^5) word operations,   (4)

again plus the separately paid producer/replay. This is not obtained by miscalling (3) linear bit work. When the external front-end premises give S=O(M^(1/2+beta)) and R_rows=O(m), all sparse terms are M^(1/2+beta) times a fixed polynomial in m. Since beta<1/2 and M<8N, they are O(N) for each fixed family, with potentially enormous constants. The N output pass is separately O(N) words. No practical crossover or speedup follows.

Peak production storage is bounded by

    O(Nm + (S R_rows+S+R_rows+1)H + m^2) bits,           (5)

including all original rows retained for semantic replay, endpoint/prefix records, N accumulators/counts, N output records, and the fixed-number scalar integer temporaries. Scalar signed powers reach O_D(m^2) width; they are not O(m)-bit unit-cost words. Their number live at once is bounded. Cumulative allocated/control bits are larger and separately paid. No E coefficient list, row-phase cache, or N-sized transcendental pass is present. An external caller retaining emitted audit records would pay that extra memory; the production stage does not do so.

## 7. Fresh finite evidence

The final fresh capped run succeeded with exit zero, empty stderr and unchanged executed source hashes (about 40.85 wall seconds and 14,976 KiB maximum RSS, process evidence only). Full details are in RESULTS.json, TRUE_TARGET_INTERVALS.json and PROCESS_EXIT.json.

- N=257,M=2048,D=5,P=192,p=91,t=1764; four supported estimates include near-cap opposite-signed failed-tape values and a retained exact zero.
- All 885 incidences were generated, source-checked, certified and multiplied. Exactly one pi/root setup occurred. All 257 output rows were written, on normalized grid 2^-24 then scaled by 2^31 using an exact numerator shift to exponent zero.
- A fresh independent oracle encloses the exact retained target for every row. It builds row-first membership directly, uses pi=4 atan(1/2)+4 atan(1/3) with 160-term exact alternating rational bounds, 256-bit outward interval Horner sine with 48 terms and an exact factorial remainder, and isqrt with exact squared inequalities. It calls no production numerical helper or incidence iterator. Exact rational squared complex distances satisfy (1)'s conservative l1-estimate upper bound at every row.
- An additional complete N=512 one-support stream evaluates all 441 coefficients and emits all 512 rows at scale 2^-17. Its nonzero row-zero value is checked exactly against 1025/2^27; no floating tolerance is used.
- 9,243 signed rounding controls, including 1,022 exact signed ties, and 2,401 small exact complex-product controls pass.
- Empty support pays 257 outputs without scalar setup; negative symbolic scale and exponent handling are exercised.
- Dense guards, invalid beta/d/scale/grid, strict estimate-cap violations and a 10,001-bit attempted value are rejected with paid prefixes and no scalar preparation.
- Disposable test mutations drop the first incidence, drop the last, or repeat the first. None yields a completed result; paid work already done is retained.
- The concrete unguarded dense witness has 401 lifts and only 256 distinct rows.

The oracle and production differ in pi construction, sine recurrence, root method and retention traversal. The accepted scalar source proof still supplies the universal numerical guarantee; finite tests supplement it. These are fresh controls, not historical counts. The feasible fixture satisfies the complete **outer-stage** domain. Other sparse-recovery theorem guards fail at this size, so this is not a theorem-scale random-recovery experiment.

## 8. Precise remaining dependency and stopping condition

On t>=M, the prescribed dense branch needs the original normalized N-vector (or a separately authenticated source that provides it), its scale/zero context, and a charged dense transform. FullTransfer receives only the sparse-median context, not that signal. The same admissible local context, for example an empty median support, can accompany two different unbound source signals with different Fourier transforms. Therefore this interface alone cannot determine the original signal's transform or establish its original-target identity. This is an information/interface obstruction to claiming the prescribed dense implementation, not a universal lower bound on weak approximation or an assertion that a loose weak-error bound can never be met without reading that signal.

The returned dense requirement is intentional and typed. It is not a random abort and is not being advertised as an all-length dispatcher. To close that separate gate, a caller must supply the genuine original source, paid normalization/scale policy, and dense implementation, then bind both branches to the same source. To close ALG-034 full recovery, the remaining general recovery rule/probability and its precise projected target must additionally be established. Independent tape amplification is another composition stage.

The present stopping condition is independent acceptance of full_transfer.py's complete retained-stream/scatter/output contract and this proof, or a precise counterexample. Existing finalized artifacts remain frozen. Publication remains blocked and no attempt was made to evade that restriction.
