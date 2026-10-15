# C02: current accepted scope and exact attribution target

15 October 2026 UTC. No external write; no theorem-status, discovery-count or p^d-route change.

## Correct current scope

The accepted equality in the live table is for every finite abelian 2-group, in characteristic zero: the minimum over independent row/column permutations of the maximum strict upper/lower corner rank is N/4+1 for N>=8, with bases 0,1,1 for N=1,2,4. It is no longer only a cyclic-dyadic theorem. Q05::noncyclic-minimax is already complete.

The all-group matching upper and common cut profile are already attributed to the dual subgroup-flag construction in Delvaux–Van Barel TW477 Lemma 12. N=8 lower is already classical through Corollary 21. These deductions should receive no independent ordering or N=8 novelty credit. The manuscript and bounded TW477 scalar-shortening/generalized-weight comparison are already internally accepted; neither needs to be rerun as a generic open task.

Fresh primary reading confirmed that Lemma 12 supplies simultaneous rank-one grids from a subgroup flag and its annihilator flag, while Corollary 21 makes the one-vector Hamming profile depend only on total group order. These checks validate the specific recorded attribution objects, not a new replay of the later all-group upper proof. [TW477 primary report](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW477.pdf), printed p.11 and pp.17–18.

The 2007 final-journal version was not newly inspected here. That bibliographic distinction is not a reason to reopen the already completed TW477 comparison or claim its formulas unverified.

## Precise residual historical-attribution lemma

Let G be a finite abelian 2-group, |G|=N=4L>=16. Let U_G be its normalized complex character table and E_I the coordinate subspace supported on I. Set C_I=U_G E_I, a length-N complex linear code of dimension |I|. For a code C, d_k(C) is the minimum size of the union of supports of a k-dimensional subspace of C.

The remaining prior-implication target is:

(A) For every I subset G with |I|=2L+1, d_(L+1)(C_I)>=2L+2.

Equivalently, after exchanging group and dual:

(B) For every J with |J|=2L-1, d_(L-1)(C_J)>=2L.

These are attribution targets, not unsolved claims within the project. A parameter-complete earlier theorem and a checked implication of A or B would settle the named predecessor question. A failed keyword search or scalar test cannot settle historical priority.

### Fresh derivation of the equivalence

For |I|=2L+1 and a tested output set R of size 2L-1,

rank U_G[R,I] = |I|-dim(C_I intersect E_(R^c)).

Thus rank>=L+1 for every such rectangle is exactly the assertion that no (L+1)-dimensional subspace of C_I fits inside any set of size 2L+1, which is A. A support of smaller size can always be enlarged, so the equivalence includes all supports below that threshold.

Transpose the universal rectangle statement and exchange group with dual. Its column set J now has size 2L-1 and its row set has size 2L+1. Rank>=L+1 is equivalent to the supported kernel dimension being at most L-2. Its complementary output support has size 2L-1, yielding B. This uses rank-nullity and Fourier transposition, not an unproved equivalence between independent theorem families.

### Why the completed scalar comparison is not this target

The one-vector profile gives d_1(C_I)>=2 when |I|=2L+1, and d_1(C_J)>=4 when |J|=2L-1. Strict increase alone therefore gives d_(L+1)(C_I)>=L+2 and d_(L-1)(C_J)>=L+2. For L>=4 neither reaches the target. At L=2, B is already d_1(C_J)>=4, explaining the classical order-eight case.

Likewise the ordinary flat-unitary trace-rank bound gives only rank>=ceil((2L-1)(2L+1)/(4L))=L. The accepted moment proof supplies the extra one. This explains the current remaining gate without claiming that the entire older literature cannot imply it.

## Accepted lower theorem rederived, not newly discovered

Write R size 2L-1, H size 2L+1, I=R^c, h=2L+1, V=U[R,H], A=U[I,H]*U[I,H]=I_h-V*V. Its eigenvalues are in [0,1]. For c_H(s)=|H intersect(H-s)| and f_I(s)=sum_(chi in I)chi(s),

tr(A^2)=N^(-2) sum_s c_H(s)|f_I(s)|^2.

Every nonidentity translation of a 2-group has even-order orbits; an odd set H cannot be invariant. Hence c_H(s)<=h-1 for s!=0. Orthogonality gives sum_s |f_I(s)|^2=N h and f_I(0)=h. It follows that

tr(A^2)<L+1,

more exactly tr(A^2)<=L+3/4+1/(4L)+1/(16L^2), which is less than L+1 for L>=2. The multiplicity of eigenvalue one is at most floor(tr(A^2))<=L. Therefore rank(V)=h-dim eig_1(A)>=L+1. This is the already accepted fourth-moment/complementary-Gram argument; it resolves correctness at this scope but cannot by itself resolve attribution.

## Table/editorial reconciliation that is actually justified

- Preserve C02, Q05 and TH-05 mathematical acceptance and OPEN universal-lower attribution. Do not convert this to overall CLOSED.
- Preserve the bounded TW477 comparison COMPLETE and its recorded completed-stage priority 15; parent attribution stays at its existing 52. These scores measure remaining work, not novelty probabilities.
- NEW-05 shares this comparison dependency only. Its general asymmetric finite-abelian deficit theorem must not be replaced by this 2-group critical-rectangle formulation.
- Prior work D5 and Source comparisons D4 have stale standalone text saying no matching upper for all noncyclic 2-groups. A dated addendum should supersede only that sentence, preserving the historical source comparison and all other limits.
- The publication-value assessment's sentence treating noncyclic attainment as optional uncompleted work is stale. Its remaining-value assessment can stand, but the current next step is the exact A/B predecessor implication, not another generic Kronecker or upper-ordering comparison.

The original later universal candidate/review bytes were not newly recovered here. Its accepted source bindings are retained from the live table; the fresh derivation above checks the lower argument only. No finite-field universal lower, optimal all-size rank sum, sharp approximation result, unrestricted arithmetic lower bound or worldwide firstness follows.
