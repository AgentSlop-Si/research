# Symmetric-node CRT recovery with only small residual divisors

Date: 18 October 2026 (Asia/Qyzylorda).

## Result and scope

The complete `multiply_paired_dyadic` producer replaces one bottom level of
weighted CRT reconstruction by a symmetric-node formula. Its only run-time
divisors after cancellation are divisors of the node gaps, hence below the
number of formal nodes. The large dyadic point acts by a binary shift.
Only one common weight is generated for each reflected pair, and a single
product tree serves input reduction and output reconstruction.

This is a concrete exact executor and a modest complete finite gain. It does
not reduce the outer child-product volume or remove a growing number of
Fourier/CRT levels. The retained independent-child packing obstruction remains
applicable because every outer multiplication is unchanged. No new asymptotic
multiplication or arbitrary-input FFT upper bound is claimed.

## 1. Setup and the paired identity

For `m>=1`, let

\[
D=\operatorname{lcm}(1,\ldots,m-1),\quad
 g_i=\gcd(P+i,D),\quad q_i=(P+i)/g_i,
\]

where the empty lcm is 1. The nontrivial cores are pairwise coprime.
Let `Q` be their product and

\[
C=\prod_i g_i,\quad H=C/(m-1)!,\quad
 t_i=(-1)^i H\binom{m-1}{i},\quad z_i=t_i/g_i.
\]

The preceding checkpoint proves that H and every z_i are integers and

\[
\sum_{i=0}^{m-1}z_iQ/q_i=1.
\]

The exact identity includes formal positions with `q_i=1`. For recovery
those positions may receive residue zero; dropping them changes only a
multiple of Q. These are the frozen integral CRT coefficients, not a new
assumption about arbitrary arithmetic progressions.

Pair `i` with `j=m-1-i`, with `i<j`, and put
`epsilon=(-1)^(m-1)`. Binomial symmetry gives `t_j=epsilon*t_i`.
For arbitrary canonical residues `a` at `q_i` and `b` at `q_j`, define

\[
U_i=a z_iq_j+b z_jq_i.
\]

This is the exact signed numerator contributed by those two leaves to
the old global cofactor sum. Substitution gives

\[
\boxed{
U_i=\frac{t_i}{g_i g_j}
 \left((P+i)(a+\epsilon b)+(j-i)a\right).
}
\]

For even m this uses a residue difference; for odd m it uses a sum.
The odd midpoint is handled once by its ordinary signed weight.

## 2. Every remaining divisor is small

Define

\[
c_i=\gcd(|t_i|,g_i g_j),\quad
 w_i=t_i/c_i,\quad d_i=g_i g_j/c_i.
\]

Since both `g_i|t_i` and `g_j|t_i`, their lcm divides `t_i`. Therefore

\[
\boxed{d_i\mid\gcd(g_i,g_j)\mid(j-i).}
\]

In particular `1<=d_i<m`. Both `P+i` and `j-i` are divisible by `d_i`,
so the bracket in the displayed paired identity is exactly divisible by
`d_i` for every pair of residues. Consequently the executor uses

\[
\boxed{
U_i=w_i\left[
\frac{(P+i)(a+\epsilon b)+(j-i)a}{d_i}
\right].
}
\]

It divides before multiplying by the common weight. The division is skipped
when `d_i=1`. This is stronger than merely asserting that a larger final
numerator is divisible by `g_i g_j`.

For `P=2^B`, construct the bracket as

\[
((a+\epsilon b)\ll B)+i(a+\epsilon b)+(j-i)a.
\]

The point multiplication is a shift. The other two multipliers and the
possible divisor are less than m. One multiplication by `w_i` remains.
Since `H|D`, the common weights have `O(m)` bits. No multiplication by
an `O(m)`-bit weight is treated as a unit-cost operation.

## 3. Complete reconstruction and one shared tree

Set `M_i=q_i*q_j` for each nontrivial reflected pair. The midpoint, when
active, has its single original modulus. Canonicalizing `U_i mod M_i` is
optional for correctness; the final producer does so for reflected pairs to limit the width
of the upper tree; an odd midpoint retains its signed weighted value.

Combine upper-tree children by

\[
S_v=M_R S_L+M_L S_R.
\]

At its root this is congruent to the old global sum
`sum_i r_i*z_i*Q/q_i` modulo Q. One root remainder returns the exact CRT
residue. The unchanged prior interval then chooses the unique signed
coefficient, and unchanged binary carries produce the integer product.

The full product tree is built with reflected pairs at the bottom.
Leaves retain their original residue-vector indices, while internal
`start,stop` values describe bounding spans. A span can be noncontiguous;
this does not change remainder descent, which writes only to distinct
indexed leaves. Every internal node contains at least two leaves, so its
bounding-span length exceeds one. The root span ends at the active count.
A second lightweight tree view reuses these same computed moduli for CRT
recovery. There is no duplicate modulus product tree in the final producer.

This distinction matters for the reciprocal-converter interface. Caching
nodes by `(start,stop)` can collide in a reflected tree. The converter now
keys its cache by the identity of a live node, with the tree retaining the
node lifetime. The independent bridge audit exercises actual repeated spans
and wide reciprocal edges. Natural interval-tree correctness was unaffected
by this interface correction.

## 4. What work is removed and what remains

