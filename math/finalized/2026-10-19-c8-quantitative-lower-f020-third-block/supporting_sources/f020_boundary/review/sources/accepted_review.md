# Independent review: F020 prime-power squarefreeness through b < 2p

19 October 2026 UTC. Scientific review of the author packet `f020_two_digit_hensel_20261019_0124`. Exact source bytes and the frozen author manifest are bound separately in `SOURCE_BINDINGS.json` and `INPUT_VERIFICATION.json`. This review makes no external or canonical-record changes.

## Verdict and certified scope

**ACCEPT within the written scope.** No mathematical blocker was found. Acceptance binds to author manifest SHA-256 `6a0c2cf641ff4a54ce98b9b83f2463f4ffa34425da4b4305fa995be8e615634a` and author report SHA-256 `4e68e5e6b9fe2c372cff20ca78de54deb2151ecf0f4e040780edd4c3cf537b79`. All nine declared author files were verified before and after isolated checker replay.

For every odd prime p, every s >= 1, every primitive root q of order d=p^s, and every integer 0 <= b < min(2p,d), both the actual continuous-q-Hermite polynomial P_b and the actual Rogers–Szegő polynomial H_b are squarefree in characteristic zero. Thus their actual bilinear Christoffel–Darboux kernel is nonzero at every root in this range. The new variable-degree range is p <= b < 2p when s >= 2. The accepted b < p range is recovered without alteration.

The additional boundary statement is also correct: for b=2p and s>=2, every P_(2p) root has t-normalized valuation (2p-1)/(2p), and its displayed scaled residual is Y^(2p)-1=(Y^2-1)^p. This is an inseparable residual, not a characteristic-zero collision. No all-residual closure follows.

The unlimited conclusions rest on the written algebraic argument. The independent fresh checker passed 208 exact assertions; those finite checks are transcription controls only. Neither the author proof nor this review relies on a new root-order census, a positive Hermitian metric, numerical eigenvalues, or a historical originality assertion.

## 1. Exact family and ramification

The recurrence reviewed is exactly the baseline family:

    P_0=1, P_1=X,
    P_(n+1)=X P_n-(1-q^n)P_(n-1),
    H_b(v^2;q)=v^b P_b(v+v^(-1);q).

The checker reconstructs both recurrences independently and verifies the transformation through b=12, in addition to its recurrence proof. There is no alteration of sign, Jacobi normalization, Gaussian coefficient convention, or variable between the old kernel problem and the new proof.

For a primitive p^s-th root in an algebraic closure of Q_p, t=q-1 is a uniformizer with v(t)=1 and v(p)=e=phi(p^s). The shifted cyclotomic polynomial is Eisenstein: its reduction is T^e and its constant term is p. Consequently u_j/t reduces to -j for every positive j. For s>=2, e+1>p, so u_p=-((1+t)^p-1) has valuation exactly p and u_p/t^p reduces to -1. This strict inequality is used only in the higher-order part of the theorem, never for the s=1 case.

Fractional powers of t can be chosen in a finite complete extension, and each finite set of residual roots can be included by a further finite residue-field extension. Every Hensel application is to a polynomial proved integral after its stated normalization. A monic leading coefficient is not required for simple-root Hensel lifting, so the degree drops in the middle reductions cause no problem.

## 2. Outer Hermite reduction

The normalization P_n(aY)/a^n, a^2=t, has recurrence coefficient u_j/t and is integral. Its residual h_n satisfies

    h_(n+1)=Y h_n+n h_(n-1).

For r<p, h_r'=r h_(r-1), and the nonzero recurrence coefficients rule out common zeros of h_r and h_(r-1). Hence h_r is squarefree. Its constant for even r=2m is (2m-1)!!, while its linear coefficient for odd r=2m+1 is (2m+1)!!; each is nonzero modulo p in the claimed range.

The integer coefficient formula proves h_p=Y^p in characteristic p: every nonleading coefficient has a numerator divisible by p and denominator prime to p. Because the recurrence coefficient at index p vanishes modulo p, h_(p+r)=Y^p h_r for 0<=r<p. This produces exactly r nonzero outer roots for even r and r-1 for odd r, all with valuation 1/2. The remaining zero cluster is correctly left unresolved at this stage.

For b<p all b residual roots are simple. This includes b=0 and b=1, with the standard convention that a nonzero constant is squarefree. For s=1 the requirement b<min(2p,d) is precisely b<p, so no higher-block statement is implicitly asserted at order p.

## 3. The crucial p-block coefficient estimate

For 0<k<p, the exact Gaussian identity gives, over F_p[[T]],

    [p choose k]_(1+T)
       = ((-1)^(k-1)/k) T^(p-1) + O(T^p).

