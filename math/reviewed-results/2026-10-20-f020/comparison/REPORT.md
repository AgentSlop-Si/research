# Bounded source comparison: the single-leading-digit theorem

20 October 2026 UTC. Read-only literature work; no external write. The accepted mathematics is an input to this comparison, not re-audited here.

## Disposition

**No subsumption of the complete theorem was established in the named statements inspected. Historical novelty is not established.** Substantial ingredients are classical: the Rogers–Szegő/continuous-q-Hermite recurrence and coordinate identity, the Hermite polynomial itself and its recurrence/derivative, q-exponential identities, q-Lucas block units, Newton-polygon root counting, and Christoffel–Darboux. Public packaging should distinguish these from the specific mixed-characteristic coefficient estimates and ordinary-derivative calculation.

The most concrete additional attribution finding is that the block factorial residue is an immediate q-Lucas consequence, not merely reminiscent of one. The classical Jackson discriminant still disagrees numerically with the ordinary discriminant, for every accepted leading digit.

## Exact comparison target

Let p be odd, r>=2, s>r, N=p^r, n=cN, 1<=c<p, q primitive of order p^s, and v(q-1)=1. Set B=r(p-1)p^(r-1)/2 and D_c=(c+1)N/2+cB-p. The original polynomials are

    R_n(z)=sum_j [n choose j]_q z^j,
    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1).

