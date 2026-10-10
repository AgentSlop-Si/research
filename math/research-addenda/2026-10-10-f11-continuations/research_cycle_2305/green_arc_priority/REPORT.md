# Phase 43 arc-rank bound: bounded claim-level comparison

10 October 2026 UTC. Target: Theorem 43.1 only, with boundaries separating Theorems 43.2–43.4. Source report is dated 11 October 2026. No ranking, Catalogue, repository, or other external record was changed.

## Decision

**Phase 43.1 is a correct specialized rederivation of an already accepted project theorem, not an identified new model or constant.** Catalogue row M-ROUTED-FIELD, its original SEALED_PROOF, its column-two EXTENSION_AUDIT, and REVIEW-08 already establish the identical bound

`N <= r(r+1)^r`

for a strictly larger class: independently endpoint-routed inverses of arbitrary invertible matrices with at most two nonzeros per column, over every field containing an element of exact order N. The older proof uses the same selected-row projective-class/refinement/Vandermonde argument, explicitly including consecutive frequency rows and cyclic wrap. It permits zero edge and endpoint weights as well.

The useful Phase43 contribution within this comparison is a concise Hamiltonian-cycle coordinate proof: explicit prefix products, half-open arc classes, and the common-holonomy identification of the two extreme classes. That is expository value. No additional theorem, generality, constant improvement, field extension, or independent discovery count is warranted for 43.1 relative to M-ROUTED-FIELD. This conclusion is project-local and does not certify worldwide priority of the older theorem or establish who first derived either text.

## 1. Exact reduction, including fields and outer monomials

Write the Phase43 shift as `W_s = D(w_s) P_s`, with P_s a Hamiltonian-cycle permutation in the selected convention. Set

`Q_s = I-W_s = I + (-D(w_s)) P_s`.

This is already in the original M-ROUTED-FIELD denominator grammar `D_s+E_s P_s`, before its broader column-two extension. Each column has at most two nonzeros. `W_s^N=h_s I` and `h_s != 1` make Q_s invertible. Set `r=q`, `L_s=alpha_s I`, `R_s=I`. Arbitrary scalar coefficients, including zero, are allowed endpoint weights in the older theorem.

If full Fourier equivalence is `F_N=A S B` for invertible monomial A and B, then

`F_N = sum_s (alpha_s A) Q_s^(-1) B`.

Both endpoint factors remain permutation-contained. This explicitly includes independent outer row and column permutations and arbitrary invertible complex diagonal scalings; no unitary-only assumption is needed for this exact equality reduction. Even a zero coefficient yields an allowed zero endpoint matrix, but it does not make a singular inverse meaningful. Every retained inverse must exist.

For a partial-row target, extend the chosen output-row reordering and nonzero row scalings to full monomial maps. The resulting equality is needed only on the selected `k=q+1` rows. The older headline states a full Fourier representation, but its structural lemma and Fourier-obstruction proof use no other rows. Its SEALED_PROOF lines 135–187 explicitly give the same rank-one classes, common refinement, Vandermonde test, and wrapped consecutive-row discussion. Thus the partial-row conclusion is an immediate reading of that prior proof, not a new structural ingredient hidden by its full-matrix headline.

The Phase43 report is stated over C. The accepted Phase43 review observes that its proof works over any field K with an exact-order-N element omega. The older theorem already has precisely that field scope. In positive characteristic, an exact-order-N root entails characteristic not dividing N. Neither proof assumes arbitrary Fourier minors are nonzero at composite N. Only consecutive frequency rows are used; scaling columns by `omega^(r0*j)` handles the starting frequency and wrap.

### Guards that must remain visible

- Phase43's displayed prefix formula divides by individual nonzero edge products beta_b and uses nonzero h to merge the wrap classes. Its own proof is not a zero-edge proof.
- M-ROUTED-FIELD uses deletion of constraint columns and rank-nullity. It covers zero edge weights and singular endpoint masks without dividing by edge gains. This is strictly broader, not a defect in Phase43.
- Both require legal inverses. For the Phase43 Hamiltonian shift, h != 1 is the exact nonpole condition. An `alpha=0` branch may be omitted, but `0*(undefined inverse)` is not defined.
- Nonzero Fourier nodes and nonsingular outer scalings preserve the needed ranks. Cancellation between branches can only decrease the rank on a common class, so no genericity or coefficient noncancellation hypothesis is required.
- Neither argument covers dense outer transforms, a product of sums, or an interstage diagonal simply by calling it an outer gauge.

