# Finished optimization of the accepted C8 quantitative-gap chain

19 October 2026 UTC.

## Result

Let

\[
N=216382078575297666905178343251032596362320361,
\qquad D=10^{50},\qquad
\varepsilon_-=N/D,\quad\varepsilon_+=(N+1)/D.
\]

The all-phase, original-model strict bound certified here is

\[
\boxed{
\delta_{8,0}>
\sin\!\left(\frac{3\pi}{16}+\frac{N}{2D}\right).
}
\tag{R1}
\]

Its lower endpoint is enclosed by

\[
0.555571132594891979835779216476082818062762614353022001594216234031293167572
<\sin\!\left(\frac{3\pi}{16}+\frac{N}{2D}\right)
<
0.555571132594891979835779216476082818062762614353022001594216234031293167573.
\]

These long decimal bounds are outward-rounded presentations of exact rational enclosures, not floating-point proof premises. The improvement over the previously accepted endpoint `sin(3*pi/16+10^-6)` is approximately `6.81059552378028e-8`.

For the exact sufficient-condition chain specified below, the supremum parameter \(\varepsilon_*\) is the unique root, on \(0<\varepsilon<\pi/8\), of

\[
\boxed{
\bigl(6498+1800\cos^2(3\pi/8+\varepsilon)\bigr)
\bigl(\sqrt{10\varepsilon}+\varepsilon\bigr)^2
-\cos^2(3\pi/8+\varepsilon)=0.
}
\tag{R2}
\]

It has the rigorous rational bracket

\[
\boxed{
0.00000216382078575297666905178343251032596362320361
<\varepsilon_*<
0.00000216382078575297666905178343251032596362320362.
}
\tag{R3}
\]

The bracket has width exactly \(10^{-50}\). In particular \(\varepsilon_-\) is admissible, and \(\varepsilon_+\) is not. There is **no largest parameter satisfying the strict numerical sufficient conditions**: their feasible set is exactly \((0,\varepsilon_*)\). Equality at \(\varepsilon_*\) is not certified by that strict chain. Taking limits nevertheless gives the valid, non-strict limiting conclusion

\[
\delta_{8,0}\ge
\sin\!\left(\frac{3\pi}{16}+\frac{\varepsilon_*}{2}\right).
\tag{R4}
\]

No claim of strict inequality at the implicit limiting endpoint is made.

### Parameter normalization

The spectral-arc half-width is

\[
\theta=3\pi/8+\varepsilon.
\]

The external-residual bound is \(\sin(\theta/2)\), so the increment **inside that sine is \(\varepsilon/2\)**, not \(\varepsilon\). Here the certified increment is exactly

\[
\frac{N}{2\cdot 10^{50}}
=0.000001081910392876488334525891716255162981811601805.
\]

The old proof used \(\varepsilon=2\cdot10^{-6}\), giving the old sine increment \(10^{-6}\).

## 1. What is fixed, and what is optimized

This certificate imports the already accepted all-phase analytical chain from the quantitative-gap proof and its independent review. It does not re-audit it or import/execute either historical checker. Source hashes are saved in `SOURCE_BINDINGS.json` and verified unchanged after the exact checks.

The following constants and estimates are fixed, without improvement:

\[
\theta_0=3\pi/8,\quad c=\cos(\theta_0+\varepsilon),\quad
\rho=\sqrt{10\varepsilon}+\varepsilon,\quad
\eta=2\sqrt2\rho,\quad
r=\rho+14\sqrt2\eta=57\rho.
\tag{1.1}
\]

The chain retains:

- the endpoint residual estimate derived using \(\tan\theta<5/2\);
- the modulus threshold \(m\le5\eta\), the small Fourier coefficient bounds \(7\eta,8\eta\), and the unchanged normalized-product constants \(21/25,101/50,202/105,199/100\);
- the half-shift errors \(14\eta,16\eta\) and the approximate phase-periodicity error \(30\eta\);
- the flat-vector residual \(r=57\rho\);
- the final necessary compression inequality

