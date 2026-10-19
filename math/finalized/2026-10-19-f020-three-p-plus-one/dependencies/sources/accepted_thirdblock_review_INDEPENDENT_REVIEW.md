# Independent review: F020 third partial p-block

19 October 2026 UTC. Candidate: `f020_third_block_extension_20261019_1347`.

## Verdict and exact acceptance target

**ACCEPT within the written scope. No mathematical blocking issue was found.**

This verdict binds to candidate manifest SHA-256
`042d50f56a07262323d5f0480e03bf546418669375e482db95a8575d878407b1`
and candidate report SHA-256
`2eac2d7ee2c9685aa1413482fde7b3d061d9fb35d522da4aa872df61db7fb925`.

For every odd prime p, every s>=1, every primitive p^s-th root q, and
0<=b<min(3p,p^s), the original recurrence polynomial P_b and original
Gaussian Rogers–Szego polynomial H_b are squarefree. The original
ordinary-square bilinear Christoffel–Darboux kernel is nonzero at each
P_b root. The new degrees are 2p<b<3p for s>=2. The accepted b=2p theorem
is used as an explicitly identified input.

For b=2p+r, 0<=r<p, s>=2, the stated auxiliary-center residual, full root
count and pairwise valuations are correct. The inner degree-2p factor
is irreducible over Q_p(q). The discriminant valuation, with v(q−1)=1,
is

    p(4p−3)+2pr+r(r−1)/2+(r mod 2)(2p−2).

The acceptance is a proof review, not an extrapolation from the finite
controls. It makes no statement at b=3p or later, no unrestricted F020
or all-A closure, no historical-originality claim, and no new root-order
census. F020 remains open, F023 remains its alias, and priority 58 is
unchanged. No external or canonical record was written.

## 1. Source chain and base field

All eleven candidate manifest entries and all nine directly named source
bindings were checked against the actual local bytes. The complete
manifests of the two accepted author packets and both independent
reviews were also checked. Source-binding originals and retained copies
were checked in each source packet, including their differing JSON
schemas. The combined verification covers 72 distinct files. Both
accepted review verdicts bind to the exact author reports and manifests
being used here. Details are in INPUT_VERIFICATION.json.

The accepted inputs are the b<2p theorem and p-block coefficient theorem
from `f020_two_digit_hensel_20261019_0124`, accepted by
`f020_primepower_extension_review_20261019_0124`, and the explicit b=2p
residual from `f020_boundary_hensel_resolution_20261019_0839`, accepted by
`f020_boundary_resolution_review_20261019_0840`. Their proof texts were
read, rather than relying only on verdict labels. No candidate or
historical checker was imported or executed during this review.

Put K=Q_p(q), t=q−1. The Eisenstein polynomial Phi_(p^s)(1+T) shows that
t is a uniformizer: v(K^×)=Z and v(p)=p^(s−1)(p−1). This integral value
group applies to K, not to the finite auxiliary extensions introduced
later. For s>=2 and the indices in the new block,

    v(u_j)=1 if p does not divide j,
    v(u_p)=v(u_(2p))=p,        u_j=1−q^j.

The second equality also follows from u_(2p)=u_p(1+q^p), with the last
factor reducing to 2. All relevant edges are nonzero since
3p−1<p^2<=p^s, including p=3,s=2. The s=1 case uses only the previously
accepted b<p theorem.

The accepted p-block estimate is

    P_p(X)=X^p+lambda X+E(X),
    v(lambda)=p−1, lambda/t^(p−1) -> c=(-1)^((p+1)/2),

with E odd, using exponents 3 through p−2 and having coefficient
valuations at least p−1. E is zero for p=3. Define

    C=−P_(2p)(0), kappa^2=C,
    a^p+lambda a=kappa,
    alpha=(2p−1)/(2p), L=2p−1/2.

The accepted boundary result proves v(a)=alpha, v(kappa)=p−1/2 and
the full coefficientwise reduction

    P_(2p)(a+tZ)/(2 kappa t^p) -> Z^p+cZ.

It also proves this at (−a,−kappa). Its proof explicitly handles the
mixed-characteristic binomial terms and the p=3 error gap, so the new
argument is not importing a merely formal characteristic-p reduction.

## 2. Independent verification of the new perturbation bound

In a block with n vertices and all internal edge valuations equal to 1,
a matching contributing to X^(n−2k) uses k edges. Its coefficient has
valuation at least k. Under X=a+tZ every coefficient of X^j has
valuation at least j alpha, since alpha<1. Thus an even 2j-vertex block
has coefficientwise valuation at least j and an odd (2j+1)-vertex block
has valuation at least j+alpha, because alpha>1/2.

Split P_(2p−1) after its first p vertices. Let U use the final p−1
vertices, V the final p−2 vertices, and D=P_(p−1). Their exact determinant
identity is

    P_(2p−1)=U P_p−u_p V D.

