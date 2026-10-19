# ALG-RS-FAMILIES: moving-root ordinary-discriminant comparison and original-scope disposition

Date: 19 October 2026 UTC. Status: source-bound comparison and closure recommendation, awaiting independent disposition review. No external record was edited.

## Result

The original eleven-family owner has its accepted correctness evidence and no recorded missing mathematical lemma. Its bounded primary-comparison stop is now met: the local overlap discriminant has an exact normalized interface with Sawa–Uchida's quasi-Laguerre theorem; the other named leads have explicit, hypothesis-level matches or qualified nonmatches. None of these comparisons establishes prior publication of the complete moving-root Rogers–Szegő coefficient or the arithmetic family bridge. The exact Zhedanov 1997 article remains an uninspected attribution lead.

Recommend **CLOSED at the original eleven-family theorem plus recorded bounded-comparison scope**, after independent acceptance of this comparison. This is not a worldwide novelty clearance, a new correctness acceptance, or closure of the separate all-composite, arbitrary-base, repeated-prime or numerical/algorithmic questions. The current six augmented bases are preserved separately; they are not folded into the historical eleven.

## 1. Exact owner and stopping condition

The read-only native binding is the workbook Catalogue, row 24 [private native workbook link omitted], stable ID ALG-RS-FAMILIES; the corresponding overview is row 41, and novelty view row 24. The overview is currently TO RESEARCH, priority 42. Its 13 October reconciliation explicitly identifies historical attribution/primary comparison as the leading task and says the accepted scoped correctness proof is not being reopened.

The owner asks for local ordinary-discriminant leading terms and valuation formulas, rather than static factorization alone. Its exact stopping clause is:

> Identify a primary theorem and give an exact hypothesis, formula and cost-model mapping, or record a qualified nonmatch or specific access blocker. Preserve the stated guards; no worldwide-priority, unrestricted runtime or production conclusion.

This is a bounded, disjunctive comparison requirement. It does not require proving an absence of prior art worldwide. The inherited phrase “external novelty unresolved” remains true after this stop is met.

### Accepted original clauses

| Family | Lower bases d | Prime scope | Accepted contents |
|---|---|---|---|
| Separated | 5, 9, 13, 17, 21, 25 | every odd prime p with p not dividing d | 5; 3^8; 13^4; 17^6; 3^11 7^9; 5^17 |
| One overlap | 3, 7, 11, 15, 19 | p = 3 mod 4, p not dividing d for the uniform bridge | 1; 7^2; 11^5; 3^12 5^9; 19^11 |

The target is H_((dp−1)/2)(z; ζ_dp), at every primitive characteristic-zero ζ_dp. Individually accepted certificates add N=25,169 for the original separated p=1 mod 4 statements and N=9,45,49,121,361 for the excluded overlap cases. They do not create a repeated-prime theorem. The later separated corollaries themselves do not supply N=289,63,147,125. Those restrictions are retained even if a separate finite catalogue happens to contain some such targets.

The six augmented bases {3,7,11,15,19,23}, with p=1 mod 4 and p not dividing d, are a later, distinct statement. Their exceptional-pair guard and their different scalar-bank consequence remain unchanged. Eleven is six plus five parameterizations, not eleven independent discoveries.

## 2. Source-bound moving-root target

The accepted author reports and independent reviews were freshly read as text at repository commit 435c181e984aa3389f99f01394a802d8165a74e1. Their exact paths, export hashes, and distinctions from historical original hashes are in SOURCE_BINDINGS.json. The later accepted scope reconciliation and its source manifest were read too. No historical implementation or accepted certificate was executed.

Use the monic unweighted polynomial

    H_n(z;q) = sum_(k=0)^n [n choose k]_q z^k,
    D_n(q) = Disc_z H_n(z;q),
    n=Ad+b, d odd, A>=1, 0<=b<d,
    q(epsilon)=omega(1+epsilon^2)^(1/d), omega primitive of order d,
    F(z)=z^d+1, P_A=product_(j=1)^A j^j.

The binomial branch has constant term one, so q^d−1=epsilon^2 exactly. These are formal fixed-parameter expansions, not an assertion uniform in growing A,d or degree.

