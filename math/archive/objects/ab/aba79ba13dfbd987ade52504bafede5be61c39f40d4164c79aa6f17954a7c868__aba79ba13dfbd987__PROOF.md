# All-size proof for deterministic energy pruning

## Model and statement

Let N=2^L, U_N[k,j]=exp(-2 pi i k j/N)/sqrt(N), and x in C^N. Work is counted
in an adaptive exact real-arithmetic RAM: real arithmetic and comparisons are
unit-cost, complex values are pairs of real registers, and indices fit in
O(log N)-bit words. A compatible primitive Nth root and the fixed algebraic
normalization 1/sqrt(2) are available. All root powers actually used are prepared
in O(N) work. This is not a fixed input-linear circuit or a bit-complexity model.
Norm tests are nonlinear, input-dependent computations and are charged.

For 0<epsilon<1 there is a deterministic algorithm returning every coordinate
of the exact hard threshold of U_N x at theta=epsilon||x||_2, in

    O(N [1+min(L, log_2(epsilon^-2))]) work and O(N) space.

It follows that the maximum coordinate error is at most theta. Zero input is
handled by writing N zeros. If epsilon>=1, all-zero output satisfies the same
hard-threshold specification. Epsilon=0 requires the ordinary exact transform
(zero branches may optionally be pruned), with O(N log N) work.

## Disjoint output subtrees

Use decimation in frequency, not decimation in time. At a node of length m,
split its vector v into

    a[j]=(v[j]+v[j+m/2])/sqrt(2),
    b[j]=(v[j]-v[j+m/2]) omega_m^j/sqrt(2),  0<=j<m/2.

The even-indexed entries of U_m v are U_(m/2) a; the odd-indexed entries are
U_(m/2) b. The twiddle omega_m^j has modulus one. Therefore

    ||a||_2^2+||b||_2^2=||v||_2^2.

A depth-d node owns one residue class of frequencies modulo 2^d and has length
N/2^d. Distinct nodes at that depth own disjoint output coordinates. Imagining
the full unpruned tree, the sum of node energies at every depth equals
E=||x||_2^2. The remaining transform within each node is unitary, so its norm
is exactly the square root of the energy of all final coefficients it owns.

## Algorithm and correctness

Initialize a dense length-N output array to zero. Compute E once. Visit the
root in depth-first order. For each visited node:

1. Compute its squared norm. If this is <=epsilon^2 E, prune the node.
2. Otherwise, if its length is one, write its coefficient at the owned index.
3. Otherwise, form its two DIF children and visit them.

Pruning requires no loop over the discarded output positions, because the
output is already zero. Index offsets and strides determine every leaf index.

Every coefficient below a pruned node has magnitude <=epsilon sqrt(E), by
unitarity and the elementary coordinate/norm inequality. Conversely, any
coefficient strictly greater than this threshold forces every ancestor's
norm above threshold, so its path is visited and its exact value is written.
Finally, the leaf test discards every coefficient at or below threshold.
This proves the exact hard-threshold statement, including threshold ties.
No coordinate accumulates several pruning errors: each belongs to one leaf
and at most one first-pruned subtree. Thus no depth-dependent error factor
or probabilistic union bound is needed.

## Complete work bound

Let A_d be the number of depth-d nodes whose norms are strictly above threshold.
Energy conservation gives

    A_d <= min(2^d, epsilon^-2).

Every split at that depth processes N/2^d values. The sum V of split-node
lengths consequently satisfies

    V <= N sum_(d=0)^(L-1) min(1, epsilon^-2 / 2^d).

For h=ceil(log_2(epsilon^-2)), the first min(L,h) terms cost at most one each.
If h<L, the remaining geometric sum is at most two. Also V<=NL. Hence

    V <= N min(L,h+2),

and N+V has the asserted asymptotic bound.

Computing the root norm visits N entries. The two child norms of a split node
together visit exactly the parent's length. Computing each node norm only once
therefore has total value volume N+V, including pruned children and leaves.
Every norm requires a constant number of real arithmetic operations per entry.
Butterfly arithmetic, child-array writes and twiddle reads cost O(V). The tree
has at most one plus twice its split-node count visited nodes; their comparisons,
stack management and index updates cost O(N+V). The initial input scan, all
root-power preparation, N zero writes, retained-leaf writes and final output
cost O(N+V). Allocation/copying also stays within this bound.

Depth-first traversal keeps pending sibling vectors of lengths at most
N/2,N/4,...,1, together with a constant number of current-node arrays. Their
total length is O(N). Add the input, full output and root table: O(N) space.
An implementation that retains every level need not satisfy this space bound;
the supplied implementation uses depth-first traversal.

Square roots are unnecessary in branch tests. An equivalent unnormalized DIF
implementation compares (m/N)||v||_2^2 with epsilon^2 E at a node of length m.
Its final raw Fourier values have threshold sqrt(N)epsilon||x||_2; normalize
them only for the U_N convention. This weighted version underlies the exact
Gaussian-rational audit for N<=4.

## Scope boundaries

For raw F_N the error bound is epsilon sqrt(N)||x||_2. For F_N/N it is
epsilon||x||_2/sqrt(N). Normalizations cannot be exchanged without these factors.
The bound is global-norm additive error, not per-bin relative error, relative
output l2 error, or exactness on arbitrary inputs. Comparisons make the algorithm
adaptive and outside nonbranching linear-circuit models.

To match v2's epsilon||x||_1/sqrt(N) bound, use epsilon_E=epsilon tau with
tau=||x||_1/(sqrt(N)||x||_2). The work then depends on tau and can be N log N.
In particular an impulse requires every leaf for epsilon<1 in that contract.
The v2 time-domain sparse-surrogate rank barrier does not apply to an arbitrary
adaptive algorithm producing a sparse spectrum.

Exact real-arithmetic correctness is not a certified complex128 error theorem.
Roundoff can affect norm comparisons near the threshold, root magnitudes and
the retained coefficient values. A certified numerical version needs explicit
interval/error tracking and a separate complexity analysis. The tests in this
package supply evidence about the prototype, not that missing certification.
