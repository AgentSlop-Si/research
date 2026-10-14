# Arithmetic audit of signed-bank Fourier representations

14 October 2026. Status: **fresh exact candidate audit; no arithmetic-complexity breakthrough established**. This report derives evaluation algorithms and independently checks them. It does not change the accepted fixed-size bank-count theorem or claim a new lower bound.

## Result in brief

- One inverse branch is a linear-time cyclic bidiagonal solve. A bank contains up to N separately weighted branches, so literal evaluation costs O(N²) per bank, not O(N).
- Phase sharing does help: Fourier conjugation turns each bank into a diagonally scaled Toeplitz multiplication, with permutations and a separate zero-diagonal case. A sum of B banks representing the Fourier matrix can therefore be applied in O(B M_K(N)) field operations, assuming the usual regular polynomial-multiplication cost M_K.
- This does **not** beat the classical Fourier baseline: for odd N, the Fourier matrix itself is one diagonal–circulant–diagonal factorization. It needs one cyclic convolution and at most 2N scalar multiplications, already O(M_K(N)).
- The accepted N=11 cubic-field witness gives nine full Toeplitz and four triangular Toeplitz products by this route. It has not supplied a cheaper complete circuit than the one-convolution baseline, even before charging its extension-field arithmetic.
- Tensoring a fixed length-11 codelet gives N log N scaling, not a smaller exponent. The tensor-product transform and the cyclic length-11^k DFT are different targets.

## 1. Model and source binding

Let K contain a primitive N-th root q; therefore char(K) does not divide N. Set S e_t=e_(t+1), T e_t=q^t e_t, and F[k,t]=q^(-kt). Indices are cyclic. A bank is

    B = (1/N) sum_j w_j (I-alpha S^epsilon-beta q^(epsilon delta j) T^delta)^(-1),
    Delta = 1-alpha^N-beta^N != 0,  epsilon,delta in {+1,-1}.

We count arithmetic additions and scalar multiplications over the stated field. Permutations require data movement but no scalar arithmetic. All inversions below are of input-independent constants and belong to setup. Arbitrary input vectors are required; input sparsity is not assumed.

The N=11 certificate was read as inert JSON from the accepted review, retained byte-for-byte as `dependencies/RAW_CERTIFICATE.json`, SHA-256 `33d742797218c51381783b4128615e702280051f6bcd1ce47207fbbadf92c580`. Its field is F23[u]/(u³+13u²+13u+13), q=13. The accepted review and synthesis were read for scope; no historical program was run or imported.

Write M_K(n) for the arithmetic cost of multiplying two polynomials of degree less than n over K. Keep M_K explicit. O(N log N) requires an applicable multiplication/FFT model; merely possessing a primitive N-th root does not provide convenient smooth padding roots. Finite-field bit cost, extension construction, and complex numerical accuracy are separate charges.

## 2. Literal branch evaluation, including zero diagonals

Reindex coordinates by t=epsilon i. The j-th branch equations have the cyclic form

    d_i y_i-alpha y_(i-1)=x_i,
    d_i=1-beta q^(delta epsilon(i+j)).

If alpha != 0, use the backward recurrence

    y_(i-1)=r_i y_i+z_i,   r_i=d_i/alpha,   z_i=-x_i/alpha.

After one circuit, y_(N-1)=P y_(N-1)+h, where

    P=product_i r_i=(1-beta^N)/alpha^N,
    1-P=-Delta/alpha^N != 0.

Compute h in one pass, obtain y_(N-1)=h/(1-P), and reconstruct the other coordinates in a second pass. This takes O(N) operations, even when a d_i is zero. Dividing by d_i instead would fail in legal cases. If alpha=0, legality makes every diagonal d_i nonzero, so the solve is diagonal and also O(N).

If beta^N=1 and alpha!=0, exactly one d_i is zero. Its row fixes one output immediately, and only one recurrence pass is needed. This covers all branches of the accepted beta=1 witnesses.

For s nonzero raw phase weights, a literal bank costs O(sN); arbitrary dense weights have s up to N. Repeated banks with identical orientation/alpha/beta can first merge their weights, and identical branches can share solves. Different phase branches are shifted conjugates, but they receive shifted input vectors; this does not make their solves equal.