For even m with all m cores active, each output coefficient previously used
m individual weight products and m leaf remainders, followed by `2(m-1)`
upper products. The paired executor uses m/2 common-weight products,
m/2 pair remainders, and `2(m/2-1)` upper products. In addition it pays
m/2 dyadic shifts, m small-index products, and at most m/2 divisions by
integers below m. The operand widths differ, so raw multiplication-call
counts alone are not used as an asymptotic speed estimate.

The pair-native setup generates only the first half of the binomial row.
It never creates individual canonical CRT inverse residues. The final
core gcds are retained from coverage construction; the pair constructor
does not recompute them. All factorial products, scale division, pair
cancellations, product-tree nodes and output stages are counted and timed.

The higher CRT levels still multiply growing integers and perform the
ordinary final interval recovery. Their asymptotic cost remains a balanced
reconstruction bound. The complete outer convolution calls, their operand
widths, and their total bit volume are exactly the frozen calls. Thus the
previous independent-child lower estimate `(4-o(1))N` for that packing
executor has not been bypassed.

## 5. Complete matched observations

`paired_direct_benchmark.json` contains 80 complete products: four methods,
five retained input sizes, and four cyclic-order repetitions. Each call
constructs and pays for its own point, coverage, tree, weights, input
conversion, outer products, recovery and binary output. The independent
integer-product oracle runs after the producer returns. Source and input
hashes are checked, and point/block/modulus/outer-work equality is asserted.

Times below are complete median milliseconds, with packed outer products.

| Bits per operand | Frozen prior | Paired | Prior/paired |
|---:|---:|---:|---:|
| 610 | 1.352 | 1.370 | 0.9873× |
| 2,959 | 2.809 | 2.532 | 1.1095× |
| 12,553 | 6.274 | 6.065 | 1.0344× |
| 51,040 | 21.026 | 20.260 | 1.0378× |
| 206,716 | 151.572 | 148.815 | 1.0185× |

At the largest retained size, complete packed time decreases by 1.8190%.
CRT recovery decreases from 36.842 ms to 34.853 ms. Only 2 of the 128
pairs require any exact gap division; the largest divisor has 7 bits,
versus a maximum original core width of 547 bits. The largest cancelled
common weight has 396 bits.

The largest NTT-backed comparison is 451.026 ms to 442.467 ms, with both
executing exactly 500,436 butterflies. Smaller NTT cases include regressions,
and the smallest packed case also regresses. The small improvement is not
presented as a universal runtime guarantee or a record against an external
optimized multiplication library.

An early prototype built a second product tree and divided only after the
large common-weight product. In an exploratory largest case it reduced the
CRT stage but increased complete time. Those exploratory numbers were not
mixed into this final matched benchmark. The final single-tree and cancelled
implementation is the only producer used by the retained table.

## 6. Verification and APIs

Run:

```bash
python3 fft_advance_next/newton_bridge/verify_paired_recovery.py
python3 fft_advance_next/newton_bridge/audit_reciprocal_bridge.py
python3 fft_advance_next/newton_bridge/benchmark_paired_direct.py
```

The pair verification covers 1,029 core families, 6,174 independent CRT
vectors, 2,050 signed remainder vectors through reflected trees, 8,468 gap
divisor controls, and 132 complete signed products. It includes odd counts,
missing unit cores, the all-trivial case, general integer points for the
formula, both retained outer backends, and centered input blocks.

The independent references use incremental CRT with modular inverses,
direct global cofactor sums, and ordinary integer products. They do not
use the paired reconstruction identity as their endpoint oracle.

```python
from paired_direct import multiply_paired_dyadic
product, report = multiply_paired_dyadic(a, b, rank=None, block_bits=None,
                                       outer_backend='packed', centered=False)

from combined_direct import multiply_combined_dyadic
product, report = multiply_combined_dyadic(a, b, rank=None, block_bits=None,
                                         outer_backend='packed', centered=False,
                                         conversion='auto')
```

The second wrapper additionally uses the independently developed paid
reciprocal residue converter. Its exact endpoint and four-way matched
evidence are separate from the pair-only table above.

## 7. Prior material and novelty boundary

The underlying Lagrange/barycentric interpolation identities, equidistant
binomial weights, and CRT sum trees are classical. The source-relative
contribution established here is the explicit cancellation to gap divisors,
its pair-native producer, and the complete shared-tree execution in this
retained stripped-core pipeline. Historical priority for this specialization
has not been established.

Primary context:

* [Farhi, arithmetic-progression lcm identities](https://arxiv.org/abs/0803.0290)
  supplies the earlier partial-fraction identity underlying the retained
  integral weights; the prior checkpoint already records this attribution.
* [Bostan and Schost, Polynomial evaluation and interpolation on special sets of points](https://mathexp.eu/bostan/publications/BoSc05.pdf)
  provides the established fast special-node evaluation/interpolation context.
* [van der Hoeven, Faster Chinese remaindering](https://www.texmacs.org/joris/chinese/chinese.html)
  gives established product-tree and FFT-trading context. Its fixed-modulus
  asymptotic machinery is not silently credited as a new bound here.

The earlier Newton refinement and denominator closures were read before
this branch. We have not assumed free Newton basis conversion, free
independent residue packing, or shared arbitrary input columns.
