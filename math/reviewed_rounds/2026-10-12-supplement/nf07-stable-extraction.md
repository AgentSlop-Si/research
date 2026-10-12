Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: ecb14905a32cf9154ea16e36dc4b57a634916672f76064a9dca12a5ffccb02fb.

# Independent review of rational stable covariant extraction

Reviewed 12 October 2026. Verdict: ACCEPT the explicit dyadic family and its restricted conditioning and support benchmark. This completes the concrete existence obligation in NF-07::stable-extraction. It does not establish a fast Fourier algorithm, unrestricted extraction optimality, arbitrary-similarity stability, production certification, or historical novelty.

The reviewed candidate is NF07_Rational_Stable_Extraction_CANDIDATE_2026-10-12.zip, 519721 bytes, SHA-256 8c5994b6991e55c07a03793c7d030a927d87c3c6b90e94fd038a688835c296e9. The proof is nf07_stable_extraction_0041/THEOREM_AND_COST.md. Candidate bytes were copied into a separate review directory and remained unchanged. The candidate program was read as text, but was never executed, imported, compiled, or AST-parsed. This review executes only independently authored controls.

## Accepted statement

For r >= 1 and k >= 2r, put N=4^k, m=16^r, h=4^r, d=2^r, and M=Nm. Over the explicitly embedded field Q(zeta_N), the stated rational injection E and coisometric extraction P=E* have PE=I and exactly Nh nonzeros each. The literal ambient swap J=F_N tensor (F_m/h) has alpha=1 against the unnormalized target F_N. Its rationally normalized unitary version Jhat=J/2^k extracts the normalized target Fhat_N with coupling one and exact ambient-error amplification one. The support h=sqrt(m) is least possible inside the stated same-vector orthogonal norm-optimal multiplicity class for this fixed spectator Fourier transform.

The proof supplies a full M-coordinate implementation with explicit preparation, roots, normalizations, injection, extraction, data movement, and precision charges. Its cost exceeds direct evaluation of the N-coordinate target. These resource statements are upper bounds for a deliberately nonoptimal reference implementation.

## Source and contract preservation

All six packaged source pins match their stated SHA-256 values, sizes, and the original source bytes. All 15 candidate payload hashes match the internal manifest, and the original archive CRC check passes.

SP09 is pinned at d59cd3de50e2b293bb51951112bd64c567eb453725677732dd3df2be2a7f1a2f. Its corrected primitive root, power-identity, common field, nonzero coupling, exponent-dividing-N, and literal ambient-swap requirements all hold here. No uncontrolled similarity is introduced: the specified coordinates are already the canonical tensor coordinates, with the physical Euclidean inner product explicitly fixed.

The supplement-v2 ledger is pinned at c97b97df3c0d310bb3aac843acdfd100f70da9c82a53270b0ee56ba4d7ea113d. Its I12, I13, I14, I15 acceptances and I16, I17, I18 rejections are preserved. In particular:

- PE=I alone still does not imply nonzero coupling.
- A higher-exponent character table can contain F_N without a direct cyclic N-factor; this candidate does not extend the bounded-exponent theorem.
- Covariance still does not make arbitrary E/P maps or basis changes cheap or stable.
- The single-cycle and multicycle exclusions concern a literal ambient swap, and are neither weakened nor extended by this family.

SP10 is pinned at 5d40aabbb62548da8b2478ae3e93d2ae54715c87864870c3d3603f09242e87b0. Its scalar complex-linear nonrational-gate lower bound is compatible with this exact butterfly circuit and the rational maps. It is not converted into a bit-complexity, real-wire, rounded-circuit, or N log N lower bound.

## Independent algebra review

Let D=N/2. Since D is a power of two, (x+1)^D+1 is Eisenstein at 2, proving that z^D+1 defines a field of degree D over Q. In that field z has exact order N. Since m divides N, z^(N/m) has exact order m. The selected complex embedding fixes the norm statements. The product group C_N x C_m has exponent N and a perfect standard product pairing, so it satisfies the paired-group guard without acquiring a higher-order root.

The subgroup H=h Z/m has size h, and H equals its annihilator because m=h^2. For a=1_H/d, one has a*a=h/d^2=1. Character orthogonality gives F_m a=h a. Consequently V=F_m/h is unitary and Va=a. Therefore E=I tensor a and P=I tensor a* are rational, satisfy PE=I, and each have exactly Nh nonzero entries.

