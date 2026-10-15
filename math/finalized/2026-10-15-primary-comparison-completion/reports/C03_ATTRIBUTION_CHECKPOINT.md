# C03: complete-family priority and the 1989 source checkpoint

15 October 2026, 21:49 UTC (sealed after the targeted Library check). External read-only comparison. No historical research program was executed, no accepted proof was reopened, and no workbook or repository was changed.

## Decision

**C03 remains a proved specialization of classical resultant mechanisms; exact complete-family printed priority remains unresolved. No closure or score change is proposed.**

The retained theorem is not justified as a new general elimination theory. A narrowly positioned proposition containing its particular principal-minor coefficient and explicit endpoint certificates remains a plausible presentation, but this pass supplies no evidence that such a proposition is historically original. Neither a negative search nor a missing source body establishes firstness.

There is one bounded evidentiary advance: fresh indexed text from the author-hosted 1989 primary PDF independently corroborates its field setting, Theorem 3.3, the coprime restriction in Theorem 6.3, and Corollary 6.1 equation (126). This is stronger than relying only on the previous author's report. It is **not** a successful acquisition of the complete PDF or verification of its formula artwork. Consequently it does not remove the full-body/array provenance qualification from the historical review.

## Exact target and retained source identity

The current Catalogue158 U/V inquiry is the complete evaluated arbitrary-matrix family, its prescribed signed principal-minor coefficient and endpoints. It is not merely whether a Hankel determinant can express a resultant. The live-read receipt already supplied by the parent was read; this pass did not make a new live sheet read.

The scope is arbitrary m-by-m A,B over a commutative ring S, with m>=1 and D=diag(1,w,...,w^(m-1)). Put

    f(a,w)=det(A-aDAD),  g(a,w)=det(B-awDBD),
    R=Res_(m,m)(f,g),  v=m(m-1)(4m+1)/6,
    b=m(m-1)(2m-1)/6,  T=m^2(2m-1).

The resultant retains formal homogeneous degree (m,m), including after actual-degree drops. The accepted identity is

    R(w)=w^(v+b)(w-1)^(m^2)V(w+w^(-1)),  deg V<=b,
    w^T R(w^(-1))=(-1)^(m^2)R(w).

The accepted structural supplement also gives the prescribed coefficient, not necessarily the actual leading coefficient after specialization:

    [x^b]V=(-1)^(m(m-1)/2) det(A)det(B)
      * product_(j=1..m-1) ell_j(A)r_j(A)ell_j(B)r_j(B).

Here ell_j and r_j are leading and trailing principal determinants in the displayed coordinate order. Its division-free Laurent determinant has entries

    N(w)_((i,k),(j,l))=A_ij B_kl S_(1+k-i+l-j)(w),
    S_n(w)=(w^n-1)/(w-1) in Z[w,w^(-1)],
    V(w+w^(-1))=det N(w).

In particular, for L=diag(0,...,m-1), X=A tensor B, and E/O the even/odd i+k index classes,

    V(2)=det[A tensor (LB+BL+B)-(LA+AL) tensor B],
    V(-2)=det X[E,E] det X[O,O].

These formulas are retained accepted project material, not quotations from the 1989 source and not new proofs in this pass. Source pins: assessment f44c8891c029805234b1f42a7a67f822ca3741c1e9aa723e5820f3478124c975; earlier attribution derivative 981fd6b6e237aa0f0fa4968f090fb935303e64a9e0bcfdec8335bc762a260297; structural supplement 2da369c92f44648dcf1c68c94fae623610efedf37ab11e91a1df328ebb858a14. Full local path/byte bindings are in LOCAL_SOURCE_PINS.json.

## What the fresh 1989 evidence establishes

