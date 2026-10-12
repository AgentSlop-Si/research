# ALG-079 named compiler: independent source-bound review

Date: 2026-10-12 UTC.

## Finding

The finite-domain termination, returned-factor soundness, collision-free-factor completeness, and exact arithmetic formulas below hold for the pinned `factor_sparse_hypercube` and the pinned caller's success-only accounting correction. This result is about that named compiler, its source-event cost contract, and its immediate accounting boundary. It does not qualify the detector, all callers, the entire ALG-079 lifecycle, or a production RAM/bit/time model.

Historical and candidate Python programs were only read as inert text. The reviewer executed only newly authored checking programs. This is source-level proof with independent finite controls, not a claim to have dynamically executed every historical operation in this review.

## Exact sources

- `reciprocal_union.py`, function lines 257–292: SHA-256 `246db30e69b2988aa24134b41b21496727c7e1e67c2af9abbb3d133adc7a037a`.
- `migrated_caller.py`: SHA-256 `843e5c12db800b530d200ab7d545ada01a29d3fae93881a24c1deaea342dfd00`. Compiler dispatch is lines 52–58 and the successful-return product correction is line 57.
- Prior review: the accepted caller-migration review, retained as inert evidence, already accepted the named migration while leaving complete compiler accounting/totality open. Its historical execution results are background evidence, not newly executed here. Its SHA-256 is `72ab5448080d6f69bbaad9a4400021d7b018cc154a6f20951d2eb9b8c1cbb55b`.

The fresh checker hashes the source bytes and AST-inspects the function and accounting repair. It neither imports the original modules nor compiles/evaluates their ASTs.

## Domain and outputs

Use an ordinary, stable Python dictionary `A` with `m=2^t` distinct canonical keys in `[0,n)`, canonical nonzero integer coefficients in `[1,p)`, and plain integer inputs. Here `1 <= t <= 4`, `n` is dyadic with `2 <= n <= 4096`, `p` is an admitted prime with `2 <= p <= 2^31-1`, and `n | p-1`. The supplied accounting sink is the actual truthy historical `Work` record; no adversarial properties, integer subclasses, concurrent mutation, or reentrant callbacks are included. The compiler itself does not consume the Fourier root.

The normal caller domain has `1 <= delay < n` and `1 <= alpha < p`. Zero delay is an explicit negative control: the function deliberately rejects every candidate even if its polynomial matches. One auxiliary alpha-zero case tests that a literal successful terminal product is still executed; it is not evidence that the upstream detector produces alpha zero. The `n=4096` and maximal-prime cases are separate, admitted pairs; `n=4096,p=2^31-1` would not be an admitted root domain.

The requested compiler envelope includes t=4. The named cold entry admits detector parameter s<=8, so its recovered support cannot reach 16 taps; t=4 is an explicitly bounded compiler over-domain, not an observed 16-tap detector path.

## Termination proof

Let `P=(m-1)_t` be the ordered selection count and `Cmax=m*P`. Each origin has exactly `m-1` other support entries and at most P edge tuples. The source does no data-dependent retries and has no recursive calls. Every inverse is defined because the origin coefficient is nonzero in a prime field.

For candidate c define K(c,0)={origin}. After stage i the dictionary keys are exactly

`K(c,i) = K(c,i-1) union (K(c,i-1)+d_i mod n)`.

The source copies all keys and does not delete zero-valued entries during expansion. Thus `q(c,i)=|K(c,i)| <= 2^i`; collisions and coefficient cancellations do not invalidate this bound. Every candidate performs t stages and visits at most `2^t-1=m-1` expansion entries. The final zero filter visits at most m keys. All remaining operations are finite built-in operations on these bounded plain inputs. This is ordinary mathematical/program termination assuming the declared abstract operations complete and sufficient resources exist, not immunity from process interruption or allocation failure.

For t=1,2,3,4 respectively, Cmax is 2,24,1680,524160. Expansion-entry ceilings are 2,72,11760,7862400. The multiplication ceiling `Cmax*(t+m-1)+1` is 5,121,16801,9959041. These are safe ceilings; they are not asserted to be jointly attainable by one successful execution.

## Correctness proof

At every stage the current dictionary represents `c*z^b*product_{j<=i}(1-a_j*z^d_j)` in `F_p[z]/(z^n-1)`, including stored zero coefficients. This follows by distributing multiplication by each next binomial; the copy implements the identity term and each update subtracts its shifted product. Removing zero coefficients after the final stage preserves this polynomial. Canonical coefficients and keys make dictionary equality equivalent to equality with A.

