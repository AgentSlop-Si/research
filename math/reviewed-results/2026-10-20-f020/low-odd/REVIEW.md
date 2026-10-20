# Independent adversarial audit: the low-digit squarefreeness extension

20 October 2026 UTC. This audit supplied no proof lemma. The author received an adverse exact control showing why a stronger whole-disk derivative claim would be false, but the author's proof already used root-dependent elimination and retained that restriction. The independent checkers in this package import neither the author's checker nor an earlier checker. No external state was mutated.

## 1. Verdict and exact accepted scope

**PASS**, with no mathematical revision requested, for the frozen candidate identified below.

Let p be an odd prime, r>=2, s>r, N=p^r, 0<=2c<p, n=N+2c, and q a characteristic-zero primitive p^s-th root. Normalize v(q-1)=1 and use the ORIGINAL recurrences

    P_0=1, P_1=X,
    P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_a [j choose a]_q z^a.

Write h=floor(r/2), beta=p^h, B=r(p-1)p^(r-1)/2, and D=N+B-p. The audited unlimited theorem is:

- Exactly 2c roots of P_n have valuation 1/2. Their original ordinary derivative values have valuation (n-1)/2.
- The remaining N roots have valuation >1/2 and lie in the accepted beta disks centered at x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta. Their original ordinary derivative values have valuation D+c.
- H_n has the corresponding partition by v(z+1)=1/2 or >1/2, and the same ordinary derivative valuations at the corresponding roots.
- Every root is simple. Both ordinary discriminants have valuation N(D+c)+c(n-1).
- At every P_n root xi, the ORIGINAL algebraic-square kernel sum_(j<n) P_j(xi)^2/(q;q)_j is nonzero.

This is precisely the odd-degree family with leading digit 1, no intermediate digits, and even low digit <p. It does not settle even degrees, larger leading digits, intermediate digits, arbitrary degree below p^s, or general odd composite orders. It changes no global F020/F023 ownership, historical-priority, cost, or all-A assertion. The c=0 case is the already accepted pure-power result.

The accepted author REPORT.md SHA-256 is

    47c704223199772787ac255f23bbe7eda83c0c627d57b73579299a547f060354

and the accepted author MANIFEST.json SHA-256 is

    2214a0ef237d03d3f94c9c3e7edb87e889070554dd57d79d05f70c5835f7fb5d.

## 2. Ordinary identities, parity, and the outer roots

The Newton expansion runs over k congruent to the degree modulo 2. The k=0 term is present for even degree. Its ordinary derivative is the full double sum stated in the candidate, with no q derivative or differentiation of a repeated residual substituted for the ordinary derivative. I reconstructed both parities directly from the original H recurrence at four rational q values, alongside the exact H/P Laurent identity and the full polynomial algebraic-square Christoffel-Darboux identity.

For lambda^2=-(q-1), the scaled original P recurrence is integral and reduces to the monic Hermite recurrence with coefficient j. In characteristic p, He_p=Y^p. At the beginning of each successive block the recurrence coefficient ap vanishes, so the same recurrence gives He_(ap+d)=Y^(ap)He_d, including the endpoint needed to begin the next block. Thus the residual for n=N+2c is Y^N He_(2c).

The factor He_(2c) has no zero root because its constant term is the nonzero unit (-1)^c(2c-1)!!. Its ordinary derivative is 2c He_(2c-1), and the downward recurrence proves coprimality because 2c<p. Consequently its 2c roots are simple. Simple-root lifting is applied only to those nonzero residual roots. It is not applied to the repeated residual factor Y^N. All N remaining roots, counted with multiplicity at this point, lie strictly inside the scale v(X)>1/2.

At a lifted outer root the scaled derivative is a unit, giving the claimed derivative valuation (n-1)/2. This is an actual ordinary derivative computation, with the scale factor included.

## 3. Replacement root covering

The old pure-power monic-term comparison cannot simply be reused for mixed digits. The author correctly changes the comparison term to k=N. Its coefficient has weight c.

