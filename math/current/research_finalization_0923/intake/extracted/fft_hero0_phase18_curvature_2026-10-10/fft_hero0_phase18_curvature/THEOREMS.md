# HERO #0 — Phase 18: continuous Fourier–Green curvature certificates

**Date:** 10 October 2026  
**Status:** Proofs and reproducible exact/numerical checks for restricted Green networks. **No new universal FFT runtime bound and no independent literature-novelty claim.**

## 0. Provenance and what is genuinely new *within this project*

The Phase 15 archive **already proved** the full singular-value spectrum of the half-grid Fourier commutator using an order-eight monomial reduction. Phase 17 already proved the independent-gauge approximation gap and the low-rank edit-count barrier. Do **not** describe those results as newly discovered in Phase 18. Our Phase 18 polynomial identity `V^4=-I` and modular check reproduce the older Phase 15 result independently.

The new derivation in this checkpoint is **a continuous, Frobenius-energy necessary condition** for asymmetric weights, including a distance to the full phase-gauge/flat-connection orbit. Unlike counting changed edges, it handles arbitrarily small differences spread across all vertices. The new O(E)-work evaluator computes rigorous nonzero error floors without forming the dense transform or its Green resolvents. The holonomy recognizer and rank corollary connect this quantitative gate to Phase 16's spanning-gauge method. The ingredients (resolvent identities, norm inequalities, magnetic/gauge frustration, and Fourier displacement) have extensive prior art; the project-specific synthesis has not been independently checked for mathematical priority.

## 1. Definitions and cost model

Let `s>=4` be even, `N=s²`, `h=s/2`. Each index `j=s*x+y` has a half-grid partner `tau(j)=s*x+(y+h mod s)`; let `Pi` be its permutation matrix. The normalized Fourier operator is

`U[k,j]=exp(-2 pi i k j/N)/sqrt(N)`.

A **Green term** is `G_{l,t}=(I-P_{l,t})^-1`, where `P_{l,t}` is a weighted permutation supported on one of the fixed Margulis-type permutations `pi_{l,t}`. Every such underlying permutation commutes with `tau`. We adopt the matrix convention `P[i,pi(i)]=w_i`. A layer is `L_l=sum_t alpha_{l,t} G_{l,t}` and the candidate is `T=L_m ... L_1`.

Define the scalar cost quantities

```
a = max_l sum_t |alpha_(l,t)|
A = sum_(l,t) |alpha_(l,t)|
g = a uniform bound for ||G_(l,t)||_2, plus ||G0_(l,t)||_2
    if a flat reference is used
B = (a*g)^(m-1) * g^2
```

The estimates hold for arbitrary `m`; concluding extensive curvature from constants requires `m`, `a`, `A`, and `g` to remain bounded as N grows. A cheap sufficient bound is `g=1/(1-rho)` if every weighted-permutation entry of the actual and reference terms has magnitude at most `rho<1`. This follows because `||P||_2=max_i|w_i|`.

**Operation accounting:** the certificate computes sums over the supplied edges in O(E) scalar operations, where E is the total number of term-weight occurrences, with memory O(N). For a constant number of terms E=O(N). These are *rejection/necessity tests*, not algorithms computing all Fourier outputs.

## 2. Exact half-grid Fourier commutator (reverified, NOT newly proved in Phase 18)

**Proposition (inherited from Phase 15, independently reproduced).** For all even s,

```
V = Pi U^-1 Pi U,
V^4 = -I,
spectrum(V) = { exp(+/- i*pi/4), exp(+/- 3i*pi/4) },
              each with multiplicity N/4.
```

Therefore `C=U Pi-Pi U` has singular values `sqrt(2+sqrt(2))` and `sqrt(2-sqrt(2))`, each N/2 times; in particular,

`||C||_F²=2N`, `rank(C)=N` and `||C||_2=sqrt(2+sqrt(2))`.

**Short all-size proof.** Let `omega_q=exp(-2*pi*i/q)`. Index inputs by `(x,y)`, outputs by `(a,b)`. Compute one length-s Fourier transform in x (operator C0), multiply by `D[b,y]=omega_(s²)^(b*y)`, then Fourier transform in y (operator B0). This yields exactly `U=B0 D C0` with normalized small FFTs and an output-register shuffle.

The same half-grid swap acts on y before C0 and on b after B0. Consequently V is unitarily conjugate, via C0, to `W=P_y D^-1 P_b D`, acting on `(b,y)` as

`W e_(b,y) = omega_N^((b-tau_s(b))*y) e_(tau_s(b),tau_s(y))`,

where `tau_s(t)=t+h mod s`. Write `tau_s(t)-t=h*epsilon_t` with epsilon in {+1,-1}. Applying W twice gives

`W² e_(b,y)=omega_N^(h²*epsilon_b*epsilon_y) e_(b,y)`,

