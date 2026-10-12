Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery details are omitted; mathematical source identity, assumptions, costs and limitations are preserved. Original source-report SHA-256: e9386e3b7c280cd5ba6a748be006029b7976ce70584bf68df4a75dc923894b62.

# Independent review of depth two scan dimension

Date: 2026-10-12 UTC. Verdict: ACCEPT, within the depth-two scope below. The broader M-SCAN-DIMENSION all-size and all-depth gate remains open.

## Reviewed result and provenance

The reviewed candidate is M_SCAN_DIMENSION_AllN_Depth2_Candidate_2026-10-12.zip, SHA256 ee5f179d1149ee30b6a85e76fc0ad2a93e85eee1e26fa6ad570b4cbd73d2bd29. Its proof SHA256 is f70940f6c6312ba6d3aecb0519bea955b7fedd4184932283e10f29c1f9077549. Every one of its 11 manifest members was hash- and size-checked. The original model certificate is bound to SHA256 e498e7b16cbaac2ded9976f8ef0222aa990c750b6fd18a73cf3b47ba650885f7.

Accepted statements, over the complex field:

1. For every integer N >= 8, the original separated-generator depth-two product image has Zariski-closure dimension 9N-12 with the fixed zero-based permutation p_N=(1,N-3)(2,3)(N-4,N-2).
2. For every dyadic N >= 8, the same dimension holds with actual full binary-digit reversal.
3. For each of these charts there are explicit rational regular points with invertible stages and all active generators nonzero. On a nonempty Zariski-open set, the entire original 10N-coordinate Jacobian kernel is the N+12-dimensional span of 12 local redundancies and N interstage diagonal gauges.

This is an all-size theorem at depth two, supported by a uniform symbolic minor argument. The finite larger-size controls are not used to infer the theorem.

No original upload or candidate program was executed, imported, compiled, or AST-parsed. The reviewer authored independent_review.py, differentiated the defining monomials symbolically with SymPy, and used SymPy DomainMatrix integer determinants and a separate vectorized modular elimination implementation. Supplied JSON was read as certificate data, with every numerical conclusion recomputed.

## Exact architecture and parameter count

The source stage is S_ij=a_i b_j for i>j, S_ii=d_i, and S_ij=c_i e_j for i<j. It has 5N raw coordinates. Its generic local kernel has four inactive coordinates and the two independent pair scalings, giving dimension 5N-6. The two stages therefore have exactly 10N raw coordinates, not an enlarged quasiseparable parameterization.

Fix P e_j=e_{p(j)}. With C=P A P^{-1}, the source output B P A becomes B C after the fixed right multiplication by P^{-1}. The second order is p(0),...,p(N-1). In both accepted families P is an involution. Assigning the C generator at label p(j) to original A coordinate j reproduces the original source stage exactly. The independent controls reconstruct B P A directly before applying this fixed output normalization.

For fixed nonzero epsilon, a_raw=epsilon a and c_raw=epsilon c are invertible linear changes of the original coordinates; b_raw=b, e_raw=e, and d_i=1 specify the witness. Fixing b at the first coordinate and e at the last is a valid local gauge slice because those values are nonzero. It leaves 4N-6 off-diagonal variables per stage. The leading minor uses these 8N-12 variables and N independent B diagonal variables.

The upper bound 9N-12 is also justified directly: the two stage-image dimensions total 10N-12 and the interstage diagonal torus has dimension N and acts freely on invertible tuples. Invertibility is a nonempty dense-open condition. Thus the bound applies to the full image closure. The candidate does not enlarge the source architecture or rely on singular exceptional components of a broader quasiseparable variety.

## Exact anchor and extension computations

The two prescribed 52-by-52 anchor matrices were reconstructed by symbolic differentiation of T_standard+T_order, using the precise listed row and column order. The exact integer determinants are:

- sigma=[0,5,3,2,6,1,4,7]: -8143549790088517861170017351544864768000000000000.
- Actual N=8 bit reversal [0,4,2,6,1,5,3,7]: 1089636968541322778589785838143320304025600000000000.

