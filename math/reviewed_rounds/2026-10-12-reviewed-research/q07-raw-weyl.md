Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 33733aba847c4c8cac4302e58ead3f437e3a200b1fe06156a8a5eeb47f65345e

---

# Q07 bounded raw q-Weyl executor: independent scoped acceptance

11 October 2026. Verdict: ACCEPT for the declared bounded reference interface, subject to the exact artifact pins in SOURCE_BINDING.json. This closes Q07::raw-mode-executor only on that domain. It does not promote the implementation to a generic FFT, a production numerical implementation, an unrestricted field/length interface, or a historical novelty claim.

## Frozen objects and scope

The reviewed author archive is Q07_Bounded_Raw_Weyl_Mode_Executor_CANDIDATE_2026-10-11.zip, SHA256 1070584d6d3a13e6c5b81418818f94784c41022b28bdbc3294b11331f35054fa. The implementation src/raw_weyl.py has SHA256 165ba30d6bab6e9ea24f78e3e6b190c79cb50300d253742294b0a404cb71e923. All 14 payloads in the sealed manifest match, before and after the reviewer cold replay. All five source/dependency pins also match their independently read local originals. P05's exact SHA256 is the artifact named by accepted R20; H01's bytes and R04's explicitly scoped acceptance are present. Earlier mathematical acceptance is not being mistaken for executable acceptance.

The public execute interface supports dyadic 2<=N<=1024, supplied prime N<p<=65537 with N dividing p-1, supplied canonical primitive q, integer 1<=t<=N/2, canonical raw residues, and at most 16 fresh vectors. Supplied nonzero a,b are required for operator action. Plain list/tuple and exact built-in integer checks deliberately reject coercion, subclasses and booleans. Empty input and N=1 are DomainError; the length-N zero vector is a valid zero-mode acceptance. Unsupported/malformed input is distinguished from a mathematically valid sparse nonmember. The two fallback policies have their documented distinct output contracts.

The candidate source and fresh author/reviewer controls were inspected before execution. No original research program was imported or executed. Source documents were read only as inert dependencies. No external writes were made.

## Independent mathematics-to-code audit

1. Cold validation proves p prime by bounded trial division. For dyadic N, q^N=1 and q^(N/2)!=1 prove order exactly N. No general factorization or field/root discovery is silently assumed. Every call builds and meters the full supplied-root table anew.
2. Raw membership is learned from c, not supplied. BM processes exactly the first 2t raw entries. A true s-mode sequence has a nonsingular leading s-by-s Hankel matrix V diag(gamma) V^T, so its minimal recurrence has degree s and connection polynomial product(1-lambda*z). Two t samples suffice for s<=t, even with leading cancellations. An independent time-of-last-degree-change BM trace reconstructs the output connection and every named BM counter for all reviewer raw cases.
3. The pruned positive DFT of the connection coefficients evaluates C(q^v), rather than solving a free root oracle. Degree r and exactly r distinct grid roots certify that all roots are simple and allowed. Off-grid exponentials and repeated poles reject correctly. The derivative-denominator guard is mathematically redundant once a degree-r polynomial has r distinct field roots, but is safe.
4. With A=C sum_(j<r)c_j*z^j mod z^r, the residue of A/C at lambda^-1 equals -gamma/lambda. Thus gamma=-lambda*A(lambda^-1)/C'(lambda^-1), matching the implementation's sign and inverse-grid indexing u=-v. Nonzero-amplitude checking is conservative and paid.
5. Recovered modes synthesize every raw coordinate via a separate positive sparse-input DFT. Every coordinate is compared even when a mismatch is found. When r=0, every raw coordinate is compared with zero. This ensures soundness for arbitrary misleading prefixes; completeness of BM/residues ensures rejection is genuine nonmembership within the supported domain.
6. Character orthogonality gives (F_q c)_k=N*gamma_u exactly at k=-u, with every other bin zero. The output is an explicit N-element array. It is unnormalized and positive-sign.
7. Expanding the defining matrix gives M_(i,j)=a_i*b_j*sum_k c_k*q^(k(i+j)). Substituting modes yields (M_c x)_i=N*a_i*sum_u gamma_u*b_(-i-u)*x_(-i-u). This is the implemented weighted antidiagonal permutation sum. Our independent action oracle builds the antidiagonal coefficients directly from raw c and then performs a dense matrix-vector multiplication; it does not reuse recovered modes or the candidate FFT. The author's explicit inverse-sign anti-control also cold-replays.
8. Rejected inputs retain all failed-recognition counters. With fallback='fft', one positive raw DFT plus two positive DFTs per fresh vector evaluate the defining expression; fallback='none' emits no transform/action arrays. The independent checks compare both policies for every one of 20,947 rejected raw cases and verify the recognition-stage ledgers are identical.

The API supplies a,b as part of the target definition. It neither discovers them from a raw matrix nor proves that an arbitrary matrix is a q-Weyl companion-family correction. It has no common-chirp dispatcher. Sparse rejection does not reject other possible fast representations. Full rank for a single nonzero mode is consistent with a cheap restricted operator, and is not a generic transform speedup.

