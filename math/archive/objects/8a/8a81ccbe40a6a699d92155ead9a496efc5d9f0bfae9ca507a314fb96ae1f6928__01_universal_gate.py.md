# Source 01: universal_gate.py

SHA-256: b6707b37b343be238aa52dce797e5386faff3b8008666cb5329284090207ff8a

Representative: additions/1717/extracted/fft_triple_intersection_gate_2026-10-09/universal_gate.py

Read: all 159 lines / 5894 bytes. Full inert inspection; no import, execution, compilation or syntax parse.

## Flow and complete-read coverage

Lines 1–25 state the structural necessity and import the generator/rank/dependency chain. Lines 27–73 implement modular determinant, the four projection blocks, cofactor normal, 11×9 gate, and independent row selection. Lines 75–110 enumerate the guarded finite-field chart and store three nonzero-minor witnesses. Lines 112–155 implement invertible separated positive controls; lines 157–159 run and write results.

## Mathematical scope

The signed cofactor vector annihilates Y4; stacking Y1−Y2 and Y1−Y5 encodes a shared projected upper direction. Necessity needs nonzero selected C column triples, ensured by intended invertible C. The original wording lacks that hypothesis; the existing independent counterexample and repair are preserved. Zero fourth-output multipliers are handled by the all-cofactors-zero proof branch.

## Input guards and acceptance

Public helper inputs assume a prime modulus, rectangular dimensions and 8-vectors. Enumeration explicitly skips h0=0, Δ=0, t=0 and failed Q residuals, so it does not cover exceptional charts. Positive controls require C and D invertible and exercise zero selected upper multipliers, without a retry cap.

## Cost

Fixed-size linear algebra; exhaustive h enumeration Θ(p⁴) and repeated filtered gate ranks. Exact field arithmetic is not asymptotic FFT improvement.

## Tests, records, dependencies and actual impact

Stored 4,596 prior chart survivors and 3,266 new rejections agree with independent recorded rank counts. The 1,330 admissions are not factorizations. Dependency identities identified, generator and runtime bootstrap closure not complete.

Finding references: F01 F07.
