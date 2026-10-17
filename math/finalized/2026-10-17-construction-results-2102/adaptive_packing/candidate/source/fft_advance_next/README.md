# FFT research continuation: exact conversion and CRT gains

Date: 18 October 2026 (Asia/Qyzylorda).

This checkpoint preserves the preceding six research directories and adds
`fft_advance_next`. Start with `RESEARCH_RESULT.md`.

## What advanced

* Complete reciprocal-conversion producer: on the largest matched
  3,307,456-bit pair, 24.119590503 s becomes 9.424338384 s. This is a
  2.559287x gain over the frozen instrumented Python producer.
* Exact reflected-pair CRT formula: after cancellation, every remaining
  pair divisor divides the index gap. The complete combined producer
  reaches 1.025610977 s versus 1.725640419 s at 826,864 bits.
* Complete alternatives and adverse results are retained, including the
  dyadic/Newton evaluators, whole-tree moment cancellation, fixed raw
  blocks, and a cyclic transform through a circle group.

Native Python multiplication is still substantially faster. No new
arbitrary-input FFT or multiplication exponent is established. Timings use
the explicit three-block research shapes from the prior comparison and
their stated larger extensions; the default API shapes differ.

## Complete entry points

From the extracted checkpoint root:

```python
import sys
sys.path.insert(0, 'fft_advance_next/dyadic_reduction')
from dyadic_conversion_direct import multiply_dyadic_conversion

value, report = multiply_dyadic_conversion(
    a, b, rank=None, block_bits=None,
    outer_backend='packed', centered=False, conversion='auto'
)
```

The default shape retains r=max(2,bit_length(input_bits)) and block_bits=4r².
The measured 206,716-bit case instead uses rank=128 and block_bits=68,906.
`auto` chooses conversion by fixed size/reuse thresholds; it never times
several methods and selects the winner.

For the separately tested paired reconstruction:

```python
sys.path.insert(0, 'fft_advance_next/newton_bridge')
from combined_direct import multiply_combined_dyadic

value, report = multiply_combined_dyadic(
    a, b, rank=None, block_bits=None,
    outer_backend='packed', centered=False, conversion='auto'
)
```

Pairing is not universally faster than conversion alone. Its unfavorable
206,716-bit comparison is retained beside its favorable 826,864-bit result.

## Main evidence

| Directory | Contents |
|---|---|
| `dyadic_reduction` | Paid truncated-reciprocal tree, three complete dyadic/Newton alternatives, proofs, exact checks, matched seven-size benchmark and native calibration |
| `newton_bridge` | Gap-divisor theorem, pair-native planner, shared reflected tree, combined complete producer, two matched comparisons and independent reciprocal audit |
| `crt_moment_fusion` | Two complete raw-polynomial CRT candidates, actual whole-product losses, moment hierarchy, exact range proof and reproducible controls |
| `residual_fusion` | Complete circle-group cyclic transform, precise remaining cost, restricted one-convolution classification and independent raw-CRT audit |

The previous six directories remain unchanged. The new archive is rebuilt
from their verified file contents because the previous local ZIP was
incomplete; `ARCHIVE_RECOVERY.md` records exactly what was checked.

## Reproduce

```bash
python3 fft_advance_next/verify_manifest.py
python3 fft_advance_next/run_checks.py
```

The replay runs the six new suites in an isolated temporary copy. It does
not replace the retained evidence. The old suites were already checked in
the preceding checkpoint; they are not unnecessarily repeated here.

Benchmarks deliberately take longer and write new timing evidence:

```bash
python3 fft_advance_next/dyadic_reduction/benchmark_dyadic_conversion.py
python3 fft_advance_next/newton_bridge/benchmark_combined_direct.py
```

Every complete timer includes each call's own preparation. Endpoint
verification by ordinary integer multiplication occurs after the producer
returns. Legitimate certificate/base-case products remain paid.
