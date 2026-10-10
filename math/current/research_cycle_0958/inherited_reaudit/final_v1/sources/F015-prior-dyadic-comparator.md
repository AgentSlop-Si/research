# Dyadic Fourier–Green Cut Spectra and Aggregate-Sparse Fiber FFTs

**Date:** October 10, 2026  
**Research status:** Two complete mathematical derivations, exact arithmetic implementations and supporting tests. **No unrestricted exact O(N) FFT is claimed.** Novelty relative to public literature is unverified; some ingredients are classical, and the positive theorem explicitly extends the user's prior Hero #17 algorithm.

## 0. Research contract and correction to previous work

The project asks whether a *fresh arbitrary* length-N DFT can be evaluated exactly in O(N) sequential arithmetic. The following research does **not** solve that open objective. Its contributions are:

1. A complete singular-spectrum formula for structured Fourier cuts, yielding condition-independent, **power-of-two** impossibility and approximation tests for products of arbitrary non-affine weighted Green sums.
2. A combined dyadic crossing constraint and an O(N+E)-work certificate for all dyadic residue-class cuts of E directed, nonzero-weight Green edges.
3. A budget-adaptive **exact** Fourier algorithm for a strictly larger *structured-input family* than the older Hero #17 bounded-per-fiber class, including unbounded individual fiber sparsities, with raw-input recognition and explicit dense outputs.

**Correction:** The older two-sum sparse bridge already has a linear-work application schedule: if `K=CB` and each `A,B,C,D` is a weighted cyclic difference denominator, then `K^{-1}=B^{-1}C^{-1}`. Each inverse is a linear-time cyclic Green recurrence. Building a better generic solver for `K^{-1}` is not the open step; the difficult question is finding *phase-correct parameters* such that

`(A^{-1}+B^{-1})(C^{-1}+D^{-1})=F_N` at all lengths, with charged parameter preparation.

All Green-circuit lower bounds below are **representation-specific** and do not imply a general FFT lower bound.

## 1. Dyadic-coset singular-spectrum theorem

Let `U_N[j,k] = N^{-1/2} exp(-2πijk/N)`, and fix a divisor `d|N` with `d>=2`. Write `N=dm`, `g=gcd(d,m)`, and choose any coset

`A = {a+d*u : 0<=u<m}`, `B={0,...,N-1}\A`.

### Theorem A: full exact singular spectrum

The rectangular `m × (N-m)` matrix `U_N[A,B]` has singular values

- `1`, with multiplicity `m-m/g`;
- `sqrt(1-g/d)`, with multiplicity `m/g`.

Zero-valued items are included in the singular-value list. Consequently,

`rank U_N[A,B] = m` if `g<d`, and `m-m/g` if `g=d`.

**Proof.** Let `C=U_N[A,A]`. Because the full Fourier matrix is unitary, orthonormality of its A-indexed rows gives

`U_N[A,B] U_N[A,B]^* = I_m - C C^*`.

After multiplying rows and columns of `C` by diagonal unit-modulus factors (to remove the coset shift a), its entries are

`C[u,v] = (dm)^(-1/2) exp(-2πi d*u*v/m)`.

Hence

`(C C^*)[u,v] = (1/d) * 1_{m | d(u-v)} = (1/d)*1_{u≡v (mod m/g)}`.

Reorder u by its residue modulo `m/g`. Then `C C^*` is the direct sum of `m/g` copies of the `g×g` all-ones matrix divided by `d`. Each block has one eigenvalue `g/d` and `g-1` zero eigenvalues. Subtracting from the identity proves the two displayed singular values and their multiplicities. The diagonal row/column phases removed earlier do not change the singular spectrum. QED.

**Important:** The raw subgroup/coset Fourier calculations and spectral-norm facts have prior mathematical literature. The theorem's contribution in this project is its coupling to weighted Green-network rank budgets.

## 2. Exact Green crossing ranks and robust Fourier incompatibility

For a Hamiltonian cycle permutation `σ`, let `T=diag(w)P_σ`, `K=I-T`, `G=K^{-1}` (assume invertible, which for one weighted cycle means `∏_u w_u !=1`). For any vertex set `A`, define the *active directed outgoing cut count*

`b_G(A) = #{u∈A : σ(u)∉A and w_u !=0}`.

