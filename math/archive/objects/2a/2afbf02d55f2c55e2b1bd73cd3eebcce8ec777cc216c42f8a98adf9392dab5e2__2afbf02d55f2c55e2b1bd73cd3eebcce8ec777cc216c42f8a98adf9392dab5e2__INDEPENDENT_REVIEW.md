# Independent review: prime-free correction backend

Reviewed `fermat_backend.py`, `correction_graph.py`, the imported helpers in
`graph_kernels.py`, `run_audit.py`, and the README. The algebra and implementation
support exact finite-length multiplication and the stated restricted reuse
result. They do not establish a better general multiplication complexity.

## Ring and transform

The program uses a dyadic length m at least 2n−1 (m=2 for n=1), a positive
multiple t of m/2, and P=2^t+1 greater than the largest nonnegative convolution
coefficient C=n(beta−1)^2. Consequently omega=2^(2t/m) satisfies
omega^m=1 and omega^(m/2)=−1 even when P is composite.

For d=2^s u nonzero modulo m, with u odd, translating the root sum by
m/2^(s+1) negates it. The translation decomposes into even cycles whose
alternating terms cancel; equivalently S=−S implies S=0 because 2 is a unit
modulo odd P. This supplies the principal-root condition needed by the DFT,
not merely an assertion about multiplicative order. Since m is a power of
two, its inverse exists and equals 2^(−log2 m). Thus the radix-two inverse
and the convolution theorem remain valid in this possibly composite ring.

All stage shifts are integral because every stage width divides m and m
divides 2t. Bit reversal and the positive-exponent forward convention match
the direct DFT convention in the audit. No hidden primality or CRT step is
required.

## Arithmetic endpoints and exact recovery

For canonical 0≤v≤2^t and 0<r<t, `rotate` computes

    ((v << r) & (2^t−1)) − (v >> (t−r))

and adds P once if negative. Its range requires at most this single
correction. In particular v=2^t represents −1 and maps to P−2^r, as required;
it is not accidentally treated as zero. Reducing signed exponents modulo 2t
and applying the optional negation also handles r=0 and the special residue
correctly.

For pointwise operands a,b≤2^t, the product is at most 2^(2t). Its folded
value lies in [−2^t,2^t−1], so a single conditional addition gives its canonical
residue. At the maximum endpoint a=b=2^t, this produces 1. The optional
schoolbook path computes the same nonnegative integer product before folding.

Zero padding prevents convolution wraparound. Every true coefficient lies
in [0,C] with C<P, so the recovered canonical residue is the coefficient
itself. The signed carry pass uses Euclidean `divmod` with positive beta;
its final zero carry follows because the represented product lies in
[0,beta^(2n)). This also explains why locally negative correction
coefficients are safe.

## Reuse and cost accounting

The adapter calls the new backend for preparation and fresh products; it
does not call the copied fixed-prime transform. Coordinate patches preserve
the coefficient identity. Signed numerical-difference patches preserve the
polynomial's value at beta, which is the identity needed when parent products
are cached as normalized digits. Both orientations of each edge are valid,
and the target array has room for every shifted correction. Each emitted
product is normalized before it becomes a numeric-mode parent.

The inherited fresh-product weight agrees with the operations emitted by
two transforms, inverse scaling and pointwise multiplication:
3m log2(m)+2m scalar arithmetic operations. Sparse updates agree with their
2ns+merge-length weight. These are valid scalar counters, while the scheduler
does not minimize bit cost: growing ring operations and digit operations
have different costs. Setup, discovery, normalization, copies and scheduling
are additional work, as the documentation states.

The fresh-product bit upper bound O(mt log m+m M(t)+n K^2) is valid with
K=O(log n+log beta). For fixed radix t=Theta(n), so this elementary backend
does not itself give a fast general multiplication algorithm. Its ring
workspace is O(mt) bits, including the transformed common operand.

The tighter sparse-correction width O(D+log(s+1)) and canonical-cache storage
O(QnD), D=ceil(log2 beta), apply to the default normalized numeric mode.
Raw coefficient mode instead needs O(D+log n) coefficient width and
O(Qn(D+log n)) cached-product bits. The README now states this
distinction explicitly. Warm keys prevent accidental mismatches but do not
authenticate maliciously altered cache values; the stated trusted-cache
contract is necessary.

The numeric support count 2V_beta(n,s)−1 and coordinate/numeric union bound
3V_beta(n,s)−2 are correct upper bounds per fixed anchor. For fixed beta and
s=o(n), V_beta(n,s)=exp(o(n)), so covering all inputs with these fixed-anchor
patches still requires exponentially many anchors. This is a restricted
coverage statement, not a general multiplication lower bound.

## Verification scope

The recorded audit passes 280 signed rotations, five direct-transform/inverse
ring cases, the explicitly composite modulus 2^32+1, endpoint product folds,
77 exact integer products, and cold/reuse/warm comparisons through 4096
digits. I independently checked that all three implementation hashes in
`results.json` match the current files. No implementation change or additional
broad rerun was needed for this proof review. The reported timing samples
remain same-backend audit observations, not an optimized multiplication
benchmark.
