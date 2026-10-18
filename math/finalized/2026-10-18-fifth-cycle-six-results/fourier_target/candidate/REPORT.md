# Original unrestricted F8 target: exact residual ideal and a zero-safe inverse reduction

18 October 2026. Owner M-NONLINEAR-COMPATIBILITY, priority 34. Task 6 of the selected finalization gates. No external write was made.

## Outcome

**The original target is not decided by this packet.** No exact witness, no characteristic-zero unit-ideal certificate, and no Fourier-excluding polynomial was obtained. Keep the owner TO RESEARCH. Numerical residuals and tangent experiments below are not nonexistence evidence.

The deliverable is a fully specified, machine-readable original ideal, a substantially simpler necessary inverse system that retains every original zero component, a complete zero-safe test for lifting a candidate back to the original chart, and fresh exact checks of the encodings. The unresolved task is exact characteristic-zero elimination, rather than an unspecified choice of another inverse-sparse family.

## 1. Bound source and original equations

The controlling original report is:

https://github.com/AgentSlop-Si/research/blob/511689fb34ffa88921b3d2a0dc801e048b49dce2/math/finalized/2026-10-17-resumed-mathematics-0916/reports/fourier_target/REPORT.md

Git blob 8fbc4b60b9591405464b1153698a35f90ce36674. Its retained text is `sources/ACCEPTED_INVERSE_SUPPORT.md`. The earlier actual-chart discussion and the latest accepted restriction frontier are also retained in `sources/`. These existing bodies were read as mathematical source, not imported as programs.

For S=A or B, the original forty displayed variables give

S[i,i]=d_S[i], S[i,j]=l_S[i]m_S[j] for i>j, and S[i,j]=u_S[i]v_S[j] for i<j.

The permutation is p=(7,0,6,3,4,1,2,5), with P e_j=e_p(j). Its inverse is (1,5,6,3,4,7,2,0). Work over K=Q[z]/(z^4+1). Let F[i,j]=z^(ij). The exact equations are

f[i,j] = sum(k=0,...,7) B[i,p(k)] A[k,j] - z^(ij), for all 64 pairs (i,j).

`ORIGINAL_IDEAL.json` contains every term of every equation, the full 80-variable list, coefficient vectors in the ordered basis (1,z,z^2,z^3), and the precise permutation convention. `ORIGINAL_IDEAL.sing` gives the same system over the algebraic coefficient field for a characteristic-zero elimination engine.

The only variables removed from that executable ring are l_A[0], m_A[7], u_A[7], v_A[0] and the four analogous B endpoints. They occur in no entry. Removing these eight unobservable variables is a polynomial-ring extension/retraction, so it cannot remove any solution or change whether the ideal is the unit ideal. There are 72 observable variables, 64 equations, and maximum total degree four. No generator was normalized or required nonzero.

The exact check gives det(F)=4096 z^2. Thus A and B are automatically invertible in every solution. Saturating the original ideal by determinants is unnecessary. The field is characteristic zero: z^4+1 is irreducible because its translate (x+1)^4+1 is Eisenstein at 2. The checks verify z^4=-1, z^8=1, and the Fourier inverse entrywise.

Properness of the original ideal means a solution over the algebraic closure of K; it need not mean a solution with all coefficients already in K. An algebraic witness would require its field description and all 64 entry checks.

## 2. A necessary system with no inverse-sparsity assumption

For an 8 by 8 matrix X, let L(X) consist of all two by two minors whose entries are wholly strictly below or wholly strictly above the diagonal. There are 70 below and 70 above:

X[r,a]X[s,b]-X[r,b]X[s,a], where r<s, a<b, and either b<r or s<a.

These 140 equations are equivalent to requiring rank at most one for every strict lower or upper cut block. They permit zero blocks and all zero entries. Every original separated-generator stage satisfies them, though their zero boundary is larger than the original chart.

### Inverse lemma, including singular principal blocks

For any invertible X and any coordinate cut E plus its complementary coordinate subspace H,

rank((X^-1)[E,H]) = rank(X[E,H]).

Indeed, each rank is dim(H) minus the dimension of the corresponding intersection: the right side uses XH intersect H, and the left uses X^-1 H intersect H. The invertible map X identifies these two intersections. Apply the same argument with E and H exchanged for the other orientation. This does not assume either principal block is invertible.

Consequently L(X)=0 if and only if L(X^-1)=0, for invertible X. This includes every degenerate generator choice of the original stage chart.

### The residual inverse ideal

Put C=A^-1. The original equation forces B=F C P^-1. Define

J = < L(C), L(F C P^-1), t det(C)-1 > in K[c[0,0],...,c[7,7],t].

This is a precisely specified 65-variable ideal with 280 quadrics plus one degree-nine invertibility equation. `RELAXED_QUADRICS.json` contains every quadratic term; `RELAXED_IDEAL.sing` contains the complete ideal including the determinant equation. Entries use B[i,p(j)]=(FC)[i,j], so no inverse-permutation ambiguity remains.

Every solution of the full original 80-parameter ideal gives a solution of J. Therefore an exact identity 1 in J would establish the requested unrestricted impossibility. No inverse sparsity, diagonal-plus-rank bound, nonzero generator, or invertible principal block is imposed.

The converse is not automatic. A proper J may have only boundary points that do not lift to the original chart. Section 3 gives the exact lifting test. Proving J proper would therefore not alone decide the target. This distinction is essential.

## 3. Complete zero-safe lifting test

