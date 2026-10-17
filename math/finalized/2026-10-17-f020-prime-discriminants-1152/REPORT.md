# F020: exact prime cyclotomic orders and uniform overlap simplicity

17 October 2026. Canonical owner F020; F023 remains its alias.

Two independent reviews accept the exact characteristic-zero theorem scope below. The [second review](independent_review/SECOND_REVIEW.md) independently rechecks the proof, leading coefficients, source identities and [explicit prior-work map](prior_art/REPORT.md). This report incorporates their required historical and attribution corrections. Native-table application and repository release require their own verification and are not inferred from scientific acceptance.

## Exact mathematical scope

Put H_n(z;q)=sum from k=0 to n of [n choose k]_q z^k, and D_n(q)=Disc_z H_n(z;q), using the ordinary z-discriminant and Disc(1)=Disc(monic linear)=1.

For every odd prime p and n=Ap+b, A>=0, 0<=b<p,

    ord_(Phi_p(q)) D_n(q) = p A(A-1)/2 + A(b mod 2).

For d=p^s with p odd prime, s>=1 and n=Ad+b, the corresponding exact order is

    ord_(Phi_d(q)) D_n(q) = d A(A-1)/2 + A(b mod 2),

**only for 0<=b<p**. This is not a statement for all b<d at a general prime-power order. A=0 and n=0,1 are included under the stated conventions.

The overlap result has a wider domain. For every odd d>=3, every primitive order-d root omega, every odd 1<=b<d and every A>=1,

    g_b = (H_b(z;omega)/(z+1)) at z=-1 != 0,
    J_(A+1)(x;tau_b) = x He_A(x) - A tau_b He_(A-1)(x)

is squarefree, where He is the monic probabilists' Hermite polynomial and tau_b is the retained Rogers–Szegő overlap parameter. At general odd-composite orders this removes the overlap g and J guards. It does not remove residual ordinary-discriminant guards outside independently proved subfamilies.

For d=p^s and b<p the static result gives squarefreeness of H_b. For even b, H_b is relatively prime to 1+z^d. For odd b, U_b=H_b/(z+1) is squarefree, U_b(-1) is nonzero, and U_b is relatively prime to 1+z^d. Composing these facts with the existing local theorem proves the exact orders above and the nonvanishing of its complete signed coefficients.

## Proof and normalization

The proof is documented in the [original source report](first_review/sources/archive_report.tex) and the [first independent review](first_review/INDEPENDENT_REVIEW.md). The mathematical source text is distributed as a locator-sanitized derivative; the historical corrections below govern its interpretation. The original input remains separately retained.

