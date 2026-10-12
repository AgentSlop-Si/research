# GTSL recurrence and compiler review

Reviewed 12 October 2026. This is a publication derivative of the complete scoped review. Private source-location metadata has been removed; the mathematical review, proofs, counterexamples, line references, caveats and recommendations are retained. One companion filename has been updated to match this collection.

## Conclusion

The fixed-saving recurrence theorem is valid under its stated uniform bound and a consistent nonnegative cost model. The source does not supply the growing tensor-union compiler needed to instantiate that theorem. Its claim in section 5 that convergence of rho(w) to 1/2 alone yields O(N log log N) is false. A quantitative convergence condition is necessary. The polynomial-rate hypothesis in section 13, with gamma > 0 and c fixed, actually suffices for O(N log log N), with no rate-dependent power loss at that endpoint.

This review establishes a corrected conditional recurrence result and identifies the missing circuit certificate. It does not establish a new Fourier algorithm, a Fourier lower bound, a historical novelty claim, or a public-result comparison.

## Sources and preserved evidence

The [original manuscript](originals/GTSL_Fourier_Theory_2026-10-12.md) is preserved byte for byte: 17,218 bytes, SHA-256 68b161ca9880853d38bcf060587a2813cf8b702e5a2c1d75f59f7ae599c42ad1. It contains the original endpoint-rate error and is presented as a candidate, not an accepted algorithm.

The retained original source ZIP has SHA-256 7dc77fac78b9251a97451d317ef395026fa41faf2c6b01c4ab78f73fe8df9433. Its Markdown and verifier are byte-identical to the separately supplied files. The source verifier has SHA-256 21e9f577f27118012ffc52f26cc3fae7ea0ef50cc9d1cd8bbb8270b4fedad292 and was inspected statically, never executed. Neither that code nor an executable archive is included in this prose collection.

Line references below refer to the preserved manuscript. The source report SHA-256 and derivative relation are recorded in FILE_MANIFEST.json. The archived independent result record is included separately; it is a historical finite-control result, not a new compiler certificate.

## What the source proves conditionally

For N = 2^w, let a = 2^floor(w/2), b = 2^ceil(w/2), and f(w) = C(2^w)/2^w. Dividing the proposed cost inequality by N gives exactly

f(w) <= rho(w) [f(floor(w/2)) + f(ceil(w/2))] + kappa.

The normalization is correct: a C(b)/N = C(b)/b and b C(a)/N = C(a)/a. The classical Cooley–Tukey identity in section 1 is also correct when omega_a = omega_N^b and omega_b = omega_N^a, with the index conventions stated there.

The recurrence must apply to one consistently defined family C, at every sufficiently large integer w. C must include the work that the theorem claims to bound. Assume f is nonnegative, its finite base range is bounded, rho(w) is nonnegative, and kappa is a finite nonnegative constant independent of w. Then an eventual bound rho(w) <= rho gives:

- If 1/2 < rho < 1, C(2^w) = O(2^w w^alpha), alpha = log2(2 rho).
- If rho = 1/2, C(2^w) = O(2^w log w).
- If 0 <= rho < 1/2, C(2^w) = O(2^w).

These are upper bounds. Equality recurrences describe sharp worst-case envelopes, not lower bounds on the DFT.

### Explicit rounded-child proof and constants

First suppose the recurrence holds for every w >= 2 and f(1) <= B. Put d(w) = ceil(log2 w) and q = 2 rho. Both rounded children have depth at most d(w)-1. No monotonicity of f is needed.

If q >= 1, induction gives

f(w) <= B q^d + kappa (1 + q + ... + q^(d-1)),  d = d(w).

For q > 1 this is

f(w) <= (B + kappa/(q-1)) q^d - kappa/(q-1)
     <= q (B + kappa/(q-1)) w^log2(q).

For q = 1 it is B + kappa ceil(log2 w).

For q < 1, the constant M = max(B, kappa/(1-q)) is an inductive upper bound. If the recurrence or the rho bound starts only after a finite threshold, enlarge the base range and B; the same asymptotic conclusions follow. This supplies the missing detail behind the source's odd-w sentence, lines 227–228.

The theorem concerns dyadic transform lengths N = 2^w, including odd w. It does not establish the same cost for arbitrary integer N. Zero-padding to a different transform length does not, by itself, compute the original N-point DFT.

## Exact variable-rate criterion

On the subsequence w = 2^j, define g_j = f(2^j) and q_j = 2 rho(2^j). Then

