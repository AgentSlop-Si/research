# Start here — Phase 42 (October 10, 2026)

**No new `o(N log N)` FFT has been proved.** This is the complete chain-safe research continuation from the Phase 41 unit-phase Green results.

## Read first

1. `fft_green_phase42_three_row/CHECKPOINT.md` — exact Phase 43 starting point.
2. `fft_green_phase42_three_row/THEOREM.md` — rigorous scope and proofs.
3. `fft_green_phase42_three_row/VALIDATION.md` — exactly what was rerun and checked.
4. `fft_green_phase42_three_row/RUN.sh` — standalone exact tests; `bash RUN.sh historical` also reruns Phase 41 from the nested archive.

## Main discoveries

- **Uniform theorem for weighted Hamiltonian Green *sums*:** `N<=q(q+1)^q` is necessary to equal the DFT up to monomial input/output gauges, even for arbitrary complex edge amplitudes. It is a restricted representation theorem, not a universal FFT lower bound.
- **An all-row `N=128` impossibility certificate for the original three Hamiltonian orders:** exact integer audit of all **10,668,000** four-row subsets; every one exhibits a forced rank-3 block in a `4x4` Fourier minor, independent of Green weights and external monomial gauges.
- **Three-row tangent obstruction:** exact two-prime Jacobian ranks `2N+1` for a three-cycle unit-gain sum at N=8,16,32,64; only three real degrees of freedom remain locally after fixing the first two rows.
- **Constructive escape:** a product of *two* noncommuting three-Green sums has full local three-row phase rank `4N-4` at the same four sizes. This does not prove the specific Fourier target can be reached. The tested product violates both Weyl equations.

## Next

Aim for exact **three-row Fourier synthesis** from the two-stage product, then the fourth row and complete Weyl equations, including the offline cost of phase parameter discovery, memory and precision. Do not repeat the exact additive architecture already ruled out.

The archive contains the unmodified **full Phase41 ZIP**, whose own nested archive retains earlier phases.
