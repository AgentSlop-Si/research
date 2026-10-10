# An explicit infinite family of restricted chirp matrices with exactly three Green terms

## Result

The suggested extension is valid. Let q be a positive odd integer, coprime to 5, with q ≡ 1 modulo 241. Put N=5q², let ω be any specified primitive Nth root, and set η=ω^(q⁴). Then η has order five. With

- g=1+2(η²+η³), so g²=5;
- F[i,j]=η^(ij), H[i,j]=η^(−3(i+j)²), and D[i,j]=η^(−3i²)δij;
- C_q=(F−qgH+5q³gD)/(1+5q³g),

the five-by-five matrix C_q has an explicit representation by **exactly three** diagonal-ended weighted Hamiltonian-cycle Green summands. Two summands use the same natural structural cycle, with reciprocal nonzero closing weights. The third has all edge weights zero and supplies a diagonal correction. All endpoint diagonals in the displayed construction are nonsingular. Every inverse and reconstruction denominator is nonzero at either quadratic root and under every primitive fifth-root embedding.

The upper bound is proved constructively below. Exact minimality uses the separately accepted two-summand exclusion for C_q. This is a uniform infinite family of **five-coordinate matrices**, not a three-term construction for the full N-by-N B_N. Only the lower bound passes from this block to B_N. No full FFT speedup follows from this result alone.

For the explicit sequence q=2410k+1, k≥0, the conclusion applies for every k. The broader stated congruence family includes q=483 as its smallest positive q>1, giving N=1,166,445; the block, not that million-dimensional full matrix, is synthesized here.

## 1. The target and its reversal symmetry

The accepted principal-restriction theorem gives, in the coordinate order S=(0,q²,2q²,3q²,4q²),

B_N[S,S]=C_q, where B_N=(F_N^−1+A_N)^−1 and A_N[j,j]=ω^((N+1)j²/2).

The CRT/Gauss identity is G_N=qg. Thus every scalar in C_q is retained; C_q is not B_5 when q>1. The target denominator is nonzero because

(1+5q³g)(1−5q³g)=1−125q⁶ ≠ 0.

Both off-diagonal kernels are symmetric and unchanged by (i,j)↦(−i,−j) modulo five. Consequently the six off-diagonal data have the required form

C01=C04=a, C02=C03=b, C12=C34=c,
C13=C24=e, C14=f, C23=h.

There is no assumption on the five diagonal entries. Their q³ dependence is absorbed by the diagonal correction, whose invertibility is also certified.

## 2. Uniform rational reconstruction from one quadratic

Everything in this section is computed from C_q, not copied from q=1 coefficients. Let K=Q(η), and set

α=c/(ab), β=e/(ab), γ=f/a², ε=h/b²,
L=β²−γε,
M=−2αβ+αγ+αε+βγ+βε−2γε,
J=(β−γ)².

Take either root d of

P(d)=Ld²+Md+J=0,

or, equivalently, d²+p1 d+p0=0 with p1=M/L and p0=J/L. Section 3 proves that L and every subsequent denominator are nonzero and that this monic quadratic is irreducible over K for every admitted q.

Define

T=γ(d+2)−α−β,
t=[γd+(α+β)d²]/T,
κ=(t+d²)/γ,
x=(t−d)/κ,
r1=x, r2=(α−x)/d, r3=(β−x)/d, r4=(γ−x)/d,
z=κ/(1+t),
u0=1, ui=C_q[0,i]ri for 1≤i≤4,
v0=z/t, vi=C_q[0,i]−zui for 1≤i≤4.

Then, for i<j,

C_q[i,j]=ui vj+t vi uj.

Here is the algebraic justification, independent of any finite sampling. For indices ≥1 the normalized right-hand side is ri+t rj−κri rj. The relations d=t−κx and κr4=1+d give the equations involving index 1 and the difference between the (2,4) and (3,4) equations. The (3,4) equation is the definition of t. After these equations, the remaining (2,3) residual is P(d)/(dT). The numerator identity is

(β−γ)[βd²+(β−α)d+β−γ]−(ε−β)d[γd+2γ−α−β]=P(d).

The four equations involving index 0 follow directly from vj+t v0 uj=C_q[0,j]. The fresh checker expands the residual identity as an integer multivariate polynomial.

Let W_t have row-successor weights (1,1,1,1,t), let W_(1/t) have weights (1,1,1,1,1/t), and let W_0 have all five weights zero, on the same structural cycle. Set Δ_i=C_q[i,i]−(1+t)ui vi. The three actual summands are

C_q=(1−t)diag(u)(I−W_t)^−1diag(v)
    +(t−1)diag(v)(I−W_(1/t))^−1diag(u)
    +diag(Δ)(I−W_0)^−1 I.

For the natural cycle, (I−W_s)^−1=H_s/(1−s), where H_s equals 1 on and above the diagonal and s below it. The upper off-diagonal entries are precisely the identities just proved; the lower entries follow by symmetry; the diagonal is corrected by Δ. This proves every matrix entry.

### Reciprocal roots, not just reciprocal branches

