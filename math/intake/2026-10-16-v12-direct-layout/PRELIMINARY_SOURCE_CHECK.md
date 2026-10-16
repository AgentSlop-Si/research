# v12 direct-layout intake: preliminary source check

16 October 2026. Status: queued for independent review; no table acceptance, new theorem ID, novelty rank or FFT-speed claim.

## Material inspected

The user's Library documents named `subnlogn_AUDIT_V12_2026-10-16.md` (112 extracted lines) and `subnlogn_DIRECT_LAYOUT_PROOF_V12_2026-10-16.md` (196 lines) were read in full through the Library connector. This is an extracted-text inspection, not a byte-level validation of the complete ZIP. The source conversation is https://chatgpt.com/c/6ad1012e-f904-83ed-8818-ea45fcdf0dc0 . No supplied program or test suite was run here.

## Independently inspected primary clauses

Pinned repository `openai/math`, revision `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, under `preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/`:

- [04-swap.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/04-swap.tex), Git blob `951e792b1768e6509561380b8bbfb1d1ccb64c08`: its arbitrary-width interchange lemma explicitly permits arbitrary prefix, gap and suffix lengths, includes padding and cleanup, and states a gap-independent O(V u^tau) bound under the preceding fixed-network construction. Its final paragraph supplies the unequal-width-by-one-bit construction.
- [07-resampling.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/07-resampling.tex), Git blob `256243bf9416baefb82bf9203f80215b9ebe28f2`: the tensor interface keeps the full padded box, whose axis widths differ by at most one bit. Its proof uses adjacent exchanges to expose and restore each axis, giving O(d^2) exchanges.
- [08-assembly.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/build/sections/08-assembly.tex), Git blob `337810a1d9a58a2ecf14123420923c039ba322a6`: the CRT reversal and cost table likewise use the adjacent O(d^2) schedule. Other transform-layout and arithmetic costs are explicitly separate.

These three exact source texts were retrieved through the GitHub connector. Reading their statements does not independently verify every imported rank-saving, numerical, uniform-construction or fixed-tape proof.

## Preliminary inference

Conditional on the inherited arbitrary-gap swap contract, reversing d coordinate fields by mirrored pair swaps needs floor(d/2) calls. Exposing an axis by exchanging it with the final axis, applying the same line map, then undoing that exchange needs two calls per nonfinal axis. The logical axis order can remain unchanged. Because the original interface retains the full padded box, all swapped widths continue to satisfy the equal-or-one-bit-different requirement. This supports the claimed local schedule reduction from O(d^2) to O(d), with cost O(V d(1+ell^tau)). It does not yet certify the supplied implementation, all descriptors, arbitrary stateful numerical routines or full composition.

The user's certificate reports conditional kappa approximately 7.3759e-27 instead of 3.2051e-37. Those numbers and the complete seven-margin certificate have not been independently recomputed in this intake. Their ratio is an exponent-saving ratio, not a measured product speedup. Reported finite timings concern layout only, on a no-saving control circuit. N denotes integer input bits, not arbitrary complex DFT length.

## Required next evidence

Independently check actual direct-axis code, unequal-width descriptors, arithmetic-order preservation, all exact parameter margins, and the full composition/precision/storage/control obligations. Bind the exact package bytes before any code replay. Confirm whether the scheduling substitution has already appeared in prior work before asserting novelty. Keep inherited primitives and full-framework saving credited to their sources.

A new independent-worker launch for this intake returned `agent thread limit reached`. It was not retried through another worker or route. This note preserves the source finding while current table finalization continues; it grants no global algorithm acceptance.
