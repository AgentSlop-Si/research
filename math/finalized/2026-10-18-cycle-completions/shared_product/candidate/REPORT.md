# Native-matrix run differences: a growing-structure theorem

18 October 2026. New lemma and executable extension, pending independent review. This is a structural extension of the accepted native-Newton/shared-product route, not a claim of novelty for finite differences, run-length encoding, or sparse convolution.

## Theorem

Let A,B be arbitrary nonzero signed integers of maximum magnitude bit length N. For sufficiently large N, set r=floor(log2 N) and take exactly the accepted native plan, with binary block width s=Theta(r^2), ordinary nodes x_0,...,x_(2r-2), and target -P. Use the complete dense legal s-bit block lists (a_i)_(0<=i<L_A), (b_j)_(0<=j<L_B), including their zero blocks. Extend each list by zero outside its index range. Let

K_A = #{ i in [0,L_A] : a_i != a_(i-1) },
K_B = #{ j in [0,L_B] : b_j != b_(j-1) },

where a_-1=a_(L_A)=b_-1=b_(L_B)=0. Thus each K is a number of value transitions, including start/end transitions, not the number of occupied blocks. Write K=K_A+K_B and M=K_A K_B.

There is a deterministic, exact implementation of the same native matrix/shared-product route whose complete recognized-branch bit cost is

O(N + r^12 + K r^4 + Q r^4 + M r^2),

where Q<=M is the number of distinct commutative products of sign-normalized jump coefficient vectors. In particular its uniform cost is

O(N + r^12 + M r^4).

The constants are independent of K_A,K_B and run lengths. Recognition from the dense inputs, conversion, exact comparisons, graph construction, all small arithmetic, source-row maxima and strict widths, cancellation, carrying, signs, dense output, and root-wide counters/log indices are included.

For every fixed C>0, accepting only when M r^4<=C N yields a complete O(N) recognized branch. K_A and K_B may grow: for example both may be O(sqrt(N)/log^2 N), with an appropriately fixed constant. The occupied support can simultaneously be Theta(N/log^2 N), including the entire legal block list. This strictly extends the input class covered by the accepted fixed-occupied-support linear theorem. It is not a lower-bound separation from the old dispatcher on these new families.

A front end that uses this branch when its exact recognition test passes and otherwise invokes the accepted dispatcher retains its arbitrary-input upper bound N exp(O(log N/loglog N)), with the erratum's root-wide accounting. No arbitrary-dense N log N bound follows.

## Essential source-preserving choice

Let c(a) be the complete canonical Newton coefficient vector of legal block a, and let f_a(x)=sum_h (-1)^h c_h(a) binom(x,h). Canonical encoding is not additive. Therefore the jump vector at i is

d_i = c(a_i)-c(a_(i-1)),

not the canonical encoding of the integer difference a_i-a_(i-1). This distinction ensures that for every native node, and indeed as a polynomial identity,

D_A(x,Y) := sum_i f_(d_i)(x) Y^i = (1-Y) F_A(x,Y),

where F_A(x,Y)=sum_i f_(a_i)(x)Y^i is exactly the original source row polynomial. The terminal transition is indispensable. All nonzero jump vectors have degree at most r-1; their entries lie in (-P,P), and their node values have O(r) bits.

## Computation and proof

1. Scan all legal blocks through bounded byte windows, recording each change and its original value. Zero gaps are scanned, and the terminal change to zero is recorded. Encode each new run value once and subtract the preceding canonical vector. There are at most K canonical conversions.
2. Normalize each nonzero jump vector by its first nonzero sign and intern equal vectors by deterministic sorting with exact comparisons. Keep its outer position and sign. Sort the M term pairs to intern their commutative leaf-product pairs and sort their signed event records by outer position. No hashing assumption is needed.
3. At all 2r-1 original nodes evaluate every distinct leaf and every distinct product once. Interpolate each product polynomial once at -P. For a jump pair i,j its result is exactly (a_i-a_(i-1))(b_j-b_(j-1)), with the recorded signs. This is shared interpolation across all output positions; columns are not independently re-interpolated.
4. Let e_k be the sum of these signed product events at outer position k. Recover ordinary convolution coefficients by two prefix sums: u_k=u_(k-1)+e_k and v_k=v_(k-1)+u_k, starting from zero. Since D_A D_B=(1-Y)^2 F_A F_B, v_k evaluated at -P is exactly sum_(i+j=k) a_i b_j. All these final coefficients are nonnegative. The two terminal zero coefficients and zero first prefix sum certify the zero tail.
5. Perform ordinary nonnegative base-2^s carrying and bounded-window dense serialization, then restore the input sign. This gives A B exactly.

