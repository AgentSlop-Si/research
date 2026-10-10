# An explicit aggregate Gauss family below the dense count

10 October 2026. Separate constructive continuation. The earlier five-chain 54-edge certificate is preserved unchanged.

## Result

For every odd prime p≥5, the accepted square-invertible, separately colored aggregate model admits

    E = 2p²+p−floor(p/4)

edges. A single four-vertex chain already gives 2p²+p−1. At p=5 this is 54 rather than 55 edges.

This is an exact complex construction. Its cancellation occurs within each aggregate fiber, not by identifying different latent colors. It remains quadratic: one boundary is the full Fourier matrix. It is not an asymptotically faster FFT, a claim about the minimum of the unrestricted aggregate model, or a historical-priority claim.

A complementary all-prime theorem proves that an invertible one-sided endpoint basis with at most p+2 nonzeros cannot improve the dense count. The construction has p+3 nonzeros with a single chain, so that first possible endpoint-sparsity threshold is sharp for p≥5. The p=3 full square model is handled separately by the independent review.

## 1. The four-vertex chain

Let ζ=exp(2πi/p), F[i,t]=ζ^(it), and

    a = 1+ζ+ζ⁻¹.

The real number a is nonzero and is not 1. Indeed, a=0 would give a nontrivial cube root, and a=1 would give a fourth root, impossible for a primitive odd-prime root with p≥5.

Take four distinct indices (q,q+1,q+2,q−1), interpreted modulo p. Define

    C = I + E_(q+1,q) + a E_(q+2,q+1) + E_(q−1,q+2).

Here E_(i,j) has one in row i, column j. In the ordering q→q+1→q+2→q−1, C is a unit lower-bidiagonal chain. In particular, C is invertible and has p+3 nonzeros. Let R=C⁻¹F.

For z=ζ^t, the only changed rows of R are

    R[q+1,t] = z^q (z−1),
    R[q+2,t] = z^q (z²−az+a),
    R[q−1,t] = z^q (z⁻¹−z²+az−a).

Every other row is the unchanged nonzero character z^i. The displayed formulas follow successively from CR=F, so no inverse algorithm is assumed free.

The first changed row has exactly one zero, at t=0. The middle changed row has no zeros on the pth-root grid. To see this, divide its polynomial by z. If z≠1 is an odd-order root on the unit circle, the imaginary part of

    z−a+a z⁻¹

is (1−a) Im(z), which is nonzero. At z=1 the polynomial is 1.

The last row has the decisive factorization

    z⁻¹−z²+az−a = −z⁻¹ (z−1)(z−ζ)(z−ζ⁻¹).

It therefore has exactly three grid zeros, at t=0,1,p−1. These roots are distinct. Consequently R has exactly four zero entries:

    (q+1,0), (q−1,0), (q−1,1), (q−1,p−1),

and nnz(R)=p²−4. Thus

    nnz(C)+nnz(R) = (p+3)+(p²−4) = p²+p−1.

For the simple p=5 witness choose q=0. Since a=−ζ²−ζ³,

    C = I + E_(1,0) − (ζ²+ζ³) E_(2,1) + E_(4,2).

It has 8 nonzeros, R has 21, and R's column counts are (3,4,5,5,4).

## 2. Packing independent chains

Choose m disjoint four-element blocks, with 1≤m≤floor(p/4). A concrete choice is

    q_k=4k+1,        k=0,…,m−1,

so the k-th chain uses the indices (4k+1,4k+2,4k+3,4k). Use the three preceding off-diagonal entries within each block and no entries between blocks. All other indices are singleton identity blocks.

The chain calculations apply independently, with the harmless nonzero factor z^(q_k). Hence

    nnz(C) = p+3m,
    nnz(R) = p²−4m.

More precisely, the column counts of R are

    r(0)=p−2m,
    r(1)=r(p−1)=p−m,
    r(t)=p otherwise.

No row support or latent color has been identified across different blocks. Each C edge, and each nonzero entry of every middle slice below, is charged separately.

Each four-vertex chain has a ten-entry inverse instead of its seven-entry forward block. Therefore

    nnz(C⁻¹)=p+6m,       δ_C=3m.

This explicitly passes the inverse-support-expansion gate; it does not claim that gate was sufficient in general.

## 3. Complete colored aggregate graph

Set A=F, so S=FA⁻¹=I. Write q(t)=−t²/2 modulo p and let e_t be the t-th coordinate vector. Define each separately labeled middle slice by

    B_t = ζ^q(t) R_[:,t] e_t^T.

Then, entry by entry,

    C B_t A = ζ^q(t) (C R_[:,t]) (e_t^T F)
            = ζ^q(t) χ_t χ_t^T.

This is the required aggregate identity. Every B_t is rank one and has exactly r(t) nonzero entries. One middle edge is used for each of these entries. In this particular construction the different t slices even have disjoint columns, but the count does not depend on merging them.

