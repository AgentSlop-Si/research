# Unpinned F23 singleton-bank gate

Declared 2026-10-14 01:21 UTC before the new computation.

Fix F23, N=11, q=13, original S/T and literal target F[k,t]=13^(-kt). Preserve the original bank formula and Delta!=0. Remove only the two alpha=4 pins; retain exactly one effective alpha node per cross-sign orientation, now independently variable. Do not claim a result for unrestricted orientation allocations.

Fresh standard-library code will derive target coefficients and Gaussian factors, then derive all positive-exponent central moment windows b=1,...,5 for each of the 22 possible nonzero minus-plus singleton alphas y. Zero y is excluded by the sole-support coordinate (a,b)=(10,1).

Exact finite census: for each y, solve the monic degree-five common-annihilator equations (four length-six windows in b=1 and two in b=2), and the monic degree-six equations (three length-seven windows in b=1 and one in b=2). Enumerate all solutions over F23, stopping with a reported blocker if any affine family dimension exceeds three. Evaluate every obtained polynomial at all 22 nonzero field elements. Retain sextics with exactly six distinct nonzero roots. This tests a necessary gate, not full-bank sufficiency. The quintic census, with ordinary-node padding, gives a pin-independent singleton lower bound if no admissible quintic exists.

Candidate full solves use all retained records (y,X). Test pairs in this order: each record paired with itself, then all unequal ordered pairs lexicographically. For a pair (y,X),(z,Y), use original orientation allocation (6,1,1,6) with ++ support X, -+ node y, +- node z, -- support Y, all beta=1. Solve all eleven original coefficient sectors exactly. Stop at the first full legal witness or after every declared record pair. No failed partial search becomes a nonexistence claim outside this exact family.

If a witness exists, recover all raw weights by inverse character transform; build and invert each original branch matrix independently of the coefficient expansion; check both inverse products and all 121 original target entries; verify all banks nonzero. Save the witness, complete census, source hashes, timing and errors, and perform cold replay. Run only newly authored code. Read all historical code and data as inert sources; no imports, compilation or execution. No external writes or novelty claim.
