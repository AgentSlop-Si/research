# Base-field Fourier bank construction

New author work, 10 October 2026. Main proof: BASEFIELD_FOURIER_UPPER_BOUND.md. All predecessor files remain unchanged.

Main outcome: for odd N≥7, a fresh construction gives at most 2N−4 legal Fourier banks with every node and weight in Q(q). It supplies 10 at N=7 and 18 at N=11. It does not settle K-only attainment of the smaller accepted complex/splitting-field counts 8 and 14.

fresh_probe.py, fresh_small_search.py, and fresh_full_control.py are newly authored controls. They import only standard/SymPy libraries and this packet's own arithmetic helper; they do not execute or import predecessor programs. Run fresh_full_control.py in a writable copy, because it creates witnesses and receipts beside itself. Small search misses are bounded exploration only, never impossibility theorems.

Independent reviewer: research_cycle_1535/basefield_bank_review. Review status and any accepted source hashes belong to that reviewer packet; an author statement alone does not certify acceptance.
