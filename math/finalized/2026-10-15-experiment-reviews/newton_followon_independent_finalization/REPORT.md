# Independent finalization of three Newton follow-on packets

15 October 2026. This review is local and ancillary. It does not replace, resolve, or change the user's exact Mersenne `p^d` route. No external files, repositories, tables, or services were changed. The three source directories were left unchanged; their original manifests all verify.

## Final decisions

| Packet | Final decision | Accepted result | Qualification or correction |
|---|---|---|---|
| `block_carried_newton_tree` | **ACCEPT, scoped; storage implementation qualification repaired** | Exact compact affine blocks, carry scan, complete-period symbolic shift, and the elementary width/work tradeoff | Its displayed linear live-storage schedule is attainable. The original code nevertheless materializes all interval endpoints; the supplied equivalent generator removes that avoidable control-storage term. |
| `valuation_adaptive_newton` | **ACCEPT, scoped** | Correct valuation-pruned scalar LOW producer, integral-weight criterion, paid outer specialization/high repair, and adverse independent-sample width families | The all-length recursive closure is a mathematical construction, not an executed recursive native backend. No faster multiplier or universal obstruction follows. |
| `precision_adaptive_channels` | **ACCEPT mathematical circuits; CORRECTION required for the literal elementary invoice, supplied and verified** | Correct per-coordinate CRT stopping/prefix schedule and even-step guarded scalar functional | Original arithmetic does not implement the claimed short-by-long operation costs. A separately saved repaired producer scans the shorter multiplier and uses linear bit extraction/quotient packing. Its mathematical outputs, prime schedule, and native-child histograms agree. |

No packet passes the proposed fast-multiplication/native-potential admission. No historical novelty or publishability conclusion is made. The mathematical acceptance below concerns the stated identities, specified algorithms, scoped complexity statements, and finite tests; it is not proof-assistant certification.

## 1. Source identity and independent evidence

`SOURCE_SNAPSHOT.json` records every original file's size and SHA-256 before testing. `SOURCE_MANIFEST_VERIFICATION.json` verifies all three supplied manifests. Test reruns used copies under `rerun/`, so their result-writing test bodies did not alter originals.

All three original test programs completed with exit status zero:

- Block: 1,000 scalar products; 1,000 divisions; 504 descriptor identities; 63 associativity checks; 1,424 full products; 630 period-shift comparison pairs; 2,000 chunk-carry checks; 1,904 sparse-band columns; six width witnesses; four negative controls.
- Valuation: 5,220 exhaustive LOW products; 864 progression LOW products; 420 adaptive LOW products; 540 periodic LOW/high/checksum products; 19 actually skipped outer pairs; 37,696 odd-step integral weights; 1,155 increasing-valuation weights; 512 arbitrary-length algebra controls. The reported 483 guarded and 315 tail-pruned cases reproduce.
- Precision: 1,000 elementary comparisons; 77 adaptive LOW products; 511 coefficient/bound comparisons; 15 full products; 84 guarded scalar products; 21 reachable binary aliases; the odd-CRT alias and structural checks.

`independent_checks.py` adds genuinely separate controls:

- 23,389 periodic output-capacity inequalities;
- 1,000 arbitrary unequal block-partition products;
- 1,248 complete-period symbolic shifts at arbitrary starting phases, including two periods;
- 1,200 adaptive-radix products checked against a separately assembled rational Lagrange scalar value, including 707 negative-guard cases and 57 skipped sample requests;
- 8,654 further shared-valuation integral weights;
- 123,792 exhaustive high-prefix/checksum reconstructions over all inputs and all permitted cuts for binary lengths two through seven;
- 100 precision-adaptive products whose Newton coefficients are checked by monomial polynomial multiplication followed by independent monic triangular basis elimination. This oracle does not reuse the packet's overlap-identity coefficient formula or NTT interpolation.

All passed. The independent results and seeds are preserved in `INDEPENDENT_RESULTS.json` and `INDEPENDENT_OUTPUT.txt`.

Additional repair verification passed 600 block products with exactly matching arithmetic ledgers; 9,000 signed primitive arithmetic comparisons; and all 11 representative precision schedules/histograms, unchanged except primitive work counters. The repaired precision producer also passed the entire original precision suite.

## 2. Block-carried tree: why the accepted claims hold

### Affine operator and canonical normalization

