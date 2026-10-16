# R14: mixed-prime Fourier endpoint minimax

**16 October 2026 — research derivation, not independently peer-reviewed.**

**Status:** a self-contained scope extension of the project's existing Fourier
rank argument. The construction uses classical annihilator/coset ideas; it is
not presented as an independently invented construction or a worldwide-first
theorem. This is NOT a sub-N-log-N Fourier algorithm or integer multiplier.

## 1. The statement

Let G be a finite abelian group of order N=4L. Its unnormalized character matrix
is F[alpha,x]=alpha(x), with rows in the dual group and columns in G. For a
square matrix A in a specified order define

    q(A) = max_{1 <= k < N} max(rank A[:k,k:], rank A[k:,:k]).

This is the maximum of its upper and lower quasiseparable orders, not a new
invariant and not an operation count. Row and column permutations may differ.
All ranks in the minimax theorem are over the complex numbers.

**Theorem.** If N is divisible by four, then

    min_{row permutation P, column permutation Q} q(P F Q^T)
      = 1                  when N=4,
      = N/4 + 1            when N>=8.

The conclusion includes mixed-prime examples such as C12, C2 x C2 x C3,
C20, and C4 x C3 x C3. The earlier reviewed Q05 theorem covers finite
abelian 2-groups; its report explicitly leaves mixed-prime groups outside scope.

The upper construction below works over a splitting field whose characteristic
does not divide N. The universal lower and singular-value claims below are
characteristic-zero statements. Do not transfer the analytic lower theorem
into arbitrary finite characteristic.

## 2. Source relationship

The project's `math/drafts/endpoint_rank/manuscript.md` proves the general
finite-abelian overlap-sensitive rank bound. Its later Q05 report proves the
2-group minimax and its later attribution correction explains that the upper
ordering follows from the classical Delvaux--Van Barel dual-flag method.

We retain those credits. The change here is to use only one order-two
annihilator quotient, rather than a completely binary flag. The remaining
quotient can have arbitrary order. For the lower bound the required cardinality
is relatively prime to N even when G is not a 2-group. Thus the existing
arguments extend to all N divisible by four. This is an elementary extension
of known ingredients; no claim of new machinery or global priority is made.

The full 2006/2007 primary text was not reobtained in this run: the supplied
TW477 URL redirected to an inaccessible institutional login. Its institutional
2007 publication record was checked. Therefore global novelty is UNVERIFIED,
not inferred from absent search hits. See SOURCES.json and RESEARCH_LOG.md.

## 3. An orthogonal order-two pair always exists

Choose a nonzero element x of order two in G, and a nontrivial order-two
character chi in the dual, such that chi(x)=1.

Here is an explicit existence proof from a supplied direct product
G=C_(n1) x ... x C_(nk). Identify a character label a with

    alpha_a(h)=exp(2*pi*i*sum_j a_j*h_j/n_j).

If some n_i is divisible by four, choose x_i=chi_i=n_i/2 and all other
coordinates zero. Their pairing is exp(2*pi*i*n_i/4)=1.
Otherwise N divisible by four implies two distinct even factors n_i,n_j.
Choose x_i=n_i/2 and chi_j=n_j/2, all other coordinates zero. Their disjoint
supports give chi(x)=1. In both cases x and chi have order exactly two.

Put H=ker(chi) and R={alpha: alpha(x)=1}. Both have size N/2. They contain
<x> and <chi>, respectively. The quotient pairing

    (R/<chi>) x (H/<x>) -> C*,  ([alpha],[h]) |-> alpha(h)

is well defined and perfect. Indeed the characters trivial on H are exactly
{1,chi}; the elements annihilated by every character in R are exactly {0,x}.
Both quotients have order L.

Choose t in G with chi(t)=-1 and tau in the dual with tau(x)=-1. Such choices
exist since the two nontrivial order-two homomorphisms are onto {1,-1}.

## 4. Explicit independent endpoint orderings

Choose arbitrary representatives h_0,...,h_(L-1) for H/<x> and arbitrary
representatives alpha_0,...,alpha_(L-1) for R/<chi>. Their orders and choices
within their pairs are independent.

