# ALG-WEIL-LOCAL: exact corrected-package static preflight

Prepared 18 October 2026 UTC. This is a source-bound static preflight, not implementation acceptance.

## Verdict

PASS source recovery, archive/member identity, safe extraction, manifest consistency, and static syntax inspection. Execution remains BLOCKED pending the user's required action-time authorization for this downloaded research package. No package module was imported, no supplied code was evaluated, and no supplied test, verifier, result builder, setup script, or nested archive was run.

The existing formula gate remains accepted on its own scope. The corrected implementation's 13 groups remain unrun at this report's cutoff. Original historical exhaustive suites and unrecovered earlier API bytes remain separate obligations.

## Exact source identities

- Corrected ZIP: [immutable GitHub source](https://github.com/AgentSlop-Si/research/blob/7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb/math/finalized/2026-10-16-source-repairs-0126/weil_static/fft_local_ring_weil_v25_signfix.zip).
- Commit: 7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb.
- Git blob: 70d29013db10fc0707cf5eb65b0e2d71119e6207.
- Recovered bytes: 257283.
- Recomputed archive SHA-256: e159b6a6148c8020c925afc7f56ea50d4362e64a86988c2cacd58b80eb09a556.
- Recomputed local_ring_weil.py SHA-256: 259b8047681ea555152e31c921f13653964cdcb09cc4a9ba9d40f4b2dc56266e.
- [Upstream binding file](https://github.com/AgentSlop-Si/research/blob/7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb/math/finalized/2026-10-16-source-repairs-0126/weil_static/SOURCE_BINDINGS.json), Git blob 1a109fa006a50c206a767453b33553f1d7b17aba.
- [Controlling formula proof](https://github.com/AgentSlop-Si/research/blob/a4dacc1f15eb910ec7d494f1572bc044e2d0533b/math/finalized/2026-10-17-accepted-next-gates-1256/scientific_packet/weil_fresh_checks_20261017_1203/PROOF_AND_GATE.md), Git blob 8d0da336432bfca0150f0447fb75455ac62bf2aa.

The archive was obtained through the read-only GitHub connector in base64 form, decoded locally, and hashed. Its 17 members total 303315 uncompressed bytes. Before extraction, every member was checked for absolute paths, parent traversal, symbolic links, and unexpected size. All members are regular mode-0644 files. All 17 member byte lengths and SHA-256 values match the upstream binding file; all 16 entries in the package manifest match. The manifest does not hash itself.

See MEMBER_HASHES.json, STATIC_AST_SCAN.json, and PINNED_SOURCES.json. sources/ contains exact input snapshots; static/ contains the inert extracted package. A newly authored standard-library parser and hashing script handled the archive as data. Parsing with ast.parse is not compilation, importing, or execution of package code.

## Controlling mathematics and scope

The pinned proof fixes positive-exponent F[x,y]=zeta^(xy), C_s[x,x]=zeta^(s x^2/2), and U_b=F^-1 C_(-b) F. Its direct kernel has exponent -b z^2/2+(y-x)z. For nonzero b, g=gcd(b,q), m=q/g, u=b/g, eta=zeta^g, the supported entries equal kappa_(-u,m) eta^((Y-X)^2/(2u)); the signed block cross ratio is eta^(-u^-1). Covariance is U_b D(a,c)=D(a+bc,c)U_b. The accepted proof and fresh characteristic-zero controls do not establish candidate dispatch or emitted records.

The recovered source has these signs in Fourier conjugation, direct Gauss evaluation, completed-square evaluation, the supplied independent verifier, and the added sign-sensitive tests. This agrees statically with the controlling formulas. It does not establish a runtime pass.

## Executable inventory and dependencies

All five Python files were fully read and parsed by Python 3.12.14 without importing them:

1. local_ring_weil.py: core finite-field and SL2 routines; imports only dataclasses and math, plus future annotations. No file, network, process, or installation actions.
2. test_checkpoint.py: imports the core and standard-library collections, hashlib, math, random, unittest, pathlib. Reads and hashes the predecessor ZIP. Contains exactly 13 unittest methods.
3. independent_verifier.py: independently supplied finite-field Gauss and tuple-SL2 checks; standard-library collections, json, math, pathlib. Does not import the core. Writes independent_results.json beside itself.
4. build_results.py: imports the core and standard-library collections, json, math, pathlib. Writes results.json and RESULT_SUMMARY.json beside itself.
5. run_all.py: standard-library hashlib, json, subprocess, sys, zipfile, pathlib. Launches exactly the three scripts below through sys.executable with check=True and the package root as cwd, then verifies all package-manifest members.

No requirements file, setup.py, pyproject.toml, shell installer, downloaded dependency, eval/exec, dynamic import, network API, or package-manager action is present in this five-file program. The nested PRIOR_v24_COMPLETE.zip is only read and hashed by this suite; it must remain inert. Static inspection reduces risk but cannot grant execution authorization or certify behavior by itself.

## Exact entry points and 13-group scope

The package's documented entry command is:

    python run_all.py

The unchanged driver issues, in order:

    <same Python interpreter> test_checkpoint.py
    <same Python interpreter> independent_verifier.py
    <same Python interpreter> build_results.py

The first command invokes all 13 groups with unittest verbosity 2. TEST_GROUPS.json records their source lines, domains, intended obligations, and exact individually reproducible commands. These are commands for a later authorized run; none was run here.

1. test_gauss_kernel_and_closed_form_agree: q=9,27,25,49; representative b=p^v plus b=0, 13 scalar cases; Fourier, direct Gauss, completed-square agreement.
2. test_exact_support_hierarchy: q=27,25,49, 10 scalar cases; all row/column support counts.
3. test_cross_ratio_has_exact_residual_root_order: q=27,25,49, seven nonzero representative scalars; signed ratio and exact residual order.
4. test_upper_shear_has_negative_chirp_convention: q=9, b=1,2,3,6,8; negative-chirp identity and positive-chirp rejection.
5. test_upper_shear_signed_phase_for_every_q9_scalar: all b=0,...,8; three formulas, negative representatives b-q, signed ratios, and identity dispatch.
6. test_upper_shear_weyl_covariance_label: q=9, b=0,1,3,8; displacement pairs (1,0),(0,1),(2,4), 12 operator comparisons.
7. test_sl2_valuation_counts: exhaustive SL2 enumeration at q=9 and q=25; formulas and full group size.
8. test_nonunit_cell_factorization: all q=9 SL2 elements with b divisible by 3.
9. test_congruence_parabolics_are_subgroups: q=9, levels t=1,2; all inverses and all ordered pair products.
10. test_full_fourier_weyl_element_is_outside_easy_subgroup: q=27; W outside level-one subgroup and seeded 80-factor product staying inside.
11. test_double_cosets_can_refine_valuation_but_not_core_size: q=9 lower-Borel double-cosets; four orbits, two of valuation one, residual core size.
12. test_operation_ledger: p=3,k=6 and p=5,k=4; 12 valuation rows, block products and dense-term accounting.
13. test_predecessor_archive_present_and_hashed: exact predecessor SHA-256 3d6bfe84b09b565e7e06ea6c93384d7a3352698cd90475947a01515b94910ce2.

These corrected-source groups include bounded exhaustive group operations. Passing them would not replay the original source's historical exhaustive runs. The two source identities must never be conflated.

## Resource and side-effect risks

The maximum dense transform size in the test suite is 49; larger q=729 and 625 occur only in scalar operation-ledger formulas, not matrix enumeration. The largest SL2 enumeration is q=25, with 25^4=390625 determinant candidates and predicted 15000 members. The two q=9 congruence subgroups have predicted sizes 162 and 54, giving 26244 and 2916 ordered closure pairs. These are static bounds, not measured performance.

Malformed parameters remain outside the accepted valid-domain contract. For example, unguarded invalid prime/size inputs can cause nontermination or inverse errors; no malformed-input qualification is claimed. The supplied independent verifier uses floating square roots in its tiny primality checks, another reason not to generalize its finite checks to arbitrary large inputs.

Expected mutable outputs are only the three fresh top-level JSON records. Driver output must be captured in a new external log; never overwrite historical_outputs/run_all.log. Assertions must remain enabled: no -O flag and no PYTHONOPTIMIZE. A clean environment should exclude user site packages and PYTHONPATH. Existing source and every historical byte should be hashed before and after.

## Isolation capability checks

Only installed system utilities and a harmless /usr/bin/true command were used for capability probes. No candidate code was involved.

- bwrap exists. A full --unshare-all probe failed with: “loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted”; exit 1. Therefore a separate network namespace has not been established, and this report does not promise network-disabled execution.
- A filesystem/process/user/UTS/IPC isolation probe without a new network namespace succeeded; exit 0. Exact successful probe:

      bwrap --die-with-parent --new-session --unshare-user --unshare-pid --unshare-uts --unshare-ipc --ro-bind / / --tmpfs /tmp --proc /proc --dev /dev /usr/bin/true

- timeout and prlimit are available. No system/network setting was changed and no custom filter was installed.

Proposed execution: create a fresh disposable copy, exclude credentials from its environment, use the already-installed interpreter, set explicit CPU/wall-time/address-space/file-size/process limits, and record the actual launcher and environment. The successful probe supports stronger filesystem isolation if desired; it does not itself show a production launcher or network boundary. An ordinary isolated work directory plus inherited environment restrictions is an honest minimum. Do not claim stronger containment than actually observed.

Source files, the predecessor ZIP, and historical_outputs should be mounted read-only if using filesystem isolation; only the fresh top-level output directory and separate log directory need writes. Recheck all 17 source-member hashes after the run. Do not install anything or execute the predecessor archive.

## Independent checks required after authorization

1. Record the exact copied archive/module/source hashes, interpreter, full commands, start/end timestamps, exit statuses, and complete new stdout/stderr. Confirm 13 actual named unittest “ok” results rather than trusting the summary's hard-coded count.
2. Require the unchanged driver to finish successfully and retain the three newly emitted JSON files. The historical summary says 10 tests and must not be mistaken for the fresh corrected summary.
3. Use newly written independent standard-library code, importing no package module, to check JSON structure, unique domains, counts, arithmetic fields, group counts, and double-coset records. Expected hierarchy/support records: exactly 13, with (p,k)=(3,2),(3,3),(5,2),(7,2), each v=0,...,k; blocks=p^v, length/support/cross-order=p^(k-v), terms=(k-v)*p*p^k.
4. Independently derive q=9 SL2 counts 486,108,54, total 648, subgroup size 162; independently reconstruct tuple group operations if verifying emitted cosets. For q=25 the count target is 12500,2000,500, total 15000. Expected q=9 double-coset (valuation,size) multiset is (0,486),(1,54),(1,54),(2,54).
5. Cross-check fresh hierarchy records against fresh independent_verifier output. This is corroboration, not a substitute for independent mathematics: both supplied scripts originated in the same recovered package.
6. Verify the newly observed negative-chirp, positive-chirp rejection, all-scalar q=9 signed ratio, b-q dispatch, b=0 identity, and covariance tests individually. A newly authored independent entrywise oracle should compare the core's q=9 outputs with direct finite-field sums after authorized import; its assertions and records must be reported separately from the 13 supplied groups.
7. Prove the five historical_outputs members and the predecessor ZIP are byte-identical before/after. The historical manifest belongs to original layout and is preserved as evidence, not applied to the modified layout.

A real failure must be preserved with its command/log/input. Repair only in a new explicitly versioned derivative and rerun all affected tests; never silently change the pinned source.

## Exact remaining authorization request

“May I execute the pinned fft_local_ring_weil_v25_signfix.zip from AgentSlop-Si/research (SHA-256 e159b6a6148c8020c925afc7f56ea50d4362e64a86988c2cacd58b80eb09a556), including all 13 corrected tests, its verifier and result builder, in a clean isolated work directory? Static inspection found only standard-library dependencies and three local JSON outputs. I will cap resources, preserve historical files, and independently check the new results.”

This question concerns execution of downloaded research code. Permission to upload/commit research material does not authorize this action. Until sufficient approval is received, stop at this static preflight.

## Disposition

ALG-WEIL-LOCAL stays TO RESEARCH, priority 42. Q18 remains a separate priority-37 view. No workbook, repository, or other external state was changed by this preflight. A future accepted corrected-derivative run would close only this exact finite implementation interface, not original history, unrecovered bytes, higher-dimensional congruence diagonalization, production qualification, full preparation/bit costs, global Weil normalization, novelty, or a faster general FFT.
