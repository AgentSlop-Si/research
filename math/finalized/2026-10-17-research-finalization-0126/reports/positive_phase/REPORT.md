# M-POSITIVE-PHASE: completed primary comparison and bounded finalization proposal

17 October 2026 UTC. Read-only repository baseline: `2eaef05b9bbd6a9c884596179babe9cf474a8ff2`. Current record: M-POSITIVE-PHASE. Priority42 remains unchanged.

## Result and precise stopping scope

**The existing accepted-theorem-plus-qualified-primary-comparison activity is ready for independent closure review.** Positive first-cross scaling is a direct specialization of a classical prescribed-marginal theorem. The cycle-specific approximate preprocessing follows a readable Birkhoff theorem after an explicit diameter/scan-cost calculation. Arbitrary-invertible monomial cross-ratio cancellation matches a classical invariant. The phase-rank, doubled-character metric gap, exterior transfer and fixed N4 rejection are retained as the accepted owner-specific deductions; the inspected primary statements do not themselves assert that combined Green/Fourier theorem. That is a qualified nonmatch, not proof of novelty.

This report completes the comparison selected in the current owners. It does not promote priority, certify worldwide originality, complete historical programs, or claim a faster general-input FFT. The original Phase37 target of constructing a genuinely complex noncommuting middle network is a different research direction. It is not a remaining obligation of the accepted positive-middle comparison activity, and is neither closed nor silently selected as a new successor here.

