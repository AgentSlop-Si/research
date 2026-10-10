# Marked-cycle Fourier synthesis
## An explicit fixed graph, linear-work scalar cycle data, and a precise unresolved fast-evaluation problem

**Date:** 10 October 2026.  
**Status:** Exact identities with proofs, a working arbitrary-input dyadic Fourier executor, linear-work auxiliary algorithms, and independent finite-field tests. The executor still costs **Theta(N log N)**. The proposed **O(N log log N)** marked-cycle circuit is a **conjecture**, not a constructed algorithm. No publication-priority, numerical-stability, or integer-multiplication claim is made.

The principal change from the preceding mass-contraction and short-annihilator proposals is that **every Fourier graph edge and coefficient is now explicit for every dyadic length**. There is no unspecified Fourier-compatible parameter family. The unresolved step is instead an arithmetic compiler for one explicit, input-dependent, scalar marked-determinant coefficient.

## 1. Problem and model

Let N=2^n >= 2 and let E be a characteristic-zero field containing a supplied primitive N-th root omega. The unnormalized Fourier convention is

    F_N[k,j] = omega^(k*j).

The same algebra holds in appropriate finite fields; identities with division by small integers require those integers to be nonzero in the field. The tests use 65537 and 998244353, with lengths dividing p-1. A fixed test field does not support arbitrarily large lengths.

The target counts all scalar additions, subtractions, multiplications, divisions, coefficient preparation, input reads, output writes, and addressing. Integer indices and phase exponents are polynomially bounded in N; their word representation uses O(log N) bits. Arbitrary complex scalar arithmetic is idealized and exact. This is not a bit-complexity or bounded-coefficient model.

No related-input cache, approximate sketch, amplitude-encoded quantum output, or parallel running time is substituted for the target. The requested output is N explicit values for a fresh arbitrary x.

### Research synthesis

The earlier project established valuable dynamic, sparse-defect, and structured-input algorithms, but their promises do not cover a generic new vector. Complete local phase banks restore all information but can reduce to ordinary mixed-radix FFT. Recent Green sum and common-cycle gates rule out several simple linear-scan representations. The present construction therefore preserves all input coordinates, uses a non-additive shared graph, and proves its Fourier phases directly rather than through graph rank alone. See SOURCE_LEDGER.md for the actual reviewed sources and scope.

## 2. A single fixed sparse operator implements Fourier after n steps

Define Q_N by

    (Qx)[2r]   = x[r] + x[r+N/2],
    (Qx)[2r+1] = omega^r * (x[r] - x[r+N/2]),
    0 <= r < N/2.                                      (2.1)

Equivalently, with e_s the coordinate vectors,

    Q e_s = e_(2s mod N) + omega^s e_((2s+1) mod N).    (2.2)

It is a weighted binary shift-register/de Bruijn graph. It has exactly 2N edges and the same edge weights at every application. The sign in (2.1) follows from omega^(s+N/2)=-omega^s.

Define an integer digital phase phi by

    phi(0)=0,
    phi(2a)=phi(a),
    phi(2a+1)=phi(a)+a.                                (2.3)

Let rev_n(r) reverse the n binary digits of r. Let C be diagonal with C[r,r]=omega^(-phi(r)), and let R reorder coordinates by binary reversal.

### Theorem 2.1 — explicit stationary Fourier identity

For every N=2^n and every input x,

    F_N = R C Q_N^n,                                  (2.4)

or entrywise,

    (F_N x)[k] = omega^(-phi(rev_n(k)))
                 * (Q_N^n x)[rev_n(k)].               (2.5)

**Proof.** A path through Q appends one binary digit b_t at each step and shifts out the oldest digit. After n steps, each prescribed final vertex r has exactly one path from a prescribed starting vertex s. Write the emitted word in chronological order as b_0...b_(n-1), the n binary digits of r from high to low. Its Fourier index is k=sum_t b_t 2^t=rev_n(r).

