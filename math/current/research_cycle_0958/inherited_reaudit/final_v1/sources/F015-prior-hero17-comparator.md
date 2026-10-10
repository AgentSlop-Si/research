# Hero #17, continuation: Tensor-Union, Fiber-Union and Frequency-Graph Convolution

**Checkpoint:** 10 October 2026  
**Status:** scoped exact algebraic theorems, implementation, regression and independently constructed finite-field audits. **No universal all-input exact `O(N)` DFT or arbitrary integer-multiplication algorithm. No priority/novelty claim.**

## 0. Purpose, proven assumptions and accounting contract

The original user challenge is a fully charged, sequential, exact discrete Fourier transform of **every fresh arbitrary** length-`N` input, with **all `N` explicit coefficients**, ideally `O(N)` time. Our new constructions do **not** solve that challenge. They give genuinely exact `O_r(N)` algorithms for much larger **recognized structured-input families** than the preceding phase-union checkpoint and a similarly scoped cyclic-convolution method. In particular they handle certain *dense, maximal-matrix-rank* inputs, not merely constant-rank or constant-period signals.

Arithmetic model: a prime `p>N` with `N | (p-1)`, supplied certified primitive `N`th root `omega in F_p`, exact arithmetic and comparisons in `F_p`. For the `O(N)` word-RAM interpretation assume `p=N^{O(1)}` and `Theta(log N)`-bit machine words with unit-cost modular multiplication, addition and addressing. No root-generation oracle is concealed: root-order validation via a power table takes `O(N)` work; the testing helper `root_for` is for fixture construction only. The algorithms charge input reading, public factor selection, row certification, inversion, output materialization and preprocessing tables. A supplied root is a conventional transform-model premise; a separately requested root-finding guarantee is not part of these theorems. For fixed rank/mode bound `r`, the cost of `O(r)` inversions per row on a word-RAM is still subsumed by `O(N)` because the number of rows is `O(sqrt N)` and modular inversion uses `polylog(N)` work. Exactly represented complex arithmetic has analogous identities but numerical conditioning and robust floating-point recognition are **not established**.

### New executable branches

- **Tensor-Union:** discover low matrix rank after Chinese-remainder reshaping, then explicitly compute all outputs; no supplied chirp frequencies/coefficients.
- **Coset-Union:** discover maximal cyclic support coset by a charged gcd scan, decompose its shorter sequence with the previous validated quadratic-phase recognizer, and lift all bins.
- **Fiber-Union:** recognize a few independently chosen Fourier characters along each strided input fiber and evaluate every output in linear time, **even when the fiber matrix has maximal ordinary rank**.
- **Graph-Union convolution:** match per-fiber Fourier characters between two fresh inputs, sum matching-edge contributions, and accept full reconstruction only when the surviving output-state count satisfies a fully charged linear-time budget.

The fully fused recognizer tries eligible balanced Tensor-Union, then Fiber-Union, then Coset-Union, and returns `None` otherwise. A conventional FFT/NTT is required for unsupported arbitrary vectors.

## 1. Tensor-Union theorem: arbitrary dense factors, exact `O(N)`

Let `N=A B`, `gcd(A,B)=1`, `A,B=Theta(sqrt N)`. Define CRT idempotents

`e_A = B * (B^(-1) mod A) mod N`,  `e_B = A * (A^(-1) mod B) mod N`.

Reshape the *raw* input into `X[u,v] = x[(u e_A + v e_B) mod N]`, `0<=u<A`, `0<=v<B`. For `rank(X)=r` fixed, a row-echelon scan with at most `r` basis rows provides an **exact verified-by-elimination** factorization

`X[u,v] = sum_{ell=1}^r f_ell[u] g_ell[v]`

in `O(rN+r^2(A+B))` field operations (the explicit implementation needs at most `O(rN)` for fixed `r`; it normalizes new basis rows and stores all row coefficients). At rank `r+1` it rejects without a false positive.

The CRT/output-index identity is

`DFT_N(x)[(sB+tA) mod N] = sum_{ell=1}^r DFT_A(f_ell)[s] * DFT_B(g_ell)[t]`.

**Proof:** the map `(u,v) -> u e_A+v e_B mod N` is a bijection, and for `k=sB+tA`,