g_j <= q_j g_(j-1) + kappa.

For q_j >= 0, repeated substitution gives the exact maximal envelope

E_j = g_0 product_(i=1..j)(q_i)
    + kappa sum_(t=1..j) product_(i=t+1..j)(q_i).

An empty product equals 1. Thus g_j <= E_j, with equality attainable by the scalar recurrence. For fixed positive base and kappa, an O(j) conclusion from this dyadic recurrence is equivalent to E_j = O(j). Convergence q_j -> 1 is not that condition. The product-sum formula remains meaningful even if some q_j are zero; a quotient-of-products formula would need a positivity assumption.

With kappa > 0, this criterion simplifies: write S_j for the displayed sum of suffix products and P_j for the full product. For j >= 1, P_j <= q_1 S_j, because the t=1 term of S_j is the product from i=2 through j. Hence kappa S_j <= E_j <= (g_0 q_1 + kappa) S_j. Thus S_j = O(j) is necessary and sufficient for the maximal dyadic envelope to be O(j). For zero overhead and positive base, the criterion instead is P_j = O(j).

For an all-integer sufficient condition, put

Q_j = max(1, sup {2 rho(w): 2^(j-1) < w <= 2^j}).

A shell maximum of f is bounded by the equality recurrence with Q_j. Hence a bounded cumulative positive shell excess, sum_j (Q_j - 1) < infinity, ensures all products are bounded and f(w) = O(log w). This is sufficient, not necessary: the positive-overhead recurrence can tolerate some nonsummable deviations.

For completeness, the exact all-integer analogue is the weighted recursion tree. Split each internal node of size m into floor(m/2) and ceil(m/2), stopping at 1. Give the root weight 1 and multiply by rho(m) along each outgoing edge from a node of size m. If W(v) is the product of these factors from the root to v, the equality envelope is

E(w) = B sum_(leaves l) W(l) + kappa sum_(internal nodes v) W(v).

Every recurrence solution with f(1) <= B is at most E(w), and equality is attainable. Thus E(w) = O(log w) is the exact rounded-recurrence condition. This statement handles arbitrary oscillations in rho; the shell bounds are simpler sufficient criteria. It is a condition on the recurrence envelope, not a lower bound on any separately constructed Fourier circuit.

### A sharp elementary rate family

For q_j = 1 + c/j, c >= 0, and fixed positive kappa and base,

- 0 <= c < 1 gives g_j = Theta(j).
- c = 1 gives g_j = Theta(j log j).
- c > 1 gives g_j = Theta(j^c).

Indeed product_(i=1..j)(1+c/i) = Theta(j^c), and the inhomogeneous sum becomes that product times a sum comparable to sum_(t=1..j) t^(-c).

The same O(log w) conclusion holds for all rounded splits if

0 <= 2 rho(w) <= 1 + c/d(w),  0 <= c < 1.

Choose M >= max(f(1), kappa/(1-c)). The induction f(w) <= M(d(w)+1) follows because each child is at most M d(w), so the right side is at most M d(w) + M c + kappa <= M(d(w)+1).

The sharp classifications above use positive additive overhead. If kappa = 0, the homogeneous product alone controls growth and the threshold behavior changes.

## Concrete counterexamples to overly broad endpoint statements

### Convergence to one half does not imply the critical logarithm

For every integer w >= 2, let d(w) = ceil(log2 w) and

rho(w) = (d(w)+1)/(2 d(w)).

Define f(1) = 1 and define f(w) by equality in the rounded recurrence with kappa = 1. This is a well-defined nonnegative recurrence, and rho(w) tends to 1/2. On w = 2^j, q_j = (j+1)/j, and exactly

g_j = (j+1) H_(j+1),

where H_m = sum_(i=1..m) 1/i. Therefore g_j/j grows without bound. On N = 2^(2^j), the recurrence permits work of order

N (log log N) (log log log N),

rather than O(N log log N). This directly refutes the inference at source lines 291–310. It is a counterexample to what follows from the recurrence, not a claim that a Fourier circuit has this cost or that faster Fourier circuits are impossible.

Even a fixed power of log log N need not follow from the limit alone: q_j = 1 + 1/sqrt(j) gives a product at least exp(c sqrt(j)) for a positive constant c and sufficiently large j. The equality recurrence dominates that product. This eventually exceeds j^A for every fixed A.

