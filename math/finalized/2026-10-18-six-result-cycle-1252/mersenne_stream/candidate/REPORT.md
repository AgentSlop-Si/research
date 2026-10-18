# Removing the same-scale Mersenne-conversion product by clearing the kernel denominator

18 October 2026 UTC. Fresh local continuation. No external write.

## Result and scope

The accepted wide-digit converter's remaining same-scale convolution can be replaced, in a sufficiently wide-digit regime, by explicitly smaller convolutions. The key is to clear one common odd denominator before packing, rather than pack full-width inverse-factorial residues.

Write

\[
\alpha=\log_2 3,\qquad a=\alpha-1\approx0.584963.
\]

For a length-\(n\ge2\) signed Taylor shift with input height \(h\), retain the accepted guards

\[
g=\lceil\log_2 n\rceil,\quad H=h+n+1,\quad W=H+g.
\]

Set

\[
B_n=(n-1)g,\qquad t=8\left\lceil\frac{B_n+g+1}{8}\right\rceil,
\quad b=8\left\lceil\frac{2t+g}{8}\right\rceil,
\quad q=\lceil W/t\rceil,\quad S=nb.
\]

There is an exact, fully evaluated construction with:

- exactly \(q\) packed-convolution products, each with argument capacity \(S=O(n^2\log(n+1))\) bits, independent of \(W\);
- exactly \(5nq\) local products with argument widths at most \(t\), for the input and output diagonal actions, excluding the separately counted preparation;
- three length-\(n-1\) short-factor preparation passes and one \(t\)-bit odd inverse;
- explicit bounded carry streams, all guards, all \(n\) outputs, and \(O(nW+nt)\) coefficient storage, plus the small-product backend workspace.

With the conventional, independently terminating Karatsuba core already used in this research chain, and \(W\ge t\), its complete shift cost is

\[
\boxed{O\!\left(nW\,[n^2\log(n+1)]^a\right).}\tag{1}
\]

The new saving is the exact narrow-kernel representation and its streamed evaluation. Karatsuba is inherited arithmetic, not a newly discovered multiplier or the source of a claimed historical priority. No same-scale multiplication backend is left symbolic in (1).

For the accepted binary, canonical/redundant \(p=2^m-1\), lazy raw-product and grouped \(p^d\) interfaces, put \(N=Lm\). When the actual shift widths satisfy \(W\ge t\), in particular eventually when \(m/(L\log(L+1))\to\infty\), the complete conversion cost becomes

\[
\boxed{O\!\left(N\,[L^2\log(L+1)]^a\right).}\tag{2}
\]

For example, for admissible supplied parameter families with

\[
L=O((\log N)^{4/5}),
\]

(2) is \(o(N\log N)\). This closes the conversion-cost subgate in that regime, including the convolution that remained in the preceding result. It does **not** close matrix transforms, correlated point products, the complete multiplication recurrence, or growing Mersenne-prime availability. The arithmetic does not require \(p\) to be prime. No unbounded suitable prime family is asserted.

At \(L=\Theta(\log N)\), (2) is only
\(O(N(\log N)^{2a}(\log\log N)^a)\), with \(2a>1\), so this particular bound does not give little-o there. At balanced widths \(m=\Theta(L)\), its wide-kernel premise generally fails. The previously accepted converter remains an available alternative outside the new scope.

## 1. Clear the shared denominator exactly

Let \(s(i)=\operatorname{popcount}(i)\) and

\[
u_i=\frac{i!}{2^{i-s(i)}},\qquad U=u_{n-1}.
\]

Every \(u_i\) is odd and divides \(U\). Define the **ordinary nonnegative integer** kernel

\[
K_i=2^{s(i)}\frac{U}{u_i},\qquad 0\le i<n.\tag{3}
\]

This is not a full-width modular inverse. The common denominator is retained as the separately paid output operation \(U^{-1}\bmod 2^W\).

Since \(u_i\le i!<n^{n-1}\le2^{B_n}\), and \(s(i)\le g\),

\[
0<K_i<2^{B_n+g}<2^t.\tag{4}
\]

