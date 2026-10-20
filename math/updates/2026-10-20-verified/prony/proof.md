# Original even-Prony coordinates: conditioning and a conservative paid contract

20 October 2026. NEW CANDIDATE derived after recovery. No earlier conditioning draft or final acceptance was recovered. This document is not a reconstruction of an unavailable accepted proof. Its copied dependencies retain their historical scope; this new document needs separate review.

## 1. Exact object and scope

Let N=2h>=4, q=exp(pi i/h), c_j=q^{j(j-1)/2}, and

R_h(z)=prod_{k=0}^{h-1}(z-q^k)=sum r_j z^j,
P_h(z)=sum_{j=0}^h (c_h/c_j)r_j z^j.

The recovered original model is T=D^{-1}Z with T^N=-I and normalized Fourier target Fhat=Q C(T)/sqrt(N), C(T)=sum_{j=0}^{N-1}c_j T^j. This is the original polynomial P_h, not the large-parameter pencil B_N=zP_h+2^(10N^3+2)P_(h-1).

The recovered accepted identity is P_h(z)=-H_h(qz;q), H_h(x;q)=sum [h choose j]_q x^j. P_h is monic with constant -1. For all h>=2, its roots avoid alpha^N=-1. The recovered accepted squarefreeness range includes all N>=4 with 16 not dividing N. No all-even squarefreeness statement is used. The h=8m, m odd obstruction packet is not a proof of a counterexample or of the missing squarefreeness statement.

Two distinct conclusions follow below:

A. For every h>=2, in this canonical complex embedding, the raw monomial Vandermonde on the root multiset is singular or has

kappa_2(V) >= [2/(h sin(pi/(2h)))]^((h-1)/2)/sqrt(h)
             > (4/pi)^((h-1)/2)/sqrt(h),
V[k,l]=alpha_l^k, 0<=k<h.

B. Within the accepted squarefree range 16 not dividing N, the SAME original h-root family has explicit conservative separation, precision, exhaustive certified preparation, storage, and full independent-bank application bounds. This is not useful numerical stability, polynomial preparation, a production executor, or a speedup. Outside this range the B contract is conditional on a separately certified nonzero discriminant; A needs no such condition.

The numerical condition statement is not extended to arbitrary primitive embeddings by Galois invariance: complex absolute values and singular values are not Galois invariants. The all-embedding bounds used in B are separately established coefficient bounds.

## 2. Correct Newton sum and unscaled spectral condition lower bound

Write P_h(z)=z^h+a_(h-1)z^(h-1)+a_(h-2)z^(h-2)+... . For h>=2, q^h=-1, q^2 !=1, and

sum_{k=0}^{h-1}q^k=2/(1-q),
sum_{k=0}^{h-1}q^(2k)=0.

The elementary symmetric coefficients of R_h are therefore

r_(h-1)=-2/(1-q),
r_(h-2)=((sum q^k)^2-sum q^(2k))/2=2/(1-q)^2.

Since c_h/c_(h-1)=q^(h-1)=-q^-1 and c_h/c_(h-2)=q^(2h-3)=q^-3,

a_(h-1)=2q^-1/(1-q),
a_(h-2)=2q^-3/(1-q)^2.

These formulas include h=2, where a_(h-2) is the constant coefficient. Newton's identity, counting roots with multiplicity, gives

sum_l alpha_l^2=a_(h-1)^2-2a_(h-2)
                 =-4q^-3/(1-q).

The minus sign is essential. Thus

|sum_l alpha_l^2|=4/|1-q|=2/sin(pi/(2h)).

Writing M=max_l |alpha_l|, the triangle inequality gives

M^2 >= 2/[h sin(pi/(2h))] > 4/pi,

because sin(x)<x for 0<x<=pi/4. Hence ||V||_2>=M^(h-1), using an entry in its last row. Also sigma_min(V)=sigma_min(V*)<=||V*e_0||_2=sqrt(h), using the first row of V. Division proves A whenever V is nonsingular; repeated roots give identical columns and kappa_2(V)=infinity, by convention.

The h=1 case is excluded: P_1=z-1 and the second Newton-coefficient calculation does not apply. The asymptotic lower bound is exponential in h despite its 1/sqrt(h) factor; the finite lower bound need not exceed 1 at the smallest h.

This proof says that these unscaled coordinates are exponentially ill-conditioned. It does NOT prove that actual floating-point errors attain a worst-case sensitivity, that the particular chirp right-hand side is a worst case, or that every algorithm needs exponentially many bits or operations. Even a necessary bit count would involve a logarithm of a condition number, not the condition number itself. Scaled nodes, diagonal equilibration, alternative polynomial bases, structured solves, direct residue formulas, preconditioners, shared resolvent computation, and other realizations are not excluded. The unitary Fourier target is not ill-conditioned merely because this internal representation is.

