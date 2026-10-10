# Unequal block and coprime Green audit

Audit date: 9 October 2026. Both sources label their research 10 October 2026. Original archives are preserved unchanged. Uploaded source and bytecode were treated solely as data: no uploaded program was imported, compiled, or executed. The independent checker in this directory was written for this audit.

## Main conclusions

The v14 unequal-block Green identity is valid. For an arbitrary positive partition with maximum block length L and 2(L−1)<N, its random projection is unbiased, its spectrum obeys the stated antiperiodic one-cycle recurrence, and its forcing can be evaluated in O(N log B+B²) ideal scalar arithmetic for B blocks. Balanced partitions work for every N≥3 and 3≤B≤N; N=1,2 require trivial separate branches. This is exact evaluation of a random projected signal, not exact recovery of the original DFT.

The overlap covariance bound is valid and slightly stronger than the older grouped-mask certificate in general. Its least-prime specialization was already in the master; the previous exact least-prime spectral refinement can be stronger still. The source repeats a semiprime formula that needs separate prime-square handling.

The shipped implementation is an algebraic prototype. It allocates a B-by-B Vandermonde matrix, so its general memory is O(N+B²), although an O(N)-space version is easily specified. Large-B fixed-precision stability is absent and the saved data records overflow. Its weak median row-count helper can overflow on valid inputs. Optimizing the direct-prime row's variance-only independent-median certificate against its work ledger yields order N log N for fixed energy-relative accuracy and polynomially small failure; that is a restriction of this ledger and proof pipeline, not a lower bound on other algorithms.

HERO0 Phase 4 is a different route: it embeds into a convenient composite length, then uses Gaussian resampling. Its displayed covariance improvement holds in the deliberately rough padded-length family, and also follows from the weighted overlap fusion proved below. It does not resolve the arbitrary-composite sharp-covariance conjecture. Its all-length shrinking-error theorem is supported conditionally in the explicit supplied-constant arithmetic/RAM model of the completed companion review, preserved in `companion_evidence/GAUSSIAN_ALL_LENGTH_AUDIT.md` (SHA-256 `eced2bc72d85f7cf4666dac4d1ba9faaf2c268cb343bcc497261edd2bb206cad`). For fixed 0<alpha<1/2 and c>0, it gives O_(alpha,c)(N loglog N) work, all-bin error O_alpha(N^(−alpha))||x||₂ and failure at most N^(−c) for sufficiently large N, with h>(1+c)/(1−2alpha), 2h−1 independent rows, and the stated sampling/abort contract. Inputs must be fixed independently of fresh random states. This support does not extend to certified binary64 or bit complexity.

The exact complete M-row frame identity is valid, but the supplied evaluator still pays M length-K FFTs and M length-Q scans. At M=Theta(log Q), it remains O(Q log Q). No arbitrary-input exact faster FFT or novelty result is established.

## Source identity and scope

- v14: `../source_archive/fft_rough_length_green_v14(1).zip`, 69,428 bytes; SHA-256 `39e251f37c672f6353b41997264f71831bbf0796f3b7d7348f0a7be092b389df`; Library identity `[private-id]`.
- HERO0 Phase 4: `../hero0/source_archive/fft_hero0_phase4_coprime_green_2026-10-10.zip`, 34,930 bytes; SHA-256 `e4ec42967e8e2cf803723759a55731d7202ce1d0f821eddc64ffafe6978d447d`; Library identity `[private-id]`.

The complete extracted trees and per-member hashes are preserved beside their archives. All 21 entries in v14's own SHA-256 manifest and all 16 entries in HERO0's own manifest verify. Our full manifests additionally cover the source manifest itself and v14's shipped bytecode. The duplicate `v13_composite_cycle_core.py` and HERO0 `composite_cycle_core.py` are byte-identical to the previously audited v13 composite core (SHA-256 `226e18d6cbae68b5c064a5c4a0b4aa0e7762405ecbf7613c136240ae176e610e`). This core is not a new executor.

