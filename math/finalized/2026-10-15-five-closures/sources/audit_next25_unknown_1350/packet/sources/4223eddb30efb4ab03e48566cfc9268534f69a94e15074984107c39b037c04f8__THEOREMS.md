# HERO #0 — Phase 17: two-sided Green-gauge Fourier rigidity

**10 October 2026. Status:** Algebraically proved restricted no-go theorems, explicit spectral bound, numerical and finite-field verification. **No universal exact O(N) or O(N log log N) FFT; independent novelty not established.**

## 0. Setting

Let `F_N[k,j]=omega^(k*j)` with primitive `omega=exp(-2*pi*i/N)` and `U_N=F_N/sqrt(N)`. A monomial matrix has exactly one nonzero entry per row and column. Write `Q e_j=q_j e_(tau(j))` and `R e_m=r_m e_(sigma(m))`, where all weights are nonzero.

For even `s`, `N=s^2`, `h=s/2`, and indices `j=s*x+y`, define the half-grid involution

`tau(j)=s*x+((y+h) mod s)`.

The four classical Margulis permutation topologies commute with this tau. Any constant-weight sums/products of their Green resolvents therefore commute with its permutation matrix `Pi`. The material in this phase applies to **every Pi-commuting reference operator**, not only to these Green resolvents.

## 1. Paired-monomial Fourier normalizer — exact classification

**Theorem 17.1.** `F_N Q=R F_N` if and only if there are residues `a,b`, a unit `u` modulo `N`, and nonzero scalar `c` such that

```
tau(j)       = u*j+b          (mod N)
q_j          = c*omega^(a*j)
sigma(m)     = u^-1*(m-a)     (mod N)
r_m          = c*omega^(u^-1*(m-a)*b).
```

The result holds over any field with a primitive Nth root and characteristic not dividing N. **It is a standard type of Fourier/monomial automorphism identity**; we do not claim its discovery as a novel theorem. The project uses it as a precise certificate, extending Phase 16's *commuting* case (`Q=R`) to distinct input/output monomial operators.

**Proof.** In Fourier coordinates, for all k,j,

`q_j omega^(k*tau(j)) = r_(sigma^-1(k)) omega^(sigma^-1(k)*j)`.   (1)

Set `b=tau(0)` and `a=sigma^-1(0)`. At j=0, (1) implies `r_(sigma^-1(k))=q_0 omega^(k*b)`. At k=0, this implies `q_j=q_0 omega^(a*j)`. Cancel in (1):

`k*(tau(j)-b)=(sigma^-1(k)-a)*j (mod N)`.

Putting j=1 gives `sigma^-1(k)=u*k+a`, with `u=tau(1)-b`. Bijectivity forces `u` to be a unit. Putting k=1 then gives `tau(j)=u*j+b`. The j=0 equation supplies r_m as stated, with c=q_0. Reversing these steps proves sufficiency. QED.

## 2. Independent input and output diagonal gauges still cannot realize Fourier

**Theorem 17.2 (two-sided gauge obstruction).** For every even `s>=4`, let `T0` be any N-by-N complex matrix with `T0 Pi=Pi T0`. For any invertible complex diagonal matrices `D_in,D_out`,

`T=D_out T0 D_in^-1 != F_N` and `T!=U_N`.

**Proof.** Define `Q=D_in Pi D_in^-1` and `R=D_out Pi D_out^-1`. Then `TQ=RT`. Both Q and R are monomial with the *same* underlying permutation tau. If T were F_N, Theorem 17.1 would require tau affine modulo N. For s>=4, tau(0)=h and tau(1)=h+1, so the only possible affine expression is `j+h`. But tau(h)=0, whereas `h+h=s` is not 0 modulo `s^2`. Contradiction. The same argument applies to U_N because scalar normalization cancels. QED.

**Architecture scope.** This covers independent external diagonal preprocessing/postprocessing of any half-grid-invariant Green network. It also covers a sequence of internally gauged symmetric stages `D_l L_l^0 D_l^-1` whenever each intervening diagonal bridge `D_l^-1 D_(l-1)` commutes with Pi: then the whole product is of the specified two-sided form. **Arbitrary independent vertex weights and curvature-bearing bridges that do not commute with Pi are not excluded.**

