# C03 reciprocal Hankel-resultant: breakthrough assessment

13 October 2026. Read-only source and primary-literature audit. No historical program was executed or imported. No Sheet or GitHub write occurred.

## Verdict

**Correct, useful specialized algebra; no demonstrated serious mathematical breakthrough.** The exact diagonal-pencil formula may still be an original printed specialization, but that is unresolved. Its core mechanisms have exact classical antecedents, and a complete coefficient-level reduction to classical Bezoutian/Barnett-Hankel theory is already accepted in the project. No consequential general recovery or asymptotic FFT advance follows from the accepted theorem.

This conclusion does not say that every line of the complete formula has previously appeared verbatim. The appropriate classification is **known-mechanism corollary/specialization, exact complete-family priority unestablished**. Correctness, historical firstness, and importance are separate questions.

## Identity and current accepted scope

Stable canonical ID C03; workflow Q17; NEW-06 is a view of that same result, not another discovery. Accepted base: P02 section A, review R15. Current title: Universal reciprocal diagonal-pencil resultant. Saved all331 locations: Catalogue row 158, Theorem register row 33, Research queue row 20, Research overview rows 28/31/32, New results row 9. Current saved rows explicitly leave C03::specific-priority open while retaining proof closure.

For m>=1, arbitrary A,B in S^(m×m), S any commutative ring, let D=diag(1,w,...,w^(m-1)), f(a,w)=det(A-aDAD), g(a,w)=det(B-awDBD). R is their fixed homogeneous degree-(m,m) Sylvester resultant, even if actual degrees drop. Set T=m²(2m-1), v=m(m-1)(4m+1)/6, b=m(m-1)(2m-1)/6. Then

R(w)=w^(v+b)(w-1)^(m²)V(w+w^(-1)), deg V<=b,
w^T R(w^(-1))=(-1)^(m²)R(w).

The original adjacent-Hankel case is A_ij=T_(i+j), B_ij=T_(i+j+1), m=s+1. Hankel structure is unnecessary for the universal formula. Singular inputs, zero resultants, degree drops, characteristic two, and zero-divisor rings are included. Exact vanishing orders and full residual degree are generic, not valid for every specialization.

I read the complete accepted base proof (SHA256 f6412a2cb78457a2fddd62a6e688095cb82528b4457ad1454dbbe069179937d6), structural supplement (2da369c92f44648dcf1c68c94fae623610efedf37ab11e91a1df328ebb858a14), and singular-safe evaluator (7152d1a8f5eaf813a79b3a78a5cdb2545c445a9ef0ac0e7c5c50bb5d88df7035), and checked their acceptance pins. This is not a theorem inferred from its title.

The structural supplement supplies the signed leading coefficient

[x^b]V=(-1)^(m(m-1)/2)det(A)det(B) product_(j=1..m-1) ell_j(A)r_j(A)ell_j(B)r_j(B),

with ell/r the leading/trailing principal minors. It also supplies a division-free Laurent divided-difference determinant, tangent and parity endpoint formulas, and exact field multiplicity statements. Those are useful explicit calculations, not a new theory of resultants.

## Exact primary comparisons

