# Certified bounded-support shared multiplication: a complete dispatcher

17 October 2026. Fresh implementation and fresh controls. Candidate for independent review. No historical program was imported or executed; no external write was made.

## Result

`shared_dispatcher.py` is a terminating, exact multiplier for arbitrary signed integers. Its default policy combines:

1. Exact removal of each input's binary shift.
2. A recognizer for at most four occupied native binary blocks per reduced input.
3. Extraction of the common integer content of the block-polynomial coefficient vectors, normalization and interning of repeated polynomials, and a shared product DAG.
4. Memoized, explicitly elementary evaluation of that DAG at the retained ordinary Newton nodes.
5. Exact structural and execution certificates, including actual row maxima and source-rule packing widths.
6. The newly reimplemented adaptive native-Newton recursion on unrecognized inputs, with a strictly-contracting-child guard and an elementary base case.

For every fixed support limit, the recognized branch, **including recognition, certificate checks, node preparation, reconstruction, shifts, and dense output**, costs O(n + (log n)^12) = O(n). This applies to arbitrary values in the occupied legal blocks, not just a prescribed monomial or three-term product. The exponent 12 is a deliberately loose elementary upper bound, not an optimized exponent or an empirical fit.

For arbitrary inputs the default dispatcher has the proved worst-case upper bound

T(n) <= n exp(O(log n / log log n)).

There is no matching lower bound for this new policy. In particular, neither an arbitrary-input N log N improvement nor a lower bound for arbitrary shared DAGs is claimed. This is an implementation completion of a bounded-support sharing option, not a novelty claim about sparse convolution or common-subexpression elimination.

The accepted independent-call hard family is now handled in linear time by the actual code. The legal odd perturbation also takes the shared branch: the 131,352-bit test has 33 distinct first-level child pairs, including 16 odd pairs, and no child-width multiplication is performed. General four-block cases and repeated nonconstant block-polynomial cases pass as well.

## 1. Exact algorithm and interface

The public call is `Dispatcher().multiply(a, b)`. The default base threshold is 1,024 bits, the fixed support limit is four, structural checking is always enabled, and the additional independent-form execution check is enabled by default. `force_dense=True` is a diagnostic comparison option, not the default policy. The implementation handles both signs, zero, unequal lengths, and arbitrary binary shifts.

Let n be the maximum input bit length at a call. Zero terminates immediately. For nonzero magnitudes, a dense byte scan finds t_A = v_2(A), t_B = v_2(B). The reduced operands are A' = A/2^t_A and B' = B/2^t_B. Set n_0 to their maximum bit length. Below the base threshold use explicit schoolbook multiplication of the reduced operands and restore the combined shift and sign.

Otherwise set r = floor(log2 n_0) and reproduce the accepted native integer plan:

- E_r = lcm(1,...,r), d_r = E_r/r;
- the same prime-power CRT residue construction supplies k and P_r = 1 + k E_r;
- W_j = binom(P_r + j - 1, j), beta = W_r/d_r;
- s = floor(log2 beta), rho = 2^s;
- the same dimension-only minimax translation selects 2r-1 consecutive nodes.

The plan is cached by rank and every first construction is charged. Nothing assumes prime-Mersenne points. Both inputs are split into legal s-bit binary blocks using bounded byte windows. This scans the dense input once; it does not repeatedly shift the whole input. The smaller input need not be padded until the dense fallback is chosen.

Every legal block B has its canonical expansion B = sum_j c_j W_j. Its associated ordinary polynomial is

f_B(x) = sum_(j=0)^(r-1) (-1)^j c_j binom(x,j),

and f_B(-P_r) = B. The canonical digits are produced with explicit binary long division.

### Recognizer

The recognizer reads every block, including zero blocks. It accepts precisely when both occupied supports have size at most the fixed limit. It neither assumes that zeros were supplied by an oracle nor accepts a support list without binding it to the dense input.

