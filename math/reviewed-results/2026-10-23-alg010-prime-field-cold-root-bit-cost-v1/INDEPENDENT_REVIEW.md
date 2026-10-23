# Independent review: ALG-010 represented-prime-field cold gate

23 October 2026 UTC. Verdict: **ACCEPT_SCOPED**, with the diagnostic implementation clarification below incorporated into the accepted statement. This accepts one root/bit-cost child, not ALG-010 as a whole.

## Binding and independence

The candidate is `alg010_prime_field_cold_20261023_v1`, bound by:

- MANIFEST.json: `de2f60d8d2f8f9a168e8776aad776b2beb76ebdb211ba75a122d719f55a9a488`.
- REPORT.md: `2000241f7fe236608648cedb61fc70b994fb8b19849d72aa6b951eee78e319a2`.
- prime_field_executor.py: `88e65c0764639d13a925a05782560abb5611e75bb00bdf74c68fac96010d1e80`.

All thirteen manifest members were independently checked for size and SHA-256. The original accepted source was independently fetched from the pinned commit, rather than trusting only the candidate copy. Its Git blob is `564d75a070d7c57ab4cff6226026f0dcf2e368fe`, and recovered SHA-256 is `952f1d290c9b71058687de0c663a58ec7883b0465edf12cf72496e1fcce7b2d6`:

https://github.com/AgentSlop-Si/research/blob/019b4052fdb5e0753ed248683a2c09a80590f3d3/math/archive/objects/95/952f1d290c9b71058687de0c663a58ec7883b0465edf12cf72496e1fcce7b2d6__952f1d290c9b7105__README.md

After reading live spreadsheet metadata, the exact current `Research overview!A53:Q53` row was independently read. Its structured values equal the candidate's frozen row. ALG-010 is TO RESEARCH, priority 42; the named cyclic-hypergeometric comparison is already accepted, and root acquisition/bit complexity are recorded open follow-ups. This review does not reopen that comparison or alter the parent status.

[private native worksheet locator omitted; not a scientific source]

The candidate Python and historical source were read as text only. Neither was executed or imported. `independent_controls.py` is fresh code: division-free streaming relation elimination followed by paid normalization, an independently ordered cyclic solve, and separately implemented dense RREF/direct-Fourier oracles. No external state was written. Finite controls corroborate the proof; they are neither author-code execution coverage nor a timing benchmark.

## Accepted statement

Let N=2^n>=4, let p be a supplied prime with N dividing p-1, and let b be its bit length. The input contains all N canonical residues. For an exact supplied primitive Nth root q, the original degree-one finite-boundary relation family is recognized exactly. An accepted input produces every coordinate of its positive-sign q-Fourier transform. A rank-four input returns DECLINE, not a fabricated transform or an always-output result.

The represented-field, bit-charged random-access bound is

    T_prime(p) + O(N b^2 + b^3),

including canonical input validation, root validation, recognition, singular recovery, all failed family-recognition work, complete output encoding and ordinary bounded diagnostics. There are at most six Fermat inversions. The actually used primality validation is deterministic trial division, with conservative cost O((1+sqrt(p)) b^2). This term is not free and can dominate exponentially in b. No fast primality certificate is claimed or assumed.

Under a separate caller-authorized any-root interface, unbiased independent random bits give almost-sure zero-error acquisition of some primitive q, with expected O(b^3) arithmetic bit work and at most 4b expected supplied bits, plus the actual bit-provider tariff. The exact acquired q binds both the recognized family and returned transform. All of q and the complete output must be returned on ACCEPT; q must also accompany DECLINE. There is no completeness claim over the union of families associated with different primitive roots.

## Algebra and endpoint checks

The N-1 source rows are `[x_i, q^i x_i, x_(i+1), q^i x_(i+1)]`, for i=0,...,N-2. Rank four is equivalent to absence of a nonzero coefficient quadruple. The candidate retains at most three normalized pivot rows and detects a fourth pivot without inverting it. Back substitution produces a nonzero null vector otherwise. Reading all N canonical inputs precedes any family DECLINE. Rank below three, zero vectors and vanishing coordinates need no extra promises.

The q power table is built through index N, not merely N-1. Testing q^N=1 and q^(N/2)!=1 is sufficient and necessary precisely because N is dyadic. The table then retains indices 0,...,N-1. N=1 and N=2 are outside this original source interface; so are nondyadic sizes. No endpoint generalization is silently added. In particular, at N=4 there are only three observed relation rows, so every four-vector is in the family. Controls exhaust all 625 vectors in F5^4 for both primitive roots.

Writing L=p0 I+p1 D+r0 S+r1 DS, direct coefficient manipulation gives FL=JF with

    (Jy)_k=(p0+r0 q^(-k))y_k+(p1+r1 q^(-k-1))y_(k+1).

