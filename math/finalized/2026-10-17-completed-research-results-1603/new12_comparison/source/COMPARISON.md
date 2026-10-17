# NEW-12: completed Fourier energy/metric primary-source comparison

Date: 2026-10-17. Scope: the exact remaining source-comparison gate for NEW-12. This is an author-level completed comparison, prepared for final-stage independent review. It does not repeat or reopen the accepted analytic proof.

## Result and disposition

**Recommend CLOSED for NEW-12's bounded energy/metric comparison activity.** Lange–Liu–Peyerimhoff–Post (LLPP), Theorem 4.6, has now been read at theorem/proof level in the final published article. The comparison below gives exact energy-form identifications and a qualified nonmatch for the Fourier-target inequality. The raw energy is an ordinary Dirichlet form on a matching. The common-phase flat-reference energy is exactly a nonnegative constant plus a magnetic Dirichlet form, with an explicit treatment of amplitudes, parallel occurrences and loops. Neither identification turns LLPP's Cheeger inequality into the accepted Fourier approximation floor: the objectives, quantifiers, Fourier target separation and inverse/product norm factors differ. An admissible N=16 example demonstrates that the relevant graph's first Cheeger number and first eigenvalue can vanish while the whole-vertex unit-phase minimum is positive.

This exhausts the specifically named comparison. It is not a worldwide novelty finding, does not change proof credit, and does not close NEW-10, Q19's broader implementation work, or the separate strict-chirp attribution question. No native record or repository was changed.

## 1. Exact current gate and accepted input

The accepted tenth-ten review, §99, retains NEW-12 **only** for the precise Fourier energy/metric primary mapping, and explicitly permits a bounded qualified nonmatch preserving common-gauge, inverse-norm and occurrence hypotheses. It says strict-chirp follow-on attribution is separate. Its acceptance binds the reviewed report and disposition files; the prior open disposition is therefore the starting point, not a fresh mathematical objection.

