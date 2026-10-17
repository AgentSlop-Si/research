# Independent final review: exact lazy Fermat transforms and coefficient lift

Date: 2026-10-17. Scope: the corrected, frozen files in `lazy/source`.

## Verdict

**PASS for the stated exactness, finite implementation experiment, coefficient representation, and conditional-complexity conclusions. No sub-N-log-N multiplication algorithm or general fast-batching result has been established.**

Two small review findings were corrected before this verdict:

1. Entry extraction now advances an incremental byte/bit cursor. Its linear bit-cost accounting no longer implicitly treats repeated arbitrary-precision multiplication `w*j` as constant or linear time.
2. The fixed-ratio recurrence now distinguishes upper bounds from matching Theta solutions. An O-toll alone is not used to assert a lower bound.

The author's prior bindings are preserved in `SHA256SUMS_pre_review.txt`. The corrected kernel companion is `coefficient_lift.py`, SHA-256 `09877b7a81aff33431b436f6a94437555f0f8f2bb34992f9b18120557746366f`; the corrected report is SHA-256 `14f674e37f9901e62d33f2fb939813a77ac0df60d60e4b272873257e171a1a84`. The main convolution kernel and recorded timings are unchanged. Full bindings are copied into `SOURCE_SHA256SUMS.txt` and embedded in `independent_results.json`.

## Independent execution controls

I read both fresh Python sources before importing them. They use standard-library operations; the lift imports only the inspected fresh transform module. No original uploaded or historical program was imported or executed. The new check runner uses separate seed `0x17411017` and independent arithmetic, defining-DFT, direct-convolution, and division-based digit oracles.

The initial hash gate noticed the author was making the requested corrections and stopped before any candidate import. After receipt and inspection of the final version, the independent checks ran once on its frozen hashes, which matched again at completion. The author's complete validation and timing programs were not redundantly rerun.

All **784,833 counted independent test cases passed**:

| Independent check | Cases |
|---|---:|
| Signed split-fold congruence and exact magnitude envelope | 666,988 |
| Whole-envelope single-correction canonicalization | 19,368 |
| Canonical add/subtract and folded pointwise product controls | 9,296 |
| Canonical/lazy transforms against an independently written defining DFT | 2,400 |
| Polynomial lifts against that independent defining DFT | 1,200 |
| Exhaustive small signed-carry coefficient vectors | 84,245 |
| Bounded-slice entry extraction against repeated-division oracle | 1,248 |
| Fresh full coefficient convolutions and symbolic operation ledgers | 8 |
| Fresh end-to-end integer products in binary/Mersenne radices | 80 |

These checks include negative endpoints, negative exponents, the exceptional residue `2^r`, non-byte-aligned chunk widths, composite Fermat moduli, both transform directions, every timing configuration's operation ledger, and separate full integer-product correctness. They are bounded tests supporting the proofs, not a substitute for the proofs.

## 1. Signed fold and lazy transform

Write `R=2^r`, `Q=R+1`, and `x=a*2^(r-s)+b` with `0<=b<2^(r-s)`. Floor division, including for negative `x`, gives

`((x<<s)&(R-1)) - (x>>(r-s)) = b*2^s-a = x*2^s-a*Q`.

This proves the congruence without any nonnegative-input assumption. For an integer `C>=1` and `|x|<=CR`, the stated lower/upper bounds on `a,b` imply

`-C*2^s <= F_s(x) <= R+(C-1)*2^s <= CR`.

The lower bound is also at least `-CR`. Exponent reduction modulo `2r`, a possible sign reversal, and the zero-shift branch preserve this envelope. Each butterfly doubles it at most, giving `|x|<=2^t R` after `t` stages and `|x|<=KR` at the boundary. The inverse scale is the power-of-two action with exponent `-log2(K)`, since multiplication by that power represents `K^(-1)` modulo the odd number `Q`.

