# Independent scientific rationale

Publication excerpt of the final independent review. The scientific scope decisions are retained; operational preflight and application instructions are omitted. Exact source and export hashes are recorded in PUBLIC_PROVENANCE.json. Actual application remains separately verifiable.

## Scope decisions

### ALG-045: accept the exact named record after historical-source reconciliation

The original constructor is exactly 14,893 bytes, SHA256 f95505c0b0f3749d0ae218bb38e708c5eee0ac3b669f4958e63e42a8dd283c90. Its Sections 1–6 remain accepted with supplied primitive root, genuine monomial actions and nonzero calibration seed; the normal form is necessary, and preparing opaque actions is not free.

An important cross-bound source resolves the apparent Sections 7–8 acceptance gap. The original independent report SHA256 dd4adebbde308f21a3fa5167fe211e689201c37b65b50ebb2207e33f305f6a35, encountered through M-FOURIER4-GREEN, expressly accepts those sections and supplies the correct P-transpose orientation and carry formulas. Thus finalization must be described as recovered historical acceptance plus a fresh source/proof check, not discovery of previously unproved statements. Its matching-mask corollary retains zero connecting edges and fixed radix; it does not provide a fully nonzero global-cycle lift.

For Section 7, each nonzero partial monomial bank block becomes a block having no zero row or column after Fourier conjugation. A block of a global monomial matrix can then have exactly one entry in each row/column; rank preservation makes the original block full monomial. Global support forces a permutation of whole banks. The entry cross ratio yields kj=(tau(k)-tau(0))(pi(j)-pi(0)) modulo m. At m>1, k=j=1 forces unit slopes, proving affine permutation/character weights, including composite m. The m=1 case is trivial separately.

For Section 8, let N=Lc and define the high-digit partial transform H_c[(s,t),s+Lr]=zeta_c^(rt). Its clock conjugate sends (s,t) to (s,t-1), weight omega^s. Its shift conjugate advances s, with the wrap s=L-1 to 0 contributing weight zeta_c^t. This proves monomial actions uniformly, including carries. Q is an output monomial times H_b with L=am. P^T, rather than P, is an output monomial times H_a with L=bm. Expanding the single bank path gives the exponent kj modulo N, so the bank identity is algebraic for all compatible positive digit sizes, not extrapolated from tests.

The source's ambiguous assertion about P itself must be explicitly corrected. Fresh exact arithmetic at a=m=b=2 over GF(17), omega=2, gives row zero of P S P^-1 as [0,0,0,8,0,0,0,10], which is not monomial; all required Q and P^T actions pass. Seven fresh exact cases include mixed composite digits and the N=1 matrix identity. Exactly two paired zero-mask layers per exterior require a,b in {1,2,4} and characteristic different from two; this is automatic for dyadic N>=2 but not for N=1 over GF(2). The q<=16 row-support bound is only for the four zero-mask exterior layers. Costs remain (N/a)T(a)+(N/m)T(m)+(N/b)T(b)+O(N) with supplied-root preparation and genuine action/calibration access charged. No growing-radix speedup, unrestricted converse or new discovery-priority conclusion follows.

### M-TWO-SIDED-GAUGE: accept exact obstruction/metric/edit record

Read the entire source THEOREMS.md, SHA256 4223eddb30efb4ab03e48566cfc9268534f69a94e15074984107c39b037c04f8, and bind exact REVIEW-14 outcomes SHA256 2e6916f633ab40159e17bbe93724b0e8db4d677beb8bc2a62981093de8ef204d. The whole named record includes the paired monomial normalizer, even s>=4 exact obstruction, unitary-gauge spectrum and metric floors, fixed-gauge Frobenius projection, and legal occurrence-wise rank/edit barriers. Section 9 is included.

The exact obstruction permits arbitrary invertible diagonal gauges. Metric and uniform approximation claims require complex unitary gauges. The Gram matrices have the form I+rho X and I+rho Y, with commuting involutions X,Y and four one-dimensional joint eigenspaces; their product has eigenvalues (1+rho)^2, (1-rho)^2 and 1-rho^2 twice. This proves the spectrum uniformly. Fresh rational determinant controls check 35 evaluations, and half-grid affine tests retain s=2 as the sole tested exception. Generic N/2 defect counts must not be promoted to all-gauge claims. Every old/new inverse used in rank telescoping must exist. Curvature-bearing construction outside the reference grammar and Q19 implementation are distinct open work; this closure does not close them, establish sharpness, or imply an FFT time lower bound.

### M-FOURIER4-GREEN: accept two distinct local N=4 kernels

