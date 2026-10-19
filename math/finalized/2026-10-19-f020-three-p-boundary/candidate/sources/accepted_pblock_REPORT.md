# F020: a variable-degree p-adic squarefreeness advance, b < 2p

19 October 2026 UTC. Canonical owner F020; F023 remains its alias. Fresh algebraic research packet, with no external write or historical-program execution. Independent review is required before acceptance.

## Result and boundary

Let p be an odd prime, s >= 1, d=p^s, and omega a primitive dth root. For

    H_b(z;q) = sum_(k=0)^b [b choose k]_q z^k,
    P_0=1, P_1=X,
    P_(n+1)=X P_n-(1-q^n)P_(n-1),

this packet proves

    H_b(z;omega) and P_b(X;omega) are squarefree whenever
    0 <= b < min(2p,d).                                      (T)

The b<p part reproduces the accepted range. The new variable-degree range is p<=b<2p for every s>=2. This is an unlimited theorem in p and s, not a fixed-degree calculation or a root-order census. The proof uses a p-adic embedding, an exact continuant identity, and simple-root Hensel lifting at three explicitly derived scales. It does not use any of the ruled-out positive-metric routes.

For the first subsequent residual, b=2p<d, the same analysis gives a precise new obstruction to merely continuing the simple-residual argument: all roots have normalized valuation (2p-1)/(2p), and the polynomial at that scale reduces to

    Y^(2p)-1=(Y^2-1)^p.                                    (B)

The two residual roots are p-fold. Formula (B) does not say the characteristic-zero roots collide. It identifies the new clusters that need to be resolved. No proof for all b>=2p, no characteristic-zero counterexample, and no uniform ordinary-guard closure is claimed.

Combining (T) with the accepted uniform node theorem supplies both static guards on this enlarged range. The existing local all-A theorem may therefore be composed on precisely this range, subject to acceptance of the present proof. The inherited normalization, leading coefficients, existing d=9,25 certifications, priority 58, alias relationship, and owner-open status are unchanged.

## 1. Valuation setup and the outer scale

Embed Q(omega) into an algebraic closure of Q_p, put q=omega and t=q-1, and normalize the valuation v by v(t)=1. Then

    v(p)=e=phi(p^s)=p^(s-1)(p-1).

Indeed Phi_(p^s)(1+T) is Eisenstein: it is monic, its reduction modulo p is T^e, and its constant coefficient is p. We work in finite complete extensions as necessary to contain fractional powers of t and residual roots. The residue characteristic is p. A polynomial with integral coefficients whose reduction has a simple root has a unique root reducing to it, by the usual simple-root Hensel lemma. We only apply that lemma when the derivative is explicitly nonzero.

Write u_j=1-q^j. For every positive j,

    u_j/t reduces to -j modulo the maximal ideal.           (1)

For s>=2, the stronger fact needed at a block boundary is

    v(u_p)=p,        u_p/t^p reduces to -1.                 (2)

This follows from (1+t)^p-1=t^p+sum_(j=1)^(p-1) binom(p,j)t^j: e+1>p, so the t^p term uniquely has least valuation.

Define the classical residual polynomials over F_p by

    h_0(Y)=1, h_1(Y)=Y,
    h_(n+1)(Y)=Y h_n(Y)+n h_(n-1)(Y).

If a^2=t, substitution in the actual recurrence gives

    P_n(aY)/a^n reduces to h_n(Y).                         (3)

Every polynomial in (3) is integral, since its recurrence coefficients are u_j/t. For r<p, the familiar identities, also immediate from the recurrence, are

    h_r'(Y)=r h_(r-1)(Y),
    h_(2m)(0)=(2m-1)!!,
    h_(2m+1)'(0)=(2m+1)!!.

Consecutive h's up to index r have no common root: a common root propagates downward through nonzero coefficients 1,...,r-1 to h_0=1. Thus h_r is squarefree. Its zero at 0 exists exactly when r is odd and is simple; all other roots are nonzero. Empty products and (-1)!! are 1.

