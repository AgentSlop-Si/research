# Fourier microkernels by locally normalized integer packing

10 October 2026. Independent derivation and exact arithmetic controls. Review status: dense and chirp proofs accepted by an independent project reviewer after the two literal repairs recorded below; exact controls are reported separately. This document supplies an alternative backend for the finite-word approximate theorem in `../algorithms/FINAL_THEOREM_AND_PROOF.md`. It does not assert novelty, bit-complexity improvement, or an exact arbitrary-complex FFT.

## 1. Contract and main conclusion

Let H=2^v>=2 (H=1 is an exact copy), let 0<delta<=1/4 be supplied as a precision exponent, and use the global normalization, floating quantizer, underflow threshold and exponent range of Section 1 of the cited theorem. In particular

- p=ceil(log2(1024(v+1)/delta)), u=2^(-p);
- e_min=-v-p, e_max=v+4, tau=2^(-v-p);
- the real floating states are zero or sign*(2^p+f)*2^(e-p), 0<=f<2^p and e_min<=e<=e_max;
- below upper clipping, q obeys ||q(z)-z||_2 <= u||z||_2+sqrt(2H)tau;
- every decoded global state lies on the lattice 2^(-v-2p) Z with an O(v+p)-bit numerator.

Use an address-capable word RAM with w=C(c)v bits, for a sufficiently large fixed input-format-dependent C(c). Integer addition, subtraction, multiplication, comparison, division, variable shifts, Boolean operations and indexed reads/writes cost one operation on w-bit operands and results that fit. A fixed number of words is simulated by a fixed number of such instructions. We never count an unbounded integer multiply as one instruction. The polynomial-bit certified coefficient preparation below is separately charged. The multiplication used for packing has its ENTIRE nonnegative product fitting in at most v/4 bits, so either a full-product instruction or an ordinary low-word product suffices, with no loss of high bits.

A scalar leading-bit table on ell=max(1,floor(v/4)) bits, prepared in O(2^ell) word operations and words, implements bit-length on every O(v+p)-bit online integer in O(1) operations when p=O(v). Inspect a constant number of chunks from most significant to least and consult the first nonzero chunk. The table is filled by L[0]=0 and L[k]=L[floor(k/2)]+1. This is not an input-vector response table; its cold cost remains explicitly present. If count-leading-zeros is explicitly available, omit this table. No undocumented free bit-scan operation is assumed.

For a power-of-two radix m>=2 define

  P=p+ceil(log2 m)+16, Q=2^P,
  D=2P+ceil(log2 m)+3.

Choose the largest power-of-two m satisfying

  (m^2+m)D <= v/4.                                      (A)

Every r-point normalized Fourier block, for powers of two r<=m, can be applied in O(r) word operations, using FOUR packed real integer products and no input-state response table. Its rounded stage obeys the same conservative bound as the old tabulator:

  ||computed(z)-U z||_2 <= 3u||z||_2+sqrt(2H)tau.          (B)

Consequently the old global error and first-overflow proofs apply unchanged. With guarded full-circle twiddle generation, the dyadic cold cost is

  O(H+Hv/log m+H^(1/4)+poly(v,p)),                        (C)

with O(H) words in every eventual saving regime. For p=o(v),

  m=Theta(sqrt(v/(p+log v))),
  log m=Theta(log(v/(p+log v))).                          (D)

The all-length interpolation construction therefore retains O(N log N/log log N) word work at fixed accuracy and at t=ceil((log N)^beta), 0<beta<1; it retains o(N log N) for every supplied t=o(log N). Its separate offset-coefficient table and O(Nt) interpolation work remain charged. Only the dyadic input-state response table has been removed.

A stronger classical Bluestein–Kronecker backend, proved in Section 8, replaces (A) by a linear-in-m packed-width condition and permits m=Theta(v/(p+log v)). It has the same asymptotic order in (C). Both forms are useful: the dense construction gives a particularly transparent exact packing control, while the chirp construction has a closer established antecedent and the better radix.

## 2. Normalize one block and quantify its loss

For a nonzero block z in C^r select a power of two R such that

  1/2 <= max_j max(|Re(z_j/R)|,|Im(z_j/R)|) < 1.

Then R<=2||z||_2. Scan the components, find a maximum absolute dyadic exactly, and find its leading bit as in Section 1. This costs O(r). Decode/compare on the global O(v+p)-bit lattice, so differing component exponents do not introduce unbounded alignment work. For a zero block, output r zeros directly.

