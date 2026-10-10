# Conditional all-length extension of the packed dyadic Fourier executor

10 October 2026. Independently derived composition and fallback argument.

## Status and decision

The accepted interpolation compiler transfers the candidate packed dyadic bound with **one** backend call. It does not introduce a Taylor-rank multiplier. The resulting eventual bound for every supplied t=o(log N) is conditional only on the candidate dyadic backend's full computational and representation contract.

A stronger, uniform bound throughout 2<=t<=ceil(log2(N+1)) also follows conditionally, using the separately proved conventional all-length fallback in Section 4 below. That fallback is new in this note. It is not silently inherited from the accepted compiler, whose certified general fallback costs N^2 poly(log N+t).

This is a mathematical finite-word approximation construction. Neither exact arbitrary-complex arithmetic, production execution, practical crossover, nor historical novelty is claimed. Independent review of this new note and of the candidate backend is separate from the earlier acceptance.

## 1. Sources and exact conditional interface

The accepted canonical compiler is `FINAL_THEOREM_AND_PROOF.md`, SHA-256 `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`. Its Sections 2--5 and 9--11 were read directly. The accepted consolidation is `Q01_FINALIZATION.md` revision v3, SHA-256 `9ab67e663abe0cca45299dfecbca6c4852fbcd77e5c078a62292c2b8e3f2374b`. Its acceptance note has SHA-256 `be2ab749b57363972ac5d937b74ee62d7512cc08d2af0b0bedff779465ca29d0`.

**Hypothesis H (packed dyadic backend).** For every H=2^v and supplied integer 2<=T<=v+1, the candidate gives a deterministic all-input relative-l2 approximation to U_H with tolerance 2^-T, cold time O(H(T+log2(v+1))) and O(H) words on the stated address-capable integer RAM. Its input model permits O(c(v+1))-bit dyadics with polynomial dynamic range. Normalization, initial rounding, total response tables, coefficient certificates, bit reversal, every memory operation, output decoding, and fallback are charged.

The output representation is part of this hypothesis. For a normalized input whose maximum component magnitude is in [1/2,1), let

    p=T+10+ceil(log2(v+1)).

Its output states lie on 2^(-v-2p) Z[i], have O(v+p)-bit lattice numerators, and admit O(1)-word decoding. More generally exact power-of-two restoration only shifts the common exponent by the input-format O_c(v) amount. An error guarantee with unrestricted or inaccessible output representations would not suffice for the short exact interpolation sums.

The dyadic constructor's frozen draft explicitly provides this lattice contract and a scalar fallback: `DYADIC_PACKED_THEOREM.md`, SHA-256 `bb40decffd28b87a88065880363ff099b0d22071ef976bc67a8195c9b9db6d6f`. This proof needs only the stated domain: the low branch tests T<=v+1, and the all-length fallback covers failures.

## 2. The conditional theorem

Fix the input-format constant c. Let N>=2, n=ceil(log2(N+1)), and supply an integer 2<=t<=n. Each real/imaginary input component has O(cn) dyadic description bits and polynomial dynamic range, with shared or individual exponents as in the accepted theorem. Set epsilon=2^-t.

Assuming H, there is a uniform deterministic algorithm on a RAM of width w=C(c)n, for a sufficiently large fixed constant, that explicitly writes N finite dyadic mantissa/exponent outputs satisfying

    ||y-U_N x||_2 <= epsilon ||x||_2.

Its cold time and storage are, uniformly throughout that domain,

    O_c(N(t+log2(n+1))) work,       O_c(N) words.       (1)

The allowed operations are integer addition, subtraction, multiplication, division, comparison, shifts, Boolean operations and indexed memory access. Fixed-multiple-word online operands have fixed-operation cost; larger rational coefficient certification pays its actual multiword cost. All input scans, coefficient generation, memory, address arithmetic, conversions, normalization, and output are included. Zero input writes zero; N=1 is an exact copy.

