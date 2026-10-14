# Logical scope acceptance of the singleton-minimum synthesis

14 October 2026. Verdict: **ACCEPT as a source-bound logical synthesis.**

The statements b(F23)=14, b(F23³)=13 and b(F23⁵)=12 concern the same optimization problem described in `minima_synthesis/RESEARCH_NOTE.md`. No mathematical weakening or domain correction is required. This review checks the inference and domain match; it does not repeat the previously accepted numerical audits, clear historical novelty, or constitute external peer review.

## Sources actually inspected

The inspection included the complete lower-bound exposition in A and B, the underlying parameter-gate report, the symbolic/sector construction in B's independent verifier, A's original-bank and finite-gate verifier, and the original literal-matrix construction and raw-weight accumulation in C's and D's independent verifiers. It therefore does not rely only on verdict paragraphs. Labels A–D refer to the synthesis's existing source labels.

`SOURCE_HASHES.json` binds 23 source files. The synthesis's 35-entry manifest, all bound source/snapshot files, the five accepted-archive hashes and matching report members, and all seven listed transitive integrity checks passed. Checks of E and F were integrity checks only; their separate mathematics and literature review were not repeated.

## Common original-bank domain

Every relevant lower bound and witness uses N=11, q=13, S e_t=e_(t+1), T e_t=13^t e_t, and F[k,t]=13^(-kt). A physical bank is exactly

    (1/11) sum_j w_j (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1),
    1-alpha^11-beta^11 != 0,

with independently signed epsilon, delta and all parameters in the stated field. The C and D literal verifiers build exactly these matrices entry by entry, invert them, apply the eleven raw weights and 1/11, and compare the sum with this target. Their beta=1 choice restricts only their upper witnesses. There is no target conjugation, derivative atom, trace primitive, or extra permitted operation.

For necessity, the normalized coefficient formula is

    c_B(a,b)=18 A_b alpha^([epsilon a]_11) G_(epsilon,delta)(a,b),
    A_b=beta^([delta b]_11)/(11 Delta 18) sum_j w_j 13^(epsilon b j).

It divides by neither alpha nor beta. Thus all legal beta, including zero, and arbitrary raw weights are covered. The special value beta=0 may remove sectors but cannot create a contribution outside this formula.

## Effective support versus physical count

Banks with the same orientation and alpha have the same coefficient column in each sector; summing their A_b is exact grouping. At a=0 that column is 1 for every b, so a grouped vector is zero if and only if its entire grouped matrix is zero. The definition of effective node is therefore consistent with literal matrix cancellation.

Grouping never lowers a claimed physical-bank lower bound: each distinct effective alpha in an orientation requires at least one physical bank. Repetitions create no derivative or confluent-node term. Ineffective groups and extra repeated banks consume physical summands without improving the necessary support count.

The sole-support coordinate (10,1) forces the effective (-,+) node y to be nonzero. The analogous reflected coordinate forces z nonzero. On the positive-exponent central windows, a same-sign alpha=0 contributes zero and may be omitted from the support polynomial. Cancellation between orientations is already included in the sector equations; it does not undo these necessary equations.

## Why independently free y and z still give five nodes on each side

At (11-b,b), b=1,...,5, only (-,+) contributes, forcing its amplitude from y. On b<=a<=10-b both negative-delta orientations vanish. The ++ forced windows therefore depend on y alone, without an assumption about z or the size of the -- support.

Let X be the distinct nonzero effective ++ support. Its product polynomial annihilates every available window, regardless of which amplitudes vanish in individual sectors. If |X|=m<5, multiplying that polynomial by t^(5-m) gives a compatible monic quintic with zero constant term. Each resulting degree-five recurrence is an available shifted degree-m recurrence, so truncation of the windows creates no gap.

B proves rank A(y)=5 at every parameter over every extension by a polynomial Bezout certificate for maximal minors. Rank alone would not exclude m<5. The additional facts are essential: compatibility is exactly det E(y)=0, the solution is unique there, the chosen Cramer denominator is nonzero there, and gcd(N0,det E)=1 forces its constant term nonzero. Together these contradict the padded smaller support. Thus ++ has at least five distinct nonzero effective nodes.

Conjugation by J e_t=e_(-t) preserves F and maps each original bank to signs (-epsilon,-delta), preserving alpha, beta, raw weights and the branch phase epsilon delta j. Applying the same argument to that representation bounds -- using z. It does not impose y=z. Consequently every permitted representation has at least 5+1+1+5=12 physical banks.

## Exact equalities and bounded exceptions

- **F23:** A's complete parameter/root gate excludes at most five nonzero ++ nodes for every y in F23*. Reflection separately excludes at most five -- nodes. The resulting 14 lower bound matches A's fourteen literal banks.
- **F23³:** The 12 baseline forces any candidate with at most twelve physical banks to have exactly allocation (5,1,1,5), leaving no room for zero nodes, duplicates or ineffective groups. B's parameter and splitting certificates force both cross nodes to 15 and both same-sign supports to the roots of h15. B's sector functional then annihilates every bank for arbitrary legal beta and raw weights while evaluating to 14 on F. C supplies thirteen literal banks with cross nodes (15,7), so equality is thirteen.
- **F23⁵:** D's twelve-bank witness with cross nodes (4,4) lies in the free domain. Combining its accepted upper bound with B's all-extension 12 lower bound gives equality twelve. D's older witness-only verdict is not being reinterpreted as an independently proved lower bound.

The fixed-(15,15) stronger lower bound cannot be applied to C: its cross contraction 6z(z-15) need not vanish at z=7. The pinned-(4,4) F23 minimum sixteen is also a distinct optimization domain. The synthesis correctly separates both statements.

No correction was made to the research note or source bindings. No scientific kernel or historical program was executed, and no external service was written. Only this review and its integrity records were created.
