# ALG-036: computable nondivisible Gaussian gap

22 October 2026 UTC. **Accepted for the computable positive compact-interval gap child gate only.** ALG-036 remains **TO RESEARCH, priority 34**.

For fixed integers `1 <= d <= N` with `d` not dividing `N`, and rational `0 < r0 <= r1 < infinity`, the proof specifies a terminating rational algorithm returning `gamma > 0`. Uniformly over every rank-`d` complex orthoprojector `P`, every translation `b`, and every `r` in that interval,

    Pr(||CN(0,P)-b||_infinity <= r) <= (1-exp(-N r^2/d))^d-gamma.

Read the unchanged [proof and complete algorithm](candidate/PROOF.md), the [independent review](review/REVIEW.md), and its [bound verdict](review/VERDICT.json). Proper-complex Gaussian normalization and complex-modulus constraints are essential. Acceptance relies on the stated previously accepted centering, equality and compactness results. [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) identifies immutable source copies. Relative links inside those historical copies retain their original repository-relative meaning; follow the original source URLs in SOURCE_BINDINGS.json for their optimizer, comparison, or other dependencies, which are not republished here.

The construction uses finite rational projector nets and rigorous integration. Its very large cell-count bounds are not bounds on full bit runtime or rational-accumulator growth. No practical algorithm, useful analytic rate, numerical gap run, or general maximizing projector is claimed. Changing-dimension refinements, efficiency, information-model and attribution questions remain open. The completed `N=3,d=2` optimizer is not reopened.

The candidate and review directories are byte-preserved records. Candidate-at-creation labels and statements that their authors had not published or edited a table are historical, not current publication status. The accepted verdict supersedes the candidate's pending-review label only for its exact proof hash and narrow contract. This package records mathematical acceptance, not execution of a native table edit or completion of the parent owner.

No executable implementation or numerical output is supplied for this proof-only result. [SHA256SUMS](SHA256SUMS) covers the actual bundle, excluding itself; each inherited checksum list retains its own directory-relative meaning.
