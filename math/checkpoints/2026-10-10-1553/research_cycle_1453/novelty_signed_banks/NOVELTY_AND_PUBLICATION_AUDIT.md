# Signed Weyl bank novelty and publication audit

10 October 2026. Scope: the exact whole-bank grammar in the small-order synthesis manuscript, together with the independently reviewed order-eleven upper construction. This is a bounded literature and significance assessment, not a new proof review or a claim of worldwide priority.

## Conclusion

The exact minima M_C(3)=4, M_C(5)=5, and M_C(7)=8 are plausible original, model-specific results. This search did not locate an equivalent published classification. That is sufficient to retain them as candidate new mathematics, but insufficient to certify historical priority. The classical mechanisms underneath them are well established.

The package could support a narrowly scoped research note in exact algebraic synthesis or structured decomposition. Its publication case depends on explaining why this particular dictionary is natural, and on presenting what its examples reveal beyond successful small computations. No evidence here supports calling it a major mathematical breakthrough or an FFT advance. Journal acceptance or significance cannot be inferred from internal proof acceptance.

The new M_C(11) <= 14 construction is a verified extension in the same model, over the splitting field of a sextic over Q(q). It adds a substantial exact example; it is not a minimum or an infinite-family theorem. No inspected source supplies a theorem that already yields fourteen legal banks for this precise Fourier target. Conversely, the common-node construction mechanism is established mathematics, so a special certificate by itself does not establish a new general method.

## Accepted claims and field boundaries

- N=3: the exact minimum is four over every field of characteristic not dividing three that contains the primitive root.
- N=5: the exact minimum is five over every characteristic-zero field containing the primitive root; a witness lies in Q(q).
- N=7: every characteristic-zero extension containing q requires at least eight. Eight are attained in the splitting field of the displayed cubic over Q(q), hence over C. Attainment in Q(q) alone is not claimed.
- N=11: fourteen are attained in the displayed sextic splitting field L over Q(q), with [L:Q(q)] <= 720. Together with the accepted general lower bound this gives only 6 <= M_C(11) <= 14. The twelve-bank diagnostic excludes only the singleton-one, shared-root, depressed-quintic ansatz.

These are the reviewed mathematical scopes, not historical-novelty findings. The order-eleven acceptance receipt was frozen at 15:30:21 UTC on 10 October 2026. This audit does not assess any subsequent parametric-family addendum.

## The exact object being compared

Fix one cyclic shift S and clock T with TS=qST, and F_N[k,t]=q^(-kt). One allowed unit is

B_(epsilon,delta)(alpha,beta;w)
 = (1/N) sum_j w_j (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),

with epsilon,delta in {+1,-1}, j=0,...,N-1, arbitrary complex phase weights, and 1-alpha^N-beta^N nonzero. A whole bank counts once. Different banks may choose different nodes and signs, but there are no free gauges, generator changes, pre/post maps, or products.

The reviewed coefficient identity is

B = sum_ell eta_ell sum_(r=0)^(N-1-ell) alpha^r [r+ell choose ell]_(q^(epsilon delta)) W_(epsilon r,delta ell).

This restriction must survive any purported equivalence to prior art. An expression with N scalar terms, a product of triangular matrices, a sum of rank-one matrices, or a transform conjugation has a different counted unit.

## A more precise classical-model match

There is a close structural match that deserves addition to the manuscript's literature discussion.

For a fixed orientation, write c_(r,ell) for the coefficient at W_(epsilon r,delta ell). Every Gaussian factor on r+ell <= N-1 is nonzero. Dividing by it gives

c_(r,ell) / [r+ell choose ell]_(q^(epsilon delta)) = eta_ell alpha^r.

For m banks of that orientation the right side becomes sum_i eta_(i,ell) alpha_i^r. Thus all sectors share the same m nodes, while each sector has its own amplitudes and its own available moment length. A node may have zero amplitude in a sector; that does not remove it from the bank count if another sector uses it. Coincident nodes of the same orientation combine, rather than becoming new derivative atoms.

Over C, beta introduces no additional effective dictionary freedom. For any alpha and arbitrary eta_ell, choose beta nonzero and avoid the finitely many values with beta^N=1-alpha^N. Set Delta=1-alpha^N-beta^N and

w_j = Delta sum_ell eta_ell beta^(-ell) q^(-epsilon delta j ell).

Finite-character orthogonality recovers every requested eta_ell. This explicitly includes alpha=0 by choosing a legal beta; fixing beta=1 would incorrectly omit that stratum. A legal beta=0 bank is already included in the enlarged finite-node description. The equivalence is for C, or another sufficiently large field, not asserted for every finite field.

