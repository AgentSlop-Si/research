# Independent review: completed C8 fixed-chain ceiling

19 October 2026 UTC.

## Verdict

**PASS, within the explicitly fixed strict sufficient-condition chain.** No correction to the numerical bracket, certified strict lower bound, monotonicity argument, or non-strict limiting conclusion is required.

Let

\[
N=216382078575297666905178343251032596362320361,
\quad D=10^{50},\quad \varepsilon_-=N/D,\quad\varepsilon_+=(N+1)/D.
\]

The candidate validly certifies, in the accepted original all-phase C8 rank-zero model,

\[
\delta_{8,0}>\sin\!\left(\frac{3\pi}{16}+\frac{N}{2D}\right),
\]

whose right-hand side is approximately

\[
0.555571132594891979835779216476082818062762614353022001594216234031293167572540.
\]

The declared strict sufficient conditions have exactly the feasible interval
\(0<\varepsilon<\varepsilon_*\), with

\[
0.00000216382078575297666905178343251032596362320361
<\varepsilon_*<
0.00000216382078575297666905178343251032596362320362.
\]

The supremum is not a largest parameter in that open interval. Continuity gives

\[
\delta_{8,0}\ge\sin(3\pi/16+\varepsilon_*/2).
\]

There is no numerical tuning work left open in this review. The chosen rational theorem is less than \(5\cdot10^{-51}\) below the supremal residual endpoint of this declared test.

## 1. Sources and review scope

The candidate is `/workspace/shared/phase_rankzero_method_ceiling_20261019_1431`.
Its proof has SHA-256
`f3d681355c5e8463ad1fe74a81e5957af18cb8cf7bf9dee7e68dc89c1793f80b`.

The accepted all-phase proof is `/workspace/shared/phase_rankzero_quantitative_20261019_1347/PROOF.md`, SHA-256
`755ea834b423038c67d4c813324d196045fe3594609780cd806d8afa0adfa4a0`.
Its independent accepted review is `/workspace/shared/phase_rankzero_quantitative_review_20261019_1354/REVIEW.md`, SHA-256
`7643134c6250baab3dcdb1a64a16100aafead830cd545b1b67255341b6f18983`.

The inherited analytical theorem and original model were taken as accepted. I checked how its parameter-dependent hypotheses and constants are transferred, rather than redoing its matrix/Fourier algebra. The candidate, original proof, and accepted-review manifests were verified, together with their historical source receipts. All 38 bound source files remained byte-identical. No candidate or historical checker was imported or executed.

The fresh independent program passed **213 exact assertions**. These arithmetic assertions supplement the analytic audit below; they do not replace a universal argument with parameter sampling.

## 2. The limiting condition is transferred correctly

The inherited definitions are

\[
c=\cos(3\pi/8+\varepsilon),\quad
\rho=\sqrt{10\varepsilon}+\varepsilon,\quad
\eta=2\sqrt2\rho,\quad
r=\rho+14\sqrt2\eta=57\rho.
\]

The actual-compression argument from the accepted proof forces

\[
r\ge\frac{c\sqrt{1-225\eta^2}}{\sqrt2}.
\]

Where \(c>0\) and \(1-225\eta^2>0\), its strict reverse is equivalent to

\[
2(57\rho)^2<c^2(1-1800\rho^2),
\]

which is exactly

\[
G(\varepsilon)=(6498+1800c^2)\rho^2-c^2<0.
\]

The factors 57, 6498, and 1800 are all correct. In particular no factor from the normalized Fourier transform or half-shift replacement was lost.

The old terminal comparisons \(\rho<9/2000\), \(r<13/50\), and the separated lower estimates on the right-hand side were convenient sufficient witnesses at the old parameter. They are not required analytical hypotheses once the exact final compression comparison is evaluated directly. Discarding those old terminal comparison values is consistent with the candidate's declared optimization scope.

