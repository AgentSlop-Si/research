# Fourier bank bounds and prefix stabilizer research checkpoint

This archive preserves the research developed from 17:35 to 18:04 UTC on 10 October 2026, together with final independent acceptance receipts received through 18:08:37 UTC and the separately dated 18:10 Sheet follow-on. Its strongest uniform bank theorem is a bound of 9N/5 + O(1) individual signed banks over a finite algebraic extension of the cyclotomic field. It also contains an exact prefix-ordering optimum and a verified necessary reduction of one fixed order-eleven factorization problem.

These are separate mathematical models. The bank theorem counts sums of resolvent banks. The aggregate theorem counts separately colored graph edges. The fixed-support work studies a particular 99-edge scalar graph. None establishes a faster scalar Fourier transform, an unrestricted graph impossibility, worldwide novelty, or a completed manuscript.

## The signed bank model and what is counted

For odd N, let q be a primitive Nth root of unity and K = Q(q). Indices are modulo N. Define S e_i = e_(i+1), T e_i = q^i e_i, and the negative Fourier matrix F_N[k,t] = q^(−kt).

An individual permitted signed bank is

    B_(epsilon,delta)(alpha,beta;w)
      = (1/N) sum_(j=0)^(N−1)
          w_j (I − alpha S^epsilon − beta q^(epsilon delta j) T^delta)^(-1),

where epsilon and delta are independently +1 or −1 and the legality condition is 1 − alpha^N − beta^N ≠ 0. This is the unchanged grammar from the [accepted base-field theorem](research_cycle_1535/basefield_bank_attainment/BASEFIELD_FOURIER_UPPER_BOUND.md), source SHA-256 f8bac209b3cd12da34618bb11118a0bf81b69cbb2c765d97265dda49c5202155, with its [acceptance receipt](research_cycle_1535/basefield_bank_review/ACCEPTANCE_RECEIPT.json).

Each bank contains N phase-weighted resolvent terms. Thus M declared banks have NM raw phase weights and NM literal resolvent branches. A bank is not a scalar operation, a scan, a free inverse, a root orbit, or a trace. No new coordinate maps or uncharged pre/post operations are admitted.

The new bounds use beta = 1, orientations (++,-+,+-,--) = (m,1,1,m), the same m distinct nonzero roots of a monic polynomial g in K[t] for both same-sign groups, and node 1 for each cross-sign singleton. The roots, bank amplitudes and raw weights may lie in a splitting field L/K with [L:K] ≤ m!. This is a finite algebraic extension in characteristic zero, not a finite field. The guard is then −alpha^N ≠ 0.

## Accepted bank results and their versions

- Strongest uniform result: for every odd N ≥ 27, put d = floor((N+13)/10) and m = N−d. At most 2N−2 floor((N+13)/10)+2 = 9N/5+O(1) banks suffice. The proof merges the two chirp parity components before step-one elimination. Only the three needed coordinate functionals are excluded at this range. See the [step-one theorem](research_cycle_1735/common_annihilator_barrier/STEP_ONE_LINEAR_BANK_THEOREM.md), [complete independent proof](research_cycle_1801/linear_bank_independent_review/LINEAR_BANK_INDEPENDENT_REVIEW.md) and [step-one acceptance](research_cycle_1801/linear_bank_independent_review/STEP_ONE_REVIEW_RECEIPT.json).
- Earlier linear-saving version: for odd N ≥ 45, the step-two proof gives 2N−2 floor((N+19)/16)+2 = 15N/8+O(1). Its [theorem](research_cycle_1735/common_annihilator_barrier/LINEAR_SAVING_BANK_THEOREM.md), [structured interval lemma](research_cycle_1735/three_basis_feasibility/STRUCTURED_INTERVAL_ELIMINATION.md) and [separate acceptance](research_cycle_1801/linear_bank_independent_review/STEP_TWO_REVIEW_RECEIPT.json) remain intact.
- Earlier square-root versions: 2N−2 floor((sqrt(N)+16)/13)+2 for odd N ≥ 1297 and the stronger 2N−2 floor(sqrt(N)/8)+2 for odd N ≥ 1025 remain accepted. Their separate [constant-thirteen receipt](research_cycle_1735/constructive_rank_independent_review/UNIFORM_SQRT_REVIEW_RECEIPT.json) and [constant-eight receipt](research_cycle_1735/constructive_rank_independent_review/CONSTANT_EIGHT_REVIEW_RECEIPT.json) bind the frozen source versions.
- The underlying [rank-envelope and finite-lift review](research_cycle_1735/constructive_rank_independent_review/BANK_ENVELOPE_AND_LIFTS_REVIEW.md) accepts rank A ≤ min((d−1)(d−2)/2,4d−11), the guarded 2m+2 realization, and 18,24,54 banks at N = 13,17,35. These individual constructions can be stronger than the uniform formula at their orders. The N=11 lower bound of 14 is restricted to the stated fixed-cross-singleton architecture.