Truncate every real and imaginary component of z/R toward zero on Q^(-1) Z; call the result x/Q, with integer complex vector x. Each real integer component lies in [-Q,Q] (in fact the strict magnitude bound gives [-Q+1,Q-1]). Put z_tilde=R x/Q. Truncation never increases a component magnitude, and

  ||z_tilde-z||_2 <= R sqrt(2r)/Q
                   <= 2sqrt(2r)/Q ||z||_2
                   < (u/1000)||z||_2.                  (E)

All shifts use a constant number of words. If the shift discards every bit, return zero directly rather than constructing a huge shift operand or intermediary.

## 3. Certified dyadic coefficient matrices

Prepare a complex integer matrix C_r whose entries have real and imaginary components in [-Q,Q], with A_r=C_r/Q and

  |(A_r-U_r)_(i,j)| <= 2sqrt(2)/Q.                      (F)

Exact componentwise truncation is one way to obtain a stronger bound, but is NOT required: a certified rational enclosure of width <=1/Q for each real component followed by a downward dyadic choice and clipping to [-1,1] gives (F) without deciding whether a transcendental lies exactly on a grid boundary. The same boundary-safe convention is used for all chirp coefficients below. The O(Q^(-1)) constants are deliberately loose.

The Frobenius bound gives

  ||A_r-U_r||_2 <= 2sqrt(2)r/Q < u/1000.                (G)

As ||z_tilde||<=||z||, (E) and (G) imply directly

  ||A_r z_tilde-U_r z||_2
      <= ||(A_r-U_r)z_tilde||+||U_r(z_tilde-z)||
      < (u/500)||z||_2.                               (H)

Certified coefficients are prepared by the elementary pi, sine/cosine and reciprocal-square-root interval algorithms already proved in Section 10 of the main theorem. Their cost per entry is poly(v,p); no transcendental oracle or N separately expensive coefficient calls is introduced. The dyadic endpoint convention above removes a potential exact-rounding undecidability/termination gap.

## 4. Exact signed real matrix-vector packing

This algebraic lemma is independent of Fourier analysis. Let C=(c_ij) and x=(x_j) be signed integer data of dimension r, with |c_ij|,|x_j|<=Q. Set B=2^D. Because r<=m and D=2P+ceil(log2 m)+3,

  4rQ^2 < B.

Bias each integer by Q and pack

  C_pack = sum_(i=0)^(r-1) sum_(j=0)^(r-1)
                       (c_ij+Q) B^(ir+j),
  x_pack = sum_(j=0)^(r-1) (x_j+Q) B^(r-1-j).

Their ordinary nonnegative integer product has polynomial coefficients

  s_k = sum_(ir+j+r-1-l=k) (c_ij+Q)(x_l+Q).

For each degree k, fixing l determines at most one matrix digit. Thus there are at most r summands, each at most 4Q^2, and every s_k<B. There are NO CARRIES at any digit, including unwanted intermediate digits. This is the needed all-digit argument; checking only desired dot-product digits would be insufficient.