The complementary inverse-nullity identity gives

`rank G[A,A^c] = rank K[A,A^c] = b_G(A)`.

The last equality holds because K's offdiagonal entries are a weighted partial permutation matrix.

Now take an architecture

`M= ∏_{t=1}^T (Σ_{j=1}^{q_t} L_{tj} G_{tj} R_{tj})`,

where **each L and R is invertible diagonal** and all factors are in the same coordinate frame. Common interstage coordinate permutations may also be handled after pushing them into conjugated cycles, PROVIDED the resulting outer endpoint permutations are accounted for (no arbitrary unmatched left/right permutations inside summands). Define the total budget `b(A)=Σ_{t,j} b_{G_tj}(A)`.

Partitioning the intermediate coordinate set into A and A^c gives

`(XY)[A,A^c] = X[A,A]Y[A,A^c] + X[A,A^c]Y[A^c,A^c]`.

Rank subadditivity under addition and this formula under multiplication imply

`rank M[A,A^c] <= b(A)`.

### Theorem B: exact and approximate dyadic-Green barrier

For every divisor d and coset A of Theorem A, if `M=U_N`, then

`b(A) >= m-m/g` when `g=d`, and `b(A)>=m` when `g<d`.

For arbitrary M of this architecture, the spectral norm error obeys:

- if `b(A)<m-m/g`, then `||M-U_N||_2 >=1`;
- if `g<d` and `m-m/g <=b(A)<m`, then `||M-U_N||_2 >=sqrt(1-g/d)`.

**Proof.** Apply rank inequality above and Theorem A. For approximation, Eckart–Young shows the operator-norm distance of `U[A,A^c]` to any matrix of rank <=b equals its `(b+1)`st singular value. Restricting the global error to the rectangular block cannot increase operator norm, giving the claimed lower bound. QED.

For N=2^k, choose d=2^r. Then g=2^min(r,k-r). In the range `1<=r<=k/2`, **all nonzero singular values equal 1** and

`b(A) >= (N/d)(1-1/d)` is necessary for every exact candidate, and for every candidate with `||M-U||_2<1`.

### Corollary: fiber-grouped non-affine cycles

If each Green cycle orders one selected residue class A in at most h contiguous runs (even with completely arbitrary non-affine permutations within each run), then that branch has at most h outgoing active edges across A. For q total branches, `b(A)<=q h`. Consequently, at `N=2^k`, `d=2`, `k>=2`,

`q*h >= N/4`

is necessary for exact Fourier equality and even for `||M-U||_2<1`.

**Numerical example:** At N=64, four independently weighted Hamiltonian cycles that keep all even indices contiguous each have one outgoing parity-cut edge. Thus b(A)<=4, while the unitary Fourier parity block has rank16 with sixteen singular values1. Every such network has operator-norm error at least 1. This is a *proved bound for all weights*, not a numerical optimization failure.

## 3. New multi-scale dyadic mixing certificate

Let N=2^k and write `A_{r,a}={u:u≡a (mod 2^r)}`. Let `E` be the multiset of **active** directed Green edges across all stages and summands, `e=(u,v)`, u !=v. Denote by `ν_2(u-v)` the number of common low binary digits (in `[0,k-1]`).

### Theorem C: multiscale crossing requirement

For any candidate equal to U_N, and also for any candidate with `||M-U_N||_2<1`, for `R=floor(k/2)`:

`Σ_{(u,v)∈E} max(0,R-ν_2(u-v)) >= N (R-1+2^{-R})`.

**Proof.** Theorem B, at each level `1<=r<=R`, applied to all `2^r` residue classes and summed over the classes, yields

`Σ_{a=0}^{2^r-1} b(A_{r,a}) >= N(1-2^{-r})`.

One directed edge e=(u,v) contributes to exactly one r-level outgoing cut if `u mod2^r != v mod2^r`, i.e. if `r>ν_2(u-v)`. Therefore summing the left side over r gives `Σ_e max(0,R-ν_2(u-v))`. Summing the lower bounds gives `N Σ_{r=1}^R (1-2^{-r}) = N (R-1+2^{-R})`. QED.