\[
r\ge c\sqrt{1-225\eta^2}/\sqrt2.
\tag{1.2}
\]

We optimize only \(\varepsilon\) in these exact expressions. The old proof's convenient terminal rational comparison values, such as \(\rho<9/2000\) and \(r<13/50\), are replaced by a direct exact-interval test of (1.2). Those display/comparison values were sufficient certificates for the old chosen parameter, not additional analytical restrictions that must be retained in optimizing (1.1)–(1.2).

We do not sharpen \(\rho\), change the Fourier support argument, optimize its threshold 5, replace the flat-vector estimate, or introduce a different matrix argument. Any such change would be a different sufficient-condition chain and is outside this completed optimization.

## 2. Original model and the conditional contradiction

The model remains normalized \(F_8\), arbitrary invertible complex monomial outer factors, unrestricted real core, zero correction rank, and the external complex operator norm. Absorbing only real monomial magnitudes/permutations into the real core gives exactly

\[
\delta_{8,0}=\min_{P,Q\text{ diagonal unitary}}
\|\operatorname{Im}(PF_8Q)\|_2.
\]

For a hypothetical phase choice with residual at most \(\sin(\theta/2)\), write \(A=P^2\), \(B=Q^2\), \(C=F_8AF_8\), and \(U=CB\). The accepted reduction gives \(\operatorname{Re}_H U\ge cI\). The cycle-commutator localization and quantitative Fourier argument, under the auxiliary conditions verified below, give the bounds (1.1) and

\[
|b_{j+4}-b_j|\le30\eta.
\]

This is an approximate relation on the actual phases. It does not justify or require replacement by periodic phases.

For completeness, the decisive actual-compression step is retained explicitly. Let

\[
\beta_0=(b_0+b_4)/2,\qquad\beta_2=(b_2+b_6)/2,
\]

and write the cyclic-Hankel entries as \(C[j,k]=c_{j+k}\). The two even half-shift compressions of the **actual** \(U\) have diagonals

\[
(c_0+c_4)\beta_0,\ (c_0+c_4)\beta_2
\quad\text{and}\quad
(c_0-c_4)\beta_0,\ -(c_0-c_4)\beta_2.
\]

The accepted construction supplies a flat unit vector in each sector with residual at most \(r\) for its endpoint phase. For a unitary \(U\), its adjoint residual is the same; therefore the diagonal difference of either compression is at most \(2r\). This statement needs neither an invariant sector nor a unitary compression. Accretivity gives \(|c_0\pm c_4|\ge c\), hence

\[
|\beta_0-\beta_2|\le2r/c,
\qquad |\beta_0+\beta_2|\le2r/c.
\]

Meanwhile \(|\beta_j|^2\ge1-225\eta^2\). The parallelogram identity gives precisely (1.2). Thus the strict reverse inequality in (1.2), together with the auxiliary conditions, excludes every phase choice at the proposed residual threshold. Compactness of the phase torus turns this exclusion into the strict minimum bound (R1).

No exact periodicity, invariant-sector reduction, or unitary surrogate compression is used anywhere in this certificate.

## 3. Auxiliary conditions hold uniformly beyond the optimum

It suffices to work on the whole box

\[
0<\varepsilon\le E:=3/10^6.
\tag{3.1}
\]

Every auxiliary condition of the fixed proof holds throughout this box:

1. **Arc and branch conditions.** Since \(\pi>3\), \(E<\pi/8\), so \(\theta<\pi/2\). Also \(16E<2\pi\) and \(4E<\pi/2\). These justify the opposite cycle offsets and their cosine branch exactly as in the accepted proof.

