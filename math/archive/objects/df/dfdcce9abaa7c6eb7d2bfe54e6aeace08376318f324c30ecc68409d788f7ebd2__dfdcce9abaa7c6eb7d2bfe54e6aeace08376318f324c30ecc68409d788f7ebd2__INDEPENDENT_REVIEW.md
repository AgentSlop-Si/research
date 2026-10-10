# Independent review of the H-specific branch-fusion checkpoint

Reviewer: a separate research agent. Reviewed `README.md`, `branch_fusion.py`,
`run_audit.py`, and the relevant copied `decimation.py`/`fixed_kernel.py`
implementations. The new ten-case branch audit was rerun; older suites were
not broadly repeated.

**Verdict: the exact identities, four-call implementation/counts, and restricted
determinant obstruction pass review, after one documentation scope correction.**
This checkpoint does not reduce the existing three-call decimation and does not
establish a faster fresh-input FFT.

## Scope correction applied with parent authorization

The original opening stated only N=2m. The implemented evaluator is dyadic:
its inherited kernel preparation rejects N that is not a power of two. More
specifically, the chosen phase-basis eigenvalues λ_i=−q^(−2i) satisfy
λ_i^m=(−1)^m. They are eigenvalues of J with J^m=I in the stated ordering only
when m is even. For odd m the proposed eigenbasis would therefore be invalid.

The README now explicitly assumes N=2^L≥4, says dyadic N≥8 for the obstruction,
and records why m being even matters. No operator/code modification was needed
for the supported prepared evaluator. The scalar E/O identities extend more
broadly, but that extension is not being substituted into the dyadic basis or
recursive implementation. The standalone obstruction helper inherits this
documented domain and the supplied-primitive-root precondition.

## Finite E/O identities and boundary

For 0≤j<m,

    (1−q^(2j+1)) t_(2j+1) = t_(2j).

For 1≤j<m,

    (1−q^(2j)) t_(2j) = t_(2j−1).

These prove E=(1−qτ)O and (1−τ)E=zO−t_(N−1)z^m as finite polynomial
identities. The second polynomial really has the indicated nonzero final
coefficient. Evaluation at D eliminates that term because D^m=0; evaluation
at cyclic J leaves −t_(N−1)I. The audit tests both cases explicitly.

The conjugation orientation is correct: JD=q^(−2)DJ implies
J^(−1)DJ=q²D. Hence τO(D)=J^(−1)O(D)J. Substituting the first identity into
the second gives DO(D)=O(D)−(1+q)J^(−1)O(D)J+qJ^(−2)O(D)J².

The copied first-level decimation retains the finite corner through its gauge
and split/merge maps. This review found no replacement of the nilpotent D by a
cyclic shift, and no dropped endpoint contribution.

## Norm identity

Write H(z)=E(z²)+zO(z²). Modulo z^N, H(qz)=(1−z)H(z). Multiplying this
relation at z and −z shows that the even polynomial H(z)H(−z)=R(z²) obeys
R(q²s)=(1−s)R(s) modulo s^m. Its constant coefficient is 1. Because
1−q^(2j) is nonzero for 1≤j<m, the remaining coefficients are uniquely the
q²-factorial coefficients. Therefore E(D)²−DO(D)²=H_(q²)(D) is valid.
This proof uses a finite quotient and does not evaluate a divergent infinite
root-of-unity series.

## Four calls and charged work

For arbitrary independent x,y, the implemented formulas are exactly

    u = O(D)x − q J^(−1)O(D)Jx + D O(D)y,
    v = O(D)x + O(D)y − q J^(−1)O(D)Jy.

They require four actions on x, y, Jx, Jy. Both the gauge and the full output
merge are present. There is no justified reduction from these four values to
two independent half-vector actions by linearity alone.

At the first half level, apply_family costs 3m multiplications and 2m additions.
One degree-(m−1) Horner action therefore costs 4m²−3m multiplications and
3m²−3m additions. Multiplying by four and counting input/output gauges,
split/merge, the extra D action, and q scalings gives:

| Operation | Exact online count |
|---|---:|
| multiplication | 16m²+4m−1 |
| addition | 12m²−5m |
| subtraction | 6m−2 |
| negation | 2 |

The total is 28m²+5m−1. The formulas agree with the executable counters.
The reused whole decimation plan and its preparation are disclosed separately;
they are not omitted from a fresh-run complexity claim. Root generation and
exact field representation remain explicit preconditions of the arithmetic
model. No claim that these operation counts are bit-operation bounds is made.

## Restricted determinant obstruction

In the corrected dyadic domain, the λ_i form the cyclic-shift eigenbasis. D
maps eigenvector i to a multiple of i+1. That multiplier is
(1+λ_(i+1))(1+qλ_(i+1)); it vanishes only on the last-to-first edge. The first
factor has that one zero, and the second cannot vanish because its required
q-exponent parity is odd. The resulting single directed path makes O(D)
triangular, with all entries on/below its diagonal nonzero.

On this support, division by O(D)_(i,j) is legitimate. The normalized block
has determinant (1−q)t(1−qt), where t=λ_j/λ_i. A factorization
L(J)diag(O(D),O(D))R(J) would make this scalar determinant a product of a row
function and a column function, even if the functions of J were dense.

For rows 2,3 and columns 0,1, the resulting 2×2 determinant is

    (1−q)² t_20 t_31 q (λ_1−λ_0) (λ_2^(−1)−λ_3^(−1)).

All factors are nonzero in the supplied exact field, so the required separation
fails. The algebraic sign and factorization of this certificate are correct.
The conclusion is confined to the specified multiplicative two-identical-kernel
form with phase-filter pre/post maps. The README correctly excludes additive
bypasses, different kernels, non-J maps, and general two-call algorithms from
this obstruction. It is not a time lower bound for FFT.

## Executable verification

`python fft_branch_fusion_research/run_audit.py` completed with PASS:

* 10 exact field/size cases;
* 66 half-basis vectors for the branch/norm relations;
* 132 full-basis vectors for the complete four-call evaluator;
* 7 nonzero determinant certificates;
* cyclic finite-remainder, broken-edge, triangular-support and exact gate-count
  checks.

These finite checks accompany the all-size algebra within the stated dyadic
domain. They are not used as numerical extrapolation to an asymptotic claim.
