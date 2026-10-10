# Independent Fourier endpoint rank audit

9 October 2026. The uploaded archive `fft_optimal_endpoint_rank_gate_2026-10-09(1).zip` contains a sound, self-contained characteristic-zero proof of the optimal quasiseparable rank of one dyadic Fourier matrix under independent endpoint reorderings. It supplies no new transform evaluator or FFT arithmetic-complexity improvement. This audit also proves an integer per-cut strengthening and exact total-rank optimality at N=8 and N=16.

The source archive is preserved byte-for-byte in this supplement. Its top-level folder is named `fft_subset_spectral_gate_2026-10-09`; the different outer filename does not change its contents. All 15 entries in the source SHA256 manifest were verified. Source programs were read but never executed or imported. The reproducible tests here were independently authored and use only the Python standard library. No literature-priority claim is made.

## Accepted theorem and field scope

For an N by N matrix A, define q(A) as the maximum, over cuts k=1,...,N-1, of the upper-right and lower-left off-diagonal block ranks. For N=2^m with m>=3 and the complex Fourier matrix F_N,

`min_(rho,sigma) q(P_rho F_N P_sigma^T) = N/4+1`.

The row and column permutations are arbitrary and independent. Applying bit reversal to both endpoints achieves the minimum. Thus this theorem really is endpoint-unrestricted within its single-matrix rank question. It is not a theorem about unrestricted Fourier circuits, and the dyadic size restriction is essential to the supplied proof.

The universal lower bound is proved over the complex numbers using positivity and orthogonal projections. The same ranks are unchanged in a characteristic-zero field containing the requisite algebraic roots. The audit does not extend that lower bound to all finite fields. Finite-field agreement below is a regression control, not a substitute for the characteristic-zero proof. The constructive bit-reversal recurrence and coset decomposition themselves work over fields with the required primitive roots and characteristic not dividing N.

## Why the endpoint lower bound is valid

Let N=4L, L>=2, and choose any two sets H,I of size h=t=2L+1. Let U=F_N/sqrt(N). On the coordinate space supported on H, the positive contraction

`A = P_H U* P_I U P_H`

has eigenvalue-one multiplicity d equal to the dimension of vectors supported on H whose Fourier transforms are supported on I. Equivalently,

`d = h - rank F_N[I^c,H]`.

Every eigenvalue is in [0,1], hence d<=tr(A^2). Define c_H(s)=|H intersect (H-s)| and hat1_I(s)=sum_(a in I) omega^(as). Expanding the squared Frobenius norm gives

`tr(A^2) = N^(-2) sum_s c_H(s) |hat1_I(s)|^2`.

Every nonzero translation of the cyclic group of dyadic order has even-length cycles. Since h is odd, H cannot be invariant under any such translation. Therefore c_H(s)<=h-1 for s!=0, while c_H(0)=h. Parseval gives sum_s |hat1_I(s)|^2=Nt. Consequently,

`tr(A^2) <= ((h-1)Nt+t^2)/N^2`

`= L+3/4+1/(4L)+1/(16L^2) < L+1`.

Since d is an integer, d<=L. Every (2L-1) by (2L+1) Fourier submatrix therefore has rank at least L+1. The upper-right block at cut 2L-1 is such a submatrix for every independent endpoint ordering. This proves the universal lower bound.

## Why double bit reversal attains it

Let r_N(k) be the upper-right cut rank after bit reversal of both endpoints. For N=4L and 0<=k<=N/2, the source proves the exact recurrence

`r_N(k) = ceil(k/2) + r_L(floor(k/2))`.

The first N/2 bit-reversed labels are the even Fourier indices. Among the selected k even frequencies, there are p=floor(k/2) complete pairs and possibly one unpaired frequency. All odd natural-time columns lie to the right of the cut. They span the pair-antisymmetric coordinates and the unpaired coordinate, with dimension ceil(k/2). Taking paired-row sums identifies the quotient with the smaller Fourier cut r_L(p).

The potentially delicate odd-cut endpoint is correct: when k=2p+1, the surviving member of the partly removed even-column pair still contributes residue b_(m-2)(p). The smaller column set therefore starts at p, not p+1. Index reversal changes the matrix only by invertible diagonal scalings, giving r_N(k)=r_N(N-k). The base ranks at N=1,2 are correct.

For even k<=N/2, the recurrence bounds the rank by L. For odd k it bounds the rank by L+1, attained at k=2L-1 when L>=2. The matrix is symmetric, so lower-left ranks equal the corresponding upper-right ranks. This proves the matching upper bound.

## Rank sums and the bounded extension

For any independently reordered Fourier matrix, the first trace gives the pointwise bound

`r(k) >= ceil(k(N-k)/N)`.

In particular, summing the unrounded values proves the source bound S>= (N^2-1)/6. Summing the bit-reversal recurrence gives

`S_N = N^2/8 + N/4 + 4 S_(N/4)`.

For N=2^m, this solves to

- m even: `S_N = N^2/6 + N(m/8-1/6)`
- m odd: `S_N = N^2/6 + N(m/8+1/24)`

