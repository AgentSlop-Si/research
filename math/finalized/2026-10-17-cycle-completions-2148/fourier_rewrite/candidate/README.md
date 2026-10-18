# R30 Fourier-window completion

The remaining eligibility question is closed for an explicit complete
radix-two DIT Fourier factorization and its stage-aligned component windows.

For N = 2^D there are N(D-1)+1 nonempty component windows. Exactly zero
match the implemented R30 rho = ±3 rewrite, even after invertible monomial
boundary changes. The proof uses exact row support for multi-stage windows
and a 2×2 cross ratio for single-stage windows.

Extending rho to ±i recovers ordinary two-point butterflies. PROOF.md gives
the full cyclic DFT identity, the exact count ND/2 of pair components, and
the unchanged O(N log N) arithmetic. This extension is not implemented by R30.

Further scoped results:
- A chain of full-vector two-sparse R30 kernels needs at least log₂N mixing
  factors to realize a dense DFT.
- Conjugating an ordinary Fourier phase on s axes produces exactly 2^s
  distinct XOR directions; all-axis direct factor evaluation still has
  O(N log N) work.

Files:
- PROOF.md: definitions, full identities, classification, costs, limitations
- verify_completion.py: fresh exact checks, without importing R30 code
- verification.json: complete checked results
- verification_summary.json: compact checked totals
- SOURCES.md: source and attribution ledger
- MANIFEST.json: SHA-256 hashes of the release files
- source/: exact proof/report source excerpts; the full supplied archive is retained privately
- SOURCE_PROVENANCE.json: historical source-archive digest; see ../../PORTABILITY.md

Reproduce:
    python3 verify_completion.py

Checks pass through N = 1,024, with 1,398,100 exact full-DFT entries and
16,398 declared component windows across the tested sizes. Separate exact
Gaussian-rational checks verify both coefficient classes. Finite-field
phase checks are labeled corroboration, not the complex-field proof.

This is a scoped mathematical completion, not an unrestricted Fourier
lower bound, new speedup, or historical-priority claim. The supplied
54-program duplicate audit was not repeated. No supplied program was run.