If the compiler returns, therefore `A=c*z^b*Q`. With `u=-b mod n`, `v=u+delay mod n`, and returned defects `D=c^-1*z^u*(1-alpha*z^delay)`, multiplication by `c*z^b` gives exactly `B=1-alpha*z^delay`. The source requires u!=v before constructing the result. Consequently any separately established cyclic certificate `A(S)r=B(S)e0` implies `Q(S)r=D(S)e0`. No new detector-certificate claim is needed or made.

A successful expansion has m nonzero output keys but only m subset contributions. Hence all subset exponents are distinct: successful candidates necessarily have collision-free support. Conversely, given a collision-free representation `A=c*z^b*product(1-a_i*z^d_i)` with t factors and nonzero multipliers, the origin and t incident exponents are present and distinct. Their ordered tuple occurs in the finite enumeration. The source recovers exactly each a_i from its incident coefficient, expands back to A, and returns by then when delay is nonzero. Thus `None` on the admitted nonzero-delay domain means no representation of this specified collision-free form exists. This says nothing about factorizations with a different number of factors, uniqueness, or arbitrary polynomial factorization.

## Source-exact arithmetic ledger

Across every attempted candidate, including failures, define:

- O: number of origins entered
- C: number of candidate tuples attempted
- E: sum of all pre-expansion dictionary sizes q(c,i-1)
- F: sum of final dictionary sizes before removing zero coefficients
- G: sum of final nonzero dictionary sizes
- B: number of expanded candidates equal to A, before the delay check
- S: one if the function returns a factorization, zero otherwise

Then the exact executed coefficient-operation counts are:

| Operation | Count |
|---|---:|
| Field inversions | C |
| Field products | t*C + E + S |
| Field subtractions | E |
| Coefficient unary negations | t*C + S |
| Coefficient modulo-expression evaluations | t*C + E + S |
| Exponent subtractions | t*C |
| Exponent additions | E + B |
| Exponent unary negations | B |
| Exponent modulo-expression evaluations | t*C + E + 2*B |

Products occur at exactly source lines 275, 282, 290. The last site occurs only after both equality and nonzero-delay acceptance; it is absent on a no-factor or zero-delay result. There is no normalization/inverse cache: C inversions, even for repeated origins, are charged.

The modulo-expression tally is a separate representation view, not an additional field multiplication/subtraction. Likewise a field inverse is one contracted field primitive, not a claim that Python's internal extended-gcd costs one machine step. Field negations were omitted from the historical Work vocabulary and must remain visible in a full field-primitive profile.

Historical Work records exactly `(multiplies, additions, inversions)=(t*C+E,E,C)`. The migrated caller adds S, giving `(t*C+E+S,E,C)`. This is a projection of the compiler's arithmetic, not its full operation total. The compiler makes zero backend `Field` calls, so its backend-Field delta is empty. Its arithmetic is real even though backend Field observes none.

Selected independently recomputed non-arithmetic payloads include `m*O` rest comparisons, `(m-1)*O` retained rest entries, `t*C` permutation tuple coordinates, `(t+1)*C` A dictionary reads, E copied dictionary entries, E dictionary gets and writes, F filter predicates, G surviving filter entries, C equality operations, B delay comparisons, `2*C+E` Work truth tests and `2*C+2*E` historical Work integer updates. The caller adds S more telemetry updates. Dictionary equality, hashing/probes, allocation, iterator internals, import internals, and inversion implementation are contracted in the named source-event model; that contract must be read before interpreting its total.

Do not sum compiler arithmetic and its Work projection. Do not add whole-caller Work to whole-caller Field: preview, residual, and solve overlap. The compiler-only delta can be isolated, but complete non-overlapping accounting of the entire detector/caller is still a separate obligation.

## Independent controls

The fresh checker uses a separately written all-subsets polynomial oracle, not a factor-by-factor expansion oracle. It checks every candidate expansion for small/random cases, all returned identities, and independent formulas for executed events. Controls include:

- First-candidate success for each t=1..4, with the terminal product charged exactly once
- Zero-delay rejection and no-factor exhaustion
- Explicit collision plus cancellation, and a seeded case where retained zero-valued entries are visited in a later expansion stage
- 512 exhaustive coefficient/delay cases at n=4,p=5,t=2, including 10,176 candidate comparisons to the subset oracle
- Seeded fresh arbitrary-support cases for t=1,2,3
- Separate admitted upper-n and upper-prime boundaries
- Full t=4 zero-delay traversal of all 524160 candidates, including 384 polynomial matches subsequently rejected by the delay condition

The full t=4 control has E=7653984 and exactly 9750624 coefficient products, 7653984 subtractions and 524160 inversions; S=0. This distinguishes all failed search work from the terminal success-only product. It also observes 48 final zero keys and 479868 collision stages. Finite controls support the proof; they are not exhaustive enumeration of the entire admitted input domain.

The fresh checker's small-field exhaustive fixtures and full t=4 control are generated internally and deterministically. Candidate sealed-packet recomputation and the cold-rerun seal are recorded separately. Only the reviewer-owned checker is run in those steps; candidate source remains inert.

## Preserved scientific limits

Acceptance applies only to this named compiler and the pinned immediate caller
correction, under the declared finite source-event/field model. The prior
constructor-witness correction and accepted migration results are retained.
Full detector totality/cost, other callers/importers, whole-lifecycle closure
and production RAM/bit/time remain open. This result does not establish a new
algorithm identity, novelty claim or speedup theorem.

## Exact sealed-candidate acceptance and cold result

Independent ACCEPT applies to candidate `ALG079_Source_Bound_Compiler_CSM1_CANDIDATE_2026-10-12.zip`, 52099 bytes, SHA-256 `8e77c58d88b674926134168f271ccd0b7e5ec47b0fb2664248f6c800daa3f225`. Its manifest SHA-256 is `b7add3d79076e722966b1d71f08bd54be79b742fbeaab56d51412a6c67bc128f`; all 22 manifest-bound members and the manifest itself are verified, with the exact 23-file set preserved.

The final candidate's 124-dimensional CSM1 event vocabulary was reviewed against the pinned source. Explicit scalar-load/dispatch zero-cost conventions and contracted built-in internals are essential to this acceptance. It is a complete vector under that named source abstraction, not an assertion of complete CPython machine-operation counts. The review requested and verified corrections to missing name/iterator bindings, comprehension/Work conditional-selection events and the caller correction's identity comparison before sealing.

All 11 final candidate control records were independently regenerated by the reviewer-owned checker. Returned objects, O/C/E/F/G/B/S aggregates, stage histograms, collision/zero statistics, Work projections and the empty backend Field delta match. Twenty-two selected event dimensions, including the complete field/exponent arithmetic vector, are also explicitly compared in code; the remainder of the source-event formulas are established by the source review and their dependence on those independently verified aggregates. The candidate's own additional tests and mutation log remain author evidence and were not executed by this reviewer.

A separate cold extraction ran only the two reviewer-owned programs. The independent 512-case/35-control result, candidate-control recomputation and candidate-seal validation were byte-identical to the warm results. The independently generated t=2 representation set contains 96 coefficient vectors, matching every exhaustive nonzero-delay success and every failure. Checker bytes, both original source pins and every extracted candidate member were unchanged. The exact independent-results SHA-256 is
`b7309bab8ec1e730650cf3806d4cf89c9d5ba250806fd6cf9efe774d1626329e`;
the candidate-control recomputation SHA-256 is
`589f74a6de0693727466a1f559d59326f776a74e283c6a9cb66e308be54035dc`;
and the candidate-seal validation SHA-256 is
`cf7703ef90e19dd1421ae38d72168c234a200f96fd10a6ae05d1367af3acd670`.

This final acceptance retires only the specifically named compiler obligation under CSM1. The broader detector and lifecycle obligations listed above remain open.

## CSM1 contract appendix from the accepted candidate proof

The following source-event contract is retained from the sealed candidate's
proof document so that the named abstraction and its zero-cost conventions
are explicit. It is supplementary candidate proof text reviewed in the
independent acceptance above, rather than a claim of further independent
execution. Its notation H, Q and Z corresponds respectively to B, F and G in
the independent ledger above; q_i is the stored dictionary size after stage i.
The complete candidate proof has SHA-256 `380334e3707931d4ddd4eb7101066145546f0094cf7b22af9f7f77faf12ab458`.


