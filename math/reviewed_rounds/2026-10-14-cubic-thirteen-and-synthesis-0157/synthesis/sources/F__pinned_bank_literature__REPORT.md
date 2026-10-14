# Signed bank minima prior art comparison

14 October 2026. Literature triage for the exact pinned signed-bank dictionary at N=11 and q=13 over extensions of F23.

## Conclusion

Historical novelty remains unresolved. This bounded search found close classical mechanisms, but did not locate a publication establishing the exact pinned minima studied here. Failure to locate an equivalent statement is not proof that none exists, nor proof that the result is not an immediate specialization of a general theorem.

The potentially distinctive contribution is the exact representation count in the explicitly restricted dictionary, together with complete original-bank witnesses and lower-bound certificates. The root-of-unity expansion, Weyl coefficient extraction, common-annihilator method, and general phenomenon of field-dependent minimal supports all have substantial prior literature.

## Mathematical status and scope

The base-field independent audit accepts b4(F23)=16. The new quadratic-field independent audit accepts b4(F23^2)=14 and, by embedding its witness and applying the reviewed lower bound, b4(F23^d)=14 whenever d is even and 5 does not divide d. The earlier degree-five-subfield result is a separate dependency: b4(F23^d)=12 when 5 divides d.

Here b4 counts actual original summands of the form

    B_(epsilon,delta)(alpha,beta;w)
      = (1/11) sum_(j=0)^10 w_j
        (I-alpha S^epsilon-beta 13^(epsilon delta j) T^delta)^(-1),

where S e_t=e_(t+1 mod 11), T e_t=13^t e_t, epsilon and delta independently equal +1 or -1, and 1-alpha^11-beta^11 is nonzero. The literal target is F[k,t]=13^(-kt). All legal beta values, including zero, are permitted in the minimization. Exactly one effective alpha node is required in each cross-sign orientation, and both are pinned to alpha=4. Grouping equal-alpha amplitudes is bookkeeping, not a replacement of actual-bank counting. No new generator, derivative atom, singular limit, infinite node, transformed target, pre/post map, or trace-bank primitive is admitted.

The quadratic result is no longer pending independent review. Its acceptance archive is:

    Signed_Bank_Quadratic_Field_Fourteen_Independent_ACCEPT_2026-10-14.zip
    SHA-256 cc539392243a145071e9d7a1211b3a4082fa4f84578a5ef4df24e9a7d85fb898

The acceptance excludes the candidate's complete 529-polynomial factor census, counts of eligible supports, and search-order claims. Those claims are unnecessary for the accepted fourteen-bank witness and minimum. Neither acceptance establishes an unpinned optimum, all odd extension degrees not divisible by five, characteristic-zero transfer, an asymptotic family, historical novelty, or arithmetic/FFT speed improvement. These are independent computational/proof audits, not journal peer review.

## Closest primary literature

### Root of unity quantum binomial expansion

Olga Holtz, Volker Mehrmann and Hans Schneider, *Potter, Wielandt, and Drazin on the matrix equation AB=omega BA, with some new answers to old questions*. Theorem 2 and Corollary 3 formulate the quantum-binomial expansion over general rings and its root-of-unity collapse. Their paper also identifies Potter's 1950 and Schutzenberger's 1953 antecedents.

Source: https://arxiv.org/pdf/math/0512607

Applying this mechanism to the clock/shift pair gives X_j^11=(alpha^11+beta^11)I. The legal finite geometric inverse then follows directly. The collapse and ordered Gaussian coefficients should be credited as classical ingredients. The cited paper does not establish this Fourier-target bank minimum.

### Weyl coefficient extraction and quadratic Fourier kernels

Shamgar Gurevich and Ronny Hadani, *On the diagonalization of the discrete Fourier transform*, Applied and Computational Harmonic Analysis 27 (2009), 87-99. Equations (1.2)-(1.3) give trace-based Weyl coefficient extraction and quadratic-phase kernels for Weil operators; Section 4 relates the Fourier operator to the Weil representation.

