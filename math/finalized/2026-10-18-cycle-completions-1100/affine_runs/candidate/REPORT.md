# Canonical affine runs and fourth-prefix shared multiplication

18 October 2026 UTC. New candidate result, not independently reviewed. All work in this packet is local. This extends the accepted canonical first-jump branch; it does not reprove its native plan or fallback and makes no historical-priority or arbitrary-dense speedup claim.

## 1. Result and what is new

Keep exactly the accepted native matrix plan: input magnitude bit length N, rank r=floor(log2 N), binary block width s=Theta(r^2), canonical Newton weights W_h=binom(P+h-1,h), degree at most r-1, and the same 2r-1 ordinary nodes. Let each complete legal block list be partitioned by the deterministic greedy numeric-affine scan below, with R_A and R_B runs.

A run of length ell is accepted only if the canonical vectors of its first, second, and last blocks obey

    c_last = c_first + (ell-1)(c_second-c_first).

For a singleton, use slope zero. No condition is imposed on an input without checking it. A convexity lemma proves that this constant-size endpoint certificate establishes the complete canonical vector identity at every interior block. Thus recognition costs O(N) for the dense numerical scan plus O((R_A+R_B)r^4) for the endpoint certificates, rather than requiring O(r^4) canonical work at every block.

On the accepted branch, let K_A and K_B be the actual numbers of nonzero coefficients in the zero-extended second differences of the canonical vector streams, M=K_A K_B, and Q the number of distinct commutative sign-normalized leaf-product types. Then K_A<=4R_A and K_B<=4R_B, and a complete exact signed-binary multiplier has bit cost

    O(N + r^12 + (R_A+R_B)r^4 + Qr^4 + Mr^2)
    = O(N + r^12 + R_A R_B r^4).

All dense recognition, canonical certification, graph construction and checking, source maxima and strict packing widths, signed arithmetic, four complete prefix scans, carrying, dense output, and root-wide bookkeeping are charged. A fixed-budget front end tests R_A R_B r^4<=C N before any canonical endpoint conversion or graph allocation. It then attempts the certificates; either rejection adds only O(N+r^12), and invokes the unchanged accepted jump/fallback route. Thus every accepted new branch is O(N) for fixed C>0, and the old arbitrary-input N exp(O(log N/log log N)) upper bound survives with its inherited root-wide erratum.

The genuinely new ingredient is a complete, inexpensive source-preserving recognizer for affine canonical streams. Taking a higher difference alone would not address recognition: numerically affine block values can have dense canonical second differences. The endpoint convexity certificate closes that gap for this stated class.

## 2. Canonicality is an integer-point convex condition

For any increasing positive integer weights W_0=1<W_1<...<W_(r-1), a vector c is the greedy canonical expansion of the integer a=sum_h c_h W_h if and only if

1. all c_h are nonnegative integers;
2. for every 1<=h<r, sum_(j<h) c_j W_j < W_h.

The necessity follows from the successive greedy remainders. For sufficiency, the remainder below each weight is nonnegative and strictly smaller than that weight, so top-down division recovers exactly the declared digits. If desired, include 0<=sum_h c_h W_h<2^s as two additional linear inequalities restricting legal blocks. These conditions describe the integer points in an intersection of half-spaces.

Let u and z be canonical legal vectors, ell>=2, and v an integer vector such that z=u+(ell-1)v. For every integer 0<=t<ell,

    u+t v = (1-t/(ell-1))u + (t/(ell-1))z.

All coordinate nonnegativity, legal-capacity, and prefix inequalities therefore hold for this vector. Strict prefix inequalities survive because both endpoints are at most W_h-1. The intermediate vector is integral, hence canonical.

Now suppose the actual numeric input blocks in the run are a_t=a_0+t d. Encode a_0,a_1,a_(ell-1), set u=c(a_0), v=c(a_1)-u, and test z=u+(ell-1)v. Linear decoding gives sum_h v_h W_h=d. The convexity argument makes u+t v canonical, and its decoded number is a_t. Uniqueness proves c(a_t)=u+t v for every position. This resolves canonical nonlinearity without pretending that c is additive.

The numeric recognizer is explicit: at the first uncovered position, take two positions if available, fix their numerical slope, and extend while the next adjacent difference equals it. Start a new disjoint run at the first failure; a final uncovered singleton is its own run. Every block is read O(1) times. The partition need not be an optimal segmentation. The theorem applies to this fully specified recognizer, not to an oracle providing a favorable partition.