Before step t, the state is 2^t s + prefix_t modulo N, where prefix_t is the integer represented by b_0...b_(t-1). The accumulated exponent is

    sum_t b_t (2^t s + prefix_t)
      = s*k + sum_t b_t prefix_t
      = s*rev_n(r) + phi(r) mod N.

There are no other paths with these endpoints at this length. Thus

    (Q^n)[r,s]=omega^(s*rev_n(r)+phi(r)),

which is (2.4). QED.

All phi values and reversed indices can be generated in O(N) integer operations; all required root powers take O(N) field operations. Moreover 0<=phi(r)<N. Its zero set is exactly 0 and the powers of two below N. These facts follow directly from (2.3): a nonzero summand occurs precisely when a 1 digit has a nonempty nonzero prefix, and phi(r)<r for r>0 by induction.

### Partial-power formula

For 0<=t<=n, set L=2^t and m=N/L. Write the output index as r=L p+v, 0<=v<L. Then

    (Q^t)[L p+v, a m+p]
       = omega^((a m+p)*rev_t(v)+phi(v)),              (2.6)

for a=0,...,L-1, and all other entries are zero. The same path calculation proves this. It gives a full small-Fourier-bank interpretation of intermediate powers; it is not a compressed arithmetic evaluator for them.

### Exact cost of the implemented baseline

For N>=2, one Q application uses N additions/subtractions and N/2-1 scalar multiplications when the multiplier 1 at r=0 is skipped. Applying Q n times and performing the final correction uses

    additions/subtractions = N*n,
    multiplications = n*(N/2-1) + N-n-1
                    = N*n/2 + N-2n-1.                (2.7)

The root table uses N-2 multiplications after the root is supplied; phase and reversal preparation and all data movement are O(N) per required pass. The total work remains Theta(N log N), and the working vector storage is O(N).

For example, N=8 uses 24 additions/subtractions and 13 counted scalar multiplications online, plus preparation. This is an exact instruction count for this implementation, not a superiority claim against optimized FFT kernels.

Over C, Q/sqrt(2) is unitary: a coordinate shuffle exposes N/2 disjoint phase-weighted two-point butterflies. A proposed faster compiler must not invoke this as an escape from conditioning-dependent gate lower bounds.

**Prior-art boundary.** Constant-geometry FFTs are established [P1]. The stationary reformulation is not being claimed as an independently novel FFT algorithm. Its role here is to provide completely explicit coefficients for the new cycle/Green synthesis target.

## 3. Two easy tree Green operators and an exact weighted-Haar reduction

Split

    Q=A_0+A_1,
    A_b e_s=omega^(b*s)e_(f_b(s)),
    f_b(s)=(2s+b) mod N.                              (3.1)

For b=0 the graph feeds into the fixed point 0. For b=1 it feeds into N-1. Every vertex reaches its fixed point in at most n steps, because repeated transitions append a constant binary digit.

### Lemma 3.1 — exact linear-work branch solve

The equation

    (I-z A_b)y=x

can be solved in O(N) arithmetic and addressing whenever

    1-z*lambda_b != 0,
    lambda_0=1, lambda_1=omega^(-1).                  (3.2)

**Proof.** Remove the fixed-point self-loop. The remaining graph is a directed tree toward the root. Initialize y=x. In leaf-to-root order, for each nonroot s, add

    z*omega^(b*s)*y[s]

to y[f_b(s)]. Divide the root coordinate by 1-z*lambda_b. Every nonroot edge is processed once. The topological order itself can be generated by indegrees and a queue in O(N). QED.

These operators have minimal polynomial of degree exactly n+1. Indeed A_b^(n+1)=lambda_b A_b^n gives the upper bound. For b=0, the images of e_1 through powers 0,...,n have distinct supports 1,2,4,...,N/2,0; for b=1 the images of e_0 have distinct supports 0,1,3,...,N-1. Their nonzero weights give n+1 independent vectors and the matching lower bound. Nevertheless, the direct tree solve is linear. More generally, a high minimal-polynomial degree does not by itself imply an expensive structured inverse. This corrects the temptation to treat the preceding short-annihilator feedback proposal as the only way to evaluate feedback cheaply.

