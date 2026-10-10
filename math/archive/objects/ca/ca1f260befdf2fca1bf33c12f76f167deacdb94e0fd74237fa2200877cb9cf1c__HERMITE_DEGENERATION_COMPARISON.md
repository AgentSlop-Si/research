# Bounded primary-source comparison: shared Hermite cluster

Checked 2026-10-10. Inputs read without modification: the overlap report §§2–3 and the previous primary-source ledger. This is a comparison of actual displayed formulas, not an exhaustive priority determination.

## Bottom line

The polynomial form

J_(A+1)(y;τ) = He_(A+1)(y) + A(1−τ)He_(A−1)(y)

is a standard order-two quasi-orthogonal Hermite combination (for real parameters; its complexification is the same algebraic expression). The plausible narrowly new object is its **specific fixed-root, shared-cluster origin and normalization**, including τ = dW/g, rather than a new Hermite family. None of the exact formulas inspected below supplies that origin or its ordinary-discriminant coefficient. This does not establish publication priority.

## 1. Continuous q-Hermite: exact factorization, different Hermite endpoint

M. K. Atakishiyeva, N. M. Atakishiyev, T. H. Koornwinder, *On a q-extension of Mehta's eigenvectors of the finite Fourier transform for q a root of unity*, arXiv:0811.4100v2, §2, (2.1),(2.2),(2.7),(2.8), and Remark 3.4, (3.8), were inspected in the primary PDF:
https://arxiv.org/pdf/0811.4100

Write C_n(X|q) for their continuous q-Hermite, and R_n(z;q) for the input report's Rogers–Szegő H_n. Equation (2.2) gives the exact normalization

C_n((s+s^−1)/2|q) = s^−n R_n(s²;q).

Their (2.8) states

C_(Ad+b)(X|ω) = [2T_d(X)]^A C_b(X|ω), 0≤b<d.

This is precisely R_(Ad+b)(z;ω)=(1+z^d)^A R_b(z;ω) after the substitution. Thus the degenerate factorization is an exact antecedent, not a candidate novelty.

Equation (3.8) is a q→1 Hermite limit. In the input's probabilists' normalization it becomes

lim_(q→1) (1−q)^(-n/2) C_n(√(1−q)y/2|q) = He_n(y).

It is neither a perturbation of a fixed ω≠1 nor the first nonzero coefficient at a shared residual root.

**Direct normalization check (our calculation).** At z=−1 choose s=i, giving X=0; dX/dz=1/(2i). Consequently z=−1+εx means X=−iεx/2+O(ε²). The proposed y=−√d x is a blow-up around this fixed terminal Chebyshev node. Setting q=ω exactly in (2.8) loses all information about the off-root coefficient that defines J. Combining (2.8) with the q→1 endpoint does not by itself justify exchanging these two different limits.

## 2. Askey–Wilson: terminal root equation, not repeated-cluster blow-up

V. Spiridonov and A. Zhedanov, *Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity*, arXiv:q-alg/9605034v2, §2, (2.1)–(2.8), inspected:
https://arxiv.org/pdf/q-alg/9605034

For a primitive Nth root, their terminal polynomial is

P_N(x)=t^N+t^−N−E_N, x=t+t^−1,

E_N=[a^N+b^N+c^N+d^N−(abc)^N−(bcd)^N−(abd)^N−(acd)^N]/[1−(abcd)^N].

Equation (2.6) gives its nodes r q^s+r^−1q^−s; (2.8) requires E_N≠±2 for simplicity. The continuous q-Hermite parameter limit has E_N→0 and gives 2T_N(x/2). The factor of two in the variable distinguishes this normalization from C_n above. Section 1 expressly warns that complex recurrence coefficients do not ensure simple roots.

**Scope distinction.** These equations determine the degree-N terminal node set. The candidate concerns degree Ad+b>N and the splitting of its repeated node at z=−1 under q^d−1=ε². No such first nonzero shared-cluster coefficient was established from these inspected equations.

## 3. Generalized/Dunkl Hermite: parity-wide deformation differs from J

R. Álvarez-Nodarse, M. K. Atakishiyeva, N. M. Atakishiyev, *A q-extension of the generalized Hermite polynomials with the continuous orthogonality property on R*, International Journal of Pure and Applied Mathematics 10(3) (2004), 335–347; primary author-hosted manuscript, (1.1),(1.4),(2.7),(2.9),(4.16), inspected:
https://renato.ryn-fismat.es/papers/2004-IJPAM-q-gen-her.pdf

Their classical H_n^(μ) has weight |x|^(2μ)e^(−x²), μ>−1/2, and recurrence