`omega_N^(-jk) = (omega_N^B)^(-u*s) * (omega_N^A)^(-v*t)`.

Thus the Fourier kernel factors and sum/product interchange gives the formula. Compute the `r` short transforms by **direct quadratic sums**, not by a hidden FFT, in `O(r(A^2+B^2))`. Writing and combining `N` output elements costs `O(rN)`. Therefore

`T = O(rN + r(A^2+B^2) + N)`;

for balanced factors and fixed `r`, `T=O_r(N)`. Public factor search scans down from `floor(sqrt N)` testing divisibility/coprimality, `O(sqrt N log N)` word work, which is also `O(N)`. Memory is `O(N+r(A+B))` including input/output. The fused path accepts only factors satisfying `A^2+B^2<=4N`; unbalanced CRT rank is not mislabeled linear.

### Two consequences

1. **All integer polynomial phases separate across CRT**: for integer polynomial `P` of *any degree*, `P(j) = e_A P(u)+e_B P(v) mod N`; therefore `omega_N^{P(j)} = f(u)g(v)` has CRT tensor rank one. A sum of `r` independently parameterized polynomial phases has rank at most `r`. Previous bounded-phase engine required a *shared quadratic* coefficient; this is a strict family enlargement at eligible lengths. Arbitrary factor vectors `f,g` are still allowed, and need not themselves be polynomial phases.
2. The CRT matrix rank is unchanged by the DFT (after bijective input and output reindexing), because the transform is `F_A X F_B^T` and both short DFT matrices are invertible. This is a scoped **obstruction** to lowering generic CRT rank by CRT-separable Fourier gauges, not a general FFT complexity lower bound.

### Exact convolution of bounded CRT-rank inputs

For `x=sum_i f_i tensor g_i`, `y=sum_j h_j tensor v_j`, the cyclic group `Z_N` is isomorphic to `Z_A x Z_B`, hence

`(x circledast y)[u,v] = sum_(i,j) (f_i circledast_A h_j)[u] (g_i circledast_B v_j)[v]`.

Two fresh rank-`r1,r2` raw inputs can be recognized and fully convolved with `O((r1+r2)N + r1*r2*(N+A^2+B^2))` arithmetic by direct small cyclic convolutions and an explicit full output. The output CRT rank is at most `r1*r2` (possibly lower). This is **special-input cyclic convolution**, not a general integer-multiplication result. See `tensor_union.py`.

## 2. Coset-Union theorem: every transform length

Take any raw `x`. Scan nonzero positions, choose the first `j0`, and compute

`d = gcd(N, {j-j0 : x[j]!=0})`, `u=j0 mod d`, `M=N/d`.

The nonzero input is exactly supported inside the coset `u+d Z_M`; pull it back as `y[t]=x[u+dt]`. The gcd can be updated only when a new difference is not divisible by the current `d`. Every such reduction reduces `d` by a factor at least two; therefore there are at most `O(log N)` nontrivial gcd calls, while all `N` positions are scanned only once. This gives `O(N+log^2 N)` word work.

Let `eta=omega_N^d` be a primitive `M`th root. The exact alias formula is

`DFT_N(x)[k] = omega_N^(-u*k) DFT_M(y)[k mod M]`.

Use the verified preceding `phase_union_general.py` recognizer on `y` when `M>=3r`, accepting only `<=r`-mode quadratically dephased sequences. When `M<3r`, direct `M^2=O_r(1)` evaluation is sufficient. Output lifting then costs `O(N)`.

**Completeness caveat:** if a promised larger-support chirp signal happens to vanish on additional congruence classes, shrinking to the maximal detected coset preserves the chirp-plus-`r`-character form (restriction of a quadratic exponential to an arithmetic progression is quadratic, and frequencies may merge). All-zero and singleton supports are explicit cases. This works at powers of two where no balanced nontrivial coprime CRT split exists. See `coset_union.py`.

## 3. Fiber-Union theorem: maximal-rank input matrices allowed

This is the most significant *new project extension*. For **any** factorization `N=Q M`, define input fibers

`x[t+Q*u]`,  `0<=t<Q`, `0<=u<M`.

Assume that **each fiber**, independently, is a sum of at most `r` characters of the cyclic subgroup `Z_M`:

`x[t+Q*u] = sum_{(h,c) in R_t} c*eta^(h*u)`, `eta=omega_N^Q`, `|R_t|<=r`.

The labels `h` and coefficients `c` differ freely with `t` and are *not supplied*. We discover them from every raw fiber using bounded Berlekamp--Massey, scan the publicly prepared length-`M` roots, recover amplitudes with the `O(r^2)` transposed Vandermonde formula, and verify **every input coordinate**. Per fiber this takes `O(rM+r^2)` exact field operations, so all fibers cost `O(rN+Qr^2)`.

The Vandermonde formula is explicit. Let distinct detected roots be `z_i=eta^h_i`, `P(z)=prod_i(z-z_i)`, `Q_i(z)=P(z)/(z-z_i)`, and input moments `y_j = sum_i c_i z_i^j` for `0<=j<r`. Then

`c_i = (sum_{j=0}^{r-1} coeff(Q_i,z^j)*y_j) / P'(z_i)`.

Building `P`, synthesizing each `Q_i`, and the dot products together take `O(r^2)` field operations. The roots are distinct and `P'(z_i)!=0`, so the formula is exact. The recovered full expansion is also verified; soundness does not depend on a probabilistic test. Small `M<3r` is handled with an exact direct length-`M` DFT and an explicit <=`r`-nonzero check.

Now `k=h+sM`, `0<=h<M`, `0<=s<Q`. The full transform identity is

`DFT_N(x)[k] = M * sum_{t=0}^{Q-1} sum_{(h',c) in R_t : h'=h} c * omega_N^(-k*t)`.

**Proof:** expand `j=t+Q*u` and sum over `u`:

`sum_u eta^((h'-k)*u) = M` when `h'==k mod M`, otherwise zero.

Each detected input mode contributes to **exactly `Q` output bins**. The total explicit output evaluation therefore costs `O(r Q^2 + N)` with fully charged table lookup and output writes. Thus

`T = O(rN+Qr^2+rQ^2+N)`;

with `Q^2=O(N)` and fixed `r`, **`T=O_r(N)`**, with `O(N)` memory.

The default public divisor is the largest divisor `Q<=floor(sqrt N)`, found in `O(sqrt N)` divisions. It always satisfies `Q^2<=N`, even for primes (`Q=1`, corresponding to ordinary `r`-sparse Fourier signals). Specified `Q` is allowed only if it divides `N` and `Q^2<=C N` for a fixed constant `C`.

### Why this is not just the Tensor-Union result

For `Q=M` and distinct `h_t=t`, with nonzero arbitrary amplitudes `c_t`, the `Q x M` matrix `X[t,u]=c_t*eta^(h_t*u)` consists of different DFT rows and has **full row rank `Q`**. Nevertheless its raw full DFT is recognized and emitted in `O(N)`. This family has maximal ordinary rank, whereas Tensor-Union requires constant rank. Random full raw inputs still fail the bounded-fiber promise.

### Arbitrary-degree polynomial phases and prime powers

For a perfect square `N=Q^2` and **any integer polynomial** `P`, the binomial expansion shows

`P(t+Q*u) = P(t) + Q*u*P'(t) (mod N)`.

Therefore `x_j=c*omega_N^{P(j)}` is **one character per fiber**, regardless of `deg P`, and is recognized from raw samples in `O(N)`.

For `N=p0^(2h+1)`, `h>=1`, with fixed integer prime `p0`, choose `Q=p0^h`, `M=p0^(h+1)`. Cubic-and-higher terms in `P(t+Q*u)` vanish modulo `N`, while the quadratic correction has the form `exp(2*pi*i*a*u^2/p0)`, periodic in `u` with period `p0`. A period-`p0` function over the length-`M` cyclic group has Fourier support in at most `p0` frequency classes. Therefore every fixed-degree (indeed any integer-polynomial degree) phase has **at most `p0` modes per fiber**, and obtains `O_{p0}(N)` exact all-output work. When `p0=2`, the parity identity `u^2=u (mod 2)` makes each fiber **one-mode** even for odd powers of two. Verified `N=125,243,256,512,1024` for degrees 2,3,4,5,7 and additional degrees in audit.

This is an observation from classical Fourier algebra, not a new claim about quantum computation or polynomial exponential-sum priority.

