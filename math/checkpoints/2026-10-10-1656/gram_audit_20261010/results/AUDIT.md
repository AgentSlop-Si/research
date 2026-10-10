# Connected Gram and Fourier realification audit

Date: 10 October 2026

## Verdict

The manuscript's weighted connected-Gram lemma, cyclic Fourier exclusion, sharp finite-abelian Frobenius formula, and stated spectral corollary are mathematically valid under their explicit assumptions. No mathematical correction to those formulas is needed.

The novelty assessment needs stronger qualification. The realification formula is an elementary reformulation of a classical finite-abelian Fourier operator-norm result after passing to the quotient by 2-torsion. This is substantive theorem-level overlap, not merely shared proof ingredients. The precise presentation as a realification identity may be useful, but this audit does not establish its first publication. The particular one-mask architecture application may be project-specific; its global originality remains unverified.

Neither result is a new FFT algorithm, a sub-\(N\log N\) upper bound, or a lower bound for unrestricted Fourier computation.

## Sources and audit boundary

Reviewed in full: the supplied 14,014-byte manuscript, which is byte-identical to THEOREM.md inside the supplied ZIP. Also reviewed the ZIP's README, SOURCE_AUDIT, NEXT_GATE and full member inventory. Computed SHA-256 hashes for the two supplied files and every non-directory ZIP member.

No program from the research ZIP was executed or imported. All numerical checks below were written afresh from the mathematical statements, using direct character matrices. The package's claims about earlier project checkpoints are provenance assertions in that package, not a claim that this audit independently reverified those other archives.

The attached manuscript and frozen source archive are the mathematical evidence. Original source archive identity: see SOURCE_ARCHIVE_LEDGER.json at the export root.

Source hashes:
- FFT_GRAM_LOCK_SHARP_REALIFICATION_2026-10-10.zip: b7ee0f1fa3c4b95f2278ca901268435aa079718d3f10fab6b506beefec8719d9
- THEOREM(20261010-154244).md: 71536613bd090ffa087e5f95ea8f800839520ff7d3507b65c2c5c30de0dc9c58

## Accepted weighted Gram theorem

Let \(A,B\in GL_N(\mathbb R)\), let \(L,R,D\) be invertible complex diagonal matrices, and suppose
\[
M=LADB R,\qquad M^*M=I.
\]
Define
\[
K=A^T\operatorname{diag}(|L_{11}|^2,\ldots,|L_{NN}|^2)A.
\]
For the undirected graph with edges \(ij\) wherever \(i\ne j\) and \(K_{ij}\ne0\), the phase of \(d_i\) is constant modulo \(\pi\) on every connected component. Thus, when this graph is connected, \(D=e^{i\theta}D_0\) with \(D_0\) real diagonal and invertible, and \(M\) is diagonally equivalent to a real matrix.

Proof. Expanding unitarity and using invertibility gives
\[
D^*KD=B^{-T}\operatorname{diag}(|R_{jj}|^{-2})B^{-1}\in\mathbb R^{N\times N}.
\]
At an edge, reality of \(\overline d_iK_{ij}d_j\) forces \(d_j/d_i\in\mathbb R^\times\). Propagation along a graph path proves the assertion. In fact, for a fixed real \(K\), this phase condition is also sufficient for \(D^*KD\) to be real; it is not by itself sufficient for the original product to be unitary.

The dual argument uses \(MM^*=I\) and
\[
T=B\operatorname{diag}(|R_{jj}|^2)B^T
\]
to obtain the same phase conclusion whenever the support graph of \(T\) is connected.

If \(A\) is entrywise strictly positive, every entry of \(K\) is positive. If \(B\) is entrywise strictly positive, every entry of \(T\) is positive. Therefore either positive stage suffices. This is entrywise positivity, not positive definiteness.

Outer invertible monomial factors cause no difficulty. Write \(L=P_L\Lambda_L\), \(R=\Lambda_RP_R\), remove the unitary permutations \(P_L,P_R\), and apply the diagonal statement.

### Essential limits of the statement

- The graph is the weighted Gram graph for the actual outer amplitudes. Without positivity, its connectivity may depend on those weights.
- Connectivity locks phases modulo \(\pi\), not modulo \(2\pi\). Signs of the real diagonal remain free.
- The result classifies the exact-unitary members of this architecture; it does not say that there are no such members.
- For every \(N\), \(A=I+J>0\), \(B=I-J/(N+1)\), \(D=L=R=I\) gives \(M=I\), where \(J\) is the all-ones matrix.
- Dropping connectedness invalidates the Fourier exclusion. The real and imaginary parts of the symmetric unitary Fourier matrix are commuting real symmetric matrices, so there is a real orthogonal \(Q\) and complex diagonal \(\Lambda\) with \(U_N=Q\Lambda Q^T\). Its unweighted Gram matrices are identities and their graphs are disconnected.
- The elementary example \(A=B=I\), \(D=\operatorname{diag}(1,i,1)\) already shows that a disconnected Gram graph does not force all middle phases to align.