The first N/2 column labels are

    h_0,h_0+x, h_1,h_1+x, ..., h_(L-1),h_(L-1)+x.

The first N/2 row labels are

    alpha_0,alpha_0*chi, alpha_1,alpha_1*chi, ... .

For the second column half, take the first half in reverse order and replace
h by t-h. For the second row half, take the first half in reverse order and
replace alpha by tau*alpha^(-1).

Each first half is a bijection onto its subgroup. Each second half is a
bijection onto its other coset. Thus these are full endpoint permutations.
No vector-space basis, binary expansion of L, self-dual pairing or recursive
ordering of the quotient is assumed.

Let A be the character matrix in these orders, and let B be the L by L
quotient character matrix B[i,j]=alpha_i(h_j).

## 5. Exact cut identity on the first half

Write

    r_A(k)=rank A[:k,k:],  s_A(k)=rank A[k:,:k],

including zero values at the endpoints. For 0<=k<=N/2, set p=floor(k/2)
and e=k-2p. Then

    r_A(k) = ceil(k/2) + r_B(p),
    s_A(k) = ceil(k/2) + s_B(p).                    (1)

**Proof of the upper identity.** The selected k rows contain p complete
character pairs and possibly one extra row. Every column in t+H is still in
the suffix. On those columns a row pair has entries (u,-u), since chi(t+H)=-1.
Take one row from each pair and the optional extra row. Their restrictions to
t+H differ by nonzero constants from p+e distinct quotient characters on
H/<x>; character independence therefore gives rank p+e.

Let S:C^k -> C^p add each complete row pair and discard the extra row, if
present. The t+H-column span lies in ker(S). Both spaces have dimension p+e,
so they are equal. The full selected-column span contains ker(S). Its dimension
is consequently (p+e) plus the dimension of its image under S.

For h in H, the j-th pair sum is 2*alpha_j(h). Two column labels h and h+x
have identical images because alpha_j(x)=1. The surviving H-column pairs give
exactly the quotient suffix p,...,L-1. At an ODD cut k=2p+1, the first member
of column pair p has been removed but the second remains; column p is not lost.
Thus the image has rank r_B(p). The factor two is nonzero. This proves (1).

Transposing interchanges the roles of the group and dual and gives the lower
identity. The argument does not assume A or B symmetric.

## 6. Reflection and the upper bound

If rho_i is row i and g_j is column j, the construction gives

    rho_(N-1-i)=tau*rho_i^(-1),
    g_(N-1-j)=t-g_j.

Consequently

    A[N-1-i,N-1-j]
       = tau(t) * rho_i(t)^(-1) * tau(g_j)^(-1) * A[i,j].

The scalar and diagonal row/column factors are nonzero. Simultaneous reversal
therefore preserves rank and exchanges an upper cut k with a lower cut N-k:

    r_A(k)=s_A(N-k).                                (2)

For k<=2L the quotient has L-p remaining columns in an upper corner, and L-p
remaining rows in a lower corner. From (1),

    r_A(2p), s_A(2p) <= p+(L-p)=L,
    r_A(2p+1), s_A(2p+1) <= p+1+(L-p)=L+1.

Reflection covers all remaining cuts. If L>=2, take k=2L-1. The quotient
corner at p=L-1 is a nonzero single column (or row), so its rank is one.
Hence both orientations at that cut have rank L+1, and q(A)=L+1.
For L=1 the profile is (0,1,1,1,0), and q(A)=1.

## 7. Universal lower bound, without a 2-group hypothesis

Let U=F/sqrt(N). For arbitrary selected row set Y and column set Z write
r=|Y|, h=|Z|, I=dual(G)\Y, n=N-r, and

    d_Z=h-max_{s != 0}|Z intersection (Z-s)|.

If gcd(h,N)=1, then d_Z>=1. Otherwise a nonzero translation preserving Z
would split Z into orbits all of length ord(s)>1. That length divides both
h and N, contradicting coprimality.

