# Complete cost of the outside-CRT route

Date: 2026-10-17. Scope: the retained binomial encoding, exact local integer
maps, ordinary scalar outer convolutions, and exact binary output.

## Findings

Moving the local maps outside CRT is an effective finite improvement. It does
not remove the long outer transforms. The conventional, explicitly executed
outer-NTT architecture still has an `Omega(N log N)` word-processing cost in
the growing-block parameter regime. This is an architecture-specific statement,
not a lower bound for unrestricted multiplication or unrestricted Fourier
circuits.

There is a complete all-size alternative: compute the scalar outer
convolutions by signed Kronecker substitution. It has no prime, root, or CRT
supply problem, and with the established 2021 multiplier gives a full
`O(N log N)` bound for this construction. All local conversion, evaluation,
packing, and data rearrangement costs fit `O(N (log log N)^2)` for the stated
parameters. The packed outer multiplications themselves have total argument
volume `Theta(N)` and arguments of size `Theta(N/log N)`. Their logarithmic
cost has therefore not disappeared.

The ordinary-product interface has exact bilinear rank `2r-1`. Consequently,
replacing the `3r` scalar products of the derivative representation with
`2r-1` ordinary value products is possible, and is optimal within the stated
linear evaluation/interpolation interface. It changes a constant. It cannot
remove a growing factor in the number of independent scalar products.

## 1. Uniform parameters and point production

Let `r>=2` be the inner rank. Let `P=1+k L_r` be the exact native point from
`minimal_denominator.make_plan`, where

\[
 L_r=\operatorname{lcm}(1,\ldots,r),\qquad d=L_r/r.
\]

The producer chooses `1<=k<=max(1,d-1)` in a specified CRT class. Hence

\[
 \log P=\Theta(r),\qquad \log d=O(r).
\]

Here the elementary estimates `log L_r=Theta(r)` suffice. For example,
central binomial coefficients supply an exponential lower bound and their
usual prime-valuation argument supplies an exponential upper bound. No
conjecture concerning large primes is used in constructing this point.

The retained inner radices are

\[
 R_j=1+(P-1)/j\quad(1\le j\le r),\qquad
 \beta=\frac1d\prod_{j=1}^{r}R_j.
\]

Write `s=floor(log_2 beta)` and use binary outer radix `rho=2^s`. Then

\[
 s=r\log_2P-O(r\log r)=\Theta(r^2).
\tag{1}
\]

An `N`-bit input needs `L=ceil(N/s)` blocks. For sufficiently large `N`, take
`r=floor(log_2 N)`; finitely many smaller sizes can use a fixed elementary
base case. Thus

\[
 r=\Theta(\log N),\quad L=\Theta(N/r^2),\quad
 \log L=\Theta(\log N),\quad N=\Theta(Lr^2).
\tag{2}
\]

Sieve or trial-divide integers only up to `r`, form the LCM, use extended GCD
for the small-prime-power CRT, and form the radix/product trees. The entire
point and tree producer costs `r^{O(1)}` bit operations with elementary
algorithms; all its integers have polynomially many bits in `r`. Under (2),
this is a one-time `polylog(N)` cost, absorbed in the final bound. Capacity
tuning is unnecessary for the all-size theorem. The finite benchmark may
retain its capacity-tuned plan for matched comparisons.

This proof does not extend the finite `p<2^31` NTT-prime loop by assertion.
Those primes serve a different purpose from the small primes used to make
the point.

## 2. Exact jets, heights, and local work

In falling coordinates put

\[
 a_i=A(i),\quad u_i=T A'(i),\quad T=rd,
\]

and similarly `c_i,v_i` for the second input. Since
`lcm(1,...,r-1)` divides `T`, the scaled derivatives are integral.
The input binomial coefficients have `O(r)` bits. Both the Pascal row norms
and the scale `T` contribute only `O(r)` further bits. All jet input values
therefore have `h=O(r)` bits.

The required scalar outer polynomials are

\[
 p_i=a_i c_i,\qquad e_i=u_i c_i+a_i v_i.
\tag{3}
\]

Their coefficient heights are

\[
 H=O(r+\log L).
\tag{4}
\]

The integer postprocessing formula is

\[
 H_i=J_i e_i-
 \sum_{j\ne i}\frac{T}{i-j}J_jp_j-(T h_i)J_ip_i,
\]

where `J_i=(-1)^(i+1) binom(r-1,i)` and
`h_i=Harmonic(i)-Harmonic(r-1-i)`. Every coefficient is integral, and the
fixed Cauchy kernel can be handled as a signed integer convolution.

