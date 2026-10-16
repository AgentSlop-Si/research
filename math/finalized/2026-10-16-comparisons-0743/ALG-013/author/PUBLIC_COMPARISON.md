# Binary-index rank-one Fourier evaluation: primary-source comparison

Date: 16 October 2026. Record: ALG-013.

## Outcome

The recorded comparison gate is satisfied by a **qualified interface nonmatch** to QTT–FFT, with an exact connection to classical radix-two decomposition. Binary-index rank-one data are an established tensor class. A compressed-output transform theorem does not, by itself, provide the raw-input certificate and fully charged explicit-output procedure considered here. Conversely, the linear explicit evaluator does not establish a polylogarithmic compressed transform or a general-input FFT improvement. Historical priority for the complete package remains unverified.

This is a comparison result. The previously accepted exact recognition/evaluation proof is retained, not counted as a new acceptance.

## 1. Research statement being compared

Let N=2^d, j=sum_(l=0)^(d-1) j_l 2^l, and

    x_j = c product_(l=0)^(d-1) a_l(j_l).

The input is the entire raw N-vector. For a nonzero input, choose a nonzero pivot p, set c=x_p, compute r_l=x_(p xor 2^l)/c with one paid inversion, and normalize a_l(p_l)=1 and a_l(1-p_l)=r_l. Regenerating all N entries and checking them against the original vector is mandatory. The all-zero input is separate. Over a field the pivot is invertible; over an odd residue ring the chosen pivot must be a unit. The supplied dyadic root must pass omega^(N/2)=-1 for N>1.

The generating polynomial and suffix evaluation are

    P(z) = c product_l (a_l(0)+a_l(1) z^(2^l)),
    M_l = 2^(d-l), S_d(0)=c,
    S_l(k) = (a_l(0)+a_l(1) omega^(k 2^l))
             S_(l+1)(k mod (M_l/2)),  0<=k<M_l.

Thus S_0(k)=sum_j x_j omega^(jk) gives every positive-exponent, unnormalized DFT output. There are 2N−2 suffix states. The domain has d+1 normalized parameters, with zero factors allowed, and is a proper restricted family.

## 2. Selected primary evaluation theorem

Dolgov–Khoromskij–Savostyanov, revised March 2012 preprint, Algorithm 2 and Theorem 3, Eq. (19), give a QTT-input/QTT-output transform with work bounded by sum_D O(D R_D^3), hence O(d^2 R^3). The rank bound concerns intermediate vectors, input and output; rank one at input alone does not establish R=1. Algorithm 2 uses TT rounding at a requested accuracy or rank limit. Theorem 2 bounds accumulated approximation error; Remark 2 says the result is exact when every truncation is exact. These are complex/unitary tensor-format statements, without the research statement's raw-vector certification or residue-ring guard ledger. [Primary preprint, §§4.2–4.3, printed pp. 12–15](https://webdoc.sub.gwdg.de/ebook/serien/e/MPI_Math_Nat/preprint2011_18.pdf). Published version: [DOI 10.1007/s00041-012-9227-4](https://doi.org/10.1007/s00041-012-9227-4).

### Exact rank-one specialization boundary

Savostyanov's Theorems 1–2 classify the nonzero binary-index rank-one inputs whose Fourier images are also rank one. Up to redistribution of scalar factors, for some h in {1,...,d} and integer j*, cores before h are coordinate deltas at selected bits, core h is arbitrary, and later cores are 2^(-1/2) exp(2 pi i j* k_p / 2^(d-p+1)). For this subclass, the Cooley–Tukey intermediate vectors remain rank one. Section 3 gives nonintegral-frequency exponential inputs with full QTT-rank Fourier images. The indices in Eq. (1) are least-significant-bit first, matching the research tensor indexing after p=l+1. [Primary preprint, Eq. (1), Theorems 1–2, §3](https://webdoc.sub.gwdg.de/ebook/serien/e/MPI_Math_Nat/preprint2011_45.pdf). Published version: [DOI 10.1016/j.laa.2011.11.008](https://doi.org/10.1016/j.laa.2011.11.008).

