# ALG-010: cyclic hypergeometric antecedent and exact interface boundary

14 October 2026. Source comparison candidate for independent review.

## Verdict and exact stopping condition

The selected primary-source comparison is complete: the regular periodic
q-ratio Fourier identity is a direct match to classical cyclic hypergeometric
weights, explicitly printed in Au-Yang–Perk's 1996 preprint. This is a
substantial antecedent, not merely a shared use of recurrence terminology.
The full ALG-010 raw-input recognizer and degenerate finite-boundary interface
are not supplied by the compared formulas. This is a qualified nonmatch for
that complete interface, not evidence of its worldwide novelty.

The queue asked for one finite q-difference comparison mapping unknown
coefficient discovery, cyclic closure, singular recovery and full-output
cost. Sections 2-6 supply those mappings. Retire only this selected comparison;
keep ALG-010's broader attribution/numerical/bit obligations open. Preserve
its existing priority and accepted correctness; no arbitrary-input FFT or
new asymptotic improvement is claimed.

## 1. Sources actually inspected

The local accepted ALG-010 README has SHA256
952f1d290c9b71058687de0c663a58ec7883b0465edf12cf72496e1fcce7b2d6;
its independent review has SHA256
7ce2a4690ba68ede92d38300639922bccecb5ac2819eee14c8cb3636b2ab8743.
Both were read as text. No historical program was imported or executed.

Primary comparison: Au-Yang and Perk, The Many Faces of the Chiral Potts
Model, arXiv:q-alg/9609003v1 (1996), Section 9.1, page 11, equations
(26)-(29). It displays periodic first-order q-ratio weights, defines their
positive-sign Fourier transform and derives its transformed product from
the recurrence. The same map is explicit in Perk–Au-Yang,
Recent Developments on Ising and Chiral Potts Model, arXiv:math-ph/0606027v1
(2006), page 4, equations (12)-(14). These authors cite earlier work; the
present comparison does not establish earliest priority.

- https://arxiv.org/pdf/q-alg/9609003v1
- https://arxiv.org/pdf/math-ph/0606027v1

Relevant PDF sections were read through text extraction. No PDF-byte hash or
visual-facsimile audit is claimed. evidence/PRIMARY_SOURCE_NOTES.md records
access, precise locators, corroborating 2016 equations and the failed optional
2002 author-site fetch. No verdict depends on that inaccessible copy.

## 2. Exact parameter and model match

Use the ALG-010 positive-sign unnormalized DFT
 y_k = sum_(n=0)^(N-1) q^(kn) x_n,
with q primitive of order N. The article's omega is exactly this q. Work
over C for the direct source comparison. The following algebraic deductions
also hold in any field containing that primitive root when their displayed
denominators are nonzero; that field statement is our explicit derivation,
not an attribution of a finite-field implementation theorem to the article.

For a safely regular intersection take x_0 != 0, alpha,beta,gamma != 0,
alpha^N != 1, beta^N != 1, alpha^N != beta^N and

 gamma^N (1-alpha^N) = 1-beta^N.

Define (a;q)_n=product_(i=0)^(n-1)(1-a q^i). Then

 x_n = x_0 gamma^n (alpha;q)_n/(beta;q)_n

satisfies ALG-010's relation with

 (p0,p1,r0,r1) = (-gamma, gamma alpha, 1, -beta).

Conversely, on the chart p0*r0 != 0,
 gamma=-p0/r0, alpha=-p1/p0, beta=-r1/r0,
after dividing the relation by r0. This chart is a restricted part of the
source's projective quadruple space. No normalization involving a zero
p0 or r0 is silently applied to a degenerate branch.

The cyclic product closes because product_i(1-a q^i)=1-a^N. Hence x_N=x_0
under the stated constraint, so the actual cyclic source residual Lx is zero.
Substitute the parameter map into ALG-010's accepted Fourier identity:

 (q^(-k)-gamma)y_k + (gamma alpha-beta q^(-k-1))y_(k+1)=0.

Multiplication by q^(k+1) and rearrangement give

 (beta-alpha gamma q^(k+1))y_(k+1)
   = q(1-gamma q^k)y_k.

Thus the transformed q-ratio has

 alpha_hat=gamma, beta_hat=q alpha gamma/beta, gamma_hat=q/beta.

This is precisely the parameter map displayed in the primary comparator.
The calculation independently verifies the Fourier sign, index shift and
extra q in beta_hat. No change of transform convention is concealed.

## 3. Regular-dual guard and singular scale

Input regularity alone is insufficient for a directly usable normalized
Fourier product. Under periodicity,

 gamma^N=1 iff alpha^N=beta^N,
 beta_hat^N=1 iff alpha^N=beta^N.

The second equivalence uses beta != 0 and alpha^N != 1. Our extra
alpha^N != beta^N guard therefore makes every numerator and denominator
of the transformed cyclic ratios nonzero. Since the DFT is invertible and
x != 0, one y_k is nonzero; recurrence then makes every y_k nonzero,
including y_0. Normalization by y_0 is consequently legitimate on this
explicit intersection.

Importantly, this periodic branch ALREADY has a singular homogeneous target
operator J: its nonzero y lies in the one-dimensional kernel. The compared
formula gives all ratios, and y_0=sum_n x_n determines the scale. It would be
incorrect to call all singular recovery an unmatched ALG-010 contribution.
In this matched branch the familiar Fourier product and a paid initial sum
already recover the missing scalar.

