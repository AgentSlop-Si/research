# Independent ACCEPT: unpinned singleton minimum is fourteen

14 October 2026. Independent review of the candidate in `free_singleton_candidate`.

## Verdict and exact scope

**ACCEPT.** Over F23, with N=11 and q=13, the minimum number of original signed resolvent banks is exactly **14**, provided there is exactly one effective alpha node in each cross-sign orientation (-,+) and (+,-). The locations of those two nodes are independently free. They are not assumed equal or fixed at 4 in the lower-bound proof.

The minimum ranges over all legal alpha, beta and raw phase weights in F23. Repeated banks, canceled effective groups, beta=0 and zero-alpha same-sign banks do not invalidate the necessity argument. The upper-bound construction uses the legal special choice beta=1 throughout, both cross nodes 7, and same-sign supports {6,7,12,13,17,19}.

This verdict is not an unrestricted-orientation-count optimum. It retains the two singleton conditions. It makes no claim about historical novelty, characteristic-zero lifting, asymptotic complexity, or FFT speed. The previously reported pinned-alpha=4 minimum of 16 is a distinct result; its complete proof is not re-reviewed here. The new census independently confirms the pinned six-node obstruction, but the present equality14 is self-contained and does not depend on a prior theorem.

## 1. Original grammar and independent method

Fix S e_t=e_(t+1 mod 11), T e_t=13^t e_t and F[k,t]=13^(-kt). One actual bank is

    (1/11) sum_(j=0)^10 w_j (I-alpha S^epsilon-beta 13^(epsilon delta j)T^delta)^(-1),
    epsilon,delta in {+1,-1}, Delta=1-alpha^11-beta^11 != 0.

The fresh reviewer program does not import, compile or execute candidate or historical code. Candidate JSON is read as inert proposed arithmetic, then independently reconstructed. Only newly authored reviewer code runs. No external service is written.

Two methods deliberately differ from the candidate's coefficient construction:

1. Target Weyl coefficients are extracted from the literal matrix's shifted diagonals:

       c(a,b)=(1/11) sum_t F[t+a,t]13^(-bt).

   This gives C=c(0,0)=18 and c(a,b)/C=13^(3(a+b)^2) for every coordinate.

2. Gaussian factors are reconstructed by enumerating every binary word in S^epsilon and T^delta of total length at most ten. Each T preceding S contributes 13^(epsilon delta). This is direct word counting, not an invocation of the candidate's Gaussian recurrence. All 2,047 words per orientation are included. A separate enumeration of length-eleven words verifies that every mixed coefficient vanishes and the two pure coefficients are one. Thus the geometric inverse reduction is valid for arbitrary alpha and beta in this field.

For the witness, the reviewer constructs the literal 11-by-11 matrices and inverts them with fresh modular row elimination. It checks both inverse products, forms the bank sum from raw weights, and separately reconstructs every bank from the derived Weyl factors. The raw weights are also recovered independently by solving the character-transform linear system, then compared entrywise with the proposed weights.

## 2. Literal witness result

Orientation allocation, in (++,-+,+-,--) order, is (6,1,1,6). The cross nodes are (7,7), and both same-sign supports are

    {6,7,12,13,17,19}.

All beta values are 1; all fourteen denominators are nonzero. Every bank matrix is nonzero. Each orientation/alpha pair is distinct, so the listed nodes are effective.

Independent checks passed:

- 154 newly computed literal branch inverses;
- 308 left/right inverse-product identities;
- all 154 raw phase weights reconstructed and compared;
- all fourteen bank matrices reconstructed from the literal inverses;
- every bank reconstructed a second way from word-counted Weyl coefficients;
- all eleven full-sector linear equations checked, with ranks 11,8,10,11,11,11,11,11,11,10,8;
- all 121 entries of the aggregate equal the literal target exactly;
- all supplied target, bank and branch matrices agree with the independent reconstruction.

The bank matrices and raw weights are retained in `LITERAL_WITNESS_CHECK.json`; all literal inverse matrices are retained in `LITERAL_BRANCHES.json`.

## 3. Why the lower bound permits different cross nodes

For any legal representation in the declared architecture, let y be its sole effective (-,+) alpha and z its sole effective (+,-) alpha. They are separate variables.

The coordinate (10,1) is supported only by (-,+), and its target coefficient is nonzero. Consequently y cannot be zero. Likewise z cannot be zero after reflection.

For b=1,...,5, the coordinate (11-b,b) is supported only by (-,+). Grouping the sector amplitudes of equal-alpha banks forces the normalized amplitude

    T_b(y)=1/[y^b G_-+(11-b,b)].

For b <= a <= 10-b, both negative-delta orientations have zero coefficient. The remaining ++ moments are therefore

    v_b(a;y) = [13^(3(a+b)^2)-T_b(y)y^(11-a)G_-+(a,b)]/G_++(a,b)
             = sum_(x in X) A_(b,x)x^a,

