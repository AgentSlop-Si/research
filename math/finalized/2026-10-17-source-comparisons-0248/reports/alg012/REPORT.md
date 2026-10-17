# ALG 012 comparison with dyadic Ramanujan subspaces

Date: 2026-10-17. Owner: ALG-012, Galois-defect and conductor hybrid evaluator.
Pinned repository reference: `26eb7017276591988762f27e2d1c23e739bcf3e4`.

## Bounded conclusion

**Exact conductor-space overlap, with a qualified evaluator nonmatch.** The dyadic Ramanujan block and ALG-012's odd-frequency conductor block describe the same primitive-frequency information. More precisely, the retained conductor difference vector gives the Ramanujan coefficients by the explicit normalization `beta_j = r_j/N`. This identification does not imply that an arbitrary vector has a sparse signed-P5 defect or that its full Fourier output is inexpensive. The restricted algorithm still needs charged defect discovery, two dense anchors per conductor, sparse defect evaluations, recurrence edges, root preparation, and explicit output writes.

The source comparison stops here. It does not close the parent ALG-012 record, establish priority, resolve a general relative-field rank question, or alter ALG-052. No Frobenius comparison is repeated. The earlier owner wording about a relative-field rank formula is preserved as history rather than silently treated as a theorem about the signed-P5 evaluator.

## Primary source statement and precise locator

