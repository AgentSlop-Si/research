# Fresh exact controls for the zero-node route

10 October 2026. Supplementary bounded arithmetic checks. These do not prove the uniform theorem and are not characteristic-zero lifting recipes. The standalone derivation supplies the characteristic-zero proof.

The new program `fresh_zero_node_controls.py` imports only Python standard-library modules. It does not execute or import any predecessor program. It constructs the enlarged envelope directly and constructs the actual recurrence rows independently by q-Pascal recursion. Prime search is bounded by p=kN+1, 1≤k≤200; exact order of q is checked. Searches for zero-node and legal witnesses are each bounded to 100 deterministic parameter assignments.

For every pair the controls verify:

- Enlarged-envelope rank 4d−7 and a nonzero defining pivot minor
- Every basis vector of its annihilator satisfies every actual whole-left recurrence
- Exact modular kernel gcd t−1, and zero-constant subkernel gcd t(t−1)
- Independence of delta_0, delta_1, delta_m modulo the envelope
- A monic zero-constant g_0=t(t−1)f with reciprocal-coprime f and full quotient-axis rank
- A monic legal g with nonzero constant, squarefree gcd test, and full quotient-axis rank
- Explicit axis pivot columns and nonzero corresponding pivot-minor determinant residues

| N | d | p | q | dim U | zero axis rank | legal axis rank |
|---:|---:|---:|---:|---:|---:|---:|
| 23 | 4 | 47 | 4 | 11 | 23 | 23 |
| 31 | 5 | 311 | 91 | 14 | 31 | 31 |
| 39 | 6 | 79 | 4 | 17 | 39 | 39 |
| 47 | 7 | 283 | 64 | 20 | 47 | 47 |
| 55 | 8 | 331 | 67 | 23 | 55 | 55 |
| 63 | 9 | 127 | 9 | 26 | 63 | 63 |
| 71 | 10 | 569 | 256 | 29 | 71 | 71 |
| 79 | 11 | 317 | 16 | 32 | 79 | 79 |
| 87 | 12 | 349 | 16 | 35 | 87 | 87 |
| 95 | 13 | 191 | 4 | 38 | 95 | 95 |
| 103 | 14 | 619 | 64 | 41 | 103 | 103 |
| 111 | 15 | 223 | 9 | 44 | 111 | 111 |

All 12 bounded controls passed. Matrices, nullspace bases, affine slices, coefficient witnesses, recurrence labels, and pivot data are recorded in `FRESH_ZERO_NODE_CONTROLS.json`. Finite-field squarefreeness or rank is not itself asserted to lift a witness; no lifting claim is needed for the independent uniform proof.
