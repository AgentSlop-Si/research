# Fourteen original banks over F23²: a bounded extension gate

14 October 2026. **Candidate exact result, pending independent review.**

## Result

The declared factor gate is complete, and its first eligible quadratic-field
support gives a full original-grammar fourteen-bank witness over

    K = F23[z]/(z²+1).

The new witness has orientation allocation (6,1,1,6). Both same-sign groups
use the six nodes

    {5, 6, 8+3z, 4+8z, 4+15z, 8+20z},

both cross-sign groups use the single node 4, and every beta is 1. Every
original bank and sector vector is nonzero. All 154 literal resolvent
inverses pass both product identities, and the original weighted sum equals
every one of the 121 entries of F[k,t]=13^(-kt).

The accepted extension lower-bound proof already gives b4(F23²)>=14.
Combining that dependency with this freshly checked witness gives the
candidate exact statement

    b4(F23²) = 14.

The same witness embeds into every extension containing F23². Consequently,
using the same accepted lower bound, the finite-extension corollary is

    b4(F23^d) = 14  when 2 divides d and 5 does not divide d.

The known b4(F23^d)=12 when 5 divides d remains unchanged. The accepted
base-field result is b4(F23)=16. Thus this supplies an intermediate field in
the precisely pinned dictionary. It does not classify the odd extension
degrees not divisible by five, establish an unpinned or unrestricted
minimum, or make any historical novelty or arithmetic-speed claim.

## 1. Frozen grammar and provenance

All fields extend F23. Fix N=11, q=13 and literal matrices

    S e_t = e_(t+1 mod 11), T e_t = 13^t e_t,
    F[k,t] = 13^(-kt), 0 <= k,t <= 10.

Each counted original bank is

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1),

where epsilon,delta are independently ±1 and

    Delta = 1-alpha^11-beta^11 != 0.

The minimization defining b4 permits all legal beta, including zero, and
requires exactly one effective alpha node in each cross-sign orientation,
both pinned to 4. Grouping equal-alpha sector vectors is only necessity
bookkeeping; the count is actual original summands. No derivative atom,
new generator, pre/post map, transformed target, singular limit, infinite
node, or trace-bank primitive is used.

The accepted pinned base-field obstruction and attainment reviews were read
as inert text. Their exact copied review hashes are respectively

- a2d110738cbfb31d51f6a20ad1fd7343e7932149088f11cee18a108c7bf2afc2
- f3980c0256783e69d20b73f9d8968716ea636aeb54214f03fab3f486ea49c1d5

The direct accepted extension-field lower-bound review is copied as
sources/EXTENSION_LOWER_BOUND_PROOF_REVIEW.md, SHA-256
3031f45d467e0cd0e7860de9fc59beb49758033ea0e1765e084eb19c2f97ee19.
Its reviewed fusion-source hash is
404377f23eb474dca692575b6e531d866b32ac796d9fb0b69426468a4b157231,
which exactly matches the included source report. Its lower-bound argument
is the rank-five quintic obstruction and reflection, with irreducible
quintic t^5+8t^4+t^3+18t^2+4t+6. Those accepted proof dependencies are kept
separate from the new witness computation.

Only newly authored standard-library fresh_gate.py performs scientific
calculations in this packet. No historical or supplied scientific program
was executed, imported, or compiled. No external service was written.
Source hashes are checked before and after each run.

## 2. Reconstructed moments and the complete base-coefficient family

For U=S^epsilon, V=T^delta, omega=13^(epsilon delta), VU=omega UV.
The fresh checker reconstructs the ordered coefficients from

    D(r,ell)=omega^ell D(r-1,ell)+D(r,ell-1), D(0,0)=1.

It checks all degree-eleven mixed terms vanish. Thus X_j^11 is the scalar
alpha^11+beta^11 and the finite geometric inverse applies when Delta != 0.
For r=[epsilon a]_11 and ell=[delta b]_11, let G(a,b)=D(r,ell) when
r+ell<=10, and zero otherwise. Each bank's Weyl coefficient is
alpha^r G(a,b) H_b, with

    H_b = beta^ell/(11 Delta) sum_j w_j 13^(epsilon delta j ell).

Direct extraction from all 121 literal target entries gives

    c_F(a,b)=18*13^(3(a+b)^2).

The pinned cross node 4 forces normalized cross amplitudes 22 and 20 in
sectors b=1 and b=2. Fresh reconstruction gives the shared moments

    b=1, a=1,...,9: 19,4,20,14,20,3,14,16,8;
    b=2, a=2,...,8: 21,15,14,11,13,22,19.

Their three and one length-seven windows form a rank-four matrix. Fresh
row reduction gives the full monic degree-six family with base coefficients:

    h_(u,v)(t) = t^6+v t^5+u t^4
      +(11-4u-13v)t^3+(2-16u-15v)t^2
      +(11-10u-8v)t+(17-7u-7v),

for every (u,v) in F23². The 529 reconstructed polynomials agree exactly
with the accepted review's inert sextic records.

This family is exhaustive only when the annihilator coefficients lie in
F23. A support in an extension need not have base-field annihilator
coefficients. Hence the census is neither a full extension-field search nor
an obstruction to every extension-valued six-node support.

## 3. Exact factor census

Every sextic is divided by independently generated monic linear,
irreducible quadratic and irreducible cubic polynomials as necessary. Each
remaining factor is separately verified irreducible by Frobenius powers
and polynomial gcds. Products of all factors are checked against the
original polynomial. A derivative gcd checks separability, independently
of the repeated-factor list. Constant term checks exclude a zero root.
There are 1,304 irreducible-factor checks over all 529 sextics.