Bind full original review bytes dd4adebbde308f21a3fa5167fe211e689201c37b65b50ebb2207e33f305f6a35 and 6b83dab44ee74f9cd3c905a2b16b78d38a208a7ed5efffcc4430428e098cd88a, plus REVIEW-09 outcomes ba735868bf0ae1771e53477f36d400908c492a3c79251d6c400bf573846554b1. This is closure of the local kernel record, not its global batch lift.

The positive-sign cyclic kernel requires a primitive eighth root and both distinct roots of z^2+(chi+chi^-1)z+chi^2. Its interpolation, nonzero endpoints and product of Green guards 8i are explicitly checked in the accepted proof; splitting and distinctness cannot be inferred from the primitive root alone. The separate negative-sign Phase16 certificate has two four-Green sums and exactly twelve zero mask occurrences. Its exact quadratic-tower eight-inverse certificate has SHA256 a8dc28b9b33c5df50e40cd120ea645a0e803ea0193d1cedad93b639b8731238b. The accepted checker was replayed in isolation for this finalization. The independent reviewer inspected the proof/certificate scope and does not claim an additional historical-code replay. Opposite signs, differing topologies and local-versus-global cycles stay explicit. The sanitized published export is a distinct byte identity from the original review.

### M-SORTING-RANK: accept the named rank/probability theorem

Bind full RANK_AUDIT.md f574925a32279259f6e4a2eb1c1b1f438492da4c27757fc242e13065c2d515f6 and REVIEW-13 outcomes 945de212e3857492188c989cab35fd16ca896e6447076814a9244ff1ce2e58c9. The field-independent cycle identity, binary stable-sort rank distribution, N>=3 moments and clipped all-stride probability theorem are complete.

The proof rank(W-Z^a)=N-cycles(Z^-a W) works in every characteristic. T<=1 gives W=Z and zero changed edges, including mixed two-run words. The iid transition bijection proves the binomial law and moments; the all-stride argument uses disjoint-window Hoeffding estimates plus a long-stride first-moment union bound, not coprimality or an experiment. Its small-N analytic lower bound must remain clipped at zero. Fresh independently written controls pass 2,044 complete words for N=2..10 and 16,388 word/stride cases. These supplement the analytic proof. Independent all-stride screening costs O(N^2); high correction rank can still be easy to apply. No unnamed novelty search is a missing lemma of this theorem, and novelty is not certified by closure.

### PACK-01: accept one provenance-hold edit, reject closure

Next cycle K9 can name the exact missing acceptance archive and three hashes while retaining all former text. Filename and hash pins are not recovered bytes. Future closure must follow actual byte recovery, acceptance/source-binding checks and independent scope review. PACK-01 stays TO RESEARCH, priority 15; Q01, F132 and TH-01 remain unchanged. Repeating the refused eager build is not indicated.

### ALG-075: accept two orientation corrections, reject closure

Independently read the publisher abstract at https://epubs.siam.org/doi/10.1137/0205041. It directly concerns n-by-r times r-by-n with r<=log2(n) and n^2+o(n^2) multiplications; multiplication and division by two are required. The n-by-n times n-by-log(n) orientation needs an explicit transfer whose costs are charged. The abstract does not provide a verified addition circuit or uniform compiler. Correct Catalogue H181 and novelty L221 with a dated prefix, preserving the older text as historical. Original constructive text remains source-blocked and ALG-074 remains held.

### STABLE-ARC/F018: accept one stale-provenance correction, zero closure

The exact live F018 row 258 is already CLOSED at priority 15. Its C/P fields correctly record recovered original A1/A2 and full Phase26 comparisons; O still repeats the superseded two-missing-source statement. Accept a dated O258 clarification with the full old text retained. The published independent editorial derivative is 10,580 bytes, SHA256 38475c63a2d61fcf8ced744e2ea8150886ac352821df21353485438cdf8b9408. It explicitly binds and describes unchanged v2 theorem statements, but does not replace the missing exact manuscript 159ff2e8a081fbff81d977b023b3bce08561ded1b395dd0924a48df3e5802631. This correction adds no theorem, source-byte recovery or novelty claim.

### Q34/NF-06: retain source gates and broader parents

The additional source-gate report explicitly makes no cell-change or closure proposal. Its 18 record/arithmetic checks only establish consistency of current pins and copied decimal Banach bounds. They do not recover or replay the original interval certificate, Jacobian enclosures, guards or checker. Preserve Q34 TO RESEARCH at 22 and NF-06 TO RESEARCH at 37. In particular, the corrected current record says no separately evidenced sealed-extraction reviewer cold replay is claimed. The bounded accepted existence theorem does not close the broader synthesis/minimum-q/cost record.

