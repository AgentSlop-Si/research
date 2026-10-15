# Block-carried Newton tree: exact affine composition, paid width barrier

15 October 2026. Fresh construction and tests. Scope: compose the new direct canonical Newton-Horner producer in blocks, without importing a multiplication engine, materializing a dense operator, or treating its application as an oracle.

## Result

An exact compact block operator exists. It consists of two nonnegative integers `(P,H)` and has the action

    F(V) = P V + H B.

A balanced tree constructs this descriptor and an explicit canonical carry scan applies it. Every intermediate output digit remains canonical. A block of h original Horner stages reduces the number of normalization cells by a factor of h, but its descriptor and carry width can be Theta(h w), where w is the largest radix width. The provided elementary implementation pays for that width. Its whole digit-core bound remains O(s(s+t)w^2), with the input/output conversions still paid. Thus this construction is a closed, compact elementary algorithm, not a fast-multiplication admission.

There is an important positive exception: every complete-period constant block is exactly an r-digit shift, even in the unreduced sparse algebra. It must not be charged as a generic factorial-sized matrix. The input-dependent block H remains an arbitrary product source; the shift identity does not compute H B.

The obstruction is scoped to the displayed scalar/carry implementation, explicit band expansion, and leafwise tree application. It is not an impossibility theorem for all compact carry representations, nonlinear compilers, or original-route algorithms.

## 1. Contract and compact affine semigroup

Let

    b_i = p + g (i mod r),   p >= 3, g > 0, r >= 1,
    W_0 = 1, W_(i+1) = b_i W_i.

Inputs A and B have canonical digits a_j and beta_i. Their lengths are s and t; swap them so s <= t. Put U=s+t and w=bitlength(max_i b_i).

The original direct producer executes, in descending j order,

    V <- b_j V + a_j B.

For an interval I=[l,u), define

    P_I = product_(j=l)^(u-1) b_j,
    H_I = sum_(j=l)^(u-1) a_j product_(q=l)^(j-1) b_q.

Then 0 <= H_I < P_I and the whole interval acts as

    F_I(V) = P_I V + H_I B.

This is an actual descriptor, with at most O((u-l)w) bits. It does not contain a dense matrix or a factorial-coordinate vector.

For adjacent low and high intervals L=[l,m), R=[m,u), chronological execution is R first, then L. Exact composition is

    (P_L,H_L) o (P_R,H_R)
       = (P_L P_R, H_L + P_L H_R).

The order matters in H, even though the two P factors commute. The result obeys H<P, because

    H_L + P_L H_R <= P_L-1 + P_L(P_R-1) = P_L P_R-1.

`describe` constructs this pair by a balanced binary tree; `compose` implements the two products with explicit shift/add. All descriptor arithmetic is paid. Depth is logarithmic, while arithmetic work is not thereby logarithmic.

## 2. Exact canonical block application and carries

Given canonical old digits v_i and beta_i, the block operator is applied by

    c_0 = 0,
    raw_i = P v_i + H beta_i + c_i,
    (c_(i+1), d_i) = divmod(raw_i, b_i).

Here all quantities are nonnegative. This is exactly the integer-specialized action of the composed sparse Newton steps, with canonical normalization at the block boundary. It uses neither signed symbolic coefficients nor any division in a per-frequency quotient.

The invariant is

    0 <= c_i <= P+H-1.

Indeed, if the bound holds at cell i, then

    raw_i <= (P+H)(b_i-1)+(P+H-1) = (P+H)b_i-1,

so its quotient is at most P+H-1. The base carry is zero. The raw width is at most log2(P+H)+w+O(1), hence O((h+1)w) for an h-stage block.

Uniqueness of canonical representation establishes equivalence to normalizing after each original sparse step: both compute the same nonnegative integer. This does not assert that their intermediate raw coordinates are equal.

### Output capacity

The original periodic-radix inequality W_(s+t)>=W_s W_t still applies. A suffix Horner value is at most A, so every original stage and every block boundary value is at most AB<W_(s+t). The implementation processes U+1 cells and asserts that both the extra digit at U and its outgoing carry are zero. There is no guessed high carry cutoff.

### A legal width witness

Take a single full-period block with every input digit maximal. Then

    P=Q=product_(i=0)^(r-1) b_i,  H=Q-1.

At the first block old=0. Choose B=W_L-1, so all beta_i are maximal. After i digits the carry is exactly

    c_i = H - ceil(H/W_i).

This follows directly from the lower i-digit value W_i-1. Once W_i>=H, the carry is H-1. Thus the block carry genuinely needs Theta(log Q)=Theta(r log r) bits for fixed p,g and growing r. This is an ordinary canonical legal input, not an oversized coefficient input.

For r=128,p=7,g=4, Q and the witnessed carry have 978 bits, whereas each canonical digit has at most 10 bits. Normalizing only at this block boundary is not an O(w)-bit-carry implementation. Splitting that carry into h small subdigits preserves small cells but requires a separately specified update algorithm; it does not make processing those subdigits free.

