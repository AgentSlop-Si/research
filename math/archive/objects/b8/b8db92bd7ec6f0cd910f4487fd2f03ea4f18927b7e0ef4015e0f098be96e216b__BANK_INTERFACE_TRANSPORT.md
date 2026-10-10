# Fourier-bank interface transport: exact equations, a degree obstruction, and controls

9 October 2026. Independently derived. No uploaded code was executed. No new Fourier speedup, uniform paired-Green factorization, or novelty claim is made.

## 1. Contract and result

Let N=mq over a field K containing a primitive N-th root omega, with characteristic not dividing N. Put eta=omega^q and use the unnormalized positive-sign Fourier matrices F_n[i,j]=omega_n^(ij). Let S_n e_j=e_(j+1 mod n) and D_n=diag(omega_n^j). There are q consecutive bank blocks of length m, and B=B_J has F_m on blocks in J and I_m elsewhere. Assume

    F_N = P B Q,       P=H_4 H_3,       Q=H_2 H_1,

where every H_l is a sum of two monomial-ended Hamiltonian Green terms. Exact equality makes P,Q invertible. We derive necessary conditions, not their existence.

Main results:

1. Active-active blocks with bounded Weyl descriptions and bounded block routing remain uniformly sparse across the bank. Inactive-inactive blocks are unchanged. Mixed blocks require genuine one-sided Fourier equations.
2. If both actual interface generator pairs have maximum row degree at most d and m>d^2, then a proper nonempty active bank is impossible; column degree alone gives the same exclusion. Bounding both row and column degree additionally makes every mixed block vanish. Total O(N) nonzeros does not imply any of these degree premises.
3. A 14-wire state lift identifies every extra one-sided Fourier equation introduced by off-wire state transport. Its general witnesses cannot be identified with the actual interface actions.
4. A fully explicit Cooley-Tukey control realizes every active set with arbitrary exterior matrices. For a square problem and a contiguous proper active set, all four actual interface actions have O(N) nonzeros, although one has degree m. The inactive transforms are paid for inside P, and P is not claimed to have the required paired-Green form.

## 2. Complete actual-interface equations

For the two generator pairs

    (X_1,Y_1)=(S_N,D_N),       (X_2,Y_2)=(D_N,S_N^-1),

define

    T_g=Q X_g Q^-1,           A_g=P^-1 Y_g P.

Then F_N=P B Q is equivalent to both equations

    A_g B = B T_g,            g=1,2,

together with the single scalar calibration (P B Q)[0,0]=1. Indeed, the first covariance forces the transfer to be diag(c_i) F_N; the second makes every c_i equal. Without calibration the zero transfer also satisfies the two homogeneous covariances. Alternatively, the first covariance plus the full seed P B Q e_0=1 suffices.

For each bank row block b and column block c, suppressing g, the exact equations are

    b inactive, c inactive:  A_bc = T_bc;
    b active,   c active:    A_bc = F_m T_bc F_m^-1;
    b active,   c inactive:  A_bc = F_m T_bc;
    b inactive, c active:    A_bc F_m = T_bc.

The last two equations are the mixed-bank conditions. The active-active formula is not a license to conjugate an arbitrary sparse block cheaply.

For W(a,b)=D_m^a S_m^b, exponents modulo m,

    F_m W(a,b) F_m^-1 = eta^(ab) D_m^b S_m^(-a).

Thus a block expressed as a sum of at most k Weyl monomials has at most k entries per row and column both before and after an active-active crossing. If the q-by-q block support has at most r blocks in each block row and column, and r,k are uniform constants, the active-active/inactive-inactive portion has degree at most rk and O(rkN) nonzeros. More generally O(q) such nonzero blocks gives O(kN) total nonzeros but does not by itself bound maximum degree. Allowing all q^2 block positions would instead cost O(kNq). A one-sided Fourier product of a single nonzero Weyl monomial is dense, with m^2 nonzeros.

All displayed sparsity claims concern explicitly supplied coefficients. They do not construct the required P,Q or transport coefficients.

## 3. Algebraic support-product uncertainty