All internal U,V,D edges have valuation 1. With h=(p−1)/2, their
respective bounds are h, h−1+alpha and h. The p-block coefficient
estimate gives v(P_p(a+tZ))>=p alpha. Hence the first summand has bound
h+p alpha. The second summand exceeds that bound by

    h−1/2+alpha > 0.

This is 4/3 at p=3. Therefore

    v(P_(2p−1)(a+tZ)) >= h+p alpha

coefficientwise. No cancellation hypothesis or target root was used.

Now let F_r be the r-vertex tail after vertex 2p and G_(r−1) the same
tail with its first vertex deleted. Direct recurrence gives

    P_(2p+r)=F_r P_(2p)−u_(2p) G_(r−1)P_(2p−1).

The internal edges of F_r are 2p+1 through 2p+r−1, and those of G are
2p+2 through 2p+r−1. These indices and the minus sign are correct.
At r=0 the second term is absent and F_0=1; it is not an instance using
a fictitious negative-degree G.

Write epsilon=r mod 2, m=(r−epsilon)/2. Since u_(2p+j)/t reduces to −j,
the lowest nonzero F_r coefficient reduces to the constant or linear
coefficient of the classical recurrence h_(n+1)=Y h_n+n h_(n−1). Thus

    d_r=(2m−1)!! for epsilon=0,
    d_r=(2m+1)!! for epsilon=1,
    F_r(a+tZ)/(d_r t^m a^epsilon) -> 1.

Every d_r is a p-unit because r<p. Higher X powers are suppressed by
2alpha−1>0. In the odd case, replacing a+tZ by a in the lowest linear
term is valid because 1−alpha>0. This explicitly checks the
coefficientwise statement rather than merely evaluating F_r at a.

Divide the full identity by

    N_r=2 kappa t^p d_r t^m a^epsilon,
    v(N_r)=L+m+epsilon alpha.

The first product reduces to Z^p+cZ. For even positive r, the second
product has excess at least h−1+alpha; for odd r, its excess is at least
h−alpha. Both are strictly positive. In particular,

    h−alpha=(p−3)/2+1/(2p),

whose smallest value is 1/6 at p=3. Consequently the full target
polynomial is integral after normalization and has exactly the claimed
residue Z^p+cZ. At the negative center, both kappa and the factor a in
the odd-r normalization are changed, so the same residual follows with
no parity sign missing. The candidate's transported residual is valid.

## 3. Root count, p=3, and the zero root

The residual derivative is the nonzero constant c. After a finite
residue-field extension it has p simple roots, explicitly i F_p when
i^2=−1. Simple-root Hensel lifting supplies p target roots in each of
the discs a+tO and −a+tO. The integral normalized polynomial need not
be monic for this local Hensel statement. Their discs are disjoint
because v(2a)=alpha<1. Thus there are 2p distinct inner roots, each of
valuation alpha. Distinct residual values give distance valuation 1
inside either cluster; opposite clusters have distance valuation alpha.

The outer scale tau^2=t gives

    P_(2p+r)(tau Y)/tau^(2p+r) -> Y^(2p) h_r(Y).

The identity follows from h_p=Y^p and the recurrence in characteristic
p; the same recurrence crosses the index 2p because its coefficient
there vanishes. For r<p, h_r'=r h_(r−1), and the nonzero recurrence
coefficients exclude common roots of consecutive h's. Thus h_r is
squarefree. It has a simple zero exactly for odd r; its corresponding
linear coefficient is r!!, a p-unit.

All r−epsilon nonzero residual roots lift to distinct outer roots of
valuation 1/2. Their pairwise differences have valuation 1/2. If r is
odd, parity makes P_(2p+r)(0)=0 exactly. This zero is distinct from
every already constructed root. The count

    2p+(r−epsilon)+epsilon=2p+r

then exhausts the degree with distinct roots. This proves that zero
is simple; it does not assume simplicity from odd parity or from the
high-multiplicity zero of the outer reduction. For even r the same
count without zero proves there is no zero root. This deals also with
r=0, where there are no outer roots and the accepted boundary is
recovered exactly.

At p=3, alpha=5/6 and L=11/2. For b=7, v(N_1)=19/3 while the joining
bound is 13/2, leaving 1/6. The roots are six inner roots and one
simple zero. For b=8, v(N_2)=13/2 while the joining bound is 22/3,
leaving 5/6. There are six inner and two outer roots. All estimates
apply at orders 9 and 27 and at every higher 3-power order.

## 4. Irreducibility and the discriminant

Automorphisms over the complete field K preserve its extended
valuation. The inner root set is therefore Galois-stable, and its
monic degree-2p root polynomial I_r lies in K[X]. Every inner root
is nonzero with valuation alpha. A proper monic K-factor of degree j
would have nonzero constant term of valuation j alpha in Z. Since
gcd(2p−1,2p)=1, this requires 2p to divide j, impossible when
0<j<2p. Thus I_r is irreducible. In particular P_(2p+1)/X is
irreducible. This statement uses the value group of K, not that of the
auxiliary splitting field, and does not claim full P_b irreducibility
when outer roots or zero are present.

