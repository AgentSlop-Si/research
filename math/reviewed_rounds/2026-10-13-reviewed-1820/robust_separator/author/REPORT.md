# Robust routed-separator obstruction: duplication verdict and corrected corollary

13 October 2026 UTC. Local research deliverable only. No Sheet or GitHub writes.

## Result

**Reject the proposed bare robust extension as a new result: it is already accepted.** The exact requested squared Frobenius bound and the sharper squared operator bound occur in `FINAL_MATRIX_THEOREMS.md`, Theorem 2B, lines 175–189. `CORE_MATRIX_SECOND_AUDIT.md`, §2, independently checks both bounds. The earlier `F018_ORIGINAL_REVIEW.md`, §8, already proves the Frobenius bound and a weaker operator bound. The historical independent-order theorem also has its own approximation mechanism.

A useful consolidation is the full row-sparse/rank/diagonal correction version below. The inspected accepted correction review proves the required common rectangle and its rank budget; the inspected robust theorem treats the uncorrected and diagonal models. `PREVIOUS_SEPARATOR_COMPARISON.md`, lines 50–52, explicitly says it adds no correction-compatible approximation theorem. We did not locate an identical explicitly stated full correction-compatible robust theorem in the bounded local search. That limited negative finding is not novelty evidence. Substituting the already accepted corrected rank budget into classical low-rank approximation is an immediate corollary, not an independently counted discovery.

**Review status:** the duplicate identification is source-bound. The full corrected corollary, exact recurrence guard and tolerance rearrangements are proved here as candidates and have not yet received independent review of this new packet. Do not label these additions independently accepted or use them for table claims until that review passes. Create no new discovery ID.

The supplied assessment's principal scope conclusions remain intact: this is an additive representation obstruction, not a general FFT lower bound, not a proof about arbitrary products, and not a fast Fourier algorithm.

## 1. Source bindings and duplicate search

The accepted source root is:

`/workspace/scratch/928904ebc9b0/recovery_breadth_1028/extracted/sealed_scientific_packets/research_resume_2251/next_cycle_routed_priority_independent_review/`

Relevant precise locations:

- `candidate/sources/FINAL_MATRIX_THEOREMS.md`, Theorem 2A and its proof, lines 89–173; Theorem 2B, lines 175–189. SHA-256: `6a2a6424d82e313438058a2458cdbc8f555df0fcee6c534cfd7481633d527c6b`.
- `candidate/sources/CORE_MATRIX_SECOND_AUDIT.md`, §2, including the explicit norm bounds and the fixed-error warning.
- `candidate/sources/F018_ORIGINAL_REVIEW.md`, §8, equations (5)–(7); §9 attributes the inherited accuracy mechanism.
- `INDEPENDENT_REVIEW.md`, “Independent selection and correction proof,” lines 54–78. This gives d=s+1+delta, m0=floor(N/d), k=qr+t, and all selection guards. SHA-256: `1796132039a42ad0fa9cf68fba4ebb4c49554f5cbcf7f94d716b9439fb779971`.
- `candidate/sources/PREVIOUS_SEPARATOR_COMPARISON.md`, “Approximation and field variants,” and “Claim dispositions.” The explicit no-new-correction-approximation statement is important.
- `candidate/AUDIT.md`, full corrected contract and bounded primary-source comparison. SHA-256: `55a40e2eb1bfb8f74875d954e1ba400b81e8ded19cb027f106a022697f2ab9ba`.

First-pass local research search covered `.md`, `.tex`, `.txt`, and `.py` under `/workspace/shared` and the task workspace, using Eckart–Young/Mirsky, robust/approximate separator and inverse-sum, and Frobenius-residual terms. Its 123 matching text lines are retained in `LOCAL_DUPLICATE_SEARCH.txt`. A second pass checked correction-compatible approximation and literal `qr+t`/spaced variants, then read the full relevant theorem and review sections. This is a bounded local-text search, not an exhaustive search of compressed archives, attachment binaries, or external literature. No inherited research program was imported or run.

`SOURCE_BINDINGS.json` contains fresh hashes, byte counts and copied local-source paths. The historical current-record stage cap 15 is preserved; no source or live ranking was edited.

