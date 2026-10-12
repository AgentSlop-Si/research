Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted. Mathematical assumptions, classical attribution, evidence depth and remaining work are retained. Original source-report SHA-256: cddb1ca6916dce0f3ecb34c13ac8e0755ab48e0df4590afcecb8bf92a4edd0d1.

# Q33 retained N3/N4 replay: separate cold mathematical review

Date: 12 October 2026.

## Verdict: ACCEPT, within the existing scope

The final author candidate is `Q33_Retained_N3_N4_Data_Replay_CANDIDATE_2026-10-12.zip`, SHA-256 `1cfd5fe14905d9e7a81cfdb0f08ef862962587d6e11c3fa630d2eaefb961bfcb`, 565,860 bytes. The reviewer verifies every one of its 32 manifest entries, its exact member set, the archived source bindings, and the equality of all reviewed snapshots to that final archive. No mathematical error was found.

Accept the additional complete independent replay of the retained mathematical data in `CERT_N3.json`, `CERT_N4.json`, and `HENSEL_RESULTS.json`. The accepted theorem and its limitations are unchanged. This is evidence-depth closure for a specified finite-data obligation, not another theorem, discovery, canonical entry, or priority result.

## Independent computation

`cold_review.py` is a separate implementation. It imports SymPy 1.14.0 and standard-library modules only. Neither the historical source programs nor the author candidate's checker is executed, imported, compiled, or parsed as a program. Their bytes remain inert.

The independent algorithms differ from the author candidate: finite geometric weighted-cycle series for Green inverses; SymPy exact rational matrices; polarization of minor evaluations for Q; SymPy algebraic-domain matrix determinants in Q(zeta)[t]; literal P0-inverse commutators over prime powers; and derivative/Newton Hensel corrections rather than residue-coset enumeration.

### Every Green branch and retained matrix entry

All eight weighted Hamiltonian cycles, endpoint permutations, diagonal units, and branch inverses pass. The exact Green denominators are 19, 13, 13, -26 for N3 and 82, 37, -11, -5 for N4. They are all units modulo 97. The identity W^N=hI, the denominator determinant 1-h, both inverse identities, and every rational inverse and gauged branch entry are checked independently.

All rational reconstructed branches match the author candidate. All 359 saved entries in A, B, gB1, gB2, Q, and the original commutator agree with the original JSONs, as do all seven saved b_delta entries. Both aggregate stages are invertible; all B entries are units; the Fourier roots have exact orders 3 and 4. C remains the specified identity.

### Full quadratic lifts and exact minor provenance

Polarization independently recovers every entry of Q. The matrices are 9 by 6 and 18 by 10, with ranks 6 and 10 over F97. The selected maximal determinants are 18 and 31.

For N4 the historical pivot rows are [0,1,2,3,5,4,6,7,8,9], while the accepted reconstruction uses [0,1,2,3,4,5,6,7,8,9]. These are the identical row set from the identical Q, with one transposition. Direct exact integer determinants reduced modulo 97 give 66 and 31, and 66=-31 mod 97. There is no changed witness. The earlier report's statement that the source row choice was unspecified can be clarified additively while preserving that historical report.

### Exact cyclotomic determinant construction

The determinant is independently computed over Q(zeta3)[t] or Q(i)[t] from the actual rational branch matrices. Every exact rational basis coefficient matches the author candidate, not only its reduction. The exact degrees are 6 and 8. Literal P0^-1 Pj constructions are separately checked at three rational parameter values for every matrix entry.

The reduced coefficient vectors, in ascending degree, are:

- N3: [33,8,31,37,67,4,14], f'(1)=68 mod 97.
- N4: [10,40,72,60,1,29,27,56,93], f'(1)=65 mod 97.

Both have f(1)=0 modulo 97 and nonzero derivative. The exact characteristic-zero f(1) is nonzero in both cases. Its basis coefficients are recorded in `COLD_RESULTS.json`; the lifted algebraic parameter is not asserted to equal 1.

As an independent check on the defining P matrices, the literal P0-inverse commutator determinant agrees at all 94 regular residue parameters for N3 and all 93 for N4. The excluded first-column poles are respectively [20,29,59] and [19,35,61,69]. The exact polynomial construction covers the continuation at those poles; it does not pretend P0 is invertible there. At the saved base points every original commutator entry agrees and both determinants vanish modulo 97.

### Every saved Hensel pair, with direct prime-power checks

Independent Newton corrections recover all eight saved (modulus,t,omega) records through 97^4=88,529,281. At every recorded modulus, the code checks the cyclotomic polynomial for omega, the exact determinant polynomial at t, and the literal P0-inverse commutator determinant. All required denominators, B entries, stage determinants, and the selected maximal Q minor remain units. Every full Q is freshly reconstructed at each modulus.

The varied branch is also rebuilt directly from its trace after multiplying the correctly permuted endpoint gauge by t. This proves that the parameterized B is precisely the stated legal Green branch sum, with unchanged Green denominator, at every recorded lift.

The final pairs are:

- N3: t=13,866,830; omega=44,659,902.
- N4: t=32,570,467; omega=22,709,274.

Finite digits provide regression evidence. The existing accepted simple-root/completeness proof supplies the infinite local root and algebraic complex witness. This review does not replace that argument with finite computation.

## Scope and remaining work

Only the retained N3/N4 all-data replay is closed. The previously accepted finite-witness/exceptional-complex-witness theorem is unchanged. This is additional evidence depth, not a new theorem or priority result.

The broader historical-data gate must be reconciled only against actually specified retained data. This acceptance does not create an obligation to invent additional cases. The missing 56 unsaved cases remain unavailable and uncertified. C07 N64 already has independent acceptance and is not newly replayed here. Q22 N256 is separate. Preserve previously accepted Hadamard, Jacobi, and outer controls without relabeling them as new results.

No all-length compatible construction, uniform conditioning, interval-certified decimal gap, production executor, faster FFT, unrestricted lower bound, or worldwide-priority claim follows. Historical search counters and floating-point diagnostics are outside the replay.

## Reproduction and sealing

The complete reviewer archive, preserved separately from this report publication, includes the exact final author candidate, snapshots and independent checker. Its manifest and verdict bind those bytes, and an external seal records archive validation and the isolated replay outcome. The original reproduction command is python cold_review.py with Python3 and SymPy1.14.0; executable files are not part of this report-only publication.
