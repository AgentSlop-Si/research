# Endpoint bit reversal: an exact two-step defect and a bounded unresolved disposition

Date: 2026-10-19. Record: M-SCAN-DIMENSION. Status remains TO RESEARCH; priority remains 34.

## Disposition

The prescribed endpoint Jacobian lemma is **not proved or refuted**. This packet proves a different, all-size structural result for the exact endpoint family:

- For N=2^m, m>=3, the skew defect of the squared transfer matrix is supported on exactly 4m-4 coordinates. Its rank over Q is 4m-6 when m is even and 4m-8 when m is odd.
- This defect gives an exact two-step dual factorization with a (4m-4)-square Woodbury correction matrix whose determinant is identically 1. Its invertibility does not rely on the already-disproved odd-sector Schur pivot.
- The resulting two-channel, half-length observability problem is stated explicitly. Its uniqueness is the remaining missing implication; the defect theorem does not establish it.

No nonzero rational annihilator of the original H_N is produced. In particular, a vector in the kernel of the skew defect is not a Jacobian annihilator. No new threshold-rank census, accepted depth-two rerun, external write, owner closure, changed priority, or novelty claim is made.

## 1. Fixed model and source binding

Let P=P_N reverse all m binary digits, L=L_N be the subdiagonal shift, and

    T=3I+L+L^T+E_00,   A=TP,   C=PT=A^T.

The original target is rank_Q H_N=N^2 at t=N/4+1, where

    H[(r,s),(k,i,j)] = A^k[r,i] C^(t-1-k)[j,s],
    0<=k<t, |i-j|<=2.

All computations and identities below retain both L and L^T and the actual full bit reversal. The matrix T is positive definite by strict diagonal dominance, its neighboring entries are nonzero, and its leading/trailing principal minors are positive. Thus the accepted inverse-tridiagonal tangent transport, its original-chart regularity guards, and the original parameter ledger remain valid over Q. No claim about original-chart regularity over finite fields is needed here.

Controlling source bytes, read as text:

1. Original endpoint formulation: commit b1093eb6705fbef4e6dfcc0e29e69f6a5d31e21e, math/finalized/2026-10-18-fifth-cycle-six-results/bit_reversal/candidate/REPORT.md. Git blob 1b2c206ef51122c530d42656a9271efb6aaaa6a6; SHA-256 3c2043c73d2c765d88a050e47e9f1487c8b811479c346b8c712d7b8ff0c367ae.
2. Accepted odd-sector pivot obstruction: commit 31ccd8d6f5bb6afaffa9d86b9e9e2fd27332d856, math/finalized/2026-10-19-scan-schur-pivot-obstruction/candidate/REPORT.md. Git blob 5863f9a67ea953d75d3d2a6408cf24378c120cab; SHA-256 46968f362319f164f5eb01476d46899b34b9c1593f48a9cd412250f649c355ba.

The exact local copies are those named by ../SOURCE_PROVENANCE.json. Their hashes are independently checked in this packet's SOURCE_BINDINGS.json. The accepted finite N=8,16,32 anchors, all-size depth-two result, and centrosymmetric-anchor obstruction remain unchanged.

## 2. The squared transfer has a logarithmically supported skew defect

