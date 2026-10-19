# Independent review: endpoint two-step defect and observability reduction

Date: 19 October 2026. Owner: M-SCAN-DIMENSION. Priority: 34, unchanged.

## Final disposition

ACCEPT the new two-step defect theorem, exact two-channel observability reduction, optional centered symmetry reduction, and determinant-one Woodbury core as bounded structural results. They do not establish rank_Q(H_N)=N^2 and do not produce a rational annihilator of H_N. The original endpoint gate and owner remain open. Mathematical novelty is unestablished; the determinant lemma, Sylvester determinant identity, and Woodbury inverse identity are classical.

The complete frozen candidate REPORT.md was read and checked. Reviewed report SHA-256: 70e11214b797acca739910c5515dbc2dc7a429836b2603459678ca1b4113449d (12,934 bytes). Its five-file MANIFEST.json matches the local files. No mathematical correction is required. The classical identities are credited in the candidate itself.

## Pinned original model and guards

I read the pinned original endpoint report and the accepted odd-sector pivot obstruction as inert sources. Their local byte hashes are:

- Original endpoint: SHA-256 3c2043c73d2c765d88a050e47e9f1487c8b811479c346b8c712d7b8ff0c367ae.
- Accepted pivot obstruction: SHA-256 46968f362319f164f5eb01476d46899b34b9c1593f48a9cd412250f649c355ba.

The model remains N=2^m>=8, actual reversal of all m bits, T=3I+L+L^T+E_00, t=N/4+1, A=TP, C=PT=A^T, and variations in the full band |i-j|<=2. T is symmetric strictly diagonally dominant with positive diagonal, hence positive definite. Its neighboring entries are 1 and all leading/trailing principal minors are positive. Thus the original inverse-tridiagonal raw-chart tangent equivalence and stage invertibility apply in characteristic zero. The new calculations do not introduce a different permutation or decouple either adjacency.

## Independent proof of the two-step defect

Let U=PLP and K=[T,PTP]=A^2-(A^2)^T. Define

S_m={2^r-1,N-2^r:0<=r<=m} union {2^r,N-1-2^r:0<=r<m}.

The support proof follows from first/last carry stopping bits. Outside the listed exceptional words, the pertinent prefix and suffix changes occur in disjoint regions and commute, without hitting a truncated endpoint. More explicitly:

1. [L,U] has nonzero columns only possibly at x=N-1-2^r, 0<=r<m. Its action there is e_(2^(r+1))-e_(2^(r-1)), omitting terms whose exponent is outside 0,...,m-1. On all-ones input both compositions vanish.
2. [L,U^T] has nonzero columns only possibly at x=2^r-1, 0<=r<=m. Its action there is e_(N-2^(r-1))-e_(N-2^(r+1)), omitting terms whose exponent is outside 0,...,m.
3. The other two shift commutators are the negatives of the transposes of these two matrices.
4. The endpoint contribution is e_1 wedge e_0 minus e_(N/2) wedge e_0, where e_i wedge e_j=e_i e_j^T-e_j e_i^T.

These statements give a full exact sparse formula for K, not just a support bound. Skew-symmetry then gives zero rows as well as columns outside S_m.

Use disjoint labels z=0, w=N-1, a_r=2^r-1 and b_r=N-2^r for 1<=r<=m-1, and c_r=2^r,d_r=N-1-2^r for 1<=r<=m-2. This is 2+2(m-1)+2(m-2)=4m-4 distinct labels. Extend c_0=a_1,c_(m-1)=b_(m-1),d_0=b_1,d_(m-1)=a_(m-1).

For a vector restricted to this support, Kx=0 is exactly:

- b_(r+1)=b_(r-1) and a_(r+1)=a_(r-1), 2<=r<=m-2;
- d_(r-1)=d_(r+1) and c_(r-1)=c_(r+1), 1<=r<=m-2;
- a_1=b_(m-1), b_1=a_(m-1);
- b_2-d_1+z-w=0;
- -b_(m-2)+c_(m-2)+z=0;
- a_2-c_1-z=0;
- -a_(m-2)+d_(m-2)-z+w=0.

Empty interior recurrence ranges are allowed, so this includes m=3.

I independently solved the recurrences:

- For even m, all solutions have two free parameters A,z: w=2z; a_r=b_r=A for odd r and A+z for even r; all extended c_r,d_r equal A.
- For odd m, all solutions have four free parameters A,C,z,w: a_odd=A,a_even=C,b_odd=C,b_even=A; c_even=A,c_odd=C-z; d_even=C,d_odd=A+z-w.

The displayed parametrizations are necessary by the parity recurrences and sufficient by substitution. Consequently the compressed support matrix has nullity 2 for even m and 4 for odd m. Since all other rows and columns are zero,

rank_Q K = 4m-6 for even m, and 4m-8 for odd m.

The same rank statement is valid over every field. Each free parameter is an actual distinct coordinate, and all elimination steps use only addition or subtraction. In characteristic two, the relation w=2z becomes w=0; no division by two occurs and the two free parameters remain independent. Every supported row has a coefficient 1 or -1, so the claimed exact support also survives every characteristic. This strengthening concerns K only; neither original-chart regularity nor Woodbury invertibility over arbitrary finite fields is asserted.

