# ALG-011: cold recurrence-defect discovery, primary-source comparison

Date: 16 October 2026. Scope: one bounded comparison of the accepted extended theorem, including zero and singular shifts. This report introduces no new implementation acceptance or historical-priority claim.

## Result

**Qualified nonmatch for the full algorithmic contract; exact match for a classical intermediate representation.** Sparse residual Fourier values are ordinary exponential moments and have the associated rational generating series. That observation does not identify the residual support cap with ordinary recurrence order of the raw input or the complete output, and it does not recover a missing singular kernel amplitude. The cold algorithm still pays to discover the unknown shift, verify every raw residual coordinate, form the complete forcing, reconstruct the actual input's transform and emit all outputs.

The recorded gate permits a primary theorem with an exact hypothesis/formula/cost mapping or a qualified nonmatch. This comparison meets that bounded alternative. It does not establish worldwide novelty, optimality, a universal FFT improvement, or production readiness. No independent implementation or numerical task is newly promised.

## 1. The exact selected theorem

Work over an exact field with a supplied primitive Nth root q, for dyadic N >= 4. Supply the whole fresh vector x and a nonnegative support cap s. The positive-sign Fourier matrix is F[k,j] = q^(kj). The retained operators are

    E[i,i] = -q^i,
    E[i,i+1] = -q^i(q^(i+1)-1),  0 <= i < N-1,
    (Jy)_i = (q^(-i-1)-1)y_(i+1) - q^(-i-1)y_(i+2),

with cyclic output subscripts, and FE = JF. The accepted family is exactly

    support(x) <= 2s, or there exists lambda in the field
    with support((E-lambda I)x) <= s.

The **extended** theorem includes lambda = 0 and eigenvalues lambda = -q^t. The older detector's nonzero/non-root exclusions are historical restrictions of its older solver; they must not be restored as current hypotheses.

If m = support(x) > 2s, a valid lambda is the strict majority of (Ex)_i/x_i over nonzero x_i. Cross-products discover the candidate; the final verification computes every coordinate of u = (E-lambda I)x, including positions with x_i = 0. A positive cancellation balance is insufficient. The boundary m = 2s belongs to direct sparse evaluation. The accepted algorithm has O(N(s+1)) exact field/word work and O(N) live field storage; unsupported inputs decline after O(N) work.

