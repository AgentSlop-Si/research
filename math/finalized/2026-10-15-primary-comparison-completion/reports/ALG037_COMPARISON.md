# ALG-037: primary-source comparison and scope decision

15 October 2026. Read-only comparison of Catalogue138 / Research overview199. Candidate for independent review; no workbook or repository write is performed here.

## Outcome

**The bounded comparison task is complete as a documented qualified nonmatch, with one explicit primary-text access boundary.** The accepted rank theorem remains unchanged. None of the three primary full-text comparators inspected states the same combination of target, error scale, decoder restriction and fixed-input success probability. This is not a claim that no equivalent theorem exists anywhere. In particular, the closest older linear-width antecedent, Mathé (1991), was located but its original theorem was not readable through the available publisher route; its exact constants and equivalence are not certified.

The live gate expressly permits a primary theorem mapping **or** a qualified nonmatch/specific access blocker. That gate is discharged, rather than silently changed into worldwide novelty certification. ALG-037's own live record has no outstanding construction or implementation requirement: nonlinear and input-dependent algorithms are exclusions, not an uncompleted algorithm promised by this record. Subject to independent acceptance, this record may therefore be CLOSED at its guarded theorem-plus-bounded-comparison scope. Preserve score 34, classification C and all history. Do not close another algorithm or infer an unrestricted FFT lower bound.

## 1. Exact retained contract

For any N-by-N unitary U and a measurable random complete linear map A_w whose law is independent of x, assume for every fixed x

    P(||A_w x - Ux||∞ <= ε ||x||1 / sqrt(N)) >= 1-δ,
    0 <= ε < 1, 0 <= δ < 1.

Then E rank(A_w) >= N(1-δ)(1-ε²). An almost-sure rank cap K obeys the same lower bound. This includes K linear measurements followed by a linear decoder, and fixed weighted sums with their total rank budget. It does not require one seed to work for every input. The dense-input extension uses the deterministic sequence e_j+(1/m)1 and closed success events. Original proof SHA256 fc6951129d6daaa9a962cc2e6fd012b6853a8df26f179a5f978c3b9beb21b007; independent proof review 5c0f8d0931a543512644d8aad3d164dd9eee35eb455cbb6591ae8a70b208fc87.

This is a rank/information representation constraint. No arithmetic, bit, wall-clock, data-ingestion or output-materialization lower bound follows from rank alone. The earlier proof's conventional K-point FFT discussion is conditional on actually using that implementation.

## 2. Sparse Fourier recovery and sampling: exact primary mapping

Hassanieh–Indyk–Katabi–Price, *Nearly Optimal Sparse Fourier Transform*, author full text: https://haitham.ece.illinois.edu/Papers/hikp12.pdf . Inspect §2 (printed pp.4–6), Algorithm4.1 (p.11), Theorem4.9 and proof (pp.19–20), Theorem6.1 (p.21) and its proof (pp.21–23).

For U equal to the unitary DFT and y=Ux, Theorem4.9 gives probability 2/3 and

    ||y-z||2 <= (1+η) min_{k-sparse v} ||y-v||2 + τ||y||2,
    time O((k/η) log(N/k) log(N/τ)).

The proof bounds expected running time; this is not a bit-cost or full N-output materialization certificate. Here η is its approximation parameter; τ is its additive-precision parameter, **not** ALG-037's failure probability. The length is a power of two. Omitting the additive term requires the paper's polynomial signal-to-tail condition. Algorithm4.1 uses coordinate medians and largest-coordinate selection despite nonadaptive measurements. Its output representation is sparse.

Theorem6.1 instead assumes a flat unitary F, adaptive coordinate samples of Fy, factor-2 best-k-term ℓ2 recovery with probability at least 3/4, and concludes Ω(k log(N/k)/log log N) samples. It measures sample count, not complete-map rank. [Same primary source.]

**Our mapping/nonmatch:** In the DFT special case, target and probability quantifier can be aligned with ALG-037, but neither theorem has its norm or full linear decoder restriction. A nonadaptive measurement matrix does not make the reconstruction linear. For x=e_j, the DFT output has N entries of magnitude 1/sqrt(N), and its best-k-term tail is sqrt(1-k/N). A factor-2 tail contract even permits the zero approximation when k<=3N/4; ALG-037 forbids zero on that input for every ε<1. This is a concrete scale nonimplication, not merely different notation. Neither sampling theorem certifies a general rank-N or NlogN runtime barrier.

## 3. Randomized approximation widths: exact primary mapping

Kunsch–Novak–Wnuk, *Randomized approximation of summable sequences—adaptive and non-adaptive*, arXiv:2308.01705v3: https://arxiv.org/html/2308.01705v3 . Inspect §1's algorithm/error definitions and §2.3, Theorem2.7 and its complete proof.

