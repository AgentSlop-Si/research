# Independent review: ranking, orbit gate, and cross-mode Phase 7

9 October 2026 UTC. Bounded review against the supplied version-13 master. Source filenames dated 10 October are preserved unchanged. No uploaded program, test, helper, bytecode, or nested program was executed or imported. The mathematical checks here are newly authored and separate from the uploads.

## Result

The new ranking mixes legitimate unanswered construction questions with architectures now excluded by this round’s independent reviews. No evidence justifies its numerical ordering as a probability-of-breakthrough ranking. The Phase4 orbit gate is correct in its stated edge-accumulation model. Its displacement identity and coprime routing congruence were already proved in the master; the exact support counts and complete routed recovery description are useful additions. The later Hero0 Phase7 source gives a sound new restricted cross-mode algorithm, including zero-safe recognition of unknown shifted templates. None of these sources gives an exact arbitrary-fresh-input sub-N-log-N algorithm.

Two status changes are important. Ranking #8's unresolved phasor-table proof is stale: the master already contains a complete bounded-input, coarse-accuracy Word-RAM theorem. Ranking #4's N^(3/2) orbit execution is a displayed implementation baseline, not the best available algorithm for those coordinates: the paired construction supplies explicitly charged O(N log N) recovery and evaluation. That improvement cancels to ordinary Cooley–Tukey for the actual raw-to-output map.

## 1. Sources and byte identity

- Ranking: [private-id], 8,284-byte text, all 161 lines read.
- First Phase4 source: [private-id], 14,035-byte ZIP.
- Direct Phase4 resend: [private-id], same 14,035 bytes and SHA-256 beb92f2f7ac96b7c83c3171c4b0fb548dd72c74b8916272b7d1408f265586144. These are two source identities, one archive stream.
- Hero0 Phase7: [private-id], 130,809-byte ZIP, SHA-256 90a1dbf15e0a763ea63785552e7a4b642d7b1e08d466fe43a246d4eaec7046e2.
- Phase7's embedded prior_phase6_bundle.zip is byte-identical to the already audited Phase6 archive, SHA-256 0eda6f3c099d736e3ee2439c531cdfcc6b83f672ea3a2ff9dcb5afeda5d4cd5e. It was not re-extracted or re-executed.

SOURCE_MANIFEST.json, NEW_2159_MANIFEST.json, PROVENANCE.json and STATIC_VALIDATION.json record exact identities, current source hashes, prior-evidence snapshots, and checksums. Byte novelty is distinguished from mathematical novelty. Uploaded saved tests remain source-reported results; the independent results below are newly reproduced controls.

## 2. Phase4 routing and singular branches

Use N=QM, primitive omega, eta=omega^Q, xi=omega^M, lambda_j(h)=mu_j eta^(-a_j h), and z_s=omega^(-h)xi^(-s). The kernel is K_h[s,j]=sum_(t=0)^(Q-1)(z_s lambda_j)^t. Since z_s^Q=eta^(-h),

    (1-z_s lambda_j)K_h[s,j] = d_j,
    d_j=1-eta^(-h)lambda_j^Q.

This is a polynomial identity, so it remains valid at zero denominators. If d_j is nonzero, no denominator vanishes and every kernel entry is nonzero. If d_j=0, z_s lambda_j runs over all Qth roots of unity: exactly one entry has ratio 1 and value Q, and all other entries vanish. Characteristic not dividing N ensures Q is nonzero. A naive rational implementation must explicitly retain that routed Q entry: replacing every d_j=0 column by zero is wrong. If mu_j=0, lambda_j=0 and the column is all ones, with d_j=1; inverse-node Cauchy formulations need a separate zero-node branch, although the polynomial formula does not.

Routing occurs iff mu_j^Q=eta^((a_j Q+1)h). The congruence has either zero solutions or gcd(a_j Q+1,M) solutions. Full routing of an orbit through every h forces mu_j^Q=1 and a_j Q=-1 mod M. Thus coprimality is necessary even if different orbits are allowed different shears; common shear gives the convenient explicit sufficient construction. With coprime Q,M, a=-Q^(-1) mod M, b=(aQ+1)/M, mu_j=xi^j, the sole output satisfies j=s+bh mod Q and has weight Q.

The raw-to-B recovery in this routed construction is two ordinary Fourier banks: Q transforms of length M, then M transforms of length Q with diagonal phases. Access to B is not free. A full direct-transform implementation costs O(N(M+Q)); standard FFT primitives give O(N log N). Field/root and convolution contracts must still be stated.

