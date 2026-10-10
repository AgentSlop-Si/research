# Exact closure of the Fourier-8 adjacent-anchor boundary

## Result and status

**No constructive escape exists on the boundary `u0*B1*B5*B6=0` for the stipulated adjacent anchor and stipulated second-factor support pair.** This statement allows arbitrary zero cycle-edge coefficients, but retains the legal nonzero anchor ratios and nonsingular diagonal endpoint grammar.

Five newly authored exact elimination certificates prove this boundary theorem over every characteristic-zero field containing a primitive eighth root of unity. A separate implementation, using only the Python standard library and abstract rational arithmetic in `Q[z]/(z^4+1)`, regenerates their source formulas, checks all Bézout identities and denominator supports, and passes 210 checks. Three manufactured legal non-Fourier controls include zero-edge and zero-pivot cases. This package has not yet received a separate-worker audit; its exact checker has passed.

**Corollary, combined with the accepted nonboundary obstruction:** the entire nonsingular diagonal orbit of the adjacent-pair anchor is excluded for this fixed second-factor support pair. The predecessor excludes the complementary chart `u0*B1*B5*B6 != 0`; the new theorem excludes its whole legal boundary. No universal two-layer obstruction, free-first-layer obstruction, positive Fourier-8 kernel, or growing-size FFT consequence follows.

The boundary proof and certificate checker are self-contained. The corollary explicitly invokes the accepted nonboundary theorem from `ADJACENT_ANCHOR_EXACT_OBSTRUCTION.md`; this package does not purport to reverify that predecessor's 11 MB proof DAG. The earlier diagonal-orbit reduction and support conventions were also supplied in the independently audited predecessor reports.

## 1. Exact problem and legal guards

Let `z` be abstract, with `z^4+1=0`; put `F[r,s]=z^(rs)` for `0 <= r,s < 8`. Let `K_adj` be block-diagonal with blocks `[[1,1],[1,-1]]` on pairs `(0,1),(2,3),(4,5),(6,7)`. Let

`T=diag(1,t0,1,t1,1,t2,1,t3)` with every `t_a != 0`, and `M=F T K_adj`.

Thus

`M[r,2a]=z^(2ar)+t_a z^((2a+1)r)` and
`M[r,2a+1]=z^(2ar)-t_a z^((2a+1)r)`.

The two support maps are

`pi(j)=j+1 mod 8`, and `sigma=(2,7,5,0,6,1,3,4)` as an image list.

The associated Hamiltonian orders are `(0,1,2,3,4,5,6,7)` and `(0,2,5,1,7,4,6,3)`. The convention is `P e_j=e_map(j)`.

Every legal inverse branch, with nonzero diagonal coefficients, can be normalized as

`Q0=D_rho U`, `U=I+D_u P_pi`,
`Q1=V D_tau`, `V=I+P_sigma D_v`.

All `rho_i,tau_i` are nonzero; `U,V` must be invertible. Their edge variables `u_i,v_j` may be zero. A representation `M=Q0^(-1)+Q1^(-1)` implies, for `x=rho^(-1), y=tau^(-1)`,

`U M V = U D_y + D_x V`.                                  (1)

The right side is supported, in column `j`, on `{j,pi(j),sigma(j)}`. Only this necessary support condition is used below. The proof does not use endpoint-scale reconstruction, `x_i,y_i != 0`, or the determinant guards after normalization. It therefore cannot be repaired by changing endpoint scales or exploiting a zero edge.

For context, an adjacent-anchor diagonal-orbit factorization `F=X2 A K_adj B`, with `A,B` nonsingular diagonal, reduces by pairwise diagonal gauges to asking whether this `M` is the stipulated inverse sum. Conversely, any such sum would give

`F = (M/2) (K_adj T^(-1))`.

The factor `1/2` is essential. No candidate is constructed here, so no missing reconstruction scale can affect the exclusion.

## 2. Necessary equations that remain valid on zero pivots

Set `w=u0`, and let

`B_j=M[0,j]+w M[7,j]`.

The indices `J={1,2,4,5,6}` all have row 0 off their support unions. For each off-support row `r` from 1 through 7, define

`b[r,j]=B_sigma(j) M[r,j]-B_j M[r,sigma(j)]`,
`c[r,j]=B_sigma(j) M[r-1,j]-B_j M[r-1,sigma(j)]`.

Equation (1) implies

`h[r,j]=b[r,j]+u_r c[r,j]=0`.