## 3. Explicit upper envelopes on the original roots

For this section assume P_h squarefree in characteristic zero, guaranteed by the recovered dependencies when 16 does not divide N. Put m=h and

R=2^(N+1),
delta=(2R)^[-N m(m-1)],
eta=(2 R^N)^[-Nm],
rho=eta (2R)^[-(N-1)],
K_V=m(2R/delta)^(m-1),
W_b=m K_V,
G_b=2 W_b R^N,
H_V=m^2(2R)^(m-1).

All these are positive rational quantities with explicitly computable integer exponents; m need not be a power of two.

For EVERY cyclotomic embedding sigma, the expansion of R_h into unit-root factors and the unit-modulus coefficient phases give ||sigma(P_h)||_1<=2^h. Cauchy's elementary bound therefore places all conjugate roots in |z|<=R. The constant coefficient has modulus one, so each root also has |alpha|>=R^[-(m-1)].

The nonzero discriminant is an algebraic integer in K=Q(q), of degree d=phi(N)<=N. At each embedding its modulus is at most M_D=(2R)^[m(m-1)]. Its field norm is a nonzero integer. Therefore its modulus in our embedding is at least M_D^[-(d-1)]. Isolating a particular squared root difference in its product formula gives

|alpha_i-alpha_j| >= (2R)^[-d m(m-1)/2+1] >= delta.

The all-even forbidden-node theorem gives nonzero J=Res(P_h,z^N+1). Every conjugate has |J|<=(2R^N)^m. The same norm argument, then removing the other m-1 factors, yields

|1+alpha_i^N| >= (2R^N)^[-(dm-1)] >= eta.

Factoring z^N+1 into N unit-modulus roots E, with every other distance <=2R, gives dist(alpha_i,E)>=rho. This proves uniform margins, rather than inferring them from finite numerical samples.

Lagrange interpolation, with numerator coefficient l1 norm at most (1+R)^(m-1) and denominator at least delta^(m-1), gives

||V^-1||_2 <= sqrt(m)(1+R)^(m-1)delta^[-(m-1)] <= K_V,
||V||_2 <= m R^(m-1),
kappa_2(V) <= m R^(m-1) K_V.

Solving V beta=(c_0,...,c_(m-1)) yields ||beta||_2<=W_b. The accepted recurrence propagates all N moments. Hankel rank m proves every exact beta_l is nonzero. Let gamma_l=beta_l(1+alpha_l^N); then every gamma_l is nonzero, |gamma_l|<=G_b, and

C(T)=sum_{l=1}^m gamma_l(I-alpha_l T)^-1.

For either T or the signed cyclic shift S, unitary spectral diagonalization gives

||(I-alpha_l S)^-1||_2 <= rho^-1.

Here E is closed under inversion, so min_{tau in E}|1-alpha tau|=dist(alpha,E). It follows directly that

log R=O(N), log(delta^-1)=O(N^4), log(eta^-1)=O(N^4),
log(rho^-1)=O(N^4), log K_V, log W_b, log G_b=O(N^5).

These are very weak upper envelopes. They do not mean the actual condition number is exp(Theta(N^5)). The lower and upper estimates leave a large gap.

## 4. Constructive root acquisition, not a free root oracle

For any requested root-center error e_*>0 with e_*<=1, let M_2 be the least power of two >=m, A_0=(4R)^m, and d_0=delta^(m-1). Choose r to be the largest integral power of two not exceeding

min(e_*,delta/8,d_0/(16 M_2 A_0)),

and s=d_0 r/(64 M_2 A_0). Enumerate centers w in s(Z+iZ) with both coordinates in [-R-1,R+1]. At each center compute enclosing approximations to the Taylor coefficients a_k=P_h^(k)(w)/k!, and certify the strict Rouché inequality

|a_0|+sum_{k=2}^m |a_k|r^k < |a_1|r.                  (RD)

Retain certified disks of radius r that do not intersect earlier retained disks, until m disks have been retained. All comparisons are rational outward-enclosure comparisons; inconclusive centers are rejected, never accepted.

Termination proof: at each true root alpha, a nearest grid point is within s. The chosen square contains it. At such a center, |P'_h(alpha)|>=d_0. For both roots and enumerated centers the sum of absolute Taylor coefficients is <=A_0, because |w|<=2R and the product of linear factors has coefficient sum at most (1+|w|+R)^m. If e=|w-alpha|<=s, then

|a_0|<=A_0 e<=d_0 r/(64M_2),
|a_1|>=d_0-mA_0e>=d_0/2,
sum_{k>=2}|a_k|r^k<=A_0r^2<=d_0r/(16M_2).

