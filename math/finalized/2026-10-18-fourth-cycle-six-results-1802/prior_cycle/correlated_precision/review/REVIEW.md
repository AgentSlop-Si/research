# Independent final review: correlated-product rank and integer-sample precision

18 October 2026 UTC. Candidate: `mersenne_bilinear_guard_20261018_1502`.

## Verdict

**ACCEPT the report’s theorems, implementation, time costs, and storage within their stated models, with one mandatory README/summary scope correction.**

The candidate README’s second bullet omits the report’s sufficiently-large-`H` premise when calling the guard exact for canonical product inputs. Replace it in any release summary with:

“Ordinary integer-point interpolation needs exactly `v2((2L-2)!)` guard bits for arbitrary degree-at-most-`(2L-2)` integer polynomials; this is sufficient for the product service, with canonical-factor sharpness proved here only for sufficiently large `H`.”

The full REPORT.md is already correct. No mathematical proof, arithmetic code, time-cost, or storage correction is needed. The frozen candidate has not been changed.

The accepted results are:

1. At least `2L` separated-input, fixed-precision, ring-bilinear scalar products are necessary for ordinary length-`L` convolution over `Z/(2^H)` when `L>=3`. The claim also holds on the bounded binary-chunk Taylor images. Six products attain the bound when `L=3`.
2. The exact worst-case uniform guard for recovering an arbitrary degree-at-most-`d` integer polynomial's coefficients modulo `2^H` using only values at finite ordinary integer points is `v2(d!)=d-popcount(d)`. The lower bound concerns the information in those samples and permits arbitrary nonlinear reconstruction. Consecutive nodes attain it.
3. For sufficiently large `H`, the same sample-only guard lower bound has witnesses that are products of two canonical `H`-bit length-`L` arrays. The report correctly does **not** transfer this optimality to the smaller `m`-bit original-chunk Taylor image; only guard sufficiency is established there.
4. The delivered guarded service, its integration with the accepted Taylor route, and the fully expanded small-`L` schedule obstruction have complete, correctly scoped ledgers.

No general `o(N log N)` multiplier, lower bound for arbitrary integer multiplication, exact scalar rank for `L>=4`, or obstruction for the odd native `Q_s` interface follows. There is no new FFT performance claim or historical novelty claim.

## Binding and completed evidence

The candidate was copied before execution. The review is bound to candidate manifest SHA-256:

`78c66a1f3dfcf54d4c940cf7cb986b3f8ffb56e2bf95a93646e58fcbebb5d114`.

All 15 manifest payloads and all four pinned dependencies passed verification; the originals were available for direct comparison. The original candidate was not edited. The candidate replay reproduced its published counts and digest:

`4538cc815349354c3cc8f3d749f15c62fd6afb6dc9bb462faee0db4f86e4941d`.

The separately written `independent_checks.py` passed:

- Nine exhaustive enumerations of the binary Hankel space, through length nine, identifying rank one by its row space rather than reproducing the candidate's outer-product enumeration.
- 216 signed, deliberately over-width interpolation cases, with degrees through 64 and target widths through 137 bits.
- 876 controls covering every smaller nonnegative guard for the selected null-polynomial witnesses, including negative integer nodes, plus 44 explicit lost-information detections.
- 21 canonical factorable guard witnesses, with length through 17 and several widths above the stated sufficient threshold.
- 180 odd divisions and 10,908 independently checked carry transitions, including divisors wider than the target precision.
- 48 instrumented guarded services, verifying exact evaluation-product counts, all small-multiply call counts, all odd divisors, and invariance under independent canonical `W`-bit lifts.
- 140 six-product controls, including every basis pair at seven precisions.
- 35 bounded-image unit-coefficient/capacity controls.
- 40 complete products with the delivered terminating Karatsuba default, including every uncarried final coefficient, exact forward lift, and actual sample capacity; digit widths reach 257 bits.
- 54 fully expanded finite schedule controls, with independent exact-integer checks of leaf capacity and minimum-depth inequalities.
- Five complete-residue-node scope controls establishing that canonical `H=1, L=4` products have minimum uniform guard three, smaller than `Gamma(6)=4`; see SMALL_WIDTH_SCOPE_COUNTERCONTROL.json.

Independent digest:

`0c3ceb7f80f9485c93217a99181c593887891ac17b4ff042f4f1b9f05ea88e8b`.

Finite controls supplement the proofs below; they are not asymptotic proofs or timing evidence.

## 1. Fixed-precision rank and bounded-image scope

The algorithm model is precise: fixed left-only and right-only linear forms over `R=Z/(2^H)`, with fixed `R`-linear output reconstruction. Odd divisions are multiplication by units. Precision-changing even divisions, nonlinear extraction/carries, mixed-input multiplication gates, extension-ring products counted as scalars, and value-dependent schedules are outside the claim.

