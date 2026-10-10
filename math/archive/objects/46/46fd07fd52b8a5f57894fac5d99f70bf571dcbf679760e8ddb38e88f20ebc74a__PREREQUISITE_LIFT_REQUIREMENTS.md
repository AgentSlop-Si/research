# What an N-to-4N coefficient lift must preserve

## Status

These are exact route and bank identities for a possible lifting rule, not a successful lift. In particular, a small route-defect rank is not Fourier coefficient compatibility. Growing rank is also not automatically a cost obstruction: the structured resolvent correction below still has an O(N) application algorithm.

Let the smaller geometry have dimensions a by b, with a=b or a=2b, N=ab, and b=m=2^r. The larger geometry is 2a by2b, of size4N. Index vertices by bx+y at the small level and2bx+y at the large level. Let pi(x,y)=(x mod a,y mod b), and let Q be its unnormalized fiber-sum matrix, so Q e_v=e_(pi(v)). Each fiber has four points.

## 1. Unspliced routes commute; spliced routes have an explicit defect

Every one of the eight labeled unspliced shear covers T commutes with pi. In H, changing a large y representative by b changes the x displacement by2b, divisible by a in both allowed aspect ratios. In V, changing x by a changes the y displacement by2a, divisible by b. Thus

    Q T_large = T_small Q.

Let P_small and P_large be the deterministic minimum-representative splices. In general they do not commute with pi. Define

    D = Q P_large - P_small Q
      = Q(P_large-T_large) - (P_small-T_small)Q.

If a cover has c cycles, its splice correction has the exact factorization

    P-T = B(R_c-I)A^T,

where A has the selected tail basis vectors as columns, B has the corresponding old head basis vectors as columns, and R_c shifts the representative indices cyclically. Thus rank(P-T)=c-1 for c>=1, including zero for c=1. This equality holds over any field because R_c-I has a one-dimensional kernel.

Consequently D has at most c_large+4c_small supported columns and

    rank(D) <= c_large+c_small-2.

The support bound is safe rather than always sharp: columns where the two corrections cancel are omitted by the exact formula. An exact defect column is e_(pi(P_large(v)))-e_(P_small(pi(v))). Its endpoints are unequal precisely when that column is nonzero.

There is a direct sparse application procedure. Scatter the changed large-level tail values to their two projected head positions; then, for each changed small-level tail, add its four input-fiber values and scatter their sum with the opposite sign to the two small heads. This costs O(c_large+4c_small) field operations and stores O(c_large+c_small) route data. It does not require a dense matrix or an abstract rank factorization.

Summing the bounds across the eight labels gives:

* Square: support at most8m(3r+7), sum of rank bounds at most4m(3r+8)-16.
* Rectangle: support at most12m(3r+8), sum of rank bounds at most18m(r+3)-16.

These sums count labels separately. They are not ranks of a block-free sum of eight operators. Both scales are O(sqrt(N) log N).

## 2. Resolvent defects, matching poles, and actual application cost

For the same scalar pole tau on both levels, define G_small=(I-tau P_small)^(-1) and G_large=(I-tau P_large)^(-1), assuming both inverses exist. Then

    Q G_large - G_small Q = tau G_small D G_large.

This follows by multiplying the identity (I-tau P_small)Q-Q(I-tau P_large)=tau D by the two resolvents. It preserves the rank bound but usually gives dense matrix entries.

Nevertheless, applying the displayed correction is O(N) in the small-level size: one4N-point Green scan, the sparse D scatter, and oneN-point Green scan. Its growing O(sqrt(N)logN) rank is not by itself a superlinear application cost or a fatal lifting obstruction. Preparation and any later use of dense low-rank cores must be accounted separately rather than presumed cheap.

For arbitrary weighted edges, the exact formula instead is

    Q (I-D_wlarge P_large)^(-1) - (I-D_wsmall P_small)^(-1) Q
      = (I-D_wsmall P_small)^(-1)
        [Q D_wlarge P_large-D_wsmall P_small Q]
        (I-D_wlarge P_large)^(-1).

The bracket has the previous sparse route structure when w_large(v)=w_small(pi(v)); then Q D_wlarge=D_wsmall Q and the bracket equals D_wsmall D. Without such a descent condition, an additional weight mismatch may have full support and full small-level rank. Both inverse guards must be retained: even if the small wrap product is not1, its fourth power can be1 in a general field.

Similarly an endpoint mask satisfies Q diag(a_large)=diag(a_small)Q exactly when a_large(v)=a_small(pi(v)). A coefficient law can use a more elaborate four-fiber decomposition, but its additional components and corrections must be supplied explicitly. The free384-parameter seed masks have no such law merely because they are diagonal.

## 3. Active bank labels and the exact folding mismatch

To preserve active versus inactive labels under pi, use

    J_large = J_small union (J_small+a).

At the proposed seed, J_small={0,1} among four blocks; this rule makes J_large={0,1,4,5} among eight blocks. Keeping a contiguous first half instead would not be the pullback of the old active pattern.

