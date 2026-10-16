# R14 research log — 16 October 2026

## Objective
Continue real research toward an exact all-input DFT faster than N log N;
do not relabel CrocSwap's known integer-multiplication refinements as discoveries.

## Branch triage during this run

1. **Semantic denominator resets at completed recursive C layers.** Candidate:
   shrink precision bounds using the exact semantics at child boundaries rather
   than summing all internal denominator depths. GitHub search immediately
   surfaced `references/semantic-bulk/rad20/reports/review-whole-complex-transfer.md`
   and semantic-precision composition in the CrocSwap repository. Its excerpt
   explicitly assigns completed grouped children dyadic denominator and row-sum
   bounds. This route was not developed or counted as a discovery. No external
   implementation was imported into R14.

2. **Noncyclic endpoint minimax.** The October 10 CURRENT_STATUS file still lists
   the matching noncyclic upper as unresolved. Reading the later October 12
   reviewed reports revealed that the 2-group case had already been proved and
   that the upper must be credited to classical dual flags. That case was kept
   as a regression baseline, NOT counted as new.

3. **Mixed-prime extension.** The later report and its attribution correction
   explicitly exclude mixed-prime groups. The attempted extension replaces the
   need for a completely binary flag by one orthogonal order-two pair and an
   arbitrary remaining quotient. On the lower side, the needed cardinality is
   coprime to N because gcd(N/2+1,N)=1 whenever 4 divides N. This yields the
   theorem and direct constructor in PROOF.md and annihilator_order.py.

## Relationship to the speed target

The new scope result describes the best achievable off-diagonal cut rank after
reordering, not the number of arithmetic steps. It gives no new transform
runtime. In fact that rank remains N/4+1. Treating this representation as a
constant-rank shortcut would be incorrect. No claimed kappa enhancement,
measured FFT acceleration, linear-time multiplier, or general FFT lower bound
is emitted by this checkpoint.

A separate exact transform sharing mechanism is still needed to turn the
matrix route into a faster all-input algorithm. This run does not supply one.
This is a concrete researched partial result, not an announcement of a future
asynchronous experiment.

## Verification scope

The programs were authored in this run. The modular rank oracle and the
characteristic-zero SymPy DomainMatrix rank calculation are separate arithmetic
implementations. Both use the supplied new constructor; the latter does not
call the modular rank routine. All cuts in both orientations and quotient
identities are checked. Randomized representatives are chosen by fixed seeds.
The infinite-size theorem is the mathematical proof, not an extrapolation of
the finite tests.

Read validation_modular.json, validation_charzero.json, and countercontrols.json
for exact counts, all profiles, software versions and scope statements.
Counters include empty endpoints and quotient cuts where explicitly marked.
No whole-product or whole-FFT timing was run. No GitHub writes were performed.

## Prior-art limits

The mathematical ingredients are classical/project baseline; q is standard
quasiseparable order. A complete novelty comparison with the final 2007 article
or generalized-support-weight literature was not accomplished. TW477's link
redirected to an inaccessible institutional login; no fresh PDF body or visual
inspection is claimed. The live institutional record confirms the earlier
article already concerns arbitrary finite abelian groups and subgroup-based
rank-one tilings. Our full mixed-prime minimax equality may be a consequence
of earlier results not yet checked. Global originality remains unverified.

No earlier v13 ZIP was modified or merged. R14 is a separate small research
branch with its own unambiguous filename.
