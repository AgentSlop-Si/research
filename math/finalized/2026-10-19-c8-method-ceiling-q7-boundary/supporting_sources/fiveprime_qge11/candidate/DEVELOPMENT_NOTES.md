# Development notes

The exploratory script in development used finite-dimensional floating linear programming only to discover possible weighted incidence inequalities. None of its numerical output is a proof or a verification certificate. REPORT.md proves the inequalities symbolically, and verify_fiveq.py checks their finite local configurations using integer/rational arithmetic only. The final verifier does not import the exploratory script.

A preliminary interactive five-by-five inversion call used DomainMatrix.from_list on algebraic-field elements and raised CoercionFailed. The constructor was corrected to DomainMatrix(rows, shape, domain). This was an API mismatch, not a mathematical or completed-check failure. The finished verification run passed with empty stderr.

The q=7 near-pencil/triangle row group is deliberately retained as a boundary countercontrol. It defeats a possible incorrect claim that every split group has degree at most q+3 for all primes q>5. It is rectangular and does not establish or refute a square equality mask at N=35,d=11.

No independent review has been performed by this worker; independent review of the sealed proof and retained data is the next acceptance gate. No service limit was encountered.
