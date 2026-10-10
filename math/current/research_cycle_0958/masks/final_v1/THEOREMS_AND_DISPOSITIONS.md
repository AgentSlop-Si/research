# Q26–Q27: exact mask certificates and guarded target fibers

Date: 2026-10-10. This manuscript freezes the claims below. Supplied programs were inspected only as inert text: none was executed, imported, compiled, or AST-parsed. All computations reported as fresh used the separately authored programs in this directory. Source-reported counts are explicitly separate. External independent review is recorded separately.

## Result and disposition

1. **Q26, Phase39:** the complete seven-Green no-factorization theorem is independently reconstructed at **N=4 and N=8**, for every complex projective middle coefficient, every two invertible diagonal masks, and every two intermediate permutations. Both cubic and quartic tests succeed on every mapping in each of two valid split primes. This closes these finite sizes, not all N.
2. **Phase39 N=16:** all 10,483,200 mappings per prime are claimed by source logs for the cubic test. This cycle reconstructs the exact matrices, guards, fixed witness and **2,048 distinct deterministic mappings per prime**, both certificate types. That is not an independent exhaustive N=16 proof. Larger source scopes remain untouched. No supplied exhaustive verifier was run.
3. **Phase38:** its already independently accepted six-Green N=4,8,16,32,64 theorem remains a separate inherited result. At N=4,8 it also follows from the newly rebuilt seven-Green theorem by setting the third projective coefficient to zero. Phase38 acceptance does not establish changed Phase39 data.
4. **Q27:** the Phase40 weighted-cycle chart can feed the fixed-stage Hadamard–Segre test **pointwise**, after its weights, permutations, outer stages and allowed diagonal slots are fixed. We give an exact parameterized fiber characterization below. It is a classical application, not a new Fourier construction.
5. **Useful guarded strengthening:** every saved Phase40 local-Jacobian witness at N=8,16,32 is reconstructed in both primes; the residues agree. At the same examples, both resolvents exist and the **entire middle sum is invertible and entrywise nonzero**. Consequently local four-ratio dominance remains valid on the admissible dense/invertible middle chart. This does not show that the four Fourier ratios, or the full Fourier matrix, lie in its image. No unit-modulus solution is established.

## 1. Frozen seven-Green family

N is a power of two at least 4. The six cycle orders are the unique successive lists `[0]+shuffle(1,...,N-1)` from Python's documented seeded `random.Random(37037+N)` stream, keeping the first six distinct lists. Their actual integer arrays are saved in `fresh_N*_p*.json`, removing dependence on recreating a random stream. The seventh order is the first unused analogous list from seed `39039+N`, except at N=4 where it repeats the zeroth order. Thus there are **six distinct orders at N=4**, not seven; its seventh coupling differs.

For a cycle list c, W sends e_(c_j) to e_(c_(j+1)). Put G_s=(I-alpha_s W_s)^(-1), with

alpha_0,...,alpha_6 = (1+i)/4, (2+i)/7, (1+2i)/8, (1-i)/5, (2+i)/9, (1+i)/6, (1+3i)/11.

A=G_0+(1+i)G_1/3, C=G_4+(1-i)G_5/4,
B(x)=x_0 G_2+x_1 G_3+x_2 G_6,
F[j,k]=zeta_N^(jk), T=A^(-1) F C^(-1).

The target architecture is F=A D_1 P_1 B(x) P_2 D_2 C. D_1,D_2 are arbitrary invertible complex diagonal matrices and P_1,P_2 arbitrary permutations. Coefficients x range over nonzero projective triples; their common scalar can be absorbed by D_1. The affine architecture x=(1,lambda,mu) is a subset. Green denominators, cycle orders and outer sums are fixed, rather than freely tuned synthesis parameters.

Every |alpha_s|<1, so all Green resolvents exist over C for every N. The fresh modular outer determinants below separately establish that A and C are invertible in characteristic zero at each tested size. The proof uses the coefficient field Q(zeta_N), with i=zeta_N^(N/4).

## 2. Complete algebraic certificate theorem

Let K be any field, T an N-square target, and B(x) a ternary linear matrix pencil. Fix target rows 0,1 and target columns 0,1,2,3. For proposed distinct middle rows r_0,r_1 and distinct middle columns c_0,...,c_3 define

q_ab(x)=T_(0,a) T_(1,b) B_(r_1,c_a)(x) B_(r_0,c_b)(x)
        -T_(0,b) T_(1,a) B_(r_1,c_b)(x) B_(r_0,c_a)(x).

