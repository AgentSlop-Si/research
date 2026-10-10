# Complete static review of the two generated SMT-LIB sources

## Outcome

Both assigned exact hashes pass complete static semantic/template verification. All 1,148,303 source bytes and all 1,129 lines are accounted for by independently reconstructed, reviewed text templates, with zero unmatched bytes or lines. The scope is stronger than sampling, but it is not a claim that a person or model literally read every repeated character from first to last. The complete generated repetition was checked by exact byte comparison, plus whole-file lexical checks. No supplied program, generator, SMT source, compiler, AST parser, or solver was executed or imported.

The 16-gate positive-control formula is satisfiable by the independently replayed pinned circuit. Its complete archived model, containing 208 definitions, agrees with fresh exact integer arithmetic. This is an independent satisfaction check based on the verified formula template and explicit witness, not a fresh solver run. The 15-gate source has an archived `unknown` result with reason `timeout`; no shorter witness, lower bound, impossibility result, or optimality conclusion follows.

## Exact source identities and provenance

- `positive_control.smt2`: SHA-256 `5d527ae679dbe3392d31ff5694975af3549b3bd483a395c05942a72efaf1ad2d`; 601,910 bytes; 621 lines; archive member index 21.
- `slp_15.smt2`: SHA-256 `8ac21b8608b38cd909ba6cb718989d20fb892e84228dd83e280570cdb87555c4`; 546,393 bytes; 508 lines; archive member index 24.
- Direct archive: `cancellation_transform_reproducibility.zip`, SHA-256 `cd152b676bae0a9f955b13f20e25d131bd90a57f55fa04cc77098dfbf68acdad`, 83,831 bytes. Current archive bytes were rehashed; both source member bytes were re-read directly by member index and matched against the queue content and archive graph.
- Archived Library identity: `[private-id]`; observed backing ID `[private-id]`; no observed version is available in the inherited root record.
- The inherited graph additionally places this archive inside historical bundle hash `1c311596d802a5de6cce2de4a89c4d13500419a266b63e170b97b626f37e6367`. That outer bundle is recorded provenance, not freshly rehashed here.

PROVENANCE.json includes exact hashes, sizes, original member paths/indexes, and snapshot paths for the sources, generator, control wrapper, certificate, logs, summaries, and contextual documents. The queue's `origin_unresolved` classification is retained. Matching a generator and archive does not establish original-author versus reviewer authorship. Original input files and archive were rehashed after the checks. The central registry was not changed.

## Method and comprehensive coverage

The fresh checker `checks/verify_templates_and_arithmetic.py` was written for this review using only standard-library byte readers, JSON data reading, ZIP member reading, regular expressions, hashes, string construction, and exact integers. The supplied generator `smt_search.py` (55 lines) and supplied control wrapper `verify_smt_control.py` (16 lines) were read as inert text; neither was imported, called, copied as an executable dependency, compiled, or AST-parsed. The expected source was constructed from the independently stated gate/coordinate specification below, using a generic textual S-expression formatter and a left-to-right selector-arm builder. The actual source was never parsed into an expression tree or evaluated.

Every reconstructed document was compared directly with the corresponding original bytes, including spaces, command order, all repeated branches, newline placement, and final LF. All generated lookup arms, index literals, coordinate literals, signs, operator branches, range tests, target options, pin equalities, and trailing commands participate in that comparison. This excludes additional unexamined assertions, altered repeated instances, and hidden or appended commands. Whole-file lexical passes additionally verified balanced parentheses, unique declarations, declared-before-use references, and total byte coverage. Each line has its own zero-based byte interval, length, hash, category, and gate/coordinate or target-row attribution in `per_source/<hash>.json`.

Positive control: 16 gates numbered 8 through 23; 208 declarations, 408 assertions, three header commands, and two query commands. This includes 32 predecessor bounds, 16 operation bounds, 16 symmetry bounds, 128 coefficient bounds, 128 gate equations, eight target assertions, and 80 pin equalities. Every gate-equation selector is checked in every coordinate and every repeated occurrence. The source contains 263,637 lexical tokens; maximum parenthesis depth is 31.