The original row values at each node are obtainable by one prefix scan of the jump terms, or directly from the run values. Consequently their exact maxima A_x,B_x are available without expanding repeated positions. The source rule w_x=8 ceil(bit_length(2 L A_x B_x)/8), L=max(L_A,L_B), is retained, with width zero for a zero product row. The identity is in Y, so substitution of each distinct source packing base is valid. The method never materializes or multiplies a packed child integer.

## Complete cost details

Canonical division has a sharper bound than an arbitrary division of two s-bit integers. At weight W_h, the remaining value is below W_(h+1), so its quotient is below P. Therefore the dividend and divisor have O(r^2) bits but their bit-length difference is O(r). Explicit binary long division costs O(r^3) per weight and O(r^4) per legal block. Subtracting vectors costs O(r^2).

There are O(r) nodes and O(r) entries per vector. Their entries and row matrix values have O(r) bits. Elementary schoolbook evaluation therefore costs O(r^4) per leaf. A product requires O(r) products of O(r)-bit values. Its ordinary finite-difference table has O(r^2) entries of O(r) bits: successive differences add at most O(r) extra bits. Interpolation has O(r) weights of O(r^2) bits times O(r)-bit differences, costing O(r^4). Thus conversion/evaluation/interpolation costs O((K+Q)r^4), with the accepted O(r^12) one-time native-plan bound.

Exact leaf sorting costs O(K log(K+1) r^2)=O(Kr^3), since K<=2(L_A+L_B+2)=O(N). Pair/event sorting has M records of O(r) bits and costs O(M log(M+1) r)=O(Mr^2). Event additions cost O(Mr^2). For nonzero finite block lists K_A,K_B>=2, hence K<=M, Q<=M. These terms give the displayed uniform bound.

At every stage |e_k|<=M 2^(2s), |u_k|<=M 2^(2s), and |v_k|<=(L_A+L_B+1) M 2^(2s), even without relying on cancellation. Since M=O(N^2), all these quantities have O(r^2) bits. Actual final coefficients satisfy the sharper bound min(L_A,L_B)2^(2s). Thus the two prefix scans, carry propagation, and serialization take O((L_A+L_B)r^2)=O(N) bit work. Indices, offset arithmetic, bounded-window input extraction, and run recognition fit the same bound. No repeatedly shifted whole input/output or per-byte shifting reservoir is used.

Root-wide accounting is explicit. The inherited native plan is built in a fresh ledger before the root-size stream scans; its already accepted complete O(r^12) setup bound therefore applies without a larger earlier counter. Excluding this separately paid setup, the branch has O((K+Q)r^2+M+L_A+L_B) arithmetic/administrative events. Total charges and record counts are polynomial in N, so counters and indices have O(r) bits. A counter update or reference/index operation costs O(r), giving at most O((K+Q)r^3+Mr+(L_A+L_B)r), absorbed by the previous terms. The elementary arithmetic loops themselves are already included in their bit charges. Metadata multiplication for offsets is O(r^2) per output block and is included in O(N). Sequential byte copies are charged by their copied bit length, with block-offset metadata charged separately; no root-width counter is updated once per copied bit. Trace records are appended, never searched by a root-size linear scan. Comparisons and sorted-record movement are already charged. Therefore root-wide diagnostics do not silently add an unaccounted log N factor.

The scan/recognition and plan are performed before expensive conversions and pair construction. A rejected case costs O(N+r^12) extra and invokes the accepted dispatcher. Its known bound dominates this overhead; it retains the accepted erratum rather than assuming child-local counter widths.

## Scope and examples

