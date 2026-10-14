# Pinned F23 sixteen-bank attainment

14 October 2026. **Candidate explicit witness, pending independent review.**

## Result

An explicit legal sixteen-bank representation exists over F23 for the original signed-bank Fourier target at N=11, q=13, with exactly one effective cross-sign alpha node in each orientation, both pinned at 4. Both same-sign groups use the seven distinct nonzero nodes

    {1,2,3,4,5,6,9}.

All sixteen banks have beta=1. Every bank is nonzero. Direct modular inversion and summation match all 121 entries of the unmodified Fourier matrix. Combining this upper bound with the separately accepted lower bound gives the candidate exact equality

    b_4(F23)=16.

The accepted lower bound is inherited from the hash-pinned independent review copied into source_evidence/. It has not been re-proved in this packet. Its precise grammar, field, target, pins, effective-node convention and actual-bank count agree with this witness. The prior review proved at least seven distinct nonzero nodes in each same-sign orientation and at least one actual bank in each cross-sign orientation. This witness attains exactly that count.

This is a fixed-size, pinned representation result. It establishes no unpinned or unrestricted optimum, extension-field result, characteristic-zero transfer, novelty, or arithmetic/FFT speed improvement. It does not require or assert equality of phase weights between the two same-sign groups.

## Exact grammar

Everything is in F23. On basis indices 0,...,10 modulo eleven, let

    S e_t=e_(t+1),  T e_t=13^t e_t,  F[k,t]=13^(-kt).

Each actual counted bank is literally

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
          (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1).

Here epsilon,delta are independently +1 or -1. The legal denominator is

    Delta=1-alpha^11-beta^11 != 0.

No altered target, added generators, pre/post maps, derivative atoms, trace-bank primitive, infinite node or singular limit is used. Every displayed weight is a raw phase weight in the formula above, not a normalized sector amplitude.

## Finite search and exact stopping condition

The frozen CONTRACT.md was written before the new scientific computation. There are exactly binomial(22,7)=170544 possible seven-element nonzero same-sign supports. The code enumerates all of them, retaining those that annihilate both length-eight windows in the freshly derived b=1 moments. The successive counts are

    170544 -> 7370 -> 293.

SEVEN_NODE_CENSUS.csv records every support, all eight ascending annihilator coefficients and both residuals. SURVIVORS.json contains the 293 survivors and the derived moment data. The available b=2 window has length seven and imposes no degree-seven recurrence constraint, so it is handled in the full sector systems rather than used to manufacture another filter.

The full support-pair budget is 293^2=85849 ordered pairs. The declared deterministic order starts with equal-support pairs, followed by all unequal ordered pairs. The very first pair, with both supports {1,2,3,4,5,6,9}, solves every sector and passes the literal witness verification. Search therefore stops immediately, exactly as declared. Only one pair was tested; the remaining 85848 pairs are not claimed to have been tested. The complete support census is provenance for finding the witness, not a necessary premise for validating it. No negative nonexistence assertion is made.

## Coefficient derivation and reconstruction of raw weights

Put U=S^epsilon, V=T^delta, omega=13^(epsilon delta), so VU=omega UV. The coefficient D_omega(r,ell) in (U+V)^(r+ell) is the sum of omega to the number of V-before-U inversions over all words with r letters U and ell letters V. The fresh code enumerates those words, separately verifies the recurrence

    D(r,ell)=omega^ell D(r-1,ell)+D(r,ell-1),

and checks all mixed coefficients at degree eleven vanish. Therefore X_j^11=(alpha^11+beta^11)I, and the original inverse has the finite geometric expansion through degree ten divided by Delta.

For 0<=a,b<11, set r=[epsilon a]_11, ell=[delta b]_11, and G_(epsilon,delta)(a,b)=D_omega(r,ell) when r+ell<=10, otherwise zero. Character extraction from the literal target gives

    c_F(a,b)=(1/11) sum_t F[t+a,t]13^(-bt)
            = C f(a,b),
    C=18,  f(a,b)=13^(3(a+b)^2).

The code checks all 121 extracted coefficients and reconstructs the literal target from them. For a beta=1 bank, define normalized sector amplitude

    A_b=(1/(11 Delta C)) sum_j w_j 13^(epsilon b j).

The exponent is epsilon*b*j because epsilon*delta*ell equals epsilon*b modulo eleven. The bank's normalized Weyl coefficient is

    A_b alpha^r G_(epsilon,delta)(a,b).

For each sector b independently, the code solves all eleven equations in the sixteen bank amplitudes against f(a,b). Free variables are set deterministically to zero. The eleven coefficient-system ranks, in order b=0,...,10, are

    11,9,11,11,11,11,11,11,11,11,9.

Every solved equation is rechecked. Character orthogonality then gives the raw weights

    w_j=Delta C sum_(b=0)^10 A_b 13^(-epsilon b j).

There is no omitted factor of eleven: the inverse character sum supplies exactly that factor to cancel the 11 in the amplitude definition. The program substitutes every recovered weight back into the forward character formula and checks all 176 amplitudes.

All selected alpha values are nonzero; beta=1 gives Delta=-alpha^11, hence all branches are legal. This beta choice is an explicit construction choice. More generally, any sector-amplitude vector of a bank at a nonzero alpha can be realized by beta=1 with this inverse character formula, but that general observation is not needed to validate the positive witness.