Fifteen-gate search: 15 gates numbered 8 through 22; 195 declarations, 308 assertions, three header commands, and two query commands. This includes 30 predecessor bounds, 15 operation bounds, 15 symmetry bounds, 120 coefficient bounds, 120 gate equations, and eight target assertions. There are no pin equalities. The source contains 240,144 lexical tokens; maximum parenthesis depth is 30.

Complete template/semantic inspection applies only to these two source hashes. The associated 13 archive-member snapshots preserve supporting evidence; capturing README/audit bytes does not newly certify every unrelated narrative claim in those documents.

## Mathematical meaning of the entire constraint template

There are eight independent input coordinates. Source node i, for 0 <= i < 8, has encoded coefficient 2 in coordinate i and 0 in the other seven coordinates. Every encoded integer is twice the actual coefficient. A generated node g has one 5-bit predecessor selector a_g, another b_g, one 5-bit operation selector op_g, Boolean signs sa_g and sb_g, and eight 5-bit coefficient coordinates v_g,j. These selectors and signs are shared across all eight coordinates: the formula specifies vector gates, not separate per-coordinate circuit choices.

For each coordinate, the lookup text tests predecessor indices 0 through g-2 in ascending order and uses node g-1 as its default. It returns source constants for indices below eight and previously declared v coordinates otherwise. Unsigned bounds a_g < g and b_g < g ensure the fallback corresponds only to the valid index g-1. Consequently every operand is already available, no future node or cyclic reference is possible, and there is no unintended fallback alias. All 32 possible encoded index values were checked for every actual gate index 8 through 23. Unsigned comparison is essential when g >= 16. Every actual index is representable without truncation. The generator's broader stated budget range 1..24 would end at node 31, still representable; this review credits only the two actual budgets.

The unsigned operation bound selects precisely residues 0, 1, and 2. Let A and B be the selected encoded vectors after independently selectable Boolean negations. For op=0, V=A+B. For op=1, V=2A. For op=2, 2V=A. The third branch is exhaustive because the operation bound excludes every other residue. b and sb are irrelevant to the unary equations, although b remains a valid predecessor selector; this imposes no existence restriction because at least one predecessor always exists.

All four signed binary sums are available. The optional ordering a <= b applies only to binary addition. Swapping the two predecessor/sign pairs preserves each signed sum, including repeated predecessors, so this symmetry restriction removes no circuit. This was also checked by exhaustive exact scalar arithmetic over bounded coefficient values and all ordered operand indices used in these sources.

The unary operations permit a signed source, thus literally include negative doubling and negative exact halving. Under this model's signed binary inputs, symmetric coefficient bounds, and free output signs, these are equivalent to unsigned unary primitives with per-wire sign normalization: choose each unary output's orientation to remove its input sign, propagate orientations into later binary signs, and adjust final output signs. If a different cost model forbids that sign metadata, the encoding's precise signed semantics must be retained rather than silently reinterpreted.

## Signed ranges, exact halving, and no-wrap proof

The coefficient constraint is signed `bvsge v (_ bv28 5)` and signed `bvsle v (_ bv4 5)`. In 5-bit two's-complement interpretation, residue 28 is -4; the admitted encoded values are exactly -4,-3,-2,-1,0,1,2,3,4, corresponding to half-integer actual coefficients from -2 through 2. The source basis coefficients also fall within this range.

Negating any allowed operand stays in [-4,4]. A sum of two signed operands lies in [-8,8]. A doubled signed operand lies in [-8,8]. The doubled output side of an exact-halving equation also lies in [-8,8]. These intervals fit inside the signed 5-bit representable range [-16,15]. For an asserted equality, the difference of its two mathematical integer sides lies in [-12,12], which contains no nonzero multiple of 32. Therefore equality modulo 32 is equivalent to ordinary integer equality in all three gate cases. There is no wraparound witness or spurious half solution.

The checker exhaustively compared modular and ordinary equality for all 2,916 scalar add cases, 162 double cases, and 162 half cases, including signs and every possible allowed result. Every comparison agreed. Exact halving requires every coordinate of A to be even in encoded units and fixes V=A/2; it is not rounding, truncation, or arbitrary division in a finite ring. An intermediate outside the allowed grid or coefficient range is deliberately excluded, even if later cancellation would return it to range.

## Source-target constraints and circuit budget

