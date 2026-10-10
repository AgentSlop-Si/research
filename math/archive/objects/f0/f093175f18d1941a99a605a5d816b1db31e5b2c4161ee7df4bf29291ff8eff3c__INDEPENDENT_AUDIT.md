# Independent audit: ramified half-degree Rogers–Szegő families

## Verdict

**Accept the stated theorem and its scalar-bank corollary within the stated model. No mathematical correction is required.**

For every prime `p ≡ 1 (mod 4)`, the half-degree polynomial

`H_((N−1)/2)(z;ζ_N)`

is squarefree in characteristic zero at each of `N=5p`, `N=9p`, and `N=13p`. The ramified argument proves the cases `p∤d`; the independently verified isolated certificates supply `N=25` and `N=169`. In the accepted common-cycle scalar-resolvent model with one free diagonal, the minimum is therefore `(N−1)/2` for all these orders.

This verdict rests on an independently checked uniform algebraic proof, not finite target-order tests. All complete fixed-base remainders, ordinary-discriminant normalizations, bad-prime examples, and finite exceptions audited here agree with the submitted package. No claim of literature priority, publication novelty, or all-composite squarefreeness follows from this audit.

### Recommended wording clarification

The sentence in submitted §6 that drops the congruence restriction should keep the coprimality condition explicit:

> For each fixed `d∈{5,9,13}` and every odd prime `p∤d`, squarefreeness holds without requiring `p≡1 (mod4)`. The isolated `N=25,169` certificates cover the two additional exceptions needed for the displayed `p≡1 (mod4)` families.

The present text can already be read this way from its immediately preceding exclusions. This is a scope clarification, not a defect in the theorem. In particular, this argument does not establish `N=27` by substituting `d=9,p=3`.

## 1. Scope and independence

The principal audited item is `ramified_chirp_squarefreeness_0341/RESEARCH_REPORT.md`, together with its sealed evidence. The inherited scalar-bank model and resonance result were checked against the relevant statements and proof in `diagonal_chirp_classification_0246/CLASSIFICATION.md`. This audit does not silently broaden that model.

No supplied or predecessor implementation was executed, imported, compiled, or used as an arithmetic module. Their bytes were hashed for preservation. The two existing exceptional certificates were read as JSON data. Only the two freshly authored programs in this audit directory were executed:

1. `audit_exact.py`: standard-library rational cyclotomic fields, freshly implemented polynomial arithmetic, multiplication-norm determinants for resultants, q-Pascal construction, truncated formal series, and modular certificate verification.
2. `audit_discriminants.py`: direct Gaussian product construction and installed SymPy exact polynomial arithmetic, using the reciprocal quadratic-product discriminant identity and ordinary discriminants. This also duplicates all three fixed-base computations by a different arithmetic route.

The two routes were authored in this audit by one auditor; they are not represented as two independent human implementations. The first route does not depend on SymPy. All computations are exact, with no numerical root tests.

The input manifest and its three immediate predecessor manifests contain 56 entries in total, all verified. The 78 recorded predecessor hashes also match. Ninety-four distinct protected files were hashed before and after this audit and were unchanged.

## 2. Independent q-Lucas derivation

Put `n=Ad+b`, `0≤b<d`, with `d` odd and `ω` primitive of order `d`. The finite q-binomial identity is

`∏_(j=0)^(n−1)(1+tq^j) = Σ_k q^(k(k−1)/2) [n choose k]_q t^k`.

At `q=ω`, each complete block has product `1+t^d`. Thus the product becomes

`(1+t^d)^A ∏_(j=0)^(b−1)(1+tω^j)`.

For `k=cd+e`, `0≤e<d`, coefficient comparison gives the usual q-Lucas formula. There is no missing phase: the exponent difference

`[(cd+e)(cd+e−1)−e(e−1)]/2 = d·c(cd+2e−1)/2`

is an integral multiple of `d`, since `d` is odd and `c(cd+2e−1)` is even. Consequently

`[Ad+b choose cd+e]_ω = binom(A,c)[b choose e]_ω`,

with the right side zero for `e>b`, and therefore

`H_n(z;ω)=(1+z^d)^A H_b(z;ω)`.

This independently supplies the exact degeneration used in the report. Sagan's cited Theorem 2.2, on journal pages 131–132, is an appropriate primary source for the known q-Lucas congruence: [author-hosted paper](https://users.math.msu.edu/users/bsagan/Papers/Old/cpq-pub.pdf). The source was opened and the theorem located during this audit.

## 3. Independent Hermite leading-model derivation

Write `F(z)=1+z^d`, `G(z)=H_b(z;ω)` and choose `α^d=−1`. Work entirely with formal series in characteristic zero:

`q=ω(1+ε²)^(1/d)`, `z=α+εx`.

Then `q^d−1=ε²` exactly. The ordinary formal generating function is

