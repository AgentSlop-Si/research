# Binary Newton packing: actual child sizes and a closed recursion barrier

17 October 2026. New mathematical deductions and fresh exact controls. No historical program was run. No external file was changed.

## Result and stopping boundary

The remaining direct-recursion gap can be closed for a precisely defined implementation family. Three results are proved here:

1. A single family of legal binary inputs simultaneously forces the actual input maxima at every ordinary-value node to attain its Pascal row bound within a polynomial factor. A legal final constant block then makes each packed integer's **actual** length asymptotic to its allocated length. Thus the existing one-level objection is not merely an artifact of charging unused guard space.
2. The translated node window that minimizes the maximum row norm also asymptotically minimizes the sum of logarithmic row norms, hence total independent packing volume. Its asymptotic packing-volume ratio for the native point is

   V_r = 4 + (2 + 2 J*) / κ_r + o(1),
   κ_r = log₂(P_r)/r,
   J* = 1.5444697908028986… .

   Elementary bounds give 1−o(1) ≤ κ_r ≤ 4+o(1). Consequently V_r is at least 5.2722348954…−o(1), and at most 9.0889395817…+o(1), for the cap schedule defined below. The actual legal-input witness has the same leading formula. This is stronger than the source's allocated-volume lower bound 4−o(1).
3. The completely specified, uniformly padded, independent-node recursive implementation terminates, computes the exact product for every signed binary input, and has full bit complexity

   T(n) = n exp(Θ(log n / log log n)).

   All nonrecursive work is performed with elementary arithmetic and charged. No faster integer multiplier is imported. More precisely, for every a < log(5.2722348954…) and b > log(9.0889395817…), its cost is Ω(n exp(a log n/log log n)) and O(n exp(b log n/log log n)). Here and only here, `log` in the exponent and constants is natural logarithm.

The third statement is an actual lower and upper bound for this **fixed-capacity padded recursive schedule**, not a lower bound on the source's input-adaptive program or arbitrary multiplication. The first two statements apply to the source's per-node signed-packing sizes on the stated legal input family. They do not imply that all descendants of those inputs remain worst cases. Keeping these two scopes separate is essential.

This closes the named direct independent-packing branch: it supplies actual-size witnesses, the optimal translation cost, and a solved noncircular all-cost recursion. A sub-n-log-n multiplier, a contraction using shared information between nodes, and a compatible growing prime-Mersenne family remain unproved.

## 1. Source interface and exact definitions

The new archive is `fft_outside_crt_progress_2026-10-17.zip`. Relevant source texts are:

- `fft_outside_crt/asymptotic/PACKING_AND_FULL_COST.md`, especially §§1, 4, 6;
- `fft_outside_crt/asymptotic/packed_outer.py`;
- `fft_outside_crt/audit/BOUNDS_AND_NODE_WINDOW.md`;
- `fft_compact_followup/encoding/MINIMAL_DENOMINATOR_THEOREM.md`, §3;
- `fft_fused_next/binary_alignment/BINARY_BLOCK_SPLIT_THEOREM.md`.

These were inspected as text. The earlier binary archive was also read/materialized. The supplied exact conversation link was unavailable to this worker, so no claim relies on unseen conversation content. Source timings and historical validation counts are not newly verified here.

At rank r≥2, use the source's native integer-minimum plan:

- E_r = lcm(1,…,r), d_r = E_r/r;
- P = 1+k E_r, where k is the source's least positive solution of the specified small-prime-power CRT class, and 1≤k≤max(1,d_r−1);
- R_j = 1+(P−1)/j, 1≤j≤r;
- W_0=1, W_j=∏_{h=1}^j R_h = binom(P+j−1,j);
- β=W_r/d_r, s=floor(log₂ β), ρ=2^s.

The native CRT is explicit: for each prime ℓ dividing d_r, let q=ℓ^{v_ℓ(d_r)} and let u be the largest power of ℓ not exceeding r; impose k≡−(E_r/u)^{-1} modulo q. These coprime q have product d_r, and each residue is a unit. Choose the least positive CRT representative (k=1 when d_r=1). Then q divides R_u, so d_r divides W_r. Also R_r/d_r=k+1/d_r>1, proving β>W_{r−1}. All modular inverses here involve known coprime integers and are obtained by elementary extended GCD. A binary block b<ρ≤β has the canonical expansion b=∑_{j<r} c_j W_j. For j<r−1, 0≤c_j<R_{j+1}≤P; the top digit is also <P. In falling coordinates, its polynomial is

   f(x)=∑_{j<r} (−1)^j c_j binom(x,j), so f(−P)=b.

