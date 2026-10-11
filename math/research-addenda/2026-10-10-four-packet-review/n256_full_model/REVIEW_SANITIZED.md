# Sanitized publication copy

Original review SHA-256: 17eb1fda8d7133b52568c2760754c8d424b2cc7821f50fe3d4f4a69f7d2593f2. Private source identifiers are omitted. Mathematical text is otherwise unchanged. Original review-date statements and historical execution/provenance claims below refer to that original review; they are not fresh claims about this publication assembly. Use the addendum README and replay script for the self-contained mathematical replay and its explicit archive/history exclusions.

# Independent review of the N256 complete feasibility model

**Disposition: accepted with scope clarifications.** The augmented stage system, pivot-safe linear-field-work inverse action, complete quadratic Fourier encoding, and patchwise kernel-incidence formulation are correct for the stated fixed affine routing. Their counts check. Fresh checks independently recreate the complete compressed equation family, exercise every basis column over both source fields, and reproduce the saved-point rejection. No Fourier factorization has been found or ruled out.

The material is an exact model and verification advance in the existing N256 research line. It is not a new fusion, a solved coefficient system, a faster arbitrary-input FFT, an all-length construction, a bit-complexity result, or a novelty claim.

## Source identity and audit boundary

The actual Library report and archive were materialized for this review:

- Report: `[private source identifier omitted]`, `RESEARCH(20261010-233019).md`, 4,908 bytes, SHA-256 `34b357277f25adcff11d212c54b624baabb9e070ce86adc9f60e6fbb2e85d482`.
- Archive: `[private source identifier omitted]`, `fft_banded_full_feasibility_checkpoint_2026-10-11.zip`, 5,696,733 bytes, SHA-256 `445a62e057f27449d8d503a2334e708797bc4907b5e8e92c07294cf1f82d8f3a`.
- The separate report is byte-identical to the archive's `RESEARCH.md`.
- All 16 entries in the source `SHA256SUMS.txt` match.
- The nested `prior_checkpoint_full.zip` has SHA-256 `2b712be2a70f7293a0c7d59ef2ed08c66b0c845f329e0afa2a38fd114cda90cc`, matching the prior independently reviewed saturation packet. Its ZIP integrity check passes.

The proof certificate, report, README, handoff, Python implementations, and saved JSON logs were inspected. Source Python and shell programs were never imported, compiled, or executed. `fresh_checker.py` is new audit code and reads inert JSON and archive bytes only. It uses installed NumPy and SymPy. Source logs are compared with independently obtained results, not relabeled as fresh evidence.

`source_hashes.json` pins source identities and members. `proof_controls.json` records the accepted claims and their controls; `fresh_check_results.json` records the actual audit outputs. No external sheet, repository, manuscript, or service was modified by this review.

## 1 Exact augmented system and inverse action

The source stage is

S[i,j] = a_i b_j for i > j, S[i,i] = d_i, and S[i,j] = c_i e_j for i < j.

Interleave the unknowns as (x_i,L_i,R_i), and the equations at coordinate i as

1. d_i x_i + a_i L_i + c_i R_i = y_i;
2. L_0 = 0, or L_i - L_(i-1) - b_(i-1) x_(i-1) = 0;
3. R_(N-1) = 0, or R_i - R_(i+1) - e_(i+1) x_(i+1) = 0.

This gives a 3N-square matrix A with lower bandwidth 4 and upper bandwidth 3. In particular, row 3i+1 can reach column 3i-3, while row 3i+2 can reach column 3i+5. The implementation's introductory “half-bandwidth 5” wording is a conservative bound, not the sharp bound used by the proof.

The L and R recurrences have unique solutions for any x over any commutative coefficient ring. After the same permutation of rows and columns groups x, L, and R, the auxiliary diagonal block is the direct sum of unit triangular matrices. Its determinant is one and its inverse is polynomial because its strictly triangular parts are nilpotent. Its Schur complement is S. Therefore det(A) = det(S) is a polynomial identity, valid even when diagonals or leading principal minors vanish.

