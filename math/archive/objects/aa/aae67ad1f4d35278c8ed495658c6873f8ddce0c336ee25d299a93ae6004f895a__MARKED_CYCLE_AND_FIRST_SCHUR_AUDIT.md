# Marked-cycle source and first Schur stage: independent audit

## Decision and useful outcome

**Accept the explicit stationary Fourier identity, the source's linear tree/closed-trace auxiliaries, and its conditional marked-circuit differentiation reduction.** The source constructs an ordinary Θ(N log N) full Fourier evaluator. Its faster marked scalar circuit is still a conjecture, and the reduction is computationally equivalent to the unresolved full transform rather than independent evidence of a speedup.

**Accept the constructor's root-pole cancellation and the first parity Schur elimination, including its O(N) constant-input two-run coefficient program and 6N slot bound.** Our separately authored deterministic quotient-array implementation confirms the full numerator and actual truncated series, not just evaluations at a few parameters.

The accepted construction stops at an explicit reduced bordered inverse. Neither a cheap inverse of that border nor a cheap application to an arbitrary already polynomial unknown is established. Consequently there is no justified multi-stage recurrence or generic Fourier improvement yet.

A useful independent domain control is that z=ω makes the first odd pivot singular even when the full Fourier border remains invertible. The new chart condition must be retained; the pole-free predecessor does not need it.

## Provenance, source versions and execution boundary

Uploaded Library source: `fft_marked_cycle_theory_2026-10-10.zip`, Library `[private-id]`, archive SHA-256

    6f7e9f88d82f1242ffd58b7c84bb7a76ae39e4606eff52dc7838de99f93e438f

This was initially a Library discovery, not a direct attachment in the earlier batch. The later direct `THEORY (2).md`, Library `[private-id]`, is byte-identical to this archive's `fft_marked_cycle_theory/THEORY.md`. Both identities and the comparison are preserved. All archive-manifest entries match. The source proof, implementation, verifier, README, results and lineage ledger were inspected as inert text. The inventory is historical source metadata, not evidence that this reviewer rechecked all 1,935 listed text occurrences.

Two internal construction reports are independently reviewed as exact sealed snapshots:

1. `ROOT_POLE_CANCELLATION_AND_LINEAR_TREE_JET.md`, SHA-256 `e3cd7602ca18450ed32c4e808de20fe036b61030b837511a768d22b6f3af6c7f`.
2. `ONE_SCHUR_STEP_AND_TWO_RUN_JET.md`, SHA-256 `d9b0c4ac84adc5df1c04f414b7dcddd4c2384bbee82529e24e3e51f60e0bc157`.

Their reports, verifier text, saved results and manifests are copied under `constructor_snapshots`; all six listed report/checker/result hashes match. These snapshots are evidence only. **Neither uploaded code nor constructor checker code was executed or imported by this reviewer.** Only our two auditor-authored files were run. The helper file is a byte-preserved copy of our own independently authored Phase21 mathematical primitives.

## 1. The source's stationary Fourier graph is exact

Let N=2^n≥2, with a supplied primitive Nth root ω in a field. For dyadic N this implies characteristic different from two. Use the positive-sign unnormalized Fourier convention F[k,j]=ω^(kj). Define

    A₀ e_s=e_(2s mod N),
    A₁ e_s=ω^s e_(2s+1 mod N),
    Q=A₀+A₁.

One Q step is N/2 shuffled butterflies: output 2r is x_r+x_(r+N/2); output 2r+1 is ω^r(x_r−x_(r+N/2)). This has exactly 2N nonzero matrix entries.

Let rev_n reverse n bits, and let φ(0)=0, φ(2a)=φ(a), φ(2a+1)=φ(a)+a. After n append-bit steps there is exactly one path between each initial and final vertex. Its exponent is s*rev_n(r)+φ(r), so

    (Q^n)[r,s]=ω^(s rev_n(r)+φ(r)),
    (Fx)_k=ω^(−φ(rev_n(k))) (Q^n x)_(rev_n(k)).

The partial-power formula likewise has exactly N*2^t nonzeros for 0≤t≤n, obtained from input columns a*(N/2^t)+prefix. These formulas are valid for all inputs and are not fitted from a dense Fourier matrix.

