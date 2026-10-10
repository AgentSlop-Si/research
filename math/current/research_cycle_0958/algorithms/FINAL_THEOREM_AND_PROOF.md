# Deterministic normwise Fourier tabulation at every length

10 October 2026, second-pass corrected manuscript. Complete proof-level construction; production implementation and external priority remain unverified.

## Result and status

The original F132 construction survives its finite-word, deterministic, all-input relative-Euclidean contract. A new project-level derivation here removes its power-of-two restriction by composing it with a fully charged, stable, oversampled Fourier interpolation scheme. The usual black-box Bluestein shortcut does not prove this extension: a sharp example below identifies a square-root-of-length error amplification in preparing the chirp multiplier from an l2-only FFT guarantee.

The ingredients are classical: Cooley–Tukey factorization, finite-state/Four-Russians tabulation, floating quantization, oversampled Fourier interpolation and Schur norm bounds. This document establishes a precise combined upper bound and closes a project gap. It does not establish worldwide priority, a new exact-complex arithmetic FFT, a bit-complexity breakthrough, or a practical implementation.

### Theorem 1: precise uniform domain and asymptotic all-length corollaries

Fix the input-format constant c. Let N>=2, n=ceil(log2(N+1)), and let an integer precision exponent t with 2<=t<=n be supplied. Put epsilon=2^{-t}. Every real and imaginary input component is a dyadic of O(c n) description bits and polynomial dynamic range. For example, x_j=(a_j+i b_j)2^{-B}, |a_j|,|b_j|<=N^c and |B|<=c n; separate exponents with absolute value at most c n are also allowed.

On an address-capable word RAM of word width w=C(c)n, with a sufficiently large fixed C(c), there is one uniform deterministic algorithm that explicitly writes a finite dyadic mantissa/exponent representation of all N entries of y satisfying

  ||y-U_N x||_2 <= 2^{-t} ||x||_2,
  (U_N)_{k,j}=N^{-1/2} exp(-2 pi i k j/N).

The instruction set consists of integer addition, subtraction, multiplication, division, comparisons, shifts, Boolean operations and random access. All actual integer operands have a fixed multiple of w bits in online execution, simulated by a fixed number of instructions; polynomial-bit rational work in coefficient preparation is charged separately. Memory, tables, addresses, scans, normalization, gathering, packing, scattering and every output write are charged. Space is O(N) words throughout the specified domain. N=1 is an exact copy.

The fast branch is the algorithm proved below. It is used only when m>=2, the interpolation stencil fits without duplicate indices, and a certified upper bound on total preparation work/space is at most N. This bound is a fixed computable polynomial times the explicitly displayed table cardinalities. Otherwise use the direct certified fallback in Section 9. The fallback keeps the algorithm total without declaring a useful radix or sublinear table at sizes where those claims are false.

For every supplied schedule t=t_N=o(n), these fast-branch conditions eventually hold. In particular:

* For each fixed epsilon>0, use the fixed exponent t=ceil(log2(1/epsilon)); at all sufficiently large lengths the cold running time is O_epsilon(N log N/log log N).
* For t=ceil(n^beta), where 0<beta<1 is fixed, it is O_beta(N log N/log log N).
* For every supplied t=o(n), it is o(N log N). More precisely, with b=Theta(t+log n), it is

    O(N n / log(n/(t+log n))).

The denominator in this last formula is used only in its eventual range n/(t+log n)->infinity. The less simplified bound (14), with every preparation term, is valid whenever the fast branch is selected.

These are uniform all-integer-length asymptotic bounds, with no divisibility or favorable-subsequence hypothesis. The finite t<=n domain makes the fixed word-width statement literal. Fixed epsilon at finitely many smaller lengths, or arbitrary precision outside this domain, is handled by the separate high-precision fallback proposition in Section 9; its larger representation costs are not hidden in the fast theorem.

A non-power-of-two positive dyadic accuracy target is reduced to 2^{-ceil(log2(1/epsilon))}, which is between epsilon/2 and epsilon. Reading/parsing the target and producing t are separately charged. Merely specifying a computable real beta or a computable precision schedule is not a cost bound; the integer exponent must be supplied or generated within a stated charged cost.

No polynomial-accuracy sub-N-log-N conclusion is claimed. The complete executor is a mathematical construction, not a verified production implementation or practical crossover claim. External novelty remains unresolved.

## 1. The dyadic primitive, with all charges

This section restates the original F132 argument in a self-contained form. Let H=2^v be a power of two and let 0<delta<=1/4.

### 1.1 Normalize and quantize

