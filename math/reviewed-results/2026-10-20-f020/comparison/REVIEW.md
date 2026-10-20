# Independent bounded attribution review: single-leading-digit family

20 October 2026 UTC.

## Disposition

**ACCEPTED as a scoped source comparison. No correction requested.** This accepts the attribution and non-subsumption wording of the frozen comparison, not historical novelty, literature completeness, or a new audit of the underlying theorem.

Reviewed package: `comparison`.

- `REPORT.md` SHA-256: `986b15c01a608b789a9328eeeee342ec77299bb7e14870a4c0ea03adc90e71c5`.
- `MANIFEST.json` SHA-256 / package seal: `a04690da908ea1b24ad3fa445be21842b9222c5063a7c2659798f1d48c6f3cfb`.
- All ten manifest entries, the seal, and all fourteen supplied source bindings were independently verified. The accepted theorem and its independent mathematical-audit manifests were also verified without alteration.

The theorem input has precisely odd prime p, r>=2, s>r, 1<=c<p, N=p^r, n=cN, and q primitive of order p^s. Its conclusions and acceptance are inputs. This review does not enlarge them to intermediate digits, arbitrary degrees, composite orders, or global F020/F023 closure.

## Independent primary-text inspections

I reopened the six primary/author references used for substantive statement mappings. This was a bounded verification pass, not a repeat broad search. Public extracted text was inspected; no archived remote PDF bytes or usable screenshot evidence is claimed. The inaccessible full texts listed below were not silently classified as excluded.

### A. Sagan and the factorial block residue

