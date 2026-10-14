# Independent proof-review addendum: pinned-singleton field-sensitive bank minimum

13 October 2026. **Verdict: ACCEPT for the precisely defined pinned-singleton model below.**

This is a separate result from the twelve-bank witness-only acceptance. It adds a narrowly scoped optimality theorem by combining the independently verified rank-five obstruction with that witness. It does not alter or silently enlarge the earlier witness-only archive. Historical novelty is unresolved.

## Exact reviewed edition and dependency boundary

This addendum reviews the pinned theorem and proof in sections 2–5 of FIELD_SENSITIVE_THEOREM.md, frozen SHA-256 404377f23eb474dca692575b6e531d866b32ac796d9fb0b69426468a4b157231. The exact reviewed text is included as FUSION_SOURCE_REPORT.md. Its numerical matrix, moments, minor, polynomial, and field condition agree with this review. The source's bibliographic discussion and publication assessment are not independently accepted by this mathematical proof review.

The full original-bank witness is bound to the separate archive Signed_Bank_Twelve_Extension_Field_Independent_ACCEPT_2026-10-13.zip, SHA-256 8fb11c6c9e90bdcf3d1a526821431cf41813dc2d351bf972395c322326165a46. Exact bytes are included as WITNESS_ACCEPTANCE.zip. The witness-only seal remains unchanged. Its standalone independent checker, cold replay, and exact results supply the arithmetic dependencies used here. No candidate, historical, or fusion-worker scientific program was executed for this addendum.

## 1. Model and exact theorem

Let K be any field extension of F23. Fix N=11, q=13, the standard matrices S e_t=e_(t+1 mod 11), T e_t=13^t e_t, and the negative Fourier matrix F[k,t]=13^(-kt).

Allowed banks are exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1),

where epsilon,delta are independently +/-1, alpha,beta and all eleven raw weights lie in K, and Delta=1-alpha^11-beta^11 is nonzero. No transformed target, additional generator, or derivative atom is allowed.

For each orientation, combine the sector-amplitude vectors of banks with the same alpha. An effective alpha node is a combined group whose sector-amplitude vector is not identically zero. Require exactly one effective alpha node in each cross-sign orientation (-,+) and (+,-), and require both of those nodes to be alpha=4. There is no restriction on the number of original physical banks that realize a combined node, or on their legal beta values.

Define b4(K) to be the minimum number of actual original banks in a representation of F satisfying these conditions. If no such representation exists, set b4(K)=infinity.

Then:

1. b4(K) >= 12 for every field extension K/F23.
2. If K contains an F23-subfield isomorphic to F23^5, then b4(K)=12.
3. If K contains no such subfield, then b4(K)>=14.

In particular, for each positive integer d,

    b4(F23^d) = 12    if 5 divides d,
    b4(F23^d) >= 14  if 5 does not divide d.

The second line is a lower bound. Fourteen-bank attainment has not been proved here. The result fixes both cross-sign singleton nodes at 4; it is not an optimum over free singleton choices or over unrestricted architectures.

## 2. Coefficient identity and necessary moment windows

For U=S^epsilon, V=T^delta, write VU=q^(epsilon delta) UV. Expanding in ordered monomials U^r V^ell gives Gaussian coefficients D_(epsilon,delta)(r,ell), supported on r+ell<=10. The mixed terms in degree eleven vanish, so X_j^11=(alpha^11+beta^11)I for X_j=alpha U+beta q^(epsilon delta j)V. The original inverse equals (I+X_j+...+X_j^10)/Delta.

At the Weyl coefficient W_(a,b)=S^a T^b, a bank therefore contributes

    alpha^r G_(epsilon,delta)(a,b) H_(epsilon,delta,alpha,b),

where r=[epsilon a]_11, ell=[delta b]_11, G is the ordered Gaussian coefficient at (r,ell), and the sector amplitude H absorbs beta^ell, 1/(11 Delta), and the original raw-weight Fourier sum. Combining banks at the same alpha changes H by addition. This algebra is valid for alpha=0 and beta=0 with the ordinary zeroth-power convention.

Direct target extraction gives C*f(a,b), where C=18 is nonzero and f(a,b)=13^(3(a+b)^2). Divide coefficient equations by C; this is scalar notation for coefficients, not a transformation of the target or legal bank.

At (a,b)=(11-b,b), b=1,2, only the (-,+) orientation survives. Since its effective singleton alpha is 4, its normalized amplitude is forced. Fresh exact computation gives T_1=22 and T_2=20.

For b<=a<=10-b, both negative-delta orientations vanish and G_(+,+)(a,b) is nonzero. Hence the original coefficient equations force

    v_b(a) = [f(a,b)-T_b*4^(11-a)*G_(-,+)(a,b)] / G_(+,+)(a,b)
           = sum_(x in X) A_(b,x) x^a,

