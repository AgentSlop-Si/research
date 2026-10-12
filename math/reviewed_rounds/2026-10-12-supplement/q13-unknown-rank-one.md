Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: ce359793bfe7c2d1193c0853e5bc7bb0e32c77a7f9d2dec356bdf9304cc7cd7a.

# Independent review: unknown rank-one CHIRP acquisition

12 October 2026 UTC. Verdict: **ACCEPT for the exact bounded standalone implementation and its stated accounting contract.**

This verdict binds `acquire_rank_one.py` SHA-256 `224f42077c1ddcb336379f0c3523c27d73a783aea3a53f3839ddd3c685952668`, report SHA-256 `fcbfb6351be4e4ba63352ba184aa5d61b2125d51d209ef1db08fe7bd5040cbb2`, and the 583,073-byte candidate archive SHA-256 `4fa4e400048d610937b08e34f407c218a3bd0c9b43f7fb87d49c9c3c7d7e480e`. No repair to those sealed bytes is required.

The accepted delta is a no-supplied-phase, no-dense-fallback rank-at-most-one acquisition/decision executor with paid prime/root preparation, both root-group searches, original-input verification, every Fourier output, and exact budget withholding. It is implementation/accounting integration of established mathematics. It does not close Q13 or STR-Q2 as a whole, replace their general-rank APIs, or justify a new canonical theoretical claim.

## 1. Binding, independence, and scope

The reviewer checked the archive CRC, exact manifest coverage, all 25 payload hashes and sizes, all ten source pins against their original local bytes, and agreement with the author's supplied directory. The new executor was copied out of the sealed archive to a review-owned directory. The reviewer wrote independent explicit-family, complete-phase, dense-DFT, stage-ledger, field/domain and interruption controls before inspecting the author's test harness. All final tests ran against the sealed source hash. The fresh author harness was then separately replayed in a review-owned directory; its results and examples reproduced byte-for-byte.

Original uploaded programs and all prior implementation copies remained inert. Only the newly authored candidate, fresh reviewer checkers and fresh author harness were executed. This is an independent project review, not external peer review, formal machine verification, production certification, or a performance benchmark.

The API accepts an exact built-in dictionary with precisely `N,p,omega,x`; `x` is an exact built-in list of canonical integer residues. There is no `r`, phase selector or dense fallback. Integers exclude booleans. The bounded domain is 2<=N<=512, prime 3<=p<=65537, and N dividing p-1. `omega` is a canonical exact-order-N supplied root, or None requests deterministic paid root search. The budget is an exact integer in [0,20,000,000], default 2,000,000. The tighter finite modulus/domain and changed input/output shapes mean this is a standalone API, not a drop-in replacement for the earlier general-rank reference.

INVALID reports detected malformed or out-of-domain conditions, not signal nonmembership. LIMIT is indeterminate and may precede discovery of invalidity. MEMBER supplies the prepared root, a canonical rank-one witness or empty zero witness, and all N positive-sign unnormalized DFT entries. NONMEMBER rejects only the rank-at-most-one Nth-root chirp family and supplies no transform. Outside MEMBER, no public root, representation or DFT is returned. Resident JSON-like built-ins, no concurrent mutation or hostile Python hooks, and no process/OS failure are explicit execution assumptions.

## 2. Acquisition and every-input correctness

The family is zero together with x_j=gamma*omega^(a*j^2+b*j), gamma nonzero. With an exact-order root all nonzero members have no zero coordinates. The implementation validates and reads every coordinate before prime/root validation and classification. Consequently all-zero acceptance is sound; a partly zero input cannot be a nonzero member.

For all-nonzero input, gamma=x_0 and q=x_0*x_(2 mod N)/x_1^2. A genuine member has q=omega^(2a). The cyclic N=2 endpoint is valid: x_2=x_0, canonical phase a=0, and q=1. No out-of-bounds third sample, inverse of two modulo even N, or excluded small-length assumption is hidden here.

