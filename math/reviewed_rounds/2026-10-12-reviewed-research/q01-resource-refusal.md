Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 3d4a2d6b7bdc86878fa503c37eb4414fecd59e30083c2514bd87b1ec5e1a9e27

---

# Independent review: Q01 bounded packed-execution refusal

11 October 2026 UTC. **ACCEPT, bounded scope only.**

## Verdict and binding

The exact candidate archive is `Q01_Packed_Execution_Resource_Blocker_CANDIDATE_2026-10-11.zip`, 123,029 bytes, SHA-256 `209045e1b53af25d3b67a831a44f13c939ba4bf934ca49a06a085a97797e3504`. Its report hash is `34112d5914004b2f54f3136240215d8adef6960e3166263d6cc4fa2f2e56a6b0`; its SHA256SUMS hash is `d81fcdee64c066056811c2d10cd47acaf96a68c413ba9a6400b418ba6ee78124`. All 28 archive members and 12 source-file pins were verified. Acceptance applies to these bytes, not later revisions.

Accept the design-specific mathematical resource obstruction, exact bounded fail-closed diagnostic, and four isolated theorem-precision coefficient/quantizer diagnostics. No blocking defect remains in that scope. This closes the resource-blocker alternative of Q01::admitted-execution only for the stated finite resource caps and frozen eager design. It does not qualify a complete executor, its actual literal-budget success, a universal computational lower bound, or a new asymptotic or priority claim.

In particular:

- Every guard-admitted nonzero all-length eager packed path has backend exponent v>=704, original N>=2^701+1, and strictly more than 2^352 mandatory response words and response-write instructions.
- A preparation-storage or preparation-instruction cap <=2^352 prevents that complete eager build. It does not by itself prevent the paper algorithm from taking a zero shortcut or scalar fallback.
- An original-output-write cap <=2^701 prevents any fully materialized result for those lengths, including zero/fallback results. This is a write bound, not a claim of N simultaneously stored output words.
- At N=2^701+1, t=2, the source's own enormous M=2^704 preparation cap passes the response-cardinality lower bound. Actual fully charged preparation remains unimplemented and unverified. Large diagnostic caps return only NECESSARY_BOUNDS_PASS_EXECUTOR_UNIMPLEMENTED.

## Independent derivation of the threshold and counts

The exact accepted conservative rule, not the rejected alternative packing rule, is used. With backend target T, p=T+10+ceil(log2(v+1)), k=ceil(log2(2v+p+6)), b=2(p+k+1). Require 8b<=v; set P=2 below 32b, otherwise select the largest power of two P<=v/(16b). This preserves the old packing at the old guard. P is a power of two, P>=2, 32bP>v, and 2bP<=v/2. All packed response fields and keys therefore fit the sufficiently wide fixed-multiple growing-word model. No fixed 64/128-bit claim follows.

The all-length wrapper uses M=nextpow2(4N), n=ceil(log2(N+1)), T=t+10 and t>=2. It also requires T<=v+1, 4t<=n, M>=16(t+16), and 2(16(t+16)+1)+2<M. These are the exact source guards tested by the diagnostic. In particular T>=12; the direct-dyadic T=2 threshold cannot be substituted.

For fixed v, b is nondecreasing in T. The valid range below the first possible all-length guard thus reduces to T=12 and 11<=v<=703. An independent piecewise computation gives the following constant-(p,k,b) spans:

- 11..15: (26,6,66); 16..31: (27,7,70)
- 32..47: (28,7,72); 48..63: (28,8,74)
- 64..110: (29,8,76); 111..127: (29,9,78)
- 128..238: (30,9,80); 239..255: (30,10,82)
- 256..493: (31,10,84); 494..511: (31,11,86)
- 512..704: (32,11,88)

On every span restricted to v<=703, its largest v is less than 8b. At v=704, equality first holds and P=2. For every larger v with T>=12, p>=32 and k>=11, so b>=88. This finite exact exclusion plus monotonicity proves the all-size statement; finite random or sampled tests are not being promoted to a proof.

For R=2^b, Q=2^(p+10), S=R^P and d=log2(P), independently counting the separate literal arrays gives HP=S^2, unary phase arrays=(Q-1)S, small-stage arrays=dS, scalar F=QR, scalar H=R^2. Thus

    E_response = S^2 + (Q-1+d)S + QR + R^2.

HP alone has exponent 2bP>=352, and every other family is positive. Hence E_response>2^352, with at least one write per one-word entry. At the first guard, Q=2^42, R=2^88, S=2^176 and d=1, giving exactly

    2^352 + 2^218 + 2^176 + 2^130.

The wrapper length identity gives 2^(v-1)<4N<=2^v; at v>=704, integer N>=2^701+1. The source explicitly writes every output, including zeros. These arguments do not depend on coefficient values, certificate constants, or successful generation of any table entry.

For context only, T=2 direct dyadic packing first passes at v=544. Wrapper targets t=8,16,53 first pass at v=800,928,1552. These distinct interfaces were independently verified.

## What the resource checks do and do not pay

