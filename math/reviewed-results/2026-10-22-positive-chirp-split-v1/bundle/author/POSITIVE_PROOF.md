# Original positive chirp: an exact 5-adic exclusion

Status: complete author theorem with exact certificates and byte-identical cold replay, submitted for fresh independent review. This is not a publication, native-table update, or owner closure.

## 1. Target and claim

Let N=5m be odd, with gcd(m,5)=1 and N congruent to 1 modulo 4. For every primitive complex Nth root omega, set F_ij=omega^(ij), h=(N+1)/2, A_jj=omega^(h j^2), and B_N=(F^(-1)+A)^(-1). The claim is that B_N is not a sum of two weighted Hamiltonian-cycle Green resolvents with arbitrary complex diagonal endpoints, including singular and entirely zero endpoints, and arbitrary edge weights, including zero edges, with each Green denominator nonzero. Coordinates remain fixed, and no unmatched endpoint permutations are permitted.

Equivalently the actual original positive exception set E_plus is empty. The certificate excludes a larger formal coefficient locus, so it does not need to assert that every independently chosen pair (eta,g) occurs as the Gauss data of a primitive omega. The implication is only from actual Gauss data to the excluded locus.

The accepted restriction and necessity inputs are the recovered files in source_inputs, with their exact hashes in SOURCE_INPUTS.json. They establish the formula and closed necessary system recalled below. Their accepted positive cutoff and square-modulus conclusions are preserved, not recomputed or weakened. Negative-family algebraic outputs are not evidence here. Some algorithms and minor-row choices were adapted from those packages, but every polynomial used in this proof is recomputed with the positive cubic sign.

## 2. Reduction to the exact positive polynomial curve

The accepted all-character Gauss identity gives G^2=N; either real sign is allowed. For S=(0,m,2m,3m,4m), eta=omega^(m^2) has exact order five, and

B_N[S,S]=H(G,eta)/(1+G^3),
H(g,eta)_ij=eta^(ij)-g eta^(-3(i+j)^2)+g^3 eta^(-3i^2) delta_ij.

The denominator is nonzero since |G^3|=N^(3/2)>1. The principal restriction of a weighted Hamiltonian Green matrix is again a Hamiltonian Green matrix, whose selected-to-selected edge weights are the products on the intervening arcs. The total edge product and legal denominator are preserved. There is no division by any edge, so zero edges are included. Diagonal endpoints restrict entrywise, including every singularity. Scaling the target by a nonzero scalar is absorbed in the left endpoint masks.

Thus an allowed full representation gives an allowed representation of H(G,eta). The arithmetic fact used below is v_5(N)=1. Positivity of G is not assumed, and the fifth-root block is not identified with B_5 when N>5.

## 3. The closed necessary projective system

For each ordered pair pi,tau of five-cycles, take five nonzero row pairs u_i=[a_i:b_i] and five nonzero column pairs v_j=[c_j:d_j]. Put U_ii=a_i, U_i,pi(i)=b_i, V_jj=c_j, V_tau^(-1)(j),j=d_j, with all other entries zero, and T=UHV.

An allowed representation forces:

1. T_ij=0 outside j in {i,pi(i),tau(i)}.
2. All maximal 11-column minors of the 25-by-11 matrix M vanish, where row (i,j) is the ten coefficient slots of V_ij X_i+U_ij Y_j, followed by T_ij. The ten scale symbols are coefficient-column labels, not extra projective variables.

For invertible masks, writing the two summands as P,Q gives U=D_lambda P^(-1), V=Q^(-1)D_mu and U(P+Q)V=D_lambda V+UD_mu. This proves necessity. Zero edges do not require any division. For a selected 11-row minor, let n_i and m_j be the multiplicities of matrix row and column indices. Independent direction scaling multiplies that minor by product lambda_i^(n_i-1) product mu_j^(m_j-1). If an exponent would be negative, the corresponding coefficient column is identically zero and the minor is zero. All nonzero minors therefore have nonnegative multidegrees, of total row degree six and column degree six.

For singular masks, replace every zero mask entry by a formal parameter t and retain all edge weights and Green denominators. The masks are then invertible over C((t)). Normalize each sparse inverse pair by its lowest t-valuation, obtaining integral coordinates with at least one unit in each pair. The multihomogeneous equations specialize to the required closed system at t=0. No scale-variable limit, nonzero base coordinate, or invertible limiting U or V is required. Entirely zero masks and all projective boundaries are retained.

We use selected actual augmented minors to contradict this necessary condition. Rank at most ten is never asserted to imply consistency when the first ten columns drop rank.

## 4. Exact nonvanishing by an elementary 5-adic coefficient test