whose scalar is `+i` or `-i` since `h²/N=1/4`. Thus `W⁴=-I`. Both signs occur N/2 times, so the four primitive eighth roots occur N/4 times each. Since the singular values of `U Pi-Pi U` are `|1-lambda(V)|`, the stated values follow. `modular_polyphase_certificate` independently validates the full conjugation and polynomial identity over GF(65537) for N=4,16,64,256.

## 2B. New explicit rank-k relative-Frobenius refinement (inherited spectrum)

If `T=T0+Delta`, `[T0,Pi]=0`, `rank(Delta)<=k`, then `rank([T,Pi])<=2k`. Eckart–Young applied to the **Phase 15 spectrum** gives the following additional explicit Phase 18 corollary:

`||U-T||_F/sqrt(N) >=`

```
  1/2 * sqrt(2 - (2k/N)*(2+sqrt(2)))        if 0 <= k <= N/4,
  1/2 * sqrt((1-2k/N)*(2-sqrt(2)))         if N/4 <= k <= N/2,
  0                                            if k >= N/2.
```

The bound follows because `[Delta,Pi]` has rank <=2k and can cancel at most the largest `2k` commutator singular values. Also `||[U-T,Pi]||_F<=2||U-T||_F`. In particular exact equality requires `k>=N/2`, with **no conditioning assumption**. This improves the explicit Frobenius-error accounting from the prior Phase 15 documentation; its spectral input and rank-telescoping lemma are inherited, not independently new. The value is a **necessary lower bound** and may not be attained by any Green graph.

---

## 3. NEW: raw paired-weight energy obstruction (arbitrary weights)

Define the *direct half-grid symmetry energy*

`E_tau = sum_(l,t) |alpha_(l,t)| * sum_i |w_(l,t,i)-w_(l,t,tau(i))|²`.

**Theorem 18.1.** Let `epsilon=||U-T||_F/sqrt(N)`. If every constituent Green inverse has norm at most g, then

```
 epsilon >= 1/2 * max(0, sqrt(2) - B*sqrt(A*E_tau/N)),
 B=(a*g)^(m-1)*g².
```

In particular, `T=U` requires

`E_tau >= 2N/(A*B²)`.

If a,A,g,m are bounded independent of N, a sequence of exact Fourier networks must therefore have `E_tau=Omega(N)`. More generally, relative error `epsilon<sqrt(2)/2` requires

`E_tau >= N*(sqrt(2)-2epsilon)²/(A*B²)`.

**Proof.** For `P[i,pi(i)]=w_i` and `pi tau=tau pi`, `[P,Pi]` is a weighted permutation with coefficient list `w_tau(i)-w_i` up to a permutation. Hence

`||[P,Pi]||_F²=sum_i |w_tau(i)-w_i|²`.

The exact resolvent identity gives `[G,Pi]=G[P,Pi]G`, whence `||[G,Pi]||_F<=g²||[P,Pi]||_F`. The commutator product rule and `||L_l||_2<=a*g` imply

`||[T,Pi]||_F <= B sum_(l,t)|alpha_(l,t)| ||[P_(l,t),Pi]||_F`.

Cauchy–Schwarz bounds the final sum by `sqrt(A E_tau)`. Moreover

`||[U,Pi]||_F <= ||[U-T,Pi]||_F + ||[T,Pi]||_F`
`<= 2||U-T||_F + B sqrt(A E_tau)`.

Substitute the exact inherited identity `||[U,Pi]||_F=sqrt(2N)` and rearrange. QED.

**Important scope:** This is an energy bound, not a total-arithmetic-work lower bound. Strongly nonunitary or near-singular resolvents may make g large, weakening the certificate. Changing Theta(N) weights is compatible with O(N) work.

## 4. NEW: gauge-invariant distance from every flat phase connection

Fix arbitrary nonzero phase potentials `d_i`, with `|d_i|=1`, and arbitrary scalar reference weights `c_(l,t)` such that `G0_(l,t)` exist. A **flat-reference term** has

`w0_(l,t,i)=c_(l,t)*d_i/d_(pi_(l,t)(i))`.

All term weights in this reference use the **same** D=diag(d). Consequently its full network is `T0=D T_sym D^-1`, where the scalar-weight reference T_sym commutes with Pi. Phase 17 (already proved) gives

`||U-T0||_F/sqrt(N) >= g_s`,
`g_s = (1/2)*sqrt(1-2/(s*sin(pi/s))) > 0`.

Define the phase-curvature distance to *this* reference:

`E_flat(d,c) = sum_(l,t)|alpha_(l,t)| sum_i |w_(l,t,i)-w0_(l,t,i)|²`.

**Theorem 18.2.** If all actual and reference resolvents have norm at most g, then

```
||U-T||_F/sqrt(N) >= max(0, g_s-B*sqrt(A*E_flat(d,c)/N)).
```

In particular, exact Fourier equality requires

`E_flat(d,c) >= g_s² N/(A B²)`

for *every* admissible common unit-phase gauge and reference scalar tuple sharing the stated norm bound. If a uniform bound g holds over a closed family of references, the same requirement applies to the **minimum phase-gauge curvature energy** over that family. Under constant-size/bounded-condition assumptions, it must grow as `Omega(N)`.

