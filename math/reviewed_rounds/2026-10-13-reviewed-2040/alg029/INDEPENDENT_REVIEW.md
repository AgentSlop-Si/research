# ALG-029 bounded numerical certifier: independent ACCEPT

Review date: 13 October 2026 UTC.
Verdict: ACCEPT, restricted to the frozen bounded value API and its stated arithmetic/representation ledger. No repair is required for that scope.

## 1. Exact object accepted

Input archive: `ALG029_Bounded_Numerical_Certifier_Candidate_2026-10-13.zip`

SHA-256: `afcc7641db413ed56a750350a2f86efe852665cf74e028e27fb091407d41563c`

Principal code, `certifier_fresh.py`, SHA-256:
`8752bfd2f4c64d89b504709bb70016bebec97a73a21bae52a235959986fae3f3`

Principal proof, `PROOF_API_LEDGER.md`, SHA-256:
`8dc5ac2fe26f0b71c8eb08141a4a6e60bfa80c23feefd7f6321d1b67a179050f`

All 15 manifest entries were checked by size and SHA-256. All five copied source pins match both their archive bytes and the locally available named original files. The working-directory principal code and proof also match the archived bytes. This establishes byte identity, not historical wall-clock chronology or independently authenticated provenance beyond these local source bindings.

The accepted domain consists of a built-in Python list of length N = 2^L, 0 <= L <= 8, whose entries are built-in length-two tuples or lists containing exact built-in integers in [-32768,32767], interpreted as complex Q8 values. The tolerance numerator is a built-in integer e in [0,131072], with epsilon = e/65536. The arithmetic budget is a built-in integer in [0,1000000]. Boolean and subclass substitutions are excluded by exact-type checks.

For nonzero admitted input and 1 <= e < 65536, the default-resource call returns a dense Q129 vector z with

    max_k |z_k - (U_N x)_k| <= (e/65536) ||x||_2,
    (U_N x)_k = N^(-1/2) sum_j x_j exp(-2 pi i k j/N).

The ideal intermediate states, node norm estimates, lower norm estimate ell, and retained leaf estimates are actually constructed and paid for. They are not supplied as free numerical oracles.

The exact-zero input returns dense zeros, including e=0. Nonzero e=0 returns EXACT_REQUIRED with no successful or partial vector. For e>=65536, dense zeros meet the target. Invalid inputs and exhausted arithmetic limits fail closed as specified.

This accepts a conservative approximate-output relaxation. It does not accept an exact threshold mask, exact retained coefficients, epsilon-zero transform, relative-best-k promise, zero-tail exact recovery, all-size numerical result, Python runtime/bit-complexity theorem, practical speedup, novelty claim, score change, or scientific-parent closure. It does not certify the historical complex128 program. Parent priority 42 is unchanged.

## 2. Method and independence

The candidate source and historical sources were read only as inert text. No candidate, author test, packet builder, or historical research program was imported or executed. The only executable research program run for this review was the newly written `independent_verify.py`.

The verifier performs:

- Exact archive, manifest, and copied-source checks.
- Fresh functional reconstruction of every allowed cold Q128 root setup, including exact root-table hashes, maximum widths, and setup operation counts.
- A separate Q256 direct-transform oracle: half-angle identities produce a primitive root, first-quadrant roots use consecutive multiplication, and exact quadrant rotations produce the other quadrants. This differs from the candidate's recursive even/odd table assembly and from the author's Machin/Taylor oracle. The shared half-angle identity is justified analytically below; agreement is not used as a substitute for that proof.
- Strict containment of every independently computed Q256 root enclosure inside the corresponding reconstructed Q128 interval. This is stronger than merely checking that two enclosures intersect.
- Direct residue-class sums for every stored node and direct unitary DFT sums for every output in all four sealed N=256 receipts, without candidate butterflies or candidate norm functions.
- Exact rational checks of the universal width, norm, delta, integer-size, and resource inequalities.
- Exhaustive 741,321 signed interval-product pairs at scale 16, and 2,145 nonnegative square-root interval controls. Scale-independent floor/ceiling and endpoint arguments supply the universal proof.
- Static AST/source inspection of the five exact-type validation guards, fail-closed result path, and absence of dynamic execution or external I/O.
- Eleven negative controls, including wrong exponent, bit-reversed output indexing, raw rather than unitary normalization, Q128 rather than Q129 output decoding, a corrupted output, a corrupted node norm, invalid directed-rounding substitutions, and strict comparison at a pruning equality.