1. **Resultant covariance: exact classical component.** Busé–Mourrain, Remark 2.1 and equation (2.2), uses expected degrees and arbitrary commutative rings. The degree-one change of two variables multiplies the degree-(m,m) resultant by det(C)^(m²). Coordinate reversal gives the reciprocity sign. The collision substitution a=1+epsilon*t, w=1+epsilon, combined with entrywise epsilon divisibility, gives the forced (w-1)^(m²). These are direct substitutions, not a claim that their paper prints C03. [Primary text](https://arxiv.org/pdf/cs/0612050)

2. **Trace compression: exact printed component.** Baker, Appendix B Proposition B.1 and Remark B.2, gives the reciprocal representation through w+w^(-1) over a ring and the integral recurrence C_0=2, C_1=x, C_(k+1)=xC_k-C_(k-1). C03's fixed-grade degree-drop version follows from the same coefficient argument. Remark B.3 also prints the exact geometric-series trace recurrence used by the later triangular corollary. Baker's separate square-resultant theorem is inapplicable to generally nonreciprocal a-inputs. [Primary text](https://arxiv.org/html/2309.02512v2#A2)

3. **Hankel/Bezoutian bridge: exact known-component reduction.** García-Armas–Ghorpade–Ram, Proposition 3.4, states Bez(u,h)=Bez(u,1) H(u,h) Bez(u,1) for every monic degree-m u and deg h<m over a field; coprimality is unnecessary. C03's accepted bridge uses alpha=lc_a(f), beta=lc_a(g), u=f/alpha, h=g-beta*u, and H from h/u at infinity. This gives R=(-1)^(m(m-1)/2)alpha^m det H. It is an explicit classical substitution. Over general rings this normalized chart requires units, or localization at det(A) and w. The universal padded identity precedes localization. Raw adjacent moments and this derived rational-function H are different objects. [Primary text](https://arxiv.org/html/1011.1760#S3)

4. **Degree-drop/gcd bookkeeping: established component.** Ćurgus–Dijksma §5 equation (12) prints padded nullity m-max(deg f,deg g)+deg gcd(f,g), including an infinity contribution, in the complex setting. The accepted bridge independently supplies the all-field algebraic extension and excludes the both-zero pair. This cannot be used to infer an arbitrary-ring rank theorem or base-field candidate existence. [Primary text](https://arxiv.org/pdf/1208.2385)

5. **Valuation and top coefficient: specialized classical calculation.** The accepted mixed-minor expansion has coefficient weights j(j-1) and j². The two root-slope families are -2i and -(2j+1), so no pairwise leading cancellation is possible; the resultant root product gives v=sum_(i,j)min(2i,2j+1). Sturmfels's Theorems 2.1/4.1 provide the general resultant initial-form machinery; the signed principal-minor product is the project's explicit specialization. The primary extracted theorem passages were reopened. Formula screenshots failed, so I do not claim fresh image verification of Sturmfels's displayed arrays. [Primary publisher PDF](https://link.springer.com/content/pdf/10.1023/A:1022497624378.pdf)

6. **Residual determinant: classical operator-resultant corollary.** Conrad, Theorem A.1, identifies a Kronecker difference determinant with the characteristic-polynomial resultant over commutative rings. Generic normalization followed by polynomial specialization gives Res(det(A-aC),det(B-aF))=det(A tensor F-C tensor B). Substituting C=DAD,F=wDBD and extracting entrywise factors gives the accepted residual and endpoint formulas. Conrad is an undated exposition, not evidence of earliest priority. [Primary author exposition](https://kconrad.math.uconn.edu/blurbs/linmultialg/univid2old.pdf)

7. **Moment-resultant interpolation neighbor, not a full match.** Uteshev–Baravy Theorem 6.2 expresses resultants via Hankel determinants of weighted ratio samples at distinct nodes, with sampled numerators/denominators nonzero. Their moment construction does not automatically identify the C03 pencils. The theorem is genuine prior subject matter, not an exact full-family antecedent. [Primary text](https://arxiv.org/html/1603.08752#S6)

## Algorithmic significance

The accepted deterministic O(m³) field-operation, O(m²) field-storage bound is for one supplied nonzero w, including singular pencils and the endpoint. It composes a classical degree-one polynomial-matrix determinant algorithm with a padded scalar resultant. Mulders–Storjohann Theorem 4.2 already gives O(n³d²); setting d=1 supplies the determinant cost. [Primary text](https://cs.uwaterloo.ca/~astorjoh/jscpopov.pdf)

The sample bound improves T+1 to b+1, asymptotically a factor of six, but both counts remain Θ(m³). Reciprocity alone supplies the final factor of two. All-coefficient evaluation/interpolation by the stated classical route costs O(m⁶), after supplied nodes and extensions are accounted for. No full-recovery cubic algorithm, numerical-stability benefit, bit-complexity breakthrough, or unrestricted FFT improvement is established.

The accepted triangular specialization has an explicit product of known geometric-series trace polynomials and a complete supplied-subgroup solution routine. Its simplification depends on triangularity; the base proof already used A=B=I as the sharpness example. It does not establish the intended general sparse-reconstruction advance.

## Source recovery and remaining limits

The complete_source_coverage_1453 record marks C03 as NEEDS_SCOPE_SELECTION, with no exact missing source prerequisite for its accepted base. It flags later exact triangular/general bridge archives as provenance gaps. This pass recovered their full mathematical publication derivatives directly from private GitHub and verified the returned Git blob hashes:

- [General accepted bridge](https://github.com/AgentSlop-Si/research/blob/main/math/reviewed_rounds/2026-10-12-network-algebra/c03-general-hankel-bridge.md), identifying original review SHA256 7cb68185e98e6e24696fcdfb8b348ab61aaac5bca7e16bbe116df9aed0458634.
- [Accepted triangular corollary](https://github.com/AgentSlop-Si/research/blob/main/math/reviewed_rounds/2026-10-12-reviewed-research/c03-triangular-corollary.md), identifying original review SHA256 ab24054d4b3e819897a624632f79413dac4321556c8cf0f3e54d1cb712f92e07.
- [Bounded 1989 attribution checkpoint](https://github.com/AgentSlop-Si/research/blob/main/math/reviewed_rounds/2026-10-12-coloring-attribution/c03-bounded-attribution-checkpoint.md). Its Helmke–Fuhrmann details remain author-reported because primary text was not retained for that reviewer; the source URL also failed in this pass. The already verified noncoprime 2010 bridge remains sufficient for the component assessment.

Original exact ZIP byte identity is not recovered merely by reading a derivative, but a missing current mathematical body no longer blocks this bounded assessment. No historical controls were rerun. A private GitHub code search returned no C03 hits, while direct repository tree traversal successfully located the reports; negative search alone was not treated as absence.

No inspected primary statement prints the entire arbitrary-matrix family, v/b formulas, signed leading coefficient, and endpoint package verbatim. Targeted searches did not locate one. That leaves precise formula firstness unresolved; it does not supply positive evidence for a major discovery. A supporting proposition or carefully positioned formula note is plausible. Leading a serious-breakthrough claim with C03 is not supported by the present evidence.
