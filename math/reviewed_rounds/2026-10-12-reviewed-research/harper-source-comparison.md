Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 8b371837c3ccfdb9d5644bfe830cb00cb3b88de31c7a83f14e20ee2504eb71c0

---

M HARPER bounded source comparison independent review
11 October 2026

Verdict

ACCEPT the bounded source comparison and its ten existing-cell proposals, subject to the proposal's fresh-read and merge guards. There are no blocking mathematical or source-mapping corrections. This is acceptance of a literature comparison, not a new mathematical proof acceptance, rank change, discovery, or historical-priority determination. The exact printed antecedent and worldwide priority remain unresolved.

Reviewed input

M_HARPER_Bounded_Primary_Comparison_2026-10-11.zip
SHA256 c22b3f8a40c76554cdd1a4e7cd985e83fb6c37968d5fb5579e03e6be42593a9b

All ten manifest entries match the archived bytes, declared byte counts, and working packet files. All eight private extraction snapshots match their saved receipts. The canonical theorem, direct upstream audit, and local historical verdict byte pins match. The consolidated row_outcomes.json is absent locally and is correctly only inherited through the pinned checkpoint; it must not be described as freshly byte-verified.

Independent primary-source checks

BCHKOO2000. The author's published PDF, pp. 2211-2215, gives G_n equal to H; p. 2213 gives the two reflection dimensions, the tridiagonal sector construction, and Proposition 2. The simplicity statement preceding Proposition 1 is on p. 2212. The normalized even-sector basis gives endpoint weights sqrt(2); the odd block has unit weights. The extraction's Fourier-entry line omits normalization despite declaring unitarity; that ambiguity is retained. The text also needs normalization of its orthogonal parity vectors before asserting a symmetric matrix in coordinates. Important reading safeguard: p. 2214 treats the canonical ordered Harper eigenphase assignment as conjectural. Do not turn the common eigenbasis into a proved ordered phase list, or identify its two fractional-transform constructions with exact F. The comparison does neither. Its treatment of N=4 is a direct deduction, not an uncaveated citation to the paper's small-size discussion.
Source: https://cagataycandan.github.io/pub_dir/frft_withbarker00.pdf

AA2015. The reproduced paper body verifies the positive exponent and 1/sqrt(N) in Eq. (1.12), Q and T in Eqs. (2.3)-(2.4), and U(1) in Eq. (3.3). Thus Q(+)=D^-1, Q(-)=D, T(+)=Z^-1, T(-)=Z, Phi=conjugate(F), and U(1)=H/2. The two-zero assertion appears immediately after the displayed Harper matrix on p. 6. Sections 3-4 then consider additional commuting and ladder operators; they do not establish the requested parity endpoint identity in the sections inspected. This supports a prior assertion and the normalization map, without importing a separately verified zero-mode proof.
Source: https://www.researchgate.net/publication/275062003_On_the_raising_and_lowering_difference_operators_for_eigenvectors_of_the_finite_Fourier_transform
DOI: https://doi.org/10.1088/1742-6596/597/1/012012

OWW2018. Section 2, Eq. (3), is the periodic secular matrix at p=1, q=N, k_x=k_y=0. Eqs. (7)-(8), on printed p. 2, give det(EI-H)=E^N b_(1/N)(1/E)-4 because N is even. The expression extends polynomially through E=0. Eq. (9) supplies the Kreft coefficient family. Section 3.1, Eq. (13), p. 3, instead sets the secular discriminant to zero for mid-band energies. Zero momentum gives 4. Figure 2 gives the N=4 discriminant E^4-8E^2+4; subtracting 4 agrees with H's characteristic polynomial E^4-8E^2. These are determinant coefficients, not Fourier phase interpolants.
Source: https://arxiv.org/pdf/1711.03900

OW2019. The author preprint v2, Section 1, printed p. 2, Eq. (4), explicitly connects the coefficient family with the momentum-independent secular determinant. Section 2.1 concerns coefficient extrapolation. This corroborates the determinant interpretation, without supplying the parity Fourier phase assignment.
Source: https://arxiv.org/pdf/1810.04098

QSSM2025. Eq. (A10), p. 16, becomes H/2 at a=epsilon=1 and b=0. The text after Eq. (A99), p. 24, says its determinant relation is "probably exact"; Lemma A.19 then depends on that relation. The comparison correctly preserves that qualification and uses this only as contextual prior evidence. No unconditional proof status is imported.
Source: https://arxiv.org/pdf/2507.11696

Independent algebra check

