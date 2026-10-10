# Second independent audit and focused novelty assessment

10 October 2026. This is a private mathematical and publication assessment, not journal peer review, a priority certification, or a performance benchmark.

## Executive findings

1. **Accept the adaptive affine-alphabet theorem as a valid derived theorem**, conditional on the stated binary predecessor and its explicitly imported Frobenius-transform machinery. Basis discovery, coordinate retention, constant-offset handling, full output, and the expected-time root contract are all accounted for. No correction to its asymptotic statement is needed.
2. **Accept the arbitrary-length mod-two convolution theorem as a valid derived theorem** in the specified address-capable word-RAM model. The arbitrary-exponent conversion recurrence, inverse pruned butterflies, field padding, and sublinear preparation all survive this second audit. Fixed small lengths should be stated as base cases.
3. **Neither extension is presently a defensible new asymptotic breakthrough.** The affine theorem is a direct linearity/elimination corollary of the binary result. More strongly, the same O(L log log(L+2)) binary multiplication time follows from the 1991 Cantor–Kaltofen theorem by logarithmic blocking into a small truncated-polynomial ring and fully charged tabulation. Section 5 gives that comparison deduction in full.
4. The potentially useful manuscript contribution is an explicit, uniform implementation-and-cost synthesis: the chosen field representation, charged growing tables, packed conversions, and complete cyclic-output contract. Historical originality of that precise synthesis remains unestablished. These extensions fit supporting propositions or an appendix better than a main “faster multiplication” claim.
5. The outputs remain finite-field transforms and carryless convolution. There is no general complex FFT or integer multiplication theorem here.

## 1. Evidence and independence

The following two proof documents were read in full:

- `AUDIT_AND_EXTENSIONS.md` in the supplied extension package.
- `EXACT_RESTRICTED_NTT.md` in the supplied binary-predecessor package.

Their input hashes were recorded before this worker's test execution and rechecked at sealing. The earlier publication assessment was consulted as context only; its conclusions are not evidence for the two new claims. No supplied or uploaded checker/source program was executed, imported, or modified. The only executed research test is the newly authored `independent_checks.py` in this report's directory.

Primary literature was inspected at the exact locations listed in `PRIMARY_SOURCE_RECEIPTS.json`. The 1977 Schönhage source was available only as the publisher's summary; no claim of a full-text inspection is made. The Cantor–Kaltofen author-hosted full paper and the relevant algorithms/theorems in the Frobenius papers were directly inspected.

“Accept” below means that this independent review found a coherent proof under explicit assumptions. It does not replace a formal proof assistant, independently reprove the imported Frobenius theory, or establish worldwide novelty.

## 2. Word model and common preparation

Let the RAM have w=Θ(log(input length+2)) data bits per word, with enough address bits for all working memory. Word Boolean operations, shifts, addition/subtraction, and the stated integer arithmetic/division cost O(1). A bounded number of data words may represent a field element. An address-capable RAM is essential: Θ(log n) by itself, with an unspecified too-small constant, is not an address guarantee. None of the arguments requires unit-cost operations on a packed vector of n bits.

The Artin–Schreier tower is uniform. If the previous tower product has absolute trace one, adjoining a root of u²+u+τ preserves the trace-one induction through the relative trace of τu. Consequently irreducibility is explicit. Slow recursive arithmetic and construction take poly(d), without a field-construction oracle.

For d divisible by eight, partition the represented element into eight positional d/8-bit chunks. There are 64 ordered position pairs and 2^(d/4) input pairs per table. The table cost is therefore 64·2^(d/4)·poly(d), not 2^(2d), and each full field product is a fixed 64-term XOR. Table entries are constructed using the slow arithmetic, before the lookup multiplication is used; this is not circular. The finitely many smaller d are base cases.

For the cyclic transform, d=log₂(N+1), so setup is o(N). For convolution, d<2m and n=2^m, so setup is at most n^(1/2)·poly(m)=o(n). In the latter case, field values need at most a fixed number of words even though the ambient field may have nearly n² elements. No ambient-field-size array, field-wide iteration, or discrete-log table is needed.

## 3. Adaptive affine-alphabet theorem

### 3.1 Basis discovery is valid and actually adaptive

Set β=x₀. Keep residual pivot vectors μ_i, an immutable coordinate index for each vector, and a separately ordered list of pivot positions. For each x_j+β, eliminate in descending pivot order. The running coordinate word records which stored vectors have been removed. If the final residual is nonzero, give it a new coordinate index and append it to the basis; the new coordinate bit is one.

The invariant is

    x_j+β = residual + Σ_i c_i μ_i.

