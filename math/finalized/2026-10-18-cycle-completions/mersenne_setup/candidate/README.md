# Streamed short-factor Mersenne conversion improvement

The exact converter's prefix/reverse setup drops from O(N log L) to
O(N (log L)^(log_2 3 - 1)), using only explicitly charged O(log L)-bit
Karatsuba products. This closes that scoped setup-scale obstruction.
Same-scale convolution, full-width diagonals, matrix products, and growing
Mersenne-prime selection remain separate obligations.

Read REPORT.md for the proof, dimensions, complete charge ledger and scope.
Run fresh_controls.py for the bounded independent controls. Historical code
is not imported or executed. CONTROL_RESULTS.json and RUN.log record PASS.