The explicit coefficient formula

    h_n(Y)=sum_(j=0)^floor(n/2)
       n!/[2^j j!(n-2j)!] Y^(n-2j)

shows h_p(Y)=Y^p in characteristic p. The recurrence then gives, for 0<=r<p,

    h_(p+r)(Y)=Y^p h_r(Y).                                (4)

For b<p, (3) and the squarefreeness of h_b already lift b distinct roots, proving the accepted lower range. For b=p+r, (3)-(4) lift r nonzero roots of valuation 1/2 if r is even, and r-1 such roots if r is odd. The zero cluster remains to be analyzed, not assumed simple.

## 2. The p-block is an additive separable residual

For s>=2 put h=(p-1)/2 and c=(-1)^(h+1) in F_p. Then

    t^(-p) P_p(tY;q) is integral and reduces to Y^p+cY.    (5)

In particular c is nonzero and the residual derivative is c.

Here is a direct proof, including the coefficient estimate that makes the scaling legitimate. First work formally over F_p[T], with q=1+T. For 0<k<p the Gaussian identity

    [p choose k]_q = (1-q^p)/(1-q^k) [p-1 choose k-1]_q

and the expansion in F_p[[T]] imply

    [p choose k]_(1+T)
       = [(-1)^(k-1)/k] T^(p-1) + O(T^p).               (6)

The denominators after canceling T are units, so (6) is a valid formal-series calculation for these polynomial coefficients. Thus H_p(z;1+T) equals 1+z^p modulo T^(p-1). The exact normalization

    H_p(v^2;q)=v^p P_p(v+v^(-1);q)                       (7)

and Frobenius imply

    P_p(X;1+T)=X^p modulo (p,T^(p-1)).                  (8)

The substitution X=v+v^(-1) into Laurent polynomials is injective (compare the largest v exponent), so this really is coefficientwise divisibility in X.

Differentiating H_p in z and using (6) at z=-1 gives

    H_p'(-1;1+T) = -T^(p-1)+O(T^p) modulo p.           (9)

There are p-1 intermediate terms, each contributing +T^(p-1), and the endpoint derivative p vanishes modulo p. Differentiating (7) at v=i gives the exact identity

    P_p'(0;q)=(-1)^h H_p'(-1;q).

Consequently the X coefficient in (8) has leading term c T^(p-1). Since P_p is odd, it has no constant term. After specialization T=t, every lower coefficient has valuation at least p-1, and the X coefficient divided by t^(p-1) reduces to c: the possible p-multiples have valuation at least e>p-1. Substituting X=tY therefore proves integrality in (5); only X^p and the linear term survive. This proves (5) without extrapolation from any finite prime list.

More generally the same estimates show:

- If v(x)=alpha<1, then P_p(x)/x^p reduces to 1, provided alpha>0 and comparisons are made after the corresponding normalization.
- If v(x)=alpha>1, then P_p(x)/(t^(p-1)x) reduces to c.

These statements mean equality of the indicated leading terms; we use them only in substitutions x=t^alpha Y with Y a residual indeterminate. They follow because every other coefficient has valuation at least p-1 and p is odd.

## 3. Exact block identity and its leading constants

Let F_r be the continuant for the r vertices immediately after vertex p:

    F_0=1, F_1=X,
    F_(r+1)=X F_r-u_(p+r)F_(r-1).

Thus its internal edge coefficients are u_(p+1),...,u_(p+r-1). Let G_(r-1) be the continuant on the final r-1 vertices, with internal coefficients u_(p+2),...,u_(p+r-1). For r>=1 the exact concatenation identity is

    P_(p+r)=F_r P_p-u_p G_(r-1)P_(p-1).               (10)

It follows by expanding the path determinant across its joining edge, or directly by recurrence in r; at r=1 it is the defining recurrence. At r=0 use P_p alone, with no G term.