It implies the final representation immediately. Previously stored labels remain correct because no existing basis vector changes. Reordering the pivot list does not relabel its vectors. This also covers the subtle case when a newly discovered pivot belongs between two older pivots. The labels fit in d bits, hence O(1) data words.

There are at most b pivot tests per input and at most d basis insertions. A plain bit scan for a new pivot and list insertion costs at most O(d) per insertion. Thus discovery costs O(N(b+1)+d²) and O(N+d) words. There is no free rank computation, coordinate oracle, or bit transpose in this step. N=1 and b=0 are harmless base cases.

### 3.2 Transform combination and the offset

Each coordinate plane c_i is binary. Apply the accepted binary transform using the same verified primitive root g and the same field tables. Multiply each plane's full output by μ_i and accumulate, at O(N) additional cost per plane. Extracting the plane from stored coordinate words is another O(N). Only one plane needs live transform scratch, so the space does not multiply by b.

For the constant vector β, output k=0 is Nβ=β because N is odd. For 1≤k<N, g^k≠1 and the geometric sum vanishes. Hence the offset adds β only to output zero. This remains correct when the affine set is not a subfield and β lies outside its difference span.

The complete cost is

    o(N) + O(sqrt(N)+poly(d))
       + O(N(b+1)+d²) + O(bN log(d+2)).

It is O(N(b+1)log(d+2)), with O(N) working words. The only expected component is optional primitive-root generation. A supplied root is checked; a generated root defines the returned transform. The theorem does not silently compute a transform at an unspecified external root. Trial division and exact order tests are within the budget.

### 3.3 Scope and significance

The advertised d-symbol coordinate alphabet has dimension log₂d, so O(N(log log N)²) follows. Cardinality alone cannot generally replace affine dimension: five affinely spanning symbols can have dimension four. The little-o condition is precisely b log(d+2)=o(d). The construction does not retain O(N log log N) for arbitrary unbounded b.

This is a sound and useful parameterized consequence. Its principal mechanism is linearity plus streaming Gaussian elimination, so its standalone mathematical novelty is limited without an additional surprising theorem. No exact earlier statement of this full adaptive/root/output contract was found in this focused search; that negative search result is not priority evidence.

## 4. Arbitrary-length binary convolution theorem

### 4.1 Domain and padding

For positive operand lengths a,c, let L=a+c−1. Handle bounded L directly. Otherwise choose n=2^m≥L with n<2L and let d be the least power of two at least m. Then m≤d<2m. The n-element Cantor space W_m is Frobenius-stable because squaring maps each flag space to itself. Its points lie in the represented ambient field, and the pruned transform is valid for arbitrary m≤d; m itself need not be a power of two.

Only W_m and its representative set are used. The product degree is <L≤n, so interpolation on W_m determines the ordinary product polynomial uniquely. Multiplying corresponding representative values is legitimate because they are the evaluations of that same binary product. Therefore these values satisfy the inverse transform's compatibility constraints. The inverse is not being asserted to turn every arbitrary tuple of field values into a binary polynomial.

### 4.2 Packed conversions for arbitrary exponent m

For m>1, choose the largest power of two k<m, let t=m−k, and D=2^k. Thus 1≤t≤k and y=s_k(x)=x^D+x. Recursive division by powers of y produces 2^t contiguous D-coefficient blocks. At a split of 2H coefficients, the divisor is x^H+x^R with R≤H/2.

Writing f=low+x^H high gives q=high+S(high), where S is right shift by H−R coefficients. Because S²=0 on a block of H coefficients, the inverse is high=q+S(q). The remainder is low plus the low-H truncation of x^R q; the same XOR recovers low in the reverse direction. No coefficient multiplication is involved.

For h-bit vector coefficients, implement the shifts in arrays of w-bit words. A shift, truncation, split, or copy of Hh bits costs O(1+Hh/w), including misaligned word boundaries. All coefficient groups are contiguous; interpreting a D-coefficient block as one hD-bit vector causes no transpose.

There are t division levels. Normalizing volume work by nh/w yields

    V(m) ≤ V(k)+V(t)+C t.

The entropy difference m log₂m−k log₂k−t log₂t is at least t for k≥t≥1, proving V(m)=O(m log(m+2)) by induction. The nonvolume overhead satisfies

    J(m) ≤ 2^t J(k)+J(t)+C·2^t.

For j(m)=J(m)/2^m,

    j(m) ≤ j(k)+2^(−k)j(t)+C·2^(−k).

