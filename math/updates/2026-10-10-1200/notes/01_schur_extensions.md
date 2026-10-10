# Complete Schur extensions and quadratic planar size

Version 2026-10-10, batch 1200. Mathematical status: independently accepted at the source proof hash recorded in SOURCE_MANIFEST.json, with q>=2 in the positive expander witness.

For a totally nonsingular N by N target F=P A^{-1}E, the complete support graph of K=[[A,E],[P,0]] has treewidth at least ceil(N/4)-1. For a fixed excluded minor with h vertices, its total size Q=M+N is at least ceil(N/4)^2/h^3. Every square matrix nevertheless has an explicit planar complete extension with M=3N^2+2N internal coordinates and maximum degree four. Its solve and storage costs are quadratic. The unrestricted claim that fixed-minor-free extensions are impossible is false.

The proof below is a mathematical extraction with the accepted endpoint convention applied. Acceptance concerns the stated algebraic and graph-theoretic results. Historical priority, practical runtime and finite-precision stability remain open.

## The complete extension and its inverse

Let F be invertible of order N; let A be invertible of order M, E have size M by N, and P have size N by M. Assume F=P A^{-1} E. Let K=[[A,E],[P,0]] and let T be its N final coordinates. Block elimination gives det K = det A det(-F), so K is invertible, and

K^{-1}[T,T] = -F^{-1}.

For any square matrix B, G(B) has one vertex per coordinate and an undirected edge {i,j} when i != j and either B[i,j] or B[j,i] is nonzero. Symmetry is not assumed. Injection and extraction supports must be included.

For example A=I, E=F, P=I is always a realization. Its ambient graph has treewidth zero, while its complete extension contains the dense routing. Therefore a statement excluding bounded-treewidth or bounded-bandwidth A alone is false without restrictions ensuring the complete extension is also low-treewidth.

## Inverse separator rank with singular principal blocks allowed

Suppose B is invertible and its coordinates partition as U,S,V, with B[U,V]=B[V,U]=0. Then

rank B^{-1}[U,V] <= |S|, and rank B^{-1}[V,U] <= |S|.

Proof: if an r by r minor B^{-1}[I,J], I subset U, J subset V, is nonzero with r>|S|, Jacobi's complementary-minor identity makes det B[J^c,I^c] nonzero. This complementary square matrix retains every row of U. Those |U| rows have support only in columns (U minus I) union S, of cardinality |U|-r+|S|<|U|. They are dependent, a contradiction. Interchange U,V for the reverse block. No principal subblock of B is required to be invertible.

If F is totally nonsingular, then F^{-1} is totally nonsingular by the same complementary-minor identity. Complex prime-order Fourier matrices have this property by Chebotarev's theorem. Consequently every vertex separation of G(K) obeys

min(|T intersection U|, |T intersection V|) <= |S|.                       (1)

Otherwise an (|S|+1)-square terminal inverse minor contradicts the separator bound.

## Terminal balance and the source constant

A width-w tree decomposition has a bag S of size at most w+1 such that each component of G(K)-S contains at most N/2 terminals. To see this with terminal weights rather than ambient vertex counts, assign each terminal to an arbitrary bag containing it, choose a weighted centroid of the decomposition tree, and take its bag. A vertex absent from this bag occurs only on one side of the centroid; a graph component outside the bag cannot occupy two such sides. Its terminals are therefore bounded by the corresponding tree-side weight.

Writing s=|S| and t=|S intersection T|<=s, the source's N/8 contradiction is valid: if s<N/8, at least N-s>7N/8 terminals remain. A greedy component union first reaching N/4 has fewer than 3N/4 terminals, so both it and its complement contain more than s terminals. This violates (1). Thus w>=ceil(N/8)-1.

## Sharper terminal partition

The following purely integer/real weight argument gives the independently accepted strengthening w>=ceil(N/4)-1.

Suppose s<N/4 and the remaining component terminal counts c_i satisfy 0<=c_i<=N/2 and sum c_i=N-t, where 0<=t<=s.

- If some c_i>s, put that component on one side. Its complementary side has at least N-t-N/2 >= N/2-s>s terminals.
- Otherwise all c_i<=s. Greedily collect components until their total a first exceeds s. This is possible because N-t>s. Before the last component the total was at most s; hence s<a<=2s. The other side has N-t-a>=N-3s>s terminals.

When s=0 the second case cannot occur, since the positive remaining total forces a positive component. Zero-terminal components can be assigned arbitrarily. In every case (1) is violated. Therefore every terminal-half-balanced separator has s>=ceil(N/4), and the treewidth lower bound follows.

