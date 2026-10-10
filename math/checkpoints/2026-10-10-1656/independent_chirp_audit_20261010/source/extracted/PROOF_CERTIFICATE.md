# Hero #17, Phase 23 — proof certificate: Chirped q-Green Cayley-Graph Union

**Date:** 2026-10-10. **Scope:** exact prime-field arithmetic; odd `N>=3`; supplied primitive `2N`-th root `eta`; full positive-sign `N`-point DFT of **recognized, structured fresh raw inputs**. There is **no universal exact linear-time DFT claim**, general integer-multiplication claim, complex floating-point stability claim or originality certification.

## Model and definitions

Let `p>2N` be prime with `2N | (p-1)` and `eta in F_p` primitive of order `2N`. Define `omega=eta²` (order N), `q=eta⁸=omega⁴` (also order N because N is odd), and `Phi_t=prod_(r=1)^t (1-q^r)`, `Phi_0=1`. Every denominator is nonzero for `0<=t<N`. All field operations are charged, including arithmetic root-power preparation and inversions. Index operations, `gcd`, loops and comparison tables are included in `O(N)` word-operation bounds but are not included in the *numeric field-operation ledger*. Root-of-unity discovery and bit complexity are outside the model.

For a canonical chirp exponent `0<=s<N`, nonzero amplitude `gamma`, and **any** nonzero phase `mu in F_p`, consider

`x_t = gamma mu^t eta^(s*t²) / Phi_t`, `0<=t<N`.

The requested ordinary N-point DFT has positive sign: `X_j=sum_(t=0)^(N-1) x_t omega^(jt)`. Negative-sign Fourier outputs are recovered by output-index negation in O(N) word operations.

## Theorem 1 — exact blind recognition, unrestricted phase

For `t>=1`, the input obeys

`(1-q^t)x_t = mu eta^(s(2t-1)) x_(t-1)`.

If `x_0,x_1,x_2` are nonzero, define `r_1=(1-q)x_1/x_0` and `r_2=(1-q²)x_2/x_1`. Then `r_1=mu eta^s` and `r_2/r_1=omega^s`. Because `omega` has exact order N, this phase uniquely identifies canonical `s` in `[0,N)` (if it belongs to the eligible set). Finally `mu=r_1 eta^(-s)` and `gamma=x_0`.

The implementation constructs *only* a deterministic eligibility table of chirp residues `s` whose seed-cover cost is at most the configured `B`. It compares `r_2/r_1` with every table entry and verifies the adjacent recurrence for **all** `N-1` transitions. Thus every accepted nonzero raw input has the stated exact structure; adversarial matching prefixes cannot force a false positive. The all-zero input is handled separately. With constant `B`, candidate preparation and lookup are O(1), and complete raw verification is O(N). All candidates are known in advance (not input-supplied); no discrete-log oracle or probabilistic hashing is used.

## Theorem 2 — one three-point spectral equation

Define the finite polynomial `H_s(z)=sum_(t=0)^(N-1) h_t z^t`, where `h_t=eta^(s*t²)/Phi_t`. The coefficient identity

`(1-q^t)h_t=eta^(s(2t-1))h_(t-1)` for `t>=1`

gives the exact terminating q-difference equation

`H_s(z)-H_s(qz) = eta^s z H_s(omega^s z) - eta^(-s)h_(N-1) z^N`.

The endpoint coefficient simplifies because `omega^(sN)=1`. Substitute `z=mu omega^j`, multiply by `gamma`, and express the endpoint through `x_(N-1)=gamma mu^(N-1)h_(N-1)` to obtain **for all indices modulo N**

`X_(j+4) = X_j - r_1 omega^j X_(j+s) + B_0`, where `B_0=x_(N-1) r_1 omega^(-s)`.

There is no omitted FFT, derivative jet or unknown closure term. This equation is applied only to fully recognized inputs.

## Theorem 3 — Cayley-coset graph union

Let `d=ord_(Z_N)(s)=N/gcd(N,s)` and `H=<s> = {0,s,...,(d-1)s}` be the additive subgroup of Z_N. **Compute the d Fourier values X_h for h in H directly**, each using N terms. Because s belongs to H, for any known coset `C=H+4r`, both `X_j` and `X_(j+s)` are known for all `j in C`. The three-point equation therefore computes all `X_(j+4)` in the next coset `H+4(r+1)` at constant work per output.

Since N (and hence `gcd(N,s)`) is odd, `4` is invertible modulo the quotient group `Z_N/H`. Thus the cosets `H, H+4, ..., H+4(g-1)` are all distinct and cover Z_N. Processing the first `g-1` cosets computes every output exactly once after the d direct seeds.