Over a field, A is invertible exactly when S is. This does not assert that a nonzero determinant is sufficient over a general ring; there the determinant must be a unit.

For the field solve, elimination searches rows k through k+4 for a nonzero pivot. The active lower bandwidth remains 4. After row interchanges, each upper-triangular pivot row reaches at most column k+7, the original upper bandwidth plus the lower bandwidth. Thus pivot search, updates, and back substitution each take constant work per augmented row. The solve uses O(N) field operations and O(N) storage. It divides only by selected nonzero pivots and does not divide by d_i or a leading principal determinant. Invertible zero-diagonal stages are included.

**Precise interpretation:** this computes the action S^(-1)y in linear field work. Materializing all N² inverse entries is not linear-output-size work. The auxiliary representation is division-free, but the field solve itself uses division. No linear bit-complexity bound follows.

Fresh controls include:

- 224 stage determinant comparisons against independent dense elimination in the two source fields, with 154 invertible roundtrips and 70 singular cases;
- 160 separate dense augmented-matrix determinant comparisons;
- 10 invertible fully zero-diagonal controls at N = 2, 8, 64, 256, and 1024, in both fields;
- 192 additional determinant/solve controls in characteristics 2, 3, 5, and 17;
- generic characteristic-zero symbolic determinant identities at N = 1, 2, and 3.

The new banded solver deliberately chooses the last admissible pivot in its four-row window, whereas the uploaded implementation chooses the first. All tested upper-fill bounds remain at most 7. These finite controls corroborate the proof; the universal claim rests on the recurrence and banded-elimination argument.

## 2 Routing and exact middle operator

The convention is (P v)_i = v_(pi(i)), where pi is the permutation reconstructed from `affine_shuffle_columns`. With U[i,j] = zeta_256^(ij)/16,

G = P1 S1 U^(-1) S4 P3,

and for invertible outer stages,

G^(-1) = P3^(-1) S4^(-1) U S1^(-1) P1^(-1).

Both identities are correct with this routing orientation. Fresh dense matrix checks verify both products GG^(-1) and G^(-1)G equal the identity in each field. Twelve fresh vector controls compare two banded solves and direct finite-field Fourier multiplication with the dense inverse operator.

The exact positive roots are 8340 modulo 12289 and 282 modulo 65537. They each have order 256. Multiplication by the inverse of 16 gives the stated normalization, and the independently constructed U and U^(-1) multiply to the identity.

This review uses a dense Fourier oracle for independence. It does not execute or benchmark the uploaded radix-2 NTT. The source's NTT implementation was inspected as text. A conventional NTT inside the middle-operator oracle does not improve FFT arithmetic complexity.

The JSON's `toffoli_gate_sequence_in_shuffle_2` is not applied by the source routing function. This review preserves the same affine-only interpretation as `research_cycle_2245/solver_saturation_review/`. The result must not be relabeled as a certificate for a Toffoli-modified nonlinear routing.

## 3 Complete quadratic coefficient system

Use one shared set of stage generators for every input column. At stage s and basis column j, let x^(s,j) be the input and let L^(s,j),R^(s,j) be the prefix/suffix sums. The first input is the literal basis vector e_j. Fix L_0 and R_(N-1) as literal zero constants. For i = 0,...,N-2 impose

L_(i+1) - L_i - b_i x_i = 0,

R_i - R_(i+1) - e_(i+1) x_(i+1) = 0.

Define the output expression q_i = d_i x_i + a_i L_i + c_i R_i. For s < t impose x^(s+1,j)_i - q_(pi_s(i)) = 0. At the last stage impose U[i,j] - q_i = 0. Separate output y variables are eliminated.

### Equivalence in both directions

Given a factorization U = S_t P_(t-1) S_(t-1) ... S_2 P1 S1, take its actual basis-column intermediate vectors and running sums. They satisfy every equation.

