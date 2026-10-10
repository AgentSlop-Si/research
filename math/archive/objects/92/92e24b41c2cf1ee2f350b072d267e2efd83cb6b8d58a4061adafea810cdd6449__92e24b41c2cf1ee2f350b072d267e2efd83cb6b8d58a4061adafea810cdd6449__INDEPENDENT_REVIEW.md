# Independent review: route lifting, active-bank folding, and the N16 gate

9 October 2026 UTC. This checkpoint reviews the construction track's seed and lifting proposals, including its subsequently communicated quotient-compatible splice variant. The proofs and standard-library checker here were independently reconstructed; no constructor or uploaded program was executed. The three earlier sealed reviews are unchanged. No publication-priority claim is made.

## Verdict

Accepted, with the following boundaries:

1. The original independently spliced routes have the stated sparse quotient defect and resolvent identity. Their correction is linear-time to apply with coefficients supplied, despite potentially growing rank.
2. Active Fourier banks do not descend by naive one-channel fiber summation. The exact even/odd formulas and full-rank discrepancy are correct; their Fourier work remains charged.
3. A **new hierarchical splice family** can preserve exact route quotients and the large-size balanced-cut capacity guarantee. It changes the splice rule and does not supply a coefficient lift from N16.
4. The N16 all-ones inner prefix is rigorously excluded. The full 384-parameter branch remains open. Generated-product controls validate the full-entry verifier, not a Fourier construction.
5. Exact unnormalized literal coefficient copying across the four-fiber quotient cannot give Fourier identities at both levels with a proper active bank. This normalization-sensitive no-go does not cover general rescaled or four-channel coefficient laws.

## 1. Conventions and unspliced descent

Let the small vertex set be `Z_a x Z_b`, `a=b=m` or `a=2b=2m`, with `N=ab` and dyadic `m>=2`. Number vertices by `bx+y`. The large level is `Z_(2a) x Z_(2b)` with `4N` vertices. Put

`pi(x,y)=(x mod a,y mod b)`, `Q e_v=e_pi(v)`.

Thus Q is the unnormalized four-fiber sum. For each sign and c=0,1, use the covers `H(x,y)=(x±(2y+c),y)` and `V(x,y)=(x,y±(2x+c))`, reduced in the appropriate moduli.

Changing a lifted y by b changes the horizontal displacement by 2b, divisible by a in either allowed aspect ratio. Changing a lifted x by a changes the vertical displacement by 2a, divisible by b. Therefore every labeled cover satisfies `Q T_large=T_small Q`.

## 2. Original minimum-representative splice defects

Let P_small and P_large be the independently computed minimum-representative Hamiltonian splices. Define

`D=Q P_large-P_small Q`

` =Q(P_large-T_large)-(P_small-T_small)Q`.

For a cover with c cycles, let A select the chosen tails and B select their old heads. Rotating the selected heads gives

`P-T=B(R_c-I)A^T`.

A and B are injections and the cyclic difference `R_c-I` has rank c-1 over any field. Hence `rank(P-T)=c-1`, including rank zero at c=1.

If the small and large cover counts are c_s,c_l, then D has at most `c_l+4c_s` supported columns and rank at most `c_l+c_s-2`. Its actual v-th column is

`e_pi(P_large(v))-e_(P_small(pi(v)))`.

This gives an explicit sparse scatter procedure, rather than assuming a cheap abstract rank decomposition. Across all eight labels, the safe support and sum-of-rank bounds are respectively

- square: `8m(3r+7)` and `4m(3r+8)-16`;
- rectangle: `12m(3r+8)` and `18m(r+3)-16`,

where r=log2(m). These follow by substituting the exact small and large cover counts from the earlier review. They count labels separately, not the rank of an unlabeled sum. The scale is `O(sqrt(N) log N)`.

## 3. Resolvent identity, weights, and costs

For the same scalar tau and both inverses defined, put `G_s=(I-tau P_s)^-1`, `G_l=(I-tau P_l)^-1`. Multiplying

`(I-tau P_s)Q-Q(I-tau P_l)=tau D`

