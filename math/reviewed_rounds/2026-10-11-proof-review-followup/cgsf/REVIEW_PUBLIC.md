# Independent review: CGSF full-shift commutant obstruction

Repository privacy copy. The private conversation permalink and message metadata
are omitted. Mathematical content and source SHA-256 bindings are retained.
This file is a derivative; the original sealed review SHA-256 is
`f93afd6c3eb4fddf9885b959de0b5d5c84a204cf5871be57e2f024b5fa3bccbb`.

Date: 2026-10-11 UTC.

## Decision

**ACCEPT the exact narrow obstruction in the bound reconciliation report.** The proposal's matrix-algebra model needs repair. This is an acceptance of a model-specific algebraic correction, not a Fourier complexity lower bound, a rejection of every macro compiler, or a novelty claim.

The accepted statement is:

> Let X be the full Hamiltonian cyclic shift on K^N, let char(K) not divide N, and let R_s = M_s X M_s^(-1) with M_s invertible. Then C(R_s) = K[R_s] is commutative of dimension N. If R_s is a weighted permutation with b cycles of common length L = N/b and nonzero holonomies eta_1,...,eta_b, their polynomials t^L - eta_j are pairwise coprime. In the coordinate decomposition into these cycles, every off-cycle commuting block is zero, and C(R_s) is the product of the b algebras K[t]/(t^L - eta_j). For b > 1 it is not M_b(K[t]/(t^L - eta)).

Accordingly, the full-operator commutant does not provide the asserted free mixing across the source's distinct cycles. It does retain within-cycle polynomial gauges and valid invertible gauge cancellation. Other operators, multiplicity spaces, powers, or algorithmic mechanisms must be analyzed separately.

## Exact source and version binding

Reviewed input report:

- Path: `network_leads_reconciliation_1925/REPORT.md`
- SHA-256: `1627737b09b8bcdd3fa77f9cc9c47382590dfab3f09808ec63e5ee168bbf864c`
- This equals the parent-specified digest and its companion receipt's digest.

Reviewed source snapshot:

- Path: `network_leads_reconciliation_1925/CGSF_READABLE_SOURCE.json`
- SHA-256: `f58db5c930307a4a3bb760dfbfb3250bb2904d37df7c58401297dc4ad5c50b5e`
- Snapshot contains the entire 7,529-character text; `content_omitted=false`.

This review is bound to the locally supplied exact-message snapshot. It does not claim a fresh remote fetch or access to the source's linked sandbox theory, verifier, or ZIP. The snapshot is an assistant-authored research proposal, not independently verified authority for its other research assertions.

All hashes asserted by the input receipt were checked against local bytes. This review does not promote or re-review the unrelated leads, finite-network certificates, comparator claims, or archival assertions in the larger report.

## Source-context check: full operator versus multiplicity

The source first explicitly identifies X as one Hamiltonian cyclic shift. After bit reversal and s butterfly levels it defines R_s = M_s X M_s^(-1). The proposed commutant C(R_s) is subsequently used both for exact local intertwining and for cancellation C_s C_s^(-1).

Later, the same proposal describes mixing across equal-length weighted cycles and displays M_b(K[z]/(z^L-eta)). Its proposed N=64 experiment calls for both low-degree cycle polynomials and cross-cycle mixers. There is no intervening restriction to a repeated-spectrum operator, a tensor multiplicity space, or a power of R_s that would justify replacing the full operator by one with repeated cycle modules.

Equal length alone is insufficient. Holonomy determines the polynomial of a weighted cycle. The full similarity forces the holonomies to yield coprime polynomials, and thus rules out the off-cycle blocks claimed at this precise step. This is not a criticism of the true local identity A R = R' A or of cancellation by invertible, genuinely commuting gauges.

## Proof review

### 1. Full cyclic shift centralizer

The vectors e_0, X e_0,...,X^(N-1)e_0 form a basis. A matrix C commuting with X is determined by C e_0, because C X^k e_0 = X^k C e_0. There is a unique polynomial p of degree less than N with p(X)e_0 = C e_0. Therefore C = p(X).

It follows that C(X) = K[X], with dimension N. Similarity gives C(R_s) = M_s C(X) M_s^(-1) = K[R_s]. In particular, this algebra is commutative. This centralizer conclusion actually uses cyclicity alone and holds in every characteristic; the stated characteristic assumption is sufficient for the following simple-spectrum argument.

The characteristic and minimal polynomials of X are both t^N - 1. When char(K) does not divide N, this polynomial is squarefree. Hence R_s has N distinct eigenvalues over a splitting field. If K contains a primitive N-th root, as in the Fourier setting, the centralizer is also isomorphic to K^N in an eigenbasis.