For every nonzero vector x in K^m,

    |supp x| * |supp(F_m x)| >= m.                 (1)

Here no complex norm argument is needed. Let C_x be the circulant whose columns are the m translates of x. Every row is nonzero, and each column has s=|supp x| nonzeros. A basis of r=rank(C_x) columns must cover all m rows: a row missing from every basis column would vanish in every column. Therefore rs>=m. Fourier diagonalization of C_x gives r=|supp(F_m x)|, since m is invertible and eta has exact order m. The same result applies to row vectors and to F_m^-1, whose normalization and index reversal do not change supports.

### Theorem: proper-bank obstruction for bounded-degree actual actions

Suppose 0<|J|<q and all four matrices A_1,T_1,A_2,T_2 have maximum row degree at most d. Then m<=d^2 is necessary. The same conclusion holds if all four instead have maximum column degree at most d.

Proof under row bounds. If b is inactive and c active, apply the row version of (1) to A_bc F_m=T_bc. Both row support sizes are at most d, forcing A_bc=T_bc=0 when m>d^2. This one direction of zero blocks already makes the direct sum V_J of active bank coordinates a proper nonzero common invariant subspace for T_1=Q S_N Q^-1 and T_2=Q D_N Q^-1. This is impossible: D_N has N distinct eigenvalues, so polynomial spectral projections extract a coordinate vector from any nonzero invariant subspace, and powers of S_N then produce every coordinate vector.

Under column bounds, if b is active and c inactive, apply (1) to each nonzero column of T_bc in A_bc=F_m T_bc. Both column supports are at most d, forcing these opposite mixed blocks zero. The inactive coordinate subspace is then a proper nonzero common invariant subspace, giving the same contradiction. If both row and column bounds hold, both directions vanish. QED.

Separate directional bounds sharpen the premise. Either of the following, holding for each g, is enough for the exclusion:

    (maximum column degree of A_g)*(maximum column degree of T_g) < m,
    (maximum row degree of A_g)*(maximum row degree of T_g) < m

Block-specific support bounds suffice as well. Row degree alone does not control left Fourier multiplication and cannot force that direction of mixed blocks to vanish, but it already gives the contradiction through the opposite direction. The analogous warning applies to column degree and right multiplication.

This is a restriction on the actual actions P^-1Y_gP and QX_gQ^-1. It does not rule out a full bank, growing degrees, merely O(N) total nonzeros, or a larger sparse state certificate with off-wire transport. Section 6 gives an exact counterexample to conflating total sparsity with degree.

## 4. Sparse exterior realization with the bank exposed

Write each paired layer as

    H_l = L_(l,0) U_(l,0)^-1 R_(l,0)
          + L_(l,1) U_(l,1)^-1 R_(l,1),
    U_(l,r)=I-D_(w_(l,r)) P_(pi_(l,r)).

The L and R endpoints are nonsingular monomials; pi is Hamiltonian; require 1-product_j w_(l,r)[j] != 0. Each U and endpoint has bounded row and column degree. A Hamiltonian cyclic solve costs O(N), including its scalar closure computation; a fixed four-layer exterior costs O(N) after its masks and routes have been supplied.

Use the following 14 N-dimensional state wires:

    x, y_10, y_11, z_1, y_20, y_21, z_2,
    w_2, y_30, y_31, z_3, y_40, y_41, z_4.

Set z_0=x. For stages 1,2 use input z_(l-1); for stage 3 use w_2; for stage 4 use z_3. The equations are

    x=x_in;
    U_(l,r) y_(l,r) - R_(l,r) input_l=0;
    z_l - L_(l,0)y_(l,0)-L_(l,1)y_(l,1)=0;
    w_2-B z_2=0.

Let K be this lower-triangular block system, B_0 inject the input equation, and C select z_4. Then C K^-1 B_0=P B Q. K is invertible even if a paired sum is singular, because its diagonal blocks are I or guarded U. Let z denote the bank-input wire z_2 and w the bank-output equation/state wire w_2. Put

    K = K_s - E_w B E_z^T,

