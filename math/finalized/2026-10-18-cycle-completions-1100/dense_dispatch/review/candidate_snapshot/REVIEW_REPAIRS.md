# Review-requested repair

18 October 2026 UTC.

The independent reviewer correctly identified that set(raw) preceded a dictionary-length guard. An arbitrarily large malformed dictionary could therefore cause an unbounded key scan before a constant-cost grammar rejection.

The repaired parser checks exact built-in dict type and len(raw)==4 first, then exact string key types, then the four-key set. A fresh 10,004-key malformed input is rejected before any arithmetic record, coordinate visit, coefficient preparation or output. The complete new-reference suite was rerun after this production change. The final manifest and CHECK_RESULTS.json bind the repaired bytes; the prior seal is superseded.

The reviewer also noted that a strict relative-error inequality cannot hold for zero input. The displayed theorem now uses a non-strict inequality for all inputs and states strictness only for nonzero input; zero remains exact. This is a prose clarification only. A second reproduced blocker was ordinary Python reflected equality: a Result subclass or integer subclass could return True from __eq__ and make an incorrect supplied result compare equal. Verification now uses exact-type recursive comparison against the trusted recomputed shape, with tuple/string length and integer-bit-length guards before content traversal or equality. Visited nodes and scalar operations are charged. Fresh probes reject both lying subclasses and an oversized result tuple without unbounded traversal. The full original-source replay is still paid for each probe.

The initial production repairs were the length-first/key-type parser guard and the strict expected-tree comparator with its comparison ledger. The zero-input inequality clarification changes prose only. No external write occurred.

A final wording clarification states that all dense coordinates are visited while an immutable equivalent original is retained as nonzero tuples and implicit zeros; it does not say that zero-pair objects are copied.

## Final failed-prefix accounting repairs

The new comparator could exhaust its separate arithmetic cap after replay completed. Previously its exception retained only the terminal comparison receipt. Rejected now has an immutable prior_receipts sequence; verify preserves the completed replay receipt there and keeps the terminal failed comparison receipt separately. Fresh controls at comparison caps 12, 16, 24 and 32 sum both work/storage receipts and verify that neither is dropped or counted twice. A constructor-bypassed exact Result with missing fields is also a typed RESULT_TREE_GRAMMAR rejection with the completed replay receipt retained.

The reviewer also identified pre-limit abs calls on negative metadata and components. These now use exact-int bit_length directly, and the computed small width integers are themselves charged before testing the limits. Two-million-bit negative F/component controls check paid rejection without a large pre-limit copy. The added width records change successful arithmetic counts; the cap controls use the repaired counts.

Only these review-requested failed-prefix/width fixes and their proof, ledger and fresh controls were added after the previous seal. The complete fresh suite was rerun before the replacement seal.
