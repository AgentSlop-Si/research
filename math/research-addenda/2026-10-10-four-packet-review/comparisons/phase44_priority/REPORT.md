# Phase44 full F8 representation: bounded originality and context audit

Audit date: 2026-10-10 UTC. The source labels its research date 2026-10-11; that label does not establish public priority. This is a model-matched comparison, not a new factorization, fusion, proof replay, ranking change, or publication decision.

## Bottom line

**Phase44 makes a real, independently validated advance over the reviewed Phase43 certificates: all eight Fourier rows are now certified, in a four-stage architecture with amplitude-allowed interstage diagonals. Its exact restricted-architecture existence theorem remains a candidate for model-specific originality, with publication priority unresolved.**

Full finite Fourier decompositions, cyclic sparse-inverse formulas, and linear-time application of a supplied cyclic solve are already established ideas. An especially close elementary comparator gives full F8 with **seven single, same-order, amplitude-allowed Green factors**. It does not give the Phase44 model: its weights are not all unit-modulus, and it has different depth and cycle orders. General diagonal/circulant factorization theorems likewise do not directly supply the twelve fixed, unit-edge cycles grouped into four unweighted sums.

No reviewed result below implies the exact Phase44 grammar. This is a conclusion about the stated hypotheses and missing conversion, **not evidence of novelty from unsuccessful searching**. It remains possible that a further elementary conversion or an unreviewed precedent settles priority.

## 1. Exact claim being compared

The accepted identity is

F8 = L S3 D2 S2 D1 S1 D0 S0 R,

where F8[r,j] = exp(-2 pi i r j / 8), and:

- S_l is exactly the **unweighted** sum of three (I-W_l,t)^(-1). “Weighted” refers to cycle edges; the certificate does not introduce independent complex coefficients on the three branches.
- Each W_l,t is a directed Hamiltonian 8-cycle with the particular fixed order recorded in `fresh_architecture.json`, all edge gains of modulus one, and holonomy different from one.
- A common seven-edge spanning tree of each three-cycle multigraph has gain one. It is not a separate fixed tree inside every branch.
- Each D_l is diag(1, exp(a1+i phi1), ..., exp(a7+i phi7)), allowing arbitrary nonzero complex entries. There are three such diagonals.
- L and R are free nonzero complex diagonals. This is an equality in the stated input/output order; no dense exterior transform is allowed or needed.

The fixed graph/gauge model has 110 real parameters. The Banach certificate selects 98 and fixes 12, solving all 49 complex projective target equations. The independent review establishes nonzero denominators and recovers all 64 Fourier entries by diagonal calibration. The decimal center is an approximation to an existing exact root, not an asserted exact algebraic parameter list.

The independently reviewed interstage amplitudes span approximately 0.00987 to 7.784. Consequently this certificate proves the amplitude-expanded model. It does not prove or disprove the existence of another solution with phase-only interstages.

Authority for these facts: local source L1 (the independent review), L2 (the source theorem), L3-L5 (inert architecture and parameter definitions). This audit did not rerun the interval proof or any uploaded program.

## 2. Within-project predecessors

| Predecessor | Established scope | Relation to Phase44 |
|---|---|---|
| Phase43, Theorem 43.4, independently reviewed | Two three-Green stages, one arbitrary nonzero complex diagonal; exactly four Fourier rows at N=8 and N=16 | Same amplitude-expanded lineage, smaller depth and target. Its complete certified boxes fail the fifth row and even fail full outer-monomial Fourier equivalence. Phase44 is an all-row extension, not a restatement of those witnesses. |
| Phase43 relative-gauge analysis | A unitary interstage diagonal is the relative gauge of two independently gauge-fixed unit-edge stages | Arbitrary amplitudes are an enlargement, not an omitted gauge variable. The distinction continues with three interstages. |
| Phase41/42 partial-row work | Local ranks and partial-row constructions, with strict unit-edge/amplitude qualifications | Local reachability near a test image never by itself establishes the Fourier target. Phase44's interval target certificate supplies the missing target-membership step at N=8. |
| Earlier changed-interface N=16 construction, L8, sections 5-6 | Explicit radix-based identity F16 = H4 H3 (I4 tensor F4) H2 H1 in a broader paired-Green grammar | It retains an explicit Fourier bank, permits separate monomial branch endpoints, and uses zero edge masks to make each Green inverse the identity. All three features differ from Phase44's twelve nonzero unit-edge cycles. It is not a Phase44 construction. |
| Earlier chirp identity and M-MULTISCALE-CHIRP review, L9-L10 | Chirp convolution gives an exact diagonally calibrated Fourier matrix; pure-shift inverse products have a separate restricted depth obstruction | The identity is a constructive baseline. The lower bound concerns products of single pure-shift Greens with Weyl gauges, not products of three-Green sums with arbitrary complex diagonals. It does not negate Phase44 or establish optimality of its depth. |

The earlier N=16 construction is important context: neither “a finite full Fourier factorization” nor the word “Green” alone distinguishes Phase44. The useful difference is **membership in its exact restricted grammar without an explicit Fourier bank or zero-mask monomial degeneration**.