Work in K=Q[z]/(z^4+z^3+z^2+z+1), and consider any nonzero certificate polynomial p(g) in K[g]. Its four-embedding norm P(g) is a nonzero rational polynomial. Write uniquely

P(g)=A(g^2)+g B(g^2), and E(n)=A(n)^2-n B(n)^2.

Then E is nonzero: E(g^2)=P(g)P(-g), a product of nonzero polynomials. If p(g0)=0 under any fifth-root embedding, then P(g0)=0 and hence E(g0^2)=0. This treats both signs and all embeddings, unlike a real/imaginary-part gcd argument. In particular, no negative-axis positivity certificate is imported.

For E(n)=sum c_k n^k, define d=min_k(v_5(c_k)+k), ignoring zero coefficients. The rational polynomial 5^(-d) E(5x) has 5-integral coefficients. Its reduction modulo 5 is

I(x)=sum_(v_5(c_k)+k=d) overline(c_k 5^(k-d)) x^k.

If I(1),I(2),I(3),I(4) are all nonzero modulo 5, then E(5m) is nonzero for every integer m coprime to 5. Indeed, the normalized value reduces to I(m mod 5), a nonzero residue. This is an exact coefficient/divisibility argument, not a numerical or finite-size sample.

For one explicitly identified residual rank leaf, this sufficient unit-residue test is inconclusive. A separate exact integer-root certificate completes that case: remove the zero-root factor from E, clear rational denominators and divide by the integer coefficient content to obtain a primitive integer polynomial Q. If its nonzero constant is 5^k, every nonzero integer root divides 5^k. A positive integer root with v_5(N)=1 must therefore be 5. An exact nonzero Q(5) then excludes every actual eligible N. This is a second arithmetic test, not a claim that the failed 5-adic test succeeded.

Each certificate records p, the full norm P, its even and odd parts A,B, E, d, every coefficient of I, and all four unit residues. Exact reproduction rederives these data. Rational coefficient denominators are included in v_5; after normalization the residues invert only denominators prime to 5.

## 5. Invertible off-support blocks and complete row transport

For j outside the row support define A_ij=H[(i,pi(i)),(j,tau^(-1)(j))] and I_j={i:j not in {i,pi(i),tau(i)}}. The two row and two column index sets overlap in at most one element: j differs from both row indices, and tau^(-1)(j) differs from i. Thus every such block is among the 90 unordered 2-by-2 minors whose row and column pairs have overlap at most one; reordering changes only the determinant sign.

POSITIVE_BLOCK_CERTIFICATES.json recomputes all 90 positive-sign determinants and proves their 5-adic coefficient tests. Hence every required block is invertible at every actual admissible (eta,G).

The off-support equation is u_i^t A_ij v_j=0. For i,k in I_j, eliminating the shared nonzero v_j gives u_i^t C_ikj u_k=0, where C_ikj=A_ij J A_kj^t and J=[[0,1],[-1,0]]. Its determinant is the product of the two block determinants, hence nonzero. The equation is therefore the bijective projective transport u_k proportional to J C_ikj^t u_i. A spanning forest expresses each row direction from one unrestricted projective root per component; reverse edges use adjugates, not inverses with specialized denominators.

The algorithm divides a polynomial transport matrix by its common scalar content. This scalar cannot vanish at an admissible parameter: otherwise the undivided product of already invertible transition matrices would vanish. Inductively all normalized transports remain invertible. This argument is only for full transport matrices. It does not justify dropping contents of quadratic equations, directions, or minors; those contents are separately retained and tested.

Every remaining internal edge produces a homogeneous binary quadratic on the component root. For each of 50 symmetry representatives, two selected quadratics have a nonzero homogeneous resultant. POSITIVE_ORBIT_ROWS.json records both quadratics, their contents, the exact resultant, and all three nonvanishing certificates. Consequently the two quadratics have no common projective zero, including infinity and repeated-root specializations. These representatives cover exactly 384 actual ordered pairs.

## 6. Residual augmented-rank certificates

The other 192 ordered pairs form 28 symmetry orbits. Each representative is recomputed from the same positive target, original off-support blocks, and complete projective forest. Its graph has either one component or a three-vertex component and a two-vertex component.

For a connected graph, retain one homogeneous root [x:y] and one transported quadratic q=ax^2+bxy+cy^2, with its scalar content tested. In the split case, the selected quadratic for the two-vertex component is x(ax+by) or y(bx+cy). The coefficient b is explicitly retained and proved nonzero. Its exhaustive projective roots are [0:1] and [b:-a], or [1:0] and [c:-b], respectively. Each pair remains nonzero and the roots remain distinct when a or c vanishes. The three-vertex component retains the entire projective root. Both small-component branches are separately certified.

