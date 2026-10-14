# Independent review: twelve original signed banks over F23^5

13 October 2026. **Verdict: ACCEPT, confined to the explicit fixed-N, fixed-q witness.**

The negative Fourier matrix F[k,t] = 13^(-kt), 0 <= k,t <= 10, equals the sum of the twelve supplied original legal banks over L = F23[z]/(z^5+8z^4+z^3+18z^2+4z+6). The orientation counts (++,-+,+-,--) are exactly (5,1,1,5), both cross-sign singleton alphas are 4, every beta is 1, and every bank matrix is nonzero. No mathematical repair is required for this finite witness.

This acceptance is an upper bound of twelve, not an optimality theorem. It does not accept the broader nine-case classification described in the candidate CONTRACT.md. In particular, the other seven squarefree cases and repeated-root exclusion are outside this review. No all-N, characteristic-zero, arbitrary-singleton, runtime, or historical-novelty claim is accepted.

## 1. Bound source and independent method

The reviewed candidate archive is Signed_Bank_Twelve_Extension_Field_Candidate_2026-10-13.zip, SHA-256 aca8229b5b48c6829b6b41005220b2e25aef03685243413602d1875b92feb431, 35,025 bytes. Exact bytes are included as CANDIDATE_SOURCE.zip. Every one of its nine manifested members passes both its length and SHA-256 checks.

The original grammar is independently anchored to section 3 of the previously accepted review, copied unchanged as PRIOR_ACCEPTED_GRAMMAR.md. SOURCE_VERIFICATION.json binds that copy to the accepted archive c9f6eaacdca9b7e5549cab902fc695a7e054a7ca04aa9234ddf10efe22877586 and review SHA-256 d6e63accc05574dfa654e174acd37f8a0a947bd0e98152f6493bbe9f09b7708b.

Only the newly written independent_check.py performs the mathematical calculations in this review. No candidate or historical scientific program was executed, imported, compiled, or copied as implementation. Exact witness parameters and raw weights were read as data. The checker uses its own polynomial arithmetic and degree-five field operations, constructs each original 11-by-11 branch matrix directly, computes each inverse by fresh elimination, and tests both multiplication orders. Coefficient recurrences are not used to produce these inverses. After the decisive literal check, independently generated left-multiplication coefficients check the supplied construction data.

## 2. Minimal reproducible certificate

The self-contained certificate consists of independent_check.py and MINIMAL_WITNESS.json. The latter stores only p,N,q, the modulus, and each bank's signs, alpha, beta, and eleven raw weights. It contains no claimed inverse, bank matrix, target sum, row rank, or pass/fail flag that could substitute for fresh calculation.

Run using Python 3 standard library, without optimization:

    python independent_check.py

For full comparison with all supplied matrices, amplitudes, branch hashes, and row systems:

    python independent_check.py --candidate CANDIDATE_SOURCE.zip --out RESULTS.json

The default invocation was rerun in an otherwise empty temporary directory containing only those two certificate files. Every computed result matched the candidate-comparison run; the only expected difference was the list of source manifest entries verified. Four corruption controls independently reject a changed raw weight, a missing bank, a changed cross-sign singleton, and a changed modulus. REPLAY_AND_CONTROLS.json and COLD_REPLAY.log record those results. The initial development run had a reviewer-side shape expectation mismatch for the supplied target; correcting its parser to the documented length-five vector encoding required no change to candidate data or mathematics.

## 3. Field and root certificate

The modulus has ascending coefficients (6,4,18,1,8,1). The freshly computed residues of t^(23^k) modulo g, k=1,...,5, are:

    (22,19,22,2,11)
    (0,4,14,16,6)
    (6,16,9,3,6)
    (10,6,1,2)
    (0,1)

Both gcd(g,t^23-t) and gcd(g,t^(23^2)-t) are 1. The last displayed residue also proves t^(23^5)-t = 0 modulo g. Independently, all 23 monic linear and all 529 monic quadratic divisors were tested; none divides g. Any reducible quintic over a field has a factor of degree at most two, so this proves irreducibility. Thus L is a field of exactly 6,436,343 elements.

The five roots z,z^23,z^(23^2),z^(23^3),z^(23^4) are nonzero and pairwise distinct. Fresh substitution gives g(root)=0 for all five, and multiplying their five linear factors reproduces g over L. Their vectors equal the supplied vectors exactly. q=13 has exact order eleven, and 11^-1=21 in F23.