`INDEPENDENT_RESULTS.json` and `REPLAY_LOG.txt` record 1,511,247 fresh passing checks, including eleven negative controls. Finite receipt controls are supplementary. Universal acceptance rests on the algebraic containment proof, finite exhaustive setup census, and source-level branch/ledger review.

## 3. Interval primitives and roots

A Q128 interval [l,h] denotes [l/S,h/S], S=2^128. Four exact endpoint products contain the bilinear image of a real interval pair. Floor of the minimum divided by S and ceiling of the maximum divided by S therefore enclose the product for positive, negative, and straddling intervals. The code's `-((-hi)//S)` implements mathematical ceiling, including negative values. Each end expands by less than q=1/S.

For nonnegative [l,h], `isqrt(l*S)` is a lower numerator and the integer ceiling of sqrt(h*S) is an upper numerator. The code obtains the latter by testing the exact square of `isqrt(h*S)` and incrementing exactly when necessary. Norm bounds instead square already-scaled endpoints, so their square-root input requires no extra factor S. Both uses have the correct units.

The singleton [1/2,1/2] supplies c=1/sqrt(2), enclosed in [0,1] with width at most 2q. Cardinal roots for lengths 1, 2, and 4 have exact signs. At lengths 8 through 256, the half-angle equations

    C_m = sqrt((1+C_(m/2))/2),
    S_m = sqrt((1-C_(m/2))/2)

take the positive first-quadrant branches. Starting at C_4=0, they therefore enclose cos(2pi/m) and sin(2pi/m). The primitive C_m - i S_m has the required negative exponent. Interleaving the old roots and their products with this primitive yields the full root_m table. This proves containment independently of a numerical comparison with trigonometric library values.

Fresh exhaustive cold setup results:

    N       1   2   4    8     16     32     64      128      256
    width   0   0   0    1      5     13     22       36       60
    ops    18  34  66  400   1038   2284   4746     9640    19398

Widths are Q128 numerator units. The allowed root-coordinate width is 2^20 units, and every endpoint is within [-2S,2S]. All nine table hashes match the sealed claims. There are 2N-1 logical root entries; for N>=4 the generated complex multiplications number N-4. The complete setup is performed inside each successful positive-domain call; no uncharged cache is assumed.

## 4. Universal ideal-state containment and accumulated error

The source kernel computes

    left_j = c (v_j+v_(j+m/2)),
    right_j = root_m[j] c (v_j-v_(j+m/2)).

This is the negative-exponent unitary DIF recurrence. The child offsets r and r+s, with doubled stride 2s, identify natural-order output residue classes. At depth d, s=2^d, m=N/s, the ideal state is

    v_(r,s)[j] = s^(-1/2) sum_(t=0)^(s-1)
                x[j+t*m] exp(-2 pi i r(j+t*m)/N).

This direct formula independently identifies the code's signs, scaling, and output indexing. Each split is unitary on the combined children. Thus every ideal intermediate coordinate has modulus at most r=||x||_2 <=128 sqrt(2N)<4096, and a node's norm equals the norm of its owned final Fourier coefficients.

Input intervals are singleton exact conversions. Assume a real-coordinate width bound W_d<1. Endpoints then have magnitude at most 4097. Addition or subtraction doubles width and has magnitude at most 8194. With R=2^-108,

    T_d <= 2 W_d + 16390 q,
    W_(d+1) <= 4 T_d + 8194 R + 4q
              = 8 W_d + 65564q + 8194R
              < 8 W_d + 2^-93.

The product-width bound uses the maximum endpoint magnitudes; all root, normalization, butterfly, and outward-rounding contributions are present. It is an accumulated error bound against the exact ideal state, not a local rounding estimate against a previously approximate state.

Starting at W_0=0, for d<=8,

    W_d < ((8^d-1)/7) 2^-93 < 2^(3d-93) <= 2^-69.

The corresponding bounds also give W_d,T_d<1, closing the induction rather than assuming the needed magnitude bounds. The exact rational verifier separately checks all nine depths with the stronger constant 65564q+8194R.

For a node containing m complex coordinates, minimum/maximum absolute coordinate values give rigorous box norm endpoints. Correlations can make this box bound wider, not unsound. Its exact norm width is at most sqrt(2m)W_d. Integer square-root rounding adds at most 2q. Therefore its midpoint a_A satisfies

    |a_A - ||v_A||_2| <= (sqrt(2m)W_d+2q)/2 < 2^-64.