### 2. Weighted-cycle decomposition

A length-L cycle with nonzero weights is cyclic: one coordinate vector and its first L-1 iterates form a basis. Its characteristic and minimal polynomial are f_j(t) = t^L - eta_j, where eta_j is the product of its edge weights.

The characteristic polynomial of the direct sum is the product of these f_j. Since it equals the squarefree polynomial t^N - 1, the f_j are pairwise coprime. For equal L, this also says the eta_j are distinct.

Let D be a block intertwining cycles i and j, so R_i D = D R_j. Then 0 = f_i(R_i)D = D f_i(R_j). If i differs from j, Bezout supplies u f_i + v f_j = 1; evaluating at R_j shows f_i(R_j) invertible. Thus D = 0.

Each diagonal block centralizer is K[R_j], of dimension L. Consequently the full centralizer is the finite product of these cycle algebras, of dimension b L = N. Using “direct sum” for this finite product in the input report is harmless.

### 3. Where the matrix algebra is valid

For b copies of the *same* length-L cycle module, the commuting block in every position can be an element of K[t]/(t^L - eta), giving M_b(K[t]/(t^L - eta)) with dimension b^2 L = bN. Weighted cycles with the same holonomy are diagonally similar, so the statement also covers their differently weighted presentations.

For b > 1, the characteristic polynomial is then (t^L - eta)^b and has repeated roots under the stated assumptions. Such an operator cannot be similar to the full shift. This positive case must therefore be distinguished from the actual stage operator.

### 4. Restriction and operator-change boundary

An invariant restriction of a simple-spectrum operator still has simple spectrum; restriction alone cannot produce repeated copies of an eigenvalue. A different operator, such as R_s^N = I, can have a much larger centralizer. Commutation with that changed operator does not imply commutation with R_s. Any multiplicity-based repair must explicitly define its new operator and verify that its proposed gauges retain the required full local transport.

## Independent fresh controls

Fresh code: `independent_controls.py`. Output: `INDEPENDENT_CONTROLS.json`.

The earlier control source was inspected but was not run or imported. The new construction does not assemble butterfly stages. It forms each partial transform directly as block-diagonal copies of F_(2^s) P_(2^s), followed by the global bit reversal P_N. It then computes R_s by exact finite-field similarity. To measure commutants it constructs the linear map C -> A C - C B by applying it to every matrix unit, rather than copying the earlier indexed coefficient formula. A separate rank check verifies independence of I,R_s,...,R_s^(N-1).

Exact runs: N=4 and N=8 over F_17, plus N=8 over F_97. Every run passed:

- Each M_s is invertible; full similarity and adjacent local transport hold.
- There are 2^s cycles of length N/2^s.
- The holonomies are distinct and their cycle-polynomial product is exactly t^N-1.
- Each pair of distinct cycles has an explicit constant-coefficient Bezout identity.
- Every off-cycle intertwiner space has dimension zero; each diagonal cycle space has dimension L.
- Every full centralizer has dimension N, matching the independently calculated rank of the polynomial span.
- The final transform is the complete positive-sign DFT, the final operator is diagonal with the N distinct roots, and the seed is all ones.
- Replacing all cycle holonomies by 1 produces centralizer dimensions bN and nonzero pair-intertwiner dimensions L, confirming that the method detects real repeated-module mixing.
- The changed operator R_s^N = I has dimension N^2, while a half-spectrum invariant restriction of the final operator has dimension N/2.

Dimension summary:

- N4, F17: actual stage dimensions 4,4,4; repeated-holonomy controls 4,8,16.
- N8, F17: actual stage dimensions 8,8,8,8; repeated-holonomy controls 8,16,32,64.
- N8, F97: actual stage dimensions 8,8,8,8; repeated-holonomy controls 8,16,32,64.

These bounded controls independently corroborate the proof and its scope. They do not verify the source's claimed tests through N256, any macro execution costs, or a uniform speedup.

## Required use in consolidation

Record this as **ACCEPT: full-shift commutant-model obstruction**. Preserve the full-operator, invertibility, field, cycle-length, and holonomy assumptions. Repair the CGSF optimization variables by removing the asserted off-cycle commutant mixing for these R_s. Retain the valid fission identities and invertible within-cycle gauges as available structures.

Do not infer an Omega(N log N) lower bound, failure of all commutant-gauged macro compression, failure of a two-level finite fusion, or a new FFT algorithm. Preparation, application, and legal-gauge costs remain unresolved.

No Sheet/GitHub writes, uploaded research-code execution, remote mutation, novelty claim, or new macro search was performed.