where E_a injects a state wire. K_s has maximum row and column degree at most 3. Its w-th block row contains only I in column w, and its z-th block column contains only I in row z. The only potentially dense block of K is the exposed bank coupling.

For each (X_g,Y_g), a state certificate consists of matrices S_g,R_g satisfying

    K S_g=R_g K,       R_g B_0=B_0 X_g,       C S_g=Y_g C.

These imply the transfer covariance. Two pairs and one scalar calibration certify every Fourier coefficient. Solving for dense S_g,R_g would be a verification/preparation cost, not a linear-time construction.

## 5. The missing off-wire equations

Suppress g and define the sparse product difference

    C_ab=(K_s S-R K_s)_ab.

The state identity is exactly

    C_ab = 1_(a=w) B S_zb - 1_(b=z) R_aw B.        (2)

Consequently all four cases must be checked:

    a != w, b != z:   C_ab=0;
    a = w,  b != z:   C_wb=B S_zb;
    a != w, b = z:    C_az=-R_aw B;
    a = w,  b = z:    R_ww B-B S_zz=R_wz-S_wz.     (3)

The last line uses C_wz=S_wz-R_wz. For a bank row block h, the second line reads (C_wb)_(h,:)=B_h(S_zb)_(h,:); it is one-sided F_m multiplication on active rows. For a bank column block k, the third reads (C_az)_(:,k)=-(R_aw)_(:,k)B_k; it is one-sided F_m multiplication on active columns. These equations do not become two-sided Weyl conjugations merely because h or k is active.

Even the central equation has a sparse forcing term E=R_wz-S_wz. Its bank blocks satisfy

    inactive/inactive: R_ww,hk-S_zz,hk=E_hk;
    active/active:     R_ww,hk F_m-F_m S_zz,hk=E_hk;
    active/inactive:   R_ww,hk-F_m S_zz,hk=E_hk;
    inactive/active:   R_ww,hk F_m-S_zz,hk=E_hk.

Therefore identifying R_ww,S_zz with A,T without proving away off-wire terms is invalid. The actual actions from Section 2 always exist, but can be dense even when a bigger state witness is sparse.

### Optional exact pruning for bounded-degree state witnesses

Suppose S,R have maximum row and column degree d. The incident off-wire differences C_wb and C_az have degree at most 4d: the special row/column of K_s gives one degree-d term plus a product of degrees d and 3. Applying (1) to the one-sided equations shows that, if m>4d^2,

    Pi_J S_zb=0 for every b != z,
    R_aw Pi_J=0 for every a != w,                  (4)

where Pi_J selects the active bank coordinates. Thus sparse state transport can enter or leave those bank wires off-diagonally only through inactive coordinates. This is a useful restriction, not a proper-bank impossibility proof. It bounds the active rows of the actual T and active columns of the actual A, rather than all rows and columns needed by Section 3.

More explicitly, write V=K^-1 B_0 and U=C K^-1. The state equations give S V=V X and U R=Y U. Since V_z=Q and U_w=P, the pruned off-wire blocks imply

    Pi_J S_zz=Pi_J T,             R_ww Pi_J=A Pi_J.

These equalities show exactly which parts inherit degree d. Neither supplies all four uniformly row-sparse actions or all four uniformly column-sparse actions, so neither satisfies the degree obstruction's premise.

For a full bank (4) removes all such incident mixing. On the solution subspace, S_zz=QXQ^-1; on the dual output map, R_ww=P^-1YP. The central forcing then vanishes by the actual bank identity. This reduction still does not prohibit the full-bank target, whose active-active transports can be sparse.

Sparse multiplication checks involving K_s cost O(Nd) arithmetic/storage with sparse accumulators. Equations (2)-(3) involving B are not automatically O(N)-verifiable. One must provide explicit Weyl identities, support-based pruning, or another paid method. Computing general active Fourier products or dense witness solves cannot be hidden inside the claimed certificate cost.

## 6. Exact Cooley-Tukey positive control for every active set

Let raw input index j=r+q s, with 0<=r<q, 0<=s<m. Define the stride permutation R_0 by

    (R_0 x)[rm+s]=x[r+q s].

