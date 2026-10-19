# Separate optional observation: all coordinates in the nonzero Q family

This reviewer observation is **outside acceptance of the frozen candidate**.
It is not needed for the accepted N^2-|S| theorem or adapter contract. It is an
elementary refinement for later independent checking, with no novelty claim.

## Exact N^2 distinct-query bound for the displayed family

Let N>=3, P be the row-action successor cycle, U=I-2P, V=I-3P over Q, and
S={(i,i),(i,i+1)} with indices modulo N. For an input coordinate (a,b),
U E_ab V has a nonzero entry outside S in every case:

1. If b is neither a nor a+1, choose output position (a,b). Its coefficient is 1.
2. If b=a, choose output position (a-1,a+1). Its coefficient is 6.
3. If b=a+1, choose output position (a,a+2). Its coefficient is -3.

Each chosen position lies outside S when N>=3. Thus for every feasible B0,
every nonzero single-coordinate perturbation leaves the necessary off-support
subspace. If B0 is invertible, choosing delta=1 unless the determinant lemma
forbids it, and otherwise delta=2, preserves invertibility over Q.

There is therefore an invertible infeasible alternative at each of all N^2
coordinates of the candidate's invertible B0=U^-1+V^-1. The same adaptive
transcript argument proves N^2 necessary distinct entry queries; the same
coupling proves expected distinct queries at least (1-2 epsilon)N^2 for
two-sided error epsilon<1/2. Reading all entries once is a matching distinct
query upper bound for the inherited complete decision test. The supplied
streaming adapter can instead make repeated calls, up to 4N^2; its call upper
bound is not being altered.

The exact finite controls test all 320 coordinates at
N=3,4,5,6,7,8,11. The three-case argument, not those finite tests, is the proposed
all-size justification.

## More general dimension observation

For arbitrary fixed invertible U,V, let

    L={U^-1 D_x + D_y V^-1 : x,y in F^N}.

This is a linear subspace of dimension at most 2N. Actual nonzero-scale
completions form a subset of L. At most dim L coordinate units can belong to L,
since coordinate units are linearly independent. For every feasible B0, at
least N^2-dim L coordinate units therefore yield infeasible targets
B0+delta E_ab for every nonzero delta. The same invertibility and coupling
arguments apply under the previously stated field-size conditions.

Moreover dim L<=|S|, because B -> UBV maps L injectively into matrices supported
on S. This gives the optional general count N^2-dim L, at least
N^2-min(2N,|S|), without asserting that coordinate sensitivity equals codimension.
For the nonzero Q family, dim L=2N: a kernel vector of
U D_y+D_x V=0 would obey x_i+y_i=0 and 3x_i+2y_(i+1)=0, hence
x_(i+1)=(3/2)x_i and ((3/2)^N-1)x_i=0. The kernel is zero over Q.

The stronger all-coordinate count above shows why this dimension bound need
not be sharp. None of these refinements concern compressed or symbolic input,
implicit Fourier targets, quantum or matrix-vector oracles, direction
discovery, singular masks, or an all-length transform construction.
