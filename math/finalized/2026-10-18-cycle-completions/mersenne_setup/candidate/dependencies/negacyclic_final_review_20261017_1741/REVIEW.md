# Final independent review: native negacyclic and fixed-prime-radix recursion

## Verdict

PASS for the exact algebra, native-recursion construction, paid upper bound, and the report's limits on its claims. No blocking correctness defect was found in the reviewed candidate.

The improvement from an ideal full-product child volume near 4n to a native-modular child volume near 2n is correctly identified as the classical Schönhage–Strassen direction. It is not a new sub-n-log-n multiplication algorithm. Fixed prime positional radix p can be retained, but binary conversion remains separately charged.

The two initial precision recommendations have been applied and verified in the final candidate:

1. Recursive nonleaf odd-radix levels now expressly require K >= 2.
2. The algorithmic statement from the one-sided recurrence is now O(n log n log log n). The Θ statement is expressly restricted to a fully expanded fixed schedule with matching positive toll, and is not asserted for every input of a shortcutting routine.

No open revision request remains.
## Reviewed binding and scope

Candidate directory: `retained-source/negacyclic_improvement_20261017_1728`.

Candidate manifest SHA-256: `29cda568a7c2637588efb4c77937936984203ec4a112b74162606870e080260f`.

The five final manifest file bindings match. The final REPORT.md SHA-256 is `05be918010347422c9cd5dcf999268691fdb2cfd4608d2a16d6ff35a89b650ce`. The revision bindings record only the two wording refinements above; source bindings, controls, and candidate code are unchanged. All four listed source-member hashes match the archive, whose SHA-256 is `33b4bbe04c3a0bee50cb7ac534ba7785cddfd3cb0f1934f878f7230df477c367`.

The candidate report and independent-control source were read. The supplied archive's enhanced.py and relevant Radix implementation in optimized.py were read as text. No supplied code or candidate code was imported or executed. This review ran only its freshly written independent mathematical controls. Dense DFTs, Python multiplication, and modular exponentiation in those controls are explicit test oracles and make no implementation-complexity claim.

## Exact signed recovery

For coefficient t, precisely t+1 pairs are unwrapped and K-1-t pairs are wrapped. With S=(B-1)^2 the interval is

`[-(K-1-t)S, (t+1)S]`,

whose endpoint difference is D=KS. If Q>D, a negative admissible coefficient maps to a residue at least Q-(K-1-t)S>(t+1)S, while every nonnegative coefficient stays at or below the upper endpoint. The proposed threshold rule is therefore exact. Centered decoding requiring Q>2D would be unnecessarily strong.

The strict inequality matters. For B=2,K=2,t=0, coefficients -1 and +1 both occur and collide modulo D=2. The independent controls include this negative case and exhaustive decoding at the tight permitted modulus D+1.

The polynomial identity evaluates modulo the actual B^K+1. It cannot be transferred from B=p to 2^m simply because p=2^m-1. The supplied p=3,K=2 counterexample is correct.

## Binary native construction and termination

For n=Km, the full coefficient width obeys

`b=bit_length(K(2^m-1)^2)`, `r=K ceil(b/K)`.

Hence Q=2^r+1>D, K divides r, and theta=2^(r/K) has theta^K=-1. The extra factor-of-two root requirement relative to an untwisted cyclic transform is correctly retained. For a nonzero frequency ell=2^v u, pairing within blocks at distance K/2^(v+1) multiplies each term by 2^(ru)=-1. This proves the requisite zero sums over the possibly composite ring. Odd Q makes K a unit.

The residue 2^n=-1 is the single canonical input not representable in K ordinary m-bit chunks and is correctly separated. Signed floor-division carries, followed by B^K=-1, produce low-carry. Streaming chunks and bounded carries suffice; there is no hidden general multiplication in this binary reconstruction.

The outer full-product padding and the recursively native product have different interfaces and costs. Choosing n at least the sum of input bit lengths makes the outer modular result equal to the complete integer product; it does not require full-product padding at every recursive child.

The rounding analysis is valid for an admissible exponent family. With K a power of two of order sqrt(n)/log(n), m=n/K and

`r=2m+log2(K)+O(1)+O(K)`,

so Kr/n=2+O(1/log²n+log n/sqrt n). Moreover r<n eventually. A child r is a multiple of the preceding power-of-two K. The next desired power-of-two transform length is eventually smaller than that K, so it divides r. The finitely many small sizes can be leaves. Outer rounding to a multiple of the initial K adds O(K), while repeatedly rounding all exponents to powers of two would lose the intended argument.