For k=N+2a, each added factor z+q^j has weight >1/2 at an inner point, while the coefficient ratio has weight -a. Their sum is strictly positive. For k=N-2u, the reflection is still performed below the PURE POWER N, where it is valid. The accepted consecutive-distance estimate gives the strict lower bound

    N-beta+c-W(u+c)+R_h(2u-1).

The complementary-tail identity is also invoked with N, not with n. It reduces the required estimate to

    W(u+c)+R_h(N-2u)
      <=W(u+c)+W((N-1)/2-u)
      <=W((N-1)/2+c)=B+c.

The final equality holds because adding c produces no carry in the low base-p digit. In particular, every added integer is prime to p. The resulting bound is nonnegative, and the preceding strict distance estimate makes every competing term strictly larger. The comparison term itself cannot vanish outside the disks. This proves complete covering of all N inner roots without assuming their simplicity.

Closed disks are necessary, just as in the pure-power theorem. The strictness comes from the distance comparison, not from a false assertion that every integer bound is strictly positive. The reduction to beta center representatives is valid because center differences divisible by beta have valuation at least beta.

## 4. The neighboring even-degree polynomial

The lemma for P_(N-1) is properly restricted to these disks, rather than asserted throughout v(X)>=1. Its even-degree H expansion retains the k=0 term of valuation B. Every positive even k term has strictly larger weight because R_h(k)<W(k/2) and W is superadditive. The normalized polynomial consequently has a constant unit residual, so its value has weight B at every disk point, not merely generic points.

For the ordinary H_(N-1) derivative, every double summand has weight at least B. If m is even, j=k-m is even and the estimate W(j/2)>=p^ord_p(j) suffices. If m is odd, j is odd and the less obvious step is

    ord_p((N-j)/2)=ord_p(j),
    W((N-j)/2-1)+p^ord_p(j)=W((N-j)/2)<=B.

These are exact because 0<j<N=p^r. No unavailable strict digit estimate for odd m is assumed. Transferring to P introduces only analytic unit factors and a differentiated prefactor times H_(N-1), itself of weight B. Thus both required P bounds hold.

## 5. Root-dependent elimination and its necessity

The shifted-tail continuant identity

    P_(N+d)=A_d P_N-(1-q^N)B_d P_(N-1)

has the correct initial conditions B_0=0 and B_1=1. For d=2c<p, every shifted internal edge has weight 1. The even tail A_d has a unique constant perfect-matching term of weight c, while every positive power is strictly larger throughout the inner disks. Hence A_d is nonzero there. The ordinary coefficient estimates give B_d/A_d of weight >=0 and its ordinary derivative of weight >=-1.

Differentiating before evaluating, then using P_n(xi)=0, gives the candidate's exact root identity. The perturbation inside the brackets has weight at least N+B-1=D+p-1, strictly greater than the pure-power derivative's weight D. There is therefore no leading cancellation, and multiplication by A_d gives weight D+c.

This is a claim AT ROOTS, not a constant residual statement for P_n' or H_n' over the entire disk. The distinction is material. Independent exact arithmetic at p=3, r=3, s=4, n=29 shows that H_29'(-1+t^3Y) has constant coefficient of weight 52=D+c, but its Y^3 and Y^9 coefficients have weight 46, and its Y^4 and Y^10 coefficients have weight 48. Thus a direct whole-disk derivative extension would fail. This adverse control is preserved in ACTUAL_FIELD_CHECKS.json. It does not contradict the theorem, because those arbitrary disk points are not asserted to be H_29 roots.

The independent actual-field checker instead constructs, directly from the original H recurrence and the even shifted tail A(z),

    E(z)=A(z)H_n'(z)-A'(z)H_n(z).

It checks that A has constant unit residual at weight c, and E has constant unit residual at weight D+2c. At an H_n root this is a direct certificate for derivative weight D+c. This is an audit computation of the existing root-elimination mechanism, not a proof lemma supplied to the author.

## 6. Actual ramification, coordinate maps, discriminants, and kernels