The proof only uses total nonsingularity of F, not specific Fourier coefficient values. It remains an exact algebraic representation obstruction, not an operation lower bound for unrestricted linear circuits.

## Correct minor-free size consequence

Write Q=M+N for the number of vertices of the complete extension. For a fixed h-vertex excluded minor H, the weighted Alon–Seymour–Thomas separator theorem supplies a terminal-half-balanced separator of size at most h^(3/2) sqrt(Q). Specifically, Proposition 1.3 applies after noting that an H-minor-free graph is K_h-minor-free. Compare this with the proved source separator lower bound to obtain

Q >= ceil(N/8)^2 / h^3.                                                  (2)

The independently accepted sharper argument replaces the numerator by ceil(N/4)^2. Either form implies Q=Omega_H(N^2). Merely knowing that Q is finite, polynomial, or unbounded does not contradict the separator theorem. The exclusion is valid when Q=o(N^2), including linear or N polylog(N) ambient size.

The direct weighted-separator comparison avoids any need to infer a terminal balance guarantee from an unweighted ambient separator.

## Explicit planar realization of every matrix

Fix any field k, any N>=1, and any target F=(f_ij) in k^(N by N). In this section indices i,j,k run from 1 to N; k is a column index, not the field. Let i(k)=N+1-k, so output-column order is reversed.

Use the following distinct internal coordinates:

- H[j,k] for 1<=j<=N and 0<=k<=N;
- V[j,k] for 0<=j<=N and 1<=k<=N;
- C[j,k] for 1<=j,k<=N.

There are M=N(N+1)+N(N+1)+N^2=3N^2+2N coordinates. Order first H[j,0] and V[0,k], then cells in row-major order (j increasing, then k increasing), placing C[j,k], H[j,k], V[j,k] in that order within each cell.

Define A and E by the following equations A z=E x:

H[j,0] = x_j,                 V[0,k] = 0,
C[j,k] - H[j,k-1] - V[j-1,k] = 0,
H[j,k] - C[j,k] + V[j-1,k] = 0,
V[j,k] - C[j,k] - (f_(i(k),j)-1) H[j,k-1] = 0.                          (3)

These equations specify every row of A and E, including the zero boundary equations. Every diagonal entry of A is one and every other coefficient references an earlier coordinate. Thus A is unit lower triangular, det A=1 over every field, and no further nonzero-pivot assumption is hidden. E has exactly N entries equal to one, in rows H[j,0], column j.

Define P by (Pz)_i=V[N,N+1-i]. It has exactly N entries equal to one. The bottom-right block of K=[[A,E],[P,0]] is identically zero.

The cell equations give the exact identities

H[j,k]=H[j,k-1],
V[j,k]=V[j-1,k]+f_(i(k),j) H[j,k-1].

Induction gives H[j,k]=x_j and V[j,k]=sum_(r=1)^j f_(i(k),r) x_r. Hence P A^{-1} E=F for every x. If F is invertible, K is invertible by the already-proved block identity. In particular take F to be the complex prime-order Fourier matrix.

A has M diagonal entries and at most 6N^2 off-diagonal entries; E and P contribute N each. Thus nnz K<=9N^2+4N. A forward solve is O(M)=O(N^2) arithmetic for an arbitrary right-hand side. Building/storing the coefficients is also O(N^2) given the target table. The result is a counterexample to a structural planar exclusion, not a low-cost Fourier algorithm.

### A plane drawing including the shared terminals

Draw the internal coordinate vertices at integer coordinates:

H[j,k]=(2k+1,2j),  V[j,k]=(2k,2j+1),  C[j,k]=(2k,2j).

Each cell lies in the square [2k-1,2k+1] by [2j-1,2j+1]. Its six possible support edges join its center C to the west H[j,k-1], north V[j-1,k], east H[j,k], and south V[j,k] ports, plus the north-to-east and west-to-south port pairs. Draw all six as straight segments. The two additional segments occupy the northeast and southwest corners and do not meet the center spokes except at their own endpoint vertices. Different cell interiors are disjoint, with the intended shared ports on their boundaries. Zero coefficients merely remove edges.

The input port H[j,0]=(1,2j) lies on the left boundary; its paired output port is V[N,N+1-j]=(2d_j,2N+1), where d_j=N+1-j. Introduce terminal T_j at (-d_j,2N+1+d_j).

Draw the E support edge H[j,0]--T_j as the polyline

(1,2j) -> (-d_j,2j) -> (-d_j,2N+1+d_j),

and the P support edge T_j--V[N,N+1-j] as the polyline