For j<p, equation (1) makes the leading coefficient pattern in F_r the same as h_r. Therefore for any alpha>1/2 and X=t^alpha Y:

    F_(2m)(X) / t^m -> (2m-1)!!,
    F_(2m+1)(X) / (t^m X) -> (2m+1)!!,               (11)

where the second statement is a polynomial leading-term statement before canceling the symbolic factor X. The displayed constants are nonzero when r<p. It follows either from the matching expansion of a continuant or by applying its recurrence and comparing valuations: terms with more X factors have strictly larger valuation, and the leading sums are the stated h_r coefficients.

When r=2m+1, the even G_(2m) has the constant leading term

    G_(2m)(t^alpha Y)/t^m -> 2^m m!.                   (12)

Its constant term is (-1)^m times u_(p+2)u_(p+4)...u_(p+2m), so (12) is immediate. Finally

    P_(p-1)(t^alpha Y)/t^h -> (p-2)!!, h=(p-1)/2.    (13)

All constants in (11)-(13) are nonzero modulo p in the stated ranges.

## 4. Root separation for p <= b < 2p

Write b=p+r, 0<=r<p, and assume s>=2.

### Even r=2m, including r=0

Substitute X=tY into (10). Equations (5) and (11) show that division by t^(p+m) gives the residual

    (2m-1)!! (Y^p+cY).                               (14)

For r>=2 the joining term has valuation at least p+m+h, strictly greater than p+m: G_(r-1)(tY) has valuation at least m, P_(p-1)(tY) has valuation h, and v(u_p)=p. Thus it cannot change (14). At r=0 the joining term is absent.

The p roots of (14) are simple. Its p-1 nonzero roots lift to roots of P_b of valuation 1. Its zero root lifts to the exact root X=0, since b is odd. The r outer roots already lifted in Section 1 have valuation 1/2. These b=p+r roots are all distinct, proving squarefreeness.

### Odd r=2m+1, p>=5

At X=tY, divide (10) by t^(p+m+1). Since h>=2, the joining term has valuation p+m+h>p+m+1. The residual is

    (2m+1)!! Y(Y^p+cY).

Its p-1 nonzero roots are simple and lift to roots of valuation 1. Its zero is double, so no Hensel conclusion is asserted there. Along with the r-1 outer roots of valuation 1/2, this accounts for b-2 roots.

To split the final two, set

    alpha=(p+1)/4>1,   L=p+m+h.

Choose a fractional power of t in a finite extension and put X=t^alpha Y. Equations (2), (5), and (11)-(13) give

    P_b(t^alpha Y)/t^L
      -> (2m+1)!! c Y^2 + (2^m m!)(p-2)!!.           (15)

The exponents agree because m+(p-1)+2alpha=p+m+h. All omitted terms have strictly larger valuation: P_p is dominated by its linear term when alpha>1, and the other continuants are dominated by their constant or linear terms when alpha>1/2. The sign of the constant term is positive because the joining term is -u_p and u_p/t^p reduces to -1.

Both coefficients in (15) are nonzero. In odd characteristic this quadratic has two distinct, nonzero roots over a finite residue-field extension. They lift to two roots of valuation alpha, distinct from each other and from both earlier scales. The total is (r-1)+(p-1)+2=b distinct roots.

### The sole excluded small-prime case

For p=3 the even-r argument covers b=3 and b=5. Odd r<p gives only r=1, b=4. Here alpha=1, so the preceding strict scale separation is deliberately not used. A direct degree argument settles the case. Write

    P_4=X^4-A X^2+B,
    A=(1-q)(q^2+2q+3),
    B=(1-q)^2(q^2+q+1).

For q of order 3^s>=9, B is nonzero. Also

    A^2-4B=(1-q)^2(q^4+4q^3+6q^2+8q+5).

