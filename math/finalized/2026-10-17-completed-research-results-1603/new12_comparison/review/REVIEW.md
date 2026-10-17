# NEW-12 final independent comparison review

Date: 2026-10-17. Verdict: **ACCEPT scoped activity closure.**

The newly completed comparison satisfies NEW-12's actual remaining Fourier energy/metric primary-source gate. This is acceptance of one completed comparison and its bounded qualified nonmatch, not a new analytic theorem, worldwide priority result, or closure of broader Q19/strict-chirp work. No native status or repository content was changed by this review.

## Reviewed boundary

The exact COMPARISON.md reviewed has SHA-256 `cb9275e980b107751cd91a4d95fe06355d8b51e70b3e3771d1875dbb11296f95`. All seven author artifacts, including the manifest, are individually bound in ACCEPTANCE.json; the six contents listed in that manifest match it.

The accepted tenth-ten REVIEW.md §99 retains NEW-12 only for this exact source comparison and expressly allows a bounded qualified nonmatch with common-gauge, inverse-norm and occurrence hypotheses. Its file and acceptance hashes match the author's source list. The earlier open disposition was proper when this comparison was missing; it is not an independent reason to retain the now-completed gate. The accepted curvature source bytes also match their stated hash. Its analytic proof is an input here and was not reopened.

## 1. Primary theorem checked independently

