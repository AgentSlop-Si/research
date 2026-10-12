# Engineering NTT baseline review

Review date: 12 October 2026. This is a static assessment of supplied implementation, saved tests and saved timing data. Exact sources are identified in [Source citations](SOURCE_CITATIONS.json).

The engineering archive is `FFT_Verified_Engine_2026-10-12.zip`, SHA-256 `97d2d4fcbf6772e6774a73cf684e20d500d0b55e97c5d6a2ace66ee0d5aa620a`. Its C++ and shell files and included ELF binaries were inspected only as inert bytes/text. No compilation, binary execution or test script invocation occurred.

### Reported tests

The saved log and test-loop source agree on 162 exact input vectors: 126 dyadic vectors and 36 Bluestein vectors at 12 non-dyadic lengths. The same seeded mt19937 generator is used; “independently generated vectors” must not be read as independent researcher replication. Direct quadratic comparison is performed for dyadic N≤128 and each Bluestein test length. For larger dyadic sizes through 4096 the code cross-checks schedules and inverse round trips. Separate heavy controls reach N=262144 and check all-ones, impulse, dense schedule agreement, inverse and a spectrum-sum identity. These are source-reported passing checks, not checks rerun here.

The supported exact domain is a conventional positive-exponent modular DFT over the fixed field of modulus 998244353. The Plan constructor accepts powers of two 2 through 2^23; the CLI separately handles length 1. The non-dyadic Bluestein domain requires N dividing 998244352 and a power-of-two padded length at least 2N−1 no larger than 2^23. This is not a uniform arbitrary-field or exact-complex algorithm.

### Saved timing and arithmetic

The underlying static review recomputed every saved timing ratio and verified the reported count columns directly from the formulas. The retained numerical checks are summarized in [Verification scope](VERIFICATION_SCOPE.json). At N=262144:

- In-house radix-2: 16,072.650 microseconds.
- In-house DIF radix-4: 6,788.874 microseconds.
- Saved warm ratio: 2.3674986455780442, consistent with rounded 2.37×.
- All four schedules: 4,718,592 additions/subtractions and 2,097,153 nonidentity modular products, totaling 6,815,745 field operations before plan/index work.

The source's count functions are separate analytic ledgers, not dynamic hardware counters. Their formulas match the visible schedule structure and the CSV at every saved N. The usual count is N log2 N additions and (N/2) log2 N−N+1 products. Equality of this field-operation ledger does not mean equality of machine instruction count, cache traffic, allocations or runtime.

The warm exact benchmark includes returned-vector materialization and excludes shared Plan construction. Its `cold_plan_us` combines root tables and mappings for all tested schedules, so it is not each algorithm's minimum independent cold setup. The claim that locality or generated instructions caused the difference is plausible but not established by profiling in these files. Preserve it as a proposed explanation, not a measured causal result. This review establishes consistency of saved observations, not reproducibility on this or another machine.

At all 11 saved complex sizes the custom fused radix-4 is slower than FFTW_ESTIMATE. At N=262144 they report 6,456.411 versus 3,858.694 microseconds, with relative RMS discrepancy 6.084e−16. These approximate negative-exponent complex-double comparisons differ from the exact modular domain. No universal optimized-NTT win, FFTW win, new asymptotic rate or exact-complex accuracy theorem follows.

### Relationship to Q32

Q32 has the different accepted positive normalized F60 p32 API, exact dyadic input/radius domain and matched certified comparator. The new generic NTT/FFTW demonstration neither implements that API nor certifies its compiler, caller, physical-resource or exact-build deployment obligations. The existing bounded Q32 comparator is unchanged. This package supplies a conventional implementation and benchmark baseline; its source-bound build/runtime reproduction and matched deployment/comparator qualification remain open.