**Small-size exception:** for s=2, tau(j)=1-j modulo 4 *is* affine. Choosing u=-1,b=1,a=1 and `c` with `c^2=omega_4^-1` yields involutory monomial Q,R with support tau and `F4 Q=R F4`. Since these involutions have no fixed points, each is a diagonal conjugate of Pi. This is independently checked exactly over GF(65537); therefore s=2 cannot be inserted into the theorem.

## 3. Explicit rank-four Fourier phase-ratio spectrum

Now assume the gauges are unitary (|diagonal entries|=1). Let

`H[k,j]=omega^(k*tau(j)-tau(k)*j)`.

Define `epsilon_j=+1` if j mod s<h and -1 otherwise; then `tau(j)=j+h*epsilon_j`, so

`H[k,j]=alpha^(k*epsilon_j-j*epsilon_k)`, `alpha=omega^h`.

**Theorem 17.3.** Put

`n=N/2`, `rho=2/(s*sin(pi/s))`, with `0<rho<1` for even s>=4.

Then H has precisely four nonzero singular values,

```
n*(1+rho), n*sqrt(1-rho^2), n*sqrt(1-rho^2), n*(1-rho).
```

In particular,

`||H||_2 = N*(1+rho)/2 = N*(1/2+1/(s*sin(pi/s)))`.

**Proof.** Partition rows and columns by epsilon=+/- (both groups of size n). On each sign block (e,f),

`H_(e,f)[k,j] = alpha^(f*k) alpha^(-e*j)`.

Each block is an outer product. Assemble four normalized row vectors indexed by pairs (e,f), and four normalized column vectors indexed by pairs (e,f), into N-by-4 matrices A and B. Then `H=n A B^T` and H has rank <=4.

The two row vectors in a fixed sign group have normalized inner product `gamma_e=(1/n)*sum_(k:epsilon_k=e) alpha^(-2k)`. The plus-group value has modulus rho: the length-h geometric sum has magnitude `1/sin(pi/s)`, and each y contributes s choices of x. The minus-group value is its negative. The analogous column Gram overlap is its complex conjugate, again with a sign reversal in the other group. Rephase the four coordinates to make the row and transposed-column Gram matrices simultaneously real:

```
A* A = [[1,rho,0,0],[rho,1,0,0],
        [0,0,1,-rho],[0,0,-rho,1]]
(B* B)^T = [[1,0,rho,0],[0,1,0,-rho],
             [rho,0,1,0],[0,-rho,0,1]].
```

The characteristic polynomial of their product is

`(lambda-(1+rho)^2)*(lambda-(1-rho)^2)*(lambda-(1-rho^2))^2`.

This follows by direct multiplication; the exact symbolic certificate is `test_four_by_four_gram_characteristic_polynomial`. Nonzero eigenvalues of `H H* / n^2` agree with those of that 4-by-4 Gram product. Taking square roots proves the result. Since rho<1, all four singular values are nonzero. QED.

At s=2, rho=1 and H has rank one; the spectral bound degenerates, consistent with the small exception.

## 4. Improved uniform error gap with *independent* phase gauges

**Theorem 17.4 (operator and relative-Frobenius gap).** For every even s>=4 and every Pi-commuting T0, let `D_in,D_out` be **unitary diagonal** and `T=D_out T0 D_in^-1`. Then

```
||U_N-T||_2 >= g_s
||U_N-T||_F/||U_N||_F >= g_s

g_s = 1/2 * sqrt(1-2/(s*sin(pi/s))) > 0.
```

As s -> infinity, `g_s -> (1/2)*sqrt(1-2/pi) = 0.30140513749454345...`.

**Proof.** Let Q and R be the unitary monomial involutions of Theorem 17.2, so `TQ=RT`. Their respective nonzero entries have unit modulus, denoted q_j and r_m. Directly from the Fourier matrix entries,

`(UQ-RU)[k,j] = (omega^(tau(k)*j)/sqrt(N)) * (q_j H[k,j] - r_(tau(k)))`.

Multiplication by a unit scalar does not change entry magnitude. Let `a_k=r_(tau(k))` and `b_j=q_j^-1`, both unit-modulus. Then

`||UQ-RU||_F^2 = (1/N)*||H-a*b^T||_F^2`.

Both H and `a*b^T` have Frobenius norm N. Using the singular-value bound from Theorem 17.3 and Cauchy–Schwarz,

