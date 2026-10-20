# ALG-036: strict log-convexity closes the Gaussian scalar optimizer

Date: 20 October 2026 UTC. Status: new candidate theorem, frozen for fresh
adversarial review. This is a separate completion packet. No previously accepted
artifact is changed or silently reclassified.

## 1. Contract, theorem, and accepted dependencies

For every finite a>0 retain the proper-complex Gaussian model

    F_a(q)=Pr(max_j |Z_j|<=sqrt(a)),
    Z~CN(0,I-uu*), u_j=sqrt(q_j), q_j>=0, sum_j q_j=1.

The intrinsic density is pi^(-2)exp(-||z||²) on the complex two-plane. The accepted
strict largest-pair smoothing and boundary classification reduce the global
maximum, modulo coordinate permutations and phases, exactly to

    f_a(c)=F_a(c,(1-c)/2,(1-c)/2), 0<=c<=1/3.

Write t=sqrt(c/(1-c)), t_0=1/sqrt(2), and Phi_a(t)=f_a(t²/(1+t²)).
Use rho=sqrt(2a) for the lens radius, to distinguish it from the ratio below.
The accepted scalar packet supplies

    ell(d)=Pr(|Y+d|<=rho and |Y-d|<=rho), Y~CN(0,1),
    h(d)=-ell'(d)
        =(4/pi)e^(-rho²-d²)
          integral_0^sqrt(rho²-d²) e^(2d sqrt(rho²-y²))dy,
    P(t)=a t e^(-a(1+t²)) ell(sqrt(a)t),
    N(t)=integral_0^sqrt(a) v² e^(-(1+t²)v²)h(tv)dv,
    Phi_a'(t)=2(P(t)-N(t)).

The lens and h are positive and smooth on the ranges used here, including
0<=d<=rho/2. P,N>0 for 0<t<=t_0. Define

    R_a(t)=N(t)/P(t).

**New theorem.** For every a>0,

    (log R_a)''(t)>0, 0<t<t_0.                         (1.1)

Consequently there is exactly one interior stationary point t_m(a) in (0,t_0).
It is a nondegenerate strict minimum:

    Phi_a'(t)<0 for 0<t<t_m(a),
    Phi_a'(t)>0 for t_m(a)<t<t_0,
    Phi_a''(t_m(a))>0.

In particular every interior scalar point is strictly below the larger endpoint
value. The full global optimizer of F_a is therefore an endpoint of the reduced
branch, with no additional maximizing normal.

The already accepted endpoint theorem gives exactly one a_* in (1/2,2) with

    B(a_*)=S(a_*),
    B(a)=(1-e^(-a))(1-e^(-2a)),
    S(a)=F_a(1/3,1/3,1/3).

Thus, modulo permutations and coordinate phases, the global maximizers are

- q=(0,1/2,1/2) for 0<a<a_*;
- q=(1/3,1/3,1/3) for a>a_*;
- exactly these two types for a=a_*.

The maximum is max(B(a),S(a)). The endpoint crossing is transverse, by the
accepted theorem. If the original threshold is r=sqrt(a), the transition is
r_*=sqrt(a_*), with 1/sqrt(2)<r_*<sqrt(2).

Accepted dependencies, their prior fresh reviews, and exact hashes are in
`SOURCE_BINDINGS.json`. The prior scalar acceptance does not cover any new
inequality in this packet. The unproved lead is recorded as provenance only,
not as a theorem dependency. The elementary convexity implication completing
the optimizer is proved in Section 9, not assumed from a plot or root census.

## 2. Exact logarithmic curvature identity

Set L=log ell and H=log h. For fixed t, let E_t denote expectation on
0<v<sqrt(a) with density proportional to

    w_t(v)=v² e^(-(1+t²)v²)h(tv),

