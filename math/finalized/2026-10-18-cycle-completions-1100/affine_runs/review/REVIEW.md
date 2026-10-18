# Independent final review: certified affine canonical runs

18 October 2026 UTC.

## Verdict

**PASS.** The new affine-run recognizer, source-preserving second-difference graph,
signed shared-product evaluation, and four-prefix recovery are correct. Together
with the explicitly inherited native-plan and carrying facts, they establish

    O(N + r^12 + (R_A+R_B)r^4 + Qr^4 + Mr^2)
    = O(N + r^12 + R_A R_B r^4),

where r=floor(log2 N), the complete legal input block lists have the deterministic
greedy run counts R_A,R_B, the actual nonzero second-difference term counts satisfy
K_A<=4R_A and K_B<=4R_B, M=K_A K_B, and Q<=M counts distinct normalized commutative
leaf-product types. The fixed positive budget R_A R_B r^4<=C N gives a complete
O(N) successful new branch and O(N+r^12) overhead on rejection. Its union with
the accepted jump route preserves that route's recognized inputs and inherited
arbitrary-input upper bound.

The low-digit ramp family is a strict extension of the stated fixed-budget
first-jump recognized class. This is not a lower bound for the prior dispatcher's
runtime or an arbitrary-dense multiplication improvement. The existing fallback
bookkeeping erratum remains mandatory. No new production change or erratum is
required.

## Artifacts, provenance, and execution boundary

Reviewed candidate directory: `../jump_extension_20261018_1043/`.

- `REPORT.md`: SHA-256 `4c9d19c763a5d5b60ece1189c6bc8cc8ecddc082987922a36bc7f3aeede05928`.
- `affine_shared.py`: SHA-256 `47101aabdb3789846e3822226c0ff1089b150ff5af0419b61fb036a169a154df`.
- Inherited portable `run_shared.py`: SHA-256 `3d3b6e7f0f96013cc90349d76b30aec4afd72b9f0e2b6faed861bc7d74b2480b`.
- Inherited primitive source: SHA-256 `a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06`.
- Required inherited erratum: SHA-256 `45f2f4506e5d81fa1c02d81ac8db779d88ee4292ad87aa1d680460b0ecbe368f`.

All 17 candidate manifest entries were independently checked. The inherited
report, review, clarifications, erratum, portable jump source, and relevant
primitive implementation were read. Their prior accepted theorem is an explicit
dependency, not a newly executed result.

The new `independent_controls.py` was authored after inspection. It executes only
the 12 function/class definitions extracted from the hash-bound new
`affine_shared.py`. Top-level imports and assignments are not executed. A fresh
adapter supplies independently implemented exact arithmetic, canonical conversion,
native-plan formulas, polynomial evaluation, Lagrange interpolation, and output
assembly. The plan uses direct CRT reconstruction, checks every candidate node
norm for the minimax translation, and uses direct Lagrange interpolation rather
than the inherited finite-difference implementation.

**No historical module, historical control program, or candidate author control
program was imported or executed.** The controls do not claim a fresh run of the
historical fallback or production elementary backend. Fallback dispatch was
observed only with a fresh oracle sentinel. Full-backend acceptance rests on the
read source and its already accepted dependency, while fresh execution separately
checks the new control flow and mathematical transformation. Host integer products
occur solely in these independent review oracles. All work remained local; no
repository or other external write was performed.

## 1. Canonicality and the endpoint certificate

For increasing positive integer weights W_0=1<W_1<...<W_(r-1), a nonnegative
integer digit vector c is the greedy expansion of its own decoded integer exactly
when every strict lower prefix satisfies

    sum_(j<h) c_j W_j < W_h,  1<=h<r.

Necessity follows from the greedy remainders. For sufficiency, after higher digits
have been removed, division by W_h sees c_h W_h plus a nonnegative remainder
strictly below W_h, and hence recovers c_h. The top digit is unrestricted unless
the legal-block capacity is also imposed. With that additional linear constraint,
the legal canonical vectors are integer points of a convex bounded region.

For integral u,v with canonical legal endpoints u and z=u+(ell-1)v, each
intermediate u+t v is integral and lies on the endpoint segment. Nonnegativity,
capacity, and all prefix inequalities hold throughout: integer endpoint prefixes
are at most W_h-1, so their convex combinations also satisfy the required strict
inequality. Thus all intermediate vectors are canonical.

