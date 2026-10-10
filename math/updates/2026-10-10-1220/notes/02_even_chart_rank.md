# Even chart rank corollary

Let N≥2 be even and K be a field containing a root w of exact order N. Let αβδ≠0, where δ=1−α^N−β^N, and put

φₛ=∏ⱼ₌₁ˢ(1−wʲ),  G(r)=∑ₜ₌₀ᴺ⁻¹w^(−t²−rt),  Hₛ=G(s)/(Nφₛ),

with φ₀=1 and 0≤s<N. Define the strictly truncated weight matrix by

W[a,b]=δ(φₐα^(−a))(φᵦβ^(−b))H_(a+b)  if a+b<N,

and W[a,b]=0 otherwise, for 0≤a,b<N. Then

rank W=N if N≡2 modulo 4, and rank W=N−1 if N≡0 modulo 4.

Proof. Write N=2m and κ=m modulo 2. Translation by m gives G(r)=(−1)^(m+r)G(r), so only parity κ can survive. The identity G(r+2)=w^(r+1)G(r) relates all values on that parity by nonzero factors. At least one survives because ∑ᵣG(r)=N≠0. Thus G(r) is nonzero exactly when r≡κ modulo 2.

All diagonal scaling factors φₐα^(−a), φᵦβ^(−b), and δ are nonzero. If N≡2 modulo 4, the final antidiagonal of W has degree N−1 and is nonzero; reversing all columns makes W upper triangular with nonzero diagonal. If N≡0 modulo 4, the last row and column vanish, while reversing the columns of the leading (N−1)-square makes that square upper triangular with nonzero diagonal of degree N−2. The claimed ranks follow. In particular N=2 has rank 2 and N=4 has rank 3.

The statement uses exact field arithmetic and the strict integer cutoff a+b<N. Its rank conclusion is unaffected by an overall nonzero normalization scalar. It supplies a separable-representation rank bound, not an arithmetic-operation lower bound.
