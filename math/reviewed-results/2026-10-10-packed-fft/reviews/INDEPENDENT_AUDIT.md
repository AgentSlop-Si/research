# Independent adversarial audit: packed finite-word Fourier candidate

Date: 10 October 2026. Audited the research question before reading or exchanging the construction worker's proof. This report does not rely on that worker's construction. The accepted unpacked comparison was read directly and its SHA-256 was verified as `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`.

## Disposition

No counterexample was found. The power-of-two packed construction survives the central data-movement, catalogue, quantization, address-width and all-input error objections. These gates can be proved independently, as below. The resulting cold bound is

    O(N (t + log(v+1))),  v = log2 N,

with O(N) words and explicit output, eventually for every supplied schedule t=o(v). This is a finite-dyadic, growing-word RAM result with multiplication/division and charged cold preprocessing. It is not an exact arbitrary-complex FFT improvement. No priority, practical crossover, or production implementation conclusion follows.

A stronger uniform bound over 2<=t<=v+1 can also be obtained by the explicitly charged scalar fallback in Section 7. That is an additional completion of the sketch, not a consequence of merely calling some unspecified fallback. The all-integer-length compiler and historical model comparison are outside this audit.

## 1. Packed layout and input/output are legal

Let b be the complex-state width and choose a power of two P satisfying 2bP<=v/8. Take the largest such P when one exists. A packed word is

    W_a = sum_{s=0}^{P-1} code(z_{aP+s}) 2^(bs).

All unused high bits are zero. P divides N. Initialize the N/P words to zero. Normalize each scalar input, quantize it, find its bit-reversed destination r, and OR its code into word floor(r/P), lane r mod P. This is one read-modify-write per input, hence O(N), even though successive writes are not local. The input model is a random-access RAM; it imposes no cache-locality guarantee.

Bit reversal is not free. For v sufficiently large let d=floor(v/16); enumerate the 2^d d-bit reversals. Split a v-bit index into ceil(v/d)<=32 chunks, reverse each chunk and concatenate them, then discard the padding bits. This takes a constant number of shifts/masks/lookups. The same chunk enumeration can store the leading nonzero-bit position and support scalar normalization and quantization. Input integers have O(c v) bits for fixed c, so they require only O(c) chunks. This costs 2^(v/16) poly(v), below the principal table bound. Using the comparison manuscript's v/4 chunks instead would give an additional N^(1/4) poly(v), still o(N).

For a stage of span L<=P, L divides P and every butterfly lies wholly in one packed word. All words receive the same direct sum of length-L stage maps. One P-code lookup per word is sufficient. This table represents one radix-2 stage, not an uncharged transform of arbitrary depth.

For L>P, L>=2P and both L and L/2 are divisible by P. A first-half lane block j0,...,j0+P-1, with j0 divisible by P, pairs with exactly one second-half packed word. No butterfly straddles another word. If A,B are the two words and M=2^(bP)-1, form

    key = A | (B << bP),
    payload = T[base(pattern)+key],
    new_A = payload & M,
    new_B = payload >> bP.

The key and payload each use 2bP<=v/8 bits. The two old words are read before either is replaced. Butterflies at one stage act on disjoint pairs, so in-place replacement is legal. There is no online scalar unpacking between stages.

The nested loops cost O(N/P), including loop overhead: N/L outer iterations are no more than N/(2P), and there are exactly N/(2P) pair iterations. Final unpacking and exact restoration of the original power-of-two scale cost O(N). Iterative DIT fed bit-reversed input produces ordinary frequency order.

## 2. The dangerous catalogue claim is valid

Let Q=2^g and use index floor(Qj/L). Consider only cross-word stages L>P. Write k=log2 P, ell=log2 L and h=floor(Qj0/L).

