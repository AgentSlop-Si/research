# Two exact-scope comparison gates: inverse neighborhoods and Weyl certification

Date: 16 October 2026. Repository source pin: `07455df33fd8243bc0e7facb92af6c6a5830ae2a`.
Disposition: candidate for independent review; local report and cell proposal only. No external writes.

## Results first

- **M-SPARSE-DEFECT, overview row 98:** the remaining *one-neighborhood attainment and zero-singular-value boundary comparison* is now resolved at a bounded source-specific level. Lang's Lemma 3.3 already contains the truncated-block/invertibility mechanism, beyond the previously compared lower-bound passages. A direct all-unitary specialization explains the accepted attaining construction. The positive-rank extension and unattained boundary are spelled out below as deductions, not quoted prior theorems. Li–Lim's generalized matrix-nearness problem is a qualified nonmatch for the complete spectral-norm/invertibility contract.
- **M-WEYL-TWIRL, overview row 108:** the all-dimension twirl identity is an exact specialization of Werner's unitary-depolarizer theorem. The four-phase moment identity is an exact discrete specialization of Iitaka–Ebisuzaki's complex trace-estimator variance formula. The candidate-call and preparation costs are separately mapped.
- Subject to independent acceptance, these complete the two named comparisons. **M-WEYL-TWIRL is closure-eligible at its owned fixed-linear all-N certification/comparison scope; M-SPARSE-DEFECT remains TO RESEARCH. Both retain priority 42.** The former record’s uniform-construction/training limitations are excluded consequences, not outstanding lemmas of this certificate. Q10, F081 and synthesis siblings are not closed. Global uniform row-sparsity sharpness remains an explicit M-SPARSE-DEFECT successor; worldwide priority and production are not certified.

## Owner contract and provenance

Live source workbook: [Research overview](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011).
Read full rows: overview 98 and 108; Catalogue 47–48; `novelity breakthough` 81 and 91.

Both recorded stops are:

> Identify a primary theorem and give an exact hypothesis, formula and cost-model mapping, or record a qualified nonmatch or specific access blocker. Preserve the stated guards; no worldwide-priority, unrestricted runtime or production conclusion.

The complete owner rows and every repository proof used are retained alongside this report. The recovered index was used for selection; full owner histories control the scope. The already-completed Lang nullity/lower-bound comparison is not counted again. Neither an easier substitute task nor a new generic survey is proposed.

## 1. M-SPARSE-DEFECT: complete one-neighborhood boundary

### Accepted mathematical target

For a complex (N\times N) unitary (U), sets (I,J), (t=|I|>0), (m=|J|), and integer (0\le r<t), put (d=t-r). The constrained class is

(\mathcal C=\{M\text{ invertible}:\operatorname{rank}(M^{-1}[I,J^c])\le r\}.)

The accepted source states:
- (d>m): the class is empty.
- (1\le d\le m): the distance infimum is (\beta=\sqrt{1-\sigma_d(U[J,I])^2}).
- The infimum is attained exactly when (\sigma_d>0).
- If (\sigma_d=0), every feasible invertible matrix has error strictly greater than one, although the infimum is one.
- If (r\ge t), the constraint is automatic and (U) attains zero.

These are single-allowed-neighborhood assertions, with all other entries unrestricted. They are not sharp global row-sparsity or exact-support-union theorems. The source's inverse-row, sparse-column and common-frame commutator floors remain accepted separately.

### What the additional primary passages establish