Use m=2r−1 consecutive integer nodes x=−a,…,2r−2−a, with 0≤a≤r−1. Write

   R(r,x)=∑_{j<r}|binom(x,j)|,
   A_cap(x)=(P−1)R(r,x).

For two input rows of length L and maxima A_x,B_x, the source's byte-rounded signed packing chooses

   w_x = 8 ceil(bit_length(2L A_x B_x)/8),
   Q_x=2^{w_x}>2L A_x B_x,
   U_x=∑_{j<L} f_j(x) Q_x^j,
   V_x=∑_{j<L} g_j(x) Q_x^j.

One integer product U_x V_x gives the exact row convolution by centered radix-Q_x decoding. The allocated child width is L w_x. The zero-row early exit is irrelevant to the witnesses below, whose every row is nonzero.

### Native size estimates without a prime-distribution conjecture

Put λ=log₂ P. Then

   r−O(log r) ≤ λ ≤ 4r+O(log r),
   s=rλ−O(r log r)=Θ(r²).

For completeness: every binomial coefficient binom(r,j) divides E_r, because its p-adic valuation is a sum of at most floor(log_p r) terms, each zero or one. Hence E_r≥2^r/(r+1). Also E_r divides E_ceil(r/2)·binom(r,floor(r/2)): every new prime-power level above ceil(r/2) occurs in the binomial coefficient. Iteration gives log₂ E_r≤2r+O(log r). Combining E_r<P≤1+E_r²/r proves the displayed λ bounds. Finally

   log₂ β = rλ−log₂(r!)−log₂ d_r+O(r²/P).

For a declared n-bit call, take r=floor(log₂ n) and L=ceil(n/s). Then log₂ L=r−2log₂ r+O(1), Ls=n+O(r²), and κ_r=λ/r lies in [1−o(1),4+o(1)]. All asymptotics below use this regime.

## 2. A simultaneous legal height-saturation lemma

### Construction

For each j=0,…,r−2 include an input block with the single nonzero canonical digit

   c_j = floor((R_{j+1}−1)/2).

Also include an all-zero block and end with the constant-only block P−1. Both operands contain this collection; their interior order may differ. All other interior blocks may be arbitrary legal binary blocks. There are only r+1 required blocks, whereas L grows exponentially in r divided by r².

Each singleton is legal:

   c_j W_j < W_{j+1}/2 ≤ W_{r−1}/2 < β/2 < ρ.

For sufficiently large r, the last constant is also <ρ. The blocks are therefore genuine binary chunks; no unrestricted coefficient box has been substituted for the legal encoding.

### Simultaneous saturation

At every node in the allowed window,

   (P−1)R(r,x)/(12r²) ≤ A_x,B_x ≤ (P−1)R(r,x).       (1)

To prove the lower bound, the final basis term satisfies

   |binom(x,r−1)| ≤ 2|binom(x,r−2)|

throughout −r+1≤x≤2r−2 (with zero terms interpreted directly). Thus the sum over j≤r−2 is at least R(r,x)/3. At least one of those r−1 terms is at least R(r,x)/(3(r−1)). Its available singleton digit is at least (P−1)/(4r) for sufficiently large r. Their product proves (1). The upper bound follows from the canonical digit cap P−1.

This one family works simultaneously at all 2r−1 nodes, even though different singleton blocks can provide different node maxima. The zero block also ensures that the range certificate has genuine width. For r≥3 the row vectors are pairwise distinct: the j=1 singleton distinguishes different x, while the nonzero constant block precludes nontrivial proportional equality. The argument does not depend on duplicate node rows.

Equation (1) gives, uniformly across nodes,

   log₂ A_x=λ+log₂ R(r,x)+O(log r),
   w_x=log₂ L+2λ+2log₂ R(r,x)+O(log r).              (2)

### Actual integer lengths, not only allocations

The final row coefficient is C=P−1 at every node. Since Q_x>2L A_xB_x and both maxima are ≥C≥1, each lower-row coefficient is less than (Q_x−1)/2 in absolute value. Hence

   (C−1/2)Q_x^{L−1} < U_x,V_x < (C+1/2)Q_x^{L−1}.

