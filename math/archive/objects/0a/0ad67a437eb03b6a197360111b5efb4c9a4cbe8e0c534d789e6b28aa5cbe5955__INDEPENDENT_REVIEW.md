# Independent review of the N256 expansion and coefficient gate

## Result

Accepted with the source's narrow distinction between test capacity and coefficient realization. The unchanged four-stage N256 affine layout has an exact certificate that its transported four-path Laplacian satisfies lambda_2>101/50. Consequently no contradiction can come from comparing a target block rank with this particular transported-boundary sum, for any input subset. This is not a full-network separator theorem or a Fourier factorization certificate.

The inverse-outer-stage reduction is also valid and nontrivial. Every proposed Fourier factorization must make one specified 128-square transformed block have rank at most 16, hence make all of its 17-square minors vanish. At identity outer inverses the selected block has rank 128 and the displayed 17-minor is nonzero. These are genuine Fourier-dependent polynomial constraints; their feasibility is unresolved.

The independent replay recomputes the entire integer congruence with unbounded Python integers, both Fourier certificates, and fresh full synthetic products. No uploaded program, numerical eigensolver, optimizer or Cholesky discovery script was executed.

## Source comparison and geometry

Source archive SHA256: d036f494b8649832983ebdde1b4e44245c7f0d29216e94a2f626bfa90aebab93. Its nested nonlinear-rank predecessor is byte-identical to the archive already reviewed, SHA256 8e8ef7663a3740db1eb5d4b435b5ef4fd910be8b361aadee3322dab52f807a1a. The three affine basis-column lists and the five-Toffoli comparison metadata also match that predecessor exactly. The present positive expansion certificate uses the unmodified maps; the Toffoli list in AFFINE_LAYOUT.json is not applied when forming its graph.

All permutations have the new-to-old convention (P x)[i]=x[p[i]]. Starting with v0=(0,...,255), define v_(j+1)=v_j[p_j]. Each v_j is a permutation, and each consecutive pair forms one undirected edge. The union is a multigraph with 4*255=1020 edge occurrences. Multiplicities are retained. Its integer Laplacian L is symmetric, has zero row sums and trace 2040.

For an input set A, its stage-j membership is membership of v_j[i] in A. Therefore the number of graph edges crossing A is exactly the sum of the four natural-order boundary counts for the transported sets. This verifies the link between the graph and the rank-test formulation, including permutation orientation.

The result is about this four-path affine layout. It is distinct from the earlier eight-order MGG Hamiltonian-cycle bank, its spectral theorem and its common-subset edge-count budget. No coefficient feasibility or universal no-go transfers between these grammars merely because both use expansion.

## Exact positive definiteness

The supplied compressed JSON contains an upper triangular integer matrix T of size 256. The checker verifies every entry's type, every zero below the diagonal and every nonzero diagonal entry. Hence T is invertible over Q and R; it need not be unimodular.

Set

    M=50L-101I+50J,     J=1 1^T,
    H=T^T M T.

All 65,536 entries of H are independently recomputed with arbitrary-precision integers, using the sparse Laplacian action and the exact rank-one J contribution. H is exactly symmetric. The independent results are

    nonzeros in T: 32,264;
    maximum absolute T entry: 1,416;
    minimum H diagonal: 16,706,411;
    minimum (H_ii-sum_(j!=i)|H_ij|): 4,681,152.

Every dominance margin is saved. A real symmetric matrix with these strictly positive margins is positive definite, by Gershgorin or the corresponding quadratic-form decomposition. Invertible congruence gives positive definiteness of M.

The constant vector is an eigenvector of M with eigenvalue 50*256-101=12699, which the checker verifies by row sums. On its orthogonal complement, J vanishes and M acts as 50L-101I. Hence the restriction of L there is strictly greater than 101/50, proving lambda_2(L)>2.02. No floating eigenvalue estimate enters this proof.

The source's conservative int64 partial-product bound, 1,379,922,104,160, is reproduced and is below 2^62. The independent verifier does not need this bound for arithmetic safety because every operation uses unbounded integers. It additionally checks every diagonal and the supplied mixed-entry probes directly from

    H_ab=50 sum_edges (T_ia-T_ja)(T_ib-T_jb)
          -101 sum_i T_ia T_ib +50(sum_i T_ia)(sum_i T_ib).

