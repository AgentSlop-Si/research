# Independent final review: adaptive independent packing

Date: 17 October 2026.

Reviewed report: `../candidate/REPORT.md` (provenance-redacted public copy; see `../../PORTABILITY.md`).

Reviewed SHA-256: `c1317f7f9cbf77d1f9eee41f53a8b5d1ea519653f7516094b8cdb91e1294dda3`.

## Verdict

**PASS, with the report's exact stated scope.** No mathematical defect requiring a correction was found in the closed-prefix lemma, the actual-size independent-call complexity theorem, or the explicit sparse-family sharing escapes.

The proved complexity is for the expressly defined dense-integer, independent-call adaptive completion. The historical producer still performs native integer products rather than this self-recursion. The theorem does not bound a general shared arithmetic graph, a content-aware algorithm, or unrestricted integer multiplication. The report makes these distinctions correctly.

This review independently checked the mathematical argument and relevant retained source definitions. It also wrote and ran new exact diagnostic controls without importing or executing any reviewed program. The asymptotic verdict rests on the proof below, not on the finite controls.

## 1. Native point and legal constant blocks

Let `L_r=lcm(1,...,r)` and `d_r=L_r/r`. The source's CRT chooses a positive `k<=max(1,d_r-1)`, with `P_r=1+k L_r`, and the integer-minimum plan has

- `R_j=(P_r+j-1)/j`, an integer;
- `W_j=binom(P_r+j-1,j)`;
- `beta=W_r/d_r`, an integer;
- `s_r=floor(log2 beta)`.

The CRT residue at each prime power dividing `d_r` is a unit, so its positive representative is nonzero. The prescribed congruences make the requisite prime power divide one of the factors of `W_r`, hence `d_r` divides `W_r`. Also `R_r/d_r=k+1/d_r>1`, so `beta>W_(r-1)` and the retained top canonical digit is legal.

The stated height estimates can be checked elementarily. Every binomial coefficient `binom(r,j)` divides `L_r`: each prime-adic valuation is a sum of zero-or-one carry terms and is at most `floor(log_p r)`. Thus `L_r>=2^r/(r+1)`. Conversely, `L_r` divides `L_ceil(r/2) binom(r,floor(r/2))`; a new prime-power level above `ceil(r/2)` appears in that binomial coefficient. Iterating gives `log2 L_r<=2r+O(log r)`. Since `L_r<P_r<=1+L_r^2/r`,

`r-O(log r) <= log2 P_r <= 4r+O(log r)`.

Finally,

`log2 beta = r log2 P_r - log2(r!) - log2 d_r + O(r^2/P_r)`.

In particular, eventually `r^2/2<=s_r<=5r^2`, and the exact bound `s_r<=r log2 P_r` holds because every radix factor is at most `P_r` and `d_r>=1`.

Consequently any integer `C<P_r` is represented by the constant canonical polynomial whenever `C<2^s_r`. In the proposed prefix, `bit_length(C)=c<s_r` guarantees this latter condition. These are genuine binary blocks, not unrestricted formal coefficient vectors.

## 2. Exact adaptive invariant and actual lengths

For `X=C 2^E`, with `s_r|E` and `c<s_r`, set `K=E/s_r`. Then

`ceil((E+c)/s_r)=K+1`.

There are exactly `K` zero blocks followed by `C`. Each nodal row is therefore `(0,...,0,C)`, with actual maximum `C`. The source's byte-rounded rule is exactly

`w=8 ceil(bit_length(2(K+1)C^2)/8)`.

Both packed operands at every node equal `C 2^(K w)`, and their actual lengths are exactly `K w+c`. This is not an allocated-width estimate. All `2r-1` rows are nonzero, so the zero-row shortcut removes none of them.

The report's real-valued extension of the width formula is also correct. For every positive integer `B`,

`8 ceil(bit_length(B)/8) = 8(floor(log2(B)/8)+1)`.

