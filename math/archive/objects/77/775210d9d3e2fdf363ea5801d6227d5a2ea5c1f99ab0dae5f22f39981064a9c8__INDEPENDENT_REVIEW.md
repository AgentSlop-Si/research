# Independent review of Weyl packet completeness and chirp fusion

## Result

Accepted with explicit parameter and cost guards. At odd prime length, all nonzero-shift Weyl character packets generically form a basis for off-diagonal matrices; adding the identity spans exactly the constant-diagonal matrices. A diagonal gauge of the full Fourier matrix has an exact representation in N-1 Green slots on one common Weyl line. The fused operator is the full quadratic-chirp convolution from the classical chirp-transform reduction. There is no faster transform in this result.

An additional independent strengthening removes the need to search for a generic complex parameter: every 0<|alpha|<=1/2 works for the basis theorem. In particular alpha=1/3 has a uniform elementary inverse-norm bound for each coefficient block. This improves the existence guard, not the charged evaluation complexity.

The source archives received at 00:36 and 00:42 are byte-identical (SHA256 d23a528d5beed5ba2d1635fab3b54ae0c572f9527fd892cdc7ee7a4a7cfe6f59). Both source IDs are recorded in SOURCE_PROVENANCE.json, with one mathematical audit. Their nested v20 ZIP exactly matches the previously reviewed predecessor, SHA256 43c0e5499b77d2d96dfa72ae59ff00dbd45d9aa190ff104e830bd1d1aab93eea. The new claims belong to the supplied source; no publication priority is inferred.

## Definitions and packet proof

Work over C, N an odd prime, omega=exp(2 pi i/N), X e_j=e_(j+1), Z e_j=omega^j e_j. Arithmetic exponents of omega are modulo N; divisions by 2 and nonzero h in these exponents mean modular inverses. Powers of alpha use ordinary representatives 0,...,N-1. Set W_(h,r)=X^h Z^r, h!=0, G_(h,r)=(I-alpha W_(h,r))^-1. The guard alpha^N!=1 is necessary and sufficient because W^N=I and W is a single weighted N-cycle.

The geometric series and character filter give

    H_(h,s)[j+mh,j] = alpha^m/(1-alpha^N)
                      if m j + h m(m-1)/2 = s mod N,
                      and zero otherwise.

For fixed j this is a nondegenerate quadratic in m. For fixed output i, substitute j=i-mh to obtain m i-h m(m+1)/2=s, again nondegenerate. Each packet has at most two nonzeros per row and column. With alpha!=0 its exact total is N-1 for s!=0 and 2N-1 for s=0: for every m!=0 there is exactly one j, while m=0 contributes all diagonal entries precisely when s=0. Alpha=0 makes H_(h,0)=I and the other packets zero; this boundary is excluded by the basis guard, and must not be assigned the nonzero support count.

## Block decomposition and basis

For displacement delta!=0 write t_delta(j)=T[j+delta,j]. Define positive-sign Fourier coefficients t_hat_delta(k)=sum_j t_delta(j)omega^(kj), and c_hat_h(ell)=sum_s c_(h,s)omega^(ell s). Substitution s=mj+h m(m-1)/2 with m=[delta/h]_N gives

    t_hat_delta(k) = (1-alpha^N)^-1 sum_(h!=0)
       alpha^[delta/h]_N omega^(-k(delta-h)/2) c_hat_h(kh/delta).

The invertible transforms and reindexing x=k/delta split this square coefficient map into N blocks

    B_x(delta,h)=alpha^[delta/h]_N omega^(-x delta(delta-h)/2).

The determinant degree is at most (N-1)^2. Equality requires h=-delta in every row, which is one permutation and has a nonzero root-of-unity coefficient. The determinant is therefore a nonzero polynomial. There is also a unique lowest-degree term alpha^(N-1), contributed by h=delta, with coefficient one. Thus P_N=product_x det B_x is nonzero, and P_N(alpha)(1-alpha^N)!=0 proves the off-diagonal basis claim.

