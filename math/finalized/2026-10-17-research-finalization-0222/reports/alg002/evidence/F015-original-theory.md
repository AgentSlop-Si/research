# Certified growing-fiber Fourier theory

**Date:** October 10, 2026.  
**Status:** A proved, implemented **structured-input** exact Fourier algorithm with a growing-parameter cost bound. **Not an unrestricted exact sub-N log N algorithm.** The contribution is new relative to the particular project fiber/aggregate-cost statements compared below; external mathematical priority is unverified. Prony, Berlekamp–Massey, FFT pruning, rational interpolation, and Cooley–Tukey are established ingredients.

## Executive result

Let N=2^k>=4, Q=2^floor(k/2), M=N/Q, and 1<=b<=M/2. Suppose each of the Q strided length-M fibers of a fresh input (or of its explicitly specified Green preconditioned version) has at most b Fourier modes. Their supports, coefficients and recurrences are **not supplied**.

The algorithm reads the input, discovers and exactly verifies the modes, and returns all N explicit Fourier outputs in

    O(N log(b+2) + Q b^2) = O(N log(b+2) + sqrt(N) b^2)

unit-cost exact field and logarithmic-word operations. It uses O(N) space and includes root tables, recognition, zero tests, index work and output writes. On inputs violating the fiber condition, it rejects within the same bound. An explicitly invoked full-FFT fallback gives a correct result on all inputs but retains O(N log N) worst-case cost for the polylogarithmic choices below.

Taking b=ceil((log_2 N)^c) for any fixed c>0, with a direct small-size fallback where b>M/2, gives

    O_c(N log log N)

on the stated class. Fixed b gives O_b(N). More generally b=N^o(1) yields o(N log N) for this class. These are **actual algorithms**, not consequences of an unconstructed fast operator.

**Aggregate-budget extension.** The cap on individual fibers can be removed. For a supplied total budget K0=O(Q*(log N)^c), a second implemented algorithm accepts exactly inputs with sum_t r_t<=K0 and computes the complete transform in O_c(N log log N), even if some fibers have all M modes. A failed short recovery certifies a heavy fiber, whose full M-point transform is amortized against the total budget. Section 9 proves the complete charge, including a final over-budget fiber on rejection.

The main advance over the compared project method is replacing mode-by-mode M*r work in root search and verification, and Q*K work in global synthesis, with support-pruned transforms. This allows the internal mode count to grow while the complete input and complete output remain dense.

## 1. Exact model and conventions

Work over a field E with a supplied primitive N-th root w and char(E) not dividing N. Count each field addition, subtraction, multiplication and inversion as one operation; count exact zero tests and O(log N)-bit indexing as word operations. The root w itself is supplied; computing [1,w,...,w^(N-1)] costs O(N) and is included. No claim is made about constructing a suitable finite field or root, floating-point equality tests, numerical stability, arbitrary-precision bit complexity, or practical FFT-library speed.

Our unnormalized forward transform is

    F_w(x)[k] = sum_{j=0}^{N-1} x[j] w^(j*k).

Choosing w=exp(-2*pi*i/N) gives the usual negative-exponent convention.

Write eta=w^Q and theta=w^M. The raw strided fiber is

    y_t[u]=x[t+Q*u],       0<=t<Q, 0<=u<M.

Every fiber has a unique expansion

    y_t[u]=sum_{h in H_t} a_(t,h) eta^(-h*u),

where nonzero amplitudes are retained. Let r_t=|H_t|, K=sum_t r_t, and

    kappa_h = #{t : h in H_t}.

Thus sum_h kappa_h=K. The promise is r_t<=b, not a sparse raw input, a sparse final spectrum, a low-rank reshaped matrix, or known mode locations.

## 2. The pruning lemma and what it costs

**Lemma.** A length-L dyadic Fourier transform of a vector with s known nonzero positions can be evaluated with all L outputs in

    O(L[1+log(s+1)])

field/word operations and O(L) workspace, including writing zeros for s=0.

**Proof.** Recurse by input parity and omit empty subtrees. At depth d at most min(2^d,s) subproblems are active, each of length L/2^d. Their combine work is O(L min(1,s/2^d)). The sum over d up to log_2 L is O(L[1+log(s+1)]). Partitioning the sparse lists, copying and indexing obey the same asymptotic bound (or O(s log L), which it dominates). Depth-first evaluation retains O(L) live data. The algorithm does not build a dense transform matrix. QED.

This is classical FFT pruning, not claimed as novel. It is used in **three different places** in the construction, including places where the old project implementation scanned the roots or modes individually.

