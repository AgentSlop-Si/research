# Q2 dense torus: a paid inverse and guarded numerical solve

Date: 16 October 2026. Source baseline: `AgentSlop-Si/research`, commit `de5dc664448d8e3e219df9651b2805d5a2cecbb1`.

## Result and exact stopping boundary

This is a new inverse analysis of the **actual fixed Q2 family**, not a repetition of its accepted forward-executor audit.

1. There is an exact inverse executor with **O(N^(3/2)) cold setup, O(N) work per fresh right-hand side, and O(N) storage**, in the supplied-root exact-scalar model. Its explicit warm ledger is **32N+sqrt(N)** scalar operations, plus linear copying/addressing work.
2. The new cyclic boundary system has dimension sqrt(N), and complex spectral condition number at most **5/3**. The middle sparse operator has condition number at most **3**. These are bounds on the newly exposed intermediate systems, not just the final transform.
3. A cold, normwise approximate inverse has **O(N+sqrt(N)b)** exact-scalar work for relative 2-norm error at most 2^(-b). It avoids building a dense boundary table.
4. A separate, completely specified sparse stationary iteration gives a **finite-word normwise error theorem**, with O(N(b+1)) scalar floating operations and O(N) storage. Root/coefficient preparation, precision, and exponent assumptions are explicit below. This is a new numerical executor; it does not validate the archived forward implementation.
5. The original scalar boundary collapse does **not** transfer to the inverse. An exact rational counterexample at m=2 proves this for the fixed schedule. It is a limitation of that shortcut, **not a lower bound against every cold O(N) inverse algorithm**.

**Remain open:** exact cold O(N) inversion; all-m entrywise nonvanishing of the inverse; historical-code validation; sharp exact-bit complexity; production/fixed-hardware and entrywise-relative guarantees; exact predecessor/novelty clearance; and the original uniform Fourier objective. No parent closure or priority reduction follows.

## 1. Source and notation

The original THEOREM.md is bound by SHA256 `ff6f36d2da31a41058eeec1fef664930b711ed31a39a338f9c514dcfc550d7f6`. The independent audit ZIP at the pinned repository commit has Git blob `01d919b2fbfa2ec6109ca57e0efcd46eeac1a95e` and SHA256 `99d9912103e7914a658100bee2fb106eba0fca1fabf1dbfedfcb6c99598fdb59`. These bindings were independently checked against the local bytes and the pinned Git tree. Full original theorem, PRIOR_QTGF.md, and independent written audit were read. No supplied scientific program was imported or run.

Fresh native owner reads on 16 October confirmed that Research overview row 111 / Incoming queue row 45 designate the guarded forward theorem complete, the parent open, and a separately paid inverse or finite-word question as a valid new scope. The private live snapshots are not part of the publication files.

For m>=2, N=m², let q be any primitive complex m-th root. On Z_m² put

    (A v)[a,c] = v[a-1,c]
    (B v)[a,c] = q^a v[a,c-1]
    L = I - (A+B)/4.

Let phi(a,c)=(-c,a+c), P e_x=e_phi(x), M=P^(-1)LP, G=L^(-1), H=M^(-1), and

    ell = 4 + m ceil(log2(2m)), lambda=2^(-ell),
    S = L^(-1) + lambda M^(-1).

All coordinates are reduced modulo m. The canonical exact coefficient field can be Q(omega_N), or any exact characteristic-zero extension containing the supplied root. All prepared entries remain in that field; an arbitrary fresh input is acted on linearly over the chosen scalar field. Norm and conditioning assertions use its specified complex embedding. The accepted complex bounds are ||L||₂,||M||₂ <=3/2, ||L^(-1)||₂,||M^(-1)||₂ <=2, lambda<=1/256, and ||S||₂<=2+2lambda. The earlier row solver's two guards are preserved; they are not silently assumed for arbitrary finite-field reductions.

## 2. A noncommutative factorization with the correct order

Set K=M+lambda L. Direct multiplication, without commuting L and M, gives

    S = L^(-1) K M^(-1),
    S^(-1) = M K^(-1) L.                         (1)

