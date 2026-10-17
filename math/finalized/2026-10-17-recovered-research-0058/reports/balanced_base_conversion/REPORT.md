# Balanced exact p^d conversion: the splitter remains paid

17 October 2026. Supplemental successor to the accepted streamed-divider cost lemma. Candidate pending independent review.

## Result

For p=2^m−1, m≥2, d≥1 and Q=p^d, splitting an integer after k grouped Q-digits requires division by Q^k=p^(dk). Substituting the accepted p-divider cascade therefore uses dk stages, not d. A balanced binary recursion does not remove this factor.

This report defines one complete fixed-capacity conversion tree and proves an exact transition ledger. For L=2^h≥2 output positions and C=dmL binary buffer bits, the division-transition volume is

    V(L)=d²m L²(1−1/L).

All remainder assembly, copying, recursion and output work fit O(C²/m). Thus this deliberately full-scan implementation costs Θ(C²/m) bit work. A balanced reconstruction using repeated p-multiplication has the same order. For arbitrary N-bit inputs and dm≤N, the explicit parameter choice below gives N≤C<4N, hence Θ(N²/m). These statements concern the specified implementation, not all radix-conversion methods.

The new contribution is the completed balanced-tree cost account and its exact ledger, not a new radix-conversion idea. Known large-power divide-and-conquer conversion uses genuinely faster large division/multiplication interfaces. This report does not supply those interfaces, prove their impossibility, or claim a faster integer-multiplication or Fourier algorithm.

No original research program was executed. No existing table cell, score, priority, identifier, source or external file was changed. The existing-cell proposal is empty. The result remains an unbound supplement, not a closure of a broader original-route target or of archived ALG-072.

## 1. Scope and predecessor

The directly inspected accepted predecessor is “A paid streamed divider for the exact grouped Mersenne radix,” with its separate independent acceptance. Its exact local hashes are recorded in SOURCE_REGISTER.json. That report already proves the one-stage divider, d-stage grouped divider, sequential extraction cost, coefficient/carry bounds and independently evaluated block-product invoice. None is presented here as newly proved historical work.

The predecessor explicitly leaves divide-and-conquer conversion outside its sequential lower-bound grammar. This successor examines one precise proposal for that missing case: use the same elementary cascade as the splitter in a balanced tree. It does not extend the predecessor's lower bound to every balanced algorithm.

The domain is nonnegative integers. Both m and d are positive integers with m≥2. No primality assumption is used. A separate application requiring prime p still owes its own prime-selection argument.

Write a=log2 p and w=d a. Since m−1≤a<m, one has m/2≤a<m. Logs are used in the analysis only; the implementation's buffer sizes and parameter choices below use integer arithmetic.

## 2. The exact split and its dk-stage interface

For any k≥1, let D=dk. A cascade of D exact divisions by p gives

    x=p^D q + r_0+p r_1+...+p^(D−1)r_(D−1),   0≤r_j<p.

The residual is less than p^D=Q^k. Hence it is the unique low k-group block, and q is the high block. Substituting d for D would divide by Q, not by Q^k. For example, p=3,d=1,k=2,x=20 gives the required split (q,r)=(2,2), whereas one stage gives (6,2).

For completeness, an m-bit chunk b and incoming remainder r<p are transformed by

    t=r+b; e=1 if t≥p, else 0;
    outgoing quotient chunk=r+e; new remainder=t−ep.

This follows from r·2^m+b=rp+(r+b); the accepted predecessor supplies the full streaming proof. Each transition uses a constant number of O(m)-bit scans. Sequential storage of the D states, including resetting the state head after each input chunk, costs O(Dm) per chunk. Thus no random-access unit-cost assumption is needed for this primitive.

The cascade initially returns the D factored p-digits r_j. If the recursive child expects one ordinary binary low block, that representation must be formed. Reverse Horner evaluation

    v ← (v<<m)−v+r_j

has at most jm bits after j digits. Its direct work is O(m D(D+1)/2). The high quotient is already a binary stream. No explicit integer Q^k or generic multiplication is needed for this split.

## 3. Fixed-capacity balanced conversion algorithm

Fix L=2^h and promise 0≤x<Q^L. Each node representing s grouped positions, with s a power of two, reserves c_s=dms binary bits. This is a conservative capacity: Q^s<2^(dms). It is not a claim that every c_s-bit integer fits in s Q-digits.

At a leaf s=1, copy its value to one dm-bit grouped output slot. At an internal node:

1. Read the node value in exactly ds high-to-low m-bit chunks, with leading zeros permitted.
2. Run D=ds/2 cascade stages on every chunk, including zero-valued states.
3. Materialize the low-block remainder by the reverse Horner rule above.
4. Discard the leading zero quotient capacity, pad each child to c_(s/2)=dms/2 bits, and recurse on both children.

