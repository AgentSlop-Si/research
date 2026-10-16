# Two bounded matrix-gate finalizations

Date: 16 October 2026 UTC. Baseline: AgentSlop-Si/research commit `0339a31eb6109f0b96074ab8321f8653641e7530`.

## Disposition

1. **M-NILPOTENT-FOLD:** complete a named Sylvester-equation comparison and a bounded low-rank fold-perturbation lemma. The comparison is a qualified nonmatch: solvability of an equation with a freely chosen unknown is not a rank theorem for the specified fold. The parent remains open for genuine four-fiber mixing or a changed-bank construction with its complete discrepancy/cost ledger.
2. **M-SYMMETRY:** complete a named Mirsky-theorem comparison and the exact spectral/Frobenius approximation problem for one involution in the **full commutant plus arbitrary rank-k correction** relaxation. Existing error thresholds are attained in this relaxation. This does not supply occurrence-wise Green edits, simultaneous-symmetry attainability, invertibility, unitarity, a fast implementation or the parent construction.

No parent status change, score change, new canonical record, worldwide-priority claim or FFT speed claim is proposed. Both priorities remain 42. These two records contribute zero change to the 240-open/87-closed/327-view census. Completed bounded children should not be redispatched under the old generic comparison instructions.

## Coverage and source boundary

The current open-record index was inspected to select neglected owner records distinct from this round's ALG-036, ALG-042, ALG-052, ALG-048 and F020 work. This is **not** a new source/proof audit of all 240 open records. Actual archived mathematical review bodies, rather than only titles, were read for the two selected records. The live Catalogue, novelty and Research overview owner rows were read on 16 October 2026. Other inspected candidates were not finalized.

- M-NILPOTENT-FOLD: overview row 88; Catalogue row 41; `novelity breakthough` row 71. The full archived nilpotent-fold proof, including its exact grid, root, characteristic, bank, scalar and zero-scalar guards, was read.
- M-SYMMETRY: overview row 101; Catalogue row 45; `novelity breakthough` row 84. The full archived Phase15 proof, exact commutator spectra and occurrence-wise perturbation qualification were read. The separate Phase16 gauge/rook claims are preserved, not newly audited.

The public primary sources were read at theorem level. No archived or uploaded program was executed. The small control script in this packet is newly authored; its floating diagnostics are not substitutes for the proofs below.

## 1. M-NILPOTENT-FOLD

### 1.1 Inherited exact theorem and retained guards

The archived proof fixes b=2^ell, a=b or 2b, N=ab, the precise four-to-one grid sum Q, compatible primitive roots omega of order 4N and zeta=omega^4, and a splitting field whose characteristic does not divide 4N. It proves

    rank(Q F_(4N) − gamma F_N Q) = N

for every scalar gamma. At gamma nonzero, its selected representative columns give F_N(K−gamma I), where K strictly lowers the within-block binary valuation and is nilpotent. The determinant is det(F_N)(−gamma)^N. At gamma=0, Q F_(4N) has rank N by invertibility of the Fourier matrix; b=1 is explicitly included.

For the specified single active bank the discrepancy is b|J|. The archived product-defect expansion gives a layer-defect rank sum at least N−b|J|. A proper bank is essential. Neither genuine fiber mixing nor a changed bank inherits this discrepancy formula automatically. The source already gives an O(N) full-rank mask defect, so rank alone is not a superlinear work lower bound. None of these inherited claims is counted as a new discovery here.

### 1.2 Named primary comparison