U. Helmke and P. A. Fuhrmann, *Bezoutians*, Linear Algebra and its Applications 122–124 (1989), 1039–1097, [DOI](https://doi.org/10.1016/0024-3795(89)90684-8); [author-hosted PDF](https://math.bgu.ac.il/~paf/bezoutians.pdf).

Fresh indexed primary-PDF text corroborates: Section 2, p.1042, uses a commutative field; Theorem 3.3, p.1054, relates Bezoutian kernel dimension to gcd degree and invertibility to coprimality; Theorem 6.3, p.1065, assumes coprime p,q with deg p<deg q=n; Corollary 6.1, p.1067, repeats these hypotheses and prints det H=det B(q,p) as (126). The surrounding discussion attributes the Hankel/Bezout connection to Hermite and Krein–Naimark. Matrix-array OCR is damaged. Complete normalization conventions and arrays (114)–(125) were not image-checked. Theorem 6.2's reported nonsingularity condition was not freshly recovered and remains author-reported. No 1989 PDF-byte SHA256 is claimed.

The university [publication record](https://cris.bgu.ac.il/en/publications/bezoutians-2/) and [publisher record](https://www.sciencedirect.com/science/article/pii/0024379589906848) independently identify the article. The publisher's issue dates are September–November 1989; a repository's January metadata is not evidence for an exact earlier publication day.

## Exact map and failed equivalences

The following map is the already accepted C03 coefficient-level bridge, used here only to compare hypotheses. Over a field, require w!=0 and det(A)!=0, and set

    alpha=(-1)^m w^(m(m-1))det A,
    beta=(-1)^m w^(m^2)det B,
    u=f/alpha,  h=g-beta*u.

Then u is monic of degree m and deg h<m, with h=0 allowed. The classical comparison uses q=u and p=h; the Hankel matrix is built from the coefficients of h/u at infinity. This is a derived rational-function Hankel matrix, not the original adjacent moment matrix.

The accepted formula is R=(-1)^(m(m-1)/2)alpha^m det H. The normalization and multiplier cannot be discarded when citing a formula for monic q. The 1989 OCR excerpt is insufficient to certify a new, unnormalized formula orientation.

For w!=0,1 on this field chart, V=0 makes R=0 and u,h noncoprime. Thus the printed coprime-only 1989 comparison cannot itself certify the determinant-zero recognition cases. The noncoprime extension is already explicitly covered by García-Armas–Ghorpade–Ram, [Proposition 3.4](https://arxiv.org/html/1011.1760#S3): its Padé-pair domain has monic u of degree m and deg h<m without requiring coprimality. That primary statement and its coefficient proof were freshly reopened; no new acceptance is needed.

Over a general ring, the chart requires w and det(A) to be units or explicit localization. A field nullity statement does not establish arbitrary-ring rank, padded infinity multiplicity, or existence of a base-field recovery candidate.

The endpoint comparison is a decisive nonmatch even in dimension one. The retained example A=B=[1] gives f=1-a, g=1-aw, R=w-1, H=[1-w], and V=1. At w=1 the raw Hankel determinant vanishes while V(2)=1. The endpoint requires symbolic deflation before evaluation. An inverse-Hankel or coprime-only theorem cannot be substituted for it. Characteristic two also identifies the two endpoints, so treating them as distinct requires a separate characteristic guard.

## Complete-family comparison ledger

- **Padded scalar Bezoutian/resultant and Hankel bridge:** classical component, with an explicit accepted coefficient map. The 1989 coprime formulation is a restricted historical comparison; the reopened 2010 Proposition 3.4 supplies the noncoprime field formulation.
- **Reciprocity and forced collision factor:** the existing accepted reduction uses expected-degree resultant covariance, with degree-one covariance exponent m^2. Busé–Mourrain Remark 2.1 and equation (2.2) remain the relevant [primary reference](https://arxiv.org/pdf/cs/0612050). This pass does not claim a new full-text inspection of that paper.
- **Trace variable w+w^(-1):** the accepted comparison to Baker Appendix B, Proposition B.1 and Remark B.2, remains a classical integral recurrence/reference. It requires no division by two. [Source](https://arxiv.org/html/2309.02512v2#A2).
- **Exact v,b and signed principal-minor coefficient:** the accepted computation specializes weighted resultant initial-form machinery. Its precise product and prescribed-degree interpretation are not printed in any passage verified in this pass. The existing Sturmfels Theorems 2.1/4.1 comparison remains a mechanism attribution, not an exact-family citation. [Source](https://link.springer.com/content/pdf/10.1023/A:1022497624378.pdf).
- **Residual determinant and endpoints:** Conrad's [Theorem A.1, p.5](https://kconrad.math.uconn.edu/blurbs/linmultialg/univid2old.pdf) was freshly reopened and gives the characteristic-polynomial resultant as a Kronecker-difference determinant over a commutative ring. The accepted generalized-pencil substitution and polynomial specialization lead to C03's N(w); evaluating its entries gives the two endpoint matrices. These are direct specialization steps, not an earlier verbatim printing of the whole package. Conrad is undated and cannot establish earliest historical priority.
- **Dated matrix-polynomial lineage:** Graf–Townsend [Section 2.4, equation (10)](https://arxiv.org/html/2503.22887v1) was freshly reopened. Its Kronecker-product divided-difference construction explicitly points to Heinig (1977), Barnett–Lancaster (1980), and Lerer–Tismenetsky (1982). Those older bodies were not acquired here, so their specific theorem hypotheses are not certified by the citation chain. They cannot be represented as verified complete-family antecedents.
- **Full package:** no primary statement verified in this pass combines arbitrary A,B, these two geometric diagonal deformations, formal degree, the closed exponents, signed principal-minor coefficient, and the endpoint package. This is a bounded nonmatch, not a worldwide absence result.

## Access record, deliverable boundary, and next gate

Allowed author-PDF open requests timed out; the www variant/direct download returned inaccessible/HTTP403. The publisher page returned HTTP403 through the open tool. A read-only attempt in dot's cloud browser returned ERR_BLOCKED_BY_CLIENT. Screenshot retrieval could not resolve the 1989 PDF, so no artwork is certified. No login, CAPTCHA, access restriction bypass, purchase, or local-computer action was attempted.

A final targeted check of the connected Library used title/author/DOI searches and the uploaded-PDF inventory (10 returned items, no continuation cursor). Ambiguously named mathematical candidates were resolved by their first-page text or image: Delvaux–Van Barel's 2008 Fourier-submatrix paper and Lubinsky–Saff's 1987 Padé/partial-theta paper. Neither is the 1989 article. The targeted local PDF-name and retained source-manifest check also supplied no matching primary copy. This establishes only a bounded no-match in the accessible material checked, not that no uploaded or unindexed copy exists. The Library pass did not alter the attribution conclusion.

Raw indexed search receipts are retained under local_verification_only solely for audit; their hashes identify returned extraction receipts, **not** the original article. They must not be included in a public package. Publish only this original comparison prose, locators, links and source-access qualifications. The raw third-party search excerpts and any future paper scans should remain local unless redistribution is authorized.

PUBLIC_SOURCE_LOCATORS.json pairs the exact cited locators with their access levels and any retained receipt hashes. Those receipt hashes do not certify unseen original PDF bytes. The downloaded nonmatching candidate scan, Library metadata and tool helpers also remain local-only.

The exact remaining source prerequisite is an authorized readable copy of the 1989 pages 1042, 1054 and 1065–1067, with complete normalization and formula arrays. Even satisfying that prerequisite would settle only this historical component unless it actually prints or subsumes the full diagonal family. A positive complete-family priority resolution needs an identified earlier statement and feature-by-feature map, not more proof controls.

**Apply nothing.** Preserve C03 correctness, score, novelty classification and all historical text. General sparse recovery remains a separate open task. This pass does not supply candidate sufficiency, base-field or legal-grid roots, a globally invertible denominator, a cyclic certificate, all-coefficient cubic recovery, or an FFT advance.
