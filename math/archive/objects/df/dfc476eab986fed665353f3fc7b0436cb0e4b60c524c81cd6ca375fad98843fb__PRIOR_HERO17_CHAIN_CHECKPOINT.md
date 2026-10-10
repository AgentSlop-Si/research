# RECOVER HERE — Hero #17 Tensor/Fiber/Graph Union (2026-10-10)

**No universal fresh exact O(N) DFT has been found.** New certified O_r(N) restricted algorithms are implemented and independently tested in `hero17_tensor_union`.

## Largest new positive

For any N=Q M with Q²<=C N, read raw x as Q fibers `y_t[u]=x[t+Q u]` of length M. If each fiber is a sum of <=r arbitrary M-th Fourier characters (different modes for each t), deterministic exact recognition (bounded BM, roots scan, O(r²) Vandermonde, full verification) takes O(rN+Qr²), and ALL N transform outputs cost O(rQ²+N). Fixed r and balanced Q => O(N). A full Q×M input matrix can have rank Q (maximal), e.g. rows with distinct character labels.

Exact DFT identity: for k=h+sM,

`F_N x[k] = M sum_t sum_{(h',c) in modes[t],h'=h} c omega_N^(-k*t)`.

Every integer polynomial phase `omega_N^{P(j)}` has only ONE mode per fiber at perfect-square N, and also one for N power of 2 (floor-square-root choice); at fixed odd prime-power N=p0^(2m+1), at most p0 modes per fiber.

## Graph convolution

For two fiber-sparse inputs, join equal-h character nodes, each edge (t1,h,c1),(t2,h,c2) contributes `M c1 c2 eta^(-h carry)` to partial output `(t=(t1+t2)%Q,h)` with `carry=floor((t1+t2)/Q)`. There are <=r1*r2 Q² edges. Merge in a length-N accumulator; let S be nonzero output partial Fourier states. Reconstruct all N time-domain outputs in O(M S+N). If S<=C Q, fully charged result O(N). In particular if each of two dense full-rank Q×Q input matrices uses one character per fiber with all frequency labels a permutation, exactly Q matching edges and S<=Q, so convolution is exact O(N). Adversarial Q=s² demonstrates S=Q^(3/2) and rejection, not a general lower bound.

## Other fully tested branches

- CRT tensor rank-r with coprime balanced N=A B: raw recognition O(rN), r direct length-A and B transforms O(r(A²+B²)), combine all N output O(rN). Exact cyclic convolution of two ranks r1,r2 similarly O(N) when fixed. Arbitrary polynomial phases in N are CRT rank one; distinct phase parameters allowed.
- Coset support gcd: discover one support coset u mod d in O(N) word work; old validated bounded-phase engine on pulled-back M=N/d input; exact output `X[k]=omega_N^(-ku) Y[k mod M]`. Extends to powers of two.
- `fused_fft.transform_if_supported` tries tensor, fiber, coset; unknown arbitrary data returns None, so ordinary FFT fallback necessary.

## Reproduction

`python -m unittest -v test_hero17` => 27/27 tests passed. `python independent_audit.py` => 72 random tensor vectors, 63 random fiber vectors, 36 polynomial phases, 12 full-rank graph convolutions, 44,875 independently checked exact DFT bins, 5,184 exact convolution bins, and 750 random dense rejections. Scaling further checked N=256 through 65536 with Q²=N charged updates and independently checked selected bins.

Read detailed proof/model/prior art in `RESEARCH.md`, which identifies all scope limitations.

## Unresolved exact target

When the Q×M partial Fourier matrix is dense (generic arbitrary x), the output becomes M independent dense Q-point Fourier channels. Need a non-lookup, fully charged O(N) **joint** evaluator for these channels. Do not mistake bounded-fiber family, bounded tensor rank, saved scalar multiplications, hidden precomputation, or quantum-state readout for universal exact O(N). No proof of novelty or full-FFT benchmark win.