Also \(0<u_i\le U<2^t\). Thus all kernel entries and all odd divisors fit the fixed \(t\)-bit local width. This remains true even if their inverse residues modulo \(2^W\) have \(W\) significant bits.

For \(\sigma\in\{-1,+1\}\), form

\[
A_i=2^{g-s(i)}u_i a_i\pmod{2^W},\qquad
\widetilde A_i=\sigma^i A_i\pmod{2^W},
\]

using canonical nonnegative representatives. Let

\[
C=\operatorname{rev}(\widetilde A)*K\pmod{2^W}.
\]

Only its first \(n\) coefficients are needed. For each \(j\), compute

\[
R_j=\sigma^j 2^{s(j)}u_j^{-1}U^{-1}C_{n-1-j}\pmod{2^W}.\tag{5}
\]

The two inverse actions in (5) are actual streamed modular divisions, first by \(U\), then by \(u_j\). They are not deferred symbolic scalings.

For every \(i\ge j\), the corresponding summand in (5) is

\[
\sigma^{i+j}2^{g+s(j)+s(i-j)-s(i)}
\frac{u_i}{u_j u_{i-j}}a_i
=2^g\binom ij\sigma^{i-j}a_i.
\]

Here \(\sigma^{i+j}=\sigma^{i-j}\), and
\(v_2\binom ij=s(j)+s(i-j)-s(i)\). Consequently

\[
R_j=2^g\sum_{i\ge j}\binom ij\sigma^{i-j}a_i\pmod{2^{H+g}}.\tag{6}
\]

The low \(g\) bits are zero. Dividing by \(2^g\) leaves the exact residue modulo \(2^H\). The accepted strict height bound

\[
\left|\sum_{i\ge j}\binom ij\sigma^{i-j}a_i\right|
<2^{h+n}=2^{H-1}
\]

gives unique centered integer reconstruction. Both signs and all output coordinates are covered. Empty and length-one inputs are returned directly.

Using sign changes on the wide inputs and outputs keeps \(K\) nonnegative. No signed packing ambiguity, extra convolution, or negative-residue kernel inflation is concealed.

## 2. All preparation is short and paid

Let \(o_i\) be the odd part of \(i\). Prepare exact prefixes and cofactors by

\[
u_0=1,\quad u_i=u_{i-1}o_i;
\qquad F_{n-1}=1,\quad F_{i-1}=F_i o_i.
\]

Then \(F_i=U/u_i\), without any general exact division. Every intermediate is at most \(U\), so truncated \(t\)-bit multiplication returns the exact integer. Set \(K_i=F_i2^{s(i)}\).

Compute one microinverse

\[
v_{n-1}=U^{-1}\pmod{2^t}
\]

by precision-doubling Newton iteration, then recover

\[
v_{i-1}=v_i o_i\pmod{2^t}.
\]

This gives \(v_i=u_i^{-1}\pmod{2^t}\), including the reusable inverse of \(U\).

Let \(s_0=8\lceil\max(1,g)/8\rceil=O(\log(n+1))\). These are exactly \(3(n-1)\) short-factor streamed multiplications, each consisting of \(\lceil t/s_0\rceil\) local products with argument widths at most \(s_0\). The one Newton inversion uses exactly \(2\lceil\log_2 t\rceil\) precision-bounded products, with geometric total \(O(t^\alpha)\) cost. Preparation therefore costs

\[
O\!\left(nt(\log(n+1))^a+t^\alpha\right),\tag{7}
\]

plus \(O(nt+n\log^2(n+1))\) for kernel shifts, small factors, indexing and scans. Under \(W\ge t=\Theta(n\log(n+1))\), these are absorbed by (1).

The kernel is packed once and reused, but its \(S\)-bit read by each multiplication is paid in that multiplication. Tables are regenerated for each shift in the delivered implementation; no amortized setup assumption is made.

## 3. Narrow-kernel streamed convolution

The following elementary lemma is independent of factorials.

### Lemma