In particular these packed integers are positive despite signed interior values, and

   bit_length(U_x), bit_length(V_x)
      = (L−1)w_x+λ+O(1)=Lw_x−O(r).                (3)

Summed over nodes, the gap from allocated volume is only O(r²), negligible against n. Each actual child has Θ(n/r) bits, and the aggregate actual and allocated widths have the same leading constant. Consequently, for any fixed real exponent A, substituting a size-only majorant n(log n)^A into the direct independent-child recurrence has a leading right/left ratio V_r>1 on this family. This rejects that induction; it does not assign worst-case cost to the particular structured children.

To enforce the source's rank selection from **actual** input length rather than a padded promise, choose L=floor(3·2^{r−1}/s) and the same final C block. The actual length N=(L−1)s+bit_length(C) lies between 2^r and 2^{r+1} for sufficiently large r, so floor(log₂ N)=r. This supplies an infinite exact family in the source's parameter regime.

### Constant row-centering cannot remove the leading cost

The rows contain zero and a value of magnitude at least the left side of (1). After any common additive center at a node, the maximum magnitude remains at least half the row's diameter. Therefore constant per-node centering changes these logarithmic maxima by only O(log r), not Θ(r). Its correction products would still need to be paid. This statement does not cover arbitrary index-dependent residual representations.

## 3. Total logarithmic height and the translation optimum

Let

   S_r(a)=∑_{x=−a}^{2r−2−a} log₂ R(r,x).

There is an exact telescoping identity:

   S_r(a+1)−S_r(a)
      =log₂ R(r,−a−1)−log₂ R(r,2r−2−a).            (4)

The first endpoint term increases with a and the second decreases. Thus the exact total-log objective has a single crossing, with at most two adjacent minimizers. Let k be the first integer with R(r,−k)≥R(r,2r−2−k). Both the source's minimax objective and S_r attain their minima among k−1 and k. They need not choose the identical one at finite r. The restriction 0≤a≤r−1 loses no total-log minimizer: for a<0, shifting left replaces a larger nonnegative node by a smaller one and strictly decreases S_r; for a≥r−1, the new negative endpoint has larger row norm than the removed endpoint, so S_r strictly increases. This supplies an exact monotone-search rule for total precision without multiplying all row norms.

For a=αr+O(log r), 0≤α≤1, define

   f(u)=(1+u)log₂(1+u)−u log₂u, with f(0)=0,
   J(α)=∫₀^α f(u)du +(2−α)²/2.

Uniform Stirling estimates and a Riemann sum give

   S_r(a)=r²J(α)+O(r log r).                        (5)

For negative nodes, R(r,−h)=binom(h+r−1,r−1), producing the integral. For every nonnegative x≤2r−2, the truncated binomial row contains at least half of the full row, so log₂ R(r,x)=x+O(1), producing the second term.

Now J'(α)=f(α)−(2−α), and J''(α)=log₂((1+α)/α)+1>0. The unique minimizer α* is exactly the source's minimax crossing:

   f(α*)=2−α*,
   α*=0.5482418475607564…,
   J*=J(α*)=1.5444697908028986… .

A closed expression is

   J(α)=[(1+α)² ln(1+α)−α² ln α−α]/(2 ln 2)
          +(2−α)²/2.

Thus minimizing the sum of logarithmic packing widths cannot recover a different asymptotic gain by simply translating the same consecutive nodes. Byte rounding contributes O(r) to the summed widths, and the witness's polynomial saturation loss contributes O(r log r); neither changes the leading result.

Combining (2), (5), m=2r−1, log₂ L=r−2log₂ r+O(1), and s=κ_r r²+O(r log r), gives

   L∑_x w_x / N
      =4 + (2+2J*)/κ_r + o(1).                    (6)

By (3), (6) also holds for the sum of **actual** child argument lengths, using the larger of the two operands for each child. There is no extra factor two for counting two inputs in (6): n and each child size use the ordinary maximum-operand-width convention.

## 4. Define the recursive executor before claiming a lower bound

The following is a concrete, deliberately fixed-schedule completion of the remaining direct recursion. It preserves binary outer blocks, the same retained Newton encoding, integer node maps, and independent packed ordinary node products.