The nonzero polynomial in the last parentheses has degree 4, less than phi(3^s)>=6, and so cannot vanish at q. Hence the polynomial in X^2 has distinct nonzero roots and P_4 is squarefree. This is compatible with the accepted quartic result but gives a self-contained algebraic treatment of the exception.

This completes the proof for P_b in (T).

## 5. Transfer to H_b and the bilinear kernel

The exact identity (7) holds for every b. Since every u_j has positive valuation, P_b(X) reduces to X^b modulo the maximal ideal. Thus P_b(2) and P_b(-2) are nonzero for odd p. The maps X=v+v^(-1) and z=v^2 are unramified at all roots under consideration: v is nonzero, and the only critical values of the first map are X=2,-2. Consequently squarefreeness of P_b implies squarefreeness of H_b. Equivalently, differentiating (7) at a root shows that a repeated H_b root away from z=1 would give a repeated P_b root, while z=1 is already excluded.

The accepted diagonal Christoffel-Darboux identity and coprimality of consecutive P's now make the actual bilinear kernel nonzero at every root for this enlarged range:

    sum_(k=0)^(b-1) P_k(xi)^2 / product_(j=1)^k(1-q^j) != 0.

The p-adic proof establishes an algebraic nonzero discriminant. It therefore holds at every primitive complex embedding. No positivity or p-adic valuation is transported as a complex positivity assertion.

## 6. A precise new boundary at b=2p

For s>=2, set b=2p and alpha=(2p-1)/(2p). The block formula (10), now with r=p, is still exact. The internal coefficients in F_p differ from those of P_p by

    u_(p+j)-u_j=-q^j(q^p-1),

which has valuation p. Because a continuant is a polynomial with integer coefficients in its edge coefficients, F_p-P_p has coefficientwise valuation at least p. Thus every lower coefficient of both F_p and P_p has valuation at least p-1. Since 1/2<alpha<1, both are dominated by X^p after X=t^alpha Y.

G_(p-1) and P_(p-1) are dominated by their constants. Their constants divided by t^h reduce respectively to 2^h h! and (p-2)!!. Their product is (p-1)!=-1 in F_p, by Wilson's theorem. Using -u_p/t^p -> 1 and 2p alpha=2p-1 gives the integral monic scaled polynomial

    P_(2p)(t^alpha Y)/t^(2p-1) -> Y^(2p)-1.

Its constant is a unit, so all roots have valuation alpha. But in characteristic p the residual factors as (Y^2-1)^p and has identically zero derivative. Simple-root Hensel lifting cannot separate either p-fold cluster. This proves the asserted boundary (B), while supplying no characteristic-zero collision. At (p,d,b)=(3,9,6), for example, squarefreeness is already independently certified, illustrating why an inseparable residual is not a counterexample.

Resolving these two p-fold clusters, and then controlling subsequent blocks, is additional mathematical work. This report does not replace it by numerical spectra, finite prime checks, or an assumed positive kernel.

## 7. Reproducibility and scope

The fresh checker is authored in this packet and uses only installed SymPy and Python standard-library modules. It verifies the actual Gaussian/continuant identities, the p-block coefficient divisibility and leading linear coefficient, the separate residue polynomials and their squarefreeness or inseparability, the joining-edge indexing and constants, the exceptional quartic factor, and the explicit b=2p boundary. Finite prime instances are transcription controls for the stated algebraic proof, not its justification or a new root-order census.

The source files supplied by the parent are copied and SHA-256-bound in SOURCE_BINDINGS.json. No fresh remote read or historical originality claim is represented. All computation is local; no repository or other external record is changed by this packet. The complete command log and check outcomes are retained separately. Independent acceptance remains required.

The terminal outcome is a proved author-level extension from b<p to b<2p, with the exceptional p=3 quartic handled exactly, and a precisely derived inseparable residual at the next boundary. The unrestricted ordinary guard, and hence the unrestricted prime-power all-A package, remain open.
