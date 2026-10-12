# ACWL — Affine Carry Weyl Ladder
## Candidate exact O(N log log N) Fourier theory

**Date:** 2026-10-12  
**Status:** proved 2-adic affine hierarchy + proved covariance-lift reduction + conjectural O(N) affine lift packet.  
**Goal:** exact full DFT on arbitrary fresh dense input, all N outputs explicit, all preparation/routing/arithmetic charged.

Conditional target:

\[
\boxed{T(N)=O(N\log\log N)}.
\]

This theory is built around the newest Phase 36 result: noncommuting full-period
affine Hamiltonian cycles such as \(x\mapsto5x+1\) and \(x\mapsto13x+1\)
escape the natural+bit-reversal bit-cut obstruction.

It is not another one-layer Green fit.  The aim is to use affine cycles as
**scale-doubling corrections** for partial Weyl covariance.

---

# 1. Partial Fourier covariance

Let

\[
N=2^w,\qquad
F_N[k,j]=\omega^{kj},
\]

with \(\omega\) a supplied primitive \(N\)-th root.

Let

\[
Xe_j=e_{j+1\bmod N},
\qquad
Z=\operatorname{diag}(1,\omega,\ldots,\omega^{N-1}).
\]

For \(1\le r\le w\), define the order-\(2^r\) coarse generators

\[
X_r=X^{N/2^r},
\qquad
Z_r=Z^{N/2^r}.
\]

Call an invertible operator \(M\) **r-covariant** when

\[
\boxed{
M X_r=Z_r M.
}
\tag{1}
\]

At \(r=w\),

\[
X_w=X,\qquad Z_w=Z,
\]

so full covariance is exactly the Phase-49 Fourier intertwiner relation.

If \(M_w\) is invertible and w-covariant, then

\[
M_w=\operatorname{diag}(M_we_0)\,F_N,
\]

hence one row normalization gives the exact DFT.

Thus we do not need to construct Fourier in one shot.
We only need to lift

\[
r\to2r
\]

covariance repeatedly.

---

# 2. Safe correction lemma

## Lemma 2.1

Suppose \(M\) is r-covariant and \(C\) commutes with \(Z_r\):

\[
CZ_r=Z_rC.
\]

Then \(CM\) is also r-covariant.

### Proof

\[
CMX_r=CZ_rM=Z_rCM.
\]

QED.

So once the first \(r\) spectral bits have been resolved, every later
correction should lie in the commutant of \(Z_r\).

This prevents a macro layer from destroying already-established Fourier
structure.

---

# 3. Exact lift equation

Let \(s>r\), and assume \(M\) is r-covariant.

Define

\[
P_{r,s}=M X_s M^{-1}.
\]

Then

\[
P_{r,s}^{\,2^{s-r}}=Z_r.
\]

Hence \(P_{r,s}\) commutes with \(Z_r\).

Also \(Z_s\) commutes with \(Z_r\).

## Theorem 3.1 — covariance lifting

For an invertible \(C\) commuting with \(Z_r\),

\[
CM
\]

is s-covariant iff

\[
\boxed{
C P_{r,s}=Z_s C.
}
\tag{2}
\]

### Proof

\[
CMX_s=Z_sCM
\]

iff, multiplying by \(M^{-1}\),

\[
CMP_{r,s}=Z_sCM,
\]

iff

\[
CP_{r,s}=Z_sC.
\]

QED.

Thus each macro step is an intertwiner problem **inside the already-known
coarse commutant**.

---

# 4. Full-period affine Hamiltonian cycles

For an integer \(\rho\ge2\), define

\[
a_\rho=1+2^\rho
\]

and

\[
\pi_\rho(x)=a_\rho x+1\pmod{2^w}.
\]

Because

\[
a_\rho\equiv1\pmod4
\]

and the increment is odd, the classical Hull-Dobell criterion gives one
Hamiltonian \(N\)-cycle.

The t-th orbit point from zero is

