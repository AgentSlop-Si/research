# ALG-006: bounded fixed-total-order confluent-Prony comparison

Date: 2026-10-13 UTC. Scope: only the fixed-total-order D branch. Result: **partial match overall; exact algebraic match of the channel recovery core after the stated change of basis; no demonstrated worldwide novelty.** No historical scientific code ran. No live Sheet, repository, or archived claim was changed.

## Frozen project claim

Pinned `CONFLUENT_FUSION.md`, SHA-256 `5f31ce4af2eba202f66ce217c07feafdcf038d4d96bb557c53c3a4c7f2f686a4`, “Family and pilot” through “Bound, capacity and evidence,” with the field/sign/cost qualifications in the pinned audit below.

For N=QM, raw rows y_t[u]=x[t+Qu], supplied prime p>N of polynomial size, primitive Nth root omega, eta=omega^Q, Q>=2D, and balanced Q²,M²=O(N): the first 2D rows have form

    y_t[u] = sum_j sum_{ell=0}^{d_j-1} binom(t,ell) mu_j^t b_{j,ell}[u-a_j t],
    sum_j d_j=D.

Shifts a_j are distinct; mu_j≠0; lambda_j(h)=mu_j eta^(-a_j h) are distinct at every channel h. Each channel's D-square pilot Hankel is nonsingular. Nonzero top-degree component spectra and p>D suffice. Parameters, baselines and multiplicities may be unknown. Later raw residuals under product_j(1-mu_j S_{a_j}L)^{d_j} have total spectral event budget R_b=O(Q), beginning after the clean pilot. All raw coordinates, residuals and reconstruction are checked. Wider dirty/degenerate-pilot families may decline.

The claim is recognition/bounded rejection plus explicit full DFT of the accepted input in O_D(N+M²+M(Q+R_b)+Q R_a), with O_D(M+R_b+1) scalar inversions and O_D(N+R_b) words. It is a fixed-D theorem, with an accepted design/reference check, not a shipped optimized executor or arbitrary-vector operator-application theorem.

## Primary theorem selected and retrieved

