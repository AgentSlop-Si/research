# Public derivative notice

Private native locations and source-library identifiers have been removed. The mathematical review and its original-input hashes are retained. SCIENTIFIC_PROVENANCE_EXCERPT.sha256 is a redacted list of original scientific entries, excluding the private canonical-evidence fingerprint; MANIFEST.sha256 binds this distributed derivative. The original uploaded PDF/ZIP are not distributed here.

# Independent review: odd-prime Rogers–Szegő discriminants

17 October 2026 UTC

## Decision

**ACCEPT within the stated characteristic-zero scope.** The proof removes the overlap guards for every odd root order and every odd residual, and removes the remaining static guards for odd prime powers with residual below the underlying prime. The composition with the retained version-3 local theorem is valid. No mathematical repair to the principal theorem or its coefficient formulas was identified.

This is an independent mathematical acceptance of this extension, not a historical-priority determination or a canonical promotion. No external research files were changed and no uploaded program was executed.

## Exact accepted statements

Let H_n(z;q)=sum_{k=0}^n [n choose k]_q z^k and let D_n(q) be its ordinary z-discriminant, with Disc(1)=Disc(monic linear)=1.

For every odd prime p and n=Ap+b, A>=0, 0<=b<p,

    ord_{Phi_p(q)} D_n(q) = p*A*(A-1)/2 + A*(b mod 2).

For d=p^s, p odd prime and s>=1, the same formula with d in place of p is accepted **only for n=Ad+b with 0<=b<p**. This review does not replace b<p by b<d.

Separately, for every odd d>=3, every primitive dth root omega, every odd 1<=b<d and every A>=1, the forced-root derivative g_b is nonzero and J_{A+1}(x;tau_b) is squarefree. For general odd composites, this removes only the g and J guards; the other static guards remain unless independently certified.

The statement at A=0 follows from the static theorem. The boundaries n=0,1 and b=0,1 are correctly treated. The original FFT objective, operation counts, and exponent kappa are unchanged. Even root order, positive-characteristic conclusions, and uniform growing-degree conditioning are outside this acceptance.

## Proof audit

### 1. Overlap parameter

Differentiating the classical RS recurrence at z=-1 gives the stated recurrence for g_{2r+1}. Its normalization by (q^2;q^2)_r yields the partial sum S_r. At a primitive odd root, all denominators used are nonzero. Cancellation in W_b and H_d(z;omega)=1+z^d give tau_b=S_h/S_r, h=(d-1)/2.

The principal-embedding phase t_k=a_k exp(-ik*pi/d), a_k>0, lies in a sector strictly narrower than pi/2. Thus S_r is nonzero. The displayed double sum for Im((S_h-S_r) conjugate(S_r)) is strictly negative because r<h and all sine factors are positive. This proves nonreality. Cyclotomic automorphisms commute with conjugation, so nonreality and nonvanishing pass to every primitive embedding. The supplementary complementary-residual identity has the required conjugation bar; the PDF's text extraction can obscure it, but the LaTeX source includes it.

### 2. Exact 2-adic valuation

The two parity recurrences and their scaling by pi^2=2 are correct. Their reductions obey rho_{m+1}=X rho_m+(m mod 2)rho_{m-1}, hence rho_m=X^(m mod 2)(X^2+1)^floor(m/2). The chain-rule factor pi^(-2m+2) in the scaled Wronskian is correct.

Reduction of the derivative Wronskian is (X^2+1)^(m-1). Consequently the scaled Wronskian is monic, integral, and has unit constant coefficient. A root X cannot have positive or negative valuation, by the unique-minimum term argument. Therefore every root y of either original Wronskian satisfies v_2(y-1)=1/2. Equivalently, its shifted Newton polygon has endpoints (0,m-1) and (2m-2,0), with all coefficient points on or above the segment. The m=1 case is the constant polynomial 1 and is handled separately.

### 3. Collision exclusion

At a nonzero repeated J-root, consecutive Hermite coprimality permits elimination and gives

    (tau-1)*x^2 = tau*(A*tau+1).

Tau=1 is impossible in characteristic zero. Thus y=x^2 belongs to the same unramified field as tau. Parity reduction and elimination force the relevant Wronskian to vanish at y. Its half-integer valuation contradicts the integer valuation group of an unramified extension.