For the positive Fourier convention, F_N S_N=D_N F_N and F_N D_N=S_N^(-1)F_N. These identities imply both literal ambient swap equations. The four E/P intertwining identities follow directly because X and Z act only on the first factor. Thus J=F_N tensor V is a genuine invertible ambient swap, rather than merely an operator whose extracted block happens to be Fourier. The identity Va=a yields JE=EF_N and PJE=F_N.

Normalization is consistent throughout. Jhat=J/2^k is unitary, and PJhat E=Fhat_N. When Jhat is instead written against the unnormalized F_N, its extraction scalar is 2^(-k), not one. The final multiplication by 2^k required to recover F_N is expressly charged. Every displayed normalization is rational and dyadic.

## Stability and restricted support optimality

For arbitrary ambient perturbations Delta, not necessarily respecting covariance, ||P Delta E||_2 <= ||Delta||_2. Equality is attainable with Delta=(Eu)(Ev)* for unit target vectors u,v. The gain is therefore exactly one. The general optimality lower bound also follows from the unit norm of the extracted target: an exact extraction of a unitary target cannot have product-norm gain below one.

The separately stated additive vector-error bounds follow from the triangle inequality and ||E||=||P||=||Jhat||=1. An approximate ambient operator with norm error delta_J acting on an injection having vector error delta_E contributes at most delta_J(||x||+delta_E). No componentwise relative claim for near-zero Fourier outputs is implied.

For E_b=I tensor b and P_b=E_b*, with ||b||=1, the sharp recovery gain is 1/|b*Vb|. Equality to one forces Vb=(b*Vb)b by equality in Cauchy-Schwarz. The usual support product proof gives |supp(b)| |supp(Vb)| >= m. An eigenvector has the same support before and after V, so its support is at least sqrt(m)=h. The displayed rational a attains h. This argument proves exactly the restricted class claimed, and no statement about general oblique maps or different ambient operators.

For the coordinate maps, gamma=e_0*Ve_0=1/h. Recovery therefore has sharp gain h and loses log_2(h)=2r bits under the same ambient norm-error contract. A rank-one perturbation inside their image attains that gain. The comparison charges the extra Nh support of the stable maps.

## Complete application and bit charges

The two tensor axes contain log_2(N)+log_2(m)=L=log_2(M) butterfly stages. A full M-coordinate execution has M L/2 complex twiddle products and M L complex additions/subtractions, plus M final dyadic normalizations. This computes F_(C_N x C_m), not F_M. Bit reversal, buffers, zeros, copies, output materialization, and root descriptors are accounted for.

Injection uses N input scalings, Nh nonzero copies, and M writes including zeros. Extraction uses N(h-1) complex additions, N scalings, Nh reads, and N writes. Optional recovery of F_N adds N scalings. The stated O(M log M+Nh+N) scalar/index upper bound does not improve on a direct O(N log N) target computation.

In the explicit D-coordinate field representation, addition and monomial multiplication each require O(D) rational coordinate work. The candidate's resulting rational-coordinate and dyadic bit bounds properly pay this factor; they are not O(M log M) bit claims. Arbitrary rational denominator growth is correctly left dependent on its actual representation costs.

The root-generation bound includes the naive rational Machin sum, the angle computation involving N, all fixed-point recurrence products/divisions, final storage, and a conservative schoolbook arithmetic bound. The numerical application bound also pays working precision and growing intermediate magnitudes. Root construction and numerical preparation are not waived as free transcendental constants.

## Numerical proof review

The Machin identity is correct. Alternating-series tails give the displayed pi error. A useful explicit margin, implicit in the candidate's elementary series, is pi_T<16/5: the truncated positive arctangent at 1/5 is at most 1/5 and the subtracted arctangent is positive. Hence nearest-grid angle rounding still leaves |theta|<4 for the stated s. This supplies the harmless margin behind the candidate's angle bound.

For each rounded exponential-series recurrence, an error carried forward by t steps is bounded by 4^t/t! times its initial size. Summing its later effects bounds total polynomial error by 55R 2^(-s), since exp(4)<55. With n=R+1=8(q+8), the factorial estimate and geometric tail give 2^(-4q-31). The real-angle exponential is 1-Lipschitz, and final two-coordinate rounding has L1 error at most 2^(-(q+4)). Therefore the candidate's root certificate is valid for every q>=1. It is not inferred from numerical samples. For example, grouping the rounding terms gives at most 55/4096 of 2^(-q), while the pi and tail terms are each less than 1/64 and final rounding is 1/16; their sum is less than one.