Set

    T'=PTP,   B=A^2=TT',   K=B-B^T=[T,T'].

For r in the indicated ranges define coordinate labels

    a_r=2^r-1                 (0<=r<=m),
    b_r=N-2^r                 (0<=r<=m),
    c_r=2^r                   (0<=r<m),
    d_r=N-1-2^r               (0<=r<m).

Let S be the union of these coordinates. Use the following distinct-coordinate listing:

    0, N-1;
    a_r,b_r, 1<=r<=m-1;
    c_r,d_r, 1<=r<=m-2.

For m>=3 these coordinates are distinct, so |S|=2+2(m-1)+2(m-2)=4m-4. The endpoint identifications omitted from the listing are

    c_0=a_1, c_(m-1)=b_(m-1),
    d_0=b_1, d_(m-1)=a_(m-1).

### Theorem 2.1: exact support and rank

The rows and columns of K outside S vanish, and every row and column in S is nonzero. Its rank is

    rank_Q K = 4m-6   if m is even,
    rank_Q K = 4m-8   if m is odd.

The proof below uses only identities and elimination with coefficients 1 and -1. In fact the same rank formula holds after reduction to any field; this strengthening concerns K only, not H_N or the original chart.

### Support proof

Put U=PLP. Ordinary increment L changes the suffix beginning at the last zero, and reversed increment U changes the prefix ending at the first zero. They commute on a basis word having at least two zeros, since the affected regions are disjoint and neither update changes the other's stopping bit. Thus [L,U] has columns only at the all-one and single-zero words.

The reversed argument shows that [L^T,U^T] has columns only at the all-zero and single-one words. Ordinary increment and reversed decrement commute whenever a one precedes a later zero; consequently [L,U^T] has columns only at the monotone words 0...01...1. Similarly [L^T,U] is supported on the monotone words 1...10...0. These four word families are precisely S.

Now

    K=[L+L^T,U+U^T]+[L+L^T,E_00]+[E_00,U+U^T].

The final two commutators touch only coordinates 0,1,N/2, already in S. Hence all columns outside S vanish. Since K is skew-symmetric, all rows outside S vanish too. Both adjacency directions have been used in this argument.

### Exact compressed matrix

For vectors u,v write u wedge v = uv^T-vu^T. Let e_x be the standard basis vector at coordinate x. Direct evaluation of the increments on the words in S gives

    K = sum_(r=1)^(m-2) [e_(a_r) wedge e_(b_(r+1))
                         -e_(a_(r+1)) wedge e_(b_r)]
      + sum_(r=0)^(m-2) [-e_(c_r) wedge e_(d_(r+1))
                         +e_(c_(r+1)) wedge e_(d_r)]
      + e_0 wedge (-e_(a_1)-e_(a_(m-1))+e_(b_1)+e_(b_(m-1)))
      + (-e_(a_1)+e_(b_(m-1))) wedge e_(N-1).                 (2.1)

For an independently reproducible way to check every boundary case in this evaluation, define V=L+L^T and W=PVP. For any x,

    K e_x = V W e_x - W V e_x
            + 1_(x=0)(e_1-e_(N/2))
            + (1_(x=N/2)-1_(x=1))e_0.                     (2.2)

Use V e_x=e_(x-1)+e_(x+1), with out-of-range terms omitted, and

    W e_x=e_(rev(rev(x)-1))+e_(rev(rev(x)+1)),

again omitting out-of-range terms. More explicitly, the only nonzero columns of the two generating commutators are

    [L,U] e_(d_r) = e_(c_(r+1))-e_(c_(r-1))   (0<=r<m),
    [L,U^T] e_(a_r) = e_(b_(r-1))-e_(b_(r+1)) (0<=r<=m),

with out-of-range subscripts omitted. Each commutator is zero on all other columns. The other two commutators are their negative transposes. Adding the endpoint term e_1 wedge e_0 - e_(N/2) wedge e_0 gives (2.1). These binary carry identities prove the formula for every m, rather than inferring it from numerical samples.

Equivalently, give a vector on S coordinates

    z=x_0, w=x_(N-1), alpha_r=x_(a_r), beta_r=x_(b_r),
    gamma_r=x_(c_r), delta_r=x_(d_r),

with gamma_0=alpha_1, gamma_(m-1)=beta_(m-1), delta_0=beta_1, and delta_(m-1)=alpha_(m-1). Formula (2.1) says Kx=0 exactly when

    beta_(r+1)-beta_(r-1)=0                  (2<=r<=m-2),
    alpha_(r+1)-alpha_(r-1)=0                (2<=r<=m-2),
    delta_(r-1)-delta_(r+1)=0                (1<=r<=m-2),
    gamma_(r+1)-gamma_(r-1)=0                (1<=r<=m-2),

and

    beta_2-delta_1+z-w=0,
    -beta_(m-2)+gamma_(m-2)+z=0,
    alpha_2-gamma_1-z=0,
    -alpha_(m-2)+delta_(m-2)-z+w=0,
    -alpha_1-alpha_(m-1)+beta_1+beta_(m-1)=0,
    alpha_1-beta_(m-1)=0.                                  (2.3)

Empty interior ranges at m=3 are allowed. Every row in this displayed system is nonzero, proving the asserted exact support.

### Uniform rank proof

The interior recurrences make each alpha, beta, gamma and delta sequence constant on its even and odd positions. The last two equations imply

    alpha_1=beta_(m-1),   beta_1=alpha_(m-1).

If m is even, all solutions are parameterized by two independent scalars a,z:

    w=2z;
    alpha_r=beta_r=a       for odd r;
    alpha_r=beta_r=a+z     for even r;
    gamma_r=delta_r=a      for all r.

Conversely these formulas satisfy all equations (2.3), including the endpoint identifications. Thus the compressed nullity is exactly 2 and its rank is (4m-4)-2.

If m is odd, all solutions are parameterized by four independent scalars a,b,z,w:

    alpha_odd=a, alpha_even=b;
    beta_odd=b, beta_even=a;
    gamma_even=a, gamma_odd=b-z;
    delta_even=b, delta_odd=a+z-w.

Again these satisfy every equation and endpoint identification, including m=3, so compressed nullity is exactly 4 and rank is (4m-4)-4. No division by 2 or another scalar was used. This also proves the stated field-independent rank assertion. QED.

## 3. An always-invertible correction matrix

Let E be the N-by-s coordinate inclusion for S, with s=4m-4, and let K_S=E^T K E. Then K=E K_S E^T. T, T', and B=TT' are invertible over Q.

Define

    G=E^T B^(-1) E,
    M=I_s-K_S G.

### Corollary 3.1

    det M=1,

and

    (B^T)^(-1) = B^(-1)
       + B^(-1) E M^(-1) K_S E^T B^(-1).                  (3.1)

Proof. The classical rectangular determinant identity gives

    det M = det(B-E K_S E^T)/det B
          = det(B^T)/det B = 1.

Consequently M is invertible. Multiplying (3.1) by B-E K_S E^T verifies the displayed inverse formula; equivalently it is the classical Woodbury identity. No inverse of the singular K_S is required. QED.

This correction matrix is not the odd-index principal block of TPT. Its determinant-one identity does not contradict that accepted pivot's singularity. Nor is it a certified complementary minor for a size-doubling proof of H_N. It is an exact factorization of the transpose correction for the same-size two-step dual transfer. The matrix inverse correction has rank rank K. As an operator on all N-by-N matrices, the correction in (4.2) has rank N times rank K, not merely rank K; the unknown space has not been reduced to logarithmic dimension.

## 4. The remaining observability condition, with no hidden lift assumption

Put q=t-1=N/4 and d=q/2=N/8. For any candidate dual matrix Z define

    Y_0=C^q Z^T,
    D(Y)=C^(-1)Y A.

Because A and C are invertible, Z is nonzero exactly when Y_0 is nonzero. The original dual constraints are exactly

    band_2(D^k(Y_0))=0, 0<=k<=q,                           (4.1)

where band_2 extracts every entry with |i-j|<=2. This is the original full band, including both orientations.

Let F=D^2. Then

    F(Y)=(B^T)^(-1)YB
        = B^(-1)YB
          + B^(-1)E M^(-1)K_S E^T B^(-1)YB.              (4.2)

Thus (4.1) is equivalent to the following two-channel half-length system:

    band_2(F^j(Y_0))=0       for 0<=j<=d,
    band_2(D F^j(Y_0))=0     for 0<=j<d.                   (4.3)

The exact remaining assertion is:

    For every m>=3, the only rational Y_0 satisfying (4.3),
    with the explicitly defined D,F,E,K_S,M above, is zero.

Theorem 2.1 and Corollary 3.1 do not prove this assertion. In particular:

- Invertibility of M permits exact evaluation of F; it does not make its band observations injective.
- The large kernel of K is not invariant under B in any way established here, and is not a kernel of (4.3).
- Dropping the correction term in (4.2), or dropping the odd-time observation in (4.3), changes the problem and is not justified.
- No nonzero H_N minor follows from the determinant-one correction identity alone.

Equation (4.3) is a precise unresolved bottleneck after the new factorization. Proving its injectivity uniformly, or finding a nonzero rational solution for some m, would settle the endpoint-family gate in the corresponding direction. A negative endpoint-family result would still not refute generic dominance in the original separated-generator chart.

### Optional symmetry reduction, exact but not an injectivity proof

Center the dual time instead: W=C^d Z^T A^d. Then the observations are band_2(D^ell W)=0 for -d<=ell<=d. Since

    (D^ell W)^T=D^(-ell)(W^T),

the kernel is the direct sum of its symmetric and skew-symmetric W sectors. Within either sector, nonnegative times 0,...,d suffice. This may reduce a later certificate, but supplies no rank conclusion by itself.

## 5. Verification scope

The reproducible checks independently reconstruct the exact T and actual binary reversal and compare their commutator with the full symbolic boundary matrix (2.1). They verify the all-size formula's transcription and the displayed kernel parameterizations; the proof is Sections 2-3, not the finite checks.

The checker does not construct H_N, compute a threshold Jacobian rank, rerun the accepted depth-two certificates, or use an auxiliary null vector as an H_N certificate. Source hashes and the exact check record are in the accompanying JSON files.

## 6. Final scope

This is a narrowly scoped structural result and an unresolved endpoint-rank disposition. M-SCAN-DIMENSION remains TO RESEARCH, priority 34. The original upper bound, finite threshold witnesses, depth-two theorem, good-anchor/tangent guards, and the previously accepted odd-sector obstruction are preserved. No assertion about the full owner's completion, Fourier membership, coefficient synthesis, execution savings, or historical priority follows.
