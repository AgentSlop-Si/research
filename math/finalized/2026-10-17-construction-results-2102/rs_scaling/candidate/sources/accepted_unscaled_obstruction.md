# Compact even RS banks cannot have polynomial unscaled Vandermonde conditioning

Date: 17 October 2026. Final-stage mathematical candidate for FUS-06 / NF-03 / Q20.
This is a new derivation at the explicitly fixed scope below, not a claim of external novelty or whole-owner completion.

## 1. Exact goal and inherited facts

The previously accepted compact-family theorem gives a deterministic legal parameter from the grid

    {1/(2N), 2/(2N), ..., 2N/(2N)}

and the envelope κ₂(V) ≤ 2^(2N³), with paid but exponential general certified preparation. That theorem and its legal-node proof are retained; neither is being re-proved here.

The remaining goal selected here is sharply bounded:

> Can a better choice of the compact parameter t, keeping the same pencil and the same unscaled square moment Vandermonde, produce polynomial-in-N conditioning for all even lengths?

The answer is **no**. The obstruction holds for every complex parameter |t| ≤ 1, hence for every member of the accepted real rational grid, not just the least legal choice. The result is independent of a parameter-selection algorithm. It does not identify the condition number of a different scaled basis or of the Fourier transformation itself.

### Source-bound model

Let N = 2h ≥ 4, q = exp(2πi/N) in the canonical positive complex embedding, and c_j = q^[j(j−1)/2]. Define

    R_n(z) = ∏_(k=0)^(n−1) (z−q^k) = Σ_j r_(n,j) z^j,
    P_n(z) = Σ_j (c_n/c_j) r_(n,j) z^j,
    B_t(z) = z P_h(z) + t P_(h−1)(z),
    m = h+1.

These are exactly the conventions in the accepted even-bank proof and compact-family review. B_t is monic of degree m. Let α₁,...,α_m be all its roots, counted with multiplicity. When they are distinct, define the same square moment matrix

    V[j,i] = α_i^j,   0 ≤ j ≤ h, 1 ≤ i ≤ m,

with Euclidean operator norm and no row or column normalization. For repeated roots V is singular, so its condition number is infinite. The compact bank's additional requirements α_i ≠ 0 and α_i^N ≠ −1 are retained for the accepted application, but the obstruction does not need them.

The source formula is over all primitive q, but the quantitative bound below uses the canonical q specified by the accepted conditioning theorem. A different primitive embedding is not silently included.

## 2. Exact second-power identity

**Lemma.** For every complex t and every even N ≥ 4,

    Σ_(i=1)^m α_i² = −4 q^(−3)/(1−q) − 2t.                    (1)

**Proof.** Since q^h = −1 and q² ≠ 1,

    S₁ = Σ_(k=0)^(h−1) q^k = 2/(1−q),
    S₂ = Σ_(k=0)^(h−1) q^(2k) = 0.

The first two elementary symmetric sums of 1,q,...,q^(h−1) are therefore S₁ and (S₁²−S₂)/2 = 2/(1−q)². Thus the top three coefficients of R_h are

    1,  −2/(1−q),  2/(1−q)².

The P_h coefficient multiplier at z^(h−1) is c_h/c_(h−1) = q^(h−1) = −q^(−1). The multiplier at z^(h−2) is c_h/c_(h−2) = q^(2h−3) = q^(−3). Because P_(h−1) is monic, the top three coefficients of B_t are

    B_t(z) = z^m + [2q^(−1)/(1−q)] z^(m−1)
                 + [2q^(−3)/(1−q)² + t] z^(m−2) + ... .

Newton's second identity, valid also for multiple roots, gives

    Σ α_i² = [2q^(−1)/(1−q)]² − 2[2q^(−3)/(1−q)²+t]
            = 4q^(−3)(q−1)/(1−q)² − 2t
            = −4q^(−3)/(1−q) − 2t.

