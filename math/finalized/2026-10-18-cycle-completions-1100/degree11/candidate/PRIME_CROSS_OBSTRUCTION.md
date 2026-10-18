# N13: unrestricted-support obstruction for every prime-field cross pair

18 October 2026 UTC. New bounded result for M-MAGNETIC-SPAN / NEW-17 /
Q35 / NEXT-MAGNETIC-SIGNED. Author theorem; independent final review pending.

## Result

Let K=F_(53^d), gcd(d,210)=1, N=13 and q=16. Retain the original signed-
resolvent bank grammar, with exactly one nonzero effective node in each
cross orientation. Impose only that those two independently chosen cross
nodes y,z belong to F53*. Allow **arbitrary K-valued same-sign supports**,
arbitrary legal beta values, and arbitrary K-valued raw weights. Neither
same-sign support nor its annihilator is assumed Frobenius-stable.

In this family, the exact physical-bank minimum is **18**. In particular,
there is no 16-bank or 17-bank witness over F_(53^11) in this family, even
with genuinely extension-valued annihilators admitted at the outset.

The new step proves that a seven-node side would be forced to have its
annihilator in F53[t]. It uses the b=3 compatibility equation and a new
exhaustive calculation on the **2,704 ordered cross pairs**, not a repeated
enumeration of prime-field support polynomials. The already accepted
stable-support theorem then supplies the contradiction.

Consequently any unrestricted 16- or 17-bank witness at these degrees
must have **at least one cross node outside F53**, in addition to the
previously accepted nonstable-support requirement. This is necessary,
not sufficient. For d=11 the accompanying REPORT.md now establishes the unrestricted minimum 16; degrees divisible by 11 inherit that attainment. For other unresolved degrees the inherited interval remains 16..18.

d=11 was the smallest unsettled positive extension degree at this gate’s entry: d=1 is already
exactly 18, while each d=2,...,10 has a divisor in {2,3,5,7}, whose attaining
cases were accepted earlier. The proof also covers every other d coprime
to 210. No general nonexistence conclusion is drawn for extension-valued
cross nodes.

## 1. Original model and accepted dependencies

All indices are modulo 13, S e_t=e_(t+1), T e_t=16^t e_t and
F[k,t]=16^(-kt). One physical bank is

    (1/13) sum_(j=0)^12 w_j
      (I-alpha S^epsilon-beta 16^(epsilon delta j) T^delta)^(-1),
    epsilon,delta in {+1,-1}, Delta=1-alpha^13-beta^13 != 0.

Repeated banks at an orientation/node are merged by their full normalized
amplitude vectors; an effective node has a nonzero merged vector. The
same-sign support counts only nonzero alpha nodes. Zero-alpha, repeated or
ineffective physical banks remain allowed and remain physically charged.

The accepted field-uniform lower theorem gives at least seven distinct
nonzero effective same-sign nodes on each side, and a total count at least
|X_++|+|X_--|+2. The accepted arbitrary-beta expansion has the normalized
target f(a,b)=16^(10(a+b)^2) and bank contribution

    G_(epsilon,delta)(a,b) alpha^[epsilon a]_13 A_b,

where, for r=[epsilon a]_13, ell=[delta b]_13,
omega=16^(epsilon delta),

    G = product_(i=1)^ell (1-omega^(r+i))/(1-omega^i)
        if r+ell<13, and 0 otherwise.

All displayed denominators are nonzero prime-field scalars. The amplitude
definition has no division by beta. Thus arbitrary legal beta, repeated
nodes and cancellation are covered by the same necessary equations.

The accepted stable-support result says that for gcd(d,210)=1, no original
representation can have a seven-node same-sign support with annihilator
in F53[t], even if the other support, cross nodes and weights are initially
arbitrary in K. Its proof and base-field census are **not rerun here**.
The accepted 18-bank F53 witness supplies the upper bound below.

The immutable source URLs and exact Git blob/content hashes are retained
in SOURCE_PINS.json; complete source bodies are in sources/. Only freshly
authored programs in this packet were executed.

## 2. All seven-node annihilators at a prime-field adjacent cross node

Suppose X_++ has seven nonzero distinct nodes. Write its monic annihilator

    H(t)=sum_(j=0)^7 h_j t^j, h_7=1, h_0 != 0.

At this point h_j may be anywhere in K. The adjacent (-,+) cross node is y.
The forced moments, obtained from the isolated cross row, are

    u_y(a,b) = [f(a,b)-y^(13-a-b)G_-+(a,b)/G_-+(13-b,b)] / G_++(a,b).

For (b,a)=(1,1),(1,2),(1,3),(1,4),(2,2),(2,3), the annihilator satisfies

    sum_(j=0)^7 h_j u_y(a+j,b)=0.

When y is in F53*, all coefficients are in F53. The accepted rank result
and the fresh full finite computation agree: for each of the 52 y values,
the first six coefficient columns are invertible. The entire solution set
over **K**, not merely over F53, is therefore

    H_lambda(t)=sum_(j=0)^7 (c_j(y)+lambda n_j(y)) t^j,
    lambda in K,
    c_6=0, c_7=1, n_6=1, n_7=0,

with c_j,n_j in F53. The census stores all 52 complete affine lines. This
parameterization permits every extension-valued annihilator compatible
with the forced b=1,2 windows. It does not assume stability or splitting.

