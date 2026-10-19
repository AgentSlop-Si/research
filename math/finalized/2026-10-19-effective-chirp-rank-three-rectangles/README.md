# Effective positive chirp cutoff and two-prime rank-three rectangles

19 October 2026. Two independently accepted scoped results, with their frozen proofs, independent reviews, check programs and saved results. Neither owner is closed. No historical-novelty, general Fourier-algorithm lower-bound, or performance claim is made.

## Effective positive-epsilon chirp cutoff

Conditional on the two preserved accepted certificates, the explicit bound is

    N0 = 2^(2^534).

For every odd N=5m with gcd(m,5)=1, N congruent to 1 modulo 4 and N>=N0, the specified forced chirp feedback B_N, for every primitive complex additive character, cannot be a sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary diagonal endpoint masks, legal denominators and fixed coordinates. Positive epsilon means G_N^2=+N; both real signs G_N=+sqrt(N) and G_N=-sqrt(N) are included.

Read the [proof](chirp/candidate/EFFECTIVE_POSITIVE_CHIRP_CUTOFF.md) and [independent acceptance](chirp/review/INDEPENDENT_REVIEW.md). The argument makes the former finite-exception conclusion effective through an explicit Nullstellensatz degree bound, a bounded rank-minor identity, coefficient heights, a four-embedding norm and an integer root bound. Kollár's Sharp Effective Nullstellensatz, Theorem 1.5 and Corollary 1.9, is credited exactly; the degree-two exception is handled by cubing the generators. The two accepted certificates remain dependencies, rather than being silently re-proved by the fresh controls. No expanded eliminant or actual exception list is computed.

The earlier positive square family N=5q^2 for positive odd q coprime to 5 with q congruent to 1 modulo 241 remains valid, including below N0. Crucially, the complete retained owner history also records an already accepted negative-epsilon family N=4820k-5, k>=1, k not congruent to 4 modulo 5, starting at 4815, and non-effective finite-exception exclusions for both signs. These accepted results are preserved. The negative-epsilon branch is outside the new effective-cutoff theorem; its existing accepted results are not reopened. Its effective cutoff and actual exceptional sets remain unresolved. The negative-epsilon proof bodies were not recovered in this packaging pass; their exact historical proof/review/archive digests and this evidence limit are recorded in [OWNER_DISPOSITIONS.json](OWNER_DISPOSITIONS.json).

Unmatched endpoint permutations, other feedback targets, further summands and products remain outside this new theorem. The retained Q11/SP11/H01-H05 results and dimension-five upper identities remain intact; base-field-only three-term and growing-dimensional full-B upper-construction gaps are not closed. Numerical stability, production execution and exact additive-length priority remain unresolved.

## Uniform rank-three side bound and the 2873 optimum

For distinct primes p,q>=5, every rectangle of the complex cyclic Fourier matrix F_(p^2 q) of rank at most three satisfies

    min(a,b) <= max(6p,3q).

Either prime ordering is allowed. At N=2873=13^2*17, the bound gives min(a,b)<=78 and actual rank-three endpoint-cost density at least 29/442. The exact disjoint-rectangle incidence optimum is 534378. Every optimizer consists of exactly 2873 rank-one full mutually annihilating coset-product tiles, each with unordered side sizes {17,169}; a common orientation is not required. The valid, not claimed sharp, area penalty is

    cost >= 534378 + (5/5746) A_(rank>=2).

Read the [proof](rectangle/candidate/REPORT.md), [independent review](rectangle/review/REVIEW.md) and [verdict](rectangle/review/VERDICT.json).

### Correction to the old gate

Integer stable rank alone already closes this particular target. The unrestricted rank-three scalar relaxation has exact minimum 62/957 at the unique unordered scalar shape {87,99}; its excess above 186/2873 is 124/2749461. No actual Fourier rectangle at that scalar shape is asserted. The new uniform structural theorem is a separate advance and yields the stronger target penalty. It is not necessary merely to obtain the target optimum.

The dated older statement that 2873 was the next residual of the precisely retained sufficient-domain union is preserved in the copied prior sources. Its additional suggestion that new Fourier-specific structure was necessary was too strong and is explicitly corrected here and in both new reports. No historical file has been silently rewritten.

Extending the precisely retained union by the isolated target 2873 only gives coverage of every N from 2 through 3756. The next residual is 3757=13*17^2, at rank three. This is a bounded statement about the retained union, not a claim that all p^2 q tiling optima now follow from the new side theorem. At 3757 the scalar shape (102,110) demonstrates insufficiency of the available bound; it is not a Fourier counterexample.

The objective throughout is sum r_t(a_t+b_t), with actual complex ranks and arbitrary nonempty Cartesian subsets partitioning all entries, without overlap, cancellation or sharing. Root/coefficient preparation, storage and I/O are separate; the inherited possible N extra additions in literal zero-initialized accumulation remain charged separately. Complex and characteristic-zero results are not transferred to finite fields. Prior rank-one, balanced-divisor, dominant-prime, rank-two, prime-cube and mixed-prime results and their equality/penalty qualifications remain valid. Attribution to Delvaux–Van Barel, Alman–Guan–Padaki and the distinct Tadej Fourier-family comparison is preserved in [HISTORY_AND_SCOPE.md](HISTORY_AND_SCOPE.md).

## Acceptance, integrity and publication boundary

[FINAL_ACCEPTANCE.json](FINAL_ACCEPTANCE.json) binds the two new independent acceptances to their exact proof bytes. Historical provisional labels and open-gate wording inside frozen sources remain unchanged; the final reviews and this current disposition govern their present scoped acceptance. M-CHIRP-LOWER remains TO RESEARCH, priority 34. M-RECTANGLE-TILING remains TO RESEARCH, priority 42.

[SEAL.json](SEAL.json) binds the manifest, exact publication allowlist, acceptance and owner dispositions. [COPY_BINDINGS.json](COPY_BINDINGS.json) records every exact source copy. [OMISSIONS.json](OMISSIONS.json) declares the nonrecursive historical dependency boundary and duplicate containers. [PROJECTION_DISCLOSURE.json](PROJECTION_DISCLOSURE.json) records that no scientific source text was privacy-projected or edited. Full papers and private native snapshots are excluded.

Run the documentary verifier from any directory:

    python3 -B /path/to/this/packet/verify_package.py

It checks bytes, file-set equality, pinned acceptance, scope safeguards and bounded privacy patterns. It executes no scientific checker. Original local paths and checker commands are preserved as provenance; no relocated scientific replay is claimed. Saved test results remain the authors' and reviewers' recorded executions, not fresh packaging runs.

Only the exact allowlist is intended for publication at math/finalized/2026-10-19-effective-chirp-rank-three-rectangles. This isolated local packet asserts no repository commit, native-table update or remote verification and leaves prior packets unchanged.