## 3. Second differences preserve the complete original source matrices

For one run occupying positions l through l+ell-1, let its canonical vectors be u+t v and extend this run by zero. Its second difference, equivalently multiplication of its generating polynomial by (1-Y)^2, has only these four possible events:

    l:         u
    l+1:       v-u
    l+ell:     -u-ell v = -(c_last+v)
    l+ell+1:   u+(ell-1)v = c_last.

Overlaps for ell=1 or ell=2 are merged exactly. Events from neighboring runs are merged by exact sorted position, then zeros are removed. The resulting vectors are precisely

    d_i = c(a_i)-2c(a_(i-1))+c(a_(i-2))

with the complete original block stream extended by zero. All start, internal-zero, and terminal effects are included. Each coordinate has absolute value less than 2P, since original canonical digits lie in [0,P). The degree in x remains at most r-1. At the native ordinary nodes each leaf still has O(r)-bit value.

Writing F_A(x,Y)=sum_i f_(c(a_i))(x)Y^i for the original source polynomial, the constructed stream satisfies the polynomial identity

    D_A(x,Y)=(1-Y)^2 F_A(x,Y),

and likewise for B. This holds at all x and Y, not just at x=-P. Therefore original rows, their node-specific packing bases, and their literal input values are preserved. The algorithm does not materialize or multiply the packed source integers.

Normalize each nonzero event vector by the sign of its first nonzero coordinate and intern via deterministic exact sorting. A normalized leaf can decode to a negative number even when its first coordinate is positive; all subsequent arithmetic stays signed. Sort the M term pairs to intern commutative product types and to order the signed outer events. Evaluate and interpolate each distinct product only once at the original 2r-1 nodes. Every target event is the exact product of the two decoded second-difference leaves, with its external sign restored.

## 4. Source-row widths require only run endpoints

For fixed source node x, the original row value f_(u+t v)(x) is affine in t. Its largest absolute value over the run occurs at an endpoint, because absolute value is convex. Hence evaluating each run's two canonical endpoint vectors suffices to obtain the exact actual A_x and B_x over the complete dense input rows. Zero runs, negative row values, and internal changes are included.

Retain the original strict source rule

    w_x = 8 ceil(bit_length(2 L A_x B_x)/8), L=max(L_A,L_B),

and w_x=0 when A_x B_x=0. No weakened bound or global common packing base is substituted. The identity in Y permits substituting each 2^(w_x) separately. The program computes the same maxima and widths, and its checker reevaluates endpoint maxima after independently checking the endpoint canonical expansions and the entire dense numeric run binding.

## 5. Four prefix scans and dense output

The accumulated event stream E(Y)=D_A(-P,Y)D_B(-P,Y) obeys

    E(Y)=(1-Y)^4 F_A(-P,Y)F_B(-P,Y).

Four inclusive prefix scans, all starting at zero, therefore return the ordinary nonnegative block-convolution coefficients. If their largest actual index is L_A+L_B-2, process through that index plus four. Require the last four recovered convolution coefficients to be zero and every prefix state to be zero at the final event index. These are exact tail checks; no terminal differences are omitted.

Each decoded second-difference term has magnitude less than 2*2^s, so an event product has magnitude less than 4*2^(2s). Let T=L_A+L_B+3=O(N). A conservative bound for the state after j prefixes, 1<=j<=4, is

    4 M 2^(2s) binom(T+j-1,j-1).

It has O(s+log M+log T)=O(r^2) bits. This bound pays cancellation intermediates and does not assume small final answers while integrating. Actual final convolution coefficients have the usual sharper bound min(L_A,L_B)2^(2s). Four scans over O(L_A+L_B) positions cost O(N). The inherited bounded-byte-window nonnegative carrying and serialization, followed by restoration of the sign, yields the full exact integer product in O(N) additional work.

## 6. Complete cost audit

The following costs are in the same elementary sequential-bit/array model as the accepted branch, not Python timing or an end-to-end interpreter instruction count.