## 4. Original grammar, legality, and literal matrix equality

With S e_t=e_(t+1 mod 11) and T e_t=13^t e_t, the checker constructs S and T and verifies TS=13 ST. Each supplied bank is evaluated only by the original expression

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1).

No target conjugation, replacement generator, extra phase operation, derivative atom, or omitted normalization is involved.

Every beta is 1. The general legal denominator 1-alpha^11-beta^11 is therefore -alpha^11, and it is nonzero for every bank. At the five same-sign roots the denominator vectors are:

    (7,15,5,0,6), (14,14,21,21,21), (10,9,5,10,16),
    (3,17,21,19,9), (15,14,17,19,17).

Both cross-sign denominators are (22,0,0,0,0). Independently computed determinants of all 132 literal branch matrices equal these denominators, providing a further legality check.

The checker validates all 132 inverses on both sides, for 264 matrix-product identities. Every independently computed branch-inverse digest equals its supplied digest. It accumulates each bank with its eleven original raw weights and the factor 1/11. Each of the twelve recomputed bank matrices equals the supplied matrix and has at least one nonzero entry. Within each same-sign orientation the five alphas are distinct, so those banks cannot merge merely by equal alpha. The twelve matrices sum to the directly generated negative Fourier matrix in all 121 entries, with every nonconstant extension coordinate zero. The canonical JSON hash of both fresh matrices is d167045de9e716161ca2eb5f8d0f85ed0ae0b6f885bc58f5e8ac099e6e4917b1.

## 5. Independent checks of construction data

These are supplementary checks; the literal equality above does not depend on accepting the coefficient construction.

Left multiplication in the ordered U^r V^ell basis gives the update (r,ell) -> (r+1,ell) with factor 1 and (r,ell) -> (r,ell+1) with factor q^(epsilon delta r). This independently builds every degree through eleven. The degree-eleven mixed terms vanish. Direct Fourier coefficient extraction independently yields C=18 and C*13^(3(a+b)^2) at all 121 indices.

Freshly reconstructed b=1,2 forced moments yield amplitudes 22 and 20. Their six-by-six recurrence matrix is:

    19  4 20 14 20  3
     4 20 14 20  3 14
    20 14 20  3 14 16
    14 20  3 14 16  8
    21 15 14 11 13 22
    15 14 11 13 22 19

It has rank five. A full permutation determinant computes its first-five-row/column minor as 3. Every recurrence residual against (6,4,18,1,8,1) is zero. Thus the candidate's stated unique monic quintic is verified.

All eleven original complete row matrices, right-hand sides, pivot sets, ranks, and solutions are reconstructed and compared exactly. Their ranks are 11,7,9,10,11,11,11,11,10,9,7. Solutions are independently recovered as moments of sector amplitudes obtained from the raw phase weights, rather than copied from the stored solutions. Every system is compatible. The trace pairing is independently found to have rank five, and 110 Frobenius amplitude identities verify the asserted common trace-polynomial interpolation structure.

## 6. Scope, resource accounting, and next priority

The accepted fourteen-bank lower bound over F23 relies on the relevant same-sign nodes being base-field elements in the nine singular cases. These five roots are outside F23. Consequently this valid twelve-bank extension witness refutes an unrestricted extension-node promotion of that fourteen-bank bound, while leaving the accepted base-field theorem intact.

The bank count is twelve; the displayed representation has 132 weighted branch inverses over a degree-five extension. Field construction, representing the five coordinates, obtaining roots, branch evaluation, and converting any output to a chosen representation all require accounting before an algorithmic cost conclusion. The exact roots are supplied mathematical parameters and are reproducibly computed by Frobenius powers here. Neither the supplied parameters nor this finite verification workload imply zero-cost root access, a fast implementation, or a Fourier runtime improvement. No asymptotic comparison or novelty search is part of this review.

**Next priority: 90/100.** Separately formulate and independently review the sharply pinned field-sensitive minimum with both cross-sign singleton nodes fixed at 4, using the verified rank-five gate and extension witness. Preserve the distinction from free-singleton or unrestricted bank-count optimality. That proposed theorem is not silently included in this witness-only acceptance.
