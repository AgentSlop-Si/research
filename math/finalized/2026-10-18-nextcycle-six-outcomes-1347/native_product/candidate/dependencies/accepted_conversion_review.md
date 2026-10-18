# Independent final review: denominator-cleared streamed Mersenne conversion

18 October 2026 UTC. Read-only review of the candidate; fresh checks and this review were written in a separate directory. No external write.

## Verdict

ACCEPT the exact shift construction and the complete conversion bound, with the two mandatory interpretation corrections immediately below. No arithmetic-code correction is required. The candidate bytes remain unchanged; this review is a required companion.

Let alpha=log_2(3), a=alpha−1, N=Lm. In the inherited sequential-bit/array arithmetic model, the accepted conversion cost is

O(N [L^2 log(L+1)]^a),

for the stated supplied, sufficiently wide parameter families, with every actual coefficient height at most C m and ambient m eventually at least each shift's fixed kernel-limb width t. In particular, m/(L log(L+1)) tending to infinity suffices. The complete bill includes setup, both scalar maps, the streamed convolution, two output modular divisions, guards, normalization, grouping and explicit outputs. It leaves no same-scale multiplication backend symbolic. In the strict very-wide limit the packed multiplication capacities are o(N).

For admissible supplied families L=O((log N)^(4/5)), this is o(N log N). This closes the conversion subgate in that regime only. It does not prove an end-to-end fast multiplier, a transform improvement, shared point-product saving, an FFT theorem, balanced-width improvement or availability/cheap selection of growing Mersenne primes.

### Mandatory correction 1: ambient width is not actual coefficient height

The candidate's statement that m/(L log(L+1)) tending to infinity makes “all nontrivial actual shifts” satisfy W>=t is not literally true when h is chosen from the actual values. For example n=8, h=0 gives W=12 and t=32, even if the ambient binary digit width is m=8192. Likewise n=64, h=0 gives W=71<t=392 with ambient m=524288. The zero-coefficient shift is still an n-entry shift unless separately simplified.

The standalone shift bound (1) retains its stated premise W>=t. For conversion there are two valid implementations/proofs:

1. Declare a sufficient height h=Theta(m), padding rather than inspecting minimal height; or
2. Retain the actual h and use the candidate's unsimplified ledger (11). If W<=C m and m>=t, then q=ceil(W/t)<=1+C m/t=O(m/t). Consequently q K(nt)=O(n m (nt)^a), and all other terms are absorbed by that expression. Global n=O(L) and the analogous grouped sum give the same complete conversion bound.

The second argument applies directly to the delivered code. It does not require a code change, a different exponent, or a hidden same-scale operation. Every release summary must preserve this actual-width qualification rather than repeat the erroneous implication.

### Mandatory correction 2: the encoding of an unrestricted grouping parameter is paid

For 1<=d<=L, reading d costs O(log(L+1)) and is absorbed. The inherited special handling of a lone group with d exceeding its actual length correctly avoids allocating d zero digits or constructing p^d. It does not make an arbitrarily long externally encoded d free.

If that unrestricted extension is advertised without an encoding-size promise, add O(bitlength(d)) for reading/comparing d, and account for its storage if the complete scalar is retained. The standalone little-o conversion conclusion presumes this additional input cost is itself absorbed, for example d<=L or bitlength(d)=O(N). No bound depending only on N can cover an arbitrarily longer supplied parameter encoding. This is already required by the inherited conversion report and is retained explicitly here.

## Exact inspected binding and reproducibility

The reviewed candidate snapshot is in reviewed_candidate/. It matches the original candidate's 11 manifest entries and all five source pins. The original manifest SHA-256 is 7649310d8606785a8d31f83e98d3223e881a2dae4f048b6545f382d4a605cdee.

- Candidate REPORT.md: 5c860ca4c908e7dad3620250d933621a004cf7e395b75624f61315118e5a8920
- Candidate kernel_stream.py: 920af1051ed9f4bf09631c34bd8444a79855d04e6d1c287635e77e74b2003d85
- Candidate fresh_controls.py: c918ce4a87e6079058c99719b289c561067e217dab87c4fc0f9ee2048b6b3bd7

The candidate harness was rerun only in the snapshot. RESULTS.json reproduced the original byte for byte. Its inherited source reports and earlier review were inspected for the conversion, carry, grouped, arithmetic-model and exclusion premises. Historical programs were not imported or executed. The new independent checks import only this candidate's new arithmetic core.

## 1. Independent algebra and modulus proof

For 0<=i<n let s(i)=popcount(i) and u_i=i!/2^(i−s(i)). The identity v_2(i!)=i−s(i) follows by counting multiples of powers of two. Thus u_i is odd. Since u_i is a prefix of the product of odd parts of 1,...,n−1, u_i divides U=u_(n−1).

