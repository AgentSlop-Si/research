# Full CRT chirp lift: exact coupling, charged recurrences, and a shared-pole obstruction

## Result and scope

There is a genuine full-matrix CRT identity and a genuine full-matrix shifted-resolvent decomposition. Neither supplies a bounded Green bank or a speedup. The coupling left behind by a five-coordinate synthesis is explicitly a smaller Fourier/chirp transform.

For the most direct lift of the accepted two-reciprocal-cycle-plus-diagonal formula, there is a new uniform obstruction. If each coupled 5×5 block is synthesized using one reciprocal pole pair selected from a common bank, even allowing its endpoint vectors to depend freely on that entire block, then at N=5q² the bank needs at least

    max(0, ceil((q−8)/5))

distinct reciprocal pole pairs. Thus this selected ansatz cannot have a bounded or o(log N) bank. For the admitted restricted-family parameter q=483, the bound is 95 pole pairs. This is not an exclusion of arbitrary global Green sums, arbitrary orders, or several pole pairs summed inside each block.

There is also a separate compatibility obstruction: a bank of fixed 5×5 kernels with row-fiber/column-fiber separable endpoint arrays needs at least floor(q²/2) individual kernels. Adding an arbitrary scalar coupling matrix can evade that rank bound, but the full CRT identity identifies those couplings as Fourier/chirp matrices; their applications and coefficient generation must be paid for.

A fresh standard-library checker proves the rational invariant and exception count in Q(ζ5), checks the complete N=15 inverse over Q(ζ15), and checks full CRT identities at N=15,45,65,245. At N=45, five exact modularly distinct forced pole traces give a concrete five-pair lower bound for the direct blockwise ansatz. At N=245 there are 39 such traces. These finite controls supplement the uniform proof; they are not extrapolated into it.

## 1. Definitions and the full CRT equations

Let N=5m be odd with gcd(5,m)=1. Work first over the complex numbers with a specified primitive Nth root ω. Set

    h_n = 2⁻¹ mod n,
    F_n[i,j] = ξ_n^(ij),
    A_n[i,i] = ξ_n^(h_n i²),
    D_n = A_n⁻¹,
    H_n[i,j] = ξ_n^(−h_n(i+j)²),
    G_n = Σ_j ξ_n^(h_n j²),
    c_n = n G_n.

The roots used below are specified by CRT, not chosen independently afterward. Let

    e5 = m (m⁻¹ mod 5),   em = 5 (5⁻¹ mod m),
    η = ω^e5,            θ = ω^em,
    j(a,b) = e5 a + em b mod N.

Thus j(a,b) reduces to a modulo 5 and b modulo m. In CRT coordinates, with tensor factors ordered as (a,b),

    F_N = F_5 ⊗ F_m,
    A_N = A_5 ⊗ A_m,
    D_N = D_5 ⊗ D_m,
    H_N = H_5 ⊗ H_m,
    G_N = G_5 G_m,        c_N = c_5 c_m.                 (1)

These are entry identities: the orthogonal idempotents satisfy e5²=e5, em²=em, e5 em=0 modulo N. The inverse of two also reduces correctly in both factors.

The full forced inverse, in the same coordinates, is

    B_N = [F_5⊗F_m − G_N H_5⊗H_m
           + c_N D_5⊗D_m] / (1+c_N).                  (2)

This is an identity on all N² entries, not a statement about a principal restriction. It follows from (F_N A_N)³=c_N I and B_N=(F_N⁻¹+A_N)⁻¹. Over C, |c_N|=N^(3/2), so its denominator is nonzero. Over finite fields that denominator is checked rather than inferred from the complex argument.

Now order the coordinates fiber-first: x_b consists of the five entries x_(a,b). The complete coupled 5×5 block from input fiber d to output fiber b is

    B[b,d] = [F_m[b,d] F_5 − G_N H_m[b,d] H_5
              + c_N δ_bd D_m[b,b] D_5] / (1+c_N).     (3)

In particular, its off-diagonal-in-a data is a nonzero scalar multiple of F_5+ρ_bd H_5, where

    ρ_bd = −G_N H_m[b,d]/F_m[b,d]
         = −G_N θ^(−h_m(b+d)²−bd).                   (4)

The diagonal term in (3) is present only when b=d. This equation identifies exactly which endpoint data and poles have to agree across the coupled blocks.

### The square-length residue decomposition

