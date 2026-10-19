# Checker development notes

Two preliminary failures were corrected before the completed runs recorded in RUN.stdout/RUN.stderr and CANDIDATE_AUDIT.stdout/CANDIDATE_AUDIT.stderr.

1. An initial local enumeration incorrectly asserted that no split-group local restriction could be a tripleton before imposing the global row-degree budget. The assertion correctly failed. The candidate proof does not make that mistake: it derives one global extra per nonsingleton row before excluding tripletons. The checker now retains local tripletons and separately verifies the global q=5 singleton-plus-K4 row-budget step by dynamic programming. The original failure is in DEVELOPMENT_FIRST_FAILURE.stderr.
2. The first candidate-data audit looked for a witness key named E_tilde; the candidate stores the same matrix as E. The key was corrected. The original schema failure is in DEVELOPMENT_AUDIT_SCHEMA_FAILURE.stderr. No mathematical equality had failed.

The initial connected-control data path contained only divisor controls. Before finalization it was replaced with the explicitly retained accepted endpoint positive-control file; the final run checks exactly fourteen positive masks and independently verifies connectivity for the order-eight and order-24 controls. A count assertion prevents silently omitting them.

All completed mathematical checks pass with empty standard error. No candidate or historical research program was executed.
