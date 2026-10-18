# N13: sixteen original physical banks over F_(53^19)

18 October 2026 UTC. Candidate attainment theorem; external independent review pending. The explicit construction has passed two algorithmically different literal implementations. This advances the accepted degree-seventeen construction to a new field; no historical novelty claim is made.

## 1. Exact result and scope

Fix the transform length N=13, q=16 in characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). The extension degree in this report is nineteen; the transform length remains thirteen. Let B(K) denote the minimum number of physical banks in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation. Arbitrary legal beta and raw weights are allowed. The supplied certificate, together with the accepted field-uniform lower theorem, gives

    B(F_(53^19))=16.

The allocation is (7,1,1,7). The witness uses beta=1, seven common same-sign nodes, and equal but genuinely nonbase cross nodes. Each same-sign support is non-Frobenius-stable. Independent freedom of the two cross nodes permits their equality in this witness; equality is not imposed on the theorem's grammar. A narrower constructive subfamily suffices to prove the upper bound.

The lower theorem is inherited from accepted byte-bound source reports. This work does not recompute the large lower-minor certificate, classify other cross allocations, or change the original physical primitives.

## 2. Field and exact inert data

Use K=F53[u]/(u^19+u+12). Coordinates [a0,...,a18] denote sum ai*u^i. The field order is

    53^19=577087307374494432392299037533517,

which occupies 109 bits. C++ uses unsigned 128-bit exponents for powering, inverse, splitting and factorization; 53^19 is strictly below 2^128; the field order is computed exactly at compile time. Its multiplication implements u^19=-u-12. A convolution coefficient is at most 19*52^2=51,376; the sparse one-step reduction keeps every signed coefficient within the conservative bound 14*51,376=719,264, so 32-bit signed coefficient arithmetic cannot overflow. Since 53^19 is 5 modulo 8 and 23^2=-1 modulo 53, the quadratic-gate square-root routine uses the exact 5-modulo-8 formula and explicitly squares each proposed root before accepting it. The Python checker independently implements generic monic polynomial reduction.

A deterministic modulus search tests u^19+u+c in the order c=1,...,52 and stops at c=12, the first irreducible polynomial. FIELD_SEARCH.json records all twelve exact tests and search_field.py replays them. Before any extension-field inverse, prime-polynomial modular arithmetic establishes

    X^(53^19)=X mod (X^19+X+12),
    gcd(X^19+X+12, X^53-X)=1.

Since 19 is prime, the first identity restricts factor degrees to 1 or 19 and proves squarefreeness. The gcd excludes degree 1, proving irreducibility. FIELD_IRREDUCIBILITY.json retains all nineteen Frobenius remainders. field_verify.py performs this proof without any extension-field inverse or historical import; the full standalone literal checker repeats it. The original q=16 is checked to have exact order thirteen.

The cross nodes are

    y=z=[5,43,6,27,29,18,9,18,46,44,44,36,35,21,41,35,28,46,17].

DEGREE19_LITERAL_CERTIFICATE.json supplies all seven actual same-sign nodes and the full monic degree-seven annihilator H, all sixteen physical-bank records, 208 normalized amplitudes, 208 raw branch weights, 16 guards, and all 169 matrix entries. Each coordinate is explicitly stored, never represented by a formal root placeholder. The JSON verifier checks canonical lengths and residues, distinct nonzero roots, their seven-factor product H, nonbase cross nodes, nonbase coefficients of H, and non-Frobenius-stability of the actual seven-root set.

## 3. Original physical grammar

For indices modulo thirteen, define S e_t=e_(t+1) and T e_t=16^t e_t. Every supplied bank is exactly

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1).

The general legal guard is 1-alpha^13-beta^13; here beta=1, so it equals -alpha^13. All sixteen guards are recomputed and are nonzero. Every physical-bank matrix is itself nonzero. No trace, quotient-algebra bank, derivative, singular limit, pre/post map, or uncharged transform substitutes for an original primitive.

## 4. Discovery and literal proof

The deterministic search retains the accepted symmetric subfamily y=z, equal same-sign supports and beta=1. The six forced windows produce a monic degree-seven affine recurrence line. Its b=3 compatibility gate is solved over the new field. These are necessary candidate gates only; neither passing the gate nor obtaining a split H is treated as a physical witness. The inherited rank/chart result shows the chart has no exceptional nodes in extension degree nineteen, since 37 does not divide 19.

The seed is 202610181330. The first split candidate occurs at zero-based trial 3411, after 3405 nonzero-constant recurrence candidates. The declared search cap is 100000, but execution stops at that first split candidate. SEARCH_SCOPE.json and FAILED_PREFIX.log bind the exact finite scope. This failed prefix is not a field-wide exclusion or a stable-support census.

The reconstruction factors H into seven actual field roots and solves all thirteen rows of each of the thirteen full sixteen-column sector systems. All 169 sector equalities pass. Their ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For the normalized target f(a,b)=16^(10(a+b)^2) and gamma=7, the raw weights are

    w_j=Delta*7*sum_(b=0)^12 A_b*16^(-epsilon*b*j).

Both implementations invert the transform and recover every supplied amplitude. The stronger literal verification proceeds as follows:

1. For every physical bank and every j, form the actual sparse 13-by-13 matrix M, with M[t,t]=1-16^(epsilon*delta*j+delta*t) and M[t+epsilon,t]=-alpha.
2. The C++ implementation uses Gauss-Jordan elimination for every inverse, then checks both matrix products with M entry by entry.
3. The Python implementation consumes only inert JSON, never importing the discovery or C++ code. Its separate field arithmetic and unique zero-diagonal backward recurrence construct each inverse. It separately checks both literal sparse matrix products.
4. Each implementation scales the branch by its supplied raw weight and the original factor 1/13, sums all sixteen banks, and compares every entry with 16^(-kt).

Each run establishes 208 legal branch inverses, 416 left/right inverse identities and 70,304 corresponding scalar equalities. All 208 raw-weight/amplitude checks and all 169 target-entry checks pass, with zero target mismatches and sixteen nonzero bank matrices. Thus the raw operator identity holds on every vector over the field, rather than merely on sample inputs.

Falsification controls yield 169 mismatches when 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after adding one to the last raw weight. These supplement the exact positive identities. Algorithmically distinct same-author checks are not external reviewer acceptance.

## 5. Matching lower bound and scalar extension

The accepted lower review, retained as sources/ACCEPTED_LOWER_REVIEW.md, explicitly states a field-uniform lower theorem over every characteristic-53 field for arbitrary legal beta. In this free-cross-singleton grammar, each same-sign orientation needs at least seven distinct nonzero effective alpha nodes and each cross orientation needs a nonzero node. Repeated, ineffective or cancellation-only physical banks do not weaken its count. This gives B(K)>=7+1+1+7=16. The accepted degree-eleven, degree-thirteen, and degree-seventeen reviews separately preserve that universal scope. Their exact source bytes are pinned here; the lower-minor computation is inherited, not rerun.

The explicit witness proves the matching upper bound over F_(53^19). When 19 divides d, a finite-field embedding F_(53^19) into F_(53^d) preserves nodes, raw weights, nonzero guards and the original operator identity. Hence

    19 divides d  =>  B(F_(53^d))=16.

Together with already accepted attaining degrees 2,3,5,7,11,13,17, the sufficient divisor list becomes {2,3,5,7,11,13,17,19}. Its product is 9699690. Apart from the already solved base field d=1, the still-unclassified degrees are d>1 with gcd(d,9699690)=1; the smallest is twenty-three. This is a sufficient classification boundary, not an iff or a nonexistence result at a remaining degree.

The older prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. This degree-nineteen witness has two nonbase cross nodes and two nonstable seven-node supports, so it does not contradict either obstruction. It does not strengthen those restricted obstruction hypotheses or prove that both cross nodes must be nonbase in every possible witness.

## 6. Reproducibility, cost and limits

Run python -I independent_literal_check.py to verify the certificate using only the Python standard library. Run python -I cold_replay.py for isolated verification, fresh C++ reconstruction, byte-identical reconstructed certificate, repeated standalone checking, exact failed-prefix replay and exact deterministic first-candidate replay. COLD_REPLAY.json records success; COLD_RUN.log retains the run output. Build sources use GNU C++17; no external package is needed for verification.

SOURCE_PINS.json records exact source paths, lengths, SHA256 and Git blob hashes. Source files are byte-bound local snapshots; this worker performed no new remote source read. MANIFEST.json binds the final deliverable files. source_rebuild_check.py verifies all nineteen source pins, reproduces the four adapted source files byte for byte in a disposable folder, repeats the modulus search, binds the header to discovery JSON and the certificate, and independently replays all 64,828 PRNG coordinate draws through the hit with zero all-zero nodes skipped. Compiler binaries and Python cache files are disposable and are not part of the sealed scientific source artifact.

OPERATION_LEDGER.md charges support discovery, field arithmetic, factorization, actual-root sector solving, raw-weight construction and original branch inverses. A schoolbook degree-nineteen multiplication has 361 coefficient products before reduction; sixteen banks are not sixteen scalar operations. No general faster FFT, practical runtime improvement, historical novelty, broad parent closure, complete field classification, or other cross-allocation result is claimed. No GitHub, Sheets, publication or other external write was performed.

## 7. Proven structural extension and remaining prerequisite

Applying any of the nineteen F53-automorphisms of F_(53^19) to every parameter and raw weight gives another legal original network for the same prime-field Fourier target. The cross node has nonconstant coordinates and nineteen is prime, so it has exact degree nineteen over F53 and its Frobenius orbit has length nineteen. The resulting nineteen conjugate networks are distinct at that cross node. The same argument and the explicit nonconstant coordinates show each of the seven stored support nodes has degree nineteen. None of these particular parameter lists descends to the base field; this is not a nonexistence theorem for a different base-field network.

The genuinely field-wide consequence proved here is scalar-extension transfer to every degree divisible by nineteen. A theorem for all sufficiently large degrees would require additional algebraic work, for example establishing an appropriate geometrically irreducible component of the complete split-support and full-sector incidence variety together with an effective point-count bound. Neither the necessary recurrence gate nor finitely many prime-degree witnesses establish those premises. No cofinite existence, generic gate sufficiency, monodromy, or full classification theorem is claimed here.