The baseline arithmetic count is correct: Nn additions/subtractions and n(N/2−1)+N−n−1 multiplications online. The phase has exactly n+1 zero entries and lies between zero and N−1, so the final multiplication count is exact for this implementation. Root powers take N−2 more multiplications after ω is supplied. Addressing, initialization and n vector passes still cost Θ(N log N). Over the complex numbers, Q divided by sqrt(2) is unitary; this does not manufacture a cheaper evaluator.

The source's field implementation derives ω from a supplied field generator, so that literal setup also includes modular exponentiation and order checking beyond its displayed root-table multiplication counter. Its stated mathematical contract instead supplies ω. Neither the two-field experiments nor a fixed prime support arbitrarily large N.

## 2. Auxiliary Green/Haar and closed-cycle claims

Each A_b is a weighted functional tree with one root loop. The roots are 0 and N−1, with loop weights λ₀=1 and λ₁=ω inverse. Leaf-to-root accumulation solves (I−zA_b)y=x in O(N), with exactly the guard 1−zλ_b≠0. Both branch minimal polynomials have degree n+1; distinct-support Krylov vectors prove the lower bound. Thus a nonconstant minimal-polynomial degree does not imply an expensive structured inverse.

To avoid the source's reused letter C, write C_half for the map

    (C_half v)_r=ω^r(v_r−v_(r+N/2)),

and J for injection into odd global coordinates. Then A₁=J C_half. With G₀=(I−zA₀) inverse and H=C_half G₀ J, the ordinary Woodbury identity is exact. The weighted-Haar recurrence for H and its inverse is valid; its scalar base is (2z−1)/(1−z). O(N) application and inversion of H do not imply an O(N) inverse of I−zH.

A small source API correction is appropriate: `haar_inverse` should explicitly reject z=1. The theorem excludes it, and `haar_apply` is undefined there, but the inverse implementation can return a finite array because it multiplies by 1−z rather than dividing by it. This is not a counterexample to the theorem on its stated domain. The common sufficient inverse guards z≠0,1,1/2 remain valid; some smallest-size cases admit weaker guards.

The periodic-word trace formula is also valid. A length-k closed walk is specified by a k-bit periodic word, including when k>n. The initial n-bit window and next k emitted bits determine its phase. Enumerating k=1,...,n+c uses 2^(n+c+1)−2 words, hence O_c(N) work for fixed c when root powers, reversals and φ tables are charged. Newton identities then give det(I−zQ) through degree n+c using O((n+c)²) additional arithmetic. In positive characteristic the required integers must be invertible; the source enforces p>n+c.

These are unmarked scalar spectral data. They do not compute Q^n x. The minimal-polynomial bound for Q, the quadratic number of simple input-output paths, and the exact root-filter alias denominator are valid restrictions on their specific proposed shortcuts, not general arithmetic lower bounds.

## 3. The marked determinant is an equivalent synthesis obligation

For formal marker vector h, let W=[[Q,x],[h^T,0]], D(z)=det(I−zQ), and E(z;x,h)=det(I−zW). Schur complementation gives

    E/D = 1−z² h^T(I−zQ)^(−1)x.

Since D(0)=1 this is a formal identity regardless of singular scalar evaluation points. Therefore

    −[z^(n+2)] E/D = h^T Q^n x.

E is affine in h and bilinear in its input-dependent x,h part. The alternative trace expression tr(W^(n+2))/(n+2) has the same first marker derivative at h=0 when n+2 is invertible; it can have higher marker powers and is not itself that bilinear form. Evaluating at h=0 before differentiating loses the input-dependent answer.

A uniformly generated scalar straight-line program for this marked coefficient, division-free or regular at h=0 for every permitted x, yields all marker derivatives with constant-factor reverse-mode overhead. Coefficient preparation, program generation, denominators, addressing and O(N) outputs must all be paid. The straightforward reverse tape costs O(program_size+N) memory. Conversely a fast Fourier evaluator immediately computes the marked scalar by phase/permutation correction and one dot product. This is an equivalence up to linear overhead; a fast unmarked determinant jet does not resolve it.

The source's conditional chirp extension from dyadic to arbitrary complex lengths is valid with compatible 2Mth and convolution-length roots supplied and charged. An Mth root alone is insufficient over a finite field. No precision or numerical-stability theorem is supplied for a future determinant circuit.