2. **Endpoint tangent bound.** Positive squaring using \(\sqrt2<283/200\) gives

   \[
   \cos\theta_0>191/500,\qquad \sin\theta_0<231/250.
   \]

   Sine and cosine are 1-Lipschitz, so

   \[
   c>191/500-E>0,\qquad
   \sin\theta<231/250+E.
   \]

   The exact rational inequality

   \[
   (5/2)(191/500-E)>231/250+E
   \]

   proves \(\tan\theta<5/2\) throughout the box.

3. **Small-error hypothesis.** Positive squaring gives

   \[
   (11/2000-E)^2>10E,\qquad \rho<11/2000.
   \]

   Hence

   \[
   \eta^2=8\rho^2<8(11/2000)^2<(1/50)^2.
   \]

   Thus \(\eta<1/50\), and \(1-225\eta^2=1-1800\rho^2>0\).

4. **Phase-product contradiction.** The unchanged rational comparisons are

   \[
   (24/25)(4/5)(47/50)>(21/25)^2,
   \quad
   4\frac{101/50}{21/25}\frac15=202/105<199/100.
   \]

   Also

   \[
   2\cos(4\varepsilon)\ge2-(4\varepsilon)^2
   \ge2-(4E)^2>199/100.
   \]

Consequently none of these auxiliary restrictions is active at the limiting parameter. Each exact rational comparison above is an assertion in the checker.

## 4. One limiting inequality and its unique root

Since the two sides of (1.2) are nonnegative in the box, its strict reverse is equivalent, by squaring, to

\[
2r^2<c^2(1-225\eta^2).
\]

Substituting (1.1) gives

\[
6498\rho^2<c^2(1-1800\rho^2),
\]

or

\[
G(\varepsilon):=(6498+1800c^2)\rho^2-c^2<0.
\tag{4.1}
\]

Define on the larger domain \(0<\varepsilon<\pi/8\)

\[
H(\varepsilon)=G(\varepsilon)/c^2
=\bigl(6498/c^2+1800\bigr)\rho^2-1.
\tag{4.2}
\]

Here \(c=\cos(3\pi/8+\varepsilon)\) is positive and strictly decreasing, so \(6498/c^2+1800\) is positive and strictly increasing. Also \(\rho^2=(\sqrt{10\varepsilon}+\varepsilon)^2\) is positive and strictly increasing. Their product is strictly increasing. Therefore **\(H\) is continuous and strictly increasing on the entire relevant arc domain**.

As \(\varepsilon\downarrow0\), \(H\to-1\). As \(\varepsilon\uparrow\pi/8\), \(c\to0\) with \(\rho>0\), so \(H\to+\infty\). The intermediate value theorem and strict monotonicity yield exactly one root \(\varepsilon_*\), with

\[
G<0\iff H<0\iff 0<\varepsilon<\varepsilon_*.
\]

The rational bracket in the next section places the root below \(E\). All auxiliary conditions hold for every smaller positive parameter by Section 3. Parameters above the root fail the final strict contradiction, whether or not their auxiliary conditions hold. Therefore the complete feasible set for this fixed strict chain is exactly \((0,\varepsilon_*)\); there is no hidden second feasible interval.

At equality \(G=0\), the upper estimate and necessary compression lower estimate agree. The present certificate does not reinterpret discarded strict slack elsewhere to claim that this equality endpoint is admissible. The conservative strict theorem uses \(\varepsilon_-<\varepsilon_*\). The non-strict limiting theorem (R4) follows from the strict theorem for every \(\varepsilon<\varepsilon_*\) and continuity of the sine, without making equality admissible in the strict condition.

## 5. Exact rational interval certificate

The checker uses only standard-library integer and rational arithmetic for all assertions. In particular it uses no floating-point root solver, sampling, numerical trigonometric assertion, or precomputed digits of \(\pi\).

### Algebraic trigonometric identity

The double-angle formula gives exactly

\[
c^2=\cos^2(3\pi/8+\varepsilon)
=\frac12-\frac{\sqrt2}{4}\bigl(\cos(2\varepsilon)+\sin(2\varepsilon)\bigr).
\tag{5.1}
\]

