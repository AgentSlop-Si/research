# Permutation-cycle rank formalization specification

**Verification status: unimplemented specification; no Lean build was possible.**

## 1. Frozen mathematical scope

The accepted `M-SORTING-RANK` source, section “Conventions and universal identity,” states that the fixed-vector equations for a permutation give one freely chosen scalar per cycle over every field. It uses this to obtain `rank(W − Z^a) = N − cycles(Z^(−a)W)`. The source explicitly includes characteristic two and fields whose characteristic divides a cycle length. Its SHA256 is `f574925a32279259f6e4a2eb1c1b1f438492da4c27757fc242e13065c2d515f6`.

This pilot isolates precisely that universal unweighted identity. It does not formalize stable sorting, transition counts, distribution or probability bounds. The related `M-PERMUTATION-DISPLACEMENT` result uses `D − P` and a weighted monodromy condition; this pilot is only its unweighted prerequisite, not a verification of that complete theorem or of its extremizer statement.

## 2. Exact target definitions

Let `N : ℕ`, with `1 ≤ N`, and let `K : Type u` have `[Field K]`. Set `ι := Fin N`. Let `σ : Equiv.Perm ι`.

1. Define the matrix `permMatrix K σ : Matrix ι ι K` by entry `(i,j) = 1` if `i = σ j`, and `0` otherwise. This fixes the column convention `P e_j = e_(σ j)`.
2. Define the linear endomorphism `permLinear K σ` of `ι → K` by `(permLinear K σ x) i = x (σ.symm i)`. Its additivity and scalar linearity are pointwise identities.
3. Define `defect K σ := LinearMap.id − permLinear K σ`.
4. Let `cycleSetoid σ := Equiv.Perm.SameCycle.setoid σ`; its relation is `σ.SameCycle`.
5. Define `CycleQuotient σ := Quotient (cycleSetoid σ)`, with a finite type instance obtained from finiteness of `ι`.
6. Define `cycleCount σ := Fintype.card (CycleQuotient σ)` using that instance. Each fixed point contributes its own equivalence class.

These are definition contracts, not tested Lean declarations. Once implemented, include the actual names, universes, and instantiated types in the build artifact.