The two roots of the quadratic also give conjugate poles t and 1/t. This holds for the general synthesis formulas, not just for q=1. Put s=α+β. In the quadratic field,

Norm(d)=J/L,
Norm(γ+sd)=γ²−γsM/L+s²J/L,
Norm(γd+2γ−s)=γ²J/L−γ(2γ−s)M/L+(2γ−s)².

The integer polynomial identity

J(γ²L−γsM+s²J)
=γ²JL−γ(2γ−s)ML+(2γ−s)²L²

shows that numerator and denominator of t have the same norm. Therefore Norm(t)=1, and conjugation sends t to 1/t. The checker independently expands this identity.

## 3. One local certificate proves every guard for every q

Let O=Z[η], 𝔭=(241,η−91), and R=O_𝔭. This is the discrete valuation localization of the fifth cyclotomic integer ring. Its fraction field is K and its residue field is F241. The cyclotomic relation vanishes at 91, and 91 has order five.

For every integer q≡1 modulo 241, the target denominator reduces to 34 and is therefore a unit of R. All entries of C_q lie in R and reduce to the same target

[[161,20,102,102,20],
 [20,182,62,26,92],
 [102,62,236,28,26],
 [102,26,28,236,62],
 [20,92,26,62,182]].

This is a polynomial congruence, not an inference from tested q values. In particular q=1+241k and q³ both reduce to the constant 1 in F241[k]. The checker explicitly checks the target's 25 numerator congruences and its constant denominator.

The six base-field guard residues are

(a,b,γ,β−γ,L,discriminant)=(20,102,234,89,163,163).

Consequently they are units in R. The monic root polynomial has coefficients in R and reduces to

d²+30d+124,

whose discriminant is 163. Since 163^120=−1 modulo 241, the reduction is irreducible. The characteristic-zero polynomial is irreducible over K: a root in K would be integral over the integrally closed local ring R, hence belong to R and reduce to a forbidden residue-field root. Thus E_q=K[d]/(d²+p1d+p0) is a quadratic field, of degree eight over Q.

Perform the reconstruction successively in the rank-two algebra S_q=R[d]/(d²+p1d+p0). For y=A+Bd, its norm is A²−p1AB+p0B². Whenever this norm has nonzero residue it is a unit of R, and the usual conjugate-over-norm formula makes y a unit of S_q. The following norm residues verify every remaining division in construction order:

- Norm(d)=124
- Norm(T)=139
- Norm(κ)=53
- Norm(t)=1
- Norm(1+t)=160
- Norm(1−t)=85

All 15 endpoint norm residues are nonzero as well:

- u: (1,44,153,153,44)
- v: (41,117,7,7,117)
- Δ: (72,113,64,64,113)

These residues are obtained by evaluating the reconstruction in the quadratic residue field, equivalently reducing its exact q=1 values. They persist for every q≡1 because each preceding inverse is a unit and therefore commutes with reduction. This induction is the essential uniform argument: an isolated successful complex specialization would not suffice.

The nonzero norms in K prove that neither complex root can make a guarded expression vanish. Nonzero field elements remain nonzero under each of the four embeddings η↦η^a, a=1,2,3,4. Thus all inverse, reconstruction and endpoint guards hold simultaneously at all eight embeddings of E_q. The Green denominators 1−t and 1−1/t are units because t and 1−t are units.

The same algebraic construction works for any integer q≡1 modulo 241. Oddness and coprimality with 5 are needed to identify C_q with the stated principal block of B_(5q²), rather than for the five-dimensional synthesis itself.

## 4. What is proved for the full matrices

The accepted proper-specialization certificate excludes two Green terms for C_q, including arbitrary Hamiltonian structural orders, zero edges and singular diagonal endpoint masks. The three legal summands above therefore prove that its minimum is exactly three in that grammar.

Any allowed full B_N representation restricts to one for C_q. Hence the full B_N requires at least three summands. The converse implication is false in general: factors specified only on five retained coordinates say nothing about the other N²−25 target entries. This report supplies no full B_N factors and makes no claim that three suffice for B_N when q>1.

The 5×5 C_q must also not be inserted into the F5 reconstruction formula from the q=1 certificate. For q>1 it is not the same forced inverse (F5^−1+A5)^−1. Fourier reconstruction below is conditional on an actual full B_N representation.

## 5. Precisely what a full constructive family would still need

### Global identities

For the same two-natural-cycle-plus-diagonal ansatz at length N, the missing condition is the existence of a single pole t_N≠0,1 and complete vectors u,v such that

B_N[i,j]=u_i v_j+t_N v_i u_j for every i<j,

together with Δ_i=B_N[i,i]−(1+t_N)u_i v_i. These conditions are necessary and sufficient for that exact ansatz, with singular endpoints allowed. The present construction verifies them only for ten off-diagonal pairs of one five-coordinate block.

A readily testable necessary consequence is rank B_N[0:k,k:N]≤2 for every natural-order cut k. These cut-rank inequalities alone are not asserted sufficient: all pairs must admit the same globally compatible u,v,t_N. Different cyclic orders or more branches give other possible global constructions; they are not excluded here.