Let n=r−epsilon. There are p(p−1) same-cluster inner pairs with
valuation 1, and p^2 opposite-cluster pairs with valuation alpha.
Their squared differences contribute p(4p−3). All distances involving
an outer root and a different root of another valuation are 1/2.
Distances from zero to inner roots, when zero exists, are alpha.
Consequently the complete discriminant valuation is

    p(4p−3)+n(n−1)/2+n(2p+epsilon)+epsilon(4p−2).

Substituting n=r−epsilon yields the candidate's formula exactly. The
derivative values computed from the same pair distances are

    inner: 2p−3/2+m+epsilon alpha,
    outer: (2p+r−1)/2,
    zero:  2p−1+m, if epsilon=1.

Their sum gives the same expression independently of the simplification
of the unordered-pair sum. For p=3 and b=6,7,8 the resulting values
are 27,37,40. These are t-normalized valuations, with v(3)=6 or 18
at orders 9 and 27, respectively.

## 5. Actual H transfer and bilinear kernel

The exact original-family identity is

    H_b(v^2;q)=v^b P_b(v+v^(−1);q).

It is checked independently here from the integer Gaussian recurrence,
not treated as a formal analogy. H_b(0)=1. Since every u_j lies in
the maximal ideal, P_b reduces to X^b. Odd residue characteristic
therefore makes P_b(2) and P_b(−2) units. At an H_b root choose v!=0
with v^2=z. Both maps v->v^2 and v->v+v^(−1) are unramified there:
the latter's only critical points are v=±1, giving the excluded
X=±2. The factor v^b is a local unit. Hence root multiplicity is
preserved and the proved P_b squarefreeness transfers to the actual H_b.

For w_k=product_(j=1)^k u_j, all required w_k are nonzero because
b<p^s. Consecutive P_b and P_(b−1) are coprime: any common root
propagates down the exact recurrence to P_0=1. The exact diagonal CD
identity, whose sign and normalization were independently checked, is

    sum_(k=0)^(b−1) P_k(x)^2/w_k
      =[P_b'(x)P_(b−1)(x)−P_b(x)P_(b−1)'(x)]/w_(b−1).

At a root of P_b both remaining numerator factors are nonzero, proving
the stated bilinear guard. These are ordinary squares, with no
Hermitian metric or positivity assumption. At b=0 there are no roots
and the assertion is vacuous. Algebraic nonvanishing in an injective
p-adic embedding implies nonvanishing at every primitive complex
embedding; no valuation is reinterpreted as a complex positivity claim.

## 6. Fresh exact controls and final limits

All **386 exact independent assertions passed** on the final run. The
candidate/source hash checks passed separately for all 72 distinct files.

The reviewer program was written from scratch. It imports no candidate
or historical checker. It reconstructs the actual recurrence and tail
blocks with sparse integer coefficients, at p=3,5,7,11,13 and every
0<=r<p. It checks the exact joining identities, preceding-block bound,
tail leading term, strict joining gap, outer recurrence, residual
squarefreeness, zero parity, degree count, and two derivations of the
discriminant expression.

For p=3,5,7 and every r it additionally forms the entire translated
polynomial, before imposing the auxiliary center relation:

    P_(2p+r)(A+TZ)
      −F_r(A+TZ)(g(A)^2−C)
      −2g(A)T^p d_r T^m A^epsilon (Z^p+cZ),

where g(A)=A^p+lambda A. Every remaining coefficient has weight strictly
above L+m+epsilon alpha with weight(A)=alpha, weight(T)=1, and
integer-coefficient weight p(p−1)v_p(coefficient). Substitution
g(a)=kappa and kappa^2=C gives the transported residual directly.
This tests all Z coefficients, including the constant; it neither
assumes a is an original root nor silently drops integer p-multiples.
Expansion is retained modulo T^(4p+1); omitted terms have weight at
least 4p+1, above every tested threshold.

The program also independently constructs the Gaussian H recurrence,
checks the exact H/P identity through degree 10, and checks the
denominator-cleared diagonal CD identity through degree 8. It computes
the actual symbolic discriminants of P_6,P_7,P_8, reduces modulo
Phi_9 and Phi_27, and computes their exact t-normalized valuations.
After rewriting each remainder in t=q−1 its degree is below e, so
the coefficient weights e*v_3(c_j)+j have different residues modulo
e; the unique minimum is the exact valuation, with no possible
minimum-weight cancellation. It additionally checks squarefreeness of
actual P_b and H_b by exact gcd computations in Q[q]/Phi_N for these
degrees and N=9,27, including the simple zero at b=7 and its absence
at b=8. The machine-readable control outcomes accompany this report.

The finite controls support transcription and specialization; Sections
1–5 and the exact accepted source inputs prove the unlimited theorem.
The tail unit used above fails at the next boundary r=p, so this review
does not extend the argument to b=3p. Any composition with an existing
all-A theorem remains restricted to where its other independent guard
is already available.