For Q=M and a_j=j, mu_j=omega^j, every h has one routed column j=h and M-1 dense columns. Its routed output is s=-h^2 mod M. The exact count is M^2-M+1 per channel, or M^3-M^2+M globally. Each V_h[t,j]=omega^((1-Mh)tj) is nonsingular, since 1-Mh is coprime to M^2. Hence K_h=F_M diag(omega^(-ht))V_h has ordinary rank M while its displacement has rank one. Rank-one displacement is not a rank-one matrix or an operation-count theorem.

The master's earlier CONFLUENT_FUSION.md already contained the displacement/full-rank proof and the Qa=-1 congruence. Phase4's more detailed support classification, explicit edge count, complete routed recovery pipeline, and specific square basis are additional source content. The Weyl commutator is a standard exact identity; it excludes simultaneous diagonalization of those operators, not fast general Fourier algorithms.

### Independent strengthening: best possible routing over arbitrary shears

Let D be the largest divisor of M coprime to Q, equivalently the product of the complete prime-power factors of M whose primes do not divide Q. For any a, gcd(aQ+1,M) divides D. Conversely Q is invertible modulo D, so choose aQ=-1 mod D; no prime dividing Q can divide aQ+1. Consequently

    max_a gcd(aQ+1,M) = D.

For any g fixed shear/scale orbits, the exact number of nonzero raw kernel edges is

    E = gQM - (Q-1) sum_j r_j >= gQM-g(Q-1)D,

where r_j is the number of routed h for orbit j. In particular for Q=M and g=M, every such shear choice has E>=M^3-M^2+M. The source basis attains this lower bound. This strengthens the sparse-edge obstruction from one chosen basis to every square g=M shear basis. It applies only when the evaluator explicitly processes these nonzero orbit-output contributions. Fast dense or cancellation-based circuits remain outside the claim.

## 3. Hero0 Phase7: accepted algebra and complete scope

Write its dimensions as N=Km, K>=m>=2. Its dechirped matrix is

    V[b,t]=x[bm+t] zeta^(a binom(t,2)+(amb+beta)t).

For a known per-column shift schedule g_t, align W[q,t]=V[q-g_t,t] and certify rank r. Incremental exact row elimination costs O((r+1)N) on an accepted rank-r instance, with at most r input-dependent inversions; rejection under cap R costs O((R+1)N). With W=UH, one obtains

    G_i(u)=sum_q U_i[q] zeta_K^(-uq),
    Z_ell[t]=zeta^(-a binom(t,2)-(beta+ell)t)
                zeta_K^((ell+at)g_t) sum_i H_i[t]G_i(ell+at),
    X[ell+jK]=sum_t Z_ell[t] zeta_m^(-jt).

Frequency arguments are reduced modulo K. All r factors are combined before each small transform. Signs and output placement check exactly. The charged cost is

    O((r+1)N+rK log K+N log m),

including recognition, O(N) root tables, phase/index preparation, and all outputs. For the stated eligible dyadic lengths and m=Theta(log N), this is O(N(r+log log N)), using O(N) field words. This is not an all-integer-length theorem obtained by free padding.

### Unknown shift and template discovery

For each nonzero column, list its nonzero sites cyclically. The tokens (gap to next site, next value/current value) characterize its scaled cyclic orbit. Ratios are compared by cross multiplication of nonzero denominators. This is a genuine equivalence relation, so ordinary KMP prefix-function and doubled-necklace matching retain linear comparison complexity. Equal gaps align the exact zero pattern; equal edge ratios telescope to a single global scale. Singleton support uses gap K. The zero column is handled separately. After a match, a full-coordinate multiplication-only certificate validates the recovered shift.

Using the first nonzero column as template recognizes the one-template family in O(N). All required column scales use one batch inversion of nonzero anchors; the all-zero case needs no inversion. With up to r unknown projective cyclic template classes, sequentially compare each column with existing templates. This discovers all classes in O((r+1)N) accepted work, or O((R+1)N) bounded rejection work. Because equivalence classes are disjoint, a rejected cap cannot be rescued by a different selection of r representatives. Each nonzero column uses exactly one template. This is not an algorithm for unknown sums of independently shifted templates.

The fixed-shift rank-r family has dimension r(K+m-r), and the fixed-assignment r-template family has dimension at most rK+m-r. Their codimensions are (K-r)(m-r) and (m-r)(K-1), respectively. Finitely many shift/assignment choices do not cover generic complex inputs when r<m. Nevertheless full ordinary block rank, all m modes, dense raw samples, and maximal global Hankel rank can occur simultaneously. The supplied explicit N=128 example is independently confirmed below.

