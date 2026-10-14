# Pinned F23 sixteen-bank witness candidate

Read REPORT.md for the exact theorem and restrictions. The raw witness is outputs/WITNESS.json; it alone suffices for a literal independent arithmetic check. Its SHA-256 is ad1437b4c796550d02772b7cedd78d6ff6109b180e2d9853a08b176a415dbc81.

The original-grammar target at N=11, q=13 over F23 is represented by sixteen nonzero banks with seven same-sign nodes {1,2,3,4,5,6,9} on each side, two cross-sign singleton nodes pinned at 4, and beta=1 throughout. Candidate equality b_4(F23)=16 uses the separately accepted lower bound, whose exact review is copied into source_evidence/.

This is a candidate awaiting independent review. No novelty, broader optimum or Fourier arithmetic speed claim is made.

Run: python3 -I fresh_attainment.py --out replay

The five deterministic output files match the supplied cold replay byte-for-byte, as recorded by REPLAY_VERIFICATION.json. All code in this candidate was newly authored; no historical scientific program was executed.
