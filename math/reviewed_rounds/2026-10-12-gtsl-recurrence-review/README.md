# GTSL recurrence review and corrected endpoint theorem

12 October 2026 UTC.

The fixed-saving recurrence theorem is valid with explicit uniform and nonnegative-cost hypotheses. The proposed growing tensor-union compiler remains UNPROVED. Convergence of rho(w) to one half alone does not imply O(N log log N); the original manuscript contains that rate error, preserved here as source history.

## Read the results

- [Corrected conditional theorem](CORRECTED_THEOREM.md) states fixed-factor, quantitative-rate, rounded-child and zero-overhead conditions.
- [Counterexamples and verifier limitation](COUNTEREXAMPLES.md) give the harmonic, quadratic and superpolynomial-in-depth half-limit failures, both pointwise-gap failures, and the one-vector blind spot.
- [Complete scoped review derivative](gtsl-scoped-review.md) retains the full mathematical review, compiler obligations and source-edit recommendations.
- [Complete independent rate audit derivative](gtsl-independent-rate-audit.md) retains the rate proofs, precise critical threshold and original verifier scope.
- [Original supplied manuscript](originals/GTSL_Fourier_Theory_2026-10-12.md) is preserved byte for byte, including the superseded inference in section 5 and abbreviated pointwise thresholds in section 16. It is a candidate, not an accepted fast-transform algorithm.

## Accepted mathematical scope

For N=2^w and f(w)=C(2^w)/2^w, assume finite nonnegative bases, a fixed nonnegative overhead kappa, and the uniformly valid recurrence

    f(w) <= rho(w) [f(floor(w/2)) + f(ceil(w/2))] + kappa.

An eventual fixed bound rho(w)<=r yields O(N(log N)^(log_2(2r))) for 1/2<r<1, O(N log log N) for r=1/2, and O(N) for 0<=r<1/2. Pointwise strict inequalities alone do not replace the fixed margins.

A uniform polynomial-in-w approach rho(w)<=r_*+c/w^gamma, with fixed c>=0 and gamma>0, preserves those conclusions at r_*, including O(N log log N) at r_*=1/2. A half-limit alone gives only the weaker statement C(N)=O_eta(N(log N)^eta) for every fixed eta>0. The reports also give a sharp inverse-depth rate threshold and an exact product-and-suffix-sum criterion.

These are conditional recurrence upper bounds. The counterexamples concern what the recurrence permits, not Fourier complexity lower bounds. The domain is dyadic transform lengths; arbitrary transform lengths need a separate reduction.

## Preservation and verification

The original manuscript is unchanged. The two review reports are labeled publication derivatives: private source-location metadata is removed, and reproduction wording is adjusted to the code-free contents. Mathematical proofs and counterexamples are preserved. Source hashes and derivative relationships are recorded in [FILE_MANIFEST.json](FILE_MANIFEST.json) and [PUBLIC_PROVENANCE.json](PUBLIC_PROVENANCE.json).

[ORIGINAL_CONTROL_RESULTS.json](ORIGINAL_CONTROL_RESULTS.json) preserves the independent audit's historical exact-control output. It does not report a new compiler test. [MINIMAL_VERIFICATION.json](MINIMAL_VERIFICATION.json) records fresh publication-preparation checks, and [VERIFICATION.md](VERIFICATION.md) explains independent reproduction and limitations. Executable code, executable archives and full third-party papers are not included.

## Open algorithmic work

The source does not provide the growing union compiler, a scalable exact all-input circuit certificate, a scale-uniform savings rate, or the fully charged coefficient/preparation/routing construction needed to instantiate the theorem. Existing finite structures and classical identities do not fill that gap. No faster Fourier algorithm, practical FFT speedup, Fourier lower bound, or historical novelty is established. The original manuscript's external comparator and project-phase claims are outside this review's verified scope.

## Later bounded implementation reviews

Read the [N16 ideal scan and named CSM1 compiler reviews](../2026-10-12-compiler-scan-qualification/README.md), with their exact source and implementation-model limits. These separate finite results do not instantiate the GTSL compiler.
