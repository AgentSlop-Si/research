# Narrow-kernel Mersenne conversion

The report proves an exact common-denominator rewrite and limb-streamed convolution that replaces the prior same-scale product by smaller products. With the same explicit Karatsuba core, complete conversion costs O(N (L² log(L+1))^(log₂3−1)) in the stated very-wide regime, and is o(N log N), for example when L=O((log N)^(4/5)). The full multiplication and prime-selection gates remain open.

- Read `REPORT.md` for proofs, model, complete charges and limitations.
- Run `python fresh_controls.py` for fresh deterministic correctness controls.
- `kernel_stream.py` is the self-contained production stage; native arithmetic in the driver is an oracle only.
- This is a local candidate awaiting independent review. No external write was performed.
