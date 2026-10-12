Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; scientific claims, exact source/cost boundaries and limitations are retained. Original source-report SHA-256: 72ab5448080d6f69bbaad9a4400021d7b018cc154a6f20951d2eb9b8c1cbb55b.

Review date: 12 October 2026 UTC.

The [constructor-witness correction](alg079-constructor-witness-correction.md) is part of this reviewed publication. The original candidate report remains unchanged; no universal length-specific refusal claim is made.

# ALG-079 historical caller migration: independent acceptance with a document correction

12 October 2026 UTC. **ACCEPT, bounded to the exact migrated cold entry and executed historical closure below.** The original candidate report contains one wrong constructor domain. Its bytes remain unchanged; the explicit correction below governs publication.

## Source-bound conclusion

- Candidate archive: `ALG079_Historical_Dyadic_Caller_Migration_CANDIDATE_2026-10-12.zip`, 108431 bytes, SHA-256 `00f446e1102aabcd5b913ff707ad9ff1ebd75bf433f6ade64e08c86aed149ed1`.
- Accepted migration: `candidate/src/migrated_caller.py`, SHA-256 `843e5c12db800b530d200ab7d545ada01a29d3fae93881a24c1deaea342dfd00`.
- Accepted backend: SHA-256 `2141c18183e619322443a5bb5660fe52c88018484ccca2392bf88650ef9354d3`; legacy bridge: SHA-256 `da8dcf482f4c6b4ae022cdf50b974b6b828747afa81cab97ab20a6e2ab02023b`. Both are byte-identical to the prior independent bounded bridge review.
- All 13 historical copies match the authoritative original files, their size and SHA-256 pins. No original historical source was edited. The actual `discover_short_probe`, cyclic certificate, sparse denominator evaluation, hypercube compiler, and original `transform_deferred_conjugate` are executed. Importing 13 modules does not mean every function or script entry point in those modules is qualified.

This is a new acceptance of one explicitly named and executed cold migration, distinct from the prior bounded ABI bridge. Broader lifecycle integration remains open.

## Independent numerical, algebraic and source checks

The original author suite replays all 110 cases with byte-identical results. A separately written checker adds **148 all-output direct-DFT cases**: 39 certified exits, 81 detector fallbacks, and 28 pre-detector cold fallbacks. Its fixture generator uses direct inverse DFT and independent dense Gaussian elimination, not the accepted backend solver or the author's fixture helper.

The fresh suite compares 120 detector-run cases with the unchanged original caller body using the compatible replacement engine: every output, actual detector metadata, factor-compiler result, and claimed Work arithmetic delta matches. All 39 recovered models independently satisfy the cyclic identity at every coordinate and have exactly reconstructed, nonzero Fourier denominators. Twenty-nine certified models compile, and their factors reproduce both the scaled/shifted sparse polynomial and the full cyclic defect identity. Ten certified models do not compile; exact output does not depend on compiler success.

Thirty-six corrupted spectra preserve every actual preview coordinate yet fail the full certificate and return the exact ordinary DFT. A further reviewer-constructed nullspace perturbation preserves the previews and first six cyclic equations but violates a later equation. This rules out an apparently plausible six-entry certificate replacement. Both actual linear-trace extraction and half-subgroup scanning occur. The actual singular spectral-denominator branch is reached and its zero entries observed independently; the guard remains before decoding.

Two more closed-form boundary checks exercise N=4096 ordinary fallback and p=2^31−1 at N=2. Ten malformed/out-of-cap raw domains are rejected. These are bounded controls, not exhaustive validation of the entire admitted input domain.

## Literal compiler arithmetic and non-overlapping cost interpretation

A reviewer-owned AST instrument counts every executed multiplication expression in the unchanged compiler. There are three expression sites: incident coefficient normalization, factor expansion, and the terminal `-alpha*cinv` product. Across 80 compiler observations, the literal tally equals historical Work.multiplies plus exactly one when compilation succeeds, and equals Work when compilation returns None. The migrated caller adds precisely that missing successful-return product. This establishes literal compiler multiplication accounting for the exercised calls, not a full primitive audit of every detector routine or operation category.

All 39 certified cases verify the exact replacement solve Field counts: N products/zero additions when the L shift beta is zero; 3N products/(2N−1) additions otherwise. The complete post-detector/compiler decode tail is 6N plus the solve products, N plus the solve additions, and one batch inversion. The unchanged caller's stale solve charge is larger by (2N+1 products, 2N additions) for beta zero, and (one product, one addition) otherwise; successful compilation adds one product back to the new caller. The net original/new differences are checked exactly.

Every fall-through completes exactly one dyadic graph: (N/2)log2(N) products and Nlog2(N) additions/subtractions. Preview storage has N−q retained backup words for q queried coordinates. A preserving constructor observer verifies an actual NEW fallback session exists before every attempted Green constructor. Guarded detector budgets perform no Green arithmetic. Failed setup work stays in Field. Lazy residuals materialize at most once. Certified exits release data, backups, node state and cache; fallback releases its backup bank.

Field and Work are overlapping views: graph/residual/solve work is already projected into Work, while root/Green/solver preparation is outside Work. Do not add the overlapping phases. Selected traffic counters are not a complete memory model. No production RAM/bit/time certificate, broad speedup, root-search bound, or every-detector accounting/totality theorem is asserted.

## Required factual correction to the candidate report

For the original constructor with default green=(7,2,1):

- (N,p,omega)=(16,1201,473), generator argument 11: L diagonal index 14 is zero; constructor raises ValueError('zero diagonal entry').
- (N,p,omega)=(32,353,294), generator argument 3: L diagonal index 25 is zero; constructor raises the same error.
- (N,p,omega)=(64,193,125), generator argument 5: neither L nor P has a zero diagonal; the original constructor succeeds. Two original-caller direct-DFT baseline vectors pass.

The candidate REPORT incorrectly substituted the third domain for the second in its refusal sentence. Its stored raw observations already contain the correct N=32 witness. Fresh independent observations are in `output/CORRECTED_WITNESSES.json`. The corrected statement is about these exact parameterized witnesses, not all N=32 or N=64 cases and not the unrestricted solver class. The migrated cold path returns exact outputs on all three domains.

## Mutation sensitivity

All **11** separately executed in-memory mutants are detected: missing compiler correction, unconditional correction after failed compilation, stale solve charges, omitted close, wrong preview shift, bypassed full certificate, six-coordinate certificate, bypassed singular-denominator guard, removed detector cap guard, expanded raw N cap, and fallback graph restart. `output/MUTATION_RESULTS.json` records the detecting assertion or original denominator refusal. Mutants are never written into the candidate or original sources.

## Publication and remaining obligations

This bounded migration preserves the earlier accepted results. Other callers/importers, full detector/compiler accounting and totality, broader cold resource obligations and production RAM/bit/time remain open. No historical-priority, broad speedup or full-caller qualification conclusion follows.

The candidate REPORT is retained as historical evidence. A published reviewed derivative must incorporate the explicit witness correction and link this review. Do not silently quote its incorrect N=64 refusal. 

## Reproduction

Run `python -B src/independent_check.py`, `python -B src/mutation_check.py`, and `python -B src/witness_check.py` from an extracted review packet. The candidate author replay is `python -B candidate/src/test_historical.py`. These executions use only the local pinned code plus Python standard-library modules. `src/audit_sources.py` additionally compares against the preserved authoritative original source files. Final cold-replay and archive hash evidence are supplied with the external reviewer seal.
