# RECOVER HERE — Hero #17 phase-five Gauge-Union (2026-10-10)

**Global mission:** exact sequential O(N) FFT for all fresh arbitrary N-vectors with all N explicit outputs and preprocessing/recovery fully charged. **Still open.** Don't substitute special inputs, approximate word-RAM Fourier transforms, hidden cached coefficients, or optimized existing algorithms.

**Prior completed phases:**

- `fft_hero17_shear_trace_green_union_2026-10-10.zip`: exact linear-time restricted multi-shear Green-Union with sparse innovations, and chain of earlier tensor/fiber/delta/single-shear structured-input algorithms. Prior tests `76/76` rerun cleanly in this session.
- `hero17_phase4_orbit_displacement_gate_2026-10-10.zip`: square dense graph remains ~N^1.5 edges; K has rank-one Sylvester displacement but ordinary full rank; coprime single-route factorization hides conventional FFT. Phase-four tests `7/7` rerun cleanly.

**Phase 5 findings:**

1. General square universal basis `mu_j=omega^j`, lambda_j(h)=omega^(j-M*h*a_j), with *arbitrary* shear values `a_j`: every V_h is invertible since lambda exponents are distinct mod M.
2. Every basis gives `K_h V_h^(-1)=F_M diag(omega^(-h*t))`, so no basis-only runtime benefit follows.
3. Schur channel mask `E_Delta[t,j]=eta^(-Delta*t*a_j)` has `rank=|{Delta*a_j mod M}|`. Canonical a_j=j gives `rank=M/gcd(M,Delta)`, but for adjacent channels ANY rank 1..M is possible without changing the transform. This kills single-metric cross-channel sharing claims.
4. Canonical-gauge minimum weighted channel-spanning-tree mask-rank sum is `sum_(d|M,d>1) d*(M/L_prev - M/L_current)` with L being lcm of encountered divisors. For M=2^m this is `M log2 M`; tested via independent Prim and exhaustive labeled-tree enumeration. **This is not a universal FFT circuit lower bound** and is completely gauge dependent.
5. Complex clustered-root Vandermonde V_0[t,j]=exp(2*pi*i*t*j/M^2), independent of shear list, obeys `kappa_2 >= sqrt(binomial(2M-2,M-1))*(M/(2*pi))^(M-1)`. High-precision log10 condition estimates at M=8,16,32: 7.73,21.37,53.78. Finite-field exact inversions don't imply numerical stability.
6. Well-conditioned counter-gauge mu_j=eta^j, all a_j=constant, makes every V_h a scaled Fourier matrix (condition1), mask rank1, but K_hV_h^-1 is precisely the classical Fourier stage. For prime M, all V_h remain invertible within mu_j=eta^j only when all a_j equal (rigidity theorem).

**Verification:** `8/8` new tests; 37 independently coded full arbitrary-input exact DFTs (2,719 coefficients), 183 independently computed mask ranks, 129 independent MST checks, 18,248 Prüfer trees exhaustively searched at M=2..7. All checked.

**Next real challenge:** develop a basis-INVARIANT, fully charged cross-channel contraction of the polyphase Fourier tensor from fresh x directly to all X, and demonstrate a uniform faster recurrence or exact finite circuit. Test it against this gauge counterexample, output dimension and condition-number audit. Do not present low displacement rank, channel mask rank, graph-edge count, FFT operations hidden as plan build, or quantum-state preparation as proofs of O(N).

**Reproduce:** `python -m unittest discover -v`; `python independent_audit.py`; proofs in `RESEARCH.md`.
