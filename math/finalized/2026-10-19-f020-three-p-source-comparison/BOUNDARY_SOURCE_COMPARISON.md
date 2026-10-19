# Targeted source comparison: the degree 3p boundary

Checked 19 October 2026. **No directly subsuming result was found in the inspected statements. Historical priority remains unresolved.** This is a bounded applicability comparison, not another correctness review or an exhaustive literature search.

## Exact target

Let p be an odd prime, s≥1, q have exact order p^s, and 3p<p^s. The accepted result proves ordinary characteristic-zero squarefreeness of

    P_0=1, P_1=X, P_(n+1)=X P_n−(1−q^n)P_(n−1)

and of the actual Gaussian Rogers–Szegő polynomial at n=3p. For p≥5, in Q_p(q) with v(q−1)=1, every root ξ satisfies v(P'_(3p)(ξ))=3p−2, hence

    v(Disc_X P_(3p))=3p(3p−2).

The degree-2p factor whose roots have valuation (2p−1)/(2p) is irreducible. For p=3 the conclusion is squarefreeness of P_9 for every s≥3, proved separately; neither the displayed valuation nor that factor description is asserted. The incremental degree is exactly 3p. Nothing here concerns b>3p or all composite root orders.

## 1. Terminal root-of-unity formulas still stop at a different degree

Atakishiyeva–Atakishiyev–Koornwinder, *On a q-extension of Mehta’s eigenvectors of the finite Fourier transform for q a root of unity*, §2, equations (2.1)–(2.3), (2.7)–(2.8), PDF pp. 3–4, supplies the same continuous q-Hermite recurrence after X=2x. Its terminal identity uses M=ord(q), and its factorization is H_(kM+r)=(2T_M)^k H_r for 0≤r<M. At 3p<M, this gives k=0, r=3p: the unresolved polynomial is unchanged. At p=3, M=9 the terminal identity is available, but that case is expressly outside 9<3^s.

Source: https://arxiv.org/pdf/0811.4100

## 2. Finite orthogonality does not supply the missing lower-degree simplicity

Spiridonov–Zhedanov, *Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity*, introduction, §2 and Theorem 1, PDF pp. 1–4: the zero formula and its simplicity restriction concern degree N=ord(q). The introduction explicitly makes simple terminal zeros an additional requirement for complex recurrence coefficients. Its finite orthogonality formulas therefore do not by themselves prove that a lower-degree P_(3p) has simple zeros or that its ordinary-square diagonal Christoffel–Darboux kernel is nonzero. The accepted theorem's derivative nonvanishing supplies that additional information at this degree.

Source: https://arxiv.org/pdf/q-alg/9605034v2

## 3. The explicit Rogers–Szegő product is a different discriminant

Ismail–Witte, *Discriminants and Functional Equations for Polynomials Orthogonal on the Unit Circle*, equations (1.7)–(1.9), (4.20), (5.12)–(5.17), PDF pp. 2–3, 21, 23–24: (4.20) uses the Gaussian family with variable scaled by q^(−1/2). The explicit product (5.17) is D(H_n,q), built from the q-difference operator, whereas the ordinary discriminant uses the ordinary derivative in (5.12). Substituting n=3p leaves this distinction intact. The paper's general operator theorem is broader; using it for the target would still require an ordinary-derivative lowering formula and evaluation establishing the claimed valuation.

An elementary diagnostic from its displayed quadratic formula: for f(z)=(z−1)^2, its q-discriminant is 4q−(1+q)^2=−(q−1)^2, nonzero when q≠1, while the ordinary discriminant is zero. Thus nonvanishing of that product cannot alone certify ordinary squarefreeness.

Source: https://arxiv.org/pdf/math/0012259v2

## 4. Additional author exposition identifies the same operator distinction

Ismail, *Functional Equations and Electrostatic Models for Orthogonal Polynomials*, MSRI Publications 40 (2001), pp. 225–244, Definition 5.1 and Theorem 5.2 on p. 239, and the continuous q-Hermite discussion on p. 242: the generalized discriminant is a resultant with a chosen degree-lowering operator. The continuous q-Hermite application uses the Askey–Wilson divided-difference operator. This is not the ordinary derivative. It corroborates the precise distinction, not a theorem for the degree-3p cyclotomic valuation. This author-written exposition cites the then-forthcoming work later published in 2003; it does not replace inspection of that original.

Source: https://library.slmath.org/books/Book40/files/ismail.pdf

Access qualification: the pertinent indexed primary-source passages were readable; direct PDF text extraction was garbled and screenshots failed. Claims here are limited to those passages.

## 5. A recent simple-zero statement changes both parameter and polynomial

Mao–Wang–Zheng, *Interlacing on the Unit Circle via Coefficientwise Reciprocals*, arXiv:2609.34551v1, Theorem 1.1 (p. 2), Example 4.4 and Remark 4.5 (p. 12): the Rogers–Szegő application uses a real parameter t∈[0,1] and applies a gamma-coefficient sign change followed by coefficientwise reciprocation. The simple-zero/interlacing conclusion concerns the resulting family T_n. Remark 4.5 separately discusses the original family for 0<t<1. Neither statement directly addresses the original Gaussian polynomial at a primitive p^s-th root or its p-adic ordinary discriminant. This is a primary preprint, not a claim of peer-reviewed acceptance.

Source: https://arxiv.org/pdf/2609.34551 (opened PDF identifies itself as v1)

## 6. What remains family-specific at the new boundary

The earlier comparison already checked general Newton-side, Hensel, and discriminant-product/cluster tools. They apply after the needed coefficient estimates and residual separation have been established. At this boundary the accepted calculation supplies, for p≥5,

    P_(3p)(ρY)/ρ^(3p) → Y^p(Y^(2p)−3),
    P'_(3p)(ρY)/t^(3p−2) → 3c(Y^(2p)−1),
    P_(3p)(tY)/t^(3p−1) → −3(Y^p+cY),

where t=q−1, ρ^(2p)=t^(2p−1), and c=(−1)^((p+1)/2). The first residual is inseparable, so its root count alone does not prove simplicity. The derivative residual has value 6c at its nonzero roots, and the inner residual has derivative −3c; both are units only in the asserted p≥5 case. These are the exact family-specific inputs whose prior attribution remains to be established. The separate p=3 cyclotomic certificate is not replaced by any inspected terminal or quantized-discriminant formula.

## Remaining coverage limits and publication wording

- Zhedanov, *Gauss Sums and Orthogonal Polynomials* (1997), DOI 10.1142/S0217751X97000438: publisher landing/PDF retrieval failed. The original remains unread. https://doi.org/10.1142/S0217751X97000438
- Ismail, *Difference equations and quantized discriminants for q-orthogonal polynomials* (2003), *Advances in Applied Mathematics* 30, 562–589: the publisher abstract was readable but full-text retrieval failed. No theorem-by-theorem exclusion is claimed. https://www.sciencedirect.com/science/article/pii/S019688580200547X
- Lubinsky–Saff, *Convergence of Padé approximants of partial theta functions and the Rogers–Szegő polynomials* (1987), 331–361: the author publication list supplied the official PDF link, but it could not be retrieved in this pass. This additional zero-distribution lead remains unread, with no applicability conclusion. https://www.math.vanderbilt.edu/saffeb/texts/76.pdf

Safe wording: “The inspected root-of-unity terminal formulas and quantized-discriminant statements do not directly subsume the degree-3p ordinary-squarefreeness and normalized ordinary-discriminant result. The family-specific residual calculation has not been attributed to a directly matching prior statement in this bounded check; historical priority remains unresolved.”

No full papers, extensive quotations, external writes, or repository changes are included in this packet.
