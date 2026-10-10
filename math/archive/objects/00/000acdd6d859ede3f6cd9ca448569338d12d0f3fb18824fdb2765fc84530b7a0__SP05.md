# Phase41 supplement: unit-circle rigidity and exact local rank

Date: 2026-10-10. This is a separate supplement to the frozen Q26/Q27 manuscript. Source: Library `[private-id]`, version3, ZIP SHA256 `947ef3cda041d1e167e8013aadd527f9d8a51496d9c3ac90a0391f3580148f3c`, 5,913,220 bytes. The uploaded programs were inspected as inert text; none was executed, imported, compiled, or AST-parsed. Only the independently authored local audit programs were run.

## Dispositions

- The all-size **N>8 two-unit-cycle exclusion** has a complete independently reconstructed proof below. It permits arbitrary complex scalar coefficients and arbitrary external invertible monomial factors. It remains valid with independent **unitary** monomial decorations on each summand.
- The phase-only real-rank bound is correct and in fact holds for **any fixed complex scalar coefficients**, not only a=b=1. Making their relative scalar variable changes the dimension count; it does not change the N>8 exclusion.
- All **16 saved phase-only determinant residues** are rebuilt exactly: two-cycle four-ratio rank6 and three-cycle complete two-row rank2(N−1), N=8,16,32,64, both primes. Smaller two-cycle windows k=2,3 attain ranks4,5 in fresh checks at all four sizes, including N64 where the source did not separately save them.
- All **10 two-cycle complex-amplitude full-signature ranks** are rebuilt at N=8,16,32,64,128, both primes, now with explicit fresh maximal minors. This is a different admissible family.
- Six saved numerical partial fits and two retained high-precision parameter sets were independently evaluated. Their first two rows fit accurately and their third rows do not. These are numerical diagnostics, not exact root certificates or Fourier algorithms.
- Publication priority of the specific eight-value obstruction is **unresolved**. The proof is accepted only after the external review receipt, separately from priority.

## 1. Frozen model and path-ratio lemma

Let N≥2 and let W be the successor matrix of a directed Hamiltonian cycle, with weight w_e on each directed edge. Assume every |w_e|=1. Then W is unitary, its cycle product H=∏w_e has modulus1, and W^N=HI. The Green inverse exists exactly when H≠1, and

G=(I−W)^−1=(I+W+⋯+W^(N−1))/(1−H).

For each ordered input/output pair, exactly one of these N powers supplies a nonzero entry, a directed path product. Thus every G entry is nonzero and has modulus g=1/|1−H|. No conditioning bound is needed.

For any distinct rows u,v, let P be the nonempty directed path from v to u and Q its complementary path from u to v, so PQ=H. According to which of u,v is reached first when starting at input j, cancellation of the common path gives

G_(u,j)/G_(v,j) ∈ {P, Q^−1}.

This includes j=u and j=v using the empty path of weight1. Both values lie on the unit circle. At most two ratio values occur, for every row pair and every cycle ordering.

Independent row/column permutations and unit-modulus row/column diagonal multipliers preserve this property: a row multiplier changes both values by one unit phase, column multipliers cancel, and permutations only select another row pair or reorder columns. They also preserve the constant entry modulus of each summand.

## 2. Abstract flat-summand theorem and the all-size exclusion

### Theorem P41-A: bounded ratio signatures

Let X,Y be N-square matrices with every X entry of modulus g_X>0 and every Y entry of modulus g_Y>0. Suppose for each row pair the ratios in X take at most q_X values and those in Y at most q_Y values. Let M=aX+bY for arbitrary a,b∈C. If M is equivalent to the unnormalized F_N under arbitrary invertible complex row/column diagonal matrices and row/column permutations, then

N ≤ 2q_X q_Y.

**Proof.** If a=b=0 the proposed Fourier equivalence is impossible. Otherwise choose the two rows of M that correspond, after the outer row permutation, to adjacent frequency rows of F_N. Fourier equivalence makes every entry of M nonzero. For this pair u,v, column scalings cancel in M_(u,j)/M_(v,j), and row scalings contribute one fixed nonzero factor. Therefore all these ratios have one common modulus K>0 and take exactly N distinct values, even after the column permutation.

Partition columns according to their pair of summand ratio values (r_1,r_2), giving at most q_X q_Y classes. Flatness implies |r_1|=|r_2|=1. Write X_(v,j)=g_X s_j, Y_(v,j)=g_Y t_j with |s_j|=|t_j|=1. Within one class put A=ag_X, B=bg_Y and z_j=t_j/s_j∈S^1. Then

M_(u,j)/M_(v,j) = phi(z_j) = (A r_1+B r_2 z_j)/(A+B z_j).

The denominator is nonzero at each column because M_(v,j)≠0. If A=0, B=0 or r_1=r_2, phi is constant on its domain. Otherwise A,B≠0 and r_1≠r_2. The condition |phi(z)|=K is

c+2 Re(dz)=0,
c=(1−K²)(|A|²+|B|²),
d=conj(A) B(conj(r_1)r_2−K²).

