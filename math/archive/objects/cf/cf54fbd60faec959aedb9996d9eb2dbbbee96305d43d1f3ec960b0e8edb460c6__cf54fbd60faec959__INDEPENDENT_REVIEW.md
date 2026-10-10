# Independent review of the tensor side-information evaluator

The parent researcher independently reviewed `tensor_sideinfo.py` and its
README after the subagent's focused audit. The certificate and full-output
recurrence are correct within the stated field/ring and supplied-root model.

The pivot-neighbor ratios determine the only possible normalized tensor with
the proposed pivot and scale. The doubling tree generates precisely every
subset product, and comparison at `pivot xor mask` checks all N input
coefficients. Zeros among factors are handled correctly. A nonunit pivot in
a composite ring is explicitly rejected; arbitrary nonzero field pivots are
units. A manually forged certificate is outside the stated trusted-internal
certificate contract.

Expansion of the certified generating polynomial proves the Fourier formula.
At level l, the remaining suffix depends only on frequency modulo
2^(d−l−1), which justifies the shared lookup. The sizes sum to 2N−2; all N
final outputs are materialized. The supplied-root half-power check establishes
a principal dyadic root in an odd residue ring, not just exact multiplicative
order. Every used root power is explicitly prepared.

The arithmetic ledger is consistent with the emitted loops: d factor
multiplications, N−1 regeneration products, d−1 root-check squarings,
N−1 root-table products, and 4N−4 evaluation products total
6N−7+2d for nonzero accepted inputs N≥2. Evaluation adds 2N−2 additions and
factor discovery pays one inversion. Validation, equality checks, input/output
traffic, indices and field operand widths are separately charged. The code
does not invoke a hidden FFT or multiplication macro.

The complex stability theorem uses a maximum-magnitude pivot, whereas the
implemented exact modular algorithm uses the first nonzero pivot. This
distinction is essential and correctly documented: first-nonzero ratios
are not bounded for arbitrary complex or rational inputs. With the stated
bounded factor errors and no overflow/underflow, the telescoping-product
bound is polynomial in N. The optional l1 residual certificate follows
directly from the triangle inequality and is correctly marked unimplemented.

The accepted class has only O(log N) free complex parameters and contains no
N-dimensional open set. It therefore does not defeat the global bottleneck
theorem or give a general arbitrary-input FFT improvement. The finite exact
audit is appropriate evidence for the implementation; the all-size recurrence
and complete verification procedure supply the mathematical proof.
