# FFT moving-partition and twisted-shuffle research checkpoint

**October 10, 2026** — All-length proofs and exact reproducible obstructions for quasiseparable Fourier-stage networks. This archive continues the prior `fft_four_stage_central_bit_no_go_2026-10-10.zip` checkpoint, stored as `prior_checkpoint_full.zip`.

## Main verified findings

1. A **moving-partition rank theorem** works for arbitrary changing interstage permutations, including those mixing the previously blocked middle-bit groups.
2. A constant-width binary-local GF(2) mixing program of rank-one global scans still needs **Omega(log N)** stages. With locality parameter 1, depth >= log2(N)-1.
3. Repeated **rotated bit reversal** (`rotl(bitrev(x))`) needs **Omega(sqrt N)** stages: exactly `2^(m-1)+1` or `2^m` as necessary stage-count bounds for even/odd k=log2 N.
4. **13 different finite four-stage layouts** at N=64,128,256 are excluded by exact Fourier rank versus moving-boundary capacity, certified modulo 12,289 and 65,537 and therefore over C.
5. A deliberately densely mixed four-stage candidate passes the searched interval/parity/mincut rank tests at N=256. This is a **negative result for the tested obstruction method**, *not* a working FFT algorithm.

## Run

```
python test_gate.py
python test_twisted.py
python verify_certificates.py
```

Optional explorations:

```
python interval_sweep.py
python moving_partition.py
python mixing_survivor.py
python bisection_probe.py
```

Requirements: Python 3.10+ and NumPy; optional NetworkX and SciPy for the experimental graph optimizations. Some exploratory scripts can take longer than the three verification suites.

## Contents

- `PROOF_CERTIFICATE.md` — complete mathematical arguments with explicit scope.
- `RESEARCH.md` — experimental results, technical interpretation, limitations.
- `EXACT_CERTIFICATES.json` — 13 exact no-go certificates and deterministic shuffle arrays.
- `moving_partition.py` — arbitrary-shuffle moving-boundary theorem checker.
- `verify_certificates.py` — independently reconstruct and check certificate claims.
- `test_gate.py`, `test_twisted.py` — regression tests and structural witnesses.
- `build_certificates.py` — regenerate determinants.
- `interval_sweep.py` — all consecutive input subsets.
- `bisection_probe.py` — optional balanced layout-interaction-graph heuristic.
- `mixing_survivor.py` — deliberately rank-feasible shuffled-network candidate.
- `prior_checkpoint_full.zip` — complete preceding research checkpoint.
- `SESSION_HANDOFF.md` — continuity notes for a future chat.

**No new O(N) or sub-NlogN FFT construction is claimed.**

Additional optional verification with integer network maximum flow:

```
python test_network_audit.py
```

This rechecks six exact moving-cut capacities and 24 full-capacity control cuts at N=64/128/256. It requires NetworkX and SciPy.