Source: https://people.math.wisc.edu/~sgurevich/YACHA673.pdf

This is a close classical explanation for the target's quadratic Weyl coefficients. Their representation uses complex scalar values; it must not be cited as if it states the literal F23 normalization or the present resolvent-bank optimization. The finite-coefficient identities still need their own algebraic derivation and convention checks.

### Prony interpolation over finite fields

Joris van der Hoeven and Gregoire Lecerf, *Sparse polynomial interpolation: Faster strategies over finite fields*, manuscript dated 2 May 2024. Section 5 and Algorithm 4 relate geometric-progression samples to rational generating functions, annihilating polynomials, root recovery, and amplitude reconstruction, with explicit discussion of coefficient fields and extensions.

Source: https://www.texmacs.org/joris/ffsparse/ffsparse.pdf

The bank argument's exponential moment sums, annihilator roots, and Vandermonde amplitude recovery belong to this established mechanism. Sparse polynomial interpolation has a different input/output problem and does not itself supply the bank-count theorem.

### Common recurrences for unequal length sequences

Georg Schmidt and Vladimir R. Sidorenko, *Linear Shift-Register Synthesis for Multiple Sequences of Varying Length* (2006). The paper studies the shortest common recurrence for multiple finite sequences over a field and the unequal-length case.

Source: https://arxiv.org/pdf/cs/0605044

This closely matches the stacked annihilator equations from the nine- and seven-term windows. The distinction is important: a minimum-degree recurrence need not have distinct nonzero roots in the allowed coefficient field. The present support problem imposes those additional requirements. The Hankel matrix rank is unchanged by scalar extension; availability of admissible split supports changes.

### Relative Waring ranks and splitting conditions

Bruce Reznick and Neriman Tokcan, *Binary forms with three different relative ranks*, Proceedings of the American Mathematical Society 145 (2017), 5169-5177. Theorem 2.1 gives a Hankel-kernel criterion involving a product of distinct linear factors. The paper also constructs forms with at least three different minimal ranks over different fields.

Sources: https://arxiv.org/pdf/1608.08560 and https://doi.org/10.1090/proc/13666

This is a particularly close conceptual precedent for field-sensitive minimum support controlled by squarefree splitting. Its stated field hypothesis is K contained in C, and its atoms are powers of linear forms. It does not settle the finite-field signed-bank dictionary. It does show that neither three field-dependent minima nor splitting-controlled rank is a new general phenomenon.

### Finite field and simultaneous Waring decomposition

Michel Lavrauw and Ferdinando Zullo, *Waring identifiable subspaces over finite fields*. The introduction discusses simultaneous Waring decompositions of tuples of forms, including differing degrees. The paper develops Waring subspaces and classifications for particular Veronese settings over finite fields.

Source: https://arxiv.org/pdf/2207.13456

This provides relevant finite-field vocabulary and nearby geometric literature. Its stated classifications do not identify the present constrained degree-eight/degree-six moment pair or the four-orientation resolvent-bank problem.

## Mathematical deduction connecting the moment problem to Waring decomposition

The following is a mathematical deduction from the supplied moment identities, not a theorem quoted from a source and not an equivalence with the full bank problem.

Reindex the necessary moment windows as

    m_n = v_1(n+1),  0 <= n <= 8,
    s_n = v_2(n+2),  0 <= n <= 6.

Define binary forms

    f_8(X,Y) = sum_(n=0)^8 binom(8,n) m_n X^(8-n) Y^n,
    f_6(X,Y) = sum_(n=0)^6 binom(6,n) s_n X^(6-n) Y^n.

For a shared finite support A contained in K*, the moment identities

    v_1(a) = sum_(x in A) A_(1,x) x^a,
    v_2(a) = sum_(x in A) A_(2,x) x^a

are equivalent, by the ordinary binomial expansion, to simultaneous expressions

    f_8 = sum_(x in A) lambda_x (X+xY)^8,
    f_6 = sum_(x in A) mu_x (X+xY)^6,

