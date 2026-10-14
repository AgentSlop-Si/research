# Independent review: exact pinned sixteen-bank minimum over F23

14 October 2026. **Verdict: ACCEPT.**

The exact accepted statement is:

> For N=11 and q=13 over F23, in the original signed-bank grammar with exactly one effective alpha node in each cross-sign orientation, both fixed at alpha=4, the minimum number of actual original banks representing F[k,t]=13^(-kt) is sixteen.

The minimization permits every legal beta, including zero. The explicit upper-bound witness happens to use beta=1 for every bank; this is a legal subfamily of exactly the domain covered by the accepted lower bound. The witness and lower bound therefore establish an equality in that domain, rather than two conclusions about different scopes.

## Sources and scope

The candidate archive is `Signed_Bank_Pinned_F23_Sixteen_Attainment_Candidate_2026-10-14.zip`, SHA-256 `82cf62eb1a9c430c2dc833a092821dbe2988ab24a5ac6540ae6d401f33d826f1`. Its standalone raw-weight witness has SHA-256 `ad1437b4c796550d02772b7cedd78d6ff6109b180e2d9853a08b176a415dbc81`.

The previously accepted lower-bound review has SHA-256 `a2d110738cbfb31d51f6a20ad1fd7343e7932149088f11cee18a108c7bf2afc2`. Both that review and its acceptance record are byte-identical to the candidate's `source_evidence/` copies. All 23 candidate manifest records, all 11 accepted-review manifest records, all four declared source pins, and all five candidate cold-replay comparisons pass. The 49 snapshotted source files remain byte-identical before and after each verification run.

The primitive is exactly

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
          (I - alpha S^epsilon - beta 13^(epsilon delta j) T^delta)^(-1),

where S e_t=e_(t+1), T e_t=13^t e_t, epsilon and delta are independently +1 or -1, and Delta=1-alpha^11-beta^11 is nonzero. All arithmetic is modulo 23. This review does not introduce a transformed target, pre/post map, additional generator, singular limit, derivative node, confluent atom, infinite node, or trace-bank primitive.

## Independent literal reconstruction

`check_witness.py` is newly written standard-library code. No producer or historical program was executed, imported, or compiled. Those programs were only hashed as inert bytes. The reviewer did not use the producer's Gauss-Jordan inversion or its search/solver routines.

For each of sixteen bank records and every phase j, the program constructs the literal branch matrix directly from its entries. Each column of its inverse is then found by cyclic affine substitution. In row r, the equation is

    d_r x_r - alpha x_(r-epsilon) = y_r,
    d_r = 1 - beta 13^(epsilon delta j + delta r).

Because each witness alpha is nonzero, propagation expresses every entry as u*x_0+v. Closing the eleven-cycle determines x_0, and substitution gives the entire solution. This construction is independent of both Gaussian elimination and the quantum-binomial expansion. The program then multiplies each proposed inverse on both sides of its original literal matrix, obtaining I in every case.

Only the raw alpha, beta, orientation, and eleven weights determine the reconstructed bank. The supplied bank matrices, normalized amplitudes, aggregate, inverse records, and target records are checked against independent results and are never used to manufacture the aggregate.

Verified counts:

- 176 literal inverse matrices, with 352 left/right product identities.
- All 176 raw weights and all sixteen nonzero bank matrices.
- All 1,936 entries in the supplied sixteen bank matrices.
- All 176 normalized sector amplitudes, independently recovered from raw weights.
- All 1,936 bank Weyl coefficients, extracted from literal matrices and checked against a separately evaluated ordered-word recurrence.
- All 121 aggregate entries against the newly generated literal F[k,t]=13^(-kt), with zero mismatches.
- All 121 literal target Weyl coefficients against C*13^(3(a+b)^2), where C=18.
- Eleven independently recomputed sector ranks: 11,9,11,11,11,11,11,11,11,11,9.

Both same-sign orientations use the seven distinct nonzero alpha values {1,2,3,4,5,6,9}. There is one (-,+) bank and one (+,-) bank, each at alpha=4. All banks have beta=1, and Delta=-alpha^11 is either 1 or 22, hence nonzero. The actual orientation allocation is (7,1,1,7), in the order (+,+), (-,+), (+,-), (-,-).