For every supplied t=o(n), the interpolation branch is eventually selected and its preparation is o(N). Hence (1) is o(N log N). In particular:

- Fixed t gives O(N log log N).
- t=O(log n), including inverse-polylogarithmic accuracy, gives O(N log log N).
- t=ceil(n^beta), for fixed 0<beta<1, gives O(N n^beta).
- t=Theta(n) gives only O(N log N), with no strict asymptotic saving asserted.

Precision-target parsing and generation of t remain separately charged. A positive non-power-of-two dyadic tolerance may be rounded down to the next power of two. Computability alone is not an efficient input schedule.

Without using the newly proved fallback, the same substitution already yields the eventual t=o(n) bound in (1), while preserving the old N^2 poly(n+t) correctness fallback elsewhere. Thus the eventual improvement and the stronger uniform statement have distinct proof obligations.

## 3. Fully charged interpolation branch

### 3.1 Parameters and backend precision

Use exactly the accepted compiler:

    M=2^ceil(log2(4N)),        4N<=M<8N,
    v=log2 M,                v in {n+1,n+2},
    rho=epsilon/1024=2^-(t+10),
    T=t+10,
    s=t+16,                  h=16s+1,
    a=t+16+ceil(log2(h+2)),   eta=2^-a.

Normalize x once to a0=x/R, with 1/2<=||a0||_2<=sqrt(2N), and center-pad at signed indices j-floor((N-1)/2) modulo M. This is an exact isometric map Z. Its maximum component is still in [1/2,1), so the backend's normalization can use scale 1 and introduces no new representation issue.

The backend call is at precision **T=t+10**, not t. In particular a uniform extension cannot ignore the upper-domain check T<=v+1. The candidate's pointwise guarantee gives

    ||z_hat-U_M Z a0||_2 <=rho||a0||_2.

No assertion that the rounded backend is one linear matrix is made or needed.

### 3.2 Error proof

The accepted interpolation identity is U_N=D B U_M Z, with ||B||<3. Its certified implementation constructs B_tilde and E with

    ||B_tilde-B||<=2rho,    ||B_tilde||<3,
    ||E||<2,               ||E-D||<=3rho.

Therefore the exact dyadic prequantized output E B_tilde z_hat has error at most

    (6rho+4rho+9rho)||a0||_2 =19rho||a0||_2.

Its norm is below 2||a0||_2. The accepted output quantizer has unit roundoff <=rho, underflow <=rho/(8N), and an unreachable polynomial upper threshold. It adds at most 3rho||a0||_2. Exact restoration of R gives

    ||y-U_Nx||_2 <=22rho||x||_2 <epsilon||x||_2.         (2)

This uses a pointwise backend certificate and the actual supplied finite input. Initial backend rounding is already included in H. There is only one transform call.

### 3.3 Coefficients, sums, word sizes, and preparation

Each output interpolates 2h+2=O(t+1) distinct retained samples. Its indices are computed by exact integer products, division and modular wrap; no gather/scatter is free. The kernel table has

    (2h+2)2^a = O(2^t(t+1)^2)

entries. Each is certified using the accepted Dirichlet-kernel sine-ratio construction, with the exact zero-argument limit handled separately. Its rational arguments and necessary guard precision have O(n+t+log(t+1)) bits; each certificate uses poly(n+t) charged work and scratch. There is no enumeration of M Fourier coefficients or N separately expensive kernel evaluations.

The final phase grid has 2^(t+15) entries. The dyadic approximation to sqrt(M/N) and its certificate have poly(n+t) cost. A leading-bit/normalization table, if retained from the accepted compiler, costs N^(1/4)poly(n+t). Phase addressing costs O(1) per output. Thus a fixed computable preparation bound for the wrapper alone can be chosen as

    C [N^(1/4)+2^t(t+1)^2+1](n+t+1)^K.                (3)

