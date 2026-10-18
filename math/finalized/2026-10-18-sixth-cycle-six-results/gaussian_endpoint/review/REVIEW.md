# ALG-036 critical endpoint: independent scoped acceptance

Review completed: 2026-10-18, 21:30 UTC. Owner: ALG-036, priority 34.

## Verdict

**ACCEPTED at the stated constant-fraction endpoint scope. No mathematical correction is required.**

For fixed C>0 and 0<delta<=1, the frozen candidate proves that every independently seeded, measurable transcript-only adaptive complex-linear measurement scheme with terminal complex rank deficit at least delta N satisfies

    Pr(||Xhat-U_N x||_infinity <= C N^(-1/2)||x||_2)
      <= exp[-(delta/2) exp(-8 C^2/delta) N]
         + exp[-(3-log 4)N],

where x~CN(0,I_N), U_N is any fixed unitary, and the decoder receives no uncharged input information. The right side can be capped at one. This is an upper bound on **success**, equivalently a lower bound of one minus that quantity on failure. It is uniform in residual orientation, decoder translation, independent seed law, transcript-only query policy, and allowed stopping rule. Consequently success tends to zero exponentially for fixed C and delta.

This settles the exact selected ALG-036 gate and its fixed-s, M=Theta(log N) block-local application. It does not close the broader owner record, establish an unrestricted Fourier arithmetic lower bound, settle thin deficits, or make a novelty/priority claim.

## Frozen material and source integrity

The reviewed candidate is `/workspace/shared/alg036_endpoint_20261018_2053`. Its REPORT.md SHA-256 is `545d90eb4890515e4eae922a03f2563e7cd63ab6fe3ffce98a529fb7864cd84b`; its MANIFEST.sha256 SHA-256 is `6cc0cca6da9c9dcacef1f30bda63c55cf2853753a12096c5d80407238c4a3cf5`.

I read the complete candidate report, verdict, README, source manifest, its fresh checker and recorded results, and all three copied controlling text sources. All nine payload entries in the candidate manifest verify. Every copied controlling source is byte-identical to the original local source identified by SOURCE_MANIFEST.json; all declared lengths, SHA-256 values, and supplied expected hashes verify. The controlling task is PLAN.md section 1; the earlier Gaussian audit fixes the information model and retained counterexample, and the integrated acceptance records the previously unresolved endpoint. Other task selections in PLAN.md are outside this review.

The original candidate is unchanged. `CANDIDATE_MANIFEST.sha256` in this review is a byte copy of its seal. This independent packet records acceptance without rewriting the candidate's historically accurate PENDING review marker.

## Independent proof audit

### 1. Disk estimate and arbitrary translations

For a proper complex Gaussian of scalar variance v, the centered radius-r disk has probability 1-exp(-r^2/v). A translated disk has no larger probability: at each density level, both the Gaussian superlevel set and the centered test disk are concentric disks, whose intersection area is the maximum possible minimum of the two disk areas. Layer-cake integration proves the claimed inequality for every translation. The argument includes radius zero and arbitrary conditional means. No coordinate independence or zero conditional mean is being assumed later.

### 2. Uniform cube estimate

At residual projector rank q, trace P=q and nonnegative diagonal entries imply a coordinate variance v>=q/N. Choosing the maximum diagonal with the stated tie rule is measurable and depends only on the projector. After conditioning on that coordinate, the covariance is

    P' = P - (P e)(P e)*/v.

The removed vector P e/sqrt(v) is a unit vector in the range of P. Thus P' is exactly a rank-(q-1) orthogonal projector. Previously exposed coordinates have zero residual variance, so the positive-variance pivot cannot repeat a coordinate. This proves that the process continues for d steps even for singular ambient covariance.

Conditional coordinate means depend on previous values, but the disk estimate is uniform in those means. For each selected coordinate the conditional success probability is at most 1-exp(-N r^2/q). The tower property can be applied to the intersection of earlier disk events because that intersection is measurable in the already revealed coordinates. This proves the product bound without an unjustified independence step.

Among the first ceil(d/2) pivots, q>=d/2. Discarding the remaining factors and using 1-u<=exp(-u) gives

    Pr(max_j |Z_j-b_j|<=r)
      <= exp[-(d/2) exp(-2N r^2/d)].

Both d/2 and exp(-2N r^2/d) increase when d increases. Hence d>=delta N yields exp[-(delta N/2)exp(-2r^2/delta)]. The inequality directions and the factor two are correct, including odd d and d=1. Rank-one balanced projectors provide an independently checked sharp control for the stronger product formula. No separated-coordinate theorem or unproved Gaussian comparison result is needed.

The artificial coordinate reveals are used only to bound a posterior Gaussian probability. They do not become extra information available to the decoder.

### 3. Transcript-dependent measurements and stopping

The posterior induction is valid. Given F_(t-1), the next query vector is already fixed because it is a measurable function of the independent seed and previous responses. For positive innovation variance v=a*Pa, the proper Gaussian decomposition yields the stated mean update and P-Paa*P/v. Its range is exactly the previous residual range intersected with ker(a*). A zero-variance query is already determined and adds no information. The adaptively chosen row coefficients therefore reveal no extra information beyond the transcript that selected them.

