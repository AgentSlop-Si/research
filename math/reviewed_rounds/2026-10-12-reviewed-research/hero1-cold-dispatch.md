Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 0ed05ff8ee37b06814418baf131df6fe0735439306086681e03002f2e142d1be

---

# Independent review: HERO1 Phase37 bounded cold closure

Date: 2026-10-11 UTC

## Verdict

**PASS as a bounded negative closure, with the full RAM gate explicitly open.**

Reviewed artifact: `HERO1_Phase37_Cold_Dispatch_Bounded_Closure_2026-10-11.zip`.

SHA256: `08b43330526738ca3efa8a2b91fb4137a8ad97a208ed42c1a756eb652305e566`.

The sealed closure correctly refutes universal cold scalar dominance of the pinned Phase37 selector over Phase36. It supplies an exact finite joint optimizer for the declared execution-cost objective. It does not supply a new efficient cold-dominating algorithm, a complete paid-RAM implementation, or a generic FFT improvement. No transform correctness defect was established: the distinction is the online selection objective versus an online-plus-preparation objective.

## Independent verification

- Verified the input ZIP digest, all seven closure-manifest members, the embedded original-source ZIP digest, and all 50 source-manifest members.
- Inspected the independently authored checker before execution. Executed a copied checker in a separate review directory; the produced `RESULTS.json` matches the sealed result byte for byte.
- Inspected original Phase36, Phase37, pruned-kernel, lazy-root-plan and cost-ledger source as inert text. No original uploaded program was executed or imported.
- Authored `reviewer_controls.py` separately. It counts arithmetic through executed elementary operations, collects actual requested root exponents, and compares outputs against explicit twisted Fourier matrices. Its 1,569 kernel checks include all nonempty masks through q=8 and seeded/edge-case masks at q=16,32,64 over F257. All pass.
- Independently checked all six saved N32 input/output records against direct DFT and enumerated all 27 N128 label assignments. All pass.

## N32 reconstruction

For N=32, active principal block, and only detail (5,5) supported at {0,1}, the common online overhead is 2(32-5-1)+10+16=78.

Geometric execution has kernel cost 24 and exponent union {1,2,3,6}; cached-root cost is 4+2=6. Total: 78+24+6=108.

Pruned execution has 9 diagonal operations and 11 butterfly operations, including every required odd-only negation. Its root union is {1,2,3,4,5,7,8,9,11,12,13,15}; cached-root cost is 4+13=17. Total: 78+20+17=115.

Full FFT has kernel cost 44 and cached-root cost 21. Total: 143. Dense preparation costs 31 and does not improve these candidates. The online selector chooses 20 instead of 24, but the extra 11 preparation multiplications exceed the four saved online operations.

If the principal block is inactive, subtract 10 from both totals: 98 versus 105. The separately described root validator adds five multiplications to each active-principal total: 113 versus 120. These are distinct accounting boundaries and must not be mixed.

## N128 shared-root control

Use blocks (5,5), (6,5), (7,5), each of size 8 with support {0,1}, and an active principal block. The common overhead is 302. Root exponent scaling by four preserves population counts, so geometric preparation costs 8 and pruned preparation costs 19.

- Three geometric kernels: 302+72+8=382.
- Three pruned kernels: 302+60+19=381.
- A block considered in isolation chooses geometric, 302 versus 309.
- The 27-assignment search has unique optimum all-pruned, 381; the next-best assignment is all-geometric, 382.

The all-pruned advantage shares the additional root preparation once. Independent per-block cold penalties are therefore insufficient. The one-operation execution-cost gain precedes selection overhead and is not a paid-runtime saving.

## General scalar theorem

For a fixed actual support pattern, let each assignment choose one of the three specified kernels, and let E be the union of its required root exponents. Its execution field cost is the common Haar/synthesis cost, plus kernel costs, plus min(D,L(E)), where D=t-C+2^C-1 and L(E)=t-1+sum(popcount(e)-1) over distinct nontrivial requested exponents.

The enumeration contains both inherited kernel assignments. It also permits the root strategy actually used by each inherited method; allowing a better root strategy cannot increase the minimum. Hence its minimum execution field cost is no greater than either inherited execution cost. Root-union dynamic programming and subset/subtotal dominance are sound because future union preserves inclusion and root cost is monotone.

This proves an optimum in a specified finite candidate family, not efficient discovery of that optimum. With B active blocks, the reference examines 3^B assignments. B can be t(t-1)/2. The planner is exponential in B and can be superpolynomial in N. A candidate-common planning cost is not a cost shared with an unmodified Phase36 baseline.

## RAM and ledger qualification

The report appropriately refuses a complete RAM certificate. Its concrete bit-mask implementation sketch gives a plausible all-in asymptotic planning upper bound, not a verified implementation with exact leading constants. Discovery, support verification, candidate construction, root validation/preparation, allocation, mask resets/unions, lookups, every initialization and store, output materialization and the extra selector must be charged under the same model on both sides.

The recorded 399 versus 435 stores and 32 support tests belong only to the new evaluator's declared logical-buffer model. In particular, its principal activity tests use Python `any(A)` while its ledger debits a full principal scan. Thus 32 is a declared logical support debit, not an instruction-trace proof that 32 comparisons executed. Temporary Python lists, repeated activity checks, dictionary internals, reference counting, planner scratch and host allocations remain outside the certificate. This is a nonblocking qualification for the scalar negative result, and a further reason not to advance the full RAM gate.

The source's exact tie order is fft, sparse, pruned; q=1 selects fft. The source prose's sparse-first shorthand must remain qualified. The original cost ledger expressly disclaims exact CPU/bit/RAM accounting.

## Scope and remaining work

**COUNTEREXAMPLE CONFIRMED / COLD DISPATCH REPAIR SPECIFIED / FULL RAM GATE OPEN**.

**Independent review passed for sealed bounded negative closure; complete RAM implementation and efficient selection remain unverified.**

Retain the source online arithmetic result and the existing warm prepared-plan boundary. Do not infer a new cold saving for the mixed-radix hybrid; retain I-dependent outer-codelet formulas and the I=4 qualification for the corresponding numerical constants.