`Σ_n H_n(z;q)t^n/(q;q)_n = exp(Σ_(k≥1) (1+z^k)t^k/[k(1−q^k)])`.

It follows by multiplying the two q-exponential series and solving `E(qt)=(1−t)E(t)` coefficientwise; no analytic convergence claim is needed.

Separate the logarithm into terms with `d|k` and the regular remainder. For `u=t^d`, the coefficients of `u` and `u²` in the singular logarithm are respectively

`x/(αε)+O(1)` and `−1/(2dε²)+O(ε^−1)`.

For `u^l` with `l≥3`, the pole order is at most two and is strictly below `l`. More explicitly, odd `l` have a numerator vanishing to first order in `ε`, while even `l` have a nonzero constant numerator; both denominator orders are two. Hence the order-`ε^−a` term in the coefficient of `u^a` is determined exclusively by the first two terms above:

`[u^a] exp(singular logarithm) = ε^−a d^−a/2 He_a(√d x/α)/a! + O(ε^(−a+1))`.

The regular factor's `t^b` coefficient at `ε=0` is `G(α)/(ω;ω)_b`. Its higher possible degrees `b+jd`, `j>0`, multiply singular coefficients of index `A−j` and cannot contribute at pole order `A`. Finally,

`(q;q)_(Ad+b)= (−1)^A A! d^A (ω;ω)_b ε^(2A)(1+O(ε²))`.

The resulting identity is exactly

`H_n(α+εx;q)=ε^A (−1)^A d^(A/2) G(α) He_A(√d x/α)+O(ε^(A+1))`.

No square-root ambiguity remains: its coefficient at `x^(A−2j)` is

`(−1)^(A+j) A! d^(A−j) G(α) α^(−A+2j) / [2^j j! (A−2j)!]`.

The formula remains a true identity when `G(α)=0`, but then it supplies a zero coefficient rather than a leading cluster model. The report correctly distinguishes those statements.

### Exact controls

The fresh series calculation checks every coefficient below `ε^A` and every coefficient of the asserted `ε^A` polynomial at every cluster `α=−ω^j`. It covers 39 clusters in seven cases:

`(d,A,b)=(1,5,0),(3,3,0),(5,2,2),(5,3,0),(9,2,4),(13,2,6),(3,2,1)`.

These deliberately include odd `A`, composite `d=9`, the largest claimed fixed base, and an overlapping cluster. All pass. They guard the symbolic argument; they do not replace it.

## 4. Ordinary discriminant: exact order, coefficient, and sign

Assume now `Δ=Disc(G)≠0` and `R=Res(F,G)≠0`. The Hermite discriminant is

`Disc(He_A)=P_A=∏_(j=1)^A j^j`.

This can be obtained without a real-root theorem. Differentiation gives `He_A'=A He_(A−1)`. If `r_A=Res(He_A,He_(A−1))`, the three-term recurrence gives

`r_A=(−1)^(A−1)(A−1)^(A−1)r_(A−1)`.

Its sign cancels the ordinary discriminant sign, yielding the displayed positive integer `P_A`, which is nonzero in characteristic zero. Formal implicit lifting then produces exactly `A` simple branches at each cluster:

`z_(α,j)=α+ε(α/√d)h_j+O(ε²)`.

Together with the `b` simple residual branches, these account for all `n=Ad+b` roots of the monic polynomial.

Within-cluster differences contribute

`ε^(dA(A−1)) d^(−dA(A−1)/2) P_A^d`.

The omitted product of powers of the `α` is indeed one: the product of the roots of `z^d+1` is `−1`, raised here to the even exponent `A(A−1)`. Between distinct clusters the contribution is `(Disc F)^(A²)`, where

`Disc(z^d+1)=(−1)^((d−1)/2)d^d`.

Residual-root differences contribute `Δ`, and cluster-to-residual differences contribute `R^(2A)`. Thus, with `K=dA(A−1)/2`,

`D_n(q(ε))=ε^(2K)(C(ω)+O(ε²))`,

`C(ω)=(−1)^(A(d−1)/2)d^(dA(A+1)/2)P_A^d ΔR^(2A)`.

The exponent is exact because every displayed factor is nonzero. The remainder is even because `D_n(q(ε))` is an even series. In particular, the sign is not an absolute-value approximation; replacing the sign by a universally positive coefficient would be wrong.

### Independent ordinary-discriminant controls

Fresh exact full discriminants were constructed for degrees `1–7,9,10,12`. For degrees `1–7` the reciprocal contraction was also checked against the direct ordinary derivative discriminant. The contraction is the algebraic identity

`Disc[z^r P(z+z^−1)] = P(2)P(−2)(Disc P)^2`.