Thus the theorem rests on the exact supplied witness, not the numerical method that discovered it.

## Exactly which rank tests are exhausted

For a nonempty proper set A with a=|A|, let x=1_A-(a/256)1. Then x is orthogonal to 1 and ||x||^2=a(256-a)/256. Therefore

    sum_j d(A_j)=1_A^T L 1_A
       > (101/50) a(256-a)/256
       > min(a,256-a).

The last strict inequality holds at every a=1,...,255; the checker verifies all cardinalities exactly. At a=128 the real lower bound is 129.28, so every balanced cut has at least 130 edges.

For the four order-one quasiseparable stages, the tested inequality is

    rank M_target[A_3^c,A_0] <= sum_j d(A_j),
    A_(j+1)=P_j^-1(A_j).

Any target block has rank at most min(a,256-a), strictly below the right-hand side. Hence this comparison cannot contradict any target, Fourier or otherwise, whatever the initial subset. The conclusion exhausts this specific scalar boundary-sum test family, including all parity, interval, periodic and nonlinear initial sets.

The intermediate sets here are coupled by the exact permutations. More general cuts of the scalar network may use different intermediate choices, include internal state wires, or exploit additional constraints. They are not certified by the four-path argument. Nor does the large capacity assert that actual stage cross ranks attain that upper bound. Spectral expansion is a barrier to this test method, not a sufficiency theorem for matrix factorization.

For stages of orders r_j, weight the corresponding path edges by r_j. The same calculation shows lambda_2(L_r)>=2 suffices for capacity at least every target block's maximum rank. Equality at a balanced cut still prevents a strict rank contradiction; strict spectral inequality is not required for this general sufficient criterion.

## Exact comparison with the modified predecessor

The independent checker also applies the predecessor's five Toffoli changes to the third shuffle and evaluates the known mask-112 graph cut. It has exactly 124 edges, recovering the previous Fourier rank 128 versus capacity 124 exclusion.

This gives an exact Rayleigh upper bound for the edited graph:

    lambda_2(L_edited) <= 124/64 =31/16 <2.

Thus the contrast with the unmodified graph is rigorous without relying on the source's numerical estimate near 1.509. The unchanged graph's reported estimate near 2.029 and the random-layout numerical sampling remain exploratory data. This audit does not claim to reproduce those floating eigensolver experiments, and they are unnecessary for either exact theorem.

## Why inverse outer stages stay quasiseparable

Suppose

    F=S4 P3 S3 P2 S2 P1 S1.

Since F is invertible, every square S_j is invertible. This does not force its individual generators or corner entries to be nonzero. Define C4=S4^-1 and C1=S1^-1. Invertible matrices preserve complementary off-diagonal block ranks under inversion, so C1 and C4 have the same order-one quasiseparable cut bounds.

For completeness, let I,J be complementary coordinate sets and A invertible. The kernel of (A^-1)[I,J] consists of y in E_J whose preimage A^-1 y lies in E_J. Mapping y to that preimage is a bijection onto the kernel of A[I,J]. Both domains have dimension |J|, so the two block ranks are equal. Swapping I,J gives the other off-diagonal block. This proof has no leading-principal-minor or nonzero-generator assumption.

Conversely, choosing invertible quasiseparable C1,C4 gives quasiseparable inverse outer stages. Treating their matrix entries as variables is therefore legitimate, provided all quasiseparable rank constraints and determinant-nonzero guards are retained.

## The concrete Fourier coefficient gate

Multiplication on the stated sides gives

    H=P3^-1 C4 F C1 P1^-1=S3 P2 S2.

Take C={i:bit_6(i)=0}. It has 128 elements and three natural-order boundaries. Set R={i:bit_6(p2[i])=1}, also of size 128; the transported indicator has 13 boundaries. The two-stage moving-partition inequality gives

    rank H[R,C] <=3+13=16.

Thus every 17-square minor on R,C must vanish. Each entry of H is bilinear in the matrix entries of C4 and C1, so each such determinant is bihomogeneous of degree 17 in each outer inverse, total degree 34. This degree statement concerns matrix entries; substituting a particular generator parametrization may change the degree and must not discard zero-generator branches.

