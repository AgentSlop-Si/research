Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, source identity, attribution and limitations are retained. Original source-report SHA-256: 881c49f0daecac0146898c7b17cd04d35ed929eb4efa5067213e54aaebacaac2.

# HERO17 exact seed obstruction: independent ACCEPT

Date: 12 October 2026 UTC.
Disposition: ACCEPT, with the inherited-peeling and separate-direct-sum scope stated below. This is an accepted obstruction to one route, not a new unrestricted Fourier algorithm or closure of the full recovery gate.

## Source-bound candidate

Candidate: HERO17_Exact_Seed_Obstruction_CANDIDATE_2026-10-12.zip, 559,293 bytes.
SHA256: 886b4e68fa21004636523b511b077f0978d03e62ea51391b838b08399891dc71.
Manifest SHA256: ca5511d7e4b456fcef22d75a65ef1a220f2d8eb038064fb35488cd84c908fdb4.
Proof SHA256: 607f32849c92a493616e81999f2b40a3304b464f5f1d889a5c7073b44b10dbe7.
Comparator SHA256: 85bb61ff43b80311e77e62c79a62e42a14144fb940ac59b927a51f76ffb8c161.

All 29 manifest-listed files were verified after extraction. The source-bound cold replay result is recorded separately. Original historical Python files remained inert .py.txt data and were never executed.

## Accepted result

For a>=2 and N>a(a-1), two-known/one-unknown peeling of cyclic triples {j,j+1,j+a} requires exactly a seeds. Any k<a seeds, in arbitrary positions and even chosen adaptively, close at most k(k+1)/2 vertices. The proof is universal: the triangle-merge budget and explicit short-kernel-vector bound cover cyclic collisions, all three solve directions, and lift consistency. The complete independent reasoning is in UNIVERSAL_PROOF_AUDIT.md in the separately preserved full review archive.

For the original HERO17 recurrence, N is odd prime and s=4a mod N. Reindexing X_(4i) gives precisely those triples, and every solve coefficient is a unit under the existing root/field contract. Taking a=floor(sqrt(N)) supplies an all-prime Omega(sqrt(N)) seed family. At N=257,s=64, exactly16 seeds are necessary, so neither12 nor15 suffices under this rule.

The exact minimum is over all legal peeling schedules; it need not equal the historical planner's chosen number. The explicit normalized upper-bound schedule is a fresh comparison construction. Omega(N^(3/2)) is a cost lower bound only when those seeds are evaluated as separate N-term sums. No lower bound for joint evaluation, additional identities, general linear elimination, or unrestricted Fourier algorithms is established.

## Independent controls

Reviewer-created tests, without candidate imports:

- 3,115,936 seed sets containing0, exhaustive up to translation across all integers N=3,...,31 and N=37,41,43,47, for every admissible a and k<a. All obeyed the closure bound, and its maximum k(k+1)/2 was attained in every tested (N,a,k) case.
- 6,000 larger adversarial/random/clustered/seam-crossing seed configurations through N=4093.
- 922 crosschecks against an independently implemented explicit-set closure engine.
- Six excluded-hypothesis controls: below/equal to the no-wrap threshold or at k=a, the falsely extended closure bound fails as expected.
- 2,049 complete finite-field direct DFT fixtures, including every slope and modulation with amplitudes+1/-1 for primes3 through19 in the selected list, plus N257 original matched-field fixtures. The boundary identity passed throughout; 28,269 checks passed independently for each of the three solve directions.

These are exact controls, not the basis of the universal conclusion. The reviewer's first field-test draft required the obvious s=4 mod N normalization at N=3; this was corrected in the reviewer code before the final passing run. It was not a candidate defect.

## Cold matched-field comparison

The fresh comparator's field arithmetic, root orders, Rader indexing/convolution, raw recognition, and counters were independently audited. Both routes pay cold discovery/validation of suitable roots from supplied N,p, separate needed tables, expanded inversions, raw accesses/scans, scheduling and complete output work. Field discovery from N is not claimed. Ordinary-word named events are retained separately and are not a full instruction or bit-cost model.

The reviewer independently derived and checked exact route totals. With I=bitlength(p-2)+popcount(p-2), seeded total excluding shared preparation is 9N+1+4I+2a(N-3); Rader is (9/2)(N-1)log2(N-1)+3N+I. These agree with the complete ledgers.

Cold field totals (seeded / Rader):

- N17: 438 / 457. The small-case win remains visible.
- N257: 10,722 / 10,177.
- N65537: 34,143,770 / 4,915,551.

Full output vectors agree at all three lengths. Direct DFT checks cover all274 small-case coordinates and18 large-case coordinates; a full quadratic direct oracle at N65537 is not claimed. All65,537 large-case recurrence equations pass. The separate baseline suite checks all17 standard basis inputs at N17 plus16 dense fixtures across N17/N257. COMPARATOR_AUDIT.md in the separately preserved full review archive records exact attribution and interpretation.

This comparison is of a fresh single-component executor against a specified same-field Rader implementation. It is not a new multi-component recognizer, the old Phase27 benchmark, a replacement for its installed fallback, or a universal wall-clock ordering.

## Prior art, scope and remaining work

The planar closure bound is established work: Salo–Schabanel, Triangle solitaire (2022), Lemma2 pp4–5 and Section4.1 p9; their 2025 Solitaire of independence Lemma5.1 repeats it, with a related finite-torus discussion in Example4.1. Kirchner's fill matrices precede these. The candidate correctly credits them and gives a self-contained cyclic quotient application. No worldwide priority claim is accepted.

The previously accepted conditional shared-modulation, bounded-B result and its historical implementation qualifications remain. Only a uniform constant seed cap across all slopes within this peeling model is excluded. Complete independent-modulation recovery/rejection, non-peeling output strategies and restricted-slope supply questions remain open. This obstruction does not establish a new FFT speed advance or close the broader recovery problem.


