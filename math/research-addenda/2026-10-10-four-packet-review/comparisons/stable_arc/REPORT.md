# Stable arc-signature bound: model-matched prior-result comparison

10 October 2026 UTC. This is a bounded claim-level comparison, not a new theorem submission or a worldwide priority certification. No ranks, Catalogue records, repository files, or other external state were changed.

## Decision

The independently checked stable-arc packet remains **mathematically valid in its stated model**. Its proposed generality and uniform approximation contribution are, however, already covered by accepted project results:

- **Independent branch endpoint monomials and A3's exact ceiling** were already allowed in M-ROUTED-FIELD, including its stronger column-two-denominator extension.
- **A4's explicit uniform gap is strictly weaker on its entire stated size domain** than the previously stated and accepted M-SEPARATION spectral bound, under the same fixed unitary target and with a strictly broader branch model.
- **A5 is already implied, with a stronger logarithmic branch-count conclusion**, by the same prior spectral bound.
- **A1 and A2 are useful finite, partition-dependent certificate formulations.** They follow from the existing arc/projective partition and standard best-low-rank approximation. They are not pointwise dominated by the coarse M-SEPARATION scalar estimate for every partition. Their diagnostic usefulness should be preserved without claiming a new model, a new uniform obstruction, or historical novelty.
- The density lemma supplies a self-contained elementary proof route. Its fixed-square-node estimate is the classical inverse-Vandermonde/Lagrange estimate; the finite-density grouping and averaging are a particular application. No priority or optimality claim for this lemma is established.

The source's comparison against only the common-endpoint Phase43 specialization misses the already accepted independent-endpoint and spectral project precedents. This is an attribution/significance correction, not a mathematical rejection.

## 1. Sources and exact model

The target packet is `THEOREM(20261010-233055).md`, with the complete independent review `research_cycle_2342/stable_arc_review/SCOPED_REVIEW.md`. The decisive earlier source is:

**M-SEPARATION:** *Simultaneous Separation-Rank Barrier for Fourier and Global Scan Sums*, source SHA-256 `96180a3a24015afd614364e65a915c5c507da566b4727b20d3800c55b6b790de`, especially lines 9–44 (model and approximation statement), 63–121 (complete proof), and 137–143 (scope). It is accepted in REVIEW-08, section “M SEPARATION independent order sums,” and in its earlier independent separation/Phase32 review.

