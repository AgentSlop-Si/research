# ALG-036: fresh source-bound acceptance of the all-radius scalar completion

20 October 2026 UTC. Verdict: **ACCEPT the strict ratio log-convexity theorem, unique nondegenerate interior scalar minimum, and full endpoint-only global classification at the frozen bytes below.** No mathematical correction is required.

I reconstructed every new analytic step independently from the explicitly unproved lead before receiving the completion author's candidate. I then compared the frozen proof with that reconstruction. No new essential lemma or proof repair was supplied to the author. I have not edited any accepted source or the candidate, published anything, or made an external mutation.

## Frozen candidate and dependencies

Historical candidate packet: identified by provenance/original_manifests/completion.json; public proof: candidate/PROOF.md.

- `candidate/PROOF.md`: SHA-256 `47793701643f3bd803897fd22468c7896519e4c2041c5ec36a5d02737bf4dcb2`.
- `MANIFEST.json`: SHA-256 `54006ad6fddd89985a2610457e3ea70841a1e22c5dbaa99e9885c4dd3856038e`.
- `controls/exact_controls.py`: SHA-256 `2d3a0276aa778798f1a3c164b0dae2b91c32c0835c579549f9635135ea682ef3`.
- All nine manifest entries match their declared bytes and hashes, as do all nine explicit source bindings.

The previously accepted scalar proof remains SHA-256 `502d0551a661fe9424775aa83c10858929c9ba9da4e966a2133b48a953789c32`, and its fresh acceptance remains SHA-256 `e85dc6ae11d0e563dd63d85ff21c7ca277c136fe03dc6f0b1dc523dcede7373b`. Their manifests and all declared inherited source bindings were independently checked. The all-radius largest-pair reduction is used as an already accepted dependency, not silently reproved here.

The exact scope accepted for every finite a>0 is:

1. `(log(N/P))''>0` for every 0<t<1/sqrt(2), using the actual proper-complex Gaussian N and P.
2. Exactly one interior scalar stationary point, which is a nondegenerate strict minimum; the derivative is negative before it and positive after it.
3. Every interior scalar point is strictly below the larger endpoint value, including when the endpoints tie.
4. Combined with the accepted strict structural reduction and boundary classification, the global maximizing normal weights are, modulo phases and permutations, exactly `(0,1/2,1/2)` below the unique transition a_*, exactly `(1/3,1/3,1/3)` above it, and precisely both types at a_*.
5. The previously accepted endpoint crossing, with 1/2<a_*<2, is therefore the global transition; the original radius is r=sqrt(a).

The prior packet's historical statement that the full optimizer was then unresolved remains untouched. This separate verdict is the new completion disposition.

## Original model, ratio, and differentiations

The Gaussian frame and derivative in the previously accepted scalar packet retain the proper-complex density, radius R=sqrt(2a), and shift d=tv. They give

P(t)=a t exp(-a(1+t^2)) ell(sqrt(a)t),
N(t)=integral_0^sqrt(a) v^2 exp(-(1+t^2)v^2) h(tv) dv,
Phi'(t)=2(P(t)-N(t)),

with h=-ell'>0. Both P and N are strictly positive for 0<t<=1/sqrt(2). Writing L=log ell and H=log h, and using the probability density proportional to the integrand defining N, gives

