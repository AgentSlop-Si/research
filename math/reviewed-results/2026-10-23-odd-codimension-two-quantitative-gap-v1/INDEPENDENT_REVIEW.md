# Independent acceptance: uniform relative odd codimension-two gap

Date: 2026-10-23 UTC. Stable owner: M-SPARSE-DEFECT.

## Verdict

ACCEPT the frozen strengthening at its stated scope. No mathematical correction is required. For the original normalized complex Fourier target, spectral norm, arbitrary invertible M, and at most N−2 nonzeros in every row of M^{-1}, every odd N≥3 satisfies

    Delta(N,N−2)^2 ≥ 2/N + g^2/[sqrt(N)+g sqrt(N/(N−2))]^2
                    ≥ (9−4 sqrt(3))/N,
    g=(sqrt(3)−1)/2.

This is a quantitative lower bound, not an exact value or optimal constant. The same proof applies to every odd-order flat unitary target with the same inverse-row admissibility condition. Parent owner status remains TO RESEARCH, priority 42. No full-budget quantitative classification, optimizer, cost improvement, FFT improvement, or historical novelty claim is accepted or made.

## Frozen target and inherited sources

Target directory: /workspace/shared/odd_codim2_uniform_gap_20261023.

- REPORT.md SHA-256: 77caa3fecaeef2d5dddab32a2a674c660fafa1040e52a43f17b2e059d4c1e359.
- MANIFEST.json SHA-256: b31790efbd54b61da3cec2521264285152a0900cb59d8b02fbb099ee24f2dd51.
- Accepted original-model E_REVIEW.md SHA-256: 54511a4d4c1e343b5d3bbe3edb7d9a054d42a4200681bb17cf0bda6c11538253.
- Accepted semiprime classification review SHA-256: e4b3a4674957e12b0f9e06919342c9e18a5ccb15c042aec4a93c25e66dd7989c.

All ten candidate manifest members were checked before and after each fresh run. Both source copies matched the original local files specified by the candidate source bindings. The exact report, manifest, source bindings, and inherited reviews are copied under sources/. The earlier semiprime_quantitative_codim2_20261023 report is included only as historical scope context. Its scientific programs were not executed, and its weaker bound is not separately counted as new work.

The reviewer read E_REVIEW.md in full, particularly its original-model definition, row bound, coefficient rigidity, and nonattainment discussion. The new proof does not assume that equality-mask necessity alone establishes a quantitative gap. It supplies an independent stability transfer for arbitrary admissible inverse coefficients.

## 1. Model, orientation, and support padding

Write F[j,i]=exp(−2 pi i ji/N)/sqrt(N), B=M^{-1}, E=M−F, rho=||E||_2, q=(N−2)/N, a^2=2/N, and epsilon=rho^2−a^2. The actual support of row i of B may have any cardinality at most N−2. It can be padded to S_i with exactly N−2 elements while keeping all matrix coefficients unchanged.

The definition A[j,i]=F[j,i]1_{j in S_i} is essential: inverse-row supports become retained COLUMN supports. Thus the i-th row of A* and B have supports contained in S_i, while the i-th column of C=F−A has support T_i=S_i^c. Every column of C has exactly two entries of modulus 1/sqrt(N), regardless of actual zeros in B. No regularity of C's rows is assumed or inferred.

With Y=qB−A*, row Y_i vanishes on T_i, including after padding. On padded coordinates it need not vanish: its value can be −conjugate(F[j,i]). This is allowed, and its contribution is included in the squared-norm identity. The proof never discards such terms or treats an actual inverse as a binary Fourier mask.

## 2. Exact stability identities and unrestricted coefficients

Put H=rho^2 I−EE*. This is positive semidefinite by the spectral-norm definition. For x_i=||b_i||>0 and z_i=(b_iF)_i, the relation b_iE=e_i−b_iF and unitarity give

    b_i H b_i* = 2 Re(z_i)−1−(q−epsilon)x_i^2,
    ||Y_i||^2 = q^2 x_i^2+q−2q Re(z_i).

Consequently

    q b_i H b_i*+||Y_i||^2=q epsilon x_i^2.

The sign, gain q, and Fourier conjugation are correct. In particular, Y is a quantitative coefficient-error term, not an assumption that B already has the equality-case coefficients or phases.

Let P=q epsilon BB* and Q=qBHB*+YY*. Once epsilon≥0 is established below, both are positive semidefinite and have identical diagonal entries q epsilon x_i^2. Applying positive-semidefinite Cauchy–Schwarz to each matrix separately gives

    |(P−Q)[i,j]|≤2q epsilon x_i x_j,
    ||Y_i||≤sqrt(q epsilon)x_i.

The full matrix identity is also exact. Expanding BE=I−BF first gives

    P−Q=qI−qBF−qF*B*+q^2 BB*−YY*.

