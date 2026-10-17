# Independent review: Mersenne Taylor-to-block packing

17 October 2026. Independent exact-arithmetic review; no external changes.

## Decision

**Accept the corrected, narrowly stated representation lemma and elementary cost invoice.** The worst-case actual materialized block volume is Theta(mK+K²/s), all block maxima are attained simultaneously by legal input chunks a_i=p, and the degree-safe closed linear packed-state Horner obstruction is valid. The matrix specialization is Theta(N+dM³), and separately materializing its M² pairwise products costs Theta(MN+dM⁴) actual output bits in the worst case.

The signed witness is not a collision between legal inputs. Legal packed states are injective. A fixed linear transition is nonetheless impossible because the legal shifted unit inputs span the relevant polynomial space. The corrected report makes this distinction.

One concrete scratch-width error was found and corrected: a separately stored shift inside multiplication by p can require 2N+1 bits even when the completed product fits 2N bits. This changes no asymptotic estimate. No unresolved mathematical objection to the corrected claims was found.

This acceptance does **not** establish a fast fused conversion algorithm, a better integer-multiplication runtime, an FFT/DFT improvement, historical novelty, an all-size prime-selection argument, or a global impossibility result.

Reviewed candidate: `../mersenne_next_gate_20261017_1153/REPORT.md`

SHA-256 of reviewed corrected version:

`eec1368f1f8ef61200b0310dcb616a173c2b49e9a3d50ea6c292c07a280ecdb5`

## 1. Exact domain and dimensions

The reviewed theorem takes integers m>=2, K>=1, s>=1 with s dividing K. Set p=2^m-1, B=K/s, N=mK. There are K binary chunks, indexed 0 through K-1, and K shifted coefficients:

    A(x) = sum_i a_i x^i,       0 <= a_i <= p,
    C(z) = A(1+z) = sum_j c_j z^j,
    c_j = sum_(i=j)^(K-1) binom(i,j) a_i.

Packing is the integer-linear map E_s from K coefficients to B integers:

    U_r = sum_(t=0)^(s-1) c_(rs+t) p^t.

Its exact reconstruction is X=sum_r U_r p^(rs)=A(p+1). The U_r are redundant positive integers, not canonical base-p^s digits. Neither truncation to ms bits nor binary concatenation is permitted.

The maximum-input statement uses a padded capacity N=mK. With a shorter final binary chunk imposed by an unpadded n-bit promise, a_i=p may be unavailable for that leading chunk; one must not silently claim the exact same maximizing input. The candidate explicitly states padding and charges N, so this issue is handled.

Primality of p is not used. The excluded value m=1 gives radix p=1, which is not a positional numeral base. Some algebraic identities still hold there, but this review does not enlarge the candidate's domain.

## 2. Independent volume proof

Every U_r is a nonnegative integer-linear expression in the a_i. Hence the vector a_i=p simultaneously maximizes every U_r and the sum of its ordinary magnitude bit lengths. The hockey-stick identity gives

    c_j* = p binom(K,j+1),
    U_r* = p sum_(t=0)^(s-1) binom(K,rs+t+1) p^t.

For the upper bound, all c_j <= p 2^K. Thus

    U_r < (3/2) 2^K p^s < 2^(ms+K+1).

Writing ell(0)=0 and ell(u)=floor(log2 u)+1 for u>0 yields

    sum_r ell(U_r) <= (K/s)(ms+K+1)
                  <= mK + 2K²/s.

At the all-maximum input, the highest term of every block is at least p^s. Therefore

    sum_r ell(U_r*) >= K log2 p >= mK/2.

For an independent lower-bound route, use

    binom(K,j) >= 2^min(j,K-j),     0 <= j <= K.

For j<=K/2 this follows from binom(K,j)>=binom(2j,j)>=2^j; symmetry gives the rest. Each U_r* is at least every c_j* in its block. Averaging the corresponding logarithmic lower bounds within each block gives

    sum_r ell(U_r*) >= (1/s) sum_(j=1)^K log2 binom(K,j)
                    >= floor(K²/4)/s.

Combining the two lower bounds proves Theta(mK+K²/s) uniformly, including small K by a separate trivial check. This is an independent proof of the same order; it does not depend on the candidate's central-binomial interval argument. The candidate's explicit constants, 3/64 below and 1,2 above, were also checked and are valid.

