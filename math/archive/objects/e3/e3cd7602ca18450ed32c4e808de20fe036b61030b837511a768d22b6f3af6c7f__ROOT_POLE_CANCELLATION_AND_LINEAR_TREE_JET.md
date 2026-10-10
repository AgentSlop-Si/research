# A pole-free marked-tree reduction and a linear-work complete tree jet

## Result and boundary

The stationary Fourier graph has an exact root-pole cancellation that removes the artificial singularity at z=1 from its first tree elimination. The regularized tree operator K(z) has a complete polynomial vector jet with at most 2N-2 stored coefficients and can be applied, including all those coefficients, in O(N) arithmetic. The remaining coupled problem is an explicitly displayed bordered polynomial system of dimension N/2+1. No cheap inverse or fast top-coefficient extractor for that system is supplied.

This is one bounded constructive cancellation step, not a sub-N-log-N Fourier algorithm. It does not depend on treating a determinant, inverse, power, dense solve, or polynomial jet as one scalar operation.

## 1. Provenance and explicit starting operators

The research source was discovered through Library on 2026-10-10 at approximately 00:25 UTC, rather than supplied in the user's direct attachment batch. Its Library ID is [private-id]; filename fft_marked_cycle_theory_2026-10-10.zip; verified SHA-256:

    6f7e9f88d82f1242ffd58b7c84bb7a76ae39e4606eff52dc7838de99f93e438f

Only its README.md and THEORY.md were read for this construction. They are untrusted research claims pending independent review. No executable from the source archive was run. All verification below uses a freshly authored independent standard-library program.

Take N=2^n>=2 over a field with a supplied primitive Nth root omega, so its characteristic is not 2. Let m=N/2 and

    A_0 e_s = e_(2s mod N),
    A_1 e_s = omega^s e_((2s+1) mod N),
    Q=A_0+A_1.

Let J inject E^m into the odd coordinates of E^N, and define

    (C v)_r=omega^r(v_r-v_(r+m)),   0<=r<m.

Then A_1=J C by direct substitution. Here C denotes this half-size difference map, not the source's separately named final Fourier phase correction.

The source's stationary Fourier connection follows from the explicit paths: after n append-bit steps, exactly one path connects a given starting coordinate j to a given final coordinate r. Its weight is omega^(j rev_n(r)+phi(r)), where phi(0)=0, phi(2a)=phi(a), phi(2a+1)=phi(a)+a. Thus Q^n is the full Fourier transform after a supplied reversal and diagonal correction. Applying the existing sparse Q n times still costs Theta(N log N).

## 2. The polynomial regularized tree kernel

Define

    E=e_0 1_N^T,
    K(z)=sum_(t=0)^(n-1) z^t (A_0^t-E).                 (1)

The doubling tree gives A_0^n=E, A_0 E=E A_0=E, E^2=E. Therefore

    (I-z A_0) K(z)=I-E,
    K(z)e_0=0,
    1_N^T K(z)=0.                                      (2)

For z!=1, the ordinary tree inverse splits exactly as

    (I-z A_0)^(-1)=K(z)+E/(1-z).                        (3)

Unlike the inverse on the left, K is a polynomial and is defined at z=1. This removes only the known root eigenmode, not any input coordinate: its missing scalar mass will be retained explicitly below.

### An O(N) evaluation without division

To apply K(z) to x at any scalar z, initialize y_s=x_s for s!=0. Process every nonroot vertex s in increasing v_2(s), i.e. leaves toward the root. If parent(s)=2s mod N is nonzero, add z y_s to y_parent(s). Do not accumulate into coordinate zero. Finally set

    y_0=-sum_(s!=0) y_s.

The nonroot coordinates equal the nonroot coordinates of the polynomial (1); equation (2) fixes the root. This algorithm uses N-2 edge propagations, a root sum, and O(N) initialization/addressing, with no denominator and no exceptional z. In particular x_0 is deliberately removed by K; it returns through the scalar mass in Section 4.

The order can be generated directly: for h=0,...,n-1, visit s=2^h a for odd a<N/2^h. The total number of visits is N-1, rather than N visits per level.

## 3. Stronger constructive fact: the complete K(z)x jet costs O(N)

For constant input x, the nonroot coordinate y_s(z) has degree at most v_2(s). Its upstream tree has height v_2(s), and the preceding propagation shifts a child polynomial by exactly one degree. There are N/2^(h+1) nonroot vertices with v_2(s)=h. Consequently the capacity of all nonroot coefficient arrays is

    sum_(h=0)^(n-1) (h+1) N/2^(h+1)
       =2N-n-2.                                       (4)

The root polynomial has at most n coefficients. Thus all of K(z)x, through its full degree n-1, fits in at most

    2N-2 scalar coefficient slots.                     (5)

The leaf-to-root polynomial algorithm processes each child array once. Its total scalar additions are O(N) by (4), and forming the root polynomial has the same bound. There is no convolution, generic polynomial multiplication, or N-times-log-N coefficient array hidden in this tree computation.

For an arbitrary second constant vector h, the complete scalar polynomial h^T K(z)x also costs O(N): use the identity

    h^T K(z)x=sum_(s!=0) (h_s-h_0) y_s(z)

and the same coefficient budget. Applying C to the vector polynomial, or injecting a constant half-size input with J first, also preserves an O(N) coefficient-work bound. Root powers omega^r and all index tables require O(N) separately charged preparation.