If the input is zero, output H zeros. Otherwise select a power of two R so that the largest real or imaginary component of a=x/R lies in [1/2,1). Then

  1/2 <= ||a||_2 <= sqrt(2H).

The scan, alignment and power-of-two scaling take O(H) word operations. Leading-bit discovery can use a completely enumerated table on chunks of at most v/4 bits, with H^{1/4}poly(v) preparation. It need not be assumed as a free instruction.

Set

  p=ceil(log2(1024(v+1)/delta)), u=2^{-p},
  e_min=floor(log2(delta/[1024(v+1)]))-v,
  e_max=v+4, tau=2^{e_min}.

A nonzero real state is sign*(2^p+f)*2^{e-p}, with 0<=f<2^p and e_min<=e<=e_max. For an explicit total encoding, let E=e_max-e_min+1 and k=ceil(log2(E+1)). An exponent field of k bits uses values 1,...,E for the valid exponents, and 0 for zero; every larger padded exponent value also decodes to zero, regardless of its sign and fraction fields. Encode zero canonically with all fields zero. Thus no valid finite state is sacrificed to reserve zero, even when E is a power of two. One complex state occupies

  b=2[p+ceil(log2(e_max-e_min+2))+1]=O(p+log v)

bits. The real quantizer truncates toward zero, sends magnitudes below tau to zero, and maps any magnitude at least 2^{e_max+1} to the signed largest finite value (2-2^{-p})2^{e_max}. Values below that threshold are handled by ordinary mantissa truncation. This defines the quantizer on every rational table input, including unreachable inputs whose block outputs overflow. Upper clipping is not claimed to satisfy the error inequality; the reachable execution is proved never to use it. Before any upper clipping,

  ||q(z)-z||_2 <= u||z||_2+sqrt(2H)tau.                 (1)

The identity e_min=-v-p follows directly from floor(-a)=-ceil(a). Thus a decoded state is an integer multiple of 2^{-v-2p}, and its lattice numerator has at most 2v+2p+O(1) bits. All decoded states lie on one dyadic lattice. If p=o(v), exact products and poly(v)-length dot products of these states and O(p+log v)-bit dyadic coefficients have O(v+p) bits. A fixed number of sufficiently wide words therefore suffices online. Polynomial-bit rational work during preparation is charged separately.

### 1.2 Enumerate every block response

Choose the largest power-of-two radix m with mb<=v/4. For every power-of-two r<=m, prepare a dyadic matrix A_r whose entries differ from U_r by at most u/(8r). Consequently ||A_r-U_r||_2<=u/8, by the Frobenius norm bound.

For each of the 2^{br} padded state keys, decode all r components, compute A_r z exactly in fixed-point arithmetic, apply the total underflow/truncation/clipping quantizer, and pack the r resulting codes. This defines every table entry, including invalid keys and unreachable valid keys whose outputs require clipping. The flag is not needed in the table payload; it is a proof classification. All payloads have exactly br bits, with br<=v/4. Its preparation is bounded by

  H^{1/4}poly(v,p),

and its space by the same bound. Gathering r inputs, packing their key, looking up the response, unpacking and scattering take O(r), not O(1). An output vector is never treated as a free scalar.

A nonoverflowing block stage obeys

  ||computed(z)-U z||_2 <=3u||z||_2+sqrt(2H)tau,        (2)

also when independent blocks act on the whole vector.

### 1.3 Prepare phases without a long drifting recurrence

Prepare all 2^{p+8} points of a coarse phase grid, each to complex error at most 3*2^{-(p+10)}. A requested phase exp(-2 pi i j/L) uses its nearest grid index, computed by exact integer division. The combined phase approximation error is below u/8. Rounded multiplication then obeys (2).

The complete grid costs 2^p poly(v,p) preparation. One uniform coefficient construction uses a rational interval for pi from Machin's arctangent identity, Taylor intervals for sine/cosine on a bounded reduced argument, and integer square roots for dyadic enclosures of 1/sqrt(r). Elementary polynomial-time integer arithmetic suffices; no exact transcendental oracle or fast multiplication theorem is assumed.

### 1.4 Compose unitary stages

For L=rs the classical normalized Cooley–Tukey identity is

  y_a[k]=s^{-1/2} sum_j x[a+rj] exp(-2 pi i kj/s),
  (U_L x)[k+st]=r^{-1/2} sum_a y_a[k]
                  exp(-2 pi i ak/L) exp(-2 pi i at/r).

