# Rogers–Szegő overlap for b=19: ramified completion
12 October 2026 UTC

## Decision and scope

ACCEPT. The sealed independent replay is recorded beside the final archive. The eighteen ramified middle orders
45, 51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123, 129, 135, 141, 147
satisfy the original characteristic-zero overlap theorem for every primitive order-d root q and every integer A>=1. With the pinned accepted lower, unramified-middle and improved-tail inputs, the full b=19 overlap family holds for every odd d>19. No requested ramified order remains unresolved.

The reviewed immutable candidate is
RS_B19_Ramified_Middle_Overlap_CANDIDATE_2026-10-12.zip,
SHA256 30f0c89befe103b336ddf7d7110d15fbb74504209cdac518625f4792ad395c4a.
Its frozen exact certificate has SHA256
32783641b266bb43f72d427c62007fdaca9942658cb1bc57bf860a1285205fe4.
The candidate proof and source bytes were checked against this archive. The reviewer executed newly written review programs only. No candidate or historical mathematical program was imported or executed. No external service was written.

## 1 Original object and exact normalization

The original Rogers-Szego polynomial is H19(z;q)=sum_{j=0}^{19} [19 choose j]_q z^j=(z+1)U(z;q), with g=H19'(-1;q)=U(-1;q). The original product is
W=prod_{r=1}^{19}(1-q^r)/prod_{r=1}^{(d+19)/2}(1-q^(2r)).
The parameter remains tau=dW/g. The original overlap polynomial remains
J_{A+1}(x;tau)=x He_A(x)-A tau He_{A-1}(x),
where He_0=1, He_1=x, and He_{n+1}=x He_n-n He_{n-1}.

All Gaussian denominator lengths are at most 19<d. The W denominator length (d+19)/2 is less than d. Since d is odd, both q and q^2 have exact order d, so every original product factor is nonzero. The reviewer checks the individual factors by strict rational interval norm lower bounds as well as checking the relevant aggregate polynomial units modulo Phi_d. The derivative g is also a unit modulo every named Phi_d, and its interval norm is bounded strictly away from zero.

Put h=(d-1)/2, B9=prod_{r=1}^9(1-q^(2r)), E=prod_{r=1}^h(1-q^(2r)), s_j=prod_{r=1}^j(1-q^(2r-1))/(1-q^(2r)), and S_t=sum_{j=0}^t s_j. The exact derivative recurrence gives g=B9*S9 and E*Sh=d. Factoring the original W denominator into E and the odd factors 1,3,...,19 gives W=B9/E. Consequently tau=d/(E*S9)=Sh/S9. The factor d, the derivative sign, and the Hermite normalization are preserved.

The independent program reconstructs all Gaussian coefficient polynomials by the alternate Pascal recurrence [n,j]_q=[n-1,j]_q+q^(n-j)[n-1,j-1]_q. Every one of the twenty resulting polynomials is checked against the original product-quotient definition by exact cross multiplication over Q[q]. Direct differentiation gives the universal coefficient array of g, which exactly matches the frozen array.

At each order, a separate division-free prefix-numerator recurrence in Q[q]/(Phi_d) proves g=B9*S9 and E*Sh=d. It checks the uncancelled product equality W*E=B9, exact denominator units, and the original parameter residue d*W/g. Every rational coefficient of this residue matches the frozen candidate coefficient. Exact substitution q->q^(-1) also verifies tau differs from its complex conjugate. Thus parameter normalization is an algebraic equality, not a conclusion inferred merely from overlapping interval boxes.

## 2 Independent exact arithmetic evidence

The new reviewer engine uses 768-bit signed dyadic interval endpoints with explicit outward rounding. It is separate from the candidate's 512-bit functional engine. The reviewer proves pi=4(atan(1/2)+atan(1/3)): the two positive angles have sum below pi/2 and the tangent of their sum is one. Each arctangent has 620 alternating terms plus its first omitted-term bound. Separate sine and cosine factorial recurrences, through degrees 521 and 520 respectively, enclose the primitive root q=exp(2*pi*i*k/d). The remainder bound follows from the real-variable Taylor theorem with derivatives bounded by one. No floating-point value is used in a certificate or acceptance test.

The reviewer computes the Gaussian coefficients from their original product quotients, differentiates their sum at -1, and evaluates the original uncancelled W. It also evaluates the two prefix expressions independently. All three parameter routes produce squared-norm intervals with more than 400 bits of absolute precision. The new enclosures lie inside every saved candidate interval: root, E, B9, S9, Sh, original W numerator and denominator, W, original and polynomial derivatives, all three tau values, all three squared norms, and pi.