P. P. Vaidyanathan, [Ramanujan-Sum Expansions for Finite Duration (FIR) Sequences](https://systems.caltech.edu/dsp/PPVSquare.pdf), PDF page 3, section 4: equation (15) forms `G_q` from the first `phi(q)` circular shifts of the length-N repeated Ramanujan sequence. Equations (16)-(17) concatenate divisor blocks into an N-column matrix. Theorem 1 proves full rank; equation (20) identifies each block's span with the primitive q-frequency DFT columns using an invertible Vandermonde factor. Equations (21)-(22) and Theorem 2 give an arbitrary-vector expansion. Distinct divisor blocks are orthogonal. Equations (18)-(19) illustrate N=6; they impose no extra hypothesis. These are representation results; the cited section supplies no signed-P5 support test or matching complete cost ledger.

## Exact coordinate map derived for this comparison

The following is a direct algebraic specialization and normalization check, not an attribution of ALG-012's algorithm to the paper. Work over C. Let `N = 2^d`, with unnormalized transform

    X_K = sum_(n=0)^(N-1) x_n zeta_N^(Kn).

For a divisor `q = 2^a >= 2`, set `m = q/2`. Before its split, ALG-012's current vector is the alias sum

    v_j = sum_(t=0)^(N/q-1) x_(j+tq),       0 <= j < q,
    r_j = v_j - v_(j+m),                    0 <= j < m.

This description follows by induction through the successive pair sums. For odd `k`, the original frequency `K = (N/q)k` satisfies

    X_((N/q)k) = sum_j r_j zeta_q^(kj).

It has exact conductor q: `N/gcd(N,K) = q`. Each nonzero frequency appears at exactly one q; q=1 supplies DC. Because q is dyadic, the units modulo q are exactly its odd residues, and `phi(q) = m`.

Do not identify the coefficient vector r itself with a length-N time-domain projection. Its local anti-periodic embedding is `E_q(r) = (r,-r)/2`. The q-point DFT of this vector is zero at even k and equals the displayed evaluation at odd k. To obtain the correct original-N projection, repeat it N/q times and multiply by q/N:

    x_q(n) = (q/(2N)) r_(n mod q)           if n mod q < m,
             -(q/(2N)) r_((n mod q)-m)      otherwise.

The N-point DFT of x_q equals X on its conductor-q indices and vanishes elsewhere. The factor q/N is essential: repetition alone multiplies the surviving Fourier values by N/q.

Here the Ramanujan sum simplifies directly to

    c_q(n) = m          if n = 0 mod q,
             -m         if n = m mod q,
             0          otherwise.

Its first m shifts have disjoint paired supports. Comparing them to x_q gives

    x_q(n) = sum_(j=0)^(m-1) (r_j/N) c_q(n-j),
    beta_(q,j) = r_j/N.

Together with `beta_1 = X_0/N`, these coordinates reconstruct x. Thus there is an exact, invertible change of coordinates, and in the dyadic case the coordinates can be formed by paid linear-work pair-sum/difference preprocessing and scaling. An implementation can keep unnormalized r, as ALG-012 does, without actually computing the explanatory divisions by N. No scaling operations are added to, or removed from, its existing ledger.

The represented block still has m free coordinates. An O(N) computation of these dyadic coordinates is not an O(N) computation of their complete N Fourier outputs. Evaluating an arbitrary r at all odd roots remains the same m-output subproblem.

## Defect sparsity is an additional restriction

Set `V_q = C[z]/(z^m+1)`, and let `L_q = P_5-I`, where P_5 explicitly substitutes `z -> z^5` and reduces coefficients with signs. Its evaluation map to the m odd roots is invertible. Under this map, P_5 becomes the permutation `k -> 5k mod q` of the output indices. Consequently

    Eeval_q(L_q r)_k = Y_(5k mod q) - Y_k.

For q>=4, that permutation has two cycles, represented by 1 and 3; each has length q/4. Hence `dim ker L_q = 2`, including q=4 where both cycles are singletons. The q=2 conductor is handled separately and has one coordinate.

For a fixed allowed coefficient-defect support J, with `|J| <= S`, define

    U_J = { r in V_q : support(L_q r) is contained in J }.

Writing C^J for the coordinate subspace supported in J, linear algebra gives

    dim U_J = dim ker L_q + dim(im L_q intersect C^J)
            <= min(m, 2+|J|) <= min(m, S+2).

This is a support restriction on the signed coefficient difference, not a restriction to one scalar per Ramanujan block. Under `beta=r/N`, it is equivalently the same restriction on `(P_5-I)beta`; all beta vectors are allowed by the full Ramanujan basis, so that basis does not enforce it. Defect support is also not interchangeable with support of r, support of beta, or support of the time-domain projection.

At a fixed full support pattern, the complete dyadic decomposition has at most `2 + (d-1)(S+2)` parameters for N>=2, with the 2 covering DC and q=2. Using `min(q/2,S+2)` gives a sharper levelwise bound. This agrees with the archived `O((S+2)log N)` restricted-class statement. Taking a union over support patterns does not make a bounded-S class an arbitrary-input guarantee. For small conductors the restriction can be vacuous; strict dimension separation is only asserted when `q/2 > S+2`.

## Paid evaluator interface retained without change

The archived proof and independent review support the following existing implementation ledger, which this comparison preserves. Let `d=log2(N)`, `s_q=|support((P_5-I)r_q)|`, `T=sum_(q>=4)(q/2)s_q`, and nu count the coefficient negations actually executed in discovery. For N>=2:

- Root-order validation and power preparation: `N+2d` field multiplications.
- Pair splitting, signed action and defect discovery: `3N-4+nu` field operations.
- All-orbit emission: `5N-8-2d+2T` field operations.
- Total: **`9N-12+2T+nu`**.

At a conductor q=2m>=4 the emitted orbit cost is `5m+2ms_q-2`: two dense anchors cost 4m operations, all sparse defect evaluations cost `2ms_q`, and the two cycle walks contribute `m-2` additions. Even additions from zero remain charged. The Ramanujan basis theorem supplies neither these anchors nor an uncharged defect-discovery oracle.

The same-output dense alternative modulates r by `zeta_q^j` and runs a length-m radix-two DFT with root `zeta_q^2`, at cost `m+(3/2)m log2(m)`. The hybrid chooses the smaller actual emitted count at each conductor after paying discovery. Its shared N-entry root table uses stride `2N/q` for the local FFT. Its full count is bounded by the prepared radix-two comparator `N+2d+(3/2)Nd`, plus `N-3+nu`. Generic work remains O(N log N); uniformly bounded defect gives O(N(S+1)). These are operation-count claims about these evaluators, not optimality or wall-time claims.

The capped version verifies fresh-input defects; if its cap fails, it uses the full radix-two fallback after O(N) discovery overhead. Scanning, exact zero tests, support storage, routing, and copies remain charged word operations. The dyadic scatter plus DC writes all N outputs, including the q=2 case.

The modular prototype assumes a caller-certified odd prime and a supplied primitive Nth root, pays its root-order test and table preparation, and does not include prime/root discovery or certification. An order test is insufficient for a general composite-ring extension without a principal-root condition. Arbitrary complex registers are not subjected to an implicit scalar automorphism. Bit accounting still includes index products and modular arithmetic:

    O(N(S+1)(M_mod(b)+b+M_int(log N)) + N log N).

The supporting-prime condition implies `b>=log2(N+1)`; the N explicit residues already require Omega(N log N) output bits. No fixed-precision or floating-point correctness conclusion is added.

## Verification and source map

The primary PDF was successfully read through the web PDF text service on 2026-10-17, including section 4 and Theorems 1-2. A separate local PDF download returned HTTP 403; no local PDF copy or visual inspection is claimed. The text extraction exposes all cited formulas.

`check_mapping.py` now contains wholly fresh formula-only controls, with no archival imports or evaluator execution. Exact rational and F_257 checks for N=2,4,8,16,32,64,128 pass: 51 full reconstructions; 182 exact projection-coordinate maps; 1,051 conductor-output identities; 5,866 projection spectral checks; 131 local cost-formula checks; 51 global ledger-formula checks; and 51 hybrid formula-bound checks. Ledger checks compare mathematical sums, not measured execution counts. No fallback execution is claimed in the accepted controls. The algebra above establishes the general mapping; finite controls do not establish an asymptotic claim.

Execution provenance: an earlier version of this comparison checker imported the archived `galois_defect.py` and called its `transform` and `hybrid_transform` functions in two local runs. This crossed the requested no-historical-program-execution boundary. Those scripts, results and reports were preserved separately and are excluded from accepted evidence. The public checker and results were replaced by the fresh controls described above. Observed side effects were local result-file writes and Python bytecode caches; no external writes or network calls were observed. This is an observation based on inspected source and command results, not a forensic network-monitoring claim. The original `run_audit.py` was not executed. See `EXECUTION_PROVENANCE.json` for the bounded record.

| Source | Verified locator | Role |
|---|---|---|
| Primary paper | [PDF page 3, section 4](https://systems.caltech.edu/dsp/PPVSquare.pdf#page=3), (15)-(22), Theorems 1-2 | Ramanujan block and full-basis theorem |
| ALG-012 proof | [Pinned README](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/e6/e6b9f3f934712db777939bc7656e6bbf6e0e3c3f5d22c47ed24f5870ac283e22__e6b9f3f934712db7__README.md), sections 1-3 and 5 | Signed action, restricted class, hybrid, roots and bit costs |
| Independent archival review | [Pinned review](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/93/935ed394798de3999d670e1186a9cdd26752170f81ce253eff5e948fb56ddbed__935ed394798de399__GALOIS_INDEPENDENT_REVIEW.md), lines 14-87 | Output indexing, ledger and fixed-support dimension |
| Implementation | [Pinned implementation](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/archive/objects/99/9940bcb774b94f8f9250c8760868cfd5f709d926290bfabef7931287ae6218ef__galois_defect.py), `signed_action`, `discover`, `emit_orbit`, `hybrid_transform` | Loop cost and root-stride contract inspected as text |
| Owner baseline | [Pinned open-record index](https://github.com/AgentSlop-Si/research/blob/26eb7017276591988762f27e2d1c23e739bcf3e4/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json), ALG-012 | Status TO RESEARCH, priority 34; historical gate retained |

Local source hashes match the named archival SHA-256 prefixes in full: review `935ed394798de3999d670e1186a9cdd26752170f81ce253eff5e948fb56ddbed`; proof `e6b9f3f934712db777939bc7656e6bbf6e0e3c3f5d22c47ed24f5870ac283e22`; implementation `9940bcb774b94f8f9250c8760868cfd5f709d926290bfabef7931287ae6218ef`.

## Narrow owner proposal

Append a dated bounded-comparison result and stop condition to ALG-012's existing owner history. Record exact dyadic coordinate overlap and the qualified paid-evaluator nonmatch. Retain TO RESEARCH, priority 34, all earlier proof/risk guards, and the prior relative-field rank wording as history with scope clarified. Do not edit ALG-052 or mark the broader owner gate complete. A separate owner-update proposal preserves the previous record; no external write has been made.
