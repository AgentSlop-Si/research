# Coherent sparse-jet lifting for exact Fourier synthesis

**Date:** 10 October 2026.

**Status:** A proved reduction, an explicit exact arithmetic compiler, and scoped rejection theorems. **No new arbitrary-input sub-N-log-N Fourier circuit has been constructed.** The general differentiation ingredients are classical. The two-sparse-promise formulation and its project-specific gates are a synthesis developed here, not an established publication-priority claim.

## 1. Research contract and what changes

The objective is an exact Fourier transform of every fresh input, with all N scalar outputs, sequential arithmetic, uniform coefficient and code preparation, and charged memory/indexing. It is not an approximate word-RAM result, an algorithm requiring a sparse source signal, a cached update theorem, or a speedup imported from OpenAI #130/CrocSwap.

The prior project already has (i) generic-branch differential linearization, (ii) exact fast routines on sparse or sparse-fiber promises, (iii) a marked-cycle scalar determinant target differentiated with respect to output markers, and (iv) finite-word approximate tabulation. None establishes the requested independent general bound. This note does not reclassify those results.

The question examined here is narrower and constructive:

> What additional property would let one compile a sparse-input Fourier identity into a full-input Fourier algorithm without finding a sparse representation of the actual input?

The answer is a **single regular arithmetic program with a common quadratic jet**, rather than separate support-selected programs. It is enough for a scalar program to have the correct second-order behavior on every two-coordinate plane through the origin. Its Hessian-vector circuit then handles every dense vector.

This is an equivalence of arithmetic synthesis problems, not a proof that the sparse-promise synthesis problem is easier.

## 2. Model

Let K be a field of characteristic other than 2 containing a supplied primitive Nth root omega. Set

    F[k,j] = omega^(k*j).

N >= 2; N = 1 is trivial. For complex inputs choose the usual sign convention for omega. F is symmetric and invertible. No conjugation is used below: x^T F x is a bilinear quadratic form, not a Hermitian energy.

A scalar straight-line program has N inputs and constant, add, subtract, multiply and inverse nodes. All constants are input-independent. Every intermediate inverse must be defined at input zero. A mathematically removable pole does not automatically make a particular program regular; a valid regularized program and its preparation cost must be supplied.

One scalar field operation has unit cost. An input-dependent array lookup, comparison, root identification, support index, variable exponentiation, determinant, vector transform or matrix inverse is not one such gate. Input-independent indexing and preparation are allowed but charged. Code and constants must be generated uniformly within the claimed bound. The compiler below introduces no new algebraic extensions or root oracle.

Let s be scalar arithmetic work after including relevant preparation. The general compiler has work and storage O(s+N). In particular, an O(N log log N)-work source gives O(N log log N) general storage, not automatically O(N) storage. A sharper workspace claim would require a separately proved schedule.

For finite fields, identities about parameterized inputs below are **formal rational/jet identities**. Equality merely on the finitely many field-valued inputs is not enough. Section 10 gives an exhaustive counterexample.

## 3. The two-sparse scalar target

Define

    Q_N(x) = (1/2) x^T F_N x.

For distinct i,j and formal scalar variables a,b,

    Q_N(a e_i + b e_j)
      = (1/2) omega^(i*i) a^2
        + omega^(i*j) a b
        + (1/2) omega^(j*j) b^2.                  (3.1)

One-sparse restrictions give the diagonal case. All coefficients can be addressed in a charged N-entry root table.

If the two support indices are supplied, (3.1) costs O(1) arithmetic after root preparation. Finding them in a raw N-vector costs O(N) inspections. That familiar sparse routine is NOT the required coherent scalar program: it chooses a formula based on the support and has a different execution at the origin.

### Theorem 1: sparse-jet lifting

Suppose a uniformly prepared, origin-regular scalar program Phi_N satisfies, for every two-coordinate plane,

    Phi_N(a e_i+b e_j) = Q_N(a e_i+b e_j) mod (a,b)^3.  (3.2)

The same condition is imposed on the one-coordinate restrictions. Then an explicit compiled program computes F_N v for every v in K^N in O(s(N)+N) field/index operations with O(s(N)+N) storage.

Exact agreement on all two-sparse inputs is sufficient, but agreement only through degree two is enough. No assertion about the value Phi_N(v) at dense v is required.

#### Proof

Because the program is regular at zero, it has a formal Taylor expansion there. The coefficient of a b in its restriction to a e_i+b e_j is the mixed second derivative at zero. The coefficients of a^2 and b^2 determine the diagonal second derivatives (2 is invertible). Equation (3.2) therefore gives

    Hessian(Phi_N)(0) = F_N.                         (3.3)