where X is the set of distinct nonzero effective (+,+) alpha nodes. Any zero-alpha group contributes zero on these strictly positive exponent windows. Repeated nodes only combine amplitudes; they do not introduce derivative atoms.

The independently verified sequences are

    b=1, a=1,...,9: 19,4,20,14,20,3,14,16,8;
    b=2, a=2,...,8: 21,15,14,11,13,22,19.

Their four and two consecutive length-six windows form

        19  4 20 14 20  3
         4 20 14 20  3 14
    M = 20 14 20  3 14 16
        14 20  3 14 16  8
        21 15 14 11 13 22
        15 14 11 13 22 19.

The first-five-row/column determinant is 3 in F23, while every row annihilates (6,4,18,1,8,1)^T. Thus rank(M)=5 and its kernel over F23 is one-dimensional. The same rank and kernel description hold after extending scalars to any K. Its unique monic degree-five kernel polynomial is

    g(t)=t^5+8t^4+t^3+18t^2+4t+6.

All of these numerical premises were independently rebuilt from the original grammar, not merely quoted from the candidate.

## 3. Lower bounds over arbitrary extension fields

Let m=|X| and suppose m<=5. Define the ordinary distinct-node annihilator

    h(t)=product_(x in X)(t-x),
    p(t)=t^(5-m) h(t).

The empty product is 1 if m=0. This p is monic of degree five. For any selected moment window starting at a,

    sum_(k=0)^5 p_k v_b(a+k)
      = sum_(x in X) A_(b,x) x^a p(x) = 0.

Therefore the coefficient vector of p lies in ker(M). Monicity and the one-dimensional kernel imply p=g. Since g(0)=6 is nonzero, m<5 is impossible. Thus every representation has at least five distinct nonzero effective (+,+) nodes. If m=5, then p=h=g, so g must split into five distinct linear factors over K. If g does not split over K, even m=5 is impossible, giving at least six such nodes.

Each distinct effective nonzero alpha requires at least one actual bank in that orientation. Additional zero-alpha nodes, repeated-alpha banks, or zero banks cannot weaken this counting lower bound.

Now let J e_t=e_(-t mod 11). Then JSJ=S^-1, JTJ=T^-1, and JFJ=F. Conjugating a legal bank maps (epsilon,delta) to (-epsilon,-delta), leaves alpha,beta and its original phase product epsilon*delta unchanged, and preserves its nonzero denominator. The two pinned cross-sign nodes remain 4. Applying the same (+,+) argument to the reflected representation proves the identical lower bound for (-,-).

Each cross-sign orientation contributes at least one actual bank because it has a nonzero effective singleton group. Hence every representation has at least 5+1+1+5=12 actual banks. If g does not split over K, it has at least 6+1+1+6=14 actual banks. If no representation exists these inequalities remain valid under the infinity convention.

## 4. Field embedding and attainment of twelve

The independently verified polynomial g is irreducible of degree five over F23. Therefore L=F23[t]/(g) is a field with 23^5 elements. Its five roots are the distinct Frobenius conjugates z,z^23,z^(23^2),z^(23^3),z^(23^4).

For any extension K/F23, the following are equivalent:

- g has a root in K;
- there is an F23-embedding L -> K;
- K contains an F23-subfield of size 23^5;
- g splits completely over K.

A root induces the injective quotient map L -> K because g is irreducible. The image is a subfield of size 23^5, and contains all Frobenius conjugates of that root, so all five roots lie in K. Conversely, a subfield with 23^5 elements is F23-isomorphic to L, and transports its roots into K. Complete splitting trivially supplies a root.

The separate accepted witness gives twelve original legal banks over L, with exactly the required orientation counts and pinned cross-sign nodes. Applying any F23-embedding L -> K to every parameter and raw weight preserves nonzero denominators, every inverse identity, the nonzero bank matrices, and the target F (whose entries lie in F23). This yields b4(K)<=12 whenever the equivalent field conditions hold. Combined with the lower bound, b4(K)=12 there.

For K=F23^d, it contains the degree-five subfield exactly when 5 divides d, giving the stated finite-extension corollary.

## 5. Review status, cost, and next priority

ACCEPT applies to this proof and the exact pinned model stated above. It does not establish a minimum after allowing either cross-sign node to vary, fourteen-bank attainment over F23, an all-N formula, characteristic-zero behavior, or historical novelty.

The optimum twelve counts original banks as mathematical objects. It says nothing about operation count: the explicit witness contains 132 branch inverses over a degree-five field. Supplying roots or an abstract field embedding does not provide free numerical evaluation. No FFT speed conclusion follows.

Next priority: **86/100**, determine whether the pinned base-field lower bound fourteen is attained, by producing and independently checking an explicit original-grammar witness or proving a stronger obstruction. Treat any such attainment as a separate result.
