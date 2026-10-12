# Independent bounded acceptance: Q27 stage-1 edges (8,9,14)

12 October 2026 UTC. Decision: **INDEPENDENT_ACCEPT**, restricted to the one named frozen unit-phase slice. The full Q27 target fiber remains **OPEN**.

## Accepted statement

For the original Phase42 N=8 chart, vary only stage-1 edge gains 8, 9, and 14 by unit complex multipliers x, y, z. Keep the other 31 free phases, all 14 tree-pinned unit edges, all six directed cycle masks, both unweighted three-Green sums, M=S2*S1, and the absence of an interstage diagonal fixed. Require every one of the six Green denominators to be nonzero.

No matrix in this slice is externally equivalent to F8 by arbitrary invertible complex row and column monomials. This is an exact characteristic-zero exclusion of the entire named three-phase domain, not a local Jacobian observation or approximate fit.

The tuple (1;8,9,14) is absent from the accepted 132-element union. Adding precisely this tuple gives **133 of 5,984**, with **5,851 unclassified**. The previously accepted (1;8,9,13) slice is inherited unchanged and was not rerun. The count 5,984 is choose(34,3), so it includes mixed-stage triples; the same-stage tuple notation does not reclassify those.

## Sealed candidate and source binding

Candidate: Q27_Stage1_8914_Exclusion_CANDIDATE_2026-10-12.zip, 3,982,643 bytes.

SHA-256: 70f34e248b90abd2c0f95f9220efc22b032c519dc168eb91d723efcec7837bca.

All 43 archive members are safe, unique paths; the 42 non-manifest files are length- and SHA-256-bound by the root manifest. All 17 source records match their original local source bytes. SOURCE_BINDINGS_VERIFICATION.json records those checks. The complete independently accepted edge13 predecessor is retained at SHA-256 9b102109c5dc913b809251402381a3da5e9bf8a02d9fd5513ef9b31fa14777f0. Its manifest and acceptance seal were checked as data, without executing any predecessor program.

The original chart is pinned at SHA-256 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98. The pre-search frozen-scope and six-guard hashes are, respectively, 46dcb1e517c13e40956b3be488a14b4cf145d715f630414319e761d7b33c1eae and 251f50651bfba3c28e4e3e62af733f10cf16b6240d236e0f4634d3b899aebe52. These bytes remain unchanged.

The reviewer regenerated both sets of seeded masks, the spanning-tree/chord split, and every Gaussian pair from the chart's source conventions. The inert Phase41 and Phase42 text was inspected, including the seeds 42420/42520, phase sampling seed offset 7919+N, exact Gaussian weight convention, unweighted branch sums, and product order. Additional inert Phase40 text independently confirms that Edge fields are cycle,target,source,weight. Thus the active directed edges are exactly 5→0, 0→4, and 3→7; the last is edge14, not predecessor edge13.

The primary text copies have the explicit provenance limitation in PRIMARY_SOURCE_METADATA.json: they are retained text snapshots plus final newline, not claims of byte-for-byte identity with unavailable original uploads. This does not change the directly pinned chart data. No historical research code was executed.

## Original target and all six guards

Write S_s=sum_b (I-W_sb)^(-1), b=0,1,2. All six W matrices use the original masks. Every frozen edge gain is (a+ib)/(a-ib), or a tree-pinned 1; the reviewer verified all 48 frozen gains have exact norm one.

Let h_sb be the original branch holonomy. The six values are:

- h_10=(65+72i)/97
- h_11=(-383187819337037874577+235291331868842780736i)/449660889716782337425
- h_12=(-7219486963274846816853-5897211386485827321196i)/9321914725516081613405
- h_20=(-780+731i)/1069
- h_21=(-4335586066535028372496+1298149621513208810103i)/4525759492081695535625
- h_22=(91471421459307165236012877+37193164409786343925998436i)/98743872835733949286881365

Five guards are the nonzero constants 1-h_sb. The active stage1/branch1 guard is F=1-h_11 xyz. All six literal guard polynomials were independently reconstructed and compared against their pre-search pin. The task does not discard a denominator after polynomial clearing.

The independent verifier derives each inverse by generic Gaussian elimination over Q(i)(x,y,z), then verifies both inverse products, its determinant d_sb, and the polynomial numerator B_sb=d_sb(I-W_sb)^(-1). It checks all twelve polynomial two-sided identities and all six W_sb^8=h_sb m_sb I identities. This is a different arithmetic and matrix-construction path from the author's rational-pair polynomial matrix-power verifier and directed-path generator.

Let C be the fixed second-stage sum and let

A=B_11+F(G_10+G_12), N=C A.

The verified inverse identities imply N=F M throughout the stated legal domain. Every entry is triaffine. No extra phase, gain, mask or interstage freedom is introduced.

External invertible row/column monomial equivalence to F8 implies rank-one squared entry moduli, since Fourier entries have constant modulus and external scaling separates by rows and columns. Therefore every anchored defect D_rc=|M_rc M_00|²-|M_r0 M_0c|² vanishes. This necessary condition is enough for exclusion; the review does not assert it characterizes Fourier equivalence. No matrix entry is divided out.

With t=xyz and Ntilde=t conjugate(N)(1/x,1/y,1/z), define

P_rc=N_rc N_00 Ntilde_rc Ntilde_00-N_r0 N_0c Ntilde_r0 Ntilde_0c.

On the unit torus, P_rc=t²|F|⁴ D_rc. The multiplier is nonzero on the admitted domain. Thus every Fourier-equivalent admissible point would annihilate all 49 P_rc.

## Independent exact certificate

The reviewer reconstructed all 49 P_rc from its own inverse-derived N. Exact polynomial division by F reproduces all 49 stored Q_rc=P_rc/F, followed by full multiplication back. There are 2,058 nonzero quotient coefficients, a union of 44 quotient monomials, and 63 defect monomials.