All-max input is a single legal integer X=2^(mK)-1. Thus the result concerns realizable actual payload volume, rather than incompatible per-object maxima. Length metadata can be encoded within a constant-factor overhead; zero markers add at most B bits. The lower bound applies to separately written/transferred ordinary binary integers, not to compressed or implicit representations.

### Endpoints

- K=1, s=1: U_0=a_0, with exact maximum bit length m.
- s=1: the output is all Taylor coefficients; volume Theta(N+K²).
- s=K: U_0=X; exact maximum bit length N, consistent with Theta(N+K).
- Zero input has zero magnitude payload under ell(0)=0, so the theorem is worst-case, not an all-input lower bound.

For K=dM² and s=dM, B=M and K²/s=dM³, giving Theta(N+dM³). For s=d the redundant intermediate blocks have volume Theta(N+dM⁴). For s=1 the full coefficient array has volume Theta(N+d²M⁴). These are three distinct interfaces.

## 3. Linear obstruction and legal-input relevance

The candidate quantifies over polynomials F of degree at most K-2 so that multiplication by z+1 remains within the K-dimensional coefficient space. Under 1<s<K and s|K, the witness

    F(z)=z^(s-1)-p z^(s-2)

has degree at most K-2. Its two nonzero coefficients are within the first packed block:

    E_s(F)=0,
    E_s((z+1)F)=(-p^s,1,0,...,0) != 0.

Consequently no linear L can satisfy E_s((z+1)F)=L E_s(F) throughout that degree-safe space. The dimensions and block-boundary crossing are correct. The s|K restriction matters for the stated degree conclusion: if one informally removes divisibility and permits s=K-1, this same witness has degree K-2 and still works, but a proof must restate its domain rather than assume s<=K/2.

The witness itself is signed and is not a difference between two legal shifted inputs. Indeed, inverse shifting gives A(x)=F(x-1), whose constant coefficient has magnitude p+1, exceeding the allowed difference range [-p,p]. The report does not make the invalid claim that this produces a legal collision.

The necessary extension argument is sound: each (1+z)^i, 0<=i<=K-2, comes from a legal unit binary-chunk input. These form a triangular basis of the degree-at-most-K-2 polynomial space. If one fixed linear map works on every legal such state, it works on the whole span and is contradicted by the signed witness. Adding the next digit as a separately known affine term does not remove the obstruction; set that digit to zero.

By contrast, E_s is injective on the finite legal shifted-input set. If two legal packed tuples were equal, their recombinations at p would agree, so the underlying base-2^m integers would agree. Uniqueness of legal base-2^m digits then forces all a_i equal. Thus a nonlinear decoder/update exists in principle, and this proof says nothing about its efficient implementation. Additional boundary coefficients, additional state, or original-input access also change the interface.

At s=1, E_s retains every coefficient and the linear recurrence is available. At s=K, scalar evaluation at p intertwines degree-safe multiplication by z+1 with multiplication by p+1. The degree-safe qualification is important: multiplying a degree K-1 polynomial and then splitting into an added block is a different map.

## 4. Full elementary ledger

The reviewed invoice consistently keeps ordinary bit lengths paid:

1. Reading both binary operands costs O(N).
2. Coefficient-array Horner shifting performs O(K²) additions on at most m+K payload bits. The deliberately full-width implementation costs Theta(K²(m+K)) and stores O(K(m+K)) bits. This is an implementation-specific bound, not a Taylor-shift lower bound.
3. Direct coefficient-to-final-block Horner packing makes K shift/subtract/add steps with H=ms+K+1 as a safe completed-value bound and H+1 scratch bits. It costs O(KH). It avoids the intervening p^d blocks but still materializes all K Taylor coefficients.
4. The outer-product route executes M² independent products of operands at most H bits. Their diagonal sums need at most 2H+ceil(log2 M)+1 bits. Direct accumulation costs O(M²(H+log M)).
5. Binary reconstruction makes at most 2M-2 groups of s multiplications by p, plus coefficient additions. Nonnegativity bounds every completed partial reconstruction by the final XY<2^(2N). O(KN+M(H+log M)+N) is therefore a valid upper cost, with 2N+1 bits for materialized shift temporaries.
6. Input padding, parameter setup, and any prime selection remain explicit obligations. If H>=N, the child recurrence is not shrinking and needs a paid fallback.

