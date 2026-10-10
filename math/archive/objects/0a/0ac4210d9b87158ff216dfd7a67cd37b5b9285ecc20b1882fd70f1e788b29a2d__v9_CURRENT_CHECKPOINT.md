# Current Fourier research checkpoint

9 October 2026. The five direct sources received at 19:06–19:10 are now independently audited and integrated: bounded common-chirp recognition, centered v12, multistage bit reversal, Phase25 and offset-class v12. They provide scoped exact algorithms, approximation refinements, explicit implementation corrections and restricted representation certificates. No new exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## Exact bounded common-chirp recognition and polynomial-cost phase certificate

For fixed r>=1, N>=3r and a supplied prime field containing a certified primitive Nth root omega, the recognizer accepts exactly vectors

`x[j]=omega^(a*j^2) sum_(ell=1)^s c_ell omega^(b_ell*j)`, with 0<=s<=r,

distinct active frequencies and nonzero active coefficients. The zero vector is handled as the empty representation. Recognition and all accepted transform outputs cost O_r(N) exact field arithmetic under the stated field/root contract; rejection means only nonmembership in this structured family.

The phase eliminant has degree at most D=binom(r+2,3), not necessarily exactly D. Its normalized matrix is polynomial Toeplitz with nonzero constant leading minors. This replaces factorial expansion with independently verified polynomial-cost constructions: exact Bareiss O(r^9), or truncated-series nonsymmetric Levinson with Karatsuba/Newton arithmetic O(r^(2+3 log2(3))) and one scalar inversion. No p>D assumption or division by an integer index is needed. With L=N/gcd(2,N) and C=min(D,L), charged candidate processing gives `O(T(r)+S(N,r)+C(Nr+r^3)+N)`, where `S=O(min(L(D+1),D+L^log2(3)))`. Growing-r setup, verification and storage do not disappear; this is not a general linear-time FFT.

The original independent audit classified 118,617 finite-field vectors with no false decisions in those tested spaces. The extension includes 210 coefficient comparisons, 388 scalar determinant comparisons, 123 Toeplitz/Bareiss comparisons through rank 16 and explicit p<D examples. These controls support the included general proofs. The original note and audit are unchanged. See `additions/1906_chirp/`.

The [delivered private theorem note]([private source omitted]) summarizes this result. Novelty is unconfirmed: prior-art review is focused and incomplete, and the common-chirp model and determinant/Toeplitz ingredients are classical.

## Centered v12: approximation certificate and constructive precision repair

Centering the active interval halves the largest Bessel argument. An independent sharper envelope on 0<=z<=pi/2 is `sum_(r in Z)|J_r(z)| = 1+integral_0^z J_0(t)dt < 2.278`, replacing the source's 4.25 fusion factor. Centering each occupied block at its own midpoint additionally halves the local argument, with one table for full blocks and at most one for the final partial block. At the recorded N=511, target 10^-8 proxy, the specified refinement permits H=3 instead of H=4 at R=11. This is a certified parameter/proxy improvement, not an independently measured runtime speedup.

Balanced product-tree depth does not imply logarithmic forward error: a k-leaf product still accumulates k-1 multiplication errors, and root reuse can also accumulate O(ku) error. A constructive repair reanchors every Theta(p/log p) positions, prepares bounded-angle Taylor anchors/roots with charged pi setup, and uses p+O(log p) bits to obtain uniform absolute carrier error 2^-p in O(N+p) arithmetic. A conditional summary-interface ledger and charged Bessel-series construction preserve the earlier sufficient leading mantissa order, with guard bits. They certify a specified replacement design, not the uploaded NumPy/SciPy implementation.

Centering does not stabilize the forward Bessel order recurrence. At the supplied N=511 example one mode already requires over 95 additional seed-accuracy bits by the lower amplification bound. All R short transforms and decoder passes remain charged; the shrinking-error arithmetic order and exact-summary rank barrier remain unchanged. See `additions/1906_centered/` for separate identity and precision reports.

## Multistage bit reversal: exact finite-size geometry, not Fourier synthesis

For t separated-generator stages with fixed intervening permutations, the all-size complex image-dimension bound is `min(N^2,N+t(4N-6))`. It follows from the 5N-6 dimensional stage family and the free (t-1)N-dimensional diagonal boundary gauge action. Generic matrix coverage requires at least `ceil((N^2-N)/(4N-6))` stages; this does not prove a Fourier lower bound.

All 34 saved modular Jacobian ranks and six full-row minors were independently reproduced. Nonzero integer-polynomial minors prove the corresponding complex dimensions for N=8,16,32. Gauge directions exhaust the kernel at every saved subthreshold depth. Appending identity stages extends full dimension to every larger depth for those same sizes. No all-N saturation theorem or representation of the specific Fourier matrix is established; the demonstrated fully charged generic executor is quadratic at its threshold family.

See `additions/1908/`. The 548,427-byte original source archive, absent from the standalone audit ZIP, is now preserved there unchanged. All original audit files remain byte-identical except the package manifest, whose approved original is retained separately.

## Phase25: correct affine-run identities and a complete exact frontier solver

The supplied affine-run geometric DFT identity handles z=0 and resonant ratios, with charged O(rN+r log N) field work for supplied structure/root data. The two-run dyadic cycle and twisted four-track cut-rank certificates are valid in their stated models, including the hidden rank-five cut and its approximation floor.

Two individually admissible cyclic resolvents may have a singular sum: the additional determinant `det(2I-alpha W-beta Z)` must be nonzero. The uploaded band-LU/Woodbury schedule also misses cases with zero unpivoted pivots or a singular band base, even when the full target is invertible. Exact counterexamples are retained.

An independently authored whole-matrix row-pivoted frontier solver covers every nonsingular admissible instance of this fixed-width family in O(N) exact field setup, application and storage, detecting singularity without the band-base assumptions. For complex |alpha|,|beta|<1 the sum is nonsingular with the strengthened condition estimate in the report; this does not prove floating-point backward stability. Exact controls include 21,714 stride cases, 1,846 direct affine-transform comparisons, 289 small-field parameter pairs and larger inverse checks through N=16,384. See `additions/1909/`.

## Offset-class v12: unbiased approximation with an accuracy-dependent row count

Under explicit half-up nearest-grid rounding, there are exactly L=N/gcd(N,Q) offset classes, namely congruence classes of target indices modulo L. A deterministic linear-time class plan avoids redundant sorted-uniqueness validation in the source. In the legal prime-power regime M^2<=Q, the ideal row is unbiased with per-output variance at most `(M/N)||x||_2^2`. A fresh row costs `O(L[Q+K log K])`; fixed-cofactor input lengths admit O(N) arithmetic rows with M=Theta(log Q). Exact-center means exact expectation, not exact realized transform outputs.

Accuracy and failure must be specified together. Near the variance scale with constant g, the stated all-output guarantee uses Theta(log(N/delta)) rows. At any fixed weaker power accuracy N^-alpha with alpha<1/2, a suitable constant number of rows instead suffices for polynomially high success probability on fixed-cofactor lengths. This positive regime is preserved without presenting it as an exact FFT or an unrestricted all-length result.

The scan-state rank certificate needs distinct post-cut future queries and a linear-state/no-reread model; its bound is min(R,L_after), not a general Omega(RN) time theorem. Exact-grid edge handling, N=1 identity behavior, modular integer range, modulation error, roots/FFT contracts and robust numerical aggregation remain explicit qualifications.

The claimed missing v11 core is not missing from the exact predecessor archive in this chain: the core and reference are byte-identical to preserved earlier sources. A separate conversation admits a failure of some export, which does not identify that export with this archive. See `additions/1910/` for the exact artifact comparison, independent covariance proof, conditional precision transfer and retained original archives.

## Derived slowly growing-rank fast path