[Lang, *The Inverse of a Nearly-banded Matrix*, arXiv:0812.0172v1](https://arxiv.org/pdf/0812.0172v1), Lemma 3.3, printed p.2, replaces an inverse block (C) by a truncated-SVD block (L), leaves the other blocks fixed, and obtains an invertible matrix with a zero complementary inverse block. The proof uses (\|L-C\|<1/\|K\|), with sufficiently small original perturbation as its sufficient hypothesis. This is a genuine antecedent for the attaining construction, beyond Theorem 2.1/equation (3.2), which were already compared. Section 5 explicitly separates positive-rank approximate-nullity questions; its singular-value-ratio question is not solved or claimed here.

[Li–Strang, *An elementary proof of Mirsky's low rank approximation theorem*](https://cklixx.people.wm.edu/uinorm-note.pdf), Theorem 1, printed p.1, supplies the complex rectangular truncated-SVD minimizer for every unitarily invariant norm, including spectral norm. Its statement is an ordinary rank-constrained approximation theorem. It does not itself assert the full invertible inverse-pattern class or its boundary. Publication identity: Electronic Journal of Linear Algebra 36 (2020), [journal record](https://journals.uwyo.edu/index.php/ela/article/view/5551), DOI 10.13001/ela.2020.5551.

### Exact mapping, including the remaining boundary

Write (A=U[J,I]), (C=U[J,I^c]), (k=m-d=m-t+r). Complementary inverse nullity gives, for every invertible (M),

(\operatorname{rank}(M^{-1}[I,J^c])=\operatorname{rank}(M[J,I^c])+t-m.)

Thus the actual constraint is equivalent to (\operatorname{rank}(M[J,I^c])\le k). The prior lower-bound argument is retained only as context: compression plus best rank-(k) approximation gives error at least (\sigma_{k+1}(C)=\beta), since (AA^*+CC^*=I_m).

To map the **attainment**, take a best rank-(k) truncation (L) of (C), and replace only the (J\times I^c) block of (U) by (L). Call the full matrix (M_0). Then
(\|M_0-U\|_2=\|L-C\|_2=\beta).
When (\sigma_d(A)>0), (\beta<1), so (U^*M_0=I+U^*(M_0-U)) is invertible. Nullity gives the required inverse-block rank. This reaches the lower bound.

Choose (Q) as the leading (d) left singular vectors of (A), embedded on (J). They are the bottom (d) left singular directions of (C), with zero-padding. Then
(L=C-Q_JQ_J^*C), hence
(M_0=U-QQ^*UP_{I^c}),
which is **the accepted source's attaining matrix**, not a different surrogate.

For (r=0), Lang's dimension identification is (n=t), (p=m-t\ge0), (K=U^{-1}) after independent row/column reorderings, and its inverse block is our (C). Its literal small-perturbation hypothesis need not hold for every unitary input. The displayed proof mechanism does hold whenever (\beta<1=1/\|U^{-1}\|_2). For (r>0), use (k=m-t+r) in the same truncation and the nullity identity. This is an explicit deduction using the stated rank theorem, not a claim that Lang printed the general (r) theorem.

For the **zero-critical endpoint**, any feasible (M) has a subspace
(W=\{h:\operatorname{supp}h\subset J,\;\operatorname{supp}(M^*h)\subset I\})
of dimension at least (d). If (\operatorname{rank}(A)<d), (W) contains a unit (h) with (P_IU^*h=0). The vectors (U^*h) and (M^*h\ne0) have disjoint coordinate supports. Therefore
(\|(M-U)^*h\|^2=1+\|M^*h\|^2>1).
No invertible minimizer exists. Choose a permutation (H) matching at least (d) rows of (I) into distinct columns of (J). Then (M_\delta=\delta H^{-1}) is feasible and (\|M_\delta-U\|_2\to1). This also proves feasibility when (d\le m). Empty and automatic branches remain as above.

The exact invertible endpoint statement was not found as a literal theorem in the inspected primary passages. The positive attaining mechanism is directly classical; the boundary follows by the displayed elementary argument. This neither establishes new priority nor makes a negative literature claim.

### Distinct near-match and its precise failure

[Li–Lim, *Generalized Matrix Nearness Problems*, SIAM J. Matrix Anal. Appl. 44 (2023), 1709–1730](https://www.stat.uchicago.edu/~lekheng/work/near.pdf), Section 2.1 and Algorithm 1, pp.1710–1711, solves a generalized rank-constrained (\|A-BXC\|_F) problem. This is **not the complete target**: it uses Frobenius norm, constrains the whole variable (X), and does not impose invertibility of our completed full matrix. Its free-block/minimum-norm choices cannot certify that condition. Even if a selected-block calculation agrees, its theorem does not license importing the spectral-norm distance or unattained invertible boundary. This is the bounded qualified nonmatch required by the owner gate.

### Cost and retained obligations

This is a matrix-nearness formula and source attribution, not an efficient Fourier evaluator. SVD/subspace acquisition, input access, full completion, inversion if explicitly requested, coefficient storage and readout remain paid. No scalar-work, bit, stability or physical runtime improvement is inferred. The accepted global row-sparse-plus-low-rank lower bound is unchanged and its general sharpness remains open. Common-frame commutator hypotheses, complex unitarity, Fourier flatness only where used, and sparse-column (1\le s<N) guards are preserved.

## 2. M-WEYL-TWIRL: primary match and full cost boundary

### Exact twirl mapping

Use negative-exponent unitary Fourier (U), cyclic shift (S), (D=\operatorname{diag}(\omega^j)), (W=D^aS^b), and (\Phi(W)=S^{-a}D^b=UWU^*). For fixed (M), let (X=U^*M). Then
(MW-\Phi(W)M=U[X,W]).

[Werner, *All Teleportation and Dense Coding Schemes*, arXiv:quant-ph/0003070v1](https://arxiv.org/pdf/quant-ph/0003070v1), Theorem 1 items 4–5, equations (5)–(6), printed p.5, maps an orthogonal basis of (N^2) unitaries to a depolarizer. The Weyl operators satisfy its trace orthogonality at every (N), including composite (N). Dividing equation (6) by (N^2) gives
(\mathbb E_W W^*XW=(\operatorname{tr}X/N)I).
Expanding the commutator square therefore gives precisely
(\tfrac12\mathbb E_W\|MW-\Phi(W)M\|_F^2=\|M\|_F^2-|\operatorname{tr}(U^*M)|^2/N=\min_\lambda\|M-\lambda U\|_F^2).
This is a direct mechanism match, with the displayed scalar calibration still needed. Werner's theorem does not supply a Green constructor, training convergence or candidate runtime.

### Exact discrete-moment mapping

[Iitaka–Ebisuzaki, *Random phase vector for calculating the trace of a large matrix*, arXiv:cond-mat/0401202v2](https://arxiv.org/pdf/cond-mat/0401202v2), equations (13), (16), (18), (22), printed p.2, gives the complex random-vector trace mean and variance, with the random-phase case minimizing the diagonal contribution. For independent coordinates uniform on ({1,-1,i,-i}), (\mathbb Ez=\mathbb Ez^2=0) and (|z|=1); the independence and fourth moments needed for equation (16) hold exactly. With Hermitian (H=A^*A), this gives
(\mathbb E(z^*Hz)^2=(\operatorname{tr}H)^2+\operatorname{tr}(H^2)-\sum_iH_{ii}^2).
Thus the accepted discrete identity is a specialization of the general moment calculation. The source's continuous phase example is not misreported as an explicit four-point algorithm.

Here (A=MW-\Phi(W)M), (Z=\|Az\|^2/2), and (\tau^2=\min_\lambda\|M-\lambda U\|_F^2). The retained source argument bounds (\|A\|_F\le2\tau), so (\mathbb EZ=\tau^2) and (\mathbb EZ^2\le8\tau^4). Consequently its conservative median-of-means parameters remain valid. This comparison changes no constants and claims no optimality of the constant 8.

### Cost, hypotheses and non-implications

Each independent sample uses two applications of the same fixed linear candidate, plus a shift, phases, vector arithmetic and a norm accumulation. Generating powers, acquiring/validating roots, random bits, indexing and storage are not free. The arithmetic count is (2T_M(N)+O(N)) per sample after separately declared root/phase preparation; for (epsilon,\delta) the source uses (O(\epsilon^{-2}\log(1/\delta))) samples. Linear work for constant accuracy/confidence is conditional on an actual linear-work candidate and the declared arithmetic/sampling model. No finite-word/stability guarantee is imported from the papers.

The scalar seed remains necessary; a small sampled loss is not exact equality. A candidate selected adaptively from the same probes needs fresh held-out validation or a separate uniform/adaptive theorem. The source's fixed-coordinate cut calculus, N=12 uncharged half-swap counterexample, transported-cut correction and (N=2m), odd-(m) parity condition remain intact. None of the two primary papers repairs a free shuffle or proves a Green realization, bounded training iterations, uniform synthesis or production acceptance. Their exact matches settle this named comparison, not the priority of the combined project package.

## Proposal and verification boundary

`NATIVE_CELL_PROPOSAL.json` contains 19 local-only edits: 12 next-action/pass-stop cells across the two overview rows and their owner mirrors; four previously stale current-comparison/assessment summaries in the novelty tab; overview F98 and F108 scope summaries; and E108 changing the owned M-WEYL-TWIRL record to CLOSED. It records exact live preimages. Application must preserve historical text and recheck each preimage after independent review. No priority, accepted proof, formula, format, sibling status or unrelated cell changes. M-SPARSE-DEFECT E98 remains TO RESEARCH.

`SOURCE_LOCATORS.json` identifies the five repository bodies and five primary sources; the original repository texts are hashed. Web-rendered primary passages were inspected, including formula context and PDF page locations. No downloaded PDF byte hash or final-edition equivalence is asserted where none was obtained. In particular, the four-phase paper's version identifier is v2 (2004), not its regenerated HTML date.

No supplied research program was executed, imported, compiled or AST-parsed. No solver, install or network-bypass route was used. The source-bound deductions above, rather than a finite sample census, support the comparison. No GitHub or workbook mutation occurred.