## 4. Graph-Union convolution: matching edges and charged output states

Let two fresh vectors have validated Fiber-Union representations, with mode sets `R^x_t`, `R^y_t`. For equal character label `h`, connect the node `(t1,h,c1)` to `(t2,h,c2)`. Put

`t=(t1+t2) mod Q`, `carry=floor((t1+t2)/Q) in {0,1}`.

Then the edge adds the **exact** partial-Fourier amplitude

`M*c1*c2*eta^(-h*carry)`

to output state `(t,h)`. Mismatched characters contribute zero. This follows directly by summing over the cyclic internal coordinate `u1` in the raw circular convolution. No full FFT, NTT, implicit output, or uncharged tables appear.

If each input has <=`r1`, `r2` modes per fiber, their total numbers of detected nodes are `<=r1 Q`, `<=r2 Q`. Hence matching edges

`E <= r1*r2*Q^2`.

Build all graph edges, merge identical output `(t,h)` states using a directly allocated length-`Q*M=N` exact accumulator, and let `S` be the **number of surviving nonzero states after union and cancellation**. The cost of *recognition + graph + complete time-domain reconstruction* is

`O((r1+r2)N + (r1^2+r2^2)Q + E + N + M*S)`.

For `Q^2=O(N)`, fixed `r1,r2`, and `S<=C*Q` for a fixed constant `C`, this is **exact `O(N)`**, with `O(N)` memory. The program computes the actual `S` before reconstruction and rejects the fast route if `S>C Q`; the refusal is not a false claim that the convolution doesn't exist.

### Maximal-rank positive family

Take `Q=M=sqrt N` and both inputs with exactly one character per fiber, assigning **each of the `Q` frequency labels exactly once** (independent permutations), with any nonzero input amplitudes. Both `Q x Q` input matrices have rank exactly `Q`, yet there are precisely `Q` matching edges and at most `Q` surviving output states. Recognition `O(N)`, edge union `O(Q)`, reconstruction `O(MQ)=O(N)`. This is a concrete exact linear-time cyclic convolution of two raw dense maximal-rank structured inputs. It is *not* an unrestricted convolution algorithm.

An opposite positive example has all rows using the same single frequency: there are `Q^2` matching edges, but only `<=Q` union states. The graph's aggregation, not just the raw edge count, is essential.

### Adversarial output-state growth

For `Q=M=s^2`, assign `x` frequency `h(t)=t mod s` and `y` frequency `g(t)=floor(t/s)`. Each input has exactly one character per fiber. For each of the `s` labels, the `s x s` matching row pairs cover all `Q` target rows once; hence the product has **`S=sQ=Q^(3/2)` surviving states** (take nonzero coefficients). Naive time-domain reconstruction from those states would take `M*S=Q^(5/2)=N^(5/4)` work. The implementation explicitly detects and rejects it at a fixed linear-state budget. This is a barrier for *this reconstruction mechanism*, not a proof that no different `O(N)` algorithm exists.

See `fiber_convolution.py` and tests; all output coefficients were compared with an independent exact `O(N^2)` convolution.

## 5. Why none of these solve the universal `O(N)` target

Tensor rank `r` over `F_p` is tiny on a generic raw `A x B` input. Simple counting gives at most `p^{r(A+B)}` matrices admitting a rank-`<=r` factorization, among `p^{AB}` total. In particular, for `A,B≈sqrt N` and fixed `r`, the supported proportion is at most

`p^{-N+O(r sqrt N)}`.

For Fiber-Union, the length-`M` DFT is a bijection. Each row having <=`r` nonzero transform coefficients gives at most

`sum_{j=0}^r binom(M,j)(p-1)^j`

possible rows, among `p^M`; independent rows give the `Q`th power of that fraction. For `M,Q≈sqrt N`, fixed `r`, this fraction is exponentially small in `N` (in base `p`). Thus a uniform random fresh vector almost surely defeats our restricted recognizers, although passing inputs may be dense and have maximal ordinary matrix rank.

At full fiber spectral density, our general identity becomes

`DFT_N(x)[h+s M] = M * DFT_Q(t -> C[t,h]*omega_N^(-h*t))[s]`,

