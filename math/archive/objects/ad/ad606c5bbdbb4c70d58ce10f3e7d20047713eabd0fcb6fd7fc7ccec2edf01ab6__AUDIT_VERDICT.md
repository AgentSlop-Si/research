# Independent audit: Fourier-8 diagonal-orbit rejection and adjacent interface

## Verdict

**PASS, at precisely the stated scope.**

1. The half-pair anchor's entire nonsingular diagonal orbit is excluded for the specified second-factor support cycles. The exclusion is valid over every field of characteristic other than 2 containing a primitive eighth root of unity. It does not assume the selected pivots are nonzero, does not assume nonzero cycle edges, and does not use determinant-guard inequalities in the elimination.
2. The adjacent-pair anchor's stated guarded chart is equivalent to its 40 stored equations in 12 variables. The direction and endpoint-scale reconstruction is complete. Its determinant and endpoint guards are correctly indexed and sufficient. This audit does not solve that system or establish that the chart is nonempty.
3. All 176 exported expressions, across both anchors, agree coefficient for coefficient with independently reconstructed exact matrix expressions. This is an exact polynomial check, stronger than agreement at a finite list of points.
4. No supplied Python program was run, imported, or modified. The ten supplied SHA-256 seals matched before and after the audit. The manifest itself was additionally hashed and checked unchanged.

No fatal error, missing division guard, incorrect support orientation, or scale-completion gap was found. No universal Fourier-8 obstruction, unrestricted two-layer result, growing-size algorithm, or novelty conclusion follows from this verdict.

## Inputs and reproducibility

Read-only input package:

`fourier8_kernel_construction_0249/`

Principal audited files:

- `FOURIER8_DIAGONAL_ORBIT_REDUCTION_AND_REJECTION.md`
- `ADJACENT_ANCHOR_ORBIT_SYSTEM.json`
- `HALF_ANCHOR_ORBIT_SYSTEM.json`
- `HALF_ORBIT_EXACT_REJECTION.json`
- `EXACT_INTERFACE_CONTROLS.json`
- `SHA256SUMS.txt`

The supplied source was inspected as text, not executed. A fresh checker, `independent_audit.py`, uses SymPy 1.14.0 for matrix multiplication, exact rational inverses and determinants, and polynomial remainders modulo z^4+1. It does not reuse the supplied sparse-polynomial arithmetic, supplied inverse routine, or supplied controls. The JSON coefficient arrays are read only as data and compared against fresh matrix-derived expressions.

Reproduce with:

```sh
python3 fourier8_orbit_independent_audit_0312/independent_audit.py
```

A successful run writes `AUDIT_RESULTS.json` and `SOURCE_SEALS.json`. The captured successful output is `reproduction.log`. This audit directory is separately sealed in `SHA256SUMS.txt`.

## 1. Support and branch grammar

The orders and maps are independently verified as:

- pi order: (0,1,2,3,4,5,6,7)
- sigma order: (0,2,5,1,7,4,6,3)
- pi map: (1,2,3,4,5,6,7,0)
- sigma map: (2,7,5,0,6,1,3,4)

Both are single Hamiltonian 8-cycles. Their directed edge sets are disjoint. They do not commute: pi(sigma(0))=3 and sigma(pi(0))=7. With the convention P e_j=e_pi(j), the support union of column j is exactly {j,pi(j),sigma(j)}. The least off-support pivot rows are (3,0,0,1,0,0,0,1), as claimed.

A diagonal-plus-weighted-cycle inverse branch with nonzero diagonal coefficients can be normalized as

Q0=D_rho U, U=I+D_u P_pi,

or, for the other branch,

Q1=V D_tau, V=I+P_sigma D_v.

Nonzero rho and tau are exactly what allow the two normalizations. Zero edges cause no difficulty. Conversely, such normalized matrices are inverse Green branches with nonsingular diagonal endpoints whenever they are invertible: U=I-W0 with W0=-D_u P_pi, and V=I-W1 with W1=-P_sigma D_v. Their endpoint factors are D_x and D_y, where x=rho^{-1} and y=tau^{-1}.

The matrix identity

U M V=U D_y+D_x V

follows from M=Q0^{-1}+Q1^{-1}. Every entry of its right side has been independently checked symbolically:

- diagonal i: y_i+x_i
- pi edge (pi(j),j): u_pi(j) y_j
- sigma edge (sigma(j),j): x_sigma(j) v_j
- all other positions: zero

Disjointness is essential for this simple edge-scale recovery, and is verified for this exact pair.

## 2. The four-ratio diagonal-orbit reduction is correct

Let X1=A K B with arbitrary nonsingular diagonal A,B. Since K^2=2I,

F=X2 A K B implies X2 A=F B^{-1} K/2.

For each anchor pair (a_j,b_j), define C_a_j=C_b_j=(B^{-1})_a_j and t_j=(B^{-1})_b_j/(B^{-1})_a_j. Then B^{-1}=T C, with T_a_j=1 and T_b_j=t_j. The four t_j are nonzero, and C commutes with K. Therefore