The approved polynomial ledger directly gives `O(Nr^4+r^(2+3 log2(3)))` field additions/multiplications, O(N+r^4) storage and O(r^4) cached scalar field inversions. Thus `r=o((log N)^(1/4))` permits `o(N log N)` recognition and accepted full-output transforms within the same common-quadratic-chirp family. This is a genuine relaxation beyond fixed r, not arbitrary-input Fourier recovery. The separate derivation, root/field contract, inversion accounting and fallback qualification are in `GROWING_RANK_CHIRP_COROLLARY.md`; it is not an alteration of the sealed original supplement, a numerical-stability claim or a novelty verdict.

## Newly discovered Library sources: static review only

Four additional generated archives are preserved unchanged in `additions/1930_static/`, separately from direct uploads. Twenty-five Python files parse and all four manifests/72 original member hashes verify; original programs were not imported, executed or compiled. HERO17's newly available code accompanies a note byte-identical to the already audited chirp note and does not include the later independent polynomial-cost extension. Its historical tests remain historical.

Phase26, the sparse-defect gate and mixed-radix v13 now also have completed independent mathematical reviews, summarized below. Initial static observations remain separately labeled and do not replace those proofs. In particular, the M-bank identity is inherited from the prior 17:17 checkpoint rather than a new discovery. Filenames dated October 10 are retained alongside October 9 Library creation context. Composite HERO2 is now independently audited and integrated as described below.

## Completed composite and late Library mathematical reviews

All four reviews that were awaiting incorporation are now approved and included; the bounded batch has no pending deep review. These independent reports supplement the preserved original/static evidence, without converting source-recorded tests into independent test runs.

### Composite HERO0 phase 2

The composite cycle executor and randomized approximate contract are valid for the stated factorizable lengths. Its physical map is a scaled orthogonal projection P with P^2=MP, not an idempotent projection. The uploaded covariance coefficient M(M-1)/phi(N) is weaker than the previously accepted composite certificate, which remains the primary bound. The fixed-row binomial tail also consolidates an earlier v9 result. Capped candidate counts do not automatically bound random-bit rejection work, and the offset fallback retains sampling/sorting costs needing explicit repair. This is useful restricted-length approximate implementation work, not a new exact or all-length advance. Original archive, all 24 source files, prior comparison evidence and independent checks are retained in `additions/1916/`.

### Sparse-defect inverse-stage theorem and a repaired escape example

For an arbitrary row-q-sparse baseline B, the Fourier rank defect satisfies `rank(F_N-B)>=floor(N/(q+1))`, robust under endpoint monomials. Telescoping gives the stated sparse-plus-low-rank inverse-stage product restriction, including singular sparse baselines. The uploaded bandwidth-only witness proof did not establish its broader arbitrary-row-sparsity claim.

The independent repair closes that specific gap: for the separated scan S with lower/diagonal/upper entries 1/3/2 and every row-q-sparse B,

`rank(S^-1-B)>=ceil(floor(N/(q+2))/(2q+1))`.

The proof uses interleaved nonsingular minors and a bounded-degree support graph, covers every support pattern and coefficient choice, and survives arbitrary endpoint monomials. At fixed q the defect is linear in N. Both S and its inverse have linear exact-scalar application, demonstrating a genuine separation of restricted operator classes, not a Fourier factorization. Explicit rational outputs can still require Theta(N^2) bits. Woodbury setup is `O(N+Nr^2+r^3)`, with fresh application `O(N+Nr+r^2)`; no-pivot Thomas code covers only a smaller chart. See `additions/1930_sparse/`.

### Mixed-radix v13

The independently checked physical one-row operator is exactly F_N P with the intended interleaved scaled projector. Unbiasedness, per-output covariance, rank and fixed-state/global error formulas hold under the stated randomness contract. The source's finite-field completed-bank checker reverses a one-row phase convention; averaging conceals that mismatch. The independent checker verifies the recurrence before bank averaging and closes this test-coverage gap.

Full column-state independence is sufficient but not necessary: a shared random slope with conditionally pairwise-independent beta phases preserves the covariance and reduces seed requirements. The normalized stacked complete bank is perfectly conditioned, and a common downstream twiddle perturbation loses the single-row M amplification under exact bank averaging. These are bounded improvements; they do not remove the scan/FFT work or give a complete numerical certificate.

Exact beta-bank completion and its ordinary Cooley–Tukey collapse were already established at 17:17. They are not new v13 discoveries. The independent suite checks 211,344 recurrence/composition entries and 19 exact covariance-projector cases, alongside the inherited completed-bank controls. See `additions/1930_v13/`.

### Phase26 simultaneous common-character cuts

For dyadic N and the specified products of sums of weighted Hamiltonian-cycle Green inverses, with bounded affine step magnitudes, exceptional edges, diagonal gates and affine interstage permutations, the common-character theorem is valid. A sharper Hamiltonian crossing budget halves the previous signed-edge allowance:

`rank <= min(N/2, T floor((N-1)/r)+sum_q floor(b_q/2))`, with `r=floor((N-1)^(1/s))`.

For bounded steps and bridges per term, exact Fourier representation still requires `Q=Omega(log N/log log N)` term occurrences; the same obstruction holds at fixed operator error below 1/sqrt(2). This is a restricted representation result, not an unrestricted circuit-time lower bound or a theorem for arbitrary internal non-affine permutations. The source's floating witness search can accept equality where strictness is required; an independent integer pigeonhole routine enforces `r*abs(t)<N`. The strengthened finite thresholds 7,12,21,36 are necessary-only certificates, not factorization constructions. Earlier Phase25 nonsingularity and pivot corrections remain in force. See `additions/1930_phase26/`.

All nine new mathematical audits in this bounded update are complete, alongside the distinct static/source-availability review. No new arbitrary-input exact faster Fourier transform, universal FFT lower bound, or integer-multiplication complexity improvement has been established by this project batch.

## Consolidated interpretation

The chirp and Phase25 developments are concrete restricted exact algorithms. Centered and offset-class v12 concern randomized approximation with distinct bias/variance/precision guarantees. Bit-reversal Jacobian dominance is a representation result for generic matrices at specified sizes. These statements cannot be merged into an arbitrary-input faster exact Fourier evaluator. Earlier complete F8 exception accounting, endpoint restrictions, parity/Gram statements, summary-rank bounds and charged setup requirements remain in force.

Completion of this bounded batch and its separately classified static source inventory are recorded in `PENDING_ADDITIONS.json` and `ADDITIONS_STATUS.json`. Static code/lineage review does not promote source-recorded tests or new mathematical claims to independently checked results. Baseline unread-source and account-coverage limits remain unchanged.

# Retained version 8 checkpoint

The five 19:06–19:10 sources listed as pending in the historical text below are completed above. Other new-source statuses are governed by the current pending inventory.


9 October 2026. All explicitly tracked later sources through the 18:48 UTC upload are now independently audited and integrated. This includes the 18:45 Phase24/window pair, 18:47 HERO0 note and 18:48 endpoint-rank archive. The separately discovered Phase23/window sources remain distinguished from direct uploads. No new exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## Phase24: sorting correction and a complete restricted evaluator

The stable-binary-sorting shift defect has exact rank `r=2 floor(T/2)`, with T the noncyclic transition count. Over iid fair binary inputs its exact law is `Pr(r=2k)=binom(N,2k+1)/2^(N-1)`, with mean N/2-1 and variance N/4 for N>=3. A fixed rank cap covers only polynomially many binary inputs. An explicit simultaneous bound over every nonzero cyclic stride, including noncoprime ones, gives rank at least N/8 with probability tending to one. These are restrictions on this cyclic-reference correction architecture, not general FFT lower bounds.

The nearby-order Woodbury identity is valid away from the root locus, with small correction determinant exactly one. The source needs two corrections: no nontrivial defect cycle exists at T<=1, so s=r+1 applies only at T>=2; and its s=0 implementation repeats z^N at every output, adding avoidable N log N work unless the shared factor is hoisted.