These inequalities hold also at m=2. RD has slack greater than d_0r/4. Construct the coefficient vector with l1 error at most theta=d_0r/(1024M_2 A_0), and enclose each modulus with additional width at most zeta=d_0r/(1024M_2). Taylor-shift coefficient error sums to at most theta A_0. The total disturbance of the two RD sides is bounded by 2theta A_0+(m+1)zeta<d_0r/16. Hence the nearest point is certified at one prescribed finite precision.

Each accepted disk has one root. Two disks containing distinct roots cannot intersect, because their center distance is >=delta-2r>2r. Greedy rejection can therefore only discard another disk for an already represented root, not all disks for a missing root. The degree count proves complete coverage at termination.

Coefficient acquisition is paid. Viewed as polynomials in q, the coefficients of P_h have degree <=h(h-1)<=N^2 and total integer coefficient l1 norm <=2^h. For |qhat-q|=u<=N^-2, the telescoping power bound gives total polynomial error <=3N^2 2^h u. Construct qhat to error <=theta/(8N^2R), evaluate the coefficient polynomials exactly, and round the final coefficient vector within another theta/2 l1 error. Machin's arctangent formula followed by sine/cosine Taylor series with explicit rational remainder estimates is a terminating elementary q-acquisition procedure. No floating-point transcendental oracle is assumed.

The grid has at most (8R/s)^2 centers. Coefficients can be formed by expanding the defining product, then applying the specified phases; powers, products and all cyclotomic evaluations are charged. At each center a Taylor shift costs O(m^2) rational arithmetic operations plus modulus enclosure. With B=2+N+ceil(log2(1/e_*))+ceil(log2 R)+ceil(log2(1/s)), a deliberately loose elementary envelope is

O((1+(8R/s)^2) B^20) bit operations,
O(B^10) bits of working storage,

using streamed grid addresses and only retained certificates. To justify the polynomial overhead, O(B) rational series terms have O(B^3)-bit numerators/denominators; round qhat before its degree-O(N^2) polynomial use. Taylor values and exact rational modulus-bisection comparisons fit O(B^5)-bit operands. The O(B^5) conservative bound on total arithmetic/bisection steps per center, with schoolbook O(B^10) arithmetic, is below B^20. Source construction costs fit the same envelope. These huge exponents are a safe upper bound, not a performance prediction.

Labels are the retained disjoint disks. If later refinement is needed, match an old and new center only within delta/2 after both radii are <=delta/16: the same-root centers are <=delta/8 apart, while different-root centers are >=7delta/8 apart. Never independently sort successive batches by real part.

## 5. Weight and bank precision, with output rounding

Fix target eps=2^-p, p>=1. Take

v_g=eps rho/(16m),
v_b=v_g/[8(2R)^N],
u_c=v_b/(8m K_V),
e_* <= min(1, rho/2, eps rho^2/(16m G_b),
           1/(4K_V H_V), v_b/(8K_V H_V W_b),
           v_g/[4 W_b N(2R)^(N-1)]).

Choose the largest integral power of two not exceeding this minimum and acquire root centers to that error as in Section 4. Acquire each complex moment to absolute error <=u_c/2, then ROUND each real and imaginary coordinate within u_c/4 to O(K)-bit dyadics before the weight solve, K=p+O(N^5). The final complex moment error is at most u_c/2+sqrt(2)u_c/4<u_c, including rounding. The constants in this O bound are obtained directly by taking ceilings of the displayed rational logarithms; it is not an implicit oracle tolerance.

For |alpha_tilde-alpha|<=e_*, telescoping powers give ||V_tilde-V||_2<=H_V e_*. The inverse perturbation identity then gives ||V_tilde^-1||_2<=2K_V. An exact pivoted rational solve obeys

||beta_tilde-beta||_2 <= 2K_V[m u_c+H_V e_* W_b] <= v_b/2.

Round the solved vector with total Euclidean error <=v_b/2. The root-to-weight perturbation estimate is thus paid, including the particular moment construction and output rounding. No assumed floating-point stability is used.

Form gamma_tilde=beta_tilde(1+alpha_tilde^N). Its pre-rounding coordinate error is bounded by

2(2R)^N v_b + W_b N(2R)^(N-1)e_* <=v_g/2.

Round each residue with additional absolute error <=v_g/2. Zero exact coefficients need not be detected: the original exact weights are nonzero, while rounded weights may harmlessly be zero when below tolerance.

The perturbed resolvents are legal and satisfy

||(I-alpha_tilde S)^-1||_2<=2/rho,
||(I-alpha_tilde S)^-1-(I-alpha S)^-1||_2<=2e_*/rho^2.

Writing C_tilde for the exact rational approximate bank, termwise perturbation yields

||C_tilde(S)-C(S)||_2
 <=m[2v_g/rho+2G_b e_*/rho^2]<=eps/4.