The independent proof checks monicity, nonzero constant, squarefreeness, axis rank, descent of g to K, and realization in actual banks simultaneously. A bounded exact recipe tests a grid with Nd+2m rational integer choices per free coefficient parameter, then splits g and solves the interpolation systems. This may be very expensive. Neither efficient preparation nor improved scalar arithmetic complexity, numerical stability or bit complexity is proved. The accompanying finite controls corroborate the proof; they do not replace its all-order argument.

## Aggregate edge count and exact ordering optimum

For prime p ≥ 5, define W(n) = sum over primes r of v_r(n)(1−1/r). The [subgroup-chain construction](research_cycle_1735/aggregate_subgroup_chain/MULTIPLICATIVE_PREFIX_CHAIN.md) has exact separately colored aggregate edge count

    E(p) = 2p²+2p−2 − (p−1)W(p−1).

An unconditional sequence of prime divisors of Fermat numbers gives Omega(p log log p) savings relative to the dense baseline 2p²+p. The graph and its coefficient table remain quadratic; one endpoint is dense. This construction uses the positive Fourier convention specified in its own proof.

For every finite abelian group G of order n, the [prefix theorem](research_cycle_1744/prefix_stabilizer_optimality/PREFIX_STABILIZER_OPTIMALITY.md) proves

    max over all orderings sum_j (|Stab(T_j)|−1) = n W(n).

Maximizers are exactly recursively ordered prime-index subgroup coset blocks, with independently maximizing internal orders and a unique top subgroup. The labeled count is A(G) = sum over maximal K of [G:K]! A(K)^[G:K], with A({0})=1. Consequently the displayed Fourier edge count is optimal among all orderings of its fixed sine-difference coefficient family and single-chain architecture. Different coefficient families, multiple chains and arbitrary endpoints are outside this optimum. See the [aggregate acceptance](research_cycle_1735/constructive_rank_independent_review/AGGREGATE_REVIEW_RECEIPT.json) and [independent prefix review](research_cycle_1753/prefix_independent_review/INDEPENDENT_REVIEW.md).

## Fixed support poles and the symbolic checkpoint

The [pole and gauge review](research_cycle_1735/pole_escape_review/REVIEW_REPORT.md) proves that internal gauges fixing boundary vertices make a finite DAG integral exactly when every surviving full input-output path has nonnegative valuation. Zero edges are omitted. For the fixed N=11,99-edge support, the earlier integral obstruction therefore forces a negative full path at each place above 11 in any hypothetical algebraic Fourier factorization. This does not exclude arbitrary poles or arbitrary complex coefficients.

The review excludes three specific tropical candidates, certifies 26 one-family minors, forces 63 coefficients nonzero, and supplies 21 safe gauges plus three covering charts. Nonzero coefficients need not be valuation units.

The later [independent symbolic audit](research_cycle_1758/symbolic_independent_review/REPORT.md) accepts only an exact necessary reduction: 21 safe gauges, 26 Laurent eliminations and 36 linear eliminations leave 16 variables and 59 equations, with 30,694 total terms. The [hash-bound receipt](research_cycle_1758/symbolic_independent_review/RECEIPT.json) binds every replayed input.

Reconstruction must retain nonzero surviving coordinates 39,41,44,52,83,88,91,92 and six nonconstant guards for eliminated coordinates 98,96,89,95,46,48. The guards are included in both stage and final coordinates. Two other eliminated mandatory values are verified nonzero constants. The bare final equations alone are not certified equivalent to the original problem. No contradiction and no Fourier factorization has been found. Guarded-cancellation work begun after this checkpoint is excluded.

## Sheet cutoff and historical wording

The included [Sheet verification receipt](research_sheet_1755/FINAL_VERIFICATION_RECEIPT.json) concerns the 18:00 UTC content checkpoint, verified at 18:04:45 UTC: 26 content cells, three grouped result rows, 6,038 native cell objects checked, 178 catalogue IDs, 18 source comparisons and two native tables preserved. The [exact added text](research_sheet_1755/EXACT_APPEND_TEXT.md) and [before-and-after changes](research_sheet_1755/EXACT_CHANGE_MANIFEST.json) are retained. The full historical workbook and broad API dumps are not duplicated.