Every one of the 1,287 saved candidate complex-division norm guards is positive and independently strengthened. Their different evaluation order is reconciled by the named mathematical denominator, not by list position. All original product factors are additionally checked. The saved fresh results include each named guard with both rational norm endpoints.

The independent strict rational witness bounds are:
 d    k       lower rho       upper rho      side
 45  17        860/1000        861/1000       inner
 51  23       4744/1000       4745/1000       outer
 57  13       4491/1000       4492/1000       outer
 63  22       6660/1000       6661/1000       outer
 69  31      10954/1000      10955/1000       outer
 75  17      10198/1000      10199/1000       outer
 81   4       9628/1000       9629/1000       outer
 87  13      12840/1000      12841/1000       outer
 93  41      41512/1000      41513/1000       outer
 99  19      12539/1000      12540/1000       outer
105   4      13766/1000      13767/1000       outer
111  49      41912/1000      41913/1000       outer
117  46      19745/1000      19746/1000       outer
123  55      20590/1000      20591/1000       outer
129  29      17769/1000      17770/1000       outer
135  53      22801/1000      22802/1000       outer
141  62     216330/1000     216331/1000       outer
147  65      31250/1000      31251/1000       outer

Each lower<rho<upper is strict. The order-45 upper bound is below 1 by 139/1000; the smallest outer lower bound is above 8/3 by 5473/3000. Every k is coprime to d.

The run passed 154,132 assertions, including low-level interval-order and outward-arithmetic validity checks. It rejected 26 negative controls. Corruption controls reject a wrong Rogers-Szego degree, wrong prefix, finite-A replacement, wrong Hermite degree, lost factor d, ramified-modulo-three substitution, missing or duplicate order, wrong scale, incorrect inner-annulus side, nonprimitive root, false coarse or fine intervals, missing/zero/forged division guards, changed derivative or cyclotomic parameter coefficients, false root/parameter/pi enclosures, division through zero, and duplicate JSON keys. These are malformed-proof controls, not mathematical counterexamples to the valid theorem. Finite Hermite derivative and A=1,2 checks are diagnostics only.

## 3 The uniform theorem

The principal primitive root has v=pi/d and s_j=a_j exp(-ijv), with every a_j>0. Since hv<pi/2, S9 has positive real part. Since d>19, h>=10. Thus the imaginary part of (Sh-S9)*conjugate(S9) is the nonempty strictly negative double sum -sum_{j=10}^h sum_{r=0}^9 a_j a_r sin((j-r)v). This proves g nonzero and tau nonreal. Cyclotomic automorphisms commute with complex conjugation, so the nonzero algebraic difference tau-conjugate(tau) stays nonzero at every primitive embedding. This step transports neither signs nor norm bounds.

For A>=3 and nonreal tau, a multiple root at zero would require tau=0 when A is odd or tau=-1/A when A is even. Both are excluded. A nonzero multiple root x cannot make consecutive Hermite factors vanish, by recurrence descent to He_0=1. The differentiation identity
J'=(1+A*tau)He_A+A*x*(1-tau)He_{A-1}
therefore permits elimination, giving
y=x^2=tau*(A*tau+1)/(tau-1)=A*tau+(A+1)+(A+1)/(tau-1).

For A+1=2r+s with s in {0,1}, alpha=s-1/2, the Hermite factorial formula gives He_{2j+s}(x)=x^s P_j(x^2). The P_j recurrence has diagonal entries 4j+2alpha+2 and positive off-diagonals 2 sqrt(j(j+alpha)). Hence J=x^s det(x^2 I-M), where M is the real symmetric tridiagonal Jacobi matrix with the rank-one last-diagonal perturbation A(tau-1).

A nonzero multiple root produces a repeated eigenvalue y of M. The tridiagonal recurrence proves geometric multiplicity one and a nonzero last eigenvector coordinate u_r. A Jordan chain (M-yI)w=u exists. Complex symmetry, with bilinear transpose, gives u^T u=0, so 0<t=|u_r|^2/||u||^2<=1/2. Separately, the Hermitian inner product gives Im(y)=A Im(tau)t. Comparing with the rational expression for y, and dividing by nonzero Im(tau), gives
A*t=A-(A+1)/rho, rho=|tau-1|^2.
Thus 1+1/A<rho<=2+2/A<=8/3. All denominators and strict endpoints in this argument have been checked. There is no diagonalizability assumption. The derivation applies to every A>=3, rather than extrapolating from finite tests.

