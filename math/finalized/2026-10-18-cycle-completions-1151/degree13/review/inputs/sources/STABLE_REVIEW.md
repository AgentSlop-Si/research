# Independent review: prime-Frobenius-stable N13 supports

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**.

## Accepted theorem and exact scope

For N=13, q=16, the original signed-resolvent physical-bank grammar with independently free nonzero effective cross singletons, and K=F_(53^d) with gcd(d,210)=1:

1. No legal representation can have exactly seven nonzero effective same-sign nodes on one side with that support invariant under x -> x^53. This assertion leaves the other support, both cross nodes, all legal beta values, and all raw weights initially arbitrary over K.
2. Every sixteen-bank witness must consequently have both seven-node same-sign annihilators outside F53[t]. Equivalently, both supports are non-Frobenius-stable.
3. Among representations for which both same-sign nonzero effective supports are Frobenius-stable, the exact physical-bank minimum is eighteen.

This is a genuine all-degree statement, not a conclusion from finite extension searches. The proof is correct. Acceptance uses the inherited field-uniform per-side seven-node lower bound and previously accepted eighteen-bank raw witness. Those two large original-matrix/lower-minor computations have not been repeated here. The one-sided base-field recurrence obstruction was independently reconstructed in this review.

Candidate REPORT.md accepted SHA256:
`8c339aefbcbd53403550597a4f621f6f8b58314256b39407693f9df585c4f638`.
The complete candidate packet and read source bodies are bound in INDEPENDENT_ARITHMETIC.json and CANDIDATE_BINDING.json. Acceptance attaches to the identified bytes, with the nonblocking explanatory correction below.

## 1. Source dependencies and original grammar

The complete retained source bodies were read. Their local SHA256 values and, where supplied, Git blob identifiers were freshly verified.

- sources/PINNED_REVIEW.md, sections 1–3, explicitly binds a field-uniform lower theorem for arbitrary legal beta: at least seven distinct nonzero effective same-sign nodes per side, and nonzero effective cross nodes. Section 2 supplies the original-bank amplitude expansion without any division by beta.
- sources/BASEFIELD_REVIEW.md, section 3, states and independently verifies the exact one-sided obstruction used here: every nonzero y in F53 gives a six-equation monic degree-seven recurrence family, and none of its 2,756 polynomials has seven distinct nonzero roots in F53. This obstruction is stronger and more specific than merely knowing the global F53 minimum is eighteen. It therefore applies after only one support and its adjacent cross node descend. One does not need the other support, beta values, or weights to descend.
- The same source, section 2, records a fully verified original eighteen-bank witness with both same-sign supports {1,2,6,7,12,21,22,26}, cross nodes 1, beta=1, nonzero guards, and all raw weights in F53.
- sources/RANK_REPORT.md gives the same forced moment equations and distinguishes the degree-37 coordinate-chart singularities from intrinsic rank loss. The new proof never divides by that chart determinant and does not use the uniform rank theorem to justify descent.
- sources/DEGREE7_REPORT.md provides the earlier attainment/stopping boundary. Its degree-seven attainment is not necessary to prove the new restricted minimum and is not re-credited or independently replayed here.

The candidate preserves the original physical-bank grammar. Effective amplitudes are merged as entire vectors. Zero-alpha banks vanish at the positive exponents used in the recurrence proof; additional repeated, ineffective, or cancellation-only banks cannot improve the physical-count inequality. Arbitrary legal beta is harmless because the amplitude definition divides by Delta, 13, and gamma, but never by beta. Here gamma=7 and all required constants are nonzero in characteristic 53.

## 2. Orbit argument and support descent

For any root y in F_(53^d) of a nonzero F53 polynomial of degree at most eight, its prime-Frobenius orbit has length e dividing d and at most eight. Every e from two through eight has a prime divisor among 2,3,5,7. Thus gcd(d,210)=1 forces e=1 and y is in F53.

Prime-Frobenius stability of a finite distinct support is equivalent to its monic annihilator having F53 coefficients. For a seven-element stable support, applying the preceding orbit argument to its degree-seven annihilator places each actual support root in F53. No inference from coefficient descent alone is used without the degree hypothesis. This is valid for every allowed d, including d=1, 11, 13, and 37.

## 3. Exact cross-node polynomial and all coefficient exceptions

The fresh checker reconstructs Gaussian factors through their finite product over r. The candidate uses an additive Pascal recurrence, so its algorithm was not reused or executed. Literal Fourier entries independently yield all 169 normalized Weyl targets and gamma=7. The isolated cross row and vanishings for the entire forced-moment range are checked directly.

For a stable seven-node (++) support, write H(t)=sum_(j=0)^7 h_j t^j with h7=1 and h0 nonzero. The last b=1 recurrence is sum h_j s1(4+j;y)=0. Independent reconstruction gives

    u=(19,45,51,21,12,21,49,6),
    v=(1,16,25,40,36,46,41,12),
    s1(4+j;Y)=u_j-v_j Y^(8-j).

Therefore the displayed candidate polynomial is exact:

    P_H(Y)=19h0+45h1+51h2+21h3+12h4+21h5+49h6+6
       -h0 Y^8-16h1 Y^7-25h2 Y^6-40h3 Y^5
       -36h4 Y^4-46h5 Y^3-41h6 Y^2-12Y.

