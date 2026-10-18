# Independent final review: product-service costs and native recursion

18 October 2026 UTC. Candidate manifest SHA-256: `df92828889a1b64ba48ba6030293604579ff6c91928aef1a520aaf08d01fea52`.

## Verdict

**ACCEPT the arithmetic, product-interface theorem, complete time ledger, two-wide homogeneous-charge barrier, and native exponent-potential theorem, with one mandatory storage-scope correction.** No arithmetic-code change is needed.

The general two-wide service's non-backend storage bound in Section 5 must be `O(L(H+t+g))`, where `g=ceil(log_2 L)`, or the shorter `O(L(H+t))` must explicitly assume `g=O(H+t)`. Packed inputs and the materialized packed output have `Theta(L(t+g))` bits. The bound `O(L(H+t))` does not hold for all separately permitted parameters `H>=1`, byte-aligned `t>=8`.

This correction does not change the intended product theorem: there `H=2m+g`, so `g<=H`, and the advertised `O(L(H+t))`, or `O(LH)` when `t<=H`, is valid. It also does not change the optimization barrier under its expressly stated range `g<=t<=H`, the time ledger, or any native-potential result. If backend workspace itself is linear in packed capacity, it dominates this missing storage, but calling these live non-backend buffers backend workspace would obscure the stated decomposition rather than prove it.

Two editorial clarifications are recommended but do not introduce a new premise into the application:

1. In the standalone modular-shift simplification, write `O(nH [n^2 log(n+1)]^a)` when `H>=t`; alternatively declare `m=H`. The more general ambient statement correctly requires both `m>=t` and `H+g=O(m)`.
2. Keep `g<=H` attached to the matching optimized order `Theta_charge((LH)^alpha)`. Without it, the unsimplified pair-service ledger still applies, and its lower charged bound remains valid, but `t=Theta(H)` need not give `S=Theta(LH)`.

No general integer-multiplication lower bound, universal inputwise runtime lower bound for the delivered Karatsuba routine, or lower bound against correlated/shared products follows.

## Binding and completed evidence

The candidate was copied into `candidate/` before execution, preserving the source candidate. Its 16-entry manifest and all 5 pinned dependency payloads passed verification. The copied arithmetic helper is byte-for-byte identical to `retained-source-history/mersenne_kernel_stream_20261018_1243/kernel_stream.py`; its SHA-256 is `920af1051ed9f4bf09631c34bd8444a79855d04e6d1c287635e77e74b2003d85`.

The required `fresh_controls.py` rerun reproduced digest `727f3415ad1166e13d70597634806d458f6abae81f0833edc71aebb8ddebd9b8` and all reported counts: 990 modular shifts, 792 two-wide convolutions, 203,928 carry transitions, 1,008 binary-window round trips, 4,789 small and 175 larger complete products, 80 canonical grouped controls, 1,024 native certificates, and 14 negative-control instances.

The independently written `independent_cost_checks.py` passed:

- 108 modular shifts using a polynomial-Horner oracle, with every full preparation/local/packed call count verified across `W<t`, `W=t`, and `W>t` boundaries.
- 36 complete slab schedules, including `t>H`, partial top limbs, and `g>t`/`g>H`, verifying all output coefficients, stored old limbs, carry transitions, product counts, and operand capacities.
- 105 complete products using the production Karatsuba default, with supplied widths through 257 bits, different slab choices, and every final uncarried coefficient checked independently.
- 1,155 exact native size certificates covering minimal and deliberately enlarged rounded child exponents.
- 372 finite fully expanded native trees, represented by leaf multiplicities, checking the potential with exact integer inequalities rather than floating-point logarithms.

Independent digest: `be135d53cbd1898d583b8a311e7a547a61d36980b512e72309b7f83dcddd0d8c`. These are finite implementation controls, not proofs of complexity.

## 1. Modular precision and complete shifts

The accepted converter review was read, including its mandatory actual-width and unrestricted-group-parameter qualifications. Both are retained by this candidate. The inherited tables have `t=Theta(n log(n+1))`, and their construction does not depend on the ambient coefficient width.

Let `s(i)` be the binary population count, `u_i` the odd part of `i!`, and `U=u_(n-1)`. Multiplying the input diagonal, the common-denominator convolution kernel, and both output odd inverses gives each term

`2^(g+s(j)+s(i-j)-s(i)) u_i/(u_j u_(i-j)) sigma^(i-j) x_i`

which is exactly `2^g binom(i,j) sigma^(i-j) x_i` in the ring modulo `2^(H+g)`. Thus the canonical scaled result has its low `g` bits zero, and removing those bits returns the required unsigned `H`-bit residue. Changing a representative by a multiple of `2^H` changes this complete map by a multiple of `2^(H+g)`; no input-height reconstruction is needed. The actual computational input promise is still bounded canonical residues, or separately charged reading/reduction of longer encodings.

There are exactly `q` packed calls and `5nq` local `t`-bit calls. Including preparation, the number of calls to the common backend is

`3(n-1)ceil(t/small) + 2ceil(log_2 t) + (5n+1)q`,

where `small=round8(max(1,g))`. Independent instrumentation confirmed this count. The two output odd divisions are actual implemented operations. They are not folded into a symbolic oracle.

The unsimplified cost and storage follow the accepted converter. For ambient `m>=t`, `H+g=O(m)` gives `q=O(m/t)`, whether or not the actual target precision exceeds `t`. This is the right uniform reduction to the wide-input bound. The length-one and empty cases are handled directly.

## 2. Final-only product precision and grouping

Polynomial translation is an algebra automorphism over `Z/(2^H)`. Consequently inverse translation of the ordinary linear product of the translated vectors is the original binary-chunk convolution modulo `2^H`. Each exact output coefficient lies in

