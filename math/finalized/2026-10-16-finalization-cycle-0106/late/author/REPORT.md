# Quadratic and spectral feedback: owner-specific comparison completion

16 October 2026. Candidate for independent review. Repository baseline: `73528f9e7495b0614106dfc4cc5b5c42907daaf5`. Workbook: `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`.

## Result and scope

This proposal completes two explicitly recorded **secondary, source-specific comparisons**, for M-QUADRATIC-FEEDBACK and M-SPECTRAL-FEEDBACK. It closes zero research records and zero primary mathematical gates. Both remain TO RESEARCH, priority 34. Their existing constructive obligations remain open, with no proof, novelty, numerical, production or worldwide-priority promotion.

The complete live owners were read: Catalogue 107–108; novelty 170 and 172; overview 239 and 241. Their action/stop fields still request the matrix-polynomial, Cayley, spectral-projector and Schur comparison. Catalogue Z and the earlier complete M-record inventory identify the actual constructive successors. The current owner rows, their full history and notes, both pinned research reviews, and the selected REVIEW-10 outcomes were inspected. The historical source-note references to novelty rows 190/192 are stale; the live stable IDs and live hyperlinks resolve to 170/172. No historical note is proposed for alteration.

The already-completed M-CONJUGATED-FEEDBACK comparison is prior evidence, not new work here. Its general interpolation/resolvent formula and Schur-domain observation are explicitly inherited. The additions here are the two owner-specific hypothesis/cost maps, including the common-cycle zero-weight and inverse-action distinctions, spectral integer multiplicity, forced-B order, and the difference between an involution's sign and the unnormalized target matrix's sign. No accepted control or theorem is replayed or counted again.

No supplied program was executed, imported, installed or parsed as code. No solver, benchmark, new empirical experiment or external write was performed. The formulas below are direct statement comparisons and algebraic guard illustrations, not new accepted theorem claims.

## Shared named sources