The compiler in Section 4 evaluates Hessian(Phi_N)(0) times one arbitrary vector in constant-factor arithmetic overhead. It produces all N outputs, without materializing the N-by-N Hessian. This proves the work and space statements. QED.

### Exact complexity comparison

Conversely, any uniformly prepared exact Fourier program with work T(N) gives a valid scalar program by computing F_N x and then (1/2) sum_i x_i (F_N x)_i. This costs T(N)+O(N).

Thus, up to constants and additive linear work,

    exact Fourier circuit synthesis
       <=> regular two-sparse quadratic-jet synthesis. (3.4)

This is the honest meaning of the reduction. The existence of a fast *support-dependent* sparse routine does not establish a short program satisfying (3.2).

### Conditional speed consequence

A coherent source of size O(N) gives O(N) Fourier work. A coherent source of size O(N log log N) gives that same Fourier bound. A source of size o(N log N) gives an o(N log N) exact transform. No such new source family is supplied in this note.

## 4. The exact compiler

The construction is forward differentiation of reverse accumulation, specialized at the origin. This is classical automatic differentiation/Hessian-vector methodology, with an explicit field-arithmetic implementation here.

For a gate z=f(y_1,...,y_r), r<=2, prepare at zero:

    p_i = partial f / partial y_i,
    h_ij = partial^2 f / partial y_i partial y_j.

First evaluate all gate values at zero. Reject any singular inverse. Compute the ordinary reverse adjoints bar(z), with bar(output)=1. These quantities depend only on the source circuit and its constants.

For a fresh vector v, set the input tangents dot(x_i)=v_i and propagate

    dot(z) = sum_i p_i dot(y_i).                     (4.1)

Initialize directional adjoints at zero, including dot(bar(output))=0. Traverse backward:

    dot(bar(y_i)) += p_i dot(bar(z))
                     + bar(z) sum_j h_ij dot(y_j).   (4.2)

The N input directional adjoints are Hessian(Phi)(0)v.

For multiplication z=a*b, the local first derivatives are b,a and the two mixed second derivatives are 1. For inversion z=1/a, they are -a^(-2) and 2a^(-3). They are prepared from proved nonzero base values. Addition/subtraction have constant first derivatives and zero second derivatives.

Every original node produces a bounded number of scalar operations. The emitted program contains only additions and multiplication by prepared scalars: no nonlinear input arithmetic or input-dependent inversions remain. Each output is explicit.

`circuit.py` implements an append-only SSA compiler with zero/one constant folding. It does not rely on an expensive global simplifier or a free common-subexpression optimizer. Its origin evaluation, local derivative preparation, reverse base adjoints, and emitted instruction construction are all O(s+N). In tests, modular inversions use Python's exact integer routines; unit field cost in the theorem is not a Python bit-time assertion.

For comparison, a full numerical Hessian construction would require N directional evaluations or N^2 storage. The new program never does that in its execution path. The verifier intentionally does use basis directions at small N to check the result independently.

## 5. A concrete four-point positive control

For omega=i (or the opposite primitive fourth root with the matching convention), put

    a=x0+x2, b=x0-x2, c=x1+x3, d=x1-x3.

Then

    Phi_4(x) = a^2/2 + b*c + omega*d^2/2             (5.1)

is exactly Q_4(x). Expanding its mixed coefficients proves the identity.

The source has 11 scalar arithmetic gates. The implemented compiler emits 18 linear arithmetic gates for F_4 v, after separately charged preparation. All 80 fresh controls in two fields agree exactly with a separately written direct DFT. This is a classical small-size identity used to validate compilation, not an optimal gate count or an asymptotic improvement.

A valid source may differ from Q_N at dense inputs. For example,

    Phi_N(x) = Q_N(x) + x0*x1*x2/(1+x0)             (5.2)

is regular at zero and exactly agrees on all two-sparse inputs in its domain. Its Hessian at zero still equals F_N. The test source deliberately builds Q_N densely in Theta(N^2) arithmetic; (5.2) is NOT a fast Fourier construction.

## 6. Exact algebraic search space

For a polynomial Phi, exact agreement with Q_N on all two-sparse formal inputs is equivalent to

    Phi - Q_N in I_3,
    I_3 = < x_i*x_j*x_k : i,j,k distinct >.          (6.1)

Indeed, a monomial with at most two distinct variables survives on at least one two-coordinate plane; its coefficient must vanish in the difference. Conversely, every monomial supported on at least three distinct variables vanishes on all such planes.

For a rational source A/B with B(0)!=0, the corresponding condition is

    A - Q_N B in I_3.                               (6.2)