## Accepted exact Fourier exclusion

For the normalized cyclic Fourier matrix \(U_N\), \(N\ge3\), there is no factorization
\[
U_N=LADB R
\]
with \(A,B\) real and invertible, at least one entrywise strictly positive, \(D\) invertible complex diagonal, and \(L,R\) arbitrary invertible complex monomial matrices.

Proof. Exact equality makes the product unitary. The Gram theorem makes it monomially equivalent to a real matrix. Every nonzero-entry real matrix has real \(2\times2\) cross-ratios, and row or column scaling cancels from each ratio. Permutations only relabel the collection. But the Fourier rows \(0,1\) and columns \(0,1\) have cross-ratio \(e^{-2\pi i/N}\), which is nonreal for \(N\ge3\). Contradiction.

The manuscript's displayed \(N=2\) factorization checks exactly: before its outer gauges, \(ADB=\left(\begin{smallmatrix}2&2/3\\1&-1/3\end{smallmatrix}\right)\), and the stated \(L,R\) yield \(U_2\). Thus the cyclic length restriction is genuine.

For general finite abelian \(G\), the analogous exclusion holds precisely for Fourier tables that are not monomially real-equivalent, namely those with exponent greater than two. It must not be restated as a no-go for every finite-abelian Fourier table of order at least three: Walsh-Hadamard tables of elementary abelian 2-groups are real.

Positive Green sums fall within this result only when their aggregate stages satisfy the stated real positivity and invertibility assumptions. Invertibility of summands alone does not imply invertibility of their sum. The theorem does not cover genuinely complex aggregate stages that cannot be put into the required real-stage form, or architectures with two or more independent internal masks.

## Independent derivation of the sharp formula

For a complex \(r\times s\) matrix \(Z\), write \(Z\circ Z\) for its entrywise square, and use the complex induced norm
\[
\|C\|_{\infty\to1}=\max_{\|b\|_\infty\le1}\|Cb\|_1.
\]
There is an elementary general identity
\[
\min_{\substack{|u_i|=|v_j|=1\\X\text{ real}}}
\|\operatorname{diag}(u)Z\operatorname{diag}(v)-X\|_F^2
=\frac{\|Z\|_F^2-\|Z\circ Z\|_{\infty\to1}}2. \tag{A}
\]

For fixed phases the minimizing \(X\) is the entrywise real part. The identity
\((\operatorname{Im}z)^2=(|z|^2-\operatorname{Re}z^2)/2\)
then reduces the minimization to maximizing
\(\operatorname{Re}(a^T(Z\circ Z)b)\), where \(a_i=u_i^2,b_j=v_j^2\).
Squaring maps the unit circle onto itself. Maximizing over \(a\) gives
\(\|(Z\circ Z)b\|_1\). A maximum over the product of closed unit discs can be attained on the product of their boundary circles: any interior coordinate can be expressed as a convex combination of boundary points, and convexity of the objective permits a boundary replacement without lowering the maximum. This proves (A).

Now let \(G\) be finite abelian, \(N=|G|\), \(T=G[2]=\{x:2x=0\}\), \(g=|T|\), and \(U_G\) its normalized character matrix. Set
\[
W_{\chi,x}=\chi(x)^2,\qquad U_G\circ U_G=W/N.
\]
Conjugating all characters, if desired for the Fourier sign convention, changes none of the conclusions.

### Direct lower bound

Character orthogonality gives
\[
(WW^*)_{\chi,\psi}
=\begin{cases}N,&\chi^2=\psi^2,\\0,&\text{otherwise}.\end{cases}
\]
The squaring map on the dual group has kernel of order \(g\). Hence \(WW^*\) consists, after permutation, of \(N/g\) blocks \(NJ_g\), and
\(\|W\|_2=\sqrt{Ng}\).
For unimodular \(a,b\),
\[
|a^TWb|\le\|a\|_2\,\|W\|_2\,\|b\|_2=N\sqrt{Ng}.
\]
Using (A), or the preceding scalar expansion, gives the lower bound
\[
\frac{N-\sqrt{Ng}}2.
\]

### Explicit equality witness

For a cyclic factor of order \(n\), put \(g_n=\gcd(2,n)\), \(m=n/g_n\), and
\[
c_k=\exp\!\left(\frac{\pi i}{m}k(k+\delta)\right),\quad
\delta=\begin{cases}0&m\text{ even},\\1&m\text{ odd}.\end{cases}
\]
The sequence is periodic modulo \(m\), since the ratio under \(k\mapsto k+m\) is
\(\exp(\pi i(2k+m+\delta))=1\).
For \(t\not\equiv0\pmod m\), its cyclic autocorrelation is a unit phase times
\(\sum_{k=0}^{m-1}e^{2\pi i kt/m}=0\).
Thus its unnormalized Fourier transform has constant modulus \(\sqrt m\).