The residual Lx vanishes at the first N-1 positions; its actual last coordinate is retained. Its transform is u_(N-1)q^(-k), with the positive Fourier sign fixed. Dropping that last residual would be incorrect for nonperiodic accepted inputs. Independent controls include 1,231 nonzero-boundary cases, plus 4,992 basis checks of FL=JF for all nonzero coefficient quadruples over F5 and both primitive roots.

Each upper band is either identically zero or has at most one zero because its coefficient polynomial has degree at most one and the root powers are distinct. In the nonzero-band case, cutting after the possible zero leaves N-1 nonzero path edges. The affine path solution has a starting alpha coordinate equal to one; closing the cycle yields either one scalar or a one-dimensional kernel. In the diagonal case, the nonzero degree-one diagonal has at most one zero. A nonzero quadruple cannot make all of L or all of J zero. Thus nullity at most one is proved for this family, not imported from arbitrary sparse matrices.

When J is singular, choose nonzero kernels h of J and v of L. Fourier similarity gives Fv=c h for c!=0. At any j with v_j!=0, orthogonality gives sum_k q^(-kj)h_k=N v_j/c!=0 because p does not divide N. The actual source-input constraint sum_k q^(-kj)y_k=Nx_j uniquely fixes the missing scalar. The candidate forms weights successively and pays for both kernel solves, both weighted sums, division and all-coordinate correction. The argument does not assume invertibility of a potentially zero path edge or infer the source from measurements alone.

## The root contract is substantive, not an output relabeling

Both 2 and 8 are primitive eighth roots modulo 17. For

    x=(1,14,12,1,3,0,0,0),

the relation matrix at q=2 has rank three, with coefficient witness (12,12,7,1), and the full q=2 output is

    (14,14,10,13,1,10,8,6).

At q=8, the same input's relation matrix has rank four and must DECLINE. The other primitive roots give rank three at q=9 and rank four at q=15. Thus an any-root acquisition can legitimately decline this input despite its belonging to a different root's family. Root selection is not a Las Vegas search for membership in the union of all such families.

Even when both transforms are computed, output ordering depends on q. A known odd exponent relating two roots would induce a frequency permutation, but no free discrete logarithm, root identification or permutation oracle is provided here. The acquired root never substitutes for an independently prescribed unavailable root. The acceptance statement is only relative to the exact supplied or returned q.

## Root probabilities, entropy and limit semantics

For m=(p-1)/N, a uniform a in Fp* maps via a^m uniformly onto the Nth-root subgroup: every fiber has size m. Exactly N/2 roots have order N, so half of the nonzero candidates succeed. This holds without factoring p-1 or assuming its odd part is one. Rejecting raw b-bit integers outside 1,...,p-1 preserves uniformity. Every raw draw succeeds with probability r=(p-1)/2^(b+1)>=1/4. Hence E[nonzero candidates]=2, E[raw draws]=1/r<=4, and E[random bits]<=4b. These are expectations, not deterministic caps, and independence/unbiasedness is a provider assumption rather than something established by pseudorandom tests.

Two powers require O(b) modular products per candidate. For t nonzero candidates and d raw draws, the counter-free acquisition tariff is O(t b^3+d b), plus provider setup and work. Every rejected raw draw and failed primitive-root test is included.

- Unbounded acquisition has no finite deterministic runtime bound.
- A T-candidate cap alone has failure probability 2^(-T), but raw rejection draws remain unbounded.
- A D-raw-draw cap has failure probability (1-r)^D<=(3/4)^D, consumes at most Db supplied bits, and has counter-free arithmetic tariff O(D b^3).
- With both caps, the separate exact equalities do not describe the joint stop; 2^(-T)+(3/4)^D is a valid upper bound.
- Zero caps are allowed by the implementation and immediately return ROOT_LIMIT.

ROOT_LIMIT means only that the permitted search effort was exhausted. A primitive root exists under the validated p,N hypotheses. ROOT_LIMIT is neither root infeasibility nor a family DECLINE. Scripted streams and exact finite enumerations independently check these distinctions.

## Inversions and represented-bit accounting

For s nonzero denominators, prefix products, one product inversion and a reverse pass produce all s inverses using one inversion and 3s products in the candidate's simple implementation. Empty batches perform no inversion. These denominators are known before each affine path traversal.

- Relation discovery: at most three pivot inversions, including a rank-four decline.
- Nonsingular target: one path batch and at most one closing inversion; diagonal cases need no more.
- Singular target: one batch, no closing inversion.
- Singular source kernel: one additional batch, again no closing inversion.
- Singular anchor: one inversion.

The maximum is therefore six, not an uncharged collection of O(N) divisions. Every inverse is a^(p-2); the candidate's powering uses fewer than 2b products. Its supplied-root operation envelope 200N+20b safely dominates a direct static count: relation discovery <=26(N-1)+24 non-inversion arithmetic operations; table/operator/residual/forcing preparation 13N; nonsingular target <=10N+4, or each singular path <=8N+4; anchor/correction <=7N+2; at most 12b inversion products. Diagnostic counts are not themselves measurements of bit time.