It follows by factoring into monic quadratics `z²−u_jz+1` and multiplying their discriminants and pairwise resultants. For odd-degree `H`, first divide by `z+1` and include the square of the quotient evaluated at `−1`.

Exact orders and the entire coefficient, including `Q_d(ω)^K`, pass for:

| `d,A,b` | `n` | exact `Φ_d` order |
|---|---:|---:|
| `1,5,0` | 5 | 10 |
| `3,2,0` | 6 | 3 |
| `3,3,0` | 9 | 9 |
| `5,1,2` | 7 | 0 |
| `5,2,2` | 12 | 5 |

The `d=3,A=3,b=0` case independently checks the negative leading constant `−488038239039168`. The overlap controls reproduce `ord_(Φ_3)D_7=5` and `ord_(Φ_3)D_10=12`, rather than the inapplicable separated values 3 and 9.

## 5. Exact cyclotomic bridge, including arbitrarily large K

The integer nature and timing of the division are essential. The ordinary discriminant `D_n` lies in `Z[q]`. Galois conjugacy transports its exact multiplicity `K` to every primitive `d`th root. Therefore

`D_n(q)=Φ_d(q)^K E_n,d(q)` with `E_n,d∈Z[q]`.

One can divide successively by the monic polynomial `Φ_d`; each exact rational division has an integral quotient. Set `Q_d=(q^d−1)/Φ_d`. The leading expansion yields the equality in `Q(ω)`

`E_n,d(ω)=Q_d(ω)^K C(ω)`.

Now set `A=(p−1)/2`, `b=(d−1)/2`, with `p` odd and `p∤d`. At one prime of `Z[ω]` above `p`, suppose `Δ` and `R` are both nonzero. Then:

- `d` is a unit there;
- `P_A` is a unit because `A<p`;
- `Q_d(ω)` is a unit because `q^d−1` is squarefree modulo `p` and its distinct cyclotomic factors are pairwise coprime modulo `p`;
- `E_n,d(ω)` is consequently nonzero at that residue factor.

If `D_n(ζ_dp)=0`, cyclotomic irreducibility implies `Φ_dp|D_n` over `Z[q]`. Since `Φ_dp` and `Φ_d` are distinct irreducibles, this would force `Φ_dp|E_n,d`. The integer identity

`Φ_dp(q)Φ_d(q)=Φ_d(q^p)`

then reduces in the polynomial domain `F_p[q]` to

`Φ_dp(q)≡Φ_d(q)^(p−1) mod p`.

Cancellation here is polynomial cancellation before evaluation; there is no division by a zero root value. It follows that `E_n,d(ω)` would vanish at every prime above `p`, contradicting the one chosen good factor.

**The proof needs no inequality between K and p−1.** The entire power `Φ_d^K` was removed over the integers before reduction. A direct p-adic Taylor-leading-term assertion without this division would not be an equivalent proof.

