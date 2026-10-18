# N13: sixteen original physical banks over F_(53^23)

18 October 2026 UTC. Candidate attainment theorem, with two algorithmically different literal checks and a separate exact-arithmetic preflight. External independent review is pending. This advances the accepted degree-nineteen construction to a new field; no historical novelty claim is made.

## 1. Exact theorem and scope

Keep N=13, q=16 in characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). The extension degree is twenty-three; the transform length remains thirteen. Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation. Arbitrary legal beta and raw weights are allowed. The explicit certificate and the accepted field-uniform lower theorem give

    B(F_(53^23)) = 16.

The attained allocation is (7,1,1,7). The witness uses beta=1, seven common same-sign nodes, and equal nonbase cross nodes. The two same-sign supports are non-Frobenius-stable. Independent freedom of the cross nodes allows equality in this witness; equality is not imposed on the theorem's grammar. This constructive subfamily suffices for the upper bound.

The lower theorem is inherited from the accepted source-bound reviews. This work does not rerun its large lower-minor computation, classify other cross allocations, or alter any original physical primitive.

## 2. Field and the 128-bit boundary

Use K=F53[u]/(u^23+u+5). Coordinates [a0,...,a22] denote sum ai*u^i. The exact field order is

    Q = 53^23 = 4553496434179608203397220101976502751677,
    bit_length(Q) = 132.

The old unsigned-128 representation is insufficient. Every active C++ field-order or extension-field exponent is now an unbounded GMP mpz_class. This includes ORDER, field powering, inversion, polynomial powering, the Frobenius splitting test, the quadratic-gate square-root exponent, and recursive root-factorization exponents. No narrowing conversion is used in those paths. uint64_t remains solely for the explicitly wrapping xorshift PRNG and bounded search counters. Tiny prime-field powers use ordinary int with exponents bounded by the fixed N=13 formulas.

The exact large exponents are

    Q-2       = 4553496434179608203397220101976502751675,
    (Q+3)/8   = 569187054272451025424652512747062843960,
    (Q-1)/2   = 2276748217089804101698610050988251375838.

All three exceed 2^128-1. Merely widening the order while retaining a narrow square-root or factor exponent would still be wrong.

Before any support search, arithmetic_probe.cpp was compiled and its inert JSON output was checked by check_arithmetic.py. The latter has its own generic prime-polynomial long division and Python unbounded integers; it imports neither discovery nor either literal verifier. ARITHMETIC_CHECK.json records exact agreement at ten exponents, including 2^127-1, 2^127, 2^128-1, 2^128, 2^128+1, Q-2, Q-1, Q, (Q+3)/8, and (Q-1)/2. It also checks field multiplication and inversion, splitting of a constructed polynomial with seven distinct known roots, and valid quadratic-character values in the factor splitter.

Six negative controls detect a wrapped field order, the 2^128-to-zero exponent boundary, a truncated inverse exponent, a truncated splitting order, a truncated square-root exponent, and a truncated factor exponent. The false inverse fails a*inverse=1; the false square root fails squaring; the false split remainder is not X; and the false factor-character values are not all +/-1. COLD_REPLAY.json repeats this preflight before either failed-prefix or successful support search replay. These tests guard the concrete implementation boundary; the exact field and original-operator identities below supply the mathematical witness.

Field multiplication implements u^23=-u-5. An unreduced convolution coefficient is at most 23*52^2=62,192. Each low coefficient receives at most its original term, one coefficient times 5, and one coefficient times 1. No reduced term feeds back into degree >=23. Thus the conservative signed bound is 7*62,192=435,344, safely within 32-bit int. The full C++ literal reconstruction also passes undefined-behavior sanitization.

Q is 5 modulo 8 and 23^2=-1 modulo 53. The quadratic-gate routine uses the exact 5-modulo-8 square-root formula and explicitly squares each proposed root before accepting it.

## 3. Irreducibility, original grammar, and inert witness

