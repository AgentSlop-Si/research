# Hermite overlap: bounded comparison with classical sources

12 October 2026 UTC. Historical priority remains unresolved.

## Conclusion and limits

The overlap polynomial is a classical Hermite parity combination and becomes an adjacent-Laguerre combination after a quadratic substitution. Its repeated-root elimination point agrees exactly with the evaluation point in Sawa–Uchida's quasi-Laguerre discriminant formula. The annulus follows by combining that elimination identity with an elementary finite-dimensional endpoint-Jacobi trace bound.

These observations support describing the annulus as an elementary consequence of established methods. They do not identify its first publication, establish worldwide originality, or settle priority for its Rogers–Szegő specialization. The source comparison is a bounded attribution synthesis; the separately accepted mathematical result is the [trace proof](overlap-trace-proof.md).

## 1. Normalization and exact family correspondence

Use He_0=1, He_1=x and He_(n+1)=x He_n-n He_(n-1), and let

    J_(A+1)(x;tau)=x He_A(x)-A tau He_(A-1)(x).

Write A+1=2r+s, s in {0,1}, and alpha=s-1/2. For the standard generalized Laguerre polynomial L_j^alpha, define

    p_j(u)=(-1)^j j! L_j^alpha(u),
    Q(u)=p_r(u)+(A/2)(1-tau)p_(r-1)(u),
    c_0=A(tau-1)/(2r).

Then p_j and Q are monic, and

    Q(u)=(-1)^r r! [L_r^alpha(u)+c_0 L_(r-1)^alpha(u)],
    J_(A+1)(x;tau)=2^r x^s Q(x^2/2).

The variable u=x^2/2 here differs from the determinant variable y=x^2 in the trace proof. These formulas are the comparison's explicit change of variables.

## 2. Quasi-Laguerre discriminants

[S1] Masanori Sawa and Yukihiro Uchida, “Discriminants of classical quasi-orthogonal polynomials with application to Diophantine equations,” Journal of the Mathematical Society of Japan 71 (2019), 831–860, DOI 10.2969/jmsj/79877987. [Publisher PDF](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf).

Theorem 3.6, printed pp.844–845 (PDF pp.14–15), equation (3.6), treats L_r^alpha+c_0 L_(r-1)^alpha and evaluates it at

    xi=r c_0+2r+alpha+(r+alpha)/c_0.

This is the direct family antecedent. Theorem 3.8 concerns adjacent Hermite degrees instead. Proposition 2.7 assumes a real coefficient and cannot establish the present nonreal-parameter simplicity. Apparent denominator singularities in the discriminant formula require polynomial continuation rather than unguarded substitution.

Our substitution, using A+1=2r+s, gives

    2xi=A(tau-1)+(2A+1)+(A+1)/(tau-1)
       =A tau+(A+1)+(A+1)/(tau-1)
       =tau(1+A tau)/(tau-1).

Thus 2xi equals the eliminated value x^2 at a nonzero repeated root. The same location follows directly from J=J'=0, as proved in the trace note. This is an exact specialization of the known framework, not an unrelated discriminant mechanism.

For completeness, the quadratic root-product calculation also gives

    Disc_x J=(-1)^r 2^(2r^2+(2s+1)r)
             Q(0)^(2s+1) [Disc_u Q]^2.

To see the powers, write the roots of Q as u_i. Each pair ±sqrt(2u_i) contributes 8u_i, each pair of such pairs contributes 16(u_i-u_j)^4, and the additional root zero when s=1 contributes 4u_i^2 for each i. Multiplying and using product_i u_i=(-1)^r Q(0) proves the identity, first for distinct nonzero roots and then polynomially for all coefficients. The factor Q(0) must be retained. A repeated root at zero requires tau=0 for odd A or tau=-1/A for even A, so it is excluded for nonreal tau.

## 3. Dissipative Jacobi antecedents