For a retained leaf, the Q129 componentwise midpoint has complex error at most the sum of its two component radii, hence less than 2^-69. Both estimates concern the ideal states/coefficients.

## 5. Ell, budgets, pruning, and boundaries

At the root, singleton Q8 input intervals make the squared norm exact. The lower root endpoint gives r-q<ell<=r. A nonzero Q8 component has magnitude at least 2^-8, so ell>=2^-8 and ell>=r/2. For the positive route,

    theta = epsilon ell,
    delta = theta/4 >= 2^-26.

Consequently the universal norm/leaf errors lie far inside delta. The code also tests the actual per-node width by the exact inequality

    2*65536*(h_A-l_A) <= e*ell_integer.

At a leaf, it applies the analogous inequality to the sum of the two real-coordinate widths. These are the correct cross-multiplied midpoint-radius bounds, with no missing factor two or factor S.

The pruning comparison is exactly

    2*65536*(l_A+h_A) <= 3*e*ell_integer,

which is equivalent to a_A+delta<=theta. Equality prunes. For any pruned node, ||y_A||_2<=a_A+delta<=theta, so every zero-filled coordinate below it has error at most theta. Retained leaves have error at most delta. Each output belongs to one first-pruned node or one retained leaf; pruning errors do not add along a path. Thus the global maximum-coordinate error is at most theta<=epsilon r.

This guard is intentionally different from exact ideal hard thresholding. A true coefficient tie need not be a guard tie. Acceptance does not convert the approximate conservative decisions into an exact mask guarantee.

Every unpruned node has norm greater than theta/2. Disjoint same-depth energies and ell>=r/2 yield

    A_d <= min(2^d,16 epsilon^-2),
    V <= N sum_(d=0)^(L-1) min(1,16 epsilon^-2/2^d) <= NL <=2048.

At epsilon>=1, zero output is sound because each unitary coefficient magnitude is at most r. At exact zero input, every unitary coefficient is zero even for epsilon=0. Nonzero epsilon=0 is explicitly excluded from successful numerical output rather than being silently approximated.

## 6. Complete validation and failure review

Source locations below refer to the frozen `certifier_fresh.py`.

- Lines 120-121 validate op_limit by exact `type(...) is int` before its numerical comparison, reject booleans/subclasses, and bound it in [0,1000000]. Invalid-limit rejection performs no numerical work and returns no output.
- Lines 125-127 test exact built-in list type before evaluating length, then accept only the nine stated lengths. Oversized or malformed outer containers are rejected before component traversal.
- Lines 128-129 test exact integer e before its built-in bit_length and range comparisons. Thus an arbitrary object cannot supply an epsilon callback. Both range endpoints are correct.
- Lines 131-137 require exact built-in tuple/list pair types, then length two, then exact built-in integer components before bit_length/range/nonzero comparisons. List, tuple, and integer subclasses cannot inject overridden iteration, length, arithmetic, comparison, or bit_length methods. Floats and booleans fail before numerical conversion.
- The component loop continues after discovering nonzero input, so a malformed later entry is never skipped. `validated_components` is incremented for every attempted component validation. All special zero/large-epsilon branches occur only after the full successful scan.
- Lines 138-141 implement the stated epsilon-zero and all-zero branches. Dense zeros are written before the positive route and are explicitly counted. The arithmetic limit is a numerical-primitive limit, so zero branches may succeed with op_limit=0; validation and output writes are separate work.
- Lines 22-25 increment attempted arithmetic work and check the limit before evaluating the next primitive. Consequently LIMIT reports limit+1 attempts but executes at most limit numerical primitives. Every core operation checks argument/result magnitude against the 320-bit cap.
- Lines 200-201 catch only the deliberate Halt outcomes and return output=None and an empty node list. Already-created zeros, failed work, and counters remain paid. Other runtime exceptions are not misreported as success. No exception-swallowing path returns an approximate vector.

These are source-level proofs of the actual guarded paths, not a claim that the candidate's invalid-input tests were rerun. Ordinary fixed-value call semantics and the exact built-ins are assumed; concurrent external mutation of input lists or monkeypatching the module/runtime is not a stated supported execution model.

Validation comparisons, type checks, metadata maxima, and counters are separate bounded control work, not secretly included in the core numerical count. The API is an in-memory value interface. Parsing, wire-size limits, encoding, and transport are expressly separate. No raw input or arbitrary object is echoed into a success or error result.