## Literal certificate

WITNESS.json is the complete standalone arithmetic witness, containing all sixteen orientation/alpha/beta/Delta tuples, all 176 raw weights, normalized sector amplitudes for cross-checking, every bank matrix, the target and the aggregate matrix. LITERAL_INVERSES.json supplies all 176 separately computed inverse matrices.

The fresh verifier rebuilds each literal branch matrix directly from its entries. It inverts that matrix by modular Gauss-Jordan elimination, independently of the geometric-series formula used to discover the coefficient system. It then checks both matrix products against I, applies the raw weights and original 1/11 factor, and sums the actual bank matrices.

Checks completed:

- 176 literal 11-by-11 inversions.
- 352 left/right inverse-product identities.
- 176 forward character-reconstruction identities.
- 1936 literal bank Weyl coefficients against the derived formula.
- All sixteen bank matrices nonzero.
- Exactly seven distinct nonzero ++ nodes, one effective -+ node at 4, one effective +- node at 4, and seven distinct nonzero -- nodes.
- All 121 aggregate entries equal the original F[k,t]=13^(-kt), with zero mismatches.

Because each orientation/alpha pair occurs once and every bank is nonzero, each of the sixteen listed nodes is effective. In particular the cross-sign nodes are not merely syntactic banks with zero contribution. No merging or cancellation convention reduces the count.

## Reproduction and provenance

Run only this newly authored standard-library program:

    python3 -I fresh_attainment.py --out replay

A cold run reproduced SEVEN_NODE_CENSUS.csv, SURVIVORS.json, WITNESS.json, LITERAL_INVERSES.json and RESULTS.json byte-for-byte. REPLAY_VERIFICATION.json records the hashes and lengths. Timing records are deliberately excluded from the deterministic comparison. RUN.log and COLD_REPLAY.log record the same scientific summary. All historical programs were treated as inert source context and were never executed, imported or compiled. No external service was written.

The historical accepted lower-bound archive SHA-256 is

    263babd6af21fd4a198c05284f06f057ebc36b338b1ffe0e8b5cefff6e0c936d.

Its REVIEW.md SHA-256 is

    a2d110738cbfb31d51f6a20ad1fd7343e7932149088f11cee18a108c7bf2afc2.

The new witness SHA-256 is

    ad1437b4c796550d02772b7cedd78d6ff6109b180e2d9853a08b176a415dbc81.

SOURCE_HASHES.txt records the exact earlier proof files read, including the field-fusion context. The field-fusion note's old fourteen-bank next-task proposal is superseded by the accepted sixteen-bank lower bound; it is not used as a current attainment result. No historical priority score is adopted.

## Scope and review request

Independent review should recompute from the sixteen raw-weight banks alone: alpha/beta legality, exact original phases and normalization, both inverse products, nonzero/effective groups, and all 121 entries. It should separately check that the inherited lower bound uses exactly the same field and pinned architecture. Successful independent review would close the pinned F23 attainment question and establish its exact minimum at sixteen. The separately accepted extension-field equality at twelve remains a separate dependency if someone later states the matched 16-versus-12 comparison.

No further field, pin, size, or algorithm search is part of this bounded task. Search stopped at the fully verified witness.

## Raw phase weights

All entries below are residues modulo 23, in phase order j=0,...,10. Every beta is 1. Rows are actual original banks.

| Index | epsilon | delta | alpha | Delta | Raw weights w_0,...,w_10 |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 22 | 18,16,3,11,14,16,9,16,1,5,17 |
| 1 | 1 | 1 | 2 | 22 | 15,5,3,5,5,20,17,7,11,15,15 |
| 2 | 1 | 1 | 3 | 22 | 18,20,6,22,8,16,11,12,10,22,2 |
| 3 | 1 | 1 | 4 | 22 | 8,15,16,13,12,16,18,11,16,14,18 |
| 4 | 1 | 1 | 5 | 1 | 20,15,9,0,19,8,15,12,13,2,8 |
| 5 | 1 | 1 | 6 | 22 | 13,7,16,11,5,7,6,20,20,22,7 |
| 6 | 1 | 1 | 9 | 22 | 9,20,17,5,7,16,7,9,21,3,21 |
| 7 | -1 | 1 | 4 | 22 | 10,20,12,3,10,13,7,14,15,5,6 |
| 8 | 1 | -1 | 4 | 22 | 18,1,7,1,10,8,12,10,20,14,14 |
| 9 | -1 | -1 | 1 | 22 | 2,4,20,8,2,1,21,0,0,5,6 |
| 10 | -1 | -1 | 2 | 22 | 13,22,2,2,4,9,13,4,13,8,5 |
| 11 | -1 | -1 | 3 | 22 | 5,6,7,0,9,11,21,20,3,6,13 |
| 12 | -1 | -1 | 4 | 22 | 21,17,17,18,20,11,17,10,15,6,9 |
| 13 | -1 | -1 | 5 | 1 | 18,2,3,12,1,22,17,22,19,3,2 |
| 14 | -1 | -1 | 6 | 22 | 22,17,6,17,1,9,10,15,20,21,0 |
| 15 | -1 | -1 | 9 | 22 | 3,21,21,8,14,16,19,3,15,22,16 |
