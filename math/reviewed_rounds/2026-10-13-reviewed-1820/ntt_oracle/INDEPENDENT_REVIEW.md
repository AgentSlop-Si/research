# Independent acceptance: bounded exact NTT oracle

Date: 2026-10-13. Decision: **ACCEPT_BOUNDED_EXACT_ORACLE_CANDIDATE**.

Accepted candidate manifest SHA-256:
`e1bb27b3a767517d9511c93e5aa79c3f4b1b2a58b4eb0b65537e99ebe959dbaf`.

## Decision and boundary

Accept the candidate's exact transform definition, source implementation as a bounded reference, and the complete stored expected outputs for the frozen vectors at n=2,4,8,16,32,64,128,256. No blocking repair was found within that scope. This is independent source review plus independent reconstruction of the output artifact, not a rerun of the candidate's own test program.

The review independently reproduced every one of the **128 output vectors and 8,160 coordinates**, including their complete 32,640 serialized bytes. Output SHA-256 is `1401cb324cf991f4eb69db4e962f78f3d2881b5bb9116d8fd629a08f04134091`.

This decision does **not** accept any inherited schedule, adapter, binary, full-corpus correctness gate, resource feasibility, timing, speedup, novelty, or benchmark readiness. The 160 frozen vectors at n=512 through 262144 still lack expected outputs in the candidate. Zero inherited schedule outputs were examined by execution. The historical review-body provenance gap remains open. The accepted paid-ntt-v2-20261013 protocol is unchanged.

## Evidence identity and execution discipline

- All 11 entries in the pinned candidate manifest matched their byte lengths and SHA-256 values.
- All 16 entries in the accepted v2 protocol manifest matched. Its contract, protocol, and manifest pins agree with the design-only acceptance receipt.
- Both historical files, fft_engine.cpp and benchmark_final_ntt.csv, matched their source identities. The C++ file has 400 lines and SHA-256 `0bd324e62b302e4b2e6405c953cb513a93b8840b74137755bd7388b86cddafa7`.
- Every one of the 288 frozen input vectors was independently checked for ordering, contiguous extent, complete hash, little-endian decoding, and canonical range. This is a data audit for the larger vectors, not transform testing.
- Candidate and historical code were read as text or bytes only. Python AST parsing was used for call/import inspection; no candidate AST was compiled or evaluated. Neither scientific codebase was imported, executed, or compiled.
- The only executed scientific program was the newly authored `independent_check.py`. No clocks or performance measurements occur in it. No Sheet or GitHub write occurred.
- The archive contains byte-exact snapshots of all manifest-listed inputs and the historical sources, plus the design-only receipt. Unmanifested candidate `__pycache__` material is deliberately excluded and receives no acceptance.

All accepted input manifests were rechecked after the independent run. The original workspace files were also compared against the snapshots before sealing.

## Exact domain, sign, normalization, and proof obligations

The fixed field is p=998244353 with generator g=3. Fresh trial division proves p prime. The complete factorization p-1=2^23*7*17 and the three nonunity checks g^((p-1)/q), q in {2,7,17}, prove that g has order p-1.

The mathematical public length domain is exactly n=2^e, integer 1<=e<=23. The candidate's `checked_length` excludes booleans, other non-integers, n=1, nonpowers of two, and out-of-range lengths, and pins p and g. Its input validators require exactly n list/tuple elements, each an ordinary Python integer in [0,p-1], without normalization. The default transform execution budget is n<=256, separate from mathematical legality. n=512 is mathematically legal but outside that default execution budget. The recursive reference exposes an explicit larger max_n argument; this review does not endorse using it to claim untested larger transforms.

For omega=g^((p-1)/n) mod p, the exact forward result is

    y[k] = sum_j x[j] * omega^(j*k) mod p,  0 <= k < n.

The sign is positive, output frequency order is natural, and there is no forward normalization. Fresh root checks verified exact order and quarter-root behavior through 2^23 and matched both the candidate and pinned protocol certificates. Those are scalar constant checks, not large transforms. Exact equality to the g-derived omega excludes substituting another order-n root, including the inverse root with opposite sign when n>2.

The candidate source passes these structural proofs:

1. `forward_direct` evaluates that definition by one independent modular exponentiation per summand and a final modular reduction. Python integer arithmetic avoids a machine-width overflow premise.
2. `forward_reference` splits the input coefficient sequence into its even and odd subsequences. Its recursive subproblems use omega^2 because their length-m root is g^((p-1)/m). Given natural-order length-m/2 outputs E and O, the concatenation E[k]+omega^k O[k], E[k]-omega^k O[k] equals the length-m coordinates k and k+m/2, since omega^(m/2)=-1. The length-one leaf closes the induction; it does not extend the public domain to n=1.
3. `inverse_direct` evaluates the output polynomial by descending Horner evaluation at omega^(-j), then multiplies once by n^-1. Root orthogonality makes this the exact inverse. It calls neither forward function and does not use their reversal shortcut.
4. The three candidate routines share constants and validation, but not a transform implementation. The source imports only `struct` and the future-annotations directive. The test harness imports the candidate module and standard-library modules; no inherited implementation or generator import appears.
5. Request inputs are copied to tuples, and result lists are newly allocated. The inspected transforms do not mutate the supplied input. Canonical output reduction and full-length comparison are explicit.