search_field.py tests u^23+u+c for c=1,...,52 and stops at c=5, the first irreducible polynomial. FIELD_SEARCH.json records all five tests. Before any extension-field inversion, field_verify.py establishes by prime-polynomial arithmetic

    X^(53^23) = X mod (X^23+X+5),
    gcd(X^23+X+5, X^53-X) = 1.

The degree 23 is prime. Divisibility by X^(53^23)-X restricts irreducible factor degrees to 1 or 23 and guarantees squarefreeness; the gcd removes degree 1. This proves irreducibility. FIELD_IRREDUCIBILITY.json records all twenty-three Frobenius remainders. The standalone literal checker repeats the proof without importing a historical scientific program and confirms that q=16 has exact order thirteen.

The two cross nodes are

    y=z=[6,0,8,51,7,14,3,30,31,19,32,34,0,18,49,28,35,37,40,40,2,44,22].

DEGREE23_LITERAL_CERTIFICATE.json supplies all seven actual support nodes, the full monic degree-seven annihilator H, sixteen physical-bank records, 208 normalized amplitudes, 208 raw branch weights, all guards, and all 169 resulting matrix entries. Every element is an explicit canonical coefficient vector. There are no formal root placeholders.

For indices modulo thirteen, define S e_t=e_(t+1) and T e_t=16^t e_t. Every certificate bank is literally

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1).

The legal general guard is 1-alpha^13-beta^13. Here beta=1, so the guard is -alpha^13. All sixteen guards are recomputed and nonzero, and all sixteen bank matrices are nonzero. No trace, quotient-algebra bank, derivative, singular limit, pre/post map, or uncharged transform replaces an original primitive.

## 4. Discovery is separated from proof

The search retains the accepted symmetric subfamily y=z, equal same-sign supports, and beta=1. Six forced recurrence windows define a monic degree-seven affine line. The b=3 compatibility gate is solved over the exact new field. These are necessary discovery gates, not a sufficiency theorem. A split candidate is accepted only after every full sector and literal original matrix identity passes. The inherited rank/chart theorem applies because 37 does not divide 23.

The deterministic xorshift seed is 202610181502. The first split candidate is at zero-based trial 675, after 676 nonzero-constant recurrence candidates. The initial cap was 100000; execution stopped on the first split candidate. Exact failed-prefix and first-hit replays are recorded separately. SEARCH_SCOPE.json describes the finite discovery scope. A failed finite prefix is not field-wide nonexistence, a census of stable supports, or a statement about other nodes or allocations.

The C++ verifier factors H into seven distinct nonzero actual field roots, verifies their product, and solves all thirteen equations in each full sixteen-column sector system. All 169 sector equalities pass. The ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For normalized target f(a,b)=16^(10(a+b)^2) and gamma=7, each raw weight is

    w_j = Delta*7*sum_(b=0)^12 A_b*16^(-epsilon*b*j).

Both implementations invert that transform and recover every normalized amplitude. They then verify the stronger original operator identity:

1. For each of the sixteen banks and each j, construct the actual 13-by-13 matrix M, with M[t,t]=1-16^(epsilon*delta*j+delta*t) and M[t+epsilon,t]=-alpha.
2. The C++ implementation constructs every inverse by Gauss-Jordan elimination and checks both dense matrix products entrywise.
3. The separate Python implementation consumes only inert JSON. It uses generic polynomial field reduction and the unique zero-diagonal backward recurrence to construct each inverse, then checks both sparse matrix products. It does not import the C++ or discovery implementation.
4. Each implementation scales the supplied inverse by the supplied raw branch weight and the original 1/13, adds all sixteen banks, and compares all entries with 16^(-kt).

Each establishes 208 legal branch inverses, 416 left/right inverse identities comprising 70,304 scalar equalities, 208 raw-weight/amplitude equalities, and 169 Fourier target equalities with zero mismatches. This is an exact operator identity on every input vector over K, not a test on a finite set of sample inputs.

