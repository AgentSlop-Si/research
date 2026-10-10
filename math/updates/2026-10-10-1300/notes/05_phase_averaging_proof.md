# Finite phase averaging: complete proof and boundary witnesses

Date: 10 October 2026.

## Verdict and exact scope

**Accepted.** The finite phase-averaging construction, source SHA-256
`880c45d731f4d5296f7f73ba637838542ada72dd321adb3b2b553458b5723fda`, has a correct
finite construction. The complex span of legal unitary Hamiltonian-cycle Green
resolvents is exactly the space of constant-diagonal complex matrices. In fact,
one explicit finite diagonal-conjugacy orbit of one fixed legal cycle already
has that span. A column phase gauge puts every Fourier matrix in this space.

The stated N=2 and N=3 witnesses are actual finite Green-resolvent sums with
real coefficients. Consequently the lower endpoint N=4 of the real-collinear
exclusion is sharp for this directed-cycle matrix model. N=1 depends on whether
a weighted one-vertex loop is admitted; with loops it is immediate.

This verdict concerns algebraic correctness and the stated model. It makes no
claim of historical priority, an optimal term count, an FFT speedup, or an
arithmetic-complexity lower bound. The finite controls below supplement the
all-N proof; they do not replace it. No author/uploaded program was imported or
executed in this review.

## 1. The legal objects and the cycle-support guard

For N>=2 let W be a monomial matrix supported on one directed N-cycle. After a
simultaneous relabeling, write

    W e_b = w_b e_(b+1 mod N),    |w_b|=1,
    H = product_(b=0)^(N-1) w_b != 1.

This convention admits a directed 2-cycle with both reciprocal directed edges.
It does not mean an undirected simple graph's Hamiltonian-cycle convention,
which sometimes starts only at N=3. Each row and column has exactly one
nonzero entry of modulus one, so W is unitary.

One complete circuit gives W^N=H I. The geometric identity gives

    (I-W)(I+W+...+W^(N-1)) = (1-H)I,
    G = (I-W)^(-1) = (I+W+...+W^(N-1))/(1-H).

Both left and right inverses follow because the factors are polynomials in W.
Thus every inverse used here exists literally, with no limiting argument. If
H=1, the same weighted recurrence around the cycle produces a nonzero fixed
vector of W, so the excluded condition is genuinely singular.

For every ordered pair (a,b), exactly one k in {0,...,N-1} carries b to a.
Only that power W^k contributes to G_ab, and its entry is a product of unit
phases. Hence every G_ab is nonzero. Only k=0 contributes on the diagonal, so

    G_aa = d = 1/(1-H) != 0   for all a.

The single-cycle condition matters: a disjoint cycle cover cannot provide
nonzero entries between different cycles, and diagonal conjugation cannot
repair these missing entries.

## 2. A finite phase orbit stays entirely legal

Let zeta=exp(2*pi*i/3),

    T = {(0,t_1,...,t_(N-1)): each t_j in {0,1,2}},
    Q = |T| = 3^(N-1),
    D_t = diag(zeta^t_0,...,zeta^t_(N-1)).

Define W_t=D_t W D_t^*. Every D_t is unitary. The support of W_t is exactly
the same directed Hamiltonian cycle. Each edge is multiplied by a ratio of
unit phases, and these ratios telescope around the cycle. Thus its holonomy
remains H, and every W_t remains unitary and nonsingular at spectral parameter
1. More explicitly,

    I-W_t = D_t (I-W) D_t^*,
    G_t = (I-W_t)^(-1) = D_t G D_t^*,
    (G_t)_ab = G_ab zeta^(t_a-t_b).

These equalities distinguish the internal conjugation D_t from the different
external column gauge used for Fourier below. No phase gauge changes a cycle
edge's modulus or uses a forbidden inverse.

## 3. Explicit filters and the exact complex span

For a!=b let chi_ab(t)=zeta^(t_a-t_b). With e_0=0, its exponent vector in
(Z/3Z)^(N-1) is e_a-e_b. These N(N-1) vectors are nonzero and distinct:

- If one endpoint is 0, there is one nonzero coordinate, whose value 1 or -1
  identifies its direction.
- If neither endpoint is 0, there are two nonzero coordinates, one +1 and one
  -1, which identify the ordered endpoints.

Here +1 and -1 are distinct modulo 3. Modulo 2 they coincide, so the opposite
directed entries would alias; binary phases do not provide these filters.

For any v in (Z/3Z)^(N-1), direct factorization gives

    (1/Q) sum_(t in T) zeta^(v dot (t_1,...,t_(N-1)))
      = product_(j=1)^(N-1) [(1+zeta^v_j+zeta^(2v_j))/3]
      = 1 if v=0, and 0 otherwise.

Thus, entry by entry,

    (1/Q) sum_t G_t = d I,
    (1/Q) sum_t conjugate(chi_ab(t)) G_t = G_ab E_ab  (a!=b).