For a butterfly stage, the exact norm is sqrt(2), the coefficient-perturbation norm is at most sqrt(2) eta, and the perturbed norm is at most sqrt(2)(1+eta). Telescoping L stages and dividing by sqrt(M) yields coefficient error at most (1+eta)^L-1 <= 2L eta. The complex product rounding creates at most sqrt(M) tau stage-vector error. Propagating all stages and the final normalization gives at most 5 sqrt(M) tau. These estimates apply to the entire ambient vector, before extraction. The optional final target rounding contributes at most sqrt(N) tau, so the stated total bound 2L eta+6 sqrt(M) tau is safe.

The specified q=p+ceil(log_2 L)+4 and b>=p+L/2+6 imply, uniformly,

    2L eta <= epsilon/8,
    6 sqrt(M) tau <= 3 epsilon/32,
    total <= 7 epsilon/32 < epsilon.

The other requirement b>=b_in+r makes injection exactly representable. Exact dyadic ambient scaling and extraction may enlarge the fractional exponent, as expressly permitted. The proof charges that precision and does not hide intermediate rounding. Multiplying the normalized output by sqrt(N) multiplies the absolute error accordingly; it is not free accuracy transfer to the unnormalized target.

## Fresh independent controls

INDEPENDENT_RESULTS.json records the following independently authored checks:

- Six exact common-field/subgroup cases: (N,m)=(16,16),(64,16),(256,16),(256,256),(1024,256),(4096,4096). Every spectator character sum is reduced in Q[z]/(z^(N/2)+1), and all first-factor swap entries are checked.
- Seven integer fixed-point tensor executions, including p=1 and M=65536. Dense test inputs have exactly unit norm, including complex-phase and cancellation patterns. An independently generated unrounded rational Taylor oracle provides the direct dense target reference. Every one of the M normalized ambient output coordinates is compared with the full expected tensor output, before extraction; the N extracted outputs are checked separately.
- Three full modular ambient executions, for (N,m)=(16,16),(64,16),(256,256), using dense direct DFTs on both axes rather than butterfly code. Every M output coordinate is checked, not just the extracted block.
- Fifteen negative/guard groups preserve zero-coupling and higher-exponent counterexamples, detect missing normalizations, wrong support and a literal-swap mutant, and test fresh root/precision parameter grids.

ROOT_RECURRENCE_RESULTS.json additionally records seven independent reconstructions of the candidate's rounded root recurrence, checking 344 roots against a higher-accuracy rational Taylor oracle. Nearest ties-to-even is a permitted nearest-rounding convention and remains within the same proof; this does not claim byte-for-byte replay of the author's executable.

No candidate research executable was run. The reviewer uses only its new independent_controls.py and root_recurrence_controls.py. One initial reviewer run hit Python's display limit while serializing a large exact rational after a successful inequality check; the output serialization was changed to a certified dyadic upper bound. The final sealed runs pass. This was a reviewer reporting issue, not a candidate mathematical failure.

These finite controls support the manually checked all-size arguments. They are not proof-assistant verification, a production implementation audit, practical timing evidence, or a numerical claim about arbitrary input formats.

## Classical credit and novelty limits

The representation and guarded extraction mechanism are the classical ingredients already identified by SP09. The support-product inequality and subgroup equality example appear in Terence Tao, An uncertainty principle for cyclic groups of prime order, arXiv:math/0308286v6, Introduction, equation (1) and the following subgroup paragraph, PDF pages 1–2. The primary PDF was independently inspected during this review: https://arxiv.org/pdf/math/0308286 . Its normalization differs without affecting support. Its stronger prime-order theorem is not used here. The source itself credits earlier uncertainty-principle literature.

The candidate correctly claims only a fully charged project-specific witness and benchmark. This review adds no mathematical or historical priority claim for the ingredients or their combination.

## Scope and remaining work

The explicit-family stable-extraction existence obligation is independently accepted. All earlier accepted algebra and rejected broad readings are preserved.

Keep open arbitrary fields/lengths, arbitrary similarities, general E/P support or conditioning optimality, cheap full or restricted larger-space evaluation, target-specific speedups, all-length finite-word transfer, production qualification, and historical novelty.
