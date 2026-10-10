# Global intermediate-state bottleneck for fresh exact FFTs

**Research date:** 2026-10-09  
**Status:** Two elementary, scope-limited all-length theorems, exact implementation/audit, and a deliberately misleading single-bigint-multiply control. **No new O(N) exact FFT algorithm. No novel lower bound for unrestricted FFT circuits.**  
**Task:** one fresh input; complete explicit N-value FFT output; one logical processor; all arithmetic and coefficient/representation costs charged. No related-input cache, no output subsets, no uncharged table, no GPU/threads.

## 0. Original hypothesis and previous-work gate

Our work asks whether global computation-sharing, growing with N, could reduce the full FFT of arbitrary fresh data to O(N). Prior phases ruled out exact subtree collisions, short annihilator sparsification for random inputs, implicit Fourier descriptors as explicit output, scalar Galois-orbit decoding, simple chirp-kernel recurrences, Boolean degree-two tricks, and binary-only low-degree spectral completion. The most recent `fft_joint_orbit_stability/RESEARCH.md` showed exponential conditioning in *selected Fourier-frequency measurements* of binary signals.

**This pass is different:** it covers **every bounded intermediate encoding**, even nonlinear ones having nothing to do with selected Fourier frequencies. It asks whether an entire exact Fourier computation can pass through a narrow register bottleneck and later expand into N ordinary output scalars, and what happens when a giant integer operation is treated as a macro.

The proof techniques are classical rank/chain-rule, packing, and Kronecker substitution. They are applied here as falsification gates, not presented as discoveries or a universal FFT gate-complexity lower bound.

## 1. The all-input complex rank bottleneck

Let F_N denote the unnormalized complex DFT. It is invertible (F_N* F_N = N I). Assume the full computation factors through an intermediate register vector of width w:

    C^N --E--> C^w --D--> C^N,

with `D(E(x)) = F_N x` on a nonempty open set. Suppose E and D are differentiable at a compatible point. The Jacobian chain rule gives

    F_N = J_D(E(x)) J_E(x).

Since the RHS has rank at most w, and F_N has rank N,

**THEOREM 1: w >= N.**

This is independent of whether E and D contain nonlinear multiplications or rational functions regular at that point. Real differentiability gives the same conclusion using dimension 2N and 2w. Finite piecewise-algebraic branching has a generic open branch where this reasoning applies, subject to the usual regularity assumptions.

**Important:** The theorem does **not** say an O(N) FFT is impossible. Standard FFTs retain at least N live scalar coordinates and satisfy the width requirement. It also does not rule out a circuit that emits and stores some outputs before a cut while retaining other inputs: *all* information crossing the cut, including saved outputs, must be counted in w. Nor does it apply directly to a discrete binary-only domain where no full-dimensional open set exists.

An independent exact F_p matrix-rank audit verifies rank(F_N)=N for N=1,2,4,8,16,32, and for randomized N-by-w and w-by-N Jacobian factors at N=2,4,8,16 confirms their rank is bounded by w. This is a sanity check, not a finite proof of the general theorem; the chain-rule argument is the proof.

## 2. A nonlinear **binary-only** width–conditioning theorem

Binary data can be packed into one giant real/complex scalar, so Theorem 1 cannot apply automatically. But compressing and *stably* recovering all outputs has a precise tradeoff.

Let N >= 1, and let

    E: {0,1}^N -> C^w,    |E_j(x)| <= M

be **any** encoder, possibly highly nonlinear or discontinuous, where M>0. Suppose a decoder D maps encoded states to approximations of unnormalized Fourier output, satisfying

    ||D(E(x)) - F_N x||_infty <= epsilon < 1/2

for every binary x. Assume for encoded states u,v that D is L-Lipschitz in the maximum complex-modulus norm:

    ||D(u)-D(v)||_infty <= L ||u-v||_infty.

No linearity, algebraicity or continuity of E is required. L is required only on E's finite image.

### Proof, one step at a time

1. For distinct x,y in {0,1}^N, `delta=x-y` is a nonzero integer vector and `||delta||_2 >= 1`.
2. Parseval for the *unnormalized* transform gives `||F_N delta||_2 = sqrt(N) ||delta||_2`. Consequently `||F_N delta||_infty >= ||delta||_2 >= 1`.
3. From the two output-error bounds, `||D(E(x))-D(E(y))||_infty >= 1-2 epsilon =: tau`.
4. Lipschitzness therefore forces `||E(x)-E(y)||_infty >= tau/L`.
5. Each real and imaginary part of an encoded coordinate lies inside [-M,M]. Partition that interval into cells of length `s=tau/(2L)`. A number of intervals bounded by `Q=ceil(4ML/tau)+1` covers each real coordinate.
6. If two different encoded points shared the same 2w-dimensional grid cell, each complex coordinate difference would have modulus < sqrt(2) s < tau/L. This contradicts step 4.
7. Hence all 2^N binary inputs occupy different grid cells, whose number is at most Q^(2w).

