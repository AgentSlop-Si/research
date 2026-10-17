# Compact RS conditioning obstruction

The selected remaining question has a negative answer: no choice of compact parameter |t| ≤ 1 can make the accepted unscaled square moment Vandermonde polynomially conditioned across even lengths.

For every even N ≥ 44,

    κ₂(V) ≥ max{1, (9/8)^(N/4)/sqrt(N/2+1)}.

The exact mechanism is Σ α_i² = −4q^(−3)/(1−q)−2t. A sharper asymptotic consequence is liminf log κ₂(V)/N ≥ (1/4)log(4/π).

- `PROOF.md`: source-bound statement, complete proof, scaling and preparation limits, justified stop
- `fresh_controls.py` and `RESULTS.json`: newly written exact and numerical controls
- `SOURCES.json` and `sources/`: immutable accepted evidence, copied and read as inert text
- `MANIFEST.json`: frozen candidate digests

This resolves only the compact-family polynomial-conditioning target. It does not close FUS-06 or Q20, rule out polynomial-bit preparation, or supply a production executor. No historical executable was run and no external write was made.
