# Independent order-5q first-interior review

Verdict: PASS, no required repair, for prime q>=11 and q<d<2q in the original binary Fourier mask model. Read REVIEW.md for the universal symbolic audit and preserved scope. VERDICT.json records the bounded acceptance.

The source candidate is frozen by CANDIDATE_BINDING.json and its copied manifest. No candidate or historical code was executed, no external write was made, and the owner remains M-SPARSE-DEFECT, TO RESEARCH, priority 42.

Reproduce the independent exact controls with Python 3 standard library only:

    python independent_checks.py > RUN.stdout 2> RUN.stderr

The script reads the frozen candidate and seven bound local source originals, writes only into this review directory, and uses exact integer cyclotomic arithmetic. Its elapsed-time field is runtime metadata. Reproduction changes the runtime field and therefore requires a new manifest to reseal output. CHECK_RESULTS.json contains the completed run summary; RUN.stderr is empty.

The q=7 file is a rectangular 7-by-35 row-group countercontrol, never a full square-mask construction. Controls support the symbolic proof; no full-mask census is claimed.
