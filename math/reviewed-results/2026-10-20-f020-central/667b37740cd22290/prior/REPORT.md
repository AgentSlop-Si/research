# F020 adjacent degree: n = 2 p^r + 1

20 October 2026 UTC. Bounded author candidate, frozen for separate fresh review. No external writes and no edits to prior packages.

## 1. Outcome and exact scope

Let p be an odd prime, r >= 2, s > r, N = p^r, and q a characteristic-zero primitive p^s-th root. Work in an algebraic p-adic embedding with v(q-1)=1. The ORIGINAL polynomials and normalization are

    P_0=1, P_1=X, P_(j+1)=X P_j-(1-q^j)P_(j-1),
    H_j(z)=sum_a [j choose a]_q z^a,
    w_j=(q;q)_j, Q_j=(q^2;q^2)_j.

Put

    B=r(p-1)p^(r-1)/2, h=floor(r/2), beta=p^h, L=N/beta,
    rho=beta/2                         if r is even,
    rho=p^(h-1)(2p-1)/2               if r is odd,
    E=N/2+2B, D_2=N+E-p, n=2N+1.

The bounded result has two parts.

1. For EVERY r>=3 in this family, both original H_n and P_n are squarefree and the original algebraic-square Christoffel-Darboux kernel is nonzero at every P_n root. At the exact P_n root 0, the ordinary derivative has valuation W(N)=N+2B. At every nonzero P_n root xi, put x=v(xi). Then

       v(P_n'(xi)) = x + min(D_2, N+E-2x).

   The identical derivative valuations transfer to corresponding H_n roots. This is explicitly not an all-root constant-derivative statement.

2. For r=2, the same proof establishes the exact zero root and every noncentral cluster, but it encounters a UNIFORM ACTUAL CANCELLATION on the central nonzero cluster. This is a precise obstruction to this derivative-separation/residual-coprimeness mechanism, NOT a counterexample to squarefreeness. Precisely 2p roots, counted with multiplicity, remain outside the proof of simplicity. No unrestricted r>=2 theorem is asserted.

The root geometry is proved for ALL r>=2, before assuming simplicity. Define

    x_a=i(q^(a/2)-q^(-a/2)), 0<=a<beta, i^2=-1,

using square roots of q^a congruent to 1. In addition to its exact zero root, P_n has exactly 2L roots in each disk v(X-x_a)>=rho, and ALL these 2L roots lie on the boundary. The zero root is simple and is in the strict interior of the central disk. Thus the central disk contains 2L+1 roots of P_n including zero, while the other disks contain 2L roots each. Corresponding H_n disks have centers -q^a, and the exact zero maps to z=-1.

For r=2, put t=q-1, choose mu with mu^2=t^p, and epsilon=(-1)^((p-1)/2). For the actual polynomial F=P_(2p^2+1)/X, the two coefficientwise reductions are

    F(mu Y)/t^(N+2B) -> 1+Y^(2p) = (Y^2+1)^p,
    F'(mu Y)/(t^(3B) mu^p)
        -> -2 epsilon Y^(p-2)(Y^2+1).                    (1.1)

F' here is the ORIGINAL ordinary derivative taken in characteristic zero, before reduction. Its residual has common factor Y^2+1 with the F residual, and vanishes at both nonzero residual locations. This shows exactly why the leading certificate fails for all 2p central roots. The missing step is a deeper characteristic-zero ordinary-derivative analysis above those two repeated residual locations, or another uniform argument proving those central roots simple. Neither a finite check nor a second assertion of separation supplies that step.

No arbitrary leading/intermediate digits, arbitrary n<p^s, odd-composite orders, global F020/F023 closure, FFT speed, complexity improvement, or novelty claim follows. No cost model is changed; this is only an algebraic root/kernel gate.

## 2. Actual sources and imported accepted facts

The restored public comparison package is hash-bound by its top-level MANIFEST.json and SEAL.json. Its accepted leading-c report, accepted leading-two report, and relevant independent reviews were read as actual files, together with the even-low-digit report. Source copies and their exact public-byte hashes are recorded in SOURCE_BINDINGS.json. Historical nested manifests can refer to pre-publication bytes; they are not silently treated as hashes of the projected public copies.

The leading-two proof gives, for every r>=2, the following statements on the rho disks in H coordinates:

- H_(2N) has coefficientwise weight W(N)=N+2B. Its normalized disk residual has degree 2L, nonzero constant coefficient, and form a+bY^(2L), with a,b nonzero.
- H_(2N)' has coefficientwise weight at least D_2 and has exact weight D_2 at every point of every boundary. Its residual is a nonzero multiple of Y^L.
- With N_k(z)=product_(j=0)^(k-1)(z+q^j), define

      W(m)=sum_(j=1)^m p^ord_p(j),
      T(m)=sum_(j=1)^m min(p^ord_p(j),rho), R(m)=W(m)-T(m).

  For 0<=m<=2N,

      R(m)<=W(m)/2,
      equality exactly at m=0,N,2N.                    (2.1)

  W is superadditive. The Gauss weight of N_k on every rho disk is at least T(k), and for k=N its residual is a nonzero multiple of Y^L.

For clarity, the cap (2.1) is the leading-two HALF-W cap, not the enlarged low-digit cap. The accepted proof derives it by base-p digit linearity: for h<=a<=r,

    R(p^a)=W(p^a)/2-(r-a)(p-1)p^(a-1)/2,

and lower digits have strictly positive slack. This is why equality below 2N is only at 0,N. The low-digit exclusion of x=p/2 is NOT imported: it is false for the present central r=2 boundary.

The exact identities used for the new neighboring bound are

    H_b(z)=sum_(k=b mod 2,0<=k<=b)
        w_b N_k(z)/(w_k Q_((b-k)/2)),                    (2.2)

    H_b'(z)=sum_(k=b mod 2,k>=1) sum_(0<=m<k)
        w_b z^(k-m-1) N_m(z)
        /[Q_((b-k)/2) w_m(1-q^(k-m))].                (2.3)

These are the ordinary characteristic-zero Newton and derivative identities, as proved in the accepted sources. Every exponent used is below p^s because 2N+1<pN<=p^s. Hence all relevant denominators are nonzero. The recurrence, identities, coordinate change and CD normalization are unchanged.

## 3. New neighbor bounds for P_(2N-1)

Set b=2N-1. Then W(b)=N+4B=2E. On any closed rho disk, the k-th term of (2.2) has weight at least

    W(b)-[W((b-k)/2)+R(k)].

By (2.1) and superadditivity, the bracket is at most W(b)/2=E. Here k is positive odd. The half-W inequality is strict unless k=N, so only k=N can attain E. At k=N the bracket is W((N-1)/2)+R(N)=B+(N/2+B)=E. The unique surviving term is therefore

    C_- N_N(z), C_-=w_(2N-1)/(w_N Q_((N-1)/2)).          (3.1)

Consequently H_(2N-1) has Gauss weight E, with residual a nonzero multiple of Y^L. It has exact value E at every boundary point.

Its ordinary derivative has weight at least E on the WHOLE closed disk. To prove this, in (2.3) put j=k-m>=1 and a=(b-k)/2. The bracket subtracted from W(b) is bounded by

    W(a)+R(m)+p^ord_p(j)
      <= W(b-j)/2+p^ord_p(j)
      = E + [p^ord_p(j)-W(j)/2].                       (3.2)

The last equality uses the exact reflection W(2N-1-j)=W(2N-1)-W(j), valid for 0<=j<=2N-1.

The square bracket is at most 1/2, with equality only for j=1 or j=p. Indeed, at fixed ord_p(j)=d its maximum occurs at j=p^d, and the value is

    (p^d-d(p-1)p^(d-1))/2.

It is 1/2 for d=0,1 and negative for d>=2. Increasing j at fixed d decreases it by at least 1/2. If j=1 or p, parity makes m even. For m>0, (2.1) is strict because m cannot equal the odd N, making (3.2) strictly less than E+1/2. If m=0, then 2a=2N-1-j lies in [N,2N), while a<N. Thus the floor contribution at N already makes 2W(a)<W(2a), again giving strictness. All brackets lie in (1/2)Z, so strict inequality below E+1/2 implies the required bound <=E. This is a uniform proof, not the finite maximization check.

The exact coordinate identity is

    H_b(v0^2)=v0^b P_b(v0+v0^-1).                     (3.3)

On the branch near i, z=v0^2 and X=v0+v0^-1 are related by an analytic isometry with unit ordinary derivatives. Both are in unit neighborhoods where v0 and v0-v0^-1 are units. Differentiating (3.3) BEFORE reduction gives

    H_b'(z)=v0^(b-2) [ (b/2)P_b(X)
                         +(v0-v0^-1)P_b'(X)/2 ].       (3.4)

The value and derivative lower bounds for H_b transfer through (3.3)-(3.4), since b is an integer of nonnegative valuation. Hence, writing M=P_(2N-1),

    v_Gauss(M)>=E, v_Gauss(M')>=E,
    v(M(xi))=E at every rho-boundary point.             (3.5)

Likewise P_(2N) has Gauss weight at least W(N), and on every boundary

    v(P_(2N)')=D_2.                                    (3.6)

For (3.6) the prefactor term in (3.4) has weight at least r e+W(N), where e=v(p)=(p-1)p^(s-1). This is strictly greater than D_2 because r e>N/2-p. Thus the exact boundary derivative statement from H_(2N) transfers OFF its roots as well; this additional check prevents an illicit use of the at-root-only coordinate simplification.

## 4. The odd quotient gives the complete boundary root counts

Every odd P polynomial is divisible by X by its defining recurrence. Define the POLYNOMIALS

    F=P_(2N+1)/X, G=P_(2N-1)/X.

The exact recurrence gives

    F=P_(2N)-a_(2N) G, a_(2N)=1-q^(2N), v(a_(2N))=N.  (4.1)

On a noncentral disk a!=0, X has constant valuation x_a0=p^ord_p(a)<rho. Division by X is a unit analytic operation after that scalar normalization, so G has weight at least E-x_a0>=E-rho.

On the central disk, M=XG is an exact polynomial factorization. The Gauss weight at radius rho of multiplication by X is precisely addition by rho. Thus (3.5) again gives weight(G)>=E-rho. There is no division at X=0 in this reasoning.

Since rho<N/2, on EVERY disk

    weight(a_(2N) G)>=N+E-rho
                        =W(N)+N/2-rho > W(N).          (4.2)

Therefore F has exactly the same normalized disk residual as P_(2N). This residual has degree 2L, nonzero leading and constant coefficients, and all coefficients of higher degree have positive weight after normalization. The standard closed-disk Newton-polygon count gives exactly 2L roots of F per disk, counted with multiplicity; the nonzero residual constant puts all of them on the boundary. These counts total beta*2L=2N=degree(F), so they cover ALL F roots, without a separate outside-disk comparison and without any assumption of simplicity.

The original zero root of P_(2N+1)=XF is simple. In the central disk, (4.2) is strictly smaller as a perturbation than P_(2N)'s constant residual, and

    v(F(0))=W(N).

Thus P_n'(0)=F(0)!=0, with the derivative valuation in Section 1. In particular F has no zero root. The H/P identity transfers this geometry, including multiplicities, to H_n; its root -1 corresponds to P_n's zero root.

## 5. Root-dependent derivative separation and the r>=3 theorem

For a nonzero root xi of F, put x=v(xi)>0. Differentiating the POLYNOMIAL identity (4.1), or differentiating M/X at the nonzero xi, gives the exact identity

    F'(xi)=P_(2N)'(xi)
        -a_(2N)[M'(xi)/xi-M(xi)/xi^2].                 (5.1)

By (3.5), the second piece inside the bracket has exact valuation E-2x, and the first has valuation at least E-x>E-2x. Therefore the full perturbation in (5.1) has exact valuation N+E-2x. By (3.6) the other term has exact valuation D_2=N+E-p. Unless 2x=p, their valuations differ and

    v(F'(xi))=min(D_2,N+E-2x).                         (5.2)

Since P_n=XF and F(xi)=0, P_n'(xi)=xi F'(xi), proving the claimed formula and simplicity whenever 2x!=p.

The complete geometry in Section 4 says that x is rho on the central boundary, and x=p^ord_p(a) on every noncentral disk. None of these noncentral integral powers equals p/2. Moreover rho=p/2 exactly when r=2. For r>=3, rho>p/2. Thus (5.2) proves every root simple for all r>=3. For r=2 it proves all noncentral roots simple, but makes no claim about the central 2L=2p roots.

At all roots the two ordinary coordinate derivatives in (3.3) are units. P roots reduce to zero and hence never meet X=+/-2, while H_n(0)=1. Differentiating at a corresponding ROOT removes the prefactor term exactly, so ordinary root-derivative valuations and multiplicities transfer to the original H_n without a ramified-coordinate exception.

## 6. The r=2 tie cancels on the entire root residual locus

This section proves the obstruction in (1.1) uniformly in odd p and s>2. Let N=p^2, B=p(p-1), A=(N-1)/2, t=q-1, mu^2=t^p, epsilon=(-1)^((p-1)/2). All residues below are coefficientwise at X=mu Y, with z=v0^2 and z+1=v0 X, choosing v0 congruent to i.

For any positive j<p^s, the leading edge unit is

    (1-q^j)/t^(p^ord_p(j)) -> -j/p^ord_p(j).

Direct full-block counting and Wilson's identity give

    w_N/t^(N+2B) -> -1,
    Q_A/t^B -> -1,
    a_(2N)/t^N -> -2,
    w_(2N)/w_N^2 -> 2.                                 (6.1)

For Q_A, writing a=(p-1)/2, the product of reduced positive indices j/p^ord_p(j), 1<=j<=A=ap+a, is (-1)^a(a!)^2=-1. The additional (-2)^A factor is 1 modulo p because A is even and 2^A=2^(a(p+1))=1 modulo p. The w_N unit follows by separately multiplying the p nonmultiple-of-p blocks, the nonendpoint multiples of p, and the endpoint p^2. These calculations fix phases, not just valuations.

Among j=0,...,N-1, exactly p indices are divisible by p. At z near -1 the other factors z+q^j have initial constant j t, whose product has unit -1 and t exponent B. The p divisible indices have initial term z+1, since their nonzero shifts have valuation at least p>rho. Therefore

    N_N(z) ~ -t^B(z+1)^p.                              (6.2)

Here '~' means equality of normalized Gauss initials, not an exact characteristic-zero equality. The accepted leading-two Newton residual is N_N^2+w_N: its constant coefficient is w_(2N)/Q_N with the same initial as w_N, by the block unit Q_N/w_N ->2. Combining (6.1)-(6.2) and dividing by v0^(2N), whose residue is -1, gives

    P_(2N)(mu Y)/t^(N+2B) -> 1+Y^(2p).                (6.3)

By (4.2) the perturbation does not affect this residual, proving the first formula in (1.1).

From the unique neighbor term (3.1), using w_(2N-1)=w_(2N)/a_(2N), its coefficient has initial -t^B. Combining with (6.2) and the factor v0^(-(2N-1)) gives

    M(mu Y)/(t^(2B) mu^p) -> epsilon Y^p.              (6.4)

To identify P_(2N)' relative to M, the accepted unique derivative pivot is now k=N+p^2=2N,m=N, so its H expression is

    C z^(N-1) N_N(z), C=w_(2N)/(w_N(1-q^N)).

Dividing its initial by (3.1) yields

    H_(2N)' / H_(2N-1) ~ (1+q^N)Q_A ~ -2t^B.

This notation is only a concise comparison of their identical N_N initial factors; no division at their zeros is needed. In (3.4) the P_(2N) prefactor derivative is strictly higher as already checked, and the conversion factor for this ratio is 2v0^2/(v0^2-1), with residue 1. Thus

    P_(2N)'(mu Y)/(t^(3B) mu^p) -> -2 epsilon Y^p.      (6.5)

Finally use F'=P_(2N)'-a_(2N)G'. At the central radius, the part a_(2N)M'/X has weight at least N+E-rho, strictly greater than D_2=N+E-p because rho=p/2. The other part, with its PLUS sign in (5.1), has by (6.1),(6.4)

    a_(2N)M(mu Y)/(mu^2 Y^2 t^(3B) mu^p)
        -> -2 epsilon Y^(p-2),

since N-B=p and mu^2=t^p. These quotient terms are legitimate as Laurent-series computations on the boundary; their displayed surviving initial is polynomial because p>=3. Summing with (6.5) proves the second formula in (1.1).

The residual gcd of 1+Y^(2p) and Y^(p-2)(Y^2+1) is exactly Y^2+1. Both nonzero roots of this quadratic have multiplicity p in the F residual, so all 2p central roots fall over locations where this normalized ordinary derivative vanishes. This is a genuine root-dependent tie, not a missing sign, incorrect endpoint v(a_(2N)), or a Jackson derivative. Replacing the cap with the earlier low-digit cap would not be justified and does not remove this exhibited cancellation.

## 7. Algebraic-square kernel scope

For every n=2N+1 here, all recurrence edges 1-q^j, 1<=j<n, are nonzero. If P_n and P_(n-1) shared a root, backward recurrence would force P_0=1 to vanish. Thus adjacent P polynomials are coprime regardless of the unresolved central simplicity issue.

The ordinary algebraic Christoffel-Darboux identity at a P_n root xi is

    sum_(j=0)^(n-1) P_j(xi)^2/w_j
        =P_n'(xi)P_(n-1)(xi)/w_(n-1).

For r>=3 the right side is nonzero at EVERY root, by Section 5 and the exact zero-root check. For r=2 it is nonzero at zero and every noncentral root. The central 2p roots remain unresolved by this package; no universal nonvanishing is inferred from adjacent coprimeness alone. These are algebraic squares, not absolute-value squares; no positivity, real-rootedness, or interlacing argument appears. Algebraic nonvanishing in a p-adic embedding transfers to characteristic-zero primitive embeddings by injectivity and Galois conjugacy.

## 8. Controls, independence and stopping condition

check_controls.py supplies finite exact checks of the new neighboring polynomial/ordinary-derivative bounds, the quotient and original H/P/CD identities, and the r=2 coefficientwise residual formulas. The actual-field controls reconstruct the ORIGINAL P recurrence over Z[q]/Phi_(p^s). They shift q=1+t exactly at degree below e=phi(p^s), retaining mixed-characteristic coefficient valuations j+e ord_p(c_j), with leading p/t^e unit -1. Distinct j<e give distinct weights modulo e, so their minimum is exact even above ramification. No floating root or characteristic-p truncation substitutes for these field calculations.

Additional finite good-prime witnesses show squarefreeness for the listed cyclotomic specializations, including r=2 cases where this mechanism fails. These are finite controls only and do not resolve the unlimited r=2 family.

The author derived the root-dependent quotient mechanism and the explicit central cancellation before receiving a reviewer's independently computed finite controls. Those incoming controls confirmed the formulas but supplied no lemma used above. All finite confirmations are auxiliary; the uniform partial theorem and obstruction are the mathematical statements proved in Sections 3-7. The candidate is not independently accepted until a separate reviewer binds these frozen bytes.

The stopping condition is now met: the family has a complete r>=3 proof, and the remaining r=2 central obstacle is explicitly localized, counted, and exhibited with exact residual phases. Deeper analysis of that repeated cluster is a new bounded task, not an unreported assumption in this package.
