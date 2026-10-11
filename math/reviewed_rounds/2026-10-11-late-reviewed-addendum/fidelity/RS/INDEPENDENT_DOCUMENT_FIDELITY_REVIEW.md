# Independent document fidelity review of the RS working note Version 3

Review date: 11 October 2026 UTC

## Decision

**PASS. Accept the exact 21-page Version 3 PDF, standalone LaTeX, and preservation package identified below as a faithful editorial integration. No repair is required.**

This is a document-fidelity decision. It does not reopen, reprove, or independently rerun the accepted mathematical or implementation reviews. The accepted v1.1 validator and the separately accepted residual checker remain distinct. No general residual-preparation result, growing-degree stability claim, production qualification, historical-priority conclusion, or research-ranking change follows.

The manuscript and package retain their historical pending-fidelity statements. This external review supplies acceptance tied to the exact reviewed bytes. Editing those statements would produce new bytes and is not covered automatically by this verdict.

## Exact reviewed identities

All three items were freshly materialized from Library at version 0 and independently hashed. The resulting bytes match both the supplied frozen identities and the copies within the preservation package.

- PDF: `libfile_5f8be6968df08191b4648115f5064d26`, 156,642 bytes, SHA-256 `47da02758de282ff76f4ae54dd5d07a6b583dd15f49bb8af39763242f43f805e`.
- Editable LaTeX: `libfile_467a9a6dac488191b4eb0b01a98b4600`, 64,336 bytes, SHA-256 `57bc17168b7b11efe7a5bdc7190473267b0c08fcd4f2bb5b9c59f04f1cbfa282`.
- Preservation package: `libfile_799d7adf82748191ae8aa45b49251461`, 6,178,978 bytes, SHA-256 `07131163e473bb74cd69877667731bf8c9ae8d2d32d686e80688d9e7c4e1ffac`.

## Preservation and provenance

The complete contiguous LaTeX block from Section 2 through Appendix C is **byte-identical** to accepted Version 2. This includes Sections 2–9, References, and Appendices A–C: 38,587 bytes, SHA-256 `4c94554d873c7778fece8dcc7e93c6a9118651a22ecf74a3b5882ffa02691947`.

The independent source diff confirms that prior material changed only in the version/date label, Version 3 introductory paragraph, and retrospective provenance wording in Appendix D. Appendices E–G are additions. The original 28 numbered displays and C1–C17 retain their source text and ordering. F1–F10 are new editorial labels for the accepted example.

All **34** payloads enumerated by the Version 3 manifest match both size and SHA-256; the ZIP has 35 members including the manifest, with no extra payload. All **18** source pins match. Nine previously published Library items were independently downloaded at version 0 and compared to the packaged copies: original PDF/LaTeX, accepted v2 PDF/LaTeX, v2 sealed package, v2 editorial review, accepted v1.1 review archive, residual candidate archive, and accepted residual review archive. All nine are byte-identical.

The nine source snapshots are matched to actual members of the pinned archives, not accepted on filename or status label alone. These include the exact two checker sources, both implementation-review reports, residual example LaTeX, residual certificate, finite theorem, finite review, and Q08 envelope. Historical checker programs were treated as inert bytes.

Eight manifests in the five preserved first-level ZIPs were also checked: v1.1 review (115 payloads), its original candidate (44), repaired candidate (43), residual candidate (31), residual review (46), its retained candidate (31), v2 package (20), and v2 editorial review (36). These counts overlap by design; they are not counts of distinct new results. The v2 editorial verdict confirms acceptance of its exact 15-page integration.

Appendix G accurately pins the accepted sources and their external reviews. The accepted checker identities remain:

- v1.1: `7cf350bfa8037e2addb3f26454a0e047b4f8df501500158292f45b9020d8a60c`.
- Fixed residual profile: `739759b078f4382fc093c9acf8f2fdd59b54b2250daa369f09d692348d75c800`.

## Appendix E mapping to accepted v1.1

E1 and E2 faithfully summarize the accepted implementation review and corrected certificate contract.