For an actual numerical affine run a_t=a_0+t d, the production certificate takes
u=c(a_0), v=c(a_1)-u, and checks c(a_(ell-1))=u+(ell-1)v. Linear decoding gives
decode(v)=d. The preceding convexity argument and uniqueness then give
c(a_t)=u+t v at every actual input position. This does not assume canonical
encoding is additive. A singleton uses slope zero; a two-element run is correctly
certified without additional interior conditions.

`affine_partition` is a complete, explicit greedy disjoint scan, not an oracle for
an optimal segmentation. It selects the first two uncovered blocks when available
and extends only while the adjacent numerical difference stays fixed. Every input
block is inspected O(1) times. The producer checks every run certificate. The
checker separately scans every scalar block in every declared interval and checks
first, second, and last canonical expansions. The checker need not insist that a
valid partition is the producer's greedy one for mathematical soundness; the
producer itself determines the theorem's stated R_A,R_B.

## 2. Complete source preservation and boundary events

For a zero-extended run with canonical coefficients u+t v on positions
l,...,l+ell-1, multiplying by (1-Y)^2 gives the four possible vector events

    l: u
    l+1: v-u
    l+ell: -(last+v)
    l+ell+1: last.

The producer merges coincident positions exactly, including singleton and
two-element overlaps and adjacent-run boundaries. The checker independently
reconstructs each local boundary from c_i-2c_(i-1)+c_(i-2). The two forms agree.
Summing the zero-extended intervals gives the complete original input stream;
therefore the merged list is its exact second difference, including internal
zeros, start effects, and terminal effects. At most four records per run survive,
which proves K_A<=4R_A and K_B<=4R_B.

Original canonical coordinates lie in [0,P), so the actual merged differences
have coordinate magnitude below 2P. These bounds apply to the merged source
difference, not to a numerical difference recoded canonically. The Newton degree
stays at most r-1, and the inherited ordinary-node bounds remain O(r) bits.

Linearity of the original Newton polynomial gives the identities

    D_A(x,Y)=(1-Y)^2 F_A(x,Y),
    D_B(x,Y)=(1-Y)^2 F_B(x,Y)

for every x,Y. Consequently the original source rows, row-specific packing bases,
and literal original input values are preserved. This is stronger than checking
only the target x=-P. No packed source product is used by production.

Sign normalization uses the first nonzero vector coordinate, and a normalized
leaf can decode to a negative integer. The code retains signed leaf evaluations,
products, targets, and event contributions. Fresh checks include 1,163 occurrences
of such negative decoded normalized leaves. Deterministic exact sorting interns
leaves and commutative product pairs; every actual term pair creates its own signed
outer event. Each product polynomial has degree at most 2r-2 and is evaluated at
the original 2r-1 nodes and interpolated once. The independent checker verifies
the resulting targets using only decoded O(r^2)-bit leaf operands.

## 3. Source maxima, strict widths, and four-prefix recovery

For each original node x, f_(u+t v)(x) is affine in t. Its absolute value is convex,
so its largest value over each finite run occurs at a run endpoint. Evaluating
canonical first and last vectors therefore gives the exact original dense-row
maxima, including negative values, sign crossings, internal zeros, and partial
high blocks. The checker invokes the endpoint-maxima calculation only after
independently establishing canonical endpoint legality and the full scalar
binding.

With L=max(L_A,L_B), the code retains the precise source rule

    w_x=8 ceil(bit_length(2 L A_x B_x)/8)

when A_x B_x is nonzero, and zero otherwise. The bit-length rule makes
2^(w_x)>2 L A_x B_x even at exact power-of-two boundaries. No common weakened
width replaces these actual source-specific widths. Since source preservation is
a polynomial identity in Y, each individual base can be substituted separately.

At x=-P the accumulated product events satisfy

    E(Y)=(1-Y)^4 F_A(-P,Y)F_B(-P,Y).

Four inclusive prefix scans starting at zero therefore recover the ordinary
nonnegative block convolution. Its final possible index is L_A+L_B-2. The code
continues through four more positions, checks all four recovered tail
coefficients are zero, verifies every prefix state is zero at the end, and checks
that every event was consumed. These are the correct finite-support termination
conditions. A fresh missing-terminal-event mutation is also rejected by recovery
itself, separately from the graph checker.

Every decoded second-difference term has magnitude below 2*2^s. Each individual
signed product event is therefore below 4*2^(2s). For T=L_A+L_B+3 positions, a safe
j-prefix state bound is

    4 M 2^(2s) binom(T+j-1,j-1),  1<=j<=4.

