Public derivative of a source-bound reviewed research report. Private tracking and delivery details are omitted; mathematical claims, evidence, source attribution and remaining limits are retained. Original source-report SHA-256: 423754208acf362a9d2c2f9b286f828e7e546805712d282cff57ca1c99ea5014.

Review date: 12 October 2026 UTC.

# Q11 matching Green construction prior work review

12 October 2026 UTC

## Verdict

**ACCEPT the bounded attribution comparison, with the precision corrections below.** The four closest ingredient matches withstand independent primary-text review. No correction to the accepted 20q+1 construction, its field-operation costs, or its stated mathematical scope is required. Historical priority of the complete model-and-resource contract remains **UNRESOLVED**. Reject any interpretation of this audit as proving novelty, absence of a broader predecessor, optimality, or FFT or bit-model superiority.

The comparison archive reviewed is `Q11_Matching_Green_Bounded_Prior_Work_Comparison_2026-10-12.zip`, SHA-256 `45d3cdeec4d0341b0dd4fe3c1f95f07a59f7fdbba61566a9344afd11447945e9`. The mathematical acceptance archive remains `Q11_Subquadratic_Matching_Green_Bridge_Independent_ACCEPT_2026-10-12.zip`, SHA-256 `604a419f89bd0cb79e53448d39a37798bbef05e01bccc3d3421c98a2beec6a32`. Neither original archive was edited.

## Precision corrections

1. **Green order:** replace the report's description of Boito–Eidelman's definition as merely “off-diagonal rank conditions” with **overlapping rectangular rank conditions**. Their lower condition is rank B(k:N,1:k+r−1) ≤ r; for r=1 it already includes the diagonal position (k,k). This distinction does not change the report's conclusion that Green order is not an additive branch count.
2. **Fourier conventions:** Delvaux–Van Barel use a normalized Fourier matrix and, in their notation, row classes modulo n and column classes modulo m. For the desired direct specialization take n=5q, m=q. The reviewed report's m,n labels are swapped; its displayed unnormalized algebra is correct. Global normalization does not change rank, and the elementary exponent identity supplies the unnormalized factors directly without an added root-extraction step.
3. **SSS strength:** accept an exact scalar recurrence precedent and a related shifted block-resolvent sum. Do not abbreviate Eq. (2.10) to “two legal Q11 Green branches.” Its external shifts, state dimensions and separate block diagonal must remain visible until translated.
4. **Search evidence:** the packet contains 17 distinct recorded query strings, not an independently authenticated transcript of their execution. The count and list were verified; this reviewer did not witness or repeat those original searches. Likewise, the original access outcomes are retained as the author's disclosure, not independently recreated. This limitation is separate from the fresh theorem-level reads performed here.

## Frozen mathematical contract

The archived acceptance review and candidate report agree on m≥1, q=483^m, N=5q², supplied primitive complex root omega, and L=Q(omega). The full positive-chirp target is B=(F^(-1)+A)^(-1), F_ij=omega^(ij), A_ii=omega^(h i²), h=(N+1)/2. With alpha_i=omega^(−h i²), the inherited identity is

    B_ij = rho omega^(ij) − rho G alpha_i alpha_j omega^(−ij)
           + rho c alpha_i delta_ij,
    eta=omega^(q^4), G=q(1+2eta²+2eta³), c=NG, rho=(1+c)^(-1).

In particular G²=N and rho=(1−c)/(1−125q^6), with a nonzero rational denominator. Each branch is L_b(I−W_b)^(-1)R_b, with arbitrary diagonal endpoints, permitted zero masks, a Hamiltonian structural successor on the original coordinates, and (W_bx)_i=w_i x_(sigma_b(i)). Zero edge weights are allowed. The inverse guard is 1−product(w_i)≠0. There is no free diagonal or unmatched endpoint permutation.

The accepted representation has 20q+1 branches, all zero-holonomy. It has O(N) compressed exact-field preparation, Theta(Nq) paid direct application, Theta(Nq) expanded descriptor writes/storage when materialized, and O(N) live field slots. The field degree grows with N. These are not unit-bit-cost, numerical-stability or practical-timing claims. This attribution review inherits, and does not rerun, that acceptance proof.

The original five-dimensional minimum-three result remains accepted; the broader Q11 problem remains open.

## Four closest primary matches

### Exact composite Fourier blocks

