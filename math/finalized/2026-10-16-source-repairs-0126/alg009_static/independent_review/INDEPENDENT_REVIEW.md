# Independent static review: two historical source repairs

Date: 16 October 2026 UTC.

## Verdict

**ACCEPT both precisely bounded static repairs. Reject any promotion to executed implementation acceptance, complete cost certification, broad theorem closure, or novelty clearance.**

The reviewer independently read the complete current Catalogue, novelty-register and Research-overview owner rows for ALG-009 (74, 35, 52) and ALG-WEIL-LOCAL (28, 53, 70), including their retained history and limitations. The original source files, source explanations, and relevant historical ALG-009 audit were read. Neither original nor patched research code was executed, imported, or compiled for execution. AST parsing, archive inspection and byte hashing were static only. The reviewer executed only the separately self-authored mathematical control program supplied with this report.

## 1. ALG-009: exact at-most-one-pole admission

Original `resultant_gate.py` SHA-256:

`4a1c07d1d6933a399871655eef547451fe8cb24fd026ab70b733b45bda9d8038`

Accepted static candidate SHA-256:

`09ef37694af956394b82f55bf366e121849cbaf7f4d89caff5527aad9a142ef4`

The original file independently matches the archived Hero1 Phase20 and Phase24 members. The archive SHA-256 values are respectively `c20b633a0e8a7be1ee81ab65765a15e3fb77a39d3315c7139cef5d88aa1333c3` and `6d16fea8f12c8f090e20e1b04a85152f9a9a5891f2e424c018a35d55a82f7006`; both archive CRC checks pass. The historical review hash `4e6b45aeab8f22872d9cb6ea37cb74b2c06b55492ac53c8fa1991ac7d60678e9` and subsequent resonance report hash `6b2292a9094f5566d5ffeaaf0f6ad40aa2f701e5fcea2e536cfa7d36bd1bc210` were independently verified.

The candidate is an exact single-block replacement, with every other byte unchanged. It computes `g=gcd(delta,N)` and declines a candidate precisely when `g>1 and alpha^(N/g)=1`.

### Mathematical justification and domain

Under the positive-sign DFT, `S^delta r[j]=r[j-delta]`, so

`F((I-alpha S^delta)r)[k]=(1-alpha*omega^(delta*k))*Fr[k]`.

For omega of exact order N, the homomorphism `k -> omega^(delta*k)` has kernel size g and image all `(N/g)`-th roots. Consequently there are exactly g poles if `alpha^(N/g)=1`, and zero otherwise. The new guard is necessary and sufficient for the stated policy of at most one direct-frequency repair. The old guard safely over-rejected additional noncoprime zero-pole candidates; this is a completeness repair, not discovery of incorrect accepted output.

The implemented recognition theorem still requires N>=8, a prime field p>55 for interpolation, a supplied exact-order N-th root, alpha nonzero, 1<=delta<N, a nonzero degree-at-most-45 resultant, a linear specialized gcd, and the full time-domain defect certificate. The implementation accepts one or two nonzero defects. A zero resultant, non-linear gcd, or unsupported repair is a gate decline, not a proof of nonmembership in every two-defect model.

### Retained safeguards

The N/field entry guard, eight-probe length check, degree/interpolation checks, per-instance trivial-factor divisions, candidate-count bound, nonzero-alpha check, two later Hankel filters, every-coordinate defect scan, and downstream decoder/fallback are byte-for-byte unchanged. Full certification remains essential. The change does not grant a genuine noncoprime multipole case admission.

### Independent controls

The new reviewer checker exhausts 35,904 **nonzero-alpha** predicate triples over GF(17), GF(41), GF(73), GF(97), GF(193), eligible 2<=N<=32, and every 1<=delta<N. There are zero discrepancies between the repaired predicate and an actual pole count greater than one. It reproduces 2,178 false rejections by the old predicate. These are predicate counts, not counts of nondegenerate recognized inputs; the small-field cases test the pole theorem rather than the p>55 implementation.

At N=8 it independently reconstructs the GF73 and GF97 zero-pole witnesses. Direct signed-permutation Sylvester determinants give T(2)=62 and 48 respectively; Sylvester rank five and the known common root establish a linear gcd. Every residual-transform output agrees with direct Fourier evaluation. Independent one-pole and genuine two-pole controls match the stated policy. An N16/GF193 perturbation invisible to the first eight probes has eleven nonzero defect coordinates, confirming why those probes cannot replace full certification.

The GF73 control is residual-gate-only because GF73 lacks the required 16th root for the historical fallback. The GF97 witness is in a compatible-root domain; the reviewer controls here reconstruct its residual transform, not the historical outer engine executable.

### Obligations not discharged

- No original or patched detector, decoder, fallback, hybrid, or regression suite was executed by this review.
- The separate shared-probe hybrid still needs its early N>=8 guard or an explicitly restricted domain; changing `discover_resultant` does not repair it.
- The literal engine requires its additional Green-constructor and backend-root conditions. Invertibility alone is insufficient when the source also inverts every diagonal entry. Supplied N-th roots alone do not establish compatible 2N-th and convolution roots.
- Modular exponentiation, gcd and inherited root-table, negation, fixed-algebra, preparation, failed-candidate and fallback charges remain separate. This patch preserves incomplete `Work` counters and claims no corrected exact grand total.
- Eight-probe sparse-rational uniqueness, raw membership, nondegeneracy, roots, pole repair and historical attribution remain distinct. No new algorithm, general FFT improvement, numerical-stability result or novelty clearance is accepted.

