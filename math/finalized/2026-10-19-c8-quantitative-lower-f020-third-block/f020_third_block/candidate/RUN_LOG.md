# Run log

19 October 2026 UTC. Local author-level research only.

## Inputs read

Read the exact accepted b<2p author proof and accepted b=2p author proof and independent review before extending them. Inspected the relevant acceptance verdicts and manifests. All input paths, sizes, and SHA-256 hashes are in SOURCE_BINDINGS.json. Verified the accepted boundary report and manifest hashes against its independent verdict and checked all 24 file entries across the boundary author and review manifests. No source file was modified and no prior checker was imported or executed.

## New derivation

The initial target was the nearest new degree b=2p+1. The exact joining identity exposed the strict gap (p−3)/2+1/(2p), including 1/6 at p=3. The same estimate with a short tail continuant proved sufficient for every 2p<=b<3p. Both parity cases were separated explicitly. The accepted boundary residual was transported coefficientwise; outer simple roots and the exact odd-degree zero completed the root count.

A pre-freeze proof reread corrected a displayed arithmetic equality in the auxiliary bound for P_(2p−1): its joining-term excess is h−1/2+alpha, not h−1+alpha. The weaker lower bound used in the theorem and programs was already valid. The final report gives the exact equality. No failed mathematical check or uncorrected issue remains in this author packet.

## Fresh computations

1. Authored check_third_block.py from scratch, using sparse exact integer recurrence arithmetic and finite-field arithmetic.
2. Executed:

       python /workspace/shared/f020_third_block_extension_20261019_1347/check_third_block.py

   First run: PASS, 537 exact assertions for p=3,5,7,11,13 and every 0<=r<p. No floating point, no root numerics, no imported historical checker. Results are CHECKS.json and check_run.log.
3. As an exploratory transcription check, separately computed the actual symbolic discriminants of P_7 and P_8 in SymPy, then their uniformizer valuations modulo Phi_9 and Phi_27. The values were 37 and 40 in both fields.
4. Authored check_discriminants.py from scratch to persist and extend that calculation to P_6,P_7,P_8 at s=2,3. Executed:

       python /workspace/shared/f020_third_block_extension_20261019_1347/check_discriminants.py

   First run: PASS, six exact actual-discriminant controls. Results are DISCRIMINANT_CHECKS.json and discriminant_run.log. This check computes actual discriminants rather than reusing the pairwise-distance formula.
5. Created SOURCE_BINDINGS.json, INPUT_VERIFICATION.json, RESULT.json, and a frozen MANIFEST.json.

The theorem is the uniform proof in REPORT.md; finite controls are transcription and supplementary nonvanishing evidence. The output is submitted for independent review. There was no browser use, external write, repository change, canonical record change, or claim of historical originality.