This is weaker than checking every individual coset and **does not** rule out all non-affine cycles. A stride-one Hamiltonian cycle mixes low bits at every scale and passes the necessary budget. It is a useful fast rejection criterion for p-adically local or fiber-grouped cycles, not sufficient for Fourier phase correctness.

### Theorem D: all dyadic cut budgets in O(N+E) work

A length-N binary **LSB-first** residue trie has nodes `(r,a)` for `0<=r<=k`, `0<=a<2^r`, totaling `2N-1` nodes. A node's parent is `(r-1, a mod2^{r-1})`. Given a directed active edge `(u,v)`, its lowest common ancestor in this trie is `(t,u mod2^t)`, where `t=ν_2(u-v)`.

1. Add +1 at leaf `(k,u)`.
2. Add -1 at the LCA `(t,u mod2^t)`.
3. After processing all E edges, aggregate node values from leaves toward root.

The aggregate at node `(r,a)` is **exactly** `b(A_{r,a})`. Each edge contributes +1 along the path from its source leaf until just below the LCA, corresponding precisely to residue classes containing u but not v.

A table `tz[1..N-1]` of 2-adic valuations can be built via `tz[odd]=0`, `tz[even]=1+tz[e/2]` in O(N) time. Thus no uncharged count-trailing-zero instruction is assumed. Total sequential integer work and memory are `O(N+E)` and `O(N)` respectively, with O(log(N+E))-bit counters. For a constant number of cyclic Green branches, E=O(N), so the entire multiscale cut certification costs **O(N)** operations, with no FFT oracle and no graph-cut solver.

## 4. Aggregate-sparse fiber theorem — a positive exact result

This improves *the input family* of the user's `hero17_tensor_union/fiber_union.py`; it does **not** improve worst-case complexity on arbitrary fresh dense inputs.

Let `N=QM`, `Q²<=C N`, and let the field contain a supplied primitive Nth root of unity with characteristic not dividing N. Form Q raw input fibers `y_t[u]=x[t+Q u]` (u=0..M-1), each of which has its unique finite Fourier expansion

`y_t[u]=Σ_{h∈H_t} c_{t,h} η^{hu}`, with η=ω_N^Q and all c nonzero.

Define `r_t=|H_t|` and the **total**, not maximum per-fiber, Fourier sparsity `K=Σ_t r_t`. The sets H_t and coefficients c are **not supplied**; the algorithm must discover them from raw input.

### Theorem E: fully charged total-budget recognition and transform

Given a total-mode budget K0, there is a deterministic exact algorithm that:

- reads the entire raw input;
- either returns the exact complete length-N Fourier output with a checked mode certificate when `K<=K0`, or rejects when `K>K0`;
- performs `O(N + M K0 + Q K0 + K0²)` field/word operations for **all inputs**, including rejected ones, assuming supplied primitive roots and unit-cost field arithmetic.

In particular, if `K0<=C_0 Q`, `Q²<=C_1 N`, then **all N exact outputs take O(N)** including recognition, root scanning, sparse amplitude recovery, explicit writes and rejection logic.

### Construction and proof

Let `H=floor(M/3)` (for M<3, direct M-point DFT is O(M) work per fiber). Process fibers one at a time, with `remaining` total characters still allowed:

- Run bounded Berlekamp–Massey with cap `min(H,remaining)` across the entire M-sample fiber. If it yields a recurrence of degree r, scan all M known Mth roots to locate all roots of its reversed characteristic polynomial; solve the r-node **transposed Vandermonde** system in O(r²) exact field operations and verify all M raw coordinates. For a true sum of r<=H distinct Fourier characters, M>=3r guarantees this succeeds, and its cost is `O(Mr+r²)`.
- If this exact recovery fails and `remaining<=H`, reject: any signal with <=remaining Fourier modes would have been recovered by the preceding procedure.
- Otherwise use a **direct O(M²) DFT**, count the nonzero Fourier coefficients exactly, and charge them against the remaining budget. In a valid or not-yet-rejected input, every such heavy fiber has >H modes (because a light fiber would have passed the exact verified Prony recovery). Hence each O(M²) fallback can be amortized against >=H+1 discovered modes; since H=Theta(M), the total cost of all heavy fallbacks (including a final rejected fiber) is O(MK0).