The accepted proof uses the actual arbitrary phases and compressions of the actual unitary. The candidate does not insert exact periodicity, invariant sectors, or a unitary compression assumption.

## 3. Exhaustive auxiliary-condition audit

Every parameter-dependent hypothesis used before the final compression comparison holds on
\(0<\varepsilon\le E=3/10^6\), which contains the entire certified root bracket:

1. **Angles and branches.** From \(\pi>3\), one has \(\theta_0-\varepsilon>0\), \(\theta_0+\varepsilon<\pi/2\), \(16\varepsilon<2\pi\), and \(4\varepsilon<\pi/2\). These cover positive cosines in endpoint localization, uniqueness of the opposite cycle offsets, and the phase-product cosine branch.
2. **Endpoint residual estimate.** Positive squaring with \(\sqrt2<283/200\) gives \(\cos\theta_0>191/500\) and \(\sin\theta_0<231/250\). The derivative bounds for sine and cosine then give \(c>191/500-E>0\) and \(\sin\theta<231/250+E\). The exact comparison \((5/2)(191/500-E)>231/250+E\) proves \(\tan\theta<5/2\) uniformly.
3. **Fourier-product smallness.** The positive-square comparison \((11/2000-E)^2>10E\) gives \(\rho<11/2000\). Therefore \(\eta^2=8\rho^2<1/2500\), so \(\eta<1/50\). It also implies \(1-225\eta^2=1-1800\rho^2>0\).
4. **Unchanged product constants.** The independent exact checks confirm
   \((24/25)(4/5)(47/50)>(21/25)^2\) and
   \(4(101/50)/(21/25)/5=202/105<199/100\).
   The uniform lower bound \(2\cos(4\varepsilon)\ge2-(4E)^2>199/100\) completes the same phase-product contradiction as before.

The remaining constants 5, 7, 8, 14, 16, 30 and the unit-modulus/Parseval relations are parameter-independent pieces of the accepted argument. They introduce no further numerical restriction near the root. Thus no auxiliary restriction is active before the final strict comparison fails.

## 4. Global monotonicity of the declared test

On \(0<\varepsilon<\pi/8\), let

\[
B(\varepsilon)=6498\sec^2(3\pi/8+\varepsilon)+1800,
\qquad q(\varepsilon)=(\sqrt{10\varepsilon}+\varepsilon)^2.
\]

Both are positive. An independent derivative audit gives

\[
B'=12996\sec^2(3\pi/8+\varepsilon)\tan(3\pi/8+\varepsilon)>0,
\]

\[
q'=2(\sqrt{10\varepsilon}+\varepsilon)
\left(\frac5{\sqrt{10\varepsilon}}+1\right)>0.
\]

Hence \(H=Bq-1=G/c^2\) is continuous and strictly increasing throughout that entire arc domain. Its limits are \(-1\) at zero and \(+\infty\) at \(\pi/8\). It has exactly one root.

The exact rational endpoint signs put that root below \(E\). Since every auxiliary condition holds up to \(E\), all positive parameters below the root satisfy the complete declared strict test. Every larger parameter in the relevant arc domain fails the final strict test, regardless of any auxiliary condition. This proves the stated open feasible interval and rules out a second feasible component. It does not depend on a grid, numerical optimizer, or plotting.

## 5. Independent exact arithmetic

The candidate's own interval construction is sound: its integer-square-root formula verifies bounding squares; its alternating sums have the correct parity; its positive sum and cosine-square intervals have the correct order; and its gap evaluation is increasing in \(\rho^2\) and decreasing in \(c^2\) on the stated positive-beta domain. Its outward Decimal formatting is not used as a floating-point proof premise.

To avoid merely repeating that implementation, the independent checker uses a different route:

- Square roots are enclosed by binary integer bisection on a dyadic mesh of width \(2^{-384}\), with final bounding squares verified exactly. It does not call `isqrt` or use decimal scaling.
- The angle-addition identity
  \[
  c=\frac{\sqrt{2-\sqrt2}}2\cos\varepsilon
    -\frac{\sqrt{2+\sqrt2}}2\sin\varepsilon
  \]
  replaces the candidate's double-angle identity for \(c^2\).
