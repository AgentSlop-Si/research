# ALG-036: bounded primary-source comparison for the exact complex Gaussian optimizer

Date: 20 October 2026 UTC. Status: frozen comparison candidate, ready for independent source review. No worldwide novelty claim. No external service or repository was changed.

## Result and disposition

None of the theorem statements verified in the primary full texts listed below subsumes the accepted **all-finite-radius N=3, d=2 proper-complex Gaussian optimizer classification**. This is a bounded nonmatch, not proof that no earlier result exists. The important remaining access lead is König–Koldobsky's *On the maximal measure of sections of the n-cube*: its primary chapter was not successfully retrieved, so its precise scope is not cleared here. The original Oleszkiewicz–Pełczyński paper's publisher abstract was read, but its full text was not successfully retrieved; its volume theorem is additionally stated explicitly in the accessible Glover–Tkocz–Wyczesany primary paper.

The named mathematical optimizer task is accepted by the separate fresh review. This comparison does not review or reopen that proof. It does not close ALG-036's broader recorded historical-attribution task, which concerns the Gaussian measurement-rank barrier and model-matched norm, accuracy, measurement, and cost comparisons beyond the already completed qualified HIKP comparison. These are different tasks. The present comparison can be completed at its bounded source scope while that broader gate remains open.

## 1. Exact result being compared

Let P=I-uu* be a complex orthogonal rank-two projector on C^3, with ||u||_2=1, and let Z have law CN(0,P). The nonsingular CN(0,I_2) density is π^(-2)exp(-||z||_2^2); each complex coordinate has variance one. For a=r^2>0, define F_a(q)=Pr(max_j|Z_j|≤sqrt(a)), where q_j=|u_j|^2. Coordinate phases and permutations are immaterial.

The accepted optimizer is q=(0,1/2,1/2) below a unique a_* in (1/2,2), q=(1/3,1/3,1/3) above it, and exactly those two types at a_*. The block value is B(a)=(1-e^(-a))(1-e^(-2a)); the crossing with the symmetric value is unique and transverse. No other normal type is a maximizer. Here q denotes **normal weights**, not projector leverages: P_jj=1-q_j.

The comparison relies on the independently accepted structural reduction and scalar completion, not a finite radius census. The accepted mathematical proof is a separate dependency and is not reproduced in this comparison packet. The classification is stated here for centered probability; centering/attainment are inherited results. We do not add an unreviewed classification of every possible translating center.

## 2. Three exact comparison bridges

These are direct normalization calculations for interpreting the literature, not newly attributed external theorems.

1. **Weighted polydisc section.** If H=u^⊥ and D is the unit complex disc, then

   F_a(q) = a^2 π^(-2) ∫_(D^3∩H) exp(-a||w||_2^2) dw.

   Hence F_a(q)/a^2 tends as a↓0 to the normalized unweighted section volume A_3(u)=π^(-2)vol_4(D^3∩H). An unweighted volume optimizer alone does not order these differently weighted integrals at every positive a. Nor does pointwise convergence alone supply a radius interval uniform over nearby competing normals.

2. **Realification.** In standard real-Gaussian coordinates X=sqrt(2)(Re Z,Im Z), the event is the intersection of three circular cylinders, X_(2j-1)^2+X_(2j)^2≤2a. The admissible supports are complex-linear, equivalently J-invariant, real four-planes in R^6. This is not a real cube section by a real hyperplane. Replacing each disc by a square changes the objective; no real cube optimizer transfers verbatim.

3. **Planar product-density formulation.** Let Y_j be independent complex random variables with density h_a(z)=e^(-|z|^2)1_(|z|≤sqrt(a))/[π(1-e^(-a))]. If g_(a,u) is the planar density of Σ_j conjugate(u_j)Y_j, unitary coarea gives

   F_a(q)=π(1-e^(-a))^3 g_(a,u)(0).

   Thus an applicable exact product-measure theorem must cover compactly supported **planar radial truncated Gaussians**, three weights, and all truncation parameters. A real one-dimensional truncated Gaussian theorem does not automatically provide this result. This is the precise target for further inspection of the inaccessible chapter and related product-measure papers.

## 3. Verified primary comparisons

### S01. Glover–Tkocz–Wyczesany, *Stability of polydisc slicing* (2023)

Theorem 1, equations (3)–(4), printed pp. 1166–1167, takes a sorted nonnegative unit normal v in R^n and A_n(v)=π^(1-n)vol_(2n-2)(D^n∩v^⊥). Its upper bound is

A_n(v)≤2-min{10^(-40)||v-(e1+e2)/sqrt(2)||_2, (Σv_j^4)/76}.