Lift \(c\) to length \(n\) by \(b_k=c_{k\bmod m}\). The relevant squared-character matrix evaluates the quotient Fourier transform at frequencies \((2/g_n)j\) modulo \(m\); this is a permutation because \(2/g_n\) is coprime to \(m\). Therefore every entry of \(W_nb\) has modulus \(g_n\sqrt m=\sqrt{ng_n}\). For a product of cyclic groups, tensor these lifted witnesses. Then \(|Wb|=\sqrt{Ng}\) entrywise. Setting
\(a_\chi=\overline{(Wb)_\chi}/|(Wb)_\chi|\)
and taking arbitrary unit-modulus square roots of \(a,b\) attains the lower bound.

Consequently, including the trivial group,
\[
\boxed{\min_{|u_\chi|=|v_x|=1,\ X\text{ real}}
\|\operatorname{diag}(u)U_G\operatorname{diag}(v)-X\|_F^2
=\frac{N-\sqrt{N|G[2]|}}2.}
\]

The zero case occurs exactly when \(g=N\), equivalently \(G\) has exponent at most two. For \(G=\mathbb Z_N\), \(g=\gcd(2,N)\).

### Exact reduction to an established norm theorem

Squared characters annihilate \(T\). The distinct rows of \(W\) are all characters of \(H=G/T\), and each appears \(g\) times. Columns likewise repeat \(g\) times. Thus, up to row and column permutations,
\[
W=F_H^{\rm unnormalized}\otimes J_g.
\]
For any \(C\),
\(\|C\otimes J_g\|_{\infty\to1}=g^2\|C\|_{\infty\to1}\):
sum the \(g\) input coordinates in each block for the upper bound, and repeat an extremizing input for equality.

Putting \(m=|H|=N/g\), the existing finite-abelian result
\(\|U_H\|_{\infty\to1}=m\) gives
\[
\|W\|_{\infty\to1}
=g^2m^{3/2}=N\sqrt{Ng}.
\]
Together with (A), this is exactly the claimed formula. The identification and reduction above are this audit's own algebraic comparison; the cited norm theorem is [1], Theorem 2.1.

## Accepted spectral corollary and its scope

Let \(\mathcal C\) be the set of all matrices monomially equivalent to real matrices; their real representatives need not be orthogonal or invertible. For every \(Y\in\mathcal C\),
\[
\|Y-U_G\|_2\ge
\sqrt{\frac{1-\sqrt{g/N}}2}. \tag{B}
\]
Indeed, strip unitary outer phases and permutations from \(Y\). Remaining positive amplitudes can be absorbed into a real representative. Let \(E\) be the transformed error and \(H\) the transformed Fourier table. Then
\[
\|E\|_2\ge\|\operatorname{Im}E\|_2
=\|\operatorname{Im}H\|_2
\ge\|\operatorname{Im}H\|_F/\sqrt N,
\]
where the first inequality follows from
\(\operatorname{Im}E=(E-\overline E)/(2i)\).
The exact Frobenius formula proves (B).

This base bound does not require \(Y\) to be unitary. The extra exact-unitarity assumption is required when inferring membership in \(\mathcal C\) from the connected-Gram Green architecture. An arbitrary approximate or approximately unitary \(LADB R\) is not phase-locked by this argument. The audit neither proves nor disproves a stronger bound for all such approximants.

The Frobenius minimum permits arbitrary real \(X\); it is not the minimum over real orthogonal matrices. The spectral constant in (B) is a valid lower bound, not an established sharp spectral distance.

## Statement level prior art comparison

### Fourier norm and equality witnesses

[1] Gilbert and Rzeszotnik, 2010, Theorem 2.1 gives every finite-abelian normalized Fourier \(L^p\)-to-\(L^q\) norm; its \(p=\infty,q=1\) case is \(m\). Their Theorem 4.5 supplies quadratic cyclic witnesses, Lemma 4.6 supplies tensor products, and Theorem 4.7 supplies existence on every finite abelian group. The quotient calculation above turns this prior result into the manuscript's identity. This is the strongest overlap located.

[2] Führ and Rzeszotnik, 2015, Theorem 4.1 equates the existence of a biunimodular vector for an \(m\times m\) unitary matrix with saturation of its \(\infty\)-to-\(1\) norm at \(m\). It also gives equivalent unitary diagonal-scaling descriptions. It directly contextualizes the equality mechanism, but does not state a positive-stage Green exclusion or the realification objective.

