# All-length finite-word weak Fourier approximation by constructive sparse transfer

Date: 13 October 2026 UTC. Review-incorporating edition v2. Private recovery packet.

## 0. Status and exact claim boundary

This document composes two exact source-bound inputs:

1. The explicit finite-dyadic front-end candidate `proof_snapshot_v1.zip`, SHA-256 `26b207d5d8f345493c6ec6ddcf3794220bce1280bc4d4364f85a8a15ec1bbb4d`.
2. The independently accepted downstream scope/transfer review `next_cycle_q16_parent_scope_audit_review.zip`, SHA-256 `84d6b0a45c5bc432095c8705ba84384e2825f0d46b4daab33f65e52d70784dc7`.

**Review and recovery status:** The independently accepted all-length mathematical verdict is incorporated in this edition. The exact v1 theorem, complete independent review, verdict, results receipt and prior-comparison report were restored from retained text after a workspace loss; each matches its previously recorded SHA-256. The complete E(beta) proof and the P05/finite-dyadic transfer bodies are also restored to their original hashes, as is the accepted downstream review ZIP. The original composition and all-length review ZIPs and all-length checker remain missing. The historical acceptance is preserved, but this is not a fresh independent replay or an integrated-executable certificate. `RECOVERY_SCOPE.md` identifies the preserved evidence and gaps.

The accepted review applies directly to the immutable v1 theorem, SHA-256 `4bc3e876a680cfb031d4e7d2363f81dfc713c45ef680b3a34eedb167a536d408`. This edition applies its exact harmless clarification r_amp = floor(c)+2 and incorporates the attribution and model boundaries. The previously recorded original composition ZIP hash is `f2474629f3b43b18d9e33713fc697682bf117313baabfa1a48d3b17b9af2f58a`; the original all-length review ZIP hash is `8c6b3d51589469dc7114e09324d300d34501d196b722b4aa5bb12ffb73b12a70`. Those two archives are missing, not newly sealed here. The exact text diff from the restored original is `verification/REVISION.diff`.

The accepted downstream review supplies the centered interpolation identity and its bounds from P05 section S6 (source SHA-256 `02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787`), and accepts the finite-dyadic arithmetic transfer text (SHA-256 `fed947dce547463d3829aadfe9f6e23410fb70a0b139a3b8da64d399a4cc8a9d`). We preserve those inherited mathematical premises. The current packet makes the composition, all-length branch, and every-tape accounting explicit.

A constructive finite-word algorithmic theorem does not require a production implementation to exist. Conversely a proof and finite pseudocode do not certify that any historical executable, concrete hardware random source, serializer, or integrated program implements the theorem. These are different questions. No exact DFT, relative-l2, alpha=1/2, practical speed, new analytical exponent, or historical novelty claim is made. This is a finite-word refinement of an existing weak-coordinate approximate path.

## 1. Machine, finite input family and theorem

Fix real alpha with 0 < alpha < 1/2, a fixed rational beta with alpha < beta < 1/2, a fixed c > 0, an integer d >= 1, and an integer D > alpha + 4. Set exactly

    r_amp = floor(c)+2,   J = 2 r_amp - 1.

Then r_amp > c+1 and J depends only on c. This is the accepted reviewer's witness choice, so the stated work/storage dependence is exact. If r_amp were independently prescribed instead, the constants would also depend on it. These are fixed parameters of one algorithm family, not parameters tending to their endpoints as N grows. The algorithm does not need to parse an arbitrary real c at runtime; r_amp is fixed when the family member is chosen.

For every integer N >= 1 let

    M = 2^m = 2^ceil(log2(4N)),   4N <= M < 8N.

The input is a fixed random-access vector x in C^N with the exact representation

    x_j = (a_j + i b_j) / 2^e,   0 <= j < N,
    a_j, b_j, e are integers,
    |a_j| <= 2^(d m),   |b_j| <= 2^(d m),   0 <= e <= d m.