This gives quantitative **Lebesgue-volume** stability, with the two-coordinate normal as the finite-dimensional extremizer. The paper's additional Gaussian extremizer is an n→∞ normalized-sum limit, not a Gaussian radial weight on a fixed section. In the accepted earlier local work, this theorem was borrowed for a separately proved small-radius weighted transfer. It supplies neither the exact maximal block interval nor the fixed-dimension all-radius transition/equality classification.

Primary full text: https://eprints.whiterose.ac.uk/221836/1/Mathematika%20-%202023%20-%20Glover%20-%20Stability%20of%20polydisc%20slicing.pdf

### S02. Oleszkiewicz–Pełczyński, *Polydisc slicing in C^n* (2000)

The publisher abstract states 1≤π^(1-n)vol_(2n-2)(D^n∩H)≤2 for complex codimension-one H, with the upper equality exactly at normals e_j+σe_k, |σ|=1. This is the unweighted ancestor of S01. It matches the a↓0 objective, not the weighted finite-a optimization. Original full text remains an access gap in this pass; S01 explicitly records the statement and equality cases. We do not claim to have inspected the original proof.

Publisher: https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/142/3/111809/polydisc-slicing-in-n

### S03. Barthe–Guédon–Mendelson–Naor (2005)

*A probabilistic approach to the geometry of the ℓ_p^n-ball*, §3.3, Theorem 10, reprint p. 30, states for any real k-plane E⊂R^n and r>0:

γ_E(E∩rB_∞^n)≤γ_k(r sqrt(n/k) B_∞^k).

The adjacent text records optimality when k divides n. This is a real-cube Gaussian probability envelope, not an optimizer classification when divisibility fails. Theorem 9 gives a real-cube normalized monotonicity/lower-bound statement, also not the required complex optimizer. Bridge 2 prevents replacing its cube by the polydisc without proof. Its Brascamp–Lieb mechanism is relevant prior methodology; no adaptive measurement or computational cost model is part of these theorem statements.

Primary full text, arXiv:math/0503650v1: https://arxiv.org/pdf/math/0503650v1

### S04. Zvavitch, *Gaussian measure of sections of dilates and translations of convex bodies* (2008)

The author manuscript §3, pp. 5–6, explicitly treats real B_∞^n and shows that the two-coordinate-normal section ceases to maximize for sufficiently large dilates, using the better inradius of the fully symmetric section. This is relevant prior art for **radius-dependent Gaussian section geometry**. It is not a classification of all maximizing sections for every radius, does not assert one crossing with only two optimizer types, and does not concern complex polydiscs. Accordingly, even the qualitative idea of competing small/large-radius geometries must not be described as unprecedented.

Primary full text: https://www.math.kent.edu/~zvavitch/zvavitch_sections_translations_dilates.pdf

### S05. Chasapis–Singh–Tkocz, *Haagerup's phase transition at polydisc slicing* (2024)

In arXiv v2, Theorem 2 (p. 4) determines the sharp negative-moment comparison for sums of independent vectors uniform on S^3⊂R^4. For -3<q<0, the best normalized L_q constant is the two-summand value for q≤-2 and the Gaussian-limit value for q≥-2. At q=-2, §1.3 recovers unweighted polydisc section volume. The varied parameter is a **moment exponent** and one competitor is an infinite-summand limit. Neither is the fixed-three-coordinate, finite-radius Gaussian probability problem. This named phase transition therefore does not subsume the accepted a_* theorem.

Primary full text, arXiv:2206.01026v2: https://arxiv.org/pdf/2206.01026v2

### S06. Jakimiuk–König, *Maximal sections of the unit ball of ℓ_p^n(C) for p>2*

In arXiv v2 (14 March 2025), Theorem 1.1 proves that fully symmetric normals beat two-coordinate normals for sufficiently large n at each fixed p>2. Theorem 1.2 proves two-coordinate maximality for very large p and n small relative to p. These are complex **unweighted ℓ_p-ball volume** statements. Their variable shape exponent and dimension are not the Gaussian weight parameter a on D^3∩H. Thus they are relevant to competing normal types but not an all-radius theorem for the present model.

Primary full text, arXiv:2402.12552v2: https://arxiv.org/pdf/2402.12552v2

### S07. Eskenazis–Nayar–Tkocz, *Gaussian mixtures: entropy and geometric inequalities* (2018)

Definition 1 and Theorem 2 in arXiv v3 characterize centered Gaussian scale mixtures; pp. 24–25 derive complex ℓ_q-volume comparisons for 0<q<2 using such mixtures. The positivity of every nondegenerate Gaussian scale component implies that a nonzero mixture cannot have compact support. Consequently the h_a in Bridge 3 is not a Gaussian scale mixture. The complex section application is unweighted volume for ℓ_q-balls, not all-radius weighted polydisc optimization. The word Gaussian in the representation is not a match of the objective.

Primary full text, arXiv:1611.04921v3: https://arxiv.org/pdf/1611.04921v3

### S08. Bennett–Carbery–Christ–Tao, *The Brascamp–Lieb inequalities: finiteness, structure and extremals*

