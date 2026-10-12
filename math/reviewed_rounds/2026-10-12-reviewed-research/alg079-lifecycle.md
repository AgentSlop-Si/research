Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: bfc3fdbbf58c74bfbad0f9e22c43dcbe51859709cf7124c461aac975ab454430

---

# ALG-079: independent bounded cyclic-solver and lifecycle integration review

Date: 2026-10-11 UTC

## Verdict

ACCEPT the exact frozen bounded replacement API reviewed here. It integrates the previously accepted reverse cyclic solver, including the beta=0 diagonal branch, with guarded dyadic/Good-Thomas-3 deferred sessions and a supplied-candidate Green transform. Full cyclic certification, all-frequency denominator checks, ordinary fallback before optional setup, exact persistent backup charging, and the stated cold field-operation ledger are independently verified.

This is a scoped implementation acceptance within existing ALG-079. Keep the broader `ALG-079::lifecycle-integration` gate OPEN. The archived public implementation, every historical importer/caller and its cost objects, detector/compiler/convolution backend, complete production RAM/bit/elapsed-time accounting, historical priority, and practical performance are not accepted by this review. No new canonical claim, discovery, rank upgrade, or historical-priority conclusion is created. Historical limitations remain attached to the historical source bytes.

## Frozen object and provenance

The author supplied `ALG079_Bounded_Cyclic_Lifecycle_Integration_CANDIDATE_2026-10-11.zip`, 71,656 bytes, SHA-256 `f884ae10559f70836768eaa52aa5c41143816c4e4984130f6dd8754341a7b827`. It has 23 ZIP members, comprising 22 manifest payloads and the manifest itself. All payload lengths/hashes and all 11 preserved historical source pins were independently verified. No unlisted payload exists.

The reviewed implementation, `src/integrated.py`, is 20,347 bytes with SHA-256 `2141c18183e619322443a5bb5660fe52c88018484ccca2392bf88650ef9354d3`. The author contract has SHA-256 `fc899afec7a8bb37818e2e060109fe5c0b68e0c900de0b908422a93841215f16`. Author results have SHA-256 `3e0dfeb0bbe841e2c93d00d129f4528042cd3ac87e1791727aa4ba837fb6fe5a`. Exact bindings and the complete author archive are included as evidence.

The review imported only this freshly authored implementation for its independent controls. The author’s fresh harness was subsequently replayed separately against a cold archive extraction; it reproduced the sealed author results byte for byte. The independent control program does not import any author test helper. Archived original research programs remained inert text and were neither imported nor executed.


## Public boundary

The accepted transform is the positive-exponent, unnormalized DFT over an explicitly validated prime field with 2 <= p <= 2^31-1, 2 <= N <= 4096, and N dyadic or N=3G for a dyadic G>=2. The supplied root must have exact order N. Field primality and root validation are executed, not assumed. Boolean inputs are refused where integers are required. This finite executable boundary does not narrow the separately accepted all-field reverse-solver theorem.

The reviewed public surfaces are RootPlan, its session factory, CyclicPlan supplied with a validated Field, Candidate, and transform. Direct construction of internal graphs with fabricated root tables, mutation of implementation internals, concurrent sharing of mutable counters, hostile executable Python objects, and arbitrary exception-throwing iterables are not certified interfaces. Ordinary malformed proposal containers are handled safely as described below.

A proposed sparse model must be a Candidate whose coefficients are a tuple of two-element tuples, with distinct support indices, nonzero integer coefficients, support at most s, a nonzero alpha, and 1 <= delta < N. The wrapper retains the static guards 1 <= s <= 8, N > 2s+2, and p > 4 sum(i^2, i=1..s)+20. Guard failures fall back. The proposal is supplied; there is no candidate discovery or compiler in this replacement API.

## Solver audit

