# Independent review: E25 on the generic fixed-F11 piece

## Verdict and exact scope

**PASS**, conditional on the explicitly accepted historical chart and coordinate ledger identified below.

On the accepted fixed-F11 regular **H != 0, A != 0** piece, the still-retained residual E25 = 0 is equivalent to the stored N2(b,e) = 0 and to the stored core(b,e) = 0. The exact identity is

    N2 = b^10 e^3 H core.

N2 has 370 terms and multidegree (19,39); the core has 340 terms and multidegree (9,33). These equations are **necessary conditions for the complete retained circuit**, not sufficient tests for solutions. All 50 original residuals, all 19 original guards, all accepted additional conditions and all earlier denominator/cancellation exclusions remain mandatory. The A = B = 0 exception is retained unchanged as a separate three-input piece.

No feasibility, infeasibility, dimension, global two-input, novelty, new Fourier factorization, or new linear elimination claim is accepted. Nonaffinity of this particular core does not prove absence of other pivots, linear factors, eliminations, or solutions.

## Reviewed objects and trust boundary

The mathematical object reviewed is research_cycle_2325/f11_generic_residual/CERTIFICATE.json, SHA-256:

    3db49646d9e36a1e979a31dccd49e6f4e5c4dd1484412cb7b602aa1b1511a0d9

Its author seal is pinned at:

    2edc8f9a9c46a54d5d01e6a98c9fce55dbdcceb7b83a0a8113c2732af5354273

The accepted base is research_cycle_2304/regular_hnonzero_analysis/CANDIDATE.json. Its independent acceptance is research_cycle_2310/hnonzero_continuation_review/RECEIPT.json, SHA-256:

    22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e

That accepted receipt supplies the regular chart, the rational-coordinate ledger and protection of its denominators, and the historical projection/reconstruction theorem. These historical theorems are not re-proved here. The present review independently checks the source binding and all new arithmetic, cancellation and predicate-preservation steps. All four direct input hashes and the exact accepted base binding are verified. Every author manifest entry is byte-hashed; author or inherited program source is neither inspected nor executed.

The source polynomial is the final retained E25 in the pinned original guarded-reduction certificate, at content address:

    ce2413e7d1b9e31c5372467e1d12115510d1385a73052fbb0e9c005b1d7ca841

That address is recomputed from the actual coefficient rows. This is the historical retained guarded-reduction polynomial, not a claim to rederive the entire initial Fourier system. It has exactly 55 terms and support {x11,x22,x25,x34,x39,x41,x49,x65,x83,x88}. In particular, E25 contains neither x0 nor x92, so the present substitution makes no representative or gauge assumption about those coordinates.

## Independent exact arithmetic

The new checker uses only Python's standard library. Coefficients in Q[zeta]/Phi11 are represented as ten integer coordinates with one reduced positive denominator. Every distinct nontrivial multiplication is checked by two reductions: ordinary convolution and monic Phi11 long division, and cyclic convolution modulo zeta^11 - 1 followed by elimination of zeta^10. The successful run performs 57,504 distinct cached coefficient products.

The accepted bindings x22 = 1 and x49 = zeta - c are checked against the atlas. The four rational coordinates x25, x39, x65 and x88 are loaded from the exact accepted ledger. The x65 and x88 pairs are also matched directly against their accepted atlas formulas. The original x41 and x83 guard polynomials are checked to be q and e respectively.

For each source coordinate v, the checker derives its maximum exponent m_v from E25 and independently forms the completely uncancelled rational pair:

    D_raw = product d_v^m_v,
    N_raw = sum a_m product n_v^m(v) d_v^(m_v-m(v)).

The independently computed values match the stored raw numerator and denominator. The following identities are checked coefficient by coefficient:

    N_raw = N4 T,
    D_raw = D4 T,
    cd = b H,
    N3 = cd^4 N4(b,cn/cd,q,e),
    N2 = A^2 N3(b,-B/A,e),
    N2 = b^10 e^3 H core.