The bound follows by summing M event magnitudes against the nonnegative repeated
prefix kernel. It controls cancellation intermediates, not just the final answer.
Since s=Theta(r^2), T=O(N), and M=O(N^2), every state uses O(r^2) bits. The event
accumulator obeys the same bit-width order. The ordinary final coefficients also
have their usual sharper min(L_A,L_B)2^(2s) bound. The inherited bounded-window
nonnegative carry/serialization procedure and sign restoration then yield the
complete exact signed-binary product.

## 4. Full bit-cost audit

The model is the accepted elementary sequential-bit/array model, not Python
wall-clock time, an interpreter instruction count, or the fresh oracle adapter's
cost. The inherited native facts are s=Theta(r^2), log P=Theta(r), O(r)-bit ordinary
node entries, and O(r^2)-bit target interpolation weights.

1. **Plan and dense recognition.** A fresh elementary ledger precedes plan
   construction, so the inherited O(r^12) setup remains valid. Bounded-byte input
   splitting costs O(N). Numeric differences and comparisons use O(s) bits per
   block, for another O(N). Run metadata is O(r) bits per record.

2. **Canonical certification.** Each conversion has r divisions with O(r^2)-bit
   operands and O(r)-bit quotients. Explicit binary long division therefore costs
   O(r^3) per digit and O(r^4) per converted endpoint. At most three endpoints per
   run are needed, with constant-factor repetitions in verification. Endpoint
   extrapolation uses O(r)-bit run lengths and slopes in r coordinates, costing
   O(r^3) per run. Actual extrapolated values and cancellation intermediates remain
   within O(r) bits per coordinate because run lengths are at most polynomial in
   N. The stated O((R_A+R_B)r^4) pays successful and rejected conversions.

3. **Boundary records and interning.** There are O(R_A+R_B) initial records, each
   with an O(r^2)-bit vector and O(r)-bit position. Comparison sorting, movement,
   merging, and sign normalization cost O((R_A+R_B)r^3), below the endpoint term.
   The checker uses a constant number of local vector values per boundary and
   has the same bound. There is no dense canonical expansion hidden here.

4. **Source and leaf evaluation.** Each vector at O(r) original nodes requires
   O(r^2) products of O(r)-bit operands, hence O(r^4). Endpoint source maxima,
   leaf evaluations, their repeated checks, and strict widths are covered by
   O((R_A+R_B)r^4).

5. **Products, interpolation, and verification.** Each distinct product has
   O(r)-bit node values. The finite-difference interpolation table remains
   O(r) bits per entry, while target weights have O(r^2) bits. The elementary
   products and additions cost O(r^4) per shared product. Independently decoding
   leaves costs O(r^4) each, and the checker multiplies O(r^2)-bit targets in
   O(r^4) per product. Thus all of this work costs O((R_A+R_B+Q)r^4).

6. **Pair/event records and accumulation.** There are M actual term pairs. Their
   product IDs, positions, and signs occupy O(r) bits. Exact comparison sorting
   takes O(M log(M+1) r)=O(Mr^2), including record movement. Signed target-event
   accumulation also costs O(Mr^2). The graph uses sorted append/intern passes,
   not repeated linear search through product records.

7. **All dense scans and output.** Dense certificate binding and four full prefix
   scans visit O(L_A+L_B) positions with O(r^2)-bit values. Since nontrivial input
   has O(N/s) blocks and s=Theta(r^2), their cost is O(N). Carrying and output
   serialization have the same cost. Elementary O(r)-bit block-offset
   multiplication costs O(r^2) per position and fits this budget. Reading,
   signs, dense integer conversion, unequal lengths, zeros, and partial final
   blocks are not discarded.

8. **Root-wide administrative state.** All totals, counters, record addresses,
   and indices are polynomial in N and thus use O(r) bits. After excluding
   already charged sorting and arithmetic-loop work, there are at most
   O((R_A+R_B+Q)r^2+M+L_A+L_B) administrative events. Paying O(r) each gives
   O((R_A+R_B+Q)r^3+Mr+(L_A+L_B)r), absorbed above. Byte copying is charged by
   copied length; a root-width counter update is not performed for every bit.

Combining these charges gives the refined bound. For nonempty inputs,
R_A+R_B<=2R_A R_B, M<=16R_A R_B, and Q<=M, proving the uniform bound.