Use radix m repeatedly, and the corresponding smaller table at the last level. Every stage is a permutation, a diagonal unitary target, or a direct sum of normalized Fourier blocks. The number of macrolevels is ceil(v/log2 m), with O(H) work per macrolevel.

An intentionally generous count of at most L_0=2v+1 rounded unitary stages, explicitly including the initial input quantization as a rounded identity stage, avoids circular precision selection. If e_j is the cumulative error from the ideal unitary program, (2) implies

  e_{j+1}<=(1+3u)e_j+3u||a||_2+sqrt(2H)tau.

Therefore

  e_{L_0}/||a||_2 <=6uL_0+4L_0 sqrt(2H)tau
                   <=6uL_0+8L_0 H tau <delta.           (3)

Here (1+3u)^{L_0}<=2 and ||a||_2>=1/2 were used. A first-overflow argument makes the reasoning noncircular: before the hypothetical first saturation, (3) bounds every stored vector norm by (1+delta)sqrt(2H); a prequantized block can enlarge it by only 1+u/8. This is far below the upper magnitude threshold 16H. Thus the first saturation cannot occur.

Restore R exactly in each output's exponent. The cold running time and storage are

  O(H+Hv/log m+H^{1/4}poly(v,p)+2^p poly(v,p)),
  O(H) words.

For fixed delta, b=Theta(log v), m=Theta(v/log v), and log m=Theta(log v). For t=log2(1/delta)=Theta(v^beta), 0<beta<1, b=Theta(v^beta) and log m=Theta((1-beta)log v). If p=o(v), m tends to infinity and preparation is o(H). At other parameter pairs the algorithm does not pretend that this radix exists: the explicit branch test and fallback in Section 9 apply.

## 2. A stable arbitrary-length interpolation lemma

Let N>=2, M=2^{ceil(log2(4N))}, so 4N<=M<8N. Set c=floor((N-1)/2). Embed a_j at signed index j-c modulo M, obtaining v. The occupied band obeys |j-c|<=N/2<=M/8. Define

  f(t)=sum_{j=0}^{N-1} a_j exp(-2 pi i(j-c)t),
  z=U_M v, so z_k=f(k/M)/sqrt(M).

Let s>=2 be an integer. For now suppose M>=16s and that the neighborhood below has fewer than M entries. Put L=M/4 and q=floor(M/(8s)). Let mu_q be the uniform probability measure on the integer interval [-q,q], and set

  g=1_{[-L,L]} * mu_q^{*s},
  D_a(t)=sum_{j=-a}^{a} exp(-2 pi ijt),
  K(t)=D_L(t)/M * [D_q(t)/(2q+1)]^s.                    (4)

Convolution here is on the integers, not modulo M. It gives

  0<=g_j<=1,
  g_j=1 if |j|<=L-sq, in particular if |j|<=M/8,
  g_j=0 if |j|>L+sq<=3M/8,
  K(t)=M^{-1} sum_j g_j exp(-2 pi ijt).

The support is strictly within one length-M frequency interval. Discrete orthogonality yields the exact identity

  (U_N a)_ell=d_ell sqrt(M/N) sum_{k=0}^{M-1}
                         K(ell/N-k/M)z_k,
  d_ell=exp(-2 pi i c ell/N).                            (5)

No approximation has yet occurred.

### 2.1 The full interpolation operator is bounded on arbitrary errors

Write B_{ell,k}=sqrt(M/N)K(ell/N-k/M), and D=diag(d_ell). In Fourier coordinates, B maps a vector of M Fourier coefficients to its sums over residue classes modulo N, weighted by g_j, followed by the unitary N-point DFT. Every residue class in the signed M-point frequency interval contains at most ceil(M/N)<=8 entries. Cauchy–Schwarz, g_j<=1 and disjoint residue classes imply

  ||B||_2<=sqrt(8)<3.                                   (6)

This holds for all z in C^M. It therefore controls arbitrary normwise FFT error, rather than only exactly bandlimited data. More precisely, ||B||_2^2=max_r sum_{j≡r (mod N)}g_j^2.

### 2.2 Local truncation has dimension-free spectral error

Let d=M*dist(t,Z), with 0<d<=M/2. The identity for a Dirichlet kernel and the bound |sin(pi t)|>=2 dist(t,Z), together with q>=M/(16s), give

  |K(t)| <= (1/(2d)) min(1,4s/d)^s.                     (7)

Also |K(t)|<=1 everywhere. At t=0 its exact value is (2L+1)/M; it is not generally 1.

Set h=16s+1. For each ell define

  r_ell=floor(ell M/N), theta_ell=ell M/N-r_ell,