\[
\boxed{
\psi_\rho(t)
=
1+a_\rho+\cdots+a_\rho^{t-1}
=
\frac{a_\rho^t-1}{a_\rho-1}
\pmod N.
}
\tag{3}
\]

This gives an explicit all-N affine cycle order.

---

# 5. New exact 2-adic orbit theorem

## Theorem 5.1 — affine orbit is a 2-adic isometry

For \(a\equiv1\pmod4\) and

\[
\psi_a(t)=\frac{a^t-1}{a-1},
\]

one has, for all distinct integers \(t,u\),

\[
\boxed{
v_2(\psi_a(t)-\psi_a(u))
=
v_2(t-u).
}
\tag{4}
\]

### Proof

Assume \(t>u\). Then

\[
\psi_a(t)-\psi_a(u)
=
a^u\psi_a(t-u).
\]

Since \(a\) is odd, \(v_2(a^u)=0\).

For \(m=t-u\), the 2-adic lifting-the-exponent identity gives, because
\(a\equiv1\pmod4\),

\[
v_2(a^m-1)=v_2(a-1)+v_2(m).
\]

Therefore

\[
v_2(\psi_a(m))
=
v_2(a^m-1)-v_2(a-1)
=
v_2(m).
\]

QED.

### Consequences

For every \(r\),

\[
t\equiv u\pmod{2^r}
\iff
\psi_a(t)\equiv\psi_a(u)\pmod{2^r}.
\]

So the affine Hamiltonian orbit preserves the **entire binary residue tree**.

In particular,

\[
\boxed{
v_2\bigl(\psi_a(t+2^r)-\psi_a(t)\bigr)=r.
}
\tag{5}
\]

A time jump of \(2^r\):

- preserves all lower \(r\) bits;
- changes bit \(r\);
- never collapses two different binary-prefix classes.

This is the exact carry hierarchy ACWL exploits.

---

# 6. The affine relative shear

Let \(S\) be the natural cyclic shift permutation

\[
S(x)=x+1.
\]

Define

\[
H_\rho=\pi_\rho\circ S^{-1}.
\]

Then

\[
\begin{aligned}
H_\rho(x)
&=
(1+2^\rho)(x-1)+1\\
&=
x+2^\rho(x-1)
\pmod N.
\end{aligned}
\]

Therefore

\[
\boxed{
H_\rho(x)\equiv x\pmod{2^\rho}.
}
\tag{6}
\]

So \(H_\rho\) never moves a coordinate between two residue classes modulo
\(2^\rho\).

But \(Z_\rho\) has exactly those residue classes as its eigenspaces.

Hence the permutation matrix of \(H_\rho\) commutes with \(Z_\rho\):

\[
\boxed{
H_\rho Z_\rho=Z_\rho H_\rho.
}
\tag{7}
\]

More generally, **every matrix supported only inside residue fibers modulo
\(2^\rho\)** commutes with \(Z_\rho\).

That includes:

- weighted versions of \(H_\rho\);
- sums of such fiber-preserving permutations;
- their Green resolvents whenever invertible;
- Cayley/scattering transforms built from them;
- QTGF-like sparse solves that do not cross the residue fibers.

Thus Phase 36's affine cycles generate an explicit fast correction algebra
inside the exact safe commutant required by Lemma 2.1.

---

# 7. Standard FFT proves the lift equation is consistent

Let \(M_r^{FFT}\) be bit reversal followed by the first \(r\) ordinary
radix-2 FFT stages.

Then exactly

\[
\boxed{
M_r^{FFT}X_r=Z_rM_r^{FFT}.
}
\tag{8}
\]

For \(s>r\), define

\[
C_{r\to s}^{FFT}
=
M_s^{FFT}(M_r^{FFT})^{-1}.
\]

Then:

\[
C_{r\to s}^{FFT}Z_r
=
Z_rC_{r\to s}^{FFT},
\]

and