Thus only a square root and trigonometric functions at the small **rational** argument \(2\varepsilon\) need interval evaluation.

### Rational square-root enclosure

For a nonnegative rational \(q=n/d\), put \(S=10^{100}\) and

\[
m=\operatorname{isqrt}\!\left(\left\lfloor nS^2/d\right\rfloor\right).
\]

Exact integer squaring verifies

\[
(m/S)^2\le q<((m+1)/S)^2.
\]

These give an enclosure of width \(10^{-100}\). The checker verifies the bounding squares separately at every call.

### Alternating trigonometric enclosure

For \(0\le x\le1\), sine and cosine Taylor terms decrease in magnitude. The partial sum with terms indexed \(k=0,\ldots,9\), ending in a negative term, is a lower bound. Adding the positive \(k=10\) term gives an upper bound. The checker uses those two exact rational sums, verifies the domain and term decrease, and combines them with (5.1).

### Evaluation of the decisive sign

Let \([q_l,q_u]\) enclose \(\rho^2\), and \([v_l,v_u]\) enclose \(c^2\). Since \(1-1800q_u>0\), monotonicity of

\[
G=6498q-v(1-1800q)
\]

in these two independent arguments gives the enclosure

\[
6498q_l-v_u(1-1800q_l)
\le G\le
6498q_u-v_l(1-1800q_u).
\]

At the two rational bracket endpoints, the exact tests establish

\[
G(\varepsilon_-)<-10^{-46}<0,
\qquad
G(\varepsilon_+)>10^{-46}>0.
\]

More informatively, the outward-rounded enclosures begin

\[
G(\varepsilon_-)
\in[-4.284911593797533\cdot10^{-46},\,-4.284911593797532\cdot10^{-46}],
\]

\[
G(\varepsilon_+)
\in[2.486196288061809\cdot10^{-46},\,2.486196288061810\cdot10^{-46}].
\]

The full 75-digit outward-rounded enclosures are recorded in `CHECK_RESULTS.json`. Their certified signs prove (R3), by Section 4. The same rational enclosures and positive square roots give the residual endpoint bounds via

\[
\sin(\theta/2)=\sqrt{\frac{1-\sqrt{c^2}}2}.
\]

## 6. Completion, interpretation, and limits

The rational certified residual endpoint is within \(10^{-50}\) of the fixed chain's supremal endpoint. A straightforward mean-value estimate also gives

\[
0<\sin(3\pi/16+\varepsilon_*/2)
-\sin(3\pi/16+\varepsilon_-/2)
<(\varepsilon_+-\varepsilon_-)/2=5\cdot10^{-51}.
\]

Thus numerical parameter tuning of this fixed chain is finished to a rigorously bounded, negligible remainder. No further iterations are proposed. A substantial improvement would require changing at least one estimate or using a different argument; it cannot come from choosing a larger parameter in this chain.

The inherited upper bound remains

\[
\delta_{8,0}\le\frac12\sqrt{1+\sqrt{\sqrt2-1}}
\approx0.6410136997181851621.
\]

That upper-witness theorem is inherited through the accepted review, not re-proved here. The gap between it and the lower endpoint is still substantial. The method ceiling is **not** the true optimum of the original phase minimization. There is no global-optimality or minimizer-classification claim, and there is no guarantee of literature novelty.

The certificate concerns only C8 and rank zero. It preserves the original all-phase model and actual non-invariant compressions. It changes no source files, makes no external writes, creates no subagents, and leaves no computation pending.

## 7. Reproduction

Run:

```sh
python certify_method_ceiling.py
```

Python 3 with its standard library is sufficient. The script writes `CHECK_RESULTS.json`, `ASSERTIONS.json`, and `SOURCE_BINDINGS.json` only in this new result directory. It verifies 142 exact assertions, including rejected above-ceiling and half-angle-confusion controls. `MANIFEST.json` records file hashes. Decimal strings are only outward-rounded presentation of exact interval endpoints.