and retain only k=(r_ell+j) mod M with j=-h,...,h+1. Assume 2h+2<M, so there are no duplicate retained indices. Call the resulting sparse matrix B_h. Every omitted circular distance is at least 16s. The source grid has separation 1; the target grid ell M/N has circular separation M/N>=4. For either grid, at most four points lie in any shell r<=distance<r+1. Thus each unnormalized row and column tail is bounded by

  4 sum_{r>=16s} (4s)^s/(2 r^{s+1}) <=4*4^{-s}.

The last inequality follows by bounding the series by its first term plus the integral from 16s to infinity; s>=2 provides ample slack. Multiplying by sqrt(M/N)<3 and using the Schur inequality ||E||_2<=sqrt(||E||_1||E||_infinity) gives

  ||B-B_h||_2<=12*4^{-s}.                               (8)

This is the key improvement over an entrywise error estimate followed by a sqrt(N) conversion. Periodic wrap is already included in the distance and retained-index definitions.

## 3. Uniform finite coefficient preparation

Fix 0<epsilon<=1/4 and define

  rho=epsilon/1024,
  s=ceil(log2(2^{16}/epsilon)), h=16s+1,
  a=ceil(log2(2^{16}(h+2)/epsilon)), eta=2^{-a}.

For the finitely many sizes in each stated asymptotic regime that fail M>=16s or 2h+2<M, use a direct certified finite-precision DFT (or ordinary FFT/Bluestein). Such a fallback is finite and deterministic; it makes no sub-N-log-N claim at those sizes. The main construction applies eventually whenever log(1/epsilon)=o(log N).

### 3.1 Fractional-offset kernel table

The exact Fourier representation in (4) shows

  |(d/dtheta)K((theta-j)/M)|
    <=(2 pi/M^2) sum_{|b|<=3M/8}|b|g_b <=4.             (9)

Round theta_ell downward to theta'=eta floor(theta_ell/eta). For every grid offset theta'=0,eta,...,1-eta and every j=-h,...,h+1, prepare a dyadic coefficient k_hat(theta',j) within eta of K((theta'-j)/M). Each retained entry changes by at most 5eta before the factor sqrt(M/N).

Each row has 2h+2 nonzero entries. Since target centers are separated by at least 4 and all retained points are within distance h+1, each column has at most 2h+4 nonzero entries. Hence another Schur estimate gives

  ||B_h-B_tilde||_2<=15(2h+4)eta<=rho,                  (10)

where B_tilde uses the rounded table but the exact factor sqrt(M/N). Equation (8) is also at most rho under the selected s. Therefore

  ||B_tilde-B||_2<=2rho, ||B_tilde||_2<3.              (11)

The kernel table has O(h 2^a) entries. The parameters are integers produced by shifts and leading-bit operations, or supplied precision exponents; neither computing a logarithm as a transcendental nor solving an unbounded precision-scheduling problem is needed.

Evaluate (4) through

  D_L(t)=sin((2L+1)pi t)/sin(pi t),
  D_q(t)/(2q+1)=sin((2q+1)pi t)/[(2q+1)sin(pi t)].

The only exact zero denominator in the retained grid domain is t=0, whose limiting value was given above. Every other grid argument has distance from zero at least eta/M. For example, Q=8(n+a+ceil(log2(s+1))+16) guard bits are more than sufficient to certify each normalized sine ratio to eta/[64(s+1)], after exact argument reduction. A detailed justification is in Section 10. Each normalized factor has magnitude at most 1, so the s-fold product loses only an O(s) error factor. Elementary rational interval algorithms run in poly(n,a,s) bit or word operations per entry. The Fourier coefficients g_j need not be enumerated. This explains both the uniformity and the absence of N separately expensive transcendental evaluations.

### 3.2 Scale and final phases

Prepare one dyadic alpha_hat with

  |alpha_hat/sqrt(M/N)-1|<=rho.

A certified integer-square-root interval requires polynomial(n+log(1/epsilon)) work. Prepare a complete coarse phase grid of size G=2^{ceil(log2(32/rho))}, with each entry within rho/4 of its exact unit-circle point. To obtain d_hat_ell, round (c ell mod N)G/N to the nearest integer. The angular rounding error is at most pi/G<rho/8; thus |d_hat_ell-d_ell|<=rho. Only the coarse grid is prepared, not N separate transcendental calls. Phase addresses require O(1) word arithmetic per output.

Let E=(alpha_hat/sqrt(M/N))*diag(d_hat_ell). Then

  ||E||_2<2, ||E-D||_2<=3rho.                          (12)