## 4. Accepted root-pole cancellation

Let E₀=e₀ 1^T and

    K(z)=sum_(t=0 to n−1) z^t(A₀^t−E₀).

Because A₀^n=E₀ and A₀E₀=E₀A₀=E₀, telescoping proves

    (I−zA₀)K=I−E₀,  K e₀=0,  1^T K=0,
    (I−zA₀)^(−1)=K+E₀/(1−z),  for z≠1.

K is polynomial, so its evaluation at z=1 is legitimate. The nonroot tree algorithm computes its action without division and assigns the root as minus the sum of all other coordinates. The missing x₀ information is retained separately as total input mass, rather than discarded from the final solve.

For constant x, the nonroot coordinate s has degree at most ν₂(s). Their total coefficient capacity is 2N−n−2; the root adds at most n coefficients. Thus the complete K(z)x polynomial vector uses at most 2N−2 slots and O(N) coefficient work. A scalar contraction h^T Kx also costs O(N), keeping arbitrary markers. This does not give the same bound for arbitrary polynomial-vector inputs or an expanded left row with every repeated marker coefficient materialized.

The pole-free border is

    B(z) = [[I−z C_half KJ, −e₀], [−z 1^T, 1−z]].

Solve B[u;t]=[C_half Kx;1^T x] and recover

    y=Kx+z KJ u+t e₀.

These equations are equivalent to (I−zQ)y=x and det B=det(I−zQ), including at z=1. The only intrinsic solve guard is that determinant. Inverting the upper-left block first would impose an additional chart guard. At N=2 over GF(3), z=1, the upper-left block is zero while the full border determinant is two; our independent control reproduces this exception.

The scalar identity h^T y=h^T Kx+[z h^T KJ,h₀]B inverse[C_half Kx;1^T x] retains the full marked target. The coupled inverse term is still the unresolved operation.

## 5. Accepted first Schur elimination

For N≥8 let m=N/2 and l=N/4, and split the m interface coordinates into even and odd indices. Set H=C_half KJ. The regularized weighted-Haar recurrence gives

    H_OO=ω³ T₁,  H_OE=ω T₀,
    T_b e_j=(ω⁴)^j e_(2j+b mod l).

The odd pivot D_p=I_l−zω³T₁ is one weighted ones-tree with determinant

    q(z)=1−zω^(−1).

The lift L e_j=e_(4j+3) obeys A₁L=Lω³T₁, hence L D_p inverse=(I−zA₁) inverse L whenever q≠0. This verifies weights as well as topology.

Eliminating the odd unknown gives the l+1 border whose upper block is

    S=I_l−z H_EE−z² H_EO D_p^(−1) H_OE.

Its lower row and input correction in the constructor report follow directly by substitution. The determinant relation is det B=q det B_reduced. Multiplying every reduced row by q gives determinant q^l det B; that known factor must not be dropped in coefficient extraction.

As formal series, q(0)=1 and the reduced constant matrix is invertible. At a numerical parameter q≠0 is a genuine extra restriction. Our GF(65537) controls at z=ω have q=0 but nonzero full determinants: 23,312 for N=8, 47,406 for N=16 and 34,804 for N=32. Thus this Schur chart is narrower than the pole-free full border. It is sound to decline the chart there, not to declare the original system singular.

The odd right input C_half Kx is independent of z in its odd rows, as stated. New constant-input feedback lifts to E_even^T C_half K(I−zA₁) inverse L v. The left marked correction uses the same two-tree primitive in a bilinear contraction. No marker specialization is needed.

## 6. The two-run 6N bound is constructive, with a sharp scope limit

Let λ=ω inverse and

    Ghat₁=(1−λz)(I−zA₁)^(−1)
          =(1−λz) sum_(a=0 to n−1) z^a A₁^a + z^n A₁^n.

For constant v, compute K Ghat₁ v. The endpoint of A₀^b A₁^a from s is

    2^(a+b)s + 2^b(2^a−1) modulo N.

Its potential support is an affine dyadic coset with max(N/2^(a+b),1) states. Keeping a deterministic array for this coset and merging its two preimages preserves all actual phase weights. The total visits over 0≤a≤n, 0≤b<n are less than 4N+n²≤6N. Root-projector mass updates cost O(n²)=O(N); initial weighted ones-tree states and mass sums cost O(N). No hash-table assumption is needed.

