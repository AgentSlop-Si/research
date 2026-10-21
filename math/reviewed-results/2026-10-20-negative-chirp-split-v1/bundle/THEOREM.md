# Original negative-chirp theorem: complete fusion candidate

Date: 2026-10-20 UTC. **COMPLETE AUTHOR CANDIDATE; SEPARATE WHOLE-FUSION REVIEW REQUIRED.** All ten residual-rank review groups and the baseline row review are accepted and pinned. The explicit accepted coverage is 576 of 576 ordered cycle pairs. `LEAF_GATE.json` reports PASS. This document is the end-to-end theorem submitted for fresh independent review, not an author claim of independent acceptance.

## 1. Exact theorem and logical scope

Let

\[
\mathcal N_- = \{N=5m : m\in\mathbb Z_{>0},\ N\text{ odd},\ \gcd(m,5)=1,
                         \ N\equiv3\pmod4\}.
\]

For every \(N\in\mathcal N_-\) and every primitive complex \(N\)-th root \(\omega\), index coordinates by \(0,\ldots,N-1\), and set

\[
 F[i,j]=\omega^{ij},\qquad A[j,j]=\omega^{h j^2},\quad h=(N+1)/2,
 \qquad B=(F^{-1}+A)^{-1}.
\]

The displayed inverse exists, and there are no matrices satisfying

\[
 B=L_1(I-W_1)^{-1}R_1+L_2(I-W_2)^{-1}R_2,                         \tag{T}
\]

where every \(L_r,R_r\) is an arbitrary complex diagonal matrix on these fixed coordinates, each \(W_r\) has row action

\[
 (W_rx)_i=w_{r,i}x_{\pi_r(i)}
\]

for a Hamiltonian cycle \(\pi_r\), each edge weight \(w_{r,i}\) is an arbitrary complex number, and \(\rho_r=\prod_iw_{r,i}\ne1\). Zero weights, singular masks, and identically zero masks are explicitly allowed. The two cycles may coincide or differ. No endpoint permutation independent of a cycle is allowed.

There is **no lower-size cutoff** in this statement. Define the precise exceptional set

\[
 \mathcal E_- =\{N\in\mathcal N_-:\text{there is a primitive }\omega
                 \text{ for which (T) holds}\}.
\]

The complete leaf gate is satisfied, and the conclusion is \(\mathcal E_-=\varnothing\), and, more strongly, (T) fails for every primitive character at each eligible size. This is an impossibility statement, not a construction or sufficiency classification. It neither claims an exact minimum of three summands nor concerns unrestricted Fourier algorithms, unmatched endpoint permutations, products, three-or-more summands, the positive-Gauss family, or moduli divisible by 25. No historical-novelty claim is made.

## 2. Exact inverse, all primitive characters, and the negative sign

Put

\[
 G=\sum_{x=0}^{N-1}\omega^{h x^2},\quad
 C[i,j]=\omega^{-h(i+j)^2},\quad D[i,j]=\omega^{-h i^2}\delta_{ij}.
\]

All following congruences are modulo \(N\), with \(2h=1\). Completing the square gives

\[
 (FAF)[i,j]=\sum_x\omega^{hx^2+(i+j)x}
            =G\omega^{-h(i+j)^2}=GC[i,j].
\]

Likewise

\[
 (FAC)[i,j]=\omega^{-hj^2}\sum_x\omega^{(i-j)x}
            =N\omega^{-hi^2}\delta_{ij}=ND[i,j],\qquad AD=I.
\]

The orthogonality sum uses primitivity, not primality of \(N\). Expanding the product now yields

\[
 (I+FA)(F-GC+NGD)=(1+NG)F.                                    \tag{1}
\]

For the opposite-sign product, the bijection \((x,y)\mapsto(u,v)=(x-y,x+y)\) on \((\mathbb Z/N\mathbb Z)^2\) gives

\[
 G\overline G=\sum_{u,v}\omega^{huv}=N.                         \tag{2}
\]

Thus \(|G|=\sqrt N\). Every eligible \(N\) is at least 15, so \(|NG|=N^{3/2}>1\), proving \(1+NG\ne0\). The Fourier matrix is invertible by character orthogonality. Multiplying (1) by \(F^{-1}\) on the left proves that

\[
 (F^{-1}+A)\frac{F-GC+NGD}{1+NG}=I.
\]

A right inverse of a square complex matrix is its inverse. Therefore

\[
                    B=\frac{F-GC+NGD}{1+NG}.                  \tag{3}
\]