For each occupied block, take the gcd of its coefficient vector and divide out this content. Intern the resulting primitive nonnegative coefficient vector by exact bounded linear search. Also divide out the gcd of all the contents on each side and record the first occupied outer position. These are exact factors of the formal block polynomials and of their evaluated integer. They are not asserted to be the maximal gcd of the original integer operands.

The binary shifts are removed before selecting the plan. Thus a remaining outer shift is normally zero at the integer API, but the row/compiler API supports nonzero outer shifts and has a separate exact test. Content is applied to small nodal coefficients before reconstruction; the algorithm never creates a dense large integer and then multiplies it by a supposedly free content factor.

### Shared DAG

Write the two factored outer polynomials as

F_x(Y) = g_A Y^q_A sum_(i in S_A) a_i p_(u_i)(x) Y^i,

G_x(Y) = g_B Y^q_B sum_(j in S_B) b_j p_(v_j)(x) Y^j.

Each p is one interned primitive block polynomial, represented by its entire Newton coefficient vector. There are at most eight leaves at the default limit. For every input term pair create or reuse the commutative product node {u_i, v_j}; this has at most 16 nodes. Edges record outer position i+j and the exact scale a_i b_j. Edges with the same position and product node are combined by addition.

At each retained x, evaluate each primitive leaf once, evaluate each product node once, and distribute its scaled value to the supported output columns. A second exact cache reuses equal small integer products, including products that coincide at different nodes. Cache lookup is a bounded linear search over polynomially many polynomial-bit values, so the proof does not assume expected constant-time hashing or collision-free fingerprints. All cache misses use the explicit elementary multiplier.

The node representations are **polynomials in Y**, not materialized dense integers. For a node with maxima A_x,B_x, the certificate records exactly the source packing rule

w_x = 8 ceil(bit_length(2 L A_x B_x)/8),

where L is the maximum original block-list length. If A_x B_x = 0 the row product is certified zero and w_x is recorded as zero. Otherwise substituting Y = 2^w_x gives precisely the old packed child product. Widths may vary with x; the symbolic product remains valid because its identity is in Y. No equal-width assumption is made.

Only supported outer columns are interpolated. Their values at -P_r are nonnegative integer block-convolution coefficients. Binary carrying and dense serialization then reconstruct A'B', after which the original shifts and sign are restored.

### Dense fallback

If either support exceeds the fixed limit, newly written code prepares all canonical block vectors and ordinary nodal rows. It uses the retained signed positive/negative byte streams, actual maxima, strict byte-rounded packing, balanced extraction, and ordinary finite differences.

For each nonzero row it forms the actual packed integers U_x,V_x. If any actual child width is at least n_0, this parent terminates with elementary multiplication. Otherwise the dispatcher recursively multiplies each child pair. Each recursive call can itself extract binary shifts or recognize a shared sparse representation. The returned products are balanced-unpacked, every outer column is interpolated, and the output is carried and serialized.

This is a new executable completion. The pinned historical producer still uses native Python multiplication at packed calls; that historical product is not imported into this implementation.

## 2. Certificates and exactness

There are two independent-form checks in the default sparse branch.

### Structural checker

`check_structure` does not invoke the compiler. Given the actual block lists and native plan, it checks:

- exact version, rank, point, block width, and node window;
- bounded leaf/product counts and primitive nonnegative leaf vectors;
- positive content, valid shifts, valid indices, no duplicated occupied positions;
- reconstruction of every canonical digit vector and every occupied block;
- equality with the complete support scanned from the input, so omitted nonzero blocks fail;
- the declared common contents and first positions;
- every required term-pair edge, its commutative product node, position and integer scale;
- absence of unused product nodes.

Exact integers, not digests, bind this certificate to the input. Digests in the example package are convenient identifiers only.

### Execution checker