and let m=E_t[v²]. The integration interval is fixed and finite. Because h is
positive and smooth on a neighborhood of the compact physical range, all the
following differentiations are justified by uniform domination on any compact
t subinterval of (0,t_0]. The v=0 endpoint causes no problem: w_t vanishes
quadratically there, while H and its derivatives remain bounded.

Define the score

    s_t(v)=partial_t log w_t(v)=-2tv²+vH'(tv).

Direct differentiation of the normalized integral gives

    (log N)''=E_t[-2v²+v²H''(tv)]+Var_t(s_t).

Also

    log P=log a+log t-a(1+t²)+L(sqrt(a)t),
    (log P)''=-1/t²-2a+aL''(sqrt(a)t).

Subtracting proves the exact identity

    (log R_a)''
      =1/t²+2a-aL''(sqrt(a)t)
       +E_t[-2v²+v²H''(tv)]+Var_t(s_t).              (2.1)

No sign estimate has yet entered this identity.

## 3. The lens and boundary-density curvature bounds

### 3.1 Log-concavity of the lens

The set

    K={(y_1,y_2,d):
         (y_1+d)²+y_2²<=rho²,
         (y_1-d)²+y_2²<=rho²}

is convex: each constraint is the inverse image of a Euclidean ball under a
linear map. Hence the function

    (1/pi)e^(-y_1²-y_2²) 1_K(y_1,y_2,d)