The owned statement is [the accepted curvature source, §2.1–2.4 and §2.7](https://github.com/AgentSlop-Si/research/blob/a4dacc1f15eb910ec7d494f1572bc044e2d0533b/math/archive/objects/9b/9be4a2795988244f0658fc9e90c0e7181d5d02a0325a738ee2045e3b4377ddfa__PROOFS_AND_DISPOSITIONS.md). Its exact bytes have SHA-256 `9be4a2795988244f0658fc9e90c0e7181d5d02a0325a738ee2045e3b4377ddfa`.

Fix even s ≥ 4, N=s², h=s/2 and the involution τ(sx+y)=sx+(y+h mod s), represented by Π. Let U be the normalized complex N-point Fourier matrix. Each occurrence q=(ℓ,t) has a genuine route permutation π_q commuting with τ, weights w_qi and P_q[i,π_q(i)]=w_qi. Every G_q=(I−P_q)⁻¹ exists. Set

- L_ℓ=Σ_t α_ℓt G_ℓt and T=L_m⋯L_1, m≥1;
- a=max_ℓ Σ_t |α_ℓt|, A=Σ_q |α_q|>0;
- g>0 bounds all actual inverse operator norms and all reference inverse norms used below;
- B=(ag)^(m−1)g²;
- ρ_s=2/[s sin(π/s)], γ_s=½√(1−ρ_s);
- ε_F=‖U−T‖_F/√N, so ‖U−T‖₂≥ε_F.

The already accepted raw statement is

E_τ=Σ_q |α_q| Σ_i |w_qi−w_q,τ(i)|²,

ε_F ≥ max{0, 1/√2 − (B/2)√(A E_τ/N)}.                         (R)

In particular T=U requires E_τ≥2N/(AB²). This uses the accepted exact value ‖[U,Π]‖_F=√(2N).

For the flat-reference statement choose **one common unitary** D=diag(d_i), |d_i|=1, and constants c_q. Put w⁰_qi=c_q d_i/d_πq(i). Require every G⁰_q=(I−P⁰_q)⁻¹ to exist and satisfy the same g bound. Then

E_flat(d,c)=Σ_q |α_q| Σ_i |w_qi−c_q d_i/d_πq(i)|²,

ε_F ≥ max{0, γ_s − B√(A E_flat(d,c)/N)}.                     (F)

Thus T=U requires E_flat(d,c)≥Nγ_s²/(AB²) for every admissible reference. Taking an infimum is valid only over the stipulated uniformly norm-bounded legal reference family. For fixed c and routes, legality and reference inverse norms are independent of unitary D because G⁰_q=D(I−c_qP_πq)⁻¹D*. The total reference product commutes with DΠD*, generally not Π. Constants remain charged and must stay suitably bounded for an asymptotic Ω(N) reading. A=0 is the separately trivial T=0 case; neither displayed energy threshold divides by zero.

These formulas are restatements of accepted results, not new proof credit. The s=2 affine exception and the distinction between invertible gauges for exact algebraic exclusion and unitary gauges for metric floors remain intact.

## 2. Primary theorem actually compared

Primary source: C. Lange, S. Liu, N. Peyerimhoff and O. Post, *Frustration index and Cheeger inequalities for discrete and continuous magnetic Laplacians*, Calculus of Variations 54 (2015), 4165–4196, [final published PDF](https://link.springer.com/content/pdf/10.1007/s00526-015-0935-x.pdf), [DOI](https://doi.org/10.1007/s00526-015-0935-x). The final article, rather than only metadata or switching definitions, was inspected. The author version [arXiv:1502.06299v3](https://arxiv.org/pdf/1502.06299) cross-checks the numbering. The publisher identifies the article as CC BY 4.0; this report provides attribution and uses newly written comparisons.

LLPP uses a finite **simple undirected** graph, positive symmetric edge conductances b_uv, positive vertex measure μ, and a U(1) signature σ_vu=σ_uv⁻¹. Its relevant statements are:

- Equations (2.6)–(2.8), pp.4168–4169: Q_σ(f)=Σ_{uv}b_uv|f(u)−σ_uv f(v)|² and λ₁=min_{f≠0}Q_σ(f)/Σ_u μ(u)|f(u)|².
- Definition 3.4, p.4170: ι_σ(S)=min_{d:S→U(1)}Σ_{uv within S}b_uv|d_u−σ_uv d_v|, an **unsquared** residual.
- Definition 3.5, p.4171: h₁=min_{∅≠S⊆V}[ι_σ(S)+boundary weight]/vol_μ(S).
- **Theorem 4.6**, equation (4.22), p.4175: λ₁/2≤h₁≤(3/2)√(2d_μλ₁), where d_μ=max_u(Σ_v b_uv)/μ(u). Its proof uses the quadratic Rayleigh quotient and threshold/coarea argument, with Lemma 4.8 on p.4176.
- Theorem 4.1, p.4172, treats cyclic signatures with upper constant 2; Theorem 5.1, p.4177, relates higher eigenvalues and multiway Cheeger constants. Neither changes the target/objective mismatch below. Corollary 4.10, p.4177, identifies λ₁=0 with the existence of a balanced connected component.

The source's switching and tree-flatness correspondences remain credited. The new comparison concerns the displayed energy/metric inequalities.

## 3. Exact raw-energy identification and its limit

For each occurrence q with |α_q|>0, create N graph vertices (q,i). Pair (q,i) with (q,τ(i)); τ has no fixed points. Give each unordered pair conductance 2|α_q|, trivial signature 1, and μ=1. Evaluate the vertex function f(q,i)=w_qi. Each pair occurs twice in E_τ, so

Q_1(f)=E_τ                                                     (3.1)

exactly, with no hidden factor of two. This graph is a disjoint union of edges. Its λ₁ and h₁ are zero regardless of f: a constant function on one component has zero Rayleigh energy, and that component has no boundary or frustration. LLPP Theorem 4.6 therefore gives 0≤0 for this direct graph map. It cannot supply the nonzero target-dependent term 1/√2 in (R).

This is a precise direct-theorem nonmatch, not a claim that graph estimates can never be combined with additional matrix arguments. The missing extra information is exactly the accepted Fourier commutator defect plus propagation through the particular resolvent/sum/product network. The primary Cheeger theorem does not contain U, Π, A, B or legal inverse norms.

## 4. Exact flat-energy identification, including general amplitudes

The following derivation is the comparison's own algebra. It supplies a complete map to the source's simple-graph quadratic form without assuming that all network weights have unit modulus.

For an occurrence edge e=(q,i) write u=i, v=π_q(i), β_e=|α_q|, r_e=|w_qi| and R_e=|c_q|. If r_eR_e>0 define

σ_e=w_qi·conj(c_q)/(r_eR_e) ∈ U(1),  a_e=β_e r_eR_e.

If r_eR_e=0 set a_e=0 and omit that phase edge. Because |d_u|=|d_v|=1,

β_e|w_qi−c_q d_u/d_v|²
= β_e(r_e−R_e)² + a_e|d_u−σ_e d_v|².                         (4.1)

This includes zero weights/constants through its radial term. Thus unequal amplitudes are not silently discarded. In the equal-amplitude restriction r_e=R_e, the radial term vanishes and a_e=|α_q||c_q|². This is the simplest exact magnetic-energy overlap.

LLPP's source graph is simple, while the network counts occurrences and can have loops, parallel routes, and opposed orientations. The following exact reduction handles that difference on the unit-phase domain:

1. A loop u=v contributes the constant a_e|1−σ_e|².
2. For every unordered pair {u,v}, choose u<v. Reverse an oppositely oriented occurrence by replacing σ_e with conj(σ_e). Let A_uv=Σ_e a_e and Z_uv=Σ_e a_eσ_e over that pair in the chosen orientation.
3. If Z_uv≠0 retain one simple edge with b_uv=|Z_uv| and σ_uv=Z_uv/|Z_uv|. If Z_uv=0 retain no edge. The pair's exact contribution is

Σ_e a_e|d_u−σ_e d_v|²
= |Z_uv||d_u−(Z_uv/|Z_uv|)d_v|² + 2(A_uv−|Z_uv|),             (4.2)

where the first term is zero when Z_uv=0. This follows by expanding both sides as 2A_uv−2Re(Z_uv d_v conj(d_u)).

Consequently the original energy has the exact representation

E_flat(d,c)=C(c)+Q_σ(d),                                     (4.3)

where C(c) is the sum of all radial residuals, loop terms and 2(A_uv−|Z_uv|). Every summand is nonnegative. The remaining graph is literally a finite simple magnetic graph satisfying the source's edge conventions. The zero-conductance edge case is handled by omission, not by applying a positive-weight theorem to zero weights.

This equality is for unit-phase d. It must not be promoted to an identity for arbitrary-amplitude f in the source Rayleigh minimization. The constant reduction of parallel edges depends on |d_u|=|d_v|=1.

For fixed c, put J₂=min_{|d_u|=1}Q_σ(d), J₁=ι_σ(V), W=Σ_{uv}b_uv and M=Σ_u μ(u). Compactness gives these phase minima. From source equation (2.8) and elementary Cauchy–Schwarz,

min_d E_flat(d,c)=C(c)+J₂,
J₂≥Mλ₁,
J₁²/W≤J₂≤2J₁  (W>0).                                      (4.4)

For d_μ>0, Theorem 4.6 therefore gives the valid restricted consequence

min_d E_flat(d,c)≥C(c)+Mλ₁≥C(c)+2M h₁²/(9d_μ).               (4.5)

If the reduced graph has no edges, J₂=0 and E_flat=C(c), handled directly. If c is also optimized, the reduced graph and C vary with c; apply (4.3)–(4.5) separately at each admissible c and retain the original inverse-norm guard. No single fixed graph is asserted to represent unrestricted optimization of c.

## 5. Why the theorem is a qualified nonmatch for (F)

Equation (4.3) is an exact energy-form match; **(F) is not Theorem 4.6** under that match.

- Source λ₁ minimizes over arbitrary-amplitude nonzero vertex functions. J₂ fixes unit modulus at **every** vertex. Source h₁ additionally selects a subset and includes its boundary. These minimizations are not interchangeable.
- Theorem 4.6 bounds a graph eigenvalue and an unsquared frustration/expansion statistic. The owned conclusion bounds distance between a specific Fourier matrix and an ordered product of sums of resolvents. It needs the Fourier separation γ_s and the paid norm multiplier B√A.
- A lower bound on E_flat such as (4.5) does not give the positive lower bound on ε_F in (F): the right side of (F) decreases with E_flat. A supplied small-energy reference yields the approximation obstruction; Cheeger energy lower bounds cannot be inserted in that place with the inequality reversed.
- The exact-equality requirement E_flat≥Nγ_s²/(AB²) is conditional on T=U. The graph theorem has no such matrix-equality premise. It cannot generate that particular threshold without the additional accepted Fourier/propagation argument.
- Independent phase choices d^(q) for different occurrences would minimize separate graph problems, but would generally destroy the one shared DΠD* commutant needed for (F). Repeated occurrences remain repeated in A, B, propagation and edit counts even if their quadratic energies are aggregated by (4.2).

### An admissible, exact separation example

Take s=4, N=16 and τ(i)=i+2 within each consecutive block of four. Let a single route π be the product of cycles (0 4 8)(2 6 10), fixing the other ten vertices. This route commutes with τ. Use one layer, one occurrence, α=1 and c=1/2. Put w_8=w_10=−1/2 and all other w_i=1/2. Then ‖P‖₂=1/2 and ‖P⁰‖₂=1/2, so all actual/reference inverses exist and g=2 is valid for every common unitary D.

The phase graph consists of two triangles with holonomy −1 and ten isolated vertices. Each triangle has edge conductance 1/4; fixed-point loops contribute zero. C(c)=0. Each unweighted triangle has magnetic Laplacian

[[2,−1,1], [−1,2,−1], [1,−1,2]],

whose eigenvalues are 1,1,4. Thus its unit-phase minimum is at least 3; (1,e^(iπ/3),e^(2iπ/3)) attains 3. Scaling conductance and counting both triangles gives

J₂=3/2, while λ₁=0 and h₁=0.                               (5.1)

The zero eigenvalue/Cheeger number follows already from an isolated vertex with μ=1. Therefore the minimizations cannot be identified even inside the accepted network's legal route, common-gauge and inverse-norm scope. This example does not claim a counterexample to either theorem and does not claim T=U. It only separates the alleged exact source-theorem identification. Also E_τ=0 because τ-paired weights agree, consistent with (R).

## 6. Cost-model and equality boundaries

The accepted abstract certificate evaluates supplied energies in O(E+N) scalar operations, with streamed O(N) auxiliary workspace, where E counts occurrences. Route validation, coefficients, a legal common reference and certified g are inputs or separately paid tasks. Rational/algebraic bit cost and rigorous rounding are additional. Later bounded certifier acceptances remain valid; this comparison neither reopens nor generalizes them.

LLPP's theorem is a spectral/geometric inequality. Its existence or use of eigenfunctions does not pay for eigenvalue computation, a minimizing switching function, a legal resolvent reference, or a norm certificate. Our aggregation (4.2) is an algebraic source map, not a free algorithm: it needs occurrence access and grouping, with storage/comparison and exact phase/modulus costs charged. No running-time lower bound, production certification or uncharged O(E) optimizer follows from either side.

Exact algebraic exclusion under arbitrary invertible endpoint diagonals does not license the unitary metric steps above: multiplication by d_v and the reduction (4.2) use |d_v|=1. Reference constituent inverses are required even when the total reference network need not be invertible. The source's switching-flatness equality characterization and the accepted network's forest/rank tests remain scoped as before.

## 7. Evidence-backed stop

The previously absent work was a theorem-level comparison of the Fourier energy/metric claim, not another numerical replay or a general novelty search. Sections 2–5 now identify the primary theorem, map the full energies and normalization, give the actual source implication, and prove the precise nonmatch with the retained assumptions. Section 6 pays the cost-model difference. These satisfy the current recorded completion condition.

Recommended change after independent acceptance: NEW-12's **bounded current comparison activity** may close, with one newly completed comparison and zero new theorem/discovery count. Native application, if requested, needs its separate exact preimage/readback process. Strict-chirp attribution, arbitrary endpoints, unrestricted architectures, worldwide priority, NEW-10 and Q19's remaining implementation scope remain separate; none is an invented blocker to this activity.