* If L<=Q, the complete lane vector is h+s(Q/L), 0<=s<P. A family label ell and start h determine it.
* If Q<L<QP, put B=L/Q. B is a power of two less than P, so B divides P and j0. The vector is h+floor(s/B). A family label B and h determine it.
* If L>=QP, B=L/Q is a power of two at least P. P divides B, so a P-aligned lane block cannot cross a B-cell boundary. The vector is constant h, independently of the stage. This conclusion would be false for arbitrary non-dyadic or unaligned packing; the actual hypotheses are essential.

The number of start positions for a nonconstant cross-word stage is L/(2P). Summing those powers of two over L<=Q costs less than Q/P. Summing over Q<L<QP costs less than Q/2. All constant families together use at most Q/2 starts. Harmless boundary conventions, including P=1, leave fewer than 2Q family/start labels. One may also use the simpler O(Qv) directory allowed in the question; it changes only a polynomial factor.

Constant-time IDs do not require searching for the lane vector. Store a stage prefix for each nonconstant stage and use prefix[ell]+j0/P. For all constant stages use a common prefix plus h. Stage constants, j0/P, and h require shifts only. The prefix directory has O(v) entries. Actual equal patterns need not be deduplicated across nonconstant stages.

Small-span tables contribute log2 P families. They have 2^(bP) keys rather than 2^(2bP) keys.

## 3. Certified coefficients and exact table semantics

One concrete conservative choice is

    p=ceil(log2(4096(v+1)/epsilon)), u=2^-p,
    e_min=-v-p, e_max=v+4, tau=2^e_min,
    E=e_max-e_min+1,
    b=2[p+ceil(log2(E+1))+1].

Use the comparison's total floating alphabet: exponent fields 1,...,E represent their corresponding exponents; field 0 and fields larger than E decode to zero regardless of the other bits. Real magnitudes below tau quantize to zero; ordinary mantissa truncation is used below 2^(e_max+1); larger magnitudes clip to the signed largest finite state. Every table entry is defined, including invalid padded keys and unreachable overflowing responses. Never apply the ordinary quantizer error bound to clipped responses.

Take g=p+10. Generate dyadic grid coefficients w_hat[h] with complex error at most u/128 from exp(-2 pi i h/Q). The floor-grid angular error is at most 2pi/Q<u/128, so every actual butterfly phase is approximated within u/64. Generate a dyadic s_hat approximating 1/sqrt(2) within u/128. Apply the exact dyadic map

    (a,b) -> s_hat (a+w_hat[h] b, a-w_hat[h] b)

and then quantize each output coordinate with the total quantizer. Both s_hat and all w_hat entries can use p+O(1) fractional bits, with a larger absolute constant if needed to convert real-component rounding to complex error.

Machin arctangent intervals, sine/cosine Taylor intervals at bounded arguments, and an integer-square-root enclosure provide a fully uniform polynomial(v,p) cost per coefficient, using exact rational work with polynomially many bits. This is charged preparation, not a unit-cost transcendental primitive. Final coefficient values are dyadics. No N-entry coefficient array is generated at each stage.

Every decoded state lies on the lattice 2^(-v-2p) Z in each coordinate and has O(v+p) numerator bits. The two exact coefficient products and butterfly sum still use O(v+p) numerator bits. Computing all P butterflies of one response costs polynomial(v,p) work, because P<=v. Rational interval scratch storage used in coefficient certification is separately polynomially bounded. Online packed execution never performs these scalar arithmetic operations.

## 4. All-input error and first-overflow argument

Let H be the exact normalized 2-by-2 Hadamard matrix. The ideal butterfly is H diag(1,w); the dyadic one is sqrt(2)s_hat H diag(1,w_hat). The preceding coefficient choices imply

    ||B_hat-B||_2 <= u/8,
    ||B_hat||_2 <= 1+u/8.

This holds uniformly for every butterfly phase. Direct sums have the same bound; the number of lanes does not multiply it.

Before clipping, real-component mantissa truncation and underflow give, for a complex N-vector z,

    ||q(z)-z||_2 <= u||z||_2 + sqrt(2N) tau.