An independent sparse twisted-difference executor computes all outputs of a supplied and verified near-order geometric input in O(N(s+1)) field arithmetic and O(N) storage, where s counts changed successor edges. It handles every z, including the root locus, with at most one singular output evaluated directly. Input-family checks, permutation validation, roots/normalization, inversions, bits and complex conditioning remain charged. It is an improved special-input method, not a new arbitrary-input transform.

Reports and portable evidence: `additions/1845/`. Its source pair has 736 recursive occurrences, 550 distinct contents, 13 byte-new contents against the declared predecessor union, and 873 passing embedded checksums. The accompanying window archive is byte-identical to the already audited 18:25/18:28 source.

## HERO0: operator bridge, precision obstruction and conditional scan improvement

The Bessel/operator recurrence, inverse identity and Cauchy-minor representation obstruction are correct in their stated models. The straightforward forward cycle amplifies an initial b=1 Fourier-mode error by at least `(R-1)! (K/pi)^(R-1)` after R orders for K>=4. Thus a hypothetical cheap H application alone does not supply the required numerical stability or preserve the previous leading precision budget.

The selected-output prefix-scan commutator already has a full-rank minor for degree-one output weights. A constant-rank correction cannot move those weights inside one common scan on unrestricted forcings. The actual channel forcings are correlated, so this does not exclude a specialized joint evaluator, and full rank is not a multiplication-cost lower bound.

A bounded exact-field construction evaluates the polynomial scan subproblem in

`O(Q(R/B+B) log^2(M+R))`

operations with O(Q) storage, given monomial coefficients, `1<=B<=R<=M`, `B|K`, `Q=KM` and `M^2<=Q`. Taking an admissible B comparable to sqrt(R) gives `O(Q sqrt(R) log^2(M+R))`; use its minimum with the ordinary O(QR) scan. An asymptotic saving requires `log^4(M+R)=o(R)`. Root/forcing preparation, generic multipoint node setup and output materialization are charged. For the Bessel/Chebyshev branch, a conservative O(KR^2) coefficient conversion is additionally charged; it is not hidden as free preparation.

This is a **conditional scan-only arithmetic improvement**. The R independent K-point Fourier channel transforms still cost O(RK log K)=O(RN), leaving the current total O(RN). Exact Bessel generation is unspecified; a finite-precision/bit-complexity certificate and a practical optimized implementation for the blocked method remain absent. The older scan precision contract cannot automatically certify the new conversion and product/remainder-tree operations. No overall speedup or stability improvement is claimed.

The corrected offset statement uses the residue -Nj, equivalently -Nat for j=a*t mod Q. The checker already used that expression. See `additions/1847/independent_bridge/BRIDGE_AUDIT_AND_CONSTRUCTION.md`. The original note is preserved as a complete 143-line Library text extraction matching the reported 11,664-byte size; its hash is explicitly an extraction hash, not a separately downloaded raw-blob hash.

## Optimal endpoint rank: a one-matrix result with clear product limits

Over C, for dyadic N>=8, the exact minimum quasiseparable rank of Fourier over arbitrary independent input/output permutations is N/4+1. Double bit reversal attains it. Its cut-rank recurrence and parity-dependent total-rank formula are correct, with asymptotically optimal leading total N^2/6.

The independent odd-cut refinement gives lower bounds `ceil(k(N-k)(N+1)/N^2)` at odd k and `ceil(k(N-k)/N)` at even k. They match bit reversal pointwise at N=8 and N=16, proving exact minimum upper-right total ranks 14 and 48. Finite-size total optimality at larger N is not established.

For common-coordinate-order products, quasiseparable ranks add, so s stages of rank at most r require sr>=N/4+1. Uncharged interstage permutations and differently ordered stage representations prevent using that inference directly. A rank statement is not an unrestricted arithmetic-operation lower bound.

The older two-stage bound N<=9r^2+7r retains its natural/affine-input endpoint restriction. The new one-matrix theorem does not extend its endpoint scope. The independently reproduced N=8 subset, optimized-support and trace screens do not improve the previous 15,728-survivor window screen. See `additions/1848/`; all 15 source-manifest entries and the inherited window archive hash verify.

## Consolidated outcome and scope

The strongest new constructive results remain restricted-input exact evaluators and a conditional improvement to an approximate-method scan subproblem. Every proposed arbitrary-input construction still needs a scalable exact identity, exception coverage, an efficient full evaluator, charged coefficient/root preparation, and an appropriate numerical or bit-cost contract. The F8 polynomial systems and exceptional charts remain open where previously stated. The earlier parity, Gram, uniform Prony, unitary, summary-rank and precision results remain in force.

Twenty-two later direct-upload records and two Library-discovered source records are now integrated, with known identical copies labeled separately. Earlier baseline read/coverage limits are unchanged: completing these bounded new-source audits does not imply that all historic source texts or account conversations have been fully reviewed. Five newer direct source records received at 19:06–19:10 remain pending: the bounded-chirp note, centered v12 archive, bit-reversal multistage geometry archive, Phase25 archive and offset-class joint v12 archive. Their claims are not promoted here. `PENDING_ADDITIONS.json` records their exact known identities and review status; completion of the earlier bounded audits does not declare the research problem solved.

# Retained version 7 checkpoint

Pending-source references below are historical. Phase24, HERO0 and the endpoint audit are completed above. All previous accepted results and restrictions are retained.


## Verified Phase23 and interval-window addition

9 October 2026. Integrates the exact 18:24/18:25 Library-generated archives against master version 6, including the finalized 17:42 supplement and all earlier verified work through 18:07. A distinct 18:28 same-name window archive was also downloaded and proved byte-identical. No new exact arbitrary-input, all-output sub-N-log-N evaluator has been established.

## Accepted source results

- The general window rank-nullity lemma is correct with actual transform-submatrix ranks. Its simplified Vandermonde version permits arbitrary Fourier output order, but Fourier inputs must remain in natural or affine coprime-stride order. The source's N<=9r^2+9r+3 consequence for two stages of both quasiseparable ranks <=r is valid in this scope.
- The N=8 full-window filter leaves 15,728 of 40,320 permutations, compared with 28,584 under the old bilateral filter. The 12,856 extra rejections and all endpoint-permuted N=8/N=16 Cooley–Tukey positive controls were independently reproduced. The latter controls decisively prohibit silently applying the simplified Vandermonde gate to arbitrary input permutations.
- Phase23's geometric resolvent, sparse cyclic-difference formulas, binary Hankel rank obstruction and exact inverse-residual support count are correct. They establish exact special-input linear-work routes and architecture-specific limitations. The original exponential detector requires split distinct roots in the working field; it is not a complete recognizer for arbitrary order-two recurrences.
- The classical binary Hankel rank distribution bounds low-complex-exponential-rank coverage by 2^(2r-N+1) for r<N/2. This is a restriction on low-order input descriptions, not a lower bound on arbitrary Fourier algorithms. Leading Hankel rank alone is not sufficient to recognize the entire input's recurrence.

## Independent bounded extensions

