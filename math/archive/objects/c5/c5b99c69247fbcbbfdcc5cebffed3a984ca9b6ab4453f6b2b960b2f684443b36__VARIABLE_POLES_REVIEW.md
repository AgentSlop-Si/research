# Independently certified non-affine N4 synthesis and a dyadic closure gate

Independent paired review, 9 October 2026 UTC. No uploaded or constructor
program was executed by this reviewer. The constructor's JSON isolator is
input data to a separately authored checker.

## Accepted positive statement

Let Z_N e_j=e_(j+1 mod N), R_N be bit reversal, V_N=R_N Z_N R_N^(-1),
and H_N(p,q,t)=(I-p Z_N)^(-1)+t(I-q V_N)^(-1).
There exists an exact algebraic tuple at N=4 with

F4=H4(p0,q0,t0) L H4(p1,q1,t1) M H4(p2,q2,t2),
F4[j,k]=i^(jk),
L=diag(l0,l1,l2,l3), M=diag(1,m1,m2,m3).

The tuple is uniquely specified by the rational equations and the
isolating polydisc in VARIABLE_POLES_DYADIC_CERTIFICATE.json.
All poles, weights, diagonal-mask entries, and mixer entries are nonzero;
the three mixers are pairwise noncommuting. All six Green denominators
are nonzero. Both permutation orders are active in each stage, and the
bit-reversed successor on four coordinates is non-affine in the natural
cyclic coordinate.

This is a single isolated small-size point with variable poles at each
stage. It does not settle the separate fixed-pole finite unequal-outer
chart and does not establish a uniform Fourier transform algorithm.

## Independent exact certificate

The certificate contains 16 Gaussian-dyadic center coordinates and a
16-by-16 Gaussian-dyadic preconditioner C, all with denominator 2^128.
Its coordinate-disc radius is 3402823669209384635/2^128.
The supplied preconditioner is treated as exact rational data, not as
an assumed inverse.

check_variable_pole_rectangles.py uses a separate arithmetic design:
real rectangular intervals with signed directed integer rounding at
192-bit precision. It does not use floating-point decisions, SymPy,
the constructor's ball class, or the constructor's derivative evaluator.
For each cycle distance d it directly evaluates

g_d(p)=p^d/(1-p^4),
g'_d(p)=[d p^(d-1)(1-p^4)+4p^(d+3)]/(1-p^4)^2,

with the first derivative-numerator term omitted at d=0. These
quotient-rule derivatives independently build the 16 derivative columns.

Let f be the row-major matrix entries of the claimed product minus F4.
Let S=2^192 and r be the original radius scaled to denominator S.
The checker evaluates the Jacobian on the closed real rectangle product
whose real and imaginary coordinate radii both equal r/S. This region
contains the supplied Euclidean polydisc. It proves

||C f(center)||_(real infinity) <= eta/S,
||I-C Df(z)||_(real infinity operator) <= q/S,

where the exact integer values are

eta=9145033794486455575,
q=217626011772793262676601499427942369394135953,
S=6277101735386680763835789423207666416102355444464034512896.

The bound q/S is less than 1. The exact integer inequality

eta*S + q*(r/2) < (r/2)*S

also holds. Thus T(z)=z-Cf(z) maps the half-radius real rectangle
strictly into itself and is a contraction there. Banach's theorem gives
a unique fixed point in that smaller region, which lies inside the
original complex polydisc because sqrt(2)/2<1. The contraction bound
on the full rectangle gives uniqueness throughout the original
polydisc as well.

The norm bound at the center makes C Df(center) invertible, so C is
invertible. Therefore a fixed point of T solves f=0. The same bound
makes Df invertible throughout the full rectangle. All pole denominators
are excluded from zero throughout that region. Clearing denominators
therefore gives a square polynomial system over Q(i) with nonsingular
Jacobian at its isolated zero, so its coordinates are algebraic.

The checker independently excludes zero from every pole, coupling,
mask entry, and mixer entry on the full rectangle. It also computes
interval commutators and records certified nonzero entries for each of
the three stage pairs. Once the equality holds, invertibility of every
stage follows from invertibility of F4 and the masks.

This proves all 16 complex matrix equations. Fourier normalization and
Weyl identities follow from that exact matrix equality. Complex
conjugation gives the opposite phase; scaling one mask by 1/2 gives
unitary N4 normalization. No sampled-vector claim substitutes for these
entrywise equations.

## Independently checked all-size block identity

For N=2m, m>=2, write G_p(Z)=(I-pZ)^(-1), assume p^(2m)!=1 and
q^(2m)!=1, and define

E=(I-q^2 V_m)^(-1),
B_ij=p^(m+i-j)/(1-p^(2m)), 0<=i,j<m.

The cyclic geometric-series entries and V_(2m)=[[0,V_m],[I,0]] give

G_p(Z_(2m))=[[G_p(Z_m)-B,B],[B,G_p(Z_m)-B]],
G_q(V_(2m))=[[E,q V_m E],[q E,E]].

For the natural-cycle identity, the diagonal-block equality follows
separately when i>=j and i<j by reducing the geometric denominators.
Both crossblocks have exponent m+i-j, which is positive. For the
bit-reversal identity, multiplication by [[I,-qV_m],[-qI,I]] gives
the identity matrix directly. Thus these are symbolic identities for
every allowed size and parameter, not extrapolations from finite tests.

Consequently the principal half of H_(2m)(p,q,t) is

H_m(p,q^2,t)-B.

When p!=0, B has rank one. Its row sums simplify exactly to

(B 1)_i=p^(i+1)/[(1-p)(1+p^m)].

The adjacent row-sum difference of the principal H block is therefore

row_sum(i+1)-row_sum(i)=p^(i+1)/(1+p^m), 0<=i<m-1.

This is nonzero under p!=0 and p^(2m)!=1. The principal half has
nonconstant row sums. Every valid scalar resolvent of a permutation
matrix has constant row sums, and so does every constant-weight sum of
such resolvents. Therefore this principal half cannot equal any such
smaller sum, including a scalar multiple of a retuned H_m.

## Scope of the obstruction and cost

The obstruction excludes only naive stagewise principal-half closure
through retuning poles, scalar couplings, or stage scalars. It permits
diagonal gauges, explicit boundary states, other partitions, and a
recursion of the entire masked product. It is not an all-length
impossibility theorem.

For supplied coefficients, the previously stated application ledger
remains 17N-6 scalar multiplications and 15N-12 additions, plus six
pole-dependent boundary reciprocals, index/data operations, storage,
and coefficient generation. The N4 isolator gives no growing-size rule
for those coefficients and no bounded-degree field or bit-cost claim.
No practical or asymptotic FFT improvement is certified here.

## Reproduction

The independent checker needs only Python's standard library and the
JSON certificate. VARIABLE_POLES_INDEPENDENT_REVIEW.json records every
integer bound, the input hash, and noncommutation witnesses. A portable
replay uses a different working directory and reproduces that result
byte-for-byte. Both input and checker are included in the sealed
checkpoint; numerical proposal generators are unnecessary for replay.
