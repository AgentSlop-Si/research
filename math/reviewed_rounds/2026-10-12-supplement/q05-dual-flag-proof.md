Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: e26ad7981499031c77fb3182a397e3fea04695a13a459a0a871f68b640a1f7d1.

# Independent proof of the dual flag bridge

12 October 2026 UTC. The following argument independently verifies the proposed consequence of the older flag construction. It is a derivation supplied in this review, not a theorem quoted from Delvaux and Van Barel. It establishes a favorable ordering and its ranks; it does not establish a lower bound over every ordering.

## Setup and connection to the earlier construction

Let X and Y be finite abelian groups of order N=2^m, with a perfect bicharacter b:X×Y→K*, where K is a splitting field of characteristic other than 2. Choose a subgroup chain X_i of orders 2^i, and define Y_i=X_(m−i)^⊥. For each i from 1 to m select a_i∈X_i\X_(i−1) and c_i∈Y_i\Y_(i−1). Define x(j)=Σ bit_(i−1)(j)a_i and y(j)=Σ bit_(i−1)(j)c_i.

Each index-two extension is the disjoint union of its previous subgroup and one coset. Induction therefore proves these maps are bijections. It does not require the representatives to have order two. Every aligned block of 2^i consecutive x-labels is a coset of X_i, and every aligned block of 2^i consecutive y-labels is a coset of Y_i. Consequently these are permissible simultaneous coset-sortings in TW477 Lemma 12. The source already allows arbitrary subgroup chains and independent endpoint permutations; restricting its choices to these binary transversals is legitimate.

Let M_ij=b(x(i),y(j)). Set u_N(k)=rank M[0:k,k:N] and l_N(k)=rank M[k:N,0:k], including zero ranks at k=0,N.

## The exact recurrence

Suppose N≥4. Put A=X_1, K_0=X_(m−1), B=Y_1=K_0^⊥ and L=Y_(m−1)=A^⊥. Both quotients X'=K_0/A and Y'=L/B have order N/4, and b descends to a perfect pairing between them. Well-definedness follows from b(A,L)=b(K_0,B)=1. Perfectness follows from L^⊥=A and K_0^⊥=B.

The middle binary representatives induce reversed dual flags on X',Y'. For 0≤k≤N/2 write p=⌊k/2⌋ and d=⌈k/2⌉. The first k row labels are p complete A-pairs, possibly followed by the first member of a further pair. All columns outside L survive the cut. Since a_1 has order two, their complete row pairs have opposite entries.

Consider the k-dimensional column coordinate space. Let π map a vector to the p sums of its complete row pairs, dropping the unpaired coordinate. It is surjective, so dim ker π=k−p=d. Outside-L columns lie in its kernel. Their rank is d: their d representative row characters restrict to distinct characters of L because their labels are distinct modulo L^⊥=A. Character independence holds over K since its characteristic does not divide |L|. Evaluating over the outside coset simply scales each such row by a nonzero factor. Thus those columns span exactly ker π.

For columns in L, pair sums equal twice the corresponding quotient-pairing entries. Quotient column labels that survive are p,p+1,…,N/4−1, with repetition. When k=2p+1, the second member of pair p remains, so column p is indeed present. The quotient image has precisely the upper corner rank at cut p. The dimension formula for a subspace containing ker π gives

u_N(k)=⌈k/2⌉+u_(N/4)(⌊k/2⌋), 0≤k≤N/2.

Transposing the matrix exchanges the dual flags and gives the identical recurrence for l_N. No symmetry of b or equality of endpoint permutations is required.

## Reflection and induction

Let a=Σa_i and c=Σc_i. Binary complementation gives x(N−1−j)=a−x(j) and y(N−1−j)=c−y(j). Moreover

b(a−x,c−y)=b(a,c)b(x,c)^(−1)b(a,y)^(−1)b(x,y).

Simultaneous reversal therefore differs from M by invertible diagonal factors. This gives u_N(N−k)=l_N(k) and l_N(N−k)=u_N(k). At N=1 all endpoint ranks are zero; at N=2 both orientations have profile (1). Inductively, both orientations at every N have a common profile R_N, satisfying the proposed recurrence for N≥4 and k≤N/2, with R_N(k)=R_N(N−k).

Put s=N/4. At k=2p≤N/2, the quotient column count gives R_N(k)≤p+(s−p)=s. At k=2p+1<N/2 it gives R_N(k)≤p+1+(s−p)=s+1. Reflection handles larger cuts. If N≥8 then s≥2 and k=2s−1 has quotient corner of dimensions (s−1)×1, with nonzero entries, hence rank one. Therefore R_N(2s−1)=s+1. At N=4 the profile is (1,1,1). The maximum is exactly 0,1,1 for N=1,2,4, and N/4+1 for N≥8.

This proves the all-size favorable-ordering assertion. When combined with the separately accepted universal characteristic-zero lower, it recovers the accepted minimax equality. The algebraic argument alone provides no universal positive-characteristic lower, no spectral-gap result, and no claim that this profile is pointwise minimal over arbitrary orderings.

## Containment of the accepted symmetric recursion

For Q05's symmetric perfect pairing, choose the isotropic A of order two and K_0=A^⊥. The induced symmetric pairing on Q=K_0/A is perfect. If Q_j is the recursively constructed self-dual flag, lift it by X_j=π^(−1)(Q_(j−1)), 1≤j≤m−1, and set X_0=0, X_m=X. For these intermediate indices, the preimage identity for annihilators gives X_j^⊥=π^(−1)(Q_(j−1)^⊥)=X_(m−j). The endpoint identities hold as well. The property is immediate at orders one and two, proving it by induction for every recursive choice.

The accepted low-bit involution, middle lifted representatives, and high-bit complement are exactly binary representatives of this self-dual flag. Thus the accepted symmetric construction is inside the older dual-flag mechanism. It is useful as a symmetric implementation, but is unnecessary for the existence of independently permuted endpoints with the asserted upper.