1. A strengthened marker-gap argument gives N<=9r^2+7r for r>=1 in the same natural/affine-input endpoint model. Thus two rank-one stages are excluded for N>=17, improving the source's N>=22 cutoff. A source-supplied N=16 permutation passes all window tests, making 16 the sharp maximum length permitted by this necessary rank-one filter; it is not an actual factorization.
2. The entire all-window test reduces exactly to six endpoint checks and three sliding-minimum/maximum passes. A monotone-deque implementation costs O(N) comparisons/indexing and O(N) space, and agrees with exhaustive testing on all N=8 permutations and varying asymmetric ranks. This speeds the architectural filter, not the transform.
3. A square-root-free rational generating-function executor handles every verified fixed-coefficient recurrence of order at most two, including repeated and nonsplit roots. A raw-input recognizer is complete for this class. All Fourier outputs require O(N) field arithmetic plus charged root/normalization setup and a constant number of inversions; at most two singular Fourier nodes are evaluated by O(N) direct sums each. It strictly enlarges the original restricted-input branch without improving arbitrary-input worst-case complexity.
4. For supported dyadic N>=8 over GF(998244353), the original exponential detector accepts exactly six binary words. Combined with its first/second-difference threshold, the original adaptive fast path accepts exactly N(N-1)+4 of the 2^N binary inputs, strengthening the source upper bound N(N-1)+34. This exact characterization concerns the original detector, not every possible recurrence/Green algorithm.

## Cost and construction implications

The new recurrence executor avoids data-dependent square roots and splitting-field preparation. Exact equality testing, finite-field inversion, primitive-root/normalizer preparation, coefficient representation and bit precision remain explicitly charged according to the chosen model. A fixed modulus with bounded supported lengths is not an unbounded asymptotic family. No floating-point stability guarantee is supplied by the algebraic formulas near singular denominators.

The window result prevents scaling a natural/affine-input two-rank-one-stage ansatz beyond N=16, regardless of its internal permutation. A viable architecture must enlarge ranks or stage count, use genuinely non-affine input order, or leave that architecture; each surviving candidate still needs exact full Fourier identities and a fully charged executor. The special-input recurrence result is constructive but has exponentially sparse coverage on uniform binary inputs at fixed order. Neither result resolves the arbitrary-fresh-input, all-output target.

## Evidence and integration

All paths in this section are relative to `additions/1825/`. Reports: `window_audit/WINDOW_AUDIT.md`, `phase23_audit/PHASE23_AUDIT.md`, and `SOURCE_PROVENANCE.md`. Run `python3 run_independent_audits.py` for the independently authored checks only.

Two distinct archive streams contain 721 recursive member occurrences, 536 distinct byte contents and 27 byte-new contents relative to the explicit predecessor hash union. All 860 embedded checksum entries pass. Both immediate nested predecessors exactly match the already audited 18:07 archives. Complete inert source archives, identity/version records, duplicate-copy hash evidence, independent checkers and results are included. No uploaded program or bytecode was executed or imported, and no novelty or publication-priority claim is made.

## Later direct inputs still pending

The 18:45 Phase24 archive, 18:47 HERO0 note and 18:48 optimal-endpoint archive are being reviewed separately; their new mathematical claims are not included as verified findings here. The accompanying 18:45 window archive was independently compared byte-for-byte and is identical to the now-verified 18:25 source. Exact identities and statuses are in PENDING_ADDITIONS.json.

# Retained version 6 checkpoint

Historical pending references in the retained text describe earlier snapshots. The Phase23/window discovery review is now completed above; the 17:42 review remains completed.


All uploaded batches through18:07 UTC are now independently audited, including the previously pending17:42 Phase21/v11 supplement. Two newer Library-discovered checkpoints are under separate review and are not included as verified findings. There is still no new exact arbitrary-input all-output sub-N-log-N evaluator established by this project.

9 October 2026. This resolves the previously pending 17:42 batch. Paths in this section are relative to additions/1742/. The independently verified18:07 results remain included below. The new evidence does not establish a fully charged exact arbitrary-input all-output transform below N log N.

## Provenance and exact F8 status

The new mathematical sources are Phase21 Weyl–Green research and all-length fused v11. The third archive is the same triple-intersection source bytes as the 17:17 upload. This was checked by the explicit Library identity, a fresh separate retrieval, raw-byte comparison and all 214 recursive members, not by filename. Preserve every prior exact F8 residual, resultant, saturation/corner condition and exceptional chart.

The complete batch contains 671 recursive member occurrences, 487 unique member hashes and 29 byte-new text/data/source-program contents versus the declared prior union; all 815 embedded checksum entries pass. Phase21's nested Phase20 and v11's unit-step core are unchanged. No uploaded source program or binary was executed.

## Phase21 exact representations and sharper barriers

- The Weyl chirp identity, flat dense Green example, common-Weyl pole budget q≥N/2 with arbitrary outside diagonal scales, weighted same-order sum/product bound Q≥N/2, and full-rank cheap commutator example are correct in their stated even-length domains.
- Wraparound cross-ratios sharpen the common-generator coefficient form: the otherwise geometric multiplier rho must satisfy rho^N=1.
- The degree-N/2 Prony polynomial is independently reconstructed. Nonzero derivative/forbidden-pole resultants certify matching N/2-pole complex representations for all supplied dyadic lengths4..8192, plus18 listed non-dyadic lengths. These are finite characteristic-zero certificates; the uniform N/2-pole claim remains open.
- A new uniform construction proves h≤minimum common-Weyl pole count≤h+1 for every even N=2h≥4. The pencil zP_h+tP_(h−1) preserves the required moments; consecutive coprimality and a finite bad-parameter count guarantee a valid integer t in {1,…,4h}. This is a representation existence result, not a runtime improvement. See `prony_extension/PROOF_OR_OBSTRUCTION.md`; symbolic degree8 and67finite-size controls independently pass.
- Every arbitrarily ordered weighted-cycle inverse has cross-cut rank exactly equal to the number of nonzero directed cycle edges crossing into the row half. Products/sums add this budget; masks cost zero; inserted permutations have their own crossing cost. Exact Fourier requires total budget≥N/2. Reverse direction alone still costs one and does not escape.
- For Fourier halfblock C, let v_N=tr(CC*−(CC*)²)=O(log N). A rank-q candidate block with q<N/4 has spectral error≥sqrt(max(0,1−v_N/(N/4−q))). The floor tends to1 for q=o(N), and for q≤(1/4−epsilon)N. An explicit odd-harmonic upper bound on v_N makes this quantitative.
- Term/crossing counts remain representation restrictions, not unrestricted shared-evaluator runtime lower bounds. Many same-order terms with a genuinely efficient shared evaluation are not excluded.

See `phase21_audit/PHASE21_AUDIT.md` and the explicit modular certificates.

## Fused all-length approximation and numerical qualifications

- Clenshaw streaming and Neumann block/local Bessel fusion are algebraically valid. Fixed-H storage is O(N); R decoder/short-FFT/output passes remain, so total shrinking-error work stays O(RN).
- H=0 fusion admits the sharper deterministic bias tau_R+Delta, Delta=pi(M−1)/Q, independent of an additional R multiplier. Its variance envelope remains (M/N)(1+tau_R)²||x||²; Delta enters the deterministic bias.
- G_(-h)=(-1)^h G_h, so only H+1 independent local channels per block remain. L fixed rows retain rank at most L(H+1)K, regardless of R; uniform exact summary-only recovery requires L(H+1)K≥N and, with a full input block, L(H+1)≥M.
- The source's full-row floating-point hypothesis does not automatically certify rounded fused summaries. A summary-decoder contract, summable uniform coefficient majorants, explicit summary/Clenshaw rounding and charged phase/Bessel generation are necessary. The independent sufficient ledger preserves the proposed leading precision order once those stronger contracts are met; it does not certify the uploaded SciPy/NumPy implementation or fixed binary64.
- A specified certified Bessel series generator can keep preparation within O(RN) arithmetic in the theorem regime, but its cost is not free and is not contained in the advertised O(N+RK) input-traversal saving. Bit cost, exponent range, integer overflow and robust classification/radius errors remain charged.
- The separate frozen-block rational-Taylor variant uses unweighted block summaries, O(N+RK) input-side arithmetic and O(RN) decoder work. Its deterministic bias is Delta+eta+|rho|^R/R! with |rho−pi|≤eta. This is a charged approximate exact-arithmetic variant; its fused numerical path still needs a summary-level contract.