For the boundary fold `z=(x&(R-1))-(x>>r)`, the exact coarse range is `-K<=z<=R+K-1`. The root constraint gives `r>=K/2`, and a power-of-two `K>=2` satisfies `R>=K`. Therefore one addition or subtraction of `Q` suffices. Canonical pointwise operands lie in `[0,R]`; their ordinary product fold likewise needs at most one addition of `Q`. The defining DFT comparisons verify the forward bit-reversal convention and inverse interpretation independently.

The report's representative-width bound is valid. Its measured peak is the maximum absolute bit length of stored stage values, **not peak process memory**. The literal Python expression `x<<s` can allocate a wider temporary before masking; this remains O(r+log K) bits and does not change the asymptotic cost/space conclusions. A bounded low-part extraction can avoid that temporary in a lower-level implementation.

The power-of-two Fermat-ring root and shift/add/negate framework is classical; [GMP's FFT multiplication documentation](https://gmplib.org/manual/FFT-Multiplication) directly describes this construction. This review makes no novelty claim.

## 2. Timing and operation-accounting scope

The recorded experiment compares two branches of the same fresh implementation, using fixed plans, five deterministic random input pairs per configuration, three calls per mode per pair, randomized interleaving, and independent coefficient-convolution checks after timing. The baseline uses conditional correction after additions; it does not unnecessarily fold those additions.

Every timed call to `convolution` includes:

- input array padding/copying;
- both forward transforms and their required boundary work;
- all `K` native integer pointwise products and product folds;
- the inverse transform, inverse scale, and boundary normalization.

It excludes conversion from the original integer to positional digits, plan construction, the independent correctness oracle, and final positional reconstruction. Accordingly, the original recorded canonical/lazy median ratios, approximately **1.0831–1.2572**, support only the stated finite convolution experiment. They do not establish an equal end-to-end multiplication speedup, a comparison with historical code, a guaranteed speedup on other systems, or a new asymptotic exponent. No new timing claim is made by this review.

The exact ledger formulas check out, with `ell=log2(K)` and `F=K*ell/2-K+1`:

- additions/subtractions: `3*K*ell`;
- nonidentity root actions including inverse scale: `3*F+K`;
- native pointwise multiplications: `K`;
- canonical-mode correction calls: `3*K*ell+3*F+K`;
- lazy-mode boundary canonicalizations: `3*K`.

At `K=256`, these are 6,144 additions, 2,563 root actions, 256 native products, and 8,707 versus 768 canonicalization calls. The reduction in corrections does not remove the full-width additions: their charged cost remains `Theta(K*r*log K)` in the stated explicit evaluation model.

## 3. Polynomial coefficient lift, guard growth, and storage

Let `d=K/2`, `w=r/d=2r/K`, and `B=2^w`. Evaluation at `Y=B` induces a well-defined homomorphism

`Z[Y]/(Y^d+1) -> Z/(2^r+1)`.

Every canonical residue below `R` has its ordinary `d` radix-B digits. The exceptional residue `R=Q-1` must be represented by the constant polynomial `-1`; the executable does so. The initial coefficient absolute bound is `B-1`, including that exception. The transform root is represented by `Y`, and its powers act as signed coefficient rotations. Hence exact unnormalized butterfly coefficients satisfy `|c|<=2^t(B-1)` after stage `t`, requiring `O(w+t+1)` bits each. Dyadic normalization cannot remove those exact guard bits.

The live layer contains `K*d` coefficients, so its bit volume is

`O(K*d*(w+t+1)) = O(K*r*(1+(t+1)/w))`.

For balanced `m=Theta(sqrt(N))`, `w=Theta(1)`, so this lift does not have linear final-layer volume: it grows to `O(N log N)` bits. The report correctly rejects that naive claim.

For the skewed parameters

`m=Theta(sqrt(N log N))`,
`K=Theta(sqrt(N/log N))`,
`r=2m+O(K+log N)` aligned to `K/2`,

one obtains `Kr=Theta(N)`, `w=Theta(log N)`, and `t<=log K=O(log N)`. Thus every coefficient has `O(log N)` bits and a constant number of live layers has **O(N) bits**. Overwritten/exchanged buffers suffice. Keeping all historical layers instead costs **O(N log N) bits**; this review does not approve an all-history linear-storage claim. Literal Python object overhead is not measured by the parameter table, which is a bit-volume calculation.

## 4. Paid conversions

The corrected entry routine converts one canonical residue to bytes and extracts each chunk with a bounded slice and incremental byte/bit cursor. Per-residue byte work is `O(r+d)`; charging `O(log r)` bit operations for each cursor update gives `O(d log r)`, which is `O(r)` under `w=Theta(log N)`. The exceptional residue is handled separately. This proves an O(N) entry conversion for the **ring-residue-to-lift boundary**, not for original binary-to-Mersenne positional conversion.

For exit conversion, if `|c_j|<=K(B-1)` and the incoming carry has magnitude at most `K`, then

`floor((c_j+carry)/B)` remains in `[-K,K]`.

The packed digits represent the ordinary evaluation minus the final carry times `B^d`; since `B^d=-1 mod Q`, subtracting that final carry is correct. The resulting value is again between `-K` and `R+K-1`, so a single final correction suffices. Intermediate coefficient/carry/byte-buffer widths are bounded by `O(w+log K)`; no growing Horner accumulator is used. Charging addresses as above preserves O(N) total boundary work for the skewed family.

The lift's inverse uses native multiplication by an inverse as a correctness oracle. The report discloses it. A completed implementation can use the proved signed power-of-two action after evaluation, charging its O(r)-bit work per residue. Original positional conversion and reconstruction still need their own accounting in any future end-to-end theorem.

## 5. Exact remaining batching condition

The representation does not implement a collective batch routine. The current ordinary layer loop is still `O(V*s)` for `s` successive layers. The proposed missing target is a uniform growing-s bound

`O(V*s^beta+V)`, with `beta<1`,

including all signed permutations, transpositions/address movement, carries, and entry/exit changes. Expanding all `2^s` dependencies or omitting table construction/addressing is not a proof of this target. The report correctly leaves it open.

## 6. Recursive child mass and the variable-ratio caveat

In the exact idealized fixed-ratio square-root model, dividing by N and setting `v=log N` gives

`U(v)=rho*U(v/2)+O(v^beta)`.

Summing the geometric recursion yields the report's three **upper bounds**: `O(v^beta)` for `rho<2^beta`, `O(v^beta log v)` at equality, and `O(v^(log2 rho))` for `rho>2^beta`. Matching positive Theta tolls and ordinary positive base costs give matching solutions. The corrected text makes that distinction.

Independently, a specified complete recursion with exact `rho=2` and square-root children has depth `log2(log N)+O(1)` and normalized leaf mass `Theta(log N)`. That particular expansion already costs `Theta(N log N)` in its leaves. The report does not turn this into a lower bound on all algorithms or all structured transformed inputs.

The idealized ordinary zero-padded split has `Kr` near `4N` **before rounding**; it is not a universal exact measured ratio. A native negacyclic setup can approach ratio 2 but does not by itself cross the stated barrier. Actual rounding and child sizes must be included in a completed recurrence.

A uniform child-mass ratio at most `2-epsilon`, a fully charged toll `O(N(log N)^beta)` with `beta<1`, and maximum child size `O(sqrt(N)*polylog(N))` are sufficient: choose a positive `gamma<1` above both `beta` and `log2(rho)`. The induction factor tends to `rho/2^gamma<1`, leaving room for the lower-order toll.

Uniform separation below 2 is **sufficient, not necessary**. For variable ratios, normalized leaf mass contains the product of ratios along the recursion, while total internal cost sums each depth's toll weighted by the preceding ratio product. Ratios approaching 2 from below may accumulate a saving, but approaching 2 alone does not guarantee one. Both the fully charged leaf mass and internal cost must be shown to be `o(N log N)`. The report states this caveat correctly and does not assume independent pointwise products are an unconditional information-theoretic necessity.

## Stopping point

The exact lazy kernel and small-coefficient representation pass this review. The experiment remains a convolution-level finite improvement. The collective-layer/movement bound and total recursive-cost saving remain unproved for this route. No novelty claim, general FFT acceleration claim, or independent endorsement of the cited 2026 preprint's full theorem follows from these files.
