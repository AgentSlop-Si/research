# ALG-063: certified raw-input twisted-recurrence recognition

17 October 2026 UTC. Candidate supplement for independent review. No external writes and no historical-program execution.

## Result and owner boundary

A deterministic raw-vector recognizer closes a concrete part of the recorded input-discovery gap. Given a threshold r, it accepts exactly the union of vectors with at most 2r nonzeros and vectors whose cyclic first-order twisted difference is r-sparse for some unknown scalar. It computes every Fourier output in O(N(r+1)) exact-field operations, using at most one field inversion and O(N) storage. Neither the scalar nor a permutation order is supplied. Rejections have an O(N)-replayable exact certificate.

This is an elementary composition of classical majority voting with the already accepted sparse-difference evaluator. It is not claimed to be historically novel. It does not find or certify an original permuted-geometric order, fix the historical executor, or establish arbitrary-input FFT speed, uniform field construction, bit complexity or numerical stability. Keep ALG-063 OPEN at priority 42; only the named bounded recognition stage is nominated for acceptance.

The complete current owner records were read. They already accept the all-z supplied-order transform and explicitly leave raw-input discovery separate. The leading recorded task is a model-matched primary comparison. Section 6 supplies one qualified comparison, including an exact interface nonmatch; it does not claim exhaustive historical attribution.

