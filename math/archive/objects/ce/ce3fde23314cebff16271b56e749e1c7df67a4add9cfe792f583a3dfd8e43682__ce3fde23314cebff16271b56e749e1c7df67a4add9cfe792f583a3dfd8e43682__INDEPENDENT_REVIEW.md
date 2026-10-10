# Independent review of the full-prefix surrogate planner

**Verdict:** PASS for deterministic selection, minimization of the implemented
numeric objective, and surrogate-construction mechanics. The implementation
faithfully addresses the corrected derivation's planner requirements. It does
not certify the mathematical probability bound in floating point and does not
itself implement the final full-output Fourier transform.

Reviewed `prefix_planner.py`, `run_audit.py`, the README, and the supplied
`research_inputs/surrogate_corrected/DERIVATION.md`. Source hashes and targeted
independent check results appear in `independent_review_checks.json`.

## 1. BFPRT is genuinely deterministic linear selection

Selection keys are pairs `(-computed_magnitude,index)`, so they are distinct
even when magnitudes tie. Groups contain at most five entries and use bounded
insertion sorting. The pivot is recursively selected from the group medians,
then the algorithm partitions around that pivot and recurses on only the
relevant side.

Except for the final short group and constant rounding effects, at least
three entries from each of at least half the groups lie on either side of
the pivot. The retained partition is therefore at most 7n/10+O(1). This gives

    T(n) <= T(ceil(n/5)) + T(7n/10+O(1)) + O(n) = O(n)

in the comparison/RAM model. The final scan collecting all keys up to the
cut key is also linear. Only the selected H entries are sorted afterward.
If H=m, sorting every nonzero is correctly charged by the H log H term;
if H=0, selection is skipped. The full bound is O(N+H log(H+2)), not O(N)
for every arbitrary user-specified H. The default polylogarithmic H makes
this O(N) asymptotically. Constantly many linear preparation/validation
passes should not be described as one literal memory read of each input.

This is not a bit-operation bound for Python `Fraction` arithmetic, gigantic
integer budgets, or arbitrary-precision indices. The README correctly states
that distinction. The implementation's list allocations remain O(N) live
storage in the declared element-count model.

## 2. Full-prefix objective and discontinuity

Every prefix from zero through the clamped cap is evaluated. Residual mass
is formed from exact sums of the already computed floating-point magnitudes.
The branch `residual <= epsilon*total` includes equality and sets the budget
to zero; otherwise a rational ceiling implements the numeric sample budget.
Each candidate's support objective is min(m,s+k).

The minimization key is `(support_bound, actual_draws, head_size)`. Exact-input
bypass has zero actual draws, even if its unused requested sample count is
enormous. This agrees with the operational tie rule explained in the source
and README. It also handles the deterministic cutoff's discontinuity: a
candidate at the cutoff is not forced into a positive sample budget.

The code exactly optimizes this computed numeric objective within the cap.
It does not compute mathematically exact magnitudes or logarithms: rational
ceilings after rounded `hypot` and `log` values cannot certify that the true
mathematical sample bound was rounded upward. That limitation is explicitly
acknowledged rather than hidden by the use of Fractions.

## 3. Exact fallback precedes all RNG work

Construction validates parameters and input binding first. Exact-input and
head-only branches return before accessing the RNG. On the sampled branch,
the enforced invariant is 0<k and s+k<m, hence k<N. No enormous requested
budget is used to allocate draws and then discarded afterward.

Independent tests use an RNG object that raises on *any attribute access*.
Exact fallback succeeds for epsilon=1e-300 and for the smallest positive
binary64 epsilon, and the equality-cutoff head-only case also succeeds.
These checks confirm pre-RNG bypass, not merely a zero count in metadata.

## 4. Binding and sampler validity

Input values are converted to finite Python complex values before planning
and construction. The plan stores that complete immutable value snapshot
and converted float epsilon/delta. Mismatches are rejected before reuse.
Binding is to these converted values, not to distinct arbitrary-precision
objects that round to the same complex representation.

`PrefixPlan` is trusted state generated internally by `plan_prefix`.
Snapshot/parameter matching does not authenticate deliberately forged
dataclass fields such as changed masses or budgets. No adversarial plan
integrity guarantee is intended. Within that trust boundary, stored head
indices and masses are reused without another selection call.

For valid iid uniform draws, sorting changes the draw order but preserves
the sampled multiset. The constructor compares sorted targets against exact
cumulative sums of its numeric residual masses. Strict `< cumulative`
comparison implements the standard half-open inverse-CDF intervals, including
u=0 and draws arbitrarily close to one. Positive residual coordinates are
scanned in order, repeated hits are coalesced, and head coordinates are
excluded by the marker array. Coalescing multiplies each selected phase by
residual_mass*count/k, exactly the intended formula before numerical rounding.

An independent inverse-CDF oracle checked a nonuniform, signed-real residual
with a nonempty head at index 777. All 64 deterministic test draws mapped
correctly, coalescing to five tail indices. Invalid uniform values below zero,
at one, NaN, and infinity were rejected. These are mechanical CDF checks;
they neither establish that a supplied RNG is iid/uniform nor estimate the
algorithm's probability of failure.

Python's finite-bit pseudorandom uniforms, rounded complex phases, coefficient
underflow/overflow, and any downstream FFT remain outside the ideal continuous-
uniform probability proof. In particular, dropping a coefficient that rounds
to zero can change the mathematical estimator. The documentation correctly
does not advertise a machine-certified Hoeffding guarantee.

## 5. Cost and output scope

The constructor pays another O(N) binding/marker/residual pass and
O(k log(k+2)) for sorted draws. Since k<=B_selected<=N on sampled paths,
the corrected derivation's absorption into O(N log(B_selected+2)) is valid
when combined with the stated sparse-input transform. The smaller realized
support cannot replace the planned support in that bound while ignoring draws
that coalesced.

This package returns sparse entries and metadata. The final transform,
unitary normalization, root preparation, and N output writes remain the
caller's work and are explicitly conditional in the README. No fresh exact
FFT speedup follows from this planner result.

No unresolved correctness issue was found within the declared numeric and
trusted-state scope. The independent checks supplement, rather than repeat,
the author's full-sort/prefix oracle audit and run no old benchmarks.