Thus a nonclipping stage obeys

    ||q(B_hat z)-Bz||_2 <= 3u||z||_2 + d,
    d=sqrt(2N) tau.

Include initial input quantization as one additional rounded identity stage. There are S=v+1 stages. Normalize x=R a, with R a power of two and the largest real/imaginary component of a in [1/2,1). Consequently 1/2<=||a||_2<=sqrt(2N). All ideal stages are unitary. Before a hypothetical first clip, the cumulative error therefore obeys

    e_{j+1} <= (1+3u)e_j + 3u||a||_2 + d.

Since (1+3u)^S<=2,

    e_S/||a||_2 <= 6uS + 4S sqrt(2N) tau
                    = 6uS + 4Su sqrt(2/N)
                    <= 10uS < epsilon.

The same bound applies to every preceding prefix. Hence, before a first clip, the next prequantization vector has norm less than 2sqrt(2N), whereas the clipping threshold is 2^(e_max+1)=32N. The first clip cannot occur. Initial normalized input also lies below this threshold. This removes the circularity and proves a deterministic guarantee for every represented input, including cancellation-heavy and tiny-norm inputs after normalization. Exact power-of-two scale restoration preserves the relative bound. The zero input is handled separately by explicitly writing zeros.

## 5. Cold preparation and address width

Let R=O(Q+log(P+1)) be the family count. A conservative bound is

    Cprep <= poly(v,p) [ Q 2^(2bP) + log(P+1)2^(bP)
                        + Q + 2^(v/16) + 1 ].

This includes coefficient generation, all padded keys, all outputs, scalar decoding/quantization during preparation, directory construction and the digit helper tables. If a simpler stage-by-grid directory is used, multiply the first term by v.

When t=o(v), p=o(v), b=Theta(t+log(v+1)), and the largest legal P is Theta(v/b). Thus

    Q 2^(2bP) poly(v,p) <= 2^(v/8+p+O(log(v+p)))
                         = N^(1/8+o(1)) = o(N).

The digit table is smaller. All stage indices and pointers fit O(v) bits. A fully materialized address uses at most

    2bP + log2 R + O(1) <= v/8 + p + O(log v)

bits; a response occupies at most v/8 bits. Shifting a family index by 2bP, adding a key, forming array indices and splitting a payload therefore take O(1) word operations in the specified sufficiently wide Theta(v)-bit RAM. No address or intermediate product secretly needs an unbounded integer.

Working arrays and explicit input/output occupy O(N) words. Preparation occupies o(N) words in the saving regime. The per-stage packed work is O(N/P), so total online work is

    O(N + Nv/P) = O(Nb) = O(N(t+log(v+1))).

## 6. What an honest eventual theorem requires

The sketch alone did not specify every small-size branch. A uniform implementation may attempt preparation with an N-step/N-word budget, abandoning and freeing the partial tables if either budget is exhausted. Instrumenting a fixed program with a counter costs a constant factor. This avoids treating an unspecified big-O polynomial as an executable branch test. If P does not exist, use the scalar fallback immediately.

The eventual t=o(v) claim follows because the complete preparation bound in Section 5 is o(N) for every such supplied schedule, and P grows. No useful radix or table bound is claimed on a branch that did not pass its guard. A merely correct slow fallback is enough for this eventual theorem, but not by itself for a uniform time bound on all 2<=t<=v+1.

## 7. Sufficient completion for a uniform 2<=t<=v+1 bound

There is a fully charged O(Nv) scalar fallback in this model. Use the same normalized radix-2 algorithm, scalar states, total quantizer and p=O(v). Generate a complete length-N phase circle using q=p+v+16 fractional bits. Start with a certified dyadic omega_hat within 2^-q of exp(-2pi i/N), set z_0=1, and set

    z_{j+1}=truncate_to_q_bits(z_j omega_hat).

