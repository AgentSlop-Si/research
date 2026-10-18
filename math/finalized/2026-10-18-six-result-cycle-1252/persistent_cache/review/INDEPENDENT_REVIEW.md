# ALG-070 independent review: paid persistent complete-view cache

Date: 18 October 2026. Candidate: `alg070_persistent_cache_20261018_1244`.

## Verdict

**QUALIFIED PASS at the restricted uniform-cost immutable complete-view tariff scope, with the mandatory accounting clarification below. Retain ALG-070 open.** The classical paging upper bound and matching equal-capacity deterministic lower bound are correctly realized in the expressly required complete-vector recipe grammar. This is an attributed reduction/application with an explicit convolution realization and accounting boundary, not a new paging theorem, unrestricted convolution lower bound, engineering performance result, or closure of the larger comparator gate.

### Mandatory release clarification

Preserve the candidate's original bytes and publish this clarification prominently with its result summary:

> In Section 6, the lower-bound comparator is the full declared tariff Total_OPT_K = G + F times its number of materializations. Equations (3)–(5) do not establish the same lower bound against a comparator whose additional scheduler, planning or runtime cost has been added without an upper bound. Such extra comparator work must be included in the denominator or in a justified common per-request charge. The result is a declared-tariff theorem, not a machine-runtime ratio.

This is an accounting/notation qualification. No algorithm, mathematical inequality within that tariff model, or executable checker needs correction. Extra comparator scheduling cost still only helps the separate upper bound (4). The candidate's original Section 6 already identifies the comparator tariff as G+Fo; this explicit qualification prevents a wider reading of its Total notation.

The final candidate file hashes are recorded in `CANDIDATE_BINDING.json`. The review is independent of the candidate's proof checker: `independent_checks.py` imports no candidate code. An isolated replay of the reviewed candidate checker is recorded separately.

## 1. Mathematical checks

### Upper bound and empty initialization

For online capacity K and comparator capacity h, 1 <= h <= K, the rank potential proves

    (K-h+1) a_LRU <= K o_OPT.

At an offline load the potential increase is at most K. At an online hit it does not increase; at a miss it decreases by at least K-h+1 because the requested view belongs to the comparator cache. Several absent comparator views can all have rank K+1; this does not invalidate either the update bound or the minimum h(h+1)/2. The independent checker explicitly includes up to four absent views, whereas the candidate's transition enumeration used K+1 total labels.

Padding with shared dummies placed in LRU's first h positions gives the minimum initial potential, so the exact inequality needs no additive initial-cache allowance. Retaining an otherwise prematurely discarded view until replacement is harmless, and each speculative comparator load is charged. There is no assumption that the offline policy is LRU or that prefetch is free.

Consequently the equal-capacity factor K and resource-augmented factor K/(K-h+1) hold for optional materialization tariff. Substituting K=2h-1 gives 2-1/h, including factor one for h=1. This augmentation spends h-1 additional full N-entry slots. It is not available under an unchanged total-memory budget.

### Lower bound and phase certificate

The fixed universe has K+1 views. For each fixed deterministic online policy, choose each next request outside its currently retained K-slot cache, after any finite paid speculative activity. The policy performs at least T materializations on T requests. Infinitely many speculative loads already give unbounded optional cost.

The maximal-at-most-K-distinct phase partition is valid. Every nonfinal phase has K distinct labels and at least K requests. Fill a shorter final phase to K labels. Any two K-subsets of a K+1-element universe differ by at most one member, so an offline schedule pays at most K initially and one load per phase transition. Thus its loads are at most K+floor((T-1)/K). This bound uses the K+1 universe essentially; it must not be asserted for arbitrary larger universes.

For every c<K, the difference between online cost and c times this feasible offline cost grows without bound as T grows. Therefore no sequence-length-independent additive constant repairs a smaller factor. The comparison is asymptotic and not an assertion that every finite prefix has ratio K.

### Fixed versus adversarial data