The children satisfy 0≤high,low<Q^(s/2), because x<Q^s and the divisor is Q^(s/2). By induction the leaves are exactly the L low-to-high Q-digits of x, including leading zero groups. A final linear scan can remove leading zero groups and emit canonical [0] for x=0. A public wrapper may recognize x=0 immediately; the ledger below describes the tree subroutine, including its zero-valued children.

An all-zero child is deliberately not skipped in the stated full-scan grammar. A different zero-skipping policy changes the exact ledger. It does not license charging only d states at a nonzero root whose divisor is Q^(L/2).

## 4. Exact ledger and recurrence

One size-s internal node has ds chunks and ds/2 stages. Charging m payload-bit positions per transition gives the exact volume

    V_node(s)=m·(ds)·(ds/2)=d²m s²/2.

There are 2^ell nodes of size s=L/2^ell at level ell, for 0≤ell<h. Therefore

    V(L)=sum_ell 2^ell V_node(L/2^ell)
        =(d²m L²/2) sum_(ell=0)^(h−1) 2^(−ell)
        =d²m L²(1−1/L).

This is a transition-volume identity, not an assertion that every transition takes exactly m machine instructions. The chosen full-width implementation scans Θ(m) cells per transition, so its bit work is Θ(V(L)) before the other paid operations.

The direct low-block assembly capacity ledger is

    A(L)=sum_ell 2^ell m D_ell(D_ell+1)/2
        =(md²L²/4)(1−1/L)+(mdLh/4),
    D_ell=dL/2^(ell+1).

Actual assembly uses a constant number of scans bounded by this ledger. Input/output movement, initializing states, child padding and quotient trimming cost O(C) per level, hence O(C(1+h)). Reading and writing all leaf slots costs O(C). Since h≤L and d≥1, these terms are O(C²/m) for L≥2.

Consequently a uniform bit-work recurrence for this implementation is

    T(1)=Θ(dm),
    T(s)=2T(s/2)+Θ(d²m s²),   s≥2,

and its solution is Θ(d²mL²)=Θ(C²/m). The root alone has volume C²/(2m). Dividing the recursion depth by grouping cannot remove a charge already incurred at the root.

The lower bound here is intentionally narrow: a lower bound on this full-width cascade tree, including its full-width state scans. It is not a lower bound on general division, on arbitrary balanced conversion, on any representation with shared/factored outputs, or on the original multiplication problem. The ledger applies even when many input bits happen to be zero because the algorithm explicitly scans them.

This is a bit-array/sequential-stream account. It constructs the divider primitive with sequential state traversal and pays linear movement at each tree level; it is not a certified implementation or runtime benchmark on a particular fixed-tape machine or physical computer. Storing all levels gives the safe space upper bound O(C(1+h)); a smaller-space implementation would require a separately stated storage schedule.

## 5. Coverage of arbitrary N-bit inputs

Assume N≥1 and dm≤N. Choose L to be the smallest power of two satisfying

    L≥ceil(N/[d(m−1)]).

This uses only integer division and a power-of-two ceiling. Since p≥2^(m−1), Q^L≥2^(Ld(m−1))≥2^N. Therefore every 0≤x<2^N satisfies the tree's capacity promise.

Here N/[d(m−1)]>1, so L≥2. Minimality gives

    L<2N/[d(m−1)],
    N≤C=dmL<2mN/(m−1)≤4N.

The tree thus has Θ(N²/m) work in this regime. Constructing counters, padding the input to C bits and writing the grouped slots all fit the already paid bound; no giant radix power is formed just to choose L.

If dm>N, the same coverage rule may produce one group or a buffer much larger than the actual input. The uniform Θ(N²/m) claim is not made there. A certified one-group input x<Q can simply be copied as one binary-encoded digit; if a caller instead demands a padded dm-bit slot, those dm output bits must be paid. For L=1 the tree does no split at all and its padded-slot cost is Θ(dm), not Θ(d²m).

For this particular full-scan tree with dm≤N, achieving o(N log N) conversion would require m=omega(N/log N). That necessary condition is not a sufficient multiplication algorithm: digit width, arithmetic, output reconstruction and any prime or adaptive-selector setup remain separate costs.

## 6. Balanced reconstruction with the same elementary operations

Let each node receive canonical digits 0≤a_j<Q, and recursively reconstruct its low and high halves. The combine identity is

    value=high·Q^(s/2)+low=high·p^(ds/2)+low.

Starting at high, perform D=ds/2 operations v←(v<<m)−v, then add low. All intermediate values are nonnegative and less than 2^(dms), because high<Q^(s/2), and the completed value is less than Q^s. A c_s-bit buffer therefore suffices.

