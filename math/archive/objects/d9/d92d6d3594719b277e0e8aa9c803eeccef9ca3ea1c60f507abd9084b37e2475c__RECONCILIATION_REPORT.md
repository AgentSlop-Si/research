# Seventy recovered historical texts: full-text and status reconciliation

10 October 2026 UTC. Bounded coverage/status review, separate from the new Frobenius-extension proof audit.

## Result

All **70 recovered texts, totaling 191,264 bytes**, are byte-for-byte members of **21 already preserved original ZIPs**. This review read their complete text and reconciled the proof-bearing and substantive narrative claims with the identified earlier scoped audits. **No additional theorem or newly missing original is established by this recovery.** The useful change is stronger source traceability and preservation of corrections that older source summaries can otherwise obscure.

There are 43 Markdown files and 27 text files. Only seven are standalone theorem/proof certificates; one more is a supporting precision note. The rest comprise 23 README/checkpoint/handoff narratives, four source prior-art narratives, three validation narratives, five run instructions, ten historical logs, and seventeen manifests. “Seventy reviewed texts” must not become “seventy independently proved theorems.”

The seven proof documents agree with already reviewed research branches **at their corrected scopes**. Several historical claims require the existing corrections summarized below. No fresh source programs, uploaded checkers, inherited audit checkers, native binaries, or run instructions were executed. Fresh computation in this reconciliation is limited to independently authored byte/hash and ledger checks.

## 1. Evidence chain and limits of the coverage count

The parent inventory reconciliation reports 1,394 distinct notable source texts: 1,324 whose hashes match standalone master files and these 70 whose exact bytes were found inside already recovered original archives. This report independently checks the 70-item residue. It does not independently certify the completeness of the source-provided inventory, every Library item, or all historical attachments.

For each of the 70 entries, the fresh verifier:

1. Selects a preserved original ZIP named in `EXTERNAL_INVENTORY_RECOVERY.json` and hashes the complete archive.
2. Requires a unique member with the selected exact member name, reads it as inert bytes, and verifies its byte count and SHA-256 against the inventory.
3. Compares the member bytes directly with the recovered standalone text and validates its complete UTF-8 decoding.
4. Confirms its hash is absent from the supplied standalone-master hash snapshot, and confirms the recovered-text hash sets before and after this review agree.
5. Rehashes every previously located exact local extraction used for comparison.

All checks pass. Six source-archive hashes are additionally matched directly to hashes declared in the earlier substantive audit/provenance records: sparse defect, Green Phases 25, 26 and 33, mixed-radix v13, and packet/separator v19. The latter two Phase33/v19 identities are particularly useful because their previous review read the archives directly rather than relying on an extracted source tree.

**52 of the 70 texts already have exact-byte extracted counterparts in earlier local research packages.** The remaining 18 have no match in the targeted local extraction scan, but all 18 have verified original archive members. The targeted scan was over the existing materials, research-round, synthesis, and update-package directories; it was not a proof of absence from every possible filesystem location. These are byte-coverage distinctions, not theorem-novelty distinctions.

`ARCHIVE_MEMBER_VERIFICATION.json` records every selected archive, complete archive hash, member path, member hash, and exact local counterpart. `ITEM_RECONCILIATION.json` adds per-item content scope, existing disposition, corrections, and prior review paths. `PRIOR_REVIEW_EVIDENCE.json` hashes the twelve consulted review documents. None of the source files or previous seals was modified.

## 2. Proof-bearing families and the status that must be retained

### Sparse-defect gate: items 6–10

The previously accepted Fourier sparse-rank and inverse-stage obstructions remain valid. In particular, the Fourier sparse-defect bound is `rank(F−B) >= floor(N/(q+1))` for the stated row-sparsity model, and the inverse-stage consequence uses the product of the stage sparsity budgets.

The historical scan example initially established a **bandwidth** obstruction. It did not, by itself, establish distance from every arbitrarily row-sparse matrix. The separate existing `ARBITRARY_SPARSE_REPAIR.md` supplies the required stronger bound

    rank(S^(-1)−B) >= ceil(floor(N/(q+2))/(2q+1)),

for the specified scan matrix and every row-q-sparse B. For fixed q this is linear in N, including allowed monomial changes. The source certificate and its later repair must travel together.

Retain the fully charged variable-r Woodbury costs: preparation `O(N+Nr²+r³)`, application `O(N+Nr+r²)`, storage `O(N+Nr+r²)`. The no-pivot Thomas implementation additionally needs its pivots nonzero; invertibility of a tridiagonal matrix alone is insufficient. Those executor guards do not restrict the abstract rank theorem. Historical run logs add no fresh execution evidence.