is log-concave on R³. Marginalizing in (y_1,y_2) proves log-concavity of the
physical, even lens function in d. This is an application of Prékopa's
marginalization theorem, Theorem 6, printed page 342 of
[On logarithmic concave measures and functions (1973)](https://acta.bibl.u-szeged.hu/14411/1/math_034_335-343.pdf).
Only its restriction to d>0 is differentiated; no even analytic continuation
through the cusp at zero is asserted. On 0<d<rho,

    L''(d)<=0.                                       (3.1)

### 3.2 A log-convex factor of h

The substitution y=s sqrt(rho²-d²) in the accepted h integral gives

    h(d)=(4/pi)e^(-rho²-d²)sqrt(rho²-d²) I(d),
    I(d)=integral_0^1
       exp(2d sqrt(rho²(1-s²)+d²s²))ds.              (3.2)

For A,B>=0 the function d -> 2d sqrt(A+Bd²), d>=0, is convex. For positive
A+Bd² its second derivative is

    2Bd(3A+2Bd²)/(A+Bd²)^(3/2)>=0.

The degenerate cases A=0 or B=0 follow directly or by continuity. For each s,
therefore, the integrand in I is log-convex in d. Pointwise log-convexity followed
by Hölder's inequality proves that I is log-convex. Since I is positive and
smooth for d>0, (log I)''>=0. Differentiating the other factors in (3.2) gives

    H''(d)>=-2-(rho²+d²)/(rho²-d²)².                 (3.3)

The penalty (rho²+d²)/(rho²-d²)² is increasing in d>=0. Put

    x=t², g(x)=(2+x)/(2-x)².

Because d=tv<=t sqrt(a), rho²=2a, and x<=1/2,

    (rho²+(tv)²)/(rho²-(tv)²)² <= g(x)/a.

Inserting (3.3) in (2.1), and dropping only the nonnegative variance, yields

    (log R_a)''
      >=1/x+2a-aL''(sqrt(a)t)-(4+g(x)/a)m.           (3.4)

In particular, by (3.1),

    (log R_a)''>=1/x+2a-(4+g(x)/a)m.                (3.5)

Here g'(x)=(6+x)/(2-x)³>0 and g(1/2)=10/9.

## 4. Integration-by-parts moment bound

Let U=sqrt(rho²-d²) and

    J(d)=integral_0^U exp(2d sqrt(rho²-y²))dy.

Differentiation, including the moving upper endpoint, gives

    H'(d)=-2d
       +2 [integral_0^U sqrt(rho²-y²)e^(2d sqrt(rho²-y²))dy]/J(d)
       -d e^(2d²)/(U J(d)).                         (4.1)

Consequently

    H'(d)<=2rho-2d.                                  (4.2)

For w=w_t from Section 2, integration by parts is legitimate at both endpoints:
v w(v) vanishes at zero and is strictly positive at v=sqrt(a). Thus

    0<sqrt(a)w(sqrt(a))
      =integral_0^sqrt(a)
        w(v)[3-2(1+x)v²+tvH'(tv)]dv
      <=N(t)[3-2(1+2x)m+2rho t E_t[v]].

Cauchy-Schwarz gives E_t[v]<=sqrt(m), so

    2(1+2x)m<3+2sqrt(2axm).                          (4.3)

The strict sign follows already from the upper boundary term. Equivalently,
sqrt(m) is below the unique positive root of

    2(1+2x)u²-2sqrt(2ax)u-3=0.

A convenient non-strict displayed bound is

    m<=[sqrt(2ax)+sqrt(2ax+6(1+2x))]²
          /[4(1+2x)²].                              (4.4)

We will use the exact quadratic relation (4.3), not a numerical evaluation of
the root.

## 5. A uniform moment lemma: m<=3a/5

This section proves the stronger estimate needed at small and intermediate a.
It does not infer it merely from unimodality.

Scale v=sqrt(a)y, 0<=y<=1, and use (3.2). Constants independent of y cancel
from the moment ratio. Tonelli's theorem represents its density as a positive
mixture over 0<=s<=1 of densities y²b_s(y), where

    b_s(y)=sqrt(2-t²y²) exp(a f_s(y)),
    f_s(y)=-(1+2t²)y²+2t G_s(y),
    G_s(y)=y sqrt(B+C y²),
    B=2(1-s²), C=t²s².                               (5.1)

### 5.1 Log-concavity of b_s

For B>0 and C>=0,

    G_s''(y)=C y(3B+2Cy²)/(B+Cy²)^(3/2),
    G_s'''(y)=3B²C/(B+Cy²)^(5/2)>=0,
    0<=G_s''(y)<=2sqrt(C).

The last inequality follows by squaring nonnegative quantities:

    4C(B+Cy²)³-C²y²(3B+2Cy²)²
      =CB²(4B+3Cy²)>=0.

For B=0, G_s(y)=sqrt(C)y² and all assertions hold directly, including at zero.
For C=0, G_s is linear and they also hold. Therefore

    f_s''<=-2(1+2t²)+4t sqrt(C)
           =-2-4t²(1-s)<=-2.

The other logarithmic factor has curvature

    (log sqrt(2-t²y²))''
      =-t²(2+t²y²)/(2-t²y²)²<=0.

Hence b_s is log-concave on [0,1].

### 5.2 The essential reflection property

For any convex function k on [0,1], its average over the centered interval
[y,1-y], 0<=y<1/2, is at most its average over [0,1]. To see this, the symmetric
sum k(1/2+r)+k(1/2-r) is nondecreasing for r>=0. Its average over [0,h] is
therefore nondecreasing in h; take h=1/2-y and h=1/2. This argument can equally
be obtained by differentiating those averages and using the chord bound for a
convex function.

Apply this fact to k=G_s', which is convex because G_s'''>=0. Its full-interval
average is G_s(1)-G_s(0)=sqrt(B+C). Thus

    [f_s(1-y)-f_s(y)]/(1-2y)
       <=-(1+2t²)+2t sqrt(B+C)
       <=-(1+2t²)+2sqrt(2)t
       =-(1-sqrt(2)t)²<=0.                           (5.2)

Here B+C=2-s²(2-t²)<=2, since t²<=1/2. The equality y=1/2 is immediate.
Because sqrt(2-t²y²) is decreasing in y, (5.2) implies

    b_s(1-y)<=b_s(y), 0<=y<=1/2.                     (5.3)

### 5.3 Superlevel intervals and layer cake

By log-concavity, a nonempty superlevel set of b_s on [0,1] is an interval with
endpoints alpha,beta. It obeys alpha+beta<=1. Indeed if beta<=1/2 this is
automatic; if beta>1/2, (5.3) places the reflected point 1-beta in the same
superlevel set, so alpha<=1-beta. Open endpoints can be replaced by their
closure without altering either integral.

For every 0<=alpha<=beta<=1 with alpha+beta<=1,

    integral_alpha^beta y^4dy
        <=(3/5) integral_alpha^beta y²dy.             (5.4)

To prove this, define p(z)=z³(1-z²). It increases on [0,sqrt(3/5)] and decreases
on [sqrt(3/5),1]. Since alpha<=1/2 and beta lies in [alpha,1-alpha], the minimum
of p over that interval is attained at an endpoint. Moreover

    p(1-alpha)-p(alpha)
      =alpha(alpha-1)(2alpha-1)(alpha²-alpha+2)>=0.

Thus p(beta)>=p(alpha), which is exactly
beta^5-alpha^5<=beta³-alpha³ and hence (5.4). Degenerate intervals give zero
on both sides.

The layer-cake representation of the positive continuous b_s, with Tonelli,
now gives

    integral_0^1 y^4 b_s(y)dy
       <=(3/5) integral_0^1 y² b_s(y)dy.

Integrating this inequality over s preserves it. Returning to v proves

    m<=3a/5.                                         (5.5)

Every endpoint and degeneracy in (5.1) has been included; in particular s=1
does not require a singular differentiation at y=0.

## 6. Positive curvature for 0<a<=10/3

By (3.5) and (5.5),

    (log R_a)''>=1/x-(2/5)a-(3/5)g(x).                (6.1)

For 0<x<1/2 the right side is strictly greater than its value at x=1/2, because
1/x is strictly decreasing and g is strictly increasing. When a<=10/3 its
endpoint lower bound is

    2-(2/5)(10/3)-(3/5)(10/9)=0.

Hence (1.1) holds throughout this entire a range. The physical interval in
(1.1) is open at t_0, so no strictness is lost at a=10/3.

## 7. Positive curvature for a>=4: an exact polynomial certificate

Set

    B_0=(1/x+2a)/(4+g(x)/a),
    K=2(1+2x)B_0-3,
    D=K²-8axB_0.                                     (7.1)

If K>0 and D>0, then

    2(1+2x)B_0-3>2sqrt(2axB_0).

In the quadratic in u=sqrt(m) from Section 4, this means sqrt(B_0) lies above
its unique positive root: the other root is negative because its constant
term is -3 and its leading coefficient is positive. Equation (4.3) therefore
forces m<B_0. Substitution in (3.5) proves strict positive curvature.

We establish K,D>0 uniformly for a>=4 and 0<x<1/2 by the bijective substitution

    a=4+b, x=z/[2(1+z)], b>=0, z>0.

Put

    T=18bz²+48bz+32b+77z²+201z+132.

The exact denominator of K is z(z+1)T. The exact denominator of D is its
square. Both are strictly positive on the stated domain. Their numerator
coefficient rows are as follows. Row j lists ascending powers of z in the
coefficient of b^j; every unlisted power has coefficient zero.

Numerator of K:

    j=0: 128, 692, 1697, 1590, 489
    j=1: 32, 304, 882, 864, 270
    j=2: 0, 32, 112, 114, 36

Numerator of D:

    j=0: 16384, 177152, 778128, 1536104, 1614641,
         1014612, 421046, 118668, 17361
    j=1: 8192, 122112, 654784, 1535536, 2052964,
         1796296, 1050368, 368328, 56988
    j=2: 1024, 27648, 196992, 560320, 909892,
         946112, 619324, 228552, 35784
    j=3: 0, 2048, 24576, 88576, 170944,
         199192, 138484, 52368, 8244
    j=4: 0, 0, 1024, 5120, 11648,
         14784, 10692, 4104, 648

All coefficients are nonnegative and the constant terms are strictly positive.
These finite identities prove K,D>0 without a numerical radius ladder. The
exact script reconstructs (7.1), verifies both denominator factorizations and
every coefficient row, and emits the full expanded polynomials separately.
The map omits x=1/2, which is not needed in the open-interval theorem.

## 8. A uniform analytic repair of 10/3<a<4

There is no missing compact parameter search.

### 8.1 The part with x<=4/9

For a<4 and x<=4/9, (6.1) is at least

    9/4-8/5-(3/5)(99/98)=43/980>0.                   (8.1)

Thus only 2/3<t<1/sqrt(2) needs an additional estimate. We may include the
endpoints in all bounds below.

### 8.2 A positive lower bound on H'

Use (4.1). The unweighted average of
q(y)=sqrt(rho²-y²) over [0,U] is at least its average over [0,rho], namely
pi rho/4, because U<=rho and q is decreasing. Exponentially tilting by
e^(2dq(y)) cannot decrease its mean. One elementary proof is the nonnegative
double integral of

    (q(y)-q(z))(e^(2dq(y))-e^(2dq(z)))

over the square [0,U]². Therefore the weighted mean in (4.1) is at least
pi rho/4.

Also q(y)>=d for 0<=y<=U, so J(d)>=U e^(2d²). The magnitude of the negative
moving-boundary term is consequently at most d/U²=d/(rho²-d²). On d<=rho/2
this is at most 2/(3rho). Equation (4.1) yields

    H'(d)>=rho(pi/2-1)-2/(3rho), 0<=d<=rho/2.         (8.2)

In the current a range, rho>18/7 because
rho²=2a>20/3>(18/7)². With pi>25/8, (8.2) gives

    H'(d)>81/56-7/27=1795/1512>0.                    (8.3)

### 8.3 A positive lower bound on h

The interval [0,rho/3] is inside [0,U], since d<=rho/2. Restricting the positive
integral defining h to it, and using
sqrt(rho²-y²)>=2sqrt(2)rho/3, gives

    h(d)>=(4rho/(3pi))
       exp(-rho²-d²+(4sqrt(2)/3)rho d).              (8.4)

At d=sqrt(a)t the exponent is

    a[-2-t²+(8/3)t].

The bracket is increasing for 2/3<=t<=1/sqrt(2), because its derivative is
8/3-2t>0, and its value at 2/3 is -2/3. Since a<4, the exponent is at least
-8/3. Using rho>18/7, pi<22/7, and e^(8/3)<15 in (8.4) gives

    h(d)>4/55.                                       (8.5)

The elementary constants here have exact certificates, not decimal estimates:

- The identity arctan(1/2)+arctan(1/3)=pi/4 follows from tangent addition, with
  both sides in (0,pi/2). Integrating the geometric expansion of
  1/(1+u²) gives the strict four-term lower bound
  arctan(r)>r-r³/3+r^5/5-r^7/7 for r>0. Applying it at r=1/2,1/3 yields
  pi>1538665/489888>25/8.
- The positive integral of y^4(1-y)^4/(1+y²) from 0 to 1 equals 22/7-pi,
  so pi<22/7.
- The exponential series through degree 6 at r=8/3, followed by a geometric
  majorant of its tail, gives

      e^(8/3)
        <=sum_(k=0)^6 (8/3)^k/k!
           +[(8/3)^7/7!]/[1-(8/3)/8]
        =3306347/229635<15.

  The first tail term is k=7 and every subsequent ratio is at most
  (8/3)/8=1/3.

### 8.4 Retaining the lens curvature closes the gap

Since ell'=-h,

    L''=-h'/ell-(h/ell)².

Here ell<=1, h'>0 by (8.3), and (8.3)-(8.5) imply

    -aL''>=a h'
       > (10/3)(4/55)(1795/1512)
       =4/15+659/31185.                              (8.6)

In contrast, the remaining terms of (3.4), after (5.5), are bounded below
throughout this compact box by

    1/x-(2/5)a-(3/5)g(x)>=2-8/5-2/3=-4/15.

Keeping the term -aL'' in (3.4) and combining with (8.6) yields the strict,
uniform bound

    (log R_a)''>659/31185>0.                          (8.7)

Together, Sections 6-8 prove (1.1) for every a>0.

## 9. Convexity, exact root count, and global classification

Let r(t)=log R_a(t) for fixed a>0. The accepted block cusp and the displayed
positive N,P formulas imply R_a(t)->+infinity as t->0+. The accepted symmetric
endpoint Hessian gives

    Phi_a'(t_0)=0, Phi_a''(t_0)<0.

Since Phi_a'=2P(1-R_a), it follows that

    R_a(t_0)=1, r(t_0)=0,
    r'(t_0)=-Phi_a''(t_0)/(2P(t_0))>0.

Thus r is negative immediately to the left of t_0 and tends to positive
infinity at zero. Continuity gives at least one zero t_m in (0,t_0).

Strict convexity permits at most two zeros on (0,t_0], including the endpoint:
if three distinct zeros existed, the middle value would be strictly below
the chord joining the outer two zeros, contradicting its being zero. Since
t_0 is one zero, t_m is the unique interior zero. This argument applies with
t_0 as an endpoint because r is continuous there and r''>0 on the open
interval.

Strict convexity also gives r<0 between t_m and t_0. There are no earlier
zeros and r tends to positive infinity at zero, so r>0 on (0,t_m). Consequently
Phi_a'=2P(1-e^r) has exactly the claimed negative-then-positive sign pattern.
Moreover, choosing any s in (t_m,t_0), convexity implies

    r'(t_m)<=[r(s)-r(t_m)]/(s-t_m)<0.

At t_m,

    Phi_a''(t_m)=-2P(t_m)r'(t_m)>0.

Hence the unique stationary point is a nondegenerate minimum, not a tangency
or a hidden higher-multiplicity stationary point.

For 0<t<=t_m, strict decrease gives Phi_a(t)<Phi_a(0). For t_m<=t<t_0,
strict increase gives Phi_a(t)<Phi_a(t_0). Every interior value is therefore
strictly below max(Phi_a(0),Phi_a(t_0)), including at the endpoint tie.
The monotone coordinate conversion c=t²/(1+t²) preserves these conclusions.

Finally apply the already accepted structural reduction and its equality
classification. No all-distinct interior normal or unequal boundary pair can
maximize. The accepted endpoint comparison then gives the three regimes
in Section 1, including both and only both endpoint types at a_*. This is a
global endpoint-only optimizer theorem, rather than merely a comparison of
the endpoint values.

## 10. Verification boundary and provenance

The new mathematical content is the logarithmic-curvature argument, both
moment bounds, the exact large-radius coefficient certificate, the uniform
compact-gap estimate, and their strict-convexity consequence. All were
reconstructed in this task from the explicitly unproved lead. The accepted
proper-complex scalar integral, endpoint Hessian, endpoint crossing, and
strict structural reduction are source-bound dependencies and are not claimed
as new contributions here.

The 85 exact controls verify differentiations and finite algebraic identities,
positive-coefficient certificates, elementary constants, coordinate conversion,
and every bound source hash. The analytic arguments above, not the controls
alone, prove the integral inequalities. No floating quadrature, numerical
stationary-point census, radius ladder, or optimization oracle is used.

The separately assigned fresh reviewer did not supply a structural lemma or
proof repair before this freeze. Exchanging frozen paths and hashes is review
coordination, not independent acceptance of one's own work. A final external
review verdict is required before this candidate is promoted to accepted
status. All inherited artifacts remain byte-identical. No external mutation,
repository update, or publication was performed by this author.
