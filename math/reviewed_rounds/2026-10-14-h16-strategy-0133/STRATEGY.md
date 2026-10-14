# H16 finite-word search: strategic and prior-art audit

14 October 2026. Read-only source audit; no construction search or external write.

## Recommendation

**Park further undirected H16 enumeration now. Preserve the exact ≤31-call target and its accepted conditional lift as a high-value open construction problem.** This audit did not locate a published ≥32 lower bound in the precise unrestricted-monomial model. It also did not identify a new, sufficiently specified construction family with evidence of a ≤31-call realization. Neither statement implies existence or impossibility.

Sparse-plus-low-rank constructions are genuinely different from small edits of a butterfly schedule, but they are established prior art and have already been discussed in the supplied research. Translating their additive sharing into a 16-register invertible paired-gate word is the missing idea, rather than a routine compiler step. Calling this an unexplored method would overstate the evidence.

No new finite experiment is recommended in this pass. The stopping condition is met: the declared local searches are closed, relevant published model boundaries have been checked, and no qualifying new seed was found. Reopen construction work when an explicit different topology together with a coefficient mechanism, or an actual exact word, is supplied. Mere survival of support tests, a larger numerical search budget, or another finite-field bank-count improvement is insufficient motivation by itself. This parks this search, not the broader FFT goal.

## Exact problem and why success would matter

The required identity is H16 = H2 tensor-powered four, with H2 = [[1,1],[1,-1]], acting on exactly 16 independent, arbitrary complex inputs. At most 31 forward two-register H2 calls are permitted, interleaved with invertible monomials having unrestricted nonzero complex scalars. There is no initialized or borrowed seventeenth register. A scalar-addition DAG, quantum gate count, approximate factorization, finite-field solution, or singular limiting identity is a different object.

The supplied independently accepted archive establishes a conditional interface, not a witness. Its charged active-sector recursion gives the conditional bound

    O(n (log n)^(199/200) (log log n)^(601/200)),

and eventually O(n (log n)^0.997), assuming admission of the absent finite word and the stated exact-complex, specified-root compiler interfaces. The strict inequality 31^200 < 32^199 supplies the exponent margin. This is much more consequential than replacing a fixed FFT radix by a slightly cheaper block. An ordinary fixed-radix substitution alone changes a leading constant.

The report's acceptance leaves the exact witness, admissible coefficient representation, full compiler/scheduler implementation, and any formal proof claim separate. Re-auditing the same conditional implication will not resolve the construction bottleneck. The primary source interface is the pinned [finite-win synthesis section](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/synthesis.tex); this audit used its supplied snapshot and the accepted review, without re-authenticating the remote pin or auditing the entire preprint.

## Lower bounds: the valid floor and the invalid shortcuts

