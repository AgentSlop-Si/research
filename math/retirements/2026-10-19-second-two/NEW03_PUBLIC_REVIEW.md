# Independent review: NEW-03 weaker complexity-bound retirement

19 October 2026 UTC. Verdict: **APPROVE only the retirement of NEW-03's blocked-Karatsuba complexity-bound activity as a weaker classical-primitive specialization.** The exact P03 recognition theorem remains valid. Its input verification, acceptance/rejection and output contract are retained; Q13/STR-Q2's separate engineering and resource obligations are not closed.

## Source and target

I read the complete [P03 common-chirp recognition theorem](https://github.com/AgentSlop-Si/research/blob/a4dacc1f15eb910ec7d494f1572bc044e2d0533b/math/archive/objects/a4/a41036c83b349ee470cf3c6fc886d23092403bb86b118cb242fd14b563b74d13__CHIRP_BLOCKED_THEOREM.md), with source SHA-256 a41036c83b349ee470cf3c6fc886d23092403bb86b118cb242fd14b563b74d13.

The original assumptions are r>=1, N>=3r, a supplied prime p with N dividing p−1, and a supplied certified primitive Nth root omega in F_p. The input is the entire exact N-vector. The recognizer accepts exactly vectors

x_j=omega^(a j²) sum_(ell=1)^s c_ell omega^(b_ell j), 0<=s<=r,

with distinct nodes modulo N and nonzero listed coefficients, allowing the empty representation for zero. It returns a fully verified representation and all unnormalized Fourier outputs on acceptance. Rejected inputs are not promised a Fourier transform. Composite/even lengths, phase aliases, full raw residual verification, and nonunit-phase Gauss evaluation retain the original handling.

The advertised arithmetic bound is O(N r^(2+kappa)+r^(2+3kappa)), kappa=log_2 3, with O(1+r^4) scalar inversions and O(N+r^4) stored field elements.

## Verified classical replacement

I reopened [Cantor–Kaltofen, On fast multiplication of polynomials over arbitrary algebras](https://kaltofen.math.ncsu.edu/bibliography/91/CaKa91.pdf), introduction and computation model on PDF pages 1–2, and the final theorem on PDF page 8. It supplies O(b log b log log b) additions/subtractions and O(b log b) multiplications for degree-below-b polynomial products, uniformly over the coefficient algebra. The algorithm is division-free. Its formal integer bilinear construction combines two relatively prime scaled products through integer linear combinations, and therefore specializes to F_p without a new field root, factoring oracle or division. The paper explicitly states the same asymptotic cost in an algebraic random-access model.

The auxiliary roots in its derivation are implemented through coefficient arrays and charged arithmetic. They are not an uncharged supplied extension-field operation. Small b is handled by direct multiplication; write L(r)=log(2r) log log(4r) to avoid a vanishing logarithmic expression at bounded r.

## Complete substituted ledger

Retain the Toeplitz eliminant and its original Karatsuba construction unchanged. In P03 notation its degree is D=binom(r+2,3), and at most C<=min(D,N/gcd(2,N)) phases survive. Replace only the ordinary short polynomial products used for the blocked full-grid root test and overlap-add residual verification.

For block length b=s+1<=r+1, the root-grid identity requires a length-b by length-(2b−1) product. Padding to O(b) costs O(b); the replacement costs O(b L(b)). There are ceil(N/b) blocks, including a possibly shorter final block, so the entire grid costs O(N L(r)). Root-power tables, interblock coefficient updates, chirp scales and output writes remain charged. The recurrence check uses the same order of work, because it performs length-b overlap-add products and checks every required residual. No sample is removed.

All other terms remain as in P03. The complete recognition ledger is therefore

O(r²(D+1)^kappa + N(D+1) + C[N L(r)+r³] + N).

The fully accepted Fourier output adds O(Nr), which is absorbed. Since D=O(r³), C=O(r³), and 2+3kappa>6, the total is

O(N r³ log(2r) log log(4r) + r^(2+3kappa)).

This includes the O(r^6) candidate setup term and the O(Nr³) phase scan; neither is dropped. The unchanged eliminant is deliberately not assigned a second, unreviewed acceleration.

The short-product replacement adds no field inversions, so O(1+r^4) remains valid. Even retaining every intermediate of one multiplication needs only O(r L(r)) field elements, within O(r²); candidates and blocks can be processed sequentially. The inherited O(N+r^4) storage bound therefore remains valid. Uniform instruction generation, addresses, data movement and integer linear combinations are covered by the cited algebraic-RAM routine. The original O(log N)-word indexing, separately charged Gauss gcd/modular-inverse work, and exclusions of root/field discovery, bit complexity, encoding and numerical stability remain unchanged.

## What this establishes

Exact product coefficients are unchanged. Consequently the existing proof's raw recurrence verification, root count, witness reconstruction and accepted-output implications remain intact. This review does not reprove those accepted components or claim the 1991 paper stated the complete recognizer.

Because L(r)=o(r^(kappa−1)), the new N-dependent term improves asymptotically as r grows while retaining the old eliminant term. It is not a strict gain in every regime: fixed r remains O(N), and large-r costs can be dominated by the unchanged eliminant. For example, r=floor((log N)^0.30) gives a new sufficient o(N log N) schedule, beyond the old stated sufficient exponent 1/(2+kappa). This does not establish a lower bound on the actual running time of the older implementation, improved constants, or a measured speedup.

Retire this weaker complexity-bound view; retain its original proof and historical exponent. The stronger statement is an explicit classical-primitive substitution within P03. It neither subsumes the entire recognition framework as earlier published work nor resolves general-rank production, caller integration, full resource contracts or other Q13/STR-Q2 engineering. No wider mathematical-impact or worldwide-priority conclusion follows.

No external record changed and no historical scientific program was rerun during this review.

## Existing stronger dyadic specialization: explicit exclusion

The current native NEW-03 record already retains the accepted dyadic bound O(N r^3 log(r+2)+r^(2+3 log_2 3)), alongside the all-length blocked-Karatsuba bound compared above. The Cantor–Kaltofen all-length substitution includes an additional log-log factor; it does not dominate that dyadic specialization. This review retires only pursuit of the weaker all-length complexity-bound activity. It preserves both accepted historical bounds and the full nonzero-phase-eliminant, exact raw-input recognition and output theorem. No prior-art domination of that complete theorem, no resolution of its exact historical priority, and no closure of separately specified engineering follow.

Source: [current native NEW-03 record, novelty row 98](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=214001003&range=A98:Z98), independently read on 19 October 2026; the dyadic and all-length bounds are in column L.
