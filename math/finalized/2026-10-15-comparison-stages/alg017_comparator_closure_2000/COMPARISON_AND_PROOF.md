# ALG-017: bounded q-calculus comparator completed

Date: 2026-10-14 UTC. Stable parent ID: **ALG-017**. Existing parent title: **Linear q-kernel spectrum preparation**.

## Decision and exact closure boundary

The specifically requested q-calculus/q-Pascal comparison is complete. This is a **matched classical foundation with a qualified nonmatch for the complete stated algorithm/cost package**. The source-bound result is not a worldwide priority conclusion and does not establish novelty by absence.

Proposed scope label: `ALG-017::Kuznetsov-v2-finite-boundary-spectrum-comparison`. This is a scoped ledger label under ALG-017, not a new canonical theorem, discovery count, or parent identity. Propose marking this scope `CLOSED_COMPLETED_SOURCE_COMPARISON` after review. Preserve parent `TO RESEARCH`, existing priority 34, and accepted proof status. Do not redispatch this same source comparison.

The requested stopping condition was to identify one primary theorem and map its exact hypotheses, formula and costs, or give a qualified nonmatch. Those requirements are met below. This closure is based on completing that obligation, not on a low promise score.

## Sources and comparison (primary-source synopsis)

Primary comparator: Alexey Kuznetsov, [arXiv:1507.02959v2](https://arxiv.org/pdf/1507.02959v2), five pages. Version history gives 27 March 2017; the served PDF title page also prints 26 November 2021, so neither is silently substituted for the other. The complete body was read through the public web PDF text. No downloaded-PDF byte hash is claimed.

Theorem 1 (p.2) factors V_q=(q^(ij)) as LDL^T with L=P_q T_q P_q^−1. Theorem 2 and equation (10) (pp.2,4) concern the same lower-triangular kernel T_q=ΣS^j/(q;q)_j, with nilpotent shift S. Equation (5) (p.3) supplies the q-exponential coefficients. Its infinite-series domain is |q|<1; the finite matrix theorems allow complex q having no smaller forbidden root order. Thus primitive Nth roots are allowed for size N. The five-page body does not state the supplied-2Nth-root, two-affine-orbit spectrum algorithm or its operation ledger. Attribution to the classical coefficient/factorization mechanism is exact; attribution of the entire computational package to this paper would exceed its statements.

## Pinned project source and current row

The row-specific source is `PINNED_PROJECT_SOURCE.md`, SHA-256 `9c80e17183dc11eb2f1c23d1ad7b8025cc58b564e23467cf1ad128f5f6713eaa` (8,212 bytes). It already explicitly credits Kuznetsov. This review resolves the remaining exact comparison rather than discovering that citation anew.

The closure audit and current local canonical snapshot bind ALG-017 to Catalogue row 128, novelty-register row 101 and Research overview row 176. Earlier row references 118 and 47 are historical and must not be reused as current addresses. Exact cell preimages and their hashes are in `PROPOSED_UPDATE.json`; any later live application must re-resolve the stable ID and recheck preimages.

The existing signed-bank family label is not a mathematical equivalence. This packet does not alter that label, the parent's score, or any other theorem.

## Independent algebraic reconstruction

These arguments are reconstructed from the finite coefficients, rather than from convergence of an infinite series at a root of unity.

Let F be a field and n≥2. Suppose 1−q^j is nonzero for 1≤j<n. Set t_0=1, t_j=1/∏_(a=1)^j(1−q^a), and H_n(z)=Σ_(j=0)^(n−1)t_j z^j. Then

H_n(qz)=(1−z)H_n(z)+t_(n−1)z^n.                         (A)

Proof: the constant coefficients agree. For 1≤j<n, the coefficient of H_n(qz)−(1−z)H_n(z) is (q^j−1)t_j+t_(j−1)=0. Its sole remaining coefficient is t_(n−1) at degree n. This is an equality of polynomials, with no analytic continuation assumption.

If q has exact order n and char(F) does not divide n, the roots q^0,...,q^(n−1) are distinct. Factoring (X^n−1)/(X−1) and evaluating at X=1 gives ∏_(j=1)^(n−1)(1−q^j)=n. Thus t_(n−1)=1/n, and (A) becomes exactly the pinned finite-boundary identity.

The loss of the boundary in the nilpotent matrix setting is precise: substituting S with S^n=0 kills t_(n−1)S^n. It is invalid to take that truncated identity and then substitute a nonzero scalar z. There is no F-algebra homomorphism from F[z]/(z^n) to F taking z to a nonzero a, since it would require a^n=0. The simplest direct control is z=1: H_n(q)=1/n, not zero. This explains why using the classical kernel coefficients is legitimate but dropping the boundary during spectrum evaluation is not.

### General nonzero q-orbit

For a≠0, set y_r=H_n(aq^r). Equation (A) gives

y_(r+1)=(1−aq^r)y_r+a^n/n.

The n-step affine map has slope ∏_(r=0)^(n−1)(1−aq^r)=1−a^n. Let b be its intercept, obtained by iterating from zero. Since the intended values form a cycle,

y_0=(1−a^n)y_0+b, hence y_0=b/a^n.

The denominator is nonzero. This gives a unique seed and then every orbit value using O(n) field operations, with the orbit constant/inverse and every output charged. The supplied root assumption must still be enforced; this is not a root-construction algorithm.

### Two-orbit specialization

For the accepted dyadic n=N and supplied eta of exact order 2N, put q=eta^2. Since char(F) does not divide 2N, eta^N=−1. The spectrum v_k=H_N(eta^k) obeys

v_(k+2)=(1−eta^k)v_k+(−1)^k/N.

The even orbit has a zero multiplier at k=0, so v_2=1/N; N−1 further steps fill the remaining even slots. The odd orbit's full slope is 1−eta^N=2. If b is its zero-start intercept, its unique cyclic seed is −b. Another N−1 steps materialize all remaining odd slots. Every slot is covered, and this construction contains no transformation of arbitrary fresh input.

### Exact factorization mapping

Let f_i=(q;q)_i and P=diag(f_i). In the comparator's factorization D_ii=(−1)^i q^(i(i−1)/2)f_i. Consequently

V_q=P T_q D' T_q^T P, where D'_ii=(−1)^i q^(i(i−1)/2)/f_i.

This is the same diagonal/Toeplitz/transpose structure as the pinned source. Because all denominators here are finite and invertible, its polynomial/rational identities can be checked algebraically in the permitted fields; the comparator's stated complex domain must not itself be relabeled as a finite-field implementation theorem.

## Paid cost mapping

For N=2^L≥2, compare the exact same 2N-root grid and unoptimized radix-two butterfly convention, counting multiplication even by 0 or 1.

Shared preparation: 2N−1 field multiplications for all powers of eta; one inversion of 2 and L+1 multiplications for 1/N and 1/(2N). Root discovery and representation are not included in either ledger. Root-validation controls in the checker are audit overhead, not silently charged as zero-cost production validation.

Orbit preparation caches all 2N affine multipliers 1−eta^k. Even propagation uses N−1 steps, odd zero-start composition N steps, and odd replay N−1 steps. This gives exactly:

- Multiplications: 5N+L−2
- Additions: N−1
- Subtractions: 4N−1
- Negations: 1
- Constant inversions: 1
- Total counted field operations: 10N+L−2

Caching the affine multipliers is part of this exact ledger. Recomputing them during replay changes the subtraction count; it is not the same instruction schedule.

For the comparison baseline, construct t_(N−1)=1/N and t_(j−1)=(1−q^j)t_j, zero-pad to 2N, and run the ordinary FFT. Its counts are:

- Multiplications: NL+4N+L−1
- Additions: N(L+1)
- Subtractions: NL+2N−1
- Constant inversions: 1
- Total: 3NL+7N+L−1

The cold saving in this convention is exactly 3N(L−1)+1, positive even at N=2. This is a count comparison with a specified implementation, not a minimum-complexity or elapsed-speed claim.

A fresh input still pays one forward and one inverse length-2N FFT, all 2N pointwise products and all 2N normalization multiplications. The exact counts are 2NL+6N multiplications and 2N(L+1) each additions/subtractions. Padding, traversal, output writes and root/table indexing require O(N log N) logical word work; storage is O(N). This is not a Python interpreter/RSS bound. The four padded transforms in the complete factorized Fourier application remain; no cancellation across padding, truncation, reversal or the middle nonconstant diagonal is asserted.

## Fresh independent controls

Only `check_fresh.py`, written for this review, was executed. It has standard-library imports and no historical-code dependencies. The source's saved programs and saved suites were not run. The mathematical all-size proof is the argument above; finite tests are implementation controls only.

The final run passed:

- 70 dyadic root/length/field configurations: N through 256, across F_97, F_257 and F_65537, with multiple primitive roots
- 6,328 spectrum coordinates against independently generated finite coefficients and Horner evaluation
- The same 6,328 coordinates against a newly written radix-two FFT baseline
- 6,328 negative controls showing boundary deletion is wrong at every tested nonzero grid point
- 210 full triangular-convolution output vectors, including both endpoint basis vectors and dense inputs
- 16,834 general-orbit values, including 14 additional nondyadic configurations
- 4,056 LDL factorization entries
- Four rejection controls distinguishing an Nth root from the required 2Nth root
- Exact orbit-preparation, baseline-preparation, and full online arithmetic counts in every dyadic case

During checker construction, an initial schedule recomputed odd affine multipliers instead of caching them, so its subtraction-count assertion failed. The final checker explicitly caches all 2N multipliers, matching the declared ledger. This was an audit-program schedule correction, not a correction to the accepted source theorem. All final outputs come from the corrected fresh program.

## Remaining gates and proposed update

Close only the named comparator scope after review. Broader historical priority remains unproved. A cheaper complete application graph, a numerically stable bounded-word recurrence, root/field discovery, bit complexity, physical memory/time and production use remain separate obligations; none is automatically selected or claimed finished here.

Put this completed comparison ahead of the old source-mismatch action in Catalogue AE128, novelty O101/Y101, and overview C176/P176. Add the primary URL to the source field while preserving old entries as history. Update the scoped-completion explanation, not parent status or priority. The proposal preserves exact preimages and appends rather than deletes historical text. There were no external writes.
