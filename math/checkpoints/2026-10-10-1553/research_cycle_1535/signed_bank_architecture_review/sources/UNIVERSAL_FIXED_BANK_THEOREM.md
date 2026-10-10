# Sharp universal synthesis with fixed signed magnetic bank parameters

10 October 2026. New author theorem and proof, pending independent review. Frozen prior results and source programs are not changed or executed.

## Main result

Let N≥3 be odd, let k be any field with char(k) not dividing N, and let q∈k have multiplicative order exactly N. Keep the accepted S,T,W_(a,b)=S^a T^b and whole-bank grammar

B_(ε,δ)(α,β;w) = (1/N) Σ_(j=0)^(N−1) w_j (I−αS^ε−β q^(εδj)T^δ)^−1,
Δ=1−α^N−β^N ≠0.

A fixed universal architecture is a list of permitted parameter/sign tuples (ε_i,δ_i,α_i,β_i), chosen once independently of the target matrix, such that varying only the N phase weights in every slot spans all Mat_N(k). Let U_k(N;q) be the minimum length of such a list. Repeated identical tuples can be merged, and slots with zero phase weights may be unused for an individual target.

THEOREM. U_k(N;q)=2N−2. An explicit attaining architecture has β=1 everywhere and multiplicities

(n_++,n_-+,n_+-,n_--)=(N−2,1,1,N−2).

The ++ and −− slots each use the same distinct nodes X={q²,q³,…,q^(N−1)}. Both cross-sign singleton nodes are α=1. All parameters and all target-dependent weights remain in k. Every guard is exactly −1. The construction applies to all N² matrix coordinates, including axes, and to every primitive q, including composite odd N and positive characteristic not dividing N.

In particular every matrix over k, hence F_N, has an exact representation by at most 2N−2 legal banks. This improves the old universal 4N upper bound. It does not determine the target-adaptive Fourier minimum M_k(N;q), and the accepted fourteen-bank F_11 construction remains stronger than this theorem's twenty-bank specialization.

## Coefficient identity and nonzero factors

For a,b∈{0,…,N−1}, put r=[εa]_N, ℓ=[δb]_N and

G_(ε,δ)(a,b) = [r+ℓ choose ℓ]_(q^(εδ)) if r+ℓ≤N−1, and 0 otherwise.

The accepted finite Gaussian-binomial inverse expansion says a bank contributes

η_ℓ α^r G_(ε,δ)(a,b)

to W_(a,b), where η_ℓ=β^ℓ(N^−1 Σ_j w_j q^(εδjℓ))/Δ. At fixed parameters, each sector has at most one free scalar η_ℓ; this remains true when β=0 or α=0.

Every displayed nonzero Gaussian factor is a unit of k. Indeed its numerator and denominator factors are 1−q^d or 1−q^(−d), with 1≤d≤N−1; exact order N is sufficient and primality of N is not used. The Weyl matrices are a basis because tr(W_(a,b)^−1 W_(c,d))=N times the Kronecker symbol.

For all slots in the construction β=1 and α^N=1. Hence Δ=−1, and any sector amplitudes are realized by

w_(i,j) = − Σ_(ℓ=0)^(N−1) η_(i,ℓ) q^(−ε_iδ_i jℓ).

Character orthogonality cancels the 1/N in the bank definition. Thus assigning sector amplitudes is exactly assigning legal raw phase weights, not an enlargement of the class.

## The lower bound allows every legal parameter tuple

Consider the linear projection from Mat_N(k) onto its Weyl coefficients at (a,1), 1≤a≤N−1. It is onto k^(N−1). A slot with δ=−1 has ℓ=N−1. For every nonaxis a, r=[εa]_N≥1, so r+ℓ≥N and the slot contributes zero to this whole projection. A slot with δ=+1 has ℓ=1 and contributes only η_1 times one fixed vector. Its projected span has dimension at most one, regardless of α, β, vanishing amplitudes, coincident nodes, or legal degeneracies. Consequently a universal architecture needs at least N−1 positive-δ slots.

Likewise, on (a,N−1), 1≤a≤N−1, positive-δ slots vanish and each negative-δ slot has projected dimension at most one. At least N−1 negative-δ slots are necessary. These two sets of slots are disjoint, proving U_k(N;q)≥2N−2. This argument allows all legal α,β and all four orientations; it is not restricted to β=1. Cancellation cannot increase the dimension of the sum of the projected one-dimensional spaces.

This is a lower bound on universal target-independent architecture size. It is not a lower bound of 2N−2 for any particular matrix when nodes may be tailored to that matrix.

## Constructive upper bound

Write an arbitrary target A=Σ_(a,b) c(a,b)W_(a,b), with c(a,b)∈k. Let m=N−2 and h=(N−1)/2. Enumerate X as x_i=q^(i+1), i=1,…,m. All x_i are distinct and nonzero.

The interpolation fact used below is elementary. For d distinct nonzero nodes, the square matrices (x_i^r) with r=0,…,d−1 and with r=1,…,d are invertible: their determinants are, respectively, the Vandermonde product and that product times Π_i x_i. Thus any d consecutive moments starting at zero or one can be assigned uniquely. When d<m, use the first d nodes and set all remaining amplitudes to zero.

For each physical row b, a slot's sector is ℓ=[δb]_N. Since b↦[δb]_N is a permutation, assignments for different physical rows use different sector amplitudes in every slot and never interfere.