[Higham, Functions of Matrices, 2006 author manuscript](https://eprints.maths.manchester.ac.uk/310/1/fm_final.pdf), §1 definition (4) and Facts 3, 5, 6, describes polynomial interpolation, commutation, similarity and diagonalizable evaluation. Section 6 defines the complex matrix sign by left/right half-plane eigenspaces and states its involution property. These supply classical functional-calculus comparators, not structured synthesis algorithms. Its complex half-plane language is not a finite-field theorem.

[Davies–Higham, A Schur–Parlett Algorithm for Computing Matrix Functions](https://eprints.maths.manchester.ac.uk/156/1/paper.pdf), Algorithm 5.1, takes a supplied complex matrix, an analytic function on a closed convex neighborhood of its spectrum, and derivative evaluation. It computes a Schur decomposition and block recurrence. The adjacent dense cost discussion gives roughly 28n³ to n⁴/3 flops, with savings when factors are retained for a few applications. This is an algorithmic upper bound, not a lower bound on structured computation or a constructor for admissible factors.

## 1. M-QUADRATIC-FEEDBACK: common-cycle rational algebra versus construction

### Owner guards and exact match

The pinned review assumes even N, characteristic not dividing N, one Hamiltonian row-action W=diag(w)P, alternating E with E²=I and EWE=−W, and rho=product(w). It requires 1−c^N rho≠0 for c=a,b, and lambda≠0 with lambda²≠1. Zero weights, including W=0, are allowed. The accepted pair is A=C_a and B=lambda C_b E, where

    C_c=(I+cW)(I−cW)^−1=2(I−cW)^−1−I.

Under these poles, C_c is a rational matrix function of the same W. Hence C_a,C_b and their inverses commute with each other. Conjugation by E sends C_c to C_−c=C_c^−1. With R=C_b C_a^−1, ERE=R^−1, so K=BA=lambda R E has K²=lambda²I. The research review separately proves K nonscalar; the two roots are distinct under char≠2 and lambda≠0. These are exact conditions for the two-point interpolation map already used in the conjugated-feedback comparison.

For h(z)=(1−z)^−1, the interpolating polynomial is

    h(K)=(I+K)/(1−lambda²),
    T=h(K)B=(B+BAB)/(1−lambda²)
      =[lambda C_b E+lambda² C_a^−1]/(1−lambda²).

The B multiplier is on the right of h(K). B h(K) cannot be substituted without an additional commutation condition. The second term is C_a^−1, not C_a; E C_b=C_b^−1 E is the step that determines it. This is a classical rational-functional-calculus match, not a new low-degree identity.

The zero-weight branch matters for the comparison. W may be a nonzero nilpotent matrix when rho=0, so diagonalizing W is not a justified blanket implementation. Rational substitution and the guarded cyclic solve still work. Diagonalizability of K follows from its distinct-root quadratic; it does not assert that W is diagonalizable or that a cheap eigenbasis has been generated.

### Cost and oracle distinction

The supplied common-cycle plan already has an O(N) field-operation cyclic solve that never divides by an edge weight. C_a^−1=C_−a is therefore cheap under the same even-N guard. This is stronger than the generic assertion that a cheap forward A need not have a cheap inverse; here the inverse has a specified plan. Evaluating the displayed T uses either the accepted two B/one A sequence or the explicit C_b E and C_−a actions, plus vector arithmetic. Both require paid cycle/weight setup, lawful denominators and writing all N output scalars. They are algebraic operation bounds, not finite-bit, conditioning or approximation-error guarantees. Any invocation of Fourier also pays primitive-root and field-representation preparation under its declared access contract.

This pair does not hide Fourier in its preparation. Nevertheless the accepted denominator-support proof already rules it out as a Fourier-compatible growing-length construction. Put P=(I−bW)(I+aW). P and PT have at most three entries per row. Combined with the reviewed splitting-field support-product bound, covariance requires N≤9, hence excludes even N≥10. The a=0/b=0 and a=±b refinements retain the N≤4 and N≤6 bounds. These are inherited accepted results, not consequences newly supplied by Higham or Schur–Parlett. They do not cover independently ordered general paired-Green maps.

A generic Schur evaluation of an already-supplied K cannot repair this failed target identity or certify a different A/B pair. For real |lambda|>1, the pole 1 lies between −lambda and lambda, so the literal rational h fails Algorithm 5.1's convex-domain condition; for 0<|lambda|<1 that particular obstruction disappears. The equivalent linear polynomial removes the analytic obstruction in either case, but still needs the certified K relation and its paid actions. This owner-specific consequence is an application of the earlier comparison, not an additional general discovery.

Disposition: the named secondary formula/method comparison is discharged as an exact algebraic match with constructor/cost nonmatches. The primary successor still requires a Fourier-compatible admissible family escaping the same-W denominator-support obstruction, with full setup, application and numerical/bit costs when claimed. Merely changing a,b,lambda or weights inside the accepted family cannot solve that successor in the excluded lengths.

## 2. M-SPECTRAL-FEEDBACK: projectors, multiplicities and forced target use

### Classical spectral map with exact multiplicity

The pinned review uses unnormalized positive Fourier F over a splitting field with char not dividing 2N. Let lambda≠0, lambda²≠1, prescribed integer 0<r<N, and

    delta+=lambda/(1−lambda), delta−=−lambda/(1+lambda),
    s=2lambda²/(1−lambda²), p=−lambda²/(1−lambda²), M=FA.

The accepted criterion is M²−sM+pI=0 plus rank(P+)=r, where

    P+=(M−delta−I)/(delta+−delta−), P−=I−P+.

The polynomial yields complementary algebraic idempotents and M=delta+P++delta−P−. Choosing bases of their image/kernel establishes similarity to the specified diagonal with r plus entries. This is the owner-specific diagonalizable/interpolation match. Idempotents are not necessarily orthogonal, and existence of such bases supplies no uniform cheap basis algorithm.

Rank is indispensable in the full field model. As a concrete guard illustration, work in F_25 with N=8 and lambda=2. A primitive eighth root exists; char5 does not divide16; delta+=3 and delta−=1. Diagonal projectors of integer ranks1 and6 have the same trace1 in characteristic5. M=I+2P+ obeys the same quadratic in both cases, but the two multiplicities differ. Thus a trace residue does not select the prescribed r. This illustration does not add a new accepted finite control or replace the original review's exact rank checks.

### Matrix-sign comparison: normalization is essential

Define H=2P+−I=((1−lambda²)M−lambda²I)/lambda=K/lambda. Over C, H has eigenvalues±1, so sign(H)=H and P+=(I+sign(H))/2. That is a direct match to Higham §6 for a supplied H. It is not a procedure for constructing the desired H from F and the architectural constraints.

Applying sign to M itself is different. At lambda=2, delta+=−2 and delta−=−2/3, so sign(M)=−I even though 0<r<N and the prescribed P+ is nontrivial. For purely imaginary nonzero lambda=i t, both delta values have real part −t²/(1+t²)<0, giving the same collapse. An arbitrary scalar half-plane classification of M therefore cannot silently replace the affine normalization or the integer-rank condition. No ordering or analytic sign function is transferred to finite fields.

### Forced B and Schur applicability

The owner gives B=(F^−1+A)^−1. Factoring on the correct side gives

    F^−1+A=F^−1(I+M),
    B=g(M)F,   g(z)=1/(1+z).

Using s=−2p and the accepted quadratic,

    g(M)=[(2p−1)I+M]/(p−1)
        =(1+lambda²)I+(lambda²−1)M,
    B=(1+lambda²)F+(lambda²−1)FAF.

B is not Fg(M) in general. The alternate expression (1−lambda²)F−lambda²A^−1 retains the inverse-A charge. The abstract positive controls use A=F^−1 C Delta C^−1 and are explicitly Fourier-oracle controls, not cheap admissible constructions.

At real |lambda|>1, the numbers delta+,delta− straddle −1, so the literal g fails Algorithm 5.1's convex analytic-domain requirement although neither eigenvalue equals its pole. For 0<|lambda|<1 they lie above −1, so that particular domain obstruction is absent. Polynomial replacement is entire and gives the exact matrix value once the quadratic is known. It cannot generate A, verify the quadratic or multiplicity for free, or remove the literal F actions from B. No assertion about all possible matrix-function algorithms follows.

For the owner's unnormalized positive Fourier convention, F^−1=N^−1 R F with R the index-reversal permutation. The scalar N^−1 and permutation action cannot silently disappear through a normalization change. Literal F or F^−1 evaluation pays primitive-root/field-representation preparation, its complete action cost and all N output writes. Field-operation counts alone give neither a bit-complexity bound nor a finite-precision approximation-error contract.

The fixed N4 rejection, its prescribed two amplitudes/orders/poles, and its nonzero 6×6 minor remain inherited. Schur evaluation does not extend that exclusion to general masks, weights, orders or all N. Numerical eigenspaces, approximate ranks and a computed dense factorization are not certificates of exact two-Green membership.

Disposition: the named secondary comparison is discharged as an exact algebraic specialization and qualified algorithm/constructor nonmatch. The actual gate remains uniform admissible cheap A with the exact polynomial and integer multiplicity, together with an admissible cheap forced B, paying setup and inverse work. No such constructor is supplied here.

## Minimal local proposal and reviewer checks

The proposal contains fourteen prefix-only string edits: Catalogue AE/AF, novelty Y/Z, and overview P/Q/F for each ID. The F prefix removes the stale implication that the completed named comparison is the leading task. Original text remains byte-for-byte after the history delimiter. All status, priority, proof, novelty, formulas, notes, validation, formatting and links remain unchanged. No record-count change is proposed.

Require independent acceptance, report publication, and a fresh exact-preimage/stable-ID check before application. Reconcile changed preimages instead of overwriting them. Review the distinct-root/zero-weight guards, actual cheap inverse in the common-cycle family, finite-field trace counterexample, sign(M) versus sign(H), noncommuting B order, domain versus polynomial distinction, inherited source qualifications, and zero primary-gate closure count.