The literal backend preparation caps remain M instructions and M words, and the wrapper separately retains N instructions and N words. The response count omits positive costs for all Q coefficient certificates and storage, the leading-bit table, exact arithmetic, reads, loops, counters, scratch, cleanup, and wrapper preprocessing. Successful table-cardinality checks cannot pay these costs. Likewise the reported small/large lookup counts do not constitute complete execution instruction ledgers. Normalization, padding, bit reversal, scalar output decoding, short interpolation sums and output writes remain charged in the paper theorem.

The existing proof establishes an implementation-dependent eventual finite threshold because accepted preparation is o(M); it does not identify the first guard pass as successful construction. This review preserves that theorem-level existence. A declared smaller cap can make the specific request impossible without contradicting existence at enormous finite capacities. No conclusion is drawn for changed precision, compressed/lazy/reachable-only tables, helper aliasing, other algorithms, or implicit outputs.

The Python preflight is a necessary-bound diagnostic, not a cost-certified RAM implementation. It uses exact integers and refuses out-of-domain v>100000, explicitly as a diagnostic limit. Its public parameter factory, all-length preflight and budget constructor reject malformed types, including booleans. Direct Parameters construction is an internal unvalidated record operation and is not an accepted public validation boundary. Hypothetical forced packing has a separate 200000-bit cardinality-exponent ceiling. Exact integer arithmetic avoids floating log/power misclassification at huge length boundaries.

No table allocation, fallback execution or transform execution occurs. Every returned status leaves executor_admitted false; source-required wrapper/backend fallback is distinguished from an eager resource refusal. The 2^128 storage/work/output cap with 128 address bits produces four explicit refusals before any response-array allocation. The stronger address-width limitation is compatible with the accepted sufficiently wide C(c)(v+1)-bit source model.

## Actual-precision coefficient and total-map review

The isolated scalar state really uses v=704, T=12, p=32, k=11, b=88 and g=42. A real field contains 44 bits; valid exponent fields run from 1 through 1445, representing exponents -736 through 708. Every field 0 or greater than 1445 decodes to zero, independent of its sign and fraction. The quantizer truncates toward zero, underflows below 2^-736, clips at 2^709, emits canonical zero, and stays on the common lattice 2^-768. The independently authored reference truncates a scaled integer lattice representation, rather than using the candidate's logarithm or exponent-search quantizer.

For the four actual-grid phases 0, Q/4, floor(Q/7), Q-1, an independent rigorous rational enclosure used fixed 64/24-term Machin arctangent brackets and a fixed degree-128 sine/cosine Taylor polynomial, with its factorial remainder and Lipschitz angle uncertainty. Each resulting narrow true-value enclosure lies inside the candidate's enclosure, and each saved dyadic coefficient is within 2^-42 of both endpoints, strictly. Its complex grid error and the accepted phase-floor bound therefore satisfy the source coefficient contract. The scale bracket was checked independently by squared rational inequalities for 1/2, establishing error below 2^-42.

These are four valid coefficient instances at the real theorem precision. They do not certify the other Q-4 coefficients, an entire chosen source-generator trace, its polynomial-bit instruction costs, or any packed table. They are deliberately insufficient for complete executor acceptance.

The saved exact witness is verified with independent rational arithmetic. Its input states are representable; the coefficient meets the allowed grid certificate. The split transition rounds c*b before the scaled sum/difference and rounds the outputs again. Its output differs from the one-round alternative. The independent additional controls found 332 such distinctions in 1200 transitions. One may not silently merge the two quantizers. Unreachable extreme states test total semantics, not a failure of the normalized reachable-error theorem.

## Fresh execution evidence

Only newly authored diagnostic/reviewer programs were executed. All predecessor texts and original research programs remained inert. An isolated replay of the candidate's fresh run_checks.py regenerated all 28 members byte-identically. The independent suite passed:

- 12 source hashes and lengths, and the candidate archive/member bindings
- 54,885 parameter cases, plus the exact 693-case first-guard exclusion
- 81 independently predicted combinations immediately below/at/above the storage, work, output and address lower bounds
- 180 arbitrary-bigint wrapper cases, including exact powers of two and adjacent lengths up through v=100000
- 46 public malformed/out-of-domain input refusals
- 13,572 actual-precision quantizer comparisons
- 4,824 malformed-code controls, covering every malformed exponent field, both signs, and four selected fraction patterns
- Four independent rigorous coefficient certificates and an independent scale bracket
- 1200 independent actual-precision scalar transitions; 332 distinguish two rounding sites from one; the saved witness is reproduced exactly

See INDEPENDENT_RESULTS.json, INDEPENDENT_RUN.log and AUTHOR_REPLAY_RESULT.json. No complete Q-grid, response table, transform, wrapper, fallback, RAM instruction trace or performance benchmark was produced.

## Scope and remaining work

The bounded resource-refusal alternative is accepted. Eager preparation refusal and materialized zero/fallback output refusal are different claims. The general executor remains unimplemented, actual literal-M-cap success unverified, and existing proof/precision/family distinctions remain. This does not show that the literal source M-budget fails at v704, or that every finite packed execution is impossible. Model-matched priority and ALG033 remain separate.