Here R denotes the author's Rogers–Szegő H, avoiding collision with classical Hermite notation. Acceptance covers squarefreeness, v(R_n')=v(P_n')=D_c at every root, ordinary discriminant valuation nD_c, and nonzero original algebraic-square CD kernel at every P_n root.

The sharper target uses h=floor(r/2), beta=p^h, L=N/beta, and rho=beta/2 for even r or p^(h-1)(2p-1)/2 for odd r. Each disk v(z+q^a)>=rho, 0<=a<beta, contains cL roots. Even c puts all on the boundary; odd c puts L strictly inside and (c-1)L on the boundary. On each disk the polynomial and separately normalized **original ordinary derivative** reduce respectively to

    M_c(alpha Y^L),   c M_(c-1)(alpha Y^L),   alpha != 0,
    M_c(X)=c! sum_k X^(c-2k)/(2^k k! (c-2k)!).

The derivative normalization is C_1 omega^(c-1), where omega^2=(q;q)_N and C_1=(q;q)_N/[(q^2;q^2)_((N-p^2)/2)(1-q^(p^2))]. Its valuation is D_c. These exact hypotheses and normalizations are material.

## Named statement maps

### 1. Terminal root-of-unity results: still a different degree

Spiridonov–Zhedanov, Section 2, (2.4)–(2.10) and Theorem 1, treats the terminal degree equal to the order of q, with its explicit parameter and simplicity conditions. The introduction expressly warns that complex recurrence coefficients do not guarantee simple zeros. In the target, n=c p^r<p^s. Substituting n for their terminal degree would change the order hypothesis. No general lower-degree simplicity conclusion follows from the inspected terminal theorem. [Author primary text](https://arxiv.org/pdf/q-alg/9605034).

Atakishiyeva–Atakishiyev–Koornwinder, Section 2, (2.7)–(2.8), gives C_Q=2T_Q and C_(aQ+b)=(2T_Q)^a C_b for q of order Q. Here P_n(X)=C_n(X/2|q) and Q=p^s. Since n<Q the block factorization is tautological at a=0. Their Remark 3.4, (3.8), also states the classical q-to-1 Hermite limit. It preserves the fixed polynomial index and concerns an analytic limit, not the finite-q, residue-characteristic-p disk reduction of index c. It supplies no stated coefficient error bound yielding the target radii, counts or D_c. [Author primary text](https://arxiv.org/pdf/0811.4100).

### 2. Classical Hermite content: credit it, but do not confuse the two derivatives

With probabilists' Hermite He_c, the exact identity is M_c(X)=i^(-c) He_c(iX). Equivalently M_c=(i sqrt(2))^(-c) H_c(iX/sqrt(2)) in physicists' normalization. Thus its coefficients, recurrence and derivative are classical Hermite facts, not a new polynomial family. Koekoek–Swarttouw's author reference gives the physicists' coefficients, recurrence and generating function in Section 1.13, continuous q-Hermite in 3.26, and the fixed-degree limit in 5.26. This is a classical formula reference, not an assertion of first historical priority. [Author reference](https://arxiv.org/pdf/math/9602214).

The finite-characteristic inference is elementary from those identities: for c<p, the backward recurrence proves gcd(M_c,cM_(c-1))=1. But L is divisible by p, so the derivative in Y of M_c(alpha Y^L) is zero. Consequently classical Hermite separability cannot justify differentiating that repeated residual. The nonzero second residual must come from the separate characteristic-zero ordinary-derivative calculation. Neither the fixed-degree limit nor Hermite separability alone supplies it.

### 3. q-Lucas actually covers the basic factorial block unit

Sagan, Theorem 2.2, states the Gaussian-binomial congruence modulo Phi_d(q). It has earlier antecedents explicitly acknowledged in that paper; cite it as an accessible proof, not as a first discovery. [Primary text, p. 131](https://users.math.msu.edu/users/bsagan/Papers/Old/cpq-pub.pdf).

Apply it with d=N: [jN choose N]_q congruent to j modulo Phi_N(q). At the target q,

    v(Phi_N(q))=v((1-q^N)/(1-q^(N/p)))=N-N/p>0.

For j<p these binomials therefore reduce to nonzero j. Multiplying their exact factorial expressions gives

    (q;q)_(jN)/(q;q)_N^j -> j!.

Likewise (q^2;q^2)_(tN)/(q;q)_N^t -> 2^t t!, using product(1+q^i) and 2^(tN)=2^t in characteristic p. These are classical consequences. The partial shifted block uses the elementary higher-valuation comparison for (1-q^(2tN+2i))/(1-q^(2i)); no novelty is asserted for that device. None of these facts alone establishes the disk cover, identifies every tied derivative term, or proves that their actual units sum to the required Hermite residual.

### 4. Exact generating-function ingredients are also classical

Cigler's Section 1 gives the q-exponential functional relation (1.10), product (1.12), Rogers–Szegő generating function (1.14), and q-binomial theorem (1.16). These are enough, by coefficient comparison, to obtain the accepted parity-Newton expansion. Ordinary formal differentiation then gives the displayed double sum. The literature comparison should not claim either formal manipulation as a new identity without a separate priority analysis. The issue addressed by the accepted proof is the valuation/equality/unit analysis after specialization. [Author text](https://arxiv.org/pdf/1602.07850).

Only these clearly extracted formulas are used here. Some later formulas in this PDF have poor text extraction; they were not reconstructed speculatively or treated as excluding further results. The separate Cigler overview on continuous q-Hermite was scanned only as a lead, not used as an additional theorem exclusion.

### 5. Jackson discriminant: a quantitative mismatch for all c

Ismail–Witte's general-operator Theorem 5.2 is not restricted to Jackson operators, but its explicit Rogers–Szegő products (5.16)–(5.17) are. Equation (5.12) separately uses the ordinary derivative. Finite algebraic specialization preserves this operator distinction. Their q-power change of variable is a valuation unit, but the orthonormal scaling need not be. [Primary text, Sections 4–5](https://arxiv.org/pdf/math/0012259).

For the original monic R_n, the exact Jackson lowering and consecutive resultant give

    Res(R_n,D_q R_n)=[n]_q^n product_(j=1)^(n-1)(1-q^j)^j.

Here is the general-c comparison, derived directly. Reflection j -> n-j preserves ord_p(j), because c<p. Also v([n]_q)=N-1 and W(n-1)=(c-1)N+2cB. Hence

    v Res(R_n,D_q R_n)
      =n(N-1)+(n/2)W(n-1)
      =n[(c+1)N/2+cB-1]
      =n[D_c+p-1].

The accepted ordinary value is nD_c. The gap is exactly n(p-1)>0. Thus simply relabeling the Jackson product gives the wrong answer at every target parameter, not just outside the target family.

## What the inspected results do and do not cover

- The Hermite formula, q-Lucas/basic block units, classical recurrence, generating functions and CD identity are covered ingredients.
- Standard Newton-polygon counting gives the stated multiplicities **once** the actual integral normalized polynomial has the proved reduction. Counting roots from a reduction is not itself a new principle. The substantive input is the coefficientwise reduction and the complete cover. In particular, simple-root Hensel lifting is not applicable to the repeated Y residual.
- The inspected named statements do not establish that input, the ordinary-derivative pivot/equality set, the normalized derivative residual, or the exact every-root value D_c.
- The kernel conclusion follows from ordinary derivative nonvanishing plus consecutive coprimality through classical CD; it should not be described as an independent new CD identity.
- This is a comparison of stated results and valid applications, not proof that the theorem could not be derived by another combination of classical methods.

## Bounded gap list

1. **Lubinsky–Saff (1987)**, DOI 10.1007/BF01890574: material because it concerns unit-modulus q. The author bibliography was reopened; its exact 1987 PDF link again failed. The linked 1986 four-page announcement also failed. Full theorem statements remain uninspected. [Author bibliography](https://my.dev.vanderbilt.edu/edsaff/research-articles/), [publisher](https://link.springer.com/article/10.1007/BF01890574).
2. **Zhedanov (1997), Gauss Sums and Orthogonal Polynomials**, DOI 10.1142/S0217751X97000438: the publisher retrieval again failed. The prior bibliographic verification stands; full text remains uninspected. [Publisher](https://www.worldscientific.com/doi/abs/10.1142/S0217751X97000438).
3. **Mazel–Geronimo–Hayes (1990)**, DOI 10.1109/29.60115, and **Allaway (1980)**, DOI 10.4153/CJM-1980-053-8: inherited full-text gaps, not reclassified or excluded by this extension. No fresh full-theorem claim is made about either.
4. The targeted additions inspect accessible q-Lucas and classical-Hermite formulas, not every arithmetic q-Hermite paper, every language, every source cited by those authors, or later developments. No search nonmatch is evidence of novelty.

No access restriction was bypassed. PDF screenshots were unavailable or unhelpful; a direct arXiv byte-download attempt returned HTTP 403 and was not retried. The evidence is inspected public text and exact local calculations, not a claim of archived remote PDF bytes.

## Packaging recommendation

Suggested wording:

> We prove the stated single-leading-digit mixed-characteristic theorem using classical Rogers–Szegő/q-Hermite identities, q-Lucas-type block congruences, Hermite recurrences and Newton-polygon counting. A bounded comparison with the named accessible sources did not identify a theorem subsuming the complete disk-and-original-ordinary-derivative statement. Historical priority is not claimed, and material named full-text gaps remain.

Do not promote this result to arbitrary intermediate digits, arbitrary degrees below p^s, odd-composite orders, or global F020/F023 closure. Existing independent mathematical acceptance remains unchanged.

The accompanying checker verifies 16 Hermite normalization/discriminant cases, 14 exact q-Lucas congruence cases and 102 general-c valuation-gap cases. These are finite transcription controls, not a completeness search or another proof audit. SOURCE_BINDINGS.json identifies the exact accepted inputs.