For A=1 and 2 the discriminants are 4*tau and 4*(1+2*tau)^3. Nonreality excludes their real exceptional parameters. Therefore the inner witness rho<1 or outer witness rho>8/3 proves the original discriminant nonzero for every A>=1.

For each fixed A, Disc_x J_{A+1}(x;T) lies in Q[T]. If it vanished at any primitive conjugate of tau, it would vanish at the certified conjugate. This is impossible. The same certified conjugate works for every A. Nonvanishing therefore holds at every primitive embedding. It then survives the injective map of the cyclotomic field into any characteristic-zero field containing q. The whole ambient field need not embed into C.

## 4 Composition with accepted inputs

The complete accepted source chain is retained in the sealed review. Both supplied accepted archive hashes match:
- b17 ramified acceptance: dad5faf9d288dbd9ba2f77607405e8f514617a7b3e3a80454a463f9d1a1063d0
- b19 unramified-middle acceptance: a261b4b5a0f0e82689c78560a5cfdf666439a8258321193928f359da3c018e05

The inherited general lower-strip source is exactly
RS_General_Odd_Guards_Independent_Review_ACCEPT.tex,
SHA256 c4009870cdb96f0af09065b4e41e98346d8159cc3962d7954a92b73963b2e78c.
It states the general odd-b lower strip b<d<=2b+1 for every A>=1. For b=19 this covers odd d=21..39, including rho=1 at the endpoint where relevant. The critical annulus has strict lower endpoint above 1, so that endpoint is allowed.

The improved-tail source is exactly
RS_Degree_Nine_Overlap_Independent_Review_ACCEPT.tex,
SHA256 4f3ef60634b8bc1962e22d28ad3d5254b9d9ce49d21c749040db131a92835a79.
Despite its filename, its accepted tail theorem is explicitly general in odd b. The range is d>=15(b+1)/2, giving odd d>=151 at b=19. Its strict bound |tau|^2>131/18 yields rho>8/3; the exact comparison is (101/18)^2-4*(131/18)=769/324>0.

The middle contains exactly 55 odd orders 41..149. The pinned b19 unramified acceptance covers exactly the 37 orders coprime to three. The eighteen new orders are their disjoint complement. No endpoint is missing. The full b19 overlap conclusion follows by this composition. The unramified theorem is not generalized to every unbounded unramified order without the lower/tail inputs. Its d=121 bad-prime example continues to exclude every-prime-good wording.

The source audit independently checks seven complete archive manifests and CRCs, the seven current candidate source pins, and twelve inherited b17 candidate pins. It traces the general lower/tail texts through the accepted b17, general-prime, b15 accepted and b15 candidate source chain. Copied source titles alone are not treated as sufficient provenance.

## 5 Scope and remaining work

Full accepted overlap families now include b=1,3,5,7,9,11,13,15,17,19. The remaining general overlap region is odd b>=21 with odd 2b+1<d<15(b+1)/2, except separately proved instances. The b19 middle complement is empty.

Ordinary residual squarefreeness is a separate guard. Its accepted domains remain odd b<=25 at every odd d>b, and odd b>=3 at odd d>=4b^2. Its unresolved general region remains odd b>=27 with b<d<4b^2, except separately proved instances. The accepted general derivative-nonzero and separation guards remain distinct.

The general F020 remaining-guards problem remains open. This advances the accepted odd-b overlap frontier through b=19; it does not settle the general overlap or ordinary-residual problem, or establish historical priority.

Even orders, nonprimitive roots, A=0, positive-characteristic squarefreeness, quantitative conditioning, worldwide novelty and historical priority are not proved. A characteristic-three field contains no element of order divisible by three, so the unramified prime criterion cannot be substituted for this ramified characteristic-zero proof. No finite-A extrapolation is used.

## 6 Reproducibility and seal

The sealed review includes this report, complete fresh rational results, the independently authored arithmetic and source-audit programs, the original frozen candidate ZIP (which itself contains both complete accepted source ZIPs), integrity evidence, and a payload manifest. The clean replay verifies the review ZIP digest, safe paths and complete manifest, extracts the frozen candidate certificate as data only, reruns the two new reviewer programs, and requires byte-for-byte equality with the saved outputs. Its receipt is external to the sealed ZIP to avoid a self-referential hash. All source programs remain inert.

Derivative note: the title identifies b=19 as the Rogers–Szegő parameter; the overlap polynomial has degree A+1. Private record instructions and administrative counts are omitted. The original proof, exact witnesses, accepted-source composition and remaining mathematical limits are unchanged. Original report SHA-256: `0386e37b934123b9e82449503c1d53ffc7b36db81c87a16e58bb1244505eb401`.