Here C,K are fixed implementation constants dominating the elementary certification algorithms. This is a refinement of, and compatible with, the accepted aggregate N^(1/4)poly(n,p)+2^O(p)poly(n,p). The candidate backend pays its own complete cold preparation through H; the old unpacked FFT tables are not built again.

The backend's common output lattice is essential. Each short sum, followed by dyadic scale/phase multiplication, can be performed exactly with numerator length

    O_c(n+p+a+log(s+1))=O_c(n+t+log(n+1)).

This includes alignment and carries in the O(h)-term sum. It does not multiply the numerator length by h. Throughout t<=n a fixed number of C(c)n-bit words suffices. The certificates may use polynomially more bits but their actual cost appears in (3). All interpolation rows stream; an N-by-h matrix is never stored.

Conditional cold cost whenever the branch is selected is therefore

    O(N(t+log(n+1))+N(t+1)+Prep_wrapper),              (4)

where the first term includes the complete dyadic backend. Storage is O(N)+Prep_wrapper words, bounded by the explicit cap below.

### 3.4 Branch conditions and uniform low-precision analysis

Attempt this branch only if all of the following hold:

    t<=n/4;   T=t+10<=v+1;
    M>=16s;   2h+2<M.

Then run coefficient/normalization-table preparation with a literal N-instruction and N-word budget, counting its elementary RAM operations and rational scratch allocations. Check the allocation cap before writing a new slot. Abort and reuse its storage if either cap would be exceeded; select the fallback without using partial tables. Counters add constant-factor overhead. Table cardinalities can be tested with arithmetic saturated at N+1 before allocation. A failed attempt, its cleanup, and a successful attempt each cost O(N) work and use O(N) words. Thus no branch decision depends on an oracle for asymptotic notation or an uninstantiated polynomial constant in (3).

In the actual successful fast execution, this budgeted preparation builds the leading-bit table before the O(N) input normalization scan. A chunk table for floor(n/4)-bit chunks, with bounded-size direct handling at small n, resolves each O_c(n)-bit numerator in O_c(1) word operations. The normalization in Section 3.1 specifies the exact mathematical input to the transform; it does not authorize an earlier O(Nn) bit-scanning pass. If a guard or budget fails, only the scalar fallback may use that slower scan. Padding, exact input lattice alignment, and writing every output then take O(N) charged operations.

Uniformly for t<=n/4, (3) is at most C' N^(1/4)poly(n), since 2^n<2(N+1). Consequently there is an absolute finite threshold n0 after which the preparation cap, both stencil conditions, and the backend precision-domain condition all hold for every allowed t<=n/4. The cap then guarantees both (1)'s work bound and O(N) space. For every t=o(n), these conditions hold eventually and preparation is o(N).

When t>n/4, the fallback's O(Nn) cost is O(Nt). If t<=n/4 but a guard fails, n<n0, so the same fallback cost is O(N(t+log(n+1))) with a single constant depending on n0. These finitely bounded exceptions cannot be discarded without a fallback, but they can be absorbed after it has been fully charged. Section 4 supplies exactly that fallback.

## 4. New conventional all-length fallback

This section is a self-contained new lemma. It does not invoke an exact transcendental oracle, an unproved accurate chirp-spectrum routine, or the packed backend.

### 4.1 Fixed-lattice scalar dyadic FFT

Let H=2^v, k=v+1, and u=2^-q. Suppose 4ku<=1/2. Approximate every FFT twiddle and 1/sqrt(2) by dyadics with complex/absolute error <=u. At each normalized radix-2 butterfly, evaluate the dyadic arithmetic exactly and then truncate both output components toward zero onto u Z. Round the input onto the same lattice and use the standard bit-reversed DIT layout. The inverse uses conjugate phases.

The ideal butterfly is unitary. Replacing the twiddle and scale changes its 2-by-2 matrix in operator norm by at most 4u: the two first-column errors are <=u and the two second-column errors are <=2u, so its Frobenius error is <=sqrt(10)u<4u. A whole stage obeys the same bound. Its lattice rounding error is at most sqrt(2H)u.

