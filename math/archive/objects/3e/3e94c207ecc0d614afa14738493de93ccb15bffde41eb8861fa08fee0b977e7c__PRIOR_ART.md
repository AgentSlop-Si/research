# Prior art and provenance

- `rank(P-Q)=n-#cycles(P^-1Q)` for permutation matrices is elementary, classical linear algebra; Phase 24 uses it to quantify the cost of conjugating the Fourier shift.
- Stable binary sorting is an inverse two-packet riffle shuffle. Related literature includes Persi Diaconis, Michael McGrath, Jim Pitman (1995), *Riffle shuffles, cycles, and descents*, Combinatorica 15, 11–29, DOI:10.1007/BF01294457. No claim of previously unknown combinatorial identities without a systematic literature audit.
- Sherman–Morrison–Woodbury is classical; here it turns low-rank changes to a cyclic successor into low-rank corrections of a block-diagonal spectral Green resolvent.
- The real Fourier residual `C Z=R C` and its special-input executor are inherited from Phase 22/23 and not new Phase 24 claims.
- The all-stride probability bound follows from elementary pattern counts, independence on disjoint windows, and Hoeffding's inequality.
- Existing restricted lower bounds for arbitrary FFT linear circuits do **not** transfer automatically to input-dependent sorting or unbounded-coefficient Green computations. No unrestricted FFT complexity theorem is claimed.