All theorem inequalities use exact v(1-q^j)=p^ord_p(j) for 0<j<p^s. No characteristic-p truncation is used to assert a mixed-characteristic equality, and there is no hidden requirement D<v(p).

The independent actual-field implementation constructs H in Z[q]/Phi_(p^s), reduces each coefficient to degree less than e=phi(p^s), and converts that exact representative to t=q-1 by the binomial formula. The weights j+e ord_p(c_j), for 0<=j<e, are pairwise distinct modulo e. Their minimum is therefore exact even at or above ramification. Residue units retain p/t^e -> -1. In particular, the N=81, p=3, s=5 controls have D=186>e=162 and include every beta=9 center.

For the coordinate transfer, all P roots reduce to zero and all H roots reduce to -1. On the branch v0 near i, X=v0+v0^(-1), z=v0^2, and z+1=v0 X. Both ordinary coordinate derivatives are units because p is odd. The branch gives a bijection of the relevant small neighborhoods, preserving root multiplicities and ordinary derivative valuations. The roots do not meet the ramified points corresponding to X=+/-2. This validates both the partition and equality of the two discriminant valuations.

The discriminant argument uses the monic product of the ordinary derivative at every root. The kernel argument uses the exact algebraic-square CD identity, not positivity. Consecutive original P polynomials cannot share a root because all relevant recurrence edges are nonzero; a common root would propagate to P_0=1. The nonzero derivative and nonzero denominator then give the claimed kernel nonvanishing. No common valuation for all kernel values is inferred.

## 7. Independent controls and explicit scope barriers

The independent files contain:

- Exact both-parity Newton/ordinary-derivative, original H/P, and full algebraic-square CD identity checks for degrees 0 through 15 at q=2,3,-2,1/2.
- Integer-bound checks at all six primes 3,5,7,11,17,31 and all r from 2 through 20, with every admissible c; exhaustive small grids plus fixed-seed boundary/random samples. There are 114 parameter rows, each with 3000 neighboring ordinary-derivative checks.
- Exact finite-field nonzero-resultant certificates for every degree below the nine orders 9,25,27,49,81,121,125,243,343, using a second reduction when the first is bad. These establish characteristic-zero nonvanishing for those finite controls only. A bad reduction is not treated as a characteristic-zero counterexample. H and P need not have the same bad reductions because the coordinate map can ramify at unrelated reduction primes.
- Exact mixed-characteristic original-recurrence disk controls, including the neighboring polynomial bounds and the root-elimination certificate, with both below- and above-ramification cases. ACTUAL_FIELD_CHECKS.json gives every tested parameter, center, coefficient weight, and residue unit.

The finite-field implication is rigorous: if the characteristic-zero resultant vanished at a primitive root, the monic cyclotomic polynomial would divide the integer resultant polynomial. Every primitive finite-field specialization would then make it vanish. A coprime modular reduction therefore certifies nonvanishing. No finite grid is used to justify the unlimited theorem.

The negative integer controls also independently confirm the reported scope barriers. The old monic root-cover bound at even b=p^2+1 equals -p, and at odd b=3p^2 for p>=5 it equals -p^2. The first excluded low digit c=(p+1)/2 creates a carry deficit p-1. For odd tail length the required tail polynomial is odd and vanishes at zero, so the same division argument does not uniformly cover the central disk. These are limitations of this proof, not counterexamples to squarefreeness.

## 8. Frozen-byte verification and reproducibility

verify_frozen.py checks the exact report/manifest hashes quoted above, all 10 author-manifest file lengths and hashes, the exact file inventory, the manifest seal, and equality of all retained accepted sources with their original local bytes. The full author package is retained under sources/author-final. The author checker was replayed in an isolated temporary directory. Every recorded mathematical value agreed after removing elapsed-time fields. The original author package was checked again and remained unchanged.

CANDIDATE_VERIFICATION.json and AUTHOR_REPLAY.log record these results. Run the four independent checkers and verifier with Python 3; no third-party packages, network access, numerical root solving, or floating-point arithmetic are required for the mathematical controls. MANIFEST.json and SEAL.sha256 bind this completed review package.