All root, moment, weight, and residue coordinate precisions are p+O(N^5) bits. Setup includes acquiring them; a lower bound on kappa was NOT substituted for a sufficient accuracy guarantee. Sufficiency follows from the explicit upper envelopes and inequalities above.

## 6. Complete paid application, storage, and bit model

Let S e_j=e_(j+1) for j<N-1 and S e_(N-1)=-e_0. With E_L[j]=q^[-j(j-1)/2], E_R[j]=q^[-j(j+1)/2], the recovered exact identity is

Fhat=(1/sqrt(N)) E_L C(S) E_R.

All endpoint phases and the normalizer are prepared and applied, not supplied free. An approximate branch y=(I-aS)^-1 x is computed exactly in rational arithmetic by

b_*=sum_{k=1}^{N-1} a^(N-1-k)x_k,
y_0=(x_0-a b_*)/(1+a^N),
y_i=a y_(i-1)+x_i, 1<=i<N.

Horner evaluation and the power a^N use O(N) scalar work. Running all m branches independently, weighting, accumulating, reading x, and writing all N outputs costs O(Nm)=O(N^2) rational operations. This is a complete upper bound for this specified implementation, not an unrestricted lower bound. It does not charge one branch as if it were the whole transform.

For b-bit dyadic input coordinates, handle x=0 separately. Approximate endpoint entries and 1/sqrt(N) to absolute error a_0=eps/(128N). Their phase construction, square-root bisection, O(N) storage and O(N) applications are charged. Since ||C(S)||=sqrt(N) and ||C_tilde-C||<=eps/4, expanding the three endpoint/normalizer perturbations with each approximate factor norm <=2 bounds their contribution by 16N a_0<=eps/8. Combining with the exact-endpoint-scaled bank error leaves less than eps/2 before final rounding. Round real and imaginary output coordinates to absolute error <=eps 2^-b/(16N); as ||x||>=2^-b for nonzero input, this adds <eps||x||/8. Total output error is <eps||x||.

Put K=p+b+O(N^5), chosen from the explicit preceding tolerances. Prepared scalar coordinates use O(K) bits. Building V from dyadic centers gives O(NK)-bit entries after a common dyadic denominator is cleared. Because moments were rounded first, their operands meet the same bound. Determinant/minor bounds give O(N^2K+N log N)-bit intermediates for pivoted fraction-free elimination over Gaussian integers, with O(N^3) arithmetic steps. A conservative schoolbook cost is O(N^7 K^2) for the weight solve; O(N^2) matrix entries, all preprocessing, and its polynomial working storage are charged separately from online cost.

A branch denominator 1+a^N has O(NK) bits. Accumulating at most m branch denominators increases the running output numerator/denominator size to O(N^2K). Exact rational recurrence and accumulated-vector arithmetic with O(N^2) operations therefore have the conservative online bit bound

O(N^6 K^2)=O(N^6(p+b+N^5)^2).

Stored constants need O(NK) bits. With branches streamed, O(N+m) rational scalar registers suffice online, but their growing bit sizes mean this is NOT O(N) fixed-word memory: a safe online bound is O(N^3K) bits. A single cached full Vandermonde need not be retained online. Root disks/certificates and the weight-solve matrix use polynomial setup storage, covered by Section 4's O(B^10) bound.

The elementary root route has log(1/e_*)=p+O(N^5), log(1/s)=p+O(N^5), so total cold setup, INCLUDING root acquisition, moments, coefficient generation, weights, residues, certificates, and endpoint constants, is

2^[O(p+N^5)] bit operations with polynomial working storage.

No full grid has been executed. This is a mathematical effective upper bound and a certified interface, not a benchmark or a finished production preparer. This exponential route is not asserted optimal. The separate accepted polynomial preparation for the different large-t family is recorded in COST_LEDGER.md, not transplanted without proof to this polynomial.

## 7. Attribution and stopping boundary

The root-product/norm, Lagrange, perturbation, and elementary Rouché-grid methods here explicitly adapt the recovered Oct11 NF03 proof, with new original-polynomial scope, new constants R=2^(N+1), m=h, and a checked m=2 endpoint. The corrected Newton-sum candidate was supplied in the recovery assignment and independently rederived here. The contemporary reviewer independently confirmed the core algebra; no acceptance is presumed. A separate reviewer suggested a reciprocal-root sharpening; it is deliberately NOT incorporated in the asserted theorem.

The selected result is a bounded canonical-coordinate obstruction and an expensive but fully charged original-family implementation contract on the already accepted squarefree range. It does not close useful conditioning under other coordinates, original all-even h-pole optimality, the unresolved h=8m squarefreeness step, universal t=1, practical preparation/execution, general growing-degree stability, historical priority, or fast Fourier computation. No owner count, table, repository, or external state was changed.
