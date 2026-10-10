# Independent review of the q-linear recurrence evaluator

Reviewed `qlinear.py`, `run_audit.py`, the exact field helpers, the current
README and saved results. The acceptance theorem, Fourier identity, cyclic
solver and singular recovery are correct within the stated adaptive exact-field
model. No unresolved mathematical or implementation issue was found. This
review does not claim an arbitrary-input FFT improvement.

## Discovery and source boundary

The streaming elimination is a valid four-column echelon computation. Newly
inserted pivot rows are normalized, previously occupied pivot columns are
eliminated, and sorting at most four rows preserves pivot order. Reverse
substitution with one free coordinate set to one returns a nonzero null
vector. Rank four allows an immediate sound decline; otherwise all N-1
relations have been read. Thus discovery accepts exactly the stated
nonzero-quadruple family, including zero coordinates and degenerate
coefficients, in linear work.

The constructed L retains its cyclic endpoint. Computing all of Lx and
checking the first N-1 entries leaves exactly the potentially nonzero last
coordinate. Its Fourier transform is `residual[-1]*q^(-k)` for every output
k, with no transform hidden in the forcing construction.

The conjugation has the correct order and phases. Writing D=diag(q^i) and
S for the forward cyclic source shift, F D shifts the Fourier row forward,
while F S multiplies row k by q^(-k). Consequently F D S has coefficient
q^(-k-1) on the forward target shift. This gives exactly the two implemented
bands `p0+r0*q^(-k)` and `p1+r1*q^(-k-1)`.

## Cyclic solve and the singular coordinate

For any nonzero coefficient quadruple, a nonzero degree-one band has at most
one zero on the distinct q-powers. If the upper band is not identically zero,
rotating the path to begin after its zero (if present) makes all N-1 forward
divisors nonzero. The affine representation `alpha_i*t+beta_i` then satisfies
every path equation. The final coefficient and right-hand side in the code
are precisely the remaining cyclic equation. They either determine t or
return a particular solution with one nonzero kernel vector. This proves
the nullity bound rather than assuming it for arbitrary sparse matrices.

If the upper band vanishes identically, the remaining nonzero degree-one
diagonal has at most one zero and the direct diagonal branch is correct.
Both bands cannot vanish identically without the parameter quadruple being
zero, excluded by construction. These arguments apply separately to L and J.

When J is singular, L is singular with the same one-dimensional nullspace
dimension because F is invertible. The independently computed source kernel
v and target kernel h satisfy h=c Fv for a nonzero scalar c. Choosing j with
v_j nonzero therefore gives

    sum_k q^(-kj) h_k = N c v_j != 0.

The denominator used for the missing-coordinate correction is nonzero. The
same weighted sum of the actual target must equal N*x_j, so the formula for
the correction parameter is exact. It preserves the target equations and
fixes their unique missing degree of freedom. No full inverse DFT is called:
only two explicitly charged N-term weighted sums are used. The supplied
primitive root ensures N is nonzero in the field.

## Costs, storage and verification scope

The following exact counts were independently derived from the loops:

| Stage | Field operations |
|---|---:|
| Root powers and dyadic order validation | N |
| Source/target bands, full residual and forcing | 12N |
| Nonzero-edge nonsingular cycle solve | 9N-1 |
| Nonzero-edge singular cycle solve | 7N-3 |
| Singular source-kernel solve and input constraint | at most 13N+2 |

Diagonal cycle branches cost 2N or 2N-2, and their extra singular recovery
costs 8N+3. The four-column elimination adds O(N) operations and at most
four pivot inversions. All root, source, target, kernel and output arrays
have O(N) length, while discovery keeps at most four rows. Word comparisons,
array construction, indexing and full output writes add O(N) work. There is
no per-output reconstruction hidden behind a small state descriptor.

A focused independent check matched the saved exact stage formulas for all
356 named-fixture ledgers; no functional audit was rerun for this review.
The source audit also compares all its accepted random controls with a
dense DFT oracle. Its final update additionally wraps every random accepted
and declined call in the outer arithmetic counter, with the same passing
380-output/60-decline totals. The saved finite certificates check the implementation;
the identities and loop bounds above establish the all-length conditional
result.

All inversions, including input-dependent discovery and solver inversions,
are paid in the declared adaptive rational model. Exact equality tests and
integer embeddings have the documented model scope. This is not a fixed
input-independent linear circuit, a bit-cost bound for cyclotomic tuple
arithmetic, or a stable floating-point algorithm.

The degree-one P/Q family is an additional useful class, not automatically
a strict superset of every earlier scalar-lambda E-defect family: the generic
E upper coefficient has degree two in q^i. The zero-shift E relation does
cancel a common factor and belongs here. Geometric sequences and chirps also
fit directly. This distinction does not affect either algorithm, but avoids
overstating coverage when combining the checkpoints.
