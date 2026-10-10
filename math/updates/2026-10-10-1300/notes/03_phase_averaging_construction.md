# Finite phase averaging for unitary cycle Green matrices

10 October 2026. Independently accepted phase-averaging addition.
This note is separate from the acceptance of the submitted all-length exclusion.
It supplies exact boundary witnesses and a construction outside the real-collinear
coefficient restriction. No optimal term count, fast algorithm, or historical
novelty is asserted.

## Conventions and finite orbit

Indices are 0,...,N-1, with N>=2. A weighted Hamiltonian cycle W maps
e_b to w_b e_(b+1 mod N), with |w_b|=1 and H=product_b w_b !=1.
Set G=(I-W)^(-1). Every entry of G is nonzero, and every diagonal entry
is d=1/(1-H). Indeed G=(I+W+...+W^(N-1))/(1-H), and for each
ordered coordinate pair exactly one of these powers contributes a unit phase.

Let zeta=exp(2*pi*i/3), let
T={(0,t_1,...,t_(N-1)): t_j in {0,1,2}}, and Q=3^(N-1).
For t in T put D_t=diag(zeta^t_0,...,zeta^t_(N-1)),
W_t=D_t W D_t^*, and G_t=D_t G D_t^*.

Every W_t remains one Hamiltonian cycle with unit-modulus edge weights,
the same H, and no eigenvalue 1. Thus G_t is literally (I-W_t)^(-1).
No singular inverse or formal limiting operation is used.

## Character projection and complex universality

For a!=b define chi_ab(t)=zeta^(t_a-t_b).
The N(N-1) characters chi_ab are pairwise distinct and nontrivial:
identifying t_0=0, their exponent vectors are e_a-e_b with e_0=0 in
(Z/3Z)^(N-1). A vector with one nonzero coordinate identifies a pair
involving 0; a vector with two nonzero coordinates has a unique +1 and
a unique -1 coordinate. Since +1 != -1 modulo 3, both endpoints and
their order are determined.

Character orthogonality therefore gives, entry by entry,

(1/Q) sum_t G_t = d I,
(1/Q) sum_t conjugate(chi_ab(t)) G_t = G_ab E_ab.

Let X be any complex N-by-N matrix with common diagonal x. Define

alpha_t = (1/Q) [ x/d +
             sum_(a!=b) (X_ab/G_ab) zeta^(-(t_a-t_b)) ].

Then the exact finite identity is

X = sum_(t in T) alpha_t (I-W_t)^(-1).

Thus the complex linear span of even this single fixed-holonomy orbit
is precisely the vector space of all constant-diagonal matrices:
containment follows from the shared diagonal d; the displayed formula
proves the reverse containment.

For omega=exp(2*pi*i/N), the positive-exponent Fourier matrix has
F_N[a,b]=omega^(ab). The matrix

X=F_N diag(omega^(-b^2))_(b=0)^(N-1)

has diagonal 1, so it admits the displayed representation. All external
diagonal factors are invertible. In particular, allowing unrestricted
complex coefficients permits monomial Fourier equivalence for every N.
For N>=4, the submitted exclusion itself ensures that the nonzero
coefficients in any such representation cannot all lie in one complex line.

This construction uses at most 3^(N-1) displayed terms. It makes no
claim about the smallest number of terms or the cost of computing or
applying a Fourier transform.

## An explicit legal N4 control

Use W e_b=e_(b+1) for b<3 and W e_3=-e_0. Then H=-1,
d=1/2, and

G_ab = s_ab/2, where s_ab=1 for a>=b and s_ab=-1 for a<b.

Use T={(0,t_1,t_2,t_3): t_j in {0,1,2}}, Q=27, omega=i,
and zeta=exp(2*pi*i/3). The 27 explicit coefficients are

alpha_t=(2/27) [1+
    sum_(a!=b) s_ab i^(ab-b^2) zeta^(-(t_a-t_b))].

With W_t=D_t W D_t^*, their sum is
F_4 diag(1,-i,1,-i). This is an exact cyclotomic identity over Q(zeta_12),
where i=zeta_12^3 and zeta=zeta_12^4. All W_t have holonomy -1.

## N2 is an actual Green exception

Let W=[[0,-1],[1,0]]. It is unitary, has H=-1, and

(I-W)^(-1)=(1/2)[[1,-1],[1,1]]
         =(1/2) F_2 diag(1,-1).

A single positive real coefficient therefore suffices at N=2.

## N3 is an actual real-linear Green exception

Write omega=exp(2*pi*i/3), H=omega^2, and d=1/(1-omega^2)=(1-omega)/3.
Let W e_0=e_1, W e_1=e_2, and W e_2=omega^2 e_0. Then

G=d [[1,omega^2,omega^2],
     [1,1,omega^2],
     [1,1,1]].

The target

X=d F_3 diag(1,omega^2,omega^2)
 =d [[1,omega^2,omega^2],
     [1,1,omega],
     [1,omega,1]]

has common diagonal d and skew-Hermitian off-diagonal entries.
Take D_(u,v)=diag(1,omega^u,omega^v) for u,v in {0,1,2}.
Set W_(u,v)=D_(u,v) W D_(u,v)^*. In increasing u row order and
increasing v column order, choose the nine REAL coefficients

(alpha_(u,v))=(1/9) [[4,4,1],
                   [1,-2,1],
                   [4,-2,-2]].

Then

X=sum_(u,v) alpha_(u,v) (I-W_(u,v))^(-1).

For completeness the coefficient formula is

9 alpha_(u,v)=1 + omega^u+omega^(-u) + omega^v+omega^(-v)
                  + omega^(2-u+v)+omega^(-2+u-v).

Its values are exactly the displayed integers. It follows either by the
character-projection formula (the off-diagonal ratios X_ab/G_ab are
1 except r_12=omega^2 and r_21=omega), or by direct entrywise summation.
Their sum is 1. All nine cycle matrices have holonomy omega^2!=1.

Consequently N=2 and N=3 are sharp exceptions for the actual real-linear
Green representation model, not merely for a necessary cross-ratio lemma.
N=1 is also trivially realizable if a one-vertex weighted loop is allowed.

## Attribution boundary

These constructions are reviewer-derived during the present audit and
are not claims made in the uploaded source theorem. The source's proof
does not depend on them. Their independent proof and exact controls are retained separately here; see
PROOF_STATUS.json and notes/05_phase_averaging_proof.md.
