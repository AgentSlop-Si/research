Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical proof, source attribution, limitations and review method are retained. Original source-report SHA-256: 82f1d871bd582a5e51b6728686c5a1e9caa7c33f3bfd66bae54d173408b46f1e.

Review date: 12 October 2026 UTC.

# Independent acceptance of the D8 C7 Cr prefix theorem

12 October 2026 UTC. Independent project mathematical and computational review.

## Decision

ACCEPT the stated p=7 parameter-uniform theorem for every prime r>7. No mathematical repair is required. The accepted conclusions are the exact unrestricted maximum 188r−56, the exact full-escape maximum 174r−56, the deficit 14r, the complete unrestricted recursive maximal-subgroup right-coset optimizer classification, its unique top B, and its exact labeled-count recurrence. This is a scoped additive result. The broader uniform-mixed-primes problem remains open.

This acceptance is based on a fresh implementation and a symbolic proof audit, rather than the author's PASS records. It is an independent project review, not external peer review or proof-assistant certification. The reviewer read the submitted active Python sources before execution; none of those sources, source snapshots, or nested predecessor programs was executed or imported. Only fresh reviewer programs were run. 

The reviewed immutable archive is Prefix_D8_C7_Prime_Uniform_Affine_CANDIDATE_2026-10-12.zip, 7,109,552 bytes, SHA-256 541841f2a296763462a57edcd1bc12327ba79cf4da5a548336ae0b63da36d013. Its THEOREM.md has SHA-256 0970354a3b7b01abf18453a6bd1690af89ba232199d8ecdfdedd2559327575c3. Its 54,387,189-byte affine certificate has SHA-256 ad3e2fa8e06970bba9114cc996469ee7e9031a768ccaf2b19c10bef6e9e248f7.

## Accepted statement and conventions

Let G=D8×C7×Cr, with D8 of order eight and r>7 prime. For a permutation of all actual labeled group elements, Tj is its nonempty j-element prefix, Sj is the left stabilizer of Tj, and

    Z = sum(j=1,...,56r)(|Sj|−1),
    B = <Sj : 1<=j<56r>.

The empty prefix is absent. The full prefix contributes 56r−1 exactly once and is excluded from B. Full escape means B=G. There is no quotient by translations, automorphisms, conjugacy, signatures, or representative choices.

The accepted values are

    max Z = 188r−56,
    max_(B=G) Z = 174r−56.

Every unrestricted optimizer consists recursively of consecutive right cosets of a maximal subgroup, with an independently optimal local order in each block. Its top subgroup is unique and equals B. If A(K) counts labeled unrestricted optimizing permutations, then A(1)=1 and, for nontrivial relevant K,

    A(K)=sum_(J actual maximal subgroup of K) [K:J]! A(J)^[K:J].

In particular,

    A(G)=2 A(C4×C7×Cr)^2 + 4 A(C2²×C7×Cr)^2
         +5040 A(D8×Cr)^7 + r! A(D8×C7)^r.

This does not classify or count full-escape optimizers.

## Symbolic reduction audit

Every subgroup splits into a D8 subgroup and a subgroup of the cyclic odd factor by coprime powering. Every maximal subgroup is normal of prime index 2, 7, or r. The three maximal-subgroup orders 28r, 8r, and 56 are therefore exactly the excluded orders used in the escape graph.

The maximal-subgroup barrier is valid on both sides of the invariant prefix. Before a nonempty proper J-invariant prefix, any earlier nonempty quotient support lies inside a proper subset of G/J. An outside-J element acts as a full prime cycle, so cannot preserve that support. After this prefix, a later prefix contains a full J-coset; invariance under an outside element would force the full quotient orbit of complete cosets and hence all of G. Thus every proper stabilizer lies in J. A full-escape order cannot have such a prefix. The converse is not used or claimed.

The compatibility lemma does not require D8 subgroups to be nested or permutable. For actual stabilizers L×Ce and R×Cf, their 2-part orders are comparable. If |L|>=|R|, the Cf-saturation of the earlier prefix is contained in the later prefix and invariant under a subgroup of order M=lcm(|L×Ce|,|R×Cf|). If |L|<|R|, the intersection of all Ce-translates of the later prefix gives the required invariant intermediate set. Centrality of the odd components gives the claimed invariances. Freeness of left multiplication makes the intermediate size divisible by M.

The lower endpoint can be attained only when M is the earlier stabilizer order; the upper endpoint only when M is the later stabilizer order. Otherwise equality of the intermediate set with a prefix would put a strictly larger subgroup into that prefix's actual stabilizer. This validates both endpoint exclusions. Equal-position graph vertices also conflict. Consequently every escaping permutation induces an independent set with exactly its proper-prefix score. Graph realizability in the reverse direction is unnecessary.