No pivot is divided out here. For any eligible pair of columns,

`R[r;j,k]=b[r,j] c[r,k]-b[r,k] c[r,j]=0`.                   (2)

This is the exact identity `R=c[r,k]h[r,j]-c[r,j]h[r,k]`. It remains necessary when any displayed `b,c,B`, or edge variable is zero.

When `v_l=0`, equation (1) additionally gives

`M[r,l]+u_r M[r-1,l]=0`

at every off-support row of column `l`. Combining this with `h[r,j]=0` yields the necessary zero-edge eliminant

`E^l[r,j]=b[r,j] M[r-1,l]-c[r,j] M[r,l]=0`.                (3)

The checker verifies all row/column positions used below are off support.

### Polynomial chain quotients

If `sigma(j)=k` and `sigma(k)=l`, define

`C[r;j,k,l] = B_l det_r(j,k) - B_k det_r(j,l) + B_j det_r(k,l)`,

where `det_r(a,b)=M[r,a]M[r-1,b]-M[r,b]M[r-1,a]`.

Expansion gives the polynomial identity

`R[r;j,k]=B_k C[r;j,k,l]`.                                (4)

In particular,

- `L46[r]=C[r;4,6,3]=R[r;4,6]/B6` when `B6 != 0`;
- `L15[r]=-C[r;5,1,7]=R[r;1,5]/B1` when `B1 != 0`;
- `L25[r]=C[r;2,5,1]=R[r;2,5]/B5` when `B5 != 0`.

The implementation evaluates the polynomial `C`, rather than numerically dividing by a potentially vanishing `B`. Every use of necessity after canceling a `B` is justified below.

## 3. Row-zero closure and complete case partition

At the row-zero off-support positions, (1) says

`B1+v1 B7=0`, `B2+v2 B5=0`, `B4+v4 B6=0`,
`B5+v5 B1=0`, `B6+v6 B3=0`.                              (5)

Therefore:

- `B1=0` forces `B5=B2=0`, without assuming any edge nonzero.
- `B5=0` forces `B2=0`; if `B1 != 0`, it forces `v5=0`.
- `B6=0` forces `B4=0`; if `B3 != 0`, it forces `v6=0`.

Put, for `a=0,1,2,3`,

`N_a=1+w z^(-2a)`, `D_a=1+w z^(-(2a+1))`.

Then `B_(2a)=N_a+t_a D_a` and `B_(2a+1)=N_a-t_a D_a`.

If either member of a pair is zero, its equation automatically implies `D_a != 0`: otherwise `w=-z^(2a+1)` and `N_a=1-z != 0`, a contradiction. Since `t_a != 0`, it also implies `N_a != 0`. Thus solving a zero pair as `t_a=+N_a/D_a` for an odd zero or `t_a=-N_a/D_a` for an even zero introduces no new chart assumption. The paired nonzero entry is exactly `2N_a`.

The following ordered partition covers the whole boundary, including all intersections:

1. `w=0`.
2. `w != 0` and `B1=0`.
3. `w B1 != 0` and `B5=0`.
4. `w B1 B5 != 0` and `B6=0`.
   - 4a. `B3=0`.
   - 4b. `B3 != 0`, hence `v6=0` by (5).

The proof of 4a also works without the preceding `B1,B5` assumptions, since their nonvanishing is forced there. The proof of 4b needs no additional edge-nonzero assumption. No inference treats a vanishing-pivot minor as sufficient.

## 4. The five exact eliminations

Every rational coefficient below belongs to the abstract field `Q[z]/(z^4+1)`. An affine function `f(s)` is written `A s+D`, where `D=f(0)` and `A=f(1)-f(0)`. Affineness follows directly from the displayed formulas: each term contains at most one entry depending on the indicated free ratio. The checker additionally verifies the affine identity at `s=2` and checks all resulting exact rational expressions against the stored certificate.

For a rational function, `num` denotes its stored numerator; denominators are audited separately in Section 5. Scaling a nonzero polynomial to monic changes neither its roots nor its vanishing condition.

### Case 1: `w=0`

Here every `c[1,j]` is identically zero. Consequently the actual row-1 minors, not merely their degenerate row resultants, force

`b[1,2]=b[1,4]=b[1,6]=0`.