The retained final Delvaux–Van Barel article was freshly read through a retained authorized copy, including printed pp.1593–1594, Eq. (15), and pp.1599–1602 of Section 4. Eq. (15) factors the normalized block with entries omega^((a+in)(b+jm))/sqrt(mn) as an outer product. With n=5q and m=q, Q11 retains these row classes and divides each column class modulo q into five classes modulo 5q. Restricting rank-one blocks preserves rank one. The displayed Fourier primitive is therefore an exact precedent; approximate butterfly structure is a weaker comparison. Section 4 interprets its hierarchy through the classical radix-two FFT. Neither inspected portion supplies the additive matching packing or Q11's compressed resource accounting. [Final article](https://doi.org/10.1016/j.laa.2008.04.043).

The prior PDF hash was recorded as `af33370c7d4b8f3853d36c01b512b007512886431af4963cdc6d7638af89aae4`. The reviewer verified the old audit's byte pin and freshly read the retained PDF by retained source identity; the PDF byte hash itself was not newly recomputed. This distinction is recorded in the evidence ledger.

### Canonical matching rounds

Lambrechts, Ficker, Goossens and Spieksma, Section 2.3, printed p.281, specify an even team count n, a fixed team n meeting team r in round r, and remaining pair i,j satisfying i+j=2r modulo n−1. Set n=s+1 for odd s, remove the fixed team, and relabel residues. The unmatched class is t, and the pairs are exactly {t+d,t−d}, 1≤d≤(s−1)/2. This verifies the report's exact schedule match. The paper is an accessible primary account of an established method; no earliest-origin attribution to these authors is warranted. Its carry-over optimality theorem is irrelevant to Green branch optimality. [Author-hosted final paper](https://fspieksma.win.tue.nl/papers/MathPro2018paper.pdf).

### Weighted cyclic inverse including zero weights