`Re< H,a*b^T > <= ||H||_2 * ||a||_2 * ||b||_2 <= N^2*(1+rho)/2`.

Therefore

`||UQ-RU||_F^2 >= (1/N)*(2N^2-N^2*(1+rho)) = N*(1-rho)`.

Because TQ=RT and Q,R are unitary,

`||UQ-RU||_F <= ||(U-T)Q||_F+||R(U-T)||_F = 2||U-T||_F`.

Hence `||U-T||_F/sqrt(N) >= sqrt(1-rho)/2 = g_s`. Finally `||U-T||_2 >= ||U-T||_F/sqrt(N)` establishes the operator-norm claim. QED.

**Scope caution:** The exact Theorem 17.2 holds for arbitrary nonunitary D_in/D_out. The *numerical bound* in Theorem 17.4 is proved only for unitary diagonal gauges. Our g_s is a guaranteed floor, **not** necessarily the exact minimum error over the restricted network family.

## 5. Generic rank-defect extension (not for every gauge)

If `T_g=D_out T0 D_in^-1` intertwines Q and R, then a rank-k perturbation E gives

`rank((T_g+E)Q-R(T_g+E)) <= 2k`.

Every individual change to one weighted-permutation entry in an invertible Green resolvent changes that resolvent by rank at most one (resolvent identity). Telescoping sums and products gives rank(T-T_g)<=k when k such **edge-weight occurrences** are changed from a valid reference, so the defect rank is at most 2k.

The Fourier defect `F_N Q-R F_N` has full rank N for **Zariski-generic** independent diagonal gauges: its determinant is a rational function of the gauge entries, and at `D_in=D_out=I` Phase 15 already establishes full rank for this half-grid involution. This nonzero specialization proves that its determinant numerator is not identically zero. Consequently, for such generic gauge pairs, exact Fourier equality requires `k>=N/2`.

This statement does **not** assert a full-rank defect for every gauge. The exact small-size checks show full rank for the saved random samples and for the identity-gauge specialization. k counts individual resolvent-weight occurrences, not distinct shared parameters.

## 6. Research boundary and next gate

- Positive: a closed-form, size-uniform, stronger non-approximation theorem for **independent** left/right phase gauges, and a precise field-exact normalizer test that excludes the associated exact factorizations.
- Negative: no general `O(N)` or `O(N log log N)` exact FFT; no factorization of F16 found.
- Remaining: genuinely curvature-bearing (non-coboundary) input-dependent-independent *graph weights* across mixed-axis layers whose interstage diagonal bridges **do not** commute with half-grid symmetry.
- Literature: Fourier matrix monomial automorphism groups are established. A recent presentation is *Equivalence of complex Hadamard matrices*, Journal of Algebraic Combinatorics, 2026, Theorem 9, showing `Aut(F_n) ~ (C_n x C_n) semidirect (Z/nZ)^units`. The project-specific spectral/error conjunction is not independently vetted for priority.

## 7. Reproduction

```bash
cd fft_hero0_phase17_two_sided_gauge
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase17
python phase17_gauge.py
```

The tests include exact modular Fourier intertwiners for 24+ affine parameter choices, s=2 exact gauge exception, two-sided random-gauge full-rank certificates at N=16 and 64, 4-by-4 exact symbolic characteristic polynomial, complex ratio spectra, arbitrary phase-gauge residual bounds, valid symmetric Margulis reference layers, and one-edge Green-resolvent rank perturbations.

## 8. Exact best Frobenius projection (fixed gauges)

**Theorem 17.5.** For any fixed *unitary involutions* Q,R and unitary Fourier matrix U, among all matrices satisfying `TQ=RT`, the Frobenius-closest matrix to U is

`T_star=(U+R U Q)/2`, with `||U-T_star||_F=||UQ-RU||_F/2`.

**Proof.** On the Hilbert space of N-by-N matrices with Frobenius inner product, the map `X -> R X Q` is a self-adjoint unitary involution when Q and R are unitary Hermitian involutions. The +1 eigenspace is precisely the intertwiner space `TQ=RT`. Orthogonal projection onto that eigenspace is `(I+L)/2`, yielding T_star. The error is `(U-RUQ)/2`; multiplying on the right by Q preserves Frobenius norm and gives `(UQ-RU)/2`. QED.