The resulting graph upper bound is 118r−55. Adding the single full-prefix term gives 174r−56. The low types are exactly 2,4,7,8,14,28; the high normalized types are exactly 1,2,4,7,14. The 105 high nodes and 111 categories are correctly derived. Low-low conflicts are periodic modulo 56 and vanish at distances greater than 56, but distance 56 must remain: (56,8) and (112,28) conflict. For low-high edges, common-multiple rank is integral and constant within each open rank band; the high endpoint is allowed precisely when the reduced common multiple equals its high type, whereas the low endpoint is never allowed. These facts justify the compression uniformly, rather than only at sampled primes.

## Fresh Bellman and cone reconstruction

The reviewer wrote independent_check.py from the graph definitions. It does not import the submitted frontier or verifier. Its integer conflict routine explicitly searches admissible common-multiple positions. Its mixed-edge routine independently scans common-multiple ranks using doubled rank coordinates, rather than reusing the submitted endpoint-bound formulas. The finite future masks are rebuilt from these routines.

The reviewer uses coordinatewise max-plus vectors to propagate the base, t-ray, joint-ray, and cone-vertex quantities. Different vector coordinates may take their maxima on different paths, which is conservative and exactly appropriate for these upper checks. Skipping or selecting a low vertex advances the low stream; selecting a high vertex blocks all relevant low categories and later highs. Processed bits are removed. Histories with identical masks have identical available continuations. This proves exactness of the single-coordinate Bellman recurrence and soundness of the coordinatewise certificate propagation.

All 24 reduced residues modulo 56, all 56 bands per residue, all 325,326 certificate rows, and all 1,626,630 scalar inequalities passed in the fresh implementation. At every band the base and cycle destination sets are contained in the certificate state set. Row types, distinctness, mask ranges, erased past bits, and complete residue/band coverage are checked. Every terminal t coefficient is exactly 6,608, and every terminal value at t=5 is exactly 118(280+rho)−55.

The induction domain t>=5, 4<=n<=t is valid. For a one-cycle transition n<t, the domain is precisely t=5+v+q, n=4+q, v,q>=0. The two rays are A and A+C, and the vertex comparison is 5A+4C+b+w against 5A+5C+b. The finite checker verifies these three quantities for every route through the cycle. The four-cycle base is checked using a t slope and a t=5 value; the band exit n=t becomes (A+C)t+b. The fixed tail and high-boundary affine rewards preserve the argument. The universal conclusion is therefore established by finite integer inequalities, not extrapolation from discovery samples.

The final affine certificate covers all abstract graph parameters r=56t+rho with t>=5 and gcd(r,56)=1. The reviewer independently solved all 117 reduced integers 7<r<280. These comprise 55 primes and 62 composite abstract-graph controls. Every finite maximum is exactly 118r−55. Together these ranges cover every prime r>7 without a gap. Composite runs are not claimed as group theorems for C7×Cr with the extra subgroup divisors suppressed.

Fresh result records match the author's residue and finite-base numerical records exactly. The numerical agreement is corroboration; the reviewer computed the results independently first. Timings are host observations, not resource bounds or speed claims.

## Literal graph and group controls

independent_controls.py separately constructs every absolute-position graph vertex, checks every pair against the rebuilt compressed masks, and solves the whole graph with a single absolute future-mask recurrence. Its processing order at equal positions is independent of the compressed implementation's high-first convention.

- r=11: 792 vertices, graph maximum 1,243.
- r=13: 918 vertices, graph maximum 1,479.
- r=59: 3,816 vertices, graph maximum 6,907.

Across these three graphs, 8,013,159 pair comparisons and 1,780,806 Bellman transitions passed. These are finite corroborations of the uniform reduction, not substitutes for it.

The two signatures are reconstructed in tuple coordinates (i,b,c,t), with multiplication (i,b)(j,d)=(i+(-1)^b j,b+d) in D8. Products use the stated left-to-right convention and last coordinate fastest. The unrestricted D8 order is 0,4,2,6,1,5,7,3, and the escaping D8 order is 0,1,2,3,4,5,6,7. Their proper stabilizers and scores are correct. For r=11, direct multiplication checks every one of the 616 nonempty prefixes of each witness, and every prefix size agrees with an independently derived fiber profile:

- Unrestricted witness: Z=2,012; |B|=308.
- Full-escape witness: Z=1,858; |B|=616.

The symbolic fiber identity Z_(H×K)=|H|Z_K+|K|Z_H is correct: at a strict partial fiber the unique partial outer class forces the outer stabilizer component to be trivial; at a full-fiber checkpoint the stabilizer is the outer prefix stabilizer times K. The inner odd order has score 13r−7, giving the stated two values for every prime r>7. Its first full fiber and D8 checkpoints establish the two claimed B subgroups. Neither a different decoder nor a factor reversal is used.

A further fresh exhaustive 256-subset D8 dynamic program gives maximum 12 and exactly 2,432 labeled optimizers. Independently enumerating all ten actual subgroups finds one C4 and two C2² maximal subgroups, and the recurrence gives 2·8²+4·24²=2,432. This verifies the multiplicities and conventions in a complete small case.

## Unrestricted equality and count audit