This is the complete finite filtering proof; it does not invoke a continuous
average or an approximation. Because d and every G_ab are nonzero, both I and
every off-diagonal matrix unit E_ab are in the complex span.

For any X with common diagonal x, the following is an explicit coefficient
formula on the same finite family:

    alpha_t = (1/Q) [x/d
                  + sum_(a!=b) (X_ab/G_ab) zeta^(-(t_a-t_b))].

Using the displayed filters proves exactly

    X = sum_(t in T) alpha_t (I-W_t)^(-1).

There are at most Q displayed nonzero terms. Conversely, every orbit member
has diagonal d, so every complex combination has a common diagonal. Every
legal Hamiltonian-cycle Green matrix, even with a different cycle order or
holonomy, has a common diagonal by Section 1. Consequently

    span_C {G_t: t in T}
      = span_C {all legal unitary Hamiltonian-cycle Green resolvents}
      = {X in C^(N by N): X_00=...=X_(N-1,N-1)}.

This space has dimension N(N-1)+1. The formula supplies an explicit bound
3^(N-1), not a minimality claim. Individual diagonal matrix units cannot be
isolated, because all diagonal entries carry the same trivial character.

## 4. Fourier belongs after the exact column gauge

Use the unnormalized positive-exponent Fourier convention

    omega=exp(2*pi*i/N),    F_N[a,b]=omega^(ab),
    B=diag(omega^(-b^2))_(b=0)^(N-1).

Every diagonal entry of X=F_N B is omega^(a^2-a^2)=1. B is unitary and
invertible. Section 3 therefore gives X as a finite complex Green sum, and

    F_N = X B^(-1).

This is the claimed monomial equivalence. No row/column permutation is
needed. Changing to a normalized Fourier convention only adds a nonzero
global scalar. The quadratic exponent in B has a minus sign; using a plus
sign generally fails to make the diagonal constant.

### Explicit N=4 instance

Choose w_0=w_1=w_2=1 and w_3=-1. Then H=-1 and

    G_ab = s_ab/2,
    s_ab = +1 if a>=b, and -1 if a<b.

With omega=i and t=(0,t_1,t_2,t_3),

    alpha_t = (2/27) [1 + sum_(a!=b)
                       s_ab i^(ab-b^2) zeta^(-(t_a-t_b))].

The exact 27-term sum is F_4 diag(1,-i,1,-i). Two of these coefficients are

    alpha_(0,0,0,0) = (6+4i)/27,
    alpha_(0,0,0,1) = (6+(4+2 sqrt(3))i)/27.

The imaginary part of the first times the conjugate of the second is
-4 sqrt(3)/243, which is nonzero. These coefficients therefore do not lie on
one real line through the origin in C. This directly checks the model change
at N=4, without using the abstract exclusion as a black box.

## 5. Actual real-coefficient witnesses at N=2 and N=3

### N=2

Take

    W = [[0,-1],[1,0]],
    G = (I-W)^(-1) = (1/2)[[1,-1],[1,1]]
      = (1/2) F_2 diag(1,-1).

W is unitary, has the directed 2-cycle support, and has H=-1. This single
Green term, with coefficient 1>0, is already monomially equivalent to F_2.

### N=3

Let omega=exp(2*pi*i/3), H=omega^2, and

    d = 1/(1-omega^2) = (1-omega)/3.

Choose W e_0=e_1, W e_1=e_2, W e_2=omega^2 e_0. Then

    G = d [[1,omega^2,omega^2],
           [1,1,omega^2],
           [1,1,1]].

For u,v in {0,1,2}, put D_uv=diag(1,omega^u,omega^v) and
W_uv=D_uv W D_uv^*. Set

    (alpha_uv) = (1/9) [[4,4,1],
                       [1,-2,1],
                       [4,-2,-2]],

with u as the row index and v as the column index. Every coefficient is real;
their sum is 1. All nine W_uv have unit-modulus edges and H=omega^2!=1.

The target is

    X = d F_3 diag(1,omega^2,omega^2)
      = d [[1,omega^2,omega^2],
           [1,1,omega],
           [1,omega,1]].

In the filter formula of Section 3, x/d=1. Every off-diagonal ratio X_ab/G_ab
equals 1 except X_12/G_12=omega^2 and X_21/G_21=omega. Hence

    9 alpha_uv = 1 + omega^u + omega^(-u)
                  + omega^v + omega^(-v)
                  + omega^(2-u+v) + omega^(-2+u-v).

Each pair of nonconstant terms is a conjugate pair. Evaluating
omega^k+omega^(-k) as 2 if k=0 modulo 3 and -1 otherwise gives exactly the
integer table above. The filtering identity therefore proves

    X = sum_(u,v=0)^2 alpha_uv (I-W_uv)^(-1).