The resulting direct invoice

    T(N) <= M² T(H)
      + O(K²(m+K) + KH + M²(H+log M) + KN + N)

is an honest upper account for the stated finite construction. It is not a speedup theorem. In particular, K²m=NK=N²/m remains present in elementary preparation.

### Actual eager product volume

For positive integers u,v,

    ell(u)+ell(v)-1 <= ell(uv) <= ell(u)+ell(v).

At the pair of simultaneous maximum inputs, if W=sum_i ell(U_i), summing over all M² products gives

    2MW-M² <= sum_(i,j) ell(U_i U_j) <= 2MW.

Here every block has at least two bits, so this is Theta(MW). Substitution yields Theta(MN+dM⁴). This is a separate materialization lower bound. It does not force an executor to retain every product simultaneously or rule out a fused diagonal-only algorithm.

### Optional classical coefficient kernel

The candidate's optional 2M-1-product route was checked algebraically as an upper-bound ledger, not as a novelty claim. Evaluations at 0,...,r-1 fit the stated J-bit operands. Taking common denominator D=(r-1)! and integer-scaled Lagrange polynomials gives coefficient bounds below the stated kappa-bit capacity: a product's coefficient 1-norm is at most r!, and the additional binomial factor is at most 2^(r-1). The stated W-bit signed-accumulator capacity is conservative. Schoolbook evaluation, signed decoder multiplication, exact division, and table preparation fit the displayed O(M² J ell+M² W kappa+M³ kappa²) upper account. This does not independently re-prove an optimal-rank theorem or import a new fast bit-complexity primitive.

## 5. Concrete defect found and corrected

The initial draft said 2N magnitude bits suffice throughout reconstruction without separately charging the shift temporary. Counterexample:

    m=2, p=3, d=1, M=2, K=4, s=2, N=8,
    X=Y=255,
    U=V=(66,21),
    diagonal sums S=(4356,2772,441),
    XY=65025, which has 16 bits.

The last repeated-p step starts at v=20223. The materialized shift v<<2 is 80892 and needs 17 bits, before subtraction produces 60669 and the final addition yields 65025. The author changed the report to allow 2N+1 scratch bits and similarly made the block-packing scratch allowance explicit. For p>=3, (p+1)/p<=4/3, proving one guard bit suffices. The reviewed hash includes this correction.

## 6. Fresh controls and verification limits

`independent_checks.py` is newly authored standard-library-only code. It does not import or execute candidate or historical programs. It computes the binomial formula and a separate coefficient-array Horner implementation, compares them, checks reconstruction independently, exhausts small legal domains, and performs seeded larger tests.

Completed results:

- 43,932 individual representation/maxima/width checks
- 41,532 exhaustive legal-state injectivity checks
- 835 degree-safe signed witness and inverse-shift checks
- 60 actual eager pair-product-volume checks
- 240 full matrix-product and reconstruction checks

Domains include m=2,3,4,5,7,13,31; composite Mersenne p=15; zero, maximum, exhaustive small, and seeded random inputs; s=1 and s=K; and larger K through 147 in product tests. The explicit shift-temporary counterexample is retained in `INDEPENDENT_RESULTS.json`.

These use exact Python arithmetic as an oracle. They are not performance benchmarks, bit/tape timing evidence, or a proof assistant. The universal statements rely on the proofs above.

The candidate report and predecessor text were read for claim definitions and ledger comparison. No external source or repository was changed, and historical code was not run. Historical priority and the candidate's external documentation claims were not independently searched; they remain outside this mathematical acceptance.

## 7. Remaining open work

A useful next step would be a fully specified fused producer of just the final redundant blocks, with every intermediate representation and any multiplication children charged. A faster producer alone would still leave the product, overlap resolution, readout, parameter choices, and full recurrence to prove. The current output-volume theorem only supplies a necessary materialization budget and a precise destination interface.

No canonical research status, score, owner, or broader target should be changed merely because this scoped lemma is accepted.