See `v11_audit/V11_AUDIT.md` and `v11_audit/FP_CONTRACT_REVIEW.md`. Keep fixed-input simultaneous-output guarantees distinct from uniform operator accuracy and exact all-input recovery.

## Combined next target

The old complete chirp bank still reduces to Cooley–Tukey under its known evaluator, and the exact near-grid correction still has rank N/gcd(N,Q). Fusion does not change those exact statements. Any proposed speedup must supply a scalable exact identity, complete exception coverage and a fully charged shared evaluator. Classical identities and finite prototype tests are not novelty or production-certification evidence.


# Retained checkpoint including18:07 results

The historical pending references below describe the previous version; the17:42 review is now complete as stated above.

Verified updates include the 18:07 UTC Phase22 and bilateral uploads and the previous master through 17:17 UTC. The separate 17:42 mathematical supplement remains pending; its hashes are used only for provenance comparison. No new exact arbitrary-input all-output sub-N-log-N evaluator has been established.

9 October 2026. This addition can be merged into the authoritative master through 17:17 without waiting for the separate 17:42 mathematical supplement, which remains pending unless independently finalized. All paths here are relative to additions/1807/. No exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## New exact structural facts

- Phase22's real one-mask connected-Gram obstruction is sound. A stronger exact characterization is available: for real invertible A, existence of real invertible B and one nonzero complex diagonal Q in F=A Q P B is equivalent to J A=A E for a diagonal reflection-parity matrix E with entries ±1. This characterizes the left factor when the right factor is free, not a specified pair or a fast evaluator. Positive real left Green sums fail it.
- The bilinear finite-field Gram screen is necessary for fixed A,B and every middle Q,P. The 24 sample vetoes and 12 deliberately valid recoveries are independently reproduced. Zero-diagonal/collision branches remain inconclusive; Gram equality and one calibrated entry are insufficient for Fourier equality.
- F=H Q C is an exact cheap parity/axis extraction with C a real orthogonal cosine/sine residual. C still requires at least N(log2 N-1)/2 two-coordinate unitary gates in that restricted model. The sparse covariance and full first column uniquely specify the linear C, but do not evaluate Cx cheaply.
- The finite-field covariance test requires a fixed deterministic linear oracle and independent uniform challenges. It uses one seed call plus two calls per challenge. The uploaded apply_R repeats modular exponentiation, so its advertised linear overhead is not met as written; an independently specified consecutive-power recurrence repairs the coefficient/application count. Root/field setup and precision remain separate costs.
- The all-length tail-rank theorem gives min(t,N-1-max(pi[-t:])) <= r_lower(C)+r_upper(B), with a mirror prefix inequality. It covers general quasiseparable ranks in the fixed endpoint order. The unchanged tail (1,2,5) is excluded for every N>=9 with two rank-one stages, but N=8 remains open.
- For a constant rank sum s, every suffix/prefix inequality reduces exactly to the corresponding first/last s+1 boundary test. At s=2, 28,584 of 40,320 N=8 permutations pass. A closed-form count and the disjoint-boundary uniform-permutation bound P(pass)<= (s+1)^4/[N(N-1)] are proved. Passing is only necessary.
- The inherited 11-by-9 rank gate has no independent extra maximal minors: 45 vanish identically and the remaining 10 are constant multiples of Dhat=-DB DH. All 55 were independently reconstructed. Rank<=8 is exactly DB DH=0 within this rescaled polynomial family; original feasibility equations and all exceptional branches remain required.
- DB's homogenized coefficient matrix has exact rank four, with the nonzero 11251 modulo 12289 witness reproduced, so the quadric is absolutely irreducible in characteristic zero. Its unique affine singular point has h0=h1=0, so it is smooth on the inherited regular h0!=0 chart. Its zero locus is not excluded.
- The six-column auxiliary boundary gate has rank 4+rank([[U3,-L3],[U4,-L4]]) for N>=9. Its leading determinant is -(U3 L4-U4 L3) times the six-node Vandermonde. N=8 remains a genuine rank-deficient exception. The report supplies the direct proof absent from the source's referenced proof file.

Reports and reproducible evidence: `TWO_LATEST_AUDIT.md`, `phase22_audit/`, `bilateral_audit/`, `tail_screen_extension/`.

## Provenance

Two new outer source archives; 691 recursive member occurrences; 507 distinct contents; 34 byte-new text/data/source-program contents against the declared source union through 17:42. All 833 embedded checksum entries pass. The embedded Phase21 and triple-intersection archives exactly match prior sources. No uploaded executable, source program or bytecode was run. The supplementary archive contains full inert sources, source identities, explicit hash comparison data and independently authored checks.

No unrestricted lower bound, new exact transform or novelty claim follows from these results. The earlier verified exact residual systems, exception coverage and model limitations remain in force. The 17:42 Prony, cycle-crossing and fused-summary additions keep their separate pending/completed status; their source hashes are used here only for deduplication, and this audit does not promote them automatically.


# Retained checkpoint through 17:17 UTC

Current through the three archives received at 17:17 UTC on 9 October 2026. The three newer uploads received at 17:42 UTC are being audited separately and are not included as verified results here. No new exact arbitrary-input, all-output sub-N-log-N transform has been established by this project.

9 October 2026. Verified additions through the 17:17 UTC upload. All report paths in this latest section are relative to additions/1717/. Earlier residual systems and exception coverage remain preserved below.

## Current answer

The new materials do not establish an unrestricted, fully charged exact all-output transform below N log N. They give a genuine characteristic-zero slice exclusion in the fixed F8 search, stronger restricted approximation obstructions, complete Weyl certification tools, and an all-integer-length randomized approximate lift. An independently specified rational-Taylor variant closes the source's Bessel coefficient-preparation gap at the arithmetic level and supplies a conditional precision ledger.

## Exact F8 structural chart

- The new 11-by-9 multi-column gate has rank at most eight for the intended invertible globally separated inverse-stage/final-stage factorization. The source's standalone theorem needs the nonzero-column/invertibility hypothesis. If the fourth output multiplier is zero, invertibility forces the projected four-row basis to have rank at most two, so its cofactor vector is zero; no new nonzero multiplier guard is needed.
- On `h0 Delta T != 0`, an exactly reconstructed 250-term degree-eight minor is `Dhat=-DB DH`, with nine-term quadratic DB and 105-term sextic DH. All 924 exported cyclotomic coefficient vectors match.
- `Res_h6(W,Dhat)` at `h0=1,h1=h2=0` reduces to 6 modulo `(17,zeta8-9)`. This nonzero exact resultant proves the specified regular complex slice has no factorization. It does not exclude other base points or denominator branches.
- The nonzero 37-term and 476-term eliminated resultants constrain the base to a proper hypersurface union. The necessary four-structural-variable locus has dimension at most two, not proven empty.
- A new exact refinement proves the base where W is identically zero in h6 has at most 12 points. A degree-six elimination resultant and a fixed nonzero quadratic leading coefficient certify this. Its free-h6 stratum has dimension at most one; the overall dimension bound remains two.
- Independent GF(17) enumeration reproduces 4,596 candidates and ranks 9/8/7/6 with counts 3,266/1,203/125/2. Another 630 invertible exact positive controls pass, including zero-column multipliers and zero diagonal entries.

The gate/resultants are necessary additions, not replacements for the complete Fourier equations. Keep the old saturation/corner conditions, all excluded branches and the full separated-generator lift. Report and scripts: `triple_audit/`.

## Green Phases19 and20