## 2. Complete correction-compatible theorem

Let N>=1 and r,q>=1 be integers, s,t>=0 integers, and delta in {0,1}. Let U be an N-square complex unitary with |U_ab|=N^(-1/2). Let

    M = S + K + delta D + sum_(i=1)^r L_i Q_i^(-1) R_i.

Assume:

1. S has at most s nonzero entries in each row. This is a per-row bound.
2. rank(K)<=t and D is diagonal.
3. Every Q_i is invertible. In its undirected symmetric bipartite support lift H_i=[[0,Q_i],[Q_i^T,0]], a separator of at most q vertices exists for every two-color marking invoked below, leaving every component with at most half the total mark weight. Requiring the property for all nonnegative vertex weights is sufficient.
4. Each L_i and R_i has support contained in a permutation matrix. Endpoint permutations are independent across sides and branches; coefficients may be zero. There is no common ordering or graph assumption.

Set

    d = s+1+delta,       k = qr+t,
    m0 = floor(N/d),    m_(j+1) = ceil((m_j-q)/3),
    m = m_r.

Whenever m_j>=4q for every 0<=j<r, the following global bounds hold:

    ||U-M||_F^2 >= max(0,m^2/N-k),                                  (F)
    ||U-M||_F / sqrt(N) >= sqrt(max(0,(m/N)^2-k/N)).                 (NF)

If additionally m>k, then

    ||U-M||_2^2 >= max(0,(m^2/N-k)/(m-k)).                           (O)

Here ||.||_F is the unnormalized Frobenius norm and ||.||_2 is the induced Euclidean operator norm. Since ||U||_F=sqrt(N) and ||U||_2=1, (NF) and (O) are respectively relative Frobenius and absolute/relative operator error bounds for this normalized target. When m<=k, (F) is trivial and the denominator in (O) must not be used.

A closed formula for the specified recurrence is

    a = 3^r,       c = q(a-1)/2,
    m = ceil((floor(N/d)-c)/a).                                    (R)

All recurrence preconditions are equivalent to

    floor(N/d) >= H(q,r),
    H(q,r) = (4q-1)3^(r-1) + q(3^(r-1)-1)/2 + 1.                 (G)

Equivalently, N>=d H(q,r). This guard is independent of t. It states exactly when this particular repeated-selection construction is certified, not when the representation family exists.

### Proof of the selected rectangle

Choose m0 target rows. At most (s+delta)m0=(d-1)m0 columns meet the support of S+delta D in those rows. At least m0 columns remain because N>=d m0. Retain any m0; S+delta D vanishes on that rectangle.

For one branch on a current m_j-square rectangle, mark the corresponding inverse rows red in the lower lift half and inverse columns blue in the upper half. Complete endpoint support patterns to permutations even when coefficients are zero. Thus both colors have exactly m_j distinct vertices and cannot collide with the other color. Delete a size-at-most-q half-separator, then trim each color to u=m_j-q. Every remaining component has at most m_j marks, and m_j>=4q implies m_j<=4u/3.

Partition components into two unions, each with between 2u/3 and 4u/3 retained marks. A component already in this interval can be one union; otherwise greedily accumulate components of size below 2u/3 until that lower endpoint is reached. The complement has the same interval bound. If the first union has a red and b blue marks, one of the oriented cross pairs (a,u-b) and (u-a,b) has both entries at least u/3. Otherwise the failures contradict either a+b in [2u/3,4u/3], or the total of one color being u. Integer counts give ceil(u/3) rows and columns on opposite sides.

For completeness, a support separator X between component unions A and B gives rank H_i[A,A^c]<=|X|: the cross-block is supported only on X columns. For an invertible matrix, complementary off-diagonal cut rank is preserved by inversion. This follows directly from the nullity identity

    rank H^(-1)[I,J] = rank H[J^c,I^c] + |I|+|J|-2N.

Consequently rank H_i^(-1)[A,B]<=q. Since H_i^(-1) has Q_i^(-1) in its lower-left block, the selected branch rectangle has rank at most q. Endpoint scaling and zero masks do not increase rank. Earlier branch bounds survive restriction. After r steps there is one actual m-square target rectangle I x J with

    (S+delta D)[I,J]=0,    rank M[I,J]<=qr+t=k.