## 3. Carry boundaries between digit chunks

Consider a chunk of digit positions [a,b), with local weights R_0=1 and R_(k+1)=b_(a+k) R_k. Define

    R = product_(i=a)^(b-1) b_i,
    X = sum_(i=a)^(b-1) v_i product_(q=a)^(i-1) b_q,
    Y = sum_(i=a)^(b-1) beta_i product_(q=a)^(i-1) b_q,
    K = P X + H Y.

For incoming carry c and the canonical chunk value D, the exact boundary equation is

    R c_out + D = K+c,  0<=D<R,
    c_out = floor((K+c)/R).

Two successive low-to-high chunks have descriptors (K_1,R_1),(K_2,R_2), and combine as

    (K_1+R_1 K_2, R_1 R_2).

This gives a real associative carry-scan representation. However, K is acquired by the products P X and H Y and can have O((h+chunk_length)w) bits. Calling this a constant-size descriptor means two integers, not constant bit size or free acquisition.

If R>P+H-1, the outgoing carry as c ranges over its allowed interval has at most two consecutive values, representable by a quotient and a threshold. That compresses the *effect of the already acquired chunk*. Computing K, its quotient/remainder, and the actual output digits remains necessary. The implementation does not substitute a free threshold oracle for those operations.

The tests check the exact boundary equation and its composition at random splits, including empty chunks. Dropping the incoming carry between chunks is detected as a negative control.

## 4. Sparse block expansion and the full-period cancellation

To distinguish scalar specialization from symbolic expansion, introduce the global polynomial basis

    E_i(x) = product_(t=0)^(i-1) (x+b_t),

with periodic b_t. Multiplication by x has the sparse operator

    L E_i = E_(i+1) - b_i E_i.

Evaluation at x=0 is the mixed-radix integer map, because E_i(0)=W_i. The original sparse step corresponds to M_j=L+b_j I.

### Proper blocks can expand into wide bands

Suppose [l,l+h) does not cross the first period, and i+h<=r. Then

    product_(j=l)^(l+h-1) M_j E_i
       = sum_(k=0)^h C_(h,k,i) E_(i+k),

    C_(h,k,i) = binom(h,k) g^(h-k) (l-i)^(overline(h-k)).

The rising factorial identity follows by applying the binomial convolution for rising factorials to the product of h consecutive translated linear factors; it is also checked against independent repeated sparse updates. This formula describes the actual expanded coefficients rather than pretending the original bidiagonal sparsity is preserved.

For l=0, h<=r/4, and i in [r/2,r-h], all h+1 coefficients are nonzero. For k<=h/2 their magnitudes have Omega(h log r) bits for fixed positive g. Thus explicit expansion contains Omega(r h) nonzero entries and, over those columns, Omega(r h^2 log r) stored bits. This is a cost of that explicit representation, not a lower bound on structured application.

At the diagonal, even without the no-wrap condition for the other entries,

    [E_(r-1)] product_(j=0)^(r-2) M_j E_(r-1)
       = (-g)^(r-1) (r-1)!.

So merely delaying carries across a long proper sparse block can restore the familiar factorial-sized coordinates.

### Complete-period constant blocks are different

Let f(x)=product_(j=0)^(r-1)(x+b_j). Periodicity gives

    f(x) E_i(x) = E_(i+r)(x)

for every i. Therefore

    product_(j=0)^(r-1) M_j = S^r,

where S is the global digit-position shift. This is an exact symbolic identity; cancellation removes every other band. Any complete number of periods similarly yields S^(kr), regardless of starting phase.

Consequently an h=kr block can apply P V=Q^k V by shifting the canonical old digit vector h places. `apply_block` implements this optimization. The carry recurrence becomes

    raw_i = v_(i-h) + H beta_i + c_i,
    0<=c_i<=H.

This pays only the input-dependent H beta_i product at each cell. It does not compute H B for free: H ranges over every integer in [0,Q^k), so the unresolved data product is arbitrary. For one full input block at the root, H=A and old=0. Applying the descriptor is exactly the original multiplication problem.

The tested complete-period shift identity prevents overgeneralizing the proper-block factorial witness into a false obstruction for all block constants.

## 5. Closed elementary cost and tree recurrence

All production products in `producer.py` use explicit shift/add. Division uses binary long division with a bit-list quotient, packed linearly into its integer representation; it does not repeatedly copy a growing quotient to assert a falsely linear division bound. The code never invokes Python's full-input a*b or a convolution backend. Native full multiplication and divmod are confined to the separate test oracle.

For an h-stage descriptor, P and H have at most hw+O(1) bits. Multiplying either by a canonical digit costs O(hw^2) elementary bit work. Dividing the resulting O(hw)-bit raw value by a w-bit radix also costs O(hw^2). Additions are O(hw). These are abstract bit-operation upper bounds, not Python timing claims.

