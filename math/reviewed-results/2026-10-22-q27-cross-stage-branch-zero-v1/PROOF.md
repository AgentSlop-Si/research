# Q27: both branch-zero phases and one additional edge in each stage

Candidate, 22 October 2026. Independent review is pending. This is a finite,
family-specific exclusion, not an FFT construction, owner closure or novelty
claim.

## 1. Exact source, model and selected unresolved family

Use the original N=8 chart in `sources/CHART.json`, SHA-256
`5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98`.
The same 3,138 bytes were fetched from AgentSlop-Si/research at commit
`3834be7716370cfddf84ab1200da62b7887feb05`, path
`math/finalized/2026-10-19-q27-four-phase-same-branch/candidate/sources/CHART.json`.
They are also the chart of the accepted 20 October whole-branch packet.

Stages are indexed t=0,1 (historical S1,S2). Branches b=0,1,2 have exactly
the ordered cycles in the chart. Local edge 8b+j sends cycle[j-1] to cycle[j],
with j modulo 8. Local edges 0,...,6 have fixed gain 1. Local edges 7,...,23
have the listed gains (a+ib)/(a-ib). These are nonzero, norm-one Gaussian
rationals. All 34 original pairs, 14 fixed tree edges, seeds 42420/42520,
six cycles, stage sum coefficients (1,1,1), and product order are preserved.
For each branch, W_tb is its weighted cycle, G_tb=(I-W_tb)^(-1),
S_t=sum_b G_tb, and M=S_1 S_0. No interstage diagonal or branch weights are
introduced. The inverse domain is exactly the six original conditions
1-product(edge gains in branch tb) != 0.

Choose e0,e1 independently in {8,...,23}. Multiply exactly the four gains
at encoded coordinates [7,e0,31,24+e1] by x0,x1,x2,x3 respectively. Encoded
coordinate is 24t+local edge. All four xj are arbitrary complex unit phases;
all other original gains are frozen. Thus both stages move their sole free
branch-zero gain, and each stage also moves one arbitrary free edge of branch
1 or 2. There are exactly 16*16=256 labels, four phase variables per label.

Candidate theorem: For every one of these 256 labels, no point in its original
six-guard unit-phase domain is externally invertible-complex row/column
monomial-equivalent to the 8-by-8 Fourier matrix. Here arbitrary invertible
diagonal rescalings and arbitrary row/column permutations are permitted.
The Fourier normalization is irrelevant to this equivalence.

This family is not covered by the accepted 5,984 three-coordinate slices or
the four accepted whole one-free-branch families. All four moving coordinates
may move simultaneously, across four branches and both stages, and two are
branch-zero coordinates. It is the complete smallest-coordinate family with
both branch-zero phases and an additional moving branch in each stage, not a
single selected placement. It does NOT settle all branch-zero motions, all
four-coordinate placements, simultaneous motions with more coordinates, other
witnesses, or the full 34-phase fiber. The recorded Q27 owner remains open at
priority 50. Earlier accepted exclusions are not reproved or replaced.

## 2. Division-free original equations

Work over K=Q(i). Let h_tb be each frozen original branch holonomy. It is
nonzero, has norm one, and is not 1. At each stage exactly two branches move,
each in one variable. Put m_tb=xj for its one moving variable, or 1 for the
inactive branch, and define

  d_tb=1-h_tb m_tb, B_tb=I+W_tb+...+W_tb^7,
  D_t=product_b d_tb,
  A_t=sum_b B_tb product_(c!=b) d_tc,
  Delta=D_1 D_0, N=A_1 A_0.

The identity W_tb^8=h_tb m_tb I gives N=Delta M on the six-guard domain.
Every path in B has length at most 7 and uses each edge at most once. Other
branch guards involve disjoint variables, and the two stages use disjoint
variables. Consequently every entry of N is coordinatewise affine. There is
no guard inversion in N. Write R=x0*x1*x2*x3 and

  Nt=R conjugate(N)(x0^-1,x1^-1,x2^-1,x3^-1), H=N entrywise-multiplied by Nt.

