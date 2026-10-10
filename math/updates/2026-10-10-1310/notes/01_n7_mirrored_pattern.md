# N=7 bank boundary and an exact mirrored six-bank obstruction

10 October 2026. A bounded continuation of the signed magnetic-resolvent grammar.

## Status and result

1. **Already accepted consequence:** five banks are impossible in characteristic zero. The frozen independent review already explicitly establishes `r_+ >= 3` and `r_- >= 3` at N=7. The four-orientation support requirement and isolated-row obstruction apply regardless of how many banks have the opposite delta sign. Thus the accepted lower bound is **at least six**, not merely at least five. This note does not claim this consequence as a new theorem.
2. **Independently accepted proposition (10 October 2026):** six banks with multiplicities `(n_++,n_-+,n_+-,n_--)=(2,1,1,2)` cannot realize the negative Fourier matrix in characteristic zero. This includes arbitrary parameters in an arbitrary characteristic-zero extension field, subject to the original bank legality conditions. It is proved below by a finite exact edge-row parameterization and an incompatible actual b=0 coefficient row.
3. **Not concluded:** the same-epsilon patterns (2,1,2,1) and (1,2,1,2), six-bank feasibility in general, and the exact N=7 minimum. The accepted transpose partner (1,2,2,1) is recorded in the independent proof. No algorithmic speedup or historical-priority claim is made.

The new proposition uses a certified nonzero determinant under good reduction. It is not an extrapolation from the failure of a parameter search over a finite field.

## 1. Grammar and the inherited five-bank consequence

Let q be any primitive seventh root in a characteristic-zero field. The polynomial Phi_7 is irreducible over Q because Phi_7(t+1) is Eisenstein at 7; consequently K=Q(q) has the exact basis 1,q,...,q^5 used by the certificates. Let `S e_i=e_(i+1 mod 7)`, `T e_i=q^i e_i`, and `W_(a,b)=S^a T^b`. A bank is

`(1/7) sum_(j=0)^6 w_j [I-alpha S^epsilon-beta q^(epsilon delta j) T^delta]^(-1)`,

with epsilon,delta in {+1,-1} and guard `Delta=1-alpha^7-beta^7 != 0`.

The accepted coefficient expansion is

`sum_(ell=0)^6 h_ell sum_(r=0)^(6-ell) alpha^r [r+ell choose ell]_(q^(epsilon delta)) W_(epsilon r,delta ell)`.

Allowing h_ell to be independent only enlarges the legal class. All exclusions here hold in this enlarged class, so no beta or phase-weight choice repairs them.

The Fourier Weyl coefficients are `C q^(2(a+b)^2)`, where

`C=(1/7) sum_(j=0)^6 q^(-j^2) != 0`.

Here 2 is the inverse of 4 modulo 7. Divide amplitudes by C and write `f(a,b)=q^(2(a+b)^2)`.

The four signed orientations must all occur. On b=1 and a=1,...,6, every delta=-1 bank vanishes. If only two delta=+1 banks occur, support forces one in each epsilon orientation. The accepted exact N=7 row ideal is the unit ideal over Q(q), so those two cannot match this row. Simultaneous reflection `(a,b)->(-a,-b)` gives the same statement for delta=-1. Hence `r_+>=3`, `r_->=3`, and five banks are excluded for every duplication pattern.

This is stated explicitly in the frozen baseline independent review's section “N7 symbolic control and still-open small scope.” The review's original general-six-bank attainment question remains separate.

## 2. Three-bank edge row as two-atom moments

Consider the positive-delta banks `(++ with x), (++ with z), (-+ with y)`. The negative-delta banks contribute only to the axis a=0 of the b=1 row, so they cannot alter this calculation.

Put `H=q/(1+q)`. The a=6 endpoint forces `h_y=H/y`; therefore y is nonzero. For a=1,...,5, let

`G_a=(1-q^(a+1))/(1-q)=[a+1]_q`,

`B_a=(1-q^(a-1))/(1-q^(-1))=[8-a]_(q^(-1))`.

Every G_a used is nonzero. Define m_0=1 and, for a=2,...,5,

`m_(a-1)(y)=q^(2(a+1)^2)/(H G_a) -(B_a/G_a) y^(6-a)`.

The full six nonaxis edge coefficients are equivalent to

`A+B=1`,

`A x^j+B z^j=m_j(y)`, j=1,2,3,4,

where `A=h_x x/H`, `B=h_z z/H`. This expression is valid even if x or z is initially zero; no inverse of those parameters has yet been used.

