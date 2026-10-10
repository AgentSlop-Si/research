# Reproduction and program boundaries

The notes contain general mathematical arguments. The JSON files are exact finite controls or explicit finite certificates. Their role and original-source hashes are recorded separately; a saved pass is not a new run of an uploaded source implementation.

## Standalone fresh controls

Run from a disposable copy if you want to preserve the supplied files: some programs write result files next to themselves.

- programs/schur/fresh_certificates.py uses the Python standard library. It writes fresh_results.json, a planar rotation certificate and an N=5 modular matrix certificate beside itself.
- programs/sparse_prefix/fresh_controls.py uses the standard library and writes FRESH_CONTROL_RESULTS.json beside itself.
- programs/n5/verify_n5_four_bank.py uses exact standard-library rational arithmetic and prints its certificate JSON.
- programs/n5/independent_scope_control.py uses SymPy and writes independent_scope_results.json beside itself. It checks the inherited N=3, N=7 and N=9 scope; the general larger-N proof is in the mathematical note.
- programs/phase20/fresh_controls.py uses the standard library. Its two bundled inputs under source/unpacked are read as inert text/JSON; the original Python is parsed solely to count its dense-loop operations, never imported or executed by that checker. It writes FRESH_CONTROL_RESULTS.json beside itself.
- programs/phase21/independent_check.py uses NumPy and the supplied Jacobian-index certificate. This is a portable packaging adaptation of the accepted independent checker. Only original archive-hash checks and duplicate-file checks were removed, and the certificate directory was relocated. Its mathematical tests are unchanged. The portable adaptation was statically inspected but not rerun in this integration; the included results come from the original independent run.

## Original source programs

The sparse-prefix source pair under programs/sparse_prefix/original and the Phase 32 modules under programs/phase32/original are byte-identical selected original source files, statically reviewed for privacy and retained as source evidence. They were not executed in this integration or promoted to production validation. The Phase 32 relative module requires NumPy. Its seeded rank records require reconstruction with the source generator; the JSON alone is not a self-contained list of coefficients, primitive roots and every minor witness.

The original Phase 20 program and its historical result JSON are included only as the fresh checker's two inert audit inputs. Historical large selected-output checks are not independently rerun full-output tests.

No blanket instruction to execute every supplied program is implied. Dependencies, exact fields and root availability must be satisfied. Timing, bit costs, memory in bytes and finite-precision stability are outside these exact-arithmetic controls.