**Fully charged bound:** `O(dN+N)` field operations, `O(N)` retained field elements and `O(N)` ordinary index/loop operations once primitive roots have been supplied. Root-table preparation takes `O(N)` field operations. This holds even if `s` itself grows proportionally to N. In particular, `s=N/d` for any fixed odd divisor d>=1 yields an exact O(N) accepted-input DFT using d seed values.

## Theorem 4 — bounded short-jump and wrapped-jump alternatives

For `s>=5`, the same equation can be solved forward:

`X_(j+s)=(X_j-X_(j+4)+B_0)/(r_1 omega^j)` for `0<=j<N-s`.

Compute the first s Fourier bins directly, then exactly N-s more bins in constant work each; cost `O(sN+N)`. If `s=N-t` and `t` is small, seed bins 0 through t+3 and for `t<=j<N-4` use

`X_(j+4)=X_j-r_1 omega^j X_(j-t)+B_0`;

cost `O((t+4)N+N)`. For `s=1,2,3`, four seeds suffice using the original three-point equation. The implemented planner selects the cheapest of the coset, forward and backward constructions, except the special `s=4` method below.

## Theorem 5 — the resonant one-pole case s=4

When `s=4`, the equation becomes

`(1+r_1 omega^j) X_(j+4)=X_j+B_0`.

Starting with a directly evaluated `X_0`, walk the unique N-cycle under `j -> j+4` (N odd). Because `r_1!=0` and omega has order N, at most **one** denominator `1+r_1 omega^j` can vanish. At a singular edge, evaluate the successor directly as a second seed. All other edges determine the successor by one field division. Batch inversion of all nonzero denominators uses a single field inverse and O(N) multiplications. Therefore this case requires at most two seeds and O(N) field operations, including the singular case. Correctness was checked against independent direct/NTT references, including explicit resonant parameters.

## Theorem 6 — bounded-Hankel-rank recognition really is escaped

Normalize against Phase 22's base kernel `h^(2)_t=eta^(2t²)/Phi_t`:

`b_t=x_t/h^(2)_t=gamma mu^t eta^(c t²)`, `c=s-2`.

For a leading r-by-r Hankel matrix `H_(i,j)=b_(i+j)`, `i,j=0,...,r-1`, the exact factorization is

`H_(i,j) = [gamma mu^i eta^(c i²)] * [omega^(c i)]^j * [mu^j eta^(c j²)]`.

The middle factor is Vandermonde with nodes `omega^(c i)`. These are pairwise distinct for `r<=N/gcd(N,c)`. Whenever `2r-1<=N` and this condition holds, the Hankel matrix has full rank r. If `gcd(N,s-2)=1`, choose `r=(N+1)/2` (N odd), proving **growing Hankel rank at least (N+1)/2**. Thus no fixed-order exponential-polynomial Prony/Jordan family of Phase 22 can represent such normalized inputs.

For `N=3^m` and `s=N/3`, `gcd(N,s-2)=1`, so the three-seed coset algorithm handles inputs with maximal leading Hankel rank. The same conclusion holds for `s=N-2` at any odd N because `gcd(N,N-4)=1`.

## Theorem 7 — deterministic low-seed eligibility table

Let B be the maximum supported seed budget. Every chirp `s` admitted by these planners belongs to one of:

- short-jump `s<=B` (up to a fixed four-seed allowance),
- wrapped-jump `N-s+4<=B`,
- small-order `ord_N(s)=d<=B`.

The final category implies `d | N` and `s=k(N/d)` for some `0<=k<d`. Enumerating all `d<=B` generates at most `sum_(d<=B)d=O(B²)` candidates, with duplicates removed. Thus an input-independent sparse phase table can be generated in `O(B² polylog N)` integer preprocessing after `O(N)` root powers, independently of N for fixed B. The online table scan is `O(B²)` comparisons; subsequent full raw recognition costs `O(N)`. For fixed B the fully accounted work is `O_B(N)` on accepted inputs, with `O(N+B²)` memory.

The planner rejects unsupported chirps; the demonstration's fallback is a radix-2/3 NTT, `O(NlogN)` on the smooth lengths in the audit, potentially quadratic for a large unfactored radix. That fallback is **not** a new all-length FFT bound.

## Prior work and novelty boundary

The q-hypergeometric/q-difference technique is classical, and the reduction from structured polynomial coefficients to spectral recurrence lies broadly within q-holonomic methods (e.g. Garoufalidis–Koutschan 2012; Bostan–Yurkevich 2022). The cyclic-coset propagation, blind sparse phase gate and explicit finite-size comparisons are a derived *project contribution*, but **literature priority has not been established**. This certificate proves only its stated family and field model. The general exact DFT `O(N)` problem remains open.
