# Constructive decoding with original-input side information

**Result:** two verified, fresh-input, full-output exact DFT fast paths run in
O(N) scalar work on explicitly certified structured classes. A conductor-wise
hybrid uses the Galois-defect route wherever it is cheaper and otherwise runs
the ordinary modulated half-size FFT. Its general worst-case bound remains
O(N log N). Neither construction improves the main arbitrary-input bound.

This responds to the new joint-orbit and global-bottleneck `NEXT_GATE` files.
The new algorithms retain and inspect the original coefficients. They do not
decode a complete arbitrary spectrum from a few representative scalars, use
Galois-automorphism oracles, or hide the transform in a large-integer product.
The identities below are elementary; this package makes no priority claim.

## 1. Sparse defects of a coefficient permutation

Let q be a power of two, m=q/2, and let v be the current length-q vector.
Split it into

    s_j=v_j+v_(j+m),       r_j=v_j−v_(j+m),  0≤j<m.

Even Fourier outputs are the length-m DFT of s. Odd outputs are

    Y_k = sum_(j=0..m−1) r_j zeta_q^(kj),  k odd.

Define P_5 on the m coefficients by substitution z→z^5 modulo z^m+1.
Explicitly, send coefficient r_j to index (5j mod q) mod m, negating it when
5j mod q is at least m. This is a signed permutation, computed with m reads,
m writes and at most m negations. Form the exact defect

    d=(P_5−I)r.

For every odd k, the following evaluation identity holds for arbitrary
complex coefficients, not just rational coefficients:

    Y_(5k mod q) − Y_k = sum_j d_j zeta_q^(kj) =: D_k.       (1)

No operation applies a field automorphism to a numerically encoded scalar.
The action is explicitly performed on the retained coefficient vector.

For q≥4, multiplication by 5 partitions the odd indices into two cycles,
with representatives 1 and 3 and length L=q/4. Indeed,
v_2(5^(2^h)−1)=h+2 follows by squaring, so 5 has order q/4 modulo q.
Its powers enumerate the 1 mod 4 indices, and three times these powers
enumerate the 3 mod 4 indices. At q=4 the cycles are singletons.

Compute Y_1 and Y_3 directly from r. If d has s nonzeros, compute all m
values D_k by sparse direct evaluation. Then use (1) to walk both cycles.
This costs O(q(s+1)) scalar work and explicitly writes all m odd outputs.
The q=2 odd output is simply r_0.

Repeat on the even-sum vector s. The sizes q=N,N/2,...,2 sum to less than
2N. All pair sums, differences, signed actions and zero tests therefore cost
O(N), including discovering each defect support from the fresh input.
Retained reduced vectors occupy N−1 scalars. Every original output is
written once: its unique conductor q contributes the odd index k at global
position kN/q, and the final scalar supplies DC.

**Restricted exact theorem.** If the discovered support at every q≥4 is
at most S, the complete fresh-input transform takes O(N(S+1)) field/scalar
operations and O(N) scalar workspace, including discovery, a prepared root
table and all N outputs. For fixed S this is O(N).

The implementation `transform(..., max_defect=S)` verifies the condition.
If it fails, it runs a complete radix-two DFT after at most O(N) discovery
overhead. No supplied pattern or related-input cache is trusted.

## 2. A useful adaptive hybrid

The odd outputs also satisfy

    Y_(2t+1) = DFT_m( (r_j zeta_q^j)_j )[t].

This is the requested same-output comparison with the modulated m-point FFT.
After discovery, the two emitted costs at conductor q≥4 are exactly

    orbit:         5m + 2ms − 2,
    modulated FFT: m + (3/2)m log2(m),

counting each field addition, subtraction and multiplication as one.
`hybrid_transform` chooses the smaller cost separately for each conductor.
All its subtransforms share the explicitly prepared N-entry root table;
strided indexing does not require new root oracles or tables. It preserves
useful cheap levels even when other levels have dense defects.

Let nu be the number of signed-permutation negations executed in discovery,
and T=sum_(q≥4)(q/2)s_q. For N≥2, the all-orbit implementation emits exactly

    9N − 12 + 2T + nu

field operations, including the implemented root-order validation and all
root-power preparation. Here nu≤N−2 and T≤S(N−2). Each anchor is accumulated
from zero, so even additions of zero are charged. Input scans, zero tests,
routing, comparisons, copies and output traffic are additional O(N(S+1))
word operations; the counter vector records the main categories, not CPU time.

The fresh radix-two comparator emits N+2 log2(N)+(3/2)N log2(N) field
operations with the same root validation and preparation. The hybrid is at
most this count plus N−3+nu, hence has at most O(N) added scalar work on an
arbitrary input. It remains O(N) on the bounded-S class. This is a choice
between these two actual evaluators, not a claim of global circuit optimality
or identical cost per operation in a bit model.

## 3. A nonempty dense family and stable orbit walking

The support condition is constructive. At q≥8 take an odd-coordinate basis
vector e_1 and set

    r = a sum_(h=0..q/8−1) P_5^h e_1.

Because 5^(q/8)=1+q/2 modulo q, P_5^(q/8)e_1=−e_1 and therefore

    (P_5−I)r = −2a e_1.

The defect has support one although r has q/8 nonzero coefficients. Choose
such reduced vectors independently at successive conductors, choose the
final DC scalar, and invert the pair-sum/difference steps using division by
two. Generic choices over C give dense original inputs; the audit checks
30 examples with every input entry nonzero. These examples do not give an
algorithm for arbitrary dense data.

