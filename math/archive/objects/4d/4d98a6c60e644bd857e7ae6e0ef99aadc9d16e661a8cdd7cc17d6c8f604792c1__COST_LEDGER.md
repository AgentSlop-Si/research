# Phase 28 — Fully paid field-arithmetic ledger

Transform family: `N=60H`, `H=2^t`, exact roots over `F_p`; both tested primes `2013265921` and `754974721` support the listed lengths. Entries below were reproduced by **executing** all three Python algorithms and cross-checking their outputs. Nonidentity scalar field multiplications cost one, even when the scalar is `±i`. Index arithmetic and word traffic are not conflated with field operations.

## Scalar graph

| Component | Additions | Multiplications |
|---|---:|---:|
| 60 length-`H` dyadic transforms | `60 H t` | `30 H t−60H+60` |
| Internal `(4,H)` CT twiddles | 0 | `45(H−1)` |
| `H` fused WFTA60 kernels | `444H` | `69H` |
| **Total** | **`60Ht+444H`** | **`30Ht+54H+15`** |

The Phase 27 comparison uses identical dyadic radix-2 arithmetic and output convention:

`C_27=90Ht+544H+15`; `C_28=90Ht+498H+15`; difference = `46H` exactly.

The intermediate 15-only nesting costs `90Ht+512H+15`; the extra gain from joint 60-point fusion is `14H`.

## Cold one-shot model

Root setup and the original Winograd 3-/5-point constants are inherited without modification from the Phase 27 `make_plan()` and counted in the benchmark JSON. `make_wfta_plan()` adds 10 scalar coefficient products and two coefficient additions = 12 operations. `make_fused60_plan()` adds another 17 scalar coefficient products = 17 operations. Total additional cold preparation: 29 operations. Exact cold saving **against the particular Phase 27 plan**: `46H−29`.

### Selected benchmark rows

| `N` | Phase 27 warm | Nested 15 warm | Nested 60 warm | Saving versus Phase 27 | Cold saving |
|---:|---:|---:|---:|---:|---:|
| 60 | 559 | 527 | 513 | 8.23% | 2.71% |
| 480 | 6,527 | 6,271 | 6,159 | 5.64% | 5.12% |
| 1,920 | 31,823 | 30,799 | 30,351 | 4.63% | 4.51% |
| 15,360 | 323,599 | 315,407 | 311,823 | 3.64% | 3.62% |
| 61,440 | 1,478,671 | 1,445,903 | 1,431,567 | 3.19% | 3.17% |

Full arithmetic, setup, plan/root size, and independent correctness flags are in `BENCHMARK_PHASE28.json`.

## Exclusions and warning gates

- `O(N)` CRT input/output permutation, integer modular indexing, and memory traffic are **real costs**. They are excluded from *field arithmetic*, not claimed to be free in a practical implementation.
- An external primitive root or a proven root-supply procedure is required. `make_plan` counts field powering/tables but does not include a formal primality proof or arbitrary-index word-size cost.
- The finite prime-field operations may have `O(log^2 p)` or greater bit cost, not automatically unit-time on ordinary hardware.
- Exact symbolic identities extend to complex arithmetic, but do **not** prove a numerically stable floating-point algorithm. No wall-clock benchmark is claimed.
- This is not a comparison with the fastest known NTT/FFT library; it is a fair internal comparison of two explicitly expanded circuits.
- The phase-28 60-point WFTA closely follows established prior art, and does not improve the asymptotic `Θ(N log N)` work.