[3] Chu, 1972, constructs unimodular sequences with zero cyclic autocorrelation at every nonzero shift for arbitrary length. The chirps and flat spectra used by the manuscript are classical; their existence is not a new result. The all-length theorem is explicit in the original publisher abstract.

### Gram phase gauges and cross ratios

[4] Chien and Waldron, arXiv 2013 version, define the frame graph by nonzero Gram entries and characterize projective unitary equivalence through cyclic products. Their Theorem 3.2 uses spanning trees within connected components to organize phase gauges. The manuscript's propagation of phases over connected Gram support is an elementary special-case mechanism from the same established framework. This is close conceptual overlap; their statement does not itself assert the specific weighted \(LADB R\) architecture theorem.

[5] Östergård and Valtonen, 2026, Theorem 1 treats uniqueness of dephasing, and Section 2.3 uses Haagerup's four-entry invariant. For unimodular matrices that invariant is the corresponding cross-ratio. Thus the Fourier-versus-real cross-ratio obstruction and anchored dephasing step are standard gauge tools. The article does not supply the manuscript's positive-stage architecture statement.

### Defensible novelty language

The checked package combines valid classical gauge and Fourier-norm tools into a restricted architecture exclusion. The sharp realification identity is a corollary of existing norm theory after an elementary quotient reduction. The particular application or exposition may still be valuable, but independent publication-level originality for the architecture statement and priority for the realification wording remain open.

Suggested description:

“We establish a weighted-Gram obstruction for exact Fourier realization by two real invertible stages separated by one complex diagonal mask, when either stage is entrywise strictly positive, allowing arbitrary outer monomial gauges. We derive the finite-abelian Fourier realification identity from classical biunimodular Fourier norm theory and give explicit Chu witnesses. These results constrain this architecture and do not establish an unrestricted Fourier operation-count bound.”

## Independent checks

The new program evaluated 52 finite-abelian presentations:
- Every cyclic length from 1 through 32.
- Twenty additional products, including \(\mathbb Z_4^3\), \(\mathbb Z_2\times\mathbb Z_4\times\mathbb Z_8\), \(\mathbb Z_3^3\), and elementary abelian 2-groups.
- Maximum order 64.
- Maximum absolute error in the achieved Frobenius formula: \(7.11\times10^{-15}\).
- Maximum chirp flatness error: \(1.07\times10^{-13}\).
- Maximum squared-character Gram identity error: \(2.82\times10^{-13}\).
- All predicted ranks \(N/g\) and operator norms \(\sqrt{Ng}\) agreed numerically.
- Forty random rephasings per presentation did not fall below the formula beyond rounding.
- Independent BFGS runs with six random starts on each of eight small groups reached the formula to \(1.34\times10^{-15}\) or better.
- The \(N=2\) positive-stage factorization and the identity and disconnected-Fourier scope examples were checked.
- A symbolic three-vertex path Gram example checked real sign freedom and failure of a noncollinear phase assignment.

These are reproducible finite checks supporting the exact arguments; they do not replace them. No source-program result was treated as independent evidence.

## Primary references

[1] John Gilbert and Ziemowit Rzeszotnik. The norm of the Fourier transform on finite abelian groups. Annales de l'Institut Fourier 60(4), 1317–1346 (2010). Theorem 2.1, Theorem 4.5, Lemma 4.6, Theorem 4.7.
https://aif.centre-mersenne.org/item/AIF_2010__60_4_1317_0/
https://aif.centre-mersenne.org/item/10.5802/aif.2556.pdf

[2] Hartmut Führ and Ziemowit Rzeszotnik. On biunimodular vectors for unitary matrices. Linear Algebra and its Applications 484 (2015), 86–129. Theorem 4.1.
https://arxiv.org/abs/1506.06738
https://arxiv.org/pdf/1506.06738

[3] David C. Chu. Polyphase codes with good periodic correlation properties. IEEE Transactions on Information Theory 18(4), 531–532 (1972). DOI 10.1109/TIT.1972.1054840.
https://ieeexplore.ieee.org/document/1054840/

[4] Tuan Chien and Shayne Waldron. A characterisation of projective unitary equivalence of finite frames. arXiv:1312.5393. Theorem 3.2 and its connected-component spanning-tree argument; theorem numbering here refers to the inspected arXiv text.
https://arxiv.org/pdf/1312.5393
https://www.math.auckland.ac.nz/~waldron/Preprints/Tripleprods/tripleprods.html

[5] Patric R. J. Östergård and Tuomo Valtonen. Equivalence of complex Hadamard matrices. Journal of Algebraic Combinatorics 64, article 20 (2026). Published 28 July 2026. Theorem 1 and Section 2.3.
https://link.springer.com/article/10.1007/s10801-026-01568-x

