# Prior-art comparison: selected-pair Green reachability obstruction

10 October 2026

## Conclusion

The generic algebraic mechanism is classical: clear the two inverse pencils, eliminate a variable by the resultant of two degree-one polynomials, then relax a bilinear monomial vector to an arbitrary nonzero kernel vector. The four-column rank test is therefore best described as a concrete, division-free elimination certificate for the stated Green family, rather than a new general theory of determinants, displacement rank, resolvents, or bilinear elimination.

That assessment does **not** establish that the concrete Green compatibility proposition or its pinned Fourier exclusions have appeared before. This bounded comparison found no source stating the same selected-pair theorem with the same frozen six-term model. Absence of an exact match in this search is not a novelty certification. A potentially new application can follow from entirely classical machinery; conversely, changing the names of matrices does not establish a new theorem of general algebra.

The separate correctness review accepts the selected-pair propositions, the four exact certificates, and the precisely scoped characteristic-zero exclusions. This literature comparison addresses antecedents and priority, not a second numerical verification. The accepted proof and certificate scope are recorded in PROOF_STATUS.json.

## What is being compared

The selected-pair result considers

\[
T(v,h)=(A+b(I-D_vQ_V)^{-1})(B+a(I-D_hQ_H)^{-1}),
\]

with fixed matrices, permutations, and coefficients, and arbitrary replacement vectors on the two inverse domains. Its first proposition rewrites target equality as

\[
R_{ij}-v_iU_{ij}-h_jW_{ij}+v_ih_jZ_{ij}=0.
\]

For a fixed row pair \(i,k\), eliminating each \(h_j\) gives a bilinear polynomial in \(v_i,v_k\). Its coefficients form row \(j\) of a matrix \(M_{ik}(F)\), and reachability implies

\[
M_{ik}(F)(1,v_i,v_k,v_iv_k)^T=0.
\]

The four-by-four minors are target-only necessary conditions. Their practical value is that one nonzero minor excludes every admissible choice of the two replacement arrays, including zero entries, while retaining the one-sided terms in the full finite equality.

## 1. Closest exact algebraic precedent: linear resultants and Segre coordinates