### 3.3 Exact online short sums and final quantization

All kernel, scale and phase approximations are dyadics. Align the dyadic FFT outputs to a fixed lattice and evaluate each retained O(h)-term dot product exactly, followed by exact dyadic scale and phase multiplication. The numerator bit length is

  O(n+p+a+log(s+1)),

where p=O(log n+log(1/epsilon)) is the dyadic primitive's mantissa parameter. Because p,a=o(n) and log(s+1)=o(n) in the general regime, a fixed number of sufficiently large Theta(n)-bit words suffices. This counts every multiply, addition and alignment; it is not an arbitrary-precision scalar oracle. Preparation may use polynomially many words, included in its sublinear bounds.

Finally truncate to an output floating alphabet with unit roundoff u_out<=rho, underflow threshold tau_out<=rho/(8N), and a sufficiently large polynomial upper exponent. The same first-overflow principle applies: the proved prequantization norm below is less than 2||a||_2<=2sqrt(2N), so an upper threshold such as 16M is unreachable. Final quantization obeys (1), now in dimension N.

## 4. Complete error budget

Normalize x once as in Section 1, using N in the scan. Its centered padded vector v has ||v||_2=||a||_2. Invoke the dyadic primitive at length M with relative accuracy delta=rho, giving

  ||z_hat-z||_2<=rho||a||_2.

Before final rounding the computed vector is E B_tilde z_hat. By (5), the target is D B z=U_N a. Equations (6), (11) and (12) imply

  ||E B_tilde z_hat-D B z||_2
  <=||E|| ||B_tilde|| ||z_hat-z||
     +||E|| ||B_tilde-B|| ||z||
     +||E-D|| ||B|| ||z||
  <=(6rho+4rho+9rho)||a||_2
  =19rho||a||_2.                                      (13)

In particular the prequantization vector has norm <2||a||_2. Since ||a||_2>=1/2 and N>=2, final rounding adds at most

  rho*2||a||_2+sqrt(2N)rho/(8N) <=3rho||a||_2.

The total is at most 22rho||a||_2<epsilon||a||_2. Restoring R in every output exponent proves Theorem 1. N=1 is an exact copy. All bounds are deterministic and uniform over every represented input.

## 5. Cost, space and precision boundary

Let n=ceil(log2(N+1)), t=ceil(log2(1/epsilon)), and p=O(log n+t). Applying Section 1 with H=M=Theta(N) and delta=rho uses b=O(p+log n) bits per complex state and radix m=Theta(n/b), rounded down to a power of two. The additional interpolation work is O(Nh)=O(N(1+t)). Complete preparation costs

  N^{1/4}poly(n,p)+2^{O(p)}poly(n,p).

Thus, for the main asymptotic range,

  T(N,epsilon)=O(N+N n/log m+N t
                  +N^{1/4}poly(n,p)+2^{O(p)}poly(n,p)). (14)

Both preparation terms are o(N) if p=o(n). The input, dyadic FFT working arrays, sparse interpolation working state and explicit output require O(N) words; all prepared tables occupy o(N) words in the saving regimes. A depth-first implementation reuses each child buffer after scattering its result, so simultaneously retained recursion buffers form a geometric series, rather than one fresh N-array per depth. The explicit preparation-cap check preserves the O(N)-space contract at every other allowed parameter pair. Interpolation can stream its short rows and does not store an N-by-h matrix.

For fixed epsilon, log m=Theta(log n), proving O_epsilon(Nn/log n). For t=ceil(n^beta), 0<beta<1, log m=Theta((1-beta)log n), and Nt=o(Nn/log n). For any supplied t=o(n), both Nn/log m and Nt are o(Nn). Also Nt=O(Nn/log m): put y=n/(t+log n), use m=Theta(y), and note log y=O(y). This proves the simplified general schedule bound in Theorem 1. If t=Theta(n), m is only bounded and the gain disappears; table preparation may also cease to be sublinear. No exact or polynomial-accuracy claim follows by sending epsilon to zero inside a fixed-epsilon theorem.

## 6. Why black-box Bluestein did not suffice

Here let M=nextpow2(2N-1), so M=Theta(N), distinct from the oversampling length in Sections 2–5. Define J as zero padding to length M, P as restriction to the first N entries, D_j=exp(-pi i j^2/N), and the chirp b at residues t mod M, t=-(N-1),...,N-1, by b_t=exp(pi i t^2/N), zero elsewhere. Then

  U_N=D P U_M^* diag(lambda) U_M J D,
  lambda=sqrt(M/N)U_M b,
  ||b||_2=sqrt(2N-1).                                  (15)