Canceling one T from numerator and denominator leaves a unit denominator k+O(T), and [p-1 choose k-1] at T=0 is (-1)^(k-1). Thus the coefficient formula and its sign are correct.

The q-Hermite transformation then implies coefficientwise

    P_p(X;1+T)=X^p modulo (p,T^(p-1)).

The Laurent substitution is injective over F_p because a nonzero polynomial of degree j has a unique largest Laurent exponent v^j. This justifies recovering divisibility of the P coefficients from the H identity.

At z=-1, differentiating the intermediate terms contributes p-1 copies of T^(p-1), hence coefficient -1 modulo p. The endpoint derivative is p and vanishes modulo p. Differentiating the exact transformation at v^2=-1 gives

    P_p'(0)=(-1)^((p-1)/2) H_p'(-1),

so the linear coefficient has leading residue c=(-1)^((p+1)/2). This is nonzero.

Specialization T=t is valid coefficientwise. The ignored p-multiples have valuation at least e>p-1 for s>=2, while every lower coefficient has valuation at least p-1. Since P_p is odd, no constant term occurs. Therefore

    P_p(tY)/t^p -> Y^p+cY.

All omitted coefficients have strictly greater valuation after scaling. Its derivative is c in characteristic p, so all p residual roots are simple. The same bound proves dominance of X^p when 0<alpha<1 and dominance of c t^(p-1)X when alpha>1. In particular these dominance assertions do not rely on finite coefficient sampling.

## 4. Joining-edge identity and all three scales

The exact continuant identity is

    P_(p+r)=F_r P_p-u_p G_(r-1)P_(p-1).

Here F_r uses internal edges p+1 through p+r-1, and G_(r-1) uses p+2 through p+r-1. The joining edge is u_p. These indices are correct; r=1 gives the defining recurrence, and r=0 has no joining term. The independent checker reconstructs shifted continuants directly and verifies the identity including r=p in bounded instances.

For alpha>1/2, the leading F_(2m) constant is t^m(2m-1)!!, while F_(2m+1) has leading term t^m X(2m+1)!!. G_(2m) has leading constant t^m 2^m m!, and P_(p-1) has leading constant t^h(p-2)!!, h=(p-1)/2. Nonzero constants and the strict comparison 2alpha>1 prove these estimates without cancellation. All relevant factorials have arguments below p.

### Even r=2m

At X=tY the product F_r P_p has valuation p+m. The joining term has valuation at least p+m+h, strictly higher. G_(2m-1)(tY) has at least the factor t^(m-1)X and therefore valuation at least m; its exact linear coefficient need not be nonzero for this lower bound.

The residual is (2m-1)!!(Y^p+cY). Its p-1 nonzero roots lift with valuation 1, and its simple zero lifts to the exact parity root X=0 because p+r is odd. Together with r outer roots, this gives p+r distinct roots. The r=0 case is included with (-1)!!=1 and no nonexistent G term.

### Odd r=2m+1, p>=5

At X=tY the main product has valuation p+m+1. The joining term has valuation p+m+h, so the gap is h-1=(p-3)/2>0. The residual is

    (2m+1)!! Y(Y^p+cY).

There are p-1 nonzero roots. At any such root the derivative is (2m+1)!! cY, which is nonzero. The zero is double and is explicitly not lifted by a simple-root argument. Together with the r-1 outer roots this accounts for p+r-2 roots.

For the final pair set alpha=(p+1)/4>1 and L=p+m+h. The main product has leading term t^L(2m+1)!! cY^2. The joining term contributes t^L(2^m m!)(p-2)!! with a positive sign because -u_p/t^p reduces to +1. Thus the residual quadratic is exactly

    (2m+1)!! cY^2+(2^m m!)(p-2)!!.

Both coefficients are nonzero. Its roots are nonzero and its derivative is 2(2m+1)!! cY, also nonzero in odd characteristic. It gives two distinct roots of valuation alpha. Since alpha>1>1/2, neither can coincide with either earlier scale. The total count is exactly p+r.

### Unique overlap exception

For p=3, the only odd r<p is r=1, so b=4. The formal deepest scale equals 1 and the common residual is Y^4+Y^2+1=(Y^2-1)^2 over F_3, which is inseparable. The author does not misuse it.

Instead P_4=X^4-A X^2+B has B=(1-q)^2(q^2+q+1), nonzero at order 3^s>=9, and

    A^2-4B=(1-q)^2(q^4+4q^3+6q^2+8q+5).

