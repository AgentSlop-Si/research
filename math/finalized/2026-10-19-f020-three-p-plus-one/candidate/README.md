# F020: only b=3p+1

Read REPORT.md for the scoped theorem and complete proof. The author packet awaits independent review.

Reproduce from this directory:

    python check_uniform.py
    python check_exact.py
    python verify_sources.py

The first checker uses only the standard library. The second uses installed SymPy and checks exact integer identities. Existing checker code is not imported. Both program outputs are frozen; the proof does not infer an infinite theorem from finitely many primes.

For p>=5 the three root valuations are (2p−1)/(2p), 1, and (p+1)/4, with counts 2p, p−1, and 2. The p=3 argument is separate. The ordinary X-discriminant valuation formula has no p=3 claim and is not a q-discriminant formula.

No general fourth-block theorem, unrestricted owner closure, score change, historical novelty claim, or external write is included.
