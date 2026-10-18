# Independent eight-stage review

Read REVIEW.md and VERDICT.json. Run `python independent_verify.py` to independently check the frozen data in reviewed_candidate/. The trace and target checks use the standard library; the independent finite-field factorization also needs SymPy. Producer execution is separately recorded in CANDIDATE_REPRODUCTION.log. No source code from the producer is imported by the independent verifier.