- Full Weyl duality `MZ=DM`, `MD=Z^-1M` identifies the scalar Fourier family at every integer length; one scalar calibration gives F. The sharp Frobenius residual gap is `2 sin(pi/N)`. Small raw residuals at increasing N do not imply fixed accuracy.
- A fixed linear finite-field oracle can be checked in `1+3h` calls. If its stacked residual rank is rho, independent uniform tests pass with exact probability `p^(-h rho)`. This is not a linearity test, a characteristic-zero proof, or a cheaper evaluator of the candidate.
- Projective root/histogram tests are necessary, not sufficient. Sylvester Hadamards pass every pair histogram and fail Fourier equivalence. The complete anchored-grid criterion extends to arbitrary N; the independent implementation uses a gcd-unit pivot, while the source implementation is dyadic.
- A stronger conditioning-free inverse-support bound is proved: one inverse row of support s implies `||M-F||_2>=sqrt(1-s/N)`. Pure inverse products with support bound s^t therefore have error at least `sqrt(max(0,1-s^t/N))`. Sums do not inherit inverse sparsity.
- A stronger common-frame stationary bound is proved: rank commutator at most r<N implies error at least `cos((2 floor(r/2)+1)pi/(2N))`. For t stages of q stationary path Green terms, r<=2qt, so the floor tends to one when qt=o(N). Arbitrary masks and independent path permutations require separate treatment.
- Newly supplied nested Phase19 independently verifies fixed-middle-monomial signatures, the banded inverse one-norm bound `(b/a^2)[1+2w(b/a)^2]`, resulting gain/conditioning budgets, and the one-Harper-middle-monomial exclusion. Call/stage counts do not prove an unrestricted scalar-operation lower bound for shared computation.
- The real-core and one-complex-mask axis-count restrictions are correct under their distinct assumptions. Dense positive controls do not supply a fast transform.

Reports: `phase19_audit/`, `phase20_audit/`. Exact source-family reconstructions at N=8,16,32 match. Larger source experiments are preserved as source-reported and were not rerun.

## Exact bridge and phase-aware Green extension

- For fixed a, beta_h=beta_0+hK gives M orthogonal block projectors P_h/M whose sum is I. Averaging the complete row bank therefore gives exactly F. Fewer than M rank-K row sketches cannot determine every arbitrary input from that linear transcript alone, even with nonlinear decoding. The exact/adaptive/randomized scope is made explicit in the bridge report.
- The straightforward complete bank costs O(NM+N log K); at M=Theta(log N) this is Theta(N log N). Shared local analysis gives the ordinary N log M plus N log K factorization scale. No universal shared-evaluator lower bound follows from these schedules.
- The exact near-grid residual matrix has Vandermonde rank N/gcd(N,Q), with Q the dyadic lift length. An exact separated correction needs at least that many terms; at odd N its rank is N. Completing the beta bank for each short approximate term computes the truncated center exactly without removing its bias. Different nonseparable corrections remain outside this obstruction.
- A new independently reviewed phase-aware displacement obstruction permits products of sums of c D^a P B^-1 P^-1 D^b, with constant-coefficient path denominators, integer linear phases and independent affine conjugations P. Common-frame displacement costs at most rho=2 per inverse; affine-conjugated paths cost at most rho=4.
- For b expanded branches and d distinct total phases, exact Fourier equality requires `N<=d(1+sum r_branch)<=d(1+rho t b)<=b+rho t b^2`. Fixed summand bound q>=2 therefore forces t=Omega(log N), without conditioning assumptions. One branch forces t>=(N-1)/rho. A common phase at even N improves the exact rank target to N and admits the same cosine spectral-error bound.
- Arbitrary diagonals, arbitrary path permutations, independent left/right affine factors and bare affine-multiplier wiring are outside that grammar. The reviewer gives a nearly full-rank bare-affine counterexample. This is an architectural stage bound, not an unrestricted scalar-operation lower bound.

Reports: `astra_exact_bridge/` and independent `twisted_bound_review/REVIEW.md`.

## All-length approximation and charged variant

- The v10 dyadic near-grid Bessel/Chebyshev lift is algebraically valid. Using the same state for all rank terms preserves per-output variance `(M/N)(1+tau_R)^2 ||x||_2^2`, without an R multiplier. Its deterministic bias is at most `tau_R ||x||_2` per coordinate.
- This is a fixed-input randomized simultaneous-output approximation, not arbitrary exact recovery. It does not automatically preserve the previous sparse-spectrum exact promise after input weighting.
- The uploaded prototype uses Theta(RN) Chebyshev storage, uncharged/uncertified special-function evaluations and floating grid indices. Naive forward Bessel recurrence is an unstable repair. N=1 needs its direct case. The endpoint failure target N^(-a) is vacuous at a=0 unless multiplied by a fixed constant below one.
- The independent rational-Taylor variant generates a rational rho approximating pi via finite Machin sums, with certified error eta, and tail `eta+|rho|^R/R!`. Streamed powers/factorial recurrences and exact integer indices charge coefficient generation in O(RN+log(1/eta)) arithmetic work for a fixed number of random rows, with O(N) arithmetic storage.
- Under the inherited specified dyadic row/root contract, its deterministic rounding ledger covers weights, coefficients, row error, cancellation, sum, normalizer and robust classification/radii. It is conditional implementation mathematics, not certification of the uploaded binary64 code. Growing rational/floating bit costs and exponent range remain charged.

Reports: `lift_audit/`, `taylor_extension/`. Independent full-state covariance controls through Q=32 agree numerically; 6,240 exact-rational finite-precision recurrence checks pass. Numerical controls corroborate proofs without certifying a production evaluator.

## Provenance and reproduction

The batch adds 77 new byte contents versus the declared source union through 16:46: 73 text/data files, three bytecode files and one new nested Phase19 archive. There are 656 recursive member occurrences, 472 unique hashes and 799 passing embedded checksum entries. Full sources, Library identities, hashes, fresh independent scripts and portable rerun records are preserved. Uploaded code and bytecode were never executed.

Main synthesis: `THREE_LATEST_AUDIT.md`. Source inventory: `SOURCE_PROVENANCE.md` and JSON records. No publication-priority or chat-only completeness claim is made.


# Retained detailed checkpoint through 16:46 UTC

The following earlier results remain valid within their stated models. The latest section above and additions/1717/ supersede its frontier descriptions where indicated.

9 October 2026. Includes the baseline master, the 14:50 and 15:20 additions, the three archives received at 16:28 UTC, and the spectral-determinant archive received at 16:46 UTC. Original dated inventories and audits remain preserved.

## Goal and present answer

The target remains an independently justified exact Fourier transform for every fresh arbitrary input and every output coordinate, with genuinely sub-N-log-N charged work. Root/coefficient preparation, routing, conversions, workspace, precision where claimed, and explicit outputs count.

The project has not established that target. Nor do its restricted obstructions prove an unrestricted Fourier arithmetic lower bound. Approximation, sparse-spectrum exact recovery, Boolean inputs, finite-field controls, pair-unitary circuits, additive Green sums and unrestricted complex arithmetic are different models.

## 1. Exact algebraic route: a 12-equation regular target, with exceptions retained

The fixed-permutation F8 two-separated-generator-stage problem retains its independently reconstructed older formulations:

- 30 quartics in 26 variables for an inverse-stage regular chart.
- 25 sextics in 21 variables after Fourier-support elimination; on the nonzero-t chart, primitive cancellation gives four cubics, six quartics, one quintic and fourteen sextics.
- 176 quadratics in 184 variables for the complete separated-generator lift, including zero-anchor corners.

The 16:28 dual-support/onion source gives two further reductions on smaller explicit open loci:

- First lower-column and upper-row elimination: 20 polynomials in 16 variables, degree at most 9.
- A second column gives a three-character recurrence; a second row eliminates the remaining interior generators. For n>=6 and the specified first three permutation entries, the selected conditions have an eight-parameter rational reconstruction, with (n-4)(n-5) remaining identities. At n=8 this leaves 12 rational equations in eight parameters.

Neither statement solves those remaining equations or proves inconsistency. The eight parameters do not parametrize complete Fourier factorizations without the residual conditions.