Even with this correct label pullback, the active Fourier matrices do not commute with simple fiber summation. Let Q_plus=[I_m I_m], Q_minus=[I_m -I_m], and let E_even,E_odd select coordinates2t and2t+1, respectively. With the unnormalized Fourier convention and omega a primitive2mth root, put zeta=omega^2 and D_twiddle=diag(omega^r), 0<=r<m. Exact entrywise identities are

    Q_plus F_(2m) = 2 F_m E_even,
    Q_minus F_(2m) = 2 D_twiddle F_m E_odd.

The signs and factor2 follow from omega^((r+m)j)=(-1)^j omega^(rj). This is the ordinary two-channel Fourier identity. It must be included in a coefficient lift; the assertion Q_plus F_(2m)=F_m Q_plus is false.

The one-channel discrepancy factors as

    Q_plus F_(2m)-F_m Q_plus = F_m S_m,
    S_m = 2 E_even-Q_plus.

For dyadic m and characteristic different from2, S_m has full row rank m. To see this, restrict to its even columns: the resulting matrix is2I-R, where R e_t=e_(2t mod m). If u^T(2I-R)=0, then u_(2t mod m)=2u_t. At t=0, u_0=0; after log2(m) doublings every t reaches0, forcing u_t=0. Thus the minor is nonsingular. Its determinant is2^(m-1), since R has eigenvalues1 and0 with the latter of algebraic multiplicity m-1.

Globally, for every active small block the difference Q B_large-B_small Q contains F_m S_m applied to each of its two x-child blocks. Inactive blocks contribute zero. The child blocks have disjoint supports between different small blocks. Therefore, with matched active labels,

    rank(Q B_large-B_small Q)=m |J_small|.

At a half-active bank this is N/2. This is an exact obstruction to **naive one-channel bank descent**, not to a four-channel lifting construction. Its selector core is sparse, and the two-channel identities above give the specific correction a successful coefficient law must organize. The rank statement alone is not an arithmetic lower bound.

## 4. The concrete lifting problem

A valid lift must supply all of the following simultaneously:

1. The deterministic route correction or an alternative compatible splice rule, without silently replacing the fixed geometry.
2. A coefficient law for every one of24 Green occurrences and its endpoint masks, including any four-fiber components and inverse/nonzero guards.
3. The pulled-back active set and the exact even/odd bank channels, twiddle factors, signs, and normalizations.
4. The full Fourier identity at4N, or all4N seed equations plus4N(4N-1) successor equations. A product-group route quotient alone does not imply the cyclic Fourier transform's coefficient law.
5. An explicit recurrence and operation ledger for coefficient generation, route preparation, bank work, and applying every correction. O(N) application of an already supplied correction does not generate the coefficients.

The bounded seed gate should be used to test proposed structured coefficient laws against these requirements. It should not become an indefinite search for isolated finite-size fits without an identified lift.

## 5. A no-go for literal pullback of every coefficient

Suppose an alternative hierarchical route rule makes Q P_large=P_small Q exactly. Suppose scalar poles are the same at both levels, every endpoint mask is literally pulled back, and the same eight terms occur in each corresponding layer. Then Q H_(l,large)=H_(l,small)Q. If both levels exactly realized the unnormalized Fourier target with the bank placement above, one would have

    Q F_(4N)-F_N Q
      = H_(3,small)H_(2,small)
        (Q B_large-B_small Q) H_(1,large).

All exterior factors here are invertible. Hence the rank of the Fourier defect would have to equal m|J_small|.

But the Fourier defect has full row rank N for any four-to-one equal-fiber Q. Indeed QQ*=4I, F_(4N)F_(4N)*=4N I, and F_N F_N*=N I. Thus for every row vector u,

    ||u Q F_(4N)||=4sqrt(N)||u||,
    ||u F_N Q||=2sqrt(N)||u||,
    ||u(Q F_(4N)-F_N Q)||>=2sqrt(N)||u||.

Therefore a proper active bank (|J_small|<a) makes this literal coefficient-copying law impossible. In particular the half-active seed cannot lift by simply repeating all endpoint coefficients on their four fibers, even if the route quotient is repaired perfectly.

This conclusion depends on the exact unnormalized Fourier convention and the unit multiplicative scaling in the assumed coefficient law. It is not a statement about unitary-normalized Fourier matrices: F_N/sqrt(N) and F_(4N)/(2sqrt(N)) have equal row norms after the respective Q multiplications, so the displayed norm-gap proof disappears. It does not exclude level-dependent scalar rescaling, extra fiber channels, or a different coefficient law. A global rescaling gamma would replace the Fourier defect by QF_(4N)-gamma F_NQ; the norm argument alone proves full rank only when |gamma| is not2. The route/bank correction identities remain useful constraints rather than a general exclusion.

## 6. Exact controls

`check_lift_defects.py` and `LIFT_DEFECT_CONTROLS.json` check96 labeled route lifts (both aspect ratios, m2 through64), cover commutation, actual splice defects, support/rank bounds, sparse scatter equality, same-pole resolvent identities, and compatible nonconstant weights and endpoint masks at the smaller sizes. The bank identities are checked entrywise for m1 through256, including both signs, both selector channels, all scale factors, and the exact even-column determinant2^(m-1). Five full bank-folding matrices, through N64, have rank exactly the active mass. These are controls for the proved identities, not a successful coefficient lift.