If each shift/subtract deliberately scans the full c_s-bit parent buffer, the exact multiplication-scan volume is

    R_node(s)=D c_s=d²m s²/2.

Summing the same tree gives R(L)=V(L); additions, copies and leaf reads add O(C(1+h)). This explicitly specified reconstruction is therefore Θ(C²/m). A growing-buffer variant has the same upper bound, but its data-dependent lower bound is not claimed here. The reconstruction uses no precomputed powers and no multiplication oracle.

Reading the groups as if they were binary blocks is invalid: Q≠2^(dm). Likewise p^(dk)≠2^(mdk)−1 in general. For p=3,d=1,k=2, the required power is 9 and the purported all-ones power is 15. These mistakes are covered by negative controls.

## 7. What a genuinely faster balanced interface would owe

The split/recombine tree itself is classical. To replace the cascade by another method, let Div(c,b) denote the fully paid exact quotient-and-remainder cost for a c-bit numerator and a supplied b-bit divisor, and let Mul(c) bound the selected multiply interface with operands of at most c bits. Let P be the cost of constructing Q and the required powers Q^(2^j), including representation work. Then valid schematic accounts are

    T_convert(L) ≤ P+sum_ell 2^ell [Div(c_s,c_(s/2))+O(c_s)]+O(C),
    T_rebuild(L) ≤ P+sum_ell 2^ell [Mul(c_s)+O(c_s)]+O(C),
    s=L/2^ell.

Operand widths may be tightened, but the interfaces must remain paid. Reusing a power across nodes allows P to be shared; it does not make division or multiplication by that power free. An elementary Q setup by d shift/subtract steps costs O(d²m), and repeated squaring of stored powers incurs the chosen multiplication costs as well.

The actual divisor at a size-s node has bit length between ceil(c_s/4) and c_s/2, because d(s/2)(m−1)≤log2(Q^(s/2))<dms/2. The conservative c_s-bit buffer therefore does not justify assuming an exact half-width divisor.

As a conditional algebraic consequence, suppose a separately established exact division interface costs O(M(c)) uniformly for the admitted divisors throughout that bit-length range, Mul(c)=O(M(c)), M(c)/c is nondecreasing and doubling changes M by only a fixed factor. Each level is then O(M(C)), and the sum is O(M(C)(1+log L)), plus setup. If M(c)=Θ(c^alpha) for a fixed alpha>1, the geometric level sum is O(M(C)), plus setup. These are conditional recurrences, not supplied algorithms, and the division premise cannot simply be assumed from a multiplication name.

### Focused primary-source comparison

The GNU MP manual's [Binary to Radix](https://gmplib.org/manual/Binary-to-Radix) section describes recursive quotient/remainder splits using precomputed radix powers, and explicitly charges power preparation. It credits the improvement to large subquadratic division. This matches the tree structure, while differing from this report's linear cascade in the split primitive. No novelty is claimed for balanced splitting.

The [Radix to Binary](https://gmplib.org/manual/Radix-to-Binary) section describes combining adjacent blocks with progressively larger radix powers, so the reconstruction tree is also known. That page explicitly says its description predates GMP 4.3 and needs rewriting; it is used only as historical algorithmic evidence, not as a verified description or performance claim for current GMP internals.

The [Divide and Conquer Division](https://gmplib.org/manual/Divide-and-Conquer-Division) section explains that its improvement relies on large recursive multiplication, and warns that basecase multiplication can leave essentially the old work plus overhead. Thus a balanced control structure alone is insufficient. Its displayed near-linear multiplication regime can have an additional logarithmic factor in division, so this report deliberately does not assert Div=O(M) for that particular routine.

These three pages were read directly on 17 October 2026. The comparison is sufficient to reject broad novelty of the split/recombine structure. It is not an exhaustive priority search, nor an execution or speed comparison. No GMP or historical user program was run.

## 8. Evidence and disposition

The new standalone fresh_controls.py checks exact all-stage splits, balanced conversion and reconstruction, the closed-form ledgers, integer-only input coverage, composite Mersenne bases, zero/boundary inputs, one-group cases and invalid shortcuts. Python arbitrary-precision arithmetic is an exactness oracle only, not timing evidence. CONTROL_RESULTS.json records the completed scope and counts.

The independently accepted earlier sequential theorem remains unchanged. The successor closes only the proposed “balance the same cascade” cost gate. Faster large-power division, factored/shared alternatives, optimized representations, adaptive parameter selection, the full original-route product interface and any end-to-end speed advantage remain unresolved.

Status: scoped candidate proof and cost account, pending independent review. Empty owner-cell changes; no broader closure, score change, historical novelty or FFT-break claim.
