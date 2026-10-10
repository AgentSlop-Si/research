# START HERE — Green/FFT Research Phase 21 (October 9, 2026)

**Goal:** continue the user's independent Green/graph computation-sharing research towards exact Fourier transforms below `N log N`. **No new asymptotic FFT speedup has been found.**

- `fft_green_phase21_weyl_resolvent/THEOREM.md`: algebraic identities, proofs, cross-ratio/Hankel lower bound, stronger common-order product-of-sums bound, approximation floor, and the O(N) full-rank commutator control.
- `fft_green_phase21_weyl_resolvent/CHECKPOINT.md`: recovery instructions and exact Phase 22 research target.
- `fft_green_phase21_weyl_resolvent/phase21_weyl.py`: standalone exact finite-field examples, cyclic Green solves, direct quadratic chirp executor and tests.
- `fft_green_phase21_weyl_resolvent/audit.json` and `tests`: empirical controls, not proof of complex-FFT speed.
- `fft_green_phase21_weyl_resolvent/previous_full_phase20_checkpoint.zip`: entire prior Phase 12–20 chain, with earlier sources nested.

**New takeaways:** Uniform flat-magnitude dense O(N)-work Green operations are possible but do not reproduce Fourier curvature. For any common-order sum/product circuit of cyclic weighted Green resolvents and diagonal gates, exact Fourier equality requires **at least N/2 counted Green terms**. The separate noncommuting Weyl generator already gives a full-rank commutator in O(N), so high displacement rank is not enough. Distinct coordinate orders plus true Fourier phase coherence are the necessary next design directions.

**Verification:** Run `python fft_green_phase21_weyl_resolvent/verify_full_lineage.py <phase21_archive.zip>` after archive extraction. Do not misinterpret the pole/term lower bound as a lower bound on shared-state algorithm runtime.