**Primary source:** Mathias Drton, Bernd Sturmfels, and Seth Sullivant, *Algebraic factor analysis: tetrads, pentads and beyond*, Probability Theory and Related Fields 138 (2007), 463–493. [Published article](https://doi.org/10.1007/s00440-006-0033-2); [author preprint, arXiv:math/0509390](https://arxiv.org/abs/math/0509390), §6, Theorem 19 and Examples 20–21, equations (20)–(21).

Example 20 explicitly gives the determinant resultant of two linear polynomials. Example 21 gives the resultant of three polynomials in the basis \(1,x,y,xy\), as a difference of products of three-by-three minors. Theorem 19 relates these multilinear resultants to products of projective lines in their Segre embedding. This is an exact match for the algebraic operations, though the paper's application is factor analysis rather than the Green model.

**Direct comparison with the selected-pair result.** Writing its equations as \(\alpha_i+\beta_i h_j=0\) and \(\alpha_k+\beta_k h_j=0\), the selected-pair result's elimination is exactly

\[
\alpha_i\beta_k-\alpha_k\beta_i=0.
\]

This is valid without division and is necessary even when coefficients vanish. Thus the avoidance of entrywise division is useful, but is already a basic property of this resultant construction.

The subsequent kernel vector is a coordinate chart of the Segre surface:

\[
q=(1,x,y,xy),\qquad q_0q_3-q_1q_2=0.
\]

The condition \(\operatorname{rank}M\leq3\) forgets that quadratic relation and the affine-chart requirement \(q_0\ne0\). It is a determinantal relaxation, not a full bilinear solvability criterion. In particular, the four-by-four minor should not itself be called *the bilinear resultant* or a hyperdeterminant.

For example, an abstract four-column coefficient matrix whose kernel is spanned by \((1,0,0,1)\) has rank three but admits no kernel vector \((1,x,y,xy)\): its second and third coordinates force \(x=y=0\), contrary to its fourth coordinate. This illustrates the missing constraint, without asserting that this particular abstract matrix is realized by the Green construction.

The known three-equation resultant also explains a possible refinement. For a three-by-four row submatrix \(C\), its signed maximal-minor vector \(c\) gives the necessary expression \(c_0c_3-c_1c_2=0\). This is classical, has degree six in the coefficients of \(C\), and is distinct from the selected-pair result's degree-four coefficient determinant. No new certificate using this refinement has been tested here.

## 2. Classical displacement rank: related perspective, different operator

**Primary sources:** Thomas Kailath, Sun-Yuan Kung, and Martin Morf, *Displacement ranks of matrices and linear equations*, Journal of Mathematical Analysis and Applications 68 (1979), 395–407, [DOI](https://doi.org/10.1016/0022-247X(79)90124-0); and their *Displacement ranks of a matrix*, Bulletin of the American Mathematical Society 1 (1979), 769–773, [DOI](https://doi.org/10.1090/S0273-0979-1979-14659-7), especially Lemma 1 and Theorem 1 on pp. 770–771. The latter's [primary-paper scan](https://scispace.com/pdf/displacement-ranks-of-a-matrix-1k6rb7j3ww.pdf) was inspected.

Lemma 1 describes displacement rank through the rank of \(R-ZRZ^T\) or its transposed-shift counterpart. Theorem 1 relates displacement ranks of a matrix and its inverse. The discussion on p. 771 explicitly allows choices of the displacement matrix other than the shift, including circulant choices. Thus inverse structure, non-Toeplitz structured matrices, and rank tests built from transformed matrices are established territory.

**Difference that matters.** In the selected-pair result, \(D_v,D_h\) are unknown diagonal parameters, and the cleared equation has four terms

\[
R-D_vU-WD_h+D_vZD_h=0.
\]

The four-column matrix is quadratic in target-dependent coefficient entries and is formed after eliminating a parameter. The note does not exhibit a fixed classical Sylvester or Stein displacement operator whose rank is this rank-three condition. Calling the certificate a direct restatement of a classical displacement-rank theorem would therefore require an additional reduction, which was not found here. Calling it a new displacement-rank theorem would likewise overstate what is shown.

The established conceptual overlap is that structure can imply low rank after a suitable transformation. The precise elimination map and the selected-pair application are the objects that would need a theorem-level prior-art comparison.

## 3. Resolvents and Sherman–Morrison: the inverse manipulation is standard

**Primary historical source:** Jack Sherman and Winifred J. Morrison, *Adjustment of an Inverse Matrix Corresponding to a Change in One Element of a Given Matrix*, Annals of Mathematical Statistics 21 (1950), 124–127, [DOI and publisher record](https://doi.org/10.1214/aoms/1177729893). Bibliographic details were verified; the publisher did not supply readable full text in this pass. No detailed original-paper theorem number or historical priority beyond this identified paper is claimed.

**Direct algebraic comparison.** For invertible \(S,S-E\),

\[
(S-E)^{-1}-S^{-1}=(S-E)^{-1}ES^{-1}.
\]

This follows by multiplication. A single changed row weight makes \(E\) rank at most one; arbitrary replacements of an entire weight vector can make it full rank. Sherman–Morrison is consequently the natural comparison for a single-entry/rank-one inverse update, but a bounded rank-one update argument does not automatically control the selected-pair result's arbitrary complete arrays.

Proposition 1 instead multiplies the target equation by both inverse pencils. Its validity on the stated domain is elementary clearing of inverses. The contribution under consideration is the target-only consequence obtained afterward, not a new inverse-update identity. Retaining the one-sided terms is essential to this application but is not a new principle of resolvent algebra.

## 4. Structured rational interpolation: strong analogy, no identified equivalence

**Primary sources:**

- A. C. Antoulas and B. D. O. Anderson, *On the scalar rational interpolation problem*, IMA Journal of Mathematical Control and Information 3 (1986), 61–88. [DOI](https://doi.org/10.1093/imamci/3.2-3.61); [author's publication account](https://www.ece.rice.edu/~aca/Pub.html), item 4.
- B. D. O. Anderson and A. C. Antoulas, *Rational interpolation and state-variable realizations*, Linear Algebra and its Applications 137–138 (1990), 479–509. [Publisher abstract](https://www.sciencedirect.com/science/article/pii/0024379590901408), DOI 10.1016/0024-3795(90)90140-8.
- Tibor Boros, Ali H. Sayed, and Thomas Kailath, *Structured matrices and unconstrained rational interpolation problems*, Linear Algebra and its Applications 203–204 (1994), 155–188. [Publisher abstract](https://www.sciencedirect.com/science/article/pii/002437959490202X), DOI 10.1016/0024-3795(94)90202-X. The primary-paper text available in a [paper copy](https://www.researchgate.net/publication/222282545_Structured_matrices_and_unconstrained_rational_interpolation_problems) was also checked at the introduction, §4, and conclusion.

The 1986 work parametrizes scalar rational interpolants by complexity and uses Loewner matrices. The 1990 work obtains minimal matrix realizations from interpolation data using a Loewner matrix with a controllability/observability factorization. The 1994 paper constructs a structured matrix from interpolation data, exploits its displacement equation, and obtains linear-fractional parametrizations; its stated scope includes displacement rank two in the distinct-point scalar setting.

**Direct comparison.** On a nondegenerate coefficient chart, the selected-pair result's scalar equation can be written

\[
h_j=\frac{R_{ij}-v_iU_{ij}}{W_{ij}-v_iZ_{ij}}.
\]

For different \(i\), those fractional expressions must agree at the same column parameter. Cross multiplication recovers the division-free eliminant. This is a genuine relationship to rational compatibility and linear-fractional formulas, but the coefficients here depend on both indices and the row parameters are unknown. The selected-pair result has not supplied known interpolation nodes, a single interpolating rational function, or a realization whose minimal degree is controlled by its four-column rank. It should not be described as a Loewner-rank or interpolation-degree theorem without that missing identification.

The 1994 source is the closest of these references for the combination of structured matrix equations, rational parametrization, and a constructive rank-based method. It does not, in the inspected material, provide the selected-pair result's selected-pair Green obstruction.

## Publication wording

Suggested description of the general result:

> We derive a division-free, target-only necessary condition for reachability when one input and one output Green term are allowed arbitrary replacement weights and the remaining terms and coefficients are fixed. Clearing the two inverse pencils and applying elementary bilinear elimination yields an explicit four-column compatibility matrix of rank at most three. A nonzero four-by-four minor therefore certifies nonreachability for all admissible replacement weights. The construction uses standard resultant and monomial-lifting ideas; its specialization to this Green family and the resulting certificates are the subject of the present result.

Description of the independently accepted numerical application:

> Exact modular certificates exclude the pinned Fourier targets at N = 4, 16, 64, and 256 for the specified frozen six-term baselines and selected editable pair. The stated reduction argument also proves exclusion for the explicitly defined integer/rational characteristic-zero lifts.

Do not expand this to arbitrary frozen baselines, arbitrary coefficient changes, all lengths, the unrestricted architecture, general Fourier factorization, or a computational lower bound. Do not claim a complete reachability characterization or that all compatibility polynomials have been generated. The characteristic-zero statement must retain its explicit lift; a finite-field computation alone is not a complex nonexistence theorem.

Avoid priority language such as “the first,” “a new class of algebraic invariants,” or “previously unknown elimination principle.” If the eventual manuscript claims a new specialized theorem, identify its exact hypotheses and conclusion and distinguish that claim from the classical proof ingredients. Nothing in this bounded search establishes publication significance or priority.

## Search scope and evidence limits

This was a focused public-web comparison across the four named families, with additional searches for bilinear matrix equations and row/column linear-fractional compatibility. The strongest equation-level checks were the full primary texts of the 1979 Bulletin note and the Drton–Sturmfels–Sullivant preprint. The 1986 and 1990 interpolation comparisons rely on author/publisher abstracts; the 1994 comparison also uses accessible primary-paper excerpts. The Sherman–Morrison original was identified but its full text was unavailable through the publisher tool. No inaccessible original was silently treated as fully read.

The literature assessment does not broaden the independently accepted mathematical scope or establish worldwide priority.