[S2] Yury Arlinskiĭ and Eduard Tsekanovskiĭ, “Non-self-adjoint Jacobi matrices with rank one imaginary part,” arXiv:math/0602033, inspected 58-page version. [Primary PDF](https://arxiv.org/pdf/math/0602033).

Theorem 2.3 on p.8 attributes a root-subspace trace criterion to Livsic; section 2.2 on p.10 explicitly counts algebraic multiplicities. Proposition 3.1, pp.19–21, supplies characteristic-polynomial recurrences and generalized-eigenvector chains. Proposition 4.1, pp.26–27, gives the endpoint dissipative-Jacobi setting. Reversing coordinate order matches a last-diagonal perturbation. These are methodological antecedents; the elementary finite-matrix proof here needs no completeness theorem or Jordan chain.

For M=B+A(tau-1)e_r e_r^T, the direct identity Im(lambda)/(A Im(tau))=|u_r|^2/||u||^2 gives strict positivity at every eigenvalue. The trace sums these ratios with algebraic multiplicity to one. A repeated eigenvalue has ratio at most one half. Signed normalization handles both half-planes. Combining this with the eliminated value proves the same annulus as the earlier Jordan-chain route.

For comparison, the earlier route uses complex symmetry and a chain (M-yI)w=u to obtain u^T u=0, hence |u_r|^2<=sum_(j<r)|u_j|^2. The trace replacement avoids that chain while preserving the result. Neither route establishes historical priority for the displayed annulus.

## 4. Hermite congruence and classical normalization

[S3] Codruț Grosu and Corina Grosu, “The irreducibility of some Wronskian Hermite polynomials,” arXiv:2007.00065v1. [Primary PDF](https://arxiv.org/pdf/2007.00065v1).

Page 2 fixes the probabilists' monic normalization. Theorem 31 on p.18 states and proves He_(n+m)(x) congruent to x^m He_n(x) modulo every odd m>=3, for n>=0, and explicitly attributes the result to Carlitz. Reference [7], p.33, identifies the original paper. This is an inherited arithmetic antecedent, separate from the nonreal metric annulus.

[S4] NIST Digital Library of Mathematical Functions, [section 18.7](https://dlmf.nist.gov/18.7), equations 18.7.11 and 18.7.19–20. These give the Hermite normalization conversion and even/odd Hermite–Laguerre identities with alpha=-1/2 and +1/2. The quadratic identities are credited there to Szegő (1975), equation (5.6.1).

[S5] Leonard Carlitz, “Congruence properties of the polynomials of Hermite, Laguerre and Legendre,” Mathematische Zeitschrift 59 (1954), 474–483. [Bibliographic record](https://eudml.org/doc/169405).

The original body remains unread. The prior comparison located bibliographic metadata, but opening that record failed; this addendum does not repeat that access attempt or claim original-source verification. The congruence attribution is through the inspected Grosu–Grosu statement and reference.

## 5. Rogers–Szegő specialization and contribution wording

The application uses the original parameter tau=dW/g with

    H_b(z;q)=sum_(j=0)^b [b choose j]_q z^j,
    g=H'_b(-1;q),
    W=product_(j=1)^b(1-q^j)
      /product_(j=1)^((d+b)/2)(1-q^(2j)).

Here the underlying application has odd d>b, odd b, and q a primitive order-d root in characteristic zero. The coefficient [b choose j]_q is the Gaussian binomial polynomial. Denominator and derivative nonvanishing must be justified before forming tau. The quadratic-family comparison does not provide those guards, establish the local occurrence of this parameter, or certify that its value lies in a sufficient region. Those remain duties of the separate Rogers–Szegő arguments and exact certificates.

The annulus concerns all complex nonreal tau and every A>=1; b is not the degree of J, which is A+1. At a primitive root, a successful metric bound at one suitable conjugate can prove algebraic discriminant nonvanishing at all conjugates because, for fixed A, the discriminant lies in Q[tau]. This transports nonvanishing, not the metric inequality itself.

The established ingredients are the Hermite–Laguerre reduction, adjacent-Laguerre discriminant evaluation, Carlitz congruence through its inspected later presentation, and endpoint-Jacobi recurrence and spectral methods. Repeated-zero guards, the rational elimination value, the annulus and its uniform sufficient regions are elementary consequences in this framework. Potentially distinctive Rogers–Szegő content includes the normalized parameter, its local occurrence, and the guarded all-A applications. Historical priority of that content remains unverified.

A bounded description is: “We apply classical quasi-Laguerre discriminant identities and a finite-Jacobi spectral bound to the explicit Rogers–Szegő overlap parameter tau=dW/H'_b(-1;q), obtaining the separately stated all-A nonvanishing ranges. Historical priority of the exact Rogers–Szegő formulas and applications remains unresolved.”

## 6. Evidence boundary

The public URLs and page-specific passages for S1–S4 were reopened during preparation of this addendum. Verification concerns extracted primary text and page labels; no comprehensive visual inspection of entire PDFs is claimed. The original comparison also used bounded targeted searches. A search with no matching result is not evidence of novelty. S5 remains a metadata-only reference with an unread body.

This note does not enlarge any previously accepted family, certify worldwide originality, infer quantitative conditioning or a universal good-prime result, or support an FFT improvement. It includes neither full third-party papers nor their code. Earlier scientific reports remain unchanged.