Let \(0\le x_i<2^W\) and \(0\le k_i<R=2^t\), with two length-\(n\) arrays. The first \(n\) coefficients of \(x*k\bmod2^W\) can be computed with exactly \(q=\lceil W/t\rceil\) ordinary integer multiplications of capacity \(S=nb\), where \(b=8\lceil(2t+g)/8\rceil\), and \(O(nqt+nW+nt)\) additional bounded-window bit work in the inherited array arithmetic model.

### Proof and implementation

Expand each wide input in low-to-high limbs,

\[
x_i=\sum_{r=0}^{q-1}x_{i,r}R^r,\quad0\le x_{i,r}<R,
\]

zero-padding the last limb. For each slab \(r\), compute

\[
c_{j,r}=\sum_{i=0}^{j}x_{i,r}k_{j-i}.
\]

Pack the slab and the kernel in base \(2^b\). Each ordinary convolution coefficient satisfies

\[
0\le c_{j,r}\le n(R-1)^2<nR^2\le2^{2t+g}\le2^b.
\]

Therefore no inter-slot carry occurs. Both packed argument capacities are \(nb\). A full product has capacity \(2nb\), and the first \(n\) fixed windows provide exactly the needed \(c_{j,r}\).

For each coordinate maintain \(e_{j,0}=0\), then emit

\[
d_{j,r}=(c_{j,r}+e_{j,r})\bmod R,
\qquad e_{j,r+1}=\left\lfloor\frac{c_{j,r}+e_{j,r}}R\right\rfloor.\tag{8}
\]

The invariant

\[
0\le e_{j,r}\le n(R-1)
\]

is preserved: the numerator in (8) is at most
\(n(R-1)^2+n(R-1)=nR(R-1)\). Carries have at most \(t+g+1\) bits, and all pre-split values have \(O(2t+g)\) bits. The prefix identity is

\[
\sum_{r<s}c_{j,r}R^r=
\sum_{r<s}d_{j,r}R^r+e_{j,s}R^s.\tag{9}
\]

At \(s=q\), the final carry is a multiple of \(R^q\), hence vanishes modulo \(2^W\). Masking the last partial limb yields the exact modular convolution. Final carries are deliberately discarded only because the required object is modulo \(2^W\); no ordinary exact quotient is asserted.

The implementation materializes each input byte buffer once, reads each bounded limb once, packs one slab at a time, extracts fixed windows, and writes each output limb once. It does not repeatedly right-shift a whole \(W\)-bit operand or repeatedly add into a growing \(W\)-bit output. At most one packed slab/result pair is live. Scratch output is \(O(nqt)\) bits, which is \(O(nW)\) when \(W\ge t\). This proves the lemma.

### Arithmetic model qualification

As in the accepted construction, these costs are for sequential bit arithmetic on bounded values and explicit bounded-window array storage; Python interpreter, allocator and host addressing costs are not timing claims. The multiple input arrays are scanned through monotonically advancing cursors. If an implementation charges an additional \(O(\log(nW+nt))\) bit operations per indexed window access, an explicit conservative supplement is

\[
O\!\left(nq\log(nW+nt)\right).\tag{10}
\]

It does not revive a same-scale multiplication. For growing \(L\) in the displayed \(L=O((\log N)^{4/5})\) conversion regime, this supplement is also \(o(N\log N)\), since its ratio is \(O(1/(L\log(L+1)))\). For bounded \(L\), a fixed finite Taylor circuit can instead use a constant number of sequential \(W\)-bit additions and fixed-small-integer multiplications, giving \(O(N)\). A uniform optional dispatcher can use direct binomial expansion whenever \(n\le\lceil\log_2\log_2(nW+4)\rceil\): its elementary shift/add cost is \(O(n^3W+n^3)\), whose ratio to \(nW\log(nW)\) tends to zero on that branch. On the other branch, the ratio from (10) tends to zero uniformly. This optional address-accounting dispatcher is a proved elementary construction, not an implemented or timed feature of the delivered reference stage. Thus the little-o conversion example is not dependent on declaring arbitrary-length addresses free.

## 4. The remaining scalar actions and their carry widths

For completeness, the inherited modular-division primitive used here is:

\[
b_r=((a_r-c_r)\bmod R)v\bmod R,
\qquad c_{r+1}=(u b_r+c_r-a_r)/R,
\]

