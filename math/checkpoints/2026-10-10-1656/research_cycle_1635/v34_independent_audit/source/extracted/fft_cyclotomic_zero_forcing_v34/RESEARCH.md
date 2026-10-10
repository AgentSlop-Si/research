# v34 — Cyclotomic Fourier filtration meets hypergraph zero forcing

**10 October 2026.** Goal: exact, all-output DFT on fresh arbitrary input in fully charged sequential `o(N log N)` arithmetic, ideally `O(N)` or `O(N log log N)`. This checkpoint examines **the specific 99-edge three-layer support from v33**. Its main achievement is a new **scoped arithmetic obstruction**: even allowing completely arbitrary algebraic weights integral at the cyclotomic prime, at least seven edge weights must lose unit status at that prime. It does **not** prove the support cannot compute Fourier using general complex weights, and it constructs **no faster FFT**.

## 1. Exact inherited target and coefficients

The v33 topology is three `11 x 11` matrices `A, B, C`, each the union of three edge-disjoint permutation matchings (33 nonzeros per layer), with `H = C B A`. All 99 ordered pairs `(destination, source)` are copied unchanged from v33 in `topology_11.json`, whose SHA-256 is

`4ea6269199f843363e90d3c63c2a0f12df220bbbc4b9b9a9a1ba59fd79a76a9b`.

The entire v33 archive is embedded unchanged as `PRIOR_v33_COMPLETE.zip` (SHA-256 `8daa679b23eadec2862fc8f3c4828a3bb87b469fb79536936436522fc5d04020`). v33 establishes superconcentrator connectivity and generic full-spark realizability, but **not** Fourier compatibility. This checkpoint does not change that distinction.

Write `zeta = exp(2*pi*i/11)`, `pi = zeta-1`, `K = Q(zeta)` and `O = Z[zeta]_(pi)`. More generally, the rank argument works in any valuation ring in which `zeta` reduces to 1 in characteristic 11. A coefficient `a in O` is a `pi`-**unit** iff its residue modulo `pi` is nonzero; `a` is **nonunit** iff its residue is zero (including `a=0`). No coefficients with negative `pi`-valuation are permitted in the main seven-edge theorem.

## 2. Classical uniform minor valuation, reconstructed exactly

**Theorem 2.1 (classical prime Fourier valuation).** For every prime `p`, primitive `p`-th root `zeta`, and any `k`-element row and column sets `I,J subset {0,...,p-1}`, the square Fourier minor

`D_(I,J) = det [zeta^(i*j)]_(i in I,j in J)`

has exact valuation

`v_(zeta-1)(D_(I,J)) = k(k-1)/2`.

This is a classical proof of the Chebotarev prime Fourier minor theorem, **not** a claim of v34 originality.

**Elementary complete proof.** Let `u_i = (zeta^i-1)/(zeta-1)`. In `O`, `u_i` reduces to `i mod p`. As `zeta^i=1+pi*u_i`, the binomial theorem gives

`zeta^(i*j) = sum_(r=0)^(p-1) binom(j,r) pi^r u_i^r`.

Cauchy–Binet expands every `k x k` determinant in distinct indices `0<=r_1<...<r_k<=p-1`. Its smallest possible power of `pi` is `0+1+...+(k-1)=k(k-1)/2`, and this minimum occurs only for `r=(0,...,k-1)`. The coefficient of this lowest term is

`det[u_i^r]_(i in I,0<=r<k) * det[binom(j,r)]_(0<=r<k,j in J)`.

Modulo `pi`, it equals

`Vandermonde(I)*Vandermonde(J) / prod_(r=0)^(k-1) r! (mod p)`, 

up to a harmless determinant-order sign. Because indices in `I,J` are distinct modulo prime `p` and `r<p`, every factor is nonzero. Therefore the leading coefficient is a unit; the valuation is **exactly** `k(k-1)/2`. QED.

For `p=11`, the determinantal divisors give the local Smith valuations:

`0,1,2,3,4,5,6,7,8,9,10`.

In particular `v_pi(det F_11)=55`, and

`F_11 mod pi = J_11`, where `J_11` is the all-ones rank-one matrix over `F_11`.

**Executable certificates.** `valuation_gate.py` represents minors as integer polynomials modulo `Phi_p(x)` and computes exact cyclotomic norms via a fraction-free Bareiss determinant. Since `p` is totally ramified, `v_p(Norm(D))=v_pi(D)`. Every `251` minor of `F_5` and all `3431` minors of `F_7` are exhausted, plus `31` independently selected/minimal-case `F_11` certificates. An independent verifier uses symbolic cyclotomic **resultants**, not the primary multiplication-matrix code.

