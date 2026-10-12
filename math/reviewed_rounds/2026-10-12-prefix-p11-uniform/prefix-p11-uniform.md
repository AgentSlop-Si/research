# Independent review of the p=11 uniform PREFIX slice

12 October 2026 UTC. Independent project mathematical and computational review.

## Decision

ACCEPT the stated p=11 parameter-uniform theorem for every prime r>11. No mathematical repair is required. This is a scoped additive acceptance under NEW-16; the broad mixed-prime gate remains progressed-open. This is independent project review, not external peer review or proof-assistant certification.

## Statement audited

The group is D8 of order eight times C11 times Cr, with r>11 prime. The objective scores all nonempty left-prefix stabilizers by |S_j|-1, including the full prefix once. The subgroup B is generated only by proper-prefix stabilizers. The asserted values are unrestricted maximum 300r-88 and full-escape maximum 278r-88, with sharp deficit 22r. Orders are actual labeled permutations, without a symmetry quotient or a restriction to signature representations.

The claimed unrestricted equality characterization is recursive consecutive right-coset blocks of actual maximal subgroups, with optimal local orders, and unique top B. The exact count is A(1)=1 and A(K)=sum_J [K:J]! A(J)^[K:J] over actual maximal subgroups for nontrivial K. At the top the four contributions are 2 A(C4×C11×Cr)^2, 4 A(C2²×C11×Cr)^2, 39916800 A(D8×Cr)^11, and r! A(D8×C11)^r. This has no full-escape optimizer classification/count consequence.

## Symbolic reduction

Coprime powering splits every subgroup into its D8 component and its subgroup of the cyclic odd factor. All maximal subgroups are normal of prime index 2,11,r. The proper maximal orders are exactly 44r,8r,88. The maximal-prefix barrier works both before and after the invariant prefix: earlier quotient support is a nonempty proper subset of a prime cyclic quotient, while a later prefix contains a full coset whose outside-J orbit would fill the quotient. Thus full escape excludes those stabilizer orders. No converse is asserted.

The intermediate-set compatibility argument does not require arbitrary D8 subgroups to be nested or permutable. For actual stabilizers L×Ce and R×Cf, comparable numerical two-part orders allow either saturation of the earlier prefix by Cf or the intersection of all Ce-translates of the later prefix. Centrality gives a subgroup of least-common-multiple order preserving the intermediate set. Free action gives its divisibility. An endpoint can be attained only if this order equals the corresponding actual stabilizer order. Consequently every escaping permutation maps to an independent set of precisely its proper-prefix weight. Graph realizability in reverse is unnecessary.

The new graph obligation is alpha≤190r-87. Period 88, low types (2,4,8,11,22,44), high normalized types (1,2,4,11,22), 161 high vertices, 175 categories and 1050 category/type bits follow directly. Low conflicts vanish only at distances greater than 88. The exact-period edge (88,8),(176,44) must remain. A mixed common multiple has integer rank after division by r, proving constancy within each open band and the asymmetric endpoint permissions. High/high edges reduce by canceling r.

The three-mask state records every future restriction. The low stream is infinite and periodic; residual bits past the finite endpoint do not affect the maximum. A low selection shifts the stream and adds its future low and high conflicts; a high selection adds its high and category conflicts. Processed category/high bits are erased. Max-merging identical masks is exact because they have identical legal continuations.

## Independent implementation and unbounded induction

The reviewer read the current manuscript and source, then authored audit_engine.py without importing or executing any author or predecessor mathematical program. It computes conflicts using floor/ceiling endpoint intervals; author mixed conflicts use explicit rank enumeration. Its vector Bellman propagation takes coordinatewise maxima. Different coordinates may maximize on different histories, which is conservative and appropriate for checking the affine upper inequalities.

Certificate envelopes must cover all 40 reduced residues modulo 88 and all 88 bands. The reviewer checks exact types, including rejecting Boolean coefficients, state uniqueness, all mask widths, and erasure of past bits. The proposed domain is t≥9,8≤n≤t. The eight-cycle base is checked through its t-slope and value at t=9. For a transition n<t, the domain is exactly t=9+v+q,n=8+q with v,q≥0. Thus the two ray inequalities compare A and A+C, while the cone vertex compares 9A+8C+D+w with the destination's 9A+9C+D. Every base and cycle destination must be represented.