Prior evidence copied read-only into `prior_evidence/`: the 19:54 divisor audit, 16:28 composite covariance extension, and Word-RAM v3 audit. The original master and Library have not been changed.

## Unequal block algebra

Let contiguous blocks have starts s_b, lengths l_b, and endpoints e_b. Put zeta=exp(2 pi i/N), eta=exp(pi i/N), h=N mod 2. For a unit a modulo N and beta uniform modulo N define

    S_b(t) = zeta^[a t(t−1)/2+(a s_b+beta)t] eta^(h t),
    d_b = sum_t S_b(t) x_(s_b+t),
    y_(s_b+t) = conjugate(S_b(t)) d_b.

For distinct local t,u, averaging beta annihilates zeta^[beta(u−t)]. Thus E_beta P=I for every fixed a, and E[U_N P x]=U_Nx. A block P_b is a positive semidefinite rank-one matrix with P_b²=l_b P_b; it is a scaled projection, not an idempotent projection unless l_b=1.

The local polynomial p_l(r)=sum_(0≤t<l) zeta^[−a t(t−1)/2−rt] eta^(−ht) satisfies

    p_l(r)=1+zeta^(−r)eta^(−h) p_l(r+a)
               −zeta^[−a l(l−1)/2−rl]eta^(−hl).

Substitution yields Y_k=F_k+zeta^[−(k+beta)]eta^(−h)Y_(k+a), with F=(D−E)/sqrt(N), D_k=sum_b d_b zeta^(−k s_b), and E_k=sum_b c_b d_b zeta^(−k e_b), using the source's c_b. Since a is a unit, k_j=aj modulo N is one full cycle. The gauge G_j=zeta^[a j(j−1)/2+beta j]eta^(hj) has G_N=−1: for even N, a is odd; for odd N, the eta factor supplies the minus sign. Therefore

    Y_0 = (1/2) sum_j F_(k_j)/G_j,
    Y_(k_j) = G_j [Y_0−sum_(i<j)F_(k_i)/G_i].

This proves the decoder rather than merely matching a numerical FFT.

The endpoints cyclically equal the starts, so D and E have the same nodes lambda_b=zeta^(−s_b). A sum s_k=sum_b w_b lambda_b^k obeys the degree-B recurrence with q(z)=product_b(1−lambda_b z). Given B past values, one convolution with q forms the new-block right-hand side; multiplying by q^(-1) mod z^B solves the triangular Toeplitz system. The setup and first B moments cost O(B²); there are O(N/B) blocks, each using O(M(B)) arithmetic. Including compression, phases, the scan, and output gives

    O(N+(N/B)M(B)+B²),
    O(N log B+B²) when M(B)=O(B log B).

This is an exact complex-arithmetic accounting with suitable roots/constants. A finite-field verification using schoolbook products checks algebra, not a uniform fast polynomial multiplication theorem over every field. Generating all chirp phases needs only multiplicative recurrences once the roots are supplied. The NumPy implementation instead evaluates floating exponentials. Neither representation establishes exact bit complexity or arbitrary-size integer safety.

## One forcing stream is sufficient

Let end_b be the boundary weights reindexed into start-node order. Then

    F_k = (1/sqrt(N)) sum_b (d_b−end_b) lambda_b^k.

The same recurrence can be run once on w=d−end. The uploaded core runs two channels and subtracts afterward; the fused formula is an independently verified constant-factor improvement. It preserves the same setup degree, work exponent, randomness, and decoder. It does not fuse separate random rows or recover lost input information.

The checker verifies single-stream forcing against two streams and against a direct exponential sum in every one of its 1,237 exact finite-field decoder cases.

## Covariance and comparison with the master