Let L=N/gcd(2,N). The map a -> omega^(2a) is injective for 0<=a<L, so the complete paid scan over L even powers finds at most one a. For even N, (a,b) and (a+N/2,b+N/2) give the same samples because (N/2)j(j+1) is divisible by N. This quotient covers all phases. It is crucial to shift b as well. The second group lookup searches all N powers for x_1/(gamma*omega^a), recovering the unique b. Both scans complete even after an early match.

Every genuine member must pass these forced tests. Failure of either subgroup test is therefore definitive family nonmembership, not a heuristic failure. When both pass, the executor reconstructs and compares all N original entries, accumulating mismatches without an early exit. Success proves membership and failure disproves it. The exact canonical phase/frequency uniqueness asserted here is restricted to nonzero rank one; no mixture-uniqueness claim is imported.

Static inspection confirms there is only this one raw candidate verification. No trial-phase dechirping schedule, polynomial eliminant scan, imported dense reference, pre-supplied phase, or hidden DFT fallback is called.

## 3. All phases, all lengths, full Fourier output

For G_a(c)=sum_j omega^(a*j^2+c*j), set d=gcd(2a,N), K=N/d and c0=(-a*K) mod d. Translating j by K multiplies the sum by omega^(K*(a*K+c)); the term depending on j vanishes modulo N. The multiplier equals one exactly for c=c0 mod d. Since the field has no zero divisors, G_a vanishes outside that coset.

Translating j by one gives G_a(c+2a)=omega^(-a-c)*G_a(c). The additive step 2a has order K modulo N, so it traverses exactly the surviving coset. One paid N-term seed sum and K-1 paid recurrence multiplications compute the entire row where it may be nonzero. The executor scales the seed by gamma, zero-initializes all N outputs, and scatters at k=(c-b) mod N. The result equals gamma*G_a(k+b), the stipulated positive-sign DFT.

This proof and implementation cover zero phase, odd and even nonzero phases, nonunits, odd/even composite lengths, and N=2. For a=0 the output is the N-spike at k=-b. For N=6,a=1 the nonzero coset is odd; for N=12,a=2 it is 2 modulo 4. These explicit counterexamples prevent reuse of an unconditional even-support/odd-phase formula. The seed need not be assumed nonzero for correctness; invertibility of the N-point transform, valid because p does not divide N, proves it is nonzero if that fact is desired.

Independent output-kernel tests include the full phase range, not just canonical phases, and compare every returned entry against direct sums. The final representation is independently resynthesized and every accepted transform is independently checked, rather than trusting the acquisition certificate or telemetry.

## 4. Prime/root validation and optional discovery

Trial division proves primality within the domain, with every divisor test and loop test charged. Composite moduli are INVALID even for zero input. Exact-order root verification multiplies successively, rejects a return to 1 before N, and rejects failure to close at N. Successful preparation costs exactly N products, N order tests and N table writes. Tests cover proper-divisor roots and roots not closing at N.

For root discovery, h runs through 1..p-1 and the candidate is h^((p-1)/N). Finite-field cyclicity ensures some candidate has order N. Every failed candidate, modular power and partial root table is paid. If t is the first successful h, H=(p-1)/N, B_H=bitlen(H), M_H=B_H+popcount(H)-1, and d_h is the order of h^H, the exact discovery cost is 1+t*(2+B_H+M_H)+3*sum d_h. Independent enumeration of multiplicative orders reproduced the full stage categories, not merely their aggregate total.

In discovery mode the returned root defines the returned DFT. Different root choices may permute coordinates. The membership family is unchanged because changing a primitive root multiplies both phase and frequency exponents by a unit. The report states this essential distinction. There is no promise of cheap field/root discovery or completion under every finite budget; p itself is always supplied.

## 5. Cost and withholding audit

Let s=floor(sqrt(p)), B=bitlen(p-2), M=B+popcount(p-2)-1, L=N/gcd(2,N), and E be the Euclidean step count starting at (2a,N). For a supplied-root nonzero MEMBER, the independently checked exact total is

    18N + 3L + 6K + 2s + 27 + 2B + 2M + E.

The output stage alone is E+4N+6K. Its category counts are N field additions, K field multiplications, N+K output writes (initializations plus overwrites), K scatter-index events, N+K-1 phase-index events and root reads, K-1 orbit steps, and the stated gcd/setup events. Full raw verification is exactly 5N events. Both inverse square-and-multiply internals are included. A separate instrumented method audit matched actual field-add/multiply calls to the ledger.