\[
\boxed{
C_{r\to s}^{FFT}
P_{r,s}
=
Z_s C_{r\to s}^{FFT}.
}
\tag{9}
\]

So a covariance lift always exists.

The standard lift from \(r\) to \(2r\) costs

\[
\Theta(Nr)
\]

because it executes \(r\) more binary butterfly levels.

ACWL asks whether the same lift can be realized by one **global
fiber-preserving affine packet** in \(O(N)\).

---

# 8. Affine Carry Doubling Conjecture

Let

\[
s=\min(2r,w),
\qquad
r\ge2.
\]

## Conjecture

There exists a constant-width packet \(C_r\) built from:

- a constant number of affine relative shears
  \[
  x\mapsto(1+c\,2^r)x+1
  \]
  compared against the natural shift, with odd/small fixed \(c\);
- weighted permutation Green resolvents on the resulting residue fibers;
- diagonal root-power masks;
- optionally one QTGF/nonuniform-scattering correction inside each fiber;

such that:

1. \(C_r\) commutes with \(Z_r\);
2. \(C_r\) satisfies
   \[
   C_rP_{r,s}=Z_sC_r;
   \]
3. \(C_r\) is invertible;
4. its coefficients/routing are generated in \(O(N)\);
5. one fresh application costs \(O(N)\);
6. no internal FFT of size \(2^r\) is executed independently in every
   residue fiber.

Call \(C_r\) an **Affine Carry Lift**.

This is the only major unproved step.

---

# 9. Conditional O(N log log N) theorem

Start at

\[
r_0=2.
\]

A radix-4 partial Fourier stage produces an invertible \(M_{r_0}\) in
\(O(N)\) work.

Now iterate

\[
r_{\ell+1}=\min(2r_\ell,w).
\]

The number of lifts is

\[
L
=
O(\log w)
=
O(\log\log N).
\]

If every Affine Carry Lift costs \(O(N)\), then

\[
M_w
=
C_{L-1}\cdots C_1C_0M_2
\]

is fully w-covariant:

\[
M_wX=ZM_w.
\]

Because \(M_w\) is invertible,

\[
M_w=\operatorname{diag}(M_we_0)F_N.
\]

One final \(O(N)\) row normalization gives

\[
\boxed{
T_{\rm DFT}(N)=O(N\log\log N).
}
\tag{10}
\]

This would asymptotically beat both classical \(N\log N\) and the current
fixed-\(\delta\) power-saving comparator.

---

# 10. Why Phase 36 specifically motivates the affine ladder

Phase 36 proves that the old natural + bit-reversal cycle family fails on a
middle-bit Fourier cross-cut for every admissible weight at \(N\ge64\).

But it explicitly tests the noncommuting affine Hamiltonian cycles

\[
x\mapsto5x+1,
\qquad
x\mapsto13x+1,
\]

and these pass:

- all single-bit cut gates tested;
- all half-size consecutive-interval gates tested;

through the reported dyadic lengths.

Passing is not Fourier.

But those affine cycles are qualitatively different because their relative
shears are fiber-preserving at controlled 2-adic scales.

ACWL uses that exact structure instead of treating them as generic
high-expansion graphs.

---

# 11. Why the architecture escapes old no-go results

### Phase 51 single-Green depth
A product of individual Green resolvents needs \(\Omega(\log N)\) depth.
ACWL uses **constant-width packets/sums/scattering inside each lift**, not
one Green factor per level.

### Phase 52/55 single additive Green layer
Fixed-q one-layer sums cannot remain full-spark at all lengths.
ACWL is a multiscale product whose each layer preserves already-established
Weyl covariance.

### Phase 53 translated cycles
Affine cycles \(x\mapsto ax+1\), \(a\ne1\), are not translation-step cycles.
The simultaneous translated-cycle cut theorem does not cover them.

### Phase 54/55 Hall/full-spark
Those theorems show topology alone is insufficient.
ACWL imposes the exact finer Weyl relation (2) at every lift.