Writing t=log n gives log r=t/2+O(log t). Normalized child weights are 1+O(log t/t). Along the descending chain these errors have a uniformly bounded sum above a fixed sufficiently large basecase. Thus their products stay bounded and the O(n log n log log n) upper bound follows. A fully expanded materialized schedule also has a positive constant normalized transform charge at each of Θ(log log n) levels, giving the stated schedule-specific Θ bound. This last conclusion should not be presented as a general lower bound, or inferred from the <= recurrence alone.

## Odd radix and strict-prime compatibility

For any odd p and even s, p^s=1 modulo 8; therefore Q_s=(p^s+1)/2 is an odd integer. The explicit radix-p digit formula in the report is correct and allows direct construction without computing a giant power by a general multiplication routine.

For K dividing s, B=p^(s/K). Choose even s' divisible by K and Q_(s')>K(B-1)^2. Then theta=p^(s'/K), theta^K=-1 and omega=theta². The same paired-sum proof makes omega principal, while odd Q_(s') makes K invertible. Neither positional primality nor modulus primality is used. Fixing p=3 is a valid strict-Mersenne-prime instance and invokes no unproved prime-density statement.

Power-of-p twiddles can be applied by splitting/rotating the native digits and using p^(s')=-1. The intermediate lies within a constant number of moduli, so canonicalization takes a constant number of linear digit passes. Scaling by K is not a rotation, but repeated modular halving is exact: for canonical u, choose u/2 when even and (u+Q)/2 when odd. A radix-p division-by-two pass is linear for fixed p. The report correctly charges log2(K) such passes per output and includes them in the transform-level cost.

Exact signed coefficients can first be evaluated modulo p^s+1 and then reduced modulo its divisor Q_s. The low-carry fold is valid for that reason. For K>=2, B>=3, the carry bound is small relative to B^K, so only constantly many final Q_s corrections are needed. The native family is closed under recursive pointwise products. The review independently exercised multiple genuine recursive levels for p=3,7,15,31, rather than testing only isolated coefficient identities.

With fixed p and controlled K, s'=2d+log_p K+O(1+K) and Ks'/s tends to 2. Packing p^d blocks does not change the leading twice-input coefficient width. The report appropriately does not reuse the fixed-p complexity statement when m varies without charging m-dependent work.

## Conversion and attribution

The supplied source actually uses an ordinary padded linear convolution and native Python pointwise multiplication. Its odd-radix encoder includes large divmod operations, power construction includes squaring, and its evaluator combines blocks using large multiplication. These operations cannot be dropped from an end-to-end bit-cost account. The report's separately paid E_p and J_p terms, schoolbook complete O(N²) option, and warning that zp=(z<<m)-z does not make arbitrary conversion linear are justified.

The native Fermat-modulus recursion, outer full-product padding, and negacyclic interpolation are documented in the primary [GMP FFT multiplication manual](https://gmplib.org/manual/FFT-Multiplication). The original [Schönhage–Strassen publisher abstract](https://link.springer.com/article/10.1007/BF02242355) states the O(N log N log log N) bound. These support the report's classical attribution; they do not establish novelty of this particular odd-radix presentation.

The primary [GMP radix-to-binary documentation](https://gmplib.org/manual/Radix-to-Binary) distinguishes power-of-two concatenation from general-radix multiplication-tree conversion. Its warning about the historical implementation description is correctly preserved in the candidate.

The candidate consistently denies a sub-N-log-N result, a practical-speed claim, and a general lower bound based on aggregate independent-child volume. Its discussion of correlated pointwise products is appropriately left open.

## Fresh exact controls

All controls passed:

- 5 final candidate manifest hashes and 4 supplied source-member hashes
- 7,799 negacyclic products, including 29,228 asymmetric threshold decodes at Q=D+1
- 1 strict-bound collision negative control
- 132 principal-root cases over odd radices 3,5,7,9,15,31
- 9,504 odd-radix power-shift controls and 1,584 inverse-halving controls
- 480 recursive native products spanning binary and odd-radix families
- 2,436 binary and 7,680 odd-radix recursively transformed nodes
- 43 exact rounded recursion transitions, with starting exponent sizes through n=2^4096; these tests operate on parameter integers only, not on n-bit operands

Files: `independent_checks.py` and `RESULTS.json`. These controls establish finite exact identities and parameter checks, not asymptotic complexity, benchmark performance, or novelty.