`check_execution` does not reuse the DAG evaluation or its caches. It re-encodes the occupied input blocks, directly evaluates their full canonical polynomials, and directly convolves each pair of sparse rows. It checks every recorded node, input term, actual maximum-derived envelope, strict width, supported product coefficient, and interpolated output coefficient. A zero coefficient at a formally supported position is retained consistently.

Thus a compiler, cache, or edge-scaling mistake is not silently accepted merely because the same expression was reused. The checker still shares the elementary arithmetic routines and the accepted native plan, so this is not a claim of a formally verified trusted kernel or of an independent implementation review. The separate reviewer should inspect those routines and the proof as well.

### Correctness theorem

For every signed integer pair, the default dispatcher terminates and returns their product.

For a recognized input the structural certificate establishes the displayed F_x,G_x identities term by term. Distributivity establishes the product DAG. Each output-column polynomial has degree at most 2r-2. Its values at 2r-1 distinct integer nodes determine it uniquely; finite-difference interpolation at -P_r recovers exactly the original binary-block convolution. Exact carrying, shifts and sign restoration give AB.

For a rejected input, each packed coefficient convolution is bounded by L A_x B_x and 2^w_x > 2 L A_x B_x. Centered recovery is therefore unique. The signed-stream packing and final borrow check implement that recovery, including negative packed products. The same interpolation and binary-carry argument proves the parent product once the child products are correct.

Every recursive child is strictly smaller than its parent's reduced width. Binary shift removal only decreases widths. A noncontracting request invokes the terminating schoolbook guard instead. Strong induction on width proves termination and correctness. The finite test suite supports this argument; it does not replace it.

A malformed candidate certificate is rejected by the checker; the public multiplier does not accept caller-supplied unchecked certificates. Unrecognized ordinary inputs take the exact dense fallback. A rejected internal certificate is a hard diagnostic error rather than an attempt to continue with an unverified result.

## 3. Backend: no hidden large multiplication oracle

The production module uses `Elementary.mul` for every product of arithmetic data: plan construction, block maps, content scales, nodal products, interpolation, base cases, and termination guards. It is signed bitwise shift-and-add, with no call to the host's large-integer product. Its charged elementary bound for operand lengths p >= q >= 1 is 8(p+q+1)(q+1). This pays for the repeated shifts, accumulator additions and bit scans; it is a conservative upper charge rather than an optimal multiplication count.

`Elementary.divmod` implements nonnegative binary long division. Exact divisions and signed modular reductions use it; gcd and modular inversion are built from it and the elementary multiplier. Its recorded charge is 8(p+q+1)(max(0,p-q)+1). The finite primitive controls compare this implementation with the host oracle, but the production multiplier does not use that oracle.

Host multiplication by signs, fixed constants, and loop/allocation/index dimensions remains ordinary implementation bookkeeping. Its operands are metadata, not packed child operands. The analysis charges these operations by elementary bit bounds too. This does not import the host's fast multiplier as a multiplication algorithm for the user's inputs.

The control programs alone use native products as endpoint oracles. Their operation costs are not claimed as the algorithm's runtime. Historical programs are neither imported nor run.

### Streams and output are paid

A superficially similar implementation can accidentally spend O(ns) time by repeatedly shifting an s-bit reservoir one byte at a time. This implementation avoids that as well as repeated whole-integer shifts. It takes one bounded s+7-bit window per input block. For output, it first performs the binary carry, then makes one bounded byte write per output block, OR-ing only the overlapping initial boundary byte. The byte-window routines have separate round-trip tests for every s from 1 through 65.

Signed packed children likewise use bounded byte windows. Final dense conversion, shifts, digests, and output writes are all linear in the represented lengths. Dense fallback columns are stored in a list; the sparse dictionaries have a fixed bound on their size.

### What the counters mean

