# Independent review of Phase34 moving partitions and Weyl orbit v20

## Results and corrections

The Phase34 sparse-reference product theorem and the moving-partition rank theorem are valid in their stated restricted architectures. The moving-partition theorem tracks different sets at different stages and does not require a common invariant subset. Its twisted-bit-reversal family has the claimed square-root depth obstruction. The exact finite certificates and the reported rank-feasible shuffle control reproduce independently.

The v20 Weyl character-packet identity is a valid O(N) fusion for a selected operator-index character. Its arbitrary-weight zero minor is valid and gives a stronger exclusion than the source states: at prime N>=5 it excludes every independently row/column-permuted Fourier matrix with invertible diagonal gauges, not only affine permutations. Two corrections are necessary:

1. Exact packet support counts, density of every Green matrix, and N-dimensional orbit span require alpha != 0 in addition to alpha^N != 1. At alpha=0 all resolvents are I, H_0=I, all other packets vanish, and the span has dimension one. The algebraic packet identity still holds.
2. A constant-degree sparse matrix whose inverse is a monomially gauged Fourier matrix is already impossible by the direct-inverse density argument accepted in the prior v19 review. The valid Krylov propagation theorem does not reopen that Fourier-denominator route. It remains useful for other dense-inverse sparse systems.

All uploaded programs remained inert. Four fresh standard-library checkers reproduce the mathematical claims and selected source records. No timing benchmarks were adopted or rerun. No new exact faster Fourier algorithm, full Fourier coefficient family, or unrestricted arithmetic lower bound follows.

## Source identity and predecessor comparison

The three directly uploaded archives and their exact predecessor bytes are recorded in SOURCE_PROVENANCE.json. Their SHA256 values are:

- Phase34: 6706fbe3dcb22cba7a73cb2d410ad1a6bfbc8e9865a4fe7f5544f24ba46bed01. Its nested Phase33 ZIP is byte-identical to the previously reviewed direct Phase33 upload, hash 0ff572f21b9677bf40641e82805ffd358e283374b65a33910264c6b220ed2ce4.
- Moving partitions: 7ba6c02ad9e5d47232119d618d8971199aa262c686494144d8c8be46a14b0026. Its nested central-bit checkpoint matches the prior direct upload, hash 0d0b58a05ebd8ab57d4b51deaa6dfefaa2f08a2c2511de2f0053f7bf4011e8cb.
- Weyl v20: 43c0e5499b77d2d96dfa72ae59ff00dbd45d9aa190ff104e830bd1d1aab93eea. Its nested v19 ZIP matches the prior direct packet/separator upload, hash a6dd4cd48efc8233e1cc5829eae269242b4661f92ec7f22a05222e47d935f782.

Principal sources are Phase34 THEOREM.md and CHECKPOINT.md, moving-partition PROOF_CERTIFICATE.md and RESEARCH.md, and v20 RESEARCH.md and CHAIN_CHECKPOINT_2026-10-10_v20.md. Their author-supplied statements, code, and records are preserved under sources/ as inert material. The uploaded authors receive attribution for their source derivations; this independent review makes no publication-priority claim and does not rely on novelty statements or bibliography metadata.

## 1 Phase34 sparse-reference products

### Consecutive-row sparse rigidity

Let F_N[i,j]=zeta^(ij), where zeta is primitive of order N, and let P have at most k nonzeros in each row. Put m=floor(N/(k+1)). In the first m rows, P occupies at most mk columns, leaving at least m all-zero columns. On any m of these, F_N-P is the Vandermonde matrix with distinct nodes zeta^j. Hence

    rank(F_N-P) >= floor(N/(k+1)).

The same holds for any nonzero scalar multiple of F_N or F_N^(-1). It holds at composite lengths too; it does not say every Fourier minor is nonzero. The relevant property is consecutive-row Vandermonde rank, not unrestricted full spark.

### Product theorem

For invertible stages

    S_j = sum_s c_js L_js B_js^(-1) R_js,

take invertible diagonal L_js,R_js, invertible B_js, a reference B_j0 with at most d_j nonzeros per row, and c_j=sum_s c_js != 0. For nonzero summands s!=0, let r_j bound the sum of

    rank(B_js-B_j0) + rank(L_js-L_j0) + rank(R_js-R_j0).

Resolvent subtraction and expansion of the two endpoint differences give

    S_j = c_j L_j0 B_j0^(-1) R_j0 + E_j,
    rank(E_j) <= r_j.

Inverse subtraction preserves this rank bound because both comparison matrices are invertible. The reference inverse c_j^(-1) R_j0^(-1) B_j0 L_j0^(-1) is row-d_j-sparse. Inverting the full product, including arbitrary invertible monomial gates at all interfaces and endpoints, and telescoping yields

    M^(-1)=P+E,
    row_support(P) <= product_j d_j,
    rank(E) <= sum_j r_j.

