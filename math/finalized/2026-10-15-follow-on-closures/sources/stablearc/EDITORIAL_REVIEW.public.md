Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 004754b408191bb43c1f1e9145ac04eded2d95063fe75d9a661c4ba487499800

---

# Stable arc editorial credit independent review

11 October 2026 UTC

## Verdict

ACCEPT for STABLE-ARC::editorial-credit only. The frozen editorial version applies the five accepted attribution and convention corrections, preserves the original manuscript separately, and does not change its theorem statements or upgrade proof, novelty, publication, rank, count, or FFT-complexity status. The existing editorial gate may close after an authorized writer re-reads the live stable IDs, values and complete notes and preserves their provenance. No external write was performed in this review.

This acceptance binds the candidate ZIP SHA256 dc7b0c15d50d76a6fc202f5a34611874bf8bb20cdcbc70b73c9b63c537225f11, manifest SHA256 08a1d3b19f9b5efa25688bb2fafac9b1d047fa7ee336d06a1c01737a25047638, and authoritative manuscript SHA256 159ff2e8a081fbff81d977b023b3bce08561ded1b395dd0924a48df3e5802631. Acceptance is not transferable to later byte changes without review.

## Preservation and source bodies

The reviewer extracted the sealed archive into a separate review directory and verified all 29 manifest entries and all twelve source-body/archive pins. Every source copy also matched its available original path at review time. The original theorem and source audit inside the original ZIP match the separately preserved source files. The original manuscript SHA256 remains 50ae0ea5f9cd099ab8e0d2dc30872dbce663515e541a8ef853cd48be13a15172; original ZIP SHA256 remains 40ea2d2101072723fbbb8dc637c33072666f39b57315edda245348f739dfcae8.

The nine literal replacement records exactly reconstruct the revised manuscript. Both supplied textual diffs independently match recomputed diffs. The complete Theorem A statement, all six numbered A1–A5/L displays, Steps 3 and 4, and the graph-certificate cost paragraph are byte-identical to the original segments. All local manuscript links resolve. The 134 pairs of inline and 16 pairs of display TeX delimiters balance. The source narrative now supersedes the old contribution claim instead of silently editing historical source bytes.

The authoritative artifact is editable Markdown/TeX, the source's original format. The sealed candidate contains no Word/PDF derivative, and this review makes no rendered-document quality claim.

## Prior work and exact source correspondence

M-ROUTED-FIELD already permits independently routed endpoints, even with zero endpoint masks, and proves N <= r(r+1)^r. Its extension Section A covers invertible denominators with at most two nonzero entries per column. Setting r=q, D=I, pi(v_t)=v_(t+1), and E[v_(t+1),v_(t+1)]=-w_t makes Q=D+EP exactly I-W. Its exact-order root can be chosen exp(-2 pi i/N); the complex unitary Fourier factor is nonzero and can be absorbed into an endpoint. Thus A3 and endpoint freedom are inherited. The present theorem has not silently acquired the prior theorem's broader denominator/mask assumptions or a finite-field spectral conclusion.

Phase43 Theorem 43.1 retains credit for the common-endpoint arc-rank mechanism and the same q(q+1)^q ceiling. Its convention W e_(v_t)=w^(43)_(t+1) e_(v_(t+1)) is identical after w^(43)_(t+1)=w_t. Its separate four-row, two-layer interpolation results at N=8,16 are not recast as a full transform or contradicted by the one-layer obstruction.

M-SEPARATION statement (4) supplies error squared at least max(0,m/N-q/m), where m=floor(N/2^d) and d<=q counts distinct order pairs. Using d=q weakens the bound. The function m/N-q/m is increasing for positive m, so the manuscript's branch-count-only formula is valid; it is read as zero when m=0. The source uses the same unitary target and Euclidean norm. Its row-action convention agrees exactly by reversing cycle order: u_t=v_(-t), with row weight tilde_w[u_t]=w_(-t-1). This maps T[u_t,u_(t+1)] to the very same nonzero W entry, without a Fourier transpose or sign change.

The accepted comparison's strict A4-domain dominance was independently rechecked algebraically. Put t=2^q. The hypothesis N>=4(q+1)^(q+1) implies N>=3qt^2: q=1,2 are direct, and q>=3 follows from q+1>=4. Consequently m=floor(N/t)>=5N/(6t), and m/N-q/m>=13/(30t). Meanwhile c_q^2<=2^(-2q-2)<13/(30t). This confirms strict dominance everywhere in the stated size domain, not only at sampled sizes. If q<=beta log_2 N for beta<min(2alpha,1/2), then N>=3q4^q eventually and the same bound contradicts error <=N^(-alpha). The earlier bound therefore already implies Omega_alpha(log N). The revision correctly retains A4/A5 as weaker valid conclusions and A1/A2 as partition diagnostics, without claiming pointwise domination by every possible data-dependent separation certificate.

## Exact arc and Rayleigh conventions

