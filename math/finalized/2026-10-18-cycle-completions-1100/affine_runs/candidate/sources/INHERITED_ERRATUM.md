# Required, hash-bound clarifications to the bounded-support dispatcher report

Date: 17 October 2026.

This erratum applies specifically to the following byte-exact artifacts:

- `REPORT.md`, SHA-256 `a2dfcf8d367fa9a4cb5df0599af58c90ea73f384e7d58cc51b9c9b889fd8d707`.
- `shared_dispatcher.py`, SHA-256 `a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06`.

The independent review accepts the report only together with these clarifications. They change no production source, product result, stated asymptotic upper bound, or finite primitive-charge result.

## 1. Section 5: a shifted core does not always reach the fixed elementary base case

The sentence “the implementation's first scan extracts E and its elementary base case multiplies the small cores” is not literally valid for the entire unbounded accepted family with a fixed 1,024-bit base threshold. The cores have O(log n) bits and eventually exceed any fixed threshold.

Replace that explanation with:

> The first scan extracts the input powers of two. A reduced core at or below the fixed base threshold is multiplied by the elementary base case; a larger reduced core is processed by the dispatcher. In the accepted hard family, C = 2^(c-1) + 1 has at most two occupied binary blocks for every block width, so the default support-four recognizer handles every larger core through the certified shared branch. Its cost is O(c + (log c)^12), where c = O(log n). The initial scan and dense shifted output cost O(n), so the complete computation remains O(n). More generally, for arbitrary O(log n)-bit cores, the already proved general upper bound gives (log n)^(1+o(1)) = o(n) core work, which yields the same complete O(n) bound after restoration.

This correction does not claim that the shared branch itself necessarily uses an elementary base multiplication, or that the fixed base threshold grows with input size. A fresh control demonstrates the actual continuation: a 2,049-bit odd two-term core under the default 1,024-bit threshold takes one shared call and no base call after its large binary shifts are removed.

## 2. Section 4: account explicitly for root-wide diagnostic state

The production implementation retains primitive-work counters, count totals, product logs, certificate logs, and rank-plan caches across its recursive calls. Therefore their integer and indexing widths need not be bounded solely by the current child's local width. The statement about a local polynomial-logarithmic ledger should be read with the following additional accounting argument.

Consider a fresh top-level dispatcher call of root width N, with all policy parameters fixed. First bound the arithmetic, stream work, and number of administrative events, excluding the extra bit cost of root-wide counter/index maintenance. The local O(n (log n)^12) bound, cap-child volume, and finite guard base give

S(N) = O(N exp(b0 log N / log log N))

for every fixed b0 > log(v_plus). The number of logged events and stored records is at most a constant multiple of this bound. Consequently all global count values, accumulated charged totals, and list indices have O(log N) bits. Cached ranks number at most O(log N), and even conservative linear lookup/comparison and elementary arithmetic on their metadata add only a fixed polynomial in log N per event. Thus complete diagnostic and bookkeeping cost is at most S(N) times a fixed polynomial in log N.

For any claimed b > log(v_plus), choose log(v_plus) < b0 < b. The factor

exp((b - b0) log N / log log N)

dominates every fixed polynomial in log N, so this additional bookkeeping is absorbed while preserving the stated bound O(N exp(b log N / log log N)) for every such b. No root-wide counter is treated as a constant-time unbounded integer.

For a top-level recognized fixed-support call, the root-wide trace and small-arithmetic event counts are polynomial in log N. The repeated certificate support scans are separately paid as O(N), as detailed in the review. Therefore this clarification also preserves the complete O(N) recognized-branch result.

## Parameter scope

The constants may depend on the fixed base threshold, fixed support limit, verification policy, and chosen exponent margin b - log(v_plus). The finite contraction/guard threshold is included in the induction base. These claims are not uniform when the support limit or base threshold grows with input size, and the fixed-support linear claim does not apply to the diagnostic forced-dense policy. The primitive-charge ratio is a reproducible ledger comparison, not a full instruction-count or wall-clock ratio.
