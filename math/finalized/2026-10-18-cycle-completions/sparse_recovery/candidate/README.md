# New restricted finite recovery gate

This packet advances the accepted sparse-original supplier and nonconstant
BUCKETS result to a **support-blind approximate recovery decoder**. It is a new
candidate with author checks, awaiting independent review. All work is local.

At the accepted N=M=2^28, s<=16, singleton-block parameters, the decoder reads
only finite BUCKETS values and source-independent window scalars. It uses 29
full calls, decodes unknown indices with finite phase signs, and returns sparse
coefficients for R(x)/alpha. For a uniform independent odd multiplier the proved
joint success/error probability is at least 2033/2048. Every coefficient of
magnitude at least 2^-399 is located; each returned coefficient has complex
error <=4*2^-464 and the normalized vector has l2 error <=9*2^-400.

The actual 16-mode nonconstant run produced 14 correct frequencies from 36
candidate bins. Its two omitted coefficients are below the threshold. All
3,801,088 bucket coordinates were produced and read. The full semantic replay
is separately executed and charged; see REPLAY_RESULTS.json for its outcome.
The fixed demonstration tape is not a claim of actual random sampling.

PROOF.md also gives an exact two-input indistinguishability counterexample:
the current 464-bit value-error interface cannot guarantee exact support for
all allowed 1024-bit coefficient inputs. Approximate recovery and minimum-
amplitude exact-location guarantees must remain distinct.

Files:

- PROOF.md: recovery theorem, probability, finite decisions, obstruction, costs
- recovery.py: new value-only decoder, explicit errors and cost envelope
- live_checks.py: fresh full integration and exact arithmetic controls
- replay_checks.py: paid whole-schedule original-context replay
- ORIGINAL_INPUT.json: independently retained input/state/fixed sigma
- RECOVERY_RUN.json: returned sparse result, observations and complete receipts
- CHECK_RESULTS.json / RUN_LOG.txt: author-run new recovery checks
- REPLAY_RESULTS.json / REPLAY_RUN_LOG.txt: separate full replay evidence
- CONTRACT.json / STATUS.json / MANIFEST.json: scope, status and integrity
- vendor/: unmodified pinned accepted dependencies, included for reproduction

Run python live_checks.py, then python replay_checks.py from this directory.
Only Python standard-library modules and the pinned local dependencies are
needed. The accepted dependencies' earlier test suites are not rerun.

This does not close ALG-034, establish dense/general-block input, implement
random-bit acquisition, prove outer transfer or amplification, materialize all
N output coordinates, or inherit a speedup or novelty claim. Correct execution
and independently retained original context are required; replay is not
external-origin authentication or historical execution attestation.