- Plan: the unchanged accepted O(r^12) setup, using a fresh ledger before any root-size scan.
- Dense input: bounded-byte-window splitting plus numeric adjacent differences, comparisons and run recording, O(N). This includes zeros, unequal lengths and a partial high block.
- Canonical endpoints: at most three O(r^4) canonical conversions per run. As in the accepted result, each greedy division has O(r^2)-bit operands with O(r)-bit quotient, so its explicit long division is O(r^3), repeated O(r) times. Endpoint extrapolation multiplies an O(r)-bit run length by O(r)-bit coordinate slopes O(r) times, O(r^3) per run, below the conversion bound. Rejected certificates are charged.
- Event vectors: at most four per run. Boundary construction and merging cost O((R_A+R_B)r^3), including O(r^2)-bit vector movement and O(log N)-bit positional sorting.
- Leaf and source evaluation: O((R_A+R_B)r^4). O(r)-bit leaf entries differ from the accepted width only by a constant factor, so no wider matrix arithmetic is hidden.
- Product interpolation: O(Qr^4). Each product has degree at most 2r-2, O(r)-bit node values, O(r^2)-bit interpolation weights, and one interpolation across all outer events.
- Pair/event construction: O(Mr^2), including exact comparison sorting and record movement of O(r)-bit metadata, and all event-value accumulation of O(r^2)-bit signed integers.
- Certificate checker: repeats the dense scalar binding in O(N), checks first/second/last canonical vectors in O((R_A+R_B)r^4), independently forms boundary second differences from local source values in O((R_A+R_B)r^3), checks every pair/event, and checks target products by direct O(r^2)-bit leaf multiplication in O(Qr^4). No complete input or packed child product serves as a production oracle. The source-row checks are endpoint-based only after the convexity premise has been checked.
- Recovery and dense output: four O(N) prefix scans, O(N) carrying, O(N) dense serialization. O(r)-bit block-offset multiplications cost O(r^2) per output position and fit O(N).
- Root-wide bookkeeping: all costs, records, counters and indices are polynomial in N, hence have O(r)-bit metadata. Excluding already-paid sort movement and low-level arithmetic loops, O((R_A+R_B+Q)r^2+M+L_A+L_B) administrative events cost at most O((R_A+R_B+Q)r^3+Mr+(L_A+L_B)r), absorbed above. Byte copies are charged by copied length; no root-width ledger update is performed once per copied bit. Product records are appended, not linearly searched.

Combining gives the refined theorem. Since K_A<=4R_A, K_B<=4R_B, Q<=M, and R_A+R_B<=2R_A R_B for nonempty inputs, the uniform bound follows. For fixed C, the pre-conversion test and r^12=o(N) give complete linear cost including unsuccessful certificate attempts. Subsequent use of the accepted jump route makes the overall recognized class a union, so no previously accepted class is lost. The inherited fallback erratum remains mandatory.

## 7. A strict new recognized family

For each sufficiently large r, use its native plan and set

    L = ceil(2^r/s)+1,
    a_i=i+1 for 0<=i<L.

One may use the same list for B, or the reversed ramp b_i=L-i. Both have one numeric-affine run and affine canonical vector (a_i,0,...,0), provided L<P. This condition follows within the accepted plan, without assuming an unproved growth constant: P>=H+1 for H=lcm(1,...,r). Every binomial coefficient binom(r,j) divides H, because each p-adic valuation is a sum of at most floor(log_p r) terms, each 0 or 1. Hence H>=binom(r,floor(r/2))>=2^r/(r+1). Since s=Theta(r^2), L<P for sufficiently large r. Also L<2^s.

The integer A=sum_i (i+1)2^(si) has bit length

    N=(L-1)s+bit_length(L),

which lies in [2^r,2^(r+1)) for sufficiently large r, so the rank chosen from the actual input is indeed r. The forward ramp's second difference has exactly three nonzero terms:

    1 -(L+1)Y^L +L Y^(L+1).

The reverse ramp also has three. Thus the new branch has R_A=R_B=1 and M=9, while every position is occupied and the first-jump counts are K_A^(1)=K_B^(1)=L+1. The old fixed-budget first-jump quantity is Theta(L^2 r^4)=Theta(N^2), which eventually exceeds C N for every fixed C. The new fixed-budget test r^4<=C N passes eventually. This proves a strict extension of the stated recognized input class, not a lower-bound separation from the old dispatcher's runtime and not a claim that arithmetic-progressions have no other easy multiplier.

## 8. What higher-order or scalar-polynomial generalizations do not get for free

