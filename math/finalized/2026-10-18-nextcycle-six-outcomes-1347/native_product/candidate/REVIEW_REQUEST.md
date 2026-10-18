# Independent review request

Review the new modular-output interface and two specifically scoped barriers. Do not promote them to a general fast multiplier or a lower bound against correlated products.

Priority checks:

1. `shift_mod`: target precision H, internal H+g, arbitrary residue representatives, exact two odd divisions, and returning unsigned canonical residues without an exact-height premise. Confirm the copied helper is byte-identical to the accepted source.
2. Product contract: ordinary linear convolution modulo the specified power of two, all 2L-1 outputs, T_- homomorphism, strict final nonnegative coefficient bound, and binary carry/output costs.
3. Grouped contract: H_d applies to canonical p^d input values; it does not apply unchanged to unnormalized redundant groups. Actual canonical extra digits, partial groups, and d encoding must remain paid.
4. Odd native residue mismatch: a result modulo an unrelated odd modulus cannot merely be masked to fulfill the 2-adic service. Exact reconstruction or another proved bridge is needed.
5. Two-wide schedule: precisely q(q+1)/2 calls, no missing low-order cross-limb pair, all output coefficients, bounded carry with the preexisting output limb included, row-terminal discard only at position q, and the partial last limb.
6. Packing widths, argument capacity, data movement, setup, memory, and optional address supplement. No repeated full-width shift/accumulation may be silently charged as a bounded window.
7. Optimization barrier: only a homogeneous Karatsuba charged expression for this prescribed pair recipe; actual data-dependent code does not have a proved universal Theta(w^alpha) running time.
8. Native potential: prove s'>2d and s'>=K, preserve rounding, sum s log s over a finite fully expanded tree, and distinguish growing-m linear leaf volume from the separately assumed charged Karatsuba leaf cost.
9. Confirm the negative controls and complete products independently. Test counts are finite correctness evidence, not complexity proof.

Run `python fresh_controls.py` and `python verify_package.py` in this package. Read REPORT.md and the pinned dependency review before assessing the inherited converter. No external writes are requested.