Therefore exact Fourier requires

    sum_j r_j >= floor(N/(1+product_j d_j)).

Monomial matrices only rescale or reorder rows/columns and preserve the relevant support counts. No condition-number hypothesis is used. If c_j=0 and r_j<N, the corresponding stage is singular; if its correction budget is already at least N, this argument gives no useful exclusion. An exact invertible square product itself forces all stages to be invertible.

For cyclic bidiagonal references, d_j<=2. Bounded r_j<=r give rt>=floor(N/(2^t+1)), hence t>=log_2 N-O(log log N). This is a restricted depth theorem. The usual separately executed constant-count linear scans then cannot improve complexity merely by reducing the depth below that threshold. The proof does not charge all possible shared evaluation strategies and is not a universal time lower bound.

### Exact two-order diagnostic

For alpha!=0, characteristic different from two, invertible G_a=(I-alpha W_a)^(-1), and invertible S=G_0+G_1,

    rank(S^(-1)-(I-alpha W_0)/2)
      = rank(G_1-G_0)
      = rank(W_1-W_0)
      = N-cycles(W_0^(-1)W_1).

Each equality follows from multiplication by invertible factors or from the kernel of I minus a permutation. The last kernel consists of one independent constant per permutation cycle in any characteristic. Cycle enumeration costs O(N) word work. This diagnostic selects rank-distant orders; it does not create phase-compatible Fourier coefficients.

The new theorem does not subsume the prior additive-separation theorem. It attacks products only when each sum is close to one shared sparse-reference inverse. Eight genuinely rank-distant MGG orders need not satisfy a small r_j. Closeness of each spliced order to its own unspliced cover does not make every summand close to one common reference. No exclusion of the reviewed expander family follows by that substitution.

### Reproduced controls

Independent matrices over F_998244353 reproduce all four saved N=8,16,32,64 two-stage examples, their selected Vandermonde columns and cycle deficits. The N64 residual ranks are 4 for two unpatched stages, 8 for the two endpoint-patched stages, and 6 for three unpatched stages. Their Fourier lower requirements are respectively 12,12,7. The seven uniform bound rows also reproduce.

All three rank-distant controls N=32,64,256 reproduce their cycle deficits and nonzero counts for both tested Weyl defects. They are concrete rejected candidates, not universal exclusions. Sixty-four additional arbitrary row-sparse tests, both Fourier orientations, satisfy the consecutive-row bound. The all-parameter conclusions follow from the symbolic theorem, not from finite-field failures alone.

## 2 Moving partitions and twisted reversal

### Rank theorem with moving intermediate sets

Represent an interface permutation by pi such that old coordinate pi(j) enters new coordinate j. For an input subset A_0 set A_i=pi_i^(-1)(A_(i-1)). Let d(A) be the number of natural-order boundaries j,j+1 with different memberships. If stage S_i has upper and lower quasiseparable cut ranks at most r_i, then

    rank(F_N[A_(t-1)^c,A_0]) <= sum_i r_i d(A_(i-1)).

For one stage, split A^c into consecutive runs. Its interaction with columns of A on the left has rank at most r, and likewise on the right. There is one such contribution per boundary, giving rank S[A^c,A]<=r d(A). When retaining columns originally in A_0, each new stage's complementary output is the sum of newly crossing signals and previously complementary signals. Their ranks add. Permutation moves the complementary rows without changing rank. This proves the displayed theorem without requiring invertible stages, nonsingular generator charts, bounded coefficients, or a fixed intermediate partition.

If A_0 is a consecutive interval of M columns, the final output complement has N-M distinct rows. Row scaling converts its Fourier submatrix to consecutive powers of distinct roots, giving rank min(M,N-M). Thus every such input interval supplies an exact necessary inequality. Pulling each natural-order path back to the original input labels expresses the right side as a weighted multigraph cut.

This is genuinely different from using the same subset at every stage. It still assumes each factor is quasiseparable in the stated layout. It cannot automatically be applied to an eight-order Green sum as though that sum had one order-r natural layout. Nor does passing all tested moving cuts guarantee coefficient feasibility or all network separators.

### Binary masks and locality

For N=2^k, a nonzero parity mask m has boundary count

    d_k(m)=sum_(s=0)^(k-1) 2^(k-1-s)
             [popcount(m AND (2^(s+1)-1)) is odd].

The transition j->j+1 toggles exactly the first s+1 low bits when j has s trailing ones; counting these transitions proves the formula. A map pi(x)=Mx+b pulls the membership mask back to M^T m, with an affine constant possibly complementing membership. Complements have the same boundary count. The direction of pi matters: these M matrices represent the declared new-to-old coordinate map, not an unmentioned inverse convention.