The only non-elementary number-theory input used to determine the branch is the standard odd-modulus quadratic Gauss-character identity
\(G_N(a)=(a/N)G_N(1)\) for units \(a\), including nonsquarefree odd moduli. One primary reference is Gurevich, Hadani and Howe, *Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation*, section 3.1, equation (3.3) and Remark 3.3, <https://arxiv.org/html/0808.2447>. Applying this identity to \(-1\), and using \((-1/N)=(-1)^{(N-1)/2}\), gives

\[
 \overline G=(-1)^{(N-1)/2}G,\qquad
 G^2=(-1)^{(N-1)/2}N=-N.                                      \tag{4}
\]

This applies to every primitive \(\omega\): writing \(\omega=e^{2\pi i a/N}\) simply replaces the unit Gauss coefficient by \(ah\). No sign of a square root is selected. In particular \(G\) is nonzero purely imaginary, \(NG=-G^3\), and the denominator in (3) is \(1-G^3\), not \(1+G^3\).

## 3. The five-coordinate target and exact zero-edge restriction

Let \(S=(0,m,2m,3m,4m)\), in that fixed order, and let \(\eta=\omega^{m^2}\). Because \(\gcd(5m,m^2)=m\), the order of \(\eta\) is exactly five. Also \(h\equiv3\pmod5\). Substituting these congruences and (4) into (3) gives, entry for entry,

\[
 B[S,S]=\frac{H_-(G,\eta)}{1-G^3},\quad
 H_-(g,\eta)_{ij}=\eta^{ij}-g\eta^{-3(i+j)^2}
                         -g^3\eta^{-3i^2}\delta_{ij}.          \tag{5}
\]

The denominator is nonzero by the earlier modulus argument. There is no reduction of a primitive \(N\)-th root to a nonprimitive fifth root, and the target has the negative cubic diagonal sign.

**Principal restriction lemma.** For an arbitrary Hamiltonian row cycle \(\pi\) on \(N\) coordinates and arbitrary weights \(w_i\) with \(\rho=\prod_iw_i\ne1\), every nonempty principal restriction of its Green matrix is the Green matrix of the contracted Hamiltonian cycle, including all zero weights.

**Proof.** Since \(W^N=\rho I\), polynomial multiplication proves

\[
 (I-W)^{-1}=\frac{I+W+\cdots+W^{N-1}}{1-\rho}.                 \tag{6}
\]

For each selected vertex, follow \(\pi\) to the next selected vertex; give that induced edge the product of all original weights along that arc. These arcs partition all original edges, so the product of induced weights is exactly \(\rho\). Thus the induced denominator is legal and equals the original one. For two distinct selected vertices there is exactly one directed path of length less than \(N\) in the original cycle. Its weight is the numerator of the corresponding entry of (6). Concatenating contracted arcs gives the same product, hence the same entry. A diagonal numerator is one in both matrices. For a singleton restriction the contracted self-edge has weight \(\rho\), giving the same diagonal entry \(1/(1-\rho)\). This proves equality. No division by an edge occurs anywhere, so a zero product is retained exactly. Any ordering of the selected set merely determines the induced coordinate labels. ∎

Diagonal multiplication commutes with principal restriction entrywise:
\((LGR)[S,S]=L[S,S]G[S,S]R[S,S]\). Therefore every representation (T) restricts to a representation of (5) by two five-coordinate Hamiltonian Green terms with arbitrary restricted masks and legal denominators. Multiplying both sides by \(1-G^3\) can be absorbed into the left masks. Thus any (T) yields a representation of the unscaled polynomial target \(H_-(G,\eta)\) in precisely the same grammar.

## 4. One closed necessary system for every pair of five-cycles

Fix the two induced cycles \(\pi,\tau\). Choose nonzero projective pairs
\(u_i=[a_i:b_i]\), \(v_j=[c_j:d_j]\), one for each of the five rows and five columns. Put

\[
 U_{ii}=a_i,\quad U_{i,\pi(i)}=b_i,\qquad
 V_{jj}=c_j,\quad V_{\tau^{-1}(j),j}=d_j,
\]

with all other entries zero, and put \(T=UHV\). Let \(M(H,U,V)\) be the 25-by-11 matrix whose row indexed by \((i,j)\), in order \(5i+j\), consists of the ten coefficient slots of

\[
                     V_{ij}X_i+U_{ij}Y_j
\]

followed by \(T_{ij}\). The symbols \(X_i,Y_j\) name coefficient columns; they are not extra projective variables. The necessary system is