- A single arbitrary nonzero legal block repeated for L_A positions and another repeated for L_B positions has K_A=K_B=2, although occupied support is unbounded and dense.
- Arbitrary piecewise-constant legal block strings with growing transition counts satisfying K_AK_B=O(N/log^4 N) have complete linear cost.
- Sparse inputs satisfy K_A<=2 t_A and K_B<=2 t_B, so the same theorem also gives a growing sparse-support regime.
- Random-looking blocks typically have K_A=Theta(L_A), K_B=Theta(L_B); the linear-budget recognizer rejects them. No general dense improvement is claimed.
- All structure is checked from arbitrary dense integer inputs. The theorem does not assume an RLE input oracle.


## Executable extension and exact checking

The new `run_shared.py` imports only the SHA-256-pinned reviewed `shared_dispatcher.py` primitive module. It does not import any prior control program or execute the historical original producer. The new code implements complete run recognition, coefficient-vector differencing, sign-normalized leaf interning, shared product/event construction, native evaluations, one interpolation per shared product, original source-row maxima, two-prefix reconstruction, and the complete budgeted front end.

The public complete multiplier is `multiply(a,b,budget_factor=64,verify=True)`. Its first branch uses the fixed linear budget M r^4 <= 64 N. A rejected input invokes the accepted dispatcher. `multiply_runs(...,budget_factor=None)` is an explicit unbudgeted experimental entry point: its parameterized bound holds, but its runtime is not automatically linear. Base thresholds and budget factors are fixed policy constants in the asymptotic statements.

The independent-form checker is enabled by default. It rescans both complete block lists, independently rebuilds the expected transitions and canonical jump vectors, validates every signed term and every required pair event, and rejects unused/missing product types. It separately reevaluates original run values to check actual maxima and strict source packing widths. It checks each interpolated target against a direct elementary product of the two decoded O(s)-bit jump leaves. These are block-sized checks, not packed-child or original-input multiplication oracles. Their Q O(r^4) cost and the repeated K O(r^4) conversions/evaluations are included in the theorem. All arithmetic-data multiplications use the reviewed explicit shift-and-add backend. Native Python products in the new production file concern dimensions and budget metadata only; their bit costs are included.

The primitive-charge ledger is diagnostic, not an end-to-end operation counter or a speedup claim. The theorem includes comparisons, sort movement, indices, allocations, and stream costs whether or not each appears as a separate ledger entry.

## Fresh independent evidence

`independent_controls.py` was newly authored for this extension. It independently reconstructs the native point with a direct CRT formula, uses exact binomial formulas for the native matrices, performs independent canonical expansions, and uses native arithmetic only in test oracles. It imports no earlier control file.

All controls pass:

- 22 independently reconstructed native plans, ranks 3 through 24.
- 27 complete products, including zero, signs, unequal lengths, low-threshold arbitrary data, dense constant blocks, all-ones carry boundaries, zero runs, leading shifts, and growing dense-run families.
- 27 exact original source-row and source-packed-product identities. These check the original canonical rows, their vector differences, actual maxima, byte-rounded widths, and the identity D_A(Q)D_B(Q)=(1-Q)^2 F_A(Q)F_B(Q) at each tested source node.
- Nine corrupt-certificate rejections: omitted terminal transition, omitted input change, event position/sign, duplicate product, target value, source width, leaf row, and product row.
- A nonlinear-encoding regression explicitly demonstrates that c(b)-c(a) differs from c(b-a), while the coefficient-vector construction preserves every original source row.
- Exact budget rejection and successful use of the accepted complete fallback.

The growing dense family at ranks 12,14,16,18,20 has occupied supports 18,41,140,485,1,133 on both sides. Its jump counts grow from (3,4) to (11,12). The rank-20 case has 1,050,291 input bits, 132 jump-pair events, 23 distinct signed-normalized leaves, and 132 shared products. It passes the fixed factor-64 linear-budget test, returns the correct signed product, and uses no packed child multiplication. Its largest elementary multiplication operand has 1,774 bits, versus over one million input bits. The largest prefix intermediate has 1,862 bits, consistent with the O(r^2) cancellation-width proof.

The arbitrary-valued dense-constant test has 140 and 133 occupied blocks, just two jumps on each side, and one shared product. It passes with full carry propagation. These finite examples support the construction; the growing-parameter theorem rests on the proof, not on measured timings.

## Remaining open question

The method exploits a sparse first difference of the original canonical block-polynomial stream. It does not show that general inputs possess such a representation or any other small shared representation. Typical unrelated dense blocks fail the linear-budget test. The arbitrary-dense shared-graph question remains open.