## 3. A two-seed hypergraph bound for each v33 layer

For each row of a supported matrix define the hyperedge `T_r={j : M[r,j]!=0}`. Fix a seed set of source coordinates. In a homogeneous equation `M x=0`, whenever a row has exactly one as-yet-unknown source coordinate and its coefficient is nonzero, that coordinate is uniquely determined by already-known values. Continue until no such rows remain.

**Lemma 3.1 (zero-forcing nullity).** If `t` source coordinates seed a full recovery of all `N` coordinates by this rule, then `dim ker M<=t`, equivalently `rank M>=N-t`, over **any field** and for **arbitrary nonzero entries on the prescribed support**.

**Proof.** Restriction of `ker M` to the seed coordinates is injective: two kernel vectors agreeing on the seeds must agree on each subsequently recovered coordinate. QED.

Each of the original three v33 layers has a two-element seed that recovers all nine remaining coordinates. The exact seeds are:

| Layer | Initial source coordinates | Forced recovery order |
|---|---|---|
| A | `(0,1)` | `4,7,2,10,9,3,6,8,5` |
| B | `(1,2)` | `10,9,3,5,7,6,8,4,0` |
| C | `(2,6)` | `9,7,8,0,3,10,5,4,1` |

The executable certificate stores the *specific equation row* used at every recovery step. Hence **each fully nonzero weighted layer has rank at least 9**, irrespective of values or coefficient field. For extra assurance, the three unweighted incidence matrices are actually invertible modulo 11, with determinants `2,3,3` respectively. This last full-rank fact is for the **all-ones residue choice**, not arbitrary nonzero residue choices.

## 4. Deleting edges and forcing numbers

A weight divisible by `pi` becomes a zero entry after reduction. For a support pattern with selected edges deleted, define `tau` as the smallest seed count needed to force all coordinates. By Lemma 3.1, **every** matrix over the residue field with nonzero coefficients on that remaining support has nullity at most `tau`.

We exhaustively enumerated **every** deletion set of sizes `z=0,...,5` **separately in each layer**. The computed maximum `tau` is:

| Deleted weights `z` in one layer | Layer A: max tau | Layer B: max tau | Layer C: max tau |
|---:|---:|---:|---:|
| 0 | 2 | 2 | 2 |
| 1 | 3 | 3 | 3 |
| 2 | 3 | 3 | 3 |
| 3 | 3 | 3 | 3 |
| 4 | 3 | 3 | 3 |
| 5 | 3 | 4 | 4 |

Number of deletion supports checked in each layer:

`sum_(z=0)^5 C(33,z) = 284274`.

Across three layers this is **852,822** separately enumerated support patterns. For each pattern, the minimum forcing seed was found by an exhaustive search through seed combinations, not a random heuristic. Complete histograms by seed cardinality and one concrete mask witness for every class are in `forcing_results.json`.

**Lemma 4.1 (one deletion adds at most one seed).** Deleting one nonzero edge from a row support raises `tau` by at most one.

**Proof.** Let `S` be a forcing seed before the deletion and let the removed edge be at source coordinate `j`. Begin the altered propagation with `S union {j}`. Replay the original forcing order. If a step recovered `j`, skip it because `j` is already known. Every other step still has a nonzero coefficient on the variable it recovers; any missing deleted term concerned only the already-known variable `j`. The recovery remains valid. QED.

It follows that with `6` deletions in any one layer, `tau<=5` (because the maximum at `5` is at most `4`).

## 5. Main new project-specific seven-edge obstruction

**Theorem 5.1 — π-integral Fourier weights need at least 7 nonunit edges on the fixed v33 topology.** Suppose `A,B,C` have **exactly the fixed v33 99 allowed edge positions**, with arbitrary coefficients in `O`; zeros are allowed. If

`C B A = F_11`

then at least **seven** of the 99 coefficients must be nonunits of `O` (equivalently, divisible by `pi`). The same necessary condition holds if the equality is allowed to differ by invertible unit-valued input/output diagonal gauges and permutations.

**Proof.** Let `z_A,z_B,z_C` count nonunit weights in each layer and `tau_A,tau_B,tau_C` be the forcing numbers of their surviving residue supports. Lemma 3.1 gives

`rank( A mod pi ) >= 11-tau_A`, and similarly for B,C.

By Sylvester rank subadditivity for a product of three `11 x 11` matrices,

`rank( (C B A) mod pi ) >= 11 - (tau_A+tau_B+tau_C)`.