### Implementation and cost qualifications

- The fixed field p=2013265921 supports only finitely many lengths. The asymptotic exact-field theorem needs a supplied compatible root/field family or exact complex constants, and explicit FFT/root preparation. Field discovery and bit complexity are not free consequences.
- Exact zero tests, equality comparisons, and input-dependent divisions make this a branching algebraic-RAM algorithm. It is not automatically an admissible straight-line bounded-coefficient linear circuit.
- Floating formula checks do not certify exact floating membership, stability, or precision. The code performs finite-field recognition exactly.
- The source transforms return rejection when the certificate fails. The prose's conventional FFT fallback is a valid design extension, not implemented behavior in those entry points.
- In phase7_orbit_union.py, full-coordinate verification computes expected=(H*template) mod P directly, without the Counter multiplication helper. At least K times the number of nonzero columns of algebraic multiplications is omitted from the reported counter. This costs at most N and does not alter the asymptotic theorem. Comparisons, indexing, storage and root discovery are not comprehensively represented by the printed basic-field counter either. No practical speedup is inferred from it.

## 4. Exact connection to Phase4, without a false family inclusion

The layouts match after renaming Phase4's Q=m and M=K:

    y_t[b]=x[t+mb],       eta=zeta^m.

For a Phase7 one-template instance V[b,t]=h_t f[b+g_t], its Phase4 fiber spectrum is exactly

    C_t[nu]=h_t zeta^(-a binom(t,2)-beta t)
              eta^((nu+at)g_t) F_f[(nu+at) mod K].

For multiple templates, replace h_t F_f by the corresponding sum. This is a shifted lookup in the template spectrum, not necessarily a bounded sum of temporal exponentials at fixed nu. Also m=Theta(log N), K=N/m is unbalanced for the older Q^2,M^2=O(N) orbit-recognition theorem.

There is a rigorous noninclusion witness. Take f=(2,1,...,1), distinct g_t=t, and fix one channel nu. In characteristic zero, its Fourier values are K+1 at zero and 1 elsewhere, so every multiplier in the displayed formula is nonzero. Choose nonzero h_t so that C_t[nu]=1/(t+1). The raw vector is dense; the dechirped columns have rank m (an identity-plus-all-ones minor has determinant m+1). But the s-by-s temporal Hankel matrix with s=ceil(m/2) has entries 1/(i+j+1) and is a nonsingular Cauchy matrix. Any representation C_t[nu]=sum_(j=1)^g B_j lambda_j^t therefore requires g>=s. Thus a single Phase7 template does not imply a bounded Phase4 temporal-orbit count as m grows. The same witness works over the tested suitable finite fields. This distinguishes compression coordinates without asserting that one complete structured toolkit contains the other.

## 5. Ranking corrections against version 13