I independently opened the final [Lange–Liu–Peyerimhoff–Post published article](https://link.springer.com/content/pdf/10.1007/s00526-015-0935-x.pdf), inspected the graph setup, quadratic/Rayleigh formulas, frustration/Cheeger definitions, Theorems 4.1 and 4.6, the shared proof with Lemmas 4.7–4.8, Corollary 4.10 and the statement of Theorem 5.1. The final-paper formula and numbering agree with the comparison. The source assumes a finite simple undirected weighted graph, positive retained edge weights, positive vertex measure and inverse signatures on reversed edges. Disconnected graphs and isolated vertices with positive measure are allowed. Theorem 4.6 has upper factor 3/2 multiplying sqrt(2 d_mu lambda_1); it does not equate a whole-vertex phase minimization with its eigenvalue or subset Cheeger minimum.

The PDF text was available and inspected. The optional publisher screenshot retrieval returned a cache-miss error, so no raster-inspection claim is made. The relevant text and mathematical expressions were readable; this does not leave a substantive theorem-identification gap. The publisher's explicit CC BY 4.0 notice was independently located. This review is newly written analysis, with source attribution.

## 2. Raw matching identification

For each route occurrence q, tau pairs distinct vertices. Each unordered pair contributes two equal summands to the original E_tau. A matching edge of conductance 2|alpha_q| therefore gives exactly E_tau, with no factor error. The function evaluated on this graph is the weight list, not an eigenfunction optimization.

Each component is a balanced isolated edge. Consequently both the first eigenvalue and the first Cheeger constant are zero independent of the supplied function. The direct source theorem is vacuous on that graph. The nonzero Fourier commutator defect and its propagation through the resolvent product are additional input; they are absent from the source theorem. This is a justified direct-theorem nonmatch, without an overbroad claim that graph tools could never assist a larger argument.

## 3. Flat magnetic identification

For one occurrence edge, expand the original squared residual. Its cross term is minus twice beta times Re(w conjugate(c) d_v conjugate(d_u)). With sigma = w conjugate(c)/(|w||c|) and conductance beta|w||c|, this is exactly the cross term of the stated magnetic residual. The remaining scalar difference is beta(|w|-|c|)^2. Thus equation (4.1) is exact for arbitrary amplitudes. A zero weight or zero reference constant contributes only the radial term and does not require an undefined phase.

For loops, unit modulus makes the magnetic residual constant. Reversing an edge conjugates sigma. For parallel occurrences, collecting the complex cross terms gives Z = sum a_e sigma_e. Replacing them by one edge of conductance |Z| preserves the variable cross term and leaves constant 2(sum a_e - |Z|), nonnegative by the triangle inequality. Complete cancellation Z=0 removes the edge and retains the whole constant. Therefore E_flat = C(c) + Q_sigma(d) is exact on the unit-phase domain, on a literal simple graph satisfying the source hypotheses. It is correctly not extended to arbitrary-amplitude functions.

The auxiliary inequalities are correctly directed. Rayleigh minimization gives J_2 >= M lambda_1. Applying weighted Cauchy–Schwarz at a J_2 minimizer and |residual|^2 <= 2|residual| at a J_1 minimizer gives J_1^2/W <= J_2 <= 2J_1. Squaring the upper Cheeger estimate gives lambda_1 >= 2h_1^2/(9d_mu), hence the stated restricted lower bound. Empty reduced edge sets are handled directly rather than divided by zero. All phase minima exist by compactness. If c varies, the graph and its constant vary; the comparison correctly applies the formulas pointwise in admissible c.

## 4. Legal N=16 separation

The route has the two cycles (0 4 8) and (2 6 10), with all remaining vertices fixed. It is a genuine permutation and commutes with the half-grid involution. Every actual and reference row weight has modulus 1/2, hence P*P = P0*P0 = I/4. The Neumann-series estimate gives the uniform inverse bound g=2; arbitrary common unitary D preserves the reference norm and invertibility.

The two reduced triangles each have weight 1/4 and sign product -1, with ten isolated vertices and zero constant C. The displayed unweighted triangle has characteristic polynomial (x-1)^2(x-4). The stated unit-phase vector is a 1-eigenvector. Its squared norm is 3, so the minimum is at least 3 and attained; scaling and counting two triangles gives J_2 = 3/2 exactly. A positive-measure isolated singleton gives h_1=0 and an eigenfunction supported there gives lambda_1=0. Paired network weights agree, so E_tau=0. This is a valid separation inside the accepted admissible network class, not an alleged counterexample or an assertion T=U.

Fresh independently authored exact controls passed all of these checks, including 12 mixed edge cases, reversed orientations, loops, zero weights/constants, an exactly cancelled parallel pair and the raw matching normalization. The actual/reference determinants in the N16 fixture are respectively 81/65536 and 49/65536. These controls support the algebra; the general conclusions above rest on the expansions and bounds, not finite testing alone.

## 5. Metric, common-gauge and inverse guards

The accepted raw and flat floor formulas, definitions of A, a, B, gamma_s and the normalized Frobenius error agree with the accepted curvature source. The factor 1/2 in the raw propagation bound, the flat B multiplier, and the exact-equality thresholds are retained. A=0, even s>=4 and the s=2 exception are not lost.

Only one common unitary diagonal is used across occurrences. Its shared conjugated commutant is D Pi D*, generally not Pi. The actual and each reference constituent inverse must exist; both inverse factors are paid in propagation. For fixed c and routes, reference inverse legality/norms are independent of D by unitary similarity. Infima are restricted to uniformly bounded legal references. The full reference product need not itself be invertible. Arbitrary invertible endpoint gauges in an exact exclusion result are correctly kept distinct from the unitary metric assumptions.

Crucially, a lower bound on flat energy cannot be substituted to improve the approximation floor, whose right side decreases with that energy. The source's free-amplitude/subset optimizations, Fourier target and norm-product dependencies are different. The qualified nonmatch is mathematically justified, including after the exact energy-form overlap has been granted.

## 6. Occurrences and cost

Repeated occurrences remain charged in A, B, the propagation sums and edit counts; energy aggregation does not merge the network's algorithmic or rank costs. The inherited O(E+N) notation means E scalar edge occurrences (q,i), not merely the number of route occurrences q. This is the necessary and consistent reading of the accepted source and the comparison's cost statement.

Supplied-reference energy evaluation is not minimization or norm discovery. Route validation, coefficient/reference generation, legal inverse bounds, exact phase/modulus work, grouping/storage and bit/rounding costs remain separately charged. There is no claim of a free phase optimizer, physical runtime certificate, production implementation, or unrestricted lower bound. No clarification of a larger engineering programme is needed to close this bounded source-comparison gate.

## Final disposition

**Accept CLOSED for NEW-12's bounded Fourier energy/metric comparison activity.** No required mathematical repair remains. Record one completed new comparison, zero new theorems and zero new discoveries. The author packet's preparation-time `independent_review=pending_final_stage` is superseded by this separate acceptance; the frozen author bytes are not changed.

NEW-10, broader Q19 implementation/resource work, strict-chirp follow-on attribution, arbitrary architectures/endpoints and worldwide priority remain separately scoped. This review performs no native application, repository upload or historical program execution. Any later application must use its own exact preimage/readback process and cannot infer a global census from this single activity recommendation.
