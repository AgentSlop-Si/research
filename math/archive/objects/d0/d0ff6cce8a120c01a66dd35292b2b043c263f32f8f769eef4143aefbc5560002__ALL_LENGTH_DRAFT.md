# All-length normwise Fourier compiler: draft for independent checking

This is a fresh mathematical derivation. No uploaded program was run, imported, compiled or AST-parsed. Classical oversampled Fourier interpolation is explicitly credited; the proposed new project contribution is its finite-word composition with the F132 norm-certified tabulator.

## Analytic interpolation lemma

Let N>=2, M=2^ceil(log2(4N)), so 4N<=M<8N. Set c=floor((N-1)/2), and embed x_j at index j-c modulo M, obtaining v in C^M. Its occupied signed frequencies obey |j-c|<=N/2<=M/8. Write z=U_M v and f(t)=sum_j x_j exp(-2 pi i (j-c)t), so z_k=f(k/M)/sqrt(M).

Let s>=2, M>=16s, L=M/4, q=floor(M/(8s)), and mu_q be the probability measure uniform on the integer interval [-q,q]. Define

  g=1_{[-L,L]} * mu_q^{*s},
  D_a(t)=sum_{j=-a}^a exp(-2 pi i j t),
  K(t)=D_L(t)/M * (D_q(t)/(2q+1))^s.

Then 0<=g<=1, g=1 for |j|<=L-sq (hence |j|<=M/8), and g=0 for |j|>L+sq<=3M/8. K is exactly M^-1 sum_j g_j exp(-2 pi i j t). Discrete orthogonality gives

  (U_N x)_ell = exp(-2 pi i c ell/N) sqrt(M/N)
                 sum_{k=0}^{M-1} K(ell/N-k/M) z_k.

Let B denote the N-by-M matrix multiplying z, including sqrt(M/N) but excluding the final phase. In signed frequency coordinates the map is aliasing modulo N after multiplication by g. Each residue class has at most ceil(M/N)<=8 entries, so ||B||_2<=sqrt(8). This bound is valid on all C^M, not only on exactly bandlimited z.

Put d=M*distance(t,Z), 0<=d<=M/2. For d>0, using |sin(pi t)|>=2*distance(t,Z) and q>=M/(16s),

  |K(t)| <= [1/(2d)] min(1,4s/d)^s,
  |K(t)| <=1 for every t.

Let h=16s+1, require 2h+2<M, set r_ell=floor(ell M/N), theta_ell=ell M/N-r_ell. Retain the indices k=(r_ell+j) mod M for j=-h,...,h+1. Every omitted circular distance is at least 16s. Since the source nodes are unit spaced and target nodes ell M/N are >=4 apart around the circle, there are at most four nodes in every unit-distance shell for both row and column tails. Consequently, with a generous constant,

  ||B-B_h||_2 <= 12*4^-s.

One direct bound is 4 sum_{r>=16s} (4s)^s/(2 r^(s+1)) <= 4*4^-s, applied to row and column absolute sums and then multiplied by sqrt(M/N)<3. This proves spectral, not merely entrywise, approximation without a sqrt(N) loss.

## Finite coefficient tables

For fixed integer j, theta in [0,1), the derivative of K((theta-j)/M) has magnitude at most

  (2 pi/M^2) sum_{|a|<=3M/8}|a|g_a <= 4.

Round theta down to a grid with mesh eta=2^-a. Prepare a table of certified dyadic approximations to K((theta_grid-j)/M) for every grid value and j=-h,...,h+1. If each stored coefficient has absolute error <=eta, each retained matrix entry changes by <=5eta. Each row and each column has at most 2h+4 retained entries. Thus, after sqrt(M/N),

  ||B_h-B_tilde||_2 <=15(2h+4)eta.

Choose eta<=epsilon/[2^16(h+2)], and s=ceil(log2(2^16/epsilon)). Both errors are then much smaller than epsilon/16. All tables have 2^a O(h)=2^{O(log(1/epsilon)+log log(1/epsilon))} entries. Evaluate the explicit product of Dirichlet kernels by certified rational trigonometric approximation. At t=0 use the exact limiting value; elsewhere the smallest possible denominator is >=2 eta/M. O(log M+a+log s) guard bits and polynomial(log M+a+s) work per table entry suffice. A crude polynomial-time rational method is adequate, because total table preparation is sublinear for log(1/epsilon)=o(log N). The Fourier coefficients g need never be enumerated.

Prepare sqrt(M/N) and final phases to appropriately divided epsilon accuracy, using a single certified square-root approximation and a complete phase table. Fractional offsets and phase addresses are computed exactly from O(log N)-bit integers. Compute each short dyadic dot product exactly on a fixed number of sufficiently large Theta(log N)-bit words, then round once. No uncharged transcendental evaluation, arbitrary precision online scalar, or omitted output is used.

## Composition and asymptotics

Run F132 on v with accuracy delta=epsilon/64 (or a smaller fixed constant multiple). The approximate interpolation operator has norm <4. Allocate epsilon/16 each to kernel truncation, kernel discretization, scale/phase error, and final rounding/underflow. The triangle inequality then proves ||reported-U_N x||_2<=epsilon||x||_2 after the same power-of-two input normalization and exact rescaling used by F132.

Write n=ceil(log2(N+1)), p=O(log n+log(1/epsilon)), b=O(p+log n), and m the largest dyadic radix satisfying mb<=c_0 n. Total cold work is

  O(N n/log m + N[1+log(1/epsilon)]
    + N^{1/4}poly(n,p) + 2^{O(p)}poly(n,p)).

Memory is O(N) words. Hence the fixed-epsilon O(N log N/log log N) and epsilon=2^-ceil(n^beta), 0<beta<1, bounds hold for every integer N, not just powers of two. Supplied/efficient schedules log(1/epsilon)=o(log N) give o(N log N); charge schedule computation. Polynomially small epsilon is outside the speedup. Tiny lengths where h is not small compared with M can use a conventional finite-precision Bluestein FFT; for each fixed-epsilon or fixed-beta regime only finitely many sizes need this fallback.

## Bluestein caution

For M=nextpow2(2N-1), the padded chirp b has norm sqrt(2N-1). Its normalized convolution multiplier is lambda=(unnormalized DFT_M b)/sqrt(N)=sqrt(M/N)U_M b. A uniform quadratic exponential-sum bound can yield ||lambda||_infinity=O(1), but an F132 call with only relative l2 accuracy delta controls multiplier sup error only by O(delta sqrt(N)). That black-box route therefore needs delta=O(epsilon/sqrt(N)), loses the growing radix, and does not prove the desired runtime. The interpolation construction bypasses this preparation bottleneck; it does not claim to solve it.
