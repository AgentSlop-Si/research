# Independent run log

19 October 2026 UTC. All mathematics, source reads, and execution remained local. No repository or external service write occurred. Candidate and historical programs were neither imported nor executed. Only freshly authored review programs ran, using Python standard-library modules and the installed SymPy package.

Commands on the frozen final code:

    python check_uniform.py > UNIFORM_RUN.stdout 2> UNIFORM_RUN.stderr
    python check_exact_identities.py > EXACT_RUN.stdout 2> EXACT_RUN.stderr
    python check_p3.py > P3_RUN.stdout 2> P3_RUN.stderr
    python verify_bindings.py > BINDINGS_RUN.stdout 2> BINDINGS_RUN.stderr

All passed. All four stderr files are empty. Uniform controls cover p=5,7,11,13,17,19,23. Unreduced integer identity controls cover degrees 9,15,21. The p=3 script constructs the actual P9 and its quartic from scratch, checks rational cyclotomic remainders at orders 27 and 81, uses the degree bound for every higher allowed order, and independently reproduces the candidate factor-vector, mod-2 remainder, and degree-nine discriminant identities.

The retained CANDIDATE_P3_CERTIFICATE.json is an exact byte copy of the sealed candidate's mathematical data, used only for comparison against independently computed polynomials. Its SHA-256 is f97ce09fbc75f803b12dfe84b51a46698a8100368c1ab3e4344ccc990392e758. The three mathematical checkers are portable within this directory. The separate binding verifier intentionally points to the original local dependency paths and is a provenance check, not an input to the mathematical programs.

The candidate report and accepted source proofs were read and challenged, including the whole-block edge indices, double-bridge term, all coefficient and derivative gaps, inseparable-residual multiplicity count, simple zero, primitive-value-group argument, p=3 order restriction, actual H conversion, and original bilinear CD normalization. No blocking issue was found. All 26 candidate entries, all 44 entries of four accepted dependency manifests, ten source original/copy bindings, and two acceptance bindings passed verification.

The accepted third partial block is a dependency and is not counted as new. The new theorem is only degree b=3p below the root order. No research-status or external index change is made by this review.
