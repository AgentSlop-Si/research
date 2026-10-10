# Hero #1 — Phase 27 research gate

Phase 26 rules out three misleading shortcuts in **specified** models: ordinary split radix merely changes topology at identical prime-field scalar cost, a basic nonunitary butterfly LDU lift adds operations, and black-box high-arity unitary/complex bounded-entry gates can hide their required mixing/volume toll. These are **not** universal impossibility results.

## Primary target: exact scalar circuit outside the charged models

1. Specify the computation field **before** optimizing: complex arithmetic (with accuracy/bit precision), prime-field operations (with field characteristic/prime growth), or word-RAM bit operations (with word size). Never combine bounds from incompatible models.
2. Synthesize an independently checkable `b×b` local Fourier or Green-mixing kernel for `b=8,16,32` that uses fewer actual scalar operations than the strongest legal reference for that field; count all additions, multiplications, coefficient setup, data movement and stored intermediate words. A black-box `b`-input operation counts as zero progress until expanded.
3. Prove a genuinely lower leading coefficient of `N log N` for a growing hierarchy **or** produce and verify a uniform `o(NlogN)` scalar bound. Local constant savings are useful but should not be relabeled as a breakthrough.
4. When attempting **linear gate count** with bounded arity over complex numbers, face the determinant-growth constraint: if `G≤aN` and `b≤B`, then any exact unnormalized Fourier factorization must use some coefficient with magnitude at least `N^(1/(2aB))/√B`. Supply an explicit coefficient-height and precision/conditioning ledger when exceeding constant magnitudes.
5. For a large-arity **unitary** circuit on `N` registers and no workspace, the entropy budget `sum_g b_g log2 b_g ≥ N log2 N` must be met. Explain how charged scalar operations inside a large gate supply its entropy change.
6. Keep the structural-input Green certificates from Phases 17–24 separate: they do not compress generic dense inputs, and a correct fallback's `Theta(NlogN)` work must stay in the worst-case bound.

## Highest-value cross-graph candidate

One possible research problem: find a genuinely input-independent, nonlocally shared linear circuit for `F_N P_N` where `P_N` and `P_N^{-1}` are both cheap, that is **not** Fourier conjugation or a standard recursive FFT with hidden costs. Check the entire Fourier basis and exact graph size before interpreting the candidate. Phase 16 shows cheap sparse Green inversion alone is insufficient. Phase 25 shows the pairwise unitary circuit is already gate-optimal under its restrictions.

## Avoid repeating these dead ends

- Split-radix without a separate field-optimized codelet: exact same field-operation count as optimized radix-2 in the audited recursion.
- Elementary unipotent LDU shears: a paid scalar diagonal operation increases, not reduces, work in the butterfly trial.
- Treating one giant block Fourier transform as one operation: such counting changes the operation model, not complexity.
- Borrowing numerical real-FLOP savings of classical modified split radix and relabeling them as prime-field multiplication savings.
- Reporting a saving versus Bluestein on power-of-two lengths instead of optimized radix-2 or native Good–Thomas.

**Research standard:** exact theorem + executable circuit + independent full-basis field checks + input-independent worst-case scalar accounting + cold-setup and workspace + prior-art distinction. Phase 26 does not establish a new unrestricted FFT asymptotic upper bound.