### Lemma 3.2 — exact Schur reduction

Put m=N/2. Let J:E^m -> E^N inject into odd coordinates, and let

    (Cv)[r]=omega^r(v[r]-v[r+m]).

Then A_1=JC. Write G_0=(I-z A_0)^(-1) and

    H_N(z)=C G_0 J.

An exact Woodbury/Schur identity gives

    (I-zQ)^(-1)
      =G_0+z G_0 J (I_m-z H_N(z))^(-1) C G_0.         (3.3)

It holds as a formal power series around z=0, or at values where the displayed inverses exist. It follows by multiplying the proposed right-hand side by I-zA_0-zJC; no commutation is assumed.

### Theorem 3.3 — H and H inverse have linear-work trees

For v in E^m, split v=(v_L,v_R), and set u=v_L+v_R and d=v_L-v_R. For m>=2,

    (H_N(z)v)[2a]   = z*(H_(N/2)(z)u)[a],
    (H_N(z)v)[2a+1] = omega^(2a+1)*d[a],              (3.4)

where the child uses the primitive (N/2)-th root omega^2. The scalar base, N=2, is

    H_2(z)=(2z-1)/(1-z).                              (3.5)

The recurrence costs W(m)=W(m/2)+O(m)=O(m). Its inverse also costs O(m) when z!=0,1,1/2: divide the even coordinates by z, invert the child, undo the odd phases, and reconstruct the two halves with (u+d)/2 and (u-d)/2.

**Proof of the recurrence.** For column s, let j=2s+1. The branch path visits j,2j,4j,... modulo N. Applying C gives

    H_N(z)e_s
      =sum_(t=0)^(n-2) z^t omega^(2^t*j)
          e_(2^t*j mod m)
       + z^(n-1)*(2z-1)/(1-z) e_0.                   (3.6)

The t=0 term combines paired columns s and s+m/2 with opposite signs into odd output positions. All later terms combine them with the same sign into even positions and reduce to the child with squared root. The root tail is a geometric series; no analytic convergence assumption is needed because the equality is rational. QED.

For generic admissible z, each column of H has exactly n nonzeros, so explicitly writing the matrix takes Theta(N log N) entries even though its application and inversion take O(N) work. This is a genuine example of arithmetic sharing in the project: entry count and evaluation cost are different.

**Critical limitation:** A cheap inverse of H is NOT a cheap inverse of I-zH. Formula (3.3) reduces the unresolved coupled solve but does not solve it. The current code uses dense inversion only as a small-size verification oracle for (3.3).

## 4. Linear-work closed-cycle data through logarithmic degree

The shift-register graph makes short *closed* walks much cheaper to enumerate than arbitrary input-output paths.

### Theorem 4.1 — exact periodic-word trace formula

Fix any nonnegative constant c. All traces

    tr(Q^k), 1<=k<=n+c,

can be computed with O_c(N) field and address operations after O_c(N) preparation.

For a k-bit word a, let s_n(a) be the n-bit prefix of its infinite periodic repetition. Write n=qk+r, 0<=r<k. An explicit constant-word formula is

    repeat=(2^(q*k)-1)/(2^k-1),
    s_n(a)=(a*repeat)*2^r
             + (floor(a/2^(k-r)) if r>0 else 0).      (4.1)

Let v be a rotated left by r positions within k bits. It is the next k emitted bits following that n-bit prefix. Then

    tr(Q^k)
      =sum_(a=0)^(2^k-1)
         omega^(s_n(a)*rev_k(v)+phi(v)).              (4.2)

Exponents are reduced modulo N. The recurrence (2.3) defines phi for all nonnegative arguments, so it also covers k>n.