For beta != 0, each equation is d_i x_i + beta x_(i-1) = r_i. Setting q_i=-d_i/beta and u_i=r_i/beta gives x_(i-1)=u_i+q_i x_i. Reverse affine composition computes B such that x_(N-1)=B+A x_(N-1), where A is the product of q_i. The code sets x_(N-1)=B/(1-A), then reconstructs the other coordinates in reverse order. This matches the right shift, including N=2 and characteristic two.

The determinant is (-1)^(N-1) beta^N (1-A), so the closure guard is exact. Zero diagonal entries are harmless when beta is nonzero. When beta=0, the implementation first rejects any zero diagonal; otherwise it stores diagonal inverses and solves componentwise. RHS validation precedes arithmetic and leaves counters unchanged on refusal.

The literal accepted nonzero-beta plan uses 2N multiplications, N+1 negations, one addition, and two inversions. Each solve uses 3N multiplications and 2N-1 additions. The zero-beta plan uses N inversions and its solve N multiplications. Both Green matrices use this implementation. The new wrapper reads the actual shared field ledger and adds no historical hard-coded 3N+1 charge.

Independent controls exhaust all diagonals and all beta values over GF(2), N=2..6; GF(3), N=2..4; GF(5), N=2..3; and GF(7), N=2..3. They compare to separately implemented dense elimination and verify every output row equation. They accept 3,310 plans, including 365 beta-zero plans and 1,417 plans with a zero diagonal, and correctly refuse 783 singular plans. They check 26,350 RHS solves and 16,550 invalid-RHS nonmutation cases. These finite controls support the source-level recurrence and determinant argument; they do not replace it.

## Deferred lifecycle and backup audit

Both dyadic and GT3 sessions validate a complete preview batch before graph mutation. The allowed progression is NEW -> PREVIEWED -> COMPLETE or NEW -> COMPLETE. Repeated full returns the cached immutable tuple without arithmetic or mutation. Preview is refused after preview, completion, or close. Reset validates a fresh vector first; an invalid reset leaves state, counters, caches and backup banks unchanged. A successful reset clears the old input epoch, and may explicitly reopen a closed session. Close releases the session’s data, backups, node/diagnostic states and output caches; shared plan/root tables are not claimed to disappear.

At each one-child dyadic node, the saved half is exactly the original operand overwritten by that child. The other original half remains in the inactive subtree until completion computes the missing branch. The saved missing-sibling subtrees partition the unqueried leaves, establishing exactly N-q persistent backup field words after q distinct queried outputs. The independent checker counts actual bank list lengths as well as the reported counters. Full completion releases every bank and executes each full graph primitive once.

For GT3, if r row frequencies are touched, all three row previews have that same r, so the exact row-bank total is 3(G-r). It is not N-q for outer outputs. CRT input and output indexing, triple lazy caches, and row completion are consistent with the positive DFT. The mixed-radix identity-twiddle skip is restricted to the row j=0 case; triple products remain literal, preserving the characteristic-seven qualification.

Full dyadic counts are N log2(N)/2 each of additions, subtractions and products. Full GT3 counts are 3G log2(G)/2+4G additions, 3G log2(G)/2+2G subtractions, and 3(G log2(G)/2-G+1)+2G products. These are graph counts, not total cold cost.

The independent controls cover 2,598 preview/completion schedules and 33 full-only schedules across N=2,4,6,8,12,16,24,32,48,64,96, with all nonempty batches through N=8, duplicate/reversed batches, singleton queries, random inputs, zero inputs and asymmetric basis inputs. They also check 77 invalid-query, 220 invalid-reset, 44 reset/reuse, and 44 closed-refusal cases. Separate maximum-size controls use N=4096 and N=3072 with a non-DC basis vector, and the maximum supported prime is exercised at N=2 and N=6.

Default live storage is O(N) field words and O(N) node/triple states. Diagnostic primitive-label sets are optional and need O(N log N) entries. N-q and 3(G-r) count only persistent backup banks. Root tables, graph arrays, temporary slices, caches, integer metadata and Python overhead are not totalled by those equalities. The contract correctly declines a complete RAM certificate.

