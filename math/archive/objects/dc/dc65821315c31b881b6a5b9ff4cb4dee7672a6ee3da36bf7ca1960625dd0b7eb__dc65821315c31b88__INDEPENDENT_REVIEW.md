# Independent review of the exact target-difference compiler

Reviewed 9 October 2026 against `terminal_anchor.py`, `run_audit.py`, the copied
`prior_affine_reuse.py`, and the README. No code changes or additional tests were
needed for this review; the existing full-state suite directly covers the
implementation risks. The general DAG extension is proved below rather than
represented as an implemented test result.

## Verdict

The chain compiler is correct for arbitrary source and target values, including
arbitrary dirty workspace. Its scalar operation counts and savings relative to
the previous first-target anchor are correct. It supersedes the earlier
reversible-anchor schedule for this sparse J: it uses one ADD_T, does not move
the original source through K, and does not require either J or K to be
invertible.

## Algebra and restoration

Write a_r for each target's initial value. Descending updates produce
`y_r=a_r-J*a_(r-1)`, with y_0=a_0, because the source bank r-1 has not yet been
changed. The injection gives y_0=a_0+T*P_S*x. Ascending updates then give

    y_r = a_r + J^r T P_S x = a_r + T K^r P_S x.

Thus all dependence on the targets' arbitrary starting contents is preserved
exactly as the identity. Targets receive their requested additions; they are
not supposed to return to their original values. The source x and unused dirty
bank w do return to their original values. The atomic word never changes x;
the scalar implementation temporarily scales and immediately restores source
coordinates. The existing whole-state basis audit also verifies these formal
coordinates, so its claim is stronger than a zero-workspace check.

For a general topologically ordered DAG, let L be its strictly block-lower
triangular edge operator. The descending pass computes `(I-L)a`; injecting b
and executing the ascending pass gives

    (I-L)^(-1) ((I-L)a+b) = a+(I-L)^(-1)b.

Since L is nilpotent, `(I-L)^(-1)=I+L+L^2+...` is a finite sum. This accounts
for all directed paths, including multiple parents and mixed paths. Individual
edge maps need not be invertible. The proof requires disjoint compatible target
banks, injections independent of the evolving target state, and transparent
edge/injection ADD implementations preserving source and borrowed scratch.
These assumptions are now explicit in the README. Cyclic dependency graphs are
outside this proof.

## Costs checked

The q-Weyl affine operator J has N nonzero cyclic edge entries and precisely
N-1 nonzero diagonal entries. Therefore ADD_J has 2N-1 shears. All emitted
coefficients are nonzero, and the selected scalar expansion uses three
instructions per shear. For support S, selected-column ADD_T has

    a(S) = sum_(j in S)(N-j)

shears. The total is exactly

    3a(S) + 2(R-1)(6N-3)

scalar instructions under this implementation convention. For dense S the
previous first-anchor count was `3N(N+1)/2+2(R-1)(14N-10)`, so the saving is
exactly `2(R-1)(8N-7)`. The documented dense examples check arithmetically:
2,718 instead of 4,212 at N=32,R=4; 8,526 instead of 11,556 at N=64,R=4;
35,478 instead of 49,716 at N=128,R=8.

The preparation wording has been clarified: the copied `prepare` executes
exactly 2N-1 inversions of input-independent constants, not a constant number
of inversions. Scalar expansion prepares additional cached reciprocals of
O(N) distinct nonzero coefficients. This remains O(N) field operations in a
model that explicitly counts inversion as a field operation; it is not O(N)
bit complexity. Root construction, support discovery/validation, program
emission, addressing, and full output materialization remain charged as stated.

## Scope retained

For dense arbitrary x, the implemented reference ADD_T still costs Theta(N^2).
Sparse selected-column counts implement the projected-source problem and
cannot be quoted as speedups on a dense source. The exact propagation of an
approximate anchor error is J^r e; no norm preservation is implied for this
nonunitary J. The result is an exact compiler improvement for related-input
graphs, with no fresh arbitrary-input sub-N-log-N FFT claim or novelty claim
for triangular elimination.
