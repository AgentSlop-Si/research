# Bounded literature comparison for the three-orientation obstruction

12 October 2026 UTC. Comparison target: qtorus_independent_review.md and the supplied phase-bridge manuscript. This is a bounded primary-literature search and theorem-scope comparison, not a worldwide-priority certification.

## Finding

The exact three-orientation exclusion was not identified in the primary sources retrieved and inspected in this pass. Its ingredients are largely established: the q-binomial resolvent expansion, root-of-unity Gaussian-binomial specialization, Fourier minor arithmetic and monomial-equivalence invariants. The potentially distinct contribution is the explicit choice of two frontier rectangle families that isolate one branch at a time among these three specified orientations, with arbitrary independent nonzero input/output diagonal gains on each branch. Historical novelty of that combination remains unresolved.

The appropriate publication claim is an architecture-specific Fourier synthesis obstruction. It is not a new Fourier minor theorem, not a general impossibility result for sums of resolvents, and not an FFT complexity lower bound.

## Exact comparison target

For prime-power m>=5 and N=m², consider three additive resolvent branches in precisely the identity, phi(a,c)=(-c,a+c), and psi(a,c)=(a+c,a) orientations. Each branch may have its own primitive mth root and nonzero alpha,beta, with 1-alpha^m-beta^m nonzero, and its own invertible diagonal gains on both sides. The accepted restricted result excludes equality to F_N even after arbitrary outer invertible diagonal factors and row/column permutations.

The reviewed proof uses triangular support u+v<m and two translated families of 2-by-2 rectangles. On each complete rectangle only one branch survives. The remaining frontier q-binomial factors and phase factors have cancelling determinant ratios. The row directions (0,1) and (1,-1) generate the whole grid, forcing a connected graph of row pairs with a vanishing minor. This final contradiction uses prime-power Fourier arithmetic. These quantifiers, the exact orientations, m>=5 and additivity are essential; m=4, other orientation sets and products remain outside the theorem.

## Primary sources and what they already establish

### q-binomial algebra

Koornwinder, Special functions and q-commuting variables (1996/1997), Proposition 2.1, states the q-binomial expansion for q-commuting variables and explicitly explains polynomial validity at roots of unity. The paper attributes the underlying formula to Schützenberger (1953); I inspected Koornwinder, not the original 1953 article. The resolvent numerator follows by finite geometric summation once (alpha A+beta B)^m=(alpha^m+beta^m)I. Likewise the frontier specialization [m-1 choose u]_q=(-1)^u q^(-u(u+1)/2) follows directly from the product formula at a primitive root. These should be presented as classical ingredients, with conventions checked. This source does not state the three-orientation exclusion. [Koornwinder PDF, Proposition 2.1](https://arxiv.org/pdf/q-alg/9608008)

### Prime-power Fourier minors

Alexeev, Cahill and Mixon, Full Spark Frames (2012), Theorem 9, characterizes prime-power Fourier row selections by uniform distribution modulo divisors. Its two-row case already gives the relevant residue obstruction: two rows in different classes modulo p have no vanishing 2-by-2 minor in F_(p^s). The paper has much broader row-selection results; it does not analyze the specified quantum-torus sum. [Primary paper, Theorem 9 on page 12](https://arxiv.org/pdf/1110.3548)

Osgood, Siripuram and Wu, Discrete Sampling and Interpolation: Universal Sampling Sets for Discrete Bandlimited Spaces (2012), Theorem 4, gives equivalent prime-power Fourier sampling conditions in terms of residue-class counts. This is a second direct predecessor for the Fourier-side mechanism, not a source of the particular resolvent-support construction. [Primary paper, Theorem 4 on page 7](https://arxiv.org/pdf/1204.0992)

Indeed the elementary identity is sufficient here: a Fourier minor vanishes exactly when N divides (r-r')(j-j'). If N=p^s, the graph joining distinct row pairs that admit some vanishing minor is exactly p disjoint cliques, one for each residue modulo p. The reverse direction chooses a column difference N/p when p divides the row difference. A connected forced-zero-minor graph therefore obstructs monomial Fourier equivalence. This graph formulation is a direct inference from the standard arithmetic; it should not be sold as a new Fourier-minor phenomenon.

### Equivalence invariants

Östergård and Valtonen, Equivalence of complex Hadamard matrices (2026), Section 2.3, discusses the established Haagerup invariant and its equivalence to absolute 2-by-2 minor information for complex Hadamard matrices, including row/column equivalence algorithms. This places minor-based inequivalence arguments in an established literature. For the present matrices, arbitrary nonzero diagonal scalings need the zero/nonzero minor pattern, or algebraic cross ratios where entries are nonzero, rather than directly importing a unit-modulus conjugate formula. The retrieved paper does not state the quantum-torus architecture theorem. [Primary article, Section 2.3](https://link.springer.com/article/10.1007/s10801-026-01568-x)

Tadej and Życzkowski, A concise guide to complex Hadamard matrices (2006), Lemma 2.1, also records the Haagerup nonequivalence condition. This is an earlier accessible source for crediting the method. [Author-hosted primary survey](https://chaos.if.uj.edu.pl/~karol/pdf/TZ06.pdf)

## Narrow contribution boundary

The part requiring task-specific work is support isolation for the new columns, not the final Fourier contradiction. It must hold simultaneously for all branch parameters and independent branch gauges, including coordinate wrapping. The new rectangles differ from the older two-orientation rectangles whose zeros were repaired by adding psi. Thus the three-orientation theorem is compatible with the submitted repair of those specific earlier witnesses.

A useful manuscript would state the general elementary graph obstruction separately, credit the above prior ingredients, then prove the precise resolvent-support lemma and architecture corollary. The m=4 exception and finite N=16 two-full-spark examples should remain visible, since they explain why the all-size threshold matters. A targeted comparison or generalization to other orientation triples would make the result's significance clearer; it is not supplied by this search.

No primary-source match was found for the precise identity/phi/psi architecture with independently gauged branches. That is an observation about this bounded search, not evidence that no such theorem exists. Unindexed papers, alternate terminology, older matrix-equivalence literature and unpublished work were not exhausted.

## Search record and limitations

Public web queries included:
- quantum torus resolvent discrete Fourier transform q binomial matrix minors
- Fourier matrix prime power vanishing 2 by 2 minor graph diagonal permutation equivalence
- “quantum torus” “Fourier” “resolvent”
- “Fourier” “prime power” “2x2” minors arxiv
- “q-commuting” “q-binomial theorem” Koornwinder
- “complex Hadamard” “Haagerup” invariants Tadej Zyczkowski
- “quantum torus” “resolvent” “binomial”
- “Discrete Sampling and Interpolation” “Universal Sampling Sets”
- “Full spark frames” Alexeev Cahill Mixon Fourier prime power
- “Koornwinder” “q-commuting variables”
- “Fourier” “zero minor” “connected”
- “quantum torus” “Fourier matrix”
- “q-commuting” “resolvent” “Fourier”
- “Fourier matrix” “minor” “graph” “connected”
- “resolvent” “three orientations”

The decisive comparisons used retrieved primary papers and specific theorem/section text. Unrelated graph-Fourier and noncommutative-torus search hits were not treated as antecedents merely because they share words. No external author was contacted. No claim about all literature, journal acceptance, impact rank or practical Fourier improvement follows from the negative search result.