## 3. A quadratic obstruction from b=3

Let z be the independently free (+,-) cross node. At b=3 and a=10, only
the (-,+) orientation contributes, so its amplitude is fixed. At a=1,...,9,
the (--) orientation vanishes, G_++ is nonzero, and the (+,-) orientation
is nonzero only at a=1,2. These facts are checked directly in both fresh
programs. Thus the required (++) moments obey

    s_a = U_a - C V_a, a=1,...,9,
    U_a=u_y(a,3),
    V_a=z^a G_+-(a,3)/G_++(a,3),

for the actual (+,-) normalized amplitude C in K. In particular this
argument does not depend on the size, parameters or amplitudes of X_--.
Zero-alpha (++) nodes also vanish because a>0.

The annihilator recurrences starting at a=1 and a=2 yield

    E_s = C F_s, s=1,2,
    E_s=sum_(j=0)^7 h_j U_(s+j),
    F_s=sum_(j=0)^7 h_j V_(s+j).

Eliminating C gives the necessary equation

    Q_(y,z)(lambda) = E_1 F_2 - E_2 F_1 = 0.

Each E_s and F_s is affine in lambda. Hence Q has degree at most two.
For y,z in F53*, its coefficients lie in F53. This elimination multiplies
and subtracts; it does not divide by E_s, F_s, h_0, or any parameter
polynomial. In particular no exceptional zero-amplitude case is discarded.
Indeed for an actual seven-nonzero-node support F_2=h_0 V_2 is nonzero,
but even that fact is unnecessary for the implication Q=0.

## 4. Exact finite coefficient certificate

The declared cross-node family is all 52*52=2,704 ordered pairs (y,z).
For each pair the freshly reconstructed affine line is substituted in
the exact determinant above. Coefficients of lambda^0,lambda^1,lambda^2
are stored in CROSS_GATE_CENSUS.json. The exhaustive degree counts are

    degree 2: 2,655 pairs
    degree 1:    47 pairs
    degree 0:     2 pairs
    zero polynomial: 0 pairs.

The constant cases are (y,z)=(25,28), Q=27 and (46,4), Q=30. They are
impossible over every field and are retained in the certificate.

The discovery calculation uses product-form Gaussian coefficients and
two six-column linear solves. The separate cold checker uses the additive
Gaussian Pascal recurrence and RREF of the complete six-by-seven system.
It reconstructs each quadratic by three evaluations with the a priori
degree bound, then verifies all 53 scalar parameter values at all 2,704
pairs: 143,312 exact determinant checks. It also checks all 676 reflection
identities and the exact b=3 row vanishings. No discovery or historical
program is imported by the cold checker. Both methods find zero zero-
polynomial pairs. This is exact finite arithmetic, not random sampling.

Run:

    python explore_cross_gate.py
    python independent_cross_check.py

The second checker is an independently implemented arithmetic control by
the same author; it is not labeled an independent reviewer acceptance.
Final independent review remains required.

## 5. Descent, physical count, and the exact restricted minimum

For any actual seven-node side, Q_(y,z)(lambda)=0. A nonzero constant Q is
impossible. Otherwise lambda is a root of a nonzero degree-at-most-two
polynomial over F53. Its prime-Frobenius orbit length e divides d and is
at most two. Since gcd(d,210)=1 implies d odd, e=1. Therefore lambda is in
F53, and the complete affine formula puts every h_j in F53.

An annihilator with F53 coefficients and all seven roots in K makes the
support Frobenius-stable. The accepted stable-support exclusion now gives
a contradiction. Reflection simultaneously negates a,b,epsilon,delta and
interchanges y,z, so the same reasoning excludes a seven-node (--) side.
Neither support was assumed stable before this argument.

If a representation in the declared cross family used at most 17 physical
banks, the inherited count inequality and seven-per-side lower bounds
would force at least one same-sign support to have exactly seven nodes.
The preceding contradiction therefore proves the lower bound 18. It also
covers 17-bank arrangements with one seven-node and one eight-node side,
or any additional repeated, zero-alpha or ineffective physical bank.

For attainment, the accepted original 18-bank F53 witness has allocation
(8,1,1,8), y=z=1, beta=1 and both same-sign supports

    {1,2,6,7,12,21,22,26}.

Its raw weights, guards and complete literal matrix identity were accepted
in the pinned predecessor review. Scalar extension F53 -> K preserves
that identity and nonzero guards. This packet does not claim a new replay
of its raw inverses. Hence the declared-family minimum equals 18.

## 6. Exact stopping boundary

The new finite-family gate is complete subject to final review. Stop
16/17-bank searches at d coprime to 210 that retain **both** cross nodes
in F53, even when they allow arbitrary extension-valued annihilators.

The original unrestricted classification remains open beyond the accepted attaining degrees and the accompanying new d=11 result. A possible witness
may have one or both cross nodes outside F53. The proof does not require
both cross nodes to be nonbase, and it does not forbid any extension-valued
cross pair. It does not resolve nonsymmetric extension-valued pairs,
other cross allocations, other lengths/parameters, historical priority,
or paid evaluation costs. No FFT runtime claim follows.

The separate extension-valued exploratory search, if retained with this
packet, is explicitly outside this proof and cannot justify a broader
nonexistence assertion. Local work only; no external write, commit or
research-register change was performed.