The new reconstruction requires nonzero first-row prefix expressions S, second-row elimination determinants Delta, and a boundary 2-by-2 determinant. These join the previous nonzero denominators, second-stage anchors, det(C), and inverse-stage corner conditions. The independent audit supplies a characteristic-zero Q(zeta8) exceptional partial point with S1=0 and all required old determinant/corner conditions nonzero, certified through a valid mod-97 reduction. It proves the new S exclusion is substantive, but fails the remaining equations and is not a full factorization.

The old normalization fixes diag(A), while the inverse chart fixes diag(A^-1); they are not interchangeable. The exact example A=(7/6)I-(1/6)J has diagonal one but inverse (6/7)I-(6/7)J has zero diagonal. The earlier regular-chart saturation product had degree 59, with a degree-60 reciprocal equation. Clearing denominators in the newer rational system likewise cannot silently discard excluded branches. An independently exported 3,750-node exact rational circuit records the eight-variable F8 target and 29 nonzero guards.

The older unsaturated sextics contain a spurious all-ones-matrix beta-line. Neither the original rank-60-to-61 local jet obstruction nor the newer reduced chart excludes F8 globally. The complete lift remains necessary for exception coverage.

### Latest exact-branch refinement: spectral determinant and adjacent tail

The 16:46 audit independently matches the 45-term quartic Q, three degree-seven upper resultants, a five-variable necessary determinant circuit, and the 31-term cubic W. All 898 polynomial coefficients match. These necessary projections supplement the twelve residual equations; they are not sufficient replacements. A nonzero Jacobian witness establishes algebraic independence, not emptiness or the codimension of the zero fiber.

The adjacent-column tail lemma is useful on excluded onion branches: separated tails, invertibility and the actual upper-stage rank constraint force two tail recurrences without dividing by S or Delta. Substitution into the normalized lower-generator formula still requires its own assumptions. Solving the tail recurrences introduces a new nonzero affine pivot; its zero branch remains open. Full factorization of W is undetermined.

A fresh GF(17), z=9 enumeration reproduces 78,608 h tuples and zero full-B successes among 2,546 invertible candidates; 1,927 also meet every final corner guard. Of 12,358 reconstruction rejects, 710 have alpha=0 and dependent columns, while 11,648 are omitted denominator branches. The search retains zero beta-coefficient and singular gamma cases where permitted. This is a finite-field open-branch exclusion, not a complex-field or extension-field exclusion. No valid exact F8 factorization or characteristic-zero nonexistence certificate was found.

Full report and exact certificates: `additions/1646/SPECTRAL_DETERMINANT_AUDIT.md`. Retain all twelve residuals, the nonzero guards and the complete lift for broader exception coverage.

## 2. Approximate chirp route: unit-step decoding and sharper variance

The inherited v7/v8 dyadic construction used two output cycles and covariance (2M/N) times a rank K(M-1)/2 projector. The specified v8 gauge decoder already had a complete independent numerical contract in the 15:20 audit.

v9 replaces the quadratic phase with the integer-valued binomial phase a*t*(t-1)/2. For N=p^L=KM, with K and M powers of the same prime, M>=2 and K>=M, a unit step gives one output cycle. A parity-dependent linear phase makes its monodromy -1, so one balanced scan supplies both total and prefixes, including the seed.

For each output the exact one-row error covariance is

Q_m = (M/N) Pi_m,

where Pi_m is an orthogonal projector of rank N-K. At output zero,