Light recoveries cost `O(M Σ r_t + Σ r_t²) <= O(M K0 + K0²)`. Reading/zero fibers and table generation cost O(N). Every identified mode `(t,h,c)` contributes to exactly Q output frequencies `k=h+sM`, by the orthogonality identity

`F_N x[k] = M Σ_{t=0}^{Q-1} Σ_{(h,c)∈H_t, h=k mod M} c ω_N^{-kt}`.

Hence dense output reconstruction costs `O(N+QK0)`. Combining charges proves the theorem. The reference program uses exact finite-field arithmetic, a bounded BM recognizer, an O(r²) Vandermonde solver, and intentionally quadratic **small/heavy fallback transforms only**.

This strictly extends the old `r_t<=constant` class: an individual fiber may have `r_t=Theta(Q)`, while other fibers each have one character, and the overall Q×M array can have rank Q. The reference test exercises this explicitly at N=64,256,1024.

### Limits and numerical model

- The theorem is **exact** only in an ideal field model (including finite fields with N dividing |F|-1, or an exact complex-root arithmetic model). Floating-point root identification, rounding, conditioning and bit complexity require separate analysis.
- The method uses a *sparse per-fiber spectrum* and rejects generic dense inputs. At N=Q² generic data has K=Theta(N), so the theorem does **not** yield a faster universal FFT.
- The root of unity is a supplied public parameter; the costs of root table generation (O(N)) and input scanning are included, but finding an arbitrary suitable finite field and root is not part of the claim.
- The positive family is a mathematical extension of the existing Hero #17 Prony/fiber approach, **not** claimed to be new in all of sparse-FFT/Prony literature.

## 5. Research decision gate for the exact arbitrary-input goal

The project's strongest unresolved route remains a *fixed number of products of non-affine, independently gauged Green sums* satisfying simultaneously:

(1) **all cut ranks** (the dyadic theorem is a cheap rejection test on powers of two, not a sufficient condition);

(2) **actual Fourier Weyl covariance**, e.g. `M S = D M` and `M e_0 = (1,...,1)/sqrt(N)` for unitary F, checked with exact finite-field residuals or symbolic identities;

(3) **uniform all-N weights/permutations and O(N) charged generation**, not small-n numerical fitting;

(4) **stable/bit-complexity bounds** if claiming a practical fast FFT rather than permissive exact-complex arithmetic.

**No parameter family satisfying these gates was found.** The new results provide a stronger power-of-two rejection certificate and a larger exact structured positive family, without representing either as an unrestricted FFT breakthrough.

## 6. Reproduce

`python verify.py` independently checks 252 Fourier-block singular spectra, 4,910 exact integer trie-versus-brute-force cut values, 336 exact Green block-rank identities over finite fields, 742 two-stage exact finite-field product-sum rank inequalities, 42 exact Fourier block ranks, and 24 multiscale identities.

`python verify_heterogeneous.py` runs 80 exact structured-input cases including three full-rank heavy-fiber constructions, 25,104 exact Fourier bins independently checked against direct quadratic DFT, and 49 rejected generic dense input cases.

The tests substantiate implementations and finite cases; the asymptotic claims are proved by the arguments above, not by extrapolating finite benchmarks.

## 7. Source / originality boundaries

Project sources reviewed or cross-checked: the October 9 master 3,532-file archive, Green Phase 22 and Phase 26, sparse-defect Green, Hero #0, Hero #1 v13, Hero #17 tensor/fiber/graph union, phase23/24 independent audits, previous SPFSB and chord-rigidity files, the signed-atom Word-RAM approximation study and Weyl–Expansion dual certificate. Identical nested checkpoint files should not be counted as independent research. See `SOURCE_AUDIT.md`.

External mathematics: Fourier transforms on finite groups (subgroup orthogonality), structured partial Fourier singular values, complementary inverse nullity, quasiseparable Green matrices, Berlekamp–Massey/Prony, and quadratic Vandermonde algorithms. A targeted literature search did **not** establish priority for the full combined dyadic cut-certificate or total-budget fiber statement; independent mathematical and prior-art review is still necessary.

A published exact sub-NlogN complex arithmetic result in a different model appears in OpenAI Math problem #130 (uniform `O(N(log N)^{1-10^{-13}})` with unrestricted exact complex constants). **This package does not improve that universal asymptotic bound.**