**Proof.** A length-k closed walk is a periodic binary sequence of period dividing k, with a specified starting window of n bits. Its k-period word uniquely determines both that window and its k emitted bits; conversely any such closed walk has exactly that description. Even when k>n, the emitted bits distinguish walks with the same initial state. The weight calculation is the same as the proof of Theorem 2.1. Summing these weights is exactly the diagonal sum of Q^k. QED.

The total number of words for k=1,...,n+c is

    sum_k 2^k=2^(n+c+1)-2.                            (4.3)

At c=0 this is 2N-2; at c=2 it is 8N-2. Bit reversals at every needed length and all phi values take the same O_c(N) total preparation. The exponents and integer products use O(log N) bits for fixed c, up to constant factors. There is no per-word O(log N) modular exponentiation: the implementation indexes a charged root-power table.

### Corollary 4.2 — linear-work determinant jet

Let

    D_N(z)=det(I-zQ)=sum_j d_j z^j.

Its coefficients through degree n+c are computed from the traces using

    d_0=1,
    d_j=-(1/j)*sum_(k=1)^j d_(j-k)*tr(Q^k).           (4.4)

Newton identities give (4.4). The additional work is O((n+c)^2)=O_c(N). Thus D_N(z) modulo z^(n+c+1) is available in linear work. In positive characteristic, require char(E)>n+c.

**Scope:** This computes scalar spectral data of Q, not Q^n x. Periodic-orbit expansions and characteristic-polynomial identities are established mathematics [P2]; the explicit phase formula, cost ledger, and connection to this Fourier graph are proved here. No priority claim is made for the trace algorithm in isolation.

## 5. Mark the boundary: a single scalar object contains every Fourier output

Introduce two N-vectors x and t. The vector x is the arbitrary input; t is a vector of formal markers. Add one hub vertex and define

    W_N(x,t) = [ Q_N   x ]
               [ t^T   0 ].                          (5.1)

There are at most 4N nonzero entries. The graph has a hub-to-vertex edge weighted by each x_j, and a vertex-to-hub edge weighted by each t_i. No input compression is involved.

Define

    E_N(z;x,t)=det(I_(N+1)-z W_N(x,t)).                (5.2)

### Theorem 5.1 — marked-determinant Fourier identity

As a formal power series at z=0,

    E_N(z;x,t)
      =D_N(z)*(1-z^2 t^T(I-zQ_N)^(-1)x).             (5.3)

Consequently, the explicit scalar polynomial

    S_N(x,t)=-[z^(n+2)] E_N(z;x,t)/D_N(z)             (5.4)

satisfies

    S_N(x,t)=t^T Q_N^n x,
    gradient_t S_N(x,0)=Q_N^n x,                     (5.5)

and

    (F_Nx)[k]
      =omega^(-phi(rev_n(k)))
         * (gradient_t S_N(x,0))[rev_n(k)].           (5.6)

**Proof.** Taking the Schur complement of I-zQ in I-zW gives (5.3). Because D_N(0)=1, the identity is valid formally regardless of singularities away from zero. Expand (I-zQ)^(-1)=sum_(j>=0) z^j Q^j and extract the required coefficient. Formal differentiation of the bilinear polynomial gives (5.5), and Theorem 2.1 gives (5.6). QED.

The determinant E is exactly affine in t, not just approximately affine near zero. A permutation term in a determinant can use only one entry from the hub row, and (5.3) makes this explicit. Its input-dependent part is bilinear in x,t.

Since D is input-independent and its jet through degree n+2 costs O(N), a fast program computing the marked coefficients of E through degree n+2 would yield a fast program for S. The short formal quotient requires O((n+2)^2)=O(N) additional arithmetic. This does NOT say that a fast marked E program has been found.

### Equivalent trace form

In characteristic zero, or when n+2 is invertible, put

    f_N(x,t)=tr(W_N(x,t)^(n+2))/(n+2).                (5.7)

Then

    gradient_t f_N(x,0)=Q_N^n x.                     (5.8)