The kernel k_i=2^s(i) U/u_i is therefore an ordinary positive integer. For n>=2 and g=ceil(log_2 n), u_i<=i!<n^(n−1)<=2^((n−1)g), while s(i)<=g. Thus k_i<2^((n−1)g+g)<2^t for the declared byte-rounded t. The same t contains every u_i and U. This proof concerns ordinary denominator sizes, not the sizes of their inverses modulo 2^W.

Use A_i=2^(g−s(i))u_i a_i modulo 2^W, apply the sign sigma^i, reverse this list, and convolve with the nonnegative k. At output j, multiply the appropriate correlation coefficient by sigma^j 2^s(j)/(u_j U) in the ring modulo 2^W. All denominators are odd units. A term indexed by i>=j becomes

sigma^(i+j) 2^(g+s(j)+s(i−j)−s(i)) u_i/(u_j u_(i−j)) a_i
=2^g binom(i,j) sigma^(i−j) a_i.

The parity identity sigma^(i+j)=sigma^(i−j) holds for both signs. The powers of two in the binomial coefficient are exactly s(j)+s(i−j)−s(i). Therefore each output residue equals 2^g times the required Taylor-shift coefficient modulo 2^(H+g).

The g low bits vanish. Shifting them off keeps all H required residue bits. The hockey-stick bound gives absolute value less than 2^(h+n)=2^(H−1), so centered reconstruction is unique. The last partial limb causes no precision loss, because every modular step is computed modulo 2^(qt) and then reduced modulo 2^W, with qt>=W. No even factorial is inverted, no ordinary quotient is assumed where only a modular quotient is available, and both signed directions are proved. Empty and length-one inputs bypass the construction correctly.

## 2. Preparation and every scalar operation are real, bounded work

The forward prefix table and backward cofactor table are exact products of short odd factors o_i. Every intermediate is at most U, so truncation at t bits loses no information. The third pass starts from one Newton inverse of U modulo 2^t and uses v_(i−1)=v_i o_i modulo 2^t to construct all u_i inverses at that same precision.

The short factor width is s_0=8 ceil(max(1,g)/8). Each of the three passes contains n−1 streamed multiplications, and each such multiplication has exactly ceil(t/s_0) calls with both arguments of at most s_0 bits. The one Newton inverse contains exactly 2 ceil(log_2 t) current-precision products. Current precision grows geometrically; masking the input and correction before each product ensures O(t^alpha) total inversion work.

Consequently preparation costs O(n t (log(n+1))^a+t^alpha), together with O(nt+n log^2(n+1)) table, shift and index work. Exact factorial/cofactor integers are constructed here, but their construction is both intentional and paid. Nothing imports the earlier report's “no full factorials” wording as a free-work assumption.

For the modular division stream, set R=2^t, odd 0<u<R, and v=u^−1 modulo R. From carry c and input limb a choose b=((a−c) modulo R)v modulo R. The numerator u b+c−a is divisible by R. If 0<=c<u, it lies strictly between −R and uR. Hence its quotient c' is an integer in [0,u). This proves the carry invariant, including u=1.

Telescoping gives u Y_s=X_s+c_s R^s. At the last limb R^q is divisible by 2^W, so the output's low W bits are exactly x/u modulo 2^W. The final carry need not be zero. Each limb has exactly two t-bit multiplication calls and constant-many bounded additions/subtractions. The modular product stream has exactly one t-bit call per limb and bounded carry. Both use fixed windows rather than repeated shifting of a whole W-bit input.

The delivered shift performs nq input products, 2nq products for the division by U, and 2nq for the division by u_j. Thus its exact diagonal count is 5nq, in addition to the separately counted preparation. The second output division is not a symbolic later operation. Signs, masks, small power-of-two shifts, initial reduction, final centering and every output coefficient cost O(nW+nt) in the full ledger.

## 3. The packed convolution and its missing-carry hazards

Write every wide input as q radix-R limbs. In slab r, the desired ordinary coefficient is c_(j,r)=sum_(i<=j) x_(i,r) k_(j−i). Both multiplicands in each summand are below R, so c_(j,r)<=n(R−1)^2<nR^2<=2^(2t+g). Byte-rounded b>=2t+g prevents carries between packed coefficient slots.

The complete integer product of two capacity-S=nb packed arguments has capacity 2S. Extracting the first n b-bit windows is exact; high polynomial coefficients cannot carry backward. This is q actual packed products of width S=Theta(nt), not one deferred N-bit product.

The output digits are emitted using e_(j,0)=0 and

d_(j,r)=(c_(j,r)+e_(j,r)) modulo R,
e_(j,r+1)=floor((c_(j,r)+e_(j,r))/R).