References: L6 is the independent Phase43 review; L7 is the Phase41 source; L8 is `CONSTRUCTOR_SNAPSHOT.md`; L9 is the Phase15 proof certificate; L10 is the later independent review of its chirp claims. Exact paths and hashes are in `SOURCE_PINS.json`.

## 3. Elementary full-F8 construction in a nearby, larger model

This comparison is derived here from the classical chirp identity and ordinary complex polynomial factorization. It is not claimed as new research, and it does not introduce a new fusion.

Let zeta = exp(pi i/8), let P e_j = e_(j+1 mod 8), and set

D[j,j] = zeta^(-j^2),     C[r,j] = zeta^((r-j)^2).

The chirp is 8-periodic because (t+8)^2-t^2 is divisible by 16. Expanding the square gives

F8 = D C D.

Since D is unitary and F8 F8* = 8I, C^(-1) = C*/8. Thus

C^(-1) = p(P)/8,     p(z) = sum_(t=0)^7 zeta^(-t^2) z^t.

The constant coefficient of p is 1 and its degree is seven. Over the complex numbers it therefore factors, with multiplicity, as

p(z) = product_(k=1)^7 (1-alpha_k z),     alpha_k != 0.

Because p(P) is invertible, every I-alpha_k P is invertible: equivalently alpha_k^8 != 1. Hence the exact constructive identity is

**F8 = 8 D [product_(k=1)^7 (I-alpha_k P)^(-1)] D.**

Each alpha_k P is a weighted Hamiltonian cycle and every factor is a valid cyclic Green inverse. This construction uses seven single-Green stages with arbitrary edge amplitudes, a common cycle order, and no nontrivial interstage diagonals. The roots provide an exact implicit algebraic description; this observation makes no claim about optimal root synthesis, numerical conditioning, or factor-count minimality.

The counts must not be conflated: **this comparator has seven Green solves and seven sequential stages; Phase44 has twelve Green solves grouped into four sequential stages.** The comparator uses fewer solves and a larger sequential depth, under different edge restrictions. Neither count alone establishes lower runtime, practical advantage, or priority in the other model.

### Why this recipe is not accidentally unit-edge

If all roots of p had modulus one, the conjugate-reciprocal polynomial p*(z)=z^7 conjugate(p(1/conjugate(z))) would equal zeta p(z), as follows by matching leading coefficients. But the coefficient of z in p* is conjugate(zeta^(-36)) = zeta^4 = i, whereas that coefficient in zeta p is zeta zeta^(-1) = 1. Contradiction.

At least one alpha_k therefore has modulus different from one. Its holonomy has modulus |alpha_k|^8 != 1 and cannot become a unit-edge cycle by diagonal similarity. This proves the relevant mismatch for this specific recipe; it does not rule out a different unit-edge factorization.

### Why a circulant cannot simply be renamed a Green inverse

The chirp C has dense inverse C*/8. A single Hamiltonian-cycle Green has inverse I-W with only two nonzeros per row. Invertible exterior monomial scalings and permutations preserve the inverse zero pattern. Therefore this C cannot be a single such Green even with those exterior freedoms. A sum of three Greens can have a dense inverse, so this observation is only a warning against the substitution, not an obstruction to Phase44.

The exponent identities and conjugate-reciprocal contradiction are recorded in `EXACT_COMPARISON_CHECKS.json`. These are newly written exact integer checks, not numerical source execution.

## 4. Primary-source comparison

### 4.1 Cooley-Tukey and chirp convolution