`charged_bit_work` is a reproducible ledger of the stated arithmetic primitives and stream charges, not a wall-clock measurement or a literal count of Python interpreter instructions. Metadata, control, exact comparisons, allocation and list management are included in the asymptotic bounds below, even where the diagnostic ledger does not count each interpreter action individually. The finite comparison reports this ledger specifically; it is not presented as an exact end-to-end speed ratio. There is no free large multiplication in either the implementation or the asymptotic argument.

## 4. Complete cost bounds

Write r = floor(log2 n_0). The accepted native facts are s = Theta(r^2), log2 P_r = Theta(r), and O(r) bits for canonical digits and nodal row entries. Interpolation weights and reconstructed column values have O(r^2) bits. Constants here depend only on the fixed policy, not on occupied positions or block values.

### Recognized branch

The dense scan, binary shift extraction, support recognition, carrying across absent columns, and dense output cost O(n). There are O(n/s) block indices, each of O(log n) bits; elementary index arithmetic is also absorbed in O(n), since s = Theta((log n_0)^2). If n_0 is bounded while n grows through an extracted shift, the nontrivial plan and block count are bounded and dense shift/output cost still gives O(n).

For fixed support limit t, at most 2t complete degree-(r-1) block polynomials are encoded. The entire leaf set, product graph, edge list and sparse column set are bounded in size apart from polynomial-size scalar data. There are O(r) node evaluations. Native setup, all content operations, exact interning, memo lookup, both certificate checks, finite differences and evaluation use only polynomially many O(r^2)-bit operations. With the explicit schoolbook and long-division backend, O(r^12) is a conservative common bound for all this work, including metadata and trace construction.

Therefore the **whole branch**, not just its product graph, has cost O(n+r^12) = O(n). Its dense nonzero output has Theta(n) bits, so this is tight on the nondegenerate positive families used here. The fixed t condition matters: this is not an O(n) theorem when the support limit is allowed to grow with n.

### Arbitrary-input fallback

Every failed recognition is paid by its single dense block scan. The ordinary conversion, direct maps, stream preparation, interpolation, output and all administrative work admit the conservative bound

F(n) = O(n (log n)^12).

This intentionally enlarges the accepted sharper local ledger, so no optimization of Python bookkeeping is needed to preserve the recurrence scale. Sparse accepted calls are cheaper than this bound eventually.

At a dense parent of reduced width n_0, every actual child is bounded by its accepted fixed-cap width. Each cap is O(n_0/log n_0); the total cap volume is at most (v_+ + o(1))n_0, where

v_+ = 9.0889395816... .

The elementary estimates from the accepted native policy suffice here; the numerical constant is inherited only as a convenient explicit cap. At sufficiently large reduced widths all cap children contract, so the noncontracting guard is used at only finitely many reduced sizes. Its schoolbook work is paid in the finite induction base. If much of the original input was shifted away, the O(n) restoration cost is still paid and the recursive problem has only become smaller.

For Phi_b(n) = n exp(b log n/log log n), every fixed b > log v_+ gives an eventual inductive margin because the sum of cap-child Phi values divided by Phi at the reduced parent is at most exp(-b)(v_+ + o(1)) < 1. The local polynomial-logarithmic cost is o(Phi_b(n)). Monotonicity of this majorant handles the reduction from original to shifted-away core widths. Thus

T(n) = O(Phi_b(n)) for every fixed b > log v_+,

and in particular T(n) <= n exp(O(log n/log log n)). The base threshold, caches, checks and guard do not introduce any uncharged product oracle.

**Only this upper bound is proved for the new arbitrary-input policy.** The accepted independent-call lower bound does not survive automatically after adding shifts and shared sparse products. A generic shared-graph worst-case improvement remains open.

## 5. Genuine gains and finite evidence

### The accepted closed hard family

On the accepted aligned family C 2^E, with C of O(log n) bits, the implementation's first scan extracts E and its elementary base case multiplies the small cores. Dense shift/output costs O(n). The accepted independent-call policy takes n exp(Omega(log n/log log n)) on the carefully aligned family. This is a genuine theoretical separation between those two specified policies; it is not a lower bound for other algorithms.

