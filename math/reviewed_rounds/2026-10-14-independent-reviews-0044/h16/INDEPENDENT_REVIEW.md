# Independent audit of the conditional H16-to-DFT lift

## Verdict

**ACCEPT, scoped to the conditional mathematical interface and asymptotic implication.** Assuming an admitted exact word for H_2^{⊗4} on precisely 16 arbitrary logical registers, with at most 31 forward H_2 calls and invertible monomials, the stated route supports

\[
O\bigl(n(\log n)^{199/200}(\log\log n)^{601/200}\bigr)
=O\bigl(n(\log n)^{.995}(\log\log n)^{3.005}\bigr).
\]

It consequently supports eventual O(n(log n)^.997) in the stated exact-complex, specified-root, charged scalar/index model. No 31-call word is supplied, discovered, or verified. This is not acceptance of an unconditional improved Fourier algorithm, an executable end-to-end implementation, a formal Lean theorem, or a latest-record claim.

The reviewed candidate is `H16_Finite_Win_Admission_and_Conditional_DFT_Lift_2026-10-14.zip`, SHA-256 `258e3f43558c6ceef6e5d752c17ce6817e3c3bd00dcf94a0f9b5855549e15f29`. The five archived files match their saved local counterparts byte-for-byte. The ten saved source snapshots match their recorded SHA-256 hashes, lengths, and Git blob hashes. These are independent local integrity checks; they do not authenticate the repository pins through a new remote fetch.

## 1. Exact finite interface and the shear word

The finite hypothesis must remain a matrix identity on 16 independent inputs. Its monomial factors require actual permutations and nonzero scalars. Ordered pair orientation, chronological order, endpoints, normalization, and every inverse are part of the certificate. Borrowed or initialized seventeenth registers are excluded. Checking all 16 basis inputs over an exact coefficient representation is sufficient for the full linear identity; floating-point agreement is not.

The supplied second word is valid independently of the absent first word. Direct algebra gives

\[
H\operatorname{diag}(2,1)H\operatorname{diag}(-3,1)H
=\begin{pmatrix}-8&-10\\0&-6\end{pmatrix}.
\]

Multiplication on the left by diag(-t/10,-1/6) and on the right by diag(5/(4t),1) gives the upper shear with coefficient t whenever t≠0. Thus the unit shear needs three forward H calls on exactly two coordinates. For any local Fourier coefficient μ, set t₁=1+μ\bar μ and t₂=μ-t₁. The inequality 1+|μ|²>|μ| proves both nonzero, including μ=0. Two three-H words therefore give a fixed six-H pattern without a complex-zero test. Conjugate coefficients are obtained from the shared rational/root DAG at inverse roots, before touching variable data.

Source: local.tex, lines 370–444. The candidate correctly uses the H version of the source's intermediate three-H identity, rather than silently charging calls to its different C kernel as H calls.

## 2. The recurrence and its strict exponent margin

Let j=floor(k/4), with the remaining s=k-4j≤3 axes processed by direct H calls. One finite-word call slot on the grouped axes is (H⊕I₁₄)^{⊗j}. Sectors with r active groups have multiplicity C(j,r)14^{j-r}, width 2^r, and total dimension weight

\[
p_r=\frac{\binom jr14^{j-r}2^r}{16^j}
=\binom jr(1/8)^r(7/8)^{j-r}.
\]

The weights sum to one and E[K]=j/8≤k/32. The factor 2^r is essential: counting sectors equally would give the wrong recurrence. Processing the s leftover axes and the 2^s copies of the grouped routine introduces only constant overhead after normalization by 2^k. All monomial slots, packing, unpacking, singleton sectors, and recursive call descriptions cost O(2^k) per invocation. Therefore, above a finite base range,

\[
f(k)\le C_0+g\,\mathbb E[f(K)],\qquad K\sim\mathrm{Bin}(\lfloor k/4\rfloor,1/8).
\]

