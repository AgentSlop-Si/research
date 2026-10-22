# Independent theoretical audit: branch-zero cross-stage slices

Scope: the 256 slices with variables on stage-0 edges `7,e0` and stage-1 edges `7,e1`, with `8 <= e0,e1 <= 23`. This is a theoretical audit, not an independent replay of the numerical certificates. No producer or historical program was executed. The candidate `PROOF.md` was not present when this note was initially written. The historical whole-branch proof and candidate source/program text were inspected as read-only data.

## Finding

The proposed implication is valid, provided the frozen original-model coefficient matrices really have the recorded full-column nonzero minors. The complete proof uses no additional domain exclusion, entry nonvanishing, root-of-unity assumption, or finite-field rootlessness inference. The correct reciprocal numerator preserves the stage order. The essential original-ideal multiplier is the square of the product of the four moving guards.

## 1. Polynomial model and coefficient ring

Let `k = Q(i)` and

`A = Z[i, (a+ib)^(-1), (a-ib)^(-1) for all 34 original Gaussian pairs]`.

Every original gain and its inverse/conjugate is a unit of A. For stage t and branch b let `h_tb` be the original holonomy, `m_tb` its variable monomial, `d_tb = 1-h_tb*m_tb`, and

`B_tb = I + W_tb + ... + W_tb^7`,
`D_t = product_b d_tb`,
`A_t = sum_b B_tb * product_(c != b) d_tc`.

The four active branch monomials are individually x0, x1, x2, x3; the other two are 1. Put `F = product of the four moving d_tb`, `Delta = D_1 D_0`, `N = A_1 A_0`, and `R = x0*x1*x2*x3`. The original two frozen guards are nonzero constants, so Delta is a nonzero constant times F.

The cycle identity `W_tb^8 = h_tb*m_tb*I` gives `N = Delta*M` on precisely the six original guards. A path of length at most seven traverses each moving edge at most once, and the other branch-guard factors use disjoint variables. Thus N is multiaffine in all four variables. Consequently

`Nt = R * conjugate(N)(x^-1)` and `H = N entrywise-multiplied by Nt`

are polynomials over A, and each coordinate degree of H is at most two. Coefficient conjugation here has no transpose.

On the unit torus, `H = R*|Delta|^2*|M|^2` entrywise. Invertible complex row/column monomial equivalence to F8 implies that `|M|^2` is a positive row factor times a positive column factor, including any permutations. Therefore every such Fourier-equivalent point has `rank(H) <= 1`. No sufficiency of this necessary condition is asserted.

## 2. Reciprocal order and polynomial pole identities

In the Laurent fraction field define dagger by coefficient conjugation, variable inversion, and transpose. Original unit gains imply `W^dagger = W^-1`. Therefore each Green inverse obeys `G + G^dagger = I`, and each three-branch stage obeys `S_t + S_t^dagger = 3I`.

Let `R_t` be the product of variables in stage t and `c_t = -1/(h_t0*h_t1*h_t2)`. Then

`R_t*conjugate(D_t)(x^-1) = c_t*D_t`,
`R_t*conjugate(A_t)(x^-1) = c_t*(3D_t*I - A_t^T)`.

Both sides of the latter are polynomials, so the cleared identity holds in A[x], not just at invertible coordinates or away from guards. In particular,

`Nt = c_1*c_0*(3D_1*I - A_1^T)*(3D_0*I - A_0^T)`.

The order is stage 1 followed by stage 0. Reversing it would be an error: the definition of Nt takes conjugation, not conjugate transpose, of N.

For any moving guard `f = 1-h*x_j`, the quotient `A[x]/(f)` is `A[all other variables]`, because h is a unit. It is an integral domain. In this quotient the active cycle has holonomy one and all its weights are units. Choosing unit vertex potentials gives

`B = u*v^T`, with `u_q*v_q = 1` for every vertex q.

Equivalently, B is the diagonal conjugate of the all-ones matrix. Its factorization can use its first column and row because `B_00 = 1`; no variable matrix entry is divided out.

At a stage-0 pole, `A_0 = kappa*u*v^T` and `D_0 = 0`, where kappa is the product of the other two stage-0 guards and is NOT assumed invertible. Hence

`N = kappa*(A_1*u)*v^T`,
`Nt = -c_1*c_0*kappa*((3D_1*I-A_1^T)*v)*u^T`.

Their entrywise product has identical columns, since `v_q*u_q = 1`. At a stage-1 pole the analogous expression has identical rows. These statements remain valid where other guards also vanish: no other guard was inverted in the quotient calculation.

## 3. Double centering and exact guard division

Let L be the 7-by-8 matrix with row r equal to `e_r^T-e_0^T`, for r=1,...,7. Then

`K = L*H*L^T`,
`K_rc = H_rc-H_r0-H_0c+H_00`.

An identical-column H gives K=0; an identical-row H also gives K=0. Thus every entry of K belongs to each of the four moving-guard ideals. These guards are prime and pairwise nonassociate (each uses its own variable). Their product therefore divides every K entry. Define the 7-by-7 polynomial matrix `E = K/F`.

