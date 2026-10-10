# Source 13: independent_checks.py

SHA-256: 595cae3615330c3493850b8fec4c7294c2589f481d14a18c70ca7c819735c50b

Representative: additions/1742/phase21_audit/independent_checks.py

Read: all 220 lines / 9638 bytes. Full inert inspection; no import, execution, compilation or syntax parse.

## Flow and complete-read coverage

All220 lines: independent prime/factor/root and coefficient/Prony recurrence(12–59); coefficient digest and exact NumPy polynomial remainder/resultants(61–98); Python-integer matrix helpers(100–133);18 even-size matrix controls(135–181);15 floating spectral checks(183–201);12 dyadic plus18 additional Prony artifacts/main(203–220).

## Mathematical scope

Constructs the same annihilator through a q-binomial recurrence and exact-root evaluations, independently from source repeated root multiplication. Exact modular resultants support characteristic-zero nondegeneracy for fixed sizes. Matrix checks include zero weights, singular masks, wraparound rho restriction, commutators and reordered-cycle cut ranks. Stronger spectral bound follows the written analytic variance argument; SVD is only a control.

## Input guards and acceptance

The intended primes satisfy p<10⁹; one residue multiply/subtract stays safely within signed64, with no int64 dot accumulation in modular polynomial work. Root order/primality and nonzero recurrence denominators are controlled on stored sizes. Low-level resultant helper assumes nonzero polynomials and normalized leading coefficients as generated internally.

## Cost

O(h) coefficient recurrence steps do not make the whole checker linear: pow/inverse steps and h root evaluations of degreeh polynomials add cost; Euclidean polynomial work is naive quadratic. Matrix powers use dense Python arithmetic; spectral controls use SVD. No fast simultaneous Green evaluator.

## Tests, records, dependencies and actual impact

All30 saved coefficient-u32le SHA digests match copied records; each monic degree is n/2 with nonzero constant and recorded nonzero derivative/forbidden resultants. Exact resultants were not recomputed. Remainder trace stores degrees/hashes but not every leading coefficient despite the helper docstring wording.

Finding references: F04.
