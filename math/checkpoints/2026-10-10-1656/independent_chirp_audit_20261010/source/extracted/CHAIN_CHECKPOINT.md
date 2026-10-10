# RECOVER HERE — Hero #17 Phase 23 (2026-10-10)

**Primary target still open:** exact O(N) full Fourier transform of an arbitrary fresh input vector, with all N outputs, on one sequential processor with fully charged work. Phase23 proves only a larger structured-input fast family.

## Latest positive results

1. For N odd, eta primitive 2N-root, x_t=gamma*mu^t*eta^(s t²)/(eta⁸;eta⁸)_t (any mu!=0), the fully verified raw signal admits a **single three-point spectral recurrence** `X_(j+4)=X_j-r1*omega^j*X_(j+s)+B` with `r1=(1-eta⁸)x1/x0`, `omega=eta²`, `B=x_(N-1)*r1*omega^(-s)`. No assumed parameter metadata.
2. Discover chirp s from `r2/r1=omega^s`; a deterministic table of only O(Budget²) **eligible** chirps is prepared by enumerating short/wrapped jumps and small subgroup orders, without hashing/discrete log. Verify all N raw input entries before any fast-path acceptance.
3. **Coset-union theorem:** let d=N/gcd(N,s). Directly calculate d Fourier bins in subgroup H=<s>. Propagate each coset H+4r to H+4(r+1) using one three-point equation per output; 4 generates the quotient since N is odd. O(dN+N) exact arithmetic; d fixed gives O(N), even when s grows with N.
4. Short s>=5: s raw seeds and O(N) recurrence. Wrapped s=N-t: t+4 raw seeds and O(N) recurrence. s=1,2,3: four seeds. s=4: one-pole cyclic Green solve, at most two seeds, batch inverse for nonzero denominators; resonant zeros are handled exactly. All have O(N) complexity when seed count is bounded.
5. **Hankel escape:** normalized by Phase22 base q-Gaussian, b_t=gamma*mu^t*eta^((s-2)t²). Leading r Hankel factorization is diagonally-scaled Vandermonde. If gcd(s-2,N)=1, rank r=(N+1)/2. Thus the new three-seed family s=N/3 at N=3^m has growing maximal Hankel rank; Phase22's fixed-order Prony detector rejects it.
6. Ordinary **N-output** exact-field benchmarking: at N=177147, three-seed coset 3,011,573 scalar field operations vs 6,849,772 for a fully charged conventional N-point radix-3 NTT, ratio 2.27448. Fixed s=7 uses 4,428,725; wrapped s=N-2 uses 4,251,577; nine-seed coset s=N/9 uses 5,137,301. These are different algorithms for the same structured input; no hardware or universal speedup claim.

## Verification

- New `test_phase23.py`: 18 unit test groups, including exhaustive eligible-s small cases, all strategies, resonance, non-grid mu, random/adversarial fallback, long full NTT checks.
- Inherited Phase22: 42 unit tests pass.
- `independent_audit.py`: 265,716 exact NTT output coefficients, 328 direct bins, 78 rejections/fallbacks, explicit checks Phase22 rejected cases.
- `coset_audit.py`: 1,062,720 complete exact NTT comparisons across 32 family/length cases, 413 selected directly summed outputs and 27 random fallback checks. Source was audited after introduction of the sparse phase gate and one-pole special case; regenerated final JSON/logs are authoritative.

## Stop rules

- Do not call this a general O(N) FFT; generic inputs fail fast recognition and get ordinary fallback. For large unstructured s, seed size can be Omega(N), not linear under this method.
- The data-generator's parameters are NOT supplied to the executor. Only N, prime field and a primitive root are supplied; every raw sample is checked.
- All numeric ledgers cover prime-field arithmetic and root powers; index and phase comparison work is separately O(N), not numerically included. Root discovery, bit complexity and floating point are outside model.
- No historical novelty priority established; q-holonomic and fast polynomial evaluation have substantial prior art. Avoid rediscovering Phase21/22 Jordan, earlier Green resolvents, cached FFT, CrocSwap and fixed-rank partial output results.

## Phase 24 challenge

Study **bootstrap percolation / minimal seed sets** in the exact spectral hypergraph `{j,j+4,j+s}` for generic s. Is there an *input-independent*, deterministic O(N)-constructible seed schedule with o(logN) or O(1) direct Fourier seeds for all s, and can it be extended beyond the chirped q-Green recognized family? If generic seeds cost Omega(logN), a new full-sharing evaluator is needed. Independently, assess existing q-holonomic and q-hypergeometric transform prior art before any publishability claim.