The strict escape deficit excludes B=G from every unrestricted optimizer. Choose a maximal J containing a proper B. At each insertion the global proper-prefix stabilizer is contained in the active local prefix stabilizer inside its right J-coset. Each nonempty local prefix is counted once. The final insertion replaces the local full stabilizer J by G, producing exactly the correction |G|−|J|. Thus the manuscript's accounting identity and every nonnegative loss term are correct.

Every proper subgroup needed here is covered by the pinned accepted baselines: a proper D8 subgroup is abelian, and retaining all of D8 in a proper subgroup leaves at most one of the two odd primes. The accepted finite-abelian and arbitrary two-Sylow results explicitly include the maximum, recursive equality cases, unique top, and labeled recurrence. They are used as prior theorems, not represented as newly proved here. The value is |G|[3/2+6/7+(r−1)/r]=188r−56.

At equality, every local order is optimal and every local/global stabilizer deficit vanishes. At the first completed coset the global stabilizer equals J, so all other cosets must still be empty. This forces the first consecutive block; repeating at each proper completion forces all subsequent blocks. The last coset fills the remainder. Conversely, consecutive optimal coset blocks give zero losses. At a partial block the unique partial quotient class forces its global stabilizer inside J, and at a proper full-block checkpoint a nonempty proper subset of the prime quotient has trivial translation stabilizer.

The first completed block has stabilizer J and all proper stabilizers lie inside J, so B=J. This recovers the top uniquely, preventing double counting between maximal subgroups. For a fixed actual J, the factorial counts orders of its distinct labeled right cosets; A(J) independently counts internal orders. Changing representatives is a bijection on the same internal labeled permutations and adds no factor. The singleton base is explicit. Both classification and the count recurrence are accepted without an escape-count conclusion.

## Failed fit and adversarial controls

The initially fitted t>=3,n>=2 certificate remains rejected. Its 54,387,188 bytes have SHA-256 816d83a3aa2158a6fe6c7ab4b76c897e8aad431c23c6f07f71165848b6fca239. The exact bytes are included as inert data in this review packet. Running the fresh checker on that domain independently reproduces the failed residue 1, band 36 joint-ray inequality: 3,464>3,463, while the other displayed coordinates are 3,408 and 10,388 on both sides. The longer transient is essential for the submitted certificate; this does not establish a universal impossibility of every shorter-domain certificate.

Eleven further mutations are rejected: lowered t slope while preserving the base value; lowered cycle slope while preserving the base value; missing residue; missing band; duplicate state; noninteger coefficient; Boolean coefficient; missing reachable state; lowered affine intercept; out-of-range high mask; and out-of-range low mask. Endpoint controls retain the exact-period counterexample. The documented temporary author-control phase-modulo typo is disclosed as development history, not used as a premise. No rejected fit is promoted by passing discovery samples.

## Attribution and integration limits

All 16 inert source pins match their stated sizes and hashes. Each was also compared byte-for-byte with the original workspace source. The accepted p=3 and p=5 uniform results, finite p5r7 evidence, mixed construction and compatibility sources, accepted abelian/two-Sylow scopes, and earlier classical comparisons retain their separate provenance. The candidate correctly describes its own code as an adaptation of the p=5 implementation and p=3 architecture; self-containment is not called implementation independence. The present checker is fresh, while following the same mathematical certificate specification, and is not claimed to use an algorithmically unrelated proof technique.

No new literature search or historical-priority clearance was performed. Classical signature/transversal constructions, coset branching, and elementary factorial counting remain attributed. The pinned comparison's EFK remaining-body/equality gap remains open. Neither this review nor the new slice establishes worldwide novelty, a new signature convention, a new cryptographic decoder, or an asymptotic/physical-resource advantage.

The unresolved scope is explicit: both-prime-variable upper bounds for 11<=p<r after the accepted p=3,5,7 slices; full-escape optimizer classification/count for all accepted slices; arbitrary nonabelian three-prime groups and larger exponents; all finite nilpotent groups; and historical priority. The broader mathematical problem remains open.

## Reproducibility and seal

The review packet includes the original candidate ZIP, the rejected shorter-fit data, fresh programs, result JSON, the accepted statement, this review, and the portable replay driver. replay.py validates the original archive hash, extracts only safe local paths into a new temporary directory, and runs only the reviewer programs. It compares all semantic outputs with the accepted records while excluding wall times and whether external original sources are locally present. Those originals are not needed for portable mathematical replay; their initial unchanged verification is separately retained.

All mathematical arithmetic is exact Python integer arithmetic. The manifest charges certificate data and source preservation separately from the mathematical objective. The review archive's external SHA-256 seal binds its final contents. The submitted candidate and all 16 antecedents are unchanged. No broader conclusion follows from this acceptance.

## Final cold replay result

The complete portable reviewer replay passed from a fresh temporary directory. It reproduced the cone certificate, all 117 finite bases, literal graphs and group witnesses, D8 count control, and all 12 negative tests with semantic equality to the recorded results. The run required no external source files and executed no candidate code. COLD_REPLAY_PASS.json records the commands and measured times. The final source-preservation check again found the candidate ZIP and all 16 antecedents unchanged.