For easy reproduction, the four nonconstant moments in the basis 1,q,...,q^5 are

- `m1=-1-q-q^4-q^5-(q^2+q^5)y^4`;
- `m2=1+q+q^3+q^4-(1+q^3+q^4)y^3`;
- `m3=-q^2-(1+q^2+q^3+q^4+q^5)y^2`;
- `m4=-q^2-q^3-(q^2+q^3+q^4+q^5)y`.

Set

`D=m2-m1^2`,

`Sn=m3-m1*m2`,

`Pn=m1*m3-m2^2`,

`R=det [[1,m1,m2],[m1,m2,m3],[m2,m3,m4]]`.

Every two-atom moment sequence has R=0. Exact polynomial Euclidean calculations in Q(q)[y] give

`deg R=9`,

`gcd(R,y)=gcd(R,D)=gcd(R,Pn)=gcd(R,Sn^2-4PnD)=1`.

The literal coefficients and independently recomputed exact outputs accompany this note. These gcds rule out every degenerate edge case, not only a generic open subset.

Consequently D is nonzero at every edge candidate. The two recurrence coefficients are uniquely

`S=x+z=Sn/D`, `P=xz=Pn/D`.

Indeed `m2=S m1-P`, `m3=S m2-P m1`, and the last recurrence `m4=S m3-P m2` is exactly R/D=0. The gcds ensure P is nonzero and `S^2-4P` is nonzero. Thus x,z are distinct nonzero roots of `t^2-S t+P`.

Conversely, take any root y of R in an algebraic closure of Q(q), choose the distinct roots x,z of this quadratic, and solve

`A=(z-m1)/(z-x)`, `B=(m1-x)/(z-x)`.

Set `h_x=H A/x`, `h_z=H B/z`, `h_y=H/y`. The recurrence verifies all six nonaxis edge coefficients. All denominators are nonzero. Thus this is an exact complete edge-row parameterization for this duplication pattern; it is not a full Fourier realization.

There are at most nine singleton values and at most eighteen ordered duplicated-parameter pairs. The ordering of the two duplicate banks does not change the represented class. No approximate roots or parameter scan is used.

## 3. The mirrored six-bank pattern

Now consider exactly

`(++ with x), (++ with z), (-+ with y), (+- with v), (-- with u), (-- with w)`.

The preceding edge analysis requires `R(y)=0`, `x+z=S(y)`, and `xz=P(y)`. Simultaneous reflection preserves f and transforms the negative-delta edge into the same analysis. Therefore

`R(v)=0`, `u+w=S(v)`, and `uw=P(v)`.

This leaves the finite algebra

`B=Q(q)[Y,V]/(R(Y),R(V))`,

which has dimension 81 over Q(q). Replacing R by its monic scalar multiple does not change this algebra. Both D(Y) and D(V) are units by the gcd calculation.

The axis row b=0 is not automatically free. Its seven coefficients receive six amplitudes, one ell=0 amplitude per bank. Negative-epsilon columns have entries `alpha^[(-a) mod 7]`; in particular their a=0 entries are 1. Replacing that entry by alpha^7 would be incorrect.

For a parameter variable Y, define the recurrence sequences

`U0=1, U1=0, J0=0, J1=1`,

`U_a=S(Y) U_(a-1)-P(Y) U_(a-2)`,

`J_a=S(Y) J_(a-1)-P(Y) J_(a-2)`, a=2,...,6.

For either root t of `t^2-S(Y)t+P(Y)`, one has `t^a=U_a(Y)+t J_a(Y)`.

Because the duplicated roots are distinct, the two columns `x^a,z^a` have exactly the same span as `U_a(Y),J_a(Y)`. Likewise, the two reversed columns of u,w have the same span as `U_r(V),J_r(V)`, where `r=[-a]_7`.

Define the 7-by-7 augmented matrix, with rows indexed a=0,...,6, by

`[ U_a(Y), J_a(Y), Y^r, V^a, U_r(V), J_r(V), q^(2a^2) ]`, `r=[-a]_7`.

Let A(Y,V) be its determinant, computed as an element of B. Any full six-bank representation in this pattern would require A(y,v)=0. This necessary condition uses the actual b=0 Fourier row, including its a=0 coefficient.

## 4. Exact good-reduction certificate

The accepted certificate specializes q to 7 modulo the prime 29. This is valid because 7 has multiplicative order 7 in F_29, and Phi_7(7)=0 modulo 29. Every original scalar denominator has nonzero image. The leading coefficient of R also has nonzero image, so the specialized monic polynomial is