More generally, a full-family theorem must provide, for each supported N, legal cycles, endpoint arrays and weights for every coordinate, prove the full matrix identity, and prove every nonresonance guard. It must also bound the algorithm that generates these arrays. An existence proof, dense target inversion, or unbounded nonlinear search is not a cheap generator.

### Fully charged Fourier cost

For odd N, put c=N G_N. The cubic chirp identity gives, for the actual full B_N,

F_N=(1+c)B_N+(1−2c)B_N A_N B_N+(1+c)B_N A_N B_N A_N B_N.

Three sequential B_N calls suffice. This identity follows from (A_N F_N)³=cI and is verified as a scalar polynomial identity by the checker.

Suppose a proposed full representation has r_N nontrivial cycle Green branches, explicitly stored order/weight/endpoint arrays, and generation cost S_N. A legal weighted Hamiltonian Green solve uses O(N) arithmetic operations by an order traversal, a prefix-product closure computation and a reverse recurrence; it never requires dividing by individual edge weights, so zero edges remain allowed. Endpoint diagonals, diagonal-only branches, branch summation and the chirp diagonals must all be counted. A representation with k_N total branches therefore gives

setup plus one Fourier application = O(S_N+k_N N+N)

in the declared field-arithmetic model, with at most 3r_N nontrivial Green solves. Thus k_N=o(log N) and S_N=o(N log N) are a sufficient charged asymptotic improvement over O(N log N); bounded k_N and S_N=O(N) would give O(N) arithmetic. The current restricted construction proves neither hypothesis for full B_N.

Root generation, primitive-root access, extension-field arithmetic and numerical precision are part of the model and cannot be silently free. A numerical runtime or bit-complexity theorem additionally needs coefficient-height/conditioning and precision bounds. The algebraic operation count does not establish stability.

### Supported lengths can be converted to all lengths, conditionally

A full construction only at M=5(2410k+1)² would already suffice for an all-input-length arithmetic reduction if it met the above uniform charged bounds. For desired length n, choose the smallest k≥0 with M≥2n−1. Then M=2n+O(√n)+O(1), in particular M=O(n).

Bluestein's exact identity, using any θ with θ²=ω_n,

ω_n^(ij)=θ^(i²) θ^(j²) θ^(−(i−j)²),

reduces F_n to a cyclic convolution of length M by zero-padding the input chirp and embedding kernel indices −(n−1),…,n−1 modulo M. M≥2n−1 prevents the relevant differences from aliasing. That convolution uses a length-M forward transform of the input, a length-M inverse transform of the product, and, in setup, one length-M transform of the chirp kernel. The inverse is a reversal and 1/M scaling of the positive-exponent forward transform. Chirp and padding work is O(M+n), and kernel generation must be charged.

Consequently a genuine uniformly generated O(M) full transform at these supported M would imply O(n) arithmetic for every n after all three transforms and setup are counted. This is an explicit conditional bridge, not evidence that its missing full-B premise is true. The current five-coordinate construction cannot implement even one of those full transforms.

## 6. Cost of the result actually obtained

C_q's factors are generated by a fixed number of rational operations in the degree-four field K and one monic quadratic extension. The target and factor coefficients are rational functions of q of bounded degree. For integer q given in binary, their rational-coordinate bit lengths are O(log q), and generation has polynomial bit complexity in log q using elementary rational arithmetic. An exact algebraic answer is the defining polynomial together with pairs of K coordinates; no numerical choice of square root is required, since both roots work. If the supplied root is the ambient ω rather than η, obtaining η=ω^(q⁴) costs O(log q) multiplications by repeated squaring and is charged separately.

A restricted application uses two five-entry cyclic solves and one five-entry diagonal correction, plus endpoint work. This is O(1) field operations at fixed dimension five. This statement is about the five retained coordinates and does not imply O(1), O(log N), or O(N) application of the N-dimensional B_N.

## 7. Independent runnable certificate and dependencies

`check_extension.py` is newly written standard-library Python. No uploaded or predecessor program is imported or executed. It verifies:

- the synthesis residual and reciprocal-pole identities as expanded multivariate integer polynomials;
- the universal mod-241 target congruence in the polynomial parameter k;
- all 27 guard residues, the irreducible quadratic reduction and its nonsquare discriminant;
- exact reconstruction at q=1,483,1447,1929,2411 in Q(η)[d];
- every target entry at both roots, 100 two-sided Green inverse entries per q, and 35 scan-application output entries per q;
- the scalar cubic Fourier recovery identity;
- 11 exact finite-field Bluestein convolution controls and 10 minimal supported-length padding controls, including a 30-digit target length.

The finite exact controls supplement the uniform local-ring proof; they are not extrapolated into it. Complete factors and guard data for q=1 and q=483 are saved, along with checks for the remaining parameters. The other q values can be requested with `--q`.

The accepted B5 synthesis, its independent audit, the infinite restriction theorem and its independent audit are snapshotted as inert reports in `source/`. The lower bound depends on their accepted closed-projective exclusion. The upper-bound formulas and all new computations are supplied here. Independent review of this extension remains separate from this author's certificate.
