# Final independent review: binary Newton packing barrier

Reviewed candidate in this publication: `../source/`.

- Candidate manifest SHA-256: `8d4c66ae7182adaabe50706b3ccb9d164a6561556f8558a38aa6327d6eaecc01`
- Candidate report SHA-256: `27ee597eff6253b07635f19b3eec30cee2fa5f5626de4416f9ed0a843ea45204`

## Verdict

ACCEPT the stated, sharply restricted claims with the required centering interpretation below. No blocking mathematical defect was found in the proof review. The result is a complete complexity analysis of a defined uniformly padded, independent-node recursive algorithm, together with a genuine legal-input, one-level actual-size witness. It is not an unrestricted or input-adaptive multiplication lower bound and does not supply a compatible growing prime-Mersenne family.

The candidate and historical sources were inspected as data only. The independent control program in this review directory imports neither candidate nor historical modules. Its use of ordinary multiplication is confined to test oracles and local control arithmetic, not to the proved recursive complexity model.

## Proof checks

### 1. Native plan and exact encoding

The CRT construction is valid: for each prime-power factor q of d=E/r, E/u is coprime to q; its prescribed unit residue makes q divide R_u. Consequently d divides W_r. The selected CRT residue is positive and at most d−1 when d>1. The d=1 case is explicitly handled by k=1. Since R_r/d=k+1/d>1, beta exceeds W_(r−1). Standard mixed-radix division of b<rho≤beta≤W_r gives digits strictly below their radices, hence below P. The evaluation identity f(−P)=b is exact.

Both elementary LCM estimates used for lambda are sound. A binomial coefficient divides E_r because each summand in its prime-valuation expression is zero or one. The inequality E_r | E_ceil(r/2) binom(r,floor(r/2)) follows by covering the single possible newly introduced power of each prime. Iteration gives log2 E_r≤2r+O(log r). Thus r−O(log r)≤lambda≤4r+O(log r), and s=r lambda−O(r log r)=Theta(r^2), without a prime-distribution assumption.

### 2. Legal simultaneous actual-size witness

Every singleton block is legal because c_j W_j<W_(j+1)/2≤W_(r−1)/2<beta/2<rho. The terminal constant P−1 is legal for sufficiently large r. These are canonical legal binary blocks, not arbitrary independently selected coefficients.

The last-basis-term bound holds across the entire allowed node interval, including cases where both relevant binomial coefficients vanish. It implies that one retained singleton coordinate reaches at least one third of the row norm divided by r−1. The singleton digit bound (P−1)/(4r) therefore establishes the stated uniform polynomial-factor saturation at every node simultaneously.

The terminal constant is also essential: all lower terms have absolute sum below Q^(L−1)/2. Hence the packed integer is positive and its actual bit length is (L−1)w+lambda+O(1)=Lw−O(r). Summed over Theta(r) nodes, the allocation gap is only O(r^2). This is a real actual-argument-length witness. Choosing L=floor(3*2^(r−1)/s) makes the actual original length N have floor(log2 N)=r for all sufficiently large r; also ceil(N/s)=L. The actual source parameter regime is therefore met, not merely a declared padded promise.

This witness does not establish that recursively encountered structured children are worst cases. The report correctly keeps that separate.

### 3. Translation and volume

The telescoping formula for S_r(a+1)−S_r(a) is exact. Its increasing endpoint comparison shows that the total-log and maximum-row minimizers both lie among the two adjacent integers around the stated crossing. They need not be identical at finite rank. Windows outside 0≤a≤r−1 cannot improve the objective.

For negative nodes, the hockey-stick identity gives R(r,−h)=binom(h+r−1,r−1). For nonnegative nodes through 2r−2, the truncated row contains at least half of the full binomial sum. These yield the claimed integral formula with uniform O(r log r) error. J is strictly convex, and its derivative vanishes at the same asymptotic crossing as the minimax objective. The displayed closed expression, alpha*, and J* are consistent.

The volume calculation has the correct convention: one maximum-operand width per recursive multiplication, with no spurious factor two. The 4 term comes from 2 lambda across approximately 2r nodes; the remaining term is (2+2J*)/kappa. Byte rounding, floor/ceiling choices, and polynomial witness saturation contribute only lower-order errors. Thus the claimed range [5.2722348954−o(1), 9.0889395817+o(1)] follows from the proven native point bounds.

### 4. Exact executor, child sizes, termination, and base cases

The fixed cap bounds every row of every input, including zero and negative inputs after separate sign handling. The strict condition Q>2L A_cap^2 makes centered convolution decoding unique. Finite differences on 2r−1 consecutive integer nodes reconstruct the ordinary polynomial product, and evaluation at −P gives exactly the binary-block convolution. Its carries recover the original integer product.