Restrictions of B are nonzero polynomials because its constant is nonzero. Cross multiplication is legitimate. For the weaker sufficient quadratic-jet condition, it is enough that Phi-Q_N have no terms of total degree <=2. Higher-degree terms even on two-sparse planes are harmless to Hessian extraction.

These equations give a precise synthesis target: find a small, uniform, regular DAG representing the required quadratic jet, with arbitrary allowed higher-order behavior. They do not themselves furnish such a DAG. Computing all N^2 quadratic coefficients during every transform would forfeit the intended gain; an all-N proof or certificate is a research obligation, not an uncharged per-input algorithmic step.

## 7. Why sparse recognition and tabulation do not already give the source

### Support-dependent execution

The sparse scalar routine scans the input, identifies i,j, then evaluates (3.1). At input zero its executed branch returns zero. Differentiating that branch yields a zero Hessian. It says nothing about the neighboring nonzero-support branches.

A program that returns Q_N(x) for support<=2 and zero otherwise has correct values on the entire promise set, but for N>=3 it generally has no common quadratic Taylor expansion at zero. Along a fixed dense direction its quadratic scaling is wrong. One cannot replace a common jet by separate directional formulas.

### Singular moment formulas

One-sparse labels can be encoded by ratios such as

    j = (sum_k k*x_k)/(sum_k x_k).

The denominator vanishes at zero. Recovering a root index from this ratio additionally requires a lookup, comparison, root identification, or a nontrivial arithmetic implementation. Neither issue is removed by charging just the final phase multiplication.

The new theorem requires an actual regular circuit, not permission to differentiate a singular sparse decoder.

### Quantized predictors

The previously proposed tabulation algorithm uses data-dependent quantization and lookup. Its finite-word accuracy theorem does not supply a regular exact scalar program. On real extensions, quantized outputs are locally constant inside cells, and the origin may be a quantizer boundary; there is no automatic Fourier derivative at zero. The present construction does not contradict the finite-word result or turn its approximation into an exact transform.

## 8. Full-dimensionality gate even for the scalar sparse promise

### Theorem 2: compressed linear transcript obstruction

Suppose Phi(x)=f(Ax), where A has r rows and is input-independent, and f is regular at zero. Then

    Hessian(Phi)(0) = A^T Hessian(f)(0) A,

so its rank is at most rank(A)<=r. If Phi has the Fourier two-sparse jet, invertibility of F_N forces r>=N.

This theorem concerns a fixed linear transcript followed by regular processing. It is not a rank lower bound on every nonlinear circuit or every input-adaptive measurement strategy.

The significance is that even this *scalar promise task* cannot be made coherent at zero through only O(1) fixed moments. Support-specific sparse recovery may use a short transcript precisely because it does not provide the required common regular jet.

## 9. A rejection theorem for the simplest product-based synthesis

Consider

    Phi(x) = diagonal quadratic + affine terms
             + sum_(ell=1)^r c_ell prod_(j=0)^(N-1)
                                      (b_(ell,j)+a_(ell,j)*x_j). (9.1)

All endpoint constants may vanish. This retains zero-anchor cases rather than dividing them away.

### Lemma: one separable product

If every b_j is nonzero, with B=prod b_j and v_j=a_j/b_j, the Hessian at zero is

    B*v*v^T - diag(B*v_j^2).

It is rank one after a diagonal correction. With exactly one zero b_j it is a symmetric star of rank at most two. With exactly two zeros it is supported on the corresponding symmetric off-diagonal pair and has rank at most two. With at least three zero factors its Hessian is zero.

Therefore (9.1) has Hessian R+Delta, with Delta diagonal and rank R<=2r. If all product anchors are nonzero, rank R<=r.

### Fourier-minus-diagonal lemma

For any diagonal Delta,

    rank(F_N-Delta) >= floor(N/2).                  (9.2)

Choose m=floor(N/2) consecutive Fourier rows 0,...,m-1 and m columns outside those row indices. The diagonal vanishes on this rectangle. Its Fourier block is a square Vandermonde matrix on distinct roots and is invertible. The lemma works for every admissible N, not only primes.

### Theorem 3: product count

Exact Fourier quadratic jets of the form (9.1) require

    2r >= floor(N/2).

If all anchors are nonzero, they require r>=floor(N/2).

Thus a fixed number of elementary coordinate-separable product terms cannot supply the desired source. This is a *term-count/representation* restriction. A large number of terms might be represented by a shared DAG; no general arithmetic lower bound follows from treating their unexpanded number as their cost.

This is the point where genuine graph reuse would have to enter: many correct pair interactions must be shared in an actual short regular circuit, rather than counted as independently evaluated product terms.