This establishes the precise best approximation **for fixed gauges in the enlarged class of all matrices with the intertwining symmetry**. T_star generally requires a Fourier transform to apply and is not itself a new O(N)-work circuit. The explicit lower bound of Theorem 17.4 follows for this optimal projection too, but need not be sharp across all possible choices of gauges.

An additional regression verifies the multi-stage interpretation: two separately conjugated constant-weight Green resolvents, with a different unitary diagonal gauge on each stage, still reduce to the two-sided form provided the interstage diagonal ratio commutes with Pi. The two gauges are different and their ratio need not be a scalar.

## 9. New uniform linear defect budget and rank-versus-accuracy tradeoff

The generic-rank theorem in Section 5 requires excluding a special algebraic set of gauges. This section supplies a **uniform result for every pair of unitary diagonal gauges**, at the price of a smaller but explicit constant.

**Theorem 17.6 (any-gauge rank-k approximation barrier).** Let s>=4 be even and N=s^2. Choose *any* unitary diagonal D_in,D_out and any Pi-commuting T0, and set `T_g=D_out T0 D_in^-1`. Let `Delta` be any matrix with rank <=k, and `T=T_g+Delta`. Put `rho=2/(s*sin(pi/s))`. Then

```
||U_N-T||_2 >= 1/2*sqrt(max(0,1-rho-8*k/N)),
||U_N-T||_F/sqrt(N) >= 1/2*sqrt(max(0,1-rho-8*k/N)).
```

In particular, **exact equality T=U_N is impossible unless**

`k >= ceil(N*(1-rho)/8)`, which is `~0.0454225*N` as s grows.

This is a *restricted uniform Ω(N) rank/edge-defect necessity*, not an unrestricted FFT lower bound.

**Proof.** For the Q and R from Theorem 17.2, write `E=UQ-RU`. Section 4 established `||E||_F^2>=N*(1-rho)` and `||E||_2<=||UQ||_2+||RU||_2=2`. Since T_g intertwines Q,R,

`E = ((U-T)Q-R(U-T)) + (Delta Q-R Delta)`.

The second term has rank at most 2k. By the optimal low-rank approximation bound (Eckart–Young),

```
||E-(Delta Q-R Delta)||_F^2
 >= ||E||_F^2 - sum_of_top_2k_singular_values(E)^2
 >= N*(1-rho)-8*k.
```

The left side equals `|| (U-T)Q-R(U-T)||_F^2` and is bounded above by `4||U-T||_F^2`. Divide by 4N, take square roots, and use `||U-T||_2>=||U-T||_F/sqrt(N)`. For exact equality the right-hand lower bound must vanish, giving the integer budget. QED.

### Consequence for a genuinely asymmetric interstage bridge

Suppose `L1,L2` both commute with Pi and can be executed by a constant number of Green resolvents. Let the candidate be

`T = D_out L2 B L1 D_in^-1`,

where `B` is an **arbitrary invertible diagonal bridge** and D_in,D_out are unitary diagonal. Let `k` be the number of half-grid transposition pairs `{j,tau(j)}` on which the two diagonal entries of B differ. Choose a nonzero Pi-invariant diagonal B0 that agrees with B on one entry of each pair; then `rank(B-B0)<=k` and `B0` commutes with Pi. Thus

`T_g = D_out L2 B0 L1 D_in^-1`

is a two-sided gauged Pi-invariant reference, and `rank(T-T_g)<=k`. The theorem applies. Therefore **even arbitrary bridge asymmetry must break at least ceil(N(1-rho)/8) distinct half-grid pairs to permit exact Fourier** in this two-layer grammar. No genericity caveat is needed for the unitary outer gauges.

Similarly, if k individual weighted-permutation entries of a valid phase-gauged Green-reference network are changed while keeping all relevant inverses invertible, rank(T-T_g)<=k by telescoping. The same lower bound and approximation floor apply, counting each modified resolvent occurrence separately.

### Why this is not a universal FFT result

The theorem permits changing Θ(N) edges, which still costs only O(N) to specify and execute in many sparse graph models. It therefore does **not** rule out the original dream. It identifies a necessary *scale of symmetry-breaking curvature* for this particular Green construction. More general non-diagonal interstage networks and independent arbitrary vertex weights can escape the assumptions.