**THEOREM 2 (nonlinear bottleneck; error <1/2 on unnormalized outputs):**

    2^N <= (ceil(4ML/(1-2epsilon))+1)^(2w).

For exact outputs set epsilon=0. If M and L are each polynomial in N, `log_2 Q=O(log N)`, and

    w = Omega(N/log N).

More quantitatively for epsilon=0, `2^(N/(2w)) < 4ML+2`, so

    L > (2^(N/(2w)) - 2)/(4M).

Thus compressing all N binary inputs into only w=O(log N) bounded complex registers forces exponential-in-N/log N decoder sensitivity. **This is a metric-entropy/information packing argument, not a computational lower bound on direct full-width FFT algorithms.**

### Why the normalization matters

The theorem concerns the *unnormalized* F_N and absolute error epsilon<1/2. If outputs are F_N x/N and only fixed additive error is demanded, the pairwise separation is reduced by a factor N; there is no comparable uniform bound at fixed error for large N. Prior randomized-approximate FFT results exploit a different accuracy model and are not refuted here.

### Real-only refinement and sharp simple example

When E has w **real**, rather than complex, coordinates, the cell capacity is `Q^w` rather than `Q^(2w)`.

Take block width b dividing N and w=N/b. Encode block t as the fraction

    E_t(x) = sum_{j=0}^{b-1} x_(tb+j) 2^(-j-1).

This uses O(N) ordinary scalar operations and gives a valid injection with 0<=E_t<1. Two binary inputs differing only at position b-1 of one block have encoded sup-distance exactly 2^-b. Their unnormalized Fourier outputs differ by 1 in *every* frequency. Hence **any** exact decoder on this particular code has Lipschitz constant at least 2^b.

So packing b Boolean bits into each exact real scalar is possible, but the decoder's sensitivity grows exponentially in b. The packing lower bound has the correct exponential scale up to constant factors in this explicit family. A decoder based on floor/bit extraction is NOT an algebraic exact-complex-arithmetic primitive, and reading b bits is not a free operation in a bit model.

### Finite-value representation cost

If an intermediate state has w registers with at most 2^b distinguishable values per register, exactly identifying all 2^N binary inputs demands `w*b >= N` by elementary counting. For complex scalars stored with b bits **per real component**, replace b by 2b. This is an independent discrete statement and should not be confused with a complex-field gate-count bound.

## 3. A concrete *direct global evaluator* that hides work in a macro

Can we compute a complete fresh exact DFT with *one* multiplication? Over a suitable prime field, **yes if one giant integer multiplication is counted as one operation**. The catch is that such a multiplication is *not* a scalar or word operation.

Let N be even and p an odd prime with primitive 2N-th root zeta. Let omega=zeta^2 and

    d_j = zeta^(j^2),   h_j = zeta^(-j^2).

Because N is even, h_(j+N)=h_j. The elementary identity `2kj=k^2+j^2-(k-j)^2` gives

    F_N x = d * (h circledast (d*x)),

where circledast is length-N **cyclic** convolution and * denotes coordinatewise multiplication here. This is the classical quadratic-chirp/Bluestein identity already present in our prior audit, used here as an exact control.

Let `a_j` be the canonical integer lift in [0,p-1] of `d_j x_j mod p`, and let `b_j` lift `h_j`. Their ordinary **integer** polynomial convolution coefficients c_t satisfy

    0 <= c_t <= N (p-1)^2.

Choose a radix `B=2^s > N (p-1)^2`, with s a multiple of eight. Define

    A = sum_{j=0}^{N-1} a_j B^j,
    H = sum_{j=0}^{N-1} b_j B^j.

Then ONE integer product `P = A*H` has all ordinary convolution coefficients as its base-B digits, with zero inter-digit carries. Extract c_0,...,c_(2N-2), fold `(c_k+c_(k+N)) mod p`, and multiply by d_k. This returns **all N fresh, exact modular Fourier values**, using no cached transform and no guessed relationships between inputs.

`global_bottleneck.py` implements this with efficient `int.from_bytes`/`to_bytes` packing and O(N) modular phase preparation. It is independently checked against both a quadratic direct DFT and an iterative NTT with separately implemented bit reversal. Four different primes are covered in regression tests.

### Why this is NOT an O(N) exact FFT

The two integers fed to `P=A*H` each have up to N*s bits. The s-bit base cell has to satisfy

    s > log_2 N + 2 log_2(p-1).