For a low interval `[l,m)` followed in composition by high interval `[m,u)`, execution is high first. Substitution into `P V + H B` gives exactly

`(P_l,H_l) o (P_h,H_h) = (P_l P_h, H_l + P_l H_h)`.

The mixed-radix interval value satisfies `0 <= H < P`. No commutation of the `H` components is valid or needed. A balanced descriptor tree reduces dependency depth but does not eliminate the products needed to obtain the descriptor.

For a digit cell, the invariant `0 <= c <= P+H-1` implies

`P v_i + H beta_i + c <= (P+H)b_i-1`,

so division by `b_i` yields the same carry bound at the next cell. Summing the weighted cell equalities telescopes to the required integer `P V + H B`. Thus canonical uniqueness proves equivalence to stagewise normalization; it does not identify intermediate signed symbolic coordinates with the block's scalar coordinates.

The periodic output capacity is valid because, after extracting full periods, any cyclic segment of a fixed length contains a subset of radices whose product is at least the product of that many smallest radices. Hence `W_(s+t) >= W_s W_t`. Also each processed suffix satisfies `A = A_low + W_j V`, so `V <= A`. The extra output cell and final carry checks are a legitimate capacity certificate.

### Chunk carry composition and the full-period exception

For chunk radix product `R`, local values `X,Y`, and `K=P X+H Y`, telescoping gives `R c_out + D=K+c_in`. Consecutive descriptors combine as `(K_1+R_1 K_2,R_1 R_2)`. This is a real associative carry representation, but obtaining `K` still requires its data products.

Writing `E_i(x)=product_(t<i)(x+b_t)`, periodicity gives

`product_(j=0)^(r-1)(x+b_j) E_i(x)=E_(i+r)(x)`.

The identity holds for arbitrary `i` and for any phase of the full-period product. The full-period shift optimization is therefore exact. Applying a proper-block factorial-size coefficient witness to full-period constants would be wrong; the source report correctly excludes that overreach.

For all-maximal digits, `H=P-1`, and the carry after `i` cells is `H-ceil(H/W_i)`. Its large width is a reachable canonical-input witness. It is not a lower bound on all structured carry algorithms.

### Work and storage

The original block primitives already scan the shorter multiplier and pack quotient bits once. An `h`-stage block therefore costs `O(h w^2)` per canonical cell with the stated elementary model; balanced descriptor construction costs `O(h^2 w^2)`. Summing block lengths yields the accepted `O(s(s+t)w^2)` digit-core upper bound. Paid input/output conversion and actual parameter widths remain necessary.

There is one implementation qualification. The original `multiply_digits` constructs the entire list of interval endpoint pairs before iterating backwards. With `s` digits and block length `h`, these endpoints use `Theta((s/h) log s)` control bits in an ordinary binary-index representation. That term is outside the displayed linear arithmetic-storage expression when `w,h` are fixed and `s` grows. The report says storage *can* be linear, which is correct with a generated schedule. `corrected_block_carried/producer.py` makes that schedule explicit using one descending range. No mathematical output or arithmetic ledger changed in 600 independent comparisons. This is a control-storage repair, not a speedup.

### Remaining fast interface

At the root, `H=A`, so the data operation `H B` remains the original product. Neither two descriptor integers, logarithmic tree depth, full-period shifts, nor small outgoing carry-state cardinality is an algorithm for this data product. A faster claim needs a supplied operation-level producer for that data action or the acquired carry payloads, with all widths, conversion costs, and any native recursive children included. The existing theorem is complete as an elementary construction and incomplete as a fast multiplier.

## 3. Valuation-adaptive scalar lane: accepted without a correctness repair

### Tail pruning has a short integral proof

Let `J` be the first index with `v2(E_J)>=k`. Since each `e_j` is monic over the integers, divide the true product polynomial by the monic polynomial `e_J`. The remainder is integral and has degree below `J`. It agrees with the true product at the first `J` nodes, while its value at zero differs by a multiple of `E_J`, hence by a multiple of `2^k`. This independently proves both the prefix interpolation assertion and scalar tail pruning, including non-arithmetic distinct radices.

### Nonunit denominators are handled correctly