On bank-output coordinates (r,t), let Delta[rm+t]=omega^(rt). Write B_all=I_q tensor F_m and let B_(J complement) apply F_m precisely to inactive blocks of B_J. The ordinary Cooley-Tukey identity is

    F_N=(F_q tensor I_m) Delta B_all R_0.

Since the two complementary banks commute and multiply to B_all, set

    Q=R_0,
    P=(F_q tensor I_m) Delta B_(J complement).

Then F_N=P B_J Q exactly for every J, including empty, full, and proper mixed banks. Proof by entries, with output k=t+mu:

    (F_N x)[t+mu]
      =sum_r omega^(rt) omega_q^(ru)
          sum_s eta^(st) x[r+qs].

There is no dense solve in this control, but P is an arbitrary known FFT composition, not a certified product of two paired-Green layers.

The monomial Q=R_0 itself is already inside the allowed two-layer family when zero edge masks are permitted. For the dyadic contract, characteristic is not 2: set H_1=(1/2)R_0+(1/2)R_0 and H_2=(1/2)I+(1/2)I, using U=I from zero masks and nonsingular monomial endpoints in every summand. Any Hamiltonian orders may be supplied and their denominator guards equal 1. Thus the unresolved synthesis in this particular control is specifically the two-layer P; Q contains no hidden Fourier work. Over another field, use coefficients lambda and 1-lambda with both nonzero instead of 1/2 whenever necessary.

The interface actions are explicit. T_1=R_0 S_N R_0^-1 has one nonzero block on each edge c -> c+1 mod q: I_m except on the wrap edge q-1 -> 0, which carries S_m. T_2 is block diagonal, with block omega^r D_m. Both are monomial. Since A_g=B_J T_g B_J^-1:

- A_2 has block omega^r S_m^-1 on active blocks and omega^r D_m on inactive blocks, so it too is monomial.
- A_1 is monomial on equal-status bank edges. Every status-changing edge is a dense, invertible m-by-m block: F_m or F_m^-1, with a monomial factor on the wrap edge.

Let k be the number of status changes around the q-cycle. Then exactly

    nnz(A_1)=N+k m(m-1).

For a proper nonempty contiguous cyclic interval J, k=2. If q=m, then nnz(A_1)=3N-2m=O(N), but its maximum row and column degree is m. All four actual interface matrices therefore have O(N) nonzeros. This exact control disproves any attempted version of Section 3 based solely on total O(N) sparsity.

### Fully charged cost

Let T(n) be the chosen arithmetic cost of an n-point Fourier transform. Applying P, B_J, Q costs

    |J| T(m) + (q-|J|) T(m) + m T(q) + O(N)
      = q T(m)+m T(q)+O(N).

The apparently removed active mass is paid in P. For q=m this is 2m T(m)+O(N), ordinary square Cooley-Tukey. Roots and twiddles are prepared by consecutive-power recurrences in O(N) supplied-root arithmetic; index routing costs O(N). Storing the dense mixed interface blocks costs O(km^2), which is O(N) in the square two-boundary example. Generating an arbitrary dense P or its inverse would have to be charged separately; it is unnecessary for this symbolic control and is not advertised as the constructive target.

The control confirms that full-bank rho=1 and proper mixed banks are algebraically possible with wider exteriors. It supplies no qualifying paired-Green P,Q and no complexity improvement.

## 7. A surviving linear-size boundary-transport target

For m^2=O(N), allow O(1) exceptional dense m-by-m mixed-bank blocks, together with O(q) ordinary bounded-Weyl blocks. This has O(N) total coefficients and avoids the degree obstruction. A concrete certificate ansatz is:

- Choose a bank-block support graph of O(q) edges, bounded ordinary block degree, and an exceptional mixed-edge set E of constant size.
- On each ordinary equal-status edge choose at most k=O(1) Weyl coefficients. Set the opposite action by equality on inactive/inactive edges and by the Weyl conjugation rule on active/active edges.
- On an active-row/inactive-column exceptional edge choose T_bc as a sum of at most k Weyl monomials and generate A_bc=F_m T_bc explicitly. On an inactive-row/active-column edge likewise choose T_bc as a bounded Weyl sum and generate A_bc=T_bc F_m^-1 explicitly. The alternative orientation, choosing a bounded-Weyl A_bc and generating T_bc=A_bc F_m, is also legal if desired. Zero blocks elsewhere are part of the specification.