Composing with the invertible Taylor maps preserves this model. Since the original chunk cube contains each standard basis vector, correctness on all basis pairs determines every coefficient of the bilinear tensor. Thus correctness on the bounded image extends to a ring-bilinear identity on all `R^L x R^L`. It is unnecessary, and would be incorrect, to claim that the bounded cube itself fills the ring.

Reduction modulo two is legitimate. The output slices span the `2L-1`-dimensional binary Hankel subspace. If exactly `2L-1` nonzero rank-one product matrices sufficed, their span would equal that subspace, forcing each product matrix itself to be Hankel.

A nonzero rank-one symmetric binary matrix is `vv^T`. Hankelness implies `v_i=v_(i-1)v_(i+1)` at every interior position. An interior one propagates to all positions. If every interior position is zero, at most one endpoint is one: two nonzero endpoints would contradict equality along the anti-diagonal through `(0,L-1)` for `L>=3`. Therefore the only possibilities are the two endpoint matrices and the all-ones matrix. They cannot span dimension `2L-1>3`. This proves rank at least `2L`; the length-two boundary admits precisely the familiar three directions.

The six-product length-three reconstruction is a valid identity over every commutative ring. All six backend products and all five outputs are present, and its non-backend cost/storage are `O(H)` at fixed length. Hence exact rank six follows over every `Z/(2^H)` with `H>=1`.

For the capacity corollary, a product term that survives modulo two has a nonzero pulled-back left form and right form. Each contains an odd coefficient. Varying that chunk through its `2^m` permitted values produces `2^m` distinct residues when `m<=H`. A fixed canonical binary capacity below `m` cannot represent them. Thus at least `2L` prescribed calls each have capacity at least `m`, giving aggregate scheduled capacity at least `2N`.

This concerns uniform maxima for each call, possibly attained at different inputs. It is not a simultaneous inputwise runtime lower bound, and aggregate capacity alone is not an `N log N` lower bound.

## 2. Exact guard and the restricted-product distinction

For consecutive samples at precision `W=H+Gamma`, every leading forward difference is known modulo `2^W`. The integer identity `Delta^k P(0)=k! b_k` follows from the integral falling-factorial expansion of each integer monomial. Write `k!=2^v u`, with `u` odd and `v<=Gamma`. The canonical difference residue is divisible by `2^v`; shifting it retains `W-v>=H` bits of the quotient. Odd modular division then recovers `b_k` modulo `2^H`. The Newton-basis reconstruction introduces no further denominators. This proves sufficiency, including degree zero and one with no guard.

For necessity, `P_*(Z)=2^(H-1)(Z)_d` has a coefficient nonzero modulo `2^H`, while its values at every integer are divisible by `2^(H+Gamma-1)`. The divisibility also holds at negative nodes because the generalized integer binomial coefficient is integral. Therefore all insufficient nonnegative guards yield exactly the same sampled function as zero. Adaptivity, additional integer nodes, and nonlinear postprocessing cannot restore that lost information.

The information model excludes a leading-coefficient readout (often called evaluation at infinity), derivative samples, extension/noninteger nodes, and use of operand coefficients outside the sampled values. The theorem is not a guard lower bound for every possible rank-optimal multiplication algorithm.

The product witness is valid. The two nonnegative rising-factorial factors have degree `L-1`; their product has degree `d=2L-2` and factorial divisibility at every integer. Scaling them by powers whose exponents sum to `H-1` preserves the nonzero target leading coefficient. Each unscaled coefficient is bounded by evaluation at one and hence by `d!`. With `t=bit_length(d!)`, the report's `H>=2t+2` condition safely keeps both scaled factor arrays below `2^H`.

These are unrestricted canonical `H`-bit factors. They are not proved to belong to the narrower Taylor image of `m`-bit chunks. The full report preserves that distinction in its theorem, overview, integration, and conclusions. The rank obstruction and guard obstruction therefore apply to different, explicitly identified models.

The README compression is consequential enough to correct. An independent exhaustive control considers all 256 pairs of canonical one-bit, length-four factors. At guard three, each complete integer-node sample signature modulo 16 identifies one coefficient vector modulo two, so reconstruction is possible. Nodes modulo 16 suffice to represent every integer node by polynomial periodicity. At guard two, the products `Z^6` and `Z^4` collide at every integer node modulo eight but have different coefficient vectors modulo two. Thus the exact sample-only minimum for these canonical inputs is three, although the general degree-six guard is four. This is a finite information-theoretic countercontrol, not a claim about efficient reconstruction and not a Taylor-image guard result. It shows why the report’s wide-factor premise must survive summaries.

## 3. Paid interpolation, time, and storage

