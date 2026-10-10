# An arbitrary-row-sparse repair for the separated-scan witness

Audit-derived supplement, 2026-10-09 UTC. No external priority claim is made. This proof is independent of the uploaded/source implementation.

## Result

For N >= 1 let S have entries 1 strictly below its diagonal, 3 on its diagonal, and 2 strictly above. For every integer q >= 0 and every complex N-by-N matrix B having at most q nonzeros per row,

    rank(S^(-1) - B) >= ceil(floor(N/(q+2)) / (2q+1)).                 (1)

The following easy corner improvements apply:

- If q = 0, the exact rank is N.
- If q < N, the rank is at least 1, including when the bound in (1) is zero.
- If q >= N, a uniform positive lower bound is impossible: B = S^(-1) is permitted.

In particular, at every fixed q, the minimum required rank defect grows linearly with N. This repairs the source's claimed escape from **arbitrary bounded-row-sparsity plus bounded rank**, whereas its original off-band proof established only escape from bounded bandwidth plus bounded rank. The repair is weaker in its dependence on growing q: approximately N/((q+2)(2q+1)), rather than the source's bandwidth-specific approximately N/(2b+2). No optimality is claimed.

The result also holds, with the same right side, for rank(L S^(-1) R - B), where L and R are arbitrary invertible monomial matrices.

## 1. Inverse and interleaved minors

Write D = 2^(N+1)-1, which is nonzero over C. Directly, or by the source's valid Sherman–Morrison computation,

    S^(-1)[i,j] = -2^(i-j-1)/D        if i > j,
                  (2^N-1)/D         if i = j,
                  -2^(N+i-j)/D      if i < j.

Suppose distinct indices interleave as

    r_1 < c_1 < r_2 < c_2 < ... < r_m < c_m.

Multiply selected row i by 2^(-r_i) and selected column j by 2^(c_j). The resulting m-by-m matrix has the constant value

    alpha = -1/(2D)       below the diagonal,
    beta  = -2^N/D       on and above the diagonal.

Its determinant is beta (beta-alpha)^(m-1). To see this without assuming a determinant identity, replace row i by row i minus row i-1, proceeding from i=m down to i=2. The new row i has just one nonzero, alpha-beta, in column i-1. Expanding along those rows gives the stated determinant. Here beta-alpha = -1/2 and beta != 0. Consequently the original minor has determinant

    2^(sum r_i - sum c_i) beta (beta-alpha)^(m-1) != 0.              (2)

This argument uses strictly interleaved rows and columns, so no diagonal-entry exception is hidden.

## 2. A zero minor against every row-q-sparse B

Set M = floor(N/(q+2)). If M=0, (1) is the trivial rank >= 0 statement. Otherwise use M disjoint consecutive blocks, each containing q+2 coordinates. For block i, numbered from zero, put

    r_i = (q+2)i.

Among the q+1 later coordinates r_i+1,...,r_i+q+1, at least one column c_i satisfies B[r_i,c_i]=0. Choose one. The selected pairs already have the strict interleaving needed in section 1.

Construct a simple undirected graph with these M blocks as vertices. Join i and j if either B[r_i,c_j] or B[r_j,c_i] is nonzero. There are no self-loops because B[r_i,c_i]=0.

For any induced subgraph with v vertices, the directed incidences B[r_i,c_j] != 0 number at most qv: each selected row has at most q nonzero entries, and the selected columns are distinct. Every undirected edge requires at least one such incidence. Thus this induced subgraph has at most qv edges and average degree at most 2q. It has a vertex of degree at most 2q.

Repeatedly select such a vertex and delete it and its neighbors. This constructive greedy procedure returns an independent set I of size

    |I| >= ceil(M/(2q+1)),

because each selection deletes at most 2q+1 vertices. On the selected rows {r_i:i in I} and columns {c_i:i in I}, every entry of B vanishes, including the paired entries. Equation (2) shows that the corresponding minor of S^(-1)-B is nonsingular. This proves (1).

## 3. Corners, reorderings, and quantifiers

When q=0, B=0 and det(S)=D != 0 gives rank N. When q<N, every row of B has an unoccupied column; all entries of S^(-1) are nonzero over C, so S^(-1)-B is not the zero matrix. The rank is therefore at least 1.

For monomial L,R,

    rank(L S^(-1) R - B) = rank(S^(-1) - L^(-1) B R^(-1)).

Left or right multiplication by a monomial matrix only reorders or rescales rows or columns. It preserves the maximum nonzero count per row. Applying (1) to the transformed B proves the endpoint-invariant claim. This also covers monomial-equivalent versions of S because inversion reverses the two endpoint transformations.

The proof quantifies over every B, including singular B, arbitrary support patterns, zero entries, coincident nonzero values, and parameter choices causing cancellation. There is no genericity, conditioning, nonzero-leading-principal-minor, or generator-chart assumption.

The witness S is itself a member of the separated-generator scan class. Thus that class is not contained in the family of stages whose inverse is bounded-row-sparse plus bounded rank. This is an existential separation of classes; it does not say every separated scan escapes, and does not provide a Fourier factorization.

## 4. Arithmetic scope

Both S and S^(-1) have O(N) unit-cost exact scalar-arithmetic applications, including linear scalar coefficient preparation. The construction above certifies rank separation; it does not accelerate Fourier transforms.

The O(N) arithmetic statement is not an O(N) bit-complexity statement. D has N+1 bits. In particular, S^(-1)e_0 contains N explicitly represented rational values with a total of Theta(N^2) numerator/denominator bits in the usual separate-fraction representation. Powers of two may be generated by a running doubling recurrence, but this does not erase output bit lengths. No numerical stability guarantee is claimed.

## 5. Independent finite checks

See INDEPENDENT_CHECKS.json and independent_checks.py. The latter was authored for this audit and imports only the Python standard library. It checks exact interleaved determinant formulas for 305 arbitrary sparse-support cases through N=128, direct ranks and monomial transformations in 165 small cases, and all 23,042 support patterns in the three cases (N,q)=(4,1),(4,2),(5,1). The all-N proof above, not these finite checks, establishes the theorem.