What the limit does imply is the weaker bound: for every epsilon > 0, f(w) = O_epsilon(w^epsilon), and thus C(N) = O_epsilon(N (log N)^epsilon). This follows by eventually bounding rho(w) by 2^(epsilon-1), for 0 < epsilon < 1, then applying the fixed-saving theorem. One can describe this as N (log N)^(o(1)), with the conventional upper-bound meaning.

### Pointwise inequalities need uniform margins

The final summary at lines 763–783 must retain the fixed-margin qualifications from Theorem 3.1.

- rho(w) < 1 for every w is insufficient for o(N log N). For w >= 2, choose rho(w) = 1 - 1/w, kappa = 1, and f(w) = w. Since the children sum to w, the recurrence holds with equality. The cost remains N log2 N.
- rho(w) < 1/2 for every w is insufficient for O(N). Choose rho(w) = d(w)/(2(d(w)+1)), kappa = 1, and the equality recurrence with f(1)=1. On w=2^j, q_j=j/(j+1) and g_j=(j+2)/2 exactly, which is unbounded.

An eventual bound by a fixed rho < 1/2 is sufficient for linear work. Merely approaching 1/2 from below is not.

## Corrected scaling lemma for section 13

Assume the same cost model and base conditions, and for all sufficiently large w,

0 <= rho(w) <= rho_* + c/w^gamma,

where c >= 0 and gamma > 0 are fixed and 0 <= rho_* < 1. Then:

1. If rho_* > 1/2, C(N) = O(N (log N)^log2(2 rho_*)).
2. If rho_* = 1/2, C(N) = O(N log log N).
3. If rho_* < 1/2, C(N) = O(N).

For the critical case, the positive shell excess is at most 2c 2^(-gamma(j-1)), whose sum is finite. Every accumulated product is at most exp(2c/(1-2^(-gamma))) after absorbing the finite base range; the additive term contributes O(j). For rho_* > 1/2, divide shell factors by 2 rho_*; the remaining perturbations likewise have a bounded product, preserving the limiting exponent. For rho_* < 1/2, the perturbation eventually falls below a fixed part of the gap to 1/2.

Section 13 should specify gamma > 0 and replace its rate-dependent critical-power language, lines 672–674, with conclusion 2 above. The assertion that only a fixed power saving follows above the threshold is valid but can be sharpened to conclusion 1.

## What is still required for a Fourier algorithm

The source labels Conjecture 9.1 as unproved, lines 506–531 and 732. That label is essential. Neither the Cooley–Tukey identity, diagonal conjugacy, existing finite codelets, nor the recurrence analysis supplies the missing compiler.

A valid circuit theorem would need all of the following:

- One explicit exact all-input family of scalar DAGs for every sufficiently large relevant w, and a uniform generator or rewrite schema with proved cost.
- A fixed gate model, including fan-in, output convention, operations counted, permitted scalar constants, and whether wire permutations are free or charged.
- A noncircular comparison using the same recursive family C on both sides. The child baseline cannot be deliberately inflated or changed between levels to make a savings ratio look better.
- A w-independent nonrecursive overhead bound kappa N, covering whatever setup, routing, indexing, storage and scalar work the claimed C includes.
- A proved rho bound at all required scales, with a convergence-rate hypothesis adequate for the claimed complexity. A finite trend is not a uniform theorem.
- Exact output correctness and scalar generation/height certificates compatible with the declared arithmetic model.

The two axis banks in Cooley–Tukey occur in a composition separated by twiddles. Finding identical symbolic forms can justify particular gate deletions, but the diagonal-conjugacy identity alone does not prove that enough forms coincide. Dense canonicalization or exact search may cost far more than the proposed evaluation circuit. If such work is part of the uniform algorithm, it must be charged; if it is offline mathematical discovery, it cannot be used as evidence of an efficient uniform circuit generator without an additional construction theorem.

### Cold start and constants

A supplied primitive omega_N in an exact-complex arithmetic model can generate its powers and child roots by charged arithmetic. That does not establish generation of all other proposed coefficients within O(N). Starting from rational constants and ordinary field operations alone cannot manufacture arbitrary new cyclotomic roots. The model must explicitly state whether roots are supplied, are legal built-in constants, or require additional operations.

Distinguish:

- input-dependent evaluation work;
- input-independent scalar preparation and memory allocation;
- generation of the circuit/schedule;
- mathematical certification of the constructed family;
- bit complexity of exact coefficient representation and arithmetic.

