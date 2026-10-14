# Q29 exact sparse reciprocal kernel: bounded full execution

2026-10-14 UTC. Producer computation and implementation-diverse same-author checks; this is not an independent-agent acceptance report.

## Result

The fresh C++ implementation computed exactly

R843(w;z) modulo (25, Phi3375(z), w^100)

in canonical z degree below 1800. The output contains all 100 retained w coefficients, each with 1800 coordinates in Z/25Z: exactly 180,000 bytes, each in 0,...,24.

- File: `R843_w100_mod25_zbasis.bin`
- SHA-256: `ebf51150ffbed6e87f3e08875451176963670801c59ffd9128336a02c43ca38c`
- Encoding: coefficient at w^k z^j is byte offset 1800*k+j, for 0<=k<100, 0<=j<1800.
- Nonzero coordinates: 172,968.
- Kernel: 0.473105316 seconds wall, 0.471766 seconds CPU.
- Preparation (maps and buffers): 0.001919247 seconds wall.
- Binary writing: 0.002805758 seconds wall.
- Whole production executable process, including launch: 0.481710282 seconds wall.

These timings are single-machine observations, not complexity or FFT-speed theorems. The saved small trials show timing variation. Very short CPU intervals have coarse accounting: the production clock reported zero preparation CPU and 0.004 seconds writing CPU. Do not interpret the zero as no preparation cost.

No conversion to the alpha/pi basis, no full raw U jet transformation, and no normalization by pi^60 was executed. No discriminant value or nonvanishing result is claimed.

## Exact arithmetic and fused recurrence

The ring is C2=(Z/25Z)[z]/Phi3375(z), with

Phi3375(z)=z^1800-z^1575+z^1125-z^900+z^675-z^225+1 = Phi15(z^225).

Let S_t denote multiplication by z^t. With P=R_(m-1), Q=R_(m-2), R_0=1 and R_(-1)=0, the prescribed recurrence is

R_m = (w-2+z^(2m)+z^(2m-1))*P - (1-z^(2m-1))*(1-z^(2m-2))*Q.

The implementation forms

D = Q-S_(2m-2)Q,
T = P+S_1 P+D,
R_m = wP-2P-D+S_(2m-1)T.

Expanding -D+S_(2m-1)D gives -Q+z^(2m-2)Q+z^(2m-1)Q-z^(4m-3)Q; expanding S_(2m-1)(P+S_1 P) supplies the two required P terms. This verifies the fused formula directly. Fresh formal-polynomial checks cover m=1,2,3,17,843, including the coincident exponent at m=1.

The production map uses eight blocks of 225 canonical z coefficients. Each monomial shift splits a block into two contiguous slices, then uses the exact integer reductions of y^0,...,y^14 modulo Phi15(y), where y=z^225. The identity z^3375=1 holds in the target ring. All additions and subtractions retain integer carries before canonical reduction modulo 25; no characteristic-5 Frobenius shortcut is used.

The maximum signed row l1 norm is six. Canonical inputs are in 0,...,24, and the staged accumulators have absolute magnitude at most 216, safely within signed 16-bit range. Scalar multiplication by two is also safe. The shift routine rejects any unexpected reduction-map coefficient outside +1/-1. Truncating at w^100 is exact because the recurrence never decreases w degree.

## Verification before timing

`verify_and_benchmark.py` uses standard Python modules and fresh control code. It compiles the fresh production source with `g++ -O3 -std=c++17 -Wall -Wextra -Werror`.

For every m=0,...,8 at q=z and q=z^1001:

1. Construct the entire Gaussian-binomial row over unreduced integer q-polynomials by its defining Pascal recurrence.
2. Divide H_(2m+1)(x;q) exactly by 1+x over those integer polynomials.
3. Independently reduce substituted q powers by descending monic Phi3375 division, without using production block maps or the period shortcut.
4. Reconstruct U from the computed R using the integral identity

   U_(2m+1)(x;q) = sum_(k=0)^m r_(m,k)(q) x^(m-k)(1+x)^(2k).

5. Compare every coefficient, then compare separately executed w truncations at limits 1, min(2,m+1), and min(4,m+1).

All 18 cases and all truncations pass. The independent remainder code also verifies Phi3375 divides z^3375-1. See `CONTROLS.json`. These are independent algorithms implemented by the same author, not an independent reviewer's acceptance.

## Measured budget gate

Three repeats were measured for each small case. Kernel wall intervals:

| m | w limit | Minimum seconds | Maximum seconds |
|---|---:|---:|---:|
| 32 | 8 | 0.001116501 | 0.001194015 |
| 64 | 16 | 0.004467504 | 0.004713248 |
| 128 | 32 | 0.017855124 | 0.018559304 |
| 192 | 48 | 0.040667545 | 0.046305679 |

The driver independently enumerated exact full-run work counts:

- Signed sparse-scatter coordinate updates: 849,703,500.
- Counted dense arithmetic updates: 571,320,000. This category counts T's addition and N's doubling/two subtractions; it does not count loads, stores or loop control.
- Canonical modular reductions: 428,488,200.