With source-to-destination action W e_(v_t)=w_t e_(v_(t+1)), beta_a=product_(t<a)w_t and h=product_t w_t, the inverse entry is beta_a h^[a<b]/((1-h) beta_b). Nonzero edge weights and h!=1 are essential to this formula and its projective interpretation. For sorted marked positions, the exponent pattern is constant on each right-closed interval (a_(t-1),a_t]. The source at a marked endpoint belongs to the arc ending there. The wrapping pieces b>a_n and b<=a_1 have all-one and all-zero exponent patterns; they differ by the common nonzero scalar h. Their union is one projective class. Endpoint permutations pull these labels back separately for each branch.

The new Gram identity is correct. For A=U_N[R,C], b*AA*b is the sum of squared moduli of the columns of b*A. Hence the polynomial coefficients must be conjugate(b_r). The factor z_j^r0 has modulus one. Reducing wrapping row indices modulo N does not change z_j's powers, since z_j^N=1. Conjugation is a bijection on the unit coefficient sphere, so this is the required correspondence for the existing density estimate, not a different inequality.

## Target normalization boundary

The target remains the fixed unitary Fourier matrix. Scaling the target by t rescales the absolute lower bound by |t|, using closure of the approximant grammar under nonzero scalar multiplication; t=0 gives only the trivial zero lower bound. For invertible monomial target changes A U_N B, applying A^-1 and B^-1 preserves the approximant class and gives the factor sigma_min(A)sigma_min(B). Unitary monomials preserve the bound unchanged.

The retained norm-one warning is substantive. Let G=(I-P/2)^-1, choose a right diagonal so H has exactly the target's first row, and shrink H's remaining rows by delta=epsilon/(1+||H_tail||). Against target diag(1,epsilon,...,epsilon)U_N, the first-row error vanishes and the tail error is bounded by delta||H_tail||+epsilon <2epsilon, although the target has operator norm one. Both endpoint diagonals remain invertible for epsilon>0. Thus fixed target norm alone cannot rescue an uncontrolled nonunitary target normalization. This is a counterexample to an excluded extension, not to A4.

## Primary literature checks

The reviewer separately inspected the following primary sources on 11 October 2026. They support the restricted uses in the revision; this was not a renewed worldwide priority search.

- Aubel and Bölcskei, Section 3.2, equation (2), PDF page index 4: the classical square inverse-Vandermonde product bound is indeed recorded there and attributed to Gautschi. The manuscript identifies a classical mechanism described by this paper, not a newly proved Green-sum result. https://www.mins.ee.ethz.ch/pubs/files/vandermonde-jou.pdf
- Yomdin, Theorem 1.3 and Definition 1.2, PDF page index 4: the domain and metric-span assumptions are real-domain ones. They do not directly identify the present finite complex-grid constant. https://arxiv.org/pdf/0911.1937
- Yomdin's bibliographic issue year is 2011, volume 186, pages 45–60, DOI 10.1007/s11856-011-0131-4. The publisher also records an online publication date in May 2012; this does not invalidate the manuscript's conventional issue-year citation. https://doi.org/10.1007/s11856-011-0131-4 and https://weizmann.elsevierpure.com/en/publications/remez-type-inequality-for-discrete-sets/
- Tikhonov and Yuditskii, Theorem 1.2, PDF page index 2: its measured circle set must have positive arc measure. A finite grid is outside that direct assumption. https://arxiv.org/pdf/1809.09726

## Fresh independent controls and execution scope

Only the reviewer's newly written independent_controls.py was run. No original uploaded program, author editorial checker, or historical verifier was executed, imported, compiled, or used as a control implementation. Archived programs remain inert. Source documents and stored historical results were read as data.

Fresh exact rational checks covered 568 inverse entries; 2,024 selected-row sets; 16,296 arc-column checks; 1,004 wrapping classes with both pieces; 8,192 marked-endpoint memberships; and 16 convention matrix cases. A wrong left-closed negative control fails as expected. Twenty-seven independently routed rational q-branch examples checked 145 joint classes. There were 180 exact Gaussian-rational N=4 Rayleigh checks with arbitrary row starts and all nonempty column subsets; a missing-conjugation control fails. Ninety additional floating-point Rayleigh diagnostics had maximum residual about 1.56e-15. One hundred sixty exact arithmetic boundary/near-boundary comparisons for q=1,...,40 supplement the algebraic dominance argument. Three floating-point N=16 norm-one target examples agree with the analytic counterexample, with errors below 2epsilon. These are bounded editorial regressions, not a replay of the historical 3 modular, 10 complex, 63,595 spacing or 105 density controls, and not a new all-N proof audit.

## Remaining boundaries and integration

Close only STABLE-ARC::editorial-credit. Preserve the already accepted restricted theorem and its exact A1–A5/L constants. Historical priority, publication significance, optimality, interval-certified numerical eigenvalues, bit complexity, uniform coefficient synthesis, charged setup/evaluation costs, products of sums, AESGR, and multilayer all-row/Weyl constructions are not discharged. Do not infer a new theorem row, novelty rank, result count, unrestricted arithmetic lower bound, or publication-ready status.