The source's ramification reference is correct but not needed to close this elementary polynomial argument. Sharifi's Proposition 3.1.21 states the expected exponent and residue degrees: [author's Chapter 3](https://math.ucla.edu/~sharifi/notes/algnum-ch03.html). That statement was located and checked. No literature-priority conclusion is drawn from either reference.

## 6. Content criterion and complete fixed-base verification

Let

`B_d=rem_(Φ_d)(D_b·Res_z(z^d+1,H_b))`, `b=(d−1)/2`,

and let `c_d` be its positive coefficient content when `B_d≠0`. For `p∤d`, the quotient `F_p[q]/(Φ_d)` is a product of fields. Its element represented by `B_d` is nonzero if and only if at least one component is nonzero. That is exactly one residue factor where both the discriminant and the resultant are nonzero.

Since the canonical remainder has degree below `deg Φ_d`, its reduction is the zero class if and only if every coefficient is divisible by `p`, equivalently `p|c_d`. Thus `c_d≠0` and `p∤dc_d` suffice.

This is an **existence-of-one-good-factor test**, not a claim that `B_d` is a unit in the entire product ring. A norm or an everywhere-good-factor test would impose an unnecessarily stronger condition.

Two fresh computational methods reproduce every complete remainder in the submitted `CONTROL_RESULTS.json`: ordinary discriminant, cluster resultant, their product modulo `Φ_d`, and content. Exact string comparisons of the three rendered polynomial remainders and equality of contents are separately recorded in `SUPPLIED_CLAIM_COMPARISON.json`.

The decisive values are

`c_5=5`, `c_9=6561=3^8`, `c_13=28561=13^4`.

The first method computes resultants as multiplication-map determinants in the explicitly implemented rational cyclotomic field. The second computes direct resultants over `Z[q]` and only then reduces. Agreement includes all large coefficients at `d=13`, not just the contents. Full ascending coefficient arrays appear in `EXACT_ARITHMETIC_RESULTS.json`; readable polynomial expressions appear in `DISCRIMINANT_RESULTS.json`.

Consequently all odd primes `p∤d` pass at each of the three fixed bases. This is a finite fixed-base calculation feeding a uniform theorem, not a target-order census or an inference from finitely many target orders.

## 7. Bad primes, overlap, and higher ramification

Every asserted caution is valid and matters:

1. **A specific bad residue factor does not refute characteristic-zero squarefreeness.** At `d=5,p=61`, the primitive roots `9,20,34,58` give discriminants `35,10,1,0`. At `58=−3`, the fresh polynomial is `z²−2z+1=(z−1)²`. The discriminant gcd is `q+3`, while the cluster-resultant gcd is one. Other factors remain good.
2. **Residual squarefreeness does not imply cluster separation.** At `d=13,p=5`, the fresh discriminant gcd with `Φ_13` is one, while the resultant gcd is `q⁴−2q³−2q+1`. It is a proper factor, so a good component still exists. This distinction does not invalidate the `N=65` conclusion.
3. **Intrinsic overlap invalidates the exact separated order.** If `d≡3 mod4`, `b` is odd and reciprocity gives `H_b(−1;q)=0`. Because `−1` is also a root of `z^d+1`, `R=0` identically and `B_d=0`. The ordinary-discriminant controls in §4 quantify two failures of the naive separated exponent. This audit does not reinterpret a zero leading coefficient as a nonzero one.
4. **Repeated ramification is not covered by the unit step.** At `N=p^a d`, `a≥2`, `p∤d`, the same decomposition gives `A=(p^a−1)/2≥p`. Hence `p|P_A`. Even with good residual factors, the displayed first coefficient is zero modulo `p`. The exact characteristic-zero division still exists under separation, but the unit contradiction no longer follows.
5. **The condition p∤d cannot be dropped.** It ensures simple lower cyclotomic reduction and unit factors `d,Q_d(ω)`. The `25` and `169` cases therefore need genuinely separate evidence, not a silent application of the ramified theorem.
6. **No universal assertion about c_d has been proved.** The three contents do not establish that all nonzero lower contents have prime factors only dividing `d`. Nor do they prove all orders `5r²`, every prime power, or every composite `N≡1 mod4`.

## 8. Isolated exceptions and scalar-bank implication

Only the two requested old certificate entries were rechecked. They were found byte-for-data equal to the corresponding entries in the original `MODULAR_CERTIFICATES.json`.

| `N` | degree | certificate field prime | primitive root |
|---:|---:|---:|---:|
| 25 | 12 | 101 | 5 |
| 169 | 84 | 2029 | 3 |

Fresh standard-library arithmetic establishes each field prime by trial division, establishes the exact multiplicative order of the root, rebuilds all Gaussian coefficients, constructs `T_m(z)=(-1)^mH_m(-z)`, verifies the stored coefficients and the full saved identity `UT_m+VT_m'=1`, and separately computes the derivative gcd. Every one of the `N` cycle nodes is nonzero under `T_m` at the final saved prime. No target range was repeated or extended.

The modular Bézout identities really imply characteristic-zero squarefreeness: an exact-order residue root defines a homomorphism from `Z[ζ_N]` to the finite field. A zero characteristic-zero discriminant would map to zero, contrary to the certificate. Galois conjugacy gives every primitive complex `ζ_N`.

For `p≡1 mod4`, all three target orders satisfy `N≡1 mod4`. The accepted scalar-bank characterization then applies:

- its nonsingular shifted Hankel matrix imposes the lower bound `m=(N−1)/2`;
- the unique annihilator is `T_m=(-1)^mH_m(-z)`, whose ordinary discriminant equals that of `H_m`;
- `T_m(0)=(-1)^m` excludes zero nodes;
- the proved uniform resonance guard is clear for `N≡1 mod4`;
- the now-verified squarefreeness supplies `m` distinct legal nodes, attaining the lower bound.

The conclusion concerns scalar coefficients, the same natural cycle `P`, first-order resolvents with nonzero nodes and `λ^N≠1`, and one free diagonal. It is not an unrestricted full-inverse minimum. For odd primes `p≡3 mod4` with `p∤d`, the squarefreeness theorem still holds, but the accepted resonance obstruction means this smaller bank minimum does not follow; the existing classification gives `(N+1)/2` instead.

## 9. Evidence and stopping boundary

The sealed outputs include full exact-arithmetic results, symbolic discriminant results, claim comparisons, run logs, source checks, preservation hashes, and both fresh programs. Small controls cover genuine sign and normalization risks, and the exact fixed-base calculation supports the quantified prime families through the proven bridge.

There is no remaining defect blocking acceptance of the stated three-family theorem. The appropriate next mathematical questions remain the overlapping-cluster case, higher ramification, and general lower-content behavior. This audit has not claimed to settle them, and correctness here does not establish novelty or publication priority.