The budget is evaluated after only plan construction and the dense numeric scan,
before canonical endpoint conversion or graph allocation. If it fails, the new
overhead is O(N+r^12). If it passes but a certificate fails, the endpoint work is
also O(N), because (R_A+R_B)r^4<=2R_A R_B r^4<=2C N. The code may certify the other
side after one rejection, but this only changes the constant. If it succeeds,
all graph and recovery work obeys the same fixed linear budget. Since r^12=o(N),
the complete accepted branch is O(N) for every fixed C>0. Constants need not be
uniform in a growing budget parameter.

The new wrapper calls the unchanged accepted jump dispatcher on rejection, so
the previous recognized inputs remain available. The accepted arbitrary-input
N exp(O(log N/log log N)) upper bound absorbs the new overhead, with its existing
root-wide erratum still in force.

## 5. Strict recognized-class extension and limits

For native rank r set L=ceil(2^r/s)+1 and choose a_i=i+1. The plan gives P>=H+1
for H=lcm(1,...,r). For each prime p, Legendre's formula writes the valuation of
binom(r,j) as a sum of at most floor(log_p r) terms, each 0 or 1. Therefore every
binom(r,j) divides H, and

    H>=binom(r,floor(r/2))>=2^r/(r+1).

Since s=Theta(r^2), L<P eventually. All ramp blocks have canonical vectors
(i+1,0,...,0), so they form one certified affine run. Their actual input bit length
is N=(L-1)s+bit_length(L), which lies in [2^r,2^(r+1)) eventually. Thus the rank
used by the real input is exactly the chosen native rank, not an externally
prescribed inconsistent parameter. A reversed ramp has the same conclusion.

The forward ramp has second difference

    1-(L+1)Y^L+L Y^(L+1),

and the reversed ramp has L-(L+1)Y+Y^(L+1). Each has exactly three nonzero terms.
The new pair has R_A=R_B=1 and M=9. Every first jump is nonzero, including both
boundaries, so the old counts are K_A^(1)=K_B^(1)=L+1. The old fixed-budget
quantity is Theta(L^2r^4)=Theta(N^2), while the new quantity is r^4=o(N). Hence
every fixed positive new budget eventually accepts this family and every fixed
old first-jump budget eventually rejects it. This is a genuine strict separation
of those recognition predicates, while the wrapper's union loses none of the old
accepted branches.

The report correctly withholds broader conclusions. A numeric affine sequence
alone can cross canonical carries, yielding dense canonical second differences.
The odd-P stride-(P+1)/2 examples are valid; fresh 90-block examples at ranks
6, 10, and 16 each have 92 nonzero low-coordinate second differences. The
first-three-plus-last quadratic obstruction is also valid: for sufficiently large
P and q=ceil(P/24), the samples at t=0,1,2,10 of q t(10-t) lie below P, while
the predicted low digit at t=5 is 25q>P. This defeats that sampling certificate.

Higher-order difference identities alone do not supply a cheap canonical
recognizer or exact original-row extrema. No higher-order or order-uniform
complexity theorem follows here, and no historical-priority claim is made.

## 6. Fresh control results

The final run in `RESULTS.json` and `controls.log` passed:

- 17 candidate manifest entries and 29 independently reconstructed native formula
  plans, ranks 2 through 30.
- 1,944 generic greedy-canonical inequality checks, including non-divisibility
  weight systems.
- 4,992 complete endpoint-certification cases, of which 1,729 passed, compared
  against all directly expanded interior vectors.
- 226 exact new graph products, 2,662 original-source-node identity/maxima/strict
  width checks, and 5,550 independent convolution comparisons.
- 23 corrupt-certificate or dense-input mutation rejections, plus one independent
  recovery-tail rejection.
- 13 exact signed products through the inspected new front-end bodies using the
  fresh adapter, including zero/base cases and wide affine carry cases.
- Six explicit strict-family fixed-budget separations at ranks 10,12,14,16,18,20.
  The largest has 1,049,375 input bits, 1,133 complete occupied blocks, native block
  width 927, nine pair events, and six shared products.
- Budget rejection before any canonical certification, and failed endpoint
  certification before any graph allocation.
- Three numeric-affine dense-carry obstructions and the quadratic sampling
  obstruction.

The prior intermediate status message reported the first successful suite before
three explicit signed-normalization graphs were added; the final counts above
supersede those intermediate counts. Both runs passed. No candidate source was
modified. Finite tests corroborate the proof and new implementation correspondence;
they do not measure an asymptotic speedup and do not relabel inherited runs as
fresh execution.