[Sagan, *Congruence properties of q-analogs*, Theorem 2.2, printed p. 131](https://users.math.msu.edu/users/bsagan/Papers/Old/cpq-pub.pdf) states the q-Lucas cyclotomic congruence. The preceding paragraph acknowledges earlier proofs and credits the reproduced combinatorial argument to Strehl. The comparison appropriately treats Sagan as an accessible proof, not the first discoverer.

For this application the congruence reads GaussianBinomial(jN,N)=j modulo Phi_N(q). At the target algebraic q, v(Phi_N(q))=N-N/p>0, and evaluation of the integral quotient polynomial preserves reduction. Multiplication for j=1 through d telescopes exactly to (q;q)_(dN)/(q;q)_N^d, giving d!. Nonzero reduction uses d<p. The even-step residue follows additionally from the product of 1+q^i and Frobenius, rather than being attributed as a separate theorem stated by Sagan. The comparison makes this distinction correctly.

This attribution is stronger than calling the residue merely “q-Lucas-like,” but it does not make the full disk theorem a q-Lucas theorem.

### B. Rotated classical Hermite, with two different derivatives

[Koekoek–Swarttouw, Section 1.13](https://arxiv.org/pdf/math/9602214) gives the physicists' Hermite coefficients, recurrence and generating function; Sections 3.26 and 5.26 supply continuous q-Hermite normalization and its Hermite limit. The reference is used correctly for formulas, not historical first priority.

The target coefficient formula indeed equals i^(-c)He_c(iX), or (i sqrt(2))^(-c)H_c(iX/sqrt(2)). Its recurrence is M_c=X M_(c-1)+(c-1)M_(c-2), and its ordinary derivative in X is cM_(c-1). The backward-recurrence coprimality argument is valid when c<p.

In residue characteristic p, however, L=p^(r-floor(r/2)) is divisible by p. The ordinary Y derivative of M_c(alpha Y^L) is zero. This cannot substitute for the separately normalized characteristic-zero ordinary derivative. The report preserves this distinction, including odd-c roots over Y=0. Classical Hermite formulas alone are not represented as proving the mixed-characteristic coefficient reduction or its derivative normalization.

### C. Terminal degree is the order of q, not the target n

[Spiridonov–Zhedanov, Section 2, (2.4)–(2.10), Theorem 1](https://arxiv.org/pdf/q-alg/9605034) explicitly fixes q of primitive order N and analyzes the degree-N polynomial. Simplicity and admissibility conditions (2.8)–(2.9) are material. Its introduction also gives a complex-recurrence example with a multiple zero. The report neither drops those conditions nor promotes terminal information to every lower degree.

[Atakishiyeva–Atakishiyev–Koornwinder, (2.7)–(2.8)](https://arxiv.org/pdf/0811.4100) supplies the terminal Chebyshev and subsequent block formulas for q of order M. The comparison's identification P_n(X)=C_n(X/2|q) agrees with (2.1). Taking M=p^s and n=c p^r<M makes the block exponent zero, so that formula adds no lower-degree assertion. Remark 3.4, (3.8), is a fixed-index q-to-1 Hermite limit. Its presence is acknowledged rather than overlooked, but it is not a stated finite-q residue-characteristic-p estimate for the required disks or ordinary derivative.

This establishes the limited hypothesis mismatch claimed, not an impossibility of finding another classical derivation.

### D. Jackson and ordinary discriminants are distinguished correctly

[Ismail–Witte, Sections 4–5](https://arxiv.org/pdf/math/0012259) defines the ordinary discriminant through the ordinary derivative in (5.12), then a general operator version in (5.13). Theorem 5.2 is genuinely general-operator. The explicit Rogers–Szegő applications (5.16)–(5.17), using (4.23), are Jackson-operator formulas. The report does not incorrectly describe the whole theorem as Jackson-only. Its caution about nonunit orthonormal normalization is appropriate; the q-power variable rescaling is a unit at the target specialization.

For the original monic R_n, an independent exact check verifies D_q R_n=[n]_q R_(n-1) and

    Res(R_n,D_q R_n)=[n]_q^n product_(j=1)^(n-1) (1-q^j)^j.

This formula can also be obtained directly from the Rogers–Szegő recurrence and consecutive resultant, so the report does not depend on silently discarding a normalization factor from (5.16).

### E. Formal generating functions are credited as ingredients

[Cigler, Section 1, (1.10), (1.12), (1.14), (1.16)](https://arxiv.org/pdf/1602.07850) provides the q-exponential functional equation, even product, Rogers–Szegő generating function, and q-binomial theorem used in the map. The parity-Newton expansion follows by multiplying the quotient E(zx)/E(-x) with E(x)E(-x); its ordinary derivative is a further formal manipulation. The comparison correctly does not claim priority for these manipulations. Later badly extracted material is not represented as inspected evidence excluding additional results.

## Independent comparison calculation

Write B=r(p-1)p^(r-1)/2 and D_c=(c+1)N/2+cB-p. For 0<j<n, reflection j to n-j preserves ord_p(j): below level r it follows from n divisible by p^r, and at multiples j=tN it follows from 0<t<c<p. Therefore

    sum_(j=1)^(n-1) j p^ord_p(j) = (n/2) W(n-1),
    W(n-1)=(c-1)N+2cB,
    v([n]_q)=N-1.

The Jackson resultant consequently has valuation

    n(N-1)+(n/2)((c-1)N+2cB)=n(D_c+p-1).

Compared with the accepted ordinary discriminant valuation nD_c, its excess is exactly n(p-1)>0 for every admitted parameter. This is an actual uniform mismatch, not a numerical counterexample outside the theorem's range. It prevents relabeling the Jackson product as the ordinary answer, but does not rule out other applications of Ismail–Witte's general framework.

Independent finite controls use recurrence-built Hermites, exact rational cancellation for q-binomial quotients, symbolic original-polynomial resultants, and a weighted-floor summation different from the author's sequential arithmetic. They check the statement maps, not literature completeness or the accepted theorem. Full counts and executable code are included in this packet.

## Gaps, independence, and permissible conclusion

The four material full-text gaps remain: Lubinsky–Saff (1987), DOI 10.1007/BF01890574; Zhedanov (1997), DOI 10.1142/S0217751X97000438; Mazel–Geronimo–Hayes (1990), DOI 10.1109/29.60115; and Allaway (1980), DOI 10.4153/CJM-1980-053-8. I did not reopen or resolve them during this verification. The report distinguishes fresh failed retrievals from inherited gaps, and neither abstracts nor failed accesses are treated as full-theorem exclusions.

The approved conclusion is exactly bounded: no subsumption of the complete theorem was established in the named inspected statements; substantial ingredients have explicit classical attribution; historical novelty is unestablished. The report's packaging recommendation retains all of these qualifications. Search nonmatches do not clear novelty, and a comparison of named statements does not show that their methods could never be combined to derive the theorem.

The author delivered the frozen bytes before this acceptance. I requested no mathematical or attribution change. No external writes were made. This review changes neither the independent mathematical acceptance nor its scope.
