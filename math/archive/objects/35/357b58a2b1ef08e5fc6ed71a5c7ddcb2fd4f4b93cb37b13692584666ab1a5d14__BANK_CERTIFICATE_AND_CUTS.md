# Active-bank certificates and routing constraints

## Summary

The new target is the unproved identity

\[
F_N=H_4H_3\,\mathcal B_J\,H_2H_1,
\]

where each H is a sum of two independently ordered, weighted Hamiltonian Green resolvents with nonsingular monomial endpoints. The bank has q blocks of length m, N=mq, with F_m on active blocks J and identity elsewhere. We derive three exact necessary constraints:

1. The no-bank product determines a spectral projector whose rank is exactly the active recursive Fourier mass.
2. Every interface cut gives a weighted covering inequality on the active block set. A balanced bank cut with sublinear exterior leakage forces almost every block active, excluding a fixed-fraction mass saving within that routed subclass.
3. With diagonal or bank-block-preserving monomial endpoints, the eight cycle orders must supply linear rank across each bank boundary. Natural-cycle versions fail for dyadic N>=32, even if the entire bank is active.

These are architecture/certificate gates, not a proof against general independently ordered paired-Green layers. No contracting factorization or uniform parameter generator is supplied.

## Source and conventions

Read-only source: `new_material_2257/THEORY.md`, SHA-256 `4e2429adc4079d95e95df55f952190cc8221d67acf93339db5911a8d0a77ea9c`.

The source already proves the conditional recursive-mass recurrence, the bank-aware inverse-support bound, and the bank-aware inverse-defect bound. Those are inherited. The results below retain the active set, or impose phase-compatible bank invariants, rather than counting every bank row as dense by default. No publication-priority claim is made.

Use unnormalized F_n with entries omega_n^(ij), where omega_m=omega_N^q. Inactive bank blocks are exactly I_m. Assume m>=2 is dyadic, m<N, and all factors in an exact square Fourier product are invertible. Set

\[
P=H_4H_3,\quad Q=H_2H_1,\quad C_0=PQ,\quad a=m|J|.
\]

Here a is the active recursive Fourier mass, not a rank surrogate by definition. Over characteristic zero the ranks below prove equality with that mass. Monomial endpoints are already incorporated in P and Q; the first two theorems impose no endpoint restrictions.

## 1. The active selector is a spectral projector

### Theorem 1

If F_N=P B_J Q and K=C_0^{-1}F_N, then

\[
K=Q^{-1}\mathcal B_JQ.
\]

Consequently, whenever m^2-1 is nonzero in the field,

\[
\Pi=\frac{K^4-I}{m^2-1}
\]

is an idempotent of rank a, and

\[
(K-I)(I-\Pi)=0,
\quad (K-I)(K^4-m^2I)=0,
\quad \operatorname{rank}(F_N-C_0)=a.
\]

For even m in characteristic zero,

\[
\operatorname{tr}K^2=N+a,
\qquad \operatorname{tr}K^4=N+(m^2-1)a.
\]

In a field of positive characteristic these trace equalities are field equalities and cannot by themselves recover an integer rank after reduction.

### Proof

F_m^2=m J_m, where J_m e_j=e_{-j mod m}; hence F_m^4=m^2 I. The fourth power of B_J is I on every inactive block and m^2I on every active block. Conjugating its normalized difference from I proves the projector identity, its rank, and the complementary identity. If (F_m-I)v=0, taking fourth powers gives (m^2-1)v=0; thus F_m-I is invertible under the stated guard. Therefore B_J-I has rank a, as does F_N-C_0=P(B_J-I)Q. Finally J_m has two fixed points for even m, so tr(F_m^2)=2m. Sum over the active and inactive blocks to get tr(K^2)=N-a+2a=N+a. The fourth-power trace follows similarly. QED.

The projector conditions are necessary, not sufficient. In particular they do not enforce the exact multiplicities of the four Fourier eigenvalues or the prescribed block basis. A stronger necessary invariant retaining all multiplicities is the determinant pencil

\[
\det(F_N-zC_0)=\det(C_0)(1-z)^{N-a}\det(F_m-zI_m)^{|J|}.
\]

Even that pencil does not establish the required particular Q-conjugacy or admit P,Q to the paired-Green family.

### Exact negative control: scalar no-bank products cannot work

If C0=cI with c nonzero, K^4=N^2c^{-4}I is scalar. A mixed active/inactive bank would give two distinct eigenvalues 1 and m^2 for K^4, impossible. If every block is active, K^4=m^2I forces c^4=q^2. But tr(K^2)=2N c^{-2} must equal2N, forcing c^2=1 in characteristic zero; hence q^2=1, impossible for q>1. If no blocks are active, F_N=C0 would be scalar, also impossible for N>1. Thus no scalar no-bank product implements this one-bank identity at a proper dyadic block size.