Read in full: the current three owner rows including preserved histories, the original [Phase36 theorem](https://github.com/AgentSlop-Si/research/blob/2eaef05b9bbd6a9c884596179babe9cf474a8ff2/math/archive/objects/71/7195b895861175daad81026accc33b2dac566fb678d89160c4d6b02a1f6c8bd7__THEOREM.md), the complete [accepted Phase36 review](https://github.com/AgentSlop-Si/research/blob/2eaef05b9bbd6a9c884596179babe9cf474a8ff2/math/archive/objects/3f/3f22b6b411a54f1b20c05ff9341e97bf8980801cdaaaaf5520577faaf6de1f67__REVIEW.md), and the full later REVIEW-12 per-ID outcome. The theorem and review exact SHA256 values respectively are `7195b895861175daad81026accc33b2dac566fb678d89160c4d6b02a1f6c8bd7` and `3f22b6b411a54f1b20c05ff9341e97bf8980801cdaaaaf5520577faaf6de1f67`; their Git blobs are `c5569a783346723558bd8fe19b2d96e362ee7427` and `8acff907d1a417b677c256df65497fd5025aeb3a`. Exact fetched bytes agree with those identities. No new original-archive recovery or numerical replay is claimed.

## 1. Primary statements inspected and attribution limits

- M. V. Menon, *Matrix Links, An Extremization Problem, and the Reduction of a Non-Negative Matrix to One With Prescribed Row and Column Sums*, Canadian Journal of Mathematics 20 (1968), 225–232: definitions of pattern/consistency, Theorem2 and its complete proof. For a nonnegative matrix whose support is connected under independent row/column permutations, compatible positive margins determine a unique positive diagonal scaling product, with masks unique up to reciprocal scalar gauge. Strict positivity implies the support condition. This is the exact existence/uniqueness input needed here. [Primary paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/E15F012AA4869A056F6EAB8E1AECB177/S0008414X00051592a.pdf/matrix-links-an-extremization-problem-and-the-reduction-of-a-non-negative-matrix-to-one-with-prescribed-row-and-column-sums.pdf).
- Stephan Eckstein, *Hilbert’s projective metric for functions of bounded growth and exponential convergence of Sinkhorn’s algorithm* (2025), section2.1, Theorem2.1: a positive linear map of finite projective diameter Delta contracts Hilbert distance by at most tanh(Delta/4). This paper explicitly attributes the theorem to Birkhoff and refers its proof to a standard source. We use this printed theorem, not a claim that Eckstein originated it or that its later unbounded-kernel results are needed. [Primary research article](https://link.springer.com/article/10.1007/s00440-025-01366-9).
- Takuya Ikuta and Akihiro Munemasa, *Complex Hadamard matrices contained in a Bose–Mesner algebra*, arXiv:1411.0057v3, introduction and opening of section5, pp1–2 and18: equivalence permits arbitrary nonzero complex diagonal factors and independent row/column permutations; the Haagerup quotient set is invariant. Their surrounding matrices are type-II. Cancellation itself needs only nonzero entries, as verified below, so the Green comparison does not pretend that every Green matrix is type-II. [Primary version](https://arxiv.org/pdf/1411.0057v3).
- Idel–Wolf, *Sinkhorn normal form for unitary matrices*, arXiv:1408.5728v3, Theorem2 and its preceding argument: unitary diagonal endpoints can give a unitary matrix row/column sums1. This is used only to distinguish the different normalization problem; the already completed fixed-seed M-SEED-BALANCE comparison is not reused as this owner's completion. [Primary version](https://arxiv.org/pdf/1408.5728v3).

Franklin–Lorenz1989 is retained as historical matrix-scaling/convergence context: its publisher abstract explicitly identifies geometric convergence through Hilbert/Birkhoff, but its full proof was not newly acquired here. Marshall–Olkin1968's publisher page was accessible but the attempted full-text endpoint was not. Neither inaccessible body is used to assert an exact theorem-number match. The original Eckart–Young1936 publisher abstract was inspected; its full article was not newly read. The required complex flat-spectrum rank-tail fact is proved directly in section4 rather than attributed to an unseen passage.

## 2. Exact positive-marginal map; why it calibrates only one cross

Keep the source domain: even N>=4, omega=exp(-2 pi i/N), F[j,k]=omega^(jk)/sqrt(N). First-cross calibration uses H=sqrt(N)F, whose first row and column are1. Let A,C be invertible strictly positive biregular real matrices, with common row/column sums a,c>0; B is strictly positive. Put r=A[0,:], s=C[:,0], p=r/a, q=s/c. Then p,q are positive probability vectors.

For M=A diag(x) B diag(y) C, multiplying the first-column and first-row equations by the outer inverses gives

x*(B(s*y))=(1/a)1, and ((r*x)^T B)*y=(1/c)1.

With u=r*x and v=s*y, these are exactly

u*(Bv)=p, and v*(B^T u)=q.

Conversely, these equations recover both cross equalities. Menon's pattern-consistency condition holds because the positive matrix p q^T has the requested margins and the same full support as B. Connectedness holds because every entry of B is positive. Therefore positive u,v exist with reciprocal gauge freedom, and x=u/r,y=v/s solve the cross problem. Invertibility of A,C is needed for the equivalence; it is not a hypothesis of the scaling theorem itself.

This controls 2N-1 entries. No remaining Fourier entries follow. Normalizing H to F rescales one unconstrained mask. The calculation uses real positive marginals and transpose, not complex conjugate transpose. Unitary balancing concerns a complex unitary input, unimodular masks and all row/column sums1; its middle matrix need not have positive entries. It neither supplies the present positive masks nor contradicts the Fourier phase obstruction.

## 3. Hilbert contraction, exact iteration count and charged arithmetic

For positive vectors define d_H(v,w)=log(max_j v_j/w_j)-log(min_j v_j/w_j). Positive diagonal maps and componentwise reciprocation are isometries. Let W be a Hamiltonian-cycle permutation, beta=1-1/N and

K=(1-beta)(I-beta W)^(-1).

Its entries are (1-beta) beta^d/(1-beta^N), 0<=d<N. Their ratio R=beta^(-(N-1))<e; indeed (N-1)log(N/(N-1))<1. Positive combinations of its columns have coordinate spread at most R. Consequently any two images have Hilbert distance at most2log R<2. Eckstein's printed Birkhoff theorem therefore gives contraction at most tau=tanh(1/2)=(e-1)/(e+1) for K and K^T. The full update

S(v)=q/[K^T(p/(Kv))]

contracts by at most tau^2. Menon's scaling gives a positive fixed point v*. Both S(v)/q and v*/q have spread at most R, so after one full update d_H(v1,v*)<=2log R<2, independently of N and of the positive marginals. Thus after t>=1 updates delta=d_H(vt,v*)<=2 tau^(2(t-1)).

Recompute u=p/(Kvt). Row margins are then exact. Each column ratio z_j=vt_j(K^Tu)_j/q_j has joint spread at most exp(2delta). Its q-weighted mean is1 because the row totals are1. Hence exp(-2delta)<=z_j<=exp(2delta). For 0<epsilon<1 it suffices that 4 tau^(2(t-1))<=log(1+epsilon); this yields O(log(1/epsilon)) updates and every column relative error at most epsilon. This explicit implication concerns marginal residuals. It does not automatically bound every circuit entry's error, normwise Fourier approximation, or a floating-point implementation.

To charge the matrix-free operation, order vertices around the cycle. Solving z_i-beta z_(i-1)=b_i cyclically uses one weighted accumulated sum to determine the wraparound value by division by1-beta^N and one forward recurrence scan. Powers and the denominator can be prepared by a linear scan. The transpose uses the reversed cycle. Each full Sinkhorn update uses one K application, one K^T application and O(N) componentwise arithmetic. Setup and workspace are O(N); preprocessing is O(N log(1/epsilon)) ideal-real arithmetic and O(N) working storage, given the supplied cycle orders and margins. Reading supplied N-entry orders and margins is charged. General dense B has O(N^2) matrix-vector cost instead; Menon's theorem does not confer the cyclic scan structure.

For the source outers A=(1-eta)I+eta K_A and C similarly, eta=1/100, inversion reduces to another cyclic bidiagonal solve:

A^(-1)=[(1-eta beta)I-(1-eta)beta W]^(-1)(I-beta W).

The denominator's coefficients satisfy 1-eta beta>(1-eta)beta>0. Forming the needed first row/column and applying these specified outers therefore costs O(N) ideal arithmetic too. Once masks are supplied, the complete fixed-stage online circuit costs O(N). Masks, order storage, permutations and output writing are not free.

Exact scaling existence is not a finite exact rational construction. Iterated field arithmetic converging to an algebraic or real limit does not show finite termination or membership in the input field. An exact elementary control is B=[[1,1],[1,2]] with both margins(1,1): the scaled matrix must be [[t,1-t],[1-t,t]], while invariant cross-ratio forces t^2/(1-t)^2=2, so t=2-sqrt(2) is irrational. This is a general scaling illustration, not a new impossibility statement for every admitted cyclic input. No bit-operation, rounding-error or exact algebraic-mask complexity is certified. Roots and input scalars must be supplied or separately constructed and charged.

## 4. Monomial phase rank and the exact complex Fourier rank tail

For an entrywise-nonzero B define Phi(B)_ij=B_ij/|B_ij|. If T=D1 P1 B P2 D2 with invertible complex diagonals, then

Phi(T)=Phi(D1) P1 Phi(B) P2 Phi(D2).

Thus its rank is unchanged; the phase endpoints are unitary even though the original D1,D2 need not be. Arbitrary diagonal magnitudes do not preserve singular values or distances of B itself. Entrywise nonzero is essential to this definition.

Let U=Phi(T), rank(U)<=r, and H=sqrt(N)F. The triangle and reverse-triangle inequalities give |H_ij-U_ij|<=2|H_ij-sqrt(N)T_ij|. For completeness, choose N-r orthonormal vectors in ker U. H*H=NI implies ||(H-U)v||^2=N for each. Extend to an orthonormal basis and sum: ||H-U||_F^2>=N(N-r). This is precisely the flat-spectrum special case of the classical rank-approximation tail, over C, with no unseen real-to-complex theorem transfer.

Consequently ||F-T||_F>=sqrt(N-r)/2 and ||F-T||_2>=sqrt(1-r/N)/2. It is a necessary phase-coherence condition, not a lower bound on applying T. The primary quotient invariant concerns exact equivalence; it does not on its own imply this metric inequality. This is an explicit qualified nonmatch.

## 5. Doubled-character calculation and exterior transfer

If B is strictly positive, each entry of T has the form s_ij u_i v_j/sqrt(N), where s_ij>0 and |u_i|=|v_j|=1. Minimizing over nonnegative magnitudes gives squared error at least sin^2(theta_ij)/N, where exp(i theta_ij)=omega^(ij)/(u_i v_j). This lower bound remains valid when the nearest point on the nonnegative ray is its endpoint.

Set H2_ij=omega^(2ij), g=gcd(2,N). Direct character orthogonality gives

(H2 H2*)_(i,l)=sum_(j=0)^(N-1) omega^(2(i-l)j)=N if 2(i-l)=0 mod N, and0 otherwise.

The equivalence classes have size g, so the Gram matrix consists, after reordering, of N/g blocks N J_g. Its nonzero eigenvalues are gN, proving ||H2||_2=sqrt(gN). The two squared-phase vectors have norms sqrt(N), hence their bilinear sum through H2 has magnitude at most N sqrt(gN). Using sin^2 theta=(1-cos2theta)/2 yields

||F-T||_F^2 >= (N-sqrt(gN))/2.

Combining this with r=1 in section4 gives

c_N=max{sqrt(1-1/N)/2, sqrt((1-sqrt(g/N))/2)}, and ||F-T||_2>=c_N.

For the retained even-N domain g=2. The Gram identity itself also holds for other N; that observation does not enlarge the row's original scope. The inspected invariant/scaling sources do not assert this positive-middle bound, let alone its optimality. The entrywise magnitude minimization is a relaxation, so no attainability claim follows.

If ||A-I||_2<=delta_A<1 and ||C-I||_2<=delta_C<1, put s0=(1-delta_A)(1-delta_C). Neumann bounds and ||F||_F=sqrt(N) give

||A^(-1)FC^(-1)-F||_F <= (s0^(-1)-1)sqrt(N).

Lower singular values of A,C are at least1-delta_A,1-delta_C, respectively. The triangle inequality therefore transfers the middle bound to

||F-ATC||_2 >= [s0(1+c_N)-1]_+.

This retains the accepted quantitative exterior restriction. Since each Markov K is a convex combination of permutations, delta_A,delta_C<=2eta. At eta=.01 the limiting floor is(49/50)^2(1+1/sqrt(2))-1, approximately 0.639505352652. Exact equality through a nonzero complex middle instead requires r/N>=1-4(s0^(-1)-1)^2, which at these outer bounds is5725597/5764801, approximately 0.993199. Neither conclusion excludes arbitrarily changed outers or general complex middle networks.

## 6. Quotient invariance and the low-cost high-rank countercontrol

For four nonzero entries define CR_ik;jl(B)=B_ij B_kl/(B_il B_kj). Row/column diagonal factors cancel exactly; permutations relabel the quotient set. This is the invariant printed by Ikuta–Munemasa. On unit-modulus matrices, reciprocal entries equal conjugates, giving the usual Haagerup product. That equivalence must not be used on arbitrary magnitudes without replacing conjugates by reciprocals. Equality of the quotient sets is only a necessary equivalence condition here.

For the source G_alpha=(I-alpha W)^(-1), alpha=rho exp(i theta), rho>0, alpha^N!=1, entries in cycle positions are alpha^((p_i-p_j) mod N)/(1-alpha^N). Removing row, column and global phases leaves1 on/below the diagonal and zeta=exp(iNtheta) above. Its determinant is(1-zeta)^(N-1), by successive row differences. Thus its phase rank is1 orN. In the rank-one case rho>1, retain the accepted correction: after removing row/column phases, G_rho has negative entries. Write it as a global factor-1 times the entrywise-positive matrix -G_rho. Positivity cannot be claimed after discarding that sign without explanation.

Writing each modular distance as p_i-p_j+N 1_(p_i<p_j), the linear position terms cancel from a cross-ratio. The remaining exponent is N times a difference of two interval indicators, so Delta is-1,0 or1. Hence all quotients lie in{1,alpha^N,alpha^(-N)}. For Fourier and4|N, distinct-row/distinct-column ratios attain all N roots: row difference1 gives all nonidentity roots, while differences2 and N/2 give1. Therefore no single such Green is Fourier up to arbitrary invertible monomial endpoints.

The admitted scalar alpha=exp(pi i/N) gives alpha^N=-1, all Green entry magnitudes1/2 and full phase rankN, but quotient set contained in{1,-1}. A cyclic recurrence still applies it in O(N) exact-field operations, given that scalar and legal denominator. Its root construction, algebraic representation and finite precision are not free. This expressly prevents interpreting the phase-rank fraction as an arithmetic lower bound. Computing a general dense matrix's phase rank or all four-index quotients is not charged as part of that linear online application and is not asserted to be linear-time recognition.

The fixed exact N4 cross-ratio rejection remains historical accepted evidence for its specified outers, eta=1/100, beta=3/4 and traversals[0,2,1,3],[3,1,0,2]. It excludes positive real middle matrices for those outers even with complex monomial internal masks. Its Q(i) certificate is not rerun here and is not generalized to arbitrary paired-Green endpoints.

## 7. Disposition and exact preservation

The current stopping cells require a primary hypothesis/formula/cost map or a qualified nonmatch/access boundary. Sections1–6 meet that condition: existence and quotient invariance match; the cycle diameter and cost require the supplied structure; the combined phase metric theorem is a qualified nonmatch; inaccessible older bodies and exact-priority uncertainty remain explicit. The already accepted proof obligations are not reopened or transformed into perpetual tasks.

After independent acceptance, the private guarded proposal changes only this record's overview status from TO RESEARCH to CLOSED and prepends dated completion/scope/evidence paragraphs to14 related cells across the same three owner rows. Every earlier string in those14 cells is retained verbatim after a history separator. Stable IDs, priorities42, accepted correctness, novelty/assessment band, formula links and row order are unchanged. The live census must be read afresh by the sole publisher because other independent finalizations may proceed meanwhile; this proposal contributes only one CLOSED and one fewer TO RESEARCH view.

No external writes or new numerical experiments occurred in this comparison pass. Historical programs were not executed, imported, compiled or AST-parsed. No complete historical implementation review is claimed. No selected original obligation remains within this bounded activity after independent acceptance; broader construction, bit/precision implementation and historical-priority investigations are excluded scopes, not completed results.