The new code routes every represented-value evaluation product to the pinned terminating backend. Other new multiplications are explicit shift/add multiplications by nonnegative small indices. It does not invoke a wide modular-inverse oracle.

For `n=2L-1`, the guarded service realizes exactly:

- `2nL` Horner small-multiply actions;
- `n` evaluation products;
- `n(n-1)/2` modular difference subtractions;
- `n-1` short factorial-update small-multiply actions;
- `nH` one-bit odd-division steps;
- `n(n-1)/2` Newton-to-monomial small-multiply actions, plus additions and all coefficient writes.

The odd-division recurrence has invariant `0<=carry<u`. Its equation `2 carry_next=carry+u q_bit-input_bit` telescopes to the required modular quotient. The implementation reads a fixed source byte buffer and writes a fixed output buffer; it does not repeatedly shift a wide input or grow a whole-width quotient. A carry action costs `O(log u)=O(L log(L+1))` bits, even if `u` is wider than `H`.

Horner evaluation and basis conversion cost `O(L^2 W log(L+1))`. Difference work is `O(L^2 W)`, odd-division work is `O(L^2 H log(L+1))`, and factorial preparation is `O(L^2 log^2(L+1))`. Since `W=H+v2((2L-2)!)=Omega(L)` for `L>=2`, the displayed preparation is absorbed. The direct length-one case is also covered. Hence the full non-product bound is correct.

Live sample, difference, Newton, coefficient, and temporary product buffers cost `O(LW)` bits. The current odd factorial costs `O(L log(L+1))`, also absorbed by `O(LW)`. Backend workspace remains separately charged. The earlier pair-service storage correction is retained as an inherited qualification; this new service does not use that problematic packed pair schedule.

With input product capacity `h<=W`, the complete service bound is therefore

`O((2L-1) K(h) + L^2 W log(L+1))`.

The stated address supplement counts the small-action and bitstream loops consistently with the accepted bounded-window model. The report explicitly restricts its little-o overhead conclusion to that model; under the conservative separate-address charge the bitstream term can already be `O(N log N)`. No stronger machine-model improvement is inferred.

## 4. Integration and asymptotic conclusion

Both forward shifts are correctly requested at sample precision `W`, with each inherited shift's own logarithmic guard additionally paid. Exact forward Taylor coefficients are below `2^(m+L)`. The identity `v2((2L-2)!)>=L-1`, together with `m>=2`, ensures that `W>=m+L`, so these forward residues are exact nonnegative lifts.

At node `j`, a translated polynomial evaluates as the original chunk polynomial at `j+1`. Summing its `L` bounded terms gives the report's strict sample bound `2^m L(2L-1)^(L-1)`. Reduction modulo `2^W` cannot enlarge a nonnegative value. Thus the declared `h` remains valid even when samples wrap.

Guarded interpolation returns the complete raw product modulo `2^H`. The paid inverse Taylor shift then returns the exact original chunk convolution because its nonnegative coefficients are strictly below `2^H`. Extraction, final carries, terminal tail, and full binary output are inherited and explicitly included.

The unsimplified complete ledger includes two forward shifts at `W`, every guarded scalar product and interpolation action, one length-`2L-1` inverse shift at `H`, and the final `O(L(m+log(L+1)))` streams. Under `m/(L log(L+1))->infinity`, its displayed simplified bound follows.

For `L=O((log N)^(4/5))`, the non-product exponents satisfy `2(4/5)(log_2 3-1)<1` and `4/5<1`; the extra logarithmic factors are harmless. Thus those terms are `o(N log N)` in the declared model. The prescribed Karatsuba product charge remains `Theta(N^alpha/L^(alpha-1))`, far larger than the target. This constructive service does not solve the fast-product obligation.

## 5. Fully expanded small-L recursion

The separate recursion theorem is also valid. At a node of capacity `v`, its `2L-1` equal-width children each have capacity at least `v/L`, so their aggregate is at least `(3/2)v` for `L>=2`. Because capacities are nonincreasing and `L(v)<=C(log v)^beta`, every child above the fixed terminal threshold can shrink by at most `C(log N)^beta` relative to its root capacity bound. Every root-to-leaf path therefore has at least `Omega(log N/log log N)` nonterminal levels. For `beta=0`, the stronger logarithmic-depth bound also implies the stated one.

Choose a common depth below the minimum leaf depth. Repeated aggregate growth gives at least `N(3/2)^D` capacity there. Further finite expansion cannot reduce total capacity. The leaf volume is consequently `N exp(Omega(log N/log log N))`, exceeding `N log N` even with linear leaf charges.

Termination, fixed threshold, full expansion, no sharing/combining, prescribed calls, nonincreasing capacities, and the polylogarithmic branching restriction are all essential hypotheses present in the report. The result is not transferred to other parameter scales, arbitrary schedules, or a different native-product interface.

No external service was changed during this review.