## 3. Prefix identification without trusting a prefix

For one fiber with <=b modes, read its first 2b samples and run the ordinary quadratic Berlekamp–Massey recurrence algorithm. It returns

    C(z)=1+c_1 z+...+c_r z^r,

corresponding to

    y[u]+c_1 y[u-1]+...+c_r y[u-r]=0.

On a true r-mode fiber, with lambda_h=eta^(-h),

    C(z)=product_(h in H)(1-lambda_h*z).

**Why 2b samples suffice under the promise.** For r distinct nonzero nodes and nonzero amplitudes, the r-by-r Hankel matrix is

    [y[i+j]] = V diag(a_h) V^T,

where V[i,h]=lambda_h^i is invertible Vandermonde. Its determinant is nonzero. The r-term recurrence exists, and 2r samples determine it; the 2b prefix is sufficient. This includes exact cancellations in initial samples and is not a generic-position argument.

The prefix algorithm costs O(b^2). Crucially, a recurrence fitting a prefix does **not** certify an arbitrary input. The later full-length reconstruction comparison is mandatory. If the prefix complexity exceeds b, reject. If r=0, check that the entire fiber is zero.

## 4. Find unknown roots on the Fourier grid by pruning

The unknown frequencies h are exactly those for which

    C(eta^h)=0.

The vector (C(eta^h)) for all h is the length-M DFT of the zero-padded coefficient vector (1,c_1,...,c_r). This vector has at most r+1 nonzeros.

The pruning lemma evaluates all M grid nodes in

    O(M[1+log(r+2)]),

rather than O(M*r) separate Horner evaluations. Collect the exact zero positions with one O(M) scan. If there are not exactly r distinct grid roots, reject.

No algebraic root-finding oracle, discrete logarithm, nonuniform lookup table, uncharged root search or full dense-input M-point transform is used.

## 5. Recover amplitudes in O(r^2)

Let Y(z)=sum_(u>=0) y[u] z^u and form

    A(z) = C(z) (sum_(u=0)^(r-1) y[u] z^u) mod z^r.

The true rational generating function is

    Y(z)=sum_h a_h/(1-lambda_h*z)=A(z)/C(z).

At z_h=lambda_h^(-1)=eta^h,

    C'(z_h)=-lambda_h product_(g!=h)(1-lambda_g*z_h).

Therefore

    a_h = -lambda_h A(z_h)/C'(z_h).

The denominator is nonzero because the roots are distinct. Form A by quadratic truncated multiplication and evaluate A,C' at the r roots by Horner: total O(r^2) arithmetic, O(r) storage. The implementation rejects any zero denominator or zero recovered amplitude that contradicts the candidate degree.

This rational/Vandermonde identity is established mathematics. Its formula is included so the amplitude recovery is executable rather than an unexplained linear-system oracle.

## 6. Full raw-input certification is also pruned

Synthesize the entire candidate fiber using the inverse-root transform:

    y_candidate[u]=sum_h a_h eta^(-h*u).

The amplitude vector has r known nonzero locations, so this costs O(M[1+log(r+1)]), not O(M*r). Compare all M coordinates exactly with the original fiber.

**Soundness.** Acceptance explicitly exhibits and verifies a representation using <=b distinct Fourier characters. Thus a violating fiber cannot pass.

**Completeness.** Under the promise, the prefix recurrence, grid roots and amplitude formula recover its unique representation and the full comparison passes.

The verifier includes altered-last-coordinate examples whose first 2b samples still fit the old recurrence. Every such example is rejected. Prefix fitting alone would falsely accept these inputs.

## 7. Fuse equal frequency labels, then prune in the other direction

Write a final frequency as k=h+M*v. Fourier orthogonality gives

    F_w(x)[h+M*v]
      = M sum_(t=0)^(Q-1) a_(t,h) w^(h*t) theta^(v*t).

For each h build the sparse length-Q vector

    B_h[t]=a_(t,h) w^(h*t).

Compute its length-Q DFT by pruning, then multiply by M and place the results at h+M*v. This is the project's frequency-label union operation: all fibers contributing to one residue h share one evaluation graph.

The h-th vector has kappa_h nonzeros. All output synthesis costs

    O(N + Q sum_h log(kappa_h+1)).

By concavity of log and sum_h kappa_h=K,

    Q sum_h log(kappa_h+1)
       <= N log(1+K/M).

This replaces the compared implementation's O(Q*K) direct mode-to-output streams. An absent residue h produces Q explicit zeros, not a delayed query object.

