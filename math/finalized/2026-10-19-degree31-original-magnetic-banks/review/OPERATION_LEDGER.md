# Independent-review operation ledger

This is a verification ledger. It does not assert optimal arithmetic counts or an FFT speedup.

## Executed independent mathematics

- Exact prime tests for 53 and 31; degree-31 polynomial Frobenius/gcd irreducibility, repeated in the literal and arithmetic checks.
- Independent reconstruction of all 63 recorded field-modulus tests. No extension-field inverse is used before irreducibility.
- Ordinary degree-31 schoolbook multiplication with 961 coefficient products before reduction; polynomial Euclid for inverses. Exact source-specific signed bound 1,173,536.
- 1,062 independent arithmetic differential pairs: 961 ordered basis pairs, 100 deterministic dense pairs, one all-52 pair. Two unsafe-16-bit corruption controls.
- Ten supplied large-exponent cases, six truncation/wrap controls, and seven-point evaluation-uniqueness checks for four polynomial powers.
- Literal seven-root multiplication, all sixteen guards, all 208 raw weights and amplitudes in both directions.
- 208 closed-adjugate branch inverses. Two original sparse matrix products for each branch, totaling 70,304 entry equalities.
- Sixteen complete bank matrices, 2,704 bank Weyl coefficient checks, all thirteen sectors and 169 final Fourier entries.
- Nine Frobenius node orbits; seven malformed-data controls plus sign/normalization/weight semantic controls.
- Independent replay of 34,534 PRNG draws and all ledger state/count bindings. Discovery gate/split prefix arithmetic was not independently rerun; the candidate's fresh prefix receipts are source-bound.

## Implementation and cold checks

- A separately authored driver freshly compiles the active candidate field implementation with GNU C++17, GMP, UBSan, and no sanitizer recovery. It checks 1,062 products, eleven powers including a 257-bit exponent, and one inverse against fresh Python arithmetic. Discovery main is not called.
- A new isolated directory containing only the reviewer checker and certificate reproduces the literal receipt byte for byte. Observed cold wall/CPU times: 11.90/11.88 seconds; peak RSS 13,056 KiB.
- Initial literal and arithmetic subprocesses together used about 13.52 CPU seconds, peak RSS 14,080 KiB. Fresh implementation compilation/run took 1.84 wall seconds and 1.83 child CPU seconds, with compiler peak RSS 157,088 KiB. Raw receipts retain exact observed values.
- One attempted /usr/bin/time wrapper failed because that executable is absent, before its intended checker started. The checks were then run normally using Python time/resource accounting.
- No software was installed, no network/external state was written, no historical accepted witness was rerun, and no additional agent was created.

## Physical-bank versus scalar work

The witness has sixteen legal physical banks. Preparing and applying it costs more than sixteen scalar operations. For a deliberately unoptimized literal implementation, retain 208 inverse matrices (35,152 extension-field entries) and 208 raw weights. Evaluating all dense branch matrix-vector products uses 35,152 multiplications and 32,448 additions. Weighting all branch outputs uses 2,704 multiplications; summing the 208 outputs uses 2,691 additions; applying the global 1/13 uses thirteen multiplications. Total: 37,869 multiplications and 35,139 additions, excluding preparation, input/output and storage overhead. No optimality or practical advantage is inferred.
