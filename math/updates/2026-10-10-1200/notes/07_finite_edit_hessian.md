# Mixed Hessian basis and finite edit normalization

Version 2026-10-10, Phase 21. Mathematical status: independent scoped acceptance with a finite-normalization-domain amendment.

The selected mixed Hessian matrices form a basis, and the fixed-base mixed-channel count equals the rank in the explicitly defined normalization. The finite-edit division-free identity is valid whenever the specified resolvents exist. Its entrywise-divided form additionally needs every entry of the bridge C′ to be nonzero. Defined Green inverses alone do not ensure this condition.

These are identities and restricted channel-count statements for a specified two-layer network. A full Hessian span does not establish local dominance, a Fourier construction, a Fourier impossibility theorem or a faster full transform.

## Hypotheses that stay pinned

For the Hessian theorem, N = s² with s = 2^a and a at least 1. Coordinates are (x,y) modulo s, with row-major index xs + y. The selected input permutation is (x,y) → (x + 2y + 1,y), and the selected output permutation is (x,y) → (x,y + 2x + 1).

The selected edge weights are nonzero, each selected Green cycle product differs from one, and the two selected scalar coefficients are nonzero. Any other network Green terms needed to define the full network must also have valid inverses.

The numerical Fourier-residual claims additionally pin the entire two-stage four-plus-four topology, all stage coefficients to 1/4, all eight weight arrays to the seed-19 construction, and the unnormalized finite-field Fourier matrix F[i,j] = omega^(ij), with omega = 3^((65537−1)/N). Altering the other six terms, the base point, the coefficients, the Fourier indexing, or the topology changes the residual and its normalization.

The Jacobian dimension 504 is an exact generic statement at N = 64 for the specified fixed-coefficient family. This single certificate is not an all-length equality theorem.

## Why the Hessian basis is valid

Write H = (I − diag(h)Q_H)^−1 and V = (I − diag(v)Q_V)^−1. Let B = Q_H H, C = Q_V V H, and alpha = alpha_V alpha_H.

The mixed derivative indexed by vertical edge i and horizontal edge j is

H_ij = alpha C[i,j] V[:,i] B[j,:].

Each selected permutation runs through a whole coordinate fiber because its translation step is odd modulo a power of two. Nonzero edge weights and valid cycle denominators make the Green kernel nonzero at every pair in its fiber. A horizontal fiber and a vertical fiber have exactly one relevant intersection, so every entry of C is nonzero.

With row-major vectorization and pair order (i,j),

K = (V ⊗ B^T) diag(vec(alpha C)),

det(K) = det(V)^N det(B)^N product over i,j of alpha C[i,j].

Every factor is nonzero. Thus the N² mixed derivative matrices form a basis under the stated hypotheses. This is an all-length algebraic argument; the finite-size certificates corroborate its implementation.

## What normalized rank one means

For fixed base data define

L(E) = (alpha^−1 V^−1 E B^−1) entrywise-divided by C.

Then the mixed directional term for vectors dv and dh satisfies

M(dv,dh) = alpha V diag(dv) C diag(dh) B,

L(M(dv,dh)) = dv dh^T.

The smallest number of freely chosen additive mixed channels in this same fixed normalization needed to sum to E is exactly rank(L(E)). The proof is the usual rank-one decomposition of a matrix.

This statement permits independent additive channels as mathematical summands. It does not show that those summands can be realized by one update of the original two selected resolvents, or that they can be evaluated within a particular operation budget.

This is not ordinary operator rank. Entrywise division by C is an invertible linear map on matrix space, but it does not generally preserve matrix rank. Indeed C = Q_V V H is invertible. When all entries of dv and dh are nonzero, the unnormalized M has ordinary rank N while L(M) has rank one.

The residual rank N at the pinned baselines excludes a representation of that residual by fewer than N such independently summed, fixed-base, mixed-only channels. It imposes no equivalent restriction on unrestricted finite weight updates.

## Correct finite-edit theorem

Let H′ and V′ be the modified selected Green matrices. Set dH = H′ − H and dV = V′ − V. Suppose all original and modified Green inverses exist, and hold the other six terms and all coefficients fixed.

The four-point difference of the complete network is exactly

D = T(v+dv,h+dh) − T(v+dv,h) − T(v,h+dh) + T(v,h)
  = alpha dV dH.

The resolvent identity gives the division-free equality

(V′)^−1 (D/alpha) H^−1 Q_H^−1
  = diag(dv) C′ diag(dh),