on the two sides by the appropriate inverses proves the full rectangular matrix identity

`Q G_l-G_s Q=tau G_s D G_l`.

Its sign is positive. Applying the correction takes a 4N-point cyclic Green scan, a sparse D scatter, and an N-point Green scan, hence O(N) field operations and O(N) storage with coefficients supplied. The scans include ordering, writes, and inverse guards. This does not assert constant rank or O(N) exact bit cost.

For head-weighted successors `W=D_w P`, the exact identity instead contains

`Q G_l-G_s Q=G_s [Q D_wl P_l-D_ws P_s Q] G_l`.

The bracket reduces to `D_ws D` if and only if the stated sufficient fiber descent law is supplied: `w_l(v)=w_s(pi(v))`, which gives `Q D_wl=D_ws Q`. Without that law, the remaining weight mismatch can have full support and full small-level rank. Similarly, `Q diag(a_l)=diag(a_s)Q` holds exactly when the endpoint values are fiber-constant with those descended values. Diagonality by itself is insufficient.

Both inverse guards must be checked. For Hamiltonian cycles they are `1-tau^N!=0` and `1-tau^(4N)!=0`. For descended arbitrary weights, the large total product is the fourth power of the small product, so a valid small inverse does not ensure a valid large inverse. The checker includes an explicit primitive-4N-th-root counterexample to that inference.

These identities concern all entries of an N-by-4N operator. The controls compare every entry, not selected columns.

## 4. Active banks: correct labels, channels, and discrepancy rank

Let the small active block set be J. Its correct pullback is `J_l=J union (J+a)`. In particular, `{0,1}` among four small blocks lifts to `{0,1,4,5}` among eight, not to the first four consecutive blocks.

Use unnormalized Fourier matrices, a primitive 2m-th root omega, and `Q_+=[I_m I_m]`, `Q_-=[I_m -I_m]`. If E_even and E_odd select the corresponding coordinates, direct entry comparison gives

`Q_+ F_(2m)=2 F_m E_even`,

`Q_- F_(2m)=2 diag(omega^r) F_m E_odd`.

The factor two comes from adding or subtracting rows whose entries differ by `(-1)^j`; the twiddle belongs only to the odd channel. The naive assertion `Q_+F_(2m)=F_m Q_+` is false.

Its discrepancy is `F_m S_m`, where `S_m=2E_even-Q_+`. On even columns, S_m restricts to `2I-R`, where `R e_t=e_(2t mod m)`. Every nonzero index reaches zero after repeated doubling modulo dyadic m. Thus R has one eigenvalue one and the rest zero, and

`det(2I-R)=2^(m-1)`.

Equivalently, the left-kernel equation `u_(2t mod m)=2u_t` forces u_0=0, then every u_t=0. Over characteristic different from two, with the required roots present, S_m has row rank m.

The global bank discrepancy has one independent such block for every active small x block, with two x-child input copies. Different small blocks have disjoint supports, and inactive blocks cancel. Consequently

`rank(Q B_l-B_s Q)=m|J|`,

equal to N/2 for a half-active bank. This excludes naive one-channel descent only. The selector core is sparse, but application still includes the active F_m bank work; the route correction's O(N) cost must not be transferred to this Fourier computation without a separate algorithm and budget.

## 5. New hierarchical splice family with exact route descent

This section reviews a new construction, not an identity satisfied by the original independent minimum-representative splices.

Suppose P_s is a Hamiltonian small permutation and T_s its labeled MGG cover. Put `eta=P_s T_s^-1`. If P_s differs from T_s at h_s tails, eta is nontrivial at exactly h_s heads. Lift eta to the large level by applying it to the projected base coordinate and preserving the two binary fiber coordinates. Call the lift eta_hat. It satisfies `pi eta_hat=eta pi` and has exactly 4h_s nontrivial positions.

Then `P_l^0=eta_hat T_l` is a permutation satisfying `pi P_l^0=P_s pi` and differs from T_l at exactly 4h_s tails. Every cycle of P_l^0 projects around the entire small Hamiltonian cycle, so its length is a multiple of N. As there are 4N vertices, it has at most four cycles.