For the cubic N=11 witness, there are 139 nonzero weights among 143 phases. A simple beta=1 schedule first forms -x/alpha once per bank (11 multiplications), then performs at most 10 multiplications and 10 additions for each branch recurrence, and 11 multiplications and 11 additions for its weighted accumulation. Total upper budget:

    3,062 multiplications + 2,919 additions over F23³.

This is an explicit uncomplicated schedule, not a minimum. For comparison, ordinary dense multiplication by the same F11 needs at most 121 multiplications and 110 additions, and its coefficients are already in F23. More sophisticated Fourier codelets may do better still. Bank counting has hidden substantial work here.

Precomputing all bank matrices and adding them gives an N-by-N target matrix, then O(N²) online matrix-vector multiplication. That is a valid alternative upper bound, not a speed consequence of small bank count.

## 3. Shared-phase Toeplitz reduction

Let R0=(I-alpha S^epsilon-beta T^delta)^(-1). Then

    Rj=S^(-epsilon j) R0 S^(epsilon j),
    F S^epsilon F^-1=diag(q^(-epsilon k)),
    F T^delta F^-1=S^delta.

Consequently

    (F B F^-1)[k,l] = Rhat0[k,l] v[k-l],
    Rhat0=(diag(1-alpha q^(-epsilon k))-beta S^delta)^(-1),
    v[h]=(1/N) sum_j w_j q^(epsilon j h).

This uses a Hadamard/entrywise product, not ordinary matrix multiplication by v. The fixed weight transform v is setup and must be paid once. It can be computed by a classical chirp/polynomial-multiplication algorithm in O(M_K(N)), without invoking the proposed bank evaluator as an oracle.

Orient the cycle by k=delta r. Put d_r=1-alpha q^(-epsilon delta r), and psi[h]=v[delta h].

### Case A: beta != 0 and every d_r != 0

Define p_r=product_(i=0)^r(beta/d_i), and P=p_(N-1). Then

    Rhat0[r,s] = p_r / ((1-P) p_s d_s)              if r >= s,
               P p_r / ((1-P) p_s d_s)            if r < s.

Legality implies 1-P != 0. The weighted matrix is a diagonal–Toeplitz–diagonal product whose Toeplitz entries h_(r-s) are

    h_t=psi[t] for t>=0,
    h_t=P psi[N+t] for t<0.

Prefix products and diagonal factors cost O(N) setup operations, plus constant inversions.

### Case B: beta != 0 and some d_r=0