### Separated clusters

Set G=H_b(z;omega), Delta=Disc G and R=Res(F,G). Under Delta R !=0, every alpha^d=-1 has first model

    H_n(alpha+epsilon x;q(epsilon))
      =epsilon^A (-1)^A d^(A/2)G(alpha) He_A(sqrt(d)x/alpha)
       +O(epsilon^(A+1)).

The branches start at alpha+epsilon alpha h_j/sqrt(d), with h_j the roots of the monic probabilists' Hermite polynomial. Hence

    K=dA(A−1)/2,
    D_n(q(epsilon))=epsilon^(2K)(C_sep+O(epsilon^2)),
    C_sep=(-1)^[A(d−1)/2] d^[dA(A+1)/2] P_A^d Delta R^(2A).

The residual discriminant, cross-resultant, sign and scaling are part of the target. Static multiplicity alone does not determine this coefficient. Source: [separated author report, sections 2–4](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/47/473ff7c3b3031f3cf9d4ef772a41caa574259cc4299c09c91bb629cdb4307c34__RESEARCH_REPORT.md), [accepted audit, sections 3–5](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/f0/f093175f18d1941a99a605a5d816b1db31e5b2c4161ee7df4bf29291ff8eff3c__INDEPENDENT_AUDIT.md).

### One simple overlap

For odd b write G=(z+1)U, g=U(-1), Delta_U=Disc U, R_U=Res(F,U), and

    W=(omega;omega)_b/(omega^2;omega^2)_((b+d)/2),
    tau=dW/g,
    J_(A+1)(y;tau)=y He_A(y)−A tau He_(A−1)(y)
                 =He_(A+1)(y)+A(1−tau)He_(A−1)(y).

Assume Delta_U R_U Disc J !=0. In particular g is nonzero. The exact overlap model is

    H_n(-1+epsilon x;q(epsilon))
      =epsilon^(A+1)(-1)^(A+1)d^((A−1)/2)g
       J_(A+1)(-sqrt(d)x;tau)+O(epsilon^(A+2)).

Thus

    L=dA(A−1)/2+A,
    D_n(q(epsilon))=epsilon^(2L)(C_ov+O(epsilon^2)),
    C_ov=(-1)^[A(d−1)/2] d^[dA(A+1)/2+A]
         P_A^(d−1) Disc J Delta_U R_U^(2A) g^2.

Replacing J by He_(A+1), or replacing L by K, loses the specific moving-root parameter and is incorrect. Source: [overlap author report, sections 1–3](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/88/886e05ae5a65e8d6516000f90c3821d8a54ca0812167487148b66bbb148cab79__RESEARCH_REPORT.md), [accepted audit, sections 2–4](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/67/671072d1e5b6fe57feaab5c79574535fb17681d99c1007832144121384cf022b__INDEPENDENT_AUDIT.md).

### Cyclotomic and valuation interface

For either exact order h=K or L, divide in Z[q] first:

    D_n=Phi_d^h E, E in Z[q],
    E(omega)=Q_d(omega)^h C, Q_d=(q^d−1)/Phi_d.

The family specialization is A=(p−1)/2, b=(d−1)/2. A<p makes P_A a p-unit. The separated content chooses one residue component where Delta R !=0. The paired overlap content chooses a component where both residual guards at omega and omega^(-1) hold. The identity 1/tau+1/tau*=1 and the accepted characteristic-p lemma then select a simple J when p=3 mod 4. Since Phi_dp=Phi_d^(p−1) modulo p, a zero at a primitive dp-th root would contradict the unit E on that selected component. This remains valid when h>=p−1; no leading-term-only p-adic truncation replaces the integral division.

For the separate conditional content-valuation consequence, define c_t as the positive coefficient gcd of the remainder modulo Phi_t of D_((t−1)/2)(q) Res_z(z^t+1,H_((t−1)/2)(z;q)); set it to zero for the zero remainder. Thus this is the content of a discriminant–resultant product, not of the ordinary discriminant alone. With s=1 mod 4, p=1 mod 4, c_s!=0 and p not dividing s c_s, the accepted exponent is

    L_content=3sA^2/2,
    v_p(c_(sp))=floor(L_content/(p−1))=floor(3s(p−1)/8).

