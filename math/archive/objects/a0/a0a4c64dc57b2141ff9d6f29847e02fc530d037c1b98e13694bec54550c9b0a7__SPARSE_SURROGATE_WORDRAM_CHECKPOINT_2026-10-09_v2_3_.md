# Sparse-surrogate Word-RAM FFT checkpoint v2 — 2026-10-09

## Main goal
Fresh arbitrary dense input, all N approximate Fourier outputs, with the asymptotic speedup coming from our own sparsification + finite-state lookup mechanism. Do not use OpenAI #130, CrocSwap, or Swapnil-jain as the source of the speedup.

## Established upstream approximation
For the unitary DFT U_N, importance-sample a fresh dense input to a sparse surrogate. Previous complex-magnitude sampler gave

  ||U_N y - U_N x||_inf <= eps ||x||_1 / sqrt(N)

with failure <= delta and k = O(eps^-2 log(N/delta)).

## Latest simplification: split real/imaginary mass
Instead of sampling coordinates proportional to |x_j| with arbitrary complex weights, define

  L_box(x) = sum_j (|Re x_j| + |Im x_j|).

Sample from 2N signed real/imag atoms:

  +e_j, -e_j, +i e_j, -i e_j

with probability proportional to the corresponding positive mass |Re x_j| or |Im x_j| and sign/phase carried by the atom.

Each Monte-Carlo sample therefore has exactly the same magnitude L_box(x)/k. The surrogate is unbiased:

  E[y] = x.

For every normalized Fourier coefficient, one sample contribution has magnitude L_box(x)/(k sqrt(N)). A Hoeffding/union-bound argument therefore gives a simultaneous guarantee of the same form

  ||U_N y - U_N x||_inf <= eps * L_box(x)/sqrt(N)

with k = O(eps^-2 log(N/delta)). Since L_box(x) <= sqrt(2)||x||_1, this differs from the old l1 bound only by a constant while making the descriptor alphabet finite and simple.

## Why this helps the Word-RAM lookup path
A sampled atom now needs only:

- time index j;
- one 2-bit phase/sign in {+1,-1,+i,-i};
- quantized phase information for the current output block.

There is no arbitrary complex sample weight to encode.

## Live two-level direct phasor table idea
Process output frequencies in blocks of B = Theta(log N) bins.

For each sampled atom j and output block starting at m0, its B-lane normalized Fourier contribution is a unit phasor trajectory

  s * (omega_N^(j(m0+t)))_{t=0}^{B-1},  s in {+1,-1,+i,-i}.

At fixed accuracy, quantize:

- block-start phase;
- slope phase omega_N^j;
- first-level group-average lanes;
- second-level lane sums.

Relevant bits per atom descriptor are p = O(log B + log(1/eps)) = O(log log N + log(1/eps)).

Choose first-level group size

  g = Theta(log N / p)

so one group key uses at most gamma log N bits for a fixed gamma<1. Hence first-level table has N^gamma * polylog(N,1/eps) entries and is sublinear for fixed eps.

The k = Theta(eps^-2 log(N/delta)) sampled atoms form

  G = k/g = O(eps^-2 p)

groups. For fixed eps, G = O(log log N).

A first-level lookup returns a quantized B-lane average trajectory for one group. Round each lane to a small alphabet A1 of size poly(1/eps). A second table maps the G first-level symbols for one lane to their final quantized average. For fixed eps, its key width is O(G log |A1|)=O(log log N), so the second table is polylogarithmic in N.

## Deterministic decoder error budget already derived
The two-level table decoder has additive error

  decoder_error <= (eta_phase/2 + h1/sqrt(2) + h2/sqrt(2)) * L_box(x)/sqrt(N)

where eta_phase is the phase quantization error and h1,h2 are first- and second-level rounding steps.

Allocate, e.g., eps/4 to Monte-Carlo sampling and the remaining 3eps/4 to phase/rounding to obtain a total all-bin guarantee.

## Online complexity target
There are N/B output blocks.

- fresh-input scan + sampling: O(N) word operations;
- first-level group lookups per output block: G = O(log log N) for fixed eps, but the B-lane output of each lookup is packed into O(B*p/w) words with word size w=Theta(log N);
- with B=Theta(log N), p=Theta(log log N), one packed B-lane vector occupies O(log log N) words;
- naive G lookups times packed output words would be O(N (log log N)^2 / log N) = o(N);
- second-level lane aggregation can be tabled in packed form; target is O(N/log N * polyloglog N)=o(N);
- final unpack/write of N outputs is O(N).

Therefore the intended total online cost is O(N), dominated by the mandatory input scan and output materialization.

## Crucial open obligations
1. Write the packing/transposition argument rigorously: prove all block-key construction, packed lane extraction, table-output accumulation, and final unpacking are O(N), not hidden O(N log log N).
2. Fully charge first-table construction: show N^gamma polylog(N)=o(N) time and memory for fixed eps.
3. Fully charge second-table construction: polylog(N) time/memory for fixed eps.
4. Integrate the Monte-Carlo + phase quantization + first/second rounding errors into one theorem.
5. Define exact word-RAM model: word size Theta(log N), integer/bit operations O(1), table lookup by one word key O(1), fixed-point lanes packed across O(log N)-bit words.
6. End-to-end prototype on flat, Gaussian, random-phase, power-law, spike/noise inputs.
7. Prior-art audit against Four-Russians/finite-alphabet FFT/WHT results; do not claim novelty until this is done.

## Important negative branches already closed
- shared/local chirp linear decoder: coherent adversarial error;
- block one-mode projection: variance forces Omega(M) sketches;
- recursive chirp decoder: error compounds;
- multifactor averaging/median: coherent combs remain;
- sparse-surrogate -> biased linear chirp decoder: stage-1 unbiasedness cannot remove stage-2 bias.

## Exact next step
Formalize and prototype the packed two-level lookup decoder using the signed real/imaginary atom sampler, and prove the full O(N) word-RAM + eps L_box/sqrt(N) guarantee with all preprocessing charged.