At a call with two signed integers of declared magnitude width at most the positive integer n (including zero inputs):

1. If n<16, use fixed-width schoolbook multiplication and return. Otherwise choose the native plan, r=floor(log₂ n), its minimax translation, and L=ceil(n/s).
2. Encode exactly L binary blocks, including leading zeros. Form the 2r−1 node rows.
3. Use the fixed input-independent cap A_cap(x)=(P−1)R(r,x), and choose w_x from Q_x>2L A_cap(x)², byte-rounded exactly as above. Set t_x=Lw_x.
4. If any t_x≥n, use schoolbook at this call. Otherwise recursively compute every one of the 2r−1 packed products at declared width t_x, even if a row or its leading region is zero. No equal-row memoization or structured-input shortcut is part of this defined executor.
5. Decode all centered row convolutions. At each output block, interpolate the degree-at-most-2r−2 ordinary product from its consecutive node values and evaluate it at −P. Normalize at binary radix ρ, assemble the result, and restore its sign.

The source uses data-dependent maxima and Python multiplication, so this is a defined recursive variant, not a claim that its historical code already executes these steps.

### Correctness and termination

Canonical encoding and f(−P)=b establish the input interface. The fixed cap bounds all row entries. The strict Q_x inequality uniquely separates every signed convolution coefficient. Ordinary interpolation at 2r−1 distinct nodes reconstructs the degree-at-most-2r−2 product; evaluation at −P therefore yields the convolution of binary input blocks. Binary carries give their exact ordinary integer product.

All recursive arguments have magnitude below 2^{t_x}: |U_x|≤A_cap(x)(Q_x^L−1)/(Q_x−1)<Q_x^L, and the same holds for V_x. The sign is passed separately. The integer floor defining r, ceil defining L, exact bit_length defining w_x, and byte rounding add at most the explicitly bounded O(r log r) total error in the volume formula; they do not change t_x=Θ(n/log n). Whenever a recursive call is made, t_x<n by the explicit guard. The recursion therefore terminates. Moreover t_x=Θ(n/log n), uniformly across nodes, so all sufficiently large calls pass that guard. The fallback affects only finitely many sizes and does not create an artificial asymptotic stopping point.

## 5. Full nonrecursive cost, without borrowing a fast multiplier

All local products and divisions can use ordinary schoolbook bit algorithms. The following conservative ledger suffices; it deliberately favors clarity over optimizing a branch already proved noncontracting.

- Native point, LCM, factorization up to r, prime-power CRT, weights, node-offset comparisons, and row norms: polynomially many operations on O(r²)-bit integers; O(r⁶) is a safe setup bound.
- Binary splitting and packing: O(n), using bounded windows rather than repeatedly shifting the entire integer.
- Canonical inner conversion: at most O(r) divisions per block, on O(r²)-bit integers. Charging O(r⁴) to each division gives O(Lr⁵)=O(nr³).
- Input local maps: O(r²) coefficient products per block, each on O(r)-bit integers; O(Lr⁴)=O(nr²). The source's factorial-free Pascal factorization may be retained, but no asymptotically fast version is needed for this conservative bound.
- Node-major/block-major rearrangements: O(n log r) in the fixed-tape accounting. Stored node data and packed streams have O(n) total bits.
- Fixed-cap certificate calculation, signed stream packing and centered extraction: O(n) stream work plus the already charged polynomial setup. There are no auxiliary primes, roots, field reductions, or CRT reconstructions in this packed variant.
- Output interpolation: successive finite differences cost O(r²) additions per output block. Evaluate the Newton difference expansion at the fixed integer −P+a. Its weights have O(r²) bits; O(r) schoolbook products per block, each conservatively charged O(r⁴), give O(Lr⁵)=O(nr³). Generate the fixed weights once in polynomial setup. This is exact integer evaluation, with no uncharged cancellation assumption.
- Binary carries and output: O(L(s+log L))=O(n), plus the mandatory output write.

Thus the complete nonrecursive work is bounded by

   F(n)=O(n(log n)^4)

for all sufficiently large n, after absorbing O(r⁶). A linear amount of materialization is mandatory at every non-leaf call. All scalar products not in F are exactly the recursively listed packed products. There is no external multiplication oracle and no hidden prime-supply assumption.

