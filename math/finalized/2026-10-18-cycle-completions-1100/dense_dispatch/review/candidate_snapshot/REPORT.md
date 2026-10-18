# Target-explicit dense dispatch and complete fallback costs

18 October 2026 UTC. Author-verified candidate; independent review pending.

## Result

A source-aware, fail-closed dense fallback is now constructive. The new reference receives the actual exact original vector, recognizes the dense boundary before coefficient setup, distinguishes the original first-transform target from the supplier's second-transform target, certifies every coefficient of a direct unitary DFT, checks every exact accumulation prefix, rounds once per row, and returns all N coordinates with exact scale-back. A separate branch materializes exact reversal for the singleton second-transform target. Both branches pay source reading, normalization, numerical preparation, every output and all replay/export operations.

This is a standard direct DFT and a standard reversal identity. Neither is a new fast Fourier algorithm. The contribution is the explicit source/target dispatch contract and complete accounting around the formerly missing fallback. The current accepted sparse supplier/recovery and outer stream still do not constitute a common source-bound fast branch. Consequently the actual reference routes every supported FIRST_DFT request to the direct evaluator; its honest worst-case cost is quadratic in the number of coordinates, times the stated precision overhead. This closes a bounded dense-reference/dispatch gate, not ALG-034, a general-block algorithm, or the missing sparse composition.

## 1. Source-bound dependencies and the target distinction

The exact retrieved source files and immutable repository links are in SOURCE_BINDINGS.json. They were read as text; no predecessor test suite or implementation was run.

The accepted sparse supplier at singleton B_A=N has original x_j=c_j 2^-F, E=sum |c_j|^2, h=ceil(log2 sqrt(E)), alpha=2^(h-F), and supplies f=U_N x/alpha. Its accepted value-only recovery produces an approximation to U_N f=R_N x/alpha. It does not produce an approximation to U_N x. The recovery theorem is restricted to N=2^28, nonzero support at most 16, and its declared finite BUCKETS interface. The target difference is already substantive at N=4: U_4 delta_1=(1,-i,-1,i)/2, whereas R_4 delta_1=delta_3. Their squared l2 distance is exactly 2. Substituting one target for the other is not an error-budget adjustment.

The accepted outer stage instead consumes approximations to U_M J_N u, where J_N is its prescribed centered embedding and M is the least power of two at least 4N. Its conditional final target is U_N u. The median context alone supplies no such original u. No target label or digest can establish that missing mathematical relation.

The new reference therefore uses these separate tags:

- FIRST_DFT: return an approximation to U_N x for the actual supplied original x. In ALG-034's singleton family this is U_N P(x), since P=I. No general P is implemented.
- SINGLETON_SECOND_NORMALIZED: with explicit B_A=N, return exactly R_N x/alpha, the actual target of the accepted recovery. The output is normalized. The returned alpha exponent does not claim that scale-back to the original magnitude has been materialized.

Applying this reference to a generic outer source u means supplying u itself as the original for FIRST_DFT. The program accepts no arbitrary callback, sparse result, owner claim, or alleged centering certificate in its place. A general-block B_A unequal to N is rejected. The separate centering-composition investigation owns any stronger incompatibility theorem; none is needed to justify this interface discipline.

## 2. Exact input, recognition, output and trust boundary

Input has exactly N, F, kind and data. Here N>=1 and F are exact built-in integers. Dense data has N Cartesian integer pairs, all visited; an immutable equivalent original is retained through N, F and its nonzero tuples. Sparse data has sorted distinct triples (j,Re c_j,Im c_j), with omitted coordinates exactly zero. Sparse zero entries are prohibited. At least one nonzero component must be odd, and an all-zero input must have F=0. This canonical common-grid rule is checked against the original entries, never inferred from a recovered support list. Float, boolean, subclass, duplicate and malformed coordinate coercions are not allowed. The exact dictionary length is checked before iterating or constructing a key set; at most four exact-string keys are then inspected. Oversized malformed dictionaries therefore cannot trigger an uncharged unbounded key scan. Before a metadata/component limit, exact-int bit_length is used directly, without abs copying a rejected negative integer. The computed width integers are themselves charged before the rejection test; later absolute-value operations occur only after the relevant widths have been admitted.

