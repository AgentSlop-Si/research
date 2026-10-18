# ALG-070 persistent complete-view cache gate

This package resolves a restricted mathematical successor to the accepted single-view replay/rebase theorem. It realizes classical paging inside actual filtered-bilinear convolution requests while charging immutable raw versions, exact coalescing, complete materializations, persistent cache storage and requested output.

Results:

* With K complete-view slots, the optimal deterministic asymptotic materialization factor is K.
* LRU with K slots against h<=K offline slots has factor K/(K-h+1). Therefore 2h-1 slots yield a factor below two when h>1.
* With materialization tariff F and common per-request cost g, the lower bound for the whole declared tariff is (F+g)/(F/K+g), not automatically K.

The paging bounds are classical and explicitly attributed to Sleator–Tarjan 1985. What this package adds for ALG-070 is a precise convolution-view realization, paid version/coalescing interface, and full-cost boundary. Partial views, compressed answers, cross-view algebraic sharing, unequal build costs, cost-learning guarantees, unrestricted arithmetic algorithms, and production qualification remain outside scope. ALG-070 remains open.

Files:

* REPORT.md: complete model, proofs and scope
* check_cache.py: new exact standard-library verifier
* VALIDATION.json and REPLAY_OUTPUT.txt: executed finite checks
* SOURCE_BINDING.json: exact owner/source bindings
* source/: exact previous report and selected existing owner record
* MANIFEST.json: package file hashes

Run `python check_cache.py` from any working directory. This regenerates the validation receipts next to the script and performs no network or external writes. Finite checks corroborate the proofs; they do not establish a larger algorithmic lower bound. Independent review is a separate acceptance step.