Numeric affine runs alone do not certify affine canonical vectors. The three consecutive block values P-1,P,P+1 have canonical vectors (P-1,0,...), (0,1,0,...), (1,1,0,...), which fail affine extrapolation. More strongly, with odd P and numeric stride D=(P+1)/2, the legal blocks a_i=(i+1)D form one numeric-affine run but their lowest canonical digit is a_i mod P, an alternating sawtooth. For lengths below the block-capacity limit and away from its eventual period boundary, its second difference is nonzero at essentially every index. The theorem therefore deliberately rejects such an uncertified run instead of claiming that scalar polynomial structure passes through canonical encoding.

For fixed order d>2, the algebraic identity remains valid: source-preserving d-th vector differences give (1-Y)^(2d) times the product, and 2d prefix scans have O(r^2)-bit state for fixed d. This observation alone is not a complete extension theorem. A full result must specify a cheap recognizer for canonical-vector polynomial pieces and pay exact extrema for original row maxima; endpoint convexity is special to affine pieces. Polynomial interpolation through canonical endpoints can leave the canonicality polytope at interior positions. For an explicit quadratic failure, take q=ceil(P/24) for sufficiently large native P and a_t=q t(10-t), 0<=t<=10. At t=0,1,2,10 the canonical vectors are (a_t,0,...,0), all agreeing with the predicted quadratic. At t=5 the predicted first digit 25q exceeds P, so a canonical carry invalidates that vector. All scalar blocks remain legal and nonnegative. Thus even first-three-plus-last sampling does not certify a quadratic canonical run. Encoding every block would cost O(N r^2), beyond the linear branch target. A higher-order result could use certified interval polynomial inequalities or another succinct legality proof, but this packet does not claim that obligation solved or assume that such a certificate is free. Growing difference order also widens coefficients and multiplies scan work, so no order-uniform O(N) theorem is asserted.

## 9. Executable artifact and verification scope

`affine_shared.py` is new production code and imports the unchanged portable accepted `run_shared.py`, checks that portable file hash, and retains the exact primitive dependency hash. `multiply` tries the budgeted affine branch and then the accepted jump dispatcher. `multiply_affine(..., budget_factor=None)` is an explicitly unbudgeted experimental entry point whose cost is parameterized, not automatically linear. Every arithmetic-data multiplication in new production is routed through the accepted explicit shift-and-add backend; native products concern dimensions, budget metadata, or signs.

`controls.py` is newly authored for this candidate. It independently computes canonical digits from exact binomial weights, original node polynomials, dense second differences and direct convolutions; native large products occur only as test oracles. It checks dense source identities and full signed outputs, certificate mutations, the early budget guard, and nonlinear-encoding obstructions. `RESULTS.json` and `controls.log` report the actual run, not a future or independent-review promise. The recorded final run passed 23 native formula checks, 1,265 endpoint-certification cases, 74 exact graph products, 780 original-source-node identities, 1,634 convolution comparisons, 17 complete signed products or full-front-end cases, 22 corrupt-certificate rejections, three dense-carry obstructions, and the explicit quadratic sampling obstruction. It also verified that both budget rejection and failed endpoint certification stop before graph construction. The largest low-digit ramp has 1,049,375 bits and is accepted with nine events and six shared products while the old first-jump budget rejects it. A separate 1,050,291-bit wide-affine carry case exercises 1,865-bit prefix intermediates and a largest elementary-multiplication operand of 1,774 bits. These are author controls, not independent acceptance. The inherited plan/fallback and historical reviewed test counts are not relabeled as fresh executions here.

## Provenance

Accepted source: private repository `AgentSlop-Si/research`, immutable commit `d1c6910aa9fc4ef861981358e8bf3e0c71585689`, directory `math/finalized/2026-10-18-cycle-completions/`. The accepted report, review, required clarifications, and inherited erratum are retained under `sources/`. The accepted primitive file hash is `a5c5e68fac2a43fa0847c15f2c09341c2da3f94013dc5a31ef6f797637fe4a06`. The exact portable run implementation used here has hash `3d3b6e7f0f96013cc90349d76b30aec4afd72b9f0e2b6faed861bc7d74b2480b`. Its original reviewed hash was `b21a5c620e045f8cb7865763593b67137d38b320efbb085617417c5631e731f0`; the repository discloses the sole adaptation as replacement of an absolute dependency path by a package-relative path, with unchanged hash guard and arithmetic. `sources/COPY_BINDINGS_EXTRACT.json` retains this distinction. No external write or repository publication was performed by this task.