**P1:** Dmitry Batenkov and Yosef Yomdin, *Geometry and Singularities of the Prony Mapping*, Journal of Singularities 10 (2014), 1–25, DOI 10.5427/jsing.2014.10a. [Publisher full paper](https://www.journalofsing.org/volume10/batenkov-yomdin.pdf#page=7). Use Problem 1.3 (pp. 2–3), Theorem 3.6 (p. 7), and Theorem 3.5 proof, Appendix A (pp. 22–24).

Theorem 3.6 treats 2d complex moments with unknown multiplicities. If r is the rank of the d-by-(d+1) Hankel, solvability is equivalent to its leading r-square minor being nonzero. The recovered rank is r<=d; nodes, multiplicities and coefficients are unique up to permutation. Multiplicities come from poles of the Padé rational function.

**P2, supporting mechanism only:** Batenkov and Yomdin, *On the Accuracy of Solving Confluent Prony Systems*, SIAM J. Appl. Math. 73(1) (2013), 134–154, DOI 10.1137/110836584. [Author-hosted full paper](https://dimabatenkov.info/pdf/batenkov2011accuracy.pdf#page=5). Eq. (1.5), p. 135; Proposition 2.1, Corollary 2.2 and Algorithm 1, p. 138; determinant (2.4), p. 139; Lemma 2.6 and Theorem 2.7, p. 140.

Algorithm 1 takes 2C samples, solves a Hankel system, finds all characteristic roots with multiplicities, and solves for amplitudes. Lemma 2.6 factors the Hankel through confluent Vandermonde matrices; distinct nodes and nonzero highest coefficients give nondegeneracy. Theorem 2.7 prints an inclusive 0,...,2C range; the exact 2D comparison here relies on P1 and Algorithm 1, not silently editing that wording. No finite-field bit-operation ledger is supplied by these cited results.

Retrieval: both full publisher/author PDFs were opened through the web PDF reader; theorem, algorithm, determinant and proof pages were inspected. Direct shell byte downloads returned HTTP 403, so **no local PDF-byte hash or downloaded PDF artifact is claimed**. This is not a theorem-access blocker. Stable edition identifiers and inspected page locations are in SOURCE_IDENTIFIERS.json.

## Exact algebraic dictionary (comparison derivation)

Let m_t=DFT_M(y_t)[h] and B_{j,ell}[h]=DFT_M(b_{j,ell})[h]. The archive gives

    m_t = sum_{j,ell} B_{j,ell}[h] binom(t,ell) lambda_j(h)^t.

Set the Prony node xi_j=lambda_j(h) and coefficient

    alpha_{j,ell}=B_{j,ell}[h] lambda_j(h)^ell / ell!.

Then alpha_{j,ell}(t)_ell xi_j^(t-ell) is exactly the archived summand. This change of coordinates is invertible for nonzero nodes and p>D. Set the primary theorem's order bound d=D and full-rank case r=D. The annihilator is P_h(z)=product_j(z-lambda_j(h))^{d_j}. Solving the archived Hankel system is exactly solving its monic annihilator coefficients.

This establishes a same-field algebraic identification, not an assertion that a theorem stated over C literally has F_p as its domain. Transport to the archived split-node F_p case follows directly from the polynomial recurrence/Hankel identities and invertible factorials; complex topology and stability assertions are not transported.

## Compact exact-match / partial-match / nonmatch matrix

| Claim component | Assessment | Exact boundary and evidence |
|---|---|---|
| Polynomial-exponential channel family and annihilating recurrence | Exact algebraic match | The dictionary above identifies the archived sequence with P2 Eq. (1.5), Proposition 2.1 and Algorithm 1. This recovery mechanism is already known. |
| Unknown multiplicities from 2D clean channel values | Exact core match | P1 Theorem 3.6 already includes multiplicity recovery. Unknown multiplicities alone are not the extension. |
| Clean nondegenerate pilot | Partial match | Archive requires exact rank D in every channel and a clean 2D-row segment before any innovations. P1 also addresses lower-rank data. Do not import at-most-D completeness into this exact-D pilot. The separate ALG-006 exact-g warning remains unchanged. |
| Field and root interface | Partial match | Archive uses supplied F_p, p>N, p>D, omega and cyclic indices; the comparison derivation gives the guarded algebraic transfer. Supplied-field/root discovery and finite-field bit costs are separate. |
| Cross-channel shear parameter recovery | Nonmatch to selected theorem | Archive uses s[h]=sum_j d_j mu_j eta^(-a_jh), one M-DFT and the support index -a_j to recover rho_j=d_j mu_j. It tests positive compositions of D and the resulting P_h at every h. This coupled root-free route is additional project-specific structure. |
| Sparse forcing after the pilot | Nonmatch to selected theorem | Archive discovers raw residual modes and reconstructs the forced recurrence. The selected theorem's moment inversion does not certify that later forcing family. |
| Complete raw rejection/soundness | Nonmatch to selected theorem | Archive pays every attempted candidate and checks all N coordinates. A channel pilot fit alone cannot certify the whole raw vector. Wider-family nonmembership is not inferred from pilot failure. |
| Repeated-pole Green algebra | Partial match | Rational partial fractions and confluent exponential coefficients are established tools; the archive assembles the truncated cyclic/output identity. This is an application/corollary structure, not new repeated-pole mathematics. |
| Output and resource guarantee | Nonmatch to selected theorem | ALG-006 emits all N DFT values with its own charged transforms, support discovery, kernels, raw validation and fixed-D ledger. The selected theorem does not supply this end-to-end bound. |
| Numerical or bit-complexity claim | Nonmatch | The archive promises exact field operations under the declared word model, not numerical stability or O(N) bit complexity. Neither conclusion may be inferred from this comparison. |

Here “nonmatch” means absent from the selected result, **not absent from all prior literature**. No independent publication-level novelty conclusion has been established for the combined construction.

## Preprocessing and complete cost mapping

These are archive charges, not costs imported from the comparator:

- Field/root/length contract: p is supplied and assumed prime; omega's order is validated by the archived complete O(N) scan. Creating a suitable prime/root or a balanced factorization is not free theorem output. Root, scalar-power, inverse and index tables are paid.
- Raw-to-moment conversion: 2D direct M-point pilot DFTs cost O(DM²). One direct trace transform costs O(M²). Moments are not a free input oracle.
- Recurrence recovery: M dense D-square Hankel solves cost O(MD³) by ordinary elimination, with pivot inversions separately charged.
- Cross-channel decoding: the negative-sign trace DFT gives M rho_j at -a_j. Division by M and d_j uses nonzero field elements. No discrete-log oracle is required.
- Multiplicities: C_*=binom(D-1,g-1) ordered positive compositions, not one free guessed pattern. Every generated candidate, pole-separation test, polynomial comparison, and subsequent failed verification is charged. Straightforward degree-D polynomial construction/checking costs polynomial work per h per candidate. The stated theorem only absorbs this into a D-dependent constant.
- Amplitude recovery: per-channel confluent solves, then D direct inverse baseline transforms, are paid; elementary dense solves give O(MD³), and baseline transforms O(DM²), per relevant candidate.
- Recurrence formation and reconstruction: at most product_j(d_j+1)-1<=2^D-1 nonconstant shifted terms. Both raw passes and failed branches must remain charged. There is no uniform growing-D linear bound.
- Sparse residual discovery: O_D(M(Q+R_b)), including bounded failure; raw event expansion is also paid.
- Output: per-channel partial-fraction setup is a fixed-D solve; all baselines cost O_D(N), and R_a innovations cost O_D(Q R_a). Kernel singular case z=1 uses the binomial value. Every output write is counted.
- Inversions/storage: retain O_D(M+R_b+1) scalar inversions and O_D(N+R_b) field words. The archive absorbs inversion word costs only under its balanced polynomial-size-prime regime. This is not unit-bit-cost arithmetic.

Summing only under fixed D, Q²,M²=O(N), R_a<=R_b=O(Q), and the stated field/word assumptions recovers the archived O_D(N) conclusion. Polynomial root extraction in a generic per-channel Prony algorithm is not a free substitute for the archived trace/composition step.

## Classification and bounded next test

**Already known:** repeated-pole exponential representation, monic annihilator/Hankel recovery, confluent nondegeneracy, and recovery with unknown multiplicities. **Project-specific corollary/construction:** joining those ingredients to finite cyclic shear coupling, bounded sparse innovations, complete raw certificates and an explicit full-output work ledger. **Genuine globally unmatched extension:** not established by this pass.

Next test, if commissioned: freeze only the cross-channel trace/composition lemma and compare it against one full primary theorem for shared-parameter or multichannel confluent Prony over a finite field/cyclic group. Require matching unknown shifts/scales/multiplicities, no free factorization or discrete-log oracle, and paid moment construction. Stop after a hypothesis-and-cost map or a source-qualified nonmatch. Do not rerun finite confluence controls, expand to all ALG-006 branches, or change the accepted correctness/status based on this literature pass.

## Archived source pins

- CONFLUENT_FUSION.md: `5f31ce4af2eba202f66ce217c07feafdcf038d4d96bb557c53c3a4c7f2f686a4`.
- AUDIT_REPORT.md, §§2–3,6: `5597a056be038290dc763c846dab8a1e4a3e280a2b7b1d606c45d911b14e8ac3`.
- INTEGRATED_RESULTS.md, §1: `2d2a67a3ec1f72c32ac39b54ce853048a195e0b90ddf2543fd8d5f83c34794ae`.
- Native frozen six-field identity: `e8e7f11c55b036f1ce333d7e1ecbda79b56f21d1ac1f3f1cad7f61afeec13685`.
- Selection authority: complete_source_coverage_1453/packet/PRIORITIZED_NEXT_TASKS.json, order 5; next_unknown_sources_1207/packet/SOURCE_READINESS_10_GROUPS.json, ALG-006.
