# FFT Green graph reuse — recovery through Phase 34

**Main goal:** a new exact arbitrary-input FFT with a genuine cost advantage; no such algorithm has yet been proved by this project. Preserve the original graph-reuse/nonunitary Green direction, distinct from CrocSwap/OpenAI integer multiplication.

The working directory is `fft_green_phase34_lowrank_products/`:
- Start with `CHECKPOINT.md` for today's theorems and the exact Phase 35 target.
- Use `THEOREM.md` for the full proofs, assumptions and caveats.
- Run `python -m unittest -v tests_phase34` and `python phase34_products.py`.
- Open `previous_full_phase33_checkpoint.zip` to recover Phases 12–33 and all the former code, tests and documents.

**New mathematical result:** A product of t closely related Green-sum stages with inverse-correction rank budget R and base denominator row-sparsity d cannot be the exact length-N Fourier transform unless `R >= floor(N/(d^t+1))`. This is an architecture-specific sparse-inverse-plus-low-rank theorem, not a universal FFT lower bound.

**New constructive diagnostic:** The correction rank for a two-cycle Green sum sharing one coupling equals `N - number_of_cycles(W0^-1 W1)`, computable from permutations in linear time.

**Next phase:** Genuine rank-distant non-affine Green-product designs whose internal phases satisfy both Weyl relations, with no hidden precomputation and all operation/precision costs exposed.