The nonzero factor of degree 4 cannot vanish at a primitive 3^s-th root whose minimal polynomial degree is at least 6. Hence the quadratic in X^2 has distinct nonzero roots, producing four distinct X roots. This exact treatment covers all s>=2; it is not just the d=9 check. Even r covers the remaining b=3 and b=5 cases.

## 5. Transfer to the actual H polynomial and kernel

For every j, u_j has positive valuation, so P_b(X) reduces to X^b modulo the maximal ideal. Because p is odd, P_b(2) and P_b(-2) are units. This supplies the needed endpoint exclusion directly, independently of the stronger accepted all-odd node theorem.

H_b(0)=1, so at each root choose v!=0 with z=v^2. The map v->v^2 is unramified in characteristic zero, and v->v+v^(-1) is unramified unless v=+/-1, precisely the already-excluded values X=+/-2. Multiplication by v^b is a local unit. Thus multiplicity in H_b is preserved by the exact transformation, proving its squarefreeness from that of P_b.

For b<d, every recurrence norm factor 1-q^j used in the Christoffel–Darboux identity is nonzero. Consecutive P's have no common root. At a P_b root, the kernel is P_b'(xi)P_(b-1)(xi)/w_(b-1), and both numerator factors are now nonzero in the claimed range. This is exactly the prior missing bilinear nonisotropy statement restricted to the new range, with ordinary squares rather than absolute squares.

A nonzero discriminant is an algebraic statement over Q(q). The chosen p-adic embedding is injective, and Galois conjugacy transfers nonvanishing to every primitive complex embedding. Neither p-adic valuations nor residue positivity are transported as complex positivity claims.

## 6. The b=2p boundary is correctly derived

The joining-edge identity remains valid with r=p. Each shifted edge differs by

    u_(p+j)-u_j=-q^j(q^p-1),

which has valuation p. The continuant is an integer polynomial in integral edge coefficients, so F_p-P_p has coefficientwise valuation at least p. Both odd p-blocks therefore have all lower coefficients of valuation at least p-1.

At alpha=(2p-1)/(2p), with 1/2<alpha<1, both p-blocks are dominated by X^p. The joining term is dominated by the constants of its two even continuants. Their normalized product is

    (2^h h!)(p-2)!!=(p-1)!=-1 modulo p.

Because -u_p/t^p reduces to +1, the constant in the scaled P_(2p) residual is -1. The leading term scales by t^(2p alpha)=t^(2p-1), giving

    P_(2p)(t^alpha Y)/t^(2p-1) -> Y^(2p)-1.

The scaled polynomial is monic and integral, and its constant is a unit. All its roots are integral; the valuation of their product is zero, so each has valuation zero. Hence every original root has the claimed valuation alpha. The residual has two p-fold roots and zero derivative. This proves a real obstruction to extending the particular simple-residual step, not an obstruction to characteristic-zero squarefreeness itself.

## 7. Independent checks, provenance, and limits

`independent_checker.py` was written fresh before reading the author checker and does not import or execute it. It builds integer bivariate recurrence coefficients, computes formal reductions for p=3,5,7,11,13, checks the three separate scales and the p=3 overlap, and verifies the b=2p residual with exact rational weights. It also independently reconstructs the exact block identity, the actual H/P transformation, and the exceptional quartic formula. All 208 assertions passed. The first independent pass had 183 assertions; the added boundary and block checks brought it to 208, without a failure or a mathematical correction.

The independent formal controls cannot omit a lower-weight p-multiple: every tested leading weight is at most 2p-1, whereas e>=p(p-1)>2p-1 for every odd prime. This observation connects those formal controls to all s>=2; the theorem itself remains justified by the written estimates.

The reviewer then inspected the author's checker. It uses only local standard-library and installed SymPy code; it writes CHECKS.json beside itself. Identical checker bytes were copied into the review's replay directory and passed all 418 assertions. The resulting CHECKS.json is byte-identical to the frozen author's output. All source manifest hashes and byte counts passed again afterward. The author's finite mixed-characteristic controls are supplemental to the already reviewed universal coefficient estimates.

Baseline inputs are local retained packets supplied by the parent. Their exact bytes are copied or hash-bound; this review makes no new remote-source verification claim. The baseline all-odd node theorem was previously independently accepted, and its report hash matches that accepted review's binding. The positive-metric obstruction report remains compatible with this entirely different p-adic mechanism.

## Terminal decision

Accept the theorem and the precise next-boundary residual as supplemental F020 progress. The existing all-A theorem may be composed only where both guards are separately available, now including this proven range together with accepted prior certifications. No unrestricted ordinary guard is established. F020 remains open, priority 58; F023 remains its alias. No existing normalization, coefficient, census, attribution, endpoint obligation, paired-support obligation, or repository record is changed by this independent review.
