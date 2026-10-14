# Independent review: shared-phase signed-bank evaluator

Decision: **ACCEPT the evaluator as a conditional arithmetic upper bound. No arithmetic speedup or novelty conclusion follows.** The classical odd-length DFT already reduces to one cyclic convolution with linear extra work.

This review independently derives the formulas and uses fresh standalone code, rather than executing or importing the producer's checker. Scope is exact field arithmetic; it is not a numerical stability or benchmark result.

## Conventions and exact conjugation

Let K contain a primitive Nth root q, with char(K) not dividing N. Define S e_t=e_(t+1), T e_t=q^t e_t, and F[k,t]=q^(-kt), with indices modulo N. For epsilon,delta in {+1,-1}, a bank is

B=(1/N) sum_j w_j (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1).

Require Delta=1-alpha^N-beta^N != 0. Then

F S F^(-1)=T^(-1), F T F^(-1)=S,

and R_j=S^(-epsilon j) R_0 S^(epsilon j). Consequently H=F B F^(-1) has entries

H[k,l]=[(I-alpha T^(-epsilon)-beta S^delta)^(-1)]_[k,l] v[k-l],

where v[h]=(1/N) sum_j w_j q^(epsilon j h).

Put k=delta r, d_r=1-alpha q^(-epsilon delta r), and psi[h]=v[delta h]. These orientations, signs, and the 1/N normalization are essential.

## All denominator cases

If beta=0, H is diagonal, with H[k,k]=psi[0]/(1-alpha q^(-epsilon k)). Delta!=0 ensures no denominator vanishes.

If beta!=0 and every d_r is nonzero, put p_r=product_(i=0)^r(beta/d_i), P=p_(N-1). Then

H[delta r,delta s]=p_r t_(r-s)/((1-P)p_s d_s),

where t_u=psi[u] for u>=0 and t_u=P psi[N+u] for u<0. Thus H is a permutation of a diagonally scaled ordinary Toeplitz matrix. Here product_r d_r=1-alpha^N, so 1-P=Delta/(1-alpha^N) is nonzero.

If a d_r vanishes, exactly one does: q is primitive and epsilon delta is a unit modulo N. Rotate the cyclic order so d_0=0. Since Delta=-beta^N, beta is nonzero. Put p_0=1 and p_r=product_(i=1)^r(d_i/beta). After shifting the input column index from s to (s+1) modulo N, the matrix is

H[row r,column(s+1)] = -p_s psi[r-s-1]/(beta p_r) for r<=s,

and zero for r>s. This is diagonally scaled upper-triangular Toeplitz, with an explicit cyclic column permutation. No zero d_r is inverted. All psi indices remain cyclic. Rotating row and column coordinates together leaves their difference unchanged.

These derivations require neither an ordered field nor characteristic zero. In particular, characteristic 2 is legal for odd N.

## Why the outer transforms disappear, and what this does not prove

For a supplied exact bank certificate F=sum_b B_b, conjugating the equality by F gives

F=F F F^(-1)=sum_b F B_b F^(-1).

Therefore the sum of the explicit H_b factors evaluates F on the original input vector without an online outer Fourier transform or inverse transform. An isolated bank B still requires changing coordinates if evaluated by its H factor; the cancellation applies to the certified sum targeting F.

This is an algorithmic upper bound. It is not a lower bound requiring one convolution per bank, and it does not rule out further sharing or cancellation. A fixed N=11 certificate is also not a general-N family or a uniform certificate-construction algorithm.

## Paid setup, online cost, and noncircularity

Let M_K(N) denote a specified, independently available cost for polynomial multiplication over K; assume the usual M_K(cN)=O(M_K(N)) for fixed c. A full Toeplitz action is one ordinary polynomial product of lengths N and 2N-1, followed by extracting N coefficients. Triangular Toeplitz is a special case. Thus each bank costs O(M_K(N)+N) online, including input/output diagonal scalings. Summing r banks costs O(r M_K(N)+rN), with O(rN) stored factor data.

Each fixed weight transform psi is setup work. It costs O(M_K(N)+N) using the classical chirp reduction, or O(N^2) if computed directly. Scalar factors take O(N) further field operations; divisions may be charged directly or nonzero denominators batch-inverted with O(N) products and a constant number of inversions. Raw weights must not be silently treated as already transformed. Kernel transforms, when used by a chosen FFT-based convolution engine, are also paid setup and may then be amortized across input vectors. With all setup charged, r supplied banks still cost O(r M_K(N)+rN), excluding the independent cost of finding or certifying the bank decomposition.

No target-length Fourier-transform oracle may be used inside an allegedly new convolution algorithm. Our replay uses schoolbook ordinary polynomial products and folding/extraction, making this independence explicit. A known independent multiplication algorithm may replace schoolbook multiplication for the symbolic bound. Merely having a primitive Nth root does not ensure suitable padding roots or justify an unconditional O(N log N) bound in every field. Extension-field construction/arithmetic and fixed-kernel setup must be charged in whichever concrete model is claimed.

## Decisive classical baseline

For odd N, let h be the inverse of 2 in Z/NZ. This is an integer exponent, not inversion of 2 in K. The exact identity

q^(-kt)=q^(-h k^2) q^(h(k-t)^2) q^(-h t^2)

gives F=D C D, where D[t,t]=q^(-h t^2) and C is cyclic convolution by c_u=q^(h u^2). One cyclic convolution can be obtained from one ordinary product of two polynomials of degree less than N, followed by folding coefficients modulo X^N-1. Its online cost is M_K(N)+O(N), with at most 2N additional scalar multiplications and at most N-1 folding additions. The chirp sequences cost O(N) setup using multiplicative recurrences, plus O(log N) to obtain q^h if it is not already available. Fixed-kernel acceleration must be charged on the same basis as for banks.

Therefore 13 separate Toeplitz factors provide no asymptotic advantage over this existing one-convolution baseline under the same multiplication model. This comparison is not a measured constant-factor or lower-bound statement. Even lengths have a square-root-free linear-convolution chirp reduction using integer triangular numbers, so the broader classical O(M_K(N)) baseline is not confined to odd N.

Primary source independently checked: Bostan and Schost, *Polynomial evaluation and interpolation on special sets of points* (2005), Section 5, Proposition 5, https://mathexp.eu/bostan/publications/BoSc05.pdf . In that 32-page author copy, the relevant discussion is on printed pages 26–27 (PDF indices 25–26). It records the classical chirp evaluation reduction, credits Rabiner et al. and Bluestein, and states the general-field O(M(N)) evaluation bound. The displayed odd-N cyclic identity above is checked directly here; it is not claimed as a new result.

## Replay and scope

See RESULTS.json for the exact completed counts, check.py for the fresh replay, and MANIFEST.sha256 for hashes. Checks cover all matrix columns, both inverse products, both epsilon/delta signs, all zero-diagonal rotation positions, zero alpha/beta, odd composite N, characteristic-2 extensions, and all 13 supplied N=11 banks. Weight setup is independently compared with direct character sums. The literal bank sum and the transformed-factor sum are both compared with all 121 entries of F for the N=11 certificate. A wrong-chirp-sign negative control must fail.

The first harness attempt reached the N=11 input load and stopped because its scalar q was initially treated as a coefficient list. The loader was corrected to accept both representations before the full rerun. This was an input-adapter error, not a failed mathematical assertion. No historical executable was imported or run; no external writes were made.