### Row b=0

Put d_j=(1/N) Σ_(a=0)^(N−1) c(a,0)q^(−ja). Give ++ node q^j the sector-zero amplitude d_j for j=2,…,N−1. Give the −− node q^(N−1) amplitude d_1 and the −+ singleton amplitude d_0. Set every other sector-zero amplitude to zero.

The ++ vectors are q^(ja), the selected −− vector is (q^(N−1))^[−a]_N=q^a even at a=0, and the singleton vector is 1. Their sum is Σ_j d_j q^(ja)=c(a,0). Thus the entire b=0 axis row is matched in k.

### Positive edge row b=1

Use the −+ singleton amplitude

y = c(N−1,1)/G_-+(N−1,1).

The denominator is nonzero since its local total is 2≤N−1. For a=1,…,N−2 define

v_a = (c(a,1)−yG_-+(a,1))/G_++(a,1).

Choose the m ++ amplitudes p_i uniquely so that Σ_i p_i x_i^a=v_a for a=1,…,m. Set all −− amplitudes to zero. Give the +− singleton the amplitude

z = c(0,1)−y−Σ_i p_i.

The ++ slots match a=1,…,N−2; only the −+ singleton can contribute at a=N−1. The +− singleton here has ℓ=N−1 and therefore affects only a=0; the stated z matches that axis coefficient. Every coordinate of this row is now correct. The construction also covers N=3.

### Rows 2≤b≤h

These rows exist only when N≥5. Put a_*=N−b. This nonaxis coordinate belongs exclusively to the −+ orientation: its local −+ total is 2b≤N−1, while the ++ and −− totals are N and the +− total is 2(N−b)>N−1. Set

y = c(a_*,b)/G_-+(a_*,b)

in the −+ singleton and set the +− singleton amplitude to zero.

For a=0,…,N−b−1 prescribe

P_a=(c(a,b)−yG_-+(a,b))/G_++(a,b).

There are N−b≤N−2=m such moments. Use the first N−b nodes of X to choose ++ amplitudes p_i with Σ_i p_i x_i^a=P_a for all these a, and set remaining ++ amplitudes to zero.

For the −− group prescribe moments Q_0=0 and, for r=1,…,b−1,

Q_r=(c(N−r,b)−yG_-+(N−r,b))/G_--(N−r,b).

There are b≤m moments. Use the first b nodes to choose −− amplitudes u_i with Σ_i u_i x_i^r=Q_r for r=0,…,b−1, and set remaining amplitudes to zero.

All divisions are by nonzero factors on the respective triangles. The supports show why the choices do not interfere. At nonaxis a, ++ is supported exactly on 1≤a≤N−b−1 and −− exactly on N−b+1≤a≤N−1. Their only missing nonaxis coordinate is a_*, which y matches. The −+ contribution is subtracted in each prescribed residual. At a=0 every G equals 1; the −− group contributes Q_0=0 and the +− singleton contributes zero, so the P_0 prescription matches the axis as well. This accounts for all N coordinates of the row.

### Rows h+1≤b≤N−1

Let d=N−b, so 1≤d≤h. Apply the appropriate positive-row recipe above to the reflected row t(a)=c([−a]_N,b), viewed as a target at physical row d. Swap ++ with −− and −+ with +− in the resulting amplitudes and use them at physical row b.

The identity

G_(−ε,−δ)([−a]_N,[−b]_N)=G_(ε,δ)(a,b)

holds because εδ and the local coordinates r,ℓ are unchanged. The node lists in the swapped groups are identical. Hence the reflected recipe matches c(a,b). This construction does not assume that the arbitrary target is reflection-symmetric. Reflection is a proof and coefficient-assignment device; no extra operation is performed on the original target or allowed as a free bank operation.

All N rows have been assigned. Convert the amplitudes to the raw weights displayed above. Every branch has Δ=−1, so the finite inverse identity proves it is the original legal resolvent. All N² Weyl coefficients, and therefore all N² original matrix entries, agree. This proves the upper bound and the theorem.

## Resource interpretation and cost boundary

The exact resource optimized by U_k is the number of preselected parameter/sign configurations needed for universal linear programmability via phase weights. This is an intrinsic algebraic architecture question: one fixed family can synthesize every matrix, and no smaller family can do so. It is meaningful without claiming a hardware implementation.

The architecture has 2N−2 slots and N(2N−2)=2N²−2N declared raw phase weights and inverse-branch occurrences. Its weight-to-matrix linear map has rank N² and kernel dimension N²−2N. Its ordinary scalar dimension is N², as it must be; the theorem does not compress the information in an arbitrary matrix.

A literal implementation still has O(N²) branch occurrences, each an N×N inverse action. Computing weights, sharing fixed inverses, structured application cost, conditioning, bit complexity and physical components require separate analysis. Bank slots are not scalar operations, branches, scans, memory words or time steps. No Fourier speedup follows.

## Status and relation to accepted results

This theorem is a new author derivation within the accepted bank grammar and is pending independent review. It supplies an infinite family of transform orders and a sharp universal architecture count, not a general formula for the special Fourier rank. It neither changes nor weakens the accepted exact minima at N=3,5,7 or the fourteen-bank N=11 upper bound and fixed-order parametric family. All these statements may coexist because target-dependent node selection is a strictly different optimization problem from target-independent universality.