Suppose `z_A+z_B+z_C<=6`. We prove `tau_A+tau_B+tau_C<=9` by cases:

1. **All `z_i<=4`:** every `tau_i<=3`, so the sum is at most `9`.
2. **One `z_i=5`:** the other two have at most one deletion total. Their `tau` values are bounded by `3` and `2`, while the five-deletion layer has `tau<=4`. The sum is at most `9`.
3. **One `z_i=6`:** the other two have zero deletions and `tau=2` each. Lemma 4.1 bounds `tau<=5` for the six-deletion layer. The sum is at most `9`.

Thus `(CBA) mod pi` has rank at least `11-9=2`. Yet the prime Fourier matrix reduces to the rank-one all-ones matrix. Contradiction. Therefore total nonunit coefficients **must be at least seven**. QED.

This applies to arbitrary **π-integral** coefficients, *not just positive weights, roots of unity, bounded amplitudes, or real scalars.* The precise condition is arithmetic, not Euclidean: nonzero complex numbers need not even admit a valuation unless an arithmetic coefficient field/model has been specified.

**Special case — roots of unity.** If every edge is a power of `zeta_11`, every edge reduces to `1 mod pi`, so all weights are units; each layer reduces to its flat incidence matrix of determinant `2,3,3 mod 11`. Their product is invertible, whereas `F_11` reduces to rank one. This is a second, independent, support-specific proof excluding the phase-only path considered in v32. The seven-edge gate also covers many weights beyond roots of unity.

## 6. Other local diagnostics and a useful caution

* The original three row-support hypergraphs have pairs of rows meeting in **exactly one** source coordinate, with counts `27,23,25` by layer. Therefore no individual layer can be unitary (or made unitary by invertible diagonal row/column scalings) while all prescribed weights remain nonzero. Indeed such a pair's row inner product consists of exactly one nonzero term.
* Exactly **22** input-output entries of the whole three-layer circuit have a single route; the others have 2–5 routes. The 22 corresponding edge-exponent vectors have rank `22` over the rationals, so they alone impose **no multiplicative toric identity** eliminating Fourier. This is a checked negative result for that shortcut, not a Fourier feasibility certificate.
* A scoped 42-coordinate Jacobian dependency was observed at several finite-field weight assignments, but **no symbolic polynomial defining it** or Fourier substitution certificate was obtained. It is deliberately not presented as a new impossibility theorem.
* At all growing lengths, a fixed three-layer degree-3 circuit cannot be dense once `N>27`, because an input-output path has only `3^3` possible branches. Our fixed `N=11` candidate is a finite probe, not an asymptotically scalable FFT family.

## 7. Correctness and reproducibility

* **10/10** main automated test groups passed.
* **852,822** support-deletion patterns exhaustively reproduced by the main implementation.
* Independent **set-based** implementation checked all `18,054` masks of deletion size `0..3`, plus `10,800` deterministic size `4/5` masks, and independently verified rank of the flat matrices. It does not import the main forcing implementation.
* All `3,682` Fourier minors at primes `5` and `7` verified via exact cyclotomic integer norms; **31** additional prime-`11` certificates checked.
* Independent exact `resultant` checks at prime orders `5,7,11` agree with the claimed valuations.
* Predecessor v33 SHA-256 and ZIP CRC, full v34 SHA-256 manifest and clean-extract rerun are checked.

## 8. Interpret carefully; next exact gate

**What is established:** on the exact 99-edge support from v33, a Fourier factorization over cyclotomic-integral coefficients requires at least seven nonunit residues at the ramified prime. This is stronger than the v32 positive phase-path counting model and is independent of whether individual paths interfere constructively or destructively.

**What is *not* established:** impossibility with arbitrary algebraic coefficients having poles at `pi`, impossibility with arbitrary complex weights, the existence of the missing nonlinear 100-coordinate Fourier invariant, and any new `o(N log N)` full-output exact FFT.

**Next target:** enumerate the exceptional residue support patterns beginning with seven nonunit edges; determine whether `(CBA) mod pi` can equal the all-ones rank-one matrix. If some support admits exact residue compatibility, attempt Hensel-style lifting through `pi^2,pi^3,...` while charging every coefficient preparation and multiplication. This is a testable mathematical decision procedure for the arithmetic subclass, **not** a proposed shortcut for arbitrary complex FFTs.

**Prior art:** the prime-Fourier minor valuation proof is classical Chebotarev/Stevenhagen–Lenstra; the kernel forcing method is related to zero forcing/minimum rank theory; Sylvester rank is classical. No literature-wide novelty/priority assertion is made for the specific seven-edge arithmetic certificate.