Substituting qB=A*+Y then gives

    P−Q=C*C−a^2 I−YC−C*Y*.

Hence K=C*C−a^2I=P−Q+YC+C*Y*. All factors have their original indices and dimensions. No transpose substitution, common-support ansatz, coefficient quantization, or condition-number assumption occurs.

## 3. One-row normalization and the large-error branch

Because b_i is supported in S_i and the restricted Fourier column has squared norm q, Re(z_i)≤sqrt(q)x_i. Therefore

    rho^2≥||b_iE||^2/x_i^2
          ≥a^2+(1/x_i−sqrt(q))^2.

This proves epsilon≥0 for every admissible M, even with smaller actual supports. When epsilon<q, it also proves

    x_i≤1/[sqrt(q)−sqrt(epsilon)].

This is a derived row-norm bound, not an input conditioning restriction. The denominator is positive exactly in the branch where it is used. Set

    u=sqrt(q epsilon)/[sqrt(q)−sqrt(epsilon)].

Then the preceding stability estimates give |(P−Q)[i,j]|≤2u^2 and ||Y_i||≤u. When epsilon≥q, the proposed correction g^2/[sqrt(N)+g/sqrt(q)]^2 is strictly smaller than q, since its positive square root is less than sqrt(q). Thus that entire branch satisfies the final bound automatically. No assumption rho<1 is imposed on the theorem.

## 4. Odd-order incidence obstruction with irregular rows and arbitrary phases

For any N-by-N matrix C having exactly two flat nonzeros per column, either two column supports intersect in exactly one row or they do not.

In the first case the relevant Gram entry has exactly one summand, whose modulus is exactly 1/N. Arbitrary phases cannot cancel a one-term sum.

In the second case distinct two-element supports are disjoint. If there are r distinct supports, 2r≤N. Oddness gives 2r<N. Since there are N columns, at least three must share one support. Their 3-by-3 Gram G has rank at most two, trace 6/N, and diagonal 2/N. Its nonnegative eigenvalues satisfy tr(G^2)≥(tr G)^2/2=18/N^2. Subtracting its diagonal contribution 12/N^2 leaves at least 6/N^2 over six ordered off-diagonal squares. Some off-diagonal modulus is therefore at least 1/N.

This argument includes isolated rows, highly nonuniform row degrees, repeated supports, and all complex phases. It uses no cyclotomic root-separation assumption. Even orders genuinely evade the incidence conclusion through disjoint support pairs, each used twice. No forbidden row-regularity reduction has been made.

## 5. Localization is valid and supplies the stronger scale

In the singleton-intersection case, Y_i vanishes on T_i. Therefore the product Y_i C_j sees only T_j minus T_i, which contains exactly one coordinate. The estimate is u/sqrt(N), not u sqrt(2/N). The transposed-conjugate cross term has the same bound. The exact identity thus gives

    1/N≤2u^2+2u/sqrt(N).

For v=sqrt(N)u≥0, the quadratic 2v^2+2v−1≥0 yields v≥g=(sqrt(3)−1)/2.

In the repeated-support case, choose the Gram pair above. Its supports are identical, so both cross terms vanish exactly. The estimate is stronger: 1/N≤2u^2 and v≥1/sqrt(2)>g. The same lower bound v≥g therefore holds without choosing or restricting the support pattern.

Rearranging sqrt(N)sqrt(q epsilon)/[sqrt(q)−sqrt(epsilon)]≥g in the positive-denominator branch gives

    sqrt(epsilon)≥g/[sqrt(N)+g/sqrt(q)].

Together with the large-error branch, this proves the first claimed bound for every admissible M. Squaring and taking the infimum are valid because all norms are nonnegative; attainment or compactness is not needed.

## 6. Constants, endpoint, and sharpness limits

For N≥3, 1/sqrt(q)=sqrt(N/(N−2))≤sqrt(N). Hence

    g/[sqrt(N)+g/sqrt(q)]≥g/[sqrt(N)(1+g)]
                           =(2−sqrt(3))/sqrt(N).

Adding 2/N gives (9−4sqrt(3))/N, with coefficient approximately 2.07179676972449>2. The claimed relative norm factor sqrt((9−4sqrt(3))/2)>1.01779 is correct. The stronger squared-bound coefficient is

    2+g^2/[1+g/sqrt(N−2)]^2,

which tends to 2+g^2=3−sqrt(3)/2≈2.13397459621556. These are coefficients of proved lower bounds, not asymptotics for the unknown optimum.

At N=3, q=1/3 and the two displayed lower bounds coincide. They give (9−4sqrt(3))/3≈0.690598923241497, strictly below the inherited exact Delta(3,1)^2=3/4. Thus the accepted endpoint explicitly confirms nonsharpness of the new Delta constant; the exact N=3 solution is not new credit.