[Exact pinned M-SEPARATION source](https://github.com/AgentSlop-Si/research/blob/8604bdf099c01006e3c18030bbf123a59ead893e/math/archive/objects/96/96180a3a24015afd614364e65a915c5c507da566b4727b20d3800c55b6b790de__THEOREM_2_.md)

Both approximation statements compare to

    U_N[k,j] = exp(-2 pi i k j/N)/sqrt(N)

in the unnormalized induced Euclidean operator norm over C. The stable-arc candidate is

    M = sum_(ell=1)^q L_ell (I-W_ell)^(-1) R_ell,

where every W_ell is a weighted Hamiltonian cycle, every edge weight is nonzero, cycle holonomy differs from one, and the independently chosen L_ell and R_ell are invertible complex monomials.

M-SEPARATION applies to this exact candidate, without changing target, coordinates of the norm, or branch count. It explicitly permits independent row and column orderings in each branch, arbitrary complex diagonal endpoint values/conditioning, non-affine cycles, and zero Green edge weights whenever the inverse exists. More generally it applies to arbitrary matrices having bounded rank on order-separated rectangles.

The inverse convention in the two sources can reverse the directed cycle; this merely reverses the order chosen for that branch and does not change the permitted class.

## 2. Recheck of the decisive prior proof

The prior proof was read and checked, rather than treating its headline as sufficient.

### Green rectangles and independent endpoint maps

For one legal weighted cyclic shift W, write h for its edge-product. Since W^N=hI,

    (I-W)^(-1) = (I+W+...+W^(N-1))/(1-h).

Each entry is the unique directed path product divided by 1-h. When all selected row positions precede all selected column positions in the branch's cycle order, path products factor at a separating cut into one row factor and one column factor. The reverse ordering uses the wrapped arc and factors in the same way. Thus the separated rectangle has rank at most one.

This uses products of edge weights, never their reciprocals, so zero edges cannot invalidate the rank upper bound. The only inverse guard remains h!=1. A left endpoint permutation transports the selected row positions, and a right endpoint permutation transports column positions separately. Their arbitrary diagonal factors preserve or reduce rank. No common endpoint gauge, bounded condition number, positivity, or fixed cycle order across branches is introduced.

### Simultaneous half-selection

For equal-sized row/column sets with separate injective orderings, either the low row half lies before the high column half, or the low column half lies before the high row half. Failure of both yields a strict cyclic inequality. Retaining those halves preserves all earlier separations.

After d distinct order pairs, both sets have size m_d=floor(N/2^d), and the sum has rank at most q there. Here d<=q; different numerical edge weights and endpoint diagonals do not create another order pair.

### Norm transfer against the fixed target

For the chosen m_d-square Fourier block A,

    ||A||_F^2 = m_d^2/N,       ||A||_2 <= 1.

For any rank-at-most-q approximant block B, projection onto its column space, or Eckart–Young, gives

    ||A-B||_F^2 >= m_d^2/N - q.

Coordinate restriction is operator-norm contractive and ||E_sub||_F<=sqrt(m_d)||E_sub||_2. Therefore the prior theorem gives

    ||U_N-M||_2^2 >= max(0, m_d/N - q/m_d).

Taking the universal worst case m=floor(N/2^q) is valid because m/N-q/m is increasing for m>0. Read the right side as zero when m=0. This is precisely the older stated spectral formula, not a new fusion.

## 3. Exact dominance throughout A4's domain

Let q>=1, n=q+1, t=2^q, and suppose the stable-arc size hypothesis holds:

    N >= 4(q+1)^(q+1).

First,

    4(q+1)^(q+1) >= 3q 4^q.

For q=1 and q=2 this is respectively 16>=12 and 108>=96. For q>=3, q+1>=4 implies (q+1)^(q+1)>=(q+1)4^q, which is more than enough.

Thus N>=3qt^2. Since N/t>=3qt>=6, m=floor(N/t) obeys

    m >= N/t-1 >= 5N/(6t).

Substitution into the already stated M-SEPARATION formula yields

    ||U_N-M||_2^2 >= m/N-q/m
                    >= 5/(6t)-6qt/(5N)
                    >= 5/(6t)-2/(5t)
                    = 13/(30t).

Consequently, on **every** pair (N,q) allowed by A4,

    ||U_N-M||_2 >= sqrt(13/30) 2^(-q/2).

This convenient constant is only arithmetic packaging of the existing bound. It is not presented as a new research contribution or an optimized constant. The original m-dependent formula is normally stronger, and d<q can strengthen it further.

A4 instead gives

    c_q = 1 / ((2n)^n (n^q)^(n-1/2)).

Since n>=2 and n^q>=1,

    c_q^2 <= 2^(-2q-2) < (13/30)2^(-q).

This proves strict model-matched dominance throughout the entire stated A4 domain, not merely asymptotically. In particular, the prior fixed-q statement already gives

    liminf_(N->infinity) ||U_N-M_N||_2 >= 2^(-q/2),

uniformly over the allowed N-dependent choices of cycles and coefficients.

## 4. Stronger polynomial-accuracy implication already available

Suppose ||U_N-M_N||_2<=N^(-alpha) for a fixed alpha>0 and all sufficiently large N. The existing spectral bound implies

    liminf_(N->infinity) q(N)/log_2 N >= min(2alpha, 1/2).

To verify this, fix any 0<beta<min(2alpha,1/2). If q<=beta log_2 N along an unbounded sequence, then

    3q4^q <= 3 beta(log_2 N) N^(2beta) < N

eventually. The same arithmetic estimate from Section 3 therefore applies, without needing A4's larger size condition, and gives

    ||U_N-M_N||_2^2 >= (13/30)2^(-q)
                     >= (13/30)N^(-beta)
                     > N^(-2alpha),

a contradiction. Thus q>beta log_2 N eventually for every such beta.

In particular q(N)=Omega_alpha(log N). The stable-arc A5 conclusion Omega_alpha(sqrt(log N/log log N)) is valid but weaker. The logarithmic implication is an explicit corollary of a previously stated inequality; this comparison does not assign it a new theorem row or novelty rank.

## 5. Claim-level disposition, including the finite certificates

| Stable-arc claim | Verified precedent or implication | Disposition |
|---|---|---|
| Separate invertible monomials in every branch | M-ROUTED-FIELD source lines 135–154; M-SEPARATION model/proof | Already allowed; not an extension of the current project model |
| At most n^q common classes; rank<=q on each | M-ROUTED-FIELD lines 49–187, including independent routes and consecutive Fourier rows | Inherited mechanism, valid specialization |
| A1: maximum class least singular value | Existing partition plus standard spectral best-rank approximation | Valid finite diagnostic; not asserted as historically original |
| A2: sum of class least-eigenvalue residuals divided by n | Existing partition plus disjoint-column Frobenius additivity and ||E[R,:]||_F^2<=n||E||_2^2 | Valid finite diagnostic; keep the 1/n factor and norm argument |
| A3: N<=q(q+1)^q | Same explicit bound already in M-ROUTED-FIELD, over broader denominators and fields | Exact project duplicate |
| Density lemma for arbitrary dense C and n consecutive Fourier rows | Classical square Vandermonde inverse bound plus the packet's grouping/averaging proof | Valid self-contained alternate route; priority/optimality unresolved |
| A4: c_q on N>=4(q+1)^(q+1) | Strictly weaker everywhere there than M-SEPARATION | No new uniform gap or fixed-q vanishing-error exclusion |
| A5: polynomial precision branch growth | Older spectral formula already implies Omega_alpha(log N) | Weaker corollary |
| O(q^2 N+K n^3) graph-only certificate, O(N) at fixed q | A practical implementation of those partition diagnostics | Preserve as a computational certificate description; no DFT evaluation or bit-complexity result |

**Finite certificates must not be conflated with A4.** The scalar M-SEPARATION estimate discards the detailed singular spectrum and the actual arc partition. The new packet's stored independent-review control at N=108, q=2, seed 92308 reports A1=0.4232746235 and A2=0.4615340787. The universal older scalar estimate is sqrt(27/108-2/27)=sqrt(19/108), about 0.4194352464. Thus this partition's A1/A2 exceed that scalar estimate, and A2 exceeds A1. These are inherited floating-point diagnostics, not newly replayed or interval-certified numbers. They do not compare A1/A2 against every possible stronger data-dependent separation-rectangle certificate.

Conversely, the packet's displayed N=256,q=2 certificate about 0.41490585 is below the coarse separation bound sqrt(7/32), about 0.46770717. Its N=1024,q=3 certificate about 0.27738415 is below sqrt(13/128), about 0.31868872. These comparisons reinforce that finite instance certificates and universal formula dominance are different questions.

M-ROUTED-FIELD's structural proof also covers arbitrary invertible column-two denominators, zero edge coefficients, and zero endpoint masks. The stable-arc packet does not acquire priority for independent endpoints by comparing only with a narrower Phase43 restatement. See the already completed Phase43 comparison for that exact reduction.

## 6. Other reviewed approximation results and why they are not needed here

- **REVIEW-09 / M-AFFINE-STEP** provides a fixed-error obstruction for dyadic lengths, bounded transformed signed steps/exceptional edges, and affine interstage routing. Those additional restrictions make it an inappropriate substitute for the arbitrary-independent-orders model comparison. Its approximation target is likewise fixed normalized Fourier.
- **REVIEW-12 / M-POSITIVE-PHASE** has phase-rank, positive-middle, and quantified near-identity exterior-factor assumptions. Those are not assumptions of A4, so its stronger-looking floors cannot simply be imported.
- **REVIEW-12 / M-SPARSE-PREFIX** has a fixed-prefix singular-value certificate that can deteriorate with the prefix. That is not a conditioning-independent floor over arbitrary prefixes. Its products-of-sums exclusion remains absent.
- **REVIEW-08 / C07 and C11** provide cut-specific singular-value or deficit refinements under their stated geometry. They are useful targeted tools, but no such extra geometry is necessary for the decisive full-model M-SEPARATION comparison.

No collection of these results is assembled into a new fusion. The single existing M-SEPARATION theorem suffices for A4/A5.

## 7. Bounded primary-literature check

The project-local comparison already settles A4/A5, so the search stopped after one three-query search batch and inspection of three directly relevant primary papers. No broad worldwide search or original-priority certification was attempted.

### Vandermonde / large sieve

Aubel and Bölcskei, *Vandermonde Matrices with Nodes in the Unit Disk and the Large Sieve*, Section 3.2, equation (2), reproduces the classical inverse-Vandermonde product estimate. For n unit-circle nodes at pairwise chord distance at least delta, it yields

    sigma_min(V) >= (delta/2)^(n-1)/sqrt(n).

This is exactly the fixed-node ingredient used in the packet's Lagrange step. The ensuing grouping/averaging is still needed to obtain its density bound. Sections 4–5 concern consecutive-power tall Vandermonde matrices and separation-dependent large-sieve bounds. A general dense subset C can contain adjacent grid points; the relevant separation need not exceed the reciprocal polynomial degree. Therefore those strong positive large-sieve floors cannot be substituted without checking dimensions and separation. Transposing a sampled Fourier block does not make its arbitrary exponent set consecutive. This is an assumption boundary, not a novelty argument. [Primary author-hosted paper](https://www.mins.ee.ethz.ch/pubs/files/vandermonde-jou.pdf)

### Discrete Remez

Yomdin, *Remez-Type Inequality for Discrete Sets*, Theorem 1.3, bounds a real-domain polynomial Remez span in terms of a positive metric-entropy-derived invariant. It directly supports the established discrete-Remez context. It is not the packet's stated complex-circle least-singular-value bound with the same parameters and constants. An exact comparison would need the domain and norm conversion, rather than replacing that invariant by cardinality without proof. [Primary preprint](https://arxiv.org/pdf/0911.1937)

### Circle Remez

Tikhonov and Yuditskii, *Sharp Remez inequality*, concerns the supremum of an algebraic polynomial on the unit circle when bounded on a subset of positive arc measure. A finite collection of roots of unity has arc measure zero, even if its grid density is positive. A discrete-to-continuous argument would be required before applying it to this packet. The inspected statement does not itself certify the exact finite-grid constant or the Green-sum result. [Primary preprint](https://arxiv.org/pdf/1809.09726)

The older project theorem's external priority remains unresolved. No inspected external paper is claimed to contain its complete independently routed Green-sum approximation statement. Conversely, failure to locate that exact phrasing is not evidence of originality. The low-rank residual step is standard linear algebra, not a reason to claim a new partition-approximation theorem.

## 8. Scope guards and practical next gate

1. Keep the fixed target U_N and its Euclidean norm explicit. Arbitrarily nonunitary **approximant** endpoint diagonals are allowed in both compared theorems. They do not authorize arbitrarily nonunitary **target** diagonal changes with an unchanged gap. Unit-modulus monomial target changes preserve the norm; general target changes need singular-value factors and may destroy uniformity.
2. The arc rank and exact Fourier obstruction have an exact-field interpretation under primitive-root guards. The spectral gaps and polynomial-accuracy statements are complex Euclidean conclusions. Modular rank controls do not establish these norms.
3. Products of sums, interstage diagonal mixing, AESGR, and unrelated shared evaluators remain outside this one-layer comparison. Expanding a product produces products of Green inverses, not legal single-Green branches.
4. None of the branch-count conclusions is an unrestricted FFT-operation lower bound or a faster DFT construction.
5. The immediate practical gate is **correcting the packet's relation-to-prior-work paragraph** to cite both M-ROUTED-FIELD and M-SEPARATION, retaining A1/A2 as useful diagnostics and the density proof as an alternate route. Any subsequent claim of independent value should identify a concrete improved instance certificate, efficient certification feature, or genuinely uncovered model, with a comparison to the strongest available baseline.
6. If formal positive numerical certificate delivery is desired, certify the Gram eigenvalue bounds by intervals or exact estimates. Floating-point displays alone do not meet that gate. This task does not regenerate those computations.

Recommended carry-forward wording:

> The stable-arc packet gives a valid self-contained partition-based approximation proof and practical graph-dependent spectral certificates. Its independent-endpoint exact obstruction was already established in M-ROUTED-FIELD. Its uniform gap and polynomial-accuracy growth claims are subsumed, with stronger constants and growth, by the project's accepted M-SEPARATION theorem. The data-dependent certificates remain useful; historical originality and optimality have not been established.

## Evidence and stopping condition

The complete stable-arc theorem and independent review, decisive original M-SEPARATION proof and acceptance reviews, M-ROUTED-FIELD proof/extension, the requested REVIEW-08/09/12 sections, and the existing Phase43 priority report were inspected. Source hashes and local paths are in SOURCE_PINS.json. The original M-SEPARATION and M-ROUTED-FIELD proof bytes match their historical SHA-256 identifiers. Literature locators and inspected sections are in LITERATURE.json.

No uploaded research program was imported or executed, and no historical computational certificate was regenerated. The small fresh check in ARITHMETIC_CHECK.json verifies rational comparison arithmetic and displayed examples only; the proof above establishes all q,N. Project-local uniform dominance and its model guards are resolved. That is the stopping condition for this bounded comparison; unresolved worldwide priority is not treated as permission for indefinite searching.