with lambda_x=x A_(1,x) and mu_x=x^2 A_(2,x). The converse divides by x and x^2, which is legitimate because the support is nonzero. Coefficients for either individual form may vanish; the common support is their union. Characteristic 23 exceeds both degrees, so the binomial coefficients used here are invertible.

Thus the necessary-window optimization is a restricted simultaneous Waring/Prony problem with affine nonzero nodes. It excludes the zero and projective-infinity nodes. Its common annihilator and squarefree-splitting restrictions have classical interpretations.

This correspondence does not prove that any admissible moment support lifts to a representation of all 121 target entries. The remaining sectors and orientations impose additional compatibility equations. The full original-bank witnesses and their literal reconstruction are essential separate attainment evidence. No general formula equating b4(K) to twice a moment-support rank plus two is asserted.

## Search scope and limitations

The search was performed on 14 October 2026 using public web search and primary papers available through arXiv, author/institutional pages, and publisher pages. Representative query families included:

- finite Fourier transform, Weyl operators, resolvent decomposition, quantum plane, and root-of-unity quantum binomial theorem;
- Fourier matrix, inverse or cyclic bidiagonal decomposition, Green functions, and sums of resolvents;
- Prony over finite fields, shared annihilators, multisequence linear complexity, and unequal-length recurrence synthesis;
- relative Waring rank, squarefree splitting, simultaneous Waring decomposition, and finite-field Waring subspaces;
- conceptual labels such as inverse Weyl and signed-bank Fourier representations.

Title and author searches followed promising results. The private raw weights and numerical moment lists were not submitted to public search. Search-result snippets from aggregators were used for discovery, but the comparison above relies on primary papers opened for inspection. Search results concerning Weyl-Titchmarsh functions, continuous resolvent algebras, Deligne-Lusztig Green functions, and unrelated FFT algorithms were not treated as equivalent merely because their terminology overlapped.

This was not an exhaustive MathSciNet or zbMATH review, a full citation-network traversal, or a multilingual historical search. Terminology may differ, relevant papers may be unindexed or inaccessible, and a general theorem may subsume an instance without naming its numerical parameters. No specialist author or outside party was contacted. No research code was executed for this comparison, and no external service was written.

## Publication framing and remaining checks

A defensible formulation is: an exact, field-sensitive minimum for a specified pinned signed-resolvent-bank dictionary, proved using classical quantum-binomial and common-annihilator tools and accompanied by independently checked witnesses. It should not claim a new Fourier-transform mechanism or a new general phenomenon of field-dependent rank.

Before submission:

1. Put the complete dictionary and both alpha pins in the theorem statement. Preserve the distinction between effective nodes and actual summands, and between a beta=1 witness and a lower bound allowing every legal beta.
2. Explain why this dictionary and the alpha=4 pins are mathematically or operationally natural. A verified isolated instance can still have limited significance without that motivation.
3. Present a self-contained proof with reproducible exact certificates. Separate numerical premises, exhaustive finite claims, and general algebraic implications.
4. Credit the classical mechanisms and discuss the moment-to-Waring connection without overstating a full-bank equivalence.
5. Separate the accepted quadratic witness and minimum from the unaudited full factor census. Keep unresolved extension degrees and unrestricted architecture questions explicit.
6. Obtain broader literature comparison and ordinary external mathematical review before making historical priority or publication-strength claims.

## Supplied research sources inspected

- Base-field attainment and lower-bound compatibility: `pinned_sixteen_acceptance/REVIEW.md`.
- Quadratic candidate and its declared factor-gate scope: `quadratic_fourteen_candidate/REPORT.md`.
- Earlier extension lower-bound proof: `quadratic_fourteen_candidate/sources/EXTENSION_LOWER_BOUND_PROOF_REVIEW.md`.
- Current quadratic acceptance and exclusions: `quadratic_fourteen_acceptance/INDEPENDENT_REVIEW.md`.

The supplied sources were read as research documents. This comparison does not claim to have rerun their scientific checks or independently proved all of their accepted results.