where X is the distinct nonzero effective ++ support. All relevant Gaussian denominators are nonzero, as independently checked. The legal bank's arbitrary beta factors, raw weights and Delta denominator are contained in its amplitude A_(b,x). This derivation divides by neither beta nor any same-sign alpha. A zero-alpha bank contributes zero to these positive-exponent windows. Repeated physical banks at one alpha are merged only for necessity bookkeeping and still count as actual summands.

If |X|<=5, either of two ordinary-node padding arguments yields a degree-five annihilator:

- pad X to any five-element subset of the 22 nonzero field elements and take its product polynomial; or
- multiply the support polynomial by t^(5-|X|).

Both obey all four length-six windows of b=1 and both length-six windows of b=2. The complete monic degree-five affine census below excludes both possibilities.

The reflection J e_t=e_(-t) sends (epsilon,delta) to (-epsilon,-delta), preserves alpha, beta and the phase convention, and leaves F invariant. Applying the same all-y proof to the reflected representation, with its independently chosen parameter z, gives the identical bound for --. No step sets y=z. Each cross-sign effective group requires at least one actual bank. Therefore six required ++ nodes plus six required -- nodes plus the two cross-sign groups imply at least 14 actual banks.

## 4. Complete all-22 degree-five exclusion

The independently derived coefficient matrix has rank five for every nonzero y. Twenty augmented systems are inconsistent. Exactly two monic solutions exist, with coefficients listed in increasing degree:

- y=4: (6,4,18,1,8,1), with no nonzero F23 roots;
- y=15: (14,1,14,17,12,1), with only roots 3 and 21.

Both constant coefficients are nonzero. Thus neither polynomial is a padded lower-degree support polynomial, and neither has five distinct nonzero roots. No y admits five or fewer nonzero ++ support nodes.

The full independent affine solutions, ranks, row reductions, moments and roots are in `INDEPENDENT_MOMENT_CENSUS.json`. They match every corresponding candidate record exactly.

As a genuinely different exhaustive check, the reviewer enumerated every one of C(22,5)=26,334 five-element nonzero node sets, constructed each product polynomial directly, and tested it against each of the 22 moment gates. All 579,348 set/parameter tests failed. This support enumeration independently certifies the ordinary-node exclusion, rather than only comparing two row-reduction implementations.

The matching literal witness proves the upper bound, completing equality14 in the same domain.

## 5. Accepted six-node necessary classification

For every y, the degree-six system has rank four and affine dimension two. The reviewer enumerated every one of its 23^2 members, for a total of 11,638 sextics, and evaluated each at all 22 nonzero field elements. Exactly three have six distinct nonzero roots:

- y=7, support {6,7,12,13,17,19}, coefficients (20,20,8,21,6,18,1);
- y=10, support {1,2,4,11,13,18}, coefficients (7,5,0,4,9,20,1);
- y=12, support {3,12,14,15,16,19}, coefficients (11,21,21,18,18,13,1).

A second independent enumeration considered all C(22,6)=74,613 six-element supports and all 22 parameter values: 1,641,486 tests. It found exactly those three records. The two enumeration methods agree.

Any fourteen-bank representation in this architecture must therefore have y and z each in {7,10,12}, using the corresponding displayed same-sign support. The equal pair (7,7) is a fully verified sufficient construction. No sufficiency conclusion is drawn for the other eight ordered support pairs; they were not tested in this review. Passing a recurrence gate alone does not represent all bank sectors.

If one of y,z is outside {7,10,12}, the same argument requires at least 15 actual banks. If both are outside that set, it requires at least 16. These additional necessary bounds do not provide attainment for arbitrary pinned pairs.

## 6. Mutation controls

Twenty-four deterministic rejection controls passed, including:

- perturb one raw phase weight;
- remove the 1/11 normalization;
- reverse the target Fourier exponent;
- delete each of the fourteen actual banks separately;
- reverse every branch phase sign while preserving the weights;
- allow alpha=0,beta=1 despite its zero denominator and singular literal branch;
- allow a zero cross alpha at the sole-support coordinate;
- claim a degree-six support gate at y=4;
- replace root 6 by 1 in the y=7 support;
- change a ++ bank to -+, creating a second independently detected effective cross node;
- corrupt one entry of a branch inverse.

Every control is recorded in `MUTATION_CONTROLS.json`. These are falsification checks, not a proof of unrestricted optimality.

## 7. Reproduction, timing, hashes and boundaries

The archive retains the fresh reviewer source, original input hashes, candidate data needed to replay, exact arithmetic outputs, timing, cold-replay comparisons and file hashes. Run the newly authored reviewer from the extracted archive with:

    python3 -I free_singleton_review/independent_review.py

It expects the bundled sibling `free_singleton_candidate` input directory. Its candidate program is inert evidence and is never invoked. The full cold replay takes only a few seconds; exact timings are retained rather than inferred from the conversation. Model-token usage is unavailable. No arithmetic errors were recorded.

This closes the requested independent finite gate. It supports exact free-singleton minimum14 and the three six-node necessary gates. Unrestricted allocations, other fields or primitive roots, all remaining support-pair compatibility, novelty and runtime superiority remain outside this verdict.