## 7. Arithmetic, bit, and storage accounting

The source primitives match the stated costs:

- Real interval product: four multiplications, six comparisons, two floor divisions, two negations =14 core primitives.
- Complex interval product: four real products and four endpoint additions/subtractions =60.
- Butterfly: eight plus/minus endpoint operations, four real scale products, one complex product =124, or 62 per unit of split volume.
- Norm scan: at most 22 core primitives per complex state entry, plus at most five per node for final norm square roots.
- Root setup: at most 76N+800, including all tables, half-angle radicals, range/width checks, and c.
- Conversion: 2N multiplications.
- Norm-width budget and pruning guard: seven per visited node.
- Retained-leaf budget and midpoint write: seven per retained leaf.
- Ell check and delta construction: two.

Let K<=2N-1 be the visited nodes and T<=N the retained leaves. Independently summing these categories gives

    A <= 100N + 84V + 12K + 7T + 802
       <= 131N + 84V + 790
       <= 160N + 100V + 2048
       <=247808 <1000000.

Hence the candidate's looser published bound is safe. Norm-entry traffic is exactly N+V: the root is scanned once and the two children of each split total the parent length. Setup, failed prefixes, dense writes, retained writes, state allocations, stack/index work, and constant-size node certificates are all recognized. The core counter treats compare as one abstract trichotomy and isqrt as one explicitly named numerical primitive; it is not an instruction count or unit-cost bit model.

The maximum possible input norm is below 4096, state endpoints are at most 4097S, and plus/minus endpoints at most 8194S. Root multiplication products and all scalar threshold products are smaller than the norm accumulator bound

    2N(4097S)^2 < 2^291.

Thus 320 magnitude bits safely cover valid-route numerical intermediates. Multiplication, division, and integer square root retain their separately stated backend bit costs. No proof of Python implementation-level runtime follows from these abstract counts.

Depth-first traversal keeps the current state and pending siblings at total length at most N; transient child construction adds at most N. Parent vectors are deleted before descent. Thus the state bound is 2N complex boxes, or 8N endpoint integers. All root levels contribute fewer than 8N endpoint integers; input and output each contribute 2N components; at most 2N-1 seven-field receipts contribute at most 14N logical integer slots. Stack scalars, constants, bounded metadata, and arithmetic temporaries fit within the conservative remaining allowance in 48N+512. Object headers/references and allocation overhead are explicitly additional; no RSS claim is accepted.

The output schema has at most 511 seven-field node rows, 512 output integers, bounded scalar metadata, and fixed ledger keys. Even conservatively budgeting 100 decimal characters per 320-bit scalar and generous field/separator overhead remains below one MiB. Encoding that object costs additional work; the receipt-size bound is not free I/O. An independent replay must pay again.

## 8. Fresh evidence and limitations

The four stored N=256 receipts cover minimum impulse and a full-scale complex input, at e=1 and e=49152. Independently checked:

- 1,036 node certificates from direct residue sums.
- 1,024 dense output coordinates from direct unitary DFT sums.
- 512 retained leaf certificates, including strict 2^-69 error checks.
- All node norm midpoint errors strictly below 2^-64.
- Exact ell floor identities, delta factors, guard decisions, complete/disjoint output partitions, norm/split traffic, energy counts, and dense-write ledgers.
- All nine root hashes, maximum widths, entries, and exact setup costs.

The certificate corruption, sign, indexing, normalization, and output-scale negative controls are rejected by the same exact predicates that accept the sealed receipts. They are not alternative successful transforms.

No candidate transform was executed; selected receipts were audited as inert evidence. Actual callback and exhausted-budget behavior is established by short-circuit/source review, rather than claimed as independently observed execution. The fresh numerical checks supplement the universal proof and cannot establish all signed-Q8 inputs merely by enumeration.

## 9. Disposition and remaining gate

The previous missing setup/certificate-cost construction is closed for this particular bounded API: actual roots, ell, node certificates, leaf certificates, error accumulation, boundary outcomes, and paid bounded resources are provided and independently accepted.

There is no further mathematical acceptance gate for this frozen bounded child. Production integration, optimization, a different representation, broader N, smaller precision, exact epsilon-zero outputs, an all-size bit-cost result, exact-mask semantics, or a stronger approximation target would require a separately specified task and review. The broader scientific parent remains open to its existing scope; acceptance changes neither its score nor priority 42.

No Sheet, GitHub, or other external write was performed. This review archive is the deliverable, with source bytes preserved.