In each such cycle choose one tail projecting to the same fixed base vertex, for example zero. All their old heads project to P_s(0). Rotate those heads between the cycles. This merges them into a Hamiltonian P_l without altering the quotient identity. At most four further edges change, giving

`pi P_l=P_s pi`, `h_l<=4h_s+4`.

For any two permutations, restricting to tails where they disagree preserves the multiset of heads, because the maps agree everywhere else. The half-loss argument from the earlier review therefore still applies: changing h tails can reduce any cut's incoming count by at most floor(h/2). It is not necessary for this second construction to be the original cover-cycle splice.

Across eight labels, total edits obey `H_l<=4H_s+32`, so a valid loss bound D obeys `D_l<=4D_s+16`. After ell lifts,

`D_ell<=4^ell D_0+(16/3)(4^ell-1)`.

Using the original canonical bank at the odd seed `N_0=2^17,D_0=7936`, the rational capacity margin is

`3N_ell/16-3D_ell >= 752*4^ell+16>0`.

At the even seed `N_0=2^18,D_0=11264`, it is at least

`15344*4^ell+16>0`.

Together with the previously established MGG spectral premise and `sqrt(2)<17/12`, this retains three-bank common-subset balanced-cut capacity strictly greater than N_ell/2. The two seed parities cover every dyadic size at least 2^17. Exact route descent additionally gives `QG_l=G_sQ` for compatible scalar poles and valid inverse guards.

Each level costs linear work in its vertex count: build eta and its lift, walk all cycles, merge at most four, and enumerate the resulting order. Summing geometric sizes costs O(N) at the final size, including the seed construction. Storage is O(N) words. The finite checker tests this construction from small square and rectangular seeds; the all-size capacity guarantee uses the stated large seeds and the proved recurrence, not extrapolation from those small tests.

This new family does not provide a coefficient law from the N16 seed. It does not eliminate the active-bank folding discrepancy or the endpoint/weight descent obligations. Nor does it certify arbitrary multi-stage separators or attained cross-ranks.

## 6. Separate no-go for unnormalized literal coefficient copying

Assume the new route family descends exactly and every pole, weight, and endpoint coefficient is copied by the literal fiber-descent laws, so that each entire layer obeys `Q H_l,large=H_l,small Q`. Suppose the products at both sizes are exactly the unnormalized Fourier matrices in the fixed layout `C=H3 H2 B H1`.

Then a full matrix subtraction factors as

`Q F_(4N)-F_N Q = H3,small H2,small (Q B_large-B_small Q) H1,large`.

All surrounding square H factors are invertible: each is a factor of an invertible full Fourier product with an invertible bank. Therefore the left-hand rank would equal the bank-discrepancy rank `m|J|`.

Over the complex numbers, however, `QQ*=4I`, `F_N F_N*=NI`, and `F_(4N)F_(4N)*=4NI`. Thus the row singular values of `QF_(4N)` are all `4sqrt(N)`, whereas those of `F_NQ` are all `2sqrt(N)`. For every nonzero row test vector u, the reverse triangle inequality on the adjoints gives

`||(QF_(4N)-F_NQ)*u|| >= 2sqrt(N)||u||>0`.

The Fourier discrepancy consequently has full row rank N. If J is a proper subset of the a blocks, `m|J|<N`, contradiction. This excludes the exact unnormalized literal-copy law at any such pair of levels, including a half-active bank.

Normalization is essential. For targets `alpha_large F_(4N)` and `alpha_small F_N`, the two row norms become `4|alpha_large|sqrt(N)` and `2|alpha_small|sqrt(N)`. When `|alpha_small|=2|alpha_large|`, this norm-gap proof has no force. Unit-normalized Fourier targets have precisely that relation. Likewise, level-dependent scalar factors in a modified descent law can change the comparison. No conclusion about those laws follows merely from this argument; genuine four-fiber coefficient laws remain open. The high rank of the bank discrepancy is itself not an arithmetic lower bound.

## 7. Exact N16 seed model and fixed-prefix rejection