CERTIFICATE.json supplies 42 constant Gaussian-rational multipliers, with the common positive denominator given literally in 3,334 decimal digits (11,074 bits). The largest absolute numerator component is 11,070 bits. The reviewer checks the complete identities

sum_j c_j Q_j=F,

sum_j c_j P_j=F².

Both support equations omitted in the author's square system, exponents (3,3,2) and (3,3,3), are included in this final coefficientwise check. A finite-field scout or rank computation is not used as a characteristic-zero proof.

If an admissible target point existed, all P_j would vanish and the second identity would force F²=0, contradicting the guard. Equivalently F² lies in the defect ideal, so saturation by xyz times all six guards is the unit ideal. This saturation restates the original guarded-domain exclusion; it makes no claim at an excluded pole.

## Review of the bounded divisibility lemma

The candidate's explanatory lemma is correct under its stated same-branch, fixed-other-branches and unit-frozen-gains assumptions. Modulo F, xyz=h^(-1), so the coordinate ring is the Laurent ring Q(i)[x^±1,y^±1]. All active branch edge weights are units and their product is one. Cumulative products give an invertible diagonal conjugacy from W to the plain cycle permutation matrix. Hence B=I+...+W^7 is conjugate to the all-ones matrix and has rank one. N=C B modulo F consequently has rank at most one.

Coefficient conjugation with reciprocal variables preserves (F), because 1-conjugate(h)/(xyz)=-conjugate(h)F/(xyz). It therefore induces an involution of the quotient ring. Multiplication by xyz is by a unit, so Ntilde also has rank at most one. The anchored minors of both matrices vanish, which makes every P_rc vanish modulo F and proves polynomial divisibility.

As a separate concrete check, all 784 two-by-two minors of the active B were verified divisible by F. The lemma does not supply the multiplier identity, and neither it nor this finite check excludes any other tuple. The characteristic-zero multiplier identity above is separately established for edge14 only. No new canonical research identity or novelty is inferred.

## Adversarial controls and exact oracles

The independent checker rejects:

- A changed real or imaginary multiplier numerator
- An omitted interior multiplier or changed denominator
- A wrong power of F
- Changes to either omitted-square-system target coefficient
- Omission of coefficient conjugation
- Reversal of stage product order
- Omission of each of the six guards
- A changed active guard coefficient
- A nonunit moving phase

At four exact Gaussian-rational triples and their conjugate-reciprocal triples, it performs 48 fresh direct inverse computations, 96 two-sided inverse products, 48 guard checks, 768 numerator/reciprocal entry identities, and 196 quotient-evaluation checks. Three triples lie on the unit torus and give 147 exact identities linking the constructed P_rc to the actual modulus defects of the original M. The fourth is a nonunit algebraic control and is not admitted as a feasible phase point.

At the unit-torus pole (1,1,1/h), the active B is nonzero and (I-W)B=0. Generic exact inversion explicitly rejects the matrix as singular, and the domain-admission check rejects the point. A vanishing cleared polynomial at this pole is never counted as a witness.

These controls supplement the global polynomial proof; they are not its substitute.

## Replay and independence

review_8914.py is a newly written task-local independent checker using Python's standard library and SymPy 1.14.0. It imports neither candidate nor historical programs. CODE_PROVENANCE.json records that earlier reviewer text was inspected as a static reference. It does not claim independence from all mathematical ideas in prior review; it does independently reconstruct and verify this new slice using a different inverse derivation and arithmetic implementation.

The current edge14 author verifier was inspected in full, extracted from the sealed candidate into a separate read-only directory, and replayed with python -I -S. Its PASS, exit code, hashes and outputs are bound in AUTHOR_VERIFIER_COLD_RECEIPT.json. This executes only the current task's checker, not a predecessor or original supplied program. The independent final archive is cold-replayed separately with python -I, reading its embedded candidate ZIP directly and writing its result outside the read-only extraction. The adjacent final seal binds that replay receipt and the archive bytes.

Reproduce the independent proof check with:

python -I review_8914.py Q27_Stage1_8914_Exclusion_CANDIDATE_2026-10-12.zip --expected-sha256 70f34e248b90abd2c0f95f9220efc22b032c519dc168eb91d723efcec7837bca --output q27-8914-independent.json

No author generator, C++ compiler, optional solver, predecessor program or historical executable is needed. Explicit rejection checks remain active under Python optimization; ordinary execution with -I is the documented replay.

## Cost and final scope

This is an offline, finite exact certificate. Large integer arithmetic, all literal multipliers, source reads, polynomial construction, rational arithmetic and both replays are paid work. The author's 42-dimensional Bareiss solve reports 24,682 checked exact divisions; the reviewer statically checked that this is the loop count sum(j(j+1), j=1..41), without rerunning the solver. The final proof depends on the exact verified identity, not on trusting that solve. Local elapsed times are reproducibility observations, not benchmarks.

Only the named new tuple is accepted. The broader Q27 target-fiber problem remains open. Other triples, symmetry transfer, other frozen witnesses, four or more moving phases, free interstage diagonals, nonunit internal gains, larger N, a full 34-phase witness or obstruction, construction efficiency and historical priority remain unproved here. Prior one/two-coordinate counts are unchanged. The review does not claim any broader result or historical-priority clearance.

Derivative note: private source-access/tracking and integration wording is omitted, and the reproduction output path is relative. All proof, exact certificate identities, source-provenance limitations, independent controls and remaining mathematical limits are retained. Original report SHA-256: `105ee7dbb705c74527a03c87dd232bd294c86f7c54ab9de93a9e3e09f5a012f8`.