The independent reviewer computed forward outputs by fresh polynomial Horner evaluation, advancing evaluation points multiplicatively. The independent inverse uses a separately authored inverse matrix sum with modular inverses. It neither calls nor copies the candidate's forward/reference implementation. Complete stored coordinates, rather than merely hashes, were compared before confirming the complete serialized artifact.

## Independent results and corruption coverage

The fresh checker established:

- 128/128 stored vectors and 8,160/8,160 coordinates equal the independently evaluated positive-exponent map.
- Every stored vector passes an independently evaluated inverse, the F_+ squared identity, DC and output-sum identities, and unchanged input bytes.
- All 56 applicable zero/constant/impulse/alternating closed-form vectors agree.
- Three literal anchors and 90 exhaustive vectors over {0,1,p-1} at n=2 and n=4 pass the independent controls.
- Fresh linearity and cyclic-product checks pass at n=2,4,8,16,32 using test factors different from the candidate's factors. Four finite-field linear-product examples pass with all padded tail entries checked.
- All **8,160 single-coordinate mutations** are rejected, one for every stored coordinate. These checks demonstrate sensitivity at every coordinate of the bounded artifact.
- **49 fresh negative controls** reject bad types, illegal lengths, fixed-constant mismatches, opposite roots, execution-budget overrun, short/long/iterator inputs, noncanonical input/output, short/long wire format, endian mistakes, incorrect sign or normalization, bit-reversed output, and insufficient linear padding.
- A two-coordinate mutation preserves DC and the total sum yet is rejected by full-coordinate comparison. The weaker invariants are therefore not relied on as substitutes for complete output agreement.

The candidate's 44 reported controls were checked for unique entries, recorded detection, and consistency with the test source and validator paths. They were **not rerun against candidate functions**, because candidate execution was expressly excluded. The fresh controls validate the independent review machinery, while candidate guard behavior is supported by source inspection. These two kinds of evidence are not conflated.

Fresh all-coordinate mutation checks are separate from the 49 conceptual negative controls. The 128 frozen vectors remain a finite test set, not exhaustive coverage over all possible inputs of those lengths; the structural source review supplies the general algebraic rationale.

## Cyclic versus linear semantics

The n-point product theorem is cyclic multiplication in F_p[z]/(z^n-1). A linear product requires n at least len(a)+len(b)-1, followed by zero padding and inspection of every tail entry before trimming.

The independently verified example is [1,2,3]*[4,5,6]: its linear result is [4,13,28,27,18]. At n=4 the cyclic result is [22,13,28,27], with 18 wrapped into the constant coefficient. Linear n=4 is rejected; n=8 gives the complete five-entry linear answer with a zero padded tail. Nothing here establishes integer recovery, coefficient bounds, CRT reconstruction, Bluestein behavior, or arbitrary-length support.

## Historical source claims

All six candidate defect witnesses are accepted as source-text findings. `SOURCE_REVIEW.json` includes the exact cited source lines.

- S1: Plan forwards do not check request size before n-indexed accesses. Plan(4) and a two-entry input reaches an out-of-range access.
- S2: For radix2 at n=2, the expressions applied to malformed [p,0] produce [0,p], rather than rejecting. Separately, the CLI's z%MOD normalizes malformed values. Both contradict the future reject-malformed-input wrapper contract.
- S3: With repeats=0 and at least one size-loop iteration, discarded warmups leave no stored samples; median indexing then accesses element zero of an empty vector. Negative repeats similarly leave benchfair empty. The older benchmark's zero-repeat witness is valid; its negative reserve may throw earlier, so no broader negative-repeat claim is needed.
- S4: The CLI allocates vector<u32>x(n) before Plan/Bluestein validation. Negative n converts to a large unsigned size before validation and can fail allocation. This is an ordering defect, not evidence that a particular allocation occurred.
- S5: Both inverse wrappers form begin()+1 on an empty vector before downstream checks, outside the valid iterator range.
- S6: Bluestein get_m(1)=1 leads to Plan(1), which rejects. The CLI's separate n=1 return is not Bluestein(1) support and lies outside the v2 comparison.

These findings are not executed failures and do not prove a butterfly error on valid canonical input. The original schedule bodies must not be changed on the basis of an unestablished butterfly defect.

## Remaining gates and reproduction

No candidate repair is required for the bounded acceptance. Before any paid pilot, retain the candidate's outstanding gates: explicitly authorized source-bound adapter work; reviewed source-to-adapter diff; guarded request and allocation handling; schedule-owned paid plans; full-output sink; private paid fixtures and lifetimes; correct direct enclosing intervals; exact diagnostic/release build identities and type-width/resource/sanitizer checks; all 288 independent expected outputs; every schedule's complete preflight and session pre/postflight checks. No timing may be inferred from this acceptance.

Run the new review checker from the extracted archive:

    python -I -B paid_ntt_oracle_independent_review_1801/independent_check.py

The script reads only the bundled input snapshots and overwrites only its four deterministic review-result JSON files. It does not execute any bundled candidate or historical code. `FILES_SHA256.json` binds the complete review package; the adjacent ZIP seal binds the archive and that manifest. Inspect the acceptance receipt for the exact source, output, and result pins.