This control does not require a Gauss-sum eigenvalue formula. It tests a genuinely necessary spectral condition missed by raw cut capacity. It is a narrow subclass result, not a general Green-product exclusion.

### Field and normalization caveats

If m^2=1 in the field, the displayed projector is undefined, and rank(F_m-I) may be smaller than m. A concrete exact example is m=4 over F5 with primitive root3: det(F4-I)=0. Without the guard the always-valid identity is rank(F_N-C0)=|J| rank(F_m-I). A normalized Fourier bank has different fourth powers and eigenvalue-one multiplicities; the theorem must not be transferred to that normalization unchanged.

## 2. Active-set-weighted interface cuts

### Theorem 2

Let I be output rows, J0 input columns, and let A,C be arbitrary subsets of bank output/input coordinates. Define

\[
r_P=\operatorname{rank}P[I,A^c],\qquad
r_Q=\operatorname{rank}Q[C^c,J_0].
\]

For bank block b, set A_b=A intersect block_b, C_b=C intersect block_b, and

\[
h_b=|A_b\cap C_b|,\quad
w_b=\min(|A_b|,|C_b|)-h_b.
\]

Then

\[
\operatorname{rank}(P\mathcal B_JQ)[I,J_0]
\le r_P+r_Q+\sum_b h_b+\sum_{b\in J}w_b. \tag{1}
\]

Thus if I consists of W consecutive natural Fourier rows and J0 is any W distinct columns,

\[
\sum_{b\in J}w_b\ge W-r_P-r_Q-\sum_bh_b. \tag{2}
\]

This is a family of linear covering inequalities for the active-block indicators. It allows rank or scalar-network upper bounds to be substituted for rP and rQ, preserving validity.

### Proof

Split the transfer matrix into three terms:

P[I,A] B[A,C] Q[C,J0],
P[I,A] B[A,Cc] Q[Cc,J0],
P[I,Ac] B[Ac,:] Q[:,J0].

The last two have ranks at most rQ and rP. The first has rank at most rank B[A,C]. The bank submatrix separates into independent block rectangles. An inactive block contributes exactly h_b. An active block contributes at most min(|A_b|,|C_b|), whether or not that particular Fourier subminor is nonsingular. This proves (1). The Fourier target block in (2) is Vandermonde and has full rank W. QED.

### Consequence for fixed-fraction savings

Since A_b union C_b has size at most m,

\[
0\le w_b\le m/2.
\]

Indeed, if |A_b|<=|C_b|, then w_b=|A_b minus C_b| and 2w_b<=|A_b union C_b|<=m. Therefore (2) yields

\[
a\ge2\left(W-r_P-r_Q-\sum_bh_b\right). \tag{3}
\]

For W=N/2 and disjoint interface sets A,C, this becomes

\[
a\ge N-2(r_P+r_Q).
\]

Hence an active fraction a<=theta N with theta<1 requires exterior leakage rP+rQ at least (1-theta)N/2 across every such balanced disjoint interface cut. A candidate with O(1) or o(N) leakage at one of these cuts cannot have a fixed-fraction inactive bank.

This conclusion does not exclude the full-bank rho=1 target and does not exclude layouts whose independently ordered Green terms produce linear interface ranks. It supplies a concrete necessary design property for the rho<1 target.

The coefficient m/2 is sharp for the bank itself: choose A_b and C_b to be opposite contiguous halves of each block. Each active F_m rectangle then has rank m/2, each inactive rectangle rank0. Routing these sets to two global halves gives transfer rank exactly a/2.

## 3. Bank-boundary expansion required of aligned endpoints

This theorem is a scoped restriction on cycle/endpoint choices, not on all monomial-ended candidates.

Suppose each Green term is L(I-D_w P_pi)^{-1}R, and its endpoint monomials L,R preserve every bank block. Diagonal endpoints are a special case. Let I_t be the first t bank blocks, with W=tm. Write e_pi(I_t) for the number of directed cycle edges entering I_t from its complement, ignoring possible zero weights.

For the Green matrix, the off-diagonal complementary-submatrix rank identity gives

rank[(I-D_w P_pi)^{-1}[I_t,I_t^c]]
 = rank[(I-D_w P_pi)[I_t,I_t^c]]
 <= e_pi(I_t).

The last sparse rectangle is a partial matching; with nonzero crossing weights its rank is exactly the edge count. The endpoint monomials preserve this rank because they preserve I_t. Ranks across a fixed complementary cut are subadditive under matrix products and sums. The bank itself has rank0 across this boundary. Therefore every Fourier candidate in this endpoint subclass must satisfy