- Sine and cosine are bounded by exact rational Taylor polynomials and absolute Lagrange remainder bounds. Cosine uses degree 16 with remainder at most \(\varepsilon^{17}/17!\); sine uses degree 17 with remainder at most \(\varepsilon^{18}/18!\). No alternating-series premise is needed for this independent computation.
- General interval operations separately evaluate both the direct compression margin \(c^2(1-1800\rho^2)-2(57\rho)^2\) and the normalized expression \(H\).

The resulting signs are

\[
G(\varepsilon_-)\approx-4.28491159379753226809063615945395785316\cdot10^{-46},
\]

\[
G(\varepsilon_+)\approx 2.48619628806180925317752718017115608739\cdot10^{-46}.
\]

The exact independent intervals prove the first is below \(-10^{-46}\), and the second above \(10^{-46}\). The independently evaluated normalized signs agree. Every candidate-reported endpoint/gap/improvement enclosure contains the independently constructed interval strictly.

The independent residual-bracket width is enclosed near

\[
4.15734505612424765186280692973091658795316333648\cdot10^{-51},
\]

and is strictly below \(5\cdot10^{-51}\). The improvement over the previous accepted residual endpoint is approximately \(6.8105955237802799370\cdot10^{-8}\). Destructive controls reject the upper bracket endpoint as strict-admissible, the replacement of \(\varepsilon/2\) by \(\varepsilon\), and the incorrect flat-vector factor 29.

## 6. Strict endpoint, continuity, and interpretation

The external residual threshold is \(\sin(\theta/2)\), so \(\theta=3\pi/8+\varepsilon\) gives the angle increment \(\varepsilon/2\). The candidate's rational increment \(N/(2D)\) is correct.

At \(\varepsilon_-\), the strict numerical contradiction rules out every phase choice with residual at most the proposed threshold. The inherited compactness of the phase torus makes the minimum attained, so the conclusion for \(\delta_{8,0}\) is genuinely strict.

For every \(\varepsilon<\varepsilon_*\), the same argument proves the corresponding strict lower bound. Taking an increasing sequence tending to \(\varepsilon_*\) and using continuity of sine proves the non-strict limit. The candidate correctly avoids converting this limit alone into a strict inequality. The strict numerical condition itself excludes equality by definition.

**Scope caution.** This is an exact ceiling for the explicitly chosen, relaxed numerical condition \(G<0\), with the listed constants and comparisons fixed. It is not a sharpness theorem for every possible logical consequence of the inherited proof: retaining discarded strict slack, improving an estimate, or changing a threshold would be a different test. Nor does it establish the true optimum of the original phase minimization, the optimality of the inherited upper witness, or a minimizer classification. The safe interpretation of the candidate's phrase “method ceiling is not the true optimum” is “the method ceiling does not establish the true optimum”; no separate non-equality theorem is needed or claimed here.

The inherited upper bound remains
\(\delta_{8,0}\le\sqrt{1+\sqrt{\sqrt2-1}}/2\approx0.6410136997181851621\).
It is inherited, not re-proved in this review. The certification concerns only C8 at rank zero; no literature novelty is asserted.

## 7. Reproduction and completion

Run `python independent_exact_controls.py` in this review directory. Only Python's standard library is required. It writes results, assertion names, and before/after source receipts solely into this new review directory. The source files are read-only inputs.

`INDEPENDENT_EXACT_RESULTS.json` contains the independent enclosures and pass count. `VERDICT.json` records the scoped conclusion. `SOURCE_BINDINGS_BEFORE.json` and `SOURCE_BINDINGS_AFTER.json` are identical. `MANIFEST.json` binds the completed review packet.

No external state was modified, no subagent was spawned, and no computation remains pending. Further parameter iterations of this fixed strict test are neither needed nor proposed.