The term -h0 Y^8 cannot cancel with another term. For all 52 legal values of h0 it is nonzero. Every other coefficient, including the constant term, may vanish with no effect on the proof. The eight affine basis identities were checked coefficientwise, so this is an identity for every coefficient tuple, not an interpolation claim based on sampled parameters. All 53 values of each of the seven free coefficients were additionally tested, with exact evaluation at all 53 Y values for those 371 specializations.

Thus P_H has exact degree eight and forces the initially arbitrary adjacent cross node y into F53. Its nonzero value is inherited from the original cross-singleton condition, giving y in F53*. The other cross node and all amplitude vectors are irrelevant to this descent step. Recurrences follow by finite-sum interchange and x^4 H(x)=0, so amplitudes in K need not be Frobenius-stable.

**Nonblocking correction to the mutation explanation:** h0 nonzero is needed to assert *exact degree eight*, but is not needed to ensure a nonzero polynomial of degree at most eight. Since h7=1, the coefficient of Y is always -12=41, even when h0=0. The candidate's zero-constant-term mutation only destroys the leading-degree certificate; it does not destroy the orbit-descent argument itself. This imprecision does not weaken any claimed theorem, since an actual seven-nonzero-node support has h0 nonzero. Suggested wording: “The h0=0 mutation confirms that exact degree eight relies on h0 nonzero; the polynomial remains nonzero because its Y coefficient is -12.”

The 676 sign/reflection Gaussian identities and reflected target identities all pass independently. Consequently the one-sided argument applies separately to (--), with the other free cross node. No pairing, equality, or stability of the two same-sign amplitude collections is assumed.

## 4. Independent one-sided base-field obstruction

For each y in F53*, the checker builds all six forced rows directly and computes reduced row echelon form of the full six-by-seven coefficient system with its monic right-hand side. Every rank is six, with pivot columns 0,...,5; h6 is genuinely free. Thus all 53 monic solutions are enumerated, without assuming a chosen chart is valid in advance.

All 2,756 resulting polynomials satisfy all six original recurrences. Evaluation at all 52 nonzero prime-field elements gives 143,312 exact root checks. The root-count histogram is

    0 roots: 1041
    1 root:  1006
    2 roots:  521
    3 roots:  150
    4 roots:   32
    5 roots:    5
    6 roots:    1.

No polynomial has seven distinct nonzero roots. The entire independently reconstructed polynomial/root mapping agrees with the candidate's inert JSON, not merely the histogram. All 52 zero-h0 candidates have degree-seven cross polynomials; the other 2,704 have degree eight. Every cross polynomial retains its nonzero Y coefficient.

Once the stable seven-node support and adjacent y descend, an actual representation would violate precisely this one-sided obstruction. The conclusion is valid even if the other support and all weights remain extension-valued. This is the crucial source-dependency distinction: the proof is not an invalid export of B(F53)=18 to arbitrary extension certificates.

## 5. Physical-bank count and eighteen-bank attainment

Let n+ and n- be the two nonzero effective same-sign support sizes. The inherited lower theorem gives n+,n- >= 7, while physical count is at least n++n-+2. At count at most seventeen, at least one side therefore has exactly seven nodes. If both supports are stable, the preceding one-sided exclusion is a contradiction.

The inherited eighteen-bank F53 witness has stable supports and survives scalar extension to every K because sums, products, inverses, and nonzero guard values are preserved by a field embedding. Hence the restricted minimum is exactly eighteen.

At sixteen banks, both support sizes must equal seven, and each must be nonstable independently. At seventeen banks, every seven-node side must be nonstable; the theorem does not require a possible eight-node side to be nonstable. This distinction is correctly retained in the candidate.

## 6. Correct stopping boundary

The named declared-family gate is complete. Sixteen-bank searches in these degrees that retain F53 coefficients for either seven-node annihilator cannot succeed, even with extension-valued cross nodes and weights. They should not be re-run as open experiments.

The original free-cross-singleton unrestricted minimum remains within 16..18 for d>1 coprime to 210. The result does not exclude a sixteen-bank certificate with both support polynomials genuinely outside F53[t], and does not decide possible nonstable seventeen-bank certificates. The base case d=1 is already exactly eighteen from the accepted source.

Degree-37 chart exceptions are neither discarded nor needed. No chart determinant appears in the descent proof. For a stable seven-node candidate, y is forced into F53 before the finite obstruction is used; the checked first-six-column chart is nonsingular at every such y. The broader extension-valued classification must still respect the separately accepted degree-37 chart behavior.

The four parent owners remain TO RESEARCH, priority 56, and no broad row/count/novelty change follows from this review. Unrestricted cross allocations, other lengths or parameters, historical priority, paid evaluation costs, and FFT/runtime claims remain outside scope. Native row locators and current table counts were not independently verified by this mathematical review.

## 7. Reproducibility and actions

Only independent_review_check.py, newly authored for this review, was executed. Candidate/historical programs were inspected as text and never imported, compiled, or run. Candidate census JSON was treated as inert comparison data only after independent reconstruction.

The review directory contains the fresh checker, INDEPENDENT_ARITHMETIC.json, the full FRESH_BASEFIELD_CENSUS.json, this review, frozen candidate bindings, and cold-replay hashes. There were zero failed mathematical checks. No external write, repository publication, native table edit, or denied-action retry occurred.