The same exponent e is shared by all components. The input is supplied in declared bounded-width binary fields; reading and validating all coordinates is paid. Arbitrarily long malformed host encodings are not part of this domain. The vector and all pre-tape data are fixed before independent fresh ideal fair bits are drawn.

Use the negative-sign unitary Fourier transform

    (U_N x)_ell = N^(-1/2) sum_(j=0)^(N-1) x_j exp(-2 pi i j ell / N).

A word has a sufficiently large fixed multiple of log2(N+2) bits, depending on the fixed parameters and interface width constants. Word operations include exact bounded-word addition, subtraction, comparison, Boolean operations, shifts, multiplication, and index arithmetic. Quotients or larger intermediate arithmetic may instead be carried out by elementary multiword routines at their full polynomial bit cost. No unbounded-precision integer or transcendental evaluation is a unit-cost operation. Reading or writing one fixed-width input/output field costs O(1) words. Scalar interval calculations with polynomially many bits use and pay for multiple words.

**Theorem (accepted all-length mathematical existence with inherited accepted premises).** Using the independently accepted E(beta) proof and the already accepted P05/finite-dyadic transfer premises, there is a single explicitly specified randomized finite-word algorithm for all N >= 1, returning N dyadic complex numbers y such that, for every fixed valid input x,

    Pr[ ||y - U_N x||_infinity <= C_(alpha,beta,D) N^(-alpha) ||x||_2 ]
        >= 1 - N^(-c).

It terminates without mathematical abort on every valid-domain tape and uses O_(alpha,beta,c,d,D)(N) word work and O_(alpha,beta,c,d,D)(N) words of storage on every tape. Each returned Cartesian numerator and denominator exponent has O_(alpha,beta,c,d,D)(log(N+2)) bits, with denominator exponent value O_(alpha,beta,c,d,D)(log(N+2)); a constant number of growing words suffices per output. An O(N)-bit-work or decimal-JSON claim is not implied.

One permissible constant is

    C_(alpha,beta,D) = max(1, sqrt(2) (448D+70)
                                   [1 + 1/(euler_e (beta-alpha) ln 2)]).

Larger constants are harmless. The work/storage constants can be extraordinarily large near beta=1/2, because finitely many exceptional lengths are treated densely. This theorem is not a useful-crossover or performance assertion.

The normalization is essential: for the unnormalized transform F_N = sqrt(N) U_N, the corresponding error would be C N^(1/2-alpha) ||x||_2. It is not C N^(-alpha) ||x||_2. For the unit impulse x = e_0, the unitary spectrum is dense with every coordinate 1/sqrt(N). The all-zero output meets the displayed weak-coordinate tolerance for C >= 1 and alpha < 1/2, while its relative-l2 error is exactly one. The theorem therefore does not promise exact Fourier values or useful relative-l2 accuracy.

## 2. Deterministic acquisition, normalization and exact source adapter

Read and validate all N input coordinates. If all numerators are zero, write N exact zeros and stop. Otherwise let A be the maximum absolute Cartesian numerator and let k0 = ceil(log2 A), computed by integer comparisons, including the power-of-two case. Define

    lambda = 2^(k0-e),   x' = x/lambda.

Then 0 <= k0 <= dm, -dm <= k0-e <= dm, and every normalized Cartesian component is its original integer numerator divided by 2^k0. Consequently

    max_j max(|Re x'_j|, |Im x'_j|) <= 1,
    1/2 < ||x'||_2 <= sqrt(2N).

The strict lower bound follows because the largest normalized Cartesian component lies in (1/2,1]. The algorithm never needs to compute ||x'||_2.

Let a0 = floor((N-1)/2). Embed x'_j at the residue j-a0 modulo M, and put implicit zero elsewhere. Call this vector v. Store only the normalized N-vector, not an extra materialized M-vector. A queried residue is converted by exact index arithmetic to either its unique original index or zero, in O(1) growing-word operations. Since the occupied signed indices have absolute value at most N/2 <= M/8,

    R := ||v||_2 = ||x'||_2 > 1/2.