On 2^(r−1)<m≤2^r, k=2^(r−1), and both j(k),j(t) are bounded by the preceding range maximum. Adding C gives the convergent-product bound stated in the submitted extension. This proves J(m)=O(2^m), including m close to a power-of-two boundary. Forward and reverse conversion consequently cost

    O(n + (nh/w)m log(m+2)).

At h=1 and w=Θ(m), this is O(n log(m+2)). It is important to charge packing into binary storage after the inverse transform, since inverse butterflies may be represented by field words. There are n final binary novel coefficients; checking/extracting their bits and packing them costs O(n), within the ledger. Input bits can likewise arrive one per word.

### 4.3 Inverse pruning and tree costs

At a nonpruned butterfly, q₀=p₀+tp₁ and q₁=q₀+p₁ invert as p₁=q₀+q₁, p₀=q₀+tp₁. At a pruned node with state l a positive power of two, parent coefficients are in the subfield with l-bit tower coordinates, and t=c+u lies in its next quadratic extension. Write each recovered child coefficient as R₀+uR₁. Then p₁=R₁ and p₀=R₀+cR₁.

The tower-product representation stores the two halves contiguously. A mask/shift extracts R₀ and R₁, and each parent pair needs one table-based field product and one XOR. Thus there is no hidden l-step Frobenius computation or linear-system solve inside inverse pruning. This operation is the inverse butterfly, not evaluation of the inverse field automorphism.

The inverse traverses precisely the retained forward tree. In a positive-state subtree its normalized level cost is O(n/(t+1)); summation gives O(n log(m+2)). The zero-state spine spawns geometrically shrinking subtrees, preserving the same bound. Twiddle calculation by repeated squaring/XOR has the independently bounded O(n) aggregate cost. Offset construction and traversal are also covered. Pointwise products cost at most O(n).

Conversion scratch can be reused after each sequential recursive call. Forward/inverse transform arrays on an active path have geometrically decreasing sizes, and sibling results can be combined and released. The resulting live storage is O(n) field words, plus o(n) table words. No O(n log n) collection of all recursion levels is required. Binary output materialization costs O(L), even one bit per word.

Combining the charges gives deterministic O(L log log(L+2)) time and O(L) working words. I found no missing asymptotic term. The proof is conditional on the imported Cantor/Frobenius identities and transform correctness, which this review checks against the primary statements rather than re-formalizing.

## 5. Decisive same-model comparison: Cantor–Kaltofen plus small-ring tables

This section is this review's own reduction from established literature. It is not a claim that the 1991 article prints this exact RAM corollary.