They agree with the candidate integers and residues modulo 12289 and 65537. They were additionally checked modulo the fresh primes 1000003 and 1000033. Both full 56-by-52 off-diagonal leading Jacobians have exact rational rank 52. Duplicate-row and deleted-column mutations produce determinant zero.

For each of the 25 pairs (k,l) in {2,3,4,5,6} squared, the reviewer inserts a ninth symbolic coordinate into the two anchor orders. Symbolic differentiation on the 16 incident directed edges produces the claimed row and column blocks, including their zero cross-blocks. The lexicographically first nonzero 4-by-4 minors match every candidate row choice, every matrix entry, and all 50 signed integer determinants. The independently generated complete matrices and determinants are in results/EXTENSION_MINORS.json.

For a new coordinate v, only its own eight generator columns can affect its incident anchor edges. These columns vanish on anchor-anchor edges and on edges incident to other nonanchors. Anchor columns may affect the lower-left block, which does not spoil the determinant identity. The selected matrix is therefore exactly

L_N = [[L_8, 0], [*, direct_sum_v(R_v,Q_v)]].

All rows and columns are distinct, and there are 52+8(N-8)=8N-12 of each. Its determinant is the base determinant times the product of the selected local determinants. This proves nonvanishing at every size satisfying the anchor-order hypothesis; it is not an extrapolation from the enumerated controls.

## Ordering proof for every coordinate and boundary cases

For the transposition family, the anchors are 0,1,2,3,N-4,N-3,N-2,N-1. They are distinct at N=8 and above, and the induced second order is sigma. Every nonanchor lies between the fourth and fifth anchors in both orders because it is fixed by p_N. Hence k=l=4 for every such coordinate. The leading coefficient is exactly Delta_sigma*(29754*(-2160))^(N-8). N=8 is the base with an empty product; N=9 already has the valid single extension.

For bit reversal N=2^m with m>=4, the anchors are 0,1,2,N/4,N/2-1,N/2,N-2,N-1. Reversing the m digits gives, in that order, 0,N/2,N/4,2,N-2,1,N/2-1,N-1. Since N>=16, these eight values are distinct, and sorting their labels gives sigma. Both orders contain anchors at positions 0,1,N-2,N-1. A nonanchor cannot occupy one of these four positions; consequently it has at least two anchors before it and at least two after it in each order. This proves 2<=k,l<=6 for every coordinate and every m>=4.

At N=16 all inequalities and distinctness hold; no extra exception is needed. At N=8 the displayed dyadic formula repeats anchor 2 and must not be used. The candidate correctly uses its separate actual-bit-reversal 52-by-52 minor there. The reviewer expressly tested and rejected that seven-distinct-anchor misuse.

Implementation controls inspect every nonanchor for all transposition sizes 8 through 257 and every dyadic size 8 through 65536. These controls agree with the preceding all-size proof; the finite range is not part of the logical justification.

## Polynomial lift and explicit rational regular points

Write B=I+epsilon T_B and C=I+epsilon T_C. For each chosen normalized off-diagonal parameter, the product-rule derivative is epsilon D + epsilon^2 D T_C, or epsilon D + epsilon^2 T_B D. After dividing these columns by epsilon, the chosen (9N-12)-square matrix is exactly A_N+epsilon B_N. The chosen B diagonal columns have constant parts E_ii. Accordingly A_N is block diagonal with I_N and L_N.

Thus the normalized selected determinant is epsilon^(8N-12)*det(A_N+epsilon B_N), with nonzero constant coefficient C_N in its second factor. This already proves a nonzero polynomial minor at every size. Passing to original raw coordinates multiplies by a nonzero fixed scalar at any chosen epsilon!=0, so it proves the required original-chart rank.

The bounds K=7000N and r=9N-12 are valid: an anchor generator is at most 19, a T entry at most 361, and a product-derivative entry at most 6859N. The diagonal columns satisfy the same bound. With D_N=2*r!*(2K)^r and epsilon_N=1/D_N,