Source: the [extended recurrence theorem and ledger](https://github.com/AgentSlop-Si/research/blob/8172ebf0371ef83a6c5aaa2de778358c89088b22/math/archive/objects/5a/5a1a90472e1661763d2132869ad5a3e44c8da53c8bd5e9bf7b248e793afd6c6a__5a1a90472e166176__README.md) and its independently reviewed historical source set, whose exact byte checks appear in SOURCE_HASH_CHECKS.json. All four texts were read; supplied programs were not executed.

## 2. Primary comparator and its precise endpoint

Massey's Theorem 2 and Section III algorithm synthesize a shortest constant-coefficient LFSR for a supplied finite sequence a_0,...,a_(n-1), over a field. The defining equations are a_j + sum_(i=1)^L c_i a_(j-i) = 0 for L <= j < n. On a nonzero next discrepancy, the new minimal length is max(L,n+1-L). The algorithm uses discrepancy-dependent polynomial corrections. Theorem 4 describes the infinite generated series as P(z)/C(z), with C(0)=1 and deg P < L. Neither result takes the operator E, a sparse E-shift residual, or a Fourier reconstruction request as its contract. See [Massey, 1969, pp. 122–126, equations (2), (14), Theorems 2 and 4](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf).

The comparison is with these actual equations and endpoints. In particular, allowing an untapped last LFSR stage, c_L = 0, is not the same condition as singularity of J-lambda I.

## 3. Exact mapping that does hold

The following deductions apply the selected representation to the already verified residual. Write S = support(u), d = |S| and b = Fu. Extend the frequency index periodically to k >= 0. Direct substitution gives

    b_k = sum_(j in S) u_j (q^j)^k,
    B(z) = sum_(k>=0) b_k z^k = sum_(j in S) u_j/(1-q^j z).

For d > 0 the q^j are distinct and each u_j is nonzero. At z = q^(-j), the numerator after multiplication by product_(r in S)(1-q^r z) has value u_j product_(r != j)(1-q^(r-j)), which is nonzero. Thus no denominator factor cancels: the reduced denominator has degree d. This is a genuine classical d-mode representation, not a title-level resemblance. When d = 0, b is identically zero.

It is also the representation used by [van der Hoeven–Lecerf, 2024, Section 5, Algorithm 4 and equation (10), p. 14](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf): black-box evaluations of a sparse polynomial are used to recover its terms, through rational reconstruction, root finding, exponent recovery and coefficient recovery. The stated root-order requirement is at least max(D,2T); those stages have costs and field conditions.

Here f(z) = sum u_j z^j is already explicitly known after verification. For the recurrence branch, d <= s < m/2 <= N/2; taking D=N and T=d therefore meets that order condition with the supplied q when d>0. But running interpolation to rediscover known u is the reverse of the required evaluation task. Computing the sample values, or all N values, cannot be treated as free access to a black box. Root extraction or discrete logarithms are not secretly included in ALG-011's ledger: known indices j directly determine the phase roots q^j.

## 4. Why the match does not extend to the full contract

### The support cap is not a general recurrence-order parameter

For the raw sequence, the zero-defect relation is

    (-q^i-lambda)x_i - q^i(q^(i+1)-1)x_(i+1) = 0.

Its coefficients vary with i. Replacing it by a constant-coefficient recurrence without a proved and charged change of variables changes the problem.

There is an all-size witness for a stronger mismatch. Choose lambda=-q^(N-1), set x_(N-1)=1 and solve the upper-bidiagonal eigenvector equations backwards. Every off-diagonal coefficient and every earlier diagonal difference is nonzero, so every x_i is nonzero. Yet u=0 and s=0. The periodic output sequence is sum_j x_j(q^j)^k, whose reduced rational denominator has degree N by the same noncancellation argument above. Thus a zero residual cap can coexist with N output modes. This concerns the infinite periodic sequence; it does not incorrectly assert that every N-term finite prefix has minimal LFSR length N.

### Singular forcing loses information even after the input sum

Over F_5, take N=4, q=2, lambda=1 and x=(1,3,1,0). Direct arithmetic gives

    Ex=x, u=(0,0,0,0), Fx=(0,1,4,4), y_0=0.

The zero input gives the same forcing b=0 and the same y_0=0, but a different complete transform. Therefore any attempted reduction retaining only (lambda,b,y_0) cannot distinguish these two inputs.

The extended theorem supplies exactly the missing information: lambda=-q^2, so the actual coordinate x_2=1 is retained. Its inverse-Fourier constraint is

    sum_(i=0)^3 q^(-2i)y_i = 4 = N x_2  (in F_5).

The target homogeneous trajectory h=(0,1,4,4) has both cyclic closure coefficients zero and a nonzero value under this functional. The constraint fixes its amplitude. This explicitly checks why zero forcing cannot authorize a zero answer and why the correct eigenindex matters.

The same raw four-term sequence has minimal ordinary LFSR length 2, with C(z)=1+4z+2z^2, rather than length 0 or 1. The second witness x=(1,2,2,1), lambda=2 is dense, has zero E-defect and gives Fx=(1,1,0,2); its finite raw recurrence also has length 2. These controls disprove direct parameter identification, not every conceivable reduction to classical algorithms.

## 5. Full cost and access accounting

All costs below are scoped scalar-field call counts, with every inversion paid. Exact comparisons and O(log N)-bit indexing have their stated word-work bounds. They are not timings, bit complexity, physical memory-access counts or fixed input-independent linear-circuit sizes.

Let R be the actual ratio-comparison count and d the verified residual support. The retained recurrence-route stages are:

| Stage | Count or obligation |
|---|---|
| Read fresh input and count support | O(N) work; no stored transform anchor |
| Root powers and complete E action | 6N-4 field calls |
| Cross-product majority discovery | 2R field multiplications; O(N) comparisons/indexing |
| Nonzero candidate formation | 2 field calls, including one inversion |
| All-coordinate residual formation | 2N calls for nonzero lambda; for zero lambda reuse Ex, still inspect all coordinates |
| Complete residual Fourier vector | (2N-1)d field calls; all N entries represented |
| Zero-shift target recurrence | 4N-3 calls |
| Nonzero ordinary scalar closure | 13N-5 calls, including actual y_0=sum x_i, one inverse, both closures and full output |
| Exceptional scalar closure | 18N+log_2 N-3 calls, including correct eigenindex, actual x_t, both weighted sums and one inverse; further O(N) equality/index work |
| Sparse-input route | (2N-1)m+P calls, with phase-power preparation P charged; O(N+m) bookkeeping |
| Unsupported input | O(N) decline, with the work already performed charged |

The ordinary scalar-closure branch should not be renamed the nonsingular branch: sometimes the actual y_0 already fixes a singular operator's amplitude. The exceptional branch is the case where both scalar closure coefficients vanish.

Summing the stages yields the already recorded dense one-defect totals 14N-10 for zero shift and 25N-10 for nonzero ordinary closure, when R=N-1. They include discovery, preparation, verification and complete output. The small self-authored control checks these arithmetic identities; it does not rerun or benchmark the historical implementation. For growing s, the O(N(s+1)) residual-expansion cost remains. No generic dense-input speedup follows.

For comparison, a straightforward implementation of the primary recurrence synthesis computes n discrepancies with up to L products each and polynomial updates of comparable width: O(n(L+1)) arithmetic is a direct loop bound, not a promised O(N(s+1)) Fourier evaluator. L and s are different parameters as shown above. A complete alternative through interpolation must charge creation of its samples, all recovery stages and all N output values. No model-matched speed superiority is inferred in either direction.

Finally, the [FFTW pruning discussion](https://fftw.org/pruned.html) concerns a small subset of outputs or nonzero inputs. That describes the sparse-input fallback's general setting, not the dense zero-defect witness or unknown E-shift discovery. Using it as a full-contract match would change both the input promise and output obligation.

## 6. Verification, boundaries and stopping point

The four archived texts match their recorded SHA-256 values byte-for-byte. The new standard-library mathematical control verifies FE=JF in F_5^4, both explicit witnesses, minimum finite recurrence orders, the exceptional closure functional and the two derived one-defect cost totals. It executes no inherited research program and does not repeat the earlier exhaustive correctness audit.

This closes the bounded comparison at the permitted qualified-nonmatch endpoint. The accepted extended theorem and its guardrails remain intact. Primitive-root/field construction, bit growth, numerical stability, arbitrary dense residuals, optimized runtime and historical priority remain outside the established conclusion; they are not silently converted into new obligations for this record. Reconsider the comparison if materially new primary evidence or a contradiction is supplied.
