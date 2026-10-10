# C03 novelty audit: reciprocal diagonal-pencil resultant

10 October 2026, 15:29 UTC. Read-only primary-literature comparison. No source program was executed or imported, and no external document was changed.

## Verdict

**C03 is a valid, generically sharp explicit factorization. It is not presently a demonstrated mathematical breakthrough or a novelty-cleared standalone research paper.** The strongest defensible classification is a specialized formula/application of classical resultant, determinant-weight, Newton-polygon, and reciprocal-polynomial theory. The particular family and closed exponents may be original; this search did not establish either priority or an exact earlier statement of the whole theorem.

This is not a rejection of correctness. The arbitrary-matrix proof is already closed at R15. A classical proof mechanism alone does not prove that its particular consequence has previously been printed. Conversely, failure to locate an exact formula does not establish research novelty or significance.

## Exact claim and source binding

The authoritative claim is section A of `research_cycle_0958/algebra/final_v1/PROOF_CLOSURE.md`, SHA-256 `f6412a2cb78457a2fddd62a6e688095cb82528b4457ad1454dbbe069179937d6`, which was read in full and rehashed. Its assumptions are arbitrary square matrices A,B over any commutative ring S, and D(w)=diag(1,w,...,w^(m−1)). It uses the fixed homogeneous degree-(m,m) resultant of

    P0(a,w)=det(A−aD(w)AD(w)),
    P1(a,w)=det(B−awD(w)BD(w)).

With T=m²(2m−1), v=m(m−1)(4m+1)/6 and b=m(m−1)(2m−1)/6, it proves

    R(w)=w^(v+b)(w−1)^(m²)V(w+w^(-1)),     deg V≤b,
    w^T R(w^(-1))=(−1)^(m²)R(w).

The factors at 0 and 1 and degree b are attained generically. Individual specializations may raise vanishing orders, drop degrees, or give R=0. The adjacent-Hankel formulation is a specialization, not the source of the universal mechanism.

A fresh connector read at 15:27 UTC verified the existing [Theorem register C03 row](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=404576783&range=A33:J33), Q17 row 20, and Catalogue row 6. C03 and Q17 explicitly say proof closed, R15, and formula/application priority unresolved. The Catalogue retains historical prose about an outstanding arbitrary-pencil audit, but its current overlay also records closure. No proof gate is reopened here. Exact live responses are preserved in `LIVE_SHEET_READ.json`.

## What the literature actually matches

### 1. Exact overlap: the reciprocal quotient is a known trace polynomial

Matthew Baker, *Reciprocity via Reciprocants*, Proposition B.1, manuscript p. 8, proves for a ring R that an even-degree reciprocal polynomial g has a unique trace polynomial h with g(w)=w^m h(w+w^(-1)). Remark B.2, p. 9, gives h0=2, h1=x and hn=x h(n−1)−h(n−2), exactly the recurrence used by C03. Thus neither the quotient variable nor the no-division-by-2 mechanism is new. C03's fixed-grade, degree-drop formulation is accommodated by the same coefficientwise Laurent-invariant argument.