Coefficient conjugation has no transpose. Nt is polynomial and H has degree
at most 2 in each variable. On the unit torus H=R*|Delta|^2*|M|^2 entrywise.
External invertible-complex monomial equivalence to F8 forces |M|^2 to have
rank one, since its entries are positive row factors times positive column
factors even after permutations. Hence the original 784 two-by-two minors
P_(a,r,b,c)=H_ab H_rc-H_ac H_rb must vanish. Only necessity is used. No entry,
anchor, matrix determinant, or additional local/global hypothesis is inverted
or assumed nonzero.

## 3. Cross-stage double-centering and all four original pole guards

Let F be the product of the four moving branch guards. Each is 1-h*xj for
a different variable, so they are pairwise coprime prime polynomials. The
other two guards are fixed nonzero constants. Thus Delta=cF with c!=0, and
F!=0 is exactly the remaining inverse condition.

In the Laurent rational-function field define dagger as coefficient
conjugation, reciprocal variables, and transpose. Norm-one gains give
W^dagger=W^-1, so G+G^dagger=I and S_t+S_t^dagger=3I. Put
c_t=-1/(h_t0 h_t1 h_t2) and R_t=the product of that stage's two variables.
Clearing denominators gives the polynomial identities

  R_t conjugate(D_t)(x^-1)=c_t D_t,
  R_t conjugate(A_t)(x^-1)=c_t(3D_t I-A_t^T),
  Nt=c_1*c_0(3D_1 I-A_1^T)(3D_0 I-A_0^T).

The identity is first derived where the formal inverses exist, then is an
identity of polynomials. In particular it remains true when phase coordinates
are zero. No unitarity claim at a zero coordinate is made.

Fix one moving branch guard f=1-h*xj and reduce modulo f. In this quotient
the active cycle has holonomy one and all its gains are units. Its B has
rank one and diagonal entries 1. More explicitly B=u v^T with u=B[:,0],
v^T=B[0,:], and u_k v_k=1. This follows by propagating each column around
the cycle using (I-W)B=0 and B_00=1. Thus the factorization is over the
quotient ring, not merely a pointwise rank assertion. The other stage and
other active branch variables remain polynomial indeterminates.

At a stage-0 pole D_0=0 and A_0=kappa*u v^T, with kappa the product of that
stage's other two guards. Therefore

  N=kappa*(A_1 u)*v^T,
  Nt=-c_1*c_0*kappa*((3D_1 I-A_1^T)v)*u^T.

Because v_j u_j=1, H has identical columns modulo f. At a stage-1 pole
the analogous formulas have left factors u and v, so H has identical rows.
These are polynomial identities even if kappa vanishes at an intersecting
pole. No other guard, component, or exceptional point is discarded.

For i,j in {1,...,7}, set

  K_ij=H_ij-H_i0-H_0j+H_00.

Every entry of K vanishes at each of the four original pole divisors: stage-0
poles give equal columns, and stage-1 poles give equal rows. By the prime and
coprime properties, F divides every entry of K in K[x0,x1,x2,x3]. Define

  E=K/F, a 7-by-7 polynomial matrix.

Since K has coordinate degree at most 2 and F has degree exactly 1 in every
variable, degree additivity over an integral domain gives coordinate degree
at most 1 for E (including the zero-entry case). This proves its complete
16-monomial containing support, without a modular zero projection.

Double-centering is left and right multiplication by fixed difference
matrices. Thus rank(H)<=1 implies rank(K)<=1. On the original legal domain
F!=0, rank(E)<=1 follows. All 441 two-by-two minors T of E are therefore
necessary. Each is supported on the complete 81 monomials x^e,
e in {0,1,2}^4. No support restriction beyond the proved coordinate degree
is used.

There is an exact bridge to the original 784 equations. For 1<=a<r<=7 and
1<=b<c<=7 let row pairs be [(0,a),(0,r),(a,r)], column pairs be
[(0,b),(0,c),(b,c)], and signs [+1,-1,+1] in both lists. Cauchy-Binet gives

  F^2 T_(a,r,b,c) = sum_(u=0)^2 sum_(v=0)^2 sign_u sign_v
                         P_(row_pair_u,column_pair_v).                 (1)

The identity also follows by expanding both centered 2-by-2 determinants.
It uses no rational division. It retains all zero-coordinate and pole
components in the original polynomial equations.

## 4. All 256 exact determinant certificates