These equations are necessary and not known sufficient. They must be combined with the two outer quasiseparable constraints, their invertibility guards and any further conditions required for H to factor as S3 P2 S2. One selected vanishing minor alone is not equivalent to the rank-16 condition.

This gate is compatible with the expansion result. Unknown inverse outer factors mix coordinates according to their actual coefficients before testing the middle product. That is not the earlier test using only a fixed transported input set through all four permutations.

## Exact nontriviality and orientation checks

At C1=C4=I,

    H0=P3^-1 F P1^-1,
    H0[i,j]=F[inv(p3)[i],p1[j]].

The right index is p1[j], not inv(p1)[j], under the declared new-to-old convention. The independent verifier uses this formula and matches the source's first 17 selected rows and columns. The full selected block has rank 128 in both fields, and the fixed minor determinants are

    8799 modulo 12289;
    20067 modulo 65537.

Each modulus is verified prime, and each chosen root has exact order 256. Specialization defines a ring map from Z[zeta_256] because the root satisfies z^128+1=0. A nonzero specialized determinant proves the same cyclotomic determinant is nonzero over characteristic zero. These constants are fixed Fourier entries, not a modular substitution of a fitted algebraic seed.

The identity outer stages are themselves admissible, so the equation is genuinely nontrivial on the allowed domain. Their failure does not exclude other invertible outer stages. Full-matrix invertibility preserves full rank but need not preserve a selected submatrix's rank after left/right mixing; a reduction from 128 to at most 16 is an unsolved requirement rather than a contradiction.

## Fresh positive and degenerate controls

In both fields the own checker creates fresh independent-generator order-one S2,S3 matrices and obtains selected middle rank exactly 16. Taking S2=S3=I gives selected rank zero, checking a zero-generator boundary case.

For a full nontrivial positive control, it chooses S4 as upper unit all-ones triangular and S1 as lower unit all-ones triangular, with their exact bidiagonal inverses. It assembles the complete four-stage product, applies both inverse outer factors and the correct inverse shuffles, and recovers every one of the 65,536 entries of S3 P2 S2 exactly. These factors and checks are independently generated; they do not purport to replay the source NumPy random stream. Applying the same nontrivial inverse outer factors to the Fourier target still fails the selected rank bound, without any global infeasibility inference.

## Bounded implementation caveat

Static inspection finds one reusable-helper defect in the source: rank_and_det_mod returns early at a missing pivot in a square matrix. Its determinant result is correctly zero, but its reported rank may be too small. For [[0,1],[0,0]] it returns rank zero even though the rank is one. The archive separately uses rank_mod for its singular-block rank calculations, and both certified 17-square minors are nonsingular, so this defect does not affect the accepted results. The relevant source excerpt is preserved as inert text. Future use of that helper as a general rank routine should be corrected.

## Cost and remaining obligations

The integer witness is a finite proof artifact, not a coefficient generator or Fourier evaluator. Its verification and storage costs are charged to the audit, not treated as free algorithmic preparation. The spectral theorem supplies no all-length family or exact stage coefficients.

The coefficient gate reduces which unknown stages appear in a necessary condition; it does not solve the resulting algebraic problem. Dense evaluation of candidate transformed matrices has polynomial preparation cost, and all selected minors form a very large equation family. Using quasiseparable scans or ordinary FFTs to evaluate proposed candidates still needs an explicit ledger. There is no demonstrated working transform to which a sub-N-log-N operation count can be assigned.

The surviving question is exact coefficient compatibility for the unchanged four-stage N256 layout, including all singular-generator charts within invertible stages, or a stronger full-network obstruction. Passing the now-exhausted boundary tests is not evidence that a solution exists.

## Portable replay

Run `python3 independent_checks.py` with the Python standard library. It reads the frozen layout, integer witness and certificate data, recreates every exact assertion above, and writes VERIFIED_RESULTS.json. PORTABLE_REPLAY.json records an isolated run with byte-identical output. No NumPy, SciPy, network, eigensolver, Cholesky routine or uploaded program is used. Source provenance, exact inputs, complete proof review, fresh checker and hash manifest form this additive seal.
