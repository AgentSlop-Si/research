# Full static source review: self_test_checker.py

- Source: additions/1908/self_test_checker.py
- SHA-256: 60046883b98516276c28d6f043bbe3b455c9b66514e6f87e37cf73625215e73d
- Bytes: 2482; lines: 59
- Read interval: 1–59 (complete)
- Supplied source execution/import/compile/parse: none
- New exact-hash full-read coverage: yes

## Full-source scope
Read lines 1–59: exact integer determinant oracle, all shape/prime/kind loops, comparison/recording and CLI.

## Correctness and test scope
The Leibniz oracle promotes every matrix entry to Python int before multiplication, so determinant products cannot overflow int64. It includes inversion parity and the empty 0×0 determinant convention (the single empty permutation gives one). Exact modular rank is found by searching all minors from largest order down; this validates the elimination rank on small matrices without using another Gaussian-elimination implementation. Selected-row/pivot-column determinant values are checked in the same row order returned by the implementation; full-square nonsingular determinants additionally check original row order.

The loops comprise five primes, four rectangular/square shapes and four input kinds, totaling 80 cases. Duplicate rows, zero and rank-one cases exercise deficient ranks. The rank-one NumPy outer products are safe for these fixed primes <=65537. The oracle is exponential/factorial and deliberately restricted to small shapes; it does not directly validate every entry or computation of the large stored Jacobians.

## Guards and output behavior
All test assertions disappear under -O, allowing a misleading PASS result if that unsupported mode is used. Input sizes and primes are hard-coded valid values; no generic parser contract is offered. The output directory checks/ is not created here, and would be absent if this file alone were copied somewhere without the package or the primary checker being run first. In the preserved package it exists. Running this script in place overwrites checks/self_tests.json; no rerun was performed here. Bare import check_bitrev resolves to the adjacent exact dependency in the intended invocation; alternate Python path contents could change it.

## Evidence and disposition
Saved self_tests.json contains 80 records, coherent with the loop design, and the enclosing manifest binds this test source and check_bitrev.py SHA-256 7e61ae8680e03027c0c2eab49eeaf30bfd696cb8a1a8eaf51fc76794afb3f77f. No stored-result error was established. Accept finite historical eliminator cross-check evidence and full static source coverage; do not call this a new run or a general correctness proof.
