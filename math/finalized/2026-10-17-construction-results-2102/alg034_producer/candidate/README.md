# ALG-034 exact structured theorem-scale producer

This is a fresh, deliberately restricted exact backend. It computes the same
ideal target U_negative(P_balanced_longer_first(x)) directly on canonical
quarter-axis sparse inputs with square-dyadic N and singleton blocks B_A=N.
It does not execute the old rounded serial recurrence or claim identical
rounding. Unsupported inputs are explicitly rejected.

The actual N=268435456 delta-input fixture produces every exact target value
through a four-entry period: y_j=2^-14. The accepted one-shot policy has
p=268436013. Its exact p-grid output is factored symbolically instead of
allocating 268-million-bit integers or a 268-million-entry array.

Files:

* `structured_producer.py`: fresh exact implementation, canonical input grammar,
  exact specialized all-length precision policy, immutable output and full
  original-context replay verifier.
* `PROOF.md`: complete restricted-family target/precision/input-binding/resource
  proof and exact distinction from the old general bounded backend.
* `checks.py`: fresh independent small-domain direct Fourier controls, real
  theorem-scale producer/replay execution, malformed-input and forgery tests.
* `CHECK_RESULTS.json`, `CHECK_LOG.txt`: actual successful test evidence.
* `EXAMPLE.json`: complete compact theorem-scale input, plan and output.
* `CONTRACT.json`: machine-readable interface and limits.
* `SAFE_MANIFEST.json`: payload hashes; not a signature or execution attestation.

Run the fresh controls with Python 3:

    python checks.py

No historical Python is imported or executed. The implementation uses only
dataclasses, hashlib and json. The companion adapter packet owns the
constant-source certified BUCKETS implementation, legal sparse theorem guards,
and actual full bucket output. Independent final review remains separate.