## 2. Claim-by-claim map

| Phase43 component | Closest verified project precedent | Disposition |
|---|---|---|
| `G[a,b]=(beta_a/beta_b) h^[a<b]/(1-h)` | Earlier cycle Green expansion and arc factorization in M-SEPARATION; elementary identity from `W^N=hI` | Standard exact formula, useful coordinate presentation |
| At most k projective directions on k selected rows | M-ROUTED-FIELD SEALED_PROOF structural lemma, lines 49–133 | Earlier result is stronger: exactly k independent nonzero directions before masks, with possible zero columns |
| Arbitrary cycles/edge magnitudes/scalar coefficients | Original inverse `D+EP` grammar, lines 23–44 | No new model coverage; nonzero Hamiltonian edges form a subcase |
| Independent outer row/column monomials | Older independently routed branch endpoints, lines 135–154 | Already allowed branch by branch; includes the outer-equivalence contract |
| At most `k^q` common cells; rank <=q per cell | Older Fourier obstruction, lines 156–180 | Same elementary refinement and rank-subadditivity mechanism |
| Consecutive Fourier rows are full spark | Older lines 168–187; ordinary Vandermonde determinant | Classical ingredient, including composite N and wrap |
| `N<=q(q+1)^q`, q=3 cutoff 192 | Older exact same formula, lines 7–17 and 158–180; Catalogue row 33 | Identical constant after `r=q`; no increment |
| Matching only q+1 rows suffices | Older proof consumes only those rows and explicitly handles consecutive shifts | Useful explicit restatement, already supplied by the prior proof |
| `q=Omega(log N/log log N)` | Older lines 193–205 | Already stated exact-field branch-count corollary |
| Removing unit-modulus restrictions from Phase41 | M-ROUTED-FIELD already allows arbitrary field coefficients | Broader than Phase41 alone, but not broader than current project coverage |
| Two-layer relative gauge and finite four-row certificates | Separate Phase43.2–43.4 models | Not classified as duplicates by the 43.1 comparison; remain separately scoped |

The underlying source bytes are pinned in SOURCE_PINS.json. Both decisive M-ROUTED-FIELD originals match their recorded historical SHA-256 values, rather than merely being attribution-normalized exports. Catalogue row 33 and REVIEW-08 retain their proved-scoped disposition. No fresh replay of their historical exhaustive checks was needed or claimed for this theorem-to-theorem reduction.

## 3. Other project precedents: constants and model differences

### M-SEPARATION: stronger full-target asymptotics over C

For q independently ordered Hamiltonian Green branches, M-SEPARATION provides a common `m x m` rectangle of branch-sum rank at most q, where `m=floor(N/2^d)` and d is the number of distinct branch order pairs, `d<=q`. Against a normalized complex flat unitary target it gives `m^2<=Nq`. Using d=q is the weakest universal instance; fewer distinct templates may strengthen it.

Full exact outer-monomial equivalence is covered by absorbing the endpoint maps into the branches and comparing the resulting exact sum with normalized F_N. The spectral proof is applied to the genuinely flat Fourier target after that absorption. This does not transport an unchanged approximation-norm floor through arbitrary nonunitary scaling of an approximately matched target.

For the universal d=q instance, the largest integer N that can satisfy the inequality is `q*4^q+2^q-1`. This is only arithmetic restatement of the recorded inequality: put t=2^q, k=floor(N/t); feasibility requires `k^2<=q(t*k+t-1)`, which forces `k<=qt`. It is not a new theorem or fusion. Hence the old full-target obstruction already forces `q=Omega(log N)` over C.

### F018: more general separator supports

The current accepted F018 refinement, Theorem 2A of FINAL_THEOREMS, gives `N<=p*q*9^q+p(3^q-1)` for q independently routed inverse branches whose bipartite support lifts have weighted half-separators of size p. For invertible column-two denominators p=2 suffices. Thus its full-target bound is `N<=2q*9^q+2(3^q-1)`, again implying `Omega(log N)` branches for exact complex flat targets.

Do not compare Phase43 only with obsolete `36^q` or p=3 snapshots: current Catalogue overlays and REVIEW-07 retain `9^q` and p=2. For Hamiltonian cycles, M-SEPARATION is a more useful full-target comparison than this broader separator theorem. Neither analytic theorem by itself supplies the field-general partial-row contract; M-ROUTED-FIELD supplies that exact match.