Both external factors d I and diag(1,omega^2,omega^2) are invertible, so this
is an actual real-linear Green realization monomially equivalent to F_3.
It is not merely a witness for a necessary cross-ratio condition.

For a direct structural check, d omega^2=-conjugate(d), and d omega is purely
imaginary. Thus X has common diagonal d and skew-Hermitian off-diagonal
entries, exactly as a real Green sum must.

### N=1

If a weighted one-vertex loop is legal, take W=[-1]. Then G=[1/2] and
2G=F_1=[1], with a positive real coefficient. The complex-span formula also
extends with T a singleton and no off-diagonal terms. If loops are excluded,
there is no legal one-vertex Hamiltonian-cycle object; no realization claim
is made under that convention.

## 6. Why the real-collinear restriction is essential

For completeness, the connection to the all-length exclusion can be checked
independently and briefly. If W is unitary and I-W invertible, then

    G^*=(I-W^(-1))^(-1)=-W(I-W)^(-1),
    G+G^*=I.

Thus a real linear combination M of the legal Green matrices has a common
diagonal d and satisfies M_ij=-conjugate(M_ji) for i!=j. A common complex
coefficient line lambda R can be reduced to this case by dividing M by
lambda, an allowed nonzero scalar gauge.

Suppose such a nonzero M were monomially equivalent to F_N. Every entry must
be nonzero. Its paired cross-ratios obey

    M_ii M_jj/(M_ij M_ji) = -d^2/|M_ij|^2.

Fourier's four-entry cross-ratios have modulus 1 and this property survives
invertible diagonal gauges and permutations. It follows that |M_ij|=|d|,
so every paired cross-ratio equals the same phase eta. If a_i and b_i are
the distinct Fourier row and column labels at diagonal coordinate i, then

    eta = omega^((a_i-a_j)(b_i-b_j))  for every i!=j.

Relabel coordinates so a_i=i. For a fixed c modulo N this becomes

    (i-j)(b_i-b_j)=c mod N.

Adjacent pairs force b_i=b_0+ic modulo N. Since b is a permutation, c is a
unit modulo N. When N>=3, the pair (0,2) yields 4c=c modulo N, forcing
N|3. This contradicts N>=4. (For N=2 that pair does not exist.)

Together with Sections 3-5, this proves the precise boundary: all N>=4 are
excluded for real-collinear sums, but the unrestricted complex-coefficient
model contains a column-gauged Fourier matrix at every size with a legal
cycle convention. Accordingly, at N>=4 the nonzero coefficients of any such
Fourier-equivalent representation cannot all be real-collinear.

## 7. Fresh exact controls and negative controls

The supplied `independent_exact_checks.py` was written for this review using
only Python's standard library. It implements exact rational arithmetic in
Q[z]/Phi_L(z), with L=6,12,30, rather than floating-point tolerances.

The reproducible results in `EXACT_CHECK_RESULTS.json` report:

- Direct exact complex Fourier identities for N=2,3,4,5,6, using respectively
  3,9,27,81,243 displayed terms.
- Direct exact identities for asymmetric constant-diagonal targets at N=2,3,4.
- For every displayed orbit matrix in those tests: one-cycle support,
  unitarity, unchanged nonsingular holonomy, a two-sided inverse identity,
  nonzero entries, a constant diagonal, and G+G^*=I.
- Exact N=2 and N=3 real-coefficient witnesses, including evaluation of all
  nine N=3 coefficients and their sum.
- Distinct nontrivial directed-entry characters through N=8 and the full
  13-by-13 character Gram matrix for N=4.
- The explicit N=4 noncollinearity pair from Section 4.
- Negative controls detecting singular H=1, opposite-entry aliasing with
  binary phases, a disconnected cycle cover's missing cross-block support,
  and the wrong sign of the Fourier quadratic column gauge.

All checks passed. These finite checks support the proof's formulas and
guards; no extrapolation from tested sizes is needed for the theorem.

See REPRODUCE.md for the portable independent verifier and exact mathematical results.

## 8. Classical ingredients and attribution boundary

The geometric resolvent identity, invariance of matrix inversion under
similarity, unitary diagonal conjugation, finite-character orthogonality,
and diagonal-gauge cross-ratios are classical algebraic ingredients.
For an independently available exposition of the finite-character step,
see Keith Conrad, [Characters of Finite Abelian Groups (Short Version)](https://kconrad.math.uconn.edu/blurbs/grouptheory/charthyshort.pdf), Section 4.

The material reviewed here specializes these ingredients to the fixed
holonomy orbit of a legal Hamiltonian-cycle resolvent, states the explicit
coefficient formula, applies the quadratic column gauge to Fourier, and
supplies the displayed small-size witnesses. These are additions to this
review package, separate from the submitted all-length exclusion proof.
Neither this terminology nor this acceptance verdict establishes that those
specializations are historically new. No publication-priority search or
runtime claim is part of this verdict.
