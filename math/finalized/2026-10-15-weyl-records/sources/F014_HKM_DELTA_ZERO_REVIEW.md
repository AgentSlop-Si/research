# Independent review: F014 matched comparison and delta-zero strengthening

13 October 2026 UTC. Two separate mathematical verdicts, tied to exact input bytes. No external state was changed.

## Verdicts

1. **ACCEPT the bounded primary-source comparison.** All three original rank tests are restrictions of the same finite evaluation-atom moment construction. Harmouch–Khalil–Mourrain (HKM) is an exact model match for that ingredient. Its complex-field framework is not misrepresented as a theorem over all fields: the relevant finite polynomial identity is proved directly. The inspected source sections do not state the complete finite-Weyl/gcd result. This establishes neither historical novelty nor prior publication of the assembled theorem.
2. **ACCEPT the separate delta-zero strengthening.** For every odd N at least 3 and every field allowed by P06, in precisely the original scalar-numerator, common-generating-pair, fixed-order resolvent grammar, delta=0 implies b >= ((N+1)/2)^2. The proof below is all-N algebra, supplemented by new independent checks. It does not rely on finite testing or an unproved tensor assumption.

No correction to either submitted mathematical argument is required. This review leaves the original R17/P06 acceptance intact and adds a separately reviewed strengthening. The source-comparison stage can now close at its proposed priority 15; it need not stay at its prereview priority 53. The candidate's 45 was a review-task priority, not a probability of novelty. This completed candidate review creates no new canonical discovery and supplies no worldwide priority clearance.

## 1. Exact input and source binding

The reviewed source packet has MANIFEST.json SHA-256 d16e7dfe3ff285042414412092bc9d798767f8da553d99a76b02f94ff515ab64. All 19 manifest members passed fresh byte-count and SHA-256 checks. All seven declared copied sources were also compared byte-for-byte with their recorded original local paths.

The original accepted P06 text has SHA-256 6fbe518c9837cfd73a198f9dfc77ecd9a0ffecdcf2a99ab7a0428ebd1c65f091. The baseline R17 decision says ACCEPT and binds that exact digest. REPORT.md has SHA-256 aedac37deae402972b31e2d4c913c9d8ac071e52164b82ee75346ebdf72ed2dc; CANDIDATE_DELTA_ZERO.md has SHA-256 21ef01267cc2775a80a49f59de6a032575482d7f7d330dd7f3596d9140c24a80. This review read those complete texts and the original phase-13 proof and audit. The original source checker programs were neither executed nor imported. Their historical test counts are not newly certified here.

The review bundle preserves the P06, report, candidate, input manifest, and source-pin metadata as inert evidence. INPUT_VERIFICATION.json records the full input check. The exact primary-paper version and reading depth are recorded in PRIMARY_REVIEW.json.

## 2. Primary-source comparison: exact ingredient, bounded attribution