### Weyl/metaplectic rigidity
A candidate lift that secretly carries the complete primitive Weyl pair is
rejected as Fourier-hard.
Each ACWL lift is allowed to manipulate only the unresolved high-bit
degrees while commuting with the already fixed coarse modulation.

---

# 12. Relation to CGSF and SCBF

CGSF says many binary cycle-fissions should be macro-fused.

SCBF says two fast coordinate systems may meet at one common sparse
dynamics.

ACWL supplies a much more explicit search algebra:

\[
\boxed{
\text{fiber-preserving 2-adic affine shears}
}
\]

inside the coarse Weyl commutant.

Rather than search the entire commutant, the lift is restricted to an
all-N family with:

- explicit Hamiltonian cycle formulas;
- exact binary hierarchy;
- linear-time permutation generation;
- linear-time Green solves;
- known escape from the newest fixed bit-cut obstruction.

This makes the macro-fission problem substantially more concrete.

---

# 13. First decisive experiment

Use

\[
N=256,\qquad w=8.
\]

The ladder is only

\[
2\to4\to8.
\]

1. Build exact \(M_2^{FFT}\).
2. Compute
   \[
   P_{2,4}=M_2X_4M_2^{-1}.
   \]
3. Parameterize \(C_2\) using shears generated by multipliers
   \[
   5,\;13,\;21,\ldots
   \]
   plus diagonal phase masks.
4. Enforce only
   \[
   C_2P_{2,4}=Z_4C_2.
   \]
5. Do **not** fit \(F_{256}\).
6. If solved, repeat for
   \[
   4\to8
   \]
   using multipliers \(1+c16\).
7. Verify the final operator with Phase 49.

A success at these two lift equations would be far more informative than a
small Fourier-row fit.

---

# 14. Strong falsifiers

Reject ACWL if any of the following is proved.

1. Every invertible solution of
   \[
   CP_{r,2r}=Z_{2r}C
   \]
   inside the fiber-preserving affine/Green algebra requires
   \(\Omega(Nr)\) arithmetic.

2. The affine shear algebra has insufficient dimension/rank to implement
   the standard lift for growing \(r\).

3. Any successful affine lift is blockwise equivalent to performing
   \(2^r\)-point FFTs independently in all coarse residue fibers.

4. Coefficient generation for a nominally \(O(N)\) lift costs
   \(\Omega(Nr)\).

5. A new multibit separator gives an all-weight obstruction to every
   constant-width affine packet.

Any of these would convert the theory into a meaningful restricted lower
bound on covariance-doubling circuits.

---

# 15. Prior-art boundary

Classical ingredients include:

- Hull-Dobell full-period conditions for mixed congruential generators;
- 2-adic/LTE identities;
- compatible permutations of \(\mathbb Z/2^w\);
- radix-2 partial Fourier diagonalization;
- commutants and intertwiners.

The project-specific synthesis is:

\[
\boxed{
\text{partial Weyl covariance}
+
\text{2-adic affine carry shears}
+
\text{covariance doubling}
\Longrightarrow
O(N\log\log N)\text{ target}.
}
\]

The affine-orbit arithmetic itself is not claimed as new number theory.
The proposed use as an exact Fourier macro-lift compiler is the research
hypothesis.

---

# Bottom line

Ordinary FFT resolves spectral bits one at a time:

\[
1\to2\to3\to\cdots\to w.
\]

ACWL tries to resolve them by doubling:

\[
2\to4\to8\to16\to\cdots\to w.
\]

The exact reason affine cycles are suitable is:

\[
x\mapsto(1+2^r)x+1
\]

differs from ordinary increment only in bits at scale \(r\) and above, while
its relative shear commutes with the already-resolved coarse modulation.

If one \(O(N)\) affine packet can realize each exact lift

\[
r\to2r,
\]

then

\[
\boxed{
\operatorname{DFT}_N=O(N\log\log N).
}
\]