Each exceptional dense block can be generated entrywise in O(km^2) supplied-root arithmetic, without running an m-point transform on fresh data: Fourier entries and monomial row/column modifications are produced by consecutive-power recurrences. The total exceptional coefficient preparation, storage, and application costs O(|E|km^2)=O(N). These costs must be counted, even though they fit the linear budget. The Cooley-Tukey example has exactly this form with two exceptional edges for generator 1 and none for generator 2.

Passing the bank equations does not prove compatibility with either exterior. The remaining exact coefficient equations are

    (H_4 H_3) A_g = Y_g (H_4 H_3),
    T_g (H_2 H_1) = (H_2 H_1) X_g,        g=1,2,
    [(H_4 H_3) B_J (H_2 H_1)][0,0]=1,   (5)

together with every Green denominator guard, monomial endpoint requirement, chosen active-set budget, and the parameter definitions just given. Both g must use the same four layers. The first two lines make these A_g,T_g the actual interface actions because the exteriors are invertible. A candidate may instead prove the complete state equations (2)-(3), but cannot silently replace (5) with merely matching commutators, passing cut tests, or selecting independent Weyl blocks.

To avoid expanding the dense Green matrices, realize Q and P separately by their seven-wire sparse two-layer systems K_Q,K_P. For Q seek state transport satisfying K_Q S_Qg=R_Qg K_Q, R_Qg B_Q=B_Q X_g, C_Q S_Qg=T_g C_Q. For P use K_P S_Pg=R_Pg K_P, R_Pg B_P=B_P A_g, C_P S_Pg=Y_g C_P. These are sufficient exterior coefficient equations with the bank already certified. They do not establish that linear-size witnesses exist. A sparse K and a transport with O(N) total nonzeros can be multiplied in O(N) operations because K has bounded degree in both directions; direct-index sparse accumulation and comparison checks the identities without a hidden dense Green solve. Every witness entry and its generation still have to be charged.

Arbitrary dense active-active exception blocks would require their own paid conjugation verification, potentially O(m^3) by direct products or O(m^2 log m) by ordinary Fourier transforms. The mixed-only exceptional ansatz above avoids advertising that extra work as free. The unresolved construction is precisely to realize the resulting two exterior transport pairs using the allowed cheap Green layers, rather than the FFT-containing Cooley-Tukey exterior.

## 8. Remaining constructive gate

A qualifying result must still generate all four paired-Green layers and routes uniformly, satisfy both actual interface identities and calibration (or all state equations), keep every denominator legal, and charge coefficient synthesis, witness generation, Fourier banks, and application. Full-bank rho=1 remains a candidate. A proper-bank proposal with bounded-degree actual interfaces is excluded when m grows past d^2; a proposal with O(N) aggregate sparsity or off-wire state transport needs the finer checks above.

This work does not reopen the separately excluded balanced/complement two-stage identity-middle-grid architecture. It moves its useful sparse-state certificate idea to a different, explicitly banked target while retaining the missing equations.

## Reproducibility

`verify_bank_interface.py` is newly authored, uses only Python's standard library, and executes no uploaded file. `BANK_INTERFACE_CONTROLS.json` records exact finite-field Fourier/Weyl and Cooley-Tukey controls, all bank cases, degree counts, and explicit small-field support-product checks. The all-size results are proved above; the finite controls corroborate signs, normalization, and scope rather than proving asymptotic existence.

The run passes 344 Weyl conjugation checks; 84 Cooley-Tukey bank controls over eight (m,q) pairs; 1,167 nonzero-vector support/rank controls (including all vectors over F_5 at m=4 and over F_17 at m=2); four paired directional-support examples; and the 14-wire realization and exact residual decomposition at N=4,8. The latter state controls use separately generated legal paired-Green layers and make no claim that their arbitrary transfer is Fourier.