Its Cartesian components are bounded by one and have numerator widths and dyadic denominator exponent values O_d(m), exactly the candidate's normalized finite-dyadic domain. Its immutable source is fixed before fresh randomness. Acquisition, validation, max normalization, and conversion cost O_d(N) word work/storage. No additional norm/max scan is hidden inside the sublinear front end.

## 3. An exact branch rule for every length

Form the candidate's integer parameters using the fixed rational beta:

    k = 2^ceil(2 beta m),       B = 2^ceil((1/2+beta)m),
    r_win = 2m+1,              ell_win = 8B,
    W = 2 r_win (ell_win-1)+1,
    q_sel = 512k,              L_rep = 4m+1,
    P = 16m+16.

Also set

    s = Dm,   h = 16s+1,   t = 2h+2 = 32Dm+4.

Use the sparse-transfer branch only if all of the following exact predicates hold:

- B divides M, B >= 4, and T := M/B >= 4;
- B >= 4096k and W < M;
- t < M;
- beta m >= 2, equivalently 4 M^(-beta) <= 1.

All ceilings and the last comparison are exact integer/rational operations. If any predicate fails, use the deterministic dense branch in section 8. Thus the algorithm does not assume that the user supplies a correct large-length threshold.

For each fixed beta in (0,1/2), the failing set is finite. Indeed B is within a factor two of M^(1/2+beta), k is within a factor two of M^(2beta), and

    B/k >= (1/2) M^(1/2-beta) -> infinity,
    W = O(m B),   W/M = O(m M^(-(1/2-beta))) -> 0.

Eventually the exponent of B is at most m-2, making B a divisor with T >= 4; B >= 4, t < M and beta m >= 2 also hold eventually. This proves finitude without a practical crossover assertion. The front-end candidate itself has a valid finite dense branch; the outer algorithm here bypasses it by using its own directly specified dense branch whenever any front-end or transfer guard fails.

## 4. Front-end contract and its exact use

On the sparse branch, one candidate front-end call consumes the immutable source v and independent fresh ideal bits. It returns distinct valid frequency indices and complex dyadics zhat, interpreted as zero off support. Its asserted simultaneous guarantee is

    Pr[ ||zhat - U_M v||_infinity <= 4 M^(-beta) R ]
       >= 1 - 1/M.

The candidate actually bounds this failure by M^(-3); the weaker 1/M is sufficient here and matches the accepted transfer interface. There is no heavy-gap, tail-energy, known-location, or real-only promise. This is one event for all coordinates for the fixed input, not a collection of unamplified pointwise events or one tape valid for every input.

For clarity, the candidate's mathematical operations are: exact compact box-convolution coefficient construction; paid certified scalar interval evaluations for taps, normalizer, roots and phases; folded buckets and a B-point radix-two FFT performed with finite dyadic integer arithmetic; exact squared-magnitude sorting with index tie-break; complete inverse-affine fiber enumeration; exact vote counting; fresh estimation rounds; and separate Cartesian medians. The root and filter preparations are paid. No inherited source callback is assumed to supply free roots, taps, arbitrary precision, or global norm information.

There are L_rep independent location rounds and L_rep fresh independent estimation rounds. A round draws one uniformly odd slope and one uniform shift from exactly 2m-1 fresh bits, with no rejection. Therefore a sparse call uses exactly

    2 L_rep (2m-1)

bits. Temporary location candidates number at most L_rep q_sel T; distinct returned support satisfies on every tape

    S <= 2 q_sel T = 1024 k M/B <= 2048 M^(1/2+beta).

The predicate B >= 4096k also gives S <= M/4. These are all-tape combinatorial bounds, not successful-output estimates. Returned values lie on grid 2^(-P); each Cartesian numerator and denominator exponent value has O_d(m) width/range as specified. The bucket/FFT scratch may have O_d(m^2) bits, and scalar exact rational scratch has polynomial bit width; those larger intermediates receive full finite arithmetic charges. Every call has work/storage M^(1/2+beta) poly_(beta,d)(m) on every tape and no mathematical abort on valid inputs.