Use `d=t3` as the remaining parameter. The equation `b[1,6]=A6(d)t1+D6(d)=0` solves `t1=-D6/A6`; the equation `b[1,4]=A4(d)t2+D4(d)=0` solves `t2=-D4/A4`. Explicit constant-one Bézout identities for `(num A6,num D6)` and `(num A4,num D4)` show that neither solved coefficient can vanish at a solution.

After substitution, `b[1,2]=0` gives a monic quadratic `Q(d)=0`. Next `R[2;4,5]=A0(d)t0+P0(d)=0`. A stored identity

`S(d) Q(d)+T(d) num A0(d)=1`

shows `A0 != 0` when `Q=0`, so `t0=-P0/A0`. The remaining necessary equation `R[3;1,4]=0` gives a monic quartic `H(d)=0`.

The final explicit identity is `S_final Q+T_final H=1`. Hence this case is empty, even without requiring the four `t_a` nonzero.

Artifact: `WZERO_CERTIFICATE.json`. Final degrees: `(2,4)`.

### Case 2: `w != 0`, `B1=0`

Equation (5) forces `B5=B2=0`. Thus

`t0=N0/D0`, `t1=-N1/D1`, `t2=N2/D2`, with `t3=d` free.

All six `N0,D0,N1,D1,N2,D2` are nonzero by the legal-pair argument. Also `B4=2N2 != 0`; (5) then forces `B6 != 0`.

The necessary expression `L46[1]/w` is affine in `d`, say `A(w)d+D(w)`. Constant-one Bézout coefficients for its numerator pair `(num A,num D)` show `A != 0`, so `d=-D/A`. The necessary expressions `L46[2]` and `R[3;1,4]` then have numerator polynomials `Q(w),H(w)` with a final constant-one Bézout identity.

Crucially, `R[3;1,4]` is retained in full. **No factor `B7` is divided out**, so the potential `B7=0` subcase is covered too.

Artifact: `B1_CERTIFICATE.json`. Final degrees: `(5,8)`.

### Case 3: `w B1 != 0`, `B5=0`

Now `B2=0`, and (5) forces `v5=0`. Thus

`t1=-N1/D1`, `t2=N2/D2`, with `t0` unrestricted and `t3=d` free.

Again `B4=2N2 != 0`, so `B6 != 0`. Use exactly the affine equation `L46[1]/w=A(w)d+D(w)=0` from Case 2 and solve `d=-D/A`. The necessary expressions `L46[2]` and `E^5[2,4]` give coprime numerator polynomials `Q(w),H(w)`.

These expressions use only columns belonging to pairs 1, 2, and 3, so none depends on `t0`. The builder/checker set the unused placeholder `t0` to zero solely to form a matrix expression; **no legal Fourier candidate is restricted to `t0=0`**.

Artifact: `B5_CERTIFICATE.json`. Final degrees: `(5,4)`.

### Case 4a: `B6=B3=0`

Equation (5) gives `B4=0`, hence

`t1=N1/D1`, `t2=-N2/D2`, `t3=-N3/D3`, with `t0=a` free.

Every indicated `N,D` is nonzero. In particular `B5=2N2 != 0`, and (5) forces `B1 != 0`.

The necessary `L15[3]` is affine in `a`, with numerator coefficient pair having a constant-one Bézout identity. Solve `a=-D/A`. The necessary `L25[4]` and `L25[7]` give coprime numerator quintics `Q(w),H(w)`.

Artifact: `B6_B3_CERTIFICATE.json`. Final degrees: `(5,5)`.

### Case 4b: `B6=0`, `B3 != 0`

Here `B4=0` and `v6=0`. Therefore

`t2=-N2/D2`, `t3=-N3/D3`, with `t0,t1` free.

Use `E^6[1,2]=A1(w)t1+D1(w)=0`. The stored numerator Bézout identity has right side **`w`**, rather than 1. This is sufficient because Case 1 already excluded `w=0`. Thus `A1 != 0`, and `t1=-D1/A1`.

Next `E^6[2,5]=A0(w)t0+D0(w)=0`; its numerator coefficient pair has a constant-one Bézout identity. Solve `t0=-D0/A0`. Finally the necessary `E^6[4,1]` and `E^6[4,2]` give coprime numerator polynomials of degrees 5 and 4.

Artifact: `B6_ZEROEDGE_CERTIFICATE.json`. Final degrees: `(5,4)`.

This final certificate does not divide by `B3`; its nonvanishing is used only to derive the exact edge condition `v6=0` from (5).

## 5. Exhaustive denominator and guard audit