For α=199/200, strict contraction follows from 31^200<32^199. To make the induction explicit, choose ρ with 31·32^{-α}<ρ<1. For sufficiently large k,

\[
g(1+k/32)^\alpha\le\rho(k+1)^\alpha.
\]

All K≤floor(k/4)<k there, so induction and concavity give the recursive term at most Aρ(k+1)^α. Choose A to cover the finite base range and C₀≤A(1-ρ)(k+1)^α. This proves f(k)=O((k+1)^α). It does not prove the endpoint exponent log(31)/log(32).

Source: synthesis.tex, lines 205–241; synchronization.tex, lines 6–50. This deterministic active-sector recursion differs from substituting a cheaper fixed radix into an ordinary FFT, which alone would improve only a leading constant.

## 3. Linear sector and monomial costs

The source's mixed-radix prefix tree has fewer than 2R nodes when all genuine tensor radices are at least two. Tensor monomial addresses and scalar products are updated in constant work per prefix, rather than recomputed across all axes at every leaf. Sector starts use

\[
S=\sum_j\left(\prod_{i<j}q_i\right)p_j\tau_j,
\]

with the source's four-state incremental update for start, prefix width, local offset, and original address. A separate block-prefix traversal discovers every sector in O(R), even if an axis has only one block: block-prefix counts are bounded by digit-prefix counts. Width-one sectors are included, not discarded. These statements apply to nonconsecutive and reversed ordered pairs.

For the fixed H16 word, local lookup tables are constant size. Per-invocation metadata polynomial in k is absorbed in O(2^k), with the finite small range handled directly. Recursion can use paid movement arrays and stacks without changing the mathematical 16-register certificate. No free whole-array mutation or uncharged fan-out is needed; rebuilding an output array for a fixed slot is already linear charged work.

Source: synchronization.tex, lines 6–50 and 73–84. The candidate's control code was inspected, but its saved finite test counts are not substituted for the all-size argument and were not re-executed during this review.

## 4. Exact width and coefficient preparation

The compiler first produces monomial/shear layers on exactly r coordinates, with O(1+log^4 r) layers and polynomial work in r. Its measured workspace inequality g+a+e≤v charges every borrowed gate coordinate inside the existing parent block. The compute–copy–reverse/source-suppressed replay restores arbitrary borrowed values. The fallback is effective and occurs only for finitely many small widths. Synchronization is valid by the tensor multiplication identity even when another axis changes values temporarily serving as borrowed coordinates.

Replacing each shear layer by the fixed six-H pattern preserves its exact width and changes depth by a constant factor. A simultaneous pair slot decomposes into H^{⊗k} sectors with k≤ℓ and total width R. The resulting cost is

\[
O(R(\ell+1)^\alpha(1+\log r_{\max})^4)
+\operatorname{poly}(\ell,r_{\max},\log(R+2)).
\]

Local coefficient DAGs remain shared. All divisions in Newton/Toeplitz preparation have the source's nonzero witnesses; all structural choices use integers. Evaluating conjugate DAGs adds only a constant factor to polynomial local preparation. Tensor coefficient products are charged in the full-array term.

Source: local.tex, lines 152–199, 209–365, 370–444; synchronization.tex, lines 73–84.

A rational or Q(i) finite word has fixed finite scalar preparation independent of n. Unknown complex constants cannot be treated as permitted literals. For an existence-based extension, the source's finite rational-algebra extraction can be applied with H and the target fixed rationally and all required unit equations included. A supplied or effectively obtained nonzero finite algebra E, rational multiplication table, basis beginning with 1_E, resolved permutations, inverse witnesses, and exact identities then permit a faithful constant-factor scalar simulation. E's dimension must be fixed before n. This may enlarge scalar implementation storage by a constant factor but does not authorize an extra register in the original H16 certificate. The source's extraction theorem was inspected as a stated/proved interface; no extraction computation was run.

Source: synthesis.tex, lines 92–203.