These are ranks of the two-step defect only. Its many null vectors are not H_N annihilators.

## Determinant-one core and Woodbury order

Let B=A^2 and let E be the actual coordinate-selector matrix with columns e_s, s in S_m. Let K_S=E^T K E, so K=E K_S E^T exactly, and set G=E^T B^(-1)E and M=I-K_S G.

A is invertible since T and P are invertible. Therefore B and B^T are invertible. The classical determinant/Sylvester identity gives

det M = det(B-E K_S E^T)/det B = det(B^T)/det B = 1.

Thus this particular (4m-4)-square rational core is invertible at every allowed size, although K_S is singular. No inverse of K_S is used. The classical Woodbury identity, with its matrix order retained, is

(B^T)^(-1)=B^(-1)+B^(-1)E M^(-1)K_S E^T B^(-1).

This can also be checked by multiplying on the left by B-E K_S E^T. Since D(W)=C^(-1)WA, its square is D^2(W)=(B^T)^(-1)WB, giving the stated exact correction to B^(-1)WB. The correction's left-multiplier matrix has rank rank K. As an operator on N-by-N W, its rank is N times rank K, not merely rank K. An invertible logarithmic-size core does not establish any complementary H_N minor or compress the full unknown W to logarithmic dimension.

## Exact remaining two-channel condition

With q=t-1=2d and Y_0=C^q Z^T, the original annihilator conditions are exactly band_2(D^k Y_0)=0 for 0<=k<=q. This transformation is invertible over Q. Setting F=D^2 merely separates even and odd indices, giving band_2(F^j Y_0)=0 for 0<=j<=d and band_2(D F^j Y_0)=0 for 0<=j<d. Neither orientation of the observed band is discarded. The candidate correctly identifies uniform injectivity of this precise system as still unresolved. It does not assume the defect kernel is B-invariant or drop the correction/odd channel.

## Centering and supplementary polynomial checks

Put d=N/8, so t-1=2d, and W=C^d Z^T A^d. This is an invertible rational congruence. The original dual observations are exactly D^ell(W), -d<=ell<=d. Transpose sends D^ell(W) to D^(-ell)(W^T), so the exact kernel splits into symmetric and skew-symmetric W sectors; within either sector, the nonnegative-time observations suffice.

For Q=D+D^(-1) and R=D-D^(-1), Q preserves each transpose sector, R swaps sectors, QR=RQ, and R^2=Q^2-4I. The recurrences for D^ell+D^(-ell) and D^ell-D^(-ell), together with their leading coefficients, give an exact equivalent system in each sector:

- the full |i-j|<=2 band of Q^j W vanishes for 0<=j<=d;
- the full |i-j|<=2 band of R Q^j W vanishes for 0<=j<d.

The candidate asserts the centered symmetry equivalence; the Q,R polynomial formulas here are supplementary independently verified identities, not an additional claim needed for its acceptance. The polynomial equivalence is over Q, where division by 2 is legitimate. It is not a proof that the common kernel vanishes. To clear denominators one can take theta=det T>0, Eop=theta D and Fop=theta D^(-1). Explicitly Eop(W)=adj(T) P W T P and Fop(W)=P T W P adj(T). Then Eop Fop=Fop Eop=theta^2 I, and the same recurrence uses theta^2 instead of 1. This avoids an unnecessary determinant-of-P convention.

## Independently authored controls

No candidate or historical program was imported or executed. The following scripts were authored for this review; they compute no H_N ranks:

- checks.py: exact integer construction of T, P, and adj(T); original-to-centered map on every matrix basis vector at N=8,16; full symmetric/skew sector checks; polynomial recurrences; weighted self-adjointness controls. RESULTS.json: PASS.
- commutator_checks.py: sparse action of the original commutator, independent support compression, full complement check through m=11, and exact rational ranks of the compressed matrix for m=3,...,15. COMMUTATOR_RESULTS.json: PASS. The all-size support and rank conclusions follow from the proof above, not these samples.
- wedge_checks.py: literal equation (2.1) reconstructed independently and compared with the original sparse commutator for m=3,...,17; ranks over characteristics 2,3,5,7 and exact nonzero support controls. WEDGE_RESULTS.json: PASS. The all-field statement follows from the division-free proof, not these samples.
- woodbury_checks.py: actual coordinate selector, exact core determinant, full inverse identity and D^2 identity at N=8,16,32. WOODBURY_RESULTS.json: PASS. The all-size determinant-one conclusion follows from the classical identity above, not these samples.

## Scope

Accept only these bounded structural reductions. The reviewed frozen report respects every listed limitation. Do not relabel the result as an original endpoint-rank theorem, full dyadic dominance proof, actual Jacobian annihilator, generic nondominance theorem, new runtime bound, or novelty finding. The accepted odd-sector pivot obstruction remains correct and concerns a different pivot. M-SCAN-DIMENSION remains TO RESEARCH, priority 34.
