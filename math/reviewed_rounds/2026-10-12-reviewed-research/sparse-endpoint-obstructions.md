Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: fe6c4fcf2fcc76bec7d1f06fc263a67376b167c3b79337550256105c0ec48005

---

# Independent scoped acceptance: scalar Green endpoint obstructions

Reviewed 12 October 2026 UTC. Verdict: **ACCEPT, within the exact two stated grammars**. The general sparse-endpoint matching upper remains open.

## 1. Accepted object and provenance

This verdict binds to candidate version 2, not an inferred filename or an earlier draft:

- THEOREM.md: SHA-256 `65dde91db7cb97abe32220c74cdd9ffbaa372a22dc186211f51124970c4149da`
- Candidate manifest: SHA-256 `59e312fecf1ea17c1314f522739453047ed8f3607e9452318f3ffdf527c5c83b`
- Candidate archive: `SPARSE_Endpoint_Quadratic_Obstructions_CANDIDATE_v2_2026-10-12.zip`, 40,865 bytes, SHA-256 `2fb3d8ea59e3f252a19e5b0f79742220295f47eae5bcda758dbcb44b8ffea829`

All 15 manifest-listed members were rehashed and checked for size; their archive bytes were independently compared with their sealed-directory bytes. The complete candidate is preserved under `candidate_v2/`, and its archive is included. Candidate and historical programs were never executed or imported. All executable controls in this review were independently written.

An initial draft said that a prime length permits only the dyadic divisor B=1. The review identified N=2 as an exception. Version 2 correctly says odd prime, and records that its N=2 reset B=2 plan has five endpoints, versus four for the optimal closed cycle. The repair does not change the theorem.

## 2. Exact model and accepted conclusions

The target is an N-by-N matrix T over a field. For N>=2, require every entry and every 2-by-2 minor to be nonzero. In particular, a totally nonsingular target qualifies. Let

    T = R (I-D S_M)^(-1) C,

where S_M is one scalar cyclic predecessor permutation, D is diagonal, the product of its weights is not one, C has M rows and N columns, and R has N rows and M columns. Coefficients, routes and support choices are fixed independently of the fresh input. Scalar endpoint cost means nnz(C)+nnz(R). There are no free dense pre/post transforms, nonlinear input-dependent choices, packed-vector operations, or extra interacting scans.

Accepted A: when every output has one nonzero read, the exact minimum is N²: nnz(C)>=N(N-1), nnz(R)=N. This holds for arbitrary latent length, order, padding and zero weights. Transposition and reversal of the latent order give the same result for exactly one injection per input column.

Accepted B: partition columns into q>=2 nonempty blocks, and require every output to use one independently correct masked target-row contribution per block. The exact minimum is N²+q: nnz(C)>=N(N-q)+q and nnz(R)=Nq. Interleaved marks, arbitrary unmarked vectors, noncontiguous blocks, singleton blocks and zero edges are included. The individual masked-contribution requirement is essential; arbitrary multiple reads with cross-block cancellation are outside this grammar.

Boundary: N=1 has minimum two endpoints, not one. N=0 is not in the claim. For the one-read model, requiring at least one zero edge raises the exact minimum to N²+1. More precisely, if z of the marked-to-marked gaps have zero weight product, the proof gives N²+z. This counts zero-product gaps, not the number of zero edges.

## 3. Independent proof derivation

### Cyclic gap counting

Set V=(I-D S_M)^(-1)C. Every latent row satisfies v_t=d_t v_(t-1)+c_t. Unrolling along any directed gap from a marked state u to the next marked state v gives

    v_v - alpha v_u = sum_h beta_h c_h,

with alpha the gap's weight product. The gap includes the destination forcing row and excludes the source forcing row. Thus all cyclic marked gaps partition every forcing row exactly once, including the wrap gap. Products beta_h require no division by a weight and remain valid when weights vanish. The residual's support is contained in the union of the gap's forcing supports, so its nonzero count is at most the sum of those forcing counts.

Two different target rows cannot be proportional. For any scalar alpha, their difference after relative scaling has at least N-1 nonzero coordinates: two vanishing coordinates would give a zero 2-by-2 minor. When alpha=0 there are N nonzero coordinates. In a one-read representation, each marked row is a nonzero multiple of its target row. Hence N distinct marks exist and M>=N, regardless of rank(T). Each of N cyclic gaps costs at least N-1 injections. This proves the endpoint lower bound.

Full rank must not be inferred from the weakened hypothesis. For example T_ij=a_i+b_j can have rank two while every entry and every 2-by-2 minor is nonzero. A fresh N=5 rank-two control attains 25 endpoints with M=31. The correct argument for distinct marked states is nonproportionality, as the final candidate states.

### Legal attainment, including cycle closure

Take M=N, V=T, R=I. On transitions into rows i=1,...,N-1 choose d_i=T_i0/T_(i-1)0. On the wrap choose d_0=T_01/T_(N-1)1. Each residual C_i=T_i-d_i T_(i-1) has exactly one zero. The product of weights is

    T_01 T_(N-1)0 / (T_(N-1)1 T_00),

which differs from one by the nonzero minor on rows 0,N-1 and columns 0,1. Thus the Green denominator is legal and the total is exactly N². Preserving the same column on every edge instead produces product one and is invalid; a fresh negative control detects this.

Any larger prescribed M can retain the same endpoint count by inserting homogeneous states and adjusting the last weight of each gap. The review explicitly verifies equality at N=7, M=10,007. A reset edge can instead be placed into the first marked row: that row needs N injections, the others N-1, giving N²+1 total. This also explains the difference from an open scan beginning at zero. Dropping the cyclic wrap gap or forgetting the initial reset forcing would give the wrong count.