### Theorem 1: necessity and no-root certificates

If T_(i,j)=u_i B_(r_i,c_j)(x) v_j, then every q_ab(x)=0. This is polynomial necessity even when some T or B entries vanish: substitution makes the two terms exactly the same product. No division or nonzero-entry hypothesis is used for this implication.

For pairs (01),(02),(03),(12), multiply their four quadrics by x_0,x_1,x_2. The coefficient matrix K_3 has 12 rows and the 10 cubic monomials as columns. Rank 10 over K excludes every nonzero projective common root over every extension of K. For pairs (01),(02),(13), multiply their three quadrics by the six quadratic monomials. The resulting K_4 is 18 by 15, and rank 15 gives the analogous exclusion.

**Proof.** Full column rank means the row span contains every homogeneous monomial of degree d=3 or 4. At a common root all row polynomials vanish, hence all degree-d monomials vanish. A nonzero coordinate x_j gives x_j^d nonzero, a contradiction. Full rank remains full after a field extension. Conversely, failure of either rank test supplies no factorization and need not even supply a projective common root for all necessary equations. ∎

### Theorem 2: anchor defect

For every ternary pencil and any anchor column c_0, the two forms B_(r_0,c_0), B_(r_1,c_0) have a common nonzero kernel vector over K. At that vector every anchor-star q_(0b) vanishes. Therefore no homogeneous full-column-rank certificate made solely from those anchor-star equations can succeed at any degree.

**Proof.** A 2 by 3 homogeneous linear system has kernel dimension at least one. In each term of every q_(0b), one of the two anchor forms occurs. Their common kernel therefore annihilates the star. When the coefficient rows are dependent the cross product may vanish, but a nonzero kernel vector still exists; the theorem does not rely on a nonzero cross product. If the corresponding target anchor entries are nonzero, this basepoint cannot be an actual factorization with invertible masks. ∎

### Theorem 3: modular lifting with exactly the necessary guards

Let all matrix coefficients lie in a localization R of the cyclotomic integers, and let phi:R→F_p be a ring homomorphism that sends all displayed denominators, Green determinants, and outer determinants to nonzero elements. A nonzero maximal minor of the reduced K_d implies that the same minor is nonzero in Q(zeta_N), hence over C. It therefore proves the complex no-root conclusion for that mapping.

**Proof.** A zero element of R maps to zero. The coefficient identities and inverse matrices are respected because every inverted element is a unit in the reduction. Thus a nonzero reduced determinant contradicts a zero characteristic-zero determinant. The complex conclusion follows from Theorem 1 in characteristic zero, rather than from any claim that finite-field rootlessness directly implies complex rootlessness. A modular zero is inconclusive. ∎

Here p=998244353 with generator 3 and p=2013265921 with generator 31. Fresh bounded trial division confirms primality; primitive-root tests use complete prime factor sets {2,7,17} and {2,3,5}. The reduction sends zeta_N to g^((p-1)/N), i to g^((p-1)/4), consistently with i=zeta_N^(N/4). Every rational denominator, every det(I-alpha_s W_s), det A and det C is nonzero in both reductions at N=4,8,16,32. Their residues are recorded, and all entries of T are also nonzero. The latter guard validates the interpretation of the anchor basepoint as spurious but is not needed for a full-rank exclusion.

### Theorem 4: complete finite exclusion at N=4,8

For the frozen seven-Green family, at N=4 and N=8 there is no equality F=A D_1 P_1 B(x) P_2 D_2 C for any nonzero complex x, any invertible complex D_1,D_2, or any permutations P_1,P_2.

**Proof.** Every permutation pair induces an ordered pair of distinct middle rows and an ordered quadruple of distinct middle columns for the fixed target window. There are N(N-1)·N(N-1)(N-2)(N-3) such mappings. Our fresh verifier enumerates all 288 at N=4 and all 94,080 at N=8 in each prime. Every mapping has rank K_3=10 and rank K_4=15. The explicit maximal-minor row sets and nonzero determinants for each mapping are in the witness CSVs, in lexicographic mapping order. Theorem 3 lifts each minor, and Theorem 1 excludes that mapping. Since every full permutation induces one of the enumerated mappings, none succeeds. ∎

This is a finite computational theorem with a complete transparent reconstruction and explicit certificate ledger, not a statistical extrapolation. One valid prime and one certificate type per mapping suffice; the second prime/type supply redundant checks. The diagonal masks need not have unit modulus, so the exclusion also covers that narrower mask class.

