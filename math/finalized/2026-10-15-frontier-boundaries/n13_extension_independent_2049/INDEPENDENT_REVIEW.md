# Independent acceptance of the N13 quintic-field minimum

14 October 2026. **ACCEPT_EXACT_MINIMUM_16, at the field and bank grammar below.**

The frozen candidate supplies sixteen legal original signed-resolvent banks over an explicitly certified field of 53^5 elements. Fresh independent arithmetic reconstructs their literal matrices and verifies every target entry. The source-bound all-characteristic-53 lower bound applies to exactly the same grammar, so the matching minimum is sixteen. No mathematical repair is needed.

## 1. Exact accepted statement

Let

    K = F53[u]/(u^5+20u^4+6u^3+45u^2+49u+34),
    N=13, q=16, S e_t=e_(t+1), T e_t=q^t e_t,
    F[k,t]=q^(-kt).

A counted physical bank is exactly

    (1/13) sum_(j=0)^12 w_j
      (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    Delta=1-alpha^13-beta^13 != 0,

with epsilon,delta independently ±1 and all parameters and raw weights in K. Within each orientation, banks with the same alpha are grouped by adding their normalized Weyl-sector amplitudes; a group is effective if its full amplitude vector is nonzero. Require exactly one effective alpha node in (-,+) and one in (+,-), with independently free locations. Every physical summand is still counted.

In that domain, the minimum is **B(K)=16**. The upper witness has allocation (7,1,1,7) in (++,-+,+-,--) order, y=z=1 and beta=1 for all sixteen banks. These are witness choices, not restrictions on the lower bound, which allows every legal beta and independently free extension-valued cross nodes.

The same minimum holds over every characteristic-53 field containing a copy of K, by embedding the witness and retaining the universal lower bound. In particular it holds over F53^d whenever 5 divides d. This is a sufficient field condition, not an if-and-only-if condition or a minimum-extension-degree theorem. The accepted prime-field minimum eighteen remains unchanged.

No altered target, pre/post map, changed generator, product of banks, derivative atom, singular limit, infinite node or trace-valued bank is admitted. No unrestricted-cross optimum, characteristic-zero result, other-root result, novelty finding or FFT-speed improvement is accepted.

## 2. Frozen source binding

Candidate archive: `Signed_Bank_N13_F53pow5_Exact_Sixteen_Candidate_2026-10-14.zip`, 217,114 bytes, SHA256

    428f9fe7a90609263b3f7e93b6a3419a7a76fe76f87c9a93334df963a57b0910

Candidate report SHA256:

    3b88ebef1c1eb37920b106c4a1112d9fdf1f11c627834ffb8bf342bfa7107f1b

Candidate manifest SHA256:

    4b62691502f53f68bfa6e5d72b733bb72786e080b5272f2bdc516737beba843c

Final raw witness SHA256:

    6d3d2e174d6db6c5ec737700e0264a0f85356a770c7687caa2a35843e454179a

The review first checked an unsealed witness with SHA256 `4c71e1a32fceb7031928efaed898d218744145820ec5d263fc71e986595dd347`. An exact parsed comparison proves that the final witness changes only `quotient_gate_sha256`, reflecting a portable source-path receipt in the quotient output. Every field parameter, bank, raw weight, amplitude and solution is unchanged. The independent checks were rerun against the final bytes. Acceptance binds only the final frozen archive and witness.

The accepted lower review is `review_n13_extension_1315/REVIEW.md`, SHA256 `896200e3b4b12d56dd13ac1d87b5e6ea64ef3283e77887898bb595d1bf304b6f`. Its source polynomial data is `signed_bank_n13_extension_1310/outputs/GATE.json`, SHA256 `54dd73908ececc376b4d1c49b80df3c740ffc9f4926825187c462599431920d7`. The exact copies and source-review manifest are verified. The prior accepted F53-eighteen result is preserved as a separate dependency; its complete base-field census is not rerun here.

## 3. Independent field certificate

The fresh checker verifies primality of 53, exact order thirteen of q=16, and factors the selected polynomial by exact multiplication:

    H(t)=t^7+15t^6+9t^5+8t^4+18t^3+25t^2+t+4
        =(t-22)(t-36)g(t),
    g(t)=t^5+20t^4+6t^3+45t^2+49t+34.

It scans the 53 base residues independently and finds exactly the two roots 22 and 36 of H. It computes all five Frobenius remainder steps modulo g, verifies

    t^(53^5) ≡ t (mod g),
    gcd(g,t^53-t)=1,

and also verifies gcd(H,H')=1. Since g is monic of prime degree five and divides the squarefree polynomial t^(53^5)-t, every irreducible factor degree divides five. The gcd excludes degree one, so g itself is irreducible. This establishes an actual field, not merely a quotient ring that could contain zero divisors.

The seven nodes are 22, 36 and the five distinct nonzero conjugates u,u^53,u^(53^2),u^(53^3),u^(53^4). All seven are independently evaluated as roots of H. Their five-component field encodings agree with the frozen witness. Field multiplication is fresh polynomial reduction; inversion uses a fresh extended Euclidean algorithm rather than the producer's implementation.

## 4. Quotient and Vandermonde bridge

For monic squarefree H with distinct roots x_i, evaluating the remainder identity t^r mod H yields

    [x_i^r] = R_H V_H,   V_H[k,i]=x_i^k.

The fresh checker verifies all 13×7=91 remainder evaluations and computes the nonzero Vandermonde determinant as the product of pairwise root differences. Thus replacement of root columns by remainder columns is an invertible change of coefficient coordinates. Multiplying each row by its prescribed G coefficient does not invalidate the identity. The two same-sign blocks use independent copies of that change; the cross columns remain literal cross banks.

The full quotient systems have F53 coefficients. Ranks of a matrix and its augmentation do not change under scalar extension, so base-field consistency is equivalent to extension-field consistency. This statement licenses a proof-coordinate change only; it does not introduce a quotient-valued physical operator.

For the selected witness, the review checks all 182 same-sign Vandermonde amplitude equations, all 26 cross-amplitude equations and all 169 complete sector equations. The actual raw banks are checked separately below, so no forced-window or quotient-only success is mistaken for an upper certificate.

The bounded candidate census was also reconstructed independently. A fresh base-field elimination solves the six forced degree-seven equations at each fixed t^6 coefficient. Exactly 51 of the 53 polynomials satisfy the nonzero-constant and squarefree guards. Fresh Frobenius gcds recover their factor-degree profiles. All 2,601 ordered guarded pairs were tested, using 11,126 complete sector systems before early rejection. Exactly (15,15), (15,37), (37,15) and (37,37) survive, with common splitting degrees 5,30,30 and 6. Hence (15,15) has minimum splitting degree only within this declared y=z=beta=1, degree-seven Frobenius-stable-support family. No broader negative or minimum-degree conclusion follows.

## 5. Literal original-bank upper bound

The independent checker never executes or imports producer or historical scientific code. It reconstructs each original branch by a different route: solving its cyclic row equations directly.

For d_r=1-beta q^(epsilon delta j+delta r), the literal equation is

    d_r x_r-alpha x_(r-epsilon)=b_r.

Every witness alpha is nonzero. Traversing r=0,-epsilon,... gives an affine recurrence whose closure solves x_0, then all remaining coordinates. This is done for all thirteen basis right-hand sides of each branch. Every result is independently multiplied on both sides by the original sparse matrix, checking every entry of both products against the identity. The method does not depend on the quotient solution or the producer's Gaussian inverses.

Exact checks pass:

- 208 literal 13×13 branch inverses;
- 416 left/right inverse matrix identities, totaling 70,304 entry equalities;
- all sixteen Delta values nonzero, with Delta=-alpha^13 because beta=1;
- all 208 raw-character amplitude identities with the original 1/13 factor;
- all 2,704 independently extracted bank Weyl coefficients;
- all sixteen physical bank matrices nonzero;
- distinct same-sign alpha nodes and exactly one nonzero effective alpha group in each cross orientation;
- every one of the 169 entries of the aggregate equal to q^(-kt).

All producer inverse matrices, bank matrices, aggregate and target arrays are compared with these fresh reconstructions and agree. Exact matrix equality establishes the action on every vector in K^13. It is stronger than a random-vector test. The raw weights stay in K; no trace or descent operation is applied.

Falsification controls reject omitting 1/13, using the positive-exponent target, omitting one nonzero bank, or changing one target entry. Zero individual raw weights are legal; the required effective groups and complete bank matrices remain nonzero.

## 6. Independently reconstructed universal lower bound

The lower source's grammar matches the new upper exactly, including arbitrary legal beta and extension-valued independently free y,z. I read its original-bank expansion, forced-window argument and all-extension minor proof.

The review also rebuilds that decisive algebraic certificate independently. It computes G from the Gaussian product formula, derives all target coefficients directly, verifies all reflection identities, and reconstructs the original polynomial moments

    v_b(a;y)=[q^(10(a+b)^2)
       -y^(13-a-b)G_-+(a,b)/G_-+(13-b,b)]/G_++(a,b).

For a sole effective cross node, the coefficient at (13-b,b) forces its amplitude; y=0 is impossible. The positive-exponent windows have lengths 11,9,7,5,3,1. At most six distinct nonzero effective same-sign nodes would give a common monic annihilator of degree at most six; multiplication by a power of t pads it to degree six. Zero nodes do not contribute on these windows, and repeated ordinary nodes merge without producing derivative atoms. Arbitrary beta values only change amplitudes and therefore do not evade this necessity.

The nine length-seven windows form the original 9×7 polynomial matrix. A fresh subset-dynamic-programming determinant expansion, not the producer's or previous review's determinant routine, computes its minors on row sets (0,1,2,3,4,5,6) and (0,1,2,3,4,5,7). Both are degree 39 and match the accepted source coefficient by coefficient. Multiplication by the two saved degree-38 Bézout polynomials gives exactly 1 in F53[y]. A changed-minor control fails that identity.

This is a polynomial identity, not equality only at the 53 prime-field points. It persists under every characteristic-53 field embedding. Thus at every y the two minors cannot both vanish, the matrix has full column rank seven, and no padded degree-six annihilator exists. At least seven nonzero effective (++) nodes are required. Simultaneous reflection gives the same independent bound for (--), with its own cross node z. The two effective cross groups require two additional physical banks. Hence every representation in the stated domain needs at least 7+1+1+7=16 banks.

Combining this universal lower bound with the literal upper proves the exact minimum. No base-field nonsplitting argument is incorrectly promoted to an eighteen-bank extension lower bound.

## 7. Costs and retained open scopes

This is a finite representation-count result. Sixteen banks contain 208 inverse branches, and extension-field operations have their own prime-field and bit costs. The candidate's inherited unoptimized application budget is arithmetically consistent: 16×3×13^2=8,112 K-multiplications and 16×(3×13^2−3×13)+15×13=7,683 K-additions after constant preparation. It is an upper budget for that literal schedule, not a lower bound or speedup. Setup, weights, storage and field arithmetic remain separately paid; the target already has the classical one-convolution chirp reduction.

Accept the bounded child `M-MAGNETIC-SPAN::Q35::N13-q16-F53pow5-free-cross-singleton-exact16`. The linked M-MAGNETIC-SPAN, Q35, NEW-17 and NEXT-MAGNETIC-SIGNED parent views remain TO RESEARCH at their recorded priority 56. The proposal itself specifies zero canonical closure-count change. Other fields, unrestricted cross supports, other roots/characteristics, broader constructive families and paid fast evaluation remain open. Existing exact F53 minimum eighteen is preserved.

## 8. Integrity and replay

The candidate archive, inner manifest, source snapshots and final witness are checked byte-for-byte. The earlier accepted lower-review manifest is independently rehashed. `CANDIDATE_BINDING.json` gives exact identities and the one-field pre-freeze/final difference.

A cold replay in an isolated directory runs only this review's two newly authored scientific programs with four inert JSON inputs. All six mathematical JSON outputs agree byte-for-byte with the first run. `COLD_REPLAY.json` and the review manifest supply the receipt.

No external service write, uploaded-program execution, imported historical scientific module, scope enlargement or novelty promotion occurred. The acceptance condition is met: both the literal upper and source-bound universal lower have passed independent exact checks in the same field/target/bank grammar.