The empirical admission estimate used the worst observed per-counted-update time from all twelve small runs, multiplied by eight, plus five seconds for startup/writing. It estimated 9.238624797 seconds wall and 9.377832524 seconds CPU. At admission, 178.4206 wall seconds and 118.4026 CPU seconds remained in the primary budget. Thus the full run was admitted only after measured controls and budget checks passed. The estimate is a conservative heuristic with hard runtime enforcement, not a guaranteed timing bound.

The production driver completed compilation, controls, timing trials, exact gate enumeration and full execution in 2.082052624 wall seconds; charged parent+child CPU was 2.100132948 seconds. Peak child RSS was 88,648 KiB, including compilation. The primary run used a 180-second external timeout, a total 120-second charged-CPU admission envelope with per-process remaining-CPU limits, and 512 MiB per-process address-space limits. All measurements and commands are in `EXECUTION_RECEIPT.json`; the saved pre-full checkpoint is `bench_m192_w48_r2.bin`. Python's light controller bookkeeping is not an operating-system aggregate CPU cgroup; the actual observed aggregate CPU is nevertheless far below the hard limit. No claim is made that this wrapper would enforce an aggregate parent+children CPU limit under arbitrary modified code.

## Full implementation-diverse comparison

After the production result, the fresh `cyclic_expanded_control.cpp` computed the expanded original recurrence in

(Z/25Z)[z]/(z^3375-1), truncated at w^100.

This checker uses cyclic rotations in a 3375-coordinate array. It does not use the fused D/T formula, Phi15 block maps, or in-kernel cyclotomic reduction. Only after m=843 does it perform descending monic reduction by Phi3375. Since Phi3375 divides z^3375-1, the quotient map sends every operation to the same target-ring operation.

A small m=8, w<9 comparison passed before the full comparison. Its measured admission estimate (eightfold scaled small timing plus five seconds) was 8.528561214 seconds. The full larger-ring kernel took 0.511629601 seconds wall; final monic ring reduction took 0.001359460 seconds; preparation took 0.000472508 seconds; writing took 0.001425087 seconds. All 180,000 reduced bytes match the production result exactly, with the same SHA-256.

The successful verification driver, including compilation, took 1.094386945 wall seconds and 1.091393 child CPU seconds. Peak child RSS was 91,580 KiB, including compilation. It ran under a 60-second external timeout, per-child 30-second CPU and 512 MiB address-space limits. Together with the primary work, the actual observed execution is comfortably within 180 wall seconds, 120 CPU seconds and 512 MiB. The interval between commands included report preparation; the timings above describe computation, not assistant response latency.

The first checker compilation failed only on a `-Werror=misleading-indentation` warning in its output loop. Braces fixed the formatting, after which compilation and every mathematical comparison passed. The initial source and stderr are retained as `cyclic_expanded_control_initial.cpp.txt`, `cyclic_compile_initial.stderr`, and `independent_driver_initial.stderr`. The failed compiler command took 0.522132172 shell-observed wall seconds; a separate failed-compile CPU measurement was not retained. Do not silently omit this failed attempt from audit history.

## Precision and scope

The supplied exact representation identifies z=q, alpha=z^1000, beta=z^2376 and pi=beta-1. C2 is isomorphic to the stated mixed-characteristic B2 and has absolute coefficient precision 200 in pi valuation. This file is still stored in the z basis, not the valuation-readable alpha/pi basis.

By the established integral identity

U1687(-1-v;q) = sum_(k=0)^843 (-1)^(843+k) r_(843,k)(q) v^(2k)(1+v)^(843-k),

the retained R coefficients determine the raw U jet v<200. That transformation has not been materialized here. To claim the normalized F=pi^-60 U1687(-1-pi Y;q) modulo pi^140 still requires the basis conversion, exact integral transformation, and guarded normalization with its precision accounting. None of those later computation gates is claimed complete. Coefficients w^100,...,w^843 are absent. In particular, the result does not evaluate Disc R843, certify its nonvanishing, or settle any residual repeated branch.

## Reproduction and provenance

Run from this directory:

    python3 verify_and_benchmark.py
    python3 verify_full_independent.py

The first script recompiles the production code, runs its controls and gate, and executes the full case only if admitted. The second recompiles the cyclic checker and compares all full output bytes. Timing-bearing JSON will naturally differ between machines and reruns; output coefficient hashes must agree.

Source inputs were read as inert text only: `q29_precision_contract/PRECISION_CONTRACT.md` and `sparse_execution_design/SPARSE_EXECUTION_CONTRACT.md`, plus inspection of its control definitions. No historical scientific program was imported or executed. No networking, account change, repository write, upload, table edit or ranking change was performed by this producer study. The only child processes were local compilation/execution and bounded execution wrappers. The source files, compiler binary, receipts and all coefficient checkpoints are covered by the final manifest. `SEAL.json` identifies the manifest hash without creating a circular hash dependency.