1. Partial sums express tau_b as S_h/S_r for d=2h+1 and b=2r+1. A sector argument proves nonvanishing and nonreality in the principal embedding; cyclotomic conjugation transfers the algebraic conclusions to all primitive embeddings.
2. After shifting y by 1 and scaling by a square root of 2, the two parity-Hermite Wronskians reduce to (X^2+1)^(m-1). Their integral monic forms with unit constant term force every original root to satisfy v_2(y-1)=1/2. The constant m=1 case has no roots.
3. A nonzero repeated root of J forces (tau-1)x^2=tau(A tau+1) and a parity-Wronskian zero. In an unramified extension of Q_2, x^2 belongs to the coefficient field, contradicting the half-integral valuation. The exact exceptional zero-root parameters, tau=0 for odd A and tau=-1/A for even A, are excluded by the RS parameter's nonreality. Odd cyclotomic fields are unramified at 2. Nonreality alone is insufficient over a ramified field.
4. The integral degeneration H_b(-1+tx;1+t^2)=t^b K_b(x,t), K_b(x,0)=He_b(x), gives D_b(q)=(q-1)^[b(b-1)/2] V_b(q), V_b(1)=product j^j. Evaluating a putative Phi_(p^s) divisor at 1 contradicts p>b. The analogous fixed-node quotient constants are signed double factorials, yielding separation under the same b<p restriction.
5. The existing moving-root local theorem supplies the leading cluster coefficients. No coefficient is reinterpreted in a different parameter. If C is the coefficient of (q^d-1)^M at omega, then

       lim_(q->omega) D_n(q)/(q-omega)^M = C (d omega^(-1))^M,
       [D_n/Phi_d^M](omega) = C (d omega^(-1)/Phi_d'(omega))^M.

   For d=p^s this last expression is C(omega^(d/p)-1)^M.

The full sign, powers of d, Hermite discriminant products, resultant factors and overlap g^2 factor are retained from the established local formulas, rather than promoted as newly derived expressions.

## Reconciliation with the actual project baseline

The report's comparison to an October-11 b=1,3 review is a valid comparison to that particular older document. It is not the current project baseline. Before this package, the canonical F020 record already accepted fixed-residual all-A overlap families through b=31 and separate general derivative-nonvanishing and separation inputs. Those acceptances remain in force and are not counted again as new discoveries.

The present increment is the uniform all-odd-d/all-odd-b J-squarefreeness theorem beyond the earlier fixed-residual range, together with the stated prime-power static subfamily and its exact-order composition. It also supplies a uniform alternative proof on already accepted subfamilies. No previous fixed-b certificate, source identity, limitation or dated history is removed.

The [October-16 bounded cyclotomic-deflation result](https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-research-finalization-1722/f020/REPORT.md) remains valid and separate. Its actual-family polynomial, degree bound and strict high-order criterion remain available for the general static route. This packet does not claim its remaining low-degree range, every reciprocal component, or its all-m completion condition has been resolved.

## Prior work and historical originality

The canonical project already records a completed mathematical-body comparison with Lubinsky–Saff (1987). The source report's statement that this entire body comparison is still missing is superseded by that record. The first review's later access difficulty does not undo the earlier comparison. The RS recurrence, self-reciprocity, root-of-unity factorization, static multiplicities and derivative restatements continue to be attributed to classical work.

The [explicit normalization and implication map](prior_art/REPORT.md) identifies the parity polynomials with scaled classical Laguerre polynomials. For s=0,1, A=2m+s-1 and alpha=s-1/2,

    R_m(y)=(-1)^m 2^m m! L_m^(alpha)(y/2),
    W_m^R(y)=-2^(2m-2) m!(m-1)! f_(m-1)^(alpha)(y/2,y/2),
    c=A(tau-1)/(2m),
    J_(A+1)(x;tau)=x^s (-1)^m 2^m m!
                    [L_m^(alpha)(x^2/2)+c L_(m-1)^(alpha)(x^2/2)].

Here f is Sawa–Uchida's normalized Christoffel–Darboux kernel. Its affine nonsingularity lemma implies characteristic-zero squarefreeness of the parity Wronskians: a repeated diagonal zero would have both partial derivatives zero by symmetry. The lemma applies for m>=3; m=1,2 are treated explicitly. Wronskian squarefreeness is therefore a known consequence, and cannot be promoted as a new standalone result.

The same c substitution sends the evaluation point in Sawa–Uchida's quasi-Laguerre discriminant formula to 2z_c=tau(A tau+1)/(tau-1). Thus the generic collision-location and discriminant reductions are established machinery. The comparison retains cancellation at the rational formula's exceptional parameter values and all ordinary-discriminant scaling factors.

The additional arithmetic input is the exact shifted root valuation. Sawa–Uchida's neighboring Section 4 Newton-polygon theorem does not directly supply the required shifted coefficient calculation. In particular its coefficient indexing, root variable and physicists' Hermite normalization differ; the square-root-of-two normalization is ramified. The [126 exact normalization controls](prior_art/normalization_controls.json) support the identities, while their unlimited scope follows from the displayed algebra.

The shifted valuation arithmetic and its unramified RS application remain narrowly identified candidates whose historical originality is **unverified**. A scoped nonmatch to one neighboring Newton-polygon theorem is not priority clearance. The remaining recorded source gaps include the Lubinsky–Saff reference page 360 and citations 9–36, Zhedanov (1997) full-text comparison, and the broader local-discriminant/arithmetic citation chain. The source-comparison addendum refines this list and separates proven identities from historical assertions.

Primary references already inspected in the first review:

- [Sawa–Uchida, Discriminants of classical quasi-orthogonal polynomials](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), Theorem 3.6.
- [Sawa–Uchida, Algebro-geometric aspects of the Christoffel–Darboux kernels for classical orthogonal polynomials](https://da.lib.kobe-u.ac.jp/da/kernel/90009429/90009429.pdf), especially the diagonal-kernel discussion and neighboring Section 4 Newton-polygon arguments.
- [Grosu–Grosu, The irreducibility of Wronskian Hermite polynomials](https://arxiv.org/pdf/2007.00065), the odd-prime and odd-modulus hypotheses in Theorems 7–8.
- [Lubinsky–Saff (1987), publisher record](https://link.springer.com/article/10.1007/BF01890574).

## Verification and source integrity

The first independent review records 470 fresh exact algebra controls, a ramified negative control, nine local ordinary-discriminant coefficient cases and seven complete-polynomial checks in degrees 3–8. Those seven controls use six distinct complete Z[q] discriminants, with degree 6 checked at two root orders. The universal ranges follow from the proofs, not extrapolation from those controls. An optional d=49 static control and optional (d,A,b)=(7,3,5) coefficient computation were interrupted; no result is claimed for them.

All 37 entries of the original frozen review were historically verified. This public derivative omits the selected native-cell evidence and the ID-bearing original PDF/ZIP, removes private locators from textual derivatives, and keeps the redacted scientific provenance lists. It does not claim that all original bytes are distributed or that a private original-input replay can be completed from the public subset alone. The uploaded code was not run or imported. Unchanged independently authored checkers and scientific result data are retained. The original standalone and archive PDFs had different byte hashes but identical full extracted layout text in the first review; their distinct original identities remain recorded in [SOURCE_BINDING.json](SOURCE_BINDING.json). [PUBLIC_DERIVATIVE_MAP.json](PUBLIC_DERIVATIVE_MAP.json) binds all published derivative identities and omissions.

The [second independent review](independent_review/SECOND_REVIEW.md) is distributed with its [original scoped acceptance](independent_review/ORIGINAL_ACCEPTANCE.json) and [SHA-256 manifest](independent_review/SHA256SUMS.json). It reconstructs 128 parity-Wronskian cases through m=64 using a different Hermite-recurrence implementation; nine direct full ordinary discriminants for n=2,...,10; 38 exact cyclotomic-order/full-leading-quotient checks; 20 exact parity/kernel checks; and two general symbolic collision identities. Its three newly authored checkers execute no uploaded or earlier reviewer code. No failed or interrupted computation occurred in that second review.

Native application, if subsequently performed, requires separate exact preimage and postread verification; mathematical acceptance alone is not evidence that an external table changed. Private native locations, source-library IDs, selected-cell excerpts, canonical-evidence payloads and private native-input fingerprints are excluded. The unchanged second-review Wronskian script requires the separately retained complete original first-review packet for its checksum-binding step; the public derivative is not that input.

## Remaining gates and unchanged conclusions

- F020 remains TO RESEARCH, priority 58, with F023 retained as an alias and no new owner or count.
- Full four-channel paired support remains OPEN58. The separate general endpoint gate remains OPEN53.
- The characteristic-zero overlap theorem is accepted only within its explicit scope. General odd-composite ordinary residual squarefreeness remains separate outside accepted subfamilies.
- Prime-power static scope is b<p. Even root orders, positive-characteristic conclusions and uniform growing-degree conditioning are excluded.
- Historical novelty and worldwide priority remain unverified. Generic Laguerre/CD/quasi-Laguerre machinery is not recast as new.
- FFT operation counts, the exponent kappa, practical performance and production applicability are unchanged.

Any table update must prepend the new scoped result and current-gate clarification while preserving every existing character, formula, note and rich-text run. The repository update must be additive, preserve prior research artifacts, and use a non-force expected-parent check.