The invariant 0<=e_(j,r)<=n(R−1) follows immediately from c<=n(R−1)^2. Thus the carry has O(t+g) bits and each pre-split value has O(2t+g) bits. The prefix identity

sum_(r<s) c_(j,r) R^r = sum_(r<s) d_(j,r) R^r + e_(j,s) R^s

proves correctness. Discarding the terminal carry is valid only modulo 2^W, because qt>=W. Discarding intermediate carries is false and is caught by the negative control.

The code prepares each source byte buffer once, reads a bounded input window for each limb, packs one slab, materializes one 2S-bit result, extracts bounded windows, and writes each output limb once. Although Python temporary objects can briefly coexist while an assignment replaces them, their number is constant; this does not change O(nW+nt) coefficient/scratch storage plus the backend workspace. Input buffers, output buffers, exact tables, signs and packing copies are all included. There is no repeated addition into a growing output integer.

The explicit difference-form Karatsuba routine terminates independently: all three recursive argument pairs have width at most ceil(w/2); for w>16 this is strictly smaller than w. The leaves use shift/add. The O(w) splitting/recombination toll gives K(w)=O(w^alpha). No call reaches the proposed Mersenne multiplier, and the abstract K in the proof names this implemented backend rather than an unevaluated external primitive.

## 4. Complete ledger, parameter scaling and address qualification

With t=Theta(n log(n+1)), S=Theta(nt) and q=ceil(W/t), direct aggregation gives

O(q S^alpha+nq t^alpha+n t (log(n+1))^a+t^alpha+nqt+nW+n log^2(n+1)).

For W>=t, q<=2W/t and the leading charge is

O((W/t)(nt)^alpha)=O(nW (nt)^a)
=O(nW [n^2 log(n+1)]^a).

The other terms are absorbed. This proves the standalone theorem. For actual W<t in an ambient m-wide converter, use mandatory correction 1 instead of falsely applying this simplification. In either case the global conversion contribution is O(N [L^2 log(L+1)]^a).

The original same-scale capacity was greater than 2nW. The new packed capacity is Theta(n^2 log(n+1)), independent of coefficient width W. In the strictly very-wide regime m/(L log(L+1)) tending to infinity it is o(N). Merely assuming W>=t does not itself make S=o(nW); at W=Theta(t) the capacities can be of the same order. The candidate properly distinguishes the standalone bound from the strict shrinking-capacity assertion.

The claimed improvement ratio (t/W)^a compares the two displayed upper bounds with the same Karatsuba cost model. It is not a measured speedup or a lower bound on the earlier algorithm. The bounded slab-size optimization statement is also sound: for kernel width k and W>=k, ceil(W/r)[n(r+k+g)]^alpha is bounded below by order n^alpha W k^a both for r<=k and r>=k, and r=k attains the order. The common-denominator convention requires a multiple of U, and log U=Theta(n log n), as seen by retaining the largest half of the factorial factors and subtracting at most n powers of two. This is only a limitation of that cost expression/representation, not an arbitrary convolution lower bound.

The primary theorem uses the explicitly inherited sequential-bit/array model, not literal Python interpreter timing. Charging O(log(nW+nt)) for each indexed window adds the displayed conservative O(nq log(nW+nt)) supplement. Monotone cursors can implement the address advances by additions rather than repeated large-address multiplication. The existing preparation/index costs remain bounded by the main arithmetic charge.

For growing L in the specified polylogarithmic family, the global address supplement divided by N log N is O(1/(L log(L+1))). Grouped operations obey the analogous bound with their actual group lengths. Bounded-length shifts admit a fixed finite sequential addition/short-multiplication circuit. A uniform dispatcher at n<=ceil(log_2 log_2(nW+4)) can use the elementary O(n^3W+n^3) direct construction; on that branch its ratio to nW log(nW) tends to zero, and off that branch n grows so the address supplement has vanishing ratio. This direct branch is a proved optional construction, not a feature falsely claimed to have been implemented in the candidate. These qualifications keep the little-o example valid in the stated address-cost variant without claiming universality over every machine model.

## 5. Conversion directions, carrying and grouping

Put B=2^m and p=B−1. Binary chunks a evaluated at B equal (T_+ a) evaluated at p. Conversely a signed p coefficient list c evaluates to (T_− c) at B. Canonical p digits are a special case. For lazy products, the identity T_−((T_+ a)*(T_+ b))=a*b follows because polynomial translation is an algebra homomorphism.

For binary inputs, canonical outputs, redundant inputs and raw product coefficients, the respective lengths are O(L) and coefficient heights are O(m+L+log L). Under the very-wide premise these are O(m). The possible extra canonical p digit and the raw product length near 2L change constants only; their t values remain O(L log(L+1)). The signed inverse-shift output is followed by ordinary binary carries, not an assumed nonnegative-coefficient readout.