A sparse input is an exact supplied representation, not a claim to have read an unknown dense vector. On dense input the recognition cost includes all N visits even if almost all entries are zero. Successful parsing returns an immutable copied source. The original representation is included in replay equality. Trusted exact Python/standard-library semantics and no hostile runtime mutation are assumed; this is caller-relative mathematical binding, not external origin authentication or historical attestation.

The output consists of an actual N-tuple of integer pairs and one nonnegative denominator exponent e, denoting (a_k+i b_k)2^-e. Every row, including zero rows, is written. A large positive exponent e is stored as an exponent, not as a physical integer denominator 2^e. If exact scale-back would require a negative e, the numerators must really be left-shifted; their expanded widths and output storage are charged. The reference checks its physical shift limit before coefficient generation or N-output allocation. A huge scale exponent with a short encoding is not a license for a free huge numerator.

`verify` recomputes the entire result from independently supplied original data and compares it with the complete result object using a type-strict expected-tree traversal. Exact Result, Source, tuple, string, integer and boolean types are required. Tuple/string lengths are checked before traversal/equality and exact integer bit lengths before content equality. Supplied equality hooks are never called; a result subclass or an integer subclass cannot self-certify. Each comparison node and admitted scalar comparison is charged, and the trusted recomputed shape bounds the traversal even for an oversized malformed result. A changed source, scale, target or final coordinate fails. Production, the fresh replay, the comparison and each export have separate receipts. If comparison exhausts its cap or the supplied exact dataclass lacks required fields, Rejected retains the completed replay receipt in prior_receipts and the terminal comparison prefix in receipt. Add those once each for the failed verification call; add the original production receipt separately when accounting for production plus verification. A rejection during replay has no completed replay receipt and retains its own terminal prefix. A copied hash is never a substitute for replay. Mutating a caller's source list after execution cannot change the copied source.

## 3. Exact structural dense recognition

For the outer parameters put

    M=2^m=nextpow2(4N),  t=32Dm+4,  D>=5.

The existing sparse incidence proof requires t<M. The new planner evaluates this inequality exactly before any numerical setup. It also reports the historical recovery source-domain predicate, including actual source support. That predicate is expressly not a same-target sparse-provider binding. At N=2^28, sources with 16 and 17 nonzeros are distinguished, but neither is treated as a centered-source certificate. No repeated old incidence test is used as new evidence.

There are two different reasons to use the dense fallback:

1. Structural dense boundary: t>=M.
2. Missing or unsupported same-target fast provider, even when t<M.

Only the first reason is a finite exception for each fixed D. To make this quantitative, let ell=ceil(log2(64D)) and m0=2ell. Since ell<=64D-1,

    2^m0 >= (64D)^2 > 64D ell+4 = 32D m0+4.

The ratio (32Dm+4)/2^m decreases for m>=2, so all m>=m0 pass the sparse guard. A failed guard has m<m0, and hence N<4096D^2, a deliberately loose explicit bound. Under fixed D and a fixed family with r, W, scale magnitude and parameter encoding O(log(N+1)), any finite-polynomial direct fallback cost on this structural region is O_D(N), with potentially enormous constants. This is absorption of a finite exception, not a fast direct DFT or a useful crossover.

This conclusion is not uniform in D. Choosing D>=ceil((2^m-4)/(32m)) forces a dense guard at arbitrarily large m. Fresh allocation-free source plans exercise this at lengths through 2^60. Nor does the finite-exception argument apply to reason 2: a missing fast provider can force fallback at arbitrarily large N even with D=5. The current reference has no admitted same-target sparse provider, so its general FIRST_DFT cost retains the direct-transform term.

## 4. Constructive direct fallback and error theorem

For nonzero input let u=c/2^h. Exact energy arithmetic gives

    1/2 < ||u||_2 <= 1,   x=2^(h-F)u.

For N>=2 set m=ceil(log2 N), requested r>=0, q=b=r+m+4, and working coefficient grid g=q+8. Construct N approximate unitary coefficients

    w_j = N^-1/2 exp(-2 pi i j/N),
    wtilde_j=(A_j+i B_j)2^-g,   |wtilde_j-w_j| <= 2^-q.

