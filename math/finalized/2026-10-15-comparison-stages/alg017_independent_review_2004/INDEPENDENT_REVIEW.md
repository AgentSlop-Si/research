# Independent acceptance of the bounded ALG-017 comparator

Date: 14 October 2026 UTC. Decision: **ACCEPT_COMPLETED_SOURCE_COMPARISON**.

Accepted scope: **ALG-017::Kuznetsov-v2-finite-boundary-spectrum-comparison**. This completes the one-source q-calculus/q-Pascal comparison requested by the existing row. It does not close the canonical ALG-017 parent, change its priority 34, establish worldwide priority, or add a discovery. The parent remains TO RESEARCH.

## Exact packet and evidence boundary

I read the complete comparison, pinned project source and fresh checker as text. All nine entries in the author's MANIFEST.json match their declared byte counts and SHA-256 digests. The comparison SHA-256 is 0ed2694eeaa7ebb077d17b7e04df07427d71ec3df8df7b198eafa2fc2a02af97. The pinned project manuscript is 9c80e17183dc11eb2f1c23d1ad7b8025cc58b564e23467cf1ad128f5f6713eaa.

Only my newly written independent_controls.py was executed for this review. I did not execute, import, compile or reuse the candidate checker or historical project programs. The candidate's recorded test results were inspected and their arithmetic totals reconciled; my separate controls have their own smaller, explicitly stated coverage.

## Primary-source comparison