where C′ = Q_V V H′.

This identity is valid for all finite edits with the stated inverses. If, in addition, every entry of C′ is nonzero, entrywise division gives dv dh^T and therefore normalized rank at most one. Nonzero original vertical weights and nonzero modified horizontal weights, together with valid cycle denominators, suffice for this additional condition.

The source prose says that inverse existence alone suffices and that C′ automatically has no zero entries. That wording is too broad. Its implementation already checks the extra condition and raises an error for a zero bridge entry.

A concrete counterexample sets all modified horizontal weights to zero. Then H′ = I is perfectly well-defined. At N = 16 the bridge Q_V V H′ has 192 zero entries. The division-free identity still holds, but the proposed entrywise normalization is undefined. This is a chart-domain correction, not a failure of the resolvent identity.

## First-order and higher-order terms

For the complete edit, not the four-point difference, the exact equation is

T′ − T = alpha_H L_out dH + alpha_V dV L_in + alpha_H alpha_V dV dH.

The first two terms are one-sided finite differences. Although linear in dH and dV, each already contains all orders in the original edge increments. Dropping them is not a legitimate finite-repair test. The mixed term also includes all orders through the new Green factors.

Fresh complete-network reconstructions verified this decomposition and the four-point identity at N = 4, 16 and 64. In these dense-edit examples the mixed term has normalized rank one, while the complete edit has rank N in the original fixed-base normalization. The sparse N = 16 check gives normalized complete-edit rank four.

The finite normalization depends on the unknown edited factors V′ and H′. A rank computation made with the original fixed normalization cannot simply be reused for that new normalization.

Finally, requiring only that a normalized corrected residual have all 2 by 2 minors zero is a relaxation unless the outer factors are also tied to the same dv, dh that define H′ and V′. Rank one by itself does not encode all coupled resolvent equations.

## Local and global scope

A full linear span of separate Hessian columns is compatible with a low-dimensional nonlinear image. The actual directional coefficients are tied products dv_i dh_j, rather than N² independently adjustable coefficients.

For the full fixed-coefficient architecture, the image dimension at N = 64 is 504, whereas the ambient matrix dimension is 4096. At N = 16 the previously certified image dimension is 120 versus ambient dimension 256. These image dimensions preclude an open ambient image; the full Hessian span does not establish local dominance. A particular Fourier matrix may still lie on such a lower-dimensional image.

The two-rook-factor bound N(4s−3) is also a generic image-dimension bound for invertible targets, obtained from the free intermediate diagonal gauge. It does not decide membership of a specific Fourier matrix.

## Next valid compatibility test

For an actual restricted finite-repair decision, retain the full equation with the other six terms and coefficients fixed. One denominator-safe formulation introduces H′ and V′ as variables and enforces

(I − diag(h′)Q_H)H′ = I,
(I − diag(v′)Q_V)V′ = I,

together with the full Fourier equality. These square inverse equations exclude singular Green matrices without silently discarding admissible zero-weight bridge cases.

A rational elimination approach must saturate the required Green denominators. If it additionally divides by bridge entries, it must retain and analyze the admissible zero-bridge branches separately. A no-solution result in one finite field does not by itself exclude characteristic-zero solutions. A positive finite-size candidate requires exact equality of every matrix entry and still does not establish an all-length construction or a fully charged running-time improvement.


## Exact certificates

Modulo 65537 the mixed-Hessian determinants at N=4,16,64,256 are respectively 49757,36442,45656,10163. N=4 and N=16 were rebuilt directly; N=64 and N=256 use the proved determinant-product identity. The second-field N=16 determinant modulo 786433 is 545886.

The saved 504 by 504 Jacobian minor at N=64 has determinant 8439 modulo 65537. Eight independent null directions give the matching upper bound, so the fixed 4+4, 512-weight architecture has generic rank 504. This is one exact architecture/size statement, not an all-length equality theorem. The normalized seed-19 Fourier residual has rank N at N=4,16,64,256.

At N=16 the legal edit h′=0 makes the bridge have 192 zero entries. The division-free identity survives, while the entrywise normalization is undefined. Dense complete-edit controls at N=4,16,64 have original-normalized rank N, although the isolated mixed term has normalized rank one. The complete correction cannot discard the one-sided or higher-order terms.

The certificate inputs and numerical mathematical checks are included. Historical priority, unrestricted factorization/complexity claims and practical runtime remain unestablished.