- The supported profiles are exactly `separated-2-3-0`, `overlap-1-3-1`, and the capped `b0-hermite` family: b=0, 1≤A≤16, odd 3≤d≤31, Ad≤128, with primitive embeddings. Both primitive cubic embeddings remain supported in the two specified cubic profiles. A request inside the caps need not certify.
- Canonical rational input, exact arithmetic, outward enclosures, strict analytic tests, final separation, and complete degree counting are retained. The majorant is rounded upward. The essential normalization s^(−m) is retained.
- The distinction between exponent 1 and exponent 2 is preserved: Appendix C's inverse operator-norm bound has its square-root n factor and unsquared powers; the API reports squared bounds, so n and doubled powers are used. The distinct within-cluster m−1 and cross-cluster n−m factors remain separate. Singleton empty products are one.
- The formal parameter conventions in Section 2 and the conversions in Section 7 are unchanged: q(epsilon)^d−1=epsilon² and h=log(1+epsilon²)/d. No epsilon power is silently reinterpreted as the same power of q−omega or q^d−1. The square-root and discriminant conventions are unchanged.
- Root tubes are valid on the punctured complex disk 0<|epsilon|≤r. Norms are stated on the closed annulus epsilon_min≤|epsilon|≤r, with epsilon_min>0. The presentation does not impose a real-parameter restriction.
- Only CERTIFIED is positive. Verified negative decision envelopes remain negative. Equality in a strict sufficient test is inconclusive. Failure of a sufficient norm ceiling does not establish that the actual norm exceeds the requested ceiling. Reasons are first-failure diagnostics.
- The corrected width limit is a checked-arithmetic admission budget. Parsing or geometry preparation can create a temporary before its next check; no peak-allocation, peak-memory, processor-instruction, CPU-time, or bit-complexity guarantee is claimed. Charged primitives are not CPU instructions.
- The non-JSON Python error envelope has only format and result, carries REJECT, and is not a decision certificate. Strict CLI acceptance is not promised for every negative envelope that the Python interface can produce.
- Source pins and checker identity are recomputed; certificate fields, supplied geometry, decisions, and counters are not trusted. Historical pending-review literals remain unchanged, with acceptance supplied externally.

The reported 30 author test groups and supplementary review categories are attributed to the accepted review. This document audit did not execute them again.

## Appendix F mapping to the accepted residual example

F1–F5 correctly specialize to **(A,d,b)=(1,5,2), n=7, primitive embedding 1 only**, with omega=exp(2πi/5). The implementation is not silently folded into v1.1. Tests of algebra in other embeddings do not expand this API.

### Algebra, branches, labels, and geometry

The preserved formulas are F(z)=z^5+1, G(z)=z²+(1+omega)z+1, and q(epsilon)=omega(1+epsilon²)^(1/5), with the branch fixed at omega at zero. The branch is analytic for |epsilon|<1 and even in epsilon.

The discriminant −3+2w+w², resultant 5+10w+10w², and field norms 305 and 3125 agree with the accepted source and review. The field norms across four embeddings are not substituted for complex moduli.

The positive-radical convention selects the intended primitive embedding and the square root of D with positive real and imaginary parts. Renaming source variables u,v to u_0,v_0 is harmless and consistent. The root labels remain alpha_k=−omega^k for k=0,…,4, followed by beta_plus and beta_minus with the corresponding plus/minus radical signs.

All eight printed beta rectangle endpoints match the sealed JSON certificate exactly. The 24-bit precision, independent-review 112-bit enclosure comparison, accepted geometry precisions 6–64, and exhaustion at 0–5 are described consistently with the accepted review. Rectangles enclose exact centers; their midpoints are not substituted for the centers.

The smallest reported pairwise bound is correctly attached to alpha_4 and beta_plus: 7981317/16777216>3/8. All 21 pairwise distances, the residual modulus 7/4, the ordinary |G(alpha)|≥1 margin, ordinary leading derivative ≥5, and static product-derivative margins >1 retain the source's meanings. Static and leading derivatives are not presented as computed perturbed derivatives.

### Both strict Rouché tests and the seven-root count

The parameters are exactly s=1/2, r=2^−20, eta=X=rho=1/16, epsilon_min=2^−21. The exponent bound floor(7²/4)/5=12/5≤3 is retained.

The ordinary quantities match the accepted certificate:

- B_o = 612778486328125/2199023255552.
- mu_o = 5/16.
- E_o = B_o r/[s(s−r)] = 612778486328125/576459652791795712 < 5/16.

The s^−1 normalization is explicit. There is one simple root in each of the five disks |z−alpha_k|<|epsilon|/16.

The distinct residual test is also present, with its even-tail exponent 2:

- nu = rho(3/8−rho)^6 = 15625/268435456.
- B_r = 46708681640625/17179869184.
- E_r = B_r r²/(s²−r²) = 15569560546875/1574122160950821781504 < nu.
- Strict residual threshold r² < 16/2989355689.

There is one simple root in each residual disk |z−beta_plus/minus|<1/16. The source's r=1/8192 control, where the ordinary test passes and the residual test fails, is correctly retained as an inconclusive certificate failure, not a collision.

The moving static-center radius is 2^−24, the residual radius is 1/16, the conservative common separation is Delta=1/4, and R=29/16. The disks are disjoint and 5+2=7 exhausts the degree, for every complex 0<|epsilon|≤2^−20. No root is omitted and no real-only restriction is introduced.

### Exact Q08 bounds and API qualifications

All three printed squared bounds match the accepted certificate exactly:

- Inverse norm squared: 482667664884521484375/16777216.
- Forward norm squared: 3559663633456975639/281474976710656.
- Condition number squared: 1718134533735029637122107300906494140625/4722366482869645213696.

The n=7 factor, exponent 12 after squaring, singleton empty-product rule, and the absence of an inverse-epsilon factor are preserved. The exact square monomial moment Vandermonde uses the actual seven perturbed roots, with the inherited row/column convention. The stated annulus remains 2^−21≤|epsilon|≤2^−20. Singleton bounds do not depend on epsilon_min; this is not promoted to a size-uniform, rounded-matrix, or linear-solve guarantee.

The charged 15,921 primitives and 809 observed checked bits match the published certificate and accepted review. They remain admission/cost observations, not allocation or complexity guarantees. The A=2 rejection versus earlier A=17 finite-cap indeterminacy accurately demonstrates first-failure precedence. Negative verified envelopes remain negative.

F5 correctly reports that the accepted review required no mathematical or executable repair and attributes its author-test, exact-control, mutation, source-tamper, CLI, and non-JSON evidence to that review. This audit did not execute those programs or recreate the proof.

## Independent build and visual fidelity

The freshly downloaded standalone LaTeX was copied into a clean build directory and compiled twice with XeLaTeX using `-no-shell-escape -interaction=nonstopmode -halt-on-error`. The existing writable format cache was supplied explicitly. No research code was imported, compiled, AST-parsed, or executed; only document-building and independently authored artifact-checking utilities ran.

Both builds completed and the rebuilt PDF has **21 pages**. Original and rebuilt PDFs were independently rendered with Poppler at 110 dpi. All **21 of 21 full-page rasters are pixel-identical**, and the layout-preserving extracted text is byte-identical. Every page was visually reviewed; the new appendices received full-page inspection. Mathematical glyphs, inequalities, root labels, exact fractions, source hashes, headings, and page numbers are legible, with no clipped or overlapping content.

The PDF binaries are **not byte-identical**. The rebuilt PDF has the same 156,642-byte length and SHA-256 `e0d71b65d041ef4888de35079ea7a4a059a0c643c964f5a2497358f817c1f9f1`. The original reports creation time 17:09:59 UTC; the independent rebuild reports 17:16:36 UTC. Both encode these as +05:00 local timestamps. Document IDs and embedded font-subset prefixes differ, changing some compressed streams and associated cross-reference offsets. Decoded page content, page boxes, annotations, and normalized PDF objects match. All non-xref decoded stream differences are explained by the creation timestamp or font-subset prefixes. There are no unexplained content differences. No stronger cross-engine or future-build binary reproducibility claim is made.

The final LaTeX log has no overfull boxes or missing-reference warnings. It records two underfull hbox notices: one in the revised introductory paragraph and one inherited at lines 549–552. Neither creates a visible defect. The author's `inherited_underfull_hbox: 1` describes the inherited notice, not the total of both notices. Appendix E ends with intentional whitespace on page 17 before the page-break opening of Appendix F; this is acceptable appendix separation.

## Required changes and limits

Required corrections: **none**.

This review accepts the exact frozen Version 3 integration and its preservation evidence. It does not accept later changes automatically. It makes no new mathematical, executable, historical-priority, production, or growing-degree claim. No source or manuscript was changed, and no Sheet or GitHub write was performed.

The packet includes the frozen candidate preservation ZIP, independent source/payload checks, full source diff, accepted-certificate literal mapping, rebuild logs and PDF, extracted text, per-page pixel comparisons, inspected page images, and a machine-readable verdict. The independent artifact-checking script contains no imports or execution of the historical research programs.