All six complete-route formulas in the candidate report were independently checked, including zero, partly-zero, failed curvature, failed frequency and full-synthesis rejection. Optional discovery replaces only the successful supplied-root cost 3N with its full measured R. Invalid cases retain actual prefix ledgers. No rejected attempt is free.

The supplied-root MEMBER field arithmetic is exactly 2N+K+5+2M multiplications and N additions, hence O(N+log p). Complete named work also contains trial division and is O(N+sqrt(p)+log p). Optional root search is worst-case O(p*(N+log p)) named work. Live field-array storage is O(N). The report correctly excludes Python instruction counts, object/telemetry allocation, arbitrary-precision bit complexity, OS CPU/memory bounds and wall-clock claims. This is not an optimized FFT comparison or an unconditional linear cold-request bound in N alone.

The meter charges each named operation before execution, including deferred guard predicates. All public mathematical payloads are constructed only in the completed MEMBER return. Independent traces compare the entire prefix category and stage dictionaries at every unit cutoff in representative success, rejection, discovery and invalid cases. At hard dimensions both denial of the final output overwrite and denial of the final publication event withhold the root, witness and whole transform. Partial telemetry is not a mathematical certificate.

## 6. Executable evidence

Final source-bound counts and hashes are in `INDEPENDENT_RESULTS.json`, `ACCOUNTING_AND_DOMAIN_RESULTS.json`, `ADVERSARIAL_RESULTS.json` and `AUTHOR_REPLAY_VERIFICATION.json`. Coverage includes:

- 881,521 exhaustive raw-vector decisions, using independently enumerated full-phase families: F3^2, F5^2, F7^2, both primitive roots for F7^3/F5^4/F7^6, and all four primitive roots for F11^5.
- 4,655 all-phase structured decisions across every N=2..96; 2,352 even alias identities; 380 arbitrary vectors, 330 tail corruptions, 284 partial-zero cases and 95 zero cases.
- 887,284 complete-route exact total checks and 316,553 independently computed accepted output coordinates, including separate hard-boundary decisions.
- 3,239 all-phase Gauss kernel cases at N=2..80, with 173,879 direct-output coordinates and exact output category ledgers.
- 2,601 every-unit cutoffs across 14 success/rejection/discovery/invalid fixtures, exact completion caps, 18 hard-dimension cases, 18 denied last-output writes and 18 denied publication events.
- 8,920 independent complete stage-ledger predictions, 1,121 searched-root stage ledgers with 35,437 direct output coordinates, 308 zero-input root searches, 1,003 prime/composite cases, eight max-modulus cases including N=512,p=65537, and 44 bad roots on zero input.
- 25 malformed input cases, five invalid budgets, four actual field-call audits, and eight explicit alias/sign/support/damage/order-2N adversaries. First-entry damage that passes both group lookups still checks all 16 raw coordinates before rejecting.

The author replay is separate evidence: its archived same-author totals are reproduced rather than added to the independent counts. Finite coverage supplements the proofs; it is not their replacement. Runtime is diagnostic only.

## 7. Established theory and remaining work

CHIRP v3 C1 already records the curvature identity and reciprocal eliminant convention. C2 already records the even alias. The original audit Section 5 and v3 Section 6 already supply all-length/all-phase Gauss evaluation. The new orbit recurrence is an elementary executable form of those established facts. The accepted supplied-odd executor explicitly left phase acquisition external and used a dense fallback. These sources distinguish the new integration from both prior theory and previously accepted implementations.

Only the bounded standalone rank-one acquisition obligation is complete. The whole phase-acquisition problem remains open. Curvature and Gauss identities retain their earlier mathematical credit; accepted dense, phase-zero, phase-one, supplied-odd and raw-Weyl results are preserved.

Higher-rank structural acquisition, all-phase sparse mixture execution, min(B,H), blocked/Toeplitz integration, production/bit-cost qualification, optimized FFT comparisons and historical priority remain open. Legacy general-rank API/dispatcher integration is not delivered by this standalone API.
