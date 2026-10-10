# Final review checklist

- Confirm source A is the corrected `c8a77523…fc8d` version, not the earlier interpolation manuscript; verify all four source hashes.
- Check the literal supplied domain `2 <= t <= ceil(log2(N+1))`, charged precision generation, total fast-branch test and separately priced higher-precision fallback.
- Check that the theorem states deterministic relative-l2 error for represented inputs, writes every output, and charges preparation and memory movement on the specified growing-word RAM.
- Check every hypothesis and all three channel terms in the composition lemma; no linearity of rounded backends or input preprocessing is assumed.
- Check the interpolation instantiation: output norm below 6, output perturbation at most `13 rho`, final rounding at most `3 rho`, total `22 rho`.
- Check Taylor's factorial/error ledger and preserve its weaker inverse-polylogarithmic bound; do not infer the full sublinear-precision theorem for Taylor.
- Keep the correction-rank statement representation-specific. Keep the exact Necklace–Green seed/intertwining construction open, with root, denominator, transpose and characteristic conditions explicit.
- Confirm the publication text contains no private account identifiers or private links; resolve all local source links. Preserve the original accepted artifacts and do not recount historical tests.
- Retain the final qualification: no new asymptotic improvement, production executor certification, practical crossover or historical novelty is claimed.