1. \(T_{ij}=0\) whenever \(j\notin\{i,\pi(i),\tau(i)\}\).
2. All \(\binom{25}{11}=4,457,400\) maximal 11-column minors of \(M\) vanish.

We use selected minors only to contradict this universal necessary condition. We never assert that rank at most ten implies consistency of the ten-column coefficient system when its rank drops.

**Necessity for nonsingular masks.** Write the two summands as \(P,Q\). Since their masks and Green matrices are invertible, so are \(P,Q\). The row support of \(P^{-1}=R_1^{-1}(I-W_1)L_1^{-1}\) is \(\{i,\pi(i)\}\); the column support of \(Q^{-1}\) is \(\{j,\tau^{-1}(j)\}\). The diagonal entry of each inverse row or column is nonzero. Row- and column-normalizing therefore gives

\[
 U=D_\lambda P^{-1},\qquad V=Q^{-1}D_\mu,
 \qquad U(P+Q)V=D_\lambda V+UD_\mu.                            \tag{7}
\]

Equation (7) proves both sets of equations: the right side has the required support, and its entries give coefficients \(X_i=\lambda_i,Y_j=\mu_j\) for the target column of \(M\). Edges may already be zero; only mask invertibility was used.

**Projective polynomiality.** Rescale the \(i\)-th row pair by \(\lambda_i\) and the \(j\)-th column pair by \(\mu_j\). An off-support equation has weight \(\lambda_i\mu_j\). For a selected set \(E\) of eleven rows of \(M\), let \(n_i\) and \(m_j\) count its matrix row and column indices. Every determinant term uses each \(X_i\) and each \(Y_j\) coefficient column once and the target column once. Factoring scales rowwise and then from the coefficient columns shows that its weight is

\[
                 \prod_i\lambda_i^{n_i-1}\prod_j\mu_j^{m_j-1}.\tag{8}
\]

If some \(n_i=0\), coefficient column \(X_i\) is zero; if some \(m_j=0\), column \(Y_j\) is zero. Such a minor is identically zero. Otherwise all exponents in (8) are nonnegative. The nonzero minors are therefore multihomogeneous polynomials on \((\mathbf P^1)^{10}\), with total row degree six and total column degree six. Their coefficients are polynomial in the entries of \(H\). The necessary system is closed and well-defined on the full product of projective lines, not just an invertible or nonzero-coordinate chart.

**Necessity for arbitrary singular masks.** Replace each zero entry of each of the four diagonal masks by \(t\), retaining every originally nonzero entry and every edge weight. Legal Green denominators remain fixed. This produces invertible summands over \(\mathbb C((t))\), whose sum \(H(t)\) lies in \(\mathbb C[[t]]^{5\times5}\) and satisfies \(H(0)=H\). Choose the sparse inverse pairs in (7). For each of the ten pairs, divide both coordinates by the common smallest power of \(t\) among its nonzero entries. The normalized coordinates lie in \(\mathbb C[[t]]\) and at least one coordinate is a unit. Consequently every pair has a nonzero projective specialization at \(t=0\).

All normalized equations still vanish over \(\mathbb C((t))\) by multihomogeneity. Since their evaluations now lie in \(\mathbb C[[t]]\), reduction modulo \(t\) gives all equations for \(H\) and the ten nonzero limiting pairs. There is no need for a finite limit of \(X,Y,\lambda,\mu\). This covers an entirely zero endpoint mask as well as any partial singularity. It never divides by an edge or a single projective coordinate. Hence every allowed original representation gives a point of one of these closed necessary systems.

Scaling \(H\) by a nonzero scalar preserves the necessary zero set: the off-support entries and each augmented minor are linear in \(H\). This independently confirms the scalar step following (5).

## 5. The exact parameter domain and the accepted algebraic leaves

Write \(K=\mathbb Q[z]/(z^4+z^3+z^2+z+1)\). Every computational leaf uses the same polynomial \(H_-(g,z)\) in characteristic zero. Its exclusion domain is

\[
 \mathcal D=\{(g,\eta):g\in i\mathbb R\setminus\{0\},
                          \eta\text{ a primitive fifth root}\}.
\]

For clarity the formal positive variable in leaf tests can be called \(n=-g^2>0\); it need not be an integer or an eligible full-matrix dimension. The full theorem will use only the actual values \(n=N\) established in (4). A theorem on the wider algebraic test domain does not enlarge the claimed original family.