Thus the big integers contain `L = Theta(N (log N + log p))` bits. Computing P costs `M_int(L)` bit operations plus O(L) packing/unpacking bit work. In particular, **the macro itself is not a unit-cost arithmetic operation**. If the field varies with N so that primitive 2N-th roots exist, `p >= 2N+1` and `L=Omega(N log N)` bits. Even the explicit N field outputs then occupy Omega(N log N) bits in conventional fixed-width representation.

A fixed prime like p=998244353 only supports finitely many power-of-two lengths, so fixed-modulus benchmarks alone establish no asymptotic family. In a word-RAM model with Theta(log N)-bit words, an arbitrary-length multiplication on Theta(N) words is not a single word operation; no O(N)-word-time multiplication bound is proved by this reduction.

**Practical negative result:** In our Python benchmark the packed implementation eventually becomes *slower* than our separate Python NTT as N grows. These timings compare two educational implementations and do not establish optimal native performance. The scientific result is the explicit bit accounting, not wall-time dominance.

### Concrete collected data

| N | Packed operand bits per input | One-bigint method (ms) | Python NTT (ms) |
|---:|---:|---:|---:|
| 64 | 4,608 | 0.079 | 0.062 |
| 256 | 18,432 | 0.338 | 0.348 |
| 1,024 | 73,728 | 2.272 | 2.254 |
| 4,096 | 294,912 | 16.223 | 9.655 |
| 16,384 | 1,310,720 | 143.368 | 46.719 |

Medians of five deterministic but different fresh inputs, one process, no prior cached transforms; phase preparation and output extraction included. This run uses p=998244353. Measurements are exploratory and platform dependent. **A nominal count of 'one multiplication' is intentionally deceptive and should never be called a linear-time FFT algorithm.**

### Prior-art status

Both steps are classical and already known: Bluestein's reduction of DFT to convolution, and Kronecker substitution of polynomial convolution into integer multiplication. They are combined here as a falsifiable counterexample to hidden work, not a novelty claim.

- Bluestein/rocFFT design: https://rocm.docs.amd.com/projects/rocFFT/en/docs-6.3.0/design/bluestein.html
- Kronecker substitution: https://en.wikipedia.org/wiki/Kronecker_substitution
- Dumas, Fousse, Salvy, *Simultaneous Modular Reduction and Kronecker Substitution for Small Finite Fields*: https://arxiv.org/abs/0809.0063

## 4. What actually follows for the original fresh FFT goal?

- **Complex exact all-input:** any smooth full-state bottleneck must retain w >= N scalar dimensions. This does not force N log N arithmetic; an O(N)-gate algorithm could remain N-wide throughout, if a new legal global evaluator exists.
- **Binary input:** w can be much smaller, but a bounded and polynomially well-conditioned decoder requires w=Omega(N/log N). A w=O(log N) sketch would require enormous dynamic range or extreme sensitivity.
- **Finite-field exact NTT in bit complexity:** standard full output requires Omega(N log N) bits when the field supports primitive N-th roots with p growing at least linearly in N. **O(N) bit-time all-output NTT is impossible in that particular output format**, irrespective of algorithms. An O(N)-word-operation question is distinct and not answered here.
- **One-bigint direct transform:** shows the danger of hiding N log N-bit data in one macro. It does not evade any applicable lower bound and does not improve #130's exact-complex arithmetic complexity.

The OpenAI Math #130 result (as described in its Lean scope document) already claims a fully charged uniform exact-complex DFT below N log N with unrestricted coefficients. This work does not compete with that exponent or imply integer-multiplication improvements. The earlier user research checkpoint remains authoritative regarding duplicate avenues.

## 5. Research direction and next falsification gate

For the *original* exact complex O(N) ambition, stop looking for an output decoder from a handful of exact values. A candidate must be a **wide global evaluator** that accepts arbitrary fresh complex input, keeps all live information, and gives a complete operation-level recurrence faster than N log N, with all coefficient/condition/routing costs. An unbounded-coefficient candidate needs its effect on numerical conditioning and bit representation quantified; a bounded-coefficient candidate must confront the standard lower bounds.

One mathematically narrow next test would be to take a *specific* proposed wide-state global mixing identity (not another compressed representation), unroll it into charged elementary operations for all N=2^m, and try to prove `T(N)=o(N log N)` before doing extensive optimization. We have **no such identity yet**; declaring an algorithm now would be misleading.

## 6. Reproduction

    cd fft_global_bottleneck_audit
    PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
    PYTHONDONTWRITEBYTECODE=1 python audit.py

No pip dependencies: Python standard library only. All field computations are exact; no threading. `audit_results.json` holds the cost model, bit widths, median timings, and condition-growth examples.

**Rejection criteria:** wrong output, hidden giant-field arithmetic, unchecked root existence, input state stored elsewhere, intermediate decoder not actually Lipschitz, incomplete output, or a claimed O(N) gate count made by treating a big integer multiplication as one elementary operation.