For nonzero signed displacement d, let D_d be the diagonal mask selecting input coordinates whose shifted partner remains in the same block. Let Pi_g be the orthogonal Fourier projector onto the gcd shell {k:gcd(k,N)=g}, g=gcd(N,d). Beta averaging removes unequal displacements under 2(L−1)<N. Multiplication of a uniform unit by d is uniform on its shell. Up to a harmless output-dependent diagonal unitary,

    Q = sum_d D_d Pi_g D_d / phi(N/g).

The PSD inequality Pi_g≤I gives

    Q ≤ diag_i [sum_(d allowed at i) 1/phi(N/gcd(N,d))].

Thus the source's overlap bound V_ov is correct. For a position t in a length-l block the bracket is the prefix sum through t plus the prefix sum through l−1−t.

The older master bound C sums, over shells, the maximum mask count divided by the corresponding totient. Taking the maximum after adding those nonnegative weighted counts is no larger:

    V_ov ≤ C < two-sided triangle sum, for nontrivial equal blocks.

This can be strictly better than C, not just the v13 triangle certificate. For N=12, block length M=3, the new overlap bound is 3/4 whereas C=1. This lies within the older M≤sqrt(N) scope. The older independent logarithmic mask bound may still be retained in the minimum; the new overlap proof does not automatically dominate every previous bound.

For M equal to the least prime p of composite N, all short displacements are units and V_ov=(p−1)/phi(N). That constant was already an explicit corollary in the older master. The 19:54 audit supplied a stronger exact spectral description. In particular p²|N gives exact norm (p−1)/phi(N), while p² does not divide N admits a strict improvement involving the least eigenvalue of the local mask matrix. Do not replace that refinement by the looser source bound.

The semiprime specialization must read:

    N=pq, p<q: V_ov=1/(q−1).
    N=p²:      V_ov=1/p.

The source's unqualified displayed 1/(q−1) misses the square case. Its general formula and totient implementation remain valid.

## A prime covariance refinement

For prime N, Pi_1=I−11*/N, so the covariance has the exact formula

    Q = diag_i(l_(block(i))−1)/(N−1)
          − [1/(N(N−1))] sum_d m_d m_d*,

where m_d is the 0–1 mask vector. This is a diagonal matrix minus a positive semidefinite mask Gram matrix. It proves V_ov=(L−1)/(N−1), and also identifies when that upper bound is sharp.

If at least two blocks have maximum length L, take the difference between the same local coordinate in two such blocks. Every mask has equal values on those two coordinates, so all mask inner products vanish. This is an eigenvector with eigenvalue (L−1)/(N−1); hence the certificate is exactly sharp.

If precisely one block has length L>1, equality would require a vector supported entirely on that longest block and orthogonal to every restricted mask. The positive-displacement masks restricted there are all nonempty proper prefixes, and the negative masks are suffixes. Together they span that block: successive prefix differences isolate all but the final coordinate, and a suffix isolates the final coordinate. Therefore such a nonzero vector does not exist, and the norm is strictly below the displayed upper bound. The all-singleton case has zero covariance. These are bounded spectral refinements, not a general composite solution.

## Bulk error works at every length

Using unitarity, P_b²=l_bP_b, and E P_b=I gives the exact identity

    E||U_N P x−U_Nx||₂² = sum_b (l_b−1)||x_(I_b)||₂².

If Z_tau counts bins with error greater than tau||x||₂, then

    E[Z_tau/N] ≤ (L−1)/(N tau²),
    Pr[Z_tau/N > (L−1)/(N delta tau²)] ≤ delta.

These statements hold for every admissible integer length and partition, without prime or roughness assumptions. They are often stronger than applying V_ov separately to every output, as the source does in its displayed bulk bound. They do not identify the exceptional frequencies, guarantee every bin, or give coefficientwise relative accuracy.

## Direct prime amplification and work

For prime N and balanced B=o(N), V=(ceil(N/B)−1)/(N−1)=Theta(1/B). This is a worst-case uniform covariance scale; the actual tail probability of a particular input need not be Theta(1/B).