## Independent cost audit

The counters are named semantic events, not timings, instructions, or a complete Python allocation/bit-operation census. Inversion-call counts are annotations: their actual powering multiplications are already included in field_mul and must not be counted twice.

For L=log2 N, accepted cold preparation uses exactly N+2L field multiplications: N-1 table multiplications, L+1 for q^N, and L for q^(N/2). It uses 2L+1 powering-bit steps, N table writes, two root comparisons, and floor(sqrt(p))-1 trial divisions for valid prime p. Each of these exact identities is checked independently for every raw case.

For a pruned transform with support S, let a_d be the number of occupied residue classes modulo 2^d. Its exact butterfly count is B=sum_(d=0)^(L-1) a_d*N/2^(d+1). Active-node output initialization and writes are both 2B. Partition events equal |S|L; occupied leaves equal |S|. Every empty child is charged its returned zero-array length, and total node calls are 1+2 sum_d a_d. A separately implemented residue-class census checks these exact counts, not just the author's upper bound, for root discovery, accepted synthesis, rejected raw fallback, and 332 standalone kernel cases. Since a_d<=min(2^d,|S|), the advertised O(N(1+log(|S|+1))) bound follows; the partition traffic is dominated by that bound. The empty-support case is one node and N zero writes.

For r recovered roots, let m_p=popcount(p-2)+bitlength(p-2)-1. The implemented amplitude phase has:

- r(r+1)/2+r+r(2r+2+m_p) multiplications,
- r(r+1)/2+2r^2 additions,
- r subtractions, r inversion calls, and 2r equality calls.

The independent checks verify those exact counts on every reached amplitude phase. BM is independently re-traced including discrepancy loops, polynomial lengths/copies/padding, coefficient updates, and inversion powering; it performs at most 2t inversions. Together with residues, total inversions are at most 3t. Full input verification makes exactly N raw comparisons whenever reached.

Accepted scatter has N explicit zero initializations and s writes/multiplications. Each fresh-vector stage uses exactly Ns additions/mode terms, N(s+3) multiplications, N b*x writes, and N final output writes. In particular zero-mode action still pays O(N), and growing-s action is O(N(s+1)), not O(N log s). No cost-minimizing route selection is claimed for accepted dense-support cases.

For rejected fresh-vector fallback, let B1 and B2 be the independently reconstructed butterfly counts of the actual b*x and c*(F(b*x)) supports. The action costs B1+B2+3N multiplications and B1+B2 additions and subtractions, plus the measured FFT support/output events. There are two full support scans and N final output writes. We audit this exact count for 382 fallback fresh vectors. Raw fallback separately incurs its own actual support-tree cost. Failed recognition remains additional work.

Consequently the split-model accepted bound is O(sqrt(p)+N log(t+2)+t^2+JN(s+1)) with scalar inversions. The concrete implementation pays an additional O(t log p) modular multiplications to realize inversions. Unrestricted bit complexity and numerical stability are not certified. Storage is O(N(1+J)), including supplied copies and explicit J output arrays; recursion retains O(N) transform storage. The 17-bit modulus and fixed resource caps are API boundaries, not an asymptotic performance breakthrough.

## Finite evidence and limitations

The fresh independent checker passes 21,260 raw input/cap cases: 313 acceptances and 20,947 rejections. It compares 194,278 DFT coordinates and 67,588 operator coordinates across 478 fresh vectors. Coverage includes all F7^2 inputs/caps, all F5^4 inputs/caps, all ternary length-8 inputs at caps 1,2,4, randomized raw inputs over different valid fields and odd powers of primitive roots, and structured/undersized-cap cases through N=1024 and s=512. It includes maximal J=16 accepted and rejected calls at N=1024.

Additional evidence: 18 impulse cases; true early-cancellation examples with the first s-1 samples zero; off-grid and repeated poles; late corruption; separate-family chirps; 72 typed/domain refusals; 332 independently censused pruned kernels; 77 accepted fallback='none' equivalence checks; and replay/result-mutation isolation. All seven feasible observed acceptance/rejection outcomes are recorded. Defensive zero-residue/zero-amplitude paths were inspected, not claimed to have been dynamically reached.

The sealed author suite also independently cold-replays unchanged: 2,475 raw cases, 27,578 DFT coordinates, 13,376 operator coordinates, 48 kernel controls, 29 domain refusals, plus sign-orientation, maximum-batch zero-action, and result-isolation controls. These author totals are kept separate from reviewer totals. Original research executables remain inert.

The finite runs corroborate the proof-to-code audit; they do not exhaust every supported array or replace the argument. No hardware benchmark, memory profiler, floating-point accuracy certificate, world-priority search, or common-chirp integration is claimed. The abstract accepted proof remains intact.

## Scope and remaining work

Only the bounded raw-mode executor obligation is accepted. Classical mechanism attribution and historical-priority limitations remain. Broader non-dyadic, unbounded and extension-field interfaces, numerical/production implementation and common-chirp integration remain separate open work.