The elementary recurrence gives |z_j-exp(-2pi i j/N)|<=6N2^-q<u/128 for j<=N. Every product and truncation uses O(v+p)=O(v) bits; circle generation costs O(N), plus polynomial(v) certified seed/root work. The stage phase j/L is fetched at index jN/L. Every scalar butterfly and its floating quantization cost O(1) using the charged digit helper tables. Consequently the fallback costs O(Nv)+poly(v), with O(N) space. Fixed polynomial(v) overhead is O(N) asymptotically and can be absorbed uniformly over the finite remaining sizes.

For a fixed sufficiently small constant gamma>0, e.g. gamma=1/1024, the fast preparation succeeds uniformly for all sufficiently large v with t<=gamma v: p<=gamma v+O(log v), b<=2gamma v+O(log v), P exists, and Section 5 is exponentially sublinear uniformly in that range. If t>gamma v, scalar O(Nv) work is O(Nt). Finite exceptions have a finite maximum constant. Thus the guarded fast branch plus this particular fallback proves the uniform O(N(t+log(v+1))) bound for 2<=t<=v+1. It is essential to supply the high-guard circle construction; independently generating N certified roots at polynomial(v) cost apiece would not establish the stated scalar fallback cost.

This fallback remains a mathematical construction. The fresh controls below do not implement or benchmark its production-scale certified root generator.

## 8. Fresh independent controls

Only the new local script `check_packed_controls.py` was executed. It imports standard Python modules and NumPy; no predecessor/uploaded research program was imported, executed, compiled or AST-parsed.

Results saved in `control_results.json`:

* 704 power-of-two parameter combinations and 130,216 actual lane vectors checked the three exact pattern formulas, collision consistency and the fewer-than-2Q catalogue bound. This includes artificial Q<P and P=1 edge cases, not only the intended Q>P regime.
* 119 bit-reversal packed-placement cases checked the chunk construction against direct bit-string reversal.
* Eight complete P=2 complex-state lookup tables, with 4 bits per complex toy state, were eagerly constructed. All 524,288 cross-table entries were checked against a separately written scalar exact-integer butterfly; the 256 within-word entries were also constructed.
* 210 random toy packed FFT executions through lengths 4,...,256 matched the separate scalar executor after every stage, including L=P and L=2P boundaries and constant-phase reuse.
* All 65,536 two-input keys of a separate p=1, two-exponent toy alphabet were tested with exact Fraction arithmetic. There were 112 complex codes with padded invalid exponents and 768 response keys requiring clipping. The total semantics and all nonclipping quantizer inequalities passed.
* 288 numerical stress cases using the actual conservative precision schedule passed the requested relative-l2 target; the largest error/tolerance ratio was approximately 0.00055203. Cases included impulses, constants, alternating signs, Fourier modes and mixed dynamic ranges.

Limitations: tiny eager tables test actual packing and total maps, not target precision. Some combinatorial packing controls use Python big integers and do not by themselves certify word width; Section 5 does that analytically. Numerical stress cases use ordinary floating trigonometry and therefore are not certified coefficient-generation tests. These are falsification controls, not proofs, asymptotic benchmarks, or evidence of practical speedup.

## 9. Gate summary and remaining work

Independently proved at paper level: bit-reversal construction; maintained packed layout; early/late-stage transitions; O(1) phase IDs; O(Q) catalogue; legal key/payload/address widths; total invalid and overflow semantics; charged polynomial coefficient generation; sublinear cold preparation for t=o(v); exact output and scaling; all-input error accumulation and saturation exclusion. Section 7 supplies a sufficient uniform high-precision fallback.

Not established by this audit: a production executor with the large certified tables; an independently rerun all-integer-length interpolation compiler; practical crossover; an external priority/model-matching conclusion. The accepted compiler may be composed only after its own coefficient-grid, interpolation-rank and arithmetic charges are checked; replacing its backend cost symbol is not an independent compiler proof.

The obstruction in the old unpacked executor was genuine for its representation. It is not a lower bound on this different packed representation. Conversely, this positive packed result does not bypass the finite-word/approximation restrictions of the theorem.
