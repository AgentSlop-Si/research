# Reproduce the eight-bank construction

Requirements: Python 3 and SymPy. Copy this directory to a disposable location and run from that copy:

    python verify_literal_trace.py
    python verify_literal_trace.py --source sources/EXACT_WITNESS.json

The first command derives an independent witness by exact row elimination and trace-pairing reconstruction. The second reads only the inert frozen author JSON, checks its explicit edge/selected-system/reflection recipe and every saved sector polynomial, then repeats all original inverse-matrix and Fourier-entry checks for those exact amplitudes. Neither command executes or imports an author or predecessor program.

Both commands must report PASS. They regenerate LITERAL_TRACE_RESULTS.json and AUTHOR_LITERAL_RESULTS.json respectively. The included result files preserve the accepted exact calculations; the author result's source path has been relocated to the relative path used above. All mathematical fields and the source-witness hash are unchanged.

The cubic quotient checks cover all three distinct nonzero roots, hence all 56 literal phase resolvents, and verify both inverse products. The trace sums the triple banks and the direct matrix comparison verifies all 49 Fourier entries. The parameter field is the cubic splitting field over Q(q), not asserted to be Q(q) itself.

Read the [upper proof](../../notes/02_upper_bound.md), [explicit author recipe](../../notes/03_exact_witness_recipe.md), and [scoped acceptance](../../receipts/upper_acceptance.json). Raw run logs and author programs are excluded.