At the critical cut, h=2L+1 and r=2L-1. For EVERY integer L,

    gcd(2L+1,4L)=1,                                (3)

because a common divisor also divides 4L-2(2L+1)=-2 and 2L+1 is odd.
Thus the project lower-bound hypothesis survives odd prime factors in N.

For completeness, here is the inherited Gram-moment argument rather than an
appeal to uninspected external text. Set C=U[I,Z]^* U[I,Z]. Then 0<=C<=Id and
U[Y,Z]^* U[Y,Z]=Id-C. If f_I(s)=sum_(alpha in I) alpha(s), orthogonality gives

    sum_s |f_I(s)|^2=Nn,   f_I(0)=n,
    tr(C^2)=N^(-2) sum_s |Z intersection (Z-s)| |f_I(s)|^2
      <= h*n/N - d_Z*r*n/N^2.

The nullity of U[Y,Z] is the multiplicity of the eigenvalue one of C, at most
tr(C^2). Consequently

    rank U[Y,Z] >= r*h/N + d_Z*r*(N-r)/N^2.

Use d_Z>=1, r=2L-1, h=2L+1, N=4L to obtain

    rank U[Y,Z] >= L+1/4-1/(4L)-1/(16L^2) > L       (L>=2).

Integer rank is therefore at least L+1. Every independent endpoint ordering
has this critical rectangle, proving the universal lower. At N=4, any nonempty
one-row corner is nonzero, so q>=1. The construction proves equality.

## 8. Retained approximation obstruction

The same moment argument also gives the inherited quantitative gap, now at
all group orders divisible by four. For L>=2, set

    B_L=L+3/4+1/(4L)+1/(16L^2),
    delta_N=sqrt(1-sqrt(B_L/(L+1)))>0.

For every critical rectangle of the normalized U,

    singular_value_(L+1)(U[Y,Z]) >= delta_N.

Indeed if the eigenvalues of C decrease as c_1>=...>=c_h, then
(L+1)c_(L+1)^2<=tr(C^2)<=B_L, while the relevant singular value squared is
1-c_(L+1). A rank-at-most-L approximant to that rectangle has operator-norm
error at least delta_N, by restricting to its kernel on the top L+1 right
singular-vector subspace. In particular any whole-matrix approximant whose
critical cut rank is at most L has that operator error lower bound.
This is an inherited bound with extended scope, not a new optimal gap claim.

## 9. Construction cost and limits

The constructor receives the explicit cyclic moduli. It finds the pair from
Section 3 and enumerates the quotient representatives directly in mixed-radix
order. It does not build a character matrix, pairing table or addition table.
With k factors it uses O(kN) operations on O(log N)-bit words and O(kN) words
of storage in the provided tuple implementation. The optional serialization to
flattened labels also uses O(kN) word arithmetic operations. Its deterministic
bit cost must charge the size of these words; the explicit permutations alone
contain Theta(N log N) output bits. This is not an O(N)-bit algorithm.

The rank verifier separately constructs dense matrices and performs elimination.
Its cost is NOT part of the lightweight permutation constructor and is NOT a
Fourier benchmark. The direct-product decomposition is supplied, not computed
for a black-box group.

Most importantly, q=N/4+1 is LINEAR in N. It is not a logarithmic or constant
rank compression. No full transform is implemented here. These identities do
not provide the missing sub-N-log-N arithmetic recurrence. They also do not
prove a universal Omega(N log N) lower bound for FFTs: high cut rank can coexist
with sparse multistage fast algorithms.

## 10. Precisely what this round establishes

The self-contained proof extends the project minimax equality to every finite
abelian group of order divisible by four and gives a direct label constructor.
The subgroups, quotient rank mechanism and Gram bound are attributed baseline
ideas. The mixed-prime conclusion is new relative to the READ project scopes,
not verified new across the worldwide literature or every uninspected archive.

The cases of odd N, N congruent to 2 modulo 4, nonabelian transforms, an optimal
approximation gap, and an actual faster unrestricted DFT are outside this proof.