The full ALG-010 singular method permits a different anchor: compute source
kernel v and target kernel h, choose j with v_j != 0, and use
sum_k q^(-kj)y_k=N x_j. Similarity ensures the corresponding functional on
h is nonzero. This handles cases where the displayed classical normalization
at Fourier index zero is undefined; the accepted local review supplies its
proof. The comparison does not establish that no earlier paper has an
alternative anchor, limiting formula or complete degenerate algorithm.

## 4. Endpoint forcing: a concrete nonmatch

ALG-010 imposes its relation only for 0<=n<N-1, then pays the actual cyclic
endpoint residual. It does not assume the periodic product constraint.
On the regular source-ratio chart, extend one more step and define
 delta=x_N-x_0.
The cyclic last residual is
 u_(N-1)=-(1-beta/q)delta.
The same Fourier calculation now yields

 (beta-alpha gamma q^(k+1))y_(k+1)
   = q(1-gamma q^k)y_k + delta(q-beta).

The article's homogeneous product is recovered when delta=0. Omitting this
extra term outside that case changes the problem.

Exact example over Q(i): N=4, q=i, x=(1,2,4,8), with parameters
(-2,0,1,0). Every required N-1 source relation holds, but x_4=16 rather
than x_0=1. Here delta=15 and u_3=-15. The correct transform is

 (15, -3-6i, -5, -3+6i),

or y_k=15/(2q^k-1). Its target operator is nonsingular diagonal. The zero
forcing substitution would return zero, demonstrably wrong. This example
separates the accepted finite-boundary interface from the compared regular
periodic formula; it is not a counterexample to that formula's hypotheses.

There is also a periodic normalization boundary: N=4, q=i,
x=(1,i,-1,-i) has y=(0,0,0,4). One may represent the source ratio using
alpha=beta=2 and gamma=i. The normalized expression y_k/y_0 is undefined.
ALG-010's accepted source-kernel/input-constraint method still determines
the exact output. A meromorphic limiting identity or a different normalization
may handle this example mathematically; the displayed normalized formula
alone is not that complete executable branch. The zero input likewise has
no x_n/x_0 normalized representation but is admitted by the raw source.

## 5. Unknown discovery and complete paid output

The primary formula receives alpha,beta,gamma and normalizations. It does
not, in the compared statements, certify an arbitrary fresh array or select
an unknown nonzero projective quadruple from all its entries. ALG-010 does
that using the N-1 by 4 system with rows
 [x_i,q^i x_i,x_(i+1),q^i x_(i+1)].
Streaming exact rank/nullspace computation and a full residual recheck cost
O(N) field operations; rejection and any fallback remain paid. Those are
ordinary exact linear-algebra ingredients, not a reason to infer novelty.

Conversely, the matched supplied-parameter periodic case DOES imply a paid
O(N) all-output evaluator by a simple implementation deduction:

1. Read all x and build/validate the supplied dyadic root table in O(N).
2. Check regularity, the parameter relation and all source equations in O(N).
3. Compute y_0=sum_n x_n in O(N) additions.
4. Generate all subsequent y_k with the transformed ratio, using O(N)
   multiplications/additions/inversions, and write all N outputs.

All arrays fit O(N) field-element storage; output alone is length N. No
fractional powers, complex branch-choice oracle, or repeated N-term sum per
frequency is needed. This operation-count corollary is our transparent
implementation inference from the identity, not a quoted runtime theorem of
the physics paper. Root acquisition, bit representation, floating precision,
conditioning and failure detection are extra model requirements.

For comparison, the local accepted review already charges N field operations
for root powers, 12N for bands/residual/forcing, up to 9N-1 for a nonsingular
nonzero-edge target solve, or 7N-3 before singular completion, with at most
13N+2 for its source-kernel/input constraint. Discovery, comparisons, copies
and output writes are also paid. Those existing counts are retained, not
rerun or newly certified as host-machine measurements here.

## 6. Exact disposition by obligation

- Degree-one periodic q-ratio family: direct classical match.
- Fourier sign and transformed coefficients: exact match by explicit map.
- Generic periodic singular scale: classical normalized product plus one
  paid sum already suffices; no broad singular-recovery novelty assertion.
- Unknown-quadruple raw recognition and rejection: not supplied by the
  compared formulas; standard linear algebra is used by the local source.
- Nonzero endpoint residual: genuinely outside the homogeneous periodic
  formula, with an exact separating example.
- Zero bands, zero data, zero Fourier anchor and degenerate coefficient
  charts: not certified by direct use of the regular normalized formula.
- Full-output O(N) field work on the matched regular subfamily: follows by
  the explicit paid implementation above; therefore linear work there is
  not a new asymptotic distinction from this antecedent.
- Complete-interface priority, numerical stability, uniform bit complexity,
  and generic-input FFT acceleration: not settled by this comparison.

This satisfies the queue's selected match/nonmatch stopping condition once
independently reviewed. It does not close the broader ALG-010 parent merely
because a major algebraic component is classical.

## 7. Fresh controls and reproducibility boundary

fresh_comparison_controls.py uses only the standard library and new exact
arithmetic. It imports no historical module. On 120 regular periodic tuples
at N=4,8,16,32,64 it checks all 2,976 Fourier coordinates against a dense
finite-field DFT, the mapped four-column relation, Fourier recurrence and
normalized product. All 120 omitted-q-shift mutants are detected. Exact
Gaussian-rational controls verify both characteristic-zero examples, the
endpoint-omission failure and zero-input normalization boundary. The finite
field controls corroborate our elementary algebra, not an attributed
finite-field software implementation from the primary paper. Results are
in results/COMPARISON_CONTROLS.json. Universal parameter claims rest on the
algebraic derivation above, not the finite census.