These coefficients are not supplied by an oracle. Section 5 specifies and pays their entire construction.

For each k, sum exactly over all represented nonzero originals:

    S_k = sum_j (Re c_j+i Im c_j)(A_(jk mod N)+i B_(jk mod N)).

Products and every partial sum are exact signed integers. Round each Cartesian component of S_k/2^(h+g) once to the grid 2^-b by signed nearest-ties-to-even. Then scale by exactly 2^(h-F), changing the common denominator exponent or physically shifting numerators as required.

**Dense error theorem.** The mathematical construction terminates for every finite represented input and r, and returns all N finite dyadic outputs Y satisfying

    ||Y-U_N x||_2 <= (3/16) 2^-r ||x||_2 <= 2^-r ||x||_2.

The final inequality is strict for nonzero input. For N=1 the output is an exact copy; zero input produces exactly N zeros with no coefficient setup.

Proof. Each normalized coordinate has coefficient perturbation at most 2^-q ||u||_1 <=2^-q sqrt(N)||u||_2. Across N outputs this gives at most N2^-q||u||_2 <=2^-r||u||_2/16. Cartesian nearest rounding has complex error at most 2^-b, so its vector contribution is at most sqrt(N)2^-b <=2^-r/16 <2^-r||u||_2/8. Add the bounds and scale exactly. No cancellation assumption or random success event is used.

**Every-prefix width.** If each raw Cartesian component has magnitude below 2^W, the certified coefficient numerators have magnitude below 2^(g+1). A Cartesian product contribution has magnitude below 2^(W+g+2), so every prefix containing at most N terms has magnitude below 2^(W+g+m+2). A signed allocation of W+g+m+4 bits suffices. The implementation checks this at every update. A later cancellation cannot hide an earlier range violation. Python integers do not wrap.

This is normwise relative accuracy against represented input. There is no per-coordinate relative error, correct-rounding, rounded-serial-equivalence, fixed-hardware or speed claim.

## 5. Entire coefficient preparation, with exact certificates

Production uses Fraction, integer arithmetic and isqrt only. No floating number, transcendental library, inherited research module, network operation or downloaded code is used.

1. Enclose pi by Machin's identity pi=16 atan(1/5)-4 atan(1/239), using g+10 terms of each exact alternating rational series and its next-term remainder. Convert the enclosure outwards to the dyadic grid 2^-(g+16). This paid reduction keeps large rational pi denominators out of every later power.
2. For the signed residue a congruent to j with |a|<=N/2, let x=(2a/N) times the midpoint pi. Then |x|<4. The true angle differs by at most (2|a|/N) times the pi radius.
3. Compute the real and imaginary parts of the complex exponential Taylor polynomial of degree K=g+40 using exact rational term recurrence. Each Cartesian remainder is at most 4^(K+1)/(K+1)!, plus the angle uncertainty by the derivative bound for sine/cosine. The imaginary component is negated for the negative DFT sign.
4. Enclose N^-1/2 on the 2^-g grid. With A=floor(sqrt(floor(2^(2g)/N))), the lower endpoint A/2^g is valid. The upper endpoint is equal on exact equality, otherwise (A+1)/2^g. Exact square comparisons certify both endpoints.
5. Multiply the root and normalization intervals outwards using exact rationals, select the nearest g-grid point to each interval midpoint, and check the exact squared sum of the maximum Cartesian endpoint distances against 2^-2q. Only a passing complex-radius certificate is returned. Check the Cartesian numerator range as well.

The Machin identity follows exactly from tan(2 atan(1/5))=5/12, tan(4 atan(1/5))=120/119, and tan(4 atan(1/5)-atan(1/239))=1, with the angle in (0,pi/2). No experimental pi value is its premise.

These checks cannot fail for the uncapped construction. The alternating pi interval has width below 2^-(4g+37). After outward dyadic reduction its radius is below 2^-(g+15). Since K=g+40 and (K+1)!>=16^(K+1-16), the Taylor remainder is at most 2^(62-2K)=2^(-2g-18). Thus each phase enclosure has midpoint error below 2^-(g+14). The reciprocal-square-root interval has width at most 2^-g and lies in [0,1]. Each final Cartesian endpoint distance from the chosen rounded point is below 2*2^-g. Its complex radius is therefore below 3*2^-g<2^-q. The stored range bound follows from |w_j|<=1 and error below 1.

