# The fixed Cooley-Tukey interface determines the exterior uniquely

9 October 2026. This is a bounded constructive-target analysis, not a coefficient search or an FFT speedup. No uploaded program was executed.

## 1. Result

Fix the bank B_J and the explicit Cooley-Tukey interface actions from `BANK_INTERFACE_TRANSPORT.md`. The two linear intertwining equations for P have a one-dimensional solution space. Their only calibrated solution is exactly

    P_0=(F_q tensor I_m) Delta B_(J complement).

There is no non-scalar simultaneous-centralizer freedom that can replace P_0 by a different, cheaper exterior operator while preserving those actions. A cheap paired-Green factorization of this same operator could still exist; uniqueness neither constructs nor rules out such a factorization. That is the remaining task. No generic numerical scan was performed.

## 2. Fixed data and exact linear system

Let N=mq, let omega have exact order N in a field of characteristic not dividing N, and use the positive unnormalized Fourier convention. Let B=B_J be the direct sum of F_m on active blocks and I_m elsewhere. Define the stride permutation

    (R_0 x)[rm+s]=x[r+qs],      0<=r<q, 0<=s<m.

Set V=B R_0. The fixed interface pair is

    A_1=V S_N V^-1,            A_2=V D_N V^-1.

The corresponding required output pair is Y_1=D_N, Y_2=S_N^-1. The exact system is

    P A_1-D_N P=0,
    P A_2-S_N^-1 P=0,
    ell(P):=(P V)[0,0]=1.                           (1)

This is an affine linear system in the N^2 entries of P. The A matrices are supplied by the bank-block formulas; for a contiguous proper active set in a square problem, they have only O(N) total nonzeros, including the two dense boundary blocks in A_1. Their sparse description does not alter the number of unknown entries of an unrestricted P.

In entry form, with all row indices modulo N, the first two equations are

    sum_k P[i,k] A_1[k,j] = omega^i P[i,j],
    sum_k P[i,k] A_2[k,j] = P[i+1,j].                (2)

Both equations use the same P. Satisfying only one generator leaves a substantial false degree of freedom.

## 3. Uniqueness without solving a dense system

Set Z=P V. Since V is invertible, this is an invertible linear change of the unknown matrix. Equations (1) become

    Z S_N=D_N Z,              Z D_N=S_N^-1 Z.

Their scalar recurrences are

    Z[i,j+1]=omega^i Z[i,j],
    Z[i+1,j]=omega^j Z[i,j].                        (3)

The first recurrence gives Z[i,j]=c_i omega^(ij). The second at j=0 gives c_(i+1)=c_i. Thus every solution is Z=c F_N and

    P=c F_N R_0^-1 B^-1=c P_0.

Calibration ell(P)=Z[0,0]=1 fixes c=1. No nonsingularity assumption on the unknown P is needed: the uncalibrated kernel includes c=0, and every nonzero solution is automatically invertible. Therefore the homogeneous linear map in (1) has rank exactly N^2-1, and adding the calibration gives full column rank N^2.

The first generator alone would permit P=diag(c_i) P_0. Its kernel has dimension N, not one. The second generator removes all nonconstant row scalings. This is why a one-generator displacement identity plus one scalar calibration is insufficient.

### Equivalent centralizer statement

If a matrix C commutes with both S_N and D_N, then D_N's distinct eigenvalues force C to be diagonal, and commutation with S_N makes that diagonal constant. Hence

    Cent(S_N,D_N)=K I,
    Cent(A_1,A_2)=V Cent(S_N,D_N) V^-1=K I,
    Cent(D_N,S_N^-1)=K I.

For any other intertwiner P, P_0^-1 P lies in Cent(A_1,A_2), giving the same scalar result. This argument holds over the stated splitting field; it does not require complex unitarity or an algebraically closed field.

## 4. The unique entries and their exact density

Write output i=mu+t, 0<=u<q, 0<=t<m, and bank input column j=rm+s. Put eta=omega^q and omega_q=omega^m. Directly expanding F_N R_0^-1 B^-1 gives

    P_0[mu+t,rm+s]
      =omega_q^(ur) omega^(rt) delta_(t,s),          r active;
      =omega_q^(ur) omega^(rt) eta^(ts),             r inactive.

On an active block the inverse Fourier sum is

    (1/m) sum_h eta^((t-s)h)=delta_(t,s),

so there is no missing scale factor. Every displayed root factor is nonzero. If j_A=|J|, then exactly

    nnz(P_0)=j_A*m*q+(q-j_A)*m*N
            =N[j_A+(q-j_A)m].                       (4)

Consequences:

- Full bank: nnz(P_0)=Nq. In a square split this is N^(3/2).
- A fixed proper active fraction theta=j_A/q: nnz(P_0)=theta*Nq+(1-theta)*N^2. A fixed inactive fraction therefore makes P_0 genuinely Theta(N^2)-dense.
- Empty bank: P_0=F_N R_0^-1 has N^2 nonzeros.