### Masked blocks

For every nonsingleton block J, restricted target rows are pairwise nonproportional, so select N distinct marked states. For every singleton block select just one representative state. Marks from different blocks cannot coincide because they are nonzero and have disjoint supports. Selection is permissible even if other, unselected marked states lie between selected ones: their forcing rows remain charged in the larger gap.

A same-block gap costs at least |J|-1 at its destination. A cross-block gap costs at least |J|, because its source is zero on every destination-block coordinate. Summing the baseline over the selected marks gives N(N-q). A cyclic word containing q different block labels has at least q cross-block transitions. This proves the injection bound.

For equality, concatenate reset tours. A nonsingleton block's first target row costs |J| injections, and each later row preserves one fixed coordinate and costs |J|-1. A singleton uses one state x_j and N separately weighted output reads. Summing gives N(N-q)+q injections and Nq reads; the cycle product is zero. At q=N this gives N²+N, as it should. For q=1 the closed optimum reverts to Theorem A; the reset construction costs N²+1.

## 4. Fourier domain and composite guard

For prime p and an element omega of exact order p in a field, a Fourier 2-by-2 minor is a nonzero root factor times 1-omega^((i-k)(l-j)). Distinct rows and columns make this exponent nonzero modulo p. This elementary calculation suffices for both accepted theorems, including in positive characteristic. It does not claim that every larger minor of every prime finite-field Fourier matrix is nonzero.

Exact characteristic-zero controls in cyclotomic quotient rings check every 2-by-2 minor and the attaining construction at p=2,3,5,7,11,13. The primary complex Chebotarev theorem is not needed for this elementary specialization, although it underlies the separate historical totally-nonsingular Fourier claims.

Composite Fourier matrices do not satisfy the premise. Independently constructed complex dyadic closed tours have endpoint totals 14 at N=4, 50 at N=8, and 186 at N=16, each below N². Their exact injection counts are (2N²-2)/3 and their cycle weight product is a primitive root, not one. The N=4 Gaussian-integer certificate is also recorded explicitly. These controls rule out promoting the theorem to all Fourier lengths.

The supplied `block_tour_plan` was inspected as inert text. Its line 182 requires B to be a dyadic divisor of N. The balanced Θ(N^(3/2)) construction therefore has a divisor-supported domain; it is not a uniform prime-length upper. For odd prime N only B=1 is legal and it costs N²+N. N=2 has the separate B=2 reset case noted above. In composite block restrictions many Fourier rows share the same projective direction, which is exactly the premise failure that permits fewer marks.

## 5. Fresh evidence and scope of execution

All independent controls passed:

- 616 tight Cauchy cases over GF(1009), covering every row/column permutation at N=2,3,4 with nonzero read gauges
- 33 exact padded attainments and 33 exact zero-edge cases across N=2,...,12
- 220 arbitrary latent-vector, shuffled-mark and zero-edge cases, with exact reconstruction and per-gap accounting
- One equality case N=7, M=10,007
- One N=5 rank-two target satisfying the weakened premise
- 502 exact masked-block attaining constructions, covering all ordered column-size compositions with q>=2 at N=2,...,9
- 502 additional arbitrary interleaved block orders with padding and zero edges, checking each local gap and the crossing count
- Exact complex cyclotomic prime and composite checks described above
- N=1 and singular-denominator negative controls

The finite-field reconstructor independently solves the whole cyclic boundary equation, then checks all latent rows and read outputs exactly. No candidate checker is imported. These finite controls corroborate the proof and boundary handling; they are not an all-size proof, a performance benchmark or a reproduction of the original transform programs.

## 6. Classical overlap and novelty limitation

Boito and Eidelman's primary paper states the classical band-inverse/Green rank correspondence and develops quasiseparable inverse generators. That establishes adjacent classical structure, not this target-dependent exact endpoint optimization with arbitrary padding and a one-read or masked-block grammar. [Computation of quasiseparable representations of Green matrices, §2](https://arxiv.org/html/2308.02701v1#S2).

De Sa, Gu, Puttagunta, Ré and Rudra's primary paper distinguishes sparse product width from raw factor nonzero totals and connects the former to linear straight-line programs. Its Appendix B also discusses FFT factorizations and the prefix-sum example. This supports keeping endpoint counts separate from unrestricted arithmetic complexity; its multi-factor representation is not the single scalar cyclic inverse reviewed here. [A two-pronged progress in structured dense matrixvector multiplication, Appendix B](https://pmc.ncbi.nlm.nih.gov/articles/PMC6534155/).

These are targeted overlap checks, not an exhaustive priority search. No external-priority, novelty ranking or assessment-band promotion is justified. The recurrence and projective-distance ingredients are elementary.

## Scope and remaining work

Accept the scoped obstruction alternative as completed for the two named families. Keep `SPARSE-PREFIX::matching-upper` open for a general one-Green representation with unrestricted sparse endpoints. The remaining mathematical task is a legal fixed-coefficient O(N log N/log log N) endpoint family with construction/evaluation costs charged, or a stronger obstruction covering general multi-read mixed latent contributions. The present result gives neither.

The candidate's quadratic materialization cost is appropriate to its scoped optimal constructions. Scalar endpoint size, runtime of the explicitly charged evaluator, root/coefficient generation, sorting/indexing and bit/precision models remain distinct. No historical-priority conclusion is added.

The historical M-SPARSE-PREFIX result is a distinct inverse-preconditioned model T=P^(-1)H with per-row sparse inverse preconditioner, independent separation orders and additive rank budget. Its floor(N/(s 2^d))<=R conclusion, total-nonsingularity hypothesis and complex prime-Fourier specialization are unchanged; it must not be merged with this endpoint theorem.