Indeed d tr(W^L)=L tr(W^(L-1)dW), and at t=0 the top-right block of W^(n+1) is Q^n x. In closed-walk language, a walk visiting the hub exactly once uses one x edge, n Q edges, and one t edge; the n+2 possible starting positions explain the factor.

Unlike E, f can contain terms of higher degree in t, corresponding to multiple hub visits. They disappear after differentiation at zero, not from the full trace polynomial. It would be incorrect to equate f itself with t^T Q^n x.

The scalar value f_N(x,0) is independent of x. A program that discards all t-dependent terms before differentiation loses the answer. A fast unmarked trace algorithm cannot therefore be differentiated as though it had proved a fast marked trace algorithm.

## 6. The proposed speedup theorem and its missing hypothesis

### Theorem 6.1 — uniform marked-circuit transfer

Suppose a fixed deterministic construction, given N and the supplied root, generates a scalar arithmetic straight-line program for S_N(x,t) of size s(N). Count all generation, scalar preparation, addressing, and execution in O(s(N)+N). Require the program to be division-free in x,t, or regular at t=0 for every permitted input with every used denominator nonzero there.

Then F_N x has an exact, full-output, arbitrary-input algorithm using

    O(s(N)+N) sequential operations.                 (6.1)

The straightforward reverse-mode implementation uses O(s(N)+N) memory; no linear-memory improvement is asserted automatically.

**Proof.** Evaluate the circuit at (x,0), retain intermediate values, and propagate an adjoint backward from its scalar output. An addition needs two adjoint additions; a multiplication uses the stored operands to propagate two products and additions; division has a constant-size derivative rule when the denominator is nonzero. This obtains all t derivatives with constant-factor extra work, plus O(N) output initialization. Finally apply the phase and address correction (5.6). This is the standard arithmetic-circuit differentiation principle [P3], applied to the explicit scalar polynomial here. QED.

### Marked-cycle cancellation conjecture (not established)

There is a uniform exact scalar program for (5.4), exploiting the binary-tree Green decomposition and algebraic cancellations among marked cycles, with

    s(N)=O(N log(n+1))=O(N log log(N+2)).              (6.2)

Together with Theorem 6.1, this would prove O(N log log N) full Fourier computation. The stronger s(N)=O(N) statement would prove linear work.

**No program satisfying (6.2) is in this package.** The existing baseline for S computes Q^n x and takes the dot product with t, costing Theta(N log N). The conjecture is the unproved central algorithmic assertion, not a derived bound.

This reduction is close to an equivalence of computational problems: a fast Fourier program also yields a fast S program by reversing the output phase and permutation and taking a dot product. Therefore the reduction is not independent evidence that the target is easier. Its research value is the completely specified marked-cycle/determinant structure and the exact auxiliary tree and scalar-jet algorithms, which replace the preceding unspecified-parameter factorizations.

## 7. Three traps excluded by exact arguments

### 7.1 A large power is not a cheap graph edge

Equation (2.6) gives exactly N*2^t nonzero entries in Q^t for 0<=t<=n. Materializing powers to skip t stages expands the representation exponentially in t. Applying those powers as existing smaller Fourier banks restores the ordinary cost unless a genuinely different arithmetic circuit is constructed.

Also, e_0,Qe_0,...,Q^n e_0 have strictly nested supports {0,...,2^t-1}; a largest new support coordinate proves their linear independence. The minimal polynomial of Q therefore has degree at least n+1. A scalar polynomial of degree o(n) cannot simply replace Q^n. This is a restriction on this power representation, not a general Fourier lower bound.

### 7.2 Literal marked-cycle enumeration is quadratic

The n-step input-output paths of Q are the N^2 binary words of length 2n: n initial state bits followed by n emitted bits. A path contains n+1 consecutive n-bit windows. For a fixed pair of different window positions, equality imposes exactly n independent binary constraints, even when the windows overlap; there are N satisfying 2n-bit words.

