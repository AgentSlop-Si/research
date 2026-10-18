# Independent final review: complementary Fourier masks

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**.

## Verdict

**ACCEPT all four stated results at their exact scopes. No mathematical correction is required.**

1. The complementary Fourier-mask criterion is necessary and sufficient for equality of the simultaneous inverse-row-sparsity infimum with the inherited floor. It characterizes every floor-attaining minimizer.
2. For each positive proper divisor d of N, Delta(N,N-d)=sqrt(d/N), with the displayed attained witness. In particular, the budget s=N-1 is solved for every N≥2.
3. At s=N-2, the floor is attained for even N and the infimum is strictly larger for odd N≥3.
4. For prime p, floor sharpness occurs exactly at s=p-1. Every other nontrivial budget has a strict infimum gap.

Retain parent status **TO RESEARCH**, priority **42**. Exact values in the new nonsharp slices, quantitative gap bounds, and the remaining composite-dimensional classification are not resolved. The prior accepted half-density, singleton, and exact N=3 results remain intact.

## Candidate and evidence binding

This decision concerns the final bytes inspected in `../candidate`:

- REPORT.md SHA-256: `1fcfed20e788dbc9bc1085b8eab8fcd92564888d21f429db8c044ee7569d10ee`
- MANIFEST.json SHA-256: `af33ccd9209cb61a4fa87f689304330932f9ea23c9ec3af51ae3324e5177f04f`
- Candidate checker SHA-256: `525c9f18e4d61e578c16c3af7dddcb5194fcb1506ecf065b4da1588dfed38745`
- Pinned repository commit: `c3a882a7e6e61af05fe1045145bc1a43038d77c6`
- Independently recomputed Phase20 source Git blob: `28212b19e78502ce5acf52a90570d42b0285d3d0`

All 14 candidate manifest members matched their declared sizes and SHA-256 hashes before and after the fresh controls. The candidate seal matched the report, manifest, and checker. All six bound source copies matched both their original local files and the declared hashes. These include the prior accepted review `../candidate/sources/ACCEPTED_REVIEW.md`, whose SHA-256 is `cdee425a609892f0c220de1ed4174ff96164534c766091745f298f0584495997`.

The candidate manifest is copied here as `CANDIDATE_MANIFEST.json`. This review does not endorse later changed bytes without renewed review.

## 1. Model and lower bound

The model is exactly the complex normalized Fourier matrix F with entries N^(-1/2) omega^(jk), omega=exp(-2 pi i/N), the spectral/operator 2-norm, invertible M, and a bound of s on the number of nonzeros in **every row of M^(-1)**. There is no restriction on the support pattern, complex coefficients, condition number, or sparsity of M itself. Assume N≥2 and 1≤s≤N-1 throughout.

The inherited one-row bound applies to this smaller simultaneous admissible class. For row b_i of B=M^(-1), write t_i for its actual support cardinality and x_i=||b_i||>0. Unitarity of F, b_i M=e_i, and flat Fourier entries give

    ||M-F||² ≥ (1/x_i - sqrt(t_i/N))² + 1 - t_i/N ≥ 1 - s/N.

This is the Phase20 floor, correctly credited as inherited. Set q=s/N and a=sqrt(1-q). The relevant strictness fact is a<1, which relies on s≥1.

## 2. Necessity, including all coefficient rigidity

Suppose ||M-F||=a and put E=M-F. Equality in the preceding chain is forced for each row separately. It gives t_i=s, x_i=q^(-1/2), and equality with positive real phase in the estimate Re((b_i F)_i)≤sqrt(q)x_i. If S_i is the support of b_i, Cauchy–Schwarz rigidity consequently yields

    (b_i)_j = q^(-1) conjugate(F[j,i]) 1_{j in S_i}.

Thus there is no remaining complex amplitude or phase freedom once the row support has been fixed. Let A[j,i]=F[j,i]1_{j in S_i}; each column of A has s nonzeros, and B=q^(-1)A*.

The simultaneous hypothesis now supplies an essential extra conclusion. The positive semidefinite matrix H=a²I-EE* satisfies b_i H b_i*=0 for every i. Equivalently, every b_i H^(1/2) is zero. Therefore B H^(1/2)=0, and invertibility of B implies H=0. Hence

    EE* = a² I.

It would be incorrect to infer this from one constrained row alone. Here all inverse rows provide an invertible spanning family, so the inference is valid.

Using BE=I-BF and FF*=I gives

    I - BF - F*B* + q BB* = 0.

Substitute B=q^(-1)A* and multiply by q:

    qI - A*F - F*A + A*A = 0.

