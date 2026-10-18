# Harper theorem and independent review binding

11 October 2026

## Result

The direct independent review of the parity-resolved Harper theorem has been recovered and bound to the exact canonical theorem bytes. M-HARPER's upstream proof-review gap is closed by recovering existing evidence. The downstream phase-pencil audit was never the only relevant review, although it was the only review cited by that catalogue row.

The recovered review, dated 9 October, explicitly proves the zero-mode obstruction and the exact parity polynomial degrees in Section 3. The present pass checks that proof's hypotheses and argument, verifies its source and capsule hashes, and checks the arithmetic consistency of its saved finite-result summaries. It does not rerun the archived verifier or reclassify inherited computations as fresh matrix replay.

## Exact evidence chain

The canonical theorem is PRIOR_PHASE18_THEOREM.md in the catalogue source snapshots, also present as fft_green_phase18_harper_covariance/THEOREM.md in the original Phase18 ZIP. Both copies are 12,425 bytes and have SHA-256:

0e8b143e730ccb7aceeab4a0f32f63be7f02fc851fad20c04d61ddb460393796

The newly recovered direct review is PHASE18_PHASE17_INDEPENDENT_AUDIT.md, 28,261 bytes, from master additions/1628/audits/phase18. Its SHA-256 is:

2711aa3a4d6e57f392ebef7b7fd4ad72d6543139e0634efa1aa7ec2c6db12304

Its accompanying source_inventory.json explicitly records the canonical theorem's member name, size and exact hash. The inventory has SHA-256:

15b00c713be86a332b184d7c4662370fea3a73cf85115a8ffc438dbef8e43917

The audit capsule's AUDIT_FILES.json lists and binds the review, inventory, saved results, verifier, logs and other companion files. All eight listed files have been recovered and their byte counts and hashes match. The manifest itself has SHA-256:

bfcb0a8ca3eca9b18d9658da35ecdf738741ffbc5917977715e9f5f18afd7083

The underlying original source ZIP, fft_green_research_phase18_2026-10-09(1).zip, has 587,649 bytes and SHA-256:

6838b9f1466d1adb7a63dfff277a4eafdf945db9ba9204b033d4018f45b0a291

Its CRC checks pass. A fresh recursive byte inventory matches all 382 member occurrences in the saved inventory exactly. All 23 entries in the direct Phase18 source checksum manifest also match. This includes the directly embedded preceding checkpoint as well as the theorem and original finite certificate. Full recovery paths and byte counts are in RECOVERED_BYTES.json and PHASE18_ZIP_MEMBERS.json; BINDING_VERIFICATION.json records the checks.

This is content-and-scope binding through the recovered review capsule and its paired inventory. It does not infer acceptance from a filename, the phrase independent audit, or a shared research-family label.

## The claim and hypotheses checked

Let N be a positive multiple of four, N at least 4. Work over the complex numbers with normalized Fourier F[j,k] = exp(-2 pi i jk/N)/sqrt(N), cyclic shift Z, phase diagonal D, reflection J = F squared, and H = Z + inverse(Z) + D + inverse(D).

The accepted assertions are:

1. H has exactly two zero modes, one of each J parity. Their Fourier eigenvalues lie respectively in {1,-1} and {i,-i}. Thus no single scalar spectral function f(H), including a rational function whose denominator is invertible at H, equals F.
2. There are unique polynomials p_plus and p_minus below their parity-sector dimensions such that F equals p_plus(H)(I+J)/2 plus p_minus(H)(I-J)/2. Their exact minimal degrees are N/2 and N/2-2. The leading even coefficient is 1/(2 sqrt(N)); the leading odd coefficient is -2i sin(2 pi/N)/sqrt(N) for the stated Fourier sign convention.
3. These are restrictions on one commuting Harper functional calculus. They do not exclude arbitrary noncommuting Green constructions or prove a general Fourier arithmetic-circuit lower bound.