Thus the inverse problem is one sparse solve with K, surrounded by two sparse matrix-vector products. It is not enough to write (1) and charge K^(-1) as a unit-cost primitive.

The conjugated shifts act as

    (A' v)[a,c] = v[a-1,c+1],
    (B' v)[a,c] = q^(-c) v[a-1,c].

These follow directly from phi^(-1)(x,y)=(x+y,-x) and the source convention P e_x=e_phi(x). In particular the q-phase is q^(-c), with no extra q^a factor. Therefore

    (K y)[a,c] = (1+lambda)y[a,c]
                -lambda q^a y[a,c-1]/4
                -[y[a-1,c+1]+q^(-c)y[a-1,c]+lambda y[a-1,c]]/4.   (2)

## 3. Exact cyclic-row reduction

On a row, let (U v)[c]=v[c-1], Q=diag(q^(-c)), and define

    s=1+lambda, t=lambda/(4s),
    D_a=s(I-t q^a U),
    R=(U^(-1)+Q+lambda I)/4,
    T_a=D_a^(-1)R.

Equation K y=g is precisely

    y_a = D_a^(-1) g_a + T_a y_(a-1).             (3)

The inverse of D_a is computed by a length-m first-order cyclic recurrence, not by a dense row inverse. Since (t q^a)^m=t^m, its denominator is 1-t^m, shared by all rows. Over C, 0<t<1/4, so s and 1-t^m are units.

A concrete D_a solve for v is:

1. Form h=v/s.
2. Starting z=0, scan c=0,...,m-1 using z=h_c+(t q^a)z.
3. Set the cyclic preceding value b=z/(1-t^m).
4. Repeat the scan, starting with b, retaining every output.

This costs 5m+1 additions/multiplications after shared reciprocal setup. Rv costs 5m. For a general field, the route must explicitly check s !=0, 1-t^m !=0 and invertibility of the boundary matrix below; analytic complex contraction cannot justify those guards in a finite field.

Let

    E=T_(m-1)...T_0,  F=I-E.

A sweep of (3) from preceding boundary b produces last row p+E b, where p is the last row obtained from zero boundary. Hence the true cyclic boundary satisfies

    F b=p.                                      (4)

After solving (4), a second sweep reconstructs all y. Formula (1) then gives the desired output.

## 4. Conditioning of every newly exposed system

Each U,Q,A,B,A',B' is unitary. Therefore

    ||D_a^(-1)||₂ <= 1/(s-lambda/4)=1/(1+3lambda/4) <=1,
    ||R||₂ <= (2+lambda)/4,
    ||T_a||₂ <= tau=(2+lambda)/(4+3lambda) <1/2.

Consequently

    ||E||₂ <= tau^m <=1/4,
    ||F^(-1)||₂ <=1/(1-tau^m),
    kappa₂(F) <=(1+tau^m)/(1-tau^m) <=5/3.        (5)

The same rowwise bounds hold in induced infinity norm, since the row shift and diagonal phases have infinity norm one. In particular F is strictly row diagonally dominant over C. Exact Gaussian elimination with pivoting is nevertheless allowed in the executor; the field proof needs only invertibility.

Write

    C=(A'+B'+lambda A+lambda B)/(4s).

Then K=s(I-C) and ||C||₂<=1/2. Thus

    sigma_min(K)>=s/2, ||K||₂<=3s/2, kappa₂(K)<=3.   (6)

Neither (5) nor (6), by itself, certifies a particular floating-point implementation. Section 8 supplies its own explicit numerical algorithm and rounding argument.

## 5. Paid exact cold setup and warm executor

To prepare E, apply the homogeneous row sweep to every row basis vector e_j, j=0,...,m-1. Each application traverses m rows and takes O(m²)=O(N) scalar work. Assemble F=I-E, and store a pivoted LU factorization of the m-by-m F. This costs O(m³) additional work and O(m²) storage.

This setup is **paid**, not an oracle or a free precomputed coefficient table:

- Supplied-root preparation: q=omega_N^m and q^a table, O(m) exact scalar multiplications by straightforward repeated products.
- ell and lambda: integer doubling for ceil(log2(2m)); ell repeated halvings, O(m log m) exact scalar operations. Word indexing uses O(log N)-bit words.
- Row coefficients and shared denominators: O(m) scalar work, including t^m and divisions.
- Monodromy E: exactly 10m³+m² scalar additions/multiplications in the specified implementation, after coefficients are prepared.
- Form F: m² subtractions.
- Exact LU: m(m-1)/2 divisions and m(m-1)(2m-1)/3 multiplications/subtractions, plus O(m³) comparisons/indexing if a naive pivot-search implementation is used.
- Storage and address maps: O(N) words/scalars.

For each fresh vector f, compute g=Lf, obtain p with the zero-boundary sweep, solve Fb=p using the saved factorization, reconstruct y with a second sweep, and output My. The explicit scalar ledger is

    Lf and My:                 8N
    two inhomogeneous sweeps: 22N+2m
    two triangular solves:     2N-m
    total:                    32N+m.            (7)

Copies, permutations, input reads, output writes, and address calculations add O(N), not zero. The total for r right-hand sides is O(N^(3/2)+rN). The O(N) per-vector claim is a **warm** claim. Even for one input, its full cold cost remains O(N^(3/2)). Exact cyclotomic field operations are not assigned unit *bit* cost.

## 6. A rigorous limitation of the old scalar-boundary shortcut

At lambda=0, the old root-of-unity mechanism can collapse a monodromy to a scalar. At the actual fixed lambda it cannot simply be copied to (3).

For m=2, q=-1, lambda=1/256, evaluate the two-by-two row matrices exactly over Q. The (0,1) entry of E=D_1^(-1)R D_0^(-1)R is

    E[0,1] = 58141184 / 159541472727 !=0.         (8)

The complete rational matrix is retained in EXACT_RESULTS.json and is independently reconstructed by check_inverse.py. Thus E is not scalar already for the smallest actual family member. A purported uniform inverse proof that replaces F by a scalar using the forward audit's identity is false.

Equation (8) does not prove E lacks some other fast representation, does not prove an Omega(N^(3/2)) lower bound, and does not exclude a different cold linear-work inverse. The residual exact problem is now concrete: prepare/apply F^(-1) (or solve K by another route) with total cold O(N), with all coefficient generation and addressing paid.

## 7. Cold approximation using the small boundary monodromy

This section counts exact scalar operations but permits a controlled approximation to S^(-1)f. For k>=1, approximate the boundary by

    b_k = sum_(j=0)^(k-1) E^j p.

No E matrix is materialized: each E application is one homogeneous row sweep of O(N) work. A final inhomogeneous sweep uses b_k as the boundary. Because b-b_k=E^k b,

    ||b-b_k||₂ <=tau^(mk)||b||₂.

For the zero-boundary sweep, Cauchy-Schwarz over the m row blocks yields

    ||p||₂ <= ||g||₂/sqrt(1-tau²) <=2||g||₂/sqrt(3),
    ||b||₂ <=4||f||₂/sqrt(3).

An error delta in the preceding boundary contributes row errors bounded by tau^(a+1)||delta||₂. The concatenated reconstruction error is at most ||delta||₂/sqrt(3); applying M costs at most another factor 3/2. Therefore, writing x=S^(-1)f,

    ||x_k-x||₂ <=2 tau^(mk)||f||₂,
    ||x_k-x||₂/||x||₂ <=4(1+lambda)tau^(mk) <5*2^(-mk).  (9)

For f=0 output zero. For f!=0 and integer b>=0, take k=ceil((b+3)/m). This gives relative 2-norm error below 2^(-b). Zero-boundary setup, k-1 monodromy applications, and final reconstruction cost O(N(k+1))=O(N+sqrt(N)b), with O(N) storage and the already charged O(N) coefficient preparation.

This is not an exact inverse: a finite Neumann truncation is not an algebraic inverse merely because its residual is small. Section 7 does not by itself prove finite-word stability of the row implementation.

## 8. A fully specified finite-word normwise theorem

To avoid silently assuming row- or LU-solver stability, use a separate direct sparse iteration. It operates on the same actual K and returns the same inverse target.

    h = Lf/s
    y_0 = 0
    y_(j+1) = h + C y_j,  j=0,...,k-1
    x_k = M y_k.                               (10)

Every C application is the explicitly written weighted sum of four unitary monomial maps. L and M each have three terms. No dense solve, transform, or spectral oracle occurs in (10).

### Rounding model and concrete kernel costs

Let u be a complex-operation roundoff bound: each multiplication has error at most u|z||w|, each division by a nonzero scalar has error at most u|z/w|, and each addition error at most u(|z|+|w|). Conventional correctly rounded real arithmetic implements these bounds with u a fixed constant multiple of its real unit roundoff; the only divisions needed in (10) are preparation of real nonzero scalar coefficients. Every stored nonzero coefficient has relative error at most delta; phase coefficients are nonzero and unit-modulus before their real weights.

For a sum of at most five coefficient-times-input terms, sequential multiplication/addition gives the componentwise absolute-error bound

    e sum_i |c_i v_i|,  e=(1+delta)(1+u)^5-1.

This follows by propagating each individual product error through at most four subsequent additions. The Euclidean norm of a monomial permutation of |v| equals ||v||₂. Triangle inequality therefore gives kernel errors <=(3/2)e||v||₂ for L and M, <=e||v||₂ for scaling by 1/s, and <=e(||h||₂+||y||₂) for h+Cy. With eta=2e, all these are bounded by eta times the stated norm sums. Each kernel uses a fixed number of real floating operations per coordinate.

Assume eta<=1/16; adequate exponent range prevents overflow/underflow; and f is the represented input (input quantization, if any, is a separate initial perturbation). Compute h by the two stated kernels, retaining the rounded h for every iteration. Then

    ||h_hat-h||₂ <=3eta||f||₂,   ||h_hat||₂<=2||f||₂.

Writing each update as h_hat+C y_hat+r, its local error satisfies

    ||r||₂ <=eta(||h_hat||₂+||y_hat||₂).

Since ||C||₂<=1/2, induction gives ||y_hat_j||₂<=3||h_hat||₂<=6||f||₂. For the exact fixed point y_star_hat=(I-C)^(-1)h_hat, the error recurrence and a geometric sum give

    ||y_hat_k-y_star_hat||₂ <=4*2^(-k)||f||₂+16eta||f||₂.

The error in h moves its fixed point by at most 6eta||f||₂. The final M multiplication adds at most 6eta||f||₂, and ||M||₂<=3/2. Combining these bounds,

    ||x_hat_k-S^(-1)f||₂ <=[6*2^(-k)+39eta]||f||₂,
    ||x_hat_k-S^(-1)f||₂/||S^(-1)f||₂
        <=20*2^(-k)+120eta.                     (11)

The second line uses ||S||₂<3 and slightly enlarges constants. The proof is independent of k and m except through the explicitly prepared coefficient error eta. In particular roundoff does not receive an unproved k- or m-fold amplification factor inside the iteration.

Choose k=b+6 and eta<=2^(-b)/256. Then (11) is strictly below 2^(-b). Thus a stable normwise b-bit inverse costs O(N(b+1)) floating scalar work and O(N) storage, plus O(N) coefficient preparation. This proves a **new executor theorem**, not stability of the historical source code.

### Root precision, lambda and bit costs are not free

For the original supplied primitive N-th-root interface, request a numerical approximation omega_hat with absolute error at most the working u. Generate powers through N by repeated multiplication and retain the entries omega_hat^(ma) needed for q^a. Under Nu<=1/1024, each phase error is at most (1+u)^(2N)-1<=4Nu. Form lambda as the exact binary value 2^(-ell). Computing s=1+lambda and its reciprocal incurs relative weight error at most (1+u)/(1-u)-1<=3u; scaling by 1/4 or lambda is exact binary exponent scaling when the stated exponent assumption holds. Multiplying these weights by stored phases and rounding adds at most one further factor 1+u. Thus every nonzero coefficient has relative error at most (1+4Nu)(1+3u)(1+u)-1, bounded conservatively by delta=64Nu. This gives eta=2[(1+delta)(1+u)^5-1]<=256Nu when 64Nu<=1/16. The hypotheses hold for the precision choice below.

Taking working complex precision p with u<=2^(-p) and

    p >= b + ceil(log2 N) + 20

therefore suffices for the eta requirement above; real floating arithmetic needs only a further fixed number of guard bits. If q itself is supplied to working precision, log2 N can be replaced by log2 m in this table-generation argument. Production of a certified primitive root from no supplied root is outside the accepted model and is **not claimed free**.

The exact lambda has ell=Theta(m log m) binary places as a fixed-point rational, although a floating significand/exponent representation stores it with a short significand and O(log ell) exponent bits. A fixed hardware exponent range is not assumed: sufficiently large m can underflow lambda and destroy exact density even while a normwise approximation remains accurate. Input exponent range and intermediate exponent range must likewise be supported, or explicitly rescaled with a separately verified implementation.

At mantissa length p, the arithmetic bit cost is O(N(b+1) M(p)) plus exponent/address handling, where M(p) is the chosen p-bit multiplication cost; it is not O(N) bit work. Addresses take O(log N) bits, and exponent operations must be charged at their actual bit length. This result does not bound exact cyclotomic coefficient-height growth, provide a fixed-machine performance claim, or guarantee relative accuracy in every tiny output coordinate/entry.

## 9. Fresh exact checks

The new standard-library-only check_inverse.py was written for this report. It executes no supplied program and imports no project implementation. It constructs source L directly and M via explicit permutation conjugation, obtains a deliberately expensive independent dense inverse of S, and compares every output basis vector with the new paid inverse.

At m=2,3,4,5,6,8 over the independently checked prime 14401, all **154 basis solves** pass exact residual and independent dense-inverse comparisons. Primitive N-th-root and m-th-root orders, the exact relation q=omega_N^m, row units, boundary factorization, the noncommutative factor order, and the explicit orientation formula are checked. The warm count is exactly 32N+m in every case. All six finite-field monodromies are nonscalar; the characteristic-zero m=2 statement rests on the separate exact rational computation (8), not on extrapolation from those controls.

The dense test oracles are excluded from the executor ledger. These finite checks corroborate the all-m analytic/algebraic proof; they do not replace it. The floating theorem is a rounding analysis, not a claim that an arbitrary floating implementation or archived code was tested.

## 10. Gate dispositions

| Question | Disposition from this report |
|---|---|
| Accepted Q2 forward density/conditioning/exact executor | Preserved; not reopened or recounted |
| Exact inverse with fully paid cold/warm ledger | New proved candidate: O(N^(3/2)) cold, O(N) warm, O(N) storage |
| Conditioning of new sparse and boundary systems | New proved candidate: kappa₂(K)<=3, kappa₂(F)<=5/3 |
| Cold normwise approximate inverse | New proved candidate: O(N+sqrt(N)b) exact scalar work |
| Finite-word normwise inverse | New guarded theorem for explicit iteration (10), O(N(b+1)) floating work at charged precision |
| Reuse of the forward scalar-boundary shortcut for the inverse | Refuted for actual m=2 schedule |
| Exact cold O(N) inverse | OPEN; no universal lower bound asserted |
| All-m dense inverse support | OPEN; unnecessary for applying the inverse |
| Historical-source implementation and forward floating stability | OPEN / outside this new executor theorem |
| Sharp exact bit complexity, fixed-hardware robustness, entrywise relative accuracy | OPEN |
| Exact primary-source predecessor / worldwide priority | OPEN; no novelty claim |
| Uniform exact fast DFT / parent row | OPEN; unchanged |

These are author-side proof/test findings pending independent review. “New” means newly developed for this Q2 work product; the cyclic reduction, Neumann series, and rounding arguments are elementary ingredients, and literature priority has not been investigated or established. The report justifies a bounded inverse result, not an automatic source-register acceptance or parent closure. No repository or spreadsheet content was modified.

## Source link

[Pinned original independent-audit archive](https://github.com/AgentSlop-Si/research/blob/de5dc664448d8e3e219df9651b2805d5a2cecbb1/math/reviewed_rounds/2026-10-13-reviewed-1517/archives/Q2_Dense_Torus_Independent_Theorem_Audit_2026-10-13.zip).