At n=t, the envelope becomes (A+C)t+D. Fixed tails and affine high-boundary rewards preserve it. The target terminal slope is 16720 and the t=9 target is 190(792+rho)-87. Once all finite inequalities pass, this is a theorem for every reduced abstract parameter t≥9, not an extrapolation of fitting samples.

For the remaining range, every prime 11<r<792 must be verified. Complete coverage of small composite parameters is neither needed nor claimed. The reviewer authored finite_checker.cpp using exact fixed masks and signed 64-bit scores on this bounded range. Mask capacities match the proved widths; score arithmetic is far below overflow. Its deterministic primality test is independently compared with a Python sieve. Its small cases agree with the independently written Python recurrence and absolute graph solver. The C++ code is newly authored, compiled with warnings treated as errors, and not a historical executable. A temporary compile warning about indentation was fixed before any executable was generated; no mathematical output came from that failed compilation.

## Exact finite controls

The separate absolute-position graph control enumerates all allowed divisor vertices and checks every pair against the compressed masks. It then solves the whole graph by one absolute future-mask recurrence, with ordinary increasing-type tie order, which can interleave low and high vertices and is distinct from the compressed high-first convention. It does not reuse compressed states in optimization.

- r=13: 1338 vertices, 894453 pair checks, optimum 2383.
- r=19: 1884 vertices, 1773786 pair checks, optimum 3523.
- r=89: 8254 vertices, 34060131 pair checks, optimum 16823.

These finite comparisons corroborate the uniform compression; they do not replace induction.

Actual group controls use tuple coordinates (i,b,c,t) with D8 multiplication (i,b)(j,d)=(i+(-1)^b j,b+d). Every left translation is updated for every prefix of both r=13 witnesses. Each witness therefore gets 1308736 translation/prefix checks. The unrestricted order gives score 3812 and |B|572; the escaping order gives score 3526 and |B|1144. Every stabilizer size agrees with a separately derived fiber profile.

The witness signatures retain ordered type (2,2,2,11,r), left-to-right multiplication, last coordinate fastest, and flattened D8 orders (0,4,2,6,1,5,7,3) and (0,1,2,3,4,5,6,7). The odd factor has score 21r-11. The product-fiber identity follows from the unique partial outer fiber and the stabilizer at complete-fiber checkpoints. The first complete odd fiber and later D8 checkpoints establish both B values. This gives attainment for all primes in the stated scope.

A separate exhaustive D8 subset dynamic program gives maximum 12 and exactly 2432 labeled optimizers. Enumerating all ten actual subgroups finds one cyclic and two Klein-four maximal subgroups; the count recurrence gives 2·8²+4·24²=2432.

## Equality and labeled counting

The strict escape deficit excludes B=G from unrestricted optimizers. In the nonescaping case choose maximal J containing B. At every insertion the global stabilizer lies in the active local prefix stabilizer in the right J-coset. Summing local scores counts each nonempty local prefix once, with final correction N-|J| and nonnegative losses |L_j|-|S_j|. Every required proper subgroup is either abelian or a direct product of two prime-power groups, covered by the pinned accepted baselines. Their maxima produce 300r-88.

Equality forces all local scores optimal and all losses zero. At the first completed coset the global stabilizer equals J; every other coset must then be empty, forcing the initial consecutive block. Repetition forces all later blocks. Conversely, consecutive locally optimal blocks give zero losses. The first completed block has stabilizer J and all proper stabilizers lie in J, recovering B=J uniquely.

This uniqueness prevents double counting between maximal subgroups. For a fixed actual J, the factorial orders its distinct labeled right cosets and each A(J) counts an independent internal order. Changing representatives only changes the identifying bijection; it introduces no factor. The singleton is a base case, not an empty recurrence. No escape count is inferred.

## Adversarial and source checks