At zero, the exact exceptional parameters are tau=0 for odd A and tau=-1/A for even A. The odd cyclotomic field embeds in an unramified extension at 2; the RS parameter is nonreal and avoids both rational exceptions. The field hypothesis is essential: the exact negative control A=3, tau=(-1+2*sqrt(-2))/3 gives

    J_4(x;tau) = (x^2-(1+sqrt(-2)))^2.

This nonreal parameter lies in a ramified 2-adic field. Nonreality alone would not justify a general collision-exclusion theorem.

### 4. Static prime-power theorem

The exact substitution q=1+t^2, z=-1+tx yields H_b=t^b K_b with K_b integral and monic and K_b(x,0)=He_b(x). The discriminant scaling is correct and gives

    D_b(q)=(q-1)^[b(b-1)/2] V_b(q),
    V_b(1)=product_{j=1}^b j^j.

If Phi_{p^s} divided V_b, evaluation at 1 would force p to divide that product, contradicting b<p. The fixed-node quotient arguments similarly give nonzero constants (-1)^r b!! for odd b=2r+1, and (-1)^r(2r-1)!! for even b=2r. Monic division ensures integral quotient polynomials. The conclusion includes the derivative at the forced root.

The restriction b<p is a restriction of this proof and accepted statement. This review does not claim that every excluded residual is a counterexample.

### 5. Composition and normalization

The report's local initial forms and complete coefficients (20)–(23) match the retrieved version-3 Section 3 formulas, including the sign, powers of d, P_A, resultant powers, g^2, and the ordinary discriminant of J. The retrieved October-11 overlap review explicitly covers b=1,3 only. It is a valid formula baseline, but it is not the latest canonical project state; the reconciliation below is required before any promotion.