For the family m=q², let ζ=θ^q and write b=s+qr, d=t+qu with 0≤s,t,r,u<q. Direct expansion gives

    F_m[s+qr,t+qu] = θ^(st) ζ^(rt+su),
    H_m[s+qr,t+qu] = θ^(−h_m(s+t)²) ζ^(−(s+t)(r+u)).  (5)

Each fixed-(s,t) q×q block has rank one, but the full transform does not. Also

    G_(q²) = Σ_s θ^(h_m s²) Σ_r ζ^(sr) = q.           (6)

Hence G_N=qg and c_N=5q³g, with g=1+2(η²+η³), agreeing with the accepted restricted family. Here η=ω^(q⁴), because q⁴ is exactly the CRT idempotent e5 modulo 5q².

## 2. What cheap, compatible endpoints would mean

Consider the explicit shared-kernel ansatz

    B[b,d] = δ_bd E_b
           + Σ_(s=1)^r diag(u_s[b]) K_s diag(v_s[d]),  (7)

where E_b is diagonal, each K_s is a fixed 5×5 Green kernel or other fixed 5×5 matrix, and endpoint vectors depend only on the output fiber b or input fiber d respectively. This is stronger compatibility than choosing separate endpoints for every pair (b,d), and it is exactly what permits the tempting O(rN) preaggregation:

    z_s = Σ_d diag(v_s[d]) x_d,
    w_s = K_s z_s,
    y_b = E_b x_b + Σ_s diag(u_s[b]) w_s.

But each summand in (7), viewed as a full N×N matrix, has rank at most five. More sharply, let R={0,...,floor(m/2)−1} be a set of residue labels and I consist of all five coordinates in fibers R. Then

    rank B_N[I,Iᶜ] = 5 floor(m/2).                    (8)

Indeed, for any invertible matrix T, a complementary off-diagonal cut has the same rank in T and T⁻¹. Apply this to B_N. Its inverse cut is the cut of F_N⁻¹, since A_N is diagonal; (1) makes this F_5⁻¹⊗F_m⁻¹[R,Rᶜ]. The second factor has full row rank floor(m/2), by a Vandermonde minor on consecutive row exponents. The first factor has rank five.

Equation (7) therefore requires

    5r ≥ 5 floor(m/2),  or  r ≥ floor(m/2).            (9)

Singular endpoints and zero-edge kernels do not change this argument. An actual global diagonal correction contributes nothing across this cut.

A separate correction diag(Δ_bd) for every 5×5 block is NOT a global diagonal when b≠d. It is five independent m×m coupling matrices. Treating those corrections as N scalar multiplications would lose their cost and their off-diagonal-fiber coupling.

One can instead enlarge (7) by a coupling coefficient C_s[b,d] multiplying each summand. This evades (9) if C_s has sufficiently high rank. Equation (2) does exactly that using three fixed small kernels, with coupling matrices F_m, H_m and D_m. It is a useful three-kernel description, but application of those coupling matrices is not a free endpoint operation.

A related cycle-order consequence is also immediate. A global Hamiltonian cycle that visits the five coordinates of each fiber consecutively and visits fibers in their common cyclic residue order has one outgoing crossing of I. A sum of r diagonal-ended Green maps on such orders needs r≥5 floor(m/2). Arbitrary intrafiber permutations, cycle rotations, reverse residue order, poles and zero weights do not remove the crossing bound. Arbitrary global orders are not covered by this restriction.

## 3. A forced reciprocal-pole invariant for the five-coordinate block

This section relaxes endpoint compatibility entirely. It still obstructs a small pole bank for the direct use of the accepted construction.

Let K=Q(η), η a primitive fifth root, and let

    C(ρ) = F_5 + ρ H_5.

Its off-diagonal data is

    a = C01 = C04 = 1+ρη²,
    b = C02 = C03 = 1+ρη³,
    c = C12 = C34 = η²+ρη³,
    e = C13 = C24 = η³+ρη²,
    f = C14 = η⁴+ρ,
    h = C23 = η+ρ.                                   (10)

Multiplying the whole target by a nonzero scalar does not affect the pole invariant. Its five diagonal entries are irrelevant because the chosen ansatz permits a diagonal correction.

Suppose there are t≠0,1 and vectors u,v such that

    C(ρ)[i,j] = u_i v_j + t v_i u_j,   i<j.            (11)

This is precisely the upper-triangular condition for one reciprocal pair of natural-order Green kernels plus a diagonal correction. The pole pair {t,t⁻¹} is unchanged by swapping the two summands.

