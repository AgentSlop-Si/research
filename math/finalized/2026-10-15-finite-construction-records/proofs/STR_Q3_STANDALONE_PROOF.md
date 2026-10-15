# Accepted non-Fourier tensor compiler instantiation

Independent proof, 11 October 2026. This is a scoped mathematical acceptance, not a claim of worldwide novelty, practical acceleration, or validation of a production implementation.

## 1. Statement and exact computational contract

Let d >= 1, N = 2^d, M = [[3,-4],[4,3]], and U_N = (M/5)^{tensor d}. The operator is specified by this fixed family and N, not by an arbitrary N-by-N input matrix. The input is an arbitrary length-N complex dyadic vector; each real and imaginary part is a*2^e, where |a| < 2^(Bd) and |e| <= Bd for a fixed B. Zero is legal. Let epsilon = 2^(-t), with integer t >= 0 and t <= C_t d for a fixed C_t.

The model is an address-capable word RAM with w = C d bits for a sufficiently large fixed C depending on B and C_t, and constant-word integer arithmetic, multiplication, shifts, comparisons, and division. This is not an exact real-arithmetic model, a field-operation count, or a bit-operation count. Outputs are N explicit dyadic mantissa/exponent pairs per real/imaginary array; exponents need not stay within the input's polynomial numerical range.

For 1 <= k <= d, define

    m = 2^k, q = ceil(d/k), L = q+1,
    eta = epsilon/(8L),
    p = t + ceil(log2(1536 m L)), h = 2^(-p),
    b = 2(p+2), E = 2+mb.

If E <= d/2, a uniform cold algorithm computes y with

    ||y-U_N x||_2 <= epsilon ||x||_2

in O(NL + d + m^2 k + 2^E m^2) word operations and O(N + 2^E m) words. Preparation, input validation, key formation, table population, coefficient generation, routing, and every output are included. In particular the work is O(NL + N^(1/2) polylog N), and storage is O(N) for sufficiently large N.

For each fixed t, a selectable m = Theta(d/log d) yields L = Theta(d/log d), hence O(N log N/log log N) word work. If no admissible k exists, direct rounded size-two block evaluations give O(Nd) word work with the same error contract. No fast-table claim is made for that branch. For any fixed a > 0, t >= ad forces every legal table choice to have m < 1/(4a). This last assertion concerns only this sufficient budget.

## 2. Orthogonality, exact factorization, and non-Fourier witness

Since M^T M = 25 I, U_N is real orthogonal and hence unitary on complex vectors. Every entry is a nonzero signed product of d factors in {3/5,4/5}; the matrix is dense and full rank.

Partition the binary coordinates into consecutive groups of lengths r_j = min(k,d-(j-1)k), and set n_j = sum_{i<=j} r_i. On group j, apply M^{tensor r_j}; apply identity on the other digits. Call this layer A_j. Append A_L = 5^(-d) I. Operations on different digits commute, so the product of all layers is U_N. This also verifies the least-significant-digit-first convention directly.

Fix all but one row and column digit and take the resulting 2-by-2 rectangle. Its absolute cross ratio is |3*3/((-4)*4)| = 9/16. Every normalized finite-abelian Fourier character matrix has every such absolute cross ratio equal to one, because its entries all have the same nonzero magnitude. Multiplication by arbitrary invertible diagonal matrices on both sides cancels in each rectangle ratio, and row/column permutations merely permute rectangles. U_N is therefore not diagonally/permutation equivalent to a finite-abelian Fourier character matrix. This is the exact meaning of non-Fourier accepted here.

## 3. Paid balancing and constant numerical-template diversity

Each raw prefix P_j, j <= q, equals 5^(n_j) times an orthogonal map. Thus its two separate norm certificates are

    ||P_j|| = 5^(n_j), ||P_j^(-1)|| = 5^(-n_j),

whose product is one. Define f(n) as the unique integer with 2^f(n) <= 5^n < 2^(f(n)+1), and set s_j = 2^(-f(n_j)), with s_0 = s_L = 1. The scaled prefix is s_j P_j = rho_j times an orthogonal map, where

    rho_j = 5^(n_j)/2^f(n_j), 1 <= rho_j < 2.

Hence every scaled prefix and its inverse have norms at most 2. The inverse interior norm is actually <= 1. Endpoints are exactly unitary. The scaled block in digit group j is

    B_j = M^{tensor r_j}/2^(f(n_j)-f(n_{j-1})),