In particular, at `B=2^(8q)` the required width is `8(q+1)`, preserving the strict separation at the boundary. The exact interval controls independently tested both neighboring integers as well as the boundary itself.

## 3. Closed-prefix existence: the divisibility argument is not circular

Write `ell=ceil(log2 R)`, `c=floor(3R/4)`, `C=2^(c-1)+1`, and `D=floor(R/(16 ell))`. The relaxed process is defined on the full real interval `[2^R, 3*2^(R-1)]` before any integer exponent or divisibility condition is selected.

### Uniformity before selecting a cell

Suppose inductively that the rank is in `[0.9R,R]` and the exponent has not increased. Since `C` has `c` bits,

- the width is at least `2c-O(1)`, which eventually exceeds `1.25R`;
- the width is at most `R+2c+O(1)`, including byte rounding, which eventually is at most `3R`;
- `s` lies between `(0.9R)^2/2` and `5R^2`.

Thus `1/(4R)<=e_(j+1)/e_j<=8/R`. The upper estimate gives contraction for large `R`. The lower estimate gives

`r_j >= R-j(log2 R+2)-1`.

For `j<=D` this exceeds `0.9R` eventually. This is a valid bootstrap induction; it does not assume the final divisibility conditions. Exponents remain exponentially large throughout the prefix. The native point bound then gives `log2 P_(r_j)>c`, and the block width gives `s_(r_j)>c`, uniformly for the whole relaxed process.

### Cell count

On a cell with a fixed previous parameter history, `e_j=alpha_j e` for a positive rational constant `alpha_j`. The initial parameter ratio is at most `3/2`, so both positive affine expressions `alpha_j e+c` and, at a fixed rank, `2(alpha_j e/s_j+1)C^2` vary by a ratio at most `3/2`.

The first can cross at most one consecutive power-of-two boundary, hence gives at most two ranks. Inside either rank interval, the second can cross at most one boundary between consecutive powers of 256, hence gives at most two widths. Therefore each existing cell produces at most four subcells. Through `D` steps there are at most `4^D` cells. Endpoint conventions do not change their lengths; a strictly interior point will be used below.

At least one final cell `J` has length at least `2^(R-1-2D)`. On that cell all `s_j,w_j` are already fixed. Let `S=product_(j<D) s_j`. Uniformly,

`log2 S <= D(2 log2 R+log2 5)`.

The logarithmic separation satisfies

`log2(|J|/S) >= R-1-D(2+2 log2 R+log2 5)`

`>= (7/8-o(1))R`.

Thus the cell width exceeds `S` by an exponentially large factor. Choosing a sufficiently long cell first and then its own modulus `S` is valid because the same bound applies to every cell; the selection is not circular.

### Exact alignment

An integer multiple `E=tS` exists strictly inside `J`. It has the fixed relaxed parameter history of `J`. At every stage,

`E_j/s_j = t (product_(h<j) w_h)(product_(j<h<D) s_h)`,

an integer. Hence each relaxed step is the exact integer source rule at the actual current input length. No earlier parameter is changed by the integer choice, because the choice remains in the same cell. The constant polynomial remains legal at every required level. The lemma establishes the claimed growing prefix, rather than merely a favorable root.

All rank and width breakpoints are rational, so the existence proof can also be made constructive by exact interval enumeration. Efficient witness generation is not a prerequisite of the lower bound.

## 4. Lower bound from actual independently executed work

Set `n_j=E_j+c`. All children at a given prefix level are identical, but the specified policy executes them independently. Their actual volume ratio is exactly

`V_j=(2r_j-1)(E_j w_j/s_j+c)/(E_j+c)`.

Because the prefix has exponentially large exponents and `s_j=Theta(R^2)`,

`w_j >= r_j+2c-O(log R) >= r_j+1.5R-O(log R)`.

Combining this with `s_j<=r_j(4r_j+O(log R))` yields

`V_j >= 1/2+3R/(4r_j)-o(1) >= 5/4-o(1)`.

