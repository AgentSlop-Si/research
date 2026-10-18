# Independent final review: short-limb factorial setup

18 October 2026.

## Verdict

PASS for the scoped construction, exact arithmetic, and stated bit-complexity upper bounds. No blocking correction is required.

The forward/reverse odd-factorial table products can be computed in

O(n W (log(n+1))^(log_2(3)-1)).

Consequently the accepted wide-digit conversion interface, with N=Lm and m>=cL for a fixed positive c, has the paid bound

O(M(CN) + L M(Cm) + N (log(L+1))^(log_2(3)-1)).

This discharges the previous independent N-log-N-scale prefix/reverse setup obligation. It does not discharge the same-scale convolution, full-width diagonal, modular inversion, matrix-transform, correlated point-product, or growing-prime obligations. It does not prove a complete sub-N-log-N multiplier or a speedup for an implementation's wall-clock runtime.

## Exact reviewed binding

The candidate directory is `../candidate`. An immutable-for-this-review copy of its eight supplied files is retained under `reviewed_candidate/`.

- Candidate manifest SHA-256: `c2cb358873a0ebe29c324f3baf56e239fd1db02b9f523b180fe8ff2219890ee3`
- Report SHA-256: `01dc8f12ad16d11ff99b2ea958cd40580c7a3d1e4b6ed7c27bd8b40e6503baf2`
- Fresh code SHA-256: `3ed1b8ade5028c45067051794505505a3452dd037e999f9c3b6fa03d21659dbe`

All seven manifest entries and all four separately pinned source reports match. The two prior accepted conversion reports were read for the inherited interface, cost assumptions, and previous setup obligation. The negacyclic source reports were read for the separate native-recursion/matrix scope. No historical program was imported or executed. After inspection, this review executed only the newly written candidate snapshot and its own new test driver.

## Streaming lemma and carry widths

Set t to the specified byte-rounded bit length of U-1, R=2^t, and q=ceil(W/t). Since k<U<=R, every input limb a satisfies 0<=a<R and k<R.

For k>0, the invariant 0<=c<k implies

a*k+c <= (R-1)k+(k-1)=Rk-1.

Thus the next carry is again less than k and has at most t bits; the pre-split value has at most 2t bits. For k=0 the initial and all later carries are zero. The partial final limb needs no special arithmetic rule: the discarded carry is multiplied by R^q, which is divisible by 2^W, and masking the last output to W bits is exact.

The telescoping prefix identity proves the output is x*k modulo 2^W. This is a complete modular product, rather than a remainder-only or carry-dropping approximation.

Exactly q short products are performed. With input and output processed through fixed windows, the charge is O(q(K(t)+t)+W+t). The formula retains the q=1 case when W<t. The once-only conversion to/from buffers and final W-bit mask are linear in W+t. The candidate does not repeatedly shift an entire W-bit operand or add into an ever-growing result.

The theorem is an arithmetic-core construction in the report's sequential-bit/array model. Sequential input and output cursors suffice; the theorem is not a literal interpreter-overhead analysis of Python object allocation, arbitrary-precision loop indices, or timings. This qualification is already explicit in the candidate and is important when using the result.

## Independently terminating short multiplication

The difference-form Karatsuba split has h=ceil(t/2). Each low/high part lies in [0,2^h), and the magnitude of a difference of two such parts is less than 2^h. Therefore all three recursive argument pairs have at most h bits, including the signed middle product after magnitude conversion. Restoring its sign and computing the cross term require only O(t)-bit additions, subtraction, and shifts.

The fixed 16-bit shift/add leaves terminate independently of the proposed Mersenne multiplier. The recurrence K(t)<=3K(ceil(t/2))+O(t) gives K(t)=O(t^(log_2 3)); ordinary rounding to the next power of two handles ceilings. There is no uncharged extra-bit recursive child and no growing diagnostic counter inside the routine.

Substituting this K into the streaming charge gives O(W t^(alpha-1)+t^alpha), alpha=log_2 3. For the table application, t=Theta(log(n+1)) and W>=n+2 for n>=2, so t=O(W), including byte-padding constants. Consequently both terms sum over 2(n-1) products to O(n W (log(n+1))^(alpha-1)). For n=1 there are no short-factor products.

