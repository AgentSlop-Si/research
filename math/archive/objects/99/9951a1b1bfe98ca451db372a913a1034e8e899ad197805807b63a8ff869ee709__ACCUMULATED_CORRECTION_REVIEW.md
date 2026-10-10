# Exact accumulated natural-term correction rank and linear application

Independent paired review, 9 October 2026 UTC.

## Definition and exact compression

Let N=km with k>=2 dyadic, p,d!=0, and p^N!=1. Let

T_N=D_d(I-pZ_N)^(-1)D_d^(-1), D_d=diag(d^j).

Define Q_(N,k) by subtracting from T_N its k contiguous principal-block
diagonal. Thus Q keeps precisely the off-block entries of this natural
Green term. It is not the off-block part of the whole two-term stage.

Put r=p^m, s=pd, u_i=s^i, v_j=s^(-j), 0<=i,j<m, and

C_k=(I-rZ_k)^(-1)-I/(1-r^k).

Then

Q_(N,k)=[D_(d^m) C_k D_(d^m)^(-1)] tensor (u v^T).

Indeed, for distinct block indices alpha,beta, set h=(alpha-beta mod k),
so 1<=h<k. The fine cyclic distance is hm+i-j, which lies strictly
between 0 and N. The corresponding entry equals

d^(m(alpha-beta)) r^h (pd)^(i-j)/(1-r^k),

exactly the displayed Kronecker factorization. Both sides are zero on
diagonal blocks. This proves the compression for every allowed size.

## Exact rank, including the exceptional locus

Over C, Z_k has the k distinct eigenvalues zeta with zeta^k=1. Hence
C_k has eigenvalues

r(zeta-r^(k-1))/[(1-r zeta)(1-r^k)].

The denominator is nonzero because r^k=p^N!=1. Since r!=0, an
eigenvalue vanishes precisely when zeta=r^(k-1). There is at most one
such zeta, and it exists exactly when

(p^N)^(k-1)=1.

The gauge factor is invertible and u v^T has rank one. Therefore

rank Q_(N,k) = k-1 if (p^N)^(k-1)=1,
rank Q_(N,k) = k otherwise.

For k=2 the exceptional condition is already forbidden by p^N!=1,
so the rank is always 2. For example, k=4 and r=(1+sqrt(-3))/2
give the allowed exceptional rank 3. At p=0 the natural term is I,
so Q is identically zero and the inverse powers above are not used.
The case d=0 is outside the defined gauge family. This statement is
over characteristic zero; no assertion uses inseparable roots in a
field whose characteristic divides k.

## What this rank does and does not obstruct

The rank grows at least k-1. Thus this particular flattened global
correction cannot be represented as U V^T with a number of columns
bounded independently of k. This excludes a bounded-rank global
correction of that precise kind.

It does not exclude a constant-state streaming recurrence or a
hierarchical representation. In fact the exact compression itself
gives a linear-time application, even at full correction rank k.
For each input block x_beta, form h_beta=v^T x_beta. Apply

g=[D_(d^m) C_k D_(d^m)^(-1)]h,

then output block u g_alpha. The coarse operator is a weighted cyclic
Green operator minus the scalar identity 1/(1-r^k), so it needs one
weighted-cycle pass and a subtraction. With coefficient vectors and
boundary scalars supplied, a direct counted schedule costs

2N+3k-1 multiplications and N+2k-2 additions.

This is O(N+k)=O(N). Vector/power/reciprocal preparation, index/data
work, and coefficient bit costs are additional. Rank growth therefore
does not constitute a runtime lower bound for this structured operator.

## Whole masked product: an upper bound only

If each of three two-term stages is changed only by replacing its
natural Green term by its k-block principal diagonal, its non-affine
Green term remains intact. Each stage difference has rank at most k.
Telescoping the product with its intervening diagonal masks gives

rank(original product - modified product) <= min(N,3k).

More precisely the bound is the minimum of N and the sum of the three
individual correction ranks. Multiplication cannot increase rank and
rank is subadditive. No lower bound follows: the three corrections can
interact or cancel. Replacing entire stages by block diagonals would
be a different operation because their non-affine crossblocks were
not removed here. Nothing in this lemma proves or disproves a Fourier
factorization or a full masked-product recursion.

## Independent checks

check_accumulated_correction.py verifies 14 exact rational instances
at N=4,8,16,32 and every dyadic k>=2 up to N. It checks every entry of
the Kronecker compression, both exact ranks, and the operation-counted
linear application against the dense correction. It also checks the
exceptional complex k=4 rank drop using exact algebraic arithmetic.
These controls accompany the symbolic proof above. No constructor
program or uploaded code is executed.
