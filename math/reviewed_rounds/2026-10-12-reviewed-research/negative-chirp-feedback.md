Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: d89108b404074f6b3d995407b61b30acb57aa07069e736b29bf53025292d3c4b

---

# Independent review of negative sign chirp feedback exclusion

Date: 2026-10-11 UTC. Verdict: **ACCEPT SCOPED. No mathematical repair required.**

The new negative-sign geometric anchor, explicit arithmetic family, and both-sign non-effective generic extension pass independent review. This acceptance is tied to the exact author report SHA-256 `30f0ec725c0df8c4487df5f24aacb98130986fe081ecfd53aab5153a23360a6b` and candidate archive SHA-256 `6cd662b19ff4d7e47e60c7d32c5e93d708d726ae22d49f8f9812c528f9656cae`. It is a correctness review, not worldwide novelty clearance or external peer review.

## Accepted statements

For every integer k>=1 with k not congruent to 4 modulo 5, set N=4820k-5. For every primitive complex Nth root omega, define the unnormalized Fourier matrix F_N[i,j]=omega^(ij), the fixed chirp A_N[j,j]=omega^((N+1)j^2/2), and B_N=(F_N^(-1)+A_N)^(-1). Then B_N cannot be a sum of two terms L_r(I-W_r)^(-1)R_r, where each W_r is supported on a Hamiltonian cycle of the fixed N coordinates, L_r and R_r are arbitrary diagonal matrices, and each Green denominator 1-product(w_r) is nonzero. Zero edge weights, singular endpoints, and identically zero endpoint masks are included. The first length in this explicit family is 4815; the unrestricted sequence N=24100t+4815, t>=0, is a valid subfamily.

Combined with the separately accepted positive-sign generic argument, only finitely many odd N=5m with gcd(m,5)=1 can evade this same five-coordinate necessary obstruction. The finite exceptional set is not computed. There is no effective cutoff and no assertion excluding every eligible N.

Negative sign means the Gauss-square identity G_N^2=-N, equivalently N=3 modulo 4. It does not choose one of the two imaginary square roots. Both signs of G_N and every primitive omega are covered.

## Source integrity and independence

All 23 author payloads match the manifest's byte counts and hashes; the manifest matches its seal. The archive contains the same payload bytes. All eight source pins match. The three historical theorem texts were additionally compared byte-for-byte with their original members in the master checkpoint archive. Five remaining pinned texts were compared with their original local paths, including SP11 and its accepted independent review and H01-H05 ledger. `ORIGINAL_ARCHIVE_PIN_CHECKS.json` records the three archive comparisons.

SP11's accepted SHA-256 is `4aed4e38953ac9266f8dbe8995dae1d61046f02972f11c5434c018681eac8df5`. The historical restriction review SHA-256 `8fcf5b11cd161e33b8fcab05acae7bf1f17d0f6775b9d2cca6c8f3807b1ea82f` expressly accepts the positive-sign generic result and expressly leaves the negative-sign anchor open. Therefore this is a genuine extension of that accepted scope, rather than relabeling the old square family.

No author, uploaded, or historical program was executed, imported, compiled, or AST-parsed. The reviewer programs were written afresh from the necessary equations. Source programs are preserved inert. The controls import only the reviewer's own arithmetic module. No Sheet, GitHub, or Library write was made in this review.

## Complete geometric reconstruction

The negative numerator is H_-(g)=F-gC-g^3D with F_ab=eta^(ab), C_ab=eta^(-3(a+b)^2), and D_ab=eta^(-3a^2)delta_ab. At p=241, eta=91, and g=103, direct arithmetic gives eta of exact order 5, g^2=5, g^3=33, and denominator 1-g^3=209. The rebuilt numerator is

    106 198  94  94 198
    198 205 180 161 236
     94 180  37 229 161
     94 161 229  37 180
    198 236 161 180 205

This is not the old positive N5 numerator: its diagonal has the opposite cubic contribution.

The new implementation uses tuple field elements (a,b) for a+b*theta with theta^2=7, descending-root depth-first forests, exhaustive projective quadratic root enumeration, and last-available-pivot Gauss-Jordan elimination. These choices differ from the author's packed field representation, ascending breadth-first forests, quadratic-formula roots, and first-pivot elimination. It reconstructs all equations and branches before comparing source data; reported totals are never inputs to the mathematical classification.

