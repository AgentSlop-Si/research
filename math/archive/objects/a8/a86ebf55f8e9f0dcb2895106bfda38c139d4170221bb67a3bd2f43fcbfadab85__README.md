# Hero #1 — Phase 29: All-input noncoprime 120-point FFT fusion

**Main exact result:** for `N=120h`, `h=2^t`, the complete charged prime-field arithmetic network needs

`T29(N) = 180h*t + 1163h + 15`

operations, against `T28(N)=180h*t+1176h+15` at the same length. Saving: **13h arithmetic operations on every input** (43h multiplications saved at the cost of 30h extra additions). In both tested prime fields and in characteristic zero the 120-point short kernel costs **1,038 additions plus 140 nonidentity scalar multiplications**. Cold setup introduces 57 more operations; net cold saving **13h−57**, positive from `N=960`.

**Verification:** 28 new and retained tests, exact characteristic-zero polynomial checks, 2,448,000 distinct basis-matrix entries independently compared against closed-form Fourier values through three implementations (7,344,000 exact comparisons), and exact finite-field benchmarks through `N=61,440` in two primes.

**Research limits:** the short transform is classical Winograd/Good–Thomas architecture, no claim of historical novelty. The restricted gauge and weighted-four theorems give mathematically audited negative research gates. Full complexity remains **Θ(N log N)**. No stable floating-point, bit complexity, best-known FFT or practical wall-clock claim.

Start with `THEOREM.md`, `COST_LEDGER.md`, `NEGATIVE_GATE.md`, `NEXT_GATE.md`, and `RUN.md`. The original Phase 28 checkpoint is nested unchanged as `PRIOR_PHASE28_COMPLETE.zip`.