1. Exceptional-locus Green synthesis remains a concrete unresolved architecture after the listed fixed-family exclusions. A generic proper-algebraic-locus theorem does not exhibit an admissible exceptional Fourier factorization. It also does not apply indiscriminately to restricted parameter subfamilies without its nonzero-specialization premise. No evidence establishes this as statistically the most likely breakthrough route.
2. The previously reported repeated-bit-reversal survival is superseded. This round’s independently reviewed boundary-discrepancy theorem proves r1+r2+r3>=ceil(log2(N)/2), excluding three order-one repeated-bit-reversal stages at every dyadic N>=128. More generally, cyclic-window averaging and the classical planar discrepancy theorem force total quasiseparable order Omega(log N) for every three-stage internal-permutation family, provided at least one Fourier endpoint is affine with coprime stride; the other may be arbitrarily permuted. Thus no fixed-order growing-length family survives in that scope. Both endpoints arbitrarily non-affine, more stages, or non-quasiseparable mixers require separate analysis. See cross_track/THREE_STAGE_REVIEW.md and cross_track/BIT_REVERSAL_EXCLUSION.md, independently reviewed this round.
3. The identity A L^(-1) F R^(-1) B=A+B is correct for invertible factors, but the single diagonally gauged sum of two weighted-permutation inverses is now excluded at growing length over C. The independently reviewed cyclic additive-separator theorem requires m0^2<=2N, m0=ceil(floor(N/2)/2), and therefore excludes N=30,31 and every N>=34, in particular every dyadic N>=64. Arbitrary non-affine cycle orders, multiple cycles, zero edge weights, and independent invertible diagonal term gauges are included. The Fourier norm step is specifically over C, not a transferred finite-field lower bound. Products of sums and non-diagonal outer mixers remain outside this argument. Small surviving sizes are not thereby certified feasible. See cross_track/GREEN_REVIEW_MILESTONE.md, independently reviewed this round.
4. The displayed O(N^(3/2)) orbit-edge route is superseded as an algorithmic baseline by the paired explicit O(N log N) recovery/synthesis. The harder question is jointly beating the Fourier banks, not just beating edge enumeration. Exact finite-field invertibility does not provide complex conditioning.
5. Dense inverse structure escapes one sparse-inverse obstruction, but does not certify Fourier compatibility, cheap parameter construction, or an O(N) inverse. Inversion preserves corresponding strict complementary cut ranks, so dense-inverse stages of bounded quasiseparable order remain subject to the new three-stage exclusion. A construction must change the excluded rank/stage/endpoint architecture, not merely make inverse support dense.
6. The finite Bessel/chirp all-length lift is approximate. An exact separated residual correction already has rank N/gcd(N,Q), equal to N at odd N for dyadic Q. Pre-materialization fusion must genuinely change the representation to evade that statement. The independent-channel scan-state barrier does not by itself exclude correlated-input special methods. However, the master also has a correlation-aware first-Bessel-forcing obstruction: moving its nonconstant output weight into one fixed Green scan with the same diagonal extension requires repair rank at least max(0,K-1-(Q-N)), or K-2 at N=Q-1. Other input-side weights or a genuinely joint architecture remain open; generation/evaluation is still charged. See cross_track/THREE_STAGE_REVIEW.md, section E.
7. Phase7 now gives a concrete cross-mode relation beyond sparse global support: unknown cyclic template classes with charged recognition and all-mode output. It is a verified restricted advance, not a generic-input contraction. The older growing-rank tensor/fiber and rank-one chirp results should remain in the comparative baseline.
8. The alleged missing phasor-table proof was already completed in the master. For fixed epsilon, failure exponent c and input-width exponent C, bounded-integer/common-fixed-scale inputs on logarithmic-word RAM admit explicit all-bin approximation in O(N) word work, with error at most epsilon L_box(x)/sqrt(N) and failure at most N^(-c). Uniform tables, capped exact sampling, descriptor work, guard arithmetic, finite-accuracy constants, and output writes are charged in that theorem. Full asymptotic implementation and benchmarking remain absent; exactness, relative l2 recovery, ordinary working precision and arbitrary exact-real inputs remain outside it.

The current primary OpenAI #130 scope page was read on 9 October 2026. It separately reports a subsequential exact-circuit result and deterministic all-length DFT/convolution programs with O(n(log n)^(1-10^-13)) work. Its model supplies a root and permits exact complex arithmetic with unrestricted coefficients; scalar preparation is charged. This review does not verify the full papers or Lean development. The appropriate comparison is therefore an externally reported, model-specific baseline, not an independently certified theorem of this project. Source: https://github.com/openai/math/blob/main/lean/docs/130.md .

## 6. Independent evidence

independent_checks.py and bridge_and_hankel_checks.py run on Python's standard library alone. They do not import source uploads or the paired constructor's program. Exact finite-field checks corroborate the algebra; they are not substitutes for all-size proofs.

- 87,770 Phase4 kernel columns; 501,167 kernel entries, including 7,233 zero-denominator/resonant entries; 12,208 routing-count cases and 44 extremal-gcd cases.
- 90 square full-rank/displacement blocks, M=2 through 13, with all edge counts checked.
- 70,541 exhaustive projective cyclic-equivalence vector pairs, including zero/singleton/periodic supports and false matches.
- 96 known-factor and 96 unknown-template Phase7 raw-input cases, totaling 13,888 complete output-bin comparisons.
- The N=128 explicit source parameters independently give 128 nonzero raw values, block rank 8, all 8 phase modes, Hankel rank 64, and exact DFT agreement.
- Five exact layout-bridge families through N=2048: one dense Phase7 template, full block rank m, but temporal-channel Hankel rank m/2.
- 756 direct independent evaluations of the paired two-convolution inverse formulas, M=2 through 22, with 3,794 nonzero factorial values checked.
- 4,389 independent leading-Hankel determinant identities for the paired inverse kernel, M=2 through 29.

The sealed accompanying PEER_REVIEW.md records the current constructor review. No practical speed, unrestricted lower bound, new publication priority, finite-precision theorem, or completed universal Fourier breakthrough is claimed.