For a desired complex error epsilon||x||₂, declare a row good if its complex error is at most epsilon||x||₂/sqrt(2). Chebyshev gives p=min(1,2V/epsilon²). For odd R=2h−1, a majority of good rows puts the real and imaginary coordinate medians within epsilon||x||₂. Thus

    Pr[any bin bad] ≤ N Tail_Binomial(R,p; h)
                    ≤ N binom(R,h) p^h.

The exact binomial tail is preferable when p is not small; the subset bound can be wasteful. For fixed epsilon>0 and target delta N^(−c), c≥0 and 0<delta<1 fixed, a sufficient regime is

    R=O_(epsilon,c)(1+log N/log B),

for growing B with p bounded safely below 1/2. For fixed sufficiently large B, R=Theta(log N). The corresponding independent-row work ledger is

    R [N log B+B²].

It cannot be optimized to o(N log N) through this variance-only certificate. A precise scoped argument is: if B² already exceeds order N log N the setup term alone prevents that ledger; otherwise B=o(N), so p=Theta(1/B). The binomial upper-tail expression itself contains the all-R-bad term p^R. Making N times that expression at most delta N^(−c) requires R log(1/p)≥(c+1)log N+log(1/delta). Hence R log B=Omega(log N), and the ledger contains Omega(N log N). Taking fixed sufficiently large B and R=O(log N) achieves O(N log N), establishing the order of the optimized certificate/ledger. The same conclusion follows with logarithmic, polylogarithmic or subpolynomial growing B. Shrinking epsilon=N^(−alpha) only increases the demanded row information; it does not rescue this calculation.

This is not an actual failure-probability lower bound. Chebyshev can be very loose, and neither the given big-O row theorem nor this certificate rules out a better implementation, different decoder, correlated construction, Gaussian lift, packed model, or different estimator. Shared recurrence setup across rows also does not remove the main R N log B term in this particular separate-row design.

The exact-Fraction sample ledger checks use a screened small-p subset bound at N=101,1009,10007,100003, tolerance 1 and failure at most 1/N. They illustrate the formulas and are not a universal parameter optimization or a timing measurement.

## Source implementation discrepancies

1. **Memory:** `arbitrary_block_core.py:226–230` materializes a B-by-B Vandermonde when N≥B. Thus its general memory is O(N+B²), not O(N+B). In the source's B=N^o(1) regimes, B²=o(N) eventually, so its stated asymptotic examples still have O(N) storage. A uniform O(N)-space design can generate one initial moment at a time with B running node powers, retaining O(B²) time and O(B) initialization workspace.
2. **Median helper:** `covariance.py::variance_only_rows_for_union` rejects p≥1/2, but its actual bound equals N(4p)^h for R=2h−1. If 1/4≤p<1/2, that bound cannot decrease. At N=17, B=5, V=3/16, tolerance 1 gives p=3/8, so the bound is 17(3/2)^h. For any requested failure below 1 it never succeeds; the expression `2.0**rows` eventually overflows. This is established by exact algebra and static reading, not by running the source. Use an exact/stably evaluated binomial tail or an appropriate sharper bound, and handle unreachable certificates explicitly.
3. **Precision:** source v14 benchmark data includes enormous errors and infinities for squared-logarithmic B. Its finite-field checks prove algebra only. Initial phases, polynomial coefficients, scan and cancellation all need a numerical error budget. No fixed-precision theorem is supplied.
4. **Randomness:** both source samplers cap unit rejection. Conditional on acceptance they are uniform. An unconditional probabilistic guarantee must add R(1−phi(N)/(N−1))^T for R rows and T attempts per row, or use an equivalent certified sampler. The cap counts calls to the bounded-integer RNG, not its possible internal rejection work; deterministic fair-bit work needs the separate bounded pair-trial repair specified in the completed companion review. A fixed public pseudorandom seed is reproducibility, not a guarantee against seed-dependent inputs.
5. **Scope:** `balanced_partition` enforces N≥3 and 3≤B≤N. Its looser prose “every integer length” needs the trivial small-N branch. The raw arbitrary-length covariance helper checks total length and aliasing but does not explicitly reject every nonpositive partition; the theorem requires positive lengths.
6. **Diagnostics:** v14's robust experiments use direct O(NB) exponential forcing, not the fast recurrence. They support no sub-N-log-N all-output runtime claim. The saved reports and tests are historical data; this audit does not relabel them as independently rerun tests.