The packed arguments have magnitude below 2^(Lw), so declared child capacity t=Lw is valid. The explicit guard t<n ensures strict decrease whenever recursion is entered. The n<16 base case prevents an invalid native rank. The guard can invoke schoolbook at other small sizes; since t=Theta(n/log n) uniformly across nodes, it eventually always passes, leaving only a finite fallback region. There is no implicit recursion through equal or larger capacities.

### 5. Full nonrecursive ledger

The conservative polynomial setup allowance covers the LCM, small prime factoring, CRT, weights, row norms, and window selection. These involve only polynomially many operations on at most O(r^2)-bit integers.

Mixed-radix conversion costs O(Lr^5)=O(nr^3) with elementary division. Input maps cost O(Lr^4). Packed streams and all node values together occupy O(n) bits; a fixed-tape rearrangement can use O(n log r), and bounded-window signed packing and extraction use linear stream work. No field-prime supply, roots, or auxiliary CRT reconstruction is needed in this variant.

Finite differences use polynomial local work. The Newton evaluation weights have O(r^2) bits, and O(r) schoolbook products per output block cost O(Lr^5). Intermediate sums retain O(r^2) bits, so no uncharged large cancellation or division is required. Binary carries cost O(n). These estimates fit the claimed conservative F(n)=O(n(log n)^4), including setup for sufficiently large n. The recursively listed packed products are the only nonlocal multiplications; there is no imported fast multiplication oracle.

### 6. Both recurrence inequalities

Writing y=ln n and t=Theta(n/ln n) gives ln t=y−ln y+O(1), uniformly in the node. For h(y)=y/ln y, the mean-value theorem yields h(y)−h(ln t)=1+o(1). Consequently

sum Phi_c(t)/Phi_c(n)=exp(−c)(V_r+o(1)).

For c<ln v_minus this exceeds one by a fixed eventual margin. Strong induction from a finite positive base interval gives the lower bound; the fixed capacity schedule supplies the same child requirements at every node, independent of values. For c>ln v_plus the ratio is less than one by a fixed margin, and F(n)=o(Phi_c(n)) is absorbed by a sufficiently large multiplicative constant. Strong induction gives the upper bound. Both directions are justified, rather than treating an upper recurrence as a lower bound.

The resulting n exp(Theta(ln n/ln ln n)) scale is therefore correct. The work does not prove a limiting leading exponential constant.

## Required interpretation of the centering conclusion

The accepted centering conclusion is the row-height/slot-width lower bound and its fixed-padded-schedule consequence. It is not an unqualified actual-packed-length lower bound after arbitrary centering. The paragraph's wording about changing maxima should be read as limiting their possible reduction: an arbitrarily large center can increase them.

If publication asserts actual-length resistance after common integer centering, it must add the hypothesis that the required zero block is immediately before the final constant P−1 block. This is an allowed strengthening of the construction. For center c, those trailing coefficients are −c and P−1−c, so at least one is nonzero. With strict centered packing separation, lower coefficients cannot cancel that leading nonzero coefficient. Thus the centered integer has at least (L−2)w bits up to an absolute additive constant, and the actual-length deficit is at most 2w+O(1)=O(r) per node for a size-minimizing center. The same leading volume survives.

Without the placement hypothesis, an actual-length-after-centering assertion can fail: place the zero and singleton blocks early, fill a long tail with constant P−1 blocks, and center by P−1. The long tail disappears. This counterexample does not affect the uncentered actual-size witness or the uniformly padded recursion theorem. Publication must preserve this precise scope or explicitly include the sufficient trailing-zero hypothesis.

## Scope boundary

The evidence supports closure of the defined padded independent-packing branch only. It leaves open the source's genuinely data-adaptive recursion, cross-node sharing or fused recovery, arbitrary multiplication algorithms, historical novelty, and existence of the original compatible growing prime-Mersenne specialization. The candidate says this explicitly and does not overclaim those conclusions.

## Fresh controls

The independently written `independent_checks.py` checks all candidate manifest and source pins, elementary LCM claims, exact canonical encoding, simultaneous height saturation, exact shift/two-candidate minimizers, signed and zero-valued complete recursive products, equality of capacity call schedules across different values, and large exact child/actual-length metadata. The completed outcomes are recorded in `RESULTS.json` and `RUN.log`. The centering scope and its sufficient strengthening are also isolated in `SCOPE_CLARIFICATION.md`, with 2,226 independent placement controls and a native-rank counterexample recorded in `CENTERING_RESULTS.json`.

Completed fresh run: 127 exact ranks, 60 full recursive products through 512-bit declared capacity, 62,648 total executor calls, 11 exact metadata ranks through 384, and 2,226 centering-placement controls all passed. Candidate hashes remained unchanged at finalization.
