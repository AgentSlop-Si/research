# Independent Mersenne diagonal review

The scoped arithmetic and complete conversion upper bound pass independent review. Read REVIEW.md for the exact theorem, inherited premises, open gates, and one nonblocking addition/subtraction-count wording correction.

The original candidate remains untouched. reviewed_candidate/ is the separately bound inspection/reproduction snapshot. Reproduce in a disposable copy because the scripts write result files:

- python reviewed_candidate/fresh_controls.py
- python independent_checks.py

BINDINGS.json binds the reviewed inputs. INDEPENDENT_RESULTS.json and the run logs record the fresh evidence. MANIFEST.json seals this review package. No external write was performed.