This claim specifically starts with constant-coordinate input vectors. It does not say that K applied to an arbitrary full-degree polynomial vector costs O(N), nor that closing feedback preserves the coefficient sparsity in (5).

## 4. Exact pole-free bordered solve

Set

    H_tilde(z)=C K(z) J,
    M(z)=I_m-z H_tilde(z),

and form the explicit (m+1)-dimensional bordered operator

              [ M(z)       -e_0 ]
    B(z)  =   [                  ].                    (6)
              [ -z 1_m^T    1-z ]

For a given x, solve

    B(z) [u;t] = [C K(z)x; 1_N^T x].                   (7)

Then recover

    y=K(z)x+z K(z)J u+t e_0.                           (8)

Equations (7)-(8) are equivalent to

    (I-zQ)y=x                                           (9)

whenever either corresponding system is invertible. They remain algebraically valid at z=1. No division by 1-z occurs.

Proof. Starting from (9), write u=C y and t=1_N^T y. Project (9) onto the zero-sum subspace and use (2); this gives (8). Applying C to (8), using C e_0=e_0 in E^m, gives the first block equation of (7). Taking total coordinate sums in (9), using 1_N^T A_0=1_N^T and 1_N^T J=1_m^T, gives the last block equation. Conversely, (7) and (8) imply C y=u and 1_N^T y=t. Multiplying (8) by I-z A_0 and substituting the last block equation gives x+zJ u, establishing (9). All operations are valid without dividing by 1-z.

### Exact determinant cancellation

The determinant identity is

    det B(z)=det(I-zQ).                                 (10)

For z!=1, (3) yields

    C(I-z A_0)^(-1)J=H_tilde(z)+e_0 1_m^T/(1-z).

The usual determinant Schur identity, together with det(I-z A_0)=1-z, gives both sides of (10) as

    (1-z) det(M(z)-z e_0 1_m^T/(1-z)).

Both sides of (10) are polynomials. Equality as rational functions proves equality at z=1 as well. Thus the exact guard for the bordered solve is det(I-zQ)!=0; an extra branch guard 1-z!=0 is unnecessary.

If one elects to solve by inverting M first, that creates an additional chart condition and remaining scalar denominator. Write a=1_m^T M^(-1)e_0 and b=1_m^T M^(-1)C Kx. Then

    t=(1_N^T x+z b)/(1-z-z a),
    u=M^(-1)(C Kx+t e_0).

This is optional. M can be singular even when the full border is invertible, so it must not be silently assumed invertible. No cheap M inverse is proved here.

### Explicit N=2 control at the formerly singular parameter

For N=2, omega=-1, z=1,

    Q=[[1,1],[1,-1]],       B(1)=[[3,-1],[-1,0]],
    (I-Q)^(-1)=[[-2,-1],[-1,0]].

Thus the algorithm gives y_0=-2x_0-x_1 and y_1=-x_0. Both determinants equal -1. This works also in characteristic 3: the upper-left block M=[3] is then singular, but the bordered system remains invertible. The control demonstrates why the full border is preferable to an unguarded M-inversion shortcut.

## 5. The marked quantity survives exactly, with the expensive operation exposed

For arbitrary constant marker vector h, let

    b_x=[C Kx; 1_N^T x],
    a_h^T=[z h^T KJ, h_0].

Equations (7)-(8) give the exact bilinear identity

    h^T(I-zQ)^(-1)x
       =h^T Kx+a_h^T B(z)^(-1)b_x.                    (11)

The first scalar polynomial is available in O(N) by Section 3. The right input b_x is also a linear-work complete tree jet. The remaining operation is specifically the coupled bordered inverse contribution a_h^T B^(-1)b_x, or its coefficient of z^n, not an unmarked determinant or an already cheap tree inverse.

Since

    [z^n] h^T(I-zQ)^(-1)x=h^T Q^n x,

a genuinely faster scalar circuit for the needed coefficient, retaining h as markers until differentiation, would still have to solve the same full Fourier task described by the source. Formula (11) does not provide that circuit. Materializing a generic full vector resolvent jet through degree n would use N(n+1) coefficient slots; this is an implementation cost warning, not a lower bound against a circuit that extracts only the required coefficient.

Applying the operator B(z) at one scalar parameter is O(N), using K, C, J, and the scalar sums. A cheap matrix-vector product does not imply a cheap inverse. The dense border solves in the verifier are explicitly test oracles. No inverse call, determinant node, power, polynomial jet, or automatic-differentiation step is counted as a single scalar operation.

## 6. Exact independent controls

The authored verifier checks 58 combinations over GF(97), GF(65537), and the N=2 GF(3) exceptional-block example, for N through 64. They include 12 evaluations at z=1 and 174 exact arbitrary-input recovery checks, each with an independent dense solve as the test oracle. It verifies:

- the K identities (2), zero root column, and zero column sums;
- the full polynomial coefficient budget 2N-2 and agreement with scalar evaluation;
- det B=det(I-zQ), including the root-pole parameter;
- (7)-(8) against (9);
- the marked bilinear identity (11), with 174 controls;
- an invertible border with singular M over GF(3).

These bounded field checks supplement the self-contained algebra; they are not the Fourier application algorithm and do not establish a performance claim. Existing seals and the pending source reviews are unchanged.

Companions: verify_root_pole_cancellation.py, ROOT_POLE_CANCELLATION_CONTROLS.json, ROOT_POLE_CANCELLATION_SHA256SUMS.txt.