Cooley and Tukey derive exact radix decompositions and the repeated binary schedule; F8 is consequently an ordinary three-radix-2 example. This already settles the broad existence of a short, exact full-F8 factorization. It does not express the butterfly stages as the particular Green sums required here. See their original 1965 paper, pp. 297-300, especially equations (6)-(12) and (17)-(22), [primary paper scan](https://www.ece.ucdavis.edu/~bbaas/281/papers/CooleyTukey.1965.pdf).

The chirp identity is documented explicitly by [AMD's rocFFT design document](https://rocm.docs.amd.com/projects/rocFFT/en/docs-5.7.1/design/bluestein.html), “Bluestein Algorithm.” The original Bluestein paper has [DOI 10.1109/TAU.1970.1162132](https://doi.org/10.1109/TAU.1970.1162132); its publisher text did not render, so this audit does not attribute an uninspected theorem to that paper. Section 3 above proves the precise even-length cyclic specialization used here directly.

### 4.2 Diagonal/circulant and sparse-cycle factorization

Schmid, Steinwandt, Muller-Quade, Roetteler and Beth (2000) establish diagonal/circulant product existence over complex numbers as a case of their field theorem. The [authors' institutional record](https://www.microsoft.com/en-us/research/publication/decomposing-matrix-circulant-diagonal-factors/) verifies this statement; only that abstract was inspected. It specifies neither Phase44's four stages nor unit-edge Green sums.

Huhtanen and Peramaki (2015) are closer. Their [author-hosted paper](https://math.aalto.fi/~mhuhtane/manu.pdf), Proposition 2.5, Theorems 2.7, 2.9, 2.10 and 4.3, treats linear-cost sparse-cycle inversion, explicit inverses of I+DS, diagonal reduction to I+alpha S, and generic matrix factorization into n-1 cyclic-bidiagonal factors plus a diagonal, yielding at most 2n-1 alternating diagonal/circulant factors. Their cyclic-factor parameter alpha is unrestricted complex; the generic theorem is not a membership certificate for the specific Fourier matrix. It supplies neither four three-Green stages nor the twelve fixed orders nor unit-edge gains. Its inversion machinery is a direct predecessor for the individual Green primitive, not an established derivation of Phase44. Publication: [DOI 10.1007/s00041-015-9395-0](https://doi.org/10.1007/s00041-015-9395-0).

The missing step is a **model-preserving compilation**: convert the preceding factors into exactly four sums of three unit-edge resolvents with the prescribed cycles, absorbing only legal diagonals and retaining all pole guards. Neither citing genericity nor replacing a general circulant with a single Green supplies that step.

### 4.3 Green/quasiseparable inverse representations

Boito and Eidelman's [primary preprint](https://arxiv.org/pdf/2308.02701), introduction and Theorems 4.3-4.4/5.6-5.8, studies quasiseparable representations of inverses of banded matrices with linear complexity. This is appropriate background for structured inverse storage and application. Its use of “Green matrix” denotes a rank-structured class, not exactly a weighted Hamiltonian-cycle resolvent, and it does not assert Fourier membership in four three-resolvent stages. Publication information is verified on the [arXiv record](https://arxiv.org/abs/2308.02701), DOI 10.1016/j.laa.2024.04.034.

### A structural check on any proposed conversion

For unitary W with I-W invertible, G=(I-W)^(-1) satisfies G+G*=I: indeed G*=-(I-W)^(-1)W=I-G. Therefore every **unweighted** three-unit-Green stage satisfies S+S*=3I. This is an elementary consequence of the present definitions. A general circulant or arbitrary sparse-inverse factor does not come with this property. Any proposed stagewise substitution must account for it, as well as graph orders and edge moduli. This necessary property is not asserted sufficient and is not promoted as a separate novelty claim.

## 5. Claim-level disposition

| Claim | Assessment | Reason |
|---|---|---|
| The Phase44 frozen architecture contains exact full F8 up to exterior nonzero diagonals | **Established**, relying on the independent interval review | All projective equations and nonzero guards are certified. This is not merely a numerical fit. |
| This adds full-target membership beyond Phase43 | **Established project advance** | Phase43 had four-row targets and rigorously failed full Fourier in its boxes. |
| Phase44 merely restates the earlier N=16 paired-Green construction | **Incorrect** | Zero masks, per-branch monomial endpoints and an explicit Fourier bank belong to the earlier grammar. |
| A classical elementary construction already proves full F8 in a nearby Green model | **Yes** | Section 3 gives seven same-cycle, amplitude-allowed single Greens. |
| The reviewed elementary or primary results imply this exact four-stage unit-edge, fixed-order architecture | **Not established** | Each lacks a required model-preserving conversion. No claim of impossibility of such a conversion is made. |
| The exact architecture is literature-first or publication-significant | **Unresolved** | This bounded comparison is not an exhaustive priority review or significance assessment. |
| The O(N) cyclic solve or fixed-size online representation is new by itself | **Unsupported** | Individual sparse-cycle inversion and finite exact Fourier representations have direct precedents. |
| Phase-only interstages, full F16, a uniform family or sub-N-log-N algorithm follow | **No** | Those are different unresolved statements. At fixed N=8, asymptotic notation cannot establish an FFT improvement. |
| Four stages or twelve solves are optimal, fastest, or more stable than FFT | **Unproved** | No matching lower bound, cost-normalized comparison, or stability theorem is supplied. |

## 6. Remaining priorities and stopping boundary

1. **Exact-grammar priority:** If pursued, investigate a concrete conversion from chirp/sparse-cycle factorizations to the twelve fixed unit-edge cycles. Demand a written identity or a theorem with matching restrictions. Search absence alone remains irrelevant to novelty.
2. **Analytic understanding:** Determine whether the certified root admits a recognizable algebraic or trigonometric description. The interval existence theorem is already valid; a closed-form description would clarify structure and comparisons.
3. **Model separation:** Independently study the smaller phase-only interstage architecture if that is the actual target. Setting the current log-amplitudes to zero and observing failure is not a nonexistence proof.
4. **Scaling only with evidence:** A full F16 certificate or a proved uniform lifting rule would be a further target, separate from the completed F8 result. Local rank alone does not supply either. Account for synthesis, precision and conditioning before any computational claim.

Recommended wording: **“An independently interval-certified full 8-point Fourier representation in a fixed four-stage architecture of three unit-edge Hamiltonian-cycle Green resolvents per stage, with arbitrary nonzero complex interstage and exterior diagonals. This advances the project's earlier partial-row certificates; model-specific publication priority is undetermined.”**

The bounded assessment stops here. No parameters were fitted, no source program was executed, no new fusion was constructed, and no external files or rankings were changed. Sources and access limits are pinned separately.
