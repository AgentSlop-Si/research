# Independent bounded source-domain comparison supplement

Date: 2026-10-23 UTC. Owner: M-SPARSE-DEFECT. Verdict: ACCEPT the source-domain comparison at its expressly bounded scope. No change to the separate mathematical acceptance, and no historical-novelty clearance.

## Exact target

This supplement reviews odd_codim2_predecessor_comparison_20261023/REPORT.md, SHA-256 628b546aef5ee7085465ad28f7918b8a9973f5d915fc223d4a5320d3359a9358, and its MANIFEST.json, SHA-256 2e93c2af6b4b6860b9682a10e7c34b64a9aa69ab688818a9b8bdf05de0872acc. All five manifest members and four original-file bindings match. The recorded search ledger contains 11 batches and 41 queries; this verifies the ledger's counts, not independent replay of that search.

The accepted theorem remains the one bound by author REPORT 77caa3fecaeef2d5dddab32a2a674c660fafa1040e52a43f17b2e059d4c1e359 and independent mathematical REVIEW 30e9ef6ddc95208d7ce5b885b1d07d09f5aa5414367aa371881967addde6118f. Neither file was changed. Exact comparison files are copied under sources/; BINDING_CHECK.json records verification.

## Objective and normalization

The correct objective is inf ||M−F||_2 over complex invertible M with at most N−2 nonzeros in each row of B=M^{-1}. Here F is normalized Fourier, N is odd, and the norm is the induced Euclidean operator norm. Coefficients, supports, and conditioning remain unrestricted.

For H=sqrt(N)F and X=sqrt(N)M, inverse zero patterns remain unchanged and ||X−H||_2^2=N||M−F||_2^2. The comparison's unnormalized constant 9−4sqrt(3) is therefore correct. Flat-unitary predecessors are relevant because the accepted proof needs only unitarity and constant entry magnitudes. Real-Hadamard-only assertions do not by themselves cover the stated odd complex orders.

## Classical ingredients

The equal-support estimate is exactly the first Welch bound with three unit vectors in dimension at most two: after x_i=sqrt(N/2)c_i, a normalized correlation of at least 1/2 becomes |<c_i,c_j>|≥1/N. The geometric paper's trace/rank proof supports this directly. Original Welch attribution is appropriate, but the original 1974 full text was not read in this comparison. [Datta, Howard and Cochran, Sections 1–2](https://arxiv.org/pdf/0909.0206).

Singleton intersections preclude orthogonality, and three vectors supported on two coordinates violate the corresponding dimension condition. The comparison correctly identifies these as quadrangularity/strong-quadrangularity ingredients, not a new support theorem or a quantitative inverse-row-distance result. The elementary odd-order pigeonhole step introduces no additional spectral-distance claim. [Severini, Definitions 1–2 and Lemma 1](https://arxiv.org/pdf/math/0205187).

## Sparse dual frames

The source defines duality by ΨΦ*=I, works over real or complex scalars, and studies sparsity for a fixed Φ. Theorem 3.2 and Proposition 3.3 give spark-based sparsity statements. The report's map Φ=M*, Ψ=M^{-1} is correct: ΨΦ*=M^{-1}M=I, row sparsity remains row sparsity of Ψ, and ||Φ−F*||_2=||M−F||_2. In the square invertible case the dual is unique. The read theorem passages do not supply a minimum perturbation radius as Φ varies around F*. Their total-entry statements and rowwise proof constraints must not be silently substituted for the simultaneous every-row budget. Thus this is a close structural neighbor, not an established matched quantitative predecessor. [Krahmer, Kutyniok and Lemvig, equation (2.3), Theorem 3.2, Proposition 3.3](https://arxiv.org/pdf/1204.5062).

## Residual approximate inverses

Holland–Wathen–Shaw's accessible publisher abstract minimizes ||T−PA|| over prescribed sparse P, initially discusses Frobenius norm, and explicitly considers other norms. It therefore cannot justify a blanket claim that approximate-inverse literature is Frobenius-only. Its publisher page also flags an appended correction; neither the article's full theorem text nor that correction was read. [Publisher abstract](https://epubs.siam.org/doi/10.1137/030601132).

Cosgrove–Díaz–Griewank's public publisher abstract explicitly discusses consistent residual norms and distinguishes the 1-norm, 2-norm, and Frobenius norm. Direct page opening returned 403 in this supplement; the indexed public publisher abstract was retrieved by a narrowly targeted title query. No full-text access or theorem review is claimed. [Publisher abstract](https://www.tandfonline.com/doi/abs/10.1080/00207169208804097).

The mathematical objective distinction is correct. With A=F, P=B, T=I,

    R=I−BF=B(M−F),
    M−F=B^{-1}R,
    ||R||_2=||B−F*||_2.

The residual objective approximates F* by B; the target objective approximates F by B^{-1}. They are not identical. This is not a claim that no transfer is possible: for invertible B, ||M−F||_2≥||R||_2/||B||_2, and unitarity gives ||B||_2≤1+||R||_2. A genuinely relevant published residual theorem could be transferred if all its support, invertibility, norm, and constant hypotheses were checked. No transfer establishing the accepted constant or an exact optimum was established in the inspected material. Prescribed-pattern constraints, possible singular P, and total-entry or column budgets also require explicit matching rather than identification by title.

## Limits and disposition

The comparison correctly separates classical ingredients from its internal quantitative strengthening. “Original-model” denotes the original admissible class, not historical originality. The supported conclusion is: no directly matched published bound or optimum was established in this bounded pass. It is not: no such theorem exists.

Residual-paper full texts and the noted correction remain unreviewed. This supplement did not repeat the mathematical proof, conduct a broad search, inspect the peripheral Xie abstract anew, or independently reproduce all search screening decisions. It directly checked the requested Welch, support-obstruction, dual-frame, and residual-objective mappings. Parent status stays TO RESEARCH; exact optimum, optimal constant, broader budgets, and historical priority remain unresolved.

No source or author inventory was modified, no scientific program was executed, and no external state was changed. This is a separately sealed supplement for the root and sole publisher.