## HERO0 weighted overlap fusion

Use a working modulus Q, a positive contiguous partition satisfying 2(L−1)<Q, and an input support S. Let g_j be nonzero diagonal input weights, and evaluate the deweighted projected row at any real frequency xi:

    A_xi = (1/sqrt(N)) sum_i g_i^(-1) exp(−2 pi i xi t_i) (Pz)_i,
    z_j=g_j x_j on S, zero elsewhere.

Here N is the original normalization/input length, and t_i may be the centered representatives used by the Gaussian construction. Subtract the corresponding P=I row. For each displacement d, the coefficient on x_j contains a mask, g_j/g_(j+d), a unit-modulus target phase, and a chirp character with frequency ad. Average beta first. The distinct displacements separate. Average a second to obtain a Fourier-shell projector, conjugated by the displacement-dependent diagonal coefficients.

For any such diagonal H_d and shell projector Pi_g≤I,

    H_d* Pi_g H_d ≤ H_d*H_d.

Consequently the exact support-sensitive diagonal certificate is

    Var(A_xi−target)
      ≤ (Q/N) max_(j in S) sum_(d allowed at j)
           |g_j/g_(j+d)|² / phi(Q/gcd(Q,d)) · ||x||₂².       (F1)

The bound is uniform in real xi. It requires no short displacement to be a unit. If all local ratios are bounded by R, then (F1) is at most

    (Q/N) R² V_ov(Q; partition) ||x||₂².                    (F2)

For equal M-blocks and every 1≤d<M coprime to Q, every coordinate has M−1 allowed shifts, so (F2) becomes exactly HERO0 P4.1:

    (Q/N) R² (M−1)/phi(Q) ||x||₂².

With Gaussian g_j=exp(pi sigma² t_j²)/sigma and support |t_j|≤tau, staying in the same local block gives |t_(j+d)−t_j|≤M/Q and hence the source's R. The representative discontinuity must stay outside the touched-block support, as required by its tau+M/Q<1/2 guard. The sharper (F1) may be much smaller than replacing all ratios by R.

This is a valid fusion of the two uploaded sources and the older masked-projector proof. It strengthens covariance accounting and applies to arbitrary padded moduli within the stated partition/support contract. It is not the unresolved uniform sharp bound O(M/phi(Q)) for arbitrary nonunit displacement patterns.

Five independent direct state-average checks include both rough and nonrough Q. For example at original N=11, Q=55, M=5, sigma²=8, the support-sensitive bound is about 0.671686 versus the source-style R² overlap bound 1.738642; the numerical covariance norm is about 0.500569. These values are diagnostics, not exact eigenvalue certificates. The universal result is the PSD proof above.

## HERO0 exact frame and source correspondence

For Q=KM, fixed a and beta_0, set beta_r=beta_0+rK, 0≤r<M. Inside each block the phase multiplier is exp(2 pi i r t/M). Orthogonality of the M characters gives

    (1/M) sum_r P_(a,beta_r)=I_Q.

All M block summaries are the positive-sign M-DFT of the locally weighted block, implementable with M times a normalized inverse FFT. This costs O(Q log M). The source then calls the existing decoder separately M times:

    M length-K transforms: O(Q log K),
    M length-Q scans:      O(QM),
    summaries:            O(Q log M).

At M=Theta(log Q), the total remains O(Q log Q). Outside that stated logarithmic-block regime the general ledger is O(Q log M+Q log K+QM), not automatically O(Q log Q). Even eliminating the scans alone would leave O(Q log K), which is O(Q log Q) for the source's K≈Q/log Q. Any proposed exact improvement must address both remaining components.