### Green Phase25: items 42–49

The affine-run structured-input Fourier executor, all-stride rank bound, commutator rank and hidden-cut obstruction retain their earlier acceptance. The structured-input evaluator has charged `O(rN+r log N)` arithmetic with the supplied run description and field/root contract. It does not evaluate an arbitrary vector in that cost merely because an ordering has few runs.

**The source's unconditional inverse-of-a-sum statement is false.** Writing `S=A^(-1)+B^(-1)=A^(-1)(A+B)B^(-1)`, its inverse exists exactly when `A+B` is invertible. With the source's cyclic resolvents, admissible parameters `alpha=3/2, beta=1/2` make the sum annihilate the all-ones vector. Even when the sum is nonsingular, the source unpivoted band/Woodbury implementation can encounter a zero pivot or a singular band base.

The accepted correction is already available: require `det(A+B) != 0` and use the whole-matrix pivoted constant-frontier solver. It solves all nonsingular instances and detects singularity in linear field-arithmetic work and storage. It does not assume favorable band pivots, and it is not a floating-point stability or bit-complexity theorem. The source's old theorem, README, validation and checkpoint wording cannot supersede this repair merely by being recovered again.

### Green Phase26: items 11–18

The earlier common-character-cut argument still proves `Q = Omega(log N/log log N)` for products of weighted cyclic Green sums with fixed step/exception budgets and **affine** intermediate coordinate permutations. The accepted audit strengthens the crossing constant and keeps arbitrary allowed diagonal gates. It does not cover arbitrary non-affine interstage permutations, free shared-state computation, or unrestricted FFT circuits.

Two prior corrections remain mandatory. First, the source's floating-tolerance witness can accept equality where the proof requires strictness; at `N=16` and strides `[1,2,8]`, `h=1` has a shift `8=N/r`. The correct acceptance predicate is integer `r*abs(t)<N`. Second, the finite logarithmic necessary inequality needs its small-bridge branch condition or a disjunction with the large-bridge case. The fixed-budget asymptotic theorem survives. Including Phase25 as a nested predecessor does not repair its inverse-of-a-sum claim automatically.

### Mixed-radix v13: items 19–27

The accepted results concern the exact operator/projector identity, covariance and a randomized approximate full-output estimator under the stated arithmetic and precision assumptions. The standalone theorem and precision note do not establish a general exact accelerated Fourier evaluator.

An individual character row has the already audited projector geometry and nonzero error. The **complete** character bank is exact, but that bridge was already present in the previous work and its fully materialized computation reduces to ordinary Cooley–Tukey. It is not a new v13 sub-`N log N` result.

Retain the earlier one-row finite-field phase-sign correction: summing a complete bank can hide this error because the alternative signs permute its channels. Also retain the stronger independent result that conditional pairwise independence of the character choices can suffice with a shared slope; the source's blanket claim that full state independence is indispensable is too strong. Precision coverage is partial/conditional, and timing proxies are not same-accuracy full-transform benchmarks. The four recovered test/experiment logs remain historical records.

### Green Phase33: items 50–56

The existing audit accepts several distinct results, each with a different quantifier:

- The six-variable two-Green certificate excludes the **specified cycle pairs and fixed couplings**, while allowing arbitrary invertible two-sided diagonal gauges. It does not exclude every cycle/coupling choice.
- The `q²` dimension bound describes a nonsingular response chart and a generic additional target vector. It is not a proof that a particular Fourier vector is absent from every chart.
- The tangent obstruction is local. Matching five full columns and the first five entries of a sixth is not a full matrix identity.
- The inherited common-separated-rectangle argument gives `floor(N/2^q)^2 <= qN`, hence an additive `q = Omega(log N)` restriction. Products and shared-state algorithms are outside that statement.

The old prose described extra large-size controls absent from its main saved JSON; the earlier independent audit supplied those controls. This reconciliation does not relabel either historical source logs or prior independent controls as newly executed tests.

### Multistage bit-reversal geometry: items 59–64

The accepted all-size dimension upper bound is

    min(N², N+t(4N−6)),

for the stated separated-generator parameter image, retaining `N>=3`. Exact Jacobian saturation was certified at `N=8,16,32` and the stated saved depths; identity stages extend the corresponding full-dimensional conclusions to greater depths at those same sizes. This does not establish saturation at all N or a Fourier factorization. The separated-generator image must not silently be replaced by every quasiseparable boundary component. A generic dimension exclusion also does not single out Fourier without a separate argument.

