# Phase 24 — exact correction rank of sorting, a uniform all-stride obstruction, and low-rank Green updates

**Date:** 2026-10-09  
**Status:** New *project-specific* mathematical identities with full proofs, finite-field implementations, exhaustive finite checks. No new worst-case sub-`N log N` FFT, no integer-multiplication improvement, and no claim of independent peer review or priority over the existing riffle-shuffle literature.

## 0. Why Phase 24 takes this path

Phase 23 proved exact `O(N)` Green transforms on inputs comprising a few exponentials or having sparse cyclic differences. A potential attempt to broaden their applicability is to stably sort a random binary input into two constant runs, run the sparse-difference Green algorithm, and undo the sorting. But changing input order changes the shift operator that defines Fourier covariance. Phase 24 measures the unavoidable reordering correction as an **exact matrix rank**, including the probability distribution for random bits. It also constructs and verifies a low-rank Green correction when the permutation is genuinely near a known cyclic ordering.

The key result concerns the *specific permutation-conjugated shift and its low-rank-resolvent correction model*. It is **not** a general lower bound against adaptive FFT algorithms, all noncommuting Green graphs, or precomputed tables with uncharged access costs.

## 1. Conventions and the universal permutation rank identity

Let `Z e_j = e_(j+1 mod N)` for `j=0,...,N-1`. Let `L` be any ordering of those coordinates, and define `P^-1 e_k=e_(L[k])`. Then `W=P^-1 Z P` is the Hamiltonian-cycle successor in that ordering:

```
W e_j = e_(L[(position_L(j)+1) mod N]).
```

For any integer stride `a`, `W-Z^a = Z^a(V_a-I)` with `V_a=Z^(-a) W`, a permutation matrix. Every vector in `ker(V_a-I)` is constant along every cycle of `V_a`, and conversely, regardless of the field characteristic. Thus

```
rank(W-Z^a) = N - cycles(Z^(-a) W).                (1.1)
```

This requires `O(N)` time to calculate for a specified `a` and is **exact over every field**. If `m_a` is the number of matching columns (fixed points of `V_a`), every nontrivial cycle has length at least 2. Therefore

```
rank(W-Z^a) >= (N-m_a)/2.                         (1.2)
```

## 2. Exact stable-binary-sort theorem

For a binary word `x=(x_0,...,x_(N-1))`, let `L` list all zero indices in increasing original order, followed by all one indices in increasing original order. Set

```
T(x) = #{0<=j<N-1 : x_j != x_(j+1)}
```

(count *noncyclic* transitions; the edge from `N-1` back to `0` is intentionally excluded).

**Theorem 1.** The stable-sorted successor satisfies

```
rank(W-Z) = 2 floor(T(x)/2).                        (2.1)
```

In fact, if both colors occur, `Z^-1 W` has exactly **one nontrivial cycle**; all other coordinates are fixed. Its support has cardinality `rank(W-Z)+1`.

**Proof.** Write the internal transition indices as `t_1<...<t_m`, where `m=T(x)`. If `m=0`, the word already contains a single color run, stable sorting preserves its complete cyclic order, and `W=Z`, giving rank 0.

For a mixed word, consider `V=Z^-1 W`, acting as `V(j)=W(j)-1 mod N`. Every `j<N-1` that is not a transition satisfies `x_j=x_(j+1)`. Stable sorting preserves the relative order within that color, so `W(j)=j+1`, and `V(j)=j`.

For a transition `t_k` that is not the final transition, the next occurrence of the color `x_(t_k)` begins just after the next transition `t_(k+1)`. Hence `W(t_k)=t_(k+1)+1` and `V(t_k)=t_(k+1)`.

If `m` is odd, then `x_0 != x_(N-1)`. The last transition `t_m` ends the final occurrence of the initial color, so stable sorting connects it to the first occurrence of the other color, at `t_1+1`; thus `V(t_m)=t_1`. The last coordinate `N-1` connects to coordinate 0 and remains fixed. Consequently the transition indices form **one cycle of length `m`**, all others fixed, and `rank(W-Z)=m-1`.

If `m` is even and positive, `x_0=x_(N-1)`. The last transition `t_m` instead connects to coordinate 0, so `V(t_m)=N-1`; the last coordinate connects to the first occurrence of the other color and gives `V(N-1)=t_1`. Thus the transition indices **together with `N-1` form one cycle of length `m+1`**, and `rank(W-Z)=m`.