### Corollary 4B: generic stability inside the constrained Green family

Keep the saved cycle orders fixed at N=4 and N=8. Allow the seven scalar Green couplings and two outer mixing weights to vary as nine independent complex parameters theta. There is a **nonempty Zariski-open set of theta, containing the displayed common specialization**, for which the full projective two-mask/two-permutation factorization is excluded at both N=4 and N=8.

**Proof.** For each size and each mapping, choose one maximal cubic minor certified nonzero above. Its characteristic-zero value is a rational function f_mapping(theta), regular where the Green and outer inverses exist. At the displayed specialization every chosen minor and every required denominator is nonzero. Clearing denominators and multiplying their finitely many numerator polynomials, together with the inverse guards, gives one polynomial H(theta) nonzero at that common specialization. On the nonempty open set H≠0, all those same no-root certificates remain valid. Theorems 1 and 4 then apply simultaneously at both sizes. ∎

This is a classical openness corollary but is genuinely on the **constrained fixed-order Green parameter space**, not merely the unrestricted space of pencil entries. It leaves exceptional parameter tuples and other cycle orders unclassified, and does not prove an all-N theorem. An actual Fourier construction in this chart must lie on the exceptional algebraic locus; identifying a point on that locus is not by itself a construction.

### Finite accounting

- Fresh exhaustive: N=4, 288 mappings/prime/type; N=8, 94,080 mappings/prime/type; two primes and both types. Total 188,736 distinct prime/mapping checks and 377,472 full-rank matrices for the exhaustive sizes.
- Fresh sampled: N=16 and N=32, 2,048 distinct mappings/prime/type at each size, two primes, both types. These deterministic finite samples are not representative-probability estimates. Each passed mapping is individually excluded. No full-permutation theorem follows at either size from these samples.
- Fresh fixed-order/guards/data: N=4,8,16,32 in both primes; source T,G_2,G_3,G_6 data agree entry-for-entry with matrices reconstructed by directly inverting sparse I-alpha W, rather than by executing the supplied Green constructor.
- Fresh planted controls: at every one of the eight size/prime instances, an explicitly masked/permuted B(1,7,11) has common root (1,7,11), all six quadrics vanish, and both rank tests are deficient. Anchor-star basepoints also vanish exactly.
- Source-reported only in this cycle: Phase39 exhaustive N=16 cubic (10,483,200 mappings per prime); its 100,000-mapping larger samples, direct Q(i) calculation, historical online executor tests and other source logs. The saved logs have been inspected and hashed, but their counts are not fresh independent computations.
- Phase40 eight-Green N=8 all-mapping exclusion is not rerun here. This task reconstructs its weighted two-cycle Jacobian chart, which is a **different parameter family**.

## 3. Exact pointwise compatibility with Hadamard–Segre

Fix a field K, invertible matrices F,A,C, permutations P,Q and a rational middle family B(h). Its admissible domain U requires that every h coordinate and every rational-function denominator required by the architecture be nonzero. On the dense chart additionally require B(h) invertible and entrywise nonzero. Set B_tilde(h)=P B(h) Q. These permutations are absorbed in B_tilde only after their precise ordering is fixed.

### Theorem 5: parameterized full target fiber

There exist h in U and invertible diagonal L,D,E such that

F=L A D B_tilde(h) E C

if and only if there exist h in U and a vector c with every c_i nonzero such that

Z(h,c)=[A^(-1) diag(c) F C^(-1)] ⊘ B_tilde(h)

has rank one and every entry nonzero. If L is forbidden, set c=(1,...,1); do not silently add a free endpoint. If only two internal masks occur, this is exactly the two-mask target-fiber test for that fixed parameter point.

**Proof.** Forward: c_i=L_ii^(-1) gives Z=d e^T. Conversely every nonzero-entry rank-one matrix factors as d e^T with nonzero coordinates, for example d_i=Z_(i,0), e_j=Z_(0,j)/Z_(0,0). Multiplying back gives the required factorization with L=diag(c)^(-1). ∎

Equivalently all 2 by 2 minors of Z vanish and the guards hold. After clearing denominators, the **exact admissible fiber**, rather than its potentially larger closure, is the polynomial system consisting of those cleared minors together with t·G(h,c)-1=0, where G is a common denominator times the products of all required nonzero h, c and matrix entries and the required determinant numerators. Over C, this extra equation is equivalent to G≠0. With h fixed and P_0 invertible, this reduces to the accepted common-eigenvector formulation in `matrix/OMITTED_MATRIX_THEOREMS_AUDIT.md` §C. Without an invertible P_0, that eigenvector reformulation cannot be used, while the rank-one formulation remains valid.