The proof uses the reflection-even and reflection-odd Jacobi blocks, of dimensions N/2+1 and N/2-1. Their nonzero off-diagonal entries make each eigenspace at most one-dimensional by the first-component recurrence; real symmetry then gives simple spectra. Signed reversal sends either block to its negative. Each odd-dimensional block consequently has precisely one zero eigenvalue. Commutation with F and F squared = J distinguish their Fourier eigenphases.

Within either simple-spectrum block, an operator commuting with H is a unique polynomial below the block dimension. The even endpoint entry at cycle distance N/2 is zero for every smaller power. At degree N/2, exactly two unit-weight shortest paths contribute, yielding the leading coefficient 1/(2 sqrt(N)). The odd-block endpoint distance is N/2-2; its unit-weight unique path and nonzero Fourier endpoint entry force the second exact degree. N=4 is included: its odd block has dimension one and its odd polynomial is a nonzero constant. No additional genericity assumption is needed.

No defect was found in this argument at the stated scope. The direct sparse Horner evaluation costs quadratic arithmetic; that observation is not a universal lower bound on every way of evaluating or factoring F.

## What was and was not replayed

The saved independent_phase18_results.json has SHA-256:

972331cafbe1d4d2b4e75ba8c84bab1cb234a8462855bf3ad1bc0623888af202

The recovered audit attributes exact all-entry Harper reconstruction to N = 4, 8, 12, 16, 20, 28, 32, 36, 60, 64 and 128. These checks use the unnormalized W = sqrt(N) F, avoiding arbitrary modular square-root choices. They record the two nullities, exact polynomial degrees, leading coefficients and distinct zero-line Fourier eigenvalues. They are prior independent results, not executions performed in this pass.

The new verifier verify_binding.py only reads archived bytes and JSON data. It independently checks primality and exact root order for the eleven saved cases, dimensions and degrees, the recorded even leading coefficient 1/2, the odd coefficient from the root, nonvanishing, and the zero-mode relation lambda squared = parity times N. All summaries are internally consistent. It does not regenerate the matrices, coefficients or eigenvectors behind those summaries, and their all-entry-equality flags are retained as attributed results. The all-N complex theorem rests on the proof above, not an inference from finitely many residues.

The original harper_audit.json and its original implementation are separate from the independent audit. A later static program review of harper_certificate.py is also recovered. That review explicitly says the uniform complex theorem was not reviewed there; it cannot substitute for the direct mathematical audit. No archived program, including the earlier independent checker, was executed, imported, compiled or syntax-parsed in this pass.

## Minimal catalogue correction

Catalogue row 70 and canonical novelty row 106 should replace the current missing-upstream-review language with this exact direct-review binding. Historical statement and historical inspection fields may remain as history. Preserve the original downstream phase-pencil review and its distinct scope; there is no need to discard or rerun it.

The catalogue's Phase19 source and downstream gauge conclusions are not promoted beyond their existing acceptance by this recovery. The recovered Phase18 audit also contains sparse-intertwiner and fixed-factor middle-monomial arguments, but no blanket acceptance of every statement, implementation or later construction in the same family is asserted here.

ROW_CORRECTIONS.json supplies proposed cell edits only. This pass wrote neither Google Sheets nor GitHub. The existing repository export variant of the downstream review remains a separately recorded byte identity; no repository variant was fetched or declared corrupt in this pass.

## Remaining work

There is no remaining missing-proof-audit obligation for the precise Harper zero-mode and parity-degree theorem. The next M-HARPER obligation is a model-matched primary-literature comparison for the exact minimal degrees and leading coefficients. The recovered audit attributes the basic Harper commutation, parity structure and double-zero phenomenon to earlier literature and makes no priority claim. That attribution is retained; no fresh external novelty search was performed here. Generic Fourier-rank or graph-rank references alone do not settle this specific priority question.

A constructive noncommuting Fourier family still needs its own exact identity or dual intertwiners, calibration and paid evaluator. It is a separate research problem, not a prerequisite for accepting this restricted theorem. No faster FFT, new original theorem, integer-multiplication improvement or unrestricted impossibility is claimed.