This is an exact match to one component, not the full pencil theorem. Baker's Proposition 2.3, p. 3, concerns the square resultant of two monic even-degree reciprocal input polynomials. C03's inputs are generally not reciprocal in a at fixed w, so that separate square-resultant theorem must not be substituted for C03. [Primary full text and propositions](https://arxiv.org/html/2309.02512v2#A2); [PDF, pp. 3, 8–9](https://arxiv.org/pdf/2309.02512).

An older research use appears in Gross–McMullen, *Automorphisms of even unimodular lattices and unramified Salem numbers* (2002), §2, manuscript p. 5: its trace polynomial is defined by S(x)=x^n R(x+x^(-1)). That source has additional real/separability assumptions for its surrounding application; Baker is the directly checked arbitrary-ring statement. [Author's manuscript](https://people.math.harvard.edu/~ctm/papers/home/text/papers/unim/unim.pdf#page=6).

### 2. Exact classical Hankel/Bezoutian connection, but a different identity

García-Armas–Ghorpade–Ram, *Relatively Prime Polynomials and Nonsingular Hankel Matrices over Finite Fields*, Proposition 3.4, manuscript pp. 3–4, proves Barnett's factorization

    Bn(u,v)=Bn(u,1) Hn(u,v) Bn(u,1)

for a monic degree-n u and deg v<n over a field. Hn is built from the Laurent coefficients of v/u, and coprimality is not required. Proposition 2.2 gives the usual coprimality/nonsingularity correspondence. This establishes that a determinant/resultant/Hankel bridge is classical. It does not identify C03's two arbitrary matrix pencils with this rational-function Hankel construction, and it does not supply its v,b exponents. [Primary full text, §3](https://arxiv.org/html/1011.1760#S3); [PDF](https://arxiv.org/pdf/1011.1760).

Ćurgus–Dijksma, *A proof of the main theorem on Bezoutians*, eqs. (7)–(9), manuscript pp. 3–4, explicitly connects the Sylvester resultant matrix to the Bezoutian and their nullities. Its §5, eq. (12), p. 5, handles padded degrees: nullity is n−max(deg f,deg g)+deg gcd(f,g), accounting for a common root at infinity. Thus fixed-degree bookkeeping and singular leading-coefficient cases are established elimination practice, not a new general elimination theory. [Primary manuscript](https://arxiv.org/pdf/1208.2385).

Cayley's original *Note sur la méthode d'élimination de Bezout* (1857), pp. 366–367, gives the coefficient matrix of the divided difference of two homogeneous binary forms as an eliminant. This is the historical Bezout/Cayley construction, not this monomial diagonal deformation. The repository's indexed text of p. 366 was readable; full scan OCR was not available in this pass, and direct download returned HTTP 403. I do not claim a full image-level audit of both historical pages. [Original scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN243919689_0053/LOG_0032.pdf).

### 3. The resultant reciprocity and collision factor use standard covariance

For two degree-m binary forms, simultaneous change of their two variables by C multiplies the resultant by det(C)^(m²). Swapping coordinates yields (−1)^(m²); the affine substitution a=1+εt yields ε^(m²). C03 combines these with determinant row/column scaling and the fact that each pencil entry vanishes to first order at (a,w)=(1,1). Its ε^(2m²) coefficient scaling minus ε^(m²) change-of-variable weight leaves (w−1)^(m²).

That is the audit's direct identification of C03's argument as a specialization of classical covariance, not a claim that a source prints the C03 formula. Busé–Jouanolou, *On the discriminant scheme of homogeneous polynomials*, §4.3, proof of Proposition 4.13, manuscript p. 43, explicitly invokes and writes the resultant linear-coordinate covariance, referring to Jouanolou (1991), §5.13.1. The general original Jouanolou treatise was not obtained in full. [Primary article, p. 43](https://arxiv.org/pdf/1210.4697#page=43).

### 4. The w-adic exponent is a specific Newton-polygon calculation

Sturmfels, *On the Newton Polytope of the Resultant* (1994), Theorem 2.1, journal p. 213, and Theorem 4.1, p. 220, describe resultant initial forms under coefficient weights. C03's mixed-minor calculation identifies the particular coefficient valuations j(j−1)+ej. Its opposite-parity root slopes make the root differences non-cancelling, giving v=sum(i,j) min(2i,2j+1). This is a computed specialization of established valuation machinery; an exact published match to that matrix family was not found. [Primary article](https://www.maths.tcd.ie/EMIS/journals/JACO/Volume3_2/m4496732732u7744.fulltext.pdf).

Nart, *Local computation of differents and discriminants*, §3.1, Definition 3.1, manuscript p. 16, defines the Newton-side resultant contribution as min(EH′,E′H). It is a close statement-level match to the min contribution mechanism. C03 works over a formal Laurent field with generic coefficients and does not require or inherit the hypotheses or guarantees of Nart's full local-field algorithm. [Primary manuscript](https://arxiv.org/pdf/1205.1340#page=16).

### 5. Recovery through Hankel/resultant identities already has prior applications

Uteshev–Baravy, *Solution of Interpolation Problems via the Hankel Polynomial Construction*, Theorem 6.2, eqs. (6.6)–(6.7), derives resultant formulas from Hankel determinants of samples p(xj)/q(xj). This is a genuine application neighbor, with distinct nodes and nonzero sampled numerator/denominator assumptions. It is not the same pair of diagonal pencils or the same reciprocal-quotient interpolation. Its algebraic-specialization argument also shows why extension from generic inputs is not alone a novelty discriminator. [Primary full text, §6](https://arxiv.org/html/1603.08752#S6).

## What can still fairly be claimed

Suggested strongest defensible wording:

> We explicitly determine generically sharp universal factors and the reciprocal residual degree for the resultants of a specified pair of monomially deformed matrix pencils, over arbitrary commutative rings. The resulting trace-polynomial representation reduces interpolation to b+1 admissible quotient nodes. The derivation uses classical resultant and Newton-polygon tools; priority for this particular formula remains to be established.

Do not claim a new Bezoutian identity, a new reciprocal invariant, a new theory of elimination, or a general sparse-recovery/FFT breakthrough from C03 alone.

The sampling benefit is concrete: b+1 instead of the conservative T+1 full-grade samples. Both are Θ(m³); their ratio tends to six. Reciprocity alone is only the final factor-two reduction from residual grade 2b to b. A lower sample count is not an end-to-end arithmetic or bit-complexity improvement without paying for resultant evaluations, admissible node supply or field extensions, interpolation, candidate lifting, degeneracy handling, and final recovery certification.

## Remaining novelty and paper-worth gate

1. **Formula priority:** compare the exact two pencils, exponent sequence, homogeneous convention and universal specialization against earlier monomial-deformation and structured-elimination literature. An abstract or a theorem about arbitrary resultants is not an exact printed-family match. Current searches establish component overlap, not exhaustive worldwide priority.
2. **Significance:** supply a consequential application, a genuinely stronger algorithm with complete cost accounting, or a broader structural theorem that is not merely the same covariance and minimum-weight calculation with relabeled exponents.
3. **Editorial decision:** as it stands, C03 is best used as a supporting proposition or potentially a focused formula note after priority clearance. It does not presently justify leading a standalone paper as a major breakthrough. This is an assessment of the evidence and mathematical contribution, not a prediction that no journal could publish a careful note.

Proof correctness remains closed at the pinned source. This pass changes the specificity of the prior-art comparison, not the accepted theorem.