I independently reopened the complete five-page [Kuznetsov v2 paper](https://arxiv.org/pdf/1507.02959v2). Its finite matrix domain excludes smaller forbidden root orders. Theorem 1, page 2, supplies the diagonal/Toeplitz LDL factorization. Equation (5), page 3, gives the classical coefficients; equation (10), page 4, uses the nilpotent shift. The infinite-series restrictions must not be applied indiscriminately to the finite matrix statements. The paper does not present the complete supplied-2N-root, two-orbit spectrum algorithm and its cost ledger. This is a qualified nonmatch within this selected source, not a literature-wide absence result.

Access was complete PDF text extraction. PDF screenshots failed with cache-miss errors; no local PDF digest or visual-facsimile inspection is claimed. The arXiv version line says 27 March 2017 and the title page says 26 November 2021; the candidate correctly distinguishes them.

The project manuscript already cited Kuznetsov. The completed work makes the exact hypothesis/formula/cost comparison explicit rather than claiming a newly discovered citation.

## All-size proof audit

### Finite boundary

For t_j = 1 / product_(a=1)^j(1-q^a), let H_n(z) = sum_(j=0)^(n-1)t_j z^j. In H_n(qz) - (1-z)H_n(z), every coefficient of degree j from 1 to n-1 is (q^j-1)t_j+t_(j-1)=0. The degree-n coefficient is t_(n-1), and the constants cancel. Therefore the exact polynomial identity is

H_n(qz) = (1-z)H_n(z) + t_(n-1) z^n.

For a primitive n-th root with the stated nonzero characteristic guard, evaluating (X^n-1)/(X-1) at X=1 gives the finite product n, hence t_(n-1)=1/n. This uses a finite polynomial identity, not convergence at roots of unity.

The term vanishes at a nilpotent shift S with S^n=0. It cannot be discarded at a nonzero scalar: the quotient relation z^n=0 has no field-valued homomorphism taking z to a nonzero element. In particular H_n(q)=1/n. This is a genuine boundary distinction, not an implementation detail.

### General orbit and two-orbit specialization

On z=a q^r with a nonzero, the forcing is a^n/n. The full affine orbit has slope product_r(1-aq^r)=1-a^n. If its zero-start intercept is b, the cyclic seed is uniquely b/a^n. The denominator is nonzero. The actual polynomial values obey the same recurrence and cycle, so uniqueness proves the reconstructed values are those polynomial values.

For supplied eta of exact order 2N, q=eta^2 has order N and eta^N=-1 under the stated characteristic assumption. The even orbit resets at its zero multiplier: v_2=1/N. Its next N-1 steps cover every other even slot exactly once. The odd full-orbit slope is 2, so its fixed seed is -b; N-1 replay steps cover the remaining odd slots. This proves all 2N values for every permitted dyadic N, not just the tested sizes. Root discovery and construction from a merely supplied N-th root remain excluded.

### Factorization and full application

Writing f_i=(q;q)_i and P=diag(f_i), the comparator's L=P T P^-1 and diagonal D give V=P T D' T^transpose P with D'_ii=(-1)^i q^(i(i-1)/2)/f_i. This is the pinned diagonal/Toeplitz structure. Its finite rational identities admit algebraic specialization when their denominators remain invertible; the paper's stated complex domain is not silently relabeled as a finite-field implementation theorem.

A padded length-2N convolution is sufficient because the product degree is at most 2N-2. Returning its first N coordinates gives the triangular action. Fresh input still pays its forward and inverse transforms. Applying both triangular factors leaves four length-2N transforms and three N-entry diagonal passes; padding, truncation, reversal and the middle diagonal do not justify cancelling adjacent transforms.

## Paid arithmetic audit

The field-operation convention counts multiplication by zero or one. Root/table indexing and logical memory operations are distinct from these scalar counts. One inversion supplies 1/2; L+1 multiplications supply 1/N and 1/(2N). The shared power chain costs 2N-1 multiplications.

For the orbit implementation, caching all 2N multipliers costs 2N subtractions. The even, odd composition and odd replay phases have N-1, N and N-1 updates. Thus the exact counts are:

- Multiplications: 5N+L-2
- Additions: N-1
- Subtractions: 4N-1
- Negations: 1
- Constant inversions: 1
- Total: 10N+L-2

The cached schedule is essential to the stated subtraction count. The author's disclosed early audit-script correction is consistent with the final inspected code; it changes the implementation schedule, not the finite-boundary theorem.

For the ordinary baseline, the backward coefficient recurrence costs N-1 multiplications and subtractions. A length-2N radix-two transform has N(L+1) butterflies. Adding shared preparation yields exactly NL+4N+L-1 multiplications, N(L+1) additions, NL+2N-1 subtractions and one inversion. Total: 3NL+7N+L-1. The difference is 3N(L-1)+1, including the positive N=2 edge case.

For one online triangular action, two padded transforms, 2N pointwise multiplications and 2N normalizations give 2NL+6N multiplications and 2N(L+1) each additions/subtractions. Twice this plus three N-entry diagonal passes gives the source's 4NL+15N multiplication count for the complete factorized application. These are implementation-specific field counts; no minimum-complexity, elapsed-speed, bit-cost or physical-memory claim follows.

The candidate's bit-reversal loop uses O(N log N) integer work per transform, which is compatible with its stated online logical-work bound. Storage is O(N) logical field elements. The field-operation ledger neither charges root validation as free nor claims the supplied-root contract constructs or authenticates roots.

## Independent controls

My fresh program passed:

- 26 dyadic configurations over F_5, F_17, F_97 and F_193, including N=2 and both root orientations
- 432 spectrum-bin comparisons against direct coefficient evaluation, with nonzero boundary checks
- Complete polynomial-identity checks at every field element for those configurations
- 444 nonzero general-orbit cases, totaling 5,088 values, including nondyadic orders
- 512 factorization entries
- 26 controls rejecting substitution of the N-th root for the required 2N-th root
- Instrumented orbit counts and independently decomposed baseline counts in every dyadic configuration

The recorded candidate aggregates also reconcile: 70 configurations give 6,328 bins, 210 complete online vectors and 4,056 checked factorization entries. I inspected its independent Horner/FFT comparison and online implementation but did not rerun that code. My independent controls are not a substitute for the all-size proof above and are not a production or numerical-stability audit.

## Update and remaining gates

All 11 proposed plain-text preimages match the fresh 20:00 UTC full native workbook snapshot. Each new text preserves its earlier value verbatim. Stable IDs resolve to Catalogue row 128, novelty row 101 and overview row 176. The fresh parent status is TO RESEARCH and score is 34. There are no proposed canonical-row closures or numeric changes.

The proposed texts still say independent review pending. Keep that candidate packet immutable. Before publication, prepare a separate dated acceptance addendum using this review and a verified immutable source link, then recheck live cell preimages and preserve native rich links, notes and formats. The plain-text proposal is not itself a safe native-cell update request.

Scientific review of the named comparison is complete. Remaining substantive gates are broader historical priority, a cheaper complete application graph, numerical stability and bounded-word/bit contracts, root/field discovery, physical performance and production readiness. These different tasks do not keep this exact one-source comparison open. The current GitHub approval blocker and pending 48-cell publication batch remain untouched. No external state was changed.
