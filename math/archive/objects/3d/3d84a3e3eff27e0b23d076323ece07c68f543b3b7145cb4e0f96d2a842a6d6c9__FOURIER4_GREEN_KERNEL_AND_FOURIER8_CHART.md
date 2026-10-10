# An exact Fourier-4 paired-Green kernel and a bounded Fourier-8 chart obstruction

Status: additive finite-kernel result. This document neither supplies a two-layer Fourier-8 factorization nor excludes one outside its expressly stated commuting chart. Existing seals remain unchanged.

## 1. Conventions and field requirements

For the cyclic shift S_n e_j=e_(j+1 mod n), a constant-mask Green operator is (I-r S_n)^(-1). Its guard is 1-r^n != 0, and every edge mask is genuinely nonzero if r != 0. A paired-Green layer is a sum of two such Green terms with nonsingular diagonal or monomial endpoints. All Fourier transforms here have positive exponent and no normalization.

The positive theorem below holds over any field containing a primitive eighth root chi, with characteristic different from 2, in which z^2+(chi+chi^(-1))z+chi^2 has two distinct roots. Complex numbers supply a characteristic-zero example. The distinct-root condition is an explicit additional guard; primitive roots alone do not imply it in every positive characteristic. Coefficient recovery must supply these constants or pay for the field extension and quadratic-root computation. No free root extraction is assumed.

## 2. One paired-Green layer equals F_4

Put i=chi^2, h=chi+chi^(-1), and a=chi^(-1). Thus i^2=-1, h^2=2, and h a=1-i. Let r,s be the distinct roots of

    z^2+h z+i=0,

and define

    A=(a-s)/(r-s),       B=(r-a)/(r-s),
    E=diag(chi^(j^2): 0<=j<4).

Then the following is an exact allowed layer:

    F_4 = A(1-r^4) E (I-r S_4)^(-1) E
        + B(1-s^4) E (I-s S_4)^(-1) E.                 (1)

All eight masks in the two Green terms are nonzero. Both endpoint diagonals are nonsingular. The two Green guards are nonzero, with their product exactly

    (1-r^4)(1-s^4)=8i.                                (2)

Proof. The chirp sequence c_t=chi^(-t^2), 0<=t<4, is [1,a,-1,a]. It satisfies c_(t+2)=-h c_(t+1)-i c_t for t=0,1. Consequently c_t=A r^t+B s^t for all four indices. Since S_4^4=I,

    (1-r^4)(I-r S_4)^(-1)=sum_(t=0)^3 r^t S_4^t.

Hence the middle circulant in (1) has entry chi^(-(u-v)^2). The sequence is 4-periodic, so E C E has entry chi^(u^2+v^2-(u-v)^2)=i^(uv), exactly F_4.

For the guards, rs=i != 0 and r+s=-h. One obtains r^4+s^4=2-8i and r^4 s^4=1, yielding (2). Thus neither denominator vanishes when characteristic is not 2. Also a is not either root because a^2+h a+i=1-i != 0, so A and B are nonzero. The discriminant h^2-4i=2-4i must be nonzero, as stated in the field hypotheses. E is nonsingular.

This is a finite exact algebraic control with O(4) cyclic-recurrence application after its constant-size setup. It does not establish a growing-size complexity improvement.

## 3. A precise commuting chart that cannot produce F_8

Let chi now be a primitive sixteenth root, omega=chi^2, and c_t=chi^(-t^2), 0<=t<8. Remove the fixed outer chirp diagonals E=diag(chi^(j^2)) from F_8, leaving the circulant C(S_8), where

    C(z)=sum_(t=0)^7 c_t z^t modulo z^8-1.

Restrict each of two layers to the following exact grammar:

    H_l(z)=alpha_l/(1-r_l z)+beta_l/(1-s_l z),   l=1,2,

with scalar endpoints, the same cycle S_8 for every term, and each denominator individually nonsingular modulo z^8-1. The chart allows repeated or zero poles; allowing them does not rescue it. It does not allow varying masks up to independent diagonal endpoints, different Hamiltonian orders, shifts in individual numerators, or interstage diagonal twists.

Each layer has numerator degree at most 1 and denominator degree at most 2. Thus C=H_2 H_1 would imply

    C(z) D(z)=A(z) modulo z^8-1,
    deg D<=4, D(0)=1, deg A<=2.

The five coefficients at powers k=3,4,5,6,7 give the homogeneous square system

    sum_(j=0)^4 c_((k-j) mod 8) d_j=0.

Its matrix is invertible. Indeed c is 8-periodic, and its (k,j) entry factors as

    chi^(-k^2) chi^(-j^2) omega^(k j).

After removing nonzero row and column factors and omega^(3j), it is the five-by-five Vandermonde matrix on the distinct nodes 1,omega,omega^2,omega^3,omega^4. Its determinant is a product of nonzero node differences. Thus D=0, contradicting D(0)=1.

This proof works in every field with the stated primitive root and characteristic not dividing 16. It proves only this bounded commuting, unshifted, scalar-resolvent chart empty. It gives no general two-paired-Green impossibility.

## 4. Costs and lifting caveat

Formula (1) is a genuine Hamiltonian length-4 construction. Direct sums of its cyclic Green factors have disjoint 4-cycles, not a Hamiltonian cycle on all batch coordinates. Therefore the formula cannot be promoted for free to an allowed global batched layer. A lift needs an explicit Hamiltonian stitching or cancellation construction, with its masks, endpoints, guards, and extra terms charged. The same caveat applies to a future local F_8 kernel.

The existing nonzero-mask butterfly construction uses acyclic matching masks and can be stitched with zero connecting edges. That argument does not apply to the full nonzero cyclic masks in (1).

## 5. Verification and provenance

The accompanying freshly authored standard-library verifier checks (1), every mask/endpoint/guard, and the five-by-five chart rank over several splitting prime fields. It also records fields rejected for a missing split or repeated root. These finite controls supplement the proofs; no uploaded executable was run.

The chirp identity and exponential-recurrence interpolation are standard mechanisms. The primary paper by Beylkin and Monzon, "On approximation of functions by exponential sums," Applied and Computational Harmonic Analysis 19 (2005), 17-48, explicitly discusses exact exponential interpolation as Prony's method: https://www.colorado.edu/amath/sites/default/files/attached-files/bey-mon-2005.pdf . Bluestein's original paper is "A linear filtering approach to the computation of discrete Fourier transform," DOI https://doi.org/10.1109/TAU.1970.1162132 ; the official IEEE landing page was reached but blocked full-text access. No novelty claim is made for either mechanism or for the present finite identity.