The normalized multiplier satisfies ||lambda||_infinity=O(1), uniformly in N. Here is an elementary version of the standard quadratic exponential-sum estimate. Write z_t=exp(2 pi i f(t)), f(t)=t^2/(2N)-kt/M. Its successive phase difference d_t=f(t+1)-f(t) advances by exactly 1/N and ranges over an interval of length below 2. For N>=16, set alpha=N^{-1/2}. Remove those indices where d_t lies within alpha of an integer; there are O(alpha N+1)=O(sqrt(N)) of them, because only a fixed number of integers can occur. The remaining indices form a fixed number of intervals on each of which d_t increases inside [r+alpha,r+1-alpha]. Put v_t=(exp(2 pi i d_t)-1)^{-1}. The identity v_t=-1/2-(i/2)cot(pi d_t) shows both |v_t|=O(1/alpha) and total variation O(1/alpha) on each interval. Summation by parts in z_t=v_t(z_{t+1}-z_t) bounds its exponential sum by O(1/alpha)=O(sqrt(N)). Including the removed indices proves |sum_t z_t|=O(sqrt(N)). The finitely many N<16 are absorbed by the same absolute constant. Dividing by sqrt(N) proves the multiplier bound.

This controls propagation of input and inverse-transform error; the crude l1 bound would unnecessarily lose sqrt(N). It does not give a sufficiently accurate cold construction of lambda.

In fact, an l2-relative chirp-transform contract permits error e=delta sqrt(2N-1)e_k in U_M b. The induced multiplier error is sqrt(M/N)e. Choose a unit input satisfying

  (D x)_j=N^{-1/2} exp(2 pi i k j/M), 0<=j<N.

Its padded unitary transform has kth coordinate sqrt(N/M). Restricting the kth inverse Fourier basis vector to N coordinates has norm sqrt(N/M). Consequently the induced final error is exactly

  delta sqrt[N(2N-1)/M]=Theta(delta sqrt(N)).           (16)

Dyadic approximations to this input with O(log N) bits preserve a constant fraction of the lower bound, so the phenomenon is compatible with the finite input model. Thus a guarantee relying only on that black-box contract must choose delta=O(epsilon/sqrt(N)). Its precision is Theta(log N), collapsing the growing radix.

Equation (16) is a sharp insufficiency example for the stated black-box guarantee. It does not assert that the actual F132 quantization error is the chosen vector, that all Bluestein implementations fail, or that a more structured chirp-spectrum construction is impossible. An efficient certified sup-norm chirp multiplier remains a separate potentially useful problem. The interpolation construction proves the all-length theorem without assuming its solution.

## 7. Fusion boundaries and useful corollaries

### 7.1 Orthogonal structured component plus residual

If an orthogonal projector P and its Fourier support projector Pi satisfy U_N P=Pi U_N, and a charged procedure computes s=Px and r=(I-P)x in the same finite dyadic model, independently approximate their transforms with errors eta_s||s|| and eta_r||r||. Enforce the disjoint supports Pi and I-Pi on the outputs. Orthogonality gives

  ||error||_2^2 <=eta_s^2||s||_2^2+eta_r^2||r||_2^2.    (17)

A concrete compatible case is N=QM with Q,M powers of two and (Px)_{a+tQ}=M^{-1}sum_u x_{a+uQ}. It costs O(N) exact dyadic work; U_N Px is supported at frequencies divisible by M, with those values sqrt(M)U_Q of the fiber means. The square-root factor is prepared or exact when appropriate. A small certified residual can use coarser tabulation accuracy. This does not turn an exact-field sparse-fiber recognizer into a stable dyadic decomposer; the generic growing-fiber fusion still needs such an interface.

### 7.2 Spectral certificates and nonlinear execution

The interpolation matrices B and B_h have genuine spectral norm certificates. Each dyadic small-block coefficient matrix does too. The complete rounded tabulator, however, is nonlinear. The correct global statement is an all-input normwise error contract, not a claim that the program equals one fixed approximating matrix. Replacing this distinction by an operator norm of the whole nonlinear execution would be unjustified.

### 7.3 A general lesson, not a new Four-Russians principle

A stable program with a small reusable family of growing local transforms can be compiled into finite response tables when its total live key width is O(log N), its precision alphabet is sublinear in log N, and all table preparation and data movement fit the claimed budget. The F132 proof verifies these premises for normalized Fourier macroblocks. A generic arbitrary circuit theorem must separately charge its coefficient/template descriptions and cannot treat an unbounded collection of different local maps as a single free table.

