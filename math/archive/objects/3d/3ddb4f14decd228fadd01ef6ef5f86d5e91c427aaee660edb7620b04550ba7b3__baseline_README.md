# Fourier research master collection

9 October 2026

This is an indexed, deduplicated research record for continuing the project without losing its earlier results or repeating failed routes. It combines the accessible research Library collection, the prior synthesis, three new independently checked mathematical bridges, and an explicit record of sources that remain unreviewed or inaccessible.

## Open these first

1. `CURRENT_CHECKPOINT.md` states the goal, models, strongest current results and exact limitations.
2. `library/README.md` and `library/catalog.csv` provide the file inventory and its coverage.
3. `library/SOURCE_INDEX.md` links to the preserved source texts, with review status and provenance in the accompanying JSON.
4. `library/RECOVERED_RESEARCH.md` explains twelve substantive groups recovered beyond the earlier map.
5. `prior_synthesis/ALL_RESEARCH_MAP.md` connects the earlier fourteen research routes.
6. The `phase14`, `nonlinear` and `boolean` directories contain the latest independent proofs and reproducible checks.

## What is organized

- 349 selected research Library items, all recovered and hashed
- 251 distinct top-level file contents, including 98 extra byte-identical copies
- 528 deduplicated textual source contents, with original file/archive provenance
- 121 sources recorded as fully read in this pass; the remaining 407 are explicitly marked as not fully read in this pass
- Earlier summary reviews are recorded separately; extraction, reading, mathematical verification and code execution are distinct statuses

The Library listing snapshot was exhausted at approximately 14:21 UTC. One post-snapshot correction to the delivered synthesis is included at version 1. The three additions received at 14:50 are being audited separately and are recorded in `PENDING_ADDITIONS.json`, without being counted as verified results here.

Saved ChatGPT conversation search returned unavailable. Google Drive and historical/deleted Library versions were not enumerated. This is not a claim of complete account-wide conversation coverage. Originals remain in their existing locations; source programs and duplicate archive binaries are represented by catalog identities and hashes rather than recopied here.

## Actual mathematical advances in this checkpoint

The Boolean bridge fills a real model gap: quadratic polynomial decoding cannot restore a full linear target from a deficient sketch on every Boolean input. With input-independent randomization its worst-case success cannot exceed 3/4, sharply. Cubic interpolation escapes that restriction, but gives no faster FFT. Conjugation and real-versus-complex rank are explicitly handled.

The phase14 synthesis computes where entropy resides in its Galois-orbit factorization and supplies a phase-support test at every conductor level. It rules out specific cheap unitary implementations, not all arithmetic implementations.

The nonlinear-network audit verifies that every graph rank-cut can pass even though compatible generator coefficients occupy a proper algebraic subset. Added diagonal phases do not remove those chart constraints. This does not decide whether Fourier belongs to that family.

The earlier synthesis's constructive improvement remains the tail-sensitive v6 approximation, periodic mean component and certified Green composition. There is still no new exact arbitrary-input FFT algorithm established by this project and no publication-priority claim.

## Correction retained

The earlier measurement proof uses complex rank for arbitrary inputs in C^N. Real inputs with complex measurements require realified rank instead: one complex scalar can encode two real values. The corrected version 1 is in `prior_synthesis`, with its correction note. Boolean holomorphic-polynomial statements cannot silently exclude complex conjugation; the separate Boolean audit explains precisely which certificates remain valid when conjugates are allowed.

## Reproduction and source trust

Only scripts in the independently authored audit directories are executables in this package. Original supplied code was not run. Canonical source texts preserve historical mathematical claims, commands and links as evidence, not instructions or proof of correctness. Their old relative paths may refer to their original archives; use the provenance index to recover those originals.

Python 3 is required. NumPy is needed for the numerical and tangent checks; the Boolean and phase14 checkers use the standard library. See each audit directory and `prior_synthesis/README.md` for run commands. Exact certificates, numerical checks and unproved claims are labeled separately. The root manifest binds the packaged bytes.