X2 A C^{-1}=F T K/2.

Left and right multiplication by nonsingular diagonals preserves each specified inverse support: if G=Q^{-1}, then L G R=(R^{-1} Q L^{-1})^{-1}, with the same diagonal and cycle-edge locations and nonzero diagonal coefficients. Scaling by 2 also preserves this class because characteristic is not 2. Consequently the full diagonal orbit is equivalent to testing whether M=F T K is the prescribed inverse-branch sum.

Conversely, any such sum gives

F=(M/2)(K T^{-1}).

The factor 1/2 is indispensable and is correctly present in the source and stored reconstruction; the actual second-factor inverse branches are 2Q0 and 2Q1. The audit verifies this Fourier reconstruction exactly for both anchors, symbolically in all four ratios.

### First-factor legality

The displayed sparse-mask anchor construction is correct. Put i=z^2. On every pair (a,b), take W0_ab=1/i=-i and W1_ba=1/(-1-i)=(i-1)/2. Both masks square to zero. Their inverse Green matrices are I+W0 and I+W1, with determinant guard 1. The sum

i(I+W0)+diag(1-i on a,-1-i on b)(I+W1)

is exactly K. The endpoint factors are nonzero because i has order 4 and characteristic is not 2. The alternating orders stated in the source contain these directed pair edges. Remaining connecting edges have zero weight. Multiplication by T^{-1} preserves nonsingular endpoints. This validates the sparse-mask grammar, not an all-first-layer-edges-nonzero grammar.

## 3. Necessity of the off-support minors needs no pivot guard

Set A=UM, C=A P_sigma, a_j=A_kj,j, c_j=C_kj,j, and H_ij=c_j A_ij-a_j C_ij.

For any off-support row i, the full matrix identity implies A_ij+v_j C_ij=0. Its pivot row implies a_j+v_j c_j=0. The identity

c_j(A_ij+v_j C_ij)-C_ij(a_j+v_j c_j)=H_ij

proves H_ij=0 with no division. It is valid when a_j=0, c_j=0, or both. In particular, when both are zero, the resulting minors can be identically zero; this weakens the necessary test but cannot make a genuine solution fail it.

The half-orbit contradiction uses only this necessary condition. It does not turn it into a sufficiency claim on degenerate pivots.

## 4. Independent half-orbit certificate audit

The fresh F T K construction reproduces these four minors exactly:

H_2,5=-4 t1 z (u0-u2),
H_3,5=4 t1 z (i-u0 u3),
H_4,5=-4 t1 z^3 (u0-u4),
H_7,5=-4 t1 z (i-u0 u7).

Because t1 and z are nonzero and 4 is a unit, these give, with w=u0,

u2=u4=w, u3=u7=i/w.

The nonzero condition on w is derived from w u3=i; it is not borrowed from the adjacent chart's edge guard.

After this substitution, exact polynomial identities give

w(H_4,0+H_3,4)=-4i(t0+t2).

Thus t2=-t0. Write a=t0, so a is nonzero. Define

E=(a^2+1)(1+i)w+i(1-a^2),
R=(a+1)w-(a-1),
S=-i(a-1)w-(a+1).

The exact reduced minors are w H_4,0=-2E and H_2,4=-2RS, hence E=0 and RS=0. At a=1 or a=-1, E=2(1+i)w is nonzero; thus both a-1 and a+1 are nonzero. Here 1+i is nonzero since (1+i)(1-i)=2.

Put q=a^2-2ia+1 and C=(a^2+1)(1+i). The checked identities are

(a+1)E=C R+(a-1)q,

i(a-1)E+C S=-i(a+1)q.

Over a field, RS=0 means R=0 or S=0. Either identity, with the appropriate already-verified nonzero multiplier, gives q=0. Therefore a^2+1=2ia is nonzero and C is nonzero. The first identity now forces R=0. The further exact identity

(a+1)^2(w^2-i)-(1-i)q=R((a+1)w+(a-1))

forces w^2=i.

Finally, the independent reduced last minor is

w H_7,2=(1-a)J,

J=(t1+1)w(z^3-z)+(t1-1)(1+i).

Since a is not 1, J=0. However, the exact product identity is

J((t1+1)w(z^3-z)-(t1-1)(1+i))
=2(t1+1)^2(w^2-i)+8i t1.

This uses (z^3-z)^2=2 and (1+i)^2=2i, both separately verified modulo z^4+1. Since w^2=i, its right side is 8i t1, which is nonzero in every stated field. Contradiction.

All eight source positions are independently confirmed off support. All 12 principal certificate identities are checked as exact identities in characteristic zero with integral coefficients, and the argument above accounts for every division and nonzero inference when specialized to any allowed characteristic. No numerator is discarded and no zero-edge branch is silently removed. There are no numerical residuals, prime-sampling extrapolations, or unproved radical-membership assertions in this exclusion.

## 5. Adjacent guarded chart: complete necessity and sufficiency

