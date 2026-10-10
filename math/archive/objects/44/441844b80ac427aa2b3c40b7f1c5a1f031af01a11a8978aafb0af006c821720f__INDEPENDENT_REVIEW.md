# Independent review of nonlinear routing Fourier rank gates

## Result and scope

Accepted. The exact arbitrary-output rank oracle, moving-partition bound and low-rank permutation-edit bound are valid with the stated hypotheses. Independent controls reproduce the modified N256 obstruction: Fourier rank 128 exceeds scan capacity and exact network min-cut 124. They also reproduce the two-Toffoli perturbation bounds 1024>902 at N2048 and 2048>1911 at N4096.

These are necessary coefficient-independent obstructions for the specified quasiseparable stage grammar. The original, unmodified N256 affine layout remains feasible under the tested rank inequalities, with no Fourier coefficient construction established. The separately accepted N16 eight-order Green construction is outside this four-common-order-rank-one model. There is no contradiction with that seed, no arbitrary nonlinear-routing exclusion, and no arithmetic speedup or general FFT lower bound.

Source SHA256: 8e8ef7663a3740db1eb5d4b435b5ef4fd910be8b361aadee3322dab52f807a1a. The nested predecessor is byte-identical to the previously reviewed parity-affine archive, SHA256 187469b7ae06bb3758da7c5642c889cf44ed3ba32e7deb0249052da7b7db1c06. SOURCE_PROVENANCE.json records the authenticated source ledger and CRC check. Uploaded scripts were read as inert text; none was executed or imported. The supplied proofs and constructions retain their source attribution, with no publication-priority claim.

## Exact Fourier rank oracle

Let h divide N, d=N/h, and E be m distinct residues modulo h. Assume every m-row restriction of F_h[:,E] is nonsingular over C. Define C={e+h j: e in E, 0<=j<d}. For arbitrary distinct output indices R, write n_rho=|{r in R: r=rho mod d}|. Then

    rank F_N[R,C] = sum_(rho=0)^(d-1) min(n_rho,m).

To prove this, write r=rho+d ell and c=e+h j. The Fourier entry factors as

    zeta_N^(rho e) zeta_h^(ell e) zeta_d^(rho j).

An invertible d-point Fourier change among the j-columns for each e separates the rho row classes. The rho block is a row restriction of F_h[:,E] times nonzero column scalings. Its rank is min(n_rho,m): if fewer than m rows are present, extend them to m independent rows; if at least m are present, select any m. The sum formula follows. No Gaussian elimination or approximation of roots is needed once the full-spark premise is certified.