Definition 2.1 and Proposition 2.8 (pp. 9, 12) give constant one for coisometries B_j satisfying Σp_j B_j*B_j=I. For an isometric complex frame V, normalized nonzero rows B_j=v_j/sqrt(P_jj) are real rank-two coisometries. Disc-truncated Gaussian inputs yield the inherited leverage-product bound. This is a direct borrowed inequality, not a new general comparison theorem. Importantly, Example 1.6 and Proposition 2.8 explicitly credit **Ball and Barthe** for the geometric theorem; BCCT is a verified source and reproof. Optimizing the unattained nondivisible envelope is additional work, not settled by its constant-one conclusion.

Primary full text: https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf

### S09. Valdimarsson, *Optimisers for the Brascamp-Lieb inequality* (2008)

Definitions 8–9 (preprint p. 10), Theorem 12 (p. 12), and the L1 extension (pp. 15–16) classify equality inputs through independent factors and Gaussian factors on the dependent component. These cover the bounded-support disc inputs used in the inherited equality argument. In this application, nonzero dependent components cannot carry those compactly supported inputs; further complex-line reasoning yields the phase-block classification. This is an attributed specialization of a published theorem. Equality in an upper bound does not identify the maximum when the upper bound is unattained, so the exact N=3,d=2 optimizer remains additional to this checked theorem.

Primary full text: https://uni.hi.is/siv/files/2017/07/optimisers.pdf

### S10. Fodor–González Merino, *Central diagonal sections of Gaussian n-cubes*

The full arXiv:2511.01504v2 HTML defines real product probability densities proportional to exp(-b||x||²) on [-1,1]^n, then evaluates the n→∞ limit for the single diagonal normal family in Theorem 1.1. This recent continuation is directly relevant to weighted real-cube sections, but it is neither complex-disc geometry nor maximization over all normals at fixed n=3. The retrieved HTML abstract and main theorem differ in a leading numerical factor; no coefficient or historical threshold from that page is used here. Its summary of König–Koldobsky is a useful lead, not direct verification of that earlier chapter.

Primary full text: https://arxiv.org/html/2511.01504v2

## 4. Unresolved primary access lead, not a cleared nonmatch

### G01. König–Koldobsky, *On the maximal measure of sections of the n-cube*

The citation is Contemp. Math. 599 (2013), 123–155, DOI 10.1090/conm/599/11907. The DOI, AMS chapter-PDF candidate, and AMS volume pages returned tool retrieval errors. An author publication-directory attempt also failed. The accessible research-profile abstract advertises Gaussian-type product measures, and a section/projection survey identifies this as an important real-cube Gaussian lead. Those secondary indications were used **only to discover the lead**. They do not establish its exact hypotheses or rule out relevant additional results.

The next meaningful check is the primary theorem for planar radial product measures, if any, against Bridge 3, including parameter range and full equality cases. No author contact, access purchase, sign-in, or other external mutation was attempted. Absence of retrieved full text is not a proof of nonexistence or nonmatch.

DOI locator: https://doi.org/10.1090/conm/599/11907

## 5. Selected historical-attribution gate

Historical attribution / primary-source comparison remains distinct from accepted correctness. Unresolved attribution and model-matched novelty **beyond** the qualified HIKP comparison are preserved. The earlier named HIKP v2 Theorems 4.9/6.1 comparison was accepted as a norm/measurement/cost certificate nonmatch; it should not be rerun or treated as newly unresolved.

The present N=3,d=2 theorem concerns a fixed Gaussian projector probability. It supplies neither a primary-source equivalence for the original transcript-only adaptive rank barrier nor an arithmetic/runtime lower bound. The higher-dimensional/changing-dimension, arbitrary nonhomogeneous sphere-prior, every-fixed-input, implementation, and information-model qualifications remain distinct. A fixed-dimensional optimizer improvement cannot clear them by implication.

Recommended disposition: mark only the named all-radius N=3,d=2 mathematical optimizer scope complete according to its separate acceptance; record this bounded source comparison and G01 access gap; retain broader attribution and whole-owner status/priority unchanged. No claim of worldwide originality, historical priority, or complete literature clearance follows.

## 6. Review boundary and reproducibility

The source register gives titles, version/edition, exact theorem locations, URLs, access class, and disposition. It contains no purported PDF hashes: primary bodies were inspected through the web tool, not successfully archived as local PDFs. Reopening the pinned arXiv versions and named theorem locations is the independent source-review procedure. The unversioned author/publisher copies may change.

The public manifest freezes this projection. SOURCE_BINDINGS.json records the accepted source identities; PROJECTION_AUDIT.json identifies privacy and portability changes. VERIFY_PACKET.py checks packaged bytes and retained scope qualifications, not the external mathematical literature or historical completeness. No historical program was executed.
