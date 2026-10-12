# Exact factorization and manuscript binding

## Equation identity

The construction reuses the classical positive, unnormalized Fourier factorization recorded in ALG-022/F096. This is an exact equation correspondence, not a similarity of titles.

The archived source [Exact Fourier reduction to one reusable fixed kernel](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/bc/bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0__059_bc62a95e8677464a.inert.txt), SHA-256 bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0, specifies in lines 11–23:

- N dyadic, q primitive of order N, zero-based F[i,j] = q^(ij)
- f_j = product from s=1 to j of (1−q^s), S = diag(f_j)
- T_ij = [i≥j]/f_(i−j)
- d_j = (−1)^j q^(j(j−1)/2)/f_j
- F = S T diag(d) T^transpose S

Lines 25–40 give the classical q-binomial LDL^T attribution and rational-identity/nonzero-denominator justification. Lines 42–45 specify the full input/output and reusable kernel. Lines 68–79 and 140–149 retain the ordinary O(N log N) convolution application bound and exclude a faster direct application oracle, bit-complexity or stability claim. The archive URL uses the main branch; the SHA-256 above fixes the reviewed bytes.

Section 4, equation (1), of the submitted proof is identical under N=r, q=u, f_j=H_j, S=D_H and d_j=p_j/H_j. The positive sign, lack of normalization, ordinary transpose, sign factor and chirp exponent all match. No inverse, conjugate transpose, 1/r, reversal, square root or phase adjustment is needed.

## Domain and cost boundaries

The identities coincide on the original dyadic-field domain, including its complex cyclotomic specialization. Their theorem contracts are not identical. The archived package states dyadic N over suitable fields of characteristic not dividing N. The reviewed local compiler states every positive r over the complex numbers, uses additional supplied power-of-two roots, and uses conjugates of prepared root expressions for the nonzero regularizer. No extension of that complex norm-regularization theorem to arbitrary finite fields is inferred. The finite-field checks use a different shift-selection procedure.

The separate F096 sources with SHA-256 4571d3e8e6f06f0ddfe0c57b78b84b2c03c77ea5f5b78643f1a7766ef201473e and 58001a15deae9625ae6b4bf9e98327fc3c6138a8e5196e2fd152ede1894193de concern the finite q-exponential tail/first-layer recurrence and sparse q-difference forcing, respectively. They are not this compiler theorem. Sharing a factorization or family label does not resolve those other application-cost questions.

Exactly r refers to the emitted word's data coordinates. Polynomial coefficient, schedule and index storage are separate. O(log² r) counts local layers, not sequential work for an arbitrary r-vector. The global saving uses synchronized small-axis words and an imported charged C-tensor engine. It does not follow from treating each layer as constant sequential work.

## Corrected prior comparison

The reviewed OpenAI local manuscript displays O(log⁴ r), but its same pinned revision already includes the model-matching exact-width O(log² r) compiler, charged polynomial preparation and two-bank construction introduced on 8 October 2026. The accepted one-bank mathematics is therefore an alternative implementation of a prior asymptotic theorem. See [the detailed prior review](COMPOSITION_AND_PRIOR_REVIEW.md) and [the corrected audit](AUDIT.md).

The source-binding review used for this checkpoint has SHA-256 351c4e8b155d45933b7719f95eca3930faab3cb0e25895aaeb37fc297d654c39. This public account is a purpose-written derivative that preserves its mathematical correspondence and corrected conclusion; it does not reproduce operational records.

## Original and public reading copy

The submitted seven-page PDF, dated 13 October 2026, has SHA-256 bfe36aa3cf26cfda0e74fbab75d1f3d021c9dd98ba78be8c1752bd2f10e651d5 and 363,389 bytes. It is not included in this checkpoint and has not been altered. The source package's PDF has SHA-256 267dfe8c7ac9c0d525bf7d4d1cb2d1a821790120446c4fe21799a9204d023190 and 320,656 bytes. Static checks found the same extracted plain/layout text, the same seven decoded page-content streams, and identical page renders at the checked resolution, although their PDF containers differ. The package's LaTeX source has SHA-256 4eab0dc0011ff5bf169989d24584891a4e5322e17f69fdecc710aab98592373b.

[PROOF_READING_COPY.pdf](PROOF_READING_COPY.pdf) is newly typeset from that source and expressly labeled an editorial derivative. It adds a correction page and a separate Section 6 annotation, omits one nonmathematical paragraph, restates one nonmathematical test-provenance sentence, and uses black title styling. Sections 1–5 are preserved byte-for-byte in the mathematical-source body; their extracted source segment has SHA-256 2d0449aac164c399bf137eaa4c40c7405ef6b2852bf612af8e294df69331a382. No original source file was edited. The original historical-comparison paragraphs are retained for auditability and are explicitly superseded, not silently rewritten.

The corrected four-page audit PDF is included unchanged at SHA-256 1d9bb0604a0e1b723da69e9e41c48812ec1e9bc65cd696490f5fb2cecb08b5a5. The public manifest pins this PDF, its Markdown companion, the proof reading copy and every other published file.