### Endpoint minimax: items 65–69

The accepted characteristic-zero theorem states that for dyadic `N>=8`, the minimum possible maximum quasiseparable cut rank under **independent row and column permutations** is `N/4+1`; bit reversal attains it. The rank recurrence and coset formula survive the earlier review.

The summed-rank conclusion is asymptotic in its leading term. The previous audit proved exact finite-size total minima at N=8 and N=16, not for every N. This is a single-matrix representation theorem, not an arithmetic improvement or a general multistage exclusion. The historical standalone exploratory entry point also refers to a missing sibling module; that does not invalidate the proof or turn its old log into a portable current replay.

## 3. Recovered narratives that need current context

**Three-stage bit reversal, items 37–40.** The source's uniform cut for `N=32m>=64` was already accepted: cut capacity `12m+1` is below the natural-endpoint Fourier block rank `13m`. This is a genuine earlier source improvement over the older N128 witness, but not a new result created by recovering its README and handoff. More importantly, its suggestion that four stages remain the next unexcluded growing-family lead is obsolete. The later accepted central-partition theorem proves `N/2 <= d_N sum r_i`, yielding total quasiseparable order `Omega(sqrt N)` and excluding four rank-one repeated-bit-reversal stages at every dyadic `N>=128`. Its all-length scope is permutations preserving or swapping the designated groups, not arbitrary mixing shuffles. N64 remaining unexcluded at depth four is not an existence claim.

**Packet/separator v19, items 28–29.** These are a prior-art narrative and README, not a newly recovered v19 proof. Earlier packet fusion and rational common-order rank statements retain their guards and coefficient/numerator costs. The old proposed sparse high-treewidth direct-inverse escape is unavailable: if `A^(-1)=LFR` for invertible monomial L,R, then `A=R^(-1)F^(-1)L^(-1)` is dense. Its denominator cannot have constant degree. The previous independent audit already supplied this correction and a stronger guard-free separator lemma.

**Offset-class v12, items 32–33.** The accepted row-covariance and approximation statements keep the specified half-up rounding, prime-power/divisor model, future-query/no-reread conditions where used, and precision assumptions. Literal sorting by `np.unique` does not establish the advertised linear work; the earlier structural residue-class construction repairs this. The source's assertion that the exact v11 chain was missing a core file was previously disproved by a byte-identical core. Do not reinstate that provenance claim.

**Unit-step chirp v9, item 34.** The README's one-cycle estimator belongs to the previously audited prime-power/divisor and exact-index contract. The zero projector at M=1, mixed-prime limitations, corrected precision contract and timing qualifications remain. The source README is not new independent evidence for a uniform arbitrary-length fixed-precision FFT.

## 4. Metadata-only and historical-execution scopes

Items 0–5, 30–31, 35–36, 41, 57 and 58 contribute only historical logs or manifests to this 70-item recovery. They concern Weyl expansion, Phase34, moving partitions, Hero0 Phase12, interleaved scans, two-stage cuts, global/wide-scan gates, bidirectional macros, Hero17 Phase5 and an earlier updates audit. Their complete text was read, but this reconciliation makes no fresh theorem acceptance claim for those branches based on these files.

All ten logs are source-reported results. All seventeen manifest texts are inert hash declarations; verifying the recovered manifest's own bytes does not assert that every declared package member was rerun or independently proved here. Likewise, reading five run-instruction files does not authorize or constitute executing their commands. Source prior-art summaries remain source narratives; no new external literature/priority review was performed for these older branches in this task.

Exploratory same-basename/fuzzy comparisons made before exact linking are outside this seal and are not evidence of semantic equivalence. The final ledger relies on exact-byte links, source archive hashes, complete text reading and identified prior scope/correction records.

## 5. What this closure permits

The master coverage narrative may now state that these 70 historical texts have been recovered from exact original members, fully read, and reconciled at the item scopes recorded here. It should retain the seven proof-bearing families' previously corrected conclusions and the updated three-stage/four-stage chronology. It should not count 70 new theorems, 70 new missing originals, 70 fresh source executions, or a blanket proof audit of every branch named in a manifest.

The separate Frobenius-extension seal remains unchanged. It contains the second mathematical audit and focused novelty comparison for the new affine-alphabet and arbitrary-length mod-two convolution results. This historical coverage closure neither enlarges those theorems nor supplies a new general complex FFT, integer-multiplication, or publication-priority claim.