## 5. Constructing only the active interpolation coefficients

Put z = U_M v. The accepted P05 centered interpolation supplies the exact identity

    U_N x' = D_phase B_full z,
    (D_phase)_(ell,ell) = exp(-2 pi i a0 ell / N),
    (B_full)_(ell,k) = sqrt(M/N) K(ell/N - k/M),

where

    L_K = M/4,   q_K = floor(M/(8s)),
    K(u) = D_(L_K)(u)/M * [D_(q_K)(u)/(2q_K+1)]^s,
    D_j(u) = sum_(v=-j)^j exp(-2 pi i v u).

Retain the t distinct indices

    k = (floor(ell M/N) + j) mod M,   -h <= j <= h+1,

and call the combined retained phase/interpolation matrix C. The accepted bounds are

    |C_(ell,k)| < 3,
    ||D_phase(B_full - B_retained)||_(2->2) <= 12 * 4^(-s).

Here t < M guarantees no repeated index within a retained row. It also guarantees q_K >= 1 (indeed q_K >= 4), so the displayed kernel regime is well defined.

For each of the S returned sparse indices k, enumerate integer target indices ell in the at most three clipped intervals

    0 <= ell < N,
    |ell M/N - (k+jM)| <= h+2,   j in {-1,0,1},

using exact signed integer endpoint divisions. Test the exact floor/modular retention rule and remove duplicate incidences. This finds every true incidence. Each interval has O(h) possible targets because M/N >= 4; clipping and wraps do not create a longer interval. Thus candidate and retained incidences number O(S t) on every tape. No scan over all N rows is made to decide which coefficients or phases to prepare.

Set

    eta = 2^(-(D+3)m),   p = (D+3)m + g,

where a fixed guard g (for example three extra final grid bits, after certified evaluation to eta/2) ensures that the combined complex coefficient is approximated by Ctilde on common grid 2^(-p) with |Ctilde-C| <= eta. This is an absolute complex error, not a Cartesian error mislabeled as the complex norm.

This coefficient generator is algorithmically constructive and finite. At nonzero reduced rational u = ell/N-k/M modulo one, distance to an integer is at least 1/(NM); the sine denominator has magnitude at least 2/(NM). Dirichlet ratios are evaluated with exact rational argument reduction and certified sine/cosine intervals; at zero use their exact limits. The normalized powered factor has magnitude at most one and exponent s = O(m). Computing phase, sqrt(M/N), ratios and the power to error eta needs O(m) target/guard bits with polynomial-bit scalar intermediates. Truncated alternating Machin arctangent series, rational Taylor polynomials with factorial remainders, and integer-square-root bracketing are explicit elementary choices. Each coefficient therefore costs a fixed polynomial in m. The inherited accepted P05 coefficient argument supplies this mathematical complexity; no existing source implementation of the coefficient evaluator is thereby certified.

Most importantly, the coefficient cost is

    O(S t poly(m)) = M^(1/2+beta) poly(m),

not N poly(m). Phase coefficients can be made per active incidence, or cached only for active targets. The N dense accumulators are initialized by a plain O(N) word pass, which does not prepare N transcendental phases.

## 6. Every-tape finite sums, final rounding and the error ledger

Candidate output already has common denominator exponent P. More generally the accepted transfer can align O(m)-bounded denominator exponents exactly, but no such extra alignment is needed here. Multiply each active complex Ctilde and zhat as four exact integer products and sum signed integer numerators at common exponent p+P. There is no intermediate arithmetic rounding.

For an explicit all-tape bound, candidate section 6 has ideal bucket magnitude at most 2M^2 and uniformly tiny estimation error. Hence each returned Cartesian median has magnitude less than 3M^2. Its numerator is less than 2^w in magnitude for

    w = P + 2m + 2.