There is no exponentially unstable measurement-only decoding step. If each
anchor has absolute error at most alpha, each computed D_k has error at most
eta, and each orbit addition contributes absolute error at most gamma, then
every recovered output in that conductor has error at most

    alpha + (q/4−1)(eta+gamma).

The amplification is polynomial. This bound includes errors in roots or
earlier coefficient work only insofar as those are included in alpha and
eta; it is not a floating-point error certification of the modular prototype.

A further analytic certificate allows approximate defect sparsity. If an
omitted defect tail has l1 norm tau_q, sparse evaluation changes each D_k by
at most tau_q, so with exact anchors the odd-output error is at most
(q/4−1)tau_q. The groups of output bins are disjoint, so the full-spectrum
bound is the maximum over conductors. This optional truncation certificate
is proved here but not implemented; the executable fast path accepts exact
zeros only. It gives no arbitrary-input approximate complexity improvement.

The accepted class is small. For each fixed defect-support pattern, the
preimage of that support under P_5−I has dimension at most S+2, because
ker(P_5−I) has dimension two (one constant per odd frequency cycle).
The dyadic sum/difference coordinates form an invertible decomposition.
Thus a fixed support pattern across all levels has O((S+2)log N) free
parameters, not an N-dimensional open set. This is why the new global rank
theorem remains intact.

## 4. A second full-output route: binary-index tensors

`tensor/` contains an independently implemented and audited fast path.
If the explicit fresh input verifies

    x_j = c product_(l=0..d−1) a_l(j_l),  N=2^d,

its generating polynomial is

    X(z)=c product_l (a_l(0)+a_l(1)z^(2^l)).

At the N roots, suffix products repeat on successively smaller frequency
sets. Computing these suffixes needs only sum_l 2^(d−l)=2N−2 evaluations,
not an N-by-log(N) unshared product. The algorithm finds a pivot, proposes
factors from its bit neighbors, regenerates all N input entries, checks each
one, prepares all root powers, and returns all N Fourier values.

For nonzero accepted inputs N≥2, it charges 6N−7+2log2(N) modular
multiplications, 2N−2 additions and one inversion, plus linear scans,
comparisons and routing. A decline returns `None` so a caller can retain the
original input and invoke a general transform. The complex max-magnitude
pivot stability theorem and the implemented first-nonzero modular pivot
are explicitly separated in `tensor/README.md`.

This tensor identity is not a primitive-frequency measurement decoder.
It applies to a low-dimensional structured class. Its binary instances
do not contain the arbitrary binary family used by the new packing bounds.

## 5. Exact-complex versus bit costs

The Galois identity holds over C, but arbitrary exact complex values are
formal scalar registers in that model. Neither Python implementation claims
to encode arbitrary exact complex numbers in fixed precision.

The Galois prototype uses a caller-certified odd prime p and a supplied
primitive Nth root. It checks the root order with charged modular products
and prepares the entire power table. It does not prove primality or discover
the supplied root. The same hypotheses apply to its radix-two comparator.
If the root must instead be constructed from a supplied primitive generator,
binary exponentiation costs O(log p) additional modular multiplications;
prime/root discovery or certification is a separate cost for both methods.
An order test alone is not a principal-root test in arbitrary composite
rings; the prototype does not claim that extension. The tensor implementation
uses the stronger dyadic half-power test and also requires a unit pivot.

With b-bit residues, let M_mod(b) be the paid cost of modular multiplication
including reduction, and M_int(log N) the cost of multiplying two index
integers. The bounded-S Galois route costs

    O(N(S+1)(M_mod(b)+b+M_int(log N)) + N log N)

bits of work, including the variable products j*k used to index sparse
twiddles. Its storage is O(N(b+log N)) bits. Schoolbook arithmetic gives the
simpler upper bound O(N(S+1)b^2), since b≥log2(N+1). Under the usual monotone
costs where M_mod(b) dominates M_int(log N), the explicit index-product term
can also be absorbed in M_mod(b).
The tensor route adds one paid b-bit modular inversion. No growing field
element is a unit-cost bit operation. For prime fields supporting length N,
b≥log2(N+1), so even N explicit residues require Omega(N log N) output bits.
Fixed-prime finite tests are not themselves an asymptotic field family.

## 6. Verification and current outcome

Run `python3 run_audit.py` and `python3 tensor/run_audit.py` using the standard
library. Original attached source packages were read but not executed or
modified. The new Galois implementation was inspected before its first run.

The Galois audit passes 30 dense structured inputs through N=1024, 21
independent direct-DFT comparisons, 62 independent orbit identities, four
generic fallbacks, 12 zero-cap controls, six invalid-argument checks and 34
complete hybrid comparisons. Tensor audit: 291 full-output exact cases through
N=4096, 18 unstructured declines and eight invalid cases. These are exact
functional and operation-count checks, not wall-time benchmarks.

For one structured example at each size, all-orbit field counts versus the
fully prepared radix-two comparator are 1438 vs 1486 at N=128, 2898 vs 3344
at N=256, and 11652 vs 16404 at N=1024. The growing-family statement is the
proved O(N) restricted bound, not those finite constant-factor comparisons.

**Main goal unchanged:** no fresh arbitrary-input exact O(N) FFT, no general
sub-N-log-N improvement, and no integer-multiplication breakthrough. The
useful new output is an explicit, paid orbit decoder that becomes cheap when
the retained coefficient state supplies sparse defects, plus a separate
verified tensor evaluator and an adaptive exact hybrid.