Q_0[n,n'] = (M delta[n=n'] - 1[n congruent to n' mod K])/N.

Thus its nullspace is the K-periodic input subspace; other outputs have the corresponding diagonal modulation. This is an explicit covariance/error-nullspace statement, not an arbitrary-input exact-transform construction. At M=1 the covariance is zero, so its norm is zero rather than M/N.

The same three shifted grids and Boyer–Moore counters give simultaneous all-output error at most

(5/sqrt(2)) g sqrt(M/N) ||x||2

with failure at most 2N exp(-R D(1/2 || 1/g^2)), under the exact-arithmetic quantization contract and its stated parameter range. The deterministic radius improves by sqrt(2) compared with the preceding construction. Work per row remains O(N+K log K); streaming storage is O(N) words.

Claims obtained by choosing M=Theta(log N) require a fixed or bounded prime, or explicit prime-dependent constants. A nearby power of an unbounded prime need not be Theta(log N); prime N has no nontrivial admissible M under K>=M. Mixed-prime lengths do not inherit the projector theorem merely from K>=M.

For the specified dyadic implementation, the earlier explicit bound transfers:

row numerical error <= 800 sqrt(NM) log2(N) u ||x||2,

provided 8u log2(N)<=0.01 and the same certified-root/normalizer, exact-index, range, pairwise-summary and normalized radix-2 short-FFT contract holds. The v9 seed charges half the total-scan error plus prefix error deterministically; no independence assumption is needed. Odd prime powers still need an explicit certified short-FFT constant.

Taking u <= theta g/[800 N log2(N)] bounds deterministic numerical error by a chosen fraction of the stochastic radius. Certified norms and inflated grid radii preserve the failure argument. This theorem covers the specified implementation, not the uploaded NumPy/native prototypes or arbitrary fixed IEEE precision. Root setup, exact represented-grid classification, bit cost, exponent range and input/output bits remain charged. Space is O(N) words, not bits. Source benchmark timings are source-reported and were not rerun. The source's short-FFT input-error contract needs a separate input-perturbation term when exact summaries cancel; the independent theorem supplies it. Its default constant 64 is not certified. Native summaries are sequential, timings omit root/plan setup, and the saved five-row benchmark parameters have a vacuous generic all-output confidence bound.

### Two bounded extensions, with different guarantees

An independent exact structured-input corollary is available for a fixed input with at most h nonzero Fourier coefficients. For prime-power N, a row's off-diagonal Fourier interaction requires m-j congruent to a*d mod K for some 0<|d|<M. Its diagonal equals one, and the interaction probability is at most 2M/K. Consequently exact-value Boyer–Moore on R=2s-1 rows recovers every output exactly except with probability at most

N binom(2s-1,s) (2hM/K)^s.

This uses exact arithmetic, exact complex equality, a sparse-spectrum promise and charged root/short-FFT primitives. It is not an exact dense-input or finite-precision result. For fixed h and fixed prime, choosing M=Theta(log N) and three rows gives O(N) arithmetic work and O(h^2 log^4(N)/N) failure. This is a restricted sparse-Fourier corollary, not a novelty claim or the unrestricted project target.

For arbitrary composite N=KM with 2<=M<=K, the projector shortcut fails, but an independent masked-shell proof gives a usable variance bound. Let D(N,M) count divisors g of N with g<M and let L=ceil(log2 M). Then

||Q|| <= [(M-1)/phi(N)] min{D(N,M), 2(L+1)^2}.

The extension provides a sharper computable shell-count bound as well. Substituting the proved variance proxy into the robust decoder gives a composite-length approximation with an explicit accuracy loss. Factorization and phi/divisor preparation are charged: trial division takes O(sqrt(N)) word divisions for array length N, so these need not be hidden oracles. Linear work per row still requires an appropriate divisor M near log N; no uniform all-integer-length speed theorem follows. The stronger tested inequality ||Q||<=M/phi(N) remains a conjecture. Numerical sweeps and exact rational-entry checks do not prove it.

## 3. Independently ordered Green sums: a broader restricted obstruction

The newly included nested Phase17 studies the additive architecture

A = sum_r L_r P_r^-1 B_r^-1 P_r R_r,

where each B_r is invertible with half-bandwidth w_r in its own order, P_r conjugates both row and column labels of that summand, and L_r,R_r are diagonal. Put W=sum_r w_r. Coefficients may be complex, nonunitary, noncommuting and ill-conditioned.

A common separator exists in all q orders with equal group size at least

m* = ceil(floor(N/2) / 2^(q-1)).

The uploaded weaker floor(N/2^q) bound remains valid. Across this separator A has rank at most W. Every normalized Fourier submatrix of size m has squared Frobenius norm m^2/N and operator norm at most one. Hence exact equality requires m*^2<=WN. When m*>W and m*^2>WN, the uniform operator-norm error is at least

sqrt((m*^2/N-W)/(m*-W)).

For bounded bandwidth this forces logarithmically many summands, but does not prove a scalar-operation lower bound for shared-state evaluation. It does not cover arbitrary products of sums or arbitrary non-diagonal outside mixers. The independently permuted row/column case is covered by the separate weaker separator extension below.

A bounded independent synthesis combines the sharper separator with the complex prime-order DFT's full-spark theorem: for prime N, exact equality requires N<=2^q W+1. In particular, two tridiagonal Green summands are excluded for every prime N>=11. This uses characteristic-zero Chebotarev theory, not arbitrary finite-field full-spark. It improves the uploaded prime monotone-chain threshold, with no publication-priority claim.

A second independent extension closes the source's proposed escape through distinct row and column permutations inside each summand. Sorted row/column position lists always admit strictly separated subsets of size floor(m/2), even if their original label sets overlap. Iterating gives m=floor(N/2^q), so the original all-length rank and spectral-gap bounds also hold for sum_r L_r P_r^-1 B_r^-1 Q_r R_r with independent P_r,Q_r. For prime N this gives N<=2^q(W+1)-1. The stronger ceil-rounded matched-order bound is not claimed here; two tridiagonal terms with independent endpoints are excluded at prime N>=13.

Products of Green sums can escape the additive crosscut bound. Passing that rank test is necessary architectural progress, not evidence of correct Fourier coefficients or a low-cost transform.

## 4. Harper and phase coherence: exact certificates, no fast executor

Phase18 adds a sparse self-dual operator H=T+V, where T is the cyclic nearest-neighbor shift sum and V is the cosine diagonal. For N divisible by four, the even and odd reflection sectors are irreducible Jacobi matrices, each with one zero mode. Fourier acts differently on those two zero lines, so no scalar rational function of H with an invertible denominator equals F.

Adding reflection parity gives a correct polynomial representation with exact degrees N/2 and N/2-2. The top even coefficient is 1/(2 sqrt(N)). Direct sparse Horner application is quadratic; degree alone is not an unrestricted arithmetic lower bound.

For even N>=4, the joint commutant of T and V is span{I,J}. Therefore the exact sparse intertwining identities MT=VM and MV=TM force M=F(aI+bJ); calibrating M e_1=F e_1 fixes M=F. These are useful symbolic certification targets. Exhaustively probing them is not a faster black-box equality algorithm.

For fixed invertible outside factors A,B, Weyl covariance of A Q P B forces A^-1 D A and B Z B^-1 to be monomially similar. Diagonal multisets and directed two-cycle products give necessary vetoes for every intermediate diagonal Q and permutation P at once. A veto for sampled fixed factors is not an all-parameter exclusion. Modular nonzero witnesses lift only when the relevant root map and inverses/denominators reduce correctly.

The real eigenbasis identity F=O Lambda O^T with a four-phase diagonal Lambda is a positive algebraic control. No fast O application is provided; allowing its growing coefficient field also explains why it does not contradict the earlier single-mask field-descent obstruction.

## 5. Unitary route and earlier filters retained

- Phase15's exact normalized Fourier factorization uses N log2(N)/2 pair-unitary gates. Its Fourier-bank costs are not removed by further optimizing the already-linear fold.
- Phase16 compiles a full path/Haar–Green stage into at most (11N/2)-8 pair-unitary gates, giving at least N log2(N)/(11N-16) stages for exact F. Adaptive prefix pivoting repairs a generic degenerate-column pivot issue. Parameter preparation is not automatically linear-time.
- Entropy continuity retains logarithmic stage count for exactly unitary approximants with fixed error below one in the stated operator or normalized-Frobenius norms. Zero-initialized ancillas do not remove the pair-unitary count; nonunitary/shared-state circuits remain outside this result.
- Common-order noncommuting tridiagonal resolvents retain additive expanded-expression cut-rank budgets. This is a consequence of inverse rank and rank subadditivity, not a general Fourier lower bound.
- Products with inverse-stage row sparsities s_j require product(s_j)>=N. Dense inverses and sums need separate analysis.
- Common-base rational functions, low-cut-rank local-port solves, field descent and Galois phase-support tests retain their original stated scopes.
- Quadratic polynomial decoding of a deficient fixed linear sketch cannot recover every Boolean input's full linear target; worst-case randomized success is at most 3/4. Cubic interpolation escapes that restriction without supplying a faster transform. Realification and conjugate-bin symmetry remain explicit.

## 6. Why the branches do not collapse into one claim

The chirp result is a fixed-input probabilistic coordinate-error guarantee with a nonlinear robust decoder. The Green-sum bound concerns uniform operator-norm approximation by a particular linear architecture. The unitary entropy theorem concerns reversible two-coordinate gates. The polynomial/rational reductions characterize specified algebraic charts. A success or obstruction in one is not automatically transferable to the others.

Dense support, high cut rank, fast individual solves, correct covariance, small polynomial systems and exact small examples each address only part of the target. A candidate exact algorithm still needs complete identities for arbitrary input and size, exception handling, and a fully charged evaluator.

## Decisive next results

1. Solve or exclude the explicitly saturated 12-equation F8 regular system, then cover every excluded branch using the complete lift. Numerical residuals and finite-field infeasibility alone do not settle the complex problem.
2. For a noncommuting product candidate, prove the two sparse intertwining identities symbolically and calibrate one vector, while verifying that its architecture and total cost escape the applicable rank and entropy restrictions.
3. Implement the specified certified dyadic v9 numerical contract before claiming an end-to-end practical guarantee. A precision theorem does not certify the uploaded benchmark binary.

## Source and evidence record

The baseline remains a dated snapshot of 349 Library items and 528 canonical text contents. The 14:50 and 15:20 additions contribute respectively 50 and 58 byte-new contents relative to their declared predecessor sets. The 16:28 batch contributes 90 relative to all preceding member and top-level source hashes: 88 text/data contents, one new nested Phase17 archive stream and one compiled binary. Two other nested archives match previously supplied top-level archives and are inherited. Its 562 recursive member occurrences have 381 unique hashes, and all 714 embedded hash entries pass.

The 16:46 addition has 194 recursive member occurrences, 180 unique byte contents and 29 byte-new contents relative to the declared preceding union; all 490 embedded checksum entries pass. Its nested predecessor exactly matches the 16:28 dual-support archive.

Uploaded code and the compiled binary were not executed. Independent proof reconstructions, fresh check scripts, finite-field controls, numerical stress tests and source-reported claims are labeled separately. No publication-priority claim is made. Chat-only account coverage remains unverified.

## Navigation

- Latest determinant audit and exact/finite-field checks: additions/1646/.
- Three-branch fusion, source inventory, full proofs and checks: additions/1628/.
- Previous precision, inverse-support and Phase16 audit: additions/1520/.
- Previous jet and streaming comparison-only audit: additions/1450/.
- Baseline catalog and 528 source texts: library/.
- Earlier baseline checkpoint: checkpoint_history/baseline_CURRENT_CHECKPOINT.md.
- Earlier exact/real/Boolean corrections and route map: prior_synthesis/, boolean/, phase14/ and nonlinear/.
- Chat-only coverage limits: CONVERSATIONS.md.


## Next source batch outside this version

Six new attachments received at 19:54 UTC are assigned to a separate next-version review. They are not included as verified findings here; the completed nine-audit batch above remains unchanged.