The finite reference additionally enforces explicit resource ceilings; a resource or grammar rejection returns a typed paid prefix and no successful answer. The mathematical termination statement does not mean that a finite resource cap admits arbitrary N or precision.

## 6. Complete costs, storage, output expansion and exceptions

Use a sequential binary arithmetic/control model with ordinary schoolbook integer multiplication, division, gcd and integer square root; each can be upper-bounded by a cubic polynomial in its operand bit width. These are logical upper bounds, not Python instruction counts or measured performance.

Let s be the actual original support, W the maximum raw component width, f the bit length of F, d_enc the bit length of D, and

    L=2+r+ceil(log2(N+1))+W+f+d_enc,
    J=max(0,h-F-b) for N>=2; J=max(0,-F) for the exact N=1 copy.

J is the number of physical scale-back shift bits. Metadata of short encoding can have enormous J; it cannot be discarded. An entire input scan, original retention, energy/normalization, index arithmetic, every root, all N coefficients, every exact sum, rounding, output movement and newly reached counter widths are included.

The exact rational pi series uses O(L) records with O(L^2)-bit intermediates: a common denominator can be bounded by the product of its O(L) term denominators. After dyadic reduction, an angle has O(L)-bit numerator/denominator. Each Taylor partial sum has denominator dividing an angle-denominator power times K!, hence O(L^2) bits. There are O(NL) coefficient-preparation records, so a straightforward schoolbook binary bound is O(NL^7) for this setup. It is not an O(N) table oracle.

The direct arithmetic uses Ns complex products/updates with O(L)-bit operands before scaling. Dense reading still costs N visits when s is small. All N outputs are materialized. The reference's deliberately conservative cubic per-record ledger and global bookkeeping envelope give the following safe complete production upper bound:

    T_ref = O((Ns + N(L+J+1)) (L^2+J)^3).

In particular, the arbitrary dense bound is

    O((N^2 + N(L+J+1)) (L^2+J)^3).

This bound intentionally pays more than a sharp arithmetic analysis would. It covers the numerical receipts as well as cumulative counters, addresses, validation and output-description bits. In the common J=0 case it is O(Ns L^6+NL^7). No O(N) or O(N log N) general bound is asserted for this reference.

Peak production data, including retained originals for later source comparison, coefficient table, output pairs and fixed-number large rational temporaries, is

    O(N(L+J)+L^2) bits.

The receipt's cumulative produced/control-bit bound is larger and explicitly separate from peak storage. Retaining an extra export, comparison result, trace or original caller copy adds its own actual memory. All N output writes are mandatory, even when the input and target are sparse.

For SINGLETON_SECOND_NORMALIZED, no root or Fourier table is built. The program initializes all N rows, scatters c_j to index -j mod N, and returns common denominator h. Unitarity and U_N^2=R_N prove exactness. Exact normalization and full source/output costs remain; a safe ledger bound is O((N+sL)L^3), with O(NL) peak bits. This works mathematically for any singleton original, including a dense original. It does not solve the original first-transform target, discover hidden support, or claim a faster sparse recovery method. F affects source metadata and the returned alpha exponent but does not induce a physical scale-back in this normalized branch.

One export has a separate explicit byte/work/storage receipt. The `verify` call reruns production and returns the additional replay and comparison receipts; both production receipts must be summed. Failed prefixes are retained. No table reuse, free semantic verification, forgotten historical counter, random retry, remote I/O or future export is included silently.

The shipped bounded Limits are N<=128, raw component width<=1024, metadata width<=128, r<=128, physical numerator shift<=8192, at most two million arithmetic records and a one-million-bit conservative arithmetic envelope. These are explicit engineering guards, not an all-length performance result. A larger request gets a resource rejection and its paid prefix; it is never represented as an inaccurate successful transform. Each successful result carries the certified numerical theorem. The universal construction and the bounded reference's success domain are deliberately distinguished.

## 7. What a future mixed dispatcher is allowed to claim