2xH_n^(μ)=H_(n+1)^(μ)+2(n+2μθ_n)H_(n−1)^(μ), θ_n=n mod 2.

In the input's monic scale G_n^(μ)(y)=2^(−n/2)H_n^(μ)(y/√2), this is

yG_n^(μ)=G_(n+1)^(μ)+(n+2μθ_n)G_(n−1)^(μ).

Their (2.9) takes their generalized q-Hermite family to H_n^(μ) as q→1; it does not perturb Rogers–Szegő at a fixed odd root. Equation (1.1) identifies its even and odd parts with single Laguerre polynomials having parameter μ∓1/2.

**Algebraic distinction (our calculation).** J is obtained by retaining ordinary Hermite polynomials through degree A and changing only the final recurrence coefficient A to Aτ. Generalized/Dunkl Hermite changes every odd-index coefficient. In the fixed monic scale, J_2=y²−τ and J_3=y³−(1+2τ)y; G_2^(μ)=y²−(1+2μ) and G_3^(μ)=y³−(3+2μ)y. Matching both forces τ=1 and μ=0. Thus J is not this generalized Hermite family under a common parameter identification in the stated normalization. This does not exclude isolated degree-specific coincidences or separately chosen rescalings.

## 4. Uglov: simultaneous two-parameter Macdonald limit

Denis Uglov, *Yangian Gelfand–Zetlin Bases, gl(N)-Jack Polynomials and computation of Dynamical Correlation Functions in the Spin Calogero–Sutherland Model*, arXiv:hep-th/9702020, §4, equations (4.29)–(4.44), especially (4.32),(4.38),(4.39), inspected:
https://arxiv.org/pdf/hep-th/9702020

For γ>0, (4.32) takes

q=ω_N p, t=ω_N p^γ, p→1,

in symmetric Macdonald polynomials P_λ(x_1,…,x_n;q,t). The coefficientwise limit is P_λ^(γ,N), with monomial-triangular expansion (4.39). Equation (4.38) explicitly computes the limiting box factor: it is [a_λ(s)+γl_λ(s)+γ]/[a_λ(s)+γl_λ(s)+1] when N divides the hook length and 1 otherwise. Orthogonality for γ=Nβ+1 is (4.44).

**Scope distinction.** Taking N=d and p=(1+ε²)^(1/d) matches the candidate's q path, but simultaneously prescribes a second parameter t→ω_d and does not move any polynomial variable toward a coalescing root. The inspected construction is an unscaled coefficientwise limit, not the ε^(−A−1) local limit of R_(Ad+b)(−1+εx;q). No explicit specialization/limit identity was found that makes it the proposed J origin. Shared use of a root of unity is insufficient to identify the two constructions; the comparison does not rule out a future deeper relation.

## 5. Recent fixed-root measure limit also has a different output

Dan Dai, Mourad E. H. Ismail, Xiang-Sheng Wang, *From continuous to discrete: weak limit of normalized Askey–Wilson measure* (2024), §5 and Lemma 5.1, (5.1),(5.2), inspected in the author original:
https://userweb.ucs.louisiana.edu/~xxw6637/papers/RJ2024.pdf

The q-Hermite specialization has limiting mass points cos[π(r−1/2)/n], with weights calculated from a second solution p_n* and its Stieltjes–Wigert expression (5.2). This is a fixed-root degeneration and therefore relevant context. Its stated output is a terminal discrete measure, not a high-degree shared-cluster splitting polynomial or derivative-discriminant leading coefficient.

## Boundary and recommended wording

Recommended claim: “The root-of-unity factorization and Hermite limiting mechanisms have classical antecedents. We derive the explicit leading polynomial at a simple shared residual root, identify it as a quasi-Hermite combination, and obtain the associated ordinary-discriminant order and coefficient.” Do not call J a new generalized/Dunkl Hermite family, or infer originality from searches not returning the exact formula.

The parent is separately checking quasi-Laguerre discriminants, including the parity reduction of J. That is a closer algebraic antecedent than the generalized-Hermite or Uglov labels considered here.

Searches covered q-Hermite/Rogers–Szegő root-of-unity splitting, coalescing zeros, generalized Hermite limits, and Uglov's original construction. Relevant equations were read in primary PDF text, rather than abstracts. Some screenshot attempts returned cache-miss errors; extracted text supplied the equations reported above. The previously denied Vanderbilt /texts/76.pdf route was not requested, and no alternative was used to circumvent that denial. This bounded pass does not clear the outstanding Zhedanov *Gauss sums and orthogonal polynomials* full-text priority check recorded by the parent.