Restriction to off-diagonals already makes the N(N-1) packets independent. Their diagonals are constant. The identity is independent of them, since a packet combination with vanishing off-diagonal part must vanish. Hence adjoining I gives dimension N(N-1)+1, exactly the constant-diagonal subspace, with unique coefficients for each matrix there.

The exceptional guard is substantive. At alpha=-1, all Greens are invertible for odd N, but B_0 has row_-delta=-row_delta, hence rank at most (N-1)/2. Merely checking Green denominators cannot certify completeness.

## Explicit complex guard and its cost meaning

For each fixed delta, h -> delta/h permutes the nonzero residues. B_x has diagonal alpha and off-diagonal magnitudes |alpha|^2,...,|alpha|^(N-1). For 0<r=|alpha|<=1/2,

    sum_(m=2)^(N-1) r^m < r.

Every B_x is strictly diagonally dominant. An elementary maximum-coordinate argument proves its kernel is zero, without a spectral assumption. This proves the basis and representation simultaneously for the explicit parameter alpha=1/2. The diagonal-dominance gap there is 2^(-(N-1)); no good numerical conditioning follows from that particular bound.

For the alternative alpha=1/3, the gap exceeds 1/6. The same argument gives ||B_x^-1||_infinity<6 and ||B_x||_infinity<1/2, so this elementary condition-number bound is below three uniformly in N. These norm statements use ordinary complex modulus. They do not transfer to finite fields, nor turn an infinite Neumann expansion into a finite exact cheap solver.

## Full Fourier representation and uniqueness

Use the unnormalized positive-sign F[i,j]=omega^(ij), and D[i,i]=omega^(-i^2). The target DF has diagonal one and displacement profile omega^(-delta j-delta^2). Its positive displacement Fourier transform is supported only at k=delta, with value N omega^(-delta^2). Consequently only block x=1 is needed:

    B_1 A = (1-alpha^N) (omega^(-delta^2))_(delta!=0).

Inverting this (N-1)-square block gives A_h; the packet coefficients are c_(h,s)=A_h omega^(-hs), because c_hat_h(h)=N A_h. Summing the packets over s produces exactly G_(h,-h). The scalar correcting the diagonal is

    lambda = 1 - (sum_h A_h)/(1-alpha^N).

Thus DF=lambda I+sum_(h!=0) A_h G_(h,-h). For this Fourier identity alone, invertibility of B_1 suffices; all-block genericity is a convenient stronger guard.

The N-1 phrase counts available Green terms, not a proved minimum at every specialization. The saved N=13 finite-field case has 10 nonzero A_h among 12 slots. For generic complex alpha all A_h are nonzero: near zero, B_1=alpha(I+O(alpha)) and A_h=alpha^-1 omega^(-h^2)+O(1), so no coefficient is the zero rational function. Extra exceptional zeros can occur at particular parameters.

## Exact fusion and the classical interpretation

For U=XZ^-1,

    X^h Z^-h = omega^(h(h-1)/2) U^h,
    DF = sum_(h=0)^(N-1) omega^(-h(h+1)/2) U^h.

These signs follow directly from U^h e_j=omega^(-hj-h(h-1)/2)e_(j+h). Every Green term is a rational function of the same U, so the terms commute. They are not independent noncommuting scan orders.

The symmetric identity

    omega^(ij)=omega^(i^2/2) omega^(-(i-j)^2/2) omega^(j^2/2)

makes F diagonally equivalent to cyclic convolution by g_d=omega^(-d^2/2). The full chirp coefficients can be generated in O(N) arithmetic by updating consecutive ratios. A diagonal similarity converting U to X likewise has O(N) preparation and application cost. The remaining convolution is DFT-equivalent in both directions up to these invertible diagonal operations.