The ring, N, A, B, all K+1 kernels, materialization recipes, F, and raw storage are fixed before the adversarial request construction. The request sequence may depend on the deterministic policy. Once that policy is fixed, the adaptive procedure determines a concrete worst-case sequence. This does not provide one sequence that defeats all policies, a randomized oblivious-adversary lower bound, or a lower bound inferred from unrealisable generic MTS task vectors.

For a fully explicit realization, take rational/integer coefficients, N>=2,

    A=(N,1,...,1), B=e_0,
    H_i[j]=1+(i+1)^(j+1), 0<=i<=K.

The cyclic convolution matrix of A is (N-1)I+J, with determinant (N-1)^(N-1)(2N-1), hence invertible. Every H_i is dense and distinct; so are A*H_i. For N=4, K=2, the checker obtains determinant 189 and vectors (14,14,14,14), (43,49,61,85), and (136,154,208,370). These are actual instances of the owner's filtered-bilinear target (A*B)*H.

This example also exposes the scope honestly: A*H[t]=sum(H)+(N-1)H[t] admits a cheap algebraic recipe. Mandatory equal-price full-loop materialization, not algebraic hardness of these inputs, forces the paging charge. The candidate already declares this restriction. A realization of the service contract is not a reduction proving every convolution evaluator must pay F.

## 2. Comparator and accounting audit

The reviewed comparison requires all of the following:

- Immutable, exactly identified view handles and identical raw inputs/backing-store availability on both sides
- K or h equal-size complete N-entry materializations, with no persistent partial, compressed, cross-view, scalar-output, or scratch-cache substitutes
- The same positive known tariff F for every allowed build, including arithmetic, reads, writes, replacement and required scratch handling
- Mandatory full materialization on an active miss, even for one requested coordinate
- Both real caches initially empty; no free warming, prefetch, preparation, conversion or admission
- Exact normalization/coalescing work, retained raw versions, outputs and common preparation charged in G; no free hash-collision equality or canonicalization of arbitrary circuits
- A certified common tariff, not unknown policy-dependent runtime learning

These are explicit restrictions, rather than consequences of the filtered-bilinear formula. Variable products may be registered view contents when they satisfy the same certified tariff contract. This does not give a uniform cheap implementation for all arbitrary-depth expression DAGs, nor compare algebraic evaluation strategies inside such views.

Paid +delta/-delta normalization can return to an old handle, preserving a cached old materialization. The paging theorem applies to any such normalized handle sequence. Zero-output requests are ingested and charged but omitted from the active paging sequence. The proof does not inherit the older event-count monotonicity assumption.

The full declared tariff upper bound is

    G + F a_LRU + E_LRU <= c (G + F o_OPT) + E_LRU,
    c=K/(K-h+1).

The explicit O(KT) bookkeeping bound is in handle-comparison/index operations, not constant bit time for unbounded handles or exact rationals. Extra comparator scheduling charges can only help this upper inequality.

For G=G_0+gT, the lower bound against the tariff comparator is

    liminf (G+F a_A)/(G+F o_OPT) >= (F+g)/(F/K+g).

Extra nonnegative online scheduling work does not weaken it. Extra comparator scheduling work requires its own upper bound or inclusion in the denominator/common charge; it cannot silently be added to the comparator while retaining the same lower-bound expression. This notation point was raised during review. The candidate bytes remain unchanged; the mandatory release clarification above supplies the explicit denominator qualification. No actual machine-runtime lower bound is accepted.

For fixed N and positive g, increasing T alone gives the displayed diluted factor, not K. Approaching K requires a family with F/g tending to infinity. The direct-loop tariff grows quadratically in N and full output linearly in the stipulated arithmetic model, so that family exists. This is not a bit-complexity claim. The cold term G_0 is fixed for each instance before taking the long-sequence limit.

## 3. Exact counterchecks against overextension

The independent artifact includes numerical and algebraic witnesses that fail if the restrictions are dropped:

1. **Unequal build prices.** With capacity two, prices (1000,1,1), and sequence (0,1,2,1) repeated twenty times, weighted LRU costs 20,021 while the exact offline optimum costs 1,040. The ratio 20,021/1,040 exceeds two. Equal build prices are essential to this LRU theorem.
2. **Partial coordinate caches.** For K=2, N=4 and 300 cyclic requests to three view handles, a simple arithmetic/write tariff gives mandatory full-build LRU cost 9,900. Storing three requested scalar answers costs 324 including all 300 outputs. Three scalars fit within the nominal eight scalar full-cache budget. The ratio is 275/9. This is an escape from the grammar, not a counterexample within it; these deliberately simple arithmetic tariffs illustrate the representation gap rather than physical runtime.
3. **Large mandatory outputs.** For K=4, F=4 and g=100, the asymptotic tariff lower bound is 104/101, far below four. Common work must not be erased.
4. **Hidden scratch slot.** Three actual complete slots serve the same 300-request three-view cycle with only three builds. A nominal K=2 guarantee cannot ignore a persistent extra scratch view.
5. **Free initial cache.** A first request to a warm comparator's retained view costs it zero loads and an empty online cache one. The no-additive exact inequality requires the stipulated compatible initialization.
6. **Coordinate aliasing.** A=(2,1), H_0=(2,1), H_1=(1,3) give distinct full outputs (5,4) and (5,7), but the first coordinate is always 5. Distinct full views do not establish distinct or hard selected-coordinate queries. Mandatory handle-specific full materialization is therefore essential even without scalar caching.

The cheap full-convolution identity in Section 1 is a further explicit arithmetic-shortcut check. These counterchecks support retaining the broad ALG-070 gate open.

## 4. Independent finite evidence

All exact checks passed:

- 9,764 request sequences, including all shorter lengths and empty sequences in the tested domains
- 77,359 equal/unequal-capacity competitive inequalities
- 9,761 offline phase certificates
- 1,789 comparisons of a demand-only eviction oracle to a separate arbitrary-subset paid-prefetch Bellman oracle
- 37,114 potential request transitions, 209,068 offline-load transitions, and 7,090 minimum-potential checks for K up to eight and universe K+4
- 64 explicit rational/integer convolution families, 1,936 coordinate checks, and exact determinant/distinctness controls
- 32 adaptive traces including a policy that performs paid speculative reloads
- 63 exact cancel/restore controls, 189 requested answers, and explicit zero-output filtering, with 4,194 charged version comparisons and 882 stored raw scalar slots in that test
- Six rejected extrapolations/accounting escapes as described above

Finite tests are corroboration. The proofs establish arbitrary-sequence claims. The author checker was also replayed in an isolated copy, and its output validation file matched the candidate's committed validation bytes; see `AUTHOR_REPLAY.txt` and `REPLAY_BINDING.json`.

## 5. Attribution and final disposition

Primary-source verification: Sleator and Tarjan, *Amortized Efficiency of List Update and Paging Rules*, Communications of the ACM 28(2), 202–208 (1985), Section 4, Theorems 5 and 6, printed pages 207–208. The author-hosted PDF was opened independently: https://www.cs.cmu.edu/~sleator/papers/amortized-efficiency.pdf . The classical deterministic lower bound, LRU unequal-capacity bound, and initial-state qualification support the attribution. The present candidate supplies its own exact empty-start proof and declared convolution-view contract. No historical novelty is accepted from restating these results.

Accept only the paid uniform immutable complete-view comparator: equal-capacity deterministic factor K, LRU factor K/(K-h+1) with resource augmentation, actual filtered-bilinear realization within that grammar, and common-cost dilution/accounting. Preserve prior accepted fixed-filter/event-list results.

Keep ALG-070 open for nonuniform prices, flexible partial/compressed states, certified sharing, state-dependent/asymmetric conversions, changing memory, paid policy-dependent learning, and numerical/bit/runtime qualification. No status, priority, identity, census, spreadsheet, or repository change was made by this review.