If M_s[i,j]=0 for j<i-c, an ancestral top-bit mask remains supported at positions >=k-1-cs after s interfaces. The formula gives d_s<=2^(cs+1)-1 (also a valid, possibly loose bound after reaching the bottom bit). Order at most r at every stage therefore requires

    2^(k-1) <= r [2(2^(ct)-1)/(2^c-1)-t].

For fixed c,r this forces logarithmic depth. At c=r=1 it implies t>=k-1. Repeated cyclic bit rotation has a separate ancestral-mask argument with boundaries 1,3,7,... before wraparound; it has the same stated order-one lower bound. The global rotation is not falsely assumed to obey the banded condition at all bit positions.

### Twisted reversal

For repeated pi=rotl(bitrev), the bit-position map is j->-j mod k. If k=2m, bit m is invariant, its half-set has d=2^m-1, and the complementary Fourier half-block has rank N/2. Writing N=4q^2, q=2^(m-1), two small Fourier changes of basis reduce the block to q^2 invertible two-by-two blocks with primitive-fourth-root entries eta^(uv), u in {2,3}, v in {0,1}, up to nonzero diagonal scales. Thus

    sum_i r_i >= 2^(2m-1)/(2^m-1),
    t >= 2^(m-1)+1 for order-one stages.

If k=2m+1>=3, the parity of bits m,m+1 is invariant with d=2^m. Put q=2^(m-1), N=8q^2. Fourier changes isolate the low-coordinate residues modulo q. The remaining four-by-four blocks have entries eta_8^(XY), X in {2,3,4,5}, Y in {0,1,6,7}, up to nonzero scales. The four X values are consecutive and the four nodes are distinct, so each block is Vandermonde-invertible. This gives

    sum_i r_i >= 2^m,
    t >= 2^m for order-one stages.

The source's displayed odd indexing assumes m>=1; the omitted k=1 case is checked directly and gives t>=1. Even k starts at k=2. If intermediate maps swap rather than preserve membership, the alternate output half-block is also invertible: the even case again has two consecutive row exponents, and the odd case uses cyclically consecutive exponents {6,7,0,1}. Thus the stated preserve-or-swap extension is valid.

These are square-root-depth barriers for this specific repeated twisted-reversal family. Four order-one stages fail at every dyadic N>=64. They do not exclude all global shuffles.

### Certificates and survivor

All 13 serialized four-stage obstructions reproduce from the actual permutation arrays. The reviewer directly recomputes every moving set, boundary sum, and each of the 26 saved determinants over primes 12289 and 65537. Nonzero specialization of a cyclotomic determinant certifies characteristic-zero nonvanishing; this is not finite-field nonexistence extrapolated to complex coefficients.

Additional checks cover all 2036 nonzero masks through k=10, 200 independently generated quasiseparable stage products, and twisted witnesses at N=2 through 1024. Full Fourier half-block ranks are checked through N256 for both possible final membership signs; larger cases use the exact two-by-two/four-by-four proof blocks, not a claimed full dense rank rerun.

The N256 seeded mixing candidate passes all 255 parity masks, with minimum moving capacity 167>128, and all 32895 nonempty proper consecutive intervals, with minimum capacity slack 3. A fresh integer max-flow implementation, using no source modules or third-party graph package, reproduces six tight moving-cut capacities and all 24 saved full-capacity probes across N64,128,256. These remain necessary structural tests. No coefficients or Fourier factorization are supplied by this survivor.

## 3 Weyl character packets

Let N be an odd prime, h a unit modulo N, omega a primitive Nth root, and W_r=X^h Z^r, where X^h e_j=e_(j+h) and Z e_j=omega^j e_j. Work over a field with N invertible and the stated root. For alpha^N!=1,

    W_r^m e_j=omega^[r(mj+h m(m-1)/2)] e_(j+mh),
    W_r^N=I,
    W_r W_q=omega^[h(r-q)] W_q W_r.

The finite geometric expansion gives G_r=(I-alpha W_r)^(-1). Averaging with the selected operator-index character yields exactly

    H_s e_j = (1-alpha^N)^(-1)
              sum_(0<=m<N, mj+h m(m-1)/2=s) alpha^m e_(j+mh).

For every nonzero m there is one j, since N is prime. For m=0 the identity contribution occurs precisely at s=0. With alpha!=0 these positions are distinct and nonzero, giving N-1 entries for s!=0 and 2N-1 for s=0. Index inverses can be generated in O(N) modular-word operations, powers of alpha incrementally in O(N) field operations, and the sparse operator applied in one O(N) pass. This is a valid fusion of N dense solves for one selected aggregate. It does not compute all N aggregates in O(N), nor a full Fourier transform.

All W_r have the same support order. In fact, for u_h(t)=t(t-h)/(2h) modulo N and D_r[t,t]=omega^[r u_h(t)],

    W_r=D_r X^h D_r^(-1).