The falsification controls give 169 mismatches if 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after adding one to the final raw weight. The final cold rebuild additionally uses -fsanitize=undefined -fno-sanitize-recover=all. Distinct same-author implementations and sanitizer checks are not external reviewer acceptance.

## 5. Matching lower bound and rigorous transfer

The accepted lower review states the field-uniform lower theorem for every characteristic-53 field and arbitrary legal beta: each same-sign orientation needs at least seven distinct nonzero effective alpha nodes, and each cross orientation needs a nonzero effective node. Repeated, ineffective, or cancellation-only banks do not lower this count. In this grammar B(K)>=7+1+1+7=16. The inherited degree-eleven, degree-thirteen, degree-seventeen, and accepted degree-nineteen reviews retain the same scope. Their exact local source bytes are pinned here. No lower-minor computation is claimed anew.

The explicit certificate gives the matching upper bound in F_(53^23). Whenever 23 divides d, the finite-field embedding F_(53^23) into F_(53^d) preserves all nodes, raw weights, nonzero guards, and the literal bank identity. Therefore

    23 divides d  =>  B(F_(53^d))=16.

Together with the previously accepted attaining degrees, the sufficient divisor list is now

    {2,3,5,7,11,13,17,19,23}, with product 223092870.

Apart from the separately solved base-field case d=1, the remaining unclassified degrees are d>1 with gcd(d,223092870)=1; the smallest is 29. This is a sufficient coverage boundary, not an iff classification or an exclusion at degree 29.

Applying any of the twenty-three F53 automorphisms to all coefficients gives another original network for the same prime-field target. Every stored support node and the common cross node has nonconstant coordinates; since 23 is prime, each has exact extension degree 23. Thus the cross-node orbit distinguishes twenty-three conjugate parameter lists. These lists do not descend to F53; this says nothing about whether a different base-field parameter list could exist.

The previously proved prime-field-cross and Frobenius-stable-support restrictions keep their original gcd(d,210)=1 hypotheses. This construction has two nonbase cross nodes and nonstable supports, so it contradicts neither restriction. It does not prove both cross nodes must be nonbase in all possible witnesses.

## 6. Reproducibility, costs, and exclusions

A standalone certificate check requires only the Python standard library:

    python -I independent_literal_check.py

To replay source adaptation and bindings:

    python -I source_rebuild_check.py

To rebuild the arithmetic preflight, reconstruct and independently check the certificate, run undefined-behavior sanitization, and replay the exact failed prefix and first hit in a disposable directory:

    python -I cold_replay.py

The C++ commands require GNU C++17 and GMP development headers/libraries (the tested GMP version is 6.3.0), linked with -lgmpxx -lgmp. No new software installation occurred. The JSON-only literal checker remains free of nonstandard packages.

SOURCE_PINS.json binds sixteen inherited source files by byte length, SHA256, and Git blob SHA. source_rebuild_check.py reproduces five active sources byte-for-byte, replays the modulus search, binds the candidate/header/certificate, audits the large-exponent call paths, and independently replays all 15,548 PRNG coefficient draws through the first hit with no zero node skipped. COLD_REPLAY.json records byte-identical arithmetic receipts, certificate reconstruction, and discovered candidate. MANIFEST.json binds the final source and evidence files; disposable compiler binaries are excluded.

OPERATION_LEDGER.md charges field arithmetic, modulus selection, support search, factorization, full-sector solves, weight construction, and actual branch inversion. A schoolbook degree-23 multiplication has 529 coefficient products before reduction. Sixteen banks are not sixteen scalar operations. No general faster FFT, practical runtime advantage, historical novelty, other-allocation theorem, or full field classification is claimed. This worker performed no GitHub, Sheets, publication, or other external write.

No finite list of prime-degree witnesses proves cofinite or generic existence. Such a theorem would require additional algebraic results, for example a suitable geometrically irreducible component of the complete split-support/full-sector incidence variety and an effective point-count bound. Neither the recurrence gate nor this exact certificate establishes those prerequisites.
