# Restricted Taylor-product precision: constructive savings and linear necessity

Research candidate, 18 October 2026 UTC. Local files only; independent review pending.

- Exact recovery from the actual bounded Taylor image is possible at `W_box=2m+v2((2L-2)!)+delta`, where m>=2 and delta is one only when L>=4 is even and m>=3. This saves `ceil(log2 L)-delta` bits relative to the general-polynomial guard. This is a sufficient height-envelope bound, not the minimum restricted guard.
- Explicit pairs with the same left factor prove a restricted sample-only guard lower bound `0.8535762332... L-O(log L)` for explicitly sufficiently wide m. Their original chunks are all below `2^m`, and their values collide at every integer node, before and after Taylor translation.
- The implemented two-scale decoder pays `O(L^2 W_box log(L+1))` non-product work and `O(L W_box+L^3)` storage, plus backend workspace. Exactly `2L-1` evaluation products are made, all using the pinned terminating Karatsuba backend. The full Mersenne route and final carries are implemented.
- This does not provide a general sub-`N log N` multiplier, exact restricted optimum, improved recursive sharing, or historical novelty claim.

Read REPORT.md for the proofs and complete cost/precision scope. Run `python exact_controls.py` in this directory. RESULTS.json records the deterministic outcomes; WITNESSES.json contains explicit bounded-input collision arrays. SOURCE_PINS.json and MANIFEST.json bind the package and accepted dependencies. INITIAL_CONTROL_FAILURE.stderr retains a repaired zero-width statistics-field issue.