## 8. Main theorem: charged total complexity

The costs are:

| Component | Charged upper bound |
|---|---|
| Read input, roots, fiber indexing, final writes | O(N) |
| Q prefix recurrence computations | O(Q*b^2) |
| All root-grid searches | O(M sum_t[1+log(r_t+2)]) |
| All amplitude solves | O(sum_t r_t^2) <= O(Q*b^2) |
| All full raw-fiber comparisons and synthesis | O(M sum_t[1+log(r_t+1)]) |
| Label union, phases, sparse output synthesis | O(N+K+Q sum_h log(kappa_h+1)) |

For accepted inputs this yields the profile-sensitive estimate

    O(N + Q*b^2
        + N log(2+K/Q)
        + N log(1+K/M)).

A more refined successful-prefix accounting can replace Q*b^2 by O(Q*b+b*K); the headline theorem deliberately retains the simpler conservative cap.

Since K<=Q*b and Q<=M<=2Q, the total is

    O(N log(b+2)+Q*b^2).

Rejected candidates also stay within this budget: stop when a fiber fails, and every attempted degree is <=b. No unbounded search is permitted.

Only root tables, input/output vectors, one current fiber workspace, recurrence buffers and K<=N/2 mode records are required: O(N) memory. All parameter setup is uniform.

### Corollaries

For fixed c>0, b=ceil((log_2 N)^c), eventually b<=M/2 and

    Q*b^2=O(sqrt(N)*(log N)^(2c))=o(N).

Thus the exact recognized transform costs O_c(N log log N). Handle finitely many small sizes by an ordinary FFT; its cost is covered by a c-dependent constant.

For any b=N^o(1), log b=o(log N) and Q*b^2=N^(1/2+o(1))=o(N), yielding o(N log N) on the recognized class. In particular b=exp(sqrt(log N)) yields O(N sqrt(log N)).

Fixed b gives O_b(N). For an all-input implementation set b from N, not from an oracle, and perform an ordinary full FFT only after certified rejection. This preserves correctness on every input, **not** a sub-NlogN worst-case bound.

## 9. Aggregate-budget theorem: permit arbitrarily heavy fibers

The individual cap r_t<=b is not necessary for an O(N log log N) total-budget result. Let K0 in [0,N] be supplied as a public complexity budget, not an oracle for the actual support. Define

    ell=log_2 M,
    a=max(1,ceil(K0/Q)),
    B=min(M/2, a*ell).

For each fiber, run the exact light-fiber recognizer with threshold B. If it rejects, compute that fiber's full M-point DFT and divide by M to obtain all its amplitudes. This is a **charged ordinary transform**, not a claimed new primitive. Because the light recognizer is complete, rejection certifies r_t>B. Maintain the total discovered modes and reject the entire input immediately when it exceeds K0.

### Heavy-fiber charging

Every completed heavy fiber consumes at least B+1 modes. On success,

    number_of_heavy_fibers <= floor(K0/(B+1)).

On rejection, one final over-budget fiber can have been examined, giving the bound

    number_of_heavy_fibers <= floor(K0/(B+1))+1.

All those ordinary transforms together cost

    O(M*ell*[1+K0/B]).

This extra +1 is essential: even the first fiber can exceed the entire budget. The rejection proof does not charge unavailable future modes as though they fit K0.

The light-recognizer attempts cost at most O(N log(B+2)+Q*B^2). Accepted synthesis still costs O(N[1+log(1+K0/M)]). Therefore a complete all-input success-or-rejection bound is

    O(N log(B+2)+Q*B^2
      + M*ell*(1+K0/B)
      + N log(1+K0/M)).

Whenever a*ell<=M/2, B=a*ell and K0<=a*Q, so the heavy term is O(N+M*ell)=O(N). The bound simplifies to

    O(N log(a*ell+2)+Q*a^2*ell^2).

For K0=O(Q*(log N)^c), fixed c>=0, eventually a*ell<=M/2 and Q*a^2*ell^2=o(N). Hence

    O_c(N log log N)

for exact raw-input recognition and full outputs. The maximum r_t may equal M: no per-fiber sparsity cap remains in this aggregate theorem. A zero budget is handled correctly by the same implementation; it accepts only the zero signal (or zero Green residual).

The finite-size min(M/2,...) is included in the implementation. The unsimplified bound applies at every supported size. Constants needed to cover small lengths may depend on c; the asymptotic simplification is not a practical crossover guarantee.

