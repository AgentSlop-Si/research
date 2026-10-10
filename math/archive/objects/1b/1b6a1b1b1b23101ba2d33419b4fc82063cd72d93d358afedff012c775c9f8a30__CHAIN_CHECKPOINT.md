# RECOVER HERE — Hero #17 Delta-Graph / Spectral Newton Union

**Date:** 2026-10-10. **Main goal unachieved:** no exact O(N) transform for every fresh arbitrary N-vector. The newest methods are exact, deterministic, **raw-input conditional O(N)** algorithms for a larger structured family. No external novelty or stable-float claim.

## Code to continue

- **`newton_union.py`** — strongest general result. For balanced N=QM and fixed order d, all first d polyphase fibers may be arbitrary dense, while the total number R of length-M Fourier modes in the subsequent d-th backward differences is O(Q). Full exact DFT in O_d(N+d*M²+M*(Q+R)+Q*R). The recognizer discovers the structure from the raw input. It supports any fixed d; test covers 1–4.
- `delta_graph_budget.py` — special d=1, **global** Fourier-change budget instead of fixed r per row. A single fully dense M-mode difference is allowed when R>=M=Theta(sqrt N), fully charged O(N).
- `delta_graph.py` — special d=1 with fixed per-difference mode cap and optionally a constant number of arbitrary dense resets.
- `second_difference_graph.py` — special d=2, arbitrary first two dense fibers and sparse second differences. d=1 can reject a full-rank dense example that d=2 recognizes.
- `graph_convolution_delta.py` — augments old sparse-fiber graph convolution with low temporal-difference output reconstruction; rescues previous adversarial S=Q^(3/2) state graph when D=2sqrt(Q)-1.
- Inherited previous Hero #17 source modules are bundled for reproducibility, and all prior 27 tests are included.

## Essential mathematics

For row spectra C_t[h], and z=omega^(-(h+sM)):

`F_N(x)[h+sM]=sum_t z^t C_t[h]`.

For d-th spectral difference E_a at time a and initial Newton spectral coefficients A_j[h]:

`F_N(x)[k] = sum_(j<d) A_j[h]*z^j*B_(j+1,Q-j)(z) + M sum_(event a,h,c) c*z^a*B_(d,Q-a)(z)`.

`B_(d,L)(z) = [1-z^L sum_(j<d) binom(L+j-1,j)(1-z)^j]/(1-z)^d` for z!=1; at z=1 it equals `binom(L+d-1,d)`.

**Critical implementation trap fixed:** every `z^L` inside output loops MUST come from the root phase table. Python `pow(z,L,p)` inside the output loops silently multiplies the work by log N. `newton_union.py` supplies precomputed z^L in every call. One batch inversion builds all reciprocals in O(N)+one inversion.

## Tests verified

- `python -m unittest discover -q -p 'test_*.py'` => **51 passed** (27 old + 24 new).
- `python independent_audit.py` => **361 independent full transform checks**, **91,608 exact DFT bins**, **300 random rejects**, **2 rescued convolution adversaries**, order 1..4 including odd composite N, plus large N=65536 37-bin spot check.
- Full N=4096 graph convolution independently equals reference radix-2 NTT in `test_delta_graph.py` (the NTT is TEST-ONLY).
- `AUDIT_RESULTS.json`, `tests.log`, `independent_audit.log` reproduce findings.

## Next research target

Dense unrelated d-th differences: R=Theta(N) regardless of fixed d. This method then pays Q*R, so the **universal hard core is a joint evaluation of all high-entropy dense Fourier channels**. Need a uniform, explicit and fully charged new arithmetic graph. The restricted support count is at most `p^(dM)*sum_{e<=R} binom((Q-d)M,e)(p-1)^e`, a negligible fraction `p^(-N+O(sqrt N))` for R=O(Q). Do not confuse maximal ordinary matrix rank with information-theoretic input coverage.

## Avoid repeated or false claims

Do not present low spectral *variation* as universal high-entropy input coverage. Do not replace the online short DFT with an uncharged FFT. Do not treat the known #130 construction, CrocSwap, kappa, cached inputs, threading, full-state lookup or quantum amplitude readout as a new success. No all-input O(N) result, integer multiplication theorem, bounded-coefficient theorem or originality certification in this package.
