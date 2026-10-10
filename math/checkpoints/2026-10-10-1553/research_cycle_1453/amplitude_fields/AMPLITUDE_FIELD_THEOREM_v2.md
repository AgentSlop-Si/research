# Exact amplitude-field boundary for prime cyclotomic phase gates

Date: 10 October 2026. Independent research addendum to `new_source_audit/TECHNICAL_AUDIT_v2.md`.

## Result and status

The positive-rational restriction can be replaced by an exact field-intersection condition. Let p be an odd prime, ζ = exp(2πi/p), E = Q(ζ), K any subfield of R, L = K ∩ E, H = Gal(E/L), and h = |H| = [E:L]. Positivity always means positivity in the displayed real embedding, not total positivity at every algebraic embedding.

1. Mandatory target-phase coverage holds for all positive-K representations of pth roots **if and only if L = Q**.
2. The minimum number of global phases for a depth-one, positive-K, parallel-edge realization of the entire unnormalized Fourier matrix Fp[i,j] = ζ^(ij) is exactly **h+1**. Amplitudes in L already attain it.
3. Subject to using this minimum palette size, the exact minimum edge count is

   E_min = (2p−1) + h(p−1)(p−h)
         = h p² − (h−1)((h+2)p−(h+1)).

4. Three phases suffice if and only if K contains E+ = Q(ζ+ζ⁻¹). In that case a uniform explicit palette is {1, ζ^((p−1)/2), ζ^((p+1)/2)}, and E_min = 2p²−4p+3. Thus the audited 33-edge F5 example is the first nontrivial instance of an all-odd-prime construction.
5. For fixed finite-degree number field K, coverage holds at every prime p not dividing disc(K), so only finitely many prime lengths can escape this obstruction within that fixed field.

These statements are restricted phase/amplitude results, not a fast Fourier algorithm or an unrestricted circuit lower bound. The ingredients are classical cyclotomy, Chebotarev's prime-Fourier minor theorem, and positive-basis linear algebra. The particular synthesis and optimized depth-one formula have not been priority-cleared. They should be tracked as a proved field-boundary refinement of the existing v32 path gate, not automatically counted as historically new mathematics.

## 1. Model and exact algebraic criterion

A finite scalar linear DAG has disjoint input and output terminals. Every relevant edge has weight a_e ζ^(r_e), where a_e ∈ K is strictly positive and r_e ∈ Z/pZ. Parallel edges are permitted and charged individually. No free endpoint gauges, signs, normalizations, or non-K amplitudes are supplied. A path's amplitude is the product of its edge amplitudes, hence positive in K. Aggregating all paths with each phase gives nonnegative masses c_r ∈ K.

For a particular input-output pair, put C(X) = Σ_(r=0)^(p−1) c_r X^r. Then

    Σ_r c_r ζ^r = ζ^k
    if and only if
    m_(K,ζ)(X) divides C(X)−X^k in K[X],

where

    m_(K,ζ)(X) = m_(L,ζ)(X) = ∏_(a∈H)(X−ζ^a) ∈ L[X].

Consequently the relation space on the p phases has K-dimension p−h. It is the truncated ideal of this minimal polynomial, not generally the one-dimensional span of Φp.