and the last scalar is c_N = 2^f(d)/5^d in (1/2,1]. Every digit block has norm rho_j/rho_{j-1} < 2, and the final scalar has norm <= 1. Thus Kappa = 1, K = 2, G = 2 are valid; merely knowing a condition number of one would not have sufficed without these scales.

Construct 5^n by multiplying by five once per digit. Its floor exponent rises by two or three; a constant number of comparisons locates the next exponent. All relevant integers have O(d) bits, so this costs O(d) word work and O(L) retained words. Reciprocal envelopes use the same denominator and need no root, logarithm, SVD, or norm oracle. The real logarithm below is used only for the proof of diversity, never for construction.

For a full k-digit group, f(n+k)-f(n) belongs to {floor(k log2 5), ceil(k log2 5)} by the floor-addition identity. There are therefore at most two full-group numerical templates, at most one shorter residual template, and one final scalar template: T <= 4. Actual dimensions are used; no padding layer or hidden dense identity is executed. The four bound is attained, for example, at d=5,k=2: digit templates have (r,delta) = (2,4),(2,5),(1,2), followed by the scalar.

## 4. Fully paid finite tables

Construct each needed M^{tensor r} as integer coefficients, for example by multiplying the r selected entries of M for each row/column pair. There are O(m^2) coefficients and each has O(k) bits. The conservative preparation cost is O(m^2 k). There are at most two different unscaled block sizes; repeated scalar versions do not require different integer matrices. The final scalar numerator/denominator were computed above.

For a nonzero complex block v of actual dimension ell <= m, let H be the largest absolute real or imaginary coordinate. Find a power-of-two s satisfying H <= s < 2H. Set u=v/s and round its coordinates to the nearest h-grid point, obtaining q in [-1,1]^(2ell). A zero block maps exactly to zero.

Each real grid digit is an integer a in [-2^p,2^p]. Encode a+2^p in p+2 bits. The complex key has 2ell(p+2) <= mb bits. Decode every unused field value above 2^(p+1) as +2^p. This defines the table on the whole power-of-two address space, not just on valid keys. Actual calls use only valid fields. Different templates have separate charged tables or a two-bit template identifier.

For each template and each padded key, compute Bq and round every real/imaginary output to h Z. This calculation needs no coefficient approximation oracle. If B=A/D with integer matrix A and positive integer denominator D, and q=a h, the output grid digit is round_nearest((A a)/D). Integer sums and rounded division suffice. Digit matrices use D=2^delta; the scalar uses A=2^f(d),D=5^d. Products, sums, quotients, and remainder comparisons occupy O(p+k+log m) or O(d+p+log m) bits. Under the budget these are O(d), and for the fallback they are also O(d) because t=O(d). One division is one constant-word operation in the stated model.

There are at most 4*2^(mb)=2^E table entries. Enumerating every address, decoding its O(m) fields, densely evaluating its O(m)-by-O(m) block, and writing all O(m) result coordinates costs O(m^2) per entry, yielding O(2^E m^2) work and O(2^E m) words. This is an eager cold-table existence construction; small reference tests do not constitute its practical implementation.

## 5. Local and global error, including nonlinear rounding

Nearest rounding gives

    ||u-q||_2 <= sqrt(2ell) h/2 <= m h,
    ||z_B(q)-Bq||_2 <= sqrt(2ell) h/2 <= m h.

Since ||B|| <= G=2 and s < 2||v||_2,

    ||s z_B(q)-Bv||_2
      <= s (G+1)m h
      < 2(G+1)m h ||v||_2
      <= (eta/32) ||v||_2
      <= eta ||v||_2.

Here h <= epsilon/(1536mL) = eta/[64m(G+1)]. This is stronger than the required local guarantee. The table-value error is in particular <= eta/192 < eta/8. Ties can use any fixed nearest rule; the reference controls use ties toward +infinity for both signs. Direct sums preserve the local bound because squared errors add across disjoint blocks.