## Certified wrapper and fallback audit

The ordinary RootPlan and session exist before optional GreenPlan construction. No proposal, a failed static guard, or a malformed proposal can enter optional setup. A refused or singular Green plan completes the existing ordinary graph. This avoids the historical constructor-before-fallback failure within the new API.

With F[k,j]=omega^(kj), the code’s matrices satisfy LF=FP, with L=diag(a+c omega^k)+bS and P=diag(a+b omega^(-j))+cS. It computes the probes but never accepts on them alone. Every coordinate of A(S)Px=e_0-alpha e_delta is checked, even after a mismatch. Every spectral denominator A(omega^k) is evaluated before deciding whether any is zero. If all pass, Fourier diagonalization gives FPx=(1-alpha omega^(delta k))/A(omega^k), and the exact L solve returns Fx. Failed certification or denominator checks finish the same deferred graph. Successful structured exit closes the abandoned preview data and backups.

Independent structured fixtures were built differently from the author’s: select random sparse support, delta and alpha; form the desired residual in spectral coordinates; use a direct inverse DFT; then solve P densely. One hundred distinct fixtures across five dyadic/GT3 domains pass full output comparison, including 40 beta-zero certified outputs. All 100 cold field ledgers match independently derived formulas. The checker also verifies 300 corrupted-input certificate fallbacks, with every coordinate charged; 15 valid cyclic certificates with singular A and full denominator scans; 50 malformed-proposal fallbacks; 20 refused Green-setup fallbacks; and five no-proposal routes with no Green/solver/residual work.

During pre-seal review, Candidate(None,1,2) and Candidate(3,1,2) exposed an uncaught TypeError at tuple conversion. The author repaired this before freezing: coefficients must now be an exact tuple and malformed containers take ordinary fallback. The repaired source is the hash accepted above. This report does not accept the earlier preview bytes. Final controls include the triggering malformed inputs, and the author added its own regressions. No outstanding defect was found on the supported surface after this repair.

## Cold accounting and independence

The field ledger explicitly includes root-order checks, root-table preparation, GT3 coefficient preparation, both Green plans, preview graph, probes, residual, full certificate, denominator scan, decode and solve. The independent formulas count preview branches from distinct frequency residues at each graph level, rather than invoking the candidate’s recursive scheduler. They account separately for both possible zero-shift plans. Repeated-squaring counts are popcount(e)+bitlength(e)-1 for each checked exponent. No phase mismatch appears in the 100 complete certified ledgers.

Prime trial division has a separate integer counter. CRT index inverses, integer arithmetic, representative reductions, comparisons, memory movement, allocation, dictionaries, instrumentation and host overhead are not field operations in this stated model. Inversions are separate literal primitives, not assertions of constant bit-time. No detector/compiler cost is paid because none is implemented; that fact is disclosed, not credited as an improvement.

The independent program was written after inspection of the fresh implementation and author controls. It does not claim blind review or a disjoint mathematical technique for standard dense elimination. Its input families, spectral construction, level-residue ledger and whole-state snapshots are separately authored. The fresh author harness is separately reproduced: 5,996 schedules, 16,056 RHS matches and all sealed counts/results are byte-identical. Review evidence distinguishes those replay counts from the new independent counts.

## Scope and remaining work

The bounded replacement API is independently accepted, including reverse/beta-zero solves, guarded lifecycle, exact bank counts, certificate/denominator guards, fallback-before-setup and bounded cold field accounting. Historical public source/all callers and detector/compiler/backend still need migration. Complete production cold RAM/bit/elapsed-time accounting remains open. This acceptance does not certify unmodified original programs or all-length/all-field executable compatibility. Historical constructor witnesses and the characteristic-seven literal-product qualification remain separate.