For each column choose an actual off-support row and recover v_j proportional to J A_ij^t u_i. It is nonzero because the block and row direction are nonzero. Thus no rank-zero column continuum is omitted. Scalar contents removed from row directions, column directions, quadratic equations, or selected minors are recorded as guards and subjected to the exact 5-adic test.

The selected determinant is an actual eleven-row minor of the original 25-by-11 matrix M. Its homogeneous degree in the free root is computed from the multidegrees in Section 3, counting only row and column directions depending on that root. This prescribed degree is retained even when the coefficient of its highest affine power vanishes.

For q=ax^2+bxy+cy^2 and a degree-d minor f, form the homogeneous resultant at fixed degrees (2,d). The implementation computes a polynomial identity as follows. If f(1,t)=sum f_k t^k, reduce c^(d-1) f(1,t) modulo ct^2+bt+a as U+Vt, using division-free recurrences. Then

Res(q,f)=(c U^2-bUV+aV^2)/c^(d-1).

The displayed division is exact in K[g]. This identity is established where c is nonzero and extends as a polynomial identity; there is no division by its specialized value. It is the fixed-degree Sylvester resultant and retains infinity, repeated roots, zero forms, and affine degree drops. Each leaf supplies the exact remainder polynomials and quotient, which can be checked against the fixed-degree determinant. A common projective zero necessarily makes the resultant zero.

All guards and all but one selected resultant have successful 5-adic coefficient tests. The sole exception is representative 87, split branch 1, witness 1. Its unit initial form is x^8(1-x+x^2-x^3+x^4), which vanishes at x=4 modulo 5; that test is honestly recorded as unsuccessful. INTEGER_BRANCH_087_B1_W1.json instead proves that its square eliminant is a nonzero rational scalar times n^8 Q(n), where Q is primitive integral of degree 344, Q(0)=5^48, and Q(5) is a recorded nonzero integer. The integer-root argument of Section 4 excludes every positive integer N with v_5(N)=1. The coverage gate requires this exact supplementary certificate and does not accept the unsuccessful unit-residue flag. Thus each exhaustive branch contradicts the necessary rank condition. No surviving block-system point is promoted into a full-target construction; in fact no projective necessary point survives.

## 7. Symmetry and exhaustive pair coverage

Enumerate all permutations of (1,2,3,4) lexicographically, prepend 0, and form the successor map. These are precisely all 24 five-cycles. Ordered pair index 24i+j uses pi as the outer cycle. The following two transformations preserve the entire projective necessary system:

- Dilation r_a(i)=ai modulo 5 for a=1,2,3,4: H(g,eta)_(ai,aj)=H(g,eta^(a^2))_(i,j). Simultaneously conjugate both cycles by r_a. All fifth-root embeddings are already included in each norm certificate.
- Transpose: H^t=H, U'=V^t, V'=U^t sends (pi,tau) to (tau^(-1),pi^(-1)), swaps scale-column labels, and permutes equation rows. No U or V inversion is used.

The transformations preserve zero coordinates and singular limits. POSITIVE_ORBITS.json independently enumerates their 78 orbits and explicit transport data. The coverage gate verifies the actual successor maps, not only counts. It verifies a disjoint partition of all 576 ordered pairs into the 384 row-excluded pairs and 192 residual-rank pairs, and requires all branches of each of the 28 residual representatives to have a successful retained certificate.

## 8. Conclusion and exact scope

Suppose an original eligible B_N had the permitted two-Green representation. Section 2 would give a representation of H(G,eta), with G^2=N and v_5(N)=1. Section 3 gives a point of its closed necessary projective system. The exhaustive pair partition places its induced cycles in a row-excluded or residual-rank-excluded orbit. The corresponding exact certificate, transported by Section 7, contradicts that point by the elementary nonvanishing test in Section 4. Hence no allowed representation exists and E_plus is empty.

No finite cutoff, square-family congruence, assumed positivity of a Gauss sign, or independent realizability of formal (eta,g) is used in this final implication. The proof uses actual primitive-character Gauss data only through the accepted formula, exact fifth-root order, G^2=N, and v_5(N)=1.

This is a two-term representation obstruction for the original fixed-feedback target. It says nothing about unmatched endpoint permutations, moduli divisible by 25, different feedback, general Fourier algorithms, exact-three full-target upper bounds, more summands, products, stability, bit cost, or production performance. It does not close the broad research owner or revise any source table. The positive and negative original families remain separately certified results; no negative-family algebraic exclusion is a dependency of this proof.