The integral factorization gives a lower bound at every upper prime and equality at one good upper prime; rational content uses the minimum over primes and then the floor. A field norm or a single-prime lower bound does not supply this statement. This valuation is compared as a related accepted consequence, not merged into the family owner's distinct valuation sibling. Sources: [content author report, section 4](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/18/1803504c44766f8545a587a7d6f487d5fa13f2a8a01984e95d4c8dc421f1511e__RESEARCH_REPORT.md), [accepted content audit, sections 4–5](https://github.com/AgentSlop-Si/research/blob/435c181e984aa3389f99f01394a802d8165a74e1/math/archive/objects/10/10afa7335e19e155419b47b7549623d5d76ceb5db8a1cba4c2f045f4a2d46590__INDEPENDENT_AUDIT.md).

## 3. Exact quasi-Laguerre comparison

Primary source: Sawa–Uchida, published Theorem 3.6 and equation (3.6), printed pp.844–845, [published paper](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf). It evaluates the ordinary discriminant of L_m^(alpha)+gamma L_(m−1)^(alpha). The adjacent-Hermite Theorem 3.8 alone is not the correct interface for the degree-gap-two J. Its real-coefficient quasi-orthogonality definition does not license complex-parameter simplicity. The algebraic discriminant identity extends through removable denominators.