The coefficient C is in the parameter q^d-1. The required conversions are

    lim D_n(q)/(q-omega)^M = C*(d*omega^(-1))^M,
    [D_n/Phi_d^M](omega) = C*(d*omega^(-1)/Phi_d'(omega))^M.

For d=p^s, (q^d-1)/Phi_d(q)=q^(d/p)-1 exactly, so the final expression becomes C*(omega^(d/p)-1)^M. No local coefficient has been silently substituted into a different parameter.

## Fresh exact controls

Only newly written reviewer programs were executed. The uploaded ZIP's programs were treated as inert data.

`fresh_algebra_controls.json` records:

- 100 parity-Wronskian controls, both families for m=1,...,50, constructed from the factorial formula for Hermite coefficients. All shifted Newton bounds, endpoint valuations, and scaled mod-pi coefficients pass.
- 67 exact characteristic-zero static checks over Q(omega): all b<p for d=3,5,7,11,13,17,9,25,27. Both squarefreeness and the appropriately deflated fixed-factor gcd pass. An optional d=49 gcd test was interrupted for computational cost; no result is claimed for that control.
- 153 exact partial-sum/derivative/normalization/nonreality checks: every odd d from 3 through 35 and every odd b<d.
- 100 rational-parameter collision controls for A=1,...,20, including both exceptional parameters, tau=1, and two additional rational parameters.
- 50 integral fixed-node quotient checks, b=0,...,9 and j=0,1,3,7,11.
- The exact ramified-field negative control above.

`fresh_coefficients/` contains a separate implementation of actual ordinary-discriminants using the reciprocal reduction and a Bezout determinant over Q(omega)[[t]], with q=omega*(1+t). It checks the leading coefficient independently of its proposed formula. Controls include:

| (d,A,b) | n | Exact order M |
|---|---:|---:|
| (7,1,5) | 12 | 1 |
| (7,2,5) | 19 | 9 |
| (7,2,4) | 18 | 7 |
| (9,1,2) | 11 | 0 |
| (9,2,1) | 19 | 11 |
| (9,2,2) | 20 | 9 |
| (3,3,0) | 9 | 9 |
| (3,3,1) | 10 | 12 |

Every listed control matches C*d^M in the t-parameter and the exact cyclotomic quotient conversion. Seven full Z[q] discriminants in degrees 3–8 independently agree with the local engine and proposed formulas. These tests check normalization; the unlimited ranges rest on the written proofs above.

## Literature status

Historical novelty remains unverified. The published Sawa–Uchida Theorem 3.6 is indeed the adjacent quasi-Laguerre discriminant formula, and the parameter identification in the report is correct. It should not be presented as a new general discriminant formula. Primary source: https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf (printed pp. 844–845).

Grosu–Grosu Theorems 7–8 explicitly use primes greater than 2 and odd moduli respectively, as the report says. Those statements do not directly give the shifted 2-adic result. Primary source: https://arxiv.org/pdf/2007.00065 (p. 4).

An additional relevant comparison for a future publication audit is Sawa–Uchida, *Algebro-geometric aspects of the Christoffel–Darboux kernels for classical orthogonal polynomials*, Transactions AMS 373, 1243–1264. Its Section 4 uses Newton polygons, including half-integer slopes, to obstruct rational zeros of quasi-Hermite polynomials. Its stated result is different from the parity-Wronskian valuation lemma here; this is a relevant neighboring source, not a priority clearance or a demonstrated duplicate. Author manuscript: https://da.lib.kobe-u.ac.jp/da/kernel/90009429/90009429.pdf.

The report's statement that a Lubinsky–Saff (1987) full-body comparison is missing is stale against the current project record. The previously completed canonical F020 literature comparison records that the full mathematical body was already checked. It classifies the RS recurrence/self-reciprocity, root-of-unity factorization, static multiplicities, and derivative restatements as classical, while preserving exact moving-z splitting, ordinary-discriminant coefficients, and guarded arithmetic as narrow candidates with priority unverified. This audit did not retrieve and recheck that body anew: the official publisher page exposed a subscription preview and the author bibliography's PDF link did not load. Neither that access failure nor the new mathematical acceptance reverses the earlier comparison.

The remaining recorded historical-source gaps are journal reference page 360/citations 9–36, full-text comparison with Zhedanov (1997), and broader exact local-discriminant and arithmetic priority review. The newly identified Sawa–Uchida Christoffel–Darboux paper above should also be compared specifically with the shifted parity-Wronskian lemma before asserting originality. Historical novelty is therefore **UNVERIFIED**. Sources: https://link.springer.com/article/10.1007/BF01890574 and https://my.vanderbilt.edu/edsaff/research-articles/ (item 76).

## Canonical reconciliation and promotion gate

The existing canonical owner is **F020**, “Local ordinary discriminants at odd roots of unity,” with F023 retained as an alias. The recorded project state was inspected on 17 October 2026. Private table locations and native excerpts are omitted from this public derivative.

That state already includes accepted fixed-residual all-A overlap families through b=31, as well as separate accepted general derivative-nonvanishing and separation inputs. The present all-odd-b squarefreeness theorem for J extends beyond that finite fixed-residual coverage and gives a uniform alternative proof in the already accepted subfamilies. Do not characterize it as only an advance from b=1,3, erase those later acceptances, or count the already accepted g/separation results as new project discoveries.

The current F020 parent remains TO RESEARCH, priority 58; the full paired-support gate is OPEN 58 and the general endpoint gate OPEN 53. The newest linked October-16 acceptance concerns bounded low-order cyclotomic deflation, a different part of the project: https://github.com/AgentSlop-Si/research/blob/a462b0f54fc0e05da1fe689b7d1de665bd147944/math/finalized/2026-10-16-research-finalization-1722/f020/REPORT.md. The present report proves characteristic-zero overlap squarefreeness and the specified prime-power static subfamily. It does not, by itself, prove the separate all-m paired-support or endpoint assertions, nor arbitrary odd-composite ordinary residual squarefreeness.

**Before promotion:** reconcile the manuscript's historical project baseline and literature-access statement as above, preserve the existing canonical owner/history and independent gates, and obtain the separately requested next-stage review of this frozen packet. This mathematical acceptance does not authorize a status, priority, novelty, repository, or canonical-record change. No such change has been made.

## Source integrity of the original reviewed inputs

The complete nine-page standalone report was read. The ZIP's report, LaTeX, README, component proofs, and recorded data were inspected without running uploaded code. All 14 manifest entries match their archived bytes.

The standalone report and ZIP report have different PDF bytes, but their full pdftotext -layout outputs are identical. The standalone PDF is therefore not assumed to be byte-identical to the archived PDF; both identities are retained below.

- Standalone report source identity retained privately. SHA-256 aa8f0a979e8194aafc9124cdf8427992f65aacdc3ec6319baf0eb3b7b88c1ae5.
- Companion ZIP source identity retained privately. SHA-256 d96217c6afdd197258d5e535f93c83a4a8fcaa762283b26adb25deeb6224ca6f.
- Archived PDF SHA-256 62ae0621ebd46bd8e93d98dfb6ae1bb1ffec3c3b0322b50c691612919ec70f74.
- Retrieved prior version-3 source: [private source locator omitted].
- Retrieved accepted b=1,3 review: [private source locator omitted].

No canonical file, external repository, or publication record was changed by this review.