(log(N/P))''=1/t^2+2a-a L''(sqrt(a)t)
  +E[-2v^2+v^2 H''(tv)]+Var(-2tv^2+vH'(tv)).

This follows by differentiating an integral on a fixed bounded interval. Inherited analytic smoothness supplies domination, including v=0. The signs and a scaling are correct.

The joint set {(z,d): |z+d|<=R, |z-d|<=R} in R^2 times R is convex. Multiplying its indicator by exp(-|z|^2) gives a jointly log-concave function, and marginal log-concavity gives L''<=0 on the positive physical interval. The even geometric lens need not be differentiable at zero; the argument uses only its smooth positive branch.

The exact fixed-domain formula is

h(d)=(4/pi) exp(-R^2-d^2) sqrt(R^2-d^2)
  integral_0^1 exp(2d sqrt(R^2(1-s^2)+d^2s^2)) ds.

For A,B>=0, d sqrt(A+Bd^2) is convex for d>=0. Thus Holder gives log-convexity of the displayed integral. Differentiating the remaining logarithmic factors proves

H''(d)>=-2-(R^2+d^2)/(R^2-d^2)^2.

At x=t^2 and m=E[v^2], monotonicity of (R^2+d^2)/(R^2-d^2)^2 for 0<=d<=sqrt(a)t gives

(log(N/P))'' >= 1/x+2a-(4+g(x)/a)m,
g(x)=(2+x)/(2-x)^2.

One can retain -a L'' on the right when needed. The discarded variance is nonnegative, not nonpositive.

## Second moment 3a/5

After v=sqrt(a)y and the fixed-domain h substitution, the relevant weights are positive mixtures in s of y^2 b_s(y), where

b_s(y)=sqrt(2-t^2y^2) exp(a f_s(y)),
f_s(y)=-(1+2t^2)y^2+2t y sqrt(B+Cy^2),
B=2(1-s^2), C=t^2s^2.

For G(y)=y sqrt(B+Cy^2), exact differentiation gives

G''=Cy(3B+2Cy^2)/(B+Cy^2)^(3/2),
G'''=3B^2 C/(B+Cy^2)^(5/2)>=0.

Moreover G''<=2sqrt(C). For B,C>0 this follows after z=sqrt(C/B)y by the exact squared difference 4(1+z^2)^3-z^2(3+2z^2)^2=4+3z^2>0. Degenerate C=0 is immediate; B=0 gives G=sqrt(C)y^2 explicitly, including y=0. Hence f_s''<=-2(1+2t^2)+4t^2s<=-2. The logarithm of the square-root prefactor is also concave. Therefore b_s is log-concave, so its superlevel sets are intervals.

Because G' is convex, its mean on a centered subinterval [y,1-y] is at most its mean on [0,1]. One direct justification pairs G'(r)+G'(1-r); this paired sum is nonincreasing as r increases from 0 to 1/2 because its derivative is G''(r)-G''(1-r)<=0. Removing outer pairs cannot raise the mean. Thus

G(1-y)-G(y) <= (1-2y) G(1), 0<=y<=1/2.

Furthermore G(1)=sqrt(2(1-s^2)+t^2s^2)<=sqrt(2), and

-(1+2t^2)+2sqrt(2)t=-(sqrt(2)t-1)^2<=0.

It follows that f_s(1-y)<=f_s(y). The decreasing square-root prefactor preserves b_s(1-y)<=b_s(y).

For a nonempty superlevel interval with endpoints alpha,beta, this reflection implies alpha+beta<=1. If beta<=1/2 that is immediate; otherwise reflection of beta into the same closed superlevel set gives alpha<=1-beta. Open endpoints or singleton levels do not affect integration.

Put q(z)=z^3(1-z^2), which is increasing then decreasing on [0,1], with its only interior maximum at sqrt(3/5). For alpha<=1/2 and beta in [alpha,1-alpha], the minimum of q on this interval occurs at one of its endpoints. Also

q(1-alpha)-q(alpha)=alpha(alpha-1)(2alpha-1)(alpha^2-alpha+2)>=0.

Consequently q(beta)>=q(alpha), or beta^5-alpha^5<=beta^3-alpha^3. Thus

integral_alpha^beta y^4 dy <= (3/5) integral_alpha^beta y^2 dy.

Layer-cake integration over the superlevel intervals proves the same inequality with weight b_s. Tonelli then proves it for the positive s mixture. Hence m<=3a/5. Unimodality by itself would not suffice; reflection and interval superlevels are essential.

The ratio-curvature lower bound becomes

1/x-(2/5)a-(3/5)g(x).

Since g is increasing, g(1/2)=10/9, this is strictly positive for 0<a<=10/3 and 0<x<1/2. At the excluded corner a=10/3,x=1/2 it is zero, so the open interval must be stated correctly.

## Integration by parts and all large a

Write u=sqrt(R^2-d^2) and J=integral_0^u exp(2d sqrt(R^2-y^2))dy. Its moving endpoint gives

H'(d)=-2d+2 E_J[sqrt(R^2-y^2)]-(d/u) exp(2d^2)/J <= 2R-2d.

The endpoint term has a minus sign. With w(v)=v^2 exp(-(1+x)v^2)h(tv), integrate (v w)' from zero to sqrt(a). Its upper boundary value is strictly positive. Substituting the upper bound on H', then Cauchy-Schwarz, yields

2(1+2x)m <= 3+2sqrt(2axm).

The inequality direction is correct: replacing H' by an upper bound makes the nonnegative boundary identity still larger. It is not legitimate to set this boundary term to zero.

Define B0=(1/x+2a)/(4+g(x)/a) and K=2(1+2x)B0-3. If K>0 and K^2-8ax B0>0, then the positive quadratic root bound above forces m<B0. Indeed, the quadratic in sqrt(m) has constant -3 and only one positive root, and its value at sqrt(B0) is strictly positive.

I independently substituted a=4+b and x=z/[2(1+z)], b>=0,z>0. The numerator of K has 14 positive coefficients and positive constant 128; its denominator is

z(z+1)(18bz^2+48bz+32b+77z^2+201z+132)>0.

The numerator of K^2-8axB0 has 42 positive coefficients and constant 16384; its denominator is the square of that K denominator. Full exact coefficients are in INDEPENDENT_CONTROLS.json. This proves the required signs for every a>=4, 0<x<1/2, not merely sampled radii. The omitted endpoint x=1/2 was separately checked by direct substitution, though it is unnecessary for the open-interval log-convexity theorem.

## Uniform compact gap

For a<=4 and x<=4/9, the 3a/5 bound is at least

9/4-8/5-(3/5)(99/98)=43/980>0.

It remains to consider 10/3<a<4 and 2/3<t<1/sqrt(2), where 0<d=sqrt(a)t<R/2.

For the moving-boundary J formula, its weighted mean of sqrt(R^2-y^2) is at least pi R/4. First truncate the uniform interval [0,R] to [0,u], which removes only the smallest values of that decreasing function; then tilt by exp(2d times that function), which can only increase its mean. The latter fact follows from the nonnegative covariance of two increasing functions of the same variable. Also J>=u exp(2d^2), so the magnitude of the endpoint term is at most d/(R^2-d^2)<=2/(3R). Hence

H'(d)>=R(pi/2-1)-2/(3R).

Restricting the positive integral defining h to [0,R/3] gives

h(d)>=4R/(3pi) exp(-R^2-d^2+(4sqrt(2)/3)Rd).

The restriction is legal because sqrt(R^2-d^2)>=sqrt(3)R/2>R/3. Its exponent is a[-2-t^2+(8/3)t]. This bracket is increasing in the required t interval and equals -2/3 at t=2/3. Since a<=4, the exponent is at least -8/3.

The rational constants satisfy R>18/7 and 25/8<pi<22/7. A wholly rational certificate for exp(8/3)<15 is its Taylor sum through degree three plus the geometric upper bound on the remaining tail:

sum_{k=0}^3 (8/3)^k/k! + [(8/3)^4/4!]/(1-8/15)=8447/567<15.

Therefore h>4/55 and H'>81/56-7/27=1795/1512>0. In particular h'=h H' is positive. Since ell<=1 and

-L''=h'/ell+(h/ell)^2>=h',

we have -a L''> (10/3)(4/55)(1795/1512). The 3a/5 lower bound without this term is at least -4/15. The resulting strict margin is

(10/3)(4/55)(1795/1512)-4/15=659/31185>0.

This is a single uniform compact-box proof, not a radius ladder.

## Scalar consequence and endpoint classification

Set F(t)=log(N/P). Accepted endpoint facts give F(t)->+infinity as t->0+, F(t0)=0, and F<0 immediately left of t0. Strict positive F'' on the open interval implies exactly one other zero tm: existence follows by continuity and the sign change, and a third zero would contradict strict convexity using the outer two zeros. Convexity and continuity at t0 make F<0 between tm and t0 and F>0 to the left of tm. Moreover F'(tm)<0 because its secant slope to t0 is zero and F''>0. Thus the interior derivative root is simple, with Phi''(tm)=-2P(tm)F'(tm)>0.

Since Phi'=2P(1-exp(F)), Phi decreases strictly on (0,tm) and increases strictly on (tm,t0). Every interior point is strictly below at least one endpoint, hence strictly below their maximum. The accepted unique endpoint crossing therefore becomes the global transition after combining this scalar result with the accepted structural reduction. The block endpoint wins below the crossing, the symmetric endpoint above, and precisely both endpoint orbits win at the crossing.

## Frozen-proof comparison, primary source, and replay

The candidate contains all the steps reconstructed above, including the essential reflection property, degenerate s=1 and y=0 cases, the nonzero integration-by-parts endpoint, strict polynomial numerator positivity, positive denominators, and the closed compact-gap bound. The finite controls are not used in place of these analytic arguments.

I separately checked the author's exact positive-coefficient rows against my independently reconstructed rational expressions, not merely against the author's generated certificate. The 14 nonzero K numerator coefficients and 42 nonzero D numerator coefficients agree. The substitution covers the entire open physical x interval and all a>=4.

The candidate uses a different valid exponential-tail certificate from my independent one: it truncates through degree six and bounds the tail by a geometric series with ratio 1/3, obtaining 3306347/229635<15. Its four-term arctangent lower certificate gives pi>1538665/489888>25/8. The positive-integral upper certificate gives pi<22/7. I independently verified all of those rational identities and inequalities.

The cited marginal log-concavity result was checked directly in [Prékopa's 1973 paper, Theorem 6 on printed page 342](https://acta.bibl.u-szeged.hu/14411/1/math_034_335-343.pdf). It applies to a jointly log-concave function integrated over a convex set in the marginalized coordinates. Taking that set to be R^2 proves exactly the lens claim used here. The indicator's convex support is valid, and differentiation is restricted to the smooth positive branch, not the geometric cusp at zero.

The author's full 85-control script was replayed only in a separate copy in a temporary directory; all three generated outputs were byte-identical to the frozen outputs. The candidate itself was not modified. My own `independent_controls.py` records 143 passing exact controls covering the new analytic algebra, both alternative constant certificates, the Gaussian normalization, all candidate coefficient rows, and candidate/inherited source integrity. No floating optimization, numerical quadrature, finite radius census, or root sampler enters this verdict.

## Adversarial failure modes excluded

- Substituting a real-Gaussian measure or a different radial normalization.
- Losing the factor a or reversing a sign in the log-ratio curvature identity.
- Confusing log-concavity of the lens with log-convexity of the fixed-domain boundary-density integral.
- Omitting or reversing the moving-boundary term in h'.
- Dropping the strictly positive integration-by-parts upper boundary.
- Inferring m<=3a/5 from a merely unimodal density.
- Assuming centered averages behave monotonically without the verified convexity of G'.
- Losing the reflection property or failing to handle endpoint superlevel sets.
- Squaring the large-a certificate without first verifying K>0.
- Clearing a denominator of unknown sign or claiming the z substitution includes x=1/2.
- Replacing the compact parameter gap with finite radius sampling.
- Using -L''>=h' without first establishing h'>0 and ell<=1.
- Inferring unique global optimization from endpoint comparison alone.
- Omitting ties, permutations, phases, boundary maximizers, or the a=r^2 conversion.

None produces a defect in this frozen proof. The bounds cover 0<a<=10/3, a>=4, and the whole intervening compact range, with no uncovered endpoint or parameter seam. The root-count argument uses actual strict convexity and endpoint signs, not the older finite stationary-root bound.

## Review independence and disposition

Before freeze, substantive verification findings were reported separately from the author; direct communication with the author was confined to independent-reconstruction status and frozen source identities. The author supplied no proof assistance to this reviewer, and this reviewer supplied no structural lemma or repair to the author. The original unproved lead is the common research object, not an accepted theorem dependency. The independent reconstruction was written before the frozen candidate arrived and is preserved separately.

The acceptance is conditional only on the explicitly bound previously accepted structural and endpoint results in the usual dependency sense. There is no remaining scalar analytic obstruction, no required proof amendment, and no authorization or execution blocker. This is an acceptance of the frozen mathematical completion, not a claim of historical novelty or permission to publish.