For a nonzero output r, write t for its trailing-zero length and h for the adjacent ones-run length. Except for r=N−2^t, its degree is at most t+h+1; the exceptional degree is at most n+t. Together with the root this gives the full capacity

    5N+(n²−3n−10)/2 ≤ 6N.

This is a complete coefficient vector through degree 2n−1, not a scalar evaluation counted as a whole jet. The actual series K(I−zA₁) inverse v through degree n also has an O(N) quotient-state evaluator: retain a+b≤n. There is no required N-times-n generic division pass. Our checker verifies both the full numerator and every truncated coefficient, including numerator_d=series_d−λ series_(d−1).

A marker-weighted contraction of these O(N) coefficients retains arbitrary h in O(N) arithmetic. Repeated left-row values may be represented by shared quotient trees; expanded left-row entries need not be written. But contraction against the unknown polynomial e(z) from the reduced inverse is an additional operation. Feeding that jet into a constant-input routine does not inherit this bound automatically.

The next-pivot matrix supplied at N=32, GF(65537), z=1 matches our independent derivation exactly; its first column has three off-diagonal nonzeros. This excludes literal closure as another single functional-tree pivot in those coordinates. It does not exclude other low-rank, routed, summed-tree or shared representations and proves no generic inverse-cost lower bound. No recurrence such as a sum of shrinking per-stage costs is justified by this first-stage result alone.

## 7. Independent controls and replay

Our code does not execute either submitted checker. It builds dense graph matrices independently, uses exact Gaussian solves/interpolation as bounded oracles, and implements the two-run algorithm with shrinking deterministic coset arrays rather than the constructor's dictionary states.

Passed controls include:

- Five full stationary Fourier matrix identities through N=32 and twenty complete partial-power matrix identities; four omitted-phase negative controls.
- Twenty-five periodic-word traces against dense powers, four independent determinant-polynomial jets, and four marked determinant quotients plus dual-number trace derivatives.
- Weighted unitarity and nine nonzero Krylov minors; three exact resolvent-packet alias identities where deleting the denominator gives a wrong result.
- Thirty-two pole-free/Schur cases across GF(65537) and GF(97), including z=0,1,2,3, the three q=0/full-invertible controls, exact determinant and solve recovery, and marked bilinear equality.
- The GF(3) upper-block-singular/full-border-invertible example.
- Fourteen complete two-run numerator/truncation cases through N=128, using both dense and lifted constant inputs. Every polynomial coefficient matches an independent full-vector-power convolution oracle; all marker contractions match. The largest allocated numerator is 649 slots at N=128, agreeing with the proved formula.
- The state and slot sum formulas for n=1 through 20, and exhaustive simple-path counts through N=64.

Finite checks supplement the algebraic proofs; they do not certify a later stage. `PORTABILITY.json` records a relocated, byte-identical replay using only the two auditor files. `REPLAY.md` gives the exact command.

## 8. Prior work and acceptance boundary

The source appropriately acknowledges established constant-geometry FFTs, periodic-orbit characteristic polynomials and arithmetic-circuit differentiation. We verified the metadata of Miel's constant-geometry paper and Baur–Strassen's differentiation paper, but the PDF endpoints did not render in this check; no detailed formula comparison with those papers is claimed. [Harrison and Hudgins](https://arxiv.org/abs/2101.00006) provide directly relevant quantum-graph/periodic-orbit context. [Ailon's paper](https://arxiv.org/abs/1403.1307) explicitly concerns a well-conditioned computation model; it is not an unrestricted impossibility result.

The stationary and marked identities above have self-contained proofs. The source's unsuccessful project-text novelty search gives no external-priority evidence. The current separate generic Fourier-complexity comparator is not improved by this package or this first Schur stage.

Final acceptance: explicit Fourier graph and honest Θ(N log N) baseline; valid linear auxiliaries; equivalent marked-circuit target; polynomial root-pole cancellation; one guarded Schur reduction; O(N) constant-input two-run jets and contractions. Open: a fast reduced-border inverse, control of polynomial unknowns and further stages, a complete faster marked program, and numerical/bit-complexity guarantees.