A valid same-target sparse branch must establish its source binding and target equation in code/proof, its numerical success/failure statement for each fixed source and independent tape, and an all-tape resource budget. A caller assertion or a returned tag is insufficient. Before recognizing the sparse branch, pay input acquisition, any original-form recognition, normalization, parameter preparation and all source/context validation. An output support count cannot certify an original-source sparsity premise.

For such a separately supplied branch, the exact total is a sum of the stages actually reached:

- Pure dense path: source/recognition work plus the complete dense evaluator.
- Completed sparse path: source/recognition, supplier, measurements, recovery, any amplification, median production and replay, outer coefficients/scatter, and final scale/output work.
- Aborted sparse prefix followed by dense: every already incurred prefix plus the entire dense path. A budget guard must apply before expensive preparation/allocation if it is intended to preserve a worst-case bound.

If the sparse result has joint successful-return-and-accuracy probability at least 1-delta and the dense path is deterministic and correct for the identical target, falling back on explicit rejection cannot worsen that error probability. It does not make undetected bad sparse answers deterministic. No repeat-until-success, post-selection or free amplification is licensed. Selection depending on input is allowed under the fixed-input theorem only with fresh independently sampled tape and the stated source-specific guarantee. Every repeated measurement schedule and failed attempt remains paid.

The inherited sparse supplier's finite caps and its single recovery length do not furnish a uniform fast asymptotic T_sparse(N). The outer stage's every-tape coefficient error theorem does not furnish the missing supplier/centering/recovery premise. Thus the displayed mixed-dispatch accounting is a composition contract, not an assertion that the current accepted pieces satisfy it.

## 8. Fresh evidence and exact stopping point

Only the new dense_dispatch.py and fresh_checks.py were executed. CHECK_RESULTS.json records a fresh complete batch: 16 main direct-transform runs and 278 output rows, six exact-reversal runs and 126 output rows, seven allocation-free variable-D plans through N=2^60, two source-domain plans at N=2^28, 13 complete original-source replay executions (33 additional rows), five changed-source/target/answer or immutable-source checks, three strict-tree rejection probes with one additional one-row source run, 12 paid source/resource rejections, five comparison failures retaining their completed replay receipts, and a separate two-row precision-endpoint run. In total, 31 completed direct evaluations wrote 314 rows; replay and endpoint work are not hidden in the main-run count.

Fifteen direct runs have guaranteed independent rational target enclosures for every row. That oracle uses pi/4=atan(1/2)+atan(1/3), separate even/odd Horner polynomials, and an integer-bisection reciprocal-square-root enclosure. It imports no production numerical helper. All squared l2-error comparisons are exact rational inequalities. The N=128, r=128 complete endpoint run independently checks the exact constant-vector Fourier identity and a 220-bit rational enclosure of 1/sqrt(2), including every nominally zero output. Signed cancellation, a 201-bit component, non-power-of-two lengths, sparse and dense supplied originals, zero input, huge symbolic positive F, and a physically expanded scale are covered.

The enormous negative-F probe is rejected before coefficient preparation, whereas normalized exact reversal can legitimately retain the same F only in its alpha metadata. Exceeding the dense allocation guard never produces a claim to have written N outputs. Changed original coefficient/scale, changed target and changed last output fail complete source-relative replay. A lying Result subclass, a lying integer subclass and a 10,000-row supplied result tuple are rejected using fewer than 64 comparison-node visits each in their one-coordinate source context. Four comparison-cap failures at caps 12, 16, 24 and 32 preserve and sum the complete replay and comparison-prefix work/storage; a missing-field Result receives the same completed-prefix protection. Two-million-bit negative metadata/component probes reject via charged small width metadata, without a pre-limit absolute-value copy. The test times are process observations, not speed or complexity evidence.

The stopping condition is independent review of this target-explicit dispatch/cost contract and bounded certified reference. The remaining bottleneck for the intended fast ALG-034 pipeline is a genuine same-source, same-target sparse branch with the correct general/centered source, quantified recovery/amplification and full costs. General B_A, original-target composition, uniform fast all-length complexity, serial rounded equivalence and historical priority remain open. No external write occurred.
