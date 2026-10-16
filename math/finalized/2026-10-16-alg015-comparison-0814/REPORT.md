# Ordered affine-cycle Fourier filters: primary-source comparison

Date: 16 October 2026. Record: ALG-015.

## Outcome

The bounded comparison is complete as a **qualified nonmatch** to classical lifting cascades. Inverting noncommuting factors in reverse operational order is established algebra, illustrated constructively by the selected primary theorem. That theorem does not identify the present supplied affine-cycle certificate, pooled cyclic closure, or fully charged all-output Fourier procedure. No historical-priority claim for the complete package follows from this comparison.

The accepted restricted correctness result remains unchanged. Earlier Prony, rational-generating-function, sparse-interpolation and pruning leads are addressed below rather than silently dropped. Both recorded implementation repairs were already accepted; parameter discovery remains unimplemented and outside the supplied-parameter theorem.

## 1. Exact statement and supplied data

Let N be dyadic, N>=4, with supplied exact field and suitable primitive Nth root q. The positive-exponent DFT is F[k,j]=q^(kj). Each supplied filter is L_i=I-lambda_i M_i, where

    (M_i x)[j] = q^(b_i j) x[(a_i j+c_i) mod N],
    a_i=1 mod 4, and b_i,c_i odd.

The finite ordered list has depth d and uses every entry of an r-element scalar pool. Descriptors have O(log N)-bit lengths. All source and target permutations are checked to be single cycles. An accepted raw N-vector has a fully computed final residual

    u=L_d ... L_1 x,  |supp(u)|=s<=the supplied cap.

The intermediate residuals may be dense. No graph or continuous-parameter discovery is supplied by the theorem. Each closure 1+lambda^N must be nonzero before division; lambda=0 remains valid.

The exact Fourier conjugate has

    (Mhat_i y)[k] = q^(-c_i a_i^(-1)(k+b_i))
                    y[a_i^(-1)(k+b_i) mod N],
    F M_i = Mhat_i F.

Consequently v=Fu=Lhat_d ... Lhat_1 Fx. Starting at v, solve Lhat_d, then Lhat_(d-1), down to Lhat_1. In product notation Fx=Lhat_1^(-1) ... Lhat_d^(-1)v; the rightmost inverse acts first. Reversing the source cascade changes u in general.

The retained source and review are [the original proof and ledger](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/83/837c563f27047531043692615f6cdfa3d59b395cff17446e60d10e6d7c261cd1__837c563f27047531043692615f6cdfa3d59b395cff17446e60d10e6d7c261cd1__README.md) and [the independent scoped review](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/0d/0d838ebbcc7268a3a95dd6d7ac971c42b41c4bbab8c7d44b44ea3477239657ae__0d838ebbcc7268a3a95dd6d7ac971c42b41c4bbab8c7d44b44ea3477239657ae__INDEPENDENT_REVIEW.md).

## 2. Selected primary theorem

Daubechies–Sweldens, *Factoring Wavelet Transforms into Lifting Steps* (1998), Theorem 4, printed p.257, assumes a complementary finite filter pair with determinant-one Laurent-polyphase matrix P. It factors

    P(z) = product_(i=1)^m [[1,s_i(z)],[0,1]]
                          [[1,0],[t_i(z),1]] diag(K,K^(-1)),
    K != 0.

