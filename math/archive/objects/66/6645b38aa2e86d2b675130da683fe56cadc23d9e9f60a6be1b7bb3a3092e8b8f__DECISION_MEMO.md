# Priority decision: actual-source packets and the adjacent-anchor orbit

Date: 2026-10-10. This is a bounded priority and significance assessment, separate from a fresh correctness audit. No supplied program was run, and no material was published or shared externally.

## Decision

**The adjacent-anchor exclusion is subsumed by a short classical cut-rank argument.** The accepted long certificates remain valid, but neither their length nor closure of their boundary cases supplies a new obstruction method. See CUT_RANK_PROOF.md for the complete argument, which is stronger than the audited statement.

**The actual-source packet theorem is a sound and useful project-specific application of classical bounded-coefficient volume bounds.** It materially improves the earlier arbitrary-jet result: its inputs really are only one N-vector. Its reusable content is the exact selected-packet spectrum and its marker-density application. Current evidence does not justify calling it an independently publication-worthy new lower-bound theorem. It fits best as a supporting proposition in a motivated marker-feedback paper.

Neither result should presently be elevated above the ramified Rogers–Szegő local-discriminant candidate solely because it has passed an exact audit. That separate candidate retains its own unresolved priority checks, which are not repeated here.

## 1. The decisive adjacent-anchor comparison

Set S={0,1,2,3}. The pi support has one edge leaving S; sigma has two. For an invertible matrix, a complementary off-diagonal block has the same rank as the corresponding block of its inverse. Thus the S-to-S^c block of any sum of the two prescribed inverse branches has rank at most three.

The adjacent anchor and all its nonsingular diagonal scalings preserve S. The corresponding block of F8 has rank four, being a Vandermonde block on four distinct eighth roots. This contradiction excludes the entire orbit at once, including zero edges and zero pivots.