If e_l is the cumulative distance from the ideal computation on input z, then e_0<=sqrt(2H)u and

    e_(l+1)<=(1+4u)e_l+4u||z||_2+sqrt(2H)u.

Since (1+4u)^v<2, summing gives the deliberately loose uniform bound

    ||FFT_q(z)-U_H z||_2
        <=16k u (||z||_2+sqrt(H)).                    (5)

The same holds for the inverse. Every stored stage value has magnitude bounded by its input norm plus the right side of (5). Inputs of polynomial magnitude therefore have only O(log H) integer bits, together with q fractional bits. No growing exact product of all stage coefficients is retained: each stage is explicitly rounded.

### 4.2 Fully charged phase construction

A full circle of any integer order L=O(N) can be generated with target coefficient error <=u. Certify its primitive phase with error <=2^-K, where

    K=q+ceil(log2 L)+10.

Starting at 1, repeatedly multiply by this dyadic seed and truncate components to 2^-K Z. If e_j is the phase error, then

    e_(j+1)<=(1+2^-K)e_j+(1+sqrt(2))2^-K,
    e_j<=6L2^-K<u/128,   0<=j<L.

The generated values have magnitude <2. Keep these guarded dyadics directly as coefficients; no rounding to the coarser u lattice is needed. Each exact product and truncation occupies O(q+log L) bits and constant many words in the domain below. The seed, 1/sqrt(2), and any scalar square root are certified using the accepted elementary rational interval construction, at poly(n+t) work and scratch. Generating the full arrays takes O(N) operations and words after those certificates.

### 4.3 Bluestein identity and computed quantities

Take H=nextpow2(2N-1). For N>=2, 2N<=H<4N and k=log2 H+1. For normalized a0=x/R, write A=||a0||_2, so 1/2<=A<=sqrt(H).

Let d_j=exp(-pi i j^2/N), let D=diag(d_j), and form b at residues j modulo H for -(N-1)<=j<=N-1 by b_j=exp(pi i j^2/N), zero elsewhere. These residues are distinct. Let J pad to H, P restrict to N, alpha=sqrt(H/N), and

    lambda=alpha U_H b,
    U_N a0=D P U_H^* diag(lambda) U_H J D a0.           (6)

In particular ||b||_2<=sqrt(H), alpha<2, and

    ||lambda||_infinity<=||lambda||_2<=sqrt(2H).

This crude bound is enough; no delicate exponential-sum estimate is assumed. The exact identity follows immediately by expanding circular convolution: d_k d_j exp(pi i(k-j)^2/N)=exp(-2pi i k j/N).

Build complete circles of orders H and 2N as in Section 4.2. The H circle supplies every FFT phase by a shift/multiply address, with conjugation for the inverse. The 2N circle supplies d_hat_j and b_hat_j through j^2 modulo 2N. All phase errors are <=u, and every phase address costs O(1) on O(n)-bit integers. Obtain alpha_hat with error <=u by a certified square-root enclosure.

Writing R_q for complex componentwise truncation to u Z, execute

    v_hat=R_q(J D_hat a0),
    z_hat=FFT_q(v_hat),
    c_hat=FFT_q(b_hat),
    lambda_hat=R_q(alpha_hat c_hat),
    w_hat=R_q(lambda_hat .* z_hat),
    f_hat=IFFT_q(w_hat),
    y_hat=R_q(D_hat P f_hat).

Here .* is coordinatewise multiplication. All arrays are explicit. These are three scalar radix-2 transforms, with O(N) extra arithmetic and three root/scale certificates of polynomial cost. The initial quantization inside (5) is allowed even when a vector was already rounded; rounding an existing u-lattice vector leaves it unchanged.

### 4.4 Explicit absolute error budget

