# Independent review: sparse q-kernel grading

9 October 2026. Reviewed `README.md`, `grading.py`, the imported sparse-C
preparation, and `run_audit.py`. The algebra, coordinate formulas, and displayed
operation counts are consistent. No implementation changes or additional test
runs were needed; the existing audit checks the relevant identities over both
prime fields and exact cyclotomic fields.

## Algebra checked

From UW=qWU and Q=U^-1, one obtains WQ=qQW. Therefore R=QW satisfies
RU=q^-1 UR and RW=q^-1 WR, giving RC=q^-1 CR. Its explicit weights are
q^(i+1)-1 for i<N-1 and -1/N at the corner. For even N their product is
`(-N)*(-1/N)=1`, proving R^N=I and that every weight is nonzero. Both R and
R^-1 are monomial operators and preserve support cardinality.

The commutation orientation is correct: C R=q R C, hence

    H_q(C) R = R H_q(qC) = R(I-C) H_q(C).

The finite q-difference identity is applicable because C^N=0. The explicit
implementation of D=R(I-C) reads coordinates i+1 and i+2 modulo N, including
the genuine corner weight. Exactly d1[N-1] vanishes; all other displayed sparse
coefficients are nonzero, so D has 2N-1 entries even at N=2. Since H_q(C) has
constant term one and nilpotent argument, it is invertible. Thus D=HRH^-1 and
D^N=I follow without assuming D itself is monomial.

## Pair coordinates checked

For m=N/2, K=R^m has K^2=I and KC=-CK. Its weights satisfy
h_i*h_(i+m)=1. The stated paired coordinates are exactly the +1 and -1
eigencomponents of K. Their inverse reconstructs both original coordinates,
using h_(i+m)=h_i^-1. Conjugating the anticommutation relation by this coordinate
map forces both diagonal blocks of C to vanish, since the characteristic is
not two. This proves a cheap first parity split, without assuming the reduced
off-diagonal blocks have a cheap recursively closed representation.

## Costs checked independently

The imported sparse-C plan uses N+log2(N) multiplications, N-1 subtractions,
one negation, and one inversion of 2. The additional grading preparation uses

    (19/2)N-3 multiplications,
    N subtractions, N negations, one inversion of 2.

The sum is precisely the README's `(21/2)N+log2(N)-3` multiplications,
`2N-1` subtractions, `N+1` negations, and two inversions of 2. The prefix/suffix
inverse-weight construction correctly uses the proved total product one;
the sliding half-shift recurrence divides by r_i via the prepared inverse_r.
No batch of uncounted individual inversions or quadratic half-window products
is hidden. Index traversal and stored arrays remain linear in N.

The input update uses N multiplications. The output update uses 2N-1
multiplications and N-1 additions. The paired split uses 3m multiplications,
m additions and m subtractions; joining uses m of each. These agree with both
the loops and the audit's assertions.

## Claim boundary retained

The first evaluation of H_q(C) is still charged in full. The reusable family
is specifically x_j=R^j x_0. Support preservation does not turn an arbitrary
fresh input into a member of that orbit, and the nonunitary weights give no
automatic approximate-error stability. The result is a valid restricted-reuse
and first-split improvement, with no independent sub-N-log-N FFT conclusion.