Figure 8, p.258, reverses the cascade for reconstruction. Section 8, Theorem 5, p.264, counts additions and multiplications per output sample pair. With degrees 2n,2m, m>n, its general nonsymmetric schedule compares 4(n+m)+2 against 2(n+m+2), approaching a factor two for long filters. These n,m are filter-degree parameters, not the Fourier input length N. [Author-hosted published paper, Theorems 4–5 and Figures 7–8](https://sites.math.duke.edu/~ingrid/publications/J_Four_Anal_Appl_4_p247.pdf).

### Our algebraic mapping and nonmatch

Write U(s)=[[1,s],[0,1]] and D(t)=[[1,0],[t,1]]. Direct multiplication gives U(s)^(-1)=U(-s), D(t)^(-1)=D(-t). In general U(s)D(t) != D(t)U(s); for s=2,t=3 the products are [[7,2],[3,1]] and [[1,2],[3,7]]. Thus the inversion-order principle used by ALG-015 is the same elementary inverse-of-a-product law. Noncommutation alone is not a new theorem.

The match stops at that law. The named ALG-015 factors act on one length-N cyclic vector with index-dependent chirp coefficients and affine reindexing. They have no displayed identification with the two-channel Laurent-polyphase factors in the selected theorem. For one full weighted cycle, the determinant is 1 minus the product of edge weights, hence det(L_i)=1+lambda_i^N. It can vanish, whereas the displayed triangular factors have determinant one. In our finite control lambda=2,N=32 gives det(L_i)=2 in F_65537. A hypothetical embedding or rescaling into another factorization would require its own exact map and cost; this comparison does not rule out such embeddings.

The Fourier intertwining, the final sparse defect test, and the shared denominator arise from the specific ALG-015 representation. The selected factorization does not itself establish those additional identities, their raw-input certification, or this exact cold field-operation bill. Conversely ALG-015 does not factor every finite perfect-reconstruction filter bank. This is a qualified hypothesis/interface nonmatch, not a claim that the complete idea is absent from all earlier literature.

## 3. Shared preparation, singular exclusion and paid cost

The following derivation comes from the retained ALG-015 statement, not from the lifting paper. A single scaled table per pool entry, scaled_lambda[e]=lambda q^e, supplies both source and target coefficients by indexing. No cross-query cache is assumed. Since the target permutation visits all residues,

    product_k lambda q^(-c pi(k))
      = lambda^N q^(-c N(N-1)/2) = -lambda^N.

Odd c and the dyadic primitive root give the last equality. The source product is identical using odd b. Therefore every filter using the same lambda shares h_lambda=(1+lambda^N)^(-1), independently of its affine descriptor. Nonzero closure is checked before inversion. Cyclic solving uses two backward traversals and this closure inverse, not inverses of individual edges; zero lambda therefore causes no edge-division problem.

| Stage | Accepted-query field operations |
|---|---:|
| Root-power construction and root-order validation | N |
| r shared scaled-root tables | rN |
| r closure powers, additions and inversions | r(log2 N+2) |
| Every row of all d source layers | 2dN |
| All N outputs of the actual s-entry residual | 2sN |
| d Fourier-side cyclic solves | d(4N+1) |
| Total | (1+r+6d+2s)N+r(log2 N+2)+d |

Addition, subtraction, multiplication and inversion each count as one field operation. Exact equality tests, materialization, graph/index validation, bounded-word normalization and Euclidean index inversion are charged separately with O(N(d+r+s)) word work. Storage is O(N(r+1)+d). Root/field discovery, bit complexity and floating-point stability cannot be inferred from that unit-field model.

For d=2,r=1,s=1 the formula is 16N+log2 N+4. Re-evaluating the recorded arithmetic schedules gives 16,398 versus 16,384 at N=1,024, and 65,552 versus 77,824 at N=4,096, against the stated radix-two schedule N+(3/2)N log2 N. This is a cold arithmetic comparison; it is neither a wall-clock benchmark nor a comparison against every optimized FFT.

The lifting paper's per-pair filter-application count cannot replace this raw-query ledger. Even where a supplied operator factorization is reusable, preparation must be labeled amortized or charged on both sides. Here each raw query pays its root and scalar tables, all validation and all explicit outputs.

A singular closure declines before division. Excessive final support declines only after paying every executed source layer. Fixed depth, pool size and defect cap give an O(N) rejected attempt, followed by a separately paid ordinary FFT with a fresh root table. The all-input worst case remains O(N log N). Growing depth, pool or defect budgets must remain visible in the formula.

## 4. Earlier recorded leads

### Finite recurrences, Prony and rational generating functions

Massey's finite-sequence model uses homogeneous constant-coefficient recurrences; Eq. (2) tests every index from L through N−1. Theorem 2 supplies the shortest-register synthesis update. Section IV, Eqs. (16)–(18), represents a recurrence-generated infinite extension by S(D)=P(D)/C(D), with deg P<L. [Massey 1969, §§II–IV](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf).

Our comparison is with this specific low-order interface, not with every generalized operator-Prony method. An accepted ALG-015 input need not have a short natural-order constant-coefficient recurrence. Choose any valid graph list and a single used pool value lambda=0. Then every L_i=I and x=e_(N−1) is accepted with s=1. For every L<N, a recurrence at index N−1 would combine only preceding zeros and could not produce the final 1. Its minimal finite-sequence LFSR length is N. The finite generating polynomial z^(N−1) has denominator one but a long numerator, so a small denominator alone is no low-total-degree certificate. This does not preclude a useful sparse-polynomial treatment of that particular spike.

More generally, the source equations have position-dependent weights and affine index steps. Turning them into a homogeneous constant-coefficient recurrence in the raw coordinate order is an additional operation and hypothesis, not justified by counting r+s parameters. The final residual transform v_k=sum_(j in supp u) u_j(q^j)^k is indeed an s-term exponential sequence. Here its amplitudes and exponents are already available after full source verification, and explicitly writing all N v_k is charged 2sN. Prony discovery on that overlapping residual would not eliminate the source-filter verification or reverse solves. If recovery is instead attempted from samples, its sample, recurrence, root, coefficient and verification work must be paid.

### Sparse polynomial interpolation, including its Prony formulation

Van der Hoeven–Lecerf's 2024 final version studies recovery of monomial coefficients/exponents from a polynomial black box with degree and sparsity bounds. Section 5, Algorithm 4, uses geometric evaluations, rational reconstruction, roots, discrete logarithms and coefficient recovery. Section 1.2 labels its headline finite-field bounds heuristic under H1/H2. [Primary source, §§1 and 5, Algorithm 4](https://www.texmacs.org/joris/ffsparse/ffsparse.html).

For the raw coefficient polynomial X(z)=sum_j x_j z^j, the ALG-015 defect cap s is not a bound on its monomial count. Our exact N=32 control has all 32 raw coefficients nonzero while r=1,s=1. Its DFT also has all 32 coordinates nonzero. The residual polynomial U(z) is s-sparse, but it is obtained by the paid cascade and is already explicitly known. Black-box interpolation of X changes the supplied-data interface; interpolation of U rediscovers data already certified. Neither substitution provides free raw certification, a cheap discovery theorem for the affine filters, or a reduced all-output bill.

No formula hidden in the primary HTML's image-rendered equations is assumed here. The comparison uses the explicit input/output description and named stages; no unseen complexity expression is imported or compared numerically.

### Pruned FFTs

The FFTW authors describe pruning when only K outputs are requested or inputs are sparse; their first-K construction has O(N log K) work when K divides N. [Official FFTW discussion](https://fftw.org/pruned.html).

ALG-015 requests all N outputs and accepts dense raw inputs, so output omission does not explain its bound. Pruning or direct sparse evaluation may be used on the final residual once its sparse support is verified; its transform is already paid in the ledger. The residual's sparsity cannot be credited to the unfiltered input, and the cascade and inverse passes cannot be discarded.

These are explicit qualified nonmatches on their stated interfaces. They permit overlapping special cases and make no lower bound against other algorithms.

## 5. Independent mathematical controls and retained obstruction

A fresh small checker, using only self-authored matrix construction, Gaussian elimination and direct DFT, reconstructed the supplied witness over F_65537 at N=32 with q=65529, lambda=2, graphs (a,b,c)=(5,1,1),(9,3,5). It verified

    (|x|_0, |L1x|_0, |L2x|_0, |L2L1x|_0, |L1L2x|_0)
      = (32,32,32,1,32).

Both full Fourier intertwining identities and all 32 final outputs matched direct DFT. The two target closure denominators were both 2. Correct reverse solves succeeded; swapped target order failed. These checks also established dense raw/output polynomial controls and the lambda-zero spike boundary. They are finite mathematical checks, not execution of the supplied programs, a new production certification, or an independent operation-counter replay.

The witness defeats the two named single-filter constituents only. It does not prove failure of every possible single graph. For fixed discrete graph/pool/support choices, the nonsingular representation x=L1^(-1)...Ld^(-1)u is rational in at most r+s scalar values. A finite union therefore has complex dimension at most r+s and cannot contain generic C^N when r+s<N. This is a representation restriction, not a general FFT lower bound or a finite-field counting theorem. Singular branches require separately retained kernel amplitudes and decoding cost.

The earlier sparse-surrogate obstruction remains closed at its accepted scope: for a map with at most c nonzeros per column, a k-sparse correction removes at most ck support positions from its defect. In particular, the single-filter bound has c=2. It is not silently extended to arbitrary chains or unrestricted Fourier circuits. [Retained fusion-gate proof and limitations](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/9b/9b6d9bfeedec91ed214308b29537b3da2e07bdb64930ad2a8b028f64ae66bc1c__9b6d9bfeedec91ed214308b29537b3da2e07bdb64930ad2a8b028f64ae66bc1c__FUSION_GATE.md).

## 6. Full recorded obligation audit and closure boundary

The current gate requests one noncommuting cascade theorem and an exact hypothesis/formula/cost comparison, allowing a qualified nonmatch. Sections 1–3 supply it. The older named comparison leads are covered in §4. All-coordinate verification, shared preparation, singular exclusion, reverse order, paid fallback and the full accepted cost remain explicit. The sparse-surrogate obstruction is preserved in §5.

The original independent review records both implementation repairs as already made: materializing supplied iterables before checking emptiness, and charging fallback work in the stage ledger as well as the total. The present comparison does not reopen those accepted repairs or claim a fresh replay. Parameter/graph discovery is explicitly absent from the supplied-parameter theorem and source implementation. It remains additional research if that different capability is requested; completing this bounded comparison does not prove or implement it. Likewise, singular reconstruction, exact bit complexity, numerical stability and hardware performance retain their separate boundaries.

After independent acceptance, the owner row may close at its recorded bounded-comparison scope. This does not assert worldwide novelty, unrestricted sub-N-log-N Fourier evaluation, production readiness, or that every possible future research direction is finished. No priority, accepted theorem, historical statement, note or format is changed by the proposed update.