The complete edge ledger is

    input boundary A:                 p²,
    output boundary C:                p+3m,
    separately colored middle edges:  p²−4m,
    total:                            2p²+p−m.

The mixing penalty Σ_t(r(t)−1)(s(t)−1) is zero because every s(t)=1. The inverse-expansion gate reads 3m>0.

The construction also explicitly fails the fixed-gauge pointwise-character condition. For a chain root q, column q of C attaches the same hidden vertex to outputs q and q+1 with equal weights. Its R row is the nonzero character z^q, so every latent color reaches that vertex. A pointwise output-character law with fixed endpoint gauges would require 1=(g_(q+1)/g_q)ζ^t for every t. Colors 0 and 1 contradict this. Thus the support saving uses a genuine aggregate-cancellation escape.

For completeness, let G=Σ_t ζ^(−t²/2), which is nonzero. If B=Σ_t B_t, then

    (CBA)[i,j] = G ζ^((i+j)²/2).

Set

    C' = G⁻¹ diag(ζ^(−i²/2)) C,
    A' = A diag(ζ^(−j²/2)).

All diagonal corrections are nonzero, so the charged supports are unchanged, and C' B A'=F exactly. The transformed individual slices have the corresponding endpoint gauges. No additional graph layer or uncharged edge is being introduced: these scalars multiply existing boundary edge weights.

## 4. Why p+3 is the first allowed endpoint sparsity

**Theorem.** For every odd prime p and every invertible p×p matrix X with nnz(X)≤p+2,

    nnz(X)+nnz(X⁻¹F) ≥ p²+p.

First choose a nonzero determinant matching. Permuting and scaling hidden columns, which only permutes/scales rows of X⁻¹F, normalizes X to I+N with at most two off-diagonal nonzeros. This preserves both support counts under consideration. With at most one off-diagonal entry, or two noncomposable entries, N²=0 and the inverse is no denser. Two opposite entries form a nonsingular 2×2 block whose inverse has the same support. The accepted Fourier-uncertainty inequality then proves the claim in these cases.

The only remaining pattern is a chain on three distinct indices i→j→k, with nonzero links α and β. The only changed Fourier rows are

    χ_j−αχ_i,
    χ_k−βχ_j+αβχ_i.

By prime Fourier uncertainty, they have at most one and two zeros respectively. It remains to exclude all three zeros simultaneously.

If the first row vanishes at t0, then α=ζ^((j−i)t0). Shift t by t0 and divide out the nonzero character phases. Put x=j−i and y=k−i; thus x,y,y−x are nonzero. The changed rows become, up to nonzero factors,

    ζ^(xt)−1,
    ζ^(yt)−b(ζ^(xt)−1),

with b≠0. The second row is nonzero at t=0. If it vanished at two distinct nonzero residues u,v, eliminating b would give

    ζ^(yu+xv)+ζ^(yv) = ζ^(yv+xu)+ζ^(yu).

The rational coefficients in this relation sum to zero. For a prime root, the only rational relation among 1,ζ,…,ζ^(p−1) is a multiple of their full sum. The zero coefficient sum forces that multiple to be zero. Thus the two exponent multisets must agree.

For one matching, yv=yu, contradicting u≠v and y≠0. For the other matching, xv=xu=0, contradicting x≠0 and u,v≠0. This excludes three simultaneous zeros. There are therefore at most two removed entries, exactly no more than the two added chain edges, proving the theorem.

The same argument also covers disjoint three-vertex-chain blocks. It is an all-complex argument, not a finite coefficient-grid inference. The four-vertex construction above demonstrates that extending it to arbitrary longer chains would be false.

## 5. Scope, cost, controls, and stopping point

The formulas directly generate a, C, R, and every B_t coefficient from ζ and powers of it. The inverse is also explicitly I−N+N²−N³, since the chains are disjoint and N⁴=0. The construction does not treat dense inverses or nonlinear fitting as free operations.

The graph has Θ(p²) edges and A alone is dense. Writing all edges is quadratic output size; no O(p log log p) preprocessing, running time, bit complexity, finite-word stability, or live-state improvement is asserted. This is a strict support improvement and a counterexample to extending the dense aggregate lower bound to every square invertible basis.

`fresh_four_chain_controls.py` is newly authored, standalone, and exact in rational prime cyclotomic fields. It imports or executes no supplied research program. It checks the simple p=5 witness and packed-chain cases, inverse supports, CR=F, separately counted slice identities, and corrected Fourier transfer. The symbolic factorization and proof establish the family; these finite controls independently test its implementation. The earlier bounded chain-order search was a discovery device only.

The original five-chain p=5 certificate and its results are preserved in the parent folder. No optimization claim beyond the stated family or the p+2 no-escape threshold is made. The constructive task stops with this explicit family and its independent review.