At N16 use the constructor's fixed labeling `4x+y` and label order `H0-,H0+,H1-,H1+,V0-,V0+,V1-,V1+`. Let `tau_j=1/(j+2)` and `G_j=(I-tau_j P_j)^-1`. The rational guards `1-tau_j^16` are nonzero. Put

`B=diag(F4,F4,I4,I4)`,

`H_l=sum_j diag(a_(l,j)) G_j`, `C=H3 H2 B H1`.

This is exactly 24 Green occurrences and 384 left endpoint entries. Right endpoints, poles, orders, and bank are fixed. The proposed first branch requires all 384 entries nonzero. No successful coefficient set is asserted.

Over `K=Q[z]/(z^8+1)`, a full seed certificate checks all 256 equations `C[i,j]=z^(ij)`. Equivalently it checks 16 seed equations `C[i,0]=1` and all 240 successor equations `C[i,j+1]=z^i C[i,j]`, for j<15. The seed cannot be dropped: `2F16` passes every successor equation and fails every seed equation. An actual solution would make every H_l invertible because B and F16 are invertible.

For a fixed inner prefix `X=H2 B H1`, define T_i with row j equal to row i of `G_j X`. The outer equation is linear in its eight coefficients: `a_(3,:,i)^T T_i=F16[i,:]`. A verified invertible eight-column pivot chart recovers those coefficients, after which the other eight entries must be checked. All pivot and endpoint nonzero guards remain part of the chart. A singular chosen chart is not a nonexistence proof.

T_i entries are quadratic in the 256 inner parameters. The original full equations are cubic in 384 parameters; outer elimination produces cleared consistency polynomials of degree at most 16, homogeneous of that degree when nonzero in the unconstrained inner variables. Variable elimination does not imply an easier solver.

The bounded rejected prefix fixes all 256 inner entries to one and leaves all 128 outer entries free, even permitting zeros. Independent reconstruction over the prime field F998244353 gives primitive root `z=929031873` and prefix determinant `195063167`. For every output row, its augmented nine-by-nine minor using columns 0 through 8 is nonzero. The first determinant is

`750393234 mod 998244353`.

The checker records all actual minors, determinants, pivots, reconstructed pivot coefficients, and all sixteen residuals per row. In particular, solving the first eight columns succeeds but the remaining eight fail, so those selected columns alone are misleading.

All rational pole denominators and Green guards survive this prime, and z satisfies `z^8+1=0`. Nonzero modular specialization of a determinant proves that determinant is nonzero in the characteristic-zero cyclotomic field. Therefore the augmented row lies outside the span of the eight templates even after extending the scalar field. This excludes precisely the fixed all-ones prefix, not other inner coefficients, the complete 384-variable family, or the general eight-order architecture.

## 8. Independent controls and replay

The fresh standard-library checker verifies:

- ten square/rectangle route sizes, with all eight labels in each;
- 24 complete scalar and 24 complete descended-weight resolvent identities, each compared entrywise;
- both Fourier folding channels through m64, exact even-column determinants, five global active-bank discrepancy ranks, and the full row rank of the corresponding unnormalized global Fourier discrepancies;
- 64 hierarchical lifts, each checked for Hamiltonicity, exact quotient, cycle count, and edit bound; exact margin recurrences through 65 levels per large seed;
- all sixteen N16 augmented minors and full residual rows;
- a generated product from 384 supplied nonzero endpoint entries, recovering all 128 outer entries and matching all 256 product entries;
- a changed-entry rejection and the missing-seed control;
- row-template ranks at N4,8,16,32,64, with all poles and inverse guards checked.

The generated-product control is a verifier test only; its target is its generated product, not the Fourier matrix. The modular row-template ranks prove the corresponding characteristic-zero ranks since the rational minors survive specialization. The prime is independently checked by trial division.

Run `python3 independent_checks.py` to reproduce `VERIFIED_RESULTS.json`. The sealed package includes isolated replay with byte equality and a hash manifest. Finite controls complement the proofs and do not turn a route or cut identity into full Fourier compatibility.