| q | Phase43 = M-ROUTED-FIELD ceiling | M-SEPARATION full-complex ceiling, d=q | F018 full-complex ceiling, p=2 |
|---:|---:|---:|---:|
| 1 | 2 | 5 | 22 |
| 2 | 18 | 35 | 340 |
| 3 | 192 | 199 | 4426 |
| 4 | 2500 | 1039 | 52648 |
| 5 | 38880 | 5151 | 590974 |
| 6 | 705894 | 24639 | 6378748 |
| 7 | 14680064 | 114815 | 66965938 |
| 8 | 344373768 | 524543 | 688760656 |
| 9 | 9000000000 | 2359807 | 6973608166 |

These are necessary ceilings, not existence or optimality claims. Phase43 has the better displayed small-q full-target ceiling for q=1,2,3 against M-SEPARATION, but those ceilings were already in M-ROUTED-FIELD. Against F018 alone the crossover occurs later. Treating only that comparison as the strongest known project obstruction would be misleading.

### Nearby but nonidentical branches

- Phase41's two-unit-edge-cycle theorem excludes full Fourier equivalence for N>8. At q=2 it is stronger than the general 18 ceiling but assumes unit-modulus gains and uses a different circle/ratio argument. Phase43 broadens that specific model at the cost of a weaker constant; the earlier field theorem already made that broadening.
- F014's much larger lower counts concern ordered products built from a single fixed Weyl pair, with carefully restricted endpoints. Its coefficient/Hankel ranks cannot be imported into arbitrary single Hamiltonian inverses or branch-dependent generators.
- C05's earlier large one-layer thresholds are historical, and the current correction-compatible separator extension is broader. Its original-author-file gap has been closed by the later Catalogue addendum; the old separator-priority report's missing-locator wording is not a current absence claim.
- C02's endpoint cut-rank budget and C07's inverse-rectangle/interface budgets provide additional rank tools under their own hypotheses. They do not turn 43.1 into a product theorem or a circuit-operation bound.

## 4. Primary literature: what is classical, and what was actually checked

### Inverse/Green/quasiseparable rank structure

