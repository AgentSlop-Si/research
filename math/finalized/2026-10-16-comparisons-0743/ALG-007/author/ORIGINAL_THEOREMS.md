# Hero #0 / Phase 6 — Exact adaptive Green-mode Fourier transform

**Research date:** 10 October 2026  
**Status:** New *project-level* verified conditional execution theorem, finite-field and complex implementations, a general high-Hankel-rank lemma, and a strict coverage obstruction. **Not** a general exact `O(N)` FFT, **not** a novelty claim against the literature, and **not** a bit-complexity or fixed-precision theorem.

## 1. Precise setting

Take `Q = K M`, `K >= M >= 2`, with even `Q`. All `Q` input coordinates are fresh, arbitrary *within the family defined below*, and all `Q` Fourier outputs are explicitly written. Count sequential exact complex field operations and charged input/index/root-table preparation. A primitive `Q`-th root is supplied or constructed by the stated model. In a finite-field implementation, use characteristic not dividing `Q`, a primitive `Q`-th root in the field and invertible scalar `2`. The included modular code uses a specific 31-bit prime with power-of-two dimensions; the complex decoder derives from the existing Phase 2 Green identity.

Define `zeta=exp(2*pi*i/Q)` and the unit-chirp matrix, for any unit `a mod Q` and shift `beta`:

\[
 s_{b,t}=\zeta^{a\binom t2+(aMb+\beta)t},\quad 0\le b<K,\quad 0\le t<M. \tag{1}
\]

For even `Q`, this is exactly the Phase 2 chirp. For odd `Q`, the original decoder has an additional half-root parity twist; this phase does **not** extend the finite-field certificate to odd `Q` without a separate proof.

Set `v[b,t]=s[b,t]*x[bM+t]` and `zeta_M=zeta^K`. Define the *global Green-mode coefficients*:

\[
 D_{b,r}=\sum_{t=0}^{M-1} v_{b,t}\zeta_M^{rt},\qquad 0\le r<M.\tag{2}
\]

For a mode set `S subset {0,...,M-1}`, define the linear subspace

\[
 \mathcal V_S=\{x\in\mathbb F^Q:\ D_{b,r}(x)=0\ \forall b,\,r\notin S\}.\tag{3}
\]

`S` is shared **globally** across all blocks, although the coefficients `D[b,r]` vary arbitrarily and independently from block to block. The input can be dense in the ordinary coordinate basis. Crucially, the algorithm is **not** given `S` in advance.

## 2. Exact reconstruction and Green-cycle decomposition

Fourier orthogonality in every block gives:

\[
 x_{bM+t}=\frac{s_{b,t}^{-1}}{M}\sum_{r=0}^{M-1}D_{b,r}\zeta_M^{-rt}.\tag{4}
\]

The mode-`r` Green chirp is exactly the original slope `a` with shift `beta_r=beta+rK (mod Q)`. Let its rank-one block projector be

\[
 (P_r x)_{bM+t}=s_{b,t}^{-1}\zeta_M^{-rt}D_{b,r}.\tag{5}
\]

Therefore `sum_r P_r=M I_Q`. On `x in V_S`, all `r notin S` vanish, hence

\[
 \boxed{F_Qx=\frac1M\sum_{r\in S}F_QP_r x.}\tag{6}
\]

The previous Phase 2 Green-cycle theorem executes `F_QP_r x` given the `K` block summaries `D[b,r]` using one `K`-point FFT/NTT followed by a length-`Q` gauged cycle/scan. It never executes a full `Q`-point FFT. It charges `O(Q+K log K)` scalar operations per `r`. The modular code here independently reimplements that exact cycle decoder and verifies (6) against a separate `Q`-point NTT oracle.

This is the *project's own* Green-cycle fast path, not the CrocSwap/kappa optimization path. Its algebraic ingredients overlap known Fourier, Gabor/chirp and pruned-transform mathematics; scholarly novelty is **not** established.

## 3. Deterministic adaptive recognition (the new algorithmic gate)

Initialize a **discovered global set** `S = empty`. For each input block `b`:

1. Form the `M` dechirped entries `v[b,t]` by the charged multiplication (1).
2. For each `r in S`, compute its exact coefficient `D[b,r]` from (2) in `O(|S| M)` operations.
3. Reconstruct the block using only those modes via (4), and compare **every coordinate** with the raw block. This is a *certificate*, not a probabilistic guess.
4. If the certificate succeeds, store the coefficients. If it fails, compute the full **small** length-`M` DFT of this block, append its previously unseen nonzero mode indices to `S`, and store the resulting coefficients. Newly discovered modes were rigorously zero in all earlier blocks that passed their certificates.
5. If `|S|>r_max`, reject the sparse path and call the existing full-FFT fallback. Otherwise complete all blocks and evaluate (6) with the recovered `|S|` Green rows.

The number of full short-block transforms is bounded by `r_max+1`: every such transform either discovers at least one new mode or terminates by rejection. This includes the all-zero input (which has zero modes).

With root-power table construction **charged** in `O(Q)` and standard length-`M` FFTs for discovery, for a successful input with at most `r` global modes:

\[
\boxed{W(Q,r)=O(Q+rQ+rK\log K+(r+1)M\log M),\qquad S(Q,r)=O(Q).}\tag{7}
\]

For `M=Theta(log Q)` and `K=Q/M`, this becomes

\[
\boxed{W(Q,r)=O((r+1)Q).}\tag{8}
\]

In particular `r=O(1)` gives **exact O(Q)**, and `r=O(log log Q)` gives **exact O(Q log log Q)**. No persistent cache or input-dependent preprocessing from an earlier query is assumed. The modulus/root preparation cost must be included in any alternative model; the source generates the `Q`-entry root table with `Q-1` charged modular multiplications, and any remaining scalar modular exponentiations are at most `O(log^2 Q)` per short FFT or `O(log p)` setup, negligible under the stated model.

**Worst-case:** For generic arbitrary inputs, `r=M`, so the same architecture returns `O(Q log Q)`, not a uniform sub-FFT bound. Recognition alone does not make a generic transform faster.

## 4. New high-Hankel-rank lemma: this family is not globally low-Prony-rank

For any fixed nonempty `S` and any even `K`, write `h=Q/2`, and consider the ordinary `h x h` Hankel matrix `H[i,j]=x[i+j]`.

Choose one active mode `r in S`. Set its coefficient `D[b,r]` nonzero only on block `b*=K/2-1`, and all other mode coefficients zero. This signal is zero for every index `j>=h` and has `x[h-1] != 0`: the last sample of the populated central block is a nonzero root times a nonzero scalar.

The Hankel entries vanish whenever `i+j>h-1`, and `H[i,j]=x[h-1]` whenever `i+j=h-1`. Reverse its columns. The resulting matrix is triangular, with diagonal constantly `x[h-1]`, so

\[
 \boxed{\det H=\pm x[h-1]^h\ne0.}\tag{9}
\]

For a fixed `S`, this Hankel determinant is a polynomial in the free `K|S|` block-mode coefficients. Since it is nonzero at the displayed assignment, it is **not the zero polynomial**. Consequently, when the coefficients are drawn from any jointly absolutely continuous distribution, the Hankel matrix has **maximal rank `Q/2` with probability one**. Moreover, all time-domain coordinates are nonzero with probability one because each is a nonzero linear functional of its own block coefficients.

Hence, even the one-mode family can consist of dense, nonperiodic, *maximal-Hankel-rank* inputs. It is **not** restricted to the globally low-order linear recurrences handled in previous Phase 23. This is an existence/genericity statement about the conditional class, not a worst-case speedup for all inputs.

The accompanying exact modular experiments checked full Hankel rank at `Q=64,128,256,512`, including the explicit anti-triangular witness. Dense random one- and two-mode signals also reached the maximal rank in every tested case.

## 5. New finite-library coverage obstruction

The map `x -> (D[b,r])` is an invertible blockwise coordinate change, so

\[
\dim \mathcal V_S=K|S|.\tag{10}
\]

For any `r<M`, these are proper subspaces. Even if one searches **all** invertible slopes `a`, all `Q` shifts `beta`, and all possible supports with `|S|<=r`, there are only finitely many such subspaces. Their union has Lebesgue measure zero in `C^Q`. Therefore **generic arbitrary complex inputs admit no exact r-mode representation under any of these chirps**.

Over a compatible field `F_p`, uniform random `x` lies in a particular `j`-mode subspace with probability `p^{-K(M-j)}`. The union bound yields

\[
\boxed{\Pr[\exists\ a,\beta,S,\ |S|\le r:\ x\in\mathcal V_{a,\beta,S}]
\le Q\varphi(Q)\sum_{j=0}^r\binom Mj p^{-K(M-j)}.}\tag{11}
\]