The full degree-pattern counts, retaining multiplicities, are:

| Factor degrees | All sextics | Six distinct nonzero roots in a splitting field |
|---|---:|---:|
| 1,1,1,1,1,1 | 2 | 0 |
| 1,1,1,1,2 | 10 | 5 |
| 1,1,1,3 | 29 | 21 |
| 1,1,2,2 | 31 | 28 |
| 1,1,4 | 74 | 57 |
| 1,2,3 | 75 | 72 |
| 1,5 | 127 | 122 |
| 2,2,2 | 11 | 11 |
| 2,4 | 63 | 63 |
| 3,3 | 35 | 35 |
| 6 | 72 | 72 |
| Total | 529 | 486 |

The two completely linear cases have repeated roots and remain ineligible
over every extension. Of the 43 ineligible polynomials, 21 are squarefree
with a zero root, 20 have repeated roots without zero, and 2 have both faults.

For a squarefree base-field polynomial, the least extension degree in which
it splits is the least common multiple of its irreducible factor degrees.
The numbers of eligible polynomials by that minimum splitting degree are

    degree 2: 44; degree 3: 56; degree 4: 120;
    degree 5: 122; degree 6: 144.

In particular there are 44 eligible supports over F23² and 56 over F23³.
These counts establish support eligibility only. Full bank sufficiency is
verified separately for the one selected quadratic-field witness below.
No F23³ witness was searched after the quadratic witness met the declared
stopping condition.

## 4. Explicit field and support

The lexicographically first quadratic-eligible pair is (u,v)=(0,11):

    h(t)=t^6+11t^5+6t^3+21t^2+15t+9
        =(t-5)(t-6)(t²+7t+4)(t²+15t+11).

The field modulus z²+1 is irreducible over F23; the fresh code verifies its
irreducibility and enumerates every field element when finding the six
roots. Its roots are precisely the six displayed in the result. The
quadratic pairs are conjugate because z^23=-z.

The integer encoding used in the JSON files is exact and unambiguous:

    integer a+23b encodes the field element a+bz, 0<=a,b<23.

The six roots in that encoding are [5,6,77,188,349,468]. The standalone
RAW_WITNESS.json provides the field, orientations, alpha, beta, Delta, and
all eleven raw weights for each of the fourteen actual banks. Its SHA-256 is
5afef05b733e2838eed4b1a42ccb50ebaac3253a4bfa60b0b1aed995c26b7dc8.
WITNESS_TABLE.md prints the same raw bank data as coefficient pairs.

## 5. Full sector solve and literal reconstruction

For each b=0,...,10, solve the complete eleven coefficient equations in
fourteen sector amplitudes H_(i,b):

    sum_i alpha_i^[epsilon_i a]_11 G_i(a,b) H_(i,b) = c_F(a,b)
    for all a=0,...,10.

This is the full original four-orientation compatibility system, not a
moment-only acceptance. Deterministic exact row reduction chooses free
variables zero. All eleven systems are compatible, with ranks

    11,8,10,11,11,11,11,11,11,10,8.

Because beta=1, Delta_i=-alpha_i^11 is nonzero for every selected node.
The inverse finite character transform recovers the raw phase weights:

    w_(i,j) = Delta_i sum_(b=0)^10 H_(i,b) 13^(-epsilon_i j b).

The checker recovers H again from those weights with the exact original
factor 1/(11 Delta). For every bank and every phase, it then builds the
literal eleven-by-eleven branch matrix from its entries and independently
inverts it by Gauss-Jordan elimination. It does not use the geometric
series to manufacture those inverses.

All 154 branch inverses multiply their literal matrices to I on both sides,
giving 308 matrix-product checks. The matrices are weighted using the raw
weights and the original 1/11 factor. Each of the fourteen resulting bank
matrices is nonzero. Every one of 1,694 bank Weyl coefficients, extracted
from those literal matrices, equals its separately computed coefficient
formula. Every bank's sector vector is nonzero. There is one actual bank
per orientation/alpha pair, so all fourteen listed nodes are effective.

Finally all 121 entries of the aggregate equal the freshly generated,
unmodified Fourier target, with zero mismatches. The literal branch
matrices/inverses, bank matrices, full sector row reductions, raw parameters
and aggregate are retained as exact machine-readable evidence.

## 6. Controls, reproduction, and conclusion boundary

All 171 mutation controls detect their intended defect:

- Each of the 154 individual raw weights is increased by one, separately;
  its exact linear contribution changes the aggregate.
- Deleting each of the fourteen original banks changes the aggregate.
- Corrupting one inverse entry fails both product identities.
- Omitting the original 1/11 normalization fails the target check.
- Alpha=0 with beta=1 is detected as illegal because Delta=0.

A cold replay reproduces every deterministic scientific output byte for
byte; timing files are excluded from that comparison. REPLAY_VERIFICATION.json
records lengths and hashes. Run either command with Python 3:

    python fresh_gate.py --out replay

The declared scope was all 529 base-coefficient sextics plus one explicit
full witness. It is finished. This packet does not claim that every one of
the 44 eligible quadratic supports or 56 eligible cubic supports satisfies
the full bank equations. It does not reopen or reinterpret base-field
attainment: the accepted value there remains sixteen.

The new upper bound is supported by literal arithmetic. The exact minimum
and even-degree corollary additionally depend on the separately accepted
pinned extension lower-bound proof, which applies to every legal beta and
is not inferred from the factor census. This is a fixed-size mathematical
representation count. No scalar operation savings, FFT improvement,
characteristic-zero lift, unrestricted optimum, or novelty follows.