No equality U=M was used in its construction, so exactly the same rectangle applies to global approximation. This is the crucial reason the accepted exact proof transports to the robust version.

### Proof of the norm bounds

Let V=U[I,J]. Coordinate restriction is contractive in both Frobenius and operator norm. Unitarity gives ||V||_2<=1, while flatness gives ||V||_F^2=m^2/N. Write its singular values sigma_1>=...>=sigma_m>=0.

Classical best rank-k approximation gives

    ||U-M||_F^2 >= sum_(j>k) sigma_j^2,
    ||U-M||_2 >= sigma_(k+1)      if k<m.

Each sigma_j<=1, so the first k singular values consume at most k squared energy. Therefore the tail has at least max(0,m^2/N-k) energy. The largest of its m-k values has square at least their average. This proves (F), (NF) and (O). It is not valid to divide this improved tail bound by m-k by claiming the actual error matrix has rank m-k; that error may have full rank. The correct argument uses the target singular-value tail.

The nested-ceiling identity ceil((ceil(x)-q)/3)=ceil((x-q)/3), for integer q, proves (R) inductively. Under valid iteration the sequence decreases, so the last required input m_(r-1)>=4q is the controlling guard. Applying the integer identity ceil(y/b)>=4q iff y>(4q-1)b yields (G). The recurrence is monotone and its backward threshold automatically ensures all earlier guards, including for r=1.

## 3. Explicit finite-error size cutoffs

These are convenient conservative rearrangements, not new rank principles. Put

    z = d 3^r,
    C = d q(3^r-1)/2 + d-1,
    B = z^2 k.

The accepted exact cutoff is N<=B+2C. Both tolerance cutoffs below reduce to it at zero error; numerical equality at a displayed cutoff is not excluded.

### Relative Frobenius tolerance

If ||U-M||_F/sqrt(N)<=eta and 0<=eta<1/z, then

    N <= (B+2C)/(1-z^2 eta^2).                                    (CF)

Proof by contradiction: this proposed threshold is at least B+2C, so a violation validates all accepted selection preconditions. Also m>=(N-C)/z>0. Bound (F) would force

    (1-z^2 eta^2)N^2 - (B+2C)N + C^2 <= 0.

For N>(B+2C)/(1-z^2 eta^2) the left side is strictly positive.

### Operator tolerance

If ||U-M||_2<=epsilon and 0<=epsilon<1/sqrt(z), then

    N <= [C(2-z epsilon^2)+B(1-epsilon^2)]/(1-z epsilon^2).         (CO)

Proof by contradiction: the right side minus B+2C is

    epsilon^2 [B(z-1)+Cz]/(1-z epsilon^2) >= 0.

A violation therefore validates selection and ensures m>k. Set x=(N-C)/z. From (O) an approximation would require

    f(m) = m^2 - N epsilon^2 m - Nk(1-epsilon^2) <= 0.

But x>0, and the cutoff violation gives

    z^2 f(x)
      = (1-z epsilon^2)N^2
        - [C(2-z epsilon^2)+B(1-epsilon^2)]N + C^2 > 0.

Because epsilon<1, f has one positive root and is positive to its right. Thus f(x)>0 and m>=x imply f(m)>0, contradiction.

For fixed r,q,s,t,delta, N tending to infinity gives m/N -> 1/z. Hence

    liminf ||U-M||_F/sqrt(N) >= 1/z,
    liminf ||U-M||_2 >= 1/sqrt(z).

These are fixed-branch error floors. At fixed positive tolerance, making r a sufficiently large constant makes these floors smaller than that tolerance. This reasoning does not imply r=Omega(log N) at fixed nonzero tolerance. Nor does its failure establish existence of a matching approximating family.

For unnormalized Fourier F=sqrt(N)U, scale the complete approximant by sqrt(N); the class is closed under this scalar scaling. The squared absolute Frobenius floor is max(0,m^2-Nk), and the squared absolute operator floor is max(0,(m^2-Nk)/(m-k)). Relative norm versions are unchanged.

## 4. Fresh exact controls

`fresh_checks.py` was written for this task and run once successfully. It does not import predecessor research code. `CHECK_RESULTS.json` records:

- 14,523 exact nested-ceiling and selection-guard cases;
- 3,840 exact rational tolerance-cutoff cases, including the proof that cutoff violations inherit every selection guard;
- 5,411 exact rational singular-square/rank-budget cases;
- 71 actual normalized Hadamard square blocks, with exact rational Gram eigenvalues and all rank budgets checked;
- four actual independently routed forest-lift families, with zero endpoint masks, row-sparse/diagonal elimination and low-rank corrections. Their parameters (N,r,q,s,t,delta) are (64,1,1,0,0,0), (256,2,1,0,1,0), (1024,2,1,1,1,0), and (1024,1,1,1,2,1). Each has a strictly positive certified Frobenius floor. The last two explicitly exercise sparse correction and all correction types.

The actual family uses Q=I-superdiagonal, whose inverse has entry 1_(i<=j), with independently randomized left and right endpoint permutations. Its lift is a path, so a weighted centroid supplies q=1. Every selected branch matrix and the corrected sum are checked by exact rational rank, and the actual selected target error is checked exactly. These are legal concrete controls, not an exhaustive test of all separator graphs or all q.

Hypothesis/negative controls document why flatness without unitarity fails (J_4/2 is rank one), why m=k cannot enter the spectral denominator, why unnormalized Fourier needs the factor N, and why average sparsity cannot replace the per-row bound. All arithmetic acceptance is exact; no floating-point test supports the verdict. Finite checks complement the proof, not replace it.

## 5. Primary prior-art comparison

The analytic step is classical best low-rank approximation. A freshly opened primary author manuscript is Chi-Kwong Li and Gilbert Strang, *An elementary proof of Mirsky's low rank approximation theorem*, Theorem 1, pp.1–3: https://cklixx.people.wm.edu/uinorm-note.pdf . It states optimality of truncated SVD for every unitarily invariant norm over real or complex matrices and proves singular-value domination of an error after rank-k subtraction. It explicitly includes operator and Frobenius norms. Its references identify Eckart–Young (1936), Mirsky (1960), and Schmidt (1907). Fresh DOI opens for the 1936 and 1960 originals failed, so this packet does not claim to have newly inspected those original bodies. The full primary manuscript theorem is sufficient for the applied analytic comparison.

The bound here is a direct consequence of that classical theorem plus sigma_j(V)<=1 and known block energy; no general approximation theorem is new. The matrix-specific guarantee is the accepted independently routed common rectangle. The source-bound accepted F018 audit already compares the structural ingredients with GIRS, final TQS, nullity and weighted separators. This pass does not repeat or broaden that completed literature claim. The full S/K correction transport is elementary support deletion and rank subadditivity.

No worldwide novelty probability or external-human-review claim is made. No primary source inspected here turns the common-rectangle rank budget into unrestricted Fourier circuit complexity.

## 6. Priority and remaining gate

Candidate recommendation after independent review: **15/100 for this bounded robust-extension/consolidation stage, COMPLETE.** The author pass is finished; independent review of the new corollary is pending. Keep it attached to F018 rather than create another discovery count. Preserve existing parent scores unless the parent's actual rubric and stage mapping support a change. This is remaining-work priority, not correctness confidence, theorem quality or novelty probability.

Explicit work-triage rubric, each dimension 0–5: information gain 1 (weight 4), tractability 5 (weight 3), scoped usefulness 2 (weight 4), evidence readiness 5 (weight 3), unmet proof need 1 (weight 6). Uncapped work score is 48/100; completed-stage cap is 15. Novelty is not one of these numerical dimensions. Novelty disposition separately: bare theorem is an exact accepted duplicate; full corrected statement and tolerance rearrangements are immediate corollaries, not supported independent novelties.

The remaining substantive robustness gate is a stronger uniform argument, such as certified simultaneous spectral energy or nonoverlapping/controlled-overlap rectangle accumulation, that could constrain branch count as N grows at a fixed positive error tolerance; or a model-legal construction clarifying sharpness of the existing floors. Neither follows from this one-rectangle Eckart–Young argument. Existing historical-priority/publication and sharpness questions also remain. No such new frontier is proved or started by this packet, and the completed F018 comparison is not reopened.