To justify base change, EK/K is the splitting field of X^p−1. Restriction identifies Gal(EK/K) with H: if J is its image in Gal(E/Q), then the fixed field E^J is E∩K = L, so J = Gal(E/L). Thus [EK:K] = h and the orbit product above is the minimal polynomial. Equivalently E and K are linearly disjoint over L. This does not require K/Q to be finite or algebraic. This is the standard Galois base-change theorem; see [Milne, Fields and Galois Theory, Proposition 3.19 and its infinite extension 7.15](https://www.jmilne.org/math/CourseNotes/FT.pdf).

If an initially named coefficient field is a subfield of C rather than R, positive real amplitudes belong to K∩R. Apply the theorem to that real field. Arbitrary complex amplitudes are a different model.

### A complete positive-cone criterion, including descent

Fix a phase set S and target k. Choose an L-basis of E. Let A_S have as columns the coordinate vectors of ζ^r for r∈S, and let b_k be the coordinate vector of ζ^k. These coordinates lie in L. The target is realizable precisely when

    A_S x = b_k,     x ∈ K_(≥0)^S.

Moreover this is feasible over K if and only if it is feasible over L. To prove the nontrivial direction, take a K-solution and retain its strictly positive support T. Row reduction over L parametrizes all solutions of A_T x = b_k as an affine L-space. Its given real point has all coordinates strictly positive. Approximate the free real parameters by elements of Q⊂L; positivity persists in an open neighborhood. This gives an L-solution with the same zero pattern outside T. In the zero-dimensional case the unique solution already lies in L.

Thus a larger real coefficient field changes these feasibility questions only through its intersection with E. This is an exact finite-dimensional cone test, not an efficient uniform circuit generator or a coefficient-bit-complexity bound.

## 2. Independence lemma from classical prime-Fourier minors

**Lemma.** Every set of at most h distinct pth roots is K-linearly independent.

**Proof.** Suppose Σ_(r∈S) a_r ζ^r = 0 with a_r∈K and |S|≤h. Apply the h automorphisms of EK/K indexed by H. The coefficients a_r remain fixed, producing the system

    Σ_(r∈S) a_r ζ^(tr) = 0,    t∈H.

Choose |S| distinct rows t∈H. The resulting square matrix is a prime Fourier minor, which is nonzero by Chebotarev's theorem. Hence every a_r is zero. See [Tao, Lemma 1.3, An uncertainty principle for cyclic groups of prime order](https://arxiv.org/pdf/math/0308286). The theorem and its earlier provenance are explicit there. □

In particular, if ζ^k is represented without its own phase, at least h distinct contributing phases are needed: otherwise the representation and target would give a nontrivial dependence among at most h roots.

## 3. Gaussian periods give both directions of the coverage boundary

Because L⊂R, complex conjugation belongs to H, so −1∈H and h is even. For the multiplicative cosets C of H in (Z/pZ)× define the real Gaussian periods

    η_C = Σ_(r∈C) ζ^r ∈ L.

Their two elementary moment identities are

    Σ_C η_C = −1,
    Σ_C η_C² = p−h.

For the second identity, parameterize ordered pairs in the same coset by (r,rt), with r≠0 and t∈H:

    Σ_C η_C² = Σ_(t∈H) Σ_(r≠0) ζ^(r(1+t)).

The summand t=−1 contributes p−1, and each of the other h−1 choices contributes −1. This proves p−h. Gaussian periods themselves are classical objects, not a new construction in this addendum.

### If L = Q

Then h=p−1 and m_(K,ζ)=Φp=1+X+⋯+X^(p−1). Since C−X^k has degree at most p−1, it equals tΦp for some t∈K. Therefore

    c_r = t + 1[r=k].

Any r≠k shows t≥0, so c_k≥1 and the target phase must occur. This statement permits irrational coefficients in K when K∩E=Q. Integer path-count conclusions require integer path masses and do not follow from this field condition alone. The classical vanishing-sum context is [Lam and Leung, On vanishing sums for roots of unity](https://arxiv.org/abs/math/9511209).

### If L ≠ Q

Then h<p−1, hence p−h>1. If all η_C were nonpositive, their sum −1 would imply Σ_C η_C²≤(Σ_C |η_C|)²=1, contradicting the second moment. Thus some η_D>0. It follows that

    1 = (1/η_D) Σ_(r∈D) ζ^r.

All h amplitudes are the same strictly positive element of L; phase 0 is absent. Rotating the identity gives a missing-target representation of any ζ^k. By the independence lemma, h terms are optimal among missing-target representations. This proves coverage fails whenever L≠Q, and proves the exact iff statement.

## 4. Sharp global palette theorem

### Lower bound

Suppose a phase palette S realizes every entry of Fp at depth one. Its phases positively span every pth root because row i=1 contains all p phases. Their K-linear span therefore has dimension h. If |S|<h, this is impossible. If |S|=h, the phases form a linear basis. Summing nonnegative representations of all p roots would give a nonzero nonnegative dependence on that basis, because Σ_r ζ^r=0. This too is impossible. Hence |S|≥h+1.

Equivalently, summing the target representations gives a nonzero nonnegative relation among the at most h palette roots, contradicting the independence lemma. The dimension proof clarifies the connection to classical positive bases.

### Explicit attaining palette

Since Σ_C η_C=−1, some coset C has η_C<0. Set

    S = {0} ∪ C,                  q_0 = −η_C,  q_r = 1 for r∈C.

Here exponents denote phases. Then |S|=h+1, all q_r are strictly positive in L, and

    Σ_(r∈S) q_r ζ^r = 0.

Any h of these roots are an L-basis of E by the independence lemma. For an arbitrary root, first write it in an h-root basis, extend by one coefficient zero on the remaining palette element, and call the resulting coefficients b_r∈L. Let

    t = −min_(r∈S) (b_r/q_r).

Because one b_r is zero, t≥0. The coefficients b_r+tq_r are all nonnegative, at least one is zero, and they represent the same root. Thus every root uses at most h palette terms. All coefficients remain in L.

If the target is outside S, the independence lemma forces exactly h nonzero terms. If the target lies in S, one direct term suffices. Therefore S realizes all Fp with h+1 phases, proving sharpness. This is a concrete Gaussian-period positive basis, rather than an appeal to planar convexity. Planar Carathéodory alone would not justify a field-constrained statement when h>2.

The underlying positive-dependence theory is old: [Chandler Davis, Theory of Positive Linear Dependence, American Journal of Mathematics 76 (1954), 733–746](https://www.jstor.org/stable/2372648). Publisher metadata was checked; its full text was not available in this research pass, so no exact Davis theorem-number attribution is made.

## 5. Exact edge optimization at minimum palette size

This section concerns depth one with **exactly the minimum palette cardinality h+1**. It is not an edge bound when all p phases are permitted.

Every included target phase needs at least one edge. Every omitted target phase needs at least h edges by the independence lemma, even if repetitions are allowed, and the construction attains h. In Fp, phase 0 appears 2p−1 times; every nonzero phase appears p−1 times. A minimum palette including 0 covers

    (2p−1) + h(p−1) = (h+2)p−(h+1)

entries with direct edges. The remaining (p−h−1)(p−1) entries each use h edges. Therefore

    E_min = (2p−1) + h(p−1) + h(p−h−1)(p−1)
          = (2p−1) + h(p−1)(p−h).

A palette of the same size omitting 0, when such a palette is possible, has h+1 nonzero phases and costs (h−1)p more edges. The negative-period palette already includes 0, so the optimum is attained without a rotation argument.

If L=Q, h=p−1 and all p phases are required; the formula reduces to p². If L≠Q, restricting the palette to its minimum increases the edge count above the p² unrestricted-palette direct construction. There is no asymptotic speedup here.

## 6. Maximal-real subfield and the explicit all-prime triangle

For odd p, [E:E+]=2, and L⊂E+. Thus h≥2. The sharp palette size h+1 is three if and only if h=2, if and only if L=E+, if and only if E+⊂K.

Let a=(p−1)/2 and θ=2π/p. The palette S={0,a,p−a} has the positive dependence

    (2 cos(π/p))·1 + ζ^a + ζ^(−a) = 0.

For 0≤k≤a,

    ζ^k = [sin((a−k)θ)/sin(aθ)]·1
          + [sin(kθ)/sin(aθ)]·ζ^a.

The coefficients are positive for 0<k<a; endpoints use one edge. They belong to E+ because each sine ratio is a quotient

    (ζ^u−ζ^(−u))/(ζ^a−ζ^(−a))

fixed by complex conjugation. Conjugating the displayed identity handles p−a≤k≤p. Since p−a=a+1, these cases cover every root. The same argument works for the conjugate ζ. An arbitrary choice of primitive root is handled by relabeling exponents so that the geometric triangle has the indicated angles.

For Fp this uses exactly 2p²−4p+3 edges. At p=3, all three phases are present and nine direct edges result. At every p≥5 it uses s=3 phases and depth d=1, yet the positive-rational variable-depth count would give binom(d+s,s)=4<p. This is a full-matrix counterexample to extending that rational gate to unrestricted positive real amplitudes. It is quadratic-size, with algebraic amplitude complexity left uncharged by this edge-only statement.

## 7. General DAG alphabet and path consequences

Let B be the set of available path-phase residues of a positive-K circuit computing all Fp. Each transfer entry is a nonnegative K-combination of phases in B, so the palette lower bound gives |B|≥h+1, even when B arises from a deeper network.

If the global edge-phase alphabet has size s and every path has at most d edges, there are at most binom(d+s,s) possible exponent-multisets. If every path has exactly d edges, the bound is binom(d+s−1,s−1). Consequently necessary conditions are

    binom(d+s,s) ≥ h+1                      (depth at most d),
    binom(d+s−1,s−1) ≥ h+1                  (depth exactly d).

These may overcount residues and are only necessary conditions. They recover the original threshold p precisely when L=Q. No sufficiency claim about sparse graph realization follows. The lower bound h on distinct phases in a missing-target representation also gives a lower bound h on contributing paths, but paths are not interchangeable with arithmetic work or edges in a shared DAG.

## 8. Fixed coefficient fields recover the obstruction almost everywhere

Let K be a fixed real number field. If L=K∩Q(ζp) is nontrivial, the prime p ramifies in L: p is totally ramified in Q(ζp), and ramification descends to every nontrivial intermediate field. Since L⊂K, ramification-index multiplicativity implies p ramifies in K, hence p divides disc(K). Thus

    p ∤ disc(K)  ⇒  L=Q  ⇒  mandatory coverage and minimum palette p.

The total ramification used here is standard; see [Milne, Algebraic Number Theory, Proposition 6.2(c)](https://www.jmilne.org/math/CourseNotes/ANTc.pdf).

Examples: K=Q(√2) never escapes at an odd prime; K=Q(√5) can escape only at p=5; at p=13 the quadratic subfield Q(√13) has h=6 and minimum palette seven. More generally, if [K:Q]=D, then h≥(p−1)/D, so the minimum palette is at least (p−1)/D+1. The all-prime three-phase construction uses a varying/growing field E+ or a larger infinite real field containing the required subfields. Saying merely “irrational positive amplitudes” omits this decisive distinction.

## 9. Fresh exact controls

`fresh_exact_controls.py` was authored for this addendum and imports only the Python standard library. It does not read, import, or execute source-package programs. It performs arithmetic in Q[X]/Φp using exact rational coefficients. Positivity is certified with rational intervals: Machin's arctangent identity bounds π, and Taylor remainder bounds certify each cosine evaluation. No numerical tolerance is used for equality or positivity.

Results in `FRESH_EXACT_RESULTS.json`, with the terminal run in `FRESH_EXACT_RUN.log`:

- All 18 real subfields at p=3,5,7,11,13,17,19: fixed-field membership of periods and amplitudes, both period moments, signs of the needed periods, minimal-polynomial orbit products, exact positive palette relations, every root representation, and all 3,314 Fourier entries.
- All non-rational-intersection cases in that set have an exact h-term missing-target certificate and an h+1-phase full-matrix certificate; the minimum-palette edge formula passes in every case.
- The explicit all-prime triangle at p=3,5,7,11,13,17,19,23,29,31,37,41,43: all root identities and 8,253 Fourier entries, with certified positive E+ amplitudes and the edge formula.
- p=2 is checked separately: E=L=Q, h=1, two phases, four direct edges, and mandatory coverage. It has no nontrivial real cyclotomic field boundary.

These are finite exact controls of the displayed constructions, not a computational proof of Chebotarev's theorem, a historical-priority search, or a uniform bit-complexity audit. The JSON includes full exact coefficient vectors in the power basis 1,ζ,…,ζ^(p−2), so individual certificates can be rechecked independently.

## 10. Prior art, scope, and what remains unresolved

Primary-source search checked Tao's paper in full for the required minor theorem, Milne's Galois and algebraic-number-theory notes for base change and ramification, Lam–Leung's author preprint record for classical vanishing-sum context, and the original Davis publication metadata for positive-dependence context. Additional searches included Gaussian periods, positive spanning roots of unity, and coefficient-field-constrained positive relations. An unavailable Davis full text and an imperfectly parsed Gaussian-period survey were not treated as fully reviewed sources. Failure to find this exact formulation is not novelty evidence.

The theorem, cone criterion, sharp palette, sharp minimum-palette edge count, and explicit construction are proved above. The open step is historical placement of this precise combined formulation and its optimized network-language corollary. The broader exact subquadratic/depth-three Fourier construction problem remains untouched. No source, accepted artifact, Sheet, Library record, or repository has been modified.

Suggested tracker binding: retain the existing Schur/path v32 restriction under the relevant SCHUR-V28 lineage, append this as its amplitude-field boundary refinement, and keep “historical novelty unresolved.” Do not increment a new-theorem count solely on this addendum.