`[0, L(2^m-1)^2]`, strictly below `2^(2m+ceil(log_2 L))`.

Canonical residue readout is therefore exact. All `2L-1` coefficients are required. A cyclic/negacyclic result without sufficient padding is a different object. The pipeline does not need to reconstruct the potentially much larger redundant intermediate convolution.

The carry bound `carry<=L(2^m-1)` includes each incoming carry and yields `O(m+log(L+1))` bits per operation. Initial extraction and final window assembly are explicit. The terminal carry tail is covered, including outside the very-wide regime; in that regime the entire extraction/carry/output bill is `O(N)`.

For canonical block inputs below `p^d`, `k(p^d-1)^2<2^(2dm+ceil(log_2 k))` proves the grouped coefficient precision. This does not apply to groups of redundant unnormalized Taylor coefficients. Starting from binary inputs requires the accepted canonical conversion and its actual possible extra digit; `k=ceil(L_p/d)` with `d<=L` keeps `kd=O(L)`. Partial groups, the `2k-1` raw outputs, bounded-overlap reconstruction, and parameter encoding remain paid. No claim about freely converting by a huge power `p^d` is used.

A residue modulo an unrelated odd `Q` does not identify the residue modulo `2^H`: integers differing by `Q` give the same first residue and different second residues. Exact interval reconstruction or another proved bridge is necessary. The explicit counterexample is valid.

## 3. Pair schedule, time, storage, and optimization

The included pairs are exactly `r+s<q`. Every omitted term contains `2^(qt)`, so it vanishes modulo `2^H`. The slot bound is strict:

`c<=L(2^t-1)^2<L2^(2t)<=2^(2t+g)`.

Thus packing with byte-rounded `b>=2t+g` isolates every coefficient and all `2L-1` windows are read. Each packed argument has capacity `S=Lb`.

For a row, let `R=2^t`. Including the preexisting stored output limb, the maximal pre-split sum is

`L(R-1)^2+(R-1)+L(R-1)=LR(R-1)+(R-1)`.

Therefore the new carry is at most `L(R-1)`, with no `log q` growth. The carry telescopes along all positions from `r` through `q-1`; only the final carry at position `q` is discarded. Resetting a row carry sooner would be wrong. Final masking handles the partial most-significant limb.

The complete time ledger pays source preparation, repeated right-slab scans, packing, materialized product outputs, all output windows and carry updates:

`O(q(q+1)K(S)+q(q+1)L(t+g)+L(H+t))`.

The last term covers persistent source/result buffers. The pair terms cover the packed buffers and carry work. There is no repeated addition into a growing whole-width coefficient.

For storage, the persistent source and coefficient-output buffers cost `O(L(H+t))`, while the current packed arguments/results and row state cost `O(L(t+g))`. Adding these establishes the corrected `O(L(H+t+g))` plus backend workspace. A direct counterfamily to the unqualified shorter non-backend bound is `L=2^k`, `H=1`, `t=8`: even an all-zero product is materialized by the code as `2L ceil((16+k)/8)` output bytes. This is `Theta(Lk)`, whereas `L(H+t)=9L`.

Under `max(8,g)<=t<=H`, byte rounding changes only constants, and the prescribed call charge is

`Theta(L^alpha H^2 t^(alpha-2))`.

Since `alpha<2`, narrowing `t` increases that expression. For every `t<=H`, even below `g`, the lower estimates `q>=H/t`, `S>=2Lt` give a charged bound of order at least `(LH)^alpha`. When `H>=g`, choosing a byte-rounded one-slab width gives the matching order. When `t>H`, its one call cannot improve this lower charged order. This is an optimization statement for the explicitly prescribed pair calls. It is not a universal runtime lower bound for their data-dependent backend or for a different bilinear organization.

The optional address supplement is nonnegative and cannot remove the obstruction. Using the corrected storage size in its logarithm is safe; it has the same asymptotic logarithmic order as the stated one.

## 4. Native potential, rounded parameters, and exact scope

At every internal node `s=Kd`, the multiple-of-`K` twist condition gives `s'>=K`. If `s'<=2d`, writing `z=p^d>=3` gives

`Q_(s')<=(z^2+1)/2<2(z-1)^2<=K(z-1)^2`,

contradicting the strict decoding bound. Thus `s'>2d`. These facts are exact for every admissible `p`, `K`, and `d`; deliberately enlarging the rounded child only strengthens them.

It follows that `Ks'>=2s` and `(s')^2>=2s`. Hence

`K s' log_2 s'>=s log_2(2s)>=s log_2 s`.

No asymptotic replacement of an upward-rounded size is involved. The inequality is local, so different choices of `K` at different internal nodes are allowed. Summing it over any finite fully expanded tree gives the leaf-potential bound. Termination is an explicit hypothesis, not a consequence asserted for every even root exponent or every parameter choice. Some choices cannot contract, which is fully compatible with this conditional theorem.

With all leaf exponents at most a fixed `s_0>1`, leaf exponent volume is at least `s log s/log s_0`. At fixed `m`, the associated fixed-width leaf volume is therefore `Omega(N log N)`. When `m` grows across a supplied family, it gives only `Omega(N log s)`.

Charging each leaf explicitly at `Theta((m s_leaf)^alpha)`, with uniform constants, yields the stronger `Omega(m^alpha s log s)=Omega(N m^(alpha-1)log s)`. This extra assumption is essential to the very-wide conclusion. The current implementation can skip work on numerical values, so the homogeneous ledger cannot be promoted to its universal inputwise runtime lower bound. A fixed-width fully expanded implementation realizes that ledger, but different backends, radix changes, and shared correlated point products are outside the theorem.

No further arithmetic or complexity correction was found within these scopes. No external service was changed.