Let `M(t)` be a regular integer-multiplication cost bound, with fast division
available at comparable cost. Clearing factorial denominators in the exact
input maps produces `O(r)` coefficients of `O(r log r)` bits. Their packed
convolutions have `O(r^2 log r)` bits, and the diagonal products/divisions have
a safe additional cost `O(r M(r log r))`. Thus

\[
 C_{\rm input}(r)=O(M(r^2\log r)+rM(r\log r)).
\tag{5}
\]

For postprocessing and direct integer Lagrange evaluation a safe bound is

\[
 C_{\rm output}(r,H)=O(M(r(r+H))\log r+rM(r+H)).
\tag{6}
\]

The factor `rH` in (6) is necessary: there are `r` input values, each with
`H` bits. It must not be replaced with a single `H`-bit contribution.
Balanced inner decoding fits `O(M(r^2) log r)`. Binary carries have
`O(s+log L)` bits and binary packing costs `O(N+L log L)`.

With (2), (4) gives `H=O(r)`. Taking the established
`M(t)=O(t log t)` subroutine in (5)-(6), all these block-local operations
cost

\[
 O(Lr^2(\log r)^2)=O(N(\log\log N)^2).
\tag{7}
\]

That estimate includes an integer product by `beta` for each output block;
it does not assign zero cost to large signed intermediate evaluations.

## 3. What the conventional NTT/CRT executor costs

Let `ell=nextpow2(L_A+L_C-1)=Theta(L)`. Let the selected prime fields have
bit widths `w_1,...,w_q`, total width `W=sum w_j`, and enough total modulus
for the input-only interval certificate. The per-prime jet core has
`6r` length-`ell` NTTs and `3r ell` scalar point products. A safe arithmetic
upper bound is

\[
 O\left(r\ell\log\ell\sum_{j=1}^{q}M(w_j)\right).
\tag{8}
\]

Let `G(ell,H)` denote the actual cost of producing the requisite primes,
primitive roots, and their certificates. A complete accounting must also
include input reductions, root/twiddle preparation, and reconstruction.
Using shared product/remainder trees, the many-coefficient CRT interface
can be bounded by

\[
 O(rL M(W)\log(q+1))+O(M(W)\log(q+1)).
\tag{9}
\]

The incremental CRT in the finite prototype is an executed alternative,
but its growing operands do not justify the tree bound unless the producer
is actually changed. Formula (9) describes a valid available all-size
replacement, not the precise loop cost of the prototype.

Adding (5)-(9), point setup, coefficient scans, output evaluation, and data
movement yields the complete schematic upper bound

\[
\begin{split}
T_{\rm NTT}(N)\le{}&r^{O(1)}+
 O\bigl(L C_{\rm input}(r)+L C_{\rm output}(r,H)\bigr)\\
 &+G(\ell,H)+
 O\left(r\ell\log\ell\sum_j M(w_j)\right)\\
 &+O(rL M(W)\log(q+1))+
 O(rLH\log r+N+L\log L).
\end{split}
\tag{10}
\]

In a fixed-tape implementation the `r`-by-`L` arrays must be available in
both node-major and block-major order. Standard recursive transposition
along the smaller dimension costs `O(rLH log r)`, already present in (10).
There is no unit-cost arbitrary-address assumption hidden in that term.

### Architecture-specific barrier

Assume the executor explicitly processes full `w_j`-bit residue records at
every butterfly, as the retained conventional transforms do. Each level
processes `Theta(r ell w_j)` bits, for `Theta(log ell)` levels. Its cost is
therefore at least

\[
 \Omega(r\ell\log\ell\,W).
\tag{11}
\]

For the actual interval producer, use the following legal input family:
each operand contains at least one all-zero inner block and at least one
constant-only block `P-1`. These are legal because the first radix is `P`
and both values lie below the binary block capacity for all sufficiently
large ranks. Fill the other blocks with generic legal polynomials and end
with a nonzero block, so input length is `Theta(Lr^2)` and nodal rows need
not coincide.

At every node the input range then contains both `0` and `P-1`. Its product
interval contains `[0,(P-1)^2]`. The executor's global per-node input-range
certificate multiplies that interval by the maximum outer overlap
`Theta(L)`, yielding width at least `Theta(L(P-1)^2)`. Consequently the
required modulus at every node has `Omega(r+log L)` bits. This proves the
same bound with either a common modulus width `W` or separate node widths
`W_i`. Under (2), (11) becomes

\[
 \boxed{\Omega(N\log N).}
\tag{12}
\]

Large magnitude alone would not prove this: if all blocks were the same
constant polynomial, an endpoint-based interval certificate could have
width zero. The explicit zero-plus-nonzero family is essential. Likewise,
this is a statement about the specified interval producer and full-word
transform executor, not about every possible certificate or an algorithm
that can skip repeated rows or change representation.