## 10. A finite-field certificate trap, checked exhaustively

Over F_p, the scalar expressions

    Phi(x) = Q_N(x) + (x0^p-x0)*x1

and Q_N agree on every field-valued input. Nevertheless their formal mixed second derivatives at zero differ by -1 in the (0,1) and (1,0) positions.

For p=17,N=2, the verifier exhausts all 289 possible inputs: the scalar values all agree. The formal quadratic jet and the compiled Fourier result fail, as they must.

Thus even exhaustive finite-field value tests are not an adequate replacement for the formal sparse-jet condition when arbitrary polynomial degree is allowed. Formal truncated-polynomial arithmetic, an explicit symbolic identity, or an appropriate verified degree/unisolvence bound is required.

## 11. Dense full-rank positive controls that are not Fourier

Let L be the lower-triangular all-ones prefix matrix and define

    Phi(x) = (1/2) sum_i (sum_(j<=i) x_j)^2.

It has a linear-size arithmetic circuit and Hessian L^T L, whose entries are N-max(i,j). The Hessian is dense and invertible, yet it is not Fourier. Two scans apply it in linear work.

The compiler reproduces this family through N=128. Source work is 4N gates; emitted work is 5N-2 for the tested formula and folding policy. This checks that the compiler can preserve a genuine linear-size mechanism. It also prevents 'dense/full-rank Hessian' from being mistaken for Fourier phase compatibility.

## 12. Reproducibility

Run `python verify.py` using the Python standard library. The recorded run passes seven groups:

- 372 Fourier basis vectors and 150 dense vectors, checking 10,044 output coordinates, across sizes 2,4,8,16,32 in two prime fields;
- 438 independent bivariate formal quadratic-jet checks and 1,314 two-sparse scalar value checks;
- 30 general regular arithmetic circuits, checked by 180 independent formal mixed-direction computations;
- the 11-gate four-point scalar source, its 18-gate emitted transform, and 80 fresh vector checks;
- six linear-size dense/full-rank/non-Fourier controls through N=128;
- 64 Fourier-minus-diagonal rank checks and 32 separable-product controls including 0,1,2,3 zero anchors;
- support-branch, singular-inverse, one-sparse-only and exhaustive Frobenius negative controls, plus the two-moment Hessian-rank check.

The source Fourier potentials at larger sizes are deliberately Theta(N^2). Their compiled programs are correctness controls, not sub-NlogN constructions. The experiment's root search is test setup, separate from the supplied-root computational contract. Finite checks substantiate code and fixed cases; the displayed all-N reductions are proved above.

## 13. Prior art and honest endpoint

Baur--Strassen's partial-derivative complexity theory and Pearlmutter's Hessian-vector method are established. The archive also already records generic-branch linearization and a different marked-cycle derivative proposal. This note's additional formulation is the two-sparse scalar/formal-jet equivalence, the explicit compiler, the support-chart and finite-field rejection controls, and the exception-complete separable-product gate. A limited comparison cannot certify external priority for these consequences.

Current official OpenAI Math #130 documentation reports a separate uniform exact-complex O(N(log N)^(1-10^-13)) result with supplied roots and unrestricted coefficients. That result is a comparator, not a backend in this work. This note does not improve it or establish a new independent general upper bound.

**Unresolved constructive target:** a uniformly generated origin-regular scalar circuit with the Fourier two-sparse quadratic jet and total work o(N log N), ideally O(N log log N). Finding such a circuit would genuinely complete an exact faster-FFT construction via the implemented compiler. Neither a fast support-selected oracle, a small-input numerical fit, a finite-field pointwise identity, nor the reduction itself supplies that circuit.

## Primary references

1. W. Baur and V. Strassen, *The complexity of partial derivatives*, Theoretical Computer Science 22 (1983), 317--330. DOI 10.1016/0304-3975(83)90110-X. Publisher record: https://www.sciencedirect.com/science/article/pii/030439758390110X
2. B. A. Pearlmutter, *Fast Exact Multiplication by the Hessian*, Neural Computation 6 (1994), 147--160. DOI 10.1162/neco.1994.6.1.147. Publisher record: https://doi.org/10.1162/neco.1994.6.1.147 ; author-deposited record: https://mural.maynoothuniversity.ie/id/eprint/5501/
3. OpenAI Math, *Exact Fourier transforms below n log n*, official scope statement checked 10 October 2026: https://github.com/openai/math/blob/main/lean/docs/130.md . No proof-kernel build or complete independent audit of the external result was performed.

Project inputs and reviewed-scope limits are recorded in SOURCE_LEDGER.md.