The historical relaxed-mask operator-defect lemma has the separately sharp constant sqrt(2)/N. Its 3-by-3 witness, before normalization, has columns of weight two and row degrees (3,2,1); its Gram-defect characteristic polynomial is x(x^2−2). Appending two-by-two Hadamard blocks extends that relaxed example to every odd order. This does not make it a fixed-Fourier mask or an admissible optimizer for the original inverse-row problem. The current proof does not rely on identifying those two sharpness notions.

## 7. Fresh independent controls and their limits

The new independent_controls.py was authored for this review. It imports no candidate or historical scientific program and does not execute one. Normal and python -O runs produce byte-identical RESULTS.json and RESULTS_OPT.json, with empty final stderr files.

Exact controls:

- Exhaust all 27 N=3 and all 100,000 N=5 ordered two-entry-per-column support patterns. There are 99,564 singleton-intersection certificates and 463 repeated-support triple certificates. The enumeration includes 97,981 row-irregular masks.
- Check 1,152 additional seeded larger odd-order incidence patterns and nine even-order negative examples.
- Check nine original-model stability instances at N=3,5,7 in exact Q[z]/Phi_N arithmetic. Use W=sqrt(N)F, D=B/sqrt(N), and J=D^{-1}=sqrt(N)M. Independent triangular inversion verifies both inverse products. The exact normalizations are Y=(NqD−V*)/sqrt(N) and E=(J−W)/sqrt(N).
- For exact identity tests use a rational certified upper bound lambda≥||E||_2^2 obtained from coefficient-l1 bounds and the Frobenius norm. The identities hold with rho^2 replaced consistently by lambda. These are exact algebraic and PSD-certificate tests, not an exact calculation of each sample's spectral norm.
- Include 33 strictly padded rows, 58 exact same-support cancellations, nine wrong-q-gain mutations, six detected row/column orientation mutations, and nine omitted-support mutation controls.
- Verify six exact constant/endpoint certificates and the historical relaxed-mask characteristic polynomial independently.

Explicitly numerical controls:

- 163 admissible matrix samples: 85 original Fourier-target samples and 78 flat-unitary rephasing/permutation extension samples. Arbitrary complex inverse coefficients, smaller actual supports, and both obstruction cases occur.
- 38 samples have epsilon<q, so the nontrivial row-norm and localized-bound branch is exercised. There are 121 singleton-intersection cases and 42 repeated-support cases, with 272 strictly padded rows. Seven samples have condition number above 10^8. Forty-seven singular generated candidates are excluded because they are not admissible.
- The numerical tests use the actual computed spectral norm. The largest operation-scaled matrix-identity residual is 3.70e−15; the largest forward residual on well-scaled samples is 4.54e−14. The largest equal-diagonal relative residual is 1.48e−15. The declared tolerance is 8e−10.
- A 1,000-point odd-order numerical sweep checks the scalar weakening and automatic large-error branch, supplementing rather than replacing their exact proofs.

The first reviewer harness run used an inappropriate forward-error normalization for a condition-number-10^10 sample: subtracting P and Q at extreme scale catastrophically cancels in double precision. That harness failure is preserved in DEVELOPMENT_FAILURE.txt. The final harness uses operation-scaled residuals for such samples, reports well-scaled forward residuals separately, and retains the independent exact identity controls. It is not a correction or limitation of the mathematical theorem.

Finite checks corroborate formula, indexing, boundary, and implementation details; they do not replace the universal proof.

## 8. Publication scope and stop

This review accepts one strengthening of the existing odd codimension-two quantitative result. Distinct odd semiprimes are included as a subfamily, not as an additional independent achievement. The earlier strictness classification, exact N=3 optimum, and historical weaker quantitative packet remain inherited context.

The proved mechanism is per-row equality stability plus two-column omitted-support localization. No novelty is attributed to its elementary incidence or Gram-rank ingredients. The repeated-support estimate is the classical Welch bound for three unit vectors in C^2, rescaled by 2/N; see [Datta, Howard and Cochran, Geometry of the Welch Bounds, Sections 1 and 2](https://arxiv.org/pdf/0909.0206). The unitary-support exclusions correspond to classical quadrangularity and strong quadrangularity; see [Severini, On the Digraph of a Unitary Matrix, Definitions 1–2 and Lemma 1](https://arxiv.org/pdf/math/0205187). These sources were directly inspected. This mathematical acceptance does not constitute a completed closest-predecessor or historical-novelty comparison for the arbitrary-inverse-row quantitative bridge. Other nonexceptional budgets remain outside this result. No exact nonsharp optimum, optimal lower-bound constant, global support classification, algorithmic speedup, FFT gain, arithmetic-cost statement, or historical-priority clearance follows.

The independent gate is complete. No GitHub, spreadsheet, repository index, or other external state was modified. Publication remains with the sole publisher, using this exact frozen review and its bound target bytes.