Since eta <= 1 and |C| < 3, a Cartesian coefficient numerator has magnitude less than 4 * 2^p. A Cartesian product numerator is less than 2^(p+w+3), and each row receives at most t distinct support contributions. A signed accumulator allocation of

    p+w+4+ceil(log2 t) bits

therefore suffices on every tape, including total recovery failures. This is O_d(m); it does not use a success-conditioned estimate of ||zhat||. Integer products and incidence work are charged at full polynomial bit cost inside the sparse budget. Fixed-width wrap is forbidden.

Round each Cartesian row once, nearest-even, to the common grid 2^(-b), where

    b = ceil((beta+2)m).

The complex error from that one final round is at most 2^(-b). Since R > 1/2, its contribution relative to R is at most 2^(1-b). Multiply the output by lambda exactly by changing its exponent, or by an exact numerator shift if nonnegative denominator exponents are required. This changes widths by O_d(m). All dense output values and later Cartesian medians are thus bounded-width dyadics on every tape.

On the one global successful front-end event put E_M = 4 M^(-beta). Unitarity gives ||z||_2 = R and ||zhat||_infinity <= (1+E_M)R. The accepted transfer, now with the candidate's explicit constants, gives for every coordinate

    |y'_ell - (U_N x')_ell|
      <= [3t E_M + t eta (1+E_M) + 12 * 4^(-s) + 2^(1-b)] R.    (1)

The terms are, respectively, sparse-coordinate error through the retained row; finite coefficient error applied to zhat; the interpolation tail applied to the exact z; and the sole final rounding. In particular the coefficient multiplier is t, not S or N, and the tail is not applied to an uncontrolled norm of zhat. Exact scaling by lambda preserves the inequality relative to ||x||_2.

On this branch E_M <= 1. Because D+3 > beta and 2D > beta, the bracket is at most

    (14t+14) M^(-beta)
        = (448Dm+70) M^(-beta)
        <= (448D+70)(m+1) M^(-beta).                              (2)

Let delta = beta-alpha > 0. For all m >= 0,

    (m+1) 2^(-delta m) <= 1 + 1/(euler_e delta ln 2),

using the maximum of u exp(-delta ln(2) u). Together with M >= 4N, this proves the promised O(N^(-alpha)) coordinate error with an explicit constant, before the sqrt(2) median factor. The strict beta-alpha slack is essential; neither beta=alpha nor alpha=1/2 is supplied by this proof.

## 7. Independent amplification and worst-case linear word cost

Repeat the complete sparse call and transfer J = 2r_amp-1 times using disjoint independent fresh bit blocks. Deterministic precomputed data may be shared: only the randomness needs independence. Return the separate real and imaginary coordinate medians of the J dense outputs, taking exact comparisons of common-grid dyadics.

If at least r_amp runs satisfy (1) at all coordinates, then every Cartesian median lies in the corresponding good Cartesian interval. Combining components multiplies the complex-radius bound by at most sqrt(2). This factor cannot in general be omitted. The event of at least r_amp bad runs is covered by subsets of r_amp failed runs, so

    Pr[failure] <= 2^(2r_amp-1) M^(-r_amp)
                 <= (1/2) N^(-r_amp) <= N^(-c).

This inequality is valid for every N >= 1; the separate branch guards, not the amplification, impose the large-length regime. There is no union bound over N output coordinates here: the input event for each run was already simultaneous. Reusing one tape does not amplify. The sparse outer branch uses exactly J * 2L_rep(2m-1) fresh bits; the dense branch uses none.

For some fixed finite exponent A and constant K, all front-end work, O(S t) active coefficient evaluations, exact products, sorting, source access, phase preparation and finite intermediate arithmetic for all J runs cost at most

    K M^(1/2+beta) (m+1)^A.

This bound includes unsuccessful tapes. Put epsilon = 1/2-beta > 0. Then

    M^(1/2+beta)(m+1)^A / N
       < 8 (m+1)^A 2^(-epsilon m).