Every Hamiltonian cycle is enumerated exactly once by a traversal beginning at zero. For every one of the 24^2 order pairs, every eligible shared-column row-pair equation is derived directly by a 2-by-2 determinant. All 4,320 transition matrices are invertible. Thus their projective transports are bijections, with no singular-transition stratum discarded. Each connected component has a nonzero homogeneous quadratic after transport.

For each selected nonzero quadratic the reviewer enumerates all 58,081 affine points (1,a+b*theta) plus infinity (0,1), and then intersects every remaining quadratic. Since every binary quadratic over F241 splits over its quadratic extension, this finite enumeration is complete over the algebraic closure. It is not merely an F241-rational-point test. Linear, constant, repeated-root, and infinity cases are retained; no zero-base guard is used. The actual complete component intersections produce:

- 384 empty order-pair domains
- 72 pairs with one component and two directions
- 120 pairs with two components and two directions each
- 624 total row branches

All 3,120 joint column systems have rank exactly one, hence one projective column direction. No rank-zero column continuum is dropped. Full off-support multiplication is checked for every resulting pair U,V. All source normalized branch sets agree exactly with the independently rebuilt sets.

Every branch has coefficient rank 10 and augmented rank 11. The review produces its own nonzero 11-by-11 minor for all 624 branches, and separately recomputes every one of the author's 624 recorded determinant values. All agree. Each independently selected minor passes an exact rescaling by ten independently chosen nonzero extension-field units, with the predicted nonnegative row and column multidegrees. Both total multidegrees are six.

For the negative target, 242 branches have a zero row base coordinate and 242 have a zero column base coordinate; 144 have neither. Four have both. All are rejected by closed minors, never by base-coordinate exclusion. The positive control independently reproduces its distinct 240,240,144 boundary counts. Matching the principal totals between positive and negative cases does not identify their targets or boundaries.

`NEGATIVE_REBUILD.json` contains the complete independently generated 576-pair and 624-branch witnesses. `POSITIVE_REBUILD.json` independently checks the positive control as a sanity check. The extension arithmetic passes all 58,080 nonzero inverse checks and 58,081 additive-negative checks. Seven explicit degenerate quadratic controls also pass.

## Necessity and every allowed boundary

For nonsingular endpoints, inverse row and column supports are respectively {i,pi(i)} and {j,tau^(-1)(j)}. Inverting the two branches gives U B V=D_x V+U D_y after independent direction normalization. This forces the off-support bilinears and all maximal minors of the 25-by-11 augmented scale matrix to vanish.

Under projective rescalings u_i->lambda_i*u_i and v_j->mu_j*v_j, a selected minor gains product_i lambda_i^(n_i-1) times product_j mu_j^(m_j-1). If a selected row set has n_i=0 or m_j=0, a coefficient column is identically zero, so the minor itself is zero. Otherwise all degrees are nonnegative. Thus the universal necessary equations define a closed subscheme of (P1)^10. The selected minors are pointwise witnesses against this full closed system; no sufficiency claim is needed.

Replace zero endpoint entries by a formal epsilon while fixing the legal weights and their denominators. Both perturbed branches become invertible over C((epsilon)), and their sum specializes to the proposed target. Normalize each inverse direction pair by its smallest valuation. Every pair has a nonzero projective limit, and all homogeneous equations specialize to zero. Scale variables may have poles. Zero edge weights are never divided by. This proves inclusion of every singular-mask boundary, including all-zero masks.

As finite controls, the reviewer rebuilt all 96 author targets by direct matrix inversion rather than the author's path formula. All listed ranks agree, including 72 singular-mask controls. An additional 96 independently generated controls pass, with 55 entirely zero-mask cases across the additional tests. In total 168 of 192 controls have singular masks. Four tampering checks detect a changed determinant, a duplicated minor row, the opposite-sign target, and an omitted cycle pair.

## Uniform specialization and explicit family