If `L_t=2^lambda n/d` with odd `n,d`, a sample product modulo `2^(k-lambda)` determines its weighted term modulo `2^k`. A common lift by `2^h`, where `h=max(0,-min lambda)`, converts all terms to integral 2-adic residues. The accumulated representative modulo `2^(k+h)` is divisible by `2^h`, because the scalar interpolant is an ordinary integer. The final shift is exact. Terms with `lambda>=k` vanish and may be omitted. The code's signed-magnitude truncation followed by sign restoration is congruentially valid.

The guard is sufficient termwise. It is not claimed optimal against all correlated decoders. Repeated nodes are outside this interpolation contract; a confluent replacement has not been supplied.

### Integral weights and adaptive valuations

For a progression with `v2(p)>=v2(g)`, cancel the common power of two and write the target as `-p0/g0` with odd `g0`. The cardinal polynomial

`binom(z,t) binom(J-1-z,J-1-t)`

is integer-valued on nonnegative integers, using the usual polynomial/generalized interpretation of binomial coefficients for the second factor. Approximate `-p0/g0` by nonnegative integers modulo arbitrarily high powers of two. Continuity of this fixed rational polynomial establishes integrality of each weight. This elementary argument suffices; no uninspected stronger interpolation theorem is required.

For strictly increasing radix valuations `s_t`, each denominator difference has valuation `min(s_u,s_t)`, yielding exactly `lambda_t=sum_(u>t)(s_u-s_t)`. For `p=g=2^s`, direct cancellation yields `L_t=(-1)^t binom(J,t+1)`. Both formulas agree with the independent controls.

### Outer specialization and high repair

The scalar identity `XY=sum_(i,j)Q^(i+j)X_iY_j` is exact before any transform. A pair can be omitted precisely under the stated sufficient condition `(i+j)v2(Q)>=k`; every retained local precision and outer scaling is paid. This is a valid alternative scalar compiler. It is not permission to omit boundary maps inside a different generic-frequency quotient compiler.

For `t=a+1`, truncating each input to its first `t` bits creates a scaled-product error strictly below one at the high-quotient cut. Therefore `H <= floor(XY/2^k) <= H+1`. Since `2^k` is a unit modulo three, the original-input checksum identifies the remaining bit. The prefix product and input scans remain separate paid operations. Exhaustive controls cover all cuts for small lengths.

### Adverse families and exact scope

The odd-step near-Mersenne family is sound: its sample operands stay odd with exactly `m` magnitude bits, required precisions exceed their full product widths, and tail pruning does not occur. The independent extension verifies these claims through `r=1024`, with exact input capacity and exact samples, in `ADVERSE_FAMILY_EXTENSION.json`. The finite potential ratios stay above one. Their limit is established by the displayed asymptotic calculation, not by numerical extrapolation: the optimistic ordinary-root comparison tends to `2^(1-beta)>1` for the pinned beta.

The scaled family genuinely prunes high channels, but its surviving sample widths grow to input scale. The native-wrapper noncontraction counterexamples therefore coexist with real pruning. Neither implies an impossibility theorem for all adaptive nodes or correlated/shared producers.

The all-length dispatcher is a mathematically specified recursive closure with elementary fallback. The supplied code checks its LOW/high algebra, using a different finite test parameter choice, and does not execute that complete native recursion. This distinction must remain explicit in any finalized description. No missing correctness lemma was found for the stated recurrence construction; the missing *fast* result is a paid shrinking-child invoice with target-compatible total overhead. The existing preparation and sampling upper bounds do not supply it.

## 4. Precision-adaptive channels: mathematical acceptance and concrete invoice correction

### Correctness and finite savings

The basis product identity gives the stated coordinate height bounds. The geometric bound and tent sum are valid. A prefix of samples determines a prefix of Newton coefficients, and the factorial convolution implements that relation over each certified field. The selected primes exceed all relevant factorial indices and do not divide `g`. Exact root order follows from the power-of-two order test.

Per-coordinate CRT accumulators contain residues modulo every prime used before that coordinate stops. The condition `P>2^(h_j+1)` is sufficient for unique signed reconstruction. Later primes need only the maximum active prefix; stopping a coordinate does not invalidate any still-active accumulator.

The finite `r=8,p=7,g=4` example reproduces the 713 versus 1,155 coordinate-capacity total and 3,840 online butterflies. These are coordinate-storage/operation counts, not whole-program memory or timing gains. The recorded illustrative row asks for `k=17`; it should not be represented as a full-product timing experiment. Full-product correctness is separately tested.