The right-hand side is bounded for all m and tends to zero. Equivalently the supremum H_(epsilon,A) = sup_(u>=0) (u+1)^A 2^(-epsilon u) is finite, so this term is at most 8 K H_(epsilon,A) N. This is exactly where all fixed polylogarithmic coefficient and multiword overhead is absorbed. It is not an assumption that an arbitrary sublinear support remains sublinear after polylog factors; the explicit positive exponent gap establishes it.

The only dense passes are bounded-width input validation/normalization, accumulator zeroing, one final round per coordinate per run, J-entry coordinate medians, exact power-of-two scaling, and packed output. Each is O_(c,d)(N) word work. In particular there are no N separate polylogarithmic root/phase preparations. Storing J output arrays costs O_c(N) words; J is fixed. Sparse work/storage is o(N) eventually and O(N) uniformly. Every-tape support and magnitude bounds, rather than a successful recovery event, justify these charges.

The constant-word primitive multiplication model is explicit. Even if all sparse multiplications are conservatively charged schoolbook bit cost instead, their fixed polynomial overhead remains absorbed by epsilon. An O(N) bit-complexity claim still fails because the dense input/output may contain Theta(N log N) bits.

## 8. Certified deterministic treatment of every exceptional length

This branch is a specification of a finite algorithm, not an unspecified appeal to a dense baseline. Continue using the same normalized x' and exact scaling factor lambda. If N=1 one may return x exactly. Otherwise put

    Q = 16m+16,   rho = 2^(-Q).

Using the finite rational routines described above, prepare each root exp(-2 pi i a/N), 0 <= a < N, as a complex dyadic with absolute error at most rho. Prepare a dyadic approximation to 1/sqrt(N) with error at most rho. For example use a component grid 2^(-(Q+4)), certified scalar interval error smaller than 2^(-(Q+8)), and integer-square-root bracketing for the scale. These operations are total with predetermined O(m) targets and proved polynomial-bit scratch; no unbounded interval-refinement loop is needed.

For each ell, form exactly the dyadic sum

    sum_(j=0)^(N-1) x'_j root_tilde[(j ell) mod N],

multiply exactly by the dyadic scale, then round each component once nearest-even to grid 2^(-Q). No ideal DFT oracle or uncharged transcendental value is used. Preparing N roots is O(N poly(m)); the N^2 exact terms cost O(N^2 poly_(d)(m)). One output row can be accumulated at a time, with O(N poly_(d)(m)) words as a conservative storage bound.

Here |x'_j| <= sqrt(2) < 2, the exact scale is at most one, and rho < 1. Root perturbations change the raw sum by at most 2N rho. Using the perturbed scale changes the final unrounded result by at most 6N rho; final complex rounding contributes at most rho. Thus for every coordinate, deterministically,

    |y'_ell - (U_N x')_ell| <= 7N rho
                            < 14N rho R.

Since rho = 2^(-16) M^(-16), M >= N and N >= 1,

    14N rho <= (14/65536) N^(-15) <= N^(-alpha).

Scaling by lambda yields the theorem's error with constant one and failure zero. Root/scale denominators are O(m); exact sums add O(log N) numerator bits. Final normalized output numerators and the exact scale-back representation have O_d(m) bits on every tape. The branch uses no random bits and has no abort.

Only finitely many N take this branch for the fixed parameters. Consequently the maximum of its paid work divided by N and its storage divided by N over that finite set is finite and depends only on the fixed parameters. Absorb those finite maxima into the theorem's constants. This is a valid uniform all-length finite algorithm with possibly enormous parameter-dependent constants. It neither claims that the dense branch is intrinsically sublinear nor asserts a production executable or useful speed at those exceptional lengths.

## 9. Accepted premises and every-tape versus probability boundaries

