# Matrix second-audit proof package, v1

Accepted scoped mathematics, with proof/certificate/priority status separated. Start with CORE_THEOREMS_SECOND_AUDIT.md and STATUS_UPDATES.json.

Main new theorem: the fixed-pair Weyl–Green lower bound extends from primes to all odd prime powers, with an explicit gcd bound at every odd length. The deficit–separator extension and strengthened commutator gap are supporting results. Displacement, paired-Jacobi, Hadamard–Segre and multiscale previously source-only statements now have independent proof review and fresh decisive controls.

All five manuscripts have been accepted at statement/proof level by a separate reviewer. Data reconstruction was performed by the matrix author, not independently rerun by that reviewer. C01 uses its existing accepted certificate chain; the final Delvaux–Van Barel2008 priority comparison remains blocked. Q33 finite quadratic reconstruction is explicitly outside this frozen version.

Reproduce fresh controls with Python3 standard library: run fresh_checks.py, paired_checks.py and multiscale_checks.py from this directory. They read only the three inert JSON source_inputs where required. No supplied research program is included as an executable dependency. The results are mathematical finite controls, not timing benchmarks or general proofs.
