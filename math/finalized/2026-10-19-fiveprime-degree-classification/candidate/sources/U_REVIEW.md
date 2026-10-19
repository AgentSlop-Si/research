# Independent audit of the order-5q upper interior interval

Date: 2026-10-19 UTC. This is a local, independent symbolic proof audit and exact control packet. The target is the original binary entry mask of a fixed Fourier matrix, with prime q>5 and only 3q<d<4q. Verdict: PASS for the frozen candidate packet whose MANIFEST.json SHA-256 is 07099cb8e9a7feb83c206e4d74a9c382bfed04ef0dd3389c75fd0942235cee27. All 19 bound files and five original source copies were verified. No proof repair is required.

## Accepted narrow statement

For N=5q, a primitive Nth root zeta, and an arbitrary binary N-by-N array R, put D[r,c]=R[r,c] zeta^(rc) in the actual original indices. No such D has either square Gram equal to dI when 3q<d<4q. Equivalently, a mask of the normalized fixed Fourier matrix cannot have either Gram (d/N)I in this interval.

The quantification is over arbitrary binary masks. The row support structure used below is derived, rather than assumed. No endpoint, whole order-5q classification, general semiprime classification, block-support classification, novelty, or Fourier-algorithm assertion is reviewed or made here.

## Symbolic dependency audit

1. A square identity D*D=dI with d>0 implies invertibility and DD*=dI; the converse is identical. The two diagonal identities force every row and every column to have degree d. Both directions of regularity are genuinely available and are needed below.

2. Let e5=q(q^(-1) mod 5) and eq=5(5^(-1) mod q), taken modulo 5q. These satisfy e5+eq=1, e5 eq=0, and e5^2=e5, eq^2=eq. Consequently r=a e5+b eq and c=u e5+v eq give rc=au e5+bv eq in the original cyclic ring. Thus the Fourier phase is exactly alpha^(au) beta^(bv), with alpha=zeta^e5 of order 5 and beta=zeta^eq of order q. There is no arbitrary replacement of the row-column pairing by an unrelated tensor model.

3. For two rows in the same a group, orthogonality has prime-q character. Their overlap counts in each five-point fiber v must therefore be equal. For two rows with both coordinates different, their difference character has order 5q. The exact binary cancellation alternative follows from the rational basis alpha^i beta^j, 0<=i<4, 0<=j<q-1. This basis spans and has the cyclotomic field's degree 4(q-1), so it is independent. A vanishing binary array has

       epsilon[i,j]-epsilon[i,q-1]-epsilon[4,j]+epsilon[4,q-1]=0.

   Hence epsilon[u,v]=A[u]+B[v] for integer A,B. If both vary, their Cartesian sum has range at least two, impossible for binary values. Thus the overlap is a union of full five-point fibers or a union of full q-point lines. The coordinate multipliers introduced by a primitive character only permute these two parallel families. The empty set is allowed. This is a binary-only cancellation lemma; no weighted or unrestricted descent is assumed.

4. Fix a supported position of row r=(a,b). Exactly q+4 rows, including r, agree with r in at least one CRT coordinate. Since column degree d>=3q+1>q+4, another supporting row differs from r in both coordinates. Its overlap with r is a primitive zero sum, so it contains a full line or fiber through the chosen position. Applying this to every position proves that each row support is a union of full cycles. Define A_r to be all full q-lines and B_r to be all full five-fibers in that row. Then

       S_r=(A_r x Z/q) union (Z/5 x B_r),
       d=ell_r q+(5-ell_r) f_r,
       ell_r=|A_r|<=3, f_r=|B_r|.

   This is canonical: all full cycles are counted. It allows mixed values of ell_r and f_r at this stage. If f_r were zero, coverage would give d=ell_r q<=3q, so every B_r is nonempty.

5. Distinct rows in one a group have disjoint B sets. A shared full fiber would make the balanced overlap count equal to five on every fiber, giving total overlap 5q, impossible because each row has degree less than 4q. There are q rows and q possible fibers. Their nonempty, pairwise disjoint B sets must therefore all be singletons and must partition the fiber set. This derives the permutations f_a without any initial uniformity assumption.

6. Only now may the degree equation become d=5+ell_r(q-1). For ell_r=0,1,2, its values are 5, q+4, and 2q+3, all less than 3q for q>5. Hence every row has ell_r=3 and the only remaining degree is d=3q+2, which is strictly inside the target interval. For distinct same-group rows, the two special fibers differ. Their overlap has three points on either special fiber and |A_r intersect A_s| on all other fibers. Since q>2 there is another fiber. Prime balance forces |A_r intersect A_s|=3, so their triples coincide. Thus a group-wide triple A_a is derived.