Define polynomial quantities, all in K[ρ],

    A=cab, B=eab, C=fb², E=ha²,
    S=A+B, U=2C−S,
    L=B²−CE,
    M=−2AB+AC+AE+BC+BE−2CE,
    J=(B−C)²,
    V=LU²−MUC+JC².                                  (12)

The use of C as a polynomial in (12) is separate from the matrix C(ρ). Define the guard polynomial

    Q(ρ)=ab C(A−B)(B−C)(C−S)L V.                      (13)

It has degree 32 but only eight distinct roots over an algebraic closure. The latter statement is an exact polynomial identity: the checker computes gcd(Q,Q′) in K[ρ], divides Q by it, and obtains the degree-eight squarefree polynomial recorded in GLOBAL_LIFT_RESULTS.json. No numerical root count is used.

Whenever Q(ρ)≠0, equation (11) forces

    t+t⁻¹ = R(ρ) = n(ρ)/d(ρ),                         (14)

where n,d are relatively prime degree-five polynomials. In the basis (1,η,η²,η³), their coefficients in increasing powers of ρ are:

    n:
    ( 7, 10, 10, 0)
    ( 7,  8,  8, 2)
    ( 3,  8, 10, 4)
    (−5, −8, −4, 2)
    (−1, −8, −6, 0)
    (−3,−10,−10, 0)

    d:
    ( 1, 0, 0, 0)
    ( 1,−1,−1, 1)
    (−1,−1, 0, 2)
    ( 0, 1, 3, 1)
    ( 2, 1, 2, 0)
    ( 1, 0, 0, 0).                                  (15)

In particular R is nonconstant under every primitive-fifth-root embedding.

### Why the trace is necessary, including singular endpoints

Set α=c/(ab), β=e/(ab), γ=f/a² and ε=h/b². The common denominator is a²b², so (12) is exactly the denominator-cleared version of the quadratic reconstruction in the accepted five-coordinate certificate.

Since a,b are nonzero, u0 and v0 cannot both vanish. Replacing (u,v,t) by (v,t u,t⁻¹) if needed preserves every entry; then rescaling the two endpoint vectors inversely puts u0=1. Write z=t v0, r_i=u_i/C0i and κ=(1+t)z. Then all normalized off-diagonal equations for indices at least one are

    r_i+t r_j−κr_i r_j.

Put x=r1 and δ=t−κx. Since β≠γ, δ cannot vanish. The equations with index 1 give

    r2=(α−x)/δ, r3=(β−x)/δ, r4=(γ−x)/δ.

Since α≠β, subtracting the (2,4) and (3,4) equations forces κr4=1+δ. If κ=0, these equations force t=−1 and γ=α+β, contrary to C−S≠0. Thus κ≠0, and

    κ=(t+δ²)/γ,
    t[γ(δ+2)−α−β]=γδ+(α+β)δ².                       (16)

The last remaining off-diagonal equation is equivalent to

    (β²−γε)δ²
    +(−2αβ+αγ+αε+βγ+βε−2γε)δ
    +(β−γ)²=0.                                     (17)

The resultant of (17) and the denominator in (16) is V, up to the already nonzero common denominators. Thus V≠0 makes that denominator nonzero at either quadratic root. No assumption that all endpoint entries are nonzero was used.

In the quadratic algebra, put p1=M/L, p0=J/L. The numerator of t after reducing δ² is a0+a1δ with

    a0=−S J/L, a1=C−S M/L;

the denominator is U+Cδ. Its trace is therefore

    [2a0U − p1(a0C+a1U) + 2p0a1C]
    / [U²−p1UC+p0C²].                               (18)

The norm of t is one. This follows by the expanded polynomial identity

    J(C²L−CSM+S²J)
      = C²JL−CUM L+U²L².

Therefore the field/algebra trace in (18) is t+t⁻¹, even if the quadratic splits. Clearing denominators in (18) yields

    N0 = −2SJU L − M[−SJC+(CL−SM)U]
         + 2J(CL−SM)C,
    D0 = LV.                                        (19)

The checker independently verifies N0 d=D0 n, their degree-13 common factor, gcd(n,d)=1, and that n is not a constant multiple of d. This establishes (14) as a necessary invariant for every representation in the specified natural-order reciprocal-pair ansatz at every nonexceptional ρ. It is not merely the pole produced by one convenient reconstruction chart.

## 4. Uniform obstruction to reusing a bounded pole bank