The accepted row/block source is `negative_chirp_exact_row_elimination_20261020`, author manifest `5784fa0d03c24bd4c8a5eaf8716c94791368b8fd907920fc0efdff8716f2dd6d`. Its separate final review manifest is `7a7188fb1dbd3ed45e611cdffba98dacefb04d284ee1495aee29a053d07b2dfb`. The fusion verifies every payload of both manifests, not just these names.

### 5.1 Why the row/block lemma is a complete implication

For an unsupported entry define

\[
 A_{ij}=H[\,(i,\pi(i)),\ (j,\tau^{-1}(j))\,],\qquad
 I_j=\{i:j\notin\{i,\pi(i),\tau(i)\}\}.
\]

The equations are \(u_i^tA_{ij}v_j=0\). For \(i,k\in I_j\), eliminating the shared nonzero \(v_j\) gives

\[
 u_i^t C_{ikj}u_k=0,\qquad C_{ikj}=A_{ij}JA_{kj}^t,
 \quad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.                \tag{9}
\]

Every block uses two row indices and two column indices whose sets intersect in at most one element: neither \(i\) nor \(\pi(i)\) equals \(j\), and \(\tau^{-1}(j)\ne i\). The accepted exact block calculation covers all 90 such unordered two-by-two minors, and ordering changes only their determinant sign. The four-embedding norm and negative-axis split of each determinant has gcd 1 or a power of \(n+1\); thus all these blocks, and hence all transitions, are invertible throughout \(\mathcal D\).

Equation (9) consequently transports directions bijectively as \(u_k\sim JC_{ikj}^t u_i\). A spanning forest expresses directions by one full projective root per component. Reverse edges use adjugates. A polynomial scalar removed from an entire transport matrix cannot vanish on \(\mathcal D\): otherwise its undivided product of invertible matrices would be zero. This statement does not justify discarding arbitrary scalar contents of equations. Those contents are explicitly retained and separately tested.

Every non-tree or repeated-column edge imposes a homogeneous binary quadratic on its component root. In 384 explicitly identified ordered pairs, two selected quadratics and their contents yield a nonzero homogeneous-resultant obstruction. Their exact necessary \(n\)-candidate polynomials have the following distribution:

- 231 copies of 1;
- 115 copies of \((n+1)^4\);
- 11 copies of \(n^2(n+1)^4\);
- 22 copies of \((n+1)^8\);
- 3 copies of \(n^4-n^3+n^2-n+1\);
- 2 copies of \(n^2\).

None has a positive real zero. For the only alternating factor, multiplication by \(n+1\) gives \(n^5+1>0\). The records identifying every pair and its actual factors are `EMPTY_PAIR_ELIMINANTS.json`; the accepted review reconstructs the coefficients. The fusion separately checks that those records match its own enumerated \(\pi,\tau\). These are 384 specific exclusions, not an assumed count.

### 5.2 Why the residual rank-leaf mechanism preserves every boundary

The other 192 pairs form 28 residual symmetry orbits. Each representative's accepted rank leaf begins with the same invertible-block projective transports. Selecting only some transported quadratic equations weakens the necessary system, which is safe when proving emptiness.

Representative 7 uses a monic two-root algebra after retaining the chart guards. For a quadratic \(q=ax^2+bxy+cy^2\), it chooses \(k\) and retains \(A=ak^2-bk+c\). When \(A\ne0\), the omitted point \([-k:1]\) is not a root. The vector \([A-kt:t]\), with \(t^2+(b-2ka)t+aA=0\), covers every root. The tensor product of the two quadratic algebras covers both components, including repeated roots. If an original minor vanishes at a root evaluation, the evaluation is a nonzero functional annihilating multiplication by that minor, so its multiplication determinant vanishes. The accepted exact norm of this determinant has necessary factor \((n+1)^{32}\); all retained chart and content guards also have no positive zero. This method is used only for representative 7.

Every other residual leaf uses full homogeneous minors and prescribed-degree resultants. A connected graph retains one complete root \([x:y]\). A split graph has a two-vertex component with selected relation \(x(ax+by)=0\) or \(y(bx+cy)=0\), where the retained \(b\) guard is proved nonzero on \(\mathcal D\). Its exhaustive roots are, respectively, \([0:1],[b:-a]\), or \([1:0],[c:-b]\). These pairs remain nonzero and distinct even when \(a\) or \(c\) vanishes. The other component retains a complete homogeneous root. No discriminant or square-root branch is assumed.