The errors are uniform over the prefix, and `r_j<=R`. Therefore every prefix ratio is eventually at least `6/5`. The individual child/parent size ratio is `O(1/R)`, so the noncontracting-child guard is inactive there.

At depth `D`, the number of calls is `product_(j<D)(2r_j-1)`. Each input is still exactly `C 2^(E_D)`, whether or not its next transformation stays constant-block aligned. Its returned square has `Theta(n_D)` bits. The specified dense representation and independent execution require each return to be materialized. Counting only these depth-`D` materializations gives

`Omega(n_0 product_(j<D)V_j) >= Omega(n_0(6/5)^D)`.

There is no substitution of a worst-case lower estimate into an upper recurrence and no requirement that the unexamined descendants remain worst cases. Reusing storage between calls does not eliminate the separately required writes; sharing a previously computed return or representing a shifted value virtually would change the specified policy.

The base conversion of logarithms is correct:

`D=(1/16+o(1)) ln n_0/ln ln n_0`.

Thus every fixed `a<ln(6/5)/16` gives the stated lower bound along the witness sizes. For the expressly used worst-case-over-at-most-`n` convention, a witness from the preceding rank interval is within a fixed multiplicative factor of any sufficiently large `n`. Monotonicity of that worst-case function extends the same lower scale to all such `n`.

## 5. Upper bound and complete local work

For a nonzero row, the actual maxima are bounded by `(P_r-1) R(r,x)`. The actual width is at most the corresponding fixed-cap width. Moreover `Q>2L A_x B_x` and the positive integral maxima imply each packed integer has magnitude below `Q^L`. Consequently its actual bit length is at most `L w_x`, and hence at most the fixed cap `t_x`.

The inherited cap calculation is consistent with the retained source definitions. With `lambda=log2 P_r`, `kappa_r=lambda/r`, and minimax translation,

- `log2 L=r-2log2 r+O(1)`;
- `sum_x log2 R(r,x)=J* r^2+O(r log r)`;
- `s_r=r lambda+O(r log r)`;
- `w_cap(x)=log2 L+2lambda+2log2 R(r,x)+O(1)`.

Thus each `t_x=Theta(n/log n)` and

`sum_x t_x/n=4+(2+2J*)/kappa_r+o(1) <= 9.0889395816...+o(1)`.

The row-norm asymptotic can be checked directly: for negative nodes use `R(r,-h)=binom(h+r-1,r-1)`; for nonnegative nodes in the allowed window the truncated binomial sum is between half and all of `2^x`. The minimax limit solves the same crossing equation as the minimum of the resulting integrated logarithmic objective. No new assumption on the native point sequence is needed.

For `Phi_b(n)=n exp(b ln n/ln ln n)`, the difference of the exponential arguments between `n` and any cap child tends uniformly to `b`, so the summed ratio is at most `e^(-b)(v_plus+o(1))`. Choosing `b>ln v_plus` supplies a fixed induction margin. Applying the increasing majorant to cap sizes is valid even if the actual runtime function itself is not monotone in exact input length.

The conservative elementary local-work ledger is sufficient:

- Polynomial native setup on polynomial-bit integers is absorbed by `n(log n)^4` eventually.
- Canonical conversion using `O(r)` schoolbook divisions on `O(r^2)`-bit integers per block costs at most `O(Lr^5)=O(nr^3)`.
- Direct input maps cost at most `O(Lr^4)`.
- Node data, packing streams, and output streams have total `O(n)` bits; bounded-window scans and the charged transpositions avoid repeated whole-integer shifts.
- Finite-difference interpolation and direct evaluation with `O(r^2)`-bit fixed weights fit `O(Lr^5)` using schoolbook products.
- Binary carrying and the output write fit `O(n)`.

Therefore `F(n)=O(n(log n)^4)=o(Phi_b(n))`. Above a fixed finite threshold every cap child contracts, so the fallback guard causes schoolbook work only at finitely many sizes. It is absorbed in the induction base. Neither a hidden large multiplier nor an unproved prime supply is needed.