Suppose a bank contains pole pairs {t_s,t_s⁻¹}, 1≤s≤r, and every coupled block (3) is realized by one pair from the bank in form (11), with its own completely unrestricted endpoint vectors and diagonal correction. This is a relaxation of a globally compatible lift, so an obstruction here also obstructs that more restrictive mechanism.

Each pair has one trace τ_s=t_s+t_s⁻¹. For any fixed τ in any extension field, the equation

    n(ρ)−τ d(ρ)=0

is a nonzero polynomial of degree at most five, because n/d is nonconstant. Thus one pole pair handles at most five distinct nonexceptional block parameters.

At m=q², take b=0 and d=0,...,q−1. Equation (4) gives

    ρ_0d = −qg θ^(−h_m d²).

These q parameters are all distinct: 0≤d²<q², their ordinary integer squares are distinct, h_m is a unit modulo q², θ is primitive, and qg≠0. At most eight can be roots of Q. Consequently

    5r ≥ q−8,
    r ≥ max(0,ceil((q−8)/5)).                        (20)

This holds for every positive odd q coprime to 5, in particular for the accepted q≡1 mod 241 family. It is Ω(q)=Ω(√N). Exceptional points are handled conservatively by discarding all eight; no existence or regularity at them is assumed.

The conclusion is deliberately about the selected bank model. It does not constrain a single arbitrary global weighted cycle merely because its subblocks are 5×5; off-diagonal subblocks of such a cycle need not themselves have the common-pole form (11). It also does not rule out combining multiple bank pairs within each block, changing the internal five-coordinate order per block, or using different global routings. Those are different construction problems.

## 5. A genuine full shifted-resolvent lift, and its actual cost

For λ define

    B_m(λ)=(F_m⁻¹+λA_m)⁻¹
          =[F_m−λG_m H_m+λ²c_mD_m]/(1+λ³c_m).       (21)

Let M5=F5 A5. Since M5³=c5 I, its three distinct possible eigenvalues λ_j are the roots of x³−c5. Over a splitting extension, its spectral projectors are

    P_j = (I+λ_j⁻¹ M5+λ_j⁻² M5²)/3.

They are explicit constant-size matrices. Let d_j=rank P_j; Σ_j d_j=5. The exact full identity is

    B_(5m)(λ) = Σ_(j=1)^3 (P_j F5) ⊗ B_m(λλ_j).     (22)

Indeed, left-multiplying F_N⁻¹+λA_N by F5⊗I yields I⊗F_m⁻¹+λM5⊗A_m, which is block diagonal under the projectors. This derivation retains the endpoint order P_j F5.

The smaller inverse guards are all identical to the full one:

    1+(λλ_j)³c_m=1+λ³c5c_m.

Thus over C at λ=1 all are nonzero. No independent unshifted B5 or Bm inverse is needed. In the finite N=15, p=31 control, the unshifted B5 is in fact resonant, while the full and required shifted inverses exist; the checker correctly avoids assuming an unneeded inverse.

Factor each constant-size P_j F5=U_j V_j with d_j columns/rows. This needs bounded field arithmetic and produces a real implementation: use V_j to form d_j length-m input channels, apply B_m(λλ_j) independently to them, and use U_j to recombine. If T_m(μ) is the cost per arbitrary-input shifted solve and S_m(μ) is its setup, then

    T_(5m)(λ) ≤ Σ_j d_j T_m(λλ_j) + O(N),
    S_(5m)(λ) ≤ Σ_j S_m(λλ_j) + O(N) + R5.           (23)

R5 includes generating the constant-degree splitting extension/projectors. Root extraction is not declared a free field operation. One may specify the constant-degree algebraic coefficients symbolically, or charge an exact root-generation procedure in the chosen model. Applying them over the extension must also be charged. The root-free formula (2) avoids this extension entirely.

Equation (23) is a conditional full lift, not a closed recursion solved by the accepted B5 certificate: that certificate supplies neither the arbitrary-length shifted B_m(μ) solvers nor their parameter generator. Further CRT factoring is possible only for coprime factors; q² cannot be silently split as the CRT product q×q.

### Root-free charged application

H_m=D_m Fbar_m D_m, and Fbar_m is a row reversal of F_m. Thus (2), with constant-size five-coordinate kernels, costs

    T_B(5m) ≤ 10 T_F(m) + O(N).                      (24)

The setup satisfies S_B(5m)≤S_F(m)+O(N) when the same stored length-m transform plan is reused. There are five length-m Fourier actions for each of its first two tensor terms, plus constant-size fiber actions, chirps, additions and permutations. Sharing a named kernel is not sharing an arbitrary-input transform across five independent channels.

