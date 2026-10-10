# Sparse-surrogate / structured-sketch FFT frontier checkpoint — 2026-10-09

## Main goal
Fresh arbitrary dense input, all N Fourier outputs, asymptotic speedup derived from our own sparsification / structured-sketch mechanism. Do not use OpenAI #130, CrocSwap, or Swapnil-jain as the source of the speedup.

## Established theorem branch
For unitary DFT U_N and fresh x in C^N, importance-sample coordinates with p_j=|x_j|/||x||_1 to form a k-sparse unbiased surrogate y.

Universal simultaneous guarantee:

  ||U_N y - U_N x||_inf <= eps ||x||_1 / sqrt(N)

with failure <= delta for

  k = O(eps^-2 log(N/delta)).

Using the current input-pruned full-output transform gives

  O(N log(k+2))
  = O(N[log(1/eps)+log log(N/delta)]).

Head/tail sparsification improves k for compressible inputs. A perturbed-identity rank argument gives k = Omega(log N /(eps^2 log(1/eps))) on flat worst-case inputs even for arbitrary complex sparse weights, so k=Theta(log N) for fixed eps is essentially optimal inside the time-domain sparse-surrogate model.

## Strongest exact linear-decoder primitive found
For N=K M, a global quadratic-chirp block sketch was derived. With random odd a and beta,

  sigma_n = exp(2*pi*i*(a*n^2 + beta*n)/N).

Block summaries plus a q-difference recurrence decode all N outputs with:

- one K-point FFT;
- O(N) recurrence work;
- exact agreement with materializing the sketched signal and a reference FFT (observed ~1e-13 to 2e-12 numerical error).

Choosing M=Omega(log N) makes K log K = O(N), so one sketch is true O(N).

Artifacts:
- quadratic_global_block_sketch.py
- global_chirp_concentration_results.json
- global_chirp_scaling_results.json
- global_chirp_logblock_results.json

## Negative result 1: block-projection variance
For any estimator that independently projects each length-M block onto one random orthonormal local vector and rescales to be unbiased,

  E ||x_tilde - x||_2^2 = (M-1)||x||_2^2.

Averaging L independent sketches divides this by L. Thus this whole local one-mode projection family needs Omega(M) sketches for uniform constant relative RMS error. With M=Theta(log N), total cost returns to Omega(N log N).

## Negative result 2: recursive chirp decoder
Replacing the remaining K-point FFT recursively by the same global chirp sketch gives formal T(N)=O(N)+T(N/M)=O(N), but approximation error compounds badly. At N=1024, even four recursive trees had max-error/||x||2 roughly 0.56--0.76 on dense cases, and worse on sparse inputs. Abandon current recursive version.

Artifact: recursive_chirp_fft.py

## Negative result 3: multifactor averaging / median
Changing factorizations changes alias-comb geometry, but neither averaging nor coordinatewise complex median gave a universal constant-sketch fix.

At N=15015 across multiple coprime (K,M) splits:
- flat/global-mode inputs remained ~0.5--1.0 l1-scale error even with 8 averaged factorizations;
- median remained ~0.82--1.0 for flat/global-mode with 7 factorizations;
- sparse-ish inputs remained especially poor on the strong ||x||_1/sqrt(N) target.

Artifacts:
- multifactor_affine_results.json
- multifactor_median_results.json
- multifactor_affine_test.py
- multifactor_median_test.py

## Negative result 4: two-stage composition
Tested:

  dense x -> k-sparse importance-sampled y -> L affine-chirp O(N) sketches of y.

N=64*257=16448, k in {128,256,512}, L in {1,2,4}.

Stage 1 remained good (median l1-scale errors ~0.13--0.28), but stage 2 dominated:
- dense cases: stage2 median ~1.05--3.3 even at tested k,L;
- sparse-ish: stage2 median ~2.46--4.83.

Core reason: for a fixed stage-2 linear sketch A,

  E_y[A y | A,x] = A x,

not x. Therefore stage-1 unbiased randomization cannot remove a coherent stage-2 bias; as k grows, y converges toward x and the original stage-2 failure returns.

Artifact:
- two_stage_linear_test.py
- two_stage_linear_results.json

## Useful variance identity behind stage-2 failure
Within one length-M block, the chirp projection is P = v v^* with ||v||_2^2=M and E[P]=I. Therefore

  P^2 = M P,
  E ||(P-I)z||_2^2 = (M-1)||z||_2^2.

This identity is independent of whether z is sparse. Stage-1 sparsification changes z but does not eliminate the local projection variance/bias geometry.

For the importance-sampled surrogate y=(1/k) sum Z_s with E Z_s=x and E||Z_s||_2^2=||x||_1^2,

  E||y||_2^2 = (1-1/k)||x||_2^2 + ||x||_1^2/k.

Hence a block-projection second stage has large expected energy error on flat inputs unless enough independent stage-2 sketches are used.

## Current live frontier
The unresolved primitive is still rectangular Fourier evaluation:

  X_m = sum_{s=1}^k a_s omega_N^(j_s m),  m=0,...,N-1,
  k=Theta(log N) for fixed strong l_inf / (||x||_1/sqrt N) accuracy.

Current exact/pruned method costs O(N log k)=O(N log log N).

No standard lower bound located so far forces Omega(N log k); obvious Fourier circuit bounds only force about N + Omega(k log k). Therefore O(N) worst-case evaluation is not ruled out.

Equivalent forms:
1. evaluate a k-term exponential sum at all N roots of unity;
2. generate first N terms of an order-k linear recurrence whose characteristic roots are Nth roots of unity;
3. expand rational generating function P(z)/Q(z), Q(z)=prod_s(1-z_s z), for N coefficients.

The next research should focus on whether the roots-of-unity structure of Q permits an O(N) block recurrence / word-level algorithm unavailable for generic short convolution. Do not return to #130/CrocSwap/Swapnil finite-certificate machinery.