Balanced descriptor construction has the elementary recurrence

    D(k) <= D(floor(k/2))+D(ceil(k/2))+O(k^2 w^2),
    D(1)=O(w),

hence D(k)=O(k^2 w^2). For a partition into block lengths h_q summing to s,

    descriptor construction = O(w^2 sum_q h_q^2),
    canonical applications = O((U+1) w^2 sum_q h_q)
                           = O(s(U+1)w^2),
    normalized cells = number_of_blocks * (U+1).

Since h_q<=s<=U, descriptor construction is covered by the same upper bound. Period-shift blocks remove one constant product per cell but leave the stated generic data-product bound. A finite witness can show better constants and fewer cells without establishing a different asymptotic bound.

For equal size h, this is the precise tradeoff: roughly sU/h cells of width hw, not sU/h cells of width w. For h=s, the descriptor is `(W_s,A)` and its application is elementary wide-by-digit multiplication of A and B. For h=1 the descriptor scan uses positive scalar multiplication rather than the original signed sparse arithmetic; its asymptotic elementary ledger agrees, but its constants are not claimed to match the earlier code.

If a tree is instead kept unevaluated and applied by calling its two child actions, its s leaves still visit the U-digit accumulator. If the tree is evaluated to its compact root descriptor, the H B operation remains. Replacing that operation with a faster unnamed multiply would be circular or would import a different engine. No such substitution is used here.

### Paid binary conversion

`to_digits` uses repeated explicit binary long division by the actual radices. `from_digits` uses reverse Horner evaluation with explicit shift/add. Their elementary bounds are O(n_A^2+n_B^2) and O(n_out^2), respectively, where n_out<=n_A+n_B. The zero-quotient conversion step short-circuits when the current value is smaller than the radix; oversized unused parameters do not force a false n-by-w division scan.

Including base-table preparation and the supplied binary parameter-length lambda, the complete bound is

    O(lambda + r w + n_A^2+n_B^2+n_out^2 + s(s+t)w^2).

The actual digit lengths and actual w must be used. This is O(n^2) in the balanced, complete-period regimes where n=Theta(r log r) for a single growing period with fixed positive p,g. It is not an unconditional replacement of arbitrary parameter size by n.

Live arithmetic storage can be O(n_A+n_B+n_out+(r+s+t+h)w) bits, using a depth-first descriptor tree and applying each root before moving to the next block. No dense matrix, coordinate CRT range, all-block product table, or factorial constants are retained.

## 6. Executed validation and counters

`python block_carried_newton_tree/test_blocks.py` passed on 15 October 2026:

- 1,000 explicit scalar-product checks and 1,000 long-division checks
- 504 interval-descriptor identities and 63 associativity checks
- 1,424 full binary-input/binary-output products
- 630 optimized/unoptimized period-shift pairs
- 2,000 chunk boundary and carry-map composition checks
- 1,904 no-wrap sparse-band coefficient columns, plus full-period symbolic shift checks
- 6 legal maximum-digit width witnesses, r=4,...,128
- 4 negative controls: wrong interval order, discarded carry, invalid partial-period shift, and false one-digit carry cap

No supplied source program or earlier producer is imported or run by these files. `results.json` contains the actual seeded runs and ledgers.

In a fixed r=128 maximum-digit example with operand lengths 128 and 256, block size 1 uses 49,280 normalized cells and at most 10 carry bits. Block size 128 uses 385 normalized cells and at most 978 carry bits. The latter also exploits the exact period shift. These counts illustrate the paid width tradeoff. They are not a wall-clock benchmark, a universal lower bound, or a faster arithmetic-backend comparison.

## 7. Admission and exact remaining interface

Retain:

1. The concrete affine block descriptor, its composition orientation, and the fully paid elementary application.
2. The exact chunk-carry descriptor and its boundary equation.
3. The distinction between proper-block wide bands and complete-period pure shifts.
4. The legal carry-width witness and complete conversion/storage invoice.

The proposed fast target remains unmet. To improve this lane, a next construction must evaluate the input-dependent H B or the carry-map payloads with fewer *paid bit operations*, while preserving the actual output digits and both conversion costs. A claim that the descriptor tree has logarithmic depth, that it stores two integers, or that a complete-period constant product is a shift does not establish that missing operation.

This result does not settle other adaptive precision, valuation, nonlinear carry, or correlated-channel proposals. It isolates the current block compiler's exact useful interface and its remaining multiplication cost.

Sources: fresh derivation from `newton_direct_carry/REPORT.md` and `producer.py`; recovered-source context in `latest_multibase_material_audit/REPORT.md` and `source_multibase_report_1640.md`. These are dependency records, not a historical novelty claim. No external mathematical-source attribution or external-engine result is needed for the displayed elementary identities.
