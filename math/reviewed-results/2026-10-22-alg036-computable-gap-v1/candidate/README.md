# All-size computable nondivisible Gaussian gap

The proof in [PROOF.md](PROOF.md) gives an explicit terminating algorithm that takes fixed integers `1 <= d <= N`, with `d` not dividing `N`, and rational `0 < r0 <= r1 < infinity`, and returns rational `gamma > 0` satisfying

    Pr(||CN(0,P)-b||_infinity <= r)
      <= (1-exp(-N r^2/d))^d-gamma

for every orthogonal rank-`d` complex projector `P`, every translation `b`, and every `r in [r0,r1]`. The Gaussian is proper complex with density `pi^(-d)exp(-||g||^2)` in standard coordinates.

This is a generic effective-compactness certificate. It closes computability, conditional on the accepted centering/equality/compactness dependencies and separate acceptance of the present proof. It is not a useful analytic gap rate or an efficient numerical method. No full-search numerical run is claimed.

The construction uses exact rational projectors from rounded frames, a uniform annulus estimate valid at zero leverage, certified integration in real dimension `2d`, explicit Gaussian tails, and outward rational scalar enclosures. Stage `k` returns a sound rational lower bound `gamma_k`, and proves `gamma_k >= Delta-5*2^(-k)` for the positive compact-interval minimum gap `Delta`. Thus the positive stopping test eventually succeeds without knowing `Delta`.

General maximizers, changing-dimension critical-window rates, efficiency, adaptivity, information models, block-local constructions, historical novelty, and complete attribution are not resolved. The `N=3,d=2` optimizer is already closed and is not rerun. ALG-036 remains TO RESEARCH, priority 34.

Status at creation: candidate submitted for separate verification. This directory contains no claim of independent acceptance, external publication, repository commit, or native spreadsheet edit.