For an all-input result use an ordinary full N-point FFT after total-budget rejection. This still has O(N log N) worst-case complexity for the polylogarithmic-budget schedules. The accepted family is the promised internal-mode-budget class, not every vector.

### Exact implemented evidence

`certified_aggregate_fft` implements this algorithm. Its tests include one completely dense M-mode fiber alongside many two-mode fibers, both directly and behind the Green preconditioner. They also lower K0 by one to force an over-budget rejection, check the heavy-fiber inequality including its +1, and compare fallback outputs to an independent FFT.

The aggregate family with K0=Q*polylog(N) contains the earlier K0=O(Q) aggregate regime and allows larger total internal support. The earlier O(N) algorithm remains better for a constant total average; this new theorem improves the growing-budget regime rather than claiming to improve every parameter point. The simpler per-fiber-cap algorithm is often substantially cheaper at finite sizes; recorded arithmetic profiles use that variant, not the aggregate variant.

## 10. This includes dense input, full matrix rank, dense output

Let N=M^2 and 1<=b<M. Give fiber t the modes

    H_t={t,t+1,...,t+b-1} mod M,

with a_(t,t)=2b and each other amplitude equal to 1. The coefficient matrix is 2b*I plus b-1 cyclic-permutation matrices. Over C it is invertible because the latter sum has norm <=b-1<2b. Multiplying it by the invertible M-point Fourier matrix produces the Q-by-M raw fiber matrix, so that matrix has full rank M.

Every raw coordinate has magnitude at least 2b-(b-1)=b+1 by the reverse triangle inequality. In every output residue, the dominant t=h term has amplitude 2b and at most b-1 other terms have unit magnitude. Thus every full Fourier output has magnitude at least M(b+1).

Consequently the family has:

- no zero input coordinates;
- no zero final Fourier coefficients;
- maximal rank after the balanced reshaping;
- K=M*b internal modes, with b growing as log N or faster.

This is not merely the usual promise that the final Fourier spectrum is sparse. It is a promise about a **sparse intermediate bank**.

The strict dominance also permits continuous perturbations of all active amplitudes, preserving density and full rank. Nevertheless this family has only at most Q*b free complex amplitudes for fixed support, not N generic degrees of freedom.

Finite fields have no such norm ordering: 2b need not prevent modular cancellation. The exact modular dense controls select a tested diagonal coefficient explicitly. At p=65537,N=16,diagonal=4 one output cancels; diagonal=5 yields the dense control. This is not an algorithm error and the characteristic-zero norm argument is never imported into finite fields.

## 11. Fuse the project's Green preconditioner without hiding FFT work

Define S e_j=e_(j+1 mod N), D=diag(w^j),

    P=7I+S+2D^-1,    L=7I+D+2S.

The elementary identities F S=D F and F D^-1=S F prove

    F P=L F.

For a fresh input x, form r=P x in O(N). Apply the certified fiber algorithm to r. If accepted, solve

    L y=F r

by one cyclic first-order recurrence and return y=F x. This extends the class to inputs whose **Green residual** has the sparse-fiber property. It does not claim a generic input gets compressed.

Over C, ||P-7I||_2,||L-7I||_2<=3. Both are invertible, singular values lie in [4,10], and their 2-norm condition numbers are at most 2.5. This bounds only the endpoint operators, not the stability of Prony recognition.

A cyclic solve of (diag(d)+beta*S)y=x uses

    y_j=a_j*y_(j-1)+b_j,
    a_j=-beta/d_j, b_j=x_j/d_j,

composes one scalar affine recurrence, closes its loop with one division, then scans forward. All work is O(N). In finite fields the implementation checks the actual diagonal and closure denominators; inappropriate parameter choices raise an error. No complex conditioning estimate is substituted for an exact finite-field denominator check.

The optional generator x=P^-1 r is used only to prepare independent test inputs. Generation is not part of the measured raw-input transform, nor is a previously computed spectrum supplied to the algorithm.

## 12. Why this does not imply a universal faster FFT

For a fixed support pattern (H_t), the accepted vectors form a linear subspace of C^N of dimension K<=Q*b. There are finitely many such patterns. Applying any fixed invertible P preserves their dimensions.

**Finite-bank obstruction.** If Q*b<N, no finite collection of fixed invertible preconditioners can make every complex input satisfy the b-mode-per-fiber condition. The accepted set is a finite union of proper linear subspaces, and cannot cover C^N.

For the aggregate variant, replace Q*b by K0 in this argument. More generally, adding a correction in any fixed d-dimensional linear space raises the dimension by at most d. A finite bank of such schemes still cannot cover C^N if K0+d<N. This statement concerns fixed linear correction spaces; it is not an obstruction to every possible nonlinear input-dependent parameterization.