where \(0<u<R\) is odd, \(v=u^{-1}\bmod R\), and \(a_r\) are input limbs. If \(0\le c_r<u\), the numerator is an exact multiple of \(R\) strictly between \(-R\) and \(uR\). Therefore \(0\le c_{r+1}<u\). Telescoping gives

\[
u\sum_{r<s}b_rR^r=\sum_{r<s}a_rR^r+c_sR^s,
\]

which proves the modular quotient after the last mask. Each limb uses exactly two \(t\)-bit products and \(O(1)\) bounded additions/subtractions. The ordinary truncated product primitive uses one \(t\)-bit product per limb with a bounded carry.

The present shift uses:

- \(nq\) local products for the \(u_i\) input multiplications;
- \(2nq\) local products for division by \(U\) at all outputs;
- \(2nq\) local products for division by \(u_j\) at all outputs.

These are exactly \(5nq\), apart from preparation. Even divisors equal to one go through this declared reference schedule; optional simplification is not assumed. Every inverse needed by those divisions was prepared in section 2. No \(W\)-bit modular inverse is formed anywhere. Signs, the shifts by at most \(g\), masks and centered reconstruction cost \(O(nW)\).

## 5. Complete cost and where the saving comes from

The full ledger, valid even when \(W<t\) before simplification, is

\[
\begin{split}
T(n,h)=O(&q\,\mathcal K(S)+nq\,\mathcal K(t)
+nt(\log(n+1))^a+t^\alpha\\
&+nqt+nW+n\log^2(n+1)),
\end{split}\tag{11}
\]

where \(\mathcal K(z)=O(z^\alpha)\) is explicit Karatsuba and \(S=\Theta(nt)\). All recursion children of that core have at most half the parent's width, rounded up; leaves at width at most 16 use binary shift/add. Thus (11) is independently terminating, with no call to the proposed Mersenne multiplier.

For \(W\ge t\), \(q\le2W/t\). Consequently

\[
q\mathcal K(S)=O(n^\alpha Wt^a)
=O(nW(nt)^a),
\]

and the diagonal contribution is \(O(nWt^a)\). Since \(t=\Theta(n\log(n+1))\), the first term dominates, yielding (1).

The old prescribed convolution had capacity \(S_{old}>2nW\). The new construction instead makes \(q\) calls of capacity \(\Theta(n^2\log(n+1))\). Relative to explicitly instantiating both constructions with the same Karatsuba upper-bound model, the dominant displayed bounds differ by

\[
\frac{(W/t)(nt)^\alpha}{(nW)^\alpha}
=(t/W)^a.
\]

It tends to zero when \(W/(n\log(n+1))\to\infty\). This compares proved construction bounds, not runtime measurements and not a lower bound for the old implementation.

The earlier noncontracting-child obstruction concerned literally substituting the whole Mersenne multiplier into an \(S_{old}>2N\) call. The new schedule does not perform that substitution. Its local convolution capacity is \(o(N)\) when \(m/(L\log(L+1))\to\infty\), and its chosen backend is independently terminating. This removes that particular circularity; it does not make the remaining matrix multiplication recursion contract by itself.

### A bounded optimization obstruction for this recipe

Within a recipe that packs one wide-input slab against the entire exact common-denominator kernel, merely changing slab width cannot improve the order of the homogeneous Karatsuba charge. If the kernel width is \(k\) and the slab width is \(r\), the charged expression is

\[
F(r)=\lceil W/r\rceil\,[n(r+k+g)]^\alpha.
\]

For \(W\ge k\) and \(k\ge g\),

\[
\inf_{r\ge1}F(r)=\Theta(n^\alpha Wk^a).
\]

For \(r\le k\), use \(W/r\ge W/k\) and \(r+k+g\ge k\); for \(r\ge k\), use \(F(r)\ge(W/r)(nr)^\alpha\). Choosing \(r=k\) attains the matching order. Moreover the exact denominator convention requires a multiple of \(U\), whose bit length is \(\Theta(n\log n)\): the upper bound was proved above, and the lower bound follows from \(\log_2((n-1)!)-(n-1)\) by retaining the largest half of the factorial factors. In particular \(K_0=U\) has that width.