## 8. Verification and remaining work

The original F132 mathematical construction was read directly, including normalization, saturation exclusion, all padded tables, twiddle generation and space. Its source hash is a18a347674000c77f29ad86d5ffad2986b4f1091bcb25a3f9487905216a09f84. No uploaded program was executed, imported, compiled or AST-parsed. The historical prototype's tests are not fresh execution evidence.

The preceding-cycle independent script, check_new_interpolation.py, checked the centered identities, cutoff plateaus, exact alias-norm formula, Schur tails, coarse coefficient perturbations and sharp Bluestein expression. Its recorded eight interpolation cases N=17 through 129 and six obstruction cases N=17 through 1001 passed. Those are inherited records, not reruns in this second pass. The largest interpolation identity entry discrepancy is below 1.8e-14 in ordinary floating arithmetic. These are falsification checks, not proofs or runtime benchmarks; the analytic proofs above carry the theorem.

Two preceding-cycle mathematical reviewers checked the interpolation identity, alias normalization, periodic shell bounds, fractional-offset derivative and word-size/preparation arguments. This is internal proof review, not external peer review. The strongest remaining tasks are an independent external theorem/model comparison, a formally checked implementation of the eager-table executor and coefficient certificates, and a realistic crossover study. None is needed to state the present paper-level upper bound honestly; none has been claimed complete.

Primary literature comparisons and precise novelty boundaries are recorded separately in PRIOR_ART_COMPARISON.md and prior_art_comparison.json.


## 9. Total fallback and the word-width boundary

For every N>=2 and 2<=t<=n, a direct fallback satisfies the same accuracy and O(N)-word space contract. Normalize x as above. Construct each entry of U_N to complex error at most 2^{-t}/(16N), using a common dyadic denominator of O(t+n) bits and the certified generator in Section 10. Form each row's dot product exactly and write it, restoring R exactly. The approximation matrix A obeys ||A-U_N||_2<=||A-U_N||_F<=2^{-t}/16, so the output error is already below the target. No final loss of accuracy is required: the exact dyadic row sum has O(cn+t) bits. Construct entries a row at a time, and reuse all coefficient scratch memory.

Its conservative time is N^2 poly(n+t), with an absolute fixed polynomial. Its working storage is O(N)+poly(n+t) words; because t<=n and every fixed polynomial in n is O(2^n)=O(N), this is O(N) with an absolute constant. Addresses to that storage and all fixed-length online numerators fit the asserted fixed multiple of n bits. The integer interval algorithms in preparation use polynomially many ordinary word operations and never count an unbounded integer as one instruction.

This fallback is deliberately a correctness fallback, not a claim of an efficient practical algorithm. For every t=o(n) schedule the fast branch is eventually selected, since its complete preparation bound is N^{1/4}poly(n)+N^{o(1)}=o(N), m->infinity, and its O(t)-width stencil is smaller than M. Consequently the fallback does not affect any stated asymptotic saving.

**Separate arbitrary-precision totality proposition.** For arbitrary supplied t>=2, the same direct construction works on a RAM with w=C(c)(n+t+1) bits and time N^2 poly(n+t), using O(N)+poly(n+t) words. Alternatively, ordinary multiword arithmetic may be used with enough address capacity for the explicit precision-dependent storage. This proposition accounts for fixed-epsilon small-size exceptions and arbitrary higher precision. It is not the fixed-w=Cn saving theorem. No assertion about an arbitrarily long precision target fitting a log N-bit address space is made.

## 10. Complete elementary coefficient-generation justification

Here is one uniform construction sufficient for every coefficient assertion in the manuscript. It is intentionally inefficient by a polynomial factor, which all cold bounds already pay.

Given a rational angle parameter with O(L) numerator/denominator bits and a requested absolute error 2^{-Q}, reduce it modulo one or modulo two by exact division. Machin's identity pi=16 arctan(1/5)-4 arctan(1/239), with alternating-series remainder bounds, produces a rational interval for pi of width 2^{-O(Q+L)} using O(Q+L) terms. Evaluate sine and cosine on a bounded reduced interval by rational Taylor sums with certified factorial remainders. A degree O(Q+L) suffices; for instance any sufficiently large fixed multiple of Q+L+1 makes the elementary factorial remainder exponentially small. Exact rational numerators and denominators have polynomially many bits, even without sophisticated cancellation. Grade-school integer operations therefore give a fixed polynomial bound on time and scratch storage. Round only after the resulting interval certifies the requested dyadic enclosure.