This real equation cannot vanish identically on S^1: c=0 would force K=1, and d=0 would then force r_1=r_2. A nontrivial real affine equation cuts the circle in at most two points. If d=0 and c≠0 there are no points; otherwise rotate d to a nonnegative real number and fix one coordinate of the circle. Hence at most two ratio values occur in each signature class. There are at most 2q_Xq_Y values overall, contradicting N larger than that bound. ∎

### Corollary P41-B: two unit-gain Green cycles, with unitary decorations

For every integer N>8, let G_1,G_2 be any two admissible Hamiltonian-cycle Green inverses with unit-modulus edge gains. For s=1,2 let U_s,V_s be arbitrary unitary monomial matrices, independently chosen. Then

F_N ≠ L P [a U_1 G_1 V_1+b U_2 G_2 V_2] Q R

for arbitrary a,b∈C, invertible complex diagonal L,R, and permutations P,Q.

**Proof.** Apply the path-ratio lemma to X=U_1G_1V_1 and Y=U_2G_2V_2, giving q_X=q_Y=2, then Theorem P41-A. ∎

With U_s=V_s=I this is the source's exact all-N statement. The branchwise-unitary decoration extension is an elementary new corollary of the same proof; it is not asserted to be independently novel literature. **Nonunitary branch decorations, nonunit edge amplitudes, three summands and products of sums are outside this theorem.** An arbitrary external monomial factor is allowed; inserting one between factors in a product changes the architecture.

A zero matrix entry cannot evade the argument: it immediately prevents external monomial equivalence to the dense Fourier matrix. Singular Green denominators are excluded at the definition stage, rather than treated as usable limits.

## 3. Phase-only local dimension bound

### Theorem P41-C: any fixed coefficients

Fix a,b∈C, two Hamiltonian cycle orders, and k+1 distinct columns including the two selected row indices, labelled rows0,1 and columns0,...,k, where 2≤k≤N−1. On the open domain where both Green inverses and all selected matrix entries exist and are nonzero, put M=aG_1+bG_2 and

R_j=M_(0,j) M_(1,0)/(M_(1,j) M_(0,0)), 1≤j≤k.

As unit-modulus edge gains vary, the real differential rank of R is at most min(2k,k+2).

**Proof.** Each unit-weighted cycle can be written W_s=V_s W_s^can(H_s)V_s^−1, with V_s unitary diagonal, all but one canonical edge weight equal to1, and last weight H_s. Consequently G_s=V_s K_s(H_s)V_s^−1. One common diagonal conjugation reduces M to aK_1(H_1)+bD K_2(H_2)D^−1, D=V_1^−1V_2. All anchored ratios are unchanged by this conjugation. Normalize the irrelevant scalar of D so d_1=1. The entries used by R depend only on H_1,H_2,d_0,d_2,...,d_k: exactly k+2 real circle variables. Therefore the differential has rank at most k+2 and at most the output dimension2k. ∎

The chosen selected columns containing both row labels is important to this exact count. For a general window, count the union of selected row and column vertices explicitly. The source uses the stated 0/1 and 0,...,k window, so its bound applies. Allowing the relative complex scalar coefficient to vary adds at most two real variables, giving only the corresponding relaxed upper bound. The N>8 theorem already allows arbitrary a,b.

## 4. Exact real-Jacobian reduction and all rebuilt finite witnesses

The phase-only examples have canonical tree-edge gains1 and chord gains

h_e=(a_e+i b_e)/(a_e−i b_e)∈Q(i), |h_e|=1.

The graph orders and integer pairs (a_e,b_e) are saved explicitly in the source and reproduced in `FRESH_JACOBIAN_RESULTS.json`. The chord phase derivative is ∂h_e/∂theta_e=i h_e. For edge e:u→v in cycle s,

∂G_s/∂theta_e=i h_e G_s E_(v,u)G_s,

so the logarithmic output derivative is the signed sum of four corresponding entry derivatives divided by M_(r,c). All divided entries are nonzero by the tested guards. Multiplication of the jth complex derivative row by the nonzero R_j converts it to the ordinary derivative; on real and imaginary parts this is an invertible 2-by-2 real block. Therefore ordinary and logarithmic real Jacobians have the same rank.

To compute the real Jacobian exactly, reduce Q(i) using both i↦+iota and i↦−iota at each split prime p. The second reduction includes conjugating the factor i h_e, so it gives the conjugate derivative, not an unrelated numerical sample. Taking (z+conj(z))/2 and (z−conj(z))/(2i) produces the exact rational real/imaginary entries modulo p. All gain denominators, both conjugate sets of Green determinants, and selected matrix entries are checked nonzero. A nonzero minor of this rational Jacobian modulo p proves that its characteristic-zero rational determinant is nonzero. No finite-field absolute-value claim is made.

Fresh construction uses direct sparse inversion of I−W, independently computed derivatives, and independent modular elimination. It matches **every one of the 16 saved determinant residues**:

- Two phase cycles, k=4: rank6 at N=8,16,32,64, each in both primes. The k=2 and k=3 subwindows additionally have exact ranks4 and5 at every one of those sizes. Together with Theorem P41-C this proves the exact characteristic-zero ranks.
- Three phase cycles: complete N−1 complex ratios, full real rank2(N−1) at N=8,16,32,64, each in both primes. All listed full-row-rank minors match the source exactly. The real submersion theorem gives a Euclidean-open image near each certified point. It does not identify that image with the Fourier target.
- Two complex-amplitude cycles: rankN−1 at N=8,16,32,64,128, each in both primes. These ten computations reconstruct the same underlying integer-weight problems (the source's conditional modular weight adjustment is never triggered), all guards, and full complex logarithmic Jacobians. Fresh nonzero maximal minors are now recorded. They prove dominance over C at these fixed graph orders, not surjectivity or target membership.

There are 26 prime/family/size records in total. In all records the complete middle sum is invertible and entrywise nonzero in the tested reduction; phase examples also pass the conjugate embedding guards. The latter properties give a compatible open chart for the earlier Hadamard–Segre target-fiber test. They do not solve that fiber. These are explicit finite witness checks, not samples of all graph orderings or all sizes.

### Supporting lemma: invertibility for positive scalar sums is automatic

For any unitary W with I−W invertible, G=(I−W)^−1 satisfies G+G*=I. Indeed I−W*=−W*(I−W), so G*=−G W=I−G. If M=∑c_s G_s with real c_s>0, then M+M*=(∑c_s)I. For every vector v,

||Mv||·||v|| ≥ Re(v*Mv)=(∑c_s)||v||²/2.

Hence sigma_min(M)≥(∑c_s)/2 and ||M^−1||≤2/(∑c_s). For the equal-weight two/three-cycle phase sums, invertibility thus holds throughout their admissible complex phase domains, not just at the saved points. Individual Green norms and the condition number of M may still be large. This is a standard Cayley-transform identity, not a new conditioning theorem for arbitrary complex coefficients. It also does not survive arbitrary independently decorated summands without its stated unitary-resolvent form.

## 5. Numerical partial fits independently re-evaluated

`fresh_partial_fit_checks.py` loads only saved parameter JSON, constructs the cycle matrices anew, and evaluates the displayed matrices. No source optimizer or Newton solver was run. At N=8,16,32:

- Three phase cycles: first-two-row max errors approximately 1.26e−11, 1.75e−12, 2.09e−12; third-row errors approximately195.89, 2.31, 3.22.
- Two arbitrary-amplitude cycles: first-two-row max errors approximately2.83e−12, 6.32e−12, 9.20e−12; third-row errors approximately3.19, 2.97, 3.99. The N32 middle condition number is about8.48e5.

The retained high-precision decimal amplitudes were re-evaluated using110 working digits. The N8 and N16 two-row ratio residuals are about2.06e−93 and4.92e−84, respectively, while their third-row errors remain about3.19 and2.97. These findings confirm the source's narrow numerical story. They do not supply validated error intervals, exact algebraic parameters or a rigorous target-root existence theorem.

The amplitude escape template is a correct exact local identity: for |z|=1 put t=(2−z)/(z−1/2). Then |t|=2, its denominator and1+t are nonzero, and (2+t/2)/(1+t)=z. It illustrates why unit-modulus assumptions matter but does not place the parameters in a globally consistent Green network.

## 6. Interaction with Q26/Q27 and remaining work

The current supplement leaves the Q26/Q27 proof freeze unchanged. It narrows one separate synthesis branch: at N>8 **two unit-phase Green summands**, even with branchwise unitary monomial decorations, cannot give the full Fourier transform after arbitrary external monomial changes. Searching more phase parameters within that same architecture cannot overcome the theorem. The arbitrary-amplitude two-cycle chart remains distinct and is not ruled out by this result. Three-cycle phase local freedom does not imply multi-row coherence.

A complete candidate must satisfy the entire guarded rank-one target-fiber system, or both Weyl identities with the correct scalar normalization, in the identical architecture and field. A singular commutator, local rank or small floating residual is not acceptance. The O(N) supplied-parameter recurrence excludes parameter finding, precision, coefficient representation, preprocessing and data movement; those costs remain charged. No faster Fourier or integer-multiplication result is established.

## 7. Priority boundary and primary comparison

The earlier directly inspected Engel–Schneider [1982 final paper](https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs066.pdf), Theorem3.8, Corollaries3.9–3.11 and §4.4, supplies the classical diagonal/gauge-equivalence mechanism used in the background. It does not itself provide the specific eight-value flat-summand bound proved here.

On2026-10-10 the two Hadamard catalogue URLs listed in Phase41's source prior-art note failed to load through the available route. Three targeted searches combining weighted cycles, resolvents, Hadamard matrices and row ratios did not produce a matched primary theorem for this exact family. Unrelated Green/PDE results and unmatched Hadamard classifications were not treated as comparators. This is an incomplete bounded search, not a global priority certificate. The precise eight-value theorem and fixed-size Jacobian applications remain **priority unclosed**; background circle geometry, Green path sums, gain switching, inverse differentiation and local submersion/dominance principles are classical.