The rejected n=4,t≥5 residue1 fit is independently rejected at band16 by exactly 8845>8839. This establishes failure of that particular fitted invariant only. The longer transient is necessary for the submitted replacement, not claimed necessary for every possible certificate.

The new checker rejects malformed coefficient/state types, Boolean coefficients, duplicate states, missing reachable states, missing bands, out-of-range masks, past high/category bits, lowered t/joint rays with preserved base value, lowered intercepts and incorrect cone domains. Endpoint controls retain the exact-period counterexample. The final negative-result record enumerates each test.

All 16 source snapshots were compared byte-for-byte with their workspace originals and their pinned hashes. The accepted p7 archive/proof/review, prior p3/p5 scope, mixed construction/compatibility, accepted abelian/two-Sylow results and classical comparisons retain distinct provenance. They are premises or inert historical documentation, not newly executed proofs. Final archive integrity and archive-only cold replay have passed, with semantic equality to all independently computed records.

## Scope and positioning

The new result is the named p=11 slice under existing NEW-16. It does not retire the broad uniform-mixed-primes gate. Both-prime-variable bounds for 13≤p<r, full-escape classification/count even for accepted slices, broader nonabelian three-prime groups, larger exponents and all finite nilpotent groups remain open. EFK remaining-body/equality source gaps and unresolved historical priority remain unchanged.

Classical signature/transversal constructions, coset branching and factorial counts retain attribution. No external literature search, worldwide novelty clearance, algorithmically unrelated proof method, cryptographic decoder, speed claim, rank/band change or discovery-count promotion is established. The review performs no external write.

## Final evidence and portable replay

The accepted author archive is Prefix_D8_C11_Prime_Uniform_Affine_CANDIDATE_2026-10-12.zip, 27,722,215 bytes, SHA-256 6929b9ae8327a78c71314089218042231432a6df5b40e1d9b0564324e16679cc. Its manuscript SHA-256 is 4a99c1ae7bf188859d2171a18f7fb220436ae589957bc7b0f08d7845012c355b. All 116 manifest entries match the sealed archive and working candidate. All 40 certificate-file hashes are identical to the data actually checked independently.

The complete reviewer run verifies 919,370 affine rows and 4,596,850 scalar inequalities. Every terminal slope is 16,720 and every t=9 value is exactly 190(792+rho)-87. The independent finite checker verifies all 133 primes from 13 through 787; a separately implemented Python sieve confirms exact prime-range coverage. All 17 negative controls pass. Literal finite graphs give 36,728,370 pair comparisons and 4,115,652 Bellman transitions, alongside direct group and D8 count controls.

The portable cold replay extracts only safe paths from the exact sealed candidate ZIP to a fresh temporary directory. It verifies every manifest entry and checksum, all inert source pins, and runs only the newly authored reviewer programs. It recompiles the reviewer C++ source and repeats all 40 cones, 133 finite primes, literal graphs, group witnesses, D8 count and negative tests. All semantic outputs agree with the original independent records; measured wall times are deliberately excluded from equality. Original workspace sources are unnecessary for this replay. Their byte-for-byte preservation was checked separately before and after replay.

The mathematical objective is distinct from verification cost. Integer arithmetic is exact. Python proof arithmetic is arbitrary precision; the bounded C++ mask widths are proved sufficient, and its signed 64-bit reward arithmetic is safely bounded on r<792. The C++ band_peak_states diagnostic measures only open-band exits; it is not an RSS or whole-execution peak-memory bound. No execution complexity, asymptotic advantage or physical speed claim is added.

The reviewer packet carries the candidate ZIP as inert input, source code, complete deterministic results, accepted statement, this report and cold replay. Its manifest and outer ZIP seal bind the final review. No author or predecessor mathematical program was executed by the reviewer, and no external service was changed.

Derivative note: private tracking-version and cell-integration instructions are omitted. The complete uniform proof, exact maxima, unrestricted equality/count theorem, rejected invariant, independent evidence and remaining limits are unchanged. Original report SHA-256: `bb991618b13984ba778c261243bfbbc58c5cb2c5238a742212f362bfdffd230f`.