Thus bit reversal is asymptotically optimal in the leading term N^2/6. The source does not claim exact minimum total rank for every finite N.

A further consequence of the same proof is useful. At every odd cut k, h=N-k is odd. Repeating the second-moment calculation with |H|=|I|=h gives

`r(k) >= ceil(k(N-k)(N+1)/N^2)`.

Indeed, `h-((h-1)Nh+h^2)/N^2 = k(N-k)(N+1)/N^2`. At even cuts, retain the first-trace ceiling bound. These are valid simultaneously for every ordering.

For N=8 the resulting lower profile is

`[1,2,3,2,3,2,1]`, with sum 14.

For N=16 it is

`[1,2,3,3,4,4,5,4,5,4,4,3,3,2,1]`, with sum 48.

Both profiles exactly match double bit reversal. It is therefore pointwise cut-rank optimal at these sizes, and the exact minima of the total upper-right rank sums are 14 and 48. The same argument gives totals 1 and 3 at N=2 and N=4. This extension does not establish larger-size exact optimality: at N=32 the bound sums to 182 while bit reversal gives 192; at N=64 the values are 708 and 720.

## Relationship to the earlier window theorem

The inherited window audit remains valid and separate. Its two-stage consequence `N<=9r^2+7r` assumes natural or affine coprime-stride input order, while allowing arbitrary output order. At r=1 it gives N<=16, sharp for that necessary window filter, not a proof that a factorization exists.

The new endpoint theorem concerns q of the entire Fourier matrix. It does not remove the earlier window theorem's input-order condition or permit replacing arbitrary Fourier submatrix ranks by full Vandermonde ranks. The exact reordered N=16 control still has rank 8 for the 13 by 9 submatrix tested here; the naive min(rows,columns)=9 substitution is false.

For the restricted case in which every factor is measured in one common coordinate order, the off-diagonal block product formula gives q(AB)<=q(A)+q(B). Thus an exact s-stage product with each q<=r must satisfy sr>=N/4+1. The upper-right total-rank sums are also subadditive, so the factors' summed totals must exceed the Fourier lower bound. Arbitrary interstage coordinate changes invalidate a free application of this deduction: permutation matrices must be included as factors, or their cut ranks otherwise charged in the inequality. This remains a rank statement, not an arithmetic lower bound.

## Exact coset identities and exploratory screens

The source full-coset identity is correct. For N=QL, input columns in complete cosets b+Qj, and any output rows K, applying a Fourier basis change separately within each input coset separates output residues modulo L. The resulting rank is the sum of the corresponding smaller F_Q block ranks. A consecutive part of one coset has Vandermonde rank equal to the minimum of its length and the number of distinct output residues modulo L.

The independently reproduced N=8, GF(12289) screens cover all 40,320 internal permutations:

- Earlier interval-window screen: 15,728 survivors
- All-subset boundary screen: 31,384 survivors
- All retained support supersets for interval windows: 15,728 survivors, exactly the same set as the interval-window screen
- First-trace uncertainty screen: 40,320 survivors, rejecting none at this size

Every interval-window survivor also passes the other two weaker screens. These are finite-field necessary-screen counts, not counts of factorizations. The uploaded standalone `subset_gate.py` main block refers to an external sibling `window_gate` module rather than the included `prior_window_gate`; that exploratory entry point is not self-contained in this archive. This does not affect the proof or the independent portable checks. No uploaded file was modified.

## Reproducible controls and computational accounting

Run the two independently authored programs in this audit directory:

`python3 independent_checks.py`

`python3 independent_screen_checks.py`

Python 3.10 or later suffices. No NumPy, external archive extraction, network, or uploaded-code execution is required. The first program checks:

- 435 direct bit-reversal cut ranks, using every cut for N=4,8,16,32,64 and 26 selected cuts at N=128, over GF(257), GF(12289), and GF(65537)
- All 3,136 critical N=8 submatrices per field, 9,408 total
- 288 independent random critical submatrices at N=16,32,64,128
- 336 full-coset decompositions and 336 consecutive-coset ranks
- 32,767 exact rational odd-cut algebra checks, and recurrence/profile/sum checks through N=32,768
- The preserved arbitrary-endpoint Vandermonde counterexample in all three fields

The second program independently recomputes 17,978 required N=8 submatrix ranks and enumerates all permutations for the exploratory-screen comparisons. These dense exact rank calculations are verification costs. The rank recurrence computes a supplied cut's rank in O(log N) arithmetic steps; it does not apply F_N to an input vector. Computing a full rank profile also incurs its output-size cost.

No stage coefficients, uniform arbitrary-input evaluator, or end-to-end charged operation count are supplied by this checkpoint. A large quasiseparable rank does not itself force a proportionate arithmetic application cost: structured matrices and even permutation matrices can have large cut ranks and still apply cheaply. Root preparation, exact coefficient representation, indexing, memory, and bit complexity remain separate obligations for any claimed transform speedup. General overlapping multi-stage constructions remain unresolved.