`Rbar(T)=T^9+23T^8+2T^7+5T^6+27T^4+21T^3+12T^2+25T+21` in F_29[T].

The checker verifies that D has an inverse modulo Rbar. Consequently the specialized finite free algebra

`Bbar=F_29[Y,V]/(Rbar(Y),Rbar(V))`

still has the same monomial basis `Y^i V^j`, 0<=i,j<9, and every entry used to form A has a well-defined reduction.

The determinant A is computed by a division-free subset recurrence. The checker then builds the complete 81-by-81 matrix for multiplication by A in this monomial basis and obtains

`det(multiplication by A) = 14 mod 29`.

The full reduced A element is recorded as 81 coefficients in `AXIS_QUOTIENT_CERTIFICATE.json`; `AXIS_MULTIPLICATION_MATRIX.json` contains the complete 81-by-81 multiplication matrix, determinant, basis convention, and good-reduction data. No root search is involved.

### Why this proves a characteristic-zero exclusion

Take the local coefficient ring of Z[q] at the prime ideal `(29,q-7)`. All scalar denominators and the leading coefficient of R are units there. Since D is invertible in the reduced monic quotient, the determinant of multiplication by D is also a unit in this local ring; hence D has a quotient-ring inverse before reduction. Thus the matrix for multiplication by A is defined over a local ring and reduces to the displayed finite-field matrix.

Its determinant has nonzero reduction 14, so it is nonzero in Q(q). Multiplication by A is therefore invertible on B. Hence A itself is a unit in B: apply the inverse multiplication map to 1.

For any characteristic-zero extension field and any simultaneous root pair R(y)=R(v)=0, evaluation is a homomorphism from B to that field. It sends the unit A to a nonzero element. Therefore A(y,v) cannot be zero, contradicting the necessary actual b=0 row condition.

This argument uses nonvanishing of a determinant in a finite free algebra with verified good reduction. An ordinary finite-field failure or a finite-field parameter scan would not justify this conclusion.

## 5. Scope and public evidence

The result excludes the specified mirrored duplication pattern in characteristic zero. The separate [independent proof](03_n7_independent_proof.md) also verifies the transpose-equivalent pattern (1,2,2,1). The same-epsilon patterns (2,1,2,1) and (1,2,1,2) remain open, as do general six-bank attainment and the exact N7 minimum. The inherited overall lower bound remains six.

The proof applies in the larger independent-amplitude class, so arbitrary legal beta parameters and phase weights cannot repair the specified patterns. This is a representation obstruction in a fixed small-size grammar. One hypothetical six-bank representation would involve up to 42 literal phase-indexed resolvents, with separately charged weights. Nothing here is a runtime lower bound, an FFT improvement, or a claim of historical novelty.

The accepted author note has SHA-256 7d6b742bd6289fd099f3f713204725d5a54b496262733996920c8edb4a2809b8. Sections 1–4 preserve its mathematical argument. This public transcription updates the status and source navigation only. The [proof status](../PROOF_STATUS.json) records the accepted source hashes and the exact scope.

Public literal data are [the edge moments](../controls/n7/sources/EDGE_MOMENT_CERTIFICATE.json), [the axis element](../controls/n7/sources/AXIS_QUOTIENT_CERTIFICATE.json), and [the complete multiplication matrix](../controls/n7/sources/AXIS_MULTIPLICATION_MATRIX.json). The [independent controls](../controls/n7/README.md) were freshly written from the mathematical definitions; no supplied or predecessor research program was executed or imported in producing this checkpoint.

## Source linkage

The inherited signed-bank model and control scope are retained in the [earlier signed magnetic fusion note](../../../current/research_cycle_0958/signed_magnetic_fusion/final_v1/SIGNED_MAGNETIC_FUSION.md) and [small-size scope](../../../current/research_cycle_0958/signed_magnetic_fusion/final_v1/SMALL_CONTROL_SCOPE.md). The inherited independent acceptance record has SHA-256 ef38042e02ff4771cb396f3b3b61d2bc29fe9f24676b5660306f2a44729c7ffc.

The [N5 lower bound](../../2026-10-10-1220/notes/06_four_bank_lower_bound.md) and [five-bank construction](../../2026-10-10-1220/notes/05_n5_five_bank_construction.md) motivate checking actual axis constraints but are not used as an N7 sufficiency claim.