There is exactly one zero. Rotate the cycle to d_0=0; set p_0=1 and p_r=product_(i=1)^r(d_i/beta). Cyclically shift the input columns so column s' denotes original column (s'+1) mod N. In these coordinates the weighted inverse is upper triangular:

    entry[r,s'] = -p_(s')/(beta p_r) psi[r-s'-1]   if s'>=r,
                  0                              if s'<r.

Thus it is a diagonal–upper-triangular-Toeplitz–diagonal product with row/column permutations. No division by the zero d_0 occurs.

### Case C: beta=0

All phase inverses coincide. In Fourier coordinates the bank is diagonal with entries v[0]/d_r. In original coordinates it is one scalar multiple of a cyclic bidiagonal inverse and is linear-time applicable.

### Online and setup costs

A general bank alone can be evaluated by applying F, the relevant Toeplitz factors, and F^-1: O(C_F(N)+M_K(N)) online, or by O(sN) direct phases. Special cases such as bounded phase support, alpha=0, or beta=0 admit O(N) online evaluation after setup. No general linear-time evaluator for arbitrary weights is proved here, and no lower bound excluding one is asserted.

For a proved Fourier representation F=sum_l B_l, a useful algebraic cancellation removes online outer transforms:

    F = F F F^-1 = sum_l F B_l F^-1.

Therefore apply the transformed factors directly to the original input and sum. This is an identity between explicit matrices; it does not require computing Fx first. Setup still includes every weight transform and coefficient construction. Online cost is O(B M_K(N)+BN), setup O(B M_K(N)+BN) once weights are given, storage O(BN). Discovering the representation has a separate, potentially much larger cost.

More explicitly, the present witness gives nine full Toeplitz products, four triangular Toeplitz products, at most 286 diagonal scalar multiplications, and 132 output-summation additions. A full Toeplitz product reduces to one suitable polynomial product bounded by M_K(2N)+O(N); a triangular one to M_K(N)+O(N). This is an upper-bound implementation, not an optimized codelet or timing claim. Diagonal scalings generally differ between banks, so shared transformed inputs must be demonstrated rather than presumed.

## 4. The decisive existing Fourier baseline

For odd N, take h=2^(-1) mod N. Directly,

    q^(-kt) = q^(-h k²) q^(h(k-t)²) q^(-h t²).

Hence F=D C D, with D[k,k]=q^(-h k²) and C[k,t]=q^(h(k-t)²). C is circulant. The entire transform requires one fixed cyclic convolution and at most 2N diagonal multiplications. A polynomial product followed by reduction modulo x^N-1 supplies that convolution in M_K(N)+O(N) operations. This is the classical chirp-transform mechanism, not a new algorithmic discovery.

Thus reducing each bank to a convolution improves the literal O(BN²) bank evaluation, but does not improve the established O(M_K(N)) Fourier bound. Using B independent convolution calls only yields a weaker generic upper bound. Further cancellations or specially cheap kernels might yield a better concrete circuit, but no such complete circuit or matched benchmark is established by the bank minima.

Relevant primary literature:

- Rabiner, Schafer and Rader (1969), [The Chirp z-Transform Algorithm](https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/015_czt.pdf), develops transform evaluation through convolution. The original [Bell System paper](https://doi.org/10.1002/j.1538-7305.1969.tb04268.x) also states the convolution mechanism and arbitrary-length application.
- Bostan and Schost (2005), [Polynomial evaluation and interpolation on special sets of points](https://cs.uwaterloo.ca/~eschost/publications/BostanSchost.pdf), §5, the chirp-transform subsection of the author manuscript, gives the algebraic-field O(M(n)) chirp formulation. This is the closest direct complexity baseline here.
- Bostan, Jeannerod, Mouilleron and Schost (2017), [On matrices with displacement structure](https://cs.uwaterloo.ca/~eschost/publications/BoJeMoSc17.pdf), pp. 738–740, explicitly recalls O(alpha M(n)) Toeplitz/Hankel-like matrix-vector products from displacement generators. Pan's [Transformations of Matrix Structures Work Again II](https://arxiv.org/abs/1311.3729) treats transformations among Toeplitz, Hankel, Vandermonde and Cauchy structures. Our reduction is an elementary instance of this established structured-matrix approach; we have not found or claimed historical priority for this particular bank formula.

The bank sum should not automatically be called displacement-rank B under the ordinary shift operator: arbitrary differing diagonal factors can change that operator. The explicit sum of B diagonal-Toeplitz terms is sufficient for the stated cost; no extra displacement-rank claim is needed.

## 5. Field and preprocessing charges

The F11 target has coefficients in F23. A method using F23³ or F23⁵ must be charged against a base-field method on the same input/output problem. In a degree-d polynomial basis, addition costs d base-field additions. Multiplication by a precomputed extension constant is a d-by-d base-field linear map and admits at most d² multiplications and d(d-1) additions. Multiplication by a base-field constant costs only d scalar multiplications. Faster specialized circuits, Frobenius sharing, or Galois averaging may improve constants, but must be explicitly constructed and counted. Thirteen cubic-field banks versus fourteen base-field banks is not an arithmetic comparison.

For one input, include setup and representation construction unless a nonuniform/precomputed model is explicitly chosen. For R repeated inputs, report setup/R plus online cost. Neither Gaussian elimination used to discover weights nor weight DFTs become free because the resulting certificate is short. A fixed N=11 certificate says nothing by itself about uniform coefficient generation as N grows.

An NTT over finite fields is not automatically a complex DFT algorithm: there is no characteristic-preserving embedding of F23 into C. A characteristic-zero identity and its numerical precision/stability contract would need separate proof.

## 6. Tensoring the length-11 codelet

Let a11 and m11 be actual comparable-field counts for additions and scalar multiplications of a complete length-11 algorithm, after fixed setup. For N=11^k, applying F11 on each tensor axis computes the product-group transform F11^(tensor k), with

    A_k = k 11^(k-1) a11,
    M_k = k 11^(k-1) m11.

Equivalently T_k=11 T_(k-1)+11^(k-1)c11, where c11=a11+m11. This is exactly (c11/11) N log_11 N in this schedule. Replacing c11 can improve its leading constant if the full new codelet is cheaper under the same model; fixed radix cannot change its N log N exponent.

F11^(tensor k) is the Fourier transform of (Z/11Z)^k. It is not the cyclic length-11^k DFT. A standard radix-11 Cooley–Tukey schedule for the latter adds twiddle multiplications. Counting every nontrivial twiddle as one multiplication gives

    A_k = k 11^(k-1) a11,
    M_k = k 11^(k-1) m11 + (10k-11)11^(k-1)+1,

from M_k=11M_(k-1)+11^(k-1)m11+10(11^(k-1)-1). This is an exact count for that declared schedule, not an optimality claim. See the original [Cooley–Tukey paper](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Cooley65.pdf).

The cyclic transform also requires a primitive 11^k-th root. Since v_11(23^d-1)=1+v_11(d), this requires 11^(k-1) dividing d over F23. The fixed fields F23, F23³ and F23⁵ have no primitive 121st root. Keeping the cubic bank coefficients as well requires an extension degree divisible by 3*11^(k-1). Extension arithmetic cannot be ignored as k increases.

## 7. A falsifiable sub-N-log-N gate

Fix an infinite size family, a base-field input/output specification, and a setup-amortization model. Supply an explicit exact circuit and count A_N extension additions, U_N multiplications by base-field constants, V_N multiplications by genuinely extension-field constants, and P_N base-field setup operations. For degree d_N, a sufficient, checkable cost gate is

    [d_N A_N + d_N U_N + (2d_N²-d_N)V_N + P_N/R_N] / (N log N) -> 0.

Include input/output conversion and all accumulation in these counts. The displayed conversion uses a conservative fixed-constant multiplication circuit; an improved verified circuit can replace it. For a claim about one input, R_N=1. A claim with arbitrary precomputation must explicitly state that nonuniform model.

A simpler sufficient special case would be uniformly O(N)-applicable banks with B_N times their fully charged field-overhead equal to o(log N), plus sub-N-log-N setup per input. The current generic convolution evaluator does not meet this gate, and the N=11 bank count supplies neither such a family nor such a circuit. To claim a practical constant improvement instead, publish a complete same-field codelet and compare its full additions/multiplications or matched implementation against the chirp and relevant FFT codelets.

This is a positive test that a new algorithm could pass, not a claimed lower bound. [Morgenstern's 1973 bound](https://doi.org/10.1145/321752.321761) concerns bounded-coefficient complex linear algorithms; it must not be applied as an unconditional lower bound to unrestricted finite-field circuits.

## 8. Fresh verification and limits

Only `fresh_check.py`, written for this audit, was executed. It uses Python standard-library code and freshly implemented finite-field arithmetic/Gaussian elimination. It independently reconstructed all 143 original literal inverses, checked both inverse products, tested the backward solve against literal inversion, checked all thirteen transformed Toeplitz matrices, and verified both original and transformed sums against all 121 Fourier entries. There were 139 nonzero weights and four triangular cases.

Twenty-four additional generated N=5/F11 cases cover all sign orientations, alpha=0, beta=0, full-cycle and zero-diagonal factorizations. The classical chirp identity was checked entrywise for N=5,11,13, including N=13/F53/q=16. The radix-11 cost recurrence was checked through k=6. `RESULTS.json` records the outputs. Reproduce with `python3 -I fresh_check.py` from this directory or its workspace path.

These bounded exact checks support the formulas; the general derivations above supply their all-size justification. No asymptotic benchmark, numerical-stability test, exhaustive circuit optimization, novelty certification, or external publication was performed. No external service was written.