Cantor and Kaltofen prove, uniformly over the coefficient algebra A, polynomial multiplication of length s using O(s log s) algebra multiplications and O(s log s log log s) additions/subtractions. Their paper explicitly permits arbitrary algebras and an algebraic RAM interpretation. [Primary theorem, pp. 1–2 and 8](https://kaltofen.math.ncsu.edu/bibliography/91/CaKa91.pdf).

Choose, for sufficiently large L,

    h = floor(log₂(L+2)/16),
    R = F₂[z]/(z^(2h)).

An element of R is a 2h-bit vector, fitting in O(1) words; addition is XOR. Build the complete multiplication table for R. There are 2^(4h)≤(L+2)^(1/4) ordered pairs. Each entry is computed by ordinary carryless schoolbook multiplication and truncation in poly(h) operations. The total preparation is o(L), including all table entries and addresses. Each later ring multiplication is one lookup with a 4h-bit key. This comparison can even use a complete table because the chosen coefficient ring is deliberately much smaller than the ambient field of the submitted theorem.

Split each binary input polynomial into h-bit coefficient blocks:

    A(z)=Σ_i A_i(z)z^(ih),    B(z)=Σ_j B_j(z)z^(jh),
    deg A_i, deg B_j < h.

Form the outer polynomials A*(Y)=Σ_i A_i(z)Y^i and B*(Y)=Σ_j B_j(z)Y^j over R. Their lengths are O(L/h). Apply the quoted algorithm to obtain coefficients C_k in R. Each exact coefficient before reduction is Σ_(i+j=k) A_i(z)B_j(z), of degree at most 2h−2. Consequently reduction modulo z^(2h) loses nothing in any final coefficient. Intermediate wraparound is harmless because the algorithm is a ring identity.

Recover the binary product by XOR-overlapping C_k shifted by kh bits. This costs O(L/h) packed-word work plus O(L) if separate output bits are required. With s=O(L/log L), the main computation costs

    O(s log(s+2) log log(s+4)) = O(L log log(L+2)).

The reduction uses exactly the ordinary finite-word operations and charged growing tabulation allowed in the reviewed theorem. It requires neither roots nor a finite field, and it applies to arbitrary input lengths. Thus the numerical word-time upper bound cannot credibly be sold as a new asymptotic binary multiplication speedup over the consequences of classical algorithms.

For a conservative comparison, this section only needs the matching time bound. It does not infer a published O(L)-space theorem from the arithmetic-operation count alone. A full state-of-the-art bit-complexity or implementation comparison is outside this focused assessment.

## 6. Primary-literature placement

- **van der Hoeven–Larrieu, 2017.** Frobenius symmetry and orbit-representative finite-field Fourier transforms are prior work; cyclic transforms and polynomial multiplication are part of the motivation. The paper uses a bit-complexity framework and should not be cited as directly proving the submitted charged word-table bound. [Author PDF](https://www.texmacs.org/joris/ffft/ffft.pdf).
- **Li–Chen–Kuo–Cheng–Yang, 2018.** The arbitrary m≤d additive domain, forward pruning, inverse pruning, and binary evaluate/multiply/interpolate pipeline are already explicit in §§2.3, 3.3–3.5 and 4. Algorithm 1 also uses the largest suitable power-of-two exponent for basis conversion. What this package adds to that machinery is its particular bounded-word accounting and preparation/output contract, not those algebraic algorithms. [Paper](https://arxiv.org/pdf/1802.03932).
- **Chen–Cheng–Kuo–Li–Yang, 2018.** Practical binary multiplication using Frobenius partitions, packing/encoding and word-oriented implementation was already studied. The paper's dedicated fixed-field practical regime is different from a uniform unbounded RAM theorem; no runtime benchmark follows from the submitted asymptotic proof. [Paper](https://arxiv.org/pdf/1803.11301).
- **Schönhage, 1977.** The publisher's summary already records characteristic-two multiplication using synthetic roots and quasi-linear arithmetic complexity. Since only the summary was inspected, this source is background rather than the evidence for Section 5's exact comparison. [Publisher record](https://link.springer.com/article/10.1007/BF00289470).

These comparisons distinguish historical method overlap, a derived theorem, and a priority claim. “Not found in a focused search” cannot establish originality. There is no basis here to state “first,” “best known,” or “breaks the FFT barrier.”

## 7. Independent checks and remaining limits

The fresh checker uses polynomial-basis arithmetic as an independent field representation and discovers tower generators within it. It compares pruned evaluations with direct Horner evaluation, checks orbit coverage, and runs the inverse through explicit tower-coordinate splits. The packed-conversion path uses actual lists of bounded data words, with copying, masking, nonaligned extraction and shifts counted. Reference routines use Python integers; neither timings nor a Python integer's unit cost are used as complexity evidence. Array indices remain Python indices, so this is a word-boundary test, not a complete RAM emulator.

Passing checks:

- 144 word-array conversion/inverse cases for m=0,…,11, h∈{1,3,9,19}, w∈{7,17,31}; includes vector lanes wider than a data word and arbitrary m
- 680 pruned forward/inverse/orbit cases in extension degrees 1,2,4,8
- 400 arbitrary-length mod-two product cases
- 57 adaptive affine cyclic-transform cases, including constant data and general affine spans
- All 65,536 positional table products in the degree-eight field
- 600 small-ring blocking/recovery checks supporting Section 5's comparison reduction
- 4,095 recurrence controls, covering every m from 2 through 4096

The small-ring comparison tests deliberately use schoolbook outer convolution; they verify the blocking/recovery identity, not the imported Cantor–Kaltofen algorithm. The tested operation counters corroborate boundary handling but do not prove the asymptotic bounds. The mathematical derivations, not finite samples, support those bounds.

The characteristic-two limitation is intrinsic: (1+x)²=1+x² here, while integer convolution includes a middle coefficient 2. This validates neither ordinary integer convolution nor an approximation to it. Bit complexity, numerical stability, practical speed, and historical priority remain separate questions.

## 8. Recommended publication language

Safe: “We give an explicit fully charged word-RAM implementation of established Frobenius additive transforms, derive an affine-dimension-adaptive cyclic-transform corollary, and record its arbitrary-length binary polynomial multiplication consequence.”

Necessary qualification: “The multiplication time bound also follows from classical polynomial multiplication over arbitrary algebras with blocking and tabulation; no asymptotic multiplication priority is claimed.”

Recommended placement: retain both accepted extensions as supporting results. Put the exact model, preparation, basis conversion and explicit-output contract in the main technical statement if that implementation synthesis is the intended contribution. Before submission, complete a broader focused search for this exact RAM synthesis and decide whether it contributes enough beyond a careful exposition of known machinery.
