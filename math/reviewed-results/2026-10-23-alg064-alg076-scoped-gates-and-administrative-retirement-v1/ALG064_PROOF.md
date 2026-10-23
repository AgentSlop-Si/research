# ALG-064: guarded noise-stable full-tail coefficient discovery

23 October 2026. Candidate bounded gate, pending independent review. **ALG-064 remains TO RESEARCH, priority 42.** No novelty, practical-speed, or whole-owner closure is proposed.

## 1. What is new, and what is not

The exact root-free recurrence transform, capped exact synthesis, supplied-coefficient residual-aware numerical evaluator, exact-data coefficient bridge, and certified all-length FFT fallback were already accepted. They are not new results here. The current owner explicitly retains stable/noisy recurrence recognition and conditioning.

This gate supplies a different coefficient proposal: fit **every tail equation by least squares**, compute a rational conditioning lower certificate from the observed data, and verify the complete rounded residual before allowing the existing numerical evaluator. The proposal need not satisfy any recurrence exactly. It comes with a proved perturbation bound relative to an externally specified nearby exact recurrence model, an observable conditional bound, and an explicit small-noise sufficient condition for fast-branch acceptance.

The implementation is an **exact rational reference for noise-stable discovery from dyadic observations**. It is not a backward-stable floating-point implementation of normal equations. It does not certify that an unknown clean signal exists, identify its minimal order, denoise it, or stably reconstruct its entire trajectory by iterating the fitted recurrence. Acceptance certifies the DFT of the actual observed vector through the inherited residual theorem, not the DFT of an inferred clean signal.

The fresh module terminates at the coefficient/certificate interface. It does not execute a complete DFT backend. The end-to-end statement below is a mathematical composition with explicitly charged accepted backends; no historical code was executed.

## 2. Source and stopping-condition check

Fresh main was `ea78d5c259d99c2907bc822fcc4b33f2a405593d`. The native ALG-064 owner row was reread in full on 23 October; it still requests stable/noisy recognition, conditioning, non-dyadic input, integration, resource-limited certification and production work while parking the accepted fallback.

Read dependencies:

1. [Original Phase23 theorem](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/archive/objects/d3/d32912d6f37d714b429fd21f1faaff1457f75c53a87ce91288ab3abe0073180b__THEOREM.md) and [independent Phase23 audit](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/archive/objects/c0/c074b19dd40f6a50a5a4a3b91b0e447824f47e90206032d4c88dc8673a723817__13_PHASE23_AUDIT.md), especially audit Sections 6–7.
2. [Accepted residual-aware numerical evaluator](https://github.com/AgentSlop-Si/research/blob/5f76c073d35877c12d4d57be1e5e0cb3321dfa35/math/finalized/2026-10-17-research-finalization-0110/reports/alg064/REPORT.md), Sections 2–6. Its supplied-coefficient gate is already complete.
3. [Accepted exact-data bridge](https://github.com/AgentSlop-Si/research/blob/511689fb34ffa88921b3d2a0dc801e048b49dce2/math/finalized/2026-10-17-resumed-mathematics-0916/reports/alg064/REPORT.md), Sections 3–6. It explicitly disclaims stable inference from noisy observations.
4. [Accepted all-length FFT fallback](https://github.com/AgentSlop-Si/research/blob/b1093eb6705fbef4e6dfcc0e29e69f6a5d31e21e/math/finalized/2026-10-18-fifth-cycle-six-results/certified_fft/candidate/REPORT.md) and [independent review](https://github.com/AgentSlop-Si/research/blob/b1093eb6705fbef4e6dfcc0e29e69f6a5d31e21e/math/finalized/2026-10-18-fifth-cycle-six-results/certified_fft/review/REVIEW.md). Their scope does not accept new discovery or noisy recognition.

Only the bounded discovery-to-certificate gate defined below is proposed complete. The old all-size proofs are dependencies, not rediscoveries or fresh implementation replay.

## 3. Input and exact all-tail proposal

Take N>L, L in {1,2}, a raw complex dyadic vector x, and rational absolute tolerance 0<epsilon<=1. The target remains the unnormalized positive-exponent DFT of x. L is a **declared span**, distinct from the eventual connection-polynomial degree. For L=2 a full-column-rank proposal requires N>=4. N=1, zero vectors, invalid dimensions, or rank-deficient proposals can use explicit direct/zero handling or the paid fallback; rank refusal is not nonmembership.

Let m=N-L. Form the m-by-L complex lag matrix and target:

    A_x[j,i] = x_(L+j-i),   0<=j<m, 1<=i<=L,
    b_x[j]   = x_(L+j).

A connection is (1,c_1,...,c_L); its full tail defect is r=b_x+A_x c. Compute

    G=A_x* A_x,  w=-A_x* b_x.

All sums use every tail row, not the first four samples or a sampled prefix. If rank(G)<L, return RANK_DEFICIENT for this proposal. Otherwise set c=G^(-1)w exactly. For L=1 this is one scalar division. For L=2 it is the explicit 2-by-2 Hermitian inverse. The implementation recomputes all r_j and checks A_x* r=0 exactly.

For any candidate d,

    ||b_x+A_x d||_2^2 = ||r||_2^2 + ||A_x(d-c)||_2^2.

The cross term vanishes by the normal equations. Thus the proposal is the unique full-tail least-squares minimizer. This is ordinary classical least squares, not a new recognition theorem. The exact rational arithmetic avoids normal-equation roundoff; it does not justify performing the same operations in ordinary floating point.

## 4. Conditioning is measured, not supplied as an oracle

When L=1 put gamma=G_11. When L=2 put

    gamma=det(G)/tr(G).

For positive eigenvalues lambda_min<=lambda_max,

    lambda_min/2 <= det(G)/tr(G) <= lambda_min.

Compute a positive dyadic s satisfying s^2<=gamma<4s^2, by integer bit-length estimates and exact rational comparisons. No eigensolver, square root, fitted characteristic roots, or assumed spectral gap is used. Then

    sigma_min(A_x)>=s,
    ||A_x||_2^2<=tr(G),
    kappa_2(A_x)^2<=tr(G)/s^2.

All quantities are returned. The bound can be pessimistic by a constant factor. It can be arbitrarily bad; the method makes no uniform conditioning promise. A caller with a declared amplification or condition budget can reject it by these exact comparisons and still pay the attempted discovery cost. The reference returns the certificate without inventing an application-specific threshold.

The coefficient transform c(x) is continuous on each full-column-rank stratum. The following explicit inequalities state exactly what noise stability means here.

## 5. Noise stability and its logical limits

### 5.1 Conditional proximity to a true recurrence

Suppose an independently meaningful signal y satisfies a declared-span-L recurrence with coefficients c_star, and x=y+e with ||e||_2<=eta. This is an **external premise**, not established by the fit. Truncating and shifting e gives

    ||A_x-A_y||_2 <= sqrt(L) eta,
    ||b_x-b_y||_2 <= eta.

Since b_y+A_y c_star=0 and c is the observed-data least-squares solution,

    c-c_star = -A_x^+[(b_x-b_y)+(A_x-A_y)c_star].

Therefore the computed lower certificate s proves

    ||c-c_star||_2 <= eta(1+sqrt(L)||c_star||_2)/s.        (1)

This result does not require the unknown y matrix to be well-conditioned once the observed x certificate is available. For a purely rational conservative implementation, sqrt(L)<=L and ||v||_2<=sum_i nu(v_i), where nu(z)=|Re z|+|Im z|. The module returns

    eta[1+L sum_i nu(c_star_i)]/s.

It does not estimate eta from the residual.

### 5.2 Observable conditional bound

Let alpha=eta/s. If sqrt(L)alpha<1, replace ||c_star||_2 by ||c||_2+||c-c_star||_2 in (1) and solve:

    ||c-c_star||_2
      <= alpha(1+sqrt(L)||c||_2)/(1-sqrt(L)alpha).       (2)

The reference uses the stronger rational guard L alpha<1 and returns

    alpha[1+L sum_i nu(c_i)]/(1-L alpha).

This bounds proximity to **every** true span-L recurrence coefficient vector whose signal lies within the externally supplied noise ball. It neither proves that this set is nonempty nor determines a clean signal. If the guard fails, it returns no such bound, rather than a stability claim.

### 5.3 Stability of the proposal map without a clean-model assertion

For another observation x'=x+e, let c',A',b',s' denote its full-rank proposal and certificate. Set r=b_x+A_x c. Since A_x* r=0,

    ||c'-c||_2
      <= sqrt(L)eta ||r||_2/(s')^2
         + eta(1+sqrt(L)||c||_2)/s'.                  (3)

Indeed the new residual at c is r+f, with f=(b'-b_x)+(A'-A_x)c. The normal equations give c'-c=-(A')^+(r+f). For the r term, (A')*r=(A'-A_x)*r, yielding the first term; the f term yields the second. Thus no unknown clean signal is needed for a local perturbation inequality, but conditioning and the full residual are explicitly paid/measured.

### 5.4 No stable trajectory reconstruction follows

For the fixed recurrence multiplier 2, choose x_0=0 and x_j=delta 2^(j-1) for j>=1. Its full first-order defect has l1 mass delta, but iteration from x_0 yields the zero trajectory, with final discrepancy delta 2^(N-2). Small defect therefore does not supply input-uniform closeness to the fitted trajectory initialized at the first observation. No root-modulus/growth assumptions or denoising theorem are smuggled into (1)–(3).

## 6. New noisy coefficient bridge into the accepted evaluator

Compute exact S=sum_j nu(x_j) and R0=sum_j nu(r_j) for the rational least-squares coefficients. Set tau=(2N)^(-L). Choose a dyadic grid h=2^(-b_c), at least as fine as the raw input grid, with

    h <= epsilon tau/[16 L(S+1)].

Round each real/imaginary part of c_i to nearest h, keeping c_0=1. Each complex coefficient changes by nu-distance at most h. Recompute the **entire** rounded tail defect e_j exactly; define R=sum nu(e_j). Then

    R <= R0+L h S <= R0+epsilon tau/16.                (4)

A sufficient, but not necessary, discovery-success condition is R0<=epsilon tau/16. The actual acceptance test is precisely R<=epsilon tau/8. The module can therefore accept some proposals failing the sufficient test. Rank or residual refusal does not prove that no other coefficient choice or representation works.

On acceptance, construct the declared-span-L boundary polynomial A_boundary exactly using the accepted convolution identity. Keep the rounded degree r<=L separate. The inherited evaluator applies with the conservative threshold tau=(2N)^(-L), which is no larger than its degree-r threshold. It computes denominator bounds from certified Fourier-node evaluations, has at most r suspect bins, and evaluates those bins directly. **No denominator lower bound is assumed as an oracle.** Every accepted output approximates the DFT of x to the inherited absolute epsilon tolerance.

The rounded coefficient vector has an additional Euclidean error at most sqrt(L)h, so either (1) or (2) can be extended to it by adding that term. This coefficient-proximity bound is separate from the actual-data output certificate (4).

### Nonvacuous sufficient noisy-model class

Under the model premise in Section 5, least-squares optimality gives

    ||r||_2 <= eta(1+sqrt(L)||c_star||_2),
    R0 <= sqrt(2m) eta(1+sqrt(L)||c_star||_2).          (5)

Hence full observed rank together with

    sqrt(2m) eta(1+sqrt(L)||c_star||_2)
        <= epsilon (2N)^(-L)/16                     (6)

guarantees coefficient-certificate acceptance after rounding. If the clean lag matrix has sigma_min(A_y)>=sigma_star, Weyl's elementary singular-value bound gives full observed rank whenever sqrt(L)eta<sigma_star. The reference does not claim to know either clean condition or noise level; (6) is a proved completeness class, whereas actual acceptance uses only computed R.

For fixed L=2 and fixed coefficient magnitudes, (6) permits noise of order epsilon N^(-5/2), not a fixed macroscopic noise floor. This conservative restriction is important. The method is not a general noisy sparse-Fourier recovery result, statistical consistency result, relative-error transform, or practical robustness benchmark. It closes only the stated certificate-producing proposal gate.

## 7. Complete costs and the finite-word boundary

Let raw real/imaginary entries share denominator 2^b and have integer numerators of at most B bits after alignment; let E be actual encoded input/tolerance length. All of b, B, and the encoding cost are charged. L<=2 is fixed throughout.

Accumulating G and w takes O(N) exact operations. Their integer numerator length after clearing denominator 2^(2b) is H=O(B+log(N+1)). The 2-by-2 determinant, inverse numerators, and reduced rational coefficients have O(H) bits. Arbitrarily small nonzero determinants are not treated as unit-cost inverses. Recomputed rational residuals have a common coefficient denominator times 2^b; all stored numerator/denominator lengths remain O(H+b). The conditioning certificate and dyadic square-root bracket require exact comparisons on this width. Gram accumulation can stream in O(1) auxiliary words; retaining x, residuals, and final outputs uses O(N) words.

Coefficient rounding adds b_c bits with

    b_c=O(b+log(1/epsilon)+L log(2N)+log(S+1)).

Let T also include the actual rational tolerance encoding length. A conservative width for discovery, squared comparisons, residuals, boundary formation, rounding and certificate preparation is

    W=O(B+b+log(N+1)+b_c+T).

With A(W) charging addition, multiplication, integer division, gcd/reduction, copying and comparison on O(W)-bit operands, the new discovery-and-certificate gate costs

    O(E+(N+b_c+W) A(W)) bit operations,

and O(NW) bits of storage for the materialized reference. Bit-length bracketing or grid-selection loops are included in the W+b_c term. Rational arithmetic reductions are not free. Testing both L=1 and L=2 changes only constants and retains both invoices. A rank/residual failure still pays all performed work.

For successful full DFT composition, add the accepted node construction and finite-precision evaluator bills without erasing predecessor work. With L<=2, one explicit previously accepted realization has:

- certified rational node construction: O((p+1)^2+N(p+1)) exact operations at the predecessor's stated root width H_root;
- evaluator, normalization convention unchanged: O(N) arithmetic at the predecessor's stated finite width W_eval, including at most two direct N-term suspect evaluations, all denominator classification/divisions, all residual verification, and all N writes;
- precision p satisfying all predecessor inequalities, including p>=2b_c and the actual coefficient/boundary magnitudes.

Equivalently the cumulative successful bit bill is the new discovery bill plus C_roots(N,p)+O(N[M(W_eval)+D(W_eval)]) and actual output transport. It is **not** O(N) total bit time: conservative paid root construction and precision dominate in some regimes. On refusal add the accepted certified Bluestein/radix-2 fallback's complete root, kernel, bit/storage, invoice-processing and output bill. Its O(N log N) kernel arithmetic is not a new overall bit bound or a speedup result here.

The new reference does not call those historical backends, nor claim to validate their production integration. Composing their mathematical contracts is sound because the new packet supplies exactly the admitted raw dyadic input, declared span, rounded coefficients, boundary data, certified residual budget and complete discovery charge. A future actual adapter must preserve these fields and invoice handling.

## 8. Classical attribution and floating-point caution

The least-squares objective, normal equations, orthogonal residual and pseudoinverse inequalities are classical. The [LAPACK Users' Guide](https://netlib.org/lapack/lug/node27.html) documents full-rank QR/LQ least-squares solvers and rank-deficient complete-orthogonal-factorization/SVD alternatives. This report uses exact arithmetic because normal equations can square conditioning; replacing its exact operations with ordinary floating point needs a new certified forward/backward-error analysis. No such implementation guarantee is asserted here.

The elementary determinant/trace bound, noise perturbation proof, and rounded residual composition are proved above. Their conjunction supplies a checkable specialized interface, not historical priority or a new general least-squares method. No broad prior-art clearance was attempted.

## 9. Verification and disposition

The newly written `discovery.py` and `checks.py` import no historical research code. Run `python checks.py` in this packet. The exact regression covers N=4,5,8,13,16,31,64, spans one and two, real/complex and repeated-root recurrences, dyadic noise, late defects, rank deficiency, nearly rank-one data, and malformed inputs. Results:

- 256 cases: 235 full-rank proposals, 177 accepted coefficient packets, 58 residual refusals, 21 rank refusals;
- 235 exact normal-residual checks and 235 exact positive-semidefinite conditioning checks;
- 705 exact least-squares optimality identities;
- 224 externally specified model-noise bounds and 224 observable conditional bounds;
- 643 exact boundary identities at available rational unit roots;
- 96 exact proposal-map perturbation controls with no clean-signal premise;
- 117 accepted packets have nonzero residual;
- four ill-conditioning controls through 300-bit raw dyadics and four invalid-interface rejections;
- an exact 64-step unstable-reconstruction countercontrol with gain 2^62.

These are finite transcription/interface controls, not all-size proof, complete DFT execution, statistical validation or performance evidence. The proofs above establish the all-size guarded assertions. No floating-point backend, historical program, broad numerical search, external publication or table mutation was executed.

**Proposed bounded completion after independent review:** guarded noise-stable, all-tail rank-one/two coefficient proposal and rounded actual-data residual certificate, with the explicit exact-rational implementation and paid composition interface. Keep ALG-064 open at priority 42. Keep floating-point stable discovery, broad/optimal noise regimes, non-dyadic acquisition, normalized real-residual adaptation, resource-budgeted production integration and benchmarking, arbitrary-input architecture and historical novelty unresolved. Do not redispatch this exact bounded proposal as an unfilled oracle, and do not delete any broader claim because this subgate is done.