## 2. ALG-WEIL-LOCAL: consistent negative-chirp upper shear

Original v25 archive SHA-256:

`f8fbf4c58e95202665326bc7e66bc2da859502d38225a4d5ce3b42c043a00d15`

Original `local_ring_weil.py` SHA-256:

`dd0047554b2884c8ff1f62bb696c82d512825ac881dfd66d20828b746e5dd9d1`

Accepted static candidate module SHA-256:

`259b8047681ea555152e31c921f13653964cdcb09cc4a9ba9d40f4b2dc56266e`

The original archive CRC, all original extracted bytes, all fourteen original-manifest entries and all sixteen derivative-manifest entries independently verify. The module has exactly four formula changes across `upper_shear_matrix`, `upper_shear_gauss_matrix`, and `predicted_upper_shear`, plus a scope docstring and explanatory comment. No other module behavior changes. All five derivative Python files parse statically.

### Exact convention and proof

Let q=p^k with p odd prime and k>=1, use an exact coefficient field with a primitive q-th root zeta, positive Fourier matrix `F[x,y]=zeta^(xy)`, and `C_b[x,x]=zeta^(b*x^2/2)`. For `W=[[0,-1],[1,0]]`, direct multiplication gives `W^-1 L(-b) W=U(b)`. Thus the consistently labelled operator is

`U(b)=F^-1 C_(-b) F`.

Its kernel is `q^-1 sum_z zeta^(-b*z^2/2+(y-x)z)`.

For nonzero b with b=p^v u, put g=p^v, m=q/g and eta=zeta^g. The kernel vanishes unless x and y share a residue modulo g. On a residue block x=r+gX and y=r+gY, it equals

`[m^-1 sum_z eta^(-u*z^2/2)] * eta^((Y-X)^2/(2u))`.

The scalar is nonzero in the stated field/root domain. The signed four-entry cross ratio at local rows/columns 0,1 is `eta^(-u^-1)`, of exact order m. These signs agree across the patched Fourier conjugation, direct Gauss expression, completed-square expression, documentation, verifier, and added tests. b=0 remains the identity. Negative and noncanonical integer b values are interpreted modulo q.

The old positive-chirp kernel is mathematically valid and represents the opposite shear U(-b). The native owner's explicitly positive kernel formula is not a false support theorem: its valuations, block sizes and order conclusions survive b -> -b. Archival wording must remain distinguishable from the corrected operator label.

### Retained safeguards and independent controls

All ten historical test groups remain present: nine bodies are unchanged, while the cross-ratio-order test is strengthened with a signed-value assertion. Three new groups test negative-chirp separation, every q9 scalar including identity/noncanonical b, and Weyl covariance. These thirteen derivative tests remain **unrun** in this review. Historical results, logs and manifest are preserved verbatim in a separately labelled directory; they are not reused as repaired-source execution evidence.

The reviewer independently checks all 125 scalar values b over q=3,5,7,9,25,27,49. The fresh controls cover 154,181 kernel entries by their exact circulant identity, 462,543 entrywise Weyl-covariance comparisons, the signed cross ratio, the completed-square formula, every identity case, and a distinct wrong-positive-chirp control for every nonzero b. Twenty-one independent integer 2x2 group-relation cases pass. These controls import no original or candidate module and are not a cold replay of the source.

The original subgroup, double-coset-refinement, valuation-count, operation-ledger and predecessor-hash tests are retained. Their retention is static evidence only. In particular the derivative still does not identify valuation with all lower-parabolic double cosets, does not extend to p=2, and does not license arbitrary digit routing in the restricted ring-Weil factor grammar.

### Obligations not discharged

- Original and corrected exhaustive SL2/subgroup suites and full source drivers remain unexecuted by this review.
- Supplied p,k,q, coefficient-field and primitive-root consistency are domain assumptions; the existing helper functions are not accepted as validators of arbitrary malformed inputs.
- Global representation normalization, higher-dimensional general symmetric congruence diagonalization, numerical production, preparation/bit costs and practical speed remain separate.
- The selected radix schedule plus O(q) monomial work is an upper implementation schedule, not an arbitrary-evaluator lower bound.
- The later accepted bounded-API archive/review hashes `a206af8dc4aa68faf2ebdb6406c0be854b4ca692ac5805b8bdd0ccc3705f4f52`, `ae5450d760e1b2922efe2d840b97dd3c0728e0db85a5e6f1d8c1594e505c5f6a`, and `51f2ae033138859f5d7c30b3692e7c29d664dfdf5028b0ebe66226fa14fe59ae` are recorded but unrecovered in the available evidence registers. This review does not claim to reread or replay those bodies. The present repair is independently justified against the available original v25 source.
- Historical novelty and stronger FFT conclusions remain unestablished.

## 3. Safe disposition

The static source-repair sub-obligations may be recorded as independently accepted for the exact hashes above. Do not mark either whole canonical research record closed, alter priority or discovery counts, convert previous historical runs into fresh evidence, or merge these two lineages with unrelated later bypass/detector fixes.

The accompanying mathematical checker, its results, the two static review JSON records and this report are publication-safe research artifacts. Raw live native-row snapshots are excluded from the publication folder. No external write, upload, installation or third-party communication was performed by this reviewer.