(-d_j,2N+1+d_j) -> (2d_j,2N+1+d_j) -> (2d_j,2N+1).

Bends are points on graph edges, not extra matrix coordinates. These arcs lie outside the grid except at their endpoints. For j<ell one has d_j>d_ell: the j arc extends farther left, lower, and right. The ell arc begins lower on the left boundary and ends farther left on the bottom boundary, so it lies inside the j arc and never crosses it. This is exactly why the output-column order was reversed. The two terminal incidences refer to the same terminal vertex; no duplicated input/output terminals or uncounted terminal identifications are used.

This supplies a plane drawing of the complete graph, including every A, E and P support edge. Its maximum degree is at most four: cell centers have degree four; interior horizontal/vertical ports have at most two incident edges from each of their two adjacent cells; boundary ports and terminals have lower degree.

The construction therefore lies in a fixed-minor-free family (planar graphs), has O(N^2) total coordinates, and realizes every Fourier matrix exactly. Together with (2), the quadratic size scale is asymptotically sharp for planar exact totally nonsingular targets, up to constants. No novelty claim is made for this linear crossover construction.

## High treewidth and linear solves

The construction principle is straightforward. Let G_q be any explicit bounded-degree vertex-expander family on q vertices, adjoin a Hamiltonian path, order its vertices along that path, and let L have L[i,j]=1 for each graph edge with i>j. For q>=2, set Delta equal to maximum undirected degree and lambda=1/(4 Delta). Then A=I-lambda L is unit lower triangular with O(q) nonzero entries.

- Forward substitution and multiplication each cost O(q) exact field arithmetic.
- ||L||_1 and ||L||_infinity are at most Delta, so ||lambda L||_2<=1/4. Singular values of A lie between 3/4 and 5/4, yielding kappa_2(A)<=5/3.
- The Hamiltonian path gives a directed path from every earlier coordinate to every later one. For positive real lambda, A^{-1}=sum_(r=0)^(q-1) (lambda L)^r has every strict lower-triangular entry positive.
- Bounded-degree vertex expansion implies every balanced separator has Omega(q) vertices, so tw G(A)=Omega(q).
- A^{-1} is still triangular with q(q-1)/2 zero entries. Nonzero diagonal gauges and independent row/column permutations preserve the number of zeros, so this inverse alone cannot be a dense q by q Fourier matrix.

The last point does not exclude arbitrary E,P around a triangular inverse: the planar construction above realizes arbitrary F with such an A at larger M. The source's suggestion that a single triangular solve is excluded must remain limited to the direct monomial-equivalence comparison it actually proves.

### The source graph generator needs an expansion bridge

The original v28 graph generator uses the horizontal moves x+y, x-y, x+y+1, x-y+1, with y fixed, and the analogous vertical moves. Undirected closure and loop deletion are then applied. This is not literally the canonical eight-regular MGG multigraph with moves x±2y and x±(2y+1), and analogous vertical moves. In fact the source's saved maximum degree after the path reaches 14.

Let G be the simple graph produced by these moves before adding the path, and let H be the canonical MGG multigraph's simple support. Every positive canonical horizontal move is a path of at most two edges in G:

(x,y) -> (x+y,y) -> (x+2y,y),
(x,y) -> (x+y,y) -> (x+2y+1,y).

Use reversed paths for negative moves and exchange coordinates for vertical moves. Repeated intermediate vertices only shorten the path. Thus H is a subgraph of G squared. The source symmetric support has maximum degree at most 12 (and at most 14 after the path).

If |partial_H S|>=alpha |S| for all 0<|S|<=q/2, let B=partial_G S. Any H-neighbor outside S is in B or has a G-neighbor in B, hence

alpha |S| <= |partial_H S| <= (1+Delta_G)|B| <= 13 |B|.

So G has expansion at least alpha/13 uniformly. Canonical MGG's uniform expansion therefore suffices to justify linear treewidth of the actual source family, with a constant loss. Small positive expansion measurements by themselves would not prove the all-size claim; this comparison does.


## Evidence and references

The accompanying original exact certificate program and finite matrix/rotation data check the construction. Finite controls do not replace the general proofs above or extend complex Chebotarev full spark to arbitrary finite fields.

Classical ingredients: [Frenkel on Chebotarev](https://arxiv.org/abs/math/0312398), [Alon, Seymour and Thomas, Proposition 1.3](https://web.math.princeton.edu/~nalon/PDFS/spr.pdf), and the [formalized Margulis Gabber Galil graph](https://isa-afp.org/browser_info/current/AFP/Expander_Graphs/Expander_Graphs_MGG.html). No publisher PDF is included.
