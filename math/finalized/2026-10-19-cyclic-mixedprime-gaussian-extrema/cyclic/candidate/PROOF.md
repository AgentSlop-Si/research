# A sharp cyclic family at the last nonzero correction rank

19 October 2026 UTC. This is a self-contained extension of the accepted C8 argument. No novelty claim or FFT operation-count conclusion is made.

## 1. Model and results

Let F_N[j,k]=N^(-1/2) exp(-2 pi i j k/N), with indices modulo N. Let delta_(N,r) be the minimum of

||F_N - L(B+E)R||_2

over arbitrary real N-by-N B, complex E of rank at most r, and arbitrary invertible complex monomial L,R. The norm is the external operator norm. For 2r >= N, set sigma_(2r+1)=0 by convention.

**Theorem A (uniform lower bound).** For even N >= 4 and integers 0 <= r with 4r < N-2,

delta_(N,r) >= sin(pi (N-4r-2)/(4N)).

**Theorem B (attaining infinite family).** For every integer m >= 1,

delta_(4m,m-1) = sin(pi/(8m)),

and delta_(4m,r)=0 for r >= m. In particular, the least correction rank allowing zero error is exactly m. Theorem B includes every dyadic N >= 4, with r=N/4-1, and recovers the accepted N=8,r=1 value.

Theorem A is not claimed sharp for all smaller ranks r<m-1. No attainment statement is inferred just from its lower bound.

**Theorem C (width-sharp open-arc threshold).** For N=4m and arbitrary diagonal unitary A,B, every open arc of width 2 pi/N contains at most N/2+1 eigenvalues, counted with multiplicity, of F_N A F_N B. A closed arc of this width can contain N/2+2 eigenvalues. The witness for Theorem B attains this closed-arc count. Hence the stated width cannot be enlarged while retaining the N/2+1 upper count. This does not assert that the N/2+1 open-arc count is itself attained.

## 2. Exact fixed-phase and monomial reductions

Every complex monomial L factors as D_L T_L, with D_L diagonal unitary and T_L invertible real monomial. Similarly R=T_R D_R. Absorbing T_L,T_R into the unrestricted real core and the correction preserves the represented matrix and correction rank. There is no nonunitary multiplication of the residual. Multiplying only the external residual by diagonal unitaries then shows

delta_(N,r) = min_(P,Q diagonal unitary) sigma_(2r+1)(Im(P F_N Q)).       (2.1)

For completeness, the fixed-phase statement follows without invoking a black-box approximation theorem. Put Y=Im V. Since Im Z=(Z-conjugate Z)/(2i), ||Im Z|| <= ||Z||. A complex-rank-r matrix has imaginary part of real rank at most 2r. If T has real rank at most 2r, its kernel intersects the span of the first 2r+1 right singular vectors of Y; a unit vector in the intersection gives ||Y-T|| >= sigma_(2r+1)(Y). Conversely, the real singular-value expansion truncated at 2r attains this error. Write this truncation as sum_(a=1)^(2r) v_a u_a^T, padding with zero terms if needed. Then

E = sum_(ell=1)^r (v_(2ell-1)+i v_(2ell))(u_(2ell)+i u_(2ell-1))^T

has complex rank at most r and imaginary part equal to the truncation. Taking B=Re(V-E) realizes equality. This also handles r=0 by empty sums. Compactness of the phase torus and continuity show that the phase minimum exists.

For unitary V=P F_N Q, let W=V^T V. This is symmetric unitary and

Q^(-1) W Q = F_N P^2 F_N Q^2,
Y^T Y = (I-Re W)/2.

The real and imaginary parts of W are commuting real symmetric matrices, so they admit a simultaneous real orthogonal eigenbasis. If the eigenvalues of W are exp(i phi_j), its corresponding imaginary singular values are |sin(phi_j/2)|. This establishes the spectral-arc reduction with multiplicity.

## 3. The commutator lemma, with the required rank count

Suppose a unitary U of order N has N-k eigenvalues in an open arc |arg lambda|<theta, where 0<theta<pi/2. Replace precisely those eigenvalues by 1 in an orthonormal eigenbasis, obtaining U_0. Then rank(U_0-I)<=k. Write U=U_0 E; all eigenvalues of E have argument of absolute value less than theta. With a=cos theta,

||E-a I|| < sin theta,

because |exp(i t)-cos theta|^2=1+cos^2 theta-2 cos theta cos t < sin^2 theta.

For any unitary T, set K=UTU* T* and K_0=U_0 T U_0* T*. Then

rank(K_0-I)<=2k,
||K-K_0||=||ET-TE||<=2||E-aI||<2 sin theta.

The fixed space ker(K_0-I) therefore has dimension at least N-2k. The singular-value min-max principle, or the same subspace-intersection argument used in Section 2, gives at least N-2k singular values of K-I strictly below 2 sin theta. As K is unitary, these are |lambda-1|; equivalently, at least N-2k eigenvalues of K have |arg lambda|<2theta.