The inherited exact p-divider processes a high-to-low binary limb with remainder r using s=r+a, delta=[s>=p], quotient limb r+delta and new remainder s−delta p. The identity rB+a=(r+delta)p+(s−delta p) proves exact Euclidean division. Signed floor-division correction is also exact. All states have O(m) bits. Across coefficient streams of O(m) height, including final carry tails and possible extra digits, the inherited complete O(N) cost remains valid. These carry routines were inspected as proofs; their historical code was not rerun or relabeled as new implementation.

For canonical p^d grouping with d<=L, each actual group uses a shift of length at most d and O(m)-height coefficients. There are O(L/d) groups, and n=O(d), so their total is O(N [d^2 log(d+1)]^a), bounded by the global L term. Partial groups use their actual lengths. Converting a grouped integer back uses O(d) binary chunks of width m, not one uncharged general division by p^d.

For raw grouped product coefficients of O(dm+log L) bits, converting each magnitude into p digits involves O(d) binary chunks. There are O(L/d) such coefficients. Restoring signs and placing their short expansions at offsets jd produces bounded overlap, so total explicit storage and normalization remain O(N) and the same local-plus-global cost bound applies. The ordinary long division or construction of the huge radix p^d is unnecessary. The exceptional lone-group parameter case is governed by mandatory correction 2.

This grouping argument transfers the conversion theorem only. It does not transfer or improve matrix arithmetic, transform layers, correlated point products, or the native multiplication recurrence. Their coefficient-height and precision proofs remain independent obligations.

## 6. The little-o implication and strict exclusions

For L=O((log N)^beta), beta>0, the accepted cost is at most

O(N (log N)^(2a beta) (log log N)^a).

It is little-o of N log N whenever beta<1/(2a), approximately 0.854756. For beta=4/5 the power 2a beta is approximately 0.935940, strictly below one. Since m=N/L, the very-wide ambient condition holds automatically along such supplied families as N tends to infinity. Bounded L is handled by the fixed-length/direct case and costs O(N). Additional unrestricted parameter-reading costs must still be retained as stated above.

At L=Theta(log N), this particular bound has exponent 2a>1 on log N and does not prove little-o. At balanced m=Theta(L), the narrow-kernel width premise generally fails and the unsimplified bound does not recover the advertised saving. The previous converter may be chosen as an alternative, but no improvement there is established by this candidate.

The arithmetic uses no primality. If a larger application demands suitable Mersenne primes, the parameters must be supplied and their selection/validation separately paid; no unbounded prime family is asserted. Conventional Karatsuba supplies an independent terminating primitive, not a new general multiplication theorem. The result closes the specified conversion gate only.

## 7. Fresh independent evidence

Run python independent_checks.py from this review directory. The fresh deterministic controls passed:

- 544 signed, boundary and unequal-width products with the explicit Karatsuba core.
- 219 Newton inversions, with exact call counts and every current-precision argument cap checked.
- All 4,194,304 legal 8-bit odd-division carry transitions.
- 200 complete modular-division/product cases, up to 16,385 input bits, checking every prefix, carry, partial limb, argument width and call count.
- 46 exact factorial/cofactor/microinverse tables, including the three preparation passes' exact schedules and short-factor operand bounds.
- 630 maximal/random narrow-kernel convolutions, checking every coefficient, inter-slab carry, prefix, packed call count and capacity.
- 726 exhaustive signed Taylor-shift/inverse cases against a separately written polynomial-Horner oracle, plus the empty input.
- 84 signed shift/inverse controls with complete preparation/local/packed ledgers across W<t, W=t, W>t, byte and guard boundaries.
- 36 full round-trip/lazy raw-product controls, 216 actual-length grouped round trips and 108 raw grouped product readouts.
- 16,392 independent signed floor-division checks, 40 signed raw-p readouts and 120 signed raw-grouped readouts.
- Negative controls for missing denominator, intermediate carry and guard precision, plus shrinking-capacity and actual-width counterexamples.

All candidate production multiplications in these controls use its explicit Karatsuba routine. Native arithmetic is used separately for independent expected values, polynomial-Horner/positional identities, deliberate representation perturbations and carry-identity tests. The test normalization/grouping helpers are correctness oracles, not a new production implementation or a timing claim. In particular, the finite interface checks do not replace the inherited streamed carry proof or establish complexity by measurement.

INDEPENDENT_RESULTS.json records digest e6366b206f49ec3ba847927a36ecdd7c6cbcac3496d441e31ec2d81dfba3ab86. These finite controls support the implementation; the independent algebra and ledger above establish the accepted asymptotic statement. No further mathematical or code correction is required within this scope.