Our convention mapping is exact: if y is the negative-exponent unitary transform in those papers, the research output is sqrt(N) y((-k) mod N). Sign, scale and bit order must be mapped explicitly; they are not grounds for claiming different mathematics.

## 3. Formula-level connection to ordinary radix two

Cooley–Tukey's original paper decomposes a composite-length DFT into smaller transforms, with its complex positive-exponent convention stated in Eqs. (1)–(2). It does not state the present raw-input tensor certificate or its cold ledger. [Cooley–Tukey 1965, pp. 297–298](https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf).

The following is our direct specialization, not a claim that the 1965 paper explicitly gives the present package. Put

    t_q = c product_(l=1)^(d-1) a_l(q_(l-1)),
    x_(2q+b)=a_0(b)t_q,
    T_r=sum_q t_q (omega^2)^(rq).

Splitting the raw sum into even and odd indices yields

    X_k=(a_0(0)+a_0(1) omega^k) T_(k mod N/2).

Both child slices are scalar copies of one smaller tensor, so that smaller transform is evaluated once. Repeating the argument gives precisely the displayed suffix recurrence and T(N)=T(N/2)+O(N). This establishes the classical algebraic relationship without importing any compressed-output rank assumption. It does not settle the first historical appearance of this specialization together with the raw certificate.