In the rank-r application k=2r, so the forced count is precisely N-4r, not N-2r. Multiplying U by a scalar phase changes neither commutator, so the original arc may have any center.

## 4. Cyclic commutator and all-r lower bound

Let S e_j=e_(j+1), C=F_N A F_N and M=C B. The cyclic-Hankel entry formula gives C S=S* C. With T=B* S B,

K=M T M* T*=S* B* S* B,
K e_j=(b_j/b_(j-1)) e_(j-2).                         (4.1)

There are g=gcd(N,2) cycles, each of length L=N/g. For even N, g=2, L=N/2, and their products are Gamma and Gamma^(-1), where Gamma is the product of the even b_j divided by the product of the odd b_j. Thus

chi_K(x)=(x^L-Gamma)(x^L-Gamma^(-1)).                 (4.2)

For odd N there is one cycle and its product telescopes to 1, so chi_K(x)=x^N-1. No cycle count is obtained from samples.

An open arc of width 2 pi a/L, for an integer 1<=a<L, contains at most a roots from each degree-L factor. It therefore contains at most 2a eigenvalues of K for even N. Multiplicities add when the two factors share roots. The open endpoints are essential.

For even N choose a=N/2-2r-1>0 and theta=pi a/N. If sigma_(2r+1)(Im(PF_NQ))<sin(theta/2), at least N-2r eigenvalues of M=F_N P^2 F_N Q^2 lie in |arg lambda|<theta. Section 3 forces N-4r eigenvalues of K into an open arc of width 4theta=2 pi a/L. Section 4 permits at most 2a=N-4r-2. This contradiction proves Theorem A.

For Theorem C, N/2+2 eigenvalues of M in an open arc of width 2 pi/N would use k=N/2-2, theta=pi/N in Section 3, forcing at least four eigenvalues of K into an open arc of width 4 pi/N. Its two length-N/2 cycles permit at most two. Thus the count is at most N/2+1.

As an optional companion, the same one-cycle argument gives, for odd N and N-4r-1>0,

delta_(N,r) >= sin(pi (N-4r-1)/(4N)).

No odd-order attainment is asserted here.

## 5. An explicit witness for every N=4m

Set

N=4m, h=N/2=2m, zeta=exp(2 pi i/N), alpha=pi/N,
t=(-1)^m zeta^(-1), z=exp(i pi/(2N)).

Choose the diagonal Q explicitly by

q_j=1                                      if j is even,
q_j=exp(i pi m/2) exp(-i pi/N) exp(2 pi i j/N) if j is odd.

Let P=zQ, V=P F_N Q and B_0=Q^2. Then

b_j=1 if j is even, and b_j=t zeta^(2j) if j is odd.

Every entry is unimodular. Write R_0 e_j=e_(-j), D e_j=zeta^(2j)e_j, H=S^h and Pi_+=(I+H)/2, Pi_-=(I-H)/2. The discrete geometric-sum identity gives

C=F_N B_0 F_N=(Pi_+ + t S^2 Pi_-) R_0.            (5.1)

Indeed B_0 is the sum of the even-coordinate indicator and tD times the odd-coordinate indicator, so its Fourier support consists of 0,h,2,h+2, including coincident locations when N=4. Formula (5.1) remains valid in that case.

The operators C and B_0 preserve the four mutually orthogonal spaces

H_(epsilon,eta)={x: x is supported on parity epsilon, Hx=eta x},

epsilon in {even,odd}, eta in {+1,-1}. Each space has dimension m, since H pairs two coordinates of the same parity without fixed coordinates. On these four spaces, C B_0 acts respectively as

- even,+ : R_0;
- odd,+  : t R_0 D;
- even,- : t S^2 R_0;
- odd,-  : t^2 S^2 R_0 D.

The first three displayed weighted reflections square to I after removing their scalar t factors. Also

(S^2 R_0 D)^2=zeta^4 I,
t^2=zeta^(-2).

Consequently, define four unitary involutions on these spaces:

J_1=R_0,
J_2=(-1)^m R_0 D,
J_3=(-1)^m S^2 R_0,
J_4=zeta^(-2) S^2 R_0 D.

All J_a are Hermitian because they are unitary involutions. Since W=V^T V is similar to M=z^2 C B_0, the four blocks of M are

exp(i alpha) J_1,
exp(-i alpha) J_2,
exp(-i alpha) J_3,
exp(i alpha) J_4.                                 (5.2)

The exact multiplicities come from traces; one must not assume all signs are positive.

## 6. Trace count and singular spectrum

Let e=1 if m is even and e=0 otherwise; let o=1-e. The four traces are

tr J_1=1+e,  tr J_2=o,  tr J_3=o,  tr J_4=1+e.     (6.1)

Here is a direct fixed-coordinate calculation. On a parity subspace, restriction to H=eta has trace equal to half the trace of J plus eta HJ on that parity.

