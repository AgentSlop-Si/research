# Portable Phase30 replay

Use Python with SymPy and a standard C++17 compiler. Copy this directory to a fresh work location before running, so the sealed payload stays unchanged. The authored scripts resolve paths relative to their own location. No master snapshot is required. Do not run the uploaded scripts under extracted/.

Run:

```
python prepare_and_check.py
python extra_checks.py
g++ -O3 -std=c++17 exhaustive_four.cpp -o independent_four
./independent_four four_N4_p998244353.txt ranks_N4_independent.bin failures_N4.txt
./independent_four four_N8_p998244353.txt ranks_N8_independent.bin failures_N8.txt
./independent_four four_N16_p998244353.txt ranks_N16_independent.bin failures_N16.txt
g++ -O3 -std=c++17 -DAUDIT_PRIME=2013265921 exhaustive_four.cpp -o independent_four_p2
./independent_four_p2 four_N8_p2013265921.txt ranks_N8_p2_independent.bin failures_N8_p2.txt
```

Expected mapping counts are 576, 112896 and 11289600 at N=4,8,16. Every rank is 20 and every failure file is empty. The N16 stream SHA-256 is f57c8b81adb0976bd5a3f5bf51d6701dcc897a6f7196d528f0fb3e23fcbc5e44. The largest enumeration can take several minutes.

The independent reviewer repeated Python reconstruction, all saved-minor and five-term checks, and the complete N16 enumeration from a fresh copied directory. All nine selected regenerated artifacts were byte-identical; see PORTABLE_REPLAY.json. Initial runs also completed N4 and both N8 enumerations; those results are in EXHAUSTIVE_RESULTS.json.

Check payload integrity with `sha256sum -c SEALED_MANIFEST.sha256` in this directory. The manifest excludes only itself, its JSON companion, transient __pycache__ files and the temporary replay-path marker. PHASE30_REVIEW.md contains the exact statement and limitations.
