# All order extensions of signed magnetic bank synthesis

This packet contains two fully stated all-order theorems in the accepted additive bank grammar and a classical common-node feasibility formulation. It leaves all accepted small-order and order-eleven source files unchanged.

## Main findings

- UNIVERSAL_FIXED_BANK_THEOREM.md proves that exactly 2N−2 fixed legal parameter/sign configurations are necessary and sufficient for universal linear synthesis of Mat_N(k), for every odd N≥3 and every field k containing a primitive Nth root q with char(k)∤N. The explicit construction uses q-power nodes, β=1 and guard−1 throughout. It gives M_k(N;q)≤2N−2 but does not determine the Fourier minimum.
- EXACT_BORDER_RANK_SEPARATION.md proves R_N(S^−1)=N−1 and border R_N(S^−1)=1 over C, in the full legal four-orientation dictionary. This is a quantified effect of the nonclosed finite-node restriction, not a rank/border-rank theorem for a closed projective scroll.
- COMMON_NODE_CRITERION_AND_LITERATURE.md gives the exact simultaneous squarefree-annihilator criterion, including the legal zero-node stratum, and records the primary-source and significance boundaries.

The exact universal architecture count gives an intrinsic mathematical resource interpretation: fixed parameter configurations with programmable phase weights. A bank still includes N weighted inverse terms. Neither theorem establishes an FFT speedup, a physical hardware count, scalar-operation savings, numerical stability, or historical priority.

## Fresh author controls

fresh_architecture_control.py was created from scratch for this packet. It checks full row rank and all prescribed Weyl equations for every odd N from 3 through 41 over suitable prime fields: 12,340 equations total. At N=3,5,9,15 it additionally computes all 616 literal branch inverses, verifies both inverse products, reconstructs the raw phase-weighted sums, and checks 340 original target matrix entries. FRESH_CONTROL_RESULTS.json and fresh_control.log record PASS.

fresh_boundary_control.py is a separate freshly written standalone control. For N=3,5,7,9,11,15 it computes 560 literal branch inverses, verifies both inverse products, and checks the roots-of-unity exact construction plus two nonzero parameter values of the one-bank boundary curve. BOUNDARY_CONTROL_RESULTS.json and boundary_control.log record PASS.

The all-order proofs, not these finite-field tests, establish the theorems. No modular lifting or extrapolation is used. No supplied or predecessor research program was read, imported, executed, compiled or parsed. Only the new controls in this folder were executed. No external edits were made.

## Review status

The theorem notes retain their original author-status text. Independent review receipts, when issued, are separate records and must be consulted for the accepted scope and reviewed hashes. The universal construction has received an independent proof check of the field, supports, axes, raw weights and lower-bound quantifiers; its reviewer did not claim to have executed the author controls.