Canonical residues are bounded by b bits, and unreduced products by 2b bits. Schoolbook modular multiplication and remainder cost O(b^2), comparisons/additions O(b), and each Fermat inverse O(b^3). Since N<=p-1, represented indices have at most b bits. Index arithmetic and data access are charged in a random-access model with length-dependent tariffs; this is not a unit-cost arbitrary-precision field model and does not assert the same bound for a sequential-tape simulation. Memory is O(Nb), with long-run acquisition diagnostic space separately stated below.

The p,N-known wire format has one status byte. ACCEPT adds q and N residues, exactly 1+(N+1)ceil(b/8) bytes; DECLINE adds q, exactly 1+ceil(b/8) bytes; ROOT_LIMIT is one byte. All output conversion/write costs are O(Nb) or smaller. The encoder is an explicit callable to be included in the evaluation workflow, not an already encoded return value of `evaluate`. Malformed inputs raise exceptions rather than the mathematical DECLINE status. Unbounded integer, rational, extension-field or other foreign encodings need their own input conversion/read tariffs and are not covered by silently truncating to canonical residues.

## Required diagnostic clarification, nonblocking for this verdict

The report's phrase that diagnostics “can be disabled” must be read as an optional implementation modification, not a switch that exists in the frozen reference API. `Field` always increments and returns counters; the frozen function signatures expose no disabling argument. This review did not modify the candidate or pretend to exercise a nonexistent switch.

For the actual retained diagnostics, charge the report's conservative additional acquisition work

    O((t b+d) log(t b+d+2)),

and O(log(t b+d+2)) extra counter bits, in addition to normal evaluator costs and any requested serialization. The total counters also include post-root evaluation; if acquisition counters dominate N this extra tariff covers their effect, and otherwise the ordinary O(Nb^2+b^3) evaluator tariff subsumes it. Expected costs remain within the stated expected bound because the raw-draw and candidate counts have geometric tails with uniformly bounded success probabilities.

For a D-raw-draw cap, a safe statement for the frozen diagnostic reference is the arithmetic tariff O(D b^3) **plus** O((Db+D)log(Db+D+2)) conservative counter work, provider costs and required cap/input encoding. Merely fixing a maximum counter width from a cap does not make bit operations on that width free. A T-candidate cap alone still does not bound raw draws. No bare O(Db^3) complete diagnostic worst-case claim is accepted for arbitrarily large cap encodings. This explicit reading resolves the wording issue without changing the algebra, expected bound, source identity or tests.

## Fresh evidence and limits

The fresh controls pass:

- 1,825 raw vectors: 1,545 full-output accepts, 280 rank-four declines, 23,264 checked output coordinates.
- 988 singular recoveries and 1,231 nonzero finite boundaries.
- 4,992 cyclic systems and 4,992 independent Fourier-similarity basis identities.
- Seven complete primitive-root candidate populations, five scripted limit/encoding cases, five exact candidate-tail and five exact raw-tail enumerations, and twenty joint-cap union-bound checks.
- 398 prime/composite validations, nineteen malformed inputs including N=1,2 and nondyadic shapes, and empty/nonempty batch-inversion checks.
- Eight explicit supplied-root output-binding pairs; the root-dependent-family witness above.
- Maximum six inversions observed. One independent-reconstruction witness is p=5, q=2, x=(0,1,0,1), with output (2,0,3,0), coefficient choice (3,1,0,0), nonzero boundary and a singular target. The coefficient choice need not match the candidate's choice, because a relation need not be unique.

These checks use deterministic scripted/pseudorandom values for reproduction; the probability claims follow from exact group/fiber counting, not empirical randomness. All-size correctness and complexity follow from the algebra and static loop reasoning, not a finite census.

For attribution only, Shoup's *A Computational Introduction to Number Theory and Algebra*, version 2.5, Section 3.4, printed page 66, explicitly gives repeated-squaring Fermat inversion in cubic bit time. The original PDF was independently inspected: https://www.shoup.net/ntb/ntb-v2_5.pdf . Section 2.1 of Klamti, Hasan and Karabina, *Efficient Methods for Simultaneous Homomorphic Inversion*, reviews the classical simultaneous-inversion method and attributes it to Montgomery; this review uses only that ordinary-field mechanism, not its homomorphic model: https://cic.iacr.org/p/2/1/36/pdf .

## Table/publication scope

Accept and stop only the selected represented-prime-field cold-root/bit-cost child, with the returned-root-relative DECLINE and diagnostic tariff qualifications above. Keep ALG-010 TO RESEARCH at priority 42. Preserve the completed source comparison and accepted finite-boundary recognizer. Remaining work includes other represented fields, unavailable prescribed-root acquisition, numerical recognition/stability, complete-interface historical priority, caller/fallback integration and unrelated acceleration questions. Do not label this arbitrary-input FFT acceleration, a new mechanism, worldwide novelty, practical speed or whole-owner closure.