Constructing all odd parts o_i in O(n log^2(n+1)) and storing/scanning the O(nW)-bit tables fit within this charge because W>=n and log^2(n+1)=O(n). No full factorial or large radix power is constructed by the algorithm. Full factorials appear only in correctness oracles.

## Preserved Taylor shift and complete ledger

The odd factorial and inverse recurrences preserve their residues exactly. The single terminal inverse is still computed by paid Newton precision doubling. Under the inherited regularity conditions on M, its cost is O(M(W)); it is not included for free in the short-factor improvement.

For 0<=i<n, popcount(i)<=g=ceil(log_2 n), so all initial exponents g-popcount(i) are nonnegative. The valuation identity gives the required exact factor 2^g times the binomial coefficient. Odd denominators are units modulo 2^W. With W=H+g, dividing away the g zero low bits preserves H result bits. The strict coefficient bound below 2^(H-1) makes centered signed reconstruction unique.

The packed-convolution width b=8ceil((2W+ceil(log_2 n))/8) prevents every inter-slot carry: each coefficient is strictly below n*2^(2W)<=2^b. It therefore uses one paid multiplication of S=nb-bit-capacity operands, plus O(nW) bounded-window work. The input and final diagonal maps use 2n full-width products. All these operations remain separately charged.

The resulting ledger is exactly O(M(S)+n M(W)+nW(log(n+1))^(alpha-1)). The candidate code's native multiplication syntax outside the oracle consists only of size/index operations and list allocation; represented-value multiplication uses the supplied explicit routine.

In the accepted conversion regime, n=O(L), W=O(m), and S=O(N). The constant C depends only on the fixed wide-digit ratio and fixed number of conversions. Grouping into p^d uses the inherited local interface and the separately charged bound (L/d)M(Cdm)+L M(Cm)+N(log(d+1))^(alpha-1); monotonicity of M(t)/t aggregates the first term into O(M(CN)). The new grouped finite tests establish positional identities only, as the report correctly says; they are not a new fast grouped-matrix implementation.

Since alpha-1 is approximately 0.584963<1 and log(L+1)=O(log(N+1)), the revised setup is o(N log N) uniformly over 1<=L<=N as N tends to infinity. This is a proved upper bound for the specified construction, not a lower bound on the old one. No primality is used in this improvement, and the report correctly retains the distinction between supplied wide Mersenne digits and fixed-prime native recursion.

## Fresh independent controls

The candidate's complete saved result was reproduced exactly, including its digest and every count. The separately seeded review driver additionally passed:

- 16,384 exhaustive small Karatsuba products and 168 larger split-boundary products, up to 4,097-bit operands
- 1,182 short products with independently traced prefix invariants and carry-width checks, including W<t, partial limbs, W up to 32,769, and factors with 66-bit capacity
- 6 instrumented cases verifying exactly ceil(W/t) outer short products and halving contraction at every recursive child
- 54 odd-factorial/inverse tables against independent factorial and modular-inverse oracles
- 1 empty-shift case and 144 signed shift/inverse cases against direct binomial sums
- 234 exact local Mersenne quotient cases, including byte-window overlap and boundary remainders
- 52 binary/canonical-p round trips and independently generated signed-carry normalization cases, including composite Mersenne radices

The tests do not establish asymptotic complexity or performance. Those conclusions depend on the explicit proofs above. Files `independent_checks.py`, `INDEPENDENT_RESULTS.json`, and `INDEPENDENT_RUN.log` contain the reproducible evidence.

## Corrections and usage notes

No blocking correction or unproved replacement premise was found. As an optional editorial cleanup, README.md could use log(L+1) in place of log L, matching the main report's expression at L=1. The report already treats that boundary correctly, so this does not affect acceptance.

The candidate's VERDICT.json still says independent review is pending. This review is the independent acceptance artifact for the exact hashes above; any later candidate edit should be resealed and separately bound rather than silently treated as reviewed.