For the implemented nonlinear layers a_j, let y_0=x,y_j=a_j(y_{j-1}), and w_j=(P'_j)^(-1)y_j. No linearity of a_j is presumed. With separate prefix norms <=K=2,

    ||w_j-w_{j-1}|| <= K^2 eta ||w_{j-1}||.

Induction and telescoping give

    ||y_L-U_Nx|| <= ((1+4eta)^L-1)||x||
                  <= (exp(epsilon/2)-1)||x||
                  <= epsilon ||x||,

because 0<epsilon<=1. The last inequality follows, for example, from convexity of exp on [0,1/2] and exp(1/2)-1<1. This proves the all-input relative l2 assertion independently of finite test success.

## 6. Word size, exponents, routing, and output traffic

An output table coordinate has magnitude <= ||Bq||+h/2 <= 2 sqrt(2m)+h/2, so its integer grid mantissa has O(p+log m) bits. Scaling it by s is an exact exponent adjustment, not an enormous integer shift. Across one layer, exponent magnitudes can change by O(p+log m+log(G+1)); across L<=d+1 layers the magnitude is O(d^2), plus the O(d) input contribution. Its binary description is only O(log d) bits. Each coordinate is therefore O(1) words. A final restriction to polynomial numerical dynamic range is not part of the contract and would require a separately charged truncation.

Normalize and quantize by inspecting mantissa bit lengths and exponent differences. If a negative shift exceeds the mantissa's bit length plus one, its nearest grid digit is zero; compare first rather than performing the huge shift. For the remaining cases all shifts are O(d). Signed half-grid ties are settled by a quotient/remainder comparison. Thus polynomial-sized exponent values do not imply polynomial-sized mantissas or free unbounded-bit work.

Bit-length need not be a primitive. For sufficiently large d, prepare a leading-bit table on floor(d/8)-bit chunks in O(2^(d/8)) work and storage using length[i]=length[i>>1]+1. An O(d)-bit word has a fixed number of these chunks. Locate the highest nonzero chunk and look up its bit length in O(1) word work. This preparation is O(N) and is absorbed by NL and N storage. Bounded small d is a fixed finite case. This explicitly reconciles the bit-length requirement with the listed RAM primitives.

For a group of r digits starting at position u, blocks have indices

    a*2^(u+r) + v*2^u + b,
    0<=a<N/2^(u+r), 0<=b<2^u, 0<=v<2^r.

These blocks partition all N coordinates. Addresses use O(d) bits. Per block, gather, maximum/scale selection, quantization, packing, reading all table outputs, exact exponent rescaling, and scatter cost O(2^r). Therefore each layer costs O(N), including the final scalar layer and all zero outputs. Input validation and every final output also cost O(N). There is no O(N/m) claim for a whole layer and no free large-arity gate. The known family is recognized from N and its fixed definition; arbitrary raw dense-matrix recognition is excluded.

## 7. Uniform parameter selection and accuracy boundary

When the budget holds, m=O(d), and E<=d/2 gives the stated cold-table and storage bounds. The term d+m^2k is polynomial in d; it is included explicitly and is negligible compared with N. The parameter selector scans 1<=k<=floor(log2 d), computes L,p,b by integer arithmetic, and picks the largest legal k. Any legal k is in this range because mb+2<=d/2 implies m<d. Its polynomial-in-d work is absorbed by NL.

For fixed t and m near a sufficiently small constant times d/log d, k=Theta(log d), L=Theta(d/log d), and p=O(log d). Hence mb=O(m log d), and a sufficiently small constant makes mb+2<=d/2. Rounding m down to a power of two preserves Theta(d/log d). All coefficients, tables, and parameters are recomputed from d,t; this is a uniform algorithm rather than nonuniform advice.

If no k is legal, choose k=1 and directly compute each requested rounded local value using its size-one or size-two rational block. The local-error proof still applies. There are d+1 layers, each costing O(N), so O(Nd) work and O(N) words suffice with t<=C_t d.

For t>=ad, p>=t and b>=2ad. The budget then implies 2+2adm<=d/2, hence m<=1/(4a)-1/(ad)<1/(4a). Thus growing blocks are impossible under this exact sufficient certificate at polynomial relative accuracy. This is not an impossibility theorem for tensor transforms, a bound for all algorithms, or a transfer to a different arithmetic model.

## 8. Dependency and antecedent boundary

The candidate is an instantiation of H01 T1 at SHA-256 4afd27bacea1bd896d8b44e7e4c1eb51c1b24b3db997ceca9e554e69f81202bb and P05 S1 at SHA-256 02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787. The preceding proof states and verifies their needed mechanisms in full. Their accepted ledger entries R01 and R19 concern this finite-word, paid-preparation, separate-prefix-norm scope.

The Kronecker algebra and ordinary O(Nd) separable transform are classical. Charles Van Loan's 26 October 2009 author-hosted lecture verifies the mixed-product identities (PDF page 4), reshaped application (page 5), and shuffled block-diagonal factorization (page 13): https://bpb-us-e1.wpmucdn.com/blogs.cornell.edu/dist/c/9924/files/2021/11/KPHist.pdf. These antecedents do not by themselves establish or refute priority of the precise finite-word lookup corollary. No priority assertion is made.