Thus their projective noncommutation comes from chirp gauges, not genuinely different Hamiltonian support permutations. Roots, coefficient generation, inverses, and arithmetic precision must be charged in their respective models; the O(N) statement is not a bit-complexity claim.

### Arbitrary weights and stronger zero-minor exclusion

For T=sum_r c_r G_r and chat(q)=sum_r c_r omega^(rq), write m=h^(-1)(i-j) in {0,...,N-1}. Then

    T[i,j] = alpha^m/(1-alpha^N) * chat(u_h(i)-u_h(j)).

This entry formula is valid. It does not make chat free for arbitrary fresh weights, nor supply O(N) application of a generally dense arbitrary-weight packet. For alpha!=0, the selected character packets have disjoint nonempty matrix supports, proving the span has dimension N. At alpha=0 it instead has dimension one.

Since u_h(h-t)=u_h(t), use row pair {0,h} and column pair {2h,-h}, valid and distinct for prime N>=5. Every entry uses the same chat value. The two determinant products have powers alpha^N on both sides: the corresponding nonzero signed step representatives sum to N. Hence the two-by-two determinant is zero for every choice of c, including the alpha=0 special case.

For prime N, every two-by-two Fourier minor on distinct rows r_0,r_1 and columns c_0,c_1 is nonzero, since its determinant is a nonzero root factor times

    1-omega^[(r_1-r_0)(c_1-c_0)],

and the exponent is nonzero modulo N. Arbitrary independent row and column permutations preserve this property, as do invertible diagonal gauges. Therefore the packet zero minor excludes every monomially gauged/permuted prime Fourier matrix, including non-affine permutations. The source's limitation to affine permutations is unnecessarily narrow.

This does not exclude term-specific endpoint masks, several different h values combined, genuinely different support orders, or a forced intermediate operator such as B=(F^(-1)+A)^(-1). The N3 case does not have the displayed N>=5 reflected witness. No map realizing that forced B from these packets is given by v20. In particular, the separate three-point chirp construction is not contradicted by this Fourier-packet gate.

## 4 Krylov propagation and the inherited denominator correction

If A[i,j]!=0 defines an arc j->i, then A^d e_j is supported within d directed steps of j. Every vector in span(e_j,Ae_j,...,A^d e_j) has the same support restriction, regardless of adaptively chosen scalar coefficients. If A^(-1)[i,j]!=0, the required degree is at least the directed distance from j to i. A dense inverse therefore forces worst-case degree at least the support diameter.

With maximum outgoing support count Delta>1, at most 1+Delta+...+Delta^d vertices are reachable. Thus

    N <= (Delta^(d+1)-1)/(Delta-1).

For Delta=1 use the separate bound N<=d+1; the logarithmic displayed expression is undefined there. Constant Delta>1 gives Omega(log N) degree. A literal schedule of that many separate matrix-vector passes, each costing Theta(N), costs Omega(N log N). Degree alone does not prove that every structured polynomial evaluation or non-Krylov solver performs that schedule. The source correctly scopes the propagation theorem; its broad Fourier-denominator motivation needs correction.

If A^(-1)=L F_N R for invertible monomial L,R, then A=R^(-1) F_N^(-1) L^(-1), which is dense at every N. A constant-degree sparse direct denominator cannot satisfy this equation, irrespective of treewidth or Krylov/non-Krylov evaluation. For A=I-sum_(j=1)^g alpha_j P_j, each row has at most g+1 occupied positions; density forces g>=N-1. This corrects the inherited v19/v20 proposed escape, without asserting a lower bound for unrelated implicit formulations or multi-operator products.

Independent controls verify 150 full selected-character matrices at prime N=3,5,7,11,13,17,19 with h=1,2; 14 arbitrary-weight entry formulas; 12 weighted-packet zero minors and every prime Fourier two-by-two minor at the checked N>=5; 14 alpha-zero guard cases; and all four source Krylov examples over F_1009. The saved inverse-polynomial degrees 6,10,12,16 and diameters 6,10,6,6 reproduce. The examples do not validate a sparse Fourier inverse that the direct density argument forbids.

## 5 Replay and scope ledger

Run the four review-authored programs: check_phase34.py, check_moving.py, check_weyl_v20.py, and check_flow.py. They import only exact_utils.py and Python standard-library modules. The uploaded programs under sources/ are never imported or executed. PORTABLE_REPLAY.json records isolated replay with only these five programs and the four required source JSON data files; all four result files must match byte-for-byte.

The source benchmarks are mechanism demonstrations against literal research implementations, not FFT-library comparisons, and were not rerun. The review retains the distinctions among an algebraic identity, a necessary rank or separator inequality, generic/local behavior, a coefficient-consistent exact Fourier product, and a fully charged fast evaluator. None may replace another without a proof.