Conversely, the boundary values and recurrences uniquely force L_i = sum_(h<i) b_h x_h and R_i = sum_(h>i) e_h x_h. Therefore q = S_s x at every stage. Coupling equations uniquely force the next stage input to be P_s q. Induction from the fixed e_j input proves that the final column is the actual network product on e_j. Enforcing all j proves all N² coefficients of the claimed operator equality.

This argument has no denominators and loses no zero-generator or zero-diagonal branch. It also shows that, for fixed generators, the auxiliary witness is unique. Equivalently, eliminating the deterministic auxiliary variables yields exactly the full coefficient equations, not a relaxed test.

At N = 256 and t = 4:

- raw generator coordinates: 5tN = 5,120;
- intermediate input coordinates: (t-1)N² = 196,608;
- free running-sum coordinates: 2tN(N-1) = 522,240;
- total unknowns: 723,968;
- stage output/coupling equations: tN² = 262,144;
- running-sum equations: 522,240;
- total equations: 784,384.

Each equation has total degree at most 2 and at most four nonzero monomials. The fresh checker enumerates the actual monomial support of all 784,384 equation instances and assigns all coordinate IDs. There are 16 structurally unused raw generator coordinates: a_0, b_(N-1), c_(N-1), and e_0 for each stage. The source count intentionally retains these; it is not a count of identifiable or gauge-quotiented parameters. Omitting them gives 723,952 used coordinates but does not invalidate the stated raw-coordinate count.

For the complex target the coefficient field is Q(zeta_256), since sqrt(256) = 16. Over any field supporting the stated target, U and the permutations are invertible. A square product equal to U has every stage invertible. Consequently, additional stage-determinant saturation equations are redundant for this complete system. This conclusion does not transfer to the previous selected-minor system or an isolated kernel gate.

### What was independently replayed

All 256 basis columns were propagated from the archived inert generator arrays in each field. Prefix/suffix outputs were compared with independent dense stage multiplication, and every compressed recurrence and coupling/output equation was checked against the synthetic full-product target. This verifies 784,384 equations per field, 1,568,768 in total. Thirty-two interior-state mutations were rejected by the defining recurrence equations.

The synthetic product differs from the positive normalized Fourier matrix in 65,532 entries modulo 12289 and 65,535 entries modulo 65537, exactly reproducing the saved negative-control counts. Thus the positive controls validate the encoding and its evaluation, not a Fourier solution. The checker does not solve the system, compute its dimension, determine its complex zero fiber, or provide a complex feasible witness.

## 4 Exact mask64 kernel incidence model

With the reconstructed P2, let g(i) indicate even parity of i & 64. The source A-side gate uses

I = {i : g(i) is false}, J = {j : g(pi2(j)) is true}.

Both have size 128. The sum of adjacent transitions of g and g composed with pi2 is 16. For B = G[I,J], the inherited necessary gate is rank(B) <= 16. This audit reconstructs these index sets and bound; it does not re-prove every other gate in the historical 64-block family.

Over a field, rank(B) <= b is equivalent to a full-column-rank matrix Z of size 128 by (128-b) with BZ = 0. The forward direction chooses any independent (128-b)-tuple in ker(B). The reverse direction follows from nullity at least 128-b.

Some row subset K of size 128-b has an invertible Z[K,:]. Right-multiply Z by this submatrix's inverse to normalize Z[K,:] = I. This preserves the kernel equation. Hence the rank condition is exactly the union over all such K of these normalized charts. Every chart witness already has independent columns because it contains an identity block. Rank less than b, singular subminors, zero generators, and B = 0 are covered by the union. One preselected chart need not cover all valid B.

For b = 16 there are 112 kernel columns. A fixed K leaves 16 times 112 = 1,792 free Z entries and 128 times 112 = 14,336 equations. These counts exclude the outer generators and treat the 112-square identity block as constants. If both outer stages remain raw variables, include their 2,560 coordinates as well; the fixed-chart total is then 4,352 variables before optional saturation.