The eight literal target rows are recorded in CHECK_RESULTS.json. Each target assertion asks that some generated node have all eight coordinates equal to either +2 times that row or -2 times that row. Both signs are checked for every generated node. This means the actual unnormalized matrix M is available with free output sign metadata and free selection/fanout. No separate output identity/order variables are needed; each assertion identifies its intended row. All row entries, signs, coordinate positions, gate alternatives, and conjunction/disjunction boundaries matched the independently reconstructed target template.

Each target row has four nonzero coordinates and all eight rows are mutually orthogonal with squared norm four, as checked by exact integer dot products. Hence no target is an original basis input, and no two target rows are equal up to sign. Excluding input nodes from target alternatives is harmless for this particular target. Different target assertions cannot be accidentally satisfied by the same signed row.

There are exactly k generated gates, each charged one arithmetic operation. This is equivalent to a budget of at most k in the stated model: any shorter admissible circuit can be padded with zero nodes computed as an input minus itself, which remain in range and do not affect outputs. The pinned control fixes k=16, all operations to signed addition, and every predecessor/sign choice. The unpinned source sets k=15.

The SMT targets M, not the final normalized transform M/4. The separate baseline certificate records normalization 1/4. Quarter-scaling operations and their cost are absent from both SMT sources. Circuit gate counts therefore cannot be presented as complete normalized-transform costs unless the common final normalization is accounted for separately. The formulas likewise do not model in-place restoration, memory costs, truncation at round boundaries, floating-point rounding, numerical stability, or arbitrary rational coefficients.

## Positive control: fresh witness and archived model

The pinned stages are four pairwise sums x_i+x_(i+4), four pairwise differences x_i-x_(i+4), then eight specified sums/differences of those intermediates. The fresh arithmetic replay builds all 16 encoded coefficient vectors from the eight doubled basis inputs, checks every predecessor gate is earlier and ordered, and checks every coordinate remains in range. Nodes 16 through 23 equal the eight target rows times two, in the certificate's recorded order with positive output signs. The result establishes exact linear identities for arbitrary inputs, under the stated exact arithmetic interpretation.

The entire supplied certificate was read as JSON data. All 16 gate records, input count, target rows, output mappings, normalization, and expected fields agree with the independently transcribed circuit. It was not imported as code.

The full archived positive_control.log was consumed by a flat, tightly constrained lexical format check for constant model definitions. No SMT parser or interpreter was used. All 208 definitions are unique, have the correct declared types and names, and agree with the independently computed selector, sign, operation, and encoded-coordinate assignments. There is no ignored model tail or unexamined assignment. The archived summary reports SAT in approximately 0.04418 seconds. That timing and SAT response are archived claims; the mathematical witness validation is fresh.

## Timeout and historical execution interpretation

slp_15.smt2 specifies timeout 30000 ms. Its exact saved log is `unknown` followed by reason `timeout`. Its summary agrees on budget 15, timeout 30000 ms, and status unknown, with archived elapsed time approximately 30.05005 seconds. The model remains unresolved: this review neither finds a 15-gate solution nor excludes one.

An earlier saved smt_run.log also records unknown/timeout and a model-unavailable error at line 509. The README attributes that earlier attempt to a 120-second run, but that duration is not established by the raw earlier log or the presently reviewed 30-second source. The currently archived generator's inert text only requests a model after a SAT response, consistent with the documented correction. No inference of historical solver version, dependency provenance, successful live rerun, or independent UNSAT proof is made.

An actual UNSAT result, were later obtained and validated, would concern only this finite coefficient grid, coefficient bound, gate set, gate budget, free-sign convention, and target. No UNSAT result is present here. A pinned SAT sanity check validates its own witness and helps detect encoding mistakes; it does not establish search completeness beyond the separately proved template semantics or validate an unrestricted optimality claim.

## Files and seal

COVERAGE.json and the two per-source JSON files are exact-hash integration records. CHECK_RESULTS.json contains all fresh arithmetic and witness outcomes. PROVENANCE.json and the preserved manifests tie inputs to their archive members and queue rows. PRESERVATION.json records unchanged originals. SHA256SUMS.txt hashes every deliverable except itself and SEAL.json; SEAL.json records the manifest hash and artifact count. This is an integrity seal, not an externally signed timestamp or attestation. No central coverage file has been edited.