By a union bound, at most binom(n+1,2)*N paths repeat a vertex. Therefore at least

    N^2-binom(n+1,2)*N                               (7.1)

paths have all n+1 vertices distinct (replace a negative lower bound by zero). Since n=log2 N, this remains asymptotically N^2. Eliminating self-intersecting walks alone does not make the marked problem linear.

At N=128, the exact test counts 14,592 simple paths out of 16,384, above the proved lower bound 12,800. This is a warning for determinant/pseudo-orbit enumeration, not a lower bound for arithmetic circuits with algebraic cancellations.

### 7.3 Sampling Green inverses introduces aliasing

For b>n, a primitive b-th root xi, and nonsingular evaluations,

    (1/b) sum_(j=0)^(b-1) xi^(-j*n) (I-a*xi^j Q)^(-1)
      = a^n Q^n (I-a^b Q^b)^(-1).                    (7.2)

The roots-of-unity filter keeps all powers congruent to n modulo b, not only Q^n. Dropping the extra inverse factor is an incorrect exactness argument. This is the same rational packet-filter phenomenon already recognized in the project's Green packet branch, not a new escape from it.

## 8. What is actually implemented and tested

Run from this directory:

    python verify.py --output RESULTS.json

No third-party package or old checkpoint code is needed. The verifier uses two prime fields and deterministic seeds. It separates the actual O(N log N) Fourier kernel, O(N) auxiliary methods, and deliberately expensive independent verification oracles.

The recorded eight groups pass:

| Verification | Actual coverage |
|---|---|
| Full explicit Fourier construction | 508 basis vectors and 54 fresh/structured test vectors; 66,716 outputs checked; sizes through 4,096 |
| Every small basis input | All basis vectors at N=2,4,8,16,32,64,128 over both fields |
| Partial-power formula and support | 54 exact matrix identities, 21,588 nonzero entries |
| Tree Green and Haar | 96 branch solves, 48 Haar apply/inverse pairs, 10 complete Schur matrix checks |
| Scalar closed-cycle data | 66 traces checked against dense powers, eight determinant jets checked by independent determinant interpolation |
| Marked trace derivative | 120 dual-number derivative coordinates on 16 fresh inputs; direct DFT is the independent target |
| Bordered determinant | 24 independent polynomial quotient checks and 24 exact marker-affinity checks |
| Rejections and path counts | Eight missing-phase failures, four resolvent-alias failures, four singular-parameter rejections, seven exhaustive simple-path counts |

The 4,096-point comparisons use a separately written ordinary even/odd recursive Fourier algorithm. Small fresh-vector checks use the direct DFT sum. Unlike the previous feedback positive controls, the new Q kernel is not supplied a dense Fourier matrix to define its coefficients.

The dense matrix products, determinant interpolation, Gaussian inverses, and dual-number traces in verify.py are **test oracles**, not parts of a claimed sub-N-log-N algorithm. There is no wall-clock FFT-library victory in these results. Finite-field agreement supports the identities; the symbolic proofs provide the all-dyadic statements.

## 9. Conditional arbitrary-length transfer and precision boundary

The explicit construction is dyadic. A hypothetical bound (6.2) for all dyadic lengths extends to every complex length M through a standard chirp convolution, provided the computational model supplies the needed roots and charges preparation.

Choose L to be the next power of two with L>=2M-1, so L<4M. Let eta be a primitive 2M-th root, omega_M=eta^2. The elementary identity

    omega_M^(j*k)=eta^(j^2)*eta^(k^2)*eta^(-(k-j)^2)

turns the length-M DFT into one zero-padded cyclic convolution of length L, two diagonal chirps, and output extraction. Three length-L transforms suffice using the inverse transform convention. Chirps can be generated in O(M) work by updating their first ratios geometrically. A supplied primitive (2ML)-th root has order <8M^2 and supplies both eta and the L-th root by integer powers. Root derivation and coefficients must be charged.