The exact block on S=(0,m,2m,3m,4m), N=5m, is (F-G_N C+N G_N D)/(1+N G_N), with eta=omega^(m^2). The primitive order is five because gcd(m,5)=1. The Gauss-square identity for all odd composite moduli and primitive characters follows from the opposite-sum product and the Jacobi character identity in [Gurevich-Hadani-Howe, section 3.1, equation 3.3 and Remark 3.3](https://arxiv.org/html/0808.2447). It requires no squarefreeness assumption. The actual denominator is nonzero because |N G_N|=N sqrt(N)>1.

For N=3 modulo 4, Q(G_N) is imaginary quadratic. The cyclic quartic K=Q(eta) has unique quadratic subfield Q(sqrt(5)), which is real. Therefore X^2+N is irreducible over K. The monic ring O_N=Z[T,U]/(Phi5(T),U^2+N) is free of rank two over Z[T]/Phi5(T), embeds in its field K(G_N), and is an integral domain. It embeds in C by T->eta,U->G_N for every supplied primitive omega.

If N=-5 modulo 241, the map T->91,U->103 respects both defining relations and has residue field F241. Localizing at its kernel gives an integral local ring with fraction field K(G_N). The denominator 1+N U is a unit because it reduces to 209. The numerator reduces to exactly the excluded negative target. No primality, squarefreeness, normality, DVR, flatness, or hidden extra prime exclusion is required. In particular 241 does not divide N under the displayed congruence. The argument works in the descended coefficient field; it never sends a primitive Nth root directly to a fifth root.

The full necessary scheme is projective over this local base and hence proper, by [Stacks, Tag 01WC](https://stacks.math.columbia.edu/tag/01WC). A complex point would make the generic fiber nonempty. Its proper image is closed, so would contain the special point, contradicting geometric special-fiber emptiness. Target division by the unit209 does not change the scheme because the target occurs linearly in each off-support equation and in the last column of each minor.

Principal restriction preserves each Hamiltonian Green term: multiply edge weights along skipped arcs, whose union covers the original cycle. The total product and its denominator remain unchanged. This proof uses no edge division, and endpoint masks restrict entrywise. Thus an allowed full representation would induce a forbidden five-coordinate representation.

The congruences give m=-1 modulo241 and m=-1 modulo4, hence m=964k-1 and N=4820k-5. Positivity is k>=1 and gcd(m,5)=1 is exactly k not congruent to4 modulo5. Every such N is 3 modulo4, disjoint from the previously accepted N=5q^2 family with odd q, which is 1 modulo4.

## Generic argument and exact open set

For fixed eta and cycle pair, the closed direction family over the symbolic g-line for H_-(g) projects properly. Its characteristic-zero fiber at g=103 is empty by the same local specialization, so its image is a proper closed subset of the affine line and is finite. The parameter103 need not be an actual negative-sign Gauss sum; one excluded symbolic parameter suffices. Taking the finite union over 576 order pairs and four embeddings gives a finite exceptional parameter set. Since |G_N|=sqrt(N), only finitely many eligible negative-sign N can map into it. The already accepted positive-sign generic theorem supplies the other sign.

Still open: the effective exceptional set or cutoff; which eligible sizes outside the explicit families are excluded individually; even sizes and sizes divisible by25; unmatched endpoint permutations; other choices of feedback; products or three-or-more-term grammars; negative-family upper constructions and growing-dimensional full-B upper constructions; base-field-only length-three closure in the previously accepted five-dimensional upper; numerical or runtime guarantees; worldwide historical priority. No numerical matrix of size4815 or larger is constructed here, nor is one needed.

The feedback architecture is exactly F=B(I-AB)^(-1)=(I-BA)^(-1)B, which forces B^(-1)=F^(-1)+A for this fixed A. No lower bound for arbitrary Fourier algorithms follows.

## Publication decision and replay

The exact negative-sign extension may be recorded as independently accepted under the existing canonical claim M-CHIRP-LOWER. Preserve the old positive-family text and existing SP11 acceptance. Replace only the obsolete negative-sign-open qualification with this scoped new acceptance, while retaining the uncomputed-exception warning. This supplies no separate worldwide-new-discovery count and does not close Q11's outstanding upper-construction tasks.

Run `python independent_review.py` and `python independent_controls.py` from this package. Only these reviewer-owned programs execute. The bundled `source_candidate/` and candidate ZIP are inert inputs. Original local-source comparisons are repeated when their original paths are present; portable replay still verifies every bundled source hash. `SPECIALIZATION_REVIEW.md` records the separate mathematical audit. The seal and manifest identify every review payload.