The full theorem uses two named inherited mathematical components: the finite-dyadic E(beta) construction of section 4, and P05 centered interpolation, coefficient construction and tail bounds in section 5. The accepted downstream transfer supplies the reduction architecture. The exact-restored independent review accepts the outer all-length composition, including the deterministic fallback, and explicitly retains those dependencies. It does not reprove E(beta)'s filter/hash/location analysis or all of P05 from scratch. The complete E(beta) proof is restored to its original hash in reconstructed/E_BETA_PROOF_V1.md. The exact P05 source, transfer lemma and accepted downstream review archive are also included. Their restoration is not a new proof review or an execution of their original programs.

The restored review's verdict is ACCEPT_ALL_LENGTH_CONSTRUCTIVE_FINITE_WORD_EXISTENCE_WITH_INHERITED_PREMISES. That historical mathematical acceptance remains distinct from the incomplete local evidence recovery and the engineering certificate below. The original reviewer requested only the r_amp witness clarification to align the parameter dependence. Sections 2-8 of this edition are byte-identical to v1; their formulas and algorithmic specification are unchanged.

For every valid input and every tape, the specification guarantees totality, support/magnitude caps, bounded output fields, and the paid work/storage bounds. The deterministic dense branch also has its stated accuracy on every valid input. For each fixed input, probability at least 1-N^(-c) applies to one simultaneous weak unitary coordinate-accuracy event over fresh independent ideal bits. Failure tapes need not be accurate but keep the resource bounds. No tape is guaranteed to work for every input. Physical entropy, a seeded pseudorandom generator and an integrated implementation are not certified by this probability statement.

The unitary convention and weak norm matter: the bound is C N^(-alpha)||x||_2 per coordinate. It gives neither exact Fourier values nor a vanishing relative-l2 error. Multiplying by sqrt(N) gives the unnormalized-transform error C N^(1/2-alpha)||x||_2. All dense input/output work is paid in growing words; Theta(N log N) bit volume is compatible with the O(N) word bound. Finitely many dense exceptions can create enormous constants. No useful practical crossover is asserted.

The original STR-Q1 precise-blocker stopping alternative remains a historical completed stage. P05/S6 and R18 retain their accepted ideal O(N) weak-coordinate classification. The distinct Gaussian/Green F016 mechanism retains its accepted ideal O(N log log N) classification. Substituting a different sparse-Fourier algorithm does not improve that mechanism's own bound.

## 10. Prior analytical guarantees and attribution

The complete bounded comparison report is exact-hash restored in `reconstructed/PRIOR_COMPARISON_REPORT.md`. The substantive source-credit and classification sections of the separate attribution addendum are recovered as a fragment; its missing preamble is not invented. Their earlier pending-candidate wording is historical. Neither report is itself a proof-acceptance or novelty certificate.

[Hassanieh, Indyk, Katabi and Price, SODA 2012](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf), Theorem 4.4, already supplies the analytical specialization

    ||ztilde-z||_infinity <= sqrt(epsilon/k + M delta^2) R.