The complete accepted [Woodbury audit](https://github.com/AgentSlop-Si/research/blob/2eaef05b9bbd6a9c884596179babe9cf474a8ff2/math/archive/objects/28/289facfec75c2b6fdd651a2f16b85bc2e992b26a479c1e9370bdf10fb0f313ce__289facfec75c2b6fdd65__WOODBURY_AUDIT.md) was read as text and pinned at repository commit 2eaef05b9bbd6a9c884596179babe9cf474a8ff2, Git blob d5193b826f515831b789025e66d960e10c80f466, content SHA256 289facfec75c2b6fdd651a2f16b85bc2e992b26a479c1e9370bdf10fb0f313ce. The inherited REVIEW-19 scope and later owner history were read in their current owner cells, not independently rerun. The prior finalization survey correctly refused whole-owner closure; its supplied-order evaluator is not re-presented as a new result here.

## 1. Exact contract

Work over a field K with exact equality and arithmetic. Let N>=1 and let omega in K have exact multiplicative order N. Indices are cyclic modulo N and (Zx)_j=x_(j-1). The unnormalized target is

    X_k = sum_(j=0)^(N-1) x_j omega^(kj),  0<=k<N.

Input: the complete raw vector x in K^N, the integer 0<=r<=N, and the already selected field and root. Define

    m = nnz(x),
    tau(x) = min_(z in K) nnz(x-zZx),
    A_r = {x : m<=2r} union {x : tau(x)<=r}.

The minimum is well-defined: the set of attained nonnegative integer support sizes is nonempty. The algorithm returns the exact N-vector X if and only if x belongs to A_r; otherwise it returns REJECT with a candidate pair and its verified residual support. This is a recognized promise family, not a promise that every vector is accepted for small r.

Field/root construction is outside the arithmetic bound and remains charged separately. Given omega, exact order can be verified by one O(N) running-power pass: no earlier positive power equals1 and omega^N=1. The same pass stores all N root powers for the evaluator. No factorization, discrete logarithm or root search occurs inside this entry point.

## 2. Recognition lemma, including its complete rejection proof

If m<=2r, directly transform the sparse x by m geometric progressions across output k. This costs O(N(m+1))<=O(N(r+1)) and certifies membership in the first part of A_r. It need not assert that tau(x)<=r.

Otherwise m>2r. Form a stream of exactly m pairs

    (u_j,v_j)=(x_j,x_(j-1)) for those j with v_j!=0.

These represent ratios u_j/v_j without division. Two pairs (u,v),(a,b) represent the same field element precisely when ub=av. All denominators are nonzero, so this is an equivalence relation. Run the standard majority-cancellation algorithm on these equivalence classes: retain a pair and counter, replace it when the counter is zero, increment for equality and decrement for inequality.

**Majority invariant.** After each prefix, its entries can be partitioned into disjoint pairs of unequal classes and a collection of copies of the current candidate whose size is the counter. Each cancellation removes at most one copy of any fixed class. Consequently a class that occurs in strictly more than half the complete stream cannot disappear; the final candidate represents it. This proves the exact equality-only majority property needed here, without relying on a probabilistic or numeric comparison.

If a scalar z has nnz(x-zZx)<=r, at most r of the m eligible pairs fail u_j=zv_j. Thus at least m-r>m/2 pairs represent z, and the candidate (a,b) must have a/b=z. In particular at most one such z exists when m>2r. This establishes completeness of candidate selection, including zeros in x.

Now compute and scan the entire homogeneous residual

    d_j = b x_j-a x_(j-1).

Its support is exactly that of x-(a/b)Zx because b!=0. Accept this branch only when t=nnz(d)<=r. This all-coordinate verification, including locations whose predecessor is zero, establishes soundness. Candidate frequency alone is insufficient.

If t>r, there can be no other admissible z: any such z would have been the strict majority and hence equal a/b. Together with m>2r, this proves x is outside A_r. The certificate is the candidate pair, vote trace or deterministic replay, m, and the complete residual support. A verifier needs the raw x and O(N) work; the residual list alone is not asserted to be a sublinear standalone certificate.

At x=0 the sparse branch returns all zeros, including r=0. At r=0 and x!=0, only an exact cyclic geometric recurrence can pass. At z=0, the promise itself implies m<=r, so the sparse branch handles it. No division by a possibly zero x entry occurs.

## 3. Exact evaluation after recognition

For an accepted candidate, Fourier covariance gives

    (b-a omega^k) X_k = D_k,
    D_k = sum_(j in supp(d)) d_j omega^(kj).

The coefficients d_j and their support were already prepared and verified in O(N). For each supported j, start at d_j and repeatedly multiply by the stored omega^j; accumulating all N contributions costs O(Nt). Prepare every q_k=b-a omega^k in O(N).

If a=0, all q_k=b!=0. Otherwise exact root order implies at most one q_k vanishes. Batch-invert only the regular denominators: store their prefix products, invert the final nonzero product once, and sweep backwards. This uses O(N) multiplications and at most one inversion. Return X_k=D_k/q_k at every regular index.

At a zero denominator k*, compute the original one-bin sum directly from x using the running step omega^k*. This costs O(N). It restores the homogeneous component even when d=0. No claim that a general permuted character is a single Fourier character is used. If N=1, the sole bin can be resonant and the regular list empty; the direct sum returns x_0 and no inversion is needed.

The algebra proves every accepted output correct, for all lengths and fields satisfying the contract. The finite tests below are controls, not this proof.

## 4. Complete cost and implementation scope

The work paid by this entry point is:

- O(N) raw-input reading, validation and nonzero scan
- O(N) root-order verification and generation/storage of all powers
- O(N) division-free majority voting and full residual verification
- O(Nm)<=O(Nr) sparse-direct output, or O(Nt)<=O(Nr) residual numerator output
- O(N) denominator generation, batch inversion bookkeeping and output multiplication
- At most one field inversion and one O(N) direct resonant bin
- N materialized outputs and O(N) field/index words; O(log N)-bit indices

Recognition/rejection itself is O(N); rejected inputs never launch dense Fourier work. Combining rejection with an ordinary FFT is optional and would restore its usual worst-case cost, not improve it.

The newly authored prime-field reference uses canonical integer residues and a trusted prime p. It verifies the supplied root in O(N), uses no sorting or hashing, and counts the arithmetic in the entry point. A deliberately conservative bound is multiplications<=N(2r+14), additions/subtractions<=N(2r+4), field equalities<=7N and inversions<=1. The sparse branch uses Nm multiplications and additions, plus root setup. In the recurrence branch, numerator work is Nt; root/vote/residual/denominator/prefix/backward/resonance multiplication contributions are bounded respectively by N,2N,2N,N,N,3N,2N. The addition and equality bounds follow by counting the corresponding linear scans. Encoding/type/range checks and index operations are additional O(N) work.

Python's modular inverse is treated as the separately counted field inversion. Its bit cost is not constant when p grows. Reading oversized or noncanonical encodings, primality proofs, field construction, root finding, extension-field arithmetic, and complex numerical conditioning are not hidden inside the field-operation count. In a prime-field family with primitive Nth roots, p>=N+1 and explicit output still uses Omega(N log N) bits. No numerical tolerance is substituted for exact equality; near-ratio/near-resonance stability remains unproved.

This fresh reference is a bounded research implementation with proved arithmetic flow and finite exact regression. It is not an acceptance of the archived uploaded routine or a production integration claim.

## 5. Exact relation to the original owner and negative controls

The accepted ALG-063 theorem gives, for x_(L[t])=z^t and s changed cyclic successor edges,

    nnz((I-zZ)x)<=2s+1,

improved to 2s when z^N=1. Therefore this new raw-vector entry point, with r=min(N,2s+1), accepts every such x without being given L or z and preserves O(N(s+1)) exact-field work. In the resonant subclass, the sharper supplied cap r=min(N,2s) also works. This is an existence-based coverage corollary: a user choosing a smaller cap can receive a justified rejection, and the algorithm neither discovers s nor reconstructs L. A scalar-normalized recurrence is broader than the original exact permutation family.

The extension is strict. Over F17, the length 8 vector (2,2,2,2,2,2,2,2) passes r=0 with z=1, yet cannot be a permutation of (1,z,...,z^7) for any z because it contains no 1. Thus acceptance must not be labeled certification of an original geometric order.

Full verification is necessary even after a successful majority vote. In F17 with N=8 and r=1, x=(1,1,1,1,1,2,2,2) has ratio 1 six times among eight eligible edges. Its cyclic residual for z=1 has support{0,5}, so it must reject. Every z other than 1 fails on at least those six matching edges. This is a precise negative certificate against using the majority alone as the acceptance test.

For homogeneous resonance, x=(3,...,3) in F17 at N=8,r=0 has zero residual but Fourier output (7,0,...,0). Setting the missing bin to zero would fail. The direct bin is indispensable.

## 6. Primary-source hypothesis/formula/cost comparison

**Classical recognition component.** The author-maintained [Boyer–Moore majority page](https://www.cs.utexas.edu/~moore/best-ideas/mjrty/index.html) and its [complete algorithm example](https://www.cs.utexas.edu/~moore/best-ideas/mjrty/example.html) give the candidate/counter equality-only scan and explicitly require another pass if majority existence is not known. Its prerequisite maps here to m-r>m/2; ratio classes are compared by cross multiplication. Our residual pass checks the stronger cyclic recurrence property, including zero-predecessor positions. No new majority algorithm is claimed. The linked 1991 chapter has garbled text extraction; this comparison relies on the readable author pages and the full proof above, not an unverified chapter transcription.

**Prony/rational generating functions.** The inspected [van der Hoeven–Lecerf version of 2 May 2024, section 5, Algorithm 4](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf) takes a polynomial-evaluation blackbox with degree and term bounds. It obtains geometric samples, a rational generating function via Padé, its roots, exponent discrete logarithms and coefficients. The paper charges Padé/coefficient recovery O(M_K(T)log T) in its bit-cost notation (section 1.1), distinct from our field-operation ledger; field/root and logarithm work have additional hypotheses and costs in sections 5.1–5.3. Our input is all N coefficients of x; our output is all N evaluations. For f(U)=sum x_j U^j, a small twisted residual does not imply small term count: x=(1,...,1) has tau=0 but f has N terms. Alternatively, after detecting a/b the sparse residual polynomial has <=r known coefficients and positions; interpolation would recover information already read. Thus Algorithm 4 is a classical mechanism comparison, not a theorem supplying our raw-recognition/all-output contract. No relative-speed claim follows between these different interfaces.

Our own cyclic formula makes the distinction explicit. Put f(U)=sum x_j U^j and h(U)=sum d_j U^j. Direct coefficient comparison gives

    (b-aU) f(U) = h(U) + a x_(N-1)(1-U^N).

On U=omega^k the boundary term vanishes. These are values of a quotient-ring identity with one possible singular evaluation. By contrast the Prony generating function sums geometric sample moments as an ordinary formal rational series. Neither the named primary source nor the common word “rational” removes the raw-data, exponent, all-coordinate or resonance obligations. The named comparison is complete at this qualified interface boundary; worldwide attribution and a broader exact-match search are not declared complete.

## 7. Fresh controls and proposed disposition

The fresh reference and independently formulated dense oracle were run once, using only new code in this packet. 14,909 valid cases and 8 malformed cases passed:

- 13,316 exhaustive raw-vector/threshold cases over F2,N1; F3,N2; F5,N4; F7,N3; F13,N3, with brute-force testing of every possible z
- 1,386 original-geometric inclusion cases at N8,12,16,32,64, with no L or z passed into the new entry point
- 180 randomized raw cases, 24 piecewise-geometric cases and 3 named controls
- 8,498 sparse-direct successes, 1,231 residual successes, 5,180 exact rejections
- 829 resonant successes and 322 zero-residual successes
- Counter bounds and at-most-one-inversion checks in every valid case

The deterministic ordered-case digest is b130fb75b91c0adcc046f9e64c352b0b43dab49cd663595182251465f4b05a61. Exact examples and counters are in CHECK_RESULTS.json. Independent review remains separate from this author-run result.

After independent acceptance, append a dated bounded-recognition and qualified-comparison supplement to the existing owners, preserving all history. Do not change the stable ID, priority 42, novelty band, main status, discovery count, or original executor claim. Record that supplied L/z are unnecessary for this recognized sparse-residual union, while exact original-order discovery, historical-source implementation repair, uniform setup, bit/precision analysis and worldwide priority remain distinct. No fresh arbitrary-input exact all-output FFT theorem is supplied.