An evaluation-size bound with preloaded arbitrary coefficients is not automatically a cold-start uniform runtime bound. Reusing tables over many transforms does not satisfy the source's fresh-input, fully charged one-call goal unless the amortization model is explicitly authorized and stated. Verification of all N^2 transfer entries may be appropriate for finite research certificates, but cannot be counted as O(N) production setup.

The coefficient-volume implication in section 7 is algebraically correct conditional on its stated ledger inequality: the maximum log-weight is at least the total required weight divided by the number of gates. This is a necessary condition on a putative circuit, not a method of constructing one. A magnitude lower bound is not itself a bit-complexity or conditioning theorem; compact symbolic representation and the cost of using it need separate analysis.

### Measuring rho without a free offset

The proposed empirical statistic (C_union(N) - kappa N)/(a C(b)+b C(a)), source lines 623–635, is meaningful only after kappa and the accounting convention are fixed independently of the observed result. Choosing a larger kappa after seeing a small instance can make the reported rho arbitrarily small, even negative. A valid finite experiment should publish raw total counts, child-bank counts, actual nonrecursive work, the predeclared overhead bound, and the resulting inequality. Finite success still needs a scalable construction and uniform proof.

## Imported verifier scope and stronger certification

Static inspection of verify_gtsl_core.py shows:

- It checks classical balanced Cooley–Tukey against a direct DFT over the field with 257 elements at N = 16, 32, 64, 128 and 256.
- At each N it uses one vector, x_j = 7 + 11j + 3j^2 modulo 257.
- It checks the elementary fixed-rho affine recurrence against its closed form for rho = 3/4, 1/2 and 2/5, base 5, kappa 3, through depth 12.
- It does not construct a fused tensor-union DAG, certify a sub-one savings ratio, test the varying-rho claim, audit coefficient magnitude/preparation, or establish a uniform all-input complex circuit.

A single vector cannot certify a linear map. Here the failure is explicit: x_0 = 7 and x_1 = 21, so the nonzero rank-one perturbation

E = e_0 (21 e_0^T - 7 e_1^T)

annihilates the tested vector. F_N + E therefore passes that one-vector comparison but differs from F_N on e_0 by 21 e_0. This demonstrates a limitation of the test, not a defect in the classical Cooley–Tukey formula.

Testing all standard basis vectors certifies the whole map over the chosen finite field. It still does not automatically certify a characteristic-zero cyclotomic identity: a nonzero error can vanish under a particular specialization. Exact symbolic identities, or a justified lifting/reconstruction argument with the necessary bounds, are needed for that inference.

The Weyl certificate in source section 11 is sufficient when conventions are explicit: X e_j = e_(j+1 mod N), Z = diag(omega_N^k), MX = ZM, and M e_0 = 1. Then M e_j = Z^j 1 for every j, giving every DFT entry. This requires exact operations in the claimed field and a verified primitive root. The imported script does not implement that certificate.

## Recommended source edits

1. Retain the fixed-saving theorem, adding nonnegative rho/base conditions and the rounded-child proof.
2. Replace section 5's limit-only O(N log log N) conclusion with the weaker N(log N)^(o(1)) consequence, and state a sufficient quantitative rate for the critical bound.
3. Separate the half-limit conjecture from the stronger critical-rate or eventual-half conjecture. The first does not have the second's complexity consequence.
4. Sharpen section 13 using the corrected lemma above and explicitly require gamma > 0.
5. Repeat fixed uniform gaps in the final summary, rather than only pointwise rho < 1 or rho < 1/2.
6. Label the included verifier as classical-identity and fixed-recurrence checks. Add variable-rate and adversarial controls without describing them as a compiler certificate.
7. Predeclare kappa, child baselines, scalar model, cold-start accounting and the required uniform generator before interpreting finite savings measurements.

The external comparator mentioned in source sections 5–6 is not established by these files. The algebra rho < 2^(-delta) is correct conditional on comparing against an exponent 1-delta in the same model. Actual algorithmic superiority additionally requires a proved compiler and matching uniformity, root, setup and arithmetic assumptions. No historical comparison is asserted here.

## Independent control evidence

The companion independent rate audit records 11 passing groups of freshly authored exact controls. They cover fixed factors and rounded children through w = 4096, variable-rate barriers and counterexamples, zero-factor/zero-overhead cases, source hashes and ZIP identity, and the one-vector blind spot. A cold extraction checked the packet manifest and reproduced the controls byte-for-byte. The imported verifier was not executed. Finite checks support reproducibility; the asymptotic conclusions are proved analytically above and in the companion gtsl-independent-rate-audit.md.