The matrix B is bilinear in the entries of S1 and S4. Each off-diagonal entry is itself quadratic in raw separated generators. Thus BZ has total raw-coordinate degree at most 2+2+1 = 5. In outer matrix-entry coordinates plus Z, its degree is at most 3. There is no claim that this gate is sufficient for structured middle stages or for the full factorization.

### Cubic lift and its exact projection

Let E_J be the 256-by-128 coordinate injection. Introduce X of size 256-by-112 and impose

X - S4 P3 E_J Z = 0,

(P1 S1 U^(-1) X)[I,:] = 0.

This explicitly restores the coordinate injection implicit in the source's notation `P3[:,J]`. The first equation has 256 times 112 = 28,672 entries; the second has 14,336 entries. There are 28,672 extra X variables and 43,008 equations total. With raw outer generators and Z entries included, both blocks have degree at most 3. The total fixed-chart variable count including both outer stages is 2,560 + 1,792 + 28,672 = 33,024 before saturation.

Every original chart witness determines exactly one X by the first block. Substituting it into the second returns precisely BZ = 0. Conversely, every lifted solution satisfies that same substitution identity. The lift is therefore equivalent on each chart, with no introduced denominator or lost zero case. The identity rows of Z are again fixed constants and are not extra equations in these counts.

### Fresh positive, negative, and exceptional-chart controls

In each field, an independent dense inverse of the archived synthetic middle product S3 P2 S2 gives a rank-16 block. Fresh row reduction gives a normalized 112-column kernel whose hashes exactly match the archived inert hashes. All 14,336 kernel residuals vanish. The actual Fourier-target outer block has rank 128, so the archived outer point is rejected.

For a positive full cubic-lift control, the synthetic complete stage product replaces the Fourier target. Its corresponding G is exactly the inverse of the synthetic middle product. Both cubic equation blocks were independently evaluated using raw prefix/suffix scans: all 43,008 entries vanish per field. With the real Fourier target restored, the second block has nonzero residuals, as expected.

Additional controls include ranks 0, 1, 15, and 16; a rank-17 rejection by nullity; a mutation of a free kernel entry while preserving the identity pivot rows; and a rank-16 matrix that accepts one normalized chart but makes a different fixed chart impossible. The last test is a concrete reason not to discard chart branches.

**Invertibility qualification:** incidence charts encode exactly rank(B) <= 16, including singular outer stages. Taking a zero outer stage can make B = 0 and satisfy them. They are not a substitute for outer-stage nonvanishing conditions in a standalone admissibility search. Retain the prior reciprocal/determinant-transfer constraints when using the kernel gate alone. The complete all-basis Fourier system forces stage invertibility by a different argument.

## 5 Accepted next step and remaining gates

The complete quadratic model genuinely upgrades the formulation from selected necessary equations to an exact algebraic feasibility problem. It does not make that problem solved or computationally practical merely because the degree is low. The 550 minors remain necessary screens; they are not silently upgraded to completeness by this new result.

A bounded next experiment may use the mask64 incidence chart with both outer stages variable, explicit outer invertibility, and chart switching or branching. A candidate needs exact rank verification, the other relevant rank gates, compatible structured middle stages, and all Fourier coefficient equations. Even an exact N256 solution would not establish an all-length sub-N-log-N algorithm.

Keep the original architecture feasibility, broader asymptotic objective, and external novelty assessment open. Do not infer infeasibility from the saved-point rejection, feasibility over C from finite-field solutions, an FFT speed improvement from the middle oracle, or bit complexity from the linear count of field operations.

## Reproduction and delivery

Run the fresh checker from the workspace root:

`OPENBLAS_NUM_THREADS=1 python research_cycle_2344/n256_full_model_review/fresh_checker.py`

It uses only the pinned local source data and installed packages, and writes audit JSON beside itself. `Incomingqueue_proposal.json` is a proposed research-queue entry; no row was written. `MANIFEST.sha256` hashes the frozen review deliverables and original inputs. Uploaded source code remains inert reference material throughout.