The following normalized substitution is an algebraic comparison, already identified by the retained prior comparison review; it is not attributed as a new RS theorem to Sawa–Uchida. The classical identities used are [DLMF 18.7.11, 18.7.19–20](https://dlmf.nist.gov/18.7):

    N=A+1=2m+s, s in {0,1}, m>=1,
    alpha=s−1/2,
    c=(N−1)(1−tau), gamma=−c/(2m),
    Q(x)=(-1)^m m! [L_m^(alpha)(x)+gamma L_(m−1)^(alpha)(x)],
    J_N(y;tau)=2^m y^s Q(y^2/2).

Q is monic. In the original overlap families p=3 mod 4, A is odd, so s=0 and m=(p+1)/4; explicitly gamma=−A(1−tau)/(A+1), alpha=−1/2. The s=1 branch describes the general initial-form identity and the later opposite parity, without merging those owners.

For a monic Q of degree m with roots r_i, the roots of J are the pairs ±sqrt(2r_i), and also zero when s=1. Within-pair squared differences give 8^m product r_i. Between two pairs they give 16(r_i−r_j)^4. The optional zero gives an additional 2^(2m)Q(0)^2. Therefore

    Disc_y J_N=(-1)^m 2^[2m^2+(2s+1)m]
               Q(0)^(2s+1) (Disc_x Q)^2,
    Disc Q=(m!)^[2m−2] Disc(L_m^(alpha)+gamma L_(m−1)^(alpha)).

For completeness, writing V=L_m^(alpha)+gamma L_(m−1)^(alpha), Theorem 3.6 becomes

    xi=[m gamma^2+(2m+alpha)gamma+m+alpha]/gamma,
    Disc V=[product_(k=1)^m k^(k−2m+3)]
           [product_(k=1)^(m−1) (k+alpha)^(k−1)]
           (-gamma)^m V(xi)/(m+alpha+m gamma).

At gamma=0 or a zero displayed denominator, use the polynomial continuation, not a literal division by zero. This formula and the preceding two normalization identities give the exact source-to-Disc J substitution.

These polynomial identities extend to repeated or zero roots. They establish a complete normalization route for the factor Disc J in C_ov, including signs, powers of two, the nonmonic-to-monic conversion and the zero-root factor. Consequently Disc J is not an unexplained new general discriminant object.

They do not identify the RS-specific tau=dW/g, prove the local epsilon^(A+1) occurrence, produce the other factors of C_ov, or establish a unit at a suitable finite-characteristic residue component. No positivity theorem is substituted for Disc J!=0. This is an exact component match and a qualified nonmatch to the complete moving-root/arithmetic theorem.

## 4. Other named comparisons

### Lubinsky–Saff 1987

The [primary record](https://doi.org/10.1007/BF01890574), printed p.332 (1.5)–(1.6), uses G_n equal to the unweighted H_n here. Lemma 4.5/(4.15), p.346, becomes H_(Ad+b)(z;omega)=(1+z^d)^A H_b(z;omega) under (nu,k,l)=(d,A,b). Those exact pages were read as authorized scan images. This proves static degeneration, with no epsilon derivative or first displacement. Its Padé determinant D(M/n) is not Disc_z H_n. No exact moving-root or valuation match is established by those statements.

The later accepted manuscript records access to the complete mathematical body, pp.331–359, and reference p.361. Missing reference p.360 is a bibliography-chain limit, not a missing mathematical-body blocker. This pass does not repeat a complete article audit or infer absence from the missing page.

### Atakishiyeva–Atakishiyev–Koornwinder 2009

In [section 2, equations (2.2), (2.7)–(2.8)](https://arxiv.org/html/0811.4100v2), let v=e^(i theta), z=v^(-2), x=(v+v^(-1))/2. Their continuous q-Hermite H_n^AAK satisfies H_n^AAK(x|q)=v^n H_n^RS(z;q); their lowercase h_n denotes a different q^(-1)-Hermite family. At root order d, (2.8) is exactly the same static factorization after this substitution. Remark 3.4/(3.8) is a fixed-degree q→1 Hermite limit, not a fixed d>1 multi-cluster expansion. The complex-weight orthogonality and Fourier-eigenfunction results do not certify simple half-degree zeros or the normalized ordinary discriminant. Thus the static identity is an exact match; the moving-root/ramified target is a qualified nonmatch to the inspected statements.

### Grosu–Grosu 2020

[Definition 1 and Theorems 2,7,8](https://arxiv.org/pdf/2007.00065v1), PDF pp.2–4, concern partition-indexed Wronskian Hermite polynomials, irreducibility and congruences. Theorem 8 assumes an odd modulus coprime to the degree-sequence Vandermonde. It does not state the RS moving parameter or coefficient.

An exact narrow comparison is available: from their definition and the Hermite recurrence,

    He_(A,1)(y)=Wr(He_1,He_(A+1))/A
              =y He_A(y)+He_(A−1)(y)=J_(A+1)(y;−1/A).

This is a special fixed tau, not the full J family. At the actual half-residual characteristic-zero RS parameters, tau*=conjugate(tau) and 1/tau+1/tau*=1; the negative real value −1/A is incompatible. In characteristic p with A=(p−1)/2 it equals 2, exactly the delicate paired parameter; source characteristic-zero irreducibility does not transfer nonvanishing modulo p. No match to the required one-good-residue-component lemma or valuation coefficient has been established.

### Ismail–Witte 2001: the invariant check

[Equations (1.7)–(1.9), (4.20), and (5.16)–(5.18)](https://arxiv.org/pdf/math/0012259v2), PDF pp.2–3,21,24, distinguish ordinary and q-discriminants. Their RS normalization is H_n^IW(z|q)=H_n^RS(q^(-1/2)z;q). Correcting that variable scaling does not change D_q into the ordinary derivative. For a quadratic az^2+bz+c, the q-invariant is qb^2−(1+q)^2ac, while the ordinary invariant is b^2−4ac. Even where the coefficients analytically continue, the first is not a formula for D_n(q). The displayed product is an invariant-level nonmatch, so it cannot discharge the local orders or arithmetic bridge.

### Derivative and root-of-unity citation leads

[Schultz–Walker, Theorem 1.1](https://arxiv.org/pdf/1202.0199v1), PDF p.3 with primitive choices p.13, supplies mixed derivative vanishings: set the odd product kc=d, polynomial weight to the jth falling factorial, ordinary q-derivative order r, and auxiliary exponent/divisibility parameter zero. Its threshold becomes 2r+j<A. The surviving initial polynomial and its discriminant coefficient are not specified by this vanishing conclusion.

[Gorodetsky, Propositions 8.1–8.2](https://arxiv.org/pdf/1805.01254v2), PDF pp.23–24, gives first and second ordinary q-derivatives of Gaussian coefficients. The second requires the root order to divide both indices. These fixed-order coefficient formulas do not supply the all-A, all-residual cluster polynomial or a cyclotomic valuation of its ordinary discriminant.

[Zudilin, Lemma 1/(9)](https://arxiv.org/pdf/1901.07843v2), PDF pp.3–4, expands weighted Gaussian coefficients with both indices divisible by the root order through cubic radial order. The formal conversion is eta=1−(1+epsilon^2)^(1/d), with source root order d. The residual b of H_(Ad+b) is not its lower quotient index. The fixed-order expansion is a bounded antecedent, not the all-A local coefficient. No inward-radial interpretation is imposed on a positive-real epsilon path.

[Spiridonov–Zhedanov, section 2/(2.4)–(2.8)](https://arxiv.org/pdf/q-alg/9605034v2), PDF p.3, treats terminal degree equal to root order. The simplicity caveat on PDF p.2 explicitly separates complex recurrence data from positive orthogonality. Neither terminal-degree zeros nor complex discrete weights imply the half-degree RS assertion. This is a different paper from Zhedanov 1997, DOI 10.1142/S0217751X97000438; that six-page body has not been inspected here and is not used negatively or as a proof dependency.

### Arithmetic reference

[Sharifi, Propositions 3.1.20–3.1.21](https://math.ucla.edu/~sharifi/notes/algnum-ch03.html) give the integral cyclotomic ring and prime ramification. With source n=sp and p not dividing s, ramification index is p−1. These support the accepted min-valuation-to-content conversion. They do not evaluate the RS element or establish its exact exponent. That ingredient-level match leaves the displayed conditional RS content valuation without an exact external antecedent identified in this bounded comparison.

## 5. Cost-model and hypothesis conclusion

All comparisons above concern exact polynomial identities, formal characteristic-zero germs, or explicitly guarded arithmetic reduction. Their use supplies no runtime comparison with an FFT. The accepted family proof uses a uniform theorem plus fixed-base data, rather than enumerating all target orders. It provides no uniform efficient root-construction, numerical stability, growing-degree analytic certificate, production execution, or unrestricted inverse-bank optimum.

The scalar-bank consequence remains confined to scalar coefficients, one natural cycle, first-order resolvents with distinct nonzero legal nodes and one free diagonal, with the existing congruence/resonance condition. The opposite-congruence augmented families do not yield the smaller bank count.

## 6. Original-scope disposition

The original owner's positive theorem clauses are supported by accepted proofs and finite fixed-base inputs; the accepted reconciliation explicitly records no remaining lemma for the stated families. The remaining native task was a bounded model-matched source comparison. Sections 2–5 perform it at the moving-root level and preserve exact nonmatches and access limits. The original stopping criterion is satisfied without inventing a new base, demanding an all-composite result, or requiring a worldwide negative-priority proof.

Accordingly, close only ALG-RS-FAMILIES at this original scope once this report passes independent disposition review. Keep priority 42 and the existing B/unverified historical-novelty classification unchanged. Preserve all historical source text and links. Do not change F020/F022, Q29, ALG-OPEN-UNIFORM-SQUAREFREE, ALG-RS-CONTENT-VALUATION, arbitrary-base support, or other siblings merely because their family label overlaps.

Preserved external limits: Zhedanov 1997 full-text comparison and broader citation chaining remain uncompleted; LS87 reference p.360 remains missing. These are explicit historical-priority qualifications, not a mathematical defect in the eleven accepted families or a failure of the owner's allowed qualified-nonmatch/access-blocker stop.

## 7. Verification and publication boundary

Performed: fresh native owner read, pinned repository text reads, exact source-content hashing, accepted scope/review reading, relevant primary theorem text inspection, LS87 authorized-page image inspection, and written normalization/root-product comparison. The web PDF image tool returned cache misses for Sawa–Uchida and Ismail–Witte; their relevant indexed text was readable, and no rendered-image verification is claimed.

Not performed: any historical or accepted-program replay, new fixed-base computation, certificate rerun, owner mutation, publication, or proof/novelty upgrade. The publication allowlist contains only authored reports, the comparison matrix, source bindings, stop criterion, and manifest. Licensed source PDFs, scans, page images, raw paper bodies and private native snapshots are excluded.
