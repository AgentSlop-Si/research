# HERO #0 — Phase 24 continuation checkpoint

**Date:** October 10, 2026. **Phase 23 verified.** Main objective remains an input-independent sequential exact FFT for arbitrary fresh inputs with fully charged `O(N)` or `O(N log log N)` complexity. **Still not achieved.**

## Preserve and do not repeat

1. Phase22: fixed complementary Green backgrounds cannot be repaired by retuning the other four terms at the saved N=16/64/256 instances; many generic and real backgrounds excluded at all square lengths. Phase21 Hessian span does *not* imply finite reachability.  
2. Phase23: fully complex, simultaneously adjustable horizontal/vertical rook factors satisfy **two** necessary Schur-rank gates, each `rank(A) rank(B) >= s-2` across every off-rook Fourier block. This is new-to-project, not an arbitrary FFT lower bound.
3. If either crossed pair has uniform transverse rank product `rho <= s-3`, the relative Frobenius Fourier error is >= `sqrt(1-(3+rho)/s+1/s^2)`. Complex homogeneous Green kernels have rho=1, hence cannot match Fourier at any s>=4 and error tends to 1.
4. Each crossed pair needs at least `ceil(s² max(m(s)-2,0)/(s-1))` nonreal **effective matrix entries**, with `m=floor((s-1)/2)` for odd s and `m=(s-2)/2` for even. Both pairs separately need this. One complex Green edge can influence many effective entries, so do NOT relabel this as a lower bound on independent edge weights.
5. All tests pass (17 Phase23 + 88 inherited); `audit_phase23.py` regenerates exact GF65537 and numerical certificates. True Green cyclic resolvents verify the rank obstruction for s=4,8,16. Fully complex fiber-varying low-separation-rank examples checked for s=8,16,32.

## Phase24 constructive target

**Do not add more sparse/real/low-rank restrictions.** Attack *high-transverse-rank* two-layer mixed-axis Green networks, where both Schur rank-product conditions are satisfied. The complete nonlinear equation is

`F[(x,y),(a,b)] = YV[(x,y),(x,b)] XH[(x,b),(a,b)] + YH[(x,y),(a,y)] XV[(a,y),(a,b)]`  for `x!=a,y!=b`.

A useful next gate is a **joint tensor-completion / polynomial-elimination** certificate, treating both paths as unknown and retaining on-rook constraints. Start at `s=4`, N=16, over `GF(65537)` with genuine Green cycles and singular branches separated. The unrestricted two-rook-matrix superset should be used as a control before restricting to Margulis Green parameters.

**Acceptance test for breakthrough:** an exact factorization `F_N = T_L...T_1` for a uniform infinite family, with deterministic synthesis of parameters and all complex arithmetic/precisions/precomputation charged; or a rigorous all-size exclusion of a well-defined proposed architecture. A finite root of an approximate optimizer is not enough.

## Reproduction

```
cd fft_hero0_phase23_dual_bridge
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase23
OPENBLAS_NUM_THREADS=1 python audit_phase23.py
cd fft_hero0_phase22_bridge_elimination
OPENBLAS_NUM_THREADS=1 python -m unittest -q test_phase19 test_phase19_tuning test_phase20 test_phase21 test_phase22
```

Read `THEOREMS.md`, `RESULTS.json`, `phase23_dual_phase.py`, `test_phase23.py` and `PROVENANCE.md`. Previous full Phase22 archive is included as `prior_phase22_bundle.zip`.

Final test correction: **17 Phase23 test methods**, not 16, plus 88 inherited = 105. The additional test assembles and checks actual complex cyclic Green resolvents at grid sides 4,8,16.