The chart requires nonzero t_j, u_i, a_j and c_j. Therefore v_j=-a_j/c_j is defined and nonzero, and

(UMV)_ij=H_ij/c_j.

The two disjoint edge positions determine all 16 endpoint scales:

x_i=-H_i,s(i)/a_s(i),
y_j=H_pi(j),j/(c_j u_pi(j)),

where s=sigma^{-1}. These are the source's formulas, with their orientations independently verified.

There are five off-support rows per column. The pivot's minor is identically zero, leaving four listed conditions per column, or 32 equations. This count does not claim algebraic independence of the 32 polynomials. The eight remaining diagonal equations are the zero numerators of

H_ii/c_i-x_i-y_i.

Their common clearing factor is precisely c_i a_s(i) u_pi(i), all nonzero in the chart. The resulting polynomial is

u_pi(i) a_s(i) H_ii+c_i u_pi(i) H_i,s(i)-a_s(i) H_pi(i),i.

There is no additional denominator hidden by this clearing. All 64 entries of the matrix sufficiency statement were independently checked symbolically with arbitrary H,a,c,u:

- the 16 pi/sigma edge equations close identically by reconstruction;
- the 8 diagonal residuals are the stated diagonal equations divided by guarded factors;
- the 40 off-support residuals are H_ij/c_j, with 8 pivot minors identically zero.

Consequently the 40 equations imply the full matrix identity. The invertibility guards then allow multiplication by U^{-1} and V^{-1}, giving the exact inverse sum. The reverse implication follows by the same identities. This proves iff on the stated chart; zero-pivot and zero-edge points outside it are not tested by this equivalence.

### Complete guard accounting

- Four t_j: T and the first factor's right endpoint are nonsingular.
- Eight u_i: every first normalized second-factor edge is nonzero and the y reconstruction denominators exist.
- Eight a_j and eight c_j: v exists and has every edge nonzero; the x reconstruction denominators exist.
- Eight H_pi(j),j: all y_j are nonzero, hence Q1's diagonal endpoint coefficients are nonzero.
- Eight H_sigma(j),j: all x_sigma(j) are nonzero, hence Q0's diagonal endpoint coefficients are nonzero.
- 1-product(u_i): det U is nonzero.
- product(c_j)-product(a_j): det V is nonzero, because det V=1-product(v_j) and, for eight columns, product(v_j)=product(a_j)/product(c_j).

The two determinant formulas were independently computed symbolically. No additional edge or endpoint guard is needed for the prescribed second-factor branch grammar. The first-factor constants and factor of 2 are nonzero under the field assumptions.

### Stored coefficient audit

For each anchor, the independent checker rebuilds F,T,K as matrices, multiplies them to obtain M, computes U M and (U M)P_sigma, and forms its minors. The diagonal equations are separately generated by reconstructing x,y and clearing the actual diagonal residual, rather than by copying the source polynomial-generation routine.

All 88 expressions per anchor match exactly, including all zero pivot minors. Variables, zero-equation indices, support maps, pivots, and guard indices agree. The adjacent equations have maximum total degree 7 and 890 monomials; the half equations have maximum total degree 7 and 880 monomials. Counts treat 1,z,z^2,z^3 as the coefficient basis, not additional unknowns.

## 6. New exact controls and boundary tests

Four newly chosen rational parameter sets (seeds 7, 11, 19, 23), including negative values and nonintegral fractions, manufacture legal full-edge inverse sums on the stipulated supports. Each control verifies:

- all chart guards;
- all 40 equations;
- recovery of the original eight v, eight x, and eight y;
- the full 8-by-8 exact inverse-sum identity.

For each seed, perturbations of entries (0,0), (2,5), (4,0), and (7,7) by 1/13 are rejected. Thus all 16 new negative controls fail the equations as expected.

Two endpoint-boundary controls set x0=0 or y0=0 in the normalized matrix identity. Each still satisfies the 40 equations, but violates the corresponding endpoint numerator guard. These controls demonstrate why the endpoint guards are necessary and must not be dropped. They are deliberately not asserted to be legal inverse-branch sums.

Two legal edge-degenerate controls use all edges zero, or selected edges zero. Every off-support minor still vanishes. The all-zero-edge control has all eight pivot pairs (a_j,c_j)=(0,0); the mixed control has one such pair. These explicitly check that the necessary-minor mechanism remains valid when the constructive chart is unavailable.

These manufactured controls validate the interface and its boundaries; none is a Fourier-8 solution.

## Scope limits and remaining work

This audit establishes the exact exclusion of the specified half-anchor diagonal orbit and validates the adjacent open-chart interface. It does not solve the adjacent system, certify numerical near-solutions, inspect the optional numerical probe's search coverage, or claim that no other Fourier factorization exists. Other first factors, support pairs, endpoint permutations, and zero-pivot adjacent branches remain outside this conclusion. The source's bounded-probe disclaimer and warning against a free growing-N lift are appropriate.