Both cases equal `2 floor(m/2)` by (1.1). QED.

**Consequences.** The number `s` of changed successor edges (`W(j)!=(j+1) mod N`) equals `rank(W-Z)+1` whenever both symbols occur. This gives a matching, **explicit** size for the Woodbury update in Section 5. There is no hidden small-rank representation for typical binary sorting in this reference basis.

## 3. Exact random-binary rank distribution

Take independent fair bits. The map

```
(x_0,...,x_(N-1)) <-> (x_0, x_0 xor x_1,...,x_(N-2) xor x_(N-1))
```

is a bijection, so the `N-1` internal transition bits are independent fair Bernoulli variables. Therefore `T ~ Binomial(N-1,1/2)`.

**Theorem 2.** For every possible even rank `r=2k`,

```
P(rank(W-Z)=2k)
 = [binom(N-1,2k)+binom(N-1,2k+1)] / 2^(N-1)
 = binom(N,2k+1)/2^(N-1).                           (3.1)
```

Odd ranks have probability 0. For `N>=3`,

```
E[rank(W-Z)] = N/2-1,     Var(rank(W-Z))=N/4.    (3.2)
```

This gives the exact finite-size law, not just `Omega(N)` in probability. A standard binomial tail shows, for `0<t<(N-1)/2`,

```
P(rank(W-Z) < (N-1)/2 - t - 1)
 <= exp(-2*t*t/(N-1)).                               (3.3)
```

Exhaustive checks include all `2^N` words at every `N=2,...,16`; the code checks both the rank identity and every probability count.

## 4. The all-stride theorem (including `Z^a`)

Could the sorted successor be very close to *some other* cheap cyclic stride `Z^a`? A structured word such as `010101...` can indeed make `W` close to `Z^2` rather than `Z`. The correction must therefore be analyzed **simultaneously for every stride** instead of declaring that the rank relative to `Z` settles the issue.

**Theorem 3.** Let `N>=16`, and take independent fair input bits. Put

```
A = min(N-1, ceil(3 log2(N))).
```

With probability at least

```
max(0, 1 - exp(-N/32)
         - A(A+1) exp(-N/[16(A+1)])
         - N*2^(-A)),                                (4.1)
```

we have **simultaneously for every `1<=a<N`**, including strides that are not coprime to `N`,

```
rank(W-Z^a) >= N/8.                                 (4.2)
```

The explicit bound tends to 1 as `N` grows; it is conservative and can be vacuous for moderate `N`. At `N=8192` it already exceeds `0.995`.

**Proof.** In the stable-sorted cycle, all but **at most two** edges connect an index `j` to the *next larger original index of the same color*. To coincide with `Z^a` on a nonbridge edge, there must be a substring of length `a+1` of the form

```
0 1 1 ... 1 0     or     1 0 0 ... 0 1.
```

For each starting index this has probability `2^(-a)`. Let `Q_a` count these substrings, using nonwrapping starts `0<=j<N-a`. The number `m_a` of matching edges satisfies

```
m_a <= Q_a+2,   E[Q_a]=(N-a)/2^a.                    (4.3)
```

For `a=1`, the equality indicators for adjacent independent bits are themselves independent fair bits (by the same XOR bijection used in Section 3). Hoeffding gives

```
P(Q_1 > E Q_1+N/8) <= exp(-N/32).
```

For `2<=a<=A`, group the start indices modulo `a+1`. Windows within a group are disjoint, so their indicators are independent. If `Q_a-EQ_a>N/4`, at least one of its `a+1` groups exceeds its own expectation by `N/[4(a+1)]`. Hoeffding and group size at most `ceil(N/(a+1))<=2N/(a+1)` imply

```
P(Q_a>EQ_a+N/4)
 <= (a+1) exp(-N/[16(a+1)]).
```

For longer gaps, a first-moment/union bound gives

```
P(exists a>A with Q_a>0)
 <= sum_(a>A) (N-a) 2^(-a) <= N 2^(-A).
```