Suppose a matrix T satisfies the 140 ladder minors. Consider its lower triangle. Let R be the row indices with at least one nonzero lower entry, and S the column indices with at least one nonzero lower entry.

If R and S are empty, choose both lower generators zero. Otherwise set r*=max R and s*=min S. A separated lower factorization exists exactly when every permitted edge (i,j), i in R, j in S, i>j, is nonzero. Equivalently, its support must be the intersection of the lower triangle with the Cartesian product of its active row and column sets.

Necessity follows from T[i,j]=l[i]m[j]. For sufficiency the pivot T[r*,s*] is nonzero. Set

l[i]=T[i,s*] for i in R, and zero outside R;
m[j]=T[r*,j]/T[r*,s*] for j in S, and zero outside S.

For any active permitted edge, the relevant ladder minor gives T[i,j]=l[i]m[j]. The pivot row and column obey the same identity directly. All remaining entries are zero. This proves sufficiency without assuming a generic support. Apply this argument to T transpose for the upper triangle, and retain its diagonal entries freely.

The checker implements this canonical lifting algorithm and directly verifies the resulting products, rather than trusting a support test alone. Thus an algebraic solution C of J can be accepted as an original target witness exactly when both C^-1 and F C P^-1 pass this test; the recovered generators must then be substituted into all 64 original equations.

### Why simply parameterizing C as another original stage is unsound

Take A[i,j]=1 for i>=j and zero otherwise. A is an original stage and det(A)=1. Its inverse C has ones on the diagonal, minus ones on the first subdiagonal, and zeros elsewhere. It satisfies all ladder minors but is not an original separated-generator stage: C[1,0] and C[2,1] are nonzero while C[2,0]=0. The first two entries would force l[2]m[0] nonzero.

This is an actual invertible original-stage inverse on the excluded zero boundary. Hence a replacement of C by generic nonzero inverse generators would discard legitimate original possibilities. The necessary ideal J and the unnormalized original ideal do not discard them.

For scale, one triangular support has 7,280 distinct active-support patterns including the zero pattern. The naive Cartesian product of four triangles has 2,808,830,402,560,000 patterns, before exploiting equations or symmetries. This is only a warning against a naive exhaustive support split, not a claim that all those patterns are feasible for F or must be enumerated. The original polynomial ideal encodes them jointly.

## 4. Fresh checks and discovery outcome

`build_exact_systems.py` and `verify_exact.py` are freshly written standard-library programs. No historical executable or downloaded research package was run. The exact checker verifies:

- The root identities, both 64-entry Fourier inverse identities, and det(F)=4096 z^2.
- The original permutation, all 64 target equations, and exactly eight unobservable endpoints.
- 192 evaluations of original equations against separately constructed matrix products.
- 560 evaluations of the emitted inverse-system quadrics against direct minors of C and F C P^-1.
- 560 inverse-ladder identities on fresh invertible integer-stage examples, alongside both inverse identities.
- Canonical generator recovery on stages with zero entries, invertible diagonal controls, and the non-liftable bidiagonal inverse boundary.

The general inverse and lifting claims come from the proofs above; finite checks validate their transcription. These are independently implemented checks within this packet, not a separately commissioned independent mathematical review.

A deterministic numerical discovery run used twelve complex initializations in a 60-complex-parameter normalized dense chart. None produced a candidate to exactify; the smallest Frobenius residual was about 0.6601447747. This chart excludes zero cases, the optimization is nonconvex, and coefficients may escape to infinity. The result proves neither absence of an exact point nor exclusion from the image closure. Its source, seeds, settings, parameter arrays, and logs are retained solely as discovery provenance.

The tangent `matroid_probe.py` output is exploratory and unused in every proof or claimed exclusion. It does not supply a Fourier vanishing polynomial.

## 5. Precise remaining resource/interface

The complete original ideal was submitted to SymPy 1.14.0's characteristic-zero F5B implementation over QQ in the 72 observable variables plus z, adjoining z^4+1. This is exactly equivalent to the coefficient-field system, not a modular specialization. `EXACT_ELIMINATION.log`, `EXACT_ELIMINATION.stderr`, and `ELIMINATION_STATUS.json` record the bounded attempt, resource settings, and outcome. The run terminated at its 180 CPU-second soft limit with SIGXCPU (exit 152), before returning a basis. Its address-space ceiling was 1 GiB; no memory-exhaustion event was observed. This is a concrete limit of this recorded computation, not a lower bound on resources needed by every method.

The unresolved original residual remains all of I_F, with no zero component certified empty. The alternative sufficient residual is J from Section 2; it has not been eliminated. The requested next resource is a proof-producing characteristic-zero elimination computation or a new structural argument for one of these two explicit ideals. A favorable finite-field calculation alone cannot certify a unit ideal in characteristic zero. A solver's bare report of a unit basis would also need an independently checkable lifted identity in the stated generators.

Acceptable completion interfaces are:

1. Exact algebraic original generators, their field and invertibility certificates, and all 64 verified entries; or
2. An exact identity 1=sum h[i,j] f[i,j] over K for the original ideal; or
3. An exact identity 1=sum q_k J_k for the full inverse relaxation, which implies original infeasibility; or
4. A separately proved polynomial vanishing on the original image whose value at F is nonzero.

No finite degree, additional inverse restriction, owner closure, or automatic larger numerical benchmark is proposed. Existing restricted-family obstructions remain valid pruning lemmas only.
