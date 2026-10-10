# Hero #17 — Phase 23: Chirped q-Green Cayley-Graph Union

**Date:** October 10, 2026  
**Status:** exact identities, reproducible finite-field implementations, complete coefficient comparisons, operation ledgers, and predecessor regressions. **Not a universal O(N) FFT or historical novelty certificate.**

## Executive result

Phase 22 handled q-Gaussian signals whose normalized coefficient vectors were bounded-order exponential polynomials. Phase 23 handles another strictly wider *structured* family: an **unknown quadratic chirp**, unknown amplitude and arbitrary nonzero unknown phase, directly recognized from every raw input sample.

For `x_t=gamma mu^t eta^(s t²)/prod_(j=1)^t(1-eta^(8j))`, over odd transform length N in a field with primitive 2N-root eta, the full positive-sign N-point DFT obeys one exact three-point spectral recurrence:

`X_(j+4)=X_j-r_1 omega^j X_(j+s)+B`, with `omega=eta²`, `r_1=(1-eta⁸)x_1/x_0`, `B=x_(N-1) r_1 omega^(-s)`.

This creates a sparse **frequency-domain Cayley hypergraph**. It admits four exact evaluation strategies:

| Strategy | Seed Fourier bins calculated directly | Other work | When useful |
|---|---:|---:|---|
| Short jump | `max(4,s)` | `O(N)` | fixed small s |
| Wrapped jump | `N-s+4` | `O(N)` | s close to N |
| **Subgroup/coset union** | `d=N/gcd(N,s)` | `O(N)` | s of bounded additive order, including s=N/3 |
| Resonant one-pole | at most 2 | `O(N)` | s=4, including zero denominator |

A deterministic input-independent **sparse phase gate** enumerates all chirps with seed cost <=B using only O(B²) candidates. It recognizes unknown s, unknown mu (not necessarily a Fourier root), and verifies every input sample before using the fast path. For fixed B, the accepted-input cost is **O_B(N)** field arithmetic and **O_B(N)** word operations, including root-power table preparation and all N outputs. Unsupported/random inputs fall back to a conventional N-point NTT.

## Why this escapes Phase 22

Relative to the original q-Gaussian normalization, the input contains `mu^t eta^((s-2)t²)`. Its leading r-by-r Hankel matrix is a diagonally scaled Vandermonde in `omega^((s-2)i)`; if `gcd(N,s-2)=1`, it has rank `(N+1)/2` for r=(N+1)/2. Thus the Phase22 bounded-order recognizer cannot accept these inputs when N grows. This is true for the central example `N=3^m`, `s=N/3`: the chirp curvature itself increases with N while exactly **three** Fourier seeds suffice. See `PROOF_CERTIFICATE.md`.

## Exact finite-field operation comparisons

Both compared programs compute the **same N Fourier outputs** with supplied primitive roots. New algorithm and ordinary radix-3 NTT have independently charged root table preparation and online scalar operations. Input fixture generation is excluded from both. Integer/control/addressing work is O(N) and separately noted; the table shows **field operations**, not hardware runtimes.

| N | Fixed s=7 | Wrapped s=N-2 | Coset s=N/3 | Ordinary NTT |
|---:|---:|---:|---:|---:|
| 729 | 18,234 | 17,504 | 12,426 | 16,085 |
| 2,187 | 54,688 | 52,500 | 37,216 | 55,455 |
| 6,561 | 164,043 | 157,481 | 111,579 | 188,138 |
| 59,049 | 1,476,261 | 1,417,211 | 1,003,893 | 2,086,472 |
| **177,147** | **4,428,725** | **4,251,577** | **3,011,573** | **6,849,772** |

The coset method's final field-operation ratio is **2.27448x** versus the particular conventional reference program. This does **not** mean an optimized FFT implementation would be slower, nor establish a universal speedup. The family is recognized and structured; generic inputs still use the ordinary NTT.

A fourth tested class, `s=N/9`, has exactly nine seeds. At N=177147, it uses 5,137,301 field operations versus 6,849,772 for the conventional comparator.

## Independent correctness evidence

- 18 Phase23 unit-test groups pass, including a complete enumeration of eligible chirp residues at small lengths, random dense-input rejection, adversarially forged prefixes, off-root-grid phase parameters, multiple odd/composite lengths, resonance and large coset tests.
- 42 inherited Phase22 tests pass (Jordan, piecewise and parity modes).
- The initial independent Phase23 audit verified all 265,716 outputs across ten sizes, plus 328 directly summed bins and 78 random/adversarial fallback cases; Phase22 fallback was independently confirmed at two sizes.
- The broader coset audit compared **1,062,720 output coefficients** across four strategies and eight lengths (N=81 through 177147) against a separately implemented N-point NTT, in addition to 413 selected directly summed coefficients and 27 random dense-input fallback checks.
- `s=4` one-pole tests include an exactly resonant denominator and independent complete spectrum checks.
- Larger tests included odd composite lengths and primitive-root fields chosen specifically for each length. No floating-point accuracy claim is made.

## What this does NOT solve

This is **not** a universal FFT algorithm. A random dense input usually fails the first two ratio checks or the complete recurrence verification. For a general quadratic chirp parameter s with additive order theta(N) and distance theta(N) from either end, the current seed count grows and the accepted-input O(N) bound is not established. The demonstration falls back to a conventional NTT on such inputs. The bounded-order phase recognition does not compress arbitrary high-complexity coefficient data into a constant-dimensional family.

Our fastest large example uses exactly three direct Fourier evaluations plus N−3 constant-work spectral propagation steps; it never produces the general Fourier operator from an arbitrary vector using this recurrence.

## Novelty and literature

Classical q-holonomic methods and root-of-unity transformations are relevant prior art. In particular, Garoufalidis–Koutschan, *Twisting q-holonomic sequences by complex roots of unity* (2012), and Bostan–Yurkevich, *Fast computation of the N-th term of a q-holonomic sequence and applications* (2022). We have **not** performed an exhaustive historical priority search or independent peer review. The project-specific theorem, source code and audit may be useful for a specialized structured-transform paper after literature comparison, but no priority claim is made.

## Next research gate (Phase 24)

Find a **joint evaluator with fewer than N seeds** when the three-point spectral hypergraph has a generic jump s, without presupposing that its associated input is low-order Prony, low support, periodic or near-periodic. Charge its graph-construction, raw-input recognition, precomputation, simultaneous output decoder and all input/output writes. The cyclic-coset argument gives O(N) when `ord_N(s)=O(1)`; it does **not** show uniform O(N) over all chirps, much less all arbitrary inputs. An appropriate next proof obligation is a bound on the smallest seed set that percolates through the hyperedges `{j,j+4,j+s}` at charged recognition cost. Existing FFT/finite-tensor and q-holonomic prior art must be compared carefully.