This is why the theorem permits response-dependent coefficients, but not coefficients chosen using an uncharged full-input read. Conditioning on the latter could invalidate Gaussianity; such a model is explicitly excluded.

For an almost-sure finite stopping time, {T=t} belongs to F_t. The Gaussian conditional-kernel identity can be restricted to each such event and summed over t, yielding the stated conditional law on F_T. This does not condition the posterior on an additional, unobserved event. There is no hidden deterministic bound on query count. Independent decoder coins can be included in R.

The optional countably infinite extension is also valid. At most N positive-variance rank reductions occur on any path, so the decreasing finite-dimensional residual subspaces, and hence their projectors, eventually stabilize pathwise. Meanwhile the conditional means converge as L2 martingales. The characteristic-function identity has the correct proper-complex factor 1/4; martingale convergence on a countable dense set, followed by continuity, identifies the limiting conditional Gaussian. A countable row family spans a finite-dimensional subspace and causes no missing closure issue.

After conditioning on the terminal transcript, unitary conjugation preserves the projector and its rank. The decoder difference Xhat-U_N m is a fixed but arbitrary translation under that conditional law. The cube lemma is uniform over both quantities and can therefore be averaged over the transcript.

### 4. Norm event and constants

The proof uses the inclusion

    success and ||x||_2<=t sqrt(N)
      implies ||Xhat-U_N x||_infinity<=Ct.

It does not condition a Gaussian on the norm cutoff. The fixed-radius cube event is first bounded using the measurement posterior, then the unconditional norm-tail probability is added. Since |x_j|^2 are independent mean-one exponentials, Chernoff optimization at lambda=1-t^(-2) yields exp[-N(t^2-1-log(t^2))]. At t=2 the two displayed exponents are exactly (delta/2)exp(-8C^2/delta) and 3-log 4. Both rates are positive for the fixed allowed parameters. An exceptional rank-deficit event of probability eta_N adds eta_N; an expected deficit alone does not suffice.

### 5. Every-fixed-input consequence and architecture

For one fixed admissible scheme, Fubini gives E_x p_N(x)<=epsilon_N, with p_N(x)=Pr_R(success on x). An every-fixed-input lower promise p_N(x)>=1-rho_N would imply 1-rho_N<=epsilon_N. Thus the conclusion does not choose a bad input after observing the seed. A deterministic input with p_N(x)<=epsilon_N exists, and Markov gives Pr_x(p_N(x)>eta)<=epsilon_N/eta. The null sets allowed in the Gaussian pathwise deficit hypothesis do not invalidate this implication.

Under the retained fixed-block local information model, d>=B(M-s), B>=floor(N/M)-2. For N>=6M the latter is at least N/(2M). If s/M<=1-gamma, the choice delta=gamma/2 is valid, giving the stated exponent (gamma/4)exp(-16C^2/gamma). For fixed s and M=Theta(log N), delta=1/4 is eventually valid; indeed d/N tends to one under the stated conservative block count. The stronger asymptotic comment and its factors are correct.

## Independent controls and inspected replay

The sibling's newly authored checker was read in full before execution. It imports only ordinary numerical/symbolic libraries, does not load historical research programs, and makes no network requests. Its execution reproduced the frozen controls/RESULTS.json **byte-for-byte**, including 919 exact pivots, 150 Schur-complement comparisons, seven adaptive paths and all reported diagnostics. The replay is saved as controls/AUTHOR_REPLAY.json.

My separately authored controls/independent_controls.py passed. It uses a different exact subspace construction and a different scalar-disk probability calculation:

- 21 rational complex Householder-generated projectors, with 56 exact pivots and 56 independent principal-determinant conditional-variance checks
- Six adaptive paths with continuously transcript-dependent complex coefficients, two stopping paths, both direction branches, ten positive-variance queries and four redundant queries; terminal posterior means/covariances checked against independent whole-transcript least-norm formulas
- 60 scalar-disk Bessel-quadrature checks, avoiding the author's noncentral chi-square evaluator; maximum numerical excess 1.12e-16, within the explicit 5e-12 check tolerance
- 96 bound chains at 80-digit precision, including radius zero and the sharp balanced rank-one product control
- 1,425 exact block-count checks, all nine sealed payload hashes, and all three original source byte comparisons

These controls check algebra, constants, branch handling and transcription. Neither the finite tests nor numerical quadrature substitute for the all-N proof audited above. Recorded versions, seeds and script hashes are in controls/INDEPENDENT_RESULTS.json.

## Retained boundaries and terminal acceptance

The accepted alpha<1/2 conditional positive approximation theorem remains unchanged. The random-one-coordinate-omission counterexample remains valid and outside a fixed positive rank-fraction assumption. In particular its alpha=1/2 failure upper bound 1/(C^2 N) is consistent with this result.

No endpoint theorem for d asymptotic to N/log N, arbitrary nonzero deficit, input-dependent uncharged side information, full-input algorithms, Fourier arithmetic complexity, implementation performance, novelty or priority is accepted here. No wider ALG-036 owner closure follows. No research queue, external repository, source packet, or other external state was changed by this review. No historical research program was executed.

**Final disposition: accept the constant-fraction alpha=1/2 endpoint and its stated adaptive/stopping and block-local consequences. There is no unresolved lemma within this selected gate.**