This is a conditional lifting identity, not a new all-length algorithm. A finite field containing an M-th root alone does not necessarily contain the needed roots. The fixed-prime experiments do not establish an unbounded finite-field or bit-complexity result.

No numerical-stability theorem is claimed for a future determinant/cancellation circuit. The actual Q baseline is phase-scaled and unitary after normalization, but scalar coefficients in an alternative circuit can be large and cancellations severe. Conditioning-dependent Fourier lower bounds [P4] have model hypotheses; neither ignoring them nor treating them as unrestricted impossibility is appropriate.

## 10. Novelty and current comparator

Constant-geometry Fourier algorithms [P1], quantum-graph periodic-orbit characteristic-polynomial methods [P2], Schur complements, Newton identities, and reverse-mode arithmetic-circuit differentiation [P3] are established. The preceding project also already used automatic differentiation for related-input expression graphs. None of those ingredients is claimed as newly invented here.

The project contribution in this note is the explicit combination of the fixed phase graph (2.1)-(2.5), its periodic-word determinant-jet evaluator, the exact weighted-Haar Green reduction, and the marked scalar coefficient target with precise cost and failure controls. Exact-term searches of the indexed master text did not locate this complete construction. That is **not** a proof of global originality; a literature-wide formula comparison or independent review has not been done.

The official OpenAI Math #130 documentation [P5] reports a separate uniform exact-complex DFT algorithm with work O(N(log N)^(1-10^-13)), a supplied chosen root, unrestricted coefficients, and charged scalar preparation. This note does not import that algorithm. Its stronger proposed O(N log log N) target remains unproved. It would be inaccurate to claim that sub-N-log-N exact Fourier work is unknown in every model, or that this package improves the published comparator.

## 11. Concrete continuation target

Keep the explicit Q_N, x,t hub, and phase correction fixed. The next legitimate success is a uniform scalar program for

    -[z^(n+2)] det(I-z W_N(x,t))/det(I-z Q_N)

whose total cost is o(N log N), ideally O(N log log N), with a direct proof of the program's exactness and complete coefficient/addressing charges. An equivalent success is a sub-N-log-N arithmetic evaluator for the first marked trace jet in (5.8).

Do not count a determinant node, matrix inverse, truncated polynomial operation, repeated Green solve, or Q^n application as one scalar instruction. Do not differentiate a program valid only after t has been specialized to zero. Do not reclassify the unmarked O(N) trace algorithm as an input-dependent Fourier algorithm.

The present result is a concrete exact construction and a mathematically specified proposed route. **The faster marked evaluator is not yet constructed.**

## Public references

[P1] G. Miel, *Constant Geometry Fast Fourier Transforms on Array Processors*, IEEE Transactions on Computers 42 (1993), 371-375. DOI 10.1109/12.210180. The publisher search record supports the constant-geometry prior-art comparison; no claim of comparing every formula in the full paper is made.

[P2] J. M. Harrison and T. Hudgins, *Periodic orbit evaluation of a spectral statistic of quantum graphs without the semiclassical limit*, arXiv:2101.00006v3 (29 March 2022). The HTML article discusses binary de Bruijn quantum graphs and characteristic-polynomial orbit expansions. Its result is not the full marked Fourier algorithm conjectured here.

[P3] W. Baur and V. Strassen, *The Complexity of Partial Derivatives*, Theoretical Computer Science 22 (1983), 317-330. DOI 10.1016/0304-3975(83)90110-X. The elementary reverse-mode proof needed for this note is included in Section 6; no uninspected theorem variant is required.

[P4] N. Ailon, *An n log n Lower Bound for Fourier Transform Computation in the Well Conditioned Model*, arXiv:1403.1307v5 (2014).

[P5] OpenAI Math, `lean/docs/130.md`, *Exact Fourier transforms below n log n*, public statement checked 10 October 2026. Repository: github.com/openai/math. Section "Scope" distinguishes subsequential and uniform formalizations and their computational models.