An original column direction is reconstructed as \(JA_{ij}^t u_i\) using one off-support row. It is nonzero because the block and row direction are nonzero and the block is invertible. Thus no rank-zero column continuum is lost. Each removed raw quadratic, row-direction, column-direction, and minor content is retained as an explicit guard, with its nonvanishing proved on \(\mathcal D\).

The selected 11-row determinant is an actual minor of the original \(M\), not a new smaller surrogate rank test. Its homogeneous degree in the free root is fixed by (8), including zero leading coefficients in its affine encoding. For a binary quadratic \(q\) and a minor of prescribed degree \(d\), the fixed \((d+2)\)-square Sylvester determinant is the homogeneous resultant. Its vanishing is necessary for a common projective root, including infinity, repeated roots, specialized degree drops, or a specialized zero form. The efficient quadratic-remainder formulas in the author leaves are exact polynomial identities, checked against these full-degree Sylvester determinants in their independent reviews. They never divide by a specialized leading coefficient.

The shared exact nonvanishing test is elementary. For every nonzero guard or resultant \(p(g)\in K[g]\), take its four-conjugate norm \(P(g)\in\mathbb Q[g]\). A zero under any fifth-root embedding forces \(P(g)=0\). Write

\[
                       P(g)=A(n)+gB(n),\quad g^2=-n.
\]

For real \(n>0\), both \(A(n),B(n)\) are real, while either \(g\) is nonzero imaginary. Hence \(A(n)=B(n)=0\). The exact gcd \(\gcd(A,B)\), verified using quotient/coprimality or Bezout records, contains all possible positive parameters. The leaf certificates prove its positive-root count is zero, directly from the displayed factors or by an exact squarefree Sturm chain. Thus none of the guards or necessary resultants vanishes on \(\mathcal D\). Every exhaustive branch is contradicted. Finite-field anchors and selected numeric controls are not the evidence for this characteristic-zero claim.

The ten rank-review groups are 7; 11/15/19; 20/23/30; 32/33/38; 10/41/43; 45/55/57; 66/69/70; 80/83/84; 86/87/90; and 111/115/129. Their exact author and independent-review manifests, acceptance text, domains, representative sets, and coefficient-certificate files are bound in `DEPENDENCY_LEDGER.json`. Any group without an accepted pinned review disables the theorem, regardless of partial calculations or author conclusions.

## 6. Exact symmetries and the rebuilt 576-pair partition

Enumerate every permutation of \((1,2,3,4)\) lexicographically. Prepending zero gives a traversal \((0,t_1,t_2,t_3,t_4)\); set its successor map to the corresponding five-cycle. Starting at zero makes this a bijection between the 24 traversals and all Hamiltonian cycles. Form the ordered Cartesian square, with \(\pi\) outermost and \(\tau\) innermost. There are exactly 576 systems, and every possible induced pair occurs once.

Two operations preserve their zero sets on the full projective domain:

1. For \(a\in\{1,2,3,4\}\), let \(r_a(i)=ai\pmod5\). Then
\(H(g,\eta)_{ai,aj}=H(g,\eta^{a^2})_{ij}\). Relabeling rows and columns sends the cycles to \((r_a\pi r_a^{-1},r_a\tau r_a^{-1})\). It permutes equation rows and coefficient columns; signs do not matter for zero determinants. All fifth-root embeddings are included in each leaf, so this preserves its scope.
2. Since \(H^t=H\), set \(U'=V^t,V'=U^t\). Then \(T'=T^t\), and the new pair is \((\tau^{-1},\pi^{-1})\). The coefficient labels \(X,Y\) swap, yielding the same rank condition up to permutations. The support set is exactly transposed. Neither \(U\) nor \(V\) is inverted.

Both operations preserve coordinate zeros and singular limits. They commute, and their at most eight images form each orbit. The fusion independently reconstructs each orbit and records, for every member, an explicit multiplier and transpose flag taking its representative to that member. It checks the resulting cycle maps against the independently enumerated pair, not merely a numeric index.

`PAIR_COVERAGE.json` contains:

- all 24 actual successor maps;
- all 576 ordered pairs, with their actual \(\pi\) and \(\tau\);
- all 78 symmetry orbits (66 of size eight and 12 of size four);
- the exact 384 row-eliminant indices;
- the exact 28 residual orbits and their 192 members;
- an author/review binding and explicit exclusion source for each individual pair.

The checker compares the baseline record's actual permutations to its own list. It proves the row set and residual set are disjoint and cover all indices; proves the residual set is a union of full orbits; proves every residual representative belongs to exactly one rank group; and checks every member's explicit symmetry map. Only then does it derive group sizes. The expected group sizes are respectively

\[
384;\quad 8,24,16,24,20,24,20,16,24,16.
\]

Their sum is an output cross-check, not a substitute for a set partition. An omitted pair, overlapping orbit, wrong representative, different traversal convention, unaccepted leaf, or wrong coefficient-field scope cannot be repaired by a matching arithmetic total.

## 7. Fusion implication and the exact empty-set conclusion

The leaf gate has passed. Suppose (T) holds for some \(N\in\mathcal N_-\) and primitive \(\omega\). Sections 2–3 produce \(g=G\ne0\) with \(g^2=-N\), a primitive fifth root \(\eta\), and a two-Green representation of \(H_-(g,\eta)\), with zero edges and arbitrary masks retained. Section 4 gives a nonzero projective point of the original closed necessary system for its induced cycles \(\pi,\tau\).

Section 6 puts that particular ordered pair in exactly one reviewed exclusion class. If it belongs to the row class, Section 5.1 contradicts its off-support equations. Otherwise the explicit symmetry map carries it to one of the 28 rank representatives without changing the domain, and its accepted complete rank leaf contradicts its necessary augmented minor equations. Therefore no such point and no such (T) exists.

All parameters arising from the original family are in the exclusion domain, so no modulus remains below an effective cutoff or at a dropped leading coefficient. Hence \(\mathcal E_-=\varnothing\). The implication is one-way and needs no sufficiency theorem: complete emptiness of a necessary condition is enough to prove impossibility. The conclusion is strictly limited to the original eligible family and grammar defined in Section 1.

## 8. Provenance, controls, reproducibility, and the final gate

The elementary orthogonality, geometric-series, finite-dimensional inverse, projective specialization, determinant multidegree, field-norm, polynomial-gcd and resultant arguments are standard identities or supplied explicitly here. The odd-modulus Gauss-character identity is the identified borrowed number-theory input. Sturm's root-counting theorem is a standard computational ingredient of the leaf certificates. The mathematical case results are the sealed row/block result and ten separately reviewed rank groups. They are accepted dependencies, not claims of fresh recomputation by this fusion author. The exact inventory/coverage reconstruction and end-to-end assembly are the new fusion work. The earlier effective cutoff, properness argument and effective Nullstellensatz are not used in this no-cutoff proof. No historical missing author bytes are needed.

`audit_fusion.py` imports no author or reviewer algebra executable. It verifies the exact manifests and every inventoried payload, reconstructs the permutations and explicit symmetry transports independently, binds each review to the correct author manifest and representative set, and writes an explicit acceptance gate. `--require-complete` fails if even one leaf acceptance is missing. `--snapshot` makes inert copies of all bound dependency payloads; subsequent audits use those copies. The copies retain their original author-pending-review wording, but the separate frozen acceptance reports are authoritative for their reviewed scope.

`exact_controls.py` is a fresh rational/integer-cyclotomic implementation, importing no case code. Its controls include exact principal restrictions with zero edges, reordered selected sets, singleton and full subsets, singular and entirely zero masks; exact nonzero projective limits of perturbed inverse pairs and all off-support/rank conditions; exact Gauss and sign identities for every primitive character at seven eligible dimensions including nonsquarefree 135; the complete two matrix identities at dimensions 15 and 35; all five-coordinate target exponents; and all four-embedding dilation identities. These are supplementary finite controls, not replacements for the universal proof or exact polynomial leaf certificates. The completed controls give 132 exact principal restrictions (130 with zero edges, 130 with singular masks and 33 with an entirely zero mask), 40 formal singular-mask necessary-system checks, 424 primitive-character Gauss checks, 2,900 exact matrix-identity entries, 10,600 principal-target exponent checks, 424 wrong-cubic-sign rejections, and 400 embedding/dilation identities. The fusion-specific boundary controls reject twelve altered bindings, coverage records or dependency bytes, and recheck all 384 recorded row candidate polynomials on the open positive half-line. The inventory checks 1,444 payload occurrences in 23 bound packages.

The final freeze contains a PASS leaf gate, full 576-pair accepted coverage, exact-controls PASS, bound input snapshots, this proof, and a manifest covering their bytes. The author submits it to a fresh independent whole-fusion reviewer. That reviewer must separately assess the composition and scope. An accepted collection of leaves alone is not described as an accepted end-to-end theorem.

No GitHub, research table, Library, native document, or other external state is changed by this package.