Each orientation/alpha pair appears once, every recovered sector-amplitude vector is nonzero, and every bank matrix is nonzero. Thus all sixteen nodes are effective, including the required cross-sign singleton nodes. No grouping or cancellation changes the actual bank count.

## Lower-bound compatibility and additional arithmetic control

The accepted lower bound counts actual original banks, permits arbitrary legal alpha and beta values, and requires exactly one effective alpha node in each cross-sign orientation at alpha=4. It does not require a cross-sign effective group to have only one physical bank. Our witness, with one nonzero bank in each such group, satisfies that condition exactly.

The lower-bound argument first excludes at most six distinct nonzero effective (+,+) nodes. Its argument permits ineffective groups, repeated physical banks, zero-alpha groups, and arbitrary negative-delta orientations. Reflection then gives at least seven nonzero effective (-,-) nodes. The two required cross groups contribute at least one bank each, giving 7+1+1+7=16.

As an extra independent check, the new program reconstructs the lower-bound forced moments from the literal target and an independently evaluated ordered-word recurrence. It obtains forced cross amplitudes T_1=22 and T_2=20 and the windows

    b=1: 19,4,20,14,20,3,14,16,8;
    b=2: 21,15,14,11,13,22,19.

It constructs their four-row sextic-annihilator system, row-reduces it anew, and enumerates every one of its 529 monic sextics. The distribution by distinct nonzero root count 0 through 6 is

    190,214,92,26,5,2,0.

There is no six-distinct-nonzero-root annihilator. The accepted proof's padding argument covers all smaller nonzero supports too; positive exponents exclude zero-alpha contributions on these windows. The new code additionally checks 176 literal branch reflection identities and JFJ=F.

This additional check is not described as a rerun of every earlier lower-bound experiment: the 74,613-support census and historical synthetic tests were not independently re-enumerated in this review. The previously accepted proof and its complete scope remain explicit dependencies. The decisive sextic obstruction was independently reconstructed here.

Consequently the accepted lower bound gives at least sixteen banks, while the fully reconstructed witness gives at most sixteen. The pinned minimum is exactly sixteen.

## Mutation controls and reproducibility

All 198 negative controls detect their intended fault:

- Increment each of the 176 individual raw weights by one modulo 23, one at a time. Each resulting literal aggregate differs from F. Since branch matrices are weight-independent, these controls rebuild the affected contribution by the exact linear update (1/11) times its freshly computed inverse.
- Delete each of the sixteen actual banks, one at a time. Every deletion changes the aggregate.
- Corrupt one literal inverse entry. Both product identities fail.
- Omit the 1/11 normalization. The resulting aggregate differs from F.
- Change a cross alpha pin from 4 to 5. The scope checker rejects it.
- Set alpha=0 with beta=1. Legality and the witness solver reject it.
- Change an orientation. The pinned allocation check rejects it.
- Append one byte to a copy of the witness. The required source hash rejects it.

All mutations occur only in memory. The pinned sources are unchanged. A cold replay reproduces the six deterministic scientific JSON outputs byte-for-byte; timing records are excluded from that comparison. Full rebuilt branches, banks, amplitudes, coefficients, lower-bound family, mutation outcomes, and source hashes are retained in `outputs/`. The source snapshots and newly written checker support a standalone replay without executing any supplied historical code.

## Timing, errors, and acceptance boundary

The review began at 2026-10-14 00:52:44 UTC. Exact run start/end times and process/elapsed timings appear in the per-run `TIMING.json` files and consolidated `TIMING_AND_ERRORS.json`. No verification errors were observed. Model token usage is unknown.

No further search is needed for this scoped attainment question. The seven-support discovery census is source provenance only; this review does not independently endorse the search's ordering or runtime claims, which are unnecessary for witness validity. No external service was written.

This acceptance establishes no unpinned or unrestricted optimum, no result over another field, no independently re-reviewed extension-field comparison, no characteristic-zero transfer, no historical novelty, and no asymptotic or arithmetic/FFT speed improvement. It closes only the specified fixed-size, pinned, original-grammar F23 minimum at sixteen.