Do not use `(σ.cycleFactorsFinset).card` as the number of all cycles. That API omits fixed points; in particular its value for the identity permutation is zero. If that API is used for an executable cycle count later, the separate fixed-point contribution and the equality to this quotient count must both be proved. See [mathlib cycle factors](https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/Perm/Cycle/Factors.html#Equiv.Perm.cycleFactorsFinset_one).

## 3. Theorem contracts and dependency order

A. Matrix/operator compatibility:

For every `x : ι → K` and `i : ι`,

`(permMatrix K σ).mulVec x i = x (σ.symm i)`.

Therefore the linear map corresponding to `1 − permMatrix K σ` is `defect K σ`.

B. Elementary kernel characterization:

`x ∈ LinearMap.ker (defect K σ) ↔ ∀ i, x (σ i) = x i`.

C. Cycle constancy:

`(∀ i, x (σ i) = x i) ↔ ∀ i j, σ.SameCycle i j → x i = x j`.

D. Kernel classification, the main construction:

Produce an explicit `K`-linear equivalence

`LinearMap.ker (defect K σ) ≃ₗ[K] (CycleQuotient σ → K)`.

E. Exact nullity:

`Module.finrank K (LinearMap.ker (defect K σ)) = cycleCount σ`.

F. Linear rank formula:

`Module.finrank K (LinearMap.range (defect K σ)) + cycleCount σ = N`.

Then derive the natural-number subtraction form

`Module.finrank K (LinearMap.range (defect K σ)) = N − cycleCount σ`.

Use the additive form first so truncated natural subtraction cannot conceal a missing inequality.

G. Matrix conclusion:

`Matrix.rank (1 − permMatrix K σ) = N − cycleCount σ`.

This is the completion target for the bounded pilot. If only B or C can be implemented initially, report exactly that smaller prerequisite as checked and keep D–G explicitly pending.

## 4. Proof construction, without spectral assumptions

For A, the finite row sum has a single nonzero entry at `j = σ.symm i`; evaluate that term. Check the orientation explicitly rather than silently switching `σ` and `σ⁻¹`.

For B, the coordinate equation of the kernel is `x i − x (σ.symm i) = 0`. Evaluate at `σ j` for the forward implication, and use the same equation in reverse for the other implication.

For C, invariance propagates by induction along nonnegative powers of `σ`. On a finite type, `SameCycle.exists_nat_pow_eq` gives a power carrying one index to the other. Conversely, an index and its image under `σ` are in the same cycle. The equivalence relation and finite power witness are supplied by [mathlib permutation cycles](https://leanprover-community.github.io/mathlib4_docs/Mathlib/GroupTheory/Perm/Cycle/Basic.html).

For D, map a kernel vector `x` to the function on classes `[i] ↦ x i`. Use C to discharge the quotient-lift well-definedness obligation. Conversely, map `g` to `i ↦ g [i]`; this lies in the kernel because `[σ i] = [i]`. Prove both inverse laws with quotient induction and function extensionality. Prove additivity and scalar compatibility pointwise. No division by cycle lengths occurs.

For E, transfer finite dimension along D and use the dimension of a finite scalar-function space. For F, use rank-nullity and `dim_K(K^(Fin N)) = N`. For G, apply A and the standard matrix/linear-map rank bridge. The proposed imports and documented declarations are in `DEPENDENCY_MAP.json`.

## 5. Source transport boundary

The source's shift identity follows mathematically by putting `V = Z^(−a)W`: left multiplication by the invertible permutation matrix `Z^(−a)` changes `W − Z^a` into `V − I`, and multiplication by `−1` changes it to `I − V`. Both operations preserve rank over every field, including characteristic two. A later Lean wrapper may formalize those two steps, but it must not be reported as checked merely because G is checked.

For the Fourier permutation-displacement record, a future weighted kernel-classification theorem must separately track nonzero diagonal weights and the product around each cycle. No primitive root, characteristic guard, Fourier invertibility, minimum-rank optimizer, or novelty conclusion is established by G.

## 6. Boundary examples and tests to include after implementation

These are planned regression obligations, **not tests executed in this packet**:

- Identity on `Fin N`: exactly N quotient classes; defect rank zero.
- N = 1: one fixed point; rank zero.
- One 2-cycle over `ZMod 2`: one cycle and rank one despite the characteristic dividing its length.
- One 3-cycle over `ZMod 3`: one cycle and rank two.
- One 2-cycle plus two fixed points on `Fin 4`: three cycles and rank one.
- A permutation and its inverse: equal cycle counts and equal defect ranks, while matrix/operator conventions remain explicit.

An optional N = 0 extension is valid mathematically, but it is unnecessary for this frozen positive-size pilot. Do not let an empty-type convenience change the documented source scope.

## 7. Dependency and toolchain discipline

The exact imports to try, after pinning a compatible mathlib checkout, are:

- `Mathlib.GroupTheory.Perm.Cycle.Basic`
- `Mathlib.LinearAlgebra.FiniteDimensional.Lemmas`
- `Mathlib.LinearAlgebra.Dimension.Constructions`
- `Mathlib.LinearAlgebra.Matrix.Rank`

These modules were found in current official documentation. This is not a successful import check, nor a claim that their current API matches the archived research pin. The packet records no active Lean or mathlib version. A future implementation must record its actual `lean --version`, `lake --version`, `lean-toolchain`, `lake-manifest.json`, mathlib commit, imports, and complete build output.

## 8. Verification acceptance gate

The eventual checked deliverable must include:

1. A self-contained Lean file and a reproducible command such as `lake env lean PermutationCycleRank.lean`, actually executed in the pinned project.
2. Successful exit status and retained stdout/stderr from a clean re-run.
3. No `sorry`, `admit`, newly introduced unproved axioms, or unsafe shortcuts. A text scan alone is insufficient.
4. `#print axioms` output for each exported theorem, excluding `sorryAx` and project-specific unproved axioms. Ordinary foundational axioms used by Lean/mathlib are to be disclosed accurately, not represented as newly proved facts.
5. An independent review of hypotheses and the matrix orientation against the accepted source.
6. Distinct labels for general kernel-checked theorems and any finite regression examples.

Lean's official description explains that elaborated declarations are checked by its kernel; prose and finite tests do not provide that check. See [Lean elaboration and kernel](https://lean-lang.org/doc/reference/latest/Elaboration-and-Compilation/#the-kernel).

Current gate outcome: **blocked before implementation and compilation because no usable toolchain is available.**
