# Deterministic normwise Fourier tabulation at every length

10 October 2026. Final research statement and proof-level synthesis.

## Result and status

The original F132 construction survives its finite-word, deterministic, all-input relative-Euclidean contract. A new project-level derivation here removes its power-of-two restriction by composing it with a fully charged, stable, oversampled Fourier interpolation scheme. The usual black-box Bluestein shortcut does not prove this extension: a sharp example below identifies a square-root-of-length error amplification in preparing the chirp multiplier from an l2-only FFT guarantee.

The ingredients are classical: Cooley–Tukey factorization, finite-state/Four-Russians tabulation, floating quantization, oversampled Fourier interpolation and Schur norm bounds. This document establishes a precise combined upper bound and closes a project gap. It does not establish worldwide priority, a new exact-complex arithmetic FFT, a bit-complexity breakthrough, or a practical implementation.

### Theorem 1: all lengths, all represented inputs

Fix a constant c describing the input format. There is a uniform deterministic algorithm with the following properties.

* N is any positive integer.
* Each real and imaginary input component is an O(log(N+1))-bit dyadic of polynomial dynamic range. For example, x_j=(a_j+i b_j)2^{-B}, |a_j|,|b_j|<=N^c and |B|<=c log2(N+1). Separate exponents bounded by O(log N) are also permitted.
* The machine is an address-capable word RAM with w=C log2(N+1) bits, for sufficiently large fixed C depending only on c, supporting integer arithmetic including multiplication and division, comparisons, shifts, Boolean operations and random access. A fixed number of words costs O(1).
* Epsilon is a fixed dyadic in (0,1/4], or a supplied dyadic precision target described below.

The algorithm explicitly writes all N coordinates of y, in a finite dyadic mantissa/exponent format, such that

  ||y-U_N x||_2 <= epsilon ||x||_2,
  (U_N)_{k,j}=N^{-1/2} exp(-2 pi i k j/N).

For fixed epsilon its cold running time is O_epsilon(N log N/log log N), and its storage is O(N) words. Every table entry, root/phase approximation, input scan, normalization, gather/scatter, address, and output write is charged.

Let n=ceil(log2(N+1)). For epsilon_N=2^{-ceil(n^beta)} and any fixed 0<beta<1, the same running-time order holds with a constant depending on beta, provided the integer exponent ceil(n^beta) is supplied or efficiently generated; its generation cost is charged. More generally, when t_N=ceil(log2(1/epsilon_N))=o(n) is supplied or efficiently computed, the running time is o(N log N), plus the charged cost of producing t_N. Mere computability of a precision schedule is not a complexity bound.

These assertions are asymptotic. The deliberately conservative tables can have astronomically late crossovers. Polynomially small epsilon=N^{-a} is not covered by the saving.

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

A nonzero real state is sign*(2^p+f)*2^{e-p}, with 0<=f<2^p and e_min<=e<=e_max. Reserve a zero code; define unused padded codes to mean zero. One complex state occupies

  b=2[p+ceil(log2(e_max-e_min+2))+1]=O(p+log v)

bits. Mantissa truncation with underflow to zero satisfies, before any upper saturation,

  ||q(z)-z||_2 <= u||z||_2+sqrt(2H)tau.                 (1)

All decoded states lie on one dyadic lattice. If p=o(v), exact products and poly(v)-length dot products of these states and O(p+log v)-bit dyadic coefficients have O(v+p) bits. A fixed number of sufficiently wide words therefore suffices online. Polynomial-bit rational work during preparation is charged separately.

### 1.2 Enumerate every block response

Choose the largest power-of-two radix m with mb<=v/4. For every power-of-two r<=m, prepare a dyadic matrix A_r whose entries differ from U_r by at most u/(8r). Consequently ||A_r-U_r||_2<=u/8, by the Frobenius norm bound.

For each of the 2^{br} padded state keys, decode all r components, compute A_r z exactly in fixed-point arithmetic, quantize, and pack the r resulting codes. This defines every table entry, including invalid and unreachable keys. Its preparation is bounded by

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

An intentionally generous count of at most L_0=2v+1 rounded unitary stages avoids circular precision selection. If e_j is the cumulative error from the ideal unitary program, (2) implies

  e_{j+1}<=(1+3u)e_j+3u||a||_2+sqrt(2H)tau.

Therefore

  e_{L_0}/||a||_2 <=6uL_0+4L_0 sqrt(2H)tau
                   <=6uL_0+8L_0 H tau <delta.           (3)