The fixed-stage commutator determinant and quantitative gap depend on h. A nonzero determinant at one h rejects that h; it does not reject every h. A positive fixed-stage gap can tend to zero along a variable family. To exclude an entire synthesis chart requires a uniform argument or an actual elimination certificate over its variables.

If B has zeros, replace the dense quotient theorem with the exact support/bipartite-cycle criterion: Y=A^(-1)diag(c)FC^(-1) must have exactly the same support; every supported quotient Y_ij/B_ij must be nonzero; alternating products around every bipartite cycle must agree. Tree propagation then reconstructs d,e. This is the classical sparse diagonal-equivalence extension and has no implication that solving the unknown parameter fiber is easy.

### Why the common holonomy gauge fits the two free internal masks

If the original weighted middle is B_original=V B_normalized V^(-1) for an invertible vertex diagonal V, then

D_1 P_1 B_original P_2 D_2
= [D_1(P_1 V P_1^(-1))] P_1 B_normalized P_2 [(P_2^(-1) V^(-1) P_2)D_2].

Both bracketed factors are invertible diagonal matrices. Hence the common gauge normalization loses no candidates **when both internal masks are arbitrary invertible diagonals in exactly these slots**, even with permutations. If masks are phase-only, this absorption preserves that class only when V is unitary up to an irrelevant scalar; arbitrary nonunitary normalization cannot be assumed harmless. The edge-phase case below supplies a unitary normalization because it propagates only unit-modulus gains.

### Unit-modulus contract

Over C, if L,D,E must be unitary diagonal matrices, Theorem 5 additionally needs |c_i|=1 and |Z_ij|=1 for every entry. These conditions are necessary and sufficient on the rank-one dense chart: the explicit factors above then have unit modulus. If the edge gains themselves must be phases, their chord coordinates must also be unit modulus. Tree normalization preserves the unit circle when the original gains are unit modulus. Conversely unit-modulus chord values with all tree weights 1 are a phase-gain representative.

No algebraic nonvanishing witness at arbitrary integer/rational complex weights proves any of these real constraints or establishes that a desired fiber meets the unit torus. The complex local Jacobian calculation is not a phase-only controllability theorem.

## 4. Admissible local dominance, with guards independently restored

For two fixed Hamiltonian cycle orders on N vertices, list the 2N directed edges separately even if endpoints repeat. Normalize a spanning tree by one common diagonal similarity, leaving N+1 nonzero chord coordinates h. If an edge u→v has weight w, its normalized weight is w D_u/D_v, with a common nonzero vertex potential D. Tree normalization exists and is unique after fixing one root potential. A common scalar in D is irrelevant, so exactly E-N+1=N+1 independent chord coordinates remain. The same conjugacy works for both Green resolvents. This normal form is classical.

Let G_s(h)=(I-W_s(h))^(-1), M(h)=G_1(h)+G_2(h), and

R_j(h)=M_(0,j) M_(1,0)/(M_(1,j) M_(0,0)), j=1,2,3,4.

For a chord edge e:u→v in cycle s, differentiating (I-W_s)G_s=I gives

∂G_s/∂h_e=G_s E_(v,u) G_s,
∂log R_j/∂h_e=G_(0,v)G_(u,j)/M_(0,j)+G_(1,v)G_(u,0)/M_(1,0)
 -G_(1,v)G_(u,j)/M_(1,j)-G_(0,v)G_(u,0)/M_(0,0).

The log notation is a rational differential. The rank agrees with the ordinary Jacobian because all four R_j are nonzero.

### Theorem 6: guarded finite-size dominance

For each of the exact Phase40 cycle pairs at N=8,16,32, the rational map h↦(R_1,...,R_4) is dominant **even after restricting to the open set where all h are nonzero, both Green resolvents exist, and M is invertible and entrywise nonzero**.

**Proof.** Fresh construction starts with the same explicit integer edge weights and cycle arrays, saved in `fresh_holonomy_results.json`, and computes the common tree normalization by direct potential equations. It independently inverts I-W_s, forms M, and computes the displayed derivatives. In both split primes, the selected 4 by 4 Jacobian determinants match the saved source values:

N=8: 56838468 modulo 998244353; 1747559245 modulo 2013265921.
N=16: 481014383; 660534201.
N=32: 428415093; 14681146.