Since H has coordinate degree at most two and F has degree exactly one in every variable, degree additivity over the polynomial domain gives `deg_(x_j) E_rc <= 1` for every entry and variable. The coefficients actually lie in A: sequential division by each `1-h*x_j`, whose constant coefficient is one, has coefficient recurrence `Q_e = V_e + h*Q_(e-e_j)`. This uses only A arithmetic; divisibility guarantees that the recurrence terminates. No guard is inverted in the coefficient ring.

On the original domain F is nonzero. If rank(H)<=1 then rank(K)<=1 and rank(E)<=1, so all `C(7,2)^2 = 441` minors of E vanish. This uses only the original moving guards, not an extra denominator or a nonzero anchor entry.

## 4. Relation to the original 784 minors

Write `P_(ar,bc) = H_ab*H_rc-H_ac*H_rb`, with ordered row pair a<r and column pair b<c. For 1<=a<r<=7 and 1<=b<c<=7, let T_(ar,bc) be the corresponding minor of E. Cauchy-Binet, or direct expansion, gives

`F^2*T_(ar,bc)`
` = P_(ar,bc) - P_(ar,0c) + P_(ar,0b)`
` - P_(0r,bc) + P_(0r,0c) - P_(0r,0b)`
` + P_(0a,bc) - P_(0a,0c) + P_(0a,0b)`.

Thus each `F^2*T` is in the ideal generated by the original 784 H minors. This is an exact polynomial identity, not merely a set-theoretic consequence of rank or a guard-domain argument.

## 5. Why full rank modulo 65537 lifts safely

Every T is a polynomial over A supported in the entire 81-element cube `{0,1,2}^4`, by multiaffinity of E. Let C be an 81-by-81 selected-row submatrix of the full 441-by-81 coefficient matrix, using ALL 81 columns, including the constant monomial. This complete characteristic-zero support bound is essential; projecting to an observed modular support would not suffice.

The prime p=65537 has `256^2 = -1 mod p`. If both `a+256b` and `a-256b` are nonzero for every original pair, the map `A -> F_p`, `i -> 256`, is a genuine ring homomorphism. Coefficient conjugation must be evaluated through the opposite Gaussian embedding, `i -> -256`; it is not the trivial involution of F_p. One valid embedding and one nonzero determinant per label suffice for lifting. Repeating under the conjugate embedding is useful additional control but is not logically necessary.

If the recorded determinant residue of C is nonzero, then the exact `d=det(C)` is a nonzero element of A and k. Let c0 denote the constant-monomial column. The adjugate identity is

`d = sum_j cofactor(C)_(j,c0)*T_j`.

The coefficients are exact finite determinants of specified Gaussian-rational matrices. Dividing by d in k proves `1` lies in the ideal generated by the T equations. Multiplying the unnormalized identity by F^2 and applying the nine-term formula proves `d*F^2` lies in the original H-minor ideal, equivalently `F^2` lies in that ideal over k.

At any complex point where the original H minors vanish, this forces F=0. Such a point is outside the original guarded domain. This proves the desired contradiction for arbitrary complex unit phases, not merely Gaussian-rational points, roots of unity, or finite-field points. No assertion about modular rootlessness is involved, and no map from the whole field Q(i) to F_p is presumed.

## Boundary and outstanding evidence

The theoretical conclusion covers exactly the 256 cross-stage labels once each full frozen coefficient matrix and specified determinant is independently verified. This note does not itself replay those matrices. The candidate JSON files report rank 81 for all 256 labels in each Gaussian embedding, but that report is input evidence, not independently established arithmetic here.

No conclusion follows for all four-coordinate placements, all simultaneous branch motions, the entire 34-phase fiber, other witnesses, higher dimensions, constructions, algorithms, complexity, or novelty priority. Same-stage extra-edge pilots are separate experiments and are not part of this 256-label theorem. In particular, the inspected three-branch pilot reports rank 69, so it cannot support the present full-81-column lift for that other placement.

## Final candidate-text review

The subsequently delivered `candidate/PROOF.md` was read in full. Its stage order, coefficient involution, quotient-ring pole factorization, intersecting-pole retention, four-guard divisibility, multiaffine support, nine-term Cauchy-Binet signs, adjugate cofactor indices, specialization argument, arbitrary-unit-phase scope, and non-closure qualifications agree with the proof above. Section 2 explicitly defines the original generators as the 784 H minors, resolving the potential generator-identification ambiguity. No theoretical revision is required. Arithmetic acceptance relies on the separate independently reconstructed 512 coefficient matrices and fixed-minor replays reported by the parent reviewer, not on an execution by this theory auditor.

### Frozen final-byte acceptance

Reread the complete frozen `candidate/PROOF.md` and directly verified its SHA-256 as `3b8b8fa0535988ba4922972e5ea3fc7f48ff3386fce5adc02fa0c408a94b2729`. The final text is theoretically accepted with no required revision. Its mathematical content agrees with the previously reviewed version; the final checklist now has corrected spacing. This acceptance is scoped to the 256 stated cross-stage families and the original guarded unit-phase domain. The parent reports that all 512 final independent exact modular reconstructions and fixed determinant replays pass; those arithmetic runs remain the separate review evidence.