The exact c-degree of N4 is 4, and the exact q-degree of N3 is 2. The accepted c numerator and denominator are matched directly to the atlas. The accepted A and B depend only on b,e. No gcd, factorization, irreducibility, maximal cancellation or numerical argument is needed.

Polynomial sizes and multidegrees, in the uniform order (b,c,q,e), are:

- N_raw: 391 terms, (7,4,4,5)
- D_raw: 54 terms, (5,2,3,4)
- N4: 118 terms, (5,4,2,3)
- D4: 6 terms, (3,2,1,2)
- T: 12 terms, (2,0,2,2)
- N3: 207 terms, (9,0,2,15)
- N2: 370 terms, (19,0,0,39)
- core: 340 terms, (9,0,0,33)

Both N2 and core have exactly zero c- and q-exponents in every term.

## Denominator proof and guarded equivalence

Every coordinate denominator appearing in D_raw is nonzero on the accepted domain by the pinned accepted ledger. Consequently D_raw is nonzero. Since D_raw = D4 T in a field, D4 and T are nonzero there. Thus replacing the raw pair by N4/D4 preserves E25 without deleting a zero-denominator case.

The c clearing is protected by cd = b H and the already mandatory b != 0 and H != 0 conditions. The q clearing uses A only on the explicit A != 0 piece. Therefore the exact rational identity on that domain is

    E25 = N2 / [A^2 cd^4 D4(b,cn/cd,-B/A,e)].

Every denominator in this identity is nonzero. Moreover b^10 e^3 H is nonzero by the accepted b guard, original x83 guard, and explicit H condition. Hence E25 = 0 iff N2 = 0 iff core = 0 on this domain.

There is no division by the new E41 coefficient B. In particular A != 0, B = 0 reconstructs q = 0 and is rejected by the original q != 0 guard. The A = B = 0 exceptional piece is outside this division and remains present. The names A,B here denote the new E41 coefficients; the older F_A,F_B/E35 coefficients appearing in the accepted chart are distinct.

The generic and exceptional branch records are compared in their entirety with their accepted originals. These comparisons preserve every reconstruction definition, retained residual/guard content address, extra equation/guard, explicit H != 0, d != 0 and F_M != 0 predicate, projection and evaluation order. The other accepted atlas branches are untouched by this bounded calculation.

## Audit and rejection controls

The final fresh run passes 87 positive checks and rejects 38 deliberate corruptions without using a candidate-hash gate for those controls. Rejected mutations include every stored polynomial class, wrong clearing powers, incorrect source selection, q sign change, deleted A/H/b/q/e/D25 guards, deleted E25, dropped inherited definitions, stripped-factor changes, removal or alteration of the A = B = 0 exception, and unsupported feasibility/infeasibility/globality/linear-solve/novelty claims.

The five guards whose polynomial bodies are outside the original source dictionary are preserved by exact comparison with the accepted atlas mappings and the accepted receipt, not represented as newly re-proved polynomial bodies. All 64 available retained residual/guard bodies in that original dictionary have their content addresses independently recomputed.

The author DERIVATION.json and STRIPPED.json are consistent with the authoritative certificate. Author search logs and scripts are byte-bound only; their exploratory assertions are not relied upon. In particular, no unfinished factorization or content search is used as evidence.

## Reproduction and stopping point

Run from the repository root:

    python research_cycle_2333/f11_generic_core_review/check_independent.py

The checker writes ARITHMETIC_RECEIPT.json and NEGATIVE_CONTROLS.json. The review packet also contains the successful check log, the present report, final RECEIPT.json, SHA256SUMS.txt and SEAL.json. Re-running changes runtime information and requires resealing; the frozen digests identify the accepted run.

This review stops at the additional exact necessary equation. Feasibility of the residual system and the retained A = B = 0 exception remain unresolved. No external action or ranking change was performed by this reviewer.