For the certified field `p=2013265921`, `Q=256`, `M=16`, `r=2`, this bound is smaller than `10^-2077`. This is a mathematical finite-union/volume obstruction, not an empirical estimate or a lower bound for all FFT algorithms.

**Interpretation for the original cycle hypothesis:** a finite search over chirp slopes and input-local mode sets cannot make generic fresh inputs compressible. A universal exact sub-FFT breakthrough needs something other than simply detecting a short global support in one of these coordinate systems.

## 6. Unitary-cycle entropy gate (separate restricted no-go)

For a unitary matrix `A`, let `Phi(A) = -sum_{i,j} |A_ij|² log2 |A_ij|²`, with `0log0=0`. Identity and permutations have `Phi=0`. The normalized Fourier matrix has `Phi(F_Q/sqrt Q)=Q log2 Q`.

A two-coordinate unitary mixing gate changes only two rows. At each column, the sum of their squared magnitudes is conserved; splitting this sum between two rows changes their binary Shannon entropy by at most one bit per unit of column mass. Because the total mass of the two rows is two, **one gate changes Phi by at most 2 bits**. Therefore

\[
\boxed{\text{two-row unitary mixers required}\ge (Q/2)\log_2Q.}\tag{12}
\]

An ordinary radix-2 normalized butterfly network exactly achieves this for powers of two: all its gates couple vectors with disjoint supports and increase `Phi` by 2 bits. We independently tested the complete matrices at `Q=8,16,32,64,128`.

This obstruction covers **unitary two-coordinate classical amplitude circuits only**, not general arithmetic circuits with nonunitary coefficients, global multi-coordinate gates, table lookups, or quantum circuits counting operations on qubits instead of explicitly maintained classical amplitudes. It is in the spirit of classical entropy/volume lower bounds, not a new unrestricted FFT lower bound.

## 7. Independent reproducibility and operation accounting

Run `python verify_all.py` from the package directory. The exact finite-field implementation uses the prime `2013265921` and primitive root `31`; all transform sizes in the tests divide `p-1`. In modular checks every output is exactly equal (integer congruence), not merely within a tolerance.

- `test_phase6.py`: **336 distinct exact finite-field sparse-mode cases** across multiple `Q,M,a,beta,r`, plus 21 nonsparse rejections; ten modular Hankel-rank checks.
- `test_complex.py`: **96** near-machine-precision complex cases (up to `Q=8192`), plus eight nonsparse rejections. Maximum normalized absolute discrepancy `4.99e-16`.
- `test_adversarial.py`: disjoint per-block supports, late new-mode rejection, full-support ordinary-case control, four full-Hankel-rank corner witnesses, independent complex support-split case.
- `scale_audit.py`: `Q=256` to `32768`, active support `r=2`. With the root table charged, the executable modular addition+multiply count stays at roughly `27–29` field operations per input entry over the tested range. This is a finite-instance operation-count trend, not itself an asymptotic theorem.
- `coverage_bound.py`: (11) evaluated in logarithmic form; these are **upper bounds**, not observed frequencies.
- `unitary_entropy_gate.py`: exact FFT butterfly counts and numerical matrix/entropy checks; lower bound comes from the proof, not the sample sizes.

**Implementation caveat:** the complex128 detector uses a numerical threshold for support recognition and cannot be advertised as a guaranteed exact classification of all complex floating inputs near a mode-subspace boundary. The finite-field detector uses strict equality and gives an exact certificate. Floating-point stability and bit complexity remain open.

## 8. What comes next

**Do not repeat:** local complete-frame phase fusion (it gives ordinary Cooley–Tukey); constant-mode searches on unrelated dense data; low-rank unitary transfers; exact subtree collision caches; short global Prony decompositions; unitary two-wire gate rearrangements.

**Next falsifiable exact target:** construct and cost a new **global nonunitary cross-mode contraction** that reduces *generic* full-support `D[b,r]` to a smaller number of globally executable channels, without an independently paid `M`-fold decoder, without an arbitrary-input transform oracle, and with all coefficient construction, index work and final explicit outputs counted. First test against generic random modular inputs—then attempt a family-of-`Q` bound. Comparison must be in the same exact scalar model as the known 2026 `o(N log N)` result, not against a weaker radix-2 baseline alone.

The current output is a **valid restricted-class theorem and independent testing package, not an exact all-input FFT breakthrough.**