`CERTIFICATES_PRIMARY.json` and `CERTIFICATES_CONJUGATE.json` each contain
all 256 labels in order e0=8,...,23, then e1=8,...,23. The coordinates,
all 81 coefficient columns, 81 selected original equation rows, and the
determinant residue are explicit in every record. Every recorded rank is 81
and every determinant residue is nonzero, in both embeddings.

Equation rows are indexed by 21 times the lexicographic pair index for rows
0,...,6 of E, plus the lexicographic pair index for columns 0,...,6 of E.
These are original H row/column indices one greater. Coefficient columns are
the lexicographic list {0,1,2}^4, last coordinate varying fastest. The constant
monomial is column 0. Selected rows are in their recorded ascending original
order; determinant signs include the pivot-column permutation. No row or
column projection changes an equation.

Use the coefficient ring

  R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 original Gaussian pairs].

All gains, conjugate gains, h and inverse h lie in this ring. N,Nt,H,K use
ring operations. Division by an original factor 1-h*xj has constant term 1,
and the recurrence q_e=p_e+h*q_(e-unit_j) proves every coefficient of each
exact polynomial quotient stays in R0. Consequently E and T coefficients
are in R0; no pole guard is inverted in the coefficient ring.

The prime p=65,537 is checked by complete trial division. Its two embeddings
send i to 256 and 65,281. Both square to -1 modulo p. All 68 Gaussian
factors inverted in R0 have nonzero images, as do every frozen holonomy and
guard. Thus each calculation is under a genuine coefficient-ring map
R0 -> F_p. Conjugation is computed via the opposite Gaussian embedding,
never via a finite-field absolute value. Coefficient computations use exact
integer arithmetic and explicit reductions; no floating point is used.

For a label let C be the 81-by-81 exact characteristic-zero coefficient
matrix of its recorded T rows and all 81 columns. The recorded nonzero
determinant residue proves d=det(C)!=0 in K. Since the entire proved support
is used, the adjugate identity is an exact polynomial identity

  d = sum_(j=0)^80 cofactor(C)_(j,0) T_(selected_row_j).                 (2)

Every cofactor is the determinant of an explicitly specified 80-by-80
Gaussian-rational matrix; the certificate is reconstructible without
printing enormous expanded rational coefficients. Combining (1) and (2)
gives d F^2 in the ideal of the original 784 P. On the original guarded
unit torus every P would vanish while dF^2 is nonzero. Contradiction.

This is characteristic-zero determinant lifting with a complete support
proof and an adjugate identity. It is not finite-field rootlessness, a
modular Groebner-unit inference, numerical fitting, or a claim that a
modular point is a complex Fourier witness.

## 5. New controls, exact delta and independent review checklist

`check_cross_stage.py` is newly authored for this candidate. It constructs
all weighted path numerators directly from the inert chart, forms the
opposite-embedding reciprocal numerator, builds H and the centered K,
checks complete division by each active guard, multiplies F*E back in all
81 coefficient positions, constructs all 441 full T coefficient vectors,
and records the full-column determinant certificates. No historical program
was imported, executed or compiled. A certificate is not independently
accepted merely because its author produced it.

The exact proposed delta is 256 previously uncovered four-dimensional
phase families, under the one original chart and all original guards.
The family includes all 16-by-16 placements stated in section 1. It neither
closes Q27 nor changes its priority. Algebraic elimination, determinant
lifting and Cauchy-Binet are classical tools. The family-specific guarded
exclusion is the candidate contribution; no historical-priority or
complexity novelty is established.

Independent reviewer should:
1. Match the chart and predecessor hashes and verify this family is outside
   the accepted triples and one-free-branch scopes.
2. Reconstruct the exact original six Green branches, edge directions,
   frozen gains, product order and all denominator/phase premises.
3. Check the cleared conjugate-reciprocal identity, both pole directions,
   intersecting-pole retention, coprimeness, and E's characteristic-zero
   multiaffine support.
4. Check all nine signs in (1), the monomial/equation order, and the
   coefficient-ring specialization and determinant sign convention.
5. Independently reconstruct all 256 coefficient matrices and replay the
   frozen row minors in both embeddings, without selecting replacements.
6. Check a separately reconstructed exact rational original-model control
   and zero/pole/normalization negative controls as appropriate.
7. Confirm the conclusion remains only this 256-family exclusion, with no
   full-fiber, Fourier construction, runtime, novelty, status or publication
   claim. No external writes or table changes were performed here.