## 6. Solve the padded recurrence

For this fixed-cap schedule,

   t_x=Θ(n/log n),
   ∑_x t_x/n = V_r
      =4+(2+2J*)/κ_r+o(1).

Set v_−=4+(2+2J*)/4=5.272234895401449… and v_+=4+(2+2J*)=9.088939581605797… . Then v_−−o(1)≤V_r≤v_++o(1).

The mandatory padded work has a lower recurrence ∑ child work + Ω(n); the full implementation has an upper recurrence ∑ child work + O(n(log n)^4). Because child schedules depend only on declared capacities, these inequalities hold simultaneously at every recursive node for every input. No assumption about adversarial descendants is being inferred from a one-level witness.

For fixed c, let

   Φ_c(n)=n exp(c log n/log log n).

Uniformly for t_x=Θ(n/log n),

   [log n/log log n]−[log t_x/log log t_x]=1+o(1),

and consequently

   ∑_x Φ_c(t_x)/Φ_c(n)=e^(−c)(V_r+o(1)).          (7)

If c<log v_−, the right side is eventually >1. Induction from a sufficiently large fixed base interval gives T(n)=Ω(Φ_c(n)); the source of the lower bound is the actual compulsory padded work.

If c>log v_+, the right side is eventually <1 by a fixed margin. Since n(log n)^4=o(Φ_c(n)), a sufficiently large constant multiple of Φ_c absorbs F(n) and the finite base interval. Induction yields T(n)=O(Φ_c(n)).

This proves the stated n exp(Θ(log n/log log n)) full complexity. The upper and lower estimates match in this scale, not in their leading exponential constant; no limit for the native sequence κ_r is asserted. In particular the padded independent recursion is asymptotically slower than n(log n)^A for every fixed A. This is a completed cost analysis of a defined exact algorithm, not a lower bound manufactured from an upper-bound recurrence.

## 7. What is and is not settled

Settled here:

- Unused allocated space is not the explanation for the one-level expansion: the legal family forces actual child lengths of the same leading size.
- Per-node precision, constant row-centering, byte rounding, and a different translation of the same consecutive window do not create a leading contraction in this branch.
- The fully padded independent-node self-recursion has a proved complete complexity, legal inputs, exact decoding, and a noncircular stopping rule.

Not settled:

- The cost of the source's genuinely input-adaptive self-recursion. A legal worst case at one level does not prove that every structured child is a worst case at the next level.
- A batched or fused representation that exploits correlations across the 2r−1 node rows, changes the requested intermediate output, or replaces independent signed Kronecker packing.
- A universal lower bound for integer multiplication, FFTs, CRT, linear algebra, or all polynomial-packing algorithms.
- Historical novelty. The new work here is the explicit legal saturation/actual-length lemma, total-volume calculation, and scoped recurrence completion in this research chain, not a claim of priority over the literature.
- The original fixed prime-Mersenne specialization. The archive's native P=1+k lcm(1,…,r) is not asserted to equal (2^m−1)^g. Binary outer alignment fixes the outer conversion issue but does not manufacture a compatible prime-Mersenne point family. On any such compatible family with suitable short-point bounds, analogous size accounting can be instantiated, but existence remains a separate gate.

The justified stopping condition is the closure of the precisely defined direct independent-packing branch above. Advancing the broader multiplication target requires a different, explicitly produced sharing/recovery mechanism or a different compatible interface; neither is claimed to have been supplied.

## 8. Fresh controls and evidence

`fresh_controls.py` is new, standard-library-only arithmetic. It imports no historical source. It independently rebuilds small native plans from the stated CRT congruences, tests legal singleton encodings, computes integer binomial rows, packs and decodes signed outer products, and evaluates products by finite differences. Small whole products are compared against ordinary integer multiplication solely as an oracle.

It also checks the exact telescoping identity and adjacent-minimizer theorem for ranks 2–64, and computes exact cap/actual-length metadata at ranks up to 256 without allocating their exponentially long outer arrays. These are arithmetic controls, not speed measurements and not substitutes for the proofs above. The run passed 63 exact shift ranks, 8 complete integer products comprising 96 signed node convolutions, and 9 large metadata ranks through 256. `CONTROL_RESULTS.json` and `RUN.log` record the completed run; `SOURCE_PINS.json` pins the inspected source files.