Boito and Eidelman, *Computation of quasiseparable representations of Green matrices*, arXiv:2308.02701v1, Section 2, Theorem 2.1 and equations (2.1)–(2.3), PDF p.3, state the Asplund band-inverse rank characterization and quasiseparable generators. Their introduction identifies older structured-inverse work. This establishes the classical rank-structured background; it is not an inspected statement of the q-branch Fourier inequality. A cyclic bidiagonal denominator is one-sided banded in its cycle order, but calling a matrix generically quasiseparable does not automatically grant the exact k-projective-direction lemma. The common holonomy in Phase43 or the inverse-column-two proof is the relevant extra structure. [Primary preprint](https://arxiv.org/pdf/2308.02701)

Vandebril and Van Barel, *A short note on the nullity theorem*, TW397 (2004), Section 3, Corollary 1, printed p.5/PDF p.7, give the swapped-complement rank identity used by separator arguments and credit Fiedler–Markham. It requires invertibility of the whole matrix, not every principal block. This is a classical exact rank ingredient; the original 1984/1986 papers were not reopened here. [Institution PDF](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf)

Chandrasekaran, Epperly and Govindarajan, *Graph-Induced Rank Structures and their Representations*, arXiv:1911.05858v3, Section 2.1, Propositions 2.1–2.3, pp.5–8, preserve complementary block ranks under inversion and give sum/product rank algebra for a shared graph. Those results support the classical mechanism. They are not the same statement as unrelated branch routings plus a Fourier common-refinement count; a shared-graph product law also does not prove that products remain single cycle inverses. [Primary preprint](https://arxiv.org/pdf/1911.05858v3)

### Exact projective-direction antecedent

Zaslavsky, *Biased Graphs IV: Geometrical Realizations*, Section 2.1, author PDF pp.8–10, defines switched incidence representations and a contraction map that sends coordinate vectors in each balanced component to its component direction, or to zero. Theorem 2.1 and equation (2.2) give the associated rank/cycle-gain structure, including the cycle determinant factor `1−holonomy`. This is a direct classical antecedent of the componentwise direction mechanism underlying the older inverse-row lemma, rather than merely a vague similarity to low rank. Its inspected pages do not state the Fourier q-sum bound. [Author PDF](https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf)

Nelson and van Zwam, *On the existence of asymptotically good linear codes in minor-closed classes*, Section 2, PDF pp.4–5, define frame matrices by at most two nonzeros per column and describe their graph representation. They explicitly discuss the GF(2) singleton issue. The project’s support/rank-nullity proof avoids that gain-label convention and therefore preserves its stated exact-field domain. The frame class itself is established terminology. [Author PDF](https://www.math.uwaterloo.ca/~apnelson/asympgood.pdf)

### What the Phase43 citations do and do not support

The Phase43-linked DOI `10.1007/s11075-024-01809-9` is Ben-Artzi, Eidelman and Fishelov's *Numerical solution of the boundary value problems for the biharmonic equations via quasiseparable representations*, published online in 2024. Section 3 provides scalar quasiseparable background in a PDE discretization application. It is relevant background but less direct than the structural/frame references above; it is not a located Fourier-sum obstruction. [Published article](https://link.springer.com/article/10.1007/s11075-024-01809-9)

Ailon's 2013 preprint proves an arithmetic lower bound for a layered circuit restricted to unitary 2x2 gates. That model differs from a Green inverse-sum representation; it cannot supply a missing cost lower bound for 43.1. No conclusion about an unrestricted exact-complex arithmetic model is imported. [Primary preprint](https://arxiv.org/abs/1305.4745)

The finite geometric inverse identity, rank subadditivity, common partition refinement, pigeonhole count, and consecutive-row Vandermonde determinant are elementary established machinery. The current comparison does not assign their general invention to this project. It also does not claim that any one external primary source contains the exact assembled Fourier restriction theorem. The decisive exact match here is the already accepted project source.

## 5. Keep the two-layer results separate

This report neither downgrades nor awards novelty to Phase43.2–43.4. The independent Phase43 review separately accepted the relative-gauge identity, modular local ranks, and exact interval existence for four rows at N=8 and N=16 in the expanded complex-interstage-diagonal model. Those interval fixtures are not examples of one sum of q Green inverses. Expanding a product gives products of inverses, which need not be individual Hamiltonian-cycle Green inverses.

The verified boxes fail the next row, and their cross-ratio modulus witnesses exclude full outer-monomial DFT equivalence throughout those specific boxes. N=32 target existence remains numerical only. The original two-layer unit-edge gauge has unit-modulus D; arbitrary complex D is a larger architecture. None of these facts changes the old/new identity of the one-layer bound, and none gives a full DFT or asymptotic FFT speedup.

## 6. Provisional significance and safe carry-forward wording

Suggested characterization:

“Phase43.1 supplies a short arc-coordinate proof of the Hamiltonian-cycle specialization of the project's already accepted field-general column-two inverse-sum obstruction. Its exact ceiling, endpoint allowance, consecutive-row mechanism, and asymptotic branch count were previously established in M-ROUTED-FIELD. The broader theorem’s external priority remains unresolved.”

For a manuscript, cross-reference that prior project theorem and its proof rather than presenting the same bound as a new independent discovery. The bounded external reading supports classical attribution of ingredients but cannot certify worldwide originality, optimality, publishability, or attribution chronology. No rank change is made here.

The useful content is a model-specific impossibility statement. A q-term representation count is not a lower bound on scalar arithmetic operations. Even if separate evaluation costs O(Nq), shared evaluators or different architectures need not pay that cost; products, parameter preparation, bit complexity, and unrestricted algorithms remain outside the conclusion.

## 7. Evidence scope and stopping point

The comparison inspected the Phase43 theorem and full independent review; the decisive M-ROUTED-FIELD original proof and extension; current Catalogue records; relevant REVIEW-07/08 sections; M-SEPARATION; current F018 Theorem 2A; Phase41's stated theorem/proof; and the listed primary passages. Historical computational certificates were read as accepted dependencies, not rerun. No uploaded research code was executed, imported, compiled, or parsed as executable code.

External work was bounded to four initial searches and seven relevant primary sources. A requested arXiv HTML version returned 404; the openly provided primary PDF was read instead. This was an ordinary missing representation, not an access-denial bypass. No denied route was retried, and no paywall or security boundary was bypassed. Unrelated branching-program search results were not used. No copyrighted article body is bundled. The completed exact project reduction is the stopping condition; a worldwide priority search is not attempted.