The classical input is the inverse-block identity and rank subadditivity, explicitly treated in [Chandrasekaran–Epperly–Govindarajan, Propositions 2.1–2.3](https://arxiv.org/html/1911.05858). The application to these exact maps is a derivation in this assessment, not a claim that their paper states this example.

The short proof extends to every invertible first factor block diagonal for S|S^c and every field containing a primitive eighth root. It even dispenses with nonzero diagonal coefficients in the branch matrices, retaining only their invertibility and supports. These extensions are straightforward consequences of the same proof. They are not independent originality claims.

## 2. Actual-source packets: exact overlap and remaining contribution

The audit establishes H as an actual selection of output-time/coordinate pairs depending on x in C^N, with no independently supplied temporal jets. Its complete quotient banks produce

    H*H = F_unitary* diag(lambda_ell) F_unitary,
    lambda_ell = sum_(h,t) 2^h 1_(E_(h,t)(ell)).

The marker argument places at least N/4096 eigenvalues above 2^(n-L), with N=2^n and L=o(n). Identity augmentation and Cauchy–Binet then give

    additions >= (1/2) log2 det(I+H*H)
                 -(1/2) log2 binom(N+D,N).

This is a direct instance of the rectangular volume inequality: take A=[I;H] and r=N in equations (2) and (4) of [Bürgisser–Lotz, Section 3](https://arxiv.org/html/cs/0301016). Their exact binomial comparison, before its coarser stated proposition, yields precisely this subtraction. The project's direct gate-potential proof also isolates additions when all scalar moduli are at most one. Neither identity augmentation nor retaining the binomial factor creates a new volume method.

The remaining possible contribution is the particular map being analyzed: correct phase/routing fusion; complete quotient-bank occupancy despite the actual-source dependence; exact weighted spectral coverage; and the neighboring-marker construction that gives high-weight density. This combination is a meaningful scoped theorem. Its historical priority is unresolved, and its significance depends on explaining why this interface matters outside the unsuccessful algorithmic route that motivated it.

There is established context for tree-selected orthogonal packet systems in [Coifman–Wickerhauser](https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/2/436/files/2011/04/coifman92en.pdf?bid=436) and overlap-sensitive word counting in [Guibas–Odlyzko](https://doi.org/10.1016/0097-3165%2881%2990005-4). Neither comparison has been shown to state the same marker-output theorem. Similarity is insufficient to claim duplication; failure to locate duplication is insufficient to claim novelty.

Normalization is part of the substance. Replacing each time-h row by 2^(-h/2) times itself makes every output row have norm one. Every N-row minor of [I;H_normalized] is then at most one by Hadamard. This particular determinant witness disappears. [Ailon](https://arxiv.org/pdf/1403.1307) obtains normalized-transform lower bounds in a different, condition-controlled model; those results do not automatically cover this rectangular output interface or this circuit model.

## 3. Claim-by-claim disposition

| Claim | Priority/significance judgment | Recommended use |
|---|---|---|
| Actual-source fusion is a mask of the same-time orbit | Exact project-specific identity; no independently established historical novelty | Explain why the proposed causal alias does not compute the orbit |
| Complete quotient-bank Gram and exact rank | Standard Fourier orthogonality applied correctly to this selected family; useful explicit formula | Supporting structural lemma |
| Positive-density neighboring-marker event at high h | Concrete combinatorial application, with correct overlap treatment; no new counting principle established | Short proof inside the packet theorem |
| N-input Omega(N log N) unnormalized exposed-output lower bound | Genuine strengthening within this project; classical volume method | Supporting obstruction, with gate and interface assumptions in its title |
| Matching O(N log N) charged construction | Standard layered FFT/orbit implementation | Establish sharpness in the stipulated model |
| Normalized or unexposed interface requires the same cost | Not established | Exclude from claims |
| Whole adjacent-anchor diagonal-orbit impossibility | Correct, but follows immediately from a classical cut-rank criterion | Example or brief lemma; replace the large proof in the main narrative |
| A new algebraic obstruction is required for this support pair | Unsupported; the elementary rank contradiction suffices | Drop |
| Exact unit-ideal and boundary certificates | Valid redundant verification artifacts; certificate methodology is established | Optional reproducibility supplement, not the mathematical lead |
| General two-layer Fourier impossibility or asymptotic FFT consequence | Not established by either package | Exclude from abstract and conclusions |

The inverse-branch primitive is also established: [Huhtanen–Perämäki, Propositions 2.5 and Theorems 2.7–2.10](https://math.aalto.fi/~mhuhtane/manu.pdf) treat linear-cost sums of permutation-diagonal matrices and cyclic normal forms. Unit-ideal infeasibility certificates are standard, as illustrated constructively by [De Loera–Lee–Malkin–Margulies](https://arxiv.org/pdf/0801.3788). Neither source is claimed to contain this particular target matrix.

## 4. Minimal responsible theorem statements

### Packet note, if a separate note is pursued

A suitable narrow working description is “A bounded-coefficient obstruction for marker-selected Fourier packets.” Define N=2^n, b=floor(log2(n/(4 ln n))), L=2^(b-1), and K_t as the t-bit words beginning and ending in one and avoiding 0^b. For every 1<=t<=L, 2b+t<=h<=n, k in K_t, and 0<=v<2^(h-2b-t), include the complete quotient bank

    f=rev_t(k) 2^(h-b-t)+v,
    P_(h,q,f)(x)=sum_(s=q mod 2^(n-h)) omega^(sf)x_s,
    0<=q<2^(n-h).

Unimodular row phases do not change the following result. Any exact complex linear circuit exposing all these unnormalized values, using binary additions/subtractions and scalar multipliers of modulus at most one, needs at least

    (1/8192-o(1)) N log2 N

additions. A layered orbit implementation achieves O(N log N) field operations for the audited bank. The row-bank Gram is the stated Fourier multiplier; the proof uses classical volume bounds.

This is a faithful mathematical center for a short note, not a recommendation to submit one now. Its actual-source feedback interpretation should be an application, so the statement can be understood independently of the project's internal terminology.

### Adjacent-anchor example

Use the stronger short statement in CUT_RANK_PROOF.md: F8 is not a sum of two inverses with the prescribed supports multiplied by an invertible S-block-diagonal first factor. A one-page proof is sufficient. A standalone research note centered only on this immediate application is not presently justified.

## 5. What evidence would change the recommendation?

For the packet theorem:

1. Establish an independently motivated use for this output bank or a natural family of marker languages with a genuinely informative uniform criterion.
2. Compare the exact selected family against pruned/multiresolution Fourier-transform lower bounds and subgroup packet literature. Existing search results alone are not a priority clearance.
3. Distinguish a reusable theorem from a reformulation of the already-known spectral threshold bound. Better constants or a general lemma that merely restates rectangular volume are not substantial advances by themselves.
4. Keep the normalized interface, unbounded coefficients, positive characteristic, nonlinear circuits, and implementations avoiding H outside the result unless separately proved.

For the fixed-support certificate:

1. Replace the lengthy main argument by the cut-rank proof now.
2. Before additional eliminations, test classical cut-rank constraints for the proposed supports and anchor-invariant cuts.
3. A stronger research case would require an obstruction that survives all such obvious cuts and proves a structural family theorem, a sharp classification, or a genuinely new invariant. None is established by the present adjacent example.

These are research thresholds, not instructions to expand the current task or to publish. No exact antecedent to the full packet application was established; no global novelty claim follows. The strongest immediate result of this assessment is the classical simplification and resulting priority downgrade of the adjacent-anchor certificate.