The sealed candidate formula specification defines the named event vector. Events are counts, not seconds. Scalar literal/name loads, method resolution, internal short-circuit dispatch within a named chained-comparison/boolean operation, function-argument passing and reference release are zero-cost in this particular abstract model; explicit bindings, loops, operators, calls and container payloads below are charged. Conditional branch selections are explicit if-test events, including comprehension filters and Work/caller correction tests. Integer-to-boolean predicate conversion for coefficient and Work objects is additionally a truth-test event; comparison predicates are their own comparison events. Source list/dict/tuple allocation is one creation event, and element copies/writes are separate payload events. Dictionary lookup/update/equality, permutation initialization/yield, `pow` inversion, `len`, `bit_length`, and import resolution are named abstract operations. Their implementation-specific probing, hashing, internal allocations, interpreter dispatch, inversion bits and module loader internals are not silently converted into unit RAM costs.

Coverage by pinned line number:

- 264–267: one import, t binding, guard comparisons/boolean operators/len/shift/if; support-list creation and all m key copies. This is the compiler's input ingestion, not an assumed-free dense input scan.
- 268–270: outer iterator and every attempted next; O rest-list creations, mO comparisons and (m−1)O selected writes; O permutation initializations with (m−1)O pool input copies; C tuple yields with tC tuple coordinates. Successful early termination has no artificial terminal next; failed outer/inner iterator exhaustion is included.
- 271–276: C coefficient reads/inversions; all per-candidate bindings; tC incident exponent arithmetic, coefficient reads/negates/products/mods; ds/aa list creations, iterator visits, and writes; Work truth tests and counter record changes. The fixed -1 exponent literal is separately named, not confused with a field negation.
- 277–284: initial dictionary creation/write; all C zip creations and tuple coordinates; tC dictionary copies with E copied key/value pairs; tC items views, E+tC next attempts; E gets/writes and all exponent add/mod, field mul/sub/mod, bindings and Work increments. Copies include zeros.
- 285–288: C filtering dictionary creations/items views, Q+C next attempts, Q truth tests, Z writes; C dictionary comparisons and C−H rejection continues. The H equality matches each compute both defect addresses and their equality, including H−S zero-delay continues.
- 289–292: only S successes allocate two output tuples (2t copied slots), a two-entry defects dictionary and a four-entry result dictionary, perform terminal negation/product/mod and return that output. Failed compilation returns None once. No n-vector is produced.
- Caller 52–58 and snapshot 7–8: dispatch length/membership/if, compiler call/argument length/bit_length/subtraction, factors binding, successful-only correction if, and two exact ordinary Work snapshots. Each snapshot visits all ten attributes, type-tests ten values, copies the nine integer entries, and returns/binds one dictionary. Counter-update costs already include +S and are not duplicated here.

The finite vector supplies all above categories without relying on an unspecified “O(1) setup.” The verification checker's own domain validation, subset oracle, JSON serialization, SHA-256 and AST parsing are verification overhead, not costs of the historical compiler. Their ingested source-byte counts are reported separately, and their output file hashes are sealed. Importing/executing the historical source is neither required nor performed. This distinction avoids charging a source archive's hashing as part of the user's runtime compiler, or claiming it happened for free.

All variables in the vector are finite: 1≤O≤m, C≤C_max, E≤C(m−1), Q≤Cm, 0≤Z≤Q, S≤H≤C. If S=0, O=m and C=C_max. If S=1, the one successful candidate's q_i=2^i and it contributes exactly m−1 expansion updates and m final retained entries. The source vector is therefore bounded uniformly in admitted n and p at fixed t, with abstract inversion/lookup/permutation primitives. Broader detector, module-ingestion/cold production, actual hash traffic, bit complexity, and elapsed time remain open.

## Publication provenance and derivative disclosure

This is a privacy-filtered repository report derivative, not a byte-for-byte
copy of the sealed review. Mathematical proofs, numerical and computational
limits, and source-accounting qualifications are retained. Administrative
integration instructions and environment-specific replay paths are omitted.
No program, archive or full third-party paper is included in this publication.

- Accepted reviewer archive: `ALG079_Source_Bound_Compiler_CSM1_Independent_ACCEPT_2026-10-12.zip`, 87,713 bytes.
- Accepted reviewer archive SHA-256: `4ba683924d80f3458f61b8a3b475aca47576c3a4c69831f8825b36c161b45160`.
- Unmodified independent source-report SHA-256: `6e28f713774cf05bc780b469de8ae2328ba9f3c4fef4a89cac4feea15db0c4cd`.