This is not a lower bound on arbitrary arithmetic circuits. It rules out the specific attempted universal extension: 'try enough fixed cheap Green gauges, and every input will become polylogarithmically sparse internally.' For algebraically generic input, every intermediate Fourier coordinate is nonzero in each fixed frame, so each r_t=M.

An all-input exact sub-NlogN theory must avoid this fixed low-dimensional representation restriction. Nothing here proves a coverage theorem for arbitrary input-dependent nonlinear parameter families, and their identification/evaluation costs cannot be omitted.

## 13. Relation to the earlier project results

The directly compared `Dyadic Fourier–Green Cut Spectra and Aggregate-Sparse Fiber FFTs`, Theorem E, gives O(N+M*K0+Q*K0+K0^2) and an exact O(N) regime when K0=O(Q). The older bounded-fiber scheme has a stated O(r*N+Q*r^2+r*Q^2+N) ledger. The new theorem changes the r-dependent arithmetic, not just the name of the same recurrence:

1. identify from a 2b prefix, then separately verify the entire input;
2. find grid roots using a pruned transform of a short recurrence polynomial;
3. verify fibers with a pruned synthesis;
4. perform one pruned synthesis for each united frequency residue.

For K=Q*b with b=log N, the older mode-streaming implementation has N*b-scale terms; the present certified implementation has N*log b plus lower-order Q*b^2. This is a comparison of **documented algorithms and upper bounds**, not a lower bound against all possible versions of the old method.

The **cap-only** class with max r_t<=b is not a superset of every aggregate-budget example: a very heavy exceptional fiber can violate this cap. Conversely, the growing uniform-rank construction permits total K=Q*polylog N, beyond the earlier linear aggregate regime. The cap-only classes overlap and have complementary advantages. The separately proved aggregate algorithm in Section 9 removes that limitation and permits unrestricted individual fiber weights at the stated total budget.

The previous mass-contraction, annihilator-feedback and marked-cycle proposals still have unproved all-input construction/evaluation steps. This algorithm does not solve those steps; it instead delivers a complete positive result in the structured branch of the same project.

## 14. Evidence and explicit limits

See RESULTS.json for authoritative exact counts. Tests use GF(65537) and GF(998244353) with supplied primitive roots, plus an independently implemented direct DFT / dense iterative FFT. They include all small atomic fiber-coordinate inputs, deliberately forged prefixes, generic dense rejection, late corruption, Green conjugation, and dense/full-rank constructions.

The finite operation profiles are **not** a wall-clock FFTW comparison. At N=262144,b=18 the current implementation uses 7,516,160 counted field operations versus 7,340,032 for the supplied full-radix baseline: about 2.4% MORE. Its asymptotic structured-input bound is lower, but no finite arithmetic crossover or practical speed advantage was demonstrated in these profiles. Inversions are counted as field primitives; Python big-integer costs are not constant in a bit model.

External literature already contains hybrid Fourier–Prony methods and sparse FFT tree exploration. A limited source search cannot certify publication novelty. Independent proof/code review and a detailed literature comparison remain necessary. No unrestricted FFT breakthrough, generic matrix lower bound, numerical stability theorem or integer-multiplication bound is claimed.

## References

- User project: `Dyadic Fourier–Green Cut Spectra and Aggregate-Sparse Fiber FFTs`, Theorem E (THEOREMS(2).md, inspected October 10, 2026).
- User project: Hero #17 fiber/graph-union sources and the master v17 archive; Hero #1 Green residual factorization and sparse-rational checkpoints.
- FFTW, *Pruned FFTs*: https://fftw.org/pruned.html . O(N log K) support/output pruning is established.
- M. Briani, A. Cuyt, W.-s. Lee, *A hybrid Fourier-Prony method* (2017): https://arxiv.org/abs/1706.04520 . The broad Fourier/Prony hybrid idea is prior art.
- K. Bringmann et al., *Traversing the FFT Computation Tree for Dimension-Independent Sparse Fourier Transforms* (2021): https://arxiv.org/abs/2107.07347 . Prior sparse FFT tree-based recovery and its limitations.

## Reproduction

    python verify.py

The module is standard-library-only. `certified_fiber_fft(...,fallback=False)` returns an exact accepted output or explicit rejection. `fallback=True` computes the ordinary exact full FFT after rejection, charging its work. All output vectors are explicit Python lists; no symbolic or compressed output is being substituted for the problem.