### Distinct odd children

For X = C 2^E + P_r with s dividing E and C smaller than P_r, the recognized blocks are a constant polynomial C and the full canonical polynomial for P_r. The generic compiler, without a special-case identity, produces the shared graph. The child operands C 2^(Ew/s) - x are pairwise distinct; at least r-1 are odd. The code does not rely on duplicate packed calls or an input binary shift in this case.

At r=17 the fresh control has E=131340, C=2049, P=7867935195121 and 131352-bit operands. All 33 child pairs are distinct, 16 are odd, and each has 6380 actual bits. The default computation makes one dispatcher call, takes the shared branch, and performs no 6380-bit child multiplication. Its largest elementary operand, including setup and interpolation, has 1254 bits. The certificate's sparse product substituted at each source packing base agrees with the fully materialized child product in all 33 oracle checks.

The previously accepted report did not establish a closed recursive lower bound for this odd perturbation, so neither does this report claim an asymptotic lower bound for independently multiplying it. Its purpose is to establish that the new implementation really shares structure even when the packed inputs are distinct and the original input is odd.

### Wider positive class

Three controls use four arbitrary legal nonzero block values on each side, at ranks 12, 14 and 16. They all take the shared branch and return exact signed products. Another control has repeated nonconstant primitive polynomial 2-x, with common contents 3 and 5, and compiles four term pairs to one shared product node. It exercises content normalization and polynomial sharing beyond the earlier leading-monomial formula.

### Negative and fallback controls

- Adding one fifth occupied block forces the dense fallback at the root; the product remains exact.
- Changing a nearly equal block creates an additional primitive leaf rather than falsely sharing it.
- A nodal zero certifies zero width and no packed multiplication.
- Twelve forged-certificate tests reject missing support, changed content/leaf/edge scales, wrong native point/window/outer shift, wrong width/envelope/convolution/interpolation, and replay on a changed input.
- 120 exact strict-width boundary checks include the power-of-two boundary and its two neighbors.
- An explicit low-threshold, support-one case triggers the noncontracting guard and returns the exact product.

The complete control files also cover dense random signed inputs, unequal lengths, all-ones inputs, independent large shifts, minimal base settings, 4,225 small signed primitive products, 4,096 small long divisions, 100 larger primitive pairs, 260 stream round trips, and 108 legal canonical blocks.

The 16,490-bit comparison runs the same input through the default shared path and the newly implemented forced-dense path, both with the elementary backend. The shared execution makes one dispatcher call; the forced-dense execution makes 522 calls. The exact primitive-charge totals and their ratio are in `CONTROL_RESULTS.json`. This finite reproducible gain is not an asymptotic fit or a claimed wall-clock factor.

## 6. Provenance, reproducibility and stopping point

`SOURCE_PINS.json` records hashes of the intact accepted source archive and its precise native point, node-window, binary nodal-map and packed-outer definitions. It separately names and hashes `shared_dispatcher.py` as the new producer. The accepted adaptive report and its final independent review are also pinned. No statement silently attributes the new dispatcher to a historical module.

Run only the new programs:

- `python3 run_controls.py`
- `python3 boundary_controls.py`

`CONTROL_RESULTS.json`, `BOUNDARY_RESULTS.json`, `RUN.log`, and `BOUNDARY_RUN.log` preserve the completed evidence. `EXAMPLE_CERTIFICATE.json` is a portable example of the new DAG and node execution certificate; verification also needs the actual operands and native plan, not just their digests.

This completes the specific bounded-support dispatcher: recognizer, common shifts/content, reusable polynomial DAG, memoized evaluation, exact checks, dense fallback, end-to-end cost proof and adversarial controls. The next scientifically different question is whether a larger efficiently recognizable class of dense inputs admits a useful shared representation. That is not needed to finish this implementation and is not claimed to be settled here.