For C=F-A, this is exactly C*C=(1-q)I=a²I. The matrix C is the omitted-entry Fourier mask and has N-s nonzeros per column. Since C is square and a>0, C/a is unitary, so CC*=a²I as well. Its diagonal gives N-s nonzeros in every row. Both retained and omitted masks are therefore regular on both sides, and the inverse B has exactly s nonzeros in every row and column.

Every floor-attaining M is uniquely recovered from its mask by M=q(A*)^(-1). This proves the claimed classification of all minimizers at the floor, not just of the explicit divisor examples.

## 3. Independent sufficiency proof

Suppose C is a Fourier-entry mask with C*C=a²I and N-s omitted entries in every column. Define T=F*C. Then T*T=TT*=a²I, so T is normal and ||T||=a<1. Therefore I-T and I-T* are invertible. As A=F-C=F(I-T), the asserted witness exists and equals

    M = q F (I-T*)^(-1).

Its inverse is q^(-1)A*, with exactly s nonzeros per row. The row-regularity deduction above also proves the exact column count.

There is a direct error certificate independent of merely reversing the necessity calculation:

    E = M-F
      = F (T* - a²I)(I-T*)^(-1)
      = F T* Q,
    Q = (I-T)(I-T*)^(-1).

Because T is normal, these factors commute with their adjoints, and QQ*=I. It follows that

    EE* = F T*T F* = a²I.

Thus the witness attains the operator-norm floor exactly. This also shows why a retained Fourier mask A alone need not be the right approximant. The inverse formula, including its factor q, is essential outside special cases.

The candidate's conditioning statement is valid: singular values of A lie in [1-a,1+a], hence singular values of q(A*)^(-1) lie in the same interval because q=(1-a)(1+a). Consequently kappa_2(M)≤(1+a)/(1-a). A general condition-number-one assertion is neither proved nor claimed.

## 4. Why absence of a mask implies a strict infimum gap

This step is valid and closes the potential nonattainment loophole. The admissible class is nonempty, for example it contains nonzero scalar multiples of I, so its infimum is finite.

If Delta(N,s)=a, choose admissible M_j with ||M_j-F||→a. For all sufficiently large j, put rho=(1+a)/2<1 and obtain

    ||M_j|| ≤ 1+rho,
    sigma_min(M_j) ≥ 1-rho > 0.

A subsequence converges in the finite-dimensional matrix space to M_infinity. The singular-value lower bound survives the limit, so M_infinity is invertible. Inversion is continuous on this uniformly nonsingular set, giving M_j^(-1)→M_infinity^(-1).

Matrices with at most s nonzeros in each row form a finite union of closed coordinate subspaces. Thus inverse-row sparsity survives the limit, even if some coefficients vanish or the support pattern changes along the original sequence. Norm continuity gives ||M_infinity-F||=a. The necessity proof then produces the forbidden mask.

Accordingly, equality of the infimum forces attained equality and a mask. When there is no mask, Delta(N,s)>a. The argument does not produce a numerical gap size, and it would not justify the same conclusion at a=1 without additional work. The report's parameter range avoids that endpoint.

## 5. Complementary-divisor construction

Let N=md with 1≤d<N. The row sets I_t={td+u:0≤u<d} and column sets J_t={t+ell m:0≤ell<d}, for 0≤t<m, partition the coordinates. The omitted mask retains exactly I_t×J_t.

Inside the t-th rectangle,

    omega^((td+u)(t+ell m))
       = omega^((td+u)t) (omega^m)^(u ell),

because td ell m=t ell N. The phase omega^m is a primitive d-th root. Each rectangle is therefore sqrt(d/N) times a diagonal unitary times F_d. Distinct rectangles have disjoint row and column sets. After a column permutation, C is block diagonal with these scaled unitary blocks, so both Gram matrices equal (d/N)I.

The criterion applies with s=N-d and gives Delta(N,N-d)=sqrt(d/N). At d=1 the omitted mask is the diagonal, solving s=N-1 for all N≥2. At d=2 the construction works exactly for even N≥4, giving the positive codimension-two result. The claim that d divides N is sufficient is valid; no unsupported necessity statement is made for general composite dimensions.

## 6. Odd codimension-two obstruction

For odd N and omission weight two, consider two distinct columns j,k of a hypothetical mask. Their inner product, apart from the common factor 1/N, is

    sum_{r in T} omega^(r(k-j)),

where T is their support intersection. It has at most two elements. A one-term sum is nonzero. Two terms can cancel only if their quotient is -1, impossible among N-th roots for odd N. This remains true when the two terms coincide, in which case their sum is twice a nonzero root.