That Sheet checkpoint records the constant-eight bank theorem and predates the step-one/step-two and symbolic acceptance. Its dated wording remains unchanged. Likewise, frozen author documents may say “pending review” or “unreviewed”; later acceptance applies only to the exact source hashes and scope identified in [ACCEPTANCE_BINDINGS.json](ACCEPTANCE_BINDINGS.json). [VERSION_STATUS.json](VERSION_STATUS.json) records this precedence. The separately dated [18:10 Sheet follow-on](research_sheet_1805/FINAL_VERIFICATION_RECEIPT.json) is also included: it appends the accepted 9N/5 theorem to three existing cells, creates no rows, preserves the earlier history and passes native, export and rendered-view verification. Its [exact changes](research_sheet_1805/EXACT_CHANGE_MANIFEST.json) and [added text](research_sheet_1805/EXACT_APPEND_TEXT_FINAL.md) remain separate. Two row heights were adjusted after clipping was observed. The symbolic reduction remains a separate accepted research receipt; this Sheet follow-on does not add it.

## Verification and reconstruction

Only explicitly allowlisted research files are exported. Source programs are preserved as inert text; none was executed, imported or compiled while preparing this archive. All bound sources were freshly rehashed. The only content transformations remove private spreadsheet location metadata from four JSON exports and private conversation/file-delivery identifiers from the earlier fixed-support report. Canonical source hashes and export hashes are separately recorded in [SOURCE_EXPORT_BINDINGS.json](SOURCE_EXPORT_BINDINGS.json), with an exact field-level [transformation ledger](TRANSFORM_LEDGER.json). Mathematical statements and review decisions are unchanged. Earlier archives and source versions remain preserved; earlier ZIPs are not embedded merely to duplicate them.

The 52,488,899-byte final certificate is stored only as its 1,113,781-byte original gzip. Its SHA-256 is 2d3b26ba34c07dd4192cac12ca9fa2144dbc37becef22126f3692702ec144952; decompression reconstructs exact original SHA-256 ad2500599d3af6d04e9dca371952234cfd09cd70b63f1bc15355bd32b53a6cc6. The 30-step checkpoint is handled the same way. Both gzip outputs were compared byte-for-byte against their frozen dense originals. [COMPRESSED_CERTIFICATES.json](COMPRESSED_CERTIFICATES.json) records both pairs.

To reconstruct in a separate writable copy, use standard gzip decompression and retain the gzip:

    gzip -dc research_cycle_1734/pole_escape/full_fourier_linear_reduction.json.gz > research_cycle_1734/pole_escape/full_fourier_linear_reduction.json
    gzip -dc research_cycle_1734/pole_escape/full_fourier_linear_reduction_30steps.json.gz > research_cycle_1734/pole_escape/full_fourier_linear_reduction_30steps.json

Check their SHA-256 values against COMPRESSED_CERTIFICATES.json before any reproduction attempt. Use python VERIFY_ARCHIVE.py for a data-only integrity check. Treat the research programs as source to inspect before running. Canonical source-hash gates distinguish privacy-transformed exports from their originals; see [canonical replay guidance](CANONICAL_REPLAY_NOTICE.md) before attempting mathematical replay. Some historical programs refer to earlier project material beyond this focused packet; a preserved reproduction command is not a claim that every historical dependency is bundled.

[ALLOWLIST.json](ALLOWLIST.json) enumerates every archive member. [EXPORT_MANIFEST.json](EXPORT_MANIFEST.json) and SHA256SUMS cover all payload and metadata files except their explicitly stated self-reference exclusions. A separate full-member receipt accompanies the saved archive and binds every member including those checksum documents. The privacy scan recursively inspected all text and both decompressed gzip payloads, and verified that no nested predecessor ZIPs, credentials, private conversations or transport records were included.

## Open questions

The approximately 8N/5 bank direction still needs stronger simultaneous legal-polynomial guards. Smaller splitting fields, attainment of the strongest counts over K alone, unrestricted minimality and efficient construction remain open. The aggregate optimum has not been extended to arbitrary coefficient families or endpoint designs. The fixed-support algebraic factorization problem with poles remains open. The included literature reports document bounded applicability checks; they do not certify historical priority.