I independently opened [HKM, arXiv:1701.05805v1](https://arxiv.org/pdf/1701.05805v1), the version dated 19 January 2017. Section 2, PDF pages 3–4, defines moment matrices on arbitrary nonnegative multi-index sets and, more generally, polynomial lists. Example 2.4, PDF page 5, identifies point evaluation with a rank-one Hankel operator and gives the corresponding finite matrices. Its points range over complex affine space, so zero coordinates are included. The paper's infinite series use characteristic-zero factorial conventions. Those series and its decomposition/recovery theorems are unnecessary for the implication under review.

That definition/example is the inspected predecessor for the finite rank-one mechanism. I inspected the relevant defining passages and neighboring statements, not the complete numerical article or every cited paper. The paper is bibliographically pinned by its versioned URL, not represented as a locally hashed PDF. The supplied comparison's other specialist nonmatches remain bounded by its stated access depth; this review neither enlarges them into full-paper exclusions nor repeats previously blocked retrievals.

### Direct finite-field-neutral substitution

Work over the common extension field E containing the branch parameters. Let V_box be the E-vector space with basis x^i y^j for 0 <= i,j < N; it is not a quotient algebra with x^N=y^N=1. Define the linear functional L only on V_box by L(x^i y^j)=C'_F[i,j]. A branch representation gives

L = sum_l kappa_l ev_(alpha_l,beta_l) on V_box,

where kappa_l=c_l/((1-alpha_l^N)(1-beta_l^N)). For any two monomial lists P,Q with every product in V_box,

M[P,Q] = sum_l kappa_l (p(alpha_l,beta_l))_p (q(alpha_l,beta_l))_q^T.

This equality is elementary multiplication of field elements, including zero coordinates. It proves rank M[P,Q] <= b without factorials, infinite target moments, positivity, distinct atoms, nonzero parameters, flat extension, reconstruction, or separation assumptions. Repeated atoms and cancellations can only lower the rank. This is the exact all-field algebra used from the complex evaluation model.

Choose:

- P=(1,x,...,x^(N-1)), Q=(1,y,...,y^(N-1)): M=C'_F, since each product has a separate coordinate exponent below N.
- P=Q=(1,x,...,x^(m-1)), m=(N+1)/2: M[a,c]=C'_F[a+c,0]. The maximum exponent is 2m-2=N-1.
- P=Q=(1,y,...,y^(m-1)): M[b,d]=C'_F[0,b+d], with the same nonwrapping boundary.

These are precisely the three original tests, using all legal branch parameters. An infinite functional could be extended in many ways, but no extension is needed and the target is never assumed N-periodic outside its known box.

## 3. Rechecked operator algebra and original target ranks

Let S e_t=e_(t+1), T e_t=omega^t e_t, U=S^u T^v, V=S^r T^s, and D=us-vr invertible modulo N. Write A=u^2+v^2, B=r^2+s^2, h=ur+vs, delta=(D-h)/2. All exponent divisions are inverses in Z/NZ, never division by 2 or 4 in E.

The canonical Weyl coefficient is

C_F[a,b] = (1/N) sum_t omega^(-bt) F[t+a,t]
           = Gamma omega^(-(a-b)^2/4),

where Gamma=(1/N) sum_t omega^(t^2). The invertible residue change (t,s) -> (t-s,t+s) and character orthogonality give G(omega)G(omega^(-1))=N. As N is nonzero in E, Gamma is nonzero. This proof also works in field characteristic 2.

Direct multiplication, with the displayed order unchanged, gives

U^i V^j = omega^(uv i(i-1)/2 + rs j(j-1)/2 + vr ij)
          S^(ui+rj) T^(vi+sj).

The direction map is invertible modulo N, so these words form an independent basis. Dividing the canonical coefficient by the word phase gives

C'_F[i,j] = Gamma omega^(-A i^2/4+uv i/2-B j^2/4+rs j/2+delta ij).

This sign was also checked against actual monomial actions and full reconstruction. In particular, the mixed exponent is delta, not its negative or the reversed-order exponent.

Odd N gives U^N=V^N=I. Thus each inverse is the finite geometric numerator divided by 1-alpha^N or 1-beta^N. Multiplying the U sum before the V sum requires no commutation and gives exactly kappa alpha^i beta^j. Nonresonance makes both denominators nonzero. Even a zero scalar c does not legalize an undefined resolvent.

Scaling C'_F by nonzero row/column chirps leaves [omega^(delta ij)]. With d_delta=N/gcd(N,delta), it has at most d_delta distinct rows and a leading d_delta-square Vandermonde minor of full rank. Each axis Hankel matrix similarly reduces to [omega^(-A ac/2)] or [omega^(-B bd/2)], with exact ranks min(m,N/gcd(N,A)) and min(m,N/gcd(N,B)). This checks the entire three-way maximum as a calculation made for this target, not a theorem attributed wholesale to HKM.

The arithmetic implication is retained: AB=h^2+D^2. Any prime divisor of N and delta forces h=D and AB=2D^2 nonzero modulo that odd prime. Consequently gcd(gcd(N,delta),gcd(N,A))=1 and d_delta d_A >= N. With m >= sqrt(N), the original uniform square-root and odd-prime-power half-length corollaries follow. The N=15 tuple (1,2,1,3) still gives the original maximum 5, not 8.

## 4. All-odd-N proof of the accepted delta-zero extension

Assume the full P06 hypotheses, with delta=0 modulo N. Keep exactly the same U,V in every branch, scalar numerators c_l only, the same ordered product of resolvents, and alpha_l^N !=1, beta_l^N !=1. Permit zero c_l, alpha_l, beta_l. No additional Weyl endpoints, nonconstant numerator factors, branch-specific generators, reverse orders, or correction terms are included.

Since h=D modulo N, the residue-ring identity AB=h^2+D^2 becomes AB=2D^2. The factors 2 and D are units in Z/NZ, so their product is a unit and hence both A and B are units. This is a statement in Z/NZ, independent of the characteristic of E.

Set m=(N+1)/2 and I={(a,b):0<=a,b<m}. Define a square matrix of size m^2 by

H[(a,b),(c,d)]=C'_F[a+c,b+d].

Every coordinate sum is at most 2m-2=N-1. Thus every entry belongs to the original finite coefficient box and no reduction modulo N occurs.

Let f_i=omega^(-A i^2/4+uv i/2) and g_j=omega^(-B j^2/4+rs j/2). The verified coefficient identity gives C'_F[i,j]=Gamma f_i g_j. Under lexicographic ordering of I,

H=Gamma (X tensor Y), X[a,c]=f_(a+c), Y[b,d]=g_(b+d).

Exactly,

X=diag(f_a) [omega^(-A ac/2)] diag(f_c),
Y=diag(g_b) [omega^(-B bd/2)] diag(g_d).

The m nodes omega^(-A a/2) are pairwise distinct: equality would imply N divides a difference times a unit, and the difference has magnitude less than N. The same holds for B. Both square Vandermonde matrices are invertible in E. Their diagonal factors and Gamma are nonzero. Hence H is invertible, with inverse Gamma^(-1)(X^(-1) tensor Y^(-1)), and rank H=m^2.

One legal branch gives

H_l[(a,b),(c,d)]=kappa_l(alpha_l^a beta_l^b)(alpha_l^c beta_l^d).

The constant-index entry of its evaluation vector is 1. Consequently this outer product has rank one if c_l is nonzero and rank zero if c_l=0. At a zero parameter, the monomial convention 0^0=1 is precisely polynomial evaluation; alpha^(a+c)=alpha^a alpha^c remains true for all nonnegative indices. Nothing requires alpha or beta to be invertible.

Finally, H=sum_l H_l, so m^2=rank H <= sum_l rank H_l <= b. Therefore

b >= ((N+1)/2)^2.

This proves the claim for every odd N under the stated field and grammar hypotheses. The slice exists for every such N, for example (u,v,r,s)=(1,0,1,1), where D=h=1, A=1, B=2. In particular the bounds for N=3,5,9,15,21 are respectively 4,9,25,64,121.

No assertion follows about equality attainment, minimum over all pairs, all-pair quadratic bounds, optimal legal-pole decompositions, arithmetic runtime, or wider grammars. Tensor separation here explicitly uses delta=0.

## 5. Fresh independent checker and adversarial controls

independent_check.py was authored for this review, without inspecting or using the submission's checker code. It uses only the Python standard library. Its operator path computes monomial column actions by repeated composition, extracts coefficients by trace, and reconstructs the complete Fourier matrix. It then compares the separately derived phase formula. Dense Gaussian inversion computes actual legal resolvents in the small-operator controls. All ranks use exact elimination, including binary extension fields.

The fresh run and an isolated relocated `python -I` replay produce byte-identical CHECK_RESULTS.json:

- 80 direction/field cases, with 21,800 actual coefficient entries and complete operator reconstructions
- All three original ranks in every case, including mixed composites and characteristic 2
- 21 full delta-zero bivariate rank computations, up to m^2=169, including characteristic-2 lifts at N=3,5,7,9,15,21
- 40 actual dense-resolvent branch checks, including each zero-parameter boundary and zero scalar
- 350 evaluation-atom controls, including rank-zero weights; these are not all nonzero rank-one atoms
- A five-term moment-sum check with repeated cancelling nodes, zeros, and zero weight
- An independent residue arithmetic sweep of 270,336 generating direction pairs for all odd N from 3 through 19, including 15,328 delta-zero pairs

Thirteen negative controls guard the inference boundaries. At N=5 over F101, actual single operators acquire bivariate Hankel ranks 2 with an extra left U endpoint, 2 with numerator I+U, 9 with reverse resolvent order, and 9 after changing a branch's generator pair. Enlarging the evaluation index set and wrapping cyclically turns a legal rank-one atom into rank 9. Further controls detect false periodic extension, forbidden poles (including zero scalar at a pole), loss of U^N=I at even N, a nonprimitive root's deficient rank, failed tensor separation when delta is nonzero, loss of the coordinate basis for nonunit D, and a rank-one coefficient array which is not geometric.

These controls demonstrate why the exclusions matter; they are not claimed counterexamples to the accepted narrowly stated lower bound. The finite evidence supports the explicit proof above and does not replace it.

## 6. Closure and remaining scope

Accept the named-source substitution and close that bounded comparison stage. Preserve the qualified historical nonmatch and do not recast it as either historical priority or a claim that the entire result was old. Record the delta-zero theorem as an accepted same-grammar strengthening attached to F014, separately from the unchanged original P06. Do not create an additional canonical discovery or automatically reopen sharpness/wider-grammar work. No external table, repository, or publication was modified by this review.