Their cost n counts arbitrary real linear functionals. Reconstruction may be nonlinear. Their error is sup_{||x||1<=1} E||A(x)-x||∞. Theorem2.7 gives this error at least ε0=(1/3)(1/20-e^-4)>0 whenever m>=C exp(a n²), for suitable positive constants C,a. Equivalently, achieving error below ε0 needs n>=sqrt(log(m/C)/a). This is a real identity-embedding result, not Fourier recovery or an arithmetic-cost theorem.

**Our mapping/nonmatch:** Set m=N and, for a fixed-rank sketch, n=K. An input-independent linear ALG-037 estimator is a restricted information algorithm, but its target is U and its guarantee is a probability threshold with uncontrolled failure magnitude. A probability bound alone gives no finite mean-error upper bound. Applying U* to the output preserves ℓ2, not ℓ∞. The safe converted success statement is ||U*A_w x-x||2<=ε||x||1, with no 1/sqrt(N) gain left. Thus the primary theorem does not yield the exact N(1-δ)(1-ε²) formula.

## 4. Deterministic perturbed-identity rank: exact primary mapping

Alon, *Perturbed identity matrices have high rank: proof and applications*, author full text: https://www.math.tau.ac.il/~nogaa/PDFS/identity1.pdf . Inspect Theorems1.1/2.1, Lemma2.2 and §2 proofs (author PDF pp.1–3).

Theorem1.1 assumes a real n-by-n B, |b_ii|>=1/2, |b_ij|<=ρ for i≠j, and 1/(2sqrt(n))<=ρ<1/4. It concludes rank(B)>=c log(n)/(ρ² log(1/ρ)). Lemma2.2 gives rank(B)>=n/(1+(n-1)ρ²) for real symmetric B with diagonal1. These are deterministic rank statements; no computational-work model is asserted.

**Our mapping/nonmatch:** U*A_w preserves complex rank, but transforms a successful column's strong ℓ∞ error only into an ℓ2 error <=ε. An entrywise bound <=ε follows for that column, not ε/sqrt(N), and there is no common all-column success event. The transformed matrix need not be real or symmetric. Even in a deterministic real identity special case, Alon's rank inequality is a different formula under different hypotheses. Its trace/energy mechanism is a classical relative of the retained projection proof, not a verbatim probabilistic unitary theorem.

## 5. Older antecedent: explicitly bounded access result

The KNW introduction attributes linear randomized ℓ1^m→ℓ2^m constant-order lower bounds for m>=2n, and ℓ1^m→ℓ∞^m n^-1/2 lower bounds, to Mathé, *Random approximation of Sobolev embeddings*, Journal of Complexity7 (1991),261–281, §3 Lemma2(ii). This is a useful primary-source lead, not a fresh read of that lemma. DOI: https://doi.org/10.1016/0885-064X(91)90036-W . The publisher record is https://www.sciencedirect.com/science/article/pii/0885064X9190036W . Its record identifies an open-archive article, but direct fulltext retrieval returned403; the PDF route also failed. Do not mislabel it inherently paywalled, and do not promote the later authors' attribution to an independently inspected 1991 theorem.

Eckart–Young's original1936 article was also located at DOI10.1007/BF02288367, but the publisher fulltext route was inaccessible in this pass. It is not used as a primary-read theorem in this deliverable. No third-party abstract or search snippet is treated as proof evidence.

## 6. Norm, model and closure controls

On ALG-037's success event, ||error||2/||x||2 <= ε||x||1/||x||2, which can range up to εsqrt(N). Thus an apparently small per-bin error does not guarantee a small uniform relative-ℓ2 error for dense inputs. At coordinate inputs the stronger ε bound is precisely what drives the rank obstruction. Promises quantitatively separating inputs from coordinate vectors require a new analysis; merely requiring nonzero coordinates does not.

Input-dependent importance sampling, adaptive selection and nonlinear coordinate medians remain outside the complete fixed-seed linear-map theorem. No experiments, new implementation, changed-interface solver, priority upgrade, worldwide novelty determination or general FFT complexity result was obtained or required by this comparison. Reopening is justified by a newly accessible exact primary antecedent or contradictory evidence, not an indefinite negative search.

## Evidence and proposed edits

SOURCE_READ_RECEIPT.json records exact accessible theorem locations and source-access limits. The local sources directory contains unmodified tool-read receipts solely for local verification, not republication; their hashes identify the receipts, not PDF bytes. The public deliverable contains original comparison prose and mathematical mappings only. EXACT_CELL_PROPOSALS.json contains eight guarded, before/after edits; all descriptive histories are retained verbatim. Applying the CLOSED proposal requires independent acceptance and a fresh preflight of those exact before-values. No scores, novelty classification, aliases, source proof bytes or other records change.