The parameterization eta_ell(1,alpha,...,alpha^(N-1-ell)) is the finite-node chart of a rational normal scroll, with a degree-zero sector giving a cone vertex. Sturmfels and Sullivant explicitly use x_ij=s^j t_i and describe the secant ideals through concatenated Hankel minors in Section 5, Theorem 5.7. Our identification of one bank with that chart is a direct algebraic deduction from the displayed coefficient formula. [Sturmfels and Sullivant, Combinatorial secant varieties](https://arxiv.org/pdf/math/0506223).

Comon, Qi, and Usevich formulate simultaneous decompositions with common vectors and different coefficients, identify the binary case as a rational normal scroll, and distinguish exact rank from secant closure and border rank. This is a direct conceptual predecessor to shared-node sector synthesis. [Comon, Qi, and Usevich, Sections 2.4 and 3.2](https://arxiv.org/pdf/1603.01566).

Three differences prevent claiming that these passages already prove the present minima:

1. The four sign choices have different coordinate embeddings and different Gaussian rescalings. Their triangular supports overlap. One cannot independently divide the full target by four incompatible coefficient scalings and then add independent rank answers.
2. A scroll's projective closure includes the infinite-node fiber. Secant closure can also include limiting or confluent decompositions. The bank model permits finite parameters and ordinary repeated-node merging, not derivative atoms. A border-rank upper bound is not automatically an exact legal bank construction.
3. A generic-rank theorem does not decide the rank of the particular quadratic-phase Fourier coefficient array. The deficient rows and coupled axes are exactly where target-specific compatibility matters.

Accordingly, a careful description is: exact rank of a special Fourier point relative to a union of four weighted, embedded finite-node scroll dictionaries. This is a classical framework with a potentially new special target and exact-rank classification.

## Comparison with primary sources

### Weyl powers and the cyclic resolvent

Holtz, Mehrmann, and Schneider state Potter's root-of-unity identity and the noncommutative Gaussian-binomial formula in Theorems 1 and 2. Once X^N=(alpha^N+beta^N)I is known, the finite inverse follows by multiplication of a geometric sum. These are not new parts of the packet. [Holtz, Mehrmann, and Schneider](https://people.math.wisc.edu/hans/hms_sub.pdf).

Ouvry, Wagner, and Wu's cyclic linear system has diagonal 1-q^k y1-q^(-k)y2 and forward/backward shift coefficients. Setting the reverse variables to zero gives the same branch family, up to the explicitly chosen orientation. Their Section 2.2 has the corresponding 1-alpha^N-beta^N denominator. This is exact overlap at the branch level; the inspected work studies walk generating functions and Hofstadter moments, not minimum sums of arbitrary phase-weighted whole banks realizing F_N. [Ouvry, Wagner, and Wu, equations 7 and 8](https://arxiv.org/pdf/1606.03273).

Gross's finite-dimensional Weyl formalism supplies the operator basis, character transform, and trace-coordinate viewpoint. The manuscript's choice of Weyl phase differs, so formulas must be converted rather than copied. This supports the classical status of projection, not a bank-count classification. [Gross, Section II](https://arxiv.org/pdf/quant-ph/0602001).

### Prony moments and interpolation

Potts and Tasche's Section 2 links exponential sums, annihilating recurrences, Hankel kernels, and Vandermonde recovery. Peter and Plonka's Theorem 2.1 extends that recovery mechanism to eigenfunction sums. The order-seven cubic and order-eleven sextic use this same annihilator/common-node principle. Their special coefficients and compatibility conditions remain target-dependent. [Potts and Tasche](https://www-user.tu-chemnitz.de/~potts/paper/prony.pdf); [Peter and Plonka](https://num.math.uni-goettingen.de/plonka/pdfs/Operator_Prony_revised2.pdf).

Mourrain's polynomial-exponential decomposition framework connects finite Hankel rank, quotient algebras, root multiplicities, and recovery from moments. It strengthens the reason to credit the general algebraic machinery. It does not license derivative terms in the bank grammar or resolve the four-orientation coupling. [Mourrain, Theorem 3.1 and Sections 3 and 4](https://arxiv.org/pdf/1609.05720).

### Cauchy representations and finite Fourier factorization

Pan's Vandermonde-to-Cauchy transformations concern structured matrix identities and conditioning. They show that replacing polynomial/exponential formulas by rational kernels is not itself a novelty claim. The inspected transformations are not count-preserving mappings into sums of the permitted banks. [Pan, Sections 1 and 4](https://arxiv.org/pdf/1504.02118).

Kuznetsov gives V_q=LDL^T with q-Pascal L, including the root-of-unity Fourier specialization when no lower power of q is one. This is a concrete pre-existing Fourier/q-binomial synthesis, but it is multiplicative and admits factors not supplied free by the bank grammar. It neither duplicates nor disproves the additive minima. [Kuznetsov, Theorem 1](https://files.ele-math.com/articles/oam-12-45.pdf).

Petz, Plonka, and Derevianko reconstruct non-harmonic exponential sums by rational interpolation of Fourier coefficients. Their unknowns are signal frequencies and amplitudes, not an exact additive representation of the finite Fourier operator by fixed shift-clock resolvents. The common vocabulary does not establish an equivalent optimization problem. [Petz, Plonka, and Derevianko](https://arxiv.org/abs/2011.13346).

### Sparse dictionary and atomic decomposition

Eldar and Mishali study sums of selected subspaces and common-support recovery; Chandrasekaran, Recht, Parrilo, and Willsky formulate general simplicity as sums of atoms. These are relevant conceptual frameworks, not formulas for this dictionary's Fourier rank. Arbitrary phase weights make a bank a whole parameterized subspace contribution, so scalar sparsity and convex atomic norm values cannot silently replace bank count. [Eldar and Mishali](https://arxiv.org/abs/0807.4581); [Chandrasekaran and colleagues](https://arxiv.org/abs/1012.0621).

## What could actually be new

Subject to broader expert comparison, the defensible contributions are:

- The fixed-grammar exact minima at N=3,5,7, with field scope stated precisely.
- The all-candidate order-five axis obstruction, not just failure of a chosen ansatz.
- The order-seven two-row incompatibility, including degenerate nodes and amplitudes, and a short justified good-reduction certificate.
- Legal exact attaining witnesses and reconstruction of original phase weights, including the algebraic-field boundary at N=7.
- The N=11 fourteen-bank certificate, including simultaneous edge compatibility and original-resolvent verification, without a minimum assertion.

The four-support-triangle observation and elementary general bounds can be useful parts of the paper, but their originality or depth should not be inflated. An internal exact verification establishes correctness within scope; it does not establish that these statements have never been proved elsewhere.

## Does existing general theory already yield fourteen at order eleven

No inspected theorem was found to give this particular bound in the exact bank grammar. The common-node and scroll literature explains how to search for, formulate, and certify such a decomposition. It does not remove the need to show that these specific cyclotomic moments admit a legal squarefree shared annihilator, that every sector is compatible, and that the remaining row systems are solvable.

Nor can the standard maximum-rank versus generic-rank principle be read as a fourteen-bank result. A bank has at most N+1 effective affine parameters after the explicit beta elimination above. For N=11, seven-bank sums have dimension at most 84, below the ambient 121. More generally, (N-1)(N+1)<N^2 shows that the generic count is at least N. Consequently, doubling a generic count cannot yield a universal bound fourteen at N=11. This elementary parameter-count observation is included only to explain why that proposed shortcut fails; it is not a computation of the generic count or the Fourier minimum.

A special-target consequence of an uninspected theorem remains possible. The appropriate literature verdict is 'no exact-match theorem located in the inspected sources,' not 'there is no such theorem.'

## Standalone paper potential and the main missing question

The strongest present paper would be an exact structured-rank study with complete small-order classifications, not a Fourier algorithm paper. It already has real assets: lower bounds beyond dimension heuristics, full degeneracy coverage, legal witnesses, and independently checkable certificates. The small-order results are more publication-worthy together than as separate isolated notes. N=11 belongs as an extension or example, unless its construction can be generalized.

The main missing significance question is: Why should minimizing the number of these whole banks be important, independently of having defined the model? One bank contains N inverse terms and N free weights. A count reduction is not yet reduced arithmetic work, memory, physical components, precision, or preparation cost. The paper needs an intrinsic algebraic question, a natural application that charges exactly this unit, or a general theorem showing structure beyond small N.

The most useful next result would be one of:

1. An infinite-family construction with a proved bound and a conceptual shared-annihilator criterion, including all deficient sectors and inverse guards.
2. A general lower-bound mechanism that improves the current linear estimate or explains exact counts for a nontrivial family.
3. A substantive exact-rank versus border-rank, or base-field versus splitting-field, separation in this model.
4. A demonstrated application where the whole-bank resource is physically or computationally meaningful, accompanied by a complete cost and stability analysis.

More small-N upper bounds alone would improve evidence and examples but are unlikely to transform the significance assessment. No general formula, N+1 bound, optimality at eleven, FFT speedup, or historical breakthrough should be inferred from the present sequence.

## Safe claim language

"We determine the exact number of phase-weighted signed Weyl resolvent banks needed to synthesize the Fourier matrices of orders three, five, and seven, in a fixed additive model, obtaining four, five, and eight. We also give an exact fourteen-bank construction at order eleven. The underlying Weyl, Gaussian-binomial, and common-node moment methods are classical. We have not located an equivalent classification in the primary sources examined; historical priority remains unconfirmed."

## Search limitations and evidence boundary

The search used both the model's names and its standard mathematical translations: shift-clock resolvents, Hofstadter Green systems, q-binomial Fourier factorization, common-node exponential moments, rational interpolation, rational-normal-scroll secants, X-rank, unions of subspaces, and atomic decompositions. Primary papers were opened and the identified passages read. Search titles, abstracts, and unrelated keyword hits were not treated as exact matches.

The strongest negative evidence is the explicit mismatch analysis above, not absence of a search-engine hit for custom terminology. This was not an exhaustive MathSciNet/zbMATH review, an all-citation forward/backward search, or a specialist consultation. No author was contacted. All accepted research files were left unchanged; no supplied research program was executed, imported, compiled, or parsed, and no external write was made.
