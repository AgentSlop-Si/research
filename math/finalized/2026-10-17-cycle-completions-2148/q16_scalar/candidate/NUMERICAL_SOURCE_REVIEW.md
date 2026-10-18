# Fresh Q16 numerical kernel candidate

Status: AUTHOR COMPONENT CHECKS PASS; independent review pending. This packet is a new implementation, not a rerun of the historical bounded reference. It does not alone close the production sparse-output binding or the complete four-support coefficient stream.

## Source authority and execution boundary

The recovered contract archive was fetched read-only at GitHub commit `e3f3fd2fde808e577989907f00740c16905dbeb1`, path `math/reviewed_rounds/2026-10-14-reviewed-0023/q16_outer_contract/Q16_Outer_Active_Coefficient_Contract_Recovered_Candidate_2026-10-13.zip`.
Its exact 86,658 bytes have SHA-256 `0c7f8c8c4eedf4a4f6e332e429c4a785c02c952ba1ffe4c87a51537b00f502bc`.
The archive is retained privately. This public packet includes the exact contract and proof as inert text; the original source/acceptance collection remains privately retained.

The current `production_scalar.py`, `test_scalar.py` and `launch.py` were newly authored for this task. Only these fresh files and Python standard-library dependencies were executed. Historical uploaded Python was not imported, compiled for execution or executed. No external write occurred. The full new numerical dependency requires independent source review; the old acceptance is not inherited merely because the recurrence agrees.

## Concrete API

- `Paid` provides a monotone binary-work/storage ledger. Header validation and every subsequent preparation call retain all previous charges.
- `Interval(lo,hi,bits)` is an immutable exact dyadic rectangle coordinate.
- `Scalar(bits,paid)` prepares fixed-term Machin pi; `sin_pi(p,q)` uses integer congruence reduction, exact zero/unit branches, a rational-angle midpoint and fixed-term point Taylor enclosure.
- `signed_power(interval,s,paid)` implements odd monotone signed endpoint powers and even absolute-endpoint ranges. Its integer exponentiation is square-and-multiply; the `2^(K*(s-1))` divisor is explicitly paid.
- `CoefficientEngine(N,M,D,paid)` validates the exact built-in integer header and computes fixed metadata. It performs no pi or square-root work until its first valid retained-incidence call. It rejects `t>=M` with `OUTER_DENSE_REQUIRED` before numerical preparation.
- `coefficient(ell,k)` validates exact integer indices, range, and the row-first retained stencil. It returns a frozen `CoefficientResult`, including the p-grid midpoint, both K-grid coordinate enclosures and the exact squared-radius certificate. Sparse-output identity and immutable run-header/support association are the companion wrapper's responsibility.

## Audited recurrence

The fresh source follows the accepted contract:

1. `J=(D+5)m+bit_length(s)+8`, `K=J+2*bit_length(J+1)+16`, `p=(D+3)m+3`.
2. Pi uses exactly `K+8` terms each of `atan(1/5)` and `atan(1/239)`, with outward term rounding and signed alternating next-term tails; Machin combination is `16a-4b`.
3. Sine folds by exact integers to `[0,1/2]`, multiplies the pi enclosure, selects a downward integer midpoint and records an enclosing angle radius. Taylor has `K+8` terms, independent lower/upper recurrence, a fixed factorial loop and the degree-2n remainder bound. Analytic clipping and width guards are explicit.
4. Square root performs exactly `K+2` bisections from `[0,2^(K+2)]` on `floor(M*2^(2K)/N)`. It verifies adjacent integer endpoints and returns the next K-grid unit interval.
5. Zero residue directly creates exact F and R limits. Otherwise all three kernel sine enclosures are evaluated, the denominator lower endpoint is checked positive, and all four normalized quotient corners are rounded outward.
6. Signed power, all-corner products, amplitude scaling and the two exact phase-argument formulas follow the contract. No absolute-power replacement is used.
7. Midpoint rounding uses floor/remainder nearest-even including negative ties. The final check is `Rr^2+Ri^2 <= 2^(2*(K-A))`. Failure raises `CertificateError`, explicitly a deterministic defect rather than random recovery failure.

The accompanying mathematical contract/proof establishes enclosure validity and the universal precision bound. The fresh numerical source must be checked independently for faithful implementation. Passing author tests is supplementary evidence.

## Structural loop and allocation review

The complete production module imports only `dataclasses`. Its loops are:

- `Paid.record`: operand/result tuple of constant length
- `Paid.power`: halving a nonnegative exponent
- `interval_product`: four corners, constant size
- `normalized_quotient`: two by two corners
- `_arctangent`: `K+8` terms, twice per preparation
- `sin_pi`: `K+7` recurrence steps and `2(K+8)` factorial steps, only for non-exact branches
- `sqrt_ratio`: `K+2` bisections

There is no loop with N or M iterations, no dense row/vector allocation, no phase table, and no sine cache. The only persistent numerical preparation is one pi enclosure and one square-root enclosure per engine. Per-call scratch consists of fixed-count intervals and scalar integers. The coefficient kernel does not retain all outputs. The test driver retains exactly three records, and the companion wrapper is responsible for streamed incidence traversal.

Repeated `prepare()` is paid with a call and reuse check but does not repeat pi/root computation. No method resets or subtracts ledger charges. Empty engine construction and a rejected dense call have positive paid header work and zero pi/root events.

## Author controls and exact process evidence

`RESULTS.json` retains all three selected records in the required order `(0,0)`, `(2^53,2^55+1)`, `(0,1710)`, exact rectangles/certificates and ledgers. The metadata are `D=5,m=57,N=2^55-1,M=2^57,s=285,J=587,K=623,p=459`.

- Actual production signed-power sentinel `[-1/2,-1/4]^285` returns exactly `(-2^338,-2^53)` on the K=623 grid. A positive absolute-power replacement fails. A newly authored even-only guard rejects 285; the historical helper is not executed.
- Minimum nonzero residue is exactly one and its denominator lower endpoint is strictly positive.
- All three exact squared-radius certificates pass. The tiny negative-ratio witness still rounds to zero; it is not promoted to an eta-violating final-output example.
- 945 signed-power endpoints agree exactly with separate Fraction calculations.
- 123 positive/negative nearest-even ties pass.
- 99 sine controls enclose exact rational values or exact algebraic squares across positive and negative periods.
- Root endpoints satisfy exact rational-square inequalities.
- Seven malformed headers and seven invalid incidence inputs reject; malformed headers retain paid prefix receipts and no pi setup.
- The exact certificate boundary passes; an oversized rectangle fails with `squared-radius certificate failed`.

The fresh test process exits zero, without stderr or timeout. `PROCESS_EXIT.json` preserves unchanged pre/post source hashes under caps of 45 CPU seconds (50 hard), 90 wall seconds, 512 MiB address space and 16 MiB output-file size. Observed CPU/wall/RSS are host measurements only, not complexity or FFT speed evidence.

## Remaining numerical acceptance requirement

A separate reviewer must author a rational coefficient oracle using a different pi identity and independent root/sine/error code, without consuming production Scalar output. It should compare exact guaranteed enclosures or certify the error directly. The existing bounded reference report is background evidence, not a new independent run of this source. Full sparse-output wrapper acceptance, incidence enumeration, full stream/scatter, every-tape estimates, paid accumulators and N outputs, scale-back, dense/all-length dispatch and independent amplification remain separate.
