# Reproduction commands

Use Python 3 with `numpy`, `sympy` and a C++17 compiler. No network connection is required.

```bash
cd fft_green_phase38_joint_masks
python -m unittest -v tests_phase38
python charzero_n4.py

g++ -O3 -std=c++17 -Wall -Wextra exhaustive_permutations.cpp -o exact_checker
./exact_checker instances/phase38_instance_N32_p998244353.txt
./exact_checker instances/phase38_instance_N32_p2013265921.txt
./exact_checker instances/phase38_instance_N64_p998244353.txt

# At N=64 the p2 reduction has exactly one accidental common modular root.
# Its expected exit code is 1; compare the p1 witness in phase38_audit.json.
./exact_checker instances/phase38_instance_N64_p2013265921.txt || true

# Finite-field two-mask polynomial witness + planted valid Fourier control:
python phase38_joint_masks.py --max-n 128 --output recomputed_masks_audit.json

sha256sum -c SHA256SUMS.txt
```

Native output fields: `checked`, `nonzero_resultants`, `zero_resultants`, and a rolling modular checksum. Deterministic ordering and seeded cycle lists are saved.

For `N=128,256`, the archived 200,000-map audits were sampled (`./exact_checker instance.txt 0 200000`). They are not exhaustive.

**Complexity:** constructing the *proof target* `T=A^-1 F C^-1` by dense modular inversion is `O(N^3)` in the implementation; the exhaustive audit is `O(N^5)` at fixed degree. This is only certification and is not an FFT algorithm. Applying a supplied six-Green circuit remains `O(N)` online arithmetic, but the audited family cannot equal the DFT.
