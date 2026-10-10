# Independent proof capsule — all rank cuts vacuous, algebraic codimension four

**Mathematical claim (scoped)**: Let `n=8`, `p=[7,0,6,3,4,1,2,5]`, and write `M=B P A`, where both `A,B` belong to the **rank-one separated-generator semiseparable chart**

```
S[i,j] = L[i]*V[j] if i>j
S[i,j] = d[i]      if i==j
S[i,j] = U[i]*W[j] if i<j.
```

Then the **scalar-signal graph** for this two-stage architecture has `c_G(R,C)=min(|R|,|C|)` for *every* row and column subset, while the Zariski closure of the **actual complex output matrix family** has dimension `60`, strictly less than `64`.

## Proof of unrestricted graph capacities

The graph is constructed in `prior_checkpoint/scan_flow.py` with input/output wire capacity 1, forward/backward register capacity 1, infinite-coefficient links, and permutation `p`. `superconcentrator_gate.py` independently checks with exact integer Dinic maxflow

```
for k=1..8:
  for all C,R subsets of {0,...,7} with |R|=|C|=k:
      assert maxflow(R,C) == k
```

There are `sum_{k=1}^8 binomial(8,k)^2 = 12869` loop iterations. The zero-size case is trivial. For arbitrary cardinalities `|R|≠|C|`, choose equal-cardinality subsubsets of size `k=min(|R|,|C|)`; flow cannot *decrease* on enlarging terminal sets, and it cannot exceed `k` because each boundary wire has capacity 1. Thus equality holds for all subsets. The machine-checkable certificate `superconcentrator_N8_certificate.json` also specifies the exact permutation, check counts, and 32 NetworkX cross-checks.

## Proof of complex algebraic image upper dimension

The strictly lower rank-one generator chart has `n−1` row factors and `n−1` column factors and is invariant under one nonzero scalar rescaling, so its dimension is `2n−3`; the upper chart is independent and contributes the same, the diagonal adds `n`. Therefore a single stage chart has dimension `5n−6=34` at n8.

The product map `(A,B)↦B P A` has an **8-dimensional** generic orbit that leaves its output fixed:

```
A -> D A
B -> B P D^-1 P^-1
```

for every invertible diagonal `D`. The generic orbit is free, so the complex algebraic image has dimension at most `34+34−8=60`.

## Proof of matching complex algebraic lower dimension

`superconcentrator_N8_certificate.json` stores a concrete deterministic integer parameter point (seed 1011), the `60` selected rows and columns of its full `64×80` Jacobian, and the exact residue

```
det(J[stored_rows,stored_columns]) == 4779 (mod 12289),
```

verified by `python superconcentrator_gate.py`. Because the determinant is an integer polynomial evaluated at integer coefficients, nonzero reduction modulo the prime **implies nonzero determinant over Q and C**. Thus the complex polynomial map has differential rank at least 60 somewhere, so its image has dimension at least 60. Combined with the proved upper bound, the dimension is exactly **60**, codimension **4**.

## Logical consequence, and boundary

For **every** matrix target `T`, all tested graph inequalities `rank(T[R,C])≤c_G(R,C)` are trivial. But a 60-dimensional algebraic closure cannot equal the full 64-dimensional matrix space. Consequently nontrivial polynomial equations are necessary to distinguish the generator image from generic 8×8 matrices. This rigorously proves **min-cut completeness fails** in the given generator chart.

**Not implied**: no explicit polynomial is given; the 8×8 Fourier matrix may lie in the 60-dimensional image; nothing here proves an FFT upper or lower arithmetic bound or excludes exceptional quasiseparable charts.