7. For a column (u,v), let h_u count groups a whose triple contains u. Those groups each contribute q rows, and each other group contributes one because f_a is a permutation. Column regularity therefore gives

       5+h_u(q-1)=3q+2,

   or h_u=3 for every u. The five triples cannot all coincide: that would give incidence counts five on the common triple and zero elsewhere. Hence two groups have different triples. For distinct three-element subsets of a five-element set, their intersection has size h=1 or h=2.

8. Fix any row in one of those two groups. In the other group, exclude its one possible same-b row and the unique row with the same special fiber. At most two rows are excluded; q>=7 leaves at least q-2>=5 eligible rows. Any selected row has a primitive difference character and a different special fiber. The overlap has three points on both special fibers and h<=2 points on every other fiber. It cannot be a union of full five-fibers because the two nonempty special fibers have cardinality three. It cannot be a union of full q-lines because its fiber cardinalities are nonconstant. This contradicts primitive cancellation and excludes the only residual degree.

9. The q=7 boundary is covered directly. The interval degrees are 22 through 27, and even the smallest exceeds q+4=11. The singleton equation leaves d=23. At least five partner rows remain after the exclusions, and five other fibers provide the cardinality mismatch. No exceptional first-interior q=7 theorem or geometry is needed.

10. Strict endpoints matter. The reasoning uses d>3q to ensure a nonempty B set and d<4q to bound ell_r by three. The result neither includes nor decides d=3q or d=4q. Coprimality of 5 and q and primality of q are also explicit hypotheses, and q=5 is not silently included.

These steps form a symbolic proof for every prime q>5. The finite checks below are corroboration, not the basis of acceptance.

## Independently authored exact controls

The fresh standard-library program independent_check.py constructs Phi_(5q)(X) by exact division of Phi_5(X^q) by Phi_5(X). It computes every character sum in actual original cyclic indices by integer polynomial remainder. It imports no candidate or historical verification program and uses no floating tolerances.

At q=7,11,13 it checks 8,475 actual CRT phase products. It examines every ordered pair of baseline triples and every ordered pair of singleton fiber locations; every primitive character is used for q=7 and q=11, and character 1 is used for q=13. Across 618,500 overlap checks, vanishing occurs exactly when the triples agree and the fibers differ. This includes every distinct-triple/distinct-fiber shape required by the contradiction.

The checker preserves every mixed (ell,f) count solving the pre-singleton degree equation in each interval. It confirms the coverage margins and that singleton fibers leave only ell=3, d=3q+2. It separately checks 41,732 partner selections using arbitrary target fibers and affine bijections, corroborating the general at-most-two-exclusions argument.

Full-square negative masks use A_a={a,a+1,a+2} modulo 5 and the genuinely group-dependent maps f_a(b)=(a+1)b+2a modulo q. All row and column degrees are 3q+2 and all same-a row-Gram entries vanish, but both complete Grams fail. Exact primitive original-index witnesses are retained. The negative controls account for 16,950 complete Gram entries. Positive monomial, q-line, five-fiber, and full masks verify both Grams at degrees 1,q,5,5q, totaling another 67,800 entries. These do not claim constructions at the excluded interval's endpoints.

The run completed with PASS and empty stderr. All output counts are recorded in RUN.stdout; detailed coefficients, witnesses, degree reductions, and counts are in RESULTS.json.

## Frozen-packet integrity and rerun

The candidate manifest binds 19 files totaling 131,877 bytes, all of which match their recorded SHA-256 values. Its seal matches the manifest hash. All five source copies are byte-identical to their original local sources. The frozen REPORT.md hash is c4bacdf2b20eb12c16602aba08e14b04bdd65e9c0f1cce427c7df2c58aceb664.

After inspecting the author's fresh checker, the reviewer copied the entire candidate packet into a separate candidate_rerun directory and reran it. The run exited successfully with empty stderr. All 19 bound files, including regenerated controls, result summary, and stdout, remained byte-identical to the frozen originals. In particular its 188,400 full Gram entries and 601,600 primitive overlap checks reproduced exactly. This rerun is separate from the independently authored polynomial-remainder checks.

## Scope and final verdict

PASS for the stated open-interval exclusion in the original arbitrary binary fixed-phase model. The audit is symbolic and dependency-by-dependency; it is not an inference from the finite tests. No endpoint, full classification, general block geometry, novelty, sharp defect optimum, or Fourier/FFT improvement is asserted. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No external write, score change, or owner closure was made.