For k comparable to M^(2beta), fixed epsilon and leakage delta=O(M^(-beta-1/2)), this gives error O(M^(-beta)R), global failure at most 1/M and arithmetic work O_beta(M^(1/2+beta) log^(3/2)M). R is used in the analysis, not supplied as an input. Lemma 4.3 already supplies the success-independent vote-count support bound and unknown-location preimage enumeration. [Their STOC 2012 paper](https://groups.csail.mit.edu/netmit/wordpress/wp-content/themes/netmit/papers/SFFTstoc.pdf), section 7, Lemma 7.3, explicitly pays for supported-window construction and response evaluation. These ingredients are not new here.

[Kapralov 2016](https://theory.epfl.ch/kapralov/papers/ft-sublinear-loglogn.pdf), section 8.1, Algorithm 4 and Lemma 8.1, is a directly relevant unknown-support infinity-norm comparator. The bounded comparison derives an outer adapter using a norm envelope R <= Rbar < 2R computed during the paid input pass, and

    K = 2^(2 ceil(beta*m+4)),   chi = 0,
    nu = mu = Rbar/sqrt(K),    Rstar = sqrt(K).

Total-energy inequalities satisfy the source's displayed threshold hypotheses, including exactly sparse spectra. Its numerical abstraction then yields error at most 2M^(-beta)R plus an inverse-polynomial numerical remainder, failure M^(-10), and one-dimensional arithmetic work M^(2beta)polylog(M). That exponent is smaller than 1/2+beta. The norm envelope is paid by the outer caller and is not free in standalone scale-free E(beta). This does not certify every finite-dyadic execution path of a particular Kapralov implementation.

The cited results already match or improve the analytical sparse-front target. This consolidation makes the finite-input, precision, setup, rounding and every-tape obligations explicit for the stated construction. The bounded source comparison establishes no historical novelty for that refinement. No new asymptotic FFT breakthrough, exact-transform result, global absence claim or numerical-priority upgrade is made.

## 11. Precise remaining integrated executable work

A source-pinned integrated executable certificate is still open. It requires the following separately verifiable deliverables.

1. **Finite fields and machine interface.** Implement the common-exponent binary input, exact range checks, zero handling, max normalization, centered source adapter and bounded dyadic output. Pin the source, toolchain, dependencies and growing-word simulation. Charge parsing and serialization under the declared binary model; arbitrary malformed strings and decimal JSON are outside its constant-per-field claim.
2. **Certified scalar and filter routines.** Supply finite argument reduction, pi/sine/cosine and square-root enclosures, exact zero limits, signed nearest-even rounding and fixed precision/iteration budgets. Certify polynomial-bit intermediates and the E(beta) tap/root/phase errors, active coefficient error eta and dense root/scale error rho. Pay window and normalizer construction in full. Ordinary floating-point agreement cannot replace interval certificates.
3. **Complete E(beta) implementation.** Implement odd affine hashes, folded buckets, finite dyadic radix-two transforms, exact magnitude selection with index tie-breaking, inverse fibers, vote counts, fresh estimation rounds and Cartesian medians. Verify distinct valid support, S <= 1024kM/B, grid exponent P and every-tape Cartesian magnitude <3M^2. Include failed tapes, temporary candidates, source queries, sorting and all preparation in the resource ledger.
4. **Active transfer and finite sums.** Implement signed interval endpoints, wrapped exact retention filtering and duplicate removal. Generate only active coefficients/phases. Use the stated common exponents and signed accumulator allocation; perform one final rounding per row and exact scale-back. Exercise cancellation, empty/maximal support, negative boundaries, wraps and extreme failed-tape values. Do not introduce N polylogarithmic phase preparations.
5. **All-length dispatch and amplification.** Implement the exact rational guards and certified dense fallback, including N=1 and zero input. Fix r_amp=floor(c)+2, use disjoint bit blocks, and preserve the sqrt(2) Cartesian-median loss. Verify exactly J*2L_rep*(2m-1) sparse-branch bits and zero dense-branch bits. Define any nonideal entropy or generator assumption separately.
6. **Source-bound conformance and end-to-end checks.** Test against exact/reference transform enclosures on feasible lengths and adversarial finite inputs, all dispatch/tie/wrap boundaries, maximal fields and injected recovery failures. Provide code-to-proof width and complete-path resource arguments, plus executable counters and reproducible builds. Actual sparse crossovers can be enormous: small reduced-parameter fixtures validate components, not the full large-length theorem. Finite empirical tests alone do not establish universal probabilities or asymptotic bounds.

Evidence recovery is a separate outstanding task: restore the missing original composition/frontend archives and complete all-length review/checker evidence, then perform the desired fresh independent review or full source-bound replay. The exact-restored historical result receipt reports 23,988 dispatch cases, 267,638 retained scatter incidences, 354 error ledgers, 196 accumulator cases, 1,089 amplification cases and 120 certified dense coordinates. Those counts are historical evidence, not a claim that those tests ran again after recovery. Only newly authored recovery/revision checks are run in the present packet.

This packet is private. No repository publication, shared-sheet edit or execution of unrecovered historical code is performed.