This is optimization of an explicitly assigned cost expression and a common-denominator representation constraint. It is **not** a lower bound on actual multiplication, arbitrary fixed-kernel convolution, other denominator choices with additional structure, or other Taylor-shift constructions. To improve the \(L^{2a}\) exponent in this particular ledger, one must change more than its slab size.

## 6. Composition with p and p^d

The inherited exact quotient/carry streams and binary carries remain unchanged. Their complete output, final carry tails and possible extra \(p\)-digit are paid at \(O(N)\) under the inherited wide-digit interface.

For the global binary-to-\(p\), \(p\)-to-binary and raw-product shifts, \(n=O(L)\), \(W=O(m)\), and \(nW=O(N)\). The common-denominator width is now \(O(L\log(L+1))\). If \(m/(L\log(L+1))\to\infty\), all nontrivial actual shifts eventually satisfy \(W\ge t\), proving (2).

For grouping length \(d\le L\), \(O(L/d)\) actual-length shifts add at most

\[
O\!\left(N[d^2\log(d+1)]^a\right),
\]

which is no larger than the global term. Partial groups, raw grouped coefficients of \(O(dm+\log L)\) bits, bounded overlap after expansion, and a lone digit with \(d\) exceeding its actual length retain the accepted actual-width handling. No table of the declared length \(d\) is allocated for a lone shorter digit, and no powers \(p^d\) or general long divisions are treated as free.

For \(L=O((\log N)^\beta)\), \(\beta>0\),

\[
N[L^2\log(L+1)]^a
=O\!\left(N(\log N)^{2a\beta}(\log\log N)^a\right).
\]

It is little-o of \(N\log N\) whenever

\[
\beta<\frac1{2(\log_2 3-1)}\approx0.854756.
\]

The stated \(\beta=4/5\) is a simple concrete choice. The growth condition on \(m\) follows automatically in these polylogarithmic-\(L\) families because \(m=N/L\). Bounded \(L\) is linear-time as already noted. Strict-prime use remains conditional on supplied admissible parameters and their separately paid selection/validation.

The delivered program implements the new complete Taylor-shift stage. Conversion carry algorithms and the raw/grouped interface proofs are inherited accepted constructions. The finite full-value tests below use independent normalization oracles and do not mislabel a rerun of the historical carry code as a new implementation.

## 7. Fresh reproducible evidence and remaining work

Run `python fresh_controls.py` in this directory. Default production multiplications use only the fresh explicit Karatsuba core; test-driver native multiplication, factorial, binomial coefficients, powers and inverses are independent correctness oracles. No historical program was imported or run. No timings are used to infer complexity.

The fresh controls cover:

- signed Karatsuba products across leaf and split boundaries;
- exact odd-factorial/cofactor/microinverse tables;
- exhaustive small and random wider narrow-kernel convolutions, checking every coefficient, carry, prefix identity, exact packed-call count and argument-capacity bound;
- modular division, including partial limbs, every tested carry transition and exact local product counts;
- complete instrumented scalar ledgers, separating all preparation products, the exact 5nq local diagonal products and the exact q packed products;
- both signed Taylor shifts and inverses, including \(W<t\), \(W>t\), zero, empty and length-one cases;
- Mersenne positional/canonical round trips and grouped identities, including composite controls;
- negative controls for the omitted common denominator and omitted inter-slab carries;
- concrete shrinking-capacity ledgers, without claiming those metadata-only examples are complete timed multiplications.

`RESULTS.json` and `RUN.log` contain the completed finite counts and digest. `SOURCE_PINS.json` binds the read-only accepted reports and independent review that establish the inherited interface. `MANIFEST.json` binds this new artifact. This candidate still needs independent review.

The remaining full-target gates are matrix/transform schedules, correlated point-product cost, growing-prime selection when required, and a complete recursive multiplier composition. The new result closes only the complete conversion bill for the stated very-wide supplied families. It neither imports a whole fast multiplication algorithm as the proposed answer nor claims an arbitrary-input multiplication lower bound or an end-to-end sub-\(N\log N\) multiplier.
