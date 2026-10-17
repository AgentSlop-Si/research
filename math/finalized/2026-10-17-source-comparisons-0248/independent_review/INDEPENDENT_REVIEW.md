# Independent verification of three bounded source comparisons

17 October 2026, UTC. Mathematical review of ALG-077, ALG-047 and ALG-012 against named primary sources. Publication and native-table application are separate from the mathematical acceptance below.

## Verdict

ACCEPT the three frozen bounded comparisons, with ALG-012 accepted only after the execution-evidence repair disclosed below. This is not whole-owner closure. Exact candidate bytes and publication limits are sealed in ACCEPTANCE.json.

## Independent work

The reviewer read the two complete ALG-077 proof/audit bodies, the accepted ALG-047 proof/review, and ALG-012's proof README and independent review. The exact owner identity, open status, priority 34, current gate and historical overlays were inspected in the fresh native baseline and commit-pinned open index at `26eb7017276591988762f27e2d1c23e739bcf3e4`.

The following primary source bodies were read directly, rather than inferred from abstracts or secondary summaries:

- [Chan et al., v3](https://arxiv.org/html/2310.13174v3): Lemma 2.2 and Appendix B, particularly B.6–B.8 and their input packing, preparation, twiddle and transposition accounting.
- [Fürer, v1](https://arxiv.org/pdf/1402.1811v1): Definitions 1–2, the SS-C discussion and Theorem 1(a).
- [Gurevich–Hadani, v1](https://arxiv.org/pdf/math/0610818v1): Theorem 1.2.1, equations (1.2.2)–(1.2.3), the induced vector-space twisted convolution and Cayley kernel (2.1.1).
- [Gurevich–Hadani–Howe, v3](https://arxiv.org/pdf/0808.2447v3): standard Heisenberg action and Theorem 2.4, including the displayed Weyl matrix and unnormalized Fourier scalar.
- [Vaidyanathan, author-hosted body](https://systems.caltech.edu/dsp/PPVSquare.pdf): section 4, equations (15)–(22), Theorems 1–2 and concluding complexity boundary.

This independent reviewer did not import or execute any supplied or historical executable. The reviewer wrote a new standard-library control program from the mathematical formulas. It does not load any other program.

## ALG-077: qualified nonmatch

The named multiplication theorems have discrete exact outputs and logarithmic-word machine contracts. The reviewed lift has per-input randomized, energy-relative coordinate error for all normalized complex Fourier outputs, with represented-input and finite-precision hypotheses. These contracts cannot be identified by equating their length symbols or by noting that each uses an FFT.

The report correctly distinguishes full weighted-input Taylor from frozen-block fusion, including the latter's extra bias. The full-row numerical contract and the separately supplied summary-decoder contract are different. A fresh exact scalar countermodel corroborates this logical point: compression by 1001/1000 followed by decoding by 1000/1001 has zero composite error, but the latter operator is not an exact identity decoder on supplied summaries. This is only a countermodel to an inference from composite accuracy alone, not a simulation of the implementation.

The immediate conversion from coordinate error to vector l2 error loses sqrt(N), which is sharp for that inference. Input bit length is distinct from coordinate count. Paid coefficients, guard roots, range handling, output conversion and R full scans remain in the ledger. Qualified nonmatch means that the specified direct implication or fully charged adapter has not been supplied; it is not a proof that no future adapter can exist. Q01 and ALG-028 remain separately scoped.

## ALG-047: exact specialization plus elementary deduction

With the repository's shift convention, its vector (a,b) maps to the primary source's (-a,b). This preserves the repository symplectic form. The Fourier Weyl matrix used in Theorem 2.4 has Cayley transform minus itself, giving the negative quadratic symbol in the repository convention. The source's standard-character Fourier scalar is checked separately; arbitrary primitive complex roots use the trace-defined Gauss scalar rather than silently retaining that scalar.

The comparison uses explicit vector-space synthesis and its trace inverse. A literal full-Heisenberg-group sum with counting measure repeats every central-equivalent term and requires division by the center size. This normalization is fixed explicitly, rather than left to ambiguous synthesis notation. The theorem's Weyl matrix, not the differently signed introductory display, fixes the sign convention.

Pulling the symbol back through an independent ordered pair and removing its multiplication cocycle yields invertible row/column scalings of the matrix with entries omega^(-kappa mn/2). It has rank one for kappa=0 and rank N otherwise. This last rank statement and product-count interpretation are elementary deductions from the primary algebra/kernel, not literal quoted theorems there. Reversing an independent compatible pair changes compatibility. The separate guarded finite-field specialization, rational-degree obstruction and broader evaluator questions are not attributed to the complex-valued representation theorem. No arithmetic lower bound follows.

## ALG-012: exact ambient-space correspondence, different evaluator contract

At q=2m, the folded coefficient difference r has odd outputs given by evaluation modulo z^m+1. The time-domain primitive-frequency projection is the periodic repetition of q/(2N) times (r,-r). The dyadic Ramanujan sum is m at 0, -m at m and zero elsewhere in one period. Consequently the first m shifted sums have exact coordinates beta_j=r_j/N in the original length-N projection. This establishes the complete phi(q)-dimensional ambient correspondence, with the normalizations and domains explicit.

The source basis theorem does not provide the separately charged signed-P5 sparse-defect discovery, two dense anchors, recurrence walks or cheaper-local-FFT choice. For q>=4, the kernel of P5-I is two-dimensional; the preimage of a fixed S-coordinate defect support has dimension at most S+2. The q=2 case has dimension one. This is a restricted union of subspaces, not arbitrary input coverage. The reviewed all-orbit count 9N-12+2T+nu, local fallback, root/index costs and all N outputs remain intact. ALG-052's global relative-field rank formula is a different result and must not be imported into this owner.

## Fresh controls and limits

`independent_comparison_checks.py` passes:

- Exact modular Weyl trace symbols, dephased tensors and ranks for every independent ordered pair at prime lengths 3, 5, 7 and 11; the respective compatible counts are 16, 64, 288 and 1200. All compatible reversed-pair controls fail compatibility as required.
- Four complex standard-character normalization controls, with largest floating residual below 6e-16.
- Exact modular signed-P5/odd-evaluation conjugacy, full evaluation rank and fixed-support dimension bounds at dyadic conductors 2 through 256.
- All primitive spectral projections for 28 ambient-N/conductor pairs through N=128, using beta=r/N.
- Complete output-index partitions and independently recomposed orbit/local-FFT ledgers for ten dyadic lengths through N=1024.
- The exact abstract composite/summary-interface countermodel described above.

The modular controls use explicitly verified roots in prime fields; they corroborate the algebra and do not extend the external complex representation theorem by themselves. Floating controls are corroboration, not exact proofs. Ledger recomposition is not a replay of the production operation counters. The comparison verdicts rest on the written contracts and derivations.

## Execution-boundary deviation and repair

During review, the first ALG-012 candidate checker was found to import and call the archived evaluator. The author confirmed two local runs, contrary to the no-historical-program-execution boundary. Those results are excluded from the accepted comparison evidence. The earlier files and observed cache/result-file changes were preserved separately, and the report now discloses the event and its observation limits. No conclusion of production replay is accepted.

The revised ALG-012 checker was inspected to confirm that it consists of fresh formula-only controls with standard-library imports and no historical code dependency. The independent reviewer executed only that revised checker. Its formula and coordinate results agree with the reviewer's independently authored controls. This repair restores the accepted evidence's required scope; it does not undo or conceal the earlier deviation.

## Application boundary

Only the three comparator-specific outcomes may be recorded as completed. Keep each owner TO RESEARCH at priority 34, the 90 closed / 237 open / 327 total census, all prior proof and novelty attributions, all historical characters and notes, and unrelated owners unchanged. Historical text may be appended to, never silently erased. Any change to a current gate must preserve its previous value in dated history. Native/index plans and postwrite receipts require separate exact verification.