Splitting the same reconstruction precision among more smaller primes
does not change this conclusion: the sum `W` remains. Node-specific
precisions also retain this worst-case requirement at every node.

The theorem concerns this explicit layer-by-layer, full-residue-word
architecture. It is not a claim that each abstract field operation has a
universal linear bit lower bound, nor a lower bound for algorithms that
compress several transform layers, exploit another representation, or avoid
these transforms. It remains true if all local maps and prime setup were
free, because it counts an already mandatory executed portion of this
particular schedule.

## 4. A complete prime-free alternative

The file `packed_outer.py` implements signed Kronecker substitution for an
ordinary scalar outer convolution. For input coefficient maxima `A,B` and
overlap `K=min(L_A,L_C)`, choose a power-of-two slot base `Q=2^w` satisfying

\[
 Q>2KAB.
\tag{13}
\]

Every coefficient of the product lies strictly between `-Q/2` and `Q/2`.
Evaluate both coefficient lists at `Q`, multiply the resulting signed
integers, then extract the centered base-`Q` coefficients. The actual
source rounds `w` up to a multiple of eight. This adds at most seven bits
per slot and makes bounded byte-window processing direct.

Signed input packing is the difference of two nonnegative byte streams.
For the output, form the fixed-length two's-complement stream once and
scan its slots with a one-bit carry. No loop repeatedly divides or shifts
the whole packed integer. Every output coefficient is checked against the
prior bound `KAB`. Negative final products are explicitly checked by the
terminal carry.

If input heights are at most `h`, then

\[
 w=O(2h+\log L),\qquad
 C_{\rm conv}(L,h)=O(M(L(2h+\log L))+L(2h+\log L)).
\tag{14}
\]

Using three ordinary products per node gives the jet completion

\[
\boxed{
T_{\rm packed}(N)\le
 3rM(C L(r+\log L))+
 O(N(\log\log N)^2)+r^{O(1)}
}
\tag{15}
\]

for a fixed constant `C` and parameters (2). The linear stream packing,
certificate scans, both transpositions, integer pre/post maps, exact
division, binary carrying, and plan production are all covered above.
Prime, root, and CRT costs are absent because this version performs none.

The implemented values-only alternative uses `2r-1` products in place of
`3r`. Its centered node offset is `O(r)`, so the same `O(r)` input-height
bound applies. The final recursive integer value map in
`recursive_pascal.py` replaces (5) with

\[
 C_{\rm input,recursive}(r,h)=O(M(r(h+r))\log r).
\tag{15a}
\]

It has peak packed size `O(r(h+r))`, avoiding the additional factorial
`log r` in intermediate coefficient height. Equation (15a), both output
evaluations, layout rearrangements, and all setup still fit the stated
`O(N(log log N)^2)` local allowance. The complete values-only packed backend
therefore satisfies (16) as well. The proof and exact-integer controls for
this final local producer are in `RECURSIVE_PASCAL_THEOREM.md`.

With the specified established `M(t)=O(t log t)` subroutine, (15) gives

\[
 \boxed{T_{\rm packed}(N)=O(N\log N).}
\tag{16}
\]

This is an unconditional all-size completion of this algebraic route using
that subroutine. It is not an improvement over the subroutine's order.
No assertion about the best current literature bound is needed to state it.
The reference uses Python's integer multiplication for each explicitly
reported call; it does not claim that CPython implements the 2021 asymptotic
algorithm.

## 5. Optimal bilinear compression of the inner ordinary product

Over any infinite field of characteristic zero, including `Q(Y)`, let

\[
 \mu:K[X]_{<r}\times K[X]_{<r}\to K[X]_{<2r-1},\quad
 \mu(A,C)=AC.
\]

Suppose `mu` is written as `R` products of one scalar linear form in `A`
and one in `C`, followed by linear output reconstruction. Then the image
span has dimension at most `R`. The products `X^i X^j` include every
monomial `1,X,...,X^(2r-2)`, so the image span has dimension `2r-1`.
Therefore `R>=2r-1`.

Conversely, evaluate at any `2r-1` distinct field points, multiply the
values, and interpolate. The nonzero Vandermonde determinant proves that
this gives `R=2r-1`. Thus

\[
 \boxed{\operatorname{rank}(\mu)=2r-1.}
\tag{17}
\]

The pair `(P,H)` is an invertible linear coordinate system for the same
ordinary product, since `AC=P+(B_r/d)H`. Hence the same lower bound applies
to any interface that reconstructs both pieces. The jet approach's `3r`
products are not rank-optimal; ordinary evaluation at `2r-1` falling nodes
attains the lower bound and avoids derivative denominators. This is
classical evaluation/interpolation, useful here as a concrete alternative.