Outside the union of these events, all `m_a<=3N/4` for `N>=16`: for `a=1`, use `(N-1)/2+N/8+2<=3N/4`; for `a>=2`, use `N/4+N/4+2<=3N/4`. Equation (1.2) yields `rank(W-Z^a)>=(N-m_a)/2>=N/8`. Taking the union bound yields (4.1). QED.

**Scope.** This excludes low-rank perturbations of *any fixed cyclic power* as a universal shortcut for random sorted binary inputs. It does **not** imply the shifted operator has no other computationally cheap representation, nor does it exclude independently ordered Green sums.

## 5. A positive exact Woodbury Green correction for nearby orders

Now assume the permutation really is close to the standard cyclic ordering. Let `J` be the `s` coordinates whose outgoing successor edge differs from `Z`. The difference has the exact factorization

```
W-Z = sum_(j in J) (e_(W(j)) - e_(j+1)) e_j^T.
```

Using the Phase 22 real orthogonal residual `C`, let `R=C Z C^-1` (block-diagonal rotations), and define

```
R_W = C W C^-1 = R + U V^T,
U[:,j] = C(e_(W(j))-e_(j+1)),   V^T[j,:]=e_j^T C^-1.
```

Let `P^-1 e_k=e_(L[k])` and `g(z)=(1,z,...,z^(N-1))`. The covariance of `C P^-1` is `C P^-1 Z=R_W C P^-1`, with seed `C e_(L[0])`. Therefore, whenever `z^N != 1`, the *exact* identity is

```
C P^-1 g(z)
  = (1-z^N) (I-zR_W)^-1 (C e_(L[0])).            (5.1)
```

Put `A_z=I-zR`. The Sherman–Morrison–Woodbury identity gives

```
(A_z-zUV^T)^-1 b
 = A_z^-1 b + z A_z^-1 U
     (I_s-z V^T A_z^-1 U)^-1 V^T A_z^-1 b.         (5.2)
```

Since `R` consists of independent `1x1` and `2x2` blocks, each `A_z^-1` multiplication uses `O(N)` field work. Computing all the columns and the small dense correction in (5.2) costs

```
O(N*s^2+s^3) field operations, O(N*s+s^2) space.
```

For **constant `s`**, this is an exact `O(N)` executor, including output materialization and coefficient preparation. The implementation uses `F_998244353`, counts modular operations, and excludes the singular case `z^N=1` (which has a separate spectral branch in Phase 23).

This is a positive **special-permutation** Green construction, not a faster arbitrary-input FFT. For randomly sorted binary inputs, Theorems 2–3 show that the correction is generally not bounded rank or bounded number of mismatched edges. In particular, Theorem 1 gives `s=rank(W-Z)+1=Theta(N)` with high probability, so (5.2) no longer yields linear work.

## 6. Experiments and controls

- **Exhaustive binary words:** every word of every length `N=2,...,16` checked for exact rank formula and exact distribution; moment checks for `N=3,...,16`.
- **Arbitrary stride:** all `a=1,...,N-1` checked for seeded random binary samples at `N=32,64,128,256` in the tests and up to `N=4096` in the independent audit.
- **Green Woodbury:** correct `C P^-1 g(z)` reconstruction over a finite field for one/two arbitrary coordinate swaps at `N=8,16,32,64`, multiple `z`; identity-order and stable-one-run positive controls.
- **Phase 23 inheritance:** previous exact geometric/sparse-difference Green executor and its 24 tests preserved; complete Phase 12–23 nested archive preserved for independent verification.

## 7. Attribution and nonclaims

Permutation-cycle rank and Sherman–Morrison–Woodbury are classical. Stable binary sorting is closely related to inverse riffle shuffles, which have a developed combinatorial literature (Diaconis–McGrath–Pitman, 1995). The finite rank formula and concentration estimate above are **project-specific derived consequences**, not an assertion of priority or external peer review. Related background:

- Diaconis, McGrath, Pitman, *Riffle shuffles, cycles, and descents*, Combinatorica 15 (1995), 11–29. https://doi.org/10.1007/BF01294457
- Phase 22 and 23 checkpoints, included in the nested archive.

**Final status:** Proven exact linear-size correction rank for random sorting, an explicit high-probability simultaneous all-stride rank obstruction, and an exact low-rank Green correction in the genuinely near-order case. No new `o(N log N)` FFT; worst-case algorithmic complexity and bit precision of general noncommuting Green networks remain unresolved.
