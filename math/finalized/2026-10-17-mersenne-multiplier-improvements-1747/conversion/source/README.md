# Exact Mersenne conversion improvement

Read `REPORT.md` for the precise construction, proof, prior art and residual bottleneck.

This provides a fresh exact implementation of a modulo-power-of-two factorial-Toeplitz shift, a local Mersenne quotient/carry stream, binary/canonical/redundant/grouped positional conversion, and raw convolution readout. It does not prove multiplication below N log N.

Run the bounded controls with:

    python fresh_conversion.py

The program uses its own Karatsuba recursion for represented arithmetic; native multiplication/division in the test harness is only an independent oracle. No historical source is imported or executed. The saved run is `CONTROL_RESULTS.json` with console copy `RUN.log`.