|det(A+epsilon_N B)-det A| <= r!*K^r*(2^r-1)/D_N < 1/2.

The estimate uses the expansion by the number of B factors and epsilon^j<=epsilon for epsilon in [0,1]. Since det A is a nonzero integer, the rational specialization cannot vanish. Also 361(N-1)/D_N<1. Each stage has diagonal 1 and off-diagonal absolute row sum below 1, so both stages are invertible. This works for every N in the stated families and establishes a nonempty Zariski-open regular, invertible, active-nonzero domain.

The independent source-coordinate controls evaluate this exact rational epsilon modulo two fresh primes, rather than substituting the candidate's epsilon=1 control. For N=8,9,10,16,17 in the transposition family and N=8,16 in the bit-reversal family, all 14 audits verify the full original Jacobian rank, the selected product minor, source-to-normalized equality, and invertible A and B. They additionally verify the exact integer inequalities in the rational-error and diagonal-dominance bounds.

An important chart distinction is preserved: epsilon=0 is not used as a regular witness. The epsilon-dependent normalized chart collapses to rank N there. For the N=8 transposition witness the original raw chart instead has rank 36 at epsilon=0, while the normalized chart has rank 8. The candidate correctly qualifies its rank-N statement as normalized; it must not be restated as an original-raw-chart rank claim.

## Completeness of the full gauge kernel

For one stage with all active generators nonzero, dividing a tangent equation delta(a_i b_j)=0 by a_i b_j yields delta a_i/a_i + delta b_j/b_j=0. The lower bipartite graph is connected: the first column and last row connect every active a and b vertex. It has exactly one scaling kernel, with the two inactive lower coordinates independent. The upper graph gives the analogous result. The diagonal entries are independent. Hence each stage has exactly six local kernel directions, and the two-stage tuple has 12 independent local directions.

The interstage variations delta C=HC and delta B=-BH are represented by row scaling C and column scaling B within the original chart, including the diagonal parameters. In source coordinates the C row index is matched through P to A. The product derivative is -BHC+BHC=0. If a linear combination of these directions lies in the local 12-dimensional kernel, its stage-matrix variation HC must vanish. Since C is invertible, H=0; the remaining independent local coefficients vanish. Therefore the full gauge span has dimension N+12.

The regular rank 9N-12 gives raw nullity 10N-(9N-12)=N+12. Equality of these dimensions proves the entire kernel is precisely the gauge span. This is a pointwise theorem on the stated open set, not merely an observed finite modular nullity. The independent original-source controls verify JG=0 and gauge rank N+12 and reject an unmatched interstage-gauge mutation.

## Adversarial controls and scope

Additional exact negative controls give leading rank 44 for identity ordering, 37 for all-one anchor coefficients, and row-block rank 2 at the forbidden exterior cut (0,0). These diagnose the minor construction only; they are not claimed to classify all product points for those choices.

No substantive mathematical correction is required for acceptance. The epsilon-zero raw/normalized distinction above is an explicit preservation note. The rational denominator has O(N log N) bits; naive repeated rational storage can cost O(N^2 log N) bits. The certificate is not an efficient coefficient solver for a requested target. The source's deliberately loose two-stage executor upper bound remains at most 10N multiplications and 8N additions, with permutation and coefficient work charged separately.

Keep the following open or unchanged:

- Arbitrary-depth t>=3 repeated-bit-reversal equality at previously unproved lengths.
- Arbitrary-depth t>=3 generic gauge completeness below saturation.
- General saturation and the necessary nongauge kernel at ambient saturation.
- Fourier membership, exact Fourier factorization, and coefficient synthesis for specified targets.
- Historical novelty or priority.
- The original accepted N=8,16,32 finite-depth certificates, all-size upper bound, and identity-shuffle obstruction.

Since 9N-12<N^2 for N>=8, this depth-two result does not parameterize generic dense matrices. It supports no new FFT speedup or unrestricted FFT lower bound. The broader all-depth dimension and Fourier-construction problems remain open.