All cancellations fall into the following explicit categories:

1. Nonzero cyclotomic scalars and rational integers: valid in characteristic zero. No positive-characteristic extension is claimed.
2. `N_a,D_a` for a pair whose `B` entry is zero: nonzero by the elementary pair argument in Section 3 and the original legal guard `t_a != 0`.
3. `w`: used only after Case 1 has been excluded.
4. `B6` in Cases 2 and 3: forced nonzero by `B4=2N2 != 0` and `B4+v4B6=0`.
5. `B1,B5` in Case 4a: `B5=2N2 != 0`, then `B5+v5B1=0` forces `B1 != 0`.
6. Each newly solved affine coefficient: certified nonzero by an exact numerator Bézout identity. The only nonconstant right side is `w` in Case 4b; the other conditional coefficient in Case 1 is protected by `S Q+T num A0=1` at `Q=0`.

The checker does not merely compare rational functions after clearing arbitrary denominators. At each stage, it verifies that the denominator of every stored fraction is supported only on the currently justified nonzero factors: repeated exact polynomial gcd/division must remove every nonconstant denominator factor. It then adds a solved coefficient's numerator to the permitted guards only after checking the relevant Bézout identity.

This proves there is no discarded coefficient-zero branch, no unlisted reconstruction denominator, and no assumption that every cycle edge is nonzero. The legal determinant guards and endpoint-scale guards are not needed to obtain a contradiction.

Because all arithmetic and certificates are abstract in `Q[z]/(z^4+1)`, the theorem holds under every embedding into any characteristic-zero extension field. No numerical root selection or modular extrapolation enters the proof.

## 6. Verification, controls, and preservation

Run, from any working directory:

`python3 boundary_factorization_escape_0328/verify_boundary_certificates.py`

The portable checker requires only Python's standard library. It implements independent rational coefficient arithmetic, multiplication modulo `z^4+1`, a fresh 4-by-4 exact inversion routine, univariate polynomial gcd/division, and rational-function normalization. It imports neither SymPy nor any predecessor program.

It independently regenerates all matrix-derived source expressions for the five new certificates; checks the affine coefficient extractions and every stored Bézout identity; verifies the source positions and all denominator supports; and rejects a perturbed final Bézout identity. The separate discovery builders use SymPy but are not required for checking.

Three freshly manufactured legal **non-Fourier** inverse sums test the necessary-equation mechanism:

- `u0=0`, with other branch edges nonzero;
- `v5=v6=0`, with full first-branch edges;
- all branch edges zero, giving simultaneous zero pivots.

For each, exact dense inversion verifies `UMV=UD_y+D_xV`, all required minors, and every applicable zero-edge eliminant. Appropriate single-entry perturbations of the first two controls fail the necessary minors. These controls demonstrate that the checker is not simply rejecting every boundary matrix. They are not Fourier solutions.

The successful run reports 210 checks and approximately 12 seconds in this environment. The five certificate files total 71,655 bytes. Rational arithmetic and algebraic-coefficient representation are charged work; no constant-bit-cost or uniform root-finding claim is made.

Predecessor reports were read as text only. No supplied source program was executed, imported, or modified. All code executed in this continuation was freshly authored. This package contains its own proof artifacts and optional exploratory records. Exploration logs are not theorem evidence.

## 7. Consequences and remaining construction bottleneck

This continuation closes a specific potential escape, rather than constructing a faster Fourier transform. Combining it with the accepted nonboundary certificate excludes the full adjacent-anchor nonsingular diagonal orbit for the two specified support cycles. Together with the previously audited half-anchor obstruction, both of those anchor orbits are closed for this particular pair of remaining-factor supports.

Unresolved possibilities include a genuinely free first layer, different second-factor support pairs, and endpoint permutations not covered by the diagonal-orbit normalization. No obstruction for those broader families has been proved here. A constructive search must move outside the now-closed specified-anchor/support families.

Even a future positive fixed-size Fourier-8 factorization would not supply a growing-size FFT speedup by itself. One would still need explicit coefficient construction, all legal guards, all-output application cost, and a scalable batching/stitching procedure satisfying the global cycle grammar. Direct sums of local 8-cycles are not a single Hamiltonian global cycle. Setup, coefficient bit complexity, permutations, endpoint multiplications, and the cost of any extra terms must all be charged. No such lift or asymptotic improvement is claimed.

No novelty or prior-art claim is made.