This proves (1). ∎

There is no asymptotic or numerical step in this identity. In particular the parameter contribution is −2t, not +2t, and the phase is q^(−3).

## 3. Quantitative spectral obstruction

**Theorem.** Let N = 2h ≥ 4, let |t| ≤ T, and suppose

    A_N(T) = [2 csc(π/N) − 2T]/m > 0.

For the above V,

    κ₂(V) ≥ max{1, A_N(T)^(h/2)/sqrt(m)}.                    (2)

In particular, for every complex |t| ≤ 1 and every even N ≥ 44,

    κ₂(V) ≥ max{1, (9/8)^(N/4)/sqrt(N/2+1)}.                (3)

For every sequence t_N with |t_N| ≤ 1 and nonsingular V_N,

    liminf_(N→∞, N even) log κ₂(V_N)/N
         ≥ (1/4) log(4/π) = 0.0603911188... .                (4)

The conclusion remains true with infinite condition number at singular lengths. More generally, (4) holds for |t_N| = o(N).

**Proof.** Write ρ = max_i |α_i|. From (1), the triangle inequality, and |1−q| = 2 sin(π/N),

    m ρ² ≥ Σ_i |α_i|² ≥ |Σ_i α_i²|
           ≥ 4/|1−q| − 2|t|
           ≥ 2 csc(π/N) − 2T.

Hence ρ² ≥ A_N(T). A column of V corresponding to a root of modulus ρ has last entry of modulus ρ^h, so σ_max(V) ≥ ρ^h. The zeroth row consists of m ones. In particular,

    σ_min(V) = σ_min(V*) ≤ ||V* e₀||₂ = sqrt(m).

If V is nonsingular, dividing proves κ₂(V) ≥ ρ^h/sqrt(m) ≥ A_N(T)^(h/2)/sqrt(m). Also κ₂(V) ≥ 1. If V is singular, the statement is immediate with κ₂(V) = ∞. This proves (2).

For T = 1, sin(π/N) ≤ π/N and π < 22/7 give

    2 csc(π/N) − 2 > 7N/11 − 2.

The rational comparison with (9/8)m is exact:

    7N/11 − 2 − (9/8)(N/2+1) = 13N/176 − 25/8.

At N = 44 the right side is 1/8, and it increases with N. Thus A_N(1) > 9/8 for every N ≥ 44. Since h/2 = N/4, this proves (3). The lower bound including its polynomial prefactor can be below 1 at some small admitted N; the maximum with 1 avoids claiming otherwise. The assertion is a uniform exponential-growth obstruction, not a large finite lower bound at the threshold.

Finally,

    [2 csc(π/N) − 2]/(N/2+1) → 4/π > 1.

Take logarithms of (2), divide by N, and use h/(2N) = 1/4 and log(m)/N → 0. This proves (4). If |t_N| = o(N), replacing 1 by |t_N| leaves the same limit. ∎

### Consequence for the accepted finite grid

Every one of its 2N parameters satisfies 0 < t ≤ 1. Therefore every legal member, including the least legal member selected in the accepted theorem, satisfies (2)–(4). In particular there are no fixed constants C,d and no sequence of legal compact-grid selections for which κ₂(V_N) ≤ C N^d for all even N. Indeed (4) has a strictly positive right side, whereas log(C N^d)/N → 0.

This conclusion does not require a theorem that the first grid point is always legal. It also does not discard or remove a possible zero bank residue: the matrix here uses all m polynomial roots, exactly as does the accepted square moment solve. A different reduced-residue matrix is outside this claim.

## 4. Scaling, arithmetic, and preparation boundaries

The following distinctions are necessary:

1. The result is for the exact unscaled square matrix V[j,i] = α_i^j. Permuting roots, applying unit-modulus diagonal phases, or multiplying the entire matrix by one nonzero scalar does not change κ₂. General row/column rescaling or a different polynomial basis can change it and is not ruled out.
2. The root-radius mechanism is a genuine obstruction to the specified condition target. It is not a lower bound on the numerical condition number of the final unitary Fourier target, whose 2-norm condition number is 1. Endpoint phases and final cancellation cannot change the stated matrix, but a different algorithm need not solve this system as an unstructured perturbed problem.
3. The lemma concerns all roots even if some bank residue vanishes. It does not prove h-pole optimality, the behavior of an h-column reduced system, or a lower bound for every scalar common-shift bank construction.
4. A large matrix condition number describes worst-case input sensitivity. For any invertible V and ε > 0, taking x equal to a top right singular vector and δb along a bottom left singular vector gives relative solution change exactly κ₂(V)ε for relative right-side change ε. This does not prove that the one fixed chirp right side c = (c₀,...,c_h) realizes this worst case.
5. Exponential κ is compatible with polynomial bit complexity because log₂ κ can be linear in N. Thus (3) does **not** rule out polynomial-bit certified preparation, and it does not claim a lower bound for all structured algorithms. Nor does it improve or invalidate the accepted p+O(N³) sufficient precision budget.
6. Exact legal-node selection, resonance margins, accepted upper bounds, and simultaneous query operation counts remain inherited facts. This packet executes no production evaluator and supplies no practical runtime or memory benchmark.

## 5. Fresh controls

`fresh_controls.py` was written for this candidate. It imports only installed general-purpose arithmetic libraries and executes no historical program.

- For every even N = 4,...,128, it constructs R_h directly by multiplying the factors (z−q^k) in Q[q]/(q^N−1), applies the exact c_h/c_j coefficient multipliers, and reduces cleared-denominator identities modulo Φ_N(q). It checks the two top coefficients and (1) independently of the proof's closed forms.
- The dependence on t is handled as an exact formal coefficient cancellation; all 2N rational grid members at each checked N are separately verified to be distinct and in (0,1]. No finite grid check is presented as a legality re-proof.
- Wrong-phase q^(−2) and omitted −2t variants must fail exactly at each checked N.
- Rational arithmetic checks the advertised N ≥ 44 constant through N = 10000, including its exact N = 44 margin of 1/8 and failure of this particular sufficient comparison at N = 42. The affine formula in the proof, not this finite sweep, supplies the all-N result. N = 44 is a convenient uniform threshold, not a claimed optimal threshold.
- A separate numerical three-term matrix produces roots for N in {4,6,8,16,24,32,44,64,128}, including complex unit-disk parameters, t = 0, and an out-of-disk control. Numerical root sums are compared to (1). At modest sizes direct SVD checks the elementary spectral inequality. These numerical values are sanity checks, not certified root or condition-number enclosures.

`RESULTS.json` records the actual completed cases and limitations. `SOURCES.json` pins the inert accepted inputs by immutable repository URL and exact UTF-8 digest. `MANIFEST.json` freezes this candidate's files.

## 6. Resolution and justified stop

**Resolved at this scope:** polynomial conditioning cannot be obtained by any choice of |t| ≤ 1 within the accepted pencil when the square moment coordinates are unchanged. The target has a proof-level negative resolution, so further parameter searching for that exact goal is mathematically unnecessary. The new result goes beyond merely recognizing the existing exponential upper envelope.

**Still unresolved here:** useful conditioning after explicitly paid rescaling or a different basis/pencil, polynomial-bit certified preparation, the fixed-right-side stability of a structured solver, a practical production executor and matched FFT comparison, exact h-pole optimality, general primitive embeddings, and FUS-06's separate Q08 obligations. No whole-owner archive or closed status follows.

**Stopping condition met:** an all-even-N obstruction covers every parameter admitted by the chosen compact-family target, with exact source conventions and fresh finite controls. This packet stops after that bounded result and independent review; it does not silently replace the target with another normalization or keep expanding the research program.