Formula (5) gives the ordinary two-stage residue application

    T_F(q²)=2q T_F(q)+O(q²),                          (25)

with q transforms over u, a q²-entry twiddle table, and q transforms over t. The setup recurrence is S_F(q²)≤S_F(q)+O(q²) with one reused subtransform plan. The twiddle table is generated by rowwise geometric progressions in O(q²), not materialized for free. The inverse/square chirps and Gauss scalar have O(N) phase recurrences; the CRT roots/idempotents require modular arithmetic and O(log N) powering, both inside the O(N) setup budget.

Consequently the explicit root-free construction here satisfies

    T_B(5q²) ≤ 20q T_F(q)+O(N).                       (26)

For the Fourier transform itself, CRT plus (25) gives 10q T_F(q)+O(N). Recursing the square decomposition on q=p^(2^k) with fixed p produces the standard Θ(N log N) recurrence, not a sublogarithmic-scan improvement. Replacing T_F(q) by three calls to an as-yet-unknown B_q implementation does not discharge the obligation.

A hypothetical genuine full Green family with k_N branches and coefficient generator S_N would still have to charge O(S_N+k_N N+N), and Fourier recovery makes three B calls. Neither the restricted B5 certificate nor the polynomial-size pole bank derived here supplies k_N=o(log N) and S_N=o(N log N).

## 6. Exact controls and reproducibility

Run, from this directory:

    python check_global_lift.py

The script imports only Python standard-library modules, not exploratory scripts or any predecessor/uploaded source. It expands the universal reconstruction-residual and reciprocal-norm identities as integer multivariate polynomials, reconstructs the polynomial quantities from (10)–(13), and checks the invariant coefficient identity, relative primality, nonconstancy and the eight-root exception bound. It checks the claimed pole trace in the quadratic algebra for every good finite-field block. When the additional endpoint-reconstruction norms are nonzero, it reconstructs both-root endpoint data and checks all ten upper entries. A guard for a necessary invariant is not claimed sufficient for legal synthesis; reductions with a zero additional norm are recorded as trace-only controls. Its rational arithmetic is in an explicitly implemented cyclotomic field.

It checks the entire 15×15 forced inverse in Q[x]/Φ15(x), where

    Φ15(x)=x⁸−x⁷+x⁵−x⁴+x³−x+1.

Both products with F15⁻¹+A15 equal the identity, checking 450 characteristic-zero entries. It also computes two different exact block traces in that field.

The finite controls are:

- N=15 over F31, ω=9: two distinct required pole traces, complementary fiber-cut rank 5, full two-sided inverse and shifted-resolvent identity.
- N=45 over F181, ω=16: five distinct required traces, cut rank 20, full two-sided inverse and shifted-resolvent identity.
- N=65 over F131, ω=4: 13 distinct traces and cut rank 30.
- N=245 over F491, ω=4: 39 distinct traces and cut rank 120.

All four check every N² entry of the CRT formula. The N=65 and N=245 cases do not run a full two-sided dense inverse check; they verify the explicit target, CRT entries and cuts. The full inverse identity is already proved uniformly and checked independently in characteristic zero at N=15 and modulo 181 at N=45.

For N=45, exact trace witnesses include:

    (b,d,ρ,trace) = (0,0,81,38), (0,1,145,10),
                   (0,2,135,120), (0,4,82,9),
                   (1,1,87,166).

All witness guards are nonzero modulo the listed prime. Therefore these unequal traces and nonzero guards lift to characteristic zero under the corresponding primitive-root specialization. They prove the stated finite lower bounds for the chosen ansatz, without claiming those numbers of pairs suffice.

GLOBAL_LIFT_RESULTS.json records every trace witness, polynomial coefficient, spectral multiplicity and checked scope. REPRODUCE.md identifies the commands and file provenance. The exploratory routes and their failures are preserved separately. Independent review remains a separate task.

## 7. What remains open

This work completes a global algebraic decomposition and gives two precise obstructions to natural ways of turning repeated five-coordinate formulas into a cheap compatible bank. It does not produce an FFT improvement or prove one impossible.

A different positive attempt would need full-N cycles and endpoint arrays that escape both the separable-endpoint rank constraint and the single-pair-per-block pole invariant, together with a generator whose cost includes every coupling coefficient. A sum of several differently ordered block kernels or a genuinely global cycle family could escape the selected ansatz; no compatibility or cheap application has been established for either here.