## 5. All lengths, roots, and the final exponent

For maximal initial-odd-prime product R_ℓ≤2n and minimal e with L=R_ℓ2^e≥2n, the source establishes 2n≤L<4n, ℓ=Θ(log n/log log n), r_max=poly(ℓ), and e=O(log(ℓ+2)). Finding primes, local schedules, CRT tables, and coefficients costs poly(log n); CRT entry permutations use prefix traversal in O(L). The remaining 2^e axis costs O(L(1+e)), which the stated main term absorbs.

Bluestein then uses exactly three charged working transforms: variable-vector transform, the fixed chirp-kernel transform as scalar preparation, and an inverse via reversal/scaling. Chirp tables, padding, and prepared-scalar pointwise multiplication cost O(n). Thus substituting ℓ yields log-log exponent 4-α=601/200, not 4 and not 3. The gap .997-.995=.002 absorbs this fixed log-log power eventually. Direct transforms cover the finite initial range.

The supplied root resource is essential. The explicit order

\[
D_*=(2n)L\,2^{\lceil\log_2(16L)\rceil}<1024n^3
\]

is divisible by 2n, L, and each needed power-of-two local root order. Binary powering extracts the polynomially many local roots in poly(log n) work. The algorithm does not claim to derive arbitrary required roots from ζ_n alone using field operations. All address/index integers are polynomially bounded in n; a fixed number of O(log(n+2))-bit words suffices. Complex field operations remain unit cost, with unrestricted coefficients/magnitudes and no numerical-stability or bit-complexity consequence.

Source: introduction.tex, lines 62–101; all-lengths.tex, lines 14–155. The local comparator snapshot independently states the same one-canonical-root order cap and charged preparation/execution requirements (Sussman_UniformFourierChallenge.lean, lines 24–49 and 305–315). This review checks model compatibility, not the complete imported Lean dependency graph.

## 6. Open obligations and claim boundaries

1. Obtain the absent exact ≤31-call H16 word. No bounded negative topology result establishes or refutes this general hypothesis.
2. Supply the full pair/monomial schedule, exactly 16 independent inputs, nonzero factors and inverse witnesses, and an admissible exact coefficient representation. Independently replay the full identity and mutation controls.
3. If using non-rational constants, actually provide or derive and check the fixed rational-algebra representation; do not assume an arbitrary algebraic-number or coefficient oracle.
4. Bind the actual admitted word to the charged scheduler. An implementation claim additionally needs the full coefficient preparer, exact-width local compiler, sector/CRT routines, all-length reduction, and regression evidence. None is delivered by the finite control script alone.
5. A formal theorem claim additionally needs a complete corresponding formalization and checked build. No Lean build or imported proof audit was performed here.
6. Keep the stronger quantitative direct-compilation route explicit. The general bounded-printer theorem alone concludes only o(n log n), with no comparable fixed exponent supplied.

No mandatory correction to the candidate's scoped conditional statement was identified. These obligations are already substantially disclosed in the candidate; this review keeps them open rather than reclassifying the conditional result as a construction.

## 7. Saved addenda, evidence, and execution scope

The original archive contains five files and no lift addendum. No separately saved H16/lift addendum was located in the candidate directory or the scoped nearby artifact/shared-workspace locations inspected. The earlier earlier exact-width THEORY.md note was read as prior context: it already records the same conditional 199/200 route. It is not a newly supplied witness or an independently replayed historical computation. The independent delete-two/insert-one acceptance report was read only to confirm its separate, bounded-negative scope.

This review ran no historical scientific code, candidate control replay, theorem prover, construction search, or external write. Executed helper code only inspected local bytes and computed hashes. Initial broad listings were truncated and replaced by bounded reads. A nonessential directory-listing attempt was denied; it was not retried, and no required source was blocked. Model input, output, reasoning and total token counters were unavailable; output-size estimates are not model-usage accounting.

UTC timing is recorded in AUDIT_RECEIPT.json.