For J_1, fixed coordinates of R_0 satisfy 2j=0 and are j=0,h, both even. Fixed coordinates of H R_0 satisfy 2j=h and are j=m,3m, both even exactly when m is even. This gives 1+e.

For R_0 D on the odd coordinates, 2j=0 gives none. For H R_0 D, the two candidates m,3m are odd exactly when m is odd, and both weights zeta^(2j) are -1. The + half-space and factor (-1)^m yield tr J_2=o.

For S^2 R_0 on the even coordinates, its fixed coordinates 1,h+1 are odd, so contribute none. For H S^2 R_0, the candidates m+1,3m+1 are even exactly when m is odd. The - half-space and factor (-1)^m yield tr J_3=o.

For zeta^(-2) S^2 R_0 D on the odd coordinates, the fixed coordinates 1,h+1 each have weight 1. The additional fixed coordinates m+1,3m+1 are odd exactly when m is even and each has weight -1. The - half-space therefore gives tr J_4=1+e.

Thus sum_a tr J_a=4. An m-dimensional involution with trace tau has (m+tau)/2 positive eigenvalues and (m-tau)/2 negative ones. Formula (5.2) gives the complete spectrum of W:

- exp(i alpha): multiplicity m+1+e;
- exp(-i alpha): multiplicity m+o;
- -exp(i alpha): multiplicity m-1-e;
- -exp(-i alpha): multiplicity m-o.

Zero multiplicities are allowed. In total, N/2+2 eigenvalues lie at exp(+-i alpha), and N/2-2 lie at their negatives. Put s=sin(pi/(2N)), c=cos(pi/(2N)). Section 2 gives exactly

singular values of Im V: s repeated N/2+2 times; c repeated N/2-2 times.  (6.2)

Since 2(m-1)=N/2-2, the rank-(m-1) complex correction removes all c directions. This proves the upper bound in Theorem B. Theorem A with r=m-1 supplies the identical lower bound. The closed-arc assertion of Theorem C follows from the N/2+2 eigenvalues on its endpoints.

## 7. A constructive legal correction and real core

The displayed P,Q already give a fully explicit phase witness. A correction can also be generated deterministically without an optimization. Let Y=Im V and

R=(Y^T Y-s^2 I)/(c^2-s^2).

By (6.2), R is a real orthogonal projector of rank N/2-2=2r, and Y(I-R) has norm s. Obtain a real orthonormal basis u_1,...,u_(2r) of its range by Gram-Schmidt on R e_0,...,R e_(N-1), discarding zero residuals and choosing positive normalization constants. Define v_a=Y u_a and use

E=sum_(ell=1)^r (v_(2ell-1)+i v_(2ell))(u_(2ell)+i u_(2ell-1))^T,
B=Re V-Re E.

Then rank_C E<=r, Im E=YR, B is real, and

V-(B+E)=iY(I-R),  ||V-(B+E)||_2=s.

For the original objective use L=P* and the right outer gauge Q*. Their external residual is P* [V-(B+E)] Q*, of exactly the same norm. Empty sums for N=4,r=0 give E=0.

## 8. Zero-error rank and endpoint controls

For the unphased F_N, W=F_N^T F_N=R_0. This reversal has a negative eigenspace of dimension (N-2)/2=2m-1. Therefore Im F_N has real rank 2m-1 and can be packed into a complex correction of rank ceil((2m-1)/2)=m, with zero error. The positive bound at r=m-1 rules out all lower correction ranks. This proves the zero-error statement.

For the witness, the even product of b_j is 1, while the odd product is

t^h zeta^(2 sum_(j odd) j)=(-1) zeta^(2h^2)=-1.

Thus Gamma=-1 and

chi_K(x)=(x^(N/2)+1)^2.

The two eigenvalues nearest 1 are exp(+-2 pi i/N), each of multiplicity two. The open commutator arc |arg lambda|<2 pi/N contains none; its closed version contains four. The original closed arc |arg lambda|<=pi/N contains N/2+2 eigenvalues. Replacing open arcs by closed arcs in either obstruction would therefore be false.

## 9. What remains open

For N=4m and r<m-1, this packet supplies the uniform lower bound from Theorem A but does not establish a matching upper construction. The precise unproved attainment question is whether there exist diagonal unitary P,Q such that

sigma_(2r+1)(Im(PF_NQ))=sin(pi(N-4r-2)/(4N)).

Equivalently, an attaining M=F_NP^2F_NQ^2 must have at least N-2r eigenvalues in the closed centered arc of angular radius pi(N-4r-2)/(2N), after scalar rotation. This is an attainment problem, not an asserted theorem. Other cyclic orders and general finite groups retain their separate scope; no jointly real Green construction is supplied.

The analytic proof covers all integers m and all phases in the lower bound. Fresh finite exact checks verify the implementation and multiplicity formulas at listed sizes; finite checks are not promoted to proof of a continuum or an infinite family.