Put z=U_H J D a0, c=U_H b, w=lambda .* z, and f=U_H^*w. Assume 500ku<=1, as guaranteed by the final choice below. Repeated use of (5), ||z||=A<=sqrt(H), and the preceding crude bounds gives:

    ||v_hat-J D a0|| <=3 sqrt(H)u,
    ||v_hat||<=5 sqrt(H),
    ||z_hat-z|| <=100k sqrt(H)u,      ||z_hat||<=2 sqrt(H),
    ||c_hat-c|| <=50k sqrt(H)u,       ||c_hat||<=2 sqrt(H),
    ||lambda_hat-lambda|| <=160k sqrt(H)u,
    ||lambda_hat||_infinity<=3 sqrt(H).

For clarity, the last error is bounded by 3 times the c error, plus u||c|| and sqrt(2H)u for scalar and rounding error. The norm bounds follow because 100ku, 160ku<=1.

The product error is at most

    3 sqrt(H) * 100k sqrt(H)u
      +160k sqrt(H)u * sqrt(H) +sqrt(2H)u
    <=500k H u.

Since ||w||<=sqrt(2H) A<2H, this gives ||w_hat||<=3H. The inverse transform adds at most 16ku(3H+sqrt(H)), so

    ||f_hat-f|| <=600k H u.

Finally ||D_hat||<=2 and, importantly, ||P f||=A by (6). Thus phase multiplication and final rounding yield

    ||y_hat-U_N a0||
      <=1200k H u+uA+sqrt(2N)u
      <=2048k H u.                                   (7)

Choose

    q=t+log2 H+ceil(log2 k)+13,

so u<=epsilon/(8192kH). All smallness conditions above hold. Equation (7) is at most epsilon/4<=epsilon A/2, since A>=1/2. Restore R exactly in the output exponent. This proves the requested all-input relative-l2 guarantee, with slack, independently of the packed hypothesis.

### 4.5 Fallback work, words, and arbitrary precision boundary

For 2<=t<=n, q and every guarded coefficient width are O(n); normalized input lattice alignment uses O_c(n) bits. Each butterfly, phase recurrence step, product, truncation, index, and output occupies a fixed number of C(c)n-bit words. Intermediate vector magnitudes are polynomial in N, as just proved. Input normalization can either use the charged leading-bit table or bit scans within the fallback's O(Nn) budget.

Total cold work and storage are

    O_c(Nn+poly(n+t)),       O_c(N)+poly(n+t) words.    (8)

Because t<=n and each fixed polynomial in n is O(2^n)=O(N), (8) is uniformly O_c(Nn) work and O_c(N) words, including all small sizes with one fixed constant. This is a formal RAM statement; no favorable practical constant is implied.

For arbitrary supplied t>=2, the same fallback remains valid with width w=C(c)(n+t+1), work (8), and O(N)+poly(n+t) words. Alternatively fixed-width multiword costs must be paid. This separate proposition does not smuggle arbitrary precision into (1)'s log-N-bit word contract.

## 5. What is preserved and what is new

The previously accepted theorem remains valid independently of H: its finite-word, all-length domain, error guarantee, and supplied t=o(n) bound

    O(Nn/log2(n/(t+log2 n)))

are not weakened or withdrawn by this candidate. Its explicit direct fallback and arbitrary-precision proposition also retain their established status.

New conditional conclusions are the improved bound (1) and its listed regimes. The accepted interpolation stability proof is reused at its exact scope. The packed runtime is a new backend hypothesis, not something proved by that stability argument. The uniform strengthened conclusion additionally uses the new, independently checkable fallback of Section 4.

This construction says nothing about exact arbitrary-complex Fourier computation or the exact Necklace--Green transport gate. It does not give per-coordinate relative error, correct rounding, exact norm preservation, a fixed binary64 runtime, a bit-complexity breakthrough, or publication priority.

No uploaded/source program was executed, imported, compiled, or parsed into an executable representation while deriving this note. No remote changes were made. Any separately recorded fresh controls are independently authored falsification checks and do not replace the analytic proof or certify a production eager-table executor.