The elementary existence argument for arbitrarily many eligible primes is valid for power-of-two transform lengths. It proves termination, not fast prime/root discovery. Trial division and exhaustive root search remain in the cost.

### Required primitive correction

The source's `Arithmetic.divmod` does both `q <<= 1` and `(a >> j) & 1` on every bit. With an `N`-bit dividend and a fixed small divisor, these are successively growing quotient and input copies. Their total materialized integer-bit volume is quadratic in `N`. Its counter only charges the bounded-width remainder comparison. Thus the literal routine does not support the claimed `O(N w)` short-divisor cost. This matters for binary input conversion and reductions of growing CRT accumulators.

The source's `Arithmetic.mul(a,b)` scans all bits of `b` without swapping. In final scalar Horner it is called as `mul(radix,z)`. When the radix is small and `z` has `k` bits, the routine performs `k` shifts of growing values, giving the schoolbook upper bound `O(k(k+v))`, not the stated `O(kv)` short-factor bound. The field-only `w`-by-`w` upper bound remains quadratic either way.

These are invoice/implementation mismatches, not output errors. They cannot be removed merely by calling a Python implementation an abstract bit model; the model schedule must specify the efficient primitives.

`corrected_precision_channels/producer.py` supplies that schedule:

1. Swap product magnitudes so the bit loop scans the shorter operand. Signed semantics and wrapper widths are unchanged.
2. Extract input bits once through bytes, append quotient bits once, and pack the quotient once. Only the bounded-width remainder is shifted during long division. Include linear extraction/packing movement and the signed Euclidean adjustment.

The repaired producer passes the entire original suite and 9,000 independent signed arithmetic comparisons. All 11 representative mathematical records, NTT/CRT schedules, and native-wrapper histograms agree exactly with the original; only primitive work counters differ. With these repairs, the displayed parameterized elementary cost envelope is justified by the specified primitives. It remains an unfavorable cost envelope, including cold setup and output.

If the original code is retained unchanged, replace its short-by-long division and multiplication costs by the corresponding larger schedule bounds rather than claiming this repaired invoice.

### Guard and alias claims

For odd `p` and even `g`, the Lagrange numerator is odd, so the denominator valuation and requested `K_t` are exact for this termwise decoder. Common lifting, odd inversion, accumulation, and one final exact shift are correct. The binomial-valuation spread is only logarithmic.

The reachable product `e_h^2` has all sampled values divisible by the stated `2^G`, but its scalar value is odd. The resulting common-precision lower obstruction is valid for a decoder restricted to that sampled transcript. The gap `v2 binom(2h,h)=popcount(h)` is exact. This does not make each individual sample precision optimal and does not constrain access to the original input bits.

Likewise, the `17*97` constant-digit alias shows that a sufficiently large *odd* CRT modulus alone does not specify a binary low word without a range or error certificate. It is a transcript-interface obstruction, not a raw-input multiplication lower bound.

### Native gate scope

The asymptotic failed potential in the report charges every conventional field slot a full-width generic wrapper. That declared invoice fails. It must not be promoted to an asymptotic lower bound for the actual operand-width histogram after special constants, zero-skipping, shared work, or another backend. The report already limits its claim in this way, and this review retains that limit. The finite measured histogram also fails contraction/potential, but finite rows alone do not establish the asymptotic actual-histogram statement.

A fast successor needs a real cheaper scalar/product or transform circuit with a complete operation/child-width invoice, including CRT or its replacement, precision guards, setup, and binary endpoints. No such missing lemma is supplied by the current packet.

## 5. Reproduction and deliverables

From the workspace root:

- `python newton_followon_independent_finalization/independent_checks.py`
- `python newton_followon_independent_finalization/corrected_precision_channels/test_precision.py`
- `python newton_followon_independent_finalization/verify_repairs.py`

Original-suite reruns and their output are preserved under `rerun/` and the three `*_rerun.txt` files. The block test uses a working-directory-relative output path, so rerun it from `newton_followon_independent_finalization/rerun/` as originally recorded. The optional adverse-family extension contains very large exact capacities and is slower than the ordinary checks.

`VERDICTS.json` is the concise machine-readable finalization. `MANIFEST.sha256.json` seals this finalization packet. Original sources remain immutable. Corrected producers are separate artifacts and do not silently replace the submitted versions.
