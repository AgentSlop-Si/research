# Independent review of the direct target recurrence

Result: PASS. Root reviewed `extended_recurrence.py`, its claimed family,
all target branches and the cold ledgers, separately from the author audit.
No unresolved correctness or cost issue was found within the exact-field,
supplied-primitive-root contract. This is not a universal FFT improvement.

The source action and Boyer-Moore detector preserve the earlier verified
intertwining FE=JF. Removing the old zero/root tests is legitimate because
the new output solver supplies the missing input information explicitly.
For zero shift, the last coefficient in the cyclic first-order transition
vanishes, fixing its start value. For nonzero shift, the code propagates the
two affine coefficients through rows 0 through N-2, then enforces both
remaining cyclic endpoint equations. The known Fourier coordinate y0 is
the actual, paid sum of the fresh input.

When both scalar closure coefficients vanish, the propagated nonzero h is
a target kernel vector. Source triangularity gives a unique eigenvalue
index t with lambda=-q^t. Its source eigenvector has nonzero t coordinate,
so the inverse-Fourier coordinate functional used by the code separates h.
The weighted sums, root-index scan and normalization N are explicitly paid.
This correctly reconstructs nonzero outputs even when the verified defect
is zero. It is not valid to infer a zero answer from zero forcing alone.

Independent loop accounting gives target costs 4N-3 for zero shift,
13N-5 for ordinary closure, and 18N+log2(N)-3 for the exceptional constraint.
On the reported dense one-defect automatic workloads, the E action/root
table costs 6N-4, ratio comparisons 2N-2, and sparse forcing 2N-1. Zero
shift adds neither a candidate inverse nor residual subtractions, yielding
14N-10. Nonzero shift adds two candidate operations and 2N residual
operations, yielding 25N-10. These totals independently reproduce the
reported comparison entries. Inversions remain exact-field operations,
not free machine instructions or fixed input-independent constants.

The separate `independent_checks.py` exhausts all 625 vectors over F5^4 at
caps zero and one. An independently formed dense E matrix and enumeration
of all five possible shifts decide exact promised-family membership. All
1,250 input/cap pairs agree with the implementation: 214 accepted complete
Fourier outputs and 1,036 declines. The accepted cases include 32 exceptional
singular reconstructions, eight zero-shift scans and 60 ordinary cyclic
closures; sparse evaluation supplies the rest. Each output is compared with
the independently formed Fourier matrix. The JSON records the reviewed
implementation hash. This focused exhaustive check complements, rather
than duplicates, the author's larger field/size and operation-wrapper audit.

The exported low-level target scan assumes its forcing really is the Fourier
transform of the supplied source residual. The public evaluator constructs
that forcing itself. Primitive-root validity and consistent field encodings
remain preconditions. The primary API returns a decline for unsupported
dense inputs; it does not silently claim to have evaluated them.