All normalization denominators and Green determinants are nonzero, every entry of the complete M is nonzero, and det M is nonzero in each reduction. The source's conditional modular adjustment of an integer weight is not triggered in any of these cases, so each pair of primes tests the same characteristic-zero integer problem. Nonzero reductions prove all these rational expressions are nonzero at the same complex parameter point. The complex inverse function theorem on the four selected coordinates gives a local open image; hence no nonzero polynomial vanishes on the full image, so the rational map is dominant. The image of an algebraic morphism on this open domain is constructible, so it contains a nonempty Zariski-open subset of the target torus. All guards hold on a neighborhood of the certified point, and therefore the same argument applies to the guarded domain. ∎

This supplies an actual compatible **admissible chart** for Theorem 5. It does not establish its Fourier fiber. The scalar four-middle-generator Phase40 family is different from this two-weighted-cycle family; neither its fixed-family exclusions nor its sampled Weyl failures transfer to arbitrary holonomies.

### Exact counterexamples to the invalid inference

Dominance does not imply surjectivity. On U=(C\{0,-1})^4, the map h↦(h_1+1,...,h_4+1) has identity Jacobian everywhere and maps to (C*)^4, but omits (1,1,1,1). Thus even a guarded full-rank local map can miss a specified torus target.

Matching one local cross-ratio window is also insufficient. For a concrete invertible dense target, take the positive-exponent F_8 and let B equal F_8 except B_(7,7)=2F_(7,7). Both are entrywise nonzero. The matrix determinant lemma gives det B=(1+1/8)det F_8≠0, since F_8^(-1)[7,7] F_8[7,7]=1/8. The first two rows and first five columns agree exactly, so all four selected ratios agree. Yet F_8⊘B is all ones except its (7,7) entry is 1/2, so its rows 0,7 and columns 0,7 have a nonzero 2 by 2 determinant. It cannot be fitted by two diagonal masks. This is a counterexample to the inference, not a claim that this B lies in the two-cycle family.

## 5. Computational and priority boundaries

The candidate Green executor uses O(N) field operations once fixed routes, gains, masks and coefficients have been supplied. None of the dense inversions, target construction, determinant audits, finding the parameters, algebraic root generation, precision work, storage or movement is free. The exhaustive local mapping test is O(N^6) fixed-dimension field tests; it is a proof audit, not a Fourier executor. No sub-N log N Fourier algorithm, all-size synthesis result, or integer-multiplication bit bound follows.

Direct primary-source inspection on 2026-10-10:

- Engel–Schneider, *Algorithms for Testing the Diagonal Similarity of Matrices and Related Problems* (1982), [author-hosted final paper](https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs066.pdf), Theorem 3.8, Corollaries 3.9–3.11 and §4.4. These provide tree normalization, Hadamard-quotient comparison and the bipartite reduction to diagonal equivalence. The guarded fiber formulation applies this classical mechanism to the present rational Green family.
- [Macaulay2 EliminationMatrices documentation](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/EliminationMatrices/html/_elimination__Matrix_lp__Z__Z_cm__List_cm__Matrix_rp.html), definition and displayed 2-by-3 homogeneous matrix example. This documents established determinantal elimination machinery; it is not a theorem-level priority comparison for the specific four/three-minor seven-Green windows. The full-rank implication is proved directly above.

No worldwide novelty claim is made. The newly rebuilt finite certificates and admissible-chart refinement are supported project-specific material; the underlying elimination, diagonal-equivalence, gauge and Jacobian principles are classical. Priority for the precise small projective-window construction remains unclosed pending a matched specialist comparator. Negative searches are not a novelty certificate.

## 6. Queue transitions recommended

- Q26: replace `queued_unassigned` by `narrow_finite_exclusion_reconstructed_review_pending` until the independent reviewer accepts Theorems 1–4 and fresh certificate records. Then close N=4,8 at this frozen scope; retain **N=16 exhaustive independent reconstruction** as an explicit residual task, rather than calling all original claims closed. Keep Phase38's inherited N≤64 theorem separate.
- Q27: close the **compatibility question** with Theorems 5–6 once independently reviewed. The answer is a guarded pointwise/classical interface and admissible local dominance, not a construction fusion. Preserve **actual admissible Fourier target-fiber witness** and optional **unit-modulus witness** as distinct unsolved constructive tasks, with parameter-generation/precision costs unproved.
- Do not add a new headline fusion on the strength of these results. A supporting theorem row may record admissible-chart dominance and the target-fiber characterization with classical attribution and explicit finite graph orders.