Together with the lower bound this proves the precise policy's `n exp(Theta(log n/log log n))` worst-case scale. A looser elementary constant bound on the cap volume would already suffice for that scale; the quoted sharper constant is consistent with the inherited analysis.

## 6. Sharing escapes and the perturbed control

### Unperturbed family

A dense scan extracts `E=v_2(X)` and the odd core `C`. Schoolbook multiplication of the `Theta(log n)`-bit core and dense shifted assembly cost `O(n+(log n)^2)=O(n)`. Equal-call memoization likewise removes the `2r-1` branching on the aligned prefix, although the report correctly does not assert that this fact alone proves a complete linear bound for every later descendant.

### Distinct odd perturbation

For `X=C 2^E+P_r`, the low binary block `P_r` is legal eventually, and its canonical representation is exactly the digit `c_1=1`. Its polynomial is `-x`; hence the row is `(-x,0,...,0,C)` and the packed child is `H-x`, with `H=C 2^(K w)`.

All nodes have magnitude `O(r)<<C`, so the actual maxima and widths are unchanged. Since `C=2^(c-1)+1`, the unperturbed `H` has exponentially more than the node magnitudes of slack above its lower bit-length boundary. Subtracting or adding `x` therefore preserves the actual child bit length. The children are pairwise distinct. Because `H` is even, every odd node gives an odd child; any consecutive set of `2r-1` integers contains at least `r-1` odd integers. Also `P_r` is odd because `L_r` is even, so the perturbed root is odd.

The exact shared identity is

`(H-x)^2=C^2 2^(2K w)-(2Cx)2^(K w)+x^2`.

Only one small leading product `C^2` needs sharing; residual products are on `O(r)`-bit integers. The three nonzero outer columns interpolate at `-P_r` to `P_r^2`, `2CP_r`, and `C^2`. Dense node-product construction has total linear size, and reconstruction need only visit these three known supported columns. Native setup and all small arithmetic are polynomial in `r=Theta(log n)`, hence eventually dominated by `n`; full dense assembly is `O(n)`. Recognizing this sparse family can also be done by a dense scan and the computed native point, so the bound need not rely on uncharged input advice.

This positive construction may skip zero columns and share leading structure. Those permissions deliberately differ from the independent policy in Theorem A. It is therefore an escape from that lower bound, not a contradiction. Literal child inequality and root oddness do not imply a sharing-resistant hard instance. The report correctly leaves the arbitrary-input shared route and a closed sharing-resistant lower-bound family open.

## 7. Fresh independent controls

`independent_controls.py` was written for this review. It uses no imported reviewed implementation. Its native CRT is reconstructed with the direct CRT sum formula; its block capacity uses the exact binomial product. Its parameter routine enumerates the entire piecewise-rational initial interval at each tested stage rather than merely locating a cell around one sample.

The completed run verified:

- Entire-interval cell partitioning, exact coverage, at most four children per cell, and the selected interior product multiple at ranks 64, 128, 256, 512, and 1024.
- The prescribed theorem depths at ranks 128–1024: 1, 2, 3, and 6. Rank 64 was deliberately tested for one diagnostic level although its conservative theorem depth is zero.
- At rank 1024, full stage cell counts `1, 2, 3, 4, 4, 4`, with every divisibility, rank, point, width, actual size, and contraction condition checked exactly.
- Fourteen total exact diagnostic levels: 13 levels in the five large-rank tests and one rank-17 materialized level.
- Minimum large-test volume ratios ranging from approximately 1.7193 to 1.8312, all exceeding `6/5`.
- A materialized rank-17 sparse perturbation, all 33 distinct children, at least 16 odd children, exact preserved child bit lengths, the three-term shared square, and all three independent finite-difference evaluations.
- 297 exact width checks at, immediately below, and immediately above byte-boundary powers of two.

These controls are reproducible diagnostics and do not establish any asymptotic claim by themselves. `INDEPENDENT_RESULTS.json` and `RUN.log` preserve the exact outcomes. No external repository, Library item, or source deliverable was changed.