For a positive rational R in a fixed polynomial range, floor(sqrt(2^{2Q}R))/2^Q and the adjacent dyadic give a certified square-root interval, obtained by integer division and integer square root. In particular floor(2^Q/sqrt(r))=isqrt(floor(2^{2Q}/r)). This constructs 1/sqrt(r), sqrt(M/N), and every scale factor. An entry of A_r needs only Q=p+ceil(log2 r)+O(1) final fractional bits, with extra polynomial-cost guard precision during certification.

For the interpolation kernel, a nonzero retained argument t_0=(theta'-j)/M has distance from an integer at least eta/M and less than 1/2. Thus |sin(pi t_0)|>=2 eta/M. Coefficient denominators 2q+1 and M are exact integers with O(n) bits. If the sine intervals have absolute width d, standard interval division bounds each normalized quotient error by at most a fixed constant times M^2 eta^{-2} d. With Q=8(n+a+ceil(log2(s+1))+16), taking d<=2^{-Q} is far smaller than the eta/[64(s+1)] target. It also makes the denominator interval disjoint from zero. The t_0=0 case is evaluated from its exact limiting value, so no zero denominator is passed to division.

All exact normalized factors have magnitude at most one. If each is approximated within xi=eta/[64(s+1)], repeated multiplication (or binary exponentiation with separately certified error) gives an s-fold product error at most s xi (1+xi)^s<=2s xi. Combining the first normalized Dirichlet factor and final dyadic rounding keeps the total kernel coefficient error below eta. Every intermediate certificate requires only polynomial(n+a+s) work. The coefficients g_j are used in the proof but are never enumerated by the algorithm.

This establishes a fixed computable polynomial P dominating preparation cost and storage per table entry. Use that P in the fast-branch preparation-cap test. Its value is part of the uniform implementation description, not an unknown asymptotic oracle. Sublinear table cardinalities multiplied by P remain sublinear in all claimed regimes.

## 11. Optional guarded full-circle twiddle preparation

The coarse-grid method in Sections 1 and 3 is sufficient. A second, independently justified implementation can remove its exponential-in-p phase-preparation term at the cost of O(H) storage/work. This does not improve the input-state/key precision boundary or remove the interpolation offset table.

Let H=2^v, u=2^{-p}, and Q=p+v+12. Certify omega_hat with |omega_hat-exp(-2 pi i/H)|<=2^{-Q}. Set z_0=1 and recursively compute z_{j+1}=R_Q(z_j omega_hat), where R_Q truncates both real components to the fixed lattice 2^{-Q}Z. The complex rounding error is at most sqrt(2)2^{-Q}. For e_j=|z_j-omega^j|,

  e_{j+1}<=(1+2^{-Q})e_j+(1+sqrt(2))2^{-Q}.

For j<=H, H2^{-Q}<=1/4096, hence

  e_j<=6H2^{-Q}<u/512<u/8.

In particular |z_j|<2; every product, truncation and address has O(v+p) bits. The seed costs poly(v+p) operations and the complete H-entry circle costs O(H). All Cooley-Tukey phase orders divide H, so their addresses are exact integer multiples in this circle. The dyadic primitive's stage bound is unchanged. Likewise an N-entry circle generated with Q=t+ceil(log2 N)+O(1) supplies the final d_ell phases in O(N)+poly(n+t) work.

This is a precision-aware recurrence. A recurrence performed at only p fractional bits has an O(H2^{-p}) error bound and is not interchangeable with it. The additional v guard bits are legal because this word-RAM charges O(v)-bit integer multiplication as O(1), while p=o(v) in the saving regime. Nothing here proves a bounded-bit hardware speedup or new numerical-analysis principle.

## 12. Second-pass disposition

No counterexample to the main finite-word approximate upper bound was found. The revisions make total quantizer semantics, spare zero-code capacity, initial rounding, exact exponent widths, fallback conditions, coefficient certificates and the precision domain explicit. The original all-length interpolation identity, all-input spectral bound, separated-grid Schur tails and 22rho error budget remain intact.

Fresh controls in this directory are independently authored. They exercise finite toy tables exhaustively, high-guard recurrence behavior, actual-parameter interpolation identities and the symbolic budgets. They do not execute supplied research programs, establish publication novelty, validate an asymptotic eager-table production executor, or replace the proofs.

The novelty disposition is unresolved. The finite-state mechanism has explicit precedents; model-matched source comparisons are in PRIOR_ART_SECOND_PASS.md. The open exact arbitrary-complex FFT objective is not solved by this finite-word approximate theorem.