Huhtanen–Perämäki, Theorem 2.9, manuscript p.6, assumes a cyclic shift S, diagonal D, and nonsingular I+DS. It imposes no requirement that each entry of D be nonzero. Its inverse expansion specializes to I−W after a common coordinate relabeling and D=−diag(w). The denominator becomes 1−product(w_i). Theorem 2.10 is a separate result requiring invertible diagonal data and an nth-root choice for its nonzero constant cycle weight; it does not justify normalizing nilpotent Q11 branches. The principal 2n−1 factorization is multiplicative, so it is not an additive branch theorem. [Author manuscript, Theorems 2.9–2.10](https://math.aalto.fi/~mhuhtane/manu.pdf).

### Bidirectional scalar scans and shifted resolvents

Chandrasekaran–Epperly–Govindarajan, Section 2.2, Eqs. (2.6)–(2.8), explicitly give forward/backward state recurrences and multiplication from prepared generators. Eq. (2.10) is

    A = D + U Z^T (I−W Z^T)^(-1) V^T
          + P Z (I−R Z)^(-1) Q^T.

Here the bold source symbols are block diagonal and Z is the nilpotent downshift. The independent endpoint shifts, block state spaces and free diagonal distinguish this expression from a count of scalar Q11 branches. For a supplied Q11 path, its scalar recurrence is an exact specialization of the same algebraic mechanism. Section 3.1 also verifies the corner-replacement/restoration comparison. The source presents real-valued generators, but the elementary finite recurrence is valid over L; a real-versus-cyclotomic distinction alone would not defeat this overlap. Arbitrary matrix transitions cannot be counted as separately evolving scalar modes without additional decoupling. [Primary version 3](https://arxiv.org/html/1911.05858v3).

## Remaining primary comparisons

Boito–Eidelman, Section 2, Eqs. (2.1)–(2.3) and Theorem 2.1, support the rank-structured Green/quasiseparable comparison with the overlapping-rank correction above. Their band-inverse equivalence requires invertibility. Since masking may make L_b(I−W_b)^(-1)R_b singular, nonsingularity of I−W_b alone does not authorize inverting the complete branch. [Primary article](https://arxiv.org/html/2308.02701).

Li–Yang–Martin–Ho–Ying, pp.720–723, Eqs. (7)–(9), construct approximate low-rank middle blocks and assemble a sparse multiplicative butterfly factorization. Eq. (7) immediately precedes Section 3.1, rather than being inside it; this is a locator refinement only. The report fairly identifies a block-organization precedent while declining to import an exact additive grammar or its costs. [Author-hosted paper](https://web.stanford.edu/~lexing/BF.pdf).

Zheng–Puy–Riccietti–Pérez–Gribonval, Section 2, explicitly set N=2^L, define the Monarch classes, and characterize membership by rank at most one on the specified row/column block partitions. The broader identification procedure seeks permutations and uses a heuristic approximation objective. Q11's analytic non-dyadic partition is therefore not an unchanged application of that dyadic identification result. [Primary body](https://arxiv.org/html/2307.00820).

Thomas–Gu–Dao–Rudra–Ré, Sections 2–3, give AM−MB=R, disjoint-spectrum recovery, weighted subdiagonal/corner operators, and a Krylov-product parametrization. Proposition 3's stated displacement pair involves A^(-1); a nilpotent Q11 operator cannot simply replace it. The elementary Krylov matrix itself still exists for nilpotent A. No complete Q11 displacement certificate or branch count follows solely from the low-displacement vocabulary. [Official proceedings paper](https://proceedings.neurips.cc/paper_files/paper/2018/file/8e621619d71d0ae5ef4e631ad586334f-Paper.pdf).

## Independent translation and assembly check

These are reviewer calculations about the accepted construction, not statements attributed to the cited sources.

For s=5q and i=a+su, j=b+sv, the difference ij−ib−a(j−b)=s²uv is divisible by N. Thus each same-partition Fourier block has rank one. Replacing omega by its inverse and applying the nonzero chirp diagonals preserves this statement. Both pieces are two-sided diagonal scalings, not a required diagonal similarity.

For any weighted Hamiltonian successor cycle, W^N=hI with h=product(w_i). Therefore (I−W)sum_(k=0)^(N−1)W^k=(1−h)I. No individual edge division occurs. If h=0, the inverse is a finite path sum. Zero boundaries isolate components; disjoint endpoint masks select an outer-product rectangle. A common permutation can describe the proof ordering and conjugate back without introducing unmatched endpoint permutations.

In a round, each paired class component can carry independent forward and reverse factors for every supplied rank-one mode. On the singleton, opposite scans include the diagonal twice. Every class is a singleton once, so one final W=0 branch removes the duplicated diagonal and inserts the desired correction. This gives 2rs+1 legal branches for an odd s-class partition with r supplied outer products per ordered class block. For Q11, r=2 and s=5q, giving 20q+1.

The four-table O(N) preparation is special to the analytic shared Fourier factors. It does not follow for an arbitrary supplied rank-r block matrix. Expanded occurrences and each application's indexing, routing, multiplication, accumulation and outputs remain paid. Ordinary block multiplication already explains O(Ns); matching is what fits that computation into the permitted additive Green grammar. The inherited two-DFT O(N log N) evaluator remains asymptotically faster.

The independent standard-library checker verifies 77,700 modular grid entries, complete canonical matchings through s=2415, 343 guarded weighted-cycle specializations (301 with at least one zero edge), and four generic supplied-factor packing instances totaling 586 matrix entries. All 20 unit-holonomy cases are excluded. Removing diagonal calibration is detected in every packing instance. Small grid/packing controls are not members of the frozen family, and the s=2415 matching check is not a full million-coordinate Q11 application. The infinite-family acceptance and its full resource certificate are not replaced by these controls.

## Provenance and stopping boundary

The independent checker verifies all 10 manifest payload entries in the comparison archive and all 13 in the acceptance archive. It checks the acceptance-review hash, nested candidate hash, author-report pin, eight primary-comparison rows and 17 distinct recorded queries. Separately, all eight local source pins in the comparison ledger were freshly recomputed and matched. The checker was newly written; no supplied research program was imported or executed.

Fresh primary reads covered all eight cited comparisons. The Delvaux final body was read from the retained authorized copy. No whole third-party paper is included in this packet.

The 2007 Delvaux–Van Barel Kronecker article and older attribution chains remain unexhausted. This review therefore establishes exact ingredient overlap and checks the proposed assembly boundary. It does not establish that no broader theorem specializes to the whole contract. Preserve the accepted full positive-family upper, fixed-field impossibility, ordinary-order-only lower bound, retired five-dimensional minimum-three result and open arbitrary-cycle optimality, all-length, negative-family, stability and historical-priority questions. No historical-novelty determination is justified.

Recommended short annotation: **The accepted 20q+1-term Q11 upper explicitly assembles classical exact Fourier blocks, canonical round-robin matchings and scalar scans, with paid diagonal calibration and compressed coefficient synthesis. Its complete-contract priority remains unresolved. Its direct application improves the dense additive baseline and remains slower than the two-DFT evaluator.**