Therefore all column supports must be disjoint. N columns each containing two entries cannot have disjoint supports in only N rows. No mask exists. Section 4 converts this obstruction into a strict infimum inequality. Together with the even divisor construction, the asserted parity classification is complete at its stated sharpness scope.

For N=3, this is consistent with the prior accepted exact value sqrt(3)/2, which exceeds sqrt(2/3).

## 7. Prime-dimensional obstruction

For prime p, let w=p-s with 2≤w≤p-1. For distinct column indices j,k, multiplication by k-j permutes the residues modulo p. Their support-intersection sum is consequently P(omega), where P has 0–1 coefficients, degree at most p-1, and fewer than p nonzero coefficients.

The cyclotomic polynomial Phi_p=1+x+...+x^(p-1) is the minimal polynomial of omega over Q. The report's Eisenstein proof after x→x+1 is correct. If P(omega)=0, Phi_p divides P. The degree bound makes P either zero or a scalar multiple of Phi_p; the coefficient condition and fewer than p occupied coefficients exclude the latter nonzero case.

Thus any two column supports are disjoint. Having p disjoint supports of size w≥2 in p rows is impossible. The compactness result yields strict separation of the infimum. At w=1 the divisor construction works. This proves the entire prime-dimensional floor-sharpness classification, including the vacuous excluded-budget range at p=2. It gives no exact values or quantitative gap in the nonsharp cases.

## 8. Fresh independent exact controls

`fresh_controls.py` was written for this review after inspection. It neither imports nor executes the candidate checker or historical checkers. It uses rational coefficient tuples in Q[z]/Phi_N(z), exact polynomial reduction, independently implemented matrix arithmetic and Gaussian elimination, and exact polynomial inverses. Conjugation is z→z^(-1). No floating-point tolerance or numerical norm estimate enters any test.

The successful run is recorded in `FRESH_RESULTS.json`, `FRESH_RUN.log`, and empty `FRESH_RUN.stderr`:

- **171 divisor masks:** every proper divisor for N=2,...,42 and N in {48,54,60,66,72}. Both Gram orders and all row/column support counts were verified exactly.
- **20 direct inverse witnesses:** every divisor case for N=2,...,10, plus noncanonical weight-one permutation masks at N=3,5,7. The latter test the general criterion beyond the displayed block constructor. Both inverse products, both exact error Grams, every inverse-row and inverse-column support, the diagonal BF entries, and inverse-row squared norms passed.
- Normalization in those tests is W=sqrt(N)F, Z=sqrt(N)M, K=M^(-1)/sqrt(N). Thus ZK=KZ=I and (Z-W)(Z-W)*=dI are precisely the required normalized statements, with no unrepresented square-root approximation.
- **208,116 exhaustive masks:** all fixed-column-weight masks for N=2,...,5 and every nontrivial weight. The test checks exact column cross-Grams without first discarding row-irregular masks. It then independently verifies that every passing mask is row-regular. The passing counts are N! for weight one, eight at (N,w)=(4,2), and zero for all remaining tested weights.
- **141,470 prime root subsets:** every nonempty proper subset for p in {2,3,5,7,11,13,17}; none vanishes.
- **35,853 odd root pairs:** every pair of distinct roots for every odd N=3,...,75; none vanishes. Equal-root pairs are nonzero trivially.
- **Negative controls:** invalid divisor parameters; deletion of a mask entry; correct column norms without orthogonality; two-sided support regularity without orthogonality; the naive choice M=A at (N,d)=(3,1), whose inverse is dense; and a wrong witness gain. Each was rejected by the appropriate exact condition.

Finite controls corroborate the proofs and guard against formula, normalization, and implementation mistakes. They are not substitutes for the infinite statements. No broader composite-mask search was started.

## 9. Scope, record delta, and stop

The candidate's proposed record delta is accurate. The solved scope is global simultaneous **floor sharpness**, the divisor exact-value family, codimension-two parity, and the prime sharpness classification. No general exact optimizer, full composite classification, or quantitative gap is implied.

The construction can produce a dense M and uses an inverse or equivalent solve. Sparse inverse support does not by itself establish a cheap application algorithm, FFT improvement, free preparation or output, finite-word stability, or an arithmetic lower bound. Sparse-column and fixed-frame commutator limitations elsewhere in the owner record are unchanged. No historical-priority or worldwide novelty clearance is claimed by this review.

The requested independent gate is complete: necessity, sufficiency, compactness, divisor blocks, parity, and prime arguments were checked; fresh exact and negative controls passed; and the final candidate bindings remained unchanged. No GitHub, spreadsheet, repository index, or other external state was modified. No further research gate is needed to accept these exact scoped results.