Here (1+3u)^{L_0}<=2 and ||a||_2>=1/2 were used. A first-overflow argument makes the reasoning noncircular: before the hypothetical first saturation, (3) bounds every stored vector norm by (1+delta)sqrt(2H); a prequantized block can enlarge it by only 1+u/8. This is far below the upper magnitude threshold 16H. Thus the first saturation cannot occur.

Restore R exactly in each output's exponent. The cold running time and storage are

  O(H+Hv/log m+H^{1/4}poly(v,p)+2^p poly(v,p)),
  O(H) words.

For fixed delta, b=Theta(log v), m=Theta(v/log v), and log m=Theta(log v). For t=log2(1/delta)=Theta(v^beta), 0<beta<1, b=Theta(v^beta) and log m=Theta((1-beta)log v). If p=o(v), m tends to infinity and preparation is o(H).

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

The only exact zero denominator in the retained grid domain is t=0, whose limiting value was given above. Every other grid argument has distance from zero at least eta/M. A sufficiently large constant times n+a+log(s+1) guard bits certifies the sine ratios to O(eta/s), after exact argument reduction. Each normalized factor has magnitude at most 1, so the s-fold product loses only an O(s) error factor. Elementary rational interval algorithms run in poly(n,a,s) bit or word operations per entry. The Fourier coefficients g_j need not be enumerated. This explains both the uniformity and the absence of N separately expensive transcendental evaluations.

### 3.2 Scale and final phases

Prepare one dyadic alpha_hat with

  |alpha_hat/sqrt(M/N)-1|<=rho.

A certified integer-square-root interval requires polynomial(n+log(1/epsilon)) work. Prepare a complete coarse phase grid of size G=2^{ceil(log2(32/rho))}, with each entry within rho/4 of its exact unit-circle point. To obtain d_hat_ell, round (c ell mod N)G/N to the nearest integer. The angular rounding error is at most pi/G<rho/8; thus |d_hat_ell-d_ell|<=rho. Only the coarse grid is prepared, not N separate transcendental calls. Phase addresses require O(1) word arithmetic per output.

Let E=(alpha_hat/sqrt(M/N))*diag(d_hat_ell). Then

  ||E||_2<2, ||E-D||_2<=3rho.                          (12)

### 3.3 Exact online short sums and final quantization

All kernel, scale and phase approximations are dyadics. Align the dyadic FFT outputs to a fixed lattice and evaluate each retained O(h)-term dot product exactly, followed by exact dyadic scale and phase multiplication. The numerator bit length is

  O(n+p+a+log(s+1)),

where p=O(log n+log(1/epsilon)) is the dyadic primitive's mantissa parameter. Because p,a,s=o(n) in the general regime, a fixed number of sufficiently large Theta(n)-bit words suffices. This counts every multiply, addition and alignment; it is not an arbitrary-precision scalar oracle. Preparation may use polynomially many words, included in its sublinear bounds.

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

Both preparation terms are o(N) if p=o(n). The input, dyadic FFT working arrays, sparse interpolation working state and explicit output require O(N) words; all prepared tables occupy o(N) words. Interpolation can stream its short rows and does not store an N-by-h matrix.

For fixed epsilon, log m=Theta(log n), proving O_epsilon(Nn/log n). For t=ceil(n^beta), 0<beta<1, log m=Theta((1-beta)log n), and Nt=o(Nn/log n). For any supplied t=o(n), both Nn/log m and Nt are o(Nn). If t=Theta(n), m is only bounded and the gain disappears; table preparation may also cease to be sublinear. No exact or polynomial-accuracy claim follows by sending epsilon to zero inside a fixed-epsilon theorem.

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

A fresh independent script, check_new_interpolation.py, checks the new centered identities, cutoff plateaus, exact alias-norm formula, Schur tails, coarse coefficient perturbations and sharp Bluestein expression. Eight interpolation cases N=17 through 129 and six obstruction cases N=17 through 1001 pass. The largest interpolation identity entry discrepancy is below 1.8e-14 in ordinary floating arithmetic. These are falsification checks, not proofs or runtime benchmarks; the analytic proofs above carry the theorem.

Two separate mathematical reviewers checked the interpolation identity, alias normalization, periodic shell bounds, fractional-offset derivative and word-size/preparation arguments. This is internal proof review, not external peer review. The strongest remaining tasks are an independent external theorem/model comparison, a formally checked implementation of the eager-table executor and coefficient certificates, and a realistic crossover study. None is needed to state the present paper-level upper bound honestly; none has been claimed complete.

Primary literature comparisons and precise novelty boundaries are recorded separately in PRIOR_ART_COMPARISON.md and prior_art_comparison.json.
