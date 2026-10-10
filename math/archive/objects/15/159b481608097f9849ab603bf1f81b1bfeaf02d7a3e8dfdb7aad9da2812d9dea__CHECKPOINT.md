# RECOVER HERE — Phase 24 (2026-10-09)

**Status:** The stable-binary-sorting / reordered-covariance issue is now mathematically quantified. New theorems and exact modular constructive control. **No worst-case sub-`N log N` Fourier algorithm.**

## Proven, checked achievements

1. Let `P` be stable binary sort and `W=P^-1 ZP`. If `T` is the number of noncyclic bit transitions, then `rank(W-Z)=2 floor(T/2)` over any field. Exact proof via a single nontrivial cycle in `Z^-1 W`; exhaustive all `2^N` binary words `N=2..16`.
2. For iid fair binary bits, exact law `P(rank=2k)=binom(N,2k+1)/2^(N-1)`; `E rank=N/2-1`, `Var rank=N/4`. Exhaustive counts confirmed.
3. Stronger: simultaneously for every stride `a=1..N-1` (including non-coprime `a`), `rank(W-Z^a)>=N/8` with probability `1-o(1)`. Explicit Hoeffding/union-bound guarantee in `THEOREM.md`; random all-stride audits through N=4096. This blocks perturbative cyclic-spectral Green shortcuts for **uniform random binary data**, not all possible Green architectures.
4. Positive constructive side: if `s` successor edges change relative to standard `Z`, an exact modular Woodbury solver for `C P^-1 g(z)` takes `O(Ns^2+s^3)` field work and `O(Ns+s^2)` memory, yielding linear work for fixed `s`. Random binary stable sorting instead has `s=Theta(N)` typically. One/two swaps, identity and one-run controls matched the independent Phase23 FFT reference.

## What NOT to repeat

- Claim that sorted input's sparse cyclic differences imply fast Fourier output in the *original* coordinate order.
- Claim that rank relative to standard `Z` alone rules out all stride choices: an alternating binary string makes `W` close to `Z^2`, even while far from `Z`.
- Treat modular field operations or inversions as free bit operations; or treat a generic near-resonant complex Green inverse as numerically stable.
- Apply Woodbury with a rank growing linearly in N and then call the algorithm linear.
- Claim an arbitrary-input `o(NlogN)` FFT from exact finite tests or from a fixed finite alphabet.

## Next constructive gate (Phase 25)

The high-probability rank theorem excludes **only cyclic-reference low-rank corrections**. Continue to genuinely **independent, noncommuting coordinate orders**, with a representation that does *not* need `Theta(N)` Woodbury channels. A concrete candidate to test is a *multiresolution sparse conjugated-shift factorization*, enforcing the **same** exact real covariance `MZ=R M` and seed `Me0=v` while measuring every intermediate solve and permutation. Compare direct exact modular residual outputs and try to prove a uniform operation bound. Also investigate whether a different noncyclic sparse reference has small deviation rank on binary stable shuffles, rather than assuming it does.

## Reproduce

`cd fft_green_phase24_ordering_defect && python -m unittest discover -s tests -v && python audit.py`

For full lineage, unpack `previous_full_phase23_checkpoint.zip` and run its `verify_full_lineage.py` with that archive. The Phase24 packaging includes a self-contained copy of Phase23's tested executor and a full nested historical archive.