This does not exclude a lower-cost algorithm that reconstructs only the
final binary answer, uses nonlinear bounded-integer decoding, or changes
what constitutes a scalar product. It does exclude a sublinear-in-`r`
number of scalar products obtained merely by a different linear basis for
the full ordinary-product output.

## 6. Why recursively packing the remaining products does not close a saving

Consider the rank-optimal values-only version with `m=2r-1` nodes, balanced
outer length `L`, and node-specific slot widths `w_i`. Each scalar product
has an allocated operand size `t_i=Lw_i`. A recursive implementation that
uses itself on those integer products would be estimated by

\[
 T(N)\le\sum_{i=0}^{m-1}T(t_i)+F(N).
\tag{18}
\]

It is insufficient to count only `m` products and argue that each is
smaller. Their total operand volume matters. Use legal inputs containing
both a zero block and a constant-only block `P-1`, as in Section 3. Every
node has maximum absolute input value at least `P-1`. The implemented
symmetric signed packing rule (13) therefore requires

\[
 w_i\ge 2\log_2(P-1)+\log_2L+O(1).
\]

Also `s<=r log_2 P` for the retained integer minimum scale. Consequently,
even before Pascal growth and byte rounding, the ratio satisfies

\[
 \frac{\sum_i t_i}{Ls}
 \ge
 \frac{2r-1}{r}
 \frac{2\log_2(P-1)+\log_2L+O(1)}{\log_2P}
 \ge 4-o(1).
\tag{19}
\]

With (2), each `t_i=Theta(N/r)`, so
`log t_i/log N -> 1`. For any fixed exponent `alpha`, substituting a proposed
majorant `N(log N)^alpha` into the right-hand side of (18) gives a leading
ratio at least `4-o(1)`. Thus this direct recurrence does not establish any
fixed power saving in `log N`. It has no volume contraction.

This is a failure of this proof route, not a lower bound derived from an
upper-bound recurrence. Additional reuse between child multiplications or
a substantially different packing/recovery representation would need its
own producer and its own cost analysis.

The exact cap experiment in `packing_validation.json` uses native plans,
`L=2^r`, separate node widths, and ordinary radix caps. It does not allocate
the exponentially long arrays. It evaluates the exact slot formulas:

| Rank | Nodes | Binary block bits | Sum of node slot widths | Child operand volume / N |
|---:|---:|---:|---:|---:|
| 32 | 63 | 2,595 | 16,616 | 6.4031 |
| 64 | 127 | 10,542 | 66,936 | 6.3495 |
| 128 | 255 | 45,087 | 279,024 | 6.1886 |
| 256 | 511 | 181,131 | 1,118,520 | 6.1752 |

These are certified allocations for a declared full-cap family, not runtime
measurements and not a universal lower bound on every possible packing.
The calculation already permits different precisions at different nodes.

## 7. Reproducible checks

Run:

```bash
python3 fft_outside_crt/asymptotic/verify_packed_outer.py
```

The saved evidence reports 350 independent signed scalar convolutions,
84 jet-array products, 84 values-array products, and exact output-span /
Vandermonde witnesses at ranks 2 through 32. Tests include negative leading
coefficients, carry boundaries, zeros, unequal lengths, and coefficients up
to 1,024 bits. Every nonzero packed scalar convolution reports both the
allocated and actual integer-multiplication operand lengths. Its independent
reference is ordinary coefficient-by-coefficient polynomial multiplication.

## 8. Sources and historical scope

The packing, ordinary evaluation/interpolation, and general cost ingredients
are classical; these notes do not claim them as new mathematical results.
They provide a complete accounting and explicit limitation for this retained
construction.

- Harvey, van der Hoeven, Lecerf, *Even faster integer multiplication*,
  Sections 2.1, 2.3 and 2.6 (array movement, transforms, and packing):
  <https://www.texmacs.org/joris/mul/mul.html>.
- Harvey and van der Hoeven, *Integer multiplication in time O(n log n)*,
  Annals of Mathematics 193 (2021), 563-617. This is the specified ordinary
  subroutine used for (7) and (16):
  <https://annals.math.princeton.edu/2021/193-2/p04>.
- Bostan and Schost, *Polynomial evaluation and interpolation on special
  sets of points* (2005), for fast special-node transforms:
  <https://mathexp.eu/bostan/publications/BoSc05.pdf>.

The current September 2026 OpenAI preprint makes a separate all-size
sub-NlogN theorem claim. `CURRENT_PRIOR_WORK.md` records exactly what was
read, without importing its method into this construction or asserting that
its long proof was independently verified here.