These are output-size bounds for explicitly materializing P_0, not arithmetic lower bounds for applying it implicitly. Dense Fourier matrices themselves have fast factorizations. The compact closed formula can be described using O(N) supplied-root tables, an active mask, and index rules, but this description alone is not an O(N) evaluator on fresh arbitrary data.

## 5. Honest construction and application costs

No generic dense linear solve is needed to recover P_0: equations (3) give its entries symbolically. If all nonzero matrix entries are requested, writing them takes Omega(nnz(P_0)) operations/words; consecutive-power recurrences attain O(nnz(P_0)+N) scalar preparation. A black-box elimination that returns a dense matrix must also pay its actual solve and output costs. The O(N) size of the input interface does not make such costs free.

The known implicit evaluator is exactly

    B_(J complement) -> Delta -> (F_q tensor I_m),

with cost

    (q-j_A) T(m)+m T(q)+O(N).                       (5)

Adding the active bank and the O(N) stride permutation gives qT(m)+mT(q)+O(N), ordinary Cooley-Tukey. Generating the O(1) dense mixed interface blocks separately costs O(m^2)=O(N) in a square split; these are certificate coefficients, not a replacement for the transforms in (5).

Q=R_0 is already a legal product of two paired-Green layers using zero masks and monomial endpoints. If one could additionally construct P_0=H_4H_3 with two legal paired-Green layers, uniformly generate all their coefficients/routes in O(N), and apply every guarded cyclic solve in O(N), then the exterior cost in (5) would genuinely fall to O(N). Such a result would be a new factorization of this same matrix. The uniqueness theorem leaves this possibility open and supplies no such factors.

## 6. Which gauges remain legitimate?

Three different notions must not be conflated.

### Fixed-interface operator gauge

Right multiplication P_0 C preserves both intertwining equations only when C commutes with A_1,A_2. This permits scalar C only. Calibration removes that scalar. The analogous left gauge is also scalar. There is no operator-level centralizer freedom left to exploit.

### Internal factorization gauge

For a proposed factorization P_0=H_4H_3, any invertible matrix G formally gives

    P_0=(H_4 G)(G^-1 H_3).

An arbitrary G need not preserve the allowed layer family. Every invertible monomial G does preserve it: absorb G into each right endpoint of H_4 and G^-1 into each left endpoint of H_3. This is a real parameter redundancy among factorizations of the same P_0, not a different exterior map or a cheaper evaluator by itself. For example, one may normalize one chosen left monomial endpoint of H_3 to I by selecting G equal to that endpoint, without changing P_0 or the Green denominator guards.

There is also a within-term diagonal representation gauge. For nonzero diagonal E,

    L U^-1 R=(L E)(E^-1 U E)^-1(E^-1 R).

The conjugated denominator retains its cycle support and changes only edge weights; its cycle-weight product and invertibility guard are unchanged. This removes representation redundancy, not Fourier work.

### Changing the interface

A non-scalar bank-coordinate change may produce different exterior operators only by changing the interface data or Q as well. For example, if C commutes with B, then P'=P_0 C^-1 and Q'=C R_0 preserve P' B Q'=F_N, but their interface pairs become C A_g C^-1 and C T_g C^-1. Holding the fixed CT pair and Q=R_0 does not allow this move. A genuinely different interface is a separate construction target with its own sparsity and cost obligations.

## 7. Reduced exact membership target

After fixing the CT interface and calibrating, the remaining problem is precisely

    [sum_(r=0,1) L_(4,r) U_(4,r)^-1 R_(4,r)]
    [sum_(r=0,1) L_(3,r) U_(3,r)^-1 R_(3,r)] = P_0,
    U_(l,r)=I-D_(w_(l,r)) P_(pi_(l,r)),
    1-product_i w_(l,r)[i] != 0,

with Hamiltonian pi, nonsingular monomial endpoints, and a paid uniform generator. Internal monomial and diagonal gauges may be normalized before a later structural construction. Solving the fixed linear intertwining equations alone cannot produce a second target operator: every calibrated solution is the P_0 already displayed.

No coefficient search is launched here. The useful next proof would either factor this explicit P_0 in the allowed family with a paid all-size generator, or establish a scoped obstruction that applies to it. An unsuccessful numerical fit, a dense solve, or the mere O(N) interface description would not accomplish either.

## Exact controls

`verify_exterior_uniqueness.py` is independently authored and uses only the Python standard library. It checks the fixed-interface equations, exact P_0 density, the full homogeneous rank N^2-1, calibrated rank N^2, and one-generator rank N^2-N over F_65537 at small sizes. `EXTERIOR_UNIQUENESS_CONTROLS.json` records the results. These controls corroborate the algebraic proof and do not assert the required paired-Green factorization.