where `C[t,h]` is the partial length-`M` Fourier transform of the `t`th fiber. This is just the ordinary Cooley--Tukey structure: there are `M` unrelated dense length-`Q` channels, so applying separate generic FFTs returns `Theta(N log Q)` work. **Finding a fully charged universal joint evaluator of these dense channels is the unresolved gate.** Repeated lookup/hash/union for random channels does not by itself constitute a proof of saving. A quantum Fourier circuit is not an oracle returning `N` exact classical amplitudes.

## 6. Reproducibility and provenance

The reproducible implementation requires only Python standard library. The prime field and root are explicit; `root_for` is used only by tests to manufacture fixtures, never by the online transform functions. The original `phase_union_general.py` is copied verbatim from the prior Hero #17 all-length checkpoint; it is an inherited dependency, **not** an independently invented generic primitive. All new scripts are clearly separate.

Run:

```bash
python -m unittest -v test_hero17
python independent_audit.py
```

The last run completed **27/27 test methods**, including full-output exact tensor, fiber, coset and convolution checks; rank/zero/adversarial branches; and a large length-2303 spot-check. The independent reproducibility script reports:

- `72` random low-rank tensor inputs, independently checked against direct all-output DFT.
- `63` random sparse-fiber inputs, independently checked against direct all-output DFT.
- `36` polynomial-phase vectors, independently checked against direct all-output DFT.
- `12` pairs of maximal-rank fiber matrices whose complete cyclic convolutions were independently checked.
- `44,875` independently calculated Fourier output bins, plus `5,184` independently calculated circular-convolution bins.
- `750` rejected independently random dense candidates and a deliberate `S>2Q` graph-union rejection.

The run uses deterministic PRNG seed `1717` with exact finite-field arithmetic. Counts are stored in `AUDIT_RESULTS.json`. **Correctness tests are not timings against optimized FFT libraries**, and do not prove any new fastest algorithm in the unrestricted model.

### References and novelty caveat

The CRT/tensor Fourier reduction is classically known as the **Good--Thomas or prime-factor FFT**. The row/character sparse step is a classical subgroup Fourier projection and can be interpreted as a particularly transparent pruned Cooley--Tukey calculation. Sparse Fourier/Prony, Berlekamp--Massey, Gaussian sums, Fourier rank and stabilizer/phase structures have extensive prior art. What is provided here is a coherent **research checkpoint and verified combined implementation**, not a claim of first discovery.

Helpful background:

- Good--Thomas prime-factor FFT: <https://www.dsprelated.com/freebooks/mdft/Prime_Factor_Algorithm_PFA.html>
- OpenAI Math exact DFT result #130, all lengths in a permissive complex arithmetic model, `O(n(log n)^(1-1e-13))`: <https://github.com/openai/math/blob/main/lean/docs/130.md>
- Stabilizer rank and higher-order Fourier analysis: <https://quantum-journal.org/papers/q-2022-02-09-645/>

## 7. Exact next research target for Hero #18

Work in the same cost model and keep the same full-output contract. Is there a **uniform joint graph evaluator** for all the dense `M` polyphase channels whose total *charged* cost is `O(N)`? In particular, show a finite, input-independent arithmetic identity that compresses the family of `M` unrelated length-`Q` DFTs, rather than assuming their values happen to share sparse support. Explicitly test random full-support `C[t,h]`, count state preparation and index operations, and reject any candidate that succeeds only on a proper low-rank / low-mode subset. The present full-rank sparse-fiber examples demonstrate that ordinary rank is not the right sole invariant, while the counting bound demonstrates that bounded spectral support still cannot suffice in the worst case.

### Additional exact scaling sanity check

For `F_65537`, at square lengths `N=256, 1024, 4096, 16384, 65536`, we constructed one-character-per-fiber signals with all `Q=sqrt N` frequencies distinct and nonzero amplitudes. With `Q=M=sqrt N`, the **charged output-accumulation loop uses precisely `Q^2=N` contributions** at every tested size (plus the proven linear input scan, character recognition, root preparation and `N` writes). The independently computed selected-bin checks matched all 134 tested bin values across those five sizes. This is a complexity/spot-check sanity test on the promised family, **not a proof about random arbitrary inputs and not a comparison to native FFT library timing**. Full parameters are in `SCALING_CHECK.json`.