The desired exponent k=(i+1)r-1 receives a term from row i' exactly when

  (i'-i)r + j-l = 0.

Since |j-l|<=r-1, this forces i'=i and j=l. Hence its extracted base-B digit is

  d_i = ((C_pack*x_pack) >> D*((i+1)r-1)) & (B-1)
      = sum_j(c_ij+Q)(x_j+Q).

No spacer digit between matrix rows is necessary. Intermediate convolution bands overlap, but they do not contaminate selected digits; the all-digit no-carry bound handles their overlap.

Store the SIGNED row sums s_i=sum_j c_ij during preparation and compute the SIGNED input sum S=sum_j x_j during gathering. Recover the exact signed dot product by

  y_i = d_i - Q s_i - Q S - rQ^2 = sum_j c_ij x_j.     (I)

Using biased sums in (I) would be wrong. Each correction and final row sum has O(P+log r) bits, where constants account for 2P as well. Negative outputs are ordinary signed integers; no signed base-B borrow convention is needed.

The largest possible product exponent is r^2+r-2. Therefore the FULL product is less than B^(r^2+r-1), and has at most (r^2+r-1)D bits. Condition (A) is a conservative upper bound. Both multiplicands, every requested shift count, and B-1 also fit the word contract. Building x_pack and S, making one multiply, and extracting/correcting all rows costs O(r), not O(1).

## 5. Complex arithmetic, preparation and storage

Write C=C_R+iC_I and x=x_R+ix_I. Form the four exact real matvec products

  a=C_R x_R, b=C_I x_I, c=C_R x_I, d=C_I x_R.

Then Cx=(a-b)+i(c+d). There are four packed multiplications. The two biased packed input words and their two signed sums are built once; the two biased packed coefficient words and their signed row sums are reusable. Per row there is constant extraction/correction and real/imaginary combination work. Restoring the scale R/Q^2 gives exactly A_r z_tilde, before the global quantizer. The complex integer numerator components have magnitude at most 2rQ^2, hence O(P+log r) bits.

There are O(log m) required powers-of-two block sizes. Total coefficient entries are sum_(r=1,2,...,m) r^2=O(m^2), so certified preparation and matrix packing cost poly(v,p). Store two packed words per r and 2r signed row sums; total storage is O(m+log m) words. The original scalar bit-length table contributes O(H^(1/4)) words and preparation. The H-entry guarded full-circle phase list adds O(H) words and work. Matrices may be discarded after packing apart from their row sums.

Online decoded global inputs and intermediate rescaled dyadics have O(v+p+P) bits. Multiplication changes a fixed constant in this bound, never the asymptotic word count. Global requantization discards low bits and restores the original global state range. Its zero, underflow and upper-clipping definitions remain the total ones in the main theorem; the packing backend is invoked only on represented reachable states, so it has no need to tabulate unreachable padded input keys.

## 6. Local-to-global stability and totality

Let w=A_r z_tilde. Equation (H) implies ||w||<=(1+u/500)||z||. Before clipping,

  ||q(w)-U_r z||
  <= ||q(w)-w||+||w-U_r z||
  <= (u(1+u/500)+u/500)||z|| +sqrt(2r)tau
  < 3u||z||+sqrt(2r)tau.

For disjoint blocks, apply the Euclidean triangle inequality to the vector of block-error norms. The relative pieces sum in squares and yield 3u||z||; the underflow pieces yield sqrt(2H)tau. Thus (B) is valid even though each block has its own R and the algorithm is nonlinear.

Twiddle stages obey the same (B) by the guarded full-circle construction in Section 11 of the main theorem. Include initial input quantization in the stage count L_0<=2v+1. The identical recurrence and first-overflow argument prove total relative error <delta. Before a hypothetical first saturation the norm remains below the old bound, and the new prequantized block has norm at most (1+u/500)||z||, so it cannot reach the old upper threshold 16H. Local normalization introduces no new saturation mode: |x_j|<=Q by construction, and all packed products are exactly bounded.

The uniform algorithm tests (A), the existing interpolation admissibility conditions and a known preparation cap, with the original certified direct DFT fallback if any fail. This maintains the precise finite-input/accuracy domain 2<=t<=ceil(log2(N+1)) and O(N)-word space. For each supplied t=o(log N), all fast conditions eventually hold. No useful growing radix is claimed for t=Theta(log N), and no polynomial-accuracy speedup is inferred.

## 7. Radix calculation and all-length consequence

With P=p+log2 m+16 for power-of-two m, D=Theta(p+log m+1). When p=o(v), a radix satisfying (A) tends to infinity. Its largest power-of-two choice satisfies

  m=Theta(sqrt(v/(p+log v))).

For the upper bound, if p>=log v then D>=2p and m=O(sqrt(v/p)); if p<log v, an admissible m cannot exceed O(sqrt(v/log v)) once m is at least v^(1/4), while smaller m already satisfies that bound for large v. For the lower bound, choose a sufficiently small constant multiple of sqrt(v/(p+log v)) and round down to a power of two; log m<=log v and (A) then holds. Rounding changes only constants. Thus log m=Theta(log(v/(p+log v))) throughout the eventual range v/(p+log v)->infinity.

Each macrolevel makes H/r calls on r-sized blocks plus O(H) twiddle/permutation work. Every call costs O(r), including movement and output. There are ceil(v/log2 m) macrolevels. Together with polynomial preparation, scalar leading-bit table and full-circle phase preparation this proves (C).

At arbitrary N use the existing centered padding M=Theta(N), stable interpolation and certified offset table unchanged. Writing n=ceil(log2(N+1)) and t=log2(1/epsilon), the complete cost is

  O(N + Nn/log m + Nt + N^(1/4) + poly(n,t)
       + 2^(O(t+log(t+2))) poly(n,t)),                 (J)

where the last term is the existing interpolation coefficient table and its certified preparation, not a dyadic input-response table. Equivalently one may retain the main theorem's more conservative 2^(O(p))poly(n,p) bound. Every preparation term is o(N) when t=o(n). For fixed t or t=ceil(n^beta), beta<1, (J) is O(Nn/log n). For every t=o(n), it is o(Nn). The original O(Nn/log(n/(t+log n))) simplified statement remains valid.

## 8. Stronger classical chirp-packed backend

This section is a fully specified optional replacement, not needed for the dense theorem. It uses classical Bluestein and Kronecker substitution, closely matching Harvey–van der Hoeven–Lecerf's established short-transform pipeline. There is no global chirp-spectrum preparation and no black-box approximate FFT inside this local convolution.

For r>=1 define d_j=exp(-pi i j^2/r) for 0<=j<r, b_k=exp(pi i k^2/r) for -(r-1)<=k<=r-1, and alpha=1/sqrt(r). The exact identity is

  (U_r z)_i = alpha d_i sum_(j=0)^(r-1) b_(i-j)d_j z_j.

Choose certified dyadic d_hat_j=D_j/Q and b_hat_k=K_k/Q, with every real numerator in [-Q,Q] and complex errors <=2sqrt(2)/Q. Choose alpha_hat=A/Q in [0,1] with |alpha_hat-alpha|<=2/Q. Take the same local input x/Q. These rational choices terminate using the certified enclosure rule in Section 3.

Let sigma=2sqrt(2)/Q. For Q>=16, every approximated phase has magnitude <=1+sigma<=1.18. A telescoping expansion gives

  |alpha_hat d_hat_i b_hat_(i-j) d_hat_j
       - alpha d_i b_(i-j) d_j|
  <= (2/Q)(1+sigma)^3
      + alpha sigma[(1+sigma)^2+(1+sigma)+1]
  < 16/Q.

Therefore the effective approximate matrix differs from U_r in spectral norm by at most 16r/Q <=u/4096. Combining with (E) gives local prequantization error below u/1000 and hence the same conservative stage bound (B).

Compute integer prechirped data a_j=D_j x_j EXACTLY. Its real/imaginary components lie in [-2Q^2,2Q^2]. Let V=2Q^2. For one real convolution, with |a_j|<=V and |k_l|<=Q for 0<=l<=2r-2 (k_l is the shifted b coefficient), set

  D_chirp=3P+ceil(log2 m)+4, B_chirp=2^(D_chirp),
  A_pack=sum_(j=0)^(r-1) (a_j+V) B_chirp^j,
  K_pack=sum_(l=0)^(2r-2) (k_l+Q) B_chirp^l.

Each ordinary product coefficient contains at most r summands, each at most (2V)(2Q)=8Q^3. Thus every coefficient is <B_chirp. The full product has degree at most 3r-3 and fits in (3r-2)D_chirp bits. Impose

  3m D_chirp <= v/4.                                  (K)

The extracted digit at i+r-1 contains exactly r terms, because 0<=i,j<r ensures 0<=i-j+r-1<=2r-2. Set S=sum_j a_j and T_i=sum_j k_(i-j+r-1). Recover

  c_i=digit_(i+r-1) - Q S - V T_i - rVQ
     =sum_j a_j k_(i-j+r-1).                           (L)

T_i is a precomputed signed length-r sliding sum of the kernel, obtainable for all i in O(r) with prefix sums. Four biased real packed products give the complex convolution. The two input sums are computed once, and the two lists of kernel-window sums are reused. Prechirp, packing, four products, extraction/correction, postchirp and normalization cost O(r) in total.

The integer complex convolution has denominator Q^3. Multiply by the integer postchirp D_i and integer scale A and restore R/Q^5. This is exactly alpha_hat d_hat_i sum_j b_hat_(i-j)d_hat_j z_tilde_j; there are no hidden arithmetic roundings. Intermediate complex numerators are bounded by a fixed constant times rQ^5 and have O(P+log r) bits. Coefficient preparation across powers-of-two sizes costs O(m) coefficients times poly(v,p), and storage for chirps and sliding sums is O(m) words. The packed kernels occupy O(log m) words.

The largest admissible power-of-two m under (K), with P=p+ceil(log2 m)+16, is

  m=Theta(v/(p+log v)),

by the same two-regime argument as Section 7. Its macrolevel and asymptotic time statements follow as before, with the improved radix. Dense and chirp backends may each use their own maximal admissible radix; do not apply (K) to the dense packed matrix.

## 9. Primary antecedents and novelty boundary

1. David Harvey, Joris van der Hoeven and Grégoire Lecerf, *Even faster integer multiplication*, 2015, §§2.5–2.6 and Proposition 4.1/§4. Their paper explicitly combines Cooley–Tukey short transforms, Bluestein conversion and Kronecker substitution, with finite-precision error analysis. This is a particularly direct antecedent to Section 8, not just a distant analogy. Their complexity objective is integer multiplication in a Turing bit model. The present note specializes an established mechanism to a unit-cost logarithmic-word contract and separately supplies local normwise quantization and the preexisting all-length interpolation interface. https://www.texmacs.org/joris/mul/mul.pdf
2. Martin Fürer, *How Fast Can We Multiply Large Integers?*, 2014, Definitions 1–2. The log-RAM explicitly charges O(log n)-bit integer multiplication/division as O(1), and forbids treating rapidly growing arbitrary integers as unit-cost scalars. This supports the need to state the machine model, not a priority claim about this Fourier bound. https://arxiv.org/pdf/1402.1811
3. The normalized Cooley–Tukey and Bluestein identities are classical. The cited Harvey–van der Hoeven–Lecerf paper provides primary proofs and cites their originals; no novelty is claimed for either factorization, no-carry Kronecker substitution, signed bias correction, or word-level parallelism.

The model-specialized complete theorem may already be an implicit or explicit corollary of prior work. An exhaustive model-matched literature comparison has not been completed. “New project derivation” must not be promoted to “new algorithm” or “first sub-N-log-N FFT.”

## 10. Verification plan and exact controls

The accompanying `fresh_packed_controls.py` is newly authored for this note and does not import, execute or parse supplied research programs. It checks exhaustive signed dense matvecs for small dimensions, worst-case carry budgets, randomized larger packed products, signed complex composition, local mixed-exponent normalization, zero/underflow/upper-clipping behavior, and the separate chirp-convolution extraction. High-precision Fourier comparisons are falsification controls, not certified coefficient generation or proof.

The next implementation check is a faithful bounded-word executor: enforce the actual packed product bit budget before multiplication; use the explicit scalar leading-bit table or a declared CLZ instruction; generate coefficients with rational interval certificates and boundary-safe dyadic choices; implement global q exactly; compare every output of small composed FFTs against an exact dyadic slow backend and verify normwise error against a certified interval Fourier reference. Count gathers, coefficient reads, all four packed multiplications, each correction, requantization, scatters, phase preparation and output writes. Run dense and chirp backends separately. This note is not a benchmark, verified production executor or practical crossover result.

## 11. Independent review

An independent project reviewer accepted the dense and chirp mathematical constructions, including all-digit carry bounds, digit isolation, signed corrections, full product widths, R/Q^5 chirp scaling, coefficient perturbation bound, nonlinear blockwise error composition and paid bit-scan table. Before acceptance the reviewer required two literal repairs, now applied: the packed product fits in **at most** v/4 bits, and H>=2 with H=1 handled by exact copy. This is internal mathematical review, not external peer review, production verification or novelty clearance.

## 12. Fresh control results

All newly authored controls passed: 15,650 exhaustive signed dense matvec cases; 690 exhaustive signed convolution cases; 576 randomized complex cases; 96 all-extreme cases; 12 total-quantizer boundary cases; and 252 high-precision local Fourier cases. Two deliberate negative controls (insufficient digit base and incorrect use of biased correction sums) were detected. Every convolution digit, including unselected overlapping bands, was compared with its exact integer coefficient.

At 120 decimal digits, the largest observed dense local error divided by u||z|| was 1.27748e-05, and the largest chirp ratio was 1.24349e-05. The largest rounded-stage error divided by the conservative stage budget was 0.21917 for dense and 0.264989 for chirp. These observations do not replace the proofs. Python exact integers validate the proved bit bounds but do not benchmark a physical fixed-word executor. No full production FFT executor or certified transcendental implementation was run.