**A coefficient-independent floor is 28.** The complete gossip theorem requires 2n−4 pair meetings for n≥4. A two-register linear operation can only pass on the union of its operands' input dependencies. Arbitrary diagonal scalings do not spread dependencies; permutations can be absorbed into wire labels. Since H16 is dense, every output needs a path from every input. Applying the theorem therefore gives g≥28. It does not exclude 28–31, and gossip schedules meeting the bound need not realize the target coefficients. The same argument rules out strict pair-call improvements at widths four and eight. [Baker–Shostak, 1972; the linked collection also contains Tijdeman's matrix formulation](https://www.math.uni-bielefeld.de/~sillke/PUZZLES/gossips.pdf).

**The familiar 32-call entropy bound has an extra hypothesis.** Ailon's Theorem 2.1 works with unitary two-coordinate gates and unitary intermediate matrices. Its entropy proof also applies to normalized Walsh–Hadamard matrices because every squared entry modulus is 1/n. Allowing arbitrary invertible diagonals removes that premise. Normalizing the final answer does not normalize every intermediate state. [Ailon, 2013, theorem and proof](https://arxiv.org/html/1305.4745v1).

Ailon's later bounds require uniform ordinary or algebraic conditioning. Those restrictions cannot be silently added to the present target. [Well-conditioned model](https://arxiv.org/abs/1403.1307), [algebraic conditioning](https://arxiv.org/abs/1609.03278).

Likewise, determinant-growth arguments with bounded scalar coefficients do not apply to free unrestricted scalings. Here det(H16)=2^32, so a 31-call word would merely need the product of its monomial determinants to equal −2, which is allowed. This is a necessary consistency check, not an obstruction.

## What is already excluded, and what prior art actually supplies

The supplied relocation report excludes all 1,845,120 labeled delete-two/insert-one descriptions of the fixed ordinary schedule by exact support propagation. Its two independent checks have no survivor. This is complete for that declared family only.

Earlier saved exact-width work reports 210,833,760 delete-one/replace-at-most-two descriptions: 556 pass support and all fail its rank-cut stage. These historical results were read, not rerun or newly certified here. The two family counts must not be added as a count of distinct excluded circuits. Increasing edit radius is not supported by a success trend in these results.

The closest constructive alternative is published non-rigidity work. Alman gives a rank-one matrix differing from 16-by-16 Hadamard in 96 entries; this supports improvements in a wire-count linear-circuit model, not the required paired-gate count. His notation H4 denotes our H16. [Alman, Lemma 4.7 and Corollary 4.10](https://arxiv.org/pdf/2102.11992).

Alman–Rao's Algorithm 5 uses 22 additions in its scaled-input size-eight core; expanding it at size sixteen gives 44 top-level additions plus 16 base-case additions. This is an arithmetic DAG, not a 30-H2 word. The distinction is substantive: the 22-addition size-eight core still cannot become an 11-H2 word on exactly eight registers, by the gossip bound above. Their work supplies useful algebraic benchmarks and leading-constant improvements, but no admitted H16 word. The paper also explicitly distinguishes operation-count and wire-count models. [Alman–Rao, Algorithm 5, Section 6.2 and related-work discussion](https://arxiv.org/pdf/2211.06459).

Published searches for optimal streamed WHT networks optimize RAM and switches among structured butterfly networks. Their optimality does not mean optimal H2 count under arbitrary diagonals. [Serre–Püschel, 2019, Sections 1–4](https://fserre.github.io/publications/pdfs/icassp2019.pdf).

## Relative value of the bank results and the FFT frontier

The recent signed-resolvent-bank results are exact finite-field representation results in a specified dictionary. The accepted quadratic result fixes N=11, q=13, two cross-sign singleton nodes pinned to 4, and counts original resolvent-bank summands. The newly read unpinned candidate retains singleton restrictions and was still marked awaiting independent review. These are useful completed or nearly completed algebraic obligations in their own domains.

They provide neither a characteristic-zero H16 factorization nor a charged asymptotic method for evaluating a growing family of banks. A summand count does not pay for its matrix inversions, coefficient preparation, applications, or recombination. Thus they currently have weaker direct relevance to the stated FFT exponent objective than an admitted H16 word, despite being much closer to fully certified standalone results. Further dictionary refinements should be justified as bank research, not reported as progress on the absent FFT construction.

The right frontier distinction is: the conditional H16 implication is accepted; a qualifying H16 word is absent; a general 31-call impossibility theorem was not found; the actual all-length FFT improvement remains unproved by this work. Parking an unguided search preserves all four statements.

## Audit scope and provenance

Primary-paper searches covered unrestricted/in-place pair gates, unitary and conditioning bounds, Hadamard non-rigidity, and optimal butterfly networks. This was bounded literature triage, not an exhaustive bibliographic review or a historical-priority determination. Failure to find an exact-model theorem is not proof that none exists. Search-engine freshness labels were not treated as publication dates. No third party was contacted.

The supplied archive, relocation report, earlier exact-width notes, cancellation audit, and recent bank reports were read as inert documents. No historical scientific code was executed. Only local source hashing and report creation were performed. `INPUT_HASHES.json` identifies the exact local sources, including the reviewed archive and its internal review text. No new transform, lower bound, novelty claim, benchmark, or source-code search result is asserted.