Schweinsberg, *The operator equation AX−XB=C with normal A and B*, Pacific Journal of Mathematics 102 (1982), Theorem 1, printed pp.447–448, gives an equivalence between solvability of a Sylvester equation and a block-triangular similarity condition for normal operators on two complex Hilbert spaces. The full source theorem and proof were inspected: [publisher PDF](https://msp.org/pjm/1982/102-2/pjm-v102-n2-p14-s.pdf).

Map A=gamma F_N, B=F_(4N), X=Q and C=−D_gamma(Q). Over the complex specialization A and B are normal; the rectangular dimensions fit the two-space formulation. But X is already prescribed, so the equation is already satisfied by definition. The source conclusion gives no rank bound for C, no valuation-lowering selected minor, no proper-bank discrepancy and no charged evaluator. Its complex-Hilbert hypothesis also does not supply the original arbitrary splitting-field scope. Thus this theorem is a **qualified nonmatch to the complete fixed-fold theorem**, not evidence of either global novelty or global nonnovelty.

A separate exact elementary control prevents a tempting spectral shortcut. Let

    A=diag(1,2), B=diag(3,4), X=[[3,2],[2,1]].

The spectra are disjoint and X is invertible (det X=−1), but

    AX−XB=[[-6,−6],[-2,−2]]

has rank one. Consequently even disjoint spectra and full-rank X do not imply a full-rank Sylvester image. At the smallest allowed fold N=1, Q=(1,1,1,1) and gamma=2, D_gamma(Q)=(2,−2,−2,−2) has rank one despite the balancing case. These controls identify precisely why the layout-specific nilpotent argument cannot be replaced by a generic operator-equation statement.

### 1.3 New bounded continuation: low-rank fold changes

**Lemma F.** Retain every inherited field/root/layout hypothesis for the baseline Q. Let r be any nonnegative integer and Q'=Q+E any N-by-4N matrix with rank E<=r. Then

    rank(Q' F_(4N)−gamma F_N Q') >= max(0,N−2r)

for every nonzero gamma. At gamma=0 the stronger lower bound is max(0,N−r).

**Proof.** The difference from the baseline defect is E F_(4N)−gamma F_N E. Each term has rank at most r. Rank(A+B)>=rank A−rank B and the inherited rank-N theorem give the first bound. At gamma=0, only E F_(4N) occurs; equivalently rank(Q' F_(4N))=rank Q'>=N−r. This proof uses no complex norm and therefore retains the inherited splitting-field scope. Q' need not be a legal fold; the conclusion is an algebraic necessary condition only.

**Product corollary.** For the same three-layer/single-bank product topology, define each layer defect using Q' and nonzero layer scalars. If both total products equal nonzero scalar multiples of their compatible Fourier targets, and

    beta = rank(Q' B_large−B_small Q'),

the same telescoping expansion implies

    sum_l rank(D_l(Q')) >= max(0,N−2r−beta).

Here beta is the **actual changed-bank discrepancy**, not an automatically inherited b|J|. If the bank itself is unchanged from the archived theorem, rank subadditivity gives beta<=b|J|+2r, hence the weaker necessary bound max(0,N−b|J|−4r). There is no assertion of sharpness, legal coefficient realization, bank normalization invariance or operation complexity.

This is a completed bounded rank-robustness child. A low-rank change of the interface cannot be claimed to evade the obstruction without paying these terms. Arbitrary rank changes and genuine mixing/construction remain open.

## 2. M-SYMMETRY

### 2.1 Named primary comparison and exact relaxed problem

Li and Strang, *An elementary proof of Mirsky's low rank approximation theorem*, Electronic Journal of Linear Algebra 36 (2020), Theorem 1.1, pp.694–695, establishes truncated-SVD optimality under unitarily invariant norms. Its proof's inequality (2.1) is a singular-tail lower bound. The complete four-page primary paper was read: [journal PDF](https://journals.uwyo.edu/index.php/ela/article/download/5551/5179/7151).

This is an exact classical ingredient for the norm/low-rank step, already consistent with the archived proof's Eckart–Young attribution. It is not a prior printed theorem about Margulis Green realizability, the specific Fourier commutator spectra, shared occurrence counts or the full package. The following block completion explicitly solves the relaxed interface using that ingredient. No historical originality is claimed for the completion or its specialization.

**Theorem S.** Let Pi=Pi*=Pi^(-1) on a finite-dimensional complex space. In an orthonormal basis of its eigenspaces, write an arbitrary target M as

    M=[[A,B],[C,D]].

For a nonnegative integer k, allow arbitrary complex matrices T0 and E with [T0,Pi]=0 and rank(E)<=k. No unitary, invertibility, Green, conditioning, sparsity or cost constraint is placed on T0 or E. Let sigma_j of a block be zero beyond its singular-value list. Then the following are minima, not merely infima:

    min ||M−T0−E||_2 = max(sigma_(k+1)(B), sigma_(k+1)(C)),

    min ||M−T0−E||_F^2
      = sum_(j>k) sigma_j(B)^2 + sum_(j>k) sigma_j(C)^2.

The same pair T0,E attains both minima. Exact representation M=T0+E exists precisely when k>=max(rank B,rank C).

**Proof of lower bounds.** In this basis every commuting T0 is block diagonal. Each offdiagonal block of E has rank at most k. Rectangular compression cannot increase spectral norm, so Mirsky's spectral specialization applied independently to B and C gives the maximum lower bound. The squared Frobenius error is at least the sum of the squared offdiagonal errors; the two Frobenius specializations give the second lower bound. Exact representation requires the two offdiagonal ranks to be at most k.

**Proof of simultaneous attainment.** Choose truncated-SVD rank-k approximants B_k=L_B R_B and C_k=L_C R_C, padding both factorizations to inner dimension k with zeros if needed. Put

    E = [L_B; L_C] [R_C, R_B]
      = [[L_B R_C, B_k],[C_k,L_C R_B]].

Thus rank E<=k, even though both offdiagonal blocks have been approximated. Let T0 have diagonal blocks A−L_B R_C and D−L_C R_B and zero offdiagonal blocks. Then

    M−T0−E=[[0,B−B_k],[C−C_k,0]].

Its squared Frobenius norm is the sum of the two squared tail norms; its spectral norm is the maximum of the two tail norms (multiply by the adjoint to see block diagonality). Both lower bounds are attained. This also proves the zero threshold. For k=0 the empty factors mean E=0. Unequal eigenspace dimensions and zero singular values are included.

### 2.2 Guarded Fourier specialization

Use the archived complex unitary Fourier U=F_N/sqrt(N), with N=s^2 and even s, and one of the archived half-grid involutions Pi_x, Pi_y or Pi_xy. Their plus/minus eigenspaces both have dimension N/2. Write U in those two blocks.

The offdiagonal blocks B,C have the same singular-value multiset: from unitarity,

    B B*=I−A A*,   C* C=I−A* A,

and square A A* and A* A have the same eigenvalues including zeros. Also the commutator is, up to signs, [[0,2B],[−2C,0]]. The archived commutator multiplicities therefore split equally between B and C. This equal-block argument is necessary; the combined spectrum alone would not justify allocating multiplicities to each block.

Set h=N/4, c=cos(pi/8), d=sin(pi/8). Each B and C has:

- Pi_x: singular value 1 with multiplicity h, and 0 with multiplicity h.
- Pi_y or Pi_xy: singular value c with multiplicity h, and d with multiplicity h.

Thus the exact **relaxed** spectral minima are:

- Pi_x: 1 for 0<=k<h; 0 for k>=h.
- Pi_y/Pi_xy: c for 0<=k<h; d for h<=k<2h; 0 for k>=2h.

The exact relaxed relative squared Frobenius minima (divide by ||U||_F^2=N) are:

- Pi_x: max(1/2−2k/N,0).
- Pi_y/Pi_xy: (2/N)[c^2 max(h−k,0)+d^2 max(2h−max(k,h),0)].

For k=0 these reproduce the archived single-involution full-commutant values. For k>0 they establish attainability of the corresponding rank-budget floors in the larger unconstrained class. The exact zero thresholds are N/4 and N/2 respectively.

### 2.3 What this does not close

A legal occurrence-wise k-edit Green product is a subset of this relaxed class only after the archived invertible symmetric-reference/telescoping hypotheses establish rank(T−T0)<=k. The constructed low-rank E and its diagonal completion need not come from k allowed weight edits or any allowed Green network; T0 can be singular and dense. This packet proves no efficient factorization, no all-prefix conditioning, no bit-cost claim, no arbitrary-gauge norm invariance and no simultaneous-two-involution completion. In particular, the existing joint relative-Frobenius sqrt(3)/2 statement is preserved and not extended here to a positive-k joint optimum.

General symmetry-breaking weights/routes, a uniformly Fourier-compatible construction, and full-package historical priority stay open. Only the named classical norm comparison and the explicitly defined one-involution relaxation are finished.

## 3. Diagnostics and stopping condition

`verify_new_lemmas.py` is newly written mathematical control code. Its output records:

- 68 exact finite-field fold-perturbation cases over F_65537, including gamma=0, scalar balancing, and ranks r=0,1,2 where dimensions permit;
- the exact 2-by-2 Sylvester-rank counterexample;
- 142 generic complex block-completion cases including unequal eigenspace dimensions and k=0/zero-tail boundaries;
- 192 floating-point Fourier-specialization cases for s=2,4,6,8 and every k=0,...,N/2 for each of three involutions.

All passed. These are corroborating finite diagnostics; the algebraic proofs above are the universal evidence. No numerical run is labelled exact spectral certification. The source programs and historical large experiments were not rerun.

The bounded work stops here. Parents stay open; next dispatch needs a distinct primary theorem or a concrete legal construction/interface, not another repetition of these finished comparisons or relaxed calculations.

## Source links

- [Pinned nilpotent-fold proof](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/e9/e997688eac279b14aa64e64f7bc55998f778169d3e32e5f885aab60e07e319f3__e997688eac279b14aa64e64f7bc55998f778169d3e32e5f885aab60e07e319f3__INDEPENDENT_REVIEW.md)
- [Pinned Phase15 symmetry proof](https://github.com/AgentSlop-Si/research/blob/0339a31eb6109f0b96074ab8321f8653641e7530/math/archive/objects/9e/9e18319f9acd030444e2f72e1596e09393c3b18181af96ad3accb447b8b7aabf__REVIEW.md)
- [M-NILPOTENT-FOLD owner view](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A88:Q88)
- [M-SYMMETRY owner view](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011&range=A101:Q101)