For h a power of two and E selecting exactly one member of each pair {s,s+h/2}, counts modulo every lower power of two are equal; at h they are zero or one. The prime-power balanced-residue characterization makes E universal, and Fourier symmetry converts this to the required column full-spark property. This step is imported, with attribution to [Osgood, Siripuram and Wu, Theorem 4](https://arxiv.org/html/1204.0992v1#S4.SS2). It is not a new theorem of the supplied archive.

For a nonzero binary parity mask a, put h=2^(msb(a)+1). Its within-period parity halfset is precisely such a transversal. This gives the oracle for any output set, including nonlinear images of parity sets. For |R|=N/2, each n_rho<=h and min(n_rho,h/2)>=n_rho/2, yielding rank>=N/4. When a has the top bit, h=N and d=1, so every output halfset gives full rank N/2.

The oracle costs O(|R|+d) integer accounting, with O(d) storage. This is a rank diagnostic, not an algorithm applying the Fourier matrix. It applies only with the stated periodic/full-spark columns; arbitrary input sets cannot be inserted into the formula without verifying that premise.

## Moving sets and arbitrary nonlinear shuffles

Let S_j be a matrix whose strict lower and upper cut blocks have rank at most r_j in the stated linear order. For a set A, its indicator has d(A) adjacent changes. Each consecutive run of input indices in A contributes a rectangle reaching rows to its left and one reaching rows to its right, omitting missing endpoint boundaries. Each rectangle is a restriction of one strict upper or lower cut block, of rank at most r_j. These rectangles cover S_j[A^c,A]. Therefore

    rank S_j[A^c,A] <= r_j d(A).

This argument includes singular stages and zero generators and does not need a generic chart.

The routing convention is x_next[j]=y_previous[P_j[j]], so A_(j+1)={j:P_j[j] in A_j}. Insert coordinate projections between all factors and telescope the input-to-complement crossing. Interstage permutations transport the partitions exactly and create no crossing rank. Consequently

    rank (S_t P_(t-1) ... P_1 S_1)[A_t^c,A_1]
       <= sum_j r_j d(A_j).

No affinity is needed for this inequality. The exact oracle supplies the Fourier target rank for A_1 a parity halfset even when A_t is nonaffine. A strict rank excess excludes every coefficient choice in this grammar. Rank survival alone proves neither coefficient compatibility nor attainable structural rank.

## The modified N256 certificate

The three GF(2)-affine basis-column maps are recorded verbatim in the source JSON. They use zero offsets and are regenerated as permutations. Only the third map is changed, successively replacing P by P composed with each gate:

    controls (2,7), target 6;
    controls (3,6), target 2;
    controls (2,4), target 3;
    controls (3,4), target 2;
    controls (2,3), target 4.

Composition orientation matters: the new-to-old shuffle list is indexed by the gate list. The own verifier implements this convention independently. The resulting map disagrees at 160 inputs with the affine map inferred from its values at zero and the eight basis vectors, proving it is genuinely nonaffine.

For input mask 112, the original boundaries are [11,53,43,60], capacity 167. After the five gates they are [11,53,43,17], capacity 124. The intermediate fourth-stage boundaries are 31,25,23,21,17, giving the recorded gaps -10,-4,-2,0,+4 for this same input mask.

The final output complement contains 128 rows, split equally between the two residues modulo d=2. With h=128 and m=64, the oracle gives min(64,64)+min(64,64)=128. Thus 128>124 rigorously excludes the changed layout over C. The own full 128-square submatrices have rank 128 in both GF(12289) and GF(65537).

A separately authored integer augmenting-path implementation recreates the directional scan network and returns flow/min-cut 124. There are 8176 active stage vertices before adding source and sink; the own allocated array also contains harmless unused boundary slots. Unit input/output wire capacities, two directional rank-one states and the exact permutation connections match the model. This network calculation is an independent structural check, not the logical basis of the characteristic-zero Fourier rank proof.

The archive's 504 single-Toffoli search consists of three possible shuffle positions, eight targets and 21 pairs of remaining control bits. The independent search tests all 255 nonzero input parity masks for every one of these 504 altered layouts. Its results and witness masks are stored in SINGLE_EDIT_SEARCH.json. No such single edit gives a contradiction; the best gap is -10, while the unchanged baseline best gap is -39. This is a finite parity search, not universal network feasibility. The source's additional unspecified nonparity search is not promoted to an exhaustive statement.

## Low-rank edit robustness

Hold the S_j fixed. Replace baseline shuffles A_j by P_j one at a time. Each product difference has a factor P_j-A_j; multiplying on either side cannot increase rank. Hence

    rank(M-M0) <= H = sum_j rank(P_j-A_j),
    rank M[R,C] <= rank M0[R,C] + H.

For permutation matrices, rank(P-A)=N-c(A^-1 P), counting all cycles including fixed points. Multiplying by an invertible permutation reduces the statement to I-Q; its kernel comprises vectors constant on each cycle, over every field. The row-permutation convention may invert or conjugate the relative permutation but leaves its cycle count unchanged.

An m-control NOT exchanges N/2^(m+1) disjoint pairs, so its edit rank is exactly N/2^(m+1). A two-control Toffoli contributes N/8. Products of affine mixers with inserted nonlinear gates satisfy the sum bound by another telescoping argument. High edit rank does not mean high arithmetic cost: even a rank-Theta(N) index permutation can be applied with O(N) indexing work.

For affine baseline routing, impose q_j low-bit-zero conditions on each transported parity mask. These are sum q_j homogeneous GF(2) equations in k input-mask bits. If sum q_j<k, a nonzero mask exists. Affine offsets may complement the set but do not change its boundary count. A mask with q low bits zero is constant on each aligned interval of size 2^q, giving d(A)<=N/2^q-1. Thus

    sum_j r_j (N/2^q_j-1) + H < N/4

excludes the edited family. The sum uses the actual stage orders r_j; the older unweighted reporting issue does not occur in this mathematical inequality.

For uniform r,t, choose q=ceil(log2(8rt)) and suppose k>tq. If the total normalized nonlinear-edit budget delta=sum_l 2^(-m_l-1)<=1/8, then

    rt(N/2^q-1)+N delta <= N/4-rt < N/4.

One Toffoli satisfies this budget. With t=4,r=1,q=5, every k>=21 is excluded. The weak inequality delta<=1/8 and strict dimension inequality k>tq are both essential to this particular bound. Two generic Toffolis have delta=1/4 and are not covered uniformly by that corollary.

## The two specific large baselines

The N2048 saved parity mask has baseline boundaries [93,75,83,139], capacity 390, and Fourier rank 1024. Two gate edits each have rank 256, giving cap 390+512=902 and strict gap 122.

The N4096 saved parity mask has boundaries [5,65,395,422], capacity 887, and Fourier rank 2048. Two gate edits each have rank 512, giving cap 887+1024=1911 and gap 137.

The verifier regenerates all baseline permutations, transported endpoint sets and relative cycles from the recorded basis columns. Both input masks contain the top bit, so the rank oracle gives full N/2 for any output halfset; no enormous numerical Fourier elimination is needed. The perturbation argument compares original endpoint sets, not a silently substituted moving cut for the edited network.

The per-layout statement permits gate locations and affine conjugations whose deletion recovers these stated baselines. It does not permit arbitrary changes to the affine baseline itself while retaining its old capacity 390 or 887.

## An independent endpoint strengthening

The N/4 balanced Fourier lower bound used in the robust theorem does not actually require parity structure or the imported sampling theorem. For any N/2-square submatrix A of the unnormalized Fourier matrix,

    ||A||_F^2=N^2/4,       ||A||_2^2<=N,
    rank(A)>=||A||_F^2/||A||_2^2>=N/4.

Thus the coarse robust obstruction also tolerates arbitrary fixed input and output permutations and nonzero diagonal endpoint gauges: these preserve the relevant submatrix ranks and simply change the balanced Fourier index sets. The exact rank oracle and its full-rank N/2 cases remain useful for stronger finite-layout witnesses.

## Independent controls and field caveat

The own standard-library checker reproduces 580 parity-input/arbitrary-output cases and 360 nonparity-transversal cases, each in the two source prime fields, plus all 21,342 parity-pair oracle comparisons. It independently checks 168 controlled-NOT cycle ranks, including direct matrix ranks over GF(2) and GF(12289) at small sizes. The permutation-cycle formula is valid in characteristic two as well.

Fresh, independently generated four-stage products at N64 give baseline selected rank 4, edited selected rank 19, full perturbation rank 16 and Fourier target rank 32, in both fields. These are new exact product controls; they are not claimed to reproduce the source NumPy random stream. The threshold checker verifies 32 choices of t and r at their first guaranteed one-Toffoli exponent.

Full spark over C does not assert full spark in every finite-field specialization. The reviewer preserves an explicit control: at N16, universal columns [0,1,2,3,4,13,6,7] and rows [0,1,2,3,4,6,7,12] have complex rank 8 by the theorem, but rank 7 modulo 12289 and rank 8 modulo 65537. This supports the archive's correct distinction between characteristic-zero proof and finite-field corroboration.

The matrix-class terminology is standard; see [Pernet, Computing with quasiseparable matrices](https://arxiv.org/abs/1602.01246). The actual inequalities used here were derived explicitly above rather than inferred from that abstract.

## Relationship to the eight-order Green architecture

The tested model consists of four stages with low quasiseparable rank in one prescribed order per stage, connected by specified shuffles. The accepted N16 family has three sums of eight differently ordered cyclic Green matrices, one-sided endpoint masks and an active Fourier bank. A sum of eight terms whose low ranks hold in different orders cannot be assigned rank one in one common order. The bank also cannot be erased from the model. Accordingly, neither the modified N256 example nor the fixed-rank/low-edit all-size theorem excludes that accepted seed or the remaining N64 coefficient problem.

These tools could be applied to a new Green model only after explicitly proving its stage ranks in the relevant orders and charging every factor. No such reduction is supplied by this source. Likewise, the earlier expander construction defeated only a common-subset edge-count obstruction; this moving-set theorem does not automatically settle its differing intermediate cuts.

## Replay

Run `python3 independent_checks.py` and `python3 check_single_edits.py` with the standard library. PORTABLE_REPLAY.json records isolated replay and byte-identical result files. The file flow_utils.py is copied from a previously authored independent reviewer implementation; it imports no uploaded code. No solver, NumPy, SciPy, NetworkX or network access is needed. The written all-size proof, imported theorem attribution, complete source certificate snapshot, fresh checkers and hash manifest form this additive review seal.