Set n=N/2. In the orthonormal reflection-even basis e_0,(e_j+e_-j)/sqrt(2),e_n, H has dimension n+1 with endpoint edge weights sqrt(2), internal weights 1, and diagonal 2cos(2pi j/N). In the odd basis (e_j-e_-j)/sqrt(2), 1<=j<=n-1, H has dimension n-1 and all edge weights 1. Irreducible symmetric tridiagonal matrices have simple spectrum: an eigenvector is determined by its first coordinate, that coordinate cannot vanish, and symmetry supplies diagonalizability.

For a size-L Jacobi matrix A and any commuting B, the simple eigenvalues give a unique polynomial p of degree <L with B=p(A). At the opposite endpoints, A^k vanishes for k<L-1, while A^(L-1) has entry equal to the product of all edge weights. Hence the coefficient of x^(L-1) is B_endpoint divided by that product. This proves sharpness when B_endpoint is nonzero, including the empty-product convention at L=1. These are standard interpolation and path arguments; their application here is not evidence of historical novelty.

The even Fourier endpoint is <e_0,F e_n>=1/sqrt(N). The path product is 2. Thus the minimal reduced degree is n and the leading coefficient is 1/(2sqrt(N)).

For odd basis vectors v_j=(e_j-e_-j)/sqrt(2), direct expansion gives <v_j,Fv_k>=(omega^(jk)-omega^(-jk))/sqrt(N). Put j=1 and k=n-1. Since omega=exp(-2pi i/N), omega^(n-1)-omega^(-(n-1))=-2i sin(2pi/N), nonzero for N>=4. The path product is 1; the minimal reduced degree is n-2 and leading coefficient is -2i sin(2pi/N)/sqrt(N). At N=4 this is the constant -i; the even coefficient is 1/4.

The reduced representative is unique; higher-degree representatives may differ by multiples of the sector characteristic polynomial. The characteristic degrees are n+1 and n-1, distinct from interpolation degrees n and n-2.

For AA2015, define coefficient-wise conjugation by p_bar. Its interpolants are r_+(u)=p_bar_+(2u) and r_-(u)=p_bar_-(2u). The leading coefficients are respectively 2^n/(2sqrt(N)) and 2^(n-2)*2i sin(2pi/N)/sqrt(N). Writing conjugate(p(2u)) is equivalent only when u is treated as a real spectral variable; the coefficient-wise wording removes any ambiguity for a formal polynomial variable. This is a notational clarification, not a correction to the numerical formula.

Finally n is even, so both sector dimensions are odd. Signed index reversal negates the diagonal and, by alternating signs, the off-diagonal edges. Each simple block therefore has exactly one zero eigenvector. F^2=J forces the two zero-line Fourier phases into disjoint sets {1,-1} and {i,-i}. Any scalar function of H is one scalar on the whole kernel and cannot equal F. This remains a single-commuting-Harper obstruction, not a statement about arbitrary noncommuting constructions.

Access limitations

Fresh permitted web retrieval independently returned errors for the Dickinson-Steiglitz author PDF, the TU Berlin compressed PostScript, and the separate Barker Mathematika publisher PDF. CERN returned a bot-check page. No restriction was bypassed. These checks reproduce the body-access gaps, but do not freshly certify the exact HTTP status codes from the author's earlier attempts. The author's HTTP-403/unsupported-content-type descriptions are historical retrieval reports. Barker screenshots also failed in this review; its available PDF text extraction, not a visually checked original-page rendering, supports this review.

No inference of novelty follows from these gaps or from failing to find the assembled statement in the bounded excerpts. A later readable original or equivalent full-text edition can change the historical comparison without changing the accepted algebra.

Exact existing-cell guidance

The ten approved candidate overlays are byte-preserved in APPROVED_EXISTING_CELL_PROPOSALS.json. They concern three existing M-HARPER rows:
- Catalogue: U70 and V70; verify stable ID A70.

All baseline values equal their corresponding cells in the byte-pinned 21:41 checkpoint. That establishes provenance, not present-day write eligibility. Freshly read each actual target cell and stable-ID cell before an authorized write. If unchanged, the candidate proposed_value is eligible. If changed, merge only its new_overlay with the latest text; never overwrite newer text with the stored baseline. If an equivalent overlay is already present, avoid duplication. Preserve formulas and history; resolve unexpected formula targets rather than blindly replacing them. Read back the persisted values and verify that no adjacent fields, formatting, colors, ranks, row counts, or proof states changed.

The T106 wording changes only the literature-review classification. It does not upgrade mathematical proof status or novelty. Do not write any mathematical status/rank/discovery fields, add rows, modify the gauge clauses, or reopen the already closed upstream audit-binding issue. The printed-source comparison gate may be marked bounded-comparison complete with access limits only; historical priority stays unresolved.

This review made no external writes, ran no uploaded or archived research program, and performed no fresh all-entry matrix replay. Only independently authored standard-library file/hash/JSON checks were run.
