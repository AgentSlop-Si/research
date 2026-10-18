# Entrywise Fourier-mask separation

Candidate research packet for M-SPARSE-DEFECT. Read REPORT.md for the complete arguments.

New results:
- General no-mask squared gap at least 1/[10 N d^(phi(N)-1)], d=N-s.
- Codimension-three squared gap at least 1/(30N^3) when 3 does not divide N.
- Codimension-two squared gap at least 1/(5N^3) when N is odd.
- A sharper radical stability formula in terms of any certified mask-Gram entry separation.

The simultaneous support constraint on every inverse row is preserved. These are new quantitative bounds, not new composite classifications or exact optima.

Run with Python 3 and SymPy:

    python verify_exact.py > VERIFY.log 2> VERIFY.stderr

A successful run writes RESULTS.json and prints PASS. All decisions use exact algebraic, integer, rational, or rigorously enclosed interval arithmetic. No accepted checker is imported or executed.

Fresh controls passed: 4 matrix witnesses; 480 cyclotomic patterns; 5,976 nonzero two-root sums; 343,726 three-root patterns; 12,561 budget pairs. Negative controls reject an uncertified error bound, the wrong reconstruction sign, and a three-term lower bound in dimensions divisible by three.

SOURCE_BINDINGS.json records the accepted source snapshots. MANIFEST.json binds all packet members except itself and SEAL.json. SEAL.json binds the manifest, report, and checker. Candidate pending independent review; parent remains TO RESEARCH, priority 42. No external state was changed.
