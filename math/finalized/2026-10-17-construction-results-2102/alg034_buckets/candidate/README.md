# ALG-034 theorem-parameter constant-source integration candidate

Fresh restricted producer/adapter/BUCKETS backend. Read `PROOF.md` before using.

Run `python checks.py` (about one minute in the observed environment). No network,
external writes, floating arithmetic, N-vector, time-window, or FFT is used.

`ScaleAdapter.execute(raw,state)` calls the actual pinned structured producer and
returns 131072 exact dyadic bucket values at M=2^28, beta=5/56, k=32, P=464.
Input is the producer's canonical sparse representation of 2^-F delta_0 with
singleton ALG-034 blocks. `ScaleAdapter.verify` re-executes the producer and
compares the complete output/context against paid reusable numerical state.

All known theorem window/BUCKETS guards hold, and max complex bucket error is
<=2^-464 from the original ideal operator. This is a new restricted algebraic
backend, not bit-equivalent legacy rounded serial/FFT execution. It does not
execute or close full sparse recovery or separate outer-transfer guards.

`CHECK_RESULTS.json` contains actual tests, pins and conservative resource
receipts. `NUMERICAL_RESULTS.json` is the first standalone numerical run.
No publication or other external mutation occurred.