**Proof.** For each term, the resolvent identity gives

`G-G0 = G(P-P0)G0`, so `||G-G0||_F <= g²||P-P0||_F`.

Telescoping the products of layer sums (using both actual and reference layer norms <=a*g) yields

`||T-T0||_F <= B sum_(l,t)|alpha_(l,t)| ||P_(l,t)-P0_(l,t)||_F`
`<= B sqrt(A E_flat(d,c))`.

The phase-gauge bound from Phase 17 and triangle inequality produce the conclusion. QED.

Unlike Section 3, this certificate handles **purely gauge-shaped asymmetry**: weights can have large differences `w_i-w_tau(i)` but tiny genuine holonomy/curvature distance. The two tests are complementary, not substitutes.

### A genuinely linear-cost certificate

`linear_time_curvature_certificate` does **not** form U, T, or any dense resolvents. It scans all phase-gauge reference and actual edges, verifies the shared phase gauge, uses `rho=max|w|<1` to certify `g<=1/(1-rho)`, and outputs the proved error floors. This takes O(E+N) field/arithmetic operations and no dense memory. If any term has `rho>=1`, it rejects that *sufficient norm-bound method* rather than claiming impossibility; a different valid Green norm bound could still be supplied.

## 5. NEW combined algorithmic gate: fundamental holonomies and exact rank

Given a connected multigraph of directed generator edges `i -> pi_t(i)`, nonzero field edge weights `w_(t,i)`, and nonzero reference scalars `c_t`, a spanning forest determines vertex potentials d via

`d_(pi_t(i)) = (c_t/w_(t,i))*d_i`.

Every forest edge is flat by construction; for each nontree edge the ratio

`H_e = w_(t,i)*d_(pi_t(i)) / (c_t*d_i)`

is the multiplicative holonomy of its fundamental cycle. The test `H_e=1` is gauge invariant. The *number* of failed fundamental cycles depends on the chosen forest; the property that all pass does not.

Let k be the number of failing non-tree edges, **counting term occurrences**. Fixing those edges gives an exact common-gauge flat reference; the full network differs from that reference by rank at most k by resolvent rank-one update and product telescoping. If that reference is defined and invertible, then

`rank(F_N Q-Q F_N) <= 2k` must hold for any exact Fourier candidate,

where `Q=D Pi D^-1` and F_N is the unnormalized DFT. The rank is computed over the same field. In particular, an exact certificate `rank(F_NQ-QF_N)=N` rules out k<N/2 for **that specific recovered gauge**. Phase 16 already proved generic full rank; this new gate packages the forest-recovered gauge and the exact rank obstruction into one falsification protocol. In the phase-only complex setting Theorem 18.2 instead gives a uniform norm-based condition, without genericity.

The forest is constructed in O(E+N) field operations, plus inversions of nonzero field elements. The optional exact rank audit currently uses cubic Gaussian elimination for small test instances and is **not** claimed O(N).

## 6. Evidence, replication and limitations

Run:

```bash
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase18 test_phase17
OPENBLAS_NUM_THREADS=1 python audit_phase18.py
```

The verifier covers independently computed complex commutators, exact GF(65537) Fourier phase sums and polyphase-conjugation identities, raw/flat curvature error floors, O(E) certificate validity, exact forest holonomy counts and fixed-field rank changes, and adverse cases. The original 15 Phase 17 tests are rerun unchanged.

**What is not established:** an exact Fourier factorization at any new length, a uniform arbitrary-input O(N) FFT, a better upper bound for integer multiplication, a new lower bound for unrestricted FFT arithmetic circuits, or mathematical novelty relative to all published magnetic-graph and displacement literature.

## 7. Next precise research target

The combined restrictions say that any bounded-condition, constant-depth Green network approximating Fourier must have **extensive** paired-weight energy and extensive distance from all pure-gauge phase connections. These are *necessary* constraints, not sufficient conditions. Phase 19 should search for globally distributed, nonflat holonomies satisfying the full Fourier Weyl equations `TS=D_F T` and `Te_0=ones` at `N=16,64`, using exact modular rejection. A successful finite witness would then need a **uniform construction for all N with fully charged arithmetic costs**.

### Prior-art boundary

- Fourier commutator spectrum and low-rank perturbation bounds: **already in this project's Phase 15**.
- Two-sided phase-gauge obstruction: **already in Phase 17**.
- Graph frustration, switching/gauge holonomy and magnetic Laplacians: e.g. *Frustration index and Cheeger inequalities for discrete and continuous magnetic Laplacians* (2016), https://link.springer.com/article/10.1007/s00526-015-0935-x.
- Low-displacement-rank matrix methods: Chandrasekaran et al., *Fast Algorithms for Displacement and Low-Rank Structured Matrices* (2018), https://arxiv.org/abs/1807.03437.

Phase 18 is a controlled combination with a charged O(E) diagnostic, not a priority claim for those classical ingredients.