With fewer than M fixed states and a fully supported M-coordinate input block, the measurement map on that block has at most that many scalar rows and a nonzero kernel. All downstream projected outputs vanish on a nonzero kernel input. This excludes exact arbitrary-input recovery from only those measurements, including nonlinear postprocessing. It does not exclude an algorithm that retains other information, nor a randomized per-fixed-input additive approximation. Source kernel witnesses are chosen after seeds; this quantifier must remain explicit.

HERO0 `gaussian_robust` uses actual real/imaginary coordinate medians, so it does not inherit the v13 offset/Bessel three-grid certification mismatch. The old composite core is unchanged. `analytic_error_budget` and `stronger_local_noise_budget` retain older conservative formulas; Phase 4's sharper scalar is computed separately in `verify_phase4.py`. The entry point permits halfwidth, sigma and bucket overrides, so the asymptotic theorem applies only to parameters satisfying its hypotheses. There is no general finite-instance, outward-rounded all-bin certification API.

## Accuracy contracts and remaining gates

The v14 row gives per-output energy-relative variance and all-length bulk control. Its direct-prime row-plus-median calculation does not close simultaneous accuracy below N log N. HERO0 changes the estimator/evaluation problem by padding and short Gaussian interpolation; its conditionally supported all-length supplied-constant-model theorem therefore is not contradicted by that v14-specific cost conservation.

The previously audited packed Word-RAM construction has a different guarantee, epsilon L_box(x)/sqrt(N), with fixed epsilon and special logarithmic-word/table operations. The present energy-relative scales cannot be compared by dropping the input-dependent factor. For the usual L_box=sum_j(|Re x_j|+|Im x_j|), its ratio to ||x||₂ ranges from 1 to sqrt(2N). Dense vectors can make the fixed Word-RAM bound of order ||x||₂; an impulse makes it of order ||x||₂/sqrt(N). Thus HERO0's N^(−alpha)||x||₂ for alpha<1/2 improves the dense-data scale while not uniformly dominating that sparse-input bound. Arithmetic models also differ.

No source proves coefficientwise relative error, exact recovery, a binary64-safe full algorithm, or practical speed superiority. The Gaussian Poisson/truncation, short-filter segmentation, padding-search, supplied-coefficient setup and randomness obligations have now been independently reviewed in the completed companion report. That report supports the conditional all-length theorem and specifies the remaining numerical-model limitations. This report retains responsibility for the covariance, exact-frame and source-correspondence findings. No novelty certification is claimed.

## Independent checks

Run only the fresh checker:

    OPENBLAS_NUM_THREADS=1 python3 independent_checks.py

The preserved `CHECK_RUN.log` and `CHECK_RESULTS.json` report:

- 1,237 exact finite-field Green cases across N=3 through 65, including balanced and valid unbalanced partitions, with 44,476 exact output comparisons against direct projected DFTs. Roots and field primes are independently checked. The modular transform omits the irrelevant unitary normalization.
- 121 exact beta-averaged projection identities.
- 116 exact complete-frame identities and 116 exact one-row nonzero kernel controls.
- 292 exact-rational covariance assemblies with numerical PSD/norm diagnostics and exact trace checks; 25 sharp prime top-eigenvalue cases and 41 unique-longest-block strict cases.
- Seven independent full-state projection-matrix covariance averages (686 states total), agreeing with the rational formula to below 4e−16 per entry.
- Five Gaussian weighted covariance cases (10,400 states total), including two nonrough moduli, with independently materialized projection averages agreeing with the Gram formula to below 1.3e−14 in the selected quadratic forms.
- Four exact-rational sufficient-median ledger grids.
- Static AST import/call inventories and both source manifest checks.

Exact checks support the displayed algebra. Floating eigenvalues and Gaussian evaluations are not promoted to exact inequalities; the PSD proofs provide the general certificates. No uploaded tests or benchmarks were rerun.