\[
\sum_{\ell=1}^4\sum_{r=0}^1 e_{\pi_{\ell,r}}(I_t)
\ge\min(tm,N-tm),\qquad 1\le t<q. \tag{4}
\]

The target rank is full because I_t is a consecutive Fourier row prefix (or use the complementary consecutive row suffix when W>N/2).

If all eight cycles are the natural Hamiltonian cycle, each contributes one incoming edge, so N/2<=8 is necessary. Thus every dyadic N>=32 fails in this aligned-endpoint natural-cycle subclass, irrespective of which bank blocks are active. Reversing a natural cycle gives the same count.

There is also a quantitative long-range routing consequence. Give coordinate j its bank label floor(j/m). Summing (4) over t and using that a full cycle's entering-cut sum is one half its total absolute bank-label edge displacement gives, for even q,

\[
\sum_{\ell,r}\sum_{j=0}^{N-1}
|\operatorname{block}(\pi_{\ell,r}(j))-\operatorname{block}(j)|
\ge Nq/2.
\]

Across the eight cycles, the average edge must therefore span at least q/16 bank labels. Local cycle orders with sublinear bank-range cannot support the target under block-preserving endpoints. Arbitrary endpoint permutations may supply global routing themselves and lie outside this corollary.

## 4. Supplement to the inherited inverse-defect gate

Suppose H_i^{-1}=A_i+E_i with at most s_i nonzeros per row in A_i and rank(E_i)<=r_i. Put d=product s_i. Erase the bank and all inverse defects. The resulting inverse baseline has row support at most d. Telescoping the true inverse against it gives rank difference at most rank(B_J^{-1}-I)+sum r_i, which is at most a+sum r_i. The inherited Fourier-versus-row-sparse lemma therefore gives

\[
a+\sum_i r_i\ge\left\lfloor\frac{N}{d+1}\right\rfloor. \tag{5}
\]

This complements, rather than replaces, the source's inequality sum r_i>=floor(N/(1+md)), which retains the full bank in its sparse baseline. For sufficiently small active fraction, (5) can force a linear total inverse-defect rank rather than merely a square-root-scale defect. For general paired-Green sums, no small inverse-defect representation is assumed.

## 5. A complete bank-aware coefficient certificate

The spectral projector and cuts are rejection tests. To certify every Fourier entry, retain the source's Weyl shift/modulation certificate. With S e_j=e_{j+1}, D=diag(omega_N^j), set

\[
A=P^{-1}DP,\qquad T=QSQ^{-1}.
\]

Then the full identity is equivalent to

\[
A\mathcal B_J=\mathcal B_JT,
\qquad P\mathcal B_JQe_0=\mathbf1.
\]

In bank blocks, these are A_bc B_c=B_b T_bc. When both blocks are inactive they require A_bc=T_bc; mixed blocks require the appropriate single Fourier multiplication; active-active blocks require two-sided intertwining. The seed must remain: the covariance alone permits row-scaled Fourier outputs.

Equivalently, with E=P^{-1}F_NQ^{-1}-I, all off-block rectangles must vanish, and every diagonal block must be alpha_b(F_m-I), where alpha_b is 0 or1. Over characteristic zero, the invertibility of F_m-I makes this block label unambiguous. Enforce sum alpha_b<=theta q as the active budget. The blocks and their coefficients cannot be chosen independently of P and Q.

For each paired-Green term, enforce its sparse defining equation (I-D_w P_pi)Z=R and use LZ as its matrix. Guard 1-product w!=0. If dense variables or inverses are used in a search/certificate, their cost is part of verification/preparation; they are not a proposed O(N) coefficient generator. Fixed finite certificates do not supply an all-N parameter recursion.

## 6. Exact controls and next question

`check_bank_constraints.py` is newly authored. It constructs16 independently ordered paired-Green layers over F65537, with zero weights retained, and56 banked products across N4,8,16,32. It verifies the similarity, idempotent, exact rank, complement, trace and erasure identities;144 determinant-pencil evaluations;448 weighted separator bounds;22 sharp opposite-half bank cuts; and15 Weyl/erasure controls. In those last15 controls P is deliberately solved as a dense abstract matrix to force the Fourier target: they are algebra controls, not claimed paired-Green factorizations. The F5 singular-erasure example checks the field warning. Results are in `BANK_CONSTRAINT_RESULTS.json`.

The next constructive question is now explicit: can one give uniform independently ordered paired-Green P,Q whose no-bank product has the required bank spectral pencil, while their full block-intertwining equations and seed hold, and whose interface leakage is linear where a fixed inactive fraction demands it? A proposed size-lifting rule should preserve these equations and the active budget simultaneously. Passing only the projector or only the cut inequalities is insufficient.