Camps–Van Beeumen–Yang discuss rank growth when applying a QFT decomposition to rank-one tensors on a classical computer. Their §5.1 blocks the inference of automatic O(d^2) classical work through rank-preserving contractions. It is not an all-algorithm lower bound of Omega(N log N), and therefore does not contradict an O(N) explicit-output recurrence. [Primary preprint, §5.1, pp. 8–9](https://escholarship.org/content/qt9jf6s82b/qt9jf6s82b_noSplash_e94d15418d1b531eca1b9ac59a76097b.pdf).

## 4. Cold cost and input/output comparison

The retained nonzero accepted-input ledger for N>=2 is:

| Stage | Multiplications | Additions | Separately charged work |
|---|---:|---:|---|
| Recover normalized factors | d | 0 | One inverse, pivot/input scan and neighbor reads |
| Regenerate the raw tensor | N−1 | 0 | All N comparisons and coordinate accesses |
| Check supplied root | d−1 | 0 | Half-power equality check |
| Prepare root table | N−1 | 0 | N table entries |
| Evaluate suffix states | 4N−4 | 2N−2 | All N explicit outputs |
| Total | 6N−7+2d | 2N−2 | One inverse and O(N) word work/storage |

This count is inherited from the reviewed research statement, not newly attributed to QTT literature. N=1 and the zero path have separate linear-or-trivial handling. A rejected tensor still pays its raw checks; any general FFT fallback is additional external work.

To compare interfaces fairly:

- A supplied QTT representation does not certify that an arbitrary raw vector agrees with its cores. A deterministic exact certificate must account for the raw data it claims to certify.
- Returning QTT cores does not write N explicit values. Materializing every value costs at least N writes. A direct prefix-contraction expansion gives an O(N R^2) arithmetic upper bound for uniform TT rank at most R; for rank-one factors it is linear. This expansion estimate is our elementary accounting, not a bound quoted from the primary theorem.
- With R=1, adding fresh verification and explicit output makes the comparison linear overall. The rank-one-output hypothesis is nevertheless a strict restriction beyond the research statement's input promise.
- With arbitrary accepted rank-one inputs, a low rank bound for all Fourier intermediates/output is unavailable. A larger QTT upper bound is not a lower bound against a different evaluator.
- The research root table is cold preparation, not an amortized free table. Exact root/field discovery is outside the supplied-root model on both sides; comparisons cannot silently credit free roots to only one algorithm.
- The complex QR/SVD/rounding model in QTT work is not automatically a finite-field or odd-residue-ring algorithm. The unit-pivot and principal-root checks remain explicit independent conditions.
- Scalar counts are not bit counts or optimized runtime claims. With modulus bit width b, the retained conservative research bound is O(N b^2+b^3+N log N) bit work, with inversion and indices included.

## 5. Exact separating controls and older comparator leads

### Output rank is an extra condition

For x=(1,2,3,6), a_0=(1,2), a_1=(1,3), the positive DFT at omega=i is

    X=(12, -2-4i, -4, -2+4i).

The low-bit-first 2-by-2 unfolding has determinant X_0 X_3−X_1 X_2=−32+32i, nonzero. Thus input tensor rank one and full explicit suffix evaluation coexist with output QTT rank two. This finite, exact mathematical control tests the comparison boundary; it does not replay or replace the earlier proof acceptance.

### Prony, linear recurrences and rational generating functions

Massey treats shortest finite-sequence linear feedback shift registers over a field. His Eq. (2) tests the recurrence at every remaining index; Theorem 3 specifies when the shortest connection polynomial is unique. Section IV, Eqs. (16)–(18), connects the recurrence with a rational generating series whose numerator degree is below the register length. [Massey 1969, §§II–IV](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf).

Our model separation is decisive: e_(N−1) is an accepted rank-one binary tensor, obtained with every factor (0,1). Any homogeneous order-L recurrence with L<N sees only zeros when trying to produce the final 1, so its shortest finite LFSR length is N. Its finite generating polynomial is z^(N−1): denominator degree zero does not make the numerator short. Therefore a fixed low-order Prony/recurrence or bounded-total-degree rational interface does not follow from binary rank one. On an overlapping low-order subclass those tools may apply, but discovery, recurrence verification, coefficient/root recovery and full output must remain paid. No uniform low-order reduction is asserted.

### Sparse interpolation

Van der Hoeven–Lecerf study recovering a polynomial's monomial representation from a black box; their parameters include degree, term count and evaluation cost, and their introduction distinguishes field and bit models and warns about probabilistic/heuristic assumptions. [Primary final version, 2 May 2024, §1](https://www.texmacs.org/joris/ffsparse/ffsparse.html).

For our product P(z) over a field, a nonzero scale c and nonzero entries in all binary factors give N nonzero coefficients at distinct exponents 0,...,N−1. Thus its monomial term count is N, even though its factored description has O(d) parameters. This assertion is not transferred to zero divisors in residue rings. Treating the factor count as monomial sparsity would change the problem. Recovery from polynomial black-box evaluations also differs from verifying an already supplied raw coefficient vector.

### Pruned FFTs

The FFTW authors' pruned-FFT page gives O(N log K) arithmetic for K requested outputs, including a first-K construction when K divides N. [Official FFTW discussion](https://fftw.org/pruned.html).

The present evaluator requests K=N outputs, and its accepted family includes dense inputs with dense Fourier output, as the four-entry control shows. Hence sparse input/output pruning does not supply the same linear claim. The reuse is between scalar-related subproblems, rather than omission of unrequested coordinates.

These entries dispose of the older recorded comparator leads by explicit hypothesis and interface nonmatches. They are not silently removed and are not claimed to be impossible methods on their overlapping subfamilies.

## 6. Status and retained boundaries

The selected primary evaluation theorem, exact hypothesis/normalization mapping, classical recurrence relationship, cold ledger, and qualified nonmatches satisfy the recorded pass/stop condition. The bounded historical-comparison stage can be marked complete after independent review. This closes neither a worldwide-priority question nor an unrestricted Fourier theorem.

The recorded scope already says to keep numerical certification separate. The source labels the residual certificate optional and the stability discussion a theorem, not floating-point code. Its statement that floating residual certification requires paid outward rounding is retained as a conditional limitation; it is not a positive assignment to implement that optional path. Likewise, a paid external fallback is described as optional, rather than a missing promised implementation. The first-nonzero pivot still does not provide the maximum-magnitude pivot required by the separate complex stability argument. No numerical implementation, source-program replay, production benchmark, or unrestricted-input claim is added by this comparison. These retained limits are not newly invented exclusions.
