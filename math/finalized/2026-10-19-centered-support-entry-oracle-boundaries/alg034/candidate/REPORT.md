# ALG-034 centered-output support obstruction

19 October 2026 UTC. Author-verified source-bound result, pending independent review.

The current accepted nonconstant bounded-variation supplier is unchanged. Its already accepted precision and complete-cost proofs were not repeated. The proof uses the classical comb/roots-of-unity identity and Parseval energy counting; the result is a contract-specific application, not a claim that these mechanisms are new.

The proposed extension tested here is to cover arbitrary dyadic originals while retaining that supplier's O(M^(1/4)) explicit candidate list, or that size times fixed logarithmic factors. An exactly normalized dyadic-comb family refutes it:

- At tolerance R M^(-1/4), at least sqrt(M)/16 nonzero coordinates must be retained.
- Even at the outer theorem's weaker tolerance 4R M^(-1/4), at least sqrt(M)/256 must be retained.
- Omitted selected coefficients are exactly twice the respective tolerance. No extra precision or randomized tape repairs a too-small list.
- Parseval gives a matching O(sqrt(M)) existence bound for explicit P-grid approximations. It does not give a recovery algorithm or make source preparation free.

The same comb also explains a concrete cap-only failure in the unchanged BV source: its variation cutoff becomes M or 4M, violating the required cutoff below M/2. This does not contradict the accepted bounded-variation family, which excludes the comb.

With the accepted P=16m+16 grid, required coefficient magnitudes occupy Omega(sqrt(M) m) bits in the explicit list. At N=M/4 the unchanged outer iterator has exactly 40m+1 incidences per retained coordinate. Setup, source binding/replay, medians, scale, history and all N output records remain separately charged. These are contract/implementation-specific facts, not a general FFT lower bound. The all-length theorem's larger O(M^(3/4)) allowance remains compatible, and no inherited saving is presented as new.

Fresh exact checks passed: 34 symbolic plans through m=1024; 24 centered coefficients via 279,552 original-coordinate terms; all 1024 alias-grid rows via another 262,144 terms; omission/location/precision-boundary controls; two paid default-provider rejections; and two recognition-only diagnostics with explicit cap overrides. No general supplier, full outer execution or practical speedup is claimed.

All 37 members of the latest accepted BV manifest were verified before binding the snapshots. See PROOF.md for complete statements, prior-work separation, source links, precision and lifecycle costs; SOURCE_BINDINGS.json for hashes; CHECK_RESULTS.json and check_obstruction.py for reproduction.

ALG-034 remains open. No table, score or GitHub write was performed.
