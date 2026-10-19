# N=3757: exact rank-three rectangle gate

The independently reviewed target result is sharp local rank-three density
16/221, strict above 238/3757, and original disjoint-rectangle optimum 894166.
Every optimizer has exactly 3757 full rank-one coset products with unordered
sides {17,221}. Paid preparation, I/O, storage and the possible 3757 accumulation
additions remain separate. The all-length problem stays open at priority 42.

- Proof: [rectangle/candidate/REPORT.md](rectangle/candidate/REPORT.md)
- Independent mathematical review: [rectangle/review/REVIEW.md](rectangle/review/REVIEW.md)
- Exact source pins, complete finite certificates and original checkers are retained.
- OWNER_UPDATE_PROPOSAL.json is inert. It appends this isolated result to the
  existing owner only; it does not execute an index or native-table change.
- PROJECTION_DISCLOSURE.json gives the only two reversible locator changes.
  Original scientific reports, programs and dependencies are preserved.

Run `python3 verify_package.py` to check the complete package. Run
`python3 verify_package.py --replay` to rerun both mathematical checkers in
an isolated temporary copy, preserving all published receipts. Python 3.8+
and SymPy are required for the full independent replay. No network or
finite-field rank is used in these verifications.

This package does not select another target or change the accepted N=2873
record, any owner status, priority, record count or general open boundary.