All chirp coefficients are nonzero. Their spectral values are nondegenerate quadratic Gauss sums. Directly expanding the squared modulus and setting d=h-k leaves an inner character sum sum_k omega^(2 a d k), zero for d!=0 and N for d=0. Thus every spectral value has magnitude sqrt(N). Full coefficient and spectral support is an obstruction to those sparsity shortcuts, not a general arithmetic lower bound.

The supplied source appropriately attributes the filtering/chirp reduction to Bluestein and the chirp-z literature. The publisher's 1969 abstract explicitly describes the convolution reduction: [Rabiner, Schafer and Rader](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1969.tb04268.x). Its institutional record is [Nokia Bell Labs](https://www.nokia.com/bell-labs/publications-and-media/publications/the-chirp-z-transform-algorithm-and-its-application/). Bluestein's supplied 1970 DOI resolves to [the IEEE record](https://doi.org/10.1109/TAU.1970.1162132), whose full page was blocked by a JavaScript check during this audit; no unseen text from it is quoted or relied upon. The algebraic equivalence above is independently proved.

## Charged operations and boundaries

A selected packet has Theta(N) structural nonzeros for alpha!=0 and can be enumerated in O(N): for each m!=0 solve the one scalar congruence for j, add the s=0 diagonal, and precompute modular inverses and alpha powers. A literal separate sparse execution therefore costs Theta(qN). A dense monomial-gauged Fourier target needs q>=ceil(N/2), since each column has at most 2q supported entries; this yields Omega(N^2) for that explicit separate-packet schedule. Including a free identity term weakens the count to ceil((N-1)/2) and still leaves the same asymptotic separate-scan conclusion.

Each dense Green applies by a weighted cyclic scan in Theta(N). Executing N-1 supplied slots separately is Theta(N^2); generic coefficients indeed activate all slots. This is not a lower bound on a fused implementation, nor on the number of necessary terms at every exceptional parameter.

Coefficient preparation is not free. The explicit alpha guard avoids an exceptional-parameter search over C. The Fourier coefficients still require solving the B_1 system; ordinary elimination costs O(N^3) field operations and O(N^2) storage after constructing its entries. Arbitrary constant-diagonal data uses N such blocks, O(N^4) with straightforward elimination, plus coefficient transforms. These are valid charged upper bounds, not claimed optimal bounds. The source's prototype may use even denser systems; its tests are certificates, not scalable setup oracles.

The already known chirp polynomial avoids this coefficient solve entirely but remains a full convolution. Direct evaluation is quadratic; conventional convolution FFT is O(N log N), including O(N) chirp and indexing work. An exact faster evaluator for this specific convolution would, by the diagonal identities, itself give an exact faster DFT. The source supplies none. Two non-collinear Weyl-line products are only a proposed next architecture; the present results neither synthesize them nor exclude all of them. This prime-length one-line analysis does not supersede the separately accepted dyadic N16 eight-order coefficient certificate.

## Independent controls and replay

The newly authored standard-library checker verifies all four saved fields (N=7,11,13,17) and additional N=3,5,19 specializations. It checks every entry of every character packet against independently inverted resolvents; the full off-diagonal ranks at all lengths through 17; every B_x rank; arbitrary constant-diagonal reconstruction; independently solved Fourier-line coefficients; iterative U powers, chirp polynomial and symmetric identity; all chirp spectral entries; and nonpole exceptional alpha controls. It also enumerates determinant permutations at N=3,5,7, checking both unique extremal degrees, and exact rational dominance bounds through N=1021.

The saved source's file called independent_verifier checks chirp entries, block ranks and sampled support, but does not itself reconstruct the Green-line identity or arbitrary targets. This review supplies those additional independent checks. Source execution and test-count claims are not mistaken for our own replay.

Run `python3 independent_checks.py` with the Python standard library. PORTABLE_REPLAY.json records an isolated temporary-directory run and byte-identical output. Original source programs and bytecode were never imported or executed. The exact finite-field controls corroborate the written characteristic-zero proofs; they do not substitute for them.
